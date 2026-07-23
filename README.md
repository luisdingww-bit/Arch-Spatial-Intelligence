# Arch-Spatial-Intelligence

A Python toolkit for architectural spatial analysis — space-syntax metrics, graph-based connectivity, and design comparison.

> **Status: functional core.** Runnable end-to-end on the included example.

## What's implemented (`src/`)

- **`spatial_analyzer.py`**
  - Connectivity and **integration / depth** via real shortest-path (Floyd–Warshall) over a room-adjacency graph.
  - Diversity metric and `compare_designs()` to rank alternative schemes by a weighted spatial score.
- **`space_graph.py`** — builds adjacency graphs and reports density / diameter / average degree.
- **`report_generator.py`** — emits a Markdown analysis report.
- **`examples/sample_analysis.py`** — runs Scheme A vs Scheme B and prints comparison scores.

## Honest notes

- **Facade classification is heuristic, not CV.** `facade_classifier.py` uses a keyword / symmetry rule — no computer-vision model is trained or loaded.
- **`networkx` is listed but not actually imported**; graph algorithms are hand-rolled with numpy / scipy.
- `docs/methodology.md` has been rewritten into clean documentation (the previous version was garbled).

## Tech

Python · numpy · scipy · matplotlib

## Run

```bash
pip install -r requirements.txt
python examples/sample_analysis.py
```

## License

MIT
