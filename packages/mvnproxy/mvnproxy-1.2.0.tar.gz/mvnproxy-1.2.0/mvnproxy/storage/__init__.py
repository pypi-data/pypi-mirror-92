import os
from mvnproxy import config


def is_cached(path: str) -> bool:
    return os.path.isfile(cache_path(path))


def cache_path(path: str) -> str:
    return os.path.join(config.cache_folder, path)
