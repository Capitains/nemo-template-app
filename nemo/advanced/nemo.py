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
    def __init__(self, *args, **kwargs):

        self.has_about_route = kwargs.get("about_route", False)
        if self.has_about_route:
            del kwargs["about_route"]

        self.has_full_text_route = kwargs.get("full_text_route", False)
        if self.has_full_text_route:
            del kwargs["full_text_route"]

        super(NemoTemplate, self).__init__(*args, **kwargs)

    def render(self, template, **kwargs):
        kwargs["has_about_route"] = self.has_about_route
        kwargs["has_full_text_route"] = self.has_full_text_route
        return super(NemoTemplate, self).render(template, **kwargs)

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
        """ An about page
        """
        return {
            "template": "main::about.html"
        }


def build_nemo(configuration_file, *args, **kwargs):
    """

    :param configuration_file:
    :return: Nemo class with registered option
    :rtype: class
    """
    for add_route_full_text in configuration_file.xpath("//full-text-route/text()"):
        if add_route_full_text.lower() == "true":
            NemoTemplate.ROUTES += [("/text/<objectId>/complete", "r_full_text", ["GET"])]
            NemoTemplate.CACHED += ["r_full_text"]
            kwargs["full_text_route"] = True

    for add_route_for_about in configuration_file.xpath("//about-route/text()"):
        if add_route_for_about.lower() == "true":
            NemoTemplate.ROUTES += [("/about", "r_about", ["GET"])]
            NemoTemplate.CACHED += ["r_about"]
            kwargs["about_route"] = True

    return NemoTemplate(*args, **kwargs)
