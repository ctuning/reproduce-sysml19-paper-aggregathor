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
* **Evaluators:** 

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
to automate and facilitate this evaluation.

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

 Test 


# Reproducibility badges

## ACM badges
* ACM artifacts available 
* ACM artifacts evaluated - reusable 

[![](https://www.acm.org/binaries/content/gallery/acm/publications/replication-badges/artifacts_available_dl.jpg)](https://www.acm.org/publications/policies/artifact-review-badging)
[![](https://www.acm.org/binaries/content/gallery/acm/publications/replication-badges/artifacts_evaluated_reusable_dl.jpg)](https://www.acm.org/publications/policies/artifact-review-badging)

## cTuning foundation badges
[![automation](https://github.com/ctuning/ck-guide-images/blob/master/ck-artifact-automated-and-reusable.svg)](http://cTuning.org/ae)
[![workflow](https://github.com/ctuning/ck-guide-images/blob/master/ck-workflow.svg)](http://cKnowledge.org)
