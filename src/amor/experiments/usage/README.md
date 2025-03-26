# Simple examples of edge-cloud collaboration for the experiments

## Running the examples

All the queries in this document are also provided as a separate text file (e.g., [news_all.sparql](./remote/news_all.sparql)).
You can run remote queries with the `remote_query.py` and `local_query` scripts, like so:

```
> uv run remote_query.py remote/news_one.sparql

PREFIX amor:               <http://www.gsi.upm.es/ontologies/amor/ns#>
PREFIX amor-bhv:           <http://www.gsi.upm.es/ontologies/amor/models/bhv/ns#>
PREFIX amor-data:          <http://www.gsi.upm.es/ontologies/amor/datasets/ns#>
...

amor-data:news_1effdbcd-e6b9-6c0b-850a-7f017c762070
        rdf:type               schema1:NewsArticle;
        schema1:articleBody    "El Gobierno de Pedro ..."
```


> [!WARNING]  
> The SPARQL endpoint in this repository now requires a username and password.
> The local queries that make use a remote service will not work propertly.
> Feel free to modify the examples to include HTTP authentication.
> In the meantime, we provide a `local_query_remote` set of queries that simulate these queries through a SPARQL query to more than one graph.
> The results are equivalent.

## Prefixes

The following prefixes are assumed in all the sparql examples:

```sparql
prefix amor-bhv: <http://www.gsi.upm.es/ontologies/amor/models/bhv/ns#>
prefix amor-data: <http://www.gsi.upm.es/ontologies/amor/datasets/ns#>
prefix amor-data-examples: <http://www.gsi.upm.es/ontologies/amor/datasets/examples#>
prefix amor-exp: <http://www.gsi.upm.es/ontologies/amor/experiments/ns#>
prefix amor-graph: <http://amor-graph.gsi.upm.es/ns#>
prefix amor: <http://www.gsi.upm.es/ontologies/amor/ns#>
prefix amor-mft: <http://www.gsi.upm.es/ontologies/amor/models/mft/ns#>
prefix bhv: <http://www.gsi.upm.es/ontologies/bhv/ns#>
prefix dc: <http://purl.org/dc/terms/>
prefix marl: <http://www.gsi.upm.es/ontologies/marl/ns#>
prefix mft: <http://www.gsi.upm.es/ontologies/mft/ns#>
prefix mls: <http://www.w3.org/ns/mls#>
prefix nif: <http://persistence.uni-leipzig.org/nlp2rdf/ontologies/nif-core#>
prefix onyx: <http://www.gsi.upm.es/ontologies/onyx/ns#>
prefix oro: <http://kb.openrobots.org#>
prefix owl: <http://www.w3.org/2002/07/owl#>
prefix prov: <http://www.w3.org/ns/prov#>
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
prefix schema: <http://schema.org/>
prefix sebb: <http://www.gsi.upm.es/ontologies/sebb/ns#>
prefix skos: <http://www.w3.org/2004/02/skos/core#>
prefix vann: <http://purl.org/vocab/vann/>
prefix wnaffect: <http://gsi.upm.es/ontologies/wnaffect/ns#>
prefix xsd: <http://www.w3.org/2001/XMLSchema#>
prefix oa: <http://www.w3.org/ns/oa#>
```

## Federated queries

These queries should be run from a local graph.
In particular, we have tested the queries with the graph in `local/graph.ttl`.

To run these queries, you can use the `local_query.py` script.

### News recommendations based on adaptation strategy

This query uses the content adaptation strategy for every experiment in the local graph to fetch recommendations for every news article in the dataset used in the experiment.

```sparql local/recommendations_criterion.sparql

SELECT ?experiment ?news ?recommendation
WHERE {      
	?experiment amor-exp:hasContentAdaptationStrategy ?strategy ;
		    amor-exp:usesDataset [
			amor:hasNews ?news 
	    ] .

	SERVICE <https://amor-graph.gsi.upm.es/news/> {
		?strategy amor-exp:usesRecommendationCriterion ?criterion .

		?annotation a amor:Recommendation ;
			    amor-exp:hasRecommendationCriterion ?criterion ;
			    oa:hasTarget ?news ;
			    oa:hasBody ?recommendation .
	}
}
LIMIT 10
```

### News recommendations based on user preferences

The local graph should include information about the preferences of a user.
Based on that, this query fetches all recommendations for these news articles from the remote graph.


```sparql local/recommendations_preferred_news.sparql
SELECT ?preference ?recommendation
WHERE {      
	ex-exp:experiment1 amor-exp:hasExperimentSubject [
		amor-exp:hasPreferredContent ?preference
	] .
	OPTIONAL {
		SERVICE <https://amor-graph.gsi.upm.es/news/> {
			[] a amor:Recommendation ;
					oa:hasTarget ?preference ;
					oa:hasBody ?recommendation .
		}
	}
}
LIMIT 10
```

### News matching emotion

In this example, we construct a new set of (local) recommendations based on the emotion shown by the experiment subject and the emotion annotation of news in the remote news knowledge graph.


```sparql local/recommendations_matching_emotion.sparql
CONSTRUCT {
	?subject amor-exp:hasPreferredContent ?recommendation .
	?recommendation ?prop ?value .
}
# Alternatively
#SELECT ?subject ?cat ?recommendation ?prop ?value
WHERE {      
	#This would be the experiment in process
	ex-exp:experiment1 amor-exp:hasExperimentSubject ?subject .
	?subject onyx:hasEmotionSet [
			onyx:hasEmotion [
				onyx:hasEmotionCategory ?cat 
			]
		]
	.
	SERVICE <https://amor-graph.gsi.upm.es/news/> {
		?recommendation a schema:NewsArticle .
		?annotation a amor:EmotionAnnotation ;
			    onyx:hasEmotion [
				onyx:hasEmotionCategory ?cat
			    ] ;
			    oa:hasTarget ?recommendation .
		?recommendation ?prop ?value
	}
}
LIMIT 10
```

## Simple Remote Queries

These queries do not require a local knowledge graph and can be executed with a simple HTTP query.

### Getting news articles 

The queries in this section involve fetching more news articles from the graph.


#### IRIs for every article

Get the URIs of news articles in the graph:

```sparql
SELECT *
WHERE {
	?uri a schema:NewsArticle.
}
```

#### All the properties for every news article in the graph 

Similar to the previous one, but this will also include any direct properties of the news article (e.g., headline and body).

```sparql
DESCRIBE ?uri
WHERE {
	?uri a schema:NewsArticle.
}
LIMIT 10 # This limit can be increased
```

#### All articles as a JSON object

A Fuseki extension also allows you to retrieve JSON objects with a specific structure:

```
JSON {
	"@id": ?uri,
	"headline": ?headline,
	"articleBody": ?body
}
WHERE {
	?uri a schema:NewsArticle ;
	     schema:headline ?headline ;
	     schema:articleBody ?body .
}
LIMIT 5
```

#### Articles filtered by topic

This query returns news articles in a given topic (`Travel`), as well as all their annotations.

```sparql

DESCRIBE *
WHERE {
    ?uri a schema:NewsArticle ;
	 schema:category "Travel"@en .
    OPTIONAL {
	    ?annotation oa:hasTarget ?uri .
    }
}
LIMIT 5
```

#### Articles filtered by entities mentioned

Get more news articles based on the entities they mention.
In this example, we filter mentions to `amor-data:PoliciaNacional`.

```sparql

DESCRIBE *
WHERE {
    ?uri a schema:NewsArticle .
    ?annotation a amor:EntityAnnotation ;
	oa:hasTarget ?uri ;
	itsrdf:taIdentRef amor-data:PoliciaNacional .
}
LIMIT 10
```

#### Articles filtered by moral value

Get more news articles based on their moral value.
In this example, we filter news with the `mft:purity` value.

```sparql

DESCRIBE *
WHERE {
    ?uri a schema:NewsArticle .
    ?annotation a amor:MoralValueAnnotation ;
	oa:hasTarget ?uri ;
	amor:hasMoralValueCategory mft:purity .
}
LIMIT 10
```

### Getting more information about a news article

These examples query the remote graph for more information.
This might be useful when deciding what recommendations to make to a user based on the previous articles the user has interacted with.

#### Recommendations

Get any recommendations, regardless of the recommendation strategy or confidence:

```sparql

DESCRIBE ?recommended
WHERE {
	?recommendation oa:hasTarget ?target_news ;
			oa:hasBody ?recommended .

	# This sub-query gets one news article from the graph. You can replace it with the IRI of the news
	# article you are interested in.
	{
		SELECT ?target_news WHERE { ?target_news a schema:NewsArticle; } LIMIT 1
	}
}
```

#### Ranked recommendations

Similar to the previous query, but filtering out unlikely recommendations:

```sparql
SELECT ?recommended ?confidence
WHERE {
	?recommendation oa:hasTarget ?target_news ;
			oa:hasBody ?recommended ;
		     itsrdf:taConfidence ?confidence .
	FILTER (?confidence >= 0.5)

	# This sub-query gets one news article from the graph. You can replace it with the IRI of the news
	# article you are interested in.
	{
		SELECT ?target_news WHERE { ?target_news a schema:NewsArticle; } LIMIT 1
	}
}
ORDER BY DESC(?confidence)
LIMIT 2
```
#### Recommendations with a specific criterion

Similar to the previous query, but focusing on a specific recommendation criterion (`amor-exp:EntitySimilarity`):

```sparql remote/recommendation_by_criterion.sparql
SELECT ?recommended ?confidence
WHERE {
	?recommendation oa:hasTarget ?target_news ;
            amor-exp:hasRecommendationCriterion amor-exp:EntitySimilarity ;
			oa:hasBody ?recommended ;
		     itsrdf:taConfidence ?confidence .
	FILTER (?confidence >= 0.5)

	# This sub-query gets one news article from the graph. You can replace it with the IRI of the news
	# article you are interested in.
	{
		SELECT ?target_news WHERE { ?target_news a schema:NewsArticle; } LIMIT 1
	}
}
ORDER BY DESC(?confidence)
LIMIT 2
```

