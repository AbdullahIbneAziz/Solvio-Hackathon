import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.sale import Sale
from app.models.product import Product
import os
import pickle
from app.config import settings

class ForecastingService:
    """Service for sales forecasting using LSTM and ARIMA models"""
    
    def __init__(self):
        self.model_dir = settings.MODEL_STORAGE_PATH
        os.makedirs(self.model_dir, exist_ok=True)
    
    def prepare_sales_data(self, db: Session, product_id: Optional[int] = None, 
                          branch_id: Optional[int] = None, days: int = 30) -> pd.DataFrame:
        """Prepare historical sales data for forecasting"""
        query = db.query(Sale).filter(
            Sale.sale_date >= date.today() - timedelta(days=days)
        )
        
        if product_id:
            query = query.filter(Sale.product_id == product_id)
        if branch_id:
            query = query.filter(Sale.branch_id == branch_id)
        
        sales = query.order_by(Sale.sale_date).all()
        
        if not sales:
            return pd.DataFrame()
        
        data = []
        for sale in sales:
            data.append({
                'date': sale.sale_date,
                'quantity': sale.quantity,
                'revenue': sale.total_price
            })
        
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
        df = df.resample('D').sum().fillna(0)
        
        return df
    
    def simple_forecast(self, db: Session, product_id: Optional[int] = None,
                      branch_id: Optional[int] = None, forecast_days: int = 7) -> List[Dict]:
        """Simple moving average forecast (fallback when ML models aren't available)"""
        df = self.prepare_sales_data(db, product_id, branch_id, days=30)
        
        if df.empty:
            return []
        
        # Calculate moving average
        window = min(7, len(df))
        if window == 0:
            return []
        
        avg_quantity = df['quantity'].tail(window).mean()
        avg_revenue = df['revenue'].tail(window).mean()
        
        # Generate forecast
        forecast = []
        start_date = date.today() + timedelta(days=1)
        
        for i in range(forecast_days):
            forecast.append({
                'date': str(start_date + timedelta(days=i)),
                'predicted_quantity': float(avg_quantity),
                'predicted_revenue': float(avg_revenue)
            })
        
        return forecast
    
    def arima_forecast(self, db: Session, product_id: Optional[int] = None,
                      branch_id: Optional[int] = None, forecast_days: int = 7) -> List[Dict]:
        """ARIMA-based forecasting"""
        try:
            from statsmodels.tsa.arima.model import ARIMA
        except ImportError:
            return self.simple_forecast(db, product_id, branch_id, forecast_days)
        
        df = self.prepare_sales_data(db, product_id, branch_id, days=30)
        
        if df.empty or len(df) < 7:
            return self.simple_forecast(db, product_id, branch_id, forecast_days)
        
        # Use quantity for forecasting
        series = df['quantity'].values
        
        try:
            # Fit ARIMA model
            model = ARIMA(series, order=(1, 1, 1))
            fitted_model = model.fit()
            
            # Forecast
            forecast = fitted_model.forecast(steps=forecast_days)
            
            # Generate forecast with dates
            result = []
            start_date = date.today() + timedelta(days=1)
            
            # Calculate average revenue per unit for revenue prediction
            avg_price_per_unit = (df['revenue'] / df['quantity']).replace([np.inf, -np.inf], 0).mean()
            if pd.isna(avg_price_per_unit) or avg_price_per_unit == 0:
                avg_price_per_unit = 1.0
            
            for i, pred_qty in enumerate(forecast):
                result.append({
                    'date': str(start_date + timedelta(days=i)),
                    'predicted_quantity': float(max(0, pred_qty)),
                    'predicted_revenue': float(max(0, pred_qty) * avg_price_per_unit)
                })
            
            return result
        except Exception as e:
            print(f"ARIMA forecast error: {e}")
            return self.simple_forecast(db, product_id, branch_id, forecast_days)
    
    def forecast_sales(self, db: Session, product_id: Optional[int] = None,
                      branch_id: Optional[int] = None, forecast_days: int = 7,
                      model_type: str = "arima") -> List[Dict]:
        """Main forecasting method"""
        if model_type == "arima":
            return self.arima_forecast(db, product_id, branch_id, forecast_days)
        else:
            return self.simple_forecast(db, product_id, branch_id, forecast_days)

