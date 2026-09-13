#!/usr/bin/env python3
"""static_scan.py — mechanical fact extractor for qc-ux-html-checker
Usage: python static_scan.py <file.html> [--json out.json]
Extracts FACTS only. Judging facts against iron rules is Claude's job
(rules must be Sync Read fresh from the highest installed html-generator — v9 as of 2026-08-25).
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
    watch = ["920px", "680px", "540px", "440px", "232px", "52px", "1290px", "244px", "58px"]
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
    # --- v9 facts: #94/#102 combobox, #95 overlay portal, #96 list full-height, #97 responsive, #98-101 doc archetype ---
    f["select_big"] = sum(1 for m in re.finditer(r"<select[^>]*>(.*?)</select>", src, re.S) if m.group(1).count("<option") > 7)
    f["select_big_template"] = len(re.findall(r"<select[^>]*>\$\{[^}]*\.map\(", src))
    f["combobox_count"] = len(re.findall(r"combo-pop|item-combo|search-select|searchSelectHTML", src))
    f["combo_person_option"] = len(re.findall(r"emp-av", src))
    f["overlay_root"] = "overlay-root" in src
    f["portal_menu"] = bool(re.search(r"portalMenu|menu-fixed|position:\s*fixed;[^}]*combo-pop|\.combo-pop\{position:fixed", src))
    f["page_fill"] = "page-fill" in src
    f["render_table_only"] = "renderTableOnly" in src
    f["body_minwidth_768"] = bool(re.search(r"body\s*\{[^}]*min-width:\s*768px", src))
    f["scrollbar_gutter_stable"] = "scrollbar-gutter" in src
    f["doc_archetype"] = {
        "is_document": bool(re.search(r"vat_mode|renderSignTab|line-tbl", src)),
        "line_tbl": 'class="tbl line-tbl"' in src,
        "wizard_steps": re.findall(r"renderStepperItem\(\d+,\s*'([^']+)'", src),
        "view_tabs": re.findall(r"tabBtn\('(\w+)'", src),
        "attach_in_detail": bool(re.search(r"SEC\('paperclip',\s*`เอกสารแนบ", src)),
        "has_calcLineVat": "function calcLineVat" in src, "has_totals": bool(re.search(r"function totals\(", src)),
        "has_taxBadgeV": "function taxBadgeV" in src, "has_docPill": "function docPill" in src,
        "has_signProgress": "function renderSignProgress" in src, "a4": 'class="a4"' in src, "slot_row": "slot-row" in src,
        "vat_segmented_3": "'รวมแล้ว (NET)'" in src, "endbill_mode": "endbill.mode" in src,
        "line_tbl_widths": re.findall(r'<th style="width:\s*(\d+)px', src[src.find('class="tbl line-tbl"'):src.find('class="tbl line-tbl"')+1500]) if 'class="tbl line-tbl"' in src else [],
    }
    f["td_multi_pill"] = len(re.findall(r'<td[^>]*>[^<]*(?:<span class="pill[^>]*>[^<]*</span>[^<]*){2,}</td>', src))
    f["preflight_stamp"] = (re.search(r"<!--\s*PREFLIGHT[^>]{0,200}", src) or [None, ""])[0][:200] if re.search(r"<!--\s*PREFLIGHT", src) else None
    f["planner_archetype"] = bool(re.search(r"cal-grid|pool-card|gt-row", src))
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
