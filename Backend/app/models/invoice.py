from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.db.base import Base
from sqlalchemy.sql import func

class Invoice(Base):
    __tablename__ = "invoices"  # FIXED
    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, unique=True, index=True, nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String, default="generated")
    file_path = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    order = relationship("Order", back_populates="invoices")