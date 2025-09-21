from fastapi import APIRouter, HTTPException, Body, Response
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
    root = tree.nodes.get(tree.root_id)
    rv = 0
    if root:
        m = getattr(root, "mcts", None)
        if m is not None and hasattr(m, "visits"):
            rv = m.visits
        else:
            rv = getattr(root, "visit_count", 0)
    stats = {
        "num_nodes": len(tree.nodes),
        "root_visits": rv,
    }
    return SimulationResult(tree=tree, stats=stats, golden_path=golden, alternatives=[])

@router.get("/tree/{tree_id}/export/json")
def export_json(tree_id: str):
    tree = store.get_tree(tree_id)
    return tree.dict()

def _markdown_outline(tree: Tree) -> str:
    lines = []
    def rec(nid: str, prefix: str = ""):
        n = tree.nodes[nid]
        label = n.text
        lines.append(f"{prefix}- {label}")
        for cid in n.branches:
            bmeta = tree.nodes[nid].branch_meta.get(cid) if hasattr(tree.nodes[nid], "branch_meta") else None
            edge = f" ({bmeta.description})" if bmeta else ""
            rec(cid, prefix + "  ")
    rec(tree.root_id)
    return "\n".join(lines)

@router.get("/tree/{tree_id}/export/markdown")
def export_markdown(tree_id: str):
    tree = store.get_tree(tree_id)
    md = _markdown_outline(tree)
    return Response(content=md, media_type="text/markdown")

def _mermaid(tree: Tree) -> str:
    lines = ["graph TD"]
    def rec(nid: str):
        n = tree.nodes[nid]
        lines.append(f'  {nid}["{n.text}"]')
        for cid in n.branches:
            bmeta = tree.nodes[nid].branch_meta.get(cid) if hasattr(tree.nodes[nid], "branch_meta") else None
            label = bmeta.description if bmeta else ""
            lines.append(f"  {nid} -->|{label}| {cid}")
            rec(cid)
    rec(tree.root_id)
    return "\n".join(lines)

@router.get("/tree/{tree_id}/export/mermaid")
def export_mermaid(tree_id: str):
    tree = store.get_tree(tree_id)
    mm = _mermaid(tree)
    return Response(content=mm, media_type="text/plain")

@router.post("/simulate/{tree_id}/qa")
def qa_checks(tree_id: str, tree: Tree = Body(...)):
    results = []
    max_depth = max((n.depth for n in tree.nodes.values()), default=0)
    results.append({"name": "sufficient_depth", "pass": max_depth >= 3, "detail": f"max_depth={max_depth}"})
    has_terminal = any(n.is_terminal or not n.branches for n in tree.nodes.values())
    results.append({"name": "terminal_nodes", "pass": has_terminal, "detail": "at least one terminal/leaf"})
    ok_depths = all(tree.nodes[cid].depth == n.depth + 1 for n in tree.nodes.values() for cid in n.branches if cid in tree.nodes)
    results.append({"name": "logical_consistency", "pass": ok_depths, "detail": "depths monotonic"})
    return {"checks": results}
