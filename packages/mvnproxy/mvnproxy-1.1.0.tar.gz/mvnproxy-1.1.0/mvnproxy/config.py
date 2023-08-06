import os
import sys
from typing import cast, Dict

import addict
import yaml
from termcolor_util import red

# read the configuration file, and return some "decent" error
_config_file_path = "mvnproxy.yml"

if not os.path.isfile(_config_file_path):
    home_folder = os.environ.get("HOME") or ""
    _config_file_path = os.path.join(home_folder, ".mvnproxy")

if not os.path.isfile(_config_file_path):
    print(
        red("No configuration given.", bold=True),
        red("Unable to find"),
        red("mvnproxy.yml", bold=True),
        red("nor"),
        red(_config_file_path, bold=True),
    )
    sys.exit(1)

# interpolate environment variables
with open(_config_file_path, "rt", encoding="utf-8") as f:
    config_content_template = f.read()
    config_content = config_content_template.format(**os.environ)
    data = addict.Dict(cast(Dict, yaml.safe_load(config_content)))

if not data.mirrors:
    print(red("No mirrors defined in"), red(_config_file_path, bold=True))
    sys.exit(2)

# use defaults and export variables
cache_folder = data.get("cache_folder", "/tmp/mvnproxy")
host = data.get("host", "0.0.0.0")
port = int(data.get("port", 7000))
