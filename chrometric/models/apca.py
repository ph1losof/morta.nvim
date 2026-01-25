"""
chrometric/models/apca.py - APCA Contrast Model

APCA (Accessible Perceptual Contrast Algorithm) - SAPC 0.0.98G

Key differences from WCAG:
- Uses power curves optimized for each polarity
- Better for dark mode (correctly models halation)
- Returns Lc (Lightness Contrast) on ~0-106 scale

Guidelines:
- Lc 75+: Body text (preferred)
- Lc 60+: Body text (minimum)
- Lc 45+: Large text / UI components
- Lc 30+: Non-text elements
"""

from __future__ import annotations

from typing import Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from ..color import Color


class APCAModel:
    """APCA (SAPC-8) contrast model for readability assessment."""

    # APCA thresholds
    THRESHOLD_BODY_PREFERRED = 75.0
    THRESHOLD_BODY_MINIMUM = 60.0
    THRESHOLD_LARGE_TEXT = 45.0
    THRESHOLD_NON_TEXT = 30.0

    @staticmethod
    def contrast(text: "Color", bg: "Color") -> float:
        """
        Calculate APCA Lc (Lightness Contrast) between text and background.

        Returns a value on approximately 0-106 scale where:
        - Positive values indicate dark text on light background
        - The absolute value indicates contrast magnitude

        Args:
            text: Text color
            bg: Background color

        Returns:
            APCA Lc contrast value
        """
        Y_txt = text.Y_apca
        Y_bg = bg.Y_apca

        # Soft clamp to avoid issues with very dark colors
        Y_txt = max(Y_txt, 0.0)
        Y_bg = max(Y_bg, 0.0)

        # SAPC power curves differ by polarity
        if Y_bg > Y_txt:
            # Light background, dark text (positive polarity)
            S_txt = Y_txt ** 0.57
            S_bg = Y_bg ** 0.56
            C = S_bg - S_txt
        else:
            # Dark background, light text (negative polarity)
            # This is optimized for dark mode - handles halation better
            S_txt = Y_txt ** 0.62
            S_bg = Y_bg ** 0.65
            C = S_bg - S_txt

        # Scale factor and clamp
        Lc = abs(C) * 114.0 if abs(C) >= 0.001 else 0.0

        return Lc

    @staticmethod
    def score_contrast(lc: float, target: float = 75.0) -> float:
        """
        Convert Lc to a 0-100 score based on target threshold.

        Args:
            lc: APCA Lc contrast value
            target: Target Lc for 100% score (default: 75 for body text)

        Returns:
            Score from 0-100+
        """
        if lc <= 0:
            return 0.0
        # Linear scaling with target as 100%
        return min((lc / target) * 100.0, 120.0)

    @classmethod
    def analyze(
        cls,
        colors: Dict[str, "Color"],
        bg: "Color",
        fg: "Color" = None,
    ) -> Dict:
        """
        Analyze APCA contrast for all text tokens against background.

        Args:
            colors: Dict mapping token names to Color objects
            bg: Background color
            fg: Optional foreground color (defaults to colors['fg'])

        Returns:
            Dict with contrast analysis results
        """
        if fg is None:
            fg = colors.get("fg")

        # Primary contrast: fg vs bg
        primary_lc = 0.0
        if fg and bg:
            primary_lc = cls.contrast(fg, bg)

        # Text tokens to check
        text_tokens = [
            "keyword",
            "string",
            "function",
            "type",
            "variable",
            "comment",
            "constant",
            "operator",
            "number",
            "boolean",
            "property",
            "parameter",
        ]

        # Analyze each token
        token_results: Dict[str, Dict] = {}
        lc_values: List[float] = []

        for token in text_tokens:
            if token not in colors:
                continue

            lc = cls.contrast(colors[token], bg)
            lc_values.append(lc)

            passed = lc >= cls.THRESHOLD_BODY_MINIMUM
            level = "excellent" if lc >= cls.THRESHOLD_BODY_PREFERRED else (
                "adequate" if lc >= cls.THRESHOLD_BODY_MINIMUM else (
                    "marginal" if lc >= cls.THRESHOLD_LARGE_TEXT else "poor"
                )
            )

            token_results[token] = {
                "lc": round(lc, 1),
                "passed": passed,
                "level": level,
            }

        # Special case: comment contrast (lower threshold OK)
        if "comment" in token_results:
            comment_lc = token_results["comment"]["lc"]
            # Comments can be lighter, Lc 45+ is acceptable
            token_results["comment"]["passed"] = comment_lc >= cls.THRESHOLD_LARGE_TEXT

        # Aggregate metrics
        mean_lc = sum(lc_values) / len(lc_values) if lc_values else 0.0
        min_lc = min(lc_values) if lc_values else 0.0
        all_passed = all(r["passed"] for r in token_results.values())

        # Overall score (weighted toward minimum)
        overall_score = cls.score_contrast(min_lc * 0.4 + mean_lc * 0.6)

        return {
            "primary_lc": round(primary_lc, 1),
            "mean_lc": round(mean_lc, 1),
            "min_lc": round(min_lc, 1),
            "score": round(overall_score, 2),
            "tokens": token_results,
            "passed": all_passed and primary_lc >= cls.THRESHOLD_BODY_MINIMUM,
        }
