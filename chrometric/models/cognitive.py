"""
chrometric/models/cognitive.py - Cognitive Metrics (T2)

Advanced cognitive and semantic metrics for code comprehension:
- Semantic Entropy: Color density and distribution
- Functional Delta E: Distinguishability between functional categories
- Visual Saliency: Itti-Koch attention model approximation
- Feature Congestion: Rosenholtz clutter metric
- Subband Entropy: Spatial frequency complexity
- JND variants for different text sizes
"""

from __future__ import annotations

import math
from typing import Dict, List, Tuple, TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from ..color import Color


class CognitiveModel:
    """
    Cognitive metrics for T2 (Cognitive Logic & Semantics).

    These metrics evaluate how well the colorscheme supports
    code comprehension and visual parsing efficiency.

    Based on research:
    - Sarkar 2015: Syntax highlighting reduces comprehension time by 8.4s
    - Hindle et al. 2016: Code follows n-gram patterns with 3-4 bits entropy
    - Busjahn et al. 2014: Eye-tracking shows identifier-expression focus
    """

    # Import from token registry when available
    try:
        from ..tokens import TokenRegistry
        SYNTAX_TOKENS = TokenRegistry.SYNTAX_CORE[:6]
        FUNCTIONAL_GROUPS = TokenRegistry.FUNCTIONAL_GROUPS
    except ImportError:
        # Fallback
        SYNTAX_TOKENS = ["keyword", "string", "function", "type", "variable", "comment"]
        FUNCTIONAL_GROUPS = {
            "control": ["keyword", "operator"],
            "data": ["string", "number", "boolean", "constant"],
            "structure": ["function", "type", "namespace"],
            "identifier": ["variable", "parameter", "property"],
            "documentation": ["comment"],
            "diagnostic": ["error", "warning", "info", "hint"],
        }

    # Extended syntax tokens for comprehensive analysis
    SYNTAX_TOKENS_EXTENDED = [
        "keyword", "string", "function", "type", "variable", "comment",
        "constant", "operator", "number", "boolean", "property", "parameter",
    ]

    # Critical pairs for functional delta E (expanded)
    CRITICAL_PAIRS = [
        ("keyword", "variable"),
        ("keyword", "string"),
        ("function", "variable"),
        ("type", "variable"),
        ("function", "type"),
        ("constant", "variable"),
        ("parameter", "variable"),
        ("property", "variable"),
    ]

    # Inter-group distinctness requirements (research-backed)
    GROUP_DISTINCTNESS = {
        ("diagnostic", "identifier"): 0.25,   # Errors must pop on variables
        ("diagnostic", "structure"): 0.25,    # Errors must pop on functions
        ("identifier", "structure"): 0.15,    # Variables vs functions
        ("data", "identifier"): 0.12,         # Literals vs variables
        ("control", "identifier"): 0.10,      # Keywords vs variables
        ("documentation", "identifier"): 0.18,  # Comments must recede
    }

    @classmethod
    def semantic_entropy(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Calculate semantic entropy of the colorscheme.

        Entropy measures the information content of the color distribution.
        Higher entropy = more distinct colors = better differentiation.

        H = -Σ p(c) * log2(p(c))

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Dict with entropy analysis
        """
        present = [t for t in cls.SYNTAX_TOKENS if t in colors]

        if len(present) < 2:
            return {"entropy": 0.0, "passed": False}

        # Collect Oklab vectors
        labs = [colors[t].oklab for t in present]

        # Quantize colors into bins for entropy calculation
        # Using 8 bins per channel (L, a, b)
        bins = 8
        quantized = []

        for lab in labs:
            # Normalize to 0-1 range
            L_norm = lab[0]  # Already 0-1
            a_norm = (lab[1] + 0.4) / 0.8  # Approximate range
            b_norm = (lab[2] + 0.4) / 0.8

            # Quantize
            L_bin = int(np.clip(L_norm * bins, 0, bins - 1))
            a_bin = int(np.clip(a_norm * bins, 0, bins - 1))
            b_bin = int(np.clip(b_norm * bins, 0, bins - 1))

            quantized.append((L_bin, a_bin, b_bin))

        # Count unique quantized colors
        unique = set(quantized)
        n_unique = len(unique)

        # Calculate entropy
        counts = {}
        for q in quantized:
            counts[q] = counts.get(q, 0) + 1

        total = len(quantized)
        probs = [c / total for c in counts.values()]
        entropy = -sum(p * math.log2(p) for p in probs if p > 0)

        # Maximum possible entropy for this number of colors
        max_entropy = math.log2(len(present)) if len(present) > 1 else 1.0

        # Normalized entropy (0-1)
        norm_entropy = entropy / max_entropy if max_entropy > 0 else 0.0

        return {
            "entropy": round(entropy, 4),
            "normalized_entropy": round(norm_entropy, 4),
            "unique_colors": n_unique,
            "total_tokens": len(present),
            "passed": norm_entropy >= 0.7,  # At least 70% of max entropy
        }

    @classmethod
    def functional_delta_e(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Calculate functional delta E between critical syntax pairs.

        Measures distinguishability between tokens that frequently
        appear adjacent in code.

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Dict with functional delta E analysis
        """
        results = {
            "pairs": {},
            "mean_de": 0.0,
            "min_de": float("inf"),
        }

        de_values = []

        for token1, token2 in cls.CRITICAL_PAIRS:
            if token1 in colors and token2 in colors:
                de = colors[token1].oklab_distance(colors[token2])
                results["pairs"][f"{token1}-{token2}"] = round(de, 4)
                de_values.append(de)

                if de < results["min_de"]:
                    results["min_de"] = de

        if de_values:
            results["mean_de"] = round(float(np.mean(de_values)), 4)
            results["min_de"] = round(results["min_de"], 4)
            results["passed"] = results["min_de"] >= 0.08
        else:
            results["min_de"] = 0.0
            results["passed"] = False

        return results

    @classmethod
    def visual_saliency(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Approximate visual saliency using simplified Itti-Koch model.

        Saliency predicts where attention will be drawn first.
        For code, keywords and errors should be most salient.

        Uses chroma and luminance contrast as saliency proxies.

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Dict with saliency analysis
        """
        bg = colors.get("bg")
        if not bg:
            return {"saliency_peak": 0.0, "passed": False}

        saliency_scores = {}

        # Important tokens that should be salient
        important = ["keyword", "function", "error", "warning"]

        for token, color in colors.items():
            if token in ["bg", "fg"]:
                continue

            # Saliency based on chroma and luminance contrast
            chroma = color.oklab_chroma
            lum_contrast = abs(color.Y - bg.Y)

            # Combined saliency (chroma is weighted higher)
            saliency = chroma * 0.6 + lum_contrast * 0.4
            saliency_scores[token] = round(saliency, 4)

        if not saliency_scores:
            return {"saliency_peak": 0.0, "passed": False}

        # Find peak saliency token
        peak_token = max(saliency_scores.items(), key=lambda x: x[1])

        # Check if important tokens are among the most salient
        important_saliency = [
            saliency_scores.get(t, 0) for t in important if t in saliency_scores
        ]
        mean_important = float(np.mean(important_saliency)) if important_saliency else 0.0

        all_saliency = list(saliency_scores.values())
        mean_all = float(np.mean(all_saliency)) if all_saliency else 0.0

        return {
            "saliency_scores": saliency_scores,
            "peak_token": peak_token[0],
            "peak_value": peak_token[1],
            "important_mean": round(mean_important, 4),
            "overall_mean": round(mean_all, 4),
            "passed": mean_important >= mean_all,  # Important tokens should be above average
        }

    @classmethod
    def feature_congestion(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Calculate feature congestion (Rosenholtz clutter metric approximation).

        High congestion = too many competing visual elements = harder to parse.
        Lower is better.

        Uses variance of color features as a proxy for congestion.

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Dict with congestion analysis
        """
        present = [t for t in cls.SYNTAX_TOKENS if t in colors]

        if len(present) < 2:
            return {"congestion": 0.0, "passed": True}

        # Collect feature vectors
        features = []
        for t in present:
            c = colors[t]
            # Feature vector: [L, a, b, chroma]
            features.append([
                c.oklab[0],
                c.oklab[1],
                c.oklab[2],
                c.oklab_chroma,
            ])

        features = np.array(features)

        # Congestion = variance across features
        # High variance in any dimension indicates potential confusion
        variances = np.var(features, axis=0)
        mean_variance = float(np.mean(variances))

        # Normalize to 0-1 scale (empirical calibration)
        congestion = min(mean_variance * 10, 1.0)

        return {
            "congestion": round(congestion, 4),
            "feature_variances": {
                "L": round(variances[0], 4),
                "a": round(variances[1], 4),
                "b": round(variances[2], 4),
                "chroma": round(variances[3], 4),
            },
            "passed": congestion < 0.5,  # Lower is better
        }

    @classmethod
    def subband_entropy(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Calculate subband entropy (spatial frequency complexity).

        Measures the distribution of colors across different
        "frequency bands" (lightness levels, chroma levels).

        Higher entropy = more even distribution = better use of color space.

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Dict with subband entropy analysis
        """
        present = [t for t in cls.SYNTAX_TOKENS if t in colors]

        if len(present) < 2:
            return {"subband_entropy": 0.0, "passed": False}

        # Create 2D histogram (L vs chroma)
        L_bins = 4
        C_bins = 4

        hist = np.zeros((L_bins, C_bins))

        for t in present:
            c = colors[t]
            L_idx = int(np.clip(c.oklab[0] * L_bins, 0, L_bins - 1))
            C_idx = int(np.clip(c.oklab_chroma * C_bins / 0.2, 0, C_bins - 1))
            hist[L_idx, C_idx] += 1

        # Flatten and calculate entropy
        flat = hist.flatten()
        total = flat.sum()
        if total <= 0:
            return {"subband_entropy": 0.0, "passed": False}

        probs = flat / total
        entropy = -sum(p * math.log2(p) for p in probs if p > 0)

        # Maximum entropy for this grid
        max_entropy = math.log2(L_bins * C_bins)
        norm_entropy = entropy / max_entropy if max_entropy > 0 else 0.0

        return {
            "subband_entropy": round(entropy, 4),
            "normalized": round(norm_entropy, 4),
            "max_entropy": round(max_entropy, 4),
            "passed": norm_entropy >= 0.5,
        }

    @classmethod
    def jnd_small_text(cls, text: "Color", bg: "Color") -> float:
        """
        Calculate JND margin for small text (8pt).

        Small text requires higher contrast.

        Args:
            text: Text color
            bg: Background color

        Returns:
            JND margin (>1.0 means visible)
        """
        L_bg = bg.Y
        L_txt = text.Y

        # Stricter threshold for small text
        alpha, beta = 5.0, 0.4
        jnd = 1.5 * (alpha * L_bg + beta * math.sqrt(max(L_bg, 0)))

        delta = abs(L_txt - L_bg)
        return delta / (jnd + 1e-9)

    @classmethod
    def jnd_large_text(cls, text: "Color", bg: "Color") -> float:
        """
        Calculate JND margin for large text (18pt+).

        Large text is more forgiving.

        Args:
            text: Text color
            bg: Background color

        Returns:
            JND margin (>1.0 means visible)
        """
        L_bg = bg.Y
        L_txt = text.Y

        # Relaxed threshold for large text
        alpha, beta = 5.0, 0.4
        jnd = 0.75 * (alpha * L_bg + beta * math.sqrt(max(L_bg, 0)))

        delta = abs(L_txt - L_bg)
        return delta / (jnd + 1e-9)

    @classmethod
    def analyze(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Run all cognitive analyses.

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Dict with comprehensive cognitive analysis
        """
        bg = colors.get("bg")
        fg = colors.get("fg")

        results = {
            "semantic_entropy": cls.semantic_entropy(colors),
            "functional_de": cls.functional_delta_e(colors),
            "saliency": cls.visual_saliency(colors),
            "congestion": cls.feature_congestion(colors),
            "subband_entropy": cls.subband_entropy(colors),
        }

        # JND for primary text
        if fg and bg:
            results["jnd_small"] = round(cls.jnd_small_text(fg, bg), 4)
            results["jnd_large"] = round(cls.jnd_large_text(fg, bg), 4)

        # Overall cognitive score
        entropy_score = results["semantic_entropy"].get("normalized_entropy", 0) * 100
        func_de_score = min(results["functional_de"].get("min_de", 0) / 0.15 * 100, 100)
        saliency_score = 100 if results["saliency"].get("passed", False) else 50
        congestion_score = (1 - results["congestion"].get("congestion", 0)) * 100
        subband_score = results["subband_entropy"].get("normalized", 0) * 100

        results["cognitive_score"] = round(
            entropy_score * 0.25 +
            func_de_score * 0.30 +
            saliency_score * 0.15 +
            congestion_score * 0.15 +
            subband_score * 0.15,
            2
        )

        results["passed"] = all([
            results["semantic_entropy"].get("passed", False),
            results["functional_de"].get("passed", False),
            results["saliency"].get("passed", False),
            results["congestion"].get("passed", False),
        ])

        return results

    # =========================================================================
    # Functional Group Analysis (Research-Backed)
    # =========================================================================

    @classmethod
    def analyze_functional_groups(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Analyze color distinctness between functional groups.

        Based on eye-tracking research showing programmers organize
        visual attention by functional category.

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Dict with functional group analysis
        """
        group_colors: Dict[str, list] = {}

        # Collect colors by group
        for group, tokens in cls.FUNCTIONAL_GROUPS.items():
            group_colors[group] = []
            for token in tokens:
                if token in colors:
                    group_colors[group].append(colors[token])

        # Calculate inter-group distances
        group_analysis: Dict[str, Dict] = {}

        for (group_a, group_b), required_de in cls.GROUP_DISTINCTNESS.items():
            colors_a = group_colors.get(group_a, [])
            colors_b = group_colors.get(group_b, [])

            if not colors_a or not colors_b:
                continue

            # Find minimum distance between any pair from the two groups
            min_dist = float("inf")

            for ca in colors_a:
                for cb in colors_b:
                    dist = ca.oklab_distance(cb)
                    if dist < min_dist:
                        min_dist = dist

            key = f"{group_a}-{group_b}"
            group_analysis[key] = {
                "min_distance": round(min_dist, 4),
                "required": required_de,
                "passed": min_dist >= required_de,
                "margin": round((min_dist - required_de) / required_de, 4) if min_dist != float("inf") else 0,
            }

        # Calculate pass rate
        passed = sum(1 for a in group_analysis.values() if a["passed"])
        total = len(group_analysis)

        return {
            "group_analysis": group_analysis,
            "passed_count": passed,
            "total_count": total,
            "pass_rate": round(passed / total, 4) if total > 0 else 0.0,
            "passed": passed == total,
        }

    @classmethod
    def diagnostic_visibility(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Analyze diagnostic token visibility.

        Errors and warnings MUST stand out from regular code tokens.
        This is critical for developer productivity and safety.

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Dict with diagnostic visibility analysis
        """
        diagnostics = ["error", "warning", "info", "hint"]
        code_tokens = ["keyword", "variable", "function", "string", "type"]

        bg = colors.get("bg")
        if not bg:
            return {"diagnostic_visibility": 0.0, "passed": False}

        results = {}
        all_passed = True

        for diag in diagnostics:
            if diag not in colors:
                continue

            diag_color = colors[diag]

            # Distance from background
            bg_distance = diag_color.oklab_distance(bg)

            # Minimum distance from code tokens
            min_code_dist = float("inf")
            closest_token = ""

            for token in code_tokens:
                if token in colors:
                    dist = diag_color.oklab_distance(colors[token])
                    if dist < min_code_dist:
                        min_code_dist = dist
                        closest_token = token

            # Requirements based on diagnostic type
            if diag == "error":
                required_bg = 0.30    # Must be very visible
                required_code = 0.20  # Must stand out from code
            elif diag == "warning":
                required_bg = 0.25
                required_code = 0.15
            else:  # info, hint
                required_bg = 0.20
                required_code = 0.10

            passed = bg_distance >= required_bg and min_code_dist >= required_code
            if not passed:
                all_passed = False

            results[diag] = {
                "bg_distance": round(bg_distance, 4),
                "min_code_distance": round(min_code_dist, 4),
                "closest_token": closest_token,
                "required_bg": required_bg,
                "required_code": required_code,
                "passed": passed,
            }

        return {
            "diagnostics": results,
            "passed": all_passed,
        }
