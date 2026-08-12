#!/usr/bin/env python3
"""E2E — ทะเบียนหน่วยวัด (F-UOM-001)

เดินจอจริงด้วย Chromium + assert ทุกเคส ไม่ใช่แค่ screenshot
ตัวรัน/ตัวรายงานอยู่ที่ `_SHARED/_e2e/uikit.py` — ไฟล์นี้มีแค่ "ลำดับการเดินจอ"

────────────────────────────────────────────────────────────────────────────
ตัวหาร (บังคับตั้งแต่ 2026-08-10) — อ้าง `Brief Feature/2. UOM/FUNCTION_CHECKLIST_F-UOM`
  FN บวก 23 ตัว (FN-01…19 + FN-13b + FN-90/92/93)
  ทะเบียนตั้งต้น 35 หน่วย · 25 แถว/หน้า (Strike 2026-08-10) → แบ่งหน้า 2 หน้า
    · ทดสอบบนจอนี้ได้ 22 ตัว
    · **FN-07 ทดสอบที่นี่ไม่ได้ตามนิยาม** — checklist เขียนเองว่า "(ตรวจฝั่งสินค้า)"
      คือ combobox ของ `F-PDM-001` ไม่ใช่จอนี้ (ดู GAP-03 ใน _COVERAGE_REPORT)
  FN-40 = 6 รายการที่ "ห้ามมี" → ต้องเป็นเคสเชิงลบ เรนเดอร์จริงแล้ว assert ว่าไม่มี

⚠️ ทำไม FN-40 ต้องอยู่ที่นี่ ไม่ใช่แค่ step 4:
   `qc-coverage` grep โค้ดได้แค่ "ไม่เจอ" — จับไม่ได้ถ้าปุ่ม **มีแต่ซ่อน** หรือโผล่เฉพาะบาง state
   E37–E42 จึงเดินทุก route (list / create / edit / view) ทุก tab แล้ว assert ว่าไม่มีจริง

ขอบเขต: เทสเฉพาะกฎที่ผูก "หลักยึดภายนอก"
  · FN-01…FN-19 + FN-13b + FN-90/92/93 + FN-40 จาก FUNCTION_CHECKLIST
  · BR-01…BR-07 · S-01…S-09 · OB-1…OB-6 จาก PREBRIEF
  · Global Contracts §2 #1 (DOA placeholder) · #6 (soft-reference) · #9
  · Iron Rule #16 (คอลัมน์ ≤8) · #70 (stat ≥4) · #95 (overlay portal) · #96 · #97 · #62.1
ไม่เทสสิ่งที่ AI ตัดสินเองตอนสร้าง (ถ้อยคำบนจอ · ลำดับคอลัมน์ · สีที่เลือก)

รัน: .claude/venv/bin/python _final-docs/F-UOM-001/_e2e/e2e-uom.py <file.html>
"""
import sys, pathlib, csv, io

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / '_SHARED' / '_e2e'))
from uikit import Suite, n, txt, settle, ready          # noqa: E402
from playwright.sync_api import sync_playwright         # noqa: E402

HTML = pathlib.Path(sys.argv[1]).resolve().as_uri()
S = Suite('ทะเบียนหน่วยวัด (F-UOM-001)')
check = S.check

# ─── FN-40 ①④⑤ — คำที่ห้ามโผล่บนจอ (ตรวจข้อความที่ "มองเห็นจริง") ─────────
BANNED_TEXT = {
    'FN-40① ตัวคูณ/ความละเอียด': ['ตัวคูณ', 'อัตราแปลง', 'สูตรแปลง', 'ความละเอียด',
                                  'ทศนิยม', 'หน่วยฐาน', 'หน่วยแปลง',
                                  'conversion', 'factor', 'precision'],
    'FN-40④ อนุมัติ':            ['ส่งอนุมัติ', 'สายอนุมัติ', 'ผู้อนุมัติ', 'รออนุมัติ',
                                  'อนุมัติแล้ว', 'ผู้ตรวจสอบ'],
    'FN-40⑤ จัดการหมวด':         ['เพิ่มหมวด', 'แก้ไขหมวด', 'จัดการหมวด', 'สร้างหมวด'],
}
# ─── FN-40 ② — ปุ่มที่กดแล้วลบได้รายตัว (ตรวจเฉพาะ element ที่กดได้) ───────
BANNED_ROW_SEL = ['.table [data-lucide="trash-2"]', '.table .ra-btn.is-danger',
                  '.table [onclick*="Delete"]', '.table [data-lucide="eye"]']

JS_VISIBLE_TEXT = """() => {
  const seen = [];
  document.querySelectorAll('body *').forEach(el => {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || cs.opacity === '0') return;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return;
    for (const nd of el.childNodes)
      if (nd.nodeType === 3 && nd.textContent.trim()) seen.push(nd.textContent.trim());
  });
  return seen.join(' \\n ');
}"""

JS_CLICKABLE_TEXT = """() => [...document.querySelectorAll(
  'button, a[onclick], [role=button], [role=menuitem], .sb-item, .stat, .drawer-tab')]
  .filter(el => { const r = el.getBoundingClientRect();
                  return r.width > 0 && r.height > 0 && getComputedStyle(el).display !== 'none'; })
  .map(el => (el.textContent || el.getAttribute('aria-label') || '').trim())"""


def reset(pg):
    """โหลดใหม่ = คืนข้อมูลตั้งต้น 35 หน่วย (mock อยู่ในหน่วยความจำ ไม่มี storage)"""
    ready(pg, HTML)
    return pg


def rows(pg):
    return pg.eval_on_selector_all(
        '.table tbody tr',
        "a=>a.map(tr=>[...tr.querySelectorAll('td')].map(td=>td.innerText.trim()))")


def codes(pg):
    return [r[1] for r in rows(pg)]


def stat_values(pg):
    return pg.eval_on_selector_all('.stat .stat-value', 'a=>a.map(x=>+x.textContent.replace(/\\D/g,""))')


def raw(pg, js):
    return pg.evaluate(js)


def fill(pg, sel, val):
    pg.fill(sel, val)


def main(pg):
    # ══════════════════════════════════════════════════════════════════════
    # A · โครงหน้า list (FN-18 · FN-19 · Rule #16/#70/#96)
    # ══════════════════════════════════════════════════════════════════════
    reset(pg)

    def a01():
        assert pg.evaluate('location.hash') in ('', '#/uom'), pg.evaluate('location.hash')
        c = n(pg, '.table thead th')
        assert c == 8, f'คอลัมน์ {c} ตัว (Rule #16 ต้อง ≤ 8)'
        assert n(pg, '.table tbody tr') == 25, 'หน้าแรกต้องมี 25 แถว (Strike 2026-08-10)'
        assert txt(pg, '.ph-count').startswith('35'), txt(pg, '.ph-count')
        return f'8 คอลัมน์ · 25 แถว/หน้า · ทั้งหมด 35 รายการ'
    check('E01', '[FN-19 · Rule #16] หน้า list เปิดได้ · โครงตาราง 8 คอลัมน์ · แบ่งหน้า 25 แถว', a01)

    def a02():
        v = stat_values(pg)
        assert len(v) >= 4, f'stat {len(v)} ใบ (Rule #70 ต้อง ≥ 4)'
        real = raw(pg, """() => ({t: RAW.length,
            a: RAW.filter(r=>r.status==='active').length,
            i: RAW.filter(r=>r.status==='inactive').length,
            d: RAW.filter(r=>r.status==='draft').length})""")
        assert v[:4] == [real['t'], real['a'], real['i'], real['d']], f'{v[:4]} != {real}'
        return f'{v[:4]} ตรงกับข้อมูลจริง'
    check('E02', '[FN-19 · Rule #70] stat 4 ใบ · ตัวเลขตรงกับข้อมูลจริง', a02)

    def a03():
        pg.click('.stats .stat:nth-child(4)'); settle(pg)     # ร่าง
        st = [r[6] for r in rows(pg)]
        assert st and all('ร่าง' in s for s in st), st
        got = len(st)
        pg.click('.stats .stat:nth-child(1)'); settle(pg)      # ทั้งหมด
        assert n(pg, '.table tbody tr') == 25, 'กดใบแรกต้องคืนตัวกรองทั้งหมด'
        return f'กรอง "ร่าง" ได้ {got} แถว แล้วคืนค่าได้'
    check('E03', '[FN-19] stat card กดกรองเร็วได้จริง (และกดซ้ำคืนค่า)', a03)

    def a04():
        fill(pg, '.input-search input', 'กิโล'); settle(pg)
        assert 'KG' in codes(pg), codes(pg)
        fill(pg, '.input-search input', 'pcs'); settle(pg)      # ค้นด้วยสัญลักษณ์
        assert 'PCS' in codes(pg), codes(pg)
        fill(pg, '.input-search input', 'CARTON'); settle(pg)   # ค้นด้วยรหัส
        assert codes(pg) == ['CARTON'], codes(pg)
        fill(pg, '.input-search input', ''); settle(pg)
        return 'ค้นได้ทั้ง ชื่อไทย / สัญลักษณ์ / รหัส'
    check('E04', '[FN-19] ค้นหาครอบ รหัส · ชื่อ · สัญลักษณ์', a04)

    def a05():
        pg.select_option('.filter-bar select >> nth=0', 'service'); settle(pg)
        assert all(r[4] == 'บริการ' for r in rows(pg)), rows(pg)
        svc = len(rows(pg))
        pg.select_option('.filter-bar select >> nth=1', 'inactive'); settle(pg)
        assert n(pg, '.table tbody tr') == 0 or all('ไม่ใช้งาน' in r[6] for r in rows(pg))
        pg.click('.btn-reset'); settle(pg)
        assert n(pg, '.table tbody tr') == 25, 'ล้างตัวกรองแล้วต้องกลับมาเต็มหน้า'
        opts = n(pg, '.filter-bar select >> nth=0 >> option')
        assert opts == 7, f'ตัวเลือกหมวด {opts} (ต้อง 6 หมวด + ทุกหมวด)'
        return f'กรองหมวดบริการได้ {svc} · หมวดมี 6 ค่าคงที่ · ล้างตัวกรองคืนค่าครบ'
    check('E05', '[FN-19] filter หมวด (6 ค่า) + สถานะ (3 ค่า) + ปุ่มล้างตัวกรอง', a05)

    def a06():
        first_asc = codes(pg)[0]
        pg.click('.table th.is-sortable >> nth=0'); settle(pg)   # code → desc
        first_desc = codes(pg)[0]
        assert first_asc != first_desc, f'sort ไม่เปลี่ยน ({first_asc})'
        pg.click('.table th.is-sortable >> nth=3'); settle(pg)   # used
        used = [int(r[5].replace(',', '')) for r in rows(pg)]
        assert used == sorted(used), f'sort ตัวเลขไม่เรียง: {used}'
        pg.click('.table th.is-sortable >> nth=0'); settle(pg)
        return f'code {first_asc}↔{first_desc} · used เรียงเลขถูก'
    check('E06', '[FN-19 · Rule #73] หัวคอลัมน์ sort ได้จริง (ตัวหนังสือ + ตัวเลข)', a06)

    def a07():
        p1 = codes(pg)
        pg.click('.pagination .pg-btn >> nth=2'); settle(pg)     # หน้า 2
        p2 = codes(pg)
        assert set(p1) & set(p2) == set(), 'หน้า 2 ต้องเป็นคนละชุด'
        assert len(p2) == 10, f'หน้า 2 ควรมี 10 แถว (35-25) แต่ได้ {len(p2)}'
        assert '35 รายการ' in txt(pg, '.table-foot'), txt(pg, '.table-foot')
        pg.click('.pagination .pg-btn >> nth=1'); settle(pg)
        return f'หน้า1 {len(p1)} · หน้า2 {len(p2)} · ไม่ทับกัน'
    check('E07', '[FN-19] แบ่งหน้าเดินได้จริง · แถวไม่ซ้ำข้ามหน้า', a07)

    def a08():
        fill(pg, '.input-search input', 'ไม่มีทางเจอแน่นอน'); settle(pg)
        assert n(pg, '.empty') == 1, 'ต้องมี empty state'
        t = txt(pg, '.empty-title')
        assert 'ไม่พบ' in t, t
        assert n(pg, '.empty [onclick*="resetFilters"]') == 1, 'empty ต้องมีปุ่มล้างตัวกรอง'
        pg.click('.empty .btn'); settle(pg)
        assert n(pg, '.table tbody tr') == 25, 'กดล้างตัวกรองจาก empty ต้องกลับมาเต็ม'
        return f'"{t}" + ปุ่มล้างตัวกรองใช้ได้'
    check('E08', '[FN-19 · Rule #39] empty state เคส "filter ไม่เจอ" + ปุ่มพากลับ', a08)

    def a09():
        bad = pg.eval_on_selector_all(
            '.table tbody tr td:nth-child(2)',
            "a=>a.filter(td=>td.querySelector('i,svg,img')).length")
        assert bad == 0, f'คอลัมน์รหัสมี icon/avatar {bad} จุด'
        return 'คอลัมน์รหัสเป็นตัวหนังสือล้วนทั้ง 25 แถว'
    check('E09', '[FN-18 · FN-40⑥] คอลัมน์รหัสไม่มี icon/avatar', a09)

    def a10():
        g = raw(pg, """() => {
            const f = document.querySelector('.table-foot').getBoundingClientRect();
            const w = document.querySelector('.table-wrap');
            return {gap: Math.round(window.innerHeight - f.bottom),
                    scrollable: w.scrollHeight > w.clientHeight + 1,
                    bodyScroll: document.documentElement.scrollHeight > window.innerHeight};}""")
        assert g['gap'] <= 40, f"ขอบล่างตารางห่างจอ {g['gap']}px (Rule #96 ต้องชิด)"
        assert not g['bodyScroll'], 'ทั้งหน้าไม่ควร scroll — scroll ต้องอยู่ใน .table-wrap'
        return f"ขอบล่างห่างจอ {g['gap']}px · scroll อยู่ในตาราง = {g['scrollable']}"
    check('E10', '[Rule #96] ตารางยืดชิดขอบล่าง · scroll อยู่ใน .table-wrap ไม่ใช่ทั้งหน้า', a10)

    # ══════════════════════════════════════════════════════════════════════
    # B · สร้าง (FN-01 · FN-02 · FN-03 · FN-04 · FN-12 · FN-92)
    # ══════════════════════════════════════════════════════════════════════
    def b11():
        pg.click('.ph-actions .btn-primary'); settle(pg)
        assert pg.evaluate('location.hash') == '#/uom/create', pg.evaluate('location.hash')
        assert pg.eval_on_selector('#drawer', 'e=>e.classList.contains("is-open")')
        assert n(pg, '.drawer .d-stepper, .drawer .stepper') == 0, 'ต้องเป็นฟอร์มเดียว ไม่มี wizard'
        f = n(pg, '.drawer-body .field')
        assert f == 6, f'ฟอร์มมี {f} ช่อง (ต้อง 6)'
        req = pg.eval_on_selector_all('.drawer-body .field-label .req', 'a=>a.length')
        assert req == 2, f'ช่องบังคับ {req} (ต้อง 2: ชื่อไทย + หมวด)'
        pg.reload(); settle(pg)
        assert pg.eval_on_selector('#drawer', 'e=>e.classList.contains("is-open")'), 'refresh แล้วลิ้นชักต้องยังเปิด'
        return 'drawer เดียว 6 ช่อง บังคับ 2 · route refresh-safe'
    check('E11', '[FN-01 · S-01] สร้างจาก drawer เดียว (ไม่มี wizard) · route กลับมาได้หลัง refresh', b11)

    def b12():
        c = n(pg, '.drawer-body .field-help, .drawer-body .info-tip, .drawer-body [data-tip], .drawer-body .hint-i')
        assert c == 0, f'พบข้อความอธิบายใต้ช่อง {c} จุด'
        return 'field-help / ⓘ / data-tip = 0'
    check('E12', '[FN-04 · Rule #67.1] ฟอร์มไม่มีข้อความคำอธิบายใต้ช่อง', b12)

    def b13():
        pg.click('#btn-save'); settle(pg)
        assert n(pg, '.field.is-invalid') == 1, 'ต้องมีช่องที่ถูกตีว่าไม่ผ่าน 1 ช่อง'
        assert n(pg, '#fld-name.is-invalid') == 1, 'ช่องที่ผิดต้องเป็นชื่อไทย'
        assert pg.evaluate('location.hash') == '#/uom/create', 'ห้ามบันทึกผ่าน'
        return 'บล็อกที่ช่องชื่อไทย · ลิ้นชักยังเปิด'
    check('E13', '[FN-92 · S-01] ไม่กรอกชื่อไทย → บล็อก + ชี้ช่องที่ผิด', b13)

    def b14():
        before = raw(pg, '() => RAW.length')
        fill(pg, '#in-name-th', 'ถัง')
        pg.select_option('#in-category', 'volume')
        pg.click('#btn-save'); settle(pg)
        assert pg.evaluate('location.hash') == '#/uom', 'บันทึกแล้วต้องกลับหน้า list'
        after = raw(pg, '() => RAW.length')
        assert after == before + 1, f'{before} → {after}'
        rec = raw(pg, "() => RAW.find(r=>r.name_th==='ถัง')")
        assert rec['code'].startswith('VOL'), f"รหัสอัตโนมัติ {rec['code']} ต้องขึ้นต้นด้วยหมวด"
        assert rec['category'] == 'volume' and rec['used'] == 0
        return f"สร้าง \"ถัง\" ได้ด้วยชื่อ+หมวด · รหัสอัตโนมัติ = {rec['code']}"
    check('E14', '[FN-01 · FN-02 · S-01] กรอกแค่ชื่อ+หมวด บันทึกได้ · เว้นรหัสว่าง → ออกรหัสจากหมวด', b14)

    def b15():
        pg.click('.ph-actions .btn-primary'); settle(pg)
        opts = pg.eval_on_selector_all('#in-status option', 'a=>a.map(o=>o.value)')
        assert opts == ['draft', 'active', 'inactive'], opts
        fill(pg, '#in-name-th', 'หน่วยร่างทดสอบ')
        fill(pg, '#in-code', 'TSTDRAFT')
        pg.select_option('#in-status', 'draft')
        pg.click('#btn-save'); settle(pg)
        rec = raw(pg, "() => RAW.find(r=>r.code==='TSTDRAFT')")
        assert rec and rec['status'] == 'draft', rec
        return 'เลือก 3 ค่าได้ตั้งแต่สร้าง · บันทึกเป็น ร่าง สำเร็จ'
    check('E15', '[FN-03 · BR-03] เลือกสถานะได้ 3 ค่าตั้งแต่ตอนสร้าง', b15)

    def b16():
        pg.click('.ph-actions .btn-primary'); settle(pg)
        fill(pg, '#in-name-th', 'ชิ้นซ้ำ')
        fill(pg, '#in-code', 'pcs')                 # ตัวพิมพ์เล็ก — ต้องยังชนกับ PCS
        pg.click('#btn-save'); settle(pg)
        assert n(pg, '#fld-code.is-invalid') == 1, 'ต้องบล็อกที่ช่องรหัส'
        msg = txt(pg, '#err-code')
        assert 'ถูกใช้แล้ว' in msg, msg
        assert pg.evaluate('location.hash') == '#/uom/create', 'ห้ามบันทึกผ่าน'
        pg.keyboard.press('Escape'); settle(pg)
        return f'"pcs" ชนกับ "PCS" → {msg}'
    check('E16', '[FN-12 · BR-01 · S-06] รหัสซ้ำไม่สนตัวพิมพ์ → บล็อก + ชี้ช่อง', b16)

    def b17():
        pg.click('.ph-actions .btn-primary'); settle(pg)
        fill(pg, '#in-name-th', 'ทดสอบกันกดซ้ำ')
        fill(pg, '#in-code', 'TSTDBL')
        before = raw(pg, '() => RAW.length')
        pg.evaluate("""() => { const b=document.getElementById('btn-save');
            b.click(); b.click(); b.click(); }""")          # กดรัว 3 ครั้ง
        settle(pg)
        after = raw(pg, "() => RAW.filter(r=>r.code==='TSTDBL').length")
        assert after == 1, f'กดรัว 3 ครั้งได้ {after} รายการ (ต้อง 1)'
        assert raw(pg, '() => RAW.length') == before + 1
        return 'กดรัว 3 ครั้ง → เกิดรายการเดียว'
    check('E17', '[FN-92 · Rule #44] ปุ่มบันทึกกันกดซ้ำ (double-submit)', b17)

    # ══════════════════════════════════════════════════════════════════════
    # C · แก้ไข (FN-05 · FN-12)
    # ══════════════════════════════════════════════════════════════════════
    reset(pg)

    def c18():
        pg.click('.table tbody tr:first-child .ra-btn'); settle(pg)
        assert pg.evaluate('location.hash').startswith('#/uom/edit/'), pg.evaluate('location.hash')
        rid = pg.evaluate("() => location.hash.split('/').pop()")
        dis = pg.eval_on_selector_all('.drawer-body .input, .drawer-body .select',
                                      'a=>a.filter(x=>x.disabled||x.readOnly).length')
        assert dis == 0, f'มีช่องที่แก้ไม่ได้ {dis} ช่อง (FN-05 ต้องแก้ได้ทุก field)'
        fill(pg, '#in-name-th', 'กล่องแก้ชื่อแล้ว')
        pg.click('#btn-save'); settle(pg)
        rec = raw(pg, f"() => RAW.find(r=>r.id==='{rid}')")
        assert rec['name_th'] == 'กล่องแก้ชื่อแล้ว', rec
        assert rec['updated_by'] == 'วิภา ผลิตภัณฑ์' and rec['updated_at'] == '2026-08-10', rec
        assert 'กล่องแก้ชื่อแล้ว' in pg.inner_text('.table'), 'list ต้องสะท้อนชื่อใหม่'
        return f"แก้ {rid} ได้ทุกช่อง · ผู้แก้/เวลาอัปเดต"
    check('E18', '[FN-05 · BR-07 · S-02] แก้ไขได้ทุก field + บันทึกผู้แก้/เวลา + list อัปเดต', c18)

    def c19():
        rid = raw(pg, "() => RAW.find(r=>r.status==='draft').id")
        pg.evaluate(f"() => location.hash = '#/uom/edit/{rid}'"); settle(pg)
        assert n(pg, '#in-name-th') == 1, 'สถานะ ร่าง ต้องเปิดแก้ได้'
        fill(pg, '#in-name-en', 'Edited While Draft')
        pg.click('#btn-save'); settle(pg)
        rec = raw(pg, f"() => RAW.find(r=>r.id==='{rid}')")
        assert rec['name_en'] == 'Edited While Draft', rec
        assert rec['status'] == 'draft', 'แก้แล้วสถานะต้องไม่ถูกเปลี่ยนเอง'
        return f'แก้ record สถานะ ร่าง ({rid}) ได้ · สถานะไม่ถูกแตะ'
    check('E19', '[FN-05] แก้ไขได้ "ทุกสถานะ" (ทดสอบกับ record สถานะ ร่าง)', c19)

    def c20():
        rid = raw(pg, "() => RAW.find(r=>r.code==='KG').id")
        pg.evaluate(f"() => location.hash = '#/uom/edit/{rid}'"); settle(pg)
        pg.click('#btn-save'); settle(pg)                       # รหัสเดิมของตัวเอง
        assert pg.evaluate('location.hash') == '#/uom', 'รหัสเดิมของตัวเองต้องไม่ถือว่าซ้ำ'
        pg.evaluate(f"() => location.hash = '#/uom/edit/{rid}'"); settle(pg)
        fill(pg, '#in-code', 'PCS')                             # ไปชนของคนอื่น
        pg.click('#btn-save'); settle(pg)
        assert n(pg, '#fld-code.is-invalid') == 1, 'ต้องบล็อกเมื่อไปชนรหัสของแถวอื่น'
        pg.keyboard.press('Escape'); settle(pg)
        return 'รหัสเดิม = ผ่าน · ชนรหัสคนอื่น = บล็อก'
    check('E20', '[FN-12 · BR-01] รหัสซ้ำตอนแก้ไข — แต่รหัสเดิมของตัวเองไม่นับซ้ำ', c20)

    # ══════════════════════════════════════════════════════════════════════
    # D · สถานะ (FN-06 · FN-08 · FN-09)
    # ══════════════════════════════════════════════════════════════════════
    reset(pg)

    def d21():
        pg.click('.table tbody tr:first-child'); settle(pg)
        assert pg.evaluate('location.hash').startswith('#/uom/view/')
        pg.click('#btnStatus'); settle(pg)
        items = pg.eval_on_selector_all('#statusMenu .st-item',
                                        'a=>a.map(x=>[x.innerText.trim(), x.disabled])')
        assert len(items) == 3, items
        cur = [i for i in items if i[1]]
        assert len(cur) == 1, f'ค่าปัจจุบันต้องกดไม่ได้ 1 ตัว: {items}'
        assert n(pg, '#statusMenu [onclick*="approve"], #statusMenu [onclick*="submit"]') == 0
        pg.keyboard.press('Escape'); settle(pg)
        return f'เมนู 3 ค่า · ปัจจุบัน "{cur[0][0]}" กดไม่ได้ · ไม่มีขั้นอนุมัติ'
    check('E21', '[FN-06 · BR-03 · S-03] เมนูเปลี่ยนสถานะ 3 ค่า · ค่าปัจจุบันกดไม่ได้ · ไม่มี gate', d21)

    def d22():
        rid = pg.evaluate("() => location.hash.split('/').pop()")
        seq = []
        for want, idx in (('draft', 1), ('inactive', 3), ('active', 2)):
            pg.click('#btnStatus'); settle(pg)
            pg.click(f'#statusMenu .st-item:nth-child({idx})'); settle(pg)
            got = raw(pg, f"() => RAW.find(r=>r.id==='{rid}').status")
            assert got == want, f'ตั้ง {want} แล้วได้ {got}'
            seq.append(got)
        return 'ใช้งาน → ' + ' → '.join(seq) + ' (ครบทุกทิศ)'
    check('E22', '[FN-06 · BR-03 · §5 state machine] เปลี่ยนสถานะได้ทุกทิศ ไม่มีลำดับบังคับ', d22)

    def d23():
        pg.keyboard.press('Escape'); settle(pg)
        assert n(pg, '.bulk-bar') == 0, 'ยังไม่เลือกต้องไม่มี bulk bar'
        pg.click('.table tbody tr:nth-child(1) .cb'); settle(pg)
        pg.click('.table tbody tr:nth-child(3) .cb'); settle(pg)
        assert n(pg, '.bulk-bar') == 1, 'เลือกแล้วต้องมี bulk bar'
        t = txt(pg, '.bulk-count')
        assert '2' in t, t
        assert pg.evaluate('location.hash') in ('', '#/uom'), 'ติ๊ก checkbox ต้องไม่เปิดลิ้นชัก'
        return f'"{t}" · กด checkbox แล้วไม่เผลอเปิด view'
    check('E23', '[FN-08 · Rule #41] ติ๊กหลายแถว → bulk bar พร้อมจำนวน (ไม่เผลอเปิด view)', d23)

    def d24():
        pg.click('.table thead .cb'); settle(pg)
        sel = raw(pg, '() => Object.values(state.sel).filter(Boolean).length')
        assert sel == 25, f'เลือกทั้งหน้าได้ {sel} (ต้อง 25)'
        assert n(pg, '.table tbody tr.is-selected') == 25
        return 'เลือกทั้งหน้าได้ครบ 25 แถว'
    check('E24', '[FN-08] เลือกทั้งหน้าด้วย checkbox หัวตาราง', d24)

    def d25():
        before = stat_values(pg)
        pg.click('.bulk-bar .btn-secondary >> nth=1'); settle(pg)      # ตั้งเป็น ร่าง
        after = stat_values(pg)
        assert after[3] > before[3], f'จำนวน ร่าง ต้องเพิ่ม: {before} → {after}'
        assert n(pg, '.bulk-bar') == 0, 'ทำงานเสร็จต้องล้างการเลือก'
        d = raw(pg, "() => RAW.filter(r=>r.status==='draft').length")
        assert d == after[3], f'stat {after[3]} != ข้อมูลจริง {d}'
        return f'ร่าง {before[3]} → {after[3]} · stat sync กับข้อมูลจริง'
    check('E25', '[FN-09 · BR-03 · S-04] bulk ตั้งสถานะ → เปลี่ยนครบ + ตัวนับอัปเดต', d25)

    # ══════════════════════════════════════════════════════════════════════
    # E · ลบ (FN-10 · FN-11 · FN-90 · BR-02)
    # ══════════════════════════════════════════════════════════════════════
    reset(pg)

    def e26():
        ids = raw(pg, """() => { const used = RAW.find(r=>r.used>0), free = RAW.find(r=>r.used===0);
            state.sel = {}; state.sel[used.id]=true; state.sel[free.id]=true; render();
            return {used: used.code, free: free.code}; }""")
        settle(pg)
        pg.click('.bulk-bar .btn-danger'); settle(pg)
        assert n(pg, '.modal-backdrop.is-open') == 1, 'ต้องเปิดหน้าต่างยืนยัน'
        body = pg.inner_text('.modal')
        assert 'ข้าม' in body, body
        btn = txt(pg, '#btn-del')
        assert '1' in btn, f'ปุ่มต้องบอกจำนวนลบจริง = 1: "{btn}"'
        return f"เลือก {ids['used']}(ถูกใช้) + {ids['free']}(ว่าง) → ปุ่ม \"{btn}\" + แจ้งข้าม"
    check('E26', '[FN-10 · BR-02 · S-05] confirm บอกจำนวนลบจริง + จำนวนที่จะข้าม', e26)

    def e27():
        before = raw(pg, '() => RAW.length')
        info = raw(pg, """() => { const k = Object.keys(state.sel).filter(x=>state.sel[x]);
            const u = k.map(i=>RAW.find(r=>r.id===i));
            return {used: u.find(r=>r.used>0).code, free: u.find(r=>r.used===0).code}; }""")
        pg.click('#btn-del'); settle(pg)
        after = raw(pg, '() => RAW.length')
        assert after == before - 1, f'{before} → {after} (ต้องลบแค่ 1)'
        left = raw(pg, '() => RAW.map(r=>r.code)')
        assert info['used'] in left, f"{info['used']} ถูกสินค้าใช้ ห้ามหาย"
        assert info['free'] not in left, f"{info['free']} ไม่ถูกใช้ ต้องหาย"
        assert n(pg, '.modal-backdrop.is-open') == 0, 'ยืนยันแล้วต้องปิดหน้าต่าง'
        return f"{info['free']} หาย · {info['used']} ยังอยู่ · {before}→{after}"
    check('E27', '[FN-11 · BR-02 · GC#6] ลบเฉพาะที่ไม่ถูกใช้ · ตัวที่ถูกสินค้าใช้ถูกข้าม', e27)

    def e28():
        # ไม่มีทางลบไหนที่ไม่ผ่าน confirm — ตรวจทุก route + ทุก tab
        found = []
        for h in ['#/uom', '#/uom/create']:
            pg.evaluate(f"() => location.hash='{h}'"); settle(pg)
            found += pg.eval_on_selector_all(
                '[onclick*="confirmBulkDelete"], [onclick*="RAW.filter"]',
                'a=>a.map(x=>x.getAttribute("onclick"))')
        rid = raw(pg, '() => RAW[0].id')
        pg.evaluate(f"() => location.hash='#/uom/view/{rid}'"); settle(pg)
        for i in (1, 2, 3):
            pg.click(f'.drawer-tab:nth-child({i})'); settle(pg)
            found += pg.eval_on_selector_all('.drawer [onclick*="confirmBulkDelete"]',
                                             'a=>a.map(x=>x.getAttribute("onclick"))')
        assert found == [], f'พบทางลบที่ข้าม confirm: {found}'
        pg.keyboard.press('Escape'); settle(pg)
        return 'ทุก route/ทุก tab: ไม่มีปุ่มที่เรียกลบตรง ๆ'
    check('E28', '[FN-90] การลบทุกทางต้องผ่าน confirm — ไม่มีทางลัด', e28)

    # ══════════════════════════════════════════════════════════════════════
    # F · นำเข้า / ส่งออก (FN-13 · FN-13b · FN-14 · FN-15 · FN-16 · FN-17)
    # ══════════════════════════════════════════════════════════════════════
    reset(pg)

    def f29():
        pg.click('.ph-actions .btn-secondary >> nth=1'); settle(pg)
        assert n(pg, '.modal.is-lg') == 1, 'ต้องเป็น modal ขนาดใหญ่ (Rule #32.1)'
        assert n(pg, '#pick-box') == 1, 'ต้องมีกล่องเลือกไฟล์'
        assert n(pg, '[onclick*="downloadTemplate"]') == 1, 'ปุ่ม template ต้องอยู่ในหน้าต่างนี้ (Rule #32.2)'
        body = pg.inner_text('.modal-body')
        for w in ['code', 'name_th', 'category', 'คอลัมน์', 'header']:
            assert w not in body, f'จอแรกต้องไม่มีข้อความอธิบายคอลัมน์ แต่เจอ "{w}"'
        return f'modal ใหญ่ · กล่องไฟล์ + ปุ่ม template · ไม่มีคำอธิบายคอลัมน์ (body="{body.strip()}")'
    check('E29', '[FN-13 · Rule #32.1/32.2] จอแรกมีแค่กล่องไฟล์ + ปุ่ม template', f29)

    def f30():
        with pg.expect_download() as d:
            pg.click('[onclick*="downloadTemplate"]')
        path = d.value.path()
        text = pathlib.Path(path).read_text(encoding='utf-8-sig')
        rows_ = list(csv.reader(io.StringIO(text)))
        assert rows_[0] == ['code', 'name_th', 'name_en', 'symbol', 'category', 'status'], rows_[0]
        st = [r[5] for r in rows_[1:]]
        assert set(st) == {'ใช้งาน', '', 'ไม่ใช้งาน'}, f'แถวตัวอย่างต้องครอบ 3 สถานะ: {st}'
        assert text.startswith('﻿') or pathlib.Path(path).read_bytes()[:3] == b'\xef\xbb\xbf', 'ต้องมี UTF-8 BOM'
        return f'header 6 คอลัมน์ถูก · ตัวอย่าง 3 แถวครอบ 3 สถานะ ({st}) · มี BOM'
    check('E30', '[FN-13b · Rule #32.2] ปุ่ม template ได้ไฟล์จริง header ถูก + ครอบ 3 สถานะ', f30)

    def f31():
        pg.click('#pick-box'); settle(pg)
        head = pg.eval_on_selector_all('.imp-table thead th', 'a=>a.map(x=>x.textContent.trim())')
        assert 'สถานะ' in head, head
        errs = pg.eval_on_selector_all('.imp-table .err-txt', 'a=>a.map(x=>x.textContent.trim())')
        joined = ' '.join(errs)
        for code_ in ('CODE_DUPLICATE', 'BAD_STATUS'):
            assert code_ in joined, f'ต้องเจอ {code_} ใน preview: {errs}'
        sums = pg.inner_text('.imp-sum')
        assert '5' in sums and '3' in sums and '2' in sums, sums
        return f'คอลัมน์สถานะมี · {len(errs)} จุดขึ้นข้อความผิดพลาด ({joined[:60]}…) · สรุป "{sums.strip()}"'
    check('E31', '[FN-14 · BR-05 · Rule #32.3] preview รายแถว: คอลัมน์สถานะ + รหัสข้อผิดพลาด', f31)

    def f32():
        before = raw(pg, '() => RAW.length')
        pg.click('#btn-import'); settle(pg)
        after = raw(pg, '() => RAW.length')
        assert after == before + 3, f'{before} → {after} (ต้องเข้า 3 แถว)'
        got = raw(pg, """() => ['TON','SET','KM'].map(c => {
            const r = RAW.find(x=>x.code===c); return r ? c+':'+r.status : c+':หาย'; })""")
        assert got == ['TON:active', 'SET:draft', 'KM:inactive'], got
        assert raw(pg, "() => RAW.filter(r=>r.code==='BAG').length") == 0, 'แถว BAD_STATUS ต้องไม่เข้า'
        assert raw(pg, "() => RAW.filter(r=>r.code==='PCS').length") == 1, 'แถวรหัสซ้ำต้องไม่เพิ่มซ้ำ'
        cat = raw(pg, "() => RAW.find(r=>r.code==='TON').category")
        assert cat == 'weight', f'หมวดไทย "ชั่งน้ำหนัก" ต้อง map เป็น weight ได้ (ได้ {cat})'
        return 'TON=ใช้งาน · SET=ร่าง(ว่าง) · KM=ไม่ใช้งาน · BAG/PCS ถูกข้าม · หมวดไทย map ถูก'
    check('E32', '[FN-15 · BR-05 · S-07] นำเข้าได้สถานะตามไฟล์ (ว่าง=ร่าง) · แถวผิดถูกข้ามไม่ล้มไฟล์', f32)

    def f33():
        assert n(pg, '.imp-sum') == 1, 'ต้องมีจอสรุปผล'
        assert 'ข้าม' in pg.inner_text('.modal-body'), 'จอผลต้องบอกจำนวนที่ข้าม'
        reasons = pg.eval_on_selector_all('.modal .err-txt', 'a=>a.length')
        assert reasons >= 2, f'จอผลต้องไล่สาเหตุที่ข้าม (เจอ {reasons})'
        pg.click('.modal-footer .btn-secondary'); settle(pg)
        assert n(pg, '.modal-backdrop.is-open') == 0
        assert txt(pg, '.ph-count').startswith('38'), txt(pg, '.ph-count')
        assert stat_values(pg)[0] == 38, stat_values(pg)
        assert 'TON' in pg.inner_text('.table') or n(pg, '.pagination .pg-btn') >= 4
        return 'ปิดจอผล → หัวข้อ 38 รายการ · stat 38 · ตารางสะท้อนของใหม่'
    check('E33', '[FN-16] ปิดจอผลนำเข้า → list + ตัวนับ stat อัปเดตตาม', f33)

    def f34():
        pg.select_option('.filter-bar select >> nth=1', 'inactive'); settle(pg)
        want = raw(pg, "() => RAW.filter(r=>r.status==='inactive').length")
        with pg.expect_download() as d:
            pg.click('[onclick*="exportCSV"]')
        text = pathlib.Path(d.value.path()).read_text(encoding='utf-8-sig')
        rr = [r for r in csv.reader(io.StringIO(text)) if r]
        assert rr[0][0] == 'รหัสหน่วย' and 'จำนวนสินค้าที่ใช้' in rr[0], rr[0]
        assert len(rr) - 1 == want, f'ส่งออก {len(rr)-1} แถว แต่ filter มี {want}'
        assert all(r[5] == 'ไม่ใช้งาน' for r in rr[1:]), rr[1:]
        pg.click('.btn-reset'); settle(pg)
        return f'กรอง "ไม่ใช้งาน" {want} แถว → ไฟล์ได้ {len(rr)-1} แถว ตรงกัน · 7 คอลัมน์'
    check('E34', '[FN-17 · S-08] ส่งออก CSV ตามตัวกรองปัจจุบัน (ไม่ใช่ทั้งทะเบียน)', f34)

    # ══════════════════════════════════════════════════════════════════════
    # G · ประวัติ + แท็บ (FN-93 · Rule #73.1)
    # ══════════════════════════════════════════════════════════════════════
    reset(pg)

    def g35():
        rid = raw(pg, "() => RAW.find(r=>r.code==='BOX').id")
        pg.evaluate(f"() => location.hash='#/uom/view/{rid}'"); settle(pg)
        pg.click('.drawer-tab:nth-child(3)'); settle(pg)
        body = pg.inner_text('.drawer-body')
        rec = raw(pg, f"() => RAW.find(r=>r.id==='{rid}')")
        assert 'สร้างรายการ' in body and 'แก้ไขล่าสุด' in body, body
        assert rec['created_by'] in body and rec['updated_by'] in body, body
        assert n(pg, '.timeline .tl-item') >= 2
        return f"ประวัติมีผู้สร้าง ({rec['created_by']}) + ผู้แก้ ({rec['updated_by']}) + เวลา"
    check('E35', '[FN-93 · BR-07] แท็บประวัติแสดงผู้สร้าง/ผู้แก้ + เวลา', g35)

    def g36():
        seen = []
        for i, want in ((1, 'รหัสหน่วย'), (2, 'จำนวนสินค้าที่ใช้'), (3, 'ประวัติการเปลี่ยนแปลง')):
            pg.click(f'.drawer-tab:nth-child({i})'); settle(pg)
            body = pg.inner_text('.drawer-body')
            assert want in body, f'แท็บ {i} ไม่มีเนื้อหา ("{want}" หาย)'
            assert len(body.strip()) > 20, f'แท็บ {i} ว่างเปล่า'
            seen.append(want)
        return 'ทั้ง 3 แท็บมีเนื้อหาจริง: ' + ' · '.join(seen)
    check('E36', '[Rule #73.1] ทุกแท็บมีชีวิต — ไม่มีแท็บกดแล้วเงียบ', g36)

    # ══════════════════════════════════════════════════════════════════════
    # H · FN-40 — เคสเชิงลบ 6 ข้อ (หัวใจของ scope lock)
    # ══════════════════════════════════════════════════════════════════════
    def walk_all_states(pg, collect):
        """เดินทุก route + ทุก tab + ทุก overlay แล้วเก็บผลด้วย collect(pg)"""
        acc = []
        reset(pg)
        acc.append(collect(pg))                                    # list
        pg.click('.table tbody tr:nth-child(1) .cb'); settle(pg)    # list + bulk bar
        acc.append(collect(pg))
        pg.click('.bulk-bar .btn-ghost'); settle(pg)
        pg.evaluate("() => location.hash='#/uom/create'"); settle(pg)
        acc.append(collect(pg))                                    # create
        rid = raw(pg, '() => RAW[0].id')
        pg.evaluate(f"() => location.hash='#/uom/edit/{rid}'"); settle(pg)
        acc.append(collect(pg))                                    # edit
        pg.evaluate(f"() => location.hash='#/uom/view/{rid}'"); settle(pg)
        for i in (1, 2, 3):                                        # view ทุก tab
            pg.click(f'.drawer-tab:nth-child({i})'); settle(pg)
            acc.append(collect(pg))
        pg.click('#btnStatus'); settle(pg)                          # view + เมนูสถานะ
        acc.append(collect(pg))
        pg.keyboard.press('Escape'); pg.keyboard.press('Escape'); settle(pg)
        pg.click('.ph-actions .btn-secondary >> nth=1'); settle(pg)  # import pick
        acc.append(collect(pg))
        pg.click('#pick-box'); settle(pg)                            # import preview
        acc.append(collect(pg))
        pg.click('.modal-footer .btn-ghost'); settle(pg)
        return acc

    def h37():
        seen = walk_all_states(pg, lambda p: p.evaluate(JS_VISIBLE_TEXT))
        hits = {}
        for blob in seen:
            low = blob.lower()
            for w in BANNED_TEXT['FN-40① ตัวคูณ/ความละเอียด']:
                if w.lower() in low:
                    hits[w] = hits.get(w, 0) + 1
        assert not hits, f'พบคำที่ล็อกไว้ว่าห้ามมี: {hits}'
        flds = raw(pg, '() => Object.keys(RAW[0])')
        for f_ in ('factor', 'conversions', 'precision', 'base_uom', 'decimals'):
            assert f_ not in flds, f'โมเดลมี field ต้องห้าม: {f_}'
        return f'เดิน {len(seen)} สถานะ · ไม่มีคำ/field เชิงแปลงหน่วยเลย (โมเดล {len(flds)} field)'
    check('E37', '[FN-40① · OB-1 · BR-04 · SCOPE LOCK] ไม่มีตัวคูณ/ความละเอียด/หน่วยฐานต่อสินค้า ทุกสถานะ', h37)

    def h38():
        reset(pg)
        found = []
        for sel in BANNED_ROW_SEL:
            if n(pg, sel):
                found.append(f'list:{sel}')
        rid = raw(pg, '() => RAW[0].id')
        for h in (f'#/uom/view/{rid}', f'#/uom/edit/{rid}'):
            pg.evaluate(f"() => location.hash='{h}'"); settle(pg)
            labels = pg.eval_on_selector_all(
                '.drawer button', 'a=>a.map(x=>(x.textContent||x.getAttribute("aria-label")||"").trim())')
            for lb in labels:
                if lb.startswith('ลบ') or lb == 'ลบ':
                    found.append(f'{h}:{lb}')
        assert found == [], f'พบปุ่มลบรายตัว: {found}'
        return 'แถวตาราง + view + edit: ไม่มีปุ่มลบรายตัว (ลบผ่าน bulk เท่านั้น)'
    check('E38', '[FN-40② · pattern เลน] ไม่มีปุ่มลบรายตัวทั้งในแถวและในลิ้นชัก', h38)

    def h39():
        reset(pg)
        code_ = raw(pg, """() => { const u = RAW.find(r=>r.used>0);
            state.sel = {}; state.sel[u.id]=true; render(); return u.code; }""")
        settle(pg)
        pg.click('.bulk-bar .btn-danger'); settle(pg)
        disabled = pg.eval_on_selector('#btn-del', 'e=>e.disabled')
        assert disabled, 'เลือกเฉพาะตัวที่ถูกใช้ → ปุ่มยืนยันลบต้องกดไม่ได้'
        pg.click('.modal-footer .btn-ghost'); settle(pg)
        assert code_ in raw(pg, '() => RAW.map(r=>r.code)'), f'{code_} ต้องยังอยู่'
        return f'เลือกเฉพาะ {code_} (ถูกสินค้าใช้) → ปุ่มลบ disabled · record ยังอยู่'
    check('E39', '[FN-40③ · BR-02 · OB-6] ลบหน่วยที่ถูกสินค้าใช้ไม่ได้เลย (ปุ่มยืนยันถูกปิด)', h39)

    def h40():
        seen = walk_all_states(pg, lambda p: p.evaluate(JS_CLICKABLE_TEXT))
        bad = [t for blob in seen for t in blob
               for w in BANNED_TEXT['FN-40④ อนุมัติ'] if w in t]
        assert not bad, f'พบปุ่ม/เมนูเกี่ยวกับอนุมัติ: {set(bad)}'
        txts = walk_all_states(pg, lambda p: p.evaluate(JS_VISIBLE_TEXT))
        bad2 = [w for blob in txts for w in BANNED_TEXT['FN-40④ อนุมัติ'] if w in blob]
        assert not bad2, f'พบข้อความเกี่ยวกับอนุมัติบนจอ: {set(bad2)}'
        ph = raw(pg, """() => RAW.every(r => r.approver_role===null && r.approved_by===null
                                          && r.approved_at===null && r.approval_chain===null)""")
        assert ph, 'field placeholder ของ DOA ต้องมีครบและเป็น null ทุกแถว (OB-3)'
        return 'ไม่มีปุ่ม/ข้อความอนุมัติเลย · placeholder 4 field = null ครบทุกแถว'
    check('E40', '[FN-40④ · OB-3 · GC#1] ไม่มีขั้นส่งอนุมัติ/สายอนุมัติ · placeholder เก็บเงียบ', h40)

    def h41():
        seen = walk_all_states(pg, lambda p: p.evaluate(JS_CLICKABLE_TEXT))
        bad = [t for blob in seen for t in blob
               for w in BANNED_TEXT['FN-40⑤ จัดการหมวด'] if w in t]
        assert not bad, f'พบปุ่มจัดการหมวด: {set(bad)}'
        reset(pg)
        cats = raw(pg, '() => CATEGORIES.map(c=>c.id)')
        assert cats == ['count', 'weight', 'volume', 'length', 'time', 'service'], cats
        # หมวดต้องโผล่ในรูป <option> เท่านั้น — ไม่มีช่องกรอกหมวดอิสระ
        pg.evaluate("() => location.hash='#/uom/create'"); settle(pg)
        free = n(pg, '.drawer-body input[id*="categ"], .drawer-body input[placeholder*="หมวด"]')
        assert free == 0, 'ต้องไม่มีช่องกรอกหมวดแบบพิมพ์เอง'
        assert n(pg, '#in-category option') == 6, n(pg, '#in-category option')
        pg.keyboard.press('Escape'); settle(pg)
        return '6 หมวดคงที่ · เลือกได้อย่างเดียว · ไม่มีปุ่ม/ช่องเพิ่มหมวด'
    check('E41', '[FN-40⑤] ไม่มี UI เพิ่ม/แก้หมวดหน่วยวัด (fix 6 หมวด)', h41)

    def h42():
        reset(pg)
        bad = []
        for h in ['#/uom']:
            pg.evaluate(f"() => location.hash='{h}'"); settle(pg)
            for page in (1, 2):
                if page == 2:
                    pg.click('.pagination .pg-btn >> nth=2'); settle(pg)
                c = pg.eval_on_selector_all(
                    '.table tbody tr td:nth-child(2)',
                    "a=>a.filter(td=>td.querySelector('i,svg,img,[class*=avatar],[class*=thumb]')).length")
                if c:
                    bad.append(f'{h} หน้า{page}: {c}')
        assert bad == [], f'คอลัมน์รหัสมี icon/avatar: {bad}'
        return 'ทั้ง 2 หน้าของตาราง: คอลัมน์รหัสเป็นตัวหนังสือล้วน'
    check('E42', '[FN-40⑥ · FN-18] ไม่มี icon/avatar หน้ารหัสในตาราง (ตรวจทุกหน้า)', h42)

    # ══════════════════════════════════════════════════════════════════════
    # I · Global Contracts · overlay · responsive · a11y
    # ══════════════════════════════════════════════════════════════════════
    def i43():
        bad = raw(pg, """() => RAW.filter(r => !('approver_role' in r) || !('approved_by' in r)
            || !('approved_at' in r) || !('approval_chain' in r)).map(r=>r.code)""")
        assert bad == [], f'แถวที่ขาด placeholder: {bad}'
        return f"ครบทุกแถว ({raw(pg,'() => RAW.length')} รายการ) × 4 field"
    check('E43', '[GC#1 · OB-3] DOA placeholder 4 field มีครบทุกแถวและเป็น null', i43)

    def i44():
        r = raw(pg, '() => RAW[0]')
        assert isinstance(r['used'], int), 'used ต้องเป็นตัวเลขอ่านอย่างเดียว'
        reset(pg)
        pg.evaluate("() => location.hash='#/uom/create'"); settle(pg)
        assert n(pg, '.drawer-body [id*="used"]') == 0, 'ต้องไม่มีช่องแก้ "จำนวนสินค้าที่ใช้"'
        pg.keyboard.press('Escape'); settle(pg)
        return 'ปลายทางเก็บรหัส · used อ่านอย่างเดียว ไม่มีช่องแก้'
    check('E44', '[GC#6 · LD-4C-02] soft-reference — ไม่มีช่องแก้ค่าที่ปลายทางเป็นเจ้าของ', i44)

    def i45():
        pg.set_viewport_size({'width': 1024, 'height': 800})
        reset(pg)
        assert pg.eval_on_selector('.nav-toggle', "e=>getComputedStyle(e).display!=='none'"), \
            'จอ 1024 ต้องมีปุ่มเปิดเมนู'
        rid = raw(pg, '() => RAW[0].id')
        pg.evaluate(f"() => location.hash='#/uom/view/{rid}'"); settle(pg)
        m = raw(pg, """() => { const d=document.querySelector('.drawer').getBoundingClientRect();
            return {w: Math.round(d.width), over: d.left < 0,
                    hscroll: document.documentElement.scrollWidth > window.innerWidth}; }""")
        assert not m['over'] and m['w'] <= 1024, m
        assert not m['hscroll'], 'จอ 1024 ต้องไม่มี horizontal scroll'
        pg.keyboard.press('Escape'); settle(pg)
        pg.set_viewport_size({'width': 1440, 'height': 900})
        return f"1024px: nav-toggle โผล่ · ลิ้นชัก {m['w']}px ไม่ล้น · ไม่มี h-scroll"
    check('E45', '[Rule #97] จอ 1024px — sidebar ยุบ · ลิ้นชักไม่ล้น · ไม่มี horizontal scroll', i45)

    def i46():
        reset(pg)
        pg.eval_on_selector('.table-wrap', 'e => e.scrollTop = 240'); settle(pg)
        rid = raw(pg, '() => RAW[2].id')
        pg.evaluate(f"() => location.hash='#/uom/view/{rid}'"); settle(pg)
        top = raw(pg, """() => { const th=document.querySelector('.table thead th');
            const r=th.getBoundingClientRect();
            const el=document.elementFromPoint(r.x+r.width/2, r.y+r.height/2);
            return el ? (el.closest('.drawer') ? 'drawer' : el.tagName+'.'+el.className) : 'none'; }""")
        z = raw(pg, """() => [getComputedStyle(document.querySelector('.table-wrap thead th')).zIndex,
                              getComputedStyle(document.querySelector('.drawer')).zIndex]""")
        assert 'TH' not in top, f'หัวตาราง sticky ทะลุลิ้นชัก (elementFromPoint = {top})'
        assert int(z[1]) > int(z[0]), f'z-index ลิ้นชัก ({z[1]}) ต้องมากกว่าหัวตาราง ({z[0]})'
        pg.keyboard.press('Escape'); settle(pg)
        return f'จุดกลางหัวตาราง = {top} · z-index thead {z[0]} < drawer {z[1]}'
    check('E46', '[Rule #62.1] หัวตาราง sticky ไม่ทะลุลิ้นชัก', i46)

    def i47():
        rid = raw(pg, '() => RAW[0].id')
        pg.evaluate(f"() => location.hash='#/uom/view/{rid}'"); settle(pg)
        pg.click('#btnStatus'); settle(pg)
        r = raw(pg, """() => { const m=document.getElementById('statusMenu');
            const b=m.getBoundingClientRect();
            const el=document.elementFromPoint(b.x+b.width/2, b.y+8);
            return {host: m.parentElement.id, fixed: getComputedStyle(m).position,
                    z: +getComputedStyle(m).zIndex,
                    drawerZ: +getComputedStyle(document.querySelector('.drawer')).zIndex,
                    onTop: el ? (m.contains(el) ? 'menu' : el.className) : 'none'}; }""")
        assert r['host'] == 'overlay-root', f"เมนูต้อง portal ไป #overlay-root (อยู่ที่ {r['host']})"
        assert r['fixed'] == 'fixed', r['fixed']
        assert r['z'] > r['drawerZ'], f"z เมนู {r['z']} ต้องมากกว่าลิ้นชัก {r['drawerZ']}"
        assert r['onTop'] == 'menu', f"จุดกลางเมนูถูก {r['onTop']} บังอยู่"
        pg.keyboard.press('Escape'); settle(pg)
        return f"portal → #overlay-root · position fixed · z {r['z']} > drawer {r['drawerZ']} · อยู่บนสุดจริง"
    check('E47', '[Rule #95] เมนูในลิ้นชัก portal ออกไปแล้วอยู่บนสุดจริง (ไม่จมใต้ลิ้นชัก)', i47)

    def i48():
        pg.click('#btnStatus'); settle(pg)
        assert pg.eval_on_selector('#statusMenu', 'e=>e.classList.contains("open")')
        pg.keyboard.press('Escape'); settle(pg)
        assert not pg.eval_on_selector('#statusMenu', 'e=>e.classList.contains("open")'), 'Esc ต้องปิดเมนู'
        assert pg.eval_on_selector('#drawer', 'e=>e.classList.contains("is-open")'), \
            'Esc ครั้งแรกต้องไม่ปิดลิ้นชักไปด้วย'
        pg.keyboard.press('Escape'); settle(pg)
        assert not pg.eval_on_selector('#drawer', 'e=>e.classList.contains("is-open")'), 'Esc ครั้งที่ 2 ต้องปิดลิ้นชัก'
        assert pg.evaluate('location.hash') == '#/uom'
        return 'Esc①ปิดเมนู (ลิ้นชักยังเปิด) → Esc②ปิดลิ้นชัก + คืน route'
    check('E48', '[Rule #68 Esc chain] Esc ปิดทีละชั้น — ไม่ปิดลิ้นชักทั้งใบในครั้งเดียว', i48)

    def i49():
        reset(pg)
        pg.click('.ph-actions .btn-primary'); settle(pg)
        first = pg.evaluate('() => document.activeElement.id || document.activeElement.className')
        assert pg.eval_on_selector('#drawer', 'e=>e.contains(document.activeElement)'), \
            f'เปิดลิ้นชักแล้วโฟกัสต้องอยู่ข้างใน (อยู่ที่ {first})'
        for _ in range(30):
            pg.keyboard.press('Tab')
        inside = pg.eval_on_selector('#drawer', 'e=>e.contains(document.activeElement)')
        assert inside, 'กด Tab วนแล้วโฟกัสต้องไม่หลุดออกนอกลิ้นชัก (focus trap)'
        pg.keyboard.press('Escape'); settle(pg)
        return f'โฟกัสเข้าลิ้นชักอัตโนมัติ ({first}) · Tab 30 ครั้งยังไม่หลุด'
    check('E49', '[a11y] เปิดลิ้นชักแล้วโฟกัสเข้าใน + Tab ไม่หลุดออกพื้นหลัง', i49)


with sync_playwright() as pw:
    br = pw.chromium.launch()
    page = br.new_page(viewport={'width': 1440, 'height': 900})
    S.watch(page)
    main(page)
    br.close()

print()
print('ตัวหาร — FUNCTION_CHECKLIST_F-UOM')
print('  FN บวก 23 ตัว · ทดสอบบนจอนี้ได้ 22 (FN-07 = cross-feature ตรวจที่ F-PDM-001)')
print('  FN-40 6 รายการ · ครอบด้วยเคสเชิงลบ E37–E42 ครบ 6/6')
print('  FN ที่ครอบ: 22/22 · รวมเคสทั้งหมด', len(S.results))
S.report()
