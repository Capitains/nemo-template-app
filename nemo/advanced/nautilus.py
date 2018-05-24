import os.path

from lxml import etree
from werkzeug.contrib.cache import SimpleCache, FileSystemCache

from MyCapytain.resources.prototypes.cts.inventory import CtsTextInventoryCollection, CtsTextInventoryMetadata
from MyCapytain.resolvers.utils import CollectionDispatcher
from capitains_nautilus.cts.resolver import NautilusCTSResolver


def relative_folder(configuration_file, directory):
    """

    :param configuration_file:
    :param directory:
    :return:
    """
    return os.path.abspath(
            os.path.join(
                os.path.abspath(os.path.dirname(configuration_file)),
                directory
            )
        )


def collection_dispatcher_builder(collection, prefix_filters, citation_filters):
    """

    :param collection:
    :param prefix_filters:
    :param citation_filters:
    :return:
    """
    prefix_results = len(prefix_filters) == 0
    citation_results = len(citation_filters) == 0

    for anonymous_function in prefix_filters:
        if anonymous_function(collection) is True:
            prefix_results = True
            break
    for anonymous_function in citation_filters:
        if anonymous_function(collection) is True:
            citation_results = True
            break

    print(collection, prefix_results, citation_results)
    return prefix_results and citation_results


def citation_contain_filter(collection, citation_name):
    for text in collection.readableDescendants:
        for citation in text.citation:
            if citation.name == citation_name:
                return True
    return False


def build_resolver(configuration_file):
    """

    :param configuration_file:
    :return: Organizer, Resolver and Cache handler
    """
    with open(configuration_file) as f:
        xml = etree.parse(f)

    directories = [
        # Compute path relative to the configuration files
        relative_folder(configuration_file, directory)
        for directory in xml.xpath("//corpora/corpus/text()")
    ]

    default_collection = None
    general_collection = CtsTextInventoryCollection()
    filters_to_register = []

    for collection in xml.xpath("//collections/collection"):
        identifier = collection.xpath("./identifier/text()")[0]
        if collection.get("default") == "true":
            default_collection = identifier

        current_collection = CtsTextInventoryMetadata(
            identifier,
            parent=general_collection
        )
        for name in collection.xpath("./name"):
            current_collection.set_label(name.text, name.get("lang"))

        # We look at dispatching filters in the collection
        for filters in collection.xpath("./filter"):

            # We register prefix filters
            prefix_filters = []
            for prefix in filters.xpath("./id-starts-with/text()"):
                prefix_filters.append(lambda collection, path=None, **kwargs: str(collection.id).startswith(prefix))

            # We register citation filters
            citation_filters = []
            for citation_name in filters.xpath("./citation-contains/text()"):
                citation_filters.append(lambda collection, path=None, **kwargs: citation_contain_filter(collection, citation_name))

            filters_to_register += [
                (
                    identifier,
                    lambda collection, path=None, **kwargs: collection_dispatcher_builder(
                        collection,
                        prefix_filters,
                        citation_filters
                    )
                )
            ]

    # Create the dispatcher
    organizer = CollectionDispatcher(
        general_collection,
        default_inventory_name=default_collection
    )

    for destination_collection, anonymous_dispatching_function in filters_to_register:
        organizer.add(anonymous_dispatching_function, destination_collection)

    # Set-up the cache folder
    # ToDO : Add a system for redis ?
    cache = None
    for cache_folder in xml.xpath("//cache-folder/text()"):
        cache = FileSystemCache(cache_folder)
    if cache is None:
        cache = SimpleCache()

    resolver = NautilusCTSResolver(
        resource=directories,
        dispatcher=organizer,
        cache=cache
    )

    return organizer, resolver, cache


if __name__ == "__main__":
    organizer, resolver, cache = build_resolver(
        os.path.join(
            os.path.dirname(__file__),
            "../../corpora.xml"
        )
    )
    from MyCapytain.common.constants import Mimetypes
    resolver.parse()
    print(resolver.getMetadata("sources").export(Mimetypes.XML.CTS))
