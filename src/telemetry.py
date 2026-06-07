import time
from functools import wraps

def track_metrics(phase_name: str):
    """
    Decorator to capture and format key infrastructure performance indicators
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            print(f"\n===== [TELEMETRY START: {phase_name.upper()}] =====")
            
            result = func(*args, **kwargs)
            
            duration = time.time() - start_time
            print(f"⏱️  [METRIC] Execution Time: {duration*1000:.2f}ms")
            print(f"===== [TELEMETRY END: {phase_name.upper()}] =====\n")
            return result
        return wrapper
    return decorator