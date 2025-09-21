from typing import Dict
from ..models import Tree, Node

class MemoryStore:
    def __init__(self):
        self.trees: Dict[str, Tree] = {}
    def put_tree(self, tree: Tree):
        self.trees[tree.id] = tree
    def get_tree(self, tree_id: str) -> Tree:
        return self.trees[tree_id]
    def update_node(self, tree_id: str, node: Node):
        t = self.trees[tree_id]
        t.nodes[node.id] = node

store = MemoryStore()
