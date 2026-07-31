# 02_API — F-PURCH-CFG-001 ตั้งค่าการจัดซื้อ (Purchase Configuration)

> **Audience:** BE (HTTP layer) · logic/validation/numbering → 03_LOGIC

---

## PCFG-API-01 — Get config
- **GET** `/api/purchase/config` · **Calls:** getConfig (FN-01), checkAdminAccess (FN-09 read)
- **200:** `{ config:{ enable_comparison, comparison_required, comparison_min_quotes, comparison_threshold_amount, comparison_award_rule, require_pr_before_po, pt_enabled{}, default_payment_type, deposit_default_pct, installment_default_terms, credit_default_days, pr_mandatory{}, quote_attachment_required, require_approved_vendor_only, vendor_pricelist_autofill }, updated_by, updated_at }`

## PCFG-API-02 — Save config  �driven mutation
- **PUT** `/api/purchase/config` · **Body:** config object · **Calls:** validateConfig (FN-03) → saveConfig (FN-02) → writeAudit
- **200:** `{ ok:true, updated_at }` · **400:** `VALIDATION_FAILED` (รายการ field+เหตุ) · **403:** `ACCESS_DENIED`

## PCFG-API-03 — List numbering
- **GET** `/api/purchase/numbering` · **Calls:** listNumbering (FN-04)
- **200:** `{ items:[{ doc_type, label, prefix, digits, reset_cycle, next_no, last_reset_period, preview }] }`

## PCFG-API-04 — Save numbering  �driven mutation
- **PUT** `/api/purchase/numbering/:doc_type` · **Body:** `{ prefix, digits, reset_cycle, next_no }` · **Calls:** validateNumbering (FN-03b) → saveNumbering (FN-05) → writeAudit
- **200:** `{ ok:true, preview }` · **400:** `NUMBERING_INVALID`

## PCFG-API-05 — Preview next number
- **GET** `/api/purchase/numbering/:doc_type/preview` · **Calls:** previewDocNumber (FN-06) → ENG-DOCNUM-01 (no increment)
- **200:** `{ preview:"PR-2569-0232" }`

## PCFG-API-06 — Effective config (สำหรับ consumer PR/PO/CP)
- **GET** `/api/purchase/config/effective` · **Calls:** getConfigForConsumer (FN-07)
- **200:** config keys ที่ PR/PO/Comparison ใช้ gate flow (รวม resolve กับ Budget Config release flag + Payment Term list) · **read-only**

## PCFG-API-07 — Audit log
- **GET** `/api/purchase/config/audit?from=&to=` · **Calls:** listAuditLog (FN-08) — reads T_purchase_config_log
- **200:** `{ items:[{ changed_at, changed_by, field, old_value, new_value }] }`

## PCFG-API-08 — Payment term list (source ของ payment types)
- **GET** `/api/purchase/payment-terms` · **Calls:** resolvePaymentTermList (FN-10) — reads Finance Payment Term master
- **200:** `{ items:[{ code, name, type }] }`

---

## §2.1 Internal (ไม่ใช่ public Purchase Config API)
- **Issue document number** (เพิ่ม next_no จริง) เกิดตอน PR/PO/CP **create** — feature เหล่านั้นเรียก `ENG-DOCNUM-01.issue(doc_type)` ภายใน transaction (atomic increment + reset guard). Purchase Config ให้แค่ตั้งค่า + preview (ไม่ increment)

## §2.2 Cross-cutting
- **Mutations:** API-02, API-04 → validate ก่อน persist → writeAudit (R8) · idempotent reads ที่เหลือ
- **Auth:** ทุก endpoint ผ่าน checkAdminAccess (FN-09); read-only endpoints อนุญาต viewer · mutation เฉพาะ Admin/Manager
- **Effective config real-time:** consumer (PR/PO) อ่าน API-06 สดทุกครั้ง (forward-only — ไม่กระทบเอกสารเดิม)
- **Classification:** Internal ทั้งหมด (ไม่มี Confidential/PII)
