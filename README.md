# 🚀 High-Throughput LLM Inference Workshop

Welcome to the **AI Inference HackDay 2026** core workshop workspace. 

This hands-on session bypasses local setup friction to dive straight into the mechanics of production-grade AI infrastructure. Instead of waiting for models to download or struggle with local GPU configurations, you will interact directly with a pre-configured, high-performance **vLLM serving engine** hosted on an **Akamai Linode Kubernetes Engine (LKE)** cluster.

---

## 🏗️ Topology Architecture

Your client environment acts as a lightweight consumption layer. The massive parameter weights and high-compute scheduling architectures are entirely abstracted into the cloud infrastructure layer:

```text
 💻 Hacker Laptop (Client Machine)
        │
        │ [ Port 8000 / HTTP REST API ]
        ▼
 🌐 Akamai Linode Load Balancer 
        │
        ▼
 ☸️ Linode Kubernetes Engine (LKE) Cluster
        │
        ├── 📦 Pod 1: vLLM Engine ── 🔥 NVIDIA GPU (Meta-Llama-3-8B-Instruct)
        └── 📦 Pod 2: vLLM Engine ── 🔥 NVIDIA GPU (Meta-Llama-3-8B-Instruct)
```

## ⏱️ Workshop Agenda (45 Minutes)

*   **00:00 - 00:05** | Environment Check & Cluster Connectivity
*   **00:05 - 00:15** | **Module 1:** The Infrastructure Layer (`01_bench.py`)
*   **00:15 - 00:27** | **Module 2:** The Architectural Layer (`02_router_demo.py`)
*   **00:27 - 00:40** | **Module 3:** The Production/Ops Layer (`03_resilient.py`)
*   **00:40 - 00:45** | Q&A & Hackathon Project Ideation

---

## 📂 Repository Structure & Workshop Flow

```text
ai-inference-hackday-quickstart-demo/
├── README.md                
├── requirements.txt           
├── .env.example
├── infra/                  
│   ├── vm/
│   └── lke/             
│       ├── terraform             
│       ├── scripts           
│       └── manifests          
└── demo/                 
    ├── 01_bench.py     
    ├── 02_router_demo.py     
    ├── 03_resilient demo/
└──src/
   ├── config.py     -> reads env vars
   ├── clients.py    -> creates API clients
   ├── inference.py  -> calls model
   ├── router.py     -> classifies intent
   └── resilience.py -> timing/TTFT helpers
```

## Initial Application Setup

Set environment variables in your terminal before running the modules:

```bash
export AKAMAI_INFERENCE_URL="http://YOUR_ENDPOINT:8000/v1/chat/completions"
export BASE_MODEL="meta-llama/Llama-3-8B-Instruct"
export LARGE_MODEL="gpt-4o-mini"
```

Install dependencies:
```bash
pip install -r requirements.txt
```


## 🛠️ Quick Sandbox Smoke Test

Before running the Python scripts, run this quick terminal smoke test to verify your laptop can successfully pierce the cluster firewall and communicate with the vLLM engine:

```bash
curl http://YOUR-SHARED-SANDBOX-IP:8000/v1/models \
  -H "Authorization: Bearer akamai-hackathon-2026-token"
```

Expected Response: A clean JSON object listing meta-llama/Llama-3-8B-Instruct. If you receive a connection timeout, double-check your cluster endpoint IP or alert a workshop mentor.


## ⏱️ Interactive Playbook: How to Run the Modules

Every script is fully configured to execute directly from your terminal. Run them sequentially as we advance through the presentation slides.

### Module 1: The Raw Infrastructure Benchmark (`01_bench.py`)
* **Core Concepts:** Time-to-First-Token (TTFT), Continuous Batching, PagedAttention, VRAM overhead.
* **What it does:** Simulates 4 concurrent hacker requests hitting the shared Akamai LKE cluster simultaneously. It captures token streaming to isolate exactly how vLLM optimizes throughput at the iteration level rather than making requests queue up sequentially.

```bash
python modules/01_bench.py
```

### Module 2: The Intent Router (`02_router_demo.py`)
* **Core Concepts:** Deployment Trade-offs (Latency vs. Cost vs. Quality), LLM-based Routing Systems.
* **What it does:** Demonstrates how to build a dynamic routing layer. Simple tasks (like password resets) are processed instantly and for free on the local Akamai Llama-3-8B cluster. Complex tasks (like code stack traces) are automatically escalated to a larger, premium reasoning engine.

```bash
python modules/02_router_demo.py
```

### Module 3: The Resilient Engine (`03_resilient.py`)
* **Core Concepts:** Circuit Breakers, Graceful Degradation, LLM-as-a-Judge Evaluations.
* **What it does:** Implements production-grade reliability guards. You will intentionally break the connection to the primary cluster live during the workshop to watch the application instantly failover to a backup cloud provider. It then triggers a lightweight background evaluation to grade the quality of the response.

```bash
python modules/03_resilient.py
```

---

## 📊 The 3 Operational AI KPIs to Watch
When building your weekend hackathon entries, move past standard server uptime and monitor your AI Operations Suite:

* **Time to First Token (TTFT):** Measures input processing efficiency. Use context optimization and streaming to keep this under 200ms.

* **Tokens Per Second Per User:** Measures throughput speed. Maximize this via production runtime engines utilizing continuous batching.

* **KV Cache Utilization:** Measures available GPU memory headroom. Protect this using a semantic cache and strict input traffic queues.

---

## 📊 Core Concepts Cheat Sheet

### 1. The VRAM Formula (The Hard Constraint)
Your AI model must fit entirely inside your GPU's video memory (VRAM). Use this formula to calculate your base storage requirements before provisioning hardware:

$$\text{Model Weights Size (GB)} \approx \frac{\text{Parameter Count (in Billions)} \times \text{Precision (in bits)}}{8}$$

* **The 25% Rule:** Always add 20-30% extra VRAM headroom on top of your model weight size to accommodate system software overhead and the KV Cache (conversation history).

### 2. Akamai GPU Virtual Machine Matrix
Use your **\$300 hackathon credits** to spin up one of these dedicated compute options within your private account dashboard:

| Akamai VM Selection | VRAM Size | Hourly Cost | Ideal Hackathon Workload Target |
| :--- | :--- | :--- | :--- |
| **RTX 4000 Ada (Small)** | 16 GB | \$0.52 / hr | 7B or 14B open-source models running at a 4-bit quantization level. |
| **NVIDIA Quadro RTX 6000** | 24 GB | \$1.50 / hr | Unquantized 7B models at full FP16 precision or heavy embedding tasks. |
| **RTX 4000 Ada (Large)** | 64 GB | \$0.96 / hr | Large context window applications, multi-agent frameworks, batched vision tasks. |
| **RTX PRO 6000 Blackwell** | 96 GB | \$2.50 / hr | 70B scale models or specialized custom fine-tuning tasks. |

> ⚠️ **Cost Optimization Pro-Tip:** High-performance GPUs consume your credit pool continuously while active. Remember to completely **destroy/delete** your active instances if you take an extended break or finish hacking for the night to protect your remaining balance.

---

## 🛠️ Essential Cloud Terminal Troubleshooting Commands

When managing your private Akamai Linux server compute workspace via SSH, keep these three foundational diagnostic utilities documented:

1. **Inspect Real-Time VRAM Space Allocations:**
```bash
   nvidia-smi
   ```
*Instantly reveals how much total hardware memory your model weights consume, alongside active system execution processes.*

2. **Continuously Monitor Active Memory Changes:**
```bash
   watch -n 1 nvidia-smi
   ```
   *Refreshes your hardware console metrics every single second, allowing you to watch context memory capacity adapt as complex user data streams in.*

3. **Force-Purge Stalled Memory Processes:**
```bash
   sudo killall python3
   ```
   *If your software system throws an unhandled Out-of-Memory (OOM) exception freeze, running this instantly clears stuck application frameworks without forcing a complete system restart.*

---
**Happy Hacking!** 🚀