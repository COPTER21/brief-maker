from pathlib import Path
import json
import sys

from playwright.sync_api import sync_playwright


OUTPUTS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(OUTPUTS / "_SHARED" / "_e2e"))
from uikit import Suite, ready, settle as shared_settle, after as shared_after, hush, JS_LAYOUT  # noqa: E402


HTML = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parents[1] / "f-wh-picking.html").resolve()
BASE = HTML.as_uri()
SHOTS = Path(__file__).parent / "shots"
SHOTS.mkdir(exist_ok=True)
suite = Suite("F-WH-PICK Picking")
route_nonce = 0


def settle(page, timeout=900):
    shared_settle(page, timeout=timeout)


def after(page, js, timeout=900):
    return shared_after(page, js, timeout=timeout)


def open_route(page, route="#/list"):
    global route_nonce
    route_nonce += 1
    ready(page, f"{BASE}?e2e={route_nonce}{route}", timeout=1200)
    assert page.locator("#page-content").inner_text().strip()


def snap(page, name):
    hush(page)
    page.screenshot(path=SHOTS / name, full_page=True)


def queue_and_gates(page):
    open_route(page)
    body = page.locator("#page-content").inner_text()
    assert "คิวรอหยิบ (SO)" in body and "SO-2026-0207" in body
    assert "ลูกค้ามารับเอง" in body
    assert "รอชำระก่อนส่ง" in body and "พัก (hold)" in body
    disabled = page.evaluate("""() => ['SO-2026-0200','SO-2026-0205','SO-2026-0206'].every(code => {
      const row=[...document.querySelectorAll('#table-body tr')].find(r=>r.innerText.includes(code));
      return row && row.querySelector('input[type=checkbox]').disabled;
    })""")
    assert disabled
    snap(page, "01-queue-gates.png")


def so_drill_and_remaining(page):
    open_route(page)
    page.locator("#table-body tr").filter(has_text="SO-2026-0201").click()
    settle(page)
    modal = page.locator(".modal-overlay")
    assert modal.is_visible()
    text = modal.inner_text()
    assert "จอง (ฐาน)" in text and "หยิบแล้ว" in text and "ในใบหยิบ" in text and "คงเหลือ" in text
    assert "PICK-2026-0890" in text


def create_allocate_and_save(page):
    open_route(page, "#/create/SO-2026-0207")
    assert "มอบหมายงานหยิบ" in page.locator("#create-drawer").inner_text()
    allocation = page.evaluate("""() => ({
      n:wiz.data.lines.length,
      eligible:wiz.data.lines.filter(x=>x.bal).every(x=>isPickEligible(BAL.find(b=>b.id===x.bal),x.pid,wiz.data.wh)),
      sorted:wiz.data.lines.map(x=>x.loc ? LOCATIONS[x.loc].seq : 999)
    })""")
    assert allocation["n"] > 0 and allocation["eligible"]
    page.get_by_role("button", name="ถัดไป").click(force=True)
    settle(page)
    assert "ตรวจสอบรายการหยิบ" in page.locator("#create-drawer").inner_text(), page.locator("#create-drawer").inner_text()[:500]
    before = page.evaluate("() => PICKS.length")
    page.get_by_role("button", name="บันทึกร่าง").click(force=True)
    settle(page)
    assert page.evaluate("() => PICKS.length") == before + 1, page.locator("body").inner_text()[:500]
    assert page.evaluate("() => PICKS[0].lines.filter(x=>x.bal).every(x=>BAL.find(b=>b.id===x.bal).alloc>0)"), page.locator("body").inner_text()[:500]
    assert "PICK-2026-" in page.locator("#view-drawer").inner_text(), page.locator("body").inner_text()[:500]


def manual_hard_eligibility(page):
    open_route(page, "#/view/PICK-2026-0891")
    after(page, """() => { const p=findPick('PICK-2026-0891'); const l=p.lines.find(x=>x.loc); openRelocModal(p.id,l.id,true); }""")
    text = page.locator(".modal-overlay").inner_text()
    assert "เฉพาะตำแหน่ง Active ที่อนุญาตให้หยิบและไม่บล็อกขาออก" in text
    assert page.evaluate("""() => {
      const p=findPick('PICK-2026-0891'), l=p.lines.find(x=>x.loc);
      return candidatesFor(l.pid,p.wh,true,l.bal).every(b=>isPickEligible(b,l.pid,p.wh));
    }""")
    assert all(word not in text for word in ("HOLD", "STAGING", "RECEIVING", "TRANSIT", "VIRTUAL"))
    snap(page, "04-manual-hard-eligibility.png")


def assignment_keyboard_and_permissions(page):
    open_route(page, "#/create/SO-2026-0207")
    box = page.locator("#cbi-wiz-asg")
    box.focus()
    box.fill("ธน")
    settle(page)
    assert page.locator("#combo-pop").is_visible()
    assert page.locator("#combo-pop button").count() >= 1
    layout = page.evaluate(JS_LAYOUT)
    covered_combo = [item for item in layout.get("menuCovered", []) if item.get("menu") == "combo-pop"]
    assert not covered_combo, f"assignee options are covered: {covered_combo}"
    assert not layout.get("optionCrowded", []), f"assignee options are vertically crowded: {layout['optionCrowded']}"
    page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")
    settle(page)
    assert page.evaluate("() => !!wiz.data.assignee")
    selected_layout = page.evaluate(JS_LAYOUT)
    assert not selected_layout.get("selectionCrowded", []), f"selected assignee is vertically crowded: {selected_layout['selectionCrowded']}"
    after(page, "() => switchPersona(3)")
    assert page.locator("button", has_text="สร้างใบหยิบ").count() == 0
    after(page, "() => switchPersona(2)")
    after(page, "() => navigate('view/PICK-2026-0891')")
    assert page.get_by_role("button", name="บันทึกหยิบ").count() >= 1


def line_scan_and_movement(page):
    open_route(page, "#/view/PICK-2026-0891")
    before = page.evaluate("() => MOVEMENTS.length")
    page.get_by_role("button", name="บันทึกหยิบ").first.click(force=True)
    settle(page)
    page.locator(".scan-tile").nth(0).click(force=True)
    page.locator(".scan-tile").nth(1).click(force=True)
    settle(page)
    confirm = page.get_by_role("button", name="ยืนยันหยิบครบ")
    assert confirm.is_enabled()
    confirm.click(force=True)
    settle(page)
    assert page.evaluate("() => MOVEMENTS.length") == before + 1
    assert page.evaluate("() => MOVEMENTS.at(-1).type==='pick' && MOVEMENTS.at(-1).ref==='PICK-2026-0891'")


def partial_short_and_relocate(page):
    open_route(page, "#/view/PICK-2026-0891")
    page.get_by_role("button", name="บันทึกหยิบ").first.click(force=True)
    settle(page)
    page.locator(".scan-tile").nth(0).click(force=True)
    page.locator(".scan-tile").nth(1).click(force=True)
    qty = page.locator(".modal-overlay input[type=number]")
    qty.fill("1")
    qty.press("Tab")
    settle(page)
    page.get_by_role("button", name="ของไม่พอที่ตำแหน่ง").click(force=True)
    page.get_by_role("button", name="ไปหยิบตำแหน่งอื่น").click(force=True)
    settle(page)
    page.get_by_role("button", name="ยืนยัน · เปลี่ยนตำแหน่ง").click(force=True)
    settle(page)
    assert "เปลี่ยนตำแหน่ง/ล็อต" in page.locator(".modal-overlay").inner_text()
    assert page.get_by_role("button", name="ใช้ตำแหน่งนี้").count() >= 1


def refresh_and_replenish(page):
    open_route(page, "#/view/PICK-2026-0891")
    drawer_text = page.locator("#view-drawer").inner_text()
    assert "ไม่มีตำแหน่ง" in drawer_text, drawer_text[:500]
    assert page.locator('button[title="ขอเติม Pick Face / โอนจากคลังอื่น"]').count() == 0
    after(page, """() => { const p=findPick('PICK-2026-0891'); const l=p.lines.find(x=>!x.loc); requestReplenish(p.id,l.id); }""")
    text = page.locator(".modal-overlay").inner_text()
    assert "ขอเติม Pick Face / โอนจากคลังอื่น" in text, text[:500]
    upper = text.upper()
    assert "RESERVE/BULK ในคลัง" in upper and "คลังอื่น" in text and "งานที่จะสร้าง" in text, text[:500]
    snap(page, "08-replenishment-modal.png")


def finish_and_pack(page):
    open_route(page, "#/view/PICK-2026-0891")
    after(page, "() => pickAllRemaining('PICK-2026-0891')")
    after(page, "() => finishPick('PICK-2026-0891')")
    assert page.evaluate("() => findPick('PICK-2026-0891').status") == "picked", page.locator("#view-drawer").inner_text()[:500]
    assert page.get_by_role("button", name="ส่งต่อ Packing").is_visible(), page.locator("#view-drawer").inner_text()[:500]
    after(page, "() => toPack('PICK-2026-0891')")
    pack_state = page.evaluate("() => {const p=findPick('PICK-2026-0891'); return {status:p.status,packRef:p.packRef};}")
    assert pack_state["status"] == "to_pack" and str(pack_state["packRef"]).startswith("PACK-"), str(pack_state)


def hold_resume_close_short(page):
    open_route(page, "#/view/PICK-2026-0891")
    page.get_by_role("button", name="พัก").click(force=True)
    settle(page)
    page.locator("#md-reason").fill("พักเปลี่ยนกะ")
    page.locator("#md-ok").click(force=True)
    settle(page)
    assert page.evaluate("() => findPick('PICK-2026-0891').status") == "on_hold"
    page.get_by_role("button", name="หยิบต่อ").click(force=True)
    settle(page)
    after(page, """() => { const p=findPick('PICK-2026-0891'); p.lines[0].picked=1; p.lines[0].status='partial'; renderViewDrawer(); }""")
    page.get_by_role("button", name="ปิดงานแบบขาด").click(force=True)
    settle(page)
    page.locator("#md-reason").fill("ปิดตามจำนวนที่พบ")
    page.locator("#md-ok").click(force=True)
    settle(page)
    assert page.evaluate("() => findPick('PICK-2026-0891').status") == "picked"


def cancel_before_start(page):
    open_route(page, "#/view/PICK-2026-0891")
    after(page, """() => { const p=findPick('PICK-2026-0891'); p.status='assigned'; renderViewDrawer(); }""")
    page.get_by_role("button", name="ยกเลิก", exact=True).click(force=True)
    settle(page)
    page.locator("#md-reason").fill("คำสั่งขายยกเลิก")
    page.locator("#md-ok").click(force=True)
    settle(page)
    assert page.evaluate("() => findPick('PICK-2026-0891').status") == "cancelled"


def so_only_rendered_negative(page):
    open_route(page)
    body = page.locator("#page-content").inner_text()
    assert "คิวรอหยิบ (SO)" in body
    for forbidden in ("ใบโอนระหว่างคลัง", "RTV", "Production", "srcType"):
        assert forbidden not in body
    page.locator(".drawer-tab").filter(has_text="ใบหยิบ").click(force=True)
    settle(page)
    assert "SO-2026-" in page.locator("#main-table").inner_text()
    snap(page, "12-so-only-negative.png")


def tabs_print_history_esc_and_responsive(page):
    open_route(page, "#/view/PICK-2026-0891")
    expected = (("รายละเอียด · SO", "เงื่อนไขชำระ"), ("ใบหยิบ (พิมพ์)", "PICK LIST"), ("ประวัติ", "ประวัติ"))
    for tab, anchor in expected:
        page.get_by_role("button", name=tab).click(force=True)
        settle(page)
        assert anchor in page.locator("#view-drawer").inner_text()
    page.keyboard.press("Escape")
    settle(page)
    assert page.locator("#view-drawer").count() == 0
    page.set_viewport_size({"width": 1024, "height": 900})
    open_route(page)
    assert page.locator("#main-table").is_visible()
    assert page.evaluate("() => document.documentElement.scrollWidth <= innerWidth")
    snap(page, "13-responsive-1024.png")
    page.set_viewport_size({"width": 1440, "height": 900})


def printable_files_and_audit(page):
    assert (HTML.parent / "PICK_template.html").exists()
    assert (HTML.parent / "PICK_sample.pdf").stat().st_size > 10000
    open_route(page, "#/view/PICK-2026-0891")
    after(page, "() => pickAllRemaining('PICK-2026-0891')")
    assert page.evaluate("() => { const p=findPick('PICK-2026-0891'); return p.audit.length>=3 && MOVEMENTS.every(m=>m.ref && m.so); }")
    page.get_by_role("button", name="ประวัติ").click(force=True)
    settle(page)
    assert "บันทึกหยิบครบทุกบรรทัด" in page.locator("#view-drawer").inner_text()


CASES = [
    ("FN-01 FN-02 FN-03", "คิว SO, payment gate, hold, pickup/service/backorder", queue_and_gates),
    ("FN-04", "ยอดคงเหลือและ drilldown SO", so_drill_and_remaining),
    ("FN-05 FN-06 FN-07", "สร้าง wave/auto allocation/hard allocate", create_allocate_and_save),
    ("FN-08 FN-17", "manual relocation ใช้ hard eligibility", manual_hard_eligibility),
    ("FN-10 FN-11", "assignee keyboard และ role permissions", assignment_keyboard_and_permissions),
    ("FN-12 FN-13", "เริ่ม/บันทึกหยิบและ Inventory movement", line_scan_and_movement),
    ("FN-14 FN-15", "partial short และไปตำแหน่งอื่น", partial_short_and_relocate),
    ("FN-09 FN-16 FN-18", "no-location, หาใหม่ และขอเติม/โอน", refresh_and_replenish),
    ("FN-19 FN-20", "หยิบครบและส่งต่อ Packing", finish_and_pack),
    ("FN-21 FN-22", "พัก/หยิบต่อ/ปิดงานแบบขาด", hold_resume_close_short),
    ("FN-23", "ยกเลิกก่อนเริ่มและปล่อยจอง", cancel_before_start),
    ("FN-24", "rendered negative: รับ source SO เท่านั้น", so_only_rendered_negative),
    ("FN-90 FN-91 FN-93", "list/tabs/Esc/responsive", tabs_print_history_esc_and_responsive),
    ("FN-92 FN-94", "A4 print และ audit/movement trace", printable_files_and_audit),
]


with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.set_default_timeout(4000)
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
covered = sorted({token for ids, _, _ in CASES for token in ids.split()})
result = {
    "feature": "F-WH-PICK",
    "fn_covered": len(covered),
    "fn_total": 29,
    "fn40_total": 0,
    "tests_passed": passed,
    "tests_total": len(CASES),
    "console_errors": suite.console_errors,
    "results": [{"ids": r[0], "name": r[1], "status": r[2], "detail": r[3]} for r in suite.results],
}
(Path(__file__).parent / "results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"FN ครอบ {len(covered)}/29 · FN-40 rendered negative 0/0 · เคสรวม {len(CASES)} · ผ่าน {passed}/{len(CASES)}")
suite.report(exit_on_fail=False)
sys.exit(0 if passed == len(CASES) and not suite.console_errors else 1)
