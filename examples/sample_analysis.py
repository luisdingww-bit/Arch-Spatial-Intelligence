"""
Arch-Spatial-Intelligence - Sample Analysis
Compare two architectural design proposals using spatial analysis.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.spatial_analyzer import SpatialAnalyzer
from src.space_graph import SpaceGraph
from src.report_generator import ReportGenerator

analyzer = SpatialAnalyzer()

# Two design proposals
scheme_a = [
    {"name": "Courtyard", "area": 200, "type": "public", "connections": [1, 2]},
    {"name": "Lecture Hall", "area": 180, "type": "public", "connections": [0, 2]},
    {"name": "Corridor", "area": 60, "type": "circulation", "connections": [0, 1]},
]

scheme_b = [
    {"name": "Entrance", "area": 80, "type": "public", "connections": [1]},
    {"name": "Main Corridor", "area": 120, "type": "circulation", "connections": [0, 2]},
    {"name": "Exhibition", "area": 200, "type": "public", "connections": [1]},
]

print("=" * 50)
print("Arch-Spatial-Intelligence - Sample Analysis")
print("=" * 50)

for name, rooms in [('Scheme A - Central Courtyard', scheme_a), ('Scheme B - Linear Layout', scheme_b)]:
    m = analyzer.analyze_floor_plan(rooms)
    print()
    print(name)
    print(f"  Total Area: {m.total_area} m2")
    print(f"  Connectivity: {m.connectivity}")
    print(f"  Integration: {m.integration}")
    print(f"  Diversity: {m.diversity_index}")

print()
print("--- Design Comparison ---")
comparison = analyzer.compare_designs([('Scheme A', scheme_a), ('Scheme B', scheme_b)])
for c in comparison:
    print(f"  {c[chr(39)+chr(39)+chr(39)]}")

print("Done!")