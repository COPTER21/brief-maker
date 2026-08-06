# 00_OVERVIEW — F-LOCATION-MASTER-001 · Location Hierarchy Management (v2)

> FRD Pack (frd-generator-v5.1) · Variant: **FULL** (9 files + INDEX) · Source: BRD-F-LOCATION-MASTER-001 **v2.0** (Enhancement)
> Supersedes FRD v1 (single-entity `locations`). v2 = full CRUD ครบ 5 ระดับ + dual-view + geo address + PACK type.

## §0.1 Document Control
| Field | Value |
|---|---|
| FRD ID | FRD-F-LOCATION-MASTER-001 |
| Feature | Location Hierarchy Management (5-level CRUD + flexible parent + dual-view + geo address) |
| Variant | FULL (has-state=Yes, multi-entity=6, multi-engine=2, critical CHECK) |
| Version | 2.0 |
| Status | Draft (from BRD v2.0) |
| Date | 2026-05-29 |
| Source | BRD-F-LOCATION-MASTER-001 v2.0 + `location-hierarchy.html` v1.1.0 |

## §0.2 Scope
CRUD เต็มทั้ง 5 ระดับ (Warehouse → Zone → Area → Rack → Location) ผ่าน UI เดียว · **flexible parent** (Location ใต้ Rack หรือ Area, XOR) · **10 core location types** (9 core + PACK) · capacity · rotation · behavior/mixing flags · bulk generation · status lifecycle · **dual-view** (List drill-down + Hierarchy tree+summary) · **Warehouse geo address** (province/district/subdistrict/postcode cascade จาก Geo Master) · WORM audit · referential-safe delete.
**Out:** Geo Master feature เอง (consume read-only), stock/on-hand (F-INV-STOCK), DOA/approval (LD-07), pick_sequence/capacity หลายมิติ/ABC (NICE — เฟสถัดไป), PACK↔Ship dock flow (pick-pack-ship feature).

## §0.3 Roles
Warehouse Manager (full + delete), Supervisor (create/edit ทุกระดับ, ไม่ลบ), Operator (view + scan), Inventory Controller (view + location status block/freeze), Admin (config + Geo Master). **RBAC only — no DOA** (LD-07). SoD: delete = Manager/Admin ≠ Supervisor (creator).

## §0.4 Pages (from BRD §14.6)
| Page | Route / Surface | Layout Template ID |
|---|---|---|
| Hierarchy (List view) | `#/hierarchy` (default) | `A_list-view` (drill-down) |
| Hierarchy (Tree view) | `#/hierarchy` + view=tree | **NON-STANDARD** (tree + node summary) — LD-09 / OQ |
| Create/Edit WH·Zone·Area·Rack | drawer | `B_create-drawer` |
| Create/Edit Location | drawer (2-step wizard) | `B_create-drawer-wizard` |
| View (location) | drawer (3 tabs) | `C_view-drawer-tabbed` |
| View (WH·Zone·Area·Rack) | drawer | `C_view-drawer` |
| Bulk Generate | drawer (template + preview) | `B_create-drawer-wizard` |
| Delete / Decommission | modal | `D_modal-confirmation` |

## §0.5 Dependencies
Upstream: **Geo Master** (read-only lookup; ดู OQ-1). Downstream: F-INV-STOCK-001 (location_id + `hasStock`), F-GRN/Putaway/RTV, **pick-pack-ship** (PACK type). Engines: `location-generation-engine` (ENG-LOC-GEN), `hierarchy-path-builder` (ENG-HIER-PATH).

## §0.7.1 Data Classification Summary
Highest: **Internal** (operational master — no PII sensitive, no financial). geo_master = **Public** (province/district/subdistrict names เป็นข้อมูลสาธารณะ). Warehouse address components = Internal (corporate location). PII overlay: `created_by`/`modified_by` (user refs). No Confidential / Restricted fields → ไม่ต้อง register Policy Center Restricted Resources.

## §0.8 Open Questions
- **OQ-1:** Geo Master เป็น feature แยก — timeline + schema (77 จังหวัด / 928 อำเภอ / 7,255 ตำบล) + endpoint contract? (BRD Q1; ทดไว้ทำแยก)
- **OQ-2:** Hierarchy Tree view เป็น NON-STANDARD (ไม่มี tree pattern ใน html-generator-v3 A–I) — อนุมัติคงไว้ หรือใช้ List อย่างเดียว? (BRD Q4 / LD-09)
- **OQ-3:** type-driven default behavior (PACK ⇒ not pickable, work location) — auto-set ตั้งแต่ Phase 1 หรือ Phase 3? (BRD Q3 / FN-23)
- **OQ-4:** Deactivate Zone ที่มี Area active → cascade หรือ block? (BRD Q2; default = block)
- **OQ-5:** Re-parent location: enforce empty vs allow live migration? (carry from v1)
