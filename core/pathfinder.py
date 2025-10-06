"""
pathfinder.py - Algorithm selector + preprocessing for Large Graph Path Finder.

Exports:
    preprocess_index(adj) -> dict
    choose_algorithm(adj, index=None) -> callable
    find_path(adj, start, goal, index=None) -> (path, cost)

Preprocessing:
- weight_map[u][v] = w
- weakly-connected components (undirected view) for fast reachability checks
- optional ALT (A*, Landmarks, Triangle inequality) tables for large graphs

Notes:
- We do NOT enumerate all possible paths (exponential).
- We do build quick indexes so queries are fast to reject (unreachable)
  and fast to pretty-print (edge weights).
"""

from collections import deque, defaultdict
from typing import Dict, List, Tuple, Callable, Optional
from algorithms import *
import algorithms as alg
from landmarks import *
from typing import TypedDict


class Index(TypedDict, total=False):
    weight_map: Dict[int, Dict[int, float]]
    weak_components: Dict[int, int]
    uniform_weights: bool
    node_count: int
    edge_count: int
    landmarks: List[int]
    dist_L_to_v: Dict[int, Dict[int, float]]
    dist_v_to_L: Dict[int, Dict[int, float]]


Adjacency = Dict[int, List[Tuple[int, float]]]


# ---------------- Internal helpers ----------------
def _build_weight_map(adj: Adjacency) -> Dict[int, Dict[int, float]]:
    wm: Dict[int, Dict[int, float]] = {}
    for u, edges in adj.items():
        m = wm.setdefault(u, {})
        for v, w in edges:
            m[v] = w
    return wm


def _build_weak_components(adj: Adjacency) -> Dict[int, int]:
    """
    Build weakly-connected components (treat each directed edge as undirected).
    Returns comp_id per node. Nodes in same comp_id are potentially reachable.
    """
    und: Dict[int, List[int]] = defaultdict(list)
    for u, edges in adj.items():
        for v, _ in edges:
            und[u].append(v)
            und[v].append(u)

    comp: Dict[int, int] = {}
    cid = 0
    for start in adj.keys():
        if start in comp:
            continue
        cid += 1
        comp[start] = cid
        q = deque([start])
        while q:
            x = q.popleft()
            for y in und.get(x, []):
                if y not in comp:
                    comp[y] = cid
                    q.append(y)
    return comp


def _reachable(index: Optional[Index], s: int, g: int) -> bool:
    if not index:
        return True
    comp = index.get("weak_components", {})
    if not comp:
        return True
    return comp.get(s) == comp.get(g)


# ---------------- Preprocessing ----------------
def preprocess_index(adj: Adjacency, stop_flag=None) -> Index:
    """
    Build reusable indexes for queries:
      - weight_map: fast edge weight lookup
      - weak_components: quick reachability check
      - basic stats (node_count, edge_count, uniform_weights)
      - optional: landmarks + ALT distance tables for large graphs
      - Supports early abort if stop_flag["abort"] is set.
    """
    weight_map: Dict[int, Dict[int, float]] = {}
    for u, edges in adj.items():
        if stop_flag and stop_flag.get("abort"):
            print("[INFO] Aborting weight_map build early.")
            break
        m = weight_map.setdefault(u, {})
        for v, w in edges:
            m[v] = w

    weak_components: Dict[int, int] = {}
    if not (stop_flag and stop_flag.get("abort")):
        weak_components = _build_weak_components(adj)

    weights = [w for edges in adj.values() for _, w in edges]
    uniform = all((w == 1 or w == 1.0) for w in weights) if weights else True

    index: Index = {
        "weight_map": weight_map,
        "weak_components": weak_components,
        "uniform_weights": uniform,
        "node_count": len(adj),
        "edge_count": len(weights),
    }

    if not (stop_flag and stop_flag.get("abort")) and len(adj) >= 10000:
        L = landmarks.select_landmarks(adj, k=12)
        dist_L_to_v, dist_v_to_L = landmarks.build_tables(adj, L)
        index.update(
            {
                "landmarks": L,
                "dist_L_to_v": dist_L_to_v,
                "dist_v_to_L": dist_v_to_L,
            }
        )

    return index


# ---------------- Algorithm chooser ----------------
def choose_algorithm(adj: Adjacency, index: Optional[Index] = None):
    """
    Decide which algorithm to use based on graph profile:
      - If ALT tables exist → A* + ALT
      - If negative weights exist → Bellman–Ford
      - If large graph (>10k nodes) → A* with zero heuristic
      - If unweighted → BFS
      - Else → Dijkstra
    """
    idx = index or {}
    node_count_val = idx.get("node_count", len(adj))
    node_count = (
        int(node_count_val)
        if isinstance(node_count_val, (int, float, str))
        else len(adj)
    )
    uniform = idx.get("uniform_weights", True)

    # ALT support
    if "landmarks" in idx:

        def _strategy(a, s, g):
            dist_L_to_v = idx.get("dist_L_to_v", {})
            dist_v_to_L = idx.get("dist_v_to_L", {})
            h = landmarks.alt_heuristic_factory(
                g,
                dist_L_to_v if isinstance(dist_L_to_v, dict) else {},
                dist_v_to_L if isinstance(dist_v_to_L, dict) else {},
            )
            return alg.a_star(a, s, g, h)

        _strategy.__name__ = "AStar_ALT"
        return _strategy

    # Bellman-Ford fallback for negative weights
    if any(w < 0 for edges in adj.values() for _, w in edges):
        return alg.bellman_ford

    # Large graph heuristic
    if node_count > 10000:
        return lambda a, s, g: alg.a_star(a, s, g, alg.zero_heuristic)

    # Small unweighted
    if uniform:
        return alg.bfs

    # Default
    return alg.dijkstra


# ---------------- Path wrapper ----------------
def find_path(adj: Adjacency, start: int, goal: int, index: Optional[Index] = None):
    """
    Wrapper to check cheap reachability first, then run the chosen algorithm.
    """
    if start == goal:
        return [start], 0.0

    if not _reachable(index, start, goal):
        return None, float("inf")

    algorithm = choose_algorithm(adj, index)
    return algorithm(adj, start, goal)
