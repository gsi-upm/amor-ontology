# AMOR Ontology

## Introduction

This repository contains various ontologies for representing experiments and evaluations in the [AMOR project](https://www.gsi.upm.es/amor). Below is a summary of the TTL files and their respective published URLs.

## Ontologies Summary

### 1. **AMOR Ontology**

- **File:** [./src/amor/amor.ttl](./src/amor/amor.ttl)
- **URL:** [http://www.gsi.upm.es/ontologies/amor/ns#](http://www.gsi.upm.es/ontologies/amor/ns#)
- **Description:** This ontology provides the foundational concepts and relationships for Moral Annotation in the AMOR project.

### 2. **AMOR Examples**

- **File:** [./src/amor/examples/amor-examples.ttl](./src/amor/examples/amor-examples.ttl)
- **URL:** [http://www.gsi.upm.es/ontologies/amor/examples#](http://www.gsi.upm.es/ontologies/amor/examples#)
- **Description:** This ontology provides examples and use cases for annotation of news in the AMOR project, demonstrating how the concepts and relationships can be applied.

### 3. **Basic Human Values Taxonomy**

- **File:** [./src/bhv/bhv.ttl](./src/bhv/bhv.ttl)
- **URL:** [http://www.gsi.upm.es/ontologies/bhv/ns#](http://www.gsi.upm.es/ontologies/bhv/ns#)
- **Description:** This SKOS taxonomy mirrors the categories in Basic Human Values Theory and provides a semantic representation using the standard SKOS representation.

### 4. **AMOR Basic Human Values Ontology**

- **File:** [./src/amor/models/amor-bhv.ttl](./src/amor/models/amor-bhv.ttl)
- **URL:** [http://www.gsi.upm.es/ontologies/amor/models/bhv/ns#](http://www.gsi.upm.es/ontologies/amor/models/bhv/ns#)
- **Description:** AMOR-BHV is an ontology that uses AMOR ontology and BHV SKOS Taxonomy to create required relations to use BHV to define moral annotations.

### 5. **Moral Foundations Theory Taxonomy**

- **File:** [./src/mft/mft.ttl](./src/mft/mft.ttl)
- **URL:** [http://www.gsi.upm.es/ontologies/mft/ns#](http://www.gsi.upm.es/ontologies/mft/ns#)
- **Description:** This SKOS taxonomy mirrors the categories in Moral Foundations Theory and provides a semantic representation using the standard SKOS representation.

### 6. **AMOR Moral Foundations Ontology**

- **File:** [./src/amor/models/amor-mft.ttl](./src/amor/models/amor-mft.ttl)
- **URL:** [http://www.gsi.upm.es/ontologies/amor/models/mft/ns#](http://www.gsi.upm.es/ontologies/amor/models/mft/ns#)
- **Description:** AMOR-MFT is an ontology that uses AMOR ontology and MFT SKOS Taxonomy to create required relations to use MFT to define moral annotations.

### 7. **AMOR Experiments Ontology**

- **File:** [./src/amor/experiments/amor-experiments.ttl](./src/amor/experiments/amor-experiments.ttl)
- **URL:** [http://www.gsi.upm.es/ontologies/amor/experiments/ns#](http://www.gsi.upm.es/ontologies/amor/experiments/ns#)
- **Description:** This ontology is designed for representing experiments and evaluations in the AMOR project. It includes classes and properties for defining experiments, experimentation subjects, parameters, and various strategies used in the experiments.

### 8. **AMOR Experiments Examples**

- **File:** [./src/amor/experiments/examples/amor-experiments-examples.ttl](./src/amor/experiments/examples/amor-experiments-examples.ttl)
- **URL:** [http://www.gsi.upm.es/ontologies/amor/experiments/examples#](http://www.gsi.upm.es/ontologies/amor/experiments/examples#)
- **Description:** This ontology provides examples and use cases for the AMOR Experiments Ontology, demonstrating how the concepts and relationships can be applied in experimental scenarios.
- **File:** [./src/amor/experiments/examples/amor-experiments-examples.json](./src/amor/experiments/examples/amor-experiments-examples.json)
- **Description:** JSON-LD representation for the same example.

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

## Generating documentation

All the documentation generated by [WIDOCO](https://github.com/dgarijo/Widoco) (and some manually added content) is located in `./doc/ontologies`.

Example WIDOCO command:

```bash
docker run -ti --rm -v ./src:/usr/local/widoco/in:Z -v ./doc:/usr/local/widoco/out:Z ghcr.io/dgarijo/widoco:latest -confFile in/widoco-amor-experiments-examples-config.properties -ontFile in/amor-experiments-examples.ttl -outFolder out/ontologies/amor/experiments/examples/doc -webVowl -rewriteAll
```

Every folder has a properties file for widoco configuration.

## Testing

There are some basic tests at `tests/`.

To run them:

```bash
pytest
```
