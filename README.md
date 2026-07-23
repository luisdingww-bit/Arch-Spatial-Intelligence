# Arch-Spatial-Intelligence

> **🚩 Flagship project.** A Python toolkit for architectural spatial analysis — space-syntax metrics, graph-based connectivity, and design comparison, with real generated figures.

A Python toolkit for analyzing architectural spatial configurations — connectivity, integration (depth via real shortest-path), circulation efficiency, and functional diversity — then ranking alternative design schemes by a weighted spatial score.

## Results (generated from the real analyzer)

Every figure below is produced by `examples/generate_results.py` from the **actual computed metrics** in `src/spatial_analyzer.py` — no hand-set values.

### Spatial connectivity graphs
Rooms are nodes (size ∝ area, color = function); edges are the declared connections.

| Central Courtyard | Linear Corridor | Campus Library |
|---|---|---|
| ![Central Courtyard](results/space_graph_central_courtyard.png) | ![Linear Corridor](results/space_graph_linear_corridor.png) | ![Campus Library](results/space_graph_campus_library.png) |

### Metrics comparison across schemes
![Spatial metrics comparison](results/metrics_compare.png)

### Ranking (overall spatial score)
| Scheme | Overall score |
|--------|---------------|
| Central Courtyard | 0.847 |
| Linear Corridor | 0.653 |
| Campus Library | 0.628 |

> Scores are computed by `SpatialAnalyzer.compare_designs()` (weights: connectivity 0.3, integration 0.25, diversity 0.25, openness 0.2).

## What's implemented (`src/`)

- **`spatial_analyzer.py`**
  - Connectivity and **integration / depth** via real shortest-path (Floyd–Warshall) over a room-adjacency graph.
  - Diversity metric and `compare_designs()` to rank alternative schemes by a weighted spatial score.
- **`space_graph.py`** — builds adjacency graphs and reports density / diameter / average degree.
- **`report_generator.py`** — emits a Markdown analysis report.
- **`facade_classifier.py`** — heuristic facade-style classifier (see honest note below).
- **`examples/sample_analysis.py`** — runs Scheme A vs Scheme B and prints comparison scores.
- **`examples/generate_results.py`** — renders the figures in the *Results* section above.

## Honest notes

- **Facade classification is heuristic, not CV.** `facade_classifier.py` uses a keyword / symmetry rule — no computer-vision model is trained or loaded.
- **`networkx` is used only by the visualization script** (`examples/generate_results.py`); the core analyzer's graph algorithms are hand-rolled with numpy / scipy.
- `docs/methodology.md` has been rewritten into clean documentation (the previous version was garbled).

## Tech

Python · numpy · scipy · matplotlib · networkx

## Run

```bash
pip install -r requirements.txt

# Text-only analysis
python examples/sample_analysis.py

# Regenerate the figures in results/ (PNGs + JSON report)
python examples/generate_results.py
```

## License

MIT
