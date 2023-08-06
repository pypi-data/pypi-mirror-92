import string
import xml
from typing import Iterable
from xml.etree.ElementTree import Element, ElementTree

from mvnproxy.metadata.model_to_xml import write_model
from mvnproxy.metadata.xml_to_model import read_model


def _version_comparator(v1: str, v2: str) -> int:
    v1_tokens = v1.split(".")
    v2_tokens = v2.split(".")

    for i in range(min(len(v1_tokens), len(v2_tokens))):
        len1 = len(v1_tokens[i].strip(string.digits))
        v1_numeric_token = v1_tokens[i][0:-len1] if len1 else v1_tokens[i]
        len2 = len(v2_tokens[i].strip(string.digits))
        v2_numeric_token = v2_tokens[i][0:-len2] if len2 else v2_tokens[i]

        if not v1_numeric_token and not v2_numeric_token:
            return 0

        if not v2_numeric_token:
            return 1

        if not v1_numeric_token:
            return -1

        token_v1 = int(v1_numeric_token)
        token_v2 = int(v2_numeric_token)

        if token_v1 - token_v2 != 0:
            return token_v1 - token_v2

    if len(v1_tokens) > len(v2_tokens):
        return 1
    elif len(v1_tokens) < len(v2_tokens):
        return -1
    else:
        return 0


def merge_maven_metadata(documents: Iterable[xml.etree.ElementTree.ElementTree]):
    if not documents:
        raise Exception("No documents passed for merging")

    result = None
    for document in documents:
        if not result:
            result = read_model(document.getroot())
            continue

        other_model = read_model(document.getroot())
        result.merge(other_model)

    return write_model(result)


def xml_to_string(document: ElementTree) -> str:
    return xml.etree.ElementTree.tostring(
        document.getroot(), encoding="utf8", method="xml"
    ).decode("utf-8")
