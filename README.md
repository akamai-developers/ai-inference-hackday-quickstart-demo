# 🚀 AI Inference Optimization: A Decision Framework Workshop 

Welcome to the **AI Inference HackDay 2026** workshop.

In this hands-on session, you'll learn how modern AI systems are built beyond a simple prompt-and-response workflow. We'll explore three key challenges faced by production AI applications:

1. **Serving models efficiently**
2. **Routing requests intelligently**
3. **Evaluating outputs automatically**

Instead of downloading models locally or configuring GPUs, you'll interact with a pre-configured **vLLM serving environment** running on an **Akamai Linode Kubernetes Engine (LKE)** cluster.

---

# 🏗️ Architecture Overview

```text
 💻 Client Application
        │
        ▼
 🌐 OpenAI-Compatible API Endpoint
        │
        ▼
 ☸️ Akamai Linode Kubernetes Engine (LKE)
        │
        ├── 📦 vLLM Engine
        ├── 📦 Model Serving Layer
        └── 🔥 NVIDIA GPU Infrastructure
```

The workshop focuses on the application and serving layers rather than infrastructure provisioning.

---

# 📂 Repository Structure

```text
ai-inference-workshop/
├── README.md
├── requirements.txt
├── v.env
│
├── demo/
│   ├── 01_bench.py
│   ├── 02_cost_aware_router.py
│   └── 03_evaluation.py
│
└── src/
    ├── client.py
    ├── config.py
    ├── inference.py
    └── routing.py
```

---

# ⚙️ Initial Setup

Install dependencies:

```bash
pip install -r requirements.txt
```
---

## 🛠️ Connectivity Smoke Test

Verify connectivity to the inference endpoint:

```bash
curl http://agentgateway:8080/v1/chat/completions \
  -H "Authorization: Bearer sk-workshop-87e36a3353f376fe98e181457244d3434a1c642e" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen3-8B-FP8",
    "messages": [
      {
        "role": "user",
        "content": "hello"
      }
    ],
    "max_tokens": 20
  }'
```

Expected output:

```json
{
  "model": "Qwen/Qwen3-8B-FP8",
  "usage": {
    "prompt_tokens": 9,
    "completion_tokens": 20,
    "total_tokens": 29
  }.....
}
```

---

# 📖 Workshop Modules

## Module 1: High-Throughput Inference (`01_bench.py`)

### Core Question

> How do we serve AI models efficiently when many users arrive simultaneously?

### Concepts Covered

* OpenAI-compatible APIs
* Streaming responses
* Time to First Token (TTFT)
* Sequential vs concurrent requests
* Throughput
* Continuous batching
* GPU utilization

### What You'll Build

A benchmark that compares:

```text
Sequential Requests
        vs
Concurrent Requests
```

to demonstrate how vLLM handles multi-user traffic efficiently.

### Run

```bash
python -m demo.01_bench
```

---

## Module 2: Cost-Aware Routing (`02_cost_aware_router.py`)

### Core Question

> Should every request use the most expensive model?

### Concepts Covered

* Model routing
* Latency vs Cost vs Quality
* Base model vs Premium model
* Request classification
* AI system design trade-offs

### What You'll Build

A lightweight routing layer that:

```text
Incoming Request
        │
        ▼
   Router Decision
        │
        ├── FAST_TRACK
        │      ▼
        │   Base Model
        │
        └── COMPLEX_ANALYSIS
               ▼
          Premium Model
```

Simple requests stay on the base model.

More complex requests are escalated to a premium reasoning model.

### Run

```bash
python -m demo.02_cost_aware_router
```

---

## Module 3: Lightweight Evaluation (`03_evaluation.py`)

### Core Question

> How do we know whether an AI response is actually good?

### Concepts Covered

* Evaluation pipelines
* LLM-as-a-Judge
* Automated quality checks
* PASS / FAIL evaluation patterns

### What You'll Build

A lightweight evaluation system:

```text
User Request
        │
        ▼
 Model Response
        │
        ▼
 Evaluator Model
        │
        ▼
   PASS / FAIL
```

This pattern is commonly used in production systems to automatically assess response quality.

### Run

```bash
python -m demo.03_evaluation
```

---

# 📊 Key Metrics

## 1. Time to First Token (TTFT)

Measures how quickly a user sees the first generated token.

Lower TTFT improves perceived responsiveness.

---

## 2. Throughput

Measures how many requests a system can handle simultaneously.

Higher throughput allows more users to be served efficiently.

---

## 3. Quality

Measures whether model outputs meet expectations.

Examples:

* Correctness
* Helpfulness
* Completeness
* Professionalism

---

# 🎯 Key Takeaways

By the end of this workshop, you will have built systems that demonstrate:

### Efficient Serving

Using vLLM to maximize throughput and GPU utilization.

### Intelligent Routing

Choosing the cheapest model that can successfully complete the task.

### Automated Evaluation

Using AI models to assess the quality of AI-generated outputs.

---


# ☁️ Next Steps: Run It Yourself on Akamai Cloud

This repo includes ready-to-use Terraform templates in the `infra/` directory that can provision a GPU-powered Linode VM with NVIDIA drivers and CUDA pre-installed.

1. Create an [Akamai Cloud account (includes $300 credits)](http://login.linode.com/signup?promo=akm-dev-git-300-31126-M055)
2. Generate an API token.
3. Copy and update `terraform.tfvars.example` with your own configuration.
4. Run Terraform to provision the GPU instance.
5. SSH into the machine and run vllm server.


**NOTE:** Choose the GPU that best fits your workload, from lightweight inference deployments to larger model-serving environments.

| Akamai VM Selection | VRAM Size | Hourly Cost | Ideal Hackathon Workload Target |
| :--- | :--- | :--- | :--- |
| **RTX 4000 Ada (Small)** | 16 GB | \$0.52 / hr | 7B or 14B open-source models running at a 4-bit quantization level. |
| **NVIDIA Quadro RTX 6000** | 24 GB | \$1.50 / hr | Unquantized 7B models at full FP16 precision or heavy embedding tasks. |
| **RTX 4000 Ada (Large)** | 64 GB | \$0.96 / hr | Large context window applications, multi-agent frameworks, batched vision tasks. |
| **RTX PRO 6000 Blackwell** | 96 GB | \$2.50 / hr | 70B scale models or specialized custom fine-tuning tasks. |


> ⚠️ **Cost Optimization Pro-Tip:** High-performance GPUs consume your credit pool continuously while active. Remember to completely **destroy/delete** your active instances if you take an extended break or finish hacking for the night to protect your remaining balance.

**Happy Hacking! 🚀**
