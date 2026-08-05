#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_fonts.py — (re)generate assets/fonts_b64.json by subsetting TTFs to woff2.

Only needed if you want to refresh the embedded fonts. The skill already ships a
prebuilt assets/fonts_b64.json, so you normally do NOT run this.

Requires: fonttools + brotli   (pip install fonttools brotli)

Usage:
  python make_fonts.py --noto NotoSansThai.ttf --inter Inter.ttf --out ../assets/fonts_b64.json
"""
import argparse, base64, json, subprocess, tempfile, pathlib

# Latin + Latin-1 + Thai block + the punctuation/symbols the doc uses
UNICODES = "U+0020-007E,U+00A0-00FF,U+0E00-0E7F,U+2013,U+2014,U+2018-201F,U+2022,U+2026,U+2039,U+203A,U+00B7,U+00D7,U+2713,U+2717,U+2304"

def subset(ttf, out_woff2):
    subprocess.check_call([
        "pyftsubset", ttf, f"--unicodes={UNICODES}",
        "--layout-features=*", "--flavor=woff2", f"--output-file={out_woff2}"
    ])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--noto', required=True)
    ap.add_argument('--inter', required=True)
    ap.add_argument('--out', default='../assets/fonts_b64.json')
    args = ap.parse_args()
    out = {}
    with tempfile.TemporaryDirectory() as d:
        for fam, ttf in [('Noto Sans Thai', args.noto), ('Inter', args.inter)]:
            w = pathlib.Path(d) / (fam.replace(' ', '') + '.woff2')
            subset(ttf, str(w))
            out[fam] = base64.b64encode(w.read_bytes()).decode()
            print(f"{fam}: {w.stat().st_size//1024} KB woff2")
    json.dump(out, open(args.out, 'w'), ensure_ascii=False)
    print("wrote", args.out)

if __name__ == '__main__':
    main()
