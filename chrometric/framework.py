"""
chrometric/framework.py - Main Chrometric Framework

Integrates all analysis models and provides composite scoring.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Union

from .color import Color
from .models import (
    APCAModel,
    SyntaxContextModel,
    EyeHealthModel,
    PerceptualModel,
    CVDModel,
    TemporalModel,
    HarmonyModel,
)


@dataclass
class SchemeReport:
    """Complete analysis report for a single colorscheme."""

    name: str
    metadata: Dict = field(default_factory=dict)

    # Primary metrics (new)
    apca: Dict = field(default_factory=dict)
    syntax: Dict = field(default_factory=dict)
    health: Dict = field(default_factory=dict)

    # Perceptual metrics
    perceptual: Dict = field(default_factory=dict)

    # Safety metrics
    cvd: Dict = field(default_factory=dict)

    # Temporal metrics
    temporal: Dict = field(default_factory=dict)

    # Harmony metrics
    harmony: Dict = field(default_factory=dict)

    # Composite score
    composite: float = 0.0

    def to_dict(self) -> Dict:
        """Convert report to dictionary."""
        return {
            "name": self.name,
            "metadata": self.metadata,
            "composite_score": self.composite,
            "metrics": {
                "apca": self.apca,
                "syntax": self.syntax,
                "health": self.health,
                "perceptual": self.perceptual,
                "cvd": self.cvd,
                "temporal": self.temporal,
                "harmony": self.harmony,
            },
        }


class ChrometricFramework:
    """
    Main entry point for colorscheme analysis.

    Loads colorscheme data exported by chrometric_export.lua and
    runs all analysis models to produce comprehensive reports.
    """

    # Metric weights for composite scoring
    METRIC_WEIGHTS = {
        # Primary (new metrics) - 60%
        "apca_contrast": 0.20,      # APCA body text readability
        "syntax_adjacency": 0.20,   # Weighted token distinguishability
        "cvd_safety": 0.12,         # Color vision deficiency
        "health": 0.08,             # Blue light + cognitive load

        # Secondary (preserved metrics) - 40%
        "perceptual_oklab": 0.08,   # Oklab mean delta E
        "perceptual_cam16": 0.08,   # CAM16-UCS mean delta E
        "harmony": 0.08,            # Palette balance
        "temporal": 0.08,           # JND + TAFD + Drift
        "hksm": 0.08,               # Brightness stability
    }

    # Direction: whether higher or lower values are better
    METRIC_DIRECTION = {
        "apca_contrast": "higher",
        "syntax_adjacency": "higher",
        "cvd_safety": "higher",
        "health": "higher",         # health_score where higher is better
        "perceptual_oklab": "higher",
        "perceptual_cam16": "higher",
        "harmony": "higher",
        "temporal": "higher",
        "hksm": "lower",            # Lower HKSM is better
    }

    def __init__(self, json_path: Union[str, Path] = None, data: List[Dict] = None):
        """
        Initialize the framework.

        Args:
            json_path: Path to JSON file from chrometric_export.lua
            data: Pre-loaded scheme data (alternative to json_path)
        """
        if json_path:
            self.schemes = self._load_schemes(Path(json_path))
        elif data:
            self.schemes = data
        else:
            self.schemes = []

        self.reports: Dict[str, SchemeReport] = {}

    def _load_schemes(self, path: Path) -> List[Dict]:
        """Load schemes from JSON file."""
        if not path.exists():
            raise FileNotFoundError(f"Scheme data not found: {path}")

        with open(path, "r") as f:
            return json.load(f)

    def _parse_colors(self, scheme_data: Dict) -> Dict[str, Color]:
        """Parse color hex values into Color objects."""
        colors = {}
        raw_colors = scheme_data.get("colors", {})

        for name, hex_value in raw_colors.items():
            try:
                colors[name] = Color(name, hex_value)
            except (ValueError, Exception):
                # Skip invalid colors
                pass

        return colors

    def analyze_scheme(self, scheme_data: Dict) -> SchemeReport:
        """
        Run all analyses on a single colorscheme.

        Args:
            scheme_data: Dict with 'name', 'colors', and optional 'metadata'

        Returns:
            SchemeReport with all analysis results
        """
        name = scheme_data.get("name", "unknown")
        metadata = scheme_data.get("metadata", {})
        colors = self._parse_colors(scheme_data)

        if not colors:
            return SchemeReport(name=name, metadata=metadata)

        bg = colors.get("bg")
        fg = colors.get("fg")

        report = SchemeReport(name=name, metadata=metadata)

        # Run all models
        try:
            if bg:
                report.apca = APCAModel.analyze(colors, bg, fg)
        except Exception:
            report.apca = {"error": "Analysis failed"}

        try:
            report.syntax = SyntaxContextModel.calculate_score(colors)
        except Exception:
            report.syntax = {"error": "Analysis failed"}

        try:
            report.health = EyeHealthModel.analyze(colors)
        except Exception:
            report.health = {"error": "Analysis failed"}

        try:
            report.perceptual = PerceptualModel.analyze(colors)
        except Exception:
            report.perceptual = {"error": "Analysis failed"}

        try:
            report.cvd = CVDModel.analyze(colors)
        except Exception:
            report.cvd = {"error": "Analysis failed"}

        try:
            report.temporal = TemporalModel.analyze(colors)
        except Exception:
            report.temporal = {"error": "Analysis failed"}

        try:
            report.harmony = HarmonyModel.analyze(colors)
        except Exception:
            report.harmony = {"error": "Analysis failed"}

        return report

    def analyze(self) -> Dict[str, SchemeReport]:
        """
        Run all models on all schemes.

        Returns:
            Dict mapping scheme names to SchemeReport objects
        """
        self.reports = {}

        for scheme_data in self.schemes:
            report = self.analyze_scheme(scheme_data)
            self.reports[report.name] = report

        # Compute composite scores with relative normalization
        self._compute_composite_scores()

        return self.reports

    def _extract_metric_value(self, report: SchemeReport, metric: str) -> Optional[float]:
        """Extract a specific metric value from a report."""
        try:
            if metric == "apca_contrast":
                return report.apca.get("score", 0.0)
            elif metric == "syntax_adjacency":
                return report.syntax.get("syntax_score", 0.0)
            elif metric == "cvd_safety":
                return report.cvd.get("cvd_score", 0.0)
            elif metric == "health":
                return report.health.get("health_score", 0.0)
            elif metric == "perceptual_oklab":
                oklab = report.perceptual.get("oklab", {})
                return oklab.get("mean_delta_e", 0.0) * 100 / 0.15  # Normalize
            elif metric == "perceptual_cam16":
                cam16 = report.perceptual.get("cam16_ucs", {})
                return cam16.get("mean_delta_e_cam16", 0.0) * 100 / 0.06  # Normalize
            elif metric == "harmony":
                harmony = report.harmony.get("harmony", {})
                return harmony.get("harmony", 0.0) * 100
            elif metric == "temporal":
                return report.temporal.get("temporal_score", 0.0)
            elif metric == "hksm":
                hksm = report.harmony.get("hksm", {})
                return hksm.get("HKSM_mean", 25.0)  # Default to high value
            else:
                return None
        except Exception:
            return None

    def _compute_composite_scores(self):
        """Compute composite scores for all schemes using relative normalization."""
        if not self.reports:
            return

        schemes = list(self.reports.keys())
        scores = {s: 0.0 for s in schemes}

        for metric, weight in self.METRIC_WEIGHTS.items():
            # Collect values for this metric
            vals = []
            for scheme in schemes:
                val = self._extract_metric_value(self.reports[scheme], metric)
                vals.append(val)

            # Get valid numeric values
            numeric = [v for v in vals if v is not None]
            if not numeric:
                continue

            mn, mx = min(numeric), max(numeric)
            rng = mx - mn if abs(mx - mn) > 1e-12 else 1.0

            direction = self.METRIC_DIRECTION.get(metric, "higher")

            for i, scheme in enumerate(schemes):
                v = vals[i]
                if v is None:
                    norm = 0.0
                else:
                    if direction == "higher":
                        norm = (v - mn) / rng
                    else:
                        norm = (mx - v) / rng

                scores[scheme] += norm * weight

        # Scale to 0-100
        max_score = max(scores.values()) if scores else 1.0
        for scheme in schemes:
            self.reports[scheme].composite = round(
                (scores[scheme] / (max_score + 1e-12)) * 100, 2
            )

    def get_ranking(self) -> List[tuple]:
        """
        Get schemes ranked by composite score.

        Returns:
            List of (scheme_name, composite_score) tuples, sorted descending
        """
        return sorted(
            [(name, report.composite) for name, report in self.reports.items()],
            key=lambda x: x[1],
            reverse=True,
        )

    def get_pairwise_comparison(self) -> List[str]:
        """
        Generate pairwise comparison statements.

        Returns:
            List of comparison strings
        """
        ranking = self.get_ranking()
        lines = []

        for i in range(len(ranking)):
            name_i, val_i = ranking[i]
            for j in range(i + 1, len(ranking)):
                name_j, val_j = ranking[j]
                if val_i == 0:
                    pct = 0.0
                else:
                    pct = (val_i - val_j) / (val_i + 1e-12) * 100.0
                lines.append(f"{name_i} beats {name_j} by {pct:.1f}%")

        return lines

    def to_dict(self) -> Dict:
        """Convert all reports to dictionary format."""
        return {
            name: report.to_dict()
            for name, report in self.reports.items()
        }
