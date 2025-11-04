from fastapi import APIRouter
from app.api.admin import branches, staff, products, dashboard, ai, reports

router = APIRouter()

# Include sub-routers
router.include_router(branches.router, prefix="/branches", tags=["Admin - Branches"])
router.include_router(staff.router, prefix="/staff", tags=["Admin - Staff"])
router.include_router(products.router, prefix="/products", tags=["Admin - Products"])
router.include_router(dashboard.router, prefix="/dashboard", tags=["Admin - Dashboard"])
router.include_router(ai.router, prefix="/ai", tags=["Admin - AI Insights"])
router.include_router(reports.router, prefix="/reports", tags=["Admin - Reports"])

