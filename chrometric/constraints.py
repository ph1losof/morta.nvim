"""
chrometric/constraints.py - Bounded perceptual constraints

The composite score in framework.py rewards pushing metrics to extremes (more
contrast, less chroma), which produced a palette that scored best and read
worst. This module instead checks each property against a RANGE: a floor below
which a token is hard to read and, where one exists, a ceiling above which it
causes glare or stops standing out from body text.

Usage:
    python -m chrometric.constraints export.json [--profile personal|public]

Thresholds are starting points, not settled science; calibrate them with the
blind comparison in tools/blindtest.lua.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from dataclasses import dataclass
from typing import Callable, Dict, List

import numpy as np

from .color import Color

ACCENTS = ["keyword", "string", "function", "type", "constant", "operator"]
DIAGNOSTICS = ["error", "warning", "info", "hint"]
DIFF_BGS = ["diff_add", "diff_change", "diff_delete"]

# Machado, Oliveira & Fernandes (2009), severity 1.0, applied in linear sRGB.
MACHADO = {
    "protan": np.array(
        [[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]]
    ),
    "deutan": np.array(
        [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]]
    ),
    "tritan": np.array(
        [[1.255528, -0.076749, -0.178779], [-0.078411, 0.930809, 0.147602], [0.004733, 0.691367, 0.303900]]
    ),
}


def apca(text: Color, bg: Color) -> float:
    """APCA 0.0.98G Lc magnitude, including the black soft clamp and offset."""

    def y(c: Color) -> float:
        r, g, b = c.rgb**2.4
        v = 0.2126729 * r + 0.7151522 * g + 0.0721750 * b
        return v if v > 0.022 else v + (0.022 - v) ** 1.414

    yt, yb = y(text), y(bg)
    if yb > yt:
        s = (yb**0.56 - yt**0.57) * 1.14
        return 0.0 if s < 0.1 else (s - 0.027) * 100
    s = (yb**0.65 - yt**0.62) * 1.14
    return 0.0 if s > -0.1 else abs(s + 0.027) * 100


def simulate(c: Color, deficiency: str) -> Color:
    lin = np.clip(MACHADO[deficiency] @ c.rgb_linear, 0, 1)
    srgb = np.where(lin <= 0.0031308, lin * 12.92, 1.055 * lin ** (1 / 2.4) - 0.055)
    return Color(c.name, "#" + "".join(f"{round(float(v) * 255):02x}" for v in srgb))


def de(a: Color, b: Color) -> float:
    return a.oklab_distance(b)


def worst_cvd_de(a: Color, b: Color) -> float:
    return min(de(simulate(a, d), simulate(b, d)) for d in MACHADO)


@dataclass
class Result:
    rule: str
    ok: bool
    hard: bool
    detail: str

    @property
    def status(self) -> str:
        return "PASS" if self.ok else ("FAIL" if self.hard else "WARN")


def check(colors: Dict[str, Color], profile: str = "personal") -> List[Result]:
    c = colors
    bg = c["bg"]
    out: List[Result] = []
    cvd_hard = profile == "public"

    def add(rule: str, ok: bool, detail: str, hard: bool = True):
        out.append(Result(rule, ok, hard, detail))

    def rng(rule: str, value: float, lo: float, hi: float, fmt: str = "{:.0f}", hard: bool = True):
        add(rule, lo <= value <= hi, f"{fmt.format(value)} (want {fmt.format(lo)}-{fmt.format(hi)})", hard)

    # Body text: readable floor, glare ceiling for dark mode in mixed lighting.
    fg_lc = apca(c["fg"], bg)
    rng("text contrast", fg_lc, 75, 90)

    # Accents: APCA floor for non-body content text, never brighter than body text.
    for r in ACCENTS:
        rng(f"{r} contrast", apca(c[r], bg), 60, fg_lc)

    # Accents must read as coloured, not as body text. No study fixes a number for
    # thin glyphs, so 0.10 is the hard floor and 0.15 the target.
    for r in ACCENTS:
        d = de(c[r], c["fg"])
        add(f"{r} vs text", d >= 0.10, f"dE {d:.3f} (floor 0.10)")
        add(f"{r} vs text, target", d >= 0.15, f"dE {d:.3f} (target 0.15)", hard=False)

    pairs = list(itertools.combinations(ACCENTS, 2))
    worst = min(pairs, key=lambda p: de(c[p[0]], c[p[1]]))
    add("accent separation", de(c[worst[0]], c[worst[1]]) >= 0.08,
        f"closest {worst[0]}/{worst[1]} dE {de(c[worst[0]], c[worst[1]]):.3f} (floor 0.08)")
    worst = min(pairs, key=lambda p: worst_cvd_de(c[p[0]], c[p[1]]))
    add("accent separation, CVD", worst_cvd_de(c[worst[0]], c[worst[1]]) >= 0.04,
        f"closest {worst[0]}/{worst[1]} dE {worst_cvd_de(c[worst[0]], c[worst[1]]):.3f} (floor 0.04)", cvd_hard)

    # Comments recede: readable, but dimmer than every accent.
    cm = apca(c["comment"], bg)
    rng("comment contrast", cm, 45, 60)
    dimmest = min(apca(c[r], bg) for r in ACCENTS)
    add("comment below accents", cm < dimmest, f"comment Lc {cm:.0f} vs dimmest accent {dimmest:.0f}")

    # Diagnostics: salience follows severity, and error must not read as a keyword.
    # sRGB cannot make a red both bright and saturated on a dark background, so
    # error leads on chroma (a red's salience) and the rest step down in lightness.
    chroma = {d: c[d].oklab_chroma for d in DIAGNOSTICS}
    add("error most saturated", chroma["error"] == max(chroma.values()),
        ", ".join(f"{d} {v:.3f}" for d, v in chroma.items()))
    lcs = [apca(c[d], bg) for d in DIAGNOSTICS[1:]]
    add("diagnostic order", all(a > b for a, b in zip(lcs, lcs[1:])),
        " > ".join(f"{d} {v:.0f}" for d, v in zip(DIAGNOSTICS[1:], lcs)) + " (want descending)")
    for d in DIAGNOSTICS:
        rng(f"{d} contrast", apca(c[d], bg), 60, fg_lc)
    near = min(ACCENTS, key=lambda r: de(c["error"], c[r]))
    add("error vs syntax", de(c["error"], c[near]) >= 0.08, f"nearest {near} dE {de(c['error'], c[near]):.3f} (floor 0.08)")
    add("info vs hint", de(c["info"], c["hint"]) >= 0.05, f"dE {de(c['info'], c['hint']):.3f} (floor 0.05)")

    # Diff backgrounds: tellable apart, and body text stays readable on them.
    for a, b in itertools.combinations(DIFF_BGS, 2):
        add(f"{a[5:]} vs {b[5:]} bg", de(c[a], c[b]) >= 0.05, f"dE {de(c[a], c[b]):.3f} (floor 0.05)")
        add(f"{a[5:]} vs {b[5:]} bg, CVD", worst_cvd_de(c[a], c[b]) >= 0.03,
            f"dE {worst_cvd_de(c[a], c[b]):.3f} (floor 0.03)", cvd_hard)
    for k in DIFF_BGS + ["visual", "cursor_line", "popup_sel"]:
        lc = apca(c["fg"], c[k])
        add(f"text on {k}", lc >= 75, f"Lc {lc:.0f} (floor 75)")

    # UI layers: each surface separable from the editor background.
    for k in ["cursor_line", "visual", "popup_bg", "status_line"]:
        dl = abs(c[k].lightness_oklab - bg.lightness_oklab)
        add(f"{k} layer", dl >= 0.03, f"dL {dl:.3f} (floor 0.03)")
    add("visual vs cursor_line", de(c["visual"], c["cursor_line"]) >= 0.03,
        f"dE {de(c['visual'], c['cursor_line']):.3f} (floor 0.03)")
    rng("line number contrast", apca(c["line_nr"], bg), 30, cm)

    return out


def load(path: str) -> List[Dict]:
    data = json.load(open(path))
    return data if isinstance(data, list) else [data]


def main(argv: List[str] = None) -> int:
    p = argparse.ArgumentParser(prog="chrometric.constraints")
    p.add_argument("input", help="JSON from chrometric_export.lua (one scheme or a list)")
    p.add_argument("--profile", choices=["personal", "public"], default="personal",
                   help="public makes colour-vision-deficiency rules hard failures")
    args = p.parse_args(argv)

    failed = False
    for scheme in load(args.input):
        colors = {k: Color(k, v) for k, v in scheme["colors"].items()}
        results = check(colors, args.profile)
        print(f"\n{scheme['name']}")
        for r in results:
            print(f"  {r.status:4}  {r.rule:28} {r.detail}")
        n = {s: sum(r.status == s for r in results) for s in ("PASS", "WARN", "FAIL")}
        print(f"  -- {n['PASS']} pass, {n['WARN']} warn, {n['FAIL']} fail")
        failed |= n["FAIL"] > 0
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
