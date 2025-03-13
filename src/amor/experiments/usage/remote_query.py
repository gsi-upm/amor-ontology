import requests
import sys

ENDPOINT = "https://amor-graph.gsi.upm.es/news/"
with open("../../../prefixes.sparql") as f:
    PREFIXES = f.read() + "\n\n"

if __name__ == '__main__':

    QUERY = sys.argv[1]

    if len(sys.argv) > 2:
        ENDPOINT = sys.arg[2]

    query_string = PREFIXES

    with open(QUERY) as f:
        query_string += f.read()

    requestheader = {
            'User-Agent': 'TestAgent/0.1', 
            'Accept': 'application/sparql-results+json',
            'Content-Type': 'application/x-www-form-urlencoded'
            }
        
    response = requests.post(ENDPOINT, data={'query' : query_string}, headers=requestheader)

    print(response.text)
