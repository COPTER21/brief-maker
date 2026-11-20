# 02_API — F-TMP-003
> base `/api/v1/project-screenings` · tenant จาก token (RLS) · ทุก write ต้องมี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/project-screenings?q&status&decision&dept&mine_to_act&page&size&sort` | รายการตามสิทธิ์ | FN-10 |
| API-02 | GET `/project-screenings/{id}` | รายละเอียด + criteria + chain + audit | FN-10 |
| API-03 | POST `/project-screenings` | สร้างร่าง + ออกเลข + snapshot เกณฑ์/น้ำหนัก | FN-01, FN-02, FN-03 |
| API-04 | PUT `/project-screenings/{id}` | แก้ร่าง (เจ้าของ · draft) | FN-01, FN-02 |
| API-05 | GET `/project-screenings/{id}/doa-preview` | resolve สายค่าเริ่ม (slot) | FN-04 |
| API-06 | POST `/project-screenings/{id}/submit` `{assignees[]}` | ส่ง · snapshot chain | FN-04 |
| API-07 | POST `/project-screenings/{id}/decide` `{decision: approve\|reject, note}` | ตัดสินขั้นปัจจุบัน | FN-05, FN-06 |
| API-08 | POST `/project-screenings/{id}/cancel` `{reason}` | ยกเลิก | FN-07 |
| API-09 | GET `/project-screenings/{id}/pdf` | PDF FM-BDM-03 (2 หน้า) | FN-08 |
| API-10 | GET `/project-screenings/export.csv` | CSV ตามตัวกรอง | FN-10 |
| API-11 | POST/DELETE `/project-screenings/{id}/attachments` | ไฟล์ (Document Center) | — |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ criteria:[{criterion_key, score, rationale, risk_condition}], summary:{strengths, concerns, info_needed, decision, conditions, next_steps}, attachment_ids[] }` · weight / weighted_score / total_score / recommendation ไม่รับจาก FE (server คำนวณ FN-02) · 422 ตาม VR-01..03 (ตามจอ: ตรวจครบก่อนบันทึกร่างและก่อนส่ง)
- API-06: 409 `NOT_DRAFT` · 422 `ASSIGNEE_REQUIRED` · 422 `SELF_APPROVAL` (BR-DOA-04)
- API-07: 403 `NOT_CURRENT_APPROVER` · 422 `REASON_REQUIRED` (reject) · approve ขั้นสุดท้าย → FN-09 scr_not_proceed_approved เมื่อ decision = ไม่ดำเนินการต่อ
- API-08: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/admin) · 409 `NOT_CANCELLABLE` (approved/cancelled) → FN-09 scr_cancelled (ถ้าเดิม pending)
- API-02 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)
- response มี `weighted_score` ต่อเกณฑ์ · `total_score` · `recommendation` · `decision_mismatch` (bool เตือน)

## §2.3 Common
Idempotency-Key ทุก POST · optimistic lock `version` → 409 STALE · audit ทุก write (append-only) · multi-tenant RLS

## §2.4 API → Logic Trace
ดูตาราง §2.1 คอลัมน์ Logic (ครบทุก API)

## §2.X Cross-Module Contract
| ปลายทาง | Event/Call | Payload | รอบนี้ |
|---|---|---|---|
| ENG-NOTIFY | scr_cancelled · scr_not_proceed_approved | {ref: project_screening_id, vars} | ✓ |
| ENG-DOC-STORE | store(pdf,'SCR',id,'approved_final') | | ✓ |
| ระบบอื่น / FM-BDM-04 | — | | ไม่ส่งต่อ (DEC-02) |
