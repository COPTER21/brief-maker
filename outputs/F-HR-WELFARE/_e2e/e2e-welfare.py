"""E2E · F-HR-WELFARE (สวัสดิการ / Welfare) — WF-01 Step 5

รันไทม์ตัวเดียวที่ครอบทุก FN (24 = FN-01..19 + FN-90..94) + เคสเชิงลบ 5 ข้อ
(unsupported[]) ที่เรนเดอร์จริงแล้ว assert ว่า "ไม่มี" affordance บนจอ.

ยึด helper ของ uikit เท่านั้น (ready/settle/after) — ไม่มี wait_for_timeout, ไม่มีตัวตรวจ UI ใหม่.
ขับหน้าจอผ่าน controller function จริงของไฟล์ แล้ว assert ทั้ง data model และข้อความที่เรนเดอร์บน DOM.
reload หน้าใหม่ต่อเคส → mock data reset = เคสอิสระต่อกัน.

รัน: .claude/venv/Scripts/python.exe outputs/F-HR-WELFARE/_e2e/e2e-welfare.py [path/to/welfare.html]
"""
from pathlib import Path
import re
import sys

from playwright.sync_api import sync_playwright

OUTPUTS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(OUTPUTS / "_SHARED" / "_e2e"))
from uikit import (  # noqa: E402
    Suite, ready, settle as shared_settle, after as shared_after,
    unrendered_visible_icons, assert_no_garbage_text,
    assert_combobox_closes_after_select, combobox_state_after_select,
    modal_autoopens_comboboxes, assert_no_person_cell_collision,
    JS_MODAL_UNDER_DRAWER, JS_AFFORDANCE, JS_CSSVAR, JS_OVERLAY_STACK,
)

HTML = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parents[1] / "welfare.html").resolve()
BASE = HTML.as_uri()

suite = Suite("F-HR-WELFARE สวัสดิการ")


def settle(page, timeout=1400):
    shared_settle(page, timeout=timeout)


def after(page, js, timeout=1600):
    return shared_after(page, js, timeout=timeout)


def open_(page):
    """เปิดหน้าใหม่ (reset mock data) แล้วรอ render จริง"""
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


def go_tab(page, t):
    after(page, "() => goTab('%s')" % t)


# ═══════════════════════════════ FN CASES ═══════════════════════════════

def c_fn01(page):
    """[FN-01 · S-01 · BR-03] สร้างประเภทสวัสดิการ (กลุ่ม + โควตา/วงเงิน + วันมีผล)"""
    open_(page)
    after(page, "() => openDrawer('benefit-create')")
    dt = drawer_text(page)
    assert "วันมีผล" in dt, "ฟอร์มสร้างไม่มีช่องวันมีผล (effective_date)"
    assert "กลุ่มพนักงานที่มีสิทธิ์" in dt, "ฟอร์มสร้างไม่มีการเลือกกลุ่มพนักงาน"
    grpChk = ev(page, "() => document.querySelectorAll('#drawer .cb').length")
    assert grpChk >= 3, f"ไม่มี checkbox กลุ่มครบ (ได้ {grpChk})"
    after(page, """() => { Object.assign(state.form, {name:'ประกันอุบัติเหตุ (QA)', cat:'สุขภาพ',
      unit:'money', quota:15000, coversDep:true, groups:['g-full'], effFrom:'2027-06-01', err:{}}); }""")
    assert ev(page, "() => validateBenefit()") is True, "ฟอร์มถูกต้องแต่ validateBenefit=false"
    after(page, "() => submitBenefit()")
    toast = ev(page, "() => document.getElementById('toast').textContent")
    assert "สร้างประเภทสวัสดิการสำเร็จ" in toast, f"ไม่ขึ้น toast สำเร็จ (ได้ '{toast}')"
    assert ev(page, "() => state.drawer.open") is False, "สร้างแล้วลิ้นชักไม่ปิด"
    return "สร้างประเภทสวัสดิการ: กลุ่ม+โควตา15,000+วันมีผล · validate ผ่าน · toast สำเร็จ"


NAME_SEL = "#drawer input[placeholder='เช่น ประกันสุขภาพกลุ่ม']"


def c_fn01b(page):
    """[FN-01/FN-02] benefit draft lifecycle: บันทึกร่าง=in-place draft · บันทึก(primary)=publish→active

    regression F-HR-WELFARE: แก้ร่างแล้วกด 'บันทึกร่าง' ต้อง 'อัปเดตในที่' (ไม่สร้างแถวซ้ำ · ยังเป็นร่าง)
    ส่วน submit primary (#btn-submit) = เผยแพร่ ร่าง→มีผล ในที่. เดินจอจริง (fill/click) ไม่ set state.form ตรง.
    หมายเหตุ: primary ('บันทึกการแก้ไข') มีคำ 'บันทึก' ซ้อนกับ 'บันทึกร่าง' → จับ primary ด้วย #btn-submit เท่านั้น.
    """
    open_(page)
    n0 = ev(page, "() => BENEFITS.length")
    assert ev(page, "() => BENEFITS.filter(b=>b.status==='draft').length") == 0, "seed ไม่ควรมีร่างค้าง"

    # (1) สร้างร่าง — เดินจอจริง: กรอกชื่อ + โควตา (input[type=number]) + ติ๊กกลุ่ม (.cb) → คลิก 'บันทึกร่าง'
    after(page, "() => { state.form={}; openDrawer('benefit-create'); }")
    settle(page)
    page.fill(NAME_SEL, "ทดสอบร่าง (QA)")
    page.fill("#drawer input[type=number]", "8000")
    page.locator("#drawer .cb").first.click()   # ติ๊กกลุ่มแรก (toggleGrp → render)
    assert ev(page, "() => (state.form.groups||[]).length") >= 1, "ติ๊กกลุ่มแล้วแต่ state.form.groups ว่าง"
    page.get_by_role("button", name="บันทึกร่าง", exact=True).click()
    page.wait_for_function("() => state.drawer.open===false", timeout=4000)
    drafts = ev(page, "() => BENEFITS.filter(b=>b.status==='draft')")
    assert len(drafts) == 1, f"สร้างร่างแล้วจำนวนร่างควร=1 (ได้ {len(drafts)})"
    did = drafts[0]["id"]
    assert ev(page, "() => BENEFITS.length") == n0 + 1, "สร้างร่างแล้ว BENEFITS ไม่เพิ่ม 1"
    assert drafts[0]["name"] == "ทดสอบร่าง (QA)", f"ชื่อร่างไม่ตรง: {drafts[0]['name']}"
    assert drafts[0]["quota"] == 8000, f"โควตาร่างไม่ตรง: {drafts[0]['quota']}"
    n1 = ev(page, "() => BENEFITS.length")

    # (2) แก้ร่าง → 'บันทึกร่าง' (secondary) = อัปเดตในที่ · ยังร่าง · ไม่สร้างแถวซ้ำ
    after(page, "() => { state.form={}; openDrawer('benefit-edit','%s'); }" % did)
    settle(page)
    page.fill(NAME_SEL, "ทดสอบร่าง แก้ครั้งที่ 1 (QA)")
    page.get_by_role("button", name="บันทึกร่าง", exact=True).click()
    page.wait_for_function("() => state.drawer.open===false", timeout=4000)
    assert ev(page, "() => BENEFITS.length") == n1, "แก้ร่างแล้วบันทึกร่าง = แถวเพิ่ม (สร้างร่างซ้ำ)"
    assert ev(page, "() => BENEFITS.filter(b=>b.status==='draft').length") == 1, "จำนวนร่างเปลี่ยน (ควรคง 1)"
    r2 = ev(page, "() => benById('%s')" % did)
    assert r2 and r2["status"] == "draft", f"บันทึกร่างไม่คงสถานะร่าง: {r2 and r2['status']}"
    assert r2["name"] == "ทดสอบร่าง แก้ครั้งที่ 1 (QA)", f"บันทึกร่างไม่อัปเดตชื่อในที่: {r2['name']}"

    # (3) แก้ร่าง → submit primary (#btn-submit) = เผยแพร่ ร่าง→active ในที่
    after(page, "() => { state.form={}; openDrawer('benefit-edit','%s'); }" % did)
    settle(page)
    page.fill(NAME_SEL, "ทดสอบร่าง เผยแพร่ (QA)")
    page.locator("#btn-submit").click()
    page.wait_for_function("() => { const b=benById('%s'); return b && b.status==='active'; }" % did, timeout=5000)
    assert ev(page, "() => BENEFITS.length") == n1, "เผยแพร่ร่างแล้วแถวเพิ่ม (ควรเผยแพร่ในที่)"
    assert ev(page, "() => BENEFITS.filter(b=>b.status==='draft').length") == 0, "เผยแพร่แล้วยังเหลือร่าง (draft ควร=0)"
    r3 = ev(page, "() => benById('%s')" % did)
    assert r3["name"] == "ทดสอบร่าง เผยแพร่ (QA)", f"เผยแพร่ไม่สะท้อนการแก้: {r3['name']}"
    return "draft lifecycle: บันทึกร่าง=in-place ร่าง (ไม่ซ้ำแถว·คง 1) · submit primary=เผยแพร่ ร่าง→active ในที่"


def c_fn02(page):
    """[FN-02 · S-02 · BR-03] แก้ประเภท = ออกเวอร์ชันใหม่ · เวอร์ชันเก่ายังอ้างอิงได้"""
    open_(page)
    after(page, "() => openDrawer('benefit-edit','B-HEALTH')")
    dt = drawer_text(page)
    assert "ออกเวอร์ชันใหม่" in dt, "แก้ไขไม่แจ้งว่าเป็นการออกเวอร์ชันใหม่ (FN-02)"
    # เวอร์ชันเก่า (archived) ยังอ่านได้ในมุมมองเวอร์ชัน
    after(page, "() => openDrawer('benefit-view','B-HEALTH')")
    vrows = ev(page, "() => BENEFITS.filter(b=>b.code==='WEL-HEALTH').length")
    assert vrows == 2, f"WEL-HEALTH ควรมี 2 เวอร์ชัน (active v2 + archived v1) ได้ {vrows}"
    dv = drawer_text(page)
    assert "เวอร์ชัน 2" in dv and "เวอร์ชัน 1" in dv, "มุมมองเวอร์ชันไม่แสดงทั้งเก่าและใหม่"
    assert "เก็บถาวร" in dv, "เวอร์ชันเก่าไม่ถูกทำเครื่องหมายเก็บถาวร (ยังอ้างอิงได้)"
    # submit แก้ → toast ออกเวอร์ชันใหม่
    after(page, "() => openDrawer('benefit-edit','B-HEALTH')")
    after(page, "() => submitBenefit()")
    toast = ev(page, "() => document.getElementById('toast').textContent")
    assert "ออกเวอร์ชันใหม่" in toast, f"แก้แล้วไม่ขึ้น toast ออกเวอร์ชันใหม่ (ได้ '{toast}')"
    return "แก้ไข=ออกเวอร์ชันใหม่ · WEL-HEALTH 2 เวอร์ชัน (v2 active + v1 archived อ่านได้)"


def c_fn03(page):
    """[FN-03 · S-03 · BR-07] ปิดใช้ (soft archive) — คำขอเก่าอ่านได้ ไม่มี hard delete"""
    open_(page)
    n0 = ev(page, "() => BENEFITS.length")
    after(page, "() => openModal('archiveBenefit','B-EDU')")
    mt = modal_text(page)
    assert "soft archive" in mt or "เก็บถาวร" in mt, "confirm ปิดใช้ไม่ระบุ soft archive/เก็บถาวร"
    assert "คำขอเก่ายังอ่านได้" in mt, "ไม่ยืนยันว่าคำขอเก่ายังอ่านได้"
    after(page, "() => doArchiveBenefit('B-EDU')")
    assert ev(page, "() => benById('B-EDU').status") == "archived", "ไม่ได้เปลี่ยนเป็น archived"
    assert ev(page, "() => BENEFITS.length") == n0, "soft archive แต่ record หาย (hard delete)"
    assert ev(page, "() => !!benById('B-EDU')") is True, "record B-EDU หายไป"
    # ยังเปิดดูได้ (อ่านได้)
    after(page, "() => openDrawer('benefit-view','B-EDU')")
    assert "ค่าเล่าเรียนบุตร" in drawer_text(page), "archive แล้วเปิดดูไม่ได้"
    return "ปิดใช้ soft archive: status→archived · record คงอยู่ · ยังอ่านได้ · ไม่ hard delete"


def c_fn04(page):
    """[FN-04 · S-04 · BR-03] บล็อกโควตา≤0 · บล็อกช่วงมีผลทับกัน"""
    open_(page)
    # (ก) โควตา ≤ 0 → บล็อก
    after(page, "() => openDrawer('benefit-create')")
    after(page, """() => { Object.assign(state.form,{name:'ทดสอบ', unit:'money', quota:0,
      groups:['g-full'], effFrom:'2027-06-01', err:{}}); }""")
    assert ev(page, "() => validateBenefit()") is False, "โควตา 0 แต่ผ่าน validate"
    assert "0" in ev(page, "() => (state.form.err.quota||'')") or "มากกว่า 0" in ev(page, "() => (state.form.err.quota||'')"), \
        "ไม่มี error โควตาต้องมากกว่า 0"
    # (ข) แก้เวอร์ชันด้วยวันมีผลทับเวอร์ชัน active เดิม → บล็อก BR-03
    after(page, "() => openDrawer('benefit-edit','B-HEALTH')")   # active effFrom 2026-01-01
    after(page, "() => { state.form.effFrom='2026-01-01'; }")
    assert ev(page, "() => validateBenefit()") is False, "วันมีผลทับกันแต่ผ่าน validate"
    e = ev(page, "() => (state.form.err.effFrom||'')")
    assert "ช่วงมีผลทับกันไม่ได้" in e, f"error ช่วงมีผลทับกันไม่ตรง: '{e}'"
    return "บล็อกโควตา≤0 (err.quota) · บล็อกช่วงมีผลทับ (BR-03)"


def c_fn05(page):
    """[FN-05 · S-05 · BR-10] เพิ่มผู้ติดตาม (ความสัมพันธ์ · วันเกิด · สถานะใช้สิทธิ์)"""
    open_(page)
    n0 = ev(page, "() => empById('EMP-002').dependents.length")
    after(page, "() => openDrawer('dependent-create','EMP-002')")
    after(page, "() => { Object.assign(state.form,{name:'สมหญิง วงศ์ทอง', rel:'คู่สมรส', dob:'1992-05-05', eligible:true, err:{}}); }")
    after(page, "() => submitDependent()")
    n1 = ev(page, "() => empById('EMP-002').dependents.length")
    assert n1 == n0 + 1, "ไม่ได้เพิ่มผู้ติดตาม"
    last = ev(page, "() => empById('EMP-002').dependents[empById('EMP-002').dependents.length-1]")
    assert last["name"] == "สมหญิง วงศ์ทอง" and last["rel"] == "คู่สมรส" and last["eligible"] is True, \
        "ข้อมูลผู้ติดตามที่เพิ่มไม่ตรง"
    return f"เพิ่มผู้ติดตาม: คู่สมรส · dob · ใช้สิทธิ์ได้ ({n0}→{n1})"


def c_fn06(page):
    """[FN-06 · S-06 · BR-01] บุตรอายุเกินเกณฑ์ → บล็อก · ผู้ติดตามเกินจำนวน → เตือน"""
    open_(page)
    # (ก) บุตรอายุ > 20 → บล็อก
    after(page, "() => openDrawer('dependent-create','EMP-002')")
    after(page, "() => { Object.assign(state.form,{name:'บุตรโต', rel:'บุตร', dob:'2000-01-01', eligible:true, err:{}}); }")
    after(page, "() => submitDependent()")
    assert ev(page, "() => empById('EMP-002').dependents.length") == 0, "บุตรอายุเกินแต่ยังเพิ่มได้"
    assert "อายุเกิน 20" in ev(page, "() => (state.form.err.dob||'')"), "ไม่บล็อกบุตรอายุเกิน 20 ปี"
    # (ข) เกินจำนวน (≥3) → เตือน · เพิ่มให้ EMP-001 (มี 2) ครบ 3 ก่อน
    after(page, "() => { state.form={}; }")
    after(page, "() => openDrawer('dependent-create','EMP-001')")
    after(page, "() => { Object.assign(state.form,{name:'บิดา ใจดี', rel:'บิดา', dob:'1955-01-01', eligible:true, err:{}}); }")
    after(page, "() => submitDependent()")
    assert ev(page, "() => empById('EMP-001').dependents.length") == 3, "เพิ่มผู้ติดตามคนที่ 3 ไม่สำเร็จ"
    after(page, "() => openDrawer('dependent-create','EMP-001')")
    assert "ครบ 3 คนแล้ว" in drawer_text(page), "ผู้ติดตามครบ/เกินเกณฑ์แต่ไม่เตือน"
    return "บุตรอายุ>20 บล็อก (err.dob) · ผู้ติดตามครบ 3 → เตือนเกินเกณฑ์กลุ่ม"


def c_fn07(page):
    """[FN-07 · S-07 · BR-01] สร้างคำขอ: เลือกประเภทมีสิทธิ์ + ผู้ใช้สิทธิ์(ตัวเอง/ผู้ติดตาม) + แนบหลักฐาน"""
    open_(page)
    # eligibility ทำงาน: EMP-001(g-full) มีสิทธิ์ B-EDU · EMP-003(g-prob) ไม่มีสิทธิ์ B-EDU
    assert ev(page, "() => eligibility(empById('EMP-001'),benById('B-EDU'),'2026-06-01').ok") is True, \
        "EMP-001 ควรมีสิทธิ์ B-EDU"
    assert ev(page, "() => eligibility(empById('EMP-003'),benById('B-EDU'),'2026-06-01').ok") is False, \
        "EMP-003 (นอกกลุ่ม) ไม่ควรมีสิทธิ์ B-EDU"
    after(page, "() => openDrawer('request-create')")
    after(page, "() => { state.form.empId='EMP-001'; render(); }")
    # combobox ประเภทติดป้ายมีสิทธิ์/ไม่มีสิทธิ์ (เลือกเฉพาะที่มีสิทธิ์)
    subEdu = ev(page, "() => { const o=window.__ss['reqType'].options.find(x=>x.value==='B-EDU'); return o?o.sub:''; }")
    assert "มีสิทธิ์" in subEdu, f"ตัวเลือกประเภทไม่ติดสถานะสิทธิ์: '{subEdu}'"
    # เลือกประเภท + ผู้ใช้สิทธิ์ = ผู้ติดตาม (B-EDU coversDep) + แนบไฟล์
    after(page, "() => { state.form.benefitId='B-EDU'; render(); }")
    after(page, "() => { state.form.useForType='dependent'; state.form.depId='DEP-2'; render(); }")
    after(page, "() => mockUpload()")
    assert ev(page, "() => state.form.files.length") >= 1, "แนบหลักฐานไม่ได้"
    assert ev(page, "() => { const o=window.__ss['reqType'].options.length; return o; }") > 0, "ไม่มีตัวเลือกประเภท"
    return "คำขอ: เลือกประเภทมีสิทธิ์ (ป้ายสถานะ) + ผู้ใช้สิทธิ์ผู้ติดตาม + แนบไฟล์"


def c_fn08(page):
    """[FN-08 · S-07 · BR-04] DOA slot picker เลือก 'คน' (avatar+ตำแหน่ง+ชื่อ) — ไม่ hardcode สายอนุมัติ"""
    open_(page)
    after(page, "() => openModal('doa','REQ-2569-0026')")   # REQ draft
    assert ev(page, "() => state.modal.type==='doa'"), "ไม่เปิด DOA modal"
    # ยังไม่เลือก = ไม่ hardcode
    assert ev(page, "() => Object.keys(state.doaDraft.picks||{}).length===0"), "slot ถูก preset (hardcode)"
    # option = คนจริง (avatar #102 + ชื่อ + ตำแหน่ง/แผนก) — FIX-08: person combobox ใช้ avatar แทน icon
    optok = ev(page, """() => { const s=window.__ss['doaSlot1'];
      return s && s.options.length>=3 && s.options.every(o=>o.label && o.sub && o.avatar); }""")
    assert optok, "slot picker ไม่ใช่รายชื่อคนจริง (ขาดชื่อ/ตำแหน่ง/avatar)"
    assert ev(page, "() => !!document.getElementById('ss-doaSlot1') && !!document.getElementById('ss-doaSlot2')"), \
        "ไม่มีช่องเลือกผู้อนุมัติ 2 ขั้น"
    # ส่งทั้งที่ยังไม่เลือก → บล็อก (ไม่เข้า pending)
    after(page, "() => confirmDoa('REQ-2569-0026')")
    assert ev(page, "() => reqById('REQ-2569-0026').status") == "draft", "ส่ง DOA ได้ทั้งที่ยังไม่เลือกผู้อนุมัติ"
    # เลือกคนผ่าน picker จริง แล้วส่ง
    after(page, "() => ssPick('doaSlot1',0)")   # AP-1 วิชัย ประเสริฐ
    after(page, "() => ssPick('doaSlot2',0)")   # AP-4 พรทิพย์ สุขใจ
    after(page, "() => confirmDoa('REQ-2569-0026')")
    ap = ev(page, "() => reqById('REQ-2569-0026').approvals")
    assert ev(page, "() => reqById('REQ-2569-0026').status") == "pending", "เลือกครบแล้วไม่ส่งเข้า pending"
    assert ap[0]["person"]["name"] == "วิชัย ประเสริฐ" and ap[1]["person"]["name"] == "พรทิพย์ สุขใจ", \
        f"ผู้อนุมัติที่บันทึกไม่ตรงกับที่เลือก (hardcode?): {ap}"
    return "DOA picker 2 ขั้น เลือกคนเอง · ว่าง=บล็อก · ผูกตามที่เลือก (ไม่ hardcode)"


def c_fn09(page):
    """[FN-09 · S-08 · BR-02] ใช้สิทธิ์บางส่วน → คงเหลือถูกต้อง และใช้ต่อได้"""
    open_(page)
    # EMP-001 · B-HEALTH quota 30,000 · approved เดิม 12,000 → คงเหลือ 18,000
    assert ev(page, "() => usedByPerson('EMP-001','B-HEALTH')") == 12000, "ยอดใช้สะสมเริ่มต้นไม่ใช่ 12,000"
    assert ev(page, "() => remaining('EMP-001','B-HEALTH')") == 18000, "คงเหลือเริ่มต้นไม่ใช่ 18,000"
    # ยื่น+อนุมัติเพิ่ม 5,000 → คงเหลือ 13,000 (ใช้ต่อรอบถัดไปได้)
    after(page, "() => openDrawer('request-create')")
    after(page, "() => { Object.assign(state.form,{empId:'EMP-001', useForType:'self', depId:null, benefitId:'B-HEALTH', amount:5000, value:5000, useDate:'2026-06-01', reason:'ค่ารักษา', files:[], err:{}}); }")
    after(page, "() => submitRequestForm()")
    rid = ev(page, "() => REQUESTS[0].id")
    after(page, f"() => {{ ssPick('doaSlot1',0); }}")
    after(page, f"() => {{ ssPick('doaSlot2',0); }}")
    after(page, f"() => confirmDoa('{rid}')")
    after(page, f"() => doApprove('{rid}')")   # ขั้น 1 (FIX-03 advance ทีละขั้น — สาย DOA 2 ขั้น)
    after(page, f"() => doApprove('{rid}')")   # ขั้น 2 (ขั้นสุดท้าย → finalize + ตัดคงเหลือ)
    assert ev(page, f"() => reqById('{rid}').status") == "approved", "อนุมัติคำขอใหม่ (2 ขั้น) ไม่สำเร็จ"
    assert ev(page, "() => remaining('EMP-001','B-HEALTH')") == 13000, \
        f"คงเหลือหลังใช้บางส่วนไม่ถูก: {ev(page, '() => remaining(\"EMP-001\",\"B-HEALTH\")')}"
    return "ใช้บางส่วน: 30,000 − 12,000 = 18,000 · +อนุมัติ 5,000 → คงเหลือ 13,000"


def c_fn10(page):
    """[FN-10 · S-09 · BR-02] ขอเกินคงเหลือ → บล็อก + แสดงยอดคงเหลือ"""
    open_(page)
    n0 = ev(page, "() => REQUESTS.length")
    after(page, "() => openDrawer('request-create')")
    # EMP-001 B-HEALTH คงเหลือ 18,000 · ขอ 25,000 → เกิน
    after(page, "() => { Object.assign(state.form,{empId:'EMP-001', useForType:'self', depId:null, benefitId:'B-HEALTH', amount:25000, value:25000, useDate:'2026-06-01', reason:'', files:[], err:{}}); reqRecalc(); }")
    calc = ev(page, "() => (document.getElementById('req-calc')||{}).textContent || ''")
    assert "เกินคงเหลือ" in calc, "ขอเกินแต่ไม่เตือนเกินคงเหลือ"
    assert "18,000" in calc, "ไม่แสดงยอดคงเหลือในคำเตือน"
    assert ev(page, "() => validateRequest().ok") is False, "ขอเกินแต่ validate ผ่าน"
    after(page, "() => submitRequestForm()")
    assert ev(page, "() => REQUESTS.length") == n0, "ขอเกินคงเหลือแต่ยังสร้างคำขอได้"
    return "ขอ 25,000 > คงเหลือ 18,000 → บล็อก + แสดงคงเหลือ · ไม่สร้างคำขอ"


def c_fn11(page):
    """[FN-11 · S-10 · BR-01/BR-06] ยื่นประเภทไม่มีสิทธิ์ (นอกกลุ่ม/พ้นสภาพ/นอกช่วงมีผล) → บล็อก + เหตุ"""
    open_(page)
    r_group = ev(page, "() => eligibility(empById('EMP-003'),benById('B-EDU'),'2026-06-01')")
    assert r_group["ok"] is False and "ไม่มีสิทธิ์" in r_group["reason"], "นอกกลุ่มไม่บล็อก"
    r_left = ev(page, "() => eligibility(empById('EMP-004'),benById('B-HEALTH'),'2026-10-01')")
    assert r_left["ok"] is False and "พ้นสภาพ" in r_left["reason"], "พ้นสภาพไม่บล็อก"
    r_win = ev(page, "() => eligibility(empById('EMP-001'),benById('B-HEALTH1'),'2026-06-01')")
    assert r_win["ok"] is False, "เวอร์ชันเก่า (นอกช่วงมีผล/ไม่ active) ไม่บล็อก"
    # เรนเดอร์จริงในฟอร์ม → note 'ยื่นไม่ได้' (FN-11)
    after(page, "() => openDrawer('request-create')")
    after(page, "() => { Object.assign(state.form,{empId:'EMP-003', useForType:'self', depId:null, benefitId:'B-EDU', amount:1000, value:1000, useDate:'2026-06-01', files:[], err:{}}); reqRecalc(); }")
    calc = ev(page, "() => (document.getElementById('req-calc')||{}).textContent || ''")
    assert "ยื่นไม่ได้" in calc, "ฟอร์มไม่แสดงเหตุยื่นไม่ได้"
    return "บล็อก: นอกกลุ่ม · พ้นสภาพ · นอกเวอร์ชันมีผล — พร้อมเหตุ (FN-11)"


def c_fn12(page):
    """[FN-12 · S-07] ดูสถานะคำขอ + สาย DOA ปัจจุบัน (ใครอนุมัติถึงชั้นไหน)"""
    open_(page)
    after(page, "() => openDrawer('request-view','REQ-2569-0023')")   # pending: step1 approved, step2 current
    dt = drawer_text(page)
    assert "สายอนุมัติ" in dt, "มุมมองอ่านไม่มีสาย DOA"
    assert "อนุมัติแล้ว" in dt and "กำลังพิจารณา" in dt, "ไม่แสดงสถานะรายขั้น (ถึงชั้นไหน)"
    assert "หัวหน้าสายงาน" in dt and "HR สวัสดิการ" in dt, "ไม่แสดง role รายขั้น"
    return "มุมมองอ่าน: สาย DOA + สถานะรายขั้น (approved/current)"


def c_fn13(page):
    """[FN-13 · S-07 · BR-05/BR-09] อนุมัติ → ตัดคงเหลือ + บันทึกมูลค่า 7C EC (CSQ) + payment hook"""
    open_(page)
    assert ev(page, "() => usedByPerson('EMP-003','B-CHECKUP')") == 0, "ยอดใช้ก่อนอนุมัติไม่ใช่ 0"
    after(page, "() => openModal('approve','REQ-2569-0023')")
    mt = modal_text(page)
    assert "ตัดคงเหลือ" in mt and "7C" in mt and "ส่งสถานะจ่าย" in mt, "modal อนุมัติไม่ครบ (ตัดคงเหลือ/7C/ส่งจ่าย)"
    after(page, "() => doApprove('REQ-2569-0023')")
    assert ev(page, "() => reqById('REQ-2569-0023').status") == "approved", "อนุมัติแล้วสถานะไม่ approved"
    assert ev(page, "() => usedByPerson('EMP-003','B-CHECKUP')") == 1, "อนุมัติแล้วไม่ตัดคงเหลือ (used ยัง 0)"
    assert ev(page, "() => reqById('REQ-2569-0023').pay") == "pending", "ไม่ส่งสถานะจ่ายให้ปลายทาง (payment hook)"
    after(page, "() => openDrawer('request-view','REQ-2569-0023')")
    dt = drawer_text(page)
    assert "บันทึกมูลค่าเข้า 7C · EC" in dt, "มุมมองอนุมัติไม่แสดง 7C EC"
    assert "display-only" in dt, "ไม่แสดง payment hook display-only"
    return "อนุมัติ → ตัดคงเหลือ (0→1) · CSQ 7C·EC · payment hook display-only"


def c_fn14(page):
    """[FN-14 · S-11 · BR-05] ไม่อนุมัติ → ไม่ตัดคงเหลือ + บันทึกเหตุ + แจ้งเตือน"""
    open_(page)
    after(page, "() => openModal('reject','REQ-2569-0023')")
    # เหตุว่าง → บล็อก
    after(page, "() => doReject('REQ-2569-0023')")
    assert ev(page, "() => reqById('REQ-2569-0023').status") == "pending", "เหตุว่างแต่ไม่อนุมัติผ่าน"
    # ใส่เหตุ → reject
    after(page, "() => { document.getElementById('rejectReason').value='หลักฐานไม่ครบ'; }")
    after(page, "() => doReject('REQ-2569-0023')")
    assert ev(page, "() => reqById('REQ-2569-0023').status") == "rejected", "ใส่เหตุแล้วไม่ reject"
    assert ev(page, "() => reqById('REQ-2569-0023').rejectReason") == "หลักฐานไม่ครบ", "ไม่บันทึกเหตุ"
    assert ev(page, "() => usedByPerson('EMP-003','B-CHECKUP')") == 0, "ไม่อนุมัติแต่ตัดคงเหลือ"
    toast = ev(page, "() => document.getElementById('toast').textContent")
    assert "แจ้งเตือนผู้ยื่น" in toast, "ไม่แจ้งเตือนผู้ยื่น"
    return "ไม่อนุมัติ: เหตุว่าง=บล็อก · มีเหตุ→rejected + เก็บเหตุ + ไม่ตัดคงเหลือ + แจ้งเตือน"


def c_fn15(page):
    """[FN-15 · S-12 · BR-05] ยกเลิกคำขอก่อนอนุมัติ ไม่กระทบคงเหลือ"""
    open_(page)
    after(page, "() => openModal('cancel','REQ-2569-0026')")   # draft
    mt = modal_text(page)
    assert "ไม่กระทบคงเหลือ" in mt, "confirm ยกเลิกไม่ระบุไม่กระทบคงเหลือ"
    after(page, "() => doCancelRequest('REQ-2569-0026')")
    assert ev(page, "() => reqById('REQ-2569-0026').status") == "cancelled", "ไม่ได้ยกเลิก"
    assert ev(page, "() => !!reqById('REQ-2569-0026')") is True, "ยกเลิกแล้ว record หาย"
    return "ยกเลิกคำขอ (draft) → cancelled · record คงอยู่ · ไม่กระทบคงเหลือ"


def c_fn16(page):
    """[FN-16 · S-13 · BR-06] พ้นสภาพ → คำขอค้างถูกระงับ + คงเหลือหยุด (revoked)"""
    open_(page)
    assert ev(page, "() => reqById('REQ-2569-0024').status") == "revoked", "คำขอค้างของ leaver ไม่ถูกระงับ"
    assert ev(page, "() => empById('EMP-004').ended") is True, "EMP-004 ควร ended=true (ไม่ใช่ null)"
    # balance tab ของ leaver → สิทธิ์สิ้นสุด/คงเหลือหยุด
    go_tab(page, "balance")
    after(page, "() => { state.balance.empId='EMP-004'; render(); }")
    pt = pc_text(page)
    assert "พ้นสภาพ" in pt and "สิทธิ์สวัสดิการสิ้นสุด" in pt, "balance ของ leaver ไม่แสดงสิทธิ์สิ้นสุด"
    assert "คงเหลือหยุด" in pt, "ไม่ระบุคงเหลือหยุดคำนวณ"
    return "leaver EMP-004: คำขอค้าง revoked · balance สิทธิ์สิ้นสุด+คงเหลือหยุด (ended≠null)"


def c_fn17(page):
    """[FN-17 · S-14 · BR-10] สถานะจ่าย = อ่านจาก Payroll/Expense display-only — Welfare ไม่จ่าย/ไม่ CRUD"""
    open_(page)
    after(page, "() => openDrawer('request-view','REQ-2569-0012')")   # approved · pay sent
    dt = drawer_text(page)
    assert "อ่านจาก Payroll/Expense" in dt, "ไม่ระบุว่าอ่านจากปลายทาง"
    assert "display-only" in dt and "Welfare ไม่จ่ายเอง" in dt, "ไม่ยืนยัน display-only / ไม่จ่ายเอง"
    assert "ส่งจ่ายแล้ว" in dt, "ไม่แสดงสถานะจ่ายจากปลายทาง"
    return "สถานะจ่าย display-only จาก Payroll/Expense (Welfare ไม่จ่ายเอง)"


def c_fn18(page):
    """[FN-18 · S-15 · BR-06] พนักงานเข้าใหม่ (joiner) เข้ากลุ่ม → สิทธิ์เปิดอัตโนมัติ"""
    open_(page)
    assert ev(page, "() => empById('EMP-006').joiner") is True, "EMP-006 ควรเป็น joiner"
    assert ev(page, "() => eligibility(empById('EMP-006'),benById('B-HEALTH'),'2026-10-01').ok") is True, \
        "joiner เข้ากลุ่มแล้วสิทธิ์ไม่เปิด"
    go_tab(page, "balance")
    after(page, "() => { state.balance.empId='EMP-006'; render(); }")
    pt = pc_text(page)
    assert "เข้าใหม่" in pt and "สิทธิ์เปิดอัตโนมัติ" in pt, "ไม่แสดง joiner note (สิทธิ์เปิดอัตโนมัติ)"
    return "joiner EMP-006 → สิทธิ์เปิดอัตโนมัติ (eligibility ok + note)"


def c_fn19(page):
    """[FN-19 · S-16 · BR-08] รายงานการใช้สิทธิ์ตามประเภท/กลุ่ม/ช่วงเวลา + filter ทำงานจริง"""
    open_(page)
    go_tab(page, "report")
    rows = lambda: ev(page, "() => [...document.querySelectorAll('.list-card .table tbody tr')].filter(tr=>!tr.querySelector('.empty')).length")
    base = rows()
    assert base == 2, f"baseline รายงานควรมี 2 ประเภท (B-HEALTH,B-EDU) ได้ {base}"
    # filter ตามประเภท
    after(page, "() => { state.repFilter.type='B-HEALTH'; render(); }")
    assert rows() == 1, "filter ประเภทไม่ลดแถว"
    after(page, "() => { state.repFilter.type='all'; render(); }")
    # filter ตามช่วงเวลา (ตั้งแต่ 2026-04-01 → ตัด REQ มี.ค. ออก)
    after(page, "() => { state.repFilter.from='2026-04-01'; render(); }")
    assert rows() == 1 and "ค่าเล่าเรียน" in pc_text(page), "filter ช่วงเวลาไม่ทำงาน"
    after(page, "() => { state.repFilter.from=''; state.repFilter.group='g-prob'; render(); }")
    assert rows() == 0 and "ไม่พบข้อมูลตามตัวกรอง" in pc_text(page), "filter กลุ่มไม่ทำงาน/ไม่มี empty state"
    return "รายงาน: baseline 2 → ประเภท=1 · ช่วงเวลา=1 · กลุ่ม(g-prob)=0 (empty) — filter ครบ"


# ═══════════════════════════════ GENERAL FN ═══════════════════════════════

def c_fn90(page):
    """[FN-90] ค้นหา/filter ใน list ทำงานจริง + empty state"""
    open_(page)
    after(page, "() => { state.filters.regSearch='zzzไม่มีจริง'; renderTableOnly('registry'); }")
    assert "ไม่พบรายการที่ค้นหา" in pc_text(page), "ค้นไม่เจอแต่ไม่ขึ้น empty state"
    after(page, "() => { state.filters.regSearch='ประกัน'; renderTableOnly('registry'); }")
    t2 = pc_text(page)
    assert "ประกันสุขภาพกลุ่ม" in t2 and "ไม่พบรายการที่ค้นหา" not in t2, "ค้นเจอแต่ไม่แสดงผล"
    return "search registry: เจอ/ไม่เจอ + empty state"


def c_fn91(page):
    """[FN-91] ปิดใช้/ยกเลิกผ่าน confirm เสมอ + soft archive (confirm gate)"""
    open_(page)
    after(page, "() => openModal('archiveBenefit','B-CHECKUP')")
    assert ev(page, "() => state.modal.type==='archiveBenefit'"), "ปิดใช้ไม่ผ่าน confirm"
    # ยกเลิก confirm → ต้องไม่ archive
    after(page, "() => closeModal()")
    assert ev(page, "() => benById('B-CHECKUP').status") == "active", "ยกเลิก confirm แล้วยัง archive (gate พัง)"
    # ยืนยันจริง → archived + record คงอยู่ (soft)
    n0 = ev(page, "() => BENEFITS.length")
    after(page, "() => openModal('archiveBenefit','B-CHECKUP')")
    after(page, "() => doArchiveBenefit('B-CHECKUP')")
    assert ev(page, "() => benById('B-CHECKUP').status") == "archived", "confirm แล้วไม่ archive"
    assert ev(page, "() => BENEFITS.length") == n0, "soft archive แต่ record หาย"
    return "confirm gate: ยกเลิก=ไม่ archive · ยืนยัน=archived + record คงอยู่ (soft)"


def c_fn92(page):
    """[FN-92] validate field บังคับก่อนบันทึก + กัน double-submit (loader)"""
    open_(page)
    # validate ฟอร์มว่าง
    after(page, "() => openDrawer('benefit-create')")
    assert ev(page, "() => validateBenefit()") is False, "ฟอร์มว่างแต่ validate ผ่าน"
    errs = ev(page, "() => Object.keys(state.form.err||{})")
    assert "name" in errs and "quota" in errs and "groups" in errs, f"validate ไม่ครบทุก field บังคับ: {errs}"
    assert ev(page, "() => state.drawer.open") is True, "validate ไม่ผ่านแต่ลิ้นชักปิด (ควรค้างให้แก้)"
    # double-submit loader — อ่านสถานะปุ่มทันทีก่อน setTimeout ทำงาน
    after(page, """() => { Object.assign(state.form,{name:'X', unit:'money', quota:1000, groups:['g-full'], effFrom:'2027-06-01', err:{}}); }""")
    lock = ev(page, "() => { submitBenefit(); const b=document.getElementById('btn-submit'); return b?{cls:b.className, html:b.innerHTML}:null; }")
    assert lock and "is-disabled" in lock["cls"], "กดส่งแล้วปุ่มไม่ถูกล็อก (double-submit ไม่กัน)"
    assert "spin" in lock["html"] or "กำลังบันทึก" in lock["html"], "ไม่มี loader ระหว่างบันทึก"
    settle(page)
    return "validate ฟอร์มว่าง (name/quota/groups) · กดส่ง=ปุ่มล็อก+loader (กัน double-submit)"


def c_fn93(page):
    """[FN-93] audit บันทึกทุก create/แก้/อนุมัติ/ยกเลิก (append-only)"""
    open_(page)
    after(page, "() => openDrawer('request-view','REQ-2569-0012')")   # approved
    after(page, "() => setDrawerTab('history')")
    dt = drawer_text(page)
    assert "append-only" in dt, "ประวัติไม่ระบุ append-only"
    audit = ev(page, "() => buildAudit(reqById('REQ-2569-0012'))")
    assert len(audit) >= 3, f"audit ควรมีหลายรายการ (สร้าง+อนุมัติ+ตัดคงเหลือ) ได้ {len(audit)}"
    assert audit[0]["title"].startswith("สร้างคำขอ"), "รายการแรกไม่ใช่การสร้าง (ไม่เรียงตามเวลา)"
    assert any("ตัดคงเหลือ" in a["title"] and "7C" in a["title"] for a in audit), "audit ไม่บันทึกการอนุมัติ/ตัดคงเหลือ"
    return f"audit append-only: {len(audit)} รายการ · สร้างเป็นรายการแรก · มีอนุมัติ/ตัดคงเหลือ"


def c_fn94(page):
    """[FN-94 · BR-08] ปิดบัง RESTRICTED (บุคคล/ผู้ติดตาม/มูลค่า) ตาม role ผ่าน demo strip"""
    open_(page)
    # demo strip มีจริง 3 role
    assert ev(page, "() => document.querySelectorAll('#demoRole button').length") == 3, "ไม่มี demo strip เลือก role"
    go_tab(page, "requests")
    # role employee → mask มูลค่า + บุคคล
    after(page, "() => setRole('employee')")
    masked = pc_text(page)
    assert "RESTRICTED" in masked and "12,000" not in masked, "role employee แต่ไม่ mask มูลค่า/บุคคล"
    # role admin → เห็นค่า
    after(page, "() => setRole('admin')")
    full = pc_text(page)
    assert "12,000" in full, "role admin กลับถูก mask"
    # ผู้ติดตาม: employee/manager เห็นไม่ได้ (เฉพาะ admin)
    assert ev(page, "() => { setRole('manager'); return canSeeDependent(); }") is False, "manager ไม่ควรเห็นผู้ติดตาม"
    assert ev(page, "() => { setRole('admin'); return canSeeDependent(); }") is True, "admin ควรเห็นผู้ติดตาม"
    return "mask ตาม role: employee=RESTRICTED · admin=เห็นค่า · ผู้ติดตามเฉพาะ admin"


# ═══════════════════ NEGATIVE (unsupported ×5, rendered → absent) ═══════════════════

NEG_JS = r"""
() => {
  let html='';
  state.role='admin';
  // pages (ทุก tab)
  ['registry','requests','report'].forEach(t=>{ state.tab=t; html+=renderPage(); });
  state.balance.empId='EMP-001'; state.tab='balance'; html+=renderPage();
  // drawers ทุกโหมด
  state.form={}; state.drawer={open:true,mode:'benefit-create',recordId:null,step:1}; html+=renderDrawer();
  state.form={}; state.drawer={open:true,mode:'benefit-view',recordId:'B-HEALTH',step:1}; html+=renderDrawer();
  state.form={}; state.drawer={open:true,mode:'request-create',recordId:null,step:1}; html+=renderDrawer();
  ['detail','files','balance','history'].forEach(tab=>{ state.form={}; state.drawer={open:true,mode:'request-view',recordId:'REQ-2569-0012',step:1,tab}; html+=renderDrawer(); });
  state.form={}; state.drawer={open:true,mode:'dependent-create',recordId:'EMP-001',step:1}; html+=renderDrawer();
  // modals ทุกชนิด
  [['archiveBenefit','B-HEALTH'],['cancel','REQ-2569-0026'],['removeDep',{emp:'EMP-001',dep:'DEP-1'}],
   ['approve','REQ-2569-0023'],['reject','REQ-2569-0023'],['doa','REQ-2569-0026']].forEach(m=>{
     state.modal={open:true,type:m[0],data:m[1]}; html+=renderModal(); });
  const box=document.createElement('div'); box.innerHTML=html;
  const acts=[...box.querySelectorAll('button,[onclick]')].filter(el=>{
    const h=(el.getAttribute('onclick')||'').replace(/\s/g,'');
    return !/^event\.stopPropagation\(\)$/.test(h);
  }).map(el=>({txt:(el.textContent||'').replace(/\s+/g,' ').trim(), on:(el.getAttribute('onclick')||'')}));
  return {
    acts,
    fileInputs: box.querySelectorAll('input[type=file]').length,
    hasDisplayOnly: /display-only/.test(html),
    hasNotPay: /Welfare ไม่จ่ายเอง/.test(html),
    hasReadHook: /อ่านจาก Payroll\/Expense/.test(html),
  };
}
"""


def c_unsupported(page):
    """[NEG · unsupported ×5] เรนเดอร์ทุก affordance จริงแล้ว assert 'ไม่มี' ของห้ามมี"""
    open_(page)
    r = ev(page, NEG_JS)
    acts = r["acts"]

    def hit(pat):
        rx = re.compile(pat, re.I)
        return [a for a in acts if rx.search(a["txt"]) or rx.search(a["on"])]

    assert len(acts) > 10, f"เก็บ affordance ได้น้อยผิดปกติ ({len(acts)}) — surfaces อาจไม่เรนเดอร์"

    # 1) ไม่มีปุ่มจ่ายเงินจริง/เบิก/หักผ่านเงินเดือน (payment = display-only เท่านั้น)
    v1 = hit(r"จ่ายเงิน|เบิกเงิน|เบิกจ่าย|หักเงินเดือน|หักผ่านเงินเดือน|ตัดจ่าย|ชำระเงิน|โอนเงิน|ลงบัญชี|บันทึกบัญชี|payExpense|postExpense|postGl|postGL|postAccount|payout|disburse")
    assert not v1, f"[neg1] พบ affordance จ่ายเงิน/เบิก/หักเงินเดือนจริง: {v1[:3]}"
    assert r["hasDisplayOnly"] and r["hasNotPay"] and r["hasReadHook"], \
        "[neg1] payment ควรเป็น display-only อ่านจาก Payroll/Expense (Welfare ไม่จ่ายเอง)"

    # 2) ไม่มีการจัดการผู้ให้บริการ (โรงพยาบาล/บริษัทประกัน)
    v2 = hit(r"ผู้ให้บริการ|บริษัทประกัน|จัดการโรงพยาบาล|provider|vendor|จัดการผู้ให้|เพิ่มผู้ให้บริการ|manageProvider")
    assert not v2, f"[neg2] พบ affordance จัดการผู้ให้บริการ: {v2[:3]}"

    # 3) ไม่มีสวัสดิการยืดหยุ่น/แต้ม (flex credits)
    v3 = hit(r"flex|แต้ม|credits|สะสมแต้ม|สวัสดิการยืดหยุ่น|แลกแต้ม|flexCredit")
    assert not v3, f"[neg3] พบ affordance flex credits/แต้ม: {v3[:3]}"

    # 4) ไม่มีปุ่มสร้าง/แก้ค่านโยบาย HR กลาง (ปฏิทิน/กลุ่มบริษัท/effective policy)
    #    หมายเหตุ: toggleGrp = เลือกกลุ่มที่ 'สวัสดิการนี้' ครอบ ไม่ใช่ CRUD กลุ่มบริษัทกลาง
    v4 = hit(r"สร้างกลุ่มบริษัท|แก้ไขกลุ่มบริษัท|จัดการกลุ่ม|สร้างกลุ่ม|เพิ่มกลุ่ม|จัดการปฏิทิน|ตั้งค่าปฏิทิน|แก้ไขนโยบาย|จัดการนโยบาย|createGroup|editGroup|manageCalendar|editPolicy|effectivePolicy")
    assert not v4, f"[neg4] พบ affordance สร้าง/แก้ค่านโยบาย HR กลาง: {v4[:3]}"

    # 5) ไม่มีการออกเอกสารเลขรัน/PDF ทางการ (ดาวน์โหลดไฟล์แนบ = อ่านหลักฐาน ไม่ใช่ออกเอกสาร)
    # หมายเหตุ: 'แนบ…ใบรับรองแพทย์' = แนบหลักฐาน (FN-07) ไม่ใช่ 'ออกเอกสาร' → regex จับเฉพาะการ 'ออก/พิมพ์' เอกสารทางการ
    v5 = hit(r"ออกเลขที่|เลขที่เอกสาร|เลขรัน|พิมพ์เอกสาร|พิมพ์ใบ|ออกใบรับรอง|PDF ทางการ|ดาวน์โหลด PDF|exportPdf|generatePdf|printOfficial|certPdf")
    assert not v5, f"[neg5] พบ affordance ออกเอกสารเลขรัน/PDF ทางการ: {v5[:3]}"
    assert r["fileInputs"] == 0, "[neg5] พบช่องอัปโหลดไฟล์จริง (ควร mock)"

    return f"unsupported 5/5 absent ({len(acts)} affordance ตรวจ · payment display-only)"


# ═══════════════════ BASE-KIT LATENT BUG / UI REGRESSION PROBES ═══════════════════

def c_modal_over_drawer(page):
    """[UI-REG] modal เปิดจากในลิ้นชัก (อนุมัติ/ยกเลิก) ต้องอยู่เหนือ drawer (z) — regression F-HR-RECRUIT"""
    open_(page)
    after(page, "() => openDrawer('request-view','REQ-2569-0023')")   # drawer เปิด (pending)
    after(page, "() => openModal('approve','REQ-2569-0023')")         # modal เปิดทับ drawer
    viol = ev(page, JS_MODAL_UNDER_DRAWER)
    assert viol == [], f"modal จมใต้ drawer: {viol}"
    mz = ev(page, "() => parseInt(getComputedStyle(document.querySelector('.modal-backdrop')).zIndex,10)")
    dz = ev(page, "() => parseInt(getComputedStyle(document.querySelector('.drawer')).zIndex,10)")
    assert mz > dz, f"modal z({mz}) ต้อง > drawer z({dz})"
    return f"modal เหนือ drawer (z {mz}>{dz})"


def c_overlay_stack(page):
    """[UI] ไม่มี element แปลกปลอมวาดทับ overlay (drawer+modal เปิดพร้อมกัน)"""
    open_(page)
    after(page, "() => openDrawer('request-view','REQ-2569-0023')")
    after(page, "() => openModal('approve','REQ-2569-0023')")
    viol = ev(page, JS_OVERLAY_STACK)
    assert viol == [], f"มี element วาดทับ overlay: {viol[:4]}"
    return "overlay stack สะอาด"


def c_static_css(page):
    """[UI] CSS var ที่ใช้แต่ไม่ประกาศ (ต้นตอ z-index หาย)"""
    open_(page)
    # --shellbar-h ใช้เฉพาะแบบมี fallback: var(--shellbar-h, 52px) ทั้ง 2 จุด (บรรทัด 376/377)
    # = จุด override ที่ตั้งใจให้ optional ไม่ใช่ z-index var ที่หาย → พิสูจน์แล้ว benign (precedent F-HR-TRAIN)
    # JS_CSSVAR ไม่แยก fallback ออก = false-positive · ไม่แก้ uikit รอบนี้
    BENIGN_VARS = {"--shellbar-h"}
    missing = [v for v in ev(page, JS_CSSVAR) if v not in BENIGN_VARS]
    assert missing == [], f"CSS var ใช้แต่ไม่ประกาศ (ไม่มี fallback): {missing}"
    return "CSS var ครบ (z-index scale ประกาศครบ · --shellbar-h benign fallback-only)"


def c_affordance(page):
    """[UI] ของที่มี onclick ต้องมี cursor:pointer (กดได้แต่ไม่มีสัญญาณ = base-kit bug)"""
    open_(page)
    a1 = ev(page, JS_AFFORDANCE)
    after(page, "() => goTab('requests')")
    a2 = ev(page, JS_AFFORDANCE)
    after(page, "() => openDrawer('request-view','REQ-2569-0023')")
    a3 = ev(page, JS_AFFORDANCE)
    bad = (a1 or []) + (a2 or []) + (a3 or [])
    assert bad == [], f"clickable แต่ไม่มี cursor:pointer: {bad[:5]}"
    return "affordance: ทุกจุดคลิกได้มี cursor:pointer"


def c_no_garbage_text(page):
    """[UI-REG] ไม่มี NaN/undefined/null/[object Object]/Invalid Date รั่วเป็นข้อความบนจอ

    regression F-HR-WELFARE (§C3.8): benefit-view drawer แถว 'ครอบผู้ติดตาม' เคยเรนเดอร์ 'NaN'
    (unary + หลง บีบสตริง HTML เป็น Number). กวาดทุก tab + ทุก drawer/tab + modal สำคัญ.
    """
    open_(page)
    # หน้า list ทุก tab
    for t in ("registry", "requests", "report"):
        go_tab(page, t)
        assert_no_garbage_text(page, scope="body")
    go_tab(page, "balance")
    for emp in ("EMP-001", "EMP-004", "EMP-006"):   # active · leaver · joiner
        after(page, "() => { state.balance.empId='%s'; render(); }" % emp)
        assert_no_garbage_text(page, scope="body")
    # drawers ทุกโหมด (จุดที่บั๊กเดิมอยู่ = benefit-view)
    # reset state.form={} ก่อนสลับโหมด (convention เดียวกับ NEG_JS/c_fn06) = แต่ละ drawer init สด
    for rid in ("B-HEALTH", "B-EDU", "B-CHECKUP"):
        after(page, "() => { state.form={}; openDrawer('benefit-view','%s'); }" % rid)
        assert_no_garbage_text(page, scope="#drawer")
    after(page, "() => { state.form={}; openDrawer('benefit-create'); }")
    assert_no_garbage_text(page, scope="#drawer")
    after(page, "() => { state.form={}; openDrawer('benefit-edit','B-HEALTH'); }")
    assert_no_garbage_text(page, scope="#drawer")
    after(page, "() => { state.form={}; openDrawer('request-create'); }")
    assert_no_garbage_text(page, scope="#drawer")
    after(page, "() => { state.form={}; openDrawer('dependent-create','EMP-001'); }")
    assert_no_garbage_text(page, scope="#drawer")
    # request-view ทุกแท็บ (detail/files/balance/history)
    after(page, "() => { state.form={}; openDrawer('request-view','REQ-2569-0012'); }")
    for tab in ("detail", "files", "balance", "history"):
        after(page, "() => setDrawerTab('%s')" % tab)
        assert_no_garbage_text(page, scope="#drawer")
    # modals สำคัญ
    after(page, "() => openModal('approve','REQ-2569-0023')")
    assert_no_garbage_text(page, scope="#modalBackdrop")
    after(page, "() => { closeModal(); openModal('doa','REQ-2569-0026'); }")
    assert_no_garbage_text(page, scope="#modalBackdrop")
    return "ไม่มี garbage text (NaN/undefined/null/[object Object]/Invalid Date) — กวาด 3 tab + balance ×3 + 7 drawer/tab + 2 modal"


def c_icons(page):
    """[UI] ไม่มี <i data-lucide> ที่เรนเดอร์เป็นไอคอนว่าง"""
    open_(page)
    loaded = ev(page, "() => !!(window.lucide && document.querySelector('svg.lucide'))")
    if loaded:
        after(page, "() => openDrawer('request-view','REQ-2569-0023')")
        miss = unrendered_visible_icons(page, "body")
        assert not miss, f"ไอคอน lucide เรนเดอร์เป็นช่องว่าง: {miss[:6]}"
        return "lucide โหลดจริง · ไอคอนเรนเดอร์ครบ"
    blanks = ev(page, """() => [...document.querySelectorAll('i[data-lucide]')]
      .filter(el=>!(el.getAttribute('data-lucide')||'').trim()).map(el=>el.outerHTML.slice(0,40))""")
    assert blanks == [], f"พบ <i data-lucide> ชื่อว่าง: {blanks[:6]}"
    return "lucide CDN offline — static: ไม่มีชื่อไอคอนว่าง"


# ═══════════════════ DSP-02 · BASE-KIT focus × combobox (F-HR-TRAIN precedent) ═══════════════════

# รอ rAF chain ให้ focus-restore (#29 · restoreRenderState) / trapFocus ทำงานจนจบก่อนอ่านสถานะสุดท้าย
_RAF_SETTLE = "() => new Promise(res=>{let n=0;const t=()=>{n++;if(n>=6)res();else requestAnimationFrame(t);};requestAnimationFrame(t);})"


def c_combo_closes(page):
    """[DSP-02a · UI-REG] request-create: เลือกพนักงาน (reqEmp) → dropdown ปิด · ไม่เด้งกางใหม่จาก focus-restore (#29)

    บั๊กเดิม (BASE-KIT): onSelect→render() แล้ว focus-restore เด้งโฟกัสกลับเข้า ss-input →
    onfocus=ssOpen เปิด dropdown ซ้ำ (input ว่าง · list ค้าง). fix = blur ก่อน render (mirror F-HR-TRAIN L2956).
    """
    open_(page)
    after(page, "() => openDrawer('request-create')")
    assert ev(page, "() => !!(window.__ss && window.__ss['reqEmp'])"), "reqEmp ไม่ถูก init"
    # (1) helper กลาง uikit: เลือกแล้วสถานะต้องปิดทันที (sync) + input โชว์ค่า + open=false
    r = assert_combobox_closes_after_select(page, "reqEmp", 0)
    assert ev(page, "() => !!state.form.empId"), "เลือกพนักงานแล้ว empId ไม่ถูกตั้ง (onSelect ไม่ทำงาน)"
    # (2) real-flow: จำลองการคลิกจริง (focus ss-input ค้าง → ssPick → รอ focus-restore rAF) → dropdown ต้องยังปิด
    #     (นี่คือทางที่บั๊กจริงเกิด: sync helper อย่างเดียวจับ reopen แบบ async ไม่ได้)
    after(page, "() => { state.form={}; openDrawer('request-create'); }")
    ev(page, "() => { const i=document.getElementById('ss-input-reqEmp'); if(i){ i.focus(); ssOpen('reqEmp'); } ssPick('reqEmp',0); }")
    page.evaluate(_RAF_SETTLE)
    st = ev(page, """() => ({
      open:(window.__ss['reqEmp']||{}).open,
      listHidden:(()=>{const l=document.getElementById('ss-list-reqEmp');return l?l.classList.contains('hidden'):null;})(),
      aeIsSs:!!(document.activeElement&&document.activeElement.classList&&document.activeElement.classList.contains('ss-input'))
    })""")
    assert st["open"] is False, f"[DSP-02a] เลือกแล้ว dropdown เด้งกางใหม่หลัง focus-restore (open={st['open']})"
    assert st["listHidden"] is True, "[DSP-02a] list ไม่ปิดหลัง focus-restore (reopen-after-select)"
    assert st["aeIsSs"] is False, "[DSP-02a] focus เด้งกลับเข้า ss-input (fix ไม่ได้ blur ก่อน render)"
    return f"reqEmp: เลือกแล้วปิด (sync helper + หลัง focus-restore rAF) · empId ติด · input='{str(r['inputValue'])[:14]}'"


def c_modal_no_autoopen(page):
    """[DSP-02b · UI-REG] DOA submit modal เปิดขึ้นมา → ไม่มี combobox กาง dropdown เอง (trapFocus auto-open)

    บั๊กเดิม (BASE-KIT): trapFocus auto-focus ช่องแรกของ modal ถ้าเป็น ss-input → onfocus=ssOpen เปิด
    dropdown เองตอน modal โผล่ (ผู้ใช้ยังไม่แตะ). fix = rAF guard ปิดคืนหลัง trapFocus (mirror F-HR-TRAIN L2893).
    """
    open_(page)
    after(page, "() => openModal('doa','REQ-2569-0026')")   # DOA slot picker (doaSlot1 = ช่องแรก)
    page.evaluate(_RAF_SETTLE)   # รอ rAF chain: mb.is-open → trapFocus focus → guard blur/ปิด
    st = ev(page, """() => ({
      modalOpen: state.modal.open===true && state.modal.type==='doa',
      slot1Open: (window.__ss && window.__ss['doaSlot1']) ? window.__ss['doaSlot1'].open : null,
      listHidden: (()=>{const l=document.getElementById('ss-list-doaSlot1');return l?l.classList.contains('hidden'):null;})(),
      aeIsSs: !!(document.activeElement&&document.activeElement.classList&&document.activeElement.classList.contains('ss-input'))
    })""")
    assert st["modalOpen"], "DOA modal ไม่เปิด"
    assert st["slot1Open"] is False, f"[DSP-02b] doaSlot1 กาง dropdown เองตอน modal เปิด (open={st['slot1Open']})"
    assert st["listHidden"] is True, "[DSP-02b] #ss-list-doaSlot1 ไม่ hidden ตอน modal เพิ่งเปิด"
    assert st["aeIsSs"] is False, "[DSP-02b] activeElement ยังเป็น ss-input (guard ไม่ได้ blur)"
    # helper กลาง uikit: ไม่มี combobox ตัวไหนใน modal กางเอง
    auto = modal_autoopens_comboboxes(page)
    assert auto == [], f"[DSP-02b] มี combobox กาง dropdown เองใน DOA modal: {auto}"
    return "DOA modal เปิด → ไม่มี combobox กางเอง (doaSlot1 open=false·list hidden·blur·helper สะอาด)"


def c_person_cell_collision(page):
    """[UI-REG · §C3.8] เซลล์บุคคล (.tbl-person) ชื่อ (.pn) กับตำแหน่ง·แผนก (.pm) ต้องคนละบรรทัด

    บั๊กเดิม (F-HR-WELFARE): .pmain หล่น display:flex;flex-direction:column → .pn/.pm (span inline)
    ไหลต่อกันบรรทัดเดียว "สุนิสา วงศ์ทองนักบัญชี · ฝ่ายบัญชี". ตัววัดเดิมมองไม่เห็น (ไม่ล้น/ไม่ทับ).
    บั๊กโผล่เฉพาะตอนคอลัมน์กว้างพอให้ทั้งสอง span อยู่บรรทัดเดียวได้ (ที่ 1280 span จะ wrap เองบังบั๊ก)
    → ต้องขยาย viewport ให้กว้างก่อนตรวจ ไม่งั้นจอแคบซ่อนบั๊กไว้.
    .tbl-person เรนเดอร์ที่คอลัมน์ "ผู้ยื่น" ของแท็บคำขอเท่านั้น (personCell) — แท็บอื่นไม่มีเซลล์บุคคล.
    """
    open_(page)
    page.set_viewport_size({"width": 1600, "height": 950})
    go_tab(page, "requests")
    n = ev(page, "() => document.querySelectorAll('#page-content .tbl-person').length")
    assert n >= 3, f"แท็บคำขอควรมีเซลล์บุคคลหลายเซลล์ (ได้ {n}) — surface อาจไม่เรนเดอร์"
    assert_no_person_cell_collision(page, scope="#page-content")
    page.set_viewport_size({"width": 1280, "height": 900})
    return f"person cell: ชื่อ/ตำแหน่งคนละบรรทัด ({n} เซลล์ @1600w · .pmain flex-column)"


# ═══════════════ BYPASS CATALOG GUARDS (§C3.8 — logic holes เดิมไม่มีเคสครอบ) ═══════════════

def c_b1(page):
    """[B1 · FN-13] doApprove precondition (FIX-01): อนุมัติ record สถานะปลายทางไม่ได้ (rejected/cancelled/draft/approved)"""
    open_(page)
    after(page, "() => doApprove('REQ-2569-0025')")   # rejected
    assert ev(page, "() => reqById('REQ-2569-0025').status") == "rejected", "อนุมัติ record rejected ได้ (FIX-01 หลุด)"
    after(page, "() => doApprove('REQ-2569-0027')")   # cancelled
    assert ev(page, "() => reqById('REQ-2569-0027').status") == "cancelled", "อนุมัติ record cancelled ได้"
    after(page, "() => doApprove('REQ-2569-0026')")   # draft
    assert ev(page, "() => reqById('REQ-2569-0026').status") == "draft", "อนุมัติ record draft ได้"
    used0 = ev(page, "() => usedByPerson('EMP-001','B-HEALTH')")
    after(page, "() => doApprove('REQ-2569-0012')")   # approved อยู่แล้ว
    assert ev(page, "() => reqById('REQ-2569-0012').status") == "approved", "re-approve record approved เปลี่ยน state"
    assert ev(page, "() => usedByPerson('EMP-001','B-HEALTH')") == used0, "re-approve ตัดคงเหลือซ้ำ (double-count)"
    return "B1: doApprove บน rejected/cancelled/draft/approved → status ไม่เปลี่ยน · ไม่ตัดคงเหลือซ้ำ (FIX-01)"


def c_b2(page):
    """[B2 · FN-08/FN-13] DOA advance ทีละขั้น (FIX-03): คลิกแรก ขั้น1 approved+at·ขั้น2 current·คำขอ pending · คลิกสอง approved (ทุกขั้นมี at) · ตัดคงเหลือ/EC ครั้งเดียว"""
    open_(page)
    # สร้างสาย 2 ขั้นสด (step1 current, step2 pending) ผ่าน DOA flow จริง จาก draft REQ-2569-0026
    after(page, "() => openModal('doa','REQ-2569-0026')")
    after(page, "() => ssPick('doaSlot1',0)")
    after(page, "() => ssPick('doaSlot2',0)")
    after(page, "() => confirmDoa('REQ-2569-0026')")
    ap0 = ev(page, "() => reqById('REQ-2569-0026').approvals.map(a=>({step:a.step,status:a.status,at:a.at}))")
    assert ap0[0]["status"] == "current" and ap0[1]["status"] == "pending", f"สายเริ่มต้นไม่ใช่ step1 current/step2 pending: {ap0}"
    emp = ev(page, "() => reqById('REQ-2569-0026').empId")
    ben = ev(page, "() => reqById('REQ-2569-0026').benefitId")
    used0 = ev(page, "() => usedByPerson('%s','%s')" % (emp, ben))
    # คลิกแรก → advance ขั้น 1 เท่านั้น
    after(page, "() => doApprove('REQ-2569-0026')")
    ap1 = ev(page, "() => reqById('REQ-2569-0026').approvals.map(a=>({step:a.step,status:a.status,at:a.at}))")
    assert ev(page, "() => reqById('REQ-2569-0026').status") == "pending", f"คลิกแรกแล้วคำขอควรยัง pending: {ap1}"
    assert ap1[0]["status"] == "approved" and ap1[0]["at"], "ขั้น1 ควร approved + มี at"
    assert ap1[1]["status"] == "current", "ขั้น2 ควรถูกเลื่อนเป็น current"
    assert ev(page, "() => usedByPerson('%s','%s')" % (emp, ben)) == used0, "ยังไม่ถึงขั้นสุดท้ายแต่ตัดคงเหลือแล้ว (ต้องครั้งเดียวตอนจบ)"
    # คลิกสอง → ขั้นสุดท้าย finalize
    after(page, "() => doApprove('REQ-2569-0026')")
    ap2 = ev(page, "() => reqById('REQ-2569-0026').approvals.map(a=>({step:a.step,status:a.status,at:a.at}))")
    assert ev(page, "() => reqById('REQ-2569-0026').status") == "approved", "คลิกสองแล้วควร approved"
    assert all(a["status"] == "approved" and a["at"] for a in ap2), f"ทุกขั้นที่ approved ต้องมี at: {ap2}"
    assert ev(page, "() => reqById('REQ-2569-0026').pay") == "pending", "ขั้นสุดท้ายควรตั้ง pay=pending"
    assert ev(page, "() => usedByPerson('%s','%s')" % (emp, ben)) == used0 + ev(page, "() => reqById('REQ-2569-0026').amount"), "ตัดคงเหลือไม่ตรง (ควรตัดครั้งเดียวตอนขั้นสุดท้าย)"
    return "B2: advance ทีละขั้น (step1 approved+at → step2 current → approved ทุกขั้นมี at) · ตัดคงเหลือ/EC ครั้งเดียว (FIX-03)"


def c_b3(page):
    """[B3/B8 · FN-10/FN-13] re-check เพดาน+eligibility ณ อนุมัติ (FIX-02): 2 pending รวมเกินโควตา → ใบสองถูก block (usedByPerson ≤ quota) · benefit archived → อนุมัติไม่ได้"""
    open_(page)
    # EMP-001 · B-HEALTH quota 30,000 · approved เดิม 12,000 · rem 18,000
    # inject 2 pending ใบละ 18,000 (จำลอง 'ต่างผ่าน submit เพราะ pending ไม่จองสิทธิ์' — OQ-WEL-03) เป็นสาย 1 ขั้น
    after(page, """() => {
      const mk=(id,val)=>({id, empId:'EMP-001', useFor:{type:'self'}, benefitId:'B-HEALTH', amount:val, value:val,
        useDate:'2026-06-01', reason:'', status:'pending', pay:'none', files:[],
        approvals:[{step:1, role:'หัวหน้าสายงาน', person:{name:'วิชัย ประเสริฐ',position:'ผู้จัดการฝ่ายวิศวกรรม'}, status:'current', at:null}],
        createdAt:'2026-06-01'});
      REQUESTS.unshift(mk('REQ-QA-A',18000)); REQUESTS.unshift(mk('REQ-QA-B',18000));
    }""")
    after(page, "() => doApprove('REQ-QA-A')")   # 12,000 + 18,000 = 30,000 (พอดีโควตา)
    assert ev(page, "() => reqById('REQ-QA-A').status") == "approved", "ใบแรก (พอดีโควตา) ควรอนุมัติได้"
    after(page, "() => doApprove('REQ-QA-B')")   # want 18,000 > rem 0 → block
    assert ev(page, "() => reqById('REQ-QA-B').status") == "pending", "ใบสองเกินโควตาแต่อนุมัติผ่าน (FIX-02 หลุด)"
    assert ev(page, "() => usedByPerson('EMP-001','B-HEALTH')") <= 30000, "usedByPerson ทะลุโควตา"
    # B8: archive benefit ที่มี pending อ้าง → อนุมัติคำขอค้างไม่ได้ (eligibility ณ อนุมัติ)
    after(page, "() => doArchiveBenefit('B-CHECKUP')")   # REQ-2569-0023 (pending, step2 current) อ้าง B-CHECKUP
    after(page, "() => doApprove('REQ-2569-0023')")
    assert ev(page, "() => reqById('REQ-2569-0023').status") == "pending", "benefit archived แล้วยังอนุมัติคำขอค้างได้ (B8 หลุด)"
    return "B3/B8: 2 pending เกินโควตา→ใบสอง block (used≤30,000) · benefit archived→อนุมัติไม่ได้ (FIX-02)"


def c_b4(page):
    """[B4 · FN-94] persona guard (FIX-04): role employee → doApprove/doReject/doCancelRequest no-op + ปุ่มไม่ render"""
    open_(page)
    after(page, "() => setRole('employee')")
    after(page, "() => doApprove('REQ-2569-0023')")
    assert ev(page, "() => reqById('REQ-2569-0023').status") == "pending", "employee อนุมัติได้ (guard หลุด)"
    after(page, "() => { const t=document.getElementById('rejectReason'); if(t)t.value='x'; doReject('REQ-2569-0023'); }")
    assert ev(page, "() => reqById('REQ-2569-0023').status") == "pending", "employee ปฏิเสธได้"
    after(page, "() => doCancelRequest('REQ-2569-0026')")
    assert ev(page, "() => reqById('REQ-2569-0026').status") == "draft", "employee ยกเลิกได้"
    # ปุ่มอนุมัติ/ไม่อนุมัติ ไม่ถูก render ใน header actions (pending)
    after(page, "() => openDrawer('request-view','REQ-2569-0023')")
    txts = ev(page, "() => [...document.querySelectorAll('#drawer .drawer-header-actions button')].map(b=>b.textContent.replace(/\\s+/g,' ').trim())")
    assert "อนุมัติ" not in txts and "ไม่อนุมัติ" not in txts, f"employee เห็นปุ่มอนุมัติ/ไม่อนุมัติ: {txts}"
    # admin กลับมาทำได้ปกติ (สลับ role แล้วปุ่มโผล่)
    after(page, "() => { setRole('admin'); openDrawer('request-view','REQ-2569-0023'); }")
    txts2 = ev(page, "() => [...document.querySelectorAll('#drawer .drawer-header-actions button')].map(b=>b.textContent.replace(/\\s+/g,' ').trim())")
    assert "อนุมัติ" in txts2, f"admin ควรเห็นปุ่มอนุมัติ: {txts2}"
    return "B4: employee doApprove/doReject/doCancelRequest no-op + ปุ่มไม่ render · admin เห็นปุ่ม (FIX-04)"


def c_b5(page):
    """[B5 · FN-15] doCancelRequest status guard (FIX-05): approved/rejected ยกเลิกไม่ได้ (ยอดใช้คงเดิม) · draft/pending ยกเลิกได้"""
    open_(page)
    used0 = ev(page, "() => usedByPerson('EMP-001','B-HEALTH')")   # 12,000
    after(page, "() => doCancelRequest('REQ-2569-0012')")   # approved + pay sent
    assert ev(page, "() => reqById('REQ-2569-0012').status") == "approved", "ยกเลิกคำขอ approved ได้ (FIX-05 หลุด)"
    assert ev(page, "() => usedByPerson('EMP-001','B-HEALTH')") == used0, "ยกเลิก approved ทำยอดใช้สิทธิ์หาย"
    after(page, "() => doCancelRequest('REQ-2569-0025')")   # rejected
    assert ev(page, "() => reqById('REQ-2569-0025').status") == "rejected", "ยกเลิก record rejected ได้"
    after(page, "() => doCancelRequest('REQ-2569-0026')")   # draft → ยกเลิกได้
    assert ev(page, "() => reqById('REQ-2569-0026').status") == "cancelled", "draft ยกเลิกไม่ได้"
    after(page, "() => doCancelRequest('REQ-2569-0023')")   # pending → ยกเลิกได้
    assert ev(page, "() => reqById('REQ-2569-0023').status") == "cancelled", "pending ยกเลิกไม่ได้"
    return "B5: ยกเลิก approved/rejected → block (ยอดใช้คงเดิม) · draft/pending → cancelled (FIX-05)"


def c_archive_warn(page):
    """[FIX-06 · FN-03] confirm archive แจ้งจำนวนคำขอค้างที่อ้าง benefit"""
    open_(page)
    after(page, "() => openModal('archiveBenefit','B-CHECKUP')")   # REQ-2569-0023 pending อ้างอยู่ 1 ใบ
    mt = modal_text(page)
    assert "มีคำขอรอดำเนินการ 1 ใบ" in mt, f"archive ที่มี pending ไม่แจ้งจำนวน: '{mt}'"
    after(page, "() => { closeModal(); openModal('archiveBenefit','B-EDU'); }")   # ไม่มี pending อ้าง
    mt2 = modal_text(page)
    assert "มีคำขอรอดำเนินการ" not in mt2, "benefit ที่ไม่มีคำขอค้างกลับแจ้งว่ามี"
    return "FIX-06: archive มี pending → confirm ระบุ '1 ใบ' · ไม่มีค้าง → ไม่แจ้ง"


def c_payroll_surface(page):
    """[FIX-07 · c4] balance tab: section 'จ่ายประจำผ่านเงินเดือน' โชว์ PVD (%) + สถานะส่งเข้ารอบ + hook ไป F065 (display-only)"""
    open_(page)
    go_tab(page, "balance")
    after(page, "() => { state.balance.empId='EMP-001'; render(); }")   # g-full → มี PVD (percent)
    pt = pc_text(page)
    assert "จ่ายประจำผ่านเงินเดือน" in pt, "ไม่มี section จ่ายประจำผ่านเงินเดือน"
    assert "กองทุนสำรองเลี้ยงชีพ" in pt, "section จ่ายประจำไม่แสดง PVD"
    assert "ส่งเข้ารอบเงินเดือนถัดไป" in pt, "ไม่มีสถานะส่งเข้ารอบเงินเดือน"
    assert "Payroll (F065)" in pt and "display-only" in pt, "ไม่ระบุ hook ไป F065 / display-only"
    # แก้ % ได้ (mock display-only) → เก็บใน state.payrollPct
    after(page, "() => setPayrollPct('EMP-001','B-PVD',7)")
    assert ev(page, "() => payrollPctOf('EMP-001','B-PVD')") == 7, "แก้สัดส่วน % ไม่ถูกเก็บ"
    return "FIX-07: จ่ายประจำผ่านเงินเดือน (PVD % · ส่งเข้ารอบ · hook F065 display-only · % แก้ได้)"


def c_person_combo_avatar(page):
    """[FIX-08 · #102] combobox คน (reqEmp/doaSlot) มี avatar ในทุก option (anatomy avatar→ชื่อ→ตำแหน่ง)"""
    open_(page)
    after(page, "() => openDrawer('request-create')")
    emp_ok = ev(page, "() => { const s=window.__ss['reqEmp']; return s && s.options.length>0 && s.options.every(o=>o.avatar && o.label && o.sub); }")
    assert emp_ok, "reqEmp options ไม่มี avatar ครบทุกตัว"
    after(page, "() => { ssOpen('reqEmp'); }")
    av = ev(page, "() => document.querySelectorAll('#ss-list-reqEmp .ss-opt .ss-opt-av').length")
    assert av > 0, "dropdown reqEmp ไม่เรนเดอร์ avatar (.ss-opt-av)"
    after(page, "() => { closeDrawer(); openModal('doa','REQ-2569-0026'); }")
    doa_ok = ev(page, "() => { const s=window.__ss['doaSlot1']; return s && s.options.every(o=>o.avatar); }")
    assert doa_ok, "doaSlot1 options ไม่มี avatar"
    return f"FIX-08: person combobox มี avatar #102 (reqEmp render {av} avatar · doaSlot avatar ครบ)"


def c_joindate_century(page):
    """[FIX-09] joinDate เป็น ค.ศ. — balance tab แสดงปี พ.ศ. 25xx ไม่มี 31xx"""
    open_(page)
    go_tab(page, "balance")
    bad = []
    for emp in ("EMP-001", "EMP-002", "EMP-004", "EMP-005"):
        after(page, "() => { state.balance.empId='%s'; render(); }" % emp)
        pt = pc_text(page)
        if re.search(r"31\d\d", pt):
            bad.append(emp)
    assert not bad, f"พบปีเข้างาน 31xx (joinDate ยังเป็น พ.ศ.): {bad}"
    return "FIX-09: joinDate ค.ศ. → ปีเข้างานแสดง 25xx (ไม่มี 31xx)"


def c_rev1(page):
    """[R1 · FN-13/FN-93 · OQ-WEL-01] กลับรายการคำขออนุมัติแล้ว (admin) → reversed + คืนคงเหลือ + EC-reverse + payroll clawback (append-only)"""
    open_(page)
    used0 = ev(page, "() => usedByPerson('EMP-001','B-HEALTH')")   # 12,000 (REQ-2569-0012 approved)
    assert used0 == 12000, f"ยอดใช้เริ่มต้นไม่ใช่ 12000 (ได้ {used0})"
    val0 = ev(page, "() => reqById('REQ-2569-0012').value")
    after(page, "() => openModal('reverse','REQ-2569-0012')")
    mt = modal_text(page)
    assert "เหตุผลการกลับรายการ" in mt and "คืนมูลค่าเข้าเงินได้" in mt, f"modal กลับรายการไม่ครบ: '{mt}'"
    assert "แจ้ง Payroll ตั้งเบิกคืน" in mt, "pay sent แต่ modal ไม่แจ้ง clawback"
    # เหตุว่าง → บล็อก (mirror doReject)
    after(page, "() => doReverse('REQ-2569-0012')")
    assert ev(page, "() => reqById('REQ-2569-0012').status") == "approved", "เหตุว่างแต่กลับรายการผ่าน"
    # ใส่เหตุ → reversed
    after(page, "() => { document.getElementById('reverseReason').value='อนุมัติผิดคน'; }")
    after(page, "() => doReverse('REQ-2569-0012')")
    toast = ev(page, "() => document.getElementById('toast').textContent")
    assert "กลับรายการแล้ว" in toast and "แจ้งเตือนผู้ยื่น" in toast, f"toast NTF ไม่ครบ: '{toast}'"
    r = ev(page, "() => reqById('REQ-2569-0012')")
    assert r["status"] == "reversed", f"กลับรายการแล้วสถานะไม่ reversed (ได้ {r['status']})"
    assert r["reverseReason"] == "อนุมัติผิดคน", "ไม่บันทึกเหตุกลับรายการ"
    assert r.get("reversedAt"), "ไม่บันทึกวันที่กลับรายการ"
    assert r.get("payrollClawback") is True, "pay sent แต่ไม่ตั้ง flag แจ้ง Payroll ตั้งเบิกคืน"
    # append-only: ข้อมูลเดิมคงไว้
    assert r["value"] == val0 and r["amount"] == 12000, "กลับรายการแล้วข้อมูลมูลค่า/จำนวนเดิมหาย (ไม่ append-only)"
    # คืนคงเหลืออัตโนมัติ — usedByPerson นับเฉพาะ approved (ไม่ปรับซ้ำ)
    used1 = ev(page, "() => usedByPerson('EMP-001','B-HEALTH')")
    assert used1 == used0 - 12000, f"กลับรายการแล้วคงเหลือไม่คืน (used {used0}→{used1})"
    # audit append-only: EC-reverse + payroll clawback + การอนุมัติเดิมยังอยู่
    after(page, "() => { openDrawer('request-view','REQ-2569-0012'); setDrawerTab('history'); }")
    dt = drawer_text(page)
    assert "กลับรายการ · คืนมูลค่าเข้าเงินได้ (7C · EC)" in dt, "ประวัติไม่มีบรรทัด EC-reverse"
    assert "แจ้ง Payroll ตั้งเบิกคืน" in dt, "ประวัติไม่มีบรรทัดแจ้ง Payroll ตั้งเบิกคืน"
    assert "ตัดคงเหลือ" in dt, "ประวัติการอนุมัติเดิมหาย (ไม่ append-only)"
    return "R1: reversed + คืนคงเหลือ 12000→0 · EC-reverse + payroll clawback · append-only · NTF toast"


def c_rev2(page):
    """[R2 · FN-15 · OQ-WEL-01] doReverse บนคำขอที่ยังไม่อนุมัติ (pending/draft/rejected/cancelled) → บล็อก + สถานะคงเดิม"""
    open_(page)
    for rid, st in (("REQ-2569-0023", "pending"), ("REQ-2569-0026", "draft"),
                    ("REQ-2569-0025", "rejected"), ("REQ-2569-0027", "cancelled")):
        after(page, "() => { const t=document.getElementById('reverseReason'); if(t)t.value='x'; doReverse('%s'); }" % rid)
        cur = ev(page, "() => reqById('%s').status" % rid)
        assert cur == st, f"{rid}: doReverse เปลี่ยนสถานะจาก {st} → {cur} (guard หลุด)"
    toast = ev(page, "() => document.getElementById('toast').textContent")
    assert "กลับรายการได้เฉพาะคำขอที่อนุมัติแล้ว" in toast, f"ไม่ขึ้น toast status guard: '{toast}'"
    return "R2: doReverse บน pending/draft/rejected/cancelled → บล็อก ทุกตัวสถานะคงเดิม"


def c_rev3(page):
    """[R3 · FN-94 · OQ-WEL-01] role employee → doReverse no-op + ปุ่มกลับรายการไม่ render (persona guard FIX-04)"""
    open_(page)
    after(page, "() => setRole('employee')")
    after(page, "() => { const t=document.getElementById('reverseReason'); if(t)t.value='x'; doReverse('REQ-2569-0012'); }")
    assert ev(page, "() => reqById('REQ-2569-0012').status") == "approved", "employee กลับรายการได้ (guard หลุด)"
    after(page, "() => openDrawer('request-view','REQ-2569-0012')")
    txts = ev(page, "() => [...document.querySelectorAll('#drawer .drawer-header-actions button')].map(b=>b.textContent.replace(/\\s+/g,' ').trim())")
    assert "กลับรายการ" not in txts, f"employee เห็นปุ่มกลับรายการ: {txts}"
    after(page, "() => { setRole('admin'); openDrawer('request-view','REQ-2569-0012'); }")
    txts2 = ev(page, "() => [...document.querySelectorAll('#drawer .drawer-header-actions button')].map(b=>b.textContent.replace(/\\s+/g,' ').trim())")
    assert "กลับรายการ" in txts2, f"admin ควรเห็นปุ่มกลับรายการ: {txts2}"
    return "R3: employee doReverse no-op + ปุ่มไม่ render · admin เห็นปุ่มกลับรายการ (FIX-04)"


def c_rev4(page):
    """[R4 · FN-15 · FIX-05/OQ-WEL-01] ขอบเขตไม่ทับกัน: cancel=draft/pending (FIX-05 intact) · reverse=approved เท่านั้น"""
    open_(page)
    used0 = ev(page, "() => usedByPerson('EMP-001','B-HEALTH')")   # 12,000
    # FIX-05: cancel บน approved ยังบล็อก (reversal ไม่เปิดทาง cancel หลังอนุมัติ)
    after(page, "() => doCancelRequest('REQ-2569-0012')")
    assert ev(page, "() => reqById('REQ-2569-0012').status") == "approved", "cancel บน approved ผ่าน (FIX-05 หลุด)"
    assert ev(page, "() => usedByPerson('EMP-001','B-HEALTH')") == used0, "cancel approved ทำยอดใช้หาย"
    # reverse บน draft ต้องบล็อก (reverse ไม่ล้ำเข้าขอบเขต pre-approval)
    after(page, "() => { const t=document.getElementById('reverseReason'); if(t)t.value='x'; doReverse('REQ-2569-0026'); }")
    assert ev(page, "() => reqById('REQ-2569-0026').status") == "draft", "reverse บน draft ผ่าน (ล้ำขอบเขต)"
    # cancel ยังทำงานบน draft/pending ตามเดิม
    after(page, "() => doCancelRequest('REQ-2569-0026')")
    assert ev(page, "() => reqById('REQ-2569-0026').status") == "cancelled", "cancel บน draft ไม่ทำงาน (FIX-05 พัง)"
    after(page, "() => doCancelRequest('REQ-2569-0023')")
    assert ev(page, "() => reqById('REQ-2569-0023').status") == "cancelled", "cancel บน pending ไม่ทำงาน (FIX-05 พัง)"
    return "R4: cancel=draft/pending (FIX-05 intact) · reverse=approved · สองขอบเขตไม่ทับกัน"


def c_exposure(page):
    """[EX · FN-13 · OQ-WEL-03] balance tab แสดง exposure คำขอรออนุมัติอื่นบนสิทธิ์เดียวกัน (display-only · ไม่แทน hard re-check FIX-02)"""
    open_(page)
    after(page, "() => { openDrawer('request-view','REQ-2569-0012'); setDrawerTab('balance'); }")
    dt0 = drawer_text(page)
    assert "คำขอรออนุมัติอื่นของสิทธิ์นี้" in dt0, "balance tab ไม่มีบรรทัด exposure"
    assert "0 ใบ" in dt0, f"exposure เริ่มต้นควร 0 ใบ: '{dt0[:220]}'"
    # เพิ่ม 2 คำขอ pending บน EMP-001 + B-HEALTH เดียวกัน
    after(page, """() => { REQUESTS.push({id:'REQ-EX-1',empId:'EMP-001',useFor:{type:'self'},benefitId:'B-HEALTH',amount:3000,value:3000,useDate:'2026-09-01',reason:'',status:'pending',pay:'none',files:[],approvals:[],createdAt:'2026-09-01'});
      REQUESTS.push({id:'REQ-EX-2',empId:'EMP-001',useFor:{type:'self'},benefitId:'B-HEALTH',amount:2000,value:2000,useDate:'2026-09-02',reason:'',status:'pending',pay:'none',files:[],approvals:[],createdAt:'2026-09-02'}); }""")
    n = ev(page, "() => REQUESTS.filter(x=>x.empId==='EMP-001'&&x.benefitId==='B-HEALTH'&&x.status==='pending'&&x.id!=='REQ-2569-0012').length")
    assert n == 2, f"inject pending ไม่ครบ (ได้ {n})"
    after(page, "() => { openDrawer('request-view','REQ-2569-0012'); setDrawerTab('balance'); }")
    dt1 = drawer_text(page)
    assert "2 ใบ" in dt1, f"exposure ไม่แสดง 2 ใบ: '{dt1[:220]}'"
    assert "รวม" in dt1, "exposure ไม่แสดงยอดรวม"
    return "EX: exposure 0 ใบ → เพิ่ม 2 pending → '2 ใบ · รวม' (display-only · FIX-02 hard re-check คงเดิม)"


# ═══════════════════════════════ RUN ═══════════════════════════════

CASES = [
    ('E01', '[FN-01 · S-01] สร้างประเภทสวัสดิการ (กลุ่ม+โควตา+วันมีผล)', c_fn01),
    ('E01b', '[FN-01/FN-02] benefit draft lifecycle: บันทึกร่าง=in-place draft · บันทึก=publish→active', c_fn01b),
    ('E02', '[FN-02 · S-02] แก้=ออกเวอร์ชันใหม่ · เวอร์ชันเก่าอ้างอิงได้', c_fn02),
    ('E03', '[FN-03 · S-03] ปิดใช้ soft archive · ไม่ hard delete', c_fn03),
    ('E04', '[FN-04 · S-04] บล็อกโควตา≤0 + ช่วงมีผลทับกัน (BR-03)', c_fn04),
    ('E05', '[FN-05 · S-05] เพิ่มผู้ติดตาม', c_fn05),
    ('E06', '[FN-06 · S-06] บุตรอายุเกิน บล็อก · เกินจำนวน เตือน', c_fn06),
    ('E07', '[FN-07 · S-07] สร้างคำขอ เลือกประเภทมีสิทธิ์+ผู้ใช้สิทธิ์+แนบ', c_fn07),
    ('E08', '[FN-08 · S-07] DOA slot picker เลือกคน (ไม่ hardcode)', c_fn08),
    ('E09', '[FN-09 · S-08] ใช้สิทธิ์บางส่วน คงเหลือถูกต้อง', c_fn09),
    ('E10', '[FN-10 · S-09] ขอเกินคงเหลือ บล็อก+แสดงคงเหลือ', c_fn10),
    ('E11', '[FN-11 · S-10] ยื่นประเภทไม่มีสิทธิ์ บล็อก+เหตุ', c_fn11),
    ('E12', '[FN-12 · S-07] ดูสถานะ+สาย DOA', c_fn12),
    ('E13', '[FN-13 · S-07] อนุมัติ→ตัดคงเหลือ+7C EC+payment hook', c_fn13),
    ('E14', '[FN-14 · S-11] ไม่อนุมัติ ไม่ตัด+เหตุ+แจ้งเตือน', c_fn14),
    ('E15', '[FN-15 · S-12] ยกเลิกก่อนอนุมัติ', c_fn15),
    ('E16', '[FN-16 · S-13] leaver→ระงับ+คงเหลือหยุด', c_fn16),
    ('E17', '[FN-17 · S-14] payment display-only จากปลายทาง', c_fn17),
    ('E18', '[FN-18 · S-15] joiner→สิทธิ์เปิดอัตโนมัติ', c_fn18),
    ('E19', '[FN-19 · S-16] รายงานตามประเภท/กลุ่ม/ช่วงเวลา + filter', c_fn19),
    ('E90', '[FN-90] ค้นหา/filter + empty state', c_fn90),
    ('E91', '[FN-91] confirm gate + soft archive', c_fn91),
    ('E92', '[FN-92] validate บังคับ + กัน double-submit', c_fn92),
    ('E93', '[FN-93] audit append-only', c_fn93),
    ('E94', '[FN-94] mask RESTRICTED ตาม role (demo strip)', c_fn94),
    ('NEG', '[NEG · unsupported ×5] ของห้ามมี — เรนเดอร์จริงแล้วไม่มี', c_unsupported),
    ('U01', '[UI-REG] modal เหนือ drawer (z)', c_modal_over_drawer),
    ('U02', '[UI] overlay stack สะอาด', c_overlay_stack),
    ('U03', '[UI] CSS var ครบ', c_static_css),
    ('U04', '[UI] affordance cursor:pointer', c_affordance),
    ('U05', '[UI] lucide icons ครบ', c_icons),
    ('U06', '[UI-REG] no NaN/undefined leak in drawers/tabs/modals', c_no_garbage_text),
    ('U07', '[DSP-02a] combobox reqEmp เลือกแล้วปิด (ไม่เด้งกางใหม่ · focus-restore)', c_combo_closes),
    ('U08', '[DSP-02b] DOA modal ไม่มี combobox กางเอง (trapFocus auto-open)', c_modal_no_autoopen),
    ('U09', '[UI-REG] person cell ชื่อ/ตำแหน่งไม่ชนบรรทัดเดียว (§C3.8)', c_person_cell_collision),
    ('B1', '[B1 · FN-13] doApprove precondition guard (FIX-01)', c_b1),
    ('B2', '[B2 · FN-08/FN-13] DOA advance ทีละขั้น (FIX-03)', c_b2),
    ('B3', '[B3/B8 · FN-10/FN-13] re-check เพดาน+archived ณ อนุมัติ (FIX-02)', c_b3),
    ('B4', '[B4 · FN-94] persona guard employee no-op + ปุ่มไม่ render (FIX-04)', c_b4),
    ('B5', '[B5 · FN-15] doCancelRequest status guard (FIX-05)', c_b5),
    ('B6', '[FIX-06 · FN-03] archive confirm แจ้งคำขอค้าง', c_archive_warn),
    ('B7', '[FIX-07 · c4] จ่ายประจำผ่านเงินเดือน surface (F065 hook)', c_payroll_surface),
    ('B8', '[FIX-08 · FN-08] person combobox avatar #102', c_person_combo_avatar),
    ('B9', '[FIX-09] joinDate ค.ศ. (ไม่มีปี 31xx)', c_joindate_century),
    ('R1', '[R1 · FN-13/FN-93 · OQ-WEL-01] กลับรายการ approved → reversed + คืนคงเหลือ + EC-reverse + clawback (append-only)', c_rev1),
    ('R2', '[R2 · FN-15 · OQ-WEL-01] doReverse บน non-approved → บล็อก', c_rev2),
    ('R3', '[R3 · FN-94 · OQ-WEL-01] employee doReverse no-op + ปุ่มไม่ render', c_rev3),
    ('R4', '[R4 · FN-15 · FIX-05/OQ-WEL-01] cancel vs reverse ขอบเขตไม่ทับกัน (FIX-05 intact)', c_rev4),
    ('EX', '[EX · FN-13 · OQ-WEL-03] balance tab exposure คำขอรออนุมัติอื่น (display-only)', c_exposure),
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

    # ── divisor summary: FN ครอบ NN/24 ──
    ALL_FN = ['FN-%02d' % i for i in range(1, 20)] + ['FN-90', 'FN-91', 'FN-92', 'FN-93', 'FN-94']
    covered = set()
    for _tid, nm, _st, _d in suite.results:
        for m in re.findall(r'FN-\d{2}', nm):
            covered.add(m)
    missing = [f for f in ALL_FN if f not in covered]
    print('=' * 74)
    print("FN ครอบ %d/24 · เคสรวม %d · ผ่าน %d/%d" % (len(covered & set(ALL_FN)), total, ok, total))
    if missing:
        print("  FN ที่ยังไม่มีเคส:", ', '.join(missing))
    else:
        print("  ครบทั้ง 24 FN (FN-01..19 + FN-90..94)")
    sys.exit(0 if ok == total and not suite.console_errors else 1)


if __name__ == '__main__':
    main()
