from pathlib import Path

import pytest
from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef
from rdflib.namespace import DCTERMS, OWL, XSD

from conftest import ROOT


LICENSE_IRI = URIRef("http://creativecommons.org/licenses/by/2.0/")
RELEASE_DATE = Literal("2026-07-20", datatype=XSD.date)
AMOR_MFT = Namespace("http://www.gsi.upm.es/ontologies/amor/models/mft/ns#")
RELEASE_ONTOLOGIES = (
    (
        "src/amor/amor.ttl",
        "http://www.gsi.upm.es/ontologies/amor/ns",
        "2024-02-10",
    ),
    (
        "src/bhv/bhv.ttl",
        "http://www.gsi.upm.es/ontologies/bhv/ns",
        "2024-03-15",
    ),
    (
        "src/mft/mft.ttl",
        "http://www.gsi.upm.es/ontologies/mft/ns",
        "2024-03-15",
    ),
    (
        "src/amor/models/bhv/amor-bhv.ttl",
        "http://www.gsi.upm.es/ontologies/amor/models/bhv/ns",
        "2024-03-15",
    ),
    (
        "src/amor/models/mft/amor-mft.ttl",
        "http://www.gsi.upm.es/ontologies/amor/models/mft/ns",
        "2024-03-15",
    ),
    (
        "src/amor/examples/amor-examples.ttl",
        "http://www.gsi.upm.es/ontologies/amor/examples",
        "2024-02-10",
    ),
)
WIDOCO_CONFIGS = (
    ("src/amor/widoco-amor-config.properties", "2024-02-10"),
    ("src/bhv/widoco-bhv-config.properties", "2024-03-15"),
    ("src/mft/widoco-mft-config.properties", "2024-03-15"),
    ("src/amor/models/bhv/widoco-amor-bhv-config.properties", "2024-03-15"),
    ("src/amor/models/mft/widoco-amor-mft-config.properties", "2024-03-15"),
    ("src/amor/examples/widoco-amor-examples-config.properties", "2024-02-10"),
)


@pytest.mark.parametrize(
    ("relative_path", "ontology_iri", "created"),
    RELEASE_ONTOLOGIES,
)
def test_normative_release_metadata(relative_path, ontology_iri, created) -> None:
    graph = Graph().parse(ROOT / relative_path, format="turtle")
    ontology = URIRef(ontology_iri)

    assert (ontology, RDF.type, OWL.Ontology) in graph
    assert set(graph.objects(ontology, OWL.versionInfo)) == {
        Literal("1.0.1", datatype=XSD.string)
    }
    assert set(graph.objects(ontology, OWL.versionIRI)) == {
        URIRef(f"{ontology_iri}/1.0.1")
    }
    assert set(graph.objects(ontology, OWL.priorVersion)) == {
        URIRef(f"{ontology_iri}/1.0.0")
    }
    assert set(graph.objects(ontology, DCTERMS.license)) == {LICENSE_IRI}
    assert set(graph.objects(ontology, DCTERMS.created)) == {
        Literal(created, datatype=XSD.date)
    }
    assert set(graph.objects(ontology, DCTERMS.issued)) == {RELEASE_DATE}
    assert set(graph.objects(ontology, DCTERMS.modified)) == {RELEASE_DATE}


@pytest.mark.parametrize(("relative_path", "created"), WIDOCO_CONFIGS)
def test_widoco_release_metadata(relative_path: str, created: str) -> None:
    properties = {}
    for line in (ROOT / relative_path).read_text(encoding="utf-8").splitlines():
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            properties[key] = value

    assert properties["dateCreated"] == created
    assert properties["dateIssued"] == "2026-07-20"
    assert properties["dateModified"] == "2026-07-20"
    assert properties["licenseURI"] == str(LICENSE_IRI)
    assert properties["licenseName"] == "CC BY 2.0"
    assert properties["ontologyRevisionNumber"] == "1.0.1"
    assert properties["thisVersionURI"].endswith("/1.0.1")
    assert properties["previousVersionURI"].endswith("/1.0.0")
    assert properties["status"] == "Ontology Specification"


def test_license_file_is_cc_by_2_0() -> None:
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert license_text.startswith("Creative Commons Attribution 2.0 Generic")
    assert "http://creativecommons.org/licenses/by/2.0/" in license_text
    assert "3. License Grant." in license_text
    assert "4. Restrictions." in license_text


def test_experiments_version_is_not_changed() -> None:
    graph = Graph().parse(
        ROOT / "src/amor/experiments/amor-experiments.ttl", format="turtle"
    )
    ontology = URIRef("http://www.gsi.upm.es/ontologies/amor/experiments/ns")
    assert set(graph.objects(ontology, OWL.versionInfo)) == {
        Literal("1.0.0", datatype=XSD.string)
    }
    assert set(graph.objects(ontology, OWL.versionIRI)) == {
        URIRef("http://www.gsi.upm.es/ontologies/amor/experiments/ns/1.0.0")
    }


def test_amor_mft_editorial_comments() -> None:
    graph = Graph().parse(
        ROOT / "src/amor/models/mft/amor-mft.ttl", format="turtle"
    )
    polarity_comment = Literal(
        "The polarity indicates whether an MFT moral-value category is expressed as a virtue or a vice.",
        lang="en",
    )
    intensity_comment = Literal(
        "The polarity intensity represents the direction and intensity of an MFT moral-value annotation on a scale from -1.0 (vice) to 1.0 (virtue).",
        lang="en",
    )
    assert set(graph.objects(AMOR_MFT.Polarity, RDFS.comment)) == {polarity_comment}
    assert set(graph.objects(AMOR_MFT.hasPolarity, RDFS.comment)) == {
        polarity_comment
    }
    assert set(graph.objects(AMOR_MFT.hasPolarityIntensity, RDFS.comment)) == {
        intensity_comment
    }


def test_amor_widoco_introduction_is_factual() -> None:
    config = (
        ROOT / "src/amor/widoco-amor-config.properties"
    ).read_text(encoding="utf-8")
    expected = (
        "introduction=<p>AMOR is an ontology for representing moral-value analyses "
        "and their associated annotations over textual resources.</p>"
    )
    assert expected in config
    assert "Axiomatic Moral Ontology for Reasoning" not in config
    assert "moral dilemmas" not in config
    assert "ethics education" not in config
