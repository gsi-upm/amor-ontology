# Amor Experiment API

This repository explains how the experiment API expects to receive datasets with annotated news articles.
Each article will be annotated in different ways (sentiment, emotion, morality), and will contain a set of suggestions according to different criteria.

![OpenAPI](./img/openapi.png)

## Files

The main files are the following:

* `convert-json.py` can be used to convert the example from the AMOR examples website to a working JSON-LD file
* `tests.py` contains a series of tests to ensure that the annotation of recommendations is viable. It will ensure that the both the annotated JSON object and the parsed RDF graph contain the same data and can be used to filter recommendations.
* `server.py` is a stub implementation of an experiment server that accepts the dataset with news articles in a POST request and the criteria for recommendation, and returns the mapping between each news article and the list of recommendations.
* `context.jsonld` is the JSON-LD context used in the `dataset-example.json` file
* `prefixes.json` is a simpler JSON-LD context with the main prefixes used in AMOR


## Running this project

This project is set up with `uv`, but the included `pyproject.toml` should be compatible with any other tool (e.g., poetry, pip).

You can run the stub server like so:

```
uv run fastapi dev server.py
```

The OpenAPI dashboard/docs can be access through [localhost](http://localhost:8000/docs), or you could call the API with a tool like curl:

```
curl -i -X POST -H 'Content-type: application/json' --data '@dataset-example.json' 'http://localhost:8000/experiment?recommendation_criterion=rec:MoralSimilarity'
```
