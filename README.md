[![](https://www.acm.org/binaries/content/gallery/acm/publications/replication-badges/artifacts_available_dl.jpg)](https://www.acm.org/publications/policies/artifact-review-badging)
[![](https://www.acm.org/binaries/content/gallery/acm/publications/replication-badges/artifacts_evaluated_reusable_dl.jpg)](https://www.acm.org/publications/policies/artifact-review-badging)

[![automation](https://github.com/ctuning/ck-guide-images/blob/master/ck-artifact-automated-and-reusable.svg)](http://cTuning.org/ae)
[![workflow](https://github.com/ctuning/ck-guide-images/blob/master/ck-workflow.svg)](http://cKnowledge.org)

This repository contains the reproducibility report for the SysML'19 paper 
"AGGREGATHOR: Byzantine Machine Learning via Robust Gradient Aggregation".
Feel free to continue evaluating all experimental results from this paper 
and report your feedback [here](https://github.com/ctuning/reproduce-sysml19-paper-aggregathor/issues).

* **Conference:** [SysML'19](http://sysml.cc)
* **Paper:** AGGREGATHOR: Byzantine Machine Learning via Robust Gradient Aggregation
* **Authors:** Georgios Damaskinos, El Mahdi El Mhamdi, Rachid Guerraoui, Arsany Guirguis, Sebastien Rouault
* **Artifact DOI:** [Zenodo](https://doi.org/10.5281/zenodo.2548779)
* **Evaluation methodology:** [SysML](http://cTuning.org/ae/sysml2019.html), [ACM badging](https://www.acm.org/publications/policies/artifact-review-badging), [ACM REQUEST](http://cKnowledge.org/request)
* **Automated workflow:** [CK](https://github.com/ctuning/ck)
* **Evaluators:** [Matteo Interlandi](https://interesaaat.github.io) (Microsoft) and [Grigori Fursin](http://fursin.net/research.html) (cTuning foundation and dividiti)

# Artifact check-list (meta-information)

* **Program:** TensorFlow (1.10.1), python (3.5+)
* **Compilation:** C++11
* **Data set:** MNIST, CIFAR–10, ImageNet (optional), . . .
* **Run-time environment:** Debian GNU/Linux (or equivalent)
* **Hardware:** [G5k](https://grid5000.fr) (or equivalent)
* **Metrics:** (time to reach some) top–1 cross–accuracy
* **How much disk space required (approximately)?:** <1 MB (code only)
* **How much time is needed to prepare workflow (approximately)?:** a few minutes to a few hours (several optional components, some demanding a rebuild of TensorFlow)
* **How much time is needed to complete experiments (approximately)?:** two minutes (see Section A.6) to a few days (for all the experiments of the main paper)
* **Code license:** MIT

# Installation

We implemented a simple [CK workflow (pipeline)](http://cKnowledge.org) 
with shared [CK packages](http://cKnowledge.org/shared-packages.html)
for the TensorFlow framework, models and datasets to automate and facilitate this evaluation.

## CK framework

Install CK as described [here](https://github.com/ctuning/ck#installation).

## CK workflow (pipeline) for this paper

```
$ ck pull repo:reproduce-sysml19-paper-aggregathor
```

Note that CK will pull all other related repositories.
If you already have installed CK repositories, you may update 
them at any time all as follows:
```
$ ck pull all
```

# Evaluation

We created CK program workflow (pipeline) with [meta information](https://github.com/ctuning/reproduce-sysml19-paper-aggregathor/blob/master/program/sysml19-aggregathor/.cm/meta.json) 
which describes dependencies (code, models and data sets), automates their installation 
during the first execution (TensorFlow, SLIM models, MNIST, CIFAR10),
and assembles different command lines.

* [CK run script for MNIST](https://github.com/ctuning/reproduce-sysml19-paper-aggregathor/blob/master/program/sysml19-aggregathor/ck_run.sh)
* [CK run script for CIFAR10 with automated installation of the model and the dataset](https://github.com/ctuning/reproduce-sysml19-paper-aggregathor/blob/master/program/sysml19-aggregathor/ck_run_cifar10.sh) 

* [Default environment variables](https://github.com/ctuning/reproduce-sysml19-paper-aggregathor/blob/master/program/sysml19-aggregathor/.cm/meta.json#L101)

It is possible to run this pipeline as follows:
```
$ ck run program:sysml19-aggregathor
```

You can also customize this pipeline by changing above environment variables using CK CLI as follows:
```
$ ck run program:sysml19-aggregathor --env.AGGREGATOR="average" ...
```

## Local deployment

**Platform:** [GRID5000](https://www.grid5000.fr); Rennes site; [Paravance node](https://www.grid5000.fr/mediawiki/index.php/Rennes:Hardware#paravance)

### MNIST

CK CLI:
```
$ ck run program:sysml19-aggregathor --cmd_key=local-mnist
```

Validated results: [Link](https://github.com/ctuning/reproduce-sysml19-paper-aggregathor/issues/1)

### MNIST-attack

CK CLI:
```
$ ck run program:sysml19-aggregathor --cmd_key=local-mnist-attack
```

Validated results: [Link](https://github.com/ctuning/reproduce-sysml19-paper-aggregathor/issues/2)

### CIFAR10

You can rely on CK to install this dataset and related code automatically or you can install via CK CLI before running the program pipeline as follows:
```
$ ck install package --tags=dataset,tensorflow-slim,cifar10
```

Note that you may need ~1GB of free space and it will take some time to download TensorFlow models and process this data set!

CK CLI:
```
$ ck run program:sysml19-aggregathor --cmd_key=local-cifar10
```

TBD

## Distributed depolyment

TBD



# Reproducibility badges

We awarded the following badges based on above evaluation:

## ACM badges
* ACM artifacts available 
* ACM artifacts evaluated - reusable 

[![](https://www.acm.org/binaries/content/gallery/acm/publications/replication-badges/artifacts_available_dl.jpg)](https://www.acm.org/publications/policies/artifact-review-badging)
[![](https://www.acm.org/binaries/content/gallery/acm/publications/replication-badges/artifacts_evaluated_reusable_dl.jpg)](https://www.acm.org/publications/policies/artifact-review-badging)

## cTuning foundation badges
[![automation](https://github.com/ctuning/ck-guide-images/blob/master/ck-artifact-automated-and-reusable.svg)](http://cTuning.org/ae)
[![workflow](https://github.com/ctuning/ck-guide-images/blob/master/ck-workflow.svg)](http://cKnowledge.org)
