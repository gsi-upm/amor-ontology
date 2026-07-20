from __future__ import annotations

import argparse
from pathlib import Path

from rdflib import Graph, Namespace


def repair_if_invalid(turtle_path: Path) -> bool:
    try:
        Graph().parse(turtle_path, format="turtle")
        return False
    except Exception as turtle_error:
        rdfxml_path = turtle_path.with_suffix(".owl")
        if not rdfxml_path.is_file():
            raise RuntimeError(
                f"Cannot repair {turtle_path}: {rdfxml_path} is missing"
            ) from turtle_error
        graph = Graph().parse(rdfxml_path, format="xml")
        graph.bind("xml", Namespace("http://www.w3.org/XML/1998/namespace/"), replace=True)
        graph.serialize(turtle_path, format="turtle")
        serialized = turtle_path.read_text(encoding="utf-8").rstrip() + "\n"
        turtle_path.write_text(serialized, encoding="utf-8")
        Graph().parse(turtle_path, format="turtle")
        return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Repair invalid WIDOCO Turtle from its generated RDF/XML graph."
    )
    parser.add_argument("turtle", nargs="+", type=Path)
    args = parser.parse_args()

    for path in args.turtle:
        status = "repaired" if repair_if_invalid(path) else "valid"
        print(f"{path}: {status}")


if __name__ == "__main__":
    main()
