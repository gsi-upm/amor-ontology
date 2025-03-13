import json
import unittest 
import sys
import pathlib
from collections import defaultdict

from rdflib import Graph, RDF, Namespace

ROOT = pathlib.Path(__file__).parent.parent.resolve()
BASE = Namespace('http://www.gsi.upm.es/ontologies/amor/experiments/ns#')
AMOR = ROOT / 'src' / 'amor' 

with open(ROOT / 'src' / 'prefixes.sparql') as f:
    PRELUDE = f.read()


def query(g: Graph, q: str, prelude=PRELUDE):
    return list(g.query(PRELUDE + '\n' + q))


def load_file(src, format='ttl', graph=None, **kwargs):
    '''
    Generate a new graph with the content of the file. Optionally include
    content from an existing graph.
    '''
    graph = graph.copy() or Graph()
    graph.parse(src, format=format, **kwargs)
    return graph
  

class SemanticTest(object):
    def setUp(self):
        '''Parse all the necessary files'''
        gc = Graph()
        for owl in [
                AMOR / 'experiments' / 'amor-experiments.ttl',
                ]:
            gc.parse(owl)

        self.criteria = list(gc.subjects(RDF.type, BASE['RecommendationStrategy']))
        self.assertGreater(len(self.criteria), 1)

        self.g = Graph()


class JSONTest(SemanticTest, unittest.TestCase):

    def setUp(self):
        super().setUp()

        context_file = AMOR / 'experiments' / 'amor-experiment-context.jsonld'

        with open(context_file) as f:
            self.context = json.load(f)



@unittest.skip
class DatasetJSONExamplesTest(JSONTest):
    '''This test should be adapted to the new JSON structure'''
    def setUp(self):
        super().setUp()
        self.example_file = AMOR / 'datasets' / 'examples' / 'dataset-example.json'
        with open(self.example_file) as f:
            self.js = f.read()
            self.json = json.loads(self.js)
            self.g.parse(data=self.js,
                         format="json-ld",
                         context=self.context)

    def test_basic(self): 
        '''There should be  at least one dataset, with a main entity of type schema:NewsArticle'''
        total_news = query(self.g, '''
        SELECT (COUNT(?uri) as ?total)
        WHERE {
                ?uri a schema:NewsArticle .
                }
                ''')[0]['total']

        main_news = query(self.g, '''
        SELECT (COUNT(?news) as ?total)
        WHERE {
                ?dataset schema:mainEntity ?news .
                ?news a schema:NewsArticle .
                }
                ''')[0]['total']

        self.assertEqual(2, int(total_news), f"The dataset should contain 2 news articles. It contains {total_news}")
        self.assertEqual(1, int(main_news), f"The dataset should contain 1 main news article. It contains {main_news}")


    def test_filter_recommendations_json(self):
        '''
        Each main news article in the dataset example should have a recommendation.
        '''
        assert self.json['main_news']
        for uri in self.json['main_news']:
            news = self.json['all_news'][uri]
            recommendations = defaultdict(list)
            for recommendation in news['recommendations']:
                for criterion in self.criteria:
                    if recommendation['reviewAspect'].rsplit(':')[1] == criterion.rsplit('#')[1]:
                        recommendations[criterion].append(recommendation)
                        break
                else:
                    print(self.criteria)
                    self.fail(f"This recommendation does not have a known criterion: {recommendation}")

            self.assertTrue(recommendations)
            for criterion, rec in recommendations.items():
                self.assertEqual(1, len(rec), f"There should only be one recommendation for {criterion}")

    def test_filter_recommendations_rdf(self):
        '''
        The graph that results from loading the JSON-LD dataset should contain a news article, with
        a recommendation.
        '''
        res = query(self.g, '''
                SELECT ?news ?rec ?criterion
                WHERE {
                    ?dataset schema:mainEntity ?news.
                    OPTIONAL {
                        ?news a schema:NewsArticle .
                    }
                    OPTIONAL {
                          ?news schema:subjectOf ?rec .
                    }
                    OPTIONAL {
                        ?rec schema:reviewAspect ?criterion .
                    }
                }

        ''')
        self.assertTrue(res)
        for (news, rec, criterion) in res:
            self.assertTrue(news)
            self.assertTrue(rec)
            self.assertIn(criterion, self.criteria)
  

class GenericExperimentsTest(SemanticTest):
    '''
    Definition of the tests to run on the representation of experiments in
    any of the available formats. The tests for each format will be defined in
    separate subclasses.
    '''

    def test1Experiment(self):
        '''The examples should include at least one experiment'''
        res = query(self.g, '''
                SELECT ?exp
                WHERE {
                    ?exp a amor-exp:Experiment .
                }

        ''')
        self.assertTrue(res)

    def testExperimentParameters(self):
        '''The experiments in the examples should all have parameters'''
        res = query(self.g, '''
                SELECT ?exp ?param
                WHERE {
                    ?exp a amor-exp:Experiment .
                    OPTIONAL {
                         ?exp amor-exp:hasParameter ?param .
                     }

                }
        ''')
        for (exp, param) in res:
            self.assertTrue(exp)
            self.assertTrue(param, f"Experiment {exp} does not have any params")

    def testExperimentDataset(self):
        '''At least one experiment should use a news dataset'''
        res = query(self.g, '''
                SELECT ?exp ?dataset
                WHERE {
                    ?exp a amor-exp:Experiment ;
                         amor-exp:hasParameter [
                             amor-exp:hasDataset ?dataset 
                         ] .

                }
        ''')
        self.assertTrue(res, 'At least one experiment should be linked to a dataset')

    @unittest.skip
    def testExperimentsDatasetRequired(self):
        '''All experiments should use a news dataset'''
        res = query(self.g, '''
                SELECT ?exp ?dataset
                WHERE {
                    ?exp a amor-exp:Experiment ;
                         amor-exp:hasDataset ?dataset .

                }
        ''')
        for (exp, dataset) in res:
            self.assertTrue(exp)
            self.assertTrue(dataset, f"Experiment {exp} is not linked to a dataset")


class ExperimentsTest(GenericExperimentsTest, unittest.TestCase):
    '''Test of the TTL representation of datasets'''
    def setUp(self):
        super().setUp()
        for example in [
                AMOR / 'datasets' / 'examples' / 'dataset-example.ttl',
                AMOR / 'datasets' / 'examples' / 'news-example.ttl',
                AMOR / 'experiments' / 'examples' / 'amor-experiments-examples.ttl',
                ]:
            self.g.parse(example)


class ExperimentsJSONTest(GenericExperimentsTest, unittest.TestCase):
    '''Test of the JSON-LD representation of datasets'''
    def setUp(self):
        super().setUp()
        for example in [
                AMOR / 'datasets' / 'examples' / 'dataset-example.json',
                AMOR / 'experiments' / 'examples' / 'amor-experiments-examples.ttl',
                ]:
            self.g.parse(example)


if __name__ == '__main__': 
    unittest.main()
