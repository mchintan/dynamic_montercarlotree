import { useAppStore } from "../store/useAppStore";
import { simulate } from "../lib/api";
import { resolveTemplates } from "../lib/template";

export default function SimulationPanel() {
  const { tree, ui, stateConfig, decisions, set } = useAppStore();
  const run = async () => {
    if (!tree) return;
    const payload = {
      tree,
      ui,
      state: resolveTemplates(stateConfig, ui),
      decisions: resolveTemplates(decisions, ui),
    };
    const res = await simulate(tree.id, payload);
    set({ results: res, tree: res.tree });
  };
  return (
    <div className="bg-white rounded border p-3 space-y-2">
      <h2 className="font-semibold">Simulation</h2>
      <button className="btn" disabled={!tree} onClick={run}>Run</button>
    </div>
  );
}
