import React, { useMemo, useCallback } from "react";
import ReactFlow, { Background, Controls, Node as RFNode, Edge as RFEdge, MiniMap, addEdge, OnConnect } from "reactflow";
import "reactflow/dist/style.css";
import { useAppStore } from "../store/useAppStore";
import { proposeBranches } from "../lib/api";

export default function GraphView() {
  const { tree, set } = useAppStore();
  const nodes: RFNode[] = useMemo(() => {
    if (!tree) return [];
    return Object.values(tree.nodes).map((n: any, idx: number) => ({
      id: n.id,
      data: { label: n.text },
      position: { x: (idx % 5) * 200, y: Math.floor(idx / 5) * 120 },
    }));
  }, [tree]);
  const edges: RFEdge[] = useMemo(() => {
    if (!tree) return [];
    const list: RFEdge[] = [];
    Object.values(tree.nodes).forEach((n: any) => {
      n.branches.forEach((cid: string, i: number) => {
        list.push({ id: `${n.id}-${cid}`, source: n.id, target: cid });
      });
    });
    return list;
  }, [tree]);

  const onNodeDoubleClick = useCallback(async (_: any, node: RFNode) => {
    if (!tree) return;
    const res = await proposeBranches(tree.id, node.id);
    set({ selectedNodeId: node.id, proposals: res.proposals });
  }, [tree, set]);

  const onConnect: OnConnect = useCallback((_params) => {
  }, []);

  if (!tree) return (
    <div className="bg-white rounded border p-3">
      <h2 className="font-semibold">Graph</h2>
      <p className="text-sm text-gray-600">Initialize a tree to view graph.</p>
    </div>
  );

  return (
    <div className="bg-white rounded border p-3 h-[500px]">
      <h2 className="font-semibold mb-2">Graph</h2>
      <div className="h-[440px] border rounded">
        <ReactFlow nodes={nodes} edges={edges} onConnect={onConnect} onNodeDoubleClick={onNodeDoubleClick} fitView>
          <MiniMap />
          <Controls />
          <Background />
        </ReactFlow>
      </div>
      <p className="text-xs text-gray-500 mt-1">Tip: Double-click a node to propose branches.</p>
    </div>
  );
}
