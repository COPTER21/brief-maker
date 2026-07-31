# BRD: ตั้งค่าการจัดซื้อ (Purchase Configuration)

| Field | Value |
|---|---|
| BRD ID | BRD-PURCH-CFG-001 |
| Feature Name | ตั้งค่าการจัดซื้อ (Purchase Configuration) |
| Feature ID | F-PURCH-CFG-001 |
| BRD Type | New Feature (รวมส่วน Payment Term config ที่เคยร่างไว้ใน cheat sheet) |
| Version | 1.0 |
| Status | AI Reviewed |
| Module | จัดซื้อ (Purchase / P2P) — Configuration Layer |
| Owner | ทีม BA — 2BSimple |
| Stakeholders | ฝ่ายจัดซื้อ (Purchasing Admin/Manager), Finance, Dev Lead (Bird), QA Lead |
| Created Date | 2026-06-05 |
| Last Updated | 2026-06-05 |
| Source | HTML prototype `purchase-config.html` (final-check PASS) + P2P Payment Cheat Sheet v1.0 (D01–D15) + boundary decisions ที่ stakeholder ยืนยัน |

## Changelog
- v1.0 (2026-06-05): สร้าง BRD ผ่าน brd-generator-full (Fresh Mode · New Feature) — derive จาก prototype + cheat sheet + boundary decisions. ครอบ 6 กลุ่ม config (Comparison · Flow · Payment Types · PR doc · Vendor · Numbering) + boundary references + locked rules

---

## Section 2: Business Context

### 2.1 ปัญหา / โอกาส
กระบวนการจัดซื้อ (P2P) มีหลายขั้น (PR → เปรียบเทียบราคา → PO → GRN → AP → PV) และแต่ละองค์กร/แผนกต้องการกติกาต่างกัน — บางที่บังคับเปรียบเทียบราคา 3 เจ้า บางที่ซื้อด่วนข้ามได้, บางที่ต้องผูกใบปลดอายัดงบ บางที่ไม่ผูก. ถ้า hardcode กติกาเหล่านี้ในโค้ด PR/PO จะแก้ยาก + rework ทุกครั้งที่ policy เปลี่ยน. ต้องมี **ชั้น configuration กลาง** ที่ PR/Comparison/PO อ่านไป gate flow — เปิด/ปิด/บังคับแต่ละขั้นได้โดยไม่แก้โค้ด (CUBE = config-driven, ห้าม hardcode rule)

### 2.2 เป้าหมายทาง Business
- ให้ฝ่ายจัดซื้อ **ตั้งกติกา P2P เองได้** (config-driven) — เปิด/ปิด/บังคับ การเปรียบเทียบราคา, เส้นทางเอกสาร, ประเภทการชำระ, ฟิลด์บังคับ, การเลือกผู้ขาย, รูปแบบเลขที่เอกสาร
- เป็น **single source of P2P rules** ที่ PR/Comparison/PO อ่านไปใช้ → ลด rework + ความไม่สอดคล้อง
- ระบุ **ขอบเขตชัด**: อะไรอยู่ที่นี่ vs อะไรอยู่ Budget/DOA/Finance/Inventory — กัน config ซ้ำ/ขัดกัน

### 2.3 Success Metrics
| Metric | Baseline | Target | วัดยังไง |
|---|---|---|---|
| เปลี่ยน policy จัดซื้อโดยไม่แก้โค้ด | แก้โค้ด/deploy | 100% ผ่าน config | จำนวน policy change ที่ทำผ่าน UI |
| PR/PO ปฏิบัติตามกติกาที่ตั้ง | ไม่บังคับใช้สม่ำเสมอ | 100% | PR/PO ที่ผ่าน validation ตาม config |
| เวลา onboard กติกาบริษัทใหม่ | วัน (dev) | < 30 นาที (config) | เวลาตั้งค่าครบ 1 ชุด |
| ความสอดคล้องเลขที่เอกสาร | manual/ชน | 0 เลขซ้ำ | running number engine |

### 2.4 ตำแหน่งใน Value Stream
`Config Layer (★ Purchase Config + Budget Config + DOA + Finance + Inventory Config) → PR → เปรียบเทียบราคา → PO → GRN → AP → PV`

---

## Section 3: Scope

### 3.1 In-Scope (6 กลุ่ม config + boundary view)
| # | กลุ่ม | Config keys |
|---|---|---|
| S1 | เปรียบเทียบราคา (Comparison) | enable_comparison · comparison_required · comparison_min_quotes · comparison_threshold_amount · comparison_award_rule (lowest/manual) |
| S2 | เส้นทางเอกสาร (Flow gating) | require_pr_before_po |
| S3 | ประเภทการชำระเงิน (Payment Types) | pt_enabled[6] · default_payment_type · deposit_default_pct · installment_default_terms · credit_default_days *(ดึงรายการจาก Payment Term · inherit→PO)* |
| S4 | เอกสาร PR | pr_mandatory(item/qty/need_by) · quote_attachment_required |
| S5 | การเลือกผู้ขาย (Vendor sourcing) | require_approved_vendor_only · vendor_pricelist_autofill (จาก Vendor Price List) |
| S6 | เลขที่เอกสาร (Numbering) | ต่อชนิด (PR/CP/PO): prefix · digits · reset(none/yearly/monthly) · next |
| S7 | มุมมองอ้างอิง (read-only) | แสดงว่ากติกาที่เกี่ยวข้องอยู่โมดูลไหน + กติกาที่ระบบล็อก |

### 3.2 Out-of-Scope (อยู่ feature อื่น — Purchase Config แค่อ่าน/อ้างอิง)
| รายการ | เจ้าของ |
|---|---|
| Payment Term master (เงื่อนไขชำระจริง) | Finance |
| ปลดอายัดงบ / บังคับอ้างใบปลดอายัด (release_require_unlock_ref) | Budget Config (#4) |
| ผู้มีอำนาจอนุมัติตามวงเงิน (สายอนุมัติ) | DOA (Policy Center) |
| รับของ / QC inline / Putaway / over-receipt tolerance | Inventory Config |
| Direct Payment (จ่ายตรง — เปิดที่ AP Invoice) | Finance / Accounting Config |
| Vendor master / Vendor Price List (ข้อมูล) | Master Data |

### 3.3 ขอบเขตข้อมูล
THB เท่านั้น (single currency) · config ระดับ tenant/บริษัท · มีผลกับเอกสารที่สร้าง**ใหม่**หลังบันทึก (ไม่ย้อนหลังเอกสารเดิม)

---

## Section 4: User Roles & Permissions

| Role | สิทธิ์ | หมายเหตุ |
|---|---|---|
| ผู้ดูแลการจัดซื้อ (Purchasing Admin) | ดู + แก้ + บันทึก config | ทุกการบันทึกบันทึก audit (ใคร/เมื่อ/ค่าเดิม→ค่าใหม่) |
| หัวหน้าฝ่ายจัดซื้อ (Manager) | ดู + แก้ + บันทึก (อาจต้องอนุมัติผ่าน DOA — ดู Q) | |
| ผู้ใช้จัดซื้อทั่วไป | อ่านอย่างเดียว (เห็นกติกาที่ใช้) | |
| โมดูลอื่น (PR/PO/Comparison engine) | อ่าน config keys ผ่าน API | system read |

---

## Section 5: User Journey (with COSO)

> Purchase Config = การ **ตั้งค่า Preventive Control** (กำหนดกติกาที่ระบบจะบังคับตอนทำรายการ PR/PO)

### J1 — ตั้งกติกาจัดซื้อ (Maker)
1. Purchasing Admin เปิด "ตั้งค่าการจัดซื้อ" → แท็บ ตั้งค่าทั่วไป
2. ปรับ toggle/ค่า (เปรียบเทียบราคา, flow, payment types, PR doc, vendor) → **Flow Preview อัปเดตสด**ให้เห็นผล
3. กด บันทึก → *Preventive control:* ค่าใหม่มีผลกับ PR/PO ที่สร้างหลังจากนี้ + บันทึก audit
4. *Checker/Approver (optional):* การเปลี่ยน config สำคัญอาจเข้าสายอนุมัติผ่าน DOA (ดู Section 15 Q)

### J2 — ตั้งเลขที่เอกสาร (Maker)
1. แท็บ เลขที่เอกสาร → ตั้ง prefix/หลัก/รอบรีเซ็ต/เลขถัดไป ต่อชนิด (PR/CP/PO)
2. ดู **ตัวอย่างเลขสด** (เช่น PR-2569-0232) → บันทึก

### J3 — ใช้งานจริงโดย PR/PO (Detective ผ่านการบังคับ)
1. ผู้ใช้สร้าง PR → ระบบอ่าน config: ฟิลด์บังคับ, ต้องผูกใบปลดอายัดมั้ย (จาก Budget Config), ต้องเปรียบเทียบราคามั้ย
2. ระบบ gate flow ตาม config — ข้าม/บังคับขั้นตาม toggle

---

## Section 6: Data Entity & Fields

### 6.1 ตารางใหม่
**`T_purchase_config`** (1 แถวต่อ tenant — structured config)
| Field (field_key) | Type | Null | Classification | Description |
|---|---|---|---|---|
| config_id | uuid (PK) | NO | Internal | PK |
| tenant_id | uuid | NO | Internal | unique per tenant |
| enable_comparison | boolean | NO | Internal | เปิดเปรียบเทียบราคา |
| comparison_required | boolean | NO | Internal | บังคับเปรียบเทียบ |
| comparison_min_quotes | int | NO | Internal | ผู้เสนอราคาขั้นต่ำ |
| comparison_threshold_amount | numeric(18,2) | NO | Internal | บังคับเมื่อยอด ≥ |
| comparison_award_rule | varchar(10) | NO | Internal | lowest / manual |
| require_pr_before_po | boolean | NO | Internal | PO ต้องมี PR ก่อน |
| pt_enabled | jsonb | NO | Internal | ประเภทชำระที่เปิดใช้ {postpay,prepay,deposit,installment,partial,credit} |
| default_payment_type | varchar(12) | NO | Internal | ค่าเริ่มต้น inherit→PO |
| deposit_default_pct | numeric(5,2) | YES | Internal | % มัดจำเริ่มต้น (D08) |
| installment_default_terms | int | YES | Internal | จำนวนงวดเริ่มต้น (D09) |
| credit_default_days | int | YES | Internal | วันเครดิตเริ่มต้น |
| pr_mandatory | jsonb | NO | Internal | {item,qty,need_by} |
| quote_attachment_required | boolean | NO | Internal | บังคับแนบใบเสนอราคา |
| require_approved_vendor_only | boolean | NO | Internal | เฉพาะ vendor approved |
| vendor_pricelist_autofill | boolean | NO | Internal | autofill ราคาจาก Vendor Price List |
| updated_by | uuid | NO | Internal | ผู้แก้ล่าสุด |
| updated_at | timestamptz | NO | Internal | เวลาแก้ล่าสุด |

**`T_doc_numbering`** (ต่อ tenant × ชนิดเอกสาร)
| Field | Type | Null | Class | Description |
|---|---|---|---|---|
| numbering_id | uuid (PK) | NO | Internal | PK |
| tenant_id | uuid | NO | Internal | |
| doc_type | varchar(8) | NO | Internal | PR / CP / PO |
| prefix | varchar(10) | NO | Internal | คำนำหน้า |
| digits | int | NO | Internal | จำนวนหลักเลขรัน |
| reset_cycle | varchar(8) | NO | Internal | none / yearly / monthly |
| next_no | int | NO | Internal | เลขรันถัดไป |
| last_reset_period | varchar(7) | YES | Internal | YYYY หรือ YYYY-MM (กันรีเซ็ตซ้ำ) |

**`T_purchase_config_log`** (audit — append-only) : config_id, changed_at, changed_by, field, old_value, new_value

### 6.2 อ่านจาก (read-only references)
| ค่า | จาก |
|---|---|
| รายการ Payment Term (ที่มาของ payment types) | Finance — Payment Term master |
| release_require_unlock_ref (บังคับใบปลดอายัด) | Budget Config (#4) |
| approval tiers (amount→ผู้อนุมัติ) | DOA |
| Vendor Price List (ราคา autofill) | Master |

---

## Section 7: User Stories & Acceptance Criteria

| US | User Story | Acceptance Criteria |
|---|---|---|
| US-01 | ตั้งว่าระบบมี/บังคับเปรียบเทียบราคามั้ย | toggle enable/required + min-quotes + threshold + award rule บันทึกได้ · Flow Preview สะท้อนผล |
| US-02 | ตั้งว่า PO ต้องมี PR ก่อนมั้ย | require_pr_before_po off → เปิด PO ลอยได้ |
| US-03 | เลือกประเภทการชำระที่เปิดใช้ (จาก Payment Term) | checklist 6 ประเภท + default + %มัดจำ/งวด/วันเครดิต · inherit→PO |
| US-04 | ตั้งฟิลด์บังคับของ PR | item/qty/need_by/quote attachment toggle ได้ · ไม่มี cost center/รหัสงบ (มากับใบปลดอายัด) |
| US-05 | ตั้งกติกาเลือกผู้ขาย | approved-only + pricelist autofill |
| US-06 | ตั้งรูปแบบเลขที่เอกสาร PR/CP/PO | prefix/digits/reset/next + ตัวอย่างสด · เลขไม่ซ้ำ |
| US-07 | เห็นว่ากติกาอื่นอยู่โมดูลไหน + อะไรล็อก | การ์ดอ้างอิง + การ์ด locked rules แสดงชัด |
| US-08 | ทุกการเปลี่ยน config ตรวจสอบย้อนได้ | audit log (ใคร/เมื่อ/old→new) |

---

## Section 8: Status & Lifecycle
- Config มีสถานะเดียว = **active** (บันทึกแล้วมีผลทันทีกับเอกสารใหม่) · มี draft ชั่วคราว (dirty) ก่อนกดบันทึก
- `T_doc_numbering.next_no` เพิ่มขึ้นเมื่อออกเอกสาร · รีเซ็ตเมื่อขึ้นรอบใหม่ (yearly/monthly) ตาม reset_cycle
- ค่า config มีผล **forward-only** (เอกสารเดิมไม่เปลี่ยน)

---

## Section 9: Business Rules + Validation

| BR | Rule | Tag |
|---|---|---|
| BR-01 | กติกาทั้งหมดต้องอ่านจาก config (ห้าม hardcode ใน PR/PO) | FIXED |
| BR-02 | ปิด enable_comparison → comparison_required/min/threshold/award disabled | CONFIGURABLE |
| BR-03 | default_payment_type ต้องเป็นประเภทที่ pt_enabled=true | FIXED |
| BR-04 | รายการ payment types ดึงจาก Payment Term (Finance) — ที่นี่เลือกเปิดใช้ + ค่าเริ่มต้น | FIXED |
| BR-05 | cost center/รหัสงบ ไม่ตั้งที่นี่ — มากับใบปลดอายัด (UNLK); บังคับใบปลดอายัดตั้งที่ Budget Config | FIXED |
| BR-06 | approval ส่ง amount ให้ DOA — ไม่ตั้ง tier ที่นี่ | FIXED |
| BR-07 | เลขที่เอกสารต้องไม่ซ้ำ · รีเซ็ตตาม reset_cycle (กันรีเซ็ตซ้ำด้วย last_reset_period) | FIXED |
| BR-08 | config มีผล forward-only (ไม่ย้อนเอกสารเดิม) | FIXED |
| BR-09 | ทุกการเปลี่ยน config เขียน audit log | FIXED |
| BR-10 | comparison_min_quotes / threshold / %มัดจำ / งวด / วันเครดิต ปรับได้ | CONFIGURABLE |

### Validation
| VAL | เงื่อนไข | ผล |
|---|---|---|
| VAL-01 | enable_comparison=off แต่ comparison_required=on | บังคับ required=off (disable) |
| VAL-02 | default_payment_type ไม่อยู่ใน pt_enabled | reset default เป็นตัวแรกที่เปิด หรือ block save |
| VAL-03 | prefix ว่าง / digits=0 | block + แจ้ง |
| VAL-04 | next_no ≤ เลขที่ออกไปแล้ว | เตือนเสี่ยงเลขซ้ำ |
| VAL-05 | ปิดทุก payment type | block (ต้องเปิดอย่างน้อย 1) |

### 9.5 Flexibility
toggle/number ทั้งหมด = **Config (Admin Panel)** · locked rules (D-series) = ไม่อยู่ใน config

---

## Section 10: Edge Cases

| EC | สถานการณ์ | คาดหวัง |
|---|---|---|
| EC-01 | เปลี่ยน config ระหว่างมี PR draft ค้าง | PR ที่ยังไม่ submit ใช้ config ใหม่ตอน validate · ที่ submit แล้วคงเดิม |
| EC-02 | ปิด enable_comparison ขณะมี CP ค้าง | CP เดิมเดินต่อได้ · PR ใหม่ข้าม CP |
| EC-03 | ขึ้นปีงบใหม่ + reset_cycle=yearly | next_no รีเซ็ตเป็น 1 ครั้งเดียว (last_reset_period กันซ้ำ) |
| EC-04 | ลดจำนวน payment type ที่ default ใช้อยู่ | VAL-02 — เปลี่ยน default |
| EC-05 | 2 admin แก้ config พร้อมกัน | optimistic lock — เตือน reload |
| EC-06 | require_approved_vendor_only=on แต่เลือก vendor ที่ไม่ approved ใน PR | PR block ที่ฝั่ง PR (อ่าน config นี้) |

---

## Section 11: Impact Analysis
| พื้นที่ | ผลกระทบ |
|---|---|
| PR / Comparison / PO | ต้องอ่าน config keys เหล่านี้ตอน validate/gate flow (consumer) |
| Numbering engine | ทุกเอกสาร PR/CP/PO ดึงเลขจาก T_doc_numbering |
| Budget Config (#4) | Purchase Config อ้างถึง release_require_unlock_ref — ไม่แก้ |
| Finance (Payment Term) | Purchase Config อ่านรายการ payment term — ไม่แก้ |
| Regression | เปลี่ยน config ต้องไม่กระทบเอกสารเดิม (forward-only) |

---

## Section 12: Dependencies
### Upstream (ต้องมีก่อน/พร้อมใช้)
- Finance — Payment Term master (รายการประเภทชำระ) ✓ done
- Budget Config (#4) — release_require_unlock_ref
- DOA (Policy Center) — approval tiers ✓ Test
- Vendor Master + Vendor Price List ✓ done
### Downstream (consumer)
- PR (F-PR-001) · Comparison (F-CMP-001) · PO (F-PO-001) — อ่าน config ไป gate flow
### Existing System
- มี/อ้างอิง: Payment Term, Budget Config, DOA, Vendor Price List · สร้างใหม่: T_purchase_config + T_doc_numbering + log + UI

---

## Section 13: Delivery Phases
| Phase | ขอบเขต | Output |
|---|---|---|
| P1 — Core config | Comparison · Flow · PR doc · Vendor + อ่าน Payment Term | config UI ตั้งทั่วไป + API read |
| P2 — Payment Types + Numbering | payment types (inherit) + numbering engine (PR/CP/PO) | inherit→PO + running number |
| P3 — Audit + Boundary view | config_log + การ์ดอ้างอิง/locked + (optional) DOA approval ของ config change | audit + governance |

---

## Section 14: Dev Requirements Summary "ใบสั่ง"
1. **config-driven ทั้งหมด** — PR/PO/Comparison อ่าน key จาก T_purchase_config; **ห้าม hardcode** กติกา
2. payment types = checklist เลือกเปิดใช้จาก **Payment Term (Finance)**; default + %มัดจำ/งวด/วันเครดิต **inherit ไป PO** (ปรับราย PO ได้ ตาม D08/D09)
3. **ไม่มี cost center/รหัสงบ ใน PR mandatory** — มากับใบปลดอายัด (UNLK); บังคับใบปลดอายัดอ่านจาก **Budget Config**
4. approval = ส่ง amount ให้ **DOA** (ไม่ตั้ง tier ที่นี่)
5. **Direct Payment ไม่อยู่ที่นี่** — เปิดที่ AP Invoice (Finance/Accounting)
6. Numbering engine: prefix/digits/reset(none/yearly/monthly)/next + กันเลขซ้ำ + รีเซ็ตครั้งเดียวต่อรอบ (last_reset_period)
7. config มีผล **forward-only** + **audit log** ทุกการเปลี่ยน
8. locked rules (D01–D15) = **ไม่ทำเป็น toggle** (แสดง read-only เท่านั้น)
9. Flow Preview สะท้อน toggle แบบสด (UX)

---

## Section 15: Open Questions
| Q | คำถาม | กระทบ |
|---|---|---|
| Q1 | การเปลี่ยน config สำคัญ (เช่น ปิดบังคับเปรียบเทียบ) ต้องผ่าน **DOA approval** มั้ย หรือ admin บันทึกได้เลย? | Section 4/5 |
| Q2 | **Default delivery/warehouse location** บน PO ควรอยู่ Purchase Config หรือ Inventory/PO? | scope |
| Q3 | **Tax/VAT default** บน PO อยู่ Finance หรือ Purchase Config? | scope (เอนเอียง Finance) |
| Q4 | รองรับหลายสกุลเงินในอนาคตมั้ย (ตอนนี้ THB only)? | Section 3.3 |
| Q5 | **Auto-PO จาก reorder point** (MRP) — future scope? | future |
| Q6 | Numbering แยกตามแผนก/สาขา หรือรวมทั้ง tenant? | T_doc_numbering |

---

## Section 16: Security & Compliance
> Security Preset: **P2 (Config / Admin)** — Access Control + Audit + Data Classification (Internal)

| กลุ่ม | Control |
|---|---|
| Access Control | เฉพาะ Purchasing Admin/Manager แก้ได้; อื่นอ่าน |
| Audit | T_purchase_config_log append-only (ใคร/เมื่อ/old→new) ทุกการเปลี่ยน |
| Data Classification | config keys = **Internal** (ไม่มีจำนวนเงิน Confidential/ไม่มี PII) |
| Integrity | numbering กันเลขซ้ำ + รีเซ็ตครั้งเดียวต่อรอบ |
| Change Control | (optional) DOA approval สำหรับ config change สำคัญ (Q1) |

---

## Section 17: Health Check (SLA/KPI)
| ตัวชี้วัด | Target | เตือน |
|---|---|---|
| โหลด/บันทึก config | < 1 วินาที | > 3 วินาที |
| ความถูกต้อง running number (ไม่ซ้ำ) | 100% | เลขซ้ำ = critical |
| config ที่ PR/PO อ่าน = ค่าล่าสุด | real-time | cache เก่า = แจ้ง |
| ครบ audit การเปลี่ยน config | 100% | < 100% = gap |

---

## Section 18: Monitoring
| Widget / Report | คำอธิบาย |
|---|---|
| Config Audit Log | ประวัติการเปลี่ยน config (ใคร/เมื่อ/old→new) |
| Numbering Status | next_no + รอบรีเซ็ต ต่อชนิดเอกสาร |
| Active Config Snapshot | ค่าปัจจุบันที่ PR/PO ใช้อยู่ |
| Boundary Map | กติกาที่เกี่ยวข้องอยู่โมดูลไหน (read-only) |

---

## Appendix
### A. Locked Decisions (จาก P2P Cheat Sheet — ไม่ทำเป็น config)
- D01 payment term เลือกที่ PO เท่านั้น (PR/Comparison ไม่มี) · D02 GRN trigger ตาม payment type · D03 รับไม่ครบ = Partial เสมอ · D04 auto-close PO เมื่อ GRN ครบ · D05 เปลี่ยน payment type หลัง PO approve ไม่ได้ · D06 3-Way Match บังคับ · D07 Close PO balance trigger ที่ GRN · D08 Deposit inherit %+ปรับที่ PO · D09 Installment inherit+ปรับ %/due · D10 Partial: GRN กำหนดยอด · D11 Credit overdue เตือนไม่ block · D12 Subcontract lock=full_postpay · D13 PV 2 types เอกสารเดียว · D14 CN จาก vendor เท่านั้น · D15 Installment ≠ Partial

### B. Boundary Decisions (stakeholder ยืนยัน)
- ปลดอายัด/release-ref → Budget Config · approval → DOA · payment term → Finance · GRN/QC/Putaway → Inventory Config · Direct Payment → Finance/Accounting (เปิดที่ AP Invoice) · payment types ดึงจาก Payment Term

### C. Prototype Reference
- `purchase-config.html` (final-check PASS: technical + standard) — 2 tabs (ตั้งค่าทั่วไป + เลขที่เอกสาร), Flow Preview สด, payment types checklist, boundary/locked cards
