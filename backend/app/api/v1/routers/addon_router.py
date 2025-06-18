from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSession, get_async_db
from app.api.v1.routers.auth_router import get_current_user
from app.core.config import settings
from app import crud, models, schemas
from app.models import User
from app.schemas.addon_schemas import AddonUsageLog, TorrentioInstallationUrlResponse

router = APIRouter(prefix="/addons", tags=["addons"])


@router.get("/torrentio/installation-url", response_model=TorrentioInstallationUrlResponse)
async def get_torrentio_installation_url(
    db: AsyncSession = Depends(get_async_db),
    current_user: models.User = Depends(get_current_user)
) -> TorrentioInstallationUrlResponse:
    """
    Provides a Stremio installation URL for Torrentio, pre-configured with the 
    shared TorBox API key.
    """
    # Construct the part of the manifest URL that includes the base and configuration
    # e.g., torrentio.strem.fun/torbox=YOUR_API_KEY
    manifest_config_path = f"{settings.TORRENTIO_BASE_URL.replace('https://', '').replace('http://', '')}/torbox={settings.TORBOX_API_KEY}"
    
    # The full manifest URL would be https://[manifest_config_path]/manifest.json
    # The Stremio installation URL is stremio://[manifest_config_path]/manifest.json
    installation_url = f"stremio://{settings.TORRENTIO_BASE_URL}/torbox={settings.TORBOX_API_KEY}/manifest.json"
    await crud.create_addon_usage_log(db=db, user=current_user)
    return TorrentioInstallationUrlResponse(installation_url=installation_url)


@router.get("/torrentio/usage-logs", response_model=List[AddonUsageLog])
async def read_addon_usage_logs(
    db: AsyncSession = Depends(get_async_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_user),
):
    """
    Retrieves a list of addon usage logs.
    """
    logs = await crud.get_addon_usage_logs(db, skip=skip, limit=limit)
    return logs
