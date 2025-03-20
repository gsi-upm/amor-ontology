from rdflib import Graph

g = Graph()
g.parse("examples/amor-experiments-examples.json")
l = len(g)

g2 = Graph()
g2.parse('examples/amor-experiments-examples.ttl')
l2 = len(g2) - 11 # 11 triples are not in the original file (they are the definition of the Ontology: title, preferred prefix, etc.)

# g.serialize(destination="graph_from_ttl.ttl", format='ttl')
# g2.serialize(destination="graph_from_json.ttl", format='ttl')

print(l, l2)
assert l == l2
