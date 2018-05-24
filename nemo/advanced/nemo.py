from lxml import etree

from flask_nemo import Nemo
from flask import Markup, redirect, url_for
from MyCapytain.resources.prototypes.cts.inventory import CtsWorkMetadata, CtsEditionMetadata
from MyCapytain.errors import UnknownCollection
from MyCapytain.common.constants import Mimetypes


class NemoTemplate(Nemo):
    """ This class is here for advanced developers.

    Enhance it or modify it to fit your needs !

    """
    def r_full_text(self, objectId, lang=None):
        """ Retrieve the text of the passage
        :param objectId: Collection identifier
        :type objectId: str
        :param lang: Lang in which to express main data
        :type lang: str
        :param subreference: Reference identifier
        :type subreference: str
        :return: Template, collections metadata and Markup object representing the text
        :rtype: {str: Any}
        """
        collection = self.get_collection(objectId)
        if isinstance(collection, CtsWorkMetadata):
            editions = [t for t in collection.children.values() if isinstance(t, CtsEditionMetadata)]
            if len(editions) == 0:
                raise UnknownCollection("This work has no default edition")
            return redirect(url_for(".r_full_text", objectId=str(editions[0].id)))
        text = self.get_passage(objectId=objectId, subreference=None)
        passage = self.transform(text, text.export(Mimetypes.PYTHON.ETREE), objectId)
        return {
            "template": "main::text.html",
            "objectId": objectId,
            "subreference": None,
            "collections": {
                "current": {
                    "label": collection.get_label(lang),
                    "id": collection.id,
                    "model": str(collection.model),
                    "type": str(collection.type),
                    "author": text.get_creator(lang),
                    "title": text.get_title(lang),
                    "description": text.get_description(lang),
                    "citation": collection.citation,
                    "coins": self.make_coins(collection, text, "", lang=lang)
                },
                "parents": self.make_parents(collection, lang=lang)
            },
            "text_passage": Markup(passage),
            "prev": None,
            "next": None
        }

    def r_about(self):
        return {
            "template": "main::about.html"
        }


def BuildNemoClass(configuration_file):
    """

    :param configuration_file:
    :return: Nemo class with registered option
    :rtype: class
    """
    for add_route_full_text in configuration_file.xpath("//full-text-route/text()"):
        if add_route_full_text.lower() == "true":
            NemoTemplate.ROUTES += [("/text/<objectId>/complete", "r_full_text", ["GET"])]
            NemoTemplate.CACHED += ["r_full_text"]

    for add_route_for_about in configuration_file.xpath("//about-route/text()"):
        if add_route_for_about.lower() == "true":
            NemoTemplate.ROUTES += [("/about", "r_about", ["GET"])]

    return NemoTemplate
