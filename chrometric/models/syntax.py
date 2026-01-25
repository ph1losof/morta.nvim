"""
chrometric/models/syntax.py - Weighted Syntax Adjacency Model

Measures distinguishability weighted by adjacency probability in code.
Not all color pairs matter equally - adjacent tokens need to be distinct.
"""

from __future__ import annotations

import math
from typing import Dict, List, Tuple, TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from ..color import Color


class SyntaxContextModel:
    """
    Measures syntax token distinguishability weighted by adjacency probability.

    Uses Oklab distance with sigmoid scoring to evaluate how well
    frequently adjacent tokens can be distinguished from each other.
    """

    # Weights based on how often token types appear adjacent in code
    # Higher weight = more important to distinguish
    ADJACENCY_WEIGHTS: Dict[Tuple[str, str], float] = {
        # High frequency adjacencies
        ("variable", "operator"): 1.0,     # x = y, a + b
        ("function", "variable"): 0.95,    # func(arg)
        ("function", "punctuation"): 0.9,  # func()
        ("type", "variable"): 0.9,         # int x, Type val
        ("keyword", "variable"): 0.85,     # return x, if cond
        ("keyword", "function"): 0.8,      # def func, async func
        ("keyword", "operator"): 0.75,     # if !=, while <
        ("constant", "operator"): 0.7,     # 42 + x, true &&
        ("number", "operator"): 0.7,       # 123 + 456
        ("property", "variable"): 0.65,    # obj.prop
        ("parameter", "type"): 0.6,        # param: Type
        ("string", "operator"): 0.5,       # "str" + x
        ("variable", "punctuation"): 0.5,  # arr[i], obj.key

        # Medium frequency adjacencies
        ("type", "keyword"): 0.45,         # class Name, interface
        ("constant", "variable"): 0.4,     # CONST vs var
        ("string", "variable"): 0.35,      # Less common adjacency
        ("boolean", "operator"): 0.35,     # true && false
        ("namespace", "type"): 0.3,        # Module.Type

        # Lower frequency but important for hierarchy
        ("type", "function"): 0.3,         # Type.method()
        ("keyword", "type"): 0.3,          # new Type, extends Base
        ("comment", "keyword"): 0.2,       # Distinguish from code
    }

    # Minimum Oklab distance for "good" distinguishability
    THRESHOLD_EXCELLENT = 0.18
    THRESHOLD_GOOD = 0.12
    THRESHOLD_ACCEPTABLE = 0.08

    @staticmethod
    def oklab_distance(c1: "Color", c2: "Color") -> float:
        """Compute Euclidean distance in Oklab space."""
        return float(np.linalg.norm(c1.oklab - c2.oklab))

    @classmethod
    def sigmoid_score(cls, distance: float, midpoint: float = 0.12, steepness: float = 25.0) -> float:
        """
        Convert distance to score using sigmoid function.

        Args:
            distance: Oklab distance
            midpoint: Distance at which score is 0.5
            steepness: How sharp the transition is

        Returns:
            Score from 0 to 1
        """
        return 1.0 / (1.0 + math.exp(-steepness * (distance - midpoint)))

    @classmethod
    def calculate_score(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Calculate weighted distinguishability score.

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Dict with syntax adjacency analysis results
        """
        total_score = 0.0
        total_weight = 0.0
        pair_details: Dict[str, Dict] = {}
        issues: List[str] = []

        for (role_a, role_b), weight in cls.ADJACENCY_WEIGHTS.items():
            if role_a not in colors or role_b not in colors:
                continue

            color_a = colors[role_a]
            color_b = colors[role_b]

            dist = cls.oklab_distance(color_a, color_b)
            score = cls.sigmoid_score(dist)

            # Determine quality level
            if dist >= cls.THRESHOLD_EXCELLENT:
                quality = "excellent"
            elif dist >= cls.THRESHOLD_GOOD:
                quality = "good"
            elif dist >= cls.THRESHOLD_ACCEPTABLE:
                quality = "acceptable"
            else:
                quality = "poor"
                issues.append(f"{role_a}-{role_b}: distance {dist:.3f} is too low")

            pair_key = f"{role_a}-{role_b}"
            pair_details[pair_key] = {
                "distance": round(dist, 4),
                "score": round(score, 3),
                "weight": weight,
                "quality": quality,
            }

            total_score += score * weight
            total_weight += weight

        # Compute final weighted score (0-100)
        final_score = (total_score / total_weight) * 100 if total_weight > 0 else 0.0

        # Statistics
        distances = [p["distance"] for p in pair_details.values()]
        min_dist = min(distances) if distances else 0.0
        mean_dist = sum(distances) / len(distances) if distances else 0.0

        return {
            "syntax_score": round(final_score, 2),
            "min_distance": round(min_dist, 4),
            "mean_distance": round(mean_dist, 4),
            "pairs_analyzed": len(pair_details),
            "pairs": pair_details,
            "issues": issues,
            "passed": final_score >= 70.0 and min_dist >= cls.THRESHOLD_ACCEPTABLE,
        }

    @classmethod
    def get_worst_pairs(
        cls,
        colors: Dict[str, "Color"],
        limit: int = 5,
    ) -> List[Tuple[str, str, float]]:
        """
        Get the worst-distinguished token pairs.

        Args:
            colors: Dict mapping token names to Color objects
            limit: Maximum number of pairs to return

        Returns:
            List of (role_a, role_b, distance) tuples, sorted by distance ascending
        """
        pairs = []

        for (role_a, role_b), weight in cls.ADJACENCY_WEIGHTS.items():
            if role_a not in colors or role_b not in colors:
                continue

            dist = cls.oklab_distance(colors[role_a], colors[role_b])
            # Weight-adjusted distance (lower weight = less important)
            pairs.append((role_a, role_b, dist, weight))

        # Sort by distance (ascending) then weight (descending)
        pairs.sort(key=lambda x: (x[2], -x[3]))

        return [(p[0], p[1], p[2]) for p in pairs[:limit]]
