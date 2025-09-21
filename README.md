# Dynamic Monte Carlo Tree Search (MCTS) Web App

FastAPI backend + React/Vite/Tailwind frontend for interactive, user-validated Monte Carlo Tree Search:
- AI initialization of the starting graph based on a scenario
- Visual graph editor with React Flow
- Propose branches via AI and validate in a modal before applying
- Run MCTS simulations (UCT selection, rollout, backprop)
- View golden path and stats
- Template UI parameters into configs using {{ui.*}} syntax

Notes
- In-memory store by default; data resets on backend restart.
- LLM features are mocked locally by default. Hooks exist to connect a real provider later.

Project structure
- backend: FastAPI app, MCTS engine, services, in-memory store
- frontend: React/Vite/Tailwind, React Flow graph, Zustand app store

Quick start

Backend
1) cd backend
2) python -m venv .venv && source .venv/bin/activate
3) pip install -r requirements.txt (or poetry install if preferred)
4) uvicorn app.main:app --reload
The API will be available at http://localhost:8000/api

Frontend
1) cd frontend
2) npm install
3) cp .env.example .env.local
4) npm run dev
Open http://localhost:5173

Frontend environment variables
See frontend/.env.example
- VITE_API_URL: defaults to http://localhost:8000/api

Core flows

1) Phase 1 — Initialize
- Wizard collects: starting_point, desired_goal, constraints, evaluation_criteria
- Confirm understanding, then initialize a root node
- Optionally use AI Initialize — enter a scenario; backend returns a small graph seeded by AI initializer

2) Graph editing (React Flow)
- Pan/zoom the canvas
- Double-click a node to propose branches via AI
- Validation modal shows 2–5 options with { description, rationale }; edit before applying
- Applied branches create new child nodes; edge labels reflect branch descriptions

3) Configure MCTS
- ConfigPanel: num_simulations, max_depth, exploration_c, etc.
- State and Decisions editors: define variables, constraints, guards/effects
- Use {{ui.parameter_name}} to template UI inputs into state/decisions

4) Run simulation
- Click Run in Simulation panel
- Progress updates display at ~25/50/75/100%
- Results panel shows:
  - Nodes count, depth, and total simulations
  - Golden path (numbered), with optional probabilities
  - Confidence band (High/Medium/Low)
  - Export buttons (Markdown/JSON/Mermaid)

API summary (backend/app/api.py)
- POST /api/tree/init?text=... -> Tree
- POST /api/tree/init/ai { scenario } -> Tree
- POST /api/tree/{tree_id}/propose { node_id, context? } -> { proposals: { description, rationale? }[] }
- POST /api/tree/{tree_id}/apply-branches?node_id=...  body: { description, rationale? }[] -> Tree
- POST /api/simulate/{tree_id} { tree, ui, state, decisions } -> { tree, stats, golden_path, alternatives }
- POST /api/simulate/{tree_id}/qa  body: Tree -> { checks: [{ name, pass, detail }] }
- GET  /api/tree/{tree_id}/export/json -> JSON
- GET  /api/tree/{tree_id}/export/markdown -> text/markdown
- GET  /api/tree/{tree_id}/export/mermaid -> text/plain

Screenshots
The repo includes updated v2.0 screenshots:
- ![Init Wizard](docs/images/init_wizard.png)
- ![AI Initialize](docs/images/ai_init.png)
- ![Branch Validation](docs/images/branch_validation.png)
- ![Graph with Labels/Tooltips](docs/images/graph_labels.png)
- ![Simulation Progress + QA Checks](docs/images/sim_progress_qa.png)
- ![Results v2 (Golden Path, Stats, Exports, Alternatives/Insights)](docs/images/results_v2.png)

Customization and provider hooks
- Branch proposals: backend/app/services/branch_proposer.py
- AI graph init: backend/app/services/ai_initializer.py
- Reward model: backend/app/services/reward_model.py
Swap the mock logic with real LLM calls and load API keys from env.

Limitations and next steps
- In-memory store only; add persistent DB if needed
- MCTS is optimized for interactivity; deeper simulation tuning can be added (batched rollouts, parallelism)
- Progress streaming/polling can be added to display live simulation progress

Contributing
- Fork/branch, run locally, open a PR
- Use the feature branch naming convention: devin/{timestamp}-mcts-app

License
MIT (or as you prefer)
