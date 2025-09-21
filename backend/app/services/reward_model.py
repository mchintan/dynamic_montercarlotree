from __future__ import annotations
import random
from typing import Dict, Any
import math

def evaluate_reward(state: Dict[str, Any], node_text: str, expr: str | None) -> float:
    rng = random.Random(state.get("_seed", 0))
    base = 0.5 + 0.1 * math.tanh(len(node_text) / 10)
    noise = rng.uniform(-0.2, 0.2)
    val = base + noise
    if val < 0.0:
        val = 0.0
    if val > 1.0:
        val = 1.0
    return val
