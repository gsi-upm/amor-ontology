# AMOR v1.0.0 release procedure

This file prepares the technical release. It does not authorize a production
upload, Git tag, or GitHub Release.

## Release scope and tools

The normative paper-facing RDF artefacts are:

```text
src/amor/amor.ttl
src/bhv/bhv.ttl
src/mft/mft.ttl
src/amor/models/bhv/amor-bhv.ttl
src/amor/models/mft/amor-mft.ttl
src/amor/examples/amor-examples.ttl
```

All Turtle files under `src/` remain normative version-controlled sources. The
six files above are the graph used for competency-question evaluation and the
paper-facing documentation release. Files under `doc/ontologies/` are generated
artefacts and may contain extra declarations or serialization changes.

Toolchain used for this release preparation:

| Tool | Fixed version |
|---|---|
| Python | 3.12.7 (`.python-version`) |
| uv | 0.9.0 in CI |
| pytest | 8.3.4 (`uv.lock`) |
| RDFLib | 7.1.3 (`uv.lock`) |
| WIDOCO | 1.4.25 |
| WIDOCO image | `ghcr.io/dgarijo/widoco@sha256:ef0548a0522d26cc73f3c3ecdb265cbed59aab9eeaa51f18a6096acbc239a41c` |
| Docker used during preparation | 27.4.1 |

## Pre-publication checklist

1. Work through a pull request on a dedicated branch; do not push release work directly to `main`.
2. Confirm that the intended release commit contains no unrelated working-tree changes: `git status --short --branch`.
3. Run `UV_CACHE_DIR=/tmp/uv-cache uv run --frozen pytest -q`.
4. Run all CQs independently with `uv run --frozen python evaluation/run_queries.py`.
5. From a clean commit, run `./scripts/generate_documentation.sh`.
6. Verify normative hashes with `sha256sum --check release/normative-artifacts.sha256`.
7. Re-run pytest so every generated RDF serialization parses and all release-term checks pass.
8. Review generated HTML for AMOR-MFT and AMOR examples, including Fairness, Virtue/Vice, BHV Conservation, and `moralAnnotation23`.
9. Commit the generated documentation and hash manifest without changing the normative sources.
10. From the resulting final commit, regenerate once more before publication. Confirm that `doc/ontologies/BUILDINFO` names that final commit and that semantic validation remains green. This build directory, not an older checkout, is the publication payload.

WIDOCO output is verified semantically, not byte-for-byte. The automated checks
parse generated RDF, verify ontology/version IRIs, and check the release terms
affected by the corrections. WIDOCO 1.4.25 emits invalid Turtle for one nested
`owl:oneOf` expression in the experimental ontology. The generation scripts
therefore validate `ontology.ttl` and, only on parse failure, reserialize the
same generated RDF/XML graph with RDFLib; normative sources are not changed.

## Deployment evidence and current blocker

Ignored legacy scripts under `local_scripts/` provide repository-local evidence
that publication was performed with recursive `scp` from each generated `doc`
directory to `vpsadmin@gsi.upm.es:/data/web/files/ontologies/...`. They combine
generation and upload and previously used mutable WIDOCO `latest` images.

These scripts are not part of the reproducible generation path and must not be
run as-is. Before publication, the user must confirm that the SSH host, account,
destination layout, and operational procedure are still current and explicitly
authorize production access. No CI deployment credentials or deployment job are
defined.

## Post-publication verification

After an authorized upload from the final commit:

1. Retrieve each canonical HTTPS page under `https://gsi.upm.es/ontologies/`.
2. Retrieve the RDF representations for the six artefacts using explicit HTTP `Accept` headers and save them outside the repository.
3. Parse every retrieved representation locally with RDFLib.
4. Verify the ontology IRI, `owl:versionIRI`, and `owl:versionInfo` against the normative source.
5. Verify Fairness membership, Virtue/Vice labels, BHV `/ns#Conservation`, and the category/target split for `moralAnnotation23`.
6. Compare the published normative artefact hashes with `release/normative-artifacts.sha256` where the server exposes those exact source files.
7. Record the verified final commit in the release notes and paper/archive metadata.

## Consequential actions

Only after the final commit and public representations have been verified, and
only with explicit user authorization, create the annotated tag and GitHub
Release:

```bash
git tag -a v1.0.0 <verified-final-commit> -m "AMOR ontology v1.0.0"
git push origin v1.0.0
gh release create v1.0.0 --verify-tag --title "AMOR ontology v1.0.0" --notes-file release/v1.0.0-notes.md
```

Do not execute these commands during release preparation.
