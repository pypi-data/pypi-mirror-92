import unittest
from xml.etree.ElementTree import ElementTree

from mvnproxy.metadata.merger import merge_maven_metadata, xml_to_string


def read_xml(file_path: str):
    return ElementTree(file=file_path)


class TestXmlMerge(unittest.TestCase):
    def test_merge(self) -> None:
        xml1 = read_xml("tests/data/maven-metadata-release.xml")
        xml2 = read_xml("tests/data/maven-metadata-full.xml")
        xml3 = read_xml("tests/data/maven-snapshot-metadata-v1.xml")

        xmlout = merge_maven_metadata([xml1, xml2, xml3])

        self.assertTrue(xmlout, "we should have a merged xml")

        pretty_xml_as_string = xml_to_string(xmlout)
        print(pretty_xml_as_string)

    def test_missing_fields(self) -> None:
        xml1 = read_xml("tests/data/missing-fields.xml")
        xmlout = merge_maven_metadata([xml1])
        self.assertTrue(xmlout, "we should have a merged xml")

        pretty_xml_as_string = xml_to_string(xmlout)
        print(pretty_xml_as_string)

    def test_merge_mixed_snapshot(self) -> None:
        xml1 = read_xml("tests/data/maven-snapshot-metadata.xml")
        xml2 = read_xml("tests/data/maven-metadata-full.xml")

        xmlout = merge_maven_metadata([xml1, xml2])

        self.assertTrue(xmlout, "we should have a merged xml")

        pretty_xml_as_string = xml_to_string(xmlout)
        print(pretty_xml_as_string)
