import os.path
from lxml import etree


from .advanced.nautilus import build_resolver
from .advanced.chunker import build_chunker
from .advanced.nemo import BuildNemoClass


current_folder = os.path.dirname(__file__)

with open(os.path.join(current_folder, "../nemo.xml")) as xml_file:
    configuration_xml = etree.parse(xml_file)

organizer, resolver, cache = build_resolver(
    os.path.join(
        current_folder,
        "../corpora.xml"
    )
)

chunker = build_chunker(configuration_xml)

nemo_class = BuildNemoClass(configuration_xml)

templates_folder = os.path.abspath(os.path.join(current_folder, "../templates"))
