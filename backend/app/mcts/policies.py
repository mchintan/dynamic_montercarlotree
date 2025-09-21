from __future__ import annotations
from math import sqrt, log
from typing import Optional
from ..models import Tree, Node, UIParams

def uct_value(parent_visits: int, node: Node, c: float) -> float:
    if node.visit_count == 0:
        return float("inf")
    return node.average_value + c * sqrt(log(max(1, parent_visits)) / node.visit_count)

def select(tree: Tree, node_id: str, ui: UIParams) -> str:
    current = tree.nodes[node_id]
    while current.branches:
        parent_visits = max(1, current.visit_count)
        best_child: Optional[Node] = None
        best_score = -1e18
        for cid in current.branches:
            child = tree.nodes[cid]
            score = uct_value(parent_visits, child, ui.exploration_c)
            if score > best_score:
                best_score, best_child = score, child
        current = best_child  # type: ignore
    return current.id
