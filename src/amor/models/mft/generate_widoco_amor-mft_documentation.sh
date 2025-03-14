docker run -ti --rm \
    -v ./src/:/usr/local/widoco/in:Z \
    -v ./doc_test/ontologies:/usr/local/widoco/out:Z \
    ghcr.io/dgarijo/widoco:latest \
    -confFile in/amor/models/amor/models/mft/widoco-amor-mft-config.properties \
    -ontFile in/amor/models/mft/amor-mft.ttl \
    -outFolder out/amor/models/mft/ns/doc \
    -webVowl -rewriteAll