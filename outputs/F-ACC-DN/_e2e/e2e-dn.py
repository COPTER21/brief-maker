#!/usr/bin/env python3
"""E2E · F-ACC-DN · ใบลดหนี้ผู้ขาย (Debit Note · AP) — WF-01 Step 5 (ตัวหนัก)

รันไทม์ตัวเดียวที่ต้องพิสูจน์ COMPLETENESS: ทุก FN (22 FN = FN-01..18 + FN-19 ส่วนลดท้ายบิล
(user KEEP 2026-09-22 · ยังไม่อยู่ใน pack checklist → carry step-12 governance) + FN-90/91/92)
มีเคส ≥1 (ติดรหัสในชื่อเคส) + negatives = "เรนเดอร์จริงแล้ว
assert ว่าของที่ไม่รองรับเข้าไม่ถึง" (ฟีเจอร์นี้ไม่มี FN-40 numbered · negatives อยู่ในหมวด
"สิ่งที่ไม่รองรับ": ลดลอยไม่อ้างใบ · เรียกเงินคืน · ยกเลิกหลังอนุมัติ · RTV CRUD).

ยึด helper ของ uikit เท่านั้น (ready/settle/after + assert_* กลาง) — ไม่มี wait_for_timeout,
ไม่เขียนตัวตรวจ UI generic ใหม่. ขับหน้าจอผ่าน controller function จริงของไฟล์ (pickInv /
setReason / pickRTV / updateLine / wizardNext / openSubmitModal / comboPick / confirmSubmit /
openApproveModal / confirmApprove / openRejectModal / openCancelDN / openSendDN / demoPay /
renderRefTab / renderPdfTab) + real DOM แล้ว assert ทั้ง data model และสิ่งที่เรนเดอร์.
reload หน้าใหม่ต่อเคส → mock RECS/DOC reset = เคสอิสระต่อกัน.

C3.8 wired: assert_modal_card_topmost (DSP-08 · modal-card-above-backdrop) + assert_status_guard
(bypass ปุ่มซ่อนแต่ controller เรียกได้ · C1/C2/C4).

รัน: PYTHONIOENCODING=utf-8 .claude/venv/Scripts/python.exe \
       outputs/F-ACC-DN/_e2e/e2e-dn.py outputs/F-ACC-DN/F-ACC-DN_debit-note.html
"""
from pathlib import Path
import sys
import re
import tempfile

from playwright.sync_api import sync_playwright

OUTPUTS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(OUTPUTS / "_SHARED" / "_e2e"))
from uikit import (  # noqa: E402
    Suite, ready, settle as shared_settle, after as shared_after,
    assert_text_absent, assert_modal_card_topmost, assert_status_guard,
    assert_line_cap_display_matches_enforced,
)

HTML = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parents[1] / "F-ACC-DN_debit-note.html").resolve()
BASE = HTML.as_uri()

suite = Suite("F-ACC-DN · ใบลดหนี้ผู้ขาย")


def ev(page, js):
    return page.evaluate(js)


def after(page, js, timeout=2500):
    return shared_after(page, js, timeout=timeout)


def settle(page, timeout=2000):
    shared_settle(page, timeout=timeout)


def open_(page, url=BASE):
    ready(page, url, timeout=9000)
    page.wait_for_function(
        "()=>{const e=document.getElementById('page-content');return e&&e.innerHTML.trim().length>0;}",
        timeout=9000)


def open_create(page):
    after(page, "()=>openCreateDrawer(null)")
    page.wait_for_function("()=>document.getElementById('create-drawer-content')&&createWizard.data", timeout=4000)


def goto_step(page, n):
    after(page, "()=>{createWizard.step=%d;renderCreateDrawer();}" % n)


def create_text(page):
    return ev(page, "()=>(document.getElementById('create-drawer-content')||{}).textContent||''")


def view_text(page):
    return ev(page, "()=>(document.getElementById('view-drawer-content')||{}).textContent||''")


def open_view(page, rid):
    after(page, "()=>openViewDrawer('%s')" % rid)
    page.wait_for_function("()=>document.getElementById('view-drawer-content')", timeout=4000)


def view_tab(page, tab):
    after(page, "()=>{viewState.tab='%s';renderViewDrawer();}" % tab)


def persona(page, i):
    after(page, "()=>switchPersona(%d)" % i)


def last_toast(page):
    return ev(page, "()=>{const r=document.getElementById('toast-root');if(!r)return '';"
                    "const t=r.querySelectorAll('.toast');return t.length?t[t.length-1].textContent:'';}")


def has_modal(page):
    return ev(page, "()=>!!document.querySelector('.modal-overlay')")


# ═══════════════════════════ หมวด 1 · อ้างใบตั้งหนี้ ═══════════════════════════

def c_fn01(page):
    """[FN-01 · S-01 · BR-01] เลือกใบตั้งหนี้ค้างจ่าย เห็นยอดสุทธิ/จ่าย+ลดหนี้แล้ว/คงค้าง"""
    open_(page); open_create(page)
    body = create_text(page)
    assert "ยอดสุทธิ" in body and "จ่าย + ลดหนี้แล้ว" in body and "คงค้าง" in body, "step1 picker ไม่มี 3 คอลัมน์ยอด"
    grand = ev(page, "()=>invGrand(INV_BY['API-2026-0041'])")
    applied = ev(page, "()=>dnApplied('API-2026-0041',null)")
    out = ev(page, "()=>invOutstanding('API-2026-0041',null)")
    assert applied > 0, "API-0041 ควรมียอดลดหนี้แล้ว (DN-0011 sent) แต่ dnApplied=0"
    assert abs(out - (grand - ev(page, "()=>INV_BY['API-2026-0041'].paid") - applied)) < 0.01, \
        f"คงค้าง != สุทธิ−จ่าย−ลดแล้ว ({out})"
    after(page, "()=>pickInv('API-2026-0041')")
    assert ev(page, "()=>createWizard.data.inv") == "API-2026-0041", "เลือกใบแล้ว inv ไม่ติด"
    assert ev(page, "()=>createWizard.data.partner") == "V-2001", "เลือกใบแล้วผู้ขายไม่ถูกดึง"
    return f"เลือก 0041 → สุทธิ ฿{grand:,.0f} · ลดแล้ว ฿{applied:,.0f} · คงค้าง ฿{out:,.0f}"


def c_fn02(page):
    """[FN-02 · S-12 · OQ-DN-01] tile 'ลดหนี้ไม่อ้างใบ' present แต่ปิดไว้ (เริ่ม path นั้นไม่ได้)"""
    open_(page); open_create(page)
    body = create_text(page)
    assert "ลดหนี้ไม่อ้างใบ" in body and "ปิดไว้" in body, "step1 ไม่มี tile 'ลดหนี้ไม่อ้างใบ' + ป้าย 'ปิดไว้'"
    r = ev(page, """()=>{const bs=[...document.querySelectorAll('#create-drawer-content button')]
        .filter(b=>/ลดหนี้ไม่อ้างใบ/.test(b.textContent));
        if(!bs.length) return null; const b=bs[0];
        return {cur:getComputedStyle(b).cursor, oc:(b.getAttribute('onclick')||'')};}""")
    assert r, "ไม่พบปุ่ม tile ลดหนี้ไม่อ้างใบ"
    assert r["cur"] == "not-allowed", f"tile ปิดไว้แต่ cursor ไม่ใช่ not-allowed ({r['cur']})"
    assert "showToast" in r["oc"] and "setSource" not in r["oc"], f"tile ปิดไว้ยังผูก path สร้างจริง: {r['oc']}"
    st0 = ev(page, "()=>createWizard.data.source_type")
    after(page, """()=>{const b=[...document.querySelectorAll('#create-drawer-content button')]
        .filter(x=>/ลดหนี้ไม่อ้างใบ/.test(x.textContent))[0]; if(b) b.click();}""")
    assert ev(page, "()=>createWizard.data.source_type") == st0, "กด tile ปิดไว้แล้ว source_type เปลี่ยน (path ลอยเปิด)"
    assert "ปิดไว้" in last_toast(page) or "OQ-DN-01" in last_toast(page), f"กด tile ปิดไว้ไม่เตือน ({last_toast(page)})"
    return "tile 'ลดหนี้ไม่อ้างใบ' present · cursor not-allowed · onclick=showToast · กดแล้ว source ไม่เปลี่ยน"


def c_fn03(page):
    """[FN-03 · S-01] เลือกใบ → ผู้ขาย/เลขใบกำกับเดิม/เลขภาษี/บรรทัดของใบเดิมถูกดึงมา"""
    open_(page); open_create(page)
    after(page, "()=>pickInv('API-2026-0041')")
    d = ev(page, "()=>({partner:createWizard.data.partner, nlines:createWizard.data.lines.length, "
                 "item:createWizard.data.lines[0].item_code, src:createWizard.data.lines[0].src_line})")
    p = ev(page, "()=>PARTNER_BY['V-2001']")
    iv = ev(page, "()=>INV_BY['API-2026-0041']")
    assert d["partner"] == "V-2001", "ผู้ขายไม่ถูกดึง"
    assert d["nlines"] == 2 and d["item"] == "P-1002", f"บรรทัดใบเดิมไม่ถูกดึง ({d})"
    assert d["src"] == "API-2026-0041|0", "บรรทัดไม่ผูก src_line กับใบเดิม"
    goto_step(page, 2)
    b = ev(page, "()=>document.getElementById('create-drawer-content').innerHTML")
    assert p["taxId"] in b and iv["vinv"] in b, "step2 ไม่แสดงเลขภาษีผู้ขาย/เลขใบกำกับเดิม"
    return f"เลือก 0041 → V-2001 · taxId {p['taxId']} · ใบกำกับ {iv['vinv']} · 2 บรรทัด (P-1002/P-1001) จากใบเดิม"


def c_fn04(page):
    """[FN-04 · S-13 · BR-13 · FIX-01] ใบจ่ายครบ (0038) ออก DN ได้ (คืนของหลังจ่าย) · ใบที่ลดเต็มมูลค่าแล้วไม่โผล่"""
    open_(page); open_create(page)
    keys = ev(page, "()=>invList().map(x=>x.key)")
    # FIX-01 กลับด้าน S-13: ใบจ่ายครบต้องออก DN ได้ (dnRoom = มูลค่าใบ > 0)
    assert "API-2026-0038" in keys, "ใบจ่ายครบ 0038 ต้องออกใบลดหนี้ได้ (FIX-01 · คืนของหลังจ่าย)"
    assert ev(page, "()=>invOutstanding('API-2026-0038',null)") < 0.005, "0038 outstanding=0 (จ่ายครบ)"
    assert ev(page, "()=>dnRoom('API-2026-0038',null)") > 0.005, "0038 dnRoom (มูลค่าที่ลดได้) ต้อง > 0"
    assert "API-2026-0038" in create_text(page), "ตาราง picker ควรเรนเดอร์ใบจ่ายครบ 0038"
    # ใบที่ลดหนี้เต็มมูลค่าแล้ว (dnRoom=0) → ไม่โผล่ (inject approved DN grand=invGrand ของ 0044)
    gone = ev(page, """()=>{ const iv=INV_BY['API-2026-0044']; const g=invGrand(iv);
        RECS.push({id:'RCT',inv:'API-2026-0044',partner:iv.vendor,status:'approved',reason:'SHORT',
          reasonText:'full-credit test',rtv:'',vendorCn:'',dnDate:TODAY_ISO,
          lines:[{item_code:'X-5101',item_name:'x',qty:1,unit_price:18000,vat_mode:'add',vat_pct:7,src_line:'API-2026-0044|0'}],
          endbill:{enabled:false,mode:'percent',value:0},attachments:[]});
        const room=dnRoom('API-2026-0044',null); const inList=invList().map(x=>x.key).includes('API-2026-0044');
        RECS.pop(); return {room, inList}; }""")
    assert gone["room"] < 0.005 and gone["inList"] is False, f"ใบที่ลดเต็มมูลค่าแล้วยังโผล่ ({gone})"
    return "0038 จ่ายครบ → ออก DN ได้ (dnRoom>0 · เกิดเครดิตคงเหลือ) · ใบที่ลดเต็มมูลค่าแล้วไม่โผล่"


# ═══════════════════════════ หมวด 2 · เหตุผลและยอดลด ═══════════════════════════

def c_fn05(page):
    """[FN-05 · S-01 · BR-06] คืนสินค้า (RTV) ต้องเลือกใบคืนสินค้า · จำนวนมาจาก RTV (ของใบเดียวกัน)"""
    open_(page); open_create(page)
    after(page, "()=>pickInv('API-2026-0041')")   # reason default RTV
    after(page, "()=>setReason('RTV')")
    goto_step(page, 2)
    b = create_text(page)
    assert "RTV-2026-0007" in b and "RTV-2026-0010" in b, "dropdown RTV ไม่มีใบคืนสินค้าของ 0041"
    assert "RTV-2026-0009" not in b, "dropdown RTV หลุดใบคืนของใบอื่น (RTV-0009=API-0046)"
    after(page, "()=>pickRTV('RTV-2026-0010')")     # คืน line0 · 2 กล่อง
    d = ev(page, "()=>({rtv:createWizard.data.rtv, qty:createWizard.data.lines[0].qty, "
                 "max:createWizard.data.lines[0].max, src:createWizard.data.lines[0].src_line})")
    assert d["rtv"] == "RTV-2026-0010", "เลือกใบคืนสินค้าแล้วไม่ติด"
    assert d["qty"] == 2 and d["max"] == 2, f"จำนวนไม่ได้มาจากใบคืนสินค้า (คาด 2, ได้ {d})"
    assert d["src"] == "API-2026-0041|0", "บรรทัดไม่ตรง line ของ RTV"
    return "RTV → เลือก RTV-2026-0010 (2 กล่อง) · จำนวน=2 · cap=2 (จากใบคืนสินค้า) · dropdown เฉพาะ RTV ของ 0041"


def c_fn06(page):
    """[FN-06 · S-02 · BR-04] ราคาเกิน (OVERPRICE) ลดราคาต่อหน่วยได้ แต่ไม่เกินราคาเดิม"""
    open_(page); open_create(page)
    after(page, "()=>pickInv('API-2026-0043')")     # P-1004 x5 @4100
    after(page, "()=>setReason('OVERPRICE')")        # price mode
    lid = ev(page, "()=>createWizard.data.lines[0].id")
    orig = ev(page, "()=>createWizard.data.lines[0].origPrice")   # 4100
    goto_step(page, 3)
    after(page, "()=>updateLine('%s','unit_price',%d)" % (lid, orig + 500))
    after(page, "()=>wizardNext()")
    assert ev(page, "()=>createWizard.step") == 3, "ราคาลดเกินราคาเดิมแต่ยังก้าวต่อได้"
    assert "เกินราคาเดิม" in last_toast(page), f"ราคาเกินไม่เตือน ({last_toast(page)})"
    assert "ราคาลดเกินราคาเดิม" in create_text(page), "ไม่มี meta เตือนราคาลดเกินราคาเดิมใต้บรรทัด"
    after(page, "()=>updateLine('%s','unit_price',200)" % lid)
    after(page, "()=>wizardNext()")
    assert ev(page, "()=>createWizard.step") == 4, f"ราคา ≤ เดิมแล้วยังก้าวต่อไม่ได้ ({last_toast(page)})"
    return f"OVERPRICE · ราคา {orig+500} > เดิม {orig} → บล็อก · ราคา 200 ≤ เดิม → ผ่าน"


def c_fn07(page):
    """[FN-07 · S-03 · BR-03] ของขาด (SHORT): ลดเฉพาะบรรทัดที่เลือก · ลบ/เพิ่มบรรทัดเดิมกลับได้"""
    open_(page); open_create(page)
    after(page, "()=>pickInv('API-2026-0041')")     # 2 บรรทัด
    after(page, "()=>setReason('SHORT')")
    n0 = ev(page, "()=>createWizard.data.lines.length")
    assert n0 == 2, f"ใบ 0041 ควรดึง 2 บรรทัด (ได้ {n0})"
    rm = ev(page, "()=>createWizard.data.lines[1].id")
    after(page, "()=>removeLine('%s')" % rm)
    assert ev(page, "()=>createWizard.data.lines.length") == 1, "ลบบรรทัดอื่นออกไม่ได้"
    goto_step(page, 3)
    assert "readdLine" in ev(page, "()=>document.getElementById('create-drawer-content').innerHTML"), \
        "ไม่มีปุ่มเพิ่มบรรทัดใบเดิมที่ลบออกกลับเข้ามา (step3Block)"
    after(page, "()=>readdLine(1)")
    assert ev(page, "()=>createWizard.data.lines.length") == 2, "readdLine ไม่คืนบรรทัด"
    return "ใบ 2 บรรทัด → ลบเหลือ 1 (ลดเฉพาะบรรทัดที่เลือก) · step3Block ให้เพิ่มบรรทัดเดิมกลับได้"


def c_fn08(page):
    """[FN-08 · S-04 · BR-03,BR-10] ลดหลายรอบ: บรรทัดแสดงจำนวนเดิม · ลดแล้ว · ลดได้อีก ถูกต้อง"""
    open_(page); open_create(page)
    after(page, "()=>pickInv('API-2026-0041')")     # line0 20 ก. · มี R6(draft RTV 2) ลดแล้ว
    after(page, "()=>setReason('SHORT')")
    room = ev(page, "()=>lineRoom('API-2026-0041',0,null)")
    assert room["origQty"] == 20, f"จำนวนเดิมผิด ({room['origQty']})"
    assert room["netDone"] > 0, "ลดแล้ว (netDone) = 0 ทั้งที่ควรมีรอบก่อน (R6 draft)"
    assert room["qtyLeft"] == 18, f"ลดได้อีกผิด (คาด 18, ได้ {room['qtyLeft']})"
    goto_step(page, 3)
    b = create_text(page)
    assert "ใบเดิม 20" in b, "meta ไม่แสดงจำนวนเดิม 20"
    assert "ลดแล้ว" in b and "ลดจำนวนได้อีก 18" in b, "meta ลดแล้ว/ลดได้อีกไม่ถูก"
    return f"ลดหลายรอบ 0041: เดิม 20 · ลดแล้ว ฿{room['netDone']:,.0f} · ลดจำนวนได้อีก {room['qtyLeft']}"


def c_cap_display(page):
    """[FN-05/FN-08 · BR-06 · C3.8] เลขที่โชว์ 'ลดจำนวนได้อีก N' = เพดานที่บังคับจริง (RTV-capped l.max)"""
    open_(page); open_create(page)
    after(page, "()=>pickInv('API-2026-0041')")     # line0 room.qtyLeft=18 (R6 draft ลดแล้ว 2)
    after(page, "()=>setReason('RTV')")
    after(page, "()=>pickRTV('RTV-2026-0010')")      # RTV คืน 2 → l.max=2 (แคบกว่า room 18)
    goto_step(page, 3)
    r = assert_line_cap_display_matches_enforced(
        page, "updateLine(createWizard.data.lines[0].id,'qty',{v})", note="RTV-0010 (cap<room)",
        scope="#create-drawer-content")
    assert abs(r["cap"] - 2) < 1e-9, f"เลขที่โชว์ควร = 2 (ตามใบคืนสินค้า) แต่ได้ {r['cap']} · meta: {r['metaText']}"
    assert r["suffix"], f"เพดานมาจากใบคืนสินค้า (l.max<room) ต้องต่อท้าย '(ตามใบรับคืน)' · meta: {r['metaText']}"
    return f"RTV-0010: โชว์ 'ลดจำนวนได้อีก {int(r['cap'])} (ตามใบรับคืน)' · qty=2 ok · qty=3 แดง (display=enforcement)"


def c_fn09(page):
    """[FN-09 · S-05 · BR-02] ยอดลดเกินคงเหลือ/เกินจำนวน → บล็อก + hard-warn บอกยอด"""
    open_(page); open_create(page)
    after(page, "()=>pickInv('API-2026-0041')")
    after(page, "()=>setReason('SHORT')")
    lid = ev(page, "()=>createWizard.data.lines[0].id")
    mx = ev(page, "()=>createWizard.data.lines[0].max")     # 18
    goto_step(page, 3)
    after(page, "()=>updateLine('%s','qty',%d)" % (lid, mx + 50))   # เกินจำนวน + เกินคงเหลือ
    b = create_text(page)
    assert "ยอดลดหนี้เกินมูลค่าที่ลดได้" in b, "ไม่มี hard-warn ยอดเกินมูลค่าที่ลดได้ (FIX-01)"
    assert "เกิน ฿" in b, "hard-warn ไม่บอกยอดที่เกิน"
    ov = ev(page, "()=>dnOver(createWizard.data)")
    assert ov and ov["over"] > 0, "dnOver ไม่จับยอดเกิน"
    after(page, "()=>wizardNext()")
    assert ev(page, "()=>createWizard.step") == 3, "ยอด/จำนวนเกินแต่ยังก้าวต่อได้"
    assert "ลดได้อีก" in last_toast(page), f"เกินจำนวนไม่เตือนยอดที่ลดได้ ({last_toast(page)})"
    assert ev(page, "()=>DOC.blockReason(createWizard.data)").startswith("ยอดลดหนี้เกิน"), "blockReason ไม่บล็อกยอดเกิน"
    return f"qty {mx+50} > cap {mx} → hard-warn บอกยอดเกิน · wizardNext บล็อก · blockReason บล็อก"


def c_fn10(page):
    """[FN-10 · BR-05] ต้องกรอกคำอธิบายเหตุผล ≥ 10 ตัวอักษร"""
    open_(page); open_create(page)
    after(page, "()=>pickInv('API-2026-0041')")
    after(page, "()=>setReason('RTV')")
    after(page, "()=>pickRTV('RTV-2026-0010')")
    goto_step(page, 2)
    after(page, "()=>{createWizard.data.reasonText='สั้น';renderCreateDrawer();}")   # < 10
    after(page, "()=>wizardNext()")
    assert ev(page, "()=>createWizard.step") == 2, "คำอธิบาย < 10 ตัวแต่ก้าวต่อได้"
    assert ev(page, "()=>document.getElementById('f-reasonText').classList.contains('is-error')"), \
        "ช่องคำอธิบายไม่ขึ้น error"
    after(page, "()=>{createWizard.data.reasonText='คืนสินค้าชำรุด 2 กล่อง';renderCreateDrawer();}")   # ≥ 10
    after(page, "()=>wizardNext()")
    assert ev(page, "()=>createWizard.step") == 3, f"คำอธิบาย ≥ 10 ตัวแล้วยังก้าวต่อไม่ได้ ({last_toast(page)})"
    return "คำอธิบาย 'สั้น' (<10) → บล็อก + field error · ≥10 ตัว → ผ่านไป step 3"


# ═══════════════════════════ หมวด 3 · อนุมัติ (DOA) ═══════════════════════════

def c_fn11(page):
    """[FN-11 · S-06 · BR-07] ส่งอนุมัติ: สายเปลี่ยนตามมูลค่า และต้องเลือกคนครบทุกขั้น"""
    open_(page)
    t1 = ev(page, "()=>resolveDoa({lines:[{qty:1,unit_price:1000,vat_mode:'add',vat_pct:7}],endbill:{}}).steps.length")
    t2 = ev(page, "()=>resolveDoa({lines:[{qty:1,unit_price:100000,vat_mode:'add',vat_pct:7}],endbill:{}}).steps.length")
    t3 = ev(page, "()=>resolveDoa({lines:[{qty:1,unit_price:400000,vat_mode:'add',vat_pct:7}],endbill:{}}).steps.length")
    assert (t1, t2, t3) == (1, 2, 3), f"สายไม่เปลี่ยนตามมูลค่า (ได้ {t1}/{t2}/{t3} · ต้อง 1/2/3)"
    after(page, "()=>openSubmitModal('R6')")          # draft ยอดต่ำ → 1 slot (mgr-pur)
    nslot = ev(page, "()=>modalState.slots.length")
    assert nslot == ev(page, "()=>resolveDoa(findRec('R6')).steps.length"), "จำนวน slot ไม่ตรง resolveDoa"
    after(page, "()=>confirmSubmit()")
    assert ev(page, "()=>findRec('R6').status") == "draft", "slot ว่างแต่ส่งอนุมัติผ่าน"
    assert ev(page, "()=>modalState.err") is True, "slot ว่างไม่ถูก mark error"
    after(page, "()=>comboPick('slot-0','สมศักดิ์ จัดซื้อ')")
    assert ev(page, "()=>modalState.slots[0].assignee") == "สมศักดิ์ จัดซื้อ", "เลือกคนแล้วไม่ติด"
    after(page, "()=>confirmSubmit()")
    d = ev(page, "()=>findRec('R6')")
    assert d["status"] == "pending_approval", "เลือกครบแล้วส่งอนุมัติไม่สำเร็จ"
    assert d["approval_chain"][0]["assignee"] == "สมศักดิ์ จัดซื้อ", "chain ไม่บันทึกคนที่เลือก"
    return "tier ตามมูลค่า 1/2/3 · R6 slot ว่าง → บล็อก · เลือกคน → pending (คน=สมศักดิ์ จัดซื้อ)"


def c_fn12(page):
    """[FN-12 · S-06 · BR-08] อนุมัติครบสาย → เลข DN-ปี-ลำดับ + สถานะ 'อนุมัติแล้ว'"""
    open_(page)
    assert ev(page, "()=>findRec('R4').status") == "pending_approval"
    assert ev(page, "()=>findRec('R4').code") == "", "ก่อนอนุมัติครบต้องยังไม่มีเลข DN"
    persona(page, 1)   # สมศักดิ์ (mgr-pur) — ขั้น 1
    after(page, "()=>confirmApprove('R4')")
    assert ev(page, "()=>findRec('R4').status") == "pending_approval", "อนุมัติขั้น 1 แล้วข้ามไป approved"
    assert ev(page, "()=>findRec('R4').approval_chain[0].status") == "approved", "ขั้น 1 ไม่ถูก mark approved"
    persona(page, 2)   # ประเสริฐ (mgr-acc) — ขั้นสุดท้าย
    after(page, "()=>confirmApprove('R4')")
    d = ev(page, "()=>findRec('R4')")
    assert d["status"] == "approved", "อนุมัติครบแล้วสถานะไม่ใช่ approved"
    assert d["code"] and re.match(r"^DN-2026-\d{4}$", d["code"]), f"เลขที่ไม่ใช่ DN-2026-NNNN (ได้ {d['code']})"
    assert "อนุมัติแล้ว" in ev(page, "()=>docPill('approved')"), "pill approved ไม่แสดง 'อนุมัติแล้ว'"
    return f"R4 อนุมัติ 2 ขั้น (สมศักดิ์→ประเสริฐ) → ออกเลข {d['code']} (ค.ศ.) · status=approved 'อนุมัติแล้ว'"


def c_fn13(page):
    """[FN-13 · S-07] ไม่อนุมัติต้องใส่เหตุผล → กลับเป็นร่าง + เห็นรอบก่อนหน้า (append-only)"""
    open_(page)
    # R5 = pending 3 ขั้น (สมศักดิ์ approved · ประเสริฐ pending ปัจจุบัน · อรุณี)
    persona(page, 2)   # ประเสริฐ = ขั้นปัจจุบัน
    n_hist0 = ev(page, "()=>(findRec('R5').approval_history||[]).length")
    after(page, "()=>openRejectModal('R5')")
    after(page, "()=>document.getElementById('md-ok').click()")   # เหตุผลว่าง → เตือน ไม่ตีกลับ
    assert ev(page, "()=>findRec('R5').status") == "pending_approval", "เหตุผลว่างแต่ตีกลับได้"
    assert "เหตุผล" in last_toast(page), f"เหตุผลว่างไม่เตือน ({last_toast(page)})"
    after(page, "()=>{document.getElementById('md-reason').value='ราคาไม่ตรง PO ตรวจใหม่';document.getElementById('md-ok').click();}")
    d = ev(page, "()=>findRec('R5')")
    assert d["status"] == "draft", "ตีกลับแล้วไม่เป็นร่าง"
    assert (d["approval_history"] or []) and len(d["approval_history"]) == n_hist0 + 1, "รอบก่อนหน้าไม่ถูกเก็บ (append-only)"
    open_view(page, "R5"); view_tab(page, "sign")
    assert "รอบก่อนหน้า" in view_text(page), "sign tab ไม่แสดงรอบก่อนหน้าที่ถูกตีกลับ"
    return "R5 ตีกลับ: เหตุผลว่าง→บล็อก · ใส่เหตุผล→draft + approval_history +1 · sign tab เห็นรอบก่อน"


def c_fn14(page):
    """[FN-14 · S-08] ผู้ส่งไม่เห็นปุ่มอนุมัติใบของตัวเอง (SoD · render-assert)"""
    open_(page)
    # ME default = สุภาพร เจ้าหนี้ดี = ผู้ส่ง R4/R5 → canActStep=false
    assert ev(page, "()=>findRec('R4').submittedBy") == "สุภาพร เจ้าหนี้ดี" == ev(page, "()=>ME.name")
    acts = ev(page, "()=>DOC.viewActions(findRec('R4'), 'pending_approval')")
    assert "openApproveModal" not in acts, "ผู้ส่งเห็นปุ่มอนุมัติใบตัวเอง (SoD หลุด)"
    assert "openRejectModal" not in acts, "ผู้ส่งเห็นปุ่มไม่อนุมัติใบตัวเอง"
    assert ev(page, "()=>canActStep(findRec('R4'))") is False, "canActStep ปล่อยให้ผู้ส่งกดอนุมัติเอง"
    open_view(page, "R4"); view_tab(page, "sign")
    html = ev(page, "()=>document.getElementById('view-drawer-content').innerHTML")
    assert "openApproveModal('R4')" not in html, "sign tab โชว์ปุ่มอนุมัติให้ผู้ส่ง"
    return "ผู้ส่ง (สุภาพร) เปิด R4: viewActions/sign ไม่มีปุ่มอนุมัติ/ไม่อนุมัติ · canActStep=false"


def c_fn17(page):
    """[FN-17 · S-11 · BR-02/13 · FIX-01] เพดานที่ลดได้ลดลงระหว่างรออนุมัติ (ใบลดหนี้อื่นอนุมัติเพิ่ม) → อนุมัติขั้นสุดท้ายไม่ได้"""
    open_(page)
    persona(page, 1)   # สมศักดิ์ = ขั้น 1 ของ R4
    after(page, "()=>confirmApprove('R4')")   # ขั้น 1 ผ่าน → เหลือขั้น 2 (ประเสริฐ, ขั้นสุดท้าย)
    assert ev(page, "()=>findRec('R4').approval_chain[1].status") == "pending"
    grand = ev(page, "()=>totals(findRec('R4')).grand")
    after(page, "()=>demoPay('R4')")
    assert ev(page, "()=>!!document.getElementById('md-amt')"), "harness ไม่เปิด modal จำลอง (S-11)"
    after(page, "()=>document.getElementById('md-ok').click()")   # default = กินเพดานจน room < grand
    room = ev(page, "()=>dnRoom('API-2026-0046','R4')")
    assert room < grand, f"จำลองแล้วเพดานที่ลดได้ ({room}) ควร < ยอดลด ({grand})"
    persona(page, 2)   # ประเสริฐ = ขั้นสุดท้าย
    after(page, "()=>confirmApprove('R4')")
    d = ev(page, "()=>findRec('R4')")
    assert d["status"] == "pending_approval", "เพดานไม่พอแต่อนุมัติครบสายได้ (S-11 หลุด)"
    assert d["approval_chain"][1]["status"] == "pending", "ขั้นสุดท้ายถูก mark approved ทั้งที่เพดานไม่พอ"
    assert "อนุมัติไม่ได้" in last_toast(page) and "มูลค่าที่ลดได้" in last_toast(page), f"ไม่มีข้อความบล็อกเพดานไม่พอ ({last_toast(page)})"
    return f"R4 ขั้น1 ผ่าน · จำลองใบลดหนี้อื่นกินเพดาน 0046 → เพดานเหลือ ฿{room:,.0f} < ยอดลด ฿{grand:,.0f} → ขั้นสุดท้ายบล็อก"


# ═══════════════════════════ หมวด 4 · หลังอนุมัติ ═══════════════════════════

def c_fn15(page):
    """[FN-15 · S-09] ยกเลิกร่าง/รออนุมัติได้พร้อมเหตุผล → cancelled"""
    open_(page)
    after(page, "()=>openCancelDN('R6')")
    after(page, "()=>document.getElementById('md-ok').click()")   # เหตุผลว่าง → เตือน
    assert ev(page, "()=>findRec('R6').status") == "draft", "เหตุผลว่างแต่ยกเลิกได้"
    after(page, "()=>{document.getElementById('md-reason').value='ผู้ขายยกเลิกคำขอ';document.getElementById('md-ok').click();}")
    d6 = ev(page, "()=>findRec('R6')")
    assert d6["status"] == "cancelled" and d6["cancelInfo"]["reason"] == "ผู้ขายยกเลิกคำขอ", "ยกเลิกร่างไม่สำเร็จ/ไม่เก็บเหตุผล"
    after(page, "()=>openCancelDN('R4')")          # รออนุมัติ (ผู้ส่ง = ME)
    after(page, "()=>{document.getElementById('md-reason').value='ถอนจากรออนุมัติ';document.getElementById('md-ok').click();}")
    d4 = ev(page, "()=>findRec('R4')")
    assert d4["status"] == "cancelled", "ยกเลิกใบรออนุมัติไม่สำเร็จ"
    assert all(x["status"] == "cancelled" for x in d4["approval_chain"]), "ยกเลิกแล้ว slot ที่ค้างไม่ถูกปิด"
    return "ยกเลิก R6 (ร่าง) + R4 (รออนุมัติ) พร้อมเหตุผล → cancelled · เหตุผลว่าง→บล็อก"


def c_fn16(page):
    """[FN-16 · S-10] ส่งให้ผู้ขาย → 'ส่งผู้ขายแล้ว' (sent) + snapshot"""
    open_(page)
    assert ev(page, "()=>findRec('R2').status") == "approved", "R2 ควร approved (พร้อมส่ง)"
    after(page, "()=>openSendDN('R2')")
    assert ev(page, "()=>!!document.getElementById('md-ok')"), "openSendDN ไม่เปิด modal"
    after(page, "()=>document.getElementById('md-ok').click()")   # busy + setTimeout 400
    page.wait_for_function("()=>findRec('R2').status==='sent'", timeout=3000)
    d = ev(page, "()=>findRec('R2')")
    assert d["sentAt"] and d["sentBy"], "ส่งแล้วไม่บันทึกเวลา/ผู้ส่ง (snapshot)"
    assert "ส่งผู้ขายแล้ว" in ev(page, "()=>docPill('sent')"), "pill sent ไม่แสดง 'ส่งผู้ขายแล้ว'"
    return "R2 approved → ส่งให้ผู้ขาย → sent 'ส่งผู้ขายแล้ว' · บันทึก sentAt/sentBy"


def c_fn18(page):
    """[FN-18 · S-14 · BR-09] tab ใบตั้งหนี้อ้างอิง: คงค้างก่อน/หลังลด + ภาษีซื้อที่ลด (ติดลบ) + JE (จำลอง)"""
    open_(page)
    ev(page, "()=>{const s=findRec('R2'); s.vendorCn='TFS-TEST'; s.vendorCnDate='2026-09-12';}")  # FIX-02: ให้ ref tab อยู่ state 'ได้รับใบลดหนี้ผู้ขายแล้ว'
    open_view(page, "R2")     # approved → JE renders (applied)
    view_tab(page, "ref")
    b = view_text(page)
    assert "คงค้างก่อนใบนี้" in b and "คงค้างหลังใบนี้" in b, "ref tab ไม่แสดงคงค้างก่อน/หลัง"
    assert "หักจากหนี้ค้าง" in b, "ref tab ไม่แสดงยอดหักจากหนี้ค้าง (FIX-01)"
    assert "input_vat_line ติดลบ" in b and "ภาษีซื้อที่ลด" in b and "ภ.พ.30" in b, "ref tab ไม่แสดงผลกระทบภาษีซื้อ (input_vat_line ติดลบ)"
    assert "รายการบัญชี" in b and "2110 เจ้าหนี้การค้า" in b and "1170 ภาษีซื้อ" in b, "ref tab ไม่แสดง JE (จำลอง)"
    out = ev(page, "()=>invOutstanding(findRec('R2').inv,'R2')")
    grand = ev(page, "()=>totals(findRec('R2')).grand")
    assert out >= 0 and grand > 0, "คำนวณคงค้าง/ยอดลดผิด"
    return "ref tab R2: คงค้างก่อน/หลัง · ภาษีซื้อที่ลด (input_vat_line ติดลบ · ภ.พ.30) · JE 2110/1170 (จำลอง F093)"


def c_fn20(page):
    """[FN-20 · S-13 · BR-13 · FIX-01] ใบจ่ายครบ (0038) ออก DN → แยกหักหนี้ค้าง/เครดิตคงเหลือ · card+section รายผู้ขาย"""
    open_(page); open_create(page)
    after(page, "()=>pickInv('API-2026-0038')")
    after(page, "()=>setReason('SHORT')")     # ลดจำนวน
    goto_step(page, 3)
    sp = ev(page, "()=>{const d=createWizard.data; const g=totals(d).grand; return {g, sp:dnSplit(d.inv,g,createWizard.editId), out:invOutstanding('API-2026-0038',null)};}")
    assert sp["out"] < 0.005, "0038 ควร outstanding=0 (จ่ายครบ)"
    assert sp["sp"]["applyToAp"] < 0.005, f"จ่ายครบ → หักหนี้ค้างควร=0 ({sp['sp']})"
    assert sp["sp"]["vendorCredit"] > 0.005, f"จ่ายครบ → ต้องเกิดเครดิตคงเหลือ ({sp['sp']})"
    assert "เครดิตคงเหลือกับผู้ขาย" in create_text(page), "wizard summary ไม่แสดงเครดิตคงเหลือ"
    # build เป็น pending → approveGuard ขั้นสุดท้าย 'ต้องไม่บล็อก' (ใบจ่ายครบ = เครดิตคงเหลือ · FIX-01 · กันบั๊ก approveGuard เทียบ outstanding)
    ev(page, """()=>{ const d=createWizard.data; const s=DOC.buildRecord(d); s.id='RVC'; s.status='pending_approval';
        s.submittedBy='x'; s.approval_chain=[{roles:['role-mgr-pur'],assignee:'a',status:'pending'}]; RECS.push(s); }""")
    guard = ev(page, "()=>DOC.approveGuard(findRec('RVC'), true)")
    assert guard == "", f"approveGuard บล็อกการอนุมัติใบจ่ายครบผิด (vendor credit ต้องอนุมัติได้) — ได้ '{guard}'"
    ev(page, "()=>DOC.onFinalApprove(findRec('RVC'))")
    st = ev(page, "()=>({vc:findRec('RVC').vendorCredit, ap:findRec('RVC').applyToAp, status:findRec('RVC').status})")
    assert st["status"] == "approved" and st["vc"] > 0.005 and st["ap"] < 0.005, f"onFinalApprove ไม่เก็บ vendorCredit ({st})"
    after(page, "()=>navigate('list')")
    lb = ev(page, "()=>document.getElementById('page-content').textContent")
    # ตารางเต็มเหมือนเดิม: KPI card เครดิตอยู่ใน stat-row · รายละเอียดรายผู้ขาย = modal (ไม่แทรกในหน้า list · กันตารางโดนบีบ)
    assert "เครดิตคงเหลือกับผู้ขาย" in lb, "list ไม่มี KPI card เครดิตคงเหลือ"
    assert "เครดิตคงเหลือรายผู้ขาย" not in lb, "รายละเอียดรายผู้ขายไม่ควรแทรกในหน้า list (ต้องเป็น modal · ตารางเต็ม)"
    assert ev(page, "()=>!!document.querySelector('#page-content .list-card .table-wrap')"), "ตารางหลักหาย"
    assert ev(page, "()=>getComputedStyle(document.querySelector('#page-content .stat-row')).flexShrink") == "0", "stat-row ต้อง flex-shrink:0 (ตารางกินพื้นที่ที่เหลือเต็ม)"
    # คลิก KPI เครดิต → modal รายผู้ขาย
    after(page, "()=>showVendorCreditDetail()")
    mb = ev(page, "()=>{const m=document.querySelector('.modal-overlay');return m?m.textContent:'';}")
    assert "เครดิตคงเหลือรายผู้ขาย" in mb and "รวม" in mb, "modal เครดิตไม่โชว์รายผู้ขาย/ยอดรวม"
    btns = ev(page, "()=>[...document.querySelectorAll('.modal-overlay .btn')].map(b=>b.textContent.trim())")
    assert btns == ["ปิด"], f"modal display-only ควรมีปุ่มเดียว 'ปิด' (ไม่ซ้ำ ยกเลิก/ปิด) — ได้ {btns}"
    ev(page, "()=>closeModal()")
    rows = ev(page, "()=>vendorCreditRows().length")
    assert rows >= 1, "vendorCreditRows ว่างหลังอนุมัติ DN บนใบจ่ายครบ"
    return f"0038 จ่ายครบ → DN ฿{sp['g']:,.2f} = เครดิตคงเหลือทั้งก้อน (หักหนี้ค้าง ฿0) · เก็บใน record · KPI card + modal รายผู้ขายมีค่า ({rows} ราย) · ตารางเต็ม (stat-row flex-shrink:0)"


def c_fn21(page):
    """[FN-21 · S-14 · BR-14 · FIX-02] ภาษีซื้อ 2 สถานะ: ไม่มี vendorCn → 'รอใบลดหนี้ผู้ขาย' · มีครบ → เดือนภาษี=วันที่ได้รับ (ม.82/10)"""
    open_(page)
    ev(page, "()=>{const s=findRec('R2'); s.vendorCn=''; s.vendorCnDate='';}")   # approved · ยังไม่ได้รับใบลดหนี้ผู้ขาย
    open_view(page, "R2"); view_tab(page, "ref")
    b1 = view_text(page)
    assert "รอใบลดหนี้ผู้ขาย" in b1 and "ยังไม่ลดภาษีซื้อใน ภ.พ.30" in b1, "ไม่มี vendorCn ต้องขึ้น 'รอใบลดหนี้ผู้ขาย'"
    assert "เดือนภาษีที่ลด" not in b1, "ไม่ควรโชว์เดือนภาษีก่อนได้รับใบลดหนี้ผู้ขาย"
    # ปุ่ม 'บันทึกใบลดหนี้ผู้ขาย' → openVendorCn เปิดฟอร์ม (guard = approved/sent)
    assert "บันทึกใบลดหนี้ผู้ขาย" in b1, "ไม่มีปุ่มบันทึกใบลดหนี้ผู้ขายบนใบ approved"
    after(page, "()=>openVendorCn('R2')")
    assert ev(page, "()=>!!(document.getElementById('vc-no')&&document.getElementById('vc-date'))"), "openVendorCn ไม่เปิดฟอร์มเลขที่+วันที่"
    ev(page, "()=>closeModal()")
    # มี vendorCn + วันที่ (ได้รับ ส.ค.) → เดือนภาษี = 08/2026
    ev(page, "()=>{const s=findRec('R2'); s.vendorCn='TFS-9001'; s.vendorCnDate='2026-08-15';}")
    view_tab(page, "ref")
    b2 = view_text(page)
    assert "รอใบลดหนี้ผู้ขาย" not in b2, "มี vendorCn+วันที่แล้วยังขึ้นรอเอกสาร"
    assert "เดือนภาษีที่ลด" in b2 and "08/2026" in b2, "เดือนภาษีไม่ตรงวันที่ได้รับ (คาด 08/2026)"
    assert "TFS-9001" in b2, "ไม่อ้างเลขใบลดหนี้ผู้ขายในแท็บภาษี"
    return "R2: ไม่มี vendorCn → 'รอใบลดหนี้ผู้ขาย' (ยังไม่ลด ภ.พ.30) + ปุ่มบันทึก · ใส่ TFS-9001/15-08-2026 → เดือนภาษี 08/2026 (ม.82/10)"


# ═══════════════════════════ ส่วนลดท้ายบิล (FN-19 · user KEEP · Rule1 cap + Rule2 ม.86/10) ═══════════════════════════

def _eb_open_valid(page):
    """create DN บนใบที่มีคงเหลือพอ (API-2026-0043 · SHORT · qty 3) → ไม่ชน dnOver · คืน baseline totals"""
    open_(page); open_create(page)
    after(page, "()=>pickInv('API-2026-0043')")
    after(page, "()=>setReason('SHORT')")
    lid = ev(page, "()=>createWizard.data.lines[0].id")
    after(page, "()=>updateLine('%s','qty',3)" % lid)   # qty 3 @4100 → grand < available (ไม่ชน dnOver)
    base = ev(page, "()=>totals(createWizard.data)")
    assert base["ebAmt"] == 0 and not base["ebOver"], f"ยังไม่เปิด end-bill แต่มี ebAmt/ebOver ({base})"
    assert not ev(page, "()=>!!dnOver(createWizard.data)"), "baseline ชน dnOver (เลือกยอดใหม่)"
    return base


def c_eb_amount(page):
    """[FN-19a · ม.86/10] end-bill ฿ ลดฐานภาษี → ภาษีซื้อ (VAT) คิดใหม่ตามสัดส่วน · grand ลดตาม · JE บาลานซ์"""
    base = _eb_open_valid(page)
    amt = 1000
    after(page, "()=>{createWizard.data.endbill={enabled:true,mode:'amount',value:%d}; updateLineSummaryOnly();}" % amt)
    t = ev(page, "()=>totals(createWizard.data)")
    assert abs(t["ebAmt"] - amt) < 0.01 and not t["ebOver"], f"ebAmt clamp/over ผิด ({t})"
    assert abs(t["grand"] - (base["after"] - amt)) < 0.01, f"grand ต้อง = after-{amt} ({t['grand']} vs {base['after']-amt})"
    assert t["netVat"] < base["vat"] - 0.01, f"ภาษีซื้อต้องลดลงจากเดิม (netVat {t['netVat']} vs vat {base['vat']})"
    assert abs(t["netVat"] - t["netBefore"] * 0.07) < 0.02, f"netVat ต้อง = netBefore×7% (ม.86/10) ({t['netVat']} vs {t['netBefore']*0.07:.2f})"
    assert abs(t["grand"] - (t["netBefore"] + t["netVat"])) < 0.02, f"JE ไม่บาลานซ์: grand≠netBefore+netVat ({t['grand']} vs {t['netBefore']+t['netVat']})"
    goto_step(page, 3)
    b = create_text(page)
    assert "ม.86/10" in b and "ฐานภาษีหลังหักส่วนลด" in b, "summary ไม่โชว์ ม.86/10 / ฐานภาษีหลังหักส่วนลด"
    money = ev(page, "()=>formatMoney(totals(createWizard.data).netVat)")
    assert money in b, f"summary ไม่โชว์ภาษีซื้อที่คิดใหม่ ({money})"
    return (f"฿{amt}: before {base['before']:,.2f} · vat {base['vat']:,.2f} · ebAmt {t['ebAmt']:,.2f} · "
            f"ebVat {t['ebVat']:,.2f} · netVat {t['netVat']:,.2f} · grand {t['grand']:,.2f} · JE บาลานซ์")


def c_eb_percent(page):
    """[FN-19b · ม.86/10] end-bill % (10%) → เพดาน/สัดส่วน/บาลานซ์ เหมือน ฿ mode"""
    base = _eb_open_valid(page)
    after(page, "()=>{createWizard.data.endbill={enabled:true,mode:'percent',value:10}; updateLineSummaryOnly();}")
    t = ev(page, "()=>totals(createWizard.data)")
    exp_amt = base["after"] * 0.10
    assert abs(t["ebAmt"] - exp_amt) < 0.01 and not t["ebOver"], f"10% ebAmt ผิด ({t['ebAmt']} vs {exp_amt:.2f})"
    assert abs(t["grand"] - (base["after"] - exp_amt)) < 0.01, f"grand ต้อง = after-10% ({t['grand']})"
    assert t["netVat"] < base["vat"] - 0.01, f"ภาษีซื้อต้องลดลง ({t['netVat']} vs {base['vat']})"
    assert abs(t["netVat"] - t["netBefore"] * 0.07) < 0.02, f"netVat ต้อง = netBefore×7% ({t['netVat']} vs {t['netBefore']*0.07:.2f})"
    assert abs(t["grand"] - (t["netBefore"] + t["netVat"])) < 0.02, "JE ไม่บาลานซ์ (percent)"
    goto_step(page, 3)
    assert "10%" in create_text(page) and "ม.86/10" in create_text(page), "summary % ไม่โชว์ 10% / ม.86/10"
    return f"10%: after {base['after']:,.2f} · ebAmt {t['ebAmt']:,.2f} · netVat {t['netVat']:,.2f} · grand {t['grand']:,.2f} · JE บาลานซ์"


def c_eb_cap(page):
    """[FN-19c · Rule1] end-bill เกินเพดาน → ebOver hard-warn + grand ไม่ติดลบ + submit บล็อก (blockReason/submitGuard)"""
    base = _eb_open_valid(page)
    after(page, "()=>{createWizard.data.endbill={enabled:true,mode:'amount',value:99999999}; updateLineSummaryOnly();}")
    t = ev(page, "()=>totals(createWizard.data)")
    assert t["ebOver"] is True, "end-bill เกินเพดานแต่ ebOver=false"
    assert t["grand"] >= 0 and abs(t["grand"]) < 0.01, f"grand ต้อง = 0 (ไม่ติดลบ) เมื่อส่วนลดเกิน ({t['grand']})"
    assert abs(t["ebAmt"] - t["ebCap"]) < 0.01 and abs(t["ebCap"] - base["after"]) < 0.01, f"ebAmt ต้อง clamp ที่ ebCap = after ({t})"
    assert ev(page, "()=>DOC.blockReason(createWizard.data)").startswith("ส่วนลดท้ายบิลเกิน"), "blockReason ไม่บล็อกส่วนลดเกิน"
    goto_step(page, 3)
    b = create_text(page)
    assert "ส่วนลดท้ายบิลเกินยอดที่ลดได้" in b and "สูงสุด" in b, "ไม่มี hard-warn ส่วนลดเกิน + เพดาน"
    # submitGuard บนใบ draft จริง (R6) + openSubmitModal ไม่เปิด
    open_(page)
    after(page, "()=>{findRec('R6').endbill={enabled:true,mode:'amount',value:99999999};}")
    g = ev(page, "()=>DOC.submitGuard(findRec('R6'))")
    assert g.startswith("ส่วนลดท้ายบิลเกิน"), f"submitGuard ไม่บล็อกส่วนลดเกินบนใบ draft ({g})"
    after(page, "()=>openSubmitModal('R6')")
    assert not has_modal(page), "openSubmitModal เปิด modal ทั้งที่ส่วนลดเกิน"
    assert ev(page, "()=>totals(findRec('R6')).grand") >= 0, "R6 grand ติดลบ"
    return f"amount 99,999,999 → clamp ที่เพดาน ฿{base['after']:,.2f} · grand=0 (ไม่ติดลบ) · ebOver · blockReason+submitGuard บล็อก · openSubmitModal ไม่เปิด"


def c_eb_ref_je(page):
    """[FN-19 · FN-18] ref tab (ใบ approved + end-bill) JE ใช้ netBefore/netVat · บาลานซ์ · โชว์ภาษีซื้อที่คิดใหม่"""
    open_(page)
    ref = ev(page, "()=>{const s=findRec('R2'); s.endbill={enabled:true,mode:'percent',value:10}; const t=totals(s); "
                  "return {netVat:t.netVat, vat:t.vat, netBefore:t.netBefore, grand:t.grand};}")
    assert ref["netVat"] < ref["vat"] - 0.01, "R2+end-bill: netVat ต้อง < vat (ภาษีซื้อถูกลด)"
    assert abs(ref["grand"] - (ref["netBefore"] + ref["netVat"])) < 0.02, "ref JE ไม่บาลานซ์ (grand≠netBefore+netVat)"
    money = ev(page, "()=>formatMoney(totals(findRec('R2')).netVat)")
    open_view(page, "R2"); view_tab(page, "ref")
    rb = view_text(page)
    assert "1170 ภาษีซื้อ" in rb and "2110 เจ้าหนี้การค้า" in rb, "ref tab ไม่มี JE 2110/1170"
    assert money in rb, f"ref tab (JE/ภ.พ.30) ไม่โชว์ภาษีซื้อที่คิดใหม่ ({money})"
    return f"R2+10%: netVat {ref['netVat']:,.2f} < vat {ref['vat']:,.2f} · JE DR grand={ref['grand']:,.2f}=CR({ref['netBefore']:,.2f}+{ref['netVat']:,.2f}) บาลานซ์"


def c_attach(page):
    """[FN-ATTACH] step 4 ใช้ <input type=file> จริง (ไม่ mock) — เลือกไฟล์จริง → name+size จริง · remove ได้ · ไม่มี mockUpload"""
    open_(page); open_create(page)
    goto_step(page, 4)
    inp = ev(page, "()=>{const e=document.getElementById('att-file-input');return e?{type:e.type,multiple:e.multiple}:null;}")
    assert inp and inp["type"] == "file" and inp["multiple"], f"ไม่มี <input type=file multiple> จริงใน step 4 ({inp})"
    zone_oc = ev(page, "()=>{const z=document.querySelector('#create-drawer-content .upload-zone');return z?z.getAttribute('onclick'):'';}")
    assert "triggerAttachPick" in (zone_oc or ""), f"upload-zone ไม่ยิง file picker จริง ({zone_oc})"
    assert ev(page, "()=>typeof mockUpload") == "undefined", "ยังมี mockUpload (ควรถูกถอด)"
    assert ev(page, "()=>createWizard.data.attachments.length") == 0, "ก่อนเลือกไฟล์ attachments ไม่ว่าง (มี canned file ถูกยัด)"
    d = tempfile.mkdtemp()
    f1 = Path(d) / "rtv-photo-REAL.png"; f1.write_bytes(b"x" * 700000)   # ~684 KB
    page.set_input_files("#att-file-input", str(f1))
    page.wait_for_function("()=>createWizard.data.attachments.length===1", timeout=3000)
    atts = ev(page, "()=>createWizard.data.attachments.map(a=>({name:a.name,size:a.size}))")
    assert atts[0]["name"] == "rtv-photo-REAL.png", f"ชื่อไฟล์จริงไม่ถูกอ่าน ({atts})"
    assert re.match(r"^\d+(\.\d+)? (B|KB|MB)$", atts[0]["size"]) and atts[0]["size"].endswith("KB"), f"ขนาดไฟล์ผิดรูปแบบ ({atts[0]})"
    assert "rtv-photo-REAL.png" in create_text(page), "step 4 ไม่เรนเดอร์ชื่อไฟล์จริง"
    assert ev(page, "()=>document.getElementById('att-file-input').value") == "", "ไม่ล้างค่า input หลังเลือก (re-pick ไฟล์เดิมจะไม่ยิง)"
    after(page, "()=>removeAttachment(0)")
    assert ev(page, "()=>createWizard.data.attachments.length") == 0, "removeAttachment ลบไม่ได้"
    return f"step 4 = <input type=file multiple> จริง · เลือก 1 ไฟล์ → {atts[0]['name']} ({atts[0]['size']}) · เรนเดอร์ · input reset · remove ได้ · ไม่มี mockUpload"


# ═══════════════════════════ หมวด 5 · ทั่วไป ═══════════════════════════

def c_fn90(page):
    """[FN-90] ค้นหา/กรองสถานะ/เหตุผล/ผู้ขาย + empty state"""
    open_(page)
    total = ev(page, "()=>RECS.length")
    after(page, "()=>setFilter('reason','RTV')")
    ret = ev(page, "()=>getFilteredRecords().map(r=>r.reason)")
    assert ret and all(x == "RTV" for x in ret), f"กรองเหตุผล RTV ไม่ทำงาน ({ret})"
    after(page, "()=>setFilter('reason','all')")
    after(page, "()=>setFilter('status','sent')")
    assert all(r == "sent" for r in ev(page, "()=>getFilteredRecords().map(r=>r.status)")), "กรองสถานะ sent ไม่ทำงาน"
    after(page, "()=>setFilter('status','all')")
    after(page, "()=>setFilter('vend','V-2002')")
    assert all(r == "V-2002" for r in ev(page, "()=>getFilteredRecords().map(r=>r.partner)")), "กรองผู้ขาย V-2002 ไม่ทำงาน"
    after(page, "()=>setFilter('vend','all')")
    after(page, "()=>{state.filters.search='API-2026-0046';renderTableOnly();}")
    invs = ev(page, "()=>getFilteredRecords().map(r=>r.inv)")
    assert invs and all(x == "API-2026-0046" for x in invs), f"ค้นหา inv ไม่ทำงาน ({invs})"
    after(page, "()=>{state.filters.search='ไม่มีทางเจอ-zzz-999';renderTableOnly();}")
    tb = ev(page, "()=>document.getElementById('table-body').textContent")
    assert "ไม่พบรายการที่ตรงกับเงื่อนไข" in tb, "ค้นหาไม่เจอแต่ไม่ขึ้น empty state"
    assert ev(page, "()=>getFilteredRecords().length") == 0, "empty state แต่ยังมีผลลัพธ์"
    return f"กรอง RTV/sent/ผู้ขาย · ค้นหา inv · empty state 'ไม่พบรายการ' (จาก {total} ใบ)"


def c_fn91(page):
    """[FN-91 · GR-4] ประวัติ append-only ทุกการกระทำ (ไม่ลบ ไม่ทับ)"""
    open_(page)
    n_rec0 = ev(page, "()=>RECS.length")
    a0 = ev(page, "()=>findRec('R6').audit.length")
    first0 = ev(page, "()=>findRec('R6').audit[findRec('R6').audit.length-1].act")   # entry แรกสุด (ล่างสุด)
    after(page, "()=>openCancelDN('R6')")
    after(page, "()=>{document.getElementById('md-reason').value='ทดสอบ append-only';document.getElementById('md-ok').click();}")
    a1 = ev(page, "()=>findRec('R6').audit.length")
    first1 = ev(page, "()=>findRec('R6').audit[findRec('R6').audit.length-1].act")
    assert a1 == a0 + 1, f"audit ไม่ append (คาด {a0}+1 ได้ {a1})"
    assert first1 == first0, "entry เดิมถูกทับ/ลบ (ไม่ append-only)"
    assert ev(page, "()=>findRec('R6').audit[0].act").startswith("ยกเลิก"), "action ล่าสุดไม่ได้อยู่บนสุด"
    assert ev(page, "()=>RECS.length") == n_rec0, "RECS ลดลง (มี hard delete)"
    assert ev(page, "()=>!!findRec('R6')") and ev(page, "()=>findRec('R6').status") == "cancelled", "ใบยกเลิกหายไป (ควรคงไว้)"
    open_view(page, "R6"); view_tab(page, "history")
    assert "ประวัติ" in view_text(page) and "append-only" in view_text(page), "history tab ไม่เรนเดอร์"
    return f"audit {a0}→{a1} (append) · entry เดิมคงอยู่ · RECS คงที่ (ไม่ลบ) · history tab OK"


def c_fn92(page):
    """[FN-92 · OB-6] PDF: อ้างเลข/วันที่ใบกำกับเดิม · มูลค่าเดิม/ถูกต้อง/ผลต่าง · เหตุผล · ค.ศ."""
    open_(page)
    open_view(page, "R2"); view_tab(page, "pdf")
    b = view_text(page)
    iv = ev(page, "()=>INV_BY[findRec('R2').inv]")
    iv_date = ev(page, "()=>formatThaiDate(INV_BY[findRec('R2').inv].vdate)")
    assert iv["vinv"] in b, "PDF ไม่อ้างเลขใบกำกับผู้ขายเดิม"
    assert iv["no"] in b, "PDF ไม่อ้างเลขใบตั้งหนี้เดิม"
    assert iv_date in b, "PDF ไม่อ้างวันที่ใบกำกับเดิม"
    assert "มูลค่าสินค้าตามใบกำกับเดิม" in b and "มูลค่าที่ถูกต้อง" in b and "ผลต่าง" in b, "PDF ไม่แสดงมูลค่าเดิม/ถูกต้อง/ผลต่าง"
    assert "เหตุผลการลดหนี้" in b, "PDF ไม่แสดงเหตุผล"
    assert "2026" in b and "2569" not in b, "PDF ใช้ปี พ.ศ. หรือไม่มีปี ค.ศ."
    return f"PDF R2: อ้าง {iv['no']}/{iv['vinv']} · วันที่ใบกำกับเดิม {iv_date} · มูลค่าเดิม/ถูกต้อง/ผลต่าง · เหตุผล · ค.ศ. 2026"


# ═══════════════════════════ NEGATIVES (render-assert · หมวด 'สิ่งที่ไม่รองรับ') ═══════════════════════════

def c_neg_refund(page):
    """[NEG · S-15 refund] ไม่มี affordance เรียกเงินคืน/คืนเงิน/refund ที่ไหนเลย (OQ-DN-03 · render-assert)"""
    open_(page)
    assert_text_absent(page, ["เรียกเงินคืน", "คืนเงิน", "refund", "Refund", "REFUND"], scope="#page-content")
    open_view(page, "R2")     # ใบ approved (มี action มากสุด)
    assert_text_absent(page, ["เรียกเงินคืน", "คืนเงิน", "refund", "Refund"], scope="#view-drawer-content")
    view_tab(page, "ref")
    assert_text_absent(page, ["เรียกเงินคืน", "คืนเงิน", "refund"], scope="#view-drawer-content")
    return "ไม่มีข้อความ/ปุ่ม 'เรียกเงินคืน'/'คืนเงิน'/'refund' ใน list + view (detail/ref) — S-15 ปิด (OQ-DN-03)"


def c_neg_cancel_approved(page):
    """[NEG · S-16 · OQ-DN-04] ไม่มีปุ่มยกเลิกบนใบอนุมัติแล้ว (approved/sent) — ยกเลิกได้เฉพาะ draft/pending"""
    open_(page)
    for rid, st in [("R2", "approved"), ("R1", "sent")]:
        acts = ev(page, "()=>DOC.viewActions(findRec('%s'), '%s')" % (rid, st))
        assert "openCancelDN" not in acts, f"{rid} ({st}) มีปุ่มยกเลิกทั้งที่อนุมัติแล้ว (S-16 หลุด)"
        assert ev(page, "()=>DOC.rowCancel(findRec('%s'), '%s')" % (rid, st)) is None, f"row menu {rid} ยังมี 'ยกเลิก'"
    assert ev(page, "()=>DOC.rowCancel(findRec('R6'), 'draft')") is not None, "draft ควรยกเลิกได้"
    assert ev(page, "()=>DOC.rowCancel(findRec('R4'), 'pending_approval')") is not None, "pending ควรยกเลิกได้"
    open_view(page, "R2")
    html = ev(page, "()=>document.getElementById('view-drawer-content').innerHTML")
    assert "openCancelDN('R2')" not in html, "view ใบ approved เรนเดอร์ปุ่มยกเลิก"
    return "approved (R2) + sent (R1): ไม่มีปุ่ม/เมนูยกเลิก · draft/pending ยกเลิกได้ → guard แยกสถานะจริง"


def c_neg_no_rtv_crud(page):
    """[NEG · แผน] RTV เป็น lookup (mock) เท่านั้น — ไม่มีหน้าจอ/ปุ่มสร้างใบคืนสินค้า"""
    open_(page); open_create(page)
    after(page, "()=>pickInv('API-2026-0041')")
    after(page, "()=>setReason('RTV')")
    goto_step(page, 2)
    has_select = ev(page, "()=>!!document.querySelector('#f-rtv select')")
    assert has_select, "ช่องใบคืนสินค้าไม่ใช่ dropdown lookup"
    assert_text_absent(page, ["สร้างใบคืนสินค้า", "เพิ่มใบคืนสินค้า", "แก้ไขใบคืนสินค้า", "จัดการใบคืนสินค้า", "คืนสินค้าใหม่"],
                       scope="#create-drawer-content")
    no_fn = ev(page, "()=>['openRTVDrawer','createRTV','openReturn','editRTV','openReturnDrawer']"
                    ".every(f=>typeof window[f]==='undefined')")
    assert no_fn, "มีฟังก์ชันเปิด/สร้างหน้าจอ RTV (ควรเป็น lookup เท่านั้น)"
    return "ใบคืนสินค้า = <select> lookup · ไม่มีปุ่มสร้าง/แก้/จัดการ RTV · ไม่มี controller เปิดหน้าจอ RTV"


# ═══════════════════════════ C3.8 · DSP-08 modal-z (wired assert) ═══════════════════════════

def c_modal_z(page):
    """[DSP-08 · C3.8] การ์ด modal ต้องเป็น hit-test บนสุด ณ กึ่งกลาง (ไม่จมใต้ .backdrop) — submit + reason modal"""
    open_(page)
    after(page, "()=>openSubmitModal('R6')")          # R6 draft ยอดต่ำ
    assert ev(page, "()=>!!document.querySelector('.modal-overlay #submit-modal')"), "openSubmitModal ไม่เรนเดอร์การ์ด"
    r1 = assert_modal_card_topmost(page, note="submit modal")
    after(page, "()=>closeModal()")
    after(page, "()=>openRejectModal('R4')")          # reason modal (.card ใต้ .modal-overlay)
    assert ev(page, "()=>!!document.querySelector('.modal-overlay .card')"), "openRejectModal ไม่เรนเดอร์การ์ด"
    r2 = assert_modal_card_topmost(page, note="reason modal")
    return (f"submit modal: hit กึ่งกลาง=การ์ด (card z:{r1['cardZ']} > backdrop z:{r1['backdropZ']}) · "
            f"reason modal: การ์ด z:{r2['cardZ']} บนสุด (ไม่จมใต้ .backdrop)")


# ═══════════════════════════ C3.8 · STATUS-GUARD bypass (ปุ่มซ่อน แต่ controller เรียกได้) ═══════════════════════════

def c_bypass_c1_cancel_sent(page):
    """[C1 · BLOCK · FN-15] ยกเลิกใบที่ 'ส่งผู้ขายแล้ว' (sent) เรียก openCancelDN ตรง → ต้อง block
    ในฟังก์ชัน (status/code/chain ไม่เปลี่ยน) + warning toast 'ยกเลิกได้เฉพาะ...(OQ-DN-04)'"""
    open_(page)
    r = assert_status_guard(
        page, "openCancelDN('R1')", "R1", "sent",
        "({s:findRec('R1').status,c:findRec('R1').code,n:(findRec('R1').approval_chain||[]).length})",
        note="C1 cancel-on-sent")
    assert ev(page, "()=>findRec('R1').status") == "sent", "R1 (sent) ถูกยกเลิกทั้งที่ออกเลขแล้ว (C1 หลุด)"
    assert not has_modal(page), "guard block แล้วแต่ยังเปิด modal ยกเลิก"
    return f"openCancelDN ใบ sent → block ในฟังก์ชัน · status คง sent · toast='{r['toast'][:48]}'"


def c_bypass_c2_send_draft(page):
    """[C2 · BLOCK · FN-16] ส่งใบ 'ฉบับร่าง' (draft ไม่มีเลข) เรียก openSendDN ตรง → ต้อง block
    (ไม่กลายเป็น sent · ไม่มี sentAt) + warning toast 'ต้องอนุมัติครบก่อนส่งให้ผู้ขาย'"""
    open_(page)
    r = assert_status_guard(
        page, "openSendDN('R6')", "R6", "draft",
        "({s:findRec('R6').status,c:findRec('R6').code,sent:!!findRec('R6').sentAt})",
        note="C2 send-on-draft")
    assert ev(page, "()=>findRec('R6').status") == "draft", "R6 (draft) ถูกส่งให้ผู้ขายได้ (C2 หลุด)"
    assert not ev(page, "()=>!!findRec('R6').sentAt"), "draft ส่งไม่ได้แต่มี sentAt"
    assert not has_modal(page), "guard block แล้วแต่ยังเปิด modal ส่ง"
    return f"openSendDN ใบ draft → block · status คง draft · ไม่มี sentAt · toast='{r['toast'][:40]}'"


def c_bypass_c4_submit_approved(page):
    """[C4 · BLOCK · FN-11] ส่งอนุมัติซ้ำใบ 'approved' (ออกเลขแล้ว) เรียก confirmSubmit ตรง → ต้อง block
    (chain/code เดิมไม่ถูกเขียนทับ) + warning toast · openSubmitModal (opener) ก็ block"""
    open_(page)
    # (ก) openSubmitModal (opener) guard บนใบ approved
    after(page, "()=>{findRec('R2').status='approved'; openSubmitModal('R2');}")
    assert not has_modal(page), "openSubmitModal เปิด modal ให้ใบ approved (opener guard หลุด)"
    assert "เฉพาะฉบับร่าง" in last_toast(page), f"openSubmitModal ไม่เตือน block ({last_toast(page)})"
    # (ข) confirmSubmit (commit) guard — เรียกตรงผ่าน modalState (slots ว่างเพื่อให้ถึง status guard)
    r = assert_status_guard(
        page, "modalState.slots=[]; modalState.id='R2'; confirmSubmit();", "R2", "approved",
        "({s:findRec('R2').status,c:findRec('R2').code,n:(findRec('R2').approval_chain||[]).length,"
        "sb:findRec('R2').submittedBy})",
        note="C4 submit-on-approved")
    assert ev(page, "()=>findRec('R2').status") == "approved", "R2 (approved) ถูกส่งอนุมัติซ้ำ (C4 หลุด)"
    return f"submit ใบ approved → openSubmitModal + confirmSubmit block · chain/code เดิมคงอยู่ · toast='{r['toast'][:36]}'"


# ═══════════════════════════ RUN ═══════════════════════════

CASES = [
    ("E01", c_fn01, ["FN-01"]),
    ("E02", c_fn02, ["FN-02"]),
    ("E03", c_fn03, ["FN-03"]),
    ("E04", c_fn04, ["FN-04"]),
    ("E05", c_fn05, ["FN-05"]),
    ("E06", c_fn06, ["FN-06"]),
    ("E07", c_fn07, ["FN-07"]),
    ("E08", c_fn08, ["FN-08"]),
    ("E08b-CAP", c_cap_display, ["FN-05", "FN-08"]),
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
    ("E20-VENDOR-CREDIT", c_fn20, ["FN-20"]),
    ("E21-VENDORCN-VAT", c_fn21, ["FN-21"]),
    ("E19a-EB-AMT", c_eb_amount, ["FN-19"]),
    ("E19b-EB-PCT", c_eb_percent, ["FN-19"]),
    ("E19c-EB-CAP", c_eb_cap, ["FN-19"]),
    ("E19d-EB-REF-JE", c_eb_ref_je, ["FN-19", "FN-18"]),
    ("E-ATTACH", c_attach, []),
    ("E90", c_fn90, ["FN-90"]),
    ("E91", c_fn91, ["FN-91"]),
    ("E92", c_fn92, ["FN-92"]),
    ("N-REFUND", c_neg_refund, []),
    ("N-CANCEL-APPROVED", c_neg_cancel_approved, []),
    ("N-RTV-CRUD", c_neg_no_rtv_crud, []),
    ("Z-MODAL", c_modal_z, []),
    ("C1-CANCEL-SENT", c_bypass_c1_cancel_sent, ["FN-15"]),
    ("C2-SEND-DRAFT", c_bypass_c2_send_draft, ["FN-16"]),
    ("C4-SUBMIT-APPROVED", c_bypass_c4_submit_approved, ["FN-11"]),
]

ALL_FN = ["FN-01", "FN-02", "FN-03", "FN-04", "FN-05", "FN-06", "FN-07", "FN-08", "FN-09",
          "FN-10", "FN-11", "FN-12", "FN-13", "FN-14", "FN-15", "FN-16", "FN-17", "FN-18",
          "FN-19", "FN-20", "FN-21", "FN-90", "FN-91", "FN-92"]


def diag_cap_display():
    """DIAGNOSTIC (ไม่ gate): เทียบ 'เลขที่โชว์ใน line-meta' (room.qtyLeft) กับ 'เพดานที่บังคับจริง'
    (l.max · RTV-capped) สำหรับเหตุผลคืนสินค้าที่ RTV ตัดให้แคบกว่า room — เป็น class เดียวกับ CAP-DISPLAY
    ที่ F-ACC-CN เคยแก้ (lineMeta โชว์ l.max). รายงานให้ orchestrator ตัดสิน (ไม่แตะ HTML)."""
    out = {}
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width": 1360, "height": 900})
        open_(pg, BASE); open_create(pg)
        after(pg, "()=>pickInv('API-2026-0041')")
        after(pg, "()=>setReason('RTV')")
        after(pg, "()=>pickRTV('RTV-2026-0010')")     # RTV คืน 2 · room.qtyLeft=18
        goto_step(pg, 3)
        info = ev(pg, """()=>{const m=document.querySelector('#create-drawer-content .line-meta');
            const l=createWizard.data.lines[0];
            const t=m?m.textContent:''; const mm=t.match(/ลดจำนวนได้อีก\\s*([\\d,]+)/);
            return {shown: mm?mm[1]:null, enforcedMax:l.max, metaText:t.trim().slice(0,160)};}""")
        out = info
        br.close()
    return out


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1360, "height": 900})
        suite.watch(page)
        covered = {}
        for tid, fn, fns in CASES:
            suite.check(tid, fn.__doc__.strip().splitlines()[0], lambda fn=fn: fn(page))
            status = suite.results[-1][2]
            for code in fns:
                covered[code] = covered.get(code, False) or (status == "PASS")
        browser.close()

    ok = suite.report(exit_on_fail=False)
    total = len(suite.results)

    print()
    have_case = sorted(covered.keys())
    passed_fn = [c for c in ALL_FN if covered.get(c)]
    missing = [c for c in ALL_FN if c not in have_case]
    failed_fn = [c for c in ALL_FN if c in have_case and not covered.get(c)]
    print("── FN coverage (%d) ──" % len(ALL_FN))
    for c in ALL_FN:
        mark = "PASS" if covered.get(c) else ("FAIL" if c in have_case else "MISSING")
        if mark != "PASS":
            print(f"  {c}: {mark}")
    if missing:
        print("  ! FN ที่ไม่มีเคส:", ", ".join(missing))
    if failed_fn:
        print("  ! FN ที่มีเคสแต่ยังตก:", ", ".join(failed_fn))
    if not missing and not failed_fn:
        print("  ครบทุก FN (%d/%d) — ทุกตัวมีเคสและผ่าน" % (len(ALL_FN), len(ALL_FN)))

    print()
    print("── DIAGNOSTIC (ไม่ gate) · CAP-DISPLAY (RTV เทียบ l.max vs meta) ──")
    try:
        d = diag_cap_display()
        shown = d.get("shown")
        enforced = d.get("enforcedMax")
        mism = (shown is not None and enforced is not None and
                float(str(shown).replace(",", "")) != float(enforced))
        print(f"  meta โชว์ 'ลดจำนวนได้อีก {shown}' · เพดานบังคับจริง l.max={enforced}"
              f" → {'MISMATCH (เลขที่โชว์ ≠ เพดานจริง · class เดียวกับ CN CAP-DISPLAY)' if mism else 'ตรงกัน'}")
        print(f"  meta: {d.get('metaText')}")
    except Exception as e:
        print(f"  diagnostic ERROR: {type(e).__name__}: {e}")

    print()
    print(f"FN ครอบ {len(passed_fn)}/{len(ALL_FN)} · เคสรวม {total} · ผ่าน {ok}/{total}")
    sys.exit(0 if ok == total and len(passed_fn) == len(ALL_FN) and not suite.console_errors else 1)


if __name__ == "__main__":
    main()
