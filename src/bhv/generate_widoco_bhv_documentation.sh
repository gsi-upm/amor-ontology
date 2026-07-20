docker run --rm \
    -v ./src/:/usr/local/widoco/in:Z \
    -v ./doc/ontologies:/usr/local/widoco/out:Z \
    ghcr.io/dgarijo/widoco@sha256:ef0548a0522d26cc73f3c3ecdb265cbed59aab9eeaa51f18a6096acbc239a41c \
    -confFile in/bhv/widoco-bhv-config.properties \
    -ontFile in/bhv/bhv.ttl \
    -outFolder out/bhv/ns/doc \
    -webVowl -rewriteAll
