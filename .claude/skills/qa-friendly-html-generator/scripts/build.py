#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build.py — assemble the final, self-contained QA-friendly test-case HTML.

Merges cases.json (authored by Claude) + shots_b64.json (from capture.py) into one
payload, runs DEDUP, injects fonts + the html2pdf library + the payload into the
template, and writes a single HTML file the tester can open offline.

DEDUP (two passes):
  1) collapse byte-identical images  -> keep one canonical key, remap step regionKeys
  2) drop images not referenced by any step

HARD RULE: never echo base64. Print only path / size / counts.

Usage:
  python build.py --cases cases.json --shots shots_b64.json --out result.html
      [--template ../assets/template.html]
      [--no-embed-pdf]     # use lighter file; loads html2pdf from CDN instead
      [--no-embed-fonts]   # rely on Google Fonts <link> (needs internet)
"""
import argparse, hashlib, json, pathlib, sys

ASSETS = pathlib.Path(__file__).resolve().parent.parent / 'assets'
CDN_PDF = '<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>'

def dedup(shots, cases):
    """collapse byte-identical + drop unused; mutates cases' regionKeys."""
    # pass 1: byte-identical -> canonical
    h2canon, remap = {}, {}
    for k in list(shots):
        h = hashlib.md5(shots[k].encode()).hexdigest()
        if h in h2canon:
            remap[k] = h2canon[h]
        else:
            h2canon[h] = k
    if remap:
        for c in cases:
            for s in c['steps']:
                if len(s) > 3 and s[3] in remap:
                    s[3] = remap[s[3]]
    # pass 2: drop unused
    used = set(s[3] for c in cases for s in c['steps'] if len(s) > 3 and s[3])
    kept = {k: v for k, v in shots.items() if k in used}
    dropped = set(shots) - set(kept) - set(remap)
    return kept, remap, dropped, used

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cases', required=True)
    ap.add_argument('--shots', required=True)
    ap.add_argument('--out',   required=True)
    ap.add_argument('--template', default=str(ASSETS / 'template.html'))
    ap.add_argument('--no-embed-pdf',   action='store_true')
    ap.add_argument('--no-embed-fonts', action='store_true')
    args = ap.parse_args()

    cj    = json.load(open(args.cases, encoding='utf-8'))
    shots = json.load(open(args.shots, encoding='utf-8'))
    for req in ('groups', 'cases'):
        if req not in cj:
            sys.exit(f"ERROR: cases file missing '{req}'")
    cases = cj['cases']

    # validate every referenced region exists BEFORE dedup
    need = set(s[3] for c in cases for s in c['steps'] if len(s) > 3 and s[3])
    missing = need - set(shots)
    if missing:
        print(f"WARNING: {len(missing)} referenced region(s) have no image: {sorted(missing)}")

    shots, remap, dropped, used = dedup(shots, cases)

    payload = {
        'meta':   cj.get('meta', {}),
        'groups': cj['groups'],
        'data':   cj.get('data', {}),
        'cases':  cases,
        'shots':  shots,
    }

    tpl = open(args.template, encoding='utf-8').read()

    # fonts
    if args.no_embed_fonts:
        tpl = tpl.replace('__FONT_NOTO__', '').replace('__FONT_INTER__', '')
    else:
        fonts = json.load(open(ASSETS / 'fonts_b64.json', encoding='utf-8'))
        tpl = tpl.replace('__FONT_NOTO__',  fonts['Noto Sans Thai']) \
                 .replace('__FONT_INTER__', fonts['Inter'])

    # pdf library
    if args.no_embed_pdf:
        # neutralise the inline <script>__PDFLIB__</script> and add a CDN tag
        tpl = tpl.replace('<script>__PDFLIB__</script>', CDN_PDF)
    else:
        tpl = tpl.replace('__PDFLIB__', open(ASSETS / 'html2pdf.min.js', encoding='utf-8').read())

    # payload (do this LAST; payload may contain odd chars but no placeholders)
    tpl = tpl.replace('__PAYLOAD__', json.dumps(payload, ensure_ascii=False))

    for ph in ('__PAYLOAD__', '__PDFLIB__', '__FONT_NOTO__', '__FONT_INTER__'):
        if ph in tpl:
            print(f"WARNING: placeholder {ph} still present (check flags/template).")

    pathlib.Path(args.out).write_text(tpl, encoding='utf-8')
    kb = pathlib.Path(args.out).stat().st_size // 1024
    print(f"BUILT {args.out}  ({kb} KB)")
    print(f"  cases {len(cases)} | groups {len(cj['groups'])} | regions {len(shots)}"
          f" | byte-dupes collapsed {len(remap)} | unused dropped {len(dropped)}")
    if dropped:
        print(f"  dropped: {sorted(dropped)}")

if __name__ == '__main__':
    main()
