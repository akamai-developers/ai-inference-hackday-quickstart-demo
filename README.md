# 🌐 OmniRoute AI: The Location-Aware Travel Assistant

OmniRoute AI is a smart translation and travel chatbot that automatically figures out where you are standing in the world and gives you localized answers—**without ever asking for your phone's GPS location or browser tracking permissions.**

### How It Works
1. **You type a generic question** into the chat box (e.g., *"What should I eat for breakfast here?"*).
2. **Akamai captures your web request** at the nearest network tower and instantly notes your city and country based on your internet connection.
3. **A lightweight Python script at the edge** injects that location data directly into your prompt behind the scenes, transforming your generic question into a hyper-targeted request (e.g., *"The user is in Tokyo. What should they eat for breakfast?"*).
4. **Our private Linode GPU server** runs the AI model (Llama 3.2 via vLLM) and streams a personalized, native response back to your screen in milliseconds.

---

## 🏗️ Architecture Blueprint

The application demonstrates a distributed **Edge-to-Core AI Pipeline** written entirely in **100% Pure Python**:

1. **Frontend Layer (Streamlit):** A minimalist Python dashboard that allows users to prompt the assistant and simulate traveling across global networks in real-time.
2. **Edge Orchestration Layer (Akamai Functions):** A lightweight Python script compiled to WebAssembly (WASM) via the Spin framework. It extracts geographic routing telemetry (`X-Akamai-Edgescape` headers) at the network edge and dynamically constructs an optimized AI system instruction package.
3. **Core Inference Layer (Linode GPU Cloud):** An optimized **vLLM engine** serving `meta-llama/Llama-3.2-1B-Instruct` parameters inside dedicated VRAM on high-performance compute instances, offering a secure, private, OpenAI-compatible endpoint.

---

## 📂 Project Repository Structure

```text
├── edge/
│   ├── app.py          # Akamai Functions Serverless script (Python Wasm)
│   └── spin.toml       # Spin configuration manifest for deployment
├── frontend/
│   └── streamlit.py     # Streamlit Interactive User Dashboard (Python)
├── infra/
│   ├── main.tf          
│   └── cloud-init.yaml  # Provision CUDA drivers for GPU
├── requirements.txt
└── README.md           # Project Documentation
```

## 🚀 Quickstart Deployment

### 1. Core Layer: Launch vLLM on Linode GPU
SSH into your provisioned Linode GPU compute instance and initialize your model serving engine.

```bash
# Setup a clean virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install vLLM
pip install vllm

# Authorize Hugging Face access for gated model weights
export HF_TOKEN="your_huggingface_token_here"

# Start the OpenAI-compatible vLLM server environment
python3 -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-3.2-1B-Instruct \
    --port 8000 \
    --host 0.0.0.0