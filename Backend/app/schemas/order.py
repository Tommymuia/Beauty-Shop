from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional
from decimal import Decimal
from app.schemas.order_item import OrderItemOut, OrderItemCreate
from app.schemas.user import UserOut

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    mpesa_receipt_number: Optional[str] = None

class OrderOut(BaseModel):
    id: int
    user_id: int
    total_amount: Decimal
    status: str
    created_at: datetime
    items: List[OrderItemOut]
    user: Optional[UserOut] = None

    model_config = ConfigDict(from_attributes=True)