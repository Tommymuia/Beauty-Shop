from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import Field
from typing import Any

# Auth
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    is_admin: Optional[bool] = None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    is_admin: bool = False
    class Config: from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# Product & Category
class CategorySchema(BaseModel):
    id: int
    name: str
    class Config: from_attributes = True

class ProductSchema(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    stock_quantity: int = 0
    category_id: int
    class Config: from_attributes = True

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: Optional[int] = 0
    category_id: Optional[int] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    category_id: Optional[int] = None

# Cart
class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1

class CartItemResponse(BaseModel):
    id: int
    product: ProductSchema
    quantity: int
    class Config: from_attributes = True

# Order/Invoice
class OrderResponse(BaseModel):
    id: int
    total_amount: float
    invoice_number: Optional[str] = None
    status: str
    created_at: datetime
class OrderItemResponse(BaseModel):
    id: int
    product_name: str
    quantity: int
    price: float
    class Config: from_attributes = True

# Mpesa
class MpesaPaymentRequest(BaseModel):
    phone_number: str
    amount: int
    order_id: int

class MpesaCallbackResponse(BaseModel):
    MerchantRequestID: str
    CheckoutRequestID: str
    ResultCode: int
    ResultDesc: str
class MpesaTransactionStatus(BaseModel):
    status: str

# Frontend-shaped order models
class OrderItem(BaseModel):
    name: str
    quantity: int
    price: float
    totalPrice: float | None = None

class CustomerInfo(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    address: str
    city: str
    zip: str

class OrderCreate(BaseModel):
    customer: CustomerInfo
    items: List[OrderItem]
    total: float
    paymentMethod: str | None = None
    mpesaPhone: str | None = None

class OrderDetailResponse(BaseModel):
    id: str
    createdAt: datetime
    customer: CustomerInfo
    items: List[OrderItem]
    total: float
    status: str
    class Config:
        arbitrary_types_allowed = True
