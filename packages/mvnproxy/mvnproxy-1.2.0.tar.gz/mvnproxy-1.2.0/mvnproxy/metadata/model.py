from typing import Optional, List


class ModelMetadata:
    def __init__(self, *, groupId: str, artifactId: str) -> None:
        self.model_version = "1.1.0"
        self.groupId = groupId
        self.artifactId = artifactId
        self.version: Optional[
            str
        ] = None  # the version this folder represents, used for snapshots only
        self.versioning: Versioning = Versioning()
        self.plugins: List[Plugin] = []

    def merge(self, source_metadata: "ModelMetadata") -> None:
        for plugin in source_metadata.plugins:
            found = False
            for pre_existing in self.plugins:
                if pre_existing.prefix == plugin.prefix:
                    break

            if not found:
                self.plugins.append(
                    Plugin(
                        artifactId=plugin.artifactId,
                        prefix=plugin.prefix,
                        name=plugin.name,
                    )
                )

        versioning = source_metadata.versioning
        if versioning:
            if not self.versioning:
                self.versioning = Versioning()

            for version in versioning.versions:
                if version not in self.versioning.versions:
                    self.versioning.versions.append(version)

            if "null" == versioning.lastUpdated:
                versioning.lastUpdated = (
                    None  # FIXME: serialize nulls as "null" for lastUpdated
                )

            if "null" == self.versioning.lastUpdated:
                self.versioning.lastUpdated = None

            if not versioning.lastUpdated:
                versioning.lastUpdated = self.versioning.lastUpdated

            assert versioning.lastUpdated

            if (
                not self.versioning.lastUpdated
                or self.versioning.lastUpdated < versioning.lastUpdated
            ):
                self.versioning.lastUpdated = versioning.lastUpdated

                if versioning.release:
                    self.versioning.release = versioning.release

                if versioning.latest:
                    self.versioning.latest = versioning.latest

                if versioning.snapshot:
                    self.versioning.snapshot = versioning.snapshot


class Versioning:
    def __init__(self):
        self.latest: Optional[
            str
        ] = None  # what the latest version in the directory is, including snapshots
        self.release: Optional[str] = None  # current release (non snapshot)
        self.snapshot: Optional[
            Snapshot
        ] = None  # current snapshot data used for this version

        self.versions: List[
            str
        ] = []  # versions available for the artifact - release + snapshots
        self.lastUpdated: Optional[str] = None  # when was the metadata last updated
        self.snapshotVersions: List[SnapshotVersion] = []


class Snapshot:
    def __init__(self):
        self.timestamp: Optional[str] = None
        self.buildNumber: int = 0
        self.localCopy: bool = False


class SnapshotVersion:
    def __init__(self):
        self.classifier: Optional[str] = None
        self.extension: Optional[str] = None
        self.version: Optional[str] = None  # serialized as 'value'
        self.updated: Optional[str] = None


class Plugin:
    def __init__(self, name: str, prefix: str, artifactId: str) -> None:
        self.name = name
        self.prefix = prefix
        self.artifactId = artifactId
