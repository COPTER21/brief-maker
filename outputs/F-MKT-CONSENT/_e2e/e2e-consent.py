#!/usr/bin/env python3
"""E2E · F-MKT-CONSENT · ความยินยอม PDPA (F058) — WF-01 Step 5 (ตัวหนัก)

รันไทม์ตัวเดียวที่ต้องพิสูจน์ COMPLETENESS: ทุก FN-01..20 มีเคส ≥1 (ครอบ 20/20)
+ FN-40.x เชิงลบ (เรนเดอร์จริงแล้ว assert ว่า "ไม่โผล่") + DSP regression (uikit helpers).

ยึด helper ของ uikit เท่านั้น (ready/settle/after/hush) — ไม่มี wait_for_timeout, ไม่มี
ตัวตรวจ UI generic ใหม่. ขับหน้าจอผ่าน controller function จริง + real click แล้ว assert
ทั้ง data model (state.purposes/consents/requests/rz/_csq) และ DOM ที่เรนเดอร์.
reload หน้าใหม่ต่อเคส → mock state reset = เคสอิสระต่อกัน.

หมายเหตุตัววัด (บันทึกความจริง — ไม่แกล้งเขียว):
  · combobox ของฟีเจอร์นี้ใช้ระบบเอง (.combo / CB / comboPick / id cx_*) แทน searchSelect
    ของ BASE-KIT — uikit.assert_combobox_closes_after_select ผูกกับ window.__ss/ss-* จึงใช้
    ตรงไม่ได้. DSP-02 จึงตรวจด้วย (ก) uikit.modal_autoopens_comboboxes (ยืนยันไม่มี BASE-KIT
    search-select กางเอง) + (ข) ขับ comboOpen/comboPick จริงของฟีเจอร์แล้ว assert ว่าเลือกแล้ว
    ปิด (CB[key].open===false · list hidden · input โชว์ค่า) = พฤติกรรม DSP-02 เดียวกัน.
  · assert_overlay_cleared_after_close ไม่ใช้ — drawer ของฟีเจอร์นี้ปิดด้วย transform:translateX(100%)
    (เลื่อนออกนอกจอ) โดย pointer-events ยัง auto ตาม design ; helper นั้นบังคับ invariant pe:none
    ของ BASE-KIT ซึ่งไม่ตรงรูปแบบนี้ (ไม่ใช่บั๊ก — off-screen ไม่ดักคลิกกลางจอ). ใช้ ESC chain +
    JS_MODAL_UNDER_DRAWER แทน.

รัน: .claude/venv/Scripts/python.exe outputs/F-MKT-CONSENT/_e2e/e2e-consent.py [path/to/consent-pdpa.html]
"""
from pathlib import Path
import sys
import tempfile

from playwright.sync_api import sync_playwright

OUTPUTS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(OUTPUTS / "_SHARED" / "_e2e"))
from uikit import (  # noqa: E402
    Suite, ready, settle as shared_settle, after as shared_after, hush,
    assert_text_absent, assert_no_garbage_text,
    modal_autoopens_comboboxes, assert_affordances_fire,
    assert_filter_not_flush, assert_action_button_gap, assert_modal_warn_not_cramped,
    assert_double_submit_single, assert_role_write_blocked,
    JS_FILTER_FLUSH, JS_ACTION_BTN_GAP, JS_MODAL_WARN_CRAMPED,
    JS_MODAL_UNDER_DRAWER,
)

HTML = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parents[1] / "consent-pdpa.html").resolve()
BASE = HTML.as_uri()

suite = Suite("F-MKT-CONSENT · ความยินยอม PDPA")

# ── temp .txt เอกสารสำหรับ mock upload (FN-01 · FN-02) ──
# เนื้อหาความยินยอมย้ายไปเป็น "เอกสารอัปโหลด" — FileReader อ่าน readAsText ของไฟล์ .txt นี้
# แล้วเก็บลง versions[..].body (แทนฟิลด์ text เดิม) จึง assert body ได้ว่าตรงกับไฟล์ที่แนบ
_DOC_BODY = ("เอกสารความยินยอม PDPA (ทดสอบ E2E) — ยินยอมให้ส่งข้อมูลข่าวสารและโปรโมชัน"
             "ผ่านช่องทางที่เลือกไว้ตามนโยบายฉบับนี้อย่างครบถ้วน")
_DOC_TXT = Path(tempfile.gettempdir()) / "e2e-consent-upload.txt"
_DOC_TXT.write_text(_DOC_BODY, encoding="utf-8")


def settle(page, timeout=1600):
    shared_settle(page, timeout=timeout)


def after(page, js, timeout=1800):
    return shared_after(page, js, timeout=timeout)


def ev(page, js):
    return page.evaluate(js)


def open_(page):
    """เปิดหน้าใหม่ (reset mock state) แล้วรอ render จริง (#page-content มีเนื้อหา)"""
    ready(page, BASE, timeout=9000)
    page.wait_for_function(
        "() => { const p=document.getElementById('page-content'); return p && p.innerHTML.trim().length>0; }",
        timeout=9000,
    )


def page_text(page):
    return page.evaluate("() => document.getElementById('page-content').textContent")


def drawer_text(page):
    return page.evaluate("() => (document.getElementById('drawer')||{}).textContent || ''")


def modal_text(page):
    return page.evaluate("() => (document.querySelector('#modalBackdrop .modal')||{}).textContent || ''")


def toast_text(page):
    return page.evaluate("() => (document.getElementById('toast')||{}).textContent || ''")


def go_tab(page, t):
    after(page, "() => navigate('consent/%s')" % t)
    page.wait_for_function("() => state.tab==='%s'" % t, timeout=4000)


def set_persona(page, p):
    after(page, "() => { state.persona='%s'; render(); }" % p)


def wait_drawer(page, mode=None):
    page.wait_for_function("() => state.drawer.open===true", timeout=4000)
    if mode:
        page.wait_for_function("() => state.drawer.mode==='%s'" % mode, timeout=4000)


def wait_modal(page, mtype=None):
    page.wait_for_function("() => state.modal.open===true", timeout=4000)
    if mtype:
        page.wait_for_function("() => state.modal.type==='%s'" % mtype, timeout=4000)
    page.wait_for_function("() => document.getElementById('modalBackdrop').classList.contains('is-open')", timeout=4000)


def combo_pick(page, key, index):
    """เลือกค่าใน combobox ของฟีเจอร์ (comboPick controller จริง)"""
    after(page, "() => comboPick('%s',%d)" % (key, index))


def upload_doc(page, input_id, ready_js):
    """แนบเอกสารผ่าน <input type=file> ที่ซ่อนอยู่ (set_input_files) → onchange=handleDocUpload
    → FileReader อ่าน .txt เติม body (async) · รอจน ready_js เป็นจริง (doc.body มีค่า)"""
    page.set_input_files("#" + input_id, str(_DOC_TXT))
    page.wait_for_function(ready_js, timeout=5000)


def open_recipient(page):
    """คลิกปุ่ม 'เปิดมุมมองผู้รับ' (openRecipientView) ในลิ้นชักคำขอจริง แล้วรอ overlay เต็มจอเปิด
    (แทน sim ในลิ้นชักเดิมที่ถูกถอดออก — จำลองการตอบย้ายไปหน้าผู้รับ)"""
    ok = page.evaluate(
        "() => { var b=[].slice.call(document.querySelectorAll('#drawer button'))"
        ".find(function(x){return /openRecipientView/.test(x.getAttribute('onclick')||'');});"
        " if(!b) return false; b.click(); return true; }")
    assert ok, "ไม่พบปุ่ม 'เปิดมุมมองผู้รับ' ในลิ้นชักคำขอ (sim หน้าผู้รับควรโผล่เมื่อ pending/draft + เซ็นได้)"
    page.wait_for_function("() => state.recipient && state.recipient.open===true", timeout=4000)
    page.wait_for_function("() => { var el=document.getElementById('recipientRoot'); return el && el.classList.contains('is-open'); }", timeout=4000)


def rcp_choose(page, code, decision):
    """คลิกปุ่มเลือก ยินยอม/ไม่ยินยอม รายวัตถุประสงค์ในหน้าผู้รับจริง (setRecipientChoice)
    decision: 'grant' (ยินยอม) · 'decline' (ไม่ยินยอม)"""
    sel = "setRecipientChoice('%s','%s')" % (code, decision)
    ok = page.evaluate(
        "(sel) => { var el=[].slice.call(document.querySelectorAll('#recipientRoot .rcp-choice'))"
        ".find(function(x){return (x.getAttribute('onclick')||'').replace(/\\s/g,'')===sel.replace(/\\s/g,'');});"
        " if(!el) return false; el.click(); return true; }", sel)
    assert ok, "ไม่พบปุ่มเลือกในหน้าผู้รับ: " + sel
    page.wait_for_function("(a) => state.recipient.choices[a[0]]===a[1]", arg=[code, decision], timeout=4000)


def rcp_verify(page):
    """ติ๊กช่องยืนยันตัวตนในหน้าผู้รับจริง (toggleRecipientVerify)"""
    ok = page.evaluate("() => { var el=document.querySelector('#recipientRoot .rcp-verify-row'); if(!el) return false; el.click(); return true; }")
    assert ok, "ไม่พบช่องยืนยันตัวตนในหน้าผู้รับ"
    page.wait_for_function("() => state.recipient.verified===true", timeout=4000)


def rcp_submit(page):
    """คลิก 'ยืนยันการตอบ' ในหน้าผู้รับจริง (submitRecipient)"""
    ok = page.evaluate("() => { var el=document.querySelector('#recipientRoot .rcp-submit'); if(!el) return false; el.click(); return true; }")
    assert ok, "ไม่พบปุ่ม 'ยืนยันการตอบ' ในหน้าผู้รับ"


# ═══════════════════════════════ FN 01–04 · PURPOSES ═══════════════════════════════

def c_fn01(page):
    """[FN-01 · BR-05/11] สร้างวัตถุประสงค์ + แนบเอกสาร v1 (อัปโหลด) · W1: ไม่แนบเอกสารต้องถูกปฏิเสธ"""
    open_(page)
    set_persona(page, "dpo")
    n0 = ev(page, "() => state.purposes.length")
    after(page, "() => openPurCreate()")
    wait_drawer(page, "pur-create")
    after(page, "() => togglePurCh('email')")     # render() → กรอกชื่อหลัง toggle
    # ── W1 negative: ไม่แนบเอกสาร → toast 'ต้องแนบเอกสาร' + ไม่เพิ่มวัตถุประสงค์ (กฎใหม่แทนกฎ ≥40 ตัวเดิม) ──
    after(page, "() => { document.getElementById('pfName').value='ส่งข่าวสารทดสอบ'; document.getElementById('pfLife').value='24'; }")
    after(page, "() => submitPurCreate()")
    tt = toast_text(page)
    assert "ต้องแนบเอกสาร" in tt, f"W1: ไม่แนบเอกสารไม่ขึ้น toast เตือน (toast='{tt}')"
    assert ev(page, "() => state.purposes.length") == n0, "W1: ไม่แนบเอกสารแต่กลับเพิ่มวัตถุประสงค์ (ต้องถูกปฏิเสธ)"
    assert ev(page, "() => state.drawer.open") is True, "W1: ถูกปฏิเสธแล้วลิ้นชักต้องยังเปิดให้แก้"
    # ── happy: แนบเอกสาร .txt ผ่าน set_input_files → FileReader เติม body → สร้างสำเร็จ ──
    after(page, "() => { document.getElementById('pfName').value='ส่งข่าวสารทดสอบ'; document.getElementById('pfLife').value='24'; }")
    upload_doc(page, "pfDocInput", "() => state.dd && state.dd.purForm && state.dd.purForm.doc && (state.dd.purForm.doc.body||'').length>0")
    after(page, "() => submitPurCreate()")
    assert ev(page, "() => state.purposes.length") == n0 + 1, "แนบเอกสารแล้วแต่ไม่เพิ่มวัตถุประสงค์"
    newp = ev(page, "() => state.purposes[state.purposes.length-1]")
    assert newp["name"] == "ส่งข่าวสารทดสอบ" and newp["currentVer"] == 1 and newp["lifespan"] == 24, \
        f"วัตถุประสงค์ใหม่ค่าไม่ถูก: {newp}"
    v0 = newp["versions"][0]
    assert "docName" in v0 and "docType" in v0 and "body" in v0, f"เวอร์ชัน v1 ไม่ได้เก็บข้อมูลเอกสารอัปโหลด: {list(v0.keys())}"
    assert "text" not in v0, f"เวอร์ชัน v1 ยังมีเนื้อหาแบบ text-only เดิม (ต้องเป็นเอกสารอัปโหลด): {list(v0.keys())}"
    assert v0["body"] == _DOC_BODY, "เนื้อเอกสาร v1 (body) ไม่ตรงกับไฟล์ที่อัปโหลด"
    assert v0["docName"] == _DOC_TXT.name, f"ชื่อไฟล์เอกสาร v1 ไม่ตรง: {v0['docName']}"
    # เรนเดอร์บนตารางวัตถุประสงค์จริง
    go_tab(page, "purposes")
    assert "ส่งข่าวสารทดสอบ" in page_text(page), "วัตถุประสงค์ใหม่ไม่ปรากฏบนตาราง"
    return f"สร้างวัตถุประสงค์ v1 (อัปโหลดเอกสาร '{_DOC_TXT.name}' → versions[0].body) · W1 ไม่แนบเอกสารถูกปฏิเสธ (toast) · {n0}→{n0+1}"


def c_fn02(page):
    """[FN-02 · BR-05/06] แก้นโยบาย → ออกเวอร์ชันใหม่ (อัปโหลดเอกสาร) + เตือน N รายการผูกเวอร์ชันเดิม"""
    open_(page)
    set_persona(page, "dpo")
    v0 = ev(page, "() => purpose('PUR-02').currentVer")
    nver0 = ev(page, "() => purpose('PUR-02').versions.length")
    after(page, "() => openNewVersion('PUR-02')")     # ตั้ง state.nvDoc=null + เปิด modal
    wait_modal(page, "new-version")
    mt = modal_text(page)
    assert "รายการ" in mt and ("ไม่ครอบคลุม" in mt or "ต้องขอใหม่" in mt), "modal ไม่เตือน consent เวอร์ชันเดิม"
    # ── ต้องแนบเอกสารก่อน (กฎใหม่) — publish โดยไม่แนบต้องถูกปฏิเสธ ──
    after(page, "() => doPublishVersion('PUR-02')")
    assert ev(page, "() => purpose('PUR-02').currentVer") == v0, "ยังไม่แนบเอกสารแต่กลับออกเวอร์ชันใหม่ (ต้องถูกปฏิเสธ)"
    assert "ต้องแนบเอกสาร" in toast_text(page), "publish โดยไม่แนบเอกสารไม่ขึ้น toast เตือน"
    # ── แนบเอกสารเวอร์ชันใหม่ (อัปโหลด) → ออกเวอร์ชันสำเร็จ ──
    upload_doc(page, "nvDocInput", "() => state.nvDoc && (state.nvDoc.body||'').length>0")
    after(page, "() => doPublishVersion('PUR-02')")
    v1 = ev(page, "() => purpose('PUR-02').currentVer")
    assert v1 == v0 + 1, f"currentVer ไม่เพิ่ม ({v0}→{v1})"
    assert ev(page, "() => purpose('PUR-02').versions.length") == nver0 + 1, "versions ไม่ถูก append"
    nv = ev(page, "() => purpose('PUR-02').versions[purpose('PUR-02').versions.length-1]")
    assert nv["v"] == v1 and nv.get("docName") and "body" in nv, f"เวอร์ชันใหม่ไม่มีเอกสารอัปโหลด: {nv}"
    assert "text" not in nv, "เวอร์ชันใหม่ยังเป็น text-only เดิม (ต้องเป็นเอกสารอัปโหลด)"
    assert nv["body"] == _DOC_BODY, "เนื้อเอกสารเวอร์ชันใหม่ (body) ไม่ตรงกับไฟล์ที่อัปโหลด"
    stale = ev(page, "() => staleCount('PUR-02')")
    assert stale >= 1, "ออกเวอร์ชันใหม่แล้วต้องมี consent เวอร์ชันเดิมกลายเป็น stale (ไม่ครอบคลุม)"
    tt = toast_text(page)
    assert ("v" + str(v1)) in tt and "ขอความยินยอมใหม่" in tt, f"toast ไม่บอกจำนวนที่ต้องขอใหม่ (toast='{tt}')"
    return f"ออกเอกสาร v{v0}→v{v1} (อัปโหลด · ไม่แนบถูกปฏิเสธ) · {stale} รายการผูกเวอร์ชันเดิม (ไม่ครอบคลุม)"


def c_fn03(page):
    """[FN-03] ตารางวัตถุประสงค์ + สถิติ (ยินยอม/ถอน/หมดอายุ/%ครอบคลุม)"""
    open_(page)
    go_tab(page, "purposes")
    at = page_text(page)
    assert "ความครอบคลุม" in at and "%" in at, "ตารางวัตถุประสงค์ไม่มีคอลัมน์ความครอบคลุม"
    assert "PUR-01" in at and "ส่งโปรโมชันสินค้า" in at, "ไม่แสดงวัตถุประสงค์"
    # drawer สถิติ 4 ใบ
    after(page, "() => openPurView('PUR-01')")
    wait_drawer(page, "pur-view")
    dt = drawer_text(page)
    for lb in ["ยินยอมอยู่", "ถอนแล้ว", "หมดอายุ", "ความครอบคลุม"]:
        assert lb in dt, f"drawer สถิติขาด: {lb}"
    ncards = ev(page, "() => document.querySelectorAll('#drawer .stats .stat').length")
    assert ncards == 4, f"drawer ต้องมีการ์ดสถิติ 4 ใบ (ได้ {ncards})"
    return "ตารางวัตถุประสงค์ + %ครอบคลุม · drawer สถิติ 4 ใบ (ยินยอม/ถอน/หมดอายุ/coverage)"


def c_fn04(page):
    """[FN-04 · BR-14] ปิดวัตถุประสงค์ (ห้ามสร้างคำขอใหม่ · consent เดิมคงอยู่)"""
    open_(page)
    set_persona(page, "dpo")
    n_consent = ev(page, "() => state.consents.filter(function(c){return c.purpose==='PUR-01';}).length")
    after(page, "() => openModal('close-purpose',{code:'PUR-01'})")
    wait_modal(page, "close-purpose")
    after(page, "() => doClosePurpose('PUR-01')")
    assert ev(page, "() => purpose('PUR-01').status") == "closed", "ปิดวัตถุประสงค์แล้ว status ไม่ใช่ closed"
    # consent เดิมของ PUR-01 ยังอยู่เป็นหลักฐาน (ไม่ถูกลบ)
    assert ev(page, "() => state.consents.filter(function(c){return c.purpose==='PUR-01';}).length") == n_consent, \
        "ปิดวัตถุประสงค์แล้ว consent เดิมหาย (ต้องคงอยู่เป็นหลักฐาน)"
    # สร้างคำขอใหม่ไม่ได้ — PUR-01 ต้องไม่อยู่ในรายการวัตถุประสงค์ที่เลือกได้
    after(page, "() => openReqCreate({})")
    wait_drawer(page, "req-create")
    pickable = ev(page, "() => state.purposes.filter(function(p){return p.status==='active';}).map(function(p){return p.code;})")
    assert "PUR-01" not in pickable, "ปิดแล้วแต่ PUR-01 ยังเลือกสร้างคำขอได้"
    return f"ปิด PUR-01 (closed) · consent เดิม {n_consent} รายการคงอยู่ · สร้างคำขอใหม่กับ PUR-01 ไม่ได้"


# ═══════════════════════════════ FN 05–11 · REQUESTS ═══════════════════════════════

def c_fn05(page):
    """[FN-05 · BR-01/03] สร้างคำขอรายเดียว (เจ้าของ + วัตถุประสงค์ + ช่องทาง → ลิงก์ + QR) · single-screen"""
    open_(page)
    n0 = ev(page, "() => state.requests.length")
    after(page, "() => openReqCreate({})")
    wait_drawer(page, "req-create")
    # single-screen — ไม่มี stepper/wizard (FN-40.10)
    n_step = ev(page, "() => document.querySelectorAll('#drawer .stepper, #drawer .step, #drawer .stepper-item, #drawer .stepper-circle, #drawer .step-dot').length")
    assert n_step == 0, f"[FN-40.10] create-request มี stepper/wizard {n_step} จุด (ต้อง single-screen)"
    combo_pick(page, "reqSubject", 0)     # CUS-1001
    combo_pick(page, "reqChannel", 0)     # email (onSelect → render)
    after(page, "() => toggleReqPurpose('PUR-01')")   # PUR-01 รองรับ email
    after(page, "() => submitReqCreate()")
    assert ev(page, "() => state.requests.length") == n0 + 1, "สร้างคำขอแล้วจำนวนคำขอไม่เพิ่ม"
    r = ev(page, "() => state.requests[state.requests.length-1]")
    assert r["subject"] == "CUS-1001" and r["channel"] == "email", f"คำขอค่าไม่ถูก: {r}"
    assert "PUR-01" in r["purposes"], "คำขอไม่มีวัตถุประสงค์ที่เลือก"
    assert r["link"] and "REQ-" in r["link"], "คำขอไม่มีลิงก์"
    # เปิดดู → มี QR + ลิงก์
    after(page, "() => openReqView(%r)" % r["id"])
    wait_drawer(page, "req-view")
    dt = drawer_text(page)
    assert "ลิงก์และคิวอาร์" in dt, "reqView ไม่มีส่วนลิงก์/QR"
    assert ev(page, "() => document.querySelectorAll('#drawer .qr-img svg').length") == 1, "ไม่มี QR svg"
    return f"สร้างคำขอ {r['id']} single-screen (ไม่มี stepper) · subject/channel/purpose + ลิงก์ + QR"


def c_fn06(page):
    """[FN-06 · BR-07] ส่งคำขอทางอีเมล (บันทึกเวลา · สถานะ→รอตอบ)"""
    open_(page)
    # REQ-2602 = draft ยังไม่ส่ง
    after(page, "() => openReqView('REQ-2602')")
    wait_drawer(page, "req-view")
    s0 = ev(page, "() => request('REQ-2602').sends.length")
    assert ev(page, "() => request('REQ-2602').status") == "draft", "seed REQ-2602 ต้องเป็น draft"
    after(page, "() => sendVia('REQ-2602','line')")
    assert ev(page, "() => request('REQ-2602').sends.length") == s0 + 1, "ส่งแล้วไม่บันทึกการส่ง"
    last = ev(page, "() => request('REQ-2602').sends[request('REQ-2602').sends.length-1]")
    assert last["ch"] == "line" and last["at"], "การส่งไม่บันทึกช่องทาง/เวลา"
    assert ev(page, "() => request('REQ-2602').status") == "pending", "ส่งแล้วสถานะไม่เปลี่ยนเป็นรอตอบ"
    assert "จำลอง" in toast_text(page), "ไม่มี toast จำลองการส่ง"
    return "ส่งคำขอ (บันทึกช่องทาง+เวลา · draft→รอตอบ · toast จำลอง ไม่ส่งจริง)"


def c_fn07(page):
    """[FN-07 · BR-18] ส่งซ้ำช่องทางอื่น = การส่งครั้งที่ N ในคำขอเดิม (ไม่สร้างคำขอใหม่)"""
    open_(page)
    nr0 = ev(page, "() => state.requests.length")
    # REQ-2601 pending มีส่งแล้ว 1 ครั้ง (email)
    after(page, "() => openReqView('REQ-2601')")
    wait_drawer(page, "req-view")
    s0 = ev(page, "() => request('REQ-2601').sends.length")
    combo_pick(page, "resendCh", 2)      # line
    after(page, "() => resendOther('REQ-2601')")
    assert ev(page, "() => state.requests.length") == nr0, "ส่งซ้ำแล้วกลับสร้างคำขอใหม่ (ต้องเป็นคำขอเดิม)"
    assert ev(page, "() => request('REQ-2601').sends.length") == s0 + 1, "ส่งซ้ำไม่บันทึกเป็นการส่งครั้งถัดไป"
    assert ev(page, "() => request('REQ-2601').sends[request('REQ-2601').sends.length-1].ch") == "line", \
        "การส่งครั้งใหม่ไม่ใช่ช่องทางที่เลือก"
    return f"ส่งซ้ำช่องทางอื่น = ครั้งที่ {s0+1} ในคำขอเดิม REQ-2601 (คำขอไม่เพิ่ม)"


def c_fn08(page):
    """[FN-08] ดาวน์โหลด QR (บันทึกการนำลิงก์ออก)"""
    open_(page)
    # ดัก downloadBlob (headless ดาวน์โหลดไม่ได้) — พิสูจน์ว่าเรียกจริง + บันทึก export
    after(page, "() => { window.__blob=null; window.downloadBlob=function(n,m,c){window.__blob={name:n,mime:m,content:c};}; }")
    s0 = ev(page, "() => request('REQ-2601').sends.length")
    after(page, "() => downloadQR('REQ-2601')")
    assert ev(page, "() => window.__blob && window.__blob.name") and "REQ-2601" in ev(page, "() => window.__blob.name"), \
        "downloadQR ไม่สร้างไฟล์ QR"
    exp = ev(page, "() => request('REQ-2601').sends.filter(function(x){return x.ch==='export-qr';}).length")
    assert exp >= 1, "ดาวน์โหลด QR แล้วไม่บันทึกการนำลิงก์ออก (export-qr)"
    assert ev(page, "() => request('REQ-2601').sends.length") == s0 + 1, "การนำ QR ออกไม่ถูกบันทึกเป็นเหตุการณ์"
    return "ดาวน์โหลด QR สร้างไฟล์ svg + บันทึกการนำลิงก์ออก (export-qr)"


def c_fn09(page):
    """[FN-09] ดาวน์โหลดเอกสาร (อ้างชื่อเอกสารเวอร์ชันปัจจุบันของทุกวัตถุประสงค์ในคำขอ)"""
    open_(page)
    after(page, "() => downloadPdfForm('REQ-2601')")   # PUR-01(v2) + PUR-02(v1)
    tt = toast_text(page)
    assert "ต้นแบบ" in tt, f"downloadPdfForm ไม่แจ้งดาวน์โหลดเอกสาร (toast='{tt}')"
    # ต้องอ้างชื่อเอกสาร 'เวอร์ชันปัจจุบัน' — PUR-01 = v2 · PUR-02 = v1 (curDoc ของแต่ละวัตถุประสงค์)
    assert "นโยบาย-PUR-01-v2.pdf" in tt, f"ไม่ได้อ้างเอกสารเวอร์ชันปัจจุบัน (v2) ของ PUR-01 (toast='{tt}')"
    assert "นโยบาย-PUR-02-v1.pdf" in tt, f"ไม่ได้อ้างเอกสารเวอร์ชันปัจจุบัน (v1) ของ PUR-02 (toast='{tt}')"
    return "ดาวน์โหลดเอกสาร (ต้นแบบ) อ้างเอกสารเวอร์ชันปัจจุบันของทุกวัตถุประสงค์ในคำขอ (PUR-01 v2 · PUR-02 v1)"


def c_fn10(page):
    """[FN-10 · BR-15] เจ้าของข้อมูลเซ็นผ่าน 'มุมมองผู้รับ' → 'ตอบแล้ว' + สร้างทะเบียน + หลักฐาน 5 อย่าง (ผูกเวอร์ชันเอกสาร)"""
    open_(page)
    n0 = ev(page, "() => state.consents.length")
    # REQ-2602 (draft · CUS-1008 · PUR-01) → officer เซ็นได้ → เปิดมุมมองผู้รับ (overlay) → ยินยอมทุกข้อ → ยืนยันตัวตน → ยืนยันการตอบ
    after(page, "() => openReqView('REQ-2602')")
    wait_drawer(page, "req-view")
    open_recipient(page)
    codes = ev(page, "() => request('REQ-2602').purposes.slice()")
    for code in codes:
        rcp_choose(page, code, "grant")
    rcp_verify(page)
    rcp_submit(page)
    page.wait_for_function("() => request('REQ-2602').status==='answered'", timeout=4000)
    page.wait_for_function("() => !state.recipient.open", timeout=4000)
    assert ev(page, "() => document.getElementById('recipientRoot').classList.contains('is-open')") is False, \
        "ส่งคำตอบแล้ว overlay ผู้รับต้องปิด"
    assert ev(page, "() => request('REQ-2602').status") == "answered", "เซ็นแล้วคำขอไม่เป็น 'ตอบแล้ว'"
    assert ev(page, "() => state.consents.length") > n0, "เซ็นแล้วไม่สร้างรายการในทะเบียน"
    c = ev(page, "() => state.consents.filter(function(x){return x.subject==='CUS-1008' && x.purpose==='PUR-01';}).slice(-1)[0]")
    assert c and c["status"] == "granted", "ไม่มีความยินยอมที่ได้รับสำหรับคู่นี้"
    last = ev(page, "() => state.consents.filter(function(x){return x.subject==='CUS-1008';}).slice(-1)[0]")
    ekeys = list(last["evidence"].keys())
    for k in ["answeredAt", "requestChannel", "idMethod", "policyVersion", "ipDevice"]:
        assert k in ekeys, f"หลักฐานขาดฟิลด์: {k} (ได้ {ekeys})"
    assert len(ekeys) == 5, f"หลักฐานต้องครบ 5 อย่าง (ได้ {len(ekeys)})"
    # หลักฐานผูกกับเวอร์ชันเอกสารที่เซ็น (policyVersion = currentVer ปัจจุบันของ PUR-01)
    assert last["evidence"]["policyVersion"] == ev(page, "() => purpose('PUR-01').currentVer"), \
        "หลักฐานไม่ผูกกับเวอร์ชันเอกสารปัจจุบันที่เซ็น"
    return "เซ็นผ่านมุมมองผู้รับ (recipient view) → 'ตอบแล้ว' + สร้างทะเบียน + หลักฐาน 5 อย่าง (ผูกเวอร์ชันเอกสาร)"


def c_fn11(page):
    """[FN-11 · BR-01] ยินยอมบางวัตถุประสงค์ผ่านมุมมองผู้รับ (ยินยอม 1 · ไม่ยินยอม 1 · บันทึกแยกรายข้อ ไม่ใช่ทั้งก้อน)"""
    open_(page)
    # REQ-2601 = 2 วัตถุประสงค์ (PUR-01, PUR-02) · CUS-1007 — เลือกยินยอม PUR-01 · ไม่ยินยอม PUR-02 ในหน้าผู้รับจริง
    after(page, "() => openReqView('REQ-2601')")
    wait_drawer(page, "req-view")
    open_recipient(page)
    rcp_choose(page, "PUR-01", "grant")
    rcp_choose(page, "PUR-02", "decline")
    rcp_verify(page)
    rcp_submit(page)
    page.wait_for_function("() => request('REQ-2601').status==='answered'", timeout=4000)
    recs = ev(page, "() => state.consents.filter(function(x){return x.subject==='CUS-1007';})")
    statuses = {}
    for r in recs:
        statuses[r["purpose"]] = statuses.get(r["purpose"], r["status"])
    assert "PUR-01" in statuses and "PUR-02" in statuses, f"ยินยอมบางข้อไม่บันทึกแยกรายวัตถุประสงค์: {statuses}"
    assert statuses["PUR-01"] == "granted" and statuses["PUR-02"] == "declined", \
        f"partial ต้องได้ PUR-01=granted · PUR-02=declined แยกรายข้อ (ได้ {statuses})"
    return f"ยินยอมบางข้อผ่านมุมมองผู้รับ: บันทึกแยกรายวัตถุประสงค์ {statuses} (ไม่ใช่ทั้งก้อน)"


# ═══════════════════════════════ FN 12–18 · REGISTRY / CONSENT ═══════════════════════════════

def c_fn12(page):
    """[FN-12 · BR-15] ดูหลักฐาน 1 รายการ (เวลา·ช่องทาง·ยืนยันตัวตน·เวอร์ชัน·IP/อุปกรณ์)"""
    open_(page)
    after(page, "() => openConsentView('CNS-5001')")   # granted + evidence
    wait_drawer(page, "consent-view")
    dt = drawer_text(page)
    assert "หลักฐาน 5 อย่าง" in dt, "drawer ไม่มีบล็อกหลักฐาน 5 อย่าง"
    nitems = ev(page, "() => document.querySelectorAll('#drawer .ev-item').length")
    assert nitems == 5, f"ต้องมีหลักฐาน 5 รายการ (ได้ {nitems})"
    for lb in ["เวลาที่ตอบ", "ช่องทางที่ส่งคำขอ", "วิธียืนยันตัวตน", "เวอร์ชันนโยบาย", "ไอพีและอุปกรณ์"]:
        assert lb in dt, f"หลักฐานขาดหัวข้อ: {lb}"
    return "หลักฐาน 1 รายการ: 5 ช่อง (เวลา/ช่องทาง/ยืนยันตัวตน/เวอร์ชันนโยบาย/IP+อุปกรณ์)"


def c_fn13(page):
    """[FN-13 · BR-07] ทะเบียนทั้งหมด (เจ้าของ×วัตถุประสงค์×ช่องทาง + สถานะ + หมดอายุ · กรองทุกมิติ)"""
    open_(page)
    go_tab(page, "registry")
    total = ev(page, "() => filteredConsents().length")
    assert total == ev(page, "() => state.consents.length"), "ทะเบียนไม่ได้แสดงทุกรายการตอนไม่มีตัวกรอง"
    assert ev(page, "() => document.querySelectorAll('#regRows tr').length") >= 1, "ตารางทะเบียนว่าง"
    # กรองช่องทาง email
    after(page, "() => setFilter('channel','email')")
    n_email = ev(page, "() => filteredConsents().length")
    assert 0 < n_email < total, f"กรองช่องทางไม่ลดผลลัพธ์ ({n_email}/{total})"
    assert ev(page, "() => filteredConsents().every(function(c){return c.channel==='email';})"), "กรอง email แล้วยังมีช่องทางอื่น"
    # กรองวัตถุประสงค์เพิ่ม
    after(page, "() => setFilter('purpose','PUR-01')")
    assert ev(page, "() => filteredConsents().every(function(c){return c.channel==='email' && c.purpose==='PUR-01';})"), \
        "กรองหลายมิติพร้อมกันไม่ทำงาน"
    # กรองสถานะ
    after(page, "() => { resetFilters(); setFilter('status','withdrawn'); }")
    assert ev(page, "() => filteredConsents().every(function(c){return effStatus(c)==='withdrawn';})"), "กรองสถานะไม่ทำงาน"
    after(page, "() => resetFilters()")
    assert ev(page, "() => filteredConsents().length") == total, "ล้างตัวกรองแล้วไม่กลับเป็นทั้งหมด"
    return f"ทะเบียน {total} รายการ · กรองช่องทาง/วัตถุประสงค์/สถานะ (ทุกมิติ) + ล้างตัวกรอง"


def c_fn14(page):
    """[FN-14 · E1] ดู consent ของลูกค้ารายหนึ่งในที่เดียว (Customer 360)"""
    open_(page)
    after(page, "() => openC360('CUS-1001')")     # CNS-5001(email) + CNS-5002(sms) · PUR-01
    wait_drawer(page, "c360")
    dt = drawer_text(page)
    assert "นายสมชาย รักดี" in dt, "C360 ไม่แสดงชื่อลูกค้า"
    ngrp = ev(page, "() => document.querySelectorAll('#drawer .c360-grp').length")
    nrow = ev(page, "() => document.querySelectorAll('#drawer .c360-row').length")
    assert ngrp >= 1 and nrow == 2, f"C360 ควรรวม consent ของลูกค้าในที่เดียว (grp {ngrp} · row {nrow}, คาด 2)"
    assert "ส่งโปรโมชันสินค้า" in dt, "C360 ไม่จัดกลุ่มตามวัตถุประสงค์"
    return f"Customer 360: รวม consent ของ CUS-1001 ({nrow} รายการ ต่างช่องทาง) จัดกลุ่มตามวัตถุประสงค์"


def c_fn15(page):
    """[FN-15 · BR-09/10] ถอนแทนลูกค้า (เหตุผล + ช่องทาง · มีผลทันที · ไม่ต้องอนุมัติ)"""
    open_(page)
    after(page, "() => openConsentView('CNS-5001')")   # granted
    wait_drawer(page, "consent-view")
    after(page, "() => openModal('withdraw',{id:'CNS-5001'})")
    wait_modal(page, "withdraw")
    assert "ไม่ต้องผ่านการอนุมัติ" in modal_text(page), "modal ถอนไม่สื่อว่ามีผลทันที (ไม่ผ่านอนุมัติ)"
    after(page, "() => { document.getElementById('wdReason').value='ลูกค้าไม่ประสงค์รับข้อความส่งเสริมการขาย'; }")
    combo_pick(page, "wdVia", 3)      # phone
    after(page, "() => doWithdraw('CNS-5001')")
    c = ev(page, "() => state.consents.find(function(x){return x.id==='CNS-5001';})")
    assert c["status"] == "withdrawn", "ถอนแล้วสถานะไม่เป็น withdrawn ทันที"
    last = ev(page, "() => { var c=state.consents.find(function(x){return x.id==='CNS-5001';}); return c.history[c.history.length-1]; }")
    assert last["action"] == "withdrawn" and last.get("reason") and last.get("via"), \
        f"ประวัติการถอนไม่บันทึกเหตุผล/ช่องทาง: {last}"
    return "ถอนแทนลูกค้า: เหตุผล+ช่องทาง · มีผลทันที (ไม่ผ่านอนุมัติ) · บันทึกในประวัติ"


def c_fn16(page):
    """[FN-16 · BR-12] รายการใกล้หมดอายุ ≤30 วัน (เตือน ไม่บล็อก · ต่ออายุได้)"""
    open_(page)
    go_tab(page, "registry")
    near = ev(page, "() => state.consents.filter(nearExpiry).length")
    assert near >= 1, "ไม่มีรายการใกล้หมดอายุใน seed (ต้องมีอย่างน้อย 1)"
    # stat filter 'ใกล้หมดอายุ'
    after(page, "() => setFilter('status','near')")
    assert ev(page, "() => filteredConsents().length") == near and ev(page, "() => filteredConsents().every(nearExpiry)"), \
        "กรองใกล้หมดอายุไม่ตรง"
    # เปิดรายการใกล้หมดอายุ → มีปุ่มต่ออายุ (เตือน ไม่บล็อก)
    cid = ev(page, "() => state.consents.filter(nearExpiry)[0].id")
    after(page, "() => resetFilters()")
    after(page, "() => openConsentView(%r)" % cid)
    wait_drawer(page, "consent-view")
    assert "สร้างคำขอต่ออายุ" in drawer_text(page), "รายการใกล้หมดอายุไม่มีปุ่มต่ออายุ"
    return f"ใกล้หมดอายุ ≤30 วัน: {near} รายการ · กรองได้ · เปิดแล้วมีปุ่มต่ออายุ (เตือน ไม่บล็อก)"


def c_fn17(page):
    """[FN-17 · BR-13] ต่ออายุ = คำขอใหม่อ้างรายการเดิม (ไม่แก้วันหมดอายุเดิม)"""
    open_(page)
    exp0 = ev(page, "() => state.consents.find(function(x){return x.id==='CNS-5007';}).expiresAt")   # expired
    n0 = ev(page, "() => state.requests.length")
    after(page, "() => openRenew('CNS-5007')")         # close → setTimeout openReqCreate(refOld)
    wait_drawer(page, "req-create")
    assert ev(page, "() => state.reqForm.refOld") == "CNS-5007", "ต่ออายุไม่อ้างรายการเดิม (refOld)"
    after(page, "() => submitReqCreate()")
    assert ev(page, "() => state.requests.length") == n0 + 1, "ต่ออายุไม่สร้างคำขอใหม่"
    r = ev(page, "() => state.requests[state.requests.length-1]")
    assert r["refOld"] == "CNS-5007", f"คำขอต่ออายุไม่ผูก refOld: {r}"
    exp1 = ev(page, "() => state.consents.find(function(x){return x.id==='CNS-5007';}).expiresAt")
    assert exp1 == exp0, "ต่ออายุแล้วไปแก้วันหมดอายุของรายการเดิม (ต้องไม่แก้)"
    return f"ต่ออายุ = คำขอใหม่ {r['id']} อ้าง CNS-5007 · วันหมดอายุเดิมไม่ถูกแก้"


def c_fn18(page):
    """[FN-18 · BR-16] ประวัติ 1 รายการ (timeline append-only + เหตุผลทุกครั้ง)"""
    open_(page)
    after(page, "() => openConsentView('CNS-5004')")   # withdrawn (มี requested/granted/withdrawn+reason)
    wait_drawer(page, "consent-view")
    dt = drawer_text(page)
    assert "เพิ่มอย่างเดียว" in dt, "drawer ไม่ระบุประวัติแบบ append-only"
    nitems = ev(page, "() => document.querySelectorAll('#drawer .timeline .tl-item').length")
    assert nitems >= 3, f"timeline ควรมี ≥3 เหตุการณ์ (ได้ {nitems})"
    assert "เหตุผล" in dt and "ไม่ประสงค์รับข้อความ" in dt, "ประวัติการถอนไม่แสดงเหตุผล"
    # ไม่มีปุ่มแก้/ลบในบล็อก timeline (append-only)
    nmut = ev(page, "() => document.querySelectorAll('#drawer .timeline button, #drawer .timeline [onclick]').length")
    assert nmut == 0, f"timeline มีปุ่มแก้/ลบ {nmut} (ต้อง append-only)"
    return f"ประวัติ append-only: {nitems} เหตุการณ์ + เหตุผล · ไม่มีปุ่มแก้/ลบ"


# ═══════════════════════════════ FN 19–20 · RESOLVE ═══════════════════════════════

def c_fn19(page):
    """[FN-19 · BR-19/20] ตัวจำลอง /consent/resolve (allowed + เหตุผล + JSON ล็อกฟิลด์ + HTTP 200)"""
    open_(page)
    go_tab(page, "resolve")
    combo_pick(page, "rzSubject", 0)     # CUS-1001
    combo_pick(page, "rzPurpose", 0)     # PUR-01
    combo_pick(page, "rzChannel", 0)     # email → CNS-5001 granted v2 (ปัจจุบัน) = ส่งได้
    after(page, "() => runResolve()")
    r = ev(page, "() => state.rz.result")
    assert r and r["allowed"] is True and r["status"] == "granted", f"resolve คู่ที่ยินยอมควร allowed=true: {r}"
    at = page_text(page)
    assert "ส่งได้" in at and "HTTP 200" in at, "ไม่แสดง verdict/HTTP 200"
    jtxt = ev(page, "() => (document.querySelector('.rz-json')||{}).textContent || ''")
    for f in ['"allowed"', '"status"', '"policy_version"', '"expires_at"', '"found"', '"reason"']:
        assert f in jtxt, f"JSON ผลลัพธ์ขาดฟิลด์ล็อก: {f}"
    assert '"allowed": true' in jtxt, f"JSON ไม่โชว์ allowed=true: {jtxt[:120]}"
    return "resolve คู่ที่ยินยอม → ส่งได้ · HTTP 200 · JSON ล็อกฟิลด์ (allowed/status/policy_version/...)"


def c_fn20(page):
    """[FN-20 · BR-04/08/19] คนไม่เคยถูกขอ → allowed:false · status:'never_asked' (ไม่ใช่ 404 / ไม่ใช่ 'ไม่ยินยอม')"""
    open_(page)
    # ยืนยันที่แกนกลางก่อน
    r = ev(page, "() => resolveConsent('CUS-1001','PUR-03','phone')")   # ไม่มีคู่นี้ในทะเบียน
    assert r["allowed"] is False and r["status"] == "never_asked" and r["found"] is False, \
        f"never_asked contract ผิด: {r}"
    # เรนเดอร์จริงบนจอ → JSON string ต้องเป็น never_asked (ไม่ใช่ declined/404) + HTTP 200
    go_tab(page, "resolve")
    combo_pick(page, "rzSubject", 0)     # CUS-1001
    combo_pick(page, "rzPurpose", 2)     # PUR-03
    combo_pick(page, "rzChannel", 3)     # phone
    after(page, "() => runResolve()")
    at = page_text(page)
    assert "ส่งไม่ได้" in at and "HTTP 200" in at, "never_asked ต้องตอบ ส่งไม่ได้ + HTTP 200 (ไม่ใช่ error)"
    jtxt = ev(page, "() => (document.querySelector('.rz-json')||{}).textContent || ''")
    assert '"status": "never_asked"' in jtxt, f"JSON status ไม่ใช่ never_asked: {jtxt[:160]}"
    assert '"allowed": false' in jtxt, "JSON allowed ไม่ใช่ false"
    assert "ไม่ยินยอม" not in at.replace("ค่าเริ่มต้นคือส่งไม่ได้", ""), "never_asked ถูกแสดงเป็น 'ไม่ยินยอม' (ผิด)"
    return "never_asked: allowed=false · status='never_asked' · HTTP 200 (ไม่ใช่ 404/ไม่ยินยอม)"


# ═══════════════════════════════ FN-40 NEGATIVE (render → assert absent) ═══════════════════════════════

def c_neg40_10(page):
    """[FN-40.10] สร้างคำขอ = single-screen — ไม่มี stepper/wizard Pattern-Q 5 ขั้น"""
    open_(page)
    after(page, "() => openReqCreate({})")
    wait_drawer(page, "req-create")
    n = ev(page, "() => document.querySelectorAll('#drawer .stepper, #drawer .step, #drawer .stepper-item, #drawer .stepper-circle, #drawer .step-dot, #drawer .stepper-label').length")
    assert n == 0, f"[40.10] create-request มี stepper/wizard {n} จุด"
    # ไม่มีปุ่ม 'ถัดไป/ย้อนกลับ' แบบ wizard
    assert_text_absent(page, ["ขั้นที่ 1", "ขั้นตอนที่", "ถัดไป →"], scope="#drawer")
    return "create-request single-screen: 0 stepper/step-band · ไม่มี wizard Pattern-Q"


def c_neg40_pipes(page):
    """[FN-40.5/40.6] ไม่มีการ์ดผล 7 ท่อ CSQ / OC·DC·SC บนจอ · emitConsequence = declare-only (เรนเดอร์ NOTHING)"""
    open_(page)
    # กระตุ้น emitConsequence จริง (grant) แล้วยืนยันว่าไม่มี pipe UI โผล่
    after(page, "() => answerRequest('REQ-2602','all')")
    assert ev(page, "() => Array.isArray(state._csq) && state._csq.length>=1"), "emitConsequence ควรผลัก envelope เข้า sink (declare-only)"
    npipe = ev(page, "() => document.querySelectorAll('[class*=pipe],[class*=csq],[class*=consequence],.pipe-card').length")
    assert npipe == 0, f"[40.5/40.6] มี element ท่อ CSQ บนจอ {npipe} (ต้องเป็น declare-only)"
    # เดินทุกแท็บ + เปิด consent view แล้วยังต้องไม่มีข้อความการ์ดผล 7 ท่อ
    for t in ("registry", "requests", "purposes", "resolve"):
        go_tab(page, t)
        assert_text_absent(page, ["7 ท่อ", "ท่อผลกระทบ", "ผลรายท่อ", "Consequence Engine"], scope="#page-content")
    return "CSQ declare-only: state._csq มี envelope แต่ 0 pipe-card / 0 OC·DC·SC UI บนทุกจอ"


def c_neg40_value(page):
    """[FN-40.4] ไม่มีคอลัมน์มูลค่า/จำนวนเงิน/เก็บผลรายท่อ"""
    open_(page)
    for t in ("registry", "requests", "purposes"):
        go_tab(page, t)
        assert_text_absent(page, ["มูลค่า", "จำนวนเงิน", "ยอดเงิน", "บาท"], scope="#page-content")
    return "ไม่มีคอลัมน์มูลค่า/จำนวนเงิน/บาท ในทะเบียน/คำขอ/วัตถุประสงค์"


def c_neg40_cookie(page):
    """[FN-40.1] ไม่มี cookie consent บนเว็บ"""
    open_(page)
    assert ev(page, "() => document.querySelectorAll('[class*=cookie],[id*=cookie]').length") == 0, "พบ element cookie-consent"
    for t in ("registry", "requests", "purposes", "resolve"):
        go_tab(page, t)
        assert_text_absent(page, ["คุกกี้", "cookie", "Cookie"], scope="#page-content")
    return "ไม่มี cookie-consent (element/ข้อความ) บนทุกจอ"


def c_neg40_approval(page):
    """[FN-40.2] ไม่มีสายอนุมัติ/slot-picker ก่อนส่งคำขอ (สายส่งตรง ไม่มีปุ่ม/สถานะอนุมัติ)"""
    open_(page)
    # create-request path
    after(page, "() => openReqCreate({})")
    wait_drawer(page, "req-create")
    n1 = ev(page, "() => document.querySelectorAll('#drawer [class*=approval],#drawer [class*=slot-pick],#drawer .doa,#drawer .approval-chain,#drawer .stepper').length")
    assert n1 == 0, f"[40.2] create-request มี UI สายอนุมัติ/slot {n1}"
    assert_text_absent(page, ["สายอนุมัติ", "ผู้อนุมัติลำดับ", "ส่งเพื่ออนุมัติ", "รออนุมัติ"], scope="#drawer")
    # request view (สายส่ง) — ไม่มีปุ่มขออนุมัติก่อนส่ง
    after(page, "() => { closeDrawer(); }")
    after(page, "() => openReqView('REQ-2602')")
    wait_drawer(page, "req-view")
    assert_text_absent(page, ["สายอนุมัติ", "ส่งเพื่ออนุมัติ", "รออนุมัติ"], scope="#drawer")
    return "ส่งคำขอ = ส่งตรง (สร้างลิงก์ทันที) · ไม่มี slot-picker/สายอนุมัติ/สถานะรออนุมัติ"


def c_neg40_lapsed(page):
    """[FN-40.8] คำขอหมดอายุ/รอตอบ ต้องแสดง 'หมดอายุ/รอตอบ' ไม่ใช่ 'ไม่ยินยอม'"""
    open_(page)
    go_tab(page, "requests")
    at = page_text(page)
    assert "รอตอบ" in at, "คำขอ pending ต้องแสดง 'รอตอบ'"
    assert "คำขอหมดอายุ" in at, "คำขอ expired ต้องแสดง 'คำขอหมดอายุ'"
    # หน้าคำขอ (สถานะคำขอ) ต้องไม่มีคำว่า 'ไม่ยินยอม' — การไม่ตอบ ≠ ปฏิเสธ
    assert "ไม่ยินยอม" not in at, "[40.8] คำขอที่ยังไม่ตอบ/หมดอายุ ถูกป้ายเป็น 'ไม่ยินยอม' (ผิด)"
    # ยืนยันที่ vocabulary
    assert ev(page, "() => reqStatusPill('expired')[0]") == "คำขอหมดอายุ", "reqStatusPill expired ผิด"
    assert ev(page, "() => reqStatusPill('pending')[0]") == "รอตอบ", "reqStatusPill pending ผิด"
    return "lapsed/no-answer = 'คำขอหมดอายุ'/'รอตอบ' (ไม่ใช่ 'ไม่ยินยอม')"


def c_neg40_triple(page):
    """[FN-40.7] โมเดล subject×purpose×channel — ถอน 1 คู่ ไม่กระทบคู่อื่นของคนเดียวกัน (ไม่ใช่ธงเดียว)"""
    open_(page)
    # CUS-1001 มี PUR-01/email (CNS-5001) และ PUR-01/sms (CNS-5002) — ทั้งคู่ granted
    assert ev(page, "() => effStatus(state.consents.find(function(x){return x.id==='CNS-5002';}))") == "granted", "seed CNS-5002 ต้อง granted"
    after(page, "() => openConsentView('CNS-5001')")
    wait_drawer(page, "consent-view")
    after(page, "() => openModal('withdraw',{id:'CNS-5001'})")
    wait_modal(page, "withdraw")
    after(page, "() => { document.getElementById('wdReason').value='ทดสอบถอนคู่เดียว'; }")
    combo_pick(page, "wdVia", 0)
    after(page, "() => doWithdraw('CNS-5001')")
    assert ev(page, "() => state.consents.find(function(x){return x.id==='CNS-5001';}).status") == "withdrawn", "CNS-5001 ไม่ถูกถอน"
    # คู่อื่น (PUR-01/sms) ของคนเดียวกันต้องยัง granted
    assert ev(page, "() => effStatus(state.consents.find(function(x){return x.id==='CNS-5002';}))") == "granted", \
        "[40.7] ถอน email แล้ว sms ของคนเดียวกันถูกถอนตาม (ต้องเป็นธง 3 มิติ ไม่ใช่ธงเดียว)"
    return "ถอน CUS-1001·PUR-01·email แล้ว คู่ PUR-01·sms ยัง granted (โมเดล subject×purpose×channel)"


# ═══════════════════════════════ DSP REGRESSION (uikit helpers · C3.8) ═══════════════════════════════

def c_dsp01_modal_over_drawer(page):
    """[DSP-01] modal (ถอน) เปิดจากในลิ้นชัก → JS_MODAL_UNDER_DRAWER ต้องว่าง (modal z > drawer z)"""
    open_(page)
    after(page, "() => openConsentView('CNS-5001')")
    wait_drawer(page, "consent-view")
    after(page, "() => openModal('withdraw',{id:'CNS-5001'})")
    wait_modal(page, "withdraw")
    under = ev(page, JS_MODAL_UNDER_DRAWER)
    assert not under, f"[DSP-01] modal ถอนจมใต้ drawer: {under}"
    # ยืนยัน z จริง
    mz = ev(page, "() => parseInt(getComputedStyle(document.getElementById('modalBackdrop')).zIndex,10)")
    dz = ev(page, "() => parseInt(getComputedStyle(document.getElementById('drawer')).zIndex,10)")
    assert mz > dz, f"[DSP-01] modal z ({mz}) ต้อง > drawer z ({dz})"
    return f"DSP-01: modal ถอนลอยเหนือลิ้นชัก (modal z={mz} > drawer z={dz}) · JS_MODAL_UNDER_DRAWER ว่าง"


def c_dsp02_combobox(page):
    """[DSP-02] เลือกแล้วปิด (ไม่เด้งกางใหม่) + ไม่กางเองตอน overlay เปิด (no-autoopen)"""
    open_(page)
    # (ก) uikit.modal_autoopens_comboboxes บน modal ถอน — ยืนยันไม่มี BASE-KIT search-select กางเอง
    after(page, "() => openConsentView('CNS-5001')")
    wait_drawer(page, "consent-view")
    after(page, "() => openModal('withdraw',{id:'CNS-5001'})")
    wait_modal(page, "withdraw")
    auto = modal_autoopens_comboboxes(page)
    assert auto == [], f"[DSP-02] BASE-KIT search-select กางเองตอน modal เปิด: {auto}"
    # (ข) combobox ของฟีเจอร์ (.combo/CB) — ไม่กางเองตอน modal/drawer เพิ่งเปิด
    def combo_open_flags():
        return ev(page, "() => Object.keys(CB).filter(function(k){return CB[k] && CB[k].open;})")
    assert combo_open_flags() == [], f"[DSP-02] .combo ของฟีเจอร์กางเองตอน overlay เปิด: {combo_open_flags()}"
    # (ค) เลือกแล้วต้องปิด (close-on-select) — ขับ comboOpen→comboPick จริงบน wdVia
    after(page, "() => comboOpen('wdVia')")
    assert ev(page, "() => CB['wdVia'].open") is True, "comboOpen แล้ว open ไม่ true"
    assert ev(page, "() => !document.getElementById('cx_wdVia_list').classList.contains('hidden')"), "เปิดแล้ว list ยัง hidden"
    after(page, "() => comboPick('wdVia',0)")
    assert ev(page, "() => CB['wdVia'].open") is False, "[DSP-02] เลือกแล้ว open ยัง true (reopen-after-select)"
    assert ev(page, "() => document.getElementById('cx_wdVia_list').classList.contains('hidden')"), "[DSP-02] เลือกแล้ว list ยังไม่ปิด"
    assert ev(page, "() => (document.getElementById('cx_wdVia_in')||{}).value") , "[DSP-02] เลือกแล้วช่องไม่โชว์ค่า"
    # (ง) รวมถึง resolve tab combobox (subject picker)
    after(page, "() => { closeModal(); closeDrawer(); }")
    go_tab(page, "resolve")
    assert ev(page, "() => Object.keys(CB).filter(function(k){return CB[k]&&CB[k].open;}).length") == 0, "resolve combos กางเองตอนเข้าแท็บ"
    after(page, "() => comboOpen('rzSubject')")
    after(page, "() => comboPick('rzSubject',0)")
    assert ev(page, "() => CB['rzSubject'].open") is False and ev(page, "() => state.rz.subject") == "CUS-1001", \
        "[DSP-02] subject picker เลือกแล้วไม่ปิด/ไม่ติดค่า"
    return "DSP-02: no-autoopen (modal_autoopens_comboboxes=[] + CB flags=[]) · เลือกแล้วปิด (wdVia+rzSubject)"


def c_dsp04_affordances(page):
    """[DSP-04 · C3.8] ปุ่ม 'เปิดมุมมองผู้รับ' + choice/verify/submit ของหน้าผู้รับ + persona + แถวทะเบียน + แท็บ ยิง handler จริง (bubble ไม่ถูกกลืน)

    เดิม anchor ที่ปุ่ม sim ในลิ้นชัก (answerRequest .ds-btn/in-drawer) ซึ่งถูกถอดออกแล้ว — จำลองการตอบ
    ย้ายไปหน้าผู้รับ (openRecipientView) จึง anchor ที่ปุ่มเปิดมุมมองผู้รับ + control ในหน้าผู้รับจริงแทน."""
    open_(page)
    go_tab(page, "registry")
    after(page, "() => openReqView('REQ-2601')")   # pending → sim 'เปิดมุมมองผู้รับ' โผล่ (officer เซ็นได้)
    wait_drawer(page, "req-view")
    # ยืนยันปุ่ม sim เดิมถูกถอดออกจริง — กันหลุดกลับมา (answerRequest ในลิ้นชัก + .ds-btn ใน demo-strip)
    nold = ev(page, "() => [].slice.call(document.querySelectorAll('#drawer button'))"
                    ".filter(function(b){return /answerRequest/.test(b.getAttribute('onclick')||'');}).length")
    assert nold == 0, f"ยังพบปุ่ม answerRequest ในลิ้นชัก {nold} (ควรย้ายไปหน้าผู้รับแล้ว)"
    assert ev(page, "() => document.querySelectorAll('.demo-strip .ds-btn').length") == 0, \
        "ยังพบปุ่ม .ds-btn ใน demo-strip (ควรถอดออกแล้ว — sim ย้ายไปหน้าผู้รับ)"
    # (ก) ปุ่ม 'เปิดมุมมองผู้รับ' ยิง handler จริง → เปิด overlay
    r1 = assert_affordances_fire(page, ['#drawer button[onclick*="openRecipientView"]'],
                                 note="ปุ่มเปิดมุมมองผู้รับในลิ้นชัก")
    page.wait_for_function("() => state.recipient && state.recipient.open===true", timeout=4000)
    page.wait_for_function("() => { var el=document.getElementById('recipientRoot'); return el && el.classList.contains('is-open'); }", timeout=4000)
    # (ข) control ในหน้าผู้รับ: choice (ยินยอม/ไม่ยินยอม) · ยืนยันตัวตน · ยืนยันการตอบ — ยิงจริงทุกตัว
    #     (submit ตอนยังเลือกไม่ครบ = เตือนแล้วไม่ปิด → click ยังถึง target = probe ยิง)
    r2 = assert_affordances_fire(page,
        ['#recipientRoot .rcp-choice', '#recipientRoot .rcp-verify-row', '#recipientRoot .rcp-submit'],
        note="control ในหน้าผู้รับ (choice/verify/submit)")
    # ปิดหน้าผู้รับ + ลิ้นชัก → ทดสอบ affordance ระดับแอป
    after(page, "() => closeRecipientView()")
    page.wait_for_function("() => !state.recipient.open", timeout=4000)
    after(page, "() => closeDrawer()")
    page.wait_for_function("() => state.drawer.open===false", timeout=4000)
    # (ค) persona (.ds-seg) → แถวทะเบียน (ก่อน navigate) → 4 แท็บ (navigate ท้ายสุด)
    r3 = assert_affordances_fire(page, ['.demo-strip .ds-seg button', 'tr.is-clickable', '.ptab'],
        note="persona (.ds-seg) + แถวทะเบียน + 4 แท็บ (capture-phase swallow guard)")
    ntested = len(r1["tested"]) + len(r2["tested"]) + len(r3["tested"])
    return (f"DSP-04: ปุ่มเปิดมุมมองผู้รับ + choice/verify/submit หน้าผู้รับ + persona + แถว + แท็บ "
            f"ยิง handler จริงทุกตัว (bubble ไม่ถูกกลืน · tested={ntested})")


def c_recipient_overlay(page):
    """[RCP] หน้าผู้รับ (recipient view) เรนเดอร์เต็มจอเหนือแอป (z สูงกว่า drawer) · Esc ปิดได้ (drawer ยังอยู่)"""
    open_(page)
    after(page, "() => openReqView('REQ-2601')")
    wait_drawer(page, "req-view")
    open_recipient(page)
    iw = ev(page, "() => innerWidth")
    ih = ev(page, "() => innerHeight")
    box = ev(page, "() => { var r=document.getElementById('recipientRoot').getBoundingClientRect(); return {w:r.width,h:r.height,x:r.left,y:r.top}; }")
    # fixed inset:0 → เต็ม layout viewport (กว้างน้อยกว่า innerWidth ได้ ~scrollbar ของ document ~17px)
    assert box["x"] <= 1 and box["y"] <= 1 and box["w"] >= iw - 20 and box["h"] >= ih - 1, \
        f"[RCP] หน้าผู้รับไม่เต็มจอ (fixed inset:0): {box} vs {iw}x{ih}"
    # อยู่เหนือ drawer (z-index) + จุดกึ่งกลางจอชนหน้าผู้รับจริง (ไม่ถูกอย่างอื่นบัง)
    rz = ev(page, "() => parseInt(getComputedStyle(document.getElementById('recipientRoot')).zIndex,10)")
    dz = ev(page, "() => parseInt(getComputedStyle(document.getElementById('drawer')).zIndex,10)")
    assert rz > dz, f"[RCP] recipient z ({rz}) ต้อง > drawer z ({dz})"
    hit_in = ev(page, "() => { var el=document.elementFromPoint(innerWidth/2, innerHeight/2); var rr=document.getElementById('recipientRoot'); return !!(el && (el===rr || rr.contains(el))); }")
    assert hit_in, "[RCP] จุดกึ่งกลางจอไม่ชนหน้าผู้รับ (overlay ไม่ได้อยู่บนสุด)"
    assert ev(page, "() => document.querySelectorAll('#recipientRoot .rcp-page').length") == 1, "[RCP] ไม่มี .rcp-page"
    # Esc ปิดหน้าผู้รับ (surface บนสุด — ปิดก่อน drawer/modal) · drawer คำขอต้องยังอยู่
    page.keyboard.press("Escape")
    page.wait_for_function("() => !state.recipient.open", timeout=4000)
    settle(page)
    assert ev(page, "() => document.getElementById('recipientRoot').classList.contains('is-open')") is False, \
        "[RCP] Esc แล้ว overlay ยังไม่ปิด (is-open ค้าง)"
    assert ev(page, "() => state.drawer.open") is True, "[RCP] Esc ปิดหน้าผู้รับแล้ว drawer คำขอควรยังอยู่"
    return f"หน้าผู้รับเต็มจอ ({round(box['w'])}×{round(box['h'])}) เหนือ drawer (z {rz}>{dz}) · Esc ปิดได้ (drawer ยังอยู่)"


# ═══════════════════════════════ C3.8 SPACING GUARDS (uikit helpers ใหม่ · revert-proof) ═══════════════════════════════
# ผู้ใช้เจอ 3 จุด cosmetic ที่ qc-ux/e2e เดิมมองไม่เห็น (แก้ใน HTML แล้ว) → §C3.8 บังคับเพิ่มการตรวจ
# เข้า uikit + พิสูจน์ว่าจับได้จริงด้วยการย้อน style ให้พัง (in-page · ไม่แตะ consent-pdpa.html)

def c_e33_filter_gap(page):
    """[E33 · C3.8 · bug#1] filter-bar ไม่แปะชิดตาราง (registry) + revert-proof (margin→0 ต้องจับได้)"""
    open_(page)
    go_tab(page, "registry")
    r0 = assert_filter_not_flush(page, note="registry filter-bar vs ตาราง")   # ผ่านบนไฟล์จริง (fixed)
    # ── revert-proof: ย้อน margin-bottom → 0 (สภาพก่อนแก้) → ตัววัดต้อง RAISE ──
    ev(page, "() => document.querySelectorAll('.filter-bar').forEach(e=>e.style.marginBottom='0px')")
    settle(page)
    broke = page.evaluate(JS_FILTER_FLUSH, {"min": 8})
    raised = False
    try:
        assert_filter_not_flush(page)
    except AssertionError:
        raised = True
    assert raised, "[C3.8] ย้อน margin เป็น 0 แล้วตัววัดยังไม่ฟ้อง (จับ regression ไม่ได้)"
    assert broke["ok"] is False, "[C3.8] margin→0 แล้ว measure ยังบอกว่าผ่าน (ผิด)"
    # ── restore: ล้าง inline style → กลับไปใช้ค่า stylesheet ──
    ev(page, "() => document.querySelectorAll('.filter-bar').forEach(e=>e.style.marginBottom='')")
    settle(page)
    r1 = assert_filter_not_flush(page, note="restore")
    return (f"filter↔ตาราง: fixed {r0['minGap']}px ผ่าน · revert(margin0) {broke['minGap']}px จับได้ (raise) · "
            f"restore {r1['minGap']}px ผ่าน")


def c_e34_button_gap(page):
    """[E34 · C3.8 · bug#2] ปุ่มในลิ้นชัก/หน้าต่างไม่ชิดกัน (create/view + withdraw) + revert-proof (gap→4px)"""
    open_(page)
    # (ก) create drawer + view drawer — guard ผ่าน (dw-footer-right 1 ปุ่ม→ข้าม · ไม่มีคู่ชิด)
    after(page, "() => openReqCreate({})")
    wait_drawer(page, "req-create")
    assert_action_button_gap(page, ['.dw-footer-right', '.drawer-footer', '.drawer-header-actions'], note="req-create")
    after(page, "() => { closeDrawer(); }")
    after(page, "() => openConsentView('CNS-5001')")
    wait_drawer(page, "consent-view")
    assert_action_button_gap(page, ['.dw-footer-right', '.drawer-footer', '.drawer-header-actions'], note="consent-view")
    # (ข) withdraw modal — .modal-footer มีปุ่มติดกันจริง (ยกเลิก↔ยืนยันถอน) = คู่จริงให้ทั้ง guard + revert-proof
    after(page, "() => openModal('withdraw',{id:'CNS-5001'})")
    wait_modal(page, "withdraw")
    r0 = assert_action_button_gap(page, ['.modal-footer', '.dw-footer-right'], note="withdraw modal")
    # ── revert-proof: บีบ gap ของ .modal-footer → 4px → ตัววัดต้อง RAISE ──
    ev(page, "() => document.querySelectorAll('.modal-footer').forEach(e=>e.style.gap='4px')")
    settle(page)
    broke = page.evaluate(JS_ACTION_BTN_GAP, {"selectors": ['.modal-footer'], "min": 8})
    raised = False
    try:
        assert_action_button_gap(page, ['.modal-footer'], note="revert")
    except AssertionError:
        raised = True
    assert raised, "[C3.8] gap→4px แล้วตัววัดยังไม่ฟ้อง (จับ regression ไม่ได้)"
    assert broke["ok"] is False, "[C3.8] gap→4px แล้ว measure ยังบอกว่าผ่าน (ผิด)"
    ev(page, "() => document.querySelectorAll('.modal-footer').forEach(e=>e.style.gap='')")
    settle(page)
    r1 = assert_action_button_gap(page, ['.modal-footer'], note="restore")
    g0 = min((p["gap"] for p in r0["pairs"]), default=None)
    gb = min((p["gap"] for p in broke["pairs"]), default=None)
    g1 = min((p["gap"] for p in r1["pairs"]), default=None)
    return (f"ปุ่มติดกัน: withdraw .modal-footer fixed {g0}px ผ่าน · revert(gap4) {gb}px จับได้ (raise) · "
            f"restore {g1}px ผ่าน · tested={r0['tested']}")


def c_e35_modal_warn(page):
    """[E35 · C3.8 · bug#3] กล่องเตือนใน modal ออกเวอร์ชันใหม่ ไม่อึดอัด + revert-proof (padTop6/pad4)"""
    open_(page)
    after(page, "() => openModal('new-version',{code:'PUR-02'})")
    wait_modal(page, "new-version")
    r0 = assert_modal_warn_not_cramped(page, note="new-version modal")   # ผ่านบนไฟล์จริง (fixed)
    # ── revert-proof: modal-body paddingTop→6px + warn-banner padding→4px (สภาพก่อนแก้) → ต้อง RAISE ──
    ev(page, "() => { document.querySelectorAll('#modalBackdrop .modal-body').forEach(e=>e.style.paddingTop='6px'); "
             "document.querySelectorAll('#modalBackdrop .warn-banner').forEach(e=>e.style.padding='4px'); }")
    settle(page)
    broke = page.evaluate(JS_MODAL_WARN_CRAMPED, {"clear": 8, "pad": 12})
    raised = False
    try:
        assert_modal_warn_not_cramped(page, note="revert")
    except AssertionError:
        raised = True
    assert raised, "[C3.8] padding เล็กแล้วตัววัดยังไม่ฟ้อง (จับ regression ไม่ได้)"
    assert broke["ok"] is False, "[C3.8] padding เล็กแล้ว measure ยังบอกว่าผ่าน (ผิด)"
    ev(page, "() => { document.querySelectorAll('#modalBackdrop .modal-body').forEach(e=>e.style.paddingTop=''); "
             "document.querySelectorAll('#modalBackdrop .warn-banner').forEach(e=>e.style.padding=''); }")
    settle(page)
    r1 = assert_modal_warn_not_cramped(page, note="restore")
    return (f"warn-banner: fixed clearance {r0['clearance']}px pad(t/r/b/l) {r0['padding']} ผ่าน · "
            f"revert clearance {broke['clearance']}px pad {broke['padding']} จับได้ (raise) · "
            f"restore clearance {r1['clearance']}px ผ่าน")


def c_e36_purview_footer_gap(page):
    """[E36 · C3.8 · bug#4] ปุ่มซ้ายใน dw-footer (pur-view · DPO) ไม่ชิดกัน + revert-proof (block/gap0)"""
    open_(page)
    set_persona(page, "dpo")                     # perm.purpose=true → footer โชว์ 2 ปุ่มซ้าย
    after(page, "() => openPurView('PUR-01')")    # PUR-01 active → ออกเวอร์ชันใหม่ + ปิดวัตถุประสงค์
    wait_drawer(page, "pur-view")
    # ยืนยันว่าคู่ปุ่มจริงอยู่ในกลุ่มซ้าย (สภาพที่ผู้ใช้เจอ flush 0px)
    dt = drawer_text(page)
    assert "ออกเวอร์ชันใหม่" in dt and "ปิดวัตถุประสงค์" in dt, \
        "seed: pur-view (DPO/active) ต้องมีทั้ง 'ออกเวอร์ชันใหม่' + 'ปิดวัตถุประสงค์' ในกลุ่มซ้าย"
    nleft = ev(page, "() => document.querySelectorAll('#drawer .dw-footer-left button, #drawer .dw-footer-left .btn').length")
    assert nleft == 2, f"dw-footer-left ต้องมี 2 ปุ่ม (ได้ {nleft})"
    # ── guard ผ่านบนไฟล์จริง (fixed: .dw-footer-left display:flex gap:10px) ──
    r0 = assert_action_button_gap(page, ['.dw-footer', '.dw-footer-left'], min_gap=8, note="pur-view footer (DPO)")
    # ── revert-proof: ย้อน .dw-footer-left เป็น block + gap 0 (สภาพก่อนแก้) → ตัววัดต้อง RAISE ──
    ev(page, "() => document.querySelectorAll('.dw-footer-left').forEach(e=>{e.style.display='block';e.style.gap='0px';})")
    settle(page)
    broke = page.evaluate(JS_ACTION_BTN_GAP, {"selectors": ['.dw-footer', '.dw-footer-left'], "min": 8})
    raised = False
    try:
        assert_action_button_gap(page, ['.dw-footer', '.dw-footer-left'], min_gap=8, note="revert")
    except AssertionError:
        raised = True
    assert raised, "[C3.8] ย้อน .dw-footer-left เป็น block/gap0 แล้วตัววัดยังไม่ฟ้อง (จับ regression ไม่ได้)"
    assert broke["ok"] is False, "[C3.8] block/gap0 แล้ว measure ยังบอกว่าผ่าน (ผิด)"
    # ── restore: ล้าง inline style → กลับไปใช้ค่า stylesheet (.dw-footer-left flex gap:10px) ──
    ev(page, "() => document.querySelectorAll('.dw-footer-left').forEach(e=>{e.style.display='';e.style.gap='';})")
    settle(page)
    r1 = assert_action_button_gap(page, ['.dw-footer', '.dw-footer-left'], min_gap=8, note="restore")
    g0 = min((p["gap"] for p in r0["pairs"]), default=None)
    gb = min((p["gap"] for p in broke["pairs"]), default=None)
    g1 = min((p["gap"] for p in r1["pairs"]), default=None)
    return (f"pur-view footer (DPO): fixed {g0}px ผ่าน · revert(block/gap0) {gb}px จับได้ (raise) · "
            f"restore {g1}px ผ่าน · tested={r0['tested']}")


def c_e37_qr_actions_gap(page):
    """[E37 · C3.8 · bug#5] ปุ่มดาวน์โหลด QR/ฟอร์ม PDF (req-view) ไม่ชิดกัน + revert-proof (gap0/nowrap)"""
    open_(page)
    go_tab(page, "requests")                       # แท็บ 'คำขอ'
    after(page, "() => openReqView('REQ-2601')")    # pending → มีลิงก์ + QR section
    wait_drawer(page, "req-view")
    # ยืนยันคู่ปุ่มจริงอยู่ใน .qr-actions (สภาพก่อนแก้ = stacked flush .mt-2)
    dt = drawer_text(page)
    assert "ดาวน์โหลด QR" in dt and "ดาวน์โหลดเอกสาร" in dt, \
        "seed: req-view (REQ-2601) ต้องมีทั้ง 'ดาวน์โหลด QR' + 'ดาวน์โหลดเอกสาร' ใน .qr-actions"
    nqr = ev(page, "() => document.querySelectorAll('#drawer .qr-actions button, #drawer .qr-actions .btn').length")
    assert nqr == 2, f".qr-actions ต้องมี 2 ปุ่ม (ได้ {nqr})"
    # ── guard ผ่านบนไฟล์จริง (fixed: .qr-actions display:flex gap:10px flex-wrap) ──
    r0 = assert_action_button_gap(page, ['.qr-actions'], min_gap=8, note="req-view QR actions")
    # ── revert-proof: ย้อน .qr-actions เป็น gap 0 + nowrap (สภาพก่อนแก้ = ชิดกัน) → ตัววัดต้อง RAISE ──
    ev(page, "() => document.querySelectorAll('.qr-actions').forEach(e=>{e.style.gap='0px';e.style.flexWrap='nowrap';})")
    settle(page)
    broke = page.evaluate(JS_ACTION_BTN_GAP, {"selectors": ['.qr-actions'], "min": 8})
    raised = False
    try:
        assert_action_button_gap(page, ['.qr-actions'], min_gap=8, note="revert")
    except AssertionError:
        raised = True
    assert raised, "[C3.8] ย้อน .qr-actions เป็น gap0/nowrap แล้วตัววัดยังไม่ฟ้อง (จับ regression ไม่ได้)"
    assert broke["ok"] is False, "[C3.8] gap0/nowrap แล้ว measure ยังบอกว่าผ่าน (ผิด)"
    # ── restore: ล้าง inline style → กลับไปใช้ค่า stylesheet (.qr-actions flex gap:10px) ──
    ev(page, "() => document.querySelectorAll('.qr-actions').forEach(e=>{e.style.gap='';e.style.flexWrap='';})")
    settle(page)
    r1 = assert_action_button_gap(page, ['.qr-actions'], min_gap=8, note="restore")
    g0 = min((p["gap"] for p in r0["pairs"]), default=None)
    gb = min((p["gap"] for p in broke["pairs"]), default=None)
    g1 = min((p["gap"] for p in r1["pairs"]), default=None)
    return (f"qr-actions: fixed {g0}px ผ่าน · revert(gap0) {gb}px จับได้ (raise) · "
            f"restore {g1}px ผ่าน · tested={r0['tested']}")


# ═══════════════════════════════ ESC + POLISH ═══════════════════════════════

def c_esc_chain(page):
    """[Esc] modal เปิดทับ drawer → Esc ครั้งเดียวปิด modal (drawer ยังอยู่) · Esc อีกครั้งปิด drawer"""
    open_(page)
    after(page, "() => openConsentView('CNS-5001')")
    wait_drawer(page, "consent-view")
    after(page, "() => openModal('withdraw',{id:'CNS-5001'})")
    wait_modal(page, "withdraw")
    page.keyboard.press("Escape")
    page.wait_for_function("() => state.modal.open===false", timeout=4000)
    settle(page)
    assert ev(page, "() => state.drawer.open") is True, "[Esc] ปิด modal แล้ว drawer หลุดปิดตาม (ควรอยู่)"
    page.keyboard.press("Escape")
    page.wait_for_function("() => state.drawer.open===false", timeout=4000)
    return "Esc chain: Esc#1 ปิด modal (drawer อยู่) · Esc#2 ปิด drawer"


def c_no_garbage(page):
    """[polish] ไม่มีข้อความขยะ (undefined/NaN/[object Object]/null) หลุดบนจอทุกแท็บ + drawer"""
    open_(page)
    for t in ("registry", "requests", "purposes", "resolve"):
        go_tab(page, t)
        assert_no_garbage_text(page, scope="#page-content")
    after(page, "() => openConsentView('CNS-5001')")
    wait_drawer(page, "consent-view")
    assert_no_garbage_text(page, scope="#drawer")
    # ทำ resolve คู่ที่ยินยอม (ฟิลด์ครบ ไม่มี null ตาม contract) แล้วเช็ค JSON ไม่มี undefined/NaN/null รั่ว
    open_(page)
    go_tab(page, "resolve")
    combo_pick(page, "rzSubject", 0)     # CUS-1001
    combo_pick(page, "rzPurpose", 0)     # PUR-01
    combo_pick(page, "rzChannel", 0)     # email → granted (policy_version/granted_at/expires_at มีค่าจริง)
    after(page, "() => runResolve()")
    assert_no_garbage_text(page, scope="#page-content")
    return "ไม่มีข้อความขยะ (undefined/NaN/[object Object]/null) ทุกแท็บ + drawer + ผล resolve (granted)"


# ═══════════════════════════════ UI ADDITIONS (guard cases · 2026-09-11) ═══════════════════════════════
# เพิ่ม 3 ของใหม่บนจอ → ต้องมีเคสกันถอยหลัง (ไม่แตะ FN coverage เดิม 20/20)
#  A) ชื่อฟีเจอร์เป็นค่าคงที่บน page-header ทุกแท็บ
#  B) ปุ่ม 'อ่านเนื้อหา' (viewPolicy) → modal นโยบาย ลอยเหนือ drawer · stopPropagation ไม่ติ๊ก cb
#  C) ช่องค้นหาวัตถุประสงค์ในลิ้นชักสร้างคำขอ พิมพ์แล้วโฟกัส/คาเร็ตไม่หลุด + กรองจริง

def c_e38_feature_name(page):
    """[E38 · UI-A] page-header H1 (.ph-title) = ค่าคงที่ 'ความยินยอม PDPA' ทุกแท็บ (4/4)"""
    open_(page)
    seen = {}
    for t in ("registry", "requests", "purposes", "resolve"):
        go_tab(page, t)
        n = ev(page, "() => document.querySelectorAll('.ph-title').length")
        assert n == 1, f"แท็บ {t}: .ph-title ต้องมี 1 ตัว (ได้ {n})"
        txt = ev(page, "() => document.querySelector('.ph-title').textContent.trim()")
        assert txt == "ความยินยอม PDPA", f"แท็บ {t}: .ph-title = '{txt}' (ต้องเป็นค่าคงที่ 'ความยินยอม PDPA')"
        seen[t] = txt
    assert len(set(seen.values())) == 1, f"ชื่อบน page-header ไม่คงที่ข้ามแท็บ: {seen}"
    return "page-header .ph-title = 'ความยินยอม PDPA' คงที่ทุกแท็บ (registry/requests/purposes/resolve)"


def c_e39_view_policy(page):
    """[E39 · UI-B] ลิงก์เอกสาร (.doc-link = ชื่อไฟล์) ในลิ้นชักสร้างคำขอ → modal นโยบาย (ลอยเหนือ drawer · stopPropagation ไม่ติ๊ก cb) + req-view 'เนื้อหาที่ให้เซ็น'"""
    open_(page)
    after(page, "() => openReqCreate({})")
    wait_drawer(page, "req-create")
    # หา code ของแถวแรกที่มี .doc-link (ชื่อไฟล์เอกสารเป็นลิงก์ → viewPolicy) — เดิมเป็นปุ่ม 'อ่านเนื้อหา'
    code = ev(page, "() => { var b=[].slice.call(document.querySelectorAll('#reqPurRows .doc-link'))"
                    ".find(function(x){return /viewPolicy/.test(x.getAttribute('onclick')||'');});"
                    " return b ? (b.getAttribute('onclick').match(/viewPolicy\\('([^']+)'\\)/)||[])[1] : null; }")
    assert code, "ไม่พบลิงก์เอกสาร .doc-link (viewPolicy) ในแถววัตถุประสงค์ของลิ้นชักสร้างคำขอ"
    purq0 = ev(page, "() => state.reqForm.purposes.slice()")
    # คลิก .doc-link จริง (DOM .click()) — พิสูจน์ event.stopPropagation() ของจริง ไม่ใช่เรียก controller ตรง
    clicked = page.evaluate(
        "() => { var b=[].slice.call(document.querySelectorAll('#reqPurRows .doc-link'))"
        ".find(function(x){return /viewPolicy/.test(x.getAttribute('onclick')||'');});"
        " if(!b) return false; b.click(); return true; }")
    assert clicked, "คลิกลิงก์เอกสาร .doc-link ไม่ได้"
    wait_modal(page, "policy")
    # modal โชว์ข้อความนโยบาย 'เวอร์ชันปัจจุบัน' ของ purpose นั้น
    expected = ev(page, "() => { var p=purpose(%r); var cur=p.versions.filter(function(v){return v.v===p.currentVer;})[0]"
                        "||p.versions[p.versions.length-1]; return cur.body; }" % code)
    ver = ev(page, "() => purpose(%r).currentVer" % code)
    mt = modal_text(page)
    assert expected and expected in mt, f"[UI-B] modal ไม่โชว์ข้อความนโยบายเวอร์ชันปัจจุบันของ {code}"
    assert ("v" + str(ver)) in mt, f"[UI-B] modal ไม่ระบุเวอร์ชันปัจจุบัน (v{ver})"
    # ลอยเหนือ drawer — reuse JS_MODAL_UNDER_DRAWER ต้องว่าง
    under = ev(page, JS_MODAL_UNDER_DRAWER)
    assert not under, f"[UI-B] modal นโยบายจมใต้ drawer: {under}"
    mz = ev(page, "() => parseInt(getComputedStyle(document.getElementById('modalBackdrop')).zIndex,10)")
    dz = ev(page, "() => parseInt(getComputedStyle(document.getElementById('drawer')).zIndex,10)")
    assert mz > dz, f"[UI-B] modal z ({mz}) ต้อง > drawer z ({dz})"
    # stopPropagation ทำงาน — คลิก .doc-link (ชื่อไฟล์) ต้องไม่ติ๊ก checkbox ของแถวนั้น
    purq1 = ev(page, "() => state.reqForm.purposes.slice()")
    assert code not in purq1 and purq1 == purq0, \
        f"[UI-B] คลิก .doc-link ไปติ๊ก checkbox แถว {code} (stopPropagation ไม่ทำงาน · bubble ไปโดน toggleReqPurpose): {purq1}"
    after(page, "() => closeModal()")
    page.wait_for_function("() => state.modal.open===false", timeout=4000)
    # ── req-view (REQ-2601): section 'เนื้อหาที่ให้เซ็น' + .doc-link (ชื่อไฟล์เอกสาร) เปิด modal เดียวกัน ──
    after(page, "() => openReqView('REQ-2601')")
    wait_drawer(page, "req-view")
    assert "เนื้อหาที่ให้เซ็น" in drawer_text(page), "[UI-B] req-view (REQ-2601) ไม่มีส่วน 'เนื้อหาที่ให้เซ็น'"
    clicked2 = page.evaluate(
        "() => { var b=[].slice.call(document.querySelectorAll('#drawer .doc-link'))"
        ".find(function(x){return /viewPolicy/.test(x.getAttribute('onclick')||'');});"
        " if(!b) return false; b.click(); return true; }")
    assert clicked2, "[UI-B] ไม่พบลิงก์เอกสาร .doc-link ใน req-view 'เนื้อหาที่ให้เซ็น'"
    wait_modal(page, "policy")
    assert ev(page, "() => state.modal.type") == "policy", "[UI-B] ปุ่มใน req-view ไม่เปิด modal นโยบาย (policy)"
    under2 = ev(page, JS_MODAL_UNDER_DRAWER)
    assert not under2, f"[UI-B] modal นโยบายจาก req-view จมใต้ drawer: {under2}"
    return (f".doc-link (ชื่อไฟล์เอกสาร) → modal นโยบาย {code} v{ver} (ลอยเหนือ drawer z={mz}>{dz} · JS_MODAL_UNDER_DRAWER ว่าง · "
            f"ไม่ติ๊ก cb) · req-view มี 'เนื้อหาที่ให้เซ็น' .doc-link เปิด modal เดียวกัน")


def c_e40_search_focus(page):
    """[E40 · UI-C] #reqPurSearch พิมพ์ทีละคีย์แล้วโฟกัส/คาเร็ตไม่หลุด + #reqPurRows กรอง + ล้าง=ครบ + ไม่ตรง='ไม่พบวัตถุประสงค์'"""
    open_(page)
    after(page, "() => openReqCreate({})")
    wait_drawer(page, "req-create")
    total = ev(page, "() => document.querySelectorAll('#reqPurRows .opt-row').length")
    assert total >= 2, f"ต้องมีวัตถุประสงค์ให้กรอง ≥2 (ได้ {total})"
    inp = page.locator("#reqPurSearch")
    inp.click()
    # พิมพ์ทีละคีย์ (press_sequentially) — ห้าม fill() เพราะต้องดักโฟกัสหลุดกลางคัน
    q = "โปร"     # ตรงเฉพาะ PUR-01 'ส่งโปรโมชันสินค้า'
    inp.press_sequentially(q, delay=40)
    settle(page)
    # (1) โฟกัสยังอยู่ที่ช่องค้นหา (ถ้า re-render ทั้ง drawer โฟกัสจะหลุด)
    assert ev(page, "() => document.activeElement === document.getElementById('reqPurSearch')"), \
        "[UI-C] พิมพ์แล้วโฟกัสหลุดจาก #reqPurSearch (drawer re-render ทั้งใบ?)"
    val = ev(page, "() => document.getElementById('reqPurSearch').value")
    assert val == q, f"[UI-C] ค่าที่พิมพ์ไม่ครบ (ได้ '{val}' คาด '{q}') — คีย์หล่นเพราะ re-render กลางคัน"
    caret = ev(page, "() => document.getElementById('reqPurSearch').selectionStart")
    assert caret == len(q), f"[UI-C] คาเร็ตไม่อยู่ท้ายข้อความ (selectionStart={caret} คาด {len(q)})"
    # (2) #reqPurRows กรองแล้ว (จำนวนลด + 'แสดง X จาก Y' สะท้อนตัวกรอง)
    shown = ev(page, "() => document.querySelectorAll('#reqPurRows .opt-row').length")
    assert 0 < shown < total, f"[UI-C] กรองแล้วจำนวนแถวไม่ลด (shown {shown}/{total})"
    rowtxt = ev(page, "() => document.getElementById('reqPurRows').textContent")
    assert ("แสดง %d จาก %d" % (shown, total)) in rowtxt, \
        f"[UI-C] ตัวนับ 'แสดง X จาก Y' ไม่สะท้อนตัวกรอง (shown={shown} total={total}): {rowtxt[:70]}"
    # (3) ล้าง query → กลับมาครบเท่าเดิม
    inp.press("Control+a")
    inp.press("Backspace")
    settle(page)
    assert ev(page, "() => document.getElementById('reqPurSearch').value") == "", "[UI-C] ล้าง query ไม่สำเร็จ"
    back = ev(page, "() => document.querySelectorAll('#reqPurRows .opt-row').length")
    assert back == total, f"[UI-C] ล้าง query แล้วไม่กลับมาแสดงครบ ({back}/{total})"
    assert ("แสดง %d จาก %d" % (total, total)) in ev(page, "() => document.getElementById('reqPurRows').textContent"), \
        "[UI-C] ล้าง query แล้วตัวนับไม่กลับเป็นทั้งหมด"
    # (4) query ที่ไม่ตรง → 'ไม่พบวัตถุประสงค์' (โฟกัสยังอยู่)
    inp.press_sequentially("zzzz", delay=30)
    settle(page)
    assert ev(page, "() => document.querySelectorAll('#reqPurRows .opt-row').length") == 0, \
        "[UI-C] query ที่ไม่ตรงต้องไม่เหลือแถววัตถุประสงค์"
    assert "ไม่พบวัตถุประสงค์" in ev(page, "() => document.getElementById('reqPurRows').textContent"), \
        "[UI-C] query ที่ไม่ตรงไม่ขึ้น 'ไม่พบวัตถุประสงค์'"
    assert ev(page, "() => document.activeElement === document.getElementById('reqPurSearch')"), \
        "[UI-C] โฟกัสหลุดตอนผลลัพธ์ว่าง (empty-state re-render กระทบ input?)"
    return (f"#reqPurSearch พิมพ์ '{q}' ทีละคีย์ → โฟกัส/คาเร็ตคงอยู่ (caret={caret}) · กรอง {total}→{shown} "
            f"('แสดง X จาก Y' ตรง) · ล้าง=ครบ {total} · ไม่ตรง='ไม่พบวัตถุประสงค์' (โฟกัสยังอยู่)")


# ═══════════════════════════════ BA-GATE FIXES (2026-09-14 · FIX-01..08) ═══════════════════════════════
# รอบแก้จาก BA gate: bypass ที่ e2e เดิม (41/41) มองไม่เห็น — ตอบซ้ำ/persona bypass/double-submit/
# ส่งซ้ำ-ถอนซ้ำ/snapshot เวอร์ชัน/contract anchors/demo-only/pill. อ้าง bypass id B1..B8 ในใบสั่งแก้.

def c_fix01_answer_once(page):
    """[E41 · FIX-01 · B1/B2 CRITICAL] คำขอ answered ตอบซ้ำไม่ได้ (evidence chain ไม่ถูกเขียนทับ) + หน้าผู้รับปิด"""
    open_(page)                                   # persona = officer (sign ได้) → ทดสอบ 'status guard' ล้วน
    n0 = ev(page, "() => state.consents.length")
    h0 = ev(page, "() => request('REQ-2603').status")
    assert h0 == "answered", "seed REQ-2603 ต้องเป็น answered"
    after(page, "() => answerRequest('REQ-2603','all')")     # B1: เดิม consents 9→11
    assert ev(page, "() => state.consents.length") == n0, "[FIX-01] คำขอ answered ถูกตอบซ้ำ → consent เพิ่ม (evidence ถูกเขียนทับ)"
    assert "ปิดแล้ว" in toast_text(page), f"[FIX-01] ตอบซ้ำต้องขึ้น toast 'คำขอนี้ปิดแล้ว' (toast='{toast_text(page)}')"
    # submitRecipient path ก็ต้องกันเช่นกัน (จุดเดียวคุมที่ applyAnswers)
    after(page, "() => applyAnswers(request('REQ-2603'), function(){return true;})")
    assert ev(page, "() => state.consents.length") == n0, "[FIX-01] applyAnswers ตรงบนคำขอ answered ยังสร้าง consent"
    # ── ลูกค้าเปิดลิงก์ซ้ำ (recipient view ของคำขอที่ปิดแล้ว) → หน้าสถานะปิด ไม่มีฟอร์ม/ปุ่มส่ง ──
    after(page, "() => openRecipientView('REQ-2603')")
    page.wait_for_function("() => state.recipient && state.recipient.open===true", timeout=4000)
    rt = ev(page, "() => (document.getElementById('recipientRoot')||{}).textContent || ''")
    assert "คำขอนี้ปิดแล้ว" in rt, "[FIX-01] เปิดลิงก์ซ้ำต้องเห็นหน้าสถานะปิด 'คำขอนี้ปิดแล้ว'"
    assert ev(page, "() => document.querySelectorAll('#recipientRoot .rcp-submit').length") == 0, "[FIX-01] หน้าปิดต้องไม่มีปุ่มส่งคำตอบ"
    assert ev(page, "() => document.querySelectorAll('#recipientRoot .rcp-choice').length") == 0, "[FIX-01] หน้าปิดต้องไม่มีตัวเลือกยินยอม/ไม่ยินยอม"
    return f"answered ตอบซ้ำไม่ได้ (consents คงที่ {n0} · toast ปิดแล้ว · applyAnswers ตรงก็กัน) · เปิดลิงก์ซ้ำ = หน้าสถานะปิด (ไม่มีฟอร์ม)"


def c_fix02_persona_guard(page):
    """[E42 · FIX-02 · B4] persona อ่านอย่างเดียว (auditor) เรียก mutation ตรงไม่ผ่าน (guard อยู่ในฟังก์ชัน)"""
    open_(page)
    set_persona(page, "auditor")
    # ทุก mutation: เรียกตรง → state ต้องไม่ขยับ (assert_role_write_blocked · uikit C3.8)
    assert_role_write_blocked(page, "answerRequest('REQ-2601','all')", "state.consents.length", note="sign")
    assert_role_write_blocked(page, "doWithdraw('CNS-5001')",
                              "state.consents.find(function(x){return x.id==='CNS-5001';}).history.length", note="withdraw")
    assert_role_write_blocked(page, "doPublishVersion('PUR-01')", "purpose('PUR-01').versions.length", note="purpose/publish")
    assert_role_write_blocked(page, "doClosePurpose('PUR-02')",
                              "(purpose('PUR-02').status==='closed')?1:0", note="purpose/close")
    assert_role_write_blocked(page, "sendVia('REQ-2602','line')", "request('REQ-2602').sends.length", note="send")
    n_req = ev(page, "() => state.requests.length")
    ev(page, "() => { state.reqForm={subject:'CUS-1001',channel:'email',purposes:['PUR-01'],refOld:null}; }")
    ev(page, "() => { try{ submitReqCreate(); }catch(e){} }")
    assert ev(page, "() => state.requests.length") == n_req, "[FIX-02] auditor สร้างคำขอตรงได้ (reqCreate guard ไม่อยู่ในฟังก์ชัน)"
    # ── revert-proof: defeat PERM (คืนค่า all-true = จำลองสภาพ guard UI-only) → auditor เขียนได้จริง = ตัววัดจับได้ ──
    open_(page); set_persona(page, "auditor")
    ev(page, "() => { window.__PERM=window.PERM; window.PERM=function(){return {reqCreate:true,send:true,sign:true,withdraw:true,purpose:true};}; }")
    raised = False
    try:
        assert_role_write_blocked(page, "answerRequest('REQ-2601','all')", "state.consents.length", note="revert")
    except AssertionError:
        raised = True
    assert raised, "[C3.8] defeat PERM แล้ว auditor ยังเขียนไม่ได้ = ตัววัด role-guard จับ regression ไม่ได้"
    ev(page, "() => { window.PERM=window.__PERM; }")
    return "auditor เรียก 6 mutation ตรง → state ไม่ขยับทุกตัว (guard ในฟังก์ชัน) · revert(defeat PERM) จับได้ (raise)"


def c_fix04_double_submit(page):
    """[E43 · FIX-04 · B8] double submit สร้างคำขอครั้งเดียว (_busy guard + loader-2) + revert-proof"""
    open_(page)
    set_persona(page, "dpo")
    ev(page, "() => { state.reqForm={subject:'CUS-1001',channel:'email',purposes:['PUR-01'],refOld:null}; }")
    r0 = assert_double_submit_single(page, "submitReqCreate()", "state.requests.length", note="req-create")
    # loader-2 มีในไฟล์ (Rule #44) — spinner CSS + icon ในปุ่มตอน busy
    assert ev(page, "() => /loader-2/.test(document.documentElement.innerHTML)"), "[FIX-04] ไม่พบ loader-2 (loading affordance · Rule #44)"
    # ── revert-proof: defeat guardBusy (คืน true เสมอ = ไม่มี _busy) → ยิง 2 ครั้ง = +2 → helper ต้อง RAISE ──
    open_(page); set_persona(page, "dpo")
    ev(page, "() => { window.__gb=window.guardBusy; window.guardBusy=function(){return true;}; }")
    ev(page, "() => { state.reqForm={subject:'CUS-1001',channel:'email',purposes:['PUR-01'],refOld:null}; }")
    raised = False
    try:
        assert_double_submit_single(page, "submitReqCreate()", "state.requests.length", note="revert")
    except AssertionError:
        raised = True
    assert raised, "[C3.8] defeat guardBusy แล้วยิง 2 ครั้งยังไม่ +2 = ตัววัด double-submit จับ regression ไม่ได้"
    ev(page, "() => { window.guardBusy=window.__gb; }")
    return f"double submit สร้างคำขอครั้งเดียว (delta={r0['delta']}) · loader-2 มีจริง · revert(defeat guardBusy) จับได้ (raise)"


def c_fix05_substatus_guard(page):
    """[E44 · FIX-05 · B3/B7] withdraw เฉพาะ granted · sendVia เฉพาะ draft/pending"""
    open_(page)
    set_persona(page, "dpo")
    # (a) B3: withdraw ซ้ำบน consent ที่ withdrawn แล้ว (CNS-5004) → history/CSQ ไม่เพิ่ม
    h0 = ev(page, "() => state.consents.find(function(x){return x.id==='CNS-5004';}).history.length")
    csq0 = ev(page, "() => (state._csq||[]).length")
    after(page, "() => doWithdraw('CNS-5004')")
    assert ev(page, "() => state.consents.find(function(x){return x.id==='CNS-5004';}).history.length") == h0, \
        "[FIX-05] withdraw ซ้ำบน withdrawn → history เพิ่ม"
    assert ev(page, "() => (state._csq||[]).length") == csq0, "[FIX-05] withdraw ซ้ำ → CSQ reversal ยิงซ้ำ (idempotency ฝั่ง UI พัง)"
    assert "ไม่อยู่ในสถานะยินยอม" in toast_text(page), f"[FIX-05] withdraw ซ้ำต้องเตือน (toast='{toast_text(page)}')"
    # (b) B7: sendVia บนคำขอ answered (REQ-2603) → sends ไม่เพิ่ม
    s0 = ev(page, "() => request('REQ-2603').sends.length")
    after(page, "() => sendVia('REQ-2603','line')")
    assert ev(page, "() => request('REQ-2603').sends.length") == s0, "[FIX-05] sendVia บนคำขอ answered → บันทึกการส่งเพิ่ม"
    assert "ปิดแล้ว" in toast_text(page), f"[FIX-05] sendVia บนคำขอปิดต้องเตือน (toast='{toast_text(page)}')"
    return f"withdraw เฉพาะ granted (CNS-5004 withdrawn: history {h0} คงที่ · CSQ {csq0} คงที่) · sendVia เฉพาะ draft/pending (REQ-2603 answered: sends {s0} คงที่)"


def c_fix03_send_snapshot(page):
    """[E45 · FIX-03] การส่ง snapshot เวอร์ชันนโยบาย → drawer แสดงเวอร์ชัน ณ ตอนส่ง + ป้ายเตือนเมื่อมีเวอร์ชันใหม่กว่า"""
    open_(page)
    set_persona(page, "dpo")
    v_send = ev(page, "() => purpose('PUR-01').currentVer")     # = 2 (เวอร์ชันตอนส่ง)
    after(page, "() => sendVia('REQ-2602','email')")            # REQ-2602 = [PUR-01] · snapshot vers
    snap = ev(page, "() => { var s=request('REQ-2602').sends; return s[s.length-1].vers; }")
    assert snap and snap.get("PUR-01") == v_send, f"[FIX-03] การส่งไม่ snapshot เวอร์ชัน ({snap})"
    # ออกเวอร์ชันใหม่ของ PUR-01 (v2→v3) ระหว่างคำขอค้าง
    after(page, "() => openNewVersion('PUR-01')")
    wait_modal(page, "new-version")
    upload_doc(page, "nvDocInput", "() => state.nvDoc && (state.nvDoc.body||'').length>0")
    after(page, "() => doPublishVersion('PUR-01')")
    v_now = ev(page, "() => purpose('PUR-01').currentVer")
    assert v_now == v_send + 1, f"[FIX-03] publish เวอร์ชันใหม่ไม่สำเร็จ ({v_send}→{v_now})"
    # เปิด drawer คำขอเดิม → panel 'เนื้อหาที่ให้เซ็น' ต้องแสดงเวอร์ชัน ณ ตอนส่ง (v2) + ป้ายเตือน ปัจจุบัน v3
    after(page, "() => openReqView('REQ-2602')")
    wait_drawer(page, "req-view")
    dt = drawer_text(page)
    assert ("ส่ง v%d" % v_send) in dt and ("ปัจจุบัน v%d" % v_now) in dt, \
        f"[FIX-03] drawer ไม่เตือนเวอร์ชัน (คาด 'ส่ง v{v_send} · ปัจจุบัน v{v_now}')"
    # .doc-link ต้องเปิดเวอร์ชันที่ส่ง (viewPolicy('PUR-01',2)) ไม่ใช่เวอร์ชันปัจจุบัน
    has_sent_link = ev(page, "() => [].slice.call(document.querySelectorAll('#drawer .doc-link'))"
                       ".some(function(b){return (b.getAttribute('onclick')||'').indexOf(\"viewPolicy('PUR-01',%d)\")>=0;})" % v_send)
    assert has_sent_link, f"[FIX-03] .doc-link ไม่ชี้เวอร์ชันที่ส่ง (viewPolicy('PUR-01',{v_send}))"
    return f"ส่ง snapshot v{v_send} → publish v{v_now} → drawer แสดง 'ส่ง v{v_send} · ปัจจุบัน v{v_now}' + .doc-link เปิดเวอร์ชันที่ส่ง"


def c_fix06_contract_anchors(page):
    """[E46 · FIX-06] contract anchors F136/F031/F157/DSAR อยู่ในไฟล์ (comment · display-only ไม่ mock จอ)"""
    open_(page)
    src = HTML.read_text(encoding="utf-8")
    for code in ("F136", "F031", "F157", "DSAR"):
        assert code in src, f"[FIX-06] ไม่พบ contract anchor '{code}' ในไฟล์"
    assert src.count("CONTRACT") >= 2, "[FIX-06] ไม่พบ comment 'CONTRACT:' (anchor สัญญาข้ามฟีเจอร์)"
    # display-only: ต้องไม่มีเมนู/หน้าจอของฟีเจอร์อื่นเกิดใหม่ (sidebar ยังเมนูเดียว #navConsent)
    nmenu = ev(page, "() => document.querySelectorAll('#navConsent').length")
    assert nmenu == 1, f"[FIX-06] sidebar ควรเมนูเดียว (#navConsent) — พบ {nmenu}"
    # F136/F031/F157 ต้องไม่โผล่เป็นข้อความบนจอผู้ใช้ (เป็น comment เท่านั้น)
    for t in ("registry", "requests", "purposes", "resolve"):
        go_tab(page, t)
        pt = page_text(page)
        for code in ("F136", "F031", "F157"):
            assert code not in pt, f"[FIX-06] รหัส {code} โผล่บนจอแท็บ {t} (ต้องเป็น comment/anchor ไม่ใช่ UI)"
    return "contract anchors F136/F031/F157/DSAR อยู่ในไฟล์ (comment) · เมนูเดียว #navConsent · ไม่โผล่บนจอผู้ใช้"


def c_fix07_demo_only(page):
    """[E47 · FIX-07] demo elements ติด class demo-only · ซ่อนแล้วหน้าจอสะอาด (ไม่พัง layout)"""
    open_(page)
    assert ev(page, "() => document.querySelectorAll('.demo-strip.demo-only').length") == 1, \
        "[FIX-07] demo-strip ไม่ติด class demo-only"
    # เปิดหน้าผู้รับ → simbar ต้องติด demo-only
    after(page, "() => openReqView('REQ-2601')")
    wait_drawer(page, "req-view")
    # sim section ในลิ้นชัก (พรีวิวหน้าผู้รับ) ติด demo-only
    assert ev(page, "() => document.querySelectorAll('#drawer .demo-only').length") >= 1, \
        "[FIX-07] ส่วนพรีวิวหน้าผู้รับในลิ้นชักไม่ติด demo-only"
    open_recipient(page)
    assert ev(page, "() => document.querySelectorAll('#recipientRoot .rcp-simbar.demo-only').length") == 1, \
        "[FIX-07] simbar หน้าผู้รับไม่ติด demo-only"
    # ── inject .demo-only{display:none} → ทุก demo element ซ่อน · ไม่มี h-scroll · ไม่เหลือ 'จำลอง' บนแถบ demo ──
    page.add_style_tag(content=".demo-only{display:none !important}")
    settle(page)
    vis = ev(page, "() => [].slice.call(document.querySelectorAll('.demo-only'))"
             ".filter(function(e){var r=e.getBoundingClientRect();return r.width>2&&r.height>2;}).length")
    assert vis == 0, f"[FIX-07] ซ่อน demo-only แล้วยังมี demo element โผล่ {vis} ตัว"
    hscroll = ev(page, "() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
    assert hscroll <= 2, f"[FIX-07] ซ่อน demo-only แล้ว layout พัง (h-scroll {hscroll}px)"
    assert ev(page, "() => (document.getElementById('recipientRoot').innerText||'').indexOf('จำลอง')") == -1, \
        "[FIX-07] ซ่อน demo-only แล้วยังเหลือคำ 'จำลอง' ที่มองเห็นบนหน้าผู้รับ (innerText = เฉพาะข้อความที่เรนเดอร์)"
    return f"demo-strip + ส่วนพรีวิว + rcp-simbar ติด demo-only · ซ่อนแล้ว 0 element โผล่ · ไม่มี h-scroll · ไม่เหลือ 'จำลอง'"


def c_fix08_pill_single(page):
    """[E48 · FIX-08] ตาราง purposes: เซลล์เดียวไม่มี pill ≥2 (Rule #103/#40 · แยกคอลัมน์สถานะ)"""
    open_(page)
    go_tab(page, "purposes")
    maxpill = ev(page, "() => Math.max.apply(null,[0].concat([].slice.call("
                "document.querySelectorAll('.table tbody td')).map(function(td){return td.querySelectorAll('.pill').length;})))")
    assert maxpill <= 1, f"[FIX-08] ตาราง purposes มีเซลล์ที่ใส่ pill {maxpill} ตัว (ต้องแยกคอลัมน์ · ≤1)"
    # แต่ละแถวยังมี pill สถานะ 1 ตัว (ไม่ได้หายไป)
    nrow = ev(page, "() => document.querySelectorAll('.table tbody tr').length")
    npill = ev(page, "() => document.querySelectorAll('.table tbody .pill').length")
    assert npill >= nrow, f"[FIX-08] แถว purposes บางแถวไม่มี pill สถานะ (rows={nrow} pills={npill})"
    return f"ตาราง purposes: เซลล์สูงสุด {maxpill} pill (≤1) · {nrow} แถวมี pill สถานะครบ ({npill})"


# ═══════════════════════════════ RUN ═══════════════════════════════

# (case-id, fn, FN codes ที่เคสนี้ครอบ)
CASES = [
    ("E01", c_fn01, ["FN-01"]),
    ("E02", c_fn02, ["FN-02"]),
    ("E03", c_fn03, ["FN-03"]),
    ("E04", c_fn04, ["FN-04"]),
    ("E05", c_fn05, ["FN-05"]),
    ("E06", c_fn06, ["FN-06"]),
    ("E07", c_fn07, ["FN-07"]),
    ("E08", c_fn08, ["FN-08"]),
    ("E09", c_fn09, ["FN-09"]),
    ("E10", c_fn10, ["FN-10"]),
    ("E11", c_fn11, ["FN-11"]),
    ("E12", c_fn12, ["FN-12"]),
    ("E13", c_fn13, ["FN-13"]),
    ("E14", c_fn14, ["FN-14"]),
    ("E15", c_fn15, ["FN-15"]),
    ("E16", c_fn16, ["FN-16"]),
    ("E17", c_fn17, ["FN-17"]),
    ("E18", c_fn18, ["FN-18"]),
    ("E19", c_fn19, ["FN-19"]),
    ("E20", c_fn20, ["FN-20"]),
    ("N40.10", c_neg40_10, []),
    ("N40.5/6", c_neg40_pipes, []),
    ("N40.4", c_neg40_value, []),
    ("N40.1", c_neg40_cookie, []),
    ("N40.2", c_neg40_approval, []),
    ("N40.8", c_neg40_lapsed, []),
    ("N40.7", c_neg40_triple, []),
    ("DSP01", c_dsp01_modal_over_drawer, []),
    ("DSP02", c_dsp02_combobox, []),
    ("DSP04", c_dsp04_affordances, []),
    ("RCP", c_recipient_overlay, []),
    ("E33", c_e33_filter_gap, []),
    ("E34", c_e34_button_gap, []),
    ("E35", c_e35_modal_warn, []),
    ("E36", c_e36_purview_footer_gap, []),
    ("E37", c_e37_qr_actions_gap, []),
    ("ESC", c_esc_chain, []),
    ("GBG", c_no_garbage, []),
    ("E38", c_e38_feature_name, []),
    ("E39", c_e39_view_policy, []),
    ("E40", c_e40_search_focus, []),
    ("E41", c_fix01_answer_once, []),
    ("E42", c_fix02_persona_guard, []),
    ("E43", c_fix04_double_submit, []),
    ("E44", c_fix05_substatus_guard, []),
    ("E45", c_fix03_send_snapshot, []),
    ("E46", c_fix06_contract_anchors, []),
    ("E47", c_fix07_demo_only, []),
    ("E48", c_fix08_pill_single, []),
]

ALL_FN = ["FN-%02d" % i for i in range(1, 21)]


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        suite.watch(page)
        covered = {}
        for tid, fn, fns in CASES:
            suite.check(tid, fn.__doc__.strip().splitlines()[0], lambda fn=fn: fn(page))
            status = suite.results[-1][2]
            for code in fns:
                # ครอบ = มีเคส และเคสนั้น PASS
                covered[code] = covered.get(code, False) or (status == "PASS")
        browser.close()

    ok = suite.report(exit_on_fail=False)
    total = len(suite.results)

    # ── FN coverage tally (ตัวหาร) ──
    print()
    have_case = sorted(covered.keys())
    passed_fn = [c for c in ALL_FN if covered.get(c)]
    missing = [c for c in ALL_FN if c not in have_case]
    failed_fn = [c for c in ALL_FN if c in have_case and not covered.get(c)]
    print("── FN coverage ──")
    for c in ALL_FN:
        mark = "PASS" if covered.get(c) else ("FAIL" if c in have_case else "MISSING")
        print(f"  {c}: {mark}")
    if missing:
        print("  ! FN ที่ไม่มีเคส:", ", ".join(missing))
    if failed_fn:
        print("  ! FN ที่มีเคสแต่ยังตก:", ", ".join(failed_fn))
    print()
    print(f"FN ครอบ {len(passed_fn)}/20 · เคสรวม {total} · ผ่าน {ok}/{total}")
    sys.exit(0 if ok == total and len(passed_fn) == 20 and not suite.console_errors else 1)


if __name__ == "__main__":
    main()
