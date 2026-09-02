#!/usr/bin/env python3
"""coverage_checklist.py — extract per-node coverage checklist from workflow_graph.json
Usage:
  python coverage_checklist.py <graph.json>            # validate graph only
  python coverage_checklist.py <graph.json> <node-id>  # validate + node checklist
Output: JSON to stdout. Facts/contract only — evidence hunting is Claude's job.
"""
import sys, json

def validate(g):
    errs, warns = [], []
    ids = {n["id"] for n in g.get("nodes", [])}
    rules = g.get("golden_rules", [])
    edges = g.get("edges", [])

    for e in edges:
        for k in ("from", "to"):
            if e.get(k) not in ids:
                errs.append(f"V1: edge {e.get('id','?')} {k}={e.get(k)} ไม่มีใน nodes")
        if not e.get("detail") or len(e.get("detail", "")) < 10:
            errs.append(f"V7: edge {e.get('id','?')} detail ว่าง/สั้นเกิน")
    linked = {e.get("from") for e in edges} | {e.get("to") for e in edges}
    for n in g.get("nodes", []):
        if n["id"] not in linked:
            errs.append(f"V2: node {n['id']} เป็น orphan")
        if n.get("zone") == "core" and n.get("status") != "existing":
            has_rule = any(r.get("node") == n["id"] for r in rules)
            if not has_rule and not n.get("no_rules_reason"):
                warns.append(f"V5: node {n['id']} ไม่มี golden rule และไม่มี no_rules_reason")
    for r in rules:
        if r.get("node") not in ids:
            errs.append(f"V6: rule {r.get('id','?')} อ้าง node {r.get('node')} ที่ไม่มี")

    # V3: cycle in data+config subgraph (DFS)
    adj = {}
    for e in edges:
        if e.get("type") in ("data", "config"):
            adj.setdefault(e["from"], []).append(e["to"])
    state = {}
    def dfs(u, path):
        state[u] = 1
        for v in adj.get(u, []):
            if state.get(v) == 1:
                errs.append(f"V3: cycle (data/config): {' -> '.join(path + [v])}")
            elif state.get(v, 0) == 0:
                dfs(v, path + [v])
        state[u] = 2
    for u in list(adj):
        if state.get(u, 0) == 0:
            dfs(u, [u])
    return errs, warns

def node_checklist(g, node_id):
    ids = {n["id"] for n in g.get("nodes", [])}
    if node_id not in ids:
        return {"error": f"node {node_id} ไม่มีใน graph — มีเฉพาะ: {sorted(ids)}"}
    node = next(n for n in g["nodes"] if n["id"] == node_id)
    edges_in = [e for e in g.get("edges", []) if e.get("to") == node_id]
    edges_out = [e for e in g.get("edges", []) if e.get("from") == node_id]
    rules = [r for r in g.get("golden_rules", []) if r.get("node") == node_id]
    # cross-node rules mentioning this node in text
    cross = [r for r in g.get("golden_rules", [])
             if r.get("node") != node_id and node_id in json.dumps(r, ensure_ascii=False)]
    exceptions = [e for e in edges_in + edges_out if e.get("type") == "reversal"]
    wave = None
    for w in g.get("build_order", {}).get("waves", []):
        if node_id in w.get("nodes", []):
            wave = w.get("wave")
    return {
        "node": node,
        "wave": wave,
        "edges_in": edges_in,
        "edges_out": edges_out,
        "golden_rules_block": [r for r in rules if r.get("severity") == "block"],
        "golden_rules_warn": [r for r in rules if r.get("severity") != "block"],
        "cross_node_rules": cross,
        "exception_paths": exceptions,
        "counts": {
            "edges_in": len(edges_in), "edges_out": len(edges_out),
            "rules_block": sum(1 for r in rules if r.get("severity") == "block"),
            "rules_warn": sum(1 for r in rules if r.get("severity") != "block"),
            "exception_paths": len(exceptions),
        },
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    g = json.load(open(sys.argv[1], encoding="utf-8"))
    errs, warns = validate(g)
    out = {"graph_id": g.get("graph_id"), "version": g.get("version"),
           "validation": {"errors": errs, "warnings": warns,
                          "ok": not errs}}
    if len(sys.argv) > 2:
        out["checklist"] = node_checklist(g, sys.argv[2])
    print(json.dumps(out, ensure_ascii=False, indent=2))
