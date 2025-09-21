import { useAppStore } from "../store/useAppStore";
import { initTree, proposeBranches } from "../lib/api";
import { useState } from "react";
import BranchValidationModal from "./BranchValidationModal";

function NodeItem({ id, level }: { id: string; level: number }) {
  const { tree, set } = useAppStore();
  const node = tree.nodes[id];
  const onPropose = async () => {
    const res = await proposeBranches(tree.id, id);
    set({ selectedNodeId: id, proposals: res.proposals });
  };
  return (
    <div className="pl-2 border-l ml-2">
      <div className="flex items-center gap-2">
        <span className="font-medium">{node.text}</span>
        <button className="text-xs underline" onClick={onPropose}>Propose branches</button>
      </div>
      <div className="space-y-1">
        {node.branches.map((cid: string) => <NodeItem key={cid} id={cid} level={level+1} />)}
      </div>
    </div>
  );
}

export default function TreeView() {
  const { tree, set, proposals } = useAppStore();
  const [rootText, setRootText] = useState("Starting point");
  const [scenario, setScenario] = useState("Career change to tech");

  const init = async () => {
    const t = await initTree(rootText);
    set({ tree: t });
  };

  const initAI = async () => {
    const res = await fetch(`${import.meta.env.VITE_API_URL || "http://localhost:8000/api"}/tree/init/ai`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ scenario }),
    });
    const t = await res.json();
    set({ tree: t });
  };

  return (
    <div className="bg-white rounded border p-3 space-y-2">
      <h2 className="font-semibold">Tree Builder</h2>
      {!tree ? (
        <div className="space-y-2">
          <div className="flex gap-2">
            <input className="input flex-1" placeholder="Root text" value={rootText} onChange={e=>setRootText(e.target.value)} />
            <button className="btn" onClick={init}>Create Root</button>
          </div>
          <div className="flex gap-2">
            <input className="input flex-1" placeholder="Scenario for AI init" value={scenario} onChange={e=>setScenario(e.target.value)} />
            <button className="btn" onClick={initAI}>AI Initialize</button>
          </div>
        </div>
      ) : (
        <div>
          <NodeItem id={tree.root_id} level={0} />
        </div>
      )}
      {proposals.length ? <BranchValidationModal onClose={()=>set({ proposals: [], selectedNodeId: null })} /> : null}
    </div>
  );
}
