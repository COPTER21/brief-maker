#!/usr/bin/env python3
"""
build_html.py — assemble a self-contained, single-file Thai business document.

Claude writes ONLY the <body> content (using patterns/blocks.md). This script
injects the locked <head>: CI tokens, base.css, and base64-embedded Sarabun.
That guarantees every document shares the exact same pattern & CI.

Usage:
  python build_html.py BODY.html --title "ใบสั่งซื้อ" -o OUT.html
  (BODY.html = a fragment containing one or more <div class="doc-page">...</div>)

The output opens identically in any browser and renders identically to PDF
(no external font / network dependency).
"""
import argparse, base64, pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
SKILL = HERE.parent
FONT_DIR = SKILL / "assets" / "fonts"
CSS_PATH = SKILL / "assets" / "base.css"

# weight/style -> (file, css weight, css style)
FONTS = [
    ("Sarabun-Regular.ttf",  "400", "normal"),
    ("Sarabun-Medium.ttf",   "500", "normal"),
    ("Sarabun-SemiBold.ttf", "600", "normal"),
    ("Sarabun-Bold.ttf",     "700", "normal"),
]


def font_face_block() -> str:
    faces = []
    for fname, weight, style in FONTS:
        p = FONT_DIR / fname
        if not p.exists():
            sys.exit(f"[build_html] missing font: {p}")
        b64 = base64.b64encode(p.read_bytes()).decode()
        faces.append(
            "@font-face{font-family:'Sarabun';"
            f"font-weight:{weight};font-style:{style};font-display:swap;"
            f"src:url(data:font/ttf;base64,{b64}) format('truetype');}}"
        )
    return "\n".join(faces)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("body", help="HTML fragment with .doc-page block(s)")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--title", default="เอกสาร")
    args = ap.parse_args()

    body = pathlib.Path(args.body).read_text(encoding="utf-8")
    css = CSS_PATH.read_text(encoding="utf-8").replace("{{FONT_FACE}}", font_face_block())

    html = f"""<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{args.title}</title>
<style>
{css}
</style>
</head>
<body>
{body}
</body>
</html>
"""
    out = pathlib.Path(args.out)
    out.write_text(html, encoding="utf-8")
    kb = out.stat().st_size / 1024
    print(f"[build_html] wrote {out} ({kb:.0f} KB, fonts embedded)")


if __name__ == "__main__":
    main()
