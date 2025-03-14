docker run -ti --rm \
    -v ./src/:/usr/local/widoco/in:Z \
    -v ./doc/ontologies:/usr/local/widoco/out:Z \
    ghcr.io/dgarijo/widoco:latest \
    -confFile in/bhv/widoco-bhv-config.properties \
    -ontFile in/bhv/bhv.ttl \
    -outFolder out/bhv/ns/doc \
    -webVowl -rewriteAll