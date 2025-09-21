from typing import Dict, Any, List
import os
import random

def init_graph_ai(scenario: str) -> Dict[str, Any]:
    rng = random.Random(hash(scenario) & 0xFFFFFFFF)
    root_text = f"Scenario: {scenario.strip() or 'Untitled'}"
    options = [
        "Path 1: optimistic trajectory",
        "Path 2: conservative trajectory",
        "Path 3: information gathering",
        "Path 4: pivot",
        "Path 5: defer decision",
    ]
    k = 3
    branches = options[:k]
    root = {
        "text": root_text,
        "branches": []
    }
    nodes: Dict[str, Dict[str, Any]] = {}
    def nid(prefix: str, i: int) -> str:
        return f"{prefix}-{i}-{rng.randint(1000,9999)}"
    root_id = nid("n", 0)
    nodes[root_id] = {
        "id": root_id,
        "parent_id": None,
        "text": root_text,
        "branches": [],
        "visit_count": 0,
        "total_reward": 0.0,
        "average_value": 0.0,
        "is_terminal": False,
    }
    for i, txt in enumerate(branches):
        cid = nid("n", i+1)
        nodes[cid] = {
            "id": cid,
            "parent_id": root_id,
            "text": txt,
            "branches": [],
            "visit_count": 0,
            "total_reward": 0.0,
            "average_value": 0.0,
            "is_terminal": False,
        }
        nodes[root_id]["branches"].append(cid)
    return {
        "root_id": root_id,
        "nodes": nodes,
    }
