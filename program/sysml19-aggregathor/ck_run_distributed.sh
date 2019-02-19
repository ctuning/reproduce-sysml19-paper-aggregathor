#!/bin/bash

cd ${CK_ENV_TOOL_SYSML19_AGGREGATHOR}

echo ""
echo "Cluster configuration:"
echo ""
echo "${CLUSTER_CONFIG}"
echo ""

${CK_ENV_COMPILER_PYTHON_FILE} runner.py \
 --server "${CLUSTER_CONFIG}" \
 --ev-job-name ps \
 --experiment "${EXPERIMENT}" \
 --aggregator "${AGGREGATOR}" \
 --nb-workers ${NB_WORKERS} \
 --nb-decl-byz-workers ${NB_DECL_BYZ_WORKERS} \
 --experiment-args "batch-size:${BATCH_SIZE}" \
 --max-step ${MAX_STEP} \
 --max-steps ${MAX_STEP} \
 --learning-rate-args "${LEARNING_RATE_ARGS}" \
 --evaluation-period ${EVALUATION_PERIOD} \
 --checkpoint-period ${CHECKPOINT_PERIOD} \
 --summary-period ${SUMMARY_PERIOD} \
 --evaluation-delta ${EVALUATION_DELTA} \
 --checkpoint-delta ${CHECKPOINT_DELTA} \
 --summary-delta ${SUMMARY_DELTA} \
 --no-wait
