# 02_API — F-TMP-004
> base `/api/v1/vendor-evaluations` · tenant จาก token (RLS) · ทุก write มี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/vendor-evaluations?q&status&result&mine_to_act&page&sort` | รายการตามสิทธิ์ | FN-11 |
| API-02 | GET `/vendor-evaluations/{id}` | รายละเอียด + คะแนน + chain + audit | FN-11 |
| API-03 | POST `/vendor-evaluations` | สร้างร่าง + ออกเลข + snapshot เกณฑ์ | FN-01, FN-02, FN-03 |
| API-04 | PUT `/vendor-evaluations/{id}` | แก้ไข (เจ้าของ · draft/returned) | FN-01, FN-04 |
| API-05 | GET `/vendor-evaluations/{id}/doa-preview` | resolve สายค่าเริ่มตามผลประเมิน (slot) | FN-05 |
| API-06 | POST `/vendor-evaluations/{id}/submit` `{assignees[]}` | ส่ง · snapshot chain | FN-01, FN-05 (+FN-10) |
| API-07 | POST `/vendor-evaluations/{id}/decide` `{decision: approve\|reject, note}` | ตัดสินขั้นปัจจุบัน | FN-06, FN-07 |
| API-08 | POST `/vendor-evaluations/{id}/cancel` `{reason}` | ยกเลิก | FN-08 |
| API-09 | GET `/vendor-evaluations/{id}/pdf` | PDF FM-PUR-01 (2 หน้า) | FN-09 |
| API-10 | GET `/vendor-evaluations/export.csv` | CSV ตามตัวกรอง | FN-11 |
| API-11 | POST/DELETE `/vendor-evaluations/{id}/attachments` | ไฟล์ (Document Center) | — |
| API-12 | GET `/vendor-evaluation-config` | หัวข้อ/คะแนนเต็ม/เกณฑ์ผ่าน/มาตรฐานปัจจุบัน — อ่านอย่างเดียว | FN-02 |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ vendor_name, vendor_code, supply_goods, goods_specific, supply_service, service_specific, reference_no, credit_term, scores:[{criterion_id, score:'2.5'}], certifications:['iso',...], cert_other_text, evaluator_comment, attachment_ids[] }` → 422 ตาม VR (`VENDOR_NAME_REQUIRED` · `VENDOR_CODE_REQUIRED` · `SCORE_FORMAT` · `SCORE_OVER_MAX` · `CERT_OTHER_REQUIRED`) · ร่างไม่บังคับคะแนนครบ · ตอบกลับมี `score_total`, `eval_result`, `duplicate_in_year[]` (เตือน)
- API-04: 409 `NOT_EDITABLE` (ไม่ใช่ draft/returned) · 403 `NOT_OWNER`
- API-06: 422 `SCORE_INCOMPLETE` · 422 `SUPPLY_TYPE_REQUIRED` · 422 `SUPPLY_SPEC_REQUIRED` · 409 `NOT_DRAFT` · 422 `ASSIGNEE_REQUIRED` · 422 `SELF_APPROVAL` (BR-DOA-04)
- API-07: 403 `NOT_CURRENT_APPROVER` · 422 `REASON_REQUIRED` (reject)
- API-08: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/role-mgr-pur) · 409 `NOT_CANCELLABLE` (approved/cancelled)
- API-02 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)
- score ส่งเป็น string ทศนิยม (กัน float) · server คำนวณ `score_total`/`eval_result` เอง ไม่รับจาก client

## §2.3 Common
Idempotency-Key ทุก POST · optimistic lock `version` → 409 STALE · audit ทุก write (append-only) · multi-tenant RLS

## §2.4 API → Logic Trace
ดูตาราง §2.1 คอลัมน์ Logic (ครบทุก API)

## §2.X Cross-Module Contract
| ปลายทาง | Event/Call | Payload | รอบนี้ |
|---|---|---|---|
| ENG-NOTIFY | vev_evaluation_failed · vev_cancelled | {ref: evaluation_id, vars} | ✓ |
| ENG-DOC-STORE | store(pdf,'VEV',id,'approved_final') | | ✓ |
| DOA (F-DLG-001) | resolve(feature_id=F-TMP-004, context{eval_result}) | | ✓ (เงื่อนไขผล = TODO: DOA engine) |
| Master › Supplier/Vendor | `vev.evaluation_approved` {evaluation_id, vendor_code, eval_result, score_total, certifications} | | ประกาศ ไม่ยิง (DEC-02) |
