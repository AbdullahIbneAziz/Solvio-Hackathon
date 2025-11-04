from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import date
import csv
import io
from app.database import get_db
from app.models.user import User
from app.models.sale import Sale
from app.models.inventory import Inventory
from app.models.customer import Customer
from app.models.product import Product
from app.utils.security import get_current_staff

router = APIRouter()

@router.get("/sales")
async def get_branch_sales_report(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    format: str = Query("json", regex="^(json|csv)$"),
    current_user: User = Depends(get_current_staff),
    db: Session = Depends(get_db)
):
    """Generate branch-specific sales report"""
    query = db.query(Sale).filter(Sale.branch_id == current_user.branch_id)
    
    if start_date:
        query = query.filter(Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(Sale.sale_date <= end_date)
    
    sales = query.order_by(Sale.sale_date.desc()).all()
    
    if format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Date', 'Product', 'Quantity', 'Total Price', 'Customer'])
        
        for sale in sales:
            writer.writerow([
                sale.sale_date,
                sale.product.name if sale.product else 'N/A',
                sale.quantity,
                sale.total_price,
                sale.customer.name if sale.customer else 'N/A'
            ])
        
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=branch_sales_report.csv"}
        )
    
    return {
        "branch_id": current_user.branch_id,
        "total_sales": len(sales),
        "total_revenue": sum(s.total_price for s in sales),
        "sales": [
            {
                "id": s.id,
                "date": str(s.sale_date),
                "product": s.product.name if s.product else None,
                "quantity": float(s.quantity),
                "total_price": float(s.total_price),
                "customer": s.customer.name if s.customer else None
            }
            for s in sales
        ]
    }

@router.get("/inventory")
async def get_branch_inventory_report(
    low_stock_only: bool = Query(False),
    format: str = Query("json", regex="^(json|csv)$"),
    current_user: User = Depends(get_current_staff),
    db: Session = Depends(get_db)
):
    """Generate branch-specific inventory report"""
    query = db.query(Inventory).filter(Inventory.branch_id == current_user.branch_id).join(Product)
    
    if low_stock_only:
        query = query.filter(Inventory.quantity <= Inventory.min_threshold)
    
    inventory_items = query.all()
    
    if format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Product', 'Quantity', 'Min Threshold', 'Status'])
        
        for item in inventory_items:
            status = 'Low Stock' if item.quantity <= item.min_threshold else 'OK'
            writer.writerow([
                item.product.name if item.product else 'N/A',
                item.quantity,
                item.min_threshold,
                status
            ])
        
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=branch_inventory_report.csv"}
        )
    
    return {
        "branch_id": current_user.branch_id,
        "total_items": len(inventory_items),
        "low_stock_count": sum(1 for item in inventory_items if item.quantity <= item.min_threshold),
        "inventory": [
            {
                "id": item.id,
                "product": item.product.name if item.product else None,
                "quantity": float(item.quantity),
                "min_threshold": float(item.min_threshold),
                "status": "Low Stock" if item.quantity <= item.min_threshold else "OK"
            }
            for item in inventory_items
        ]
    }

@router.get("/customers")
async def get_branch_customers_report(
    format: str = Query("json", regex="^(json|csv)$"),
    current_user: User = Depends(get_current_staff),
    db: Session = Depends(get_db)
):
    """Generate branch-specific customer report"""
    customers = db.query(Customer).filter(Customer.branch_id == current_user.branch_id).all()
    
    # Get purchase statistics for each customer
    customer_data = []
    for customer in customers:
        total_purchases = db.query(func.sum(Sale.total_price)).filter(
            Sale.customer_id == customer.id,
            Sale.branch_id == current_user.branch_id
        ).scalar() or 0.0
        
        purchase_count = db.query(func.count(Sale.id)).filter(
            Sale.customer_id == customer.id,
            Sale.branch_id == current_user.branch_id
        ).scalar() or 0
        
        customer_data.append({
            "customer": customer,
            "total_purchases": float(total_purchases),
            "purchase_count": purchase_count
        })
    
    if format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Name', 'Email', 'Phone', 'Total Purchases', 'Purchase Count'])
        
        for data in customer_data:
            writer.writerow([
                data["customer"].name,
                data["customer"].email or 'N/A',
                data["customer"].phone or 'N/A',
                data["total_purchases"],
                data["purchase_count"]
            ])
        
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=branch_customers_report.csv"}
        )
    
    return {
        "branch_id": current_user.branch_id,
        "total_customers": len(customers),
        "customers": [
            {
                "id": data["customer"].id,
                "name": data["customer"].name,
                "email": data["customer"].email,
                "phone": data["customer"].phone,
                "total_purchases": data["total_purchases"],
                "purchase_count": data["purchase_count"]
            }
            for data in customer_data
        ]
    }

