# Methodology — Arch-Spatial-Intelligence

## 1. Input
A room program: a set of spaces, each with a centroid and an adjacency relation (shared wall / direct access).

## 2. Graph construction
Each room becomes a node; adjacencies are undirected edges. Edge weight defaults to 1 (topological depth).

## 3. Spatial metrics
- **Connectivity** — degree of each node.
- **Integration / Depth** — all-pairs shortest path (Floyd–Warshall); mean depth per node, lower = more integrated.
- **Diversity** — entropy of the local connectivity distribution.

## 4. Design comparison
Alternative schemes are scored by a weighted sum of the metrics above and ranked via `compare_designs()`.

## 5. Output
A Markdown report (`report_generator.py`) summarizing per-scheme metrics and the ranked comparison.
