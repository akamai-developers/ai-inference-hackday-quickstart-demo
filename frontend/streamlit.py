import streamlit as st
import requests
import time

st.set_page_config(page_title="Global Context AI Proxy", layout="wide")
st.title("🌐 OmniRoute AI: The Global Translation & Geolocation Travel Buddy")
#st.caption("Context Engineered at Akamai Distributed Edge | Computed on Linode GPU Infrastructure")

EDGE_FUNCTION_URL = "https://your-python-travel-wasm.akamai.com"

# Sidebar to let you easily spoof different locations during your live presentation demo!
with st.sidebar:
    #st.header("✈️ Location Flight Simulator")
    st.write("Simulate moving an enterprise user across global networks instantly.")
    mock_location = st.selectbox(
        "Select Active Node Destination:",
        ["Tokyo (Shibuya District), Japan", "Paris (Le Marais), France", "Nairobi (Westlands), Kenya"]
    )
    st.info(f"Connected Edge Node PoP: {mock_location.split(',')[0]}")

# Main Chat Input
user_query = st.text_input(
    "What is your question for the local AI assistant?",
    value="What is a popular local breakfast here, and how do I politely ask for the check?"
)

if st.button("Query Global Network Pipeline", type="primary"):
    start_time = time.time()
    
    # Extract mock variables to pass over headers to our serverless endpoint
    city, country = [x.strip() for x in mock_location.split(",")]
    custom_headers = {
        "x-akamai-edgescape-city": city,
        "x-akamai-edgescape-country": country
    }

    with st.spinner("Determining network proximity & structuring context package..."):
        response = requests.post(EDGE_FUNCTION_URL, json={"prompt": user_query}, headers=custom_headers)
        elapsed_ms = (time.time() - start_time) * 1000

    if response.status_code == 200:
        data = response.json()
        
        # Telemetry Metrics
        col1, col2 = st.columns(2)
        col1.metric("Network Resolution Latency", f"{elapsed_ms:.1f} ms", "Edge Ingestion Active")
        col2.metric("Inferred Geographic Target", data["locationContext"])
        
        # Display the system prompt manipulation logs
        with st.expander("🛠️ Inspect Edge-Injected System Instructions Payload"):
            st.code(data["injectedSystemPrompt"], language="text")
            
        st.subheader("🎙️ Context-Aware AI Travel Companion Response")
        st.write(data["aiResponse"])
    else:
        st.error(f"Network error linking to Edge Function. Status: {response.status_code}")