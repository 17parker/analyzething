import argparse
import json
import random
import os
import tempfile
import shutil

import networkx as nx
import matplotlib.pyplot as plt


def generate_random_graph(num_vertices, num_edges, min_weight, max_weight, seed=None):
    if seed is not None:
        random.seed(seed)
    G = nx.gnm_random_graph(num_vertices, num_edges, seed=seed)
    for u, v in G.edges():
        G.edges[u, v]["weight"] = random.randint(min_weight, max_weight)
    return G


def safe_overwrite_json(data_obj, out_path):
    """
    NEW CODE: atomically overwrite JSON (never append).
    Writes to a temp file then replaces the target to avoid partial files.
    """
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    dir_name = os.path.dirname(out_path) or "."
    with tempfile.NamedTemporaryFile(
        "w", delete=False, dir=dir_name, suffix=".tmp"
    ) as tmp:
        json.dump(data_obj, tmp, indent=2)
        tmp_path = tmp.name
    # Atomic replace on POSIX
    os.replace(tmp_path, out_path)


def save_graph_image(G, img_out):
    if not img_out:
        return
    os.makedirs(os.path.dirname(img_out) or ".", exist_ok=True)
    # if G.number_of_nodes() <= 100:
    if G.number_of_nodes() <= 1000:
        pos = nx.spring_layout(G, seed=42)
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.savefig(img_out)
        plt.close()
    else:
        # print("There are too many nodes to draw the graph (more than 100).")
        print("There are too many nodes to draw the graph (more than 1000).")


def main():
    parser = argparse.ArgumentParser(description="Generate a random weighted graph.")
    parser.add_argument(
        "--min_weight", type=int, required=True, help="Minimum edge weight"
    )
    parser.add_argument(
        "--max_weight", type=int, required=True, help="Maximum edge weight"
    )
    parser.add_argument("--num_edges", type=int, required=True, help="Number of edges")
    parser.add_argument(
        "--num_vertices", type=int, required=True, help="Number of vertices"
    )
    parser.add_argument(
        "--json_out", type=str, default="input/graph.json", help="Output JSON filename"
    )
    parser.add_argument(
        "--img_out", type=str, default="input/graph.png", help="Output image filename"
    )
    parser.add_argument(
        "--seed", type=int, default=None, help="Random seed for reproducibility"
    )
    args = parser.parse_args()

    G = generate_random_graph(
        args.num_vertices,
        args.num_edges,
        args.min_weight,
        args.max_weight,
        seed=args.seed,
    )

    # ----------------------------- ORIGINAL CODE (commented) -----------------------------
    # data = nx.node_link_data(G)
    # with open(args.json_out, 'w') as f:        # 'w' truncates, but this is the old path
    #     json.dump(data, f, indent=2)
    #
    # if args.img_out and G.number_of_nodes() <= 100:
    #     pos = nx.spring_layout(G)
    #     edge_labels = nx.get_edge_attributes(G, 'weight')
    #     nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray')
    #     nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    #     plt.savefig(args.img_out)
    #     plt.close()
    # elif args.img_out and G.number_of_nodes() > 100:
    #     print("There are too many nodes to draw the graph (more than 100).")
    # ------------------------------------------------------------------------------------

    # ------------------------------ NEW CODE (atomic overwrite) -------------------------
    data = nx.node_link_data(G)
    safe_overwrite_json(data, args.json_out)  # guaranteed overwrite, never append
    save_graph_image(G, args.img_out)
    # ------------------------------------------------------------------------------------

    print(f"[OK] Wrote graph JSON: {args.json_out}")
    if args.img_out:
        print(f"[OK] Image (if small enough): {args.img_out}")


if __name__ == "__main__":
    main()

# Example:
# python3 example/generators/graph-generator.py --num_vertices 5000 --num_edges 15000 --min_weight 1 --max_weight 50 --json_out input/medium_graph.json --img_out input/medium_graph.png --seed 0
# python3 example/generators/graph-generator.py --num_vertices 5000 --num_edges 15000 --min_weight 1 --max_weight 50 --json_out input/medium_graph.json --img_out input/medium_graph.png --seed 0
