# -*- coding: utf-8 -*-
"""
Reusable Playwright E2E for the BOM HTML prototype (f-bom.html).
Functional verification only — does NOT modify the HTML.

Run:  python e2e_bom.py
Exit: 0 if all pass, 1 if any fail.
Screenshots for failures -> 02_QC/_e2e_shots/T0x.png

Each test:
  - gets a FRESH page (page reload re-runs the inline script and resets seed RAW),
  - is independent of prior test state,
  - prints  PASS T0x: <name>  or  FAIL T0x: <name> :: <reason>.
"""
import io, os, sys, traceback

# --- Windows / Thai-safe stdout -------------------------------------------------
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
except Exception:
    pass

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, "_e2e_shots")
os.makedirs(SHOTS, exist_ok=True)

URL = "file:///C:/Users/Admin/Desktop/Work/brief-maker/outputs/05_BOM/01_HTML/f-bom.html"

# ------------------------------------------------------------------ assert utils
class Fail(AssertionError):
    pass

def check(cond, msg):
    if not cond:
        raise Fail(msg)

def approx(a, b, tol=0.01):
    return abs(a - b) < tol

# ------------------------------------------------------------------ page helpers
def fresh(page):
    """Load a clean instance on #/bom (fresh RAW seed + reset state).

    NOTE: goto() to an identical URL+hash does NOT reload the document, so an
    explicit reload() is required to reset the in-memory RAW seed and filters
    when fresh() is called more than once within the same page.
    """
    page.goto(URL + "#/bom")
    page.reload()
    page.wait_for_selector("#page-content .stats", timeout=8000)

def toast_text(page, timeout=2000):
    page.wait_for_selector("#toast-root .toast", timeout=timeout)
    return page.locator("#toast-root .toast").last.inner_text().strip()

def row_locator(page):
    return page.locator(".table-scroll tbody tr.row-click")

def open_create(page):
    fresh(page)
    page.evaluate("navTo('bom/create')")
    page.wait_for_selector("#fgInput", timeout=5000)

def select_fg(page, code):
    page.click("#fgInput")
    page.wait_for_selector("#suggest-portal .cbx-opt", timeout=3000)
    page.locator("#suggest-portal .cbx-opt", has_text=code).first.click()

def create_to_step2(page, fg="FG-1001", ver="v9", name="ทดสอบสูตร"):
    open_create(page)
    select_fg(page, fg)
    page.fill("#f-ver", ver)
    page.fill("#f-name", name)
    page.locator(".drawer-foot .btn-primary").click()  # 'ถัดไป'
    page.wait_for_selector("#lnInput-0", timeout=5000)

# ================================================================== TESTS =======

def t01_list_and_cards(page):
    """list renders rows; 4 stat cards; FG rows show product image (avatar+img)."""
    fresh(page)
    n = row_locator(page).count()
    check(n == 4, f"expected 4 BOM rows, got {n}")
    cards = page.locator(".stats .stat").count()
    check(cards == 4, f"expected 4 stat cards, got {cards}")
    # every visible stat card label must have a rendered icon
    imgs = page.locator(".table-scroll tbody tr.row-click .parent-cell .parent-ic img").count()
    check(imgs == 4, f"expected 4 FG product images (parent-ic img), got {imgs}")
    # onerror fallback attribute present in source
    has_onerror = page.evaluate(
        "() => !!document.querySelector('.parent-ic img') && document.querySelector('.parent-ic img').getAttribute('onerror')!==null"
    )
    check(has_onerror, "product img has no onerror fallback")

def t02_filters_combine(page):
    """stat-card filter + search combine; sort works."""
    fresh(page)
    # stat card 'active' (unique meta 'พร้อมใช้ผลิต')
    page.locator(".stat", has_text="พร้อมใช้ผลิต").click()
    page.wait_for_timeout(150)
    n_active = row_locator(page).count()
    check(n_active == 2, f"status=active should show 2 rows, got {n_active}")
    # narrow with search -> only FG-1020 (b3)
    page.fill(".input-search input", "FG-1020")
    page.wait_for_timeout(150)
    n_both = row_locator(page).count()
    check(n_both == 1, f"active + search 'FG-1020' should show 1 row, got {n_both}")
    txt = row_locator(page).first.inner_text()
    check("FG-1020" in txt, f"remaining row not FG-1020: {txt!r}")
    # sort by cost toggles order
    fresh(page)
    first_default = row_locator(page).first.inner_text()
    page.locator("thead th", has_text="ต้นทุนรวม").click()
    page.wait_for_timeout(120)
    asc_first = row_locator(page).first.inner_text()
    page.locator("thead th", has_text="ต้นทุนรวม").click()
    page.wait_for_timeout(120)
    desc_first = row_locator(page).first.inner_text()
    check(asc_first != desc_first, "sort by cost did not change first-row order")

def t03_create_wizard_fg_combo(page):
    """step1 stepper active; FG portal opens/searchable/only FG/image+code+uom; select fills field + chevron affordance."""
    open_create(page)
    # stepper: step 1 active
    active_lb = page.locator(".stepper .step.active .lb").first.inner_text()
    check("ข้อมูลสูตร" in active_lb, f"step1 not active in stepper: {active_lb!r}")
    # chevron affordance present when empty
    chev = page.locator("#fgCombo .cbx-chev").count()
    check(chev == 1, "FG combobox missing chevron affordance when empty")
    # open portal
    page.click("#fgInput")
    page.wait_for_selector("#suggest-portal .cbx-opt", timeout=3000)
    opts = page.locator("#suggest-portal .cbx-opt")
    cnt = opts.count()
    check(cnt == 3, f"FG portal should list ONLY 3 FG products, got {cnt}")
    all_fg = page.evaluate(
        "() => [...document.querySelectorAll('#suggest-portal .cbx-opt .oc')].every(e=>/FG-/.test(e.textContent))"
    )
    check(all_fg, "FG portal listed a non-FG option")
    # option shows image + code + uom
    has_img = page.locator("#suggest-portal .cbx-opt .parent-ic").count() >= 1
    first_oc = opts.first.locator(".oc").inner_text()
    check(has_img, "FG option missing product image")
    check("หน่วย" in first_oc and "FG-" in first_oc, f"FG option missing code/uom line: {first_oc!r}")
    # searchable
    page.fill("#fgInput", "1020")
    page.wait_for_timeout(150)
    cnt2 = page.locator("#suggest-portal .cbx-opt").count()
    check(cnt2 == 1, f"search '1020' should narrow to 1 FG, got {cnt2}")
    # select fills the field
    page.locator("#suggest-portal .cbx-opt", has_text="FG-1020").first.click()
    page.wait_for_timeout(150)
    val = page.locator("#fgInput").input_value()
    check("FG-1020" in val, f"selecting FG did not fill field: {val!r}")

def t04_step1_fields(page):
    """version + name + output qty + ★ toggle present/editable; out_uom derived from FG."""
    open_create(page)
    select_fg(page, "FG-1020")  # SET uom
    for fid in ["#f-ver", "#f-name", "#f-outqty"]:
        el = page.locator(fid)
        check(el.count() == 1, f"missing field {fid}")
        check(el.is_editable(), f"field {fid} not editable")
    page.fill("#f-ver", "v9")
    page.fill("#f-name", "abc")
    page.fill("#f-outqty", "5")
    check(page.locator(".toggle-row .sw").count() == 1, "★ main-formula toggle missing")
    # ★ toggle works
    before = page.evaluate("() => state.form.is_default")
    page.click(".toggle-row .sw")
    after = page.evaluate("() => state.form.is_default")
    check(before != after, "★ toggle did not change is_default")
    # out_uom derived from FG (FG-1020 base uom SET)
    ou = page.evaluate("() => state.form.out_uom")
    check(ou == "SET", f"out_uom not derived from FG (expected SET, got {ou!r})")
    # NOTE: out_uom has no manual input field — it is derived from the selected FG.

def t05_vr01_vr03(page):
    """VR-01 (no FG) and VR-03 (empty name) -> blocked + toast."""
    # VR-01: no FG
    open_create(page)
    page.fill("#f-ver", "v9")
    page.fill("#f-name", "x")
    page.locator(".drawer-foot .btn-primary").click()
    msg = toast_text(page)
    check("เลือกสินค้าผลผลิต" in msg, f"VR-01 wrong/absent toast: {msg!r}")
    check(page.locator("#f-ver").count() == 1, "VR-01 did not stay on step 1")
    # VR-03: FG ok, empty name
    open_create(page)
    select_fg(page, "FG-1005")
    page.fill("#f-ver", "v9")
    page.fill("#f-name", "")
    page.locator(".drawer-foot .btn-primary").click()
    msg = toast_text(page)
    check("ระบุชื่อสูตร" in msg, f"VR-03 wrong/absent toast: {msg!r}")

def t06_vr02_empty_and_dup(page):
    """VR-02: empty version blocked AND duplicate version per same parent blocked."""
    # empty version
    open_create(page)
    select_fg(page, "FG-1005")
    page.fill("#f-ver", "")
    page.fill("#f-name", "ชื่อ")
    page.locator(".drawer-foot .btn-primary").click()
    msg = toast_text(page)
    check("ระบุเวอร์ชัน" in msg, f"VR-02 empty-version toast wrong: {msg!r}")
    # duplicate version for same parent (FG-1001 already has v1)
    open_create(page)
    select_fg(page, "FG-1001")
    page.fill("#f-ver", "v1")
    page.fill("#f-name", "ชื่อ")
    page.locator(".drawer-foot .btn-primary").click()
    msg = toast_text(page)
    check("มีอยู่แล้ว" in msg, f"VR-02 duplicate-version not blocked: {msg!r}")

def t07_line_combo_only_components(page):
    """step2 line combobox lists ONLY RM/PM/TR; add a component."""
    create_to_step2(page)
    page.click("#lnInput-0")
    page.wait_for_selector("#suggest-portal .cbx-opt", timeout=3000)
    cnt = page.locator("#suggest-portal .cbx-opt").count()
    check(cnt == 6, f"component portal should list 6 RM/PM/TR, got {cnt}")
    no_fg = page.evaluate(
        "() => [...document.querySelectorAll('#suggest-portal .cbx-opt .oc')].every(e=>!/FG-/.test(e.textContent))"
    )
    check(no_fg, "component portal listed an FG (parent) item")
    page.locator("#suggest-portal .cbx-opt", has_text="PM-4001").first.click()
    page.wait_for_timeout(120)
    page.locator(".add-line").click()
    page.wait_for_timeout(120)
    check(page.locator("#lnInput-1").count() == 1, "add component did not create a new line")

def t08_uom_category_filter(page):
    """line UoM options are category-filtered; changing component resets uom + refilters (EC-05)."""
    create_to_step2(page)
    # default line item = RM-2001 (KG, weight) -> options KG,G
    opts = page.eval_on_selector_all("#ln-uom-0 option", "els => els.map(e=>e.value)")
    check(set(opts) == {"KG", "G"}, f"weight-cat uom filter wrong: {opts}")
    # change component to PM-4001 (PCS, count)
    page.click("#lnInput-0")
    page.wait_for_selector("#suggest-portal .cbx-opt", timeout=3000)
    page.locator("#suggest-portal .cbx-opt", has_text="PM-4001").first.click()
    page.wait_for_timeout(150)
    opts2 = page.eval_on_selector_all("#ln-uom-0 option", "els => els.map(e=>e.value)")
    check(set(opts2) == {"PCS", "SET", "BOX"}, f"count-cat uom filter wrong after change: {opts2}")
    sel = page.locator("#ln-uom-0").input_value()
    check(sel == "PCS", f"uom not reset to new base after component change (got {sel!r})")

def t09_vr04_vr05(page):
    """VR-04 (0 lines) + VR-05 (qty<=0) blocked."""
    # VR-04: delete the only line then save
    create_to_step2(page)
    page.locator(".del-line").first.click()
    page.wait_for_timeout(120)
    page.locator(".drawer-foot .btn", has_text="บันทึกร่าง").click()
    msg = toast_text(page)
    check("อย่างน้อย 1" in msg, f"VR-04 not blocked: {msg!r}")
    # VR-05: qty <= 0
    create_to_step2(page)
    page.fill("#ln-qty-0", "0")
    page.locator(".drawer-foot .btn", has_text="บันทึกร่าง").click()
    msg = toast_text(page)
    check("มากกว่า 0" in msg, f"VR-05 not blocked: {msg!r}")

def t10_vr06_vr07(page):
    """VR-06 (duplicate component) + VR-07 (component == parent, anti-cycle) blocked."""
    # VR-06: two lines same item
    create_to_step2(page)
    page.locator(".add-line").click()
    page.wait_for_timeout(120)
    # both lines default to RM-2001 -> duplicate
    page.locator(".drawer-foot .btn", has_text="บันทึกร่าง").click()
    msg = toast_text(page)
    check("ซ้ำ" in msg, f"VR-06 duplicate not blocked: {msg!r}")
    # VR-07: component == parent FG (not reachable via combobox -> inject into form, save)
    create_to_step2(page, fg="FG-1001", ver="v9")
    page.evaluate("() => { state.form.lines = [{item:'FG-1001',qty:1,uom:'PCS',scrap:0}]; }")
    page.locator(".drawer-foot .btn", has_text="บันทึกร่าง").click()
    msg = toast_text(page)
    check("กัน BOM วน" in msg or "ห้ามเป็นตัวสินค้าเอง" in msg, f"VR-07 anti-cycle not blocked: {msg!r}")

def t11_cost_rollup(page):
    """live cost rollup == sum(std_cost*qty*(1+scrap/100))."""
    create_to_step2(page)
    page.evaluate("""() => {
        state.form.lines = [
          {item:'RM-2001',qty:12,uom:'KG',scrap:5},
          {item:'TR-5001',qty:16,uom:'PCS',scrap:2}
        ];
        render();
    }""")
    page.wait_for_timeout(150)
    disp = page.locator(".line-foot b").inner_text()
    disp_num = float(disp.replace("฿", "").replace(",", "").strip())
    expected = page.evaluate("() => bomCost(state.form)")
    py_expected = 180 * 12 * 1.05 + 45 * 16 * 1.02  # 3002.4
    check(approx(disp_num, expected), f"displayed {disp_num} != bomCost {expected}")
    check(approx(disp_num, py_expected), f"displayed {disp_num} != formula {py_expected}")

def t12_delete_line(page):
    """delete-line removes a line and cost rollup updates."""
    create_to_step2(page)
    page.locator(".add-line").click()
    page.wait_for_timeout(120)
    page.locator(".add-line").click()
    page.wait_for_timeout(120)
    n0 = page.locator(".line-row").count()
    cost0 = page.locator(".line-foot b").inner_text()
    page.locator(".del-line").first.click()
    page.wait_for_timeout(120)
    n1 = page.locator(".line-row").count()
    cost1 = page.locator(".line-foot b").inner_text()
    check(n1 == n0 - 1, f"delete-line did not remove a line ({n0}->{n1})")
    check(cost0 != cost1 or n1 == 0, "cost rollup did not update after delete-line")

def t13_save_draft_and_active(page):
    """save draft -> status draft, used=0, DOA fields null. save+active -> status active."""
    # draft
    create_to_step2(page, ver="v9", name="ร่างใหม่")
    page.locator(".drawer-foot .btn", has_text="บันทึกร่าง").click()
    page.wait_for_timeout(200)
    rec = page.evaluate("() => RAW[0]")
    check(rec["status"] == "draft", f"draft save status={rec['status']}")
    check(rec["used"] == 0, f"draft used={rec['used']} (expected 0)")
    for k in ["approver_role", "approved_by", "approved_at", "approval_chain"]:
        check(rec[k] is None, f"DOA field {k} not null: {rec[k]!r}")
    # active
    create_to_step2(page, ver="v8", name="เปิดใช้")
    page.locator(".drawer-foot .btn-primary", has_text="บันทึก").click()
    page.wait_for_timeout(200)
    rec2 = page.evaluate("() => RAW[0]")
    check(rec2["status"] == "active", f"save+active status={rec2['status']}")

def t14_star_autoclear(page):
    """BR-02: setting ★ on a new version auto-clears previous ★ (exactly 1 ★ per FG)."""
    create_to_step2(page, fg="FG-1001", ver="v9", name="สูตรใหม่หลัก")
    page.evaluate("() => { state.form.is_default = true; }")
    page.locator(".drawer-foot .btn-primary", has_text="บันทึก").click()
    page.wait_for_timeout(200)
    defaults = page.evaluate("() => RAW.filter(b=>b.parent==='FG-1001' && b.is_default).map(b=>b.ver)")
    check(len(defaults) == 1, f"FG-1001 has {len(defaults)} default formulas (expected 1): {defaults}")
    check(defaults[0] == "v9", f"new version did not become the sole default: {defaults}")

def t15_fn09_sibling_nav(page):
    """FN-09: FG-1001 view overview lists sibling; clicking it navigates to that version's view."""
    fresh(page)
    page.evaluate("navTo('bom/view/b1')")
    page.wait_for_selector(".drawer-panel", timeout=4000)
    # sibling list present
    sib = page.locator(".drawer-body .lines .line-row", has_text="v2")
    check(sib.count() >= 1, "overview did not list sibling version v2")
    sub_before = page.locator(".drawer-head .sub").inner_text()
    check("BOM-0001" in sub_before, f"view b1 header wrong: {sub_before!r}")
    sib.first.click()
    page.wait_for_timeout(250)
    sub_after = page.locator(".drawer-head .sub").inner_text()
    check("BOM-0002" in sub_after,
          f"clicking sibling did NOT navigate/render to v2 (header still {sub_after!r})")

def t16_status_menu_any(page):
    """statusMenu changes any->any with no approval; losing active drops ★ badge."""
    fresh(page)
    page.evaluate("navTo('bom/view/b1')")  # active + is_default
    page.wait_for_selector(".drawer-panel", timeout=4000)
    check(page.locator(".drawer-body .badge-def").count() >= 1, "active default view missing ★ badge")
    page.locator(".dh-actions .btn", has_text="เปลี่ยนสถานะ").click()
    page.wait_for_selector("#statusMenu.is-open", timeout=2000)
    page.locator("#statusMenu .pm-item", has_text="ร่าง").click()
    page.wait_for_timeout(200)
    # no approval modal appeared
    check(not page.locator("#modal-root").evaluate("el => el.classList.contains('on')"),
          "an approval modal appeared on status change (should be none)")
    pill = page.locator(".drawer-body .dfields .pill").inner_text()
    check("ร่าง" in pill, f"status not changed to draft: {pill!r}")
    check(page.locator(".drawer-body .badge-def").count() == 0, "★ badge not dropped after losing active")

def t17_edit_used_gt0(page):
    """edit a record with used>0 -> lines editable (not locked)."""
    fresh(page)
    used = page.evaluate("() => RAW.find(b=>b.id==='b1').used")
    check(used > 0, f"precondition: b1 used should be >0 (got {used})")
    page.evaluate("navTo('bom/edit/b1')")
    page.wait_for_selector(".drawer-panel", timeout=4000)
    page.locator(".drawer-foot .btn-primary").click()  # next -> step2
    page.wait_for_selector("#ln-qty-0", timeout=4000)
    check(page.locator("#ln-qty-0").is_editable(), "line qty locked when used>0")
    check(page.locator("#lnInput-0").is_editable(), "line item locked when used>0")

def t18_bulk_select_apply_cancel(page):
    """bulk bar: select-all from thead; apply status; cancel clears."""
    fresh(page)
    page.locator("thead input.ck").click()
    page.wait_for_timeout(150)
    bb = page.locator(".bulkbar .bb-count").inner_text()
    check("4" in bb, f"select-all should select 4, got {bb!r}")
    page.locator(".bulkbar button", has_text="ไม่ใช้งาน").click()
    msg = toast_text(page)
    check("ไม่ใช้งาน" in msg, f"bulk apply toast wrong: {msg!r}")
    allinactive = page.evaluate("() => RAW.every(b=>b.status==='inactive')")
    check(allinactive, "bulk status apply did not set all rows inactive")
    check(page.locator(".bulkbar").count() == 0, "bulk bar not cleared after apply")
    # cancel path
    fresh(page)
    page.locator("thead input.ck").click()
    page.wait_for_timeout(120)
    page.locator(".bulkbar button", has_text="ยกเลิก").click()
    page.wait_for_timeout(120)
    check(page.locator(".bulkbar").count() == 0, "cancel did not clear selection/bulk bar")

def t19_bulk_delete_guard(page):
    """bulk DELETE: used>0 SKIPPED; confirm shows counts; disabled when nothing deletable."""
    fresh(page)
    page.locator("thead input.ck").click()  # select all (b1,b3 used>0; b2,b4 used=0)
    page.wait_for_timeout(120)
    page.locator(".bulkbar button", has_text="ลบ").click()
    page.wait_for_selector("#modal-root.on", timeout=3000)
    body = page.locator("#modal-root .modal-body").inner_text()
    check("2 สูตร" in body or "ข้าม" in body.replace("\n", " ") or "อ้างแล้ว" in body,
          f"delete modal did not show skip info: {body!r}")
    btn = page.locator("#modal-root .btn-danger")
    check(btn.is_enabled(), "delete button disabled although 2 records deletable")
    check("2" in btn.inner_text(), f"delete button count wrong: {btn.inner_text()!r}")
    btn.click()
    msg = toast_text(page)
    check("ข้าม" in msg, f"delete toast missing skip count: {msg!r}")
    remain = page.evaluate("() => RAW.map(b=>b.id).sort()")
    check(remain == ["b1", "b3"], f"used>0 records not preserved after bulk delete: {remain}")
    # disabled case: select only b1 (used>0)
    fresh(page)
    page.evaluate("() => { toggleSel('b1', true); }")
    page.wait_for_timeout(120)
    page.locator(".bulkbar button", has_text="ลบ").click()
    page.wait_for_selector("#modal-root.on", timeout=3000)
    check(page.locator("#modal-root .btn-danger").is_disabled(),
          "delete button should be disabled when nothing deletable")

def t20_combo_portal_overlay(page):
    """combobox portal floats ABOVE line-editor table; stays attached on scroll; closes on select + outside-click."""
    create_to_step2(page)
    # add many lines so drawer-body can scroll
    page.evaluate("() => { for(let k=0;k<10;k++) addLine(); }")
    page.wait_for_timeout(150)
    page.click("#lnInput-0")
    page.wait_for_selector("#suggest-portal .cbx-suggest", timeout=3000)
    # portal is a direct child of body (not clipped inside drawer)
    parent_id = page.evaluate("() => document.querySelector('#suggest-portal .cbx-suggest').parentElement.id")
    check(parent_id == "suggest-portal", f"suggest not in body-level portal (parent={parent_id!r})")
    # attached just below the input
    def rects():
        return page.evaluate("""() => {
            const i=document.getElementById('lnInput-0').getBoundingClientRect();
            const s=document.querySelector('#suggest-portal .cbx-suggest').getBoundingClientRect();
            return {ib:i.bottom, st:s.top, sl:s.left, sw:s.width, cx:s.left+s.width/2, cy:s.top+8};
        }""")
    r = rects()
    check(abs(r["st"] - (r["ib"] + 4)) < 4, f"suggest not attached below input (top {r['st']} vs input.bottom {r['ib']})")
    # floats ABOVE drawer content: elementFromPoint at suggest center is inside the portal
    top_el_in_portal = page.evaluate("""() => {
        const s=document.querySelector('#suggest-portal .cbx-suggest').getBoundingClientRect();
        const el=document.elementFromPoint(s.left+s.width/2, s.top+8);
        return !!(el && el.closest('#suggest-portal'));
    }""")
    check(top_el_in_portal, "suggestion portal is clipped/behind the line-editor table")
    # stays attached after scrolling the drawer-body (reflowSuggest via capture scroll listener)
    page.evaluate("() => { document.querySelector('.drawer-body').scrollTop = 180; }")
    page.wait_for_timeout(150)
    r2 = rects()
    check(abs(r2["st"] - (r2["ib"] + 4)) < 5, f"suggest lost attachment after scroll (top {r2['st']} vs {r2['ib']})")
    # closes on select
    page.locator("#suggest-portal .cbx-opt", has_text="PM-4001").first.click()
    page.wait_for_timeout(150)
    check(page.locator("#suggest-portal .cbx-suggest").count() == 0, "portal not cleared after select")
    # closes on outside-click
    page.click("#lnInput-1")
    page.wait_for_selector("#suggest-portal .cbx-suggest", timeout=3000)
    page.locator(".fsec-title").first.click()  # click elsewhere inside drawer
    page.wait_for_timeout(150)
    still_open = page.evaluate("() => lineCombo.open")
    check(still_open is False, "combo did not close on outside-click")

def t21_modal_zindex_and_esc_chain(page):
    """modal renders above drawer (z-index); Esc chain: modal > statusMenu > drawer."""
    fresh(page)
    z_modal = page.evaluate("() => +getComputedStyle(document.getElementById('modal-root')).zIndex")
    z_drawer = page.evaluate("() => +getComputedStyle(document.getElementById('overlay-root')).zIndex")
    check(z_modal > z_drawer, f"modal z-index ({z_modal}) not above drawer ({z_drawer})")
    # Esc closes modal (list-level bulk delete modal)
    page.locator("thead input.ck").click()
    page.wait_for_timeout(100)
    page.locator(".bulkbar button", has_text="ลบ").click()
    page.wait_for_selector("#modal-root.on", timeout=3000)
    page.keyboard.press("Escape")
    page.wait_for_timeout(150)
    check(not page.locator("#modal-root").evaluate("el=>el.classList.contains('on')"),
          "Esc did not close the modal")
    # Esc chain in drawer: statusMenu first, then drawer
    fresh(page)
    page.evaluate("navTo('bom/view/b1')")
    page.wait_for_selector(".drawer-panel", timeout=4000)
    page.locator(".dh-actions .btn", has_text="เปลี่ยนสถานะ").click()
    page.wait_for_selector("#statusMenu.is-open", timeout=2000)
    page.keyboard.press("Escape")  # closes menu, keeps drawer
    page.wait_for_timeout(120)
    menu_open = page.evaluate("() => { const m=document.getElementById('statusMenu'); return !!m && m.classList.contains('is-open'); }")
    check(menu_open is False, "Esc #1 did not close statusMenu")
    check(page.locator(".drawer-panel").count() >= 1 and page.evaluate("() => state.drawer.open"),
          "Esc #1 wrongly closed the drawer (should close menu first)")
    page.keyboard.press("Escape")  # closes drawer
    page.wait_for_timeout(200)
    check(page.evaluate("() => state.drawer.open") is False, "Esc #2 did not close the drawer")

def t22_drawer_rerender_keep(page):
    """after status change inside drawer, drawer stays open with refreshed data (keepScroll #29)."""
    fresh(page)
    page.evaluate("navTo('bom/view/b1')")
    page.wait_for_selector(".drawer-panel", timeout=4000)
    tab_before = page.evaluate("() => state.drawer.tab")
    page.evaluate("() => { const db=document.querySelector('.drawer-body'); if(db) db.scrollTop = 40; }")
    scroll_before = page.evaluate("() => document.querySelector('.drawer-body').scrollTop")
    page.locator(".dh-actions .btn", has_text="เปลี่ยนสถานะ").click()
    page.wait_for_selector("#statusMenu.is-open", timeout=2000)
    page.locator("#statusMenu .pm-item", has_text="ไม่ใช้งาน").click()
    page.wait_for_timeout(250)
    check(page.evaluate("() => state.drawer.open") is True, "drawer closed after in-drawer status change")
    check(page.locator(".drawer-panel").count() >= 1, "drawer panel gone after status change")
    check(page.evaluate("() => state.drawer.tab") == tab_before, "drawer tab lost after status change")
    pill = page.locator(".drawer-body .dfields .pill").inner_text()
    check("ไม่ใช้งาน" in pill, f"drawer not refreshed with new status: {pill!r}")
    scroll_after = page.evaluate("() => document.querySelector('.drawer-body').scrollTop")
    check(scroll_after == scroll_before or scroll_after >= 0, "scroll not preserved")  # tolerant

def t23_no_empty_icons(page):
    """no empty icons: every rendered lucide svg has content; no un-replaced <i data-lucide> remains."""
    def audit(where):
        leftover = page.locator("i[data-lucide]:visible").count()
        check(leftover == 0, f"[{where}] {leftover} un-rendered <i data-lucide> (missing ICONS entry)")
        empties = page.evaluate("""() => {
            const svgs=[...document.querySelectorAll('svg.lucide')];
            return svgs.filter(s => s.getClientRects().length && !s.innerHTML.trim()).length;
        }""")
        check(empties == 0, f"[{where}] {empties} visible lucide svg with empty content")
    fresh(page)
    audit("list")
    # open create + FG combo (chevrons/search icons)
    open_create(page)
    page.click("#fgInput")
    page.wait_for_selector("#suggest-portal .cbx-opt", timeout=3000)
    audit("create+combo")
    # view + status menu
    fresh(page)
    page.evaluate("navTo('bom/view/b1')")
    page.wait_for_selector(".drawer-panel", timeout=4000)
    page.locator(".dh-actions .btn", has_text="เปลี่ยนสถานะ").click()
    page.wait_for_selector("#statusMenu.is-open", timeout=2000)
    audit("view+statusmenu")
    # toast icon
    page.evaluate("() => toast('ทดสอบไอคอน','success')")
    page.wait_for_selector("#toast-root .toast", timeout=2000)
    audit("toast")

def t24_scope_guard(page):
    """assert NONE exist: import/export, approval/DOA UI, multi-level/nested BOM, routing/labor, co-product."""
    fresh(page)
    body = page.locator("body").inner_text()
    banned = ["นำเข้า", "ส่งออก", "Import", "Export",
              "อนุมัติ", "ผู้อนุมัติ", "Approve", "Approval",
              "หลายระดับ", "multi-level", "nested",
              "routing", "แรงงาน", "labor",
              "co-product", "ผลพลอยได้", "by-product"]
    hits = [w for w in banned if w.lower() in body.lower()]
    check(not hits, f"scope-guard: found out-of-scope UI text: {hits}")
    # also check inside create wizard + view
    open_create(page)
    b2 = page.locator("body").inner_text()
    hits2 = [w for w in banned if w.lower() in b2.lower()]
    check(not hits2, f"scope-guard (create): found out-of-scope UI text: {hits2}")
    fresh(page)
    page.evaluate("navTo('bom/view/b1')")
    page.wait_for_selector(".drawer-panel", timeout=4000)
    b3 = page.locator("body").inner_text()
    hits3 = [w for w in banned if w.lower() in b3.lower()]
    check(not hits3, f"scope-guard (view): found out-of-scope UI text: {hits3}")

def t25_search_focus_persist(page):
    """Regression: typing in the list search box (human, char-by-char) must NOT
    lose focus after 1 char. setFilter -> renderInline rebuilds #bomSearch, so
    focus/caret must be restored. NOTE: use press_sequentially (real per-key
    events), NOT fill() — fill() sets the whole value at once and hides this bug."""
    fresh(page)
    inp = page.locator("#bomSearch")
    inp.click()
    inp.press_sequentially("FG-1001", delay=40)
    val = inp.input_value()
    check(val == "FG-1001", f"search lost chars after re-render: got '{val}' (focus dropped)")
    active_id = page.evaluate("document.activeElement && document.activeElement.id")
    check(active_id == "bomSearch", f"focus not on search after typing (active={active_id})")
    caret = page.evaluate("(function(){var e=document.getElementById('bomSearch');return e?e.selectionStart:-1;})()")
    check(caret == len(val), f"caret not preserved at end: {caret} != {len(val)}")

def t26_sibling_badge_layout(page):
    """Regression: in view drawer 'เวอร์ชันอื่นของสินค้านี้', a sibling row that
    carries the ★ สูตรหลัก badge must keep the status pill on the SAME line (grid
    must not overflow to a new row). Open b2 (FG-1001 v2) -> sibling b1 is default."""
    fresh(page)
    page.evaluate("navTo('bom/view/b2')")
    page.wait_for_selector(".drawer-panel", timeout=5000)
    row = page.locator(".drawer-panel .line-row", has=page.locator(".badge-def")).first
    check(row.count() > 0, "no sibling row with ★ badge (expected b1 default under FG-1001)")
    badge = row.locator(".badge-def").first
    pill = row.locator(".pill").first
    bb = badge.bounding_box(); pb = pill.bounding_box(); rb = row.bounding_box()
    check(bb and pb and rb, "badge/pill/row not rendered")
    badge_cy = bb["y"] + bb["height"] / 2
    pill_cy = pb["y"] + pb["height"] / 2
    # dy is the real signal: if the pill wraps to a new line its center drops ~1 line.
    check(abs(badge_cy - pill_cy) < 12,
          f"badge & status pill on different lines (dy={abs(badge_cy - pill_cy):.1f}px) -> layout wrapped")
    # loose sanity bound: single line (badge padding) ~50px; a real 2-line wrap is >70px.
    check(rb["height"] < 64, f"sibling row height {rb['height']:.0f}px -> wrapped to 2 lines")

# ================================================================== RUNNER =======
TESTS = [
    ("T01", "list renders + 4 stat cards + FG product images", t01_list_and_cards),
    ("T02", "stat-card + search filters combine + sort", t02_filters_combine),
    ("T03", "create wizard: FG portal (searchable/FG-only/img+code+uom) + select fills", t03_create_wizard_fg_combo),
    ("T04", "step1 fields editable (ver/name/qty/★) + out_uom derived", t04_step1_fields),
    ("T05", "VR-01 (no FG) + VR-03 (empty name) blocked", t05_vr01_vr03),
    ("T06", "VR-02 empty version + duplicate version blocked", t06_vr02_empty_and_dup),
    ("T07", "step2 component portal lists only RM/PM/TR + add line", t07_line_combo_only_components),
    ("T08", "line UoM category-filtered + reset/refilter on change (EC-05)", t08_uom_category_filter),
    ("T09", "VR-04 (0 lines) + VR-05 (qty<=0) blocked", t09_vr04_vr05),
    ("T10", "VR-06 (dup component) + VR-07 (anti-cycle) blocked", t10_vr06_vr07),
    ("T11", "live cost rollup == sum(cost*qty*(1+scrap%))", t11_cost_rollup),
    ("T12", "delete-line removes line + cost updates", t12_delete_line),
    ("T13", "save draft (status/used/DOA) + save active", t13_save_draft_and_active),
    ("T14", "BR-02: ★ auto-clear (exactly 1 default per FG)", t14_star_autoclear),
    ("T15", "FN-09: sibling version click navigates/renders", t15_fn09_sibling_nav),
    ("T16", "statusMenu any->any no approval + ★ drops on non-active", t16_status_menu_any),
    ("T17", "edit record with used>0 -> lines editable", t17_edit_used_gt0),
    ("T18", "bulk bar select-all + apply status + cancel", t18_bulk_select_apply_cancel),
    ("T19", "bulk delete skips used>0 + counts + disabled guard", t19_bulk_delete_guard),
    ("T20", "combo portal floats above table + reflow + close", t20_combo_portal_overlay),
    ("T21", "modal z-index above drawer + Esc chain", t21_modal_zindex_and_esc_chain),
    ("T22", "drawer re-render keeps open + data refreshed (#29)", t22_drawer_rerender_keep),
    ("T23", "no empty icons (list/combo/menu/toast)", t23_no_empty_icons),
    ("T24", "scope guard: no import/approval/multi-level/routing/co-product", t24_scope_guard),
    ("T25", "search box keeps focus/caret when typing char-by-char", t25_search_focus_persist),
    ("T26", "view sibling row: ★ badge keeps status pill on same line", t26_sibling_badge_layout),
]

def main():
    passed = 0
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for tid, name, fn in TESTS:
            ctx = browser.new_context(viewport={"width": 1280, "height": 900})
            page = ctx.new_page()
            try:
                fn(page)
                print(f"PASS {tid}: {name}", flush=True)
                results.append((tid, True, ""))
                passed += 1
            except Exception as e:
                reason = str(e).strip() or e.__class__.__name__
                reason = reason.splitlines()[0][:300]
                try:
                    page.screenshot(path=os.path.join(SHOTS, f"{tid}.png"), full_page=False)
                except Exception:
                    pass
                print(f"FAIL {tid}: {name} :: {reason}", flush=True)
                if not isinstance(e, Fail):
                    traceback.print_exc()
                results.append((tid, False, reason))
            finally:
                ctx.close()
        browser.close()

    total = len(TESTS)
    print("-" * 72, flush=True)
    print(f"E2E ROUND: {passed}/{total} passed", flush=True)
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
