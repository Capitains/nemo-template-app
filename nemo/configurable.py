import os.path
from lxml import etree


from .advanced.nautilus import build_resolver
from .advanced.chunker import build_chunker
from .advanced.nemo import BuildNemoClass
from .advanced.xslts import build_xslt_dict


current_folder = os.path.dirname(__file__)
configuration_path = os.path.abspath(os.path.join(current_folder, "../app.xml"))

with open(configuration_path) as xml_file:
    configuration_xml = etree.parse(xml_file)

organizer, resolver, cache = build_resolver(
    os.path.join(
        current_folder,
        "../corpora.xml"
    )
)

chunker = build_chunker(configuration_xml)

xslt_dict = build_xslt_dict(configuration_xml, configuration_path)

nemo_class = BuildNemoClass(configuration_xml)

templates_folder = os.path.abspath(os.path.join(current_folder, "../templates"))
statics_folder = os.path.abspath(os.path.join(current_folder, "../statics"))
