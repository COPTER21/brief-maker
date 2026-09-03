"""E2E · F-HR-TRAIN (อบรม / Training) — WF-01 Step 5

รันไทม์ตัวเดียวที่ครอบทุก FN (18) + เคสเชิงลบ 5 ข้อ (unsupported[]) ที่เรนเดอร์จริงแล้ว
assert ว่า "ไม่มี" affordance บนจอ.

ยึด helper ของ uikit เท่านั้น (ready/settle/after) — ไม่มี wait_for_timeout, ไม่มีตัวตรวจ UI ใหม่.
ขับหน้าจอผ่าน controller function จริงของไฟล์ แล้ว assert ทั้ง data model และข้อความที่เรนเดอร์บน DOM.
reload หน้าใหม่ต่อเคส → DB (mock) reset = เคสอิสระต่อกัน.

รัน: .claude/venv/Scripts/python.exe outputs/F-HR-TRAIN/_e2e/e2e-train.py [path/to/อบรม.html]
"""
from pathlib import Path
import json
import sys

from playwright.sync_api import sync_playwright

OUTPUTS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(OUTPUTS / "_SHARED" / "_e2e"))
from uikit import (  # noqa: E402
    Suite, ready, settle as shared_settle, after as shared_after,
    unrendered_visible_icons,
    nested_cards, combobox_state_after_select, assert_combobox_closes_after_select,
    modal_autoopens_comboboxes,
    JS_MODAL_UNDER_DRAWER, JS_AFFORDANCE, JS_CSSVAR, JS_LAYOUT, JS_OVERLAY_STACK,
)

HTML = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parents[1] / "อบรม.html").resolve()
BASE = HTML.as_uri()

suite = Suite("F-HR-TRAIN อบรม")


def settle(page, timeout=1200):
    shared_settle(page, timeout=timeout)


def after(page, js, timeout=1400):
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
    return page.evaluate("() => document.getElementById('page-content').textContent")


# ═══════════════════════════════ FN CASES ═══════════════════════════════

def c_fn01(page):
    """[FN-01] สร้างหลักสูตร (มีค่าใช้จ่าย + งบ) → เผยแพร่"""
    open_(page)
    n0 = ev(page, "() => DB.courses.length")
    after(page, """() => { openCourseCreate();
      TC.draft={name:'อบรมทดสอบระบบ (QA)',category:'safety',instructor:'ทีม QA',
                duration:'1 วัน (6 ชม.)',has_cost:true,budget:'12000',desc:'ทดสอบ'}; }""")
    after(page, "() => submitCourse(false)")
    last = ev(page, "() => DB.courses[DB.courses.length-1]")
    assert ev(page, "() => DB.courses.length") == n0 + 1, "ไม่ได้สร้างหลักสูตรใหม่"
    assert last["name"] == "อบรมทดสอบระบบ (QA)" and last["has_cost"] is True and last["budget"] == 12000
    assert last["status"] == "published" and str(last["code"]).startswith("CRS-")
    return f"สร้างหลักสูตร {last['code']} · has_cost · งบ 12,000 · published"


def c_fn02(page):
    """[FN-02] สร้างรอบอบรม (ร่าง) แล้วเปิดรับสมัคร"""
    open_(page)
    n0 = ev(page, "() => DB.sessions.length")
    after(page, """() => { openSessionCreate();
      TC.draft={courseId:'CO3',start:'2026-11-01',end:'2026-11-01',time:'09:00–16:00',
                location:'ห้อง QA',capacity:10}; }""")
    after(page, "() => submitSession()")
    sid = ev(page, "() => DB.sessions[DB.sessions.length-1].id")
    assert ev(page, "() => DB.sessions.length") == n0 + 1, "ไม่ได้สร้างรอบอบรม"
    assert ev(page, f"() => getSession('{sid}').status") == "draft", "รอบใหม่ควรเป็นร่างก่อน"
    after(page, f"() => sessionOpen('{sid}')")
    assert ev(page, f"() => getSession('{sid}').status") == "open", "เปิดรับสมัครแล้วสถานะไม่เป็น open"
    return f"สร้างรอบ + เปิดรับ ({sid} → open)"


def c_fn03(page):
    """[FN-03] ลงทะเบียนเกินจำนวนรับ → block (capacity guard)"""
    open_(page)
    after(page, """() => { openSessionCreate();
      TC.draft={courseId:'CO3',start:'2026-11-02',end:'2026-11-02',time:'09:00–16:00',
                location:'ห้องเล็ก',capacity:1}; }""")
    after(page, "() => submitSession()")
    sid = ev(page, "() => DB.sessions[DB.sessions.length-1].id")
    after(page, f"() => sessionOpen('{sid}')")
    # ลงคนแรก (ฟรี → confirmed) จนเต็ม (cap=1)
    after(page, f"() => {{ openEnrollModal('{sid}'); TC.draft.enr.emp_id='EMP-01'; submitEnroll(); }}")
    assert ev(page, f"() => activeEnrolls('{sid}').length") == 1, "คนแรกลงไม่สำเร็จ"
    assert ev(page, f"() => activeEnrolls('{sid}')[0].status") == "confirmed", "หลักสูตรฟรีควร confirmed ทันที"
    # เปิด modal ตอนเต็ม → ต้องถูกบล็อก (modal ไม่เปิด)
    after(page, f"() => openEnrollModal('{sid}')")
    assert ev(page, "() => state.modal.open") is False, "จำนวนเต็มแต่ยังเปิด modal ลงทะเบียนได้"
    # submitEnroll ตรง ๆ ตอนเต็ม → guard กันไม่ให้เพิ่ม
    n0 = ev(page, "() => DB.enrolls.length")
    after(page, f"() => {{ TC.draft.enr={{sid:'{sid}',emp_id:'EMP-02',source:'manual',gap_ref:null}}; submitEnroll(); }}")
    assert ev(page, "() => DB.enrolls.length") == n0, "capacity guard พัง — ลงเกินจำนวนรับได้"
    return "capacity guard: เต็ม→ปิด modal + submitEnroll ไม่เพิ่ม"


def c_fn04_08(page):
    """[FN-04] has_cost → pending_doa ก่อน confirmed · [FN-08] DOA slot picker เลือกคน (ไม่ hardcode)"""
    open_(page)
    # ลงทะเบียนหลักสูตรมีค่าใช้จ่าย (SE1/CO1) → ต้องเข้าสาย DOA
    after(page, "() => { openEnrollModal('SE1'); TC.draft.enr.emp_id='EMP-03'; submitEnroll(); }")
    eid = ev(page, "() => DB.enrolls[DB.enrolls.length-1].id")
    assert ev(page, f"() => getEnroll('{eid}').status") == "pending_doa", \
        "[FN-04] has_cost แต่ไม่เข้า pending_doa (ต้องรออนุมัติก่อน confirmed)"
    assert ev(page, f"() => getEnroll('{eid}').status") != "confirmed"
    # DOA modal เปิดต่อ (chained) — slot picker
    assert ev(page, "() => state.modal.open && TC.mctx.type==='doa'"), "ไม่เปิด DOA modal ต่อ"
    assert ev(page, "() => 'DOA-TRAIN-ENROLL-001'===TC.mctx.data.entry"), "DOA entry ผิด"
    # ยังไม่เลือก = ไม่ hardcode
    assert ev(page, "() => Object.keys(TC.draft.slots||{}).length===0"), "[FN-08] slot ถูก preset (hardcode)"
    assert ev(page, "() => !!document.getElementById('ss-input-slot_1') && !!document.getElementById('ss-input-slot_2')"), \
        "ไม่มีช่องเลือกผู้อนุมัติ 2 ขั้น"
    # option = คนจริง (มีชื่อ + ตำแหน่ง/แผนกใน sub)
    optok = ev(page, """() => { const s=window.__ss['slot_1'];
      return s && s.options.length>=5 && s.options.every(o=>o.label && o.sub && o.icon==='user'); }""")
    assert optok, "[FN-08] slot picker ไม่ใช่รายชื่อคนจริง (ขาดชื่อ/ตำแหน่ง)"
    # ส่งทั้งที่ยังไม่เลือก → บล็อก (approval ยังไม่ผูก)
    after(page, "() => submitDoa()")
    assert ev(page, f"() => getEnroll('{eid}').approval") is None, "ส่ง DOA ได้ทั้งที่ยังไม่เลือกผู้อนุมัติ"
    # เลือกผู้อนุมัติผ่าน picker จริง (idx0=EMP-01, idx1=EMP-02) แล้วส่ง
    after(page, "() => { ssPick('slot_1',0); ssPick('slot_2',1); }")
    after(page, "() => submitDoa()")
    ap = ev(page, f"() => getEnroll('{eid}').approval")
    assert ap and ap["steps"][0]["approver_id"] == "EMP-01" and ap["steps"][1]["approver_id"] == "EMP-02", \
        "ผู้อนุมัติที่บันทึกไม่ตรงกับที่เลือก (hardcode?)"
    assert ev(page, f"() => getEnroll('{eid}').status") == "pending_doa"
    return "has_cost→pending_doa · DOA picker 2 ขั้น เลือกคนเอง · ว่าง=บล็อก · ผูกตามที่เลือก"


def c_fn05(page):
    """[FN-05] no-cost → ยืนยันทันที (ข้าม DOA)"""
    open_(page)
    # SE2/CO3 = ฟรี · เพิ่มผู้เรียนใหม่ (EMP-01 ยังไม่อยู่ใน SE2)
    n0 = ev(page, "() => DB.enrolls.length")
    after(page, "() => { openEnrollModal('SE2'); TC.draft.enr.emp_id='EMP-01'; submitEnroll(); }")
    assert ev(page, "() => DB.enrolls.length") == n0 + 1
    last = ev(page, "() => DB.enrolls[DB.enrolls.length-1]")
    assert last["status"] == "confirmed", "หลักสูตรฟรีแต่ไม่ confirmed ทันที"
    assert last["approval"] is None, "หลักสูตรฟรีไม่ควรมีสายอนุมัติ (ไม่เข้า DOA)"
    assert ev(page, "() => state.modal.open") is False, "ฟรี = ไม่ควรเปิด DOA modal"
    return "no-cost → confirmed ทันที · ไม่มี approval · ข้าม DOA"


def c_fn06(page):
    """[FN-06] บันทึกผล ผ่าน/ไม่ผ่าน"""
    open_(page)
    # EN5, EN6 = confirmed (SE2/CO3 ฟรี · SE2 ปิดรอบแล้ว) → FIX-03: เช็คชื่อเข้าก่อนบันทึกผล
    after(page, "() => { setAttendance('EN5',true); openResultModal('EN5'); pickResult('pass'); submitResult(); }")
    assert ev(page, "() => getEnroll('EN5').result") == "pass" and ev(page, "() => getEnroll('EN5').status") == "passed"
    after(page, "() => { setAttendance('EN6',true); openResultModal('EN6'); pickResult('fail'); submitResult(); }")
    assert ev(page, "() => getEnroll('EN6').result") == "fail" and ev(page, "() => getEnroll('EN6').status") == "failed"
    return "บันทึกผล: EN5 ผ่าน · EN6 ไม่ผ่าน (เช็คชื่อเข้าก่อน · รอบ closed)"


def c_fn07(page):
    """[FN-07] ออกใบรับรอง soft ref (ไม่มีเลขรัน / ไม่ออก PDF ทางการ)"""
    open_(page)
    after(page, "() => { setAttendance('EN5',true); openResultModal('EN5'); pickResult('pass'); submitResult(); }")
    after(page, "() => issueCert('EN5')")
    body = ev(page, "() => TC.mctx.data.body")
    assert "soft ref" in body and "ไม่มีเลขรัน" in body, "ยืนยันออกใบรับรองไม่ระบุ soft ref / ไม่มีเลขรัน"
    after(page, "() => tcConfirmYes()")
    cert = ev(page, "() => getEnroll('EN5').cert")
    assert cert and str(cert["id"]).startswith("CERT-REF-"), "cert ไม่ใช่ soft ref (CERT-REF-)"
    assert "soft ref" in cert["note"], "cert ไม่ระบุ soft ref"
    return f"ออกใบรับรอง soft ref {cert['id']} (ไม่มีเลขรันทางการ)"


def c_fn09(page):
    """[FN-09] ค่าอบรม → Expense Claim display-only + EC ref (ไม่ hardcode ตัวเลข Rate Card)"""
    open_(page)
    # อนุมัติ EN1 (pending_doa · approver EMP-07/EMP-06) จนครบ → confirmed
    after(page, "() => setPersona('manager')")
    after(page, "() => enrollApprove('EN1')")
    after(page, "() => enrollApprove('EN1')")
    assert ev(page, "() => getEnroll('EN1').status") == "confirmed", "อนุมัติครบแล้วไม่ confirmed"
    # ส่ง Expense Claim (hook display-only)
    assert ev(page, "() => getEnroll('EN1').expenseSent") is False
    after(page, "() => sendExpense('EN1')")
    e = ev(page, "() => getEnroll('EN1')")
    assert e["expenseSent"] is True, "ไม่ได้ยิง hook Expense Claim"
    assert "display-only" in e["history"][0]["detail"] and "ไม่จ่าย" in e["history"][0]["detail"], \
        "audit ไม่ยืนยันว่า display-only / ไม่จ่าย/ไม่ post"
    # EC ref display-only + ไม่ hardcode ตัวเลข
    apr = ev(page, "() => sessionApproval(getSession('SE1'),courseOf(getSession('SE1')))")
    assert "อ้างอิง Rate Card" in apr and "ยังไม่ผูกตัวเลข" in apr, "EC ไม่ได้เป็น display-only (อาจ hardcode ตัวเลข)"
    return "อนุมัติครบ→confirmed · Expense=hook display-only (ไม่จ่าย/ไม่ post) · EC ref ไม่ hardcode"


def c_fn10(page):
    """[FN-10] gap จาก Performance → แนะนำผู้เรียน (hook display-only · อ่านอย่างเดียว)"""
    open_(page)
    after(page, "() => openEnrollModal('SE1')")  # CO1 มี gap EMP-01
    # textContent (ไม่ใช่ innerText — .sec-h มี text-transform:uppercase จะทำให้ 'gap'→'GAP')
    m = ev(page, "() => document.querySelector('#modalBackdrop .modal').textContent")
    assert "แนะนำจากผลประเมิน" in m, "ไม่มีบล็อกแนะนำจาก gap"
    assert "hook display-only" in m and "PERF-2569-0221" in m, "gap ไม่ระบุ hook display-only / perf_ref"
    # เลือกจาก gap → source=gap (อ่านมา ไม่สร้าง gap เอง)
    after(page, "() => pickGap('EMP-01','PERF-2569-0221')")
    en = ev(page, "() => TC.draft.enr")
    assert en["source"] == "gap" and en["gap_ref"] == "PERF-2569-0221" and en["emp_id"] == "EMP-01"
    return "gap hook display-only → แนะนำ + เลือกได้ (source=gap · อ่านจาก Performance)"


def c_fn11(page):
    """[FN-11] ยกเลิกลงทะเบียน (ผ่าน confirm · soft archive)"""
    open_(page)
    n0 = ev(page, "() => DB.enrolls.length")
    after(page, "() => cancelEnroll('EN6')")
    assert ev(page, "() => TC.mctx.type") == "confirm", "ยกเลิกไม่ผ่าน confirm"
    after(page, "() => tcConfirmYes()")
    assert ev(page, "() => getEnroll('EN6').status") == "cancelled", "ไม่ได้ยกเลิก"
    assert ev(page, "() => DB.enrolls.length") == n0, "soft archive แต่ record หาย"
    assert ev(page, "() => getEnroll('EN6').history[0].action") == "ยกเลิกการลงทะเบียน"
    return "ยกเลิก (confirm) → cancelled · record + ประวัติคงอยู่"


def c_fn12(page):
    """[FN-12] แจ้งเตือน (NTF) 3 จุด — เปิดรับ / ยืนยันลงทะเบียน / ประกาศผล"""
    open_(page)
    after(page, "() => { window.__ntf=[]; const _n=ntf; window.ntf=function(m){window.__ntf.push(m);return _n(m);}; }")
    after(page, "() => sessionOpen('SE1')")                                   # (1) เปิดรับ
    after(page, "() => { openEnrollModal('SE2'); TC.draft.enr.emp_id='EMP-01'; submitEnroll(); }")  # (2) ยืนยัน (ฟรี)
    after(page, "() => { setAttendance('EN5',true); openResultModal('EN5'); pickResult('pass'); submitResult(); }")  # (3) ประกาศผล (เช็คชื่อก่อน · FIX-03)
    log = ev(page, "() => window.__ntf")
    joined = " | ".join(log)
    assert any("เปิดรับสมัคร" in x for x in log), f"ไม่มี NTF เปิดรับ · log={joined}"
    assert any("ยืนยันลงทะเบียน" in x for x in log), f"ไม่มี NTF ยืนยัน · log={joined}"
    assert any("ประกาศผล" in x for x in log), f"ไม่มี NTF ประกาศผล · log={joined}"
    return f"NTF 3 จุดครบ (เปิดรับ · ยืนยัน · ประกาศผล) · {len(log)} events"


def c_fn13(page):
    """[FN-13] รายงาน completion rate + filter ตามหลักสูตร"""
    open_(page)
    after(page, "() => navigate('train/report')")
    tc = pc_text(page)
    assert "อัตราการอบรมสำเร็จ (completion rate)" in tc, "หน้ารายงานไม่มี completion rate"
    assert ev(page, "() => document.querySelectorAll('.funnel-row').length") > 0, "ไม่มีแถว funnel ต่อหลักสูตร"
    assert "อัตราผ่าน (completion)" in tc, "ไม่มีการ์ดสรุปอัตราผ่าน"
    # filter ตามหลักสูตร
    after(page, "() => { TC.f.report.course='CO3'; renderPageOnly(); }")
    rows_all = ev(page, "() => DB.courses.length")
    rows_one = ev(page, "() => document.querySelectorAll('.funnel-row').length")
    assert rows_one == 1 and rows_one < rows_all, "filter หลักสูตรไม่ได้จำกัดแถว funnel"
    assert "อัตราการอบรมสำเร็จ (completion rate)" in pc_text(page), "filter แล้วรายงานหาย"
    return f"completion report + filter (ทั้งหมด {rows_all} หลักสูตร → กรอง CO3 เหลือ {rows_one} แถว)"


def c_fn90(page):
    """[FN-90] ค้นหา/filter list + empty state"""
    open_(page)
    after(page, "() => navigate('train/course')")
    after(page, "() => { TC.f.course.q='zzzไม่มีจริง'; renderPageOnly(); }")
    assert "ไม่พบหลักสูตร" in pc_text(page), "ค้นไม่เจอแต่ไม่ขึ้น empty state"
    after(page, "() => { TC.f.course.q='ความปลอดภัย'; renderPageOnly(); }")
    t2 = pc_text(page)
    assert "ความปลอดภัยในการทำงาน" in t2 and "ไม่พบหลักสูตร" not in t2, "ค้นเจอแต่ไม่แสดงผล"
    return "search: เจอ/ไม่เจอ + empty state"


def c_fn91(page):
    """[FN-91] ปิดหลักสูตร (confirm gate + soft archive)"""
    open_(page)
    after(page, "() => courseClose('CO4')")
    body = ev(page, "() => TC.mctx.data.body")
    assert "soft archive" in body, "confirm ปิดหลักสูตรไม่ระบุ soft archive"
    # ยกเลิก (cancel) → ต้องไม่ปิด
    after(page, "() => closeModal()")
    assert ev(page, "() => getCourse('CO4').status") == "published", "ยกเลิก confirm แล้วยังปิด (gate พัง)"
    # ยืนยันปิดจริง
    h0 = ev(page, "() => getCourse('CO4').history.length")
    after(page, "() => courseClose('CO4')")
    after(page, "() => tcConfirmYes()")
    assert ev(page, "() => getCourse('CO4').status") == "closed", "confirm แล้วไม่ปิด"
    assert ev(page, "() => DB.courses.some(c=>c.id==='CO4')") is True, "soft archive แต่ record หาย"
    assert ev(page, "() => getCourse('CO4').history.length") >= h0 + 1, "ประวัติไม่ถูกเก็บต่อ"
    return "confirm gate + soft archive (record + history คงอยู่)"


def c_fn92(page):
    """[FN-92] validate field บังคับ + กัน double-submit"""
    open_(page)
    n0 = ev(page, "() => DB.courses.length")
    after(page, """() => { openCourseCreate();
      TC.draft={name:'',category:null,instructor:'',duration:'',has_cost:false,budget:'',desc:''}; }""")
    after(page, "() => submitCourse(false)")
    assert ev(page, "() => DB.courses.length") == n0, "ฟอร์มว่างแต่บันทึกได้ (validate พัง)"
    # double-submit guard: busy=true ต้องไม่บันทึก
    after(page, """() => { TC.draft={name:'X',category:'safety',instructor:'Y',duration:'1 วัน',
      has_cost:false,budget:'',desc:''}; TC.busy=true; }""")
    after(page, "() => submitCourse(false)")
    assert ev(page, "() => DB.courses.length") == n0, "busy=true แต่ยังบันทึก (double-submit guard พัง)"
    after(page, "() => { TC.busy=false; }")
    return "validate ฟอร์มว่าง + guard busy"


def c_fn93(page):
    """[FN-93] audit append-only (unshift ใหม่ · ของเก่าคงเดิม)"""
    open_(page)
    before = ev(page, "() => ({len:getSession('SE1').history.length, top:getSession('SE1').history[0].action})")
    after(page, "() => sessionOpen('SE1')")
    h = ev(page, "() => getSession('SE1').history")
    assert len(h) == before["len"] + 1, "audit ไม่ได้ append (จำนวนไม่เพิ่มทีละ 1)"
    assert "เปิดรับสมัคร" in h[0]["action"], "รายการล่าสุดไม่ใช่ action ที่เพิ่งทำ"
    assert h[1]["action"] == before["top"], "รายการเก่าถูกแก้/หาย (ไม่ append-only)"
    return "audit append-only: unshift ใหม่ · ของเก่าคงเดิม"


def c_fn94(page):
    """[FN-94] mask งบ/มูลค่า (RESTRICTED) ตาม role"""
    open_(page)
    after(page, "() => navigate('train/course')")
    after(page, "() => { setPersona('viewer'); TC.f.course.status='all'; renderPageOnly(); }")
    masked = pc_text(page)
    assert "••••••" in masked and "30,000" not in masked, "role viewer แต่ไม่ mask งบ"
    after(page, "() => { setPersona('hr'); renderPageOnly(); }")
    full = pc_text(page)
    assert "30,000" in full, "role hr กลับถูก mask งบ"
    return "mask ตาม role: viewer=•••••• · hr=เห็นตัวเลข"


# ═══════════════════════ NEGATIVE (unsupported ×5, rendered → absent) ═══════════════════════

NEG_JS = r"""
() => {
  const box=document.createElement('div');
  let html='';
  TC.dctx={kind:'course',mode:'create',id:null};
  TC.draft={name:'',category:'safety',instructor:'',duration:'',has_cost:true,budget:'1000',desc:''};
  html+=courseFormDrawer();
  TC.dctx={kind:'session',mode:'create',id:null};
  TC.draft={courseId:'CO1',start:'',end:'',time:'',location:'',capacity:20};
  html+=sessionFormDrawer();
  ['detail','learner','approval','history'].forEach(t=>{TC.dctx={kind:'session',mode:'view',id:'SE1',tab:t};html+=sessionViewDrawer();});
  TC.draft={enr:{sid:'SE1',emp_id:null,source:'manual',gap_ref:null}};
  TC.mctx={type:'enroll',data:{sid:'SE1'}};
  html+=renderModal();
  TC.draft={res:{eid:'EN5',result:null,comment:''}};
  TC.mctx={type:'result',data:{eid:'EN5'}};
  html+=renderModal();
  ['course','plan','result','report'].forEach(t=>{TC.tab=t;html+=renderPage();});
  box.innerHTML=html;
  const acts=[...box.querySelectorAll('button,[onclick]')].filter(el=>{
    const h=(el.getAttribute('onclick')||'').replace(/\s/g,'');
    return !/^event\.stopPropagation\(\)$/.test(h);
  }).map(el=>({txt:(el.textContent||'').replace(/\s+/g,' ').trim(), on:(el.getAttribute('onclick')||'')}));
  return {
    acts,
    fileInputs: box.querySelectorAll('input[type=file]').length,
    hasDisplayOnly: /display-only/.test(html),
    hasSendExpense: html.indexOf('ส่ง Expense Claim')>=0,
    hasSoftRef: /soft ref/.test(html),
    hasHrConfig: html.indexOf('อ่านจาก HR Configuration')>=0,
    hasGapHook: /hook display-only/.test(html),
  };
}
"""


def c_unsupported(page):
    """[NEG] เคสเชิงลบ ×5 — เรนเดอร์ทุก affordance จริงแล้ว assert 'ไม่มี' ของห้ามมี"""
    open_(page)
    r = ev(page, NEG_JS)
    acts = r["acts"]

    def hit(pat):
        import re
        rx = re.compile(pat, re.I)
        return [a for a in acts if rx.search(a["txt"]) or rx.search(a["on"])]

    # ยืนยันว่าเก็บ affordance ได้จริง (กัน vacuous pass)
    assert len(acts) > 10, f"เก็บ affordance ได้น้อยผิดปกติ ({len(acts)}) — surfaces อาจไม่เรนเดอร์"

    # 1) ไม่มีปุ่ม/ทางลัด "จ่ายเงินจริง / ลงบัญชี" (มีแค่ hook display-only ส่ง Expense)
    v1 = hit(r"จ่ายเงิน|ลงบัญชี|ชำระเงิน|โอนเงิน|ตัดจ่าย|บันทึกบัญชี|payExpense|postExpense|postGl|postGL|postAccount")
    assert not v1, f"[neg1] พบ affordance จ่ายเงิน/ลงบัญชีจริง: {v1[:3]}"
    assert r["hasDisplayOnly"] and r["hasSendExpense"], "[neg1] ควรมี hook Expense Claim (display-only) แทน"

    # 2) ไม่มีปุ่มสร้าง/แก้ gap หรือประเมินผลงานเอง (อ่าน Performance อย่างเดียว)
    v2 = hit(r"createGap|editGap|addGap|saveGap|newGap|delGap|removeGap|evaluatePerf|scorePerf|assessPerf|สร้าง gap|แก้ไข gap|ประเมินผลงาน")
    assert not v2, f"[neg2] พบ affordance สร้าง/แก้ gap หรือประเมินผลงาน: {v2[:3]}"
    assert r["hasGapHook"], "[neg2] gap ควรเป็น hook display-only (อ่านอย่างเดียว)"

    # 3) ไม่มี eLearning content/SCORM upload · competency mapping editor
    assert r["fileInputs"] == 0, "[neg3] พบช่องอัปโหลดไฟล์ (SCORM/eLearning content)"
    v3 = hit(r"scorm|elearning|อีเลิร์น|competen|อัปโหลด|upload|mappingEditor")
    assert not v3, f"[neg3] พบ affordance eLearning/SCORM/competency: {v3[:3]}"

    # 4) ไม่มีใบรับรองเลขรัน/ปุ่ม gen PDF ทางการ (cert = soft ref เท่านั้น)
    v4 = hit(r"genPdf|generatePdf|printCert|downloadCert|exportCert|certPdf|เลขที่ใบรับรอง|PDF ทางการ|พิมพ์ใบรับรอง|ออกเลขที่")
    assert not v4, f"[neg4] พบ affordance ใบรับรองเลขรัน/PDF ทางการ: {v4[:3]}"
    assert r["hasSoftRef"], "[neg4] cert ควรระบุ soft ref"

    # 5) ไม่มีปุ่มสร้าง/แก้ config หมวดหลักสูตรกลาง (อ่านจาก HR Config)
    v5 = hit(r"createCat|editCat|addCat|saveCat|newCategory|manageCategor|deleteCat|delCat|สร้างหมวด|แก้ไขหมวด|จัดการหมวด|เพิ่มหมวด|ลบหมวด")
    assert not v5, f"[neg5] พบ affordance CRUD หมวดหลักสูตร: {v5[:3]}"
    assert r["hasHrConfig"], "[neg5] หมวดควรระบุ 'อ่านจาก HR Configuration'"

    return f"unsupported 5/5 absent ({len(acts)} affordance ตรวจ · file-upload=0)"


# ═══════════════════════ BASE-KIT LATENT BUG PROBES ═══════════════════════

def c_modal_over_drawer(page):
    """[UI-REG] modal เปิดจากในลิ้นชักต้องอยู่เหนือ drawer (z) — regression F-HR-RECRUIT base-kit"""
    open_(page)
    after(page, "() => navigate('train/plan')")
    after(page, "() => openSessionView('SE1')")            # drawer เปิด
    after(page, "() => openEnrollModal('SE1')")            # modal เปิดทับ drawer
    viol = ev(page, JS_MODAL_UNDER_DRAWER)
    assert viol == [], f"modal จมใต้ drawer: {viol}"
    mz = ev(page, "() => parseInt(getComputedStyle(document.querySelector('.modal-backdrop')).zIndex,10)")
    dz = ev(page, "() => parseInt(getComputedStyle(document.querySelector('.drawer')).zIndex,10)")
    assert mz > dz, f"modal z({mz}) ต้อง > drawer z({dz})"
    # in-drawer confirm modal ต้องคลิกได้ (ไม่จมหลัง drawer)
    after(page, "() => { closeModal(); }")
    after(page, "() => sessionClose('SE1')")               # confirm จากในลิ้นชัก
    viol2 = ev(page, JS_MODAL_UNDER_DRAWER)
    assert viol2 == [], f"in-drawer confirm จมใต้ drawer: {viol2}"
    return f"modal เหนือ drawer (z {mz}>{dz}) · in-drawer confirm คลิกได้"


def c_overlay_stack(page):
    """[UI] ไม่มี element แปลกปลอมวาดทับ overlay (drawer+modal เปิดพร้อมกัน)"""
    open_(page)
    after(page, "() => navigate('train/plan')")
    after(page, "() => openSessionView('SE1')")
    after(page, "() => openEnrollModal('SE1')")
    viol = ev(page, JS_OVERLAY_STACK)
    assert viol == [], f"มี element วาดทับ overlay: {viol[:4]}"
    return "overlay stack สะอาด (ไม่มีของทับ drawer/modal)"


def c_static_css(page):
    """[UI] CSS var ที่ใช้แต่ไม่ประกาศ (ต้นตอ z-index หาย) + layout ของ list/drawer"""
    open_(page)
    # `--shellbar-h` ใช้เฉพาะแบบมี fallback: var(--shellbar-h, 52px) ทั้ง 2 จุด (บรรทัด 376/377)
    # = จุด override ที่ตั้งใจให้ optional ไม่ใช่คลาสบั๊ก z-index ที่ไม่มี fallback → พิสูจน์แล้วว่า benign
    # (JS_CSSVAR ของ uikit ไม่ได้แยก fallback ออก = false-positive · ไม่แก้ uikit รอบนี้ · ดูรายงาน)
    BENIGN_VARS = {"--shellbar-h"}
    missing = [v for v in ev(page, JS_CSSVAR) if v not in BENIGN_VARS]
    assert missing == [], f"CSS var ใช้แต่ไม่ประกาศ (ไม่มี fallback): {missing}"
    after(page, "() => navigate('train/plan')")
    after(page, "() => openSessionView('SE1')")
    lay = ev(page, JS_LAYOUT)
    for k in ("clipped", "hscroll", "ghostCtl", "overlap", "cellOverflow", "menuCovered"):
        assert lay.get(k) == [], f"layout ผิด [{k}]: {lay.get(k)[:4]}"
    return "CSS var ครบ · layout list+drawer สะอาด (ไม่ clip/hscroll/ghost/overlap)"


def c_affordance(page):
    """[UI] ของที่มี onclick ต้องมี cursor:pointer (กดได้แต่ไม่มีสัญญาณ = base-kit bug)"""
    open_(page)
    after(page, "() => navigate('train/course')")
    a1 = ev(page, JS_AFFORDANCE)
    after(page, "() => navigate('train/plan')")
    after(page, "() => openSessionView('SE1')")
    a2 = ev(page, JS_AFFORDANCE)
    bad = (a1 or []) + (a2 or [])
    assert bad == [], f"clickable แต่ไม่มี cursor:pointer: {bad[:5]}"
    return "affordance: ทุกจุดคลิกได้มี cursor:pointer"


def c_focus_retention(page):
    """[UI] search input พิมพ์หลายตัวอักษร → focus ไม่หลุดหลังตัวแรก (re-render preserve)"""
    open_(page)
    after(page, "() => navigate('train/course')")
    inp = page.locator(".filter-bar input.input").first
    inp.click()
    page.keyboard.type("ความ", delay=90)
    settle(page)
    q = ev(page, "() => TC.f.course.q")
    assert q == "ความ", f"พิมพ์แล้วค่าไม่ครบ (focus หลุด?) — ได้ '{q}'"
    ph = ev(page, "() => (document.activeElement && document.activeElement.placeholder) || ''")
    assert "ค้นหาชื่อหลักสูตร" in ph, f"focus ไม่กลับมาที่ช่องค้นหา (active placeholder='{ph}')"
    assert "ความปลอดภัยในการทำงาน" in pc_text(page), "พิมพ์แล้วผลค้นไม่กรอง"
    return "พิมพ์ 'ความ' ครบ · focus คงที่ · ผลกรองถูก"


def c_icons(page):
    """[UI] ไม่มี <i data-lucide> ที่เรนเดอร์เป็นไอคอนว่าง (ICONS ครบ)"""
    open_(page)
    loaded = ev(page, "() => !!(window.lucide && document.querySelector('svg.lucide'))")
    if loaded:
        after(page, "() => navigate('train/plan')")
        after(page, "() => openSessionView('SE1')")
        miss = unrendered_visible_icons(page, "body")
        assert not miss, f"ไอคอน lucide เรนเดอร์เป็นช่องว่าง (ชื่อผิด/ไม่มีใน map): {miss[:6]}"
        return "lucide โหลดจริง · ไอคอนเรนเดอร์ครบ (ไม่มีช่องว่าง)"
    # offline fallback — ตรวจแบบ static ว่าไม่มีชื่อไอคอนว่าง (blank name = ไอคอนว่างแน่นอน)
    blanks = ev(page, """() => [...document.querySelectorAll('i[data-lucide]')]
      .filter(el=>!(el.getAttribute('data-lucide')||'').trim())
      .map(el=>el.outerHTML.slice(0,40))""")
    assert blanks == [], f"พบ <i data-lucide> ชื่อว่าง (ไอคอนว่างแน่นอน): {blanks[:6]}"
    return "lucide CDN offline — static: ไม่มีชื่อไอคอนว่าง (runtime name-validity ตรวจไม่ได้รอบนี้)"


# ═══════════════════ FIX ACCEPTANCE (7 FIX ของ BA) ═══════════════════

def c_fix01(page):
    """[FIX-01] บันทึกผลได้เฉพาะรอบที่ปิดแล้ว · completion นับเฉพาะรอบ closed"""
    open_(page)
    # EN2 = confirmed ใน SE1 (status=open) → บันทึกผลไม่ได้ · ปุ่มบนจอต้อง disabled
    after(page, "() => navigate('train/plan')")
    after(page, "() => openSessionView('SE1','learner')")
    dis = ev(page, """() => { const bs=[...document.querySelectorAll('#drawer button')];
      return bs.some(b=>/บันทึกผล/.test(b.textContent) && (b.disabled||b.classList.contains('is-disabled'))); }""")
    assert dis, "รอบ open แต่ปุ่มบันทึกผลไม่ disabled"
    # เรียก openResultModal ตรง ๆ ตอนรอบยัง open → บล็อก (modal ไม่เปิด)
    after(page, "() => openResultModal('EN2')")
    assert ev(page, "() => state.modal.open") is False, "รอบ open แต่เปิด modal บันทึกผลได้"
    # เรียก submitResult ตรง ๆ → status ไม่เปลี่ยน (defense-in-depth)
    after(page, "() => { TC.draft.res={eid:'EN2',result:'pass',comment:'',evalScore:null}; submitResult(); }")
    assert ev(page, "() => getEnroll('EN2').status") == "confirmed", "รอบ open แต่ submitResult เปลี่ยนสถานะได้"
    assert ev(page, "() => getEnroll('EN2').result") is None
    # ปิดรอบ SE1 (sessionClose) แล้ว → เช็คชื่อ + บันทึกผลได้
    after(page, "() => sessionClose('SE1')")
    after(page, "() => tcConfirmYes()")
    assert ev(page, "() => getSession('SE1').status") == "closed", "ปิดรอบไม่สำเร็จ"
    after(page, "() => { setAttendance('EN2',true); openResultModal('EN2'); pickResult('pass'); submitResult(); }")
    assert ev(page, "() => getEnroll('EN2').status") == "passed", "ปิดรอบแล้วยังบันทึกผลไม่ได้"
    # completion rate นับเฉพาะผลจากรอบ closed
    assert ev(page, "() => isClosedResult(getEnroll('EN2'))") is True, "ผลจากรอบ closed ไม่ถูกนับ"
    return "รอบ open→บันทึกผลบล็อก (ปุ่ม disabled + guard) · ปิดรอบ→บันทึกได้ · completion เฉพาะ closed"


def c_fix02(page):
    """[FIX-02] สิทธิ์ hr (canApprove=false) · sendExpense/submitSession guards"""
    open_(page)
    assert ev(page, "() => TC.persona==='hr' && PERSONAS.hr.canApprove===false"), "persona เริ่มต้นไม่ใช่ hr"
    # hr เรียก enrollApprove ตรง → บล็อก (EN1 pending_doa · current ไม่ขยับ)
    after(page, "() => enrollApprove('EN1')")
    assert ev(page, "() => getEnroll('EN1').status") == "pending_doa", "hr กดอนุมัติผ่าน (ไม่ควร)"
    assert ev(page, "() => getEnroll('EN1').approval.current") == 0, "hr อนุมัติแล้ว current ขยับ"
    # hr เรียก enrollReject ตรง → บล็อก (ไม่เปิด reason modal)
    after(page, "() => enrollReject('EN1')")
    assert ev(page, "() => state.modal.open") is False, "hr กดไม่อนุมัติแล้วเปิด reason modal ได้"
    assert ev(page, "() => getEnroll('EN1').status") == "pending_doa"
    # sendExpense ตอน pending_doa → บล็อก
    after(page, "() => sendExpense('EN1')")
    assert ev(page, "() => getEnroll('EN1').expenseSent") is False, "ส่ง Expense ได้ทั้งที่ยัง pending_doa"
    # ส่งซ้ำ (EN2 expenseSent=true อยู่แล้ว) → บล็อก · idempotent ไม่ error
    after(page, "() => sendExpense('EN2')")
    assert ev(page, "() => getEnroll('EN2').expenseSent") is True
    # submitSession ให้หลักสูตรที่ปิดแล้ว (CO4 closed) → บล็อก
    after(page, "() => courseClose('CO4')")
    after(page, "() => tcConfirmYes()")
    assert ev(page, "() => getCourse('CO4').status") == "closed"
    n0 = ev(page, "() => DB.sessions.length")
    after(page, """() => { openSessionCreate();
      TC.draft={courseId:'CO4',start:'2026-12-01',end:'2026-12-01',time:'09:00–16:00',location:'ห้อง X',capacity:5}; }""")
    after(page, "() => submitSession()")
    assert ev(page, "() => DB.sessions.length") == n0, "สร้างรอบให้หลักสูตร closed ได้ (ไม่ควร)"
    return "hr: approve/reject/sendExpense บล็อก · ส่งซ้ำ idempotent · สร้างรอบหลักสูตร closed บล็อก"


def c_fix03(page):
    """[FIX-03] เช็คชื่อก่อนบันทึกผล (รอบ closed) + ประเมิน 1-5 + comment เก็บ/แสดง"""
    open_(page)
    # SE2 closed · เช็คชื่อทำได้
    after(page, "() => setAttendance('EN6',true)")
    assert ev(page, "() => getEnroll('EN6').attended") is True, "เช็คชื่อรอบปิดไม่ได้"
    # ยังไม่เช็คชื่อ (EN5 attended=null) → บันทึกผลไม่ได้
    after(page, "() => openResultModal('EN5')")
    assert ev(page, "() => state.modal.open") is False, "ยังไม่เช็คชื่อแต่เปิด modal บันทึกผลได้"
    after(page, "() => { TC.draft.res={eid:'EN5',result:'pass',comment:'',evalScore:null}; submitResult(); }")
    assert ev(page, "() => getEnroll('EN5').status") == "confirmed", "ยังไม่เช็คชื่อแต่บันทึกผลได้"
    # เช็คชื่อ = ขาด (attended=false) → ยังบันทึกผลไม่ได้
    after(page, "() => setAttendance('EN5',false)")
    after(page, "() => openResultModal('EN5')")
    assert ev(page, "() => state.modal.open") is False, "attended=false แต่ยังเปิดบันทึกผลได้"
    # EN6 เข้าอบรม → บันทึกผล + ประเมิน 4/5 + comment
    after(page, "() => { openResultModal('EN6'); pickResult('pass'); pickEval(4); TC.draft.res.comment='ตั้งใจเรียนดี'; submitResult(); }")
    assert ev(page, "() => getEnroll('EN6').status") == "passed"
    assert ev(page, "() => getEnroll('EN6').evalScore") == 4, "คะแนนประเมินไม่ถูกเก็บ"
    assert ev(page, "() => getEnroll('EN6').evalComment") == "ตั้งใจเรียนดี", "comment ประเมินไม่ถูกเก็บ"
    # แสดงในแถวผู้เรียน (evalChip)
    after(page, "() => openSessionView('SE2','learner')")
    assert "ประเมิน 4/5" in ev(page, "() => document.querySelector('#drawer').textContent"), \
        "คะแนนประเมินไม่แสดงในแถวผู้เรียน"
    return "เช็คชื่อรอบปิด · ยังไม่เช็ค/ขาด=บันทึกผลบล็อก · ประเมิน 4/5+comment เก็บ+แสดง"


def c_fix04(page):
    """[FIX-04] ประวัติอบรมรายคน · ชั่วโมงสะสมเฉพาะ passed · empty state"""
    open_(page)
    # EMP-04 (EN3 passed · CO3 = 6 ชม.) → ชั่วโมงสะสม 6
    after(page, "() => openEmpHistory('EMP-04')")
    assert ev(page, "() => state.modal.open && TC.mctx.type==='emphist'"), "ไม่เปิด modal ประวัติอบรม"
    b4 = ev(page, "() => document.querySelector('#modalBackdrop .modal').textContent")
    assert "ประวัติอบรม" in b4 and "6 ชม." in b4, "ชั่วโมงสะสม (passed) ไม่ถูก (EMP-04 ควร 6 ชม.)"
    after(page, "() => closeModal()")
    # EMP-05 (EN4 failed) → มีประวัติแต่ชั่วโมงสะสม = 0 (ไม่ผ่าน ไม่นับ)
    after(page, "() => openEmpHistory('EMP-05')")
    b5 = ev(page, "() => document.querySelector('#modalBackdrop .modal').textContent")
    assert "0 ชม." in b5, "ชั่วโมงสะสมนับรายการที่ไม่ผ่านด้วย (ต้องเฉพาะ passed)"
    after(page, "() => closeModal()")
    # EMP-07 ไม่มีประวัติ → empty state
    after(page, "() => openEmpHistory('EMP-07')")
    b7 = ev(page, "() => document.querySelector('#modalBackdrop .modal').textContent")
    assert "ยังไม่มีประวัติอบรม" in b7, "คนไม่มีประวัติไม่ขึ้น empty state"
    return "ประวัติรายคน: EMP-04=6ชม (passed) · EMP-05=0ชม (failed ไม่นับ) · EMP-07 empty state"


def c_fix05(page):
    """[FIX-05] การ์ดต้นทุนต่อหัว = งบ/ผู้ผ่าน · 0 ผ่าน/ฟรี → '—' (ไม่หารศูนย์)"""
    open_(page)
    after(page, "() => navigate('train/report')")
    rt = pc_text(page)
    assert "ต้นทุนต่อหัว" in rt, "ไม่มีการ์ดต้นทุนต่อหัว"
    assert "กันหารศูนย์" in rt, "การ์ดต้นทุนต่อหัวไม่ระบุกันหารศูนย์"
    # ยังไม่มีผู้ผ่านจากรอบ closed (CO1/CO2 has_cost) → ต้นทุนต่อหัว = '—'
    dash = ev(page, "() => [...document.querySelectorAll('.cph-total .cph-v')].map(e=>e.textContent.trim())")
    assert dash and all(v == '—' for v in dash), f"ผู้ผ่าน=0 แต่ไม่ขึ้น '—' (หารศูนย์?): {dash}"
    assert "Infinity" not in rt and "NaN" not in rt, "พบ NaN/Infinity (หารศูนย์)"
    # สร้างผู้ผ่านจริงให้ CO1: ปิด SE1 + EN2 เข้า+ผ่าน → ต้นทุนต่อหัว = 30,000/1
    after(page, "() => sessionClose('SE1')")
    after(page, "() => tcConfirmYes()")
    after(page, "() => { setAttendance('EN2',true); openResultModal('EN2'); pickResult('pass'); submitResult(); }")
    after(page, "() => navigate('train/report')")
    tot = ev(page, """() => [...document.querySelectorAll('.cph-card')].map(c=>({
      name:c.querySelector('.cph-name').textContent.trim(),
      per:c.querySelector('.cph-total .cph-v').textContent.trim()}))""")
    hit = [c for c in tot if "30,000" in c["per"] and c["per"] != "—"]
    assert hit, f"มีผู้ผ่าน 1 คน (งบ 30,000) แต่ต้นทุนต่อหัวไม่ = 30,000: {tot}"
    return "ต้นทุนต่อหัว: 0 ผ่าน→'—' (ไม่หารศูนย์) · 1 ผ่าน (งบ 30,000)→30,000"


def c_fix06(page):
    """[FIX-06] ไม่มี <i data-lucide> เรนเดอร์เป็นกล่องว่างใน modal (ลงทะเบียน/ประวัติ/บันทึกผล)"""
    open_(page)
    loaded = ev(page, "() => !!(window.lucide && document.querySelector('svg.lucide'))")

    def check_modal(open_js, label):
        after(page, open_js)
        assert ev(page, "() => state.modal.open") is True, f"{label}: modal ไม่เปิด"
        if loaded:
            miss = unrendered_visible_icons(page, "#modalBackdrop .modal")
            assert not miss, f"{label}: ไอคอนว่างใน modal {miss[:4]}"
        else:
            blanks = ev(page, """() => [...document.querySelectorAll('#modalBackdrop .modal i[data-lucide]')]
              .filter(el=>!(el.getAttribute('data-lucide')||'').trim()).length""")
            assert blanks == 0, f"{label}: พบ <i data-lucide> ชื่อว่างใน modal"
        after(page, "() => closeModal()")

    check_modal("() => openEnrollModal('SE1')", "ลงทะเบียน")
    check_modal("() => openEmpHistory('EMP-04')", "ประวัติอบรม")
    after(page, "() => setAttendance('EN5',true)")     # SE2 closed → เปิดบันทึกผลได้
    check_modal("() => openResultModal('EN5')", "บันทึกผล")
    return f"ไอคอนใน modal ครบทั้ง 3 (ลงทะเบียน/ประวัติ/บันทึกผล){'' if loaded else ' · offline: static blank-name'}"


def c_fix07(page):
    """[FIX-07] combobox ผู้เรียนใน modal ลงทะเบียน → list portal ใน #overlay-root · fixed · ≥4 option มี avatar · ไม่ clip"""
    open_(page)
    after(page, "() => openEnrollModal('SE1')")
    after(page, "() => ssOpen('enr_emp')")
    info = ev(page, """() => {
      const host=document.getElementById('overlay-root');
      const list=host&&host.querySelector('#ss-list-enr_emp');
      if(!list) return {inPortal:false};
      const cs=getComputedStyle(list);
      const vis=[...list.querySelectorAll('.ss-opt')].filter(o=>{const r=o.getBoundingClientRect();return r.width>0&&r.height>0;});
      return {inPortal:true, position:cs.position, hidden:list.classList.contains('hidden'),
              nOpts:vis.length, nAvatar:vis.filter(o=>o.querySelector('.uc-avatar.ss-opt-av')).length};
    }""")
    assert info["inPortal"], "ss-list ไม่ได้ portal ไป #overlay-root"
    assert info["position"] == "fixed", f"portal list ต้อง position:fixed (ได้ {info['position']})"
    assert info["hidden"] is False, "portal list เปิดแล้วยังมี class hidden"
    assert info["nOpts"] >= 4, f"เห็น option < 4 ({info['nOpts']}) — อาจโดน clip"
    assert info["nAvatar"] == info["nOpts"], f"บาง option ไม่มี avatar ({info['nAvatar']}/{info['nOpts']})"
    clipped = ev(page, JS_LAYOUT)["clipped"]
    ss_clip = [c for c in clipped if "ss-list" in str(c.get("el", ""))]
    assert ss_clip == [], f"combobox list โดน clip: {ss_clip[:3]}"
    return f"portal combobox: #overlay-root · fixed · {info['nOpts']} option ทุกตัวมี avatar · ไม่ clip"


# ═══════════════════ REGRESSION (2 bug จาก manual test) ═══════════════════

def c_bug01(page):
    """[BUG-01] แท็บอนุมัติ/ค่าใช้จ่าย รอบมีผู้เรียนหลายคน → การ์ดไม่ nest ซ้อนกัน"""
    open_(page)
    after(page, "() => navigate('train/plan')")
    after(page, "() => openSessionView('SE1','approval')")   # SE1 มี EN1 + EN2 (มี approval ทั้งคู่)
    nl = nested_cards(page, "#drawer")
    assert nl == [], f"การ์ด secwrap ซ้อนกันในแท็บอนุมัติ (BUG-01 กลับมา): {nl[:3]}"
    cards = ev(page, "() => [...document.querySelectorAll('#drawer .drawer-body > .secwrap')].length")
    assert cards >= 3, f"ควรมีการ์ด EC + ผู้เรียน 2 คน = ≥3 การ์ดระดับบน (ได้ {cards})"
    return f"อนุมัติ 2 ผู้เรียน: {cards} การ์ด top-level แยกกัน · ไม่ nest"


def c_bug02(page):
    """[BUG-02] session create → เลือกหลักสูตร ses_course → list ปิด + input โชว์ค่า + open=false"""
    open_(page)
    after(page, "() => openSessionCreate()")
    assert ev(page, "() => !!(window.__ss && window.__ss['ses_course'])"), "ses_course ไม่ถูก init"
    r = assert_combobox_closes_after_select(page, "ses_course", 0)
    settle(page)
    assert ev(page, "() => !!TC.draft.courseId"), "เลือกหลักสูตรแล้ว courseId ไม่ถูกตั้ง (onSelect ไม่ทำงาน)"
    return f"ses_course: เลือกแล้วปิด · input='{str(r['inputValue'])[:16]}…' · open=false · courseId ติด"


# ═══════════════════ REGRESSION (2 bug จาก manual test รอบ 2) ═══════════════════

# ปุ่มบันทึกผล disabled ที่ครอบ tt-wrap: หา button[disabled] ที่มีข้อความ 'บันทึกผล' ใน root
# แล้วตรวจว่าถูกครอบด้วย span.tt-wrap[title] (pointer-events auto → tooltip โชว์บนปุ่มที่กดไม่ได้)
JS_TTWRAP = r"""
(rootSel) => {
  const root = document.querySelector(rootSel) || document;
  const btns = [...root.querySelectorAll('button[disabled]')]
    .filter(b => /บันทึกผล/.test(b.textContent || ''));
  return btns.map(b => {
    const sp = b.closest('span.tt-wrap');
    const cs = sp ? getComputedStyle(sp) : null;
    const t = sp ? (sp.getAttribute('title') || '') : '';
    return {
      disabled: b.disabled === true,
      wrapped: !!sp,
      titleOk: t.trim().length > 0,
      pe: cs ? cs.pointerEvents : null,
      title: t.slice(0, 30)
    };
  });
}
"""


def c_bug03(page):
    """[BUG-03] ปุ่มบันทึกผล disabled → ครอบ span.tt-wrap[title] (pointer-events auto · tooltip โชว์ได้) · ปุ่มยัง disabled"""
    open_(page)

    # 1) result tab — EN2 confirmed ใน SE1 (open) → ปุ่มบันทึกผล disabled ครอบ tt-wrap (line ~2445)
    after(page, "() => navigate('train/result')")
    r1 = page.evaluate(JS_TTWRAP, "#page-content")
    assert len(r1) >= 1, "หน้ารายการบันทึกผลไม่มีปุ่มบันทึกผล disabled (คาดว่ามี EN2 confirmed รอบ open)"
    for x in r1:
        assert x["disabled"] is True, "ปุ่มบันทึกผลใน result tab ไม่ได้ disabled (assertion เดิมพัง)"
        assert x["wrapped"] is True, f"[BUG-03] ปุ่ม disabled ใน result tab ไม่ถูกครอบ span.tt-wrap: {x}"
        assert x["titleOk"] is True, f"[BUG-03] span.tt-wrap ไม่มี title เหตุผล: {x}"
        assert x["pe"] not in (None, "none"), f"[BUG-03] span.tt-wrap pointer-events=none → tooltip ไม่โผล่: {x}"

    # 2) learner tab ในลิ้นชัก — SE1 open, EN2 confirmed → disabled + tt-wrap (line ~2718)
    after(page, "() => openSessionView('SE1','learner')")
    r2 = page.evaluate(JS_TTWRAP, "#drawer")
    assert len(r2) >= 1, "แท็บผู้เรียนไม่มีปุ่มบันทึกผล disabled (คาดว่ามี EN2 confirmed รอบ open)"
    for x in r2:
        assert x["disabled"] is True, "ปุ่มบันทึกผลใน learner tab ไม่ได้ disabled (assertion เดิมพัง)"
        assert x["wrapped"] is True, f"[BUG-03] ปุ่ม disabled ใน learner tab ไม่ถูกครอบ span.tt-wrap: {x}"
        assert x["titleOk"] is True, f"[BUG-03] span.tt-wrap (learner) ไม่มี title เหตุผล: {x}"
        assert x["pe"] not in (None, "none"), f"[BUG-03] span.tt-wrap (learner) pointer-events=none: {x}"

    return f"tt-wrap ครอบปุ่ม disabled: result {len(r1)} จุด · learner {len(r2)} จุด · title+pointer-events auto · ปุ่มยัง disabled"


def c_bug04(page):
    """[BUG-04] modal ลงทะเบียน: combobox enr_emp ไม่กาง dropdown เองตอน modal เปิด · คลิก ss-input → เปิดปกติ (avatar ครบ)"""
    open_(page)
    after(page, "() => openEnrollModal('SE1')")
    # รอ rAF chain (mb.is-open → trapFocus focus ช่องแรก → fix blur/ปิด) settle ก่อนอ่านสถานะสุดท้าย
    page.evaluate("() => new Promise(res=>{let n=0;const t=()=>{n++;if(n>=6)res();else requestAnimationFrame(t);};requestAnimationFrame(t);})")

    st = ev(page, """() => ({
      modalOpen: state.modal.open === true,
      ssOpen: (window.__ss && window.__ss['enr_emp']) ? window.__ss['enr_emp'].open : null,
      listHidden: (()=>{const l=document.getElementById('ss-list-enr_emp');return l?l.classList.contains('hidden'):null;})(),
      aeIsSsInput: !!(document.activeElement && document.activeElement.classList &&
                      document.activeElement.classList.contains('ss-input'))
    })""")
    assert st["modalOpen"], "modal ลงทะเบียนไม่เปิด"
    assert st["ssOpen"] is False, f"[BUG-04] enr_emp กาง dropdown เองตอน modal เปิด (open={st['ssOpen']})"
    assert st["listHidden"] is True, f"[BUG-04] #ss-list-enr_emp ไม่ hidden ตอน modal เพิ่งเปิด (listHidden={st['listHidden']})"
    assert st["aeIsSsInput"] is False, "[BUG-04] activeElement ยังเป็น ss-input (fix ไม่ได้ blur)"
    # helper กลาง: ไม่มี combobox ตัวไหนใน modal กางเอง
    auto = modal_autoopens_comboboxes(page)
    assert auto == [], f"[BUG-04] มี combobox กาง dropdown เองใน modal: {auto}"

    # คลิก ss-input → เปิด dropdown ปกติ (option ≥1 · ทุกตัวมี .ss-opt-av avatar)
    page.click("#ss-input-enr_emp")
    settle(page)
    op = ev(page, """() => {
      const l=document.getElementById('ss-list-enr_emp');
      if(!l) return {listShown:false,n:0,nAv:0,open:null};
      const opts=[...l.querySelectorAll('.ss-opt')].filter(o=>{const r=o.getBoundingClientRect();return r.width>0&&r.height>0;});
      return { open: (window.__ss['enr_emp']||{}).open===true, listShown: !l.classList.contains('hidden'),
               n: opts.length, nAv: opts.filter(o=>o.querySelector('.ss-opt-av')).length };
    }""")
    assert op["listShown"] and op["open"] is True, f"คลิก ss-input แล้ว dropdown ไม่เปิด: {op}"
    assert op["n"] >= 1, f"เปิดแล้วไม่มี option ({op['n']})"
    assert op["nAv"] == op["n"], f"บาง option ไม่มี avatar .ss-opt-av ({op['nAv']}/{op['n']})"
    return f"BUG-04: modal เปิด→dropdown ปิด (open=false·list hidden·blur·helper สะอาด) · คลิก→เปิด {op['n']} option avatar ครบ"


def c_uikit_selfproof(page):
    """[C3.8] พิสูจน์ helper ใหม่ 2 ตัวจับ 'เวอร์ชันพัง' ได้จริง (ไม่แตะ อบรม.html — สร้างสภาพพังชั่วคราวในหน้า)"""
    open_(page)
    # (1) nested_cards — drawer จริงต้องสะอาด แล้วยัดโครงพัง secwrap-in-secwrap เข้าไปให้ helper จับ
    after(page, "() => navigate('train/plan')")
    after(page, "() => openSessionView('SE1','approval')")
    assert nested_cards(page, "#drawer") == [], "drawer จริงมี secwrap ซ้อน (BUG-01?)"
    ev(page, """() => { const d=document.querySelector('#drawer .drawer-body')||document.getElementById('drawer');
      const bad=document.createElement('div'); bad.className='secwrap'; bad.id='__proof_bad';
      bad.innerHTML='<div class="secwrap">nested proof</div>'; d.appendChild(bad); }""")
    caught = nested_cards(page, "#drawer")
    assert any(v["inner"] == "secwrap" for v in caught), "nested_cards จับ secwrap ซ้อนไม่ได้ (ตัววัดพัง)"
    ev(page, "() => { const b=document.getElementById('__proof_bad'); if(b)b.remove(); }")
    assert nested_cards(page, "#drawer") == [], "ลบโครงพังแล้ว helper ยังฟ้อง (ตัววัด noisy)"
    # (2) combobox reopen-after-select — ย้อน onSelect เป็นแบบเปิดเมนูซ้ำ (จำลองบั๊กเดิม) ให้ helper จับ
    after(page, "() => openSessionCreate()")
    ev(page, "() => { window.__ss['ses_course'].onSelect = () => ssOpen('ses_course'); }")
    broken = combobox_state_after_select(page, "ses_course", 0)
    assert broken.get("open") is True or broken.get("listHidden") is False, \
        f"helper ไม่จับ reopen-after-select เวอร์ชันพัง: {broken}"
    # (3) modal_autoopens_comboboxes — modal จริงหลัง fix ต้องสะอาด แล้วจำลอง auto-open ให้ helper จับ
    open_(page)
    after(page, "() => openEnrollModal('SE1')")
    page.evaluate("() => new Promise(res=>{let n=0;const t=()=>{n++;if(n>=6)res();else requestAnimationFrame(t);};requestAnimationFrame(t);})")
    assert modal_autoopens_comboboxes(page) == [], "modal จริงมี combobox กางเอง (BUG-04 กลับมา?)"
    # จำลองบั๊ก: บังคับเปิด dropdown ของ enr_emp เอง (เหมือน trapFocus→onfocus→ssOpen ก่อนมี fix)
    ev(page, "() => { const i=document.getElementById('ss-input-enr_emp'); if(i)i.focus(); ssOpen('enr_emp'); }")
    caught_ao = modal_autoopens_comboboxes(page)
    assert any(v["key"] == "enr_emp" for v in caught_ao), f"helper ไม่จับ combobox auto-open เวอร์ชันพัง: {caught_ao}"
    # คืนสภาพ
    ev(page, """() => { window.__ss['enr_emp'].open=false;
      const l=document.getElementById('ss-list-enr_emp'); if(l)l.classList.add('hidden');
      const i=document.getElementById('ss-input-enr_emp'); if(i)i.blur(); }""")
    assert modal_autoopens_comboboxes(page) == [], "คืนสภาพแล้ว helper ยังฟ้อง (ตัววัด noisy)"
    return "C3.8: nested_cards + combobox (reopen + auto-open) helper จับเวอร์ชันพังได้จริง (สร้างสภาพพังแล้วคืน · ไม่แตะ HTML)"


CASES = [
    ("FN-01", "สร้างหลักสูตร (has_cost+งบ)", c_fn01),
    ("FN-02", "สร้างรอบ + เปิดรับ", c_fn02),
    ("FN-03", "ลงทะเบียนเกินจำนวนรับ block", c_fn03),
    ("FN-04 FN-08", "has_cost→pending_doa + DOA slot picker (ไม่ hardcode)", c_fn04_08),
    ("FN-05", "no-cost→confirmed ทันที (ข้าม DOA)", c_fn05),
    ("FN-06", "บันทึกผล ผ่าน/ไม่ผ่าน", c_fn06),
    ("FN-07", "ใบรับรอง soft ref", c_fn07),
    ("FN-09", "Expense display-only + EC ref", c_fn09),
    ("FN-10", "gap hook display-only → แนะนำ", c_fn10),
    ("FN-11", "ยกเลิกลงทะเบียน", c_fn11),
    ("FN-12", "NTF 3 จุด", c_fn12),
    ("FN-13", "report completion + filter", c_fn13),
    ("FN-90", "search + empty state", c_fn90),
    ("FN-91", "ปิด + soft archive ผ่าน confirm", c_fn91),
    ("FN-92", "validate + double-submit guard", c_fn92),
    ("FN-93", "audit append-only", c_fn93),
    ("FN-94", "mask ตาม role", c_fn94),
    ("NEG-UNSUP", "เคสเชิงลบ unsupported ×5", c_unsupported),
    ("UI-REG", "modal เหนือ drawer (z)", c_modal_over_drawer),
    ("UI-STACK", "overlay stack สะอาด", c_overlay_stack),
    ("UI-CSS", "CSS var + layout list/drawer", c_static_css),
    ("UI-AFFORD", "affordance cursor:pointer", c_affordance),
    ("UI-FOCUS", "search focus retention", c_focus_retention),
    ("UI-ICON", "ไอคอนไม่ว่าง", c_icons),
    ("FIX-01", "บันทึกผลเฉพาะรอบ closed + completion", c_fix01),
    ("FIX-02", "สิทธิ์ hr + sendExpense/submitSession guards", c_fix02),
    ("FIX-03", "เช็คชื่อก่อนบันทึกผล + ประเมิน 1-5", c_fix03),
    ("FIX-04", "ประวัติอบรมรายคน + ชั่วโมงสะสม", c_fix04),
    ("FIX-05", "ต้นทุนต่อหัว (ไม่หารศูนย์)", c_fix05),
    ("FIX-06", "ไอคอนไม่ว่างใน modal", c_fix06),
    ("FIX-07", "combobox portal + avatar (ไม่ clip)", c_fix07),
    ("BUG-01", "การ์ดอนุมัติไม่ nest ซ้อน", c_bug01),
    ("BUG-02", "ses_course เลือกแล้ว list ปิด", c_bug02),
    ("BUG-03", "ปุ่มบันทึกผล disabled ครอบ tt-wrap (tooltip)", c_bug03),
    ("BUG-04", "modal ลงทะเบียน combobox ไม่กางเอง", c_bug04),
    ("UIKIT-PROOF", "C3.8 helper จับเวอร์ชันพังได้จริง", c_uikit_selfproof),
]

ALL_FN = ['FN-01', 'FN-02', 'FN-03', 'FN-04', 'FN-05', 'FN-06', 'FN-07', 'FN-08', 'FN-09',
          'FN-10', 'FN-11', 'FN-12', 'FN-13', 'FN-90', 'FN-91', 'FN-92', 'FN-93', 'FN-94']
FN_TOTAL = len(ALL_FN)

with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 950})
    page.set_default_timeout(6000)

    def _route(route):
        url = route.request.url
        if "lucide" in url:
            route.continue_()      # ปล่อย lucide เพื่อตรวจไอคอนว่างได้จริง (offline = fallback no-op)
        else:
            route.abort()          # กัน font/CDN อื่น เพื่อความ deterministic

    page.route("https://**", _route)
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
missing = [f for f in ALL_FN if f not in covered]
fix_ids = [r for r in suite.results if r[0].startswith("FIX-")]
bug_ids = [r for r in suite.results if r[0].startswith("BUG-")]
fix_pass = sum(1 for r in fix_ids if r[2] == "PASS")
bug_pass = sum(1 for r in bug_ids if r[2] == "PASS")
result = {
    "feature": "F-HR-TRAIN",
    "run": "re-gate (7 FIX ของ BA + 2 bug manual test)",
    "fn_covered": len(covered),
    "fn_total": FN_TOTAL,
    "fn_covered_list": covered,
    "fn_missing": missing,
    "negative_unsupported": 5,
    "fix_acceptance_passed": fix_pass,
    "fix_acceptance_total": len(fix_ids),
    "bug_regression_passed": bug_pass,
    "bug_regression_total": len(bug_ids),
    "uikit_helpers_added": ["nested_cards", "combobox_state_after_select", "assert_combobox_closes_after_select", "modal_autoopens_comboboxes"],
    "tests_passed": passed,
    "tests_total": len(CASES),
    "console_errors": suite.console_errors,
    "results": [{"ids": r[0], "name": r[1], "status": r[2], "detail": r[3]} for r in suite.results],
}
(Path(__file__).parent / "results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

print("=" * 74)
print(f"FN ครอบ {len(covered)}/{FN_TOTAL} · เคสรวม {len(CASES)} · ผ่าน {passed}/{len(CASES)} · เคสเชิงลบ unsupported 5/5")
print(f"FIX acceptance {fix_pass}/{len(fix_ids)} · BUG regression {bug_pass}/{len(bug_ids)} · console errors = {len(suite.console_errors)}")
if missing:
    print(f"  ⚠️ FN ที่ยังขาด: {missing}")
suite.report(exit_on_fail=False)
sys.exit(0 if passed == len(CASES) and not suite.console_errors else 1)
