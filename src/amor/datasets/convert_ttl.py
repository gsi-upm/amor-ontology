import json
from rdflib import Graph, RDF, Namespace

BASE_URL = 'http://www.github.com/gsi-upm/amor-experiment-api/#'
BASE = Namespace(BASE_URL)
EXAMPLE = '../../src/amor-dataset-example.json'
#TARGET = '../../src/amor-dataset-example.ttl'
PREFIX = "http://amor-graph.gsi.upm.es/ns#",

gc = Graph()
g = Graph(base=BASE)

with open("../../src/amor-experiment-context.jsonld") as f:
    context = json.load(f)

with open(EXAMPLE) as f:
    js = json.load(f)
    g.parse(data=js,
            format="json-ld",
            base=BASE_URL,
            context=context)

print(g.serialize(format='ttl'))
#g.serialize(TARGET, format='ttl')
#with open(TARGET) as f:
#    print(f.read())
