import io
import os
from xml.etree.ElementTree import ElementTree

import requests

from mvnproxy import config
from mvnproxy.metadata.merger import merge_maven_metadata, xml_to_string
from mvnproxy.storage import cache_path

import logging

LOG = logging.getLogger(__name__)


def construct_maven_metadata(path: str) -> None:
    artifact_folder = cache_path(os.path.dirname(path))
    os.makedirs(artifact_folder, exist_ok=True)

    known_xmls = []

    for mirror in config.data.mirrors:
        LOG.info("Trying to fetch %s%s", mirror.url, path)
        auth = None

        if mirror.auth:
            auth = (mirror.auth["user"], mirror.auth["pass"])

        r = requests.get(f"{mirror.url}{path}", auth=auth)

        if not r.ok:
            LOG.debug("Failed to resolve %s%s: %s", mirror, path, r)
            continue

        known_xmls.append(ElementTree(file=io.BytesIO(r.content)))

    out_xml = merge_maven_metadata(known_xmls)

    with open(cache_path(path), "wt", encoding="utf-8") as f:
        f.write(xml_to_string(out_xml))
