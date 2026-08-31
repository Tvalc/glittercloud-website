#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Cut a chroma-keyed sprite strip out of a generated animation clip.

Makko returns a 4s 24fps 1080p video of the character performing one action on
a flat chroma field. This turns that into the N-cell horizontal strip the game
actually loads.

Three things here are deliberate and were learned the hard way:

ONE SHARED CROP RECTANGLE, in BOTH axes, at fixed absolute pixel coordinates.
The camera is locked, so the body does not translate; every wobble in a frame's
own bounding box is the legs reaching or the body bobbing, which is exactly the
motion we are trying to keep. Re-centring each cell on its own centroid - which
is what you would do for a grid of separate drawings - would cancel the bob and
drag the body sideways to chase the trailing leg. So the crop is computed once,
as the union of every chosen frame, and applied identically to all of them.

DESPILL BEFORE KEYING. The green field lights the subject, so the outline picks
up a green fringe that survives a plain "is this pixel green" test and shows up
as a lime halo over the dark temple. Any pixel whose green exceeds the mean of
its own red and blue is pulled back down to that mean, which removes the cast
without touching colours that are legitimately green - of which this cast, by
construction, has none.

A SOFT ALPHA RAMP, not a binary cut. A hard threshold leaves jagged stair-steps
on every curve at the size these are drawn. Alpha ramps across a band of
chroma-distance instead, so the ink outline keeps its shape.
"""
import argparse
import os
import subprocess
import tempfile

import numpy as np
from PIL import Image


def frames_of(path, out_dir):
    subprocess.check_call(
        ['ffmpeg', '-v', 'error', '-i', path, os.path.join(out_dir, '%03d.png')])
    return sorted(os.path.join(out_dir, f) for f in os.listdir(out_dir))


def keyed(path, key):
    """RGBA array with the chroma field removed and the spill neutralised."""
    a = np.array(Image.open(path).convert('RGB')).astype(np.float32)
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

    if key == 'green':
        dist = g - np.maximum(r, b)          # how far into the field a pixel is
        spill = np.maximum(g - (r + b) * 0.5, 0)
        a[:, :, 1] = g - spill
    else:                                     # blue
        dist = b - np.maximum(r, g)
        spill = np.maximum(b - (r + g) * 0.5, 0)
        a[:, :, 2] = b - spill

    # alpha ramps over the band [LO, HI] of chroma distance rather than cutting
    LO, HI = 18.0, 70.0
    alpha = np.clip((HI - dist) / (HI - LO), 0.0, 1.0) * 255.0

    out = np.zeros(a.shape[:2] + (4,), np.uint8)
    out[:, :, :3] = np.clip(a, 0, 255).astype(np.uint8)
    out[:, :, 3] = alpha.astype(np.uint8)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('dst')
    ap.add_argument('--frames', required=True,
                    help='comma separated 1-based frame numbers, in play order')
    ap.add_argument('--key', default='green', choices=['green', 'blue'])
    ap.add_argument('--cellh', type=int, default=550)
    ap.add_argument('--pad', type=int, default=10)
    ap.add_argument('--alpha', type=int, default=40,
                    help='alpha above which a pixel counts as the subject')
    ap.add_argument('--scaleref', type=int, default=0,
                    help='how many SOURCE pixels map to one cell height. Each '
                         'clip is cropped to its own subject, so a jump - which '
                         'needs a tall crop for the arc - would otherwise be '
                         'scaled down to the same cell height as a run and the '
                         'character would visibly shrink whenever he left the '
                         'ground. Pass the same value for every strip of one '
                         'character and they all come out at one scale. Cells '
                         'are bottom-aligned, so the feet line up too.')
    ap.add_argument('--mirror', action='store_true',
                    help='flip horizontally, to match the cast convention '
                         'that every plate is drawn facing LEFT')
    a = ap.parse_args()

    want = [int(x) for x in a.frames.split(',')]
    tmp = tempfile.mkdtemp()
    fs = frames_of(a.src, tmp)

    cells = [keyed(fs[i - 1], a.key) for i in want]

    # ONE crop, the union of every cell, in absolute pixel coordinates
    x0 = y0 = 10 ** 9
    x1 = y1 = -1
    for c in cells:
        ys, xs = np.where(c[:, :, 3] > a.alpha)
        if not len(ys):
            raise SystemExit('vidstrip: a chosen frame is entirely background')
        x0, x1 = min(x0, xs.min()), max(x1, xs.max())
        y0, y1 = min(y0, ys.min()), max(y1, ys.max())
    x0 = max(0, x0 - a.pad); y0 = max(0, y0 - a.pad)
    x1 = min(cells[0].shape[1] - 1, x1 + a.pad)
    y1 = min(cells[0].shape[0] - 1, y1 + a.pad)

    w, h = x1 - x0 + 1, y1 - y0 + 1
    scale = float(a.cellh) / (a.scaleref if a.scaleref else h)
    cw = int(round(w * scale))
    ch = int(round(h * scale))
    if ch > a.cellh:
        raise SystemExit('vidstrip: crop is %d tall at this scale but the cell '
                         'is only %d - raise --cellh or --scaleref' % (ch, a.cellh))
    top = a.cellh - ch                      # bottom-aligned: the feet line up

    strip = Image.new('RGBA', (cw * len(cells), a.cellh), (0, 0, 0, 0))
    for i, c in enumerate(cells):
        cell = Image.fromarray(c[y0:y1 + 1, x0:x1 + 1], 'RGBA')
        cell = cell.resize((cw, ch), Image.LANCZOS)
        # The renderer flips a plate when the body is moving RIGHT, because
        # every existing plate - the enemies, the air strip, the legacy cast -
        # is drawn facing LEFT. These clips are generated facing right, so they
        # are mirrored here rather than teaching the renderer a second
        # convention: two facing rules in one draw call is precisely the bug
        # that reads as the animation playing backwards.
        if a.mirror:
            cell = cell.transpose(Image.FLIP_LEFT_RIGHT)
        strip.paste(cell, (i * cw, top))

    strip.save(a.dst)
    print('%-24s -> %-28s %4dx%3d  %d cells  crop %dx%d at %d,%d'
          % (os.path.basename(a.src), os.path.basename(a.dst),
             strip.width, strip.height, len(cells), w, h, x0, y0))


if __name__ == '__main__':
    main()
