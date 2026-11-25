# 02_API — F-TMP-001
> base `/api/v1/asset-repair-requests` · tenant จาก token (RLS) · ทุก write ต้องมี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/asset-repair-requests?q&status&returned&dept&mine_to_act&page&sort` | รายการตามสิทธิ์ | FN-10 |
| API-02 | GET `/asset-repair-requests/{id}` | รายละเอียด + items + history + chain + audit | FN-10 |
| API-03 | POST `/asset-repair-requests` | สร้างร่าง + ออกเลข | FN-01, FN-03 |
| API-04 | PUT `/asset-repair-requests/{id}` | แก้ร่าง (เจ้าของ · draft) | FN-01 |
| API-05 | GET `/asset-repair-requests/{id}/doa-preview` | resolve สายค่าเริ่ม (slot) | FN-04 |
| API-06 | POST `/asset-repair-requests/{id}/submit` `{assignees[]}` | ส่ง · snapshot chain | FN-04 |
| API-07 | POST `/asset-repair-requests/{id}/decide` `{decision: approve\|reject, note, reason, history[]}` | ตัดสินขั้นปัจจุบัน (ขั้นแรกส่ง history ได้) | FN-02, FN-05, FN-06 |
| API-08 | POST `/asset-repair-requests/{id}/cancel` `{reason}` | ยกเลิก | FN-07 |
| API-09 | GET `/asset-repair-requests/{id}/pdf` | PDF FM-ASM-03 | FN-08 |
| API-10 | GET `/asset-repair-requests/export.csv` | CSV ตามตัวกรอง | FN-10 |
| API-11 | POST/DELETE `/asset-repair-requests/{id}/attachments` | ไฟล์ (Document Center) | — |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ items:[{description, asset_code, qty, symptom, location, remark}], attachment_ids[] }` · qty = integer → 422 ตาม VR-01/02
- API-06: 409 `NOT_DRAFT` · 422 `ASSIGNEE_REQUIRED` · 422 `SELF_APPROVAL` (BR-DOA-04)
- API-07: 403 `NOT_CURRENT_APPROVER` · 422 `REASON_REQUIRED` (reject) · 422 `HISTORY_INVALID` (repair_count ไม่ใช่จำนวนเต็ม ≥0 · VR-05) · `history[]` รับเฉพาะขั้นแรกของสาย (ขั้นอื่นส่งมา = ไม่สนใจ)
- API-08: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/admin) · 409 `NOT_CANCELLABLE` (approved/cancelled)
- API-02 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)
- API-03 เมื่อ doc_type RPR ปิดใช้ที่ F-DOCCFG → 409 `DOC_TYPE_INACTIVE`

## §2.3 Common
Idempotency-Key ทุก POST · optimistic lock `version` → 409 STALE · audit ทุก write (append-only) · multi-tenant RLS

## §2.4 Events (ENG-NOTIFY · NTF_BRIEF_F-TMP-001)
- `rpr_cancelled` — pending → cancelled (API-08) → ผู้พิจารณาขั้นปัจจุบัน
- `rpr_ready_for_repair` — → approved (API-07) → admin role ฝ่ายบริหารสินทรัพย์
- `rpr.approved` (domain event สำหรับ Maintenance Schedule/Asset Master) — ประกาศไว้ **ไม่ยิงรอบนี้** (DEC-02)
- doa_pending / doa_result / doa_escalate = DOA engine (ห้ามยิงซ้ำ)

## §2.5 API → Logic Trace
ดูตาราง §2.1 คอลัมน์ Logic (ครบทุก API)
