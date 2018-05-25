from lxml import etree

from flask import render_template
from flask_nemo import Nemo
from flask import Markup, redirect, url_for
from MyCapytain.resources.prototypes.cts.inventory import CtsWorkMetadata, CtsEditionMetadata
from MyCapytain.errors import UnknownCollection
from MyCapytain.common.constants import Mimetypes


from .errors import Error404


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

        self.disable_reffs = kwargs.get("disable_browse_reffs_and_passage", False)
        if self.disable_reffs:
            del kwargs["disable_browse_reffs_and_passage"]

        self.full_texts_only = kwargs.get("full_texts_only", [])
        if len(self.full_texts_only) > 0:
            del kwargs["full_texts_only"]

        self.additional_pages = kwargs.get("additional_pages", {})
        if len(self.additional_pages) > 0:
            del kwargs["additional_pages"]

        super(NemoTemplate, self).__init__(*args, **kwargs)

    def render(self, template, **kwargs):
        kwargs["has_about_route"] = self.has_about_route
        kwargs["has_full_text_route"] = self.has_full_text_route
        kwargs["disable_reffs"] = self.disable_reffs
        kwargs["full_texts_only"] = self.full_texts_only
        kwargs["additional_pages"] = self.additional_pages
        return super(NemoTemplate, self).render(template, **kwargs)

    def check_allowed_partial_text(self, objectId):
        if self.disable_reffs or objectId in self.full_texts_only:
            raise Error404("This text can't be browsed this way.")

    def r_first_passage(self, objectId):
        self.check_allowed_partial_text(objectId)
        return super(NemoTemplate, self).r_first_passage(objectId)

    def r_references(self, objectId, lang=None):
        self.check_allowed_partial_text(objectId)
        return super(NemoTemplate, self).r_references(objectId, lang)

    def r_passage(self, objectId, subreference, lang=None):
        self.check_allowed_partial_text(objectId)
        return super(NemoTemplate, self).r_passage(objectId, subreference, lang)

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

    def r_page(self, page_id):
        if page_id not in self.additional_pages:
            raise Error404("This page does not exist or was removed.")
        return {
            "template": "additional::{}".format(self.additional_pages[page_id]["template"])
        }

    def page_not_found(self, e):
        kwargs = {}
        kwargs["lang"] = self.get_locale()
        kwargs["assets"] = self.assets
        kwargs["main_collections"] = self.main_collections(kwargs["lang"])
        return render_template("main::404.html", message=e.message, **kwargs), 404


def build_nemo(configuration_file, *args, **kwargs):
    """

    :param configuration_file:
    :return: Nemo class with registered option
    :rtype: class
    """
    for add_route_full_text in configuration_file.xpath("//full-text-route[1]/text()"):
        if add_route_full_text.lower() == "true":
            NemoTemplate.ROUTES += [("/text/<objectId>/complete", "r_full_text", ["GET"])]
            NemoTemplate.CACHED += ["r_full_text"]
            kwargs["full_text_route"] = True

        for text_only_node in configuration_file.xpath("//full-text-only[1]"):
            if text_only_node.get("all", "false").lower() == "true":
                kwargs["disable_browse_reffs_and_passage"] = True
            else:
                kwargs["full_texts_only"] = list(
                    text_only_node.xpath("./id/text()")
                )

    pages = list(configuration_file.xpath("//additional-pages[1]"))
    if len(pages):
        NemoTemplate.ROUTES += [("/page/<path:page_id>", "r_page", ["GET"])]
        NemoTemplate.CACHED += ["r_page"]
        kwargs["additional_pages"] = {
            page.get("id"): {
                "template": page.get("template"),
                "title": page.xpath("./link-title[1]/text()")[0]
            }
            for page in pages[0].xpath("./page")
        }

    for add_route_for_about in configuration_file.xpath("//about-route[1]/text()"):
        if add_route_for_about.lower() == "true":
            NemoTemplate.ROUTES += [("/about", "r_about", ["GET"])]
            NemoTemplate.CACHED += ["r_about"]
            kwargs["about_route"] = True

    return NemoTemplate(*args, **kwargs)
