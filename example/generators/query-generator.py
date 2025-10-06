#!/usr/bin/env python3
"""
query-generator.py — Create a query file (src dst per line) from a NetworkX node-link JSON.

Features:
- Random pairs with --count and --seed
- --reachable-only uses weakly-connected components (undirected view) to ensure pairs
  are sampled from the same component (fast precheck)
- Atomic overwrite: output file is ALWAYS replaced (never appended/partially written)
"""

import argparse
import json
import os
import random
import tempfile
from collections import defaultdict, deque
from typing import Dict, List, Tuple


# ---------------- I/O helpers ----------------
def safe_overwrite_text(lines: List[str], out_path: str) -> None:
    """
    Atomically overwrite a text file with provided lines.
    NEW CODE: prevents append/partial writes.
    """
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    dir_name = os.path.dirname(out_path) or "."
    with tempfile.NamedTemporaryFile(
        "w", delete=False, dir=dir_name, suffix=".tmp"
    ) as tmp:
        tmp.write("\n".join(l.rstrip() for l in lines))
        tmp.write("\n")
        tmp_path = tmp.name
    os.replace(tmp_path, out_path)


# ---------------- Graph loading ----------------
def load_nodes_from_node_link(path: str) -> Tuple[List[int], Dict[int, List[int]]]:
    """
    Load a NetworkX node-link JSON and return:
      - nodes: list of node ids (coerced to int when possible)
      - undirected adjacency (dict: node -> list(neighbors))
    """
    with open(path, "r") as f:
        data = json.load(f)

    nodes_raw = data.get("nodes", [])
    links_raw = data.get("links", [])

    nodes: List[int] = []
    for n in nodes_raw:
        nid = n.get("id")
        try:
            nid = int(nid)
        except Exception:
            # keep original if not coercible
            pass
        nodes.append(nid)

    und: Dict[int, List[int]] = defaultdict(list)
    for e in links_raw:
        u = e.get("source")
        v = e.get("target")
        try:
            u = int(u)
        except Exception:
            pass
        try:
            v = int(v)
        except Exception:
            pass
        und[u].append(v)
        und[v].append(u)

    return nodes, dict(und)


# ---------------- Reachability (weak components) ----------------
def weakly_connected_components(und_adj: Dict[int, List[int]]) -> Dict[int, int]:
    """
    Label weakly-connected components using undirected adjacency.
    Returns: comp_id per node.
    """
    comp: Dict[int, int] = {}
    cid = 0
    for start in und_adj.keys():
        if start in comp:
            continue
        cid += 1
        comp[start] = cid
        q = deque([start])
        while q:
            u = q.popleft()
            for v in und_adj.get(u, []):
                if v not in comp:
                    comp[v] = cid
                    q.append(v)
    return comp


# ---------------- Main ----------------
def main():
    ap = argparse.ArgumentParser(
        description="Generate query file (src dst per line) from a Node-Link graph JSON."
    )
    ap.add_argument(
        "--graph",
        required=True,
        help="Path to Node-Link JSON (from graph-generator.py / networkx.node_link_data).",
    )
    ap.add_argument(
        "--out", default="input/queries.txt", help="Output query filename (OVERWRITES)."
    )
    ap.add_argument(
        "--count", type=int, default=300, help="Number of pairs to generate."
    )
    ap.add_argument("--seed", type=int, default=0, help="Random seed.")
    ap.add_argument(
        "--reachable-only",
        action="store_true",
        help="Only sample pairs in the same weakly-connected component (fast filter).",
    )
    args = ap.parse_args()

    random.seed(args.seed)

    nodes, und = load_nodes_from_node_link(args.graph)
    if not nodes:
        raise SystemExit(f"No nodes found in {args.graph}")

    # Prepare component info if requested
    comps: List[List[int]] = (
        []
    )  # define in all branches to avoid 'possibly unbound' warnings
    if args.reachable_only:
        comp_map = weakly_connected_components(und)
        by_c: Dict[int, List[int]] = defaultdict(list)
        for n in nodes:
            if n in comp_map:
                by_c[comp_map[n]].append(n)
        comps = [c for c in by_c.values() if len(c) >= 2]
        if not comps:
            raise SystemExit(
                "No components with ≥2 nodes; cannot produce reachable-only pairs."
            )

    # Helper to sample a pair
    def sample_pair() -> Tuple[int, int]:
        if args.reachable_only:
            c = random.choice(comps)
            s = random.choice(c)
            t = random.choice(c)
            while t == s:
                t = random.choice(c)
            return s, t
        else:
            s = random.choice(nodes)
            t = random.choice(nodes)
            while t == s:
                t = random.choice(nodes)
            return s, t

    # Generate unique ordered pairs (s,t) (note: (s,t) != (t,s))
    pairs = set()
    target = max(1, args.count)
    while len(pairs) < target:
        pairs.add(sample_pair())

    # Format output lines
    lines = [f"{s} {t}" for (s, t) in sorted(pairs)]

    # NEW CODE: atomic overwrite (never append)
    safe_overwrite_text(lines, args.out)
    print(f"[OK] Wrote {len(lines)} queries to {args.out}")


if __name__ == "__main__":
    main()

# Examples:
# python3 example/generators/query-generator.py --graph input/medium_graph.json --out input/medium_queries.txt --count 500 --seed 0
# python3 example/generators/query-generator.py --graph input/medium_graph.json --out input/medium_reach.txt --count 500 --seed 0 --reachable-only
