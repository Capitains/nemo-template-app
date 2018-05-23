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
    starts_with_filters = []

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

        starts_with_filters += [
            (
                identifier,
                lambda collection, path=None, **kwargs: str(collection.id).startswith(prefix)
            )
            for prefix in collection.xpath("./id-starts-with/text()")
        ]

    # Create the dispatcher
    organizer = CollectionDispatcher(
        general_collection,
        default_inventory_name=default_collection
    )

    for destination_collection, anonymous_dispatching_function in starts_with_filters:
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
