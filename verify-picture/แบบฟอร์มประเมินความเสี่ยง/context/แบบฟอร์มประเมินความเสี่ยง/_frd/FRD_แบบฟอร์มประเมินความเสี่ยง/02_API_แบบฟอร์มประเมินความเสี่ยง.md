# 02_API — F-TMP-002
> base `/api/v1/risk-assessments` · tenant จาก token (RLS) · ทุก write ต้องมี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/risk-assessments?q&status&level&dept&mine_to_act&page&size&sort` | รายการตามสิทธิ์ | FN-10 |
| API-02 | GET `/risk-assessments/{id}` | รายละเอียด + items + chain + audit | FN-10 |
| API-03 | POST `/risk-assessments` | สร้างร่าง + ออกเลข | FN-01, FN-02, FN-03 |
| API-04 | PUT `/risk-assessments/{id}` | แก้ร่าง (เจ้าของ · draft) | FN-01, FN-02 |
| API-05 | GET `/risk-assessments/{id}/doa-preview` | resolve สายค่าเริ่ม (slot) | FN-04 |
| API-06 | POST `/risk-assessments/{id}/submit` `{assignees[]}` | ส่ง · snapshot chain | FN-04 |
| API-07 | POST `/risk-assessments/{id}/decide` `{decision: approve\|reject, note}` | ตัดสินขั้นปัจจุบัน | FN-05, FN-06 |
| API-08 | POST `/risk-assessments/{id}/cancel` `{reason}` | ยกเลิก | FN-07 |
| API-09 | GET `/risk-assessments/{id}/pdf` | PDF FM-BDM-02 (2 หน้า) | FN-08 |
| API-10 | GET `/risk-assessments/export.csv` | CSV ตามตัวกรอง | FN-10 |
| API-11 | POST/DELETE `/risk-assessments/{id}/attachments` | ไฟล์ (Document Center) | — |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ items:[{category, description, cause_effect, likelihood, impact, control_measure, residual_score, status}], attachment_ids[] }` · inherent_score ไม่รับจาก FE (server คำนวณ FN-02) · 422 ตาม VR-01..02
- API-06: 409 `NOT_DRAFT` · 422 `ASSIGNEE_REQUIRED` · 422 `SELF_APPROVAL` (BR-DOA-04)
- API-07: 403 `NOT_CURRENT_APPROVER` · 422 `REASON_REQUIRED` (reject)
- API-08: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/admin) · 409 `NOT_CANCELLABLE` (approved/cancelled)
- API-02 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)
- response item มี `inherent_score` · `level_key` (จาก RiskMatrix.level_bands ณ เวลาอ่าน) · `residual_over_inherent` (bool เตือน)

## §2.3 Common
Idempotency-Key ทุก POST · optimistic lock `version` → 409 STALE · audit ทุก write (append-only) · multi-tenant RLS

## §2.4 API → Logic Trace
ดูตาราง §2.1 คอลัมน์ Logic (ครบทุก API)

## §2.X Cross-Module Contract
| ปลายทาง | Event/Call | Payload | รอบนี้ |
|---|---|---|---|
| ENG-NOTIFY | rsk_cancelled · rsk_very_high_approved | {ref: risk_assessment_id, vars} | ✓ |
| ENG-DOC-STORE | store(pdf,'RSK',id,'approved_final') | | ✓ |
| ระบบอื่น | — | | ไม่ส่งต่อ (DEC-02) |
