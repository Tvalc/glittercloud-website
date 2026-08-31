#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Remove background white that is SEALED INSIDE a sprite's ink outline.

cutout.py floods in from the border, so any pocket of background fully enclosed
by the drawing is never reached: the gaps between a beetle's legs stayed solid
white and the sprite rendered with white webbing between its feet.

The naive fix - key out every near-white pixel - destroys the art, because the
eyes and the fly's wings are white too. Two measurements separate them:

  TINT      background white is pure (min channel ~250). Painted whites carry a
            tint: the fly's wings measure 234-235. A --pure threshold keeps any
            white the artist actually shaded.
  POSITION  the pockets are under the body, in the leg zone (vertical centre
            0.83-0.86 of the cell). The eyes sit at 0.51. --below protects
            everything in the upper part of the sprite.

A component must fail BOTH tests to be removed, so a tinted highlight low on the
body survives and so does a pure-white eye.

Also clears the 1px white halo left along the alpha edge by the first cutout,
which is what makes a keyed sprite look "cheap" against a dark stage.
"""
import argparse
import numpy as np
from PIL import Image
from scipy import ndimage


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--frames", type=int, default=1,
                    help="cells across the strip; components are judged per cell")
    ap.add_argument("--below", type=float, default=0.72,
                    help="only pockets whose vertical centre is below this "
                         "fraction of cell height may be removed")
    ap.add_argument("--pure", type=int, default=244,
                    help="min-channel mean at or above which a white counts as "
                         "background rather than painted")
    ap.add_argument("--minsize", type=int, default=40)
    ap.add_argument("--no-fringe", action="store_true")
    a = ap.parse_args()

    im = Image.open(a.src).convert("RGBA")
    arr = np.array(im).astype(int)
    h, w = arr.shape[:2]
    rgb, al = arr[:, :, :3], arr[:, :, 3]
    mx, mn = rgb.max(2), rgb.min(2)

    whiteish = (al > 128) & (mn > 222) & ((mx - mn) < 20)
    lab, n = ndimage.label(whiteish)
    cw = max(1, w // a.frames)

    killed = kept = 0
    for idx in range(1, n + 1):
        m = lab == idx
        size = int(m.sum())
        if size < a.minsize:
            continue
        ys, xs = np.where(m)
        ycen = ys.mean() / float(h)
        purity = float(mn[m].mean())
        if ycen > a.below and purity >= a.pure:
            al[m] = 0
            killed += 1
            print("  removed pocket size=%5d ycen=%.2f purity=%.0f cell=%d"
                  % (size, ycen, purity, xs.min() // cw))
        else:
            kept += 1
            why = "tinted" if purity < a.pure else "high on the sprite"
            print("  kept    white  size=%5d ycen=%.2f purity=%.0f  (%s)"
                  % (size, ycen, purity, why))

    if not a.no_fringe:
        # the pale halo the first key leaves along the silhouette
        solid = al > 128
        edge = ndimage.binary_dilation(~solid, iterations=1) & solid
        halo = edge & (mn > 236) & ((mx - mn) < 20)
        al[halo] = 0
        print("  cleared %d halo pixels along the silhouette" % int(halo.sum()))

    arr[:, :, 3] = al
    Image.fromarray(arr.astype("uint8"), "RGBA").save(a.dst)
    print("%s -> %s  (%d pockets removed, %d whites kept)"
          % (a.src, a.dst, killed, kept))


if __name__ == "__main__":
    main()
