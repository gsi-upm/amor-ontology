from rdflib import Graph
from pyld import jsonld
import json
import sys

g = Graph()

example = None

if len(sys.argv) > 1:
    example = sys.argv[1]
else:
    raise ValueError("Please provide an example file as an argument.")

g.parse(example, format='json-ld')
print(g.serialize(format='turtle'))