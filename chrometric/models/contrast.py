"""
chrometric/models/contrast.py - Contrast Metrics (T1)

Additional contrast metrics beyond APCA for comprehensive readability analysis:
- Weber Contrast: (L_txt - L_bg) / L_bg
- Michelson Contrast: (L_max - L_min) / (L_max + L_min)
- RMS Contrast: Root mean square pixel contrast
- Edge Density: Local gradient analysis for visual jitter
"""

from __future__ import annotations

import math
from typing import Dict, List, TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from ..color import Color


class ContrastModel:
    """
    Advanced contrast metrics for T1 (Physiological Readability).

    These metrics complement APCA by providing different perspectives
    on contrast and visual clarity.
    """

    # Text tokens for analysis
    TEXT_TOKENS = [
        "keyword", "string", "function", "type", "variable", "comment",
        "constant", "operator", "number", "boolean", "property", "parameter",
    ]

    # Thresholds
    WEBER_THRESHOLD = 3.0  # Minimum Weber contrast for readability
    MICHELSON_THRESHOLD = 0.3  # Minimum Michelson contrast
    RMS_THRESHOLD = 0.05  # Minimum RMS for sufficient variation

    @staticmethod
    def weber_contrast(text: "Color", bg: "Color") -> float:
        """
        Calculate Weber contrast between text and background.

        Weber contrast is the standard formula for threshold detection:
        C_w = (L_txt - L_bg) / L_bg

        Higher absolute values indicate better contrast.

        Args:
            text: Text/foreground color
            bg: Background color

        Returns:
            Weber contrast value (can be negative for dark text on light bg)
        """
        L_txt = text.Y
        L_bg = bg.Y

        # Avoid division by zero
        if L_bg < 1e-9:
            L_bg = 1e-9

        return (L_txt - L_bg) / L_bg

    @staticmethod
    def michelson_contrast(colors: List["Color"]) -> float:
        """
        Calculate Michelson contrast for a set of colors.

        Michelson contrast measures the range of luminances:
        C_m = (L_max - L_min) / (L_max + L_min)

        Range: 0 to 1, where 1 is maximum contrast.

        Args:
            colors: List of Color objects

        Returns:
            Michelson contrast value (0-1)
        """
        if not colors:
            return 0.0

        Ys = [c.Y for c in colors]
        L_max = max(Ys)
        L_min = min(Ys)

        denominator = L_max + L_min
        if denominator < 1e-9:
            return 0.0

        return (L_max - L_min) / denominator

    @staticmethod
    def rms_contrast(colors: List["Color"]) -> float:
        """
        Calculate RMS (Root Mean Square) contrast.

        RMS contrast measures the standard deviation of luminances
        relative to the mean, indicating overall contrast variation:
        RMS = sqrt(mean((L - L_mean)^2))

        Higher values indicate more contrast variation in the palette.

        Args:
            colors: List of Color objects

        Returns:
            RMS contrast value
        """
        if len(colors) < 2:
            return 0.0

        Ys = np.array([c.Y for c in colors])
        mean_Y = np.mean(Ys)

        # Standard deviation of luminances
        rms = np.sqrt(np.mean((Ys - mean_Y) ** 2))

        return float(rms)

    @classmethod
    def edge_density(cls, colors: Dict[str, "Color"]) -> float:
        """
        Calculate edge density metric for visual jitter assessment.

        Edge density measures how many "edges" (significant luminance changes)
        exist between adjacent syntax tokens. High edge density can cause
        visual fatigue.

        Uses a luminance gradient approach across syntax-adjacent token pairs.

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Edge density (0-1), where lower is better
        """
        # Common adjacency patterns in code
        adjacencies = [
            ("keyword", "variable"),
            ("keyword", "function"),
            ("function", "variable"),
            ("variable", "operator"),
            ("operator", "number"),
            ("type", "variable"),
            ("string", "operator"),
            ("comment", "keyword"),
            ("constant", "operator"),
        ]

        gradients = []
        for token1, token2 in adjacencies:
            if token1 in colors and token2 in colors:
                Y1 = colors[token1].Y
                Y2 = colors[token2].Y

                # Absolute gradient
                gradient = abs(Y2 - Y1)
                gradients.append(gradient)

        if not gradients:
            return 0.0

        # Calculate edge density as the proportion of high-gradient pairs
        # A gradient > 0.3 is considered a "sharp edge"
        edge_threshold = 0.3
        sharp_edges = sum(1 for g in gradients if g > edge_threshold)
        edge_density = sharp_edges / len(gradients)

        return float(edge_density)

    @classmethod
    def wcag_contrast_ratio(cls, fg: "Color", bg: "Color") -> float:
        """
        Calculate WCAG 2.1 contrast ratio.

        Standard formula: CR = (L1 + 0.05) / (L2 + 0.05)
        where L1 is the lighter luminance.

        Args:
            fg: Foreground color
            bg: Background color

        Returns:
            Contrast ratio (1:1 to 21:1)
        """
        L1 = fg.Y + 0.05
        L2 = bg.Y + 0.05

        if L2 <= 0:
            return 1.0

        return max(L1, L2) / min(L1, L2)

    @classmethod
    def analyze(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Run all contrast analyses.

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Dict with comprehensive contrast analysis
        """
        bg = colors.get("bg")
        fg = colors.get("fg")

        if not bg:
            return {"error": "No background color defined"}

        # Collect text colors
        text_colors = [colors[t] for t in cls.TEXT_TOKENS if t in colors]

        results = {
            "weber": {},
            "michelson": 0.0,
            "rms": 0.0,
            "edge_density": 0.0,
            "wcag": {},
        }

        # Weber contrast for each text token
        weber_values = []
        for token in cls.TEXT_TOKENS:
            if token in colors:
                weber = cls.weber_contrast(colors[token], bg)
                results["weber"][token] = round(weber, 4)
                weber_values.append(abs(weber))

        if weber_values:
            results["weber"]["mean"] = round(float(np.mean(weber_values)), 4)
            results["weber"]["min"] = round(float(np.min(weber_values)), 4)
            results["weber"]["passed"] = results["weber"]["min"] >= cls.WEBER_THRESHOLD

        # Michelson contrast (all colors including bg)
        all_colors = text_colors + [bg]
        results["michelson"] = round(cls.michelson_contrast(all_colors), 4)
        results["michelson_passed"] = results["michelson"] >= cls.MICHELSON_THRESHOLD

        # RMS contrast
        results["rms"] = round(cls.rms_contrast(all_colors), 4)
        results["rms_passed"] = results["rms"] >= cls.RMS_THRESHOLD

        # Edge density
        results["edge_density"] = round(cls.edge_density(colors), 4)
        results["edge_density_passed"] = results["edge_density"] < 0.5  # Lower is better

        # WCAG for reference
        if fg:
            wcag_ratio = cls.wcag_contrast_ratio(fg, bg)
            results["wcag"] = {
                "ratio": round(wcag_ratio, 2),
                "passed_aa": wcag_ratio >= 4.5,
                "passed_aa_large": wcag_ratio >= 3.0,
                "passed_aaa": wcag_ratio >= 7.0,
            }

        # Overall contrast score
        # Weighted by importance
        weber_score = min(results["weber"].get("min", 0) / cls.WEBER_THRESHOLD * 100, 100)
        michelson_score = min(results["michelson"] / cls.MICHELSON_THRESHOLD * 100, 100)
        rms_score = min(results["rms"] / cls.RMS_THRESHOLD * 100, 100)
        edge_score = (1 - results["edge_density"]) * 100  # Inverted

        results["contrast_score"] = round(
            weber_score * 0.4 + michelson_score * 0.3 + rms_score * 0.2 + edge_score * 0.1,
            2
        )

        results["passed"] = all([
            results["weber"].get("passed", False),
            results["michelson_passed"],
            results["rms_passed"],
            results["edge_density_passed"],
        ])

        return results
