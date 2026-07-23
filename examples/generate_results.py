"""
Arch-Spatial-Intelligence — Result Visualizations
=================================================
Generates the real figures committed under results/.

Every number plotted here comes from the actual analyzer
(SpatialAnalyzer / SpaceGraph) — nothing is hand-set.
Run:  python examples/generate_results.py
Output: results/space_graph_*.png, results/metrics_compare.png,
        results/analysis_report.json
"""
import os
import sys
import json

import matplotlib
matplotlib.use("Agg")  # headless / CI safe
import matplotlib.pyplot as plt
import networkx as nx

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.spatial_analyzer import SpatialAnalyzer
from src.space_graph import SpaceGraph

ROOT = os.path.join(os.path.dirname(__file__), "..")
RESULTS = os.path.join(ROOT, "results")
os.makedirs(RESULTS, exist_ok=True)

# ---------------------------------------------------------------------------
# Real design schemes (room dicts: name, area m2, type, connections by index)
# ---------------------------------------------------------------------------
SCHEMES = {
    "Central Courtyard": [
        {"name": "Courtyard", "area": 200, "type": "public", "connections": [1, 2]},
        {"name": "Lecture Hall", "area": 180, "type": "public", "connections": [0, 2]},
        {"name": "Corridor", "area": 60, "type": "circulation", "connections": [0, 1]},
    ],
    "Linear Corridor": [
        {"name": "Entrance", "area": 80, "type": "public", "connections": [1]},
        {"name": "Main Corridor", "area": 120, "type": "circulation", "connections": [0, 2]},
        {"name": "Exhibition", "area": 200, "type": "public", "connections": [1]},
    ],
    "Campus Library": [
        {"name": "Entrance Hall", "area": 120, "type": "public", "connections": [1, 2]},
        {"name": "Reading Room", "area": 300, "type": "public", "connections": [0, 3, 4]},
        {"name": "Stacks", "area": 200, "type": "private", "connections": [0, 3]},
        {"name": "Study Area", "area": 150, "type": "public", "connections": [1, 2]},
        {"name": "Corridor", "area": 80, "type": "circulation", "connections": [1]},
    ],
}

TYPE_COLOR = {
    "public": "#4C72B0",
    "private": "#C44E52",
    "circulation": "#DD8452",
}


def build_graph(name, rooms):
    """Build a networkx graph from the analyzer's room model."""
    g = nx.Graph()
    for i, r in enumerate(rooms):
        g.add_node(i, label=r["name"], area=r["area"], type=r.get("type", "public"))
    for i, r in enumerate(rooms):
        for j in r.get("connections", []):
            if j < len(rooms) and not g.has_edge(i, j):
                g.add_edge(i, j)
    return g


def render_space_graph(name, rooms):
    """Render the spatial connectivity graph (node size = area, color = type)."""
    g = build_graph(name, rooms)
    pos = nx.spring_layout(g, seed=42)
    areas = [g.nodes[n]["area"] for n in g.nodes]
    sizes = [300 + a * 4 for a in areas]
    colors = [TYPE_COLOR.get(g.nodes[n]["type"], "#999999") for n in g.nodes]

    fig, ax = plt.subplots(figsize=(6.5, 5))
    nx.draw_networkx_edges(g, pos, ax=ax, alpha=0.5, width=2)
    nx.draw_networkx_nodes(
        g, pos, ax=ax, node_size=sizes, node_color=colors, edgecolors="white", linewidths=1.5
    )
    labels = {n: g.nodes[n]["label"] for n in g.nodes}
    nx.draw_networkx_labels(g, pos, labels=labels, ax=ax, font_size=9)

    ax.set_title(f"Spatial Graph — {name}", fontsize=13, fontweight="bold")
    ax.axis("off")

    # legend
    from matplotlib.patches import Patch
    legend = [Patch(color=c, label=t) for t, c in TYPE_COLOR.items()]
    ax.legend(handles=legend, loc="lower right", fontsize=8, frameon=False)

    out = os.path.join(RESULTS, f"space_graph_{name.replace(' ', '_').lower()}.png")
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    plt.close(fig)
    return out


def render_metrics(compared):
    """Render a grouped bar chart of the weighted spatial metrics."""
    metrics = ["connectivity", "integration", "diversity_index", "openness", "circulation_ratio"]
    labels = ["Conn.", "Integ.", "Divers.", "Open.", "Circ."]
    names = [c["name"] for c in compared]
    x = range(len(metrics))
    width = 0.8 / max(len(names), 1)

    fig, ax = plt.subplots(figsize=(9, 5))
    palette = ["#4C72B0", "#DD8452", "#55A868"]
    for idx, c in enumerate(compared):
        m = c["metrics"]
        vals = [m.get(k, 0) for k in metrics]
        ax.bar([i + idx * width for i in x], vals, width, label=c["name"], color=palette[idx % len(palette)])

    ax.set_xticks([i + width * (len(names) - 1) / 2 for i in x])
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Normalized metric (0–1)")
    ax.set_title("Spatial Metrics Comparison Across Schemes", fontsize=13, fontweight="bold")
    ax.legend(fontsize=9)
    ax.grid(axis="y", alpha=0.3)

    out = os.path.join(RESULTS, "metrics_compare.png")
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    plt.close(fig)
    return out


def main():
    analyzer = SpatialAnalyzer()
    sg = SpaceGraph()
    compared = []

    print("=" * 56)
    print("Arch-Spatial-Intelligence — generating real result figures")
    print("=" * 56)

    for name, rooms in SCHEMES.items():
        metrics = analyzer.analyze_floor_plan(rooms)
        sg.build_from_rooms(name, rooms)
        graph_png = render_space_graph(name, rooms)
        print(f"  [graph] {name:18s} -> {os.path.basename(graph_png)}")
        print(metrics.summary())
        print()
        # rebuild compared list with analyzer's own comparison
    compared = analyzer.compare_designs([(n, r) for n, r in SCHEMES.items()])

    metrics_png = render_metrics(compared)
    print(f"  [chart] metrics        -> {os.path.basename(metrics_png)}")

    # ranking
    print("\n  Design ranking (overall spatial score):")
    for c in compared:
        print(f"    {c['name']:18s} {round(c['overall_score'], 3)}")

    # export JSON report (real computed values)
    report = analyzer.export_report(os.path.join(RESULTS, "analysis_report.json"))
    print(f"\n  Report exported -> {report}")

    # write a human-readable summary next to the images
    with open(os.path.join(RESULTS, "README.md"), "w", encoding="utf-8") as f:
        f.write("# Results\n\n")
        f.write("Generated by `examples/generate_results.py` from the real analyzer output.\n\n")
        f.write("## Spatial graphs\n")
        for name in SCHEMES:
            fn = f"space_graph_{name.replace(' ', '_').lower()}.png"
            f.write(f"- ![space graph {name}]({fn}) _{name}_\n")
        f.write("\n## Metrics comparison\n")
        f.write(f"![metrics comparison](metrics_compare.png)\n\n")
        f.write("## Ranking (overall spatial score)\n\n")
        f.write("| Scheme | Overall score |\n|--------|---------------|\n")
        for c in compared:
            f.write(f"| {c['name']} | {round(c['overall_score'], 3)} |\n")
        f.write("\n_All values are computed by `src/spatial_analyzer.py` — no fabricated data._\n")

    print("\nDone. Figures written to results/.")


if __name__ == "__main__":
    main()
