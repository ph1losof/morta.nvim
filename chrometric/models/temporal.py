"""
chrometric/models/temporal.py - Temporal Metrics

JND (Just Noticeable Difference) alignment for background layers.
TAFD (Temporal Anti-Flicker Distance) for UI transitions.
Drift Index for chroma stability over time.
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from ..color import Color


class TemporalModel:
    """Temporal perception metrics for UI stability."""

    # JND formula constants (whitepaper)
    JND_ALPHA = 5.0
    JND_BETA = 0.4

    # TAFD flicker constant
    TAFD_K = 0.01

    # Drift decay constant
    DRIFT_K = 0.01

    @staticmethod
    def _y_from_color(color: "Color") -> float:
        """Extract luminance from Color object."""
        return float(color.Y)

    @classmethod
    def synthesize_bg_layers(cls, base: "Color", factors: List[float] = None) -> List[float]:
        """
        Create synthetic background luminances by scaling linear RGB.

        Args:
            base: Base background color
            factors: Scaling factors (default: [0.70, 0.88, 1.0, 1.12])

        Returns:
            List of luminance values
        """
        if factors is None:
            factors = [0.70, 0.88, 1.0, 1.12]

        M = np.array([
            [0.4124564, 0.3575761, 0.1804375],
            [0.2126729, 0.7151522, 0.0721750],
            [0.0193339, 0.1191920, 0.9503041],
        ])

        Ys = []
        for f in factors:
            rgb_lin = np.clip(base.rgb_linear * f, 0.0, 1.0)
            xyz = M @ rgb_lin
            Ys.append(float(xyz[1]))

        return Ys

    @classmethod
    def mesopic_jnd(
        cls,
        colors: Dict[str, "Color"],
        ui_layers: List[str] = None,
    ) -> Dict:
        """
        Calculate Mesopic JND alignment for background layers.

        Whitepaper formula: delta_L_th(L) = alpha * L + beta * sqrt(L)

        Args:
            colors: Dict mapping token names to Color objects
            ui_layers: Token names for UI background layers

        Returns:
            Dict with JND alignment analysis
        """
        if ui_layers is None:
            ui_layers = [
                "bg", "cursor_line", "popup_bg", "visual",
                "status_line", "fold", "sign_column"
            ]

        # Extract luminances from available layers
        Ys = []
        for layer in ui_layers:
            if layer in colors:
                Ys.append(cls._y_from_color(colors[layer]))

        # If not enough layers, synthesize from bg
        if len(Ys) < 2 and "bg" in colors:
            Ys = cls.synthesize_bg_layers(colors["bg"])

        Ys = sorted(set(Ys))

        if len(Ys) < 2:
            return {
                "jnd_alignment": 0.0,
                "layers_analyzed": 0,
                "passed": False,
            }

        # Calculate JND thresholds and margins
        deltas = [abs(Ys[i + 1] - Ys[i]) for i in range(len(Ys) - 1)]
        thresholds = [
            cls.JND_ALPHA * Ys[i] + cls.JND_BETA * math.sqrt(max(Ys[i], 0.0))
            for i in range(len(Ys) - 1)
        ]
        margins = [d / (t + 1e-12) for d, t in zip(deltas, thresholds)]

        jnd_alignment = float(np.mean(margins)) if margins else 0.0

        return {
            "jnd_alignment": round(jnd_alignment, 4),
            "layers_analyzed": len(Ys),
            "luminances": [round(y, 6) for y in Ys],
            "deltas": [round(d, 6) for d in deltas],
            "thresholds": [round(t, 6) for t in thresholds],
            "margins": [round(m, 4) for m in margins],
            "passed": jnd_alignment > 0.5,
        }

    @classmethod
    def tafd(
        cls,
        colors: Dict[str, "Color"],
        layers: List[str] = None,
    ) -> Dict:
        """
        Calculate TAFD (Temporal Anti-Flicker Distance).

        Flicker risk: F0 = k * C0 where C0 = max contrast
        TAFD = 1 - F0 (higher = safer)

        Args:
            colors: Dict mapping token names to Color objects
            layers: Token names for background layers

        Returns:
            Dict with TAFD analysis
        """
        if layers is None:
            layers = [
                "bg", "popup_bg", "cursor_line", "visual",
                "status_line", "fold"
            ]

        Ys = []
        for layer in layers:
            if layer in colors:
                Ys.append(cls._y_from_color(colors[layer]))

        # Fallback to synthesized layers
        if not Ys and "bg" in colors:
            Ys = cls.synthesize_bg_layers(colors["bg"])

        if not Ys:
            return {"TAFD": 1.0, "max_F0": 0.0, "passed": True}

        Ys_sorted = sorted(set(Ys))

        # Calculate contrasts between adjacent layers
        contrasts = []
        for i in range(len(Ys_sorted) - 1):
            delta = abs(Ys_sorted[i + 1] - Ys_sorted[i])
            avg = (Ys_sorted[i + 1] + Ys_sorted[i]) / 2.0
            if avg > 0:
                contrasts.append(delta / avg)

        C0 = max(contrasts) if contrasts else 0.0
        F0 = cls.TAFD_K * C0
        TAFD = 1.0 - F0

        return {
            "TAFD": round(TAFD, 4),
            "max_F0": round(F0, 6),
            "max_contrast": round(C0, 4),
            "layers_analyzed": len(Ys_sorted),
            "passed": F0 < 0.01,
        }

    @classmethod
    def drift_index(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Calculate Drift Index for chroma stability over time.

        Models chromatic adaptation over extended viewing.
        D(t) = C0 * e^(-kt)
        DI = 1 - D(120min)/C0 (higher = more stable)

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Dict with drift index analysis
        """
        tokens = ["variable", "function", "type", "keyword", "string", "constant"]
        present = [t for t in tokens if t in colors]

        if not present:
            return {"drift_index": 0.0, "passed": True}

        # Collect chromas
        chromas = []
        for t in present:
            c = colors[t].oklab
            chroma = math.hypot(c[1], c[2])
            chromas.append(chroma)

        C0 = float(np.mean(chromas))

        # Decay after 120 minutes
        D120 = C0 * math.exp(-cls.DRIFT_K * 120.0)
        drift_index = 1.0 - (D120 / (C0 + 1e-12))

        return {
            "drift_index": round(drift_index, 4),
            "initial_chroma": round(C0, 4),
            "adapted_chroma_120min": round(D120, 4),
            "tokens_analyzed": len(present),
            "passed": drift_index > 0.1,
        }

    @classmethod
    def analyze(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Run all temporal analyses.

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Combined temporal analysis results
        """
        jnd = cls.mesopic_jnd(colors)
        tafd = cls.tafd(colors)
        drift = cls.drift_index(colors)

        # Combined temporal score
        jnd_score = min(jnd["jnd_alignment"] * 100, 100)
        tafd_score = tafd["TAFD"] * 100
        drift_score = drift["drift_index"] * 100

        temporal_score = (
            jnd_score * 0.4 +
            tafd_score * 0.3 +
            drift_score * 0.3
        )

        return {
            "jnd": jnd,
            "tafd": tafd,
            "drift": drift,
            "temporal_score": round(temporal_score, 2),
            "passed": jnd["passed"] and tafd["passed"] and drift["passed"],
        }
