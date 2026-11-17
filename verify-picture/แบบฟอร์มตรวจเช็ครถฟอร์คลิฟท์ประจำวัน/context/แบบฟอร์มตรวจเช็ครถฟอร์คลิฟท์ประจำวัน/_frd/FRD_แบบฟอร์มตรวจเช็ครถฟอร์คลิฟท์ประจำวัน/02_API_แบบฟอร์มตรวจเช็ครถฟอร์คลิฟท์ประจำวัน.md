# 02_API — F-TMP-002
> base `/api/v1/forklift-inspections` · tenant จาก token (RLS) · ทุก write มี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/forklift-inspections?q&status&vehicle_type&mine_to_act&page&sort` | รายการตามสิทธิ์ | FN-11 |
| API-02 | GET `/forklift-inspections/{id}` | รายละเอียด + ผล + chain + audit | FN-11 |
| API-03 | POST `/forklift-inspections` | สร้างร่าง + ออกเลข + snapshot รายการตรวจ | FN-01, FN-02, FN-03 |
| API-04 | PUT `/forklift-inspections/{id}` | บันทึกผล/แก้ (เจ้าของ · draft/returned) | FN-01, FN-02, FN-04 |
| API-05 | GET `/forklift-inspections/{id}/doa-preview` | resolve สายค่าเริ่ม (slot) | FN-05 |
| API-06 | POST `/forklift-inspections/{id}/submit` `{assignees[]}` | ส่ง · snapshot chain | FN-05 |
| API-07 | POST `/forklift-inspections/{id}/decide` `{decision: approve\|reject, note}` | ตัดสินขั้นปัจจุบัน | FN-06, FN-07 |
| API-08 | POST `/forklift-inspections/{id}/cancel` `{reason}` | ยกเลิก | FN-08 |
| API-09 | GET `/forklift-inspections/{id}/pdf` | PDF FM-WHS-04 (2 หน้า) | FN-09 |
| API-10 | GET `/forklift-inspections/export.csv` | CSV ตามตัวกรอง | FN-11 |
| API-11 | POST/DELETE `/forklift-inspections/{id}/attachments` | ไฟล์ (Document Center) | — |
| API-12 | GET `/forklift-checklist-config` | รายการตรวจปัจจุบัน (general/fuel/electric) — อ่านอย่างเดียว | FN-02 |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ vehicle_type, inspection_month:'YYYY-MM', results:[{day, section, item_id, result:'ok'|'ng'}], attachment_ids[] }` → 422 ตาม VR-01..04 (`VEHICLE_TYPE_REQUIRED` · `MONTH_INVALID` · `DAY_OUT_OF_RANGE` · `DAY_INCOMPLETE` · `SECTION_NOT_ALLOWED` · `NO_RESULT`)
- API-04: 409 `NOT_EDITABLE` (ไม่ใช่ draft/returned) · 403 `NOT_OWNER`
- API-06: 409 `NOT_DRAFT` · 422 `ASSIGNEE_REQUIRED` · 422 `SELF_APPROVAL` (BR-DOA-04)
- API-07: 403 `NOT_CURRENT_APPROVER` · 422 `REASON_REQUIRED` (reject)
- API-08: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/role-mgr-wh) · 409 `NOT_CANCELLABLE` (approved/cancelled)
- API-02 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)

## §2.3 Common
Idempotency-Key ทุก POST · optimistic lock `version` → 409 STALE · audit ทุก write (append-only) · multi-tenant RLS

## §2.4 API → Logic Trace
ดูตาราง §2.1 คอลัมน์ Logic (ครบทุก API)

## §2.X Cross-Module Contract
| ปลายทาง | Event/Call | Payload | รอบนี้ |
|---|---|---|---|
| ENG-NOTIFY | fli_defect_found · fli_cancelled | {ref: inspection_id, vars} | ✓ |
| ENG-DOC-STORE | store(pdf,'FLI',id,'approved_final') | | ✓ |
| Asset / Maintenance | `fli.defect_recorded` {inspection_id, day, item_id} | | ประกาศ ไม่ยิง (DEC-02) |
