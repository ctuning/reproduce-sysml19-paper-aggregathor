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
$ ck run program:sysml19-aggregathor --env.AGGREGATOR=average
```

or with all vars:

```
$ ck run program:sysml19-aggregathor \
    --env.EXPERIMENT=mnist \ 
    --env.WK_JOB_NAME=local \
    --env.EV_JOB_NAME=local \ 
    --env.PS_JOB_NAME=local \ 
    --env.MAX_STEP=10000 \
    --env.AGGREGATOR=average \ 
    --env.NB_WORKERS=4 \ 
    --env.CHECKPOINT_DELTA=-1 \ 
    --env.CHECKPOINT_PERIOD=-1 \ 
    --env.EVALUATION_DELTA=100 \ 
    --env.EVALUATION_PERIOD=-1 \ 
    --env.LEARNING_RATE_ARGS="initial-rate:0.05" \
    --env.SUMMARY_DELTA=-1 \
    --env.SUMMARY_PERIOD=-1 

```

## Local deployment

**Platform:** [GRID5000](https://www.grid5000.fr); Rennes site; [Paravance node](https://www.grid5000.fr/mediawiki/index.php/Rennes:Hardware#paravance)

### MNIST

CK CLI:
```
$ ck run program:sysml19-aggregathor --cmd_key=local-mnist
```

Validated results for the default aggregator: [Link](https://github.com/ctuning/reproduce-sysml19-paper-aggregathor/issues/1)

See all available aggregator plugins:
```
$ ck run program:sysml19-aggregathor --cmd_key=local-mnist --env.AGGREGATOR=""
```

You should normally see the following:
```
...
      Traceback (most recent call last):
        File "runner.py", line 343, in <module>
          aggregator = aggregators.instantiate(args.aggregator, args.nb_workers, args.nb_decl_byz_workers, args.aggregator_args)
        File "/home/gfursin/CK-TOOLS/tool-sysml19-aggregathor-1.0-compiler.python-3.5.3-lib.tensorflow-1.11.0-linux-64/AggregaThor/tools.py", line 305, in instantiate
          raise KeyError(cause)
      KeyError: "Unknown name '', available GAR(s): 'krum-py', 'bulyan-co', 'median', 'average-nan', 'average', 'krum-tf', 'averaged-median', 'krum-co', 'bulyan-py'"

```

You can then use any of the following plugins: 'krum-py', 'bulyan-co', 'median', 'average-nan', 'average', 'krum-tf', 
'averaged-median', 'krum-co', 'bulyan-py' (see the paper for more details):
```
$ ck run program:sysml19-aggregathor --cmd_key=local-mnist --env.AGGREGATOR=krum-py
```

Validated results for all aggregators: [Link](https://github.com/ctuning/reproduce-sysml19-paper-aggregathor/issues/4)

### MNIST-attack

CK CLI:
```
$ ck run program:sysml19-aggregathor --cmd_key=local-mnist-attack
```

Validated results for the default aggregator: [Link](https://github.com/ctuning/reproduce-sysml19-paper-aggregathor/issues/2)

We decided to create a simple CK workflow to automate execution of this program pipeline across all aggregators.
We added it as follows (to show you how to create similar automated workflows and pipelines):
```
$ ck add reproduce-sysml19-paper-aggregathor:module:workflow-sysml19-aggregathor
$ ck add_action module:workflow-sysml19-aggregathor --func=run
```

We then added the code for this workflow (see [here](https://github.com/ctuning/reproduce-sysml19-paper-aggregathor/blob/master/module/workflow-sysml19-aggregathor/module.py#L36)).

It is now possible to run this workflow from a command line as follows:
```
$ ck run workflow-sysml19-agregathor --cmd_key=local-mnist-attack
```

This workflow will create a directory 'results' in your current path, will run AgggregaThor with different aggregator plugins, and will record results (as text or in a reproducible CK format which is possible to replay).

You can find results for mnist-attack on GRID5000 [here](https://github.com/ctuning/reproduce-sysml19-paper-aggregathor/issues/5).

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

Validated results: [Link](https://github.com/ctuning/reproduce-sysml19-paper-aggregathor/issues/3)

## Distributed deployment (3 node example)

First you need to reserve nodes for 3 machines. For the sake of simplicity we called the following command 3 times on GRID5000:
```
$ oarsub -I -t allow_classic_ssh -p "cluster='paravance'" -l nodes=1
$ oarsub -I -t allow_classic_ssh -p "cluster='paravance'" -l nodes=1
$ oarsub -I -t allow_classic_ssh -p "cluster='paravance'" -l nodes=1
```

Let's say that we connected to the following nodes: paravance-8, paravance-9 and paravance-10.

We now need to describe configuration of our cluster for Aggregathor. You must create some JSON file (for example "grid5000.json"):

```
{
    "nodes": {
        "ps": [
            "paravance-8:7000"
        ],
        "workers": [
            "paravance-9:7000",
            "paravance-10:7000"
        ]
    }
}
```

Note that "ps" machine is the one where you will deploy AggregaThor via CK

Now you must register this configuration in the CK with some name such as "grid5000" as follows:
```
$ ck add machine:grid5000 --type=cluster --config_file=grid5000.json
```

When asked about remote node OS, select linux-64. You can view all registered configurations of target platforms as follows:
```
$ ck show machine
```

You can now deploy your server on the first machine as follows:
```
$ ck run program:sysml19-aggregathor --target=grid5000 --cmd_key=distributed-deploy-mnist &
```

You can then run AggregaThor in a distributed mode from the "ps" node as follows:
```
$ ck run program:sysml19-aggregathor \
  --cmd_key=distributed-mnist \
  --env.NB_WORKERS=2 \
  --env.MAX_STEP=100000 \
  --env.CHECKPOINT_PERIOD=600 \
  --env.EVALUATION_DELTA=1000 \
  --env.SUMMARY_DELTA=1000 \
  --env.BATCH_SIZE=50 \
  --target=grid5000
```

Validated results: [Link](https://github.com/ctuning/reproduce-sysml19-paper-aggregathor/issues/6)

## Suggestions

* Improve [CK post-processing plugin](https://github.com/ctuning/reproduce-sysml19-paper-aggregathor/blob/master/program/sysml19-aggregathor/postprocess.py) for AggregaThor to automatically validate correctness or results
* Add and test ImageNet [CK package](http://cKnowledge.org/shared-repos.html) compatible with AggregaThor
* Improve [Jupyter notebook](https://github.com/ctuning/reproduce-sysml19-paper-aggregathor/tree/master/jnotebook/sysml19-aggregathor) with step-by-step guide (ck run jnotebook:sysml19-aggregathor)

We expect the community to continue validating results from this and other SysML'19 papers.

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
