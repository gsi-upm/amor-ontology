from pathlib import Path

import pytest
from rdflib import Graph, Literal, Namespace, RDF, RDFS, SKOS, URIRef
from rdflib.namespace import OWL

from conftest import ROOT


AMOR = Namespace("http://www.gsi.upm.es/ontologies/amor/ns#")
AMOR_EXAMPLES = Namespace("http://www.gsi.upm.es/ontologies/amor/examples#")
AMOR_MFT = Namespace("http://www.gsi.upm.es/ontologies/amor/models/mft/ns#")
BHV = Namespace("http://www.gsi.upm.es/ontologies/bhv/ns#")
MFT = Namespace("http://www.gsi.upm.es/ontologies/mft/ns#")
OA = Namespace("http://www.w3.org/ns/oa#")

GENERATED_RDF = tuple(
    sorted(
        path
        for path in (ROOT / "doc" / "ontologies").glob("**/doc/ontology.*")
        if path.suffix in {".ttl", ".owl", ".jsonld"}
    )
)
RELEASE_DOCUMENTATION = (
    (
        "doc/ontologies/amor/ns/doc/ontology.ttl",
        URIRef("http://www.gsi.upm.es/ontologies/amor/ns"),
        URIRef("http://www.gsi.upm.es/ontologies/amor/ns/1.0.0"),
    ),
    (
        "doc/ontologies/bhv/ns/doc/ontology.ttl",
        URIRef("http://www.gsi.upm.es/ontologies/bhv/ns"),
        URIRef("http://www.gsi.upm.es/ontologies/bhv/ns/1.0.0"),
    ),
    (
        "doc/ontologies/mft/ns/doc/ontology.ttl",
        URIRef("http://www.gsi.upm.es/ontologies/mft/ns"),
        URIRef("http://www.gsi.upm.es/ontologies/mft/ns/1.0.0"),
    ),
    (
        "doc/ontologies/amor/models/bhv/ns/doc/ontology.ttl",
        URIRef("http://www.gsi.upm.es/ontologies/amor/models/bhv/ns"),
        URIRef("http://www.gsi.upm.es/ontologies/amor/models/bhv/ns/1.0.0"),
    ),
    (
        "doc/ontologies/amor/models/mft/ns/doc/ontology.ttl",
        URIRef("http://www.gsi.upm.es/ontologies/amor/models/mft/ns"),
        URIRef("http://www.gsi.upm.es/ontologies/amor/models/mft/ns/1.0.0"),
    ),
    (
        "doc/ontologies/amor/examples/doc/ontology.ttl",
        URIRef("http://www.gsi.upm.es/ontologies/amor/examples"),
        URIRef("http://www.gsi.upm.es/ontologies/amor/examples/1.0.0"),
    ),
)


@pytest.mark.parametrize(
    "generated",
    GENERATED_RDF,
    ids=lambda path: str(path.relative_to(ROOT)),
)
def test_generated_rdf_representation_parses(generated: Path) -> None:
    Graph().parse(generated)


@pytest.mark.parametrize(
    ("relative_path", "ontology_iri", "version_iri"),
    RELEASE_DOCUMENTATION,
)
def test_generated_release_metadata(relative_path, ontology_iri, version_iri) -> None:
    graph = Graph().parse(ROOT / relative_path, format="turtle")
    assert (ontology_iri, RDF.type, OWL.Ontology) in graph
    assert (ontology_iri, OWL.versionIRI, version_iri) in graph
    assert {str(value) for value in graph.objects(ontology_iri, OWL.versionInfo)} == {"1.0.0"}


def test_generated_mft_documentation_contains_corrected_model_terms() -> None:
    model = Graph().parse(
        ROOT / "doc/ontologies/amor/models/mft/ns/doc/ontology.ttl",
        format="turtle",
    )
    taxonomy = Graph().parse(
        ROOT / "doc/ontologies/mft/ns/doc/ontology.ttl",
        format="turtle",
    )
    assert (
        AMOR_MFT.MoralFoundationsTheoryModel,
        AMOR.hasMoralValueCategory,
        MFT.Fairness,
    ) in model
    assert (MFT.Virtue, RDFS.label, Literal("Virtue", lang="en")) in model
    assert (MFT.Vice, RDFS.label, Literal("Vice", lang="en")) in model
    assert (MFT.Virtue, SKOS.prefLabel, Literal("Virtue", lang="en")) in taxonomy
    assert (MFT.Vice, SKOS.prefLabel, Literal("Vice", lang="en")) in taxonomy


def test_generated_example_documentation_contains_corrected_bindings() -> None:
    graph = Graph().parse(
        ROOT / "doc/ontologies/amor/examples/doc/ontology.ttl",
        format="turtle",
    )
    assert (
        AMOR_EXAMPLES.annotation2,
        AMOR.hasMoralValueCategory,
        BHV.Conservation,
    ) in graph
    annotation = AMOR_EXAMPLES.moralAnnotation23
    assert (annotation, AMOR.hasMoralValueCategory, MFT.Authority) in graph
    assert set(graph.objects(annotation, OA.hasTarget)) == {AMOR_EXAMPLES.news1}


def test_human_readable_documentation_reflects_corrections() -> None:
    mft_html = (
        ROOT
        / "doc/ontologies/amor/models/mft/ns/doc/sections/crossref-en.html"
    ).read_text(encoding="utf-8")
    assert "consolidated category set from Moral Foundations Theory" in mft_html
    assert "ontologies/mft/ns#Fairness" in mft_html
    assert ">Vice<" in mft_html
    assert ">Virtue<" in mft_html

    examples_html = (
        ROOT / "doc/ontologies/amor/examples/doc/sections/crossref-en.html"
    ).read_text(encoding="utf-8")
    annotation_section = examples_html.split('id="moralAnnotation23"', 1)[1].split(
        '<div class="entity"', 1
    )[0]
    assert "ontologies/mft/ns#Authority" in annotation_section
    assert "www.w3.org/ns/oa#hasTarget" in annotation_section
    assert 'href="#news1"' in annotation_section
    assert "ontologies/bhv/ns#Conservation" in examples_html
    assert "ontologies/bhv#Conservation" not in examples_html


def test_normative_release_hash_manifest_matches_sources() -> None:
    import hashlib

    manifest = ROOT / "release/normative-artifacts.sha256"
    for line in manifest.read_text(encoding="utf-8").splitlines():
        expected, relative_path = line.split(maxsplit=1)
        content = (ROOT / relative_path).read_bytes()
        assert hashlib.sha256(content).hexdigest() == expected
