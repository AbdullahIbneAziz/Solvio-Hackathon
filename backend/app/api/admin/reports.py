from fastapi import APIRouter, Depends, Query, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from datetime import date, timedelta
import csv
import io
from app.database import get_db
from app.models.user import User
from app.models.sale import Sale
from app.models.inventory import Inventory
from app.models.customer import Customer
from app.models.product import Product
from app.models.branch import Branch
from app.utils.security import get_current_admin

router = APIRouter()

@router.get("/sales")
async def get_sales_report(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    branch_id: Optional[int] = Query(None),
    format: str = Query("json", regex="^(json|csv)$"),
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Generate sales report"""
    query = db.query(Sale)
    
    if start_date:
        query = query.filter(Sale.sale_date >= start_date)
    if end_date:
        query = query.filter(Sale.sale_date <= end_date)
    if branch_id:
        query = query.filter(Sale.branch_id == branch_id)
    
    sales = query.order_by(Sale.sale_date.desc()).all()
    
    if format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Date', 'Branch', 'Product', 'Quantity', 'Total Price', 'Customer'])
        
        for sale in sales:
            writer.writerow([
                sale.sale_date,
                sale.branch.name if sale.branch else 'N/A',
                sale.product.name if sale.product else 'N/A',
                sale.quantity,
                sale.total_price,
                sale.customer.name if sale.customer else 'N/A'
            ])
        
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=sales_report.csv"}
        )
    
    return {
        "total_sales": len(sales),
        "total_revenue": sum(s.total_price for s in sales),
        "sales": [
            {
                "id": s.id,
                "date": str(s.sale_date),
                "branch": s.branch.name if s.branch else None,
                "product": s.product.name if s.product else None,
                "quantity": float(s.quantity),
                "total_price": float(s.total_price),
                "customer": s.customer.name if s.customer else None
            }
            for s in sales
        ]
    }

@router.get("/inventory")
async def get_inventory_report(
    branch_id: Optional[int] = Query(None),
    low_stock_only: bool = Query(False),
    format: str = Query("json", regex="^(json|csv)$"),
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Generate inventory report"""
    query = db.query(Inventory).join(Product).join(Branch)
    
    if branch_id:
        query = query.filter(Inventory.branch_id == branch_id)
    if low_stock_only:
        query = query.filter(Inventory.quantity <= Inventory.min_threshold)
    
    inventory_items = query.all()
    
    if format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Branch', 'Product', 'Quantity', 'Min Threshold', 'Status'])
        
        for item in inventory_items:
            status = 'Low Stock' if item.quantity <= item.min_threshold else 'OK'
            writer.writerow([
                item.branch.name if item.branch else 'N/A',
                item.product.name if item.product else 'N/A',
                item.quantity,
                item.min_threshold,
                status
            ])
        
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=inventory_report.csv"}
        )
    
    return {
        "total_items": len(inventory_items),
        "low_stock_count": sum(1 for item in inventory_items if item.quantity <= item.min_threshold),
        "inventory": [
            {
                "id": item.id,
                "branch": item.branch.name if item.branch else None,
                "product": item.product.name if item.product else None,
                "quantity": float(item.quantity),
                "min_threshold": float(item.min_threshold),
                "status": "Low Stock" if item.quantity <= item.min_threshold else "OK"
            }
            for item in inventory_items
        ]
    }

@router.get("/customers")
async def get_customers_report(
    branch_id: Optional[int] = Query(None),
    format: str = Query("json", regex="^(json|csv)$"),
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Generate customer activity report"""
    query = db.query(Customer).join(Branch)
    
    if branch_id:
        query = query.filter(Customer.branch_id == branch_id)
    
    customers = query.all()
    
    # Get purchase statistics for each customer
    customer_data = []
    for customer in customers:
        total_purchases = db.query(func.sum(Sale.total_price)).filter(
            Sale.customer_id == customer.id
        ).scalar() or 0.0
        
        purchase_count = db.query(func.count(Sale.id)).filter(
            Sale.customer_id == customer.id
        ).scalar() or 0
        
        customer_data.append({
            "customer": customer,
            "total_purchases": float(total_purchases),
            "purchase_count": purchase_count
        })
    
    if format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Name', 'Email', 'Phone', 'Branch', 'Total Purchases', 'Purchase Count'])
        
        for data in customer_data:
            writer.writerow([
                data["customer"].name,
                data["customer"].email or 'N/A',
                data["customer"].phone or 'N/A',
                data["customer"].branch.name if data["customer"].branch else 'N/A',
                data["total_purchases"],
                data["purchase_count"]
            ])
        
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=customers_report.csv"}
        )
    
    return {
        "total_customers": len(customers),
        "customers": [
            {
                "id": data["customer"].id,
                "name": data["customer"].name,
                "email": data["customer"].email,
                "phone": data["customer"].phone,
                "branch": data["customer"].branch.name if data["customer"].branch else None,
                "total_purchases": data["total_purchases"],
                "purchase_count": data["purchase_count"]
            }
            for data in customer_data
        ]
    }

@router.get("/staff")
async def get_staff_report(
    branch_id: Optional[int] = Query(None),
    format: str = Query("json", regex="^(json|csv)$"),
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Generate staff activity report"""
    from app.models.user import User, UserRole
    
    query = db.query(User).filter(User.role == UserRole.STAFF)
    
    if branch_id:
        query = query.filter(User.branch_id == branch_id)
    
    staff_members = query.all()
    
    # Get sales statistics for each staff member
    staff_data = []
    for staff in staff_members:
        total_sales = db.query(func.sum(Sale.total_price)).filter(
            Sale.staff_id == staff.id
        ).scalar() or 0.0
        
        sale_count = db.query(func.count(Sale.id)).filter(
            Sale.staff_id == staff.id
        ).scalar() or 0
        
        staff_data.append({
            "staff": staff,
            "total_sales": float(total_sales),
            "sale_count": sale_count
        })
    
    if format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Email', 'Branch', 'Total Sales', 'Sale Count'])
        
        for data in staff_data:
            writer.writerow([
                data["staff"].email,
                data["staff"].branch.name if data["staff"].branch else 'N/A',
                data["total_sales"],
                data["sale_count"]
            ])
        
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=staff_report.csv"}
        )
    
    return {
        "total_staff": len(staff_members),
        "staff": [
            {
                "id": data["staff"].id,
                "email": data["staff"].email,
                "branch": data["staff"].branch.name if data["staff"].branch else None,
                "total_sales": data["total_sales"],
                "sale_count": data["sale_count"]
            }
            for data in staff_data
        ]
    }

@router.get("/ai-forecasting")
async def get_ai_forecasting_report(
    branch_id: Optional[int] = Query(None),
    forecast_days: int = Query(7, ge=1, le=30),
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Generate AI forecasting report"""
    from app.ai.forecasting import ForecastingService
    from app.ai.demand_prediction import DemandPredictionService
    from app.ai.shortage_detection import ShortageDetectionService
    
    forecasting_service = ForecastingService()
    demand_service = DemandPredictionService()
    shortage_service = ShortageDetectionService()
    
    # Get forecasts
    forecast = forecasting_service.forecast_sales(db, branch_id=branch_id, forecast_days=forecast_days)
    top_products = demand_service.get_top_products_by_demand(db, branch_id, days=30, limit=10)
    shortages = shortage_service.get_shortage_warnings(db, branch_id)
    
    return {
        "forecast_period": forecast_days,
        "sales_forecast": forecast,
        "top_products_demand": top_products,
        "shortage_warnings": shortages
    }

