from nemo.advanced.nautilus import build_resolver
from ..base import BaseTest


class TestResolverBuilding(BaseTest):
    def test_normal_configuration(self):
        """ Test that the original config works correctly """
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
        """ Test that corpora works with only one collection """
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

    def test_double_folder_filter(self):
        """ Check that two folder filters are effective"""
        config = self.create_corpora(corpora=["example_corpora/aperire", "example_corpora/priapees"])
        config.add_collection("default", default=True, names={"eng": "Default Collection 1"})
        config.add_collection("folder1", names={"eng": "Folder 1"},
                              filter_folder=["example_corpora/aperire"])
        config.add_collection("folder2", names={"eng": "Folder 2"},
                              filter_folder=["example_corpora/priapees"])
        self.write_corpora_config(config)

        organizer, resolver, cache = build_resolver(self.corpora_xml)

        self.assertEqual(
            len(resolver.inventory.readableDescendants), 2,
            "There should be two texts"
        )
        self.assertEqual(
            (
                len(resolver.getMetadata("folder1").readableDescendants),
                len(resolver.getMetadata("folder2").readableDescendants)
            ),
            (1, 1),
            "There should be one text in folder1 and one in folder 2"
        )

        self.assertEqual(
            sorted(list(resolver.inventory.children.keys())),
            ["folder1", "folder2"],
            "Collections should have been created"
        )

    def test_multiple_identifiers_filter(self):
        """ Check that multiple identifer filters result in the correct output """
        config = self.create_corpora(corpora=[
            "example_corpora/aperire", "example_corpora/priapees", "example_corpora/inscriptions",
            "example_corpora/other"

        ])
        config.add_collection("default", default=True, names={"eng": "Default Collection 1"})
        config.add_collection("id1", names={"eng": "Id 1"},
                              filter_identifer=["urn:cts:aperire"])
        config.add_collection("id2", names={"eng": "Id 2"},
                              filter_identifer=["urn:cts:latinLit:phi1103", "urn:cts:pompei"])
        self.write_corpora_config(config)

        organizer, resolver, cache = build_resolver(self.corpora_xml)

        self.assertEqual(
            len(resolver.inventory.readableDescendants), 4,
            "There should be two texts"
        )
        self.assertEqual(
            (
                len(resolver.getMetadata("id1").readableDescendants),
                len(resolver.getMetadata("id2").readableDescendants),
                len(resolver.getMetadata("default").readableDescendants)
            ),
            (1, 2, 1),
            "There should be one text in the first collection, two in the second, and one in the default"
        )

        self.assertEqual(
            sorted(list(resolver.inventory.children.keys())),
            ["default", "id1", "id2"],
            "Collections should have been created"
        )
