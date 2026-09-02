#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
capture.py — render the feature's HTML prototype, drive each UI state, highlight the
tested element (spotlight), screenshot the surrounding "screen", optimise, and emit a
shots_b64.json mapping  regionKey -> data:image/jpeg;base64,...

This is the SCREENSHOT ENGINE of the qa-friendly-html-generator skill. It is fully
general: the feature-specific part lives in a shot-spec JSON that Claude authors by
reading the prototype HTML (which JS calls open which screen, which selector is the
element under test). The engine just executes that spec.

HARD RULE: this script NEVER prints base64 to stdout. It writes the file and prints
only counts/paths. The caller (Claude) must NOT read the produced JSON back into the
context window — pass it straight to build.py.

Usage:
  export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers   # if needed in this env
  python capture.py --pack ./pack --spec shot-spec.json --out shots_b64.json
      [--assets ../assets] [--landscape 1300] [--portrait 940] [--quality 86]
      [--report shots.report.json] [--strict]

Verify gate (R18): the engine writes a TINY per-key status report (no base64) and
prints  OK n / SKIP+FAIL n  with the failing keys. Read the report/summary — NOT the
shots file — to confirm every important step got the RIGHT screenshot before build.
--strict makes the process exit non-zero if any requested shot produced no image.

shot-spec.json schema (see references/shot-spec-schema.md):
{
  "html": "prototype.html",        # path relative to --pack
  "route": "#/sow",                # optional initial location.hash
  "vw": 1200, "vh": 1000,          # viewport for capture
  "device_scale": 2,               # DPR (2 = crisp)
  "shots": [
    { "key": "list_stats",
      "setup": [],                            # JS statements run in page to reach state
      "wait": 400,                            # ms wait after each setup statement
      "container": "#page-content",           # element screenshotted (the "screen")
      "target": { "selector": ".stats" }      # element highlighted
    },
    { "key": "create_positions",
      "setup": ["startSow('create')"],
      "container": "#drawer",
      "target": { "selector": ".drawer-section", "has_text": "ตำแหน่งที่รับงานได้" }
    }
  ]
}
"""
import argparse, base64, json, pathlib, sys
from PIL import Image
from playwright.sync_api import sync_playwright

# spotlight: blue ring on the target + dim everything else (box-shadow scrim)
ADDHL = """(box)=>{const o=document.createElement('div');o.id='__hl';const p=7;
o.style.cssText='position:fixed;left:'+(box.x-p)+'px;top:'+(box.y-p)+'px;width:'+(box.width+p*2)+'px;height:'+(box.height+p*2)+'px;border:3px solid #0B5CFF;border-radius:10px;z-index:99999;pointer-events:none;box-shadow:0 0 0 9999px rgba(11,18,32,.42),0 0 14px 2px rgba(11,92,255,.55);';
document.body.appendChild(o);}"""

def b64_file(path):
    return base64.b64encode(pathlib.Path(path).read_bytes()).decode()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pack', required=True, help='folder containing the prototype HTML')
    ap.add_argument('--spec', required=True, help='shot-spec.json')
    ap.add_argument('--out',  required=True, help='output shots_b64.json')
    ap.add_argument('--assets', default=str(pathlib.Path(__file__).resolve().parent.parent / 'assets'))
    ap.add_argument('--landscape', type=int, default=1300)
    ap.add_argument('--portrait',  type=int, default=940)
    ap.add_argument('--quality',   type=int, default=86)
    ap.add_argument('--report', default=None,
                    help='tiny per-key status JSON (no base64). default: <out>.report.json')
    ap.add_argument('--strict', action='store_true',
                    help='exit non-zero if any requested shot did not produce an image')
    args = ap.parse_args()

    spec   = json.load(open(args.spec, encoding='utf-8'))
    pack   = pathlib.Path(args.pack).resolve()
    assets = pathlib.Path(args.assets).resolve()
    html   = (pack / spec['html']).resolve()
    if not html.exists():
        sys.exit(f"ERROR: prototype not found: {html}")
    url   = html.as_uri()
    dsf   = spec.get('device_scale', 2)
    vw, vh = spec.get('vw', 1200), spec.get('vh', 1000)
    route = spec.get('route')

    # inject the SAME fonts the final doc uses, so captures match (Thai + Inter)
    FONT = ""
    fb = assets / 'fonts_b64.json'
    if fb.exists():
        fonts = json.load(open(fb, encoding='utf-8'))
        FONT = "".join(
            f"@font-face{{font-family:'{fam}';src:url(data:font/woff2;base64,{b}) format('woff2');font-weight:100 900}}"
            for fam, b in fonts.items())
    # inject Lucide so icon-based prototypes render their glyphs
    LUCIDE = ""
    lu = assets / 'lucide.umd.js'
    if lu.exists():
        LUCIDE = lu.read_text(encoding='utf-8')

    work = pathlib.Path('./_qa_shots'); work.mkdir(exist_ok=True)
    shots = {}
    status = {}   # key -> {"status": ok|skip|fail, "note": "..."}  (R18 verify gate)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for shot in spec['shots']:
            key = shot['key']
            pg = browser.new_page(viewport={'width': vw, 'height': vh}, device_scale_factor=dsf)
            pg.goto(url, wait_until='domcontentloaded')
            if route:
                pg.evaluate("(h)=>{location.hash=h}", route)
            pg.wait_for_timeout(300)
            if FONT:   pg.add_style_tag(content=FONT)
            if LUCIDE: pg.add_script_tag(content=LUCIDE)
            pg.evaluate("()=>{try{window.lucide&&lucide.createIcons&&lucide.createIcons()}catch(e){}}")
            pg.wait_for_timeout(250)
            # drive the state
            for stmt in shot.get('setup', []):
                try:
                    pg.evaluate("()=>{ " + stmt + " }")
                except Exception as e:
                    print(f"  [warn] setup '{stmt[:40]}' on {key}: {str(e)[:60]}")
                pg.wait_for_timeout(shot.get('wait', 400))
            pg.evaluate("()=>{try{window.lucide&&lucide.createIcons&&lucide.createIcons()}catch(e){}}")
            pg.wait_for_timeout(150)
            # locate target
            t = shot['target']
            loc = pg.locator(t['selector'], has_text=t['has_text']).first if t.get('has_text') \
                  else pg.locator(t['selector']).first
            try:
                if loc.count() == 0:
                    print(f"  [skip] target matches nothing for {key}: {t}")
                    status[key] = {"status": "skip", "note": f"target matched nothing: {t}"}
                    pg.close(); continue
            except Exception:
                pass
            try:
                loc.scroll_into_view_if_needed(timeout=2000)
            except Exception:
                pass
            pg.wait_for_timeout(150)
            box = None
            try:
                box = loc.bounding_box(timeout=3000)
            except Exception as e:
                print(f"  [FAIL] target not visible for {key}: {str(e)[:60]}")
            if not box:
                print(f"  [skip] no bounding box for {key}")
                status[key] = {"status": "skip", "note": "target found but not visible (no bounding box) — setup may not reach this state"}
                pg.close(); continue
            pg.evaluate(ADDHL, box)
            pg.wait_for_timeout(120)
            png = work / f"{key}.png"
            try:
                pg.locator(shot['container']).first.screenshot(path=str(png))
            except Exception as e:
                print(f"  [FAIL] container screenshot {key}: {str(e)[:70]}")
                status[key] = {"status": "fail", "note": f"container screenshot failed: {str(e)[:70]}"}
                pg.close(); continue
            pg.close()
            # optimise: resize to target width, JPEG
            im = Image.open(png).convert('RGB')
            w, h = im.size
            target_w = args.landscape if w >= h else args.portrait
            if w > target_w:
                im = im.resize((target_w, int(h * target_w / w)), Image.LANCZOS)
            jp = work / f"{key}.jpg"
            im.save(jp, quality=args.quality)
            shots[key] = 'data:image/jpeg;base64,' + b64_file(jp)
            status[key] = {"status": "ok", "note": f"{im.size[0]}x{im.size[1]}"}
            print(f"  [ok] {key}  {im.size[0]}x{im.size[1]}  {len(shots[key])//1024} KB")
        browser.close()

    # any requested key we never reached the loop-body 'ok' for is implicitly not captured
    for shot in spec['shots']:
        status.setdefault(shot['key'], {"status": "fail", "note": "not processed"})

    json.dump(shots, open(args.out, 'w', encoding='utf-8'), ensure_ascii=False)

    # tiny status report (NO base64) — Claude reads THIS to verify per-key (R18), not the shots file
    report_path = args.report or (str(pathlib.Path(args.out).with_suffix('')) + '.report.json')
    json.dump(status, open(report_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    ok   = [k for k, v in status.items() if v['status'] == 'ok']
    bad  = [(k, v) for k, v in status.items() if v['status'] != 'ok']
    total = sum(len(v) for v in shots.values()) // 1024
    print(f"\nWROTE {args.out}  ({len(shots)} regions, ~{total} KB).  base64 NOT printed.")
    print(f"CAPTURE VERIFY (R18):  OK {len(ok)}  ·  SKIP/FAIL {len(bad)}   → report: {report_path}")
    for k, v in bad:
        print(f"  [{v['status']}] {k} — {v['note']}")
    if bad:
        print("  ↑ these steps will have NO image. Fix shot-spec (setup/selector) & re-capture,")
        print("    or set regionKey=\"\" for those steps. Do NOT let a step show a wrong screen (R18).")
    print("Next: python build.py --cases cases.json --shots", args.out, "--out result.html")
    if args.strict and bad:
        sys.exit(2)

if __name__ == '__main__':
    main()
