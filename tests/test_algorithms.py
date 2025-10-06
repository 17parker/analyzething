import pytest
from core import algorithms as alg
from core import heuristics as h

# Algorithm categories
ALGORITHMS = [
    ("BFS", lambda adj, s, g: alg.bfs(adj, s, g)),
    ("DFS", lambda adj, s, g: alg.dfs(adj, s, g)),
    ("DepthLimited", lambda adj, s, g: alg.depth_limited_dfs(adj, s, g, 5)),
    ("Dijkstra", lambda adj, s, g: alg.dijkstra(adj, s, g)),
    ("GreedyZero", lambda adj, s, g: alg.greedy_best(adj, s, g, h.zero)),
    ("GreedyManhattan", lambda adj, s, g: alg.greedy_best(adj, s, g, h.manhattan)),
    ("GreedyEuclidean", lambda adj, s, g: alg.greedy_best(adj, s, g, h.euclidean)),
    ("AStarZero", lambda adj, s, g: alg.a_star(adj, s, g, h.zero)),
    ("AStarManhattan", lambda adj, s, g: alg.a_star(adj, s, g, h.manhattan)),
    ("AStarEuclidean", lambda adj, s, g: alg.a_star(adj, s, g, h.euclidean)),
    ("BidirectionalBFS", lambda adj, s, g: alg.bidirectional_bfs(adj, s, g)),
    ("BidirectionalDijkstra", lambda adj, s, g: alg.bidirectional_dijkstra(adj, s, g)),
]


@pytest.mark.parametrize("name,algo", ALGORITHMS)
@pytest.mark.parametrize(
    "graph_fixture,start,goal,expect_type,expect_cost",
    [
        # simple graph: all should succeed
        ("simple_graph", 0, 1, "any", 1),
        # disconnected graph: all should fail
        ("disconnected_graph", 0, 3, "none", None),
        # weighted graph: only Dijkstra/A* must be optimal
        ("weighted_graph", 0, 3, "optimal", 4),
        # cyclic graph: Dijkstra/A* optimal, others may differ
        ("cyclic_graph", 0, 3, "optimal", 4),
        # larger graph: Dijkstra/A* optimal
        ("larger_graph", 0, 5, "optimal", 4),
    ],
)
def test_algorithms_on_graphs(
    request, graph_fixture, start, goal, expect_type, expect_cost, name, algo
):
    adj = request.getfixturevalue(graph_fixture)
    path, cost = algo(adj, start, goal)

    if expect_type == "none":
        # No path should exist
        assert path is None and cost == float("inf")

    elif expect_type == "any":
        # Just check path exists and is valid
        assert path is not None
        assert path[0] == start and path[-1] == goal

    elif expect_type == "optimal":
        if name in [
            "Dijkstra",
            "AStarZero",
            "AStarManhattan",
            "AStarEuclidean",
            "BidirectionalDijkstra",
        ]:
            # Must find optimal path
            assert path is not None
            assert cost == expect_cost
        else:
            # Other algorithms may be suboptimal but should return a path if reachable
            if path:
                assert path[0] == start and path[-1] == goal
