import { useAppStore } from "../store/useAppStore";
import { useState } from "react";

export default function StateEditor() {
  const { stateConfig, set } = useAppStore();
  const [text, setText] = useState(JSON.stringify(stateConfig, null, 2));
  const apply = () => {
    try { set({ stateConfig: JSON.parse(text) }); } catch {}
  };
  return (
    <div className="bg-white rounded border p-3 space-y-2">
      <h2 className="font-semibold">State Config</h2>
      <textarea className="w-full h-40 font-mono text-sm border rounded p-2" value={text} onChange={e=>setText(e.target.value)} />
      <button className="btn" onClick={apply}>Apply</button>
    </div>
  );
}
