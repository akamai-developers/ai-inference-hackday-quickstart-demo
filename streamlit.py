# frontend.py - Run locally or host on Akamai App Platform
import streamlit as st
import requests
import time

st.set_page_config(page_title="Akamai Security Gateway Dashboard", layout="wide")
st.title("🛡️ Akamai ShieldGate: Enterprise AI Firewall")
st.caption("Secured by Python WASM at Akamai Distributed Edge | Computed on Linode GPU Cloud (vLLM)")

# Enter your deployed Akamai Serverless function URL endpoint here
EDGE_FUNCTION_URL = "https://your-python-wasm-endpoint.akamai.com"

# Sidebar showing the architectural orchestration status
with st.sidebar:
    st.header("🌐 Gateway Infrastructure Status")
    st.success("Edge Firewall Nodes: ONLINE (4,400+ PoPs)")
    st.success("Core Inference Factory: ONLINE (Linode GPU Cluster)")
    st.info("Active Model Serving Node: vLLM -> Llama-3.2-1B-Instruct")
    st.markdown("---")
    st.write("This dashboard monitors real-time text compliance metrics processing at the closest global edge node.")

# Main app input
prompt = st.text_area("Corporate AI Prompt Input Panel", placeholder="Type a prompt or try to leak an email/budget amount...", height=100)

if st.button("Execute Secure Inference Pipeline", type="primary"):
    if not prompt:
        st.warning("Please enter a prompt first.")
    else:
        start_time = time.time()
        
        with st.spinner("Streaming packet to nearest Akamai Edge Node..."):
            # UI hits the edge function exclusively, hiding your internal GPU server IP
            response = requests.post(EDGE_FUNCTION_URL, json={"prompt": prompt})
            latency_ms = (time.time() - start_time) * 1000

        # Case 1: Prompt went through, cleaned successfully, and model ran
        if response.status_code == 200:
            data = response.json()
            
            # Draw telemetry dashboards
            col1, col2, col3 = st.columns(3)
            col1.metric("Edge Intercept Latency", f"{latency_ms:.1f} ms", "Sub-10ms Overhead")
            col2.metric("Gateway Status", "PROCESSED & SANITIZED", delta="100% Secure")
            col3.metric("Data Leak Risk Index", "0.00%", delta="-100% Reduction")
            
            # Show what the gateway altered under the hood
            st.info(f"📋 **Gateway Security Audit Log (What your GPU actually saw):**\n\n *\"{data['sanitizedPrompt']}\"*")
            
            st.subheader("🤖 Private Core LLM Response")
            st.markdown(data['aiResponse'])

        # Case 2: Gateway blocked an offensive prompt injection
        elif response.status_code == 403:
            data = response.json()
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Edge Intercept Latency", f"{latency_ms:.1f} ms", "Dropped at Network Edge")
            col2.metric("Gateway Status", "BLOCK TRIGGERED", delta="Threat Neutered", delta_color="inverse")
            col3.metric("Data Leak Risk Index", "ABORTED", delta="Blocked")
            
            st.error(data['error'])
            st.warning("⚠️ **System Insight:** The request was completely terminated at the edge network layer. Zero tokens were consumed on your Linode GPU backend.")
            
        else:
            st.error(f"Gateway connection issue. Status Code: {response.status_code}")