from app.models import Tree, Node, UIParams, StateConfig, DecisionsConfig
from app.mcts.engine import run_simulations, compute_golden_path

def test_basic_simulation():
    root = Node(text="Start")
    tree = Tree(root_id=root.id, nodes={root.id: root})
    ui = UIParams(num_simulations=50, max_depth=5)
    state = StateConfig()
    dec = DecisionsConfig()
    run_simulations(tree, ui, state, dec)
    path = compute_golden_path(tree)
    assert len(path) >= 1
