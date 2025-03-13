# AMOR Ontology

# TODO: improve the documentation and reorganize the repo

## Introduction

## Generating documentation

Example WIDOCO command:

```
docker run -ti --rm -v ./src:/usr/local/widoco/in:Z -v ./doc:/usr/local/widoco/out:Z ghcr.io/dgarijo/widoco:latest -confFile in/widoco-amor-experiments-examples-config.properties -ontFile in/amor-experiments-examples.ttl -outFolder out/ontologies/amor/experiments/examples/doc -webVowl -rewriteAll
```

## Testing

There are some basic tests at `tests/`.
To run them:

```
pytest
```

## Research datasets

The goal of this experiment was to see the capabilities of AMOR ontology as a universal data schema used with real data extracted with existing algorithms. 

### Webis-ArgValues-22

- Source: [https://webis.de/data/webis-argvalues-22.html](https://webis.de/data/webis-argvalues-22.html)
- Description: a dataset of 5270 arguments from four geographical cultures, manually annotated for human values.
- Reference paper: Kiesel, J., Alshomary, M., Handke, N., Cai, X., Wachsmuth, H., & Stein, B. (2022, May). Identifying the human values behind arguments. In Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers) (pp. 4459-4471).

**Arguments** (arguments.tsv)

| Dataset field | Mapping | Description | Example |
| ------------- | ------- | ----------- | ------- |
| Argument ID   | amor:extractedFrom | Reference to the text | A01001 |
| Part | uncovered:part | Name of the containing dataset part from the paper; one of "africa", "china", "india", "usa" | africa |
| Usage | uncovered:usage | Name of the set the argument is used for in the machine learning experiments; one of "train", "validation" or "test" | train |
| Conclusion | uncovered:conclusion | Conclusion text of the argument | Entrapment should be legalized |
| Stance | uncovered:stance | Stance of the `Premise` towards the `Conclusion; one of "in favor of", "against" | in favor of |
| Premise | amor:text | Premise text of the argument | if entrapment can serve to more easily capture wanted criminals, then why shouldn't it be legal? |

**Annotations Level 1** (labels_level1.tsv)

| Dataset field | Mapping | Description | Example |
| ------------- | ------- | ----------- | ------- |
| Argument ID   | amor:extractedFrom | Reference to the text | A01001 |
| Label | amor:Value | Value expressed in the text | Have a stable society; Have a safe country |

**Annotations Level 2** (labels_level2.tsv)

| Dataset field | Mapping | Description | Example |
| ------------- | ------- | ----------- | ------- |
| Argument ID   | amor:extractedFrom | Reference to the text | A01001 |
| Label | amor:Value | Value expressed in the text | Security: societal |

**Annotations Level 3** (labels_level3.tsv)

| Dataset field | Mapping | Description | Example |
| ------------- | ------- | ----------- | ------- |
| Argument ID   | amor:extractedFrom | Reference to the text | A01001 |
| Label | amor:Value | Value expressed in the text | Conservation |

**Annotations Level 4a** (labels_level4a.tsv)

| Dataset field | Mapping | Description | Example |
| ------------- | ------- | ----------- | ------- |
| Argument ID   | amor:extractedFrom | Reference to the text | A01001 |
| Label | amor:Value | Value expressed in the text | Social focus |

**Annotations Level 4b** (labels_level4b.tsv)

| Dataset field | Mapping | Description | Example |
| ------------- | ------- | ----------- | ------- |
| Argument ID   | amor:extractedFrom | Reference to the text | A01001 |
| Label | amor:Value | Value expressed in the text | Self-protection, Anxiety avoidance |

### Touché23-ValueEval

- Source: [https://webis.de/data/touche23-valueeval.html](https://webis.de/data/touche23-valueeval.html)
- Description: a supplementary dataset adding another 459 arguments for a total of 9324 annotated arguments.
- Reference paper: Mirzakhmedova, N., Kiesel, J., Alshomary, M., Heinrich, M., Handke, N., Cai, X., ... & Stein, B. (2023). The Touch\'e23-ValueEval Dataset for Identifying Human Values behind Arguments. arXiv preprint arXiv:2301.13771.

**Arguments** (arguments-training.tsv)

| Dataset field | Mapping | Description | Example |
| ------------- | ------- | ----------- | ------- |
| Argument ID   | amor:extractedFrom | Reference to the text | A27034 |
| Conclusion | uncovered:conclusion | Conclusion text of the argument | We should ban fast food |
| Stance | uncovered:stance | Stance of the `Premise` towards the `Conclusion; one of "in favor of", "against" | in favor of |
| Premise | amor:text | Premise text of the argument | obesity is rising at an alarming rate and fatty foods and sugar filled drinks are shown to be one of the biggest contributors so fast food should be banned because those foods are sold there. |

**Annotations Level 1** (level1-labels-training.tsv)

| Dataset field | Mapping | Description | Example |
| ------------- | ------- | ----------- | ------- |
| Argument ID   | amor:extractedFrom | Reference to the text | A27034 |
| Label | amor:Value | Value expressed in the text | Have good health; Have a comfortable life; Be helpful; Have the own family secured;	Be responsible |

**Annotations Level 2** (labels-training.tsv)

| Dataset field | Mapping | Description | Example |
| ------------- | ------- | ----------- | ------- |
| Argument ID   | amor:extractedFrom | Reference to the text | A27034 |
| Label | amor:Value | Value expressed in the text | Security: personal; Benevolence: caring; Benevolence: dependability |

### VALUENET

- Source: [https://liang-qiu.github.io/ValueNet/](https://liang-qiu.github.io/ValueNet/)
- Description: a new large-scale human value dataset called ValueNet, which contains human attitudes on 21,374 text scenarios. The dataset is organized in ten dimensions that conform to the basic human value theory in intercultural research.
- Reference paper: Qiu, L., Zhao, Y., Li, J., Lu, P., Peng, B., Gao, J., & Zhu, S. C. (2022, June). Valuenet: A new dataset for human value driven dialogue system. In Proceedings of the AAAI Conference on Artificial Intelligence (Vol. 36, No. 10, pp. 11183-11191).

**Annotations** (train.csv)

| Dataset field | Mapping | Description | Example |
| ------------- | ------- | ----------- | ------- |
| Scenario   | amor:text | Text of the scenario | After accomplishing every task I cross each item off my list |
| Label | amor:Value | Value expressed in the text | Power |
| Polarity | amor:valuePolarity | Value polarity; -1, 0 or 1 | 1 |

### The Moral Foundations Reddit Corpus

- Source: [https://huggingface.co/datasets/USC-MOLA-Lab/MFRC](https://huggingface.co/datasets/USC-MOLA-Lab/MFRC)
- Description: a collection of 16,123 English Reddit comments that have been curated from 12 distinct subreddits, hand-annotated by at least three trained annotators for 8 categories of moral sentiment (i.e., Care, Proportionality, Equality, Purity, Authority, Loyalty, Thin Morality, Implicit/Explicit Morality) based on the updated Moral Foundations Theory (MFT) framework.
- Reference paper: Trager, J., Ziabari, A. S., Davani, A. M., Golazizian, P., Karimi-Malekabadi, F., Omrani, A., ... & Dehghani, M. (2022). The moral foundations reddit corpus. arXiv preprint arXiv:2208.05545.

**Annotations** (final_mfrc_data.csv)

| Dataset field | Mapping | Description | Example |
| ------------- | ------- | ----------- | ------- |
| Text   | amor:text | Text of the Reddit post | That particular part of the debate is especially funny. Macron was explaining he did not think FN voters were evil and that from where he comes from he knew many, and she was like ""ooooh the evil FN invaders they're everywhere...!"" Self-awareness: zero. |
| Subreddit | uncovered:subreddit | Subreddit where the post was published | europe |
| Bucket | uncovered:bucket | Bucket where the post was published | French politics |
| Annotator  | uncovered:annotator | Annotator of the post | annotator03 |
| Label | amor:Value | Value expressed in the text | Non-Moral |
| Confidence | amor:confidence | Confidence of the annotation, one of Confident, Somewhat Confident, Not Confident | Confident |

### Moral Foundations Twitter Corpus

- Source: [https://osf.io/k5n7y/](https://osf.io/k5n7y/)
- Description: a collection of 35,108 tweets that have been curated from seven distinct domains of discourse and hand annotated by at least three trained annotators for 10 categories of moral sentiment.
- Reference paper: Hoover, J., Portillo-Wightman, G., Yeh, L., Havaldar, S., Davani, A. M., Lin, Y., ... & Dehghani, M. (2020). Moral foundations twitter corpus: A collection of 35k tweets annotated for moral sentiment. Social Psychological and Personality Science, 11(8), 1057-1071.


**Annotations** (MFTC_V4.json)

| Dataset field | Mapping | Description | Example |
| ------------- | ------- | ----------- | ------- |
| TweetID   | amor:extractedFrom | Reference to the tweet | 521033092132503552 |
| Annotation | amor:Value | Value expressed in the text | Care; Purity |
| Annotator  | uncovered:annotator | Annotator of the post | annotator01 |

### The Moral Integrity Corpus (MIC)

- Source: [https://github.com/SALT-NLP/mic](https://github.com/SALT-NLP/mic)
- Description: MIC contains 114k annotations, with 99k distinct "Rules of  Thumb" (RoTs) that capture the moral assumptions of 38k chatbot replies to open-ended prompts.
- Reference paper: Ziems, C., Yu, J., Wang, Y. C., Halevy, A., & Yang, D. (2022, May). The Moral Integrity Corpus: A Benchmark for Ethical Dialogue Systems. In Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers) (pp. 3755-3773).


**Annotations**

| Dataset field | Mapping | Description | Example |
| ------------- | ------- | ----------- | ------- |
| Answer | amor:text | Answer of the chatbot to be annotated | I don't think so. Attempted murder carries a maximum sentence of life imprisonment. |
| Moral | amor:Value | Value expressed in the text | care-fairness |

### SOCIAL CHEMISTRY 101

- Source: [https://maxwellforbes.com/social-chemistry/](https://maxwellforbes.com/social-chemistry/)
- Description: a large-scale corpus that catalogs 292k rules-of-thumb such as “It is rude to run a blender at 5am” as the basic conceptual units. Each rule-of-thumb is further broken down with 12 different dimensions of people’s judgments, including social judgments of good and bad, moral foundations, expected cultural pressure, and assumed legality.
- Reference paper: Forbes, M., Hwang, J. D., Shwartz, V., Sap, M., & Choi, Y. (2020). Social chemistry 101: Learning to reason about social and moral norms. arXiv preprint arXiv:2011.00620.


**Annotations**

| Dataset field | Mapping | Description | Example |
| ------------- | ------- | ----------- | ------- |
| Answer | amor:text | The rule of thumb written by the worker | It's good to listen to your parents' advice. |
| Rot Moral Foundations | amor:Value | Worker labeled "\|" separated list of 0 -- 5 moral foundation _axes_. Choices: {care-harm, fairness-cheating, loyalty-betrayal, authority-subversion, sanctity-degradation}.  | care-harm\|fairness-cheating |

