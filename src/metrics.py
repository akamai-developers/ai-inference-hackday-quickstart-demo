def build_trace(
    module: str,
    model: str,
    latency_ms=None,
    tokens_in=None,
    tokens_out=None,
    retrieved_docs=None,
    route_reason=None,
    fallback_used=False,
    errors=None,
):
    return {
        "module": module,
        "model_used": model,
        "route_reason": route_reason,
        "latency_ms": latency_ms,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "retrieved_docs": retrieved_docs or [],
        "fallback_used": fallback_used,
        "errors": errors or [],
    }