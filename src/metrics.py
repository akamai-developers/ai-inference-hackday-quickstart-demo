import time


# A simple in-memory session store to aggregate live telemetry traces
TRACE_HISTORY = []

def build_trace(
    module: str,
    model: str,
    latency_ms=None,
    ttft_ms=None,      # 👈 Explicitly capturing hardware response time
    tokens_in=None,
    tokens_out=None,
    retrieved_docs=None,
    route_reason=None,
    fallback_used=False,
    errors=None,
):
    # Calculate generation throughput speed (Tokens per Second)
    # To measure true AI speed, you must subtract the initial network lag (TTFT) from total latency 
    # because that waiting time is not part of the actual text generation process.
    tokens_per_sec = 0.0
    if tokens_out and latency_ms and ttft_ms:
        generation_time_sec = (latency_ms - ttft_ms) / 1000.0
        if generation_time_sec > 0:
            tokens_per_sec = round(tokens_out / generation_time_sec, 2)

    trace = {
        "timestamp": time.strftime("%H:%M:%S"),
        "module": module,
        "model_used": model,
        "route_reason": route_reason,
        "latency_ms": latency_ms,
        "ttft_ms": ttft_ms,
        "tokens_in": tokens_in or 0,
        "tokens_out": tokens_out or 0,
        "tokens_per_sec": tokens_per_sec,  # 👈 Crucial hardware throughput metric
        "retrieved_docs": retrieved_docs or [],
        "fallback_used": fallback_used,
        "errors": errors or [],
    }
    
    # Store globally so Module 6 can read the historical trail
    TRACE_HISTORY.append(trace)
    return trace

def get_all_traces():
    """Returns the historical trail for Module 6 aggregation analytics."""
    return TRACE_HISTORY

def clear_trace_history():
    global TRACE_HISTORY
    TRACE_HISTORY = []