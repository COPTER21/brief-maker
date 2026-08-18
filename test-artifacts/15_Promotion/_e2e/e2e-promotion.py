#!/usr/bin/env python3
"""Feature E2E for the seed-based Promotion prototype."""

import pathlib
import sys

from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[2] / "_SHARED" / "_e2e"))
from uikit import Suite, ready, settle, after, n  # noqa: E402


def must(value, message):
    if not value:
        raise AssertionError(message)
    return ""


def body(pg):
    return pg.locator("body").inner_text()


def has(pg, *words):
    text = body(pg)
    return all(word in text for word in words)


def source_has(pg, *parts):
    source = "\n".join(node.text_content() or "" for node in pg.locator("script").all())
    return all(part in source for part in parts)


def reset(pg, url):
    pg.reload()
    pg.wait_for_load_state("load")
    settle(pg)


def open_create(pg):
    pg.get_by_role("button", name="สร้างโปรโมชัน").click()
    settle(pg)


def open_detail(pg, code):
    after(pg, f"() => openView('{code}')")


def step_two(pg, promo_type):
    open_create(pg)
    pg.get_by_role("button", name=promo_type, exact=True).click()
    pg.locator("#drawerEl input").first.fill("โปรโมชันทดสอบ")
    pg.get_by_role("button", name="ถัดไป").click()
    settle(pg)


def check_list(pg):
    must(n(pg, ".page-tabs .tab") == 7, "แท็บสถานะต้องมี 7 แท็บ")
    must(n(pg, ".stats") == 0, "พบ KPI card ที่ซ้ำกับแท็บ")
    must(n(pg, ".ta-list tbody tr") == 7, "รายการ mock ต้องมี 7 แถว")
    pg.locator(".search-box input").fill("WELCOME100")
    settle(pg)
    must(n(pg, ".ta-list tbody tr") == 1 and has(pg, "PM-2026-015"), "ค้นหาคูปองไม่พบรายการ")
    after(pg, "() => resetF()")
    pg.locator(".filter-bar select").first.select_option("FREE_GOODS")
    settle(pg)
    must(n(pg, ".ta-list tbody tr") == 1, "กรองชนิดไม่ทำงาน")
    after(pg, "() => resetF()")
    scope_filter = pg.locator("select[aria-label='กรองขอบเขต']")
    must(scope_filter.locator("option").count() == 4, "ตัวกรองขอบเขตต้องมี ทุกขอบเขต/ทุกลูกค้า/กลุ่ม/ช่องทาง")
    scope_filter.select_option("all")
    settle(pg)
    must(pg.evaluate("() => state.scope") == "all" and n(pg, ".ta-list tbody tr") == 2, "กรองทุกลูกค้าเลือกไม่ได้")
    scope_filter = pg.locator("select[aria-label='กรองขอบเขต']")
    scope_filter.select_option("group")
    settle(pg)
    must(pg.evaluate("() => state.scope") == "group" and n(pg, ".ta-list tbody tr") >= 1, "กรองกลุ่มลูกค้าเลือกไม่ได้")
    pg.locator("select[aria-label='กรองขอบเขต']").select_option("channel")
    settle(pg)
    must(pg.evaluate("() => state.scope") == "channel" and n(pg, ".ta-list tbody tr") >= 1, "กรองช่องทางเลือกไม่ได้")
    pg.locator("select[aria-label='กรองขอบเขต']").select_option("any")
    settle(pg)
    must(pg.evaluate("() => state.scope") == "any" and n(pg, ".ta-list tbody tr") == 7, "กลับทุกขอบเขตไม่ได้")
    pg.locator(".sortable").first.click()
    settle(pg)
    must("is-sorted" in (pg.locator(".sortable").first.get_attribute("class") or ""), "sort ไม่ทำงาน")
    after(pg, "() => { state.q='ไม่พบแน่นอน'; render(); }")
    must(has(pg, "ไม่พบรายการที่ค้นหา", "ล้างตัวกรอง"), "empty state ไม่ครบ")
    return ""


def check_create_shell(pg):
    open_create(pg)
    must(n(pg, ".d-stepper .stepper-item") == 3, "ขั้นสร้างต้องมี 3 ขั้น")
    must(n(pg, "#drawerEl .seg-b") >= 7, "ตัวเลือกชนิด/ขอบเขตไม่ครบ")
    must(has(pg, "ส่วนลดสินค้า", "ซื้อ X แถม Y", "ยอดใบถึงเกณฑ์", "ชุดราคาพิเศษ"), "ชนิดโปรโมชันไม่ครบ")
    return ""


def check_scope(pg):
    pg.get_by_role("button", name="กลุ่มลูกค้า", exact=True).click()
    settle(pg)
    must(n(pg, "#cbi-scoperef") == 1 and has(pg, "เลือกได้หลายรายการ"), "multi-pick กลุ่มลูกค้าไม่แสดง")
    must(n(pg, "#drawerEl button:has-text('ลูกค้าเฉพาะราย')") == 0, "มี scope ลูกค้าเฉพาะรายเกินขอบเขต")
    pg.get_by_role("button", name="ช่องทางการขาย", exact=True).click()
    settle(pg)
    must(n(pg, "#cbi-scoperef") == 1, "multi-pick ช่องทางไม่แสดง")
    return ""


def check_invalid(pg):
    open_create(pg)
    pg.locator("#drawerEl input").first.fill("ทดสอบ validation")
    pg.locator("#drawerEl input[type=date]").first.fill("2026-08-15")
    pg.locator("#drawerEl input[placeholder='เช่น WELCOME100']").fill("!")
    pg.get_by_role("button", name="ถัดไป").click()
    settle(pg)
    must(n(pg, "#drawerEl .is-error") >= 2 and has(pg, "วันเริ่มต้องไม่ย้อนหลัง", "โค้ด 3–20 ตัว"), "validation ไม่ block ข้อมูลผิด")
    return ""


def check_submit_modal(pg):
    open_detail(pg, "PM-2026-015")
    pg.get_by_role("button", name="ส่งอนุมัติ", exact=True).click()
    settle(pg)
    must(n(pg, ".modal .slot-row") == 2, "DOA slot ต้องมี 2 ขั้น")
    must(n(pg, ".modal .dw-summary .dg") == 4, "สรุปก่อนส่งต้องมี 4 ช่อง")
    pg.locator(".modal").get_by_role("button", name="ส่งอนุมัติ", exact=True).click()
    settle(pg)
    must(n(pg, ".modal .slot-row.is-err") == 2, "ไม่เลือกผู้อนุมัติต้องส่งไม่ได้")
    return ""


def check_pending(pg):
    open_detail(pg, "PM-2026-014")
    must(n(pg, "#drawerEl button:has-text('แก้ไข')") == 0, "รออนุมัติยังแก้ไขได้")
    pg.get_by_role("button", name="การอนุมัติ & ข้อมูล").click()
    settle(pg)
    must(has(pg, "DOA-SALES-PROMO", "มานพ ขายเก่ง", "ศิริพร หัวหน้า BU"), "สายอนุมัติที่ freeze แสดงไม่ครบ")
    return ""


def check_reject(pg):
    open_detail(pg, "PM-2026-014")
    pg.locator("#drawerEl").get_by_role("button", name="ไม่อนุมัติ", exact=True).click()
    settle(pg)
    pg.locator(".modal").get_by_role("button", name="ไม่อนุมัติ", exact=True).click()
    settle(pg)
    must(n(pg, "#fld-reason.is-error") == 1, "ไม่อนุมัติโดยไม่มีเหตุผลยังผ่าน")
    pg.locator("#md-reason").fill("ข้อมูลไม่ครบ")
    pg.locator(".modal").get_by_role("button", name="ไม่อนุมัติ", exact=True).click()
    settle(pg)
    must(pg.evaluate("() => findP('PM-2026-014').status") == "draft", "ไม่อนุมัติแล้วไม่กลับร่าง")
    return ""


def check_overlap(pg):
    after(pg, "() => { const p=findP('PM-2026-015'); p.validFrom='2026-08-31'; openView(p.id); }")
    pg.get_by_role("button", name="ส่งอนุมัติ", exact=True).click()
    settle(pg)
    must(has(pg, "ทับซ้อน", "ลำดับ", "ไม่มีการทับ/ยกเลิกโปรฯ เดิมอัตโนมัติ"), "คำเตือนทับซ้อนไม่ครบ")
    must(n(pg, ".ack-row") == 1, "ไม่มีตัวรับทราบการทับซ้อน")
    return ""


def check_copy(pg):
    open_detail(pg, "PM-2026-011")
    pg.get_by_role("button", name="ทำสำเนา", exact=True).click()
    settle(pg)
    copied = pg.evaluate("() => ({name:state.form.name,coupon:state.form.coupon,from:state.form.validFrom,mode:state.drawer.mode})")
    must(copied["name"].endswith("(สำเนา)") and copied["coupon"] == "" and copied["from"] == "2026-08-16" and copied["mode"] == "create", "ทำสำเนาไม่ได้ร่างสะอาด")
    return ""


def check_sim_ui(pg):
    pg.get_by_role("button", name="ทดสอบตะกร้า").click()
    settle(pg)
    must(n(pg, "#drawerEl table tbody tr") >= 4, "ตะกร้า/ของแถมไม่ครบ")
    must(has(pg, "ของแถม", "0.00", "โปรโมชันที่ประเมิน", "ผลจำลองนี้ใช้กติกาเดียวกับใบเสนอราคาและใบสั่งขาย"), "ผลจำลองไม่ครบ")
    must(not has(pg, "ENG candidate:") and not has(pg, "calcPromo(lines, doc)"), "ยังมีข้อความเทคนิคใน simulator")
    coupon = pg.locator("#cbi-sim-coupon")
    coupon.fill("")
    coupon.press_sequentially("WELCOME100")
    must(coupon.input_value() == "WELCOME100" and pg.evaluate("() => document.activeElement && document.activeElement.id") == "cbi-sim-coupon", "ช่องคูปองพิมพ์ต่อเนื่องหรือรักษา focus ไม่ได้")
    qty = pg.locator("#cbi-sim-qty-0")
    qty.fill("")
    qty.press_sequentially("12")
    must(qty.input_value() == "12" and pg.evaluate("() => document.activeElement && document.activeElement.id") == "cbi-sim-qty-0", "ช่องจำนวนพิมพ์ต่อเนื่องหรือรักษา focus ไม่ได้")
    cells = pg.locator(".sim-cart-table tbody tr").first.locator("td")
    product_box = cells.nth(0).bounding_box()
    unit_box = cells.nth(1).bounding_box()
    must(product_box and unit_box and product_box["x"] + product_box["width"] <= unit_box["x"] + 1, "คอลัมน์สินค้าทับคอลัมน์หน่วย")
    pg.locator("#cbi-sim-add").focus()
    settle(pg)
    menu = pg.locator(".cb-menu")
    must(menu.count() == 1 and menu.evaluate("e => e.scrollHeight > e.clientHeight"), "dropdown เพิ่มสินค้าไม่มีพื้นที่ scroll")
    scrolled = menu.evaluate("e => { e.scrollTop = 120; e.dispatchEvent(new Event('scroll')); return e.scrollTop; }")
    must(scrolled > 0, "dropdown เพิ่มสินค้า scroll ไม่ได้")
    before = pg.evaluate("() => state.sim.lines.length")
    after(pg, "() => simLineAdd('FG-5001')")
    must(pg.evaluate("() => state.sim.lines.length") == before + 1, "เพิ่มสินค้าในตะกร้าไม่ทำงาน")
    after(pg, f"() => simLineDel({before})")
    must(pg.evaluate("() => state.sim.lines.length") == before, "ลบสินค้าในตะกร้าไม่ทำงาน")
    return ""


def check_timeline_and_bundle_combo(pg):
    open_detail(pg, "PM-2026-014")
    pg.get_by_role("button", name="การอนุมัติ & ข้อมูล").click()
    settle(pg)
    must(n(pg, "#drawerEl .audit-timeline") == 1 and n(pg, "#drawerEl .audit-timeline .tl-i") == 3, "DOA timeline ไม่ครบ")
    must(n(pg, "#drawerEl .emp-av") >= 2 and has(pg, "ผู้จัดการฝ่ายขาย", "หัวหน้า BU", "มานพ ขายเก่ง", "ศิริพร หัวหน้า BU"), "ตัวตนผู้อนุมัติไม่ครบ")
    aligned = pg.locator("#drawerEl .audit-timeline").evaluate("""e => {
      const line = getComputedStyle(e, '::before');
      const x = e.getBoundingClientRect().left + parseFloat(line.left) + parseFloat(line.width) / 2;
      return [...e.querySelectorAll('.tl-i')].every(i => {
        const dot = getComputedStyle(i, '::before');
        const r = i.getBoundingClientRect();
        const dx = r.left + parseFloat(dot.left) + parseFloat(dot.width) / 2;
        return Math.abs(dx - x) <= 1;
      });
    }""")
    must(aligned, "เส้น timeline ไม่ตรงกึ่งกลางจุด")
    after(pg, "() => { closeDrawer(); openCreate(); fSetType('BUNDLE'); state.form.name='ทดสอบ bundle'; nextStep(); }")
    combo_input = pg.locator("#cbi-r-item-0")
    must(combo_input.count() == 1 and float(combo_input.evaluate("e => parseFloat(getComputedStyle(e).paddingLeft)")) >= 34, "search icon ในช่องสินค้า bundle ทับข้อความ")
    return ""


def calc(pg, expression):
    return pg.evaluate(expression)


def check_usage(pg):
    open_detail(pg, "PM-2026-012")
    pg.get_by_role("button", name="การใช้งาน & งบ").click()
    settle(pg)
    must(has(pg, "ใช้ไป", "ส่วนลด/มูลค่าของแถมที่ให้", "ลูกค้าที่ใช้", "เหลืองบ", "ของแถมราคา 0", "ตัดสต๊อก"), "ข้อมูล usage/บัญชีไม่ครบ")
    return ""


def check_pause(pg):
    open_detail(pg, "PM-2026-011")
    after(pg, "() => openModal('pause','PM-2026-011')")
    pg.locator("#md-reason").fill("พักทดสอบ")
    pg.locator(".modal").get_by_role("button", name="ระงับ", exact=True).click()
    settle(pg)
    must(pg.evaluate("() => pStatus(findP('PM-2026-011'))") == "paused", "ระงับไม่เปลี่ยนสถานะ")
    pg.locator("#drawerEl").get_by_role("button", name="เปิดต่อ", exact=True).click()
    settle(pg)
    must(pg.evaluate("() => pStatus(findP('PM-2026-011'))") == "active", "เปิดต่อไม่กลับกำลังใช้")
    return ""


def check_end(pg):
    open_detail(pg, "PM-2026-011")
    after(pg, "() => openModal('end','PM-2026-011')")
    must(n(pg, "#md-eff") == 1, "ปิดก่อนกำหนดไม่มีวันมีผล")
    pg.locator("#md-reason").fill("จบแคมเปญ")
    pg.locator(".modal").get_by_role("button", name="ปิดก่อนกำหนด", exact=True).click()
    settle(pg)
    must(pg.evaluate("() => findP('PM-2026-011').status") == "ended", "ปิดก่อนกำหนดไม่สำเร็จ")
    return ""


def check_cancel(pg):
    open_detail(pg, "PM-2026-015")
    pg.locator("#drawerEl .drawer-footer").get_by_role("button", name="ยกเลิก", exact=True).click()
    settle(pg)
    pg.locator("#md-reason").fill("ยกเลิกการทดสอบ")
    pg.locator(".modal").get_by_role("button", name="ยกเลิก", exact=True).click()
    settle(pg)
    must(pg.evaluate("() => findP('PM-2026-015').status") == "cancelled", "ยกเลิกร่างไม่สำเร็จ")
    return ""


def main():
    html = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else HERE.parents[1] / "Promotion.html").resolve()
    url = html.as_uri() + "#/promotions"
    suite = Suite("Promotion seed — 38 FN")

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        pg = browser.new_page(viewport={"width": 1440, "height": 900})
        suite.watch(pg)
        ready(pg, url)

        suite.check("FN-90", "รายการ แท็บ ค้นหา กรอง sort และ empty", lambda: check_list(pg))
        reset(pg, url)
        suite.check("FN-92", "Export CSV ใช้ผล filtered", lambda: must(source_has(pg, "function exportCsv", "const rows = filtered()"), "CSV ไม่ได้ใช้ filtered()"))
        suite.check("FN-95", "Esc chain และ combobox portal", lambda: must(source_has(pg, "e.key !== 'Escape'", "dd-portal", "renderPortal"), "overlay contract ไม่ครบ"))

        suite.check("FN-01", "สร้าง 3 ขั้นและ 4 ชนิด", lambda: check_create_shell(pg))
        suite.check("FN-02", "คูปอง ลำดับ ซ้อน โควตา งบ GL", lambda: must(has(pg, "คูปองโค้ด", "ลำดับ (น้อยก่อน)", "กติกาซ้อน", "โควตารวม", "งบส่วนลด", "บัญชี GL"), "field ส่วนหัวไม่ครบ"))
        suite.check("FN-03", "ขอบเขตและ multi-pick", lambda: check_scope(pg))
        reset(pg, url)

        suite.check("FN-04", "editor ส่วนลดสินค้า", lambda: (step_two(pg, "ส่วนลดสินค้า"), must(has(pg, "ใช้กับ", "ลด %", "บาท/หน่วยฐาน", "ซื้อขั้นต่ำ"), "editor ส่วนลดไม่ครบ"))[1])
        reset(pg, url)
        suite.check("FN-05", "editor ซื้อ X แถม Y", lambda: (step_two(pg, "ซื้อ X แถม Y"), must(has(pg, "ซื้อสินค้า", "แถมสินค้า", "จำนวนซื้อ", "จำนวนแถม", "ทำซ้ำได้"), "editor ของแถมไม่ครบ"))[1])
        reset(pg, url)
        suite.check("FN-06", "editor ยอดใบหลายขั้น", lambda: (step_two(pg, "ยอดใบถึงเกณฑ์"), calc(pg, "() => state.form.r.tiers.length"), after(pg, "() => tierAdd()"), must(pg.evaluate("() => state.form.r.tiers.length") >= 2 and has(pg, "เพิ่มขั้น"), "เพิ่ม tier ไม่ทำงาน"))[3])
        reset(pg, url)
        suite.check("FN-07", "editor ชุดราคาพิเศษ", lambda: (step_two(pg, "ชุดราคาพิเศษ"), must(has(pg, "สินค้าในชุด", "ราคาชุด", "เพิ่มสินค้าในชุด", "ทุกชุด"), "editor bundle ไม่ครบ"))[1])
        reset(pg, url)
        suite.check("FN-08", "ข้อมูลผิดถูก block", lambda: check_invalid(pg))
        reset(pg, url)

        suite.check("FN-09", "ส่งร่างผ่าน DOA slots", lambda: check_submit_modal(pg))
        reset(pg, url)
        suite.check("FN-10", "freeze หลังส่ง", lambda: check_pending(pg))
        suite.check("FN-11", "ผู้อนุมัติปัจจุบันเห็น action", lambda: must(n(pg, "#drawerEl button:has-text('อนุมัติ')") >= 2, "approval action ไม่ครบ"))
        suite.check("FN-12", "อนุมัติครบเป็น active/scheduled", lambda: must(source_has(pg, "p.status = 'active'", "pStatus(p) === 'active'"), "approval transition ไม่ครบ"))
        reset(pg, url)
        suite.check("FN-13", "ไม่อนุมัติบังคับเหตุผลและกลับร่าง", lambda: check_reject(pg))
        reset(pg, url)
        suite.check("FN-14", "SoD ตัดผู้ใช้ปัจจุบัน", lambda: must(calc(pg, "() => {state.modal={open:true,type:'submit',id:'PM-2026-015',slots:resolveDoa(findP('PM-2026-015')).steps.map(s=>({roles:s.roles,assignee:null}))}; return comboSpec('slot-0').items('').every(e=>e.name!==ME.name)}"), "picker ยังมีผู้ใช้ปัจจุบัน"))

        reset(pg, url)
        suite.check("FN-15", "แจ้งโปรโมชันทับซ้อน", lambda: check_overlap(pg))
        suite.check("FN-16", "ต้องรับทราบและไม่ยกเลิกของเดิม", lambda: must(source_has(pg, "!state.modal.ack", "overlapAck", "ไม่มีการทับ/ยกเลิกโปรฯ เดิมอัตโนมัติ"), "overlap acknowledgement ไม่ครบ"))
        reset(pg, url)
        suite.check("FN-17", "ทำสำเนาเป็นร่างสะอาด", lambda: check_copy(pg))

        reset(pg, url)
        suite.check("FN-19", "ตะกร้าและของแถม 0 บาท", lambda: check_sim_ui(pg))
        suite.check("FN-18", "ส่วนลดบรรทัดและ GL", lambda: must(calc(pg, "() => {const o=calcPromo([{product:'FG-1010',uom:'ขวด',qty:48,unit:22.75,promoAllowed:true}],{customer:'CUST-2026-0021',channel:'SALESREP',date:TODAY_ISO,coupon:''}); return o.applied.some(a=>a.promo.code==='PM-2026-011'&&a.amount>0&&a.gl==='4110-02')}"), "line discount/GL ไม่ถูก"))
        suite.check("FN-20", "threshold ใช้ขั้นสูงสุด", lambda: must(calc(pg, "() => {const o=calcPromo([{product:'FG-5003',uom:'ขวด',qty:500,unit:119,promoAllowed:true}],{customer:'CUST-2026-0060',channel:'ONLINE',date:TODAY_ISO,coupon:''}); return o.applied.some(a=>a.promo.code==='PM-2026-013'&&a.note.includes('50,000'))}"), "threshold ขั้นสูงสุดไม่ติด"))
        suite.check("FN-21", "bundle ใช้ limiting item", lambda: must(calc(pg, "() => {const p=findP('PM-2026-014'),old={status:p.status,from:p.validFrom};p.status='active';p.validFrom=TODAY_ISO;const o=calcPromo([{product:'FG-5003',uom:'ขวด',qty:2,unit:119,promoAllowed:true},{product:'FG-5001',uom:'ก้อน',qty:3,unit:24,promoAllowed:true},{product:'FG-5002',uom:'หลอด',qty:2,unit:65,promoAllowed:true}],{customer:'CUST-2026-0056',channel:'STORE',date:TODAY_ISO,coupon:''});p.status=old.status;p.validFrom=old.from;return o.applied.some(a=>a.promo.code==='PM-2026-014'&&a.note.includes('×2'))}"), "bundle ไม่ใช้จำนวนน้อยสุด"))
        suite.check("FN-22", "coupon ไม่สนตัวพิมพ์และข้ามเมื่อไม่ใส่", lambda: must(calc(pg, "() => {const p=findP('PM-2026-015'),old={status:p.status,from:p.validFrom};p.status='active';p.validFrom=TODAY_ISO;const lines=[{product:'FG-5003',uom:'ขวด',qty:5,unit:119,promoAllowed:true}],doc={customer:'CUST-2026-0060',channel:'ONLINE',date:TODAY_ISO,coupon:'welcome100'};const yes=calcPromo(lines,doc).applied.some(a=>a.promo.code===p.code);doc.coupon='';const no=calcPromo(lines,doc).skipped.some(a=>a.promo.code===p.code&&a.why.includes('ต้องใส่คูปอง'));p.status=old.status;p.validFrom=old.from;return yes&&no}"), "coupon rule ไม่ถูก"))
        suite.check("FN-23", "priority และ exclusive ladder", lambda: must(source_has(pg, "sort((a, b) => a.priority - b.priority", "if (p.exclusive) stopped = true", "ถูกกันโดยโปรโมชัน exclusive"), "priority/exclusive ไม่ครบ"))
        suite.check("FN-24", "TA net price ข้ามส่วนลด", lambda: must(calc(pg, "() => calcPromo([{product:'FG-1010',uom:'ขวด',qty:48,unit:20,promoAllowed:false}],{customer:'CUST-2026-0021',channel:'SALESREP',date:TODAY_ISO,coupon:''}).skipped.some(x=>x.why.includes('ไม่ลดซ้ำ'))"), "TA net price ไม่ถูกข้าม"))
        suite.check("FN-31", "โควตาต่อลูกค้าข้าม", lambda: must(calc(pg, "() => {const p=findP('PM-2026-015'),old={status:p.status,from:p.validFrom};p.status='active';p.validFrom=TODAY_ISO;p.usage.byCust['CUST-2026-0060']=1;const o=calcPromo([{product:'FG-5003',uom:'ขวด',qty:5,unit:119,promoAllowed:true}],{customer:'CUST-2026-0060',channel:'ONLINE',date:TODAY_ISO,coupon:'WELCOME100'});delete p.usage.byCust['CUST-2026-0060'];p.status=old.status;p.validFrom=old.from;return o.skipped.some(x=>x.promo.code===p.code&&x.why.includes('ครบโควตา'))}"), "โควตาต่อลูกค้าไม่ block"))

        reset(pg, url)
        suite.check("FN-25", "การลงบัญชีส่วนลด/ของแถม", lambda: check_usage(pg))
        suite.check("FN-26", "usage และ budget metrics", lambda: must(has(pg, "ใช้ไป", "ส่วนลด/มูลค่าของแถมที่ให้", "ลูกค้าที่ใช้", "เหลืองบ"), "usage metrics ไม่ครบ"))
        suite.check("FN-27", "งบ/โควตาหมดและ 90%", lambda: must(source_has(pg, "งบ/โควตาหมด", "v >= 90", "งบส่วนลดไม่พอ"), "budget guard/เตือนไม่ครบ"))

        reset(pg, url)
        suite.check("FN-28", "ระงับและเปิดต่อ", lambda: check_pause(pg))
        reset(pg, url)
        suite.check("FN-29", "ปิดก่อนกำหนด", lambda: check_end(pg))
        reset(pg, url)
        suite.check("FN-30", "ยกเลิกได้เฉพาะก่อนมีผล", lambda: check_cancel(pg))

        reset(pg, url)
        open_detail(pg, "PM-2026-015")
        suite.check("FN-91", "drawer 4 แท็บและ hero", lambda: must(n(pg, "#drawerEl .dtab") == 4 and n(pg, "#drawerEl .fact-grid .fact") == 6 and has(pg, "ยอดใบถึงเกณฑ์"), "drawer anatomy ไม่ครบ"))
        pg.get_by_role("button", name="ประวัติ (1)").click()
        settle(pg)
        suite.check("FN-94", "audit append-only", lambda: must(n(pg, "#drawerEl .tl-i") >= 1 and n(pg, "#drawerEl button:has-text('ลบประวัติ')") == 0, "audit timeline ไม่ถูก"))
        reset(pg, url)
        suite.check("FN-96", "timeline ผู้อนุมัติและ bundle combobox", lambda: check_timeline_and_bundle_combo(pg))
        suite.check("FN-93", "validation และกัน double submit", lambda: must(source_has(pg, "state.busy", "if (state.busy) return", "disabled"), "double-submit guard ไม่ครบ"))

        browser.close()

    passed = suite.report(exit_on_fail=False)
    total = len(suite.results)
    print(f"FN ครอบ {total}/38 · เคสรวม {total} · ผ่าน {passed}/{total}")
    sys.exit(0 if passed == total == 38 and not suite.console_errors else 1)


if __name__ == "__main__":
    main()
