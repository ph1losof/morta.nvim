"""
chrometric/models/perceptual.py - Perceptual Distance Metrics

Oklab and CAM16-UCS based perceptual distance measurements
for evaluating color separation and distinguishability.
"""

from __future__ import annotations

from typing import Dict, List, TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from ..color import Color


class PerceptualModel:
    """Perceptual distance metrics using Oklab and CAM16-UCS color spaces."""

    # Syntax tokens for analysis
    SYNTAX_TOKENS = ["keyword", "string", "function", "type", "variable", "comment"]

    # Thresholds
    OKLAB_THRESHOLD_MEAN = 0.15
    OKLAB_THRESHOLD_MIN = 0.08
    CAM16_THRESHOLD_MEAN = 0.06
    CAM16_THRESHOLD_MIN = 0.03

    @classmethod
    def oklab_separation(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Analyze pairwise Oklab distances between syntax tokens.

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Dict with Oklab separation analysis
        """
        present = [t for t in cls.SYNTAX_TOKENS if t in colors]

        if len(present) < 2:
            return {
                "mean_delta_e": 0.0,
                "min_delta_e": 0.0,
                "max_delta_e": 0.0,
                "passed": False,
            }

        vecs = [colors[t].oklab for t in present]
        dists: List[float] = []
        pair_distances: Dict[str, float] = {}

        for i in range(len(vecs)):
            for j in range(i + 1, len(vecs)):
                dist = float(np.linalg.norm(vecs[i] - vecs[j]))
                dists.append(dist)
                pair_key = f"{present[i]}-{present[j]}"
                pair_distances[pair_key] = round(dist, 4)

        mean_de = float(np.mean(dists))
        min_de = float(np.min(dists))
        max_de = float(np.max(dists))

        # Find worst pair
        worst_pair = min(pair_distances.items(), key=lambda x: x[1])

        return {
            "mean_delta_e": round(mean_de, 4),
            "min_delta_e": round(min_de, 4),
            "max_delta_e": round(max_de, 4),
            "worst_pair": worst_pair[0],
            "worst_distance": worst_pair[1],
            "pair_distances": pair_distances,
            "passed": mean_de >= cls.OKLAB_THRESHOLD_MEAN and min_de >= cls.OKLAB_THRESHOLD_MIN,
        }

    @classmethod
    def cam16_ucs_separation(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Analyze pairwise CAM16-UCS distances between syntax tokens.

        CAM16-UCS is appearance-based and accounts for viewing conditions.

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Dict with CAM16-UCS separation analysis
        """
        present = [t for t in cls.SYNTAX_TOKENS if t in colors]

        if len(present) < 2:
            return {
                "mean_delta_e_cam16": 0.0,
                "min_delta_e_cam16": 0.0,
                "max_delta_e_cam16": 0.0,
                "passed": False,
            }

        vecs = [colors[t].cam16ucs for t in present]
        dists: List[float] = []
        pair_distances: Dict[str, float] = {}

        for i in range(len(vecs)):
            for j in range(i + 1, len(vecs)):
                dist = float(np.linalg.norm(vecs[i] - vecs[j]))
                dists.append(dist)
                pair_key = f"{present[i]}-{present[j]}"
                pair_distances[pair_key] = round(dist, 4)

        mean_de = float(np.mean(dists))
        min_de = float(np.min(dists))
        max_de = float(np.max(dists))

        worst_pair = min(pair_distances.items(), key=lambda x: x[1])

        return {
            "mean_delta_e_cam16": round(mean_de, 4),
            "min_delta_e_cam16": round(min_de, 4),
            "max_delta_e_cam16": round(max_de, 4),
            "worst_pair": worst_pair[0],
            "worst_distance": worst_pair[1],
            "pair_distances": pair_distances,
            "passed": mean_de >= cls.CAM16_THRESHOLD_MEAN and min_de >= cls.CAM16_THRESHOLD_MIN,
        }

    @classmethod
    def wcag_contrast(cls, fg: "Color", bg: "Color") -> Dict:
        """
        Calculate WCAG 2.0 contrast ratio (for reference/legacy comparison).

        Note: APCA is preferred for actual readability assessment.

        Args:
            fg: Foreground color
            bg: Background color

        Returns:
            Dict with WCAG contrast analysis
        """
        L1 = fg.Y + 0.05
        L2 = bg.Y + 0.05

        if L2 <= 0:
            return {"ratio": 0.0, "passed_aa": False, "passed_aaa": False}

        ratio = max(L1, L2) / min(L1, L2)

        return {
            "ratio": round(ratio, 2),
            "passed_aa": ratio >= 4.5,
            "passed_aa_large": ratio >= 3.0,
            "passed_aaa": ratio >= 7.0,
        }

    @classmethod
    def analyze(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Run all perceptual analyses.

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Combined perceptual analysis results
        """
        oklab = cls.oklab_separation(colors)
        cam16 = cls.cam16_ucs_separation(colors)

        # WCAG for reference
        fg = colors.get("fg")
        bg = colors.get("bg")
        wcag = cls.wcag_contrast(fg, bg) if fg and bg else {}

        # Combined score
        oklab_score = min(oklab["mean_delta_e"] / cls.OKLAB_THRESHOLD_MEAN * 100, 100)
        cam16_score = min(cam16["mean_delta_e_cam16"] / cls.CAM16_THRESHOLD_MEAN * 100, 100)

        return {
            "oklab": oklab,
            "cam16_ucs": cam16,
            "wcag": wcag,
            "perceptual_score": round((oklab_score * 0.6 + cam16_score * 0.4), 2),
            "passed": oklab["passed"] and cam16["passed"],
        }
