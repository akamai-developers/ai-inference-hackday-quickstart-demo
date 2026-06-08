import time
import os
from openai import OpenAI

# Module 2: The Intent Router.
# Shows your application automatically identifying simple incoming emails vs. heavy analytical data payloads, 
# routing them to either the fast local Akamai 8B instance or an external reasoning API.


LKE_URL = os.environ.get("AKAMAI_INFERENCE_URL", "http://YOUR-SHARED-SANDBOX-IP:8000/v1")
LOCAL_MODEL = os.environ.get("SMALL_MODEL", "meta-llama/Llama-3-8B-Instruct")
PREMIUM_MODEL = os.environ.get("LARGE_MODEL", "gpt-4o-mini")

akamai_client = OpenAI(base_url=LKE_URL, api_key="akamai-hackathon-2026-token")
premium_client = OpenAI(api_key=os.environ.get("BACKUP_API_KEY", "mock-key"))

def process_support_ticket(ticket_text: str):
    print(f"\n📥 [New Ticket]: {ticket_text[:60]}...")
    
    # 1. STRUCTURAL ROUTING LAYER
    router_prompt = f"""
    Classify this support ticket into exactly ONE category:
    - [FAST_TRACK]: Simple password resets, refunds, or basic greetings.
    - [COMPLEX_ANALYSIS]: Code bugs, raw data errors, or architecture complaints.
    Respond with ONLY the category label. Do not include quotes or punctuation.
    Ticket: "{ticket_text}"
    """
    
    t0 = time.time()
    router_res = akamai_client.chat.completions.create(
        model=LOCAL_MODEL,
        messages=[{"role": "user", "content": router_prompt}],
        max_tokens=10,
        temperature=0.0 # Force absolute determinism
    )
    intent = router_res.choices[0].message.content.strip()
    print(f"🎯 [Router Decision]: {intent} (Took {time.time() - t0:.2f}s)")
    
    # 2. EXECUTION LAYER
    t1 = time.time()
    if "[FAST_TRACK]" in intent:
        print(f"⚡ Processing locally on Akamai Cluster ({LOCAL_MODEL})...")
        res = akamai_client.chat.completions.create(
            model=LOCAL_MODEL,
            messages=[{"role": "user", "content": ticket_text}],
            max_tokens=80
        )
    else:
        print(f"🧠 Escalating to Premium High-Intelligence Engine ({PREMIUM_MODEL})...")
        res = premium_client.chat.completions.create(
            model=PREMIUM_MODEL,
            messages=[{"role": "user", "content": ticket_text}],
            max_tokens=150
        )
        
    print(f"✅ Processed in {time.time() - t1:.2f}s -> Reply: {res.choices[0].message.content[:80]}...")


if __name__ == "__main__":
    process_support_ticket("Hi, I forgot my account password. Can you send a reset link?")
    process_support_ticket("Your system threw a traceback error: ZeroDivisionError: division by zero in analytics.py line 42. Fix it.")
