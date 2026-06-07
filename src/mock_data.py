# Simulating a massive enterprise context bloat payload (e.g., raw recursive PDF scraping)
MOCK_15K_TOKEN_CONTEXT = " " * 60000 + "[CRITICAL DATA BLOCK: Use CUDA cache invalidation flag --force-clear]"

# Basic Semantic Cache Mock Store
_semantic_database = {
    "how do i clear my gpu memory cache?": "Execute torch.cuda.empty_cache() or reboot the running runtime worker.",
    "can you show me how to clear gpu memory?": "Execute torch.cuda.empty_cache() or reboot the running runtime worker."
}

def mock_semantic_cache_lookup(prompt: str) -> str:
    """Simulates a fast vector database cosine-similarity match lookup"""
    cleaned = prompt.strip().lower()
    return _semantic_database.get(cleaned, None)

# Small 'Golden Prompt' dataset for automated evaluations
GOLDEN_DATASET = [
    {
        "prompt": "Extract metadata: The AI HackDay 2026 infrastructure track has 45 teams.",
        "expected_truth": "hackathon_name='AI HackDay 2026' track_theme='Infrastructure' expected_teams=45"
    }
]