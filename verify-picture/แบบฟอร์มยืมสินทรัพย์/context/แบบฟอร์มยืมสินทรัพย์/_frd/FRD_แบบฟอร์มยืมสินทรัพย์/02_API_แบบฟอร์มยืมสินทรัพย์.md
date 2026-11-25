# 02_API — F-TMP-002
> base `/api/v1/asset-borrows` · tenant จาก token (RLS) · ทุก write ต้องมี `If-Match: version` (optimistic) + `Idempotency-Key`

## §2.1 API Overview
| ID | Method · Path | ใช้ทำ | Logic |
|---|---|---|---|
| API-01 | GET `/asset-borrows?q&status&dept&mine_to_act&overdue&page&page_size&sort` | รายการตามสิทธิ์ | FN-10 |
| API-02 | GET `/asset-borrows/{id}` | รายละเอียด + chain + return + audit | FN-10 |
| API-03 | POST `/asset-borrows` | สร้างร่าง + ออกเลข | FN-01, FN-02, FN-03 |
| API-04 | PUT `/asset-borrows/{id}` | แก้ร่าง (เจ้าของ · draft) | FN-01, FN-02 |
| API-05 | GET `/asset-borrows/{id}/doa-preview` | resolve สายค่าเริ่ม (slot) | FN-04 |
| API-06 | POST `/asset-borrows/{id}/submit` `{assignees[]}` | ส่ง · snapshot chain | FN-04 |
| API-07 | POST `/asset-borrows/{id}/decide` `{decision: approve\|reject, qty_lent[], note}` | ตัดสินขั้นปัจจุบัน | FN-05, FN-06 |
| API-08 | POST `/asset-borrows/{id}/cancel` `{reason}` | ยกเลิก | FN-07 |
| API-09 | POST `/asset-borrows/{id}/return` `{received_at}` | บันทึกรับคืน | FN-11 |
| API-10 | GET `/asset-borrows/{id}/pdf` | PDF FM-ASM-04 | FN-08 |
| API-11 | GET `/asset-borrows/export.csv` | CSV ระดับรายการตามตัวกรอง | FN-10 |
| API-12 | POST/DELETE `/asset-borrows/{id}/attachments` | ไฟล์ (Document Center) | — |
| API-13 | GET `/assets?q` (Asset Master · อ่าน) | combobox ทะเบียนสินทรัพย์ | — (feature เจ้าของ) |

## §2.2 Contract สำคัญ
- API-03/04 body: `{ purpose, items:[{asset_code, qty_requested, borrow_date, return_date, remark}], attachment_ids[] }` → 422 ตาม VR-01..04 (`PURPOSE_REQUIRED` · `ITEM_INCOMPLETE` · `RETURN_BEFORE_BORROW` · `DUPLICATE_ASSET`)
- API-06: 409 `NOT_DRAFT` · 422 `ASSIGNEE_REQUIRED` · 422 `SELF_APPROVAL` (BR-DOA-04)
- API-07: 403 `NOT_CURRENT_APPROVER` · 422 `REASON_REQUIRED` (reject) · 422 `QTY_LENT_INVALID` (approve · BR-02)
- API-08: 403 `NOT_OWNER` (ไม่ใช่เจ้าของ/admin) · 409 `NOT_CANCELLABLE` (approved/returned/cancelled)
- API-09: 409 `NOT_APPROVED` · 403 `NOT_RECEIVER` (ไม่ใช่ผู้ให้ยืมในสาย/admin) · 422 `RECEIVED_AT_INVALID` (> วันนี้ หรือ < วันที่ยืมแรก)
- API-02 ของใบที่ไม่มีสิทธิ์ → 404 `NOT_FOUND` (ไม่เปิดเผยว่ามี)

## §2.3 Common
Idempotency-Key ทุก POST · optimistic lock `version` → 409 STALE · audit ทุก write (append-only) · multi-tenant RLS

## §2.4 API → Logic Trace
ดูตาราง §2.1 คอลัมน์ Logic (ครบทุก API)

## §2.X Cross-Module Contract
| ปลายทาง | Event/Call | Payload | รอบนี้ |
|---|---|---|---|
| ENG-NOTIFY | aln_cancelled · aln_returned · aln_overdue | {ref: aln_id, vars} | ✓ |
| ENG-DOC-STORE | store(pdf,'ALN',id,'approved_final') | | ✓ |
| Asset Master | `aln.approved` {aln_id, items[asset_code, qty_lent, return_date], borrower} · `aln.returned` {aln_id, received_at} | | ประกาศ ไม่ยิง (DEC-02) |
