from __future__ import annotations
from math import sqrt, log
from typing import Optional, List, Tuple
from ..models import Tree, Node, UIParams

def uct_value(parent_visits: int, node: Node, c: float) -> float:
    if node.mcts.visits == 0:
        return float("inf")
    return node.mcts.avg_value + c * sqrt(log(max(1, parent_visits)) / node.mcts.visits)

def select(tree: Tree, node_id: str, ui: UIParams) -> Tuple[str, List[str]]:
    current = tree.nodes[node_id]
    path: List[str] = [current.id]
    while current.branches:
        parent_visits = max(1, current.mcts.visits)
        best_child: Optional[Node] = None
        best_score = -1e18
        for cid in current.branches:
            child = tree.nodes[cid]
            score = uct_value(parent_visits, child, ui.exploration_c)
            if score > best_score:
                best_score, best_child = score, child
        current = best_child  # type: ignore
        path.append(current.id)
    return current.id, path
