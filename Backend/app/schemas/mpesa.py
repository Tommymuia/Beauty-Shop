from pydantic import BaseModel, Field
from typing import Optional

class MpesaPaymentRequest(BaseModel):
    order_id: int
    phone_number: str = Field(..., pattern=r"^254\d{9}$", description="Phone number in format 254XXXXXXXXX")

class MpesaCallbackResponse(BaseModel):
    ResultCode: int
    ResultDesc: str

class MpesaTransactionStatus(BaseModel):
    checkout_request_id: str
    status: str
    receipt_number: Optional[str] = None