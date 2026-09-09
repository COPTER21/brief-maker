"""E2E · F-HR-Performance (ประเมินผลงาน / Performance) — WF-01 Step 5

รันไทม์ตัวเดียวที่ครอบทุก FN (18 = FN-01..13 + FN-90..94) + เคสเชิงลบ 4 ข้อ
(unsupported[]) ที่เรนเดอร์จริงแล้ว assert ว่า "ไม่มี" affordance บนจอ.

ยึด helper ของ uikit เท่านั้น (ready/settle/after) — ไม่มี wait_for_timeout, ไม่มีตัวตรวจ UI ใหม่.
ขับหน้าจอผ่าน controller function จริงของไฟล์ แล้ว assert ทั้ง data model และข้อความที่เรนเดอร์บน DOM.
reload หน้าใหม่ต่อเคส → mock data (PERF) reset = เคสอิสระต่อกัน.

BASE-KIT regression ที่ต้องมีทุก HR feature (Recruit/Train/Welfare โดนมาแล้ว):
  DSP-01  modal เปิดในลิ้นชัก z ต้องอยู่เหนือ drawer (JS_MODAL_UNDER_DRAWER)
  DSP-02a เลือก combobox แล้ว dropdown ต้องปิด (assert_combobox_closes_after_select)
  DSP-02b เปิด modal แล้ว combobox ต้องไม่กางเอง (modal_autoopens_comboboxes)

รัน: .claude/venv/Scripts/python.exe outputs/F-HR-Performance/_e2e/e2e-performance.py [path/to/performance.html]
"""
from pathlib import Path
import re
import sys

from playwright.sync_api import sync_playwright

OUTPUTS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(OUTPUTS / "_SHARED" / "_e2e"))
from uikit import (  # noqa: E402
    Suite, ready, settle as shared_settle, after as shared_after,
    assert_combobox_closes_after_select,
    modal_autoopens_comboboxes, assert_no_garbage_text,
    assert_drawer_footer_pinned, assert_text_absent, assert_icons_rendered,
    JS_MODAL_UNDER_DRAWER,
)

HTML = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parents[1] / "performance.html").resolve()
BASE = HTML.as_uri()

suite = Suite("F-HR-Performance ประเมินผลงาน")


def settle(page, timeout=1400):
    shared_settle(page, timeout=timeout)


def after(page, js, timeout=1600):
    return shared_after(page, js, timeout=timeout)


def open_(page):
    """เปิดหน้าใหม่ (reset PERF mock) แล้วรอ render จริง"""
    ready(page, BASE, timeout=9000)
    page.wait_for_function(
        "() => { const p=document.getElementById('page-content'); return p && p.innerHTML.trim().length>0; }",
        timeout=9000,
    )


def ev(page, js):
    return page.evaluate(js)


def pc_text(page):
    return page.evaluate("() => document.getElementById('page-content').textContent")


def drawer_text(page):
    return page.evaluate("() => (document.getElementById('drawer')||{}).textContent || ''")


def modal_text(page):
    return page.evaluate("() => (document.querySelector('#modalBackdrop .modal')||{}).textContent || ''")


def toast_text(page):
    return page.evaluate("() => (document.getElementById('toast')||{}).textContent || ''")


def go_tab(page, t):
    after(page, "() => { state.tab='%s'; render(); }" % t)


def calib_publish(page, aid, dec="ผ่าน", pick=(0, 1)):
    """ขับ staged calibration (FIX-06) จนเผยแพร่ผล: เปิด modal → เลือกผู้สอบทาน 2 ขั้น →
    ส่งสอบทาน (freeze · คง calibration) → บันทึกขั้น 1 → เลือก decision → บันทึกขั้นสุดท้าย (publish)
    """
    after(page, "() => openModal('doaCalib',{id:'%s'})" % aid)
    after(page, "() => ssPick('doa0',%d)" % pick[0])
    after(page, "() => ssPick('doa1',%d)" % pick[1])
    after(page, "() => doCalibSend('%s')" % aid)          # จังหวะ 1 — freeze reviewers (ยังไม่ publish)
    after(page, "() => doCalibStage('%s')" % aid)          # บันทึกผลขั้น 1 (ยังไม่ publish)
    after(page, "() => { const s=document.getElementById('p_dec'); if(s) s.value='%s'; }" % dec)
    after(page, "() => doCalibStage('%s')" % aid)          # ขั้นสุดท้าย → published


# ═══════════════════════════════ FN CASES ═══════════════════════════════

def c_fn01(page):
    """[FN-01 · S-01 · BR-01] สร้างรอบประเมิน — อ่านรอบ/แบบจาก HR Config → เปิดกรอก"""
    open_(page)
    n0 = ev(page, "() => PERF.cycles.length")
    after(page, "() => openDrawer('newCycle')")
    dt = drawer_text(page)
    assert "ตั้งค่า HR" in dt, "ฟอร์มสร้างรอบไม่ได้อ้าง HR Configuration (ตั้งค่า HR)"  # microcopy: snake_case appraisal_cycle ถูกถอดออกจากจอ (Rule #81) — ยังอ้าง ตั้งค่า HR
    assert ev(page, "() => !!window.__ss['cfgCycle']"), "combobox เลือกรอบจาก HR Config ไม่ถูก init"
    optn = ev(page, "() => window.__ss['cfgCycle'].options.length")
    assert optn >= 3, f"ตัวเลือกรอบจาก config ควร >=3 (ได้ {optn})"
    after(page, "() => ssPick('cfgCycle',0)")
    after(page, "() => submitNewCycle()")
    assert ev(page, "() => PERF.cycles.length") == n0 + 1, "สร้างรอบแล้ว PERF.cycles ไม่เพิ่ม 1"
    assert "สร้างรอบ" in toast_text(page), f"ไม่ขึ้น toast สำเร็จ (ได้ '{toast_text(page)}')"
    assert ev(page, "() => state.drawer.open") is False, "สร้างแล้วลิ้นชักไม่ปิด"
    # รอบใหม่ status = open (เปิดกรอก) + ยิง notif รอบเปิด
    assert ev(page, "() => PERF.cycles[0].status") == "open", "รอบใหม่ไม่ได้เปิดกรอก (status!=open)"
    assert ev(page, "() => PERF.notifs[0].b.indexOf('เปิดกรอก')>=0"), "ไม่ยิงแจ้งเตือน 'รอบเปิด'"
    return "สร้างรอบจาก config (อ่าน appraisal_cycle) · เปิดกรอก · notif รอบเปิด · ลิ้นชักปิด"


def c_fn11(page):
    """[FN-11 · S-10 · BR-09] ปิดรอบประเมิน (ล็อกแก้ไข · soft archive)"""
    open_(page)
    n0 = ev(page, "() => PERF.cycles.length")
    after(page, "() => openDrawer('viewCycle','CY1')")
    after(page, "() => openModal('closeCycle',{id:'CY1'})")
    mt = modal_text(page)
    assert "ล็อกการแก้ไข" in mt, "confirm ปิดรอบไม่ระบุว่าล็อกการแก้ไข"
    assert "soft archive" in mt, "confirm ปิดรอบไม่ระบุ soft archive"
    after(page, "() => doCloseCycle('CY1')")
    assert ev(page, "() => cyc('CY1').status") == "closed", "ปิดรอบแล้ว status ไม่เป็น closed"
    assert ev(page, "() => PERF.cycles.length") == n0, "ปิดรอบแล้ว record หาย (ควร soft archive)"
    assert ev(page, "() => !!PERF.cycles.find(c=>c.id==='CY1')") is True, "record CY1 หายไป"
    return "ปิดรอบ CY1 → closed · ล็อกแก้ไข · record คงอยู่ (soft archive)"


def c_fn02(page):
    """[FN-02 · S-02 · BR-02] ตั้งเป้า/KPI ต่อคน — น้ำหนักรวม ≠ 100% บล็อกบันทึก"""
    open_(page)
    after(page, "() => { state.view.tab='kpi'; openDrawer('viewAppr','A1'); }")
    assert ev(page, "() => Array.isArray(state.edit)"), "โหมดตั้งเป้า (goal+manage) ไม่เข้า KPI editor (state.edit ว่าง)"
    # (ก) น้ำหนักรวม ≠ 100 → บล็อก
    after(page, "() => { state.edit[0].w = 50; }")   # 50 + 40 = 90
    st0 = ev(page, "() => appr('A1').status")
    after(page, "() => saveKpi('A1')")
    assert ev(page, "() => appr('A1').status") == st0 == "goal", "น้ำหนักรวม≠100 แต่บันทึกผ่าน (สถานะเปลี่ยน)"
    assert "100%" in toast_text(page), f"ไม่เตือนน้ำหนักต้องรวม 100% (ได้ '{toast_text(page)}')"
    # (ข) น้ำหนักรวม = 100 → บันทึกได้ → เปิดให้พนักงานประเมินตนเอง (status→self)
    after(page, "() => { state.edit[0].w = 60; }")   # 60 + 40 = 100
    after(page, "() => saveKpi('A1')")
    assert ev(page, "() => appr('A1').status") == "self", "น้ำหนัก 100% แล้วบันทึกไม่สำเร็จ (ไม่เปิดประเมินตนเอง)"
    return "KPI editor: น้ำหนัก 90% บล็อก+เตือน 100% · 100% บันทึกผ่าน (goal→self)"


def c_fn03(page):
    """[FN-03 · S-03 · BR-03] พนักงานประเมินตนเอง (คะแนน+ความเห็น) → ส่งต่อหัวหน้า"""
    open_(page)
    assert ev(page, "() => appr('A2').status") == "self", "A2 ควรอยู่สถานะ 'ประเมินตนเอง'"
    after(page, "() => { state.view.tab='kpi'; openDrawer('viewAppr','A2'); }")
    # ให้คะแนนตนเองไม่ครบ → บล็อก
    st0 = ev(page, "() => appr('A2').status")
    after(page, "() => saveSelf('A2')")
    assert ev(page, "() => appr('A2').status") == st0, "ให้คะแนนตนเองไม่ครบแต่บันทึกผ่าน"
    # ให้คะแนนครบ (1-5) → ส่งต่อหัวหน้า (status→mgr)
    after(page, "() => { appr('A2').kpis.forEach(k=>k.self=4); }")
    after(page, "() => saveSelf('A2')")
    assert ev(page, "() => appr('A2').status") == "mgr", "ประเมินตนเองครบแล้วไม่ส่งต่อหัวหน้า (status!=mgr)"
    return "ประเมินตนเอง: ไม่ครบ=บล็อก · ครบ 1-5 → ส่งต่อหัวหน้า (self→mgr)"


def c_fn04(page):
    """[FN-04 · S-04 · BR-04] หัวหน้าประเมิน + คะแนนรวมถ่วงน้ำหนักถูกต้อง"""
    open_(page)
    assert ev(page, "() => appr('A3').status") == "mgr", "A3 ควรอยู่สถานะ 'หัวหน้าประเมิน'"
    after(page, "() => { state.view.tab='kpi'; openDrawer('viewAppr','A3'); }")
    # ให้คะแนนหัวหน้าไม่ครบ → บล็อก
    after(page, "() => saveMgr('A3')")
    assert ev(page, "() => appr('A3').status") == "mgr", "หัวหน้าให้คะแนนไม่ครบแต่บันทึกผ่าน"
    # A3 kpis w 50/50 · mgr 4,5 → ถ่วงน้ำหนัก = (4*50+5*50)/100 = 4.50
    after(page, "() => { const a=appr('A3'); a.kpis[0].mgr=4; a.kpis[1].mgr=5; }")
    score = ev(page, "() => rawScore(appr('A3'))")
    assert abs(score - 4.5) < 1e-9, f"คะแนนรวมถ่วงน้ำหนักผิด: ได้ {score} (ควร 4.50)"
    assert ev(page, "() => scoreText(appr('A3'))") == "4.50", "scoreText ไม่แสดง 4.50"
    after(page, "() => saveMgr('A3')")
    assert ev(page, "() => appr('A3').status") == "calibration", "บันทึกหัวหน้าแล้วไม่ส่งเข้าสอบทาน (status!=calibration)"
    return "หัวหน้าประเมิน: ไม่ครบ=บล็อก · (4·50+5·50)/100 = 4.50 ถูกต้อง · mgr→calibration"


def c_fn09(page):
    """[FN-09 · S-08 · BR-09] ประเมินเกินกำหนด → เตือน + ปุ่มส่งการเตือน"""
    open_(page)
    # A2 due 2026-09-05 < TODAY 2026-09-09 · ยังไม่ published → overdue
    assert ev(page, "() => isOverdue(appr('A2'))") is True, "A2 ควรเกินกำหนด (isOverdue)"
    go_tab(page, "appr")
    pt = pc_text(page)
    assert "เกินกำหนด" in pt, "หน้ารายคนไม่แสดงป้าย 'เกินกำหนด'"
    assert "เตือนผู้ประเมิน" in pt or "แบบประเมินเกินกำหนด" in pt, "ไม่มี banner เตือนแบบประเมินเกินกำหนด"
    assert ev(page, "() => !!document.querySelector('.note.is-warn button')"), "ไม่มีปุ่มส่งการเตือนใน banner"
    after(page, "() => sendReminder()")
    assert "เตือน" in toast_text(page), "กดส่งการเตือนแล้วไม่ขึ้น toast"
    return "เกินกำหนด: A2 (ครบ 5 ก.ย.) → ป้าย+banner เตือน + ปุ่มส่งการเตือน"


def c_fn05(page):
    """[FN-05 · S-05 · BR-05] สอบทานผล (calibration แบบแยกจังหวะ · FIX-06) + บันทึก decision"""
    open_(page)
    assert ev(page, "() => appr('A4').status") == "calibration", "A4 ควรรอสอบทาน"
    after(page, "() => openModal('doaCalib',{id:'A4'})")
    assert "RESTRICTED" in modal_text(page), "modal สอบทานไม่ระบุผล/คะแนน = RESTRICTED"  # คงคำ RESTRICTED สำหรับ masking (Rule #81)
    # จังหวะ 1 · เลือกผู้สอบทาน 2 ขั้น (slot ว่าง) → ส่งสอบทาน = freeze รายชื่อ · สถานะคง calibration (ยังไม่ publish)
    after(page, "() => { ssPick('doa0',0); ssPick('doa1',1); }")
    after(page, "() => doCalibSend('A4')")
    assert ev(page, "() => appr('A4').status") == "calibration", "ส่งสอบทานแล้วไม่ควร publish ทันที (ต้องคง calibration)"
    assert ev(page, "() => (appr('A4').approvals||[]).length") == 2, "ส่งสอบทานแล้วไม่ freeze ผู้สอบทาน 2 ขั้น"
    assert ev(page, "() => appr('A4').approvals[0].status") == "current" and \
        ev(page, "() => appr('A4').approvals[1].status") == "pending", "ขั้น 1 ต้อง current · ขั้น 2 ต้อง pending"
    # จังหวะ 2 · ผู้สอบทานขั้น 1 บันทึกผล → stamp at · ยังคง calibration
    after(page, "() => doCalibStage('A4')")
    assert ev(page, "() => appr('A4').status") == "calibration", "บันทึกขั้น 1 แล้วไม่ควร publish (ยังไม่ถึงขั้นสุดท้าย)"
    assert ev(page, "() => appr('A4').approvals[0].status=='done' && !!appr('A4').approvals[0].at"), "ขั้น 1 ต้อง done + มี at (timeline)"
    assert ev(page, "() => appr('A4').approvals[1].status") == "current", "ขั้น 2 ต้องเลื่อนเป็น current"
    # ขั้นสุดท้าย · เลือก decision (ผลการตัดสิน) = ไม่ผ่าน → บันทึก → publish
    assert ev(page, "() => !!document.getElementById('p_dec')"), "ขั้นสุดท้ายไม่มีช่องบันทึกผลการตัดสิน (decision)"
    after(page, "() => { document.getElementById('p_dec').value='ไม่ผ่าน'; }")
    after(page, "() => doCalibStage('A4')")
    assert ev(page, "() => appr('A4').status") == "published", "บันทึกขั้นสุดท้ายแล้วไม่ published"
    assert ev(page, "() => appr('A4').decision") == "ไม่ผ่าน", "ไม่บันทึก decision ที่เลือก"
    assert ev(page, "() => appr('A4').approvals[1].at != null"), "ขั้น 2 ไม่ stamp at"
    assert ev(page, "() => PERF.notifs[0].b.indexOf('เผยแพร่')>=0"), "ไม่ยิงแจ้งเตือนผลเผยแพร่"
    return "สอบทานแยกจังหวะ: ส่งสอบทาน(คง calibration)→บันทึกขั้น1→ขั้นสุดท้าย publish · decision='ไม่ผ่าน' · ทุกขั้นมี at"


def c_fn08(page):
    """[FN-08 · S-05 · BR-05] สอบทานผ่าน DOA slot picker ตามตำแหน่ง — ไม่ hardcode · slot ว่าง (FIX-06a)"""
    open_(page)
    after(page, "() => openModal('doaCalib',{id:'A4'})")
    # 2 slot picker · option = คนจริงจาก PERF.people (label + ตำแหน่ง·แผนก) — resolve ตามตำแหน่ง
    assert ev(page, "() => !!document.getElementById('ss-doa0') && !!document.getElementById('ss-doa1')"), \
        "ไม่มีช่องเลือกผู้สอบทาน 2 ขั้น"
    optok = ev(page, """() => { const s=window.__ss['doa0'];
      return s && s.options.length>=3 && s.options.every(o=>o.label && o.sub); }""")
    assert optok, "slot picker ไม่ใช่รายชื่อคนจริง (ขาดชื่อ/ตำแหน่ง)"
    npeople = ev(page, "() => window.__ss['doa0'].options.length")
    assert npeople == ev(page, "() => PERF.people.length"), "ตัวเลือกไม่ได้ resolve จาก PERF.people (อาจ hardcode)"
    # FIX-06a · เปิดมา slot ต้องว่างทั้งคู่ (ไม่ preset P1/P2)
    assert ev(page, "() => window.__ss['doa0'].value == null && window.__ss['doa1'].value == null"), \
        "slot ผู้สอบทานถูก preset ค่ามาให้ (ต้องว่างทั้งคู่ · FIX-06a)"
    # ยังไม่เลือก → ส่งสอบทานไม่ผ่าน (บังคับเลือกครบ · ไม่ freeze approvals)
    after(page, "() => doCalibSend('A4')")
    assert ev(page, "() => appr('A4').status") == "calibration" and ev(page, "() => !appr('A4').approvals"), \
        "slot ว่างแต่ส่งสอบทานผ่าน (ไม่บังคับเลือก)"
    # เลือกคนผ่าน picker จริง (คนละคนกับที่เคย default P1) แล้วส่งสอบทานได้
    after(page, "() => { ssPick('doa0',2); ssPick('doa1',0); }")   # ขั้น 1 = P3 วิชัย · ขั้น 2 = P1
    assert ev(page, "() => window.__ss['doa0'].value") == "P3", "เลือกผ่าน picker แล้วค่าไม่ผูกตามที่เลือก"
    after(page, "() => doCalibSend('A4')")
    assert ev(page, "() => (appr('A4').approvals||[]).length") == 2, "เลือกครบแล้วส่งสอบทานไม่ freeze ผู้สอบทาน"
    assert ev(page, "() => appr('A4').approvals[0].personId") == "P3", "ผู้สอบทานขั้น 1 ไม่ผูกตามคนที่เลือก (P3)"
    # เดินขั้นจนเผยแพร่ (ขั้น 1 → ขั้นสุดท้าย)
    after(page, "() => doCalibStage('A4')")
    after(page, "() => doCalibStage('A4')")
    assert ev(page, "() => appr('A4').status") == "published", "เดินครบขั้นแล้วสอบทานไม่ published"
    return "DOA picker 2 ขั้น · option=คนจาก PERF.people (ไม่ hardcode) · slot ว่าง · ว่าง=บล็อก · เลือกเองผูกตามที่เลือก (P3)"


def c_fn06(page):
    """[FN-06 · S-06 · BR-06] ผลออก → ระบุ gap → ส่งต่อ Training (hook display-only)"""
    open_(page)
    go_tab(page, "review")
    pt = pc_text(page)
    assert "Gap" in pt and "ส่งไปอบรม" in pt, "หน้าผล & Gap ไม่มีปุ่มส่งไปอบรม (hook)"
    # A5 published + gap → เรียก hook แล้วเป็น display-only (ไม่สร้างหลักสูตร · ไม่ mutate)
    apprs0 = ev(page, "() => JSON.stringify(PERF.apprs)")
    after(page, "() => sendTraining('A5')")
    tt = toast_text(page)
    assert "อบรม" in tt and ("hook" in tt or "ไม่สร้างหลักสูตร" in tt), f"hook Training ไม่ใช่ display-only: '{tt}'"
    assert ev(page, "() => JSON.stringify(PERF.apprs)") == apprs0, "hook Training mutate ข้อมูล (ควร display-only)"
    return "Gap → ส่งไปอบรม (hook Training) display-only · ไม่สร้างหลักสูตร · ไม่ mutate"


def c_fn07(page):
    """[FN-07 · S-07 · BR-07] ผล → ส่ง event ปรับเงินเดือน/เลื่อนตำแหน่งให้ Movement (ไม่ปรับเอง)"""
    open_(page)
    go_tab(page, "review")
    assert "ส่งเรื่องปรับตำแหน่ง/เงินเดือน" in pc_text(page), "หน้าผลไม่มีปุ่มส่งเรื่องให้ระบบโยกย้าย"  # microcopy: ตัดคำ event ออกจากปุ่ม (Rule #81)
    apprs0 = ev(page, "() => JSON.stringify(PERF.apprs)")
    after(page, "() => sendMovement('A5')")
    tt = toast_text(page)
    assert "ไม่ปรับเอง" in tt, f"movement ไม่ใช่ display-only (ต้องระบุ 'ไม่ปรับเอง'): '{tt}'"  # microcopy: ตัดคำ event ออกจาก toast (Rule #81)
    assert ev(page, "() => JSON.stringify(PERF.apprs)") == apprs0, "ส่ง event โยกย้ายแล้ว mutate ข้อมูล (ควรส่ง event เท่านั้น)"
    return "ผล → ส่ง event ปรับเงินเดือน/เลื่อนตำแหน่งให้ Movement (ไม่ปรับเอง · ไม่ mutate)"


def c_fn10(page):
    """[FN-10 · S-09 · BR-05] คะแนนต่ำ/ทบทวน → เปิดแผน PIP + decision"""
    open_(page)
    # A6 published · decision 'ทบทวน (PIP)' → ปุ่ม PIP โผล่ · A5 (ผ่าน) ไม่มี PIP
    after(page, "() => { state.view.tab='detail'; openDrawer('viewAppr','A5'); }")
    assert "PIP" not in drawer_text(page) or "เปิดแผน PIP" not in drawer_text(page), \
        "A5 (decision ผ่าน) ไม่ควรมีปุ่มเปิด PIP"
    after(page, "() => closeDrawer()")
    after(page, "() => openModal('pip',{id:'A6'})")
    mt = modal_text(page)
    assert "PIP" in mt and "ทบทวน" in mt, "modal PIP ไม่ผูกกับ decision ทบทวน"
    n0 = ev(page, "() => (PERF.audit['A6']||[]).length")
    after(page, "() => { document.getElementById('pip_gap').value='ปรับปรุงความแม่นยำ'; }")
    after(page, "() => doPip('A6')")
    assert ev(page, "() => appr('A6').gap") == "ปรับปรุงความแม่นยำ", "เปิด PIP แล้วไม่บันทึก gap ที่แก้"
    assert ev(page, "() => (PERF.audit['A6']||[]).length") == n0 + 1, "เปิด PIP แล้ว audit ไม่เพิ่ม"
    assert ev(page, "() => PERF.audit['A6'][0].act.indexOf('PIP')>=0"), "audit ไม่บันทึกการเปิด PIP"
    return "PIP: A6 (ทบทวน) เปิดแผน+บันทึก gap+audit · A5 (ผ่าน) ไม่มีปุ่ม PIP"


def c_fn12(page):
    """[FN-12 · S-11 · BR-08] แจ้งเตือน รอบเปิด / ครบกำหนด / ผลเผยแพร่"""
    open_(page)
    # seed มี 3 event ครบ 3 หมวด
    assert ev(page, "() => PERF.notifs.length") >= 3, "notif seed ไม่ครบ 3 หมวด"
    after(page, "() => toggleNotif()")
    p = ev(page, "() => (document.getElementById('notifPanel')||{}).textContent || ''")
    assert "รอบเปิด" in p and "ครบกำหนด" in p and "ผล" in p, "หัว panel ไม่ครอบ 3 หมวด (รอบเปิด·ครบกำหนด·ผล)"
    assert "เปิดกรอกแล้ว" in p, "ไม่มี event รอบเปิด"
    assert "ใกล้ครบกำหนด" in p, "ไม่มี event ครบกำหนด"
    assert "เผยแพร่แล้ว" in p, "ไม่มี event ผลเผยแพร่"
    return "notification 3 หมวด: รอบเปิด · ครบกำหนด · ผลเผยแพร่ (panel + seed ครบ)"


def c_fn13(page):
    """[FN-13 · S-12 · BR-08] รายงานการกระจายคะแนน (distribution) + filter รอบ"""
    open_(page)
    go_tab(page, "report")
    # CY1 (default): มีคะแนน 3 คน (A4=4.60 ดีเยี่ยม · A5=4.00 ดี · A6=2.30 ต่ำ)
    base_in = ev(page, "() => PERF.apprs.filter(a=>a.cycle==='CY1').length")
    assert base_in == 6 and "การกระจายคะแนน" in pc_text(page), "รายงาน baseline (CY1) ผิด"
    # กระจายคะแนน: ต่ำ 1 · ดี 1 · ดีเยี่ยม 1
    dist = ev(page, """() => { const bk={low:0,mid:0,good:0,top:0};
      PERF.apprs.filter(a=>a.cycle===state.f.repCycle||state.f.repCycle==='all').forEach(a=>{const s=rawScore(a);
        if(s!=null){ if(s<3)bk.low++; else if(s<4)bk.mid++; else if(s<=4.5)bk.good++; else bk.top++; }}); return bk; }""")
    assert dist == {"low": 1, "mid": 0, "good": 1, "top": 1}, f"การกระจายคะแนน CY1 ผิด: {dist}"
    # filter รอบ → CY2 (ไม่มีแบบประเมิน) → รายงานว่าง
    after(page, "() => { state.f.repCycle='CY2'; refreshView(); }")
    empty = ev(page, "() => PERF.apprs.filter(a=>a.cycle==='CY2').length")
    assert empty == 0, "CY2 ควรไม่มีแบบประเมิน (ทดสอบ filter)"
    stat0 = ev(page, "() => (document.querySelector('.stat .stat-value')||{}).textContent")
    assert stat0 == "0", f"filter CY2 แล้ว stat 'แบบประเมินในรอบ' ไม่เป็น 0 (ได้ {stat0})"
    # filter → all → กลับมาครบ
    after(page, "() => { state.f.repCycle='all'; refreshView(); }")
    assert ev(page, "() => (document.querySelector('.stat .stat-value')||{}).textContent") == "6", "filter=all ไม่คืนทุกรอบ"
    return "รายงาน: CY1 กระจาย ต่ำ1·ดี1·ดีเยี่ยม1 · filter CY2=0 · all=6 — filter ทำงาน"


# ═══════════════════════════════ GENERAL FN ═══════════════════════════════

def c_fn90(page):
    """[FN-90] ค้นหา/filter ในรายการ + empty state"""
    open_(page)
    go_tab(page, "appr")
    after(page, "() => { state.f.search='zzzไม่มีจริง'; refreshView(); }")
    assert "ไม่พบแบบประเมินที่ค้นหา" in pc_text(page), "ค้นไม่เจอแต่ไม่ขึ้น empty state"
    after(page, "() => { state.f.search='อรทัย'; refreshView(); }")
    t2 = pc_text(page)
    assert "อรทัย แสนสุข" in t2 and "ไม่พบแบบประเมินที่ค้นหา" not in t2, "ค้นเจอแต่ไม่แสดงผล"
    # filter สถานะ
    after(page, "() => { state.f.search=''; state.f.status='goal'; refreshView(); }")
    t3 = pc_text(page)
    assert "มะลิ ดอกไม้" in t3 and "อรทัย แสนสุข" not in t3, "filter สถานะ (goal) ไม่ทำงาน"
    return "search: เจอ/ไม่เจอ+empty · filter สถานะ goal กรองถูกต้อง"


def c_fn91(page):
    """[FN-91] ปิด/ยกเลิกผ่าน confirm + soft archive (ยกเลิก confirm = ไม่ทำ)"""
    open_(page)
    after(page, "() => openDrawer('viewCycle','CY1')")
    after(page, "() => openModal('closeCycle',{id:'CY1'})")
    assert ev(page, "() => state.modal.type==='closeCycle'"), "ปิดรอบไม่ผ่าน confirm modal"
    # ยกเลิก confirm → ต้องไม่ปิดรอบ
    after(page, "() => closeModal()")
    assert ev(page, "() => cyc('CY1').status") == "open", "ยกเลิก confirm แล้วรอบยังถูกปิด (confirm gate พัง)"
    # ยืนยันจริง → closed + record คงอยู่ (soft archive)
    n0 = ev(page, "() => PERF.cycles.length")
    after(page, "() => openModal('closeCycle',{id:'CY1'})")
    after(page, "() => doCloseCycle('CY1')")
    assert ev(page, "() => cyc('CY1').status") == "closed", "confirm แล้วไม่ปิดรอบ"
    assert ev(page, "() => PERF.cycles.length") == n0, "soft archive แต่ record หาย"
    return "confirm gate: ยกเลิก=ไม่ปิด · ยืนยัน=closed + record คงอยู่ (soft)"


def c_fn92(page):
    """[FN-92] validate field บังคับก่อนบันทึก + กัน double-submit (loader)"""
    open_(page)
    # (ก) validate: สร้างรอบโดยไม่เลือก config → บล็อก + field error
    n0 = ev(page, "() => PERF.cycles.length")
    after(page, "() => openDrawer('newCycle')")
    after(page, "() => submitNewCycle()")
    assert ev(page, "() => PERF.cycles.length") == n0, "ไม่เลือกรอบแต่สร้างได้ (validate ไม่บล็อก)"
    assert ev(page, "() => document.getElementById('err-cfg').closest('.field').classList.contains('is-invalid')"), \
        "validate ไม่ผ่านแต่ field ไม่ขึ้น is-invalid"
    assert ev(page, "() => state.drawer.open") is True, "validate ไม่ผ่านแต่ลิ้นชักปิด (ควรค้างให้แก้)"
    # (ข) double-submit: เลือกแล้วกดส่ง → ปุ่มถูกล็อก + loader (อ่านทันทีก่อน setTimeout ทำงาน)
    after(page, "() => ssPick('cfgCycle',0)")
    lock = ev(page, "() => { submitNewCycle(); const b=document.getElementById('btnNewCycle'); return b?{cls:b.className, html:b.innerHTML}:null; }")
    assert lock and "is-disabled" in lock["cls"], "กดส่งแล้วปุ่มไม่ถูกล็อก (double-submit ไม่กัน)"
    assert "spin" in lock["html"] or "กำลังบันทึก" in lock["html"], "ไม่มี loader ระหว่างบันทึก"
    assert ev(page, "() => state._busy") is True, "ไม่ตั้ง _busy guard ระหว่างบันทึก"
    settle(page)
    return "validate: ไม่เลือก config = บล็อก+is-invalid · กดส่ง=ปุ่มล็อก+loader+_busy (กัน double-submit)"


def c_fn93(page):
    """[FN-93] audit ทุก create/แก้/สอบทาน (append-only · เรียงใหม่บนสุด)"""
    open_(page)
    after(page, "() => { state.view.tab='history'; openDrawer('viewAppr','A5'); }")
    dt = drawer_text(page)
    assert "append-only" in dt, "ประวัติไม่ระบุ append-only"
    log = ev(page, "() => PERF.audit['A5']")
    assert log and len(log) >= 3, f"audit A5 ควรมีหลายรายการ ได้ {log and len(log)}"
    assert any("เผยแพร่ผล" in x["act"] for x in log), "audit ไม่บันทึกการเผยแพร่ผล"
    # append proof: บันทึกผลหัวหน้าของ A3 → audit เพิ่ม 1 รายการบนสุด (unshift · append-only)
    n0 = ev(page, "() => (PERF.audit['A3']||[]).length")
    after(page, "() => { const a=appr('A3'); a.kpis.forEach(k=>k.mgr=4); saveMgr('A3'); }")
    n1 = ev(page, "() => (PERF.audit['A3']||[]).length")
    assert n1 == n0 + 1, f"บันทึกหัวหน้าแล้ว audit ไม่ append (n0={n0} n1={n1})"
    assert ev(page, "() => PERF.audit['A3'][0].act.indexOf('หัวหน้าประเมิน')>=0"), "รายการใหม่ไม่ขึ้นบนสุด (ไม่ append-only)"
    return f"audit append-only: A5 {len(log)} รายการ (มีเผยแพร่ผล) · save หัวหน้า → append บนสุด (+1)"


def c_fn94(page):
    """[FN-94 · BR-08] ปิดบังผลประเมิน (RESTRICTED) ตาม role ผ่าน demo strip"""
    open_(page)
    # demo strip 3 role
    assert ev(page, "() => document.querySelectorAll('.demo-strip .seg-item').length") == 3, "ไม่มี demo strip เลือก 3 role"
    go_tab(page, "appr")
    # role พนักงาน (staff · mask=true) → คะแนนถูกปิดบัง (masked · ไม่เห็นเลข)
    after(page, "() => setRole('staff')")
    masked = pc_text(page)
    masked_html = ev(page, "() => document.getElementById('page-content').innerHTML")
    assert "masked" in masked_html, "role staff แต่ไม่มี element ปิดบัง (.masked)"
    assert "4.60" not in masked and "2.30" not in masked, "role staff แต่ยังเห็นคะแนนจริง (ไม่ mask)"
    # role HR (mask=false) → เห็นคะแนน
    after(page, "() => setRole('hr')")
    full = pc_text(page)
    assert "4.60" in full and "4.00" in full, "role HR กลับถูก mask (ควรเห็นคะแนน)"
    # helper mask ผูกกับ role จริง
    assert ev(page, "() => { setRole('staff'); return curRole().mask; }") is True, "staff mask ควร true"
    assert ev(page, "() => { setRole('hr'); return curRole().mask; }") is False, "hr mask ควร false"
    return "mask ตาม role: staff=ปิดบัง (masked·ไม่เห็นเลข) · HR=เห็นคะแนน (4.60/4.00)"


# ═══════════════════ NEGATIVE (unsupported ×4, rendered → absent) ═══════════════════

NEG_JS = r"""
() => {
  let html='';
  state.role='hr';
  // pages ทุก tab
  ['cycle','appr','review','report'].forEach(t=>{ state.tab=t; html+=pageHTML(); });
  // drawers ทุกโหมด
  state.drawer={open:true,mode:'newCycle',recordId:null,step:1}; html+=drawerHTML();
  state.drawer={open:true,mode:'viewCycle',recordId:'CY1',step:1}; html+=drawerHTML();
  state.edit=null; state.view.tab='kpi'; state.drawer={open:true,mode:'viewAppr',recordId:'A1',step:1}; html+=drawerHTML();
  ['detail','kpi','calib','history'].forEach(tab=>{ state.view.tab=tab; state.drawer={open:true,mode:'viewAppr',recordId:'A6',step:1}; html+=drawerHTML(); });
  // modals ทุกชนิด
  [['doaCalib',{id:'A4'}],['closeCycle',{id:'CY1'}],['pip',{id:'A6'}]].forEach(m=>{
    state.modal={open:true,type:m[0],data:m[1]}; html+=modalHTML(); });
  const box=document.createElement('div'); box.innerHTML=html;
  const acts=[...box.querySelectorAll('button,[onclick]')].filter(el=>{
    const h=(el.getAttribute('onclick')||'').replace(/\s/g,'');
    return !/^event\.stopPropagation\(\)$/.test(h);
  }).map(el=>({txt:(el.textContent||'').replace(/\s+/g,' ').trim(), on:(el.getAttribute('onclick')||'')}));
  return {
    acts,
    fullText: box.textContent||'',
    hasDisplayOnly: /ส่งต่อผล/.test(html),
    hasNotAdjust: /ไม่ปรับเอง/.test(html),
    hasReadConfig: /อ่านจาก ตั้งค่า HR|appraisal_cycle/.test(html),
    hasNoFormEdit: /ไม่สร้าง\/แก้ฟอร์มกลาง|ไม่สร้าง.{0,3}แก้ฟอร์มกลาง/.test(html),
    hasTrainingHook: /ส่งไปอบรม/.test(html),
  };
}
"""


def c_unsupported(page):
    """[NEG · unsupported ×4] เรนเดอร์ทุก affordance จริงแล้ว assert 'ไม่มี' ของห้ามมี"""
    open_(page)
    r = ev(page, NEG_JS)
    acts = r["acts"]
    full = r["fullText"]

    def hit(pat):
        rx = re.compile(pat, re.I)
        return [a for a in acts if rx.search(a["txt"]) or rx.search(a["on"])]

    assert len(acts) > 10, f"เก็บ affordance ได้น้อยผิดปกติ ({len(acts)}) — surfaces อาจไม่เรนเดอร์"

    # 1) ไม่มีปรับเงินเดือน/เลื่อนตำแหน่ง "เอง" — อนุญาตเฉพาะ display-only ส่ง event ให้ Movement (sendMovement)
    v1 = [a for a in acts
          if re.search(r"ปรับเงินเดือน|บันทึกเงินเดือน|ตั้งเงินเดือน|แก้เงินเดือน|เลื่อนตำแหน่ง|setSalary|editSalary|adjustSalary|savePromotion|promote\(|payroll",
                       a["txt"] + " " + a["on"], re.I)
          and "sendMovement" not in a["on"]]
    assert not v1, f"[neg1] พบ affordance ปรับเงินเดือน/เลื่อนตำแหน่งเอง (นอก event display-only): {v1[:3]}"
    assert r["hasDisplayOnly"] and r["hasNotAdjust"], "[neg1] การส่งต่อผลควรเป็น display-only event (ไม่ปรับเอง)"

    # 2) ไม่มี 360 feedback / competency model / continuous check-in
    assert not re.search(r"360|competency|สมรรถนะ|check-?in|เช็คอิน|รอบด้าน|ต่อเนื่อง.*ประเมิน", full, re.I), \
        "[neg2] พบร่องรอย 360 / competency / continuous check-in บนจอ"
    v2 = hit(r"360|competency|สมรรถนะ|checkIn|continuousReview")
    assert not v2, f"[neg2] พบ affordance 360/competency/check-in: {v2[:3]}"

    # 3) ไม่มีสร้าง/แก้รอบประเมิน-แบบฟอร์มกลาง (create cycle = อ่าน config เท่านั้น)
    v3 = hit(r"สร้างแบบฟอร์ม|แก้แบบฟอร์ม|สร้างแบบประเมิน|แก้แบบประเมิน|เพิ่มหัวข้อประเมิน|แก้ฟอร์มกลาง|สร้างฟอร์มกลาง|formBuilder|createForm|editForm|createTemplate")
    assert not v3, f"[neg3] พบ affordance สร้าง/แก้แบบฟอร์มประเมินกลาง: {v3[:3]}"
    assert r["hasReadConfig"], "[neg3] สร้างรอบควรอ่านจาก HR Configuration (appraisal_cycle)"

    # 4) ไม่มีสร้าง/แก้หลักสูตรอบรม (อนุญาตเฉพาะ hook 'ส่งไปอบรม')
    v4 = hit(r"สร้างหลักสูตร|เพิ่มหลักสูตร|แก้หลักสูตร|จัดการหลักสูตร|createCourse|newCourse|editCourse")
    assert not v4, f"[neg4] พบ affordance สร้าง/แก้หลักสูตรอบรม: {v4[:3]}"
    assert r["hasTrainingHook"], "[neg4] ควรมี hook 'ส่งไปอบรม' (display-only) แต่ไม่พบ"

    return f"unsupported 4/4 absent ({len(acts)} affordance ตรวจ · ส่งต่อผล=display-only event/hook)"


# ═══════════════════ BASE-KIT REGRESSION (DSP · recurs ทุก HR feature) ═══════════════════

def c_dsp01(page):
    """[DSP-01] modal เปิดในลิ้นชัก z ต้องอยู่เหนือ drawer (JS_MODAL_UNDER_DRAWER)"""
    open_(page)
    # เปิดลิ้นชัก viewAppr (A4 รอสอบทาน) → กดปุ่มในลิ้นชักเปิด modal สอบทาน (modal ซ้อนบน drawer)
    after(page, "() => openDrawer('viewAppr','A4')")
    after(page, "() => openModal('doaCalib',{id:'A4'})")
    assert ev(page, "() => state.drawer.open && state.modal.open"), "ต้องมีทั้ง drawer + modal เปิดพร้อมกัน"
    buried = ev(page, JS_MODAL_UNDER_DRAWER)
    assert not buried, f"modal จมใต้ drawer (DSP-01): {buried[:3]}"
    return "modal (doaCalib) เปิดจากในลิ้นชัก → z อยู่เหนือ drawer (ไม่จม)"


def c_dsp02a(page):
    """[DSP-02a] เลือก combobox แล้ว dropdown ต้องปิด (reopen-after-select)"""
    open_(page)
    # cfgCycle ในลิ้นชักสร้างรอบ
    after(page, "() => openDrawer('newCycle')")
    st_cfg = assert_combobox_closes_after_select(page, "cfgCycle", 0)
    # doa0 ใน modal สอบทาน
    open_(page)
    after(page, "() => openModal('doaCalib',{id:'A4'})")
    st_doa = assert_combobox_closes_after_select(page, "doa0", 1)
    return f"เลือกแล้วปิด: cfgCycle open={st_cfg['open']} · doa0 open={st_doa['open']} (ทั้งคู่ปิด+โชว์ค่า)"


def c_dsp02b(page):
    """[DSP-02b] เปิด modal แล้ว combobox ต้องไม่กางเอง (trapFocus auto-open)"""
    open_(page)
    after(page, "() => openModal('doaCalib',{id:'A4'})")
    autos = modal_autoopens_comboboxes(page, root_sel="#modalBackdrop .modal")
    assert not autos, f"combobox กางเองตอนเปิด modal (DSP-02b): {autos}"
    return "เปิด modal สอบทาน → combobox (doa0/doa1) ไม่กาง dropdown เอง"


def c_regression(page):
    """[REG] ไม่มี garbage text (NaN/undefined/[object Object]/Invalid Date) รั่วบนจอ

    หมายเหตุ: ไม่ใช้ JS_CSSVAR ที่นี่ — ไฟล์นี้ set custom prop แบบ inline (--w, --fw ผ่าน style=)
    และใช้ var แบบมี fallback (--shellbar-h,52px) ซึ่ง JS_CSSVAR (อ่านเฉพาะ <style>) จะฟ้องเป็น
    false-positive ทั้งที่ไม่ใช่ของพัง (C3.9 — สัญญาณหลอก ไม่ไล่แก้). CSS var ที่ควรประกาศจริง
    (--z-*, สี, ระยะ) ถูก qc-ux/self_audit ตรวจใน 3/4 อยู่แล้ว.
    """
    open_(page)
    # กวาดทุก tab + drawer + modal หา garbage text
    assert_no_garbage_text(page, scope="#page-content")
    go_tab(page, "appr")
    assert_no_garbage_text(page, scope="#page-content")
    go_tab(page, "report")
    assert_no_garbage_text(page, scope="#page-content")
    after(page, "() => { state.view.tab='kpi'; openDrawer('viewAppr','A4'); }")
    assert_no_garbage_text(page, scope="#drawer")
    after(page, "() => openModal('doaCalib',{id:'A4'})")
    assert_no_garbage_text(page, scope="#modalBackdrop .modal")
    return "regression: ไม่มี garbage text รั่วบนจอ (page ทุก tab + drawer + modal)"


# ═══════════════════ §C3.8 · manual-test bugs — เพิ่มการตรวจกันหลุดซ้ำ ═══════════════════

def c_bug3_mgr_edit(page):
    """[FN-04 · BUG-3] persona 'หัวหน้าสายงาน' ต้องกรอกคะแนนหัวหน้าได้ (permission reachability)

    root cause: mgrEdit = a.status==='mgr' && curRole().manage → manage=true เฉพาะ HR
    → หัวหน้า (mgr manage:false) เข้าหน้าประเมินหัวหน้าไม่ได้ ทั้งที่เป็นงานของ FN-04
    """
    open_(page)
    # สลับ persona เป็นหัวหน้าสายงาน แล้วเปิด A3 (อรทัย แสนสุข · status mgr) ที่แท็บ KPI/คะแนน
    after(page, "() => { setRole('mgr'); state.view.tab='kpi'; openDrawer('viewAppr','A3'); }")
    assert ev(page, "() => curRole().id") == "mgr", "ไม่ได้อยู่ persona หัวหน้าสายงาน (mgr)"
    assert ev(page, "() => appr('A3').status") == "mgr", "A3 ควรอยู่สถานะ 'หัวหน้าประเมิน'"
    st = ev(page, """() => {
      const inps = [...document.querySelectorAll('#kpiScoreBody input.in')];
      return { n: inps.length, disabled: inps.filter(i=>i.disabled).length,
               hasBtn: /บันทึกผลหัวหน้า/.test((document.getElementById('btnMgr')||{}).textContent||''),
               hasLive: !!document.getElementById('liveScore') };
    }""")
    assert st["n"] >= 2, f"หัวหน้าเปิด A3 แล้วไม่มีช่องกรอกคะแนนหัวหน้า (ได้ {st['n']}) — permission บล็อกผิด"
    assert st["disabled"] == 0, f"ช่องกรอกคะแนนหัวหน้าถูก disable {st['disabled']} ช่อง (ควรกรอกได้)"
    assert st["hasBtn"], "ไม่มีปุ่ม 'บันทึกผลหัวหน้า' สำหรับ persona หัวหน้า"
    assert st["hasLive"], "ไม่มี element คะแนนสด (#liveScore) ให้หัวหน้า"
    # live weighted score ต้องอัปเดตจริง — A3 w 50/50 · mgr 4,5 → (4·50+5·50)/100 = 4.50
    live = ev(page, """() => {
      const inps=[...document.querySelectorAll('#kpiScoreBody input.in')];
      inps[0].value='4'; inps[1].value='5'; onScoreInput();
      return (document.getElementById('liveScore')||{}).textContent||'';
    }""")
    assert live.strip().startswith("4.50"), f"คะแนนสดของหัวหน้าไม่อัปเดต (ได้ '{live}' · ควร 4.50 / 5)"
    return "หัวหน้าสายงานกรอกคะแนนหัวหน้าได้ (ช่อง+ปุ่ม+#liveScore) · คะแนนสด 4.50 อัปเดตจริง"


def c_bug1_footer(page):
    """[BUG-1] footer ลิ้นชักต้องปักก้น ไม่ลอยกลางแผง (.drawer-panel fill drawer)

    root cause: .drawer-panel ไม่มี layout CSS → panel ยุบ → drawer-body ขยายไม่ได้ → footer ลอย
    """
    open_(page)
    # เนื้อหาสั้น (newCycle) — เห็นช่องว่างใต้ footer ชัดสุด
    after(page, "() => openDrawer('newCycle')")
    r_short = assert_drawer_footer_pinned(page)
    # เนื้อหายาว (viewAppr A6 · แท็บประวัติ) — footer ต้องปักก้นเช่นกัน (body เลื่อนแทน)
    open_(page)
    after(page, "() => { state.view.tab='history'; openDrawer('viewAppr','A6'); }")
    r_long = assert_drawer_footer_pinned(page)
    return f"footer ปักก้นทั้ง newCycle (gap {r_short['gapBelow']}px) และ viewAppr (gap {r_long['gapBelow']}px)"


def c_bug2_filtergap(page):
    """[BUG-2] แถวกรอง Tab 2 ไม่มีช่องว่างใหญ่ (ตัด .fr-spacer ออก)"""
    open_(page)
    go_tab(page, "appr")
    # ใส่ค้นหาให้ปุ่ม 'ล้างตัวกรอง' เรนเดอร์
    after(page, "() => { state.f.search='อรทัย'; refreshView(); }")
    r = ev(page, r"""() => {
      const fr = document.querySelector('#page-content .filter-row');
      if(!fr) return {err:'no-filter-row'};
      const spacer = fr.querySelector('.fr-spacer');
      const sel = fr.querySelector('select');
      const clr = [...fr.querySelectorAll('button')].find(b=>/ล้างตัวกรอง/.test(b.textContent||''));
      let gap=null;
      if(sel && clr) gap = Math.round(clr.getBoundingClientRect().left - sel.getBoundingClientRect().right);
      return { hasSpacer: !!spacer, hasClear: !!clr, gap };
    }""")
    assert not r.get("err"), r.get("err")
    assert r["hasSpacer"] is False, "fr-spacer ยังอยู่ในแถวกรอง Tab 2 (ดันปุ่มล้างตัวกรองห่างเป็นช่องว่างใหญ่)"
    assert r["hasClear"], "ใส่ค้นหาแล้วปุ่ม 'ล้างตัวกรอง' ไม่เรนเดอร์"
    assert r["gap"] is not None and r["gap"] < 48, \
        f"ช่องว่าง select→ปุ่มล้างตัวกรองกว้างผิดปกติ {r['gap']}px (ควร <48px · ไม่มี spacer ดัน)"
    return f"แถวกรอง Tab 2: ไม่มี .fr-spacer · select→ล้างตัวกรอง ห่าง {r['gap']}px (ชิด ไม่โหว่)"


# ═══════ BA-GATE BYPASS / GOVERNANCE (FIX-01..09 · re-gate) — เรียก controller ตรงแล้ว assert state ═══════

def c_p1_published_immutable(page):
    """[FN-02 · P1 · FIX-02] save* บน record ที่เผยแพร่แล้ว → state ไม่เปลี่ยน (ไม่ถอยสถานะ/แก้คะแนน)"""
    open_(page)
    assert ev(page, "() => appr('A5').status") == "published", "A5 ควร published (เตรียมเคส)"
    snap = ev(page, "() => JSON.stringify(appr('A5'))")
    for fn in ("saveSelf", "saveKpi", "saveMgr"):
        after(page, "() => %s('A5')" % fn)
        assert ev(page, "() => appr('A5').status") == "published", f"{fn} บน published แล้วสถานะเปลี่ยน (FIX-02 พลาด)"
    assert ev(page, "() => JSON.stringify(appr('A5'))") == snap, "save* บน published ทำ record เปลี่ยน (ควรคงเดิมทั้งก้อน)"
    return "published immutable: saveSelf/saveKpi/saveMgr(A5) → record ไม่เปลี่ยน (ไม่ถอยสถานะ/ไม่แก้คะแนน)"


def c_p2_calib_precondition(page):
    """[FN-05 · P2 · FIX-01] ส่งสอบทาน record ขั้นตั้งเป้า (คะแนนหัวหน้า null) → ไม่ publish"""
    open_(page)
    assert ev(page, "() => appr('A1').status") == "goal", "A1 ควรอยู่ขั้นตั้งเป้า"
    assert ev(page, "() => rawScore(appr('A1'))") is None, "A1 คะแนนหัวหน้าควร null ทั้งหมด"
    after(page, "() => openModal('doaCalib',{id:'A1'})")
    # เลือกผู้สอบทานครบทั้ง 2 ขั้น → เหลือ precondition (FIX-01) เป็นด่านเดียวที่กัน (prove-by-break ได้)
    after(page, "() => { ssPick('doa0',0); ssPick('doa1',1); }")
    after(page, "() => doCalibSend('A1')")
    assert ev(page, "() => appr('A1').status") == "goal", "goal-stage record ถูกส่งสอบทานได้ (FIX-01 พลาด)"
    assert ev(page, "() => !appr('A1').approvals"), "goal-stage record freeze approvals ได้ (ไม่ควร)"
    assert "ให้คะแนนหัวหน้าครบ" in toast_text(page) or "รอสอบทาน" in toast_text(page), \
        f"ไม่เตือน precondition ({toast_text(page)})"
    return "precondition: doCalibSend(A1 goal · mgr null) → ไม่ publish · ไม่ freeze · เตือน (FIX-01)"


def c_p3_role_guard(page):
    """[FN-04 · P3 · FIX-03/04] role พนักงาน: เรียก mutation ตรง → ไม่เปลี่ยน + ไม่เห็นปุ่ม + ไม่เห็นข้อมูลคนอื่น"""
    open_(page)
    after(page, "() => setRole('staff')")
    # (a) function guard — staff เรียก mutation ตรง → state ไม่เปลี่ยน
    # เติมคะแนนหัวหน้าครบ + คง status mgr → เหลือ role guard เป็นด่านเดียว (prove-by-break FIX-03 ได้)
    after(page, "() => { const a=appr('A3'); a.kpis.forEach(k=>k.mgr=4); }")
    st3 = ev(page, "() => appr('A3').status")
    assert st3 == "mgr", "A3 ควรอยู่ขั้นหัวหน้าประเมิน (เตรียมเคส)"
    after(page, "() => saveMgr('A3')")
    assert ev(page, "() => appr('A3').status") == st3 == "mgr", "staff เรียก saveMgr (คะแนนครบ) แล้วสถานะเปลี่ยน (FIX-03 function พลาด)"
    after(page, "() => doCalibSend('A4')")
    assert ev(page, "() => appr('A4').status") == "calibration" and ev(page, "() => !appr('A4').approvals"), \
        "staff เรียก doCalibSend แล้ว freeze/เปลี่ยนสถานะ (FIX-03)"
    g6 = ev(page, "() => appr('A6').gap")
    after(page, "() => doPip('A6')")
    assert ev(page, "() => appr('A6').gap") == g6, "staff เรียก doPip แล้ว gap เปลี่ยน (FIX-03)"
    assert "สิทธิ์ไม่พอ" in toast_text(page), f"staff เรียก mutation ไม่เตือนสิทธิ์ ({toast_text(page)})"
    # (b) UI — staff ไม่เห็นปุ่ม mutation ในแท็บสอบทาน (เช็คที่ปุ่มจริง · ไม่ใช่ข้อความบรรยายใน ph-sub)
    go_tab(page, "review")
    forbidden = ev(page, """() => [...document.querySelectorAll('#page-content button')]
        .map(b => b.getAttribute('onclick') || '')
        .filter(o => /doaCalib|'pip'|sendTraining|sendMovement|sendSuccession|doCalibSend|doCalibStage/.test(o))""")
    assert not forbidden, f"staff เห็นปุ่ม mutation ในแท็บสอบทาน (FIX-03 UI): {forbidden}"
    # มุม Calibration ระดับทีม (แสดงคะแนนทั้งทีม) ต้องไม่โผล่ให้พนักงาน
    assert_text_absent(page, ["Calibration ระดับทีม"], scope="#page-content")
    # (c) scope SELF — staff เห็นเฉพาะของตน (สมชาย ใจดี) · ชื่อ/decision/gap คนอื่นไม่อยู่ใน DOM
    go_tab(page, "appr")
    assert "สมชาย ใจดี" in pc_text(page), "staff ควรเห็นแบบประเมินของตนเอง (สมชาย ใจดี)"
    assert_text_absent(page, ["มะลิ ดอกไม้", "อรทัย แสนสุข", "ธนากร พูนผล", "กนกพร วงศ์ไทย",
                              "ปิยะ มั่นคง", "ทบทวน", "ทักษะการนำเสนอ", "ความถูกต้องในงาน"],
                       scope="#page-content")
    return "staff: saveMgr/doCalibSend/doPip → state คงเดิม+เตือนสิทธิ์ · ไม่เห็นปุ่ม mutation · เห็นเฉพาะของตน (คนอื่นไม่อยู่ใน DOM)"


def c_p4_closed_lock(page):
    """[FN-11 · P4 · FIX-05 · FIX-A] ปิดรอบแล้ว → mutation ถูกล็อกทั้ง (ก) ฟังก์ชัน save (FIX-05)
    และ (ข) front-end gate: KPI tab ไม่มี input แก้ไข + banner read-only + ปุ่ม mutation หายทั้ง drawer/review (FIX-A)"""
    open_(page)
    after(page, "() => doCloseCycle('CY1')")
    assert ev(page, "() => cyc('CY1').status") == "closed", "ปิดรอบไม่สำเร็จ (เตรียมเคส)"
    # (ก) function guard (FIX-05) — save ทุกตัวยัง block (defense-in-depth · ยังคงไว้)
    checks = [("saveSelf", "A2", "self"), ("saveMgr", "A3", "mgr"), ("saveKpi", "A1", "goal")]
    for fn, aid, expect in checks:
        after(page, "() => %s('%s')" % (fn, aid))
        assert ev(page, "() => appr('%s').status" % aid) == expect, \
            f"รอบปิดแล้วแต่ {fn}({aid}) ยัง mutate ได้ (สถานะเปลี่ยนจาก {expect})"
    after(page, "() => openModal('doaCalib',{id:'A4'})")
    after(page, "() => doCalibSend('A4')")
    assert ev(page, "() => appr('A4').status") == "calibration" and ev(page, "() => !appr('A4').approvals"), \
        "รอบปิดแล้วแต่ doCalibSend(A4) ยังทำงาน"
    assert "รอบนี้ปิดแล้ว" in toast_text(page), f"ไม่เตือนว่ารอบปิด ({toast_text(page)})"
    # (ข) FIX-A front-end gate — KPI tab ของรอบปิด: ไม่มี input แก้ไข (editor/self/mgr) + banner read-only
    for aid in ("A1", "A2", "A3"):
        after(page, "() => { state.view.tab='kpi'; openDrawer('viewAppr','%s'); }" % aid)
        n_edit = ev(page, "() => document.querySelectorAll('#drawer #kpiEditor input, #drawer #kpiScoreBody input').length")
        assert n_edit == 0, f"รอบปิดแต่ KPI tab ({aid}) ยังมี input แก้ไขได้ {n_edit} ช่อง (FIX-A front-end gate)"
        assert not ev(page, "() => Array.isArray(state.edit)"), f"รอบปิดแต่ {aid} ยังเข้า KPI editor (state.edit เป็น array)"
        assert "รอบนี้ปิดแล้ว" in drawer_text(page), f"KPI tab ({aid}) รอบปิดไม่ขึ้น banner read-only"
    # (ค) FIX-A — ปุ่ม mutation ถูกซ่อน: drawer footer (สอบทาน DOA / เปิดแผน PIP) + tabDetail hookbox ส่งต่อผล
    after(page, "() => { state.view.tab='detail'; openDrawer('viewAppr','A4'); }")
    foot4 = ev(page, "() => [...document.querySelectorAll('#drawer .drawer-footer button')].map(b=>b.textContent).join('|')")
    assert "สอบทาน (DOA)" not in foot4, f"รอบปิดแต่ footer A4 ยังมีปุ่มสอบทาน (DOA): {foot4}"
    after(page, "() => { state.view.tab='detail'; openDrawer('viewAppr','A6'); }")
    foot6 = ev(page, "() => [...document.querySelectorAll('#drawer .drawer-footer button')].map(b=>b.textContent).join('|')")
    assert "เปิดแผน PIP" not in foot6, f"รอบปิดแต่ footer A6 ยังมีปุ่มเปิดแผน PIP: {foot6}"
    after(page, "() => { state.view.tab='detail'; openDrawer('viewAppr','A5'); }")
    assert_text_absent(page, ["ส่งเรื่องปรับตำแหน่ง/เงินเดือน", "ส่งเข้า Succession"], scope="#drawer")
    # review view — closed ทุกใบใน CY1 → ไม่มีปุ่ม mutation หลงเหลือ
    after(page, "() => closeDrawer()")
    go_tab(page, "review")
    rv_forbidden = ev(page, """() => [...document.querySelectorAll('#page-content button')]
        .map(b => b.getAttribute('onclick') || '')
        .filter(o => /doaCalib|'pip'|sendTraining|sendMovement|sendSuccession/.test(o))""")
    assert not rv_forbidden, f"รอบปิดแต่ review view ยังมีปุ่ม mutation: {rv_forbidden}"
    return ("closed lock: (ก) fn guard saveSelf/saveMgr/saveKpi/doCalibSend block+เตือน · "
            "(ข) FIX-A front-end gate: KPI ไม่มี input + banner read-only · ปุ่ม mutation หายทั้ง drawer footer/hookbox/review")


def c_slot_staged(page):
    """[FN-06 · SLOT · FIX-06] modal เปิดมา slot ว่างทั้งคู่ · ไม่เลือก=block · publish หลังขั้นสุดท้ายเท่านั้น"""
    open_(page)
    after(page, "() => openModal('doaCalib',{id:'A4'})")
    assert ev(page, "() => window.__ss['doa0'].value == null && window.__ss['doa1'].value == null"), \
        "modal เปิดมา slot ไม่ว่าง (FIX-06a)"
    after(page, "() => doCalibSend('A4')")
    assert ev(page, "() => !appr('A4').approvals"), "ไม่เลือกครบแต่ freeze ได้"
    after(page, "() => { ssPick('doa0',0); ssPick('doa1',1); }")
    after(page, "() => doCalibSend('A4')")
    assert ev(page, "() => appr('A4').status") == "calibration", "publish เกิดในจังหวะเลือกผู้สอบทาน (ต้องแยก · FIX-06)"
    after(page, "() => doCalibStage('A4')")
    assert ev(page, "() => appr('A4').status") == "calibration", "publish ก่อนขั้นสุดท้าย"
    after(page, "() => doCalibStage('A4')")
    assert ev(page, "() => appr('A4').status") == "published", "ขั้นสุดท้ายแล้วไม่ publish"
    assert ev(page, "() => appr('A4').approvals.every(x=>x.status=='done' && x.at)"), "บางขั้นไม่มี at/ไม่ done"
    return "staged: slot ว่าง · ไม่เลือก=block · เลือกแล้วส่ง=คง calibration · publish หลังขั้นสุดท้าย · ทุกขั้นมี at"


def c_csq_hook(page):
    """[FN-05 · CSQ · FIX-07 · FIX-B] เผยแพร่ผลแล้วมีร่องรอย 7C ใน audit + toast (ref ภายใน CSQ_BRIEF ถอดออกจากจอ)"""
    open_(page)
    calib_publish(page, "A4", dec="ผ่าน")
    assert ev(page, "() => appr('A4').status") == "published", "ขับ calibration ไม่ถึง published"
    log = ev(page, "() => (PERF.audit['A4']||[]).map(x=>x.act).join(' | ')")
    assert "บันทึกผลประเมินเข้า 7C" in log, f"audit ไม่มีร่องรอย 'บันทึกผลประเมินเข้า 7C' หลัง publish (FIX-07): {log}"
    # FIX-B · ref ภายในต้องไม่โผล่บนจอ (audit + toast) — คง token 7C ที่มองเห็นได้
    assert "CSQ_BRIEF" not in log, f"audit ยังโชว์ ref ภายใน CSQ_BRIEF บนจอ (FIX-B): {log}"
    assert "7C" in toast_text(page), f"toast เผยแพร่ไม่พ่วง 7C ({toast_text(page)})"
    assert "CSQ_BRIEF" not in toast_text(page), f"toast ยังโชว์ ref ภายใน CSQ_BRIEF ({toast_text(page)})"
    return "CSQ hook: publish → audit 'บันทึกผลประเมินเข้า 7C' + toast พ่วง 7C · ref ภายใน CSQ_BRIEF ถอดจากจอ (คงในคอมเมนต์ HTML)"


def c_succession_hook(page):
    """[FN-07 · SUCC · FIX-09] ผลที่เผยแพร่ (ผ่าน/top) มีปุ่มส่งเข้า Succession (display-only)"""
    open_(page)
    go_tab(page, "review")
    assert "Succession" in pc_text(page), "หน้าผลไม่มีปุ่มส่งเข้า Succession (A5 ผ่าน · FIX-09)"
    assert ev(page, "() => typeof sendSuccession === 'function'"), "ไม่มีฟังก์ชัน sendSuccession"
    apprs0 = ev(page, "() => JSON.stringify(PERF.apprs)")
    after(page, "() => sendSuccession('A5')")
    assert "Succession" in toast_text(page), f"sendSuccession ไม่ขึ้น toast ({toast_text(page)})"
    assert ev(page, "() => JSON.stringify(PERF.apprs)") == apprs0, "sendSuccession mutate ข้อมูล (ควร display-only)"
    return "Succession hook: ผลเผยแพร่ (ผ่าน) มีปุ่ม Succession เคียง Movement/Training · display-only ไม่ mutate"


def c_fix10_drawer_icon(page):
    """[FIX-10] ปุ่มปิด drawer ต้องมี svg เสมอ (renderIcons หลังเติม drawer)"""
    open_(page)
    after(page, "() => openDrawer('viewAppr','A4')")
    assert_icons_rendered(page, root="#drawer")
    has_svg = ev(page, "() => { const b=document.querySelector('#drawer .drawer-header .icon-btn'); return !!(b && b.querySelector('svg')); }")
    assert has_svg, "ปุ่มปิด drawer ไม่มี svg (icon ไม่ render · FIX-10)"
    return "drawer close button มี svg (renderIcons หลังเติม drawer innerHTML · FIX-10)"


# ═══════════════════ OQ RESOLUTIONS (OQ-PERF-01 re-open · OQ-PERF-03 dept scope) ═══════════════════

def c_reopen(page):
    """[FN-05 · REOPEN · OQ-PERF-01] เปิดแก้ไขผลที่เผยแพร่แล้ว — authorized + audit ผู้แก้ · re-publishable clean

    มติ PM/BA: 'แก้ไขได้แต่ต้องเก็บ logs ว่าใครแก้.' — HR (manage) re-open published + เหตุผลบังคับ →
    status กลับ 'mgr' + audit บันทึกผู้แก้ · staff/unauthorized เรียกตรงไม่เปลี่ยน state + ไม่เห็นปุ่ม
    """
    open_(page)
    assert ev(page, "() => appr('A5').status") == "published", "A5 ควร published (เตรียมเคส)"
    n0 = ev(page, "() => (PERF.audit['A5']||[]).length")
    after(page, "() => openModal('reopen',{id:'A5'})")
    # เหตุผลว่าง → บล็อก (required reason · field is-invalid)
    after(page, "() => doReopen('A5')")
    assert ev(page, "() => appr('A5').status") == "published", "เหตุผลว่างแต่เปิดแก้ไขผ่าน (ควร required reason)"
    assert ev(page, "() => document.getElementById('reopenErr').closest('.field').classList.contains('is-invalid')"), \
        "เหตุผลว่างแต่ field ไม่ขึ้น is-invalid"
    # ใส่เหตุผล → เปิดแก้ไข → status='mgr' + เคลียร์ approvals + audit ผู้แก้ (who=HR)
    after(page, "() => { document.getElementById('reopenReason').value='คะแนนผิด ต้องแก้'; }")
    after(page, "() => doReopen('A5')")
    assert ev(page, "() => appr('A5').status") == "mgr", "เปิดแก้ไขแล้วไม่กลับขั้นหัวหน้าประเมิน (status ต้อง = 'mgr')"
    assert ev(page, "() => !appr('A5').approvals"), "เปิดแก้ไขแล้วไม่เคลียร์ผู้สอบทานเดิม (approvals) → re-calibrate ไม่ clean"
    log = ev(page, "() => PERF.audit['A5']")
    assert len(log) == n0 + 1, f"เปิดแก้ไขแล้ว audit ไม่ append 1 รายการ (n0={n0} · now={len(log)})"
    assert "เปิดแก้ไขผลหลังเผยแพร่" in log[0]["act"], f"audit ไม่บันทึกการเปิดแก้ไข (act): {log[0]}"
    assert "คะแนนผิด ต้องแก้" in log[0]["act"], f"audit ไม่บันทึกเหตุผลที่กรอก: {log[0]}"
    hr_name = ev(page, "() => PERF.roles.find(r=>r.id==='hr').name")
    assert log[0]["who"] == hr_name, f"audit ไม่บันทึก 'ใครแก้' (who ต้อง = HR name '{hr_name}'): {log[0]}"
    assert log[0].get("at"), "audit ไม่ stamp เวลา (at) ของผู้แก้"
    # re-publishable clean: mgr re-score → calibration → publish ใหม่ (CSQ 7C ยิงซ้ำ per-person)
    after(page, "() => { const a=appr('A5'); a.kpis.forEach(k=>k.mgr=5); saveMgr('A5'); }")
    assert ev(page, "() => appr('A5').status") == "calibration", "re-score หัวหน้าหลังเปิดแก้ไขแล้วไม่ส่งเข้าสอบทาน"
    calib_publish(page, "A5", dec="ผ่าน")
    assert ev(page, "() => appr('A5').status") == "published", "re-publish หลังเปิดแก้ไขไม่สำเร็จ (flow ไม่ clean)"
    assert "บันทึกผลประเมินเข้า 7C" in ev(page, "() => (PERF.audit['A5']||[]).map(x=>x.act).join(' | ')"), \
        "re-publish แล้ว CSQ 7C ไม่ยิงซ้ำ (per-person · OQ-PERF-02)"
    # staff/unauthorized → เรียก doReopen ตรง ไม่เปลี่ยน state (guard)
    open_(page)
    after(page, "() => setRole('staff')")
    st0 = ev(page, "() => appr('A5').status")
    after(page, "() => openModal('reopen',{id:'A5'})")
    after(page, "() => { const t=document.getElementById('reopenReason'); if(t) t.value='พยายามแก้'; doReopen('A5'); }")
    assert ev(page, "() => appr('A5').status") == st0 == "published", "staff เรียก doReopen แล้วสถานะเปลี่ยน (guard พลาด)"
    assert "สิทธิ์ไม่พอ" in toast_text(page), f"staff เรียก doReopen ไม่เตือนสิทธิ์ ({toast_text(page)})"
    # ปุ่ม 'เปิดแก้ไขผล' โผล่ให้ HR ในหน้าผล & Gap (authorized) — ไม่โผล่ตอนรอบปิด
    after(page, "() => setRole('hr')")
    go_tab(page, "review")
    assert "เปิดแก้ไขผล" in pc_text(page), "HR ไม่เห็นปุ่ม 'เปิดแก้ไขผล' ในหน้าผล & Gap (authorized)"
    after(page, "() => doCloseCycle('CY1')")
    go_tab(page, "review")
    assert_text_absent(page, ["เปิดแก้ไขผล"], scope="#page-content")   # รอบปิด → ปุ่ม re-open หาย (ไม่อ่อน closed lock)
    return ("re-open: HR+เหตุผล → published→mgr + audit ผู้แก้(HR)+at+เหตุผล · เคลียร์ approvals · re-publish clean (CSQ ยิงซ้ำ) · "
            "staff=block+เตือนสิทธิ์ · ปุ่มโผล่เฉพาะ authorized+รอบเปิด")


def c_mgr_dept_scope(page):
    """[FN-04 · DEPT · OQ-PERF-03] หัวหน้า (mgr) เห็นเฉพาะแผนกตัวเอง (ฝ่ายผลิต) · HR เห็นทุกแผนก · staff เห็นเฉพาะตน

    มติ PM/BA: 'เฉพาะแผนกตัวเอง.' — คนแผนกอื่น (ชื่อ/decision/gap) ต้องไม่อยู่ใน DOM (ไม่ใช่แค่ mask)
    """
    open_(page)
    assert ev(page, "() => PERF.roles.find(r=>r.id==='mgr').dept") == "ฝ่ายผลิต", "mgr role ไม่มี dept=ฝ่ายผลิต"
    # --- mgr persona: apprView เห็นเฉพาะ ฝ่ายผลิต (A2 สมชาย ใจดี) ---
    after(page, "() => setRole('mgr')")
    go_tab(page, "appr")
    pt = pc_text(page)
    assert "สมชาย ใจดี" in pt, "mgr (ฝ่ายผลิต) ควรเห็นแบบประเมินแผนกตัวเอง (สมชาย ใจดี)"
    assert_text_absent(page, ["มะลิ ดอกไม้", "อรทัย แสนสุข", "ธนากร พูนผล", "กนกพร วงศ์ไทย",
                              "ปิยะ มั่นคง", "ทักษะการนำเสนอ", "ความถูกต้องในงาน", "ทบทวน"],
                       scope="#page-content")
    # --- mgr persona: reviewView (team-calib + queue + ผล&Gap) ก็ dept-scoped → ไม่มีคนแผนกอื่น ---
    go_tab(page, "review")
    assert_text_absent(page, ["ธนากร พูนผล", "กนกพร วงศ์ไทย", "ปิยะ มั่นคง", "อรทัย แสนสุข",
                              "มะลิ ดอกไม้", "ทักษะการนำเสนอ", "ความถูกต้องในงาน"],
                       scope="#page-content")
    # --- mgr เปิดแบบประเมินนอกแผนก (A6 ปิยะ · คลังสินค้า) → detail guard block (ชื่อ/gap ไม่หลุด) ---
    after(page, "() => { state.view.tab='detail'; openDrawer('viewAppr','A6'); }")
    assert "RESTRICTED" in drawer_text(page), "mgr เปิดแบบประเมินนอกแผนกแล้ว detail ไม่ถูก guard (RESTRICTED)"
    assert_text_absent(page, ["ความถูกต้องในงาน"], scope="#drawer")   # gap ของ A6 ไม่หลุดใน detail
    after(page, "() => closeDrawer()")
    # --- HR persona: เห็นทุกแผนก (ALL) ---
    after(page, "() => setRole('hr')")
    go_tab(page, "appr")
    ph = pc_text(page)
    for nm in ("มะลิ ดอกไม้", "สมชาย ใจดี", "อรทัย แสนสุข", "ธนากร พูนผล", "กนกพร วงศ์ไทย", "ปิยะ มั่นคง"):
        assert nm in ph, f"HR ควรเห็นทุกแผนก แต่ไม่พบ {nm} (scope ALL พลาด)"
    # --- staff persona: ยังเห็นเฉพาะของตน (SELF · unchanged) ---
    after(page, "() => setRole('staff')")
    go_tab(page, "appr")
    st = pc_text(page)
    assert "สมชาย ใจดี" in st, "staff ควรเห็นของตน (สมชาย ใจดี)"
    assert_text_absent(page, ["มะลิ ดอกไม้", "อรทัย แสนสุข", "ธนากร พูนผล"], scope="#page-content")
    return ("dept scope: mgr(ฝ่ายผลิต) เห็นเฉพาะ สมชาย · คนแผนกอื่นไม่อยู่ใน DOM (appr+review) · detail นอกแผนก=RESTRICTED · "
            "HR=ALL (6 คน) · staff=SELF (unchanged)")


# ═══════════════════════════════ RUN ═══════════════════════════════

CASES = [
    ("E01", c_fn01), ("E02", c_fn11), ("E03", c_fn02), ("E04", c_fn03),
    ("E05", c_fn04), ("E06", c_fn09), ("E07", c_fn05), ("E08", c_fn08),
    ("E09", c_fn06), ("E10", c_fn07), ("E11", c_fn10), ("E12", c_fn12),
    ("E13", c_fn13), ("E14", c_fn90), ("E15", c_fn91), ("E16", c_fn92),
    ("E17", c_fn93), ("E18", c_fn94),
    ("NEG", c_unsupported),
    ("DSP-01", c_dsp01), ("DSP-02a", c_dsp02a), ("DSP-02b", c_dsp02b),
    ("REG", c_regression),
    ("B3", c_bug3_mgr_edit), ("B1", c_bug1_footer), ("B2", c_bug2_filtergap),
    # BA-gate re-gate · bypass/governance (FIX-01..10)
    ("P1", c_p1_published_immutable), ("P2", c_p2_calib_precondition),
    ("P3", c_p3_role_guard), ("P4", c_p4_closed_lock),
    ("SLOT", c_slot_staged), ("CSQ", c_csq_hook),
    ("SUCC", c_succession_hook), ("FIX10", c_fix10_drawer_icon),
    # OQ resolutions
    ("REOPEN", c_reopen), ("DEPT", c_mgr_dept_scope),
]

REQUIRED_FN = ["FN-01", "FN-02", "FN-03", "FN-04", "FN-05", "FN-06", "FN-07",
               "FN-08", "FN-09", "FN-10", "FN-11", "FN-12", "FN-13",
               "FN-90", "FN-91", "FN-92", "FN-93", "FN-94"]


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        suite.watch(page)
        for tid, fn in CASES:
            name = (fn.__doc__ or fn.__name__).strip().splitlines()[0]
            suite.check(tid, name, lambda fn=fn: fn(page))
        browser.close()

    # ── FN coverage divisor line (C3.5) ──
    covered = set()
    for _tid, name, _st, _detail in suite.results:
        for m in re.findall(r"FN-\d+", name):
            covered.add(m)
    covered_req = [f for f in REQUIRED_FN if f in covered]
    missing = [f for f in REQUIRED_FN if f not in covered]
    total = len(suite.results)
    passed = sum(1 for r in suite.results if r[2] == "PASS")
    print()
    print(f"FN ครอบ {len(covered_req)}/{len(REQUIRED_FN)} · เคสรวม {total} · ผ่าน {passed}/{total}")
    if missing:
        print("  FN ที่ยังไม่ถูกครอบ:", ", ".join(missing))
    print()
    suite.report(exit_on_fail=True)


if __name__ == "__main__":
    main()
