docker run -ti --rm \
    -v ./src/:/usr/local/widoco/in:Z \
    -v ./doc/ontologies:/usr/local/widoco/out:Z \
    ghcr.io/dgarijo/widoco:latest \
    -confFile in/amor/experiments/widoco-amor-experiments-config.properties \
    -ontFile in/amor/experiments/amor-experiments.ttl \
    -outFolder out/amor/experiments/ns/doc \
    -webVowl -rewriteAll