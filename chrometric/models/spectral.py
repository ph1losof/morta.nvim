"""
chrometric/models/spectral.py - Spectral Metrics (T3/T4)

Color temperature and spectral quality metrics:
- CCT (Correlated Color Temperature): McCamy approximation
- Duv (Planckian Distance): Distance from blackbody locus
- Pupillary Diameter: De Groot model
- Retinal Illuminance: Troland calculation
- Whiteness Index (Berger): Background quality
- Yellowness Index (ASTM E313): "Muddy" color detection
- Metameric Failure Index: D65 vs D50 color shift
"""

from __future__ import annotations

import math
from typing import Dict, List, Tuple, TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from ..color import Color


class SpectralModel:
    """
    Spectral quality metrics for T3 (Biological Safety) and T4 (Polish).

    These metrics evaluate the spectral characteristics of colors
    for physiological comfort and perceptual quality.
    """

    # CCT comfort ranges (Kelvin)
    CCT_COMFORTABLE_MIN = 4000  # Warm limit
    CCT_COMFORTABLE_MAX = 6500  # Cool limit

    # Duv threshold (distance from Planckian locus)
    DUV_THRESHOLD = 0.02  # Noticeable color cast

    # Pupil diameter range (mm)
    PUPIL_MIN = 2.0
    PUPIL_MAX = 8.0

    @classmethod
    def cct_mccamy(cls, x: float, y: float) -> float:
        """
        Calculate Correlated Color Temperature using McCamy's approximation.

        CCT = 449n³ + 3525n² + 6823n + 5524
        where n = (x - 0.3320) / (0.1858 - y)

        Args:
            x: CIE 1931 x chromaticity
            y: CIE 1931 y chromaticity

        Returns:
            CCT in Kelvin
        """
        # Avoid division by zero
        if abs(y - 0.1858) < 1e-9:
            y = 0.1858 + 1e-9

        n = (x - 0.3320) / (0.1858 - y)

        cct = 449 * n**3 + 3525 * n**2 + 6823 * n + 5524

        # Clamp to reasonable range
        return max(1000, min(25000, cct))

    @classmethod
    def duv(cls, x: float, y: float) -> float:
        """
        Calculate Duv (distance from Planckian locus).

        Duv indicates how far a color is from the blackbody curve.
        Positive = greenish, Negative = pinkish.

        Args:
            x: CIE 1931 x chromaticity
            y: CIE 1931 y chromaticity

        Returns:
            Duv value (signed distance)
        """
        # Convert to CIE 1960 UCS (u, v)
        denom = -2 * x + 12 * y + 3
        if abs(denom) < 1e-9:
            return 0.0

        u = 4 * x / denom
        v = 6 * y / denom

        # Approximate distance from Planckian locus
        # Using simplified polynomial approximation
        Lfp = math.sqrt((u - 0.292) ** 2 + (v - 0.24) ** 2)

        # Sign based on position relative to locus
        if v > 0.24 + 0.05 * (u - 0.292):
            duv = Lfp  # Above locus (greenish)
        else:
            duv = -Lfp  # Below locus (pinkish)

        return duv

    @classmethod
    def pupillary_diameter(cls, luminance: float) -> float:
        """
        Calculate pupillary diameter using De Groot & Gebhard model.

        log(d) = 0.8558 - 0.000401(log(L) + 8.1)³

        Args:
            luminance: Luminance in cd/m² (Y * typical screen luminance)

        Returns:
            Pupil diameter in mm
        """
        if luminance <= 0:
            return cls.PUPIL_MAX  # Dark adapted

        # Assume typical screen luminance of 200 cd/m²
        L = luminance * 200

        log_L = math.log10(max(L, 0.001))
        log_d = 0.8558 - 0.000401 * (log_L + 8.1) ** 3

        d = 10 ** log_d

        return max(cls.PUPIL_MIN, min(cls.PUPIL_MAX, d))

    @classmethod
    def retinal_illuminance(cls, luminance: float, pupil_diameter: float) -> float:
        """
        Calculate retinal illuminance in Trolands.

        T_d = L × Pupil_Area = L × π × (d/2)²

        Args:
            luminance: Luminance in cd/m²
            pupil_diameter: Pupil diameter in mm

        Returns:
            Retinal illuminance in Trolands
        """
        pupil_area = math.pi * (pupil_diameter / 2) ** 2
        return luminance * pupil_area

    @classmethod
    def whiteness_berger(cls, color: "Color") -> float:
        """
        Calculate Berger Whiteness Index.

        W = Y + 3.108Z - 3.831X

        Higher values indicate "whiter" appearance.

        Args:
            color: Color object

        Returns:
            Whiteness index
        """
        X, Y, Z = color.xyz
        W = Y + 3.108 * Z - 3.831 * X
        return W * 100  # Scale to 0-100 range

    @classmethod
    def yellowness_astm(cls, color: "Color") -> float:
        """
        Calculate Yellowness Index (ASTM E313).

        YI = 100 × (1.2769X - 1.0592Z) / Y

        Higher values indicate more yellow/muddy appearance.

        Args:
            color: Color object

        Returns:
            Yellowness index
        """
        X, Y, Z = color.xyz

        if Y <= 0:
            return 0.0

        YI = 100 * (1.2769 * X - 1.0592 * Z) / Y
        return YI

    @classmethod
    def metameric_failure(cls, color: "Color") -> float:
        """
        Calculate Metameric Failure Index (D65 vs D50).

        Estimates color shift under different illuminants.
        Higher values indicate unstable color appearance.

        Uses simplified chromatic adaptation transform approximation.

        Args:
            color: Color object

        Returns:
            Metameric failure index (0-10 scale)
        """
        # D65 reference (already computed)
        x65, y65 = color.chromaticity_x, color.chromaticity_y

        # Approximate D50 chromaticity via von Kries transform
        # D65 white: x=0.31271, y=0.32902
        # D50 white: x=0.34567, y=0.35850

        # Simplified shift estimation
        dx = 0.34567 - 0.31271  # D50 - D65 x shift
        dy = 0.35850 - 0.32902  # D50 - D65 y shift

        # Estimate color shift
        x50 = x65 + dx * 0.3  # Partial adaptation
        y50 = y65 + dy * 0.3

        # Calculate chromatic difference
        de = math.sqrt((x65 - x50) ** 2 + (y65 - y50) ** 2)

        # Scale to 0-10
        return min(de * 100, 10.0)

    @classmethod
    def analyze_color(cls, color: "Color") -> Dict:
        """
        Analyze spectral properties of a single color.

        Args:
            color: Color object

        Returns:
            Dict with spectral analysis
        """
        x, y = color.chromaticity_x, color.chromaticity_y

        cct = cls.cct_mccamy(x, y)
        duv = cls.duv(x, y)
        pupil = cls.pupillary_diameter(color.Y)
        retinal = cls.retinal_illuminance(color.Y * 200, pupil)
        whiteness = cls.whiteness_berger(color)
        yellowness = cls.yellowness_astm(color)
        metameric = cls.metameric_failure(color)

        return {
            "cct": round(cct, 0),
            "duv": round(duv, 4),
            "pupil_diameter": round(pupil, 2),
            "retinal_illuminance": round(retinal, 2),
            "whiteness": round(whiteness, 2),
            "yellowness": round(yellowness, 2),
            "metameric_failure": round(metameric, 4),
        }

    @classmethod
    def analyze(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Run all spectral analyses.

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Dict with comprehensive spectral analysis
        """
        bg = colors.get("bg")

        results = {
            "background": {},
            "syntax_colors": {},
        }

        # Background analysis (most important for eye comfort)
        if bg:
            bg_analysis = cls.analyze_color(bg)
            results["background"] = bg_analysis

            # Overall background comfort
            cct = bg_analysis["cct"]
            duv = abs(bg_analysis["duv"])
            yellowness = abs(bg_analysis["yellowness"])

            results["cct"] = cct
            results["duv"] = bg_analysis["duv"]
            results["cct_comfort"] = cls.CCT_COMFORTABLE_MIN <= cct <= cls.CCT_COMFORTABLE_MAX
            results["duv_passed"] = duv < cls.DUV_THRESHOLD
            results["yellowness_passed"] = yellowness < 20

        # Syntax color analysis
        syntax_tokens = ["keyword", "string", "function", "type", "variable", "comment"]
        whiteness_values = []
        yellowness_values = []
        metameric_values = []

        for token in syntax_tokens:
            if token in colors:
                analysis = cls.analyze_color(colors[token])
                results["syntax_colors"][token] = analysis
                whiteness_values.append(analysis["whiteness"])
                yellowness_values.append(analysis["yellowness"])
                metameric_values.append(analysis["metameric_failure"])

        if whiteness_values:
            results["mean_whiteness"] = round(float(np.mean(whiteness_values)), 2)
            results["mean_yellowness"] = round(float(np.mean(yellowness_values)), 2)
            results["mean_metameric"] = round(float(np.mean(metameric_values)), 4)
            results["max_metameric"] = round(float(np.max(metameric_values)), 4)

        # Pupil and retinal for overall palette
        if bg:
            results["pupil_diameter"] = bg_analysis["pupil_diameter"]
            results["retinal_illuminance"] = bg_analysis["retinal_illuminance"]

        # Overall spectral score
        cct_score = 100 if results.get("cct_comfort", False) else 50
        duv_score = (1 - min(abs(results.get("duv", 0)) / 0.05, 1)) * 100
        yellowness_score = max(0, 100 - abs(results.get("mean_yellowness", 0)) * 2)
        metameric_score = (1 - results.get("mean_metameric", 0) / 5) * 100

        results["spectral_score"] = round(
            cct_score * 0.25 +
            duv_score * 0.25 +
            yellowness_score * 0.25 +
            metameric_score * 0.25,
            2
        )

        results["passed"] = all([
            results.get("cct_comfort", True),
            results.get("duv_passed", True),
            results.get("yellowness_passed", True),
        ])

        return results
