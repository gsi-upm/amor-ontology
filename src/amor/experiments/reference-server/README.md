# Amor experiments reference API

This is a reference implementation of an Experiments API that uses the JSON model of experiments defined in the AMOR project.

### Running

```shell
uv run fastapi dev server.py
```


### Sending a JSON object

```
#!/bin/sh
curl -H "Content-Type: application/json"  -X POST -d @experiment-example-for-api.json 'http://localhost:8000/run'
```
