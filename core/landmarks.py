"""
landmarks.py - ALT (A*, Landmarks, Triangle inequality) support.

- select_landmarks: strategies to choose K landmarks
- build_tables: precompute d(L, v) and d_rev(L, v) (i.e., d(v, L))
- alt_heuristic_factory: goal-specific heuristic for A* using precomputed tables
"""

from typing import Dict, List, Tuple, Callable
import heapq
from collections import defaultdict, deque

Adj = Dict[int, List[Tuple[int, float]]]


# ---------------- Basic graph helpers ----------------
def reverse_graph(adj: Adj) -> Adj:
    rev: Adj = defaultdict(list)
    for u, edges in adj.items():
        for v, w in edges:
            rev[v].append((u, w))
    return dict(rev)


def dijkstra_from_source(adj: Adj, src: int) -> Dict[int, float]:
    dist: Dict[int, float] = {src: 0.0}
    pq = [(0.0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in adj.get(u, []):
            nd = d + w
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist


# ---------------- Landmark selection ----------------
def select_landmarks(adj: Adj, k: int) -> List[int]:
    """
    Simple, fast strategy (good enough for 60s budget):
    1) pick the highest-degree node
    2) then iteratively pick the node that maximizes min-distance to the set (farthest-1 approx)
    Falls back to random-ish by degree if distances unavailable.
    """
    if not adj:
        return []
    # Start from a high-degree node
    seed = max(adj.keys(), key=lambda u: len(adj[u]))
    L = [seed]

    # For speed, limit candidate pool to top by degree
    candidates = sorted(adj.keys(), key=lambda u: len(adj[u]), reverse=True)[
        : min(5000, len(adj))
    ]

    for _ in range(1, max(1, k)):
        # compute dist from current landmark set (use last added for cheap approx)
        last = L[-1]
        dist = dijkstra_from_source(adj, last)
        # pick candidate with largest distance to L (min of distances from all L; approximated by last)
        far = max(candidates, key=lambda u: dist.get(u, float("inf")))
        if far not in L:
            L.append(far)
    return L


# ---------------- Table building ----------------
def build_tables(
    adj: Adj, landmarks: List[int]
) -> Tuple[Dict[int, Dict[int, float]], Dict[int, Dict[int, float]]]:
    """
    Returns:
      dist_L_to_v[L][v] = d(L, v) using forward graph
      dist_v_to_L[L][v] = d(v, L) using reverse graph (i.e., distance in reversed graph from L to v)
    """
    dist_L_to_v: Dict[int, Dict[int, float]] = {}
    dist_v_to_L: Dict[int, Dict[int, float]] = {}
    rev = reverse_graph(adj)

    for L in landmarks:
        dist_L_to_v[L] = dijkstra_from_source(adj, L)
        # In the reversed graph, distance from L to v equals original d(v, L)
        dist_v_to_L[L] = dijkstra_from_source(rev, L)

    return dist_L_to_v, dist_v_to_L


# ---------------- Heuristic ----------------
def alt_heuristic_factory(
    goal: int,
    dist_L_to_v: Dict[int, Dict[int, float]],
    dist_v_to_L: Dict[int, Dict[int, float]],
) -> Callable[[int, int], float]:
    """
    Returns h(u, goal) that A* can call.
    Uses both forward and reverse landmark tables.
    """
    # Capture column values for t to avoid dict lookups in the hot loop
    dLt = {L: dist_L_to_v[L].get(goal, float("inf")) for L in dist_L_to_v.keys()}
    dtL = {L: dist_v_to_L[L].get(goal, float("inf")) for L in dist_v_to_L.keys()}

    def h(u: int, v: int) -> float:  # v should equal 'goal'; keep signature consistent
        best = 0.0
        for L in dist_L_to_v.keys():
            dLs = dist_L_to_v[L].get(u, float("inf"))
            dsL = dist_v_to_L[L].get(u, float("inf"))

            # Triangle inequalities (admissible lower bounds). Skip infs safely.
            # |d(L,t) - d(L,s)|
            if dLt[L] < float("inf") and dLs < float("inf"):
                cand = abs(dLt[L] - dLs)
                if cand > best:
                    best = cand
            # |d(s,L) - d(t,L)|
            if dtL[L] < float("inf") and dsL < float("inf"):
                cand = abs(dsL - dtL[L])
                if cand > best:
                    best = cand
        return best

    return h
