import importlib_metadata

from .influxdb_database import InfluxdbDatabase as Database


try:
    __version__ = importlib_metadata.version("vnpy_influxdb")
except importlib_metadata.PackageNotFoundError:
    __version__ = "dev"