"""
chrometric/models/health.py - Eye Health Metrics

Estimates eye strain factors for extended coding sessions:
- Blue light exposure index
- Polarity detection (dark vs light mode)
- Melanopic load
- Cognitive load
"""

from __future__ import annotations

import math
from typing import Dict, List, TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from ..color import Color


class EyeHealthModel:
    """Eye health and strain metrics for colorscheme evaluation."""

    # Background tokens (excluded from blue light calculation)
    BACKGROUND_TOKENS = {"bg", "cursor_line", "cursor_column", "popup_bg", "visual", "fold", "sign_column"}

    # Weights for different token categories in melanopic calculation
    MELANOPIC_WEIGHTS = {
        "keyword": 0.20,
        "string": 0.15,
        "function": 0.20,
        "type": 0.15,
        "variable": 0.20,
        "comment": 0.10,
    }

    @classmethod
    def blue_light_index(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Calculate blue light exposure index.

        Higher blue ratio + higher luminance = more eye strain.
        Score 0-1 where lower is better.

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Dict with blue light analysis
        """
        total_exposure = 0.0
        count = 0
        breakdown: Dict[str, float] = {}

        for name, c in colors.items():
            # Skip background elements
            if name in cls.BACKGROUND_TOKENS:
                continue

            # Blue proportion weighted by intensity
            blue_ratio = c.blue_ratio
            intensity = c.Y

            # Exposure = blue_ratio * intensity (higher = more strain)
            exposure = blue_ratio * intensity
            breakdown[name] = round(exposure, 4)
            total_exposure += exposure
            count += 1

        avg_exposure = total_exposure / count if count > 0 else 0.0

        # Score: lower is better
        # Threshold: 0.15 is comfortable, 0.25+ is high strain
        return {
            "blue_light_index": round(avg_exposure, 4),
            "total_exposure": round(total_exposure, 4),
            "breakdown": breakdown,
            "rating": "low" if avg_exposure < 0.12 else (
                "moderate" if avg_exposure < 0.20 else "high"
            ),
            "passed": avg_exposure < 0.20,
        }

    @classmethod
    def polarity_analysis(cls, bg: "Color") -> Dict:
        """
        Analyze colorscheme polarity (dark vs light mode).

        Args:
            bg: Background color

        Returns:
            Dict with polarity analysis
        """
        y = bg.Y
        l_oklab = bg.lightness_oklab

        if y < 0.1:
            mode = "dark"
            comfort = "high"  # Dark mode is generally easier on eyes
        elif y < 0.2:
            mode = "dark"
            comfort = "moderate"
        elif y > 0.8:
            mode = "light"
            comfort = "low"  # Very bright backgrounds cause strain
        elif y > 0.5:
            mode = "light"
            comfort = "moderate"
        else:
            mode = "medium"
            comfort = "moderate"

        return {
            "mode": mode,
            "luminance": round(y, 4),
            "oklab_lightness": round(l_oklab, 4),
            "comfort_rating": comfort,
        }

    @classmethod
    def melanopic_load(
        cls,
        colors: Dict[str, "Color"],
        weights: Dict[str, float] = None,
    ) -> Dict:
        """
        Calculate melanopic (circadian) light load.

        Blue light affects melatonin production and circadian rhythm.
        This metric estimates the impact on alertness/sleep.

        Args:
            colors: Dict mapping token names to Color objects
            weights: Optional custom weights for token categories

        Returns:
            Dict with melanopic load analysis
        """
        if weights is None:
            weights = cls.MELANOPIC_WEIGHTS

        available = [k for k in weights.keys() if k in colors]
        if not available:
            return {
                "melanopic_load": 0.0,
                "circadian_friendliness": 1.0,
                "passed": False,
            }

        # Weight by blue channel in linear RGB
        weighted_sum = sum(
            weights.get(name, 0) * colors[name].rgb_linear[2]
            for name in available
        )

        melanopic_index = float(np.clip(weighted_sum, 0.0, 1.0))
        circadian_friendliness = round(1.0 - melanopic_index, 3)

        return {
            "melanopic_load": round(melanopic_index, 3),
            "circadian_friendliness": circadian_friendliness,
            "rating": "low" if melanopic_index < 0.50 else (
                "moderate" if melanopic_index < 0.70 else "high"
            ),
            "passed": melanopic_index < 0.70,
        }

    @classmethod
    def cognitive_load(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Estimate cognitive load from color salience vs separation.

        High salience (chroma) with poor separation = high cognitive load.
        The brain has to work harder to distinguish similar bright colors.

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Dict with cognitive load analysis
        """
        tokens = ["keyword", "string", "function", "type", "variable", "comment"]
        present = [t for t in tokens if t in colors]

        if not present:
            return {"cognitive_load": 0.0, "passed": False}

        # Collect chromas and Oklab vectors
        chromas: List[float] = []
        labs: List[np.ndarray] = []

        for t in present:
            c = colors[t].oklab
            chroma = math.hypot(c[1], c[2])
            chromas.append(chroma)
            labs.append(c)

        # Average salience (chroma)
        salience = float(np.mean(chromas))

        # Average pairwise separation
        dists: List[float] = []
        for i in range(len(labs)):
            for j in range(i + 1, len(labs)):
                dists.append(float(np.linalg.norm(labs[i] - labs[j])))

        mean_separation = float(np.mean(dists)) if dists else 1e-6

        # Cognitive load = salience / separation (scaled)
        # High salience with low separation = high load
        cognitive_load = salience / (mean_separation + 1e-9) * 10.0

        return {
            "cognitive_load": round(cognitive_load, 3),
            "salience": round(salience, 3),
            "mean_separation": round(mean_separation, 3),
            "rating": "low" if cognitive_load < 6.0 else (
                "moderate" if cognitive_load < 10.0 else "high"
            ),
            "passed": cognitive_load < 10.0,
        }

    @classmethod
    def analyze(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Run all eye health analyses.

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Combined health analysis results
        """
        bg = colors.get("bg")

        results = {
            "blue_light": cls.blue_light_index(colors),
            "melanopic": cls.melanopic_load(colors),
            "cognitive": cls.cognitive_load(colors),
        }

        if bg:
            results["polarity"] = cls.polarity_analysis(bg)

        # Overall health score (lower is better for most metrics)
        blue_score = 100 - (results["blue_light"]["blue_light_index"] * 400)
        melanopic_score = results["melanopic"]["circadian_friendliness"] * 100
        cognitive_score = 100 - (results["cognitive"]["cognitive_load"] * 5)

        health_score = (
            blue_score * 0.3 +
            melanopic_score * 0.3 +
            cognitive_score * 0.4
        )

        results["health_score"] = round(max(0, min(100, health_score)), 2)
        results["passed"] = all([
            results["blue_light"]["passed"],
            results["melanopic"]["passed"],
            results["cognitive"]["passed"],
        ])

        return results
