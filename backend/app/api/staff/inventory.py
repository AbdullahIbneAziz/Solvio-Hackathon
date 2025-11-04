from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.user import User
from app.schemas.inventory import InventoryCreate, InventoryUpdate, InventoryResponse
from app.utils.security import get_current_staff

router = APIRouter()

@router.get("/", response_model=List[InventoryResponse])
async def get_inventory(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_staff),
    db: Session = Depends(get_db)
):
    """Get all inventory items for the staff member's branch"""
    inventory_items = db.query(Inventory).filter(
        Inventory.branch_id == current_user.branch_id
    ).offset(skip).limit(limit).all()
    return inventory_items

@router.get("/{inventory_id}", response_model=InventoryResponse)
async def get_inventory_item(
    inventory_id: int,
    current_user: User = Depends(get_current_staff),
    db: Session = Depends(get_db)
):
    """Get a specific inventory item by ID (only if it belongs to staff's branch)"""
    inventory_item = db.query(Inventory).filter(
        Inventory.id == inventory_id,
        Inventory.branch_id == current_user.branch_id
    ).first()
    
    if not inventory_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory item not found"
        )
    return inventory_item

@router.post("/", response_model=InventoryResponse, status_code=status.HTTP_201_CREATED)
async def create_inventory_item(
    inventory_data: InventoryCreate,
    current_user: User = Depends(get_current_staff),
    db: Session = Depends(get_db)
):
    """Create a new inventory item (automatically set to staff's branch)"""
    # Verify product exists
    product = db.query(Product).filter(Product.id == inventory_data.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Check if inventory item already exists for this branch and product
    existing = db.query(Inventory).filter(
        Inventory.branch_id == current_user.branch_id,
        Inventory.product_id == inventory_data.product_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inventory item already exists for this product. Use update instead."
        )
    
    # Create inventory item
    db_inventory = Inventory(
        branch_id=current_user.branch_id,
        product_id=inventory_data.product_id,
        quantity=inventory_data.quantity,
        min_threshold=inventory_data.min_threshold
    )
    
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

@router.put("/{inventory_id}", response_model=InventoryResponse)
async def update_inventory_item(
    inventory_id: int,
    inventory_update: InventoryUpdate,
    current_user: User = Depends(get_current_staff),
    db: Session = Depends(get_db)
):
    """Update an inventory item (only if it belongs to staff's branch)"""
    db_inventory = db.query(Inventory).filter(
        Inventory.id == inventory_id,
        Inventory.branch_id == current_user.branch_id
    ).first()
    
    if not db_inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory item not found"
        )
    
    update_data = inventory_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_inventory, field, value)
    
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

@router.delete("/{inventory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inventory_item(
    inventory_id: int,
    current_user: User = Depends(get_current_staff),
    db: Session = Depends(get_db)
):
    """Delete an inventory item (only if it belongs to staff's branch)"""
    db_inventory = db.query(Inventory).filter(
        Inventory.id == inventory_id,
        Inventory.branch_id == current_user.branch_id
    ).first()
    
    if not db_inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Inventory item not found"
        )
    
    db.delete(db_inventory)
    db.commit()
    return None

