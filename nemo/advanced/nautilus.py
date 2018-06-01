import os.path

from lxml import etree
from werkzeug.contrib.cache import SimpleCache, FileSystemCache

from MyCapytain.resources.prototypes.cts.inventory import CtsTextInventoryCollection, CtsTextInventoryMetadata
from MyCapytain.resolvers.utils import CollectionDispatcher
from capitains_nautilus.cts.resolver import NautilusCTSResolver


from .utils import relative_folder


def collection_dispatcher_builder(prefix_filters, citation_filters, directory_filters):
    """

    Any condition that is True would make the would category True.
    All condition's category need to be True : A filter and a Path needs to be True

    :param prefix_filters:
    :param citation_filters:
    :param directory_filters:
    :return:
    """
    def dispatcher(collection, path=None, **kwargs):
        prefix_results = len(prefix_filters) == 0
        citation_results = len(citation_filters) == 0
        directory_results = len(directory_filters) == 0

        for anonymous_function in prefix_filters:
            if anonymous_function(collection) is True:
                prefix_results = True
                break

        for anonymous_function in citation_filters:
            if anonymous_function(collection) is True:
                citation_results = True
                break

        for anonymous_function in directory_filters:
            if anonymous_function(collection, path=path) is True:
                directory_results = True
                break

        return prefix_results and citation_results and directory_results
    return dispatcher


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

        prefix_filters = []
        citation_filters = []
        directory_filters = []

        # We look at dispatching filters in the collection
        for filters in collection.xpath("./filters"):
            # We register prefix filters
            for prefix in filters.xpath("./id-starts-with/text()"):
                prefix_filters.append(
                    lambda collection, starts_with=prefix:
                        str(collection.id).startswith(starts_with)
                )

            # We register citation filters
            for citation_name in filters.xpath("./citation-contains/text()"):
                citation_filters.append(
                    lambda collection, citation_system=citation_name:
                        citation_contain_filter(collection, citation_system)
                )

            # We register path based filters
            for target_directory in filters.xpath("./folder/text()"):
                current_folder = relative_folder(configuration_file, target_directory)
                directory_filters.append(
                    lambda collection, path=None, starts_with=current_folder:
                        path.startswith(starts_with)
                )

        if prefix_filters or citation_filters or directory_filters:
            filters_to_register += [
                (
                    identifier,
                    collection_dispatcher_builder(
                        prefix_filters,
                        citation_filters,
                        directory_filters
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
