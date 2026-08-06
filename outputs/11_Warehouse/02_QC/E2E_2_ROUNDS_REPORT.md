# E2E 2-ROUND REPORT — WarehouseBin.html (F-LOCATION-MASTER-001 · คลังและตำแหน่ง / Warehouse & Bin)

> Playwright end-to-end verification · single-file SPA · run via project venv · **VERIFY-ONLY (ไม่แก้ HTML)**
> วันที่รัน 2026-08-06 · driver `02_QC/e2e_2rounds_warehouse.py` · หลักฐานภาพ `02_QC/e2e_shots/` (159 shots)

## ✅ VERDICT: PASS

| Metric | ค่า |
|---|---|
| Total assertions passed | **213** |
| Total failed | **0** |
| Console errors | **0** |
| Page (JS) errors | **0** |
| Viewports | 1280, 1440, 1920 |

เกณฑ์ผ่าน = ทุก assertion เขียว **และ** 0 console error **และ** 0 page error ในทุก viewport ของทุกรอบ → ครบทั้งหมด.

| รอบ | pass | fail | console err | page err | ทุก viewport เขียว |
|---|---|---|---|---|---|
| Round 1 | 90 | 0 | 0 | 0 | ✅ |
| Round 2 | 123 | 0 | 0 | 0 | ✅ |

> หมายเหตุ: pass count เป็นผลรวม 3 viewport (assertion เดียว × 3). Round 1 = 30×3=90 · Round 2 = 41×3=123.

## Round 1 — Happy-path lifecycle + Dual-view (สร้างคลังทั้งต้นจนครบ 5 ระดับ + สลับ List/Hierarchy)

_30 assertions (แสดง viewport 1280 เป็นตัวแทน — ผลตรงกันทั้ง 1280/1440/1920)_

- [x] root list renders (5 KPI stats + drill chip) — stats=5 chips=1
- [x] D14 title shows คลังและตำแหน่ง (Warehouse & Bin) — คลังและตำแหน่ง (Warehouse & Bin) · Warm Light
- [x] D14 sidebar label = คลังและตำแหน่ง — คลังและตำแหน่ง
- [x] WH create drawer opens (node-form/warehouse)
- [x] geo cascade resets child levels when province picked
- [x] geo cascade auto-fills postcode (ตำบล -> 10540) — form=10540 dom=10540
- [x] WH persisted (branch=BR-01, postcode=10540, active, drawer closed) — {"id": "WAREHOUSE-855658", "branch": "BR-01", "pc": "10540", "st": "active"}
- [x] KPI warehouse count updated after create — kpi_first_stat=4
- [x] branch chip shown in drill breadcrumb after drilling into WH — สาขา
สาขา 1 (บางนา)
- [x] Zone persisted (temp_controlled true, range 2-8, under new WH) — {"id": "ZONE-857888", "wh": "WAREHOUSE-855658", "tc": true, "mn": 2, "mx": 8}
- [x] Area persisted (allows_direct true, under new Zone) — {"id": "AREA-859799", "zone": "ZONE-857888", "ad": true}
- [x] Rack persisted (grid 2x3x2, under new Area) — {"id": "RACK-861480", "area": "AREA-859799", "rows": 2, "cols": 3, "levels": 2}
- [x] Location wizard step 1 opens (loc-form)
- [x] Location wizard advances to step 2 (2-step, stepper=2)
- [x] Location persisted via wizard (type=PACK, cap=5>0, barcode set -> active) — {"id": "LOC-863762", "type": "PACK", "cap": 5, "rack": "RACK-861480", "bc": "8859999000019", "st": "active"}
- [x] Bulk Generate drawer opens
- [x] Bulk preview count = 2 racks x 2 = 4 locations — preview='2 ชั้นวาง × 2 = 4' calc={"per": 2, "qty": 2, "total": 4}
- [x] Bulk commit atomic (+2 racks, +4 locations, drawer closed) — racks 6->8 locs 15->19
- [x] view-location drawer opens with 3 tabs — tabs=3
- [x] view-loc capacity&flags tab renders (real click, non-blank) — ov_len=308
- [x] view-loc history tab renders
- [x] view-node shows full_path with branch in breadcrumb (bold + ' › ') — <b>สาขา 1 (บางนา)</b> › WH-E2E
- [x] view-node shows child counts + drill button
- [x] 5-level drill reaches rack level + location list rows present — levels=['warehouse', 'zone', 'area', 'rack'] locrows=2
- [x] D12 view switcher -> Hierarchy renders tree pane + summary
- [x] D12 view switcher -> List renders table
- [x] D12 tree expand/collapse toggles children — {"before": 0, "afterOpen": 1, "afterClose": 0}
- [x] D12 tree select -> summary panel (sel synced + code + level badge + full path + child chips) — {"zid": "Z-STORAGE", "zcode": "Z-STG", "selLevel": "zone", "selId": "Z-STORAGE", "title": "Z-STG", "badge": true, "pathOk": true, "chips": 1}
- [x] D12 child chip -> switches to List drilled to that node — {"view": "list", "drillZone": "Z-STORAGE", "level": "zone"}
- [x] D12 shared selection preserved BOTH directions (List<->Tree) — {"selInList": "{\"level\":\"area\",\"id\":\"A-FM\"}", "aCode": "A-FM", "aId": "A-FM", "shownCode": "A-FM", "ancestorsOpen": true, "backLevel": "area", "backArea": "A-FM"}

## Round 2 — Negative / Guards / RBAC / State / Robustness (ทุกเคสต้องบล็อก/behave ถูก)

_41 assertions (แสดง viewport 1280 เป็นตัวแทน — ผลตรงกันทั้ง 1280/1440/1920)_

- [x] flexible-parent XOR: exactly one parent id set; other nulled on switch — one=True swap=True
- [x] flexible-parent XOR: neither parent selected -> blocked at step 1 — กรุณาเลือกพื้นที่
- [x] allows_direct=false blocks direct location + suggests 'เพิ่มชั้นวางก่อน' — err='พื้นที่นี้ allows_direct = false — เลือกพื้นที่อื่น หรือเพิ่มชั้นวางก่อน'
- [x] duplicate code blocked at warehouse level (409-style, no insert) — err='รหัสซ้ำในระบบ'
- [x] duplicate code blocked at zone level (409-style, no insert) — err='รหัสซ้ำภายในคลังเดียวกัน'
- [x] duplicate code blocked at area level (409-style, no insert) — err='รหัสซ้ำภายในโซนเดียวกัน'
- [x] duplicate code blocked at rack level (409-style, no insert) — err='รหัสซ้ำภายในพื้นที่เดียวกัน'
- [x] duplicate code blocked at location level (within parent, no insert) — รหัสซ้ำภายใน parent เดียวกัน
- [x] capacity <= 0 blocked (no insert) — ความจุต้องมากกว่า 0
- [x] zone temp_controlled with missing range blocked (no insert) — กรุณากรอกช่วงอุณหภูมิ
- [x] bulk-gen collision -> atomic rollback (submit disabled, 0 rows added) — collisions=2 disabled=True racks==True locs==True
- [x] bulk-gen grid=0 -> blocked (total 0, submit disabled, no insert) — total=0 disabled=True
- [x] GAP-02 reparent BLOCKED when location has stock (parent unchanged, drawer stays w/ error) — {"rack": "R-A01", "drawerOpen": true, "hasErr": true}
- [x] GAP-01 archive blocked when node has active children (no confirm path, block msg shown) — {"kids": 4, "hasConfirm": false, "blockText": true, "status": "active"}
- [x] GAP-01 blocked node stays active — WH-01 status=active
- [x] decommission location with stock blocked (no confirm, status unchanged) — {"block": true, "hasConfirm": false, "status": "active"}
- [x] barcode required before activate (L006 no barcode stays inactive) — inactive -> inactive
- [x] RBAC Operator = view-only (perms create/del/status all false) — {"create": false, "del": false, "status": false}
- [x] RBAC Operator: header create button disabled
- [x] RBAC Operator: no edit/archive controls in view drawer — {"edit": false, "danger": false}
- [x] RBAC Supervisor: create/edit yes, archive/delete no (del=false) — {"create": true, "del": false, "status": true}
- [x] RBAC Supervisor: header create enabled
- [x] RBAC Supervisor: edit present but archive (danger) hidden in view drawer — {"edit": true, "danger": false}
- [x] RBAC Manager: full (create + del/archive + status) — {"create": true, "del": true, "status": true}
- [x] D13 role switcher aligned with create button (top & height within 2px) — {"dTop": 0, "dH": 0}
- [x] 7-state: active->blocked(+reason)->active — {"st": "blocked", "reason": "ทดสอบบล็อก E2E"}
- [x] 7-state: frozen / maintenance / full transitions apply — frozen=frozen maint=maintenance full=full
- [x] 7-state: decommission is SOFT-kept (record stays, status=decommissioned, length unchanged) — {"exists": true, "st": "decommissioned", "len": 14}
- [x] state transitions each write WORM audit entries — audit 0->9
- [x] node soft-archive: record kept, status=archived, 'จัดเก็บแล้ว' badge shown in list — {"exists": true, "status": "archived", "badgeOnList": true}
- [x] refresh-safe: reload mid-drill renders valid root without crash (no page errors) — level area -> root
- [x] refresh-safe: reload mid-drawer -> drawer closed, valid render, no crash
- [x] Esc chain tier 1: combobox list closes first, drawer stays open — comboOpen=True comboClosed=True drawer=True
- [x] in-drawer modal renders ABOVE drawer (z-index measured + elementFromPoint=modal) — {"modalBackdropZ": "70", "modalZ": "auto", "drawerBackdropZ": "50", "drawerZ": "55", "topmostAtModalCenter": "modal"}
- [x] Esc chain tier 2: modal closes first, drawer stays — modalClosed=True drawer=True
- [x] Esc chain tier 3: next Esc closes drawer
- [x] drawer content re-renders after in-drawer tab switch (persists, not blank/collapsed) — len 320 -> 340 open=True
- [x] empty state renders on no-match filter
- [x] loading skeleton renders — sk-line=6
- [x] error state renders when drilling into a deleted/missing node
- [x] geo cascade resets district/subdistrict/postcode when province changes — pc1=10540 after={"d": "", "s": "", "p": ""}

## หมายเหตุถึงผู้ทดสอบมือ (by-design ไม่ใช่ bug)
- **UX-06 (drill/tree position in-memory):** refresh กลางทาง กลับ root — mock ไม่ hash-encode ตำแหน่ง drill (ไม่มี spec บังคับ) ไม่ crash/ไม่มี error. Round 2 ยืนยัน reload-safe ทั้ง mid-drill และ mid-drawer.
- **UX-07 (role switcher):** เป็น prototype affordance ช่วยทดสอบ RBAC — dev ต้องลบตอน production (D13). E2E ยืนยัน alignment กับปุ่มสร้าง + perm ต่อ role ถูกต้อง.
- **UX-08 (tree keyboard nav):** tree row ยังไม่มี arrow-key navigation (toggle/switcher เป็น real button แล้ว) — carry ลง FRD/UI-brief.

## Latent-bug regression (base-kit) — CLEAN
- in-drawer modal z-index: modal อยู่เหนือ drawer จริง (measured + elementFromPoint=modal). ✅
- drawer re-render หลัง in-drawer action/tab switch: เนื้อหาคงอยู่ ไม่ว่าง/ไม่ยุบ. ✅
- Esc chain 3 tier (combobox → modal → drawer) ทำงานตามลำดับ. ✅

---
**สรุป:** HTML prototype ผ่าน E2E 2 รอบเต็ม (Happy + Negative/Guards/RBAC/State) ทุก viewport ไม่มี error → **พร้อมให้ทดสอบมือ**. เมื่อทดสอบมือผ่าน → เปิด gate เข้าขั้นที่ 5 (brd-generator-full).