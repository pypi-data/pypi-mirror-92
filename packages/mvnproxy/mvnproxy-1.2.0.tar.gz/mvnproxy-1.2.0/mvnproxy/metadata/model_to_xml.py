import io
from typing import Optional, Union, List
from xml.etree.ElementTree import ElementTree, Element

from mvnproxy.metadata.model import (
    ModelMetadata,
    Snapshot,
    SnapshotVersion,
    Versioning,
    Plugin,
)


def write_model(model: Optional[ModelMetadata]) -> ElementTree:
    if not model:
        raise Exception("Expected a model, got none")

    result = ElementTree()
    result.parse(io.StringIO('<metadata modelVersion="1.1.0"/>'))

    metadata = result.getroot()

    xml_add_element_text(metadata, "groupId", model.groupId)
    xml_add_element_text(metadata, "artifactId", model.artifactId)
    xml_add_element_text(metadata, "version", model.version)
    xml_add_versioning(metadata, model.versioning)
    xml_add_plugins(metadata, model.plugins)

    return result


def xml_add_element_text(
    parent_element: Element, tag: str, text: Optional[Union[int, str, bool]]
) -> Optional[Element]:
    if text is None:
        return None

    element = xml_add_element(parent_element, tag)

    if isinstance(text, int):
        element.text = str(text)
    elif isinstance(text, bool):
        element.text = str(text).lower()
    else:
        element.text = text

    return element


def xml_add_element(node: Element, tag: str) -> Element:
    element = Element(tag)
    node.append(element)

    return element


def xml_add_versions(node: Element, versions: List[str]):
    if not versions:
        return

    versions_node = xml_add_element(node, "versions")

    for version in versions:
        xml_add_element_text(versions_node, "version", version)


def xml_add_snapshot(versions_node: Element, snapshot: Optional[Snapshot]):
    if not snapshot:
        return

    snapshot_node = xml_add_element(versions_node, "snapshot")

    xml_add_element_text(snapshot_node, "timestamp", snapshot.timestamp)
    xml_add_element_text(snapshot_node, "buildNumber", snapshot.buildNumber)
    xml_add_element_text(snapshot_node, "localCopy", snapshot.localCopy)


def xml_add_snapshot_versions(
    versions_element: Element, snapshotVersions: List[SnapshotVersion]
):
    if not snapshotVersions:
        return

    snapshot_versions_node = xml_add_element(versions_element, "snapshotVersions")

    for snapshotVersion in snapshotVersions:
        snapshot_version_node = xml_add_element(
            snapshot_versions_node, "snapshotVersion"
        )

        xml_add_element_text(
            snapshot_version_node, "extension", snapshotVersion.extension
        )
        xml_add_element_text(snapshot_version_node, "version", snapshotVersion.version)
        xml_add_element_text(snapshot_version_node, "updated", snapshotVersion.updated)
        xml_add_element_text(
            snapshot_version_node, "classifier", snapshotVersion.classifier
        )


def xml_add_versioning(metadata_element: Element, versioning: Optional[Versioning]):
    if versioning is None:
        return

    versioning_element = xml_add_element(metadata_element, "versioning")

    xml_add_element_text(versioning_element, "latest", versioning.latest)
    xml_add_element_text(versioning_element, "release", versioning.release)
    xml_add_versions(versioning_element, versioning.versions)
    xml_add_snapshot(versioning_element, versioning.snapshot)
    xml_add_element_text(versioning_element, "lastUpdated", versioning.lastUpdated)
    xml_add_snapshot_versions(versioning_element, versioning.snapshotVersions)


def xml_add_plugins(metadata_element: Element, plugins: List[Plugin]):
    if not plugins:
        return

    plugins_element = xml_add_element(metadata_element, "plugins")

    for plugin in plugins:
        plugin_element = xml_add_element(plugins_element, "plugin")

        xml_add_element_text(plugin_element, "artifactId", plugin.artifactId)
        xml_add_element_text(plugin_element, "prefix", plugin.prefix)
        xml_add_element_text(plugin_element, "name", plugin.name)
