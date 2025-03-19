docker run -ti --rm \
    -v ./src/:/usr/local/widoco/in:Z \
    -v ./doc/ontologies:/usr/local/widoco/out:Z \
    ghcr.io/dgarijo/widoco:latest \
    -confFile in/amor/models/bhv/widoco-amor-bhv-config.properties \
    -ontFile in/amor/models/bhv/amor-bhv.ttl \
    -outFolder out/amor/models/bhv/ns/doc \
    -webVowl -rewriteAll
