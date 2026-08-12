# 00_OVERVIEW — F-LOCATION-MASTER-001 Warehouse & Bin

> **Variant:** FULL — มี 6 lifecycle states, bulk transaction และ 2 engine candidates  
> **Status:** DRAFT FOR REVIEW · **BRD:** `BRD-F-LOCATION-MASTER-001` APPROVED  
> **UI source of truth:** `outputs/06_Warehouse-Bin/warehouse-bin.html`

## §0.1 Purpose

กำหนด master hierarchy `Warehouse › Zone › Area › Rack › Location` สำหรับค้นหา จัดการสถานะ ตั้ง `storage_uom` และส่ง storage contract ให้ Inventory โดยไม่สร้าง flow รับเข้า/จ่ายออกใน feature นี้

## §0.2 Scope

**In scope:** list/tree/detail, CRUD Warehouse/Zone/Area/Rack/Location, Location 10 types, direct Location ใต้ Area ที่อนุญาต, status lifecycle, bulk status/UOM/generation, WORM audit, active-only Branch lookup แบบ soft reference, Geo lookup contract และ Inventory `hasStock` guard

**Out of scope:** F-INV build-out, Geo Master schema, GRN, Putaway, RTV, Pick-Pack-Ship, DOA, document numbering, notification declaration, print/PDF และ `company_id`

## §0.3 Roles

| Role/capability | Read | Mutate |
|---|---:|---:|
| Authenticated user | ✅ | — |
| `canManage` | ✅ | ✅ |
| System integration | contract only | derived `full` signal only |

ทุก mutation ตรวจ `canManage` อีกครั้งตอน commit; ไม่มี approval chain

## §0.4 System Context

```text
Company/T_branch ──branch_id──> Warehouse & Bin ──storage contract──> Inventory
Geo Master ──lookup only──────> Warehouse & Bin ──mutation diff────> Audit Trail
```

- `branch_id` → `T_branch` เป็น active-only picker; saved inactive reference ยัง resolve ได้
- ไม่มี FK cascade ข้าม module และไม่มี `company_id`; child inherit branch ผ่าน warehouse chain
- Inventory integration จำกัดที่ `storage_uom`, `loc_status` และ `hasStock` guard

## §0.5 Architecture Summary

- SPA ใช้ state route (`state.view`, `state.sel.level`, drawer/modal state) ไม่ใช้ hash route
- API layer ทำ HTTP/auth/idempotency mapping; business logic อยู่ `03_LOGIC.md`
- PostgreSQL multi-tenant RLS ใช้ `tenant_id` `[AI-DEFAULT]`
- optimistic locking ผ่าน `version` และ `If-Match` `[AI-DEFAULT]`
- `ENG-LOC-GEN` และ `ENG-HIER-PATH` เป็น DRAFT; global IDs ยังเปิด

## §0.6 Primary Entities

`T_warehouse`, `T_zone`, `T_area`, `T_rack`, `T_location`, `T_location_audit`, `T_location_type_config`

## §0.7 Source Priority

1. Scope Locks ใน `07_LOCKED_DECISIONS.md §7.0`
2. BRD business intent/rules
3. `warehouse-bin.html` สำหรับ UI structure, labels และ microcopy
4. `[AI-DEFAULT]` เฉพาะจุดที่ source ไม่กำหนด

## §0.8 Open Questions

| ID | Question | Current answer |
|---|---|---|
| OQ-LOC-01 | Geo Master timeline + endpoint contract | ไม่พบข้อมูลในบทสนทนา |
| OQ-LOC-02 | อนุมัติ Hierarchy tree NON-STANDARD หรือเหลือ List | ไม่พบข้อมูลในบทสนทนา |
| OQ-LOC-03 | type-driven defaults เริ่ม phase ใด | ไม่พบข้อมูลในบทสนทนา |
| OQ-LOC-04 | parent มี active child ใช้ cascade หรือ block | UI ปัจจุบัน block; final ไม่พบข้อมูลในบทสนทนา |
| OQ-LOC-05 | re-parent บังคับว่างหรือ live migration | ไม่พบข้อมูลในบทสนทนา |
| OQ-LOC-06 | ใครเปลี่ยน `storage_uom` ได้ | UI ปัจจุบัน `canManage` + no stock; final ไม่พบข้อมูลในบทสนทนา |
| OQ-LOC-07 | global IDs ของ `ENG-LOC-GEN` / `ENG-HIER-PATH` | ไม่พบข้อมูลในบทสนทนา |
| OQ-LOC-08 | Inventory stock-presence endpoint/event contract | ไม่พบข้อมูลในบทสนทนา |

## §0.9 Verified HTML Behavior Gaps

เอกสารนี้คง UI contract จาก HTML แต่บันทึกจุดที่ mock handler ยังไม่ครบ เพื่อไม่ให้ dev ลอก defect:

1. `submitLoc()` แสดง field แก้ไข `storage_uom` แต่ edit branch ไม่ persist field นี้
2. `confirmModal()` เปลี่ยน Location เป็น `decommissioned` แต่ไม่ append `AUDIT`
3. `submitBulk()` mock insert เพียงตัวอย่างหนึ่ง record แม้ UI preview/ข้อความระบุ atomic ทั้ง batch

Production implementation ต้องทำตาม BR-LOC-05/06/09/11/14 และ test ใน `06_TESTS.md`

## §0.10 Assumptions

- `[AI-DEFAULT]` ทุก owned table มี `tenant_id`, RLS, `version`, timestamps และ actor IDs
- `[AI-DEFAULT]` mutation รับ `Idempotency-Key`; retry body เดิมคืนผลเดิมโดยไม่สร้าง audit ซ้ำ
- `[AI-DEFAULT]` parent delete ใช้ block เมื่อมี child จนกว่า OQ-LOC-04 ปิด
- type-driven defaults ไม่ enforce ใน Phase 1 จนกว่า OQ-LOC-03 ปิด

## §0.11 Scope Lock Pointer

ดู immutable locks ที่ `07_LOCKED_DECISIONS.md §7.0`; หากเนื้อหาอื่นขัดกัน locks ชนะ

## §0.12 Coverage Manifest

| BRD source | Covered by |
|---|---|
| S-01 hierarchy drill/breadcrumb | `01_UI §1.2 P-01/P-03`, API-01/02, FN-01, `ENG-HIER-PATH`, AC-01 |
| S-02 all Locations/filter | `01_UI P-02`, API-03, FN-02, AC-02 |
| S-03 create Location | `01_UI D-02`, API-14, FN-14/15, AC-03/04 |
| S-04 status + reason | `01_UI M-01`, API-16/18, FN-17/19, AC-05 |
| S-05 bulk UOM | API-19, FN-20, AC-06, XT-02 |
| S-06 atomic generation | `01_UI D-03`, API-17, FN-18, `ENG-LOC-GEN`, AC-07 |
| S-07 decommission | `01_UI M-02`, API-20, FN-21, AC-08, XT-03 |
| BR-LOC-01..17 | `05_RULES §5.1`, DB constraints, AC/EC mappings |
| Company/Inventory/Audit/Reporting edges | `02_API §2.5`, `03_LOGIC §3.4`, `06_TESTS §6.9` |
| LOCK-LOC-01..06 | `07_LOCKED_DECISIONS §7.0` |

## §0.13 Phase 3.5 Self-check

| Section | Result |
|---|---|
| A Scope/BRD alignment | ✅ |
| B UI fidelity/state routes | ✅ |
| C R8 mutation API → logic | ✅ |
| D DB/classification/PII | ✅ |
| E rule/error coverage | ✅ |
| F state and permissions | ✅ |
| G engine placement | ✅ |
| H edge probes | ✅ |
| I cross-module contracts | ✅; OQ-LOC-08 explicit |
| J tests/DoD | ✅ |
| K coverage manifest | ✅ |
| L scope locks | ✅ |
| M HTML alignment | ✅; three mock gaps recorded |
