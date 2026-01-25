"""
chrometric/cli.py - Command Line Interface

Usage:
    python -m chrometric chrometric_data.json
    python -m chrometric chrometric_data.json --format markdown
    python -m chrometric chrometric_data.json --output results
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

from .framework import ChrometricFramework
from .exporters import Exporter


def run_lua_export(lua_script: str = "chrometric_export.lua") -> str:
    """
    Run the Lua export script in Neovim.

    Args:
        lua_script: Path to chrometric_export.lua

    Returns:
        Path to the generated JSON file
    """
    if not Path(lua_script).exists():
        raise FileNotFoundError(f"Lua export script not found: {lua_script}")

    output_file = "chrometric_data.json"

    # Remove old output if exists
    if Path(output_file).exists():
        os.remove(output_file)

    print(f"Running Neovim export with {lua_script}...")

    result = subprocess.run(
        ["nvim", "--headless", "-u", lua_script],
        capture_output=True,
        text=True,
        timeout=60,
    )

    if result.stdout:
        print(result.stdout.strip())

    if not Path(output_file).exists():
        if result.stderr:
            print(f"stderr: {result.stderr[:500]}", file=sys.stderr)
        raise RuntimeError(f"Export failed: {output_file} not created")

    return output_file


def main(argv: list = None):
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="chrometric",
        description="Chrometric: Scientific Colorscheme Analysis Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m chrometric chrometric_data.json
  python -m chrometric chrometric_data.json --format markdown
  python -m chrometric --export --format table

Output Formats:
  table     ASCII table (default)
  markdown  Markdown with detailed breakdowns
  json      Full JSON export
        """,
    )

    parser.add_argument(
        "input",
        nargs="?",
        help="JSON file from chrometric_export.lua (or omit with --export)",
    )

    parser.add_argument(
        "--export",
        action="store_true",
        help="Run chrometric_export.lua in Neovim first",
    )

    parser.add_argument(
        "--lua-script",
        default="chrometric_export.lua",
        help="Path to Lua export script (default: chrometric_export.lua)",
    )

    parser.add_argument(
        "-f", "--format",
        choices=["table", "markdown", "json"],
        default="table",
        help="Output format (default: table)",
    )

    parser.add_argument(
        "-o", "--output",
        help="Output file base name (without extension)",
    )

    parser.add_argument(
        "--threshold",
        type=float,
        default=70.0,
        help="Minimum composite score to pass (default: 70.0)",
    )

    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress informational output",
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version="%(prog)s 2.0.0",
    )

    args = parser.parse_args(argv)

    # Determine input file
    input_path = args.input

    if args.export or not input_path:
        try:
            input_path = run_lua_export(args.lua_script)
        except (FileNotFoundError, RuntimeError, subprocess.TimeoutExpired) as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    if not input_path or not Path(input_path).exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        return 1

    # Run analysis
    if not args.quiet:
        print(f"Analyzing {input_path}...")

    try:
        framework = ChrometricFramework(input_path)
        reports = framework.analyze()
    except Exception as e:
        print(f"Error during analysis: {e}", file=sys.stderr)
        return 1

    if not reports:
        print("No valid colorschemes found.", file=sys.stderr)
        return 1

    # Generate output
    if args.format == "table":
        output = Exporter.to_table(reports)
    elif args.format == "markdown":
        output = Exporter.to_markdown(reports)
    elif args.format == "json":
        output = Exporter.to_json(reports)
    else:
        output = Exporter.to_table(reports)

    # Write or print output
    if args.output:
        ext = {"table": ".txt", "markdown": ".md", "json": ".json"}[args.format]
        output_path = Path(args.output).with_suffix(ext)
        with open(output_path, "w") as f:
            f.write(output)
        if not args.quiet:
            print(f"Saved to {output_path}")
    else:
        print()
        print("=" * 80)
        print("Chrometric Colorscheme Analysis")
        print("=" * 80)
        print()
        print(output)

    # Summary
    if not args.quiet:
        print()
        ranking = framework.get_ranking()
        passed = sum(1 for _, score in ranking if score >= args.threshold)
        print(f"Analyzed {len(ranking)} colorschemes, {passed} passed threshold ({args.threshold})")

        # Top 3
        print("\nTop performers:")
        for name, score in ranking[:3]:
            status = "PASS" if score >= args.threshold else "FAIL"
            print(f"  {name}: {score:.1f} [{status}]")

    return 0


def cli():
    """Entry point for console script."""
    sys.exit(main())


if __name__ == "__main__":
    cli()
