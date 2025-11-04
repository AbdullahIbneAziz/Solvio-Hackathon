from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    quantity = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    sale_date = Column(Date, nullable=False, server_default=func.current_date())
    staff_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    branch = relationship("Branch", back_populates="sales")
    product = relationship("Product", back_populates="sales")
    customer = relationship("Customer", back_populates="sales")
    staff_member = relationship("User", back_populates="sales")

