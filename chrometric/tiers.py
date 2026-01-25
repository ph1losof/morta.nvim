"""
chrometric/tiers.py - AHP Tier-Weighted Scoring System

Implements the 4-tier AHP (Analytic Hierarchy Process) weighted hierarchy
based on Visual Task Performance (VTP) and CIE S 026:2018 photobiology standards.

Tier Weights (Eigenvector-Derived):
- T1: Physiological Readability (0.551) - Prerequisite for all ocular functions
- T2: Cognitive Logic & Semantics (0.247) - Parser efficiency for code comprehension
- T3: Biological Safety & Fatigue (0.144) - Long-term fatigue and melatonin suppression
- T4: Perceptual Polish & Harmony (0.058) - Subconscious "jitter" and satisfaction

Critical Rule: If APCA Lc < 60 (Metric #1), apply 0.5x multiplier (Physiological Veto).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class MetricDefinition:
    """Definition of a single metric in the framework."""

    number: int  # Metric number (1-50)
    name: str  # Short name
    description: str  # Full description
    tier: str  # T1, T2, T3, or T4
    sub_weight: float  # Weight within tier (sums to 1.0 per tier)
    direction: str = "higher"  # "higher" or "lower" for scoring direction
    model_key: str = ""  # Key to extract from model results


class TierSystem:
    """
    AHP-derived tier weighting system for 50-metric framework.

    The system organizes metrics into 4 tiers with eigenvector-derived weights
    based on Visual Task Performance sensitivity analysis.
    """

    # Tier weights (eigenvector-derived from AHP pairwise comparison matrix)
    TIER_WEIGHTS = {
        "T1": 0.551,  # Physiological Readability
        "T2": 0.247,  # Cognitive Logic & Semantics
        "T3": 0.144,  # Biological Safety & Fatigue
        "T4": 0.058,  # Perceptual Polish & Harmony
    }

    # Tier descriptions
    TIER_NAMES = {
        "T1": "Physiological Readability",
        "T2": "Cognitive Logic & Semantics",
        "T3": "Biological Safety & Fatigue",
        "T4": "Perceptual Polish & Harmony",
    }

    # Physiological veto threshold
    APCA_VETO_THRESHOLD = 60.0
    VETO_MULTIPLIER = 0.5

    # Complete 50-metric specification
    METRICS: Dict[int, MetricDefinition] = {}

    @classmethod
    def _init_metrics(cls):
        """Initialize the 50-metric definitions."""
        if cls.METRICS:
            return  # Already initialized

        # T1: Physiological Readability (Tier Weight: 0.551)
        t1_metrics = [
            (1, "APCA_Lc_Dark", "APCA Lc (Dark-Mode)", 0.25, "higher", "apca.lc_dark"),
            (2, "APCA_Lc_Light", "APCA Lc (Light-Mode)", 0.10, "higher", "apca.lc_light"),
            (3, "Weber", "Weber Contrast", 0.10, "higher", "contrast.weber"),
            (4, "Michelson", "Michelson Contrast", 0.08, "higher", "contrast.michelson"),
            (5, "Mesopic_JND", "Mesopic JND", 0.10, "higher", "readability.mesopic_jnd"),
            (6, "Halation", "Halation Risk Index", 0.12, "lower", "readability.halation"),
            (7, "WCAG", "WCAG 2.1 Ratio", 0.05, "higher", "contrast.wcag"),
            (8, "RMS", "RMS Contrast", 0.05, "higher", "contrast.rms"),
            (9, "Pelli_Robson", "Pelli-Robson Sensitivity", 0.10, "higher", "readability.pelli_robson"),
            (10, "Edge_Density", "Edge Density", 0.05, "lower", "readability.edge_density"),
        ]

        # T2: Cognitive Logic & Semantics (Tier Weight: 0.247)
        t2_metrics = [
            (11, "Oklab_DE", "Oklab Delta E", 0.15, "higher", "perceptual.oklab_de"),
            (12, "CAM16_DE", "CAM16-UCS Delta E", 0.10, "higher", "perceptual.cam16_de"),
            (13, "CIEDE2000", "CIEDE2000", 0.05, "higher", "perceptual.ciede2000"),
            (14, "Protan_CLDM", "Protanopia CLDM", 0.10, "higher", "cvd.protan"),
            (15, "Deutan_CLDM", "Deuteranopia CLDM", 0.10, "higher", "cvd.deutan"),
            (16, "Tritan_CLDM", "Tritanopia CLDM", 0.10, "higher", "cvd.tritan"),
            (17, "Semantic_Entropy", "Semantic Entropy", 0.08, "higher", "cognitive.entropy"),
            (18, "Functional_DE", "Functional Delta E", 0.05, "higher", "cognitive.functional_de"),
            (19, "Saliency_Peak", "Visual Saliency Peak", 0.05, "higher", "cognitive.saliency"),
            (20, "Feature_Congestion", "Feature Congestion", 0.05, "lower", "cognitive.congestion"),
            (21, "Subband_Entropy", "Subband Entropy", 0.05, "higher", "cognitive.subband"),
            (22, "Delta_h_CAM16", "Delta Hue (h) CAM16", 0.04, "higher", "perceptual.delta_h"),
            (23, "Delta_C_CAM16", "Delta Chroma (C) CAM16", 0.04, "higher", "perceptual.delta_c"),
            (24, "JND_Small", "Small-Text JND (8pt)", 0.02, "higher", "cognitive.jnd_small"),
            (25, "JND_Large", "Large-Text JND (18pt+)", 0.02, "higher", "cognitive.jnd_large"),
        ]

        # T3: Biological Safety & Fatigue (Tier Weight: 0.144)
        t3_metrics = [
            (26, "Melanopic_EDI", "Melanopic EDI", 0.15, "lower", "photobiology.melanopic_edi"),
            (27, "Blue_Hazard", "Blue Light Hazard (Kb)", 0.15, "lower", "photobiology.blue_hazard"),
            (28, "Circadian_CS", "Circadian Stimulus (CS)", 0.10, "lower", "photobiology.circadian_cs"),
            (29, "TAFD", "TAFD (Flicker Risk)", 0.08, "higher", "temporal.tafd"),
            (30, "Drift", "Drift Index", 0.08, "higher", "temporal.drift"),
            (31, "S_Cone_Load", "S-Cone Load", 0.06, "lower", "photobiology.s_cone"),
            (32, "M_Cone_Load", "M-Cone Load", 0.06, "lower", "photobiology.m_cone"),
            (33, "L_Cone_Load", "L-Cone Load", 0.06, "lower", "photobiology.l_cone"),
            (34, "Rod_Load", "Rod Load (Scotopic)", 0.06, "lower", "photobiology.rod_load"),
            (35, "Pupil_Diameter", "Pupillary Diameter", 0.05, "higher", "spectral.pupil"),
            (36, "Retinal_Illum", "Retinal Illuminance", 0.05, "lower", "spectral.retinal"),
            (37, "Blue_Ratio", "Blue-Light Ratio (<450nm)", 0.04, "lower", "photobiology.blue_ratio"),
            (38, "Melatonin_Supp", "Melatonin Suppression Index", 0.02, "lower", "photobiology.melatonin"),
            (39, "CCT", "CCT (Color Temperature)", 0.02, "lower", "spectral.cct"),
            (40, "Duv", "Duv (Planckian Distance)", 0.02, "lower", "spectral.duv"),
        ]

        # T4: Perceptual Polish & Harmony (Tier Weight: 0.058)
        t4_metrics = [
            (41, "HKSM", "HKSM (HK Stability)", 0.30, "lower", "harmony.hksm"),
            (42, "Moon_Spencer", "Moon-Spencer Harmony", 0.10, "higher", "harmony.moon_spencer"),
            (43, "Opponent_Balance", "Opponent Balance", 0.10, "higher", "harmony.opponent"),
            (44, "Hasler_Colorfulness", "Hasler Colorfulness", 0.10, "higher", "harmony.hasler"),
            (45, "Saturation_Uniformity", "Saturation Uniformity", 0.10, "higher", "harmony.sat_uniformity"),
            (46, "Lum_Histogram", "Luminance Histogram Flatness", 0.05, "higher", "harmony.lum_histogram"),
            (47, "Matsushita", "Matsushita Contrast-Affinity", 0.05, "higher", "harmony.matsushita"),
            (48, "Whiteness", "Whiteness Index (Berger)", 0.05, "higher", "spectral.whiteness"),
            (49, "Yellowness", "Yellowness Index (ASTM E313)", 0.05, "lower", "spectral.yellowness"),
            (50, "Metameric", "Metameric Failure Index", 0.10, "lower", "spectral.metameric"),
        ]

        # Build metrics dictionary
        for tier, metrics in [("T1", t1_metrics), ("T2", t2_metrics),
                              ("T3", t3_metrics), ("T4", t4_metrics)]:
            for num, short, desc, weight, direction, key in metrics:
                cls.METRICS[num] = MetricDefinition(
                    number=num,
                    name=short,
                    description=desc,
                    tier=tier,
                    sub_weight=weight,
                    direction=direction,
                    model_key=key,
                )

    @classmethod
    def get_metric(cls, number: int) -> Optional[MetricDefinition]:
        """Get metric definition by number."""
        cls._init_metrics()
        return cls.METRICS.get(number)

    @classmethod
    def get_tier_metrics(cls, tier: str) -> List[MetricDefinition]:
        """Get all metrics for a given tier."""
        cls._init_metrics()
        return [m for m in cls.METRICS.values() if m.tier == tier]

    @classmethod
    def compute_tier_score(
        cls,
        tier: str,
        metric_values: Dict[int, float],
    ) -> float:
        """
        Compute weighted score for a single tier.

        Args:
            tier: Tier identifier (T1, T2, T3, T4)
            metric_values: Dict mapping metric numbers to normalized values (0-1)

        Returns:
            Weighted tier score (0-1)
        """
        cls._init_metrics()

        tier_metrics = cls.get_tier_metrics(tier)
        if not tier_metrics:
            return 0.0

        total_score = 0.0
        total_weight = 0.0

        for metric in tier_metrics:
            if metric.number in metric_values:
                value = metric_values[metric.number]

                # Invert if lower is better
                if metric.direction == "lower":
                    value = 1.0 - value

                total_score += value * metric.sub_weight
                total_weight += metric.sub_weight

        if total_weight <= 0:
            return 0.0

        # Normalize by total weight to handle missing metrics
        return total_score / total_weight

    @classmethod
    def compute_final_score(
        cls,
        tier_scores: Dict[str, float],
        apca_lc: float = None,
    ) -> Tuple[float, bool]:
        """
        Compute final composite score from tier scores.

        Applies physiological veto if APCA Lc < 60.

        Args:
            tier_scores: Dict mapping tier IDs to tier scores (0-1)
            apca_lc: APCA Lc value for veto check (optional)

        Returns:
            Tuple of (final_score 0-100, veto_applied bool)
        """
        # Compute weighted sum
        final = 0.0
        for tier, weight in cls.TIER_WEIGHTS.items():
            score = tier_scores.get(tier, 0.0)
            final += score * weight

        # Scale to 0-100
        final *= 100.0

        # Apply physiological veto
        veto_applied = False
        if apca_lc is not None and apca_lc < cls.APCA_VETO_THRESHOLD:
            final *= cls.VETO_MULTIPLIER
            veto_applied = True

        return round(final, 2), veto_applied

    @classmethod
    def normalize_metric(
        cls,
        metric_number: int,
        raw_value: float,
        min_val: float = None,
        max_val: float = None,
    ) -> float:
        """
        Normalize a raw metric value to 0-1 range.

        Uses min-max normalization with optional bounds.

        Args:
            metric_number: Metric number for direction lookup
            raw_value: Raw metric value
            min_val: Minimum value for normalization
            max_val: Maximum value for normalization

        Returns:
            Normalized value (0-1)
        """
        metric = cls.get_metric(metric_number)
        if metric is None:
            return 0.0

        # Default bounds based on metric type
        if min_val is None or max_val is None:
            # Use reasonable defaults
            min_val = 0.0 if min_val is None else min_val
            max_val = 100.0 if max_val is None else max_val

        if abs(max_val - min_val) < 1e-9:
            return 0.5

        # Clamp to range
        value = max(min_val, min(max_val, raw_value))

        # Normalize to 0-1
        normalized = (value - min_val) / (max_val - min_val)

        return normalized

    @classmethod
    def get_metric_bounds(cls, metric_number: int) -> Tuple[float, float]:
        """
        Get recommended min/max bounds for a metric.

        Args:
            metric_number: Metric number

        Returns:
            Tuple of (min_value, max_value)
        """
        # Define bounds for each metric type
        BOUNDS = {
            # T1: Readability
            1: (0, 106),  # APCA Lc Dark
            2: (0, 106),  # APCA Lc Light
            3: (-10, 50),  # Weber Contrast
            4: (0, 1),  # Michelson Contrast
            5: (0, 2),  # Mesopic JND
            6: (0, 1),  # Halation Risk (inverted)
            7: (1, 21),  # WCAG Ratio
            8: (0, 0.5),  # RMS Contrast
            9: (0, 3),  # Pelli-Robson LogCS
            10: (0, 1),  # Edge Density (inverted)

            # T2: Cognitive
            11: (0, 0.5),  # Oklab Delta E
            12: (0, 0.2),  # CAM16-UCS Delta E
            13: (0, 50),  # CIEDE2000
            14: (0, 1),  # Protan CLDM
            15: (0, 1),  # Deutan CLDM
            16: (0, 1),  # Tritan CLDM
            17: (0, 4),  # Semantic Entropy (bits)
            18: (0, 50),  # Functional Delta E
            19: (0, 1),  # Saliency Peak
            20: (0, 1),  # Feature Congestion (inverted)
            21: (0, 4),  # Subband Entropy
            22: (0, 180),  # Delta h CAM16
            23: (0, 100),  # Delta C CAM16
            24: (0, 2),  # JND Small Text
            25: (0, 2),  # JND Large Text

            # T3: Biological
            26: (0, 500),  # Melanopic EDI (lux) (inverted)
            27: (0, 1),  # Blue Light Hazard (inverted)
            28: (0, 0.7),  # Circadian Stimulus (inverted)
            29: (0.9, 1),  # TAFD
            30: (0, 1),  # Drift Index
            31: (0, 1),  # S-Cone Load (inverted)
            32: (0, 1),  # M-Cone Load (inverted)
            33: (0, 1),  # L-Cone Load (inverted)
            34: (0, 1),  # Rod Load (inverted)
            35: (2, 8),  # Pupil Diameter (mm)
            36: (0, 1000),  # Retinal Illuminance (Td) (inverted)
            37: (0, 1),  # Blue Ratio (inverted)
            38: (0, 1),  # Melatonin Suppression (inverted)
            39: (2700, 10000),  # CCT (K) (inverted)
            40: (0, 0.05),  # Duv (inverted)

            # T4: Polish
            41: (0, 30),  # HKSM (inverted)
            42: (0, 1),  # Moon-Spencer
            43: (0, 1),  # Opponent Balance
            44: (0, 100),  # Hasler Colorfulness
            45: (0, 1),  # Saturation Uniformity
            46: (0, 1),  # Luminance Histogram Flatness
            47: (0, 1),  # Matsushita Contrast-Affinity
            48: (0, 100),  # Whiteness Index
            49: (0, 50),  # Yellowness Index (inverted)
            50: (0, 10),  # Metameric Failure (inverted)
        }

        return BOUNDS.get(metric_number, (0, 100))


@dataclass
class TierReport:
    """Report for a single tier's analysis."""

    tier: str
    name: str
    weight: float
    score: float
    metrics: Dict[str, float] = field(default_factory=dict)
    passed_count: int = 0
    total_count: int = 0

    @property
    def pass_rate(self) -> float:
        """Percentage of metrics that passed."""
        if self.total_count == 0:
            return 0.0
        return self.passed_count / self.total_count * 100


@dataclass
class FullAnalysisReport:
    """Complete 50-metric analysis report."""

    scheme_name: str
    tier_reports: Dict[str, TierReport] = field(default_factory=dict)
    final_score: float = 0.0
    veto_applied: bool = False
    apca_lc: float = 0.0

    def to_dict(self) -> Dict:
        """Convert to dictionary for export."""
        return {
            "scheme_name": self.scheme_name,
            "final_score": self.final_score,
            "veto_applied": self.veto_applied,
            "apca_lc": self.apca_lc,
            "tiers": {
                tier: {
                    "name": report.name,
                    "weight": report.weight,
                    "score": report.score,
                    "pass_rate": report.pass_rate,
                    "metrics": report.metrics,
                }
                for tier, report in self.tier_reports.items()
            },
        }


# Initialize metrics on module load
TierSystem._init_metrics()
