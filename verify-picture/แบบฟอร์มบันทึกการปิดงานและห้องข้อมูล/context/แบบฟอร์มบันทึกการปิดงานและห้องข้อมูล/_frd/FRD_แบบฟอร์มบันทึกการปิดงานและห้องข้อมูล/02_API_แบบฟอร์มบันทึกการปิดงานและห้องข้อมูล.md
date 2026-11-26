# 02_API — F-TMP-003
> base `/api/v1/ivm-closings` · tenant จาก token (RLS) · ทุก write ต้องมี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/ivm-closings?q&status&checklist=complete\|open&mine_to_act&page&size&sort` | รายการตามสิทธิ์ | FN-10 |
| API-02 | GET `/ivm-closings/{id}` | รายละเอียด + checks + lessons + chain + audit | FN-10 |
| API-03 | POST `/ivm-closings` | สร้างร่าง + ตั้งต้นรายการตรวจสอบจาก config + ออกเลข | FN-01, FN-03 |
| API-04 | PUT `/ivm-closings/{id}` | แก้ร่าง (เจ้าของ · draft) | FN-01 |
| API-05 | GET `/ivm-closings/{id}/doa-preview` | resolve สายค่าเริ่ม (slot) | FN-04 |
| API-06 | POST `/ivm-closings/{id}/submit` `{assignees[]}` | ตรวจกติกาส่ง + ส่ง · snapshot chain | FN-01, FN-04 |
| API-07 | POST `/ivm-closings/{id}/decide` `{decision: approve\|reject, note}` | ตัดสินขั้นปัจจุบัน | FN-05, FN-06 |
| API-08 | POST `/ivm-closings/{id}/cancel` `{reason}` | ยกเลิก | FN-07 |
| API-09 | GET `/ivm-closings/{id}/pdf` | PDF FM-IVM-11 | FN-08 |
| API-10 | GET `/ivm-closings/export.csv` | CSV ตามตัวกรอง | FN-10 |
| API-11 | POST/DELETE `/ivm-closings/{id}/attachments` | ไฟล์ (Document Center) | FN-02 |
| API-12 | GET `/ivm-closings/checklist-template` | รายการตรวจสอบตั้งต้น (config ivmk.checklist_items · ver) สำหรับฟอร์มใหม่ | FN-03 |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ project_name, closing_date, outcome, post_owner_employee_id, archive_location, checks:[{seq, status:'not_started'|'in_progress'|'done'|'na', owner, done_date, remark}], lessons:[{topic, lesson, owner, due_date}], attachment_ids[] }` → 422 ตาม VR-01..06/09 · `item_text` ไม่รับจาก client (snapshot จาก config ฝั่ง server · ส่งมา = ignore)
- API-06: 409 `NOT_DRAFT` · 422 `CHECKLIST_INCOMPLETE` (VR-07) · 422 `LESSON_REQUIRED` (VR-08) · 422 `ASSIGNEE_REQUIRED` · 422 `SELF_APPROVAL` (BR-DOA-04)
- API-07: 403 `NOT_CURRENT_APPROVER` · 422 `REASON_REQUIRED` (reject)
- API-08: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/admin) · 409 `NOT_CANCELLABLE` (approved/cancelled)
- API-02 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)
- Events (FN-09): `ivmk_cancelled` · `ivmk_closed_handover` · `ivmk_lesson_assigned` ผ่าน ENG-NOTIFY · `ivmk.approved` ประกาศไว้ไม่ยิง (DEC-02)

## §2.3 Common
Idempotency-Key ทุก POST · optimistic lock `version` → 409 STALE · audit ทุก write (append-only) · multi-tenant RLS

## §2.4 API → Logic Trace
ดูตาราง §2.1 คอลัมน์ Logic (ครบทุก API)
