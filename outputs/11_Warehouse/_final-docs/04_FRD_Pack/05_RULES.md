# 05_RULES — F-LOCATION-MASTER-001 · Warehouse & Bin

> Audience: BE dev + QA. Declarative business rules, validation, edge cases, error catalog, data-classification enforcement.

---

## §5.1 Business Rules (from BRD §9 — traced to FN/API)

| ID | Rule | Tag | Enforced by | Source |
|---|---|:-:|---|---|
| BR-001 | ลำดับชั้น 5 ระดับ WH→Zone→Area→Rack→ตำแหน่ง | 🔒 | schema (04_DB §4.3) | 🤖 |
| BR-002 | location parent = rack **XOR** area | 🔒 | DB CHECK + WHB-FN-07; err `PARENT_XOR_VIOLATION` | 🤖 |
| BR-003 | parent=area ต้อง allows_direct=true | 🔒 | WHB-FN-06; err `ALLOWS_DIRECT_REQUIRED` | 🤖 |
| BR-004 | code unique — WH system-wide, others within parent | 🔒 | DB unique index + WHB-FN-04; err `DUPLICATE_CODE` | 🤖 |
| BR-005 | archive node ที่มีลูก active → block (referential-safe) | 🔒 | WHB-FN-03/FN-05; err `HAS_ACTIVE_CHILDREN` | ✅ D11 |
| BR-006 | capacity cap_val > 0 | 🔒 | DB CHECK + WHB-FN-07; err `CAPACITY_INVALID` | 🤖 |
| BR-007 | ปิด allows_direct ไม่ได้ถ้ามี direct location | 🔒 | WHB-FN-06 (edit); err `ALLOWS_DIRECT_HAS_CHILDREN` | 🤖 |
| BR-008 | temp_controlled → temp range required + min≤max | 🔒 | DB CHECK + WHB-FN-01/02; err `TEMP_RANGE_INVALID` | 🤖 |
| BR-009 | warehouse ต้องมี branch_id (required soft-ref) | 🔒 | WHB-FN-01; err `BRANCH_REQUIRED` | ✅ D3/GC#4 |
| BR-010 | decommission location ต้อง stock=0 | 🔒 | WHB-FN-09/FN-16; err `DECOMMISSION_STOCK_NOT_EMPTY` | ✅ D11/AD-5 |
| BR-011 | ไม่มี hard delete — node=archive, location=decommission (soft) | 🔒 | WHB-FN-03/FN-09 (no DELETE) + WORM | ✅ GC#7/D11 |
| BR-012 | reparent location ที่ stock≠0 → block | 🔒 | WHB-FN-08/FN-16; err `REPARENT_STOCK_NOT_EMPTY` | ✅ AD-5 |
| BR-013 | block location ต้องระบุเหตุผล | 🔒 | WHB-FN-10; err `BLOCK_REASON_REQUIRED` | 🤖 |
| BR-014 | location ต้องมี barcode ก่อน activate (else บันทึก inactive) | ⚙️ CONFIG | WHB-FN-15/FN-10 (`loc_require_barcode`); err `BARCODE_REQUIRED` | ✅ AD-7 |
| BR-015 | bulk generate = preview + collision + atomic (all-or-nothing) | 🔒 | WHB-FN-11/FN-12 + ENG-BULK-PLAN; err `BULK_COLLISION`/`BULK_TEMPLATE_INVALID` | ✅ |
| BR-016 | RBAC role (create=Mgr/Sup/Admin, del=Mgr/Admin, status≠Operator) | ⚙️ CONFIG | perms() gate + server; Permission Matrix system-wide (D8) | ✅ D8 |
| BR-017 | geo cascade: เปลี่ยน parent → reset ลูก + auto postcode | 🔒 | WHB-FN-14 | 🤖 |
| BR-018 | type-driven default behavior flags (auto-apply) | 🔄 DEFERRED | WHB-FN-18 schema-ready — **Phase 3, NOT implemented** | ✅ AD-3 |

## §5.2 Status Machine (BRD §8)
- **Node (WH/Zone/Area/Rack):** `active → archived` (soft, no children active). No hard delete.
- **Location 7-state:** `inactive ⇄ active` (activate needs barcode), `active → full|blocked|frozen|maintenance`, `→ decommissioned` (terminal, stock=0). Table-driven (WHB-FN-17, no hardcode).
- Status labels (verbatim HTML L2027): active=ใช้งาน · inactive=ปิดใช้ · blocked=บล็อก · maintenance=ซ่อมบำรุง · full=เต็ม · frozen=แช่แข็ง · decommissioned=ปลดระวาง · archived=จัดเก็บแล้ว.

## §5.3 Validation
- Required: code, name (all node), branch (WH), cap_val>0, parent (loc). Msgs verbatim: "กรุณากรอกรหัส", "กรุณากรอกชื่อ", "กรุณาเลือกสาขา", "กรุณาเลือกคลัง/โซน/พื้นที่/ชั้นวาง", "ความจุต้องมากกว่า 0". Aggregate: "กรุณากรอกข้อมูลให้ครบถ้วน".
- Uniqueness = **DB-enforced** (not client-only) — EC-15.

## §5.4 Edge Cases

### Implemented in prototype (☑, BRD §10.1)
| EC | Case | Handling |
|---|---|---|
| EC-01 | flexible-parent violation (rack+area both) | DB CHECK XOR block (BR-002) |
| EC-02 | allows_direct=false chosen | inline-warn + link "เพิ่มชั้นวางในพื้นที่นี้ก่อน" (suggestAddRack) |
| EC-03 | referential-safe archive (child active) | block `HAS_ACTIVE_CHILDREN` (BR-005) |
| EC-04 | decommission stock≠0 | block `DECOMMISSION_STOCK_NOT_EMPTY` (BR-010) |
| EC-05 | reparent stock≠0 | block `REPARENT_STOCK_NOT_EMPTY` (BR-012) |
| EC-06 | bulk-gen collision | atomic rollback ทั้งชุด (BR-015) |
| EC-07 | code ซ้ำ (WH system / others parent) | `DUPLICATE_CODE` 409 (BR-004) |
| EC-08 | ปิด allows_direct ทั้งที่มี direct loc | block (BR-007) |
| EC-09 | zone temp missing / min>max | block `TEMP_RANGE_INVALID` (BR-008) |
| EC-10 | geo cascade reset on parent change | WHB-FN-14 reset + auto postcode |
| EC-11 | activate location ไม่มี barcode | block `BARCODE_REQUIRED` (BR-014) |
| EC-12 | Operator = view only | buttons disabled + tooltip (BR-016) |
| EC-13 | Supervisor/Controller archive/decommission | 403 `FORBIDDEN_ROLE` (SoD, BR-016) |

### AI-suggested (☐ — `[AI-DEFAULT]`, BA confirm at SOW3.7)
| EC | Case | Default |
|---|---|---|
| EC-14 | soft-ref (branch/geo) code not-found | show stored code + inline warn "ไม่พบใน master" (conservative); no hard fail — OQ-4 |
| EC-15 | 2 users same code concurrent | DB unique index → 409 `DUPLICATE_CODE` (PR-1) — OQ-7 |
| EC-16 | archive node with already-archived children | childCount counts **active only** → not blocked (matches HTML L3167) |
| EC-17 | bulk-gen huge (rows×cols×levels) | soft cap ~500/atomic batch (SLA §17.1); confirm perf — OQ-5 |
| EC-18 | full_path when parent renamed | downstream re-reads path (contract); emit no separate event, path recomputed on read — OQ (cache contract) |

## §5.5 Error Catalog (UPPER_SNAKE)
`MISSING_REQUIRED` 400 · `BRANCH_REQUIRED` 400 · `DUPLICATE_CODE` 409 · `TEMP_RANGE_INVALID` 400 · `PARENT_XOR_VIOLATION` 400 · `ALLOWS_DIRECT_REQUIRED` 400 · `ALLOWS_DIRECT_HAS_CHILDREN` 409 · `CAPACITY_INVALID` 400 · `HAS_ACTIVE_CHILDREN` 409 · `DECOMMISSION_STOCK_NOT_EMPTY` 409 · `REPARENT_STOCK_NOT_EMPTY` 409 · `BARCODE_REQUIRED` 409 · `BLOCK_REASON_REQUIRED` 400 · `BULK_TEMPLATE_INVALID` 400 · `BULK_COLLISION` 409 · `FORBIDDEN_ROLE` 403 · `NOT_FOUND` 404.

## §5.6 Deferred Rules (Phase 3)
BR-018 `applyTypeDefaults` — schema-ready contract only; **must NOT implement in Phase 1** (BRD §14.2). Confirm type→flags map at OQ-3 before enabling. Also candidate: default-location-per-warehouse (D9, defer to pick-pack-ship).

## §5.7 Data Classification Enforcement (D-CLASS)
- Highest level = **Internal** (§0.7.1). Enforcement: **DB** (RBAC + IDOR on id) · **API** (role gate every mutation) · **UI** (perms() button gating §1.4) · **Audit** (WORM append-only, every mutation logged). Geo = Public (read). No Confidential/Restricted → no Restricted Resources wire. PII overlay = actor cols only.
