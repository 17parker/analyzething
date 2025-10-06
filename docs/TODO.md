🔹 Uninformed / Classical

Iterative Deepening DFS (IDDFS) → combines DFS’s memory efficiency with BFS’s completeness.

Uniform Cost Search (UCS) → a generalization of Dijkstra (already covered by Dijkstra, but nice for teaching clarity).

🔹 Advanced Pathfinding

Bellman-Ford Algorithm → handles graphs with negative edge weights (not supported by Dijkstra).

Floyd–Warshall Algorithm → computes all-pairs shortest paths (useful if you’ll query many node pairs).

Johnson’s Algorithm → more efficient than Floyd–Warshall for sparse graphs with many queries.

🔹 Heuristic / Search Variants

IDA* (Iterative Deepening A*) → more memory efficient than A* for large graphs.

Weighted A* → introduces a factor w to bias heuristics, trading optimality for speed.

Landmark-based Heuristics → precompute distances to/from selected “landmarks” to speed up A*.

🔹 Other Useful Techniques

Minimum Spanning Tree (Prim/Kruskal) → not exactly shortest-path, but useful if your project expands into connectivity problems.

Bidirectional A* → combines bidirectional and heuristic search, very fast for large sparse graphs.

📌 My Recommendation

For your project scope (efficient pathfinding with preprocessing under 60s and ≤1GB memory):

Add IDDFS → improves completeness vs DFS.

Add Bellman-Ford → covers negative weights.

Add Floyd–Warshall or Johnson’s → if you need many queries per graph.

Add Bidirectional A* → huge speed boost on big graphs.

Keep heuristics separate (heuristics.py), and maybe add landmark heuristics later.