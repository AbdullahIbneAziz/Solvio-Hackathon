from fastapi import APIRouter
from app.api.staff import sales, inventory, customers, dashboard, ai, reports

router = APIRouter()

# Include sub-routers
router.include_router(sales.router, prefix="/sales", tags=["Staff - Sales"])
router.include_router(inventory.router, prefix="/inventory", tags=["Staff - Inventory"])
router.include_router(customers.router, prefix="/customers", tags=["Staff - Customers"])
router.include_router(dashboard.router, prefix="/dashboard", tags=["Staff - Dashboard"])
router.include_router(ai.router, prefix="/ai", tags=["Staff - AI Insights"])
router.include_router(reports.router, prefix="/reports", tags=["Staff - Reports"])

