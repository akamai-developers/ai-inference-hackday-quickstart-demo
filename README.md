# Enterprise AI Inference Gateway

Welcome to the **AI Inference HackDay 2026** core workshop workspace. 

This repository functions as a fully instrumented, production-grade **AI Inference Gateway**. An Inference Gateway acts as an intelligent, defensive proxy layer sitting directly between your front-end client applications and underlying high-performance GPU infrastructure (powered by `vLLM` and `Ollama`). 

Instead of treating Large Language Models like standard web APIs, this project demonstrates how to architect for the core bottlenecks of AI workloads: **Memory Capacity, Bandwidth, Latency (TTFT), and Hardware Costs.**

---

## 🏗️ Gateway Architecture Overview
```text
                  [ FRONTEND USER REQUEST ]
                              │
                              ▼
┌─────────────────────── AI GATEWAY ───────────────────────┐
│                                                          │
│  [Module 3]  👉  Semantic Cache Lookup                   │──(Hit)──► [ Return 5ms Response ]
│                              │ (Miss)                    │
│                              ▼                           │
│  [Module 4]  👉  Tiered Escalation Router                │
│                              │                           │
│             (Conversational) │  (Complex / Bloated RAG)  │
│                    ▼         │           ▼               │
│             [ 1B Edge Worker ]      [ 8B vLLM Cluster ]  │
│                                              │           │
│  [Module 5]  👉                      Asynchronous Queue  │
│                                              │           │
│  [Module 5]  👉                   Structured Validation  │
│                                              │           │
│  [Module 5]  👉                   Streaming Telemetry    │
│                                              │           │
└──────────────────────────────────────────────╪───────────┘
                                               │ (If Crash / Rate Limit)
                                               ▼
                                   [ Circuit Breaker Fallback ]
```



## 📂 Repository Structure & Workshop Flow

The workspace is split into core architectural machinery (`src/`) and isolated, runnable modular lessons (`modules/`). Each module acts as an interactive science experiment validating infrastructure behaviors under load.

```text
ai-inference-hackday-quickstart-demo/
├── README.md                
├── requirements.txt           
├── src/                      
│   ├── config.py              # Centralized cluster URLs (vLLM / Ollama backends)
│   ├── telemetry.py           # Metrics capture hooks tracking operational KPIs
│   └── mock_data.py           # Local vector space cache & Golden Dataset prompts
│
└── modules/                   
    ├── part1_vram_frameworks.py     # Hardware sizing math & sequential blocking demo
    ├── part2_paged_attention.py     # Concurrent stress test: Ollama vs. vLLM execution
    ├── part3_token_tax_cache.py     # Prompt optimization benchmarks & Semantic Caching
    ├── part4_tiered_routing.py      # Context-aware request classification middleware
    ├── part5_reliability_queues.py  # Pydantic JSON enforcement, SSE streaming, & Circuit Breakers
    └── part6_automated_evals.py     # Programmatic LLM-as-a-Judge validation pipeline
```


### How to Run Application

Set environment variables:

```bash
export AKAMAI_INFERENCE_URL="http://YOUR_ENDPOINT:8000/v1/chat/completions"
export SMALL_MODEL="your-small-model"
export LARGE_MODEL="your-large-model"
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## ⏱️ Interactive Playbook: How to Run the Modules

Every script is fully configured to execute directly from your terminal. Run them sequentially as we advance through the presentation slides.

### 🟢 Phase 1: Hardware Layer, VRAM Math, & Runtimes
Understand your memory footprint to prevent the dreaded **3:00 AM Out-of-Memory (OOM) Crash**. Learn how Quantization yields up to a 70% VRAM saving, and see why standard synchronous web servers lock up under load.

```bash
python modules/part1_vram_frameworks.py
```

### 🔀 Phase 2: Packaging, Routing, & Extreme Cost Cutting
Mitigate the Input Token Tax. Witness how massive, unoptimized RAG contexts destroy Time to First Token (TTFT) metrics. Implement an in-memory Semantic Cache to intercept repeating prompts, resulting in a 5ms response at a $0 GPU cost.

```bash
python modules/part3_token_tax_cache.py
``` 

Implement the gateway's brain: a Tiered Escalation Router. Automatically offload minor text generation to lightweight edge devices or 1B models, saving your premium clusters for complex logic.

```bash
python modules/part4_tiered_routing.py
```

### 📈 Phase 3: Reliability, Observability, & Live Telemetry
Bulletproof your application structure. Use Pydantic/Instructor to enforce rigid output schemas so your front-end never crashes over malformed JSON. Calculate live performance KPIs (TTFT and Throughput Tokens/Sec) over an active stream, and watch the Circuit Breaker automatically switch to safe fallbacks when a cluster disconnects.

```bash
python modules/part5_reliability_queues.py
```

Move past generic server logging. Implement automated LLM-as-a-Judge verification loops. Rather than checking generations manually, score your pipeline's safety and alignment programmatically against a curated dataset of Golden Prompts.

```bash
python modules/part6_automated_evals.py
```

## 📊 The 3 Operational AI KPIs to Watch
When building your weekend hackathon entries, move past standard server uptime and monitor your AI Operations Suite:

- **Time to First Token (TTFT)**: Measures input processing efficiency. Use context optimization and streaming to keep this under 200ms.

- **Tokens Per Second Per User**: Measures throughput speed. Maximize this via production runtime engines utilizing continuous batching.

- **KV Cache Utilization**: Measures available GPU memory headroom. Protect this using a semantic cache and strict input traffic queues.

Happy Hacking! Copy any module's architectural design patterns directly into your submission builds to ensure a bulletproof, high-performance project presentation.