from typing import Optional
from xml.etree.ElementTree import Element

from mvnproxy.metadata.model import ModelMetadata, Snapshot, SnapshotVersion, Plugin


def read_model(metadata: Element) -> ModelMetadata:
    # read base
    result = ModelMetadata(
        groupId=xml_read_required_text(metadata, "./groupId"),
        artifactId=xml_read_required_text(metadata, "./artifactId"),
    )
    result.version = xml_read_text(metadata, "./version")

    # read versioning
    result.versioning.lastUpdated = xml_read_text(metadata, "./versioning/lastUpdated")
    result.versioning.latest = xml_read_text(metadata, "./versioning/latest")
    result.versioning.release = xml_read_text(metadata, "./versioning/release")
    result.versioning.snapshot = xml_read_snapshot(metadata, "./versioning/snapshot")

    # read versioning/versions
    for version_node in metadata.findall("./versioning/versions/version"):
        if not version_node.text:
            raise Exception(f"Unable to find text in versoin node: {version_node}")

        result.versioning.versions.append(version_node.text)

    # read versioning/snapshotVersions
    for snapshot_node in metadata.findall(
        "./versioning/snapshotVersions/snapshotVersion"
    ):
        result.versioning.snapshotVersions.append(
            xml_read_snapshot_version(snapshot_node)
        )

    # read plugins
    for plugin_node in metadata.findall("./plugins/plugin"):
        result.plugins.append(xml_read_plugin(plugin_node))

    return result


def xml_read_snapshot(node: Element, path: str) -> Optional[Snapshot]:
    snapshot_node = node.find(path)

    if snapshot_node is None:
        return None

    snapshot = Snapshot()
    snapshot.timestamp = xml_read_text(snapshot_node, "./timestamp")

    build_number = xml_read_int(snapshot_node, "./buildNumber")
    if build_number is not None:
        snapshot.buildNumber = build_number

    local_copy = xml_read_bool(snapshot_node, "./localCopy")
    if local_copy is not None:
        snapshot.localCopy = local_copy

    return snapshot


def xml_read_plugin(plugin_node: Element) -> Plugin:
    return Plugin(
        name=xml_read_required_text(plugin_node, "./name"),
        artifactId=xml_read_required_text(plugin_node, "./artifactId"),
        prefix=xml_read_required_text(plugin_node, "./prefix"),
    )


def xml_read_snapshot_version(snapshot_node: Element) -> SnapshotVersion:
    snapshot_version = SnapshotVersion()

    snapshot_version.version = xml_read_text(snapshot_node, "./value")
    snapshot_version.extension = xml_read_text(snapshot_node, "./extension")
    snapshot_version.updated = xml_read_text(snapshot_node, "./updated")
    snapshot_version.classifier = xml_read_text(snapshot_node, "./classifier")

    return snapshot_version


def xml_read_int(node: Element, path: str) -> Optional[int]:
    n = node.find(path)

    if n is None:
        return None

    if not n.text:
        raise Exception(f"Unable to read int on node {node} with path {path}")

    return int(n.text)


def xml_read_bool(node: Element, path: str) -> Optional[bool]:
    n = node.find(path)

    if n is None:
        return None

    if not n.text:
        raise Exception(f"Unable to read bool on node {node} with path {path}")

    return n.text.lower() == "true"


def xml_read_text(node: Element, path: str) -> Optional[str]:
    n = node.find(path)

    if n is None:
        return None

    return n.text


def xml_read_required_text(node: Element, path: str) -> str:
    n = node.find(path)

    if n is None:
        raise Exception(f"Unable to find text node for {node} with path {path}")

    if not n.text:
        raise Exception(f"Unable to read text on node {node} with path {path}")

    return n.text
