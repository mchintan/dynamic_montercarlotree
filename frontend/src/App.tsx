import ConfigPanel from "./components/ConfigPanel";
import StateEditor from "./components/StateEditor";
import DecisionsEditor from "./components/DecisionsEditor";
import TreeView from "./components/TreeView";
import SimulationPanel from "./components/SimulationPanel";
import ResultsPanel from "./components/ResultsPanel";
import GraphView from "./components/GraphView";

function Classes() {
  return (
    <style>{`
      .btn{ @apply bg-blue-600 text-white px-3 py-1.5 rounded hover:bg-blue-700; }
      .btn-secondary{ @apply bg-gray-200 px-3 py-1.5 rounded hover:bg-gray-300; }
      .input{ @apply border rounded px-2 py-1 w-full; }
    `}</style>
  );
}

export default function App() {
  return (
    <div className="p-4 grid grid-cols-1 lg:grid-cols-3 gap-4">
      <Classes />
      <div className="space-y-4">
        <ConfigPanel />
        <StateEditor />
        <DecisionsEditor />
      </div>
      <div className="lg:col-span-2 space-y-4">
        <TreeView />
        <GraphView />
        <SimulationPanel />
        <ResultsPanel />
      </div>
    </div>
  );
}
