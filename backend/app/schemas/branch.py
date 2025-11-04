from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BranchBase(BaseModel):
    name: str
    address: Optional[str] = None

class BranchCreate(BranchBase):
    pass

class BranchUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None

class BranchResponse(BranchBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

