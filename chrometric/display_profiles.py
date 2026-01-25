"""
chrometric/display_profiles.py - Display Technology SPD Profiles

Display-specific spectral power distribution profiles for accurate
photobiology calculations.

Based on:
- EMPIR 15SIB07 PhotoLED database measurements
- Measured spectra from various display technologies
- CIE TN 011:2020 "What to document and report in studies of ipRGC-
  influenced responses to light"

Different display technologies have vastly different spectral characteristics,
particularly in the blue region, which affects melanopic/circadian calculations.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class PrimarySpec:
    """Specification for a display primary color."""
    center: float  # Peak wavelength (nm)
    fwhm: float    # Full width at half maximum (nm)


@dataclass
class DisplayProfile:
    """
    Display technology profile for spectral calculations.

    Attributes:
        name: Human-readable display type name
        description: Additional details about the technology
        red: Red primary specification
        green: Green primary specification
        blue: Blue primary specification
        blue_peak_ratio: Relative blue peak intensity (0-1)
        has_phosphor: Whether display uses phosphors (affects spectrum shape)
        typical_cct: Typical correlated color temperature when at D65
    """
    name: str
    description: str
    red: PrimarySpec
    green: PrimarySpec
    blue: PrimarySpec
    blue_peak_ratio: float = 0.25
    has_phosphor: bool = False
    typical_cct: int = 6500

    def to_dict(self) -> Dict:
        """Convert to dictionary format for SpectralRecovery."""
        return {
            "red": {"center": self.red.center, "fwhm": self.red.fwhm},
            "green": {"center": self.green.center, "fwhm": self.green.fwhm},
            "blue": {"center": self.blue.center, "fwhm": self.blue.fwhm},
        }


class DisplayProfiles:
    """
    Collection of display technology profiles.

    Each profile defines the spectral characteristics of display primaries,
    enabling accurate photobiology calculations for different screen types.
    """

    # =========================================================================
    # LCD with White LED Backlight (W-LED)
    # Most common display type (laptops, monitors, phones)
    # =========================================================================
    LCD_WLED = DisplayProfile(
        name="LCD with White LED Backlight",
        description=(
            "Standard LCD with phosphor-converted white LED backlight. "
            "Characterized by narrow blue peak (LED emission) and broader "
            "yellow-green region (phosphor emission)."
        ),
        red=PrimarySpec(center=610, fwhm=50),
        green=PrimarySpec(center=550, fwhm=60),
        blue=PrimarySpec(center=450, fwhm=25),  # Narrow blue LED peak
        blue_peak_ratio=0.25,
        has_phosphor=True,
        typical_cct=6500,
    )

    # =========================================================================
    # LCD with RGB LED Backlight
    # Higher color gamut displays, some gaming monitors
    # =========================================================================
    LCD_RGB_LED = DisplayProfile(
        name="LCD with RGB LED Backlight",
        description=(
            "LCD with individual red, green, blue LED backlight. "
            "Wider color gamut than W-LED, narrower primary peaks."
        ),
        red=PrimarySpec(center=625, fwhm=20),
        green=PrimarySpec(center=530, fwhm=35),
        blue=PrimarySpec(center=460, fwhm=25),
        blue_peak_ratio=0.28,
        has_phosphor=False,
        typical_cct=6500,
    )

    # =========================================================================
    # OLED (RGBW or RGB)
    # Premium phones, TVs, some monitors
    # =========================================================================
    OLED = DisplayProfile(
        name="OLED (Organic LED)",
        description=(
            "Organic LED with individual emissive pixels. "
            "Excellent contrast, moderate primary bandwidth. "
            "Blue OLED tends to have shorter lifespan, often slightly less blue."
        ),
        red=PrimarySpec(center=625, fwhm=35),
        green=PrimarySpec(center=530, fwhm=45),
        blue=PrimarySpec(center=460, fwhm=30),
        blue_peak_ratio=0.18,  # Often reduced to extend lifespan
        has_phosphor=False,
        typical_cct=6500,
    )

    # =========================================================================
    # Quantum Dot LCD (QD-LCD / QLED)
    # High-end TVs, some monitors (Samsung QLED, etc.)
    # =========================================================================
    QUANTUM_DOT = DisplayProfile(
        name="Quantum Dot LCD",
        description=(
            "LCD with quantum dot enhancement film. "
            "Very narrow, saturated primaries for wide color gamut. "
            "Blue from LED, red/green from QD phosphors."
        ),
        red=PrimarySpec(center=630, fwhm=25),
        green=PrimarySpec(center=535, fwhm=25),
        blue=PrimarySpec(center=450, fwhm=20),  # Narrow blue from LED
        blue_peak_ratio=0.22,
        has_phosphor=True,
        typical_cct=6500,
    )

    # =========================================================================
    # Mini-LED / Micro-LED
    # High-end displays with local dimming
    # =========================================================================
    MINI_LED = DisplayProfile(
        name="Mini-LED / Micro-LED",
        description=(
            "Advanced LED technology with very small LEDs. "
            "Similar spectral characteristics to standard W-LED but "
            "with better local contrast control."
        ),
        red=PrimarySpec(center=610, fwhm=45),
        green=PrimarySpec(center=550, fwhm=55),
        blue=PrimarySpec(center=450, fwhm=25),
        blue_peak_ratio=0.24,
        has_phosphor=True,
        typical_cct=6500,
    )

    # =========================================================================
    # E-Ink / E-Paper (for reference)
    # No active light emission, uses ambient/front light
    # =========================================================================
    EINK = DisplayProfile(
        name="E-Ink / E-Paper",
        description=(
            "Reflective display technology. No backlight emission. "
            "Spectral characteristics depend on ambient lighting. "
            "Included for reference; use ambient lighting profile instead."
        ),
        red=PrimarySpec(center=600, fwhm=100),
        green=PrimarySpec(center=550, fwhm=100),
        blue=PrimarySpec(center=450, fwhm=100),
        blue_peak_ratio=0.0,  # No blue emission
        has_phosphor=False,
        typical_cct=5500,  # Typically warm/neutral
    )

    # =========================================================================
    # CRT (Legacy Reference)
    # For comparison with historical displays
    # =========================================================================
    CRT = DisplayProfile(
        name="CRT (Cathode Ray Tube)",
        description=(
            "Legacy CRT display technology. "
            "Phosphor-based emission with broad spectra. "
            "Included for historical reference."
        ),
        red=PrimarySpec(center=620, fwhm=60),
        green=PrimarySpec(center=530, fwhm=70),
        blue=PrimarySpec(center=465, fwhm=50),
        blue_peak_ratio=0.20,
        has_phosphor=True,
        typical_cct=6500,
    )

    # =========================================================================
    # Night Mode / Warm Display Setting
    # Simulates reduced blue light from Night Shift, f.lux, etc.
    # =========================================================================
    NIGHT_MODE = DisplayProfile(
        name="Night Mode (Reduced Blue)",
        description=(
            "Simulates display with night mode / blue light filter enabled. "
            "Reduced blue peak, shifted toward warmer color temperature."
        ),
        red=PrimarySpec(center=610, fwhm=50),
        green=PrimarySpec(center=555, fwhm=55),
        blue=PrimarySpec(center=470, fwhm=40),  # Shifted and broadened
        blue_peak_ratio=0.10,  # Significantly reduced
        has_phosphor=True,
        typical_cct=4500,  # Warmer
    )

    # =========================================================================
    # Profile Selection
    # =========================================================================
    ALL_PROFILES: Dict[str, DisplayProfile] = {
        "lcd_wled": LCD_WLED,
        "lcd_rgb": LCD_RGB_LED,
        "oled": OLED,
        "quantum_dot": QUANTUM_DOT,
        "mini_led": MINI_LED,
        "eink": EINK,
        "crt": CRT,
        "night_mode": NIGHT_MODE,
    }

    # Default profile (most common display type)
    DEFAULT = "lcd_wled"

    @classmethod
    def get(cls, profile_name: str) -> Optional[DisplayProfile]:
        """
        Get a display profile by name.

        Args:
            profile_name: Profile identifier

        Returns:
            DisplayProfile or None if not found
        """
        return cls.ALL_PROFILES.get(profile_name)

    @classmethod
    def get_default(cls) -> DisplayProfile:
        """Get the default display profile."""
        return cls.ALL_PROFILES[cls.DEFAULT]

    @classmethod
    def list_profiles(cls) -> Dict[str, str]:
        """
        List all available profiles with descriptions.

        Returns:
            Dict mapping profile name to description
        """
        return {
            name: profile.name
            for name, profile in cls.ALL_PROFILES.items()
        }


# Convenience function
def get_profile(name: str = None) -> DisplayProfile:
    """
    Get a display profile by name, or the default if not specified.

    Args:
        name: Profile name (optional)

    Returns:
        DisplayProfile
    """
    if name is None:
        return DisplayProfiles.get_default()
    profile = DisplayProfiles.get(name)
    if profile is None:
        return DisplayProfiles.get_default()
    return profile


# Blue light emission characteristics by display type
# Used for quick photobiology estimates without full spectral calculation
BLUE_EMISSION_FACTORS = {
    "lcd_wled": 1.0,       # Reference
    "lcd_rgb": 1.1,        # Slightly higher
    "oled": 0.72,          # Lower blue (lifespan optimization)
    "quantum_dot": 0.88,   # Moderate
    "mini_led": 0.96,      # Similar to W-LED
    "night_mode": 0.40,    # Significantly reduced
    "crt": 0.80,           # Historical reference
}


def get_blue_factor(profile_name: str) -> float:
    """
    Get relative blue emission factor for a display type.

    Args:
        profile_name: Display profile name

    Returns:
        Relative blue emission (1.0 = standard W-LED LCD)
    """
    return BLUE_EMISSION_FACTORS.get(profile_name, 1.0)
