from typing import List, Dict, Optional
from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.sale import Sale
from app.ai.demand_prediction import DemandPredictionService

class ShortageDetectionService:
    """Service for detecting inventory shortages and low stock warnings"""
    
    def __init__(self):
        self.demand_service = DemandPredictionService()
    
    def check_low_stock(self, db: Session, branch_id: Optional[int] = None) -> List[Dict]:
        """Check for items with stock below threshold"""
        query = db.query(Inventory).join(Product).filter(
            Inventory.quantity <= Inventory.min_threshold
        )
        
        if branch_id:
            query = query.filter(Inventory.branch_id == branch_id)
        
        low_stock_items = query.all()
        
        result = []
        for item in low_stock_items:
            result.append({
                'inventory_id': item.id,
                'branch_id': item.branch_id,
                'product_id': item.product_id,
                'product_name': item.product.name,
                'current_quantity': float(item.quantity),
                'min_threshold': float(item.min_threshold),
                'shortage_amount': float(item.min_threshold - item.quantity),
                'severity': 'critical' if item.quantity == 0 else 'warning'
            })
        
        return result
    
    def predict_shortages(self, db: Session, branch_id: Optional[int] = None,
                         forecast_days: int = 7) -> List[Dict]:
        """Predict potential shortages based on current inventory and forecasted demand"""
        # Get all inventory items
        query = db.query(Inventory).join(Product)
        
        if branch_id:
            query = query.filter(Inventory.branch_id == branch_id)
        
        inventory_items = query.all()
        
        predictions = []
        
        for item in inventory_items:
            # Predict demand for next N days
            demand_pred = self.demand_service.predict_demand(
                db, item.product_id, item.branch_id, forecast_days
            )
            
            predicted_demand = demand_pred['predicted_demand']
            current_stock = item.quantity
            
            # Check if shortage is predicted
            if current_stock < predicted_demand:
                shortage_risk = 'high' if (current_stock < predicted_demand * 0.5) else 'medium'
                
                predictions.append({
                    'inventory_id': item.id,
                    'branch_id': item.branch_id,
                    'product_id': item.product_id,
                    'product_name': item.product.name,
                    'current_stock': float(current_stock),
                    'predicted_demand': round(predicted_demand, 2),
                    'shortage_amount': round(predicted_demand - current_stock, 2),
                    'shortage_risk': shortage_risk,
                    'forecast_days': forecast_days,
                    'recommended_stock': round(predicted_demand * 1.2, 2)  # 20% buffer
                })
        
        return predictions
    
    def get_shortage_warnings(self, db: Session, branch_id: Optional[int] = None) -> Dict:
        """Get comprehensive shortage warnings (current + predicted)"""
        current_low_stock = self.check_low_stock(db, branch_id)
        predicted_shortages = self.predict_shortages(db, branch_id)
        
        return {
            'current_low_stock': current_low_stock,
            'predicted_shortages': predicted_shortages,
            'total_warnings': len(current_low_stock) + len(predicted_shortages),
            'critical_count': len([item for item in current_low_stock if item['severity'] == 'critical'])
        }

