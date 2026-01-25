"""
chrometric/models/readability.py - Advanced Readability Metrics (T1)

High-level readability metrics beyond basic contrast:
- Halation Risk Index: Penalty for excessive contrast on very dark backgrounds
- Pelli-Robson Sensitivity: LogCS fatigue model for sustained reading
- Mesopic JND Enhancement: Enhanced Just Noticeable Difference for low-light
"""

from __future__ import annotations

import math
from typing import Dict, List, TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from ..color import Color


class ReadabilityModel:
    """
    Advanced readability metrics for T1 (Physiological Readability).

    These metrics address specific visual comfort issues that aren't
    captured by basic contrast measurements.
    """

    # Text tokens for analysis
    TEXT_TOKENS = [
        "keyword", "string", "function", "type", "variable", "comment",
        "constant", "operator", "number", "boolean", "property", "parameter",
    ]

    # Halation thresholds
    HALATION_LC_THRESHOLD = 90.0  # Lc above which halation risk exists
    HALATION_BG_THRESHOLD = 0.05  # Y_bg below which halation is problematic

    # Pelli-Robson constants
    PELLI_ROBSON_OPTIMAL = 2.0  # Optimal LogCS value

    # JND constants (mesopic vision)
    JND_ALPHA = 5.0
    JND_BETA = 0.4

    @classmethod
    def halation_risk(
        cls,
        text: "Color",
        bg: "Color",
        lc: float = None,
    ) -> float:
        """
        Calculate halation risk index.

        Halation occurs when very bright text on very dark backgrounds
        causes optical "blooming" that reduces legibility. This is
        especially problematic in dark mode themes.

        Penalizes when: Lc > 90 AND Y_bg < 0.05

        Args:
            text: Text color
            bg: Background color
            lc: Pre-computed APCA Lc value (optional)

        Returns:
            Halation risk (0-1), where 0 is no risk and 1 is severe risk
        """
        Y_bg = bg.Y
        Y_txt = text.Y

        # If Lc not provided, estimate from luminance difference
        if lc is None:
            # Simplified Lc estimation
            if Y_bg > Y_txt:
                S_txt = Y_txt ** 0.57
                S_bg = Y_bg ** 0.56
            else:
                S_txt = Y_txt ** 0.62
                S_bg = Y_bg ** 0.65
            lc = abs(S_bg - S_txt) * 114.0

        # No halation risk if contrast is reasonable
        if lc <= cls.HALATION_LC_THRESHOLD:
            return 0.0

        # No halation risk if background is not very dark
        if Y_bg >= cls.HALATION_BG_THRESHOLD:
            return 0.0

        # Calculate risk based on how much we exceed thresholds
        lc_excess = (lc - cls.HALATION_LC_THRESHOLD) / (106 - cls.HALATION_LC_THRESHOLD)
        bg_darkness = (cls.HALATION_BG_THRESHOLD - Y_bg) / cls.HALATION_BG_THRESHOLD

        # Combined risk (product of excess factors)
        risk = lc_excess * bg_darkness

        # Also consider text brightness
        if Y_txt > 0.9:
            risk *= 1.5  # Extra penalty for very bright text

        return min(risk, 1.0)

    @classmethod
    def pelli_robson_sensitivity(cls, text: "Color", bg: "Color") -> float:
        """
        Calculate Pelli-Robson contrast sensitivity.

        The Pelli-Robson test measures the minimum contrast a person
        can detect. LogCS (log contrast sensitivity) indicates how
        well the color pair supports sustained reading.

        LogCS = -log10(C_min)

        Higher values indicate better sensitivity (easier to read).

        Args:
            text: Text color
            bg: Background color

        Returns:
            LogCS value (typically 0-3, higher is better)
        """
        L_txt = text.Y
        L_bg = bg.Y

        # Calculate Weber contrast
        if L_bg < 1e-9:
            L_bg = 1e-9

        weber = abs(L_txt - L_bg) / L_bg

        # Minimum detectable contrast (at threshold)
        # Weber contrast threshold varies with luminance
        # Using simplified model
        C_min = 0.01 + 0.005 / (L_bg + 0.001)

        # If contrast is below threshold, return 0
        if weber <= C_min:
            return 0.0

        # LogCS calculation
        # Higher contrast = higher sensitivity
        log_cs = -math.log10(C_min) + math.log10(weber / C_min + 1)

        return max(0.0, min(3.0, log_cs))

    @classmethod
    def mesopic_jnd_enhanced(
        cls,
        colors: Dict[str, "Color"],
        bg: "Color",
    ) -> Dict:
        """
        Enhanced Mesopic JND (Just Noticeable Difference) analysis.

        Analyzes luminance differences relative to the mesopic JND threshold:
        ΔL_th(L) = α * L + β * √L

        This determines if luminance differences between elements are
        reliably distinguishable under typical coding conditions.

        Args:
            colors: Dict mapping token names to Color objects
            bg: Background color

        Returns:
            Dict with JND analysis results
        """
        L_bg = bg.Y

        # Mesopic JND threshold at background luminance
        jnd_threshold = cls.JND_ALPHA * L_bg + cls.JND_BETA * math.sqrt(max(L_bg, 0))

        results = {
            "bg_luminance": round(L_bg, 6),
            "jnd_threshold": round(jnd_threshold, 6),
            "tokens": {},
            "above_jnd_count": 0,
            "total_count": 0,
        }

        for token in cls.TEXT_TOKENS:
            if token not in colors:
                continue

            L_txt = colors[token].Y
            delta_L = abs(L_txt - L_bg)

            # Compute margin (how many JNDs above threshold)
            margin = delta_L / (jnd_threshold + 1e-9)

            results["tokens"][token] = {
                "luminance": round(L_txt, 6),
                "delta": round(delta_L, 6),
                "margin": round(margin, 4),
                "visible": margin > 1.0,
            }

            results["total_count"] += 1
            if margin > 1.0:
                results["above_jnd_count"] += 1

        # JND alignment score
        if results["total_count"] > 0:
            results["jnd_alignment"] = round(
                results["above_jnd_count"] / results["total_count"],
                4
            )
        else:
            results["jnd_alignment"] = 0.0

        results["passed"] = results["jnd_alignment"] >= 0.8

        return results

    @classmethod
    def small_text_jnd(cls, text: "Color", bg: "Color") -> float:
        """
        Calculate JND margin for small text (8pt).

        Small text requires higher contrast due to reduced visual acuity.
        Uses a stricter JND threshold.

        Args:
            text: Text color
            bg: Background color

        Returns:
            JND margin (>1.0 means visible)
        """
        L_bg = bg.Y
        L_txt = text.Y

        # Stricter threshold for small text (1.5x normal)
        jnd_threshold = 1.5 * (cls.JND_ALPHA * L_bg + cls.JND_BETA * math.sqrt(max(L_bg, 0)))

        delta_L = abs(L_txt - L_bg)
        margin = delta_L / (jnd_threshold + 1e-9)

        return float(margin)

    @classmethod
    def large_text_jnd(cls, text: "Color", bg: "Color") -> float:
        """
        Calculate JND margin for large text (18pt+).

        Large text is more forgiving, using a relaxed JND threshold.

        Args:
            text: Text color
            bg: Background color

        Returns:
            JND margin (>1.0 means visible)
        """
        L_bg = bg.Y
        L_txt = text.Y

        # Relaxed threshold for large text (0.75x normal)
        jnd_threshold = 0.75 * (cls.JND_ALPHA * L_bg + cls.JND_BETA * math.sqrt(max(L_bg, 0)))

        delta_L = abs(L_txt - L_bg)
        margin = delta_L / (jnd_threshold + 1e-9)

        return float(margin)

    @classmethod
    def analyze(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Run all readability analyses.

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Dict with comprehensive readability analysis
        """
        bg = colors.get("bg")
        fg = colors.get("fg")

        if not bg:
            return {"error": "No background color defined"}

        results = {
            "halation": {},
            "pelli_robson": {},
            "mesopic_jnd": {},
        }

        # Halation risk for each text token
        halation_values = []
        for token in cls.TEXT_TOKENS:
            if token in colors:
                risk = cls.halation_risk(colors[token], bg)
                results["halation"][token] = round(risk, 4)
                halation_values.append(risk)

        if halation_values:
            results["halation"]["mean"] = round(float(np.mean(halation_values)), 4)
            results["halation"]["max"] = round(float(np.max(halation_values)), 4)
            results["halation"]["passed"] = results["halation"]["max"] < 0.3

        # Pelli-Robson sensitivity for each text token
        sensitivity_values = []
        for token in cls.TEXT_TOKENS:
            if token in colors:
                log_cs = cls.pelli_robson_sensitivity(colors[token], bg)
                results["pelli_robson"][token] = round(log_cs, 4)
                sensitivity_values.append(log_cs)

        if sensitivity_values:
            results["pelli_robson"]["mean"] = round(float(np.mean(sensitivity_values)), 4)
            results["pelli_robson"]["min"] = round(float(np.min(sensitivity_values)), 4)
            results["pelli_robson"]["passed"] = results["pelli_robson"]["min"] >= 1.5

        # Mesopic JND analysis
        results["mesopic_jnd"] = cls.mesopic_jnd_enhanced(colors, bg)

        # Small and large text JND
        if fg:
            results["jnd_small"] = round(cls.small_text_jnd(fg, bg), 4)
            results["jnd_large"] = round(cls.large_text_jnd(fg, bg), 4)

        # Overall readability score
        halation_score = (1 - results["halation"].get("max", 0)) * 100
        pelli_score = min(results["pelli_robson"].get("mean", 0) / cls.PELLI_ROBSON_OPTIMAL * 100, 100)
        jnd_score = results["mesopic_jnd"].get("jnd_alignment", 0) * 100

        results["readability_score"] = round(
            halation_score * 0.3 + pelli_score * 0.4 + jnd_score * 0.3,
            2
        )

        results["passed"] = all([
            results["halation"].get("passed", False),
            results["pelli_robson"].get("passed", False),
            results["mesopic_jnd"].get("passed", False),
        ])

        return results
