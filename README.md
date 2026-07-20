# AMOR Ontology

## Introduction

This repository contains ontologies for representing experiments and evaluations in the [AMOR project](https://www.gsi.upm.es/amor). The links below are the canonical HTTPS publication pages. The RDF vocabulary and ontology IRIs remain exactly as declared in the Turtle sources, including their historical `http://www.gsi.upm.es` form.

## Ontologies Summary

### 1. **AMOR Ontology**

- **File:** [./src/amor/amor.ttl](./src/amor/amor.ttl)
- **URL:** [https://gsi.upm.es/ontologies/amor/ns](https://gsi.upm.es/ontologies/amor/ns)
- **Description:** This ontology provides the foundational concepts and relationships for Moral Annotation in the AMOR project.

### 2. **AMOR Examples**

- **File:** [./src/amor/examples/amor-examples.ttl](./src/amor/examples/amor-examples.ttl)
- **URL:** [https://gsi.upm.es/ontologies/amor/examples](https://gsi.upm.es/ontologies/amor/examples)
- **Description:** This ontology provides examples and use cases for annotation of news in the AMOR project, demonstrating how the concepts and relationships can be applied.

### 3. **Basic Human Values Taxonomy**

- **File:** [./src/bhv/bhv.ttl](./src/bhv/bhv.ttl)
- **URL:** [https://gsi.upm.es/ontologies/bhv/ns](https://gsi.upm.es/ontologies/bhv/ns)
- **Description:** This SKOS taxonomy mirrors the categories in Basic Human Values Theory and provides a semantic representation using the standard SKOS representation.

### 4. **AMOR Basic Human Values Ontology**

- **File:** [./src/amor/models/bhv/amor-bhv.ttl](./src/amor/models/bhv/amor-bhv.ttl)
- **URL:** [https://gsi.upm.es/ontologies/amor/models/bhv/ns](https://gsi.upm.es/ontologies/amor/models/bhv/ns)
- **Description:** AMOR-BHV is an ontology that uses AMOR ontology and BHV SKOS Taxonomy to create required relations to use BHV to define moral annotations.

### 5. **Moral Foundations Theory Taxonomy**

- **File:** [./src/mft/mft.ttl](./src/mft/mft.ttl)
- **URL:** [https://gsi.upm.es/ontologies/mft/ns](https://gsi.upm.es/ontologies/mft/ns)
- **Description:** This SKOS taxonomy mirrors the categories in Moral Foundations Theory and provides a semantic representation using the standard SKOS representation.

### 6. **AMOR Moral Foundations Ontology**

- **File:** [./src/amor/models/mft/amor-mft.ttl](./src/amor/models/mft/amor-mft.ttl)
- **URL:** [https://gsi.upm.es/ontologies/amor/models/mft/ns](https://gsi.upm.es/ontologies/amor/models/mft/ns)
- **Description:** AMOR-MFT is an ontology that uses AMOR ontology and MFT SKOS Taxonomy to create required relations to use MFT to define moral annotations.

### 7. **AMOR Experiments Ontology**

- **File:** [./src/amor/experiments/amor-experiments.ttl](./src/amor/experiments/amor-experiments.ttl)
- **URL:** [https://gsi.upm.es/ontologies/amor/experiments/ns](https://gsi.upm.es/ontologies/amor/experiments/ns)
- **Description:** This ontology is designed for representing experiments and evaluations in the AMOR project. It includes classes and properties for defining experiments, experimentation subjects, parameters, and various strategies used in the experiments.

### 8. **AMOR Experiments Examples**

- **File:** [./src/amor/experiments/examples/amor-experiments-examples.ttl](./src/amor/experiments/examples/amor-experiments-examples.ttl)
- **URL:** [https://gsi.upm.es/ontologies/amor/experiments/examples](https://gsi.upm.es/ontologies/amor/experiments/examples)
- **Description:** This ontology provides examples and use cases for the AMOR Experiments Ontology, demonstrating how the concepts and relationships can be applied in experimental scenarios.
- **File:** [./src/amor/experiments/examples/amor-experiments-examples.json](./src/amor/experiments/examples/amor-experiments-examples.json)
- **Description:** Non-normative, application-oriented JSON view for the experimental API; it is not an RDF-equivalence artefact for the Turtle source.

### 9. **AMOR Datasets Examples Folder**

- **File:** [./src/amor/datasets/examples/](./src/amor/datasets/examples/)
- **Description:** This folder contains some examples for NewsDataset used in the experiments.

### 10. **SEGB Ontology**

- **File:** [https://github.com/gsi-upm/amor-segb/blob/main/ontology/segb.ttl](https://github.com/gsi-upm/amor-segb/blob/main/ontology/segb.ttl)
- **URL:** [http://www.gsi.upm.es/ontologies/segb/ns#](http://www.gsi.upm.es/ontologies/segb/ns#)
- **Description:** This ontology provides the foundational concepts and relationships for the Semantic Ethical Glass Box (SEGB), inside the AMOR project, focusing on semantic representation of social and ethical guidelines for behavior.
- **Note:** This is published in an independent repository to publish the SEGB as an independent tool.

### 11. **SEGB Examples**

- **File:** [https://github.com/gsi-upm/amor-segb/blob/main/ontology/example.ttl](https://github.com/gsi-upm/amor-segb/blob/main/ontology/example.ttl)
- **URL:** [http://www.gsi.upm.es/ontologies/segb/examples#](http://www.gsi.upm.es/ontologies/segb/examples#)
- **Description:** This ontology provides examples and use cases for the SEGB ontology, demonstrating how the concepts and relationships can be applied in various scenarios.
- **Note:** This is published in an independent repository to publish the SEGB as an independent tool, but this example uses a lot of the ontologies published in this repository (i.e. the reminder AMOR project ontologies.).

## Competency-question evaluation

The ten executable competency questions, their exact six-file graph manifest,
expected evidence, and CQ-to-test traceability are documented in
[`evaluation/README.md`](./evaluation/README.md).

## Generating documentation

The Turtle files under `src/` are normative. The RDF serializations, HTML,
diagrams, and support files under `doc/ontologies/` are generated publication
artefacts; they do not replace the source Turtle graphs.

Release documentation uses WIDOCO 1.4.25, pinned to the published container
digest `sha256:ef0548a0522d26cc73f3c3ecdb265cbed59aab9eeaa51f18a6096acbc239a41c`.
From a clean release commit, generate all six paper-facing documentation sets:

```bash
./scripts/generate_documentation.sh
sha256sum --check release/normative-artifacts.sha256
```

The script rejects modified normative inputs by default, records the source
commit and image digest in the generated `doc/ontologies/BUILDINFO`, and
refreshes the normative SHA-256 manifest. `--allow-dirty` exists only for local
pre-commit verification and marks the build accordingly. Individual pinned
generators remain next to their source/configuration files.

Generation does not deploy. See [`RELEASE.md`](./RELEASE.md) for the complete
release order, semantic checks, repository evidence about the historical
deployment mechanism, and actions that require explicit authorization.

## Testing

Python 3.12.7 and uv 0.9.0 are fixed for release validation. The lockfile is
authoritative for Python dependencies. Run the same command used by CI:

```bash
UV_CACHE_DIR=/tmp/uv-cache uv run --frozen pytest -q
```

After dependencies have been materialised once, the suite itself is fully
offline and can be checked explicitly with `uv run --offline --frozen pytest -q`.
