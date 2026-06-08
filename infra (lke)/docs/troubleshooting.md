# Troubleshooting Guide

## Student Issues

### "I can't connect to my workspace"

1. Check the pod is running:
   ```bash
   kubectl -n workshop get pod ws-XX
   ```
2. If `CrashLoopBackOff`: check logs
   ```bash
   kubectl -n workshop logs ws-XX
   ```
3. If `Pending`: check node capacity
   ```bash
   kubectl describe pod -n workshop ws-XX
   ```
4. If running but not reachable: check ingress
   ```bash
   kubectl -n workshop get ingress
   ```

### "The agent is really slow"

1. Check vLLM pod health:
   ```bash
   kubectl -n workshop exec vllm-0 -- curl -sf http://localhost:8000/health
   ```
2. Check GPU utilization:
   ```bash
   kubectl -n workshop exec vllm-0 -- nvidia-smi
   ```
3. If model not loaded (no GPU memory used): restart the pod
   ```bash
   kubectl -n workshop rollout restart statefulset/vllm
   ```

### "Tool calls fail"

1. Check nba-stats-mcp is installed:
   ```bash
   kubectl -n workshop exec ws-XX -- .venv/bin/which nba-stats-mcp
   ```
2. Check internet connectivity:
   ```bash
   kubectl -n workshop exec ws-XX -- curl -sf https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json | head -c 100
   ```

### "Student is stuck"

Point them to the solutions folder:
```
python workshop/solutions/01_first_agent_done.py
python workshop/solutions/02_add_tools_done.py
# etc.
```

## Infrastructure Issues

### vLLM pods won't start

1. Check GPU node availability:
   ```bash
   kubectl get nodes -l nvidia.com/gpu
   ```
2. Check pod events:
   ```bash
   kubectl -n workshop describe statefulset vllm
   ```
3. Common cause: GPU nodes not yet provisioned (takes 5-10 min on Linode)

### Workspace pods stuck in Pending

1. Check CPU node capacity:
   ```bash
   kubectl describe nodes | grep -A 5 "Allocated resources"
   ```
2. If out of capacity: reduce workspace count or add CPU nodes

### Ingress not routing

1. Check ingress controller is running:
   ```bash
   kubectl get pods -n ingress-nginx
   ```
2. Check ingress rules:
   ```bash
   kubectl -n workshop describe ingress workshop-ingress
   ```

### Model download slow

The Qwen3.5-9B-FP8 model is ~10GB. First download takes 5-10 minutes per pod. Run `provision.sh` at T-24h to ensure models are cached.
