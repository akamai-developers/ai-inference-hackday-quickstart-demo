#!/usr/bin/env bash
set -euo pipefail

# Tear down all workshop infrastructure. Destructive.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INFRA_DIR="$(dirname "$SCRIPT_DIR")"
KUBECONFIG_PATH="${INFRA_DIR}/kubeconfig.yaml"

echo "=== AI Agents Workshop — Teardown ==="
echo ""
echo "WARNING: This will destroy ALL workshop infrastructure, including PVCs."
read -p "Continue? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "Aborted."
    exit 0
fi

# Step 1: K8s cleanup (best-effort)
if [ -f "${KUBECONFIG_PATH}" ]; then
    export KUBECONFIG="${KUBECONFIG_PATH}"

    echo ""
    echo "--- Step 1: Delete Kubernetes resources ---"
    # Delete StatefulSet first so PVCs can be cleaned up explicitly.
    kubectl -n workshop delete statefulset vllm --ignore-not-found --timeout=120s || true
    # StatefulSet does not delete its PVCs by default; remove them explicitly.
    kubectl -n workshop delete pvc --all --ignore-not-found --timeout=120s -n workshop || true
    kubectl delete namespace workshop --ignore-not-found --timeout=120s || true
else
    echo "No kubeconfig found — skipping K8s cleanup"
fi

# Step 2: Terraform destroy
echo ""
echo "--- Step 2: Terraform destroy ---"
cd "${INFRA_DIR}/terraform"
terraform destroy -auto-approve

# Local cleanup
rm -f "${KUBECONFIG_PATH}"
rm -rf "${INFRA_DIR}/manifests/generated"

echo ""
echo "=== All resources destroyed. ==="
