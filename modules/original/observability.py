import pandas as pd
from src.metrics import get_all_traces


def run_observability_analysis() -> dict:
    """
    Module 6: Aggregates historical inference metrics.
    Transforms raw JSON logs into a structured system health audit.
    """
    history = get_all_traces()
    
    if not history:
        return {
            "has_data": False,
            "summary": {},
            "dataframe": pd.DataFrame()
        }
    
    # Convert execution traces into a clean Pandas dataframe for easy UI rendering
    df = pd.DataFrame(history)
    
    # Compile aggregated infrastructure highlights
    summary = {
        "total_requests": len(df),
        "avg_ttft_ms": round(df["ttft_ms"].mean(), 2) if "ttft_ms" in df.columns else 0,
        "avg_throughput": round(df["tokens_per_sec"].mean(), 2) if "tokens_per_sec" in df.columns else 0,
        "total_tokens_consumed": int(df["tokens_in"].sum() + df["tokens_out"].sum()),
        "fallback_count": int(df["fallback_used"].sum()) if "fallback_used" in df.columns else 0
    }
    
    return {
        "has_data": True,
        "summary": summary,
        "dataframe": df[[
            "timestamp", "module", "model_used", "latency_ms", 
            "ttft_ms", "tokens_in", "tokens_out", "tokens_per_sec", "fallback_used"
        ]]
    }