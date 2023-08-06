import os

import requests
import termcolor_util

from mvnproxy import config
from mvnproxy.storage import cache_path


def download_artifact(path) -> None:
    artifact_folder = cache_path(os.path.dirname(path))
    os.makedirs(artifact_folder, exist_ok=True)

    for mirror in config.data.mirrors:
        print(f"Trying to fetch {mirror.url}{path}")
        auth = None

        if mirror.auth:
            auth = (mirror.auth["user"], mirror.auth["pass"])

        r = requests.get(f"{mirror.url}{path}", auth=auth)

        if not r.ok:
            if r.status_code == 401:
                print(
                    termcolor_util.red(
                        f"401 UNAUTHORIZED: {mirror.url} failed to resolve {path}: {r}"
                    )
                )
            if r.status_code == 403:
                print(
                    termcolor_util.red(
                        f"403 FORBIDDEN: {mirror.url} failed to resolve {path}: {r}"
                    )
                )
            else:
                print(
                    termcolor_util.yellow(f"{mirror.url} failed to resolve {path}: {r}")
                )

            continue

        with open(cache_path(path), "wb") as f:
            f.write(r.content)

        return
