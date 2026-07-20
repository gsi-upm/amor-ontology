from pathlib import Path

import pytest
from rdflib import Graph


ROOT = Path(__file__).resolve().parent.parent
EVALUATION_DIR = ROOT / "evaluation"
QUERY_DIR = EVALUATION_DIR / "competency-questions"
GRAPH_MANIFEST = EVALUATION_DIR / "graph-manifest.txt"


def evaluation_graph_entries() -> tuple[str, ...]:
    entries = (
        line.strip()
        for line in GRAPH_MANIFEST.read_text(encoding="utf-8").splitlines()
    )
    return tuple(entry for entry in entries if entry and not entry.startswith("#"))


@pytest.fixture(scope="session")
def evaluation_graph() -> Graph:
    graph = Graph()
    for entry in evaluation_graph_entries():
        graph.parse(ROOT / entry, format="turtle")
    return graph
