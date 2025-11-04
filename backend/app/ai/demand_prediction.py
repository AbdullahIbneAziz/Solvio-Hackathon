import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.sale import Sale
from app.models.product import Product

class DemandPredictionService:
    """Service for predicting product demand and identifying trends"""
    
    def get_top_products_by_demand(self, db: Session, branch_id: Optional[int] = None,
                                   days: int = 30, limit: int = 10) -> List[Dict]:
        """Get top products by demand (sales quantity)"""
        query = db.query(
            Product.id,
            Product.name,
            func.sum(Sale.quantity).label('total_quantity'),
            func.sum(Sale.total_price).label('total_revenue'),
            func.count(Sale.id).label('sale_count')
        ).join(Sale, Sale.product_id == Product.id).filter(
            Sale.sale_date >= date.today() - timedelta(days=days)
        )
        
        if branch_id:
            query = query.filter(Sale.branch_id == branch_id)
        
        results = query.group_by(Product.id, Product.name).order_by(
            func.sum(Sale.quantity).desc()
        ).limit(limit).all()
        
        return [
            {
                'product_id': r.id,
                'product_name': r.name,
                'total_quantity': float(r.total_quantity),
                'total_revenue': float(r.total_revenue),
                'sale_count': r.sale_count,
                'avg_daily_demand': float(r.total_quantity) / days
            }
            for r in results
        ]
    
    def get_demand_trends(self, db: Session, product_id: int,
                         branch_id: Optional[int] = None, days: int = 30) -> Dict:
        """Analyze demand trends for a specific product"""
        query = db.query(
            func.date(Sale.sale_date).label('date'),
            func.sum(Sale.quantity).label('quantity')
        ).filter(
            Sale.product_id == product_id,
            Sale.sale_date >= date.today() - timedelta(days=days)
        )
        
        if branch_id:
            query = query.filter(Sale.branch_id == branch_id)
        
        results = query.group_by(func.date(Sale.sale_date)).order_by(
            func.date(Sale.sale_date)
        ).all()
        
        if not results:
            return {
                'product_id': product_id,
                'trend': 'stable',
                'growth_rate': 0.0,
                'data_points': []
            }
        
        quantities = [r.quantity for r in results]
        
        # Calculate trend
        if len(quantities) >= 2:
            first_half = sum(quantities[:len(quantities)//2])
            second_half = sum(quantities[len(quantities)//2:])
            growth_rate = ((second_half - first_half) / first_half * 100) if first_half > 0 else 0.0
            
            if growth_rate > 5:
                trend = 'increasing'
            elif growth_rate < -5:
                trend = 'decreasing'
            else:
                trend = 'stable'
        else:
            trend = 'stable'
            growth_rate = 0.0
        
        return {
            'product_id': product_id,
            'trend': trend,
            'growth_rate': round(growth_rate, 2),
            'avg_daily_demand': sum(quantities) / len(quantities),
            'data_points': [
                {
                    'date': str(r.date),
                    'quantity': float(r.quantity)
                }
                for r in results
            ]
        }
    
    def predict_demand(self, db: Session, product_id: int,
                      branch_id: Optional[int] = None, days: int = 7) -> Dict:
        """Predict demand for a product over the next N days"""
        # Get historical data
        query = db.query(
            func.sum(Sale.quantity).label('total_quantity')
        ).filter(
            Sale.product_id == product_id,
            Sale.sale_date >= date.today() - timedelta(days=30)
        )
        
        if branch_id:
            query = query.filter(Sale.branch_id == branch_id)
        
        result = query.scalar() or 0
        
        # Simple prediction: average daily demand * forecast days
        avg_daily_demand = result / 30
        predicted_demand = avg_daily_demand * days
        
        return {
            'product_id': product_id,
            'forecast_days': days,
            'predicted_demand': round(predicted_demand, 2),
            'avg_daily_demand': round(avg_daily_demand, 2),
            'confidence': 'medium'  # Can be enhanced with statistical analysis
        }

