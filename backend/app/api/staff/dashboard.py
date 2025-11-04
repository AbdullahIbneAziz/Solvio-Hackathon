from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.database import get_db
from app.models.user import User
from app.models.sale import Sale
from app.models.inventory import Inventory
from app.models.customer import Customer
from app.models.product import Product
from app.utils.security import get_current_staff

router = APIRouter()

@router.get("/")
async def get_branch_dashboard(
    current_user: User = Depends(get_current_staff),
    db: Session = Depends(get_db)
):
    """Get branch-specific dashboard data for staff"""
    branch_id = current_user.branch_id
    
    # Date ranges
    today = datetime.now().date()
    last_7_days = today - timedelta(days=7)
    last_30_days = today - timedelta(days=30)
    
    # Total sales (last 30 days) for this branch
    total_sales = db.query(func.sum(Sale.total_price)).filter(
        Sale.branch_id == branch_id,
        Sale.sale_date >= last_30_days
    ).scalar() or 0.0
    
    # Sales count (last 30 days)
    sales_count = db.query(func.count(Sale.id)).filter(
        Sale.branch_id == branch_id,
        Sale.sale_date >= last_30_days
    ).scalar() or 0
    
    # Recent sales (last 7 days)
    recent_sales = db.query(func.sum(Sale.total_price)).filter(
        Sale.branch_id == branch_id,
        Sale.sale_date >= last_7_days
    ).scalar() or 0.0
    
    # Total inventory items
    total_products = db.query(func.count(Inventory.id)).filter(
        Inventory.branch_id == branch_id
    ).scalar() or 0
    
    # Low stock items (inventory below threshold)
    low_stock_items = db.query(Inventory).filter(
        Inventory.branch_id == branch_id,
        Inventory.quantity <= Inventory.min_threshold
    ).count()
    
    # Total customers for this branch
    total_customers = db.query(func.count(Customer.id)).filter(
        Customer.branch_id == branch_id
    ).scalar() or 0
    
    # New customers (last 30 days)
    new_customers = db.query(func.count(Customer.id)).filter(
        Customer.branch_id == branch_id,
        func.date(Customer.created_at) >= last_30_days
    ).scalar() or 0
    
    # Top selling products (last 30 days) for this branch
    top_products = db.query(
        Product.name,
        func.sum(Sale.quantity).label('total_quantity'),
        func.sum(Sale.total_price).label('total_revenue')
    ).join(Sale, Sale.product_id == Product.id).filter(
        Sale.branch_id == branch_id,
        Sale.sale_date >= last_30_days
    ).group_by(Product.id, Product.name).order_by(
        func.sum(Sale.total_price).desc()
    ).limit(10).all()
    
    # Sales trend (last 7 days)
    sales_trend = db.query(
        func.date(Sale.sale_date).label('date'),
        func.sum(Sale.total_price).label('revenue'),
        func.count(Sale.id).label('count')
    ).filter(
        Sale.branch_id == branch_id,
        Sale.sale_date >= last_7_days
    ).group_by(func.date(Sale.sale_date)).order_by(
        func.date(Sale.sale_date)
    ).all()
    
    return {
        "branch_id": branch_id,
        "summary": {
            "total_sales": float(total_sales),
            "sales_count": sales_count,
            "recent_sales": float(recent_sales),
            "total_products": total_products,
            "low_stock_items": low_stock_items,
            "total_customers": total_customers,
            "new_customers": new_customers
        },
        "top_products": [
            {
                "name": product.name,
                "total_quantity": float(product.total_quantity),
                "total_revenue": float(product.total_revenue)
            }
            for product in top_products
        ],
        "sales_trend": [
            {
                "date": str(trend.date),
                "revenue": float(trend.revenue),
                "count": trend.count
            }
            for trend in sales_trend
        ]
    }

