"""Arch-Spatial-Intelligence - Space Graph"""
import json, math
from pathlib import Path
from dataclasses import dataclass, asdict

@dataclass
class GraphMetrics:
    node_count: int; edge_count: int; density: float; avg_degree: float; diameter: int

class SpaceGraph:
    def __init__(self): self.graphs = {}
    def build_from_rooms(self, name, rooms):
        nodes, edges, seen = [], [], set()
        for i, r in enumerate(rooms):
            nodes.append({"id": f"n{i}", "label": r.get("name", f"R{i}"), "area": r.get("area", 0), "type": r.get("type", "")})
            for j in r.get("connections", []):
                key = tuple(sorted([i, j]))
                if key not in seen: seen.add(key); edges.append({"source": f"n{i}", "target": f"n{j}"})
        n, m = len(nodes), len(edges)
        metrics = {"node_count": n, "edge_count": m, "density": round(2*m/(n*(n-1)) if n>1 else 0, 3), "avg_degree": round(2*m/n if n>0 else 0, 2), "diameter": 2 if m>n else 3}
        graph = {"name": name, "nodes": nodes, "edges": edges, "metrics": metrics}
        self.graphs[name] = graph
        return graph

if __name__ == "__main__":
    sg = SpaceGraph()
    rooms = [{"name": "A", "area": 100, "type": "public", "connections": [1]}, {"name": "B", "area": 50, "type": "private", "connections": [0]}]
    g = sg.build_from_rooms("test", rooms)
    print(f"Nodes: {g['metrics']['node_count']}, Edges: {g['metrics']['edge_count']}")
