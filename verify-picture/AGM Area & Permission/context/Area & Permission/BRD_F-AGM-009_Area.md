# BRD — F-AGM-009 Area & Permission Management (พื้นที่และการกำหนดสิทธิ์)

> Constraint mode (จาก invariants.md 🔒) · Module เกษตรกรรม (AGM)/การบริหาร · WKN · สถานะ: APPROVED

## §1 Business Context
โมดูล **org-geography + RBAC backbone** ของทั้งระบบ AGM — นิยามพื้นที่ปฏิบัติการ (Area) ตามโครงภูมิศาสตร์ (จังหวัด→อำเภอ→ตำบล), ผูกรหัสต่อสาย (Extension Code) กับพื้นที่, และมอบหมายบทบาท (Area Head, Director, Extension Officer) จากพนักงาน ERP. พื้นที่เป็น scope container ที่ Farmer (F-AGM-001) / Quota (F-AGM-002) อ้างอิง และ role คุมสิทธิ์ทั้ง chain.

## §2 Problem / Opportunity
ของเดิม (React prototype) มี model + RBAC ครบแต่ UI shadcn slate, edit/assign เป็น stub, ไม่มี stats. Refactor → CUBE Warm Light + governance (deactivate guard, RBAC write-gate, audit trail, optimistic lock) และเชื่อม chain AGM.

## §3 Goals & Scope
### §3.4 Locked Decisions (LOCK — จาก invariants)
| LOCK | Decision |
|---|---|
| LOCK-01 | คงพฤติกรรม AS-BUILT 100% (entities, enums, validation, RBAC) |
| LOCK-02 | **Deactivate guard**: ปิดใช้งานพื้นที่ที่ codes_count > 0 ไม่ได้ (BR-01) |
| LOCK-03 | **Geography cascade**: จังหวัด→อำเภอ→ตำบล→รหัสไปรษณีย์ auto-fill (BR-02) |
| LOCK-04 | Extension Code = 4 หลัก · ผูก Active area เท่านั้น (BR-03/validation) |
| LOCK-05 | Code EMPTY↔OCCUPIED ผ่าน assign/unassign พนักงาน (BR-04) |
| LOCK-06 | **Extension Officer = code assignment** (ไม่ใช่ role โดยตรง) (BR-05) |
| LOCK-07 | เพิ่ม head/director/officer ได้เฉพาะ ErpEmployee status=active (BR-06) |
| LOCK-08 | **RBAC write-gate**: create/edit/toggle/roles = เฉพาะ System Admin/Director · อื่น read-only · Roles tab ซ่อน (BR-07) |
| LOCK-09 | Optimistic lock (version) + idempotency key ทุก mutation (BR-08) |
| LOCK-10 | Audit trail (before/after snapshot) ทุก action (BR-09) |
| LOCK-11 | People เลือกจาก ERP (searchErpEmployees ชื่อ/รหัส/email) — ไม่สร้างคนใหม่ (BR-10) |

### Out of Scope
Edit area / assign-unassign-reassign officer เต็มรูป (stub) · snapshot diff view · server-side RBAC enforcement · Payment-run/accrual (ไม่เกี่ยว).

## §4 Entities & State
- **Area** (พื้นที่ uuid): Active/Inactive · aggregate ของ heads + codes · version
- **ExtensionCode** (รหัสต่อสาย 4 หลัก): EMPTY/OCCUPIED · ผูก 1 area · assign → Extension Officer
- **AreaHead / Director**: บทบาท map ERP employee → area/global
- **AuditEntry**: action/actor/details + snapshot
State machine → invariants §4.

## §5 Key Business Rules
BR-01..11 (invariants §3). สำคัญ: deactivate guard (BR-01), geography cascade (BR-02), RBAC write-gate SA/Director (BR-07), active-employee-only (BR-06), optimistic+idempotent (BR-08), audit trail (BR-09).

## §6 Functional Requirements (สรุป → FRD)
1. **US-01 Areas List** — ค้นหา (ชื่อ/รหัส) · กรอง จังหวัด+สถานะ · Export CSV · pagination 25 · bulk select · stats
2. **US-02 Area Create** — geography cascade + postal auto-fill · RBAC gated
3. **US-03 Area Detail** — 4 แท็บ (Overview/Area Heads/Extension Codes/Audit) + toggle status (guard) + edit
4. **US-04 Area Heads** — เพิ่ม (ERP search, active-only) / ลบ (confirm)
5. **US-05 Extension Codes** — สร้าง (4-digit + Active area) · EMPTY/OCCUPIED + assigned
6. **US-06 Roles (SA/Director)** — Directors (เพิ่ม/ลบ) · Area Heads (global) · Extension Officers (codes cross-area + filter)
7. **US-07 Audit** — timeline ต่อ area (action/actor/details)
8. **US-08 RBAC** — write-gate + Roles-tab visibility ตามบทบาท
9. **US-09 Cross-module** — Areas scope Farmer/Quota · people จาก ERP

## §7 Non-Functional
list p95<3s · action<1s · RBAC (5 roles) · optimistic lock + idempotency · audit immutable · geography integrity · CSV ไทย.

## §18 Stats (list dashboard)
4 การ์ด: พื้นที่ทั้งหมด · เปิดใช้งาน (Active) · Extension Codes รวม (+ OCCUPIED) · Area Heads รวม.

## §Cross-Module Map
```
ERP HR ──read(employees)──▶ Area & Permission (heads/directors/officers)
Geography masters ──read──▶ Area (province→district→subdistrict→postal)
Area (F-AGM-009) ──scope──▶ Farmer (F-AGM-001) / Quota (F-AGM-002)
Roles (RBAC) ──gate──▶ AGM chain ทั้งหมด (write permissions)
```
