#!/bin/bash

cwd=$(pwd)

# Linking CIFAR from other packages to AggregaThor

cd ${CK_ENV_TOOL_SYSML19_AGGREGATHOR}

pwd

cd experiments
unlink slim_package
ln -s ${CK_ENV_TENSORFLOW_MODELS}/slim slim_package
unlink slim
ln -s ${CK_ENV_TENSORFLOW_MODELS}/slim slim

cd datasets
unlink cifar10
ln -s ${CK_ENV_DATASET_IMAGENET_TRAIN_TF} cifar10

. ${cwd}/../ck_run.sh
