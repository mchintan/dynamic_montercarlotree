import { useState } from "react";
import { useAppStore, ProposedBranch } from "../store/useAppStore";
import { applyBranches } from "../lib/api";

export default function BranchValidationModal({ onClose }: { onClose: () => void }) {
  const { tree, selectedNodeId, proposals, set } = useAppStore();
  if (!selectedNodeId) return null;
  const [local, setLocal] = useState<ProposedBranch[]>(
    (proposals && proposals.length ? proposals : [{ description: "" }, { description: "" }, { description: "" }]).slice(0, 5)
  );

  const update = (idx: number, field: keyof ProposedBranch, val: string) => {
    const copy = [...local];
    (copy[idx] as any)[field] = val;
    setLocal(copy);
  };

  const add = () => {
    if (local.length >= 5) return;
    setLocal([...local, { description: "", rationale: "" }]);
  };

  const remove = (idx: number) => {
    const next = local.filter((_, i) => i !== idx);
    setLocal(next.length >= 2 ? next : next.concat({ description: "" }));
  };

  const confirm = async () => {
    if (!tree || !selectedNodeId) return;
    const cleaned = local.filter(b => b.description && b.description.trim().length > 0).slice(0, 5);
    if (cleaned.length < 2) return;
    const updated = await applyBranches(tree.id, selectedNodeId, cleaned);
    set({ tree: updated, proposals: [], selectedNodeId: null });
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black/30 flex items-center justify-center">
      <div className="bg-white p-4 rounded w-full max-w-lg space-y-3">
        <h3 className="font-semibold">Validate branches</h3>
        <p className="text-xs text-gray-600">Provide 2–5 options. Edit description and rationale as needed.</p>
        <div className="space-y-2 max-h-[60vh] overflow-auto pr-1">
          {local.map((b, i) => (
            <div key={i} className="border rounded p-2 space-y-1">
              <div className="flex items-center gap-2">
                <span className="text-xs text-gray-500">#{i + 1}</span>
                <input className="input flex-1" placeholder="Description" value={b.description} onChange={e=>update(i, "description", e.target.value)} />
                <button className="btn-secondary" onClick={()=>remove(i)}>Remove</button>
              </div>
              <input className="input w-full" placeholder="Rationale (optional)" value={b.rationale || ""} onChange={e=>update(i, "rationale", e.target.value)} />
            </div>
          ))}
        </div>
        <div className="flex justify-between">
          <button className="btn-secondary" onClick={add} disabled={local.length >= 5}>Add option</button>
          <div className="flex gap-2">
            <button className="btn-secondary" onClick={onClose}>Cancel</button>
            <button className="btn" onClick={confirm}>Apply</button>
          </div>
        </div>
      </div>
    </div>
  );
}
