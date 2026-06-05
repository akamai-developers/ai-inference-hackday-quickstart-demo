# 🚀 Akamai AI Cloud Inference Day Quickstart

Welcome to the **Akamai AI Cloud Inference Day Hackday Quickstart**! This repository is a production-ready blueprint designed to take your hackathon project from a fragile, slow API wrapper to a blazing-fast, cost-optimized, and resilient AI product running on Akamai's distributed cloud infrastructure.

## 🛑 The "3 AM Hackathon Crisis"
Most hackathon teams build an AI application that works beautifully for exactly *one* developer. But during live judging, multiple users hit the app simultaneously, causing the underlying GPU cluster to hit an **Out-Of-Memory (OOM) crash**, skyrocketing latency to 30 seconds, and turning the UI into a frozen blank screen. 

**The fix isn't choosing a bigger model. The fix is Engineering the Inference Path.**

---

## 🏗️ 6-Layer Architecture Blueprint
This quickstart is split into progressive, decoupled modules. Follow along or copy-paste these structural blocks to bulletproof your application architecture:

## Repository Structure

```text
ask-akamai-ai-cloud/
│
├── app.py
├── config.py
├── requirements.txt
│
├── data/
│   └── docs.jsonl
│
├── src/
│   ├── inference_client.py
│   ├── retriever.py
│   ├── router.py
│   ├── reliability.py
│   └── metrics.py
│
├── modules/
│   ├── baseline.py
│   ├── context_optimization.py
│   ├── latency_quality.py
│   ├── model_routing.py
│   ├── reliability_demo.py
│   └── observability.py
│
└── README.md
```

### 📦 The Core Modules
1. **01 Baseline (Streaming vs. Non-Streaming):** Switches your app configuration from slow, blocked block-loading to real-time packet streaming. Drastically slashes **Time to First Token (TTFT)**.
2. **02 Context Optimization:** Implements a localized keyword matcher over your `docs.jsonl` database. Teaches context budgeting to prevent bloating input tokens and driving up latency.
3. **03 Hardware Sizing:** Compares a large reasoning model tier against a small, highly efficient edge model tier to prove that bigger parameters aren't always better for basic lookups.
4. **04 Intent-Driven Smart Router:** Uses an ultra-fast, cheap model pass to dynamically classify user intent into `SMALL` or `LARGE` JSON tiers, executing the cheapest hardware profile capable of solving the query.
5. **05 Fault-Tolerant Ring:** Simulates a primary GPU infrastructure blackout. The code captures the exception and instantly switches traffic to a backup model so judges never see a crash.
6. **06 Live Observability Deck:** Compiles all session memory traces into a centralized analytics system health ledger, tracking aggregate processing delays and token volume.
7. **07 Micro-Evaluations (LLM-as-a-Judge):** Runs your output against a small set of "Golden Ground Truths" to score factual accuracy from 1 to 5, ensuring optimization hasn't degraded intelligence.

---

## ⚡ Quickstart Setup

### 1. Clone & Install Dependencies
Ensure you have Python 3.10+ installed on your environment. Clone this project and install the lean required library stack:
```bash
git clone https://github.com
cd ai-inference-hackday-quickstart-demo
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a standard configuration file or export your authorization keys matching your Akamai AI Cloud settings:
```bash
export AKAMAI_INFERENCE_URL="http://YOUR_AKAMAI_ENDPOINT_IP:8000/v1/chat/completions"
export AKAMAI_API_KEY="your-super-secret-authorization-token"
```

### 3. Launch the Master Panel
Spin up the interactive Streamlit user interface panel:
```bash
streamlit run app.py
```

---

## 📊 Core AI Infrastructure KPIs to Track
When developing your system, watch the dashboard analytics trace at the bottom of your screen closely:
* **TTFT (Time to First Token):** How many milliseconds does the user stare at a blank screen before text appears? Keep this under 200ms using streaming configurations.
* **Tokens In (`tokens_in`):** Your cost and pre-fill latency tax. Keep this as small as possible by using tight retriever limits and short document context snippets.
* **Throughput (Tokens/Sec):** The computation generation velocity of the model execution. Smaller models running on optimized Akamai cloud cards will generate significantly faster.

---

## 💡 Hackathon Demo Winning Strategy
During your final presentation or pitch to the judges, **do not just show the raw output text**. 

Open the **Module 6 Observability Report** at the bottom of your page. Prove to the judges that you didn't just wrap an LLM, but built a distributed, scalable enterprise network layout. Show them your dynamic router reasons, your fallback capabilities, and highlight how your application manages processing performance and resource economics gracefully!