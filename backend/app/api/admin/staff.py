from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User, UserRole
from app.models.branch import Branch
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.utils.security import get_current_admin
from app.utils.auth import get_password_hash

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
async def get_staff(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get all staff members"""
    staff = db.query(User).filter(User.role == UserRole.STAFF).offset(skip).limit(limit).all()
    return staff

@router.get("/{staff_id}", response_model=UserResponse)
async def get_staff_member(
    staff_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get a specific staff member by ID"""
    staff_member = db.query(User).filter(User.id == staff_id, User.role == UserRole.STAFF).first()
    if not staff_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff member not found"
        )
    return staff_member

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_staff(
    staff_data: UserCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create a new staff member"""
    # Verify branch exists if provided
    if staff_data.branch_id:
        branch = db.query(Branch).filter(Branch.id == staff_data.branch_id).first()
        if not branch:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Branch not found"
            )
    
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == staff_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Create staff user
    db_staff = User(
        email=staff_data.email,
        password_hash=get_password_hash(staff_data.password),
        role=UserRole.STAFF,
        branch_id=staff_data.branch_id
    )
    
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff

@router.put("/{staff_id}", response_model=UserResponse)
async def update_staff(
    staff_id: int,
    staff_update: UserUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update a staff member"""
    db_staff = db.query(User).filter(User.id == staff_id, User.role == UserRole.STAFF).first()
    if not db_staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff member not found"
        )
    
    # Verify branch exists if provided
    if staff_update.branch_id is not None:
        branch = db.query(Branch).filter(Branch.id == staff_update.branch_id).first()
        if not branch:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Branch not found"
            )
    
    update_data = staff_update.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["password_hash"] = get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(db_staff, field, value)
    
    db.commit()
    db.refresh(db_staff)
    return db_staff

@router.delete("/{staff_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_staff(
    staff_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete a staff member"""
    db_staff = db.query(User).filter(User.id == staff_id, User.role == UserRole.STAFF).first()
    if not db_staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Staff member not found"
        )
    
    db.delete(db_staff)
    db.commit()
    return None

