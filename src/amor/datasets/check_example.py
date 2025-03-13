import sys
import rdflib
g = rdflib.Graph()
g.parse(sys.argv[1])
print(g.serialize(format='ttl'))
