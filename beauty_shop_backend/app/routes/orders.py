from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Order, CartItem, Product
from app.schemas import OrderResponse
from app.routes.auth import get_current_user
from app.utils.mpesa import initiate_stk_push
from app.utils.invoice import generate_invoice_pdf
import uuid

router = APIRouter()

@router.post("/checkout")
def checkout(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # 1. Get Cart Items
    cart_items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # 2. Calculate Total
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    # 3. Generate Invoice Number
    invoice_no = f"INV-{uuid.uuid4().hex[:6].upper()}"
    
    # 4. Create Order in DB
    new_order = Order(
        user_id=current_user.id,
        total_amount=total,
        invoice_number=invoice_no,
        status="pending"
    )
    db.add(new_order)
    
    # Clear cart
    db.query(CartItem).filter(CartItem.user_id == current_user.id).delete()
    db.commit()
    db.refresh(new_order)

    # 5. GENERATE PDF INVOICE
    # This saves a file in the /invoices folder
    pdf_path = generate_invoice_pdf(
        invoice_number=invoice_no, 
        amount=total, 
        email=current_user.email
    )

    # 6. TRIGGER M-PESA STK PUSH
    # Note: current_user.phone_number must be in format 2547XXXXXXXX
    mpesa_response = {}
    try:
        mpesa_response = initiate_stk_push(
            phone=current_user.phone_number,
            amount=int(total),
            invoice_no=invoice_no
        )
    except Exception as e:
        mpesa_response = {"error": str(e)}

    return {
        "message": "Checkout initiated",
        "order_details": {
            "id": new_order.id,
            "invoice": invoice_no,
            "total": total
        },
        "pdf_location": pdf_path,
        "mpesa_status": mpesa_response
    }