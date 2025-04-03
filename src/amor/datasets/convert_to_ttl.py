import json
from rdflib import Graph, RDF, Namespace
from rdflib import Graph
import json
import sys

g = Graph()

if len(sys.argv) > 1:
    json_file = sys.argv[1]
else:
    raise ValueError("Please provide a JSON-LD file as an argument.")

with open(json_file) as f:
    js = json.load(f)
    g.parse(data=js,
            format="json-ld")

print(g.serialize(format='ttl'))
#g.serialize(TARGET, format='ttl')
#with open(TARGET) as f:
#    print(f.read())
