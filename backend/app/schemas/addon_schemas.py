from datetime import datetime
from pydantic import BaseModel, HttpUrl


class TorrentioInstallationUrlResponse(BaseModel):
    installation_url: str # Stremio URLs are custom scheme, not HttpUrl


class AddonUsageLog(BaseModel):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
