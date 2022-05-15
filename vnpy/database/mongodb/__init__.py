from .mongodb_database import database_manager

import importlib_metadata

from .mongodb_database import MongodbDatabase as Database

try:
    __version__ = importlib_metadata.version("vnpy_mongodb")
except importlib_metadata.PackageNotFoundError:
    __version__ = "dev"