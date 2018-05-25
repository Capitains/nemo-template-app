import re
from lxml import etree
from collections import namedtuple

from flask_nemo.chunker import level_grouper

RegExpChunker = namedtuple(
    "RegExpChunker",
    ["regexp", "config"]
)
CitationChunker = namedtuple(
    "CitationChunker",
    ["system", "config"]
)
ChunkerConfig = namedtuple(
    "ChunkerConfig",
    ["level", "name_template", "group_by"]
)


def get_citation_scheme(text):
    # We create an empty list to store citations level names
    citation_types = []
    #  We loop over the citation scheme of the Text
    for citation in text.citation:
        # We append the name of the citation level in the list we created
        citation_types.append(citation.name)
    # At this point, we just return
    return citation_types


def build_chunker(configuration_file):
    """ XML configuration file

    :param xml:
    :return:
    """

    identifier_regexps = [
        RegExpChunker(
            re.compile(regexp_node.text),
            ChunkerConfig(
                int(regexp_node.get("level")),
                regexp_node.get("level-name", "{passage}"),
                int(regexp_node.get("group-by", 1))
            )
        )
        for regexp_node in configuration_file.xpath(".//identifier-regexp")
    ]
    citation_sytems = [
        CitationChunker(
            citation_node.text,
            ChunkerConfig(
                int(citation_node.get("level")),
                citation_node.get("level-name", "{passage}"),
                int(citation_node.get("group-by", 1))
            )
        )
        for citation_node in configuration_file.xpath(".//citation-system")
    ]
    hardcoded_systems = {
        citation_node.get("identifier"): [
            (
                ref_node.get(
                    "id",
                    "{}-{}".format(
                        ref_node.get("start"),
                        ref_node.get("end")
                    )
                ),
                ref_node.text
            )
            for ref_node in citation_node.xpath("./ref")
        ]
        for citation_node in configuration_file.xpath(".//hardcoded")
    }

    def chunker(text, getreffs):
        # We build a the citation type
        citation_types = get_citation_scheme(text)
        identifier = str(text.id)
        config = ChunkerConfig(1, "{passage}", 1)
        changed_config = False

        if identifier in hardcoded_systems:
            return hardcoded_systems[identifier]

        for identifier_regexp in identifier_regexps:
            if identifier_regexp.regexp.match(identifier):
                config = identifier_regexp.config
                changed_config = True

        if not changed_config:
            for citation_sytem in citation_sytems:
                if citation_sytem.system.split(",") == citation_types:
                    config = citation_sytem.config

        if config.group_by > 1:
            reffs = [
                r
                for r, _ in level_grouper(text, getreffs, config.level, config.group_by)
             ]
        else:
            reffs = getreffs(level=config.level)

        reffs = [
            (
                reff,
                config.name_template.format(passage=reff)
            )
            for reff in reffs
        ]

        return reffs

    return chunker
