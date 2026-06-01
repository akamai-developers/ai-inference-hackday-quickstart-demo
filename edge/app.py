from spin_sdk import http
from spin_sdk.http import IncomingHandler, Request, Response
import json


class IncomingHandler(IncomingHandler):

    def handle_request(self, request: Request) -> Response:

        # Parse request body
        try:
            body = json.loads(request.body)
            user_prompt = body.get("prompt", "")
        except Exception as e:
            return Response(
                400,
                {"content-type": "application/json"},
                json.dumps({
                    "error": "Invalid request payload",
                    "details": str(e)
                }).encode()
            )

        # Determine location source
        demo_city = request.headers.get("x-demo-city")
        demo_country = request.headers.get("x-demo-country")

        akamai_city = request.headers.get("x-akamai-edgescape-city")
        akamai_country = request.headers.get("x-akamai-edgescape-country")

        if demo_city and demo_country:
            detected_city = demo_city
            detected_country = demo_country
            location_source = "Simulated Destination"

        elif akamai_city and akamai_country:
            detected_city = akamai_city
            detected_country = akamai_country
            location_source = "Akamai Edge"

        else:
            detected_city = "Tokyo (Shibuya)"
            detected_country = "Japan"
            location_source = "Fallback Demo Location"

        # Build system prompt
        system_instruction = (
            f"You are a local cultural travel companion. "
            f"The user is currently located in {detected_city}, {detected_country}. "
            f"Answer their prompt using local context, nearby recommendations, "
            f"and useful native phrases with phonetic pronunciation."
        )

        # Build vLLM request
        vllm_url = "http://172.235.244.111:8000/v1/chat/completions"

        vllm_payload = {
            "model": "meta-llama/Llama-3.2-1B-Instruct",
            "messages": [
                {
                    "role": "system",
                    "content": system_instruction
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            "temperature": 0.6
        }

        # Call vLLM
        try:
            vllm_response = http.send(
                Request(
                    "POST",
                    vllm_url,
                    {"content-type": "application/json"},
                    json.dumps(vllm_payload).encode()
                )
            )

            vllm_data = json.loads(vllm_response.body)

        except Exception as e:
            return Response(
                500,
                {"content-type": "application/json"},
                json.dumps({
                    "error": "Failed to call vLLM",
                    "details": str(e)
                }).encode()
            )

        # Validate vLLM response
        if "choices" not in vllm_data:
            return Response(
                502,
                {"content-type": "application/json"},
                json.dumps({
                    "error": "Unexpected response from vLLM",
                    "vllm_response": vllm_data
                }).encode()
            )

        ai_text = vllm_data["choices"][0]["message"]["content"]

        # Return to Streamlit
        output_payload = {
            "locationContext": f"{detected_city}, {detected_country}",
            "locationSource": location_source,
            "injectedSystemPrompt": system_instruction,
            "aiResponse": ai_text
        }

        return Response(
            200,
            {"content-type": "application/json"},
            json.dumps(output_payload).encode()
        )