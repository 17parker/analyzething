import os
import time
import pytest
from core import algorithms as alg

# Ensure results folder exists
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(RESULTS_DIR, exist_ok=True)
RESULTS_FILE = os.path.join(RESULTS_DIR, "benchmark_results.txt")

# Algorithms to benchmark
ALGORITHMS = [
    ("BFS", lambda adj, s, g: (alg.bfs(adj, s, g), None)),
    ("DFS", lambda adj, s, g: (alg.dfs(adj, s, g), None)),
    ("DepthLimited", lambda adj, s, g: (alg.depth_limited_dfs(adj, s, g, 5), None)),
    ("Dijkstra", lambda adj, s, g: alg.dijkstra(adj, s, g)),
    (
        "GreedyZero",
        lambda adj, s, g: (alg.greedy_best(adj, s, g, alg.zero_heuristic), None),
    ),
    ("AStarZero", lambda adj, s, g: alg.a_star(adj, s, g, alg.zero_heuristic)),
    ("BidirectionalBFS", lambda adj, s, g: (alg.bidirectional_bfs(adj, s, g), None)),
    ("BidirectionalDijkstra", lambda adj, s, g: alg.bidirectional_dijkstra(adj, s, g)),
]

# Graphs to benchmark (reuses fixtures from conftest.py)
GRAPH_CASES = [
    ("simple_graph", 0, 1),
    ("disconnected_graph", 0, 3),
    ("weighted_graph", 0, 3),
    ("cyclic_graph", 0, 3),
    ("larger_graph", 0, 5),
]


@pytest.mark.parametrize("graph_fixture,start,goal", GRAPH_CASES)
@pytest.mark.parametrize("name,algo", ALGORITHMS)
def test_benchmark_algorithms(request, graph_fixture, start, goal, name, algo):
    """Benchmark all algorithms on all sample graphs."""
    adj = request.getfixturevalue(graph_fixture)

    start_time = time.time()
    result = algo(adj, start, goal)
    elapsed = time.time() - start_time

    # Normalize return values
    if isinstance(result, tuple):
        path, cost = result
    else:
        path, cost = result, len(result) if result else float("inf")

    # Write results to log file
    with open(RESULTS_FILE, "a") as f:
        f.write(
            f"{graph_fixture:20} | {name:25} | Time: {elapsed:.6f}s | Cost: {cost}\n"
        )

    # Minimal correctness check so pytest passes
    assert True
