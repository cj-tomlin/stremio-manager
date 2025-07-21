# This file makes Python treat the 'schemas' directory as a package.
# It also makes schemas available at the top level of the package.

from .user_schemas import User, UserCreate, UserUpdate, Token, TokenData
from .addon_schemas import TorrentioInstallationUrlResponse

