from fastapi import APIRouter, HTTPException, Body
from .models import *
from .store.memory import store
from .mcts.engine import run_simulations, compute_golden_path
from .services.ai_initializer import init_graph_ai

router = APIRouter(prefix="/api")

@router.post("/tree/init", response_model=Tree)
def init_tree(text: str):
    root = Node(text=text, depth=0, metadata={"rationale": None})
    tree = Tree(root_id=root.id, nodes={root.id: root})
    store.put_tree(tree)
    return tree

@router.post("/tree/init/ai", response_model=Tree)
def init_tree_ai(scenario: str = Body(..., embed=True)):
    payload = init_graph_ai(scenario)
    nodes = {}
    for nid, ndata in payload["nodes"].items():
        base = dict(ndata)
        base.setdefault("depth", 0 if nid == payload["root_id"] else 1)
        base.setdefault("metadata", {"rationale": base.get("metadata", {}).get("rationale") if isinstance(base.get("metadata"), dict) else None})
        nodes[nid] = Node(**base)
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
    proposals = [ProposedBranch(**p) for p in props]
    return ProposeBranchesResponse(proposals=proposals)

@router.post("/tree/{tree_id}/apply-branches", response_model=Tree)
def apply_branches(tree_id: str, node_id: str, branches: List[ProposedBranch] = Body(...)):
    tree = store.get_tree(tree_id)
    node = tree.nodes[node_id]
    for pb in branches:
        child = Node(parent_id=node.id, text=pb.description, depth=node.depth + 1, metadata={"rationale": pb.rationale})
        tree.nodes[child.id] = child
        node.branches.append(child.id)
        node.branch_meta[child.id] = Branch(id=child.id, description=pb.description, rationale=pb.rationale)
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
        "root_visits": getattr(tree.nodes[tree.root_id], "mcts", None).visits if hasattr(tree.nodes[tree.root_id], "mcts") else tree.nodes[tree.root_id].visit_count,
    }
    return SimulationResult(tree=tree, stats=stats, golden_path=golden, alternatives=[])
