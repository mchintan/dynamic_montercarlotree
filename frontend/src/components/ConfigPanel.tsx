import { useAppStore } from "../store/useAppStore";
import { useState } from "react";

export default function ConfigPanel() {
  const { ui, set } = useAppStore();
  const [local, setLocal] = useState(ui);
  const apply = () => set({ ui: local });
  return (
    <div className="bg-white rounded border p-3 space-y-2">
      <h2 className="font-semibold">MCTS Parameters</h2>
      <div className="grid grid-cols-2 gap-2">
        <label className="text-sm">num_simulations
          <input className="input" type="number" value={local.num_simulations} onChange={e=>setLocal({...local,num_simulations:+e.target.value})}/>
        </label>
        <label className="text-sm">max_depth
          <input className="input" type="number" value={local.max_depth} onChange={e=>setLocal({...local,max_depth:+e.target.value})}/>
        </label>
        <label className="text-sm">exploration_c
          <input className="input" type="number" step="0.001" value={local.exploration_c} onChange={e=>setLocal({...local,exploration_c:+e.target.value})}/>
        </label>
        <label className="text-sm">time_budget_ms
          <input className="input" type="number" value={local.time_budget_ms||""} onChange={e=>setLocal({...local,time_budget_ms:e.target.value?+e.target.value:undefined})}/>
        </label>
        <label className="text-sm">random_seed
          <input className="input" type="number" value={local.random_seed||""} onChange={e=>setLocal({...local,random_seed:e.target.value?+e.target.value:undefined})}/>
        </label>
        <label className="text-sm">golden_path_criterion
          <select className="input" value={local.golden_path_criterion} onChange={e=>setLocal({...local,golden_path_criterion:e.target.value})}>
            <option value="avg_reward">avg_reward</option>
            <option value="visits">visits</option>
          </select>
        </label>
      </div>
      <button className="btn" onClick={apply}>Apply</button>
    </div>
  );
}
