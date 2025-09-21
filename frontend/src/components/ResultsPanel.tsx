import { useAppStore } from "../store/useAppStore";

export default function ResultsPanel() {
  const { results } = useAppStore();
  if (!results) return (
    <div className="bg-white rounded border p-3">
      <h2 className="font-semibold">Results</h2>
      <p className="text-sm text-gray-600">Run a simulation to see results.</p>
    </div>
  );
  return (
    <div className="bg-white rounded border p-3 space-y-2">
      <h2 className="font-semibold">Results</h2>
      <div className="text-sm">Nodes: {results.stats.num_nodes} | Root visits: {results.stats.root_visits}</div>
      <div>
        <h3 className="font-semibold">Golden Path</h3>
        <ol className="list-decimal ml-6">
          {results.golden_path.map((nid: string) => (<li key={nid}><code>{nid}</code></li>))}
        </ol>
      </div>
    </div>
  );
}
