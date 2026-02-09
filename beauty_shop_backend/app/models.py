from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.database import Base
import json

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    address = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)
    
    orders = relationship("Order", back_populates="owner")
    cart_items = relationship("CartItem", back_populates="user", cascade="all, delete-orphan")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float)
    stock_quantity = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    
    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")
    cart_items = relationship("CartItem", back_populates="product")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    total_amount = Column(Float)
    invoice_number = Column(String, unique=True, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    mpesa_checkout_id = Column(String, nullable=True)
    mpesa_receipt = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    customer_info = Column(Text, nullable=True)

    owner = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def get_customer(self):
        if self.customer_info:
            return json.loads(self.customer_info)
        if self.owner:
            return {
                "firstName": self.owner.first_name,
                "lastName": self.owner.last_name,
                "email": self.owner.email,
                "address": self.owner.address,
                "city": "",
                "zip": ""
            }
        return None

    def get_items(self):
        return [
            {
                "name": item.product.name,
                "quantity": item.quantity,
                "price": item.price_at_purchase,
                "totalPrice": item.quantity * item.price_at_purchase,
            }
            for item in self.items
        ]

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price_at_purchase = Column(Float)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

class CartItem(Base):
    __tablename__ = "cart_items"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")
