"""
chrometric/exporters.py - Output Formatters

JSON, Markdown, and Table output formatters for analysis results.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .framework import SchemeReport, ChrometricFramework


class TableExporter:
    """Generate text table output."""

    # Column definitions: (header, width, metric_path, format)
    COLUMNS = [
        ("Scheme", 20, "name", "s"),
        ("Score", 8, "composite", ".1f"),
        ("APCA", 8, "apca.score", ".1f"),
        ("Syntax", 8, "syntax.syntax_score", ".1f"),
        ("Health", 8, "health.health_score", ".1f"),
        ("CVD", 8, "cvd.cvd_score", ".1f"),
        ("Oklab", 8, "perceptual.oklab.mean_delta_e", ".3f"),
        ("CAM16", 8, "perceptual.cam16_ucs.mean_delta_e_cam16", ".3f"),
        ("Harmony", 8, "harmony.harmony.harmony", ".3f"),
        ("HKSM", 8, "harmony.hksm.HKSM_mean", ".1f"),
        ("Temporal", 8, "temporal.temporal_score", ".1f"),
    ]

    @classmethod
    def _get_nested_value(cls, data: Dict, path: str, default="N/A"):
        """Get a nested value from a dict using dot notation."""
        try:
            parts = path.split(".")
            value = data
            for part in parts:
                if isinstance(value, dict):
                    value = value.get(part, default)
                else:
                    return default
            return value
        except Exception:
            return default

    @classmethod
    def generate(cls, reports: Dict[str, "SchemeReport"]) -> str:
        """
        Generate a text table from reports.

        Args:
            reports: Dict mapping scheme names to SchemeReport objects

        Returns:
            Formatted table string
        """
        # Convert reports to dicts
        data = {name: report.to_dict() for name, report in reports.items()}

        # Build header
        headers = [col[0] for col in cls.COLUMNS]
        widths = [col[1] for col in cls.COLUMNS]

        header_line = "  ".join(
            h.ljust(w) for h, w in zip(headers, widths)
        )
        separator = "-" * len(header_line)

        lines = [header_line, separator]

        # Sort by composite score
        sorted_names = sorted(
            data.keys(),
            key=lambda n: data[n].get("composite_score", 0),
            reverse=True,
        )

        for name in sorted_names:
            report = data[name]
            row_values = []

            for header, width, path, fmt in cls.COLUMNS:
                if path == "name":
                    value = name
                elif path == "composite":
                    value = report.get("composite_score", 0)
                else:
                    # Navigate into metrics
                    if path.startswith("metrics."):
                        path = path[8:]
                    value = cls._get_nested_value(
                        report.get("metrics", {}), path
                    )

                # Format value
                if value == "N/A" or value is None:
                    formatted = "N/A"
                elif fmt == "s":
                    formatted = str(value)
                else:
                    try:
                        formatted = f"{float(value):{fmt}}"
                    except (ValueError, TypeError):
                        formatted = str(value)

                row_values.append(formatted.ljust(width))

            lines.append("  ".join(row_values))

        return "\n".join(lines)


class MarkdownExporter:
    """Generate Markdown output."""

    @classmethod
    def generate(
        cls,
        reports: Dict[str, "SchemeReport"],
        include_details: bool = True,
    ) -> str:
        """
        Generate Markdown report.

        Args:
            reports: Dict mapping scheme names to SchemeReport objects
            include_details: Whether to include detailed breakdowns

        Returns:
            Markdown string
        """
        lines = ["# Chrometric Colorscheme Analysis\n"]

        # Summary table
        lines.append("## Summary\n")
        lines.append("| Scheme | Score | APCA | Syntax | Health | CVD | Harmony |")
        lines.append("|--------|-------|------|--------|--------|-----|---------|")

        sorted_reports = sorted(
            reports.items(),
            key=lambda x: x[1].composite,
            reverse=True,
        )

        for name, report in sorted_reports:
            apca = report.apca.get("score", 0)
            syntax = report.syntax.get("syntax_score", 0)
            health = report.health.get("health_score", 0)
            cvd = report.cvd.get("cvd_score", 0)
            harmony = report.harmony.get("harmony", {}).get("harmony", 0)

            lines.append(
                f"| {name} | {report.composite:.1f} | {apca:.1f} | "
                f"{syntax:.1f} | {health:.1f} | {cvd:.1f} | {harmony:.3f} |"
            )

        lines.append("")

        # Detailed breakdowns
        if include_details:
            lines.append("## Detailed Analysis\n")

            for name, report in sorted_reports:
                lines.append(f"### {name}\n")
                lines.append(f"**Composite Score:** {report.composite:.1f}\n")

                # APCA
                if report.apca and "error" not in report.apca:
                    lines.append("#### APCA Contrast")
                    lines.append(f"- Primary Lc: {report.apca.get('primary_lc', 'N/A')}")
                    lines.append(f"- Mean Lc: {report.apca.get('mean_lc', 'N/A')}")
                    lines.append(f"- Score: {report.apca.get('score', 'N/A')}")
                    lines.append("")

                # Syntax
                if report.syntax and "error" not in report.syntax:
                    lines.append("#### Syntax Adjacency")
                    lines.append(f"- Score: {report.syntax.get('syntax_score', 'N/A')}")
                    lines.append(f"- Min Distance: {report.syntax.get('min_distance', 'N/A')}")
                    if report.syntax.get("issues"):
                        lines.append("- Issues:")
                        for issue in report.syntax["issues"]:
                            lines.append(f"  - {issue}")
                    lines.append("")

                # CVD
                if report.cvd and "error" not in report.cvd:
                    lines.append("#### Color Vision Deficiency Safety")
                    lines.append(f"- Score: {report.cvd.get('cvd_score', 'N/A')}")
                    lines.append(f"- Min CLDM: {report.cvd.get('min_cldm', 'N/A')}")
                    lines.append("")

                # Health
                if report.health and "error" not in report.health:
                    lines.append("#### Eye Health")
                    lines.append(f"- Health Score: {report.health.get('health_score', 'N/A')}")
                    blue = report.health.get("blue_light", {})
                    lines.append(f"- Blue Light Index: {blue.get('blue_light_index', 'N/A')}")
                    cognitive = report.health.get("cognitive", {})
                    lines.append(f"- Cognitive Load: {cognitive.get('cognitive_load', 'N/A')}")
                    lines.append("")

                lines.append("---\n")

        return "\n".join(lines)


class JSONExporter:
    """Generate JSON output."""

    @classmethod
    def generate(
        cls,
        reports: Dict[str, "SchemeReport"],
        indent: int = 2,
    ) -> str:
        """
        Generate JSON report.

        Args:
            reports: Dict mapping scheme names to SchemeReport objects
            indent: JSON indentation level

        Returns:
            JSON string
        """
        data = {
            name: report.to_dict()
            for name, report in reports.items()
        }

        return json.dumps(
            data,
            indent=indent,
            default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o),
        )

    @classmethod
    def save(
        cls,
        reports: Dict[str, "SchemeReport"],
        path: Path,
        indent: int = 2,
    ):
        """
        Save JSON report to file.

        Args:
            reports: Dict mapping scheme names to SchemeReport objects
            path: Output file path
            indent: JSON indentation level
        """
        with open(path, "w") as f:
            f.write(cls.generate(reports, indent))


class Exporter:
    """Unified exporter interface."""

    @staticmethod
    def to_table(reports: Dict[str, "SchemeReport"]) -> str:
        """Generate text table."""
        return TableExporter.generate(reports)

    @staticmethod
    def to_markdown(
        reports: Dict[str, "SchemeReport"],
        include_details: bool = True,
    ) -> str:
        """Generate Markdown report."""
        return MarkdownExporter.generate(reports, include_details)

    @staticmethod
    def to_json(
        reports: Dict[str, "SchemeReport"],
        indent: int = 2,
    ) -> str:
        """Generate JSON report."""
        return JSONExporter.generate(reports, indent)

    @staticmethod
    def save_all(
        reports: Dict[str, "SchemeReport"],
        base_path: Path,
        formats: List[str] = None,
    ):
        """
        Save reports in multiple formats.

        Args:
            reports: Dict mapping scheme names to SchemeReport objects
            base_path: Base path without extension
            formats: List of formats to save ('json', 'md', 'txt')
        """
        if formats is None:
            formats = ["json", "md"]

        base_path = Path(base_path)

        if "json" in formats:
            with open(base_path.with_suffix(".json"), "w") as f:
                f.write(JSONExporter.generate(reports))

        if "md" in formats:
            with open(base_path.with_suffix(".md"), "w") as f:
                f.write(MarkdownExporter.generate(reports))

        if "txt" in formats:
            with open(base_path.with_suffix(".txt"), "w") as f:
                f.write(TableExporter.generate(reports))
