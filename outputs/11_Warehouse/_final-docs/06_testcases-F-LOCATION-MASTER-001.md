# AI Test Cases — Warehouse & Bin (คลังและตำแหน่ง)

ไฟล์นี้ให้ **AI agent (browser-use / vision)** อ่านแล้วลงมือทดสอบบนหน้าจอจริงของ prototype `WarehouseBin.html` แล้วรายงานผลกลับ. ทุก action anchor ด้วย **ข้อความที่เห็นบนจอ** (verbatim จาก HTML source of truth) + สถานะจริง (`state.view` / `state.drawer.view` / `state.modal.type`) — **prototype เป็น SPA ไม่มี hash route** (LD-08/D15). Expected ทุกข้อเช็คได้ด้วยตา.

> **สำคัญ — RBAC (D15):** prototype **ไม่มี role switcher บนจอ** (ถอดออกแล้ว). การเปลี่ยน role ต้องทำผ่าน **state จริง** ที่โค้ดใช้: เปิด browser console แล้วสั่ง `setRole('<role>')` (เช่น `setRole('operator')`) — ฟังก์ชันนี้ set `state.role` + re-render. role เริ่มต้น = `manager`. ห้ามมองหา/คลิกปุ่มสลับ role บนหน้าจอ (มันไม่มี).

---

## Meta

| ฟิลด์ | ค่า |
|---|---|
| Feature ID | F-LOCATION-MASTER-001 |
| ชื่อ | Warehouse & Bin (TH: คลังและตำแหน่ง) |
| เวอร์ชัน TC | 1.0 (fresh, ไม่ใช่ regen) |
| App entry | เปิดไฟล์ `01_HTML/WarehouseBin.html` ใน browser → default `state.view='list'`, `state.role='manager'`, drill=root ("ทุกคลัง") |
| "Routes" (SPA state) | list=`state.view='list'` · tree=`state.view='tree'` · drawer=`state.drawer.view` (`node-form`/`loc-form`/`bulk`/`view-node`/`view-loc`) · modal=`state.modal.type` (`delete-node`/`decommission`/`block`) |
| Navigation model | drill-down: คลิกแถวใน List เพื่อเจาะระดับถัดไป (คลัง→โซน→พื้นที่→ชั้นวาง→ตำแหน่ง); breadcrumb "ทุกคลัง › WH(code) › Zone(name) › Area(name) › Rack(name)" |
| ที่มา | FRD Pack `04_FRD/FRD_F-LOCATION-MASTER-001_Pack` (06_TESTS/05_RULES/02_API/01_UI/00_OVERVIEW/07_LOCKED) · BRD `03_BRD/BRD_Warehouse_Bin.md` · DECISION_LOG D1–D15 · HTML source of truth |
| จำนวนเคส | 70 (happy 24 · negative 20 · edge 8 · permission 9 · cross-module XT 4 · Scope-Lock verify 5) — error codes ครอบใน negative/edge; ดู Coverage |
| Seed roles | manager(ธนา) · supervisor(สมชาย) · controller(วิภา) · operator(มานี) · admin(อรุณ) — `ROLES` L2030 |

---

## Coverage

| group | เคส | ความสำคัญ |
|---|---|---|
| A · สร้าง/แก้ไข คลัง (Warehouse) | TC-A01..A06 | สูง |
| Z · สร้างโซน (Zone) + temp | TC-Z01..Z05 | สูง |
| AR · สร้าง/แก้ไข พื้นที่ (Area) + allows_direct | TC-AR01..AR04 | สูง |
| RK · สร้างชั้นวาง (Rack) | TC-RK01..RK02 | กลาง |
| L · สร้างตำแหน่ง (Location 2-step) | TC-L01..L08 | สูง |
| B · Bulk Generate | TC-B01..B04 | สูง |
| ST · เปลี่ยนสถานะ / activate / block | TC-ST01..ST06 | สูง |
| AC · จัดเก็บ node / ปลดระวาง / reparent | TC-AC01..AC06 | สูง |
| P · สิทธิ์ (RBAC) | TC-P01..P09 | สูง |
| V · View / dual-view / full_path | TC-V01..V05 | กลาง |
| F · List filter / states / KPI | TC-F01..F06 | กลาง |
| XT · Cross-module | TC-XT01..XT04 | สูง |
| LK · Scope Lock verify | TC-LK01..LK05 | สูง |

---

## Coverage Ledger

### FR / Acceptance (06_TESTS §6.1)
| item | cases |
|---|---|
| AT-01 create WH + branch | TC-A01, TC-A02, TC-A04 |
| AT-02 zone temp | TC-Z02, TC-Z03, TC-Z04 |
| AT-03 allows_direct gate | TC-L03, TC-AR04 |
| AT-04 location XOR + cap | TC-L01, TC-L04, TC-L05, TC-L07 |
| AT-05 bulk generate | TC-B01, TC-B02 |
| AT-06 archive node | TC-AC01, TC-AC02 |
| AT-07 decommission | TC-AC03, TC-AC04 |
| AT-08 status change | TC-ST01, TC-ST03, TC-ST04 |
| AT-09 Operator view-only | TC-P01, TC-P02 |
| AT-10 switch view keep sel | TC-V03 |
| §6.2 barcode gate (create inactive) | TC-L06 |
| §6.3 edit | TC-A06, TC-E-in-ST02, TC-AR04 |
| §6.4 reparent gate | TC-AC05 |

### Business Rules (05_RULES §5.1)
| rule | cases |
|---|---|
| BR-001 5-level hierarchy | TC-F06, TC-V03, TC-LK05 |
| BR-002 parent rack XOR area | TC-L01, TC-L02, TC-L07 |
| BR-003 area allows_direct required | TC-L03 |
| BR-004 code unique | TC-A04, TC-Z05, TC-AR03, TC-RK02, TC-L05 |
| BR-005 archive block active children | TC-AC01 |
| BR-006 capacity > 0 | TC-L04, TC-B03 |
| BR-007 no turn-off allows_direct w/ direct loc | TC-AR04 |
| BR-008 temp range required + min≤max | TC-Z02, TC-Z03, TC-Z04 |
| BR-009 warehouse branch required | TC-A02 |
| BR-010 decommission stock=0 | TC-AC03, TC-AC04 |
| BR-011 no hard delete (soft) | TC-AC02, TC-AC04, TC-LK02 |
| BR-012 reparent stock=0 | TC-AC05 |
| BR-013 block reason required | TC-ST03, TC-ST04 |
| BR-014 barcode before activate | TC-L06, TC-ST01, TC-ST02 |
| BR-015 bulk preview+collision+atomic | TC-B01, TC-B02 |
| BR-016 RBAC roles | TC-P01..TC-P09 |
| BR-017 geo cascade reset + postcode | TC-A05 |
| BR-018 type default flags | — ข้าม (DEFERRED Phase 3, schema-ready ไม่ implement — 05_RULES §5.6) |

### Edge Cases (05_RULES §5.4)
| EC | cases / สถานะ |
|---|---|
| EC-01 flexible-parent (rack+area) | TC-L07 (XOR radio-card เลือกได้ทีละ 1 — ป้องกันที่ UI) |
| EC-02 allows_direct=false chosen | TC-L03 |
| EC-03 referential-safe archive | TC-AC01 |
| EC-04 decommission stock≠0 | TC-AC03 |
| EC-05 reparent stock≠0 | TC-AC05 |
| EC-06 bulk collision atomic rollback | TC-B02 |
| EC-07 code ซ้ำ | TC-A04, TC-Z05, TC-L05 |
| EC-08 turn-off allows_direct w/ direct loc | TC-AR04 |
| EC-09 zone temp missing/min>max | TC-Z02, TC-Z03 |
| EC-10 geo cascade reset | TC-A05 |
| EC-11 activate no barcode | TC-ST01 |
| EC-12 Operator view-only | TC-P01, TC-P02 |
| EC-13 Supervisor/Controller archive/decommission deny | TC-P04, TC-P06 |
| EC-14 soft-ref not-found `[AI-DEFAULT]` | — ข้าม (prototype ใช้ mock branch/geo ที่ code เจอเสมอ; UI ไม่มี path จำลอง not-found — OQ-4, ทดสอบเมื่อต่อ master จริง Phase 2) |
| EC-15 concurrent same code `[AI-DEFAULT]` | — ข้าม (single-client prototype จำลอง 2-user race ไม่ได้; uniqueness DB-enforced ทดสอบที่ API/DB — OQ-7) `[AI-DEFAULT]` |
| EC-16 archive w/ already-archived children only | TC-AC06 |
| EC-17 bulk huge cap `[AI-DEFAULT]` | TC-B04 `[AI-DEFAULT]` (สังเกต preview จำนวน; soft cap ~500 — OQ-5) |
| EC-18 full_path when parent renamed | TC-XT02 (contract re-read; prototype ไม่มี downstream cache → simulate) |

### Error Codes (05_RULES §5.5)
| error | cases |
|---|---|
| MISSING_REQUIRED (400) | TC-A03, TC-L08 |
| BRANCH_REQUIRED (400) | TC-A02 |
| DUPLICATE_CODE (409) | TC-A04, TC-Z05, TC-AR03, TC-RK02, TC-L05 |
| TEMP_RANGE_INVALID (400) | TC-Z02, TC-Z03 |
| PARENT_XOR_VIOLATION (400) | TC-L07 (UI-prevented via radio-card XOR) |
| ALLOWS_DIRECT_REQUIRED (400) | TC-L03 |
| ALLOWS_DIRECT_HAS_CHILDREN (409) | TC-AR04 |
| CAPACITY_INVALID (400) | TC-L04, TC-B03 |
| HAS_ACTIVE_CHILDREN (409) | TC-AC01 |
| DECOMMISSION_STOCK_NOT_EMPTY (409) | TC-AC03 |
| REPARENT_STOCK_NOT_EMPTY (409) | TC-AC05 |
| BARCODE_REQUIRED (409) | TC-ST01 |
| BLOCK_REASON_REQUIRED (400) | TC-ST03 |
| BULK_TEMPLATE_INVALID (400) | TC-B02 (collision path) |
| BULK_COLLISION (409) | TC-B02 |
| FORBIDDEN_ROLE (403) | TC-P04, TC-P06 (UI = disabled + tooltip; API = 403 — simulate) |
| NOT_FOUND (404) | TC-F05 (error state UI — "รายการที่คุณกำลังเจาะดูอาจถูกลบหรือย้ายไปแล้ว…") |

### Permission Matrix (role × action — 00 §0.8)
| cell | cases |
|---|---|
| manager create/edit/status/del = allow | TC-P07 |
| admin create/edit/status/del = allow | TC-P08 |
| supervisor create/edit/status = allow | TC-P03 |
| supervisor archive/decommission = deny | TC-P04 |
| controller status = allow · create = deny | TC-P05 |
| controller archive/decommission = deny | TC-P06 |
| operator create/bulk = deny | TC-P01 |
| operator status/archive/decommission = deny | TC-P02, TC-P09 |

### Cross-Module (XT — 06_TESTS §6.9)
| XT | Downstream | Case |
|---|---|---|
| XT-01 decommission → no orphan stock | Inventory | TC-XT01 |
| XT-02 reparent → path change event | downstream cache re-read | TC-XT02 |
| XT-03 block/frozen → picking/putaway gate | Picking/Put Away | TC-XT03 |
| XT-04 full_path contract (no branch, D15) | Inventory/GR/… | TC-XT04, TC-V04 |

### Scope Lock (LOCK — 07 §7.0)
| LOCK | ข้อยืนยัน (ย่อ) | Case verify |
|---|---|---|
| D1 | feature id / HTML file / naming | TC-LK03 |
| D3 | branch_id บน warehouses เท่านั้น, no company_id | TC-LK01 |
| D8 | RBAC role-only, branch = filter/UX | TC-P05, TC-F01 |
| D11/GC#7 | no hard delete (archive/decommission soft + WORM) | TC-LK02, TC-AC02, TC-AC04 |
| D12 | dual-view List + Hierarchy Tree | TC-LK05, TC-V03 |
| D14 | canonical name "คลังและตำแหน่ง" | TC-LK03 |
| D15 | no role switcher · branch not in path | TC-LK04, TC-V04 |

### Cross-cutting / States / Events
| item | cases |
|---|---|
| KPI 5-tile (คลัง/โซน/พื้นที่/ชั้นวาง/ตำแหน่ง) | TC-F06 |
| loading skeleton / empty / filtered-empty / error state | TC-F05 |
| WORM audit written every mutation (ประวัติ tab) | TC-V02, TC-ST04, TC-AC04 |
| status pill = color-code / type pill = icon+label (D10) | TC-F06, TC-V02 |
| Esc chain / dirty-check drawer | TC-L08 (Esc), TC-A06 |
| event location.decommissioned/reparented/blocked | TC-XT01, TC-XT02, TC-XT03 (simulate) |

---

## Data Sets

### ชุดข้อมูล (กรอกได้จริง)
| ชุด | ฟิลด์ | ค่า |
|---|---|---|
| **WH-OK** (คลังถูก) | รหัสคลัง | `WH-TEST` |
| | ชื่อคลัง | `คลังทดสอบ QA` |
| | สาขา | `สาขา 1 (บางนา)` (BR-01) |
| | จังหวัด → อำเภอ → ตำบล | `สมุทรปราการ` → `บางพลี` → `บางพลีใหญ่` (postcode auto = 10540) |
| **WH-DUP** (code ซ้ำ) | รหัสคลัง | `WH-01` (มีอยู่แล้วในระบบ) · ชื่อ `ซ้ำทดสอบ` · สาขา `สำนักงานใหญ่` |
| **WH-NOBRANCH** | รหัสคลัง `WH-NB` · ชื่อ `ไม่มีสาขา` · **สาขา = เว้นว่าง** |
| **WH-NOCODE** | รหัสคลัง = **เว้นว่าง** · ชื่อ `ไม่มีรหัส` · สาขา `สำนักงานใหญ่` |
| **ZONE-COLD-OK** | รหัสโซน `Z-TEST` · ชื่อ `โซนแช่เย็นทดสอบ` · ควบคุมอุณหภูมิ = เปิด · ต่ำสุด `2` · สูงสุด `8` |
| **ZONE-TEMP-EMPTY** | รหัส `Z-TE` · ชื่อ `อุณหภูมิว่าง` · ควบคุมอุณหภูมิ = เปิด · ต่ำสุด/สูงสุด = เว้นว่าง |
| **ZONE-TEMP-INVERT** | รหัส `Z-TI` · ชื่อ `อุณหภูมิสลับ` · ควบคุมอุณหภูมิ = เปิด · ต่ำสุด `10` · สูงสุด `4` |
| **ZONE-DUP** | รหัส `Z-STG` (ซ้ำใน WH-01) · ชื่อ `ซ้ำโซน` |
| **AREA-DIRECT-ON** | รหัส `A-TEST` · ชื่อ `พื้นที่วางตรง` · allows_direct = เปิด |
| **AREA-DUP** | รหัส `A-FM` (ซ้ำใน Z-STORAGE) |
| **RACK-OK** | รหัส `R-TEST` · ชื่อ `ชั้นวางทดสอบ` · rows `4` · cols `10` · levels `4` |
| **RACK-DUP** | รหัส `R-A01` (ซ้ำใน A-AISLE-A) |
| **LOC-RACK-OK** | parent = ใต้ชั้นวาง (Rack) `R-A01` · รหัส `A-01-R9-C9-L9` · ประเภท `RESERVE` · หน่วย `pallet` · ความจุ `2` · rotation `FIFO` · barcode `8850009000001` |
| **LOC-AREA-OK** | parent = ใต้พื้นที่ (Area) `A-FM` (allows_direct) · รหัส `FM-PF-TEST` · ประเภท `PICK_FACE` · ความจุ `40` · barcode `8850009000002` |
| **LOC-AREA-DENY** | parent = ใต้พื้นที่ (Area) `A-AISLE-A` (allows_direct=false) · รหัส `X-DENY` |
| **LOC-CAP0** | parent = Rack `R-A01` · รหัส `CAP0` · ความจุ `0` |
| **LOC-DUP** | parent = Rack `R-A01` · รหัส `A-01-R1-C1-L1` (ซ้ำ L001) |
| **LOC-NOBARCODE** | parent = Rack `R-A02` · รหัส `NB-TEST` · ความจุ `2` · barcode = เว้นว่าง |
| **BULK-OK** | target_area `A-AISLE-A` · รูปแบบรหัสชั้นวาง `R-NEW-{n}` · จำนวนชั้นวาง `2` · รูปแบบรหัสตำแหน่ง `{rack}-R{r}-C{c}-L{l}` · rows `2` cols `2` levels `1` · ความจุ `2` |
| **BULK-COLLIDE** | target_area `A-AISLE-A` · รูปแบบรหัสชั้นวาง `R-A0{n}` (ชนกับ R-A01/R-A02 ที่มีอยู่) · จำนวน `2` · ความจุ `2` |
| **BULK-CAP0** | target_area `A-AISLE-A` · รูปแบบ `R-Z-{n}` · จำนวน `1` · ความจุ `0` |
| **BLOCK-REASON** | เหตุผลที่บล็อก `รอซ่อมคานชั้นวาง` |

### Seed records (มีใน prototype ตั้งต้น — อ้างในเคส)
- **Warehouses:** WH-01 (คลังกลาง บางนา · BR-01), WH-02 (คลังภาคเหนือ ลำพูน · BR-02), WH-03 (คลัง Cross-dock สนญ. · HQ). WH-01 มีลูก (zones) active → archive block.
- **Areas allows_direct=false:** `A-AISLE-A`, `A-AISLE-B`, `A-CHILL`. **allows_direct=true (มี direct loc):** `A-FM` (มี L003/L004/L005).
- **Locations hasStock=true (decommission/reparent block):** L001 (A-01-R1-C1-L1), L003 (FM-PF-01), L004 (FM-PF-02, full), L007 (B-01-R2-C1-L1), L009 (HOLD-GRN0412), L012 (C-01-R1-C1-L1, frozen).
- **Locations stock=0 (decommission ได้):** L010 (DMG-01, active, มี barcode).
- **Location inactive ไม่มี barcode (activate block):** L006 (PACK-02, ใต้ A-PACK). **active ไม่มี barcode:** L013 (VIRT-ADJ).
- **Location blocked:** L008 (B-01-R2-C1-L2, เหตุผล "รอซ่อมคานชั้นวาง").
- `LOC_REQUIRE_BARCODE = true` (BR-014 ON).

### ไฟล์ทดสอบ (Files)
- ไม่มี — feature นี้ไม่มี CSV import/upload. ทุกเคส `files=—`.

---

## Test Cases

### Group A — สร้าง/แก้ไข คลัง (Warehouse)

#### TC-A01 — สร้างคลังครบฟิลด์ + สาขา + geo (happy)
- group: สร้างคลัง · ความสำคัญ: สูง · trace: AT-01 / S-01 / BR-004, BR-009, BR-017 / event node.created
- actor (role): Warehouse Manager
- Setup: role=manager (default) · seed=— · files=—
- Start: OPEN app (`state.view='list'`, breadcrumb = "ทุกคลัง")
- ชุดข้อมูล: WH-OK
- ผ่านเมื่อ: toast `สร้างคลัง "WH-TEST" สำเร็จ` + drawer ปิด + แถวใหม่ปรากฏใน List

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY หัวข้อหน้า | — | h1 = **คลังและตำแหน่ง (Warehouse & Bin)**; sub มี "จัดโครงสร้างจัดเก็บครบ 5 ระดับ…" | ☐ |
| 2 | CLICK ปุ่ม **สร้างคลัง** (มุมขวาบน card) | — | drawer เปิด (`state.drawer.view='node-form'`) หัวข้อ **สร้างคลัง** | ☐ |
| 3 | TYPE → ช่อง **รหัสคลัง** | WH-OK | ช่องแสดง `WH-TEST` | ☐ |
| 4 | TYPE → ช่อง **ชื่อคลัง** | WH-OK | ช่องแสดง `คลังทดสอบ QA` | ☐ |
| 5 | CLICK ช่อง **สาขา** (Master Combobox) → เลือก | WH-OK | dropdown เปิด, เลือก `สาขา 1 (บางนา)` แล้วช่องแสดงค่านั้น | ☐ |
| 6 | SELECT **จังหวัด** → **อำเภอ/เขต** → **ตำบล/แขวง** | WH-OK | เลือก สมุทรปราการ → บางพลี → บางพลีใหญ่ | ☐ |
| 7 | VERIFY ช่อง **รหัสไปรษณีย์** | — | เติมอัตโนมัติ `10540` (readonly) | ☐ |
| 8 | CLICK ปุ่ม **บันทึก** | — | drawer ปิด + toast **สร้างคลัง "WH-TEST" สำเร็จ** | ☐ |
| 9 | VERIFY ตาราง List (ระดับคลัง) | — | มีแถว `WH-TEST` / `คลังทดสอบ QA` + pill สถานะ **ใช้งาน** | ☐ |

#### TC-A02 — สร้างคลังไม่เลือกสาขา (negative, BRANCH_REQUIRED)
- group: สร้างคลัง · ความสำคัญ: สูง · trace: AT-01 / S-01 / BR-009 / err BRANCH_REQUIRED
- Setup: role=manager · seed=— · files=—
- Start: OPEN app → CLICK **สร้างคลัง**
- ชุดข้อมูล: WH-NOBRANCH
- ผ่านเมื่อ: บันทึกไม่ได้ + toast/inline แจ้ง "กรุณาเลือกสาขา"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างคลัง** | — | drawer node-form เปิด | ☐ |
| 2 | TYPE → **รหัสคลัง** + **ชื่อคลัง** | WH-NOBRANCH | แสดง `WH-NB` / `ไม่มีสาขา` | ☐ |
| 3 | VERIFY ช่อง **สาขา** | — | ปล่อยว่าง (ยังไม่เลือก) | ☐ |
| 4 | CLICK ปุ่ม **บันทึก** | — | drawer **ไม่ปิด** + toast **กรุณากรอกข้อมูลให้ครบถ้วน** + ช่องสาขาแสดง error **กรุณาเลือกสาขา** | ☐ |

#### TC-A03 — สร้างคลังไม่กรอกรหัส (negative, MISSING_REQUIRED)
- group: สร้างคลัง · ความสำคัญ: กลาง · trace: BR (required) / err MISSING_REQUIRED
- Setup: role=manager · seed=— · files=—
- Start: OPEN app → CLICK **สร้างคลัง**
- ชุดข้อมูล: WH-NOCODE
- ผ่านเมื่อ: บันทึกไม่ได้ + error ที่ช่องรหัส

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างคลัง** | — | drawer เปิด | ☐ |
| 2 | TYPE → **ชื่อคลัง** + เลือก **สาขา** (เว้นรหัสว่าง) | WH-NOCODE | รหัสยังว่าง | ☐ |
| 3 | CLICK ปุ่ม **บันทึก** | — | drawer ไม่ปิด + toast **กรุณากรอกข้อมูลให้ครบถ้วน** + ช่องรหัสแสดง **กรุณากรอกรหัส** | ☐ |

#### TC-A04 — สร้างคลัง code ซ้ำทั้งระบบ (negative, DUPLICATE_CODE / EC-07)
- group: สร้างคลัง · ความสำคัญ: สูง · trace: AT-01 / BR-004 / EC-07 / err DUPLICATE_CODE
- Setup: role=manager · seed=WH-01 มีอยู่ · files=—
- Start: OPEN app → CLICK **สร้างคลัง**
- ชุดข้อมูล: WH-DUP
- ผ่านเมื่อ: บันทึกไม่ได้ + error "รหัสซ้ำในระบบ"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างคลัง** | — | drawer เปิด | ☐ |
| 2 | TYPE → **รหัสคลัง** = ค่าที่ซ้ำ + **ชื่อ** + เลือก **สาขา** | WH-DUP | รหัสแสดง `WH-01` | ☐ |
| 3 | CLICK ปุ่ม **บันทึก** | — | drawer ไม่ปิด + ช่องรหัสแสดง error **รหัสซ้ำในระบบ** + toast **กรุณากรอกข้อมูลให้ครบถ้วน** | ☐ |

#### TC-A05 — geo cascade reset + auto postcode (edge: EC-10 / BR-017)
- group: สร้างคลัง · ความสำคัญ: กลาง · trace: BR-017 / EC-10
- Setup: role=manager · seed=— · files=—
- Start: OPEN app → CLICK **สร้างคลัง**
- ชุดข้อมูล: WH-OK (แล้วเปลี่ยนจังหวัด)
- ผ่านเมื่อ: เปลี่ยนจังหวัด → อำเภอ/ตำบล ถูกล้าง + postcode รีเซ็ต

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างคลัง** | — | drawer เปิด | ☐ |
| 2 | SELECT **จังหวัด** → **อำเภอ** → **ตำบล** | WH-OK: สมุทรปราการ→บางพลี→บางพลีใหญ่ | postcode auto = `10540` (readonly) | ☐ |
| 3 | SELECT **จังหวัด** = เปลี่ยนเป็นค่าอื่น | เช่น กรุงเทพมหานคร | ช่อง **อำเภอ/เขต** และ **ตำบล/แขวง** ถูกล้าง (ต้องเลือกใหม่) + postcode ว่าง/รีเซ็ต | ☐ |
| 4 | SELECT อำเภอ + ตำบล ของจังหวัดใหม่ | (ค่าที่มีใน dropdown) | postcode เติมใหม่ตามตำบลที่เลือก | ☐ |

#### TC-A06 — แก้ไข node + dirty-check ปิด drawer (happy / UX §6.3)
- group: แก้ไขคลัง · ความสำคัญ: กลาง · trace: §6.3 edit / event node.updated
- Setup: role=manager · seed=WH-01 · files=—
- Start: OPEN app (ระดับคลัง)
- ชุดข้อมูล: —
- ผ่านเมื่อ: แก้แล้วบันทึก → toast "บันทึกการแก้ไขแล้ว"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไอคอน **แก้ไข** (ดินสอ) ท้ายแถว `WH-01` | — | drawer node-form เปิด หัวข้อ **แก้ไขคลัง** ค่าเดิมกรอกอยู่ | ☐ |
| 2 | TYPE → **ชื่อคลัง** = แก้เป็นค่าใหม่ | `คลังกลาง บางนา (แก้ไข)` | ช่องแสดงค่าใหม่ | ☐ |
| 3 | PRESS Esc | — | เพราะมีการแก้ไข → มี confirm ถามยืนยันทิ้งการแก้ไข (dirty-check) | ☐ |
| 4 | CLICK ยกเลิก confirm → CLICK ปุ่ม **บันทึก** | — | drawer ปิด + toast **บันทึกการแก้ไขแล้ว** | ☐ |

---

### Group Z — สร้างโซน (Zone) + temperature

> การสร้างโซนต้องเจาะเข้าคลังก่อน (drill → level=warehouse → ปุ่ม create = **สร้างโซน**).

#### TC-Z01 — สร้างโซนปกติ (ไม่ควบคุมอุณหภูมิ) (happy)
- group: สร้างโซน · ความสำคัญ: สูง · trace: BR-004 / S-02
- Setup: role=manager · seed=WH-01 · files=—
- Start: OPEN app → CLICK แถว `WH-01` (drill เข้าโซนของ WH-01)
- ชุดข้อมูล: (รหัส `Z-NORMAL` · ชื่อ `โซนปกติ` · ควบคุมอุณหภูมิ = ปิด)
- ผ่านเมื่อ: toast `สร้างโซน "Z-NORMAL" สำเร็จ`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว **WH-01** ใน List | — | breadcrumb เปลี่ยนเป็น "ทุกคลัง › WH-01"; ตารางแสดงโซนของ WH-01 | ☐ |
| 2 | CLICK ปุ่ม **สร้างโซน** | — | drawer node-form (level=zone) เปิด หัวข้อ **สร้างโซน** | ☐ |
| 3 | TYPE → **รหัส** + **ชื่อ** | Z-NORMAL / โซนปกติ | ช่องแสดงค่า | ☐ |
| 4 | VERIFY toggle **ควบคุมอุณหภูมิ (Cold chain)** | — | ปิดอยู่ (default) → ไม่มีช่องอุณหภูมิต่ำสุด/สูงสุด | ☐ |
| 5 | CLICK ปุ่ม **บันทึก** | — | drawer ปิด + toast **สร้างโซน "Z-NORMAL" สำเร็จ** | ☐ |

#### TC-Z02 — โซน temp เปิดแต่ไม่กรอกช่วง (negative, TEMP_RANGE_INVALID / EC-09 / AT-02)
- group: สร้างโซน · ความสำคัญ: สูง · trace: AT-02 / S-02 / BR-008 / EC-09 / err TEMP_RANGE_INVALID
- Setup: role=manager · seed=WH-01 · files=—
- Start: OPEN app → CLICK แถว `WH-01` → CLICK **สร้างโซน**
- ชุดข้อมูล: ZONE-TEMP-EMPTY
- ผ่านเมื่อ: บันทึกไม่ได้ + "กรุณากรอกช่วงอุณหภูมิ"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → **รหัส** + **ชื่อ** | ZONE-TEMP-EMPTY | Z-TE / อุณหภูมิว่าง | ☐ |
| 2 | TOGGLE **ควบคุมอุณหภูมิ (Cold chain)** = เปิด | — | ปรากฏช่อง **อุณหภูมิต่ำสุด (°C)** + **อุณหภูมิสูงสุด (°C)** | ☐ |
| 3 | CLICK ปุ่ม **บันทึก** (เว้นช่องอุณหภูมิว่าง) | — | drawer ไม่ปิด + error ที่ช่องอุณหภูมิ **กรุณากรอกช่วงอุณหภูมิ** + toast **กรุณากรอกข้อมูลให้ครบถ้วน** | ☐ |

#### TC-Z03 — โซน temp min>max (negative, TEMP_RANGE_INVALID / EC-09)
- group: สร้างโซน · ความสำคัญ: สูง · trace: AT-02 / BR-008 / EC-09
- Setup: role=manager · seed=WH-01 · files=—
- Start: OPEN app → CLICK `WH-01` → CLICK **สร้างโซน**
- ชุดข้อมูล: ZONE-TEMP-INVERT
- ผ่านเมื่อ: error "อุณหภูมิต่ำสุดต้องไม่เกินสูงสุด"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → **รหัส** + **ชื่อ** | ZONE-TEMP-INVERT | Z-TI / อุณหภูมิสลับ | ☐ |
| 2 | TOGGLE **ควบคุมอุณหภูมิ** = เปิด | — | ช่องอุณหภูมิปรากฏ | ☐ |
| 3 | TYPE → **อุณหภูมิต่ำสุด** = 10, **อุณหภูมิสูงสุด** = 4 | ZONE-TEMP-INVERT | ค่าปรากฏ | ☐ |
| 4 | CLICK ปุ่ม **บันทึก** | — | drawer ไม่ปิด + error **อุณหภูมิต่ำสุดต้องไม่เกินสูงสุด** | ☐ |

#### TC-Z04 — โซน temp ถูกต้อง (happy, BR-008)
- group: สร้างโซน · ความสำคัญ: สูง · trace: AT-02 / S-02 / BR-008
- Setup: role=manager · seed=WH-01 · files=—
- Start: OPEN app → CLICK `WH-01` → CLICK **สร้างโซน**
- ชุดข้อมูล: ZONE-COLD-OK
- ผ่านเมื่อ: toast `สร้างโซน "Z-TEST" สำเร็จ`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → **รหัส** + **ชื่อ** | ZONE-COLD-OK | Z-TEST / โซนแช่เย็นทดสอบ | ☐ |
| 2 | TOGGLE **ควบคุมอุณหภูมิ** = เปิด → TYPE ต่ำสุด `2` สูงสุด `8` | ZONE-COLD-OK | ค่าปรากฏ min≤max | ☐ |
| 3 | CLICK ปุ่ม **บันทึก** | — | drawer ปิด + toast **สร้างโซน "Z-TEST" สำเร็จ** | ☐ |

#### TC-Z05 — โซน code ซ้ำภายในคลัง (negative, DUPLICATE_CODE / EC-07)
- group: สร้างโซน · ความสำคัญ: กลาง · trace: BR-004 / EC-07 / err DUPLICATE_CODE
- Setup: role=manager · seed=WH-01 มีโซน Z-STG · files=—
- Start: OPEN app → CLICK `WH-01` → CLICK **สร้างโซน**
- ชุดข้อมูล: ZONE-DUP
- ผ่านเมื่อ: error "รหัสซ้ำภายในคลังเดียวกัน"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → **รหัส** = `Z-STG` + **ชื่อ** | ZONE-DUP | Z-STG / ซ้ำโซน | ☐ |
| 2 | CLICK ปุ่ม **บันทึก** | — | drawer ไม่ปิด + error **รหัสซ้ำภายในคลังเดียวกัน** | ☐ |

---

### Group AR — สร้าง/แก้ไข พื้นที่ (Area) + allows_direct

#### TC-AR01 — สร้างพื้นที่ allows_direct เปิด (happy)
- group: สร้างพื้นที่ · ความสำคัญ: สูง · trace: S-03 / BR-004
- Setup: role=manager · seed=WH-01 › Z-STORAGE · files=—
- Start: OPEN app → CLICK `WH-01` → CLICK แถวโซน `Z-STG` (drill) → CLICK **สร้างพื้นที่**
- ชุดข้อมูล: AREA-DIRECT-ON
- ผ่านเมื่อ: toast `สร้างพื้นที่ "A-TEST" สำเร็จ`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว **WH-01** → CLICK แถวโซน **Z-STG** | — | breadcrumb "ทุกคลัง › WH-01 › Storage Zone"; ตารางแสดงพื้นที่ | ☐ |
| 2 | CLICK ปุ่ม **สร้างพื้นที่** | — | drawer node-form (level=area) เปิด | ☐ |
| 3 | TYPE → **รหัส** + **ชื่อ** | AREA-DIRECT-ON | A-TEST / พื้นที่วางตรง | ☐ |
| 4 | TOGGLE **อนุญาตวางตำแหน่งตรงใต้พื้นที่** = เปิด | — | toggle เปิด (sub "วางบนพื้นได้โดยไม่ต้องผ่านชั้นวาง…") | ☐ |
| 5 | CLICK ปุ่ม **บันทึก** | — | drawer ปิด + toast **สร้างพื้นที่ "A-TEST" สำเร็จ** | ☐ |

#### TC-AR02 — สร้างพื้นที่ allows_direct ปิด (happy)
- group: สร้างพื้นที่ · ความสำคัญ: กลาง · trace: S-03
- Setup: role=manager · seed=WH-01 › Z-STORAGE · files=—
- Start: OPEN app → drill WH-01 → Z-STG → CLICK **สร้างพื้นที่**
- ชุดข้อมูล: (รหัส `A-NOD` · ชื่อ `พื้นที่ไม่วางตรง` · allows_direct = ปิด)
- ผ่านเมื่อ: toast `สร้างพื้นที่ "A-NOD" สำเร็จ`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → **รหัส** + **ชื่อ** | A-NOD / พื้นที่ไม่วางตรง | ค่าปรากฏ | ☐ |
| 2 | VERIFY toggle **อนุญาตวางตำแหน่งตรงใต้พื้นที่** | — | ปิดอยู่ (default) | ☐ |
| 3 | CLICK ปุ่ม **บันทึก** | — | drawer ปิด + toast **สร้างพื้นที่ "A-NOD" สำเร็จ** | ☐ |

#### TC-AR03 — พื้นที่ code ซ้ำภายในโซน (negative, DUPLICATE_CODE)
- group: สร้างพื้นที่ · ความสำคัญ: กลาง · trace: BR-004 / EC-07
- Setup: role=manager · seed=Z-STORAGE มี A-FM · files=—
- Start: OPEN app → drill WH-01 → Z-STG → CLICK **สร้างพื้นที่**
- ชุดข้อมูล: AREA-DUP
- ผ่านเมื่อ: error "รหัสซ้ำภายในโซนเดียวกัน"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → **รหัส** = `A-FM` + **ชื่อ** = ซ้ำ | AREA-DUP | ค่าปรากฏ | ☐ |
| 2 | CLICK ปุ่ม **บันทึก** | — | drawer ไม่ปิด + error **รหัสซ้ำภายในโซนเดียวกัน** | ☐ |

#### TC-AR04 — แก้พื้นที่ปิด allows_direct ทั้งที่มี direct location (negative edge: EC-08 / BR-007 / ALLOWS_DIRECT_HAS_CHILDREN)
- group: แก้พื้นที่ · ความสำคัญ: สูง · trace: AT-03 / BR-007 / EC-08 / err ALLOWS_DIRECT_HAS_CHILDREN
- Setup: role=manager · seed=A-FM allows_direct=true + มี direct location L003/L004/L005 · files=—
- Start: OPEN app → drill WH-01 → Z-STG (ตารางพื้นที่)
- ชุดข้อมูล: —
- ผ่านเมื่อ: ปิด allows_direct ไม่ได้ + error "ปิด allows_direct ไม่ได้ — ยังมีตำแหน่งวางตรงอยู่ {n} รายการ"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไอคอน **แก้ไข** (ดินสอ) ท้ายแถว `A-FM` | — | drawer node-form (แก้ไขพื้นที่) เปิด, toggle **อนุญาตวางตำแหน่งตรง** = เปิดอยู่ | ☐ |
| 2 | TOGGLE **อนุญาตวางตำแหน่งตรงใต้พื้นที่** = ปิด | — | toggle เปลี่ยนเป็นปิด | ☐ |
| 3 | CLICK ปุ่ม **บันทึก** | — | drawer ไม่ปิด + error **ปิด allows_direct ไม่ได้ — ยังมีตำแหน่งวางตรงอยู่ 3 รายการ** (จำนวน = direct loc ของ A-FM) | ☐ |

---

### Group RK — สร้างชั้นวาง (Rack)

#### TC-RK01 — สร้างชั้นวาง + grid (happy)
- group: สร้างชั้นวาง · ความสำคัญ: กลาง · trace: BR-004 / S-05 (grid source)
- Setup: role=manager · seed=WH-01 › Z-STORAGE › A-AISLE-A · files=—
- Start: OPEN app → drill WH-01 → Z-STG → คลิกแถวพื้นที่ `A-AISLE-A` → CLICK **สร้างชั้นวาง**
- ชุดข้อมูล: RACK-OK
- ผ่านเมื่อ: toast `สร้างชั้นวาง "R-TEST" สำเร็จ`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถวพื้นที่ **A-AISLE-A** (allows_direct=false → sub-tab "ชั้นวางในพื้นที่") | — | breadcrumb ถึง Area; ตารางชั้นวางของ A-AISLE-A | ☐ |
| 2 | CLICK ปุ่ม **สร้างชั้นวาง** | — | drawer node-form (level=rack) เปิด | ☐ |
| 3 | TYPE → **รหัส** + **ชื่อ** + **rows/cols/levels** | RACK-OK | R-TEST / ชั้นวางทดสอบ / 4 × 10 × 4 | ☐ |
| 4 | CLICK ปุ่ม **บันทึก** | — | drawer ปิด + toast **สร้างชั้นวาง "R-TEST" สำเร็จ** | ☐ |

#### TC-RK02 — ชั้นวาง code ซ้ำภายในพื้นที่ (negative, DUPLICATE_CODE)
- group: สร้างชั้นวาง · ความสำคัญ: กลาง · trace: BR-004 / EC-07
- Setup: role=manager · seed=A-AISLE-A มี R-A01 · files=—
- Start: OPEN app → drill ถึง A-AISLE-A → CLICK **สร้างชั้นวาง**
- ชุดข้อมูล: RACK-DUP
- ผ่านเมื่อ: error "รหัสซ้ำภายในพื้นที่เดียวกัน"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE → **รหัส** = `R-A01` + **ชื่อ** | RACK-DUP | ค่าปรากฏ | ☐ |
| 2 | CLICK ปุ่ม **บันทึก** | — | drawer ไม่ปิด + error **รหัสซ้ำภายในพื้นที่เดียวกัน** | ☐ |

---

### Group L — สร้างตำแหน่ง (Location · 2-step wizard)

#### TC-L01 — สร้างตำแหน่งใต้ชั้นวาง (happy, XOR=rack)
- group: สร้างตำแหน่ง · ความสำคัญ: สูง · trace: AT-04 / S-04 / BR-002, BR-006, BR-014 / event location.created
- Setup: role=manager · seed=R-A01 (ใต้ A-AISLE-A) · files=—
- Start: OPEN app → drill WH-01 → Z-STG → A-AISLE-A → คลิกแถวชั้นวาง `R-A01` → CLICK **สร้างตำแหน่ง**
- ชุดข้อมูล: LOC-RACK-OK
- ผ่านเมื่อ: toast `สร้างตำแหน่ง "A-01-R9-C9-L9" สำเร็จ` (มี barcode → active)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถวชั้นวาง **R-A01** → CLICK ปุ่ม **สร้างตำแหน่ง** | — | drawer loc-form เปิด, stepper 2 ขั้น: **ต้นทาง & ข้อมูลระบุ** / **ความจุ & พฤติกรรม**; step 1 active | ☐ |
| 2 | VERIFY radio-card ต้นทาง | — | มี 2 การ์ด **ใต้ชั้นวาง (Rack)** / **ใต้พื้นที่ (Area)**; ปกติ context = rack ถูกเลือก | ☐ |
| 3 | CLICK การ์ด **ใต้ชั้นวาง (Rack)** → เลือก rack `R-A01` (Master Combobox) | LOC-RACK-OK | การ์ด rack เป็น is-sel; picker แสดง R-A01 | ☐ |
| 4 | TYPE → **รหัสตำแหน่ง** | LOC-RACK-OK | `A-01-R9-C9-L9` | ☐ |
| 5 | CLICK ปุ่มไปขั้นถัดไป (step 2) | — | เข้าสู่ **ความจุ & พฤติกรรม** | ☐ |
| 6 | SELECT **ประเภท** + **หน่วยความจุ** + TYPE **ความจุ** + SELECT **rotation** + TYPE **บาร์โค้ด** | LOC-RACK-OK | RESERVE / pallet / 2 / FIFO / 8850009000001 | ☐ |
| 7 | CLICK ปุ่ม **บันทึก** | — | drawer ปิด + toast **สร้างตำแหน่ง "A-01-R9-C9-L9" สำเร็จ** (ไม่มีวงเล็บ "ปิดใช้") | ☐ |

#### TC-L02 — สร้างตำแหน่งใต้พื้นที่ allows_direct=true (happy, XOR=area)
- group: สร้างตำแหน่ง · ความสำคัญ: สูง · trace: AT-04 / BR-002, BR-003
- Setup: role=manager · seed=A-FM allows_direct=true · files=—
- Start: OPEN app → drill WH-01 → Z-STG → คลิกแถวพื้นที่ `A-FM` → (sub-tab "ตำแหน่งใต้พื้นที่โดยตรง") → CLICK **สร้างตำแหน่ง**
- ชุดข้อมูล: LOC-AREA-OK
- ผ่านเมื่อ: toast `สร้างตำแหน่ง "FM-PF-TEST" สำเร็จ`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถวพื้นที่ **A-FM** → CLICK sub-tab **ตำแหน่งใต้พื้นที่โดยตรง** (มี tag "flexible parent") | — | ตารางตำแหน่งตรงของ A-FM; ปุ่ม create = **สร้างตำแหน่ง** | ☐ |
| 2 | CLICK ปุ่ม **สร้างตำแหน่ง** → CLICK การ์ด **ใต้พื้นที่ (Area)** → เลือก area `A-FM` | LOC-AREA-OK | ไม่มี inline-warn (A-FM allows_direct=true) | ☐ |
| 3 | TYPE **รหัสตำแหน่ง** → step 2 → SELECT ประเภท `PICK_FACE` + ความจุ `40` + barcode | LOC-AREA-OK | ค่าปรากฏ | ☐ |
| 4 | CLICK ปุ่ม **บันทึก** | — | drawer ปิด + toast **สร้างตำแหน่ง "FM-PF-TEST" สำเร็จ** | ☐ |

#### TC-L03 — เลือกพื้นที่ allows_direct=false เป็น parent (negative edge: EC-02 / BR-003 / ALLOWS_DIRECT_REQUIRED)
- group: สร้างตำแหน่ง · ความสำคัญ: สูง · trace: AT-03 / BR-003 / EC-02 / err ALLOWS_DIRECT_REQUIRED
- Setup: role=manager · seed=A-AISLE-A allows_direct=false · files=—
- Start: OPEN app → CLICK **สร้างคลัง**? ไม่ — เข้า loc-form: drill ถึงจุดที่เปิด loc-form ได้ (เช่นจากใต้ rack) แล้วสลับ parent เป็น area A-AISLE-A
- ชุดข้อมูล: LOC-AREA-DENY
- ผ่านเมื่อ: แสดง inline-warn + ลิงก์ "เพิ่มชั้นวางในพื้นที่นี้ก่อน" และบันทึกไม่ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด drawer **สร้างตำแหน่ง** (จาก R-A01) → step 1 | — | loc-form step 1 | ☐ |
| 2 | CLICK การ์ด **ใต้พื้นที่ (Area)** → เลือก area `A-AISLE-A` (allows_direct=false) | LOC-AREA-DENY | ปรากฏ inline-warn **พื้นที่ A-AISLE-A ตั้งค่า allows_direct = false — วางตำแหน่งตรงไม่ได้ ต้องเลือกพื้นที่อื่น หรือ เพิ่มชั้นวางในพื้นที่นี้ก่อน** (มีลิงก์) | ☐ |
| 3 | TYPE **รหัสตำแหน่ง** → พยายามไป step 2 / CLICK **บันทึก** | LOC-AREA-DENY | บันทึกไม่ได้ + error ที่ area **พื้นที่นี้ allows_direct = false — เลือกพื้นที่อื่น หรือเพิ่มชั้นวางก่อน** | ☐ |
| 4 | CLICK ลิงก์ **เพิ่มชั้นวางในพื้นที่นี้ก่อน** | — | นำไปสู่ flow สร้างชั้นวางในพื้นที่ A-AISLE-A (suggestAddRack) | ☐ |

#### TC-L04 — capacity = 0 (negative, CAPACITY_INVALID / BR-006)
- group: สร้างตำแหน่ง · ความสำคัญ: สูง · trace: AT-04 / BR-006 / err CAPACITY_INVALID
- Setup: role=manager · seed=R-A01 · files=—
- Start: OPEN app → drill R-A01 → CLICK **สร้างตำแหน่ง**
- ชุดข้อมูล: LOC-CAP0
- ผ่านเมื่อ: error "ความจุต้องมากกว่า 0"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด loc-form → เลือก parent rack `R-A01` → TYPE รหัส `CAP0` → step 2 | LOC-CAP0 | ถึง step 2 | ☐ |
| 2 | TYPE **ความจุ** = `0` | LOC-CAP0 | ช่องแสดง 0 | ☐ |
| 3 | CLICK ปุ่ม **บันทึก** | — | บันทึกไม่ได้ + error/toast **ความจุต้องมากกว่า 0** | ☐ |

#### TC-L05 — code ซ้ำภายใน parent (negative, DUPLICATE_CODE / EC-07)
- group: สร้างตำแหน่ง · ความสำคัญ: สูง · trace: AT-04 / BR-004 / EC-07
- Setup: role=manager · seed=R-A01 มี L001 code A-01-R1-C1-L1 · files=—
- Start: OPEN app → drill R-A01 → CLICK **สร้างตำแหน่ง**
- ชุดข้อมูล: LOC-DUP
- ผ่านเมื่อ: กลับไป step 1 + error "รหัสซ้ำภายใน parent เดียวกัน"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด loc-form → parent rack `R-A01` → TYPE รหัส `A-01-R1-C1-L1` → step 2 กรอกความจุ `2` + barcode | LOC-DUP | ถึง step 2 | ☐ |
| 2 | CLICK ปุ่ม **บันทึก** | — | drawer กลับไป **step 1** + toast **รหัสซ้ำภายใน parent เดียวกัน** + error ที่ช่องรหัส | ☐ |

#### TC-L06 — ไม่มี barcode → บันทึกเป็น "ปิดใช้" (edge: §6.2 / BR-014)
- group: สร้างตำแหน่ง · ความสำคัญ: สูง · trace: §6.2 / BR-014 / EC-11 (create side)
- Setup: role=manager · seed=R-A02, LOC_REQUIRE_BARCODE=ON · files=—
- Start: OPEN app → drill R-A02 → CLICK **สร้างตำแหน่ง**
- ชุดข้อมูล: LOC-NOBARCODE
- ผ่านเมื่อ: toast มีส่วน "(ปิดใช้ — ต้องเพิ่มบาร์โค้ดก่อนเปิดใช้งาน)" + status = ปิดใช้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด loc-form → parent rack `R-A02` → TYPE รหัส `NB-TEST` → step 2 ความจุ `2`, **เว้น barcode ว่าง** | LOC-NOBARCODE | ถึง step 2, barcode ว่าง | ☐ |
| 2 | CLICK ปุ่ม **บันทึก** | — | drawer ปิด + toast **สร้างตำแหน่ง "NB-TEST" สำเร็จ (ปิดใช้ — ต้องเพิ่มบาร์โค้ดก่อนเปิดใช้งาน)** | ☐ |
| 3 | VERIFY แถว `NB-TEST` ในตาราง | — | pill สถานะ = **ปิดใช้** | ☐ |

#### TC-L07 — parent XOR (radio-card เลือกได้ทีละ 1) (edge: EC-01 / BR-002 / PARENT_XOR_VIOLATION)
- group: สร้างตำแหน่ง · ความสำคัญ: สูง · trace: AT-04 / BR-002 / EC-01 / err PARENT_XOR_VIOLATION
- Setup: role=manager · seed=R-A01, A-FM · files=—
- Start: OPEN app → เปิด loc-form (จาก R-A01)
- ชุดข้อมูล: —
- ผ่านเมื่อ: เลือก rack แล้ว area ถูกเคลียร์ (และในทางกลับกัน) — เลือกทั้งคู่พร้อมกันไม่ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK การ์ด **ใต้ชั้นวาง (Rack)** → เลือก `R-A01` | — | การ์ด Rack is-sel; picker rack = R-A01 | ☐ |
| 2 | CLICK การ์ด **ใต้พื้นที่ (Area)** | — | การ์ด Area กลายเป็น is-sel + การ์ด Rack เลิก selected + **rack_id ถูกเคลียร์** (เหลือ parent เดียว — XOR) | ☐ |
| 3 | CLICK การ์ด **ใต้ชั้นวาง (Rack)** อีกครั้ง | — | สลับกลับ Rack + area_id ถูกเคลียร์ (ยืนยันเลือกได้ทีละ 1 เท่านั้น) | ☐ |

#### TC-L08 — step 1 ไม่กรอกรหัส + ปิด drawer ด้วย Esc (negative + UX)
- group: สร้างตำแหน่ง · ความสำคัญ: กลาง · trace: MISSING_REQUIRED / UX Esc chain
- Setup: role=manager · seed=R-A01 · files=—
- Start: OPEN app → เปิด loc-form (จาก R-A01)
- ชุดข้อมูล: —
- ผ่านเมื่อ: กรอกรหัสว่าง → error "กรุณากรอกรหัสตำแหน่ง"; Esc ปิด drawer

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เลือก parent rack `R-A01` (เว้นรหัสว่าง) → พยายามไป step 2 / CLICK บันทึก | — | error **กรุณากรอกรหัสตำแหน่ง** + toast **กรุณากรอกข้อมูลให้ครบถ้วน** | ☐ |
| 2 | PRESS Esc | — | drawer ปิด (`state.drawer` เคลียร์) กลับสู่ List | ☐ |

---

### Group B — Bulk Generate

#### TC-B01 — bulk preview + submit atomic (happy, AT-05 / BR-015)
- group: Bulk Generate · ความสำคัญ: สูง · trace: AT-05 / S-05 / BR-015 / event location.created(bulk)
- Setup: role=manager · seed=A-AISLE-A (ไม่มี R-NEW-1/2) · files=—
- Start: OPEN app → drill WH-01 → Z-STG → A-AISLE-A (sub-tab ชั้นวาง) → CLICK ปุ่ม **สร้างจำนวนมาก**
- ชุดข้อมูล: BULK-OK
- ผ่านเมื่อ: preview box แสดงจำนวน + toast `สร้าง {N} ชั้นวาง × {M} ตำแหน่งสำเร็จ (atomic)`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สร้างจำนวนมาก** | — | drawer bulk เปิด หัวข้อ **สร้างจำนวนมาก (Bulk Generate)** | ☐ |
| 2 | เลือก **target_area** + TYPE **รูปแบบรหัสชั้นวาง** `R-NEW-{n}` + **จำนวนชั้นวาง** `2` | BULK-OK | ค่าปรากฏ (hint "{n} = ลำดับชั้นวาง") | ☐ |
| 3 | TYPE **รูปแบบรหัสตำแหน่ง** `{rack}-R{r}-C{c}-L{l}` + rows `2` cols `2` levels `1` + ความจุ `2` | BULK-OK | ค่าปรากฏ | ☐ |
| 4 | VERIFY **preview box** | — | แสดง **จะสร้างทั้งหมด** = `2 ชั้นวาง × 4 = 8` (2×2×1=4 ต่อชั้นวาง) — ไม่มี collision box | ☐ |
| 5 | CLICK ปุ่ม **บันทึก** | — | drawer ปิด + toast **สร้าง 2 ชั้นวาง × 4 ตำแหน่งสำเร็จ (atomic)** | ☐ |

#### TC-B02 — bulk collision → block ทั้งชุด (negative edge: EC-06 / BULK_COLLISION / BULK_TEMPLATE_INVALID)
- group: Bulk Generate · ความสำคัญ: สูง · trace: AT-05 / BR-015 / EC-06 / err BULK_COLLISION, BULK_TEMPLATE_INVALID
- Setup: role=manager · seed=A-AISLE-A มี R-A01/R-A02 อยู่แล้ว · files=—
- Start: OPEN app → drill ถึง A-AISLE-A → CLICK **สร้างจำนวนมาก**
- ชุดข้อมูล: BULK-COLLIDE
- ผ่านเมื่อ: collision box แสดง + สร้างไม่ได้ (atomic, ไม่มี partial commit)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างจำนวนมาก** → เลือก target_area `A-AISLE-A` | BULK-COLLIDE | drawer bulk เปิด | ☐ |
| 2 | TYPE **รูปแบบรหัสชั้นวาง** `R-A0{n}` + **จำนวนชั้นวาง** `2` (ชนกับ R-A01/R-A02) + ความจุ `2` | BULK-COLLIDE | ปรากฏ collision box **พบรหัสชน 2 รายการ — การสร้างถูกบล็อก (atomic ไม่มี partial commit):** + list `R-A01, R-A02` | ☐ |
| 3 | CLICK ปุ่ม **บันทึก** | — | สร้างไม่ได้ (ถูกบล็อก) — ไม่มีตำแหน่งใดถูกสร้าง (all-or-nothing) | ☐ |

#### TC-B03 — bulk ความจุ = 0 (negative, CAPACITY_INVALID)
- group: Bulk Generate · ความสำคัญ: กลาง · trace: BR-006 / err CAPACITY_INVALID
- Setup: role=manager · seed=A-AISLE-A · files=—
- Start: OPEN app → drill ถึง A-AISLE-A → CLICK **สร้างจำนวนมาก**
- ชุดข้อมูล: BULK-CAP0
- ผ่านเมื่อ: toast "ความจุต้องมากกว่า 0"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | กรอกฟิลด์ bulk ตาม BULK-CAP0 (ความจุ `0`) | BULK-CAP0 | ค่าปรากฏ | ☐ |
| 2 | CLICK ปุ่ม **บันทึก** | — | สร้างไม่ได้ + toast **ความจุต้องมากกว่า 0** | ☐ |

#### TC-B04 — preview จำนวน scale ใหญ่ (edge: EC-17 soft cap) `[AI-DEFAULT]`
- group: Bulk Generate · ความสำคัญ: กลาง · trace: EC-17 (OQ-5, `[AI-DEFAULT]` soft cap ~500) `[AI-DEFAULT]`
- Setup: role=manager · seed=A-AISLE-A · files=—
- Start: OPEN app → drill ถึง A-AISLE-A → CLICK **สร้างจำนวนมาก**
- ชุดข้อมูล: (รูปแบบชั้นวาง `R-BIG-{n}` จำนวน `10` · locPat + rows `10` cols `10` levels `5` · ความจุ `2`)
- ผ่านเมื่อ: preview box คำนวณ total ถูกต้อง (สังเกตค่า; prototype ยังไม่มี hard cap — OQ-5)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | กรอก bulk: ชั้นวาง `10`, rows `10` cols `10` levels `5` | — | ค่าปรากฏ | ☐ |
| 2 | VERIFY preview box **จะสร้างทั้งหมด** | — | แสดง `10 ชั้นวาง × 500 = 5000` (10×10×5=500 ต่อชั้นวาง) — บันทึก note: ไม่มี cap warning ใน prototype (OQ-5 confirm perf) `[AI-DEFAULT]` | ☐ |

---

### Group ST — เปลี่ยนสถานะ / activate / block

#### TC-ST01 — activate ตำแหน่งไม่มี barcode → block (negative edge: EC-11 / BR-014 / BARCODE_REQUIRED)
- group: เปลี่ยนสถานะ · ความสำคัญ: สูง · trace: AT-08 / S-08 / BR-014 / EC-11 / err BARCODE_REQUIRED
- Setup: role=manager · seed=L006 PACK-02 inactive ไม่มี barcode (ใต้ A-PACK) · files=—
- Start: OPEN app → drill WH-01 → Z-OUTBOUND → A-PACK (ตำแหน่งใต้พื้นที่) → คลิกแถว `PACK-02` เปิด view-loc
- ชุดข้อมูล: —
- ผ่านเมื่อ: activate ไม่ได้ + toast "ต้องเพิ่มบาร์โค้ดก่อนถึงจะเปิดใช้งานตำแหน่งได้"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถวตำแหน่ง **PACK-02** | — | drawer view-loc เปิด (tab **ภาพรวม**); pill สถานะ = **ปิดใช้** | ☐ |
| 2 | VERIFY inline-warn ใน tab ภาพรวม | — | ข้อความ **ตำแหน่งนี้ยังไม่มีบาร์โค้ด จึงยังเปิดใช้งานไม่ได้ — เพิ่มบาร์โค้ดก่อน แล้วปุ่มเปิดใช้งานจะกดได้** | ☐ |
| 3 | CLICK ปุ่ม **เปิดใช้งาน** (ถ้ากดได้) | — | toast **ต้องเพิ่มบาร์โค้ดก่อนถึงจะเปิดใช้งานตำแหน่งได้** + สถานะยังเป็น **ปิดใช้** (ไม่เปลี่ยน) | ☐ |

#### TC-ST02 — เพิ่ม barcode แล้ว activate ได้ (happy, BR-014 positive)
- group: เปลี่ยนสถานะ · ความสำคัญ: สูง · trace: §6.3 edit / BR-014 / event location.updated
- Setup: role=manager · seed=L006 PACK-02 inactive · files=—
- Start: OPEN app → drill ถึง A-PACK → คลิกแถว `PACK-02`
- ชุดข้อมูล: (barcode `8850009000099`)
- ผ่านเมื่อ: หลังเพิ่ม barcode + activate → toast "เปลี่ยนสถานะเป็น \"ใช้งาน\" แล้ว"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไอคอน **แก้ไข** ท้ายแถว `PACK-02` (หรือปุ่มแก้ไขใน view drawer) | — | loc-form (แก้ไข) เปิด | ☐ |
| 2 | ไป step 2 → TYPE **บาร์โค้ด** = `8850009000099` → CLICK **บันทึก** | — | drawer ปิด + toast **บันทึกการแก้ไขแล้ว** | ☐ |
| 3 | CLICK แถว `PACK-02` → CLICK ปุ่ม **เปิดใช้งาน** | — | toast **เปลี่ยนสถานะเป็น "ใช้งาน" แล้ว** + pill = **ใช้งาน** | ☐ |

#### TC-ST03 — block ไม่ระบุเหตุผล (negative, BLOCK_REASON_REQUIRED / BR-013)
- group: เปลี่ยนสถานะ · ความสำคัญ: สูง · trace: AT-08 / S-08 / BR-013 / err BLOCK_REASON_REQUIRED
- Setup: role=manager · seed=L010 DMG-01 active (A-HOLD) · files=—
- Start: OPEN app → drill WH-01 → Z-QC → A-HOLD → คลิกแถว `DMG-01`
- ชุดข้อมูล: —
- ผ่านเมื่อ: modal block เปิด + เว้นเหตุผล → toast "ระบุเหตุผลที่บล็อก"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว **DMG-01** → CLICK ปุ่ม **บล็อก** | — | modal (`state.modal.type='block'`) เปิด หัวข้อ **บล็อกตำแหน่ง**, ช่อง **เหตุผลที่บล็อก** (มี * required) | ☐ |
| 2 | CLICK ปุ่ม **บล็อก** ใน modal (เว้นเหตุผลว่าง) | — | modal ไม่ปิด + toast **ระบุเหตุผลที่บล็อก** | ☐ |

#### TC-ST04 — block พร้อมเหตุผล + audit (happy, BR-013)
- group: เปลี่ยนสถานะ · ความสำคัญ: สูง · trace: AT-08 / BR-013 / event location.blocked / WORM audit
- Setup: role=manager · seed=L010 DMG-01 active · files=—
- Start: OPEN app → drill ถึง A-HOLD → คลิกแถว `DMG-01`
- ชุดข้อมูล: BLOCK-REASON
- ผ่านเมื่อ: toast "บล็อกตำแหน่งแล้ว" + pill = บล็อก + audit บันทึก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว **DMG-01** → CLICK ปุ่ม **บล็อก** | — | modal block เปิด | ☐ |
| 2 | TYPE ช่อง **เหตุผลที่บล็อก** | BLOCK-REASON | `รอซ่อมคานชั้นวาง` | ☐ |
| 3 | CLICK ปุ่ม **บล็อก** ใน modal | — | modal ปิด + toast **บล็อกตำแหน่งแล้ว** | ☐ |
| 4 | CLICK แถว `DMG-01` → CLICK tab **ประวัติ** | — | pill สถานะ = **บล็อก**; tab ประวัติ (WORM audit) มีรายการ **บล็อกตำแหน่ง** ล่าสุด (detail มีเหตุผล) | ☐ |

#### TC-ST05 — เปลี่ยนสถานะ frozen/maintenance/full (happy, status machine)
- group: เปลี่ยนสถานะ · ความสำคัญ: กลาง · trace: §6.7 status machine
- Setup: role=manager · seed=L010 DMG-01 active · files=—
- Start: OPEN app → drill ถึง A-HOLD → คลิกแถว `DMG-01`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เปลี่ยนเป็นสถานะที่อนุญาต → toast "เปลี่ยนสถานะเป็น \"{label}\" แล้ว"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว **DMG-01** → เลือก action เปลี่ยนสถานะ (เช่น frozen/maintenance/full ตามปุ่มที่มีใน status-actions) | — | toast **เปลี่ยนสถานะเป็น "แช่แข็ง" แล้ว** (หรือ label ตามที่เลือก: ซ่อมบำรุง/เต็ม) | ☐ |
| 2 | VERIFY pill สถานะ | — | pill = สถานะใหม่ (color-code ตาม D10) | ☐ |

#### TC-ST06 — decommissioned เป็น terminal (edge: status machine — illegal transition)
- group: เปลี่ยนสถานะ · ความสำคัญ: กลาง · trace: §6.7 / BR-011 (terminal)
- Setup: role=manager · seed=ตำแหน่งที่ decommission แล้ว (สร้างจาก TC-AC04 หรือ decommission L010 ก่อน) · files=—
- Start: OPEN app → drill ถึงตำแหน่งที่ decommissioned
- ชุดข้อมูล: —
- ผ่านเมื่อ: ตำแหน่ง decommissioned ไม่มีปุ่มเปลี่ยนสถานะ/ปลดระวางอีก (terminal)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถวตำแหน่งสถานะ **ปลดระวาง** → เปิด view-loc | — | pill = **ปลดระวาง** | ☐ |
| 2 | VERIFY แถบ action / ปุ่มปลดระวาง | — | ไม่มีปุ่มปลดระวางซ้ำ (row action decommission ถูกซ่อนเมื่อ status='decommissioned'); ไม่มี transition ออกจาก terminal | ☐ |

---

### Group AC — จัดเก็บ node / ปลดระวาง location / reparent

#### TC-AC01 — archive node ที่มีลูก active → block (negative edge: EC-03 / BR-005 / HAS_ACTIVE_CHILDREN)
- group: จัดเก็บ node · ความสำคัญ: สูง · trace: AT-06 / S-06 / BR-005 / EC-03 / err HAS_ACTIVE_CHILDREN
- Setup: role=manager · seed=WH-01 มีโซน active · files=—
- Start: OPEN app (ระดับคลัง)
- ชุดข้อมูล: —
- ผ่านเมื่อ: modal danger + block "จัดเก็บไม่ได้ — ยังมีรายการลูกใช้งานอยู่ {n} รายการ"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไอคอน **จัดเก็บ** (archive) ท้ายแถว `WH-01` | — | modal (`state.modal.type='delete-node'`) เปิด แบบ **danger** หัวข้อ **จัดเก็บคลังไม่ได้** | ☐ |
| 2 | VERIFY กล่องข้อความ | — | **จัดเก็บไม่ได้ — ยังมีรายการลูกใช้งานอยู่ {n} รายการ** (referential-safe · BR-005) — ไม่มีปุ่มยืนยันจัดเก็บ | ☐ |
| 3 | VERIFY แถว `WH-01` หลังปิด modal | — | สถานะยังเป็น **ใช้งาน** (ไม่ถูกจัดเก็บ) | ☐ |

#### TC-AC02 — archive node ไม่มีลูก active → success (soft archive) (happy, BR-011 / no hard delete)
- group: จัดเก็บ node · ความสำคัญ: สูง · trace: AT-06 / S-06 / BR-005, BR-011 / D11 / WORM audit
- Setup: role=manager · seed=สร้าง node ใหม่ที่ไม่มีลูก (เช่น สร้าง Rack ว่าง `R-TEST` ตาม TC-RK01) · files=—
- Start: OPEN app → drill ถึงพื้นที่ที่มี rack ว่าง (ไม่มีตำแหน่ง)
- ชุดข้อมูล: —
- ผ่านเมื่อ: confirm → toast "จัดเก็บชั้นวางแล้ว" + status=จัดเก็บแล้ว (record ยังอยู่ = soft)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไอคอน **จัดเก็บ** ท้ายแถว rack ว่าง (ไม่มีตำแหน่ง) | — | modal **warning** (ไม่ใช่ danger) หัวข้อ **จัดเก็บชั้นวาง**; note "…จะถูกตั้งเป็น **จัดเก็บแล้ว** และเก็บประวัติไว้ (soft — ไม่ลบถาวร)" | ☐ |
| 2 | CLICK ปุ่ม **จัดเก็บ** ใน modal | — | modal ปิด + toast **จัดเก็บชั้นวางแล้ว** | ☐ |
| 3 | VERIFY record | — | แถวไม่ถูกลบถาวร — สถานะ = **จัดเก็บแล้ว** (soft archive, ยังมีในระบบ ตาม D11/GC#7) | ☐ |

#### TC-AC03 — decommission location ที่มีสต็อก → block (negative edge: EC-04 / BR-010 / DECOMMISSION_STOCK_NOT_EMPTY)
- group: ปลดระวาง · ความสำคัญ: สูง · trace: AT-07 / S-07 / BR-010 / EC-04 / err DECOMMISSION_STOCK_NOT_EMPTY
- Setup: role=manager · seed=L003 FM-PF-01 hasStock=true (A-FM) · files=—
- Start: OPEN app → drill WH-01 → Z-STG → A-FM (ตำแหน่งใต้พื้นที่) → คลิกแถว `FM-PF-01`
- ชุดข้อมูล: —
- ผ่านเมื่อ: modal danger + block "ต้องย้ายสต็อกออกก่อน…(BR-010)"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไอคอน **ปลดระวาง** (archive-x) ท้ายแถว `FM-PF-01` | — | modal (`state.modal.type='decommission'`) แบบ **danger** หัวข้อ **ปลดระวางไม่ได้** | ☐ |
| 2 | VERIFY กล่องข้อความ | — | **ต้องย้ายสต็อกออกก่อน** + "ตำแหน่งนี้ยังมีสต็อกอยู่ — ต้องย้ายสต็อกออก (stock = 0) ก่อนปลดระวาง (BR-010)" — ไม่มีปุ่มยืนยัน | ☐ |
| 3 | VERIFY สถานะ `FM-PF-01` | — | ยังเป็น **ใช้งาน** (ไม่ถูกปลดระวาง) | ☐ |

#### TC-AC04 — decommission location stock=0 → success (happy, BR-010/BR-011)
- group: ปลดระวาง · ความสำคัญ: สูง · trace: AT-07 / S-07 / BR-010, BR-011 / D11 / event location.decommissioned / WORM
- Setup: role=manager · seed=L010 DMG-01 active, hasStock=false (A-HOLD) · files=—
- Start: OPEN app → drill WH-01 → Z-QC → A-HOLD → คลิกแถว `DMG-01`
- ชุดข้อมูล: —
- ผ่านเมื่อ: confirm → toast "ปลดระวางตำแหน่งแล้ว" + pill=ปลดระวาง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไอคอน **ปลดระวาง** ท้ายแถว `DMG-01` | — | modal **warning** หัวข้อ **ปลดระวางตำแหน่ง**; note "ตำแหน่งจะถูกตั้งเป็น **decommissioned** และเก็บประวัติไว้ (soft — ไม่ลบถาวร)" | ☐ |
| 2 | CLICK ปุ่ม **ปลดระวาง** ใน modal | — | WAIT ~0.5s → modal ปิด + toast **ปลดระวางตำแหน่งแล้ว** | ☐ |
| 3 | VERIFY แถว `DMG-01` + tab ประวัติ | — | pill = **ปลดระวาง** (record ยังอยู่ = soft); ประวัติมีรายการ **ปลดระวางตำแหน่ง** (active → decommissioned) | ☐ |

#### TC-AC05 — reparent location ที่มีสต็อก → block (negative edge: EC-05 / BR-012 / REPARENT_STOCK_NOT_EMPTY)
- group: ปลดระวาง/reparent · ความสำคัญ: สูง · trace: §6.4 / BR-012 / EC-05 / err REPARENT_STOCK_NOT_EMPTY
- Setup: role=manager · seed=L003 FM-PF-01 hasStock=true (parent=A-FM) + area/rack อื่นให้ย้าย · files=—
- Start: OPEN app → drill ถึง A-FM → คลิกไอคอนแก้ไข `FM-PF-01`
- ชุดข้อมูล: —
- ผ่านเมื่อ: เปลี่ยน parent ไม่ได้ + toast "ต้องย้ายสต็อกออกก่อนย้ายตำแหน่ง (stock = 0)"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไอคอน **แก้ไข** ท้ายแถว `FM-PF-01` | — | loc-form (แก้ไข) เปิด, parent เดิม = A-FM | ☐ |
| 2 | เปลี่ยน parent (เช่นเลือก rack อื่น หรือ area อื่น ที่ต่างจากเดิม) → CLICK **บันทึก** | — | บันทึกไม่ได้ + error ที่ parent + toast **ต้องย้ายสต็อกออกก่อนย้ายตำแหน่ง (stock = 0)** | ☐ |

#### TC-AC06 — archive node ที่มีลูกแต่ลูก archived หมด → ไม่ block (edge: EC-16)
- group: จัดเก็บ node · ความสำคัญ: กลาง · trace: EC-16 (childCount นับ active only)
- Setup: role=manager · seed=node ที่ลูกทั้งหมด archived/decommissioned (เตรียมโดย archive ลูกก่อน) · files=—
- Start: OPEN app → drill ถึง node นั้น
- ชุดข้อมูล: —
- ผ่านเมื่อ: archive ได้ (ไม่ถูก block) เพราะไม่มีลูก active

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เตรียม: จัดเก็บ/ปลดระวาง ลูกทั้งหมดของ node ให้เหลือ 0 active | — | ลูก active = 0 | ☐ |
| 2 | CLICK ไอคอน **จัดเก็บ** ที่ node นั้น | — | modal **warning** (ไม่ใช่ danger block) — childCount นับเฉพาะ active = 0 | ☐ |
| 3 | CLICK ปุ่ม **จัดเก็บ** ใน modal | — | toast **จัดเก็บ{ระดับ}แล้ว** (สำเร็จ — archived children ไม่ block) | ☐ |

---

### Group P — สิทธิ์ (RBAC · D8/BR-016)

> เปลี่ยน role ผ่าน console `setRole('<role>')` เท่านั้น (ไม่มี UI switcher — D15).

#### TC-P01 — Operator: ปุ่มสร้าง/bulk disabled + tooltip (permission, EC-12 / AT-09 / S-09)
- group: สิทธิ์ · ความสำคัญ: สูง · trace: AT-09 / S-09 / BR-016 / EC-12
- Setup: role ตั้งเป็น operator ผ่าน console `setRole('operator')` · seed=— · files=—
- Start: OPEN app → console: `setRole('operator')`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ปุ่มสร้าง disabled + tooltip "บทบาทนี้ไม่มีสิทธิ์สร้าง (ดูอย่างเดียว)"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | PRESS console → พิมพ์ `setRole('operator')` | — | หน้า re-render (role=operator) | ☐ |
| 2 | VERIFY ปุ่ม **สร้างคลัง** | — | ปุ่ม disabled (is-disabled) + hover tooltip **บทบาทนี้ไม่มีสิทธิ์สร้าง (ดูอย่างเดียว)** | ☐ |
| 3 | VERIFY ปุ่ม **สร้างจำนวนมาก** (ระดับที่มี bulk) | — | disabled + tooltip **ไม่มีสิทธิ์** | ☐ |

#### TC-P02 — Operator: ไม่มีปุ่ม archive/decommission + แก้ไข disabled (permission, EC-12)
- group: สิทธิ์ · ความสำคัญ: สูง · trace: AT-09 / BR-016 / EC-12
- Setup: role=operator (`setRole('operator')`) · seed=WH-01, ตำแหน่งใด ๆ · files=—
- Start: OPEN app → console `setRole('operator')`
- ชุดข้อมูล: —
- ผ่านเมื่อ: row action archive/decommission disabled; แก้ไข disabled + tooltip

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY row action ของแถว `WH-01` | — | ไอคอน **แก้ไข** disabled + tooltip **ไม่มีสิทธิ์แก้ไข**; ไอคอน **จัดเก็บ** disabled + tooltip **จัดเก็บได้เฉพาะผู้จัดการ/ผู้ดูแลระบบ** | ☐ |
| 2 | drill ถึงตำแหน่ง → VERIFY row action location | — | ไอคอน **ปลดระวาง** disabled + tooltip **ปลดระวางได้เฉพาะผู้จัดการ/ผู้ดูแลระบบ** | ☐ |

#### TC-P03 — Supervisor: สร้าง/แก้ไข ได้ (permission allow)
- group: สิทธิ์ · ความสำคัญ: กลาง · trace: BR-016 (create=supervisor allow)
- Setup: role=supervisor (`setRole('supervisor')`) · seed=— · files=—
- Start: OPEN app → console `setRole('supervisor')`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ปุ่มสร้างใช้งานได้ (ไม่ disabled)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | console `setRole('supervisor')` → VERIFY ปุ่ม **สร้างคลัง** | — | ปุ่มกดได้ (ไม่ disabled, ไม่มี tooltip ห้าม) | ☐ |
| 2 | VERIFY ไอคอน **แก้ไข** ท้ายแถว | — | กดได้ (create=true) | ☐ |

#### TC-P04 — Supervisor: จัดเก็บ/ปลดระวาง ถูกปฏิเสธ (permission deny, EC-13 / SoD / FORBIDDEN_ROLE)
- group: สิทธิ์ · ความสำคัญ: สูง · trace: BR-016 / EC-13 / err FORBIDDEN_ROLE (API)
- Setup: role=supervisor (`setRole('supervisor')`) · seed=WH-01, ตำแหน่ง · files=—
- Start: OPEN app → console `setRole('supervisor')`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไอคอนจัดเก็บ/ปลดระวาง disabled + tooltip

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ไอคอน **จัดเก็บ** ท้ายแถว `WH-01` | — | disabled + tooltip **จัดเก็บได้เฉพาะผู้จัดการ/ผู้ดูแลระบบ** (SoD; API → 403 FORBIDDEN_ROLE) | ☐ |
| 2 | drill ถึงตำแหน่ง → VERIFY ไอคอน **ปลดระวาง** | — | disabled + tooltip **ปลดระวางได้เฉพาะผู้จัดการ/ผู้ดูแลระบบ** | ☐ |

#### TC-P05 — Inventory Controller: เปลี่ยนสถานะได้ แต่สร้างไม่ได้ (permission mixed)
- group: สิทธิ์ · ความสำคัญ: สูง · trace: BR-016 (status allow, create deny) / D8
- Setup: role=controller (`setRole('controller')`) · seed=ตำแหน่ง active · files=—
- Start: OPEN app → console `setRole('controller')`
- ชุดข้อมูล: —
- ผ่านเมื่อ: create disabled; ปุ่มเปลี่ยนสถานะ (block/frozen) ใช้งานได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | console `setRole('controller')` → VERIFY ปุ่ม **สร้างคลัง** | — | disabled + tooltip **บทบาทนี้ไม่มีสิทธิ์สร้าง (ดูอย่างเดียว)** | ☐ |
| 2 | drill ถึงตำแหน่ง active → เปิด view-loc → VERIFY status-actions | — | มีปุ่มเปลี่ยนสถานะ เช่น **บล็อก** (status=true สำหรับ controller) — ไม่ขึ้นข้อความ "บทบาทนี้ไม่มีสิทธิ์เปลี่ยนสถานะ" | ☐ |

#### TC-P06 — Inventory Controller: จัดเก็บ/ปลดระวาง ถูกปฏิเสธ (permission deny, EC-13)
- group: สิทธิ์ · ความสำคัญ: กลาง · trace: BR-016 / EC-13
- Setup: role=controller (`setRole('controller')`) · seed=WH-01, ตำแหน่ง · files=—
- Start: OPEN app → console `setRole('controller')`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ไอคอนจัดเก็บ/ปลดระวาง disabled

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ไอคอน **จัดเก็บ** ท้ายแถว node | — | disabled + tooltip **จัดเก็บได้เฉพาะผู้จัดการ/ผู้ดูแลระบบ** | ☐ |
| 2 | VERIFY ไอคอน **ปลดระวาง** ท้ายแถวตำแหน่ง | — | disabled + tooltip **ปลดระวางได้เฉพาะผู้จัดการ/ผู้ดูแลระบบ** | ☐ |

#### TC-P07 — Warehouse Manager: สิทธิ์เต็ม (permission allow all)
- group: สิทธิ์ · ความสำคัญ: กลาง · trace: BR-016 (manager full)
- Setup: role=manager (default) · seed=WH-01 · files=—
- Start: OPEN app (role=manager)
- ชุดข้อมูล: —
- ผ่านเมื่อ: create/edit/status/archive/decommission ทุกปุ่มกดได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่ม **สร้างคลัง** + ไอคอน **แก้ไข**/**จัดเก็บ** ท้ายแถว | — | ทุกปุ่มกดได้ (ไม่มี disabled/tooltip ห้าม) | ☐ |
| 2 | drill ถึงตำแหน่ง → VERIFY ไอคอน **ปลดระวาง** + ปุ่มเปลี่ยนสถานะ | — | กดได้ทั้งหมด | ☐ |

#### TC-P08 — Admin: สิทธิ์เต็ม (permission allow all)
- group: สิทธิ์ · ความสำคัญ: กลาง · trace: BR-016 (admin full)
- Setup: role=admin (`setRole('admin')`) · seed=WH-01 · files=—
- Start: OPEN app → console `setRole('admin')`
- ชุดข้อมูล: —
- ผ่านเมื่อ: create/edit/status/del ทุกปุ่มกดได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | console `setRole('admin')` → VERIFY ปุ่ม **สร้างคลัง** + ไอคอน **จัดเก็บ** | — | กดได้ทั้งหมด (del=admin allow) | ☐ |
| 2 | drill ถึงตำแหน่ง → VERIFY ไอคอน **ปลดระวาง** | — | กดได้ | ☐ |

#### TC-P09 — Operator: เปลี่ยนสถานะไม่ได้ (permission deny, status≠operator)
- group: สิทธิ์ · ความสำคัญ: กลาง · trace: BR-016 (status deny operator)
- Setup: role=operator (`setRole('operator')`) · seed=ตำแหน่ง active · files=—
- Start: OPEN app → console `setRole('operator')`
- ชุดข้อมูล: —
- ผ่านเมื่อ: ใน view-loc ไม่มีปุ่มเปลี่ยนสถานะ + ข้อความ "บทบาทนี้ไม่มีสิทธิ์เปลี่ยนสถานะ"

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | console `setRole('operator')` → drill ถึงตำแหน่ง active → เปิด view-loc | — | drawer view-loc เปิด | ☐ |
| 2 | VERIFY แถบ status-actions | — | ไม่มีปุ่มเปลี่ยนสถานะ + ข้อความ **บทบาทนี้ไม่มีสิทธิ์เปลี่ยนสถานะ** | ☐ |

---

### Group V — View / dual-view / full_path

#### TC-V01 — View Node drawer (fields + full path + child stats) (happy, P-06)
- group: View · ความสำคัญ: กลาง · trace: 01_UI P-06 / WHB-API-06
- Setup: role=manager · seed=WH-01 · files=—
- Start: OPEN app (ระดับคลัง)
- ชุดข้อมูล: —
- ผ่านเมื่อ: drawer view-node แสดง fields + full path + chip สถิติลูก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ไอคอน **รายละเอียด** (panel-right-open) ท้ายแถว `WH-01` | — | drawer view-node เปิด แสดงข้อมูลคลัง WH-01 (code/ชื่อ/สาขา) + full path | ☐ |
| 2 | VERIFY child stat chips | — | มี chip นับจำนวนลูก (เช่น จำนวนโซน) คลิกได้เพื่อ drill | ☐ |

#### TC-V02 — View Location 3 tabs + status/type pill (happy, P-07 / D10)
- group: View · ความสำคัญ: กลาง · trace: 01_UI P-07 / D10 pill / WORM audit
- Setup: role=manager · seed=L001 A-01-R1-C1-L1 · files=—
- Start: OPEN app → drill ถึง L001 → คลิกแถว
- ชุดข้อมูล: —
- ผ่านเมื่อ: 3 tabs ทำงาน (ภาพรวม/ความจุ & flags/ประวัติ)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถวตำแหน่ง `A-01-R1-C1-L1` | — | drawer view-loc เปิด tab **ภาพรวม** (มี "มีสต็อก" flag); pill สถานะ = **ใช้งาน** (color-code), type pill = icon+label (ไม่ color-code) | ☐ |
| 2 | CLICK tab **ความจุ & flags** | — | แสดงความจุ + toggle flags (pickable/putawayable/…) | ☐ |
| 3 | CLICK tab **ประวัติ** | — | timeline WORM audit ("ประวัติการเปลี่ยนแปลง (WORM audit)") | ☐ |

#### TC-V03 — สลับ List ↔ Hierarchy Tree คง selection (happy, AT-10 / S-10 / D12)
- group: View · ความสำคัญ: สูง · trace: AT-10 / S-10 / D12 / BR-001
- Setup: role=manager · seed=WH-01 › Z-STORAGE · files=—
- Start: OPEN app (`state.view='list'`)
- ชุดข้อมูล: —
- ผ่านเมื่อ: เลือก node ใน Tree → สลับ List เห็น context เดิม

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY view switcher (segmented ใต้ header) | — | มี 2 ปุ่ม **มุมมองรายการ** / **มุมมองลำดับชั้น** | ☐ |
| 2 | CLICK **มุมมองลำดับชั้น** | — | `state.view='tree'` — tree pane ซ้าย (WH→Zone→Area→Rack collapsible) + node summary panel ขวา | ☐ |
| 3 | CLICK node `Z-STG` (Storage Zone) ใน tree | — | node summary panel ขวาแสดง Storage Zone (ชื่อ/code/full path/attribute + child chips) | ☐ |
| 4 | CLICK **มุมมองรายการ** | — | กลับ List และ context (selection `state.sel`) ยังชี้ที่ WH-01 › Storage Zone เดิม | ☐ |

#### TC-V04 — full_path format = ชื่อ (zone/area/rack) + code (WH/location), ไม่มีสาขา (edge: D15 / XT-04)
- group: View · ความสำคัญ: สูง · trace: XT-04 / D15 / LOCK D15
- Setup: role=manager · seed=L001 (WH-01 › Storage Zone › Aisle A › Rack A-01 › A-01-R1-C1-L1) · files=—
- Start: OPEN app → drill ถึง L001 → เปิด view-loc
- ชุดข้อมูล: —
- ผ่านเมื่อ: full path แสดงชื่อ zone/area/rack + code WH/location และ **ไม่มีชื่อสาขาใน path**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว `A-01-R1-C1-L1` → เปิด view-loc → หา Full Path | — | full path = `WH-01 › <ชื่อโซน> › <ชื่อพื้นที่> › <ชื่อชั้นวาง> › A-01-R1-C1-L1` (WH+location = code; zone/area/rack = ชื่อ) | ☐ |
| 2 | VERIFY ไม่มีสาขาใน path | — | **ไม่ปรากฏชื่อสาขา** (เช่น "สาขา 1 (บางนา)"/BR-01) ใน full path หรือ breadcrumb (D15) | ☐ |
| 3 | VERIFY breadcrumb drill (List) | — | "ทุกคลัง › WH-01 › <ชื่อโซน> › <ชื่อพื้นที่> › <ชื่อชั้นวาง>" — WH เป็น code, ระดับอื่นเป็นชื่อ, ไม่มีสาขา | ☐ |

#### TC-V05 — tree child chip → สลับกลับ List (happy)
- group: View · ความสำคัญ: ต่ำ · trace: P-02 chipToList
- Setup: role=manager · seed=WH-01 · files=—
- Start: OPEN app → CLICK **มุมมองลำดับชั้น** → เลือก node
- ชุดข้อมูล: —
- ผ่านเมื่อ: คลิก chip สถิติลูก → สลับไป List ที่ระดับลูกนั้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ใน Tree → เลือก `WH-01` → ใน node summary panel CLICK chip สถิติ (เช่น "โซน") | — | สลับไป `state.view='list'` ที่ระดับโซนของ WH-01 (chipToList) | ☐ |

---

### Group F — List filter / states / KPI

#### TC-F01 — branch filter (happy, D7/D8)
- group: List filter · ความสำคัญ: กลาง · trace: D7 filter / D8 (branch = UX only)
- Setup: role=manager · seed=WH-01(BR-01), WH-02(BR-02), WH-03(HQ) · files=—
- Start: OPEN app (ระดับคลัง)
- ชุดข้อมูล: —
- ผ่านเมื่อ: เลือก branch → ตารางแสดงเฉพาะคลังของสาขานั้น + KPI ปรับ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+จดจำนวนแถวคลังทั้งหมด | — | จด baseline: มี 3 คลัง (WH-01/02/03) | ☐ |
| 2 | CLICK branch filter (combobox) → เลือก `สาขา 2 (ลำพูน)` | — | ตารางเหลือเฉพาะ `WH-02` (คลังภาคเหนือ ลำพูน) | ☐ |
| 3 | VERIFY KPI tile **คลัง (Warehouse)** | — | ค่าลดลงเทียบ baseline (แสดงจำนวนตาม scope สาขาที่เลือก) | ☐ |

#### TC-F02 — type filter ที่ระดับตำแหน่ง (happy)
- group: List filter · ความสำคัญ: กลาง · trace: 01_UI filters
- Setup: role=manager · seed=A-FM มีหลายประเภทตำแหน่ง · files=—
- Start: OPEN app → drill ถึงระดับตำแหน่ง (A-FM)
- ชุดข้อมูล: —
- ผ่านเมื่อ: เลือก type filter → เหลือเฉพาะตำแหน่งประเภทนั้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | drill ถึงตำแหน่งใต้ A-FM → VERIFY มี filter ประเภท/สถานะ | — | ปรากฏ filter ที่ระดับ location | ☐ |
| 2 | เลือก type filter = `PICK_FACE` | — | ตารางเหลือเฉพาะตำแหน่งประเภท PICK_FACE (เช่น FM-PF-01/02) | ☐ |

#### TC-F03 — status filter (happy)
- group: List filter · ความสำคัญ: กลาง · trace: 01_UI filters
- Setup: role=manager · seed=ตำแหน่งหลายสถานะ · files=—
- Start: OPEN app → drill ถึงระดับตำแหน่ง
- ชุดข้อมูล: —
- ผ่านเมื่อ: เลือกสถานะ → กรองถูกต้อง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | drill ถึงตำแหน่ง → เลือก status filter = `เต็ม` (full) | — | ตารางเหลือเฉพาะตำแหน่งสถานะ **เต็ม** (เช่น FM-PF-02) | ☐ |
| 2 | รีเซ็ต filter | — | ตารางแสดงทุกสถานะเหมือนเดิม | ☐ |

#### TC-F04 — search (happy + filtered-empty)
- group: List filter · ความสำคัญ: กลาง · trace: 01_UI search / filtered-empty state
- Setup: role=manager · seed=WH-01/02/03 · files=—
- Start: OPEN app (ระดับคลัง)
- ชุดข้อมูล: —
- ผ่านเมื่อ: ค้นเจอ + ค้นไม่เจอแสดง empty

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE ช่องค้นหา = `WH-02` | — | ตารางเหลือเฉพาะ `WH-02` | ☐ |
| 2 | TYPE ช่องค้นหา = `ZZZ-ไม่มีจริง` | — | ตารางว่าง + empty state (filtered-empty) | ☐ |

#### TC-F05 — states: loading / empty / error (edge, NOT_FOUND)
- group: List states · ความสำคัญ: กลาง · trace: UI states / err NOT_FOUND (error state)
- Setup: role=manager · seed=— · files=—
- Start: OPEN app (refresh)
- ชุดข้อมูล: —
- ผ่านเมื่อ: สังเกต loading skeleton ตอนโหลด; error state มีข้อความ verbatim

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN app (refresh) → VERIFY ช่วงโหลด | — | เห็น loading skeleton ก่อนตารางแสดง (renderLoading) | ☐ |
| 2 | drill เข้าระดับที่ไม่มีข้อมูล (เช่นโซนที่ไม่มีพื้นที่) | — | empty state (Iron #39) — ข้อความ "ยังไม่มี{ระดับ}" + คำแนะนำ "เริ่มต้นด้วยการสร้าง…แรกของคุณ" (ถ้ามีสิทธิ์) | ☐ |
| 3 | VERIFY error state (ถ้า drill ไป ref ที่หาย — สังเกต desc) | — | ข้อความ **รายการที่คุณกำลังเจาะดูอาจถูกลบหรือย้ายไปแล้ว กรุณากลับไปที่รายการคลังทั้งหมด** (NOT_FOUND UI) | ☐ |

#### TC-F06 — KPI 5 tiles (happy, BR-001)
- group: KPI · ความสำคัญ: กลาง · trace: BR-001 / renderKpi
- Setup: role=manager · seed=default · files=—
- Start: OPEN app (ระดับคลัง)
- ชุดข้อมูล: —
- ผ่านเมื่อ: KPI แสดง 5 tile ตามลำดับระดับ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แถว KPI ใต้ view switcher | — | 5 tile: **คลัง (Warehouse)** · **โซน (Zone)** · **พื้นที่ (Area)** · **ชั้นวาง (Rack)** · **ตำแหน่ง** (ระดับ 5 = "ตำแหน่ง" ตาม D15) พร้อมตัวเลขนับ | ☐ |

---

### Group XT — Cross-Module (06_TESTS §6.9)

> Prototype ไม่มีหน้าโมดูลปลายทาง (Inventory/Picking) → เคสเหล่านี้ **(ต้อง simulate)**: ตรวจ event/audit/สถานะฝั่งต้นทางแทนผลปลายทาง.

#### TC-XT01 — decommission → no orphan stock + event (XT-01) (ต้อง simulate)
- group: Cross-module · ความสำคัญ: สูง · trace: XT-01 / BR-010 / event location.decommissioned
- Setup: role=manager · seed=ตำแหน่ง stock=0 (L010 DMG-01) + ตำแหน่ง hasStock (L003) · files=— · simulate: ตรวจ audit/console แทน Inventory จริง
- Start: OPEN app → drill ถึงตำแหน่ง
- ชุดข้อมูล: —
- ผ่านเมื่อ: decommission ทำได้เฉพาะ stock=0 (gate กัน orphan) + event/audit บันทึก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ปลดระวาง `L003` (hasStock) | — | ถูก block (ตาม TC-AC03) — กัน orphan stock ที่ปลายทาง | ☐ |
| 2 | ปลดระวาง `L010` (stock=0) | — | สำเร็จ + toast **ปลดระวางตำแหน่งแล้ว**; ประวัติ (WORM) บันทึก → downstream ควรได้ event `location.decommissioned` (simulate: ตรวจ audit entry) | ☐ |

#### TC-XT02 — reparent → path change / downstream re-read (XT-02 / EC-18) (ต้อง simulate)
- group: Cross-module · ความสำคัญ: กลาง · trace: XT-02 / EC-18 / event location.reparented
- Setup: role=manager · seed=ตำแหน่ง stock=0 ที่ย้าย parent ได้ · files=— · simulate: ตรวจ full_path ใหม่แทน downstream cache
- Start: OPEN app → drill ถึงตำแหน่ง stock=0 → แก้ไข
- ชุดข้อมูล: —
- ผ่านเมื่อ: ย้าย parent (stock=0) สำเร็จ → full_path recompute (event location.reparented)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+จด full_path เดิมของตำแหน่ง stock=0 | — | จดค่า path เดิมไว้อ้าง | ☐ |
| 2 | แก้ไขตำแหน่ง → เปลี่ยน parent เป็น rack/area อื่น → บันทึก | — | สำเร็จ (toast บันทึกการแก้ไขแล้ว) เพราะ stock=0 | ☐ |
| 3 | เปิด view-loc → VERIFY full_path | — | full_path **เปลี่ยนต่างจากค่าที่จดใน step 1** (recompute ตาม parent ใหม่) → downstream ต้อง re-read (EC-18, simulate) | ☐ |

#### TC-XT03 — block/frozen → picking/putaway gate (XT-03) (ต้อง simulate)
- group: Cross-module · ความสำคัญ: กลาง · trace: XT-03 / event location.blocked/frozen
- Setup: role=manager · seed=ตำแหน่ง active · files=— · simulate: prototype ไม่มีหน้า Picking → ตรวจสถานะ+audit
- Start: OPEN app → drill ถึงตำแหน่ง active
- ชุดข้อมูล: BLOCK-REASON
- ผ่านเมื่อ: block/frozen → status event ที่ downstream ใช้ gate หยิบ/วาง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | บล็อกตำแหน่ง active (พร้อมเหตุผล) | BLOCK-REASON | สถานะ = **บล็อก** + audit บันทึก → event `location.blocked` (simulate: Picking/Put Away ควรถูก gate) | ☐ |

#### TC-XT04 — full_path contract export (no branch, D15) (XT-04) (ต้อง simulate)
- group: Cross-module · ความสำคัญ: สูง · trace: XT-04 / D15 / contract
- Setup: role=manager · seed=L001 · files=—
- Start: OPEN app → drill ถึง L001 → view-loc
- ชุดข้อมูล: —
- ผ่านเมื่อ: contract = `location_id + full_path` โดย full_path = "WH code › zone name › area name › rack name › location code" ไม่มีสาขา

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิด view-loc `A-01-R1-C1-L1` → VERIFY full_path ที่จะ export | — | รูปแบบ = `WH-01 › <zone name> › <area name> › <rack name> › A-01-R1-C1-L1`; **ไม่มีสาขา** (ตรง 02_API §2.9 contract + D15) | ☐ |

---

### Group LK — Scope Lock verify

#### TC-LK01 — D3: branch_id อยู่บน warehouse เท่านั้น (LOCK verify)
- group: Scope Lock · ความสำคัญ: สูง · trace: LOCK D3
- Setup: role=manager · seed=— · files=—
- Start: OPEN app
- ชุดข้อมูล: —
- ผ่านเมื่อ: ฟอร์ม WH มีช่องสาขา; ฟอร์ม zone/area/rack ไม่มีช่องสาขา; ไม่มี company_id ที่ไหน

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปิดฟอร์ม **สร้างคลัง** → VERIFY ช่อง **สาขา** | — | มีช่องสาขา (required, Master Combobox) | ☐ |
| 2 | drill WH-01 → เปิดฟอร์ม **สร้างโซน** / **สร้างพื้นที่** / **สร้างชั้นวาง** | — | **ไม่มีช่องสาขา** และ **ไม่มีช่อง company/บริษัท** (สืบทอดผ่าน warehouse_id — D3) | ☐ |

#### TC-LK02 — D11/GC#7: ไม่มี hard delete ทุกระดับ (LOCK verify)
- group: Scope Lock · ความสำคัญ: สูง · trace: LOCK D11/GC#7 / BR-011
- Setup: role=manager · seed=— · files=—
- Start: OPEN app
- ชุดข้อมูล: —
- ผ่านเมื่อ: ทุก destructive = จัดเก็บ/ปลดระวาง (soft) ไม่มีคำว่า "ลบ" ถาวร; record คงอยู่หลัง action

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY microcopy ปุ่ม/tooltip destructive | — | ใช้คำ **จัดเก็บ** (node) / **ปลดระวาง** (location); ไม่มีปุ่ม "ลบ" ถาวร | ☐ |
| 2 | VERIFY modal จัดเก็บ/ปลดระวาง note | — | ระบุ "(soft — ไม่ลบถาวร)" + "เก็บประวัติไว้" (WORM) | ☐ |

#### TC-LK03 — D1/D14: canonical name & entry (LOCK verify)
- group: Scope Lock · ความสำคัญ: กลาง · trace: LOCK D1, D14
- Setup: role=manager · seed=— · files=—
- Start: OPEN app
- ชุดข้อมูล: —
- ผ่านเมื่อ: ชื่อ "คลังและตำแหน่ง" ปรากฏใน title/sidebar/breadcrumb/h1

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY title/sidebar/breadcrumb/h1 | — | tab title = "คลังและตำแหน่ง (Warehouse & Bin)"; sidebar active = **คลังและตำแหน่ง**; breadcrumb-current = **คลังและตำแหน่ง**; h1 = **คลังและตำแหน่ง (Warehouse & Bin)** | ☐ |

#### TC-LK04 — D15: ไม่มี role switcher บนจอ + branch ไม่อยู่ใน path (LOCK verify)
- group: Scope Lock · ความสำคัญ: สูง · trace: LOCK D15
- Setup: role=manager · seed=— · files=—
- Start: OPEN app
- ชุดข้อมูล: —
- ผ่านเมื่อ: header ไม่มีตัวสลับ role; path ไม่มีสาขา

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY header ขวาบน | — | **ไม่มี** ปุ่ม/dropdown สลับ role (มุมมองผู้จัดการคลัง ฯลฯ) — role มาจาก state/auth (D15/LD-10) | ☐ |
| 2 | VERIFY breadcrumb + full path (อ้าง TC-V04) | — | ไม่มีชื่อสาขาใน path ทุกจุด | ☐ |

#### TC-LK05 — D12: dual-view มีจริง (LOCK verify)
- group: Scope Lock · ความสำคัญ: กลาง · trace: LOCK D12 / BR-001
- Setup: role=manager · seed=— · files=—
- Start: OPEN app
- ชุดข้อมูล: —
- ผ่านเมื่อ: มี view switcher 2 มุมมอง + tree ทำงาน (NON-STANDARD approved)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY view switcher | — | มี **มุมมองรายการ** + **มุมมองลำดับชั้น** (dual-view, D12) | ☐ |
| 2 | CLICK **มุมมองลำดับชั้น** | — | tree pane + node summary panel ปรากฏ (5-level hierarchy) | ☐ |

---

## วิธีที่ agent รัน (Run protocol)

1. เปิดไฟล์ `01_HTML/WarehouseBin.html` ใน browser (ไม่ต้องมี server) — refresh ก่อนทุกเคสเพื่อ reset state (refresh-safe). role เริ่มต้น = `manager`, view = `list`, drill = root.
2. ทำตาม `Setup:` ของแต่ละเคสก่อน: ถ้า role ≠ manager ให้เปิด browser console แล้วสั่ง `setRole('<role>')` (state-driven — ไม่มี UI switcher, D15). ถ้าต้อง seed สถานะ (เช่น node ว่างสำหรับ archive) ให้เตรียมตาม step "เตรียม" ในเคส.
3. ทำ Action ทีละ step (ขึ้นต้น verb tag) แล้วตรวจ Expected ด้วยตา (ข้อความ/pill/toast/route-state ที่เห็น). ติ๊ก ☐ → pass/fail.
4. เคส **(ต้อง simulate)** (XT): prototype ไม่มีหน้าปลายทาง → ตรวจ event/audit/สถานะฝั่งต้นทางแทน; ถ้าตรวจ event ไม่ได้เลย → mark `blocked`.
5. toast หายเองใน ~3s — ใช้ WAIT จับ toast ก่อนมันหาย. modal decommission มี delay ~0.5s.
6. เคสที่ Expected เป็น delta (full_path เปลี่ยน, จำนวนแถวลด) — จดค่าตั้งต้นใน step แรกก่อนเทียบ (R17).
7. บันทึกผลกลับตาม schema ด้านล่าง — `evidence` = สิ่งที่เห็นจริงตอน fail (ข้อความ error/สถานะ/route-state ที่ค้าง).

---

## Coverage Audit

| หมวด | covered / total |
|---|---|
| FR / Acceptance (AT-01..10 + §6.2/6.3/6.4) | 13 / 13 |
| Business rules (BR-001..018) | 17 / 18 (BR-018 ข้าม — DEFERRED Phase 3) |
| Edge cases (EC-01..18) | 15 / 18 (EC-14, EC-15 ข้าม — ต้อง master/DB จริง; EC-18 ผ่าน simulate) |
| Error codes (17) | 17 / 17 (บาง code = simulate/UI-prevented) |
| Permission cells (5 roles × 3 actions) | 15 / 15 (ครอบ allow+deny ครบทุก role) |
| Cross-Module (XT-01..04) | 4 / 4 (simulate) |
| Scope Lock (LOCK D1/D3/D8/D11/D12/D14/D15) | 7 / 7 |
| Cross-cutting / states / events / KPI | ครบ (loading/empty/filtered-empty/error/KPI/audit/pill) |
| Stories (S-01..10) | 10 / 10 |

- Cross-Module (XT): 4/4
- Scope Lock (LOCK): 7/7
- **Manifest cross-check (FRD §0.12): ✅ 10/10 stories + BR-001..018 + EC-01..18 ทุกแถว map เข้า Ledger**

### ข้าม (พร้อมเหตุผล)
- **BR-018** `applyTypeDefaults` — DEFERRED Phase 3, schema-ready ไม่ implement ใน Phase 1 (05_RULES §5.6 / BRD §14.2). ห้ามสร้างเคส.
- **EC-14** soft-ref (branch/geo) code not-found `[AI-DEFAULT]` — prototype ใช้ mock ที่ code เจอเสมอ, ไม่มี UI จำลอง not-found; ทดสอบเมื่อต่อ Company/Geo master จริง (Phase 2, OQ-4).
- **EC-15** concurrent same-code `[AI-DEFAULT]` — single-client prototype จำลอง 2-user race ไม่ได้; uniqueness = DB-enforced ต้องทดสอบที่ API/DB layer (OQ-7).
- **Out-of-scope (นอกขอบเขตใบเซ็น — ห้ามสร้างเคส):** Geo Master CRUD, stock/on-hand management, DOA/approval workflow, company_id/multi-company, branch-scoped data permission (D8), default-location-per-warehouse (D9), type-driven auto default flags (Phase 3), role switcher UI (D15 — dead code).

---

## Result Report (schema)

```json
{
  "feature_id": "F-LOCATION-MASTER-001",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-A01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 70, "pass": 0, "fail": 0, "blocked": 0 }
}
```
> `evidence` = สิ่งที่ agent เห็นจริงตอน fail/blocked (ข้อความ toast/error จริง, pill สถานะที่ค้าง, `state.view`/drawer ที่ค้าง, full_path ที่แสดง). `note` = หมายเหตุ เช่น เคส `(ต้อง simulate)` ที่ตรวจ event ไม่ได้.
