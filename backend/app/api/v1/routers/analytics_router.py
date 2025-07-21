from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models
from app.database import get_async_db
from app.api.v1.routers.auth_router import get_current_admin_user
from app.schemas.analytics_schemas import AnalyticsStats

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/stats", response_model=AnalyticsStats)
async def get_analytics_stats(
    db: AsyncSession = Depends(get_async_db),
    current_user: models.User = Depends(get_current_admin_user),
):
    """
    Retrieve aggregated analytics stats. Only accessible by admin users.
    """
    total_users = await crud.get_total_users(db)
    total_addon_usage = await crud.get_total_addon_usage(db)
    usage_by_day = await crud.get_addon_usage_by_day(db)
    most_active_users = await crud.get_most_active_users(db)

    return {
        "total_users": total_users,
        "total_addon_usage": total_addon_usage,
        "usage_by_day": usage_by_day,
        "most_active_users": most_active_users,
    }
