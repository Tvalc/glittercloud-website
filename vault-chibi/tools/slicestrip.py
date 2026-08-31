#!/usr/bin/env python
"""Slice a generated sprite-strip plate into evenly-sized animation frames.

THE RULE THIS ENFORCES (session 21, decision 162): every frame in one generated
row shares ONE vertical crop. Trimming each frame to its own bounding box makes
the character bob, because a pose with a raised leg has a different bbox from a
pose without one. The horizontal split is found per frame; the vertical window
is computed once across the whole row and applied to all of them.

  python tools/slicestrip.py in.png out.png --frames 6 [--pad 8]

Writes one wide PNG of N equal cells, which is what a CSS steps() animation or
a canvas drawImage cell-blit wants.
"""
import argparse
import os

import numpy as np
from scipy import ndimage
from PIL import Image


def alpha_of(path, thresh=214, sat_tol=34):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    sat = a.max(axis=2) - a.min(axis=2)
    bg = (a.min(axis=2) >= thresh) & (sat <= sat_tol)
    lab, n = ndimage.label(bg)
    if n:
        edge = set(lab[0, :]) | set(lab[-1, :]) | set(lab[:, 0]) | set(lab[:, -1])
        edge.discard(0)
        outside = np.isin(lab, list(edge)) if edge else np.zeros_like(bg)
    else:
        outside = np.zeros_like(bg)
    return im, ~outside


def bands(mask, n):
    """Find n frame windows from the column profile: the gaps between poses are
    the columns with (almost) no ink in them."""
    col = mask.sum(axis=0)
    on = col > max(2, col.max() * 0.012)
    runs, s = [], None
    for x, v in enumerate(on):
        if v and s is None:
            s = x
        elif not v and s is not None:
            runs.append((s, x))
            s = None
    if s is not None:
        runs.append((s, len(on)))
    runs = [r for r in runs if r[1] - r[0] > mask.shape[1] * 0.012]
    if len(runs) > n:                      # merge the closest neighbours down to n
        while len(runs) > n:
            gaps = [(runs[i + 1][0] - runs[i][1], i) for i in range(len(runs) - 1)]
            _, i = min(gaps)
            runs[i] = (runs[i][0], runs[i + 1][1])
            del runs[i + 1]
    return runs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--frames", type=int, required=True)
    ap.add_argument("--pad", type=int, default=8)
    ap.add_argument("--cellh", type=int, default=0, help="scale each cell to this height")
    a = ap.parse_args()

    im, mask = alpha_of(a.src)
    runs = bands(mask, a.frames)
    if len(runs) != a.frames:
        raise SystemExit("slicestrip: found %d bands, wanted %d (%s)"
                         % (len(runs), a.frames, os.path.basename(a.src)))

    # ONE shared vertical window across every frame
    ys = np.where(mask.any(axis=1))[0]
    y0, y1 = max(0, ys.min() - a.pad), min(mask.shape[0], ys.max() + 1 + a.pad)

    cw = max(r[1] - r[0] for r in runs) + a.pad * 2
    ch = y1 - y0
    rgba = np.dstack([np.asarray(im), (mask * 255).astype(np.uint8)])
    full = Image.fromarray(rgba, "RGBA")

    out = Image.new("RGBA", (cw * a.frames, ch), (0, 0, 0, 0))
    for i, (x0, x1) in enumerate(runs):
        cell = full.crop((x0, y0, x1, y1))
        out.paste(cell, (i * cw + (cw - cell.width) // 2, 0), cell)
    if a.cellh:
        out = out.resize((int(cw * a.frames * a.cellh / ch), a.cellh), Image.LANCZOS)
    d = os.path.dirname(os.path.abspath(a.dst))
    if d and not os.path.isdir(d):
        os.makedirs(d)
    out.save(a.dst)
    print("%s -> %s  %dx%d  (%d cells of %dx%d)"
          % (os.path.basename(a.src), a.dst, out.width, out.height,
             a.frames, out.width // a.frames, out.height))


if __name__ == "__main__":
    main()
