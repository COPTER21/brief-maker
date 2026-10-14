# 03_LOGIC — F-AGM-009 Area & Permission Management

> R8: mutation API → ≥1 Function · RBAC + guard centralized · no HTTP in function

## §3.1 Functions
| FN | Name | Purpose | Invoked by |
|---|---|---|---|
| FN-01 | `buildAreaListQuery` | list + filter(province/status) + stats + page(25) | API-01 |
| FN-02 | `createArea` | validate geography cascade + postal + audit | API-02 |
| FN-03 | `updateArea` | แก้ไข + optimistic(version) + audit | API-04 |
| FN-04 | `toggleAreaStatus` ⭐ | Active↔Inactive · **deactivate guard (codes_count>0 → block)** + audit | API-05 |
| FN-H | `manageAreaHead` | add(active-employee)/remove(confirm) + idempotent + audit | API-H1/H2 |
| FN-C | `manageExtensionCode` ⭐ | create(4-digit + Active area) · assign→OCCUPIED · unassign→EMPTY + audit | API-C1/C3/C4 |
| FN-D | `manageDirector` | add(active-employee)/remove + audit | API-D1/D2 |
| FN-GEO | `resolveGeography` | province→district→subdistrict→postal (getPostalCode) | API-GEO, FN-02 |
| FN-ERP | `searchErpEmployees` | ค้นพนักงาน (ชื่อ/รหัส/email, active) | API-ERP, dialogs |
| FN-AUDIT | `recordAudit` ⭐ | append AuditEntry (before/after snapshot) | ทุก FN mutation |
| FN-RBAC | `guardPermission` ⭐ | hasPermission(role, ['System Admin','Director']) → 403 ถ้าไม่ผ่าน | ทุก write FN |
| FN-LOCK | `guardOptimistic` | If-Match version + X-Idempotency-Key | ทุก mutation |

## §3.2 Engines
- **ENG-EXT-ERP** `erp-employee-connector` [read] — พนักงาน ERP HR (active)
- **ENG-GEO** `geography-master` [read] — จังหวัด/อำเภอ/ตำบล/postal cascade
- **ENG-AUDIT** `audit-logger` ⭐ — append-only + before/after snapshot (REVOKE UPDATE/DELETE)
- **ENG-RBAC** `permission-guard` ⭐ — role-based write-gate (server enforce)

## §3.3 API ↔ Logic Trace (R8)
| API | Functions |
|---|---|
| API-01 | FN-01 |
| API-02 | FN-02,GEO,RBAC,LOCK,AUDIT |
| API-04 | FN-03,RBAC,LOCK,AUDIT |
| API-05 | FN-04,RBAC,AUDIT |
| API-H1/H2 | FN-H,ERP,RBAC,LOCK,AUDIT |
| API-C1/C3/C4 | FN-C,RBAC,LOCK,AUDIT |
| API-D1/D2 | FN-D,ERP,RBAC,AUDIT |
| API-ERP/GEO | FN-ERP/GEO |
> ทุก write มี FN + FN-RBAC guard + FN-AUDIT + FN-LOCK ✅

## §3.5 Locked Decisions
- LOCK-02: FN-04 deactivate guard (codes>0)
- LOCK-03: FN-GEO cascade + postal auto
- LOCK-04/05: FN-C 4-digit + Active area + EMPTY↔OCCUPIED
- LOCK-06: Extension Officer = code assignment (FN-C, ไม่ใช่ role table)
- LOCK-07: FN-H/FN-D active-employee-only
- LOCK-08: FN-RBAC write-gate SA/Director (403)
- LOCK-09: FN-LOCK optimistic+idempotent
- LOCK-10: FN-AUDIT before/after snapshot
