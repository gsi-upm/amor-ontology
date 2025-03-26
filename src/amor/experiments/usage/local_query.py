from rdflib import Graph
import sys
import os

from remote_query import ENDPOINT, PREFIXES

g = Graph()

g.parse('local/graph.ttl')

# We used this to generate the local graph
#g.parse('../../datasets/examples/news-small-example.ttl')
#g.parse('../../experiments/examples/amor-experiments-examples.ttl')
#print(g.serialize(format='ttl'))

def local_query(q):
    query = PREFIXES + q
    if os.environ.get("DEBUG"):
        print(query)
    resp = g.query(query)
    try:
        return list(k.asdict() for k in resp)
    # For describe
    except AttributeError:
        return resp.graph.serialize(format='ttl')

if __name__ == '__main__':
    fpath = sys.argv[1]
    with open(fpath) as f:
        query = PREFIXES + f.read()
        print(local_query(query))
