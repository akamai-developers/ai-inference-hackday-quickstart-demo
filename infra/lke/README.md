# AI Inference Hackday Workshop — Infrastructure

Terraform + Kubernetes infrastructure for running the workshop on Akamai Cloud (Linode).

## Architecture

```
Student Browser
    │ HTTPS (wildcard cert *.workshop.burnersite.xyz)
    ▼
NodeBalancer  (public IP, 80/443)
    │
    ▼
ingress-nginx Controller (subdomain routing)
    ├── s01.workshop.burnersite.xyz → ws-01 pod  (code-server, per-student password)
    ├── s02.workshop.burnersite.xyz → ws-02 pod
    │   ...
    └── s80.workshop.burnersite.xyz → ws-80 pod
         │
         └── http://vllm:8000/v1 → vLLM StatefulSet (Qwen3-8B-FP8)

LKE Cluster
    ├── CPU Pool  (5x g6-dedicated-8 — 16GB, 8 vCPU)
    │   └── 80x workspace pods + ingress-nginx + system pods
    │
    └── GPU Pool  (5x g2-gpu-rtx4000a4-s — 4× RTX 4000 Ada per node, 20GB VRAM each)
        └── 5x vLLM replicas, each one spans 4 GPUs via tensor parallelism
              (--tensor-parallel-size=4), and has its own 50Gi PVC for model
              cache (StatefulSet + volumeClaimTemplates).
```

Cluster-level: `gpu-operator` (NVIDIA drivers + device plugin),
`cloud-firewall-controller` (worker node firewall),
`ingress-nginx`, NetworkPolicy (default-deny + explicit allow rules).

## Prerequisites

- [Terraform](https://terraform.io) >= 1.5
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Docker](https://docker.com) (for building the workspace image)
- [lego](https://go-acme.github.io/lego/) — `brew install lego` (for wildcard TLS via Linode DNS-01)
- [Linode API token](https://cloud.linode.com/profile/tokens) (full access, scoped to your account)
- [GitHub PAT](https://github.com/settings/tokens) — **classic** PAT (fine-grained tokens have known issues with ghcr.io), scopes: `write:packages`, `read:packages`, `delete:packages`
- A domain managed in Linode DNS (default: `burnersite.xyz`)

## Quick Start

```bash
# 1. Set API token (must have Domains: Read/Write, Linodes, NodeBalancers, Kubernetes, Volumes scopes)
export TF_VAR_token="your-linode-api-token"

# 2. Log docker into ghcr.io
echo "<your-github-pat>" | docker login ghcr.io -u <your-github-username> --password-stdin

# 3. Provision cluster + vLLM + DNS (~20-25 min)
./scripts/provision.sh

# 4. Issue wildcard TLS cert (~1-2 min, idempotent — safe to re-run)
./scripts/issue-cert.sh
kubectl -n workshop get secret workshop-tls   # confirm it exists

# 5. Build + push workspace image (~5 min)
export REGISTRY=ghcr.io/<your-github-username-or-org>   # script default is akamai-developers
./scripts/build-image.sh

# After first push, set the package to PUBLIC so the cluster can pull without auth:
#   https://github.com/users/<you>/packages/container/ai-agents-workspace/settings
#   (Change visibility → Public)
# Or set up an imagePullSecret in the workshop namespace if you need it private.

# 6. Generate ONE student workspace to verify end-to-end
./scripts/generate-pods.sh -n 1 --host workshop.burnersite.xyz
kubectl apply -f manifests/generated/
cat manifests/generated/access-cards.csv     # URL + password for s01

# 7. Validate (open https://s01.workshop.burnersite.xyz in a browser, log in, run 00_verify.py)
./scripts/health-check.sh

# 8. Scale to 80 once s01 works end-to-end. generate-pods.sh is idempotent:
#    s01's password is preserved, and only s02–s80 get newly minted passwords.
./scripts/generate-pods.sh -n 80 --host workshop.burnersite.xyz
kubectl apply -f manifests/generated/

# 9. Print access cards
./scripts/print-access-cards.sh

# 10. Load-test inference layer (optional)
./scripts/load-test.sh
```

### About the TLS cert (step 4)

`./scripts/issue-cert.sh` uses [lego](https://go-acme.github.io/lego/) + Linode DNS-01 to issue a wildcard Let's Encrypt cert for `*.workshop.burnersite.xyz`, then stores it as the `workshop-tls` K8s Secret. The Ingress (generated in step 6) references that Secret.

- **Idempotent**: re-run any time. If a cert exists locally in `.certs/`, lego will renew if near expiry, otherwise skip.
- **Token source order**: `LINODE_TOKEN` env → `TF_VAR_token` env → `terraform/terraform.tfvars`.
- **Required scopes on the token**: `Domains: Read/Write`. The script validates this before calling lego.
- **`provision.sh` also tries to call this** at its final step, but as best-effort — if lego isn't installed, or the token lacks DNS scope, it logs a warning and continues. **Always confirm the secret exists** with `kubectl get secret workshop-tls -n workshop` before applying the Ingress.
- **Renewal**: cert is valid 90 days. Re-run `./scripts/issue-cert.sh` to renew.

## Cost Estimate

Linode list pricing, US-Ord region, May 2026:

| Resource | Plan | Count | $/hr | $/4hr workshop |
|----------|------|-------|------|----------------|
| CPU Nodes | g6-dedicated-8 (16GB) | 5 | $0.216 | $4.32 |
| GPU Nodes | g2-gpu-rtx4000a4-s (4× RTX 4000 Ada, 20GB each) | 5 | $2.94 | $58.72 |
| NodeBalancer | Standard | 1 | $0.015 | $0.06 |
| Block Storage | 50Gi × 5 PVCs | — | — | ~$0.07 |
| **Total** | | | | **~$63** |

(For tighter budgets, drop `gpu_node_type` to `g2-gpu-rtx4000a1-s` and set `--tensor-parallel-size=1` — 5 GPUs instead of 20, ~$15/4hr. Median latency rises from ~11s to ~11s but p99 rises from ~14s to ~42s under burst load — see `infra/docs/runbook.md`.)

Run `./scripts/teardown.sh` immediately after the workshop to stop billing.

## Mid-workshop Operations

Common operations once the cluster is up. None of these require a full teardown.

### Regenerate manifests after editing the pod template

`workspace-pod-template.yaml` is the source for every student pod. After editing it (or `vllm-statefulset.yaml`, or any other config), re-emit and re-apply:

```bash
./scripts/generate-pods.sh -n 80 --host workshop.burnersite.xyz   # passwords preserved
kubectl apply -f manifests/generated/
```

Re-running `generate-pods.sh` is idempotent: existing passwords in `access-cards.csv` are preserved and only new students (if `-n` grew) get fresh passwords. To force-rotate all passwords (e.g., between cohorts) pass `--rotate`; the previous CSV is archived to `access-cards.csv.bak`. To trim below the current count pass `--shrink`. Changing `--host` requires `--rotate`.

### Restart a single workspace pod

If one student's environment gets wedged. Bare Pods aren't managed by a Deployment, so `delete pod` is permanent — re-applying the manifest recreates it (existing pods are no-ops):

```bash
kubectl -n workshop delete pod ws-NN
kubectl apply -f manifests/generated/workspace-manifests.yaml
```

### Reset a single student's password

`generate-pods.sh` is all-or-nothing (no per-student rotate flag, by design). To reset one student manually:

```bash
NEW=$(openssl rand -hex 16)
kubectl -n workshop create secret generic ws-NN-password \
  --from-literal=password="${NEW}" \
  --dry-run=client -o yaml | kubectl apply -f -
kubectl -n workshop delete pod ws-NN                              # pick up the new secret
kubectl apply -f manifests/generated/workspace-manifests.yaml     # recreate
echo "sNN,https://sNN.workshop.burnersite.xyz/,${NEW}"            # hand-edit access-cards.csv
```

### Restart vLLM

```bash
kubectl -n workshop rollout restart statefulset/vllm
```

### Delete all workspaces, keep the cluster + vLLM + cert

For an unplanned reset mid-workshop, or to recycle the cluster between cohorts without paying the 20-minute provision tax again:

```bash
kubectl delete -f manifests/generated/workspace-manifests.yaml
kubectl delete -f manifests/generated/workspace-secrets.yaml
kubectl delete -f manifests/generated/ingress.yaml
# Optionally also: rm manifests/generated/access-cards.csv  (keeps a .bak around)
```

LKE, GPU pool, NodeBalancer, vLLM, and the TLS Secret are all untouched. Re-run `generate-pods.sh` (with `--rotate` for fresh passwords) and `kubectl apply -f manifests/generated/` to bring workspaces back.

### Full teardown

```bash
./scripts/teardown.sh
```

Destroys the LKE cluster, GPU pool, NodeBalancer, PVCs, and the `manifests/generated/` directory. Use this after the workshop ends — billing keeps running otherwise.

## Security Model

- **Namespace PodSecurity**: `baseline` enforced, `restricted` warn/audit
- **NetworkPolicy**: default-deny ingress; explicit allow `ingress-nginx → workspaces:8080`
  and `workspaces → vllm:8000`; everything else blocked
- **Workspace pods**: non-root (UID 1000), no privilege escalation, all capabilities dropped, `seccomp=RuntimeDefault`
- **TLS**: wildcard Let's Encrypt cert (`*.workshop.<domain>`) via lego + Linode DNS-01
- **Worker node firewall**: managed by `cloud-firewall-controller` — blocks NodePort range from internet
- **vLLM is internal-only**: ClusterIP service, never exposed publicly. No API key needed; NetworkPolicy is the perimeter.
- **Unique per-student passwords**: 128-bit random hex (32 chars) generated by `generate-pods.sh`, one per workspace, stored as K8s Secrets, mounted as `PASSWORD` env var
- **Cluster destroyed after workshop** via `teardown.sh`

## File Structure

```
infra/
├── terraform/
│   ├── main.tf                # LKE + GPU pool + helm releases + DNS records
│   ├── variables.tf
│   ├── outputs.tf
│   ├── versions.tf            # Provider pinning
│   └── terraform.tfvars.example
├── manifests/
│   ├── namespace.yaml         # workshop ns with PSS baseline enforcement
│   ├── networkpolicy.yaml     # default-deny + 3 allow rules
│   ├── secret.example.yaml    # template for vllm-secrets (HF_TOKEN)
│   ├── vllm-statefulset.yaml  # 5 replicas (TP=4 each), per-pod 50Gi PVC, FP8 model, vllm/vllm-openai:v0.20.2
│   ├── vllm-service.yaml      # ClusterIP, internal only
│   ├── workspace-pod-template.yaml  # consumed by generate-pods.sh
│   ├── load-test-job.yaml     # in-cluster benchmark_serving.py runner
│   └── generated/             # output of generate-pods.sh (gitignored)
├── images/
│   └── workspace/Dockerfile   # code-server + python + workshop content
├── scripts/
│   ├── provision.sh           # one-shot: terraform → vllm → cert
│   ├── teardown.sh            # one-shot: PVCs → ns → terraform destroy
│   ├── build-image.sh         # docker build + push workspace image
│   ├── issue-cert.sh          # wildcard TLS via lego + Linode DNS
│   ├── generate-pods.sh       # emit N student workspaces (pods + svc + ingress); idempotent re-run preserves passwords
│   ├── print-access-cards.sh  # printable HTML from access-cards.csv
│   ├── health-check.sh        # end-to-end smoke test
│   ├── pre-warm.sh            # touch each vLLM replica to load CUDA graphs
│   └── load-test.sh           # launch in-cluster load-test job
└── docs/
    ├── runbook.md
    ├── security.md
    └── troubleshooting.md
```

## What Terraform actually provisions

Single `terraform apply` from `terraform/`:

| Resource | Purpose |
|---|---|
| `linode_lke_cluster.workshop` | LKE control plane + inline CPU pool |
| `linode_lke_node_pool.gpu` | Separate GPU pool with `pool=gpu` label |
| `linode_firewall.ingress` | Optional firewall for the LB (not attached by default — see comment in main.tf) |
| `helm_release.cloud_firewall_crd` + `cloud_firewall_controller` | Per-node firewalls on workers |
| `helm_release.gpu_operator` | NVIDIA drivers + device plugin DaemonSets |
| `helm_release.ingress_nginx` | ingress-nginx controller + NodeBalancer |
| `data.kubernetes_service.ingress_lb` | Reads the LB's public IP for DNS records |
| `linode_domain_record.workshop_wildcard` | `*.workshop.<domain>` → LB IP |
| `linode_domain_record.workshop_apex` | `workshop.<domain>` → LB IP |

## Documentation

- [Runbook](docs/runbook.md) — Day-of checklist
- [Security](docs/security.md) — Threat model + controls
- [Troubleshooting](docs/troubleshooting.md) — Common issues
