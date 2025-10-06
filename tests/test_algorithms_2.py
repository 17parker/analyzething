import pytest
from core import algorithms as alg
from core import heuristics as h


# --- Extra Graph Fixtures ---


@pytest.fixture
def long_chain_graph():
    # Simple chain: 0 → 1 → 2 → 3 → 4
    return {0: [(1, 1)], 1: [(2, 1)], 2: [(3, 1)], 3: [(4, 1)], 4: []}


@pytest.fixture
def weighted_trap_graph():
    # Greedy may take the "wrong" heavier edge
    # 0 → 1 (weight 1), 0 → 2 (weight 2)
    # 1 → 3 (weight 100), 2 → 3 (weight 1)
    # Optimal path = 0 → 2 → 3 = cost 3
    return {0: [(1, 1), (2, 2)], 1: [(3, 100)], 2: [(3, 1)], 3: []}


@pytest.fixture
def cycle_graph():
    # Cycle present: 0 → 1 → 2 → 0, and 2 → 3
    # Optimal path 0 → 1 → 2 → 3
    return {0: [(1, 1)], 1: [(2, 1)], 2: [(0, 1), (3, 1)], 3: []}


@pytest.fixture
def grid_graph():
    # 2x2 grid (0,0) → (1,0), (0,1), etc.
    return {
        (0, 0): [((1, 0), 1), ((0, 1), 1)],
        (1, 0): [((1, 1), 1)],
        (0, 1): [((1, 1), 1)],
        (1, 1): [],
    }


# --- Tests ---


def test_long_chain_graph(long_chain_graph):
    adj = long_chain_graph
    path, cost = alg.bfs(adj, 0, 4)
    assert cost == 4  # BFS counts hops correctly
    path, cost = alg.dijkstra(adj, 0, 4)
    assert cost == 4  # Dijkstra counts weights too


def test_weighted_trap_graph(weighted_trap_graph):
    adj = weighted_trap_graph
    # Dijkstra should find optimal cost = 3
    _, cost = alg.dijkstra(adj, 0, 3)
    assert cost == 3
    # Greedy may take suboptimal path (0→1→3 = 101)
    _, greedy_cost = alg.greedy_best(adj, 0, 3, h.zero)
    assert greedy_cost in (3, 101)


def test_cycle_graph(cycle_graph):
    adj = cycle_graph
    # DFS should still terminate and return *a* path
    path, cost = alg.dfs(adj, 0, 3)
    assert path is not None and path[0] == 0 and path[-1] == 3
    # Dijkstra should return optimal cost 3
    _, cost = alg.dijkstra(adj, 0, 3)
    assert cost == 3


def test_grid_graph(grid_graph):
    adj = grid_graph
    # BFS should find path in 2 hops
    _, cost = alg.bfs(adj, (0, 0), (1, 1))
    assert cost == 2
    # Manhattan heuristic guides Greedy and A*
    _, g_cost = alg.greedy_best(adj, (0, 0), (1, 1), h.manhattan)
    _, a_cost = alg.a_star(adj, (0, 0), (1, 1), h.manhattan)
    assert a_cost == 2  # A* always optimal
    assert g_cost in (
        2,
        float("inf"),
    )  # Greedy may succeed or fail depending on expansion order
