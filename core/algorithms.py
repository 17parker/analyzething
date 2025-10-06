"""
algorithms.py - Search & Pathfinding algorithms for Large Graph Path Finder
All algorithms return (path, cost):
    - path: list of nodes or None
    - cost: numeric cost or float("inf") if unreachable
"""

import heapq
from collections import deque
from typing import Callable
#from core import heuristics as h
import heuristics as h

# ---------- Aliases for heuristics ----------
zero_heuristic = h.zero
manhattan_heuristic = h.manhattan
euclidean_heuristic = h.euclidean


# ---------- Uninformed Search ----------


def bfs(adj, start, goal):
    """
    Breadth-first search.
    Finds shortest path in terms of *number of edges* (ignores weights).
    """
    visited = set()
    queue = deque([(start, [start])])
    while queue:
        node, path = queue.popleft()
        if node == goal:
            return path, float(len(path) - 1)  # hop count
        if node not in visited:
            visited.add(node)
            for neighbor, _ in adj[node]:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
    return None, float("inf")


def dfs(adj, start, goal):
    """
    Depth-first search.
    Returns *a path* if one exists (not guaranteed to be optimal).
    """
    stack = [(start, [start])]
    visited = set()
    while stack:
        node, path = stack.pop()
        if node == goal:
            return path, float(len(path) - 1)  # hop count
        if node not in visited:
            visited.add(node)
            for neighbor, _ in adj[node]:
                stack.append((neighbor, path + [neighbor]))
    return None, float("inf")


def depth_limited_dfs(adj, start, goal, limit):
    """
    Depth-limited DFS.
    Returns first path found within the depth limit (not necessarily optimal).
    """

    def recurse(node, path, depth):
        if node == goal:
            return path
        if depth == 0:
            return None
        for neighbor, _ in adj[node]:
            result = recurse(neighbor, path + [neighbor], depth - 1)
            if result:
                return result
        return None

    path = recurse(start, [start], limit)
    return (path, float(len(path) - 1)) if path else (None, float("inf"))


# ---------- Weighted Graph Algorithms ----------


def dijkstra(adj, start, goal):
    """Dijkstra’s algorithm for weighted shortest path."""
    pq = [(0, start, [start])]
    visited = {}
    while pq:
        cost, node, path = heapq.heappop(pq)
        if node == goal:
            return path, float(cost)
        if node in visited and visited[node] <= cost:
            continue
        visited[node] = cost
        for neighbor, weight in adj[node]:
            heapq.heappush(pq, (cost + weight, neighbor, path + [neighbor]))
    return None, float("inf")


# ---------- Informed Search ----------


def greedy_best(adj, start, goal, heuristic: Callable = h.zero):
    """
    Greedy Best-First Search.
    Expands nodes with lowest heuristic estimate.
    Not guaranteed to find optimal paths.
    """
    pq = [(heuristic(start, goal), start, [start], 0.0)]
    visited = set()
    while pq:
        _, node, path, cost = heapq.heappop(pq)
        if node == goal:
            return path, cost
        if node not in visited:
            visited.add(node)
            for neighbor, w in adj[node]:
                heapq.heappush(
                    pq,
                    (heuristic(neighbor, goal), neighbor, path + [neighbor], cost + w),
                )
    return None, float("inf")


def a_star(adj, start, goal, heuristic: Callable = h.zero):
    """A* search with configurable heuristic (guarantees optimal if heuristic is admissible)."""
    pq = [(heuristic(start, goal), 0, start, [start])]
    visited = {}
    while pq:
        f, g, node, path = heapq.heappop(pq)
        if node == goal:
            return path, float(g)
        if node in visited and visited[node] <= g:
            continue
        visited[node] = g
        for neighbor, weight in adj[node]:
            new_g = g + weight
            f_val = new_g + heuristic(neighbor, goal)
            heapq.heappush(pq, (f_val, new_g, neighbor, path + [neighbor]))
    return None, float("inf")


# ---------- Bidirectional Search ----------


def bidirectional_bfs(adj, start, goal):
    """
    Bidirectional BFS.
    Works only for unweighted graphs → hop count.
    """
    if start == goal:
        return [start], 0.0

    front, back = {start: [start]}, {goal: [goal]}
    q_front, q_back = deque([start]), deque([goal])

    while q_front and q_back:
        node = q_front.popleft()
        for neighbor, _ in adj[node]:
            if neighbor not in front:
                front[neighbor] = front[node] + [neighbor]
                q_front.append(neighbor)
                if neighbor in back:
                    path = front[neighbor] + back[neighbor][-2::-1]
                    return path, float(len(path) - 1)

        node = q_back.popleft()
        for neighbor, _ in adj[node]:
            if neighbor not in back:
                back[neighbor] = back[node] + [neighbor]
                q_back.append(neighbor)
                if neighbor in front:
                    path = front[neighbor] + back[neighbor][-2::-1]
                    return path, float(len(path) - 1)

    return None, float("inf")


def bidirectional_dijkstra(adj, start, goal):
    """Placeholder: currently same as Dijkstra (optimal weighted)."""
    return dijkstra(adj, start, goal)


def bellman_ford(adj, start, goal):
    """
    Bellman-Ford algorithm. Handles negative weights but slower.
    Complexity: O(VE).
    """
    dist = {u: float("inf") for u in adj}
    prev = {}
    dist[start] = 0.0

    for _ in range(len(adj) - 1):
        updated = False
        for u, edges in adj.items():
            for v, w in edges:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    prev[v] = u
                    updated = True
        if not updated:
            break

    if dist[goal] == float("inf"):
        return None, float("inf")

    # Reconstruct path
    path = [goal]
    while path[-1] in prev:
        path.append(prev[path[-1]])
    path.reverse()
    return path, dist[goal]
