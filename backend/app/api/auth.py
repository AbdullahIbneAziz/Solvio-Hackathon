from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse
from app.utils.auth import verify_password, get_password_hash, create_access_token, create_refresh_token

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return JWT tokens"""
    user = db.query(User).filter(User.email == login_data.email).first()
    
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        user={
            "id": user.id,
            "email": user.email,
            "role": user.role.value,
            "branch_id": user.branch_id
        }
    )

@router.post("/register")
async def register_admin(login_data: LoginRequest, db: Session = Depends(get_db)):
    """Register a new admin user (for initial setup)"""
    # Check if admin already exists
    existing_user = db.query(User).filter(User.email == login_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Create admin user
    from app.models.user import UserRole
    user = User(
        email=login_data.email,
        password_hash=get_password_hash(login_data.password),
        role=UserRole.ADMIN
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {"message": "Admin user created successfully", "user_id": user.id}

