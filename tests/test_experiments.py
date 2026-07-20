from rdflib import Graph, Namespace, RDF, RDFS

from conftest import ROOT


AMOR_EXP = Namespace("http://www.gsi.upm.es/ontologies/amor/experiments/ns#")
AMOR_EXP_EXAMPLES = Namespace("http://www.gsi.upm.es/ontologies/amor/experiments/examples#")
AMOR_GRAPH = Namespace("http://amor-graph.gsi.upm.es/ns#")


def experiment_graph() -> Graph:
    graph = Graph()
    graph.parse(ROOT / "src/amor/experiments/amor-experiments.ttl", format="turtle")
    graph.parse(
        ROOT / "src/amor/experiments/examples/amor-experiments-examples.ttl",
        format="turtle",
    )
    return graph


def test_recommendation_criteria_use_the_current_class() -> None:
    graph = experiment_graph()
    criteria = set(graph.subjects(RDF.type, AMOR_EXP.RecommendationCriterion))
    assert criteria == {
        AMOR_EXP.MoralSimilarity,
        AMOR_EXP.MoralDissimilarity,
        AMOR_EXP.EmotionSimilarity,
        AMOR_EXP.EmotionDissimilarity,
        AMOR_EXP.SentimentSimilarity,
        AMOR_EXP.SentimentDisimilarity,
        AMOR_EXP.EntitySimilarity,
    }


def test_experiment_uses_the_current_dataset_property() -> None:
    graph = experiment_graph()
    experiment = AMOR_EXP_EXAMPLES.experiment1
    assert (experiment, AMOR_EXP.usesDataset, AMOR_GRAPH.dataset1) in graph
    assert (AMOR_EXP.usesDataset, RDFS.subPropertyOf, AMOR_EXP.hasParameter) in graph


def test_experiment_parameters_follow_explicit_subproperty_paths() -> None:
    graph = experiment_graph()
    results = graph.query(
        """
        PREFIX amor-exp: <http://www.gsi.upm.es/ontologies/amor/experiments/ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?predicate ?parameter
        WHERE {
          ?experiment a amor-exp:Experiment ;
            ?predicate ?parameter .
          ?predicate rdfs:subPropertyOf* amor-exp:hasParameter .
        }
        """
    )
    bindings = {tuple(row) for row in results}
    assert (AMOR_EXP.usesDataset, AMOR_GRAPH.dataset1) in bindings
    assert len(bindings) > 1
