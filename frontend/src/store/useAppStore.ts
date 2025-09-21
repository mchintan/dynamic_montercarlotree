import { create } from "zustand";

type UIParams = {
  num_simulations: number; max_depth: number; time_budget_ms?: number | null;
  exploration_c: number; random_seed?: number | null; golden_path_criterion: string;
};

export type ProposedBranch = { description: string; rationale?: string | null };

type AppState = {
  tree: any | null;
  ui: UIParams;
  stateConfig: any;
  decisions: any;
  selectedNodeId: string | null;
  proposals: ProposedBranch[];
  results: any | null;
  set: (u: Partial<AppState>) => void;
};

export const useAppStore = create<AppState>((set) => ({
  tree: null,
  ui: { num_simulations: 200, max_depth: 10, exploration_c: 1.414, random_seed: 42, golden_path_criterion: "avg_reward" },
  stateConfig: { variables: {}, constraints: {}, terminal_conditions: [], reward_expression: null, transition_noise: null },
  decisions: { decisions: [] },
  selectedNodeId: null,
  proposals: [],
  results: null,
  set: (u) => set(u),
}));
