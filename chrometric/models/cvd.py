"""
chrometric/models/cvd.py - Color Vision Deficiency Model

CLDM (Color-blind Legibility Distance Metric)
Simulates Protan, Deutan, Tritan deficiencies using LMS cone projection.
"""

from __future__ import annotations

from typing import Dict, List, Tuple, TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from ..color import Color


class CVDModel:
    """Color Vision Deficiency (CVD) safety analysis."""

    DEFICIENCIES = ["protan", "deutan", "tritan"]

    # Critical token pairs that must remain distinguishable under CVD
    CRITICAL_PAIRS = [
        ("keyword", "string"),
        ("type", "string"),
        ("type", "comment"),
        ("keyword", "comment"),
        ("variable", "function"),
        ("error", "warning"),
        ("function", "type"),
        ("constant", "string"),
    ]

    # Minimum LMS distance threshold for safety
    THRESHOLD_MIN = 0.15
    THRESHOLD_COMFORTABLE = 0.25

    @staticmethod
    def simulate_deficiency(lms: np.ndarray, deficiency: str) -> np.ndarray:
        """
        Simulate color vision deficiency using zero-cone projection.

        Args:
            lms: LMS cone response values
            deficiency: Type of deficiency ('protan', 'deutan', 'tritan')

        Returns:
            Simulated LMS values
        """
        if deficiency == "protan":
            # L-cone deficiency (red-blind)
            return np.array([0.0, lms[1], lms[2]])
        elif deficiency == "deutan":
            # M-cone deficiency (green-blind)
            return np.array([lms[0], 0.0, lms[2]])
        elif deficiency == "tritan":
            # S-cone deficiency (blue-blind)
            return np.array([lms[0], lms[1], 0.0])
        return lms

    @classmethod
    def analyze_pair(
        cls,
        color1: "Color",
        color2: "Color",
    ) -> Dict[str, float]:
        """
        Analyze a color pair under all deficiency types.

        Args:
            color1: First color
            color2: Second color

        Returns:
            Dict mapping deficiency type to LMS distance
        """
        results = {}
        lms1 = color1.lms
        lms2 = color2.lms

        for deficiency in cls.DEFICIENCIES:
            sim1 = cls.simulate_deficiency(lms1, deficiency)
            sim2 = cls.simulate_deficiency(lms2, deficiency)
            dist = float(np.linalg.norm(sim1 - sim2))
            results[deficiency] = round(dist, 4)

        return results

    @classmethod
    def analyze(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Test critical pairs under each deficiency type.

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Dict with CVD safety analysis
        """
        available_pairs = [
            (a, b) for a, b in cls.CRITICAL_PAIRS
            if a in colors and b in colors
        ]

        if not available_pairs:
            return {
                "min_cldm": 0.0,
                "passed": False,
                "deficiency_breakdown": {},
                "pair_analysis": {},
            }

        # Collect distances by deficiency type
        dists_by_type: Dict[str, List[float]] = {d: [] for d in cls.DEFICIENCIES}
        pair_analysis: Dict[str, Dict] = {}

        for a, b in available_pairs:
            pair_key = f"{a}-{b}"
            pair_dists = cls.analyze_pair(colors[a], colors[b])
            pair_analysis[pair_key] = pair_dists

            for deficiency, dist in pair_dists.items():
                dists_by_type[deficiency].append(dist)

        # Compute statistics per deficiency
        deficiency_breakdown: Dict[str, Dict] = {}
        all_mins: List[float] = []

        for deficiency, dists in dists_by_type.items():
            if not dists:
                continue

            min_dist = min(dists)
            mean_dist = sum(dists) / len(dists)
            all_mins.append(min_dist)

            deficiency_breakdown[deficiency] = {
                "min": round(min_dist, 4),
                "mean": round(mean_dist, 4),
                "passed": min_dist >= cls.THRESHOLD_MIN,
            }

        # Find worst-performing pairs
        worst_pairs: List[Tuple[str, str, float]] = []
        for pair_key, dists in pair_analysis.items():
            min_dist = min(dists.values())
            worst_deficiency = min(dists, key=dists.get)
            worst_pairs.append((pair_key, worst_deficiency, min_dist))

        worst_pairs.sort(key=lambda x: x[2])

        # Overall metrics
        global_min = min(all_mins) if all_mins else 0.0
        passed = all(d["passed"] for d in deficiency_breakdown.values())

        # CVD safety score (0-100)
        safety_score = min((global_min / cls.THRESHOLD_COMFORTABLE) * 100, 100)

        return {
            "min_cldm": round(global_min, 4),
            "cvd_score": round(safety_score, 2),
            "deficiency_breakdown": deficiency_breakdown,
            "pair_analysis": pair_analysis,
            "worst_pairs": worst_pairs[:5],
            "passed": passed,
        }

    @classmethod
    def get_recommendations(cls, analysis: Dict) -> List[str]:
        """
        Generate recommendations based on CVD analysis.

        Args:
            analysis: Results from analyze()

        Returns:
            List of recommendation strings
        """
        recommendations = []

        if not analysis["passed"]:
            for deficiency, data in analysis["deficiency_breakdown"].items():
                if not data["passed"]:
                    recommendations.append(
                        f"Improve {deficiency} safety: minimum distance is {data['min']:.3f}, "
                        f"needs >= {cls.THRESHOLD_MIN}"
                    )

            # Specific pair recommendations
            for pair, deficiency, dist in analysis.get("worst_pairs", [])[:3]:
                if dist < cls.THRESHOLD_MIN:
                    recommendations.append(
                        f"Pair '{pair}' is hard to distinguish under {deficiency} "
                        f"(distance: {dist:.3f})"
                    )

        return recommendations
