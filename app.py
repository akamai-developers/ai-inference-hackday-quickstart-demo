import streamlit as st
from modules import baseline
from modules import context_optimization
from modules import latency_vs_quality
from modules import model_router 
from modules import reliability_demo

# Set page config to wide mode so 5 columns look beautiful and clean
st.set_page_config(layout="wide")

st.title("Akamai Inference Day: Core Architecture Blueprint")
st.caption("A step-by-step masterclass in engineering the inference path.")

# ---------------------------------------------------------
# GLOBAL CONTROLLER SIDEBAR
# ---------------------------------------------------------
st.sidebar.header("🛠️ Infrastructure Knobs")

# 1. The Perceived Performance Switch (Module 1)
use_streaming = st.sidebar.checkbox("Enable Real-Time Streaming", value=True)

# 2. Manual Hardware Tier Toggles (Module 3)
model_tier = st.sidebar.radio("M3 Hardware Sizing Selection:", ("Large Model", "Small Model"))
use_large = True if model_tier == "Large Model" else False

# 3. The Live Infrastructure Sabotage Toggle (Module 5)
kill_primary_gpu = st.sidebar.toggle("Simulate Primary GPU Outage (Force Crash)", value=False)


# ---------------------------------------------------------
# MAIN INTERACTIVE PROMPT INTERFACE
# ---------------------------------------------------------
question = st.text_input(
    "Test Input Prompt:", 
    value="What are the specs of the NVIDIA RTX PRO 6000 Blackwell GPU?"
)

# Initialize columns for our 5 architectural modules
col1, col2, col3, col4, col5 = st.columns(5)

# Initialize a central place to store results so we can render the dashboard at the bottom
if "current_answer" not in st.session_state:
    st.session_state["current_answer"] = ""
if "latest_trace" not in st.session_state:
    st.session_state["latest_trace"] = None


# --- MODULE 1: THE RAW BASELINE ---
with col1:
    st.markdown("### 01\n**Raw Baseline**")
    if st.button("Execute M1", use_container_width=True):
        st.session_state["current_answer"] = ""
        output_box = st.empty()
        for result in baseline.run(question, stream=use_streaming):
            output_box.markdown(result["answer"])
            st.session_state["latest_trace"] = result["trace"]

# --- MODULE 2: CONTEXT OPTIMIZATION ---
with col2:
    st.markdown("### 02\n**Context Optimized**")
    if st.button("Execute M2", use_container_width=True):
        st.session_state["current_answer"] = ""
        output_box = st.empty()
        for result in context_optimization.run(question, stream=use_streaming):
            output_box.markdown(result["answer"])
            st.session_state["latest_trace"] = result["trace"]

# --- MODULE 3: LATENCY VS QUALITY ---
with col3:
    st.markdown("### 03\n**Hardware Sizing**")
    if st.button("Execute M3", use_container_width=True):
        st.session_state["current_answer"] = ""
        output_box = st.empty()
        for result in latency_vs_quality.run(question, use_large_model=use_large, stream=use_streaming):
            output_box.markdown(result["answer"])
            st.session_state["latest_trace"] = result["trace"]

# --- MODULE 4: INTENT-DRIVEN ROUTER ---
with col4:
    st.markdown("### 04\n**Smart Router**")
    if st.button("Execute M4", use_container_width=True):
        st.session_state["current_answer"] = ""
        output_box = st.empty()
        for result in model_router.run(question, stream=use_streaming):
            output_box.markdown(result["answer"])
            st.session_state["latest_trace"] = result["trace"]

# --- MODULE 5: FAULT-TOLERANT RING ---
with col5:
    st.markdown("### 05\n**Reliability Layer**")
    if st.button("Execute M5", use_container_width=True):
        st.session_state["current_answer"] = ""
        output_box = st.empty()
        for result in reliability_demo.run(question, stream=use_streaming, simulate_failure=kill_primary_gpu):
            output_box.markdown(result["answer"])
            st.session_state["latest_trace"] = result["trace"]


# ---------------------------------------------------------
# THE CENTRAL TELEMETRY DASHBOARD
# ---------------------------------------------------------
trace = st.session_state["latest_trace"]

if trace:
    st.divider()
    st.subheader("📊 Akamai Cloud Infrastructure Metrics Trace")
    
    # Render clear status indicators based on active modules
    if trace.get("fallback_used"):
        st.error(f"🚨 **Fault-Tolerance Intercept Active!** System captured: {trace['errors'][0]}")
    elif trace.get("route_reason"):
        st.info(f"🧠 **LLM Router Intelligence Context:** {trace['route_reason']}")

    # Metric Cards Core Display Layout
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Active Module Step", trace["module"])
    m2.metric("Target Model Running", trace["model_used"].split("/")[-1]) # Shorten model string for readability
    m3.metric("Total Processing Delay", f"{trace['latency_ms']} ms")
    m4.metric("Tokens Passed In", trace["tokens_in"] if trace["tokens_in"] else "N/A")
    m5.metric("Tokens Computed Out", trace["tokens_out"] if trace["tokens_out"] else "N/A")

    # Display underlying retriever sources transparently
    if trace.get("retrieved_docs"):
        st.markdown(f"📁 **Context Sources Extracted from `docs.jsonl`:** " + 
                    ", ".join([f"`{title}`" for title in trace["retrieved_docs"]]))