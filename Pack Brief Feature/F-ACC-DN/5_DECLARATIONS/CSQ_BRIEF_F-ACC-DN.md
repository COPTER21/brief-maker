# CSQ_BRIEF — F-ACC-DN Debit Note
## 1. Identity: CSQ-ACC-DN [DEFAULT] · กลุ่ม B · v1.0
## 2. Declared Events
| event_id | trigger | ท่อ | เงื่อนไข | payload |
|---|---|---|---|---|
| ap_dn.approved | pending→approved | **AC** | ทุกใบ | dn_id, dn_no, api_no, vendor_code, reason_code, base_amount, vat_amount, grand_total, dn_date |
| ap_dn.approved | (เดียวกัน) | **EC** kind=actual | api เป็นเส้นค่าใช้จ่าย (no_po) | expense_code, base_amount (ติดลบ) |
## 3. ไม่ประกาศ: OC · DC · SC · FC (เงินสดไม่เปลี่ยน) · SecC
## 4. OQ: CSQ-OQ-DN-1 EC ติดลบ [DEFAULT] — Strike
