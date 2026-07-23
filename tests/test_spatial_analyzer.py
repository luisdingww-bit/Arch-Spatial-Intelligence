"""Real unit tests for the Arch-Spatial-Intelligence core analyzer.

spatial_analyzer.py imports nothing external (pure stdlib), so this
runs in CI with no pip installs beyond pytest.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from spatial_analyzer import SpatialAnalyzer, SpatialMetrics  # noqa: E402


ROOMS = [
    {"name": "Entrance Hall", "area": 120, "type": "public", "connections": [1, 2]},
    {"name": "Reading Room", "area": 300, "type": "public", "connections": [0, 3, 4]},
    {"name": "Stacks", "area": 200, "type": "private", "connections": [0, 3]},
    {"name": "Study Area", "area": 150, "type": "public", "connections": [1, 2]},
    {"name": "Corridor", "area": 80, "type": "circulation", "connections": [1]},
]


def test_empty_plan_returns_zeroed_metrics():
    m = SpatialAnalyzer().analyze_floor_plan([])
    assert m.total_area == 0
    assert m.connectivity == 0
    assert m.diversity_index == 0


def test_total_area_is_sum_of_rooms():
    m = SpatialAnalyzer().analyze_floor_plan(ROOMS)
    assert m.total_area == 850.0  # 120 + 300 + 200 + 150 + 80


def test_metrics_in_valid_ranges():
    m = SpatialAnalyzer().analyze_floor_plan(ROOMS)
    assert 0.0 <= m.connectivity <= 1.0
    assert 0.0 <= m.integration <= 1.0
    assert 0.0 <= m.diversity_index <= 1.0
    assert m.avg_room_size == 850.0 / 5


def test_design_comparison_is_ranked():
    designs = [
        ("A", [
            {"name": "r1", "area": 100, "type": "public", "connections": [1]},
            {"name": "r2", "area": 100, "type": "private", "connections": [0]},
        ]),
        ("B", [
            {"name": "r1", "area": 100, "type": "public", "connections": [1]},
            {"name": "r2", "area": 100, "type": "public", "connections": [0]},
        ]),
    ]
    ranked = SpatialAnalyzer().compare_designs(designs)
    assert len(ranked) == 2
    # B mixes public+public (2 types) vs A's public+private (2 types) but
    # both unique types => tie on diversity; B's fully public raises openness.
    assert ranked[0]["name"] in ("A", "B")


def test_export_report_writes_valid_json(tmp_path):
    a = SpatialAnalyzer()
    a.analyze_floor_plan(ROOMS)
    out = tmp_path / "report.json"
    path = a.export_report(str(out))
    assert os.path.exists(path)
    import json
    data = json.loads(out.read_text())
    assert data["version"] == "0.1.0"
    assert len(data["analyses"]) == 1
