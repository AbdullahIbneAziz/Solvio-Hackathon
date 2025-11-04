from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.user import User
from app.utils.security import get_current_staff
from app.ai.forecasting import ForecastingService
from app.ai.demand_prediction import DemandPredictionService
from app.ai.shortage_detection import ShortageDetectionService

router = APIRouter()

@router.get("/forecast")
async def get_branch_forecast(
    product_id: Optional[int] = Query(None),
    forecast_days: int = Query(7, ge=1, le=30),
    model_type: str = Query("arima", regex="^(arima|simple)$"),
    current_user: User = Depends(get_current_staff),
    db: Session = Depends(get_db)
):
    """Get sales forecast for staff's branch"""
    forecasting_service = ForecastingService()
    forecast = forecasting_service.forecast_sales(
        db, product_id, current_user.branch_id, forecast_days, model_type
    )
    return {"forecast": forecast, "model_type": model_type}

@router.get("/demand/top-products")
async def get_branch_top_products(
    days: int = Query(30, ge=1, le=365),
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_staff),
    db: Session = Depends(get_db)
):
    """Get top products by demand for staff's branch"""
    demand_service = DemandPredictionService()
    top_products = demand_service.get_top_products_by_demand(
        db, current_user.branch_id, days, limit
    )
    return {"top_products": top_products}

@router.get("/shortages")
async def get_branch_shortages(
    forecast_days: int = Query(7, ge=1, le=30),
    current_user: User = Depends(get_current_staff),
    db: Session = Depends(get_db)
):
    """Get inventory shortage warnings for staff's branch"""
    shortage_service = ShortageDetectionService()
    warnings = shortage_service.get_shortage_warnings(db, current_user.branch_id)
    predicted = shortage_service.predict_shortages(db, current_user.branch_id, forecast_days)
    warnings['predicted_shortages'] = predicted
    return warnings

@router.get("/insights")
async def get_branch_ai_insights(
    current_user: User = Depends(get_current_staff),
    db: Session = Depends(get_db)
):
    """Get comprehensive AI insights for staff's branch"""
    forecasting_service = ForecastingService()
    demand_service = DemandPredictionService()
    shortage_service = ShortageDetectionService()
    
    # Get top products
    top_products = demand_service.get_top_products_by_demand(
        db, current_user.branch_id, days=30, limit=5
    )
    
    # Get shortage warnings
    shortages = shortage_service.get_shortage_warnings(db, current_user.branch_id)
    
    # Get branch forecast
    branch_forecast = forecasting_service.forecast_sales(
        db, branch_id=current_user.branch_id, forecast_days=7
    )
    
    return {
        "top_products_demand": top_products,
        "shortage_warnings": shortages,
        "sales_forecast": branch_forecast
    }

