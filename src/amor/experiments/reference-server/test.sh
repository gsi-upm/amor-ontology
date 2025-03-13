#!/bin/sh
curl -H "Content-Type: application/json"  -X POST -d @experiment-example-for-api.json 'http://localhost:8000/run'


