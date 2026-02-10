import time
import json
from app.models import Order


def create_order_record(db, payload):
    """Create and persist an Order from frontend-shaped payload.
    Returns the Order ORM object.
    """
    public_id = f"ORD-{int(time.time() * 1000)}"

    # Set status based on payment method
    status = 'Paid' if payload.paymentMethod == 'mpesa' else 'Processing'

    new_order = Order(
        public_id=public_id,
        total_amount=payload.total,
        status=status,
        invoice_number=f"INV-{public_id[-8:]}"
    )
    # store customer json with payment info
    customer_data = payload.customer.dict()
    customer_data['paymentMethod'] = payload.paymentMethod
    if payload.paymentMethod == 'mpesa' and hasattr(payload, 'mpesaPhone'):
        customer_data['mpesaPhone'] = payload.mpesaPhone
    if hasattr(payload, 'transactionId'):
        customer_data['transactionId'] = payload.transactionId
    
    new_order.set_customer(customer_data)

    # ensure items include totalPrice
    items = []
    for it in payload.items:
        item = it.dict()
        if 'totalPrice' not in item or item['totalPrice'] is None:
            item['totalPrice'] = item.get('price', 0) * item.get('quantity', 1)
        items.append(item)
    new_order.set_items(items)

    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


def fetch_order_by_public_id(db, public_id: str):
    return db.query(Order).filter(Order.public_id == public_id).first()
