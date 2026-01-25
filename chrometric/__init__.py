"""
Chrometric - Scientific Colorscheme Analysis Framework

A modular framework for analyzing colorscheme quality using:
- APCA contrast algorithm (better than WCAG for dark mode)
- Weighted syntax adjacency analysis
- Color vision deficiency safety testing
- Eye health metrics (blue light, cognitive load)
- Perceptual distance metrics (Oklab, CAM16-UCS)
- Temporal stability metrics (JND, TAFD, Drift)
- Palette harmony and HKSM

Usage:
    from chrometric import ChrometricFramework

    framework = ChrometricFramework("chrometric_data.json")
    reports = framework.analyze()

    for name, report in reports.items():
        print(f"{name}: {report.composite:.1f}")

CLI Usage:
    python -m chrometric chrometric_data.json
    python -m chrometric chrometric_data.json --format markdown
"""

__version__ = "2.0.0"

from .color import Color
from .framework import ChrometricFramework, SchemeReport
from .exporters import Exporter, TableExporter, MarkdownExporter, JSONExporter
from .models import (
    APCAModel,
    SyntaxContextModel,
    EyeHealthModel,
    PerceptualModel,
    CVDModel,
    TemporalModel,
    HarmonyModel,
)

__all__ = [
    # Version
    "__version__",

    # Core
    "Color",
    "ChrometricFramework",
    "SchemeReport",

    # Exporters
    "Exporter",
    "TableExporter",
    "MarkdownExporter",
    "JSONExporter",

    # Models
    "APCAModel",
    "SyntaxContextModel",
    "EyeHealthModel",
    "PerceptualModel",
    "CVDModel",
    "TemporalModel",
    "HarmonyModel",
]
