#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Key a generated PROP still onto transparency.

Makko's Prop Sprite mode does not hand back an alpha PNG - it hands back the
subject on a flat CHROMA field, and it picks the key colour per subject (a
sandstone door came back on green, the same door open came back on blue). So
props go through the same keying the animation frames do, and for the same
reasons: the field has to be removed, the spill it throws onto the ink outline
has to be neutralised or the sprite wears a coloured halo over the dark temple,
and the cut has to ramp rather than threshold or every curve stair-steps.

This is `vidstrip.keyed` applied to a single image, plus a crop to content, and
it auto-detects which key it is looking at rather than being told.
"""
import argparse

import numpy as np
from PIL import Image


def detect_key(a):
    """green or blue - whichever dominates the border, where the field is."""
    h, w, _ = a.shape
    edge = np.concatenate([a[:6].reshape(-1, 3), a[-6:].reshape(-1, 3),
                           a[:, :6].reshape(-1, 3), a[:, -6:].reshape(-1, 3)])
    m = edge.mean(0)
    return 'green' if m[1] >= m[2] else 'blue'


def key_image(path, key=None, lo=18.0, hi=70.0):
    a = np.array(Image.open(path).convert('RGB')).astype(np.float32)
    if key is None:
        key = detect_key(a)
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    if key == 'green':
        dist = g - np.maximum(r, b)
        a[:, :, 1] = g - np.maximum(g - (r + b) * 0.5, 0)
    else:
        dist = b - np.maximum(r, g)
        a[:, :, 2] = b - np.maximum(b - (r + g) * 0.5, 0)
    alpha = np.clip((hi - dist) / (hi - lo), 0.0, 1.0) * 255.0
    out = np.zeros(a.shape[:2] + (4,), np.uint8)
    out[:, :, :3] = np.clip(a, 0, 255).astype(np.uint8)
    out[:, :, 3] = alpha.astype(np.uint8)
    return out, key


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('dst')
    ap.add_argument('--key', default=None, choices=['green', 'blue'])
    ap.add_argument('--pad', type=int, default=4)
    ap.add_argument('--height', type=int, default=0,
                    help='scale so the cut-out is this tall; 0 keeps source size')
    ap.add_argument('--alpha', type=int, default=40)
    a = ap.parse_args()

    px, key = key_image(a.src, a.key)
    ys, xs = np.where(px[:, :, 3] > a.alpha)
    if not len(ys):
        raise SystemExit('keyprop: nothing survived the key - wrong colour?')
    y0, y1 = max(0, ys.min() - a.pad), min(px.shape[0] - 1, ys.max() + a.pad)
    x0, x1 = max(0, xs.min() - a.pad), min(px.shape[1] - 1, xs.max() + a.pad)
    im = Image.fromarray(px[y0:y1 + 1, x0:x1 + 1], 'RGBA')
    if a.height:
        im = im.resize((int(round(im.width * a.height / float(im.height))), a.height),
                       Image.LANCZOS)
    im.save(a.dst)

    solid = px[:, :, 3] > 200
    if key == 'green':
        resid = (px[:, :, 1].astype(int) - np.maximum(px[:, :, 0], px[:, :, 2]).astype(int))
    else:
        resid = (px[:, :, 2].astype(int) - np.maximum(px[:, :, 0], px[:, :, 1]).astype(int))
    print('%s -> %s  %dx%d  key=%s  max spill left on opaque px: %d'
          % (a.src.split('/')[-1], a.dst.split('/')[-1], im.width, im.height, key,
             resid[solid].max() if solid.any() else 0))


if __name__ == '__main__':
    main()
