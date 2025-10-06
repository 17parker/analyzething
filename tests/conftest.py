import pytest


@pytest.fixture
def simple_graph():
    # Trivial 2-node graph
    return {0: [(1, 1)], 1: []}


@pytest.fixture
def disconnected_graph():
    # Two components (0-1 and 2-3), no path from 0 → 3
    return {0: [(1, 1)], 1: [], 2: [(3, 1)], 3: []}


@pytest.fixture
def weighted_graph():
    # DAG with known shortest path cost = 4
    return {0: [(1, 1), (2, 4)], 1: [(2, 2), (3, 5)], 2: [(3, 1)], 3: []}


@pytest.fixture
def cyclic_graph():
    # Graph with cycle, shortest path 0 → 3 has cost = 4
    return {0: [(1, 1)], 1: [(2, 1)], 2: [(0, 1), (3, 2)], 3: []}


@pytest.fixture
def larger_graph():
    # Larger graph, shortest path 0 → 5 has cost = 4
    return {
        0: [(1, 2), (2, 2)],
        1: [(3, 1)],
        2: [(3, 5), (4, 1)],
        3: [(5, 3)],
        4: [(5, 1)],
        5: [],
    }
