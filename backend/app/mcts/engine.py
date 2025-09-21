from __future__ import annotations
import time, random
from typing import List
from ..models import Tree, Node, UIParams, StateConfig, DecisionsConfig
from .policies import select
from ..services.branch_proposer import propose_branches_llm, build_prompt
from ..services.reward_model import evaluate_reward

def expand(tree: Tree, node_id: str, k: int = 3):
    node = tree.nodes[node_id]
    if node.branches or node.is_terminal:
        return
    prompt = build_prompt(node.text, context={})
    proposals = propose_branches_llm(prompt, k=k)
    for txt in proposals:
        child = Node(parent_id=node.id, text=txt)
        tree.nodes[child.id] = child
        node.branches.append(child.id)

def simulate_rollout(tree: Tree, start_node_id: str, ui: UIParams, state: StateConfig, decisions: DecisionsConfig) -> float:
    rng = random.Random(ui.random_seed)
    depth = 0
    node = tree.nodes[start_node_id]
    reward = 0.0
    while depth < ui.max_depth and not node.is_terminal:
        if not node.branches:
            break
        node = tree.nodes[rng.choice(node.branches)]
        depth += 1
        reward = evaluate_reward({"_seed": rng.randint(0, 10**6)}, node.text, state.reward_expression)
    return reward

def backpropagate(tree: Tree, path: List[str], reward: float):
    for nid in path:
        n = tree.nodes[nid]
        n.visit_count += 1
        n.total_reward += reward
        n.average_value = n.total_reward / max(1, n.visit_count)

def run_simulations(tree: Tree, ui: UIParams, state: StateConfig, decisions: DecisionsConfig, progress_cb=None):
    start_time = time.time()
    for i in range(ui.num_simulations):
        leaf_id = select(tree, tree.root_id, ui)
        expand(tree, leaf_id)
        reward = simulate_rollout(tree, leaf_id, ui, state, decisions)
        backpropagate(tree, path=[leaf_id], reward=reward)
        if progress_cb and (i + 1) % 10 == 0:
            progress_cb(i + 1, ui.num_simulations)
        if ui.time_budget_ms:
            elapsed_ms = (time.time() - start_time) * 1000
            if elapsed_ms >= ui.time_budget_ms:
                break

def compute_golden_path(tree: Tree, criterion: str = "avg_reward") -> List[str]:
    path: List[str] = []
    current = tree.nodes[tree.root_id]
    while True:
        path.append(current.id)
        if not current.branches:
            break
        if criterion == "avg_reward":
            next_id = max(current.branches, key=lambda cid: tree.nodes[cid].average_value)
        else:
            next_id = max(current.branches, key=lambda cid: tree.nodes[cid].visit_count)
        current = tree.nodes[next_id]
    return path
