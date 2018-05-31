from unittest import TestCase
import os
from lxml import objectify, etree
import shutil
from MyCapytain.common.constants import get_graph

class CorporaConfig(object):
    def __init__(
            self,
            cache_folder="./cache_folder",
            corpora=None
    ):
        """

        :param cache_folder:
        :param corpora:
        :param collections:
        """

        default_corpora = [
            "example_corpora/other"
        ]
        self.cache_folder = cache_folder
        self.corpora = corpora or default_corpora
        self.collections = []

    def add_collection(
            self,
            identifier,
            default=False, names=None,
            filter_folder=None, filter_identifer=None
    ):
        self.collections.append({
            "default": default,
            "names": names or {},
            "identifier": identifier,
            "filters": [
               {"type": "folder", "value": value} for value in filter_folder or []
            ] + [
               {"type": "id-starts-with", "value": value} for value in filter_identifer or []
            ]
        })

    @staticmethod
    def collection_serializer(node):
        default = ""
        if node["default"]:
            default = " default=\"true\""
        xml = "<collection"+default+">"
        xml += "<identifier>"+node["identifier"]+"</identifier>"
        for lang, name in node["names"].items():
            xml += "<name lang=\""+lang+"\">"+name+"</name>"
        if node["filters"]:
            xml += "<filters>"
            for filter_ in node["filters"]:
                xml += "<"+filter_["type"]+">"+filter_["value"]+"</"+filter_["type"]+">"
            xml += "</filters>"
        return xml+"</collection>"

    def xml(self):
        corpora = "\n".join([
            """<corpus>{}</corpus>""".format(corpus_folder)
            for corpus_folder in self.corpora
        ])
        collections = "\n".join([
            CorporaConfig.collection_serializer(collection)
            for collection in self.collections
        ])
        xml = """<configuration>
        <cache-folder>{cache_folder}</cache-folder>
        <corpora>{corpora}</corpora>
        <collections>{collections}</collections>
</configuration>""".format(
            cache_folder=self.cache_folder,
            corpora=corpora,
            collections=collections
        )
        return xml


class BaseTest(TestCase):
    def setUp(self):
        self.origin_app_xml = self.app_xml = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..", "app.xml"
            )
        )
        self.origin_corpora_xml = self.corpora_xml = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..", "corpora.xml"
            )
        )

        self.default_app_xml = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "test_data", "default_configs", "app.xml"
            )
        )
        self.default_corpora_xml = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "test_data", "default_configs", "corpora.xml"
            )
        )

        self.origin_corpora_xml = self.corpora_xml = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..", "corpora.xml"
            )
        )

        self.origin_app_xml += ".bak"
        self.origin_corpora_xml += ".bak"
        shutil.copy2(self.app_xml, self.origin_app_xml)
        shutil.copy2(self.corpora_xml, self.origin_corpora_xml)

        shutil.copy2(self.default_app_xml, self.app_xml)
        shutil.copy2(self.default_corpora_xml, self.corpora_xml)

        self.client = None
        self.nemo = None
        self.nautilus = None

    def tearDown(self):
        shutil.copy2(self.origin_app_xml, self.app_xml)
        shutil.copy2(self.origin_corpora_xml, self.corpora_xml)
        os.remove(self.origin_app_xml)
        os.remove(self.origin_corpora_xml)

        if self.client:
            del self.client

        if self.nemo or self.nautilus:
            get_graph().remove((None, None, None))

            if self.nemo:
                del self.nemo
            if self.nautilus:
                del self.nautilus

    def create_corpora(self, cache_folder="./cache_folder", corpora=None):
        return CorporaConfig(cache_folder, corpora)

    def write_corpora_config(self, config):
        """ Write the configuration app

        :param config: Configuration for corpora
        :type config: CorporaConfig
        """
        with open(self.corpora_xml, "w") as f:
            f.write(config.xml())

    def create_app(self):
        """ Creates the app and set it to run

        :return: Client, Nemo, Nautilus
        :rtype: (FlaskClient, flask_nemo.Nemo, capitains_nautilus.flask_ext.FlaskNautilus)
        """
        from nemo.app import app, extension_nemo, extension_nautilus

        self.client = app.app.test_client()
        self.nemo = extension_nemo
        self.nautilus = extension_nautilus

        return self.client, self.nemo, self.nautilus

    def withConfig(self, app_xml, corpora_xml):
        """ Loads the following config

        :param app_xml:
        :param corpora_xml:
        :return:
        """
        self.app_xml = app_xml
        self.corpora_xml = corpora_xml


class TestBaseTest(TestCase):
    """ Test the mockup tools for tests"""
    def test_app_serialization(self):
        a = CorporaConfig()
        a.add_collection("id1", False, {"fre": "Nom", "eng": "Name"},
                         filter_folder=["dossier1"], filter_identifer=["id1"])
        a.add_collection("id2", True, {"fre": "Nom2", "eng": "Name2"})

        xml = etree.fromstring(a.xml())

        self.assertEqual(
            sorted(xml.xpath("/configuration/collections/collection/identifier/text()")),
            ["id1", "id2"],
            "Collection identifiers should be compiled"
        )
        self.assertEqual(
            sorted(xml.xpath("/configuration/collections/collection/name[@lang='eng']/text()")),
            ["Name", "Name2"],
            "Name should be serialized"
        )
        self.assertEqual(
            sorted(xml.xpath("/configuration/collections/collection/name[@lang='fre']/text()")),
            ["Nom", "Nom2"],
            "Name should be serialized"
        )
        self.assertEqual(
            sorted(xml.xpath("/configuration/collections/collection[./identifier/text()='id1']/filters/folder/text()")),
            ["dossier1"],
            "Folder filter should be dealt with"
        )
        self.assertEqual(
            xml.xpath("/configuration/collections/collection[./identifier/text()='id1']"
                             "/filters/id-starts-with/text()"),
            ["id1"],
            "ID Folder should be dealt with"
        )
        self.assertEqual(
            xml.xpath("/configuration/collections/collection[@default='true']/identifier/text()"),
            ["id2"],
            "Default collection should be found"
        )
        self.assertEqual(
            len(xml.xpath("/configuration/collections/collection[@default='true']/filters")),
            0,
            "Filters should only be append to the right nodes"
        )
