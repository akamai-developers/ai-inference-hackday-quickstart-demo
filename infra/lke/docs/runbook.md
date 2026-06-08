# Workshop Day Runbook

## Timeline

### T-24h: Provision Infrastructure

```bash
# Set Linode API token
export TF_VAR_token="your-linode-api-token"

# Provision cluster
./scripts/provision.sh
```

Expected: LKE cluster with 3 CPU nodes + 5 GPU nodes. vLLM pods downloading the model.

### T-12h: Pre-warm and Validate

```bash
# Ensure models are loaded
./scripts/pre-warm.sh

# Full health check
./scripts/health-check.sh
```

Expected: All vLLM pods healthy, test inference succeeds.

### T-2h: Generate Student Workspaces

```bash
# Generate 80 workspace pods
./scripts/generate-pods.sh -n 80 --host workshop.example.com

# Deploy workspaces
kubectl apply -f manifests/generated/workspace-secrets.yaml
kubectl apply -f manifests/generated/workspace-manifests.yaml
kubectl apply -f manifests/generated/ingress.yaml
```

Expected: 80 pods starting, each with unique password.

Re-running `generate-pods.sh` is idempotent by default — existing passwords in `access-cards.csv` are preserved, and bumping `-n` only mints passwords for the new students. Pass `--rotate` to mint fresh passwords for everyone (e.g., between cohorts); the previous CSV is archived to `access-cards.csv.bak`.

### T-1h: Final Validation

```bash
# Full health check including workspaces
./scripts/health-check.sh
```

Expected: All checks green.

### T-30m: Manual Smoke Test

1. Open `https://workshop.example.com/s01/` in a browser
2. Enter the password from access-cards.csv
3. Run all workshop modules manually:
   ```
   python demo/01_bench.py
   python demo/02_intent_router.py
   python demp/03_resilient.py
   ```
4. Confirm colored output, tool calls work, LLM responds

### T-15m: Distribute Access Cards

```bash
# Generate printable cards
./scripts/print-access-cards.sh

# Open in browser and print
open manifests/generated/access-cards.html
```

DA distributes printed cards to students.

### T-5m: QR Code on Projector

Display the workshop URL QR code. Students start connecting.

### T+0: Workshop Begins

Sheilah follows the docs/ guide. Students run scripts in order.

### T+60m: Teardown

```bash
./scripts/teardown.sh
```

All resources destroyed. Workshop complete.

## Emergency Procedures

| Scenario | Action |
|----------|--------|
| vLLM pod crash | `kubectl -n workshop rollout restart statefulset/vllm` |
| Student can't connect | Check pod status: `kubectl -n workshop get pod ws-XX` |
| All workspaces down | Check CPU nodes: `kubectl get nodes` |
| Total infra failure | Fallback: Du'An demos from laptop with Ollama |
