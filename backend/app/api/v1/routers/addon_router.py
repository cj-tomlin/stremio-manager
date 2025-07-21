from typing import List, Dict, Any
import base64
import json
from urllib.parse import urlparse, quote
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSession, get_async_db
from app.api.v1.routers.auth_router import get_current_admin_user, get_current_user
from app.core.config import settings
from app import crud, models, schemas
from app.models import User
from app.schemas.addon_schemas import AddonUsageLog, TorrentioInstallationUrlResponse, AIOStreamsInstallationUrlResponse

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
    parsed_url = urlparse(settings.TORRENTIO_BASE_URL)
    hostname = parsed_url.netloc

    # Construct the installation URL in the format stremio://<hostname>/<config>/manifest.json
    installation_url = f"stremio://{hostname}/torbox={settings.TORBOX_API_KEY}/manifest.json"

    await crud.create_addon_usage_log(db=db, user=current_user)
    return TorrentioInstallationUrlResponse(installation_url=installation_url)


@router.get("/aiostreams/installation-url", response_model=AIOStreamsInstallationUrlResponse)
async def get_aiostreams_installation_url(
    db: AsyncSession = Depends(get_async_db),
    current_user: models.User = Depends(get_current_user)
) -> AIOStreamsInstallationUrlResponse:
    """
    Provides a Stremio installation URL for AIOstreams, pre-configured with all needed add-ons:
    - Self-hosted Comet (with shared TorBox API key)
    - AIOLists
    - OpenSubtitles
    - USA TV
    """
    # Get the hostname for our self-hosted Comet instance
    server_address = "localhost:8002"  # TODO: Replace with proper domain in production
    comet_manifest_url = f"http://{server_address}/manifest.json"
    
    # Define the addon configuration for AIOstreams
    config: Dict[str, Any] = {
        "addons": [
            # Our self-hosted Comet instance
            {
                "name": "Comet (Self-Hosted)",
                "manifestUrl": comet_manifest_url
            },
            # AIOLists for curated content
            {
                "name": "AIOLists",
                "manifestUrl": "https://aiolists.dexter21767.workers.dev/manifest.json"
            },
            # OpenSubtitles for subtitles
            {
                "name": "OpenSubtitles",
                "manifestUrl": "https://opensubtitlesv3-pro.dexter21767.com/manifest.json"
            },
            # USA TV for live TV streams
            {
                "name": "USA TV",
                "manifestUrl": "https://usa-tv.dexter21767.workers.dev/manifest.json"
            }
        ]
    }
    
    # Convert the configuration to a JSON string and encode it in base64
    encoded_config = base64.b64encode(json.dumps(config).encode()).decode()
    
    # Generate the installation URL in AIOstreams format
    installation_url = f"stremio://aiostreams.elfhosted.com/{encoded_config}/manifest.json"
    
    # Log the usage
    await crud.create_addon_usage_log(db=db, user=current_user)
    
    return AIOStreamsInstallationUrlResponse(installation_url=installation_url)


@router.get("/torrentio/usage-logs", response_model=List[AddonUsageLog])
async def read_addon_usage_logs(
    db: AsyncSession = Depends(get_async_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_admin_user),
):
    """
    Retrieves a list of addon usage logs.
    """
    logs = await crud.get_addon_usage_logs(db, skip=skip, limit=limit)
    return logs
