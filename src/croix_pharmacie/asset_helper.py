import importlib.resources
from pathlib import Path

PATH_PACKAGE = "croix_pharmacie.assets"

def get_asset_path(file_name: str, subdirs: str | None = None) -> Path:
    package = f"{PATH_PACKAGE}.{subdirs}" if subdirs else PATH_PACKAGE
    with importlib.resources.path(package, file_name) as path:
        return path