# COVERAGE_MAP — 11_Warehouse (F-LOCATION-MASTER-001 · Warehouse & Bin)

> **ยาร์ดสติ๊กสำหรับ qc-coverage-checker** — สกัด scope จาก Central Plan (node Warehouse & Bin) + legacy pack
> ทุก ✓ ตอน QC ต้องชี้ evidence ใน HTML ได้ · ครบตามนี้ = PASS

## 1. Node identity
- **Warehouse & Bin** · Warehouse module · Wave W3 · Sellable (Lite/Full — แต่เส้นที่เกี่ยวเป็น `[config]` soft-ref จึง **ไม่ต้องทำ dual-mode** ตาม §1 Central Plan)
- ขอบเขต: master จัดโครงสร้างจัดเก็บ **5 ระดับ** ผ่าน UI เดียว

## 2. Hierarchy / entities ที่ต้องมี (CRUD ครบ)
| ระดับ | Entity | key attributes |
|---|---|---|
| L1 | warehouses | code, name, **branch_id (required, soft-ref)** ⭐NEW, geo address (province→district→subdistrict→postcode cascade), status |
| L2 | zones | code, name, warehouse_id, temp_controlled + temp_min/max, status |
| L3 | areas | code, name, zone_id, **allows_direct** (flexible-parent gate), status |
| L4 | racks | code, name, area_id, rows/cols/levels (grid), status |
| L5 | locations | code, **parent_type rack XOR area**, type (10 core incl PACK), capacity(uom+val>0), rotation, coords, behavior flags, mixing flags, 7-state status, barcode/qr |

## 3. เส้นเชื่อม (edges) — ต้องมี hook/mock ใน UI
| ทิศ | เส้น | ชนิด | ต้องเห็นใน HTML |
|---|---|---|---|
| IN | **Company → Warehouse & Bin** (branch) ⭐NEW | `config` soft-ref | branch picker ในฟอร์ม WH |
| IN | Geo Master → Warehouse (address) | `config` read-only | cascade dropdown (mock TH_GEO) |
| IN | Inventory → (hasStock flag) | runtime read | gate decommission (stock≠0 → block) |
| OUT | **Warehouse & Bin → Inventory** (ยอดต่อที่เก็บ) | `config` | location_id + full_path expose |
| OUT | location_id → GR / Put Away / Picking / RTV / Stock Adj / Transfer / Stocktake | ref | type enum + path เป็น contract |
| OUT | ENG-HIER-PATH (full path) | engine | reuse ได้โดย feature อื่น |

## 4. หน้าจอที่ต้องมี (screens)
- [ ] List view drill-down (WH→Zone→Area→Rack→Location) + KPI 5 ระดับ + filter (type/status ที่ location level) + **branch filter/group** (D7) + **branch ใน full_path** ("สาขา › WH › ...")
- [ ] Create/Edit node — WH (**branch + geo**), Zone (temp), Area (allows_direct), Rack (grid)
- [ ] Create/Edit Location — 2-step wizard (parent&identity → capacity&behavior)
- [ ] View — Location (3 tabs) / node (fields + path + child counts)
- [ ] Bulk Generate (template + preview + collision check + atomic)
- [ ] Archive (node WH/Zone/Area/Rack — **soft**, referential-safe: มีลูก active=block) / Decommission (location — soft, empty-before) · modal (D11)
- [ ] **Hierarchy Tree view** (D12) — view switcher segmented (List / Hierarchy) ใต้ page header · tree pane ซ้าย (WH→Zone→Area→Rack collapsible + count/level badge ทุก node) · node summary panel ขวา (icon+level badge, ชื่อ/code/status, full path, attribute fields, child stat chips คลิก→สลับ List, actions) · แชร์ state `sel` · NON-STANDARD = approved deviation

## 5. Golden rules ที่ต้อง reflect (ต้องเห็นพฤติกรรมใน UI)
- [ ] **GC#4** branch — คลังผูกสาขา (required)
- [ ] **GC#6** soft-reference — picker เท่านั้น, ไม่ cascade
- [ ] **GC#7** ไม่มี hard delete ทุกระดับ — node = archive soft · location = decommission soft · เก็บ history + audit WORM ทุก mutation (D11)
- [ ] flexible parent = rack **XOR** area (CHECK + inline validate)
- [ ] allows_direct gate — parent=area ต้อง allows_direct=true
- [ ] node code unique within parent (ทุกระดับ)
- [ ] capacity > 0 · zone temp range required ถ้า temp_controlled
- [ ] bulk-gen atomic + preview
- [ ] RBAC 5 roles · **delete = Manager/Admin เท่านั้น** (SoD)

## 6. Exception / edge paths ที่ต้องมีทางเข้าใน UI (EC-01..17)
flexible-parent violation · allows_direct block + แนะเพิ่ม rack · referential-safe delete (มีลูก=block) · empty-before-decommission (stock≠0=block) · bulk-gen collision (atomic rollback) · reparent code uniqueness re-check · ปิด allows_direct ทั้งที่มี direct loc=block · zone temp missing=block · code ซ้ำ=409 · geo cascade reset · Operator=view only (403) · Supervisor ลบไม่ได้ (403)

## 7. Out of scope (กัน scope creep — ถ้าเจอใน HTML = WARN)
- Geo Master CRUD เอง (consume read-only เท่านั้น)
- stock / on-hand management (อยู่ F-INV-STOCK — ใช้แค่ flag hasStock)
- DOA / approval workflow (LD-07 — RBAC เท่านั้น)
- pick_sequence · capacity หลายมิติ (weight/volume) · ABC class
- PACK ↔ Ship dock flow (pick-pack-ship feature)
- company_id / multi-company (1 ERP = 1 company — D3)
- branch-scoped data permission (D8 — role-only; ฝาก Permission Matrix เป็น system-wide)
- default location ต่อคลัง (D9 — defer → pick-pack-ship)
