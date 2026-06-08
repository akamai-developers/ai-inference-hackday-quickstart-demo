#!/usr/bin/env bash
set -euo pipefail

# Run an in-cluster load test against the vllm Service.
# Usage:
#   ./load-test.sh                        # 200 prompts, 80 concurrent, full blast
#   ./load-test.sh -n 500 -c 80           # 500 prompts at 80 concurrent
#   ./load-test.sh -n 200 -c 40 -r 20     # 200 prompts at 40 concurrent, 20 req/s

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INFRA_DIR="$(dirname "$SCRIPT_DIR")"
KUBECONFIG_PATH="${INFRA_DIR}/kubeconfig.yaml"
JOB_MANIFEST="${INFRA_DIR}/manifests/load-test-job.yaml"

NUM_PROMPTS=200
MAX_CONCURRENCY=80
REQUEST_RATE="inf"

while [[ $# -gt 0 ]]; do
    case $1 in
        -n|--num-prompts) NUM_PROMPTS="$2"; shift 2 ;;
        -c|--concurrency) MAX_CONCURRENCY="$2"; shift 2 ;;
        -r|--request-rate) REQUEST_RATE="$2"; shift 2 ;;
        -h|--help)
            echo "Usage: $0 [-n NUM_PROMPTS] [-c MAX_CONCURRENCY] [-r REQUEST_RATE]"
            echo "  -n  Total prompts to send (default 200)"
            echo "  -c  Max concurrent in-flight requests (default 80)"
            echo "  -r  Sustained req/s, or 'inf' for full blast (default inf)"
            exit 0
            ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

if [ -f "${KUBECONFIG_PATH}" ]; then
    export KUBECONFIG="${KUBECONFIG_PATH}"
fi

echo "=== Load test: ${NUM_PROMPTS} prompts, ${MAX_CONCURRENCY} concurrent, rate=${REQUEST_RATE} ==="
echo ""

# Clean up any prior job so we can re-run.
kubectl -n workshop delete job vllm-load-test --ignore-not-found

# Apply the Job, overriding env vars via kubectl set.
kubectl apply -f "${JOB_MANIFEST}"
kubectl -n workshop set env job/vllm-load-test \
    NUM_PROMPTS="${NUM_PROMPTS}" \
    MAX_CONCURRENCY="${MAX_CONCURRENCY}" \
    REQUEST_RATE="${REQUEST_RATE}"

echo "Waiting for pod…"
kubectl -n workshop wait --for=condition=Ready pod -l app=load-test --timeout=120s 2>/dev/null || true

# Stream logs until completion.
POD=$(kubectl -n workshop get pods -l app=load-test -o jsonpath='{.items[0].metadata.name}')
echo "Streaming logs from ${POD} (Ctrl-C to detach, job continues running)…"
echo ""
kubectl -n workshop logs -f "${POD}"

echo ""
echo "=== Done. Job status ==="
kubectl -n workshop get job vllm-load-test
