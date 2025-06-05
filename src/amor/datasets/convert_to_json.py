from rdflib import Graph
from pyld import jsonld
import json
import sys

g = Graph()

if len(sys.argv) > 1:
    ttl_file = sys.argv[1]
else:
    raise ValueError("Please provide a TTL file as an argument.")

g.parse(ttl_file, format='turtle')


context_files = [
        '../../prefixes.jsonld',
        '../experiments/amor-experiment-context.jsonld'
        ]

contexts = []
for c in context_files:
    with open(c) as f:
        contexts.append(json.load(f))

js = json.loads(g.serialize(format='json-ld',
                            context=contexts))

frame = {
        "@context": contexts[1:], 
        "@type": "amor-exp:NewsDataset",
        "@embed": "@never",
        "amor-exp:hasNews": {
            "@embed": "@never"
            }
        }

dataset = jsonld.frame(js, frame=frame)

# If a dataset has a default language (marked with the schema:language property), strings in this language will be converted to json strings.
# Strings in other languages, and any string if there is no default, will be converted to an object: {"@value": "<STRING>", "@language": "<lang>"} or {"@value": "<STRING>"} if there is no language tag.
#default_language = dataset.get("schema:language", "und")
#contexts.append({"@language": default_language})

news_frame = {
        "@context": contexts,
        "@type": "schema:NewsArticle",
        "@embed": "@once",
        "annotations": {}
        }

def format_news(news):
    # String attributes that should be converted to json objects
    str_attrs = ['schema:articleBody', 'schema:headline']
    for attr in str_attrs:
        value = news[attr]
        if isinstance(value, str):
            news[attr] = {"@value": value}
    if 'annotations' not in news:
        return news
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
    return news

all_news = {news['@id']: format_news(news) for news in jsonld.frame(js, frame=news_frame)['@graph']}

parts = dataset["schema:hasPart"]

for k in parts.keys():
    parts[k] = all_news[k]


del dataset['@context']

dataset['@context'] = "http://www.gsi.upm.es/ontologies/amor/experiments/context.jsonld"

print(json.dumps(dataset, indent=2))
