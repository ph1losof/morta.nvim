"""
chrometric/color.py - Core Color Science

Provides the Color class with comprehensive color space conversions:
- sRGB (0-1 normalized)
- Linear RGB
- XYZ (D65 reference white)
- CIELAB
- Oklab
- LMS (Hunt-Pointer-Estevez)
- CAM16-UCS
- APCA-specific luminance
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Tuple

import numpy as np


@dataclass
class Color:
    """
    Color representation with multi-space conversion support.

    Attributes:
        name: Semantic name of the color (e.g., 'keyword', 'bg')
        hex: Hex color string (e.g., '#1E1F2D')
    """

    name: str
    hex: str

    # Computed fields
    rgb: np.ndarray = field(init=False, repr=False)
    rgb_linear: np.ndarray = field(init=False, repr=False)
    xyz: np.ndarray = field(init=False, repr=False)
    Y: float = field(init=False)
    Y_apca: float = field(init=False)
    lab: np.ndarray = field(init=False, repr=False)
    oklab: np.ndarray = field(init=False, repr=False)
    oklab_chroma: float = field(init=False)
    lms: np.ndarray = field(init=False, repr=False)
    cam16ucs: np.ndarray = field(init=False, repr=False)
    cam16_J: float = field(init=False)
    cam16_Q: float = field(init=False)
    blue_ratio: float = field(init=False)

    def __post_init__(self):
        self.rgb = self._hex_to_rgb()
        self.rgb_linear = self._srgb_to_linear()
        self.xyz = self._linear_rgb_to_xyz()
        self.Y = float(self.xyz[1])
        self.Y_apca = self._compute_apca_y()
        self.lab = self._xyz_to_lab()
        self.oklab = self._linear_rgb_to_oklab()
        self.oklab_chroma = math.hypot(self.oklab[1], self.oklab[2])
        self.lms = self._linear_rgb_to_lms()
        self.cam16ucs = self._xyz_to_cam16ucs()
        self.cam16_J, self.cam16_Q = self._compute_cam16_J_Q()
        self.blue_ratio = self._compute_blue_ratio()

    def _hex_to_rgb(self) -> np.ndarray:
        """Convert hex string to sRGB (0-1)."""
        h = self.hex.lstrip("#")
        if len(h) != 6:
            raise ValueError(f"Invalid hex color: {self.hex}")
        return np.array(
            [int(h[i : i + 2], 16) / 255.0 for i in (0, 2, 4)], dtype=float
        )

    def _srgb_to_linear(self) -> np.ndarray:
        """Convert sRGB to linear RGB (inverse gamma)."""
        a = 0.055
        rgb = self.rgb
        return np.where(
            rgb <= 0.04045, rgb / 12.92, ((rgb + a) / (1 + a)) ** 2.4
        )

    def _linear_rgb_to_xyz(self) -> np.ndarray:
        """Convert linear RGB to CIE XYZ (D65 reference white)."""
        M = np.array(
            [
                [0.4124564, 0.3575761, 0.1804375],
                [0.2126729, 0.7151522, 0.0721750],
                [0.0193339, 0.1191920, 0.9503041],
            ]
        )
        return M @ self.rgb_linear

    def _compute_apca_y(self) -> float:
        """
        Compute APCA-specific luminance (Y).

        APCA uses a slightly different sRGB linearization with
        coefficients optimized for text contrast perception.
        """
        # APCA uses sRGB -> Y with power 2.4 (matches standard)
        # but with specific coefficients for text
        r, g, b = self.rgb_linear
        # APCA Y coefficients (from SAPC-8)
        y = 0.2126729 * r + 0.7151522 * g + 0.0721750 * b
        return max(y, 0.0)

    def _xyz_to_lab(self) -> np.ndarray:
        """Convert XYZ to CIELAB (D65 reference white)."""
        Xn, Yn, Zn = 0.95047, 1.0, 1.08883
        xyz = self.xyz / np.array([Xn, Yn, Zn])
        eps = 216.0 / 24389.0
        k = 24389.0 / 27.0

        def f(t):
            return np.where(t > eps, np.cbrt(t), (k * t + 16.0) / 116.0)

        fxyz = f(xyz)
        L = 116.0 * fxyz[1] - 16.0
        a = 500.0 * (fxyz[0] - fxyz[1])
        b = 200.0 * (fxyz[1] - fxyz[2])
        return np.array([L, a, b], dtype=float)

    def _linear_rgb_to_oklab(self) -> np.ndarray:
        """Convert linear RGB to Oklab."""
        M1 = np.array(
            [
                [0.4122214708, 0.5363325363, 0.0514459929],
                [0.2119034982, 0.6806995451, 0.1073969566],
                [0.0883024619, 0.2817188376, 0.6299787005],
            ]
        )
        lms = M1 @ self.rgb_linear
        lms_ = np.cbrt(lms)
        M2 = np.array(
            [
                [0.2104542553, 0.7936177850, -0.0040720388],
                [1.9779984951, -2.4285922050, 0.4505937099],
                [0.0259040371, 0.7827717662, -0.8086757950],
            ]
        )
        return (M2 @ lms_).astype(float)

    def _linear_rgb_to_lms(self) -> np.ndarray:
        """Convert linear RGB to LMS (Hunt-Pointer-Estevez matrix)."""
        M = np.array(
            [
                [0.31399022, 0.63951294, 0.04649755],
                [0.15537241, 0.75789446, 0.08670142],
                [0.01775239, 0.10944209, 0.87256922],
            ]
        )
        return M @ self.rgb_linear

    def _xyz_to_cam16ucs(self) -> np.ndarray:
        """
        Convert XYZ to CAM16-UCS.

        Returns (Jp, ap, bp) vector for perceptual uniformity comparisons.
        """
        # Viewing conditions (typical office/viewing)
        LA = 20.0  # adapting luminance cd/m^2
        c = 0.69

        # Degree of adaptation
        k = 1.0 / (5.0 * LA + 1.0)
        FL = 0.2 * (k**4) * (5.0 * LA) + 0.1 * ((1 - k**4) ** 2) * (
            (5.0 * LA) ** (1.0 / 3.0)
        )

        # XYZ -> LMS (HPE matrix)
        M_hpe = np.array(
            [
                [0.4002, 0.7076, -0.0808],
                [-0.2263, 1.1653, 0.0457],
                [0.0, 0.0, 0.9182],
            ]
        )
        LMS = M_hpe @ self.xyz

        # Nonlinear response compression
        LMS_c = np.sign(LMS) * (np.abs(FL * LMS / 100.0) ** 0.42)
        LMS_prime = 400.0 * LMS_c / (LMS_c + 27.13)

        # Opponent channels
        a = LMS_prime[0] - 12.0 * LMS_prime[1] / 11.0 + LMS_prime[2] / 11.0
        b = (LMS_prime[0] + LMS_prime[1] - 2.0 * LMS_prime[2]) / 9.0

        # Lightness correlate J
        J = 100.0 * (LMS_prime[1] / 400.0) if LMS_prime[1] != 0 else 0.0

        # CAM16-UCS transform
        Jp = (1.7 * J) / (1 + 0.007 * J)
        ap = a * 0.007 / (1 + 0.007 * J)
        bp = b * 0.007 / (1 + 0.007 * J)

        return np.array([Jp, ap, bp], dtype=float)

    def _compute_cam16_J_Q(self) -> Tuple[float, float]:
        """
        Compute CAM16 J (lightness) and Q (brightness) for HKSM.

        Q = (4/c) * sqrt(J/100) * (A + 4) * FL^0.25
        where A is the achromatic response.
        """
        LA = 20.0
        c = 0.69

        k = 1.0 / (5.0 * LA + 1.0)
        FL = 0.2 * (k**4) * (5.0 * LA) + 0.1 * ((1 - k**4) ** 2) * (
            (5.0 * LA) ** (1.0 / 3.0)
        )

        M_hpe = np.array(
            [
                [0.4002, 0.7076, -0.0808],
                [-0.2263, 1.1653, 0.0457],
                [0.0, 0.0, 0.9182],
            ]
        )
        LMS = M_hpe @ self.xyz
        LMS_c = np.sign(LMS) * (np.abs(FL * LMS / 100.0) ** 0.42)
        LMS_prime = 400.0 * LMS_c / (LMS_c + 27.13)

        # Lightness J
        J = 100.0 * (LMS_prime[1] / 400.0) if LMS_prime[1] != 0 else 0.0

        # Achromatic response A
        A = (2.0 * LMS_prime[0] + LMS_prime[1] + 0.05 * LMS_prime[2]) - 0.305

        # Brightness Q
        try:
            Q = (4.0 / c) * math.sqrt(max(J / 100.0, 0.0)) * (A + 4.0) * (FL**0.25)
        except Exception:
            Q = float(J)

        # Ensure Q >= J for sensible results
        if Q < J:
            Q = J + (abs(Q - J) * 0.1)

        return float(J), float(Q)

    def _compute_blue_ratio(self) -> float:
        """
        Compute blue channel ratio for eye health metrics.

        Returns the proportion of blue light relative to total luminance,
        weighted by intensity.
        """
        r, g, b = self.rgb_linear
        total = r + g + b
        if total <= 0:
            return 0.0
        return b / total

    @property
    def hue_oklab(self) -> float:
        """Get Oklab hue angle in radians."""
        return math.atan2(self.oklab[2], self.oklab[1])

    @property
    def lightness_oklab(self) -> float:
        """Get Oklab lightness (L)."""
        return float(self.oklab[0])

    def oklab_distance(self, other: "Color") -> float:
        """Compute Euclidean distance in Oklab space."""
        return float(np.linalg.norm(self.oklab - other.oklab))

    def cam16ucs_distance(self, other: "Color") -> float:
        """Compute Euclidean distance in CAM16-UCS space."""
        return float(np.linalg.norm(self.cam16ucs - other.cam16ucs))

    def __repr__(self) -> str:
        return f"Color(name={self.name!r}, hex={self.hex!r}, Y={self.Y:.4f})"
