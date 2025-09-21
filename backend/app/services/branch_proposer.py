from typing import List, Dict, Any

def propose_branches_llm(prompt: str, k: int = 3) -> List[Dict[str, str]]:
    base = [
        {"description": "Self-study route", "rationale": "Fast and low-cost; requires discipline"},
        {"description": "Formal education", "rationale": "Structured learning; slower but thorough"},
        {"description": "Direct application", "rationale": "Learn on the job; high variance"},
        {"description": "Hybrid approach", "rationale": "Balance study with networking"},
        {"description": "Seek mentorship", "rationale": "Guided path; quality depends on mentor"},
    ]
    k = max(2, min(5, k))
    return base[:k]

def build_prompt(node_text: str, context: Dict[str, Any] | None) -> str:
    return f"Node: {node_text}\nContext: {context or {}}\nPropose 2-5 realistic branches with short rationales."
