\"\"\"
Arch-Spatial-Intelligence — Sample Analysis
=============================================
Demonstrates a complete spatial intelligence analysis workflow.
\"\"\"

import sys
sys.path.insert(0, \"..\")

from src.spatial_analyzer import SpatialAnalyzer
from src.space_graph import SpaceGraph, GraphMetrics
from src.report_generator import ReportGenerator
import json


def main():
    print(\"=\" * 50)
    print(\"Arch-Spatial-Intelligence — Sample Analysis\")
    print(\"=\" * 50)

    # 1. Define two design proposals for comparison
    proposals = [
        (\"Scheme A - Central Courtyard\", [
            {\"name\": \"Courtyard\", \"area\": 200, \"type\": \"public\",
             \"connections\": [1, 2, 3]},
            {\"name\": \"Lecture Hall\", \"area\": 180, \"type\": \"public\",
             \"connections\": [0, 3]},
            {\"name\": \"Library\", \"area\": 250, \"type\": \"public\",
             \"connections\": [0, 3]},
            {\"name\": \"Corridor\", \"area\": 60, \"type\": \"circulation\",
             \"connections\": [0, 1, 2]},
            {\"name\": \"Office\", \"area\": 40, \"type\": \"private\",
             \"connections\": [3]},
        ]),
        (\"Scheme B - Linear Layout\", [
            {\"name\": \"Entrance\", \"area\": 80, \"type\": \"public\",
             \"connections\": [1]},
            {\"name\": \"Main Corridor\", \"area\": 120, \"type\": \"circulation\",
             \"connections\": [0, 2, 3, 4]},
            {\"name\": \"Exhibition\", \"area\": 200, \"type\": \"public\",
             \"connections\": [1]},
            {\"name\": \"Workshop\", \"area\": 160, \"type\": \"public\",
             \"connections\": [1]},
            {\"name\": \"Storage\", \"area\": 50, \"type\": \"private\",
             \"connections\": [1]},
        ]),
    ]

    # 2. Spatial Analysis
    print(\"\\n[1/3] Spatial Analysis...\")
    analyzer = SpatialAnalyzer()
    for name, rooms in proposals:
        metrics = analyzer.analyze_floor_plan(rooms)
        print(f\"  {name}:\")
        print(f\"    Connectivity: {metrics.connectivity}\")
        print(f\"    Integration:  {metrics.integration}\")
        print(f\"    Diversity:    {metrics.diversity_index}\")

    # 3. Space Graph
    print(\"\\n[2/3] Space Graph Analysis...\")
    sg = SpaceGraph()
    for name, rooms in proposals:
        graph = sg.build_from_rooms(name, rooms)
        m = graph[\"metrics\"]
        print(f\"  {name}: {m['node_count']} spaces, {m['edge_count']} connections\")

    # 4. Compare and Report
    print(\"\\n[3/3] Design Comparison...\")
    comparison = analyzer.compare_designs(proposals)
    for c in comparison:
        print(f\"  {c['name']}: {c['overall_score']:.3f}\")

    # 5. Generate Report
    print(\"\\nReport:\")
    report = ReportGenerator(\"Campus Design Competition — Spatial Analysis\")
    report.add_spatial_analysis(comparison[0][\"metrics\"])
    report_path = report.save(\"../docs/sample_report.md\")
    print(f\"\\nDone! Report saved to: {report_path}\")


if __name__ == \"__main__\":
    main()
