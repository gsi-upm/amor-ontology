docker run -ti --rm \
    -v ./src/:/usr/local/widoco/in:Z \
    -v ./doc/ontologies:/usr/local/widoco/out:Z \
    ghcr.io/dgarijo/widoco:latest \
    -confFile in/amor/experiments/examples/widoco-amor-experiments-examples-config.properties \
    -ontFile in/amor/experiments/examples/amor-experiments-examples.ttl \
    -outFolder out/amor/experiments/examples/doc \
    -webVowl -rewriteAll