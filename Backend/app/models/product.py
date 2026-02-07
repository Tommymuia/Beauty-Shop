from sqlalchemy import Column, String, Integer, Numeric, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    stock_qty = Column(Integer, default=0)
    image_url = Column(String(500), nullable=True)
    rating = Column(Float, default=0.0)
    reviews_count = Column(Integer, default=0)
    is_new = Column(Boolean, default=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    category = relationship("Category", back_populates="products")