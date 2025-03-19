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
        '../experiments/amor-experiment-context-properties.jsonld'
        ]


context = {}
for c in context_files:
    with open(c) as f:
        context.update(json.load(f))

merged_context = '../experiments/amor-experiment-context.jsonld'

with open(merged_context, 'w') as f:
    json.dump(context, f, indent=2)

#print(g.serialize(format='ttl'))
js = json.loads(g.serialize(format='json-ld',
                            context=context))

#print(json.dumps(js, indent=2))
#sys.exit(1)
exp_frame = {
        "@context": context,
        "@type": "amor-exp:Experiment",
        "@embed": "@always" #,
        # "amor-exp:usesDataset": {
        #     "@embed": "@never",
        #     }
        }

js = jsonld.frame(js, frame=exp_frame)

del js['@context']

print(json.dumps(js, indent=2))

#del context["parts"]["@container"]
#with open('frame.json') as f:
#    frame = json.load(f)
#frame["@context"] = [
#        context,
#        {"@base": "http://www.github.com/gsi-upm/amor-experiment-api#"}]
