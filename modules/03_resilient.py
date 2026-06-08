import time
import os
from openai import OpenAI

# Module 3: The Resilient Engine (03_resilient.py)
#   Concepts Supported: Observability, Evaluations (Judge-Proofing), Reliability & Fallbacks (Graceful Degradation).
#   The Demo: Integrates all concepts. You will run it once to show a perfect run with metrics, then you will change 
#             the port to a bad IP live on screen to prove that the fallback circuit breaker saves the app from crashing.

# INTENTIONAL FIX/BREAK TARGET FOR LIVE DEMO:
# Change port '8000' to '9999' live on stage to simulate a cluster crash!
AKAMAI_URL = "http://YOUR-SHARED-SANDBOX-IP:8000/v1" 

akamai_client = OpenAI(base_url=AKAMAI_URL, api_key="akamai-hackathon-2026-token")
fallback_client = OpenAI(api_key=os.environ.get("BACKUP_API_KEY", "your-backup-key"))

def execute_judge_proof_inference(prompt: str):
    print(f"\n🚀 [Processing Request] Calling Primary Engine...")
    start_time = time.time()
    
    try:
        # OBSERVABILITY & RELIABILITY
        response = akamai_client.chat.completions.create(
            model="meta-llama/Llama-3-8B-Instruct",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            timeout=3.0 # Strict timeout guard
        )
        latency = time.time() - start_time
        print(f"✅ [SUCCESS] Primary Akamai Engine responded in {latency:.2f}s")
        output = response.choices.message.content

    except Exception as e:
        # RELIABILITY & FALLBACK (GRACEFUL DEGRADATION)
        print(f"🚨 [CRITICAL OUTAGE] Primary Engine Failed! Reason: {e}")
        print("🛡️ [CIRCUIT BREAKER] Diverting traffic instantly to backup API provider...")
        fallback_start = time.time()
        
        response = fallback_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        print(f"🛡️ [FALLBACK SUCCESS] Fulfilled via cloud backup in {time.time() - fallback_start:.2f}s")
        output = response.choices.message.content

    # RAPID EVALUATION (LLM-AS-A-JUDGE LIGHTWEIGHT TEST)
    print("🔍 [Automated Eval] Running rapid accuracy check...")
    eval_prompt = f"Is the following AI response polite and professional? Answer with only YES or NO.\nResponse: '{output}'"
    
    # We use our stable fallback for evaluations to prevent bias
    eval_res = fallback_client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": eval_prompt}], max_tokens=5
    )
    print(f"📋 [Evaluation Metric] Meets professional standards: {eval_res.choices.message.content.strip()}")
    return output

if __name__ == "__main__":
    execute_judge_proof_inference("Generate a friendly welcome message for our platform.")