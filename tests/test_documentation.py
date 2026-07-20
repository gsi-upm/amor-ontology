from pathlib import Path

import pytest
from rdflib import Graph, Literal, Namespace, RDF, RDFS, SKOS, URIRef
from rdflib.namespace import DCTERMS, OWL

from conftest import ROOT


AMOR = Namespace("http://www.gsi.upm.es/ontologies/amor/ns#")
AMOR_EXAMPLES = Namespace("http://www.gsi.upm.es/ontologies/amor/examples#")
AMOR_MFT = Namespace("http://www.gsi.upm.es/ontologies/amor/models/mft/ns#")
BHV = Namespace("http://www.gsi.upm.es/ontologies/bhv/ns#")
MFT = Namespace("http://www.gsi.upm.es/ontologies/mft/ns#")
OA = Namespace("http://www.w3.org/ns/oa#")
LICENSE_IRI = URIRef("http://creativecommons.org/licenses/by/2.0/")

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
        URIRef("http://www.gsi.upm.es/ontologies/amor/ns/1.0.1"),
        URIRef("http://www.gsi.upm.es/ontologies/amor/ns/1.0.0"),
    ),
    (
        "doc/ontologies/bhv/ns/doc/ontology.ttl",
        URIRef("http://www.gsi.upm.es/ontologies/bhv/ns"),
        URIRef("http://www.gsi.upm.es/ontologies/bhv/ns/1.0.1"),
        URIRef("http://www.gsi.upm.es/ontologies/bhv/ns/1.0.0"),
    ),
    (
        "doc/ontologies/mft/ns/doc/ontology.ttl",
        URIRef("http://www.gsi.upm.es/ontologies/mft/ns"),
        URIRef("http://www.gsi.upm.es/ontologies/mft/ns/1.0.1"),
        URIRef("http://www.gsi.upm.es/ontologies/mft/ns/1.0.0"),
    ),
    (
        "doc/ontologies/amor/models/bhv/ns/doc/ontology.ttl",
        URIRef("http://www.gsi.upm.es/ontologies/amor/models/bhv/ns"),
        URIRef("http://www.gsi.upm.es/ontologies/amor/models/bhv/ns/1.0.1"),
        URIRef("http://www.gsi.upm.es/ontologies/amor/models/bhv/ns/1.0.0"),
    ),
    (
        "doc/ontologies/amor/models/mft/ns/doc/ontology.ttl",
        URIRef("http://www.gsi.upm.es/ontologies/amor/models/mft/ns"),
        URIRef("http://www.gsi.upm.es/ontologies/amor/models/mft/ns/1.0.1"),
        URIRef("http://www.gsi.upm.es/ontologies/amor/models/mft/ns/1.0.0"),
    ),
    (
        "doc/ontologies/amor/examples/doc/ontology.ttl",
        URIRef("http://www.gsi.upm.es/ontologies/amor/examples"),
        URIRef("http://www.gsi.upm.es/ontologies/amor/examples/1.0.1"),
        URIRef("http://www.gsi.upm.es/ontologies/amor/examples/1.0.0"),
    ),
)
RELEASE_CREATED_DATES = (
    "2024-02-10",
    "2024-03-15",
    "2024-03-15",
    "2024-03-15",
    "2024-03-15",
    "2024-02-10",
)


@pytest.mark.parametrize(
    "generated",
    GENERATED_RDF,
    ids=lambda path: str(path.relative_to(ROOT)),
)
def test_generated_rdf_representation_parses(generated: Path) -> None:
    Graph().parse(generated)


@pytest.mark.parametrize(
    ("relative_path", "ontology_iri", "version_iri", "prior_version_iri"),
    RELEASE_DOCUMENTATION,
)
@pytest.mark.parametrize("suffix", ("ttl", "owl", "jsonld"))
def test_generated_release_metadata(
    relative_path, ontology_iri, version_iri, prior_version_iri, suffix
) -> None:
    generated = (ROOT / relative_path).with_suffix(f".{suffix}")
    graph = Graph().parse(generated)
    assert (ontology_iri, RDF.type, OWL.Ontology) in graph
    assert (ontology_iri, OWL.versionIRI, version_iri) in graph
    assert (ontology_iri, OWL.priorVersion, prior_version_iri) in graph
    assert (ontology_iri, DCTERMS.license, LICENSE_IRI) in graph
    assert {str(value) for value in graph.objects(ontology_iri, OWL.versionInfo)} == {"1.0.1"}


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
    assert mft_html.count(
        "The polarity indicates whether an MFT moral-value category is expressed as a virtue or a vice."
    ) == 2
    assert (
        "The polarity intensity represents the direction and intensity of an MFT moral-value annotation on a scale from -1.0 (vice) to 1.0 (virtue)."
        in mft_html
    )
    assert "The polarity is represents" not in mft_html

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

    amor_intro = (
        ROOT / "doc/ontologies/amor/ns/doc/sections/introduction-en.html"
    ).read_text(encoding="utf-8")
    assert (
        "AMOR is an ontology for representing moral-value analyses and their associated annotations over textual resources."
        in amor_intro
    )
    assert "Axiomatic Moral Ontology for Reasoning" not in amor_intro
    assert "moral dilemmas" not in amor_intro
    assert "ethics education" not in amor_intro


@pytest.mark.parametrize(
    ("relative_path", "created"),
    [
        (entry[0].replace("ontology.ttl", "index-en.html"), created)
        for entry, created in zip(RELEASE_DOCUMENTATION, RELEASE_CREATED_DATES)
    ],
)
def test_human_readable_release_metadata(relative_path: str, created: str) -> None:
    html = (ROOT / relative_path).read_text(encoding="utf-8")
    assert '"version":"1.0.1"' in html
    assert f'"dateReleased":"{created}"' in html
    assert '"dateModified":"2026-07-20"' in html
    assert "<dt>Issued on:</dt>\n<dd>2026-07-20</dd>" in html
    assert "http://creativecommons.org/licenses/by/2.0/" in html
    assert "License-CC%20BY%202.0" in html
    assert "Ontology Specification Draft" not in html
    assert "Ontology Specification" in html


def test_normative_release_hash_manifest_matches_sources() -> None:
    import hashlib

    manifest = ROOT / "release/normative-artifacts.sha256"
    for line in manifest.read_text(encoding="utf-8").splitlines():
        expected, relative_path = line.split(maxsplit=1)
        content = (ROOT / relative_path).read_bytes()
        assert hashlib.sha256(content).hexdigest() == expected
