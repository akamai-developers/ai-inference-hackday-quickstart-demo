from spin_sdk import http
from spin_sdk.http import IncomingHandler, Request, Response
import json


class IncomingHandler(IncomingHandler):

    def handle_request(self, request: Request) -> Response:

        try:
            body = json.loads(request.body)
            user_prompt = body.get("prompt", "")
            max_tokens = body.get("max_tokens", 180)

        except Exception as e:
            return Response(
                400,
                {"content-type": "application/json"},
                json.dumps({
                    "error": "Invalid request payload",
                    "details": str(e)
                }).encode()
            )

        # Use Akamai EdgeScape headers only.
        # If they are unavailable, fall back to Nairobi for local testing/demo safety.
        akamai_city = request.headers.get("x-akamai-edgescape-city")
        akamai_country = request.headers.get("x-akamai-edgescape-country")

        if akamai_city and akamai_country:
            detected_city = akamai_city
            detected_country = akamai_country
            location_source = "Akamai Edge"
        else:
            detected_city = "Nairobi (Westlands)"
            detected_country = "Kenya"
            location_source = "Default Demo Location"

        system_instruction = (
            f"You are a concise local travel guide. "
            f"The user is currently located in {detected_city}, {detected_country}. "
            f"Answer in 3-5 short bullets. Include one local food recommendation, "
            f"one cultural tip, and one useful local phrase with phonetic pronunciation."
        )

        vllm_url = "http://LINODE_GPU_IP:8000/v1/chat/completions"

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
            "temperature": 0.6,
            "max_tokens": max_tokens
        }

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

        output_payload = {
            "locationContext": f"{detected_city}, {detected_country}",
            "locationSource": location_source,
            "injectedSystemPrompt": system_instruction,
            "aiResponse": ai_text,
            "messagesSentToVllm": vllm_payload["messages"],
            "model": "Llama 3.2 1B",
            "inferenceEngine": "vLLM",
            "backend": "Linode GPU VM",
            "promptTokens": vllm_data.get("usage", {}).get("prompt_tokens", "N/A"),
            "completionTokens": vllm_data.get("usage", {}).get("completion_tokens", "N/A")
        }

        return Response(
            200,
            {"content-type": "application/json"},
            json.dumps(output_payload).encode()
        )