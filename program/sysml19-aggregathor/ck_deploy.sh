#!/bin/bash

# Hack: copy our modified deploy with PYTHONPATH set via CK
cp -f ../deploy.py ${CK_ENV_TOOL_SYSML19_AGGREGATHOR}

cd ${CK_ENV_TOOL_SYSML19_AGGREGATHOR}

echo ""
echo "Cluster configuration:"
echo ""
echo "${CLUSTER_CONFIG}"
echo ""

${CK_ENV_COMPILER_PYTHON_FILE} deploy.py \
 --cluster "${CLUSTER_CONFIG}" \
 --deploy \
 --id ps:0 \
 --omit 
