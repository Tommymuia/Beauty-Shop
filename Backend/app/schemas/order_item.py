from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal
from typing import Optional
from app.schemas.product import ProductOut

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemOut(OrderItemBase):
    id: int
    order_id: int
    price_at_purchase: Decimal
    product: Optional[ProductOut] = None

    model_config = ConfigDict(from_attributes=True)