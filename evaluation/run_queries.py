from __future__ import annotations

import argparse
from pathlib import Path

from rdflib import Graph


ROOT = Path(__file__).resolve().parent.parent
EVALUATION = ROOT / "evaluation"
QUERY_DIR = EVALUATION / "competency-questions"
GRAPH_MANIFEST = EVALUATION / "graph-manifest.txt"


def graph_paths() -> tuple[Path, ...]:
    entries = (
        line.strip()
        for line in GRAPH_MANIFEST.read_text(encoding="utf-8").splitlines()
    )
    return tuple(ROOT / entry for entry in entries if entry and not entry.startswith("#"))


def load_evaluation_graph() -> Graph:
    graph = Graph()
    for path in graph_paths():
        graph.parse(path, format="turtle")
    return graph


def query_paths(selected: list[str]) -> list[Path]:
    if not selected:
        return sorted(QUERY_DIR.glob("CQ-*.rq"))
    paths = [QUERY_DIR / (name if name.endswith(".rq") else f"{name}.rq") for name in selected]
    missing = [str(path.relative_to(ROOT)) for path in paths if not path.is_file()]
    if missing:
        raise SystemExit(f"Unknown competency-question file(s): {', '.join(missing)}")
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description="Execute AMOR competency questions.")
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print row counts without individual bindings.",
    )
    parser.add_argument("query", nargs="*", help="CQ identifier(s), for example CQ-C1")
    args = parser.parse_args()

    graph = load_evaluation_graph()
    for path in query_paths(args.query):
        result = graph.query(path.read_text(encoding="utf-8"))
        print(f"{path.stem}\t{len(result)} row(s)")
        if args.summary:
            continue
        print("\t".join(str(variable) for variable in result.vars))
        for row in result:
            print("\t".join("" if value is None else str(value) for value in row))


if __name__ == "__main__":
    main()
