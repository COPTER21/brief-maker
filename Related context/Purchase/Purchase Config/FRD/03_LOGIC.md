# 03_LOGIC — F-PURCH-CFG-001 ตั้งค่าการจัดซื้อ (Purchase Configuration)

> **Audience:** BE · **Scope:** config CRUD + validate + numbering engine + payment-term resolve + audit + access gate
> **หลักการ:** config-driven (PR/PO/CP อ่าน effective config) · numbering = engine reusable · ห้าม hardcode rule

---

## §3.1 Functions (prefix PCFG-FN)

### PCFG-FN-01: getConfig
- อ่าน T_purchase_config (1 แถว/tenant) + resolve payment term list (FN-10) · **Input:** {tenant,user} · **Output:** ConfigDTO · **Calls:** FN-09, FN-10 · read

### PCFG-FN-02: saveConfig  ✍️ mutation
- validate (FN-03) → upsert T_purchase_config → writeAudit (diff old→new ลง T_purchase_config_log) · **Invoked:** API-02 · **Side effects:** write config + audit

### PCFG-FN-03: validateConfig
- VAL-01 (enable_comparison=off → comparison_required=off) · VAL-02 (default_payment_type ∈ pt_enabled) · VAL-05 (≥1 payment type) · field ranges · **Output:** {ok, errors[]}
- **FN-03b validateNumbering:** prefix ไม่ว่าง · digits≥1 · next_no≥1 (เตือนถ้า ≤ ที่ออกแล้ว)

### PCFG-FN-04: listNumbering
- อ่าน T_doc_numbering ทุก doc_type + คำนวณ preview (FN-06) · **Invoked:** API-03

### PCFG-FN-05: saveNumbering  ✍️ mutation
- validateNumbering → upsert T_doc_numbering (ต่อ doc_type) → writeAudit · **Invoked:** API-04

### PCFG-FN-06: previewDocNumber
- เรียก ENG-DOCNUM-01 แบบ **no-increment** (peek) → string · **Invoked:** API-05, FN-04

### PCFG-FN-07: getConfigForConsumer
- รวม effective config keys + resolve release_require_unlock_ref (จาก Budget Config) + payment term list → DTO ให้ PR/PO/CP · **Invoked:** API-06 · read-only

### PCFG-FN-08: listAuditLog
- อ่าน T_purchase_config_log (filter ช่วงเวลา) · **Invoked:** API-07

### PCFG-FN-09: checkAdminAccess
- role gate (User Access ENC): edit เฉพาะ Purchasing Admin/Manager · viewer = read · อื่น 403 · **Invoked:** ทุก API

### PCFG-FN-10: resolvePaymentTermList
- อ่าน Finance Payment Term master → รายการ payment types ที่เลือกเปิดใช้ได้ · **Invoked:** API-08, FN-01, FN-07 · read external

---

## §3.2 Engines

### ENG-DOCNUM-01 — doc-number-generator  🆕 NEW (reusable)
- **Type:** CUBIC reusable engine (owned by Purchase Config; reusable โดยทุกโมดูลที่ออกเลขเอกสาร)
- **issue(doc_type) ✍️:** atomic — อ่าน T_doc_numbering FOR UPDATE → ตรวจ reset (เทียบ period ปัจจุบันกับ last_reset_period: yearly=YYYY, monthly=YYYY-MM, none=ไม่รีเซ็ต) → ถ้าขึ้นรอบใหม่ next_no=1 + อัปเดต last_reset_period → format `{prefix}-{พ.ศ.}-{next_no:0{digits}}` → increment next_no → return เลข
- **peek(doc_type):** เหมือน issue แต่ **ไม่ increment** (สำหรับ preview)
- **Guards:** atomic increment (กันเลขซ้ำ concurrent) · last_reset_period กันรีเซ็ตซ้ำ
- **เรียกโดย:** PR/PO/CP ตอน create (issue) · Purchase Config (peek)

### ENG-DOCNUM ↔ External references (read-only, ไม่ใช่ engine ของ feature)
- Payment Term master (Finance) — FN-10 · Budget Config release flag — FN-07 · DOA approval tiers — consumer ของ effective config · Vendor Price List — vendor_pricelist_autofill ใช้ที่ PR/PO

---

## §3.3 Trace (API → Function → Engine)
| API | Function(s) | Engine | Mutation? |
|---|---|---|:--:|
| API-01 | FN-01, FN-09, FN-10 | — | ✗ read |
| API-02 | FN-03, FN-02, FN-09 | — | ✍️ config + audit |
| API-03 | FN-04, FN-06 | DOCNUM-01 (peek) | ✗ |
| API-04 | FN-03b, FN-05, FN-09 | — | ✍️ numbering + audit |
| API-05 | FN-06 | DOCNUM-01 (peek) | ✗ |
| API-06 | FN-07, FN-10 | — | ✗ read |
| API-07 | FN-08 | — | ✗ |
| API-08 | FN-10 | — | ✗ |
| (internal) PR/PO/CP create | — | **DOCNUM-01 (issue)** | ✍️ next_no |

> **R8:** mutation API (02/04) → validate → persist → audit log เสมอ · doc-number issue (increment) atomic ใน DOCNUM-01 · no orphan function · ✓
