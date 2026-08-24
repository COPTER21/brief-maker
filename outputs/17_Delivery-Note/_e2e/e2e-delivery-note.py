from pathlib import Path
import json
import sys

from playwright.sync_api import sync_playwright


OUTPUTS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(OUTPUTS / "_SHARED" / "_e2e"))
from uikit import Suite, ready, settle as shared_settle, after as shared_after, hush, assert_icons_rendered  # noqa: E402


HTML = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parents[1] / "f-wh-delivery-note.html").resolve()
BASE = HTML.as_uri()
SHOTS = Path(__file__).parent / "shots"
SHOTS.mkdir(exist_ok=True)
suite = Suite("F-WH-DN Delivery Note")
route_nonce = 0


def settle(page, timeout=900):
    shared_settle(page, timeout=timeout)


def after(page, js, timeout=900):
    return shared_after(page, js, timeout=timeout)


def open_route(page, route="#/list"):
    global route_nonce
    route_nonce += 1
    ready(page, f"{BASE}?e2e={route_nonce}{route}", timeout=1400)
    assert page.locator("#page-content").inner_text().strip()


def snap(page, name):
    hush(page)
    page.screenshot(path=SHOTS / name, full_page=True)


def create_reference_dn(page, pack_code=None):
    open_route(page)
    if pack_code is None:
        pack_code = page.evaluate("() => dnJobs().find(p => p.ref.startsWith('SO-')).code")
    after(page, f"() => navigate('create/{pack_code}')")
    modal = page.locator("#mkdn-modal")
    assert modal.is_visible()
    page.get_by_role("button", name="ยืนยันออกใบส่งของ", exact=True).click(force=True)
    settle(page)
    did = page.evaluate("() => DNS[0].id")
    assert page.locator("#view-drawer").is_visible()
    return did


def make_ready(page, did):
    after(page, f"""() => {{ const d=findDN('{did}'); d.contact='คุณผู้รับ · 08 0000 0000'; d.assignee=ME.name; d.carrier='OWN'; d.vehicle='V-5590'; d.driver='DRV-01'; markReady(d.id); }}""")
    assert page.evaluate(f"() => findDN('{did}').status") == "ready"


def queue_and_pack_drill(page):
    open_route(page)
    body = page.locator("#page-content").inner_text()
    assert "รอออกใบส่งของ" in body and "PACK-2026-0460" in body and "TR-2026-0012" in body
    page.locator("#table-body tr").filter(has_text="TR-2026-0012").click()
    settle(page)
    text = page.locator(".modal-overlay").inner_text()
    assert "WH-01 → WH-02" in text and "น้ำดื่ม CUBE" in text and "กก." in text
    snap(page, "01-transfer-pack-drill.png")


def multi_so_same_customer_destination(page):
    open_route(page)
    data = page.evaluate("""() => {
      const a=dnJobs().find(p=>p.ref.startsWith('SO-'));
      const b=dnJobs().find(p=>p.code!==a.code && p.ref.startsWith('SO-'));
      const source=SO_BY[a.ref], alias='SO-2026-0999';
      SO_BY[alias]=Object.assign({},source,{code:alias}); b.ref=alias;
      state.sel={[a.code]:true}; render();
      const row=[...document.querySelectorAll('#table-body tr')].find(r=>r.innerText.includes(b.code));
      return {a:a.code,b:b.code,enabled:!row.querySelector('input[type=checkbox]').disabled};
    }""")
    assert data["enabled"]
    after(page, f"() => {{ state.sel['{data['b']}']=true; createFromSel(); }}")
    assert page.locator("#mkdn-modal").is_visible()
    assert page.locator("#mkdn-modal tbody tr").count() >= 2


def create_confirm_and_defaults(page):
    open_route(page)
    pickup = page.evaluate("() => dnJobs().find(p => refInfo(p.ref).pickup).code")
    after(page, f"() => navigate('create/{pickup}')")
    text = page.locator("#mkdn-modal").inner_text()
    assert "เลขที่ที่จะได้" in text and "ยังไม่ตัดสต๊อก" in text and "ลูกค้ามารับเอง" in text
    before = page.evaluate("() => DNS.length")
    page.get_by_role("button", name="ยกเลิก", exact=True).click(force=True)
    settle(page)
    assert page.evaluate("() => DNS.length") == before


def draft_form_validation_carriers(page):
    did = create_reference_dn(page)
    customer = page.locator("#view-drawer .field").filter(has_text="จากเอกสารอ้างอิง").first
    assert customer.locator("input").is_disabled(), "reference customer must remain source-controlled"
    assert "แก้ลูกค้าที่ SO ต้นทาง" in customer.inner_text(), "read-only customer explanation missing"
    after(page, f"() => markReady('{did}')")
    assert page.locator(".field.is-error").count() >= 1, "required fields did not enter error state"
    assert "กรอกข้อมูลที่มี * ให้ครบก่อนยืนยันพร้อมส่ง" in page.locator("body").inner_text(), "required validation toast missing"
    assert page.locator("#cbi-dn").count() == 1, "assignee search input missing"
    page.locator("#cbi-dn").fill("สม")
    assert page.locator("#combo-pop").is_visible()
    page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")
    settle(page)
    assert page.evaluate(f"() => !!findDN('{did}').assignee"), "keyboard selection did not bind assignee"
    assert page.evaluate("() => CARRIERS.some(c=>c.kind==='3pl') && VEHICLES.every(v=>v.cap>0) && DRIVERS.every(d=>d.tel)"), "carrier metadata incomplete"


def dispatch_and_goods_issue(page):
    did = create_reference_dn(page)
    make_ready(page, did)
    after(page, f"() => openDispatchModal('{did}')")
    assert "ตัดสต๊อกจริง" in page.locator(".modal-overlay").inner_text()
    before = page.evaluate("() => MOVEMENTS.length")
    page.get_by_role("button", name="ยืนยันออกรถ · ตัดสต๊อก").click(force=True)
    settle(page)
    result = page.evaluate(f"() => {{ const d=findDN('{did}'); return [d.status,!!d.gi,MOVEMENTS.length>{before},MOVEMENTS.at(-1).type]; }}")
    assert result == ["in_transit", True, True, "issue"]


def tracking_timeline(page):
    did = create_reference_dn(page)
    make_ready(page, did)
    after(page, f"() => dispatch('{did}')")
    for _ in range(3):
        after(page, f"() => advanceTrack('{did}')")
    track = page.evaluate(f"() => findDN('{did}').track.map(x=>x.code)")
    assert track == ["out_for_delivery", "picked_up", "in_hub"], track
    assert "สถานะการจัดส่ง" in page.locator("#view-drawer").inner_text()


def pod_evidence_and_partial(page):
    did = create_reference_dn(page)
    make_ready(page, did)
    after(page, f"() => dispatch('{did}')")
    after(page, f"() => openPodModal('{did}')")
    page.locator("#pod-by").fill("คุณทดสอบ ผู้รับสินค้า")
    after(page, f"() => {{ mockSign('{did}'); mockPhoto('{did}'); __pod.rows[0].rejected=1; __pod.rows[0].reason=REJECT_REASONS[0]; paintPod('{did}'); }}")
    page.locator("#pod-by").fill("คุณทดสอบ ผู้รับสินค้า")
    page.locator("#pod-note").fill("รับบางส่วน")
    page.get_by_role("button", name="บันทึก · รับบางส่วน").click(force=True)
    settle(page)
    result = page.evaluate(f"() => {{ const d=findDN('{did}'); return [d.status,d.pod.sign,d.pod.photos.length,MOVEMENTS.some(m=>m.ref===d.code&&m.type==='return_in')]; }}")
    assert result == ["partial", True, 1, True]


def billing_after_delivery(page):
    did = create_reference_dn(page)
    after(page, f"() => {{ const d=findDN('{did}'); d.status='delivered'; d.pod={{by:'ผู้รับ',at:nowIso(),result:'accepted',note:'',sign:true,photos:[]}}; renderViewDrawer(); }}")
    assert page.get_by_role("button", name="ส่งต่อวางบิล").is_visible()


def failed_reschedule_attempts(page):
    did = create_reference_dn(page)
    make_ready(page, did)
    after(page, f"() => dispatch('{did}')")
    after(page, f"() => openFailModal('{did}')")
    page.locator("#md-reason").fill("ลูกค้าปิดร้าน")
    page.locator("#md-ok").click(force=True)
    settle(page)
    assert page.evaluate(f"() => findDN('{did}').status==='failed' && findDN('{did}').attempts.length===1")
    after(page, f"() => reschedule('{did}')")
    assert page.evaluate(f"() => findDN('{did}').status") == "ready"


def return_backorder_cancel(page):
    did = create_reference_dn(page)
    make_ready(page, did)
    after(page, f"() => dispatch('{did}')")
    after(page, f"() => {{ const d=findDN('{did}'); d.status='failed'; openReturnAllModal(d.id); }}")
    page.locator("#md-reason").fill("ปฏิเสธรับทั้งหมด")
    page.locator("#md-ok").click(force=True)
    settle(page)
    assert page.evaluate(f"() => findDN('{did}').status==='returned' && !findDN('{did}').gi")
    did2 = create_reference_dn(page)
    after(page, f"() => decideBackorder('{did2}', true)")
    assert page.evaluate(f"() => findDN('{did2}').audit[0].act.includes('backorder')")
    after(page, f"() => openCancelModal('{did2}')")
    page.locator("#md-reason").fill("ยกเลิกโดยผู้ใช้")
    page.locator("#md-ok").click(force=True)
    assert page.evaluate(f"() => findDN('{did2}').status") == "cancelled"


def source_flow_items_readonly(page):
    did = create_reference_dn(page)
    text = page.locator("#view-drawer").inner_text()
    assert "Document Flow" in text and "ใบสั่งขาย" in text
    page.get_by_role("button", name="รายการ · กล่อง").click(force=True)
    settle(page)
    assert "ล็อต · หมดอายุ" in page.locator("#view-drawer").inner_text()
    make_ready(page, did)
    assert page.locator("#view-drawer input:not([disabled])").count() == 0
    assert page.get_by_role("button", name="แก้ไขข้อมูลส่ง").is_visible()


def a4_and_transfer_no_so_sync(page):
    open_route(page)
    transfer = page.evaluate("() => dnJobs().find(p=>p.ref.startsWith('TR-')).code")
    did = create_reference_dn(page, transfer)
    assert page.evaluate(f"() => findDN('{did}').customer==='' && findDN('{did}').ref.startsWith('TR-')")
    page.get_by_role("button", name="ใบส่งของ (พิมพ์)", exact=False).last.click(force=True)
    settle(page)
    text = page.locator("#view-drawer").inner_text()
    assert "DELIVERY NOTE" in text and "TR-2026-0012" in text and "ผู้รับสินค้า" in text and "ผู้ตรวจสอบ" in text
    assert (HTML.parent / "06_PRINT" / "DN_template.html").exists()
    assert (HTML.parent / "06_PRINT" / "DN_sample.pdf").stat().st_size > 10000


def list_tabs_permissions(page):
    open_route(page)
    after(page, "() => { state.view='dns'; render(); }")
    assert "ส่งออก CSV" in page.locator("#page-content").inner_text(), "DN list tab did not render"
    after(page, "() => switchPersona(3)")
    assert page.locator("#manual-create-btn").count() == 0, "viewer still sees manual create"
    assert page.get_by_role("button", name="ออกใบส่งของ", exact=True).count() == 0, "viewer still sees reference create"
    after(page, "() => switchPersona(0)")
    after(page, "() => navigate('view/DN-2026-0356')")
    for tab in ("ข้อมูลจัดส่ง", "รายการ · กล่อง", "ใบส่งของ (พิมพ์)", "ประวัติ"):
        assert page.get_by_role("button", name=tab, exact=False).count() >= 1, f"tab missing: {tab}"
    assert "สร้างใบส่งของ" in page.locator("#view-drawer").inner_text(), "stepper missing"
    page.keyboard.press("Escape")
    settle(page)
    assert page.locator("#view-drawer").count() == 0


def audit_and_responsive(page):
    open_route(page)
    did = create_reference_dn(page)
    make_ready(page, did)
    assert page.evaluate(f"() => findDN('{did}').audit.length>=2 && findDN('{did}').audit.every(a=>a.act&&a.by&&a.at)")
    for width in (1024, 1280):
        page.set_viewport_size({"width": width, "height": 900})
        open_route(page)
        assert page.locator("#table-body").is_visible()
        assert page.evaluate("() => document.documentElement.scrollWidth <= innerWidth")
    snap(page, "14-responsive-1280.png")


def manual_creation_and_all_statuses(page):
    open_route(page)
    assert_icons_rendered(page, "#page-content")
    page.locator("#manual-create-btn").click(force=True)
    page.locator("#manual-ref").fill("EXT-DN-E2E-001")
    page.locator("#manual-customer").fill("หน่วยงานทดสอบ")
    page.locator("#manual-address").fill("99 ถนนทดสอบ กรุงเทพมหานคร")
    page.locator("#manual-note").fill("สร้างแยกจาก reference")
    page.locator("#manual-create-confirm").click(force=True)
    settle(page)
    did = page.evaluate("() => DNS[0].id")
    assert page.evaluate(f"() => findDN('{did}').sourceMode==='manual' && findDN('{did}').packs.length===0")
    assert page.locator("#manual-status-btn").is_visible()
    for status in ("ready", "in_transit", "failed", "partial", "delivered", "returned", "cancelled", "draft"):
        after(page, f"() => openManualStatusModal('{did}')")
        page.locator("#manual-new-status").select_option(status)
        page.locator("#manual-status-reason").fill("E2E เปลี่ยนสถานะ " + status)
        page.locator("#manual-status-confirm").click(force=True)
        settle(page)
        assert page.evaluate(f"() => findDN('{did}').status") == status
        if status == "failed":
            assert page.evaluate(f"() => findDN('{did}').attempts.length") == 1
            assert "ส่งไม่สำเร็จ ครั้งที่ 0" not in page.locator("#view-drawer").inner_text()
    assert page.evaluate(f"() => !findDN('{did}').gi && findDN('{did}').audit.length===9")
    snap(page, "15-manual-status.png")


def refresh_closes_drawer(page):
    open_route(page, "#/view/DN-2026-0356")
    assert page.locator("#view-drawer").is_visible()
    page.reload()
    page.wait_for_selector("#table-body")
    settle(page)
    assert page.locator("#view-drawer").count() == 0, "reload restored a stale drawer"
    assert page.url.endswith("#/list"), page.url


def pmba_search_and_manual_transport(page):
    open_route(page)
    pack = page.evaluate("() => dnJobs().find(p=>p.ref.startsWith('SO-') && !refInfo(p.ref).pickup).code")
    after(page, f"() => navigate('create/{pack}')")
    assert page.locator("#cbi-mkdn-assignee").is_visible()
    page.locator("#cbi-mkdn-assignee").fill("วิภา")
    assert page.locator("#combo-pop").is_visible()
    assert page.evaluate("() => cbState.list.length>0 && cbState.list.every(x=>PEOPLE.includes(x.p))")
    assert "กรอกเอง" not in page.locator("#combo-pop").inner_text()
    page.keyboard.press("Enter")
    settle(page)
    assert page.evaluate("() => __mkdn.assignee==='วิภาวี ตั้งมั่น'")

    after(page, "() => { __mkdn.vehicle=''; paintCreateConfirm(); }")
    page.locator("#cbi-mkvehicle").fill("รถไม่อยู่ในรายการ")
    page.locator("#combo-pop button").filter(has_text="กรอกเลขรถเอง").click(force=True)
    page.locator("#transport-plate").fill("3ฒก-4455 กรุงเทพมหานคร")
    page.locator("#transport-manual-confirm").click(force=True)
    settle(page)
    assert page.evaluate("() => VEHICLES.find(v=>v.code===__mkdn.vehicle)?.plate==='3ฒก-4455 กรุงเทพมหานคร'")

    after(page, "() => { __mkdn.driver=''; paintCreateConfirm(); }")
    page.locator("#cbi-mkdriver").fill("คนขับไม่อยู่ในรายการ")
    page.locator("#combo-pop button").filter(has_text="กรอกคนขนส่งเอง").click(force=True)
    page.locator("#transport-first").fill("กิตติ")
    page.locator("#transport-last").fill("ขนส่งดี")
    page.locator("#transport-tel").fill("08 1234 5678")
    page.locator("#transport-manual-confirm").click(force=True)
    settle(page)
    assert page.evaluate("() => { const x=DRIVERS.find(d=>d.code===__mkdn.driver); return x?.name==='กิตติ ขนส่งดี' && x?.tel==='08 1234 5678'; }")

    vehicle = page.evaluate("() => __mkdn.vehicle")
    driver = page.evaluate("() => __mkdn.driver")
    page.get_by_role("button", name="ยืนยันออกใบส่งของ", exact=True).click(force=True)
    settle(page)
    assert page.evaluate(f"() => DNS[0].vehicle==='{vehicle}' && DNS[0].driver==='{driver}'")
    text = page.locator("#view-drawer").inner_text()
    assert "3ฒก-4455 กรุงเทพมหานคร" in text and "กิตติ ขนส่งดี" in text and "08 1234 5678" in text
    snap(page, "17-pmba-manual-transport.png")


CASES = [
    ("FN-01 FN-02 FN-28", "คิว packed, pack drill และ Stock Transfer", queue_and_pack_drill),
    ("FN-03", "รวมหลาย SO เมื่อ customer + ship-to เดียวกัน", multi_so_same_customer_destination),
    ("FN-04 FN-05", "confirm ก่อนสร้างและค่า pickup/default", create_confirm_and_defaults),
    ("FN-06 FN-07 FN-08 FN-09 FN-10 FN-11", "draft form, validation, combobox และ carrier modes", draft_form_validation_carriers),
    ("FN-12 FN-13", "dispatch confirm และ Goods Issue", dispatch_and_goods_issue),
    ("FN-14", "tracking timeline", tracking_timeline),
    ("FN-15 FN-16 FN-17", "POD evidence และ partial return-in", pod_evidence_and_partial),
    ("FN-18", "ส่งต่อวางบิลหลังส่ง", billing_after_delivery),
    ("FN-19 FN-20", "ส่งไม่สำเร็จและนัดใหม่", failed_reschedule_attempts),
    ("FN-21 FN-22 FN-23", "return-all, backorder และ cancel", return_backorder_cancel),
    ("FN-24 FN-25 FN-26", "SO flow, items/boxes และ read-only", source_flow_items_readonly),
    ("FN-27 FN-28", "A4 และ Transfer ที่ไม่ sync SO", a4_and_transfer_no_so_sync),
    ("FN-90 FN-91 FN-92 FN-93", "stepper/list/tabs/Esc/permission", list_tabs_permissions),
    ("FN-94 FN-95", "append-only audit และ responsive", audit_and_responsive),
    ("MAN-01", "manual creation แยกและอัปเดตครบทุกสถานะ", manual_creation_and_all_statuses),
    ("REG-REFRESH", "refresh ต้องปิด drawer และกลับหน้า list", refresh_closes_drawer),
    ("PMBA-TRANSPORT", "search dropdown และกรอกคนขนส่ง/เลขรถเอง", pmba_search_and_manual_transport),
]


with sync_playwright() as pw:
    browser = pw.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.set_default_timeout(5000)
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
covered = sorted({token for ids, _, _ in CASES for token in ids.split() if token.startswith("FN-")})
result = {
    "feature": "F-WH-DN",
    "fn_covered": len(covered),
    "fn_total": 34,
    "fn40_total": 0,
    "tests_passed": passed,
    "tests_total": len(CASES),
    "console_errors": suite.console_errors,
    "results": [{"ids": r[0], "name": r[1], "status": r[2], "detail": r[3]} for r in suite.results],
}
(Path(__file__).parent / "results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"FN ครอบ {len(covered)}/34 · FN-40 rendered negative 0/0 · เคสรวม {len(CASES)} · ผ่าน {passed}/{len(CASES)}")
suite.report(exit_on_fail=False)
sys.exit(0 if passed == len(CASES) and not suite.console_errors else 1)
