import os.path
from .advanced.nautilus import build_resolver


organizer, resolver, cache = build_resolver(
    os.path.join(
        os.path.dirname(__file__),
        "../corpora.xml"
    )
)