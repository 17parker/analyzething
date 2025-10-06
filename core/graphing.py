"""
graphing.py - Result formatting & output helpers for Large Graph Path Finder.

Responsibilities:
- Turn a path [u0, u1, ..., uk] into "u0-[w01]->u1-[w12]->...->uk".
- Compute total weight from the adjacency/weight map.
- Provide a ready-to-write result line and a convenience writer.
"""

from typing import Dict, List, Tuple, Iterable, Optional


Adjacency = Dict[int, List[Tuple[int, float]]]
WeightMap = Dict[int, Dict[int, float]]  # weight_map[u][v] = w


def build_weight_map(adj: Adjacency) -> WeightMap:
    """
    Build a fast weight lookup dict-of-dicts: weight_map[u][v] = w.
    Call this once and reuse.
    """
    wm: WeightMap = {}
    for u, edges in adj.items():
        u_map = wm.setdefault(u, {})
        for v, w in edges:
            u_map[v] = w
    return wm


def edge_weight(weight_map: WeightMap, u: int, v: int) -> Optional[float]:
    """
    Retrieve weight for directed edge (u -> v). Returns None if missing.
    """
    w = weight_map.get(u, {}).get(v)
    return w


def path_to_edge_string(path: List[int], weight_map: WeightMap) -> Tuple[str, float]:
    """
    Convert a node path into a labeled edge sequence and compute total weight.

    Example:
    [1,2,3,4] + weights -> "1-[36]->2-[1]->3-[45]->4", total_weight
    """
    if not path or len(path) == 1:
        return (str(path[0]) if path else "[]", 0.0)

    parts: List[str] = [str(path[0])]
    total = 0.0

    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        w = edge_weight(weight_map, u, v)
        if w is None:
            # Edge missing in the map -> inconsistent adjacency or wrong direction.
            # Fall back to unknown marker (still produce a readable line).
            parts.append(f"-[?]->{v}")
        else:
            total += float(w)
            parts.append(f"-[{w}]->{v}")

    return ("".join(parts), total)


def format_result_line(
    src: int,
    dst: int,
    path: List[int],
    elapsed_sec: float,
    weight_map: WeightMap,
) -> str:
    """
    Produce a single, human-friendly result line.

    If path exists:
      "1 4 | 82.0 | 0.000351 | 1-[36]->2-[1]->3-[45]->4"
    Else:
      "1 4 | inf | 0.000210 | []"
    """
    if path:
        edge_str, total = path_to_edge_string(path, weight_map)
        return f"{src} {dst} | {total} | {elapsed_sec:.6f} | {edge_str}"
    else:
        return f"{src} {dst} | inf | {elapsed_sec:.6f} | []"


def write_results(
    out_path: str,
    header_lines: Iterable[str],
    result_lines: Iterable[str],
) -> None:
    """
    Write a header + many result lines to out_path.
    """
    with open(out_path, "w") as out:
        for h in header_lines:
            out.write(h.rstrip() + "\n")
        for line in result_lines:
            out.write(line.rstrip() + "\n")
