# 00_OVERVIEW — F-AGM-009 Area & Permission Management

## §0.1 Identity
| | |
|---|---|
| Feature ID | F-AGM-009 |
| ชื่อ | พื้นที่และการกำหนดสิทธิ์ (Area & Permission Management) |
| Module | เกษตรกรรม (AGM)/การบริหาร · WKN |
| Pack | FRD_F-AGM-009_Pack (7 ไฟล์ STANDARD) |
| Reverse | RIF v2 + invariants.md 🔒 (T3 code-only) |
| BRD | BRD_F-AGM-009 APPROVED (LOCK-01..11) |

## §0.2 Purpose
Org-geography + RBAC backbone ของ AGM — Area (จังหวัด→อำเภอ→ตำบล) + Extension Code (4-digit, EMPTY/OCCUPIED) + Roles (Director/Area Head/Extension Officer) จาก ERP. Areas scope Farmer/Quota; roles gate ทั้ง chain.

## §0.3 Scope
In: Areas (list/create/detail 4 tabs/toggle) · Area Heads (add/remove) · Extension Codes (create/assign) · Roles (Directors/Area Heads/Extension Officers) · Audit. Out: edit/assign stub เต็มรูป, snapshot diff, server RBAC enforcement.

## §0.4 Entities
Area (uuid) · ExtensionCode (4-digit) · Assignment · AreaHead · Director · ErpEmployee (read) · AuditEntry · Province/District/Subdistrict (masters). → 04_DB.

## §0.5 Actors / RBAC
System Admin/Director (read+write) · Area Head/Extension Officer/Audit-QA (read-only). Write-gate = hasPermission(['System Admin','Director']). → 05_RULES §5.3 + invariants §6.

## §0.6 Cross-Module
read ERP HR (employees) + Geography masters · **Areas scope** Farmer (F-AGM-001)/Quota (F-AGM-002) · **Roles gate** AGM chain.

## §0.11 Scope Lock (← BRD §3.4)
LOCK-01..11. สำคัญ: deactivate guard (05), geography cascade (01/03), RBAC write-gate (05), optimistic+idempotent (03/04), audit (04).

## §0.7 Pages (→ 01_UI)
P-01 Areas List · P-02 Area Detail (4 tabs) · P-03 Roles (3 sub-tabs) · OV create-area · OV add-head · OV create-code · OV add-director.

## §0.8 Open Questions
OQ-01 edit/assign stub · OQ-02 snapshot diff · OQ-03 server RBAC · OQ-04 Area↔Farmer/Quota FK (invariants §8).
