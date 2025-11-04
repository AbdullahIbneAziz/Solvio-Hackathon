from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
from app.database import get_db
from app.models.sale import Sale
from app.models.product import Product
from app.models.user import User
from app.schemas.sale import SaleCreate, SaleUpdate, SaleResponse
from app.utils.security import get_current_staff

router = APIRouter()

@router.get("/", response_model=List[SaleResponse])
async def get_sales(
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: User = Depends(get_current_staff),
    db: Session = Depends(get_db)
):
    """Get all sales for the staff member's branch"""
    query = db.query(Sale).filter(Sale.branch_id == current_user.branch_id)
    
    if start_date:
        query = query.filter(Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(Sale.sale_date <= end_date)
    
    sales = query.order_by(Sale.sale_date.desc()).offset(skip).limit(limit).all()
    return sales

@router.get("/{sale_id}", response_model=SaleResponse)
async def get_sale(
    sale_id: int,
    current_user: User = Depends(get_current_staff),
    db: Session = Depends(get_db)
):
    """Get a specific sale by ID (only if it belongs to staff's branch)"""
    sale = db.query(Sale).filter(
        Sale.id == sale_id,
        Sale.branch_id == current_user.branch_id
    ).first()
    
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )
    return sale

@router.post("/", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
async def create_sale(
    sale_data: SaleCreate,
    current_user: User = Depends(get_current_staff),
    db: Session = Depends(get_db)
):
    """Create a new sale (automatically set to staff's branch)"""
    # Verify product exists
    product = db.query(Product).filter(Product.id == sale_data.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Calculate total price
    total_price = sale_data.quantity * product.unit_price
    
    # Verify inventory has enough stock
    from app.models.inventory import Inventory
    inventory = db.query(Inventory).filter(
        Inventory.branch_id == current_user.branch_id,
        Inventory.product_id == sale_data.product_id
    ).first()
    
    if not inventory or inventory.quantity < sale_data.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient inventory"
        )
    
    # Update inventory
    inventory.quantity -= sale_data.quantity
    
    # Create sale
    db_sale = Sale(
        branch_id=current_user.branch_id,
        product_id=sale_data.product_id,
        customer_id=sale_data.customer_id,
        quantity=sale_data.quantity,
        total_price=total_price,
        sale_date=date.today(),
        staff_id=current_user.id
    )
    
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

@router.put("/{sale_id}", response_model=SaleResponse)
async def update_sale(
    sale_id: int,
    sale_update: SaleUpdate,
    current_user: User = Depends(get_current_staff),
    db: Session = Depends(get_db)
):
    """Update a sale (only if it belongs to staff's branch)"""
    db_sale = db.query(Sale).filter(
        Sale.id == sale_id,
        Sale.branch_id == current_user.branch_id
    ).first()
    
    if not db_sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )
    
    # Handle product change and recalculate price
    if sale_update.product_id and sale_update.product_id != db_sale.product_id:
        product = db.query(Product).filter(Product.id == sale_update.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        db_sale.product_id = sale_update.product_id
    
    # Handle quantity change
    if sale_update.quantity:
        quantity_diff = sale_update.quantity - db_sale.quantity
        product = db.query(Product).filter(Product.id == db_sale.product_id).first()
        
        # Check inventory
        from app.models.inventory import Inventory
        inventory = db.query(Inventory).filter(
            Inventory.branch_id == current_user.branch_id,
            Inventory.product_id == db_sale.product_id
        ).first()
        
        if inventory and inventory.quantity < quantity_diff:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient inventory"
            )
        
        if inventory:
            inventory.quantity -= quantity_diff
        
        db_sale.quantity = sale_update.quantity
        db_sale.total_price = sale_update.quantity * product.unit_price
    
    if sale_update.customer_id is not None:
        db_sale.customer_id = sale_update.customer_id
    
    db.commit()
    db.refresh(db_sale)
    return db_sale

@router.delete("/{sale_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sale(
    sale_id: int,
    current_user: User = Depends(get_current_staff),
    db: Session = Depends(get_db)
):
    """Delete a sale (only if it belongs to staff's branch)"""
    db_sale = db.query(Sale).filter(
        Sale.id == sale_id,
        Sale.branch_id == current_user.branch_id
    ).first()
    
    if not db_sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )
    
    # Restore inventory
    from app.models.inventory import Inventory
    inventory = db.query(Inventory).filter(
        Inventory.branch_id == current_user.branch_id,
        Inventory.product_id == db_sale.product_id
    ).first()
    
    if inventory:
        inventory.quantity += db_sale.quantity
    
    db.delete(db_sale)
    db.commit()
    return None

