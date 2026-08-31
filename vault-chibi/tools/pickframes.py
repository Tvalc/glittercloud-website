#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Choose which frames of a generated clip become the cells of a sprite strip.

The generator hands back 96 frames of a 4s clip. The game wants six to eight.
Picking them by eye, or by even spacing over the whole clip, both produce
strips with dead cells in them - two frames that look the same read as a hitch
in the cycle no matter how good the source was.

So the choice is made against a measurement: the MINIMUM delta between
CONSECUTIVE cells. Not the mean - the mean is happy to hide one repeated pair
among seven good ones, and that one pair is the hitch you actually see. For a
looping action the wrap from the last cell back to the first is included in
that minimum, because on screen it is a consecutive pair like any other.

Two guards, both of which have caught a bad strip before:

  FACING. A mirrored cell changes most of the pixels, so it scores as enormous
  motion while on screen the character snaps round to face backwards. Every
  cell is compared to cell 0 AND to a mirrored cell 0; if the mirror is closer
  the strip is rejected rather than shipped with a flip in it.

  CAMERA LOCK. If the clip drifted or zoomed, the subject's pixel count and
  bounding box wander, and the resulting "motion" is the camera moving rather
  than the character. Reported so it can be checked before cutting.

Looping actions search for their own period first, by autocorrelation, and then
lay the cells evenly across exactly one cycle. One-shot actions (a jump, a
grab) have no period; they get an even spread across the clip, refined by a
local search that is free to shift each cell a little to dodge a dead pair.
"""
import argparse
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image


def masks_of(path, key, small=(240, 135)):
    tmp = tempfile.mkdtemp()
    subprocess.check_call(
        ['ffmpeg', '-v', 'error', '-i', path, os.path.join(tmp, '%03d.png')])
    fs = sorted(os.path.join(tmp, f) for f in os.listdir(tmp))
    ms, stats = [], []
    for f in fs:
        im = Image.open(f).convert('RGB')
        big = np.array(im).astype(int)
        r, g, b = big[:, :, 0], big[:, :, 1], big[:, :, 2]
        if key == 'green':
            sub = ~((g > 120) & (g - r > 60) & (g - b > 60))
        else:
            sub = ~((b > 120) & (b - r > 60) & (b - g > 60))
        ys, xs = np.where(sub)
        stats.append((sub.sum(), xs.min(), xs.max(), ys.min(), ys.max())
                     if len(ys) else (0, 0, 0, 0, 0))
        a = np.array(im.resize(small)).astype(int)
        r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
        ms.append(~((g > 120) & (g - r > 60) & (g - b > 60)) if key == 'green'
                  else ~((b > 120) & (b - r > 60) & (b - g > 60)))
    return np.array(ms), stats


def delta(A, B):
    d = float(A.sum() + B.sum())
    return 0.0 if d == 0 else (A ^ B).sum() / d * 2


def period_of(M):
    """Frame count of one cycle, by the lag with the lowest mean difference."""
    N = len(M)
    best, bestlag = None, None
    for lag in range(5, min(40, N - 4)):
        v = np.mean([delta(M[i], M[i + lag]) for i in range(N - lag)])
        if best is None or v < best:
            best, bestlag = v, lag
    return bestlag


def score(M, idx, loop, ceiling=0.0):
    pairs = list(zip(idx, idx[1:])) + ([(idx[-1], idx[0])] if loop else [])
    ds = [delta(M[i], M[j]) for i, j in pairs]
    if ceiling and max(ds) > ceiling:
        return -1.0          # a cut in the middle of it disqualifies the whole set
    return min(ds)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('--cells', type=int, required=True)
    ap.add_argument('--loop', action='store_true')
    ap.add_argument('--minperiod', type=int, default=0,
                    help='floor on the cycle length, in frames. Autocorrelation '
                         'finds the SHORTEST repeat, which for a held pose is '
                         'the fast little tremor sitting on top of the slow '
                         'action - lock onto that and the cells sample ten '
                         'frames of nothing while the big swell underneath is '
                         'missed entirely. Set this to the length of the motion '
                         'you actually want to see.')
    ap.add_argument('--key', default='green', choices=['green', 'blue'])
    ap.add_argument('--maxdelta', type=float, default=0.0,
                    help='ceiling on the delta between consecutive cells, 0..1. '
                         'The floor stops a slideshow; this stops the opposite '
                         'failure, which looks just as broken and which a floor '
                         'alone will happily select for: a pair so different '
                         'that it reads as a CUT rather than as motion. It is '
                         'usually the loop wrap that trips it - two cells that '
                         'each follow their neighbour fine and then snap when '
                         'the cycle comes round.')
    ap.add_argument('--sizeband', type=float, default=0.0,
                    help='reject frames whose silhouette area is further than '
                         'this fraction from the clip median, 0..1. For an '
                         'action with a jump in it the character genuinely '
                         'changes size between crouch and full stretch, and '
                         'cells picked from both ends of that read as the body '
                         'growing and shrinking rather than as one performance.')
    a = ap.parse_args()

    M, stats = masks_of(a.src, a.key)
    N = len(M)
    px = np.array([s[0] for s in stats], float)
    # frames the size band allows; everything below only ever picks from these
    if a.sizeband:
        med = np.median(px)
        allow = set(i for i in range(N) if abs(px[i] - med) / med <= a.sizeband)
    else:
        allow = set(range(N))
    ws = np.array([s[2] - s[1] for s in stats], float)
    lock = (px.max() - px.min()) / px.mean()

    if a.loop:
        p = period_of(M)
        # A cycle shorter than the cell count cannot fill the strip with
        # distinct frames, and a shake that fast is a jitter rather than an
        # action anyway - so walk up to whole multiples of it until there is
        # room for every cell.
        per0 = p
        while per0 < max(a.cells, a.minperiod):
            per0 += p
        best = None
        lo, hi = max(a.cells, per0 - 1.5), min(N - 2.0, per0 + 1.6)
        for per in np.arange(lo, hi, 0.1):
            step = per / a.cells
            for s in range(0, max(1, N - int(per) - 1)):
                idx = [int(round(s + k * step)) for k in range(a.cells)]
                if idx[-1] >= N or len(set(idx)) < a.cells:
                    continue
                if not all(i in allow for i in idx):
                    continue
                v = score(M, idx, True, a.maxdelta)
                if best is None or v > best[0]:
                    best = (v, idx)
        if best is None:
            raise SystemExit('pickframes: %s has no cycle long enough for %d '
                             'distinct cells (period %d) - regenerate it'
                             % (os.path.basename(a.src), a.cells, p))
        sc, idx = best
        p = per0
    else:
        # even spread, then let each cell drift a little to dodge a dead pair
        span = N - 1
        idx = [int(round(k * span / (a.cells - 1.0))) for k in range(a.cells)]
        sc = score(M, idx, False, a.maxdelta)
        for _ in range(400):
            improved = False
            for k in range(a.cells):
                for dlt in (-3, -2, -1, 1, 2, 3):
                    cand = list(idx)
                    cand[k] = min(N - 1, max(0, cand[k] + dlt))
                    if len(set(cand)) < a.cells or cand != sorted(cand):
                        continue
                    if not all(i in allow for i in cand):
                        continue
                    v = score(M, cand, False, a.maxdelta)
                    if v > sc:
                        sc, idx, improved = v, cand, True
            if not improved:
                break
        p = None

    ref, refm = M[idx[0]], M[idx[0]][:, ::-1]
    flips = [i for i in idx if delta(M[i], ref) > delta(M[i], refm)]

    print('%-22s %d frames, %d cells%s'
          % (os.path.basename(a.src), N, a.cells, '  (loop)' if a.loop else ''))
    print('  camera lock : pixel-count spread %.1f%%  %s'
          % (lock * 100, 'OK' if lock < 0.25 else 'DRIFT - CHECK THIS'))
    print('  stride      : width swings %d..%d px%s'
          % (ws.min(), ws.max(), ('  period %d frames' % p) if p else ''))
    print('  facing      : %s'
          % ('all cells agree' if not flips else 'MIRRORED CELLS %s' % flips))
    pairs = list(zip(idx, idx[1:])) + ([(idx[-1], idx[0])] if a.loop else [])
    ds = [delta(M[i], M[j]) for i, j in pairs]
    print('  deltas      : %s' % ' '.join('%.0f' % (d * 100) for d in ds))
    print('  MIN consecutive delta %.1f%%  MAX %.1f%%   %s'
          % (sc * 100, max(ds) * 100,
             'good' if sc > 0.20 else 'WEAK - REGENERATE'))
    print('  frames %s' % ','.join(str(i + 1) for i in idx))


if __name__ == '__main__':
    main()
