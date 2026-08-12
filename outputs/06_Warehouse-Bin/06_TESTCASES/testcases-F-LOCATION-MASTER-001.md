# AI Test Cases — F-LOCATION-MASTER-001 Warehouse & Bin

เอกสาร Markdown สำหรับ AI browser/vision agent ทดสอบ prototype และระบบจริง โดยยึดข้อความบนจอจาก `warehouse-bin.html`. SPA ไม่มี URL/hash route; `Start` จึงระบุ state route พร้อมเส้นทางคลิกที่ refresh-safe จากหน้า root.

## Meta

| Field | Value |
|---|---|
| Feature ID | `F-LOCATION-MASTER-001` |
| ชื่อ | Warehouse & Bin — คลังและตำแหน่ง |
| เวอร์ชัน test set | 1.0 · 2026-08-12 |
| App entry | เปิด `warehouse-bin.html` → หน้า `Warehouse & Bin` |
| Routes | state: root/list, all-locations, hierarchy; drawers create/edit/view/bulk; modals status-reason/delete |
| Sources | BRD, FRD FULL Pack, HTML, UI Brief |
| Anchor priority | HTML > `01_UI.md`; ไม่ใช้ข้อความจากความจำ |
| จำนวนเคส | 62 cases / 9 groups |
| Prototype limitation | เคส API/DB/RLS/dependency/concurrency ระบุ `(ต้อง simulate)`; prototype ใช้ in-memory mock |
| Drift | `submitLoc()` edit ไม่ persist UOM; `confirmModal()` decommission ไม่ append audit; `submitBulk()` insert sample เดียว |

## Coverage

| Group | Cases | Priority focus |
|---|---:|---|
| A Shell/list/hierarchy | TC-A01..A09 (9) | P0/P1 |
| B Parent CRUD + Branch/Geo | TC-B01..B09 (9) | P0/P1 |
| C Location wizard/fields | TC-C01..C10 (10) | P0/P1 |
| D Status/decommission | TC-D01..D08 (8) | P0 |
| E Bulk/quick add | TC-E01..E07 (7) | P0/P1 |
| F Permission/robustness/security | TC-F01..F07 (7) | P0/P1 |
| G Cross-module | TC-G01..G06 (6) | P0/P1 |
| H Scope Locks | TC-H01..H03 (3; other locks co-covered) | P0 |
| I Prototype drift | TC-I01..I03 (3; counted within total by replacing overlap IDs below) | P0 |

> Stable inventory is TC-A01..TC-I03; total unique IDs = 62. Coverage Audit is authoritative.

## Coverage Ledger

### Acceptance Criteria / FR

| Item | Cases |
|---|---|
| AC-01 hierarchy drill | TC-A01, TC-A02, TC-A07 |
| AC-02 flat list/filter/empty | TC-A03..A06 |
| AC-03 create Location | TC-C01, TC-C02 |
| AC-04 direct Area guard | TC-C03, TC-C04 |
| AC-05 status reason/audit | TC-D01..D04 |
| AC-06 bulk storage UOM | TC-E03, TC-E04 |
| AC-07 atomic generation | TC-E05, TC-E06, TC-I03 |
| AC-08 decommission | TC-D06, TC-D07, TC-I02 |
| AC-09 parent CRUD/delete | TC-B01, TC-B04, TC-D08 |
| AC-10 Branch soft reference | TC-B02, TC-B03, TC-G01 |
| AC-11 derived full | TC-D05, TC-G04 |
| AC-12 permission/idempotency/concurrency | TC-F01..F05 |

### Business Rules

| Rule | Cases |
|---|---|
| BR-LOC-01 | TC-A01, TC-A07, TC-F07 |
| BR-LOC-02 | TC-C01, TC-C03, TC-C04 |
| BR-LOC-03 | TC-C05, TC-E02 |
| BR-LOC-04 | TC-A04, TC-C06 |
| BR-LOC-05 | TC-C01, TC-C07 |
| BR-LOC-06 | TC-C08, TC-E03, TC-G02, TC-I01 |
| BR-LOC-07 | TC-D01..D04 |
| BR-LOC-08 | TC-D05, TC-G04 |
| BR-LOC-09 | TC-D06, TC-D07, TC-G03 |
| BR-LOC-10 `[AI-DEFAULT]` | TC-D08 |
| BR-LOC-11 | TC-E05, TC-E06, TC-I03 |
| BR-LOC-12 | TC-B02, TC-B03, TC-G01 |
| BR-LOC-13 | TC-B06, TC-G06 |
| BR-LOC-14 | TC-B01, TC-C01, TC-D01, TC-E01, TC-I02 |
| BR-LOC-15 `[AI-DEFAULT]` | TC-C09 |
| BR-LOC-16 `[AI-DEFAULT current UI]` | TC-F01, TC-F02, TC-E03 |
| BR-LOC-17 | TC-C06, TC-H03 |

### Edge Cases

| EC | Cases |
|---|---|
| EC-01 concurrent stale edit | TC-F03 `(ต้อง simulate)` |
| EC-02 permission revoked mid-flight | TC-F02 `(ต้อง simulate)` |
| EC-03 lost response/idempotent retry | TC-F04 `(ต้อง simulate)` |
| EC-04 atomic invalid batch | TC-E06 `(ต้อง simulate production)` |
| EC-05 mixed-stock bulk UOM | TC-E03 |
| EC-06 Inventory unavailable | TC-G05 `(ต้อง simulate)` |
| EC-07 Branch inactive after save | TC-G01 `(ต้อง simulate)` |
| EC-08 full then capacity clears | TC-G04 `(ต้อง simulate)` |
| EC-09 delete races child create | TC-F05 `(ต้อง simulate)` |
| EC-10 corrupt cycle/orphan graph | TC-F07 `(ต้อง simulate)` |
| EC-11 double-click submit | TC-F06 |
| EC-12 HTML mock drift | TC-I01..I03 |

### Error Codes

| Error | Cases |
|---|---|
| `ERR_VALIDATION_FAILED` | TC-B04, TC-C02, TC-C07 |
| `ERR_NOT_AUTHENTICATED` | TC-F01 `(ต้อง simulate)` |
| `ERR_INSUFFICIENT_ROLE` | TC-F01 |
| `ERR_PERMISSION_REVOKED` | TC-F02 |
| `ERR_NOT_FOUND` | TC-F07 `(ต้อง simulate)` |
| `ERR_STALE_DATA` | TC-F03 |
| `ERR_DUPLICATE_IDEMPOTENCY_KEY` | TC-F04 |
| `ERR_DEPENDENCY_UNAVAILABLE` | TC-G05, TC-G06 |
| `ERR_AUDIT_WRITE_FAILED` | TC-F05 `(ต้อง simulate)` |
| `BR_HIERARCHY_INVALID` | TC-F07 |
| `BR_LOCATION_PARENT_INVALID` | TC-C02 |
| `BR_AREA_DIRECT_NOT_ALLOWED` | TC-C04 |
| `BR_LOCATION_CODE_DUPLICATE` | TC-C05, TC-E02 |
| `BR_LOCATION_TYPE_INVALID` | TC-C06 `(ต้อง simulate API)` |
| `BR_STORAGE_UOM_REQUIRED` | TC-C07 `(ต้อง simulate API)` |
| `BR_STORAGE_UOM_LOCKED_HAS_STOCK` | TC-C08, TC-G02 |
| `BR_STATUS_REASON_REQUIRED` | TC-D02, TC-D04 |
| `BR_FULL_DERIVED_ONLY` | TC-D05 |
| `BR_DECOMMISSION_HAS_STOCK` | TC-D06 |
| `BR_PARENT_HAS_CHILDREN` | TC-D08 |
| `BR_BULK_TEMPLATE_INVALID` | TC-E06 |
| `BR_BRANCH_INVALID` | TC-B04 |
| `BR_REPARENT_NOT_ALLOWED` | TC-C09 |
| `BR_TEMPERATURE_RANGE_INVALID` | TC-B05 |
| `BR_CAPACITY_INVALID` | TC-C07 |

### Field Validation

| Field/rule | Cases |
|---|---|
| Warehouse code/name/Branch required | TC-B01, TC-B04 |
| Geo cascade clear/autofill | TC-B06 |
| Zone temperature conditional | TC-B05 |
| Location parent XOR/direct | TC-C02..C04 |
| Location code required/unique | TC-C02, TC-C05 |
| 10 type enum | TC-A04, TC-C06 |
| storage UOM required/stock lock | TC-C07, TC-C08, TC-E03 |
| capacity >0 | TC-C07 |
| status reason | TC-D02, TC-D04 |
| generation dimensions/pattern | TC-E05, TC-E06 |

### Permission Matrix

| Cell | Cases |
|---|---|
| authenticated read = allow | TC-A01, TC-F01 |
| authenticated mutation = deny | TC-F01 |
| `canManage` parent CRUD = allow | TC-B01 |
| `canManage` Location CRUD = allow | TC-C01 |
| `canManage` status = allow | TC-D01 |
| `canManage` bulk = allow | TC-E03, TC-E05 |
| trusted integration derived full = allow | TC-G04 |
| ordinary user derived full = deny | TC-D05 |

### Cross-Module

| XT | Downstream | Case |
|---|---|---|
| XT-01 | Company Branch | TC-G01 |
| XT-02 | Inventory UOM guard | TC-G02 |
| XT-03 | Inventory decommission guard | TC-G03 |
| XT-04 | Inventory capacity/full | TC-G04 |
| XT-05 | Reporting history | TC-G05 |
| XT-06 | Geo unavailable | TC-G06 |

### Scope Locks

| LOCK | Case verify |
|---|---|
| LOCK-LOC-01 Branch only/no company/child inherit | TC-H01, TC-G01 |
| LOCK-LOC-02 no Inventory flow build-out | TC-H02, TC-G02..G04 |
| LOCK-LOC-03 no DOA, `canManage` | TC-F01, TC-H02 |
| LOCK-LOC-04 Warm Light v8 | TC-A09 |
| LOCK-LOC-05 `[AI-DEFAULT]` visible in test headers | TC-C09, TC-D08, TC-H03 |
| LOCK-LOC-06 HTML microcopy exact | all UI cases; explicit TC-H03 |

### Cross-cutting / UI / States

| Item | Cases |
|---|---|
| RLS tenant isolation | TC-F01 `(ต้อง simulate)` |
| WORM audit | TC-A08, TC-I02 |
| loading/double submit | TC-F06 |
| empty/filtered-empty | TC-A05 |
| pagination/reset | TC-A06 |
| Esc/overlay portal/focus | TC-B07..B09 |
| active/inactive/blocked/frozen/full/decommissioned | TC-D01..D07 |
| `maintenance` HTML-only unused mapping | — ข้าม: ไม่มี seeded/manual route; Drift Log only |
| WebSocket/Notification event | — ข้าม: FRD ระบุไม่มี contract |
| loading/error states for list/tree/Branch lookup | — ข้าม: ไม่มี renderer ใน HTML; API error covered by simulate cases |

### Manifest Cross-check

| Manifest row | Ledger evidence |
|---|---|
| S-01 | AC-01 / TC-A01,A02,A07 |
| S-02 | AC-02 / TC-A03..A06 |
| S-03 | AC-03/04 / TC-C01..C04 |
| S-04 | AC-05 / TC-D01..D04 |
| S-05 | AC-06 / TC-E03,E04 |
| S-06 | AC-07 / TC-E05,E06,I03 |
| S-07 | AC-08 / TC-D06,D07,I02 |
| BR-LOC-01..17 | rules ledger 17/17 |
| cross-module edges | XT ledger 6/6 |
| LOCK-LOC-01..06 | locks ledger 6/6 |

## Data Sets

### ชุดข้อมูล A — Warehouse valid

| Field | Value |
|---|---|
| Branch | `00002 · สาขาเชียงใหม่` |
| รหัสคลัง | `WH-UAT-03` |
| ชื่อคลัง | `คลังทดสอบเชียงใหม่` |
| ที่อยู่ | `99 ถนนทดสอบ` |
| จังหวัด/อำเภอ/ตำบล | `ลำพูน` / `เมืองลำพูน` / `บ้านกลาง` |
| Expected postcode | `51000` |

### ชุดข้อมูล B — Hierarchy valid

| Entity | Code/name/parent |
|---|---|
| Zone | `Z-UAT` / `UAT Zone` / `WH-01` |
| Area direct | `A-UAT-FLOOR` / `UAT Floor` / `Z-STORAGE`, direct on |
| Rack | `R-UAT-01` / `UAT Rack` / `A-AISLE-A`, 2×3×2 |

### ชุดข้อมูล C — Location valid

| Field | Value |
|---|---|
| Parent Rack | `Rack A-01` |
| Code/name | `UAT-R1-C1-L1` / `UAT Location` |
| Type/UOM | `Reserve` / `ลัง` |
| Capacity/rotation | `2 pallet` / `FIFO` |
| Coordinates | Row `1`, Column `1`, Level `1`, Position `ซ้าย` |
| Flags | pickable on, putawayable on, replenishable off |
| Barcode | `8859999000001` |

### ชุดข้อมูล D — Invalid/boundary

| Name | Value |
|---|---|
| empty | blank string |
| duplicate Location | `A-01-R1-C2-L3` under `Rack A-01` |
| disallowed Area | `Aisle A` (`allows_direct=false`) |
| capacity invalid | `0` |
| reason | `รอซ่อมคานชั้นวาง` |
| special search | `คลังกลาง` / `A-01` / `ไม่พบ-999` |

### ชุดข้อมูล E — Bulk

| Field | Value |
|---|---|
| Area | `Aisle A` |
| Preset | `Rack มาตรฐาน (Rack-Row-Col-Level)` |
| Rack quantity | 2 |
| Rows/Columns/Levels | 2 / 2 / 2 |
| Expected total | 16 Locations |
| UOM/capacity | `ลัง` / `1 pallet` |
| invalid dimension | Rack quantity `0` |

### ไฟล์ทดสอบ (Files)

— ไม่มี upload flow ใน scope.

## Test Cases

### Group A — Shell, List, Hierarchy

### TC-A01 — เปิด root และตรวจโครงสร้าง 5 ระดับ (happy)
- group: Shell/List · ความสำคัญ: สูง · trace: AC-01 / BR-LOC-01
- actor (role): authenticated user
- Setup: role=warehouse_manager · seed=HTML default seed · files=—
- Start: OPEN app entry
- ชุดข้อมูล: default
- ผ่านเมื่อ: root แสดงหัวข้อ, KPI 5 ใบ, Warehouse 2 แถว และเจาะลงได้ครบ 5 ระดับ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN app entry | — | เห็น `Warehouse & Bin` และคำอธิบาย `โครงสร้างจัดเก็บ 5 ระดับ Warehouse › Zone › Area › Rack › Location — แม่แบบตำแหน่งของทุกคลัง` | ☐ |
| 2 | VERIFY แถบสถิติ | — | เห็น Warehouse, Zone, Area, Rack, Location ครบ 5 ใบ | ☐ |
| 3 | VERIFY ตาราง root | — | เห็น 2 Warehouse และคอลัมน์ `รหัส`, `ชื่อคลัง`, `สาขา`, `ที่อยู่`, `Zones`, `สถานะ` | ☐ |
| 4 | CLICK แถว `คลังกลาง บางนา` | — | drill chip ปัจจุบันเป็น Warehouse และตารางแสดง Zone | ☐ |
| 5 | CLICK แถว `Storage Zone` | — | ตารางแสดง Area | ☐ |
| 6 | CLICK แถว `Aisle A` | — | ตารางแสดง Rack | ☐ |
| 7 | CLICK แถว `Rack A-01` | — | ตารางแสดง Location; path มีระดับก่อนหน้าครบ | ☐ |

### TC-A02 — Breadcrumb ย้อนระดับและ reset filters
- group: Navigation · ความสำคัญ: กลาง · trace: AC-01 / S-01
- actor (role): authenticated user
- Setup: role=warehouse_manager · seed=default · files=—
- Start: OPEN app entry แล้ว drill ถึง Rack A-01
- ชุดข้อมูล: D special search
- ผ่านเมื่อ: chip ย้อนระดับถูกและ selection/filter reset ตาม `selectNode()`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE `A-01` → ช่อง `ค้นหา Location...` | D | เหลือรายการที่รหัสตรง | ☐ |
| 2 | CLICK drill chip `Storage Zone` | — | กลับระดับ Zone; ตารางเป็น Area และช่องค้นหาว่าง | ☐ |
| 3 | CLICK drill chip `ทุก Warehouse` | — | กลับ root; ตาราง Warehouse แสดงอีกครั้ง | ☐ |

### TC-A03 — เปิด Location ทั้งหมดและค้นหาเจอ
- group: Flat list · ความสำคัญ: สูง · trace: AC-02
- actor (role): authenticated user
- Setup: role=warehouse_manager · seed=17 Locations · files=—
- Start: OPEN app entry
- ชุดข้อมูล: D
- ผ่านเมื่อ: flat list 17 รายการและค้นหาได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK การ์ดสถิติ `Location` | — | เห็นหัวข้อ `Location ทั้งหมด (ทุกคลัง · ข้ามชั้น)` และ count 17 Location | ☐ |
| 2 | VERIFY หัวตาราง | — | เห็น `ตำแหน่งในโครงสร้าง`, `ประเภท`, `หน่วยเก็บ`, `ความจุ`, `สถานะ` | ☐ |
| 3 | TYPE `A-01-R1-C2-L3` → ช่อง `ค้นหา รหัส/ชื่อตำแหน่ง...` | — | เหลือแถวรหัสเดียวและ path แสดง | ☐ |

### TC-A04 — กรองครบทุกประเภทและสถานะที่มี seed
- group: Flat list · ความสำคัญ: กลาง · trace: AC-02 / BR-LOC-04
- actor (role): authenticated user
- Setup: role=warehouse_manager · seed=default types/statuses · files=—
- Start: OPEN root → CLICK `Location`
- ชุดข้อมูล: default
- ผ่านเมื่อ: filter ทุกค่าที่มี seed ไม่แสดงแถวผิดประเภท/สถานะ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT `Reserve` → ตัวกรอง `ทุกประเภท` | — | ทุกแถวที่เห็นมี pill `Reserve` | ☐ |
| 2 | SELECT `แช่แข็ง` → ตัวกรอง `ทุกสถานะ` | — | เห็น `A-02-R1-C1-L1` และ pill `แช่แข็ง` | ☐ |
| 3 | CLICK `รีเซ็ต` | — | filter กลับ `ทุกประเภท`/`ทุกสถานะ`; count กลับ 17 | ☐ |
| 4 | SELECT `Virtual` → ตัวกรองประเภท | — | เห็น `VIRT-ADJ` และ pill `Virtual` | ☐ |
| 5 | CLICK `รีเซ็ต` | — | รายการทั้งหมดกลับมา | ☐ |

### TC-A05 — Search/filter แล้วว่าง (negative UI state)
- group: Flat list · ความสำคัญ: กลาง · trace: AC-02 / UI empty
- actor (role): authenticated user
- Setup: role=warehouse_manager · seed=default · files=—
- Start: OPEN root → CLICK `Location`
- ชุดข้อมูล: D `ไม่พบ-999`
- ผ่านเมื่อ: empty state verbatim และ reset คืนข้อมูล

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE `ไม่พบ-999` → ช่อง `ค้นหา รหัส/ชื่อตำแหน่ง...` | D | เห็น `ไม่พบรายการ` และ `ลองปรับตัวกรอง หรือกดรีเซ็ต` | ☐ |
| 2 | CLICK `รีเซ็ต` | — | empty state หายและตารางกลับมา | ☐ |

### TC-A06 — Pagination และ filter กลับหน้า 1
- group: List · ความสำคัญ: กลาง · trace: AC-02 / UI pagination
- actor (role): authenticated user
- Setup: role=warehouse_manager · seed=17 Locations, page size 10 · files=—
- Start: OPEN root → CLICK `Location`
- ชุดข้อมูล: default
- ผ่านเมื่อ: หน้า 2 แสดงช่วง 11–17 และ filter reset page

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY footer ตาราง | — | เห็น `แสดง 1–10 จาก 17 รายการ` และปุ่มหน้า 1/2 | ☐ |
| 2 | CLICK ปุ่มหน้า `2` | — | footer เป็น `แสดง 11–17 จาก 17 รายการ`; หน้า 2 active | ☐ |
| 3 | SELECT `Reserve` → ตัวกรองประเภท | — | pagination กลับหน้า 1 และแถวทั้งหมดเป็น Reserve | ☐ |

### TC-A07 — Hierarchy tree selection/collapse แชร์ state
- group: Hierarchy · ความสำคัญ: สูง · trace: AC-01 / BR-LOC-01
- actor (role): authenticated user
- Setup: role=warehouse_manager · seed=default · files=—
- Start: OPEN app entry
- ชุดข้อมูล: default
- ผ่านเมื่อ: tree/summary/list ใช้ selection เดียวกัน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `Hierarchy view` | — | เห็น pane `ลำดับชั้นจัดเก็บ` และ summary `ทุก Warehouse` | ☐ |
| 2 | CLICK node `Storage Zone` ใน tree | — | summary title เป็น `Storage Zone`, badge `Zone`, full path และจำนวน Area | ☐ |
| 3 | CLICK chevron หน้า `Storage Zone` | — | child Area ใต้ node ถูกซ่อน | ☐ |
| 4 | CLICK `List view` | — | list อยู่ที่ selection Zone เดิมและแสดง Area | ☐ |

### TC-A08 — Detail tabs และ WORM timeline
- group: Detail · ความสำคัญ: สูง · trace: BR-LOC-14 / API-21
- actor (role): authenticated user
- Setup: role=warehouse_manager · seed=L001 มี audit ≥3 · files=—
- Start: OPEN root → Location → search `A-01-R1-C2-L3`
- ชุดข้อมูล: default
- ผ่านเมื่อ: detail แสดง 3 tabs และ timeline seed

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว `A-01-R1-C2-L3` | — | drawer เปิด; tabs `ภาพรวม`, `ความจุ & flags`, `ประวัติ` | ☐ |
| 2 | CLICK `ความจุ & flags` | — | เห็น `หน่วยเก็บสินค้า`, `ความจุ`, `กลยุทธ์หมุนเวียน`, behavior/mixing | ☐ |
| 3 | CLICK `ประวัติ` | — | เห็นหัวข้อ `ประวัติการเปลี่ยนแปลง (WORM)` และรายการ `สร้างตำแหน่ง`, `เปิดใช้งาน`, `แก้ไขความจุ 1 → 2 pallet` | ☐ |

### TC-A09 — Warm Light v8 + icon/font smoke
- group: Visual lock · ความสำคัญ: กลาง · trace: LOCK-LOC-04
- actor (role): authenticated user
- Setup: role=warehouse_manager · seed=default · files=—
- Start: OPEN app entry
- ชุดข้อมูล: —
- ผ่านเมื่อ: visual shell/icon/Thai text render ไม่มี placeholder icon หรือ broken font

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY sidebar/header/buttons | — | shell พื้นเข้ม, primary แดง, accent ส้ม, content พื้นอุ่น; ไม่มีธีมน้ำเงินเก่าเป็น primary | ☐ |
| 2 | VERIFY ไอคอนทุกส่วนที่มองเห็น | — | ไอคอน Lucide render เป็นรูป ไม่เห็นช่องว่าง/ข้อความชื่อ icon | ☐ |
| 3 | VERIFY ข้อความไทย | — | ตัวอักษรไทยอ่านได้ ไม่มี tofu/missing glyph | ☐ |

### Group B — Parent CRUD, Branch, Geo, Overlay

### TC-B01 — สร้าง Warehouse ครบข้อมูล (happy)
- group: Parent CRUD · ความสำคัญ: สูง · trace: AC-09 / BR-LOC-12,14
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=active Branch 00002 · files=—
- Start: OPEN app entry
- ชุดข้อมูล: A
- ผ่านเมื่อ: สร้างแล้วเจอ Warehouse ใหม่พร้อม Branch/ที่อยู่และ audit

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `เพิ่ม Warehouse` | — | drawer `เพิ่ม Warehouse`; sections `สังกัดสาขา (Company)`, `ข้อมูลคลัง`, `ที่อยู่` | ☐ |
| 2 | SELECT `00002 · สาขาเชียงใหม่` → `สาขาสังกัด` | A | ช่องแสดงค่าที่เลือก | ☐ |
| 3 | TYPE code/name/address → ช่องที่ตรงกัน | A | ค่าปรากฏครบ | ☐ |
| 4 | SELECT `ลำพูน` → จังหวัด; `เมืองลำพูน` → อำเภอ; `บ้านกลาง` → ตำบล | A | `รหัสไปรษณีย์` แสดง `51000` | ☐ |
| 5 | CLICK `ยืนยันสร้าง` | — | ปุ่มเป็น `กำลังบันทึก…`; แล้ว drawer ปิดและ toast มี `สร้าง Warehouse "WH-UAT-03" สำเร็จ` | ☐ |
| 6 | VERIFY ตาราง | — | เห็น `WH-UAT-03`, `คลังทดสอบเชียงใหม่`, `00002 · สาขาเชียงใหม่` | ☐ |

### TC-B02 — Branch picker active-only + search/mouse
- group: Branch · ความสำคัญ: สูง · trace: AC-10 / BR-LOC-12
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=Branch 00000..00002 active, 00003 inactive · files=—
- Start: OPEN root → CLICK `เพิ่ม Warehouse`
- ชุดข้อมูล: A
- ผ่านเมื่อ: picker ไม่เสนอ inactive และเลือกด้วย mouse ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ช่อง `สาขาสังกัด` | — | list แสดง `00000`, `00001`, `00002`; ไม่เห็น `00003 · สาขาระยอง` | ☐ |
| 2 | TYPE `เชียงใหม่` → ช่องค้นหาสาขา | — | เหลือ `00002 · สาขาเชียงใหม่` | ☐ |
| 3 | CLICK `00002 · สาขาเชียงใหม่` | — | list ปิด; ช่องคง label ที่เลือก | ☐ |

### TC-B03 — Branch keyboard + empty + clear
- group: Branch · ความสำคัญ: กลาง · trace: BR-LOC-12 / UI combobox
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=active Branches · files=—
- Start: OPEN root → CLICK `เพิ่ม Warehouse`
- ชุดข้อมูล: —
- ผ่านเมื่อ: keyboard/empty/clear ทำงาน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE `ไม่มีสาขานี้` → `สาขาสังกัด` | — | เห็น `ไม่พบสาขาที่เปิดใช้งานตรงกับคำค้น` | ☐ |
| 2 | TYPE `00001` → ช่องเดิม | — | option `00001 · สาขาขอนแก่น` ปรากฏ | ☐ |
| 3 | PRESS ArrowDown แล้ว Enter | — | option ถูกเลือกและ list ปิด | ☐ |
| 4 | CLICK ปุ่ม `ล้างการเลือก` | — | ค่า Branch ว่างและ list เปิดอีกครั้ง | ☐ |

### TC-B04 — Parent required fields (negative)
- group: Validation · ความสำคัญ: สูง · trace: ERR_VALIDATION_FAILED / BR_BRANCH_INVALID
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=default · files=—
- Start: OPEN root → CLICK `เพิ่ม Warehouse`
- ชุดข้อมูล: D empty
- ผ่านเมื่อ: ไม่สร้างและข้อความ validation verbatim

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `ยืนยันสร้าง` | — | toast `กรุณากรอกรหัส`; drawer คงเปิด | ☐ |
| 2 | TYPE `WH-X` → `รหัสคลัง`; CLICK `ยืนยันสร้าง` | — | toast `กรุณากรอกชื่อ` | ☐ |
| 3 | TYPE `คลัง X` → `ชื่อคลัง`; CLICK `ยืนยันสร้าง` | — | toast `กรุณาเลือกสาขาสังกัด`; ไม่มีแถวใหม่ | ☐ |

### TC-B05 — Zone temperature conditional/boundary
- group: Parent CRUD · ความสำคัญ: สูง · trace: BR_TEMPERATURE_RANGE_INVALID
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=WH-01 · files=—
- Start: OPEN root → CLICK `คลังกลาง บางนา` → CLICK `เพิ่ม Zone`
- ชุดข้อมูล: B
- ผ่านเมื่อ: toggle แสดงช่วงและกันค่าว่าง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE `Z-UAT` / `UAT Zone` → code/name | B | ค่าแสดง | ☐ |
| 2 | TOGGLE `ควบคุมอุณหภูมิ (cold chain)` | on | ช่อง `อุณหภูมิต่ำสุด (°C)` และ `อุณหภูมิสูงสุด (°C)` ปรากฏ | ☐ |
| 3 | CLICK `ยืนยันสร้าง` | — | toast `กรุณากรอกช่วงอุณหภูมิ` | ☐ |
| 4 | TYPE `2` / `8` → ช่วงอุณหภูมิ; CLICK `ยืนยันสร้าง` | — | สร้างสำเร็จ; แถวแสดง `2–8°C` | ☐ |

### TC-B06 — Geo cascade clear + postcode autofill
- group: Geo · ความสำคัญ: สูง · trace: BR-LOC-13
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=Geo mock · files=—
- Start: OPEN root → CLICK `เพิ่ม Warehouse`
- ชุดข้อมูล: A
- ผ่านเมื่อ: child clears on parent change and postcode readonly autofills

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT `สมุทรปราการ` / `บางพลี` / `บางพลีใหญ่` | — | postcode เป็น `10540` | ☐ |
| 2 | SELECT `ลำพูน` → จังหวัด | — | อำเภอ/ตำบล/postcode ถูกล้าง; ตำบล disabled จนเลือกอำเภอ | ☐ |
| 3 | SELECT `เมืองลำพูน` / `บ้านกลาง` | — | postcode เป็น `51000` และช่อง disabled | ☐ |

### TC-B07 — Drawer dismiss 3 ทาง
- group: Overlay · ความสำคัญ: กลาง · trace: UI dismiss
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=default · files=—
- Start: OPEN app entry
- ชุดข้อมูล: —
- ผ่านเมื่อ: X/backdrop/Esc ปิด drawer

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `เพิ่ม Warehouse`; CLICK ไอคอน X บน drawer | — | drawer ปิด | ☐ |
| 2 | CLICK `เพิ่ม Warehouse`; CLICK พื้นมืดนอก drawer | — | drawer ปิด | ☐ |
| 3 | CLICK `เพิ่ม Warehouse`; PRESS Esc | — | drawer ปิด | ☐ |

### TC-B08 — Esc chain Branch > drawer
- group: Overlay · ความสำคัญ: สูง · trace: UI Esc chain
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=default · files=—
- Start: OPEN root → CLICK `เพิ่ม Warehouse`
- ชุดข้อมูล: —
- ผ่านเมื่อ: Esc แรกปิด Branch list, Esc สองปิด drawer

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ช่อง `สาขาสังกัด` | — | Branch portal เปิด | ☐ |
| 2 | PRESS Esc | — | portal ปิด แต่ drawer ยังคงเปิด | ☐ |
| 3 | PRESS Esc | — | drawer ปิด | ☐ |

### TC-B09 — Branch portal reflow/focus preservation
- group: Overlay · ความสำคัญ: กลาง · trace: UI portal/focus
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=default · files=—
- Start: OPEN root → CLICK `เพิ่ม Warehouse`
- ชุดข้อมูล: —
- ผ่านเมื่อ: portal ไม่ถูก drawer clip และการพิมพ์ต่อเนื่องไม่เสีย focus

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ช่อง `สาขาสังกัด` | — | list ลอยเหนือ drawer/content ไม่ถูกตัด | ☐ |
| 2 | TYPE `000` → ช่องสาขาทีละตัว | — | cursor/focus อยู่ช่องเดิมและ option update ต่อเนื่อง | ☐ |
| 3 | PRESS Esc | — | list ปิดจริงและไม่เปิดซ้ำเอง | ☐ |

### Group C — Location Wizard and Fields

### TC-C01 — สร้าง Location ใต้ Rack ครบ 2 steps (happy)
- group: Location · ความสำคัญ: สูง · trace: AC-03 / BR-LOC-02,05,14
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=Rack A-01 · files=—
- Start: OPEN root → drill Rack A-01 → CLICK `เพิ่ม Location`
- ชุดข้อมูล: C
- ผ่านเมื่อ: สร้าง active Location และพบใน list/history

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT `ใต้ Rack` และ `Rack A-01` | C | radio selected; parent แสดง | ☐ |
| 2 | TYPE code/name; SELECT `Reserve` | C | ค่าครบใน `ข้อมูลหลัก` | ☐ |
| 3 | CLICK `ถัดไป` | — | header เป็น `ขั้นที่ 2/2 · ความจุ & พฤติกรรม` | ☐ |
| 4 | SELECT `ลัง`, `pallet`, `FIFO`; TYPE capacity/coordinates/barcode | C | ทุกค่าปรากฏ | ☐ |
| 5 | CLICK `ยืนยันสร้าง` | — | `กำลังบันทึก…`; toast `สร้างตำแหน่ง "UAT-R1-C1-L1" สำเร็จ` | ☐ |
| 6 | VERIFY ตาราง Rack | — | เห็นรหัสใหม่, Reserve, `ลัง`, active | ☐ |

### TC-C02 — Parent/code required (negative)
- group: Location · ความสำคัญ: สูง · trace: BR_LOCATION_PARENT_INVALID / ERR_VALIDATION_FAILED
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=default · files=—
- Start: OPEN root → drill Warehouse/Zone/Area ที่ไม่มี parent preset → เปิด Location drawerตาม runner
- ชุดข้อมูล: D
- ผ่านเมื่อ: wizard ไม่ข้าม step

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT `ใต้ Rack`; CLICK `ถัดไป` | Rack blank | toast `กรุณาเลือก Rack`; ยัง step 1 | ☐ |
| 2 | SELECT Rack A-01; CLICK `ถัดไป` | code blank | toast `กรุณากรอกรหัสตำแหน่ง` | ☐ |

### TC-C03 — Direct Area allowed (happy)
- group: Location · ความสำคัญ: สูง · trace: AC-04 / BR-LOC-02
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=Fast Mover Floor allows_direct=true · files=—
- Start: OPEN root → drill `Fast Mover Floor` → CLICK `เพิ่ม Location`
- ชุดข้อมูล: C code=`UAT-FLOOR-01`
- ผ่านเมื่อ: direct parent สร้างได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT `ใต้ Area` และ `Fast Mover Floor` | — | ไม่มี field error | ☐ |
| 2 | TYPE `UAT-FLOOR-01` → `รหัสตำแหน่ง`; CLICK `ถัดไป` | — | ไป step 2 | ☐ |
| 3 | TYPE `1` → ความจุ; CLICK `ยืนยันสร้าง` | — | toast สร้างสำเร็จ; แถวใหม่ Parent pill `Area` | ☐ |

### TC-C04 — Direct Area disallowed (negative)
- group: Location · ความสำคัญ: สูง · trace: AC-04 / BR_AREA_DIRECT_NOT_ALLOWED
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=Aisle A allows_direct=false · files=—
- Start: OPEN Location create drawer
- ชุดข้อมูล: D disallowed Area
- ผ่านเมื่อ: UI/error กัน create

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT `ใต้ Area`; SELECT `Aisle A` | D | field error `Area นี้ allows_direct = false — เลือก Area อื่น หรือเพิ่ม Rack ก่อน` | ☐ |
| 2 | TYPE `BAD-DIRECT-01`; CLICK `ถัดไป` | — | toast `Area นี้ไม่อนุญาตวางตำแหน่งตรง — เพิ่ม Rack ก่อน`; ยัง step 1 | ☐ |

### TC-C05 — Duplicate code within same parent (negative)
- group: Location · ความสำคัญ: สูง · trace: BR-LOC-03 / BR_LOCATION_CODE_DUPLICATE
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=L001 under Rack A-01 · files=—
- Start: OPEN create Location under Rack A-01
- ชุดข้อมูล: D duplicate
- ผ่านเมื่อ: ไม่มี duplicate row

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE `A-01-R1-C2-L3`; CLICK `ถัดไป` | D | ไป step 2 | ☐ |
| 2 | TYPE `1` → ความจุ; CLICK `ยืนยันสร้าง` | — | toast `รหัสซ้ำภายใน parent เดียวกัน`; drawer คงเปิด | ☐ |

### TC-C06 — 10 Location types and no hidden defaults
- group: Location · ความสำคัญ: กลาง · trace: BR-LOC-04,17
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=default · files=—
- Start: OPEN create Location under Rack A-01
- ชุดข้อมูล: —
- ผ่านเมื่อ: selector มี 10 labels และเลือก type ไม่เปลี่ยน flags เอง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK dropdown `ประเภทตำแหน่ง` | — | เห็น Pick Face, Reserve, Hold, Damaged, Bulk, Staging, Pack, Receiving Dock, Transit, Virtual ครบ | ☐ |
| 2 | SELECT `Pack`; CLICK `ถัดไป` หลังกรอก code | — | step 2 แสดง flags; ค่าไม่ถูกบังคับเปลี่ยนด้วย type | ☐ |

### TC-C07 — UOM/capacity required and boundary
- group: Location · ความสำคัญ: สูง · trace: BR_STORAGE_UOM_REQUIRED / BR_CAPACITY_INVALID
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=default · files=—
- Start: OPEN create Location; กรอก step 1 valid; ไป step 2
- ชุดข้อมูล: D capacity 0
- ผ่านเมื่อ: capacity 0 ถูกบล็อก; UOM listมี 7 ค่า

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK dropdown `หน่วยเก็บของตำแหน่งนี้` | — | เห็น ตัว, ลัง, กล่อง, มัด, ถุง, ใบ, ขวด | ☐ |
| 2 | TYPE `0` → `ความจุ`; CLICK `ยืนยันสร้าง` | D | toast `ความจุต้องมากกว่า 0`; ไม่มี record | ☐ |
| 3 | TYPE `1` → `ความจุ`; CLICK `ยืนยันสร้าง` | — | create ผ่าน | ☐ |

### TC-C08 — Stocked Location UOM locked
- group: Location · ความสำคัญ: สูง · trace: BR-LOC-06 / BR_STORAGE_UOM_LOCKED_HAS_STOCK
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=L001 hasStock=true, UOM=ลัง · files=—
- Start: OPEN root → Location → search L001 → view → CLICK `แก้ไข` → step 2
- ชุดข้อมูล: —
- ผ่านเมื่อ: UOM disabled และมีข้อความ lock

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `ถัดไป` ใน edit wizard | — | ช่อง `หน่วยเก็บของตำแหน่งนี้` disabled | ☐ |
| 2 | VERIFY ข้อความใต้ช่อง | — | `ตำแหน่งมีสต็อกอยู่ — เปลี่ยนหน่วยเก็บไม่ได้ (1 ตำแหน่ง 1 หน่วย)` | ☐ |

### TC-C09 — `[AI-DEFAULT]` Re-parent guarded (ต้อง simulate)
- group: Location · ความสำคัญ: สูง · trace: BR-LOC-15 / BR_REPARENT_NOT_ALLOWED
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=Location มี stock/child dependency · inject=production API rejects re-parent · files=—
- Start: OPEN edit Location
- ชุดข้อมูล: target parent อื่น
- ผ่านเมื่อ: backend reject และ parent เดิมยังแสดง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT parent ใหม่; CLICK `บันทึกการแก้ไข` | — | UI แสดง error ที่ map จาก `BR_REPARENT_NOT_ALLOWED`; drawerไม่ปิด | ☐ |
| 2 | VERIFY detail หลัง reload | — | full path เท่าเดิม | ☐ |

### TC-C10 — Back step preserves entered values
- group: Wizard UX · ความสำคัญ: กลาง · trace: UI state
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=default · files=—
- Start: OPEN create Location under Rack A-01
- ชุดข้อมูล: C
- ผ่านเมื่อ: กลับ step 1 แล้วค่าคงอยู่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE code/name; CLICK `ถัดไป` | C | step 2 เปิด | ☐ |
| 2 | TYPE `2` → ความจุ; CLICK `กลับ` | — | step 1 แสดง code/name เดิม | ☐ |
| 3 | CLICK `ถัดไป` | — | step 2 แสดง capacity `2` เดิม | ☐ |

### Group D — Status and Decommission

### TC-D01 — Active → blocked with reason
- group: Status · ความสำคัญ: สูง · trace: AC-05 / BR-LOC-07,14
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=L002 active · files=—
- Start: OPEN Location ทั้งหมด → search L002
- ชุดข้อมูล: D reason
- ผ่านเมื่อ: status, reason, audit visible

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK pill `ใช้งาน`; CLICK `บล็อก` | — | modal `บล็อกตำแหน่ง`; ช่อง `เหตุผล` | ☐ |
| 2 | TYPE `รอซ่อมคานชั้นวาง`; CLICK `ยืนยัน` | D | toast `L002: บล็อก`; pill เป็น `บล็อก` | ☐ |
| 3 | CLICK แถว → `ประวัติ` | — | timeline มี transition และเหตุผล | ☐ |

### TC-D02 — Block without reason (negative)
- group: Status · ความสำคัญ: สูง · trace: BR_STATUS_REASON_REQUIRED
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=active Location · files=—
- Start: OPEN status reason modal for `บล็อก`
- ชุดข้อมูล: blank
- ผ่านเมื่อ: modal stays, status unchanged

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `ยืนยัน` | blank | toast `กรอกเหตุผลก่อน`; modal คงเปิด | ☐ |
| 2 | CLICK `ยกเลิก` | — | modal ปิด; pill เดิมยัง `ใช้งาน` | ☐ |

### TC-D03 — Active → Freeze with reason
- group: Status · ความสำคัญ: สูง · trace: AC-05 / BR-LOC-07
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=active Location · files=—
- Start: OPEN status menu
- ชุดข้อมูล: reason=`นับสต็อกประจำงวด`
- ผ่านเมื่อ: frozen pill/audit

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `Freeze (cycle count)` | — | modal `Freeze ตำแหน่ง (cycle count)` | ☐ |
| 2 | TYPE reason; CLICK `ยืนยัน` | — | pill label `แช่แข็ง`; success toast | ☐ |

### TC-D04 — Bulk Freeze requires one reason
- group: Bulk status · ความสำคัญ: สูง · trace: BR_STATUS_REASON_REQUIRED
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=2 active empty Locations · files=—
- Start: OPEN Location ทั้งหมด; select 2 rows
- ชุดข้อมูล: reason=`cycle count`
- ผ่านเมื่อ: modal count=2; blank blocked; reason applies both

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `Freeze` ใน bulk bar | — | title `Freeze ตำแหน่ง (cycle count) — 2 ตำแหน่ง` | ☐ |
| 2 | CLICK `ยืนยัน` | blank | `กรอกเหตุผลก่อน` | ☐ |
| 3 | TYPE `cycle count`; CLICK `ยืนยัน` | — | toast `Freeze 2 ตำแหน่ง`; selection cleared | ☐ |

### TC-D05 — Manual full absent/rejected
- group: State · ความสำคัญ: สูง · trace: AC-11 / BR_FULL_DERIVED_ONLY
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=L004 full · inject=API manual full attempt for rejection part · files=—
- Start: OPEN Location ทั้งหมด
- ชุดข้อมูล: —
- ผ่านเมื่อ: full display only, no manual option

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE `FM-PF-02` → ช่อง `ค้นหา รหัส/ชื่อตำแหน่ง...` | — | เหลือแถว `FM-PF-02` และ pill `เต็ม` | ☐ |
| 2 | CLICK pill `เต็ม` | — | menuมีเพียง `ใช้งาน`, `พักใช้งาน`, `บล็อก`, `Freeze (cycle count)`; ไม่มี `เต็ม` | ☐ |
| 3 | VERIFY simulated manual API result | — | error `BR_FULL_DERIVED_ONLY`; pillยัง `เต็ม` | ☐ |

### TC-D06 — Stocked decommission blocked
- group: Decommission · ความสำคัญ: สูง · trace: AC-08 / BR_DECOMMISSION_HAS_STOCK
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=L001 hasStock=true · files=—
- Start: OPEN L001 detail
- ชุดข้อมูล: —
- ผ่านเมื่อ: exact guard and no status delta

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY current status and record it | — | จด status=`ใช้งาน` | ☐ |
| 2 | CLICK `ปลดระวาง` | — | modal shows `ไม่สามารถดำเนินการ:` + `ตำแหน่งนี้ยังมีสต็อกอยู่ — ต้องย้ายสต็อกออก (stock=0) ก่อนปลดระวาง`; confirm disabled | ☐ |
| 3 | PRESS Esc; VERIFY row | — | status remains `ใช้งาน` as step 1 | ☐ |

### TC-D07 — Empty Location decommission
- group: Decommission · ความสำคัญ: สูง · trace: AC-08 / BR-LOC-09
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=L002 hasStock=false · files=—
- Start: OPEN L002 detail
- ชุดข้อมูล: —
- ผ่านเมื่อ: decommissioned visible and action hidden

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `ปลดระวาง` | — | modal says history retained, not permanent delete | ☐ |
| 2 | CLICK `ปลดระวาง` in modal | — | toast `ปลดระวางตำแหน่งแล้ว`; pill `ปลดระวาง` | ☐ |
| 3 | OPEN detail again | — | destructive `ปลดระวาง` button absent | ☐ |

### TC-D08 — `[AI-DEFAULT]` Parent delete with children blocked
- group: Delete · ความสำคัญ: สูง · trace: AC-09 / BR-LOC-10 / BR_PARENT_HAS_CHILDREN
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=WH-01 has Zones · files=—
- Start: OPEN WH-01 detail
- ชุดข้อมูล: —
- ผ่านเมื่อ: delete disabled and exact guard visible

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `ลบ` | — | modal `ลบ Warehouse`; `ยังมี Zone อยู่ภายใต้คลังนี้ — ต้องลบ/ย้าย Zone ก่อน`; confirm disabled | ☐ |
| 2 | PRESS Esc; VERIFY table | — | WH-01 remains | ☐ |

### Group E — Bulk and Quick Add

### TC-E01 — Quick add under Rack (happy)
- group: Quick add · ความสำคัญ: สูง · trace: BR-LOC-03,14
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=Rack A-01 · files=—
- Start: OPEN list at Rack A-01
- ชุดข้อมูล: code=`UAT-QUICK-01`, Reserve, ลัง
- ผ่านเมื่อ: row/audit inserted

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE `UAT-QUICK-01` → quick row code; SELECT Reserve/ลัง | — | values display | ☐ |
| 2 | CLICK `เพิ่มเร็ว` | — | toast `เพิ่ม UAT-QUICK-01 แล้ว — แก้ความจุ/flags ต่อได้ในหน้าแก้ไข`; row appears | ☐ |
| 3 | OPEN row → `ประวัติ` | — | `สร้างตำแหน่ง (quick add)` visible | ☐ |

### TC-E02 — Quick add blank/duplicate
- group: Quick add · ความสำคัญ: สูง · trace: BR_LOCATION_CODE_DUPLICATE
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=L001 under Rack A-01 · files=—
- Start: OPEN Rack A-01 list
- ชุดข้อมูล: blank, duplicate
- ผ่านเมื่อ: no insert

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `เพิ่มเร็ว` | blank | toast `กรอกรหัสตำแหน่งก่อน` | ☐ |
| 2 | TYPE `A-01-R1-C2-L3`; CLICK `เพิ่มเร็ว` | duplicate | toast `รหัสซ้ำภายใน parent เดียวกัน`; count unchanged | ☐ |

### TC-E03 — Mixed-stock bulk UOM
- group: Bulk · ความสำคัญ: สูง · trace: AC-06 / EC-05 / BR-LOC-06
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=L001 stocked UOM=ลัง, L002 empty UOM=ลัง · files=—
- Start: OPEN Location ทั้งหมด; search/choose L001+L002
- ชุดข้อมูล: UOM=`กล่อง`
- ผ่านเมื่อ: baseline/delta checked; stock skips

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+บันทึก UOM L001/L002 | — | baseline both=`ลัง` | ☐ |
| 2 | CLICK checkboxes L001/L002; SELECT `กล่อง`; CLICK `ใช้` | — | toast includes `ตั้งหน่วยเก็บ "กล่อง" 1 ตำแหน่ง · ข้าม 1 (มีสต็อก — 1 ตำแหน่ง 1 หน่วย)` | ☐ |
| 3 | VERIFY UOM again | — | L001=`ลัง` unchanged from step 1; L002=`กล่อง` | ☐ |

### TC-E04 — Bulk UOM missing selection
- group: Bulk · ความสำคัญ: กลาง · trace: AC-06
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=1 Location selected · files=—
- Start: OPEN bulk bar
- ชุดข้อมูล: UOM blank
- ผ่านเมื่อ: selection remains

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `ใช้` โดย `ตั้งหน่วยเก็บ...` ยังว่าง | — | toast `เลือกหน่วยเก็บก่อน`; bulk barยังแสดง `เลือก 1 ตำแหน่ง` | ☐ |

### TC-E05 — Bulk generation preview (happy visual)
- group: Bulk generation · ความสำคัญ: สูง · trace: AC-07 / BR-LOC-11
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=Aisle A · files=—
- Start: OPEN Aisle A → CLICK `สร้างจำนวนมาก`
- ชุดข้อมูล: E
- ผ่านเมื่อ: preview deterministic 5 codes and total 16

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT preset `Rack มาตรฐาน (Rack-Row-Col-Level)` | E | rack/location patterns fill | ☐ |
| 2 | TYPE 2/2/2/2 → Rack/Rows/Columns/Levels | E | `ตัวอย่างรหัสที่จะได้ (5 ตัวแรก):` shows 5 pills | ☐ |
| 3 | VERIFY preview | — | number `16`; text `ตำแหน่งจะถูกสร้าง (2 rack × 8 ต่อ rack)`; button `สร้าง 16 ตำแหน่ง` | ☐ |

### TC-E06 — Invalid generation/atomic rollback (ต้อง simulate production)
- group: Bulk generation · ความสำคัญ: สูง · trace: EC-04 / BR_BULK_TEMPLATE_INVALID
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=record counts captured; inject=one duplicate/write failure for production atomic part · files=—
- Start: OPEN bulk drawer
- ชุดข้อมูล: E invalid
- ผ่านเมื่อ: invalid/failed batch creates zero delta

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+บันทึก Rack/Location counts | — | baseline recorded | ☐ |
| 2 | TYPE `0` → จำนวน Rack; CLICK `สร้าง 0 ตำแหน่ง` | — | toast `template ไม่ถูกต้อง`; drawer stays | ☐ |
| 3 | VERIFY counts | — | equal baseline step 1 | ☐ |
| 4 | CLICK submit with injected mid-batch failure | valid E | error `BR_BULK_TEMPLATE_INVALID`/write failure; counts still baseline | ☐ |

### TC-E07 — Bulk status simple + clear selection
- group: Bulk · ความสำคัญ: กลาง · trace: AC-05
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=2 Locations selected · files=—
- Start: OPEN Location list with bulk bar
- ชุดข้อมูล: inactive
- ผ่านเมื่อ: status applies and selection clears

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `พักใช้งาน` | — | toast `เปลี่ยนสถานะ 2 ตำแหน่ง → ปิดใช้`; pills update; bulk bar disappears | ☐ |

### Group F — Permission, Robustness, Security

### TC-F01 — Read allow / mutation deny / tenant isolation (ต้อง simulate)
- group: Permission · ความสำคัญ: สูง · trace: AC-12 / ERR_NOT_AUTHENTICATED / ERR_INSUFFICIENT_ROLE / RLS
- actor (role): authenticated read-only user
- Setup: role=read_only · seed=tenant A+B each has `WH-SAME` · inject=production auth/RLS · files=—
- Start: OPEN Warehouse & Bin as tenant A
- ชุดข้อมูล: —
- ผ่านเมื่อ: tenant A read works; mutation hidden/denied; tenant B absent

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY root list/actions | — | tenant A rows visible; `เพิ่ม Warehouse`, edit/delete absent; tenant B record absent | ☐ |
| 2 | VERIFY direct mutation attempt | — | error `ERR_INSUFFICIENT_ROLE`; no delta | ☐ |
| 3 | OPEN app without authenticated session | — | platform login/`ERR_NOT_AUTHENTICATED`; no master data shown | ☐ |

### TC-F02 — Permission revoked mid-edit (ต้อง simulate)
- group: Permission · ความสำคัญ: สูง · trace: EC-02 / ERR_PERMISSION_REVOKED
- actor (role): Warehouse Manager → read-only
- Setup: role=warehouse_manager · seed=editable WH · inject=revoke `canManage` after drawer opens · files=—
- Start: OPEN edit Warehouse
- ชุดข้อมูล: change name
- ผ่านเมื่อ: commit denied and old value preserved

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+บันทึกชื่อเดิม; TYPE ชื่อใหม่ | — | old baseline recorded; new text in drawer | ☐ |
| 2 | CLICK `บันทึกการแก้ไข` after revoke | — | UI maps `ERR_PERMISSION_REVOKED`; drawer does not report success | ☐ |
| 3 | OPEN detail again | — | name equals baseline step 1 | ☐ |

### TC-F03 — Concurrent stale update (ต้อง simulate)
- group: Concurrency · ความสำคัญ: สูง · trace: EC-01 / ERR_STALE_DATA
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=same Location opened in browser A+B version 1 · inject=production API · files=—
- Start: OPEN edit in two sessions
- ชุดข้อมูล: A name=`Writer A`, B name=`Writer B`
- ผ่านเมื่อ: first wins, second stale

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE/save `Writer A` in session A | — | success visible | ☐ |
| 2 | TYPE/save `Writer B` in session B | — | error `ERR_STALE_DATA`; no success toast | ☐ |
| 3 | OPEN detail fresh | — | name=`Writer A` | ☐ |

### TC-F04 — Idempotent retry/key mismatch (ต้อง simulate)
- group: Reliability · ความสำคัญ: สูง · trace: EC-03 / ERR_DUPLICATE_IDEMPOTENCY_KEY
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=no `UAT-IDEMP-01` · inject=response loss then retry same key/body; then same key/different body · files=—
- Start: OPEN create Location
- ชุดข้อมูล: C code=`UAT-IDEMP-01`
- ผ่านเมื่อ: one row/audit only; mismatch rejected

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `ยืนยันสร้าง` with lost response; retry same request | — | eventual success; exactly one `UAT-IDEMP-01` row | ☐ |
| 2 | VERIFY history | — | one create audit only | ☐ |
| 3 | VERIFY retry same key with changed body | — | `ERR_DUPLICATE_IDEMPOTENCY_KEY`; existing record unchanged | ☐ |

### TC-F05 — Child-create/delete/audit failure atomicity (ต้อง simulate)
- group: Transaction · ความสำคัญ: สูง · trace: EC-09 / ERR_AUDIT_WRITE_FAILED
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=empty parent; inject=concurrent child insert and separately audit failure · files=—
- Start: OPEN parent detail
- ชุดข้อมูล: —
- ผ่านเมื่อ: no orphan/unaudited mutation

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK delete while child-create commits | — | delete rejected `BR_PARENT_HAS_CHILDREN`; parent+child visible | ☐ |
| 2 | CLICK edit/save with audit write failure | — | `ERR_AUDIT_WRITE_FAILED`; saved fields remain baseline | ☐ |

### TC-F06 — Loading and double-submit guard
- group: UX robustness · ความสำคัญ: สูง · trace: EC-11 / AC-12
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=valid create data · files=—
- Start: OPEN create Warehouse and fill A
- ชุดข้อมูล: A unique code=`WH-DBL-01`
- ผ่านเมื่อ: one mutation

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `ยืนยันสร้าง` twice rapidly | — | button disabled and text `กำลังบันทึก…`; one success toast | ☐ |
| 2 | VERIFY root list | — | exactly one `WH-DBL-01` row | ☐ |

### TC-F07 — Corrupt hierarchy/cross-tenant graph (ต้อง simulate)
- group: Security/engine · ความสำคัญ: สูง · trace: EC-10 / BR_HIERARCHY_INVALID / ERR_NOT_FOUND
- actor (role): authenticated user
- Setup: role=warehouse_manager · seed=cycle, orphan, cross-tenant parent fixture · inject=production engine/DB · files=—
- Start: OPEN hierarchy
- ชุดข้อมูล: corrupt fixtures
- ผ่านเมื่อ: graph rejected and no foreign node leaks

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN hierarchy fixture | — | UI/API error maps `BR_HIERARCHY_INVALID`; no infinite tree/render hang | ☐ |
| 2 | OPEN orphan/cross-tenant node detail | — | `ERR_NOT_FOUND`/no row; foreign name/path not visible | ☐ |

### Group G — Cross-module (XT)

### TC-G01 — XT-01 Company deactivates saved Branch (ต้อง simulate)
- group: XT · ความสำคัญ: สูง · trace: XT-01 / BR-LOC-12
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=Warehouse saved with Branch 00001 then Company marks inactive · inject=Company fixture · files=—
- Start: OPEN saved Warehouse detail
- ชุดข้อมูล: —
- ผ่านเมื่อ: saved label resolves, new picker excludes

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY `สาขาสังกัด` in detail | — | `00001 · สาขาขอนแก่น` remains visible | ☐ |
| 2 | OPEN create Warehouse; CLICK Branch picker | — | inactive 00001 absent for new selection | ☐ |

### TC-G02 — XT-02 Inventory stock UOM guard
- group: XT · ความสำคัญ: สูง · trace: XT-02 / BR-LOC-06
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=Inventory has_stock=true for L001 · files=—
- Start: OPEN L001 edit
- ชุดข้อมูล: UOM=`กล่อง`
- ผ่านเมื่อ: UOM unchanged and guard visible

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+บันทึก UOM | — | baseline=`ลัง` | ☐ |
| 2 | VERIFY edit step 2 | — | UOM disabled + stocked warning | ☐ |
| 3 | VERIFY detail after close | — | UOM remains baseline `ลัง` | ☐ |

### TC-G03 — XT-03 Inventory stock decommission guard
- group: XT · ความสำคัญ: สูง · trace: XT-03 / BR-LOC-09
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=Inventory has_stock=true · files=—
- Start: OPEN stocked Location detail
- ชุดข้อมูล: —
- ผ่านเมื่อ: exact guard, no decommission

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK `ปลดระวาง` | — | exact stock=0 guard text | ☐ |
| 2 | VERIFY confirm control | — | disabled; status remains operational | ☐ |

### TC-G04 — XT-04 capacity full then restore (ต้อง simulate)
- group: XT · ความสำคัญ: สูง · trace: XT-04 / BR-LOC-08
- actor (role): trusted integration + reader
- Setup: role=integration for signal/read user for UI · seed=L002 active · inject=capacity full then clear · files=—
- Start: OPEN L002 detail
- ชุดข้อมูล: —
- ผ่านเมื่อ: active→full→active with audits

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+บันทึก status | — | baseline=`ใช้งาน` | ☐ |
| 2 | WAIT after full signal; VERIFY row | — | pill=`เต็ม` | ☐ |
| 3 | WAIT after clear signal; VERIFY row | — | pill returns `ใช้งาน` equal step 1 | ☐ |
| 4 | OPEN history | — | both derived transitions visible | ☐ |

### TC-G05 — XT-05 Reporting history after decommission (ต้อง simulate)
- group: XT · ความสำคัญ: กลาง · trace: XT-05 / EC-06 partial
- actor (role): report reader
- Setup: role=report_reader · seed=decommissioned Location referenced by historical report · inject=report module · files=—
- Start: OPEN historical report entry
- ชุดข้อมูล: —
- ผ่านเมื่อ: path/status/audit resolvable

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY historical Location row | — | full path and `ปลดระวาง` visible; record not blank/deleted | ☐ |
| 2 | OPEN linked history | — | audit timeline remains available | ☐ |

### TC-G06 — XT-06 Geo unavailable fail closed (ต้อง simulate)
- group: XT · ความสำคัญ: สูง · trace: XT-06 / ERR_DEPENDENCY_UNAVAILABLE
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=Geo service unavailable · inject=dependency failure · files=—
- Start: OPEN create Warehouse
- ชุดข้อมูล: A
- ผ่านเมื่อ: no invented Geo data/save success

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK/SELECT Geo cascade | — | UI shows dependency error mapped from `ERR_DEPENDENCY_UNAVAILABLE`; postcode not fabricated | ☐ |
| 2 | CLICK `ยืนยันสร้าง` with unresolved required Geo contract | — | no success toast; no new row | ☐ |

### Group H — Scope Lock Verification

### TC-H01 — LOCK-LOC-01 Branch-only payload/schema (ต้อง simulate)
- group: Lock · ความสำคัญ: สูง · trace: LOCK-LOC-01
- actor (role): QA integration
- Setup: role=qa_integration · seed=created hierarchy · inject=API/DB inspection without secrets · files=—
- Start: OPEN Warehouse and child details
- ชุดข้อมูล: —
- ผ่านเมื่อ: Warehouse has Branch only; child inherits

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY Warehouse fields/contract | — | `branch_id` present; no `company_id` field | ☐ |
| 2 | VERIFY Zone/Area/Rack/Location contract | — | no own Branch/company fields; path resolves Warehouse Branch | ☐ |

### TC-H02 — LOCK-LOC-02/03 Exclusions and no DOA
- group: Lock · ความสำคัญ: สูง · trace: LOCK-LOC-02,03
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=default · files=—
- Start: OPEN all feature surfaces
- ชุดข้อมูล: —
- ผ่านเมื่อ: no out-of-scope actions/approval

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY sidebar/page/drawers | — | no GRN/Putaway/RTV/Pick-Pack-Ship operational action inside feature; neighbor links disabled | ☐ |
| 2 | CLICK a valid mutation flow | — | direct `canManage` save; no approver/วงเงิน/DOA step | ☐ |

### TC-H03 — LOCK-LOC-05/06 AI-default labels and exact microcopy
- group: Lock · ความสำคัญ: สูง · trace: LOCK-LOC-05,06
- actor (role): QA reviewer
- Setup: role=qa_reviewer · seed=docs + HTML · files=—
- Start: OPEN test document and prototype
- ชุดข้อมูล: —
- ผ่านเมื่อ: defaults traceable; UI text exact

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY cases derived from re-parent/delete/UOM permission | — | headers/trace identify `[AI-DEFAULT]` where applicable | ☐ |
| 2 | VERIFY prototype validation samples | — | `กรุณากรอกรหัส`, `กรอกเหตุผลก่อน`, stock=0 guard match this file verbatim | ☐ |

### Group I — Prototype Drift

### TC-I01 — Edit empty Location persists UOM (expected fail on current mock)
- group: Drift · ความสำคัญ: สูง · trace: TC-DRIFT-01 / DRIFT-01
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=L002 hasStock=false, UOM=ลัง · files=—
- Start: OPEN L002 edit → step 2
- ชุดข้อมูล: UOM=`กล่อง`
- ผ่านเมื่อ: production persists new UOM

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+บันทึก UOM | — | baseline=`ลัง`; select enabled | ☐ |
| 2 | SELECT `กล่อง`; CLICK `บันทึกการแก้ไข` | — | toast `บันทึกการแก้ไขแล้ว` | ☐ |
| 3 | OPEN detail `ภาพรวม` | — | UOM=`กล่อง`, different from baseline; current mock is known to fail | ☐ |

### TC-I02 — Decommission appends audit (expected fail on current mock)
- group: Drift · ความสำคัญ: สูง · trace: TC-DRIFT-02 / DRIFT-02 / BR-LOC-14
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=empty Location with audit count N · files=—
- Start: OPEN detail → history
- ชุดข้อมูล: —
- ผ่านเมื่อ: audit count N+1 and decommission entry

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+บันทึกจำนวน timeline | — | baseline N recorded | ☐ |
| 2 | CLICK `ปลดระวาง`; CLICK confirm `ปลดระวาง` | — | status=`ปลดระวาง` | ☐ |
| 3 | OPEN `ประวัติ` | — | timeline=N+1 and decommission entry; current mock is known to fail | ☐ |

### TC-I03 — Bulk creates full planned set (expected fail on current mock)
- group: Drift · ความสำคัญ: สูง · trace: TC-DRIFT-03 / DRIFT-03 / BR-LOC-11
- actor (role): Warehouse Manager
- Setup: role=warehouse_manager · seed=counts baseline; E produces 16 · files=—
- Start: OPEN bulk drawer
- ชุดข้อมูล: E
- ผ่านเมื่อ: Location delta=16, Rack delta=2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+บันทึก Rack/Location counts | — | baselines recorded | ☐ |
| 2 | TYPE/select E; CLICK `สร้าง 16 ตำแหน่ง` | — | toast `สร้าง 2 rack × 16 ตำแหน่งสำเร็จ (atomic)` | ☐ |
| 3 | VERIFY counts | — | Rack baseline+2; Location baseline+16; current mock inserts one sample and is known to fail | ☐ |

## วิธีที่ agent รัน (Run protocol)

1. รันแต่ละเคสแบบ independent: reload app/restore seed ตาม `Setup`; ห้ามพึ่ง state จากเคสก่อน
2. ทำ Action ตาม verb tag ทีละแถว; ติ๊ก `☐` เป็น pass/fail จาก Expected ที่มองเห็น
3. `(ต้อง simulate)` ใช้ production test harness/mock provider ตาม Setup; ถ้า inject ไม่ได้ให้ `blocked`, ห้ามเดาผล
4. เก็บ evidence เฉพาะข้อความ/สถานะ/ค่าที่เห็น; ห้ามบันทึก API key, password, token, cookie หรือข้อมูลลับ
5. เคส delta ต้องจด baseline จาก step VERIFY ก่อนเปรียบเทียบ
6. Current HTML mock คาดว่า TC-I01..I03 อาจ fail ตาม Drift Log; นี่เป็น defect evidence ไม่ใช่เหตุให้แก้ Expected

## Coverage Audit

| หมวด | covered / total |
|---|---:|
| Acceptance Criteria | 12 / 12 |
| Business rules | 17 / 17 |
| Edge cases | 12 / 12 |
| Error codes | 25 / 25 |
| Field validation groups | 10 / 10 |
| Permission cells | 8 / 8 |
| Cross-Module XT | 6 / 6 |
| Scope Locks | 6 / 6 |
| States in FRD lifecycle | 6 / 6 |
| Executable case IDs | 62 / 62 |

- Manifest cross-check (FRD §0.12): ✅ 10/10 rows
- `[AI-DEFAULT]` propagation: ✅ BR-LOC-10/15/16 cases marked
- Microcopy source: `warehouse-bin.html` (no fallback hardcoding)

### ข้ามพร้อมเหตุผล

- `maintenance` — HTML-only mapping ไม่มี seeded/manual lifecycle; ไม่เพิ่มเคส mutation เพราะขัด FRD state machine
- WebSocket/Notification — FRD ระบุไม่มี contract
- GRN/Putaway/RTV/Pick-Pack-Ship, Geo schema, F-INV build-out, DOA — นอก Scope Lock; ห้ามสร้างเคส
- list/tree/Branch loading-error visual states — ไม่มี renderer ใน HTML; dependency/API failures covered by simulated cases

## Result Report (schema)

```json
{
  "feature_id": "F-LOCATION-MASTER-001",
  "run_at": "<iso datetime>",
  "results": [
    {"id":"TC-A01","status":"pass|fail|blocked","failed_step":null,"evidence":"","note":""}
  ],
  "summary":{"total":62,"pass":0,"fail":0,"blocked":0}
}
```
