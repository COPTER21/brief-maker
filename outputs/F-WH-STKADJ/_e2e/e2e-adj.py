#!/usr/bin/env python3
"""E2E · F-WH-STKADJ · ใบปรับยอดสต๊อก (Stock Adjustment) — WF-01 Step 5 (ตัวหนัก)

รันไทม์ตัวเดียวที่ต้องพิสูจน์ COMPLETENESS: ทุก FN ใน FUNCTION_CHECKLIST (55 FN) มีเคส ≥1
+ หมวด 7 negatives (FN-32/35/36/46/47/48/49 · และ FN-45 append-only) = เคสเชิงลบที่ "เรนเดอร์จริง
แล้ว assert ว่าไม่โผล่บน DOM" (ไม่ใช่ grep source).

ยึด helper ของ uikit เท่านั้น (ready/settle/after) — ไม่มี wait_for_timeout, ไม่เขียนตัวตรวจ UI
generic ใหม่. ขับหน้าจอผ่าน controller function จริงของไฟล์ (comboPick / wizardNext / confirmApprove /
doPost / doReverse / confirmSubmit ฯลฯ) + real DOM แล้ว assert ทั้ง data model และสิ่งที่เรนเดอร์.
reload หน้าใหม่ต่อเคส → mock DOCS/DOC_SEQ reset = เคสอิสระต่อกัน.

หมายเหตุตัววัด (บันทึกความจริง — ไม่แกล้งเขียว):
  · combobox/drawer/modal ของฟีเจอร์นี้ใช้ระบบเอง (comboPick · .drawer-panel · .overlay-wrap.on ·
    .modal-overlay/.modal-card · #ss-combo-pop) — ไม่ใช่ .drawer/.modal-backdrop/search-select ของ
    BASE-KIT — helper ที่ผูก selector BASE-KIT (assert_combobox_closes_after_select /
    assert_overlay_cleared_after_close / JS_MODAL_UNDER_DRAWER) ใช้ตรงไม่ได้ จึงขับ controller จริง
    แล้ว assert state+DOM ของฟีเจอร์เอง.
  · การตั้ง state ตรง (เช่น createWizard.data.lines=[...] · d.status='approved' · l.curSys=...) คือ
    "การขับให้ถึง state" ที่ต้องทดสอบ — assertion ทุกจุดอ่านผลจาก computed/DOM ที่ render จริง.

รัน: PYTHONIOENCODING=utf-8 .claude/venv/Scripts/python.exe \
       outputs/F-WH-STKADJ/_e2e/e2e-adj.py outputs/F-WH-STKADJ/F-WH-STKADJ.html
"""
from pathlib import Path
import sys
import json
import os
import tempfile

# ไฟล์หลักฐานจริงชั่วคราวสำหรับทดสอบ upload (<input type=file>) — prototype อ่าน filename/size ฝั่ง client
_TMP_ATTACH = os.path.join(tempfile.gettempdir(), "stkadj_evidence.pdf")
if not os.path.exists(_TMP_ATTACH):
    open(_TMP_ATTACH, "wb").write(b"%PDF-1.4 stkadj test evidence\n")

from playwright.sync_api import sync_playwright

OUTPUTS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(OUTPUTS / "_SHARED" / "_e2e"))
from uikit import (  # noqa: E402
    Suite, ready, settle as shared_settle, after as shared_after,
    assert_text_absent, assert_no_garbage_text, assert_no_native_dialog,
    assert_icon_inside_input, assert_pop_above_modal, assert_no_scroll_lock_leak,
)

HTML = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parents[1] / "F-WH-STKADJ.html").resolve()
BASE = HTML.as_uri()

suite = Suite("F-WH-STKADJ · ใบปรับยอดสต๊อก")

# dialog policy — confirm() ใน onChangeAdjType / comboPick(wiz-wh) : default dismiss(false),
# เปิด accept เฉพาะเคสที่ต้องการยืนยันล้างบรรทัด (FN-09)
_dlg = {"accept": False}


def ev(page, js):
    return page.evaluate(js)


def after(page, js, timeout=2500):
    return shared_after(page, js, timeout=timeout)


def settle(page, timeout=2000):
    shared_settle(page, timeout=timeout)


def toast(page):
    return ev(page, "()=>{const r=document.getElementById('ss-toast-root');if(!r)return '';"
                     "const t=r.querySelectorAll('.toast');return t.length?t[t.length-1].textContent:'';}")


def open_(page):
    ready(page, BASE, timeout=9000)
    page.wait_for_function(
        "()=>{const e=document.getElementById('ss-page');return e&&e.innerHTML.trim().length>0;}",
        timeout=9000)


def open_create(page):
    after(page, "()=>openCreateDrawer(null)")
    page.wait_for_function("()=>document.getElementById('ss-create-content')&&createWizard.data", timeout=4000)


def open_view(page, doc_id):
    after(page, "()=>openViewDrawer('%s')" % doc_id)
    page.wait_for_function("()=>document.getElementById('ss-view-content')", timeout=4000)


def view_tab(page, tab):
    after(page, "()=>{viewState.tab='%s';renderViewDrawer();}" % tab)


def goto_step(page, n):
    after(page, "()=>{createWizard.step=%d;renderCreateDrawer();}" % n)


def line_id(page, i):
    return ev(page, "()=>createWizard.data.lines[%d].id" % i)


def pick(page, key, val):
    after(page, "()=>comboPick(%s,%s)" % (json.dumps(key), json.dumps(val)))


def set_qty(page, lid, field, val):
    after(page, "()=>updateLineNum('%s','%s',%s)" % (lid, field, json.dumps(str(val))))


def wnext(page):
    after(page, "()=>wizardNext()")


def _mkline(o):
    return "mkLine(%s)" % json.dumps(o, ensure_ascii=False)


def set_lines(page, lines, adjType="general", mode="correct"):
    """ฉีดบรรทัดเข้า wizard โดยใช้ mkLine ของไฟล์ (คง id/โครงสร้างจริง) แล้ว render"""
    js_lines = ",".join(_mkline(o) for o in lines)
    after(page, "()=>{createWizard.data.adjType=%s;createWizard.data.gridMode=%s;"
                "createWizard.data.lines=[%s];renderCreateDrawer();}"
          % (json.dumps(adjType), json.dumps(mode), js_lines))


def page_text(page):
    return ev(page, "()=>document.getElementById('ss-page').textContent")


def create_text(page):
    return ev(page, "()=>(document.getElementById('ss-create-content')||{}).textContent||''")


def view_text(page):
    return ev(page, "()=>(document.getElementById('ss-view-content')||{}).textContent||''")


def modal_text(page):
    return ev(page, "()=>{const m=document.getElementById('ss-modal');return m?m.textContent:'';}")


# ═══════════════════════════ หมวด 1 · สร้างใบ + เลือก bin ═══════════════════════════

def c_fn01(page):
    """[FN-01 · S-18 · BR-12] ประเภท=ปรับยอดกักกัน → bin picker เหลือเฉพาะ quarantine (QA-*)"""
    open_(page); open_create(page)
    set_lines(page, [{}], adjType="quarantine")
    lid = line_id(page, 0)
    items = ev(page, "()=>comboItemsFor('line-bin-%s','').map(x=>x.val)" % lid)
    types = ev(page, "()=>comboItemsFor('line-bin-%s','').map(x=>(BIN_BY[x.val]||{}).type)" % lid)
    assert items, "quarantine picker ว่างเปล่า"
    assert all(t == "quarantine" for t in types), f"picker กักกันมี bin ประเภทอื่นปน: {list(zip(items,types))}"
    assert "QA-01" in items, "ไม่พบ QA-01 ใน picker กักกัน"
    assert not any(str(v).startswith(("A-", "B-", "C-", "ST-", "DM-", "TR-")) for v in items), \
        f"picker กักกันหลุด bin ประเภทอื่น: {items}"
    return f"quarantine → picker เหลือเฉพาะ QA-* ({items})"


def c_fn02(page):
    """[FN-02 · S-19 · BR-12] ประเภท=ตัดจำหน่ายของเสีย → bin picker เหลือเฉพาะ damage (DM-*)"""
    open_(page); open_create(page)
    set_lines(page, [{}], adjType="damage")
    lid = line_id(page, 0)
    items = ev(page, "()=>comboItemsFor('line-bin-%s','').map(x=>x.val)" % lid)
    types = ev(page, "()=>comboItemsFor('line-bin-%s','').map(x=>(BIN_BY[x.val]||{}).type)" % lid)
    assert items and all(t == "damage" for t in types), f"picker ของเสียมี bin ประเภทอื่นปน: {list(zip(items,types))}"
    assert "DM-01" in items, "ไม่พบ DM-01 ใน picker ของเสีย"
    return f"damage → picker เหลือเฉพาะ DM-* ({items})"


def c_fn03(page):
    """[FN-03 · S-14 · BR-14] bin ล็อก (B-03-02-B) ค้นเจอแต่เลือกไม่ได้ + บอกเหตุผลที่ล็อก"""
    open_(page); open_create(page)
    set_lines(page, [{}], adjType="general")
    lid = line_id(page, 0)
    locked = ev(page, "()=>comboItemsFor('line-bin-%s','').filter(x=>x.val==='B-03-02-B')[0]||null" % lid)
    assert locked, "bin ล็อก B-03-02-B ไม่ปรากฏใน picker (ต้อง 'ค้นเจอ')"
    assert locked["disabled"] is True, "bin ล็อกต้อง disabled (เลือกไม่ได้)"
    assert "ล็อก" in (locked.get("disReason") or "") or "ตรวจซ่อม" in (locked.get("disReason") or ""), \
        f"bin ล็อกไม่บอกเหตุผล: {locked}"
    # เรนเดอร์ pop จริง (step 2 มี input line-bin) → ปุ่มของ bin ล็อกต้องเป็น disabled button
    goto_step(page, 2)
    after(page, "()=>comboOpen('line-bin-%s','')" % lid)
    dis = ev(page, "()=>{const p=document.getElementById('ss-combo-pop');if(!p)return -1;"
                   "return [].slice.call(p.querySelectorAll('button')).filter(b=>b.disabled&&/B-03-02-B/.test(b.textContent)).length;}")
    assert dis == 1, f"ปุ่ม bin ล็อกในเมนูไม่ได้ disabled (พบ {dis})"
    return "bin ล็อก B-03-02-B ค้นเจอ · disabled · แสดงเหตุผล 'ตรวจซ่อมชั้นวาง'"


def c_fn09(page):
    """[FN-09 · S-23 · BR-04] เปลี่ยนคลังทั้งที่มีบรรทัด → ยืนยันก่อนล้างบรรทัด (1 ใบ = 1 คลัง)"""
    open_(page); open_create(page)
    set_lines(page, [{"bin": "A-01-01-A", "item": "STA-0031", "unit": "รีม", "sysQty": 100, "correctQty": 120}])
    # (ก) เปลี่ยนคลังมีบรรทัด → ต้องเด้ง modal ของแอป (ห้าม native confirm) → กดยกเลิก → คลัง/บรรทัดไม่เปลี่ยน
    pick(page, "wiz-wh", "WH-CNX-01")
    assert ev(page, "()=>!!document.getElementById('ss-confirm-cancel')"), \
        "เปลี่ยนคลังมีบรรทัดแต่ไม่เด้ง modal ยืนยันของแอป (ห้ามใช้ native confirm)"
    after(page, "()=>document.getElementById('ss-confirm-cancel').click()")
    assert ev(page, "()=>createWizard.data.wh") == "WH-BKK-01", "กดยกเลิกแต่คลังเปลี่ยน"
    assert ev(page, "()=>createWizard.data.lines[0].bin") == "A-01-01-A", "กดยกเลิกแต่ bin ถูกล้าง"
    # (ข) เปลี่ยนคลังอีกครั้ง → กดยืนยัน → คลังเปลี่ยน + bin ในบรรทัดถูกล้าง
    pick(page, "wiz-wh", "WH-CNX-01")
    after(page, "()=>document.getElementById('ss-confirm-ok').click()")
    assert ev(page, "()=>createWizard.data.wh") == "WH-CNX-01", "ยืนยันแล้วคลังไม่เปลี่ยน"
    assert ev(page, "()=>createWizard.data.lines[0].bin") == "", "ยืนยันเปลี่ยนคลังแล้ว bin ไม่ถูกล้าง (1 ใบ=1 คลัง)"
    # C3.8: ตลอด flow ยืนยันล้าง bin ต้องไม่มี native confirm/alert/prompt เลย (uikit trap)
    assert_no_native_dialog(page, note="FN-09 เปลี่ยนคลัง/ประเภท ต้องใช้ modal ของแอป")
    return "เปลี่ยนคลังมีบรรทัด: เด้ง modal ของแอป (ไม่ใช่ native confirm) · ยกเลิก=คงเดิม · ยืนยัน=เปลี่ยน+ล้าง bin"


# ═══════════════════════════ หมวด 2 · line editor ═══════════════════════════

def c_fn04(page):
    """[FN-04 · S-01 §3.2] bin+สินค้า → ยอดระบบขึ้นเอง · correct>sys → ผลต่าง + (ชิปเขียว plus)"""
    open_(page); open_create(page); goto_step(page, 2)
    lid = line_id(page, 0)
    pick(page, "line-bin-%s" % lid, "A-01-01-A")
    pick(page, "line-item-%s" % lid, "STA-0031")
    sysq = ev(page, "()=>createWizard.data.lines[0].sysQty")
    assert sysq > 0, "เลือก bin+สินค้าแล้วยอดระบบไม่ขึ้นเอง"
    set_qty(page, lid, "correctQty", sysq + 12)
    df = ev(page, "()=>lineDiff(createWizard.data.lines[0])")
    assert df == 12, f"ผลต่างไม่ถูก (คาด +12 ได้ {df})"
    cls = ev(page, "()=>{const c=document.querySelector('#diff-%s .chip-diff');return c?c.className:'';}" % lid)
    assert "plus" in cls, f"ผลต่างบวกแต่ชิปไม่ใช่สีเขียว plus (class='{cls}')"
    txt = ev(page, "()=>(document.querySelector('#diff-%s .chip-diff')||{}).textContent||''" % lid)
    assert "+" in txt, f"ชิปผลต่างบวกไม่ขึ้นเครื่องหมาย + (txt='{txt}')"
    return f"ยอดระบบขึ้นเอง ({sysq}) · correct {sysq+12} → ผลต่าง +12 · ชิปเขียว plus"


def c_fn05(page):
    """[FN-05 · S-02 §3.2] correct<sys → ผลต่าง − (ชิปแดง minus)"""
    open_(page); open_create(page); goto_step(page, 2)
    lid = line_id(page, 0)
    pick(page, "line-bin-%s" % lid, "A-01-01-A")
    pick(page, "line-item-%s" % lid, "STA-0031")
    sysq = ev(page, "()=>createWizard.data.lines[0].sysQty")
    set_qty(page, lid, "correctQty", sysq - 7)
    df = ev(page, "()=>lineDiff(createWizard.data.lines[0])")
    assert df == -7, f"ผลต่างไม่ถูก (คาด -7 ได้ {df})"
    cls = ev(page, "()=>{const c=document.querySelector('#diff-%s .chip-diff');return c?c.className:'';}" % lid)
    assert "minus" in cls, f"ผลต่างลบแต่ชิปไม่ใช่สีแดง minus (class='{cls}')"
    return f"correct {sysq-7} < sys {sysq} → ผลต่าง -7 · ชิปแดง minus"


def c_fn06(page):
    """[FN-06 · S-01 §3.3] มูลค่าที่ปรับ = ผลต่าง × ต้นทุนอ้างอิง ถูกต้องทุกบรรทัด"""
    open_(page); open_create(page); goto_step(page, 2)
    lid = line_id(page, 0)
    pick(page, "line-bin-%s" % lid, "A-01-01-A")
    pick(page, "line-item-%s" % lid, "STA-0031")   # cost 115
    sysq = ev(page, "()=>createWizard.data.lines[0].sysQty")
    set_qty(page, lid, "correctQty", sysq + 4)
    cost = ev(page, "()=>lineRefCost(createWizard.data.lines[0])")
    val = ev(page, "()=>lineValue(createWizard.data.lines[0])")
    df = ev(page, "()=>lineDiff(createWizard.data.lines[0])")
    assert cost == 115.0, f"ต้นทุนอ้างอิง STA-0031 ต้อง 115 (ได้ {cost})"
    assert val == df * cost == 4 * 115, f"มูลค่า ≠ ผลต่าง×ต้นทุน (val={val} · {df}×{cost})"
    domval = ev(page, "()=>(document.getElementById('val-%s')||{}).textContent||''" % lid)
    assert "460" in domval, f"มูลค่าบนจอไม่ตรง (คาด 460, ได้ '{domval}')"
    return f"มูลค่า = {df} × ฿{cost} = ฿{val} (แสดงบนจอ '{domval}')"


def c_fn07(page):
    """[FN-07 · S-03 §3.2] สลับโหมด (ระบุยอดที่ถูกต้อง ↔ ระบุจำนวนที่ปรับ) แปลงกลับไปมาถูกต้อง"""
    open_(page); open_create(page)
    lid = line_id(page, 0)
    pick(page, "line-bin-%s" % lid, "A-01-01-A")
    pick(page, "line-item-%s" % lid, "STA-0031")
    sysq = ev(page, "()=>createWizard.data.lines[0].sysQty")
    set_qty(page, lid, "correctQty", sysq + 5)
    assert ev(page, "()=>lineDiff(createWizard.data.lines[0])") == 5
    # correct → delta : deltaQty ต้องกลายเป็น +5
    after(page, "()=>setGridMode('delta')")
    l = ev(page, "()=>createWizard.data.lines[0]")
    assert l["mode"] == "delta" and l["deltaQty"] == 5, f"correct→delta แปลงผิด: {l}"
    assert ev(page, "()=>lineDiff(createWizard.data.lines[0])") == 5, "ผลต่างเปลี่ยนหลังสลับโหมด (ต้องคงที่)"
    # delta → correct : correctQty ต้องกลับเป็น sys+5
    after(page, "()=>setGridMode('correct')")
    l = ev(page, "()=>createWizard.data.lines[0]")
    assert l["mode"] == "correct" and l["correctQty"] == sysq + 5, f"delta→correct แปลงผิด: {l}"
    assert ev(page, "()=>lineDiff(createWizard.data.lines[0])") == 5, "ผลต่างไม่คงที่หลังแปลงกลับ"
    return f"correct(ยอด {sysq+5}) ↔ delta(+5) แปลงกลับไปมา ผลต่าง=+5 คงที่"


def c_fn08(page):
    """[FN-08 · S-03 · BR-09] totals แยก Σ|มูลค่า| (ฐาน DOA) กับ มูลค่าสุทธิ ในใบผสม +/−"""
    open_(page); open_create(page)
    set_lines(page, [
        {"bin": "A-01-01-A", "item": "STA-0031", "unit": "รีม", "sysQty": 100, "correctQty": 120},   # +20×115
        {"bin": "A-02-03-B", "item": "STA-0044", "unit": "เล่ม", "sysQty": 90, "correctQty": 75},     # -15×85
    ])
    goto_step(page, 2)
    net = ev(page, "()=>createWizard.data.lines.reduce((s,l)=>s+lineValue(l),0)")
    abs_ = ev(page, "()=>createWizard.data.lines.reduce((s,l)=>s+Math.abs(lineValue(l)),0)")
    assert net == 20 * 115 - 15 * 85, f"net ผิด: {net}"
    assert abs_ == 20 * 115 + 15 * 85, f"abs ผิด: {abs_}"
    assert abs_ > abs(net), "ใบผสม +/− แต่ Σ|มูลค่า| ไม่มากกว่า |สุทธิ| (แยกไม่ได้)"
    body = ev(page, "()=>document.getElementById('ss-wiz-totals').textContent")
    assert "สุทธิ" in body and "ค่าสัมบูรณ์" in body, "totals ไม่แสดงทั้งสุทธิและค่าสัมบูรณ์แยกกัน"
    return f"ผสม +/−: Σ|มูลค่า|=฿{abs_} (ฐาน DOA) แยกจาก สุทธิ=฿{net} ชัดเจน"


def c_fn10(page):
    """[FN-10 · S-01,S-02 · BR-01] คู่ (bin, สินค้า) ซ้ำ → เตือน + บล็อกก้าวต่อ"""
    open_(page); open_create(page)
    set_lines(page, [
        {"bin": "A-01-01-A", "item": "STA-0031", "unit": "รีม", "sysQty": 100, "correctQty": 120},
        {"bin": "A-01-01-A", "item": "STA-0031", "unit": "รีม", "sysQty": 100, "correctQty": 130},
    ])
    goto_step(page, 2)
    wnext(page)
    assert "ซ้ำ" in toast(page), f"คู่ซ้ำไม่เตือน (toast='{toast(page)}')"
    assert ev(page, "()=>createWizard.step") == 2, "คู่ (bin,สินค้า) ซ้ำแต่ยังก้าวต่อได้ (ต้องบล็อก)"
    return "คู่ (A-01-01-A, STA-0031) ซ้ำ → เตือน 'ซ้ำ' + บล็อกที่ step 2"


def c_fn11(page):
    """[FN-11 · S-04 · BR-02] correct=sys (ผลต่าง=0) → ก้าวต่อ/บันทึกไม่ได้ + บอกวิธีแก้"""
    open_(page); open_create(page)
    set_lines(page, [{"bin": "A-01-01-A", "item": "STA-0031", "unit": "รีม", "sysQty": 100, "correctQty": 100}])
    goto_step(page, 2)
    wnext(page)
    t = toast(page)
    assert "ผลต่าง = 0" in t or "ผลต่าง = 0" in t.replace(" ", " "), f"ผลต่าง=0 ไม่เตือน (toast='{t}')"
    assert "ลบบรรทัด" in t or "แก้ยอด" in t, f"ผลต่าง=0 ไม่บอกวิธีแก้ (toast='{t}')"
    assert ev(page, "()=>createWizard.step") == 2, "ผลต่าง=0 แต่ยังก้าวต่อได้"
    return "ผลต่าง=0 → บล็อก + บอกวิธีแก้ (ลบบรรทัด/แก้ยอด · BR-02)"


def c_fn12(page):
    """[FN-12 · S-05 · BR-03] ปรับลดจนติดลบ → บล็อก + แสดงยอดคงเหลือจริง"""
    open_(page); open_create(page)
    set_lines(page, [{"bin": "A-01-01-A", "item": "STA-0031", "unit": "รีม", "sysQty": 100,
                      "mode": "delta", "deltaQty": -200}], mode="delta")
    goto_step(page, 2)
    wnext(page)
    t = toast(page)
    assert "ติดลบ" in t, f"ยอดหลังปรับติดลบไม่บล็อก (toast='{t}')"
    assert "100" in t, f"ไม่แสดงยอดคงเหลือจริง (toast='{t}')"
    assert ev(page, "()=>createWizard.step") == 2, "ยอดติดลบแต่ยังก้าวต่อได้"
    # เรนเดอร์: ป้ายเตือนใต้บรรทัดต้องขึ้น
    assert "ติดลบ" in create_text(page), "ไม่มีป้ายเตือนติดลบใต้บรรทัดบนจอ"
    return "delta -200 บน sys 100 → ยอดหลังปรับติดลบ · บล็อก + แสดงคงเหลือ 100 (BR-03)"


def c_fn13(page):
    """[FN-13 · §3.2 · G-01] ต้นทุนอ้างอิงมีป้าย mock (valuation engine ยังไม่มา) + แก้ไม่ได้"""
    open_(page); open_create(page)
    lid = line_id(page, 0)
    pick(page, "line-bin-%s" % lid, "A-01-01-A")
    pick(page, "line-item-%s" % lid, "STA-0031")
    goto_step(page, 2)
    # ช่องต้นทุนอ้างอิงในแถวเป็น readonly (แก้ไม่ได้)
    ro = ev(page, "()=>{const rows=document.querySelectorAll('#ss-create-content .line-tbl tbody tr');"
                  "let ok=true;rows.forEach(tr=>{const c=tr.querySelectorAll('td')[7];"
                  "const inp=c&&c.querySelector('input');if(inp&&!inp.readOnly)ok=false;});return ok;}")
    assert ro, "ช่องต้นทุนอ้างอิงแก้ไขได้ (ต้อง readonly)"
    body = create_text(page)
    assert "valuation engine" in body and ("mock" in body.lower() or "Item Master" in body), \
        "ไม่มีป้ายบอกว่าต้นทุนมาจาก mock / valuation engine (W5)"
    return "ต้นทุนอ้างอิง readonly + ป้าย 'Item Master (mock) · FWD-WIRE: valuation engine'"


# ═══════════════════════════ หมวด 3 · เหตุผล + หลักฐาน ═══════════════════════════

def c_fn18(page):
    """[FN-18 · BR-06] บรรทัดยังไม่เลือกเหตุผล → ส่งอนุมัติไม่ได้ + ชี้บรรทัดที่ขาด"""
    open_(page); open_create(page)
    set_lines(page, [{"bin": "A-01-01-A", "item": "STA-0031", "unit": "รีม", "sysQty": 100, "correctQty": 120, "reason": ""}])
    goto_step(page, 3)
    wnext(page)
    t = toast(page)
    assert "ยังไม่เลือกเหตุผล" in t and "A-01-01-A" in t, f"เหตุผลว่างไม่บล็อก/ไม่ชี้บรรทัด (toast='{t}')"
    assert ev(page, "()=>createWizard.step") == 3, "เหตุผลว่างแต่ยังก้าวต่อได้"
    return "บรรทัดไม่มีเหตุผล → บล็อก + ชี้บรรทัด A-01-01-A (BR-06)"


def c_fn37(page):
    """[FN-37 · BR-07] dropdown เหตุผลกรองตามทิศผลต่าง (บรรทัด + ไม่เห็นเหตุผลกลุ่มลด)"""
    open_(page); open_create(page)
    set_lines(page, [{"bin": "A-01-01-A", "item": "STA-0031", "unit": "รีม", "sysQty": 100, "correctQty": 120}])  # +20
    lid = line_id(page, 0)
    vals = ev(page, "()=>comboItemsFor('line-reason-%s','').map(x=>x.val)" % lid)
    minus_only = ["RS-03", "RS-04", "RS-05", "RS-06"]   # dir minus
    assert not any(m in vals for m in minus_only), f"บรรทัด + แต่ยังเห็นเหตุผลกลุ่มลด: {vals}"
    assert "RS-01" in vals and "RS-02" in vals, f"บรรทัด + ไม่เห็นเหตุผลกลุ่มเพิ่ม: {vals}"
    # ทางกลับกัน: บรรทัด − ต้องไม่เห็นกลุ่มเพิ่ม (RS-01/RS-02)
    set_qty(page, lid, "correctQty", 80)   # -20
    vals2 = ev(page, "()=>comboItemsFor('line-reason-%s','').map(x=>x.val)" % lid)
    assert "RS-01" not in vals2 and "RS-02" not in vals2, f"บรรทัด − แต่ยังเห็นเหตุผลกลุ่มเพิ่ม: {vals2}"
    return f"เหตุผลกรองตามทิศ: บรรทัด + → {vals} (ไม่มีกลุ่มลด) · บรรทัด − → ไม่มี RS-01/02"


def c_fn40(page):
    """[FN-40 · BR-06] เหตุผล 'อื่น ๆ' (RS-99) → บังคับพิมพ์คำอธิบายเพิ่มก่อนไปต่อ"""
    open_(page); open_create(page)
    set_lines(page, [{"bin": "A-01-01-A", "item": "STA-0031", "unit": "รีม", "sysQty": 100, "correctQty": 120,
                      "reason": "RS-99", "reasonNote": ""}])
    goto_step(page, 3)
    # ช่องคำอธิบายเพิ่มต้องเป็น required (มี * และ input ไม่ disabled)
    need = ev(page, "()=>{const n=document.getElementById('note-%s');if(!n)return false;"
                    "const inp=n.querySelector('input');return inp&&!inp.disabled;}" % line_id(page, 0))
    assert need, "เหตุผล 'อื่น ๆ' แต่ช่องคำอธิบายเพิ่มไม่เปิดให้กรอก (ต้องบังคับ)"
    wnext(page)
    t = toast(page)
    assert "คำอธิบายเพิ่ม" in t, f"'อื่น ๆ' ไม่บังคับคำอธิบาย (toast='{t}')"
    assert ev(page, "()=>createWizard.step") == 3, "'อื่น ๆ' ไม่มีคำอธิบายแต่ยังก้าวต่อได้"
    # เติมคำอธิบาย → ผ่าน
    after(page, "()=>setLineNote('%s','ปรับตามผลตรวจซ้ำ')" % line_id(page, 0))
    wnext(page)
    assert ev(page, "()=>createWizard.step") == 4, "เติมคำอธิบายแล้วยังก้าวต่อไม่ได้"
    return "RS-99 (อื่น ๆ) ไม่มีคำอธิบาย → บล็อก · เติมแล้ว → ผ่านไป step 4"


def c_fn41(page):
    """[FN-41 · §3.1] เหตุผลรวมหัวใบ → เติมทุกบรรทัดที่ว่าง แต่ยังแก้รายบรรทัดได้"""
    open_(page); open_create(page)
    set_lines(page, [
        {"bin": "A-01-01-A", "item": "STA-0031", "unit": "รีม", "sysQty": 100, "correctQty": 120, "reason": "RS-01"},
        {"bin": "B-01-01-A", "item": "PIP-0322", "unit": "ตัว", "sysQty": 300, "correctQty": 360, "reason": ""},
    ])
    after(page, "()=>{createWizard.data.headerReason='RS-02';applyHeaderReason();}")
    r0 = ev(page, "()=>createWizard.data.lines[0].reason")
    r1 = ev(page, "()=>createWizard.data.lines[1].reason")
    assert r0 == "RS-01", "เหตุผลรวมไปทับบรรทัดที่มีเหตุผลอยู่แล้ว (ต้องเติมเฉพาะที่ว่าง)"
    assert r1 == "RS-02", "เหตุผลรวมไม่เติมบรรทัดที่ว่าง"
    # ยังแก้รายบรรทัดได้
    pick(page, "line-reason-%s" % line_id(page, 1), "RS-01")
    assert ev(page, "()=>createWizard.data.lines[1].reason") == "RS-01", "แก้เหตุผลรายบรรทัดหลังเติมไม่ได้"
    return "เหตุผลรวม RS-02 เติมเฉพาะบรรทัดว่าง (บรรทัดมีเหตุผลคงเดิม) · แก้รายบรรทัดได้"


def c_fn33(page):
    """[FN-33 · S-21 §6.1] แนบไฟล์หลักฐานได้ + ไฟล์โผล่ในส่วน 'เอกสารแนบ' ที่หน้า landing"""
    open_(page)
    # (ก) landing มีส่วน Document Center รวมไฟล์แนบทุกใบ (seed มีไฟล์จริง)
    pt = page_text(page)
    assert "เอกสารแนบ" in pt and "Document Center" in pt, "landing ไม่มีส่วนเอกสารแนบ (Document Center)"
    assert "ใบตรวจนับ-Q3.pdf" in pt, "ไฟล์แนบของ seed ไม่โผล่ในส่วนเอกสารแนบที่ landing"
    # (ข) แนบไฟล์จริงผ่าน <input type=file> (upload จริง) ใน step 3 → attachments เพิ่ม
    open_create(page); goto_step(page, 3)
    n0 = ev(page, "()=>createWizard.data.attachments.length")
    page.set_input_files("#ss-attach-input", _TMP_ATTACH)
    settle(page)
    assert ev(page, "()=>createWizard.data.attachments.length") == n0 + 1, "แนบไฟล์จริงแล้ว attachments ไม่เพิ่ม"
    fname = ev(page, "()=>createWizard.data.attachments.slice(-1)[0].name")
    assert fname == os.path.basename(_TMP_ATTACH), f"ชื่อไฟล์ที่แนบไม่ตรงไฟล์จริง (got {fname})"
    return "แนบไฟล์จริงผ่าน input type=file (attachments +1, ชื่อไฟล์จริง) · โผล่ใน Document Center ที่ landing"


def c_fn51(page):
    """[FN-51 · S-19 · BR-23] ประเภท 'ตัดจำหน่ายของเสีย' ยังไม่แนบไฟล์ → ส่งอนุมัติไม่ได้"""
    open_(page); open_create(page)
    set_lines(page, [{"bin": "DM-01", "item": "CON-0210", "unit": "กล่อง", "sysQty": 85, "correctQty": 70,
                      "reason": "RS-06", "reasonNote": "ตัดจำหน่ายตามใบบันทึก"}], adjType="damage")
    goto_step(page, 3)
    assert ev(page, "()=>createWizard.data.attachments.length") == 0, "seed มีไฟล์แนบแล้ว — เคสนี้ต้องเริ่มจากไม่มี"
    wnext(page)
    t = toast(page)
    assert "แนบหลักฐาน" in t, f"ของเสียไม่แนบไฟล์แต่ไม่บล็อก (toast='{t}')"
    assert ev(page, "()=>createWizard.step") == 3, "ของเสียไม่แนบไฟล์แต่ยังก้าวต่อได้"
    page.set_input_files("#ss-attach-input", _TMP_ATTACH)
    settle(page)
    wnext(page)
    assert ev(page, "()=>createWizard.step") == 4, "แนบไฟล์แล้วของเสียยังก้าวต่อไม่ได้"
    return "damage ไม่แนบไฟล์ → บล็อก (BR-23) · แนบไฟล์จริงแล้ว → ผ่านไป step 4"


# ═══════════════════════════ หมวด 4 · สายอนุมัติ (DOA) ═══════════════════════════

def c_fn14(page):
    """[FN-14 · S-11,S-12 · BR-09] ขั้นผู้อนุมัติแสดง Σ|มูลค่า| และชั้นที่ต้องใช้ตามมูลค่านั้น"""
    open_(page); open_create(page)
    set_lines(page, [{"bin": "A-01-01-A", "item": "STA-0031", "unit": "รีม", "sysQty": 100, "correctQty": 200}])  # +100×115=11,500
    goto_step(page, 4)
    body = create_text(page)
    abs_ = ev(page, "()=>createWizard.data.lines.reduce((s,l)=>s+Math.abs(lineValue(l)),0)")
    tiers = ev(page, "()=>doaTiers(createWizard.data.lines.reduce((s,l)=>s+Math.abs(lineValue(l)),0)).length")
    assert "ค่าสัมบูรณ์" in body and ("ชั้น" in body), "step ผู้อนุมัติไม่แสดง Σ|มูลค่า| / จำนวนชั้น"
    assert ev(page, "()=>createWizard.data.slots.length") == tiers, "จำนวน slot ไม่ตรงจำนวนชั้นตามมูลค่า"
    return f"step ผู้อนุมัติแสดง Σ|มูลค่า| ฿{abs_} → {tiers} ชั้น (slot = {tiers})"


def c_fn15(page):
    """[FN-15 · S-11] ใบมูลค่าต่ำ (<20,000) → สายอนุมัติชั้นเดียว"""
    open_(page); open_create(page)
    set_lines(page, [{"bin": "A-01-01-A", "item": "STA-0012", "unit": "ด้าม", "sysQty": 100, "correctQty": 110}])  # +10×6.5=65
    goto_step(page, 4)
    n = ev(page, "()=>createWizard.data.slots.length")
    assert n == 1, f"ใบมูลค่าต่ำต้องชั้นเดียว (ได้ {n})"
    role = ev(page, "()=>createWizard.data.slots[0].roles[0]")
    assert role == "WH_LEAD", f"ชั้นเดียวต้องเป็น WH_LEAD (ได้ {role})"
    return "ใบมูลค่าต่ำ ฿65 → สายอนุมัติชั้นเดียว (WH_LEAD)"


def c_fn16(page):
    """[FN-16 · S-12] ใบมูลค่าสูง → สายอนุมัติหลายชั้น เรียงลำดับชัดเจน"""
    open_(page); open_create(page)
    set_lines(page, [{"bin": "A-01-01-A", "item": "CON-0210", "unit": "กล่อง", "sysQty": 2000,
                      "mode": "delta", "deltaQty": 1000}], mode="delta")   # 1000×245=245,000
    goto_step(page, 4)
    roles = ev(page, "()=>createWizard.data.slots.map(s=>s.roles[0])")
    assert roles == ["WH_LEAD", "WH_MGR", "FIN_MGR"], f"สายอนุมัติหลายชั้นไม่เรียงถูก: {roles}"
    return f"ใบ ฿245,000 → 3 ชั้นเรียง {roles}"


def c_fn17(page):
    """[FN-17 · S-13 · BR-10] ทุก slot ต้องเลือกคนจริง — slot ว่างแม้ช่องเดียว ส่งอนุมัติไม่ได้"""
    open_(page); open_create(page)
    set_lines(page, [{"bin": "A-01-01-A", "item": "STA-0031", "unit": "รีม", "sysQty": 100, "correctQty": 120, "reason": "RS-01"}])
    goto_step(page, 4)
    wnext(page)   # slot ว่าง
    assert "ผู้อนุมัติ" in toast(page), f"slot ว่างแต่ไม่เตือน (toast='{toast(page)}')"
    assert ev(page, "()=>createWizard.step") == 4, "slot ว่างแต่ยังก้าวต่อได้"
    assert ev(page, "()=>document.querySelectorAll('#ss-create-content .slot-row.is-err').length") >= 1, \
        "slot ว่างไม่ถูก mark เป็น error บนจอ"
    # เลือกคนจริง (avatar+ชื่อ) → ก้าวต่อได้
    pick(page, "slot-0", "วิชัย มั่นคง")
    assert ev(page, "()=>createWizard.data.slots[0].assignee") == "วิชัย มั่นคง", "เลือกคนจริงแล้ว assignee ไม่ติด"
    wnext(page)
    assert ev(page, "()=>createWizard.step") == 5, "เลือกครบแล้วยังก้าวไป step 5 ไม่ได้"
    return "slot ว่าง → บล็อก + mark error · เลือกคนจริง 'วิชัย มั่นคง' → ผ่านไป step 5"


def c_fn42(page):
    """[FN-42 · BR-10 · STD] ไม่มีที่ไหนใช้ role ID/ตำแหน่งลอย ๆ แทนตัวคนในสายอนุมัติ"""
    open_(page); open_create(page)
    lid = "slot-0"
    # ตัวเลือกในสายอนุมัติเป็น "คนจริง" ทุกตัว (มี avatar + รหัสพนักงาน EMP-)
    opts = ev(page, "()=>{createWizard.data.adjType='general';createWizard.data.lines=[mkLine("
                   "{bin:'A-01-01-A',item:'STA-0031',unit:'รีม',sysQty:100,correctQty:120,reason:'RS-01'})];"
                   "createWizard.step=4;renderCreateDrawer();return comboItemsFor('%s','');}" % lid)
    assert opts, "สายอนุมัติไม่มีตัวเลือกคน"
    assert all(o.get("av") for o in opts), "ตัวเลือกสายอนุมัติบางตัวไม่มี avatar (ไม่ใช่คนจริง)"
    assert all(("EMP-" in (o.get("line2") or "")) for o in opts), f"ตัวเลือกไม่อ้างรหัสพนักงานจริง: {opts}"
    # เลือกคนจริงแล้ว: หน้าจอ step4/step5 ต้องไม่โชว์ role code ดิบ (WH_LEAD/WH_MGR/...) เป็นตัวคน
    pick(page, "slot-0", "วิชัย มั่นคง")
    goto_step(page, 5)
    body = create_text(page)
    assert "วิชัย มั่นคง" in body, "สรุปสายอนุมัติไม่โชว์ชื่อคนจริง"
    for rid in ["WH_LEAD", "WH_MGR", "FIN_MGR", "DIR", "WH_STAFF"]:
        assert rid not in body, f"หน้าจอโชว์ role ID ดิบ '{rid}' แทนตัวคน (ผิด BR-10/FN-42)"
    return "สายอนุมัติเลือกคนจริง (avatar+EMP-) · ไม่มี role ID ดิบโผล่บนจอ"


def c_fn43(page):
    """[FN-43 · S-03 · BR-09] ใบผสม +/− สุทธิใกล้ศูนย์ ยังต้องผ่านชั้นตามค่าสัมบูรณ์ ไม่หลุด"""
    open_(page); open_create(page)
    set_lines(page, [
        {"bin": "A-01-01-A", "item": "CON-0210", "unit": "กล่อง", "sysQty": 3000, "mode": "delta", "deltaQty": 1000},   # +245,000
        {"bin": "B-01-01-A", "item": "CON-0210", "unit": "กล่อง", "sysQty": 3000, "mode": "delta", "deltaQty": -1000},  # -245,000
    ], mode="delta")
    goto_step(page, 4)
    net = ev(page, "()=>createWizard.data.lines.reduce((s,l)=>s+lineValue(l),0)")
    abs_ = ev(page, "()=>createWizard.data.lines.reduce((s,l)=>s+Math.abs(lineValue(l)),0)")
    slots = ev(page, "()=>createWizard.data.slots.length")
    assert net == 0, f"สุทธิควรเป็น 0 (ได้ {net})"
    assert abs_ == 490000, f"Σ|มูลค่า| ควร 490,000 (ได้ {abs_})"
    assert slots == 3, f"สุทธิ≈0 แต่ต้องยังบังคับ 3 ชั้นตามค่าสัมบูรณ์ (ได้ {slots} ชั้น = หลุด)"
    return f"สุทธิ ฿0 แต่ Σ|มูลค่า| ฿490,000 → ยังบังคับ {slots} ชั้น (ไม่หลุด)"


# ═══════════════════════════ หมวด 5 · สถานะ + post + reverse ═══════════════════════════

def c_fn19(page):
    """[FN-19 · S-06 · BR-21] บันทึกร่างได้ · ไม่กระทบสต๊อก · ร่างยังไม่มีเลขที่จริง"""
    open_(page)
    # seed d4 = draft (code null) → แสดง '(ร่าง — ยังไม่ออกเลขที่)' · ไม่มี movement
    assert ev(page, "()=>findDoc('d4').code") is None, "seed draft d4 ควร code=null"
    assert ev(page, "()=>displayCode(findDoc('d4'))").startswith("(ร่าง"), "ร่างไม่แสดงข้อความ '(ร่าง...)'"
    assert ev(page, "()=>!(findDoc('d4').movements&&findDoc('d4').movements.length)"), "ร่างมี movement (ต้องไม่กระทบสต๊อก)"
    # สร้างร่างใหม่ผ่าน wizard → saveDraft → status draft, code null
    open_create(page)
    set_lines(page, [{"bin": "A-01-01-A", "item": "STA-0031", "unit": "รีม", "sysQty": 100, "correctQty": 120, "reason": "RS-01"}])
    n0 = ev(page, "()=>DOCS.length")
    after(page, "()=>saveDraft()")
    assert ev(page, "()=>DOCS.length") == n0 + 1, "saveDraft ไม่เพิ่มเอกสาร"
    d = ev(page, "()=>DOCS.find(x=>x.status==='draft'&&x.createdBy===ME.name&&x.id!=='d4'&&x.id!=='d10')")
    assert d and d["code"] is None, f"ร่างใหม่ต้อง code=null (ได้ {d and d['code']})"
    return "บันทึกร่าง: status=draft · code=null (ยังไม่ออกเลขที่) · ไม่มี movement"


def c_fn20(page):
    """[FN-20 · S-07 · BR-21 · OB-8] ส่งอนุมัติ → ออกเลข ADJ-YYYY-NNNN (ปี ค.ศ.)"""
    import re
    # ส่งอนุมัติผ่านเส้นทาง wizard (submitForApproval) — เส้นทางที่ทำงานได้
    # (เส้นทาง submit-modal จาก list/row-menu พังที่ slot picker — ดูเคส DEF-SUBMIT-MODAL)
    open_(page); open_create(page)
    set_lines(page, [{"bin": "A-01-01-A", "item": "STA-0031", "unit": "รีม", "sysQty": 100, "correctQty": 120, "reason": "RS-01"}])
    goto_step(page, 4)
    pick(page, "slot-0", "วิชัย มั่นคง")
    goto_step(page, 5)
    n0 = ev(page, "()=>DOC_SEQ")
    ndoc0 = ev(page, "()=>DOCS.length")
    after(page, "()=>submitForApproval()")
    d = ev(page, "()=>DOCS.find(x=>x.status==='pending'&&x.submittedBy===ME.name)")
    assert d, "ส่งอนุมัติผ่าน wizard แล้วไม่มีเอกสาร pending ของผู้ส่ง"
    assert d["code"] and re.match(r"^ADJ-2026-\d{4}$", d["code"]), f"เลขที่ไม่ใช่ ADJ-2026-NNNN (ได้ {d['code']})"
    assert d["submittedBy"] == "ปวีณา สุขทวี" and d["submittedAt"], "ไม่บันทึกผู้ส่ง/เวลา"
    assert ev(page, "()=>DOC_SEQ") == n0 + 1, "DOC_SEQ ไม่เดินหน้า 1 (ออกเลขซ้ำ/ผิด)"
    assert ev(page, "()=>DOCS.length") == ndoc0 + 1, "ส่งอนุมัติสร้างเอกสารมากกว่า 1"
    # ปี ค.ศ. — เลขต้องขึ้นต้น 2026 ไม่ใช่ 2569 (พ.ศ.)
    assert d["code"].startswith("ADJ-2026-"), f"เลขที่ไม่ใช่ปี ค.ศ.: {d['code']}"
    return f"ส่งอนุมัติ (wizard) → ออกเลข {d['code']} (ปี ค.ศ. 2026) · status=pending · DOC_SEQ +1"


def c_def_submit_modal(page):
    """[DEFECT · FN-17/FN-20 submit-modal path] slot picker ในโมดัลส่งอนุมัติ (submitStart จาก
    list/row-menu หรือปุ่ม 'ส่งอนุมัติ' ในลิ้นชักดูใบร่าง) ใช้งานไม่ได้ — เลือกผู้อนุมัติไม่ได้"""
    open_(page)
    after(page, "()=>submitStart('d4')")
    page.wait_for_function("()=>document.getElementById('ss-submit-body')", timeout=4000)
    # slot picker ในโมดัลควรเปิดรายชื่อคนได้ (comboOpen('slot-0'))
    broke = ev(page, """()=>{ try{ comboOpen('slot-0',''); const p=document.getElementById('ss-combo-pop');
        return {ok:true, n: p?p.querySelectorAll('button').length:-1}; }
        catch(e){ return {ok:false, err:String(e).slice(0,90)}; } }""")
    assert broke.get("ok"), (
        "REAL DEFECT: โมดัลส่งอนุมัติ (submitStart) เปิด slot picker ไม่ได้ — comboOpen('slot-0') โยน error: "
        + str(broke.get("err"))
        + " · ต้นเหตุ: openSubmitModal ตั้ง _slotCtx=modalState 'ก่อน' เรียก modalShell() ซึ่งเรียก "
          "closeModal() ที่รีเซ็ต _slotCtx=null → comboItemsFor('slot-0') อ่าน (null||createWizard.data).slots "
          "โดย createWizard.data=null (ยังไม่เปิด wizard) → crash. แก้: ตั้ง _slotCtx=modalState 'หลัง' modalShell()")
    assert broke.get("n", 0) >= 1, "โมดัลส่งอนุมัติ: slot picker เปิดได้แต่ไม่มีรายชื่อผู้อนุมัติให้เลือก"
    # (C3.8 · BUG-2) dropdown ต้องลอย 'หน้า' modal คลิกได้ — ไม่จมหลัง modal (z ต่ำกว่า modal · DSP-02)
    assert_pop_above_modal(page, "#ss-combo-pop", note="slot picker ในโมดัลส่งอนุมัติ")
    return "โมดัลส่งอนุมัติ: slot picker เปิดรายชื่อได้ + dropdown ลอยหน้า modal คลิกได้"


def c_fn21(page):
    """[FN-21 · S-07,S-12] อนุมัติแล้วไป slot ถัดไป / ครบทุก slot → 'อนุมัติแล้ว'"""
    open_(page)
    # d9 = pending 1 slot (assignee = ME ปวีณา) → อนุมัติครบ → approved
    assert ev(page, "()=>findDoc('d9').status") == "pending"
    open_view(page, "d9")
    after(page, "()=>openApprove('d9')")
    page.wait_for_function("()=>document.getElementById('ss-modal')", timeout=4000)
    after(page, "()=>confirmApprove('d9')")
    assert ev(page, "()=>findDoc('d9').status") == "approved", "อนุมัติ slot สุดท้ายแล้วสถานะไม่ใช่ approved"
    assert ev(page, "()=>findDoc('d9').approval_chain[0].status") == "approved", "slot ไม่ถูก mark approved"
    # d3 = pending 2 slot → อนุมัติขั้น 1 (ME=ปวีณา) → ไป slot ถัดไป (ยัง pending)
    after(page, "()=>openApprove('d3')")
    page.wait_for_function("()=>document.getElementById('ss-modal')", timeout=4000)
    after(page, "()=>confirmApprove('d3')")
    d3 = ev(page, "()=>findDoc('d3')")
    assert d3["approval_chain"][0]["status"] == "approved" and d3["approval_chain"][1]["status"] == "pending", \
        f"อนุมัติขั้น 1 แล้วไม่ส่งต่อขั้น 2: {[s['status'] for s in d3['approval_chain']]}"
    assert d3["status"] == "pending", "ยังมีขั้นถัดไปแต่สถานะข้ามไป approved"
    return "d9 (1 ชั้น) อนุมัติครบ → approved · d3 (2 ชั้น) อนุมัติขั้น 1 → ไปขั้น 2 (ยัง pending)"


def c_fn22(page):
    """[FN-22 · S-08 · BR-11] ตีกลับต้องกรอกเหตุผลก่อน + ใบกลับเป็น 'ร่าง' แก้ได้"""
    open_(page)
    open_view(page, "d9")   # pending, ME acts
    after(page, "()=>openReject('d9')")
    page.wait_for_function("()=>document.getElementById('ss-modal')", timeout=4000)
    # เหตุผลว่าง → กด OK → เตือน ไม่ตีกลับ
    after(page, "()=>document.getElementById('ss-reason-ok').click()")
    assert ev(page, "()=>findDoc('d9').status") == "pending", "ตีกลับโดยไม่กรอกเหตุผลได้ (ต้องบล็อก)"
    assert "เหตุผล" in toast(page), f"เหตุผลว่างไม่เตือน (toast='{toast(page)}')"
    # กรอกเหตุผล → ตีกลับ → draft + returned
    after(page, "()=>{document.getElementById('ss-reason').value='หลักฐานไม่พอ ขอแก้';"
                "document.getElementById('ss-reason-ok').click();}")
    d = ev(page, "()=>findDoc('d9')")
    assert d["status"] == "draft" and d.get("returned") is True, f"ตีกลับแล้วไม่เป็นร่าง/returned: {d['status']}"
    assert d["approval_chain"] == [], "ตีกลับแล้ว approval_chain ไม่ถูกล้าง"
    # draft → แก้ไขได้ (openCreateDrawer edit ไม่เด้งออก)
    after(page, "()=>openCreateDrawer('d9')")
    assert ev(page, "()=>_ovState.type") == "edit", "ใบที่ตีกลับเป็นร่างแล้วแก้ไขไม่ได้"
    return "ตีกลับ: เหตุผลว่าง→บล็อก · กรอกแล้ว→draft+returned+ล้าง chain · แก้ไขได้"


def c_fn23(page):
    """[FN-23 · S-07,S-17 · BR-08] 'ผ่านรายการ' เฉพาะ 'อนุมัติแล้ว' — จากร่าง/pending กด post ตรงไม่ได้"""
    open_(page)
    # draft d4 → postStart → บล็อก
    after(page, "()=>postStart('d4')")
    assert ev(page, "()=>findDoc('d4').status") == "draft", "ร่างถูก post ได้ (ต้องบล็อก)"
    assert "อนุมัติแล้ว" in toast(page), f"post ร่างไม่เตือน BR-08 (toast='{toast(page)}')"
    # pending d3 → postStart → บล็อก
    after(page, "()=>postStart('d3')")
    assert ev(page, "()=>findDoc('d3').status") == "pending", "pending ถูก post ได้ (ต้องบล็อก)"
    # FIX-01: doPost precondition guard ตรง ๆ — ทุกสถานะที่ไม่ใช่ approved → ไม่เปลี่ยน + ไม่เกิด movement
    for did, st in [("d4", "draft"), ("d3", "pending"), ("d1", "posted"), ("d6", "cancelled"), ("d7", "reversed")]:
        b = ev(page, "()=>({s:findDoc('%s').status,m:(findDoc('%s').movements||[]).length})" % (did, did))
        after(page, "()=>doPost('%s',false)" % did)
        a = ev(page, "()=>({s:findDoc('%s').status,m:(findDoc('%s').movements||[]).length})" % (did, did))
        assert a["s"] == b["s"], f"doPost {did} ({st}) เปลี่ยนสถานะ {b['s']}→{a['s']} (FIX-01 guard พัง)"
        assert a["m"] == b["m"], f"doPost {did} ({st}) สร้าง/แก้ movement (FIX-01 guard พัง)"
    assert "อนุมัติครบทุกขั้น" in toast(page) or "อนุมัติ" in toast(page), "doPost ใบ non-approved ไม่เตือน"
    # approved → posted ครั้งเดียว · doPost ซ้ำบน posted → block (ไม่ regenerate movement/audit)
    after(page, "()=>{findDoc('d11').status='approved';doPost('d11',false);}")
    assert ev(page, "()=>findDoc('d11').status") == "posted", "approved กด post แล้วไม่เป็น posted"
    m1 = ev(page, "()=>findDoc('d11').movements.length")
    au1 = ev(page, "()=>findDoc('d11').audit.length")
    after(page, "()=>doPost('d11',false)")   # double-post attempt
    assert ev(page, "()=>findDoc('d11').movements.length") == m1, "double-post regenerate movements (guard พัง)"
    assert ev(page, "()=>findDoc('d11').audit.length") == au1, "double-post เพิ่ม audit ซ้ำ (guard พัง)"
    # จำลองเป็น approved → post ได้ (เส้นทาง postStart modal)
    after(page, "()=>{findDoc('d9').status='approved';postStart('d9');}")
    page.wait_for_function("()=>document.getElementById('ss-modal')", timeout=4000)
    after(page, "()=>doPost('d9',false)")
    assert ev(page, "()=>findDoc('d9').status") == "posted", "approved กด post แล้วไม่เป็น posted"
    return "post: draft/pending/posted/cancelled/reversed→doPost ไม่เปลี่ยน+ไม่มี movement (FIX-01) · approved→posted ครั้งเดียว · double-post block"


def c_fn24(page):
    """[FN-24 · S-09] ยกเลิกก่อน post ต้องกรอกเหตุผล + ใบยังอยู่ในระบบ (ไม่หายไป)"""
    open_(page)
    n0 = ev(page, "()=>DOCS.length")
    open_view(page, "d4")
    after(page, "()=>openCancel('d4')")
    page.wait_for_function("()=>document.getElementById('ss-modal')", timeout=4000)
    # เหตุผลว่าง → บล็อก
    after(page, "()=>document.getElementById('ss-reason-ok').click()")
    assert ev(page, "()=>findDoc('d4').status") == "draft", "ยกเลิกโดยไม่กรอกเหตุผลได้"
    after(page, "()=>{document.getElementById('ss-reason').value='ตรวจซ้ำแล้วยอดถูก';"
                "document.getElementById('ss-reason-ok').click();}")
    d = ev(page, "()=>findDoc('d4')")
    assert d["status"] == "cancelled" and d["cancel"]["reason"], "ยกเลิกแล้วไม่บันทึกเหตุผล/สถานะ"
    assert ev(page, "()=>DOCS.length") == n0, "ยกเลิกแล้วใบหายจากระบบ (ต้องคงอยู่)"
    assert ev(page, "()=>!!findDoc('d4')"), "ใบที่ยกเลิกหาไม่เจอในระบบ"
    # FIX-02: cancel เฉพาะก่อนผ่านรายการ — posted/reversed/approved → บล็อก + toast ชี้กลับรายการ + สถานะไม่เปลี่ยน
    for did, st in [("d1", "posted"), ("d7", "reversed"), ("d11", "approved")]:
        open_(page)
        open_view(page, did)
        after(page, "()=>openCancel('%s')" % did)
        page.wait_for_function("()=>document.getElementById('ss-modal')", timeout=4000)
        after(page, "()=>{const r=document.getElementById('ss-reason');if(r)r.value='ขอยกเลิก';"
                    "document.getElementById('ss-reason-ok').click();}")
        assert ev(page, "()=>findDoc('%s').status" % did) == st, \
            f"FIX-02: cancel {did} ({st}) เปลี่ยนสถานะได้ (guard พัง — ควรบล็อก)"
        tx = toast(page)
        # posted ชี้ทาง 'กลับรายการ' · approved/reversed ยังไม่ post → 'ยกเลิกได้เฉพาะร่าง/รออนุมัติ'
        exp = "กลับรายการ" if st == "posted" else "ร่าง/รออนุมัติ"
        assert exp in tx, f"FIX-02: cancel {st} toast ไม่ตรง (คาด '{exp}' ได้ '{tx}')"
    return "ยกเลิก: เหตุผลว่าง→บล็อก · กรอกแล้ว→cancelled + ใบยังอยู่ · FIX-02 posted→ชี้กลับรายการ · approved/reversed→ยกเลิกไม่ได้"


def c_fn25(page):
    """[FN-25 · S-10 · BR-17] ใบ posted ไม่มีปุ่ม 'ยกเลิก' — มีแต่ 'กลับรายการ' ที่บังคับกรอกเหตุผล"""
    open_(page)
    ha = ev(page, "()=>headerActions(findDoc('d1'))")   # d1 posted
    assert "กลับรายการ" in ha, "ใบ posted ไม่มีปุ่มกลับรายการ"
    assert "ยกเลิก" not in ha, "ใบ posted ยังมีปุ่มยกเลิก (ต้องไม่มี)"
    # กลับรายการต้องกรอกเหตุผล
    open_view(page, "d1")
    after(page, "()=>openReverse('d1')")
    page.wait_for_function("()=>document.getElementById('ss-modal')", timeout=4000)
    after(page, "()=>document.getElementById('ss-reason-ok').click()")   # เหตุผลว่าง
    assert ev(page, "()=>findDoc('d1').status") == "posted", "กลับรายการโดยไม่กรอกเหตุผลได้"
    assert "เหตุผล" in toast(page), "กลับรายการเหตุผลว่างไม่เตือน"
    return "posted: ไม่มีปุ่มยกเลิก · มีกลับรายการ · กลับรายการเหตุผลว่าง→บล็อก"


def c_fn26(page):
    """[FN-26 · S-06 §6.1] list กรองตามสถานะได้ครบทุกสถานะ"""
    open_(page)
    status_map = {"draft": "d4", "pending": "d3", "posted": "d1", "cancelled": "d6", "reversed": "d7"}
    for st, sample in status_map.items():
        after(page, "()=>setFilter('status','%s')" % st)
        rows = ev(page, "()=>filteredDocs().map(d=>d.id)")
        allmatch = ev(page, "()=>filteredDocs().every(d=>d.status==='%s')" % st)
        assert allmatch, f"กรองสถานะ {st} แล้วมีสถานะอื่นปน"
        assert sample in rows, f"กรอง {st} ไม่พบตัวอย่าง {sample}"
    # approved: จำลอง 1 ใบแล้วกรอง
    after(page, "()=>{findDoc('d9').status='approved';setFilter('status','approved');}")
    assert ev(page, "()=>filteredDocs().every(d=>d.status==='approved')&&filteredDocs().length>=1"), "กรอง approved ไม่ทำงาน"
    return "กรองครบ 6 สถานะ (ร่าง/รออนุมัติ/อนุมัติแล้ว/ผ่านรายการ/ยกเลิก/กลับรายการแล้ว)"


def c_fn27(page):
    """[FN-27 · S-15 · BR-15] ยอดระบบเปลี่ยนหลังสร้างบรรทัด → ตอน post เตือน + แสดงยอดเดิม vs ล่าสุด"""
    open_(page)
    # d3 มีบรรทัด C-01 ที่ curSys(1005) != sysQty(1000) → จำลองเป็น approved แล้ว post → modal เตือน
    after(page, "()=>{findDoc('d3').status='approved';postStart('d3');}")
    page.wait_for_function("()=>document.getElementById('ss-modal')", timeout=4000)
    mt = modal_text(page)
    assert "ยอดระบบเปลี่ยน" in mt, f"ยอดเปลี่ยนแต่ไม่เตือนตอน post (modal='{mt[:80]}')"
    assert "1,000" in mt and "1,005" in mt, f"ไม่แสดงทั้งยอดเดิม(1,000)และล่าสุด(1,005): {mt[:120]}"
    assert "คิดจากยอดล่าสุด" in mt and "ตีกลับ" in mt, "ไม่มีทางเลือก คิดจากยอดล่าสุด / ตีกลับไปแก้"
    # ยังไม่ post จนกว่าจะเลือก → status ยัง approved
    assert ev(page, "()=>findDoc('d3').status") == "approved", "modal เตือนยังไม่ทันเลือกแต่ post ไปแล้ว"
    return "post d3 (curSys 1005 ≠ 1000) → modal เตือน BR-15 แสดง 1,000 vs 1,005 + 2 ทางเลือก"


def c_fn44(page):
    """[FN-44 · S-10 · BR-18] ใบที่กลับรายการแล้ว กลับรายการซ้ำอีกครั้งไม่ได้"""
    open_(page)
    # d7 = reversed (reversedBy set) · d8 = isReversal → openReverse ต้องบล็อกทั้งคู่
    after(page, "()=>openReverse('d7')")
    assert ev(page, "()=>!document.getElementById('ss-modal')"), "ใบ reversed เปิด modal กลับรายการซ้ำได้"
    assert "ซ้ำ" in toast(page), f"กลับรายการซ้ำไม่เตือน (toast='{toast(page)}')"
    after(page, "()=>openReverse('d8')")
    assert "ซ้ำ" in toast(page), "ใบ isReversal กลับรายการได้ (ต้องบล็อก)"
    # posted ที่ถูกกลับรายการแล้ว → headerActions ไม่มีปุ่มกลับรายการ
    ha = ev(page, "()=>headerActions(findDoc('d7'))")
    assert "กลับรายการ" not in ha, "ใบ reversed ยังมีปุ่มกลับรายการ"
    return "กลับรายการซ้ำ: d7(reversed)/d8(isReversal) → บล็อก 'ซ้ำไม่ได้' (BR-18) · ไม่มีปุ่ม"


# ═══════════════════════════ หมวด 6 · ผลปลายทาง ═══════════════════════════

def c_fn29(page):
    """[FN-29 · S-10,S-17 · BR-16,18] tab ประวัติแสดง movement จริง + คู่ reversal ผูกกัน 2 ทาง"""
    open_(page)
    assert ev(page, "()=>(findDoc('d7').movements||[]).length") >= 1, "ใบ posted/reversed ไม่มี movement"
    open_view(page, "d8")   # isReversal ของ ADJ-2026-0007
    view_tab(page, "history")
    vt = view_text(page)
    assert "Movement" in vt, "tab ประวัติไม่แสดง movement"
    assert "ADJ-2026-0007" in vt and "2 ทาง" in vt, "movement กลับรายการไม่ผูกคู่ 2 ทาง"
    # movement ของ d8 เป็นทิศ 'กลับรายการ...'
    mtypes = ev(page, "()=>findDoc('d8').movements.map(m=>m.type)")
    assert any("กลับรายการ" in t for t in mtypes), f"movement ใบกลับรายการทิศไม่ถูก: {mtypes}"
    return "ประวัติ d8 แสดง movement จริง + ผูกคู่ ADJ-2026-0007 (2 ทาง)"


def c_fn30(page):
    """[FN-30 · S-17 · BR-19] หลัง post มีป้าย 'รอลงบัญชี' + marker forward-wire JE — ไม่มีปุ่มลงบัญชีจริง"""
    open_(page)
    open_view(page, "d1")   # posted
    vt = view_text(page)
    assert "รอลงบัญชี" in vt, "ใบ posted ไม่มีป้ายสถานะ 'รอลงบัญชี'"
    assert "JE posting" in vt, "ไม่มี marker forward-wire JE"
    # ไม่มีฟังก์ชันลงบัญชี GL จริง
    for fn in ["postJE", "doGL", "postToGL", "postGL"]:
        assert ev(page, "()=>typeof window['%s']==='undefined'" % fn), f"มีฟังก์ชันลงบัญชีจริง window.{fn} (ต้องเป็น forward-wire)"
    return "posted d1: ป้าย 'รอลงบัญชี' + marker 'FWD-WIRE: JE posting' · ไม่มีปุ่ม/ฟังก์ชันลงบัญชีจริง"


def c_fn45(page):
    """[FN-45 · BR-16] ไม่มีปุ่มลบ/แก้ movement ที่ใดเลย (append-only)"""
    open_(page)
    open_view(page, "d1")
    view_tab(page, "history")
    # ตารางประวัติ movement ต้องไม่มีปุ่ม/onclick แก้-ลบ
    nbtn = ev(page, "()=>{const c=document.getElementById('ss-view-content');"
                    "return c?c.querySelectorAll('.tbl button,[onclick*=deleteMovement],[onclick*=editMovement]').length:0;}")
    assert nbtn == 0, f"tab ประวัติ/movement มีปุ่มแก้-ลบ {nbtn} จุด (ต้อง append-only)"
    for fn in ["deleteMovement", "editMovement", "removeMovement"]:
        assert ev(page, "()=>typeof window['%s']==='undefined'" % fn), f"มีฟังก์ชัน window.{fn} (ต้องไม่มี)"
    return "movement append-only: 0 ปุ่มแก้/ลบ · ไม่มีฟังก์ชัน deleteMovement/editMovement"


def c_fn34(page):
    """[FN-34 · S-22 §6.3] tab PDF: เลขที่ · วันที่(ค.ศ.) · คลัง · ตารางบรรทัด · totals · ช่องลายเซ็นตาม DOA · พิมพ์ได้"""
    open_(page)
    open_view(page, "d1")
    view_tab(page, "pdf")
    assert ev(page, "()=>document.querySelectorAll('#ss-view-content .a4').length") == 1, "ไม่มีเอกสาร A4"
    vt = view_text(page)
    assert "ADJ-2026-0001" in vt, "PDF ไม่มีเลขที่เอกสาร"
    assert "2026" in vt and "2569" not in vt, "PDF ปีไม่ใช่ ค.ศ. (พบ พ.ศ. 2569)"
    assert "คลังกรุงเทพ" in vt, "PDF ไม่มีคลัง"
    assert "Σ มูลค่าค่าสัมบูรณ์" in vt or "ค่าสัมบูรณ์" in vt, "PDF ไม่มี totals"
    nsign = ev(page, "()=>{const a=document.querySelector('#ss-view-content .a4');"
                    "return a?[].slice.call(a.querySelectorAll('div')).filter(x=>/ผู้อนุมัติขั้น|ผู้จัดทำ/.test(x.textContent)).length:0;}")
    assert nsign >= 2, f"PDF ไม่มีช่องลายเซ็นผู้จัดทำ/ผู้อนุมัติตาม DOA (พบ {nsign})"
    # ปุ่มพิมพ์
    assert ev(page, "()=>[].slice.call(document.querySelectorAll('#ss-view-content button'))"
                   ".some(b=>/window.print/.test(b.getAttribute('onclick')||''))"), "PDF ไม่มีปุ่มพิมพ์"
    return "PDF A4: เลขที่ + วันที่ ค.ศ. + คลัง + ตารางบรรทัด + totals + ช่องลายเซ็น + พิมพ์ได้"


def c_fn28(page):
    """[FN-28 · S-12,S-22] tab ลายเซ็นแสดงการ์ดผู้อนุมัติจริง (avatar+ชื่อ+ตำแหน่ง+ผล+เวลา ค.ศ.) เรียงตามชั้น"""
    open_(page)
    open_view(page, "d1")   # posted · approval_chain มี ปวีณา approved
    view_tab(page, "sign")
    n = ev(page, "()=>document.querySelectorAll('#ss-view-content .emp-chip').length")
    assert n >= 1, "tab ลายเซ็นไม่มีการ์ดผู้อนุมัติ (emp-chip)"
    vt = view_text(page)
    assert "ปวีณา สุขทวี" in vt, "การ์ดผู้อนุมัติไม่แสดงชื่อคนจริง"
    assert "อนุมัติแล้ว" in vt and "2026" in vt, "ไม่แสดงผล+เวลา (ค.ศ.) ของการอนุมัติ"
    assert "หัวหน้าคลัง" in vt, "การ์ดไม่แสดงตำแหน่ง"
    return "ลายเซ็น d1: การ์ด ปวีณา สุขทวี (หัวหน้าคลัง) · อนุมัติแล้ว + เวลา ค.ศ. 2026"


def c_fn31(page):
    """[FN-31 · S-16 · BR-22] สินค้า/หน่วยที่ถูก archive จาก master → ใบเดิมยังแสดงได้ ไม่พัง"""
    open_(page)
    # จำลอง item ถูก archive: เปลี่ยน d1 บรรทัดให้อ้าง code ที่ไม่มีใน ITEM_BY แล้วเปิด view
    after(page, "()=>{findDoc('d1').lines[0].item='STA-9999';findDoc('d1').lines[0].unit='ด้าม';}")
    open_view(page, "d1")
    view_tab(page, "detail")
    vt = view_text(page)
    assert "STA-9999" in vt, "item ที่ถูก archive ไม่แสดงรหัสเดิม"
    assert "อ้างอิงถูกยกเลิก" in vt, "ไม่มีป้ายบอกว่า master ถูกยกเลิก"
    # ไม่มี garbage (undefined/NaN) รั่วบนจอ = ไม่พัง
    assert_no_garbage_text(page, scope="#ss-view-content")
    return "item ถูก archive (STA-9999): ใบเดิมแสดงรหัส + ป้าย 'อ้างอิงถูกยกเลิก' · ไม่มี garbage/ไม่พัง"


# ═══════════════════════════ หมวด 7 · negatives (render → assert absent) ═══════════════════════════

def c_neg_fn32(page):
    """[FN-32 · S-20 · BR-13] ค้น bin in-transit (TR-BKK-CNX) ใน picker → ไม่เจอเลยทุกกรณี"""
    open_(page); open_create(page)
    set_lines(page, [{}], adjType="general")
    lid = line_id(page, 0)
    for q in ["", "TR", "TR-BKK-CNX", "ระหว่างทาง"]:
        vals = ev(page, "()=>comboItemsFor('line-bin-%s',%s).map(x=>x.val)" % (lid, json.dumps(q)))
        assert "TR-BKK-CNX" not in vals and "TR-CNX-BKK" not in vals, f"picker คืน bin in-transit เมื่อค้น '{q}': {vals}"
    # เรนเดอร์ pop จริง (ค้น TR-) → ต้องไม่มีปุ่มของ TR-BKK-CNX + ขึ้นข้อความสงวน
    goto_step(page, 2)
    after(page, "()=>comboOpen('line-bin-%s','TR-')" % lid)
    hit = ev(page, "()=>{const p=document.getElementById('ss-combo-pop');if(!p)return -1;"
                   "return [].slice.call(p.querySelectorAll('button')).filter(b=>/TR-BKK-CNX|TR-CNX-BKK/.test(b.textContent)).length;}")
    assert hit == 0, f"เมนู bin เรนเดอร์ปุ่ม in-transit จริง {hit} จุด"
    pop = ev(page, "()=>(document.getElementById('ss-combo-pop')||{}).textContent||''")
    assert "in-transit" in pop or "ระหว่างทาง" in pop or "โอนย้าย" in pop, "ไม่มีข้อความชี้ว่า in-transit สงวนให้โอนย้าย"
    return "in-transit (TR-*) ไม่โผล่ใน picker ทุกคำค้น · เมนูขึ้นข้อความสงวนให้โอนย้ายสต๊อก"


def c_neg_fn35(page):
    """[FN-35 · S-24 · BR-24] ทั้งระบบไม่มี ใบนับสต๊อก/นับรอบ/cycle count/count sheet/blind count"""
    open_(page)
    needles = ["นับรอบ", "cycle count", "Cycle Count", "count sheet", "Count Sheet", "blind count", "ใบนับสต๊อก"]
    assert_text_absent(page, needles, scope="#ss-page")
    assert_text_absent(page, needles, scope="#ss-sidebar")
    # ในลิ้นชักสร้าง (ทุก step) ก็ต้องไม่มี
    open_create(page)
    for stp in (1, 2, 3):
        goto_step(page, stp)
        assert_text_absent(page, needles, scope="#ss-create-content")
    return "ไม่มี ใบนับสต๊อก/นับรอบ/cycle count/count sheet/blind count (list+sidebar+ทุก step)"


def c_neg_fn36(page):
    """[FN-36 · S-25 · BR-05] ในบรรทัดไม่มีช่อง bin ปลายทาง/ย้ายไป — ค้น 'ย้าย' ชี้ไป Stock Transfer"""
    open_(page); open_create(page)
    set_lines(page, [{"bin": "A-01-01-A", "item": "STA-0031", "unit": "รีม", "sysQty": 100, "correctQty": 120}])
    goto_step(page, 2)
    # แต่ละแถวมี bin input เดียว (ไม่มี bin ปลายทาง)
    per_row = ev(page, "()=>{const rows=document.querySelectorAll('#ss-create-content .line-tbl tbody tr');"
                     "return [].slice.call(rows).map(tr=>tr.querySelectorAll('input[id^=cbi-line-bin-]').length);}")
    assert per_row and all(c == 1 for c in per_row), f"บางแถวมี bin มากกว่า 1 ช่อง (bin ปลายทาง?): {per_row}"
    assert_text_absent(page, ["bin ปลายทาง", "ปลายทาง", "ย้ายไป", "ช่องเก็บปลายทาง"], scope="#ss-create-content")
    # ค้น 'ย้าย' ในเมนู bin → ชี้ไป Stock Transfer
    lid = line_id(page, 0)
    after(page, "()=>comboOpen('line-bin-%s','ย้าย')" % lid)
    pop = ev(page, "()=>(document.getElementById('ss-combo-pop')||{}).textContent||''")
    assert "โอนย้ายสต๊อก" in pop or "Stock Transfer" in pop, f"ค้น 'ย้าย' ไม่ชี้ไป Stock Transfer (pop='{pop[:80]}')"
    return "บรรทัดมี bin ช่องเดียว · ไม่มี bin ปลายทาง/ย้ายไป · ค้น 'ย้าย' → ชี้ไปโอนย้ายสต๊อก"


def c_neg_fn46(page):
    """[FN-46 · S-18 · BR-12] ของ quarantine ปรับยอดได้ แต่ไม่มีทางย้ายออกไป bin storage จากหน้านี้"""
    open_(page); open_create(page)
    set_lines(page, [{}], adjType="quarantine")
    lid = line_id(page, 0)
    types = ev(page, "()=>comboItemsFor('line-bin-%s','').map(x=>(BIN_BY[x.val]||{}).type)" % lid)
    assert types and all(t == "quarantine" for t in types), f"โหมดกักกันเลือก bin storage ได้ (ย้ายออกได้): {types}"
    # ปรับยอด "ในบิ๊นกักกันเดิม" ได้จริง (เลือก QA-01 + สินค้า + ยอด)
    pick(page, "line-bin-%s" % lid, "QA-01")
    pick(page, "line-item-%s" % lid, "ELE-0501")
    set_qty(page, lid, "correctQty", ev(page, "()=>createWizard.data.lines[0].sysQty") - 5)
    assert ev(page, "()=>lineDiff(createWizard.data.lines[0])") == -5, "ปรับยอดในบิ๊นกักกันไม่ได้"
    # ไม่มี affordance ย้ายออก
    assert_text_absent(page, ["ย้ายออก", "ย้ายไปช่องเก็บ", "ย้ายไป storage", "release to storage"], scope="#ss-create-content")
    return "quarantine: ปรับยอดในบิ๊นเดิมได้ (−5) · picker ไม่มี storage · ไม่มีปุ่มย้ายออก"


def c_neg_fn47(page):
    """[FN-47 · OB-8 · BR-20] ไม่มีช่องกรอกเลขที่เอง + ไม่มีหน้าตั้งค่ารูปแบบเลขรันในหน้า feature"""
    open_(page); open_create(page)
    goto_step(page, 1)
    # ช่องเลขที่เอกสารต้อง disabled (กรอกเองไม่ได้)
    dis = ev(page, "()=>{const inps=document.querySelectorAll('#ss-create-content input');"
                   "let bad=0;inps.forEach(i=>{const lb=(i.closest('.field')||{}).textContent||'';"
                   "if(/เลขที่เอกสาร/.test(lb)&&!i.disabled)bad++;});return bad;}")
    assert dis == 0, "มีช่องกรอกเลขที่เอกสารเองที่ไม่ disabled"
    assert_text_absent(page, ["ตั้งค่ารูปแบบเลข", "รูปแบบเลขรัน", "running number config", "ตั้งค่าเลขรัน", "prefix เลข"],
                       scope="#ss-create-content")
    assert_text_absent(page, ["ตั้งค่ารูปแบบเลข", "รูปแบบเลขรัน"], scope="#ss-page")
    return "เลขที่เอกสาร disabled (ออกอัตโนมัติ) · ไม่มีหน้าตั้งค่ารูปแบบเลขรันในหน้า feature"


def c_neg_fn48(page):
    """[FN-48 · OB-15 · BR-20] ไม่มีช่องกรอก threshold/% เตือน ในหน้า feature (อยู่ NC rules)"""
    open_(page); open_create(page)
    for stp in (1, 2, 3):
        goto_step(page, stp)
        assert_text_absent(page, ["threshold", "Threshold", "% เตือน", "เกณฑ์เตือน", "ตั้งเกณฑ์", "tolerance"],
                           scope="#ss-create-content")
    assert_text_absent(page, ["threshold", "เกณฑ์เตือน", "ตั้งเกณฑ์"], scope="#ss-page")
    # ไม่มี input ที่ผูกกับ threshold
    assert ev(page, "()=>document.querySelectorAll('[id*=threshold],[name*=threshold],[placeholder*=เกณฑ์]').length") == 0, \
        "พบ input threshold ในหน้า feature"
    return "ไม่มีช่อง threshold/% เตือน/เกณฑ์ ในหน้า feature (list + ทุก step)"


def c_neg_fn49(page):
    """[FN-49 · §3.6] ไม่มีคอลัมน์ VAT/ส่วนลด ในตารางบรรทัด"""
    open_(page); open_create(page)
    set_lines(page, [{"bin": "A-01-01-A", "item": "STA-0031", "unit": "รีม", "sysQty": 100, "correctQty": 120}])
    goto_step(page, 2)
    heads = ev(page, "()=>[].slice.call(document.querySelectorAll('#ss-create-content .line-tbl thead th')).map(th=>th.textContent.trim())")
    assert heads, "ไม่พบหัวตารางบรรทัด"
    for h in heads:
        assert not any(k in h for k in ["VAT", "ภาษี", "ส่วนลด", "Discount"]), f"ตารางบรรทัดมีคอลัมน์ VAT/ส่วนลด: '{h}'"
    # step 5 review + view drawer detail ก็ต้องไม่มีคอลัมน์ VAT
    goto_step(page, 5)
    heads5 = ev(page, "()=>[].slice.call(document.querySelectorAll('#ss-create-content table thead th')).map(th=>th.textContent.trim())")
    for h in heads5:
        assert "VAT" not in h and "ภาษี" not in h, f"หน้า review มีคอลัมน์ภาษี: '{h}'"
    return f"ตารางบรรทัดไม่มีคอลัมน์ VAT/ภาษี/ส่วนลด (หัว: {heads})"


# ═══════════════════════════ หมวด 8 · ทั่วไป ═══════════════════════════

def c_fn90(page):
    """[FN-90 · §6.1] ค้นหา/filter ใน list ทำงานจริง + empty state บอกวิธีแก้"""
    open_(page)
    total = ev(page, "()=>DOCS.length")
    # ค้นด้วยเลขที่จริง
    after(page, "()=>{state.filters.q='ADJ-2026-0001';renderListPage();}")
    ids = ev(page, "()=>filteredDocs().map(d=>d.code)")
    assert ids == ["ADJ-2026-0001"], f"ค้นเลขที่ไม่ตรง: {ids}"
    # ค้นด้วยชื่อสินค้า
    after(page, "()=>{state.filters.q='ปูนซีเมนต์';renderListPage();}")
    assert ev(page, "()=>filteredDocs().length") >= 1, "ค้นชื่อสินค้าไม่เจอ"
    # ค้นด้วยชื่อผู้จัดทำ (ต้อง search ได้ — dropdown ผู้จัดทำถูกเอาออกแล้ว)
    after(page, "()=>{state.filters.q='สมชาย';renderListPage();}")
    _cr = ev(page, "()=>filteredDocs().map(d=>d.createdBy)")
    assert len(_cr) >= 1 and all("สมชาย" in c for c in _cr), f"ค้นชื่อผู้จัดทำไม่ได้: {_cr}"
    # มีคอลัมน์ 'ผู้จัดทำ' ในตาราง + ไม่มี dropdown filter ผู้จัดทำ/เหตุผลแล้ว
    _ths = ev(page, "()=>[...document.querySelectorAll('.tbl thead th')].map(t=>t.textContent.trim())")
    assert "ผู้จัดทำ" in _ths, f"ไม่มีคอลัมน์ผู้จัดทำในตาราง: {_ths}"
    _opts = ev(page, "()=>[...document.querySelectorAll('.filt-grid select option')].map(o=>o.textContent)")
    assert not any("ผู้จัดทำ" in o for o in _opts), "ยังมี dropdown filter ผู้จัดทำ (ต้องเอาออก)"
    assert not any("เหตุผล" in o for o in _opts), "ยังมี dropdown filter เหตุผล (ต้องเอาออก)"
    after(page, "()=>{state.filters.q='';renderListPage();}")
    # ค้นไม่พบ → empty state + ปุ่มล้างตัวกรอง
    after(page, "()=>{state.filters.q='ไม่มีทางเจอ__zzz';renderListPage();}")
    assert ev(page, "()=>filteredDocs().length") == 0
    pt = page_text(page)
    assert "ไม่พบรายการ" in pt and ("ล้างตัวกรอง" in pt or "ปรับคำค้น" in pt), "empty state ไม่บอกวิธีแก้"
    after(page, "()=>resetFilters()")
    assert ev(page, "()=>filteredDocs().length") == total, "ล้างตัวกรองแล้วไม่กลับเป็นทั้งหมด"
    # (C3.8) พิมพ์ในช่องค้นหาจริงทีละตัว → focus ต้องไม่หลุด (bug: oninput เรนเดอร์ทั้งหน้า พิมพ์ได้ตัวเดียว)
    page.focus("#ss-list-search")
    for ch in "ADJ":
        page.keyboard.type(ch)
        settle(page)
        assert ev(page, "()=>document.activeElement&&document.activeElement.id") == "ss-list-search", \
            "พิมพ์ในช่องค้นหาแล้ว focus หลุด (oninput เรนเดอร์ทั้งหน้า — iron #29)"
    assert ev(page, "()=>document.getElementById('ss-list-search').value") == "ADJ", \
        "ช่องค้นหารับได้ไม่ครบทุกตัวอักษร (focus หลุดกลางคัน)"
    # (C3.8) ไอคอน search ต้องอยู่ในกล่อง input ไม่ลอย (bug: CSS `>i` หลุดหลัง Lucide swap เป็น svg)
    assert_icon_inside_input(page, ".filt-search", note="ไอคอน search ในช่องค้นหา list")
    after(page, "()=>resetFilters()")
    return f"ค้นเลขที่/สินค้าได้จริง · empty state · reset กลับ {total} ใบ · พิมพ์ค้นหาต่อเนื่อง focus ไม่หลุด"


def c_fn91(page):
    """[FN-91 · BR-16,17] ทุกยกเลิก/กลับรายการผ่าน confirm (reason modal) + ไม่มี hard delete"""
    open_(page)
    # ยกเลิก/ตีกลับ/กลับรายการ ล้วนเปิด reason modal (ต้องกรอกเหตุผล)
    for fn, sample in [("openCancel", "d4"), ("openReject", "d9"), ("openReverse", "d1")]:
        open_(page)
        if fn == "openReject":
            open_view(page, sample)   # ต้องเป็นผู้มีสิทธิ์ในขั้น
        after(page, "()=>%s('%s')" % (fn, sample))
        has_reason = ev(page, "()=>!!document.getElementById('ss-reason')")
        assert has_reason, f"{fn} ไม่เปิดช่องกรอกเหตุผล (confirm)"
        after(page, "()=>closeModal()")
    # ไม่มีฟังก์ชัน hard delete
    for f in ["deleteDoc", "removeDoc", "hardDelete", "destroyDoc"]:
        assert ev(page, "()=>typeof window['%s']==='undefined'" % f), f"มีฟังก์ชัน hard delete window.{f}"
    return "ยกเลิก/ตีกลับ/กลับรายการ ผ่าน reason modal ทุกตัว · ไม่มีฟังก์ชัน hard delete"


def c_fn92(page):
    """[FN-92 · §5.1] field บังคับ validate ก่อนบันทึก + กัน double-submit ตอนส่งอนุมัติ"""
    open_(page); open_create(page)
    # (ก) required validate: ล้างวันที่มีผล → step1 wizardNext บล็อก
    after(page, "()=>{createWizard.data.effDate='';renderCreateDrawer();}")
    wnext(page)
    assert ev(page, "()=>createWizard.step") == 1, "วันที่มีผลว่างแต่ก้าวต่อได้ (ไม่ validate)"
    assert "ครบถ้วน" in toast(page) or "กรอก" in toast(page), f"required ไม่เตือน (toast='{toast(page)}')"
    # (ข) double-submit guard: สร้างใบครบ ส่งอนุมัติ แล้วกดปุ่มซ้ำ → เกิดใบใหม่ใบเดียว
    open_(page); open_create(page)
    set_lines(page, [{"bin": "A-01-01-A", "item": "STA-0031", "unit": "รีม", "sysQty": 100, "correctQty": 120, "reason": "RS-01"}])
    goto_step(page, 4)
    pick(page, "slot-0", "วิชัย มั่นคง")
    goto_step(page, 5)
    n0 = ev(page, "()=>DOCS.length")
    # กดปุ่มส่งจริง 2 ครั้งติด — ปุ่มถูก disable หลังคลิกแรก → ต้องได้ใบเดียว
    ev(page, "()=>{const b=document.getElementById('ss-btn-submit');b.click();b.click();}")
    settle(page, timeout=3000)
    n1 = ev(page, "()=>DOCS.filter(d=>d.status==='pending'&&d.submittedBy===ME.name).length")
    made = ev(page, "()=>DOCS.length") - n0
    assert made == 1, f"double-submit สร้างใบ {made} ใบ (ต้อง 1 · กัน double)"
    return "required validate (วันที่ว่าง→บล็อก) · double-submit ปุ่ม disable → สร้างใบเดียว"


def c_fn38(page):
    """[FN-38 · OB-14] ทุกวันที่/เวลา ในจอ+PDF เป็นปี ค.ศ. ไม่มี พ.ศ. ปนแม้จุดเดียว"""
    open_(page)
    pt = page_text(page)
    assert "2026" in pt, "list ไม่มีปี ค.ศ. 2026"
    assert "2569" not in pt and "พ.ศ." not in pt, "list พบปี พ.ศ. (2569/พ.ศ.)"
    # view detail + pdf
    open_view(page, "d1")
    for tab in ("detail", "pdf", "sign", "history"):
        view_tab(page, tab)
        vt = view_text(page)
        assert "2569" not in vt and "พ.ศ." not in vt, f"tab {tab} พบปี พ.ศ."
    # fmtDate ใช้ getFullYear (ค.ศ.) โดยตรง
    y = ev(page, "()=>fmtDate('2026-09-05')")
    assert "2026" in y, f"fmtDate ไม่คืนปี ค.ศ. (ได้ {y})"
    return "ทุกวันที่เป็นปี ค.ศ. 2026 (list + view 4 tabs + PDF) · ไม่มี พ.ศ./2569"


def c_fn39(page):
    """[FN-39 · BR-25] audit บันทึกทุก create/แก้/ส่ง/อนุมัติ/ตีกลับ/post/กลับรายการ แบบ append-only"""
    open_(page)
    # d1 posted → audit มี สร้าง+ส่ง+อนุมัติ+post
    acts = ev(page, "()=>findDoc('d1').audit.map(a=>a.act)")
    assert any("สร้าง" in a for a in acts) and any("ส่งอนุมัติ" in a for a in acts) \
        and any("อนุมัติ" in a for a in acts) and any("ผ่านรายการ" in a for a in acts), \
        f"audit d1 ไม่ครบ create/ส่ง/อนุมัติ/post: {acts}"
    # อนุมัติ d9 → audit เพิ่ม (append-only, ไม่ลบของเดิม)
    n0 = ev(page, "()=>findDoc('d9').audit.length")
    open_view(page, "d9")
    after(page, "()=>openApprove('d9')")
    page.wait_for_function("()=>document.getElementById('ss-modal')", timeout=4000)
    after(page, "()=>confirmApprove('d9')")
    n1 = ev(page, "()=>findDoc('d9').audit.length")
    assert n1 == n0 + 1, f"อนุมัติแล้ว audit ไม่ถูก append (n0={n0} n1={n1})"
    # history tab ไม่มีปุ่มแก้/ลบ audit
    view_tab(page, "history")
    nbtn = ev(page, "()=>document.querySelectorAll('#ss-view-content .tl button,#ss-view-content .tl [onclick]').length")
    assert nbtn == 0, f"timeline audit มีปุ่มแก้/ลบ {nbtn} (ต้อง append-only)"
    return f"audit ครบทุก action (d1) · อนุมัติ d9 → append (+1) · ไม่มีปุ่มแก้/ลบ timeline"


def c_fn50(page):
    """[FN-50 · OB-14] sidebar เป็นเมนู Warehouse ตาม module map กลาง — ไม่มีเมนูที่ feature คิดเอง"""
    open_(page)
    feats = ev(page, "()=>[].slice.call(document.querySelectorAll('#ss-sidebar .sb-item')).map(a=>a.getAttribute('data-feature'))")
    assert feats == ["putaway", "stkadj", "stktrf", "rtv"], f"sidebar ไม่ตรง module map Warehouse: {feats}"
    active = ev(page, "()=>{const a=document.querySelector('#ss-sidebar .sb-item.active');return a?a.getAttribute('data-feature'):null;}")
    assert active == "stkadj", f"เมนู active ไม่ใช่ stkadj (ได้ {active})"
    grp = ev(page, "()=>(document.querySelector('#ss-sidebar .sb-grp-label')||{}).textContent||''")
    assert "คลังสินค้า" in grp, f"กลุ่มเมนูไม่ใช่ 'คลังสินค้า' (ได้ '{grp}')"
    return "sidebar = Warehouse module (putaway/stkadj*/stktrf/rtv) กลุ่ม 'คลังสินค้า' · stkadj active"


# ═══════════════════════════ FIX re-gate · guard-proof ═══════════════════════════

def c_rev_doa(page):
    """[FIX-03 · FN-25/FN-29] กลับรายการ ≥20k → ใบใหม่ 'pending' เดิน DOA ตาม tier (ไม่ auto-post) → อนุมัติครบ → post → movement ทิศตรงข้าม + ผูก 2 ทาง + BR-18"""
    open_(page)
    # สร้างใบ posted มูลค่าสูง (1000×245 = 245,000 → reversal ต้อง 3 ชั้น)
    after(page, """()=>{
        const big=mkLine({bin:'A-01-01-A',item:'CON-0210',unit:'กล่อง',sysQty:2000,mode:'delta',deltaQty:1000,reason:'RS-02'});
        const doc={id:'dRT',code:'ADJ-2026-0090',status:'posted',wh:'WH-BKK-01',adjType:'general',effDate:'2026-09-14',cc:'CC-WH-BKK',
          note:'ทดสอบกลับรายการเดิน DOA',createdBy:'สมชาย ใจดี',createdAt:nowIso(),updatedBy:ME.name,updatedAt:nowIso(),
          submittedBy:'สมชาย ใจดี',submittedAt:nowIso(),lines:[big],attachments:[],approval_chain:[],posted:{by:ME.name,at:nowIso()},
          audit:[{act:'สร้างใบปรับยอด',by:'สมชาย ใจดี',at:nowIso(),note:''}]};
        doc.movements=doc.lines.map(l=>mkMovement(doc,l)); DOCS.unshift(doc);
    }""")
    # กลับรายการ — เปิด view drawer ของใบ posted ก่อน (flow จริงของ user: เปิดใบดู → กดกลับรายการ)
    open_view(page, "dRT")
    after(page, "()=>openReverse('dRT')")
    page.wait_for_function("()=>document.getElementById('ss-modal')", timeout=4000)
    after(page, "()=>{document.getElementById('ss-reason').value='กลับรายการทดสอบ';document.getElementById('ss-reason-ok').click();}")
    rev = ev(page, "()=>DOCS.find(d=>d.isReversal&&d.reversalOf==='ADJ-2026-0090')")
    assert rev, "ไม่พบใบกลับรายการที่สร้าง"
    assert rev["status"] == "pending", f"FIX-03: ใบกลับรายการ auto-post (status={rev['status']}) — ต้องเป็น pending"
    assert not (rev.get("movements") and len(rev["movements"])), "FIX-03: ใบกลับรายการ pending แต่มี movement แล้ว (auto-post)"
    roles = [s["roles"][0] for s in rev["approval_chain"]]
    assert roles == ["WH_LEAD", "WH_MGR", "FIN_MGR"], f"FIX-03: chain ใบกลับรายการไม่ตาม tier มูลค่า (245k→3ชั้น): {roles}"
    assert all(s["status"] == "pending" for s in rev["approval_chain"]), "FIX-03: chain ใบกลับรายการไม่ได้ pending ทุกขั้น (ยัง hardcode approved?)"
    # ต้นฉบับ reversed + BR-18 กลับซ้ำไม่ได้
    assert ev(page, "()=>findDoc('dRT').status") == "reversed", "ต้นฉบับไม่เป็น reversed"
    after(page, "()=>openReverse('dRT')")
    assert "ซ้ำ" in toast(page), "BR-18: กลับรายการซ้ำได้ (ต้องบล็อก)"
    # อนุมัติครบทุกขั้น (override submittedBy≠ME + assignee=ME เพื่อผ่าน SoD/canActStep) → post → movement ทิศตรงข้าม
    rid = rev["id"]
    after(page, "()=>{const d=findDoc('%s');d.submittedBy='สมชาย ใจดี';d.approval_chain.forEach(s=>s.assignee=ME.name);}" % rid)
    for _ in range(3):
        after(page, "()=>openApprove('%s')" % rid)
        after(page, "()=>confirmApprove('%s')" % rid)
    assert ev(page, "()=>findDoc('%s').status" % rid) == "approved", "อนุมัติครบแล้วใบกลับรายการไม่เป็น approved"
    after(page, "()=>postStart('%s')" % rid)
    after(page, "()=>doPost('%s',false)" % rid)
    assert ev(page, "()=>findDoc('%s').status" % rid) == "posted", "post ใบกลับรายการ (approved) ไม่สำเร็จ"
    movs = ev(page, "()=>findDoc('%s').movements.map(m=>m.type)" % rid)
    assert movs and all("กลับรายการ" in t for t in movs), f"movement ใบกลับรายการทิศไม่ถูก: {movs}"
    # ผูกคู่ 2 ทาง
    assert ev(page, "()=>findDoc('%s').reversalOf" % rid) == "ADJ-2026-0090"
    assert ev(page, "()=>findDoc('dRT').reversedBy") == rev["code"], "ต้นฉบับไม่ผูกกลับไปใบกลับรายการ (2 ทาง)"
    # (C3.8 · BUG-1) หลังกลับรายการ (navigate ไป view ใบใหม่) → ปิด drawer → ต้องไม่ค้าง scroll-lock
    after(page, "()=>closeViewDrawer()")
    settle(page)
    assert_no_scroll_lock_leak(page, note="หลังกลับรายการ+ปิด drawer ใบกลับรายการ")
    return f"กลับรายการ 245k → ใบใหม่ pending 3 ชั้น {roles} (ไม่ auto-post) · อนุมัติครบ+post → movement ทิศตรงข้าม + ผูก 2 ทาง + BR-18 · ปิดแล้วไม่ค้าง scroll-lock"


def c_fix04_source(page):
    """[FIX-04 · trace ใบนับ] ใบ 'จากใบนับ' แสดง ref ใน view drawer · 'ปรับตรง' ไม่มี · wizard เลือกแหล่งที่มาได้ · ไม่มีหน้าจอใบนับ"""
    open_(page)
    # d3 seed = source count → view detail แสดงใบนับต้นเรื่อง
    open_view(page, "d3")
    view_tab(page, "detail")
    vt = view_text(page)
    assert "CNT-2026-0012" in vt, "ใบจากใบนับไม่แสดง ref (CNT-2026-0012) ใน view drawer"
    assert "ใบนับต้นเรื่อง" in vt, "ไม่มี label 'ใบนับต้นเรื่อง' ใน view drawer"
    # d1 = ปรับตรง → ไม่มี ref
    open_view(page, "d1")
    view_tab(page, "detail")
    assert "ใบนับต้นเรื่อง" not in view_text(page), "ใบปรับตรง (d1) กลับแสดง ref ใบนับ"
    # wizard: เลือกแหล่งที่มา 'จากใบนับ' + combobox display-only
    open_create(page)
    assert ev(page, "()=>createWizard.data.source") == "direct", "แหล่งที่มา default ต้องเป็น 'ปรับตรง' (direct)"
    after(page, "()=>setAdjSource('count')")
    assert ev(page, "()=>createWizard.data.source") == "count", "setAdjSource('count') ไม่ทำงาน"
    items = ev(page, "()=>comboItemsFor('wiz-countdoc','').map(x=>x.val)")
    assert "CNT-2026-0012" in items and "CYC-2026-0031" in items, f"combobox ใบนับไม่มีตัวเลือก F084/F086: {items}"
    after(page, "()=>comboPick('wiz-countdoc','CNT-2026-0012')")
    assert ev(page, "()=>createWizard.data.ref_count_doc") == "CNT-2026-0012", "เลือกใบนับแล้ว ref ไม่ติด"
    # กลับไป 'ปรับตรง' → ล้าง ref
    after(page, "()=>setAdjSource('direct')")
    assert ev(page, "()=>createWizard.data.ref_count_doc") is None, "สลับกลับปรับตรงแล้ว ref ไม่ถูกล้าง"
    # (BR-26) แหล่งที่มา 'จากใบนับ' แต่ไม่เลือกใบนับ → ไปต่อ/ส่งอนุมัติไม่ได้
    after(page, "()=>{createWizard.step=1;createWizard.data.source='count';createWizard.data.ref_count_doc=null;renderCreateDrawer();}")
    after(page, "()=>wizardNext()")
    assert ev(page, "()=>createWizard.step") == 1, "BR-26: จากใบนับไม่เลือกใบนับ แต่ข้าม step 1 ได้ (guard พัง)"
    assert "BR-26" in toast(page) or "ใบนับ" in toast(page), f"BR-26: ไม่มี toast เตือนเลือกใบนับ (ได้ '{toast(page)}')"
    assert ev(page, "()=>{const e=document.getElementById('f-source');return e&&e.classList.contains('is-error');}"), \
        "BR-26: field แหล่งที่มาไม่ขึ้นกรอบแดง (markErr ชี้ id ผิด)"
    after(page, "()=>submitForApproval()")
    assert ev(page, "()=>createWizard.data.code") is None, "BR-26: ส่งอนุมัติสำเร็จทั้งที่ยังไม่เลือกใบนับ (ออกเลขแล้ว)"
    # เลือกใบนับแล้ว → ผ่าน step 1 ได้
    after(page, "()=>comboPick('wiz-countdoc','CYC-2026-0031')")
    after(page, "()=>wizardNext()")
    assert ev(page, "()=>createWizard.step") == 2, "BR-26: เลือกใบนับแล้วยังไปต่อไม่ได้"
    # negative-scope: ไม่มีหน้าจอ/affordance นับสต๊อกในลิ้นชัก
    open_create(page)
    after(page, "()=>setAdjSource('count')")
    assert_text_absent(page, ["ใบนับสต๊อก", "count sheet", "Count Sheet", "นับรอบ", "cycle count", "blind count"],
                       scope="#ss-create-content")
    return "ใบจากใบนับ (d3) โชว์ ref · ปรับตรง (d1) ไม่มี · combobox F084/F086 · BR-26 บังคับเลือกใบนับก่อนส่ง · ไม่มีหน้าจอนับสต๊อก"


def c_fix09_demo(page):
    """[FIX-09 · demo-only] ซ่อน .demo-only แล้วไม่เหลือศัพท์ dev (ENG-DOC-NUM/FWD-WIRE/BR-xx) บนจอ + layout ไม่พัง"""
    open_(page)
    # inject .demo-only{display:none} (production build)
    ev(page, "()=>{const s=document.createElement('style');s.textContent='.demo-only{display:none!important}';document.head.appendChild(s);}")
    needles = ["FWD-WIRE", "ENG-DOC-NUM", "BR-01", "BR-02", "BR-08", "BR-10", "BR-15", "BR-18", "BR-21", "BR-23"]

    def visible_text():
        # innerText = เฉพาะข้อความที่แสดงจริง (ไม่รวม display:none / comment)
        return ev(page, "()=>{let t=document.getElementById('ss-app').innerText;"
                        "const ov=document.getElementById('ss-overlay-root');if(ov)t+=' '+ov.innerText;"
                        "const md=document.getElementById('ss-modal');if(md)t+=' '+md.innerText;return t;}")

    # list ว่าง ๆ
    vt = visible_text()
    for n in needles:
        assert n not in vt, f"หน้า list ยังเหลือศัพท์ dev '{n}' หลังซ่อน demo-only"
    # เปิดลิ้นชักสร้าง (step 2 มี valuation badge · step 4 มี DOA badge)
    open_create(page)
    for stp in (1, 2, 4):
        goto_step(page, stp)
        vt = visible_text()
        for n in needles:
            assert n not in vt, f"wizard step {stp} ยังเหลือ '{n}' หลังซ่อน demo-only"
    # view drawer (JE/valuation badges)
    open_(page)
    ev(page, "()=>{const s=document.createElement('style');s.textContent='.demo-only{display:none!important}';document.head.appendChild(s);}")
    open_view(page, "d1")
    for tab in ("detail", "sign"):
        view_tab(page, tab)
        vt = visible_text()
        for n in needles:
            assert n not in vt, f"view tab {tab} ยังเหลือ '{n}' หลังซ่อน demo-only"
    # layout ไม่พัง: badge ยังอยู่ใน DOM (textContent เห็น) แต่ innerText (มองเห็น) ไม่เห็น
    assert ev(page, "()=>document.querySelectorAll('.fwd-badge.demo-only').length") >= 1, "fwd-badge ไม่ได้ติด class demo-only"
    assert_no_garbage_text(page, scope="#ss-view-content")
    return "ซ่อน .demo-only → ไม่เหลือ FWD-WIRE/ENG-DOC-NUM/BR-xx บนจอ (list+wizard 1/2/4+view detail/sign) · badge ยังอยู่ใน DOM · ไม่พัง"


# ═══════════════════════════════ RUN ═══════════════════════════════

CASES = [
    ("E01", c_fn01, ["FN-01"]),
    ("E02", c_fn02, ["FN-02"]),
    ("E03", c_fn03, ["FN-03"]),
    ("E09", c_fn09, ["FN-09"]),
    ("E04", c_fn04, ["FN-04"]),
    ("E05", c_fn05, ["FN-05"]),
    ("E06", c_fn06, ["FN-06"]),
    ("E07", c_fn07, ["FN-07"]),
    ("E08", c_fn08, ["FN-08"]),
    ("E10", c_fn10, ["FN-10"]),
    ("E11", c_fn11, ["FN-11"]),
    ("E12", c_fn12, ["FN-12"]),
    ("E13", c_fn13, ["FN-13"]),
    ("E18", c_fn18, ["FN-18"]),
    ("E37", c_fn37, ["FN-37"]),
    ("E40", c_fn40, ["FN-40"]),
    ("E41", c_fn41, ["FN-41"]),
    ("E33", c_fn33, ["FN-33"]),
    ("E51", c_fn51, ["FN-51"]),
    ("E14", c_fn14, ["FN-14"]),
    ("E15", c_fn15, ["FN-15"]),
    ("E16", c_fn16, ["FN-16"]),
    ("E17", c_fn17, ["FN-17"]),
    ("E42", c_fn42, ["FN-42"]),
    ("E43", c_fn43, ["FN-43"]),
    ("E19", c_fn19, ["FN-19"]),
    ("E20", c_fn20, ["FN-20"]),
    ("DEF-SUBMIT-MODAL", c_def_submit_modal, []),
    ("E21", c_fn21, ["FN-21"]),
    ("E22", c_fn22, ["FN-22"]),
    ("E23", c_fn23, ["FN-23"]),
    ("E24", c_fn24, ["FN-24"]),
    ("E25", c_fn25, ["FN-25"]),
    ("E26", c_fn26, ["FN-26"]),
    ("E27", c_fn27, ["FN-27"]),
    ("E44", c_fn44, ["FN-44"]),
    ("E29", c_fn29, ["FN-29"]),
    ("E30", c_fn30, ["FN-30"]),
    ("E45", c_fn45, ["FN-45"]),
    ("E34", c_fn34, ["FN-34"]),
    ("E28", c_fn28, ["FN-28"]),
    ("E31", c_fn31, ["FN-31"]),
    ("N32", c_neg_fn32, ["FN-32"]),
    ("N35", c_neg_fn35, ["FN-35"]),
    ("N36", c_neg_fn36, ["FN-36"]),
    ("N46", c_neg_fn46, ["FN-46"]),
    ("N47", c_neg_fn47, ["FN-47"]),
    ("N48", c_neg_fn48, ["FN-48"]),
    ("N49", c_neg_fn49, ["FN-49"]),
    ("E90", c_fn90, ["FN-90"]),
    ("E91", c_fn91, ["FN-91"]),
    ("E92", c_fn92, ["FN-92"]),
    ("E38", c_fn38, ["FN-38"]),
    ("E39", c_fn39, ["FN-39"]),
    ("E50", c_fn50, ["FN-50"]),
    ("FIX03-REV-DOA", c_rev_doa, ["FN-25", "FN-29"]),
    ("E52", c_fix04_source, ["FN-52"]),
    ("FIX09-DEMO", c_fix09_demo, []),
]

ALL_FN = ["FN-01", "FN-02", "FN-03", "FN-04", "FN-05", "FN-06", "FN-07", "FN-08", "FN-09", "FN-10",
          "FN-11", "FN-12", "FN-13", "FN-14", "FN-15", "FN-16", "FN-17", "FN-18", "FN-19", "FN-20",
          "FN-21", "FN-22", "FN-23", "FN-24", "FN-25", "FN-26", "FN-27", "FN-28", "FN-29", "FN-30",
          "FN-31", "FN-32", "FN-33", "FN-34", "FN-35", "FN-36", "FN-37", "FN-38", "FN-39", "FN-40",
          "FN-41", "FN-42", "FN-43", "FN-44", "FN-45", "FN-46", "FN-47", "FN-48", "FN-49", "FN-50",
          "FN-51", "FN-52", "FN-90", "FN-91", "FN-92"]


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1360, "height": 900})
        page.on("dialog", lambda d: d.accept() if _dlg["accept"] else d.dismiss())
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
    print("── FN coverage (55) ──")
    for c in ALL_FN:
        mark = "PASS" if covered.get(c) else ("FAIL" if c in have_case else "MISSING")
        if mark != "PASS":
            print(f"  {c}: {mark}")
    if missing:
        print("  ! FN ที่ไม่มีเคส:", ", ".join(missing))
    if failed_fn:
        print("  ! FN ที่มีเคสแต่ยังตก:", ", ".join(failed_fn))
    print()
    print(f"FN ครอบ {len(passed_fn)}/55 · เคสรวม {total} · ผ่าน {ok}/{total}")
    sys.exit(0 if ok == total and len(passed_fn) == 55 and not suite.console_errors else 1)


if __name__ == "__main__":
    main()
