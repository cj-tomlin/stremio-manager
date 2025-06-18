from pydantic_settings import BaseSettings, SettingsConfigDict
import os

# Build a path to the .env file.
# It should be in the `backend` directory, which is two levels up from this file's directory.
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')

class Settings(BaseSettings):
    PROJECT_NAME: str = "Stremio Manager"

    # Trakt OAuth
    TRAKT_CLIENT_ID: str
    TRAKT_CLIENT_SECRET: str

    # Torrentio/Torbox Configuration
    TORRENTIO_BASE_URL: str = "https://torrentio.strem.fun"
    TORBOX_API_KEY: str # Loaded from .env

    # JWT settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(env_file=dotenv_path)

settings = Settings()
