#!/usr/bin/env python3
"""Pass R — Render Gate ของ qc-ux สำหรับ ทะเบียนหน่วยวัด (F-UOM-001)

จับภาพหลักฐานให้ด่าน "ตรวจด้วยตา" ของ qc-ux-html-checker:
  All-Tabs (#73.1) · Sticky-vs-Overlay (#62.1) · Bottom-Edge (#66) ·
  Dropdown Anatomy (#65) · List Full-Height (#96) · Responsive 1024 (#97)

⚠️ ไม่ใช้ `qc-ux-html-checker/scripts/render_shots.py` — ตัวนั้นไม่ใส่ `animations="disabled"`
   ทำให้ภาพ "เปลี่ยน" ทุกรอบทั้งที่จอไม่ได้เปลี่ยน (ดู CLAUDE.md) · ไฟล์นี้ใส่ให้ครบทุกใบ

รัน: .claude/venv/bin/python _final-docs/F-UOM-001/_e2e/shots-uom.py <file.html> [outdir]
"""
import sys, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / '_SHARED' / '_e2e'))
from uikit import ready, settle, hush          # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

HTML = pathlib.Path(sys.argv[1]).resolve().as_uri()
OUT = pathlib.Path(sys.argv[2] if len(sys.argv) > 2
                   else pathlib.Path(__file__).resolve().parents[1] / '_shots')
OUT.mkdir(parents=True, exist_ok=True)

errors = []
shots = []


def shot(pg, name):
    hush(pg)
    p = OUT / (name + '.png')
    pg.screenshot(path=str(p), full_page=False, animations='disabled')
    shots.append(p.name)
    print('  ·', p.name)


def run(pg, wide):
    tag = '' if wide else 'w1024_'
    ready(pg, HTML)
    shot(pg, f'{tag}01_list')

    # ── All-Tabs (#73.1) + Dropdown Anatomy/Overlay (#65/#62.1) ────────────
    pg.click('.table tbody tr:first-child'); settle(pg)
    shot(pg, f'{tag}02_view_overview')
    pg.click('.drawer-tab:nth-child(2)'); settle(pg)
    shot(pg, f'{tag}03_view_usage')
    pg.click('.drawer-tab:nth-child(3)'); settle(pg)
    shot(pg, f'{tag}04_view_history')
    pg.click('#btnStatus'); settle(pg)
    shot(pg, f'{tag}05_status_menu')
    pg.keyboard.press('Escape'); settle(pg)
    pg.keyboard.press('Escape'); settle(pg)

    if not wide:
        return

    # ── ฟอร์มสร้าง + validation ────────────────────────────────────────────
    pg.click('.ph-actions .btn-primary'); settle(pg)
    shot(pg, '06_create_form')
    pg.click('#btn-save'); settle(pg)
    shot(pg, '07_create_validation')
    pg.keyboard.press('Escape'); settle(pg)

    # ── เลือกหลายรายการ + ยืนยันลบ ────────────────────────────────────────
    pg.click('.table tbody tr:nth-child(1) .cb'); settle(pg)
    pg.click('.table tbody tr:nth-child(2) .cb'); settle(pg)
    shot(pg, '08_bulk_bar')
    pg.click('.bulk-bar .btn-danger'); settle(pg)
    shot(pg, '09_bulk_delete_confirm')
    pg.click('.modal-footer .btn-ghost'); settle(pg)
    pg.click('.bulk-bar .btn-ghost'); settle(pg)

    # ── นำเข้า CSV 3 จังหวะ ───────────────────────────────────────────────
    pg.click('.ph-actions .btn-secondary:nth-of-type(2)'); settle(pg)
    shot(pg, '10_import_pick')
    pg.click('#pick-box'); settle(pg)
    shot(pg, '11_import_preview')
    pg.click('#btn-import'); settle(pg)
    shot(pg, '12_import_done')
    pg.click('.modal-footer .btn-secondary'); settle(pg)

    # ── empty state 2 แบบ ─────────────────────────────────────────────────
    pg.fill('.input-search input', 'ไม่มีทางเจอ'); settle(pg)
    shot(pg, '13_empty_search')
    pg.click('.btn-reset'); settle(pg)

    # ── stat กดกรองเร็ว ───────────────────────────────────────────────────
    pg.click('.stats .stat:nth-child(4)'); settle(pg)
    shot(pg, '14_stat_filter_draft')
    pg.click('.stats .stat:nth-child(1)'); settle(pg)

    # ── Sticky-vs-Overlay (#62.1): เลื่อนตารางให้หัวค้าง แล้วเปิดลิ้นชัก ──
    pg.eval_on_selector('.table-wrap', 'e => e.scrollTop = 240'); settle(pg)
    shot(pg, '15_sticky_header')
    pg.click('.table tbody tr:nth-child(3)'); settle(pg)
    shot(pg, '16_sticky_vs_drawer')
    pg.keyboard.press('Escape'); settle(pg)

    # ── Bottom-Edge (#66): แถวล่างสุดของหน้า 2 → เปิดเมนูสถานะ ────────────
    pg.click('.pagination .pg-btn:nth-last-child(2)'); settle(pg)
    pg.click('.table tbody tr:last-child'); settle(pg)
    pg.click('#btnStatus'); settle(pg)
    shot(pg, '17_bottom_edge_menu')
    pg.keyboard.press('Escape'); settle(pg)
    pg.keyboard.press('Escape'); settle(pg)


with sync_playwright() as pw:
    br = pw.chromium.launch()
    for wide, vp in ((True, {'width': 1440, 'height': 900}), (False, {'width': 1024, 'height': 800})):
        pg = br.new_page(viewport=vp)
        pg.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        pg.on('pageerror', lambda e: errors.append('PAGEERROR: ' + str(e)))
        print(f"\n== viewport {vp['width']}x{vp['height']} ==")
        run(pg, wide)
        # ไม่มี body horizontal scrollbar (#97)
        ov = pg.evaluate('document.documentElement.scrollWidth > window.innerWidth')
        print(f"  body h-scroll: {ov}")
        if ov:
            errors.append(f"body มี horizontal scroll ที่ {vp['width']}px (#97)")
        pg.close()
    br.close()

print(f"\n== {len(shots)} ภาพ → {OUT} ==")
print('console/page errors:', errors if errors else 'ไม่มี')
sys.exit(1 if errors else 0)
