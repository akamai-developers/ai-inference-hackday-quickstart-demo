import time
import requests
import streamlit as st

EDGE_FUNCTION_URL = "http://127.0.0.1:3000"

st.set_page_config(
    page_title="OmniRoute AI: Your Local Guide Anywhere",
    page_icon="🌐",
    layout="wide"
)

# ------------------------------------------------------------------
# Header
# ------------------------------------------------------------------

st.title("🌐 OmniRoute AI")
st.caption(
    "Location-powered travel assistance using Akamai Edge and GPU-accelerated AI."
)

st.info(
    "🔄 Request Flow: Streamlit → Akamai Edge Function → Linode GPU (vLLM) → Local Travel Recommendations"
)

# ------------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------------

with st.sidebar:
    st.header("🧭 Trip Setup")
    st.write("Choose how location will be determined.")

    location_mode = st.radio(
        "Location Mode",
        [
            "Use Real Edge Location",
            "Simulate a Destination"
        ]
    )

    mock_location = None

    if location_mode == "Simulate a Destination":
        mock_location = st.selectbox(
            "Destination",
            [
                "Tokyo (Shibuya District), Japan",
                "Paris (Le Marais), France",
                "Nairobi (Westlands), Kenya"
            ]
        )

# ------------------------------------------------------------------
# Prompt Section
# ------------------------------------------------------------------

st.markdown("### ✈️ Ask Your Local Travel Guide")

user_query = st.text_area(
    "What would you like to know?",
    value="What is a popular local breakfast here, and how do I politely ask for the check?",
    height=120
)

# ------------------------------------------------------------------
# Query Button
# ------------------------------------------------------------------

if st.button("Get Local Tips", type="primary", use_container_width=True):

    start_time = time.time()

    custom_headers = {}

    if location_mode == "Simulate a Destination":
        city, country = [x.strip() for x in mock_location.split(",")]

        custom_headers = {
            "x-demo-city": city,
            "x-demo-country": country
        }

    try:

        with st.spinner("Building location-aware prompt..."):

            response = requests.post(
                EDGE_FUNCTION_URL,
                json={"prompt": user_query},
                headers=custom_headers,
                timeout=60
            )

        elapsed_ms = (time.time() - start_time) * 1000

        if response.status_code == 200:

            data = response.json()

            # ------------------------------------------------------
            # Metrics
            # ------------------------------------------------------

            st.markdown("### ⚡ Request Summary")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Response Time",
                f"{elapsed_ms:.1f} ms"
            )

            col2.metric(
                "Destination",
                data["locationContext"]
            )

            col3.metric(
                "Location Source",
                data["locationSource"]
            )

            st.success(
                "Location information was added before the request reached the model."
            )

            # ------------------------------------------------------
            # Architecture View
            # ------------------------------------------------------

            with st.expander("🧩 Behind the Scenes"):
                st.markdown(
                    """
                    **1. Streamlit** collects your question.

                    **2. Akamai Edge Function** determines or receives location information.

                    **3. A location-aware system prompt is created.**

                    **4. The prompt is sent to vLLM running on a Linode GPU.**

                    **5. The AI generates a localized response.**
                    """
                )

            # ------------------------------------------------------
            # Prompt Inspection
            # ------------------------------------------------------

            with st.expander("🔍 View the Prompt Sent to vLLM"):
                st.code(
                    data["injectedSystemPrompt"],
                    language="text"
                )

            # ------------------------------------------------------
            # AI Response
            # ------------------------------------------------------

            st.markdown("### 📍 Recommendations for This Destination")

            with st.container(border=True):
                st.write(data["aiResponse"])

        else:
            st.error(
                f"Could not reach OmniRoute service. HTTP {response.status_code}"
            )

    except requests.exceptions.RequestException as e:
        st.error("Unable to connect to the OmniRoute edge service.")
        st.caption(str(e))