export function resolveTemplates(obj: any, ui: any) {
  const re = /\{\{\s*ui\.([a-zA-Z0-9_]+)\s*\}\}/g;
  const recur = (v: any): any => {
    if (typeof v === "string") return v.replace(re, (_, k) => (ui[k] ?? "").toString());
    if (Array.isArray(v)) return v.map(recur);
    if (v && typeof v === "object") return Object.fromEntries(Object.entries(v).map(([k, val]) => [k, recur(val)]));
    return v;
  };
  return recur(obj);
}
