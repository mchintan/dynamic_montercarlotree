import { useAppStore } from "../store/useAppStore";
import { simulate } from "../lib/api";
import { resolveTemplates } from "../lib/template";

export default function SimulationPanel() {
  const { tree, ui, stateConfig, decisions, simulationProgress, set } = useAppStore();

  const run = async () => {
    if (!tree) return;
    set({ simulationProgress: 0, results: null });
    const payload = {
      tree,
      ui,
      state: resolveTemplates(stateConfig, ui),
      decisions: resolveTemplates(decisions, ui),
    };
    const total = ui.num_simulations || 100;
    const steps = [0.25, 0.5, 0.75, 1.0].map(f=>Math.round(total * f));
    let idx = 0;
    const ticker = setInterval(()=>{
      if (idx < steps.length) {
        set({ simulationProgress: Math.round((steps[idx] / total) * 100) });
        idx++;
      } else {
        clearInterval(ticker);
      }
    }, 500);

    const res = await simulate(tree.id, payload);
    clearInterval(ticker);
    set({ results: res, tree: res.tree, simulationProgress: 100 });
  };

  return (
    <div className="bg-white rounded border p-3 space-y-3">
      <h2 className="font-semibold">Simulation</h2>
      <div className="flex items-center gap-2">
        <button className="btn" disabled={!tree} onClick={run}>Run</button>
        {simulationProgress > 0 && simulationProgress < 100 && (
          <span className="text-sm text-gray-600">Progress: {simulationProgress}%</span>
        )}
      </div>
      {simulationProgress > 0 && (
        <div className="w-full bg-gray-200 h-2 rounded">
          <div className="h-2 bg-blue-600 rounded" style={{ width: `${simulationProgress}%` }} />
        </div>
      )}
    </div>
  );
}
