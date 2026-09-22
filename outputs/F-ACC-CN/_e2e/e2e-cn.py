#!/usr/bin/env python3
"""E2E · F-ACC-CN · ใบลดหนี้ลูกค้า (Credit Note) — WF-01 Step 5 (ตัวหนัก)

รันไทม์ตัวเดียวที่ต้องพิสูจน์ COMPLETENESS: ทุก FN ใน FUNCTION_CHECKLIST (22 FN =
FN-01..18 + FN-19 (ส่วนลดท้ายบิล · BA 2026-09-22) + FN-90/91/92) มีเคส ≥1 (ติดรหัสในชื่อเคส) + negatives = "เรนเดอร์จริงแล้ว
assert ว่าของที่ไม่รองรับเข้าไม่ถึง" (ฟีเจอร์นี้ไม่มี FN-40 numbered · negatives อยู่ในหมวด
"สิ่งที่ไม่รองรับ").

ยึด helper ของ uikit เท่านั้น (ready/settle/after + assert_* กลาง) — ไม่มี wait_for_timeout,
ไม่เขียนตัวตรวจ UI generic ใหม่. ขับหน้าจอผ่าน controller function จริงของไฟล์ (pickInv /
setReason / pickSR / updateLine / wizardNext / openSubmitModal / comboPick / confirmSubmit /
openApproveModal / confirmApprove / openRejectModal / openCancelCN / openSendCN / demoPay /
renderRefTab / renderPdfTab) + real DOM แล้ว assert ทั้ง data model และสิ่งที่เรนเดอร์.
reload หน้าใหม่ต่อเคส → mock RECS/DOC reset = เคสอิสระต่อกัน.

C3.8: เพิ่ม assert_modal_card_topmost เข้า uikit (DSP-08 modal จมใต้ .backdrop) + prove-by-revert.

รัน: PYTHONIOENCODING=utf-8 .claude/venv/Scripts/python.exe \
       outputs/F-ACC-CN/_e2e/e2e-cn.py outputs/F-ACC-CN/F-ACC-CN_credit-note.html
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
    assert_text_absent, assert_no_garbage_text, assert_modal_card_topmost,
    assert_line_cap_display_matches_enforced, assert_status_guard,
)

HTML = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parents[1] / "F-ACC-CN_credit-note.html").resolve()
BASE = HTML.as_uri()

suite = Suite("F-ACC-CN · ใบลดหนี้ลูกค้า")

# DSP-08 fix line ในไฟล์ (ตัวเต็ม rule) — ใช้ทั้งการยืนยันว่ามีอยู่ และการ revert ในสำเนา scratch
DSP08_FIX_RULE = ".modal-overlay > *:not(.backdrop) { position: relative; z-index: var(--z-modal); }"

# CAP-DISPLAY fix (F-ACC-CN 2026-09-21) — lineMeta โชว์ l.max (เพดานที่บังคับจริง · SR-capped)
# ไม่ใช่ room.qtyLeft. ใช้พิสูจน์ prove-by-revert: สำเนา scratch ที่ย้อนกลับไปโชว์ room.qtyLeft
# → assert_line_cap_display_matches_enforced ต้อง FAIL (เลขที่โชว์ ≠ จุดบล็อก)
CAP_FIX_SNIPPET = "' · ลดจำนวนได้อีก ' + fmi(capLeft) + (capFromSR ? ' (ตามใบรับคืน)' : '')"
CAP_BROKEN_SNIPPET = "' · ลดจำนวนได้อีก ' + fmi(room.qtyLeft)"

# STATUS-GUARD fix (FIX-02 openSendCN) — guard 'ในฟังก์ชัน' กัน bypass ปุ่มถูกซ่อนแต่เรียก controller ตรง.
# prove-by-revert: สำเนา scratch ที่ถอด guard นี้ → assert_status_guard ต้อง FAIL (send ใบ draft ทะลุ =
# เปิด modal/ไม่มี warning toast) · ไฟล์จริง (มี guard) → PASS.
STATUS_GUARD_FIX = ("if (s.status !== 'approved' && s.status !== 'sent') { "
                    "return showToast('ต้องอนุมัติครบก่อนส่ง', 'warning'); }  /* [FIX-02] */ ")


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


# ═══════════════════════════ หมวด 1 · อ้างใบแจ้งหนี้ ═══════════════════════════

def c_fn01(page):
    """[FN-01 · S-01 · BR-01] เลือกใบแจ้งหนี้คงค้าง เห็นยอดสุทธิ/ลดแล้ว/คงค้าง"""
    open_(page); open_create(page)
    # picker แสดงคอลัมน์ ยอดสุทธิ · ลดหนี้แล้ว · คงค้าง (INV_COLS)
    body = create_text(page)
    assert "ยอดสุทธิ" in body and "ลดหนี้แล้ว" in body and "คงค้าง" in body, "step1 picker ไม่มี 3 คอลัมน์ยอด"
    # 0140 มี R1 (sent) ลดแล้ว → คงค้าง = สุทธิ − ลดแล้ว
    grand = ev(page, "()=>invGrand(INV_BY['INV-2026-0140'])")
    applied = ev(page, "()=>cnApplied('INV-2026-0140',null)")
    out = ev(page, "()=>invOutstanding('INV-2026-0140',null)")
    assert applied > 0, "0140 ควรมียอดลดหนี้แล้ว (R1 sent) แต่ cnApplied=0"
    assert abs(out - (grand - applied)) < 0.01, f"คงค้าง != สุทธิ−ลดแล้ว ({out} vs {grand-applied})"
    after(page, "()=>pickInv('INV-2026-0140')")
    assert ev(page, "()=>createWizard.data.inv") == "INV-2026-0140", "เลือกใบแล้ว inv ไม่ติด"
    assert ev(page, "()=>createWizard.data.partner") == "C-1001", "เลือกใบแล้วลูกค้าไม่ถูกดึง"
    return f"เลือก 0140 → สุทธิ ฿{grand:,.0f} · ลดแล้ว ฿{applied:,.0f} · คงค้าง ฿{out:,.0f}"


def c_fn02(page):
    """[FN-02 · S-12 · OQ-CN-01] tile 'ลดหนี้ไม่อ้างใบ' present แต่ปิดไว้ (เริ่ม path นั้นไม่ได้)"""
    open_(page); open_create(page)
    body = create_text(page)
    assert "ลดหนี้ไม่อ้างใบ" in body and "ปิดไว้" in body, "step1 ไม่มี tile 'ลดหนี้ไม่อ้างใบ' + ป้าย 'ปิดไว้'"
    # tile นั้นต้องเป็น cursor:not-allowed และ onclick = showToast (ไม่ใช่ setSource เข้า path ลอย)
    r = ev(page, """()=>{const bs=[...document.querySelectorAll('#create-drawer-content button')]
        .filter(b=>/ลดหนี้ไม่อ้างใบ/.test(b.textContent));
        if(!bs.length) return null; const b=bs[0];
        return {cur:getComputedStyle(b).cursor, oc:(b.getAttribute('onclick')||'')};}""")
    assert r, "ไม่พบปุ่ม tile ลดหนี้ไม่อ้างใบ"
    assert r["cur"] == "not-allowed", f"tile ปิดไว้แต่ cursor ไม่ใช่ not-allowed ({r['cur']})"
    assert "showToast" in r["oc"] and "setSource" not in r["oc"], f"tile ปิดไว้ยังผูก path สร้างจริง: {r['oc']}"
    # กด tile แล้ว state ไม่เปลี่ยนไป source อื่น (ยังต้องอ้างใบเสมอ)
    st0 = ev(page, "()=>createWizard.data.source_type")
    after(page, """()=>{const b=[...document.querySelectorAll('#create-drawer-content button')]
        .filter(x=>/ลดหนี้ไม่อ้างใบ/.test(x.textContent))[0]; if(b) b.click();}""")
    assert ev(page, "()=>createWizard.data.source_type") == st0, "กด tile ปิดไว้แล้ว source_type เปลี่ยน (path ลอยเปิด)"
    assert "ปิดไว้" in last_toast(page) or "OQ-CN-01" in last_toast(page), f"กด tile ปิดไว้ไม่เตือน ({last_toast(page)})"
    return "tile 'ลดหนี้ไม่อ้างใบ' present · cursor not-allowed · onclick=showToast · กดแล้ว source ไม่เปลี่ยน"


def c_fn03(page):
    """[FN-03 · S-01] เลือกใบ → ลูกค้า/ที่อยู่/เลขภาษี/บรรทัดของใบเดิมถูกดึงมา"""
    open_(page); open_create(page)
    after(page, "()=>pickInv('INV-2026-0140')")
    d = ev(page, "()=>({partner:createWizard.data.partner, rep:createWizard.data.rep, billTo:createWizard.data.billTo, "
                 "nlines:createWizard.data.lines.length, item:createWizard.data.lines[0].item_code, "
                 "src:createWizard.data.lines[0].src_line})")
    p = ev(page, "()=>PARTNER_BY['C-1001']")
    assert d["partner"] == "C-1001", "ลูกค้าไม่ถูกดึง"
    assert d["billTo"] == p["addr"], "ที่อยู่ (billTo) ไม่ถูกดึงจากลูกค้าของใบเดิม"
    assert d["nlines"] == 1 and d["item"] == "P-1002", f"บรรทัดใบเดิมไม่ถูกดึง ({d})"
    assert d["src"] == "INV-2026-0140|0", "บรรทัดไม่ผูก src_line กับใบเดิม"
    # step 2 แสดง เลขภาษี + สาขา ของลูกค้า (อยู่ใน value attribute ของ input disabled → อ่าน innerHTML)
    goto_step(page, 2)
    b = ev(page, "()=>document.getElementById('create-drawer-content').innerHTML")
    assert p["taxId"] in b and p["branch"] in b, "step2 ไม่แสดงเลขภาษี/สาขาของใบเดิม"
    return f"เลือก 0140 → C-1001 · addr · taxId {p['taxId']} · 1 บรรทัด (P-1002) จากใบเดิม"


def c_fn04(page):
    """[FN-04 · S-13] ใบชำระครบ (0136) / ถูกยกเลิก void (0143) ไม่โผล่ให้เลือก (render-assert)"""
    open_(page); open_create(page)
    keys = ev(page, "()=>invList().map(x=>x.key)")
    assert "INV-2026-0136" not in keys, "ใบชำระครบ 0136 ยังโผล่ใน picker"
    assert "INV-2026-0143" not in keys, "ใบ void 0143 ยังโผล่ใน picker"
    # ยืนยันเหตุผล: 0136 outstanding=0 (paid ครบ) · 0143 void
    assert ev(page, "()=>invOutstanding('INV-2026-0136',null)") < 0.005, "0136 ควร outstanding=0 (ชำระครบ)"
    assert ev(page, "()=>INV_BY['INV-2026-0143'].status") == "void", "0143 ควร status=void"
    # เรนเดอร์จริง: ตาราง step1 ต้องไม่มี 0136/0143
    body = create_text(page)
    assert "INV-2026-0136" not in body and "INV-2026-0143" not in body, "ตาราง picker ยังเรนเดอร์ใบชำระครบ/void"
    # ของที่ควรโผล่ยังอยู่
    assert "INV-2026-0140" in keys and "INV-2026-0141" in keys, "ใบคงค้างจริงหายจาก picker"
    return "0136 (ชำระครบ) + 0143 (void) ไม่โผล่ใน picker · ใบคงค้าง 0140/0141 ยังอยู่"


# ═══════════════════════════ หมวด 2 · เหตุผลและยอดลด ═══════════════════════════

def c_fn05(page):
    """[FN-05 · S-01 · BR-06] RET ต้องเลือกใบรับคืน · จำนวนมาจากใบรับคืน (ของใบเดียวกัน)"""
    open_(page); open_create(page)
    after(page, "()=>pickInv('INV-2026-0140')")   # reason default RET
    after(page, "()=>setReason('RET')")
    # SR dropdown ต้องมีเฉพาะใบรับคืนของ 0140 (SR-0011, SR-0016) — ไม่ใช่ของใบอื่น (SR-0014 = 0141)
    goto_step(page, 2)
    b = create_text(page)
    assert "SR-2026-0011" in b and "SR-2026-0016" in b, "dropdown SR ไม่มีใบรับคืนของ 0140"
    assert "SR-2026-0014" not in b, "dropdown SR หลุดใบรับคืนของใบอื่น (SR-0014=0141)"
    after(page, "()=>pickSR('SR-2026-0016')")     # SR-0016 คืน 2 กล่อง
    d = ev(page, "()=>({sr:createWizard.data.sr, qty:createWizard.data.lines[0].qty, max:createWizard.data.lines[0].max})")
    assert d["sr"] == "SR-2026-0016", "เลือกใบรับคืนแล้วไม่ติด"
    assert d["qty"] == 2 and d["max"] == 2, f"จำนวนไม่ได้มาจากใบรับคืน (คาด 2, ได้ {d})"
    return f"RET → เลือก SR-2026-0016 (2 กล่อง) · จำนวน=2 · cap=2 (มาจากใบรับคืน) · dropdown เฉพาะ SR ของ 0140"


def c_fn06(page):
    """[FN-06 · S-02 · BR-04] ส่วนลดภายหลัง (DISC) ปรับราคา/หน่วยได้ แต่ไม่เกินราคาเดิม"""
    open_(page); open_create(page)
    after(page, "()=>pickInv('INV-2026-0137')")
    after(page, "()=>setReason('DISC')")          # price mode
    lid = ev(page, "()=>createWizard.data.lines[0].id")
    orig = ev(page, "()=>createWizard.data.lines[0].origPrice")   # 18000 (S-2002)
    goto_step(page, 3)
    # ราคาเกินราคาเดิม → extraLineValidate บล็อก wizardNext
    after(page, "()=>updateLine('%s','unit_price',%d)" % (lid, orig + 500))
    after(page, "()=>wizardNext()")
    assert ev(page, "()=>createWizard.step") == 3, "ราคาลดเกินราคาเดิมแต่ยังก้าวต่อได้"
    assert "เกินราคาเดิม" in last_toast(page), f"ราคาเกินไม่เตือน ({last_toast(page)})"
    assert "ราคาลดเกินราคาเดิม" in create_text(page), "ไม่มี meta เตือนราคาลดเกินราคาเดิมใต้บรรทัด"
    # ปรับราคา ≤ ราคาเดิม → ผ่าน
    after(page, "()=>updateLine('%s','unit_price',%d)" % (lid, 2000))
    after(page, "()=>wizardNext()")
    assert ev(page, "()=>createWizard.step") == 4, f"ราคา ≤ เดิมแล้วยังก้าวต่อไม่ได้ ({last_toast(page)})"
    return f"DISC (ลดราคา) · ราคา {orig+500} > เดิม {orig} → บล็อก · ราคา 2000 ≤ เดิม → ผ่าน"


def c_fn07(page):
    """[FN-07 · S-03 · BR-03] คิดจำนวนเกิน/ราคาผิด: ลดเฉพาะบรรทัดที่เลือก · ลบบรรทัดอื่นออกได้"""
    open_(page); open_create(page)
    after(page, "()=>pickInv('INV-2026-0137')")   # 2 บรรทัด (S-2002, S-2001)
    after(page, "()=>setReason('QTY')")
    n0 = ev(page, "()=>createWizard.data.lines.length")
    assert n0 == 2, f"ใบ 0137 ควรดึง 2 บรรทัด (ได้ {n0})"
    rm = ev(page, "()=>createWizard.data.lines[1].id")
    after(page, "()=>removeLine('%s')" % rm)
    assert ev(page, "()=>createWizard.data.lines.length") == 1, "ลบบรรทัดอื่นออกไม่ได้"
    goto_step(page, 3)
    b = create_text(page)
    assert "readdLine" in ev(page, "()=>document.getElementById('create-drawer-content').innerHTML"), \
        "ไม่มีปุ่มเพิ่มบรรทัดใบเดิมที่ลบออกกลับเข้ามา (step3Block)"
    # เพิ่มกลับได้
    after(page, "()=>readdLine(1)")
    assert ev(page, "()=>createWizard.data.lines.length") == 2, "readdLine ไม่คืนบรรทัด"
    return "ใบ 2 บรรทัด → ลบเหลือ 1 (ลดเฉพาะบรรทัดที่เลือก) · step3Block ให้เพิ่มบรรทัดเดิมกลับได้"


def c_fn08(page):
    """[FN-08 · S-04 · BR-03,BR-10] ลดหลายรอบ: บรรทัดแสดงจำนวนเดิม · ลดแล้ว · ลดได้อีก ถูกต้อง"""
    open_(page); open_create(page)
    after(page, "()=>pickInv('INV-2026-0140')")   # 10 กล่อง · มี R1(1,sent) + R6(2,draft) ลดแล้ว
    after(page, "()=>setReason('RET')")
    room = ev(page, "()=>lineRoom('INV-2026-0140',0,null)")
    # R1 (sent, RET 1) + R6 (draft, RET 2) → ลดแล้ว 3 ก. → เหลือ 7
    assert room["origQty"] == 10, f"จำนวนเดิมผิด ({room['origQty']})"
    assert room["netDone"] > 0, "ลดแล้ว (netDone) = 0 ทั้งที่ควรมีรอบก่อน"
    assert room["qtyLeft"] == 7, f"ลดได้อีกผิด (คาด 7, ได้ {room['qtyLeft']})"
    goto_step(page, 3)
    b = create_text(page)
    assert "ใบเดิม 10" in b, "meta ไม่แสดงจำนวนเดิม 10"
    assert "ลดแล้ว" in b and "ลดจำนวนได้อีก 7" in b, f"meta ลดแล้ว/ลดได้อีกไม่ถูก"
    return f"ลดหลายรอบ 0140: เดิม 10 · ลดแล้ว ฿{room['netDone']:,.0f} · ลดจำนวนได้อีก {room['qtyLeft']}"


def c_cap_display(page):
    """[FN-05/FN-08 · BR-06 · C3.8] เลขที่โชว์ 'ลดจำนวนได้อีก N' = เพดานที่บังคับจริง (SR-capped)"""
    open_(page); open_create(page)
    after(page, "()=>pickInv('INV-2026-0140')")   # 10 กล่อง · room.qtyLeft=7 (R1+R6 ลดแล้ว)
    after(page, "()=>setReason('RET')")
    after(page, "()=>pickSR('SR-2026-0016')")      # SR คืน 2 → l.max=2 (แคบกว่า room 7)
    goto_step(page, 3)
    # ก่อนแก้: meta โชว์ 7 (room.qtyLeft) แต่ block ที่ 2 (l.max) — display ต้องตรงกับ enforcement
    r = assert_line_cap_display_matches_enforced(
        page, "updateLine(createWizard.data.lines[0].id,'qty',{v})", note="RET+SR-0016",
        scope="#create-drawer-content")
    assert abs(r["cap"] - 2) < 1e-9, f"เลขที่โชว์ควร = 2 (ตามใบรับคืน) แต่ได้ {r['cap']} · meta: {r['metaText']}"
    assert r["suffix"], f"เพดานมาจากใบรับคืน (l.max<room) ต้องต่อท้าย '(ตามใบรับคืน)' · meta: {r['metaText']}"
    return f"RET+SR-0016: โชว์ 'ลดจำนวนได้อีก {int(r['cap'])} (ตามใบรับคืน)' · qty=2 ok · qty=3 แดง (display=enforcement)"


def c_cap_display_qty(page):
    """[FN-08 · BR-03] เหตุผล QTY (ไม่มีใบรับคืน) โชว์เพดานตามใบแจ้งหนี้ (room) · ไม่มี '(ตามใบรับคืน)'"""
    open_(page); open_create(page)
    after(page, "()=>pickInv('INV-2026-0140')")
    after(page, "()=>setReason('QTY')")            # qty mode · l.max = room.qtyLeft (7) · ไม่มี SR
    goto_step(page, 3)
    r = assert_line_cap_display_matches_enforced(
        page, "updateLine(createWizard.data.lines[0].id,'qty',{v})", note="QTY (no SR)",
        scope="#create-drawer-content")
    assert abs(r["cap"] - 7) < 1e-9, f"QTY reason ควรโชว์ room.qtyLeft=7 แต่ได้ {r['cap']} · meta: {r['metaText']}"
    assert not r["suffix"], f"QTY ไม่มีใบรับคืน — ต้องไม่มี '(ตามใบรับคืน)' · meta: {r['metaText']}"
    return f"QTY (ไม่มี SR): โชว์ 'ลดจำนวนได้อีก {int(r['cap'])}' (ตามใบแจ้งหนี้) · qty=7 ok · qty=8 แดง · ไม่มี suffix"


def c_fn09(page):
    """[FN-09 · S-05 · BR-02] ยอดลดเกินคงเหลือ/เกินจำนวนเดิม → บล็อก + hard-warn บอกยอด"""
    open_(page); open_create(page)
    after(page, "()=>pickInv('INV-2026-0140')")
    after(page, "()=>setReason('RET')")
    lid = ev(page, "()=>createWizard.data.lines[0].id")
    mx = ev(page, "()=>createWizard.data.lines[0].max")      # 7
    goto_step(page, 3)
    after(page, "()=>updateLine('%s','qty',%d)" % (lid, mx + 50))   # เกินจำนวน + เกินมูลค่าคงเหลือ
    b = create_text(page)
    assert "ยอดลดหนี้เกินยอดคงเหลือ" in b, "ไม่มี hard-warn ยอดเกินคงเหลือ"
    assert "เกิน ฿" in b, "hard-warn ไม่บอกยอดที่เกิน"
    ov = ev(page, "()=>cnOver(createWizard.data)")
    assert ov and ov["over"] > 0, "cnOver ไม่จับยอดเกิน"
    # ก้าวต่อไม่ได้ (lineOver → overMsg)
    after(page, "()=>wizardNext()")
    assert ev(page, "()=>createWizard.step") == 3, "ยอด/จำนวนเกินแต่ยังก้าวต่อได้"
    assert "ลดได้อีก" in last_toast(page), f"เกินจำนวนไม่เตือนยอดที่ลดได้ ({last_toast(page)})"
    # submit ก็ถูกบล็อก (_block)
    assert ev(page, "()=>DOC.blockReason(createWizard.data)").startswith("ยอดลดหนี้เกิน"), "blockReason ไม่บล็อกยอดเกิน"
    return f"qty {mx+50} > cap {mx} → hard-warn บอกยอดเกิน · wizardNext บล็อก · submit บล็อก"


def c_fn10(page):
    """[FN-10 · BR-05] ต้องกรอกคำอธิบายเหตุผล ≥ 10 ตัวอักษร"""
    open_(page); open_create(page)
    after(page, "()=>pickInv('INV-2026-0140')")
    after(page, "()=>setReason('RET')")
    after(page, "()=>pickSR('SR-2026-0016')")
    goto_step(page, 2)
    after(page, "()=>{createWizard.data.reasonText='สั้น';renderCreateDrawer();}")   # < 10
    after(page, "()=>wizardNext()")
    assert ev(page, "()=>createWizard.step") == 2, "คำอธิบาย < 10 ตัวแต่ก้าวต่อได้"
    assert ev(page, "()=>document.getElementById('f-reasonText').classList.contains('is-error')"), \
        "ช่องคำอธิบายไม่ขึ้น error"
    after(page, "()=>{createWizard.data.reasonText='รับคืนสินค้าชำรุด 2 กล่อง';renderCreateDrawer();}")   # ≥ 10
    after(page, "()=>wizardNext()")
    assert ev(page, "()=>createWizard.step") == 3, f"คำอธิบาย ≥ 10 ตัวแล้วยังก้าวต่อไม่ได้ ({last_toast(page)})"
    return "คำอธิบาย 'สั้น' (<10) → บล็อก + field error · ≥10 ตัว → ผ่านไป step 3"


# ═══════════════════════════ หมวด 3 · อนุมัติ (DOA) ═══════════════════════════

def c_fn11(page):
    """[FN-11 · S-06 · BR-07] ส่งอนุมัติ: สายเปลี่ยนตามมูลค่า และต้องเลือกคนครบทุกขั้น"""
    open_(page)
    # (ก) tier เปลี่ยนตามมูลค่า
    t1 = ev(page, "()=>resolveDoa({lines:[{qty:1,unit_price:1000,vat_mode:'add',vat_pct:7}],endbill:{}}).steps.length")
    t2 = ev(page, "()=>resolveDoa({lines:[{qty:1,unit_price:100000,vat_mode:'add',vat_pct:7}],endbill:{}}).steps.length")
    t3 = ev(page, "()=>resolveDoa({lines:[{qty:1,unit_price:400000,vat_mode:'add',vat_pct:7}],endbill:{}}).steps.length")
    assert (t1, t2, t3) == (1, 2, 3), f"สายไม่เปลี่ยนตามมูลค่า (ได้ {t1}/{t2}/{t3} · ต้อง 1/2/3)"
    # (ข) เปิดโมดัลส่งอนุมัติ R6 (draft ยอดต่ำ) → 1 slot · ยังไม่เลือกคน → confirmSubmit บล็อก
    after(page, "()=>openSubmitModal('R6')")
    nslot = ev(page, "()=>modalState.slots.length")
    assert nslot == ev(page, "()=>resolveDoa(findRec('R6')).steps.length"), "จำนวน slot ไม่ตรง resolveDoa"
    after(page, "()=>confirmSubmit()")
    assert ev(page, "()=>findRec('R6').status") == "draft", "slot ว่างแต่ส่งอนุมัติผ่าน"
    assert ev(page, "()=>modalState.err") is True, "slot ว่างไม่ถูก mark error"
    # เลือกคนจริง (mgr-sales ไม่ใช่ ME) → confirmSubmit → pending
    after(page, "()=>comboPick('slot-0','มานพ ขายเก่ง')")
    assert ev(page, "()=>modalState.slots[0].assignee") == "มานพ ขายเก่ง", "เลือกคนแล้วไม่ติด"
    after(page, "()=>confirmSubmit()")
    d = ev(page, "()=>findRec('R6')")
    assert d["status"] == "pending_approval", "เลือกครบแล้วส่งอนุมัติไม่สำเร็จ"
    assert d["approval_chain"][0]["assignee"] == "มานพ ขายเก่ง", "chain ไม่บันทึกคนที่เลือก"
    return f"tier ตามมูลค่า 1/2/3 · R6 slot ว่าง → บล็อก · เลือกคน → pending (คน=มานพ ขายเก่ง)"


def c_fn12(page):
    """[FN-12 · S-06 · BR-08] อนุมัติครบสาย → เลข CN-ปี-ลำดับ + สถานะ 'อนุมัติแล้ว'"""
    open_(page)
    # R4 = pending 2 ขั้น (มานพ mgr-sales · ประเสริฐ mgr-acc)
    assert ev(page, "()=>findRec('R4').status") == "pending_approval"
    assert ev(page, "()=>findRec('R4').code") == "", "ก่อนอนุมัติครบต้องยังไม่มีเลข CN"
    persona(page, 1)   # มานพ (mgr-sales) — ขั้น 1
    after(page, "()=>confirmApprove('R4')")
    assert ev(page, "()=>findRec('R4').status") == "pending_approval", "อนุมัติขั้น 1 แล้วข้ามไป approved"
    assert ev(page, "()=>findRec('R4').approval_chain[0].status") == "approved", "ขั้น 1 ไม่ถูก mark approved"
    persona(page, 2)   # ประเสริฐ (mgr-acc) — ขั้นสุดท้าย
    after(page, "()=>confirmApprove('R4')")
    d = ev(page, "()=>findRec('R4')")
    assert d["status"] == "approved", "อนุมัติครบแล้วสถานะไม่ใช่ approved"
    assert d["code"] and re.match(r"^CN-2026-\d{4}$", d["code"]), f"เลขที่ไม่ใช่ CN-2026-NNNN (ได้ {d['code']})"
    assert d["code"].startswith("CN-2026-"), f"เลขที่ไม่ใช่ปี ค.ศ. ({d['code']})"
    # docPill approved = 'อนุมัติแล้ว · รอส่ง'
    assert "อนุมัติแล้ว" in ev(page, "()=>docPill('approved')"), "pill approved ไม่แสดง 'อนุมัติแล้ว'"
    return f"R4 อนุมัติ 2 ขั้น (มานพ→ประเสริฐ) → ออกเลข {d['code']} (ค.ศ.) · status=approved 'อนุมัติแล้ว'"


def c_fn13(page):
    """[FN-13 · S-07] ไม่อนุมัติต้องใส่เหตุผล → กลับเป็นร่าง + เห็นรอบก่อนหน้า (append-only)"""
    open_(page)
    # R5 = pending 3 ขั้น (มานพ approved · ประเสริฐ pending ปัจจุบัน · อรุณี)
    persona(page, 2)   # ประเสริฐ = ขั้นปัจจุบัน
    n_hist0 = ev(page, "()=>(findRec('R5').approval_history||[]).length")
    after(page, "()=>openRejectModal('R5')")
    # เหตุผลว่าง → กด OK → เตือน ไม่ตีกลับ
    after(page, "()=>document.getElementById('md-ok').click()")
    assert ev(page, "()=>findRec('R5').status") == "pending_approval", "เหตุผลว่างแต่ตีกลับได้"
    assert "เหตุผล" in last_toast(page), f"เหตุผลว่างไม่เตือน ({last_toast(page)})"
    # ใส่เหตุผล → ตีกลับ → draft + history +1
    after(page, "()=>{document.getElementById('md-reason').value='ราคาไม่ตรงสัญญา ตรวจใหม่';document.getElementById('md-ok').click();}")
    d = ev(page, "()=>findRec('R5')")
    assert d["status"] == "draft", "ตีกลับแล้วไม่เป็นร่าง"
    assert (d["approval_history"] or []) and len(d["approval_history"]) == n_hist0 + 1, "รอบก่อนหน้าไม่ถูกเก็บ (append-only)"
    # renderSignTab เห็น 'รอบก่อนหน้า'
    open_view(page, "R5"); view_tab(page, "sign")
    assert "รอบก่อนหน้า" in view_text(page), "sign tab ไม่แสดงรอบก่อนหน้าที่ถูกตีกลับ"
    return "R5 ตีกลับ: เหตุผลว่าง→บล็อก · ใส่เหตุผล→draft + approval_history +1 · sign tab เห็นรอบก่อน"


def c_fn14(page):
    """[FN-14 · S-08] ผู้ส่งไม่เห็นปุ่มอนุมัติใบของตัวเอง (SoD · render-assert)"""
    open_(page)
    # ME default = วราภรณ์ = ผู้ส่ง R4/R5 → canActStep=false
    assert ev(page, "()=>findRec('R4').submittedBy") == "วราภรณ์ บัญชีดี" == ev(page, "()=>ME.name")
    acts = ev(page, "()=>DOC.viewActions(findRec('R4'), 'pending_approval')")
    assert "openApproveModal" not in acts, "ผู้ส่งเห็นปุ่มอนุมัติใบตัวเอง (SoD หลุด)"
    assert "openRejectModal" not in acts, "ผู้ส่งเห็นปุ่มไม่อนุมัติใบตัวเอง"
    assert ev(page, "()=>canActStep(findRec('R4'))") is False, "canActStep ปล่อยให้ผู้ส่งกดอนุมัติเอง"
    # เรนเดอร์ view จริง (sign tab) → ไม่มีปุ่มอนุมัติ/ไม่อนุมัติในไทม์ไลน์
    open_view(page, "R4"); view_tab(page, "sign")
    html = ev(page, "()=>document.getElementById('view-drawer-content').innerHTML")
    assert "openApproveModal('R4')" not in html, "sign tab โชว์ปุ่มอนุมัติให้ผู้ส่ง"
    return "ผู้ส่ง (วราภรณ์) เปิด R4: viewActions/sign ไม่มีปุ่มอนุมัติ/ไม่อนุมัติ · canActStep=false"


def c_fn17(page):
    """[FN-17 · S-11 · BR-02] คงค้างใบเดิมลดลงระหว่างรออนุมัติจนไม่พอ → อนุมัติไม่ได้ (re-check ตอนอนุมัติ)"""
    open_(page)
    persona(page, 1)   # มานพ = ขั้น 1 ของ R4
    after(page, "()=>confirmApprove('R4')")   # ขั้น 1 ผ่าน → เหลือขั้น 2 (ประเสริฐ, ขั้นสุดท้าย)
    assert ev(page, "()=>findRec('R4').approval_chain[1].status") == "pending"
    # จำลองรับชำระใบเดิม (rv-simulate demo hook) จน outstanding เหลือน้อยกว่ายอดลด
    after(page, "()=>demoPay('R4')")
    assert ev(page, "()=>!!document.getElementById('md-amt')"), "demoPay ไม่เปิด modal จำลองรับชำระ"
    after(page, "()=>document.getElementById('md-ok').click()")   # ค่า default = คงค้างทั้งหมด → เหลือ 0
    out = ev(page, "()=>invOutstanding('INV-2026-0141','R4')")
    grand = ev(page, "()=>totals(findRec('R4')).grand")
    assert out < grand, f"จำลองชำระแล้วคงค้าง ({out}) ควร < ยอดลด ({grand})"
    # ขั้นสุดท้ายอนุมัติ → approveGuard บล็อก
    persona(page, 2)   # ประเสริฐ = ขั้นสุดท้าย
    after(page, "()=>confirmApprove('R4')")
    d = ev(page, "()=>findRec('R4')")
    assert d["status"] == "pending_approval", "คงค้างไม่พอแต่อนุมัติครบสายได้ (S-11 หลุด)"
    assert d["approval_chain"][1]["status"] == "pending", "ขั้นสุดท้ายถูก mark approved ทั้งที่ยอดไม่พอ"
    assert "อนุมัติไม่ได้" in last_toast(page) and "คงค้าง" in last_toast(page), f"ไม่มีข้อความบล็อกยอดไม่พอ ({last_toast(page)})"
    return f"R4 ขั้น1 ผ่าน · จำลองรับชำระ 0141 → คงค้าง ฿{out:,.0f} < ยอดลด ฿{grand:,.0f} → ขั้นสุดท้ายบล็อก"


# ═══════════════════════════ หมวด 4 · หลังอนุมัติ ═══════════════════════════

def c_fn15(page):
    """[FN-15 · S-09] ยกเลิกร่าง/รออนุมัติได้พร้อมเหตุผล → cancelled"""
    open_(page)
    # (ก) ยกเลิกร่าง R6
    after(page, "()=>openCancelCN('R6')")
    after(page, "()=>document.getElementById('md-ok').click()")   # เหตุผลว่าง → เตือน
    assert ev(page, "()=>findRec('R6').status") == "draft", "เหตุผลว่างแต่ยกเลิกได้"
    after(page, "()=>{document.getElementById('md-reason').value='ลูกค้ายกเลิกคำขอ';document.getElementById('md-ok').click();}")
    d6 = ev(page, "()=>findRec('R6')")
    assert d6["status"] == "cancelled" and d6["cancelInfo"]["reason"] == "ลูกค้ายกเลิกคำขอ", "ยกเลิกร่างไม่สำเร็จ/ไม่เก็บเหตุผล"
    # (ข) ยกเลิกใบรออนุมัติ R4 (ผู้ส่ง = ME) → pending slots กลายเป็น cancelled
    after(page, "()=>openCancelCN('R4')")
    after(page, "()=>{document.getElementById('md-reason').value='ถอนจากรออนุมัติ';document.getElementById('md-ok').click();}")
    d4 = ev(page, "()=>findRec('R4')")
    assert d4["status"] == "cancelled", "ยกเลิกใบรออนุมัติไม่สำเร็จ"
    assert all(x["status"] == "cancelled" for x in d4["approval_chain"]), "ยกเลิกแล้ว slot ที่ค้างไม่ถูกปิด"
    return "ยกเลิก R6 (ร่าง) + R4 (รออนุมัติ) พร้อมเหตุผล → cancelled · เหตุผลว่าง→บล็อก"


def c_fn16(page):
    """[FN-16 · S-10] ส่งให้ลูกค้า → 'ส่งลูกค้าแล้ว' (sent) + snapshot"""
    open_(page)
    assert ev(page, "()=>findRec('R2').status") == "approved", "R2 ควร approved (พร้อมส่ง)"
    after(page, "()=>openSendCN('R2')")
    assert ev(page, "()=>!!document.getElementById('md-ok')"), "openSendCN ไม่เปิด modal"
    after(page, "()=>document.getElementById('md-ok').click()")   # busy + setTimeout 400 (tracked)
    settle(page)
    d = ev(page, "()=>findRec('R2')")
    assert d["status"] == "sent", "ส่งให้ลูกค้าแล้วสถานะไม่ใช่ sent"
    assert d["sentAt"] and d["sentBy"], "ส่งแล้วไม่บันทึกเวลา/ผู้ส่ง (snapshot)"
    assert "ส่งลูกค้าแล้ว" in ev(page, "()=>docPill('sent')"), "pill sent ไม่แสดง 'ส่งลูกค้าแล้ว'"
    return "R2 approved → ส่งให้ลูกค้า → sent 'ส่งลูกค้าแล้ว' · บันทึก sentAt/sentBy"


def c_fn18(page):
    """[FN-18 · S-14 · BR-09] tab ใบแจ้งหนี้อ้างอิง: คงค้างก่อน/หลังลด + ภาษีขายที่ลด + JE (จำลอง)"""
    open_(page)
    open_view(page, "R2")     # approved → JE renders (applied)
    view_tab(page, "ref")
    b = view_text(page)
    assert "คงค้างก่อนใบนี้" in b and "คงค้างหลังใบนี้" in b, "ref tab ไม่แสดงคงค้างก่อน/หลัง"
    assert "ภาษีขายที่ลด" in b and "ภ.พ.30" in b, "ref tab ไม่แสดงผลกระทบภาษีขาย (VAT Report)"
    assert "รายการบัญชี" in b and "1130 ลูกหนี้การค้า" in b and "2150 ภาษีขาย" in b, "ref tab ไม่แสดง JE (จำลอง)"
    # ตัวเลขคงค้างก่อน/หลังสอดคล้อง
    out = ev(page, "()=>invOutstanding(findRec('R2').inv,'R2')")
    grand = ev(page, "()=>totals(findRec('R2')).grand")
    assert out >= 0 and grand > 0, "คำนวณคงค้าง/ยอดลดผิด"
    return f"ref tab R2: คงค้างก่อน/หลัง · ภาษีขายที่ลด (ภ.พ.30) · JE 1130/2150 (จำลอง F093)"


# ═══════════════════════════ หมวด 5 · ทั่วไป ═══════════════════════════

def c_fn90(page):
    """[FN-90] ค้นหา/กรองสถานะ/เหตุผล + empty state"""
    open_(page)
    total = ev(page, "()=>RECS.length")
    # กรองเหตุผล RET
    after(page, "()=>setFilter('reason','RET')")
    ret = ev(page, "()=>getFilteredRecords().map(r=>r.reason)")
    assert ret and all(x == "RET" for x in ret), f"กรองเหตุผล RET ไม่ทำงาน ({ret})"
    after(page, "()=>setFilter('reason','all')")
    # กรองสถานะ + ค้นหา
    after(page, "()=>setFilter('status','sent')")
    assert all(r == "sent" for r in ev(page, "()=>getFilteredRecords().map(r=>r.status)")), "กรองสถานะ sent ไม่ทำงาน"
    after(page, "()=>setFilter('status','all')")
    after(page, "()=>{state.filters.search='INV-2026-0141';renderTableOnly();}")
    invs = ev(page, "()=>getFilteredRecords().map(r=>r.inv)")
    assert invs and all(x == "INV-2026-0141" for x in invs), f"ค้นหา inv ไม่ทำงาน ({invs})"
    # empty state
    after(page, "()=>{state.filters.search='ไม่มีทางเจอ-zzz-999';renderTableOnly();}")
    tb = ev(page, "()=>document.getElementById('table-body').textContent")
    assert "ไม่พบรายการ" in tb, "ค้นหาไม่เจอแต่ไม่ขึ้น empty state"
    assert ev(page, "()=>getFilteredRecords().length") == 0, "empty state แต่ยังมีผลลัพธ์"
    return f"กรอง RET/sent · ค้นหา inv · empty state 'ไม่พบรายการ' (จาก {total} ใบ)"


def c_fn91(page):
    """[FN-91 · GR-4] ประวัติ append-only ทุกการกระทำ (ไม่ลบ ไม่ทับ)"""
    open_(page)
    n_rec0 = ev(page, "()=>RECS.length")
    a0 = ev(page, "()=>findRec('R6').audit.length")
    first0 = ev(page, "()=>findRec('R6').audit[findRec('R6').audit.length-1].act")   # entry แรกสุด (ล่างสุด)
    # ทำ action (ยกเลิก) → audit ต้อง +1 และ entry เดิมยังอยู่ท้ายสุด
    after(page, "()=>openCancelCN('R6')")
    after(page, "()=>{document.getElementById('md-reason').value='ทดสอบ append-only';document.getElementById('md-ok').click();}")
    a1 = ev(page, "()=>findRec('R6').audit.length")
    first1 = ev(page, "()=>findRec('R6').audit[findRec('R6').audit.length-1].act")
    assert a1 == a0 + 1, f"audit ไม่ append (คาด {a0}+1 ได้ {a1})"
    assert first1 == first0, "entry เดิมถูกทับ/ลบ (ไม่ append-only)"
    assert ev(page, "()=>findRec('R6').audit[0].act").startswith("ยกเลิก"), "action ล่าสุดไม่ได้อยู่บนสุด"
    # ไม่มี hard delete: RECS ไม่ลด · ใบที่ยกเลิกยังอยู่
    assert ev(page, "()=>RECS.length") == n_rec0, "RECS ลดลง (มี hard delete)"
    assert ev(page, "()=>!!findRec('R6')") and ev(page, "()=>findRec('R6').status") == "cancelled", "ใบยกเลิกหายไป (ควรคงไว้)"
    # history tab เรนเดอร์ timeline
    open_view(page, "R6"); view_tab(page, "history")
    assert "ประวัติ" in view_text(page) and "append-only" in view_text(page), "history tab ไม่เรนเดอร์"
    return f"audit {a0}→{a1} (append) · entry เดิมคงอย่างเดิม · RECS คงที่ (ไม่ลบ) · history tab OK"


def c_fn92(page):
    """[FN-92 · OB-6] PDF: อ้างเลข/วันที่ใบเดิม · มูลค่าเดิม/ถูกต้อง/ผลต่าง · เหตุผล · ค.ศ."""
    open_(page)
    open_view(page, "R2"); view_tab(page, "pdf")
    b = view_text(page)
    s = ev(page, "()=>findRec('R2')")
    iv_date = ev(page, "()=>formatThaiDate(INV_BY[findRec('R2').inv].date)")
    assert s["inv"] in b, "PDF ไม่อ้างเลขใบแจ้งหนี้เดิม"
    assert iv_date in b, "PDF ไม่อ้างวันที่ใบเดิม"
    assert "มูลค่าตามใบกำกับเดิม" in b and "มูลค่าที่ถูกต้อง" in b and "ผลต่าง" in b, "PDF ไม่แสดงมูลค่าเดิม/ถูกต้อง/ผลต่าง"
    assert "เหตุผลการลดหนี้" in b, "PDF ไม่แสดงเหตุผล"
    # ปี ค.ศ. — ต้องมี 2026 ไม่ใช่ 2569 (พ.ศ.)
    assert "2026" in b and "2569" not in b, "PDF ใช้ปี พ.ศ. หรือไม่มีปี ค.ศ."
    return f"PDF R2: อ้าง {s['inv']} · วันที่ใบเดิม {iv_date} · มูลค่าเดิม/ถูกต้อง/ผลต่าง · เหตุผล · ค.ศ. 2026"


# ═══════════════════════════ NEGATIVES (render-assert · หมวด 'สิ่งที่ไม่รองรับ') ═══════════════════════════

def c_neg_refund(page):
    """[NEG · S-15 refund] ไม่มี affordance คืนเงิน/refund ที่ไหนเลย (render-assert)"""
    open_(page)
    # list page
    assert_text_absent(page, ["คืนเงิน", "refund", "Refund", "REFUND"], scope="#page-content")
    # view ใบ approved (มีปุ่ม action มากสุด)
    open_view(page, "R2")
    assert_text_absent(page, ["คืนเงิน", "refund", "Refund"], scope="#view-drawer-content")
    # sign + ref tab
    view_tab(page, "ref")
    assert_text_absent(page, ["คืนเงิน", "refund"], scope="#view-drawer-content")
    return "ไม่มีข้อความ/ปุ่ม 'คืนเงิน'/'refund' ใน list + view (detail/ref) — S-15 ปิด"


def c_neg_cancel_approved(page):
    """[NEG · S-16] ไม่มีปุ่มยกเลิกบนใบที่อนุมัติแล้ว (approved/sent) — ยกเลิกได้เฉพาะ draft/pending"""
    open_(page)
    # approved (R2) + sent (R1) → viewActions ไม่มี openCancelCN
    for rid, st in [("R2", "approved"), ("R1", "sent")]:
        acts = ev(page, "()=>DOC.viewActions(findRec('%s'), '%s')" % (rid, st))
        assert "openCancelCN" not in acts, f"{rid} ({st}) มีปุ่มยกเลิกทั้งที่อนุมัติแล้ว (S-16 หลุด)"
        assert ev(page, "()=>DOC.rowCancel(findRec('%s'), '%s')" % (rid, st)) is None, f"row menu {rid} ยังมี 'ยกเลิก'"
    # draft/pending ยังยกเลิกได้ (พิสูจน์ว่า guard แยกสถานะจริง ไม่ใช่ปิดหมด)
    assert ev(page, "()=>DOC.rowCancel(findRec('R6'), 'draft')") is not None, "draft ควรยกเลิกได้"
    assert ev(page, "()=>DOC.rowCancel(findRec('R4'), 'pending_approval')") is not None, "pending ควรยกเลิกได้"
    # เรนเดอร์ view จริงของ approved → ไม่มี string ปุ่มยกเลิก
    open_view(page, "R2")
    html = ev(page, "()=>document.getElementById('view-drawer-content').innerHTML")
    assert "openCancelCN('R2')" not in html, "view ใบ approved เรนเดอร์ปุ่มยกเลิก"
    return "approved (R2) + sent (R1): ไม่มีปุ่ม/เมนูยกเลิก · draft/pending ยกเลิกได้ → guard แยกสถานะจริง"


def c_neg_no_sr_crud(page):
    """[NEG · แผน] Sales Return เป็น lookup (mock) เท่านั้น — ไม่มีหน้าจอ/ปุ่มสร้างใบรับคืน"""
    open_(page); open_create(page)
    after(page, "()=>pickInv('INV-2026-0140')")
    after(page, "()=>setReason('RET')")
    goto_step(page, 2)
    # ช่องใบรับคืนเป็น <select> (lookup) จริง
    has_select = ev(page, "()=>!!document.querySelector('#f-sr select')")
    assert has_select, "ช่องใบรับคืนไม่ใช่ dropdown lookup"
    # ไม่มีปุ่ม/ลิงก์สร้างใบรับคืน หรือหน้าจอ CRUD ของ SR
    # (หมายเหตุ: "ใบรับคืนสินค้า (Sales Return)" เป็น label ของช่อง lookup — อนุญาต · ห้ามเฉพาะ affordance CRUD)
    assert_text_absent(page, ["สร้างใบรับคืน", "เพิ่มใบรับคืน", "แก้ไขใบรับคืน", "จัดการใบรับคืน", "รับคืนสินค้าใหม่"],
                       scope="#create-drawer-content")
    # ไม่มี controller เปิดหน้าจอ SR (เป็น data ล้วน)
    no_fn = ev(page, "()=>['openSRDrawer','createSR','openSalesReturn','editSR']"
                    ".every(f=>typeof window[f]==='undefined')")
    assert no_fn, "มีฟังก์ชันเปิด/สร้างหน้าจอ Sales Return (ควรเป็น lookup เท่านั้น)"
    return "ใบรับคืน = <select> lookup · ไม่มีปุ่มสร้าง/แก้/จัดการ SR · ไม่มี controller เปิดหน้าจอ SR"


# ═══════════════════════════ C3.8 · DSP-08 modal-z (wired assert) ═══════════════════════════

def c_modal_z(page):
    """[DSP-08 · C3.8] การ์ด modal ต้องเป็น hit-test บนสุด ณ กึ่งกลาง (ไม่จมใต้ .backdrop) — submit + reason modal"""
    open_(page)
    # (ก) submit modal (R6 draft ยอดต่ำ)
    after(page, "()=>openSubmitModal('R6')")
    assert ev(page, "()=>!!document.querySelector('.modal-overlay #submit-modal')"), "openSubmitModal ไม่เรนเดอร์การ์ด"
    r1 = assert_modal_card_topmost(page, note="submit modal")
    after(page, "()=>closeModal()")
    # (ข) reason modal (ไม่อนุมัติ) — การ์ด .card ใต้ .modal-overlay เดียวกัน
    after(page, "()=>openRejectModal('R4')")
    assert ev(page, "()=>!!document.querySelector('.modal-overlay .card')"), "openRejectModal ไม่เรนเดอร์การ์ด"
    r2 = assert_modal_card_topmost(page, note="reason modal")
    return (f"submit modal: hit กึ่งกลาง=การ์ด (card z:{r1['cardZ']} > backdrop z:{r1['backdropZ']}) · "
            f"reason modal: การ์ด z:{r2['cardZ']} บนสุด (ไม่จมใต้ .backdrop)")


# ═══════════════════════════ เอกสารแนบ (real file picker · 2026-09-21 fix) ═══════════════════════════

def c_attach_real(page):
    """[S-04 · เอกสารแนบ] step 4 ใช้ <input type=file> จริง (ไม่ mock) — เลือกไฟล์จริง →
    อ่าน name+size จริง เข้า attachments · แนบหลายไฟล์พร้อมกัน · removeAttachment ลบได้ ·
    คลิกแล้วไม่มี canned file ถูกยัด (ไม่มี mockUpload/sampleFiles)"""
    open_(page); open_create(page)
    goto_step(page, 4)
    # (ก) input type=file จริง + multiple + zone/ปุ่มยิง picker (ไม่ใช่ mock)
    inp = ev(page, "()=>{const e=document.getElementById('att-file-input');"
                   "return e?{type:e.type,multiple:e.multiple}:null;}")
    assert inp and inp["type"] == "file" and inp["multiple"], f"ไม่มี <input type=file multiple> จริงใน step 4 ({inp})"
    zone_oc = ev(page, "()=>{const z=document.querySelector('#create-drawer-content .upload-zone');return z?z.getAttribute('onclick'):'';}")
    assert "triggerAttachPick" in (zone_oc or ""), f"upload-zone ไม่ยิง file picker จริง ({zone_oc})"
    # (ข) ยังไม่เลือก = ว่าง + ไม่มี mock canned injector เหลืออยู่
    assert ev(page, "()=>createWizard.data.attachments.length") == 0, "ก่อนเลือกไฟล์ attachments ไม่ว่าง (มี canned file ถูกยัด)"
    assert ev(page, "()=>typeof mockUpload") == "undefined", "ยังมี mockUpload (ควรถูกถอด)"
    assert ev(page, "()=>typeof DOC.sampleFiles") == "undefined", "ยังมี DOC.sampleFiles (ควรถูกถอด)"
    # (ค) เลือกไฟล์จริงหลายไฟล์พร้อมกันผ่าน input → อ่าน name/size จริง
    d = tempfile.mkdtemp()
    f1 = Path(d) / "return-photo-REAL.png"; f1.write_bytes(b"x" * 700000)   # ~684 KB
    f2 = Path(d) / "agreement-REAL.pdf"; f2.write_bytes(b"y" * 2500000)     # ~2.4 MB
    page.set_input_files("#att-file-input", [str(f1), str(f2)])
    page.wait_for_function("()=>createWizard.data.attachments.length===2", timeout=3000)
    atts = ev(page, "()=>createWizard.data.attachments.map(a=>({name:a.name,size:a.size}))")
    assert atts[0]["name"] == "return-photo-REAL.png" and atts[1]["name"] == "agreement-REAL.pdf", f"ชื่อไฟล์จริงไม่ถูกอ่าน ({atts})"
    assert re.match(r"^\d+(\.\d+)? (B|KB|MB)$", atts[0]["size"]) and atts[0]["size"].endswith("KB"), f"ขนาดไฟล์ผิดรูปแบบ ({atts[0]})"
    assert atts[1]["size"].endswith("MB"), f"ไฟล์ใหญ่ควรเป็น MB ({atts[1]})"
    # เรนเดอร์จริงโชว์ชื่อ+ขนาด · input value ถูก reset (re-pick ไฟล์เดิมได้)
    body = create_text(page)
    assert "return-photo-REAL.png" in body and atts[0]["size"] in body, "step 4 ไม่เรนเดอร์ชื่อ/ขนาดไฟล์จริง"
    assert ev(page, "()=>document.getElementById('att-file-input').value") == "", "ไม่ได้ล้างค่า input หลังเลือก (re-pick ไฟล์เดิมจะไม่ยิง)"
    # (ง) removeAttachment ลบไฟล์ที่เลือกได้
    after(page, "()=>removeAttachment(0)")
    rem = ev(page, "()=>createWizard.data.attachments.map(a=>a.name)")
    assert rem == ["agreement-REAL.pdf"], f"removeAttachment ลบผิด ({rem})"
    return "step 4 = <input type=file multiple> จริง · เลือก 2 ไฟล์ → name+size จริง (684 KB · 2.4 MB) · list เรนเดอร์จริง · input reset · remove ได้ · ไม่มี mockUpload/sampleFiles"


# ═══════════════════════════ C3.8 · STATUS-GUARD bypass (ปุ่มซ่อน แต่ controller เรียกได้) ═══════════════════════════

def c_bypass_c1_cancel_sent(page):
    """[FIX-01 · C1 · BLOCK] ยกเลิกใบที่ 'ส่งลูกค้าแล้ว' (sent) เรียก openCancelCN ตรง → ต้อง block
    ในฟังก์ชัน (ไม่เป็น cancelled · ยอด AR/VAT ไม่เด้งกลับ) + warning toast ชี้ 'ออกเอกสารแก้ไข'"""
    open_(page)
    r = assert_status_guard(
        page, "openCancelCN('R1')", "R1", "sent",
        "({s:findRec('R1').status,c:findRec('R1').code,n:(findRec('R1').approval_chain||[]).length})",
        note="C1 cancel-on-sent")
    assert ev(page, "()=>findRec('R1').status") == "sent", "R1 (sent) ถูกยกเลิกทั้งที่ออกเลขแล้ว (C1 หลุด)"
    assert not ev(page, "()=>!!document.querySelector('.modal-overlay')"), "guard block แล้วแต่ยังเปิด modal ยกเลิก"
    return f"openCancelCN ใบ sent → block ในฟังก์ชัน · status คง sent · toast='{r['toast'][:48]}'"


def c_bypass_c2_send_draft(page):
    """[FIX-02 · C2 · BLOCK] ส่งใบ 'ฉบับร่าง' (draft ไม่มีเลข) เรียก openSendCN ตรง → ต้อง block
    (ไม่กลายเป็น sent · ไม่มี sentAt) + warning toast 'ต้องอนุมัติครบก่อนส่ง'"""
    open_(page)
    r = assert_status_guard(
        page, "openSendCN('R6')", "R6", "draft",
        "({s:findRec('R6').status,c:findRec('R6').code,sent:!!findRec('R6').sentAt})",
        note="C2 send-on-draft")
    assert ev(page, "()=>findRec('R6').status") == "draft", "R6 (draft) ถูกส่งให้ลูกค้าได้ (C2 หลุด)"
    assert not ev(page, "()=>!!findRec('R6').sentAt"), "draft ส่งไม่ได้แต่มี sentAt"
    assert not ev(page, "()=>!!document.querySelector('.modal-overlay')"), "guard block แล้วแต่ยังเปิด modal ส่ง"
    return f"openSendCN ใบ draft → block · status คง draft · ไม่มี sentAt · toast='{r['toast'][:40]}'"


def c_bypass_c4_submit_approved(page):
    """[FIX-03 · C4 · BLOCK] ส่งอนุมัติซ้ำใบ 'approved' (ออกเลขแล้ว) เรียก confirmSubmit ตรง → ต้อง block
    (chain/code เดิมไม่ถูกเขียนทับ · ไม่กลับเป็น pending) + warning toast · openSubmitModal ก็ block"""
    open_(page)
    # (ก) openSubmitModal (opener) guard
    after(page, "()=>openSubmitModal('R2')")
    assert not ev(page, "()=>!!document.querySelector('.modal-overlay')"), "openSubmitModal เปิด modal ให้ใบ approved (opener guard หลุด)"
    assert "เฉพาะฉบับร่าง" in last_toast(page), f"openSubmitModal ไม่เตือน block ({last_toast(page)})"
    # (ข) confirmSubmit (commit) guard — เรียกตรงผ่าน modalState
    r = assert_status_guard(
        page, "modalState.id='R2'; confirmSubmit();", "R2", "approved",
        "({s:findRec('R2').status,c:findRec('R2').code,n:(findRec('R2').approval_chain||[]).length,"
        "sb:findRec('R2').submittedBy})",
        note="C4 submit-on-approved")
    assert ev(page, "()=>findRec('R2').status") == "approved", "R2 (approved) ถูกส่งอนุมัติซ้ำ (C4 หลุด)"
    return f"submit ใบ approved → openSubmitModal + confirmSubmit block · chain/code เดิมคงอยู่ · toast='{r['toast'][:36]}'"


# ═══════════════════════════ ส่วนลดท้ายบิล (BA-approved · Rule 1 cap + Rule 2 ม.86/10) ═══════════════════════════

def c_eb_vat(page):
    """[FN-18 · ส่วนลดท้ายบิล · ม.86/10] end-bill ลดฐานภาษี → VAT คิดใหม่จากฐานที่ลดแล้ว (ภ.พ.30/JE/PDF โชว์ VAT ที่ลดลง)"""
    open_(page); open_create(page)
    after(page, "()=>pickInv('INV-2026-0141')")
    after(page, "()=>setReason('QTY')")            # qty mode · qty=30 (คงเหลือ) → ฐาน 360,000
    base = ev(page, "()=>totals(createWizard.data)")
    assert abs(base["before"] - 360000) < 0.01 and abs(base["vat"] - 25200) < 0.01 and abs(base["after"] - 385200) < 0.01, \
        f"ฐานเริ่มต้น INV-2026-0141 ไม่ใช่ 360,000/25,200/385,200 ({base})"
    # (ก) percent 10% → ฐานลด 360,000→324,000 · VAT 25,200→22,680 · grand 346,680
    after(page, "()=>{createWizard.data.endbill={enabled:true,mode:'percent',value:10}; updateLineSummaryOnly();}")
    t = ev(page, "()=>totals(createWizard.data)")
    assert abs(t["netBefore"] - 324000) < 0.01, f"ฐานภาษีหลังส่วนลดควร 324,000 ({t['netBefore']})"
    assert abs(t["netVat"] - 22680) < 0.01, f"VAT ที่ลด (ภ.พ.30) ต้องคิดใหม่ = 22,680 ไม่ใช่ 25,200 ({t['netVat']})"
    assert abs(t["grand"] - 346680) < 0.01, f"ยอดสุทธิควร 346,680 ({t['grand']})"
    assert abs(t["vat"] - 25200) < 0.01, f"VAT รายบรรทัด (engine B2 v2) ต้องไม่ถูกแตะ = 25,200 ({t['vat']})"
    assert t["grand"] < base["after"] - 0.01, "grand ต้องลดลงจากยอดเต็มก่อนส่วนลด"
    assert abs((t["netBefore"] + t["netVat"]) - t["grand"]) < 0.01, "ฐานใหม่ + VAT ใหม่ ต้องเท่ากับ grand (JE บาลานซ์)"
    # summary เรนเดอร์จริงต้องโชว์ VAT ที่ลด (22,680) + อ้าง ม.86/10 · ฐานใหม่ 324,000
    goto_step(page, 3)
    b = create_text(page)
    assert "22,680" in b and "ม.86/10" in b, "summary ไม่โชว์ VAT ที่คิดใหม่ (22,680 · ม.86/10)"
    assert "324,000" in b, "summary ไม่โชว์ฐานภาษีหลังหักส่วนลด (324,000)"
    # (ข) amount mode ฿1,000 (VAT-inclusive) → VAT ลดตามส่วน VAT ของ 1,000 (≈65.42)
    after(page, "()=>{createWizard.data.endbill={enabled:true,mode:'amount',value:1000}; updateLineSummaryOnly();}")
    a = ev(page, "()=>totals(createWizard.data)")
    assert abs((base["vat"] - a["netVat"]) - 65.42) < 0.05, f"amount ฿1,000: VAT ต้องลด ≈65.42 ({base['vat']-a['netVat']:.2f})"
    assert abs(a["grand"] - (base["after"] - 1000)) < 0.01, f"amount: grand ต้อง = after-1000 ({a['grand']})"
    # (ค) ภ.พ.30 (ref) + JE + PDF ของใบ approved ต้องสะท้อน VAT ที่ลด — ใส่ end-bill 10% ให้ R2 (approved → JE render)
    after(page, "()=>closeCreateDrawer()")
    ref = ev(page, "()=>{const s=findRec('R2'); s.endbill={enabled:true,mode:'percent',value:10}; const t=totals(s); "
                  "return {netVat:t.netVat, vat:t.vat, grand:t.grand, netBefore:t.netBefore};}")
    assert ref["netVat"] < ref["vat"] - 0.01, "R2+end-bill: netVat ต้อง < vat (VAT ถูกลด)"
    money = ev(page, "()=>formatMoney(totals(findRec('R2')).netVat)")
    open_view(page, "R2"); view_tab(page, "ref")
    rb = view_text(page)
    assert "2150 ภาษีขาย" in rb and "ภ.พ.30" in rb, "ref tab ไม่มี JE/ภ.พ.30"
    assert money in rb, f"ref tab (ภ.พ.30/JE) ไม่โชว์ VAT ที่ลดใหม่ ({money})"
    view_tab(page, "pdf")
    assert money in view_text(page), f"PDF ไม่โชว์ VAT ที่ลดใหม่ ({money})"
    return (f"10%: ฐาน 360,000→324,000 · VAT 25,200→22,680 · grand 346,680 · line-VAT engine คง 25,200 · "
            f"฿1,000: VAT ลด 65.42 · ภ.พ.30+JE+PDF โชว์ VAT ที่ลด ({money})")


def c_eb_cap(page):
    """[FN-09 · ส่วนลดท้ายบิล · Rule 1 จำกัด] end-bill เกินเพดาน → clamp/บล็อก · ยอดสุทธิห้ามติดลบ (grand ≥ 0)"""
    open_(page); open_create(page)
    after(page, "()=>pickInv('INV-2026-0141')")
    after(page, "()=>setReason('QTY')")
    after_amt = ev(page, "()=>totals(createWizard.data).after")
    # (ก) amount เกินยับ (99,999,999) → clamp ที่เพดาน · grand=0 (ไม่ติดลบ) · ebOver
    after(page, "()=>{createWizard.data.endbill={enabled:true,mode:'amount',value:99999999}; updateLineSummaryOnly();}")
    t = ev(page, "()=>totals(createWizard.data)")
    assert t["ebOver"] is True, "end-bill เกินเพดานแต่ ebOver=false"
    assert t["grand"] >= 0 and abs(t["grand"]) < 0.01, f"grand ต้อง = 0 (ไม่ติดลบ) เมื่อส่วนลดเกิน ({t['grand']})"
    assert abs(t["ebAmt"] - t["ebCap"]) < 0.01 and abs(t["ebCap"] - after_amt) < 0.01, f"ebAmt ต้อง clamp ที่เพดาน = after ({t})"
    # (ข) บล็อก submit — blockReason + submitGuard (บนใบ draft จริง)
    assert ev(page, "()=>DOC.blockReason(createWizard.data)").startswith("ส่วนลดท้ายบิลเกิน"), "blockReason ไม่บล็อกส่วนลดเกิน"
    # summary เรนเดอร์จริงมี hard-warn บอกเพดาน
    goto_step(page, 3)
    b = create_text(page)
    assert "ส่วนลดท้ายบิลเกินยอดที่ลดได้" in b and "สูงสุด" in b, "ไม่มี hard-warn ส่วนลดเกิน + เพดาน"
    # (ค) percent เกิน 100 (999%) → เพดานเดียวกัน · grand ไม่ติดลบ
    after(page, "()=>{createWizard.data.endbill={enabled:true,mode:'percent',value:999}; updateLineSummaryOnly();}")
    t2 = ev(page, "()=>totals(createWizard.data)")
    assert t2["ebOver"] is True and t2["grand"] >= 0 and abs(t2["grand"]) < 0.01, f"999% ต้อง clamp · grand=0 ({t2['grand']})"
    # (ง) resolveDoa (อ่าน grand) ยังทำงานหลัง cap (ไม่พังจาก grand=0)
    steps = ev(page, "()=>resolveDoa(createWizard.data).steps.length")
    assert steps >= 1, "resolveDoa พังหลัง cap (grand=0)"
    # (จ) submitGuard บนใบ draft จริง (R6) ที่ใส่ end-bill เกิน → บล็อก · openSubmitModal ไม่เปิด
    after(page, "()=>closeCreateDrawer()")
    after(page, "()=>{findRec('R6').endbill={enabled:true,mode:'amount',value:99999999};}")
    g = ev(page, "()=>DOC.submitGuard(findRec('R6'))")
    assert g.startswith("ส่วนลดท้ายบิลเกิน"), f"submitGuard ไม่บล็อกส่วนลดเกินบนใบ draft ({g})"
    after(page, "()=>openSubmitModal('R6')")
    assert not ev(page, "()=>!!document.querySelector('.modal-overlay')"), "openSubmitModal เปิด modal ทั้งที่ส่วนลดเกิน"
    assert ev(page, "()=>totals(findRec('R6')).grand") >= 0, "R6 grand ติดลบ"
    return (f"amount 99,999,999 + 999% → clamp ที่เพดาน ฿{after_amt:,.0f} · grand=0 (ไม่ติดลบ) · ebOver · "
            f"blockReason+submitGuard บล็อก · openSubmitModal ไม่เปิด · resolveDoa ยังทำงาน")


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
    ("E05b-CAP", c_cap_display, ["FN-05", "FN-08"]),
    ("E08b-CAP-QTY", c_cap_display_qty, ["FN-08"]),
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
    ("E18b-EB-VAT", c_eb_vat, ["FN-18", "FN-19"]),
    ("E09b-EB-CAP", c_eb_cap, ["FN-09", "FN-19"]),
    ("E90", c_fn90, ["FN-90"]),
    ("E91", c_fn91, ["FN-91"]),
    ("E92", c_fn92, ["FN-92"]),
    ("N-REFUND", c_neg_refund, []),
    ("N-CANCEL-APPROVED", c_neg_cancel_approved, []),
    ("N-SR-CRUD", c_neg_no_sr_crud, []),
    ("Z-MODAL", c_modal_z, []),
    ("C1-CANCEL-SENT", c_bypass_c1_cancel_sent, ["FN-15"]),
    ("C2-SEND-DRAFT", c_bypass_c2_send_draft, ["FN-16"]),
    ("C4-SUBMIT-APPROVED", c_bypass_c4_submit_approved, ["FN-11"]),
    ("E-ATT", c_attach_real, []),
]

ALL_FN = ["FN-01", "FN-02", "FN-03", "FN-04", "FN-05", "FN-06", "FN-07", "FN-08", "FN-09",
          "FN-10", "FN-11", "FN-12", "FN-13", "FN-14", "FN-15", "FN-16", "FN-17", "FN-18",
          "FN-19", "FN-90", "FN-91", "FN-92"]


def prove_by_revert():
    """C3.8 prove-by-revert: สำเนา scratch ที่ 'ถอด' DSP-08 fix rule ออก → assert ต้อง FAIL
    (พิสูจน์ว่าตัววัดจับ bug ได้จริง) · ไฟล์จริง (มี fix) → PASS. ไม่แตะไฟล์จริง."""
    src = HTML.read_text(encoding="utf-8")
    assert DSP08_FIX_RULE in src, "ไม่พบ DSP-08 fix rule ในไฟล์จริง (โครงเปลี่ยน — ตรวจ selector)"
    broken = src.replace(DSP08_FIX_RULE, ".modal-overlay > *:not(.backdrop) { position: relative; }", 1)
    assert broken != src, "revert ไม่เปลี่ยนอะไร"
    scratch = Path(tempfile.gettempdir()) / "F-ACC-CN_credit-note__DSP08-broken.html"
    scratch.write_text(broken, encoding="utf-8")

    out = {"broken_failed": None, "broken_detail": "", "real_passed": None, "real_detail": ""}
    with sync_playwright() as p:
        br = p.chromium.launch()
        # scratch (fix ถูกถอด) → assert ต้อง FAIL
        pg = br.new_page(viewport={"width": 1360, "height": 900})
        open_(pg, scratch.as_uri())
        after(pg, "()=>openSubmitModal('R6')")
        try:
            r = assert_modal_card_topmost(pg, note="scratch (fix removed)")
            out["broken_failed"] = False
            out["broken_detail"] = f"ไม่ FAIL (ok · hit={r.get('hit')} card z:{r.get('cardZ')})"
        except AssertionError as e:
            out["broken_failed"] = True
            out["broken_detail"] = str(e)[:150]
        pg.close()
        # real (fix อยู่) → assert ต้อง PASS
        pg2 = br.new_page(viewport={"width": 1360, "height": 900})
        open_(pg2, BASE)
        after(pg2, "()=>openSubmitModal('R6')")
        try:
            r = assert_modal_card_topmost(pg2, note="real (fixed)")
            out["real_passed"] = True
            out["real_detail"] = f"card z:{r['cardZ']} > backdrop z:{r['backdropZ']} · hit={r['hit']}"
        except AssertionError as e:
            out["real_passed"] = False
            out["real_detail"] = str(e)[:150]
        pg2.close()
        br.close()
    return out


def prove_by_revert_cap():
    """C3.8 prove-by-revert (CAP-DISPLAY): สำเนา scratch ที่ย้อน lineMeta กลับไปโชว์ room.qtyLeft
    → assert_line_cap_display_matches_enforced ต้อง FAIL (เลขที่โชว์ 7 ≠ จุดบล็อก 2) ·
    ไฟล์จริง (โชว์ l.max) → PASS. ไม่แตะไฟล์จริง."""
    src = HTML.read_text(encoding="utf-8")
    assert CAP_FIX_SNIPPET in src, "ไม่พบ CAP-DISPLAY fix ในไฟล์จริง (โครง lineMeta เปลี่ยน — ตรวจ snippet)"
    broken = src.replace(CAP_FIX_SNIPPET, CAP_BROKEN_SNIPPET, 1)
    assert broken != src, "revert ไม่เปลี่ยนอะไร"
    scratch = Path(tempfile.gettempdir()) / "F-ACC-CN_credit-note__CAP-broken.html"
    scratch.write_text(broken, encoding="utf-8")

    out = {"broken_failed": None, "broken_detail": "", "real_passed": None, "real_detail": ""}

    def _drive(pg):
        open_create(pg)
        after(pg, "()=>pickInv('INV-2026-0140')")
        after(pg, "()=>setReason('RET')")
        after(pg, "()=>pickSR('SR-2026-0016')")
        goto_step(pg, 3)
        return assert_line_cap_display_matches_enforced(
            pg, "updateLine(createWizard.data.lines[0].id,'qty',{v})",
            note="prove-by-revert", scope="#create-drawer-content")

    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width": 1360, "height": 900})
        open_(pg, scratch.as_uri())
        try:
            r = _drive(pg)
            out["broken_failed"] = False
            out["broken_detail"] = f"ไม่ FAIL (✘ โชว์ {r.get('cap')} · ตัววัดไม่จับ)"
        except AssertionError as e:
            out["broken_failed"] = True
            out["broken_detail"] = str(e)[:150]
        pg.close()

        pg2 = br.new_page(viewport={"width": 1360, "height": 900})
        open_(pg2, BASE)
        try:
            r = _drive(pg2)
            out["real_passed"] = True
            out["real_detail"] = f"โชว์ cap={r['cap']} · suffix(ตามใบรับคืน)={r['suffix']}"
        except AssertionError as e:
            out["real_passed"] = False
            out["real_detail"] = str(e)[:150]
        pg2.close()
        br.close()
    return out


def prove_by_revert_status():
    """C3.8 prove-by-revert (STATUS-GUARD): สำเนา scratch ที่ถอด FIX-02 guard ใน openSendCN ออก →
    assert_status_guard(send ใบ draft) ต้อง FAIL (ไม่มี warning toast / เปิด modal ส่งได้ = bypass ทะลุ) ·
    ไฟล์จริง (มี guard) → PASS. ไม่แตะไฟล์จริง."""
    src = HTML.read_text(encoding="utf-8")
    assert STATUS_GUARD_FIX in src, "ไม่พบ FIX-02 status guard ในไฟล์จริง (โครง openSendCN เปลี่ยน — ตรวจ snippet)"
    broken = src.replace(STATUS_GUARD_FIX, "", 1)
    assert broken != src, "revert ไม่เปลี่ยนอะไร"
    scratch = Path(tempfile.gettempdir()) / "F-ACC-CN_credit-note__STATUS-broken.html"
    scratch.write_text(broken, encoding="utf-8")

    args = ("openSendCN('R6')", "R6", "draft",
            "({s:findRec('R6').status,c:findRec('R6').code,sent:!!findRec('R6').sentAt})")
    out = {"broken_failed": None, "broken_detail": "", "real_passed": None, "real_detail": ""}
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width": 1360, "height": 900})
        open_(pg, scratch.as_uri())
        try:
            assert_status_guard(pg, *args, note="scratch (guard removed)")
            out["broken_failed"] = False
            out["broken_detail"] = "ไม่ FAIL (✘ ตัววัดไม่จับ — send ใบ draft ทะลุ guard)"
        except AssertionError as e:
            out["broken_failed"] = True
            out["broken_detail"] = str(e)[:150]
        pg.close()

        pg2 = br.new_page(viewport={"width": 1360, "height": 900})
        open_(pg2, BASE)
        try:
            r = assert_status_guard(pg2, *args, note="real (fixed)")
            out["real_passed"] = True
            out["real_detail"] = f"block · toast='{r['toast'][:40]}'"
        except AssertionError as e:
            out["real_passed"] = False
            out["real_detail"] = str(e)[:150]
        pg2.close()
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
    print("── FN coverage (22) ──")
    for c in ALL_FN:
        mark = "PASS" if covered.get(c) else ("FAIL" if c in have_case else "MISSING")
        if mark != "PASS":
            print(f"  {c}: {mark}")
    if missing:
        print("  ! FN ที่ไม่มีเคส:", ", ".join(missing))
    if failed_fn:
        print("  ! FN ที่มีเคสแต่ยังตก:", ", ".join(failed_fn))

    print()
    print("── C3.8 · DSP-08 prove-by-revert ──")
    try:
        pv = prove_by_revert()
        print(f"  scratch (fix ถอด) : {'FAIL (ตัววัดจับ bug ได้ ✔)' if pv['broken_failed'] else 'ไม่ FAIL (✘ ตัววัดไม่จับ)'} — {pv['broken_detail']}")
        print(f"  real   (fix อยู่)  : {'PASS ✔' if pv['real_passed'] else 'FAIL ✘'} — {pv['real_detail']}")
        revert_ok = bool(pv["broken_failed"]) and bool(pv["real_passed"])
    except Exception as e:
        print(f"  prove-by-revert ERROR: {type(e).__name__}: {e}")
        revert_ok = False

    print()
    print("── C3.8 · CAP-DISPLAY prove-by-revert ──")
    try:
        pc = prove_by_revert_cap()
        print(f"  scratch (โชว์ room) : {'FAIL (ตัววัดจับ bug ได้ ✔)' if pc['broken_failed'] else 'ไม่ FAIL (✘ ตัววัดไม่จับ)'} — {pc['broken_detail']}")
        print(f"  real   (โชว์ l.max) : {'PASS ✔' if pc['real_passed'] else 'FAIL ✘'} — {pc['real_detail']}")
        revert_cap_ok = bool(pc["broken_failed"]) and bool(pc["real_passed"])
    except Exception as e:
        print(f"  prove-by-revert (cap) ERROR: {type(e).__name__}: {e}")
        revert_cap_ok = False

    print()
    print("── C3.8 · STATUS-GUARD prove-by-revert ──")
    try:
        ps = prove_by_revert_status()
        print(f"  scratch (guard ถอด) : {'FAIL (ตัววัดจับ bypass ได้ ✔)' if ps['broken_failed'] else 'ไม่ FAIL (✘ ตัววัดไม่จับ)'} — {ps['broken_detail']}")
        print(f"  real   (guard อยู่)  : {'PASS ✔' if ps['real_passed'] else 'FAIL ✘'} — {ps['real_detail']}")
        revert_status_ok = bool(ps["broken_failed"]) and bool(ps["real_passed"])
    except Exception as e:
        print(f"  prove-by-revert (status) ERROR: {type(e).__name__}: {e}")
        revert_status_ok = False

    print()
    print(f"FN ครอบ {len(passed_fn)}/22 · เคสรวม {total} · ผ่าน {ok}/{total}")
    sys.exit(0 if ok == total and len(passed_fn) == 22 and revert_ok and revert_cap_ok
             and revert_status_ok and not suite.console_errors else 1)


if __name__ == "__main__":
    main()
