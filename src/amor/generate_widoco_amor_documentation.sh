docker run -ti --rm \
    -v ./src/:/usr/local/widoco/in:Z \
    -v ./doc/ontologies:/usr/local/widoco/out:Z \
    ghcr.io/dgarijo/widoco:latest \
    -confFile in/amor/widoco-amor-config.properties \
    -ontFile in/amor/amor.ttl \
    -outFolder out/amor/ns/doc \
    -webVowl -rewriteAll