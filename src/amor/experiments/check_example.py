from rdflib import Graph

g = Graph()

g.parse("examples/amor-experiments-examples.json")

print(g.serialize(format='ttl'))

l = len(g)

g2 = Graph()
g2.parse('examples/amor-experiments-examples.ttl')

l2 = len(g2)

print(l, l2)
assert l == l2
