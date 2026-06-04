# Ask Akamai AI Cloud

A hands-on workshop project that demonstrates how **inference decisions** can make AI applications faster, cheaper, more reliable, and more useful.

Rather than focusing on model training or infrastructure deployment, this project explores the engineering layer that sits between users and large language models (LLMs). Participants learn how to improve AI applications through techniques such as context optimization, model routing, reliability patterns, and observability.

The application is built as a simple documentation assistant powered by public Akamai AI Cloud documentation and a hosted inference endpoint.

---

## Workshop Goal

The purpose of this project is to teach participants how to think beyond simply calling an LLM API.

By the end of the workshop, participants should understand:

* When larger models are worth the latency and cost
* How model routing improves efficiency
* Why context optimization matters
* How retries and fallback models improve reliability
* What metrics should be collected to make informed inference decisions
* How these techniques are used in real AI products

The central message of the workshop is:

> Don't just call an LLM. Engineer the inference path.

---

## Application Overview

Ask Akamai AI Cloud is a lightweight question-answering assistant that answers questions about Akamai AI Cloud using publicly available documentation.

Example questions:

* What is Akamai AI Cloud?
* What are GPU Compute Instances?
* What is the difference between LKE and a virtual machine?
* How should I deploy a low-latency inference workload on Akamai?

The application evolves throughout the workshop, with each module introducing a new inference engineering concept.

---

## Workshop Modules

### Module 1: Baseline

A simple question-answering application.

```text
Question
   ↓
LLM
   ↓
Answer
```

Concepts:

* Basic inference
* Hosted model endpoint

---

### Module 2: Context Optimization

Introduces retrieval and grounding using Akamai documentation.

```text
Question
   ↓
Retrieve Relevant Docs
   ↓
LLM
   ↓
Answer
```

Concepts:

* Retrieval-Augmented Generation (RAG)
* Reducing unnecessary context
* Grounded responses

---

### Module 3: Latency vs Quality

Compares responses from a smaller model and a larger model.

Concepts:

* Response quality
* Latency tradeoffs
* Cost tradeoffs

---

### Module 4: Model Routing

Routes requests to different models based on complexity.

```text
Question
   ↓
Router
   ↓
 ┌───────────┬───────────┐
 │           │
Small      Large
Model      Model
```

Concepts:

* Dynamic model selection
* Cost optimization
* Latency optimization

---

### Module 5: Reliability

Introduces retries and fallback models.

```text
Question
   ↓
Primary Model
   ↓
Failure?
   ↓
Retry
   ↓
Fallback Model
```

Concepts:

* Resilience
* Graceful degradation
* Production reliability

---

### Module 6: Observability

Displays metrics and inference traces.

Concepts:

* Latency tracking
* Token usage
* Routing decisions
* Fallback events
* Inference transparency

---

## Architecture

```text
User
 ↓
Ask Akamai AI Cloud
 ↓
Retriever
 ↓
Router
 ↓
Reliability Layer
 ↓
Hosted Inference Endpoint
 ↓
Model
```

The application demonstrates how modern AI systems often derive more value from inference architecture than from model changes alone.

---

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

---

## Data Sources

This project uses publicly available Akamai documentation, including:

* Akamai AI Cloud
* GPU Compute Instances
* NVIDIA RTX PRO 6000 Blackwell GPU documentation
* Linode Kubernetes Engine (LKE)
* Related Akamai Cloud resources

Documentation is ingested into a lightweight retrieval system to support context optimization demonstrations.

---

## Running the Application

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

Start the application:

```bash
streamlit run app.py
```

---

## What Participants Learn

By working through the modules, participants learn how to:

* Build a retrieval-enhanced AI application
* Compare model latency and quality
* Route requests intelligently
* Implement retry and fallback strategies
* Instrument and observe inference behavior
* Make evidence-based inference decisions

These techniques can be applied to customer support assistants, enterprise copilots, documentation assistants, AI agents, and many other production AI systems.

---

## Key Takeaway

The winning AI applications are not always built with the biggest model.

They are often built by making better decisions about:

* Context
* Model selection
* Reliability
* Observability
* Cost
* Latency

This project provides a practical framework for understanding and implementing those decisions.
