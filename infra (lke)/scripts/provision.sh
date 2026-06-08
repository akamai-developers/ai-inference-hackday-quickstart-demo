#!/usr/bin/env bash
set -euo pipefail

# Provision the AI Agents Workshop infrastructure on LKE.
# Idempotent — safe to run multiple times.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INFRA_DIR="$(dirname "$SCRIPT_DIR")"
KUBECONFIG_PATH="${INFRA_DIR}/kubeconfig.yaml"

echo "=== AI Agents Workshop — Provisioning ==="
echo ""

# Step 1: Terraform — cluster + operators + DNS + ingress LB
echo "--- Step 1: Terraform (LKE + gpu-operator + ingress-nginx + cloud-firewall + DNS) ---"
cd "${INFRA_DIR}/terraform"

if [ ! -f terraform.tfvars ] && [ -z "${TF_VAR_token:-}" ]; then
    echo "ERROR: Set TF_VAR_token or create terraform/terraform.tfvars (see terraform.tfvars.example)"
    exit 1
fi

terraform init -upgrade
terraform apply -auto-approve

# Step 2: Kubeconfig
echo ""
echo "--- Step 2: Export kubeconfig ---"
terraform output -raw kubeconfig | base64 -d > "${KUBECONFIG_PATH}"
export KUBECONFIG="${KUBECONFIG_PATH}"
echo "Kubeconfig written to ${KUBECONFIG_PATH}"

LB_IP=$(terraform output -raw ingress_lb_ip)
BASE_HOST=$(terraform output -raw workshop_base_url)
echo "Ingress LB: ${LB_IP}"
echo "Base host:  ${BASE_HOST}  (DNS *.${BASE_HOST} → ${LB_IP})"

# Step 3: Wait for GPU operator to expose nvidia.com/gpu
echo ""
echo "--- Step 3: Wait for GPU operator to expose GPUs ---"
echo "    (gpu-operator installs drivers + device plugin; 3-5 min)"
for i in $(seq 1 60); do
    GPU_NODES=$(kubectl get nodes -o json | python3 -c "import sys,json; d=json.load(sys.stdin); print(sum(1 for n in d['items'] if int(n['status']['allocatable'].get('nvidia.com/gpu', '0')) > 0))" 2>/dev/null || echo "0")
    if [ "${GPU_NODES}" -ge 1 ]; then
        echo "  ✓ ${GPU_NODES} node(s) report nvidia.com/gpu"
        break
    fi
    echo "  …waiting (${i}/60) — GPU nodes ready: ${GPU_NODES}"
    sleep 15
done

if [ "${GPU_NODES:-0}" -lt 1 ]; then
    echo "ERROR: No nodes report nvidia.com/gpu after 15 min."
    echo "  kubectl -n gpu-operator get pods   # inspect operator pods"
    exit 1
fi

# Step 4: Apply base manifests
echo ""
echo "--- Step 4: Apply base manifests ---"
cd "${INFRA_DIR}"
kubectl apply -f manifests/namespace.yaml
kubectl apply -f manifests/networkpolicy.yaml

if [ -f manifests/secret.yaml ]; then
    kubectl apply -f manifests/secret.yaml
else
    echo "  (no manifests/secret.yaml — skipping; the chosen model is ungated)"
fi

kubectl apply -f manifests/vllm-service.yaml
kubectl apply -f manifests/vllm-statefulset.yaml

# Step 5: Wait for vLLM
echo ""
echo "--- Step 5: Waiting for vLLM pods to be ready ---"
echo "    (First start: 5-10 min while each replica downloads the model to its PVC)"
kubectl -n workshop rollout status statefulset/vllm --timeout=900s

# Step 6: Issue wildcard TLS cert
echo ""
echo "--- Step 6: Issue wildcard TLS cert ---"
if kubectl -n workshop get secret workshop-tls >/dev/null 2>&1; then
    echo "  ✓ workshop-tls already exists; skipping (re-issue with ./scripts/issue-cert.sh)"
else
    if ! command -v lego >/dev/null 2>&1; then
        echo "  ! lego not installed. Run later: brew install lego && ./scripts/issue-cert.sh"
    else
        "${SCRIPT_DIR}/issue-cert.sh" || echo "  ! cert issuance failed; re-run ./scripts/issue-cert.sh"
    fi
fi

echo ""
echo "=== Base cluster ready! ==="
echo ""
echo "Next steps:"
echo "  1. ./scripts/build-image.sh                    # build + push workspace image"
echo "  2. ./scripts/generate-pods.sh -n 80 --host ${BASE_HOST}"
echo "  3. kubectl apply -f manifests/generated/"
echo "  4. ./scripts/health-check.sh"
echo "  5. ./scripts/load-test.sh                      # validate throughput"
echo ""
echo "KUBECONFIG=${KUBECONFIG_PATH}"
