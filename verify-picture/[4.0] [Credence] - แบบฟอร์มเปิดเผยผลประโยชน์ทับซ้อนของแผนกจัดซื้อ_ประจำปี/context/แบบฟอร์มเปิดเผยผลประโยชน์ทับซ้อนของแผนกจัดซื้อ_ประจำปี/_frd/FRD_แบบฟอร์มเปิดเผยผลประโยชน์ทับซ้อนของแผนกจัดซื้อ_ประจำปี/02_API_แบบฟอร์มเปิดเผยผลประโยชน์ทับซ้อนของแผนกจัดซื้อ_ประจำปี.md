# 02_API — F-TMP-006
> base `/api/v1/coi-disclosures` · tenant จาก token (RLS) · ทุก write มี `If-Match: version` (optimistic) + `Idempotency-Key` · **ทุก read ตรวจ canSee (เอกสารลับ)**

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/coi-disclosures?q&status&has_conflict&year&mine_to_act&page&sort` | รายการตามสิทธิ์ (ไม่มี conflict_detail) | FN-11 |
| API-02 | GET `/coi-disclosures/{id}` | รายละเอียด + chain + audit | FN-11 |
| API-03 | POST `/coi-disclosures` `{supersedes_no?}` | สร้างร่าง + ออกเลข + snapshot ปี/ผู้เปิดเผย | FN-01, FN-02, FN-03 |
| API-04 | PUT `/coi-disclosures/{id}` | แก้ไข (เจ้าของ · draft/returned) | FN-01, FN-04 |
| API-05 | GET `/coi-disclosures/{id}/doa-preview` | resolve สายค่าเริ่ม (slot) | FN-05 |
| API-06 | POST `/coi-disclosures/{id}/submit` `{assignees[]}` | ส่ง · snapshot chain + ถ้อยคำ | FN-01, FN-05 (+FN-10) |
| API-07 | POST `/coi-disclosures/{id}/decide` `{decision: approve\|reject, note}` | รับทราบ (ข้อคิดเห็น) / ส่งกลับแก้ไข | FN-06, FN-07 |
| API-08 | POST `/coi-disclosures/{id}/cancel` `{reason}` | ยกเลิก | FN-08 |
| API-09 | GET `/coi-disclosures/{id}/pdf` | PDF FM-PUR-04 (1 หน้า) · ตรวจ canSee | FN-09 |
| API-10 | GET `/coi-disclosures/export.csv` | CSV ตามตัวกรอง — ไม่มี conflict_detail/comment | FN-11 |
| API-11 | POST/DELETE `/coi-disclosures/{id}/attachments` | ไฟล์ (Document Center · สิทธิ์ตามใบ) | — |
| API-12 | GET `/coi-disclosure-config` | current_year · statement_text · closing_text · detail_min — อ่านอย่างเดียว | FN-02 |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ has_conflict: 'none'|'has'|null, conflict_detail, confirmed: bool, supersedes_no, attachment_ids[] }` → 422 ตาม VR (`CHOICE_REQUIRED` · `DETAIL_REQUIRED` · `CONFIRM_REQUIRED`) เฉพาะโหมดส่ง · ชื่อ/ตำแหน่ง/ปี **ไม่รับจาก client** (server snapshot)
- API-04: 409 `NOT_EDITABLE` (ไม่ใช่ draft/returned) · 403 `NOT_OWNER`
- API-06: 422 `CHOICE_REQUIRED` / `DETAIL_REQUIRED` / `CONFIRM_REQUIRED` · 409 `NOT_DRAFT` · 422 `ASSIGNEE_REQUIRED` · 422 `SELF_APPROVAL` (BR-DOA-04) · 200 + `warnings:[DUPLICATE_YEAR]` เมื่อมีใบปีเดียวกัน (ไม่บล็อก)
- API-07: 403 `NOT_CURRENT_APPROVER` · 422 `REASON_REQUIRED` (reject)
- API-08: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/role-compliance) · 409 `NOT_CANCELLABLE` (approved/cancelled)
- API-02/09 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)
- API-10: คอลัมน์ = เลขที่ · ปี · วันที่ยื่น · ผู้เปิดเผย · ตำแหน่ง · ผล · สถานะ · ผู้พิจารณา · แทนฉบับ (ไม่มีรายละเอียด/ข้อคิดเห็น — DEC-16)

## §2.3 Common
Idempotency-Key ทุก POST · optimistic lock `version` → 409 STALE · audit ทุก write (append-only) · multi-tenant RLS + row policy (05 §5.3)

## §2.4 API → Logic Trace
ดูตาราง §2.1 คอลัมน์ Logic (ครบทุก API)

## §2.X Cross-Module Contract
| ปลายทาง | Event/Call | Payload | รอบนี้ |
|---|---|---|---|
| ENG-NOTIFY | coi_conflict_declared · coi_cancelled | {ref: disclosure_id, vars{doc_no, disclosure_year, declarant_name}} — **ไม่มี conflict_detail** | ✓ |
| ENG-DOC-STORE | store(pdf,'COI',id,'approved_final') | | ✓ |
| DOA (F-DLG-001) | resolve(feature_id=F-TMP-006, context{declarant_id}) | | ✓ (relative role line manager · TODO: DOA engine) |
| ทะเบียน COI / Vendor master | `coi.disclosure_acknowledged` {disclosure_id, declarant_id, disclosure_year, has_conflict} | | ประกาศ ไม่ยิง (DEC-02) |
