# PREBRIEF — F-LOC · Warehouse Location Hierarchy (แม่แบบตำแหน่งจัดเก็บ)

> **Source of truth เชิง business** — สกัดจากของเดิม (BRD_F-LOCATION-MASTER-001_v2 + FRD FULL 9 ไฟล์ v5.1) + มติ vibe 2026-08-10 ทั้งชุด
> HTML = source of truth (Reverse Mode) · ไฟล์: `f-loc.html` · Master ต้นทางของ F-INV (mock L001-L017 ชุดเดียวกัน)

---

## §0 Obligations

| # | พันธะ | ต้นทาง | อ้างกลับ |
|---|---|---|---|
| OB-1 | โครงสร้าง 5 ระดับ Warehouse › Zone › Area › Rack › Location — CRUD ครบทุกระดับใน UI เดียว, code unique ภายใน parent, referential-safe delete | LD-09 (FRD v2) | S-01..S-05 |
| OB-2 | **Flexible parent**: Location อยู่ใต้ Rack **XOR** Area (เฉพาะ area ที่ `allows_direct_location=true`) | LD-01/LD-02 | S-05, FN-14 |
| OB-3 | Location type 10 ค่า (รวม PACK) — schema-ready ขยายได้ | LD-03 | FN-13 |
| OB-4 | **Dual-view**: List (drill) + Hierarchy tree+summary แชร์ state เดียว — tree เป็น NON-STANDARD (OQ-LOC-02 รอ Chin) | LD-10 | S-06 |
| OB-5 | **storage_uom ต่อ location** (LOCK **1-loc-1-uom** จาก F-INV): ทุกตำแหน่งประกาศหน่วยเก็บสินค้า 1 หน่วย · เปลี่ยนไม่ได้เมื่อ `hasStock` `[AI-DRAFT → OQ-LOC-06]` · แยกชัดจาก `cap_uom` (หน่วยความจุ pallet/box/cbm) | มติ 2026-08-10 · PREBRIEF F-INV OB-4 | S-05, S-08, FN-15 |
| OB-6 | สถานะ location: active / inactive / blocked / frozen (+ full = derived) — **blocked/frozen ต้องมีเหตุผล** และลง audit ทุกครั้ง | FRD 05_RULES + มติ statusMenu | S-07, FN-20..22 |
| OB-7 | Deactivate/Decommission ต้อง stock=0 · decommission เก็บประวัติ (soft) · Zone/Area ที่มีลูก active → block (default) | LD-06 / OQ-LOC-04 | S-09 |
| OB-8 | Geo cascade: จังหวัด → อำเภอ/เขต → ตำบล/แขวง → รหัสไปรษณีย์เติมอัตโนมัติ (readonly, ไม่มี placeholder) — Geo Master เป็น feature แยก (OQ-LOC-01) | FRD 01_UI + มติ | FN-05 |
| OB-9 | **Bulk generation**: preset 3 รูปแบบ + live preview ชื่อ 5 ตัวแรก + จำนวนรวม — atomic, no partial commit | LD-05 + มติ D | S-10, FN-30 |
| OB-10 | **จอปฏิบัติงาน (มติ enhance A-D)**: flat "Location ทั้งหมด" ข้ามชั้น + statusMenu คลิก pill + bulk select (สถานะ/ตั้งหน่วยเก็บ ข้าม hasStock) + quick add row | มติ 2026-08-10 | S-02, S-07, S-08, S-11 |
| OB-11 | ไม่มี DOA — operational master ใช้ RBAC (Warehouse Manager เจ้าของ) | LD-07 | FN-40 |
| OB-12 | CI Warm Light + Satoshi + inline sprite (ห้าม CDN) + #67.1 no-hint + Rule #40 (คอลัมน์รหัส/ชื่อแยก) + #51 form grid 2 คอลัมน์ + drawer 680 + #96 tree full-height + WORM audit ต่อ node | v8 + มติ review | FN-50 |
| OB-13 | Engines ประกาศใน feature (engine-in-feature): `ENG-LOC-GEN` (location-generation) + `ENG-HIER-PATH` (path builder) — รอ Architect register | LD-08 | §6 |

---

## §1 Scope

**ทำ:** Master แม่แบบตำแหน่งจัดเก็บทุกคลัง — CRUD 5 ระดับ + flexible parent + geo address + storage_uom + สถานะ operational (block/freeze พร้อมเหตุผล) + bulk generation + flat list + bulk operations + quick add + dual view + audit ต่อ node
**ไม่ทำ:** ยอดสต็อก/movement (F-INV) · Putaway/GRN/RTV · Geo Master schema เต็ม (feature แยก — ที่นี่ lookup อย่างเดียว) · re-parent live migration (OQ-LOC-05)

**เส้นออก (downstream):** F-INV (location_id + storage_uom + loc_status + hasStock) · GRN/Putaway/RTV · pick-pack-ship (PACK type)
**เส้นเข้า:** Geo Master (lookup) · F-INV ป้อน `hasStock` กลับมาล็อก uom/ลบ

---

## §2 Scenarios

- **S-01 Drill ตามชั้น (happy)** — root (WH list) → zone → area (tab Racks / Location ตรง) → rack → location · breadcrumb chip กลับชั้นไหนก็ได้ · stat 5 ใบ
- **S-02 Flat "Location ทั้งหมด"** — กด stat card Location → ตารางแบนทุกตำแหน่งข้ามคลัง/ชั้น + คอลัมน์ path ย่อ (WH-01 › Storage Zone › A-FM › R-A01) + ค้น/กรอง ประเภท/สถานะ — 1 คลิกถึงทุกตำแหน่ง (OB-10)
- **S-03 สร้าง/แก้ Warehouse** — form grid 2 คอลัมน์: [รหัส|ชื่อ] [ที่อยู่] [จังหวัด|อำเภอ] [ตำบล|ไปรษณีย์ auto] — cascade ถูกลำดับ, เปลี่ยนจังหวัดล้างลูก
- **S-04 สร้าง/แก้ Zone (temp) / Area (allows_direct) / Rack (R×C×L)** — form มาตรฐานเดียวกัน · Zone cold chain ใส่ช่วงอุณหภูมิ
- **S-05 สร้าง/แก้ Location (wizard 2 ขั้น)** — ขั้น 1: parent (Rack XOR Area-direct) + รหัส + ประเภท · ขั้น 2: **หน่วยเก็บสินค้า (บังคับ — ล็อกเมื่อมีสต็อก)** + ความจุ + หมุนเวียน (FIFO/FEFO/LIFO) + พิกัด R/C/L + behavior flags · รหัสซ้ำใน parent = block
- **S-06 Hierarchy view** — tree เต็มความสูงจอ scroll ภายใน (#96) + คลิก node → summary panel ขวา + เพิ่ม/แก้/ลบจาก summary ได้ · แชร์ state กับ List
- **S-07 เปลี่ยนสถานะเร็ว (statusMenu)** — คลิก pill สถานะ → เมนู 4 ค่า · เลือก blocked/frozen → modal บังคับเหตุผล → apply + audit + toast · full ไม่ให้ตั้งมือ (derived)
- **S-08 Bulk operations** — checkbox หลายแถว → bulk bar: เปลี่ยนสถานะ (blocked/frozen ใส่เหตุผลครั้งเดียวใช้ทั้งชุด) / **ตั้งหน่วยเก็บหลายช่อง — ข้ามตัว hasStock อัตโนมัติพร้อมนับแจ้ง** (คุม 1-loc-1-uom)
- **S-09 ลบ/ปิดใช้งาน (guard)** — location มีสต็อก → ลบ/deactivate ไม่ได้ · zone/area มีลูก active → block พร้อมชี้ทาง (OQ-LOC-04 default=block) · ลบ = confirm modal เสมอ
- **S-10 Bulk generation** — เลือก preset (Rack มาตรฐาน / Aisle-Bay-Level / ชั้นเรียบ) หรือกำหนดเอง → live preview ชื่อ 5 ตัวแรก + จำนวนรวม + หน่วยเก็บใช้กับทุกตัว → สร้าง atomic
- **S-11 Quick add** — แถวท้ายตาราง (rack + area direct): รหัส + ประเภท + หน่วยเก็บ → เพิ่มทันที (default ความจุ, แก้ทีหลัง) + กันซ้ำ
- **S-12 Audit** — ทุก create/update/สถานะ/bulk ลง audit ต่อ node (append-only) เปิดดูใน view drawer

## §3 Functions → `FUNCTION_CHECKLIST_F-LOC_Warehouse-Location.md`

## §4 Data
- **WAREHOUSES**: id, code, name, addr_line, province, district, subdistrict, postcode(auto), status
- **ZONES**: id, warehouse_id, code, name, temp_controlled + temp_min/max, status
- **AREAS**: id, zone_id, code, name, allows_direct_location, status
- **RACKS**: id, area_id, code, name, rows/cols/levels, status
- **LOCATIONS**: id, code (unique in parent), name?, parent_type ('rack'|'area'), rack_id XOR area_id, type (10 ค่า), **storage_uom** (STORAGE_UOMS — ตัว/ลัง/กล่อง/มัด/ถุง/ใบ/ขวด), cap_uom+cap_val, rotation, flags (pickable/putawayable/replenishable/mixed_lot/mixed_item/neg_stock), status (active/inactive/blocked/frozen; full=derived), block_reason, hasStock (จาก F-INV), row/col/level/position, barcode
- **AUDIT[node_id]**: append-only {t, by, at, v}

## §5 Coverage Matrix (เทสสะสม ~25 เคส PASS)

| Scenario | เทสแล้ว |
|---|---|
| S-01/S-02 | ✓ drill 5 ชั้น · flat-open/path-col/ph-count |
| S-03 | ✓ drawer-680 · form-2col · cascade (เดิม) · postcode ว่าง |
| S-05 | ✓ uom-field · uom-locked-hasStock · lock-msg |
| S-06 | ✓ tree full-height 850/1050 (600 = floor 420 ทั้งหน้า scroll) |
| S-07 | ✓ status-menu portal · reason-modal · blocked-applied |
| S-08 | ✓ bulk-bar · bulk-frozen (เหตุผลชุดเดียว) · bulk-uom + hasStock-guard |
| S-10 | ✓ preset · preview 5 ชื่อ · preset-applies |
| S-11 | ✓ qa-added · qa-dup-blocked · qa-in-rack |
| CI/icons | ✓ sprite 75 · audit navy=0/cdn=0/hint=0 · no-avatar · Rule #40/#51 |

## §6 Open Questions

| OQ | คำถาม | เจ้าภาพ |
|---|---|---|
| OQ-LOC-01 | Geo Master (77/928/7,255) เป็น feature แยก — timeline + endpoint contract | Strike + พี่เบิร์ด |
| OQ-LOC-02 | Hierarchy tree = NON-STANDARD layout — อนุมัติคงไว้หรือ List อย่างเดียว | Chin |
| OQ-LOC-03 | type-driven defaults (PACK ⇒ not pickable) — auto-set เฟสไหน | Strike |
| OQ-LOC-04 | Deactivate Zone/Area ที่มีลูก active → cascade หรือ block (ตอนนี้ block) | Strike |
| OQ-LOC-05 | Re-parent location: บังคับว่างก่อน หรือยอม live migration | Strike |
| OQ-LOC-06 | **ใครมีสิทธิ์เปลี่ยน storage_uom + เงื่อนไข** (ตอนนี้: แก้ได้เมื่อไม่มีสต็อก, ทุก role ที่แก้ master ได้) — โยง OQ-INV-03 | Strike |

**Engine candidates (แจ้ง Architect):** ENG-LOC-GEN · ENG-HIER-PATH (ประกาศใน FRD v2 แล้ว — ยังไม่ register)

## §7 Precedents
- 1-loc-1-uom (LOCK จาก F-INV) · statusMenu + bulk pattern (มติเลนใหม่ — ใช้ต่อกับ master ตัวอื่นได้) · #95 portal (statusMenu) · #96 full-height · #67.1 no-hint · Rule #40/#51 · append-only audit · soft-reference

## หนี้
- FRD FULL 9 ไฟล์ (Navy v5.1) **stale ทั้งชุด** — regen เมื่อ OQ เคาะ
- Delete/Decommission state machine เต็ม (ตาม FRD 03_LOGIC) ยังไม่ review ลึกรอบ vibe — เอาไว้ตรวจตอน regen FRD
