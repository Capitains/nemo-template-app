import os.path
from lxml import etree


from .advanced.nautilus import build_resolver
from .advanced.chunker import build_chunker
from .advanced.nemo import build_nemo
from .advanced.xslts import build_xslt_dict
from .advanced.errors import Error404


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


def nemo_class(*args, **kwargs):
    return build_nemo(configuration_xml, *args, **kwargs)


templates_folder = os.path.abspath(os.path.join(current_folder, "../templates/main"))
templates_folder_additional = os.path.abspath(os.path.join(current_folder, "../templates/additional-pages"))
statics_folder = os.path.abspath(os.path.join(current_folder, "../statics"))


def instantiate_errors(app, nemo):
    @app.errorhandler(Error404)
    def error_handler(e):
        return nemo.page_not_found(e)
