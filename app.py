import streamlit as st

from modules import (
    baseline,
    context_optimization,
    latency_quality,
    model_routing,
    reliability_demo,
    observability,
)

MODULES = {
    "01 Baseline": baseline.run,
    "02 Context Optimization": context_optimization.run,
    "03 Latency vs Quality": latency_quality.run,
    "04 Model Routing": model_routing.run,
    "05 Reliability": reliability_demo.run,
    "06 Observability": observability.run,
}

st.set_page_config(page_title="Ask Akamai AI Cloud", layout="wide")

st.title("Ask Akamai AI Cloud")
st.caption("A workshop app for learning inference decisions that matter.")

mode = st.sidebar.selectbox("Workshop module", list(MODULES.keys()))

simulate_failure = st.sidebar.checkbox(
    "Simulate primary model failure",
    value=False,
)

question = st.text_area(
    "Ask a question",
    value="How should I deploy a low-latency inference endpoint on Akamai AI Cloud?",
    height=120,
)

if st.button("Run"):
    with st.spinner("Running inference..."):
        result = MODULES[mode](
            question=question,
            simulate_failure=simulate_failure,
        )

    left, right = st.columns([2, 1])

    with left:
        st.subheader("Answer")
        st.write(result["answer"])

    with right:
        st.subheader("Inference Trace")
        st.json(result["trace"])

        if "comparison" in result:
            st.subheader("Comparison")
            st.json(result["comparison"])