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

        self.assertEqual(
            len(resolver.inventory),
            4,
            "There should be four texts"
        )

    def test_single_corpora(self):
        config = self.create_corpora(corpora=["example_corpora/aperire"])
        config.add_collection("default", default=True, names={"eng": "Default Collection 1"})
        self.write_corpora_config(config)

        organizer, resolver, cache = build_resolver(self.corpora_xml)

        self.assertEqual(
            str(resolver.getMetadata("default").get_label("eng")),
            "Default Collection 1",
            "Collection title should be available"
        )
        self.assertEqual(
            sorted(list(resolver.inventory.children.keys())),
            ["default"],
            "Collections should have been created"
        )

        self.assertEqual(len(resolver.inventory), 1, "There should be four texts")
