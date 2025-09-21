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

1) Initialize a tree
- Option A: Create Root — enter root text and click Create Root
- Option B: AI Initialize — enter a scenario; backend returns a small graph seeded by AI initializer

2) Graph editing (React Flow)
- Pan/zoom the canvas
- Double-click a node to propose branches via AI
- A validation modal appears where you can accept or modify proposed branches
- Applied branches create new child nodes

3) Configure MCTS
- ConfigPanel: num_simulations, max_depth, exploration_c, etc.
- State and Decisions editors: define variables, constraints, guards/effects
- Use {{ui.parameter_name}} to template UI inputs into state/decisions

4) Run simulation
- Click Run in Simulation panel
- Results panel shows:
  - Nodes count
  - Root visits
  - Golden path (best sequence by criterion)

API summary (backend/app/api.py)
- POST /api/tree/init?text=... -> Tree
- POST /api/tree/init/ai { scenario } -> Tree
- POST /api/tree/{tree_id}/propose { node_id, context? } -> { proposals: string[] }
- POST /api/tree/{tree_id}/apply-branches?node_id=... [ "branch text", ... ] -> Tree
- POST /api/simulate/{tree_id} { tree, ui, state, decisions } -> { tree, stats, golden_path, alternatives }

Screenshots
The repo includes screenshots taken during development. Paths used below will be uploaded with the repo.
- ![Home](docs/images/localhost_5173_203025.png)
- ![Simulation](docs/images/localhost_5173_203146.png)

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
