from rdflib import Namespace

from conftest import QUERY_DIR, evaluation_graph_entries


AMOR_BHV = Namespace("http://www.gsi.upm.es/ontologies/amor/models/bhv/ns#")
AMOR_EXAMPLES = Namespace("http://www.gsi.upm.es/ontologies/amor/examples#")
AMOR_MFT = Namespace("http://www.gsi.upm.es/ontologies/amor/models/mft/ns#")
BHV = Namespace("http://www.gsi.upm.es/ontologies/bhv/ns#")
MFT = Namespace("http://www.gsi.upm.es/ontologies/mft/ns#")

EXPECTED_GRAPH_ENTRIES = (
    "src/amor/amor.ttl",
    "src/bhv/bhv.ttl",
    "src/mft/mft.ttl",
    "src/amor/models/bhv/amor-bhv.ttl",
    "src/amor/models/mft/amor-mft.ttl",
    "src/amor/examples/amor-examples.ttl",
)
EXPECTED_QUERY_IDS = {
    "CQ-C1",
    "CQ-C2",
    "CQ-C3",
    "CQ-C4",
    "CQ-C5",
    "CQ-C6",
    "CQ-C7",
    "CQ-C8",
    "CQ-C9",
    "CQ-M1",
}


def run_query(graph, query_id: str) -> set[tuple]:
    query = (QUERY_DIR / f"{query_id}.rq").read_text(encoding="utf-8")
    return {tuple(row) for row in graph.query(query)}


def test_evaluation_uses_exactly_the_documented_graph_inputs() -> None:
    assert evaluation_graph_entries() == EXPECTED_GRAPH_ENTRIES


def test_all_ten_query_files_are_present() -> None:
    assert {path.stem for path in QUERY_DIR.glob("*.rq")} == EXPECTED_QUERY_IDS


def test_cq_c1_analysed_resource(evaluation_graph) -> None:
    assert run_query(evaluation_graph, "CQ-C1") == {
        (AMOR_EXAMPLES.analysis1, AMOR_EXAMPLES.news1),
        (AMOR_EXAMPLES.analysis2, AMOR_EXAMPLES.news1),
        (AMOR_EXAMPLES.analysis3, AMOR_EXAMPLES.news1),
        (AMOR_EXAMPLES.moralAnalysis21, AMOR_EXAMPLES.news1),
    }


def test_cq_c2_generated_annotations(evaluation_graph) -> None:
    assert run_query(evaluation_graph, "CQ-C2") == {
        (AMOR_EXAMPLES.analysis1, AMOR_EXAMPLES.annotation1),
        (AMOR_EXAMPLES.analysis2, AMOR_EXAMPLES.annotation2),
        (AMOR_EXAMPLES.analysis3, AMOR_EXAMPLES.annotation3),
        (AMOR_EXAMPLES.moralAnalysis21, AMOR_EXAMPLES.moralAnnotation23),
    }


def test_cq_c3_annotation_targets(evaluation_graph) -> None:
    assert run_query(evaluation_graph, "CQ-C3") == {
        (AMOR_EXAMPLES.annotation1, AMOR_EXAMPLES.news1),
        (AMOR_EXAMPLES.annotation2, AMOR_EXAMPLES.news1),
        (AMOR_EXAMPLES.annotation3, AMOR_EXAMPLES.news1),
        (AMOR_EXAMPLES.moralAnnotation23, AMOR_EXAMPLES.news1),
    }


def test_cq_c4_moral_models(evaluation_graph) -> None:
    assert run_query(evaluation_graph, "CQ-C4") == {
        (AMOR_EXAMPLES.analysis1, AMOR_MFT.MoralFoundationsTheoryModel),
        (AMOR_EXAMPLES.analysis2, AMOR_BHV["BHVModel-level3"]),
        (AMOR_EXAMPLES.analysis3, AMOR_MFT.MoralFoundationsTheoryModel),
        (AMOR_EXAMPLES.moralAnalysis21, AMOR_MFT.MoralFoundationsTheoryModel),
    }


def test_cq_c5_assigned_categories(evaluation_graph) -> None:
    assert run_query(evaluation_graph, "CQ-C5") == {
        (AMOR_EXAMPLES.annotation1, MFT.Liberty),
        (AMOR_EXAMPLES.annotation2, BHV.Conservation),
        (AMOR_EXAMPLES.annotation3, MFT.Care),
        (AMOR_EXAMPLES.moralAnnotation23, MFT.Authority),
    }


def test_cq_c6_model_memberships(evaluation_graph) -> None:
    bindings = run_query(evaluation_graph, "CQ-C6")
    models = {model for model, _ in bindings}
    assert models == {
        AMOR_BHV["BHVModel-level1"],
        AMOR_BHV["BHVModel-level2"],
        AMOR_BHV["BHVModel-level3"],
        AMOR_BHV["BHVModel-level4a"],
        AMOR_BHV["BHVModel-level4b"],
        AMOR_MFT.MoralFoundationsTheoryModel,
    }
    assert (AMOR_BHV["BHVModel-level3"], BHV.Conservation) in bindings
    assert (AMOR_MFT.MoralFoundationsTheoryModel, MFT.Fairness) in bindings


def test_cq_c7_responsible_agents(evaluation_graph) -> None:
    assert run_query(evaluation_graph, "CQ-C7") == {
        (AMOR_EXAMPLES.analysis1, AMOR_EXAMPLES.human1),
        (AMOR_EXAMPLES.analysis2, AMOR_EXAMPLES.human2),
        (AMOR_EXAMPLES.analysis3, AMOR_EXAMPLES.robot1),
        (AMOR_EXAMPLES.moralAnalysis21, AMOR_EXAMPLES.robot2),
    }


def test_cq_c8_confidence_scores(evaluation_graph) -> None:
    bindings = run_query(evaluation_graph, "CQ-C8")
    assert {(annotation, str(score)) for annotation, score in bindings} == {
        (AMOR_EXAMPLES.annotation1, "1.0"),
        (AMOR_EXAMPLES.annotation2, "0.8"),
        (AMOR_EXAMPLES.annotation3, "0.75"),
        (AMOR_EXAMPLES.moralAnnotation23, "0.75"),
    }


def test_cq_c9_machine_learning_models(evaluation_graph) -> None:
    assert run_query(evaluation_graph, "CQ-C9") == {
        (AMOR_EXAMPLES.analysis3, AMOR_EXAMPLES.model1),
        (AMOR_EXAMPLES.moralAnalysis21, AMOR_EXAMPLES.model4),
    }


def test_cq_m1_polarity_and_intensity(evaluation_graph) -> None:
    bindings = run_query(evaluation_graph, "CQ-M1")
    assert {
        (annotation, polarity, None if intensity is None else str(intensity))
        for annotation, polarity, intensity in bindings
    } == {
        (AMOR_EXAMPLES.annotation1, MFT.Virtue, None),
        (AMOR_EXAMPLES.annotation3, MFT.Vice, "-0.2"),
        (AMOR_EXAMPLES.moralAnnotation23, MFT.Virtue, "0.2"),
    }
