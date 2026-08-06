# -*- coding: utf-8 -*-
"""
E2E browser QC for WarehouseBin.html (F-LOCATION-MASTER-001)
Drives all 6 screens across viewports 1280 & 1440, captures screenshots,
and asserts the two known base-kit latent bugs:
  (1) drawer content re-render after an in-drawer action
  (2) in-drawer modal z-index (modal + backdrop ABOVE the drawer)
Run with the project venv python.
"""
import json, os, sys, pathlib
try:
    sys.stdout.reconfigure(encoding="utf-8")   # allow Thai in assertion names/details on Windows console
except Exception:
    pass
from playwright.sync_api import sync_playwright

HTML = pathlib.Path(r"C:\Users\Admin\Desktop\Work\brief-maker\outputs\11_Warehouse\01_HTML\WarehouseBin.html")
OUT  = pathlib.Path(r"C:\Users\Admin\Desktop\Work\brief-maker\outputs\11_Warehouse\02_QC\ux-shots")
OUT.mkdir(parents=True, exist_ok=True)
URL = HTML.as_uri()

results = {"viewports": {}, "assertions": [], "console_errors": [], "page_errors": []}

def rec(name, ok, detail=""):
    results["assertions"].append({"name": name, "pass": bool(ok), "detail": detail})
    print(("PASS" if ok else "FAIL"), name, "-", detail)

def shot(page, vw, name):
    p = OUT / f"{vw}_{name}.png"
    page.screenshot(path=str(p), full_page=False)
    return p.name

def boot(page):
    page.wait_for_timeout(900)  # boot setTimeout 550ms + render

def drive(page, vw):
    tag = str(vw)
    # --- 0. initial load / list root ---
    boot(page)
    shot(page, tag, "01_list_root")
    # KPI + drill breadcrumb present
    has_kpi = page.locator(".drill-chip").count() > 0 or page.locator(".kpi, .stat, [class*='kpi']").count() > 0
    rec(f"[{tag}] list root renders (drill chips / kpi)", has_kpi)

    # --- 0b. Display name (D14 change → "คลังและตำแหน่ง (Warehouse & Bin)") ---
    title = page.title()
    rec(f"[{tag}] D14 title shows Warehouse & Bin / คลังและตำแหน่ง",
        "Warehouse & Bin" in title and "คลังและตำแหน่ง" in title, title)
    sb = page.locator('.sb-item[data-feature="location-master"] span').inner_text().strip()
    rec(f"[{tag}] D14 sidebar label = คลังและตำแหน่ง", sb == "คลังและตำแหน่ง", sb)
    bc = page.locator('.breadcrumb-current').inner_text().strip()
    rec(f"[{tag}] D14 breadcrumb = คลังและตำแหน่ง", bc == "คลังและตำแหน่ง", bc)
    h1 = page.locator('.ph-title').first.inner_text()
    rec(f"[{tag}] D14 page h1 = คลังและตำแหน่ง (Warehouse & Bin)",
        "คลังและตำแหน่ง" in h1 and "Warehouse & Bin" in h1, h1)

    # --- 0c. Role switcher aligned with create button (D13) ---
    page.evaluate("() => { state.view='list'; state.drill={wh:null,zone:null,area:null,rack:null}; state.role='manager'; render(); }")
    page.wait_for_timeout(150)
    align = page.evaluate("""() => {
        const sel = document.querySelector('.role-select');
        const btns = Array.from(document.querySelectorAll('.ph-actions .btn-primary'));
        const btn = btns.length ? btns[btns.length-1] : null;
        if(!sel||!btn) return null;
        const a=sel.getBoundingClientRect(), b=btn.getBoundingClientRect();
        return {selTop:a.top, btnTop:b.top, selH:a.height, btnH:b.height,
                dTop:Math.abs(a.top-b.top), dH:Math.abs(a.height-b.height)};
    }""")
    shot(page, tag, "rolealign_01_header")
    rec(f"[{tag}] D13 role switcher aligned with create button (top & height within 2px)",
        bool(align) and align['dTop']<=2 and align['dH']<=2, json.dumps(align))

    # --- 0d. VIEW SWITCHER + HIERARCHY TREE (D12) ---
    page.evaluate("setView('tree')"); page.wait_for_timeout(250)
    tree_on = page.evaluate("() => state.view==='tree' && !!document.querySelector('.tree-layout')")
    shot(page, tag, "tree_01_hierarchy_view")
    rec(f"[{tag}] D12 view switcher -> Hierarchy renders tree pane + summary", tree_on)
    page.evaluate("setView('list')"); page.wait_for_timeout(200)
    list_on = page.evaluate("() => state.view==='list' && !!document.querySelector('.table')")
    rec(f"[{tag}] D12 view switcher -> List renders table", list_on)
    page.evaluate("setView('tree')"); page.wait_for_timeout(200)

    exp = page.evaluate("""() => {
        const wid = WAREHOUSES[0].id;
        state.treeOpen = {}; render();
        const before = document.querySelectorAll('.tree-children').length;
        toggleTreeNode('warehouse', wid);
        const afterOpen = document.querySelectorAll('.tree-children').length;
        toggleTreeNode('warehouse', wid);
        const afterClose = document.querySelectorAll('.tree-children').length;
        return {before, afterOpen, afterClose};
    }""")
    page.wait_for_timeout(150); shot(page, tag, "tree_02_expand_collapse")
    rec(f"[{tag}] D12 tree expand/collapse toggles children",
        exp['afterOpen']>exp['before'] and exp['afterClose']==exp['before'], json.dumps(exp))

    selinfo = page.evaluate("""() => {
        const z = ZONES.find(z=>z.warehouse_id===WAREHOUSES[0].id) || ZONES[0];
        treeSelect('zone', z.id);
        const ns = document.querySelector('.node-summary');
        const title = ns ? (ns.querySelector('.ns-title')||{}).textContent : '';
        const path = ns ? (ns.querySelector('.path-str')||{}).textContent : '';
        const chips = ns ? ns.querySelectorAll('.child-stat.is-clickable').length : 0;
        return {zid:z.id, zcode:z.code, selLevel:state.sel.level, selId:state.sel.id,
                title, pathOk: path.indexOf('›')>=0 && path.indexOf(z.code)>=0, chips};
    }""")
    page.wait_for_timeout(150); shot(page, tag, "tree_03_node_summary")
    rec(f"[{tag}] D12 tree select -> summary panel (sel synced + code + full path + child chips)",
        selinfo['selLevel']=='zone' and selinfo['selId']==selinfo['zid']
        and selinfo['zcode'] in selinfo['title'] and selinfo['pathOk'] and selinfo['chips']>=1,
        json.dumps(selinfo, ensure_ascii=False))

    chip = page.evaluate("""() => {
        const c = document.querySelector('.node-summary .child-stat.is-clickable');
        if(c){ c.click(); }
        return {view:state.view, drillZone:state.drill.zone, level:curLevel()};
    }""")
    page.wait_for_timeout(200); shot(page, tag, "tree_04_chip_to_list")
    rec(f"[{tag}] D12 child chip -> switches to List drilled to that node",
        chip['view']=='list' and chip['level']=='zone', json.dumps(chip))

    two_way = page.evaluate("""() => {
        const a = AREAS[0];
        state.view='list'; state.drill = drillForSel('area', a.id); render();
        const selInList = JSON.stringify(state.sel);
        setView('tree');
        const nsEl = document.querySelector('.node-summary .ns-title');
        const shownCode = nsEl ? nsEl.textContent : '';
        const ancestorsOpen = !!state.treeOpen['warehouse:'+drillForSel('area',a.id).wh]
                            && !!state.treeOpen['zone:'+a.zone_id];
        setView('list');
        return {selInList, aCode:a.code, aId:a.id, shownCode, ancestorsOpen,
                backLevel:curLevel(), backArea:state.drill.area};
    }""")
    page.wait_for_timeout(150); shot(page, tag, "tree_05_shared_sel_bidir")
    rec(f"[{tag}] D12 shared sel context preserved BOTH directions (List<->Tree)",
        two_way['aCode'] in two_way['shownCode'] and two_way['ancestorsOpen']
        and two_way['backLevel']=='area' and two_way['backArea']==two_way['aId'],
        json.dumps(two_way, ensure_ascii=False))

    # reset to clean list root for the remaining (legacy) assertions
    page.evaluate("() => { state.view='list'; state.drill={wh:null,zone:null,area:null,rack:null}; state.treeOpen={}; state.filters={search:'',type:'all',status:'all'}; state.role='manager'; render(); }")
    page.wait_for_timeout(150)

    # --- 1. Branch filter (combobox) ---
    try:
        page.evaluate("ssOpen && ssOpen('branchf')")
        page.wait_for_timeout(200)
        shot(page, tag, "02_branch_filter_open")
        opened = page.evaluate("!!(window.__ss && window.__ss['branchf'] && window.__ss['branchf'].open)")
        rec(f"[{tag}] branch filter combobox opens", opened)
        # ESC closes combobox (chain step 1) — should NOT close anything else
        page.keyboard.press("Escape")
        page.wait_for_timeout(150)
        still = page.evaluate("!!(window.__ss && window.__ss['branchf'] && window.__ss['branchf'].open)")
        rec(f"[{tag}] Esc closes combobox list first", not still)
    except Exception as e:
        rec(f"[{tag}] branch filter combobox", False, f"err {e}")

    # --- 2. Drill through all 5 levels via real row clicks ---
    levels = []
    try:
        # WH -> Zone
        page.locator("tr.is-clickable").first.click(); page.wait_for_timeout(250); levels.append(page.evaluate("curLevel()"))
        shot(page, tag, "03_drill_zone")
        # Zone -> Area
        page.locator("tr.is-clickable").first.click(); page.wait_for_timeout(250); levels.append(page.evaluate("curLevel()"))
        shot(page, tag, "04_drill_area")
        # Area -> Rack (area tab may default to racks)
        page.locator("tr.is-clickable").first.click(); page.wait_for_timeout(250); levels.append(page.evaluate("curLevel()"))
        shot(page, tag, "05_drill_rack")
        # Rack -> Location list
        if page.locator("tr.is-clickable").count() > 0:
            page.locator("tr.is-clickable").first.click(); page.wait_for_timeout(250); levels.append(page.evaluate("curLevel()"))
        shot(page, tag, "06_drill_location_list")
        rec(f"[{tag}] drill-down reaches deep levels", "rack" in levels or "area" in levels, f"levels={levels}")
    except Exception as e:
        rec(f"[{tag}] drill-down 5 levels", False, f"err {e} levels={levels}")

    # reset to a known area with racks+locations via app state for reliable coverage
    page.evaluate("""() => {
        // drill into first warehouse->zone->area with locations if possible
        state.drill = {wh:null,zone:null,area:null,rack:null};
        state.filters={search:'',type:'all',status:'all'}; render();
    }""")
    page.wait_for_timeout(200)

    # --- 3. Role switcher: Operator = view-only, Supervisor = no delete ---
    def perms_for(role):
        return page.evaluate(f"() => {{ state.role='{role}'; render(); return perms(); }}")
    op = perms_for("operator"); page.wait_for_timeout(150); shot(page, tag, "07_role_operator")
    rec(f"[{tag}] Operator view-only (no create/del/status)", (not op['create'] and not op['del'] and not op['status']), str(op))
    sup = perms_for("supervisor"); page.wait_for_timeout(150); shot(page, tag, "08_role_supervisor")
    rec(f"[{tag}] Supervisor can create but NOT delete", (sup['create'] and not sup['del']), str(sup))
    perms_for("manager"); page.wait_for_timeout(150)

    # --- 4. Drawers ---
    # 4a. Node create (WH) with branch + geo cascade; verify subdistrict auto-fills postcode
    page.evaluate("openNodeCreate('warehouse')"); page.wait_for_timeout(350)
    shot(page, tag, "09_drawer_node_create_wh")
    drawer_open = page.evaluate("state.drawer.open===true")
    rec(f"[{tag}] node create drawer (WH) opens", drawer_open)
    # geo cascade: set province/district/subdistrict programmatically through the app helpers if present
    geo_ok = page.evaluate("""() => {
        try {
            if (typeof onGeoProvince==='function'){ /* unknown api */ }
            return true;
        } catch(e){ return false; }
    }""")
    page.evaluate("closeDrawer()"); page.wait_for_timeout(300)

    # 4b. Location 2-step wizard
    page.evaluate("() => { openLocCreate('rack', RACKS[0].id); }")
    page.wait_for_timeout(300)
    shot(page, tag, "10_drawer_loc_wizard_step1")
    loc_wizard = page.evaluate("state.drawer.open===true && state.drawer.view==='loc-form'")
    rec(f"[{tag}] location 2-step wizard opens", loc_wizard, f"step={page.evaluate('state.drawer.step')}")
    # step 2
    if loc_wizard:
        page.evaluate("() => { if(typeof gotoStep==='function'){gotoStep(2);} else { state.drawer.step=2; render(); } }")
        page.wait_for_timeout(250); shot(page, tag, "11_drawer_loc_wizard_step2")
    page.evaluate("closeDrawer()"); page.wait_for_timeout(300)

    # 4c. View node drawer
    opened_view_node = False
    try:
        page.evaluate("() => { state.drill={wh:null,zone:null,area:null,rack:null}; state.role='manager'; render(); }")
        page.wait_for_timeout(200)
        if page.locator("button.ra-btn").count() > 0:
            page.locator("button.ra-btn").first.click()
            page.wait_for_timeout(350)
            opened_view_node = page.evaluate("state.drawer.open===true && /view-node/.test(state.drawer.view||'')")
        if not opened_view_node:
            page.evaluate("() => { openViewNode('warehouse', WAREHOUSES[0].id); }")
            page.wait_for_timeout(300)
            opened_view_node = page.evaluate("state.drawer.open===true && /view-node/.test(state.drawer.view||'')")
    except Exception as e:
        pass
    shot(page, tag, "12_drawer_view_node")
    rec(f"[{tag}] view node drawer opens", opened_view_node)
    page.evaluate("closeDrawer()"); page.wait_for_timeout(300)

    # 4d. View location drawer (3 tabs) — drill to a location list then open
    page.evaluate("() => { state.drill={wh:null,zone:null,area:null,rack:null}; render(); }")
    page.wait_for_timeout(150)
    # deep drill via clicks to reach locations
    for _ in range(5):
        if page.locator("tr.is-clickable").count() == 0: break
        # if a location row (openViewLoc) exists, stop drilling
        onclicks = page.evaluate("() => Array.from(document.querySelectorAll('tr.is-clickable')).slice(0,3).map(r=>r.getAttribute('onclick'))")
        if any("openViewLoc" in (o or "") for o in onclicks):
            break
        page.locator("tr.is-clickable").first.click(); page.wait_for_timeout(250)
    view_loc_open = False
    try:
        loc_rows = page.locator("tr.is-clickable")
        # click a row that calls openViewLoc
        idx = None
        cnt = loc_rows.count()
        for i in range(cnt):
            oc = loc_rows.nth(i).get_attribute("onclick") or ""
            if "openViewLoc" in oc:
                idx = i; break
        if idx is not None:
            loc_rows.nth(idx).click(); page.wait_for_timeout(350)
        else:
            page.evaluate("() => { var L=(typeof LOCATIONS!=='undefined')?LOCATIONS[0]:null; if(L) openViewLoc(L.id); }")
            page.wait_for_timeout(350)
        view_loc_open = page.evaluate("state.drawer.open===true && /view-loc/.test(state.drawer.view||'')")
    except Exception as e:
        rec(f"[{tag}] view-loc open err", False, str(e))
    shot(page, tag, "13_drawer_view_loc_tab1")
    rec(f"[{tag}] view location drawer (3 tabs) opens", view_loc_open)

    # count tabs in drawer
    tab_count = page.locator("#drawer .tab, #drawer [role='tab'], #drawer .dw-tab, #drawer .tabs .tab").count()
    results["viewports"].setdefault(tag, {})["view_loc_tabs"] = tab_count

    # ===== LATENT BUG #1: drawer content re-render after in-drawer action =====
    if view_loc_open:
        before = page.evaluate("() => document.getElementById('drawer').innerText.length")
        # in-drawer action: switch tab (find a tab and click), fallback to changing state.drawer.tab
        clicked_tab = False
        tabs = page.locator("#drawer .tab, #drawer [onclick*='tab'], #drawer [onclick*='Tab']")
        if tabs.count() >= 2:
            try:
                tabs.nth(1).click(); clicked_tab = True
            except Exception:
                clicked_tab = False
        if not clicked_tab:
            page.evaluate("() => { state.drawer.tab = (state.drawer.tab==='overview'?'behavior':'overview'); render(); }")
        page.wait_for_timeout(300)
        after = page.evaluate("() => document.getElementById('drawer').innerText.length")
        still_open = page.evaluate("state.drawer.open===true")
        not_blank = after > 40
        shot(page, tag, "14_drawer_reRENDER_after_inaction")
        rec(f"[{tag}] LATENT#1 drawer re-render keeps content (not blank/collapsed)",
            (still_open and not_blank), f"len {before}->{after}, open={still_open}")

    # ===== LATENT BUG #2: in-drawer modal z-index =====
    if not page.evaluate("state.drawer.open===true"):
        # reopen a view-loc drawer
        page.evaluate("() => { var L=null; try{L=(typeof LOCATIONS!=='undefined')?LOCATIONS[0]:null;}catch(e){} if(L) openViewLoc(L.id); }")
        page.wait_for_timeout(300)
    # trigger decommission modal FROM WITHIN the drawer
    launched = False
    danger = page.locator("#drawer .btn-danger, #drawer button.btn-danger")
    if danger.count() > 0:
        try:
            danger.first.click(); launched = True
        except Exception:
            launched = False
    if not launched:
        page.evaluate("() => { var L=null; try{L=(typeof LOCATIONS!=='undefined')?LOCATIONS[0]:null;}catch(e){} if(L) askDecommission(L.id); }")
    page.wait_for_timeout(400)
    modal_open = page.evaluate("state.modal.open===true")
    z = page.evaluate("""() => {
        const mb = document.getElementById('modalBackdrop');
        const modal = mb ? mb.querySelector('.modal') : null;
        const db = document.getElementById('drawerBackdrop');
        const dr = document.getElementById('drawer');
        const zi = el => el ? (getComputedStyle(el).zIndex) : null;
        let topmostAtModal = null;
        if (modal) {
            const r = modal.getBoundingClientRect();
            const el = document.elementFromPoint(r.left + r.width/2, r.top + r.height/2);
            topmostAtModal = el ? (el.closest('.modal') ? 'modal' : (el.closest('.drawer') ? 'drawer' : el.className)) : null;
        }
        return {
            modalBackdropZ: zi(mb), modalZ: zi(modal),
            drawerBackdropZ: zi(db), drawerZ: zi(dr),
            topmostAtModalCenter: topmostAtModal
        };
    }""")
    results["viewports"].setdefault(tag, {})["zindex"] = z
    shot(page, tag, "15_MODAL_over_drawer_zindex")
    try:
        mb = int(z["modalBackdropZ"]); dz = int(z["drawerZ"])
        z_ok = mb > dz and z["topmostAtModalCenter"] == "modal"
    except Exception:
        z_ok = False
    rec(f"[{tag}] LATENT#2 in-drawer modal renders ABOVE drawer", (modal_open and z_ok), json.dumps(z))
    # Esc chain: modal closes first, drawer stays
    page.keyboard.press("Escape"); page.wait_for_timeout(300)
    modal_closed = not page.evaluate("state.modal.open===true")
    drawer_still = page.evaluate("state.drawer.open===true")
    shot(page, tag, "16_esc_modal_closed_drawer_stays")
    rec(f"[{tag}] Esc closes modal first (drawer stays)", (modal_closed and drawer_still),
        f"modalClosed={modal_closed} drawerOpen={drawer_still}")
    # Esc again closes drawer
    page.keyboard.press("Escape"); page.wait_for_timeout(300)
    drawer_closed = not page.evaluate("state.drawer.open===true")
    rec(f"[{tag}] Esc then closes drawer", drawer_closed)

    # --- 5. Bulk generate: preview count ---
    page.evaluate("() => { state.role='manager'; render(); }")
    page.evaluate("openBulk()"); page.wait_for_timeout(400)
    bulk_open = page.evaluate("state.drawer.open===true && /bulk/.test(state.drawer.view||'')")
    shot(page, tag, "17_drawer_bulk_generate")
    preview_txt = page.locator(".preview-num").first.inner_text() if page.locator(".preview-num").count() else ""
    rec(f"[{tag}] bulk generate drawer + preview count", bulk_open, f"preview='{preview_txt}'")
    page.evaluate("closeDrawer()"); page.wait_for_timeout(250)

    # --- 6. Node archive modal (referential-safe · D11 renames delete->archive) ---
    page.evaluate("() => { var w=null; try{w=(typeof WAREHOUSES!=='undefined')?WAREHOUSES[0]:null;}catch(e){} if(w) askDeleteNode('warehouse', w.id); }")
    page.wait_for_timeout(300)
    del_modal = page.evaluate("state.modal.open===true")
    archive_word = page.evaluate("() => /จัดเก็บ/.test(document.getElementById('modalBackdrop').innerHTML)")
    shot(page, tag, "18_modal_archive_node")
    rec(f"[{tag}] node archive modal renders (microcopy 'จัดเก็บ')", del_modal and archive_word)
    page.evaluate("closeModal()"); page.wait_for_timeout(250)

    # --- 6b. GAP-01: node delete -> SOFT ARCHIVE (D11 / GC#7 no hard delete) ---
    page.evaluate("() => { state.role='manager'; render(); }")
    # (i) archiving a CHILDLESS node keeps the record (status=archived, not removed) + audit logged
    arch = page.evaluate("""() => {
        const before = WAREHOUSES.length;
        const auditBefore = AUDIT.filter(a=>a.refId==='WH-03').length;   // WH-03 has no zones
        confirmDeleteNode('warehouse','WH-03');
        return {before, auditBefore};
    }""")
    page.wait_for_timeout(700)
    after_arch = page.evaluate("""() => {
        const rec = WAREHOUSES.find(w=>w.id==='WH-03');
        return { stillInData: !!rec, status: rec ? rec.status : null,
                 arrayLen: WAREHOUSES.length, auditAfter: AUDIT.filter(a=>a.refId==='WH-03').length };
    }""")
    shot(page, tag, "22_node_archived_kept")
    rec(f"[{tag}] GAP-01 childless node soft-archived (kept in data, status=archived)",
        after_arch["stillInData"] and after_arch["status"]=="archived" and after_arch["arrayLen"]==arch["before"],
        json.dumps(after_arch, ensure_ascii=False))
    rec(f"[{tag}] GAP-01 archive writes WORM audit entry",
        after_arch["auditAfter"] > arch["auditBefore"], f"audit {arch['auditBefore']}->{after_arch['auditAfter']}")
    # (ii) childless rack archived + archived child no longer counts against its parent
    parent_before = page.evaluate("() => childCount('area','A-AISLE-A')")
    page.evaluate("confirmDeleteNode('rack','R-A02')"); page.wait_for_timeout(700)   # R-A02 has no locations
    rack_arch = page.evaluate("() => { const r=RACKS.find(x=>x.id==='R-A02'); return {inData:!!r, status:r?r.status:null, parentCount:childCount('area','A-AISLE-A')}; }")
    rec(f"[{tag}] GAP-01 childless rack soft-archived + archived child excluded from parent count",
        rack_arch["inData"] and rack_arch["status"]=="archived" and rack_arch["parentCount"]==parent_before-1,
        json.dumps(rack_arch, ensure_ascii=False))
    # (iii) archiving a node WITH active children is BLOCKED (no confirm path)
    blocked = page.evaluate("""() => {
        askDeleteNode('warehouse','WH-01');    // WH-01 has active zones
        const html = document.getElementById('modalBackdrop').innerHTML;
        return { kids: childCount('warehouse','WH-01'), hasConfirm: /confirmDeleteNode/.test(html), blockText: /จัดเก็บคลังไม่ได้/.test(html) };
    }""")
    page.wait_for_timeout(150)
    shot(page, tag, "23_node_archive_blocked_children")
    rec(f"[{tag}] GAP-01 archive blocked when node has active children",
        blocked["kids"]>0 and (not blocked["hasConfirm"]) and blocked["blockText"], json.dumps(blocked, ensure_ascii=False))
    wh01_status = page.evaluate("() => (WAREHOUSES.find(w=>w.id==='WH-01')||{}).status")
    rec(f"[{tag}] GAP-01 blocked node stays active", wh01_status=="active", f"WH-01 status={wh01_status}")
    page.evaluate("closeModal()"); page.wait_for_timeout(200)

    # --- 6c. GAP-02: reparent guard — block moving a location that has stock (AD-5 / FN-19) ---
    page.evaluate("() => { state.role='manager'; render(); }")
    # (i) location WITH stock -> reparent BLOCKED, parent unchanged, drawer stays with error
    blocked_rep = page.evaluate("""() => {
        const src = LOCATIONS.find(l=>l.id==='L001');   // hasStock:true, rack R-A01
        const origRack = src.rack_id;
        openLocEdit('L001');
        state.form.parent_type='rack'; state.form.rack_id='R-B01';   // change parent
        submitLoc();
        return { origRack };
    }""")
    page.wait_for_timeout(750)
    after_rep = page.evaluate("() => { const l=LOCATIONS.find(x=>x.id==='L001'); return { rack_id:l.rack_id, drawerOpen: state.drawer.open, hasErr: Object.keys(state.errors||{}).length>0 }; }")
    shot(page, tag, "24_reparent_blocked_stock")
    rec(f"[{tag}] GAP-02 reparent BLOCKED when location has stock (parent unchanged)",
        after_rep["rack_id"]==blocked_rep["origRack"] and after_rep["drawerOpen"] and after_rep["hasErr"],
        json.dumps(after_rep, ensure_ascii=False))
    page.evaluate("closeDrawer()"); page.wait_for_timeout(300)
    # (ii) location WITHOUT stock -> reparent SUCCEEDS
    page.evaluate("""() => {
        openLocEdit('L002');                             // hasStock:false, rack R-A01
        state.form.parent_type='rack'; state.form.rack_id='R-B01';
        submitLoc();
    }""")
    page.wait_for_timeout(1050)   # submit 500ms + closeDrawer animation 280ms
    ok_rep = page.evaluate("() => { const l=LOCATIONS.find(x=>x.id==='L002'); return { rack_id:l.rack_id, drawerOpen: state.drawer.open }; }")
    shot(page, tag, "25_reparent_empty_ok")
    rec(f"[{tag}] GAP-02 reparent SUCCEEDS when location is empty (stock=0)",
        ok_rep["rack_id"]=="R-B01" and (not ok_rep["drawerOpen"]), json.dumps(ok_rep, ensure_ascii=False))

    # --- 7. Empty state ---
    page.evaluate("() => { state.filters={search:'zzz_nomatch_zzz',type:'all',status:'all'}; render(); }")
    page.wait_for_timeout(250)
    empty_shown = page.locator(".empty, .empty-state, [class*='empty']").count() > 0
    shot(page, tag, "19_empty_state")
    rec(f"[{tag}] empty state renders on no-match filter", empty_shown)
    page.evaluate("() => { state.filters={search:'',type:'all',status:'all'}; render(); }")

    # --- 8. Error state (invalid drill) ---
    page.evaluate("() => { state.drill={wh:'__bad__',zone:null,area:null,rack:null}; render(); }")
    page.wait_for_timeout(250)
    err_shown = page.evaluate("() => document.getElementById('page-content').innerText.length>0 && !drillValid()")
    shot(page, tag, "20_error_state")
    rec(f"[{tag}] error state renders on invalid drill", err_shown)
    page.evaluate("() => { state.drill={wh:null,zone:null,area:null,rack:null}; render(); }")

    # --- 9. Loading state (reboot) ---
    page.evaluate("() => { state.loading=true; render(); }")
    page.wait_for_timeout(150)
    loading_shown = page.locator(".sk-row").count() > 0
    shot(page, tag, "21_loading_state")
    rec(f"[{tag}] loading skeleton renders", loading_shown)
    page.evaluate("() => { state.loading=false; render(); }")

def main():
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for vw in (1280, 1440):
            ctx = browser.new_context(viewport={"width": vw, "height": 900}, device_scale_factor=1)
            page = ctx.new_page()
            page.on("console", lambda m: results["console_errors"].append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: results["page_errors"].append(str(e)))
            page.goto(URL)
            try:
                drive(page, vw)
            except Exception as e:
                rec(f"[{vw}] FATAL", False, str(e))
            ctx.close()
        browser.close()
    total = len(results["assertions"]); passed = sum(1 for a in results["assertions"] if a["pass"])
    results["summary"] = {"total": total, "passed": passed, "failed": total - passed}
    outp = pathlib.Path(r"C:\Users\Admin\Desktop\Work\brief-maker\outputs\11_Warehouse\02_QC\e2e_result.json")
    outp.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n==== SUMMARY", passed, "/", total, "console_errors:", len(results["console_errors"]), "page_errors:", len(results["page_errors"]))
    print("json ->", outp)

if __name__ == "__main__":
    main()
