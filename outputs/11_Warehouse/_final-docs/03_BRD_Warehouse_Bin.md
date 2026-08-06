# BRD — Warehouse & Bin (คลังและตำแหน่ง)

> เอกสาร Business Requirement · WF-01 · SOW3.2 · สร้างด้วย `brd-generator-full` v2.2 (Fresh Mode · HTML-first)
> Source of truth: `01_HTML/WarehouseBin.html` + Locked Decisions (`00_CONTEXT/DECISION_LOG.md`, `AI_DEFAULTS.md`, `COVERAGE_MAP.md`)

---

## 1. Document Info

| ฟิลด์ | ค่า |
|---|---|
| **BRD ID** | BRD-F-LOCATION-MASTER-001 |
| **Feature** | Warehouse & Bin (TH: **คลังและตำแหน่ง**) |
| **Feature ID** | F-LOCATION-MASTER-001 |
| **Module / Wave** | Warehouse · W3 (Central Plan node "Warehouse & Bin") |
| **ประเภท BRD** | New Feature |
| **Version** | 1.0 |
| **Status** | APPROVED |
| **Owner (BA)** | 2BSimple BA |
| **Stakeholders** | PM/BA (scope owner), Warehouse Manager, Inventory Controller, ทีม Dev |
| **วันที่** | 2026-08-06 |

### Changelog
- **v1.0 (2026-08-06):** Initial via `brd-generator-full` (Fresh Mode, HTML-first). สกัด Screen Inventory + entities + rules จาก `WarehouseBin.html` และผูกกับ Locked Decisions D1–D15 / AD-1–AD-9.

---

## 2. Business Context

### 2.1 ปัญหา / โอกาส
ระบบ ERP ต้องมี master ที่นิยาม "ที่เก็บของ" อย่างเป็นโครงสร้าง เพื่อให้โมดูล Inventory และกระบวนการรับ-จ่าย-ย้าย-นับสต็อกอ้างอิงตำแหน่งได้แม่นยำ ปัจจุบันยังไม่มี master ที่รองรับโครงสร้างจัดเก็บลึกหลายระดับ + flexible parent (บางของวางบนพื้น บางของวางในชั้นวาง) และยังไม่ผูกคลังกับสาขา (multi-branch)

### 2.2 เป้าหมาย business
- จัดโครงสร้างจัดเก็บครบ **5 ระดับ** ในหน้าจอเดียว: คลัง → โซน → พื้นที่ → ชั้นวาง → **ตำแหน่ง**
- ให้ทุกตำแหน่ง (location) มี identity + capacity + behavior + barcode ที่ downstream (Inventory/GR/Picking) นำไปอ้างได้
- ผูกคลังกับสาขา (branch) เพื่อรองรับ multi-branch และกรองดูรายสาขาได้
- ควบคุมวงจรชีวิตของ node/location แบบ soft (ไม่มี hard delete — เก็บประวัติ audit)

### 2.3 ตัวชี้วัดความสำเร็จ (บังคับวัดได้)

| ตัวชี้วัด | Baseline ปัจจุบัน | Target | วัดยังไง / จากไหน | วัดเมื่อไหร่ |
|---|---|---|---|---|
| % ตำแหน่งที่มี barcode ก่อน activate | ไม่มีระบบ (0 — ต้องเก็บ baseline ก่อน launch) | 100% ของ location `active` | นับ location.status=active ที่ barcode≠null / all active | รายเดือน |
| จำนวน location ที่ downstream อ้างได้ (full_path ครบ) | 0 | 100% ของ location ที่ไม่ decommissioned | export contract (location_id + full_path) | ต่อเนื่อง |
| เวลาเฉลี่ยในการตั้งค่าคลังใหม่ครบ 5 ระดับ | ไม่มี baseline (ต้องเก็บก่อน launch) | ลด ≥ 50% เทียบ manual ครั้งแรกหลัง launch | จับเวลาจาก audit (สร้าง WH → มี location แรก) | หลัง launch 1 เดือน |
| อัตราคลังที่ผูก branch ครบ (data quality) | ไม่มีระบบ (0) | 100% (branch_id required) | นับ warehouses ที่ branch_id≠null | ต่อเนื่อง (บังคับด้วย validation) |

### 2.4 ที่มา
Central Plan node "Warehouse & Bin" (Warehouse module, W3) · seed จาก legacy pack v2 (`_legacy/`) · regenerate HTML-first (D6)

---

## 3. Scope

### 3.1 In Scope
1. CRUD 5 entities: warehouses, zones, areas, racks, locations (ผ่าน UI เดียว)
2. Dual-view: **List (drill-down)** + **Hierarchy Tree** (D12 — NON-STANDARD approved deviation)
3. Warehouse ผูก **branch_id** (required, soft-ref) + ที่อยู่ geo cascade (province→district→subdistrict→postcode)
4. Zone temperature control (temp_controlled + min/max)
5. Area flexible-parent gate (`allows_direct`)
6. Rack grid (rows × cols × levels) สำหรับ bulk generate
7. Location: parent = rack XOR area, 10 ประเภท, capacity (uom + val>0), rotation, coords, behavior flags, mixing flags, 7-state status, barcode/QR
8. **Bulk Generate** ตำแหน่งจาก rack template (preview + collision check + atomic)
9. Soft lifecycle: node = **archive** (referential-safe), location = **decommission** (empty-before) + WORM audit
10. List: branch filter/column + type/status filter (location level) + KPI 5 ระดับ
11. RBAC role-only (5 roles) · delete/archive = Manager/Admin (SoD)

### 3.2 Out of Scope
- Geo Master CRUD เอง (consume read-only เท่านั้น — mock TH_GEO subset)
- Stock / on-hand management (อยู่ F-INV-STOCK — ใช้แค่ flag `hasStock`)
- DOA / approval workflow (RBAC เท่านั้น)
- `company_id` / multi-company (1 ERP = 1 company — D3)
- Branch-scoped data permission (D8 — ฝาก Permission Matrix / Policy & Security เป็น system-wide, future)
- Default location ต่อคลัง (receiving/pick/staging) — DEFER ไป pick-pack-ship phase (D9)
- pick_sequence, capacity หลายมิติ (weight/volume), ABC class, PACK↔Ship dock flow
- Type-driven auto default behavior flags (Phase 3 — AD-3; schema-ready ไม่ auto-apply)
- Role switcher UI (D15 — ถอดออกจาก prototype; production role มาจาก auth)

### 3.3 Assumptions
- Geo Master + Branch/Company master ยังไม่พร้อม → prototype consume read-only + mock (AD-1, AD-6); BE ทำ mock endpoint จนกว่า master จริงพร้อม (Phase 2)
- `hasStock` มาจาก Inventory runtime read (feature นี้ไม่คำนวณเอง)
- `loc_require_barcode` = ON โดย default (AD-7)

### 3.4 Scope Lock ⭐ (สืบทอดจาก DECISION_LOG — LOCKED)

> มติที่ล็อกแล้วเหล่านี้ **ห้าม override ตลอด chain** — ถ้า business rule ใดขัด → LOCK ชนะ

| LOCK | มติ | ผล |
|---|---|---|
| **D1** | Feature id = F-LOCATION-MASTER-001, folder `11_Warehouse`, HTML = `WarehouseBin.html` | คงไว้ทุกที่ |
| **D3** | `branch_id` required (soft-ref) บน **warehouses เท่านั้น** · **ไม่มี company_id** | Zone/Area/Rack/Location สืบทอดสาขาผ่าน warehouse_id |
| **D8** | RBAC = role-only · branch = filter/UX เท่านั้น (ไม่ใช่ security boundary) | ไม่มี branch-scoped data permission |
| **D11 / GC#7** | ไม่มี hard delete ทุกระดับ — node = soft archive (active children block), location = soft decommission (stock≠0 block) · append-only audit | microcopy "ลบ" → "จัดเก็บ/ปลดระวาง" |
| **D12** | Dual-view (List + Hierarchy Tree) · Tree = NON-STANDARD approved deviation | คง CI/iron rules |
| **D14** | Canonical name = "Warehouse & Bin" (TH "คลังและตำแหน่ง") | เปลี่ยนจาก legacy "Location Hierarchy" |
| **D15** | ถอด role switcher · breadcrumb + full_path แสดง **ชื่อ** สำหรับ zone/area/rack, **code** สำหรับ warehouse+location · **branch ไม่แสดงใน path** (reverse ส่วน path ของ D7) · ระดับ 5 = "ตำแหน่ง" ทุกจุด | branch ยังเป็น field คลัง (D3) + column/filter ใน List (D7) |

**SCOPE DRIFT check:** ไม่มี In Scope ข้อใดเกินขอบเขตใบเซ็น — ทุกข้อ trace กลับ COVERAGE_MAP + DECISION_LOG ได้ ✅

---

## 4. User Roles & Permissions

RBAC role-only (D8). 5 roles (สกัดจาก `ROLES` + `perms()` ใน HTML):

| Role (TH / EN) | ดู (List/Tree/View) | สร้าง/แก้ไข node+location | เปลี่ยนสถานะ (block/frozen/…) | จัดเก็บ/ปลดระวาง (delete) |
|---|:---:|:---:|:---:|:---:|
| ผู้จัดการคลัง / Warehouse Manager | ✅ | ✅ | ✅ | ✅ |
| หัวหน้างานคลัง / Warehouse Supervisor | ✅ | ✅ | ✅ | ❌ |
| ผู้ควบคุมสต็อก / Inventory Controller | ✅ | ❌ | ✅ | ❌ |
| พนักงานคลัง / Operator | ✅ | ❌ | ❌ | ❌ |
| ผู้ดูแลระบบ / Admin | ✅ | ✅ | ✅ | ✅ |

- `create` = manager | supervisor | admin · `del` (archive/decommission) = manager | admin (SoD) · `status` = ทุก role ยกเว้น operator
- Operator = view-only (create/bulk ปุ่ม disabled พร้อม tooltip "ดูอย่างเดียว")
- **Production role มาจาก auth** — ไม่มี role switcher ใน UI (D15)

---

## 5. User Journey (with COSO)

> Master Data feature — ไม่มี approval workflow (DOA out of scope). COSO Roles ใช้ default `Master Data Module` (Maker=ผู้สร้าง, Checker/Approver = ไม่มีในเฟสนี้เพราะ RBAC ตรง, System=validate/audit). SoD hard rule: การจัดเก็บ/ปลดระวาง (destructive) จำกัดที่ Manager/Admin แยกจาก Operator/Controller ที่สร้างไม่ได้.

### 5.1 Happy Path — สร้างโครงสร้างคลัง (List view)

| # | Step | หน้าจอ/จุดบน UI (จริงใน HTML) | Maker | Checker | Approver | System |
|---|---|---|---|---|---|---|
| 1 | เปิดหน้า List, ดู KPI 5 ระดับ + เลือก branch filter | Page header + KPI + branch combobox | Manager/Supervisor | — | — | โหลด (loading skeleton), scope ตาม branchFilter |
| 2 | กด "สร้างคลัง" → กรอก code/name/**branch**/geo | Node form drawer (level=warehouse) | Maker | — | — | validate code unique (system-wide), branch required, geo cascade + auto postcode |
| 3 | สร้าง Zone (เลือกคลัง, temp control) | Node form (zone) | Maker | — | — | validate code unique/คลัง, temp min≤max |
| 4 | สร้าง Area (เลือกโซน, allows_direct) | Node form (area) | Maker | — | — | validate code unique/โซน |
| 5 | สร้าง Rack (เลือกพื้นที่, grid R×C×L) | Node form (rack) | Maker | — | — | validate code unique/พื้นที่ |
| 6 | สร้าง Location (2-step wizard) หรือ **Bulk Generate** | Location form / Bulk drawer | Maker | — | — | parent rack XOR area, allows_direct gate, cap>0, barcode gate, collision check (bulk atomic) |
| 7 | ดูรายละเอียด / เจาะลูก | View drawer (node 1 tab / location 3 tabs) + drill | ทุก role (view) | — | — | render full_path (ชื่อ zone/area/rack, code WH+location), child stats |

### 5.2 Alternative / Exception Paths
- **A1 allows_direct=false** ตอนเลือก area เป็น parent → inline warn + ลิงก์ "เพิ่มชั้นวางในพื้นที่นี้ก่อน" (`suggestAddRack`) → เด้งไป create rack ใน context เดิม
- **A2 barcode ยังไม่กรอก** (loc_require_barcode ON) → บันทึกเป็นสถานะ **"ปิดใช้"** → เพิ่ม barcode ภายหลังเพื่อ activate
- **A3 เปลี่ยนสถานะ location** (block ต้องระบุเหตุผล / frozen ระหว่างนับสต็อก / maintenance) → modal + audit
- **A4 archive node** ที่มีลูก active → block (referential-safe) · **A5 decommission location** ที่ stock≠0 → block
- **A6 reparent location** ที่ stock≠0 → block (ต้อง stock=0 ก่อน)

### 5.3 Hierarchy Tree view (D12)
สลับด้วย view switcher (segmented) ใต้ page header → tree pane ซ้าย (WH→Zone→Area→Rack collapsible + count/level badge) + node summary panel ขวา (fields + full path + child chips คลิก→สลับ List). แชร์ state `sel` เดียวกับ List.

---

## 6. Data Entity & Fields

### 6.1 warehouses (คลัง — L1)
| # | Field | Label UI | Type | ค่า/ตัวเลือก | จำเป็น | เงื่อนไข | หมายเหตุ |
|---|---|---|---|---|:---:|---|---|
| 1 | code | รหัสคลัง | TEXT | — | ✅ | unique ทั้งระบบ | แสดงเป็น code ใน path |
| 2 | name | ชื่อคลัง | TEXT | — | ✅ | | |
| 3 | branch_id | สาขา | LOOKUP | BRANCHES (soft-ref) | ✅ | required (D3/GC#4) | Master Combobox (#94) |
| 4 | addr_line | ที่อยู่ | TEXT | — | ❌ | | |
| 5 | province | จังหวัด | LOOKUP | TH_GEO | ❌ | cascade | |
| 6 | district | อำเภอ/เขต | LOOKUP | ตาม province | ❌ | reset เมื่อ province เปลี่ยน | |
| 7 | subdistrict | ตำบล/แขวง | LOOKUP | ตาม district | ❌ | reset เมื่อ district เปลี่ยน | |
| 8 | postcode | รหัสไปรษณีย์ | AUTO | จาก subdistrict | ❌ | readonly | เติมอัตโนมัติ |
| 9 | status | สถานะ | ENUM | active / archived | ✅(sys) | default active | |

### 6.2 zones (โซน — L2)
code*, name*, warehouse_id* (LOOKUP active WH), temp_controlled (TOGGLE), temp_min/temp_max (NUMBER, required + min≤max ถ้า temp_controlled), status (active/archived). code unique ภายในคลัง.

### 6.3 areas (พื้นที่ — L3)
code*, name*, zone_id* (LOOKUP active zone), **allows_direct** (TOGGLE — flexible-parent gate), status. code unique ภายในโซน.

### 6.4 racks (ชั้นวาง — L4)
code*, name*, area_id* (LOOKUP active area), rows/cols/levels (NUMBER — grid สำหรับ bulk), status. code unique ภายในพื้นที่.

### 6.5 locations (ตำแหน่ง — L5)
| # | Field | Label | Type | ค่า/ตัวเลือก | จำเป็น | เงื่อนไข |
|---|---|---|---|---|:---:|---|
| 1 | parent_type | ต้นทาง | ENUM | rack \| area | ✅ | XOR |
| 2 | rack_id / area_id | Rack / Area | LOOKUP | active only | ✅ (ตัวใดตัวหนึ่ง) | area ต้อง allows_direct=true |
| 3 | code | รหัสตำแหน่ง | TEXT | — | ✅ | unique ภายใน parent |
| 4 | name | ชื่อ | TEXT | — | ❌ | |
| 5 | type | ประเภท | DROPDOWN | 10: PICK_FACE, RESERVE, HOLD, DAMAGED, BULK, STAGING, PACK, RECEIVING_DOCK, TRANSIT, VIRTUAL | ✅ | icon+label (ไม่ color-code — D10) |
| 6 | cap_uom | หน่วยความจุ | DROPDOWN | pallet/box/piece/cbm/kg | ✅ | |
| 7 | cap_val | ความจุ | NUMBER | > 0 | ✅ | > 0 |
| 8 | rotation | หมุนเวียน | DROPDOWN | FIFO/LIFO/FEFO/Manual | ✅ | |
| 9 | row/col/level/position | พิกัด | TEXT/NUMBER | — | ❌ | |
| 10 | pickable/putawayable/replenishable | พฤติกรรม | TOGGLE | — | ❌ | manual (auto=Phase3) |
| 11 | mixed_lot/mixed_item/neg_stock | การปน | TOGGLE | — | ❌ | |
| 12 | barcode / qr | บาร์โค้ด/QR | TEXT | — | ❌* | *ต้องมี barcode ก่อน activate (BR-014) |
| 13 | status | สถานะ | ENUM | 7-state (§8) | ✅(sys) | |
| 14 | block_reason | เหตุผลบล็อก | TEXT | — | ✅ ถ้า blocked | |
| 15 | hasStock | มีสต็อก | (runtime) | Inventory read | — | gate decommission/reparent |

### 6.6 Audit (WORM, append-only) — ทุก entity
refId, at (timestamp), by (ผู้ทำ), action, detail, v (success/warning). ไม่มี update/delete บน audit (GC#7).

### 6.7 Entity Relationship
```
branches (ext, soft-ref) ──(1:N)──▶ warehouses
warehouses ──(1:N)──▶ zones ──(1:N)──▶ areas ──(1:N)──▶ racks
areas ──(1:N)──▶ locations (parent_type=area, ต้อง allows_direct)
racks ──(1:N)──▶ locations (parent_type=rack)
[locations.parent = rack XOR area]   TH_GEO (ext, read-only) ──▶ warehouses (address)
locations ──(referenced by)──▶ Inventory / GR / Picking / … (location_id + full_path contract)
```

---

## 7. User Stories & Acceptance Criteria

- **S-01** ในฐานะ Manager ฉันสร้างคลังใหม่พร้อมผูกสาขา — AC: (1) branch required ห้ามบันทึกถ้าว่าง; (2) code ซ้ำทั้งระบบ → error "รหัสซ้ำในระบบ".
- **S-02** ในฐานะ Manager ฉันสร้างโซนควบคุมอุณหภูมิ — AC: (1) เปิด temp_controlled → ต้องกรอก min/max; (2) min > max → error.
- **S-03** ในฐานะ Manager ฉันกำหนดพื้นที่ให้วางของตรงบนพื้นได้ — AC: (1) allows_direct=false ปิดไม่ให้เลือก area เป็น parent; (2) ปิด allows_direct ทั้งที่มี direct location → block.
- **S-04** ในฐานะ Manager ฉันสร้างตำแหน่งใต้ชั้นวางหรือพื้นที่ — AC: (1) เลือก parent ได้เพียง rack หรือ area (XOR); (2) capacity ≤ 0 → error.
- **S-05** ในฐานะ Manager ฉันสร้างตำแหน่งจำนวนมากจาก template — AC: (1) preview จำนวนก่อนยืนยัน; (2) รหัสชน → block ทั้งชุด (atomic).
- **S-06** ในฐานะ Manager ฉันจัดเก็บ node ที่เลิกใช้ — AC: (1) มีลูก active → block; (2) ไม่มีลูก → status=archived เก็บประวัติ (ไม่ลบถาวร).
- **S-07** ในฐานะ Manager ฉันปลดระวางตำแหน่งที่เลิกใช้ — AC: (1) stock≠0 → block; (2) stock=0 → status=decommissioned + audit.
- **S-08** ในฐานะ Inventory Controller ฉันเปลี่ยนสถานะตำแหน่ง (block/frozen) — AC: (1) block ต้องระบุเหตุผล; (2) activate ตำแหน่งไม่มี barcode → block.
- **S-09** ในฐานะ Operator ฉันดูโครงสร้างคลังได้แต่แก้ไม่ได้ — AC: (1) ปุ่มสร้าง/bulk disabled; (2) ไม่มีปุ่ม archive/decommission.
- **S-10** ในฐานะผู้ใช้ ฉันสลับ List ↔ Hierarchy Tree โดยคง selection — AC: (1) view switcher เปลี่ยนมุมมอง; (2) เลือก node ใน tree แล้วสลับไป List เห็น context เดียวกัน.

---

## 8. Status & Lifecycle

### 8.1 Node (warehouse/zone/area/rack)
```
active ──(archive: ไม่มีลูก active)──▶ archived   [soft · เก็บประวัติ · ไม่มี hard delete]
```

### 8.2 Location — 7-state (+ decommissioned terminal)
```
                (barcode ok)
  inactive ◀──────────────▶ active ──▶ full        (ความจุเต็ม)
     ▲ (no barcode on create)   │
     │                          ├──▶ blocked      (ต้องระบุเหตุผล)
     │                          ├──▶ maintenance  (ซ่อมบำรุง)
     │                          └──▶ frozen        (ระหว่างนับสต็อก)
  active/… ──(decommission: stock=0)──▶ decommissioned   [terminal · soft]
```

| State | Trigger | Next | เงื่อนไข |
|---|---|---|---|
| inactive | สร้างโดยไม่มี barcode (BR-014) | active | เพิ่ม barcode |
| active | default / activate | full/blocked/maintenance/frozen/decommissioned | — |
| blocked | block action | active | ต้องมี block_reason |
| frozen | นับสต็อก | active | — |
| decommissioned | decommission | (terminal) | stock=0 (BR-010) |

---

## 9. Business Rules + Validation (with Change Likelihood Tags)

| ID | Rule | Tag | ใครเปลี่ยน / บ่อย / ระดับ | ที่มา |
|---|---|:---:|---|---|
| BR-001 | ลำดับชั้น 5 ระดับ WH→Zone→Area→Rack→ตำแหน่ง | 🔒 FIXED | — | 🤖 |
| BR-002 | Location parent = rack **XOR** area | 🔒 FIXED | — | 🤖 |
| BR-003 | parent=area ต้อง allows_direct=true | 🔒 FIXED | — | 🤖 |
| BR-004 | code unique — WH ทั้งระบบ, ระดับอื่น unique ภายใน parent | 🔒 FIXED | — | 🤖 |
| BR-005 | archive node ที่มีลูก active → block (referential-safe) | 🔒 FIXED | — | ✅ D11 |
| BR-006 | capacity cap_val > 0 | 🔒 FIXED | — | 🤖 |
| BR-007 | ปิด allows_direct ไม่ได้ถ้ามี direct location อยู่ | 🔒 FIXED | — | 🤖 |
| BR-008 | temp_controlled → ต้องมี temp range + min ≤ max | 🔒 FIXED | — | 🤖 |
| BR-009 | warehouse ต้องมี branch_id (required soft-ref) | 🔒 FIXED | — | ✅ D3/GC#4 |
| BR-010 | decommission location ต้อง stock=0 (hasStock block) | 🔒 FIXED | — | ✅ D11/AD-5 |
| BR-011 | ไม่มี hard delete — node=archive, location=decommission (soft) | 🔒 FIXED | — | ✅ GC#7/D11 |
| BR-012 | reparent location ที่ stock≠0 → block | 🔒 FIXED | — | ✅ AD-5/FN-19 |
| BR-013 | block location ต้องระบุเหตุผล | 🔒 FIXED | — | 🤖 |
| BR-014 | location ต้องมี barcode ก่อน activate (ไม่งั้นบันทึก inactive) | ⚙️ CONFIGURABLE | Admin / เป็นระยะ / **Admin Panel** (`loc_require_barcode`) | ✅ AD-7 |
| BR-015 | bulk generate = preview + collision check + atomic (all-or-nothing) | 🔒 FIXED | — | ✅ |
| BR-016 | สิทธิ์ตาม role (create=Mgr/Sup/Admin, del=Mgr/Admin, status≠Operator) | ⚙️ CONFIGURABLE | Admin / เป็นระยะ / **Admin Panel (Permission Matrix, system-wide)** | ✅ D8 |
| BR-017 | geo cascade: เปลี่ยน parent → reset ลูก + auto postcode | 🔒 FIXED | — | 🤖 |
| BR-018 | type-driven default behavior flags (auto-apply) | 🔄 DYNAMIC (DEFERRED) | Business Owner / **Rule Management** — **Phase 3, schema-ready ไม่เปิดใช้** | ✅ AD-3 |

### 9.5 สรุประดับความยืดหยุ่น
| Rule | ระดับ | เหตุผล | ที่มา |
|---|---|---|---|
| BR-014 | Admin Panel | config key เปลี่ยนค่า on/off | ✅ Stakeholder (AD-7) |
| BR-016 | Admin Panel (Permission Matrix, system-wide) | role→action mapping | ✅ Stakeholder (D8) |
| BR-018 | Rule Management | เงื่อนไข type→flags ซับซ้อน | ✅ Stakeholder (AD-3) — **DEFERRED Phase 3** |

> Escalation: BR-018 (DYNAMIC) เป็น deferred + confirmed โดย stakeholder (AD-3) แล้ว — บันทึกใน §15 OQ-3 เพื่อยืนยัน contract ก่อนเปิด Phase 3. ไม่มี rule 🤖-inferred ที่ระดับ DYNAMIC/Engine ค้าง.

---

## 10. Edge Cases

### 10.1 ที่ HTML/Decisions ระบุ (☑ implemented ใน prototype)
- ☑ EC-01 flexible-parent violation (เลือกทั้ง rack+area) → CHECK block
- ☑ EC-02 allows_direct=false → inline warn + suggest add rack
- ☑ EC-03 referential-safe archive (มีลูก active) → block (BR-005)
- ☑ EC-04 decommission stock≠0 → block (BR-010)
- ☑ EC-05 reparent stock≠0 → block (BR-012)
- ☑ EC-06 bulk-gen collision → atomic block ทั้งชุด
- ☑ EC-07 code ซ้ำภายใน parent / ทั้งระบบ (WH) → error
- ☑ EC-08 ปิด allows_direct ทั้งที่มี direct loc → block (BR-007)
- ☑ EC-09 zone temp missing / min>max → block
- ☑ EC-10 geo cascade reset เมื่อเปลี่ยน parent
- ☑ EC-11 activate location ไม่มี barcode → block
- ☑ EC-12 Operator = view only (ปุ่ม disabled)
- ☑ EC-13 Supervisor/Controller ลบไม่ได้

### 10.2 จาก AI Pattern Matching (☐ = แนะนำ — BA confirm ที่ SOW3.7)
- ☐ EC-14 (DI/Lookup) branch/geo master ยังไม่พร้อม → BE mock; ต้องนิยาม behavior เมื่อ soft-ref code หาไม่เจอ (แสดง code เดิม? warn?)
- ☐ EC-15 (CA/Concurrent) 2 คนสร้าง code เดียวกันพร้อมกัน → uniqueness ระดับ DB (ไม่ใช่แค่ client)
- ☐ EC-16 (ST/Status) archive node แล้วลูกที่ archived อยู่แล้วไม่ block (ยืนยัน childCount นับเฉพาะ active — ตรงกับ HTML)
- ☐ EC-17 (Bulk) bulk gen จำนวนมหาศาล (rows×cols×levels ใหญ่) → performance/limit cap? (ยังไม่มี cap ใน prototype)
- ☐ EC-18 (Data) full_path เมื่อ parent เปลี่ยนชื่อ → downstream ที่ cache path ต้อง re-read (contract)

---

## 11. Impact / Regression
New Feature — ไม่มี regression บนของเดิม. ผลกระทบขาออก ดู §12.1 (Downstream). Prototype E2E ผ่าน 74/74 (viewports 1280/1440) รวม dual-view + tree + shared sel.

---

## 12. System Context

### 12.1 Value Stream & Downstream Impact ⭐
**Positioning:** master data พื้นฐานของ Warehouse module (W3) — เป็น "ที่เก็บ" ที่ Inventory และกระบวนการ logistics ทั้งหมดอ้างอิง (GC#2: Inventory เป็นแกน check stock).

**Upstream (รับเข้า):**
| ต้นทาง | ข้อมูล | ชนิด |
|---|---|---|
| Company/Branch master | branch_id | config soft-ref (required, D3) |
| Geo Master | province/district/subdistrict/postcode | config read-only (cascade) |
| Inventory (runtime) | hasStock flag | runtime read (gate decommission/reparent) |

**Downstream Impact Map:**
| ปลายทาง | ข้อมูลที่ไหลไป | Trigger | ถ้าตำแหน่งเปลี่ยน/ปลดระวาง |
|---|---|---|---|
| Inventory (on-hand) | location_id + full_path | location active | decommission ต้อง stock=0 ก่อน → ไม่มี orphan stock |
| GR / Put Away / Picking / RTV / Stock Adj / Transfer / Stocktake | location_id + type enum + path (contract) | อ้างตำแหน่ง | เปลี่ยน parent (reparent) ต้อง stock=0; blocked/frozen กันการหยิบ/วาง |
| ENG-HIER-PATH (full path engine) | full_path (WH code › zone/area/rack name › location code) | render | reuse ได้โดย feature อื่น |
| รายงาน/KPI คลัง | จำนวน node/location, capacity | ต่อเนื่อง | สะท้อนทันที |

**ผลกระทบแนวขวาง:** สต๊อก (ผูก location_id), รายงานคลัง. ไม่กระทบ GL/งบประมาณโดยตรง (master ไม่ผลิตรายการเงิน).

### 12.3 Existing System Reference
| Rule | ระดับ | มีอยู่แล้ว? | Reference |
|---|---|:---:|---|
| BR-014 barcode gate | Admin Panel | ❌ | สร้าง config key `loc_require_barcode` |
| BR-016 RBAC role→menu | Admin Panel | ⚠️ บางส่วน | Permission Matrix (Policy & Security) system-wide — feature นี้ consume, ไม่สร้าง branch-scoped เอง (D8) |
| Branch / Geo master | (external) | ⚠️ mock | รอ Company/Geo Master จริง (Phase 2) |
| Audit (WORM) | (platform) | ⚠️ | ใช้ append-only audit กลาง (GC#7) |

---

## 13. Delivery Phases

**Phase 1 — Feature Launch:** CRUD 5 entities + dual-view + branch/geo (mock) + bulk generate (atomic) + soft archive/decommission + 7-state lifecycle + WORM audit + RBAC role-only (seed role→perm ไม่ hardcode). Config key `loc_require_barcode` (seed ON).
**Phase 2 — Integration:** ต่อ Company/Branch master + Geo Master จริง (แทน mock endpoint) + expose location_id/full_path contract ให้ Inventory.
**Phase 3 — Rule Management:** BR-018 type-driven auto default behavior flags (`applyTypeDefaults` — schema-ready). + (candidate) default location ต่อคลัง (D9, ตอน pick-pack-ship).
**Phase 4 — Engine:** ไม่มีในเฟสนี้.

---

## 14. Dev Requirements Summary ("ใบสั่ง")

### 14.1 Config Foundation
- `loc_require_barcode` (BR-014) — config table/admin, seed ON.
- role→permission map (BR-016) — ใช้ Permission Matrix กลาง (system-wide), **ห้าม** hardcode สิทธิ์ในโมดูล และ **ห้าม** ทำ branch-scoped (D8).
- state machine node (active/archived) + location (7-state + decommissioned) — table-driven ห้าม hardcode transition.

### 14.2 จาก Tag
- BR-014 → Admin Panel config (มี toggle).
- BR-016 → reuse Permission Matrix ที่มี, ไม่สร้างใหม่.
- BR-018 → **ห้าม implement Phase 1** — schema-ready เท่านั้น (contract type→flags), เปิดใช้ Phase 3.

### 14.3 Edge Cases สำคัญ (Dev ต้อง handle)
- Uniqueness ต้องบังคับที่ DB (unique index: WH code global; zone/area/rack/location code ต่อ parent) — ไม่ใช่แค่ client (EC-15).
- Bulk generate = transaction atomic (all-or-nothing) + collision precheck (BR-015/EC-06).
- Gate: activate ต้องมี barcode; decommission/reparent ต้อง stock=0 (อ่าน hasStock จาก Inventory).
- childCount referential guard นับเฉพาะ **active** children (archived/decommissioned ไม่ block).
- Full path formatting: WH=code, zone/area/rack=**name**, location=code, **ไม่มี branch ใน path** (D15).

### 14.4 WARNING รอข้อสรุป
ดู §15 (branch/geo master timeline, bulk cap, soft-ref not-found behavior).

### 14.5 Regression Scope
N/A (New Feature).

### 14.6 Screen Inventory + UI Signals

> ⚠️ **HTML-RIF DRIFT (resolved):** prototype เป็น **single-page SPA ที่สลับ view ด้วย state (ไม่มี hash route `#/...`)** — คอลัมน์ route จึงระบุเป็น view/drawer identifier จริงในโค้ด (`state.view`, `state.drawer.view`, `state.modal.type`) แทน URL. ไม่มีหน้าเกิน/ขาดเทียบ COVERAGE_MAP §4.

| # | หน้า/มุมมอง (business) | view/drawer id (จริงใน HTML) | ประเภทหยาบ | ผู้ใช้หลัก | หน้าที่ |
|---|---|---|---|---|---|
| P-01 | รายการ List (drill-down) | `state.view='list'` (renderDrill/Table/Card) | หน้ารายการ | ทุก role | ค้นหา/เจาะ WH→…→ตำแหน่ง + KPI + branch/type/status filter |
| P-02 | Hierarchy Tree | `state.view='tree'` (renderTreeView) | หน้ารายการ (tree) | ทุก role | มองโครงสร้าง 5 ระดับ + node summary panel (NON-STANDARD, D12) |
| P-03 | ฟอร์ม node (สร้าง/แก้ WH/Zone/Area/Rack) | drawer `node-form` | ฟอร์มสร้าง/แก้ไข (ขั้นเดียว) | Mgr/Sup/Admin | กรอกข้อมูล node + validate |
| P-04 | ฟอร์มตำแหน่ง 2 ขั้น | drawer `loc-form` (step 1–2) | ฟอร์มสร้าง (หลายขั้น) | Mgr/Sup/Admin | parent+identity → capacity+behavior+barcode |
| P-05 | Bulk Generate | drawer `bulk` | ฟอร์มสร้าง (หลายขั้น) | Mgr/Sup/Admin | template + preview + collision + atomic |
| P-06 | View Node | drawer `view-node` | หน้ารายละเอียด | ทุก role | fields + full path + child stats + actions |
| P-07 | View Location (3 tabs) | drawer `view-loc` | หน้ารายละเอียด | ทุก role | overview / behavior / audit |
| P-08 | Modal จัดเก็บ/ปลดระวาง/บล็อก | modal `delete-node` / `decommission` / `block` | หน้ายืนยัน | Mgr/Admin (del), Controller+ (block) | destructive confirm + guard message |

**~8 มุมมอง** (list 1, tree 1, drawer form 3, drawer view 2, modal 1 กลุ่ม).
**UI Signals → FRD:** ไม่ใช่ transaction document (ไม่มี approver/พิมพ์/ลายเซ็น) · ไม่มี print/PDF · **NON-STANDARD flag: Hierarchy Tree (D12)** = approved deviation, ต้อง log LD ใน FRD/HTML · Master Combobox (#94) สำหรับ branch/geo/parent picker · Esc chain (ปิด combobox ก่อน drawer). Layout/pattern/CI spec = หน้าที่ FRD (frd-generator-v6).

---

## 15. Open Questions

| # | คำถาม | สถานะ | คำตอบ/แผน |
|---|---|:---:|---|
| OQ-1 | Geo Master (schema/timeline) | ⚠️ รอ | ใช้ mock TH_GEO subset (AD-1); API จริง Phase 2 — confirm กับทีม platform |
| OQ-2 | Branch/Company master พร้อมเมื่อไหร่ | ⚠️ รอ | mock branch list (AD-6); ต่อจริง Phase 2 |
| OQ-3 | BR-018 type→default flags contract | ⚠️ รอ | DEFERRED Phase 3 (AD-3) — ยืนยัน default map ต่อ type ก่อนเปิด |
| OQ-4 | Soft-ref (branch/geo) not-found behavior | ⚠️ รอ | นิยาม UX เมื่อ code หาไม่เจอ (EC-14) — BA/PM |
| OQ-5 | Bulk generate มี cap สูงสุดไหม | ⚠️ รอ | prototype ยังไม่ cap (EC-17) — ยืนยัน performance limit |
| OQ-6 | Branch-scoped data permission | ✅ ตอบแล้ว | Out of scope — ฝาก Permission Matrix system-wide (D8) |

---

## 16. Security & Compliance

### 16.1 Preset
**P3 — Master Data (10 controls).** เหตุผล: feature เป็น master data (ไม่ใช่ financial/PII/transaction). Data classification: ทุก owned column = Internal, geo = Public, branch_id = Internal, PII overlay = created_by/modified_by (AD).

### 16.2 Applicable Standards (ย่อ)
ISO 27001 (access control) ✅ · OWASP (input validation, IDOR บน id) ✅ · PDPA ❌ (ไม่มี personal data นอก audit actor) · SOX ❌ (ไม่ใช่ financial).

### 16.3 Control Checklist (P3)
| Control | Must/Opt | Note |
|---|:---:|---|
| RBAC role-based access | ✓Must | 5 roles, create/del/status (D8) |
| Input validation (code, cap>0, temp range) | ✓Must | server-side บังคับ |
| Uniqueness constraint (DB) | ✓Must | unique index ต่อ scope |
| Referential integrity (soft) | ✓Must | archive/decommission guard |
| Append-only audit (WORM) | ✓Must | ทุก mutation, ไม่มี hard delete (GC#7) |
| Soft-delete / archive | ✓Must | node archive, location decommission |
| IDOR protection บน entity id | ✓Must | ตรวจสิทธิ์ทุก action |
| Optimistic/concurrency control | ○Opt | code uniqueness race (EC-15) |
| Config auditability (loc_require_barcode) | ○Opt | log config change |
| Data classification tagging | ○Opt | Internal/Public |

### 16.4 Risk Statement
- **R1:** hard delete ทำข้อมูลอ้างอิงหาย → mitigated by BR-011 (soft) + WORM audit.
- **R2:** ปลดระวาง/ย้ายตำแหน่งที่ยังมีสต็อก → orphan stock → mitigated by BR-010/BR-012 (stock=0 gate).
- **R3:** code ซ้ำทำ downstream อ้างผิดตำแหน่ง → mitigated by BR-004 + DB unique index.
- **R4:** สิทธิ์รั่ว (Operator ทำ destructive) → mitigated by BR-016 RBAC (server-enforced).

---

## 17. Health Check

### 17.1 SLA
| จุด | เกณฑ์ | Owner |
|---|---|---|
| โหลดหน้า List/Tree | ≤ 2s (P95) | Warehouse Ops |
| Bulk generate (atomic commit) | ≤ 5s ต่อ ~500 location | Dev/Ops |
| activate/decommission action | ≤ 1s | Ops |

### 17.2 Control Points
Map จาก §16: RBAC gate ทุก action · uniqueness check ก่อน commit · stock=0 gate ก่อน decommission/reparent · audit write ทุก mutation.

### 17.3 KPI
| KPI | ประเภท | คู่กับ §2.3 |
|---|---|---|
| % location active ที่มี barcode | Quality/Compliance | ✅ ตัวชี้วัด 1 |
| % location มี full_path ครบ (downstream-ready) | Quality | ✅ ตัวชี้วัด 2 |
| เวลาตั้งค่าคลังครบ 5 ระดับ | Speed | ✅ ตัวชี้วัด 3 |
| % คลังผูก branch ครบ | Compliance | ✅ ตัวชี้วัด 4 |
| จำนวน location ต่อคลัง / % capacity ใช้งาน | Volume | — |

### 17.4 Threshold
| ตัว | Min | Max | Action เมื่อ breach |
|---|---|---|---|
| % barcode ก่อน active | 100% | — | alert location active ไม่มี barcode (ควรเป็นไปไม่ได้ตาม BR-014) |
| location status=blocked | — | (เฝ้าระวัง) | รายงาน blocked ค้างนาน → ตรวจสอบ |
| bulk gen size | — | (OQ-5) | เกิน cap → เตือน/แบ่ง batch |

### 17.5 Throughput
Capacity: รองรับหลายคลัง/สาขา; bulk generate = จุด stress หลัก (rack grid ใหญ่). Baseline เก็บหลัง launch.

---

## 18. Monitoring

### 18.1 Reports Overview
Performance (การใช้งาน master) · Closing (สรุปโครงสร้างคลัง ณ สิ้นงวด) · Anomaly (barcode หาย/blocked ค้าง/decommission ผิดปกติ) · Transaction (audit trail mutation).

### 18.2 Dashboard Widgets
- KPI tiles 5 ระดับ (WH/Zone/Area/Rack/ตำแหน่ง) — จาก renderKpi (มีจริง)
- % barcode compliance (§17.3)
- location by status (7-state) distribution
- คลังที่ branch ไม่ครบ (ควร = 0)

### 18.3 Performance Report
จำนวน node/location ต่อสาขา/คลัง, capacity utilization, การเติบโตของโครงสร้าง.

### 18.4 Closing Report
Snapshot โครงสร้าง 5 ระดับ + สถานะ ณ สิ้นงวด (จาก audit).

### 18.5 Anomaly Report
location active ไม่มี barcode (ผิด BR-014), blocked/frozen ค้างเกินเกณฑ์, archive/decommission โดย role ที่ไม่คาด. Recipients (Watcher): Warehouse Manager, Auditor/Compliance.

### 18.6 Transaction Report
WORM audit log ทุก mutation (create/edit/status/archive/decommission/bulk) — refId, by, action, detail, timestamp.

---

## AI Review Report

```
═══════════════════════════════════════
AI REVIEW REPORT — BRD Generator Full
═══════════════════════════════════════
BRD: BRD-F-LOCATION-MASTER-001 — Warehouse & Bin (คลังและตำแหน่ง)
ประเภท: New Feature · วันที่ตรวจ: 2026-08-06

CHECKLIST RESULTS (C01–C23 + PE01–PE05):
✅ C01 Business Objective วัดผลได้ (§2.3, 4 ตัวมี baseline/target/วิธีวัด)
✅ C02 User Roles ครบ (5 roles, §4)
✅ C05 Story ไม่มีคำว่า "และ" ในคำอธิบาย (S-01..S-10)
✅ C10 ทุก rule ที่มีตัวเลข/เงื่อนไขติด Tag (BR-001..018)
✅ C13 Edge Cases ครบหมวด (10.1 BA/HTML + 10.2 AI)
✅ C18 WARNING ทุกข้อมีแผน (§15 OQ-1..6)
✅ C19 Section 14 ใบสั่งครบ + 14.6 Screen Inventory
✅ C20 Scope Lock §3.4 — LOCK D1/D3/D8/D11/D12/D14/D15 ครบ, ไม่มี SCOPE DRIFT เงียบ
✅ C21 Value Stream §12.1 — upstream + Downstream Impact Map ตอบ "แล้วไงต่อ" ทุกแถว
✅ C22 §2.3 ทุกตัวมี baseline/target/วิธีวัด + คู่ใน §17.3
✅ C23 §9.5 marker ✅/🤖 ครบ — ไม่มี 🤖+DYNAMIC ค้าง (BR-018 ✅ + deferred)
✅ PE01 COSO roles ครบทุก step §5 (Master Data — ไม่มี approval)
✅ PE02 SoD: destructive (archive/decommission) แยกจากผู้สร้างที่ไม่มีสิทธิ์ (Operator/Controller)
✅ PE03 Security Preset P3 เลือกแล้ว + 10 controls
✅ PE04 SLA + KPI + Threshold §17 ครบ
✅ PE05 Cross-section: BC↔Edge, Control↔HealthCP, Metric↔Widget ผ่าน

SUMMARY: ผ่าน 18/18 (+ PE 5/5)
สถานะ: ✅ APPROVED

หมายเหตุ conflict ที่ resolve:
- HTML PREFLIGHT comment + .role-switch CSS + setRole() ยังค้างในไฟล์ (dead code)
  แต่ renderHeader() ไม่ render role switcher → BRD ยึด LOCK D15 (ไม่ถือเป็น feature)
- prototype ใช้ view-switch (ไม่มี hash route) → Screen Inventory ใช้ view/drawer id
  จริงในโค้ดแทน URL (flag ไว้ §14.6) — จำนวนหน้าตรง COVERAGE_MAP §4
```

**สถานะเอกสาร: ✅ APPROVED — พร้อมส่งเข้า `frd-generator-v6` (WF-01 step 6)**

> หมายเหตุ output: สร้างไฟล์ `.md` (artifact หลักสำหรับ frd-generator-v6). ยังไม่สร้าง `.docx` — สคริปต์ `md_to_docx.py` ของ skill อ้าง path Linux (`/home/claude/...`) ที่ไม่มีในสภาพแวดล้อม Windows นี้; สร้าง .docx ภายหลังได้เมื่อมี converter.
