# Coverage Report — F-LOC · Warehouse & Bin / คลังและตำแหน่ง (รอบ 1: HTML prototype)

- วันที่: 2026-08-12 · Feature: F-LOCATION-MASTER-001 (F-LOC)
- Scope source (ไม่มี workflow_graph.json/NODE_BRIEF ในรอบนี้ — ใช้ตามนี้เป็น contract):
  - `Pack Brief Feature\6. Warehouse\PREBRIEF_F-LOC_Warehouse-Location.md` (OB-1..13, S-01..S-12)
  - `Pack Brief Feature\6. Warehouse\FUNCTION_CHECKLIST_F-LOC_Warehouse-Location.md` (FN-01..FN-60)
  - Architecture edges (Central Plan): Company → Warehouse & Bin [config] · Warehouse & Bin → Inventory [config]
- Artifact ที่ตรวจ: `outputs\06_Warehouse-Bin\warehouse-bin.html` (single-file SPA, 1294 บรรทัด)
- Checklist จาก contract: FN 20 ข้อ · golden rules (OB) 13 · edges 2 (in 1 / out 1) · exception paths 5
- โหมด: REPORT-ONLY (ไม่แก้ไข HTML)

## Verdict: 🟢 PASS
สรุป: FN ครอบ 19/20 มี UI hook (1 partial: FN-23 audit-on-update) · 1 process-gate = NOT-CHECKED (FN-60) · edges 2/2 hooked · golden rules 13/13 reflect · exception paths 5/5 reachable · scope creep = 0
ไม่มี block-severity rule/edge ที่ ✗ หรือ △ → ผ่านรอบ HTML. residual เดียว (FN-23) เป็น warn-level ให้ปิดก่อน FRD/TC รอบ 2

---

## Coverage Matrix — FN Checklist (FN-01..FN-60)

| Item | ประเภท | HTML | Evidence (route/selector/function · บรรทัด) |
|---|---|---|---|
| FN-01 Drill 5 ระดับ + breadcrumb chip + stat 5 ใบ | nav | ✓ | `whRow/znRow/arRow/rkRow` onclick `selectNode(...)` (L521-524) · `drillPath()` chip กลับชั้น (L579-585) · stat 5 การ์ด `renderPage` (L705-709) |
| FN-02 Flat "Location ทั้งหมด" + path col + ค้น/กรอง | nav | ✓ | stat การ์ด `is-click` onclick `selectNode('all-locations')` (L709) · `contentBody` all-locations + `locRowFlat`+`locPathShort` คอลัมน์ path (L596-610) · `locFilter:true` |
| FN-03 Area tab Racks / Location ตรง (flexible) | nav | ✓ | `seg` + `setAreaTab('racks'/'locs')` เฉพาะ area `allows_direct` (L616-621) |
| FN-04 Hierarchy tree + node summary #96 full-height | nav | ✓ | `renderTree()` (L477) + `nodeSummary()` (L639) แชร์ `state.sel` · `.explorer{height:calc(100vh-330px);min-height:420px}` (L100) · view switch (L700-703) |
| FN-05 WH form geo cascade + postcode auto readonly + ล้างชั้นล่าง | crud | ✓ | `setProvince/setDistrict/setSubdistrict` ล้างลูก (L779-781) · `geoPostcode` auto · `#f-postcode ... readonly` placeholder="" (L1063) |
| FN-10 Zone temp range · Area allows_direct · Rack R×C×L | crud | ✓ | Zone toggle+temp min/max (L1075-1076) · Area `allows_direct` toggle (L1089) · Rack rows/cols/levels (L1101) |
| FN-13 Location wizard 2 ขั้น + type 10 + พิกัด + flags | crud | ✓ | `renderLocationForm` step1/step2 (L1108-1163) · `TYPES` 10 ค่า (L448) · พิกัด row/col/level/position (L1144) · behavior flags (L1147-1154) |
| FN-14 code unique in parent · parent=area ต้อง allows_direct | rule | ✓ | `submitLoc` dup check (L856-857) · `locNext` allows_direct block (L849) · `quickAdd` dup check (L994) |
| FN-15 storage_uom บังคับ (7) · lock เมื่อ hasStock + "1 ตำแหน่ง 1 หน่วย" · list col + view | rule | ✓ | `STORAGE_UOMS` 7 (L372) · `#f-storage-uom ...disabled` เมื่อ hasStock (L1137) + ข้อความ lock (L1138) · list col (L531,601) · view drawer "1 ตำแหน่ง 1 หน่วย · มีสต็อก — ล็อก" (L1249) |
| FN-16 View drawer full path + ข้อมูล + ลูก + audit | crud | ✓ | `renderViewDrawer` (L1204) · loc tabs ภาพรวม/ความจุ/ประวัติ `renderLocViewTabsBody` (L1240) · audit timeline (L1260) |
| FN-20 statusMenu portal (fixed+flip, คลิกนอกปิด capture) 4 ค่า, full ไม่ตั้งมือ | status | ✓ | `statusPillMenu`+`openStatusMenu` portal (L921-934) flip (L933) · capture close (L935) · `LOC_STATUS_OPTS` 4 ค่า ไม่มี full (L920) |
| FN-21 blocked/frozen → modal เหตุผล → apply+audit+toast | status | ✓ | `pickStatus` เปิด modal status-reason (L948-951) · `renderModal` reason (L1267-1276) · `confirmStatusReason` บังคับเหตุผล (L937-939) · `applyStatus` audit (L956) |
| FN-22 Bulk select checkbox + bulk bar 4 สถานะ + ตั้ง uom ข้าม hasStock นับแจ้ง | bulk | ✓ | checkbox `locRow`/`locRowFlat` (L526,597) · `bulkBar` (L962-972) · `bulkStatus` (L974) · `bulkUom` ข้าม hasStock + นับ skip (L980-985) · `clearBulk` (L961) |
| FN-23 ทุก mutation ลง audit ต่อ node (append-only) | rule | △ | append มีจริงใน status/quick-add/bulk-uom (`applyStatus` L956, `quickAdd` L997, `bulkUom` L984) · **แต่ create/edit ผ่าน drawer (`submitForm` L818-843, `submitLoc` L859-863, `submitBulk` L889) ไม่ append AUDIT** · view ยังเห็น entry เพราะ `auditOf` fallback สังเคราะห์ (L397) → update ไม่ทิ้งร่องรอย |
| FN-30 Bulk generation preset 3 + custom + preview 5 + total + uom ทุกตัว + atomic | create | ✓ | `BULK_PRESETS` 3 (L873-877) · custom pattern inputs · `bulkPreviewNames(b,5)` (L1194) · total (L1195-1196) · `#b-storage-uom` ทุกตำแหน่ง (L1190) · atomic toast (L890) — *mock: `submitBulk` push 1 แถวตัวอย่าง (L889), UI hook ครบ* |
| FN-31 Quick add row (rack + area direct) code+type+uom + default cap + dup + audit | create | ✓ | `quickAddRow` (L1000-1010) · `quickAdd` dup guard (L994) · default `cap_val:1` (L996) · audit append (L997) |
| FN-40 RBAC canManage — ไม่มี DOA | guard | ✓ | `canManage` (L303) · `openDrawer` guard (L723) · `phActions`/`actionsCell` gated (L513-517,568-576) — ไม่มีสาย DOA (ตรง scope lock OB-11) |
| FN-41 ลบ = confirm modal · hasStock/มีลูก active → block | guard | ✓ | `openModal`/`renderModal` (L894,1278) · `blockReason` children+hasStock (L896-902) · `confirmModal` เช็ค reason (L904-905) · location = decommission เก็บประวัติ (L910) |
| FN-50 CI Warm Light + Satoshi + inline sprite (no CDN) + no-hint + Rule#40 + #51 2col + drawer 680 | ci | ✓* | inline sprite `ICONS` (L285) · drawer 680 (L169) · `.form-grid` 2col (L190) · Rule#40 คอลัมน์รหัส/ชื่อแยก · *ข้อสังเกต: มี `<link>` Google Fonts + Fontshare CDN (L7-9) ขัด "no CDN" — เป็นเรื่อง CI/form → ส่งต่อ `qc-ux-html-checker` ไม่นับ scope gap* |
| FN-60 Gate: node --check · audit metrics · E2E · md5 | process | ⬜ | NOT-CHECKED — เป็น build/ship gate ตรวจจากเนื้อ HTML ไม่ได้ (ต้องรัน build.py/capture ในไปป์ไลน์) |

## Coverage Matrix — Architecture Edges

| Item | ประเภท | HTML | Evidence |
|---|---|---|---|
| Company → Warehouse & Bin (branch_id, [config]) | edge in | ✓ | Branch combobox active-only `activeBranches`/`branchFiltered` (L324,795) · required at create `submitForm` (L819) · snapshot: `branchLabel` resolve by id แม้ inactive (L323) · branch คอลัมน์ list `branchCell` (L520-521) · view drawer `branchLabel` (L1220) · seed มี mock inactive `00003 สาขาระยอง` (L320) |
| Warehouse & Bin → Inventory (ยอดต่อที่เก็บ, [config] soft) | edge out | ✓ | สัญญา soft surface เป็น storage_uom lock + `hasStock` flag (mock ใน `mkLoc`/LOCATIONS L373-391) · lock ล็อก uom เมื่อ hasStock (L1137-1138) — ตรง scope lock (ไม่เรียก live Inventory) |

## Coverage Matrix — Golden Rules (OB / PREBRIEF)

| Item | HTML | Evidence |
|---|---|---|
| OB-1 5-level CRUD · code unique in parent · referential-safe delete | ✓ | CRUD 5 ระดับ (`submitForm`/`submitLoc`) · dup check (L856,994) · `blockReason` referential (L896-902) |
| OB-2 Flexible parent Location ใต้ Rack XOR Area(allows_direct) | ✓ | radio parent_type (L1120-1121) · `locNext` allows_direct XOR (L849) · `parentContext` (L753-757) |
| OB-3 Location type 10 ค่า (รวม PACK) | ✓ | `TYPES` = 10 (L448) รวม PACK/RECEIVING_DOCK/TRANSIT/VIRTUAL |
| OB-5 storage_uom 1-loc-1-uom lock (แยกจาก cap_uom) | ✓ | ล็อก uom เมื่อ hasStock (L1137-1138) · cap_uom แยก field (L1141) |
| OB-6 สถานะ 4 ค่า + full derived · blocked/frozen ต้องมีเหตุผล + audit | ✓ | `LOC_STATUS_OPTS` 4 (L920) · full ไม่อยู่ในเมนู (derived) · reason modal (L1267-1276) · audit (L956) |
| OB-7 decommission ต้อง stock=0 · zone/area มีลูก → block | ✓ | `blockReason` location hasStock (L901) · zone/area/rack มีลูก block (L897-900) · location = soft decommission (L910) |
| OB-8 Geo cascade จังหวัด→อำเภอ→ตำบล→ไปรษณีย์ auto | ✓ | `TH_GEO` cascade + auto postcode (L326-336,779-781) |
| OB-9 Bulk generation atomic + live preview | ✓ | `renderBulkDrawer` preview 5 + total (L1194-1196) · atomic (L889-890) |
| OB-10 จอปฏิบัติงาน: flat + statusMenu + bulk + quick add | ✓ | all-locations (L606) · statusMenu (L921) · bulkBar (L962) · quickAddRow (L1000) |
| OB-11 ไม่มี DOA — RBAC canManage | ✓ | `canManage` gating (L303,723) — ไม่มี approval chain (ตรง scope lock) |
| OB-12 CI + audit per node (WORM append-only) | ✓* | audit timeline WORM (L1260) · *ดู FN-23 △ update ไม่ append + FN-50 CDN font note* |
| OB-13 Engines ประกาศ (ENG-LOC-GEN/ENG-HIER-PATH) | ⬜ | เป็น backend engine declaration — ไม่มี hook ใน UI (เก็บที่ FRD 03_LOGIC รอบ 2), ไม่ใช่ gap ของ HTML |

## Exception / Negative Paths (ต้องมีทางเข้าใน UI)

| Path | HTML | Evidence |
|---|---|---|
| Blocked/Frozen → reason modal | ✓ | `pickStatus`→status-reason modal (L948-951,1267) บังคับเหตุผล (L939) |
| Delete/Decommission block (มีลูก / hasStock) | ✓ | `blockReason` warn-box แดง + ปุ่มลบ disabled (L1286-1288) |
| Validation errors | ✓ | toast: ไม่มีรหัส/ชื่อ/สาขา (L816-819) · dup code (L857,994) · area ไม่ allows_direct (L849) · cap ≤ 0 (L854) |
| Empty state (ไม่พบรายการ) | ✓ | `listCard` empty block (L554) พร้อมข้อความปรับตัวกรอง |
| Active-only branch filter (inactive ถูกกรอง) | ✓ | `activeBranches` กรอง `00003 สาขาระยอง` (active:false) ออกจาก picker (L320,324,795) |

---

## 🟡 Warnings / Residuals

### GAP-01 (warn-level) · FN-23 / OB-12 · audit ไม่ append ตอน create/update ผ่าน drawer
- หาย: การเขียน AUDIT entry เมื่อ **สร้าง/แก้ไข** Warehouse/Zone/Area/Rack/Location และ bulk-gen — ปัจจุบัน append เฉพาะ statusMenu, quick-add, bulk-uom
- ผลกระทบ: "update" ไม่ทิ้งร่องรอย; view ยังเห็น entry เพราะ `auditOf()` สังเคราะห์ fallback (ไม่ใช่ append จริง) → ขัดข้อความ FN-23/S-12 "ทุก mutation ลง audit ต่อ node"
- ไม่ block รอบ HTML (audit ยัง surface ได้ + ไม่ใช่ block-severity rule) แต่ควรปิดก่อน dev
- แก้ที่: `warehouse-bin.html` — เพิ่ม `AUDIT[id].unshift({...})` ใน `submitForm` (L818-843), `submitLoc` (L859-863), `submitBulk` (L889) · และรอบ 2 ระบุใน FRD 03_LOGIC ว่าทุก create/update/delete ต้อง append WORM audit + TC ครอบ

### OBS-01 (ส่งต่อ qc-ux, ไม่ใช่ scope gap) · FN-50 "no CDN" ขัด
- `warehouse-bin.html` L7-9 มี `<link>` ไป `fonts.googleapis.com` + `api.fontshare.com` — OB-12/FN-50 ระบุ "ห้าม CDN" · เป็นเรื่อง CI/form ไม่ใช่ business coverage → ให้ `qc-ux-html-checker` จัดการ (inline/ฝังฟอนต์)

## ⬜ NOT-CHECKED
- FN-60 (build/ship gate: node --check, audit metrics 0, E2E ~25, md5) — ตรวจจากเนื้อ HTML ไม่ได้ ต้องรันสคริปต์ไปป์ไลน์
- OB-13 Engine registration (ENG-LOC-GEN / ENG-HIER-PATH) — backend declaration, เก็บที่ FRD รอบ 2

## Scope-Creep Check
- **ไม่พบ scope creep.** ของที่ de-scoped (F-INV build-out, Geo Master schema, GRN/Putaway/RTV/Pick-Pack-Ship, DOA) **ไม่โผล่เป็น flow ใน HTML**
- Sidebar มีรายการ Product/Vendor Master, Stock by Location, **Goods Receipt**, Settings — ทั้งหมด `is-disabled` (shell nav placeholder เท่านั้น, ไม่มี route/flow จริง) → ไม่ใช่ creep, สอดคล้องกับการไม่ build GRN
- Mock inactive branch `00003 สาขาระยอง` (L320) = [AI-DEFAULT] ตั้งใจใส่เพื่อสาธิต active-only filter → **คาดไว้แล้ว ไม่ใช่ creep**
- `hasStock` + storage_uom lock = soft [config] ของ edge Inventory (mock) → อยู่ในสัญญา ไม่ใช่ creep

## 💡 เสนอเข้า contract (ไม่กระทบ verdict)
- รอบนี้ไม่มี workflow_graph.json/NODE_BRIEF — แนะนำรัน `plan-module-workflow-mapper` สร้าง graph จริงของ F-LOC ก่อน dev handoff เพื่อ lock edge Company/Inventory เป็น contract ที่ตรวจซ้ำได้ (รอบ 2 จะได้เทียบ FRD/TC กับ graph โดยตรง)

## Diff จากรอบก่อน
- ไม่มี (รอบ 1 แรกของ artifact นี้)
