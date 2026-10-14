# 02_API — F-AGM-013 Cane Payment

> REST base `/agm/cane/payments` · headers: X-Idempotency-Key, If-Match(ETag), X-Trace-Id · R8: mutation → Function

## §2.1 Endpoints (base — API/DB §8)
| API | Method | Path | Purpose |
|---|---|---|---|
| API-01 | GET | /agm/cane/payments?search=&season_id=&product_id=&checkin_type=&unload_date_from/to=&quick_filters[]= | List (filter/tab/paginate/sort) |
| API-02 | GET | /agm/cane/payments/{id} | Detail (drawer) — คืน ETag header |
| API-03 | POST | /agm/cane/payments/{id}/sync-ccs | Sync CCS เดี่ยว (X-Idempotency-Key optional) |
| API-04 | POST | /agm/cane/payments/sync-all-ccs | Sync CCS bulk → SyncAllResult (X-Idempotency-Key required) |
| API-05 | GET | /agm/cane/payments/export?…&tab= | Export CSV (sync) |
| API-06 | POST | /agm/cane/payments/{id}/installments/{n}/pay | ทำจ่ายงวด n (If-Match required · body {method}) |
| API-07 | POST | /api/storage/upload | อัปโหลดไฟล์ (multipart) → {url} |
| API-08 | POST | /agm/cane/payments/{id}/installments/{n}/cash-proof | แนบหลักฐาน (If-Match · body {url}) — optional |
| API-09 | GET | /agm/cane/payments/{id}/installments/{n}/cash-proof | ดู metadata หลักฐาน |
| API-10 | GET | /api/cane/ccs?scale_ticket_no=&unload_date=&product_id= | Legacy CCS lookup (service, internal) |

## §2.2 Endpoints (v3.1/v4.1 added ⭐)
| API | Method | Path | Purpose |
|---|---|---|---|
| **API-11** | POST | /agm/cane/payments/{id}/preview | คำนวณ step 7 ขั้น ต่องวด (non-persistent) — ประเภทอ้อย/VAT/charge/หนี้/ดอกเบี้ย/ค่าธนาคาร |
| **API-12** | POST | /agm/cane/payments/{id}/confirm ⭐ | All-in-One confirm — รับงวด1+งวด2+โปรครั้งเดียว (If-Match · X-Idempotency-Key) → status transition + auto งวด |
| **API-13** | POST | /agm/cane/payments/{id}/print-bill?type=INST1\|INST2\|PROMOTION | พิมพ์บิล (แยกใบ) |
| **API-14** | POST | /agm/cane/payments/{id}/final-receipt | ใบเสร็จการจ่ายเงินอ้อยรวม (status=completed เท่านั้น) |
| **API-EXT** | GET | /payment-settings/active?season=&product= ⭐ | อ่าน active setting จาก **F-AGM-012** (K/base/interest/bankFee/charges/green-white/VAT/cane type master/factory province) |

## §2.3 Contracts ⭐
- **API-06/12 (pay/confirm):** If-Match(ETag/row_version) optimistic · X-Idempotency-Key · body { method: "bank_transfer"|"cash"|"cheque", cheque_number?, note? } · คืน updated payment + receipt meta + debt_call_status · **transition ทันทีทุกวิธี** (ไม่มี waiting_cash_proof). Quota + โอน → ต้องมี bank_account มิฉะนั้น 422 BANK_ACCOUNT_MISSING.
- **API-11 (preview):** body { ccs, net_tons, cane_type_code, inst bill types, debt%, bank_branch_province_code, method } → per-งวด breakdown (normal/actual date, days_early, interest, bank_fee_type, amount_final). ไม่เก็บ.
- **API-EXT (read active setting):** คืนเฉพาะ status=Active — ค่าเดียวกับที่ Payment ใช้คำนวณ (invariants OQ-03). Snapshot ประเภทอ้อย+จังหวัดสาขา ณ confirm (BR-17).
- **API-03/04 (sync):** waiting_ccs → set ccs_value + status pending. bulk คืน {total, success, failed, details[]} — partial failure ไม่แตะแถวเดิม.
- **All mutations:** audit log (before/after) + optimistic lock + emit events.

## §2.4 Events
`cane.payment.ccs.synced` · `cane.payment.ccs.sync_all.completed` · `cane.payment.installment.paid` · `cane.payment.cash_proof.uploaded` · `cane.payment.completed`

## §2.5 Error Catalog (API/DB §9 → 05_RULES §5.6)
| Code | HTTP | ข้อความ |
|---|---|---|
| VALIDATION_FAILED | 400 | พารามิเตอร์ตัวกรองไม่ถูกต้อง / ไม่มีรายการที่สถานะ waiting_ccs |
| UNAUTHORIZED / INSUFFICIENT_ROLE | 401/403 | คุณไม่มีสิทธิ์ดำเนินการนี้ |
| NOT_FOUND / CCS_NOT_FOUND | 404 | ไม่พบรายการการจ่ายนี้ / ไม่พบข้อมูลตัวอย่าง CCS |
| CCS_ALREADY_SYNCED | 409 | รายการนี้ได้ทำการดึงค่า CCS แล้ว |
| CONFLICT_UPDATE_STALE | 409/412 | ข้อมูลล้าสมัย กรุณารีเฟรชแล้วลองใหม่ |
| PAYMENT_NOT_DUE | 422 | ยังไม่ถึงวันที่กำหนดชำระ |
| BANK_ACCOUNT_MISSING | 422 | บัญชีธนาคารสำหรับรายการนี้ยังไม่ระบุ |
| UNSUPPORTED_FILE_TYPE / FILE_TOO_LARGE | 422 | ไฟล์ต้องเป็น jpg/png/pdf ขนาดไม่เกิน 5MB |
| DEBT_API_ERROR | 424 | หักหนี้ล้มเหลว (เก็บใบเสร็จ + banner + retry queue — ไม่ถอนใบเสร็จ) |
| STORAGE_UPLOAD_FAILED / RECEIPT_ISSUE_FAILED | 5xx | server error |

## §2.6 Headers & Concurrency (API/DB §9.1–9.4)
- Auth: Bearer JWT + RBAC per role (5 roles)
- X-Idempotency-Key: sync-all, pay, confirm, upload (dedupe by key+actor)
- If-Match ETag/row_version: pay, confirm, cash-proof → mismatch 412 (client refresh); domain conflict 409
- Rate limit list 120 rpm · 429 + Retry-After · P95 list ≤300ms / write ≤500ms / bulk ≤500/job
- PII: account_number masked ****1234 default; unmask = Finance Officer / System Admin (RBAC)
