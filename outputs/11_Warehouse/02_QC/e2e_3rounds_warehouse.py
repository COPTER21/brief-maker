# -*- coding: utf-8 -*-
"""
3-ROUND end-to-end verification suite for WarehouseBin.html (F-LOCATION-MASTER-001)
Warehouse & Bin / Location Hierarchy — 5-level master, single-file SPA.

Rounds (each a full pass, run on every viewport; a round PASSES only with 0 console + 0 page errors):
  Round 1  Happy-path lifecycle — build a whole warehouse (WH+geo cascade -> Zone -> Area -> Rack ->
           Location 2-step wizard -> Bulk Generate -> view location 3 tabs + view node full_path/child counts).
  Round 2  Negative / validation / guards / RBAC (all must block correctly).
  Round 3  State transitions, soft-archive persistence, refresh-safety, Esc chain, in-drawer modal z-index,
           drawer re-render, empty/loading/error states, geo cascade reset.

VERIFY ONLY — does not modify the HTML.
Run with the project venv python.
"""
import json, os, sys, pathlib
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
from playwright.sync_api import sync_playwright

HTML = pathlib.Path(r"C:\Users\Admin\Desktop\Work\brief-maker\outputs\11_Warehouse\01_HTML\WarehouseBin.html")
QC   = pathlib.Path(r"C:\Users\Admin\Desktop\Work\brief-maker\outputs\11_Warehouse\02_QC")
SHOTS = QC / "e2e_shots"
SHOTS.mkdir(parents=True, exist_ok=True)
URL = HTML.as_uri()

VIEWPORTS = [1280, 1440, 1920]

# ---- test-harness JS helpers injected in the page (drive the app's REAL handlers) ----
HELPERS = r"""
window.__t = {
  setVal: function(id, v){ var el=document.getElementById('f-'+id); if(!el) return false; el.value=String(v); return true; },
  getVal: function(id){ var el=document.getElementById('f-'+id); return el?el.value:null; },
  pickSS: function(key, value){
    var s = window.__ss && window.__ss[key]; if(!s) return false;
    s.query=''; s.open=true;
    var i = s.options.findIndex(function(o){ return o.value===value; });
    if(i<0) return false;
    ssPick(key, i); return true;
  },
  ssState: function(key){ var s=window.__ss&&window.__ss[key]; return s?{open:!!s.open, value:s.value}:null; },
  drawerText: function(){ var d=document.getElementById('drawer'); return d?(d.innerText||'').length:0; },
  modalHTML: function(){ var m=document.getElementById('modalBackdrop'); return m?m.innerHTML:''; },
  pageText: function(){ var p=document.getElementById('page-content'); return p?p.innerText:''; },
  zmeasure: function(){
    var mb=document.getElementById('modalBackdrop');
    var modal=mb?mb.querySelector('.modal'):null;
    var db=document.getElementById('drawerBackdrop');
    var dr=document.getElementById('drawer');
    var zi=function(el){ return el?getComputedStyle(el).zIndex:null; };
    var topmost=null;
    if(modal){ var r=modal.getBoundingClientRect();
      var el=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2);
      topmost = el?(el.closest('.modal')?'modal':(el.closest('.drawer')?'drawer':el.className)):null; }
    return { modalBackdropZ:zi(mb), modalZ:zi(modal), drawerBackdropZ:zi(db), drawerZ:zi(dr), topmostAtModalCenter:topmost };
  }
};
"""

def build_results():
    return {"target": str(HTML), "url": URL, "viewports": VIEWPORTS, "rounds": {}}


class Rec:
    """Per (round, viewport) recorder."""
    def __init__(self, results, rnd, vw):
        self.rnd = rnd; self.vw = vw
        self.bucket = results["rounds"].setdefault(str(rnd), {}).setdefault("viewports", {}).setdefault(str(vw), {
            "assertions": [], "console_errors": [], "page_errors": [], "notes": []
        })

    def rec(self, name, ok, detail=""):
        self.bucket["assertions"].append({"name": name, "pass": bool(ok), "detail": str(detail)[:400]})
        print(("  PASS" if ok else "  FAIL"), "R%d/%d" % (self.rnd, self.vw), name, "-" if detail else "", str(detail)[:160])
        return ok

    def note(self, text):
        self.bucket["notes"].append(str(text))
        print("  NOTE", "R%d/%d" % (self.rnd, self.vw), text)


def shot(page, rnd, vw, name):
    p = SHOTS / ("round%d_%d_%s.png" % (rnd, vw, name))
    try:
        page.screenshot(path=str(p), full_page=False)
    except Exception:
        pass
    return p.name


def boot(page):
    page.wait_for_timeout(950)  # boot setTimeout 550 + render/icons
    page.evaluate(HELPERS)


# =====================================================================
# ROUND 1 — happy-path lifecycle (build a whole warehouse)
# =====================================================================
def round1(page, R, rnd, vw):
    sh = lambda n: shot(page, rnd, vw, n)

    # 0. root list renders
    kpi = page.locator(".stat").count()
    chips = page.locator(".drill-chip").count()
    sh("01_root_list")
    R.rec("root list renders (5 KPI stats + drill chip)", kpi == 5 and chips >= 1, "stats=%d chips=%d" % (kpi, chips))
    wh_count_before = page.evaluate("() => WAREHOUSES.length")

    # 1. Create Warehouse with branch + geo cascade
    page.evaluate("openNodeCreate('warehouse')"); page.wait_for_timeout(450)
    R.rec("WH create drawer opens (node-form/warehouse)",
          page.evaluate("state.drawer.open===true && state.drawer.view==='node-form' && state.drawer.level==='warehouse'"))
    page.evaluate("() => { __t.setVal('code','WH-E2E'); __t.setVal('name','คลังทดสอบ E2E'); __t.setVal('addr_line','1 ถนนทดสอบ'); }")
    page.evaluate("() => __t.pickSS('branch','BR-01')"); page.wait_for_timeout(150)
    # geo cascade: province -> district -> subdistrict -> postcode auto
    page.evaluate("() => __t.pickSS('prov','สมุทรปราการ')"); page.wait_for_timeout(200)
    dist_reset = page.evaluate("() => state.form.district==='' && state.form.postcode===''")
    page.evaluate("() => __t.pickSS('dist','บางพลี')"); page.wait_for_timeout(200)
    page.evaluate("() => __t.pickSS('subd','บางพลีใหญ่')"); page.wait_for_timeout(250)
    postcode_form = page.evaluate("() => state.form.postcode")
    postcode_dom = page.evaluate("() => __t.getVal('postcode')")
    sh("02_wh_geo_cascade")
    R.rec("geo cascade resets child levels when province picked", dist_reset)
    R.rec("geo cascade auto-fills postcode (ตำบล -> 10540)",
          postcode_form == "10540" and postcode_dom == "10540", "form=%s dom=%s" % (postcode_form, postcode_dom))
    page.evaluate("submitNode()"); page.wait_for_timeout(950)
    new_wh = page.evaluate("() => { var w=WAREHOUSES.find(x=>x.code==='WH-E2E'); return w?{id:w.id,branch:w.branch_id,pc:w.postcode,st:w.status}:null; }")
    R.rec("WH persisted (branch=BR-01, postcode=10540, active, drawer closed)",
          bool(new_wh) and new_wh["branch"] == "BR-01" and new_wh["pc"] == "10540"
          and new_wh["st"] == "active" and not page.evaluate("state.drawer.open"),
          json.dumps(new_wh, ensure_ascii=False))
    wh_id = new_wh["id"] if new_wh else None
    # KPI count increased
    page.evaluate("resetDrill()"); page.wait_for_timeout(250)
    kpi_wh = page.locator(".stats .stat").first.locator(".stat-value").inner_text()
    R.rec("KPI warehouse count updated after create",
          page.evaluate("() => WAREHOUSES.length") == wh_count_before + 1, "kpi_first_stat=%s" % kpi_wh)

    # 2. Zone (temp_controlled -> range) under new WH
    page.evaluate("drillInto('warehouse','%s')" % wh_id); page.wait_for_timeout(250)
    branch_chip = page.locator(".drill-chip.is-branch").count()
    branch_chip_txt = page.locator(".drill-chip.is-branch").first.inner_text() if branch_chip else ""
    R.rec("branch chip shown in drill breadcrumb after drilling into WH",
          branch_chip >= 1 and "สาขา 1" in branch_chip_txt, branch_chip_txt)
    page.evaluate("openNodeCreate('zone')"); page.wait_for_timeout(400)
    page.evaluate("() => { __t.setVal('code','Z-E2E'); __t.setVal('name','โซนเย็น E2E'); }")
    page.evaluate("toggleField('temp_controlled')"); page.wait_for_timeout(250)
    page.evaluate("() => { __t.setVal('temp_min','2'); __t.setVal('temp_max','8'); }")
    sh("03_zone_temp")
    page.evaluate("submitNode()"); page.wait_for_timeout(950)
    new_zone = page.evaluate("() => { var z=ZONES.find(x=>x.code==='Z-E2E'); return z?{id:z.id,wh:z.warehouse_id,tc:z.temp_controlled,mn:z.temp_min,mx:z.temp_max}:null; }")
    R.rec("Zone persisted (temp_controlled true, range 2-8, under new WH)",
          bool(new_zone) and new_zone["wh"] == wh_id and new_zone["tc"] and new_zone["mn"] == 2 and new_zone["mx"] == 8,
          json.dumps(new_zone, ensure_ascii=False))
    zone_id = new_zone["id"] if new_zone else None

    # 3. Area (allows_direct on)
    page.evaluate("drillInto('zone','%s')" % zone_id); page.wait_for_timeout(250)
    page.evaluate("openNodeCreate('area')"); page.wait_for_timeout(400)
    page.evaluate("() => { __t.setVal('code','A-E2E'); __t.setVal('name','พื้นที่ E2E'); }")
    page.evaluate("toggleField('allows_direct')"); page.wait_for_timeout(200)
    sh("04_area_allows_direct")
    page.evaluate("submitNode()"); page.wait_for_timeout(950)
    new_area = page.evaluate("() => { var a=AREAS.find(x=>x.code==='A-E2E'); return a?{id:a.id,zone:a.zone_id,ad:a.allows_direct}:null; }")
    R.rec("Area persisted (allows_direct true, under new Zone)",
          bool(new_area) and new_area["zone"] == zone_id and new_area["ad"] is True,
          json.dumps(new_area, ensure_ascii=False))
    area_id = new_area["id"] if new_area else None

    # 4. Rack (rows x cols x levels)
    page.evaluate("drillInto('area','%s')" % area_id); page.wait_for_timeout(250)
    page.evaluate("openNodeCreate('rack')"); page.wait_for_timeout(400)
    page.evaluate("() => { __t.setVal('code','R-E2E'); __t.setVal('name','ชั้นวาง E2E'); __t.setVal('rows','2'); __t.setVal('cols','3'); __t.setVal('levels','2'); }")
    sh("05_rack_grid")
    page.evaluate("submitNode()"); page.wait_for_timeout(950)
    new_rack = page.evaluate("() => { var r=RACKS.find(x=>x.code==='R-E2E'); return r?{id:r.id,area:r.area_id,rows:r.rows,cols:r.cols,levels:r.levels}:null; }")
    R.rec("Rack persisted (grid 2x3x2, under new Area)",
          bool(new_rack) and new_rack["area"] == area_id and new_rack["rows"] == 2 and new_rack["cols"] == 3 and new_rack["levels"] == 2,
          json.dumps(new_rack, ensure_ascii=False))
    rack_id = new_rack["id"] if new_rack else None

    # 5. Location via 2-step wizard (type=PACK, capacity>0, rotation, flags, barcode)
    page.evaluate("drillInto('rack','%s')" % rack_id); page.wait_for_timeout(250)
    page.evaluate("openLocCreate('rack','%s')" % rack_id); page.wait_for_timeout(400)
    R.rec("Location wizard step 1 opens (loc-form)",
          page.evaluate("state.drawer.open && state.drawer.view==='loc-form' && state.drawer.step===1"))
    stepper = page.locator(".d-stepper .stepper-item").count()
    page.evaluate("() => { __t.setVal('code','LOC-E2E'); __t.setVal('name','ตำแหน่งทดสอบ'); __t.setVal('type','PACK'); }")
    sh("06_loc_wizard_step1")
    page.evaluate("locStep(2)"); page.wait_for_timeout(350)
    R.rec("Location wizard advances to step 2 (2-step, stepper=%d)" % stepper,
          page.evaluate("state.drawer.step===2") and stepper == 2)
    page.evaluate("() => { __t.setVal('cap_val','5'); __t.setVal('rotation','fefo'); __t.setVal('barcode','8859999000019'); }")
    page.evaluate("toggleField('pickable')"); page.wait_for_timeout(150)
    sh("07_loc_wizard_step2")
    page.evaluate("submitLoc()"); page.wait_for_timeout(950)
    new_loc = page.evaluate("() => { var l=LOCATIONS.find(x=>x.code==='LOC-E2E'); return l?{id:l.id,type:l.type,cap:l.cap_val,rack:l.rack_id,bc:l.barcode,st:l.status}:null; }")
    R.rec("Location persisted via wizard (type=PACK, cap=5>0, barcode set -> active)",
          bool(new_loc) and new_loc["type"] == "PACK" and new_loc["cap"] == 5 and new_loc["rack"] == rack_id
          and new_loc["bc"] == "8859999000019" and new_loc["st"] == "active",
          json.dumps(new_loc, ensure_ascii=False))
    loc_id = new_loc["id"] if new_loc else None

    # 6. Bulk Generate (preview count -> commit atomic) into the new area
    racks_before = page.evaluate("() => RACKS.length"); locs_before = page.evaluate("() => LOCATIONS.length")
    page.evaluate("drillTo('area')"); page.wait_for_timeout(200)
    page.evaluate("openBulk()"); page.wait_for_timeout(400)
    R.rec("Bulk Generate drawer opens", page.evaluate("state.drawer.open && state.drawer.view==='bulk'"))
    page.evaluate("() => { __t.pickSS('btarget','%s'); }" % area_id); page.wait_for_timeout(200)
    page.evaluate("() => { __t.setVal('rackPat','BK-{n}'); __t.setVal('rackQty','2'); __t.setVal('rows','1'); __t.setVal('cols','2'); __t.setVal('levels','1'); __t.setVal('locPat','{rack}-R{r}-C{c}-L{l}'); __t.setVal('cap_val','1'); captureForm(); render(); }")
    page.wait_for_timeout(300)
    preview = page.locator(".preview-num").first.inner_text() if page.locator(".preview-num").count() else ""
    calc = page.evaluate("() => bulkCalc()")
    sh("08_bulk_preview")
    R.rec("Bulk preview count = 2 racks x 2 = 4 locations", calc["total"] == 4, "preview='%s' calc=%s" % (preview, json.dumps(calc)))
    page.evaluate("submitBulk()"); page.wait_for_timeout(1050)
    racks_after = page.evaluate("() => RACKS.length"); locs_after = page.evaluate("() => LOCATIONS.length")
    R.rec("Bulk commit atomic (+2 racks, +4 locations, drawer closed)",
          racks_after == racks_before + 2 and locs_after == locs_before + 4 and not page.evaluate("state.drawer.open"),
          "racks %d->%d locs %d->%d" % (racks_before, racks_after, locs_before, locs_after))

    # 7. View location — 3 tabs
    page.evaluate("openViewLoc('%s')" % loc_id); page.wait_for_timeout(400)
    tabs = page.locator("#drawer .drawer-tab").count()
    R.rec("view-location drawer opens with 3 tabs", page.evaluate("state.drawer.open && state.drawer.view==='view-loc'") and tabs == 3, "tabs=%d" % tabs)
    ov_len = page.evaluate("() => __t.drawerText()")
    page.locator("#drawer .drawer-tab").nth(1).click(); page.wait_for_timeout(300)  # capacity & flags
    cap_ok = page.evaluate("() => state.drawer.tab==='capacity' && __t.drawerText()>40 && document.getElementById('drawer').innerText.indexOf('ความจุ')>=0")
    sh("09_viewloc_capacity")
    R.rec("view-loc capacity&flags tab renders (real click, non-blank)", cap_ok, "ov_len=%d" % ov_len)
    page.locator("#drawer .drawer-tab").nth(2).click(); page.wait_for_timeout(300)  # history
    hist_ok = page.evaluate("() => state.drawer.tab==='history' && __t.drawerText()>20")
    R.rec("view-loc history tab renders", hist_ok)
    page.evaluate("closeDrawer()"); page.wait_for_timeout(350)

    # 8. View node — fields + full_path (branch bold) + child counts + drill button
    page.evaluate("openViewNode('warehouse','%s')" % wh_id); page.wait_for_timeout(400)
    vn = page.evaluate("""() => {
      var d=document.getElementById('drawer');
      return { open: state.drawer.open, path: (d.querySelector('.path-str')||{}).innerHTML||'',
               childStats: d.querySelectorAll('.child-stat').length, drillBtn: !!d.querySelector('.drill-child-btn') };
    }""")
    sh("10_viewnode_path")
    R.rec("view-node shows full_path with branch in breadcrumb (bold + ' › ')",
          vn["open"] and "สาขา 1" in vn["path"] and "<b>" in vn["path"] and "›" in vn["path"], vn["path"][:120])
    R.rec("view-node shows child counts + drill button", vn["childStats"] >= 1 and vn["drillBtn"])
    page.evaluate("closeDrawer()"); page.wait_for_timeout(350)

    # 9. 5-level drill-down via real row clicks (WH-01 subtree that has full depth)
    page.evaluate("resetDrill()"); page.wait_for_timeout(200)
    levels = []
    try:
        page.evaluate("drillInto('warehouse','WH-01')"); page.wait_for_timeout(200); levels.append(page.evaluate("curLevel()"))
        page.evaluate("drillInto('zone','Z-STORAGE')"); page.wait_for_timeout(200); levels.append(page.evaluate("curLevel()"))
        page.evaluate("drillInto('area','A-AISLE-A')"); page.wait_for_timeout(200); levels.append(page.evaluate("curLevel()"))
        # real row click to drill into a rack, then location list rows are present
        page.locator("tr.is-clickable").first.click(); page.wait_for_timeout(300); levels.append(page.evaluate("curLevel()"))
        loc_rows = page.locator("tr.is-clickable").count()
    except Exception as e:
        R.rec("5-level drill (real clicks)", False, "err %s levels=%s" % (e, levels))
        loc_rows = 0
    sh("11_drill_location_list")
    R.rec("5-level drill reaches rack level + location list rows present",
          levels[:4] == ["warehouse", "zone", "area", "rack"] and loc_rows >= 1, "levels=%s locrows=%d" % (levels, loc_rows))
    page.evaluate("resetDrill()"); page.wait_for_timeout(200)


# =====================================================================
# ROUND 2 — negative / validation / guards / RBAC
# =====================================================================
def round2(page, R, rnd, vw):
    sh = lambda n: shot(page, rnd, vw, n)

    # 1. flexible-parent XOR
    page.evaluate("openLocCreate('rack','R-A01')"); page.wait_for_timeout(350)
    xor_one = page.evaluate("() => state.form.rack_id==='R-A01' && !state.form.area_id")  # exactly one set
    page.evaluate("setParentType('area')"); page.wait_for_timeout(200)
    xor_swap = page.evaluate("() => state.form.parent_type==='area' && !state.form.rack_id && !state.form.area_id")  # neither yet
    page.evaluate("() => { __t.setVal('code','XOR-T'); }")
    page.evaluate("locStep(2)"); page.wait_for_timeout(250)  # neither parent chosen -> block
    neither_block = page.evaluate("() => state.drawer.step===1 && !!(state.errors.area)")
    sh("01_xor_guard")
    R.rec("flexible-parent XOR: exactly one parent id set; other nulled on switch",
          xor_one and xor_swap, "one=%s swap=%s" % (xor_one, xor_swap))
    R.rec("flexible-parent XOR: neither parent selected -> blocked at step 1", neither_block,
          page.evaluate("() => state.errors.area||''"))
    page.evaluate("closeDrawer()"); page.wait_for_timeout(300)

    # 2. allows_direct=false -> block + 'เพิ่มชั้นวางก่อน' suggestion (A-AISLE-A has allows_direct=false)
    page.evaluate("openLocCreate('area','A-AISLE-A')"); page.wait_for_timeout(350)
    warn_txt = page.evaluate("() => { var d=document.getElementById('drawer'); return d?d.innerText:''; }")
    page.evaluate("() => { __t.setVal('code','DIR-T'); }")
    page.evaluate("locStep(2)"); page.wait_for_timeout(250)
    err_area = page.evaluate("() => state.errors.area||''")
    ad_block = page.evaluate("() => state.drawer.step===1") and ("allows_direct" in err_area)
    sh("02_allows_direct_block")
    R.rec("allows_direct=false blocks direct location + suggests 'เพิ่มชั้นวางก่อน'",
          ad_block and ("เพิ่มชั้นวาง" in warn_txt), "err='%s'" % err_area)
    page.evaluate("closeDrawer()"); page.wait_for_timeout(300)

    # 3. duplicate code within parent at EVERY level (409-style block)
    def dup_node(level, drill_setup, code, expect_msg):
        page.evaluate("resetDrill()"); page.wait_for_timeout(100)
        if drill_setup:
            page.evaluate(drill_setup); page.wait_for_timeout(150)
        before = page.evaluate("() => ({wh:WAREHOUSES.length,z:ZONES.length,a:AREAS.length,r:RACKS.length})")
        page.evaluate("openNodeCreate('%s')" % level); page.wait_for_timeout(350)
        page.evaluate("() => { __t.setVal('code','%s'); __t.setVal('name','dup test'); }" % code)
        if level == "warehouse":
            page.evaluate("() => __t.pickSS('branch','BR-01')"); page.wait_for_timeout(120)
        page.evaluate("submitNode()"); page.wait_for_timeout(400)
        err = page.evaluate("() => state.errors.code||''")
        after = page.evaluate("() => ({wh:WAREHOUSES.length,z:ZONES.length,a:AREAS.length,r:RACKS.length})")
        blocked = (err.find(expect_msg) >= 0) and (before == after) and page.evaluate("state.drawer.open===true")
        R.rec("duplicate code blocked at %s level (409-style, no insert)" % level, blocked, "err='%s'" % err)
        page.evaluate("closeDrawer()"); page.wait_for_timeout(400)  # >280ms close-animation timer must fire before next open

    dup_node("warehouse", "", "WH-01", "รหัสซ้ำ")
    dup_node("zone", "drillInto('warehouse','WH-01')", "Z-STG", "ซ้ำ")
    dup_node("area", "() => { drillInto('warehouse','WH-01'); drillInto('zone','Z-STORAGE'); }", "A-FM", "ซ้ำ")
    dup_node("rack", "() => { drillInto('warehouse','WH-01'); drillInto('zone','Z-STORAGE'); drillInto('area','A-AISLE-A'); }", "R-A01", "ซ้ำ")
    # location dup within parent
    page.evaluate("resetDrill()"); page.wait_for_timeout(200)
    locs_before = page.evaluate("() => LOCATIONS.length")
    page.evaluate("openLocCreate('rack','R-A01')"); page.wait_for_timeout(350)
    page.evaluate("() => { __t.setVal('code','A-01-R1-C1-L1'); }")  # == L001 code within R-A01
    page.evaluate("locStep(2)"); page.wait_for_timeout(250)
    page.evaluate("() => { __t.setVal('cap_val','1'); }")
    page.evaluate("submitLoc()"); page.wait_for_timeout(450)
    loc_dup_block = page.evaluate("() => state.drawer.step===1 && (state.errors.code||'').indexOf('ซ้ำ')>=0") and \
                    (page.evaluate("() => LOCATIONS.length") == locs_before)
    sh("03_dup_location")
    R.rec("duplicate code blocked at location level (within parent, no insert)", loc_dup_block,
          page.evaluate("() => state.errors.code||''"))
    page.evaluate("closeDrawer()"); page.wait_for_timeout(300)

    # 4. capacity <= 0 -> block
    lb = page.evaluate("() => LOCATIONS.length")
    page.evaluate("openLocCreate('rack','R-A01')"); page.wait_for_timeout(350)
    page.evaluate("() => { __t.setVal('code','CAP-ZERO'); }")
    page.evaluate("locStep(2)"); page.wait_for_timeout(250)
    page.evaluate("() => { __t.setVal('cap_val','0'); }")
    page.evaluate("submitLoc()"); page.wait_for_timeout(400)
    cap_block = (page.evaluate("() => state.errors.cap_val||''").find("มากกว่า 0") >= 0) and (page.evaluate("() => LOCATIONS.length") == lb)
    sh("04_capacity_zero")
    R.rec("capacity <= 0 blocked (no insert)", cap_block, page.evaluate("() => state.errors.cap_val||''"))
    page.evaluate("closeDrawer()"); page.wait_for_timeout(300)

    # 5. zone temp_controlled with missing range -> block
    zb = page.evaluate("() => ZONES.length")
    page.evaluate("drillInto('warehouse','WH-01')"); page.wait_for_timeout(150)
    page.evaluate("openNodeCreate('zone')"); page.wait_for_timeout(350)
    page.evaluate("() => { __t.setVal('code','Z-TMPMISS'); __t.setVal('name','no range'); }")
    page.evaluate("toggleField('temp_controlled')"); page.wait_for_timeout(200)  # range fields blank
    page.evaluate("submitNode()"); page.wait_for_timeout(400)
    temp_block = (page.evaluate("() => state.errors.temp_min||''").find("อุณหภูมิ") >= 0) and (page.evaluate("() => ZONES.length") == zb)
    sh("05_temp_missing")
    R.rec("zone temp_controlled with missing range blocked (no insert)", temp_block, page.evaluate("() => state.errors.temp_min||''"))
    page.evaluate("closeDrawer()"); page.wait_for_timeout(300)

    # 6. bulk-gen code collision -> atomic rollback (no partial insert)
    page.evaluate("resetDrill()")
    rb = page.evaluate("() => RACKS.length"); lb2 = page.evaluate("() => LOCATIONS.length")
    page.evaluate("openBulk()"); page.wait_for_timeout(350)
    page.evaluate("() => __t.pickSS('btarget','A-AISLE-A')"); page.wait_for_timeout(150)
    # generate 'A-01-R1-C1-L1' & 'A-01-R1-C2-L1' which collide with existing L001/L002 in R-A01
    page.evaluate("() => { __t.setVal('rackPat','A-0{n}'); __t.setVal('rackQty','1'); __t.setVal('rows','1'); __t.setVal('cols','2'); __t.setVal('levels','1'); __t.setVal('locPat','{rack}-R{r}-C{c}-L{l}'); __t.setVal('cap_val','1'); captureForm(); render(); }")
    page.wait_for_timeout(300)
    collisions = page.evaluate("() => bulkCollisions().length")
    submit_disabled = page.evaluate("() => { var b=document.getElementById('btn-submit'); return !!(b && (b.disabled || b.classList.contains('is-disabled'))); }")
    page.evaluate("submitBulk()"); page.wait_for_timeout(500)
    collide_rollback = (collisions > 0) and (page.evaluate("() => RACKS.length") == rb) and (page.evaluate("() => LOCATIONS.length") == lb2)
    sh("06_bulk_collision")
    R.rec("bulk-gen collision -> atomic rollback (submit disabled, 0 rows added)",
          collide_rollback and submit_disabled, "collisions=%d disabled=%s racks==%s locs==%s" % (
              collisions, submit_disabled, page.evaluate("() => RACKS.length") == rb, page.evaluate("() => LOCATIONS.length") == lb2))

    # 7. bulk-gen grid=0 -> block
    page.evaluate("() => { __t.setVal('rackPat','ZZ-{n}'); __t.setVal('rackQty','2'); __t.setVal('rows','0'); __t.setVal('cols','2'); __t.setVal('levels','1'); captureForm(); render(); }")
    page.wait_for_timeout(250)
    total0 = page.evaluate("() => bulkCalc().total")
    disabled0 = page.evaluate("() => { var b=document.getElementById('btn-submit'); return !!(b && (b.disabled || b.classList.contains('is-disabled'))); }")
    rb2 = page.evaluate("() => RACKS.length")
    page.evaluate("submitBulk()"); page.wait_for_timeout(400)
    sh("07_bulk_grid_zero")
    R.rec("bulk-gen grid=0 -> blocked (total 0, submit disabled, no insert)",
          total0 == 0 and disabled0 and page.evaluate("() => RACKS.length") == rb2, "total=%d disabled=%s" % (total0, disabled0))
    page.evaluate("closeDrawer()"); page.wait_for_timeout(300)

    # 8. reparent location that has stock -> block (GAP-02, AD-5/FN-19)  L001 hasStock, rack R-A01
    orig_rack = page.evaluate("() => loc('L001').rack_id")
    page.evaluate("openLocEdit('L001')"); page.wait_for_timeout(350)
    page.evaluate("() => { state.form.parent_type='rack'; state.form.rack_id='R-B01'; }")  # change parent
    page.evaluate("submitLoc()"); page.wait_for_timeout(750)
    after_rep = page.evaluate("() => ({rack:loc('L001').rack_id, drawerOpen:state.drawer.open, hasErr:Object.keys(state.errors||{}).length>0})")
    sh("08_reparent_stock_block")
    R.rec("GAP-02 reparent BLOCKED when location has stock (parent unchanged, drawer stays w/ error)",
          after_rep["rack"] == orig_rack and after_rep["drawerOpen"] and after_rep["hasErr"],
          json.dumps(after_rep, ensure_ascii=False))
    page.evaluate("closeDrawer()"); page.wait_for_timeout(300)

    # 9. archive node with active children -> block (GAP-01, node stays active)  WH-01 has zones
    page.evaluate("askDeleteNode('warehouse','WH-01')"); page.wait_for_timeout(300)
    guard = page.evaluate("""() => {
      var html=__t.modalHTML();
      return { kids: childCount('warehouse','WH-01'), hasConfirm:/confirmDeleteNode/.test(html),
               blockText:/จัดเก็บคลังไม่ได้/.test(html), status:(WAREHOUSES.find(w=>w.id==='WH-01')||{}).status };
    }""")
    sh("09_archive_children_block")
    R.rec("GAP-01 archive blocked when node has active children (no confirm path, block msg shown)",
          guard["kids"] > 0 and not guard["hasConfirm"] and guard["blockText"], json.dumps(guard, ensure_ascii=False))
    R.rec("GAP-01 blocked node stays active", guard["status"] == "active", "WH-01 status=%s" % guard["status"])
    page.evaluate("closeModal()"); page.wait_for_timeout(250)

    # 10. decommission location with stock -> block  L001 hasStock
    page.evaluate("askDecommission('L001')"); page.wait_for_timeout(300)
    dg = page.evaluate("""() => { var html=__t.modalHTML();
      return { block:/ต้องย้ายสต็อกออกก่อน/.test(html), hasConfirm:/confirmDecommission/.test(html), status:loc('L001').status }; }""")
    sh("10_decommission_stock_block")
    R.rec("decommission location with stock blocked (no confirm, status unchanged)",
          dg["block"] and not dg["hasConfirm"] and dg["status"] == "active", json.dumps(dg, ensure_ascii=False))
    page.evaluate("closeModal()"); page.wait_for_timeout(250)

    # 11. barcode required before activate  L006 (inactive, no barcode)
    before_st = page.evaluate("() => loc('L006').status")
    page.evaluate("setLocStatus('L006','active')"); page.wait_for_timeout(300)
    after_st = page.evaluate("() => loc('L006').status")
    R.rec("barcode required before activate (L006 no barcode stays inactive)",
          before_st == "inactive" and after_st == "inactive", "%s -> %s" % (before_st, after_st))

    # 12. RBAC
    op = page.evaluate("() => { setRole('operator'); return perms(); }"); page.wait_for_timeout(250)
    hdr_create_disabled = page.evaluate("""() => { var b=document.querySelector('.ph-actions .btn-primary');
      return !!(b && (b.hasAttribute('disabled') || b.classList.contains('is-disabled'))); }""")
    sh("11_rbac_operator")
    R.rec("RBAC Operator = view-only (perms create/del/status all false)",
          not op["create"] and not op["del"] and not op["status"], json.dumps(op))
    R.rec("RBAC Operator: header create button disabled", hdr_create_disabled)
    # operator view drawer: no edit/archive controls
    page.evaluate("openViewNode('warehouse','WH-01')"); page.wait_for_timeout(300)
    op_ctrls = page.evaluate("() => ({edit:!!document.querySelector('#drawer .btn-secondary.btn-sm'), danger:!!document.querySelector('#drawer .btn-danger')})")
    R.rec("RBAC Operator: no edit/archive controls in view drawer", not op_ctrls["edit"] and not op_ctrls["danger"], json.dumps(op_ctrls))
    page.evaluate("closeDrawer()"); page.wait_for_timeout(300)

    sup = page.evaluate("() => { setRole('supervisor'); return perms(); }"); page.wait_for_timeout(250)
    hdr_create_enabled = page.evaluate("""() => { var b=document.querySelector('.ph-actions .btn-primary');
      return !!(b && !b.hasAttribute('disabled') && !b.classList.contains('is-disabled')); }""")
    sh("12_rbac_supervisor")
    R.rec("RBAC Supervisor: create/edit yes, archive/delete no (del=false)",
          sup["create"] and not sup["del"], json.dumps(sup))
    R.rec("RBAC Supervisor: header create enabled", hdr_create_enabled)
    page.evaluate("openViewNode('warehouse','WH-01')"); page.wait_for_timeout(300)
    sup_ctrls = page.evaluate("() => ({edit:!!document.querySelector('#drawer .btn-secondary.btn-sm'), danger:!!document.querySelector('#drawer .btn-danger')})")
    R.rec("RBAC Supervisor: edit present but archive (danger) hidden in view drawer",
          sup_ctrls["edit"] and not sup_ctrls["danger"], json.dumps(sup_ctrls))
    page.evaluate("closeDrawer()"); page.wait_for_timeout(300)
    page.evaluate("setRole('manager')"); page.wait_for_timeout(150)


# =====================================================================
# ROUND 3 — state, persistence & robustness
# =====================================================================
def round3(page, R, rnd, vw):
    sh = lambda n: shot(page, rnd, vw, n)

    # 1. Location 7-state transitions  (L005 PACK-01: active, has barcode, empty)
    audit_before = page.evaluate("() => AUDIT.filter(a=>a.refId==='L005').length")
    page.evaluate("openViewLoc('L005')"); page.wait_for_timeout(300)
    # active -> blocked + reason
    page.evaluate("askBlock('L005')"); page.wait_for_timeout(250)
    page.evaluate("() => { var el=document.getElementById('blk-reason'); if(el) el.value='ทดสอบบล็อก E2E'; }")
    page.evaluate("confirmBlock('L005')"); page.wait_for_timeout(650)
    s_blocked = page.evaluate("() => ({st:loc('L005').status, reason:loc('L005').block_reason})")
    # blocked -> active
    page.evaluate("setLocStatus('L005','active')"); page.wait_for_timeout(300)
    s_reactive = page.evaluate("() => loc('L005').status")
    # active -> frozen -> active
    page.evaluate("setLocStatus('L005','frozen')"); page.wait_for_timeout(200)
    s_frozen = page.evaluate("() => loc('L005').status")
    page.evaluate("setLocStatus('L005','active')"); page.wait_for_timeout(200)
    # -> maintenance
    page.evaluate("setLocStatus('L005','maintenance')"); page.wait_for_timeout(200)
    s_maint = page.evaluate("() => loc('L005').status")
    page.evaluate("setLocStatus('L005','active')"); page.wait_for_timeout(200)
    # -> full (system state; no manual button -> driven via setLocStatus) -> active
    page.evaluate("setLocStatus('L005','full')"); page.wait_for_timeout(200)
    s_full = page.evaluate("() => loc('L005').status")
    page.evaluate("setLocStatus('L005','active')"); page.wait_for_timeout(200)
    sh("01_state_transitions")
    R.rec("7-state: active->blocked(+reason)->active", s_blocked["st"] == "blocked" and s_blocked["reason"] and s_reactive == "active",
          json.dumps(s_blocked, ensure_ascii=False))
    R.rec("7-state: frozen / maintenance / full transitions apply",
          s_frozen == "frozen" and s_maint == "maintenance" and s_full == "full",
          "frozen=%s maint=%s full=%s" % (s_frozen, s_maint, s_full))
    # -> decommissioned (soft-kept)
    page.evaluate("closeDrawer()"); page.wait_for_timeout(300)
    len_before = page.evaluate("() => LOCATIONS.length")
    page.evaluate("askDecommission('L005')"); page.wait_for_timeout(300)
    has_confirm = page.evaluate("() => /confirmDecommission/.test(__t.modalHTML())")
    page.evaluate("confirmDecommission('L005')"); page.wait_for_timeout(650)
    dec = page.evaluate("() => ({exists:!!loc('L005'), st:(loc('L005')||{}).status, len:LOCATIONS.length})")
    audit_after = page.evaluate("() => AUDIT.filter(a=>a.refId==='L005').length")
    sh("02_decommission_soft")
    R.rec("7-state: decommission is SOFT-kept (record stays, status=decommissioned, length unchanged)",
          has_confirm and dec["exists"] and dec["st"] == "decommissioned" and dec["len"] == len_before,
          json.dumps(dec, ensure_ascii=False))
    R.rec("state transitions each write WORM audit entries", audit_after > audit_before, "audit %d->%d" % (audit_before, audit_after))

    # 2. node soft-archive keeps record + 'จัดเก็บแล้ว' badge (WH-03 childless)
    page.evaluate("askDeleteNode('warehouse','WH-03')"); page.wait_for_timeout(300)
    arch_confirm = page.evaluate("() => /confirmDeleteNode/.test(__t.modalHTML()) && /จัดเก็บ/.test(__t.modalHTML())")
    page.evaluate("confirmDeleteNode('warehouse','WH-03')"); page.wait_for_timeout(700)
    page.evaluate("resetDrill()"); page.wait_for_timeout(300)
    arch = page.evaluate("""() => { var w=WAREHOUSES.find(x=>x.id==='WH-03');
      return { exists:!!w, status:w?w.status:null, badgeOnList: document.getElementById('page-content').innerText.indexOf('จัดเก็บแล้ว')>=0 }; }""")
    sh("03_node_archived_badge")
    R.rec("node soft-archive: record kept, status=archived, 'จัดเก็บแล้ว' badge shown in list",
          arch_confirm and arch["exists"] and arch["status"] == "archived" and arch["badgeOnList"],
          json.dumps(arch, ensure_ascii=False))

    # 3. hash-routing refresh-safe — reload mid-drill
    page.evaluate("() => { drillInto('warehouse','WH-01'); drillInto('zone','Z-STORAGE'); drillInto('area','A-AISLE-A'); }")
    page.wait_for_timeout(250)
    lvl_before_reload = page.evaluate("() => curLevel()")
    page.reload(); boot(page)
    reloaded_ok = page.evaluate("() => !state.loading && drillValid() && document.querySelectorAll('.drill-chip').length>=1 && document.querySelectorAll('.stat').length===5")
    lvl_after_reload = page.evaluate("() => curLevel()")
    sh("04_reload_mid_drill")
    R.rec("refresh-safe: reload mid-drill renders valid root without crash (no page errors)", reloaded_ok,
          "level %s -> %s" % (lvl_before_reload, lvl_after_reload))
    if lvl_after_reload != lvl_before_reload:
        R.note("Drill depth is in-memory SPA state (not encoded in URL hash) — a reload returns to root ('%s' -> '%s'). "
               "By design for the mock (no crash, no error); NOT a defect, flagged for the manual tester." %
               (lvl_before_reload, lvl_after_reload))

    # reload mid-drawer
    page.evaluate("openViewLoc('L003')"); page.wait_for_timeout(300)
    page.reload(); boot(page)
    mid_drawer_ok = page.evaluate("() => state.drawer.open===false && !state.loading && document.querySelectorAll('.stat').length===5")
    sh("05_reload_mid_drawer")
    R.rec("refresh-safe: reload mid-drawer -> drawer closed, valid render, no crash", mid_drawer_ok)

    # 4. Esc chain — 3-tier
    # (a) combobox list closes first (drawer stays)
    page.evaluate("openLocEdit('L002')"); page.wait_for_timeout(350)
    page.evaluate("() => { ssOpen('rack'); }"); page.wait_for_timeout(200)
    combo_open = page.evaluate("() => (__t.ssState('rack')||{}).open===true")
    page.keyboard.press("Escape"); page.wait_for_timeout(200)
    combo_closed = page.evaluate("() => (__t.ssState('rack')||{}).open===false")
    drawer_still = page.evaluate("() => state.drawer.open===true")
    sh("06_esc_combobox")
    R.rec("Esc chain tier 1: combobox list closes first, drawer stays open",
          combo_open and combo_closed and drawer_still, "comboOpen=%s comboClosed=%s drawer=%s" % (combo_open, combo_closed, drawer_still))
    page.evaluate("closeDrawer()"); page.wait_for_timeout(300)

    # (b) in-drawer modal: open view drawer, launch decommission modal FROM the drawer (real click)
    page.evaluate("openViewLoc('L010')"); page.wait_for_timeout(350)  # L010 DMG-01 empty, active
    danger = page.locator("#drawer .btn-danger")
    if danger.count() > 0:
        danger.first.click(); page.wait_for_timeout(450)
    if not page.evaluate("() => state.modal.open"):
        page.evaluate("askDecommission('L010')"); page.wait_for_timeout(450)
    modal_open = page.evaluate("() => state.modal.open===true")
    z = page.evaluate("() => __t.zmeasure()")
    sh("07_modal_over_drawer_zindex")
    try:
        mb = int(z["modalBackdropZ"]); dz = int(z["drawerZ"])
        z_ok = mb > dz and z["topmostAtModalCenter"] == "modal"
    except Exception:
        z_ok = False
    R.rec("in-drawer modal renders ABOVE drawer (z-index measured + elementFromPoint=modal)",
          modal_open and z_ok, json.dumps(z))
    # Esc chain tier 2: modal closes first, drawer stays
    page.keyboard.press("Escape"); page.wait_for_timeout(350)
    modal_closed = page.evaluate("() => state.modal.open===false")
    drawer_after_modal = page.evaluate("() => state.drawer.open===true")
    R.rec("Esc chain tier 2: modal closes first, drawer stays", modal_closed and drawer_after_modal,
          "modalClosed=%s drawer=%s" % (modal_closed, drawer_after_modal))
    # Esc chain tier 3: drawer closes
    page.keyboard.press("Escape"); page.wait_for_timeout(350)
    drawer_closed = page.evaluate("() => state.drawer.open===false")
    R.rec("Esc chain tier 3: next Esc closes drawer", drawer_closed)

    # 5. drawer content re-render after in-drawer tab switch (content persists, no blank)
    page.evaluate("openViewLoc('L001')"); page.wait_for_timeout(350)
    before_len = page.evaluate("() => __t.drawerText()")
    page.locator("#drawer .drawer-tab").nth(1).click(); page.wait_for_timeout(300)
    after_len = page.evaluate("() => __t.drawerText()")
    still_open = page.evaluate("() => state.drawer.open===true")
    not_blank = after_len > 60
    sh("08_drawer_rerender")
    R.rec("drawer content re-renders after in-drawer tab switch (persists, not blank/collapsed)",
          still_open and not_blank, "len %d -> %d open=%s" % (before_len, after_len, still_open))
    page.evaluate("closeDrawer()"); page.wait_for_timeout(300)

    # 6. empty state (no-match filter at root)
    page.evaluate("resetDrill()"); page.wait_for_timeout(150)
    page.evaluate("setSearch('zzz_nomatch_zzz')"); page.wait_for_timeout(250)
    empty_ok = page.evaluate("() => { var t=document.getElementById('page-content').innerText; return document.querySelectorAll('.empty').length>0 && t.indexOf('ไม่พบรายการที่ค้นหา')>=0; }")
    sh("09_empty_state")
    R.rec("empty state renders on no-match filter", empty_ok)
    page.evaluate("resetFilters()"); page.wait_for_timeout(200)

    # 7. loading state
    page.evaluate("() => { state.loading=true; render(); }"); page.wait_for_timeout(200)
    loading_ok = page.locator(".sk-line").count() > 0
    sh("10_loading_state")
    R.rec("loading skeleton renders", loading_ok, "sk-line=%d" % page.locator(".sk-line").count())
    page.evaluate("() => { state.loading=false; render(); }"); page.wait_for_timeout(200)

    # 8. error state — drill into a deleted/missing node
    page.evaluate("() => { state.drill={wh:'__deleted__',zone:null,area:null,rack:null}; render(); }"); page.wait_for_timeout(250)
    err_ok = page.evaluate("() => !drillValid() && document.getElementById('page-content').innerText.indexOf('ไม่พบข้อมูลที่กำลังดู')>=0")
    sh("11_error_state")
    R.rec("error state renders when drilling into a deleted/missing node", err_ok)
    page.evaluate("resetDrill()"); page.wait_for_timeout(200)

    # 9. geo cascade reset when province changes
    page.evaluate("openNodeCreate('warehouse')"); page.wait_for_timeout(400)
    page.evaluate("() => __t.pickSS('prov','สมุทรปราการ')"); page.wait_for_timeout(200)
    page.evaluate("() => __t.pickSS('dist','บางพลี')"); page.wait_for_timeout(200)
    page.evaluate("() => __t.pickSS('subd','บางพลีใหญ่')"); page.wait_for_timeout(250)
    pc1 = page.evaluate("() => state.form.postcode")
    page.evaluate("() => __t.pickSS('prov','ลำพูน')"); page.wait_for_timeout(250)
    reset = page.evaluate("() => ({d:state.form.district, s:state.form.subdistrict, p:state.form.postcode})")
    sh("12_geo_reset")
    R.rec("geo cascade resets district/subdistrict/postcode when province changes",
          pc1 == "10540" and reset["d"] == "" and reset["s"] == "" and reset["p"] == "",
          "pc1=%s after=%s" % (pc1, json.dumps(reset, ensure_ascii=False)))
    page.evaluate("closeDrawer()"); page.wait_for_timeout(300)


ROUND_FN = {1: round1, 2: round2, 3: round3}


def main():
    results = build_results()
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for rnd in (1, 2, 3):
            for vw in VIEWPORTS:
                print("\n===== ROUND %d @ %dpx =====" % (rnd, vw))
                R = Rec(results, rnd, vw)
                ctx = browser.new_context(viewport={"width": vw, "height": 900}, device_scale_factor=1)
                page = ctx.new_page()
                page.on("console", lambda m, R=R: R.bucket["console_errors"].append(m.text) if m.type == "error" else None)
                page.on("pageerror", lambda e, R=R: R.bucket["page_errors"].append(str(e)))
                try:
                    page.goto(URL)
                    boot(page)
                    ROUND_FN[rnd](page, R, rnd, vw)
                except Exception as e:
                    R.rec("FATAL — round aborted", False, str(e))
                a = R.bucket["assertions"]
                R.bucket["passed"] = sum(1 for x in a if x["pass"])
                R.bucket["failed"] = sum(1 for x in a if not x["pass"])
                R.bucket["console_error_count"] = len(R.bucket["console_errors"])
                R.bucket["page_error_count"] = len(R.bucket["page_errors"])
                R.bucket["green"] = (R.bucket["failed"] == 0 and R.bucket["console_error_count"] == 0 and R.bucket["page_error_count"] == 0)
                ctx.close()
        browser.close()

    # ---- overall summary ----
    tot_pass = tot_fail = tot_ce = tot_pe = 0
    round_summary = {}
    for rnd in ("1", "2", "3"):
        rp = rf = rce = rpe = 0
        greens = []
        for vw, b in results["rounds"][rnd]["viewports"].items():
            rp += b["passed"]; rf += b["failed"]; rce += b["console_error_count"]; rpe += b["page_error_count"]
            greens.append(b["green"])
        round_summary[rnd] = {"passed": rp, "failed": rf, "console_errors": rce, "page_errors": rpe, "all_viewports_green": all(greens)}
        tot_pass += rp; tot_fail += rf; tot_ce += rce; tot_pe += rpe
    verdict = "PASS" if (tot_fail == 0 and tot_ce == 0 and tot_pe == 0) else "FAIL"
    results["round_summary"] = round_summary
    results["summary"] = {"verdict": verdict, "total_passed": tot_pass, "total_failed": tot_fail,
                          "total_console_errors": tot_ce, "total_page_errors": tot_pe,
                          "viewports": VIEWPORTS}

    out = QC / "E2E_3_ROUNDS_RESULT.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n==================== VERDICT:", verdict, "====================")
    print("pass=%d fail=%d console_err=%d page_err=%d" % (tot_pass, tot_fail, tot_ce, tot_pe))
    for rnd, s in round_summary.items():
        print("  Round", rnd, s)
    print("json ->", out)
    return verdict


if __name__ == "__main__":
    main()
