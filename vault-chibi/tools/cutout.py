#!/usr/bin/env python
"""Turn a generated plate into a game-ready transparent sprite.

The pipeline session 21 landed on, rewritten so it is not scratchpad-only:

  white-key  ->  flood fill from the border (so white INSIDE the object, like an
                 eye highlight, survives)  ->  drop the ground-shadow ellipse the
                 models draw under everything  ->  keep the largest connected
                 component  ->  tight crop  ->  optional pad to a common baseline

The border flood fill is the part that matters. A plain "white pixels are
transparent" rule eats the highlights out of eyes and metal, which is what makes
a cut-out sprite look chewed.

  python tools/cutout.py in.png out.png [--pad 6] [--shadow] [--keep-all]

Also usable as a contact-sheet builder:

  python tools/cutout.py --sheet out.png a.png b.png c.png ...
"""
import argparse
import os
import sys

import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFont


def largest_component(mask):
    """Keep only the biggest blob of True. Removes the stray fragments a tight
    crop clips in from a neighbouring pose, and any speckle the key leaves."""
    lab, n = ndimage.label(mask)
    if n == 0:
        return mask
    sizes = ndimage.sum(mask, lab, range(1, n + 1))
    return lab == (int(np.argmax(sizes)) + 1)


def border_flood(bg_like):
    """True where background reaches in from the frame edge. Label the
    background and keep every component that touches an edge - which is the
    same answer as a flood fill and runs in one pass."""
    lab, n = ndimage.label(bg_like)
    if n == 0:
        return np.zeros_like(bg_like)
    edge = set(lab[0, :]) | set(lab[-1, :]) | set(lab[:, 0]) | set(lab[:, -1])
    edge.discard(0)
    if not edge:
        return np.zeros_like(bg_like)
    return np.isin(lab, list(edge))


def cut(path, out, pad=6, thresh=214, drop_shadow=True, keep_all=False, trim=True,
        sat_tol=34, open_iters=3):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    g = a.mean(axis=2)
    sat = a.max(axis=2) - a.min(axis=2)

    # "background-like": bright and nearly neutral. The tolerance is loose
    # because the models rarely give pure white - an off-white studio card is
    # normal, and a tight key leaves a haze rectangle around the sprite.
    bg_like = (a.min(axis=2) >= thresh) & (sat <= sat_tol)
    keep = ~border_flood(bg_like)

    if drop_shadow:
        # The ground shadow the models draw under everything. It is DARKER than
        # the background and LIGHTER than the ink line, and it is desaturated -
        # so the window sits between the two. An earlier version only looked at
        # mid-greys (g > 150) and missed the heavy shadows entirely.
        h = keep.shape[0]
        band = np.zeros_like(keep)
        band[int(h * 0.55):, :] = True
        keep = keep & ~((g > 72) & (g < thresh) & (sat <= 30) & band)

    if not keep_all:
        # A shadow touches the sprite at the feet, so it survives as one blob
        # with it. Opening severs those thin bridges, the biggest remaining
        # blob is the body, and dilating back restores the edge the opening
        # ate. Without this the critter came out standing on a black puddle.
        core = ndimage.binary_opening(keep, np.ones((3, 3)), iterations=open_iters)
        if core.any():
            core = largest_component(core)
            grown = ndimage.binary_dilation(core, np.ones((3, 3)), iterations=open_iters + 2)
            keep = keep & grown
        keep = largest_component(keep)
        keep = ndimage.binary_fill_holes(keep) & (keep | ~bg_like)

    if not keep.any():
        raise SystemExit("cutout: nothing survived the key for %s" % path)

    rgba = np.dstack([np.asarray(im), (keep * 255).astype(np.uint8)])
    img = Image.fromarray(rgba, "RGBA")
    if trim:
        ys, xs = np.where(keep)
        box = (max(0, xs.min() - pad), max(0, ys.min() - pad),
               min(img.width, xs.max() + 1 + pad), min(img.height, ys.max() + 1 + pad))
        img = img.crop(box)
    d = os.path.dirname(os.path.abspath(out))
    if d and not os.path.isdir(d):
        os.makedirs(d)
    img.save(out)
    return img.size


def sheet(out, paths, cols=4, cell=340):
    """Local contact sheet, numbered, so a batch can be curated at a glance
    instead of one image at a time."""
    rows = (len(paths) + cols - 1) // cols
    sh = Image.new("RGB", (cols * cell, rows * (cell + 22)), (24, 28, 35))
    dr = ImageDraw.Draw(sh)
    try:
        font = ImageFont.truetype("consola.ttf", 15)
    except Exception:
        font = ImageFont.load_default()
    for i, p in enumerate(paths):
        im = Image.open(p).convert("RGBA")
        im.thumbnail((cell - 10, cell - 10))
        bx = (i % cols) * cell + (cell - im.width) // 2
        by = (i // cols) * (cell + 22) + 20 + (cell - 10 - im.height) // 2
        bg = Image.new("RGBA", im.size, (250, 250, 250, 255))
        bg.alpha_composite(im)
        sh.paste(bg.convert("RGB"), (bx, by))
        dr.text(((i % cols) * cell + 8, (i // cols) * (cell + 22) + 3),
                "%d  %s" % (i + 1, os.path.basename(p)), fill=(230, 200, 130), font=font)
    sh.save(out)
    return sh.size


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("args", nargs="*")
    ap.add_argument("--sheet", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--pad", type=int, default=6)
    ap.add_argument("--thresh", type=int, default=214)
    ap.add_argument("--open", dest="open_iters", type=int, default=3)
    ap.add_argument("--shadow", action="store_true", help="KEEP the ground shadow")
    ap.add_argument("--keep-all", action="store_true", help="skip largest-component")
    ap.add_argument("--no-trim", action="store_true")
    a = ap.parse_args()

    if a.sheet:
        out = a.out or a.args[0]
        paths = a.args if a.out else a.args[1:]
        print("sheet %s  %s" % (out, sheet(out, paths)))
        return
    src, dst = a.args[0], a.args[1]
    size = cut(src, dst, pad=a.pad, thresh=a.thresh, drop_shadow=not a.shadow,
               keep_all=a.keep_all, trim=not a.no_trim, open_iters=a.open_iters)
    print("%s -> %s  %dx%d" % (os.path.basename(src), dst, size[0], size[1]))


if __name__ == "__main__":
    main()
