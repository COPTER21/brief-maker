# 05_RULES — F-AGM-009 Area & Permission Management

## §5.1 Business Rules (→ invariants §3)
| BR | Rule |
|---|---|
| BR-AP-01 | Deactivate guard: ปิดใช้งานพื้นที่ที่ codes_count > 0 ไม่ได้ |
| BR-AP-02 | Geography cascade: จังหวัด→อำเภอ→ตำบล→รหัสไปรษณีย์ auto-fill |
| BR-AP-03 | Extension Code ผูก Active area เท่านั้น |
| BR-AP-04 | Code EMPTY↔OCCUPIED ผ่าน assign/unassign |
| BR-AP-05 | Extension Officer = code assignment (ไม่ใช่ role โดยตรง) |
| BR-AP-06 | เพิ่ม head/director/officer ได้เฉพาะ ErpEmployee active |
| BR-AP-07 | RBAC write-gate: create/edit/toggle/roles = SA/Director เท่านั้น · Roles tab ซ่อน |
| BR-AP-08 | Optimistic (version) + idempotency key ทุก mutation |
| BR-AP-09 | Audit trail (before/after snapshot) ทุก action |
| BR-AP-10 | People จาก ERP (ค้น ชื่อ/รหัส/email) — ไม่สร้างคนใหม่ |
| BR-AP-11 | display_code 4 หลัก · postal 5 หลัก · email format |

## §5.2 State Machine (→ invariants §4)
Area: `Active ⇄ Inactive` (Active→Inactive block ถ้า codes>0)
ExtensionCode: `EMPTY → (assign) → OCCUPIED → (unassign) → EMPTY`

## §5.3 Permission (RBAC matrix → invariants §6)
| Role | Areas | Roles tab | Write |
|---|---|---|---|
| System Admin/Director | read+write | ✅ | ✅ |
| Area Head/Extension Officer/Audit-QA | read | ❌ | ❌ |

## §5.4 Validation
| VR | Rule | Message |
|---|---|---|
| VR-01 | display_code = 4 digits | "รูปแบบหมายเลขโค้ดไม่ถูกต้อง" (desc "กรอกตัวเลข 4 หลัก เช่น 0123") |
| VR-02 | postal_code = 5 digits | (auto-fill; inline) |
| VR-03 | email format | (inline) |
| VR-04 | area required (create code) | "กรุณาเลือกพื้นที่" |
| VR-05 | employee required | "กรุณาเลือกพนักงาน" |
| VR-06 | employee active | "พนักงานไม่active" (desc "ไม่สามารถเพิ่มพนักงานที่ไม่ได้ใช้งาน…") |

## §5.5 Edge Cases
| EC | Case | Expected |
|---|---|---|
| EC-01 | toggle Active→Inactive, codes>0 | block "ไม่สามารถปิดใช้งานพื้นที่ที่มีโค้ดที่ถูกใช้" |
| EC-02 | toggle Inactive→Active | สำเร็จ "เปลี่ยนสถานะสำเร็จ" |
| EC-03 | create code, area Inactive | area ไม่แสดงใน dropdown (filter Active) |
| EC-04 | create code ไม่ใช่ 4 หลัก | VR-01 block |
| EC-05 | add head, employee inactive | VR-06 block |
| EC-06 | add head/director ซ้ำ | idempotent (no dup) |
| EC-07 | non-SA/Director เปิดหน้า | Roles tab ซ่อน · ปุ่ม write ซ่อน/disabled (read-only) |
| EC-08 | geography cascade | เลือกจังหวัด → อำเภอ enable · เลือกอำเภอ → ตำบล enable · เลือกตำบล → postal auto |
| EC-09 | remove head/director | confirm dialog → "ลบ...สำเร็จ" |
| EC-10 | assign code | EMPTY → OCCUPIED (มี assigned) |
| EC-11 | unassign code | OCCUPIED → EMPTY |
| EC-12 | optimistic stale | 409 CONFLICT_UPDATE_STALE (version) |
| EC-13 | idempotent dup | 409/no-op |

## §5.6 Error Catalog
VALIDATION_FAILED · FORBIDDEN(403) "ไม่มีสิทธิ์ดำเนินการ" · AREA_HAS_ACTIVE_CODES(409) "ไม่สามารถปิดใช้งานพื้นที่ที่มีโค้ดที่ถูกใช้" · EMPLOYEE_INACTIVE(400) "พนักงานไม่active" · CONFLICT_UPDATE_STALE(409) "ข้อมูลถูกแก้ไขโดยผู้อื่น กรุณารีเฟรช" · CONFLICT(409) "รายการซ้ำ (idempotent)"
