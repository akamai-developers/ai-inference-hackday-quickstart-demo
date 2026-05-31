from spin_sdk import http
from spin_sdk.http import Request, Response
import json

def handle_request(request: Request) -> Response:
    try:
        body = json.loads(request.body)
        user_prompt = body.get("prompt", "")
        
        # Read Akamai's native geolocation headers injected at the edge network layer
        # If headers are missing (local testing), default to a cool showcase location like Tokyo, Japan
        detected_country = request.headers.get("x-akamai-edgescape-country", "Japan")
        detected_city = request.headers.get("x-akamai-edgescape-city", "Tokyo (Shibuya)")
    except Exception:
        return Response(400, {"content-type": "application/json"}, b'{"error": "Invalid payload"}')

    # Construct a hyper-targeted System Prompt using our Edge Telemetry variables
    system_instruction = (
        f"You are a local cultural travel companion. The user is currently located in "
        f"{detected_city}, {detected_country}. Answer their prompt using hyper-local context, "
        f"recommendations physically near that region, and provide exact native phonetic translations."
    )

    # Package everything into the strict OpenAI/vLLM payload structure
    vllm_url = "http://YOUR_LINODE_GPU_IP:8000/v1/chat/completions"
    vllm_payload = {
        "model": "meta-llama/Llama-3.2-1B-Instruct",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.6
    }

    # Outbound call over Akamai internal pipes directly to your Linode GPU instance
    vllm_response = http.send(Request(
        "POST", 
        vllm_url, 
        {"content-type": "application/json"}, 
        json.dumps(vllm_payload).encode()
    ))
    
    vllm_data = json.loads(vllm_response.body)
    ai_text = vllm_data["choices"][0]["message"]["content"]

    output_payload = {
        "locationContext": f"{detected_city}, {detected_country}",
        "injectedSystemPrompt": system_instruction,
        "aiResponse": ai_text
    }

    return Response(200, {"content-type": "application/json"}, json.dumps(output_payload).encode())