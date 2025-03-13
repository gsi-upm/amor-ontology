from rdflib import Graph
from pyld import jsonld
import json
import sys

g = Graph()

example = './examples/news-example.ttl'
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
news_frame = {
        "@context": contexts,
        "@type": "schema:NewsArticle",
        "@embed": "@once",
        "annotations": {}
        }

all_news = {news['@id']: news for news in jsonld.frame(js, frame=news_frame)['@graph']}


for news in all_news.values():
#    print(news)
    if 'annotations' not in news:
        continue
    annotations = news.pop("annotations")
    indexed = {}
    for ann in annotations:
        types = ann["@type"]
        if not isinstance(types, list):
            types = [types]
        for k in types:
            if k not in indexed:
                indexed[k] = []
            if k == 'amor:Recommendation':
                ann['oa:hasBody'] = ann['oa:hasBody']['@id']
            indexed[k].append(ann)
    news["annotations"] = indexed


frame = {
        "@context": contexts[1:], 
        "@type": "amor-exp:NewsDataset",
         "@embed": "@never",
         "amor-exp:hasNews": {
             "@embed": "@never"
             }
         }

js = jsonld.frame(js, frame=frame)

parts = js["schema:hasPart"]

for k in parts.keys():
    parts[k] = all_news[k]
#js["schema:hasPart"] = all_news
#del js['@context']
#
#print(json.dumps(js, indent=2))
print(json.dumps(js, indent=2))

#del context["parts"]["@container"]
#with open('frame.json') as f:
#    frame = json.load(f)
#frame["@context"] = [
#        context,
#        {"@base": "http://www.github.com/gsi-upm/amor-experiment-api#"}]
