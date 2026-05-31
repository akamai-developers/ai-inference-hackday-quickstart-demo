# app.py - Deploys to Akamai Functions (Serverless WASM)
from spin_sdk import http
from spin_sdk.http import Request, Response
import json
import re

def handle_request(request: Request) -> Response:
    # 1. Parse incoming prompt from the Streamlit UI
    try:
        body = json.loads(request.body)
        user_prompt = body.get("prompt", "")
    except Exception:
        return Response(400, {"content-type": "application/json"}, b'{"error": "Invalid JSON payload"}')

    # 2. FIREWALL LAYER 1: Prompt Injection Guardrail
    # Catches malicious override strings right at the edge network layer
    injection_keywords = ["ignore previous instructions", "system prompt", "dan mode", "override policy"]
    if any(keyword in user_prompt.lower() for keyword in injection_keywords):
        error_payload = {
            "status": "blocked",
            "error": "SECURITY COMPLIANCE ALERT: Malicious prompt injection attempt intercepted at Akamai Edge Node."
        }
        return Response(403, {"content-type": "application/json"}, json.dumps(error_payload).encode())

    # 3. FIREWALL LAYER 2: Inline PII / Secret Redaction
    # Scrubs corporate data patterns before they cross into the core cloud network
    sanitized_prompt = user_prompt
    
    # Regex pattern matching for standard emails
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    sanitized_prompt = re.sub(email_pattern, "[REDACTED_EMAIL]", sanitized_prompt)
    
    # Regex pattern matching for sensitive dollar values or budgets (e.g., $15,000 or $5M)
    financial_pattern = r'\$[0-9,]+(?:\s*(?:million|M|billion|B))?'
    sanitized_prompt = re.sub(financial_pattern, "[REDACTED_FINANCIAL_ASSET]", sanitized_prompt)

    # 4. SECURE ROUTING: Forward clean prompt to your Linode vLLM Server
    # Note: Replace with your actual Linode GPU server public IP address
    vllm_url = "http://YOUR_LINODE_GPU_IP:8000/v1/chat/completions"
    vllm_payload = {
        "model": "meta-llama/Llama-3.2-1B-Instruct",
        "messages": [{"role": "user", "content": sanitized_prompt}],
        "temperature": 0.3 # Lower temperature ensures deterministic corporate output
    }

    try:
        # Spin SDK native outbound HTTP network client
        vllm_response = http.send(Request(
            "POST", 
            vllm_url, 
            {"content-type": "application/json"}, 
            json.dumps(vllm_payload).encode()
        ))
        
        vllm_data = json.loads(vllm_response.body)
        ai_text = vllm_data["choices"][0]["message"]["content"]
        
        output_payload = {
            "status": "passed",
            "sanitizedPrompt": sanitized_prompt,
            "aiResponse": ai_text
        }
        return Response(200, {"content-type": "application/json"}, json.dumps(output_payload).encode())
        
    except Exception as e:
        err_payload = {"status": "error", "error": f"Failed to connect to core GPU factory: {str(e)}"}
        return Response(500, {"content-type": "application/json"}, json.dumps(err_payload).encode())