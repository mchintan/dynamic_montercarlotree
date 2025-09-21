import { useAppStore } from "../store/useAppStore";
import { API_URL } from "../lib/api";

export default function ResultsPanel() {
  const { results } = useAppStore();
  if (!results) return (
    <div className="bg-white rounded border p-3">
      <h2 className="font-semibold">Results</h2>
      <p className="text-sm text-gray-600">Run a simulation to see results.</p>
    </div>
  );

  const total = results?.stats?.root_visits || 0;
  const successRatePct = Math.round(((results?.stats?.success_rate || 0) as number) * 100);
  const confidence = successRatePct > 80 ? "High" : successRatePct >= 50 ? "Medium" : "Low";

  const golden = results.golden_path;

  const exportFile = async (type: "json" | "markdown" | "mermaid", treeId: string) => {
    const res = await fetch(`${API_URL}/tree/${treeId}/export/${type}`);
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `tree.${type === "json" ? "json" : type === "markdown" ? "md" : "mmd"}`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="bg-white rounded border p-3 space-y-3">
      <div>
        <h2 className="font-semibold">📊 SIMULATION RESULTS</h2>
        <div className="text-sm text-gray-700 grid grid-cols-1 sm:grid-cols-3 gap-2">
          <div>• Total Simulations: {total}</div>
          <div>• Tree Depth: {results?.stats?.max_depth || "-"}</div>
          <div>• Nodes Evaluated: {results?.stats?.num_nodes || "-"}</div>
        </div>
      </div>

      <div>
        <h3 className="font-semibold">🏆 GOLDEN PATH (Optimal Route)</h3>
        <ol className="list-decimal ml-5 text-sm">
          {Array.isArray(golden) && golden.map((step: any, idx: number) => (
            <li key={idx}>
              {typeof step === "string" ? step : (step.node_description || step.node_id)}
              {typeof step !== "string" && step.success_probability != null ? (
                <span className="text-gray-500"> — {(step.success_probability*100).toFixed(0)}%</span>
              ) : null}
            </li>
          ))}
        </ol>
      </div>

      <div className="text-sm">
        <div>Success rate: {isNaN(successRatePct) ? "-" : `${successRatePct}%`}</div>
        <div>Confidence: {confidence}</div>
      </div>

      <div className="flex flex-wrap gap-2">
        {results?.tree?.id && (
          <>
            <button className="btn-secondary" onClick={()=>exportFile("markdown", results.tree.id)}>Export Markdown</button>
            <button className="btn-secondary" onClick={()=>exportFile("json", results.tree.id)}>Export JSON</button>
            <button className="btn-secondary" onClick={()=>exportFile("mermaid", results.tree.id)}>Export Mermaid</button>
          </>
        )}
      </div>
    </div>
  );
}
