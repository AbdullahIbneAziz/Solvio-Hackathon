from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.customer import Customer
from app.models.user import User
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse
from app.utils.security import get_current_staff

router = APIRouter()

@router.get("/", response_model=List[CustomerResponse])
async def get_customers(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_staff),
    db: Session = Depends(get_db)
):
    """Get all customers for the staff member's branch"""
    query = db.query(Customer).filter(Customer.branch_id == current_user.branch_id)
    
    if search:
        query = query.filter(
            (Customer.name.ilike(f"%{search}%")) |
            (Customer.email.ilike(f"%{search}%")) |
            (Customer.phone.ilike(f"%{search}%"))
        )
    
    customers = query.offset(skip).limit(limit).all()
    return customers

@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: int,
    current_user: User = Depends(get_current_staff),
    db: Session = Depends(get_db)
):
    """Get a specific customer by ID (only if it belongs to staff's branch)"""
    customer = db.query(Customer).filter(
        Customer.id == customer_id,
        Customer.branch_id == current_user.branch_id
    ).first()
    
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    return customer

@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(
    customer_data: CustomerCreate,
    current_user: User = Depends(get_current_staff),
    db: Session = Depends(get_db)
):
    """Create a new customer (automatically set to staff's branch)"""
    db_customer = Customer(
        name=customer_data.name,
        email=customer_data.email,
        phone=customer_data.phone,
        branch_id=current_user.branch_id
    )
    
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: int,
    customer_update: CustomerUpdate,
    current_user: User = Depends(get_current_staff),
    db: Session = Depends(get_db)
):
    """Update a customer (only if it belongs to staff's branch)"""
    db_customer = db.query(Customer).filter(
        Customer.id == customer_id,
        Customer.branch_id == current_user.branch_id
    ).first()
    
    if not db_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    update_data = customer_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_customer, field, value)
    
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(
    customer_id: int,
    current_user: User = Depends(get_current_staff),
    db: Session = Depends(get_db)
):
    """Delete a customer (only if it belongs to staff's branch)"""
    db_customer = db.query(Customer).filter(
        Customer.id == customer_id,
        Customer.branch_id == current_user.branch_id
    ).first()
    
    if not db_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    db.delete(db_customer)
    db.commit()
    return None

