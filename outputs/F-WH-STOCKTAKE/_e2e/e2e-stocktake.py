#!/usr/bin/env python3
"""E2E · F-WH-STOCKTAKE · WF-01 step 5 — ครอบ FN-01..FN-12."""
from pathlib import Path
import sys

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "outputs" / "_SHARED" / "_e2e"))
from uikit import (  # noqa: E402
    Suite,
    ready,
    settle,
    after,
    hush,
    assert_action_button_gap,
    nested_cards,
)

HTML = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parents[1] / "F-WH-STOCKTAKE.html").resolve()
URL = HTML.as_uri()
SHOTS = Path(__file__).parent / "shots"
SHOTS.mkdir(exist_ok=True)


def main():
    suite = Suite("F-WH-STOCKTAKE · ตรวจนับใหญ่")
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        suite.watch(page)

        def reset(route="rounds"):
            page.goto("about:blank")
            ready(page, URL + "#/" + route)

        def state(expr):
            return page.evaluate("() => " + expr)

        def fn01():
            reset()
            page.get_by_role("button", name="สร้างรอบนับ").click()
            settle(page)
            fields = page.locator("#drawer input")
            fields.nth(0).fill("ตรวจนับทดสอบโซน A")
            fields.nth(1).fill("โซน A")
            page.locator("#drawer .combo-option", has_text="คลังหลัก / โซน A").click()
            page.get_by_role("button", name="ยืนยันสร้าง").click()
            settle(page)
            out = state("({id:current().id,name:current().name,scope:current().scope,status:current().status})")
            assert out["name"] == "ตรวจนับทดสอบโซน A" and out["scope"] == "WH-01-A"
            assert out["status"] == "draft" and page.locator("#drawer.is-open").count() == 0
            return "ค้นหาและเลือกพื้นที่ WH-01-A แล้วสร้างรอบแบบร่างสำเร็จ"

        def fn02():
            reset("sheets")
            rows = page.locator(".tbl tbody tr")
            assert rows.count() == 2
            text = rows.all_inner_texts()
            assert any("ITM-001" in x and "WH-01-A" in x for x in text)
            assert any("ITM-002" in x and "WH-01-A" in x for x in text)
            return "ใบนับแสดงสินค้าและตำแหน่งจากรายการอ้างอิง 2 รายการ"

        def fn03():
            reset()
            after(page, """() => {
              role='supervisor';currentPersonId='P3';
              drawer={type:'create',name:'รอบคลังหลักซ้อน',scope:'WH-01'};
              return createRound(null);
            }""")
            assert state("current().status") == "draft"
            after(page, "() => freezeRound(current().id,null)")
            assert state("current().status") == "draft"
            assert "ทับซ้อน" in page.locator("#toast-root").inner_text()
            return "บล็อกรอบ WH-01 เพราะทับซ้อนรอบ WH-01-A ที่กำลังใช้งาน"

        def fn04():
            reset()
            out = after(page, """async () => {
              role='supervisor';currentPersonId='P3';
              rounds[0].status='closed';
              const r={id:'ST-IMM-001',name:'พิสูจน์ยอดตั้งต้น',scope:'WH-01-A',status:'draft',freezeAt:'',snapshot:[],assignee:'',recountAssignee:'',counts:{},recounts:{},audit:[],adjustmentRef:''};
              rounds.unshift(r); selected=r.id; await freezeRound(r.id,null);
              const before=JSON.stringify(r.snapshot); ITEMS[0].qty=999;
              return {status:r.status,before,after:JSON.stringify(r.snapshot),at:r.freezeAt};
            }""")
            assert out["status"] == "frozen" and out["at"]
            assert out["before"] == out["after"] and "999" not in out["after"]
            return "เก็บยอดตั้งต้น ณ เวลาล็อก และไม่เปลี่ยนตามยอดสินค้าในภายหลัง"

        def fn05():
            reset("sheets")
            after(page, "() => {role='supervisor';currentPersonId='P3';const r=current();r.status='frozen';openAssign(r.id,false)}")
            after(page, "() => choose('บุคคล','P2')")
            page.get_by_role("button", name="ยืนยัน").click()
            settle(page)
            assert state("current().assignee") == "P2" and state("current().status") == "counting"
            assert "พิมพ์ดาว ศรีสุข" in page.locator("main").inner_text()
            return "มอบหมายใบนับให้บุคคลจริงและเข้าสถานะกำลังนับ"

        def fn06():
            reset("sheets")
            assert page.locator(".tbl thead").get_by_text("ยอดตั้งต้น", exact=True).count() == 0
            page.locator("select[aria-label='สลับมุมมองเพื่อทดสอบ']").select_option("supervisor:P3")
            settle(page)
            assert page.locator(".tbl thead").get_by_text("ยอดตั้งต้น", exact=True).count() == 1
            return "ผู้นับไม่เห็นยอดตั้งต้น; หัวหน้างานเห็นตามสิทธิ์"

        def fn07():
            reset("sheets")
            inputs = page.locator("input[type=number]")
            inputs.nth(0).fill("-1")
            inputs.nth(1).fill("")
            page.get_by_role("button", name="ส่งผลนับ").click()
            settle(page)
            assert state("current().status") == "counting"
            assert "ศูนย์หรือมากกว่า" in page.locator("#toast-root").inner_text()
            inputs.nth(0).fill("0")
            inputs.nth(1).fill("0")
            page.get_by_role("button", name="ส่งผลนับ").click()
            settle(page)
            assert state("current().counts['ITM-001']") == 0
            return "กันค่าติดลบ/ช่องว่าง และยอมรับผลนับ 0"

        def fn08():
            reset("sheets")
            out_equal = after(page, """async () => {
              const r=current();r.counts={'ITM-001':10,'ITM-002':18};
              await submitCount(r.id,null);return r.status;
            }""")
            assert out_equal == "review", "ผลต่างเท่ากับเกณฑ์ต้องไม่บังคับนับซ้ำ"
            reset("sheets")
            out_over = after(page, """async () => {
              const r=current();r.counts={'ITM-001':9,'ITM-002':20};
              await submitCount(r.id,null);return {status:r.status,threshold:inventoryConfig.varianceThreshold,date:inventoryConfig.effectiveDate};
            }""")
            assert out_over == {"status": "recount", "threshold": 2, "date": "2026-09-01"}
            return "ผลต่าง =2 ผ่านตรวจ; ผลต่าง >2 เข้านับซ้ำตาม config effective date"

        def fn09():
            reset("sheets")
            after(page, """async () => {const r=current();r.counts={'ITM-001':9,'ITM-002':20};await submitCount(r.id,null);role='supervisor';currentPersonId='P3';openAssign(r.id,true)}""")
            after(page, "() => choose('บุคคล','P1')")
            page.get_by_role("button", name="ยืนยัน").click()
            settle(page)
            assert state("current().recountAssignee") == ""
            assert "คนละคน" in page.locator("#toast-root").inner_text()
            after(page, "() => choose('บุคคล','P2')")
            page.get_by_role("button", name="ยืนยัน").click()
            settle(page)
            assert state("current().recountAssignee") == "P2"
            return "บังคับผู้นับซ้ำเป็นคนละคนกับผู้นับครั้งแรก"

        def fn10():
            reset("variance")
            after(page, "() => {role='supervisor';currentPersonId='P3';const r=current();r.status='review';render();openDoa(r.id)}")
            after(page, "() => choose('ผู้อนุมัติ:0','P3')")
            page.get_by_role("button", name="ยืนยัน").click()
            settle(page)
            assert state("current().status") == "pending" and state("current().approver") == "P3"
            page.get_by_role("button", name="ไม่อนุมัติ").click()
            page.get_by_role("button", name="ยืนยัน").click()
            settle(page)
            assert state("current().status") == "pending" and "ระบุเหตุผล" in page.locator("#toast-root").inner_text()
            page.locator("#reject-reason").fill("ผลต่างยังไม่มีหลักฐาน")
            page.get_by_role("button", name="ยืนยัน").click()
            settle(page)
            audit = state("current().audit.map(x=>x.act)")
            assert state("current().status") == "rejected"
            assert any("ไม่อนุมัติ" in x and "หลักฐาน" in x for x in audit)
            return "เลือกผู้อนุมัติจริง; การปฏิเสธบังคับเหตุผลและบันทึกประวัติ"

        def fn11():
            reset("variance")
            out = after(page, """async () => {
              role='supervisor';currentPersonId='P3';const r=current();r.status='approved';render();
              const before=ITEMS.map(x=>x.qty);await handoff(r.id,null);
              const d={id:'ST-AFTER-001',name:'รอบหลังปิด',scope:r.scope,status:'draft',freezeAt:'',snapshot:[],assignee:'',recountAssignee:'',counts:{},recounts:{},audit:[],adjustmentRef:''};
              rounds.unshift(d);selected=d.id;await freezeRound(d.id,null);
              return {closed:r.status,ref:r.adjustmentRef,before,after:ITEMS.map(x=>x.qty),next:d.status};
            }""")
            assert out["closed"] == "closed" and out["ref"].startswith("ADJ-DRAFT-")
            assert out["before"] == out["after"] and out["next"] == "frozen"
            payload = state("rounds.find(x=>x.id==='ST-2026-001').handoff.payload")
            assert payload["ref_count_doc"] == "ST-2026-001" and len(payload["lines"]) == 2
            return "สร้างร่างใบปรับยอด, ไม่แก้ on-hand และปลดล็อกให้รอบถัดไป"

        def fn12():
            reset()
            visible = page.locator("main").inner_text()
            assert "Cycle Count" not in visible and "ABC" not in visible
            labels = page.locator(".tabs .tab").all_inner_texts()
            assert labels == ["รอบนับ", "ใบนับ", "ผลต่าง", "ประวัติ"]
            hush(page)
            page.screenshot(path=str(SHOTS / "stocktake-boundary.png"), full_page=False)
            return "DOM มีเฉพาะรอบนับใหญ่ ไม่มีเมนูหรือ action ของ Cycle Count ABC"

        def bypass_b1():
            reset("sheets")
            out = after(page, """async () => {
              role='supervisor';currentPersonId='P3';const r=current();
              const before={status:r.status,freezeAt:r.freezeAt,snapshot:JSON.stringify(r.snapshot)};
              ITEMS[0].qty=999;await freezeRound(r.id,null);
              return {before,after:{status:r.status,freezeAt:r.freezeAt,snapshot:JSON.stringify(r.snapshot)}};
            }""")
            assert out["before"] == out["after"], out
            assert "เฉพาะรอบที่ยังเป็นแบบร่าง" in page.locator("#toast-root").inner_text()
            return "freeze บน counting ถูก block; status/freezeAt/snapshot ไม่เปลี่ยน"

        def bypass_b2():
            reset("variance")
            out = after(page, """async () => {
              role='supervisor';currentPersonId='P3';const r=current();await handoff(r.id,null);
              return {status:r.status,ref:r.adjustmentRef,handoff:r.handoff,locked:isLocked(r)};
            }""")
            assert out == {"status": "counting", "ref": "", "handoff": None, "locked": True}, out
            assert "ต้องอนุมัติผลต่างก่อน" in page.locator("#toast-root").inner_text()
            return "handoff บน counting ถูก block และพื้นที่ยังล็อก"

        def bypass_b3():
            reset("variance")
            blocked = after(page, """async () => {
              const r=current();role='counter';currentPersonId='P1';
              modal={type:'approve',id:r.id};await confirmModal(null);return r.status;
            }""")
            assert blocked == "counting"
            assert "ไม่ใช่ผู้มีสิทธิ์" in page.locator("#toast-root").inner_text()
            allowed = after(page, """async () => {
              const r=current();r.status='pending';r.approvalSteps=[{level:1,label:'ผู้จัดการคลัง',person:'P3',by:'',at:''}];r.approver='P3';
              role='supervisor';currentPersonId='P3';modal={type:'approve',id:r.id};await confirmModal(null);return r.status;
            }""")
            assert allowed == "approved"
            return "ผู้นับ bypass ไม่ได้; approver จริงบน pending อนุมัติได้"

        def doa_tiers():
            reset("variance")
            first = after(page, """async () => {
              const r=current();role='supervisor';currentPersonId='P3';r.status='review';
              r.counts={'ITM-001':11,'ITM-002':20};openDoa(r.id);
              const initial=modal.slots.map(x=>x.person);choose('ผู้อนุมัติ:0','P3');choose('ผู้อนุมัติ:1','P4');
              await confirmModal(null);return {total:varianceTotal(r),initial,steps:r.approvalSteps.length,status:r.status,active:activeApproval(r).person};
            }""")
            assert first["total"] == 25000 and first["initial"] == ["", ""]
            assert first["steps"] == 2 and first["status"] == "pending" and first["active"] == "P3"
            mid = after(page, """async () => {const r=current();modal={type:'approve',id:r.id};await confirmModal(null);return {status:r.status,active:activeApproval(r).person};}""")
            assert mid == {"status": "pending", "active": "P4"}
            done = after(page, """async () => {setRole('supervisor:P4');const r=current();modal={type:'approve',id:r.id};await confirmModal(null);return {status:r.status,by:r.approvalSteps.map(x=>x.by)};}""")
            assert done == {"status": "approved", "by": ["P3", "P4"]}
            return "25,000 บาท resolve 2 ขั้น; ไม่ prefill; P3→P4 อนุมัติทีละขั้น"

        def scan_and_demo():
            reset("sheets")
            page.get_by_role("button", name="สแกน").click()
            assert "F089" in page.locator("#toast-root").inner_text()
            assert page.locator(".demo-only:visible").count() == 1
            page.add_style_tag(content=".demo-only{display:none!important}")
            assert page.locator(".demo-only:visible").count() == 0
            assert page.get_by_role("button", name="สร้างรอบนับ").is_visible()
            assert state("document.documentElement.scrollWidth <= innerWidth")
            return "ปุ่มสแกนอ้าง F089; ซ่อน demo-only แล้ว layout และ action หลักยังปกติ"

        def layout_count_actions():
            reset("sheets")
            result = assert_action_button_gap(
                page,
                ".table-foot > span:last-child",
                min_gap=8,
                note="ใบนับ · สแกน/ส่งผลนับ",
            )
            assert result["tested"], "ไม่พบคู่ปุ่ม action ใน footer ของใบนับ"
            page.screenshot(path=str(SHOTS / "ui-count-actions.png"), full_page=False)
            return "ปุ่มสแกนและส่งผลนับมีช่องไฟอย่างน้อย 8px"

        def layout_history_handoff():
            reset("history")
            after(page, """() => {
              const r=current();
              r.handoff={
                ack:{adjId:'ADJ-DRAFT-001',status:'draft'},
                payload:{ref_count_doc:r.id,lines:[{},{}]}
              };
              render();
            }""")
            bad = nested_cards(page, root="#app", sel=".card")
            assert bad == [], f"พบ card ซ้อน card ในประวัติ: {bad}"
            page.screenshot(path=str(SHOTS / "ui-history-handoff.png"), full_page=False)
            return "สรุปส่งต่อใบปรับยอดเป็น section แบน ไม่ซ้อน card"

        def recount_assignee_guard():
            reset("sheets")
            after(page, """async () => {
              const r=current();
              r.counts={'ITM-001':9,'ITM-002':20};
              await submitCount(r.id,null);
              r.recountAssignee='P2';
              r.recounts={'ITM-001':11,'ITM-002':20};
              setRole('counter:P1');
              setTab('sheets');
            }""")
            assert page.locator("input[type=number]").count() == 0
            assert page.get_by_role("button", name="ส่งผลนับ").count() == 0
            blocked = after(page, """async () => {
              const r=current();
              await submitCount(r.id,null);
              return r.status;
            }""")
            assert blocked == "recount"
            assert "ไม่ใช่ผู้ได้รับมอบหมาย" in page.locator("#toast-root").inner_text()
            page.locator("select[aria-label='สลับมุมมองเพื่อทดสอบ']").select_option("counter:P2")
            settle(page)
            assert page.locator("input[type=number]").count() == 2
            assert page.get_by_role("button", name="ส่งผลนับ").count() == 1
            return "เฉพาะ P2 ที่ได้รับมอบหมายเท่านั้นที่แก้ไขและส่งผลนับซ้ำได้"

        suite.check("FN-01", "กำหนดพื้นที่ด้วยการค้นหา", fn01)
        suite.check("FN-02", "รายการสินค้า/ตำแหน่งแบบอ้างอิง", fn02)
        suite.check("FN-03", "ล็อกพื้นที่และกันรอบซ้อน", fn03)
        suite.check("FN-04", "ยอดตั้งต้นไม่แก้ย้อนหลัง", fn04)
        suite.check("FN-05", "สร้างและมอบหมายใบนับ", fn05)
        suite.check("FN-06", "blind count และสิทธิ์หัวหน้า", fn06)
        suite.check("FN-07", "ศูนย์ได้; ติดลบ/ว่างไม่ได้", fn07)
        suite.check("FN-08", "ผลต่างและเกณฑ์ตาม effective date", fn08)
        suite.check("FN-09", "นับซ้ำโดยคนอิสระ", fn09)
        suite.check("FN-10", "อนุมัติ/ปฏิเสธพร้อม audit", fn10)
        suite.check("FN-11", "handoff ไปใบปรับยอดและปลดล็อก", fn11)
        suite.check("FN-12", "boundary จาก Cycle Count", fn12)
        suite.check("B1", "freeze ซ้ำต้องไม่ทับ snapshot", bypass_b1)
        suite.check("B2", "handoff ก่อนอนุมัติต้องถูก block", bypass_b2)
        suite.check("B3", "approve ต้อง guard สถานะและตัวตน", bypass_b3)
        suite.check("FIX-04", "DOA resolve ตามมูลค่าและอนุมัติทีละขั้น", doa_tiers)
        suite.check("FIX-07/08", "F089 scan anchor และ demo-only", scan_and_demo)
        suite.check("UI-01", "ช่องไฟปุ่มสแกน/ส่งผลนับ", layout_count_actions)
        suite.check("UI-02", "ประวัติส่งต่อไม่ซ้อน card", layout_history_handoff)
        suite.check("SEC-01", "ผู้ส่งผลนับต้องเป็นผู้ได้รับมอบหมาย", recount_assignee_guard)
        browser.close()

    print("FN ครอบ 12/12 · FN-40 0/0 · เคสรวม 20")
    suite.report()


if __name__ == "__main__":
    main()
