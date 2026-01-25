"""
chrometric/models/harmony.py - Palette Harmony and HKSM

Moon-Spencer harmony, opponent balance, hue entropy.
HKSM (Helmholtz-Kohlrausch Stability Metric).
"""

from __future__ import annotations

import math
from typing import Dict, List, TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from ..color import Color


class HarmonyModel:
    """Palette harmony and perceptual brightness stability metrics."""

    SYNTAX_TOKENS = ["keyword", "string", "function", "type", "variable", "comment"]

    # HKSM thresholds
    HKSM_COMFORTABLE = 15.0
    HKSM_ACCEPTABLE = 20.0
    HKSM_PAINFUL = 25.0

    @classmethod
    def analyze_harmony(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Analyze palette harmony using multiple metrics.

        - Moon-Spencer: Angular distribution quality in hue space
        - Opponent balance: a/b channel centering in Oklab
        - Entropy: Hue distribution evenness

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Dict with harmony analysis
        """
        present = [t for t in cls.SYNTAX_TOKENS if t in colors]

        if len(present) < 2:
            return {
                "moon_spencer": 0.0,
                "opponent_balance": 0.0,
                "entropy": 0.0,
                "harmony": 0.0,
                "passed": False,
            }

        # Collect Oklab values
        angles: List[float] = []
        a_vals: List[float] = []
        b_vals: List[float] = []

        for t in present:
            oklab = colors[t].oklab
            a_vals.append(oklab[1])
            b_vals.append(oklab[2])
            h = math.atan2(oklab[2], oklab[1])
            angles.append(h)

        # Moon-Spencer: Mean angular distance (normalized)
        ang_dists = []
        for i in range(len(angles)):
            for j in range(i + 1, len(angles)):
                diff = abs(angles[i] - angles[j])
                if diff > math.pi:
                    diff = 2 * math.pi - diff
                ang_dists.append(diff)

        mean_ang = float(np.mean(ang_dists)) if ang_dists else 0.0
        moon_spencer = mean_ang / math.pi  # 0-1 scale

        # Opponent balance: How centered is the palette in a/b space
        a_mean = np.mean(a_vals)
        b_mean = np.mean(b_vals)
        a_abs_mean = np.mean(np.abs(a_vals))
        b_abs_mean = np.mean(np.abs(b_vals))

        opponent_balance = 1.0 - (abs(a_mean) + abs(b_mean)) / (
            a_abs_mean + b_abs_mean + 1e-12
        )

        # Hue entropy: Distribution evenness
        bins = 12
        hist = [0] * bins
        for ang in angles:
            idx = int(((ang + math.pi) / (2 * math.pi)) * bins) % bins
            hist[idx] += 1

        total = sum(hist)
        probs = [h / total for h in hist] if total > 0 else [0] * bins
        entropy = -sum(p * math.log2(p) for p in probs if p > 0)
        entropy_norm = entropy / (math.log2(bins) + 1e-12)

        # Combined harmony score
        # Higher moon_spencer = more spread out hues (good)
        # Higher opponent_balance = more centered (good)
        # Lower entropy_norm = more clustered (can be intentional)
        harmony = 0.5 * moon_spencer + 0.3 * opponent_balance + 0.2 * (1 - entropy_norm)

        return {
            "moon_spencer": round(moon_spencer, 4),
            "opponent_balance": round(opponent_balance, 4),
            "entropy": round(entropy_norm, 4),
            "harmony": round(harmony, 4),
            "hue_angles": {t: round(angles[i], 4) for i, t in enumerate(present)},
            "passed": harmony > 0.45,
        }

    @classmethod
    def hksm(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Calculate HKSM (Helmholtz-Kohlrausch Stability Metric).

        Q_HK = Q - J (brightness - lightness)
        HKSM = Q_HK / Y (normalized by luminance)

        Lower is better (< 15 comfortable, < 20 acceptable, > 25 painful).

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Dict with HKSM analysis
        """
        present = [t for t in cls.SYNTAX_TOKENS if t in colors]

        if not present:
            return {
                "HKSM_mean": 0.0,
                "HKSM_max": 0.0,
                "breakdown": {},
                "passed": False,
            }

        breakdown: Dict[str, Dict] = {}
        hksm_vals: List[float] = []

        for t in present:
            col = colors[t]
            J = float(col.cam16_J)
            Q = float(col.cam16_Q)
            Q_hk = Q - J
            Y = float(col.Y) if col.Y > 0 else 1e-6

            hksm = Q_hk / Y

            breakdown[t] = {
                "J": round(J, 3),
                "Q": round(Q, 3),
                "Q_HK": round(Q_hk, 3),
                "Y": round(Y, 6),
                "HKSM": round(hksm, 3),
            }
            hksm_vals.append(hksm)

        mean_hksm = float(np.mean(hksm_vals))
        max_hksm = float(np.max(hksm_vals))

        # Determine comfort level
        if mean_hksm < cls.HKSM_COMFORTABLE:
            rating = "comfortable"
        elif mean_hksm < cls.HKSM_ACCEPTABLE:
            rating = "acceptable"
        elif mean_hksm < cls.HKSM_PAINFUL:
            rating = "elevated"
        else:
            rating = "painful"

        return {
            "HKSM_mean": round(mean_hksm, 3),
            "HKSM_max": round(max_hksm, 3),
            "breakdown": breakdown,
            "rating": rating,
            "passed": mean_hksm < cls.HKSM_ACCEPTABLE,
        }

    @classmethod
    def analyze(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Run all harmony analyses.

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Combined harmony analysis results
        """
        harmony = cls.analyze_harmony(colors)
        hksm = cls.hksm(colors)

        # Combined score
        harmony_score = harmony["harmony"] * 100
        hksm_score = max(0, 100 - (hksm["HKSM_mean"] - 10) * 5)

        return {
            "harmony": harmony,
            "hksm": hksm,
            "combined_score": round(harmony_score * 0.6 + hksm_score * 0.4, 2),
            "passed": harmony["passed"] and hksm["passed"],
        }
