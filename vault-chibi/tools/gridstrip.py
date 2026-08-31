#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Reflow a sprite sheet laid out as a GRID into a single horizontal strip.

Asked for "6 frames in a single row" the generator often returns 3x2 or 4x2
instead, which slicestrip.py cannot read - it only looks for vertical bands and
reports "found 3 bands, wanted 6".

This finds the rows first (horizontal projection), then the cells within each
row (vertical projection), then writes them out left-to-right, top-to-bottom
into one strip. Every cell is placed on ONE shared vertical crop - the union of
all cell extents - so a frame where the body sits high keeps sitting high and
the bob survives into the game, exactly as slicestrip does for a single row.
"""
import argparse
import numpy as np
from PIL import Image


def bands(mask, min_run, gap):
    """Contiguous True runs, merging gaps smaller than `gap`."""
    out, start = [], None
    run_gap = 0
    for i, v in enumerate(mask):
        if v:
            if start is None:
                start = i
            run_gap = 0
        else:
            if start is not None:
                run_gap += 1
                if run_gap >= gap:
                    if i - run_gap - start >= min_run:
                        out.append((start, i - run_gap))
                    start = None
                    run_gap = 0
    if start is not None and len(mask) - start >= min_run:
        out.append((start, len(mask) - 1))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--frames", type=int, required=True)
    ap.add_argument("--cellh", type=int, default=160)
    ap.add_argument("--pad", type=int, default=4)
    a = ap.parse_args()

    im = Image.open(a.src).convert("RGBA")
    arr = np.array(im)
    solid = arr[:, :, 3] > 24
    H, W = solid.shape

    rows = bands(solid.any(1), max(8, H // 24), max(6, H // 40))
    if not rows:
        raise SystemExit("gridstrip: no content rows found")

    cells = []
    for (y0, y1) in rows:
        band = solid[y0:y1 + 1]
        cols = bands(band.any(0), max(8, W // 60), max(6, W // 90))
        for (x0, x1) in cols:
            sub = band[:, x0:x1 + 1]
            ys = np.where(sub.any(1))[0]
            cells.append((x0, y0 + ys.min(), x1, y0 + ys.max()))

    print("gridstrip: %d row(s), %d cell(s) found" % (len(rows), len(cells)))
    if len(cells) < a.frames:
        raise SystemExit("gridstrip: only %d cells, wanted %d" % (len(cells), a.frames))
    cells = cells[:a.frames]

    # ONE shared vertical crop across every cell, so relative height is kept
    top = min(c[1] for c in cells)
    bot = max(c[3] for c in cells)
    wid = max(c[2] - c[0] for c in cells) + a.pad * 2
    hgt = bot - top + a.pad * 2

    scale = float(a.cellh) / hgt
    cw = int(round(wid * scale))
    out = Image.new("RGBA", (cw * a.frames, a.cellh), (0, 0, 0, 0))
    for i, (x0, _, x1, _) in enumerate(cells):
        cx = (x0 + x1) // 2
        left = cx - wid // 2
        cell = im.crop((left, top - a.pad, left + wid, bot + a.pad))
        out.paste(cell.resize((cw, a.cellh), Image.LANCZOS), (i * cw, 0))

    out.save(a.dst)
    print("%s -> %s  %dx%d  (%d cells of %dx%d)"
          % (a.src, a.dst, out.width, out.height, a.frames, cw, a.cellh))


if __name__ == "__main__":
    main()
