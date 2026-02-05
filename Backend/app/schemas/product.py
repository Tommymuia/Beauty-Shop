from pydantic import BaseModel, ConfigDict
from typing import Optional
from decimal import Decimal
from app.schemas.category import CategoryOut

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    stock_qty: int
    category_id: int
    rating: Optional[float] = 0.0
    reviews_count: Optional[int] = 0
    is_new: Optional[bool] = False
    
class ProductCreate(ProductBase):
    image_url: Optional[str] = None
    
class ProductOut(ProductBase):
    id: int
    image_url: Optional[str] = None
    category: Optional[CategoryOut] = None 
    
    model_config = ConfigDict(from_attributes=True)