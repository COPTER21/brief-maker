# DECISION_LOG — 11_Warehouse (F-LOCATION-MASTER-001 · Warehouse & Bin / Location Hierarchy)

> บันทึกมติก่อนเริ่ม WF-01 pipeline (HTML-first) · วันที่ 2026-08-06
> Feature นี้ = node **Warehouse & Bin** ของ Central Plan (Warehouse module, W3, Sellable Lite/Full)
> Input seed: legacy pack v2 (html-v3/frd-v5) เก็บไว้ที่ `_legacy/` — ใช้เป็น reference เท่านั้น

## มติที่ล็อกแล้ว

| # | มติ | ใครตัดสิน | เหตุผล |
|---|---|---|---|
| **D1** | Output = `outputs/11_Warehouse/` · feature id คง **F-LOCATION-MASTER-001** · ชื่อไฟล์ HTML = `WarehouseBin.html` | user | ต่อเนื่อง numbering (09 Bank, 10 Tax) |
| **D2** | **SKIP** `thai-doc-pdf-generator` (step 2) | AI แนะ + user ยืนยัน | master data ไม่ผลิตเอกสารพิมพ์ (ไม่มี PR/PO/ใบกำกับ) · ไม่ต้องการป้ายบาร์โค้ด location |
| **D3** | เพิ่ม **`branch_id` (required, soft-ref) บน `warehouses` เท่านั้น** — Zone/Area/Rack/Location สืบทอดสาขาผ่าน `warehouse_id` · **ไม่มี `company_id`** | PM/BA | 1 ERP = 1 บริษัท (company implicit) แต่ **multi-branch** → คลังต้องรู้สาขา · ปิด gap vs Central Plan GC#4 |
| **D4** | ~~**List view อย่างเดียว** · ตัด Tree view~~ ⚠️ **SUPERSEDED by D12** (user ขอ tree กลับ 2026-08-06) | AI แนะ + user | (เดิม: Tree = NON-STANDARD, List เจาะครบทุก action 100%) |
| **D5** | OQ-1..5 ตั้งเป็น `[AI-DEFAULT]` | AI แนะ + user | ดู `AI_DEFAULTS.md` |
| **D6** | **Regenerate ใหม่ HTML-first** — ของใหม่ supersede legacy · เก็บ legacy ที่ `_legacy/` เป็น reference/diff | AI แนะ + user | pipeline การันตี BRD/FRD ตรงกับ HTML (source of truth) · generator อ่าน legacy เป็น input → เนื้อหาดี ๆ (18 API/24 FN/edge/LD) ไม่หาย · เลี่ยง 2 สายพันธุ์เอกสาร |
| **D7** | **เพิ่ม branch filter/group ใน List view + branch ใน full_path** ("สาขา › WH › Zone › ...") | AI แนะ + user | multi-branch → กรองดูรายสาขาได้ + downstream (Inventory/GR) อ่าน path ง่าย · ต้นทุนต่ำ |
| **D8** | **RBAC = role-only** (ไม่ทำ branch-scoped data permission) · branch = **filter/UX เท่านั้น ไม่ใช่ security boundary** | AI แนะ + user | Central Plan วางสิทธิ์เป็น role→menu ล้วน ไม่มี row-level ที่ไหน · branch-scoped เป็นเรื่อง system-wide ของ **Permission Matrix (Policy & Security)** ไม่ใช่ master คลังประดิษฐ์เอง → ฝาก flag ไว้ที่นั่น (future) |
| **D9** | **Default location ต่อคลัง (receiving/pick/staging) = DEFER** ไปเฟส pick-pack-ship (W8/W9) | AI แนะ + user | consumer (GR/Picking) ยังไม่เกิด · type enum เดิม (RECEIVING_DOCK/STAGING/PACK) เว้นที่ไว้แล้ว เติม flag `is_default_*` ทีหลังได้ไม่ต้องรื้อ |
| **D10** | **Pill palette (แก้ QC UX-01):** **สถานะ 7 ตัว = color-code** ด้วย CUBE 5-variant + เฉด derive จาก tokens (active=info · full=warning · blocked/maintenance=red/orange · frozen/inactive=grey · decommissioned=grey จาง) · **ชนิด 10 ตัว = ไม่ color-code รายสี** แยกด้วย icon/label (หรือ 2-3 กลุ่ม storage/work-location/virtual) · **ห้ามใช้สี Tailwind/นอก palette** · ถือเป็น sanctioned CI extension (ไม่นับ drift) | AI แนะ | 17 สีตาแยกไม่ออก + ต้องอยู่ใน Warm Light · หลัก: color=state, icon=type อ่านง่ายกว่า + on-brand |
| **D11** | **Node delete → soft archive** (แก้ QC GAP-01): WH/Zone/Area/Rack เปลี่ยนจาก hard-delete เป็น **archive (soft, เก็บประวัติ + audit)** · คง referential-safe guard (มีลูก active = block) · microcopy "ลบ" → "จัดเก็บ" · **GAP-02:** reparent/edit location เพิ่ม stock guard (stock≠0 = block ตาม AD-5 / FN-19) | AI แนะ + user | Central Plan **GC#7 "ไม่มี hard delete ทุก module"** อยู่เหนือ legacy FN-08 · ให้ node สอดคล้อง location (decommission soft) + ทั้ง ERP · แก้ COVERAGE_MAP §4/§5 ที่ก่อนหน้าลอก framing "delete" มาจาก legacy โดยไม่ reconcile |
| **D12** | **(reverse D4) เอา Hierarchy Tree view กลับ = dual-view** — List (Pattern A drill-down) + **Hierarchy** (tree pane collapsible ซ้าย + node summary panel ขวา) · view switcher segmented ใต้ page header · แชร์ state `sel` เดียวกัน (สลับ view context คงอยู่) · Tree = **NON-STANDARD → approved deviation** (log LD ใน HTML + FRD) | user | user ขอ 2 view ตาม legacy BRD (hierarchy ลึก 5 ชั้น มองเป็น tree ชัดกว่า) · คง CI/token มาตรฐาน + iron rules ส่วนอื่นครบ |
| **D13** | ~~Role switcher = PROTOTYPE-ONLY (เก็บไว้ align ปุ่มสร้าง)~~ ⚠️ **SUPERSEDED by D15** — PM/BA สั่งถอด role switcher ออกจาก prototype เลย (มัน demo) | user (เดิม) | (เดิม: มีประโยชน์ตอน demo/QA — ตอนนี้ PM/BA ยืนยันไม่ต้องมีใน prototype) |
| **D14** | **Canonical display name = "Warehouse & Bin"** (TH: "คลังและตำแหน่ง") — ตรงกับ Central Plan node · เปลี่ยนจาก legacy "Location Hierarchy" ทุกที่ (sidebar/breadcrumb/h1/title) · โฟลเดอร์คง `11_Warehouse` · feature id คง F-LOCATION-MASTER-001 | user | ยึดชื่อตาม Central Plan (แผนกลาง = source of truth) |
| **D15** | **PM/BA feedback รอบ prototype review** (หลังเอา HTML ไปให้ดู): (a) **ถอด role switcher** ขวาบนออก (supersede D13) · perms()/ROLES/state.role='manager' คงไว้ (production role มาจาก auth) · (b) **breadcrumb: โชว์ชื่อ (name) แทน code** สำหรับ zone/area/rack — คลัง (warehouse) คง code ตาม legacy · (c) **ตัด branch ออกจาก path display ทั้งหมด** — ทั้ง breadcrumb (renderDrill) และ **fullPathStr / drawer "Full Path"** (pathChips L2154); fullPathStr เปลี่ยน code→ชื่อ (zone/area/rack) ให้ตรง breadcrumb, WH คง code, location คง code · **reverse ส่วน "branch ใน full_path" ของ D7 ทั้งหมด** (user เลือก) · branch ยังคงเป็น **field ในรายละเอียดคลัง** (D3) + **คอลัมน์/filter ใน List** (D7) — ไม่แตะ · (d) **ชื่อระดับ 5 = "ตำแหน่ง"** ทุกจุดที่ user เห็น (เลิกใช้ "Location" ผสม) · (e) ยืนยัน จังหวะกด/ลำดับ drill + order W→Z→A→R→L **เหมือน legacy อยู่แล้ว ไม่ต้องแก้** | PM/BA + user | อ่านง่ายขึ้น (code cryptic → name) · ตัด demo affordance · terminology สม่ำเสมอ (ระดับ 1-4 ไทย → ระดับ 5 ไทยด้วย, ตรง D14 "คลังและตำแหน่ง") |

## มติสืบเนื่อง (technical)

- **CI migration:** v3 (Navy/Primary/Teal, iron rules 31) → **v7 CUBE Warm Light** (Ivory/Charcoal/Red #FF3B30/Orange #FF9A1F), iron rules **#1-94**
- **branch picker + geo cascade + parent picker** = ใช้ Master Combobox pattern (Iron Rule #94) — search dropdown แบบเดียวกันทุกที่
- **ไม่ใช้ B2 Document Line Editor** — feature นี้ไม่มี line items แบบเอกสารธุรกรรม
- **RBAC only, no DOA** (LD-07 เดิม) · Delete = Manager/Admin (SoD)

## Golden rules กลางที่ feature นี้ต้องเคารพ (Central Plan)
- **GC#2** Inventory เป็นแกน check stock → location คือ "ที่เก็บ" ที่ Inventory อ้าง (`WH & Bin → Inventory`)
- **GC#4** คลังสังกัดสาขาในบริษัท → **branch_id** (D3)
- **GC#6** Soft-reference — master เป็น picker, nullable, ไม่ FK cascade, enforce format+uniqueness
- **GC#7** Append-only audit · soft archive · ไม่มี hard delete → decommission = soft keep history
- **GC#9** CI ล็อก + 1 ไฟล์ SPA

## Pipeline (ลำดับ skill)
1. html-generator-v7 → `01_HTML/WarehouseBin.html` + COVERAGE_MAP verify
2. ~~thai-doc-pdf~~ (SKIP — D2)
3. qc-ux-html-checker → `02_QC/`
4. qc-coverage-checker → `02_QC/` (เทียบกับ `COVERAGE_MAP.md`)
   — 🛑 **หยุดให้ user ตรวจ** —
5. brd-generator-full → `03_BRD/`
6. frd-generator-v6 → `04_FRD/`
7. html-ui-brief → `05_UI_BRIEF/`
8. ai-testcase-md-generator → `06_TESTCASES/`
9. qa-friendly-html-generator → `07_UAT/`
   → รวม `_final-docs/`
