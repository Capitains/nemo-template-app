import os.path
from .advanced.nautilus import build_resolver
from .advanced.chunker import build_chunker


organizer, resolver, cache = build_resolver(
    os.path.join(
        os.path.dirname(__file__),
        "../corpora.xml"
    )
)

chunker = build_chunker(
    os.path.join(
        os.path.dirname(__file__),
        "../nemo.xml"
    )
)
