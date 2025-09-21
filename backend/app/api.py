from fastapi import APIRouter, HTTPException, Body
from .models import *
from .store.memory import store
from .mcts.engine import run_simulations, compute_golden_path
from .services.ai_initializer import init_graph_ai

router = APIRouter(prefix="/api")

@router.post("/tree/init", response_model=Tree)
def init_tree(text: str):
    root = Node(text=text)
    tree = Tree(root_id=root.id, nodes={root.id: root})
    store.put_tree(tree)
    return tree

@router.post("/tree/init/ai", response_model=Tree)
def init_tree_ai(scenario: str = Body(..., embed=True)):
    payload = init_graph_ai(scenario)
    nodes = {nid: Node(**ndata) for nid, ndata in payload["nodes"].items()}
    tree = Tree(root_id=payload["root_id"], nodes=nodes)
    store.put_tree(tree)
    return tree

@router.post("/tree/{tree_id}/propose", response_model=ProposeBranchesResponse)
def propose(tree_id: str, req: ProposeBranchesRequest):
    tree = store.get_tree(tree_id)
    node = tree.nodes.get(req.node_id)
    if not node:
        raise HTTPException(404, "Node not found")
    from .services.branch_proposer import propose_branches_llm, build_prompt
    prompt = build_prompt(node.text, req.context)
    props = propose_branches_llm(prompt)
    return ProposeBranchesResponse(proposals=props)

@router.post("/tree/{tree_id}/apply-branches", response_model=Tree)
def apply_branches(tree_id: str, node_id: str, branches: list[str] = Body(...)):
    tree = store.get_tree(tree_id)
    node = tree.nodes[node_id]
    for txt in branches:
        child = Node(parent_id=node.id, text=txt)
        tree.nodes[child.id] = child
        node.branches.append(child.id)
    store.put_tree(tree)
    return tree

@router.post("/simulate/{tree_id}", response_model=SimulationResult)
def simulate(tree_id: str, req: SimulationRequest):
    tree = req.tree
    store.put_tree(tree)
    run_simulations(tree, req.ui, req.state, req.decisions)
    golden = compute_golden_path(tree, req.ui.golden_path_criterion)
    stats = {
        "num_nodes": len(tree.nodes),
        "root_visits": tree.nodes[tree.root_id].visit_count,
    }
    return SimulationResult(tree=tree, stats=stats, golden_path=golden, alternatives=[])
