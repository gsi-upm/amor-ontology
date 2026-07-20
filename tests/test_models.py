import pytest
from rdflib import Graph, Literal, Namespace, RDF, RDFS, SKOS, URIRef
from rdflib.namespace import OWL

from conftest import ROOT


AMOR = Namespace("http://www.gsi.upm.es/ontologies/amor/ns#")
AMOR_BHV = Namespace("http://www.gsi.upm.es/ontologies/amor/models/bhv/ns#")
AMOR_EXAMPLES = Namespace("http://www.gsi.upm.es/ontologies/amor/examples#")
AMOR_MFT = Namespace("http://www.gsi.upm.es/ontologies/amor/models/mft/ns#")
BHV = Namespace("http://www.gsi.upm.es/ontologies/bhv/ns#")
MFT = Namespace("http://www.gsi.upm.es/ontologies/mft/ns#")
OA = Namespace("http://www.w3.org/ns/oa#")


def load(*relative_paths: str) -> Graph:
    graph = Graph()
    for relative_path in relative_paths:
        graph.parse(ROOT / relative_path, format="turtle")
    return graph


def test_core_terms_used_by_the_examples_are_declared() -> None:
    graph = load("src/amor/amor.ttl")
    assert (AMOR.MoralValueAnalysis, RDF.type, OWL.Class) in graph
    assert (AMOR.MoralValueAnnotation, RDF.type, OWL.Class) in graph
    for property_iri in (
        AMOR.analysed,
        AMOR.hasMoralValueCategory,
        AMOR.usedMLModel,
        AMOR.usedMoralValueModel,
    ):
        assert (property_iri, RDF.type, OWL.ObjectProperty) in graph


def test_fairness_belongs_to_the_consolidated_mft_model() -> None:
    graph = load("src/amor/models/mft/amor-mft.ttl")
    assert (
        AMOR_MFT.MoralFoundationsTheoryModel,
        AMOR.hasMoralValueCategory,
        MFT.Fairness,
    ) in graph


@pytest.mark.parametrize(
    ("term", "english_label"),
    ((MFT.Virtue, "Virtue"), (MFT.Vice, "Vice")),
)
def test_mft_polarity_labels_match_their_iris(term, english_label) -> None:
    taxonomy = load("src/mft/mft.ttl")
    model = load("src/amor/models/mft/amor-mft.ttl")
    assert (term, SKOS.prefLabel, Literal(english_label, lang="en")) in taxonomy
    assert (term, RDFS.label, Literal(english_label, lang="en")) in model


def test_bhv_example_uses_the_published_ns_namespace() -> None:
    graph = load("src/amor/examples/amor-examples.ttl")
    assert (
        AMOR_EXAMPLES.annotation2,
        AMOR.hasMoralValueCategory,
        BHV.Conservation,
    ) in graph
    obsolete_iri = URIRef("http://www.gsi.upm.es/ontologies/bhv#Conservation")
    assert (AMOR_EXAMPLES.annotation2, AMOR.hasMoralValueCategory, obsolete_iri) not in graph


def test_moral_annotation_23_has_authority_and_only_the_news_target() -> None:
    graph = load("src/amor/examples/amor-examples.ttl")
    annotation = AMOR_EXAMPLES.moralAnnotation23
    assert (annotation, AMOR.hasMoralValueCategory, MFT.Authority) in graph
    assert set(graph.objects(annotation, OA.hasTarget)) == {AMOR_EXAMPLES.news1}


def test_bhv_and_mft_model_categories_are_typed() -> None:
    graph = load(
        "src/amor/amor.ttl",
        "src/amor/models/bhv/amor-bhv.ttl",
        "src/amor/models/mft/amor-mft.ttl",
    )
    assert (BHV.Conservation, RDF.type, AMOR.MoralValueCategory) in graph
    assert (MFT.Fairness, RDF.type, AMOR_MFT.MoralFoundation) in graph
    assert (AMOR_MFT.MoralFoundation, RDFS.subClassOf, AMOR.MoralValueCategory) in graph
