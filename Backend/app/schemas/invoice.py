from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal

class InvoiceBase(BaseModel):
    invoice_number: str
    total_amount: Decimal
    status: Optional[str] = "generated"
    file_path: Optional[str] = None

class InvoiceCreate(BaseModel):
    order_id: int
    
class InvoiceOut(InvoiceBase):
    id: int
    order_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)