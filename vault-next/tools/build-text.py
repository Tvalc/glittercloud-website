#!/usr/bin/env python3
"""Assemble vault-next/text.html — the text pacing build.

The text build must never drift from the graphical build structurally, so
its CONFIG and its entire draw/presentation/scheduler core are SPLICED
VERBATIM out of vault-next/index.html at build time:

  region A: "/* ============ CONFIG"        -> "/* ============ rng & hashing"
  region B: "/* ============ rng & hashing" -> "/* ============ constants & state"

Everything else (the text renderer) lives in the template. Re-run this
script whenever index.html changes:

    python tools/build-text.py [path-to-template]

By default the template is tools/text-template.html.
"""
import sys, pathlib

here = pathlib.Path(__file__).resolve().parent
root = here.parent
index = (root / "index.html").read_text(encoding="utf-8")
template_path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else here / "text-template.html"
template = template_path.read_text(encoding="utf-8")

def region(s, start, end):
    i = s.index(start)
    j = s.index(end, i)
    return s[i:j].rstrip() + "\n"

A = region(index, "/* ============================== CONFIG",
                  "/* ============================== rng & hashing")
B = region(index, "/* ============================== rng & hashing",
                  "/* ============================== constants & state")

assert "/*__A_CONFIG__*/" in template and "/*__B_CORE__*/" in template
out = template.replace("/*__A_CONFIG__*/", A).replace("/*__B_CORE__*/", B)
(root / "text.html").write_text(out, encoding="utf-8")
print("wrote", root / "text.html", "-", len(out), "bytes",
      "(core", len(A) + len(B), "bytes spliced verbatim from index.html)")
