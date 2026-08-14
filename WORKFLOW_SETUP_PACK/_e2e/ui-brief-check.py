#!/usr/bin/env python3
"""ui-brief-check.py — ตัวช่วยทำ UI Brief (คู่กับ skill html-ui-brief)

ทำ 2 หน้าที่:

  โหมด extract (default)  — Phase 0 · ดึง inventory จาก HTML มาเป็น checklist กันหล่น
  โหมด verify             — Phase 4 · เทียบบรีฟที่เขียนเสร็จแล้วกับ HTML ว่าตกอะไรมั้ย

    python3 _final-docs/_SHARED/_e2e/ui-brief-check.py <file.html>
    python3 _final-docs/_SHARED/_e2e/ui-brief-check.py <file.html> --verify <UI_BRIEF_xxx.md>

stdlib ล้วน ไม่ต้องติดตั้งอะไร · ใช้ python3 ธรรมดาได้

⚠️ ห้ามใช้แทนการอ่านโค้ดจริง (Iron Rule R1 ของ skill)
   ตัวนี้บอกได้แค่ว่า "มีอะไรบ้าง" บอกไม่ได้ว่า "ทำไมถึงเป็นแบบนั้น"
   ส่วนที่มีค่าที่สุดของบรีฟคือเหตุผล ซึ่งต้องอ่านคอมเมนต์ในโค้ดเอง

ที่มา: `html-ui-brief` มี SKILL.md ไฟล์เดียวโดยตั้งใจ (ยืนยันกับเจ้าของ skill แล้ว)
       ตัวนี้เป็นของที่ทีมทำเองไว้ใช้ซ้ำ เก็บในโปรเจกต์ ไม่ได้ยัดเข้า skill
ถอดจากงานจริงที่ทำสำเร็จแล้ว: _final-docs/F-PR-001/UI_BRIEF_purchase-requisition.md

พิสูจน์แล้วว่าจับของจริงได้ 5 จุดในรอบแรก — สถานะการแปลง 2 ชุดคำ · .tip-pop ·
empty state ตัวที่ 5 · TYPEMETA/UOM_CAT_TH · PROD_STATUS_TH
"""
import re
import sys
import pathlib

TH = r'฀-๿'


# ───────────────────────── สกัด ─────────────────────────

def grab(html):
    """คืน dict ของทุกอย่างที่ต้องมีในบรีฟ"""
    d = {}

    d['tokens'] = sorted(set(re.findall(r'(--[a-z0-9-]+)\s*:', html)))
    d['zindex'] = sorted(
        {(m[0], int(m[1])) for m in re.findall(r'--z-([a-z]+)\s*:\s*(\d+)', html)},
        key=lambda x: -x[1])
    d['fonts'] = sorted(set(re.findall(
        r'(fonts\.googleapis\.com[^"\')]*|api\.fontshare\.com[^"\')]*)', html)))
    d['cdn'] = sorted(set(re.findall(
        r'(unpkg\.com[^"\')]*|jsdelivr\.net[^"\')]*|cdnjs\.cloudflare\.com[^"\')]*)', html)))

    # route: จอส่วนใหญ่ประกอบ hash เอง ('#/' + route) — จับทั้ง 2 แบบ
    lit = set(re.findall(r"['\"]#/([a-z-]*)", html))
    named = set(re.findall(r"navigate\('([a-z-]+)'", html))
    named |= set(re.findall(r"name === '([a-z-]+)'", html))
    named |= set(re.findall(r"name: '([a-z-]+)'", html))
    d['routes'] = sorted((lit | named) - {''})

    # overlay จริง = กล่องที่ลอย (position fixed/absolute) เท่านั้น
    # ห้ามจับ .drawer-body / .modal-footer ฯลฯ ซึ่งเป็นส่วนประกอบข้างใน ไม่ใช่ overlay
    d['overlays'] = sorted({
        cls for cls, body in re.findall(r'\.([a-z][a-z0-9-]*)\s*\{([^}]*)\}', html)
        if re.search(r'position:\s*(fixed|absolute)', body)
        and re.search(r'\bz-index\b', body)
    })
    d['backdrops'] = re.findall(r'<div class="([a-z-]*backdrop)"[^>]*id="(\w+)"[^>]*onclick="(\w+)\(', html)

    # toast: เก็บเฉพาะสตริงไทย ตัดส่วนที่ต่อด้วยตัวแปรออก
    toasts = []
    for call, variant in re.findall(r"showToast\((.*?),\s*'(info|success|warning|error)'\)", html):
        for s in re.findall(r"'([^']{3,})'", call):
            if re.search('[%s]' % TH, s):
                toasts.append((re.sub(r"\s*'\s*\+.*", "", s).strip(" ·+"), variant))
    d['toasts'] = sorted(set(toasts))

    d['buttons'] = sorted({b.strip() for b in re.findall(
        r'<span>([^<{]+)</span>\s*</button>', html) if b.strip()})

    # ⚠️ นับเฉพาะ label map แบน ๆ (`KEY: 'ค่า'`) — ห้ามนับ mock data ที่เป็น object/array ซ้อน
    # ของเดิมจับ `var AUDIT = { D001: [ { t:'...', by:'มานพ ขายเก่ง' } ] }` มาเป็น enum ด้วย
    # แล้วสั่งให้บรีฟต้องมี "ชื่อคนในข้อมูลตัวอย่าง" ครบทุกคน = สัญญาณหลอกล้วน
    # (เจอจริงตอนทำ F-DOC-001 · 2026-08-11) · ตัวคัด: body ที่มี `[` หรือ `{` = ไม่ใช่ label map
    d['enums'] = {name: re.findall(r"'([^']+)'", body)
                  for name, body in re.findall(r'var ([A-Z][A-Z_]+)\s*=\s*\{([^}]*)\}', html)
                  if '[' not in body and '{' not in body}

    d['esc'] = [(i + 1, l.strip()[:96])
                for i, l in enumerate(html.splitlines()) if "'Escape'" in l]

    # empty state 2 แบบ: เขียนค่าตรง ๆ กับเขียนด้วย ternary (hasFilter() ? 'ก' : 'ข')
    # ของเดิมจับได้แบบแรกอย่างเดียว → ตกหล่นทุก empty state ที่สลับข้อความตามบริบท
    d['empty'] = re.findall(r"title:\s*'([^']+)',\s*desc:\s*'([^']+)'", html)
    for t_expr, d_expr in re.findall(r"title:\s*([^\n]+?),\s*\n?\s*desc:\s*([^\n]+?),", html):
        titles = re.findall(r"'([^']+)'", t_expr)
        descs = re.findall(r"'([^']+)'", d_expr)
        if len(titles) >= 2 and len(descs) >= 2:      # ternary — เก็บทุกสาขา
            for pair in zip(titles, descs):
                if pair not in d['empty']:
                    d['empty'].append(pair)

    d['funcs'] = sorted(set(re.findall(r'function\s+([a-zA-Z_]\w*)\s*\(', html)))

    # BASE-KIT ทำ scroll lock ด้วย lockScroll() + คลาส is-overlay-open ไม่ใช่ body.style.overflow
    # ของเดิมจับ 2 แบบหลังไม่ได้ → ทุกไฟล์ที่ใช้ BASE-KIT โดนธง "❗ ไม่มี" ทั้งที่มีจริง
    d['scroll_lock'] = bool(re.search(
        r'body\.style\.overflow|scroll-?lock|lockScroll|is-overlay-open', html, re.I))
    d['focus_trap'] = bool(re.search(r'trapFocus|releaseFocus', html))
    d['focus_restore'] = bool(re.search(r'preserveRenderState|withRenderPreservation', html))

    return d


def report_extract(d):
    p = print
    p("\n╔═ INVENTORY — ใช้เป็น checklist กันหล่น ห้ามใช้แทนการอ่านโค้ด ═╗\n")

    p("── z-index map (สูง → ต่ำ) ──")
    for name, val in d['zindex']:
        p("   --z-%-10s %3d" % (name, val))

    p("\n── routes (%d) ──\n   %s" % (len(d['routes']), ' · '.join(d['routes']) or '—'))

    p("\n── overlays (%d) ──\n   %s" % (len(d['overlays']), ' · '.join('.' + o for o in d['overlays']) or '—'))
    for cls, el_id, fn in d['backdrops']:
        p("   backdrop .%s #%s → คลิกแล้วเรียก %s()" % (cls, el_id, fn))

    p("\n── Esc handler (%d จุด — ลำดับนี้คือ Esc chain) ──" % len(d['esc']))
    for line, txt in d['esc']:
        p("   บรรทัด %-5d %s" % (line, txt))

    p("\n── toast (%d ข้อความ — ต้องลงบรีฟแบบตรงตัวอักษร) ──" % len(d['toasts']))
    for msg, var in d['toasts']:
        p("   [%-7s] %s" % (var, msg))

    p("\n── ปุ่ม (%d) ──\n   %s" % (len(d['buttons']), ' · '.join(d['buttons']) or '—'))

    p("\n── enum / label map ──")
    for name, vals in d['enums'].items():
        th = [v for v in vals if re.search('[%s]' % TH, v) or v.isupper()]
        if th:
            p("   %-16s %s" % (name, ' · '.join(th)))

    p("\n── empty state (%d) ──" % len(d['empty']))
    for title, desc in d['empty']:
        p("   %s / %s" % (title, desc))

    p("\n── ของที่ 'ไม่มี' ต้องเขียนในบรีฟให้ชัด กันคนอ่านเดา (R4) ──")
    p("   scroll lock ตอนเปิด overlay : %s" % ('มี' if d['scroll_lock'] else '❗ ไม่มี'))
    p("   ล็อกโฟกัสไว้ใน overlay      : %s" % ('มี' if d['focus_trap'] else '❗ ไม่มี'))
    p("   คืน focus หลัง render       : %s" % ('มี' if d['focus_restore'] else '❗ ไม่มี'))

    p("\n── ตัวเลข ──")
    p("   CSS variable %d · function %d" % (len(d['tokens']), len(d['funcs'])))
    p("   ฟอนต์ %d แหล่ง · CDN %d แหล่ง%s" % (
        len(d['fonts']), len(d['cdn']),
        '  ❗ พึ่ง CDN — offline จะ fallback ฟอนต์' if d['cdn'] else ''))
    p("")


# ───────────────────────── ตรวจ ─────────────────────────

def report_verify(d, brief, html):
    """Phase 4 Verification Gate — คืน True ถ้าผ่าน"""
    fails = []

    def check(label, missing, total):
        good = not missing
        if not good:
            fails.append(label)
        print("  %s %-46s %d/%d%s" % (
            "✅" if good else "❌", label, total - len(missing), total,
            "" if good else "  → ขาด: %s" % (missing[:4])))

    routes = d['routes']
    check("route มี section ครบ",
          [r for r in routes if ('#/%s' % r) not in brief and ('`%s`' % r) not in brief],
          len(routes))

    ovl = ['.' + o for o in d['overlays']]
    check("overlay มีแถวใน Overlay Registry",
          [o for o in ovl if o not in brief], len(ovl))

    toasts = [m for m, _ in d['toasts']]
    check("ข้อความ toast อยู่ในบรีฟแบบตรงตัวอักษร",
          [m for m in toasts if m not in brief], len(toasts))

    enum_vals = [(n, v) for n, vals in d['enums'].items() for v in vals
                 if re.search('[%s]' % TH, v)]
    check("ค่า enum ครบทุกตัว",
          ["%s='%s'" % (n, v) for n, v in enum_vals if v not in brief], len(enum_vals))

    escs = [str(line) for line, _ in d['esc']]
    check("Esc chain อ้างเลขบรรทัด handler จริง",
          [e for e in escs if e not in brief], len(escs))

    zs = ['--z-%s' % n for n, _ in d['zindex']]
    check("z-index map ครบ", [z for z in zs if z not in brief], len(zs))

    empties = [t for t, _ in d['empty']]
    check("empty state ครบ", [t for t in empties if t not in brief], len(empties))

    # sample audit — ตัวเลขที่บรีฟอ้าง ต้องมีจริงในโค้ด
    # ⚠️ ข้อนี้เป็น WARN ไม่ใช่ FAIL — บรีฟอ้างตัวเลขเชิงเล่าเหตุการณ์ได้ด้วย
    #    (เช่น "เคยถูกตัดหาย 270px") ซึ่งไม่ใช่ค่าปัจจุบันในโค้ดและไม่ผิด
    #    ให้คนอ่านตัดสินเองว่าตัวไหนเป็นสเปคตัวไหนเป็นประวัติ
    nums = set(re.findall(r'\b(\d{2,4})(?:px|ms|vw)\b', brief))
    unmatched = [n for n in sorted(nums, key=int) if not re.search(r'(?<!\d)%s(?!\d)' % n, html)]
    print("  %s %-46s %d/%d%s" % (
        "✅" if not unmatched else "⚠️ ", "ตัวเลขที่บรีฟอ้าง มีจริงในโค้ด",
        len(nums) - len(unmatched), len(nums),
        "" if not unmatched else "  → ไม่เจอในโค้ด: %s  (ถ้าเป็นตัวเลขเชิงเล่าเหตุการณ์ ไม่ผิด)" % unmatched))

    print("\n  Verdict: %s" % ("PASS ✅" if not fails else "FAIL ❌ — %s" % ', '.join(fails)))
    return not fails


# ───────────────────────── main ─────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)

    html_path = pathlib.Path(sys.argv[1])
    if not html_path.exists():
        print("ไม่พบไฟล์: %s" % html_path)
        sys.exit(2)
    html = html_path.read_text(encoding='utf-8')
    d = grab(html)

    if '--verify' in sys.argv:
        i = sys.argv.index('--verify')
        if i + 1 >= len(sys.argv):
            print("--verify ต้องตามด้วย path ของไฟล์บรีฟ")
            sys.exit(2)
        brief_path = pathlib.Path(sys.argv[i + 1])
        if not brief_path.exists():
            print("ไม่พบไฟล์บรีฟ: %s" % brief_path)
            sys.exit(2)
        print("\n## 🔍 UI Brief Verification — %s\n" % html_path.name)
        sys.exit(0 if report_verify(d, brief_path.read_text(encoding='utf-8'), html) else 1)

    report_extract(d)


if __name__ == '__main__':
    main()
