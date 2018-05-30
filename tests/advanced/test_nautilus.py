from nemo.advanced.nautilus import build_resolver
from ..base import BaseTest


class TestResolverBuilding(BaseTest):

    def test_normal_configuration(self):
        organizer, resolver, cache = build_resolver(self.corpora_xml)
