#!/usr/bin/env python
"""Download an OpenArt batch and build a local contact sheet for curation.

  python tools/fetch.py <name> <dir> <url> [<url> ...]

Writes <dir>/<name>-1.png .. -N.png and <dir>/<name>-SHEET.png. Curating from a
local sheet rather than one image at a time is what session 21 recorded as the
thing that makes best-of-8 actually work.
"""
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cutout import sheet  # noqa: E402


def main():
    name, outdir = sys.argv[1], sys.argv[2]
    urls = sys.argv[3:]
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    paths = []
    for i, u in enumerate(urls, 1):
        p = os.path.join(outdir, "%s-%d.png" % (name, i))
        if not os.path.exists(p):
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=120) as r, open(p, "wb") as f:
                f.write(r.read())
        paths.append(p)
        print("  %s  %d KB" % (os.path.basename(p), os.path.getsize(p) // 1024))
    sp = os.path.join(outdir, "%s-SHEET.png" % name)
    sheet(sp, paths, cols=4, cell=300)
    print("sheet: %s" % sp)


if __name__ == "__main__":
    main()
