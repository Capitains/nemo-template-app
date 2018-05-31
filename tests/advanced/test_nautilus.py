from nemo.advanced.nautilus import build_resolver
from ..base import BaseTest


class TestResolverBuilding(BaseTest):

    def test_normal_configuration(self):
        organizer, resolver, cache = build_resolver(self.corpora_xml)

        general_collection = resolver.getMetadata("general")
        self.assertEqual(
            str(general_collection.get_label("fre")),
            "Collection générale",
            "Collections title should be available"
        )

        self.assertEqual(
            str(general_collection.get_label("eng")),
            "General Collection",
            "Collections title should be available"
        )
        self.assertEqual(
            sorted(list(resolver.inventory.children.keys())),
            ["general", "sources", "teaching"],
            "Collections should have been created"
        )
