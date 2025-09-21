from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from uuid import uuid4

class MCTSData(BaseModel):
    visits: int = 0
    total_reward: float = 0.0
    avg_value: float = 0.0

class Branch(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    description: str
    rationale: Optional[str] = None

class Node(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    parent_id: Optional[str] = None
    text: str
    branches: List[str] = Field(default_factory=list)
    branch_meta: Dict[str, Branch] = Field(default_factory=dict)
    mcts: MCTSData = Field(default_factory=MCTSData)
    is_terminal: bool = False
    depth: int = 0
    metadata: Dict[str, Any] = Field(default_factory=dict)

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
class ProposedBranch(BaseModel):
    description: str
    rationale: Optional[str] = None


class DecisionsConfig(BaseModel):
    decisions: List[Decision] = Field(default_factory=list)

class ProposeBranchesRequest(BaseModel):
    node_id: str
    context: Optional[Dict[str, Any]] = None

class ProposeBranchesResponse(BaseModel):
    proposals: List[ProposedBranch]

class SimulationRequest(BaseModel):
    tree: Tree
    ui: UIParams
    state: StateConfig
    decisions: DecisionsConfig

class SimulationProgress(BaseModel):
    total: int
    completed: int

class GoldenStep(BaseModel):
    node_id: str
    branch_taken: Optional[str] = None
    node_description: str
    reasoning: Optional[str] = None
    success_probability: Optional[float] = None

class SimulationResult(BaseModel):
    tree: Tree
    stats: Dict[str, Any]
    golden_path: List[GoldenStep] | List[str]
    alternatives: List[List[GoldenStep]] | List[List[str]]
