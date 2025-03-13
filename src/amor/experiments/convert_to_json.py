from rdflib import Graph
from pyld import jsonld
import json
import sys

g = Graph()

example = './examples/amor-experiments-examples.ttl'
if len(sys.argv) > 1:
    example = sys.argv[1]

g.parse(example, format='turtle')
#g.parse('./examples/dataset-example.ttl', format='turtle')


#with open('../../prefixes.jsonld') as f:
context_files = [
        '../../prefixes.jsonld',
        '../experiments/amor-experiment-context.jsonld'
        ]

contexts = []
for c in context_files:
    with open(c) as f:
        contexts.append(json.load(f))

#print(g.serialize(format='ttl'))
js = json.loads(g.serialize(format='json-ld',
                            context=contexts))

#print(json.dumps(js, indent=2))
#sys.exit(1)
exp_frame = {
        "@context": contexts,
        "@type": "amor-exp:Experiment",
        "@embed": "@always" #,
        # "amor-exp:usesDataset": {
        #     "@embed": "@never",
        #     }
        }

js = jsonld.frame(js, frame=exp_frame)

print(json.dumps(js, indent=2))

#del context["parts"]["@container"]
#with open('frame.json') as f:
#    frame = json.load(f)
#frame["@context"] = [
#        context,
#        {"@base": "http://www.github.com/gsi-upm/amor-experiment-api#"}]
