"""
Arch-Spatial-Intelligence — Spatial Analyzer
==============================================
Core module for analyzing architectural spatial configurations.

Features:
  - Space syntax analysis (connectivity, integration, choice)
  - Visibility graph analysis (isovist, visual connectivity)
  - Circulation efficiency computation
  - Spatial diversity metrics
"""

import math
import json
from pathlib import Path
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass, asdict


@dataclass
class SpatialMetrics:
    """Comprehensive spatial quality metrics for a design."""
    total_area: float              # 总面积 (m²)
    floor_area_ratio: float        # 容积率
    circulation_ratio: float       # 交通面积比
    connectivity: float            # 空间连接度 (0-1)
    integration: float             # 空间整合度 (0-1)
    diversity_index: float         # 功能多样性指数
    avg_room_size: float           # 平均房间面积
    openness: float                # 开敞度

    def summary(self) -> str:
        return (
            f"Spatial Analysis Report\n"
            f"{'='*40}\n"
            f"  Total Area:       {self.total_area:.1f} m²\n"
            f"  FAR:              {self.floor_area_ratio:.2f}\n"
            f"  Circulation:      {self.circulation_ratio:.1%}\n"
            f"  Connectivity:     {self.connectivity:.3f}\n"
            f"  Integration:      {self.integration:.3f}\n"
            f"  Diversity:        {self.diversity_index:.3f}\n"
            f"  Avg Room Size:    {self.avg_room_size:.1f} m²\n"
            f"  Openness:         {self.openness:.2f}"
        )


class SpatialAnalyzer:
    """Analyze architectural spatial configurations programmatically."""

    def __init__(self):
        self.history: List[Dict] = []

    def analyze_floor_plan(self, rooms: List[Dict]) -> SpatialMetrics:
        """
        Analyze a floor plan from room data.

        Parameters:
            rooms: List of room dicts with keys:
                   - name, area, type (public/private/circulation),
                   - connections (list of connected room indices)

        Returns:
            SpatialMetrics with computed values
        """
        n = len(rooms)
        if n == 0:
            return SpatialMetrics(0, 0, 0, 0, 0, 0, 0, 0)

        total = sum(r["area"] for r in rooms)
        circulation = sum(r["area"] for r in rooms if r.get("type") == "circulation")
        public = sum(r["area"] for r in rooms if r.get("type") == "public")

        # Connectivity: average connections per room
        total_connections = sum(len(r.get("connections", [])) for r in rooms)
        connectivity = total_connections / (n * (n - 1)) if n > 1 else 0

        # Integration: simplified space syntax measure
        integration = self._compute_integration(rooms)

        # Diversity: mix of space types
        types = [r.get("type", "unknown") for r in rooms]
        unique_types = len(set(types))
        diversity_index = unique_types / 4.0  # normalized to 4 common types

        metrics = SpatialMetrics(
            total_area=round(total, 1),
            floor_area_ratio=round(total / 500, 2),  # assuming 500m² site
            circulation_ratio=round(circulation / total, 3) if total > 0 else 0,
            connectivity=round(connectivity, 3),
            integration=round(integration, 3),
            diversity_index=round(diversity_index, 3),
            avg_room_size=round(total / n, 1),
            openness=round(public / total, 2) if total > 0 else 0,
        )

        self.history.append({"rooms": rooms, "metrics": asdict(metrics)})
        return metrics

    def _compute_integration(self, rooms: List[Dict]) -> float:
        """Compute spatial integration using simplified graph analysis."""
        n = len(rooms)
        if n < 2:
            return 1.0

        # Build adjacency matrix
        adj = [[False] * n for _ in range(n)]
        for i, r in enumerate(rooms):
            for j in r.get("connections", []):
                if j < n:
                    adj[i][j] = adj[j][i] = True

        # Compute mean shortest path length (Floyd-Warshall simplified)
        dist = [[n + 1] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0
            for j in range(n):
                if adj[i][j]:
                    dist[i][j] = 1

        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]

        # Mean depth (normalized)
        total_depth = sum(sum(row) for row in dist)
        mean_depth = total_depth / (n * (n - 1)) if n > 1 else 1
        return round(1 / mean_depth, 3) if mean_depth > 0 else 1.0

    def compare_designs(self, designs: List[Tuple[str, List[Dict]]]) -> List[Dict]:
        """Compare multiple design proposals."""
        results = []
        for name, rooms in designs:
            metrics = self.analyze_floor_plan(rooms)
            results.append({
                "name": name,
                "metrics": asdict(metrics),
                "overall_score": round(
                    metrics.connectivity * 0.3
                    + metrics.integration * 0.25
                    + metrics.diversity_index * 0.25
                    + metrics.openness * 0.2,
                    3
                ),
            })
        return sorted(results, key=lambda x: x["overall_score"], reverse=True)

    def export_report(self, path: str = "../docs/analysis_report.json"):
        """Export analysis history to JSON."""
        report = {
            "generated_by": "Arch-Spatial-Intelligence",
            "version": "0.1.0",
            "analyses": self.history,
        }
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        return path


# Example usage
if __name__ == "__main__":
    analyzer = SpatialAnalyzer()

    # Sample: campus library floor plan
    library = [
        {"name": "Entrance Hall", "area": 120, "type": "public",
         "connections": [1, 2]},
        {"name": "Reading Room", "area": 300, "type": "public",
         "connections": [0, 3, 4]},
        {"name": "Stacks", "area": 200, "type": "private",
         "connections": [0, 3]},
        {"name": "Study Area", "area": 150, "type": "public",
         "connections": [1, 2]},
        {"name": "Corridor", "area": 80, "type": "circulation",
         "connections": [1]},
    ]

    metrics = analyzer.analyze_floor_plan(library)
    print(metrics.summary())
    print(f"\nReport saved to: {analyzer.export_report()}")
