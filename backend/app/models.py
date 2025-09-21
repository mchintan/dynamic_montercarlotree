from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from uuid import uuid4

class Node(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    parent_id: Optional[str] = None
    text: str
    branches: List[str] = Field(default_factory=list)
    visit_count: int = 0
    total_reward: float = 0.0
    average_value: float = 0.0
    is_terminal: bool = False

class Tree(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    root_id: str
    nodes: Dict[str, "Node"] = Field(default_factory=dict)

class UIParams(BaseModel):
    num_simulations: int = 500
    max_depth: int = 10
    time_budget_ms: Optional[int] = None
    exploration_c: float = 1.414
    random_seed: Optional[int] = 42
    golden_path_criterion: str = "avg_reward"

class StateConfig(BaseModel):
    variables: Dict[str, Any] = Field(default_factory=dict)
    constraints: Dict[str, Any] = Field(default_factory=dict)
    terminal_conditions: List[str] = Field(default_factory=list)
    reward_expression: Optional[str] = None
    transition_noise: Optional[Dict[str, Any]] = None

class Decision(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    guard: Optional[str] = None
    effects: Dict[str, Any] = Field(default_factory=dict)

class DecisionsConfig(BaseModel):
    decisions: List[Decision] = Field(default_factory=list)

class ProposeBranchesRequest(BaseModel):
    node_id: str
    context: Optional[Dict[str, Any]] = None

class ProposeBranchesResponse(BaseModel):
    proposals: List[str]

class SimulationRequest(BaseModel):
    tree: Tree
    ui: UIParams
    state: StateConfig
    decisions: DecisionsConfig

class SimulationProgress(BaseModel):
    total: int
    completed: int

class SimulationResult(BaseModel):
    tree: Tree
    stats: Dict[str, Any]
    golden_path: List[str]
    alternatives: List[List[str]]
