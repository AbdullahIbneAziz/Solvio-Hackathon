from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

class SaleBase(BaseModel):
    branch_id: int
    product_id: int
    customer_id: Optional[int] = None
    quantity: float
    total_price: float
    sale_date: date

class SaleCreate(BaseModel):
    branch_id: int
    product_id: int
    customer_id: Optional[int] = None
    quantity: float

class SaleUpdate(BaseModel):
    product_id: Optional[int] = None
    customer_id: Optional[int] = None
    quantity: Optional[float] = None

class SaleResponse(SaleBase):
    id: int
    staff_id: int
    created_at: datetime

    class Config:
        from_attributes = True

