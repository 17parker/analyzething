#!/usr/bin/env python3
"""
plot_benchmarks.py - parse benchmark_results.txt and plot algorithm performance.

Reads:  tests/results/benchmark_results.txt
Writes: tests/results/benchmark_plot_<graph>.png
"""

import os
import re
import matplotlib.pyplot as plt
from collections import defaultdict
import warnings

# Silence numpy longdouble warning
warnings.filterwarnings("ignore", category=UserWarning, module="numpy")

RESULTS_FILE = os.path.join("tests", "results", "benchmark_results.txt")
PLOT_OUT_DIR = os.path.join("tests", "results")

os.makedirs(PLOT_OUT_DIR, exist_ok=True)

# Regex to parse lines like:
# weighted_graph     | Dijkstra              | Time: 0.000004s | Cost: 4.0
LINE_RE = re.compile(
    r"^(?P<graph>\S+)\s+\|\s+(?P<algo>.+?)\s+\|\s+Time:\s+(?P<time>[0-9.eE+-]+)s\s+\|\s+Cost:\s+(?P<cost>\S+)"
)


def parse_results():
    data = defaultdict(list)  # graph -> list of (algo, time, cost)
    if not os.path.exists(RESULTS_FILE):
        raise FileNotFoundError(f"Benchmark results not found: {RESULTS_FILE}")

    with open(RESULTS_FILE) as f:
        for line in f:
            m = LINE_RE.match(line.strip())
            if not m:
                continue
            graph = m["graph"]
            algo = m["algo"].strip()
            time = float(m["time"])
            cost = m["cost"]
            data[graph].append((algo, time, cost))
    return data


def plot_data(data):
    for graph, entries in data.items():
        algos = [a for a, _, _ in entries]
        times = [t for _, t, _ in entries]

        plt.figure(figsize=(10, 6))
        plt.barh(algos, times, color="skyblue")
        plt.xlabel("Time (s)")
        plt.title(f"Benchmark runtimes on {graph}")
        plt.tight_layout()

        out_file = os.path.join(PLOT_OUT_DIR, f"benchmark_plot_{graph}.png")
        plt.savefig(out_file)
        print(f"Saved plot: {out_file}")
        plt.close()


def main():
    data = parse_results()
    plot_data(data)


if __name__ == "__main__":
    main()
