from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy.sql import func

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    total_amount = Column('total_price', Numeric(10, 2), nullable=True)  # FIXED
    status = Column(String, default="pending")
    mpesa_checkout_id = Column(String)
    mpesa_receipt = Column(String, index=True)
    phone_number = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")