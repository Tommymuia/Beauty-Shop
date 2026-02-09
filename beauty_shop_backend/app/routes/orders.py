from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from datetime import datetime, timezone
from app.database import get_db
from app.models import Order, OrderItem, CartItem, User, Product
from app.schemas import OrderCreate, OrderDetailResponse, OrderResponse
from app.services.order_service import create_order_record, fetch_order_by_public_id
from app.routes.auth import get_current_user
from app.utils.invoice import generate_invoice_pdf
from app.utils.email import send_invoice_email
import logging

router = APIRouter(prefix="/api/v1/orders", tags=["orders"])
logger = logging.getLogger(__name__)

# ======================
# PUBLIC ENDPOINTS (Guest checkout & invoice access)
# ======================

@router.post("/", response_model=OrderDetailResponse, status_code=status.HTTP_201_CREATED)
def create_guest_order(
    payload: OrderCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Guest checkout endpoint. 
    CRITICAL: Service layer MUST validate:
    - Product existence/active status
    - Stock availability (if tracked)
    - Recalculate total_amount server-side (prevent overposting)
    - Sanitize customer inputs
    """
    try:
        order_obj = create_order_record(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Order creation failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Order creation failed. Please try again."
        )
    
    # Schedule invoice generation/email in background (non-blocking)
    background_tasks.add_task(
        _generate_and_send_invoice,
        order_id=order_obj.id,
        invoice_number=order_obj.invoice_number or order_obj.public_id,
        customer_email=(order_obj.get_customer() or {}).get('email'),
        items=order_obj.get_items(),
        total_amount=order_obj.total_amount
    )
    
    return OrderDetailResponse(
        id=order_obj.public_id,
        createdAt=order_obj.created_at,
        customer=order_obj.get_customer(),
        items=order_obj.get_items(),
        total=order_obj.total_amount,
        status=order_obj.status
    )

@router.get("/{public_id}", response_model=OrderDetailResponse)
def get_public_order(public_id: str, db: Session = Depends(get_db)):
    """Secure public invoice access - ONLY active orders visible"""
    order = fetch_order_by_public_id(db, public_id)
    if not order or not order.is_active:  # Critical: prevent accessing deleted orders
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found or no longer available"
        )
    # Explicitly exclude sensitive fields in response model
    return OrderDetailResponse(
        id=order.public_id,
        createdAt=order.created_at,
        customer=order.get_customer(),
        items=order.get_items(),
        total=order.total_amount,
        status=order.status
    )

# ======================
# AUTHENTICATED ENDPOINTS (User-specific operations)
# ======================

@router.post("/from-cart", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order_from_cart(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Convert authenticated user's cart to order with full validation"""
    # Fetch cart items with product relationships (prevent N+1)
    cart_items = (
        db.query(CartItem)
        .filter(CartItem.user_id == current_user.id)
        .options(joinedload(CartItem.product))
        .all()
    )
    
    if not cart_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty"
        )
    
    # VALIDATE ALL ITEMS BEFORE ORDER CREATION
    validated_items = []
    total_amount = 0.0
    
    for item in cart_items:
        # Critical integrity checks
        if not item.product or not item.product.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product '{item.product.name if item.product else 'Unknown'}' is no longer available"
            )
        
        if item.quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid quantity for product {item.product_id}"
            )
        
        # Stock validation (if implemented in Product model)
        if hasattr(item.product, 'stock') and item.product.stock is not None:
            if item.product.stock < item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for '{item.product.name}'. Only {item.product.stock} available."
                )
        
        # Recalculate price using CURRENT price (prevent overposting)
        item_total = item.product.price * item.quantity
        total_amount += item_total
        validated_items.append({
            "product": item.product,
            "quantity": item.quantity,
            "price": item.product.price
        })
    
    # Create order with explicit fields
    try:
        new_order = Order(
            user_id=current_user.id,
            total_amount=round(total_amount, 2),
            invoice_number=f"INV-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}",
            status="pending",
            is_active=True,
            created_at=datetime.now(timezone.utc)
        )
        db.add(new_order)
        db.flush()  # Get ID without committing
        
        # Create order items with price-at-purchase snapshot
        for v_item in validated_items:
            db.add(OrderItem(
                order_id=new_order.id,
                product_id=v_item["product"].id,
                quantity=v_item["quantity"],
                price_at_purchase=v_item["price"]
            ))
        
        # Clear cart AFTER successful order item creation
        db.query(CartItem).filter(CartItem.user_id == current_user.id).delete()
        db.commit()
        db.refresh(new_order)
        
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Order creation DB error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Order creation failed due to database error"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected order error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error during order processing"
        )
    
    # Schedule invoice generation
    background_tasks.add_task(
        _generate_and_send_invoice,
        order_id=new_order.id,
        invoice_number=new_order.invoice_number,
        customer_email=current_user.email,
        items=[{
            "name": item["product"].name,
            "quantity": item["quantity"],
            "price": item["price"]
        } for item in validated_items],
        total_amount=new_order.total_amount
    )
    
    return new_order

@router.get("/my", response_model=List[OrderResponse])
def get_user_orders(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's order history with pagination"""
    limit = min(limit, 50)  # Prevent abuse
    return (
        db.query(Order)
        .filter(Order.user_id == current_user.id, Order.is_active == True)
        .options(
            joinedload(Order.order_items).joinedload(OrderItem.product)
        )
        .order_by(Order.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

@router.get("/my/{order_id}", response_model=OrderResponse)
def get_user_order_detail(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get specific order detail for authenticated user"""
    order = (
        db.query(Order)
        .filter(
            Order.id == order_id,
            Order.user_id == current_user.id,
            Order.is_active == True
        )
        .options(
            joinedload(Order.order_items).joinedload(OrderItem.product)
        )
        .first()
    )
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order

# ======================
# ADMIN ENDPOINTS (Require admin check - implement separately)
# ======================
# Note: Admin endpoints (list all orders, update status, etc.) should be 
# implemented in a separate admin router with explicit admin verification
# Example pattern:
# @admin_router.get("/")
# def list_all_orders(...):
#     verify_admin(current_user)
#     ...

# ======================
# HELPER FUNCTIONS
# ======================

def _generate_and_send_invoice(
    order_id: int,
    invoice_number: str,
    customer_email: Optional[str],
    items: list,
    total_amount: float
):
    """Background task: Generate PDF and send email with error isolation"""
    if not customer_email:
        logger.warning(f"Order {order_id}: No email for invoice delivery")
        return
    
    try:
        pdf_path = generate_invoice_pdf(
            invoice_number=invoice_number,
            total_amount=total_amount,
            customer_email=customer_email,
            items=items
        )
        send_invoice_email(
            recipient_email=customer_email,
            invoice_no=invoice_number,
            pdf_path=pdf_path
        )
        logger.info(f"Invoice sent successfully for order {order_id}")
    except Exception as e:
        # Critical: Log failure but DO NOT crash background task
        logger.error(
            f"Invoice generation/email failed for order {order_id}: {str(e)}",
            exc_info=True,
            extra={"order_id": order_id, "invoice_number": invoice_number}
        )