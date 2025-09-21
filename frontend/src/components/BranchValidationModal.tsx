import { useAppStore } from "../store/useAppStore";
import { applyBranches } from "../lib/api";

export default function BranchValidationModal({ onClose }: { onClose: () => void }) {
  const { tree, selectedNodeId, proposals, set } = useAppStore();
  const toggle = (p: string) => {
    const chosen = new Set(proposals as any);
    if (chosen.has(p)) chosen.delete(p);
    else chosen.add(p);
    set({ proposals: Array.from(chosen) as any });
  };
  const confirm = async () => {
    if (!tree || !selectedNodeId) return;
    const updated = await applyBranches(tree.id, selectedNodeId, proposals);
    set({ tree: updated, proposals: [], selectedNodeId: null });
    onClose();
  };
  if (!proposals.length) return null;
  return (
    <div className="fixed inset-0 bg-black/30 flex items-center justify-center">
      <div className="bg-white p-4 rounded w-full max-w-md space-y-2">
        <h3 className="font-semibold">Validate branches</h3>
        <ul className="space-y-1">
          {proposals.map((p) => (
            <li key={p} className="flex items-center gap-2">
              <input type="checkbox" checked={true} onChange={()=>toggle(p)} />
              <span>{p}</span>
            </li>
          ))}
        </ul>
        <div className="flex gap-2 justify-end">
          <button className="btn" onClick={confirm}>Apply</button>
          <button className="btn-secondary" onClick={onClose}>Cancel</button>
        </div>
      </div>
    </div>
  );
}
