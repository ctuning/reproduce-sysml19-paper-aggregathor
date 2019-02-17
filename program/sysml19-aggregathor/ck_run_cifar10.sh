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

if [ -d "datasets" ]; then
  cd datasets
else
  cd slim_datasets
fi

unlink cifar10
ln -s ${CK_ENV_DATASET_TF_SLIM} cifar10

. ${cwd}/../ck_run.sh
