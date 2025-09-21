export const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

export async function initTree(text: string) {
  const res = await fetch(`${API_URL}/tree/init?text=${encodeURIComponent(text)}`, { method: "POST" });
  return res.json();
}
export async function proposeBranches(treeId: string, nodeId: string, context?: any) {
  const res = await fetch(`${API_URL}/tree/${treeId}/propose`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ node_id: nodeId, context }),
  });
  return res.json();
}
export async function applyBranches(treeId: string, nodeId: string, branches: string[]) {
  const res = await fetch(`${API_URL}/tree/${treeId}/apply-branches?node_id=${nodeId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(branches),
  });
  return res.json();
}
export async function simulate(treeId: string, payload: any) {
  const res = await fetch(`${API_URL}/simulate/${treeId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return res.json();
}
