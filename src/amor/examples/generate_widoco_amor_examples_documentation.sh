docker run -ti --rm \
    -v ./src/:/usr/local/widoco/in:Z \
    -v ./doc/ontologies:/usr/local/widoco/out:Z \
    ghcr.io/dgarijo/widoco:latest \
    -confFile in/amor/examples/widoco-amor-examples-config.properties \
    -ontFile in/amor/examples/amor-examples.ttl \
    -outFolder out/amor/examples/doc \
    -webVowl -rewriteAll