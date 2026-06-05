import json
import httpx
from config import LARGE_MODEL, SMALL_MODEL, BASE_URL

def route_question(question: str) -> dict:
    """
    Analyzes user intent using a fast, low-cost LLM call.
    Returns a dict with the selected model and the structural reason.
    """
    router_prompt = (
        "You are an AI infrastructure traffic router. Classify the user query into one of two tiers:\n"
        "SMALL: Simple factual questions, basic definitions, or straightforward documentation lookups.\n"
        "LARGE: Complex logic, system comparisons, writing code/scripts, architectural tradeoffs, or deep reasoning.\n\n"
        "Output strictly a JSON object with two keys:\n"
        "1. 'tier': either 'SMALL' or 'LARGE'\n"
        "2. 'reason': a brief one-sentence string explaining your decision.\n"
        f"Query: {question}"
    )
    
    payload = {
        "model": SMALL_MODEL,  # Fast and cheap to keep routing overhead low
        "messages": [{"role": "user", "content": router_prompt}],
        "temperature": 0.0,
        "response_format": {"type": "json_object"}
    }
    
    try:
        with httpx.Client() as client:
            response = client.post(BASE_URL, json=payload, timeout=5.0)
            response.raise_for_status()
            data = response.json()
            
            # Extract and parse the model's JSON thoughts
            result = json.loads(data["choices"]["message"]["content"])
            
            if result.get("tier") == "SMALL":
                return {"model": SMALL_MODEL, "reason": result.get("reason", "Factual lookup.")}
            else:
                return {"model": LARGE_MODEL, "reason": result.get("reason", "Complex task requirements.")}
                
    except Exception as e:
        # Fallback to safe default if infrastructure routing hits an anomaly
        return {
            "model": LARGE_MODEL, 
            "reason": f"Routing exception ({str(e)}). Defaulted to Large Tier for safety."
        }