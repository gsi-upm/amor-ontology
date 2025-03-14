docker run -ti --rm \
    -v ./src/:/usr/local/widoco/in:Z \
    -v ./doc/ontologies:/usr/local/widoco/out:Z \
    ghcr.io/dgarijo/widoco:latest \
    -confFile in/mft/widoco-mft-config.properties \
    -ontFile in/mft/mft.ttl \
    -outFolder out/mft/ns/doc \
    -webVowl -rewriteAll