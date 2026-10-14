# 02_API — F-AGM-009 Area & Permission Management

> REST `/api/agm/*` · headers: X-Idempotency-Key, If-Match(version), X-Trace-Id · R8: mutation → Function · RBAC enforce server-side

## §2.1 Endpoints
| API | Method | Path | Purpose |
|---|---|---|---|
| API-01 | GET | /areas | list search/filter(province,status)/page(25) + stats |
| API-02 | POST | /areas | สร้างพื้นที่ (geography + postal) |
| API-03 | GET | /areas/:id | detail (+heads/codes/audit counts) |
| API-04 | PUT | /areas/:id | แก้ไข (If-Match version) |
| **API-05** | POST | /areas/:id/toggle-status | Active↔Inactive (**deactivate guard codes>0**) |
| API-06 | GET | /areas/export | export CSV |
| **API-H1** | POST | /areas/:id/heads | เพิ่มหัวหน้า (X-Idempotency-Key, active-employee) |
| **API-H2** | DELETE | /areas/:id/heads/:emp | ลบหัวหน้า (confirm) |
| API-H3 | GET | /areas/:id/heads | list heads |
| **API-C1** | POST | /extension-codes | สร้างโค้ด (4-digit, Active area) |
| API-C2 | GET | /extension-codes?area=&status= | list codes (cross-area filter) |
| **API-C3** | POST | /extension-codes/:id/assign | assign employee → OCCUPIED |
| **API-C4** | POST | /extension-codes/:id/unassign | unassign → EMPTY |
| API-A1 | GET | /areas/:id/audit | audit timeline |
| **API-D1** | POST | /roles/directors | เพิ่ม Director (active-employee) |
| API-D2 | DELETE | /roles/directors/:emp | ลบ Director |
| API-D3 | GET | /roles/directors | list |
| API-ERP | GET | /erp/employees?q= | ค้นพนักงาน (ชื่อ/รหัส/email, active) |
| API-GEO | GET | /geo/{provinces\|districts?province=\|subdistricts?district=} | geography cascade + postal |

## §2.X Contracts ⭐
- **RBAC:** ทุก write (API-02/04/05/H1/H2/C1/C3/C4/D1/D2) → require role ∈ {System Admin, Director} · อื่น 403 FORBIDDEN (BR-07)
- **API-05 toggle:** Active→Inactive & codes_count>0 → **409 AREA_HAS_ACTIVE_CODES** "ไม่สามารถปิดใช้งานพื้นที่ที่มีโค้ดที่ถูกใช้" (BR-01) · Inactive→Active เสมอได้
- **API-02/04:** geography validate (province→district→subdistrict consistent · postal 5-digit from subdistrict) · optimistic (If-Match version)
- **API-C1:** display_code `^\d{4}$` (400 ถ้าไม่ผ่าน "รูปแบบหมายเลขโค้ดไม่ถูกต้อง") · area ต้อง Active · unique (area, display_code)
- **API-C3/C4:** assign → OCCUPIED (มี assigned) · unassign → EMPTY · idempotent
- **API-H1/D1:** employee ต้อง status=active (400 "พนักงานไม่active") · idempotent (X-Idempotency-Key)
- **All mutations:** emit AuditEntry (before/after snapshot) + optimistic (version)

## §2.2 ตัวอย่าง
```
POST /api/agm/areas/{id}/toggle-status   (If-Match: version=3)
→ 409 { "error":"AREA_HAS_ACTIVE_CODES", "message":"ไม่สามารถปิดใช้งานพื้นที่ที่มีโค้ดที่ถูกใช้" }
```
Events: `area.created|updated|status.changed` · `area.head.added|removed` · `ext_code.created|assigned|unassigned` · `role.director.added|removed`

## §2.3 Errors → 05_RULES §5.6
VALIDATION_FAILED · FORBIDDEN(403 RBAC) · AREA_HAS_ACTIVE_CODES(409) · EMPLOYEE_INACTIVE(400) · CONFLICT_UPDATE_STALE(409 version) · CONFLICT(409 dup idempotency)
