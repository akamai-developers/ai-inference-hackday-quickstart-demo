import time
from typing import Generator
from config import SMALL_MODEL
from src.inference_client import call_model


def call_model_with_fallback(
    primary_model: str, 
    messages: list[dict], 
    stream: bool = False,
    simulate_failure: bool = False
) -> Generator[dict, None, None]:
    """
    Core Reliability Pattern: Attempts a primary model execution path.
    Instantly intercepts crashes to execute an active fallback model stream.
    """
    # 1. If the live demo switch is thrown, we poison the model string to force an API failure
    actual_model = "invalid-hardware-endpoint-force-crash" if simulate_failure else primary_model
    
    try:
        # Attempt the primary execution path
        primary_stream = call_model(actual_model, messages, stream=stream)
        for chunk in primary_stream:
            # Pass chunks through, adding a flag indicating everything is nominal
            chunk["fallback_used"] = False
            chunk["error_message"] = None
            yield chunk
            
    except Exception as primary_error:
        # 2. 🚨 CRASH INTERCEPTED
        error_msg = f"Primary cluster anomaly detected: {str(primary_error)}"
        
        # 3. Secure Fallback Mechanism
        # We instantly pivot the traffic stream to our smaller backup tier model
        fallback_stream = call_model(SMALL_MODEL, messages, stream=stream)
        for chunk in fallback_stream:
            chunk["fallback_used"] = True
            chunk["error_message"] = error_msg
            yield chunk