from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.user import User
from app.utils.security import get_current_admin
from app.ai.forecasting import ForecastingService
from app.ai.demand_prediction import DemandPredictionService
from app.ai.shortage_detection import ShortageDetectionService

router = APIRouter()

@router.get("/forecast")
async def get_sales_forecast(
    product_id: Optional[int] = Query(None),
    branch_id: Optional[int] = Query(None),
    forecast_days: int = Query(7, ge=1, le=30),
    model_type: str = Query("arima", regex="^(arima|simple)$"),
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get sales forecast using AI models"""
    forecasting_service = ForecastingService()
    forecast = forecasting_service.forecast_sales(
        db, product_id, branch_id, forecast_days, model_type
    )
    return {"forecast": forecast, "model_type": model_type}

@router.get("/demand/top-products")
async def get_top_products_demand(
    branch_id: Optional[int] = Query(None),
    days: int = Query(30, ge=1, le=365),
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get top products by demand"""
    demand_service = DemandPredictionService()
    top_products = demand_service.get_top_products_by_demand(db, branch_id, days, limit)
    return {"top_products": top_products}

@router.get("/demand/trends/{product_id}")
async def get_product_demand_trends(
    product_id: int,
    branch_id: Optional[int] = Query(None),
    days: int = Query(30, ge=7, le=365),
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get demand trends for a specific product"""
    demand_service = DemandPredictionService()
    trends = demand_service.get_demand_trends(db, product_id, branch_id, days)
    return trends

@router.get("/shortages")
async def get_shortage_warnings(
    branch_id: Optional[int] = Query(None),
    forecast_days: int = Query(7, ge=1, le=30),
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get inventory shortage warnings and predictions"""
    shortage_service = ShortageDetectionService()
    warnings = shortage_service.get_shortage_warnings(db, branch_id)
    
    # Add predicted shortages
    predicted = shortage_service.predict_shortages(db, branch_id, forecast_days)
    warnings['predicted_shortages'] = predicted
    
    return warnings

@router.get("/insights")
async def get_ai_insights(
    branch_id: Optional[int] = Query(None),
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get comprehensive AI insights"""
    forecasting_service = ForecastingService()
    demand_service = DemandPredictionService()
    shortage_service = ShortageDetectionService()
    
    # Get top products
    top_products = demand_service.get_top_products_by_demand(db, branch_id, days=30, limit=5)
    
    # Get shortage warnings
    shortages = shortage_service.get_shortage_warnings(db, branch_id)
    
    # Get overall forecast
    overall_forecast = forecasting_service.forecast_sales(db, branch_id=branch_id, forecast_days=7)
    
    return {
        "top_products_demand": top_products,
        "shortage_warnings": shortages,
        "sales_forecast": overall_forecast
    }

