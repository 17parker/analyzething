"""
heuristics.py - Heuristic functions for search algorithms.
"""

import math
from typing import Union, Tuple

Node = Union[int, Tuple[float, float]]


def zero(u: Node, v: Node) -> float:
    return 0.0


def manhattan(u: Node, v: Node) -> float:
    if isinstance(u, int) and isinstance(v, int):
        return abs(u - v)
    elif isinstance(u, tuple) and isinstance(v, tuple) and len(u) == 2 and len(v) == 2:
        return abs(u[0] - v[0]) + abs(u[1] - v[1])
    else:
        raise TypeError("Both arguments must be int or tuple of length 2.")


def euclidean(u: Node, v: Node) -> float:
    if isinstance(u, int) and isinstance(v, int):
        return abs(u - v)
    elif isinstance(u, tuple) and isinstance(v, tuple) and len(u) == 2 and len(v) == 2:
        return math.sqrt((u[0] - v[0]) ** 2 + (u[1] - v[1]) ** 2)
    else:
        raise TypeError("Both arguments must be int or tuple of length 2.")


def chebyshev(u: Node, v: Node) -> float:
    if isinstance(u, int) and isinstance(v, int):
        return abs(u - v)
    elif isinstance(u, tuple) and isinstance(v, tuple) and len(u) == 2 and len(v) == 2:
        return max(abs(u[0] - v[0]), abs(u[1] - v[1]))
    else:
        raise TypeError("Both arguments must be int or tuple of length 2.")


def octile(u: Node, v: Node) -> float:
    if isinstance(u, int) and isinstance(v, int):
        return abs(u - v)
    elif isinstance(u, tuple) and isinstance(v, tuple) and len(u) == 2 and len(v) == 2:
        dx, dy = abs(u[0] - v[0]), abs(u[1] - v[1])
        return max(dx, dy) + (math.sqrt(2) - 1) * min(dx, dy)
    else:
        raise TypeError("Both arguments must be int or tuple of length 2.")


def haversine(u: Node, v: Node) -> float:
    if isinstance(u, tuple) and isinstance(v, tuple) and len(u) == 2 and len(v) == 2:
        R = 6371  # Earth radius in km
        lat1, lon1 = map(math.radians, u)
        lat2, lon2 = map(math.radians, v)
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        )
        return 2 * R * math.asin(math.sqrt(a))
    else:
        raise TypeError("Haversine requires tuple of length 2 (lat, lon).")


# A* with Landmarks and the Triangle inequality
# Query (source s, target t): A* uses this heuristic

# h(s, t) = max over landmarks L of:
#           | d(L, t) - d(L, s) |   (forward table)
#           | d(s, L) - d(t, L) |   (reverse table)
