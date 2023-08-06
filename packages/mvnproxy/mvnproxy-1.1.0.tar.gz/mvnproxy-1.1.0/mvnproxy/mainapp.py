import os

import fastapi
import termcolor_util
import uvicorn
from fastapi.responses import FileResponse

from mvnproxy import config

# this must be read like this, not with a __main__ section
from mvnproxy.storage import is_cached, cache_path
from mvnproxy.storage.construct_maven_metadata import construct_maven_metadata
from mvnproxy.storage.download_artifact import download_artifact
from mvnproxy.storage.sha1_checksum import compute_sha1_checksum

os.makedirs(config.cache_folder, exist_ok=True)

app = fastapi.FastAPI()


print(
    termcolor_util.green(
        r"""
  __ _ _  _____  ___  _______ __ ____ __
 /  ' \ |/ / _ \/ _ \/ __/ _ \\ \ / // /
/_/_/_/___/_//_/ .__/_/  \___/_\_\\_, / 
              /_/                /___/  
"""
    )
)


def main():
    uvicorn.run(app, host=config.host, port=config.port)


@app.get("/")
def index_page():
    return FileResponse("static/index.html")


# @app.route('/repo/<path:path>', methods=['HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'])
# def not_implemented(path: str) -> None:
#     print(termcolor_util.red(f"Unable to process {path}: unsupported method"))
#     raise Exception("not implemented")


@app.get("/repo/{path:path}")
def maven_file(path: str):
    try:
        if is_cached(path):
            return FileResponse(cache_path(path))

        print(f"processing non-cached: {path}")

        if path.endswith(".sha1"):
            compute_sha1_checksum(path)
        elif path.endswith("/maven-metadata.xml"):
            construct_maven_metadata(path)
        else:
            download_artifact(path)

        return FileResponse(cache_path(path))
    except Exception as e:
        print(termcolor_util.red(f"Unable to process {path}: {e}"))
        raise e


if __name__ == "__main__":
    main()
