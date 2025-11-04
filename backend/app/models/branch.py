from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Branch(Base):
    __tablename__ = "branches"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    address = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    staff = relationship("User", back_populates="branch")
    inventory_items = relationship("Inventory", back_populates="branch")
    sales = relationship("Sale", back_populates="branch")
    customers = relationship("Customer", back_populates="branch")

