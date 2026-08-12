# -*- coding: utf-8 -*-
"""
Playwright E2E harness for warehouse-bin.html (Warehouse & Bin · F-LOC).
Functional verification of the single-file SPA — derives real selectors/state
from the file (does NOT hard-code assumptions).

Run:  python e2e_warehouse.py
Env:
  E2E_RESULTS_JSON  -> path to write per-round JSON results (default _e2e_results.json)
Exit: 0 if all pass, 1 if any fail.
Screenshots for failures -> 02_QC/_e2e_shots/<Txx>.png

Each test gets a FRESH context+page; fresh() does goto+reload so the inline
script re-runs and the in-memory seed arrays (WAREHOUSES/ZONES/.../LOCATIONS/
AUDIT/BRANCHES) reset to their initial state.
"""
import io, os, sys, json, traceback

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
HTML_PATH = os.path.normpath(os.path.join(HERE, "..", "warehouse-bin.html"))
RESULTS_JSON = os.environ.get("E2E_RESULTS_JSON", os.path.join(HERE, "_e2e_results.json"))

URL = "file:///C:/Users/Admin/Desktop/Work/brief-maker/outputs/06_Warehouse-Bin/warehouse-bin.html"

with io.open(HTML_PATH, "r", encoding="utf-8") as _f:
    HTML_SRC = _f.read()

# ------------------------------------------------------------------ assert utils
class Fail(AssertionError):
    pass

def check(cond, msg):
    if not cond:
        raise Fail(msg)

# ------------------------------------------------------------------ page helpers
def fresh(page):
    page.goto(URL)
    page.reload()
    page.wait_for_selector("#page-content .stats", timeout=8000)
    page.wait_for_timeout(60)

def toast_text(page, timeout=4000):
    page.wait_for_selector("#toast.is-visible", timeout=timeout)
    return page.locator("#toast").inner_text().strip()

def rows(page):
    return page.locator(".card .table tbody tr")

def open_wh_create(page):
    fresh(page)
    page.evaluate("openDrawer('create','warehouse',null)")
    page.wait_for_selector("#f-code", timeout=5000)

def open_branch_list(page):
    page.click("#f-branch-search")
    page.wait_for_selector("#branch-portal .mb-opt, #branch-portal .mb-empty", timeout=3000)

def audit_len(page, node_id):
    # AUDIT is a top-level `const` (NOT attached to window); reference it lexically.
    return page.evaluate("(id)=>{try{return AUDIT[id]?AUDIT[id].length:0}catch(e){return 0}}", node_id)

def click_branch_opt(page, code):
    """REAL mouse click (mousedown+mouseup+click at coords) on a branch option by code.
    NOTE: selection now happens on `mousedown` (see renderBranchOpts in warehouse-bin.html),
    so an in-page element.click() — which dispatches only a click event, never a mousedown —
    would NOT select. A real coordinate click is required, matching how a user selects."""
    page.locator("#branch-portal .mb-opt", has_text=code).click()

def branch_opt(page, code):
    """Locator for a branch option button by code (real element, portalled to <body>)."""
    return page.locator("#branch-portal .mb-opt", has_text=code)

def mouse_click_branch_opt(page, code, inner=None):
    """REAL mouse click (mousedown+mouseup+click at coords) on a branch option — the path a
    human uses and the one the keyboard-only E2E never exercised. `inner` optionally targets
    a child span (.mb-ic / .mb-nm) to prove selection works when the icon/text is the target."""
    loc = branch_opt(page, code)
    if inner:
        loc = loc.locator(inner)
    loc.click()

# ================================================================== TESTS =======

def t01_list_and_stats(page):
    """root list: 2 WH rows + 5 stat cards + 'สาขา' column + branch-cell code·name."""
    fresh(page)
    n = rows(page).count()
    check(n == 2, f"expected 2 warehouse rows, got {n}")
    cards = page.locator(".stats .stat").count()
    check(cards == 5, f"expected 5 stat cards, got {cards}")
    heads = page.locator(".card .table thead th").all_inner_texts()
    check(any("สาขา" in h for h in heads), f"WH list missing 'สาขา' column: {heads}")
    bc = page.locator(".card .table tbody .branch-cell").count()
    check(bc == 2, f"expected 2 branch cells (one per WH), got {bc}")
    txt = page.locator(".card .table tbody .branch-cell").first.inner_text()
    check("00000" in txt and "สำนักงานใหญ่" in txt, f"branch cell not 'code · name_th': {txt!r}")

def t02_drill_five_levels(page):
    """drill Warehouse>Zone>Area>Rack>Location via row-click + evaluate; breadcrumb has 5 chips."""
    fresh(page)
    # real row click -> warehouse level (zones)
    rows(page).first.locator("td").nth(0).click()
    page.wait_for_timeout(120)
    cur = page.locator(".drill-chip.is-current").inner_text()
    check("WH-01" in cur, f"row-click did not drill to WH-01 (current chip {cur!r})")
    check(rows(page).count() == 4, f"WH-01 should list 4 zones, got {rows(page).count()}")
    page.evaluate("selectNode('zone','Z-STORAGE')"); page.wait_for_timeout(80)
    check(rows(page).count() == 3, f"Z-STORAGE should list 3 areas, got {rows(page).count()}")
    page.evaluate("selectNode('area','A-AISLE-A')"); page.wait_for_timeout(80)
    check(rows(page).count() == 2, f"A-AISLE-A should list 2 racks, got {rows(page).count()}")
    page.evaluate("selectNode('rack','R-A01')"); page.wait_for_timeout(80)
    # rack level: 2 locations + 1 quick-add row
    chips = page.locator(".drill-chip").count()
    check(chips == 5, f"rack breadcrumb should have 5 chips, got {chips}")
    nloc = page.evaluate("()=>LOCATIONS.filter(l=>l.parent_type==='rack'&&l.rack_id==='R-A01').length")
    check(nloc == 2, f"R-A01 should have 2 locations in seed, got {nloc}")

def t03_flat_all_locations(page):
    """Location stat card -> flat view; 17 total; path column; search + type filter."""
    fresh(page)
    page.locator(".stat.is-click").click()
    page.wait_for_timeout(120)
    count_txt = page.locator(".ph-count").inner_text()
    check("17" in count_txt, f"flat view count not 17: {count_txt!r}")
    heads = page.locator(".card .table thead th").all_inner_texts()
    check(any("โครงสร้าง" in h for h in heads), f"flat view missing path column: {heads}")
    page.fill("#flt-search", "PACK")
    page.wait_for_timeout(120)
    check(rows(page).count() == 2, f"search 'PACK' should show 2 rows, got {rows(page).count()}")
    page.fill("#flt-search", "")
    page.evaluate("setFilter('type','PACK')")
    page.wait_for_timeout(120)
    check(rows(page).count() == 2, f"type=PACK should show 2 rows, got {rows(page).count()}")

def t04_area_tabs_racks_vs_direct(page):
    """Area without allows_direct -> racks only (no seg tab); A-FM -> seg + Location-ตรง + quick-add."""
    fresh(page)
    page.evaluate("selectNode('area','A-AISLE-A')"); page.wait_for_timeout(80)
    check(page.locator(".card-head .seg").count() == 0, "non-direct area wrongly shows racks/direct seg tabs")
    page.evaluate("selectNode('area','A-FM')"); page.wait_for_timeout(80)
    check(page.locator(".card-head .seg").count() == 1, "allows_direct area missing racks/direct seg tabs")
    page.evaluate("setAreaTab('locs')"); page.wait_for_timeout(80)
    check(page.locator("#qa-code").count() == 1, "area-direct location tab missing quick-add row")
    ndirect = page.evaluate("()=>LOCATIONS.filter(l=>l.parent_type==='area'&&l.area_id==='A-FM').length")
    check(ndirect == 2, f"A-FM should have 2 direct locations, got {ndirect}")

def t05_hierarchy_tree_shares_sel(page):
    """hierarchy view: tree explorer + node summary; selectNode updates both (shared state.sel)."""
    fresh(page)
    page.evaluate("setView('hierarchy')"); page.wait_for_timeout(100)
    check(page.locator(".explorer .tree-body").count() == 1, "hierarchy view missing tree explorer")
    check(page.locator(".tree-root-row").count() == 1, "tree missing root row")
    page.evaluate("selectNode('warehouse','WH-01')"); page.wait_for_timeout(100)
    title = page.locator(".explorer .pane:last-child .ds-title").inner_text()
    check("บางนา" in title, f"node summary not showing selected WH: {title!r}")
    selrows = page.locator(".tree-body .tn-row.is-sel").count()
    check(selrows >= 1, "tree does not mark selected node (shared state.sel)")

def t06_warehouse_geo_cascade(page):
    """province->district->subdistrict->postcode auto DISABLED(grey); changing province clears lower."""
    open_wh_create(page)
    check(page.locator("#f-postcode").is_disabled(), "postcode field not disabled (greyed)")
    page.select_option("#f-province", "สมุทรปราการ"); page.wait_for_timeout(90)
    check(page.locator("#f-district").is_enabled(), "district not enabled after province")
    page.select_option("#f-district", "บางพลี"); page.wait_for_timeout(90)
    check(page.locator("#f-subdistrict").is_enabled(), "subdistrict not enabled after district")
    page.select_option("#f-subdistrict", "บางพลีใหญ่"); page.wait_for_timeout(90)
    pc = page.locator("#f-postcode").input_value()
    check(pc == "10540", f"postcode not auto-filled (expected 10540, got {pc!r})")
    # change upper -> lower cleared
    page.select_option("#f-province", "ลำพูน"); page.wait_for_timeout(90)
    d = page.locator("#f-district").input_value()
    pc2 = page.locator("#f-postcode").input_value()
    check(d == "", f"district not cleared after province change: {d!r}")
    check(pc2 == "", f"postcode not cleared after province change: {pc2!r}")

def t07_zone_temp_and_rack_dims(page):
    """zone temp range toggle reveals min/max; rack has R/C/L editable fields."""
    fresh(page)
    page.evaluate("openDrawer('create','zone',null)")
    page.wait_for_selector("#f-code", timeout=4000)
    check(page.locator("#f-temp-min").count() == 0, "temp min shown before enabling temp control")
    page.evaluate("toggleFormFlag('temp_controlled')"); page.wait_for_timeout(80)
    check(page.locator("#f-temp-min").count() == 1 and page.locator("#f-temp-max").count() == 1,
          "temp min/max not revealed after toggle")
    fresh(page)
    page.evaluate("openDrawer('create','rack',null)")
    page.wait_for_selector("#f-rows", timeout=4000)
    for fid in ["#f-rows", "#f-cols", "#f-levels"]:
        check(page.locator(fid).is_editable(), f"rack dim field {fid} not editable")

def t08_location_wizard_two_steps(page):
    """2-step wizard; parent XOR (rack vs area); step2 has storage_uom/cap/behavior flags."""
    fresh(page)
    page.evaluate("selectNode('rack','R-A01')"); page.wait_for_timeout(60)
    page.evaluate("openDrawer('create','location',null)")
    page.wait_for_selector("#f-code", timeout=4000)
    # parent XOR: default rack context -> rack select present, area select absent
    check(page.locator("#f-rack").count() == 1, "wizard step1 missing rack select for rack-parent")
    page.evaluate("setLocParentType('area')"); page.wait_for_timeout(80)
    check(page.locator("#f-area").count() == 1 and page.locator("#f-rack").count() == 0,
          "parent XOR failed: area select not swapped in")
    page.evaluate("setLocParentType('rack')"); page.wait_for_timeout(80)
    page.fill("#f-code", "A-01-NEWBIN-1")
    page.locator(".drawer-footer .btn-primary", has_text="ถัดไป").click()
    page.wait_for_selector("#f-cap-val", timeout=4000)
    check(page.locator(".step-dot").nth(1).get_attribute("class").find("is-active") >= 0,
          "step 2 dot not active after ถัดไป")
    check(page.locator("#f-storage-uom").count() == 1, "step2 missing storage_uom select")
    check(page.locator(".drawer-body .toggle-field").count() >= 6, "step2 missing behavior/mixing flags")

def _open_loc_wizard_under_rack(page, rack="R-A01"):
    fresh(page)
    page.evaluate(f"selectNode('rack','{rack}')"); page.wait_for_timeout(60)
    page.evaluate("openDrawer('create','location',null)")
    page.wait_for_selector("#f-code", timeout=4000)

def t09_location_validation(page):
    """VR: code-unique-in-parent; parent=area requires allows_direct; cap>0.
    Driven through the real wizard DOM (captureForm reads live fields)."""
    # dup code within same rack (L001 = 'A-01-R1-C2-L3' under R-A01)
    _open_loc_wizard_under_rack(page)
    page.fill("#f-code", "A-01-R1-C2-L3")
    page.locator(".drawer-footer .btn-primary", has_text="ถัดไป").click()
    page.wait_for_selector("#f-cap-val", timeout=4000)
    page.fill("#f-cap-val", "1")
    page.locator(".drawer-footer .btn-primary", has_text="ยืนยันสร้าง").click()
    msg = toast_text(page)
    check("รหัสซ้ำ" in msg, f"dup-code-in-parent not blocked: {msg!r}")
    # parent=area but area disallows direct (A-AISLE-A allows_direct=false) -> locNext blocks
    fresh(page)
    page.evaluate("openDrawer('create','location',null)")
    page.wait_for_selector("#f-code", timeout=4000)
    page.evaluate("setLocParentType('area')"); page.wait_for_timeout(80)
    page.select_option("#f-area", "A-AISLE-A"); page.wait_for_timeout(80)
    page.fill("#f-code", "X1")
    page.locator(".drawer-footer .btn-primary", has_text="ถัดไป").click()
    msg = toast_text(page)
    check("ไม่อนุญาต" in msg, f"area-without-allows_direct not blocked: {msg!r}")
    # cap<=0
    _open_loc_wizard_under_rack(page)
    page.fill("#f-code", "A-01-NEW9")
    page.locator(".drawer-footer .btn-primary", has_text="ถัดไป").click()
    page.wait_for_selector("#f-cap-val", timeout=4000)
    page.fill("#f-cap-val", "0")
    page.locator(".drawer-footer .btn-primary", has_text="ยืนยันสร้าง").click()
    msg = toast_text(page)
    check("ความจุต้องมากกว่า 0" in msg, f"cap<=0 not blocked: {msg!r}")

def t10_storage_uom_lock_and_display(page):
    """storage_uom LOCK when hasStock (msg '1 ตำแหน่ง 1 หน่วย'); list column + view drawer show it."""
    fresh(page)
    page.evaluate("openDrawer('edit','location','L001')")  # L001 hasStock=true
    page.wait_for_selector("#f-code", timeout=4000)
    page.evaluate("locNext()"); page.wait_for_selector("#f-storage-uom", timeout=4000)
    disabled = page.locator("#f-storage-uom").is_disabled()
    check(disabled, "storage_uom not locked (disabled) when location hasStock")
    body = page.locator(".drawer-body").inner_text()
    check("1 ตำแหน่ง 1 หน่วย" in body, "hasStock lock message missing")
    # list column present in flat view
    fresh(page)
    page.locator(".stat.is-click").click(); page.wait_for_timeout(120)
    heads = page.locator(".card .table thead th").all_inner_texts()
    check(any("หน่วยเก็บ" in h for h in heads), f"flat list missing 'หน่วยเก็บ' column: {heads}")
    # view drawer shows storage_uom
    page.evaluate("openView('location','L001')")
    page.wait_for_selector(".drawer-body", timeout=4000)
    vbody = page.locator(".drawer-body").inner_text()
    check("ลัง" in vbody, "view drawer does not show L001 storage_uom (ลัง)")

def t11_status_menu_portal(page):
    """status pill menu portal: 4 statuses, NO 'เต็ม/full' manual; pick inactive -> status+audit+toast."""
    fresh(page)
    page.locator(".stat.is-click").click(); page.wait_for_timeout(120)
    page.locator('[title="คลิกเปลี่ยนสถานะ"]').first.click()
    page.wait_for_selector("#sm-portal-menu", timeout=3000)
    opts = page.locator("#sm-portal-menu .sm-opt")
    check(opts.count() == 4, f"status menu should have 4 options, got {opts.count()}")
    txt = " ".join(opts.all_inner_texts())
    check("เต็ม" not in txt and "full" not in txt.lower(), f"status menu exposes manual 'full': {txt!r}")
    before = audit_len(page, "L001")
    page.locator("#sm-portal-menu .sm-opt", has_text="พักใช้งาน").click()
    msg = toast_text(page)
    st = page.evaluate("()=>LOCATIONS.find(l=>l.id==='L001').status")
    check(st == "inactive", f"status not changed to inactive: {st!r}")
    check(audit_len(page, "L001") == before + 1, "AUDIT not incremented after status change")
    check("L001" in msg or "พัก" in msg or "→" in msg, f"status toast unexpected: {msg!r}")

def t12_status_blocked_reason_modal(page):
    """blocked -> reason modal required -> apply + audit + toast."""
    fresh(page)
    page.locator(".stat.is-click").click(); page.wait_for_timeout(120)
    page.locator('[title="คลิกเปลี่ยนสถานะ"]').first.click()
    page.wait_for_selector("#sm-portal-menu", timeout=3000)
    before = audit_len(page, "L001")
    page.locator("#sm-portal-menu .sm-opt", has_text="บล็อก").click()
    page.wait_for_selector("#sr-reason", timeout=3000)
    # empty reason blocked
    page.evaluate("confirmStatusReason(document.querySelector('.modal-footer .btn-primary'))")
    msg = toast_text(page)
    check("เหตุผล" in msg, f"empty-reason not blocked: {msg!r}")
    page.fill("#sr-reason", "รอซ่อมคาน")
    page.locator(".modal-footer .btn-primary", has_text="ยืนยัน").click()
    page.wait_for_timeout(800)
    st = page.evaluate("()=>LOCATIONS.find(l=>l.id==='L001').status")
    check(st == "blocked", f"status not blocked after reason confirm: {st!r}")
    check(audit_len(page, "L001") == before + 1, "AUDIT not incremented after blocked+reason")

def t13_bulk_select_and_uom_skip(page):
    """bulk bar (flat): 4 status buttons + bulk-uom skips hasStock (count + '1 ตำแหน่ง 1 หน่วย'); clear."""
    fresh(page)
    page.locator(".stat.is-click").click(); page.wait_for_timeout(120)
    # real checkbox click for one, evaluate for the other
    page.locator(".card .table tbody input.chk").first.check()
    page.wait_for_timeout(80)
    check(page.locator(".bulk-bar").count() == 1, "bulk bar not shown after selecting a location")
    btns = " ".join(page.locator(".bulk-bar button").all_inner_texts())
    for lbl in ["ใช้งาน", "พักใช้งาน", "บล็อก", "Freeze"]:
        check(lbl in btns, f"bulk bar missing status button {lbl!r}: {btns!r}")
    # select L002 (no stock) + L003 (hasStock) -> bulk uom skips L003
    page.evaluate("()=>{state.bulkSel.clear();state.bulkSel.add('L002');state.bulkSel.add('L003');render();}")
    page.wait_for_timeout(80)
    page.select_option("#bulk-uom", "กล่อง")
    page.evaluate("bulkUom()")
    msg = toast_text(page)
    check("ข้าม 1" in msg and "1 ตำแหน่ง 1 หน่วย" in msg, f"bulk-uom skip message wrong: {msg!r}")
    u2 = page.evaluate("()=>LOCATIONS.find(l=>l.id==='L002').storage_uom")
    u3 = page.evaluate("()=>LOCATIONS.find(l=>l.id==='L003').storage_uom")
    check(u2 == "กล่อง", f"L002 uom not applied: {u2!r}")
    check(u3 != "กล่อง", f"L003 (hasStock) uom wrongly changed: {u3!r}")
    check(page.locator(".bulk-bar").count() == 0, "selection not cleared after bulk-uom")
    # bulk status apply + clear
    page.evaluate("()=>{state.bulkSel.add('L002');state.bulkSel.add('L005');render();}")
    page.wait_for_timeout(60)
    page.evaluate("bulkStatus('active')")
    page.wait_for_timeout(60)
    check(page.locator(".bulk-bar").count() == 0, "bulk status apply did not clear selection")

def t14_bulk_generation(page):
    """bulk-gen: preset + preview 5 names + total + storage_uom applied + atomic (1 record + audit)."""
    fresh(page)
    page.evaluate("selectNode('area','A-FM')"); page.wait_for_timeout(60)
    page.evaluate("openDrawer('bulk',null,null)")
    page.wait_for_selector("#b-rackPat", timeout=4000)
    pills = page.locator(".code-sample .pill").count()
    check(pills == 5, f"bulk preview should show 5 sample names, got {pills}")
    total = page.evaluate("()=>{const b=state.bulk;return (b.rackQty||0)*(b.rows||0)*(b.cols||0)*(b.levels||0);}")
    pv = page.locator(".preview-num").inner_text().replace(",", "").strip()
    check(str(total) == pv, f"preview total mismatch: preview {pv!r} vs computed {total}")
    # custom pattern via preset then custom edit
    page.evaluate("applyBulkPreset('aisle')"); page.wait_for_timeout(80)
    pat = page.locator("#b-rackPat").input_value()
    check(pat == "AA-{n}", f"preset did not apply rack pattern: {pat!r}")
    page.select_option("#b-storage-uom", "ถุง"); page.wait_for_timeout(60)
    n_before = page.evaluate("()=>LOCATIONS.length")
    page.locator(".drawer-footer .btn-primary", has_text="สร้าง").click()
    page.wait_for_timeout(800)
    n_after = page.evaluate("()=>LOCATIONS.length")
    check(n_after == n_before + 1, f"bulk-gen not atomic single-insert: {n_before}->{n_after}")
    created = page.evaluate("()=>LOCATIONS[0]")
    check(created["storage_uom"] == "ถุง", f"bulk storage_uom not applied: {created.get('storage_uom')!r}")
    aid = page.evaluate("()=>LOCATIONS[0].id")
    hist = page.evaluate("(id)=>AUDIT[id]?AUDIT[id].map(a=>a.t).join('|'):''", aid)
    check("bulk-gen" in hist, f"bulk-gen audit entry missing: {hist!r}")

def t15_quick_add_rack(page):
    """quick-add under rack: new code -> insert + audit; duplicate code guarded."""
    fresh(page)
    page.evaluate("selectNode('rack','R-A01')"); page.wait_for_timeout(80)
    n0 = page.evaluate("()=>LOCATIONS.length")
    page.fill("#qa-code", "A-01-R4-C9-L9")
    page.locator(".qa-row .btn-primary", has_text="เพิ่มเร็ว").click()
    page.wait_for_timeout(300)
    n1 = page.evaluate("()=>LOCATIONS.length")
    check(n1 == n0 + 1, f"quick-add did not insert a location: {n0}->{n1}")
    newid = page.evaluate("()=>LOCATIONS[0].id")
    hist = page.evaluate("(id)=>AUDIT[id]?AUDIT[id].map(a=>a.t).join('|'):''", newid)
    check("quick add" in hist, f"quick-add audit entry missing: {hist!r}")
    # dup guard
    page.fill("#qa-code", "A-01-R1-C2-L3")  # L001 existing code in R-A01
    page.locator(".qa-row .btn-primary", has_text="เพิ่มเร็ว").click()
    msg = toast_text(page)
    check("รหัสซ้ำ" in msg, f"quick-add dup not guarded: {msg!r}")

def t16_quick_add_area_direct(page):
    """quick-add under area-direct tab inserts a location."""
    fresh(page)
    page.evaluate("selectNode('area','A-FM')"); page.wait_for_timeout(60)
    page.evaluate("setAreaTab('locs')"); page.wait_for_timeout(80)
    n0 = page.evaluate("()=>LOCATIONS.length")
    page.fill("#qa-code", "FM-QA-77")
    page.locator(".qa-row .btn-primary", has_text="เพิ่มเร็ว").click()
    page.wait_for_timeout(300)
    n1 = page.evaluate("()=>LOCATIONS.length")
    check(n1 == n0 + 1, f"area-direct quick-add did not insert: {n0}->{n1}")
    created = page.evaluate("()=>LOCATIONS[0]")
    check(created["parent_type"] == "area" and created["area_id"] == "A-FM",
          f"quick-add parent linkage wrong: {created.get('parent_type')}/{created.get('area_id')}")

def t17_rbac_and_actions(page):
    """canManage=true -> row actions include view+edit+delete; add button present."""
    fresh(page)
    cm = page.evaluate("()=>canManage")
    check(cm is True, "canManage should be true for warehouse_manager")
    ra = page.locator(".card .table tbody tr").first.locator(".row-actions .ra-btn").count()
    check(ra == 3, f"row actions should have view+edit+delete (3), got {ra}")
    # PM/BA: create button moved INTO the card's filter-bar, right-aligned (.filter-actions)
    check(page.locator(".card .filter-bar .filter-actions .btn-primary").count() >= 1, "create button not in filter-bar (right-aligned)")
    check(page.locator(".ph-actions").count() == 0, "ph-actions header slot should be gone (button moved to filter-bar)")

def t18_delete_guards(page):
    """delete blocked when children exist / location hasStock; decommission when clean."""
    # warehouse with zones -> blocked
    fresh(page)
    page.evaluate("openModal('warehouse','WH-01')")
    page.wait_for_selector(".modal-footer", timeout=3000)
    page.evaluate("confirmModal()")
    msg = toast_text(page)
    check("ยังมี Zone" in msg, f"WH delete not blocked by child zones: {msg!r}")
    still = page.evaluate("()=>!!WAREHOUSES.find(w=>w.id==='WH-01')")
    check(still, "WH-01 wrongly deleted despite child zones")
    # location with stock -> decommission blocked
    fresh(page)
    page.evaluate("openModal('location','L001')")  # hasStock
    page.wait_for_selector(".modal-footer", timeout=3000)
    page.evaluate("confirmModal()")
    msg = toast_text(page)
    check("สต็อก" in msg, f"location w/ stock decommission not blocked: {msg!r}")
    # clean location -> decommission ok
    fresh(page)
    page.evaluate("openModal('location','L002')")  # no stock
    page.wait_for_selector(".modal-footer", timeout=3000)
    page.locator(".modal-footer .btn-danger").click()
    page.wait_for_timeout(300)
    st = page.evaluate("()=>LOCATIONS.find(l=>l.id==='L002').status")
    check(st == "decommissioned", f"clean location not decommissioned: {st!r}")

def t19_branch_portal(page):
    """UX-01: branch list portals to <body>, floats above drawer, attached below input, reflows on scroll, closes."""
    open_wh_create(page)
    open_branch_list(page)
    parent = page.evaluate("()=>document.getElementById('branch-portal').parentElement.tagName")
    check(parent == "BODY", f"branch portal not a body-level child (parent={parent!r})")
    opts = page.locator("#branch-portal .mb-opt").count()
    check(opts == 3, f"branch list should show 3 active branches, got {opts}")
    # floats above drawer content
    inside = page.evaluate("""()=>{const p=document.getElementById('branch-portal').getBoundingClientRect();
        const el=document.elementFromPoint(p.left+p.width/2, p.top+8); return !!(el&&el.closest('#branch-portal'));}""")
    check(inside, "branch portal is clipped/behind drawer content")
    def gap():
        return page.evaluate("""()=>{const i=document.getElementById('f-branch-combo').getBoundingClientRect();
            const p=document.getElementById('branch-portal').getBoundingClientRect();return {d:p.top-i.bottom};}""")
    check(abs(gap()["d"] - 4) < 6, f"portal not attached ~4px below input: gap={gap()['d']}")
    # reflow after scrolling drawer body
    page.evaluate("()=>{document.querySelector('.drawer-body').scrollTop=90;}")
    page.wait_for_timeout(120)
    check(abs(gap()["d"] - 4) < 8, f"portal lost attachment after drawer scroll: gap={gap()['d']}")
    # close on select
    click_branch_opt(page, "00001")
    page.wait_for_timeout(120)
    check(page.locator("#branch-portal").count() == 0, "portal not closed after select")
    check(page.evaluate("()=>state.form.branch_id") == 2, "select did not store branch_id=2")
    val = page.locator("#f-branch-search").input_value()
    check("00001" in val and "ขอนแก่น" in val, f"input not showing selected label: {val!r}")
    # reopen + outside click closes
    open_branch_list(page)
    page.locator(".drawer-title").click()
    page.wait_for_timeout(120)
    check(page.locator("#branch-portal").count() == 0, "portal not closed on outside-click")

def t20_branch_keyboard_empty_esc(page):
    """keyboard ArrowDown/Enter selects; empty 'ไม่พบ' state; Esc closes list ONLY (drawer stays)."""
    # keyboard select (3rd active branch)
    open_wh_create(page)
    open_branch_list(page)
    page.keyboard.press("ArrowDown"); page.wait_for_timeout(80)
    page.keyboard.press("ArrowDown"); page.wait_for_timeout(80)
    page.keyboard.press("Enter")
    page.wait_for_timeout(100)
    bid = page.evaluate("()=>state.form.branch_id")
    check(bid == 3, f"ArrowDown x2 + Enter should select branch id 3, got {bid}")
    # empty state
    open_wh_create(page)
    page.click("#f-branch-search")
    page.fill("#f-branch-search", "ไม่มีสาขานี้")
    page.wait_for_timeout(120)
    check(page.locator("#branch-portal .mb-empty").count() == 1, "no-match empty state not shown")
    check("ไม่พบ" in page.locator("#branch-portal .mb-empty").inner_text(), "empty state text missing 'ไม่พบ'")
    # Esc closes list only, drawer stays (#94.3)
    open_wh_create(page)
    open_branch_list(page)
    page.keyboard.press("Escape")
    page.wait_for_timeout(120)
    check(page.locator("#branch-portal").count() == 0, "Esc did not close branch list")
    check(page.evaluate("()=>state.drawer.open") is True, "Esc wrongly closed the drawer (should keep it)")
    check(page.locator("#f-code").count() == 1, "drawer body gone after Esc on branch list")

def t21_branch_active_only_filter(page):
    """picker lists only 3 active; inactive 'สาขาระยอง' absent; branchLabel(4) still resolves snapshot."""
    open_wh_create(page)
    open_branch_list(page)
    txt = " ".join(page.locator("#branch-portal .mb-opt").all_inner_texts())
    check("สำนักงานใหญ่" in txt and "ขอนแก่น" in txt and "เชียงใหม่" in txt, f"active branches missing: {txt!r}")
    check("ระยอง" not in txt, f"inactive branch สาขาระยอง wrongly listed: {txt!r}")
    lbl = page.evaluate("()=>branchLabel(4)")
    check("00003" in lbl and "ระยอง" in lbl, f"branchLabel(4) snapshot did not resolve inactive branch: {lbl!r}")

def t22_branch_required_and_stored(page):
    """branch required at create -> toast; save stores numeric branch_id; list + view drawer show branch."""
    open_wh_create(page)
    page.fill("#f-code", "WH-TEST")
    page.fill("#f-name", "คลังทดสอบ")
    page.locator(".drawer-footer .btn-primary").click()
    msg = toast_text(page)
    check("สาขา" in msg, f"missing-branch not blocked at create: {msg!r}")
    check(page.evaluate("()=>WAREHOUSES.length") == 2, "warehouse wrongly created without branch")
    # now pick a branch + save
    page.click("#f-branch-search")
    page.wait_for_selector("#branch-portal .mb-opt", timeout=3000)
    click_branch_opt(page, "00001")
    page.wait_for_timeout(100)
    page.locator(".drawer-footer .btn-primary").click()
    # create defers closeDrawer (busySubmit 550ms + 280ms close) — wait until it fully closes
    page.wait_for_function("()=>state.drawer.open===false", timeout=5000)
    check(page.evaluate("()=>WAREHOUSES.length") == 3, "warehouse not created with branch")
    newb = page.evaluate("()=>{const w=WAREHOUSES.find(x=>x.code==='WH-TEST');return {t:typeof w.branch_id,v:w.branch_id};}")
    check(newb["t"] == "number" and newb["v"] == 2, f"branch_id not stored as numeric 2: {newb}")
    # list column shows branch of new WH (branch cell only renders at root level)
    page.evaluate("selectNode('root',null)"); page.wait_for_timeout(120)
    listtxt = page.evaluate("()=>document.querySelector('#page-content').innerText")
    check("WH-TEST" in listtxt and "ขอนแก่น" in listtxt, "new WH branch not shown in root list")
    # view drawer shows branch
    wid = page.evaluate("()=>WAREHOUSES.find(x=>x.code==='WH-TEST').id")
    page.evaluate("(id)=>openView('warehouse',id)", wid)
    page.wait_for_selector(".drawer-body", timeout=4000)
    vbody = page.locator(".drawer-body").inner_text()
    check("สาขาสังกัด" in vbody and "ขอนแก่น" in vbody, "view drawer missing branch info")

def t23_audit_on_mutations(page):
    """AUDIT gains an entry on create WH, edit WH, and create location."""
    # create warehouse
    open_wh_create(page)
    page.fill("#f-code", "WH-AUD")
    page.fill("#f-name", "คลังออดิท")
    page.evaluate("()=>{state.form.branch_id=1;}")
    page.locator(".drawer-footer .btn-primary").click()
    page.wait_for_timeout(800)
    nid = page.evaluate("()=>state.sel.id")
    check(audit_len(page, nid) >= 1, "no AUDIT entry after warehouse create")
    hist = page.evaluate("(id)=>AUDIT[id].map(a=>a.t).join('|')", nid)
    check("สร้างรายการ" in hist, f"create audit label wrong: {hist!r}")
    # edit warehouse WH-01 (no seed audit -> becomes 1)
    fresh(page)
    b = audit_len(page, "WH-01")
    page.evaluate("openDrawer('edit','warehouse','WH-01')")
    page.wait_for_selector("#f-code", timeout=4000)
    page.evaluate("()=>{state.form.name='คลังกลาง บางนา (แก้ไข)';}")
    page.locator(".drawer-footer .btn-primary").click()
    page.wait_for_timeout(800)
    check(audit_len(page, "WH-01") == b + 1, "edit warehouse did not add AUDIT entry")
    ehist = page.evaluate("()=>AUDIT['WH-01'].map(a=>a.t).join('|')")
    check("แก้ไขข้อมูล" in ehist, f"edit audit label wrong: {ehist!r}")
    # create location
    fresh(page)
    page.evaluate("selectNode('rack','R-A01')"); page.wait_for_timeout(60)
    page.evaluate("openDrawer('create','location',null)")
    page.wait_for_selector("#f-code", timeout=4000)
    page.evaluate("()=>{Object.assign(state.form,{parent_type:'rack',rack_id:'R-A01',code:'A-01-AUD1',cap_val:1});}")
    page.evaluate("submitLoc(null)")
    page.wait_for_timeout(800)
    lid = page.evaluate("()=>LOCATIONS[0].id")
    lhist = page.evaluate("(id)=>AUDIT[id]?AUDIT[id].map(a=>a.t).join('|'):''", lid)
    check("สร้างตำแหน่ง" in lhist, f"create-location audit missing: {lhist!r}")

def t24_submit_loading_and_double_guard(page):
    """UX-03: submit disables + spinner; rapid double-submit creates only ONE record."""
    # spinner + disabled
    open_wh_create(page)
    page.fill("#f-code", "WH-SPIN")
    page.fill("#f-name", "สปิน")
    page.evaluate("()=>{state.form.branch_id=1;}")
    page.locator(".drawer-footer .btn-primary").click()
    # immediately after click the button should be disabled + show spinner
    disabled = page.locator(".drawer-footer .btn-primary").is_disabled()
    spin = page.locator(".drawer-footer .btn-primary .spin").count()
    check(disabled, "submit button not disabled during busy state")
    check(spin == 1, "submit button missing spinner during busy state")
    page.wait_for_timeout(800)
    # double-submit guard
    open_wh_create(page)
    page.fill("#f-code", "WH-DUP")
    page.fill("#f-name", "กันซ้ำ")
    n0 = page.evaluate("()=>WAREHOUSES.length")
    page.evaluate("()=>{state.form.branch_id=1;const b=document.querySelector('.drawer-footer .btn-primary');submitForm(b);submitForm(b);}")
    page.wait_for_timeout(800)
    n1 = page.evaluate("()=>WAREHOUSES.length")
    check(n1 == n0 + 1, f"double-submit created {n1-n0} records (expected 1)")

def t25_esc_chain(page):
    """UX-08 Esc order: status menu closes first; modal before drawer; branch list before drawer."""
    # status menu first
    fresh(page)
    page.locator(".stat.is-click").click(); page.wait_for_timeout(120)
    page.locator('[title="คลิกเปลี่ยนสถานะ"]').first.click()
    page.wait_for_selector("#sm-portal-menu", timeout=3000)
    page.keyboard.press("Escape")
    page.wait_for_timeout(120)
    check(page.locator("#sm-portal-menu").count() == 0, "Esc did not close status menu first")
    # modal before drawer
    fresh(page)
    page.evaluate("openView('warehouse','WH-01')")
    page.wait_for_selector(".drawer-body", timeout=4000)
    page.locator(".drawer-header-actions .btn-danger").click()
    page.wait_for_selector(".modal-footer", timeout=3000)
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    check(page.evaluate("()=>state.modal.open") is False, "Esc #1 did not close modal")
    check(page.evaluate("()=>state.drawer.open") is True, "Esc #1 wrongly closed drawer (modal should go first)")
    page.keyboard.press("Escape")
    page.wait_for_timeout(400)
    check(page.evaluate("()=>state.drawer.open") is False, "Esc #2 did not close drawer")
    # branch list before drawer
    open_wh_create(page)
    open_branch_list(page)
    page.keyboard.press("Escape")
    page.wait_for_timeout(120)
    check(page.locator("#branch-portal").count() == 0, "Esc did not close branch list")
    check(page.evaluate("()=>state.drawer.open") is True, "Esc wrongly closed drawer instead of branch list")

def t26_ci_drift_gone(page):
    """UX-05: no navy/blue rgba(11,29,58 / rgba(11,92,255 in source or computed styles."""
    check("rgba(11,29,58" not in HTML_SRC, "source still contains navy rgba(11,29,58")
    check("rgba(11,92,255" not in HTML_SRC, "source still contains blue rgba(11,92,255")
    fresh(page)
    hit = page.evaluate("""()=>{const s=[...document.styleSheets].flatMap(ss=>{try{return [...ss.cssRules]}catch(e){return[]}}).map(r=>r.cssText).join(' ');
        return s.includes('rgba(11, 29, 58')||s.includes('rgba(11,29,58')||s.includes('rgba(11, 92, 255')||s.includes('rgba(11,92,255');}""")
    check(hit is False, "computed stylesheet still references banned navy/blue rgba")

def t27_thai_font_link(page):
    """UX-06: <link> to Noto+Sans+Thai present in <head>."""
    check("Noto+Sans+Thai" in HTML_SRC, "source missing Noto+Sans+Thai link")
    fresh(page)
    ok = page.evaluate("""()=>!!document.querySelector('head link[href*="Noto+Sans+Thai"]')""")
    check(ok, "no <head> <link> to Noto+Sans+Thai in DOM")

def t28_icon_audit(page):
    """no un-rendered <i data-lucide> and no empty lucide svg across list/form/combo/menu/toast."""
    def audit(where):
        leftover = page.locator("i[data-lucide]:visible").count()
        check(leftover == 0, f"[{where}] {leftover} un-rendered <i data-lucide>")
        empties = page.evaluate("""()=>{const svgs=[...document.querySelectorAll('svg.lucide')];
            return svgs.filter(s=>s.getClientRects().length&&!s.innerHTML.trim()).length;}""")
        check(empties == 0, f"[{where}] {empties} empty lucide svg")
    fresh(page)
    audit("list")
    page.evaluate("openDrawer('create','warehouse',null)")
    page.wait_for_selector("#f-code", timeout=4000)
    page.click("#f-branch-search")
    page.wait_for_selector("#branch-portal .mb-opt", timeout=3000)
    audit("wh-form+branch-combo")
    fresh(page)
    page.locator(".stat.is-click").click(); page.wait_for_timeout(120)
    page.locator('[title="คลิกเปลี่ยนสถานะ"]').first.click()
    page.wait_for_selector("#sm-portal-menu", timeout=3000)
    audit("statusmenu")
    page.evaluate("()=>showToast('ทดสอบไอคอน','success')")
    page.wait_for_selector("#toast.is-visible", timeout=2000)
    audit("toast")

def t29_drawer_rerender_keeps_open(page):
    """render() while a drawer is open keeps it open + preserves drawer-body scroll (#29 / UX).
    Uses the (tall, reliably scrollable) bulk-generation drawer."""
    fresh(page)
    page.evaluate("selectNode('area','A-FM')"); page.wait_for_timeout(60)
    page.evaluate("openDrawer('bulk',null,null)")
    page.wait_for_selector("#b-rackPat", timeout=4000)
    page.evaluate("()=>{document.querySelector('.drawer-body').scrollTop=120;}")
    page.wait_for_timeout(80)
    target = page.evaluate("()=>document.querySelector('.drawer-body').scrollTop")
    check(target > 0, f"bulk drawer body not scrollable (scrollTop stayed {target}) — test premise")
    page.evaluate("render()")
    page.wait_for_timeout(150)
    check(page.evaluate("()=>state.drawer.open") is True, "drawer closed after re-render")
    open_cls = page.evaluate("()=>document.getElementById('drawer').classList.contains('is-open')")
    check(open_cls, "drawer lost is-open class after re-render")
    sc = page.evaluate("()=>document.querySelector('.drawer-body').scrollTop")
    check(sc == target, f"drawer scroll not preserved after re-render (got {sc}, expected {target})")

def t30_branch_mouse_click_create(page):
    """REGRESSION (mouse path): CREATE drawer — open branch dropdown, REAL mouse-click the
    '00001 · สาขาขอนแก่น' option -> selects (branch_id=2), input shows label, portal closes.
    Old onclick-only code passed clean synthetic .click() but was fragile; this asserts the
    real down->up->click coordinate click reliably selects."""
    open_wh_create(page)
    open_branch_list(page)
    check(page.evaluate("()=>state.form.branch_id") in (None, "", 0), "branch_id should start empty in create")
    mouse_click_branch_opt(page, "00001")
    page.wait_for_timeout(120)
    check(page.evaluate("()=>state.form.branch_id") == 2, "real mouse-click did not select branch_id=2 (create)")
    check(page.locator("#branch-portal").count() == 0, "portal not closed after mouse-click select (create)")
    val = page.locator("#f-branch-search").input_value()
    check("00001" in val and "ขอนแก่น" in val, f"input not showing selected label after mouse-click: {val!r}")

def t31_branch_mouse_click_edit_change(page):
    """REGRESSION (mouse path): EDIT drawer — WH-01 starts branch_id=1; open dropdown and REAL
    mouse-click a DIFFERENT active branch ('00001') -> branch_id changes to 2, field updates,
    portal closes. Covers the 'edit' half of the reported add-AND-edit bug."""
    fresh(page)
    page.evaluate("openDrawer('edit','warehouse','WH-01')")
    page.wait_for_selector("#f-code", timeout=5000)
    check(page.evaluate("()=>state.form.branch_id") == 1, "edit WH-01 should preload branch_id=1")
    page.click("#f-branch-search")
    page.wait_for_selector("#branch-portal .mb-opt", timeout=3000)
    mouse_click_branch_opt(page, "00001")
    page.wait_for_timeout(120)
    check(page.evaluate("()=>state.form.branch_id") == 2, "real mouse-click did not change branch_id 1->2 (edit)")
    check(page.locator("#branch-portal").count() == 0, "portal not closed after mouse-click select (edit)")
    val = page.locator("#f-branch-search").input_value()
    check("00001" in val and "ขอนแก่น" in val, f"edit field not updated to new branch after mouse-click: {val!r}")

def t32_branch_mouse_click_inner_target(page):
    """REGRESSION (mouse path): clicking the inner icon (.mb-ic) OR the text (.mb-nm) of an
    option — not just the button padding — still selects (event bubbles to the button)."""
    # inner text span
    open_wh_create(page)
    open_branch_list(page)
    mouse_click_branch_opt(page, "00002", inner=".mb-nm")
    page.wait_for_timeout(120)
    check(page.evaluate("()=>state.form.branch_id") == 3, "mouse-click on .mb-nm text did not select (id 3)")
    # inner icon span
    open_wh_create(page)
    open_branch_list(page)
    mouse_click_branch_opt(page, "00001", inner=".mb-ic")
    page.wait_for_timeout(120)
    check(page.evaluate("()=>state.form.branch_id") == 2, "mouse-click on .mb-ic icon did not select (id 2)")

def t33_branch_mouse_click_survives_midclick_rerender(page):
    """REGRESSION (root-cause guard): the reported bug is that the pressed option node is
    replaced between mousedown and mouseup, so the trailing `click` never fires and an
    onclick-based select is silently dropped (keyboard was unaffected). Inject that exact race
    — a portal re-sync on mousedown — then perform a REAL mouse down->up. Selecting on
    mousedown must still record branch_id. This FAILS on the old onclick code and PASSES on the
    mousedown-select fix."""
    open_wh_create(page)
    open_branch_list(page)
    page.evaluate("""()=>{const p=document.getElementById('branch-portal');
        p.addEventListener('mousedown', ()=>{ if(state.branchCombo.open) syncBranchPortal(); }, true);}""")
    loc = branch_opt(page, "00001")
    bb = loc.bounding_box()
    page.mouse.move(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2)
    page.mouse.down()
    page.wait_for_timeout(60)
    page.mouse.up()
    page.wait_for_timeout(120)
    check(page.evaluate("()=>state.form.branch_id") == 2,
          "selection lost when portal node is replaced mid-click (onclick-not-firing race)")

# ================================================================== RUNNER =======
TESTS = [
    ("T01", "root list: 2 WH rows + 5 stats + สาขา column + branch cell", t01_list_and_stats),
    ("T02", "drill 5 levels (row-click + evaluate) + 5 breadcrumb chips", t02_drill_five_levels),
    ("T03", "flat all-locations: 17 total + path column + search/type filter", t03_flat_all_locations),
    ("T04", "area tab: racks-only vs allows_direct seg + quick-add", t04_area_tabs_racks_vs_direct),
    ("T05", "hierarchy tree + node summary share state.sel", t05_hierarchy_tree_shares_sel),
    ("T06", "warehouse geo cascade + postcode readonly + clear-on-change", t06_warehouse_geo_cascade),
    ("T07", "zone temp range toggle + rack R/C/L fields", t07_zone_temp_and_rack_dims),
    ("T08", "location wizard 2 steps + parent XOR + step2 fields", t08_location_wizard_two_steps),
    ("T09", "location validation: dup-code / area-direct / cap>0", t09_location_validation),
    ("T10", "storage_uom LOCK on hasStock + list col + view drawer", t10_storage_uom_lock_and_display),
    ("T11", "status menu portal: 4 statuses (no full) + apply + audit", t11_status_menu_portal),
    ("T12", "blocked -> reason modal required -> apply + audit", t12_status_blocked_reason_modal),
    ("T13", "bulk bar 4 statuses + bulk-uom skips hasStock + clear", t13_bulk_select_and_uom_skip),
    ("T14", "bulk-gen: preset + 5-name preview + total + uom + atomic", t14_bulk_generation),
    ("T15", "quick-add (rack): insert + audit + dup guard", t15_quick_add_rack),
    ("T16", "quick-add (area-direct): insert + parent linkage", t16_quick_add_area_direct),
    ("T17", "RBAC canManage + row actions (view/edit/delete)", t17_rbac_and_actions),
    ("T18", "delete guards: child zones / hasStock / clean decommission", t18_delete_guards),
    ("T19", "branch portal to <body> + floats above + reflow + close", t19_branch_portal),
    ("T20", "branch keyboard select + empty state + Esc keeps drawer", t20_branch_keyboard_empty_esc),
    ("T21", "branch picker active-only + branchLabel snapshot", t21_branch_active_only_filter),
    ("T22", "branch required + numeric branch_id + list/view show", t22_branch_required_and_stored),
    ("T23", "AUDIT increments on create/edit WH + create location", t23_audit_on_mutations),
    ("T24", "submit spinner+disabled + double-submit guard", t24_submit_loading_and_double_guard),
    ("T25", "Esc chain: menu > modal > drawer / branch list > drawer", t25_esc_chain),
    ("T26", "CI drift gone: no navy/blue rgba (source + computed)", t26_ci_drift_gone),
    ("T27", "Thai font <link> Noto+Sans+Thai present", t27_thai_font_link),
    ("T28", "icon audit: no empty/un-rendered lucide icons", t28_icon_audit),
    ("T29", "drawer re-render keeps open + preserves scroll", t29_drawer_rerender_keeps_open),
    ("T30", "branch REAL mouse-click select (create) + label + close", t30_branch_mouse_click_create),
    ("T31", "branch REAL mouse-click change (edit) 1->2 + field update", t31_branch_mouse_click_edit_change),
    ("T32", "branch REAL mouse-click on inner icon/text still selects", t32_branch_mouse_click_inner_target),
    ("T33", "branch mouse-click survives mid-click portal re-render (race)", t33_branch_mouse_click_survives_midclick_rerender),
]

def main():
    passed = 0
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for tid, name, fn in TESTS:
            ctx = browser.new_context(viewport={"width": 1360, "height": 900})
            page = ctx.new_page()
            try:
                fn(page)
                print(f"PASS {tid}: {name}", flush=True)
                results.append({"id": tid, "name": name, "pass": True, "reason": ""})
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
                results.append({"id": tid, "name": name, "pass": False, "reason": reason})
            finally:
                ctx.close()
        browser.close()

    total = len(TESTS)
    print("-" * 72, flush=True)
    print(f"E2E ROUND: {passed}/{total} passed", flush=True)
    try:
        with io.open(RESULTS_JSON, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"results JSON -> {RESULTS_JSON}", flush=True)
    except Exception as e:
        print(f"WARN could not write results JSON: {e}", flush=True)
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
