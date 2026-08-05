#!/usr/bin/env python3
"""static_scan.py — mechanical fact extractor for qc-ux-html-checker
Usage: python static_scan.py <file.html> [--json out.json]
Extracts FACTS only. Judging facts against iron rules is Claude's job
(rules must be Sync Read fresh from html-generator-v6).
"""
import sys, re, json, collections

def line_of(text, idx):
    return text.count("\n", 0, idx) + 1

def scan(path):
    src = open(path, encoding="utf-8", errors="replace").read()
    f = {"file": path, "size_bytes": len(src), "lines": src.count("\n") + 1}

    # --- hex colors (with counts + first-line samples) ---
    hexes = collections.Counter()
    first_line = {}
    for m in re.finditer(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b(?![0-9a-fA-F])", src):
        h = m.group(0).upper()
        hexes[h] += 1
        first_line.setdefault(h, line_of(src, m.start()))
    f["hex_colors"] = [
        {"hex": h, "count": c, "first_line": first_line[h]}
        for h, c in hexes.most_common()
    ]

    # --- fonts ---
    f["font_families"] = sorted(set(
        re.sub(r"\s+", " ", m.group(1)).strip()
        for m in re.finditer(r"font-family\s*:\s*([^;}{]+)", src)
    ))
    f["google_fonts_links"] = re.findall(r"fonts\.googleapis\.com[^\"']*", src)

    # --- px widths of interest (drawer/sidebar/shell/modal) ---
    px = collections.Counter(m.group(0) for m in re.finditer(r"\b\d{2,4}px\b", src))
    watch = ["920px", "680px", "540px", "440px", "232px", "52px"]
    f["px_watchlist"] = {w: px.get(w, 0) for w in watch}

    # --- icons ---
    f["lucide_icon_count"] = len(re.findall(r"data-lucide=", src))
    f["fontawesome"] = bool(re.search(r"fa[sbr]?\s+fa-|font-?awesome", src, re.I))
    emoji = re.findall(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", src)
    f["emoji"] = {"count": len(emoji), "samples": sorted(set(emoji))[:10]}

    # --- routing / interaction ---
    f["hash_routes"] = sorted(set(re.findall(r"#/[\w\-/:]+", src)))[:60]
    f["hashchange_listener"] = "hashchange" in src
    f["escape_handler"] = bool(re.search(r"['\"]Escape['\"]|keyCode\s*===?\s*27", src))
    f["drawer_translate"] = bool(re.search(r"translateX\(\s*100%\s*\)", src))
    f["backdrop"] = bool(re.search(r"backdrop", src, re.I))

    # --- scrollbar ---
    f["webkit_scrollbar"] = bool(re.search(r"::-webkit-scrollbar", src))
    m = re.search(r"::-webkit-scrollbar[^}]*width\s*:\s*(\d+)px", src)
    f["scrollbar_width_px"] = int(m.group(1)) if m else None

    # --- states & a11y markers ---
    f["markers"] = {
        "empty_state": len(re.findall(r"empty[-_]?state|\.empty\b", src, re.I)),
        "loading": len(re.findall(r"loading|spinner|skeleton", src, re.I)),
        "disabled": len(re.findall(r"\bdisabled\b", src)),
        "confirm_modal": len(re.findall(r"confirm", src, re.I)),
        "aria_attrs": len(re.findall(r"\baria-[a-z]+", src)),
        "placeholder": len(re.findall(r"placeholder=", src)),
    }

    # --- forbidden / risky ---
    f["localStorage_or_session"] = bool(re.search(r"localStorage|sessionStorage", src))
    f["external_scripts"] = re.findall(r"<script[^>]+src=[\"']([^\"']+)", src)
    f["inline_style_attr_count"] = len(re.findall(r"\sstyle=\"", src))

    # --- structure counts ---
    for tag in ["table", "button", "form", "input", "select", "dialog"]:
        f[f"count_{tag}"] = len(re.findall(rf"<{tag}\b", src, re.I))
    f["css_var_definitions"] = sorted(set(re.findall(r"--[\w-]+(?=\s*:)", src)))[:80]
    f["title"] = (re.search(r"<title>(.*?)</title>", src, re.S) or [None, ""])[1].strip()
    return f

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    facts = scan(sys.argv[1])
    out = json.dumps(facts, ensure_ascii=False, indent=2)
    if "--json" in sys.argv:
        open(sys.argv[sys.argv.index("--json") + 1], "w", encoding="utf-8").write(out)
    print(out)
