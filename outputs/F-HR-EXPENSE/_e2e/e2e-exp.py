"""E2E · F-HR-EXPENSE (เบิกค่าใช้จ่าย / Expense Claim) — WF-01 Step 5

รันไทม์ตัวเดียวที่ครอบทุก FN (22 = FN-01..17 + FN-90..94) + เคสเชิงลบ 7 ข้อ
(unsupported[]) ที่เรนเดอร์จริงแล้ว assert ว่า "ไม่มี" affordance บนจอ (FN-40-equivalent).

ยึด helper ของ uikit เท่านั้น (ready/settle/after) — ไม่มี wait_for_timeout, ไม่มีตัวตรวจ UI ใหม่.
ขับหน้าจอผ่าน controller function จริงของไฟล์ (openCreate/openDrawer/openModal/doApprove/…)
แล้ว assert ทั้ง data model (EXP.docs/totals/resolveDoa) และข้อความที่เรนเดอร์บน DOM.
reload หน้าใหม่ต่อเคส → mock data (EXP.docs) reset = เคสอิสระต่อกัน.

DSP checks (recur ทุก W5-HR feature):
  DSP-01  modal ที่เปิดในลิ้นชัก (submit/approve) ต้องอยู่เหนือ drawer (z portal 60 > drawer 55)
  DSP-02a combobox (wizemp) เลือกแล้วปิด ไม่เด้งกางใหม่จาก focus-restore (#29)
  DSP-02b submit modal เปิด → ไม่มี combobox (slot picker) กาง dropdown เอง (trapFocus auto-open)

รัน (cwd = repo root):
  PYTHONIOENCODING=utf-8 .claude/venv/Scripts/python.exe \
      outputs/F-HR-EXPENSE/_e2e/e2e-exp.py outputs/F-HR-EXPENSE/expense.html
"""
from pathlib import Path
import re
import sys

from playwright.sync_api import sync_playwright

OUTPUTS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(OUTPUTS / "_SHARED" / "_e2e"))
from uikit import (  # noqa: E402
    Suite, ready, settle as shared_settle, after as shared_after,
    assert_combobox_closes_after_select, modal_autoopens_comboboxes,
    assert_no_garbage_text,
    # ⭐ user-found bug probes (§C3.8 · F-HR-EXPENSE 2026-09-09)
    assert_overlay_cleared_after_close, assert_footer_actions_hittable,
    assert_stepper_well_formed, assert_filter_inside_card,
    assert_submit_requires_all_approvers, assert_overlay_cleared_after_confirm_action,
    assert_combobox_floats_in_modal,
    # ⭐ submit-modal fixes (§C3.8 · F-HR-EXPENSE 2026-09-10)
    assert_slot_dropdown_no_spill, assert_submit_modal_all_dismiss_clean,
    # ⭐ backdrop bug (§C3.8 · F-HR-EXPENSE 2026-09-10) — draft-view submit closes drawer + wizard-cancel guard
    assert_wizard_submit_cancel_keeps_drawer,
    JS_MODAL_UNDER_DRAWER, JS_AFFORDANCE, JS_CSSVAR, JS_OVERLAY_STACK,
)

HTML = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parents[1] / "expense.html").resolve()
BASE = HTML.as_uri()

suite = Suite("F-HR-EXPENSE เบิกค่าใช้จ่าย")

# รอ rAF chain ให้ trapFocus + guardOverlayAutoCombo (#29) ทำงานจนจบก่อนอ่านสถานะสุดท้าย
_RAF_SETTLE = "() => new Promise(res=>{let n=0;const t=()=>{n++;if(n>=6)res();else requestAnimationFrame(t);};requestAnimationFrame(t);})"


def settle(page, timeout=1400):
    shared_settle(page, timeout=timeout)


def after(page, js, timeout=1600):
    return shared_after(page, js, timeout=timeout)


def open_(page):
    """เปิดหน้าใหม่ (reset mock data) แล้วรอ render จริง (page-content ไม่ว่าง)"""
    ready(page, BASE, timeout=12000)
    page.wait_for_function(
        "() => { const p=document.getElementById('page-content'); return p && p.innerHTML.trim().length>0; }",
        timeout=12000,
    )


def ev(page, js):
    return page.evaluate(js)


def pc_text(page):
    return page.evaluate("() => document.getElementById('page-content').textContent")


def drawer_text(page):
    return page.evaluate("() => (document.getElementById('drawer')||{}).textContent || ''")


def modal_text(page):
    return page.evaluate("() => (document.querySelector('#modalBackdrop .modal')||{}).textContent || ''")


def pick_all_slots(page):
    """เลือกผู้อนุมัติจริง (คนแรกของพูล) ครบทุก slot ใน submit modal ที่เปิดอยู่ —
    หลัง fix Bug A ไม่มี auto-pick แล้ว ปุ่มส่งจึง disabled จนกว่าจะเลือกครบทุก slot"""
    after(page, """() => { const doa=resolveDoa((state.doaDraft&&state.doaDraft.grand)||0);
      doa.steps.forEach((s,i)=>{ if(window.__ss && window.__ss['slot-'+i]) ssPick('slot-'+i,0); }); }""")


def wizard_to_step2(page, emp=None):
    """เปิด wizard สร้างใบเบิก แล้วเลื่อนไปขั้น 2 (ข้อมูลหลัก · มี combobox wizemp)"""
    after(page, "() => openCreate()")
    js = "() => { state.wizard.step=2;%s renderDrawerOnly(); }" % (
        " state.wizard.doc.emp='%s';" % emp if emp else "")
    after(page, js)


# ═══════════════════════════════ FN CASES ═══════════════════════════════

def c_fn01(page):
    """[FN-01 · S-01] สร้างใบเบิกผ่าน wizard 5 ขั้น (เลือกแหล่งที่มา›ข้อมูลหลัก›รายการ›เอกสารแนบ›ตรวจสอบ)"""
    open_(page)
    keys = ev(page, "() => STEP_KEYS")
    assert keys == ['เลือกแหล่งที่มา', 'ข้อมูลหลัก', 'รายการค่าใช้จ่าย', 'เอกสารแนบ', 'ตรวจสอบและยืนยัน'], \
        f"ลำดับ/ชื่อ 5 ขั้นไม่ตรง contract: {keys}"
    after(page, "() => openCreate()")
    assert ev(page, "() => state.drawer.open && state.drawer.mode==='wizard'"), "openCreate ไม่เปิด wizard drawer"
    assert ev(page, "() => state.wizard.step") == 1, "wizard ไม่เริ่มที่ขั้น 1"
    dots = ev(page, "() => document.querySelectorAll('#drawer .stepper .step-dot').length")
    assert dots == 5, f"stepper ต้องมี 5 ขั้น (ได้ {dots})"
    # ใส่ข้อมูลที่ถูกต้องก่อนเดิน (BUG-4: step-advance gate — ขั้น 2 ต้องมีผู้เบิก · ขั้น 3 ต้องมีรายการ+ยอด>0)
    after(page, "() => { state.wizard.doc.emp='E01'; state.wizard.doc.lines=[{date:'2569-08-28',cat:'other',desc:'x',qty:1,unit_price:500,vat_mode:'none'}]; renderDrawerOnly(); }")
    # เดินครบ 5 ขั้น
    for s in range(2, 6):
        after(page, "() => wizNext()")
        assert ev(page, "() => state.wizard.step") == s, f"wizNext ไม่ไปขั้น {s}"
    dt = drawer_text(page)
    assert "ตรวจสอบและยืนยัน" in dt and "บันทึกและส่งอนุมัติ" in dt, "ขั้นสุดท้ายไม่มีสรุป/ปุ่มส่งอนุมัติ"
    return "wizard 5 ขั้น: เลือกแหล่งที่มา›ข้อมูลหลัก›รายการ›เอกสารแนบ›ตรวจสอบ (เดินครบ · ปุ่มส่งขั้น 5)"


def c_fn02(page):
    """[FN-02 · S-01 · BR-08] หัวเอกสาร: ผู้เบิก (combobox) · วันที่ (พ.ศ.) · ช่องทางจ่าย"""
    open_(page)
    wizard_to_step2(page)
    assert ev(page, "() => !!(window.__ss && window.__ss['wizemp'])"), "ขั้น 2 ไม่มี combobox ผู้เบิก (wizemp)"
    emp_ok = ev(page, "() => { const s=window.__ss['wizemp']; return s.options.length===EXP.emps.length && s.options.every(o=>o.label && o.sub); }")
    assert emp_ok, "combobox ผู้เบิกไม่ครบ/ไม่มี label+ตำแหน่ง"
    dt = drawer_text(page)
    assert "วันที่เอกสาร (พ.ศ.)" in dt, "ไม่มีช่องวันที่ (พ.ศ.)"
    assert "ผ่านรอบเงินเดือน" in dt and "โอนตรง" in dt, "ไม่มีตัวเลือกช่องทางจ่าย"
    # วันที่อยู่ใน input value (พ.ศ. 25xx) — textContent ไม่เก็บ value จึงอ่านจาก DOM
    assert ev(page, r"() => [...document.querySelectorAll('#drawer input')].some(i=>/^25\d\d-/.test(i.value))") is True, \
        "วันที่ default ไม่เป็น พ.ศ. (25xx)"
    return "หัวเอกสาร: ผู้เบิก combobox (4 คน) · วันที่ พ.ศ.2569 · ช่องทางจ่าย 2 ตัวเลือก"


def c_fn03(page):
    """[FN-03 · S-02 · BR-01] line editor + VAT none/add/included + ยอดรวม/VAT/สุทธิ ถูกต้อง"""
    open_(page)
    after(page, "() => openCreate()")
    after(page, """() => { state.wizard.step=3; state.wizard.doc.lines=[
      {date:'2569-08-28',cat:'other',desc:'ไม่คิด VAT',qty:1,unit_price:1000,vat_mode:'none'},
      {date:'2569-08-28',cat:'other',desc:'บวก VAT',qty:1,unit_price:1000,vat_mode:'add'},
      {date:'2569-08-28',cat:'other',desc:'รวม VAT แล้ว',qty:1,unit_price:1070,vat_mode:'included'}
    ]; renderDrawerOnly(); }""")
    # per-line VAT engine
    lt = ev(page, "() => state.wizard.doc.lines.map(l=>Math.round(calcLineVat(l).lineTotal))")
    assert lt == [1000, 1070, 1070], f"lineTotal ต่อบรรทัดผิด: {lt}"
    t = ev(page, "() => { const t=totals(state.wizard.doc); return {before:Math.round(t.before),vat:Math.round(t.vat),grand:Math.round(t.grand),n:t.n}; }")
    assert t == {"before": 3000, "vat": 140, "grand": 3140, "n": 3}, f"ยอดรวม/VAT/สุทธิผิด: {t}"
    dt = drawer_text(page)
    assert "รวมเป็นเงิน" in dt and "ภาษีมูลค่าเพิ่ม" in dt and "รวมทั้งสิ้น" in dt, "totbox ไม่แสดงสุทธิ/VAT/รวม"
    # add/del line เดินจริง
    n0 = ev(page, "() => state.wizard.doc.lines.length")
    after(page, "() => addLine()")
    assert ev(page, "() => state.wizard.doc.lines.length") == n0 + 1, "เพิ่มรายการไม่ได้"
    after(page, "() => delLine(0)")
    assert ev(page, "() => state.wizard.doc.lines.length") == n0, "ลบรายการไม่ได้"
    return "3 VAT modes: none=1,000 · add=1,070 · included(NET)=1,070 · รวม สุทธิ3,000/VAT140/รวม3,140 · add/del ok"


def c_fn04(page):
    """[FN-04 · S-03 · BR-02] รายการเกินเพดานหมวด → เตือน + บังคับกรอกเหตุผล (ไม่ hard block · A-EXP-05)"""
    open_(page)
    after(page, "() => openCreate()")
    # travel cap 5000 · ใส่ 6000 → over
    after(page, """() => { state.wizard.step=3; state.wizard.doc.emp='E01'; state.wizard.doc.lines=[
      {date:'2569-08-28',cat:'travel',desc:'ตั๋วเครื่องบิน',qty:1,unit_price:6000,vat_mode:'add'}]; renderDrawerOnly(); }""")
    assert ev(page, "() => overCapLines(state.wizard.doc).length") == 1, "ไม่ตรวจจับรายการเกินเพดาน"
    assert ev(page, "() => overCapReasonsOk(state.wizard.doc)") is False, "ยังไม่กรอกเหตุผลแต่ผ่าน"
    dt = drawer_text(page)
    assert "เกินเพดานหมวด" in dt and "ต้องระบุเหตุผล" in dt, "ไม่เตือน+บังคับเหตุผลบนจอ"
    assert "ยังส่งได้" in dt, "over-cap ควรเป็น warn ไม่ใช่ hard block (A-EXP-05)"
    # ขั้นสุดท้าย ยังส่งไม่ได้จนกรอกเหตุผล
    after(page, "() => { state.wizard.step=5; renderDrawerOnly(); }")
    assert ev(page, "() => document.querySelector('#drawer .drawer-footer .btn-primary').disabled") is True, \
        "เกินเพดานยังไม่กรอกเหตุผลแต่ปุ่มส่งไม่ disabled"
    # กรอกเหตุผล → ส่งได้
    after(page, "() => { state.wizard.doc.lines[0].over_reason='ลูกค้าเร่งด่วน ผู้บริหารอนุมัติ'; renderDrawerOnly(); }")
    assert ev(page, "() => overCapReasonsOk(state.wizard.doc)") is True, "กรอกเหตุผลแล้วยัง reasonsOk=false"
    assert ev(page, "() => document.querySelector('#drawer .drawer-footer .btn-primary').disabled") in (False, None), \
        "กรอกเหตุผลแล้วปุ่มส่งยัง disabled"
    return "over-cap (travel 6,000>5,000): เตือน+บังคับเหตุผล · ยังไม่กรอก=ส่งไม่ได้ · กรอกแล้ว=ส่งได้"


def c_fn05(page):
    """[FN-05 · S-04 · BR-03] ไม่มีรายการ/ยอดรวม = 0 → ส่งอนุมัติไม่ได้"""
    open_(page)
    after(page, "() => openCreate()")
    after(page, "() => { state.wizard.step=5; state.wizard.doc.emp='E01'; renderDrawerOnly(); }")
    # ไม่มีรายการ → grand 0 → ปุ่มส่ง disabled
    assert ev(page, "() => Math.round(totals(state.wizard.doc).grand)") == 0, "ไม่มีรายการแต่ grand ไม่ใช่ 0"
    assert ev(page, "() => document.querySelector('#drawer .drawer-footer .btn-primary').disabled") is True, \
        "ไม่มีรายการแต่ปุ่มส่งไม่ disabled"
    # ยอดรวม = 0 (มีรายการ unit_price 0) → ยังส่งไม่ได้
    after(page, "() => { state.wizard.doc.lines=[{date:'2569-08-28',cat:'other',desc:'ฟรี',qty:1,unit_price:0,vat_mode:'none'}]; renderDrawerOnly(); }")
    assert ev(page, "() => document.querySelector('#drawer .drawer-footer .btn-primary').disabled") is True, \
        "ยอดรวม 0 แต่ปุ่มส่งไม่ disabled"
    # มียอด > 0 → ส่งได้
    after(page, "() => { state.wizard.doc.lines=[{date:'2569-08-28',cat:'other',desc:'x',qty:1,unit_price:500,vat_mode:'none'}]; renderDrawerOnly(); }")
    assert ev(page, "() => document.querySelector('#drawer .drawer-footer .btn-primary').disabled") in (False, None), \
        "มียอด > 0 แต่ปุ่มส่งยัง disabled"
    return "ว่าง/ยอด=0 → ปุ่มส่งอนุมัติ disabled · มียอด>0 → ส่งได้ (BR-03)"


def c_fn06(page):
    """[FN-06 · S-05 · BR-08] ตำแหน่ง/ศูนย์ต้นทุน ดึงจากตำแหน่ง ณ วันเบิก (snapshot จาก Movement)"""
    open_(page)
    wizard_to_step2(page, emp='E01')
    dt = drawer_text(page)
    e = ev(page, "() => emp('E01')")
    assert e["pos"] in dt and e["dept"] in dt and e["cc"] in dt, f"ขั้น 2 ไม่ดึงตำแหน่ง/แผนก/ศูนย์ต้นทุน: {e}"
    assert "ณ วันเบิก" in dt and "Movement" in dt, "ไม่ระบุ snapshot ณ วันเบิก (Movement)"
    # มุมมองเอกสารก็แสดง cc ณ วันเบิก
    after(page, "() => { closeDrawer(); openView('d2'); }")
    assert "ณ วันเบิก" in drawer_text(page), "detail view ไม่ระบุ ศูนย์ต้นทุน ณ วันเบิก"
    return "snapshot ณ วันเบิก: ตำแหน่ง/แผนก/ศูนย์ต้นทุน (CC-PROD-01) จาก Movement · แสดงทั้ง wizard + detail"


def c_fn12(page):
    """[FN-12 · S-13 · BR-03] แนบใบเสร็จ — หมวดที่นโยบายบังคับต้องแนบก่อนส่ง"""
    open_(page)
    after(page, "() => openCreate()")
    # travel = receiptRequired true → ขั้นแนบเอกสารเตือนหมวดบังคับ
    after(page, """() => { state.wizard.step=4; state.wizard.doc.lines=[
      {date:'2569-08-28',cat:'travel',desc:'x',qty:1,unit_price:400,vat_mode:'add'}]; renderDrawerOnly(); }""")
    assert ev(page, "() => JSON.stringify(receiptRequiredCats(state.wizard.doc))") == '["travel"]', \
        "หมวด travel (บังคับแนบ) ไม่ถูก resolve"
    dt = drawer_text(page)
    assert "บังคับแนบใบเสร็จก่อนส่ง" in dt and "เดินทาง" in dt, "ไม่เตือนหมวดบังคับแนบใบเสร็จ"
    # หมวดที่ไม่บังคับ (mat/other) → ไม่เตือน
    after(page, """() => { state.wizard.doc.lines=[
      {date:'2569-08-28',cat:'mat',desc:'x',qty:1,unit_price:400,vat_mode:'add'}]; renderDrawerOnly(); }""")
    assert ev(page, "() => receiptRequiredCats(state.wizard.doc).length") == 0, "หมวด mat ไม่บังคับแนบแต่ resolve ว่าบังคับ"
    return "หมวดบังคับแนบ: travel→เตือน 'เดินทาง' · mat→ไม่บังคับ (นโยบายหมวดจาก HR Config)"


def c_fn07(page):
    """[FN-07 · S-01] ส่งอนุมัติจาก wizard → สร้างใบเบิกใหม่ pending_approval + สาย DOA"""
    open_(page)
    n0 = ev(page, "() => EXP.docs.length")
    after(page, "() => openCreate()")
    after(page, """() => { state.wizard.doc.emp='E01'; state.wizard.doc.lines=[
      {date:'2569-08-28',cat:'travel',desc:'ตั๋วเครื่องบิน',qty:1,unit_price:10000,vat_mode:'add'}];
      state.wizard.step=5; renderDrawerOnly(); }""")
    after(page, "() => openSubmit()")
    assert ev(page, "() => state.modal.open && state.modal.type==='submit'"), "ขั้น 5 กดส่งแล้วไม่เปิด modal เลือกผู้อนุมัติ"
    # Bug A fix: ไม่มี auto-pick — ต้องเลือกผู้อนุมัติจริงครบทุก slot ก่อนปุ่มส่งจะ enable
    assert ev(page, "() => document.getElementById('submitConfirmBtn').disabled") is True, \
        "submit modal เพิ่งเปิด (ยังไม่เลือก) ปุ่มส่งต้อง disabled (ไม่ auto-pick)"
    pick_all_slots(page)
    assert ev(page, "() => document.getElementById('submitConfirmBtn').disabled") in (False, None), \
        "เลือกผู้อนุมัติครบทุก slot แล้วปุ่มส่งยัง disabled"
    after(page, "() => doSubmit()")
    assert ev(page, "() => EXP.docs.length") == n0 + 1, "ส่งอนุมัติแล้วใบเบิกไม่เพิ่ม"
    nd = ev(page, "() => EXP.docs[0]")
    assert nd["status"] == "pending_approval", f"ใบใหม่ไม่ใช่ pending_approval: {nd['status']}"
    assert len(nd["chain"]) == 2, f"grand 10,700 → ควรมีสาย 2 ขั้น (5k-50k) ได้ {len(nd['chain'])}"
    assert ev(page, "() => state.drawer.open") is False and ev(page, "() => state.modal.open") is False, \
        "ส่งแล้ว drawer/modal ไม่ปิด"
    return f"ส่งอนุมัติจาก wizard: ใบเบิกใหม่ pending_approval + สาย DOA 2 ขั้น ({n0}→{n0+1} ใบ)"


def c_fn08(page):
    """[FN-08 · S-08 · BR-04] DOA slot picker เลือกคนตามวงเงิน (ยอดต่างช่วง=สายต่าง) — ไม่ hardcode"""
    open_(page)
    # ยอดต่างช่วง = จำนวนขั้นสายอนุมัติต่างกัน (resolve ตามวงเงิน · ไม่ตายตัว 3-tier)
    s1 = ev(page, "() => resolveDoa(3000).steps.length")
    s2 = ev(page, "() => resolveDoa(30000).steps.length")
    s3 = ev(page, "() => resolveDoa(60000).steps.length")
    assert (s1, s2, s3) == (1, 2, 3), f"resolveDoa ตามวงเงินผิด (3k/30k/60k): {(s1, s2, s3)}"
    labels = ev(page, "() => [resolveDoa(3000).label, resolveDoa(30000).label, resolveDoa(60000).label]")
    assert len(set(labels)) == 3, f"ช่วงวงเงินควรต่างกันทั้ง 3: {labels}"
    # slot picker เป็นรายชื่อคนจริง · ไม่ hardcode (เลือกคนอื่นได้ → chain สะท้อนที่เลือก)
    after(page, "() => openSubmitDraft('d1')")   # d1 draft grand 3,210 → 1 slot
    assert ev(page, "() => document.querySelectorAll('#modalBackdrop .modal .slot-row').length") == 1, \
        "d1 (ยอด<5,000) ควรมี 1 slot"
    optok = ev(page, "() => { const s=window.__ss['slot-0']; return s && s.options.length===APPROVERS.length && s.options.every(o=>o.label && o.sub); }")
    assert optok, "slot picker ไม่ใช่รายชื่อผู้อนุมัติจริง (ขาดชื่อ/ตำแหน่ง)"
    # เลือกคนที่ต่างจาก default (index 3 = ปรีชา วัฒน์) → chain ผูกตามที่เลือก
    after(page, "() => ssPick('slot-0',3)")
    after(page, "() => doSubmit()")
    ch = ev(page, "() => findDoc('d1').chain")
    assert ev(page, "() => findDoc('d1').status") == "pending_approval", "เลือกครบแล้วไม่ส่งเข้า pending"
    assert ch[0]["name"] == "ปรีชา วัฒน์", f"ผู้อนุมัติที่บันทึกไม่ตรงกับที่เลือก (hardcode?): {ch}"
    return "DOA ตามวงเงิน: 3k=1ขั้น·30k=2·60k=3 (label ต่างกัน) · slot picker คนจริง · เลือกเอง→chain ผูกตาม (ไม่ hardcode)"


def c_fn11(page):
    """[FN-11 · S-11 · BR-05] แก้ยอดหลังส่ง → re-resolve สาย DOA เมื่อข้ามช่วงวงเงิน"""
    open_(page)
    after(page, "() => openSubmitDraft('d1')")   # d1 grand 3,210 → ช่วง 1 (1 ขั้น)
    grand1 = ev(page, "() => state.doaDraft.grand")
    slots1 = ev(page, "() => document.querySelectorAll('#modalBackdrop .modal .slot-row').length")
    after(page, "() => closeModal()")
    # แก้ยอด: เพิ่มรายการใหญ่ให้ข้ามช่วง (>50,000)
    after(page, "() => { findDoc('d1').lines.push({date:'2569-08-28',cat:'ent',desc:'จัดเลี้ยงใหญ่',qty:1,unit_price:60000,vat_mode:'add'}); }")
    after(page, "() => openSubmitDraft('d1')")   # re-resolve จากยอดใหม่
    grand2 = ev(page, "() => state.doaDraft.grand")
    slots2 = ev(page, "() => document.querySelectorAll('#modalBackdrop .modal .slot-row').length")
    assert slots1 == 1, f"ยอดเดิม (<5,000) ควร 1 ขั้น ได้ {slots1}"
    assert grand2 > grand1 and grand2 > 50000, f"ยอดใหม่ไม่มากขึ้น/ไม่ข้ามช่วง: {grand1}→{grand2}"
    assert slots2 == 3, f"ยอดข้ามช่วง (>50,000) ต้อง re-resolve เป็น 3 ขั้น ได้ {slots2}"
    return f"re-resolve: ยอด {round(grand1):,}→{round(grand2):,} (ข้ามช่วง) → สาย DOA 1→3 ขั้น (BR-05)"


def c_fn13(page):
    """[FN-13 · S-06 · BR-04] ผู้อนุมัติตีกลับ (บังคับเหตุผล) → ผู้เบิกแก้แล้วยื่นใหม่ได้"""
    open_(page)
    after(page, "() => setRole('mgr')")   # FIX-03: ตีกลับได้เฉพาะผู้อนุมัติ (DOA)
    after(page, "() => openView('d3')")   # pending_approval
    assert "ไม่อนุมัติ" in drawer_text(page), "ใบ pending ไม่มีปุ่มไม่อนุมัติ"
    after(page, "() => openModal('reject',{id:'d3'})")
    assert ev(page, "() => document.getElementById('rejectConfirmBtn').disabled") is True, "เหตุผลว่างแต่ปุ่มยืนยันไม่ disabled"
    # เหตุว่าง → doReject no-op
    after(page, "() => doReject('d3')")
    assert ev(page, "() => findDoc('d3').status") == "pending_approval", "เหตุว่างแต่ตีกลับผ่าน"
    # กรอกเหตุ → ปุ่มเปิด → ตีกลับ
    after(page, "() => { document.getElementById('m_reason').value='แนบใบเสร็จไม่ครบ'; onRejectReasonInput(); }")
    assert ev(page, "() => document.getElementById('rejectConfirmBtn').disabled") is False, "กรอกเหตุแล้วปุ่มยังปิด"
    after(page, "() => doReject('d3')")
    assert ev(page, "() => findDoc('d3').status") == "rejected", "ใส่เหตุแล้วไม่ตีกลับ"
    assert ev(page, "() => findDoc('d3').reason") == "แนบใบเสร็จไม่ครบ", "ไม่บันทึกเหตุตีกลับ"
    # ผู้เบิกแก้แล้วยื่นใหม่: reopen → draft → ส่งใหม่ได้
    after(page, "() => openView('d3')")
    assert "แก้ไขและยื่นใหม่" in drawer_text(page), "ใบตีกลับไม่มีปุ่มแก้ไขและยื่นใหม่"
    after(page, "() => doReopen('d3')")
    assert ev(page, "() => findDoc('d3').status") == "draft", "reopen แล้วไม่กลับเป็นร่าง"
    after(page, "() => openSubmitDraft('d3')")
    pick_all_slots(page)   # Bug A fix: ต้องเลือกผู้อนุมัติครบทุก slot ก่อน doSubmit จะ commit
    after(page, "() => doSubmit()")
    assert ev(page, "() => findDoc('d3').status") == "pending_approval", "แก้แล้วยื่นใหม่ไม่เข้า pending"
    return "ตีกลับ: เหตุว่าง=บล็อก · มีเหตุ→rejected+เก็บเหตุ · reopen→ร่าง · ยื่นใหม่→pending"


def c_fn14(page):
    """[FN-14 · S-07 · BR-10] ยกเลิกใบเบิกก่อนอนุมัติได้ (soft archive)"""
    open_(page)
    after(page, "() => openView('d1')")   # draft
    after(page, "() => openModal('cancel',{id:'d1'})")
    assert "soft archive" in modal_text(page), "confirm ยกเลิกไม่ระบุ soft archive"
    after(page, "() => doCancel('d1')")
    assert ev(page, "() => findDoc('d1').status") == "cancelled", "ยกเลิกแล้วสถานะไม่ cancelled"
    assert ev(page, "() => !!findDoc('d1')") is True, "ยกเลิกแล้ว record หาย (ไม่ใช่ soft archive)"
    return "ยกเลิกใบร่าง → cancelled · record คงอยู่ (soft archive)"


def c_fn09(page):
    """[FN-09 · S-09 · BR-06/BR-07] อนุมัติ → ออกเลข EXP-YYYY-NNNN + สำเนา + ยิง 7C (FC/EC)"""
    open_(page)
    after(page, "() => setRole('mgr')")   # FIX-03: อนุมัติได้เฉพาะผู้อนุมัติ (DOA)
    after(page, "() => openView('d3')")   # pending
    after(page, "() => openModal('approve',{id:'d3'})")
    mt = modal_text(page)
    assert "EXP-YYYY-NNNN" in mt and "7C" in mt and "CSQ_BRIEF_F101" in mt, "modal อนุมัติไม่ระบุออกเลข/7C ตาม CSQ_BRIEF (FIX-10)"
    after(page, "() => doApprove('d3')")
    d = ev(page, "() => findDoc('d3')")
    assert d["status"] == "approved", "อนุมัติแล้วสถานะไม่ approved"
    assert re.match(r"^EXP-2569-\d{4}$", d["code"]), f"ไม่ออกเลข EXP-YYYY-NNNN (4 หลัก): {d['code']}"
    assert all(s["status"] == "approved" for s in d["chain"]), "อนุมัติแล้วสายยังไม่ approved ครบ"
    toast = ev(page, "() => document.getElementById('toast').textContent")
    assert "7C" in toast and d["code"] in toast, f"toast ไม่ยืนยันออกเลข+7C: {toast}"
    return f"อนุมัติ → ออกเลข {d['code']} · บันทึกเข้า 7C ตาม CSQ_BRIEF_F101 · chain approved (ผู้อนุมัติ)"


def c_fn15(page):
    """[FN-15 · S-15 · BR-06] ดู PDF ใบเบิก (tab PDF Preview · a4) + ลายเซ็น/อนุมัติ (tab ลายเซ็น)"""
    open_(page)
    after(page, "() => openView('d2')")   # approved
    after(page, "() => setVtab('pdf')")
    dt = drawer_text(page)
    assert "ใบเบิกค่าใช้จ่าย" in dt and "รวมทั้งสิ้น" in dt, "tab PDF Preview ไม่มีเอกสาร a4"
    assert ev(page, "() => !!document.querySelector('#drawer .a4')"), "ไม่มี .a4 (A4 preview) ใน tab PDF"
    after(page, "() => setVtab('sign')")
    st = drawer_text(page)
    assert "สายอนุมัติ" in st, "tab ลายเซ็นไม่มีสายอนุมัติ"
    assert "สมพงษ์ อินทร์" in st and "อนุมัติแล้ว" in st, "tab ลายเซ็นไม่แสดงผู้อนุมัติ/สถานะ"
    return "tab PDF Preview (.a4) + tab ลายเซ็น (สายอนุมัติ + สถานะรายขั้น)"


def c_fn17(page):
    """[FN-17 · S-15] มุมมองเอกสารมี tabs รายละเอียด›PDF›ลายเซ็น›ประวัติ · เอกสารแนบอยู่ในแท็บรายละเอียด"""
    open_(page)
    after(page, "() => openView('d2')")
    tabs = ev(page, "() => [...document.querySelectorAll('#drawer .tabs .tab')].map(b=>b.textContent.trim())")
    assert tabs == ["รายละเอียด", "PDF Preview", "ลายเซ็น / อนุมัติ", "ประวัติ"], f"ลำดับ tabs ผิด: {tabs}"
    # เอกสารแนบต้องอยู่ในแท็บรายละเอียด (default)
    assert "เอกสารแนบ" in drawer_text(page), "เอกสารแนบไม่อยู่ในแท็บรายละเอียด"
    return "view tabs: รายละเอียด›PDF›ลายเซ็น›ประวัติ · เอกสารแนบในแท็บรายละเอียด"


def c_fn10(page):
    """[FN-10 · S-10 · BR-09] เลือกช่องทางจ่าย 4 (เงินเดือน/โอนตรง/PV/เงินสดย่อย·F091) → ส่งจ่าย (hook)
       petty/PV = จุดเชื่อม F091 (Feature List F101 'c') · display-only ไม่จ่ายเอง (PM/BA OQ-EXP-01)"""
    open_(page)
    wizard_to_step2(page, emp='E01')
    dt = drawer_text(page)
    for opt in ("ผ่านรอบเงินเดือน", "โอนตรง", "ใบสำคัญจ่าย", "เงินสดย่อย"):
        assert opt in dt, f"ขั้น 2 ไม่มีตัวเลือกช่องทางจ่าย: {opt}"
    # เปลี่ยนเป็นเงินสดย่อย (F091) → หน้าสรุปสะท้อน label
    after(page, "() => { state.wizard.doc.pay='petty'; state.wizard.step=5; renderDrawerOnly(); }")
    assert ev(page, "() => state.wizard.doc.pay") == "petty", "เปลี่ยนช่องทางจ่ายไม่ได้"
    assert "เงินสดย่อย" in drawer_text(page), "หน้าสรุปไม่สะท้อนช่องทาง เงินสดย่อย"
    # ใบอนุมัติแล้วมี payment hook + ปลายทางตามช่องทาง (display-only)
    after(page, "() => { closeDrawer(); openView('d2'); }")
    vt = drawer_text(page)
    assert "ส่งจ่ายผ่านเงินเดือน" in vt and "ปลายทาง" in vt, "ไม่มี payment hook/ปลายทาง บนใบอนุมัติ"
    return "ช่องทางจ่าย 4 (เงินเดือน/โอนตรง/PV/เงินสดย่อย·F091) · หน้าสรุป+ใบอนุมัติสะท้อน hook ปลายทาง"


def c_fn16(page):
    """[FN-16 · S-14 · BR-09] สถานะ 'จ่ายแล้ว' อ่านจากปลายทาง display-only — Expense ไม่จ่ายเอง"""
    open_(page)
    assert ev(page, "() => findDoc('d6').status") == "paid", "d6 ควรเป็นสถานะจ่ายแล้ว"
    after(page, "() => openView('d6')")
    dt = drawer_text(page)
    assert "โอนแล้ว" in dt, "ไม่แสดงสถานะจ่ายจากปลายทาง"
    assert "อ่านจากปลายทาง" in dt and "display-only" in dt, "ไม่ระบุ display-only จากปลายทาง"
    assert "Expense ไม่จ่าย" in dt, "ไม่ยืนยันว่า Expense ไม่จ่าย/ไม่ลงบัญชีเอง"
    return "สถานะจ่ายแล้ว display-only จากปลายทาง (เงินเดือน/การเงิน) · Expense ไม่จ่ายเอง"


def c_advance_clear(page):
    """[F101-c · OQ-EXP-01 · PM/BA 2026-09-10] เคลียร์เงินทดรอง หักลบอัตโนมัติ (soft-ref F103 · display-only)
       จุดเชื่อม: F101 หักยอดใบเบิกกับทดรองค้าง → โชว์ยอดจ่ายสุทธิ · ไม่ออก/ไม่ปรับทดรองเอง (นั่นคือ F103)"""
    open_(page)
    # d4 = ผู้เบิก E03 มีเงินทดรองค้าง mock 15,000 · officer เห็นเงินเต็ม (ไม่ mask)
    after(page, "() => { state.role='officer'; openView('d4'); }")
    dt = drawer_text(page)
    assert "เคลียร์เงินทดรอง" in dt, "ไม่แสดงบล็อกเคลียร์เงินทดรอง (จุดเชื่อม F103)"
    assert "F103" in dt and "display-only" in dt, "ไม่ระบุ soft-ref F103 · display-only"
    calc = ev(page, "() => { const a=advanceClear(findDoc('d4')); return {adv:a.adv, offset:a.offset, netPay:a.netPay, advRemain:a.advRemain, g:totals(findDoc('d4')).grand}; }")
    assert calc["adv"] == 15000, f"ทดรองค้าง mock ผิด: {calc['adv']}"
    assert calc["offset"] == min(15000, calc["g"]), f"offset ต้อง=min(ทดรอง,ยอดรวม): {calc}"
    assert abs(calc["netPay"] - (calc["g"] - calc["offset"])) < 0.01, f"หักลบยอดจ่ายสุทธิผิด: {calc}"
    assert calc["netPay"] >= 0 and calc["advRemain"] >= 0, f"ยอดสุทธิ/ทดรองคงค้างติดลบ: {calc}"
    # ใบที่ผู้เบิกไม่มีทดรอง (d1=E01) ต้องไม่มีบล็อกนี้ (ไม่ยัด hook มั่ว)
    after(page, "() => { closeDrawer(); state.role='admin'; openView('d1'); }")
    assert "เคลียร์เงินทดรอง" not in drawer_text(page), "ใบที่ไม่มีทดรองไม่ควรมีบล็อกเคลียร์"
    return f"เคลียร์ทดรอง: ค้าง ฿15,000 หักลบอัตโนมัติ → สุทธิ {calc['netPay']:.0f} (=ยอด{calc['g']:.0f}-offset{calc['offset']:.0f}) · ไม่มีทดรอง=ไม่มีบล็อก · display-only F103"


def c_role_scope(page):
    """[OQ-EXP-03 · PM/BA 2026-09-10] ขอบเขตการมองเห็น: ผู้เบิก/ธุรการ เห็น 'เฉพาะใบของตน' ·
       role เจ้าหน้าที่ (HR/Finance) เห็น 'ทั้งหมด' + เห็นเงินเต็ม แต่ไม่ใช่ผู้อนุมัติ (DOA)"""
    open_(page)
    total = ev(page, "() => EXP.docs.length")
    # admin (self=E01) เห็นเฉพาะใบของ E01
    adminDocs = ev(page, "() => { state.role='admin'; return visibleDocs().map(d=>d.emp); }")
    assert len(adminDocs) > 0 and all(e == 'E01' for e in adminDocs), f"ธุรการควรเห็นเฉพาะใบของตน (E01): {adminDocs}"
    assert len(adminDocs) < total, "ธุรการไม่ควรเห็นครบทุกใบ"
    # officer เห็นทั้งหมด + เงินเต็ม (ไม่ mask) + ไม่ใช่ผู้อนุมัติ
    offCount = ev(page, "() => { state.role='officer'; return visibleDocs().length; }")
    assert offCount == total, f"เจ้าหน้าที่ควรเห็นทั้งหมด ({total}) แต่เห็น {offCount}"
    offMask = ev(page, "() => { state.role='officer'; return maskM(99999, findDoc('d4')); }")
    assert "•" not in offMask, f"เจ้าหน้าที่ต้องเห็นเงินเต็ม (ไม่ mask): {offMask}"
    assert ev(page, "() => { state.role='officer'; return canApprove(); }") is False, "เจ้าหน้าที่ต้องไม่ใช่ผู้อนุมัติ (DOA)"
    # ธุรการ mask เงินใบคนอื่น (d3=E02)
    adminMaskOther = ev(page, "() => { state.role='admin'; return maskM(99999, findDoc('d3')); }")
    assert "•" in adminMaskOther, f"ธุรการต้อง mask เงินใบคนอื่น: {adminMaskOther}"
    # เชิงจอ: ตาราง list ของธุรการ render เฉพาะแถวของตน (assert what the eye sees)
    after(page, "() => { state.role='admin'; state.filters={search:'',status:'all'}; render(); }")
    rows = ev(page, "() => document.querySelectorAll('#view tbody tr').length")
    assert rows == len(adminDocs), f"แถวตารางธุรการ ({rows}) ไม่ตรง visibleDocs ({len(adminDocs)})"
    return f"scope: ธุรการเห็น {len(adminDocs)}/{total} (self · mask ใบคนอื่น · จอ {rows} แถว) · เจ้าหน้าที่เห็น {offCount}/{total} เต็ม · ไม่อนุมัติ"


# ═══════════════════════════════ GENERAL FN ═══════════════════════════════

def c_fn90(page):
    """[FN-90] list มีสถานะ (docPill) + ความคืบหน้าลายเซ็น + ค้นหา/filter + empty state"""
    open_(page)
    after(page, "() => { state.role='officer'; render(); }")   # เจ้าหน้าที่ (scope:all) — list-overview เห็นทุกใบ (OQ-EXP-03)
    assert ev(page, "() => document.querySelectorAll('#page-content .pill').length") >= 4, "list ไม่มี docPill สถานะ"
    assert ev(page, "() => document.querySelectorAll('#page-content .signprog').length") >= 4, "list ไม่มีความคืบหน้าลายเซ็น"
    # ค้นหาเจอ
    after(page, "() => { state.filters.search='สมชาย'; refreshView(); }")
    assert "สมชาย ใจดี" in pc_text(page), "ค้นหาชื่อผู้เบิกไม่เจอ"
    # ค้นหาไม่เจอ → empty state
    after(page, "() => { state.filters.search='zzzไม่มีจริง'; refreshView(); }")
    assert "ยังไม่มีใบเบิก" in pc_text(page), "ค้นไม่เจอแต่ไม่ขึ้น empty state"
    # filter สถานะ
    after(page, "() => { state.filters.search=''; state.filters.status='draft'; refreshView(); }")
    rows = ev(page, "() => document.querySelectorAll('#page-content .tbl tbody tr').length")
    assert rows == 1, f"filter สถานะ=ร่าง ควรเหลือ 1 แถว ได้ {rows}"
    return "list: docPill + ความคืบหน้าลายเซ็น + ค้นหา(เจอ/ไม่เจอ+empty) + filter สถานะ"


def c_fn91(page):
    """[FN-91] ตีกลับ/ยกเลิกผ่าน confirm เสมอ + soft archive"""
    open_(page)
    after(page, "() => openView('d1')")   # draft
    after(page, "() => openModal('cancel',{id:'d1'})")
    assert ev(page, "() => state.modal.type==='cancel'"), "ยกเลิกไม่ผ่าน confirm modal"
    # ยกเลิก confirm (closeModal) → ต้องไม่ถูกยกเลิก
    after(page, "() => closeModal()")
    assert ev(page, "() => findDoc('d1').status") == "draft", "ปิด confirm แล้วยัง cancelled (gate พัง)"
    # ยืนยันจริง → cancelled + record คงอยู่
    n0 = ev(page, "() => EXP.docs.length")
    after(page, "() => { openView('d1'); openModal('cancel',{id:'d1'}); }")
    after(page, "() => doCancel('d1')")
    assert ev(page, "() => findDoc('d1').status") == "cancelled", "confirm แล้วไม่ยกเลิก"
    assert ev(page, "() => EXP.docs.length") == n0, "soft archive แต่ record หาย"
    return "confirm gate: ปิด confirm=ไม่ยกเลิก · ยืนยัน=cancelled + record คงอยู่ (soft archive)"


def c_fn92(page):
    """[FN-92] field บังคับ validate + กัน double-submit + ชื่อ/ลำดับ wizard ล็อก"""
    open_(page)
    # ชื่อ/ลำดับ wizard ล็อก
    assert ev(page, "() => STEP_KEYS.length") == 5, "จำนวนขั้น wizard ไม่ใช่ 5 (ลำดับไม่ล็อก)"
    # field บังคับ: ขั้น 2 ไม่เลือกผู้เบิก → ปุ่มถัดไป disabled
    wizard_to_step2(page)
    assert ev(page, "() => document.querySelector('#drawer .drawer-footer .btn-primary').disabled") is True, \
        "ขั้น 2 ยังไม่เลือกผู้เบิกแต่ปุ่มถัดไปไม่ disabled"
    after(page, "() => { state.wizard.doc.emp='E01'; renderDrawerOnly(); }")
    assert ev(page, "() => document.querySelector('#drawer .drawer-footer .btn-primary').disabled") in (False, None), \
        "เลือกผู้เบิกแล้วปุ่มถัดไปยัง disabled"
    # กัน double-submit: doApprove สองครั้ง sync → ครั้งสองเป็น no-op (guard _busy)
    # (FIX-03: อนุมัติได้เฉพาะผู้อนุมัติ · d4 chain 2/3 approved → คลิกจบ chain = approved + ออกเลข)
    after(page, "() => { closeDrawer(); setRole('mgr'); openView('d4'); openModal('approve',{id:'d4'}); }")
    r = ev(page, """() => { const d=findDoc('d4'); doApprove('d4'); const c1=d.code; doApprove('d4');
      return { busy: state._busy, status: d.status, c1: c1, c2: d.code }; }""")
    assert r["busy"] is True, "กดอนุมัติแล้ว _busy ไม่ถูกล็อก (double-submit ไม่กัน)"
    assert r["status"] == "approved" and r["c1"] == r["c2"], f"เรียกอนุมัติซ้ำเปลี่ยน state (double-submit): {r}"
    return "validate: ขั้น 2 ผู้เบิกบังคับ (ปุ่ม disabled) · wizard 5 ขั้นล็อก · double-submit guard (_busy)"


def c_fn93(page):
    """[FN-93] audit บันทึกทุก create/แก้/อนุมัติ/ยกเลิก (แท็บประวัติ · append-only)"""
    open_(page)
    after(page, "() => openView('d2')")   # approved · มี audit trail
    after(page, "() => setVtab('history')")
    dt = drawer_text(page)
    assert "ประวัติ" in dt and "append-only" in dt, "แท็บประวัติไม่ระบุ append-only"
    assert "อนุมัติ · ออกเลข EXP-2569-0001" in dt and "ยื่นคำขอ" in dt, "audit ไม่บันทึกยื่น+อนุมัติ"
    # ใบที่ยังไม่มี audit trail → fallback รายการสร้าง (ยังมีประวัติ)
    after(page, "() => { closeDrawer(); openView('d3'); setVtab('history'); }")
    assert "สร้างใบเบิก" in drawer_text(page), "ใบไม่มี audit ควร fallback รายการสร้าง"
    return "audit append-only: d2 มี ยื่น+อนุมัติ·ออกเลข · ใบอื่น fallback รายการสร้าง"


def c_fn94(page):
    """[FN-94 · BR-10 · FIX-03 · OQ-EXP-03] masking RESTRICTED ทิศถูก + สอดคล้อง scope:
       ผู้เบิก(admin·self=E01·scope:self) เห็น 'เฉพาะใบตน' เต็ม · กลไก mask ยังกันยอดใบคนอื่น (maskM · defense-in-depth) ·
       ผู้อนุมัติ(mgr)/เจ้าหน้าที่(officer) scope:all เห็นทั้งหมดเต็ม (mask:false)"""
    open_(page)
    # seed = admin (ผู้เบิก/ธุรการ · self=E01 · scope:self) → ลิสต์เห็นเฉพาะใบตน (d1/d2=E01) เต็ม · ไม่เห็นใบคนอื่น
    assert ev(page, "() => state.role") == "admin", "seed role ไม่ใช่ admin"
    pc = pc_text(page)
    assert "•••••" not in pc, "admin เห็นเฉพาะใบตน (self) — ในลิสต์ต้องไม่มียอด mask"
    assert "66,340" not in pc, "admin ไม่ควรเห็นยอดใบ d4 (E03 — คนอื่น · นอก scope)"
    assert ev(page, "() => document.querySelectorAll('#page-content .tbl tbody tr').length") == ev(page, "() => visibleDocs().length"), \
        "ลิสต์ admin ไม่ตรง visibleDocs (scope:self)"
    # กลไก mask ยังกันยอดใบคนอื่นสำหรับ admin (maskM ระดับฟังก์ชัน · defense-in-depth ถ้าเปิดใบนอก scope)
    assert "•" in ev(page, "() => maskM(66340, findDoc('d4'))"), "กลไก mask ของ admin ต้องปิดยอดใบคนอื่น"
    assert "•" not in ev(page, "() => maskM(1800, findDoc('d2'))"), "admin เปิดใบตน (E01) ต้องเห็นเต็ม"
    # เปิดใบของตน (d2=E01) → เห็นยอดเต็ม
    after(page, "() => openView('d2')")
    assert "•••••" not in drawer_text(page), "ผู้เบิกเปิดใบของตน (E01) ควรเห็นยอดเต็ม"
    after(page, "() => closeDrawer()")
    # ผู้อนุมัติ (mgr · FIX-03 mask:false) → เห็นเงินเต็มทุกใบ (อนุมัติตามวงเงิน)
    after(page, "() => setRole('mgr')")
    m = pc_text(page)
    assert "•••••" not in m, "ผู้อนุมัติ(mgr) ต้องเห็นเงินเต็ม — masking ห้ามกลับด้าน (FIX-03)"
    assert "66,340" in m, "ผู้อนุมัติ(mgr) ควรเห็นยอด d4 (66,340) เพื่ออนุมัติตามวงเงิน"
    after(page, "() => openView('d4')")
    assert "66,340" in drawer_text(page) and "•••••" not in drawer_text(page), \
        "ผู้อนุมัติเปิดใบรออนุมัติต้องเห็นยอดเต็ม"
    return "masking+scope: admin เห็นเฉพาะใบตน(เต็ม)·กลไก mask กันใบคนอื่น · mgr/officer เห็นทั้งหมดเต็ม (FIX-03)"


# ═══════════════════ NEGATIVE (unsupported ×7, rendered → absent) ═══════════════════

NEG_JS = r"""
() => {
  let html='';
  state.role='admin';
  // หน้า list (มี unsupportedNote)
  html += pageHTML();
  // wizard ทุกขั้น (มี line editor + upload zone + สรุป DOA)
  state.wizard = { step:1, doc:{ emp:'E01', date:'2569-08-31', pay:'payroll',
    lines:[{date:'2569-08-28',cat:'travel',desc:'x',qty:1,unit_price:6000,vat_mode:'add'}],
    endbill:{enabled:false,mode:'amount',value:0} } };
  state.drawer = { open:true, mode:'wizard', recordId:null, step:1 };
  for(let s=1;s<=5;s++){ state.wizard.step=s; html += drawerHTML(); }
  // view drawer ทุกแท็บ (over-cap · approved · paid)
  ['d4','d2','d6'].forEach(id=>{
    state.drawer = { open:true, mode:'view', recordId:id };
    ['detail','pdf','sign','history'].forEach(tb=>{ state.view={tab:tb,id}; html += drawerHTML(); });
  });
  // modals ทุกชนิด
  state.doaDraft = { picks:{}, grand:60000 };
  [['submit',{}],['approve',{id:'d3'}],['reject',{id:'d3'}],['cancel',{id:'d1'}]].forEach(m=>{
    state.modal = { open:true, type:m[0], data:m[1] }; html += modalHTML();
  });
  const box=document.createElement('div'); box.innerHTML=html;
  const acts=[...box.querySelectorAll('button,[onclick]')].filter(el=>{
    const h=(el.getAttribute('onclick')||'').replace(/\s/g,'');
    return !/^event\.stopPropagation\(\)$/.test(h);
  }).map(el=>({ txt:(el.textContent||'').replace(/\s+/g,' ').trim(), on:(el.getAttribute('onclick')||'') }));
  return {
    acts,
    fileInputs: box.querySelectorAll('input[type=file]').length,
    hasDisplayOnly: /display-only/.test(html),
    hasReadHook: /อ่านจากปลายทาง/.test(html),
    hasNotPay: /Expense ไม่จ่าย/.test(html),
  };
}
"""


def c_unsupported(page):
    """[NEG · unsupported ×7] เรนเดอร์ทุก affordance จริงแล้ว assert 'ไม่มี' ของห้ามมี (FN-40-equiv)"""
    open_(page)
    r = ev(page, NEG_JS)
    acts = r["acts"]

    def hit(pat):
        rx = re.compile(pat, re.I)
        return [a for a in acts if rx.search(a["txt"]) or rx.search(a["on"])]

    assert len(acts) > 12, f"เก็บ affordance ได้น้อยผิดปกติ ({len(acts)}) — surfaces อาจไม่เรนเดอร์"

    # 1) จ่ายเงินจริง/โอน/ตัดจ่าย & GL posting — payment เป็น hook display-only เท่านั้น
    v1 = hit(r"จ่ายเงิน|โอนเงิน|ตัดจ่าย|ตั้งเบิก|เบิกจ่าย|ชำระเงิน|ลงบัญชี|บันทึกบัญชี|ตั้งหนี้|post.?gl|glPost|payReal|payout|disburse|doPay")
    assert not v1, f"[neg1] พบ affordance จ่ายเงินจริง/GL: {v1[:3]}"
    assert r["hasDisplayOnly"] and r["hasReadHook"] and r["hasNotPay"], \
        "[neg1] payment ควรเป็น display-only อ่านจากปลายทาง (Expense ไม่จ่ายเอง)"

    # 2) เบี้ยเลี้ยง / ค่าน้ำมันต่อกิโลเมตร (mileage / per diem)
    v2 = hit(r"เบี้ยเลี้ยง|ต่อกิโล|กิโลเมตร|mileage|per.?diem|allowance")
    assert not v2, f"[neg2] พบ affordance เบี้ยเลี้ยง/mileage: {v2[:3]}"

    # 3) คำขออนุมัติเดินทางล่วงหน้า (travel request/authorization)
    v3 = hit(r"ขออนุมัติเดินทาง|คำขอเดินทาง|travel.?request|travelAuth|authoriz")
    assert not v3, f"[neg3] พบ affordance คำขออนุมัติเดินทาง: {v3[:3]}"

    # 4) ระบบเงินสดย่อย/ออกเงินทดรองเต็มรูป = อยู่ที่ F091/F103 — F101 ต่อ "แค่จุดเชื่อม" (PM/BA OQ-EXP-01 2026-09-10)
    #    ห้ามมี affordance สร้าง/ออก/จัดการ ทดรอง-เงินสดย่อย (ระบบของ F091/F103) ·
    #    "เคลียร์เงินทดรอง หักลบอัตโนมัติ" ที่เพิ่ม = display-only hook (div ไม่ใช่ปุ่ม) → allowed (ตรวจ positive ที่ E30)
    v4 = hit(r"ออกเงินทดรอง|สร้างทดรอง|ขอทดรอง|จัดการทดรอง|จัดการเงินสดย่อย|เบิกชดเชย|ตรวจนับเงิน|replenish|imprest|issueAdvance|createAdvance|manageAdvance|newAdvance")
    assert not v4, f"[neg4] พบ affordance ระบบทดรอง/เงินสดย่อยเต็มรูป (ควรอยู่ F091/F103): {v4[:3]}"

    # 5) หลายสกุลเงิน (multi-currency)
    v5 = hit(r"สกุลเงิน|หลายสกุล|เลือกสกุล|currency|อัตราแลกเปลี่ยน|exchangeRate|USD|EUR")
    assert not v5, f"[neg5] พบ affordance หลายสกุลเงิน: {v5[:3]}"

    # 6) อ่านใบเสร็จอัตโนมัติ (OCR) — มีแต่ข้อความปฏิเสธ ไม่มีปุ่ม/ทางลัด
    v6 = hit(r"\bOCR\b|อ่านใบเสร็จอัตโนมัติ|สแกนใบเสร็จ|scanReceipt|autoRead")
    assert not v6, f"[neg6] พบ affordance OCR: {v6[:3]}"

    # 7) สร้าง/แก้เพดานหมวด/นโยบายเอง — อ่านจาก HR Config (#107)
    v7 = hit(r"สร้างเพดาน|แก้เพดาน|แก้ไขเพดาน|ตั้งเพดาน|จัดการหมวด|สร้างหมวด|เพิ่มหมวด|แก้นโยบาย|createCap|editCap|manageCat|editPolicy")
    assert not v7, f"[neg7] พบ affordance สร้าง/แก้เพดานหมวด/นโยบาย: {v7[:3]}"

    assert r["fileInputs"] == 0, "[neg] พบ input[type=file] จริง (upload ควรเป็น mock zone)"
    return f"unsupported 7/7 absent ({len(acts)} affordance ตรวจ · payment display-only · upload=mock)"


# ═══════════════════ DSP · BASE-KIT overlay/combobox probes (W5-HR recurring) ═══════════════════

def c_modal_over_drawer(page):
    """[DSP-01 · UI-REG] modal เปิดในลิ้นชัก (อนุมัติ) ต้องอยู่เหนือ drawer (z portal>drawer) — F-HR-RECRUIT precedent"""
    open_(page)
    after(page, "() => openView('d3')")               # drawer เปิด (pending)
    after(page, "() => openModal('approve',{id:'d3'})")  # modal เปิดทับ drawer
    viol = ev(page, JS_MODAL_UNDER_DRAWER)
    assert viol == [], f"modal จมใต้ drawer: {viol}"
    mz = ev(page, "() => parseInt(getComputedStyle(document.querySelector('.modal-backdrop')).zIndex,10)")
    dz = ev(page, "() => parseInt(getComputedStyle(document.querySelector('.drawer')).zIndex,10)")
    assert mz > dz, f"modal z({mz}) ต้อง > drawer z({dz})"
    # ยังเปิด submit modal จาก wizard drawer ก็ต้องเหนือ
    after(page, "() => { closeModal(); closeDrawer(); openCreate(); }")
    after(page, "() => { state.wizard.doc.emp='E01'; state.wizard.doc.lines=[{date:'2569-08-28',cat:'travel',desc:'x',qty:1,unit_price:400,vat_mode:'add'}]; state.wizard.step=5; renderDrawerOnly(); }")
    after(page, "() => openSubmit()")
    assert ev(page, JS_MODAL_UNDER_DRAWER) == [], "submit modal จมใต้ wizard drawer"
    return f"DSP-01: modal เหนือ drawer (z {mz}>{dz}) · ทั้ง approve + submit modal"


def c_overlay_stack(page):
    """[UI] ไม่มี element แปลกปลอมวาดทับ overlay (drawer+modal เปิดพร้อมกัน)"""
    open_(page)
    after(page, "() => openView('d3')")
    after(page, "() => openModal('approve',{id:'d3'})")
    viol = ev(page, JS_OVERLAY_STACK)
    assert viol == [], f"มี element วาดทับ overlay: {viol[:4]}"
    return "overlay stack สะอาด (ไม่มี shell/sticky ทะลุ drawer/modal)"


def c_static_css(page):
    """[UI] CSS var ที่ใช้แต่ไม่ประกาศ (ต้นตอ z-index หายเงียบ)"""
    open_(page)
    # --shellbar-h ใช้เฉพาะแบบมี fallback: var(--shellbar-h, 52px) → optional ไม่ใช่ var หาย (precedent F-HR-WELFARE/TRAIN)
    BENIGN_VARS = {"--shellbar-h"}
    missing = [v for v in ev(page, JS_CSSVAR) if v not in BENIGN_VARS]
    assert missing == [], f"CSS var ใช้แต่ไม่ประกาศ (ไม่มี fallback): {missing}"
    return "CSS var ครบ (z-index scale --z-* ประกาศครบ · --shellbar-h benign fallback-only)"


def c_affordance(page):
    """[UI] ของที่มี onclick ต้องมี cursor:pointer (กดได้แต่ไม่มีสัญญาณ = base-kit bug)"""
    open_(page)
    a1 = ev(page, JS_AFFORDANCE)
    after(page, "() => openCreate()")
    a2 = ev(page, JS_AFFORDANCE)
    after(page, "() => { closeDrawer(); openView('d4'); }")
    a3 = ev(page, JS_AFFORDANCE)
    bad = (a1 or []) + (a2 or []) + (a3 or [])
    assert bad == [], f"clickable แต่ไม่มี cursor:pointer: {bad[:5]}"
    return "affordance: ทุกจุดคลิกได้มี cursor:pointer (list + wizard + view)"


def c_no_garbage_text(page):
    """[UI-REG · §C3.8] ไม่มี NaN/undefined/null/[object Object]/Invalid Date รั่วเป็นข้อความบนจอ"""
    open_(page)
    assert_no_garbage_text(page, scope="#page-content")
    # wizard ทุกขั้น (doc มีรายการ)
    after(page, "() => openCreate()")
    after(page, "() => { state.wizard.doc.emp='E01'; state.wizard.doc.lines=[{date:'2569-08-28',cat:'travel',desc:'x',qty:1,unit_price:6000,vat_mode:'add'}]; renderDrawerOnly(); }")
    for s in range(1, 6):
        after(page, "() => { state.wizard.step=%d; renderDrawerOnly(); }" % s)
        assert_no_garbage_text(page, scope="#drawer")
    # view drawer ทุกแท็บ (approved/paid/over-cap)
    for did in ("d2", "d6", "d4"):
        after(page, "() => { closeDrawer(); openView('%s'); }" % did)
        for tb in ("detail", "pdf", "sign", "history"):
            after(page, "() => setVtab('%s')" % tb)
            assert_no_garbage_text(page, scope="#drawer")
    # modals
    after(page, "() => { closeDrawer(); openView('d3'); openModal('approve',{id:'d3'}); }")
    assert_no_garbage_text(page, scope="#modalBackdrop")
    after(page, "() => { closeModal(); openModal('reject',{id:'d3'}); }")
    assert_no_garbage_text(page, scope="#modalBackdrop")
    return "ไม่มี garbage text — กวาด list + wizard ×5 ขั้น + view ×3 ใบ×4 แท็บ + 2 modal"


def c_combo_closes(page):
    """[DSP-02a · UI-REG] wizemp: เลือกผู้เบิก → dropdown ปิด · ไม่เด้งกางใหม่จาก focus-restore (#29)

    บั๊กเดิม (BASE-KIT): onSelect→render() แล้ว focus-restore เด้งโฟกัสกลับเข้า ss-input →
    onfocus=ssOpen เปิด dropdown ซ้ำ. fix = ssBlurActive() ก่อน renderDrawerOnly (initSelects wizemp).
    """
    open_(page)
    wizard_to_step2(page)
    assert ev(page, "() => !!(window.__ss && window.__ss['wizemp'])"), "wizemp ไม่ถูก init"
    # (1) sync helper กลาง uikit: เลือกแล้วต้องปิดทันที + input โชว์ค่า + open=false
    r = assert_combobox_closes_after_select(page, "wizemp", 0)
    assert ev(page, "() => !!state.wizard.doc.emp"), "เลือกผู้เบิกแล้ว doc.emp ไม่ถูกตั้ง (onSelect ไม่ทำงาน)"
    # (2) real-flow: focus ss-input ค้าง → ssPick → รอ focus-restore rAF → dropdown ต้องยังปิด
    wizard_to_step2(page)
    ev(page, "() => { const i=document.getElementById('ss-input-wizemp'); if(i){ i.focus(); ssOpen('wizemp'); } ssPick('wizemp',0); }")
    page.evaluate(_RAF_SETTLE)
    st = ev(page, """() => ({
      open:(window.__ss['wizemp']||{}).open,
      listHidden:(()=>{const l=document.getElementById('ss-list-wizemp');return l?l.classList.contains('hidden'):null;})(),
      aeIsSs:!!(document.activeElement&&document.activeElement.classList&&document.activeElement.classList.contains('ss-input'))
    })""")
    assert st["open"] is False, f"[DSP-02a] เลือกแล้ว dropdown เด้งกางใหม่หลัง focus-restore (open={st['open']})"
    assert st["listHidden"] is True, "[DSP-02a] list ไม่ปิดหลัง focus-restore (reopen-after-select)"
    assert st["aeIsSs"] is False, "[DSP-02a] focus เด้งกลับเข้า ss-input (fix ไม่ได้ blur ก่อน render)"
    return f"DSP-02a wizemp: เลือกแล้วปิด (sync + หลัง focus-restore rAF) · doc.emp ติด · input='{str(r['inputValue'])[:14]}'"


def c_modal_no_autoopen(page):
    """[DSP-02b · UI-REG] submit modal เปิด → ไม่มี combobox (slot picker) กาง dropdown เอง (trapFocus auto-open)

    บั๊กเดิม (BASE-KIT): trapFocus auto-focus ช่องแรกของ modal ถ้าเป็น ss-input → onfocus=ssOpen เปิด
    dropdown เองตอน modal โผล่. fix = guardOverlayAutoCombo rAF ปิดคืนหลัง trapFocus.
    """
    open_(page)
    after(page, "() => openSubmitDraft('d1')")   # submit modal · slot-0 = ช่องแรก
    page.evaluate(_RAF_SETTLE)   # รอ trapFocus focus → guardOverlayAutoCombo blur/ปิด
    st = ev(page, """() => ({
      modalOpen: state.modal.open===true && state.modal.type==='submit',
      slot0Open: (window.__ss && window.__ss['slot-0']) ? window.__ss['slot-0'].open : null,
      listHidden: (()=>{const l=document.getElementById('ss-list-slot-0');return l?l.classList.contains('hidden'):null;})(),
      aeIsSs: !!(document.activeElement&&document.activeElement.classList&&document.activeElement.classList.contains('ss-input'))
    })""")
    assert st["modalOpen"], "submit modal ไม่เปิด"
    assert st["slot0Open"] is False, f"[DSP-02b] slot-0 กาง dropdown เองตอน modal เปิด (open={st['slot0Open']})"
    assert st["listHidden"] is True, "[DSP-02b] #ss-list-slot-0 ไม่ hidden ตอน modal เพิ่งเปิด"
    assert st["aeIsSs"] is False, "[DSP-02b] activeElement ยังเป็น ss-input (guard ไม่ได้ blur)"
    auto = modal_autoopens_comboboxes(page)
    assert auto == [], f"[DSP-02b] มี combobox กาง dropdown เองใน submit modal: {auto}"
    return "DSP-02b: submit modal เปิด → slot picker ไม่กางเอง (open=false·list hidden·blur·helper สะอาด)"


# ═══════════════ USER-FOUND BUG PROBES (§C3.8 · ตัววัดใหม่ที่ gate เดิมมองไม่เห็น) ═══════════════

def c_overlay_cleared(page):
    """[BUG-6 · UI-REG] backdrop/overlay ไม่ค้างหลังปิด drawer/modal — คลิกเดียวจบ (ไม่ต้องคลิกซ้ำ)

    บั๊กเดิม: closeDrawer/closeModal ถอด .is-open + ตั้ง state หลัง timer แต่ไม่ render() →
    ลิ้นชักที่ปิดแล้ว pointer-events:auto ระหว่าง slide-out ดักคลิกแรก. fix: .drawer:not(.is-open)
    pointer-events:none + render() หลัง transition (clear DOM). ไม่แตะ DSP-01/02 · Esc chain.
    """
    open_(page)
    # (a) ปิด drawer → ไม่มี overlay ปิดแล้วดักคลิกกลางจอ + DOM ลิ้นชักถูกล้าง
    after(page, "() => openView('d3')")
    assert ev(page, "() => state.drawer.open") is True, "openView ไม่เปิด drawer"
    after(page, "() => closeDrawer()")
    assert_overlay_cleared_after_close(page, note="ปิด drawer")
    assert ev(page, "() => document.getElementById('drawer').innerHTML.trim()===''") is True, \
        "ปิด drawer แล้ว DOM ลิ้นชักเก่ายังค้าง (ไม่ได้ render ล้าง)"
    # (b) modal เหนือ drawer: ปิด modal → modal ไม่บัง · drawer ยังเปิด (ไม่ถูก clobber)
    after(page, "() => openView('d3')")
    after(page, "() => openModal('approve',{id:'d3'})")
    after(page, "() => closeModal()")
    assert_overlay_cleared_after_close(page, note="ปิด modal เหนือ drawer")
    assert ev(page, "() => state.drawer.open") is True, "ปิด modal แล้ว drawer ต้องยังเปิด"
    assert ev(page, "() => state.modal.open") is False, "ปิด modal แล้ว state.modal ต้องปิด"
    return "backdrop cleared: ปิด drawer→คลิกกลางถึงหน้าเพจ+DOM ล้าง · ปิด modal เหนือ drawer→drawer คงเปิด"


def _click_modal_confirm(page):
    """คลิกปุ่มยืนยันใน modal-foot (ตัวที่ไม่ใช่ .btn-ghost = ไม่ใช่ 'ยกเลิก') → คืนข้อความปุ่มที่กด"""
    return ev(page, """() => { const b=document.querySelector('#modalBackdrop .modal-foot .btn:not(.btn-ghost)');
      if(b){ b.click(); return (b.textContent||'').replace(/\\s+/g,' ').trim(); } return null; }""")


def c_overlay_after_confirm(page):
    """[FN-09/FN-13/FN-14 · BUG-B · UI-REG] backdrop เคลียร์หลัง confirm action (อนุมัติ/ตีกลับ/ยกเลิก) — คลิกเดียวจบ

    บั๊กเดิม (user-found 2026-09-09): doApprove/doReject/doCancel เรียกแค่ closeModal() → view-drawer +
    drawerBackdrop (is-open · pe:auto) ค้างบังทั้งจอ ผู้ใช้ต้องคลิกอีกครั้ง. fix: ทั้งสามเรียก
    closeModal(); closeDrawer(); render(); (mirror doSubmit). ตัววัดเดิม (c_overlay_cleared/BUG-6)
    ตรวจแค่ปิดด้วย X/backdrop-click — ไม่เดินผ่าน confirm action.
    """
    # (a) อนุมัติ (pending d3) → กดยืนยัน 'อนุมัติ' → backdrop เคลียร์ทันที
    open_(page)
    after(page, "() => setRole('mgr')")   # FIX-03: อนุมัติเฉพาะผู้อนุมัติ
    after(page, "() => openView('d3')")
    after(page, "() => openModal('approve',{id:'d3'})")
    lbl_a = _click_modal_confirm(page)
    settle(page)
    assert ev(page, "() => findDoc('d3').status") == "approved", f"กดยืนยันอนุมัติแล้วสถานะไม่ approved (ปุ่ม='{lbl_a}')"
    assert_overlay_cleared_after_confirm_action(page, note="อนุมัติ d3")

    # (b) ตีกลับ (pending d4) → กรอกเหตุ → กดยืนยันตีกลับ → backdrop เคลียร์
    open_(page)
    after(page, "() => setRole('mgr')")   # FIX-03: ตีกลับเฉพาะผู้อนุมัติ
    after(page, "() => openView('d4')")
    after(page, "() => openModal('reject',{id:'d4'})")
    after(page, "() => { document.getElementById('m_reason').value='เอกสารแนบไม่ครบ'; onRejectReasonInput(); }")
    lbl_b = _click_modal_confirm(page)
    settle(page)
    assert ev(page, "() => findDoc('d4').status") == "rejected", f"กดยืนยันตีกลับแล้วสถานะไม่ rejected (ปุ่ม='{lbl_b}')"
    assert_overlay_cleared_after_confirm_action(page, note="ตีกลับ d4")

    # (c) ยกเลิก (draft d1) → กดยืนยันยกเลิก → backdrop เคลียร์
    open_(page)
    after(page, "() => openView('d1')")
    after(page, "() => openModal('cancel',{id:'d1'})")
    lbl_c = _click_modal_confirm(page)
    settle(page)
    assert ev(page, "() => findDoc('d1').status") == "cancelled", f"กดยืนยันยกเลิกแล้วสถานะไม่ cancelled (ปุ่ม='{lbl_c}')"
    assert_overlay_cleared_after_confirm_action(page, note="ยกเลิก d1")
    return "confirm action เคลียร์ overlay: อนุมัติ/ตีกลับ/ยกเลิก → backdrop ไม่ค้าง (pe:none · กลางจอถึงหน้าเพจ)"


def c_footer_actions(page):
    """[BUG-5 · UI-REG] ปุ่ม footer (ไม่อนุมัติ/อนุมัติ ฯลฯ) กดได้จริง · payment card ไม่ pin ทับ footer

    บั๊กเดิม: SEC() คืน HTML เกิน </div> ดัน payment card หลุด .drawer-body + เบียด .drawer-footer
    ออกนอก .drawer-panel → ปุ่ม action ต่ำกว่าจอ กดไม่ได้. fix: SEC call เป็น .sec well-formed.
    """
    open_(page)
    after(page, "() => setRole('mgr')")   # FIX-03: ปุ่มอนุมัติ/ไม่อนุมัติ เฉพาะผู้อนุมัติ
    after(page, "() => openView('d3')")   # pending → footer มี ไม่อนุมัติ/อนุมัติ
    settle(page)
    r = assert_footer_actions_hittable(page, note="d3 pending")
    labels = ev(page, "() => [...document.querySelectorAll('#drawer .drawer-footer .btn')].map(b=>b.textContent.trim())")
    joined = ' '.join(labels)
    assert 'อนุมัติ' in joined and 'ไม่อนุมัติ' in joined, f"footer ไม่มีปุ่มอนุมัติ/ไม่อนุมัติ: {labels}"
    # payment card 'สถานะการจ่าย' ต้องอยู่ใน drawer-body (ไม่หลุด)
    assert ev(page, "() => { const s=[...document.querySelectorAll('#drawer .drawer-body .sec')].find(x=>/สถานะการจ่าย/.test(x.textContent)); return !!s; }") is True, \
        "payment card ไม่อยู่ใน .drawer-body (HTML ผิดรูปดันหลุด)"
    return f"footer actions hittable: {labels} · payment card position={r['payPos']} (ใน drawer-body)"


def c_stepper_wellformed(page):
    """[BUG-3 · UI-REG] wizard stepper 5 ขั้นเรนเดอร์สะอาดที่ 1290 (ไม่มี style base-kit รั่วทับ)

    บั๊กเดิม: base-kit .step-dot (variant .stepper-row 30px วงกลมเทา) รั่วทับ STEPH .step-dot →
    item ได้ height:30/bg เทา/ขอบ/radius:50% คลุม label. fix: scope '.stepper .step-dot' + reset.
    """
    open_(page)
    after(page, "() => openCreate()")
    r = assert_stepper_well_formed(page, note="create wizard @1290")
    return f"stepper well-formed: 5 ขั้น widths={r['widths']} (bg โปร่ง·ไม่มีขอบ·วงกลม·กว้างเท่ากัน)"


def c_filter_inside_card(page):
    """[BUG-2 · UI-REG] filter row อยู่ในการ์ด มี gutter (ไม่ล้น/ชิดขอบ) + ปุ่มล้างตัวกรอง"""
    open_(page)
    r = assert_filter_inside_card(page, note="list")
    assert "ล้างตัวกรอง" in pc_text(page), "ไม่มีปุ่มล้างตัวกรอง"
    return f"filter inside card: gutter L{r['leftGutter']}/R{r['rightGutter']}px · มีปุ่มล้างตัวกรอง"


def c_submit_gate(page):
    """[FN-08 · UX-DOA] ส่งอนุมัติไม่ auto-pick ผู้อนุมัติ + ต้องเลือกจริงครบทุก slot ก่อนส่ง (Bug A)

    บั๊ก (user-found 2026-09-09): initSelects PRE-FILL picks[i] ด้วยผู้อนุมัติที่ระบบแนะนำ → ปุ่มส่ง
    ENABLED ตั้งแต่เปิด modal ทั้งที่ช่อง slot ดูว่าง → กดส่งได้ทันทีโดยได้คน "ที่ระบบเลือกให้".
    fix: ไม่ prefill — slot เปิดมาว่างจริง (picks={}), ปุ่ม disabled จนผู้ใช้เลือกครบทุก slot.
    """
    open_(page)
    n0 = ev(page, "() => EXP.docs.length")
    # wizard ยอดใหญ่ (>50,000) → resolveDoa 3 slot → ทดสอบ "ต้องเลือกครบทุก slot" ได้จริง
    after(page, "() => openCreate()")
    after(page, """() => { state.wizard.doc.emp='E01'; state.wizard.doc.lines=[
      {date:'2569-08-28',cat:'ent',desc:'จัดเลี้ยงใหญ่',qty:1,unit_price:60000,vat_mode:'add'}];
      state.wizard.step=5; renderDrawerOnly(); }""")
    after(page, "() => openSubmit()")
    assert ev(page, "() => state.modal.open && state.modal.type==='submit'"), "openSubmit ไม่เปิด submit modal"
    # helper ตรวจ 3 เฟส: (1) เปิดมา disabled + ไม่ auto-pick + ช่องว่าง (2) กดเปล่า=no-op
    #                    (3) เลือกครบทุก slot → enable → doSubmit commit (สร้างใบใหม่ +1)
    r = assert_submit_requires_all_approvers(page, note="wizard 64,200 · 3 slot")
    assert r["steps"] == 3, f"ยอด 64,200 (>50,000) ควรมีสาย 3 slot ได้ {r['steps']}"
    assert r["hadId"] is True, "ปุ่มยืนยันไม่มี id เสถียร (submitConfirmBtn)"
    assert r["disabledWhenFresh"] is True and r["noAutoPick"] is True and r["slotInputsEmpty"] is True, \
        f"เปิด modal มาไม่ควร auto-pick (disabled+ว่าง): {r}"
    assert r["submittedWhileUntouched"] is False, "กดส่งทั้งที่ยังไม่แตะ slot แล้ว commit (ไม่ควร)"
    assert r["enabledWhenAllPicked"] is True and r["submittedWhenAllPicked"] is True, \
        "เลือกครบทุก slot แล้วปุ่มไม่ enable/ส่งไม่สำเร็จ"
    # phase 2 ไม่สร้างใบ · phase 3 สร้าง 1 ใบ → net +1
    assert ev(page, "() => EXP.docs.length") == n0 + 1, \
        f"ควรสร้างใบใหม่ 1 ใบเฉพาะตอนเลือกครบ (net +1): {n0}→{ev(page, '() => EXP.docs.length')}"
    return (f"submit gate {r['steps']} slot: เปิดมา disabled+ไม่ auto-pick+ช่องว่าง · "
            f"กดเปล่า=no-op · เลือกครบ→enable→ส่งสำเร็จ (Bug A)")


def c_combo_floats_modal(page):
    """[FN-08 · UX-DOA · BUG-C] combobox ในกล่องส่งอนุมัติต้องลอยทับ ไม่ดัน modal scroll (§C3.8)

    บั๊ก (user-found 2026-09-09): modal 'ส่งอนุมัติ' มี .modal-body{overflow-y:auto} · combobox slot picker
    เปิด dropdown (.ss-list absolute) → เนื้อ list ดันพื้นที่ scroll ของ modal-body (scrollHeight 187→440,
    scrollbar โผล่) → ทั้ง modal เลื่อน (ดูแปลก). fix: render() toggle 'has-combo' บน #modalBackdrop เมื่อ
    submit + CSS .modal-backdrop.has-combo .modal/.modal-body{overflow:visible} → dropdown ลอยพ้นกรอบ.
    ตัววัดเดิม (DSP-02b) ตรวจแค่ 'combobox ไม่กางเอง' — ไม่ได้เปิดเองแล้ววัด overflow/scroll ของ modal-body.
    """
    open_(page)
    r = assert_combobox_floats_in_modal(page, note="submit modal · slot-0 dropdown")
    assert r["hasCombo"] is True, "modalBackdrop ไม่มี has-combo (render toggle หาย)"
    assert r["bodyOverflowFresh"] == "visible" and r["bodyOverflowOpen"] == "visible", \
        f"modal-body overflowY ไม่ visible (ดัน scroll): fresh={r['bodyOverflowFresh']} open={r['bodyOverflowOpen']}"
    assert r["scrollTrapped"] is False, "modal-body เลื่อนได้ (dropdown ดัน scroll — fix หาย)"
    assert r["pickRecorded"] is True and r["pickClosedList"] is True, "เลือกผู้อนุมัติแล้ว list ไม่ปิด/ไม่บันทึก"
    return (f"combobox ลอยทับ ({r['optCount']} option · floatsBelow={r['listFloatsBelow']}): "
            f"has-combo·modal-body overflowY visible·เลื่อนไม่ได้ · เลือกได้→list ปิด+picks บันทึก (Bug C)")


def c_clear_filters(page):
    """[FN-90] ล้างตัวกรอง — reset ค้นหา+สถานะ กลับเป็นทั้งหมด แล้ว re-render (แสดงครบทุกใบใน scope)"""
    open_(page)
    after(page, "() => { state.role='officer'; render(); }")   # เจ้าหน้าที่ (scope:all) — ล้างแล้วต้องเห็นครบทุกใบ (OQ-EXP-03)
    after(page, "() => { state.filters.search='สมชาย'; state.filters.status='draft'; refreshView(); }")
    after(page, "() => clearFilters()")
    f = ev(page, "() => ({s:state.filters.search, st:state.filters.status})")
    assert f == {"s": "", "st": "all"}, f"ล้างตัวกรองแล้วค่าไม่รีเซ็ต: {f}"
    total = ev(page, "() => EXP.docs.length")
    rows = ev(page, "() => document.querySelectorAll('#page-content .tbl tbody tr').length")
    assert rows == total, f"ล้างตัวกรองแล้วควรแสดงครบ {total} แถว ได้ {rows}"
    return f"ล้างตัวกรอง: search+status → ''/all · แสดงครบ {total} ใบ"


# ═══════════ GOVERNANCE BYPASS PROBES (§C3.8 · BA re-gate F101 2026-09-09) ═══════════
# ตัววัดใหม่สำหรับ CRITICAL bypass ที่ gate เดิมมองไม่เห็น (approve/reopen/cancel ไม่มี guard,
# chain collapse, self-approve, เลขรันซ้ำ). ขับ controller จริงแล้ว assert data model + DOM.

def c_approve_precondition(page):
    """[FN-09 · FIX-01] doApprove precondition guard — อนุมัติได้เฉพาะใบ pending_approval (rejected/draft/approved/paid = no-op)"""
    open_(page)
    after(page, "() => setRole('mgr')")   # ผ่าน role guard เพื่อวัด "status guard" ล้วน ๆ
    checks = {'d5': 'rejected', 'd1': 'draft', 'd2': 'approved', 'd6': 'paid'}
    for did, st0 in checks.items():
        r = ev(page, "() => { const d=findDoc('%s'); const b={s:d.status,c:d.code}; doApprove('%s'); return {b, a:{s:d.status,c:d.code}}; }" % (did, did))
        assert r['b'] == r['a'], f"{did} ({st0}) ถูกอนุมัติได้ (ควร no-op): {r}"
        assert ev(page, "() => state._busy") is False, f"{did}: guard ควร return ก่อน set _busy"
    # pending → เดินต่อได้ (d3 chain 1 ขั้น → approved + ออกเลข 4 หลัก)
    r2 = ev(page, "() => { doApprove('d3'); const d=findDoc('d3'); return {s:d.status,c:d.code}; }")
    assert r2['s'] == 'approved' and re.match(r'^EXP-2569-\d{4}$', r2['c']), f"pending อนุมัติไม่เดินต่อ: {r2}"
    return "FIX-01: rejected/draft/approved/paid → no-op (ไม่ set _busy) · pending_approval → approved+ออกเลข"


def c_chain_stepwise(page):
    """[FN-08 · FN-09 · FIX-02] DOA chain เดินทีละขั้น — 3 ขั้น pending ต้อง 3 คลิก · เลขออกครั้งเดียวจบ chain · ทุกขั้นมี at"""
    open_(page)
    # สร้างใบ chain 3 ขั้น (ทุกขั้น pending) ผ่าน submit flow จริง: d1 (draft) + รายการ >50,000
    after(page, "() => { findDoc('d1').lines.push({date:'2569-08-28',cat:'ent',desc:'จัดเลี้ยงใหญ่',qty:1,unit_price:60000,vat_mode:'add'}); }")
    after(page, "() => openSubmitDraft('d1')")
    pick_all_slots(page)
    after(page, "() => doSubmit()")
    assert ev(page, "() => findDoc('d1').chain.length") == 3, "ยอด >50,000 → chain 3 ขั้น"
    assert ev(page, "() => findDoc('d1').chain.every(s=>s.status==='pending')") is True, "ทุกขั้นเริ่ม pending"
    after(page, "() => setRole('mgr')")   # ผู้อนุมัติ (DOA)
    # คลิก 1,2 → เอกสารยัง pending_approval · ยังไม่ออกเลข · ขั้นที่ผ่านมี at · ขั้นถัดไปยัง pending
    for i in (1, 2):
        after(page, "() => { state._busy=false; doApprove('d1'); }")
        d = ev(page, "() => findDoc('d1')")
        assert d["status"] == "pending_approval", f"คลิก {i} เอกสารต้องยัง pending_approval ได้ {d['status']}"
        assert d["code"] == "(รออนุมัติ)", f"คลิก {i} ยังไม่ควรออกเลข ได้ {d['code']}"
        assert d["chain"][i - 1]["status"] == "approved" and d["chain"][i - 1].get("at"), f"ขั้น {i} ต้อง approved + at: {d['chain']}"
        assert d["chain"][i]["status"] == "pending", f"ขั้นถัดไป ({i + 1}) ต้องยัง pending"
    # คลิก 3 (ขั้นสุดท้าย) → approved + ออกเลขครั้งเดียว + ทุกขั้น approved+at
    after(page, "() => { state._busy=false; doApprove('d1'); }")
    d = ev(page, "() => findDoc('d1')")
    assert d["status"] == "approved", "คลิก 3 (ขั้นสุดท้าย) ต้อง approved"
    assert re.match(r"^EXP-2569-\d{4}$", d["code"]), f"ออกเลขไม่ถูก format 4 หลัก: {d['code']}"
    assert all(s["status"] == "approved" and s.get("at") for s in d["chain"]), f"ทุกขั้นต้อง approved + at: {d['chain']}"
    return f"FIX-02: chain 3 ขั้น pending → 2 คลิกแรกคง pending (ไม่ออกเลข) · คลิก 3 → approved+{d['code']} (ออกเลขครั้งเดียว·ทุกขั้นมี at)"


def c_reopen_cancel_guard(page):
    """[FN-13 · FN-14 · FIX-04/05] doReopen เฉพาะ rejected · doCancel เฉพาะ draft (สถานะอื่น = no-op)"""
    open_(page)
    # doReopen: approved/paid/pending/draft → no-op · rejected → draft
    ro = {'d2': 'approved', 'd6': 'paid', 'd3': 'pending_approval', 'd1': 'draft'}
    for did, st0 in ro.items():
        r = ev(page, "() => { const d=findDoc('%s'); const b={s:d.status,c:d.code}; doReopen('%s'); return {b, a:{s:d.status,c:d.code}}; }" % (did, did))
        assert r['b'] == r['a'], f"doReopen บน {did} ({st0}) เปลี่ยนสถานะ (ควร no-op): {r}"
    r5 = ev(page, "() => { doReopen('d5'); const d=findDoc('d5'); return {s:d.status,c:d.code}; }")
    assert r5['s'] == 'draft' and r5['c'] == '(ร่าง)', f"reopen rejected (d5) ควรกลับร่าง+code ล้าง: {r5}"
    # doCancel: paid/approved/rejected/pending → no-op · draft → cancelled
    open_(page)
    ca = {'d6': 'paid', 'd2': 'approved', 'd5': 'rejected', 'd3': 'pending_approval'}
    for did, st0 in ca.items():
        r = ev(page, "() => { const d=findDoc('%s'); const b=d.status; doCancel('%s'); return {b, a:d.status}; }" % (did, did))
        assert r['b'] == r['a'], f"doCancel บน {did} ({st0}) ยกเลิกได้ (ควร no-op): {r}"
    rc = ev(page, "() => { doCancel('d1'); return findDoc('d1').status; }")
    assert rc == 'cancelled', f"ยกเลิกใบร่าง (d1) ควร cancelled ได้ {rc}"
    return "FIX-04/05: reopen เฉพาะ rejected (d5→ร่าง) · cancel เฉพาะ draft (d1→cancelled) · สถานะอื่น no-op"


def c_role_guard(page):
    """[FN-94 · FIX-03] role guard: ผู้เบิก(admin) ไม่มีปุ่มอนุมัติ + เรียก doApprove/doReject ตรงถูกบล็อก · ผู้อนุมัติ(mgr) ผ่าน"""
    open_(page)
    after(page, "() => openView('d3')")   # admin (default)
    hasBtn = ev(page, "() => [...document.querySelectorAll('#drawer .drawer-footer .btn')].some(b=>/อนุมัติ/.test(b.textContent))")
    assert hasBtn is False, "ผู้เบิก (admin) ไม่ควรเห็นปุ่มอนุมัติ/ไม่อนุมัติ (กัน self-approve)"
    assert "เฉพาะผู้อนุมัติ" in drawer_text(page), "ควรมี note ว่าเฉพาะผู้อนุมัติ (DOA) ดำเนินการได้"
    # เรียก doApprove/doReject ตรง (admin) → ถูก guard บล็อก (สถานะไม่เปลี่ยน)
    r = ev(page, "() => { const d=findDoc('d3'); doApprove('d3'); const a1=d.status; doReject('d3'); return {a1, a2:d.status}; }")
    assert r['a1'] == 'pending_approval' and r['a2'] == 'pending_approval', f"admin เรียก doApprove/doReject ตรงต้องถูกบล็อก: {r}"
    # mgr → มีปุ่มอนุมัติ + doApprove ผ่าน
    after(page, "() => { closeDrawer(); setRole('mgr'); openView('d3'); }")
    hasBtn2 = ev(page, "() => [...document.querySelectorAll('#drawer .drawer-footer .btn')].some(b=>/อนุมัติ/.test(b.textContent))")
    assert hasBtn2 is True, "ผู้อนุมัติ (mgr) ต้องเห็นปุ่มอนุมัติ"
    after(page, "() => doApprove('d3')")
    assert ev(page, "() => findDoc('d3').status") == "approved", "ผู้อนุมัติ (mgr) อนุมัติแล้วต้อง approved"
    return "FIX-03 role guard: ผู้เบิกไม่เห็นปุ่ม+เรียกตรงถูกบล็อก (สิทธิ์ไม่พอ) · ผู้อนุมัติเห็นปุ่ม+อนุมัติผ่าน"


def c_docnum_monotonic(page):
    """[FN-09 · FIX-06] เลขรัน monotonic ไม่ซ้ำ/ไม่ reuse + pad 4 หลัก (เคส E6: approve→approve→reopen+approve)"""
    open_(page)
    after(page, "() => setRole('mgr')")
    after(page, "() => { state._busy=false; doApprove('d3'); }")   # 1 ขั้น → เลขแรก
    c1 = ev(page, "() => findDoc('d3').code")
    after(page, "() => { state._busy=false; doApprove('d4'); }")   # chain 2/3 approved → คลิกจบ → เลขถัดไป
    c2 = ev(page, "() => findDoc('d4').code")
    # reopen ใบตีกลับ d5 → submit → อนุมัติ → เลขเดินหน้าต่อ ไม่ reuse
    after(page, "() => { state._busy=false; doReopen('d5'); }")
    after(page, "() => openSubmitDraft('d5')")
    pick_all_slots(page)
    after(page, "() => doSubmit()")
    after(page, "() => { state._busy=false; doApprove('d5'); }")
    c3 = ev(page, "() => findDoc('d5').code")
    codes = [c1, c2, c3]
    for c in codes:
        assert re.match(r"^EXP-2569-\d{4}$", c), f"เลขไม่ pad 4 หลัก: {c}"
    assert len(set(codes)) == 3, f"เลขซ้ำ/reuse (count-based bug): {codes}"
    nums = [int(c.split('-')[-1]) for c in codes]
    assert nums == sorted(nums), f"เลขไม่ monotonic เดินหน้า: {nums}"
    return f"FIX-06: เลข monotonic ไม่ซ้ำ/ไม่ reuse {codes} (pad 4 หลักเสมอ)"


# ═══════════ SUBMIT-MODAL FIX PROBES (§C3.8 · F-HR-EXPENSE 2026-09-10) ═══════════
# ตัววัดใหม่สำหรับ 2 fix ของกล่อง 'ส่งอนุมัติ' (DOA slot picker) ที่ gate เดิมมองไม่เห็น:
#   Bug D  slot dropdown flip-up — dropdown ของ slot ล่างสุดที่จอเตี้ยเคยทะลุก้นจอ
#   regression guard — ปิดกล่องส่งอนุมัติทุกทาง (ยกเลิก/backdrop/Escape) + Esc chain ไม่ทิ้ง backdrop ค้าง

def c_slot_no_spill(page):
    """[FN-08 · BUG-D · UI-REG] slot dropdown ในกล่องส่งอนุมัติไม่ทะลุก้นจอ + flip ขึ้น (ss-up) ที่จอเตี้ย

    บั๊กเดิม (user-found 2026-09-10): modal 'ส่งอนุมัติ' 3 slot (ยอด >50,000) · เปิด dropdown ของ slot
    ล่างสุดที่ viewport เตี้ย (~<900px) → .ss-list (absolute top:100%) กางลงล่างแล้วก้นทะลุขอบล่างจอ
    (800/768/720/650 ล้น 22/38/62/97px). fix: CSS .ss-list.ss-up + JS ssPlaceList() ท้าย ssRenderList —
    วัด wrap rect แล้ว flip ขึ้น (ss-up) เมื่อพื้นที่ล่างไม่พอ. ต้องรันที่จอเตี้ย + slot ล่างสุดถึงเห็น.
    """
    prev = page.viewport_size or {"width": 1280, "height": 900}
    try:
        page.set_viewport_size({"width": 1440, "height": 768})   # จอเตี้ย → slot ล่างสุดเคยทะลุ
        open_(page)
        r = assert_slot_dropdown_no_spill(page, note="viewport 1440×768 · 3 slot · slot ล่างสุด")
    finally:
        page.set_viewport_size(prev)   # คืน viewport เดิม กันกระทบเคสถัดไป
    return (f"slot dropdown ไม่ทะลุก้นจอ @768 (nslots={r['nslots']} · listBottom={r['listBottom']}≤{r['vh']} · "
            f"ss-up={r['hasUp']}) — flip ขึ้นเมื่อพื้นที่ล่างไม่พอ (Bug D)")


def c_submit_dismiss_clean(page):
    """[FN-08 · UI-REG · backdrop bug] กล่องส่งอนุมัติเปิด "จากลิ้นชักดูใบร่างจริง" → ปิดสะอาดทุกทาง — ทั้ง modal และลิ้นชักเคลียร์

    FAITHFUL (แก้ false pass): openView(draft) เปิดลิ้นชัก → คลิกปุ่ม 'ส่งอนุมัติ' ใน footer (openSubmitDraft) →
    submit modal ทับลิ้นชัก (drawerBackdrop ค้างใต้ modal). ทุกทาง dismiss (ยกเลิก/backdrop/Escape/Esc-chain) →
    ทั้ง modal และลิ้นชักปิด (state.drawer.open===false · ไม่มี backdrop ตัวไหนค้าง · กลางจอถึงหน้าเพจ).
    บั๊ก (user-found 2026-09-10): closeModal ปิดแค่ modal เหลือ drawerBackdrop หรี่จอค้าง ต้องคลิกซ้ำ.
    fix (closeModal): submit-modal ที่มี doaDraft.docId → เรียก closeDrawer() ด้วยทุกทาง dismiss.
    ทำไมเวอร์ชันเดิม false pass: เปิด modal ด้วย openSubmitDraft() ตรงใน eval → ไม่มีลิ้นชักใต้ modal จึงไม่เคยเดินเคสจริง.
    """
    open_(page)
    r = assert_submit_modal_all_dismiss_clean(page, note="submit modal จากลิ้นชักดูใบร่าง")
    return (f"ปิดสะอาดทุกทาง (ผ่านลิ้นชักดูใบร่างจริง): {', '.join(r['paths'])} — "
            f"ทั้ง modal และลิ้นชักปิด · ไม่มี backdrop ค้าง · Esc#1 (dropdown เปิด) คง modal")


def c_wizard_submit_cancel_keeps_drawer(page):
    """[FN-08 · UI-REG · lingering-backdrop bug] ยกเลิก/ปิดกล่องส่งอนุมัติของ CREATE WIZARD → wizard drawer ยัง **เปิดจริงบนจอ**

    คู่กับ U15: fix backdrop bug ปิดลิ้นชักด้วยเฉพาะ submit modal ที่มี docId (เปิดจากใบร่าง). ต้องกันไม่ให้ไป
    regress กล่องส่งอนุมัติของ wizard (openSubmit · ไม่มี docId) — dismiss แล้วลิ้นชัก wizard ต้องยังเปิด
    (ผู้ใช้แค่ยกเลิกการเลือกผู้อนุมัติ ไม่ทิ้งใบที่กรอก). ขับ create flow จริง (คลิก '+ สร้างใบเบิก') ไม่ใช่ openDrawer ตรง.

    ★ แก้ FALSE PASS (2026-09-10): เดิม assert แค่ state.drawer.open===true (ธง) — บั๊กจริงคือ full render()
      ทิ้ง class is-open ของ #drawer → wizard สไลด์ออก เหลือฉากหลังหรี่ค้าง ทั้งที่ธงยัง true. ตัววัดใหม่ยืนยัน
      "เปิดจริงบนจอ": #drawer มี is-open · กลางจอเป็นเนื้อ wizard (ไม่ใช่ drawerBackdrop) · stepper มองเห็น.
      ทดสอบครบ 3 ทาง dismiss (ยกเลิก / คลิก backdrop / Escape) — ของ wizard ทุกทางต้องคงลิ้นชักเปิด.
    """
    open_(page)
    r = assert_wizard_submit_cancel_keeps_drawer(page, note="wizard submit dismiss")
    return (f"wizard-dismiss guard (visually-open): {', '.join(r['paths'])} → #drawer is-open · "
            f"กลางจอ='{r['center']}' (เนื้อ wizard ไม่ใช่ backdrop) · stepper เห็น · open={r['drawerOpen']}/mode={r['drawerMode']}")


# ═══════════════════════════════ RUN ═══════════════════════════════

CASES = [
    ('E01', '[FN-01 · S-01] สร้างใบเบิกผ่าน wizard 5 ขั้น', c_fn01),
    ('E02', '[FN-02 · S-01] หัวเอกสาร: ผู้เบิก combobox + วันที่ พ.ศ. + ช่องทางจ่าย', c_fn02),
    ('E03', '[FN-03 · S-02] line editor + VAT none/add/included + ยอดรวมถูกต้อง', c_fn03),
    ('E04', '[FN-04 · S-03] เกินเพดานหมวด → เตือน+บังคับเหตุผล (warn ไม่ block)', c_fn04),
    ('E05', '[FN-05 · S-04] ไม่มีรายการ/ยอด=0 → ส่งอนุมัติไม่ได้', c_fn05),
    ('E06', '[FN-06 · S-05] ตำแหน่ง/ศูนย์ต้นทุน snapshot ณ วันเบิก', c_fn06),
    ('E12', '[FN-12 · S-13] หมวดบังคับแนบใบเสร็จก่อนส่ง', c_fn12),
    ('E07', '[FN-07 · S-01] ส่งอนุมัติจาก wizard → pending + สาย DOA', c_fn07),
    ('E08', '[FN-08 · S-08] DOA slot picker ตามวงเงิน (ไม่ hardcode)', c_fn08),
    ('E11', '[FN-11 · S-11] แก้ยอดข้ามช่วง → re-resolve สาย DOA', c_fn11),
    ('E13', '[FN-13 · S-06] ตีกลับ (บังคับเหตุ) → แก้แล้วยื่นใหม่ได้', c_fn13),
    ('E14', '[FN-14 · S-07] ยกเลิกก่อนอนุมัติ (soft archive)', c_fn14),
    ('E09', '[FN-09 · S-09] อนุมัติ → ออกเลข EXP + 7C FC/EC', c_fn09),
    ('E15', '[FN-15 · S-15] tab PDF Preview (a4) + tab ลายเซ็น', c_fn15),
    ('E17', '[FN-17 · S-15] view tabs รายละเอียด›PDF›ลายเซ็น›ประวัติ + เอกสารแนบในรายละเอียด', c_fn17),
    ('E10', '[FN-10 · S-10] เลือกช่องทางจ่าย → ส่งจ่าย (hook)', c_fn10),
    ('E16', '[FN-16 · S-14] จ่ายแล้ว display-only จากปลายทาง', c_fn16),
    ('E90', '[FN-90] list docPill + ลายเซ็น + ค้นหา/filter + empty', c_fn90),
    ('E91', '[FN-91] ตีกลับ/ยกเลิกผ่าน confirm + soft archive', c_fn91),
    ('E92', '[FN-92] validate บังคับ + กัน double-submit + wizard ล็อก', c_fn92),
    ('E93', '[FN-93] audit append-only (แท็บประวัติ)', c_fn93),
    ('E94', '[FN-94] mask RESTRICTED จำนวนเงินตาม role', c_fn94),
    ('NEG', '[NEG · unsupported ×7] ของห้ามมี — เรนเดอร์จริงแล้วไม่มี affordance', c_unsupported),
    ('U01', '[DSP-01] modal เหนือ drawer (z portal>drawer)', c_modal_over_drawer),
    ('U02', '[UI] overlay stack สะอาด', c_overlay_stack),
    ('U03', '[UI] CSS var ครบ', c_static_css),
    ('U04', '[UI] affordance cursor:pointer', c_affordance),
    ('U05', '[UI-REG] no NaN/undefined leak (list/wizard/view/modal)', c_no_garbage_text),
    ('U06', '[DSP-02a] wizemp เลือกแล้วปิด (ไม่เด้งกางใหม่ · focus-restore)', c_combo_closes),
    ('U07', '[DSP-02b] submit modal ไม่มี combobox กางเอง (trapFocus auto-open)', c_modal_no_autoopen),
    # ⭐ user-found bugs (§C3.8) — ตัววัดใหม่ที่ gate เดิมมองไม่เห็น
    ('B02', '[FN-90] ล้างตัวกรอง — reset search+status', c_clear_filters),
    ('B03', '[FN-08] ส่งอนุมัติต้องเลือกผู้อนุมัติครบทุก slot (UX-DOA)', c_submit_gate),
    ('U08', '[BUG-2] filter row อยู่ในการ์ดมี gutter + ปุ่มล้างตัวกรอง', c_filter_inside_card),
    ('U09', '[BUG-3] wizard stepper 5 ขั้นเรนเดอร์สะอาด @1290', c_stepper_wellformed),
    ('U10', '[BUG-5] footer action ปุ่มกดได้จริง · payment card ไม่ pin', c_footer_actions),
    ('U11', '[BUG-6] backdrop/overlay ไม่ค้างหลังปิด drawer/modal', c_overlay_cleared),
    ('U12', '[BUG-B] backdrop เคลียร์หลัง confirm action (อนุมัติ/ตีกลับ/ยกเลิก)', c_overlay_after_confirm),
    ('U13', '[FN-08] combobox ในกล่องส่งอนุมัติต้องลอยทับ ไม่ดัน modal scroll', c_combo_floats_modal),
    # ⭐ governance bypass probes (§C3.8 · BA re-gate F101 CRITICAL fixes)
    ('G01', '[FN-09 · FIX-01] doApprove precondition guard (อนุมัติเฉพาะ pending)', c_approve_precondition),
    ('G02', '[FN-08 · FN-09 · FIX-02] DOA chain เดินทีละขั้น + เลขออกครั้งเดียวจบ chain', c_chain_stepwise),
    ('G03', '[FN-13 · FN-14 · FIX-04/05] reopen เฉพาะตีกลับ · cancel เฉพาะร่าง', c_reopen_cancel_guard),
    ('G04', '[FN-94 · FIX-03] role guard: ผู้เบิกไม่ self-approve · ผู้อนุมัติผ่าน', c_role_guard),
    ('G05', '[FN-09 · FIX-06] เลขรัน monotonic ไม่ซ้ำ/ไม่ reuse + pad 4 หลัก', c_docnum_monotonic),
    # ⭐ submit-modal fixes (§C3.8 · F-HR-EXPENSE 2026-09-10) — ตัววัดใหม่ที่ gate เดิมมองไม่เห็น
    ('U14', '[FN-08 · BUG-D] slot dropdown ในกล่องส่งอนุมัติไม่ทะลุก้นจอ + flip ขึ้น (ss-up) ที่จอเตี้ย', c_slot_no_spill),
    ('U15', '[FN-08] กล่องส่งอนุมัติ (จากลิ้นชักดูใบร่าง) ปิดสะอาดทุกทาง — modal+ลิ้นชักเคลียร์ (backdrop bug)', c_submit_dismiss_clean),
    ('U16', '[FN-08] ยกเลิก/backdrop/Esc กล่องส่งอนุมัติของ WIZARD → wizard drawer เปิดจริงบนจอ (#drawer is-open · lingering-backdrop bug)', c_wizard_submit_cancel_keeps_drawer),
    # ⭐ PM/BA OQ 2026-09-10 (จุดเชื่อม petty/advance + role scope) — capability ใหม่รอผูก FN ใน BRD
    ('E30', '[F101-c · OQ-EXP-01] เคลียร์เงินทดรอง หักลบอัตโนมัติ (soft-ref F103 · display-only)', c_advance_clear),
    ('E31', '[OQ-EXP-03] ขอบเขตการมองเห็น self/all + role เจ้าหน้าที่ (HR/Finance)', c_role_scope),
]


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        suite.watch(page)
        for tid, name, fn in CASES:
            suite.check(tid, name, lambda fn=fn: fn(page))
        browser.close()

    ok = suite.report(exit_on_fail=False)
    total = len(suite.results)

    # ── divisor summary: FN ครอบ NN/22 ──
    ALL_FN = ['FN-%02d' % i for i in range(1, 18)] + ['FN-90', 'FN-91', 'FN-92', 'FN-93', 'FN-94']
    covered = set()
    for _tid, nm, _st, _d in suite.results:
        for m in re.findall(r'FN-\d{2}', nm):
            covered.add(m)
    missing = [f for f in ALL_FN if f not in covered]
    print('=' * 74)
    print("FN ครอบ %d/22 · เคสรวม %d · ผ่าน %d/%d" % (len(covered & set(ALL_FN)), total, ok, total))
    if missing:
        print("  FN ที่ยังไม่มีเคส:", ', '.join(missing))
    else:
        print("  ครบทั้ง 22 FN (FN-01..17 + FN-90..94)")
    sys.exit(0 if ok == total and not suite.console_errors else 1)


if __name__ == '__main__':
    main()
