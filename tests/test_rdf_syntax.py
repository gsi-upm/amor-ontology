from pathlib import Path

import pytest
from rdflib import Graph

from conftest import ROOT


TURTLE_SOURCES = tuple(sorted((ROOT / "src").rglob("*.ttl")))


@pytest.mark.parametrize(
    "source",
    TURTLE_SOURCES,
    ids=lambda source: str(source.relative_to(ROOT)),
)
def test_normative_turtle_source_parses(source: Path) -> None:
    Graph().parse(source, format="turtle")
