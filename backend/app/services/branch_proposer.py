from typing import List, Dict, Any

def propose_branches_llm(prompt: str, k: int = 3) -> List[str]:
    base = [
        "Option A: proceed with high risk",
        "Option B: conservative approach",
        "Option C: gather more information",
        "Option D: defer decision",
        "Option E: seek expert input",
    ]
    return base[:max(2, min(5, k))]

def build_prompt(node_text: str, context: Dict[str, Any] | None) -> str:
    return f"Node: {node_text}\nContext: {context or {}}\nPropose 2-5 realistic branches."
