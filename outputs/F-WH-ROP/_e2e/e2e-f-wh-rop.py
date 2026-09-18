from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "outputs" / "_SHARED" / "_e2e"))

from playwright.sync_api import sync_playwright
from uikit import Suite, ready, settle, hush, after


HTML = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "outputs" / "F-WH-ROP" / "F-WH-ROP.html").resolve()
URL = HTML.as_uri()
SHOTS = HTML.parent / "_shots"
SHOTS.mkdir(exist_ok=True)


def main():
    suite = Suite("F-WH-ROP Reorder Point")
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        suite.watch(page)

        def reset(route="records"):
            page.goto("about:blank")
            ready(page, URL + "#/" + route)

        def fn01():
            reset("records")
            assert page.locator("#tbody tr").count() == 30, f"rows={page.locator('#tbody tr').count()}"
            page.locator("#search").fill("ITEM-101")
            settle(page)
            assert page.locator("#tbody tr").count() == 2
            page.locator("#thead th").first.click()
            settle(page)
            assert "แสดง 2 จาก 30 รายการ" in page.locator("#tableFoot").inner_text()

        def fn02():
            reset("records")
            page.locator("#tbody tr").first.click()
            page.get_by_role("button", name="แก้ไขนโยบาย").click()
            settle(page)
            assert page.locator("#overlay-root .combo-menu:visible").count() == 0, "dropdown ต้องไม่เปิดเอง"
            page.locator("#ropSafety").fill("11")
            page.locator("#ropMin").fill("10")
            page.get_by_role("button", name="บันทึก").click()
            assert "ต้องไม่มากกว่าค่าขั้นต่ำ" in page.locator("#ropSafetyError").inner_text()
            assert page.locator("#ropSafety").get_attribute("aria-invalid") == "true"
            hush(page)
            page.screenshot(path=str(SHOTS / "validation-field.png"), full_page=False)
            page.locator("#ropSafety").fill("5")
            page.locator("#ropLeadTime").fill("7")
            page.locator("#ropPackSize").fill("12")
            page.locator("#ropVendor").fill("VEND-002")
            page.locator("#ropVendorMenu .combo-option", has_text="VEND-002").click()
            page.get_by_role("button", name="บันทึก").click()
            settle(page)
            assert not page.locator("#drawer").evaluate("el => el.classList.contains('open')")
            assert page.locator("#overlay-root .combo-menu").count() == 0, "ปิด Drawer แล้วต้องล้าง dropdown portal"
            preferred = page.evaluate("() => ropLatestPolicies().find(x => x.item === 'ITEM-101' && x.warehouse === 'WH-01').preferredVendor")
            assert preferred == "VEND-002"

        def fn03():
            reset()
            data = page.evaluate("""() => ({
              a: ropPolicyActive('ITEM-101','WH-01'),
              b: ropPolicyActive('ITEM-101','WH-02')
            })""")
            assert data["a"]["min"] == 10
            assert data["b"]["min"] == 25
            assert data["a"]["leadTime"] == 7
            assert data["b"]["leadTime"] == 10

        def fn04():
            reset("history")
            out = page.evaluate("""() => {
              const result = ropEvaluatePair('ITEM-101','WH-01');
              const snapshot = {atp:16, adu:2, onOrder:0, asOf:'2026-09-14T09:00:00Z', source:'F009'};
              const policy = ropPolicyActive('ITEM-101','WH-01');
              const originalSafety = policy.safety;
              policy.safety = 0;
              const withoutSafety = ropEvaluatePair('ITEM-101','WH-01',snapshot);
              policy.safety = 5;
              const withSafety = ropEvaluatePair('ITEM-101','WH-01',snapshot);
              policy.safety = originalSafety;
              return {result, withoutSafety, withSafety};
            }""")
            result = out["result"]
            assert result["atp"] == 8
            assert result["onOrder"] == 0
            assert result["adu"] == 2
            assert result["rop"] == 19
            assert result["raw"] == 27
            assert result["qty"] == 36
            assert result["reason"] == "ATP 8 < จุดสั่งเติม 19 (safety 5 + ADU 2 × lead 7)"
            assert result["snapshot"]["source"] == "F009"
            assert out["withoutSafety"]["triggered"] is False
            assert out["withoutSafety"]["qty"] == 0
            assert out["withSafety"]["triggered"] is True
            assert out["withSafety"]["qty"] == 24
            statuses = set(page.locator("#tbody .pill").all_inner_texts())
            assert {"ต่ำกว่าจุด", "ใกล้จุด", "ปกติ"}.issubset(statuses), statuses
            assert page.locator("#stats").get_by_text("ใกล้จุด", exact=True).count() == 1

        def fn05():
            reset("history")
            assert page.locator("#tbody tr").count() == 30, f"suggestion rows={page.locator('#tbody tr').count()}"
            no_policy = page.evaluate("() => ropEvaluatePair('ITEM-116','WH-01').code")
            assert no_policy == "NO_POLICY", f"no_policy={no_policy}"
            page.get_by_role("button", name="ตรวจคู่สินค้า×คลัง").click()
            page.locator("#ropItem").click()
            assert page.locator("#ropItemMenu").is_visible(), "รายการสินค้าต้องเปิดเหนือ Drawer"
            assert page.locator("#ropItemMenu .combo-option:visible").count() == 16
            page.locator("#ropItemMenu .combo-option", has_text="ITEM-116").click()
            assert page.locator("#ropItem").input_value() == "ITEM-116 · สินค้า 116"
            page.locator("#ropWarehouse").click()
            page.locator("#ropWarehouseMenu .combo-option", has_text="WH-01").click()
            page.get_by_role("button", name="ตรวจนโยบาย").click()
            result_text = page.locator("#ropCheckResult").inner_text()
            assert "ยังไม่มีนโยบายเติมสินค้า" in result_text
            assert "ITEM-116 · สินค้า 116" in result_text
            assert "WH-01 · คลังหลัก" in result_text
            page.screenshot(path=str(SHOTS / "no-policy-result.png"), full_page=False)
            page.get_by_role("button", name="เพิ่มนโยบาย").click()
            assert page.locator("#drawerTitle").inner_text() == "เพิ่มนโยบาย"
            assert page.locator("#ropItem").input_value() == "ITEM-116 · สินค้า 116"
            assert page.locator("#ropWarehouse").input_value() == "WH-01 · คลังหลัก"
            page.locator("#drawerFooter").get_by_role("button", name="ยกเลิก").click()
            page.locator("#tbody tr").first.click()
            settle(page)
            drawer_text = page.locator("#drawer").text_content() or ""
            assert "ATP จาก F009" in drawer_text, f"drawer={drawer_text[:180]}"
            hush(page)
            page.screenshot(path=str(SHOTS / "suggestion-drawer.png"), full_page=False)

        def fn06():
            reset("history")
            page.locator("#tbody tr").first.click()
            page.get_by_role("button", name="ส่งแจ้งเตือน").click()
            after(page, "() => !state._busy")
            assert page.locator("#toast").inner_text() == "ส่งแจ้งเตือนแล้ว"
            assert page.locator("#ropActionResult").inner_text() == ""
            page.get_by_role("button", name="ส่งแจ้งเตือน").click()
            after(page, "() => !state._busy")
            assert page.locator("#toast").inner_text() == "รายการนี้แจ้งเตือนไปแล้ว"
            assert page.locator("#ropActionResult").inner_text() == ""
            out = page.evaluate("""() => ropEvents.find(x => x.kind === 'notification.emitted').envelope""")
            assert out["eventType"] == "reorder_point.triggered"
            assert out["atp"] == 8

        def fn07():
            reset("history")
            page.locator("#tbody tr").first.click()
            page.get_by_role("button", name="สร้าง PR Draft ของคลังนี้").click()
            after(page, "() => !state._busy")
            assert page.locator("#toast").inner_text() == "สร้าง PR Draft แล้ว · 2 รายการ"
            assert page.locator("#ropActionResult").inner_text() == ""
            page.get_by_role("button", name="สร้าง PR Draft ของคลังนี้").click()
            after(page, "() => !state._busy")
            assert page.locator("#toast").inner_text() == "คลังนี้มี PR Draft ของรอบนี้แล้ว"
            assert page.locator("#ropActionResult").inner_text() == ""
            out = page.evaluate("""() => {
              const event = ropEvents.find(x => x.kind === 'pr.draft.created');
              const replay = ropPreparePR(ropEvaluatePair('ITEM-101','WH-01'));
              return {ack:event.ack, replay};
            }""")
            first = out["ack"]
            assert first["status"] == "draft"
            assert first["submitted"] is False
            assert first["payload"]["warehouse"] == "WH-01"
            assert len(first["payload"]["lines"]) == 2
            assert all(line["qty"] > 0 for line in first["payload"]["lines"])
            assert first["payload"]["vendor_suggests"] == ["VEND-001"]
            assert out["replay"]["replay"] is True

        def fn08():
            reset("history")
            page.get_by_role("button", name="รันตรวจตอนนี้").click()
            assert page.get_by_role("button", name="กำลังตรวจ…").is_disabled()
            after(page, "() => !state._busy")
            first_count = page.evaluate("() => ropEvents.length")
            page.get_by_role("button", name="รันตรวจตอนนี้").click()
            after(page, "() => !state._busy")
            second_count = page.evaluate("() => ropEvents.length")
            assert second_count == first_count, f"events {first_count} -> {second_count}"
            page.evaluate("""() => {
              const e = ropEvaluatePair('ITEM-101','WH-01');
              ropNcCandidate(e); ropPreparePR(e);
              ropSavePolicy('ITEM-101','WH-01',10,30,5,7,30,12,'2026-09-17');
            }""")
            page.evaluate("location.hash='#/settings'")
            settle(page)
            assert page.locator("#tbody tr").count() >= 3
            visible_history = page.locator("#mainPanel").inner_text()
            assert "notification.emitted" not in visible_history
            assert "reorder_point.triggered" not in visible_history
            assert "policy.saved" not in visible_history
            assert "POL-" not in visible_history
            assert "ส่งแจ้งเตือน" in visible_history
            assert "รายละเอียด" in page.locator("#thead").inner_text()
            assert "อ้างอิง" not in page.locator("#thead").inner_text()
            hush(page)
            page.screenshot(path=str(SHOTS / "history-human.png"), full_page=False)
            page.locator("#tbody tr", has_text="สร้าง PR Draft").click()
            settle(page)
            drawer_text = page.locator("#drawer").text_content() or ""
            assert "เลขที่ PR Draft" in drawer_text, f"drawer={drawer_text[:180]}"
            assert "รอตรวจสอบและส่งอนุมัติ" in drawer_text
            footer = page.locator("#drawerFooter").inner_text()
            assert "แก้ไข" not in footer and "ลบ" not in footer
            page.add_style_tag(content=".demo-only{display:none!important}")
            assert page.locator(".demo-only:visible").count() == 0
            assert "DEMO" not in page.locator("body").inner_text()
            assert page.evaluate("() => document.documentElement.scrollWidth <= innerWidth")

        suite.check("FN-01", "รายการ กรอง เรียง และจำนวนจากข้อมูลจริง", fn01)
        suite.check("FN-02", "สร้างรุ่นนโยบายและบล็อกค่าผิด", fn02)
        suite.check("FN-03", "เลือกนโยบายตามสินค้า×คลังและวันที่", fn03)
        suite.check("FN-04", "ATP/On-Order/ADU/Lead Time และปัด Pack Size", fn04)
        suite.check("FN-05", "คำแนะนำและสถานะไม่มีนโยบาย", fn05)
        suite.check("FN-06", "ส่งแจ้งเตือนโดยไม่แสดงรหัสระบบและไม่หัก hold ซ้ำ", fn06)
        suite.check("FN-07", "รวม PR Draft ต่อคลังและไม่ auto-submit", fn07)
        suite.check("FN-08", "ประวัติ append-only", fn08)
        browser.close()

    print("FN ครอบ 8/8 · FN-40 0/0 · เคสรวม 8")
    suite.report()


if __name__ == "__main__":
    main()
