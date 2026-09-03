"""E2E · F-HR-RECRUIT (สรรหา) — WF-01 Step 5

รันไทม์ตัวเดียวที่ครอบทุก FN (21) + เคสเชิงลบ 5 ข้อ (unsupported) ที่เรนเดอร์จริงแล้ว
assert ว่า "ไม่มี" บนจอ.

ยึด helper ของ uikit เท่านั้น (ready/settle/after) — ไม่มี wait_for_timeout, ไม่มีตัวตรวจ UI ใหม่.
ขับหน้าจอผ่าน controller function จริงของไฟล์ (เหมือน pattern ของ e2e-picking) แล้ว assert
ทั้ง data model และข้อความที่เรนเดอร์บน DOM. reload หน้าใหม่ต่อเคส → DB (mock) reset = เคสอิสระต่อกัน.

รัน: .claude/venv/Scripts/python.exe outputs/F-HR-RECRUIT/_e2e/e2e-recruit.py [path/to/สรรหา.html]
"""
from pathlib import Path
import json
import sys

from playwright.sync_api import sync_playwright

OUTPUTS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(OUTPUTS / "_SHARED" / "_e2e"))
from uikit import Suite, ready, settle as shared_settle, after as shared_after, JS_MODAL_UNDER_DRAWER  # noqa: E402

HTML = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parents[1] / "สรรหา.html").resolve()
BASE = HTML.as_uri()

suite = Suite("F-HR-RECRUIT สรรหา")


def settle(page, timeout=1200):
    shared_settle(page, timeout=timeout)


def after(page, js, timeout=1200):
    return shared_after(page, js, timeout=timeout)


def open_(page):
    """เปิดหน้าใหม่ (reset DB mock) แล้วรอ render จริง"""
    ready(page, BASE, timeout=9000)
    page.wait_for_function(
        "() => { const p=document.getElementById('page-content'); return p && p.innerHTML.trim().length>0; }",
        timeout=9000,
    )


def ev(page, js):
    return page.evaluate(js)


def pc_text(page):
    return page.evaluate("() => document.getElementById('page-content').innerText")


# ═══════════════════════════════ FN CASES ═══════════════════════════════

def c_fn01(page):
    """[FN-01] เปิดอัตรา (ตำแหน่ง·จำนวน·ระดับ·ช่วงเงินเดือน·hiring manager)"""
    open_(page)
    n0 = ev(page, "() => DB.reqs.length")
    after(page, """() => { openReqCreate();
      RC.draft={position:'QA Engineer',dept:'เทคโนโลยีสารสนเทศ',count:2,grade:'G4',
                hiring_manager_id:'EMP-0012',manpower_ref:'MP-2569-IT-99',desc:'ทดสอบ'}; }""")
    after(page, "() => submitReq(false)")
    last = ev(page, "() => DB.reqs[DB.reqs.length-1]")
    assert ev(page, "() => DB.reqs.length") == n0 + 1, "ไม่ได้สร้างอัตราใหม่"
    assert last["position"] == "QA Engineer" and last["count"] == 2 and last["grade"] == "G4"
    assert last["hiring_manager_id"] == "EMP-0012" and str(last["code"]).startswith("REQ-")
    return f"สร้างอัตรา {last['code']} · band G4 · 2 อัตรา · HM EMP-0012"


def c_fn02(page):
    """[FN-02 · BR-08] เปิดอัตราแม้ยังไม่มีแผน Manpower → เตือนแต่ทำได้"""
    open_(page)
    after(page, """() => { openReqCreate();
      RC.draft={position:'นักวิเคราะห์',dept:'การเงิน',count:1,grade:'G3',
                hiring_manager_id:'EMP-0058',manpower_ref:'',desc:''}; }""")
    html = ev(page, "() => reqFormDrawer()")
    assert "ยังไม่ได้ระบุแผนอัตรากำลัง" in html, "ไม่มีคำเตือน Manpower บนฟอร์ม"
    n0 = ev(page, "() => DB.reqs.length")
    after(page, "() => submitReq(false)")
    last = ev(page, "() => DB.reqs[DB.reqs.length-1]")
    assert ev(page, "() => DB.reqs.length") == n0 + 1, "ไม่ยอมสร้างเมื่อไม่มี Manpower"
    assert last["manpower_ref"] is None, "manpower_ref ควรว่างแต่ยังสร้างได้"
    return "เตือน Manpower แต่เปิดอัตราได้ (manpower_ref=null)"


def c_fn08(page):
    """[FN-08 · BR-04] ส่งอนุมัติผ่าน DOA slot picker ตามตำแหน่ง — ไม่ hardcode"""
    open_(page)
    after(page, """() => { openReqCreate();
      RC.draft={position:'DevOps',dept:'เทคโนโลยีสารสนเทศ',count:1,grade:'G4',
                hiring_manager_id:'EMP-0012',manpower_ref:'MP',desc:''}; submitReq(false); }""")
    rid = ev(page, "() => DB.reqs[DB.reqs.length-1].id")
    after(page, f"() => reqSubmitApproval('{rid}')")
    mtext = ev(page, "() => document.querySelector('#modalBackdrop .modal').innerText")
    assert "DOA-REQ-OPEN-001" in mtext, "modal ไม่แสดง DOA entry"
    assert "ผู้จัดการสายงาน (Hiring Manager)" in mtext and "หัวหน้าฝ่ายสรรหา" in mtext, "ไม่มี slot ตามตำแหน่ง"
    assert ev(page, "() => !!document.getElementById('ss-input-slot_1') && !!document.getElementById('ss-input-slot_2')"), \
        "ไม่มีตัวเลือกผู้อนุมัติ (slot picker)"
    # ยังไม่ได้เลือก = ผู้อนุมัติว่าง (ไม่ hardcode)
    assert ev(page, "() => Object.keys(RC.draft.slots||{}).length===0"), "slot ถูก preset (ไม่ควร hardcode)"
    # ส่งทั้งที่ยังไม่เลือก → ต้องถูกบล็อก
    after(page, "() => submitDoa()")
    assert ev(page, f"() => getReq('{rid}').status") == "draft", "ส่งอนุมัติได้ทั้งที่ยังไม่เลือกผู้อนุมัติ"
    # เลือกผู้อนุมัติผ่าน picker จริง แล้วส่ง
    after(page, "() => { ssPick('slot_1',0); ssPick('slot_2',1); }")
    after(page, "() => submitDoa()")
    r = ev(page, f"() => getReq('{rid}')")
    assert r["status"] == "pending", "ส่งอนุมัติแล้วสถานะไม่เป็น pending"
    assert r["approval"]["steps"][0]["approver_id"] == "EMP-0012", "ผู้อนุมัติขั้น 1 ไม่ตรงที่เลือก"
    assert r["approval"]["steps"][1]["approver_id"] == "EMP-0031", "ผู้อนุมัติขั้น 2 ไม่ตรงที่เลือก"
    return "DOA picker: 2 slot เลือกคนเอง · ว่าง=บล็อก · ครบ=pending"


def c_fn16(page):
    """[FN-16 · BR-07] ปิดอัตรา (รับครบ/ยกเลิก)"""
    open_(page)
    after(page, "() => reqClose('REQ-1')")  # REQ-1 = open
    after(page, "() => rcConfirmYes()")
    assert ev(page, "() => getReq('REQ-1').status") == "closed", "ปิดอัตราแล้วสถานะไม่เป็น closed"
    return "ปิดอัตรา REQ-1 → closed"


def c_fn03_04(page):
    """[FN-03 · BR-06] เพิ่มผู้สมัคร + [FN-04 · BR-03] ผูกกับอัตรา (application)"""
    open_(page)
    n0 = ev(page, "() => DB.cands.length")
    after(page, """() => { openCandCreate();
      RC.draft={name:'ทดสอบ ระบบ',email:'newcand@example.com',phone:'0900000000',
                reqId:'REQ-1',consent:true,resume:''}; }""")
    after(page, "() => submitCand()")
    last = ev(page, "() => DB.cands[DB.cands.length-1]")
    assert ev(page, "() => DB.cands.length") == n0 + 1, "ไม่ได้เพิ่มผู้สมัคร"
    assert last["name"] == "ทดสอบ ระบบ" and last["consent"]["ok"] is True
    assert last["reqId"] == "REQ-1", "ไม่ได้ผูกกับอัตรา (application)"
    return f"เพิ่มผู้สมัคร {last['code']} · ผูก REQ-1"


def c_fn14(page):
    """[FN-14 · BR-10] ตรวจผู้สมัครซ้ำ/เคยสมัคร → เตือน (ไม่บล็อก)"""
    open_(page)
    after(page, """() => { openCandCreate();
      RC.draft={name:'ซ้ำ ทดสอบ',email:'thanawat.s@example.com',phone:'081-555-0142',
                reqId:null,consent:true,resume:''}; }""")
    html = ev(page, "() => candFormDrawer()")
    assert "พบผู้สมัครซ้ำ/เคยสมัคร" in html, "ไม่เตือนผู้สมัครซ้ำ"
    n0 = ev(page, "() => DB.cands.length")
    after(page, "() => submitCand()")
    assert ev(page, "() => DB.cands.length") == n0 + 1, "เตือนซ้ำแล้วต้องยังบันทึกได้ (ไม่บล็อก)"
    assert ev(page, "() => DB.cands[DB.cands.length-1].dup") is True
    return "เตือน duplicate (email ตรง) · บันทึกต่อได้"


def c_fn05(page):
    """[FN-05 · BR-02] consent gate — ไม่ยินยอม PDPA แล้วเลื่อนสถานะ/สร้าง offer ไม่ได้"""
    open_(page)
    # C1 = ยังไม่ยินยอม
    stage = ev(page, "() => { candMoveStage('C1',1); return getCand('C1').stage; }")
    settle(page)
    assert stage == "applied", "ไม่ยินยอมแต่เลื่อนสถานะได้"
    offer_html = ev(page, "() => candOffer(getCand('C1'))")
    assert "สร้างข้อเสนอไม่ได้" in offer_html, "ไม่ยินยอมแต่ยังเปิดสร้าง offer ได้"
    assess_html = ev(page, "() => candAssess(getCand('C1'))")
    assert "นัดสัมภาษณ์/ประเมินไม่ได้" in assess_html, "ไม่ยินยอมแต่ยังนัดสัมภาษณ์ได้"
    return "consent gate: บล็อกเลื่อนสถานะ + offer + สัมภาษณ์"


def c_fn06(page):
    """[FN-06 · BR-03] เลื่อนสถานะใน pipeline board"""
    open_(page)
    after(page, "() => candMoveStage('C2',1)")   # screening → interview
    assert ev(page, "() => getCand('C2').stage") == "interview", "เลื่อนไปข้างหน้าไม่ได้"
    after(page, "() => candMoveStage('C2',-1)")  # interview → screening
    assert ev(page, "() => getCand('C2').stage") == "screening", "เลื่อนถอยหลังไม่ได้"
    return "เลื่อน stage: screening↔interview"


def c_fn07(page):
    """[FN-07 · BR-03] นัดสัมภาษณ์ + แจ้งเตือน (NTF)"""
    open_(page)
    n0 = ev(page, "() => getCand('C3').interviews.length")
    after(page, """() => { openInterviewModal('C3');
      RC.draft.iv={date:'2026-10-05',time:'10:30',interviewer_id:'EMP-0044',loc:'ห้อง A · Meet'}; }""")
    after(page, "() => saveInterview()")
    c = ev(page, "() => getCand('C3')")
    assert len(c["interviews"]) == n0 + 1, "ไม่ได้นัดสัมภาษณ์"
    assert c["interviews"][-1]["interviewer_id"] == "EMP-0044"
    assert "แจ้งเตือน" in c["history"][0]["action"], "ไม่มี event แจ้งเตือน (NTF) ใน audit"
    return "นัดสัมภาษณ์ + audit ระบุแจ้งเตือน (NTF)"


def c_fn09(page):
    """[FN-09 · BR-03] scorecard (ต่อผู้สัมภาษณ์)"""
    open_(page)
    after(page, """() => { openInterviewModal('C3');
      RC.draft.iv={date:'2026-10-06',time:'09:00',interviewer_id:'EMP-0012',loc:''}; saveInterview(); }""")
    ivid = ev(page, "() => getCand('C3').interviews[getCand('C3').interviews.length-1].id")
    after(page, "() => { openCandView('C3'); setCandTab('assess'); }")
    after(page, f"() => pickScore('C3','{ivid}',4)")
    after(page, f"() => saveScore('C3','{ivid}')")
    iv = ev(page, f"() => getCand('C3').interviews.find(x=>x.id==='{ivid}')")
    assert iv["scorecard"] and iv["scorecard"]["score"] == 4, "บันทึก scorecard ไม่สำเร็จ"
    assert ev(page, "() => getCand('C3').score") == 4
    return "บันทึก scorecard 4/5"


def c_fn10(page):
    """[FN-10 · BR-04] offer + band resolve + เงินนอก band บังคับ out_of_range_reason"""
    open_(page)
    band = ev(page, "() => bandResolve('G4','2026-10-01')")
    assert band["min"] == 45000 and band["max"] == 85000 and band["version_id"], "band resolve ผิด"
    # เงินนอก band + ไม่ระบุเหตุผล → ต้องบล็อก (ไม่สร้าง offer)
    after(page, """() => { openCandView('C3'); RC.dctx.tab='offer';
      RC.draft.offer={grade:'G4',start:'2026-10-01',salary:'999999',reason:''}; }""")
    after(page, "() => submitOffer('C3')")
    assert ev(page, "() => getCand('C3').offer") is None, "เงินนอก band ไม่มีเหตุผล แต่สร้าง offer ได้"
    # เงินนอก band + มีเหตุผล → สร้างได้ พร้อม out_of_range_reason
    after(page, """() => { RC.draft.offer={grade:'G4',start:'2026-10-01',salary:'999999',
      reason:'ประสบการณ์สูงกว่ามาตรฐานระดับ'}; submitOffer('C3'); }""")
    after(page, "() => closeModal()")   # submitOffer เปิด DOA modal ต่อ
    o = ev(page, "() => getCand('C3').offer")
    assert o and o["out_of_range_reason"], "ไม่บังคับ out_of_range_reason"
    assert o["salary"] == 999999 and o["band"]["version_id"] and o["status"] == "pending"
    # เงินใน band → ไม่ต้องมีเหตุผล
    after(page, """() => { openCandView('C2'); RC.dctx.tab='offer';
      RC.draft.offer={grade:'G4',start:'2026-10-01',salary:'60000',reason:''}; submitOffer('C2'); }""")
    after(page, "() => closeModal()")
    o2 = ev(page, "() => getCand('C2').offer")
    assert o2 and o2["out_of_range_reason"] is None and o2["status"] == "pending", "เงินใน band แต่ยังบังคับเหตุผล"
    return "band resolve OK · นอก band บังคับเหตุผล · ใน band ไม่บังคับ"


def c_fn11(page):
    """[FN-11 · BR-05] hired → handoff On/Offboard + assert ไม่มีการสร้าง employee"""
    open_(page)
    emp0 = ev(page, "() => EMPLOYEES.length")
    after(page, "() => offerResult('C4','accepted')")   # C4 offer sent → accepted
    after(page, "() => candHireHandoff('C4')")           # เปิด confirm modal
    body = ev(page, "() => RC.mctx.data.body")
    assert "ไม่สร้าง employee" in body, "ข้อความ handoff ไม่ยืนยันว่าไม่สร้าง employee"
    after(page, "() => rcConfirmYes()")
    c = ev(page, "() => getCand('C4')")
    assert c["stage"] == "hired" and c["onboardSent"] is True, "handoff ไม่สำเร็จ"
    assert ev(page, "() => EMPLOYEES.length") == emp0, "มีการสร้าง employee (ต้องไม่มี)"
    assert "On/Offboard" in c["history"][0]["action"] and "soft-linkage" in c["history"][0]["detail"], \
        "audit ไม่ระบุ handoff แบบ soft-linkage"
    return "hired → ยิง event On/Offboard · EMPLOYEES ไม่เพิ่ม (ไม่สร้างพนักงาน)"


def c_fn12(page):
    """[FN-12 · BR-07] ผู้สมัครปฏิเสธ/ถอนตัว (บันทึกเหตุ)"""
    open_(page)
    after(page, "() => candTerminate('C1')")
    after(page, "() => { RC.draft.reasonKind='withdrawn'; RC.draft.reason='ผู้สมัครขอถอนตัว'; rcReasonYes(); }")
    c = ev(page, "() => getCand('C1')")
    assert c["stage"] == "withdrawn", "ไม่ได้บันทึกถอนตัว"
    assert c["reason"] == "ผู้สมัครขอถอนตัว"
    return "ถอนตัว + บันทึกเหตุ"


def c_fn13(page):
    """[FN-13 · BR-07] ไม่ผ่าน → เก็บ talent pool (บันทึกเหตุ)"""
    open_(page)
    after(page, "() => candTerminate('C2')")
    after(page, "() => { RC.draft.reasonKind='talent_pool'; RC.draft.reason='ประสบการณ์ยังไม่ตรง'; rcReasonYes(); }")
    c = ev(page, "() => getCand('C2')")
    assert c["stage"] == "talent_pool", "ไม่ได้เก็บเข้า talent pool"
    return "ไม่ผ่าน → talent pool + เหตุ"


def c_fn15(page):
    """[FN-15 · BR-06] รายงาน funnel/time-to-hire + filter"""
    open_(page)
    after(page, "() => navigate('recruit/report')")
    # ใช้ textContent (ไม่ใช่ innerText ที่ตกข้อความ .sec-h บางตัว) + เช็ค DOM ของ funnel จริง
    tc = ev(page, "() => document.getElementById('page-content').textContent")
    assert "Funnel การสรรหา" in tc and "ผู้สมัครทั้งหมด" in tc, "หน้ารายงาน funnel ไม่ครบ"
    assert ev(page, "() => document.querySelectorAll('.funnel-row').length") > 0, "funnel ไม่มีแถว stage"
    counts = ev(page, "() => ({all: DB.cands.length, one: DB.cands.filter(c=>c.reqId==='REQ-3').length})")
    assert counts["all"] > counts["one"] and counts["one"] >= 1, "ข้อมูล filter ไม่สมเหตุผล"
    after(page, "() => { RC.f.report.req='REQ-3'; renderPageOnly(); }")
    assert ev(page, "() => !!document.querySelector('.funnel') && document.getElementById('page-content').textContent.includes('Funnel การสรรหา')"), "filter แล้ว funnel หาย"
    return f"funnel + filter (all={counts['all']} · REQ-3={counts['one']})"


def c_fn90(page):
    """[FN-90] ค้นหา/filter list + empty state"""
    open_(page)
    after(page, "() => navigate('recruit/pool')")
    after(page, "() => { RC.f.pool={q:'zzzz_ไม่มีจริง',stage:'all'}; renderPageOnly(); }")
    assert "ไม่พบผู้สมัคร" in pc_text(page), "ค้นไม่เจอแต่ไม่ขึ้น empty state"
    after(page, "() => { RC.f.pool={q:'ธน',stage:'all'}; renderPageOnly(); }")
    pc2 = pc_text(page)
    assert "ธนวัฒน์" in pc2 and "ไม่พบผู้สมัคร" not in pc2, "ค้นเจอแต่ไม่แสดงผล"
    return "search: เจอ/ไม่เจอ + empty state"


def c_fn91(page):
    """[FN-91] ปิด/ยกเลิกผ่าน confirm + soft archive"""
    open_(page)
    after(page, "() => reqClose('REQ-2')")          # approved → เปิด confirm
    body = ev(page, "() => RC.mctx.data.body")
    assert "soft archive" in body, "confirm ปิดอัตราไม่ระบุ soft archive"
    after(page, "() => closeModal()")               # ยกเลิก → confirm gate
    assert ev(page, "() => getReq('REQ-2').status") == "approved", "ยกเลิก confirm แล้วยังปิดอัตรา (gate พัง)"
    after(page, "() => reqClose('REQ-2')")
    h0 = ev(page, "() => getReq('REQ-2').history.length")
    after(page, "() => rcConfirmYes()")
    assert ev(page, "() => getReq('REQ-2').status") == "closed", "confirm แล้วไม่ปิด"
    assert ev(page, "() => DB.reqs.some(x=>x.id==='REQ-2')") is True, "soft archive แต่ record หาย"
    assert ev(page, "() => getReq('REQ-2').history.length") >= h0 + 1, "ประวัติไม่ถูกเก็บต่อ (soft archive)"
    return "confirm gate + soft archive (record + history คงอยู่)"


def c_fn92(page):
    """[FN-92] field บังคับ validate + กัน double-submit"""
    open_(page)
    n0 = ev(page, "() => DB.reqs.length")
    after(page, """() => { openReqCreate();
      RC.draft={position:'',dept:'',count:1,grade:'G3',hiring_manager_id:null,manpower_ref:'',desc:''}; }""")
    after(page, "() => submitReq(false)")
    assert ev(page, "() => DB.reqs.length") == n0, "ฟอร์มว่างแต่บันทึกได้ (validate พัง)"
    # double-submit guard: busy=true ต้องไม่บันทึก
    after(page, """() => { RC.draft={position:'X',dept:'Y',count:1,grade:'G3',
      hiring_manager_id:'EMP-0012',manpower_ref:'',desc:''}; RC.busy=true; }""")
    after(page, "() => submitReq(false)")
    assert ev(page, "() => DB.reqs.length") == n0, "busy=true แต่ยังบันทึก (double-submit guard พัง)"
    after(page, "() => { RC.busy=false; }")
    return "validate ฟอร์มว่าง + guard busy"


def c_fn93(page):
    """[FN-93] audit append-only (create/แก้/เลื่อน/อนุมัติ)"""
    open_(page)
    before = ev(page, "() => ({len:getReq('REQ-1').history.length, top:getReq('REQ-1').history[0].action})")
    after(page, "() => reqClose('REQ-1')")
    after(page, "() => rcConfirmYes()")
    h = ev(page, "() => getReq('REQ-1').history")
    assert len(h) == before["len"] + 1, "audit ไม่ได้ append (จำนวนไม่เพิ่มทีละ 1)"
    assert h[0]["action"] == "ปิดอัตรา", "รายการล่าสุดไม่ใช่ action ที่เพิ่งทำ"
    assert h[1]["action"] == before["top"], "รายการเก่าถูกแก้/หาย (ไม่ append-only)"
    return "audit append-only: unshift ใหม่ · ของเก่าคงเดิม"


def c_fn94(page):
    """[FN-94 · BR-06] mask ข้อมูลผู้สมัคร RESTRICTED ตาม role"""
    open_(page)
    masked = ev(page, "() => { RC.persona='viewer'; return candDetail(getCand('C4'), reqOfCand(getCand('C4'))); }")
    assert "•••" in masked and "araya.p@example.com" not in masked, "role viewer แต่ไม่ปิดบังอีเมล"
    assert "RESTRICTED" in masked, "ไม่มีป้าย RESTRICTED"
    full = ev(page, "() => { RC.persona='recruiter'; return candDetail(getCand('C4'), reqOfCand(getCand('C4'))); }")
    assert "araya.p@example.com" in full, "role ที่เห็นได้ กลับถูกปิดบัง"
    return "mask ตาม role: viewer=ปิดบัง · recruiter=เห็นเต็ม"


# ═══════════════════════ NEGATIVE (unsupported ×5, rendered → absent) ═══════════════════════

def c_unsupported(page):
    """[NEG] เคสเชิงลบ — เรนเดอร์จริงแล้ว assert ว่า 'ไม่มี' บนจอ (unsupported 5 ข้อ)"""
    open_(page)
    surfaces = ev(page, """() => {
      const parts=[];
      ['req','pool','board','report'].forEach(t=>{ RC.tab=t; parts.push(renderPage()); });
      RC.dctx={kind:'req',mode:'create',id:null};
      RC.draft={position:'',dept:'',count:1,grade:'G3',hiring_manager_id:null,manpower_ref:'',desc:''};
      parts.push(reqFormDrawer());
      parts.push(candFormDrawer());
      return parts.join('\\n');
    }""")
    offer_txt = ev(page, "() => candOffer(getCand('C4')) + '\\n' + candOffer(getCand('C5'))")
    reqform = ev(page, """() => { RC.dctx={kind:'req',mode:'create',id:null};
      RC.draft={position:'',dept:'',count:1,grade:'G3',hiring_manager_id:null,manpower_ref:'',desc:''};
      return reqFormDrawer(); }""")

    # 1) ไม่มีทาง "จ้างจริง/สร้าง employee/สัญญาจ้าง"
    for tok in ["สัญญาจ้าง", "จ้างจริง", "สร้างพนักงาน", "บันทึกเป็นพนักงาน", "ทะเบียนพนักงาน"]:
        assert tok not in surfaces, f"[neg1] พบ affordance สร้าง employee/สัญญา: {tok}"
    # 2) ไม่มี "ประกาศ job board ภายนอก"
    for tok in ["job board", "ประกาศงานภายนอก", "โพสต์ประกาศ", "เว็บหางาน", "JobsDB", "LinkedIn"]:
        assert tok not in surfaces, f"[neg2] พบการประกาศงานภายนอก: {tok}"
    # 3) ไม่มี "assessment/แบบทดสอบ/sourcing agency"
    for tok in ["assessment", "แบบทดสอบ", "ข้อสอบ", "sourcing", "บริษัทจัดหา", "จัดหางาน"]:
        assert tok not in surfaces, f"[neg3] พบ assessment/sourcing: {tok}"
    # 4) ไม่มี "offer letter เลขรัน/พิมพ์เอกสารมีเลขที่" (บนจอ offer)
    for tok in ["offer letter", "พิมพ์", "เลขที่เอกสาร", "เลขที่ข้อเสนอ", "เลขรัน", "ออกเอกสาร", "running number"]:
        assert tok not in offer_txt, f"[neg4] พบ offer letter/เลขรัน/พิมพ์: {tok}"
    # 5) ไม่มี "สร้าง/แก้ ระดับ-band" (band = read-only select เท่านั้น)
    assert "อ่านจาก HR Configuration" in reqform, "[neg5] band ควรเป็น read-only ref HR Configuration"
    for tok in ["สร้างระดับ", "เพิ่มระดับ", "แก้ไข band", "จัดการ band", "สร้าง band", "ตั้งค่า band", "แก้ไขระดับเงินเดือน"]:
        assert tok not in surfaces, f"[neg5] พบการสร้าง/แก้ band: {tok}"
    return "unsupported 5 ข้อ assert absent (employee/สัญญา · job board · assessment · offer-letter/เลขรัน · สร้าง band)"


def c_modal_z(page):
    """[UI-REG] modal เปิดจากในลิ้นชักต้องอยู่เหนือ drawer (z) — regression F-HR-RECRUIT 2026-09-02 (bug: modal โดน drawer ทับทุกอัน)"""
    open_(page)
    after(page, "() => { openCandView('C3'); }")
    after(page, "() => { openInterviewModal('C3'); }")
    viol = ev(page, JS_MODAL_UNDER_DRAWER)
    assert viol == [], f"modal จมใต้ drawer: {viol}"
    mz = ev(page, "() => parseInt(getComputedStyle(document.querySelector('.modal-backdrop')).zIndex,10)")
    dz = ev(page, "() => parseInt(getComputedStyle(document.querySelector('.drawer')).zIndex,10)")
    assert mz > dz, f"modal z({mz}) ต้อง > drawer z({dz})"
    return f"modal เหนือ drawer (modal z={mz} > drawer z={dz})"


def c_fix01_board_hire(page):
    """[FIX-01] บอร์ด: ห้ามข้ามไป hired ก่อน offer accepted · accepted แล้วต้อง route ผ่าน candHireHandoff"""
    open_(page)
    assert ev(page, "() => getCand('C4').offer.status") == "sent"
    after(page, "() => candMoveStage('C4',1)")
    assert ev(page, "() => getCand('C4').stage") == "offer", "ข้ามไป hired ได้ทั้งที่ยังไม่ตอบรับ offer (FIX-01)"
    after(page, "() => offerResult('C4','accepted')")
    emp0 = ev(page, "() => EMPLOYEES.length")
    after(page, "() => candMoveStage('C4',1)")
    assert ev(page, "() => RC.mctx.type") == "confirm", "board hire ไม่ route ผ่าน candHireHandoff (ไม่มี confirm)"
    after(page, "() => rcConfirmYes()")
    c = ev(page, "() => getCand('C4')")
    assert c["stage"] == "hired" and c["onboardSent"] is True, "board hire ไม่สำเร็จผ่าน handoff"
    assert ev(page, "() => EMPLOYEES.length") == emp0, "board hire สร้าง employee (ต้องไม่มี)"
    return "board→hired ผ่าน candHireHandoff เท่านั้น · บล็อกเมื่อ offer ยังไม่ตอบรับ"


def c_fix02_viewer_ro(page):
    """[FIX-02] persona ผู้ชมทั่วไป = อ่านอย่างเดียว · ปุ่มสร้างไม่แสดง + mutation ถูกบล็อก"""
    open_(page)
    after(page, "() => setPersona('viewer')")
    after(page, "() => navigate('recruit/req')")
    assert ev(page, "() => document.querySelectorAll('.ph-actions button').length") == 0, "viewer ยังเห็นปุ่ม action บนแท็บ req"
    after(page, "() => navigate('recruit/pool')")
    assert ev(page, "() => document.querySelectorAll('.ph-actions button').length") == 0, "viewer ยังเห็นปุ่ม action บนแท็บ pool"
    n0 = ev(page, "() => DB.reqs.length")
    after(page, "() => { RC.draft={position:'x',dept:'y',count:1,grade:'G3',hiring_manager_id:'EMP-0012',manpower_ref:'',desc:''}; submitReq(false); }")
    assert ev(page, "() => DB.reqs.length") == n0, "viewer submitReq สร้างได้ (ต้องถูกบล็อก)"
    m0 = ev(page, "() => DB.cands.length")
    after(page, "() => { RC.draft={name:'z',email:'z@z.com',phone:'0800000000',reqId:null,consent:true,resume:''}; submitCand(); }")
    assert ev(page, "() => DB.cands.length") == m0, "viewer submitCand สร้างได้ (ต้องถูกบล็อก)"
    return "viewer: ปุ่มสร้างไม่แสดง + submitReq/submitCand ถูกบล็อก"


CASES = [
    ("FN-01", "เปิดอัตรา", c_fn01),
    ("FN-02", "เปิดอัตราไม่มี Manpower (เตือน)", c_fn02),
    ("FN-08", "DOA slot picker (ไม่ hardcode)", c_fn08),
    ("FN-16", "ปิดอัตรา", c_fn16),
    ("FN-03 FN-04", "เพิ่มผู้สมัคร + ผูก application", c_fn03_04),
    ("FN-14", "duplicate เตือน", c_fn14),
    ("FN-05", "consent gate (PDPA)", c_fn05),
    ("FN-06", "เลื่อน stage board", c_fn06),
    ("FN-07", "นัดสัมภาษณ์ + NTF", c_fn07),
    ("FN-09", "scorecard", c_fn09),
    ("FN-10", "offer + band resolve + out_of_range", c_fn10),
    ("FN-11", "hired→handoff · ไม่สร้าง employee", c_fn11),
    ("FN-12", "ปฏิเสธ/ถอนตัว", c_fn12),
    ("FN-13", "ไม่ผ่าน→talent pool", c_fn13),
    ("FN-15", "report funnel + filter", c_fn15),
    ("FN-90", "search / empty", c_fn90),
    ("FN-91", "confirm + soft archive", c_fn91),
    ("FN-92", "validate + double-submit", c_fn92),
    ("FN-93", "audit append-only", c_fn93),
    ("FN-94", "mask RESTRICTED ตาม role", c_fn94),
    ("NEG-UNSUP", "เคสเชิงลบ unsupported ×5", c_unsupported),
    ("UI-REG", "modal เหนือ drawer (z)", c_modal_z),
    ("FIX-01", "board→hired ผ่าน handoff เท่านั้น", c_fix01_board_hire),
    ("FIX-02", "viewer read-only", c_fix02_viewer_ro),
]

FN_TOTAL = 21

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 950})
    page.set_default_timeout(6000)
    page.route("https://**", lambda route: route.abort())
    suite.watch(page)
    for ids, name, fn in CASES:
        print(f"RUN  {ids} — {name}", flush=True)
        suite.check(ids, name, lambda fn=fn: fn(page))
        print(f"DONE {ids} — {suite.results[-1][2]}", flush=True)
        if suite.results[-1][3]:
            print(f"     {suite.results[-1][3]}", flush=True)
    browser.close()

passed = sum(1 for row in suite.results if row[2] == "PASS")
covered = sorted({tok for ids, _, _ in CASES for tok in ids.split() if tok.startswith("FN-")})
result = {
    "feature": "F-HR-RECRUIT",
    "fn_covered": len(covered),
    "fn_total": FN_TOTAL,
    "fn_covered_list": covered,
    "negative_unsupported": 5,
    "tests_passed": passed,
    "tests_total": len(CASES),
    "console_errors": suite.console_errors,
    "results": [{"ids": r[0], "name": r[1], "status": r[2], "detail": r[3]} for r in suite.results],
}
(Path(__file__).parent / "results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

print("=" * 74)
missing = [f"FN-{str(i).zfill(2)}" for i in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16] if f"FN-{str(i).zfill(2)}" not in covered]
print(f"FN ครอบ {len(covered)}/{FN_TOTAL} · เคสรวม {len(CASES)} · ผ่าน {passed}/{len(CASES)} · เคสเชิงลบ unsupported 5/5")
if len(covered) != FN_TOTAL:
    print(f"  ⚠️ FN ที่ยังขาด: {sorted(set(['FN-01','FN-02','FN-03','FN-04','FN-05','FN-06','FN-07','FN-08','FN-09','FN-10','FN-11','FN-12','FN-13','FN-14','FN-15','FN-16','FN-90','FN-91','FN-92','FN-93','FN-94']) - set(covered))}")
suite.report(exit_on_fail=False)
sys.exit(0 if passed == len(CASES) and not suite.console_errors else 1)
