docker run --rm \
    -v ./src/:/usr/local/widoco/in:Z \
    -v ./doc/ontologies:/usr/local/widoco/out:Z \
    ghcr.io/dgarijo/widoco@sha256:ef0548a0522d26cc73f3c3ecdb265cbed59aab9eeaa51f18a6096acbc239a41c \
    -confFile in/amor/experiments/examples/widoco-amor-experiments-examples-config.properties \
    -ontFile in/amor/experiments/examples/amor-experiments-examples.ttl \
    -outFolder out/amor/experiments/examples/doc \
    -webVowl -rewriteAll

UV_CACHE_DIR="${UV_CACHE_DIR:-/tmp/uv-cache}" uv run --offline --frozen python \
    scripts/repair_widoco_turtle.py doc/ontologies/amor/experiments/examples/doc/ontology.ttl
