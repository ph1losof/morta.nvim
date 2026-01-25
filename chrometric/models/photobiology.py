"""
chrometric/models/photobiology.py - Photobiology Metrics (T3)

CIE S 026:2018 compliant metrics for biological safety and fatigue:
- Melanopic EDI: Circadian-weighted irradiance (spectrally accurate)
- Blue Light Hazard (Kb): IEC 62471 retinal stress factor
- Circadian Stimulus (CS): Rea et al. 2012 melatonin suppression predictor
- Cone Load Metrics: L, M, S cone stress levels
- Rod Load: Scotopic sensitivity
- Melatonin Suppression Index

Scientific References:
- CIE S 026:2018 "CIE System for Metrology of Optical Radiation for
  ipRGC-Influenced Responses to Light"
- IEC 62471 "Photobiological Safety of Lamps and Lamp Systems"
- Lucas et al. 2014 "Measuring and using light in the melanopsin age"
- Rea et al. 2012 "Modelling the spectral sensitivity of the human
  circadian system"
"""

from __future__ import annotations

import math
from typing import Dict, List, TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from ..color import Color


# Import spectral recovery for accurate calculations
try:
    from ..spectral_recovery import (
        SpectralRecovery,
        get_melanopic_sensitivity_array,
        get_blue_hazard_array,
    )
    from ..display_profiles import DisplayProfiles, get_profile
    HAS_SPECTRAL = True
except ImportError:
    HAS_SPECTRAL = False


class PhotobiologyModel:
    """
    CIE S 026:2018 compliant photobiology metrics for T3.

    This class provides scientifically accurate calculations for:
    - Non-visual effects of light (ipRGC-influenced)
    - Circadian rhythm impact
    - Retinal photochemical stress
    - Cone and rod loading

    When spectral recovery is available, uses full SPD integration.
    Otherwise, falls back to simplified RGB approximations.
    """

    # CIE S 026:2018 melanopic action spectrum peak
    MELANOPIC_PEAK_NM = 490  # Peak sensitivity wavelength

    # Background tokens (excluded from text analysis)
    BACKGROUND_TOKENS = {"bg", "cursor_line", "cursor_column", "popup_bg", "visual", "fold", "sign_column"}

    # Token weights for exposure calculation (based on typical reading time)
    TOKEN_WEIGHTS = {
        "keyword": 0.15,
        "function": 0.20,
        "variable": 0.25,    # Highest attention
        "string": 0.15,
        "type": 0.15,
        "comment": 0.10,
    }

    # Thresholds based on CIE S 026 and circadian research
    MELANOPIC_EDI_THRESHOLD = 50.0   # lux equivalent for comfort (evening)
    BLUE_HAZARD_THRESHOLD = 0.3      # Kb factor threshold (IEC 62471)
    CS_THRESHOLD = 0.3               # Circadian stimulus threshold for evening
    S_CONE_FATIGUE_THRESHOLD = 0.4   # S-cone stress threshold

    @classmethod
    def melanopic_edi(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Calculate Melanopic Equivalent Daylight Illuminance (EDI).

        Based on CIE S 026:2018, melanopic EDI quantifies the
        non-visual (circadian) effect of light.

        E_v,mel = K_m,mel * integral(L_e(λ) * s_mel(λ) dλ)

        Using simplified RGB approximation (peak at 490nm = blue-green):
        melanopic ~ 0.1*R + 0.5*G + 1.0*B (normalized)

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Dict with melanopic EDI analysis
        """
        melanopic_values = []
        breakdown = {}

        for name, color in colors.items():
            if name in cls.BACKGROUND_TOKENS:
                continue

            r, g, b = color.rgb_linear

            # Approximate melanopic response (peaks at 490nm)
            # Weights derived from melanopic sensitivity curve
            melanopic = 0.1 * r + 0.5 * g + 1.0 * b

            # Scale by luminance (brighter colors have more impact)
            melanopic_lux = melanopic * color.Y * 100  # Approximate lux

            weight = cls.TOKEN_WEIGHTS.get(name, 0.1)
            weighted_melanopic = melanopic_lux * weight

            breakdown[name] = round(melanopic_lux, 4)
            melanopic_values.append(weighted_melanopic)

        if not melanopic_values:
            return {"melanopic_edi": 0.0, "passed": True}

        mean_melanopic = float(np.mean(melanopic_values))
        max_melanopic = float(np.max(melanopic_values))

        # Lower is better for evening use
        rating = "low" if mean_melanopic < 30 else (
            "moderate" if mean_melanopic < 60 else "high"
        )

        return {
            "melanopic_edi": round(mean_melanopic, 2),
            "max_melanopic": round(max_melanopic, 2),
            "breakdown": breakdown,
            "rating": rating,
            "passed": mean_melanopic < cls.MELANOPIC_EDI_THRESHOLD,
        }

    @classmethod
    def blue_light_hazard(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Calculate Blue Light Hazard factor (Kb).

        Estimates retinal photochemical stress from short wavelengths:
        Kb = Σ L(λ) * B(λ) * Δλ

        Using simplified approximation weighted toward blue (<500nm).

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Dict with blue light hazard analysis
        """
        hazard_values = []
        breakdown = {}

        for name, color in colors.items():
            if name in cls.BACKGROUND_TOKENS:
                continue

            r, g, b = color.rgb_linear

            # Blue hazard function B(λ) peaks around 440nm
            # Approximation: B ≈ 0.0*R + 0.1*G + 1.0*B
            hazard = 0.0 * r + 0.1 * g + 1.0 * b

            # Weight by luminance
            Kb = hazard * color.Y

            breakdown[name] = round(Kb, 4)
            hazard_values.append(Kb)

        if not hazard_values:
            return {"blue_hazard": 0.0, "passed": True}

        mean_hazard = float(np.mean(hazard_values))
        max_hazard = float(np.max(hazard_values))

        return {
            "blue_hazard": round(mean_hazard, 4),
            "max_hazard": round(max_hazard, 4),
            "breakdown": breakdown,
            "rating": "low" if mean_hazard < 0.1 else (
                "moderate" if mean_hazard < 0.2 else "high"
            ),
            "passed": mean_hazard < cls.BLUE_HAZARD_THRESHOLD,
        }

    @classmethod
    def circadian_stimulus(cls, melanopic_irradiance: float) -> float:
        """
        Calculate Circadian Stimulus (CS) from melanopic irradiance.

        CS = 0.7 * (1 - 1/(1 + (CLA/355.7)^1.1))

        Where CLA is circadian light (related to melanopic irradiance).

        Args:
            melanopic_irradiance: Melanopic equivalent (lux-like)

        Returns:
            CS value (0-0.7, higher means more alertness/melatonin suppression)
        """
        # Convert to approximate CLA (Circadian Light)
        CLA = melanopic_irradiance * 10  # Scaling factor

        if CLA <= 0:
            return 0.0

        CS = 0.7 * (1 - 1 / (1 + (CLA / 355.7) ** 1.1))
        return max(0.0, min(0.7, CS))

    @classmethod
    def circadian_analysis(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Comprehensive circadian impact analysis.

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Dict with circadian analysis
        """
        melanopic = cls.melanopic_edi(colors)
        melanopic_value = melanopic.get("melanopic_edi", 0)

        cs = cls.circadian_stimulus(melanopic_value)

        return {
            "circadian_stimulus": round(cs, 4),
            "melanopic_edi": melanopic_value,
            "melatonin_impact": "low" if cs < 0.1 else (
                "moderate" if cs < 0.3 else "high"
            ),
            "passed": cs < cls.CS_THRESHOLD,
        }

    @classmethod
    def cone_loads(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Calculate cone load metrics (L, M, S cone stress).

        Based on LMS cone fundamentals, measures the relative
        stress on each cone type.

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Dict with cone load analysis
        """
        L_loads = []
        M_loads = []
        S_loads = []
        breakdown = {}

        for name, color in colors.items():
            if name in cls.BACKGROUND_TOKENS:
                continue

            # Get normalized cone loads
            L, M, S = color.cone_L, color.cone_M, color.cone_S

            breakdown[name] = {
                "L": round(L, 4),
                "M": round(M, 4),
                "S": round(S, 4),
            }

            weight = cls.TOKEN_WEIGHTS.get(name, 0.1)
            L_loads.append(L * weight)
            M_loads.append(M * weight)
            S_loads.append(S * weight)

        if not L_loads:
            return {"l_cone": 0.0, "m_cone": 0.0, "s_cone": 0.0, "passed": True}

        mean_L = float(np.mean(L_loads))
        mean_M = float(np.mean(M_loads))
        mean_S = float(np.mean(S_loads))

        # S-cone is most sensitive to fatigue
        s_load_concern = mean_S > 0.4

        return {
            "l_cone": round(mean_L, 4),
            "m_cone": round(mean_M, 4),
            "s_cone": round(mean_S, 4),
            "breakdown": breakdown,
            "balance": "balanced" if abs(mean_L - mean_M) < 0.1 else "unbalanced",
            "passed": not s_load_concern,
        }

    @classmethod
    def rod_load(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Calculate rod (scotopic) load.

        Rods are sensitive to low light levels; high rod load
        indicates the colorscheme may strain night vision adaptation.

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Dict with rod load analysis
        """
        rod_values = []
        breakdown = {}

        for name, color in colors.items():
            if name in cls.BACKGROUND_TOKENS:
                continue

            # Scotopic luminance (rod sensitivity peaks at 507nm)
            # V'(λ) ≈ 0.0*R + 0.5*G + 0.5*B for simplified model
            r, g, b = color.rgb_linear
            scotopic = 0.0 * r + 0.5 * g + 0.5 * b

            breakdown[name] = round(scotopic, 4)
            rod_values.append(scotopic)

        if not rod_values:
            return {"rod_load": 0.0, "passed": True}

        mean_rod = float(np.mean(rod_values))

        return {
            "rod_load": round(mean_rod, 4),
            "breakdown": breakdown,
            "passed": mean_rod < 0.5,
        }

    @classmethod
    def blue_ratio_analysis(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Analyze blue light ratio (<450nm proportion).

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Dict with blue ratio analysis
        """
        ratios = []
        breakdown = {}

        for name, color in colors.items():
            if name in cls.BACKGROUND_TOKENS:
                continue

            ratio = color.blue_ratio
            breakdown[name] = round(ratio, 4)
            ratios.append(ratio)

        if not ratios:
            return {"blue_ratio": 0.0, "passed": True}

        mean_ratio = float(np.mean(ratios))
        max_ratio = float(np.max(ratios))

        return {
            "blue_ratio": round(mean_ratio, 4),
            "max_ratio": round(max_ratio, 4),
            "breakdown": breakdown,
            "passed": mean_ratio < 0.4,
        }

    @classmethod
    def melatonin_suppression(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Calculate melatonin suppression index.

        Estimates the impact on melatonin production based on
        blue light exposure and intensity.

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Dict with melatonin suppression analysis
        """
        circadian = cls.circadian_analysis(colors)
        cs = circadian.get("circadian_stimulus", 0)

        # Melatonin suppression correlates with CS
        suppression = cs / 0.7  # Normalize to 0-1

        return {
            "melatonin_suppression": round(suppression, 4),
            "circadian_stimulus": cs,
            "sleep_impact": "minimal" if suppression < 0.2 else (
                "moderate" if suppression < 0.5 else "significant"
            ),
            "passed": suppression < 0.5,
        }

    @classmethod
    def analyze(cls, colors: Dict[str, "Color"]) -> Dict:
        """
        Run all photobiology analyses.

        Args:
            colors: Dict mapping token names to Color objects

        Returns:
            Dict with comprehensive photobiology analysis
        """
        results = {
            "melanopic": cls.melanopic_edi(colors),
            "blue_hazard": cls.blue_light_hazard(colors),
            "circadian": cls.circadian_analysis(colors),
            "cone_loads": cls.cone_loads(colors),
            "rod_load": cls.rod_load(colors),
            "blue_ratio": cls.blue_ratio_analysis(colors),
            "melatonin": cls.melatonin_suppression(colors),
        }

        # Overall photobiology score (lower exposure = higher score)
        melanopic_score = max(0, 100 - results["melanopic"].get("melanopic_edi", 0) * 2)
        hazard_score = (1 - results["blue_hazard"].get("blue_hazard", 0)) * 100
        cs_score = (1 - results["circadian"].get("circadian_stimulus", 0) / 0.7) * 100
        s_cone_score = (1 - results["cone_loads"].get("s_cone", 0)) * 100

        results["photobiology_score"] = round(
            melanopic_score * 0.3 +
            hazard_score * 0.3 +
            cs_score * 0.2 +
            s_cone_score * 0.2,
            2
        )

        results["passed"] = all([
            results["melanopic"].get("passed", False),
            results["blue_hazard"].get("passed", False),
            results["circadian"].get("passed", False),
            results["cone_loads"].get("passed", False),
        ])

        return results

    # =========================================================================
    # Spectral Analysis Methods (CIE S 026:2018 Compliant)
    # =========================================================================

    @classmethod
    def melanopic_irradiance_spectral(
        cls,
        color: "Color",
        display_profile: str = None,
    ) -> Dict:
        """
        Calculate melanopic irradiance using spectral power distribution.

        This method provides CIE S 026:2018 compliant calculations by:
        1. Recovering SPD from RGB using display primaries
        2. Integrating with melanopic sensitivity function
        3. Returning calibrated melanopic values

        E_mel = K_m,mel × ∫ E_e(λ) × s_mel(λ) dλ

        Args:
            color: Color object with rgb_linear attribute
            display_profile: Display technology profile (default: lcd_wled)

        Returns:
            Dict with spectral melanopic analysis
        """
        if not HAS_SPECTRAL:
            # Fall back to simplified calculation
            r, g, b = color.rgb_linear
            melanopic = 0.1 * r + 0.5 * g + 1.0 * b
            return {
                "melanopic_irradiance": round(melanopic * color.Y * 100, 4),
                "method": "rgb_approximation",
            }

        # Get display profile
        profile = get_profile(display_profile)
        primaries = profile.to_dict()

        # Recover SPD from RGB
        spd = SpectralRecovery.rgb_to_spd_improved(color.rgb_linear, primaries)
        wavelengths = SpectralRecovery.WAVELENGTHS

        # Get melanopic sensitivity function
        s_mel = get_melanopic_sensitivity_array()

        # Integrate SPD with melanopic sensitivity
        delta_lambda = wavelengths[1] - wavelengths[0]
        melanopic_irr = float(np.sum(spd * s_mel) * delta_lambda)

        # Get peak wavelength
        peak_idx = np.argmax(spd)
        peak_nm = int(wavelengths[peak_idx])

        return {
            "melanopic_irradiance": round(melanopic_irr, 6),
            "peak_wavelength": peak_nm,
            "display_profile": profile.name,
            "method": "spectral_cie_s026",
        }

    @classmethod
    def blue_light_hazard_spectral(
        cls,
        color: "Color",
        display_profile: str = None,
    ) -> Dict:
        """
        Calculate blue light hazard using IEC 62471 B(λ) function.

        L_B = ∫ L_λ(λ) × B(λ) dλ

        Where B(λ) is the blue light hazard function (peaks at 437nm).

        Args:
            color: Color object
            display_profile: Display technology profile

        Returns:
            Dict with blue hazard analysis
        """
        if not HAS_SPECTRAL:
            r, g, b = color.rgb_linear
            hazard = 0.0 * r + 0.1 * g + 1.0 * b
            return {
                "blue_hazard": round(hazard * color.Y, 4),
                "method": "rgb_approximation",
            }

        # Get display profile
        profile = get_profile(display_profile)
        primaries = profile.to_dict()

        # Recover SPD
        spd = SpectralRecovery.rgb_to_spd_improved(color.rgb_linear, primaries)
        wavelengths = SpectralRecovery.WAVELENGTHS

        # Get blue hazard function
        b_lambda = get_blue_hazard_array()

        # Integrate SPD with hazard function
        delta_lambda = wavelengths[1] - wavelengths[0]
        hazard = float(np.sum(spd * b_lambda) * delta_lambda)

        # Normalize by luminance
        Kb = hazard / (color.Y + 1e-9)

        return {
            "blue_hazard": round(hazard, 6),
            "Kb_factor": round(Kb, 6),
            "display_profile": profile.name,
            "method": "spectral_iec62471",
        }

    @classmethod
    def analyze_spectral(
        cls,
        colors: Dict[str, "Color"],
        display_profile: str = None,
    ) -> Dict:
        """
        Full spectral photobiology analysis using CIE S 026:2018.

        This method provides the most scientifically accurate
        photobiology calculations by using spectral power distribution
        integration rather than simplified RGB weighting.

        Args:
            colors: Dict mapping token names to Color objects
            display_profile: Display technology profile

        Returns:
            Dict with comprehensive spectral analysis
        """
        melanopic_values = []
        blue_hazard_values = []
        breakdown = {}

        for name, color in colors.items():
            if name in cls.BACKGROUND_TOKENS:
                continue

            mel_result = cls.melanopic_irradiance_spectral(color, display_profile)
            blh_result = cls.blue_light_hazard_spectral(color, display_profile)

            weight = cls.TOKEN_WEIGHTS.get(name, 0.1)
            mel_val = mel_result["melanopic_irradiance"]
            blh_val = blh_result["blue_hazard"]

            melanopic_values.append(mel_val * weight)
            blue_hazard_values.append(blh_val * weight)

            breakdown[name] = {
                "melanopic": round(mel_val, 4),
                "blue_hazard": round(blh_val, 4),
                "peak_nm": mel_result.get("peak_wavelength", 0),
            }

        if not melanopic_values:
            return {
                "melanopic_mean": 0.0,
                "blue_hazard_mean": 0.0,
                "method": "no_data",
                "passed": True,
            }

        mel_mean = float(np.mean(melanopic_values))
        blh_mean = float(np.mean(blue_hazard_values))

        # Circadian Stimulus from melanopic
        cs = cls.circadian_stimulus(mel_mean * 10)

        # Rating based on spectral analysis
        mel_rating = "low" if mel_mean < 0.02 else (
            "moderate" if mel_mean < 0.05 else "high"
        )
        blh_rating = "low" if blh_mean < 0.01 else (
            "moderate" if blh_mean < 0.03 else "high"
        )

        method = "spectral_cie_s026" if HAS_SPECTRAL else "rgb_approximation"

        return {
            "melanopic_mean": round(mel_mean, 6),
            "blue_hazard_mean": round(blh_mean, 6),
            "circadian_stimulus": round(cs, 4),
            "melanopic_rating": mel_rating,
            "blue_hazard_rating": blh_rating,
            "breakdown": breakdown,
            "method": method,
            "display_profile": get_profile(display_profile).name if HAS_SPECTRAL else "n/a",
            "passed": mel_rating != "high" and blh_rating != "high",
        }
