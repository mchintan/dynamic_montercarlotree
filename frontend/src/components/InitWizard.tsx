import { useState } from "react";
import { useAppStore } from "../store/useAppStore";
import { initTree } from "../lib/api";

export default function InitWizard() {
  const { tree, set } = useAppStore();
  const [startingPoint, setStartingPoint] = useState("");
  const [desiredGoal, setDesiredGoal] = useState("");
  const [constraints, setConstraints] = useState("");
  const [evaluationCriteria, setEvaluationCriteria] = useState("feasibility and effectiveness");
  const [confirmed, setConfirmed] = useState(false);

  const submitInfo = () => {
    setConfirmed(true);
  };

  const init = async () => {
    const rootText = startingPoint || "New scenario";
    const t = await initTree(rootText);
    t.nodes[t.root_id].metadata = {
      ...(t.nodes[t.root_id].metadata || {}),
      goal: desiredGoal || null,
      constraints: constraints || null,
      evaluation_criteria: evaluationCriteria || null,
    };
    set({ tree: t });
  };

  if (tree) return null;

  return (
    <div className="bg-white rounded border p-4 space-y-3">
      <h2 className="font-semibold">Phase 1: Initialize</h2>
      {!confirmed ? (
        <>
          <p className="text-sm text-gray-600">
            I'll help you explore your decision using MCTS — we'll build a decision tree together, then I'll run simulations to find the best path.
          </p>
          <div className="grid grid-cols-1 gap-2">
            <label className="text-sm">Starting point
              <input className="input w-full" placeholder="What's your starting situation?" value={startingPoint} onChange={e=>setStartingPoint(e.target.value)} />
            </label>
            <label className="text-sm">Desired goal
              <input className="input w-full" placeholder="What's your ideal outcome?" value={desiredGoal} onChange={e=>setDesiredGoal(e.target.value)} />
            </label>
            <label className="text-sm">Constraints
              <input className="input w-full" placeholder="Any constraints or limitations?" value={constraints} onChange={e=>setConstraints(e.target.value)} />
            </label>
            <label className="text-sm">Evaluation criteria
              <input className="input w-full" placeholder="How to measure success?" value={evaluationCriteria} onChange={e=>setEvaluationCriteria(e.target.value)} />
            </label>
          </div>
          <div className="flex justify-end">
            <button className="btn" onClick={submitInfo} disabled={!startingPoint || !desiredGoal}>Continue</button>
          </div>
        </>
      ) : (
        <>
          <div className="text-sm">
            Let me confirm: You're starting from <b>{startingPoint}</b>, aiming for <b>{desiredGoal}</b>, with constraints <b>{constraints || "none"}</b>. Is this correct?
          </div>
          <div className="flex gap-2 justify-end">
            <button className="btn-secondary" onClick={()=>setConfirmed(false)}>Edit</button>
            <button className="btn" onClick={init}>Yes, initialize</button>
          </div>
        </>
      )}
    </div>
  );
}
