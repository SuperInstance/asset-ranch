#!/usr/bin/env python3
"""Background-solidity QC for generated assets (the 'clean cutout' criterion).

Ring-based pixel metric: samples a ring 3px inside the image edges and
measures channel stddev + spread. A solid flat background (the style-guide
requirement) has near-zero stddev; textured/scene backgrounds fail.

Thresholds (calibrated on Scrapcraft Harvest 1):
  stddev < 6   -> SOLID    (approved set: 0.4-3.3)
  stddev < 12  -> MARGINAL (eyeball before shipping)
  stddev >= 12 -> TEXTURED (fails clean-cutout; rejected set: 23.6-29.7)

Usage:
  qc-solidity.py <file.png> [file2.png ...]
  qc-solidity.py --dir assets/scrapcraft/prop-icon   # all PNGs in a dir
  qc-solidity.py --strict <files...>                 # exit 1 if any TEXTURED

Small local VLMs (gemma3:4b, llava:7b) over-praise background solidity, so
this pixel metric is the authoritative signal for the background criterion;
use a VLM for the style/silhouette/cleanliness criteria.
"""
import argparse, glob, os, statistics, sys

from PIL import Image

STEP = 16  # sample every 16px along the edges


def ring_stats(path):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    ring = []
    for x in range(0, w, STEP):
        for y in (0, 1, 2, h - 1, h - 2, h - 3):
            ring.append(im.getpixel((x, y)))
    for y in range(0, h, STEP):
        for x in (0, 1, 2, w - 1, w - 2, w - 3):
            ring.append(im.getpixel((x, y)))
    rs = [p[0] for p in ring]
    gs = [p[1] for p in ring]
    bs = [p[2] for p in ring]
    std = max(statistics.pstdev(rs), statistics.pstdev(gs), statistics.pstdev(bs))
    spread = max(max(rs) - min(rs), max(gs) - min(gs), max(bs) - min(bs))
    verdict = "SOLID" if std < 6 else ("MARGINAL" if std < 12 else "TEXTURED")
    return std, spread, verdict


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--dir")
    ap.add_argument("--strict", action="store_true", help="exit 1 if any TEXTURED")
    a = ap.parse_args()

    files = list(a.files)
    if a.dir:
        files += sorted(glob.glob(os.path.join(a.dir, "*.png")))
    if not files:
        ap.error("pass files or --dir")

    bad = 0
    for f in files:
        std, spread, verdict = ring_stats(f)
        flag = "" if verdict == "SOLID" else "  <-- FIX/REJECT"
        if verdict == "TEXTURED":
            bad += 1
        print(f"{os.path.basename(f):28} stddev={std:6.1f} spread={spread:4d}  {verdict}{flag}")
    if a.strict and bad:
        sys.exit(f"{bad} asset(s) fail the solid-background criterion")


if __name__ == "__main__":
    main()
