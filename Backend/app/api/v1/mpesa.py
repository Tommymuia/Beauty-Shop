from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import get_db
from app.schemas.mpesa import MpesaPaymentRequest, MpesaCallbackResponse, MpesaTransactionStatus
from app.services.mpesa_service import mpesa_service
from typing import Optional

router = APIRouter(prefix="/api/v1/mpesa", tags=["mpesa"])

@router.post("/stk-push")
async def initiate_stk_push(
    payment_request: MpesaPaymentRequest,
    db: Session = Depends(get_db)
):
    """
    Initiate M-Pesa STK Push payment
    """
    try:
        # Get order details from database
        # order = db.query(Order).filter(Order.id == payment_request.order_id).first()
        # if not order:
        #     raise HTTPException(status_code=404, detail="Order not found")
        
        # For now, use a dummy amount - replace with actual order total
        amount = 1  # Replace with order.total_amount
        
        result = mpesa_service.initiate_stk_push(
            phone_number=payment_request.phone_number,
            amount=amount,
            order_id=str(payment_request.order_id)
        )
        
        if result.get("ResponseCode") == "0":
            # Save checkout request ID to order
            # order.mpesa_checkout_id = result.get("CheckoutRequestID")
            # db.commit()
            
            return {
                "success": True,
                "message": "STK Push initiated successfully",
                "checkout_request_id": result.get("CheckoutRequestID"),
                "customer_message": result.get("CustomerMessage")
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=result.get("errorMessage", "Failed to initiate payment")
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Payment initiation failed: {str(e)}")

@router.post("/callback")
async def mpesa_callback(callback_data: dict):
    """
    Handle M-Pesa callback response
    This endpoint should be publicly accessible
    """
    try:
        # Extract callback data
        result_code = callback_data.get("Body", {}).get("stkCallback", {}).get("ResultCode")
        result_desc = callback_data.get("Body", {}).get("stkCallback", {}).get("ResultDesc")
        checkout_request_id = callback_data.get("Body", {}).get("stkCallback", {}).get("CheckoutRequestID")
        
        if result_code == 0:
            # Payment successful
            # Extract transaction details
            callback_metadata = callback_data.get("Body", {}).get("stkCallback", {}).get("CallbackMetadata", {}).get("Item", [])
            
            receipt_number = None
            amount = None
            phone_number = None
            
            for item in callback_metadata:
                if item.get("Name") == "MpesaReceiptNumber":
                    receipt_number = item.get("Value")
                elif item.get("Name") == "Amount":
                    amount = item.get("Value")
                elif item.get("Name") == "PhoneNumber":
                    phone_number = item.get("Value")
            
            # Update order in database
            # order = db.query(Order).filter(Order.mpesa_checkout_id == checkout_request_id).first()
            # if order:
            #     order.status = "paid"
            #     order.mpesa_receipt = receipt_number
            #     order.phone_number = phone_number
            #     db.commit()
            
            return {
                "ResultCode": 0,
                "ResultDesc": "Payment received successfully",
                "receipt_number": receipt_number,
                "amount": amount
            }
        else:
            # Payment failed
            return {
                "ResultCode": result_code,
                "ResultDesc": result_desc
            }
    
    except Exception as e:
        return {
            "ResultCode": 1,
            "ResultDesc": f"Error processing callback: {str(e)}"
        }

@router.get("/status/{checkout_request_id}")
async def check_transaction_status(
    checkout_request_id: str,
    db: Session = Depends(get_db)
):
    """
    Check the status of a transaction
    """
    try:
        result = mpesa_service.query_transaction_status(checkout_request_id)
        
        return {
            "success": True,
            "status": result.get("status"),
            "checkout_request_id": checkout_request_id
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check status: {str(e)}")