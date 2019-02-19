#!/bin/bash

cd ${CK_ENV_TOOL_SYSML19_AGGREGATHOR}

${CK_ENV_COMPILER_PYTHON_FILE} runner.py \
 --server '{"local": ["127.0.0.1:7000"]}' \
 --ps-job-name ${PS_JOB_NAME} \
 --wk-job-name ${WK_JOB_NAME} \
 --ev-job-name ${EV_JOB_NAME} \
 --experiment "${EXPERIMENT}" \
 --learning-rate-args "${LEARNING_RATE_ARGS}" \
 --aggregator "${AGGREGATOR}" \
 --nb-workers ${NB_WORKERS} \
 --max-step ${MAX_STEP} \
 --max-steps ${MAX_STEP} \
 --evaluation-period ${EVALUATION_PERIOD} \
 --checkpoint-period ${CHECKPOINT_PERIOD} \
 --summary-period ${SUMMARY_PERIOD} \
 --evaluation-delta ${EVALUATION_DELTA} \
 --checkpoint-delta ${CHECKPOINT_DELTA} \
 --summary-delta ${SUMMARY_DELTA} \
 --reuse-gpu \
 --no-wait
