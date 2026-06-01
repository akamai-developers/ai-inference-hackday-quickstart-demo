import time
import requests
import streamlit as st

EDGE_FUNCTION_URL = "http://YOUR_LINODE_GPU_IP:3000" # Replace with deployed Spin URL later

st.set_page_config(page_title="OmniRoute AI", page_icon="🌐", layout="wide")

st.title("🌐 OmniRoute AI")

st.markdown(
    "Your AI-powered travel companion for exploring local culture, food, customs, and language. "
    "Ask questions about any destination and receive recommendations tailored to where you're visiting."
)

st.caption("Powered by Akamai Edge, Spin, vLLM, and Linode GPU inference.")

with st.sidebar:
    st.header("🌍 Location Detection")

    st.success(
        "OmniRoute uses Akamai Edge geolocation when available. "
        "If no edge location is detected, the demo defaults to Nairobi."
    )

    max_tokens = st.slider(
        "Response Length",
        min_value=80,
        max_value=350,
        value=180,
        step=20
    )

main_col, metrics_col = st.columns([2.4, 1])

with main_col:
    st.markdown("### ✈️ Ask me anything!")

    user_query = st.text_area(
        "What would you like to know?",
        value="What is a popular local breakfast here, and how do I politely ask for the check?",
        height=120
    )

    run_query = st.button(
        "Get Local Tips",
        type="primary",
        use_container_width=True
    )

with metrics_col:
    st.markdown("### ⚡ Live Summary")
    metrics_placeholder = st.empty()

if run_query:
    start_time = time.time()

    try:
        with st.spinner("Sending request through Akamai Edge and vLLM..."):
            response = requests.post(
                EDGE_FUNCTION_URL,
                json={
                    "prompt": user_query,
                    "max_tokens": max_tokens
                },
                timeout=60
            )

        total_ms = (time.time() - start_time) * 1000

        if response.status_code == 200:
            data = response.json()

            with metrics_placeholder.container():
                st.metric("Latency", f"{total_ms:.1f} ms")
                st.metric("Edge Location", data.get("locationContext", "Unknown"))
                st.metric("Model", data.get("model", "Unknown"))

            st.success(
                f"📍 Location added at the edge: {data.get('locationContext', 'Unknown')}"
            )

            st.markdown("### Location Added by Spin")
            with st.container(border=True):
                st.markdown(f"**Detected Location:** {data.get('locationContext', 'Unknown')}")
                st.markdown(f"**Source:** {data.get('locationSource', 'Unknown')}")

            st.markdown("### Prompt Sent to vLLM")

            messages = data.get("messagesSentToVllm", [])

            with st.container(border=True):
                if messages:
                    for message in messages:
                        role = message.get("role", "").upper()
                        content = message.get("content", "")

                        if role == "SYSTEM":
                            st.markdown("#### 🌐 System Instructions")
                        elif role == "USER":
                            st.markdown("#### ✈️ User Message")
                        else:
                            st.markdown(f"#### {role}")

                        st.write(content)
                        st.divider()
                else:
                    st.markdown("#### 🌐 System Instructions")
                    st.write(data.get("injectedSystemPrompt", ""))

                    st.markdown("#### ✈️ User Message")
                    st.write(user_query)

            st.markdown("### vLLM Response")
            with st.container(border=True):
                st.write(data.get("aiResponse", ""))

        else:
            st.error(f"Could not reach OmniRoute service. HTTP {response.status_code}")
            st.caption(response.text)

    except requests.exceptions.RequestException as e:
        st.error("Unable to connect to the OmniRoute edge service.")
        st.caption(str(e))