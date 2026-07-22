"""Arch-Spatial-Intelligence - Facade Classifier"""
import json
from pathlib import Path

STYLES = {
    "modern": {"keywords": ["glass", "steel", "minimal"], "era": "1920s-present"},
    "traditional_chinese": {"keywords": ["curved roof", "wood", "courtyard"], "era": "ancient-1911"},
    "parametric": {"keywords": ["algorithmic", "complex", "organic"], "era": "2000s-present"},
}

class FacadeClassifier:
    def classify_by_features(self, features):
        scores = []
        for name, info in STYLES.items():
            score = 0.5
            if features.get("symmetry", 0) > 0.7: score += 0.15
            if features.get("complexity", 0) > 0.6: score += 0.1
            scores.append({"style": name, "confidence": round(min(score, 1.0), 3)})
        return sorted(scores, key=lambda x: x["confidence"], reverse=True)

if __name__ == "__main__":
    c = FacadeClassifier()
    r = c.classify_by_features({"symmetry": 0.8, "complexity": 0.5})
    for x in r: print(f"  {x['style']:20s} {x['confidence']:.3f}")
