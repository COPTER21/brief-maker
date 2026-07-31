# 02_API — F-PO-001 ใบสั่งซื้อ (Purchase Order)

> **Audience:** Backend developer (HTTP layer)
> **🚨 Iron Rule:** ห้ามมี business logic >5 บรรทัดที่นี่ — ย้ายไป 03_LOGIC §3.1
> **🚨 R8:** ทุก mutation API ระบุ "Calls (Logic)" → trace ใน 03_LOGIC §3.3

---

## §2.1 API Overview
| ID | Method | Path | Summary | Auth |
|---|---|---|---|---|
| F-PO-001-API-01 | GET | /api/v1/purchase-orders | List PO + filter | required |
| F-PO-001-API-02 | GET | /api/v1/purchase-orders/:id | Get detail | required |
| F-PO-001-API-03 | POST | /api/v1/purchase-orders | Create draft | required (buyer) |
| F-PO-001-API-04 | PUT | /api/v1/purchase-orders/:id | Update draft | required (buyer, draft only) |
| F-PO-001-API-05 | POST | /api/v1/purchase-orders/:id/submit | Submit → pending + resolve DoA | required (buyer) |
| F-PO-001-API-06 | POST | /api/v1/purchase-orders/:id/approve | Approve | required (approver, DoA tier) |
| F-PO-001-API-07 | POST | /api/v1/purchase-orders/:id/reject | Reject (+reason) | required (approver) |
| F-PO-001-API-08 | POST | /api/v1/purchase-orders/:id/return | Return to draft (+reason) | required (approver) |
| F-PO-001-API-09 | POST | /api/v1/purchase-orders/:id/cancel | Cancel (+reason) | required (buyer draft / approver if approved) |
| F-PO-001-API-10 | GET | /api/v1/purchase-orders/:id/pdf | Render PO PDF | required |
| F-PO-001-API-11 | GET | /api/v1/comparisons/:cp_no/awarded-vendors | Awarded vendors (CP source) | required |
| F-PO-001-API-12 | GET | /api/v1/vendors?active=1&q= | Vendor lookup (combobox) | required |
| F-PO-001-API-13 | POST | /api/v1/purchase-orders/:id/attachments | Upload attachment | required (buyer) |

> API-11/-12 อ่านจาก CP/Vendor master (dependency) — PO consume เท่านั้น

---

## §2.2 Per-API Contract (mutation หลัก)

### F-PO-001-API-03: POST /purchase-orders (Create draft)
| Field | Value |
|---|---|
| auth | required · roles: buyer, senior_buyer, purch_manager |
| Calls (Logic) | FN-01 createPurchaseOrder → FN-03 buildLinesFromSource (ถ้า source) → FN-05 validatePurchaseOrder → ENG po-amount-engine |
**Request body:** `{ source_type, source_pr_no?, source_cp_no?, vendor_id, buyer, po_date, expected_date, payment_term, lines[], endbill_discount_*, wht_*, notes }`
**Response 201:** `{ id, status_doc:"draft", grand_total, ... }`
**Errors:** VENDOR_REQUIRED, INVALID_SOURCE_MODE, LINE_REQUIRED

### F-PO-001-API-04: PUT /purchase-orders/:id (Update draft)
| Calls (Logic) | FN-02 updatePurchaseOrder → FN-05 validate → ENG po-amount-engine |
- เงื่อนไข: status_doc = draft เท่านั้น (else 409 NOT_EDITABLE)

### F-PO-001-API-05: POST /:id/submit
| Calls (Logic) | FN-05 validatePurchaseOrder → FN-06 applyStatusTransition(draft→pending) → ENG doa-resolver-engine |
- resolve DoA tier จาก {feature_id:F-PO-001, cost_center:dept, amount:grand_total}
- block ถ้า amount เกิน tier สูงสุด (VR06) / เงื่อนไขไม่ครบ
**Response 200:** `{ status_doc:"pending", approver_role, doa_tier }`

### F-PO-001-API-06: POST /:id/approve
| Calls (Logic) | FN-06 applyStatusTransition(pending→approved) → FN-07 generatePoNumber |
- ตรวจ SoD: approver ≠ created_by (else 403 SOD_VIOLATION)
- ตรวจ tier: approver role ครอบคลุม amount (else 403 DOA_INSUFFICIENT)
- ออก po_no (running) + lock เอกสาร
**Response 200:** `{ status_doc:"approved", po_no }`

### F-PO-001-API-07 / -08: reject / return
| Calls (Logic) | FN-06 applyStatusTransition(pending→rejected|return) |
- body: `{ reason }` (required — VR07); return → revision_no +1, กลับ draft

### F-PO-001-API-09: POST /:id/cancel
| Calls (Logic) | FN-06 applyStatusTransition(*→cancelled) |
- draft → buyer cancel (+reason); approved → ต้อง approver + block ถ้ามี GRN/AP (E09)

### F-PO-001-API-10: GET /:id/pdf
| Calls (Logic) | FN-08 buildPoPdfModel → ENG baht-text-engine |
- เลือก template ตามรูปแบบภาษี (VAT/NoVAT/Discount/WHT) จากข้อมูล PO
**Response 200:** `application/pdf`

### F-PO-001-API-01: GET /purchase-orders (List)
| Calls (Logic) | FN-09 buildPoListQuery |
- query: `status_doc, status_delivery, status_payment, vendor_id, date_from, date_to, q, limit, offset`

> รายละเอียด request/response เต็มของทุก endpoint → ดู INDEX.md cross-ref + 04_DB field dictionary
