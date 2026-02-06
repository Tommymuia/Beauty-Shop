from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Order, CartItem
from app.routes.auth import get_current_user
from app.utils.mpesa import initiate_stk_push
from app.utils.invoice import generate_invoice_pdf
import uuid

router = APIRouter()

@router.post("/checkout")
def checkout(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # 1. Validate Cart
    cart_items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # 2. Get Phone Number with a "Test Fallback"
    # This tries the DB first, but defaults to your number if the DB is empty
    db_phone = getattr(current_user, 'phone_number', None) or getattr(current_user, 'phone', None)
    
    # FOR TESTING: If DB phone is missing, use your real number so you can see the STK Push
    user_phone = db_phone if db_phone else "254707996007" 

    # 3. Financials & Invoice Prep
    total = sum(item.product.price * item.quantity for item in cart_items)
    invoice_no = f"INV-{uuid.uuid4().hex[:6].upper()}"
    
    # 4. Save Order & Clear Cart
    new_order = Order(
        user_id=current_user.id,
        total_amount=total,
        invoice_number=invoice_no,
        status="pending"
    )
    db.add(new_order)
    
    # Important: We clear the cart here so the user doesn't double-order
    db.query(CartItem).filter(CartItem.user_id == current_user.id).delete()
    db.commit()
    db.refresh(new_order)

    # 5. Generate PDF
    pdf_path = generate_invoice_pdf(invoice_no, total, current_user.email)

    # 6. M-Pesa Trigger
    # Using the 'user_phone' logic from above
    try:
        mpesa_response = initiate_stk_push(
            phone=user_phone,
            amount=int(total),
            invoice_no=invoice_no
        )
    except Exception as e:
        mpesa_response = {"error": "M-Pesa Service Unavailable", "details": str(e)}

    return {
        "message": "Checkout initiated",
        "order_details": {
            "id": new_order.id, 
            "invoice": invoice_no, 
            "total": total,
            "phone_used": user_phone # To confirm which number was sent
        },
        "pdf_location": pdf_path,
        "mpesa_status": mpesa_response
    }