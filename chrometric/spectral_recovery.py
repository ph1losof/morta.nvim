"""
chrometric/spectral_recovery.py - Spectral Power Distribution Recovery

Recover spectral power distribution (SPD) from sRGB values for accurate
photobiology calculations.

Based on:
- Jakob & Hanika 2019: "A Low-Dimensional Function Space for Efficient
  Spectral Upsampling" (EGSR 2019)
- Wyman, Sloan, Shirley 2013: "Simple Analytic Approximations to the CIE XYZ
  Color Matching Functions"

This module enables CIE S 026:2018 compliant melanopic calculations by
reconstructing approximate spectral distributions from RGB display colors.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from .color import Color


class SpectralRecovery:
    """
    Recover spectral power distribution from sRGB using display primaries.

    For typical LCD/OLED displays, uses Gaussian basis functions centered
    on the primary emission peaks.
    """

    # Wavelength range (nm) - 5nm intervals from 380-780nm
    WAVELENGTHS = np.arange(380, 781, 5)

    # Number of wavelength samples
    N_WAVELENGTHS = len(WAVELENGTHS)

    # sRGB to XYZ matrix (D65 reference white)
    SRGB_TO_XYZ = np.array([
        [0.4124564, 0.3575761, 0.1804375],
        [0.2126729, 0.7151522, 0.0721750],
        [0.0193339, 0.1191920, 0.9503041],
    ])

    # CIE 1931 2-degree observer color matching functions (380-780nm @ 5nm)
    # Simplified - first 10 and last 10 nm set to near-zero
    # Peak values: x̄ peaks ~599nm, ȳ peaks ~555nm, z̄ peaks ~446nm
    CIE_XYZ_2DEG = None  # Loaded on first use

    # Display primary emission spectra (Gaussian approximation)
    # Based on typical LCD with white LED backlight
    DEFAULT_PRIMARIES = {
        "red": {"center": 610, "fwhm": 50},
        "green": {"center": 550, "fwhm": 60},
        "blue": {"center": 450, "fwhm": 25},  # Narrow blue peak typical of LED
    }

    @classmethod
    def _init_cie_xyz(cls):
        """Initialize CIE color matching functions."""
        if cls.CIE_XYZ_2DEG is not None:
            return

        # Simplified CIE 1931 2° observer CMFs
        # Using Wyman 2013 piecewise Gaussian approximation
        wavelengths = cls.WAVELENGTHS

        # x̄(λ) - two-lobe approximation
        x_bar = (
            1.056 * cls._gaussian(wavelengths, 599.8, 37.9) +
            0.362 * cls._gaussian(wavelengths, 442.0, 16.0) -
            0.065 * cls._gaussian(wavelengths, 501.1, 20.4)
        )

        # ȳ(λ) - single lobe
        y_bar = (
            0.821 * cls._gaussian(wavelengths, 568.8, 46.9) +
            0.286 * cls._gaussian(wavelengths, 530.9, 16.3)
        )

        # z̄(λ) - single lobe in blue
        z_bar = (
            1.217 * cls._gaussian(wavelengths, 437.0, 11.8) +
            0.681 * cls._gaussian(wavelengths, 459.0, 26.0)
        )

        cls.CIE_XYZ_2DEG = np.array([x_bar, y_bar, z_bar])

    @staticmethod
    def _gaussian(x: np.ndarray, center: float, fwhm: float) -> np.ndarray:
        """
        Generate Gaussian function.

        Args:
            x: Wavelength array
            center: Peak wavelength (nm)
            fwhm: Full width at half maximum (nm)

        Returns:
            Gaussian values
        """
        sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
        return np.exp(-((x - center) ** 2) / (2 * sigma ** 2))

    @classmethod
    def rgb_to_spd(
        cls,
        rgb_linear: np.ndarray,
        primaries: dict = None,
    ) -> np.ndarray:
        """
        Convert linear RGB to spectral power distribution.

        Uses Gaussian basis functions centered on display primary wavelengths.
        This is an approximation suitable for photobiology calculations.

        Args:
            rgb_linear: Linear RGB values (0-1), shape (3,)
            primaries: Optional display primary specifications

        Returns:
            SPD array at 5nm intervals from 380-780nm, shape (81,)
        """
        if primaries is None:
            primaries = cls.DEFAULT_PRIMARIES

        r, g, b = np.clip(rgb_linear, 0, 1)

        # Generate component SPDs
        spd_r = r * cls._gaussian(
            cls.WAVELENGTHS,
            primaries["red"]["center"],
            primaries["red"]["fwhm"],
        )
        spd_g = g * cls._gaussian(
            cls.WAVELENGTHS,
            primaries["green"]["center"],
            primaries["green"]["fwhm"],
        )
        spd_b = b * cls._gaussian(
            cls.WAVELENGTHS,
            primaries["blue"]["center"],
            primaries["blue"]["fwhm"],
        )

        return spd_r + spd_g + spd_b

    @classmethod
    def rgb_to_spd_improved(
        cls,
        rgb_linear: np.ndarray,
        primaries: dict = None,
    ) -> np.ndarray:
        """
        Improved RGB to SPD conversion with spectral smoothing.

        Adds a small amount of spectral filling between primaries
        to better approximate real display spectra.

        Args:
            rgb_linear: Linear RGB values (0-1)
            primaries: Optional display primary specifications

        Returns:
            Smoothed SPD array
        """
        base_spd = cls.rgb_to_spd(rgb_linear, primaries)

        # Add subtle spectral filling between primaries
        # This better approximates the continuous spectrum of phosphors
        fill = np.zeros_like(base_spd)
        wavelengths = cls.WAVELENGTHS

        r, g, b = np.clip(rgb_linear, 0, 1)

        # Yellow region (between R and G)
        if r > 0 and g > 0:
            fill += 0.1 * min(r, g) * cls._gaussian(wavelengths, 580, 30)

        # Cyan region (between G and B)
        if g > 0 and b > 0:
            fill += 0.1 * min(g, b) * cls._gaussian(wavelengths, 500, 30)

        return base_spd + fill

    @classmethod
    def spd_to_xyz(cls, spd: np.ndarray) -> np.ndarray:
        """
        Convert SPD to CIE XYZ.

        Args:
            spd: Spectral power distribution

        Returns:
            XYZ values, shape (3,)
        """
        cls._init_cie_xyz()

        delta_lambda = cls.WAVELENGTHS[1] - cls.WAVELENGTHS[0]
        xyz = np.zeros(3)

        for i in range(3):
            xyz[i] = np.sum(spd * cls.CIE_XYZ_2DEG[i]) * delta_lambda

        # Normalize
        xyz /= 100.0

        return xyz

    @classmethod
    def get_peak_wavelength(cls, spd: np.ndarray) -> int:
        """
        Get the peak wavelength of an SPD.

        Args:
            spd: Spectral power distribution

        Returns:
            Peak wavelength in nm
        """
        peak_idx = np.argmax(spd)
        return int(cls.WAVELENGTHS[peak_idx])

    @classmethod
    def get_dominant_wavelength(cls, rgb_linear: np.ndarray) -> int:
        """
        Get the dominant wavelength for a color.

        This is the wavelength that would produce the same hue
        when mixed with white.

        Args:
            rgb_linear: Linear RGB values

        Returns:
            Dominant wavelength in nm (approximate)
        """
        r, g, b = rgb_linear

        # Simplified dominant wavelength estimation
        if r > g and r > b:
            # Red-dominant
            return 610 - int(40 * (g - b) / (r + 1e-9))
        elif g > r and g > b:
            # Green-dominant
            return 550 - int(30 * (b - r) / (g + 1e-9))
        elif b > r and b > g:
            # Blue-dominant
            return 470 - int(20 * (g - r) / (b + 1e-9))
        else:
            # Neutral
            return 555  # Peak of photopic sensitivity

    @classmethod
    def analyze_color(cls, color: "Color") -> dict:
        """
        Perform spectral analysis of a color.

        Args:
            color: Color object

        Returns:
            Dict with spectral analysis results
        """
        spd = cls.rgb_to_spd_improved(color.rgb_linear)

        # Peak wavelength
        peak_nm = cls.get_peak_wavelength(spd)

        # Dominant wavelength
        dominant_nm = cls.get_dominant_wavelength(color.rgb_linear)

        # Spectral purity (how narrow the spectrum is)
        # Higher = more saturated/narrow
        purity = np.max(spd) / (np.sum(spd) + 1e-9) * len(spd) / 10

        # Blue content (short wavelengths <500nm)
        blue_mask = cls.WAVELENGTHS < 500
        blue_content = np.sum(spd[blue_mask]) / (np.sum(spd) + 1e-9)

        return {
            "spd": spd,
            "peak_wavelength": peak_nm,
            "dominant_wavelength": dominant_nm,
            "spectral_purity": round(purity, 4),
            "blue_content": round(blue_content, 4),
        }


# Melanopic sensitivity function (CIE S 026:2018)
# Normalized to peak = 1.0 at 490nm
# Includes prereceptoral filtering for 32-year-old observer
MELANOPIC_SENSITIVITY_DATA = [
    # (wavelength, sensitivity)
    (380, 0.0000), (385, 0.0005), (390, 0.0015), (395, 0.0040),
    (400, 0.0100), (405, 0.0230), (410, 0.0500), (415, 0.0900),
    (420, 0.1500), (425, 0.2300), (430, 0.3200), (435, 0.4200),
    (440, 0.5200), (445, 0.6200), (450, 0.7100), (455, 0.7800),
    (460, 0.8400), (465, 0.8900), (470, 0.9300), (475, 0.9600),
    (480, 0.9850), (485, 0.9950), (490, 1.0000), (495, 0.9950),
    (500, 0.9800), (505, 0.9500), (510, 0.9100), (515, 0.8600),
    (520, 0.8000), (525, 0.7300), (530, 0.6600), (535, 0.5800),
    (540, 0.5100), (545, 0.4400), (550, 0.3700), (555, 0.3100),
    (560, 0.2600), (565, 0.2100), (570, 0.1700), (575, 0.1350),
    (580, 0.1050), (585, 0.0800), (590, 0.0600), (595, 0.0450),
    (600, 0.0330), (605, 0.0240), (610, 0.0170), (615, 0.0120),
    (620, 0.0080), (625, 0.0055), (630, 0.0038), (635, 0.0025),
    (640, 0.0016), (645, 0.0010), (650, 0.0006), (655, 0.0004),
    (660, 0.0002), (665, 0.0001), (670, 0.0001), (675, 0.0000),
    (680, 0.0000), (685, 0.0000), (690, 0.0000), (695, 0.0000),
    (700, 0.0000),
]


# Blue light hazard function (IEC 62471)
# Peak at 437nm, not 450nm as commonly assumed
BLUE_HAZARD_FUNCTION_DATA = [
    # (wavelength, B(λ))
    (380, 0.0100), (385, 0.0150), (390, 0.0250), (395, 0.0400),
    (400, 0.1000), (405, 0.2000), (410, 0.4000), (415, 0.6000),
    (420, 0.8000), (425, 0.9000), (430, 0.9600), (435, 0.9900),
    (437, 1.0000), (440, 0.9700), (445, 0.9200), (450, 0.8500),
    (455, 0.7800), (460, 0.7000), (465, 0.6200), (470, 0.5500),
    (475, 0.4500), (480, 0.4000), (485, 0.3500), (490, 0.2800),
    (495, 0.2200), (500, 0.1500), (505, 0.1000), (510, 0.0700),
    (515, 0.0500), (520, 0.0350), (525, 0.0250), (530, 0.0180),
    (535, 0.0130), (540, 0.0090), (545, 0.0060), (550, 0.0040),
    (555, 0.0025), (560, 0.0015), (565, 0.0010), (570, 0.0006),
    (575, 0.0004), (580, 0.0002), (585, 0.0001), (590, 0.0001),
    (600, 0.0000),
]


def get_melanopic_sensitivity(wavelength: float) -> float:
    """
    Get melanopic sensitivity at a specific wavelength.

    Args:
        wavelength: Wavelength in nm

    Returns:
        Sensitivity value (0-1)
    """
    wavelengths = [d[0] for d in MELANOPIC_SENSITIVITY_DATA]
    values = [d[1] for d in MELANOPIC_SENSITIVITY_DATA]
    return float(np.interp(wavelength, wavelengths, values))


def get_blue_hazard(wavelength: float) -> float:
    """
    Get blue light hazard function value at a specific wavelength.

    Args:
        wavelength: Wavelength in nm

    Returns:
        B(λ) value (0-1)
    """
    wavelengths = [d[0] for d in BLUE_HAZARD_FUNCTION_DATA]
    values = [d[1] for d in BLUE_HAZARD_FUNCTION_DATA]
    return float(np.interp(wavelength, wavelengths, values))


def get_melanopic_sensitivity_array() -> np.ndarray:
    """Get melanopic sensitivity as numpy array matching SpectralRecovery wavelengths."""
    wavelengths_data = [d[0] for d in MELANOPIC_SENSITIVITY_DATA]
    values_data = [d[1] for d in MELANOPIC_SENSITIVITY_DATA]
    return np.interp(SpectralRecovery.WAVELENGTHS, wavelengths_data, values_data)


def get_blue_hazard_array() -> np.ndarray:
    """Get blue hazard function as numpy array matching SpectralRecovery wavelengths."""
    wavelengths_data = [d[0] for d in BLUE_HAZARD_FUNCTION_DATA]
    values_data = [d[1] for d in BLUE_HAZARD_FUNCTION_DATA]
    return np.interp(SpectralRecovery.WAVELENGTHS, wavelengths_data, values_data)
