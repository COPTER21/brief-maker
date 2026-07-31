# 07_LOCKED_DECISIONS — F-PO-001 ใบสั่งซื้อ (Purchase Order)

> Locked decisions (LD) + convention deviations — ห้ามเปลี่ยนโดยไม่ผ่าน review

---

## §7.1 Locked Decisions
| LD | Decision | Rationale | Source |
|---|---|---|---|
| LD-01 | ตารางผู้ชนะแสดงเฉพาะ source=CP เท่านั้น | ผู้ชนะถูกเลือกที่ Comparison; PR ไม่มีการเปรียบเทียบ | BRD §5.2.2, decision |
| LD-02 | PR-only / PO อิสระ → เลือก vendor ที่ Step 2 (combobox จาก Vendor Master) | ไม่มีผู้ชนะ → ต้องเลือกเอง | BRD §9 R05 |
| LD-03 | แหล่งที่มา "ไม่บังคับ" by default — บังคับเฉพาะเมื่อ Purchase Config ตั้งกฎ | รองรับ 3 โหมด (PR→CP→PO/PR→PO/PO ตรง) | BRD §9 R03 |
| LD-04 | VAT mode ต่อรายการ mutually exclusive (none/add/included) | นิยามการคิด VAT ชัดเจน กัน double-count | BRD §9 R08 |
| LD-05 | ส่วนลดรายการ toggle ฿/% (default %) — ฿ cap ≤ subtotal | ยืดหยุ่นแต่กันติดลบ | BRD §9 R09 |
| LD-06 | ฐาน VAT = ยอดหลังหักส่วนลด; WHT ฐานก่อน VAT | มาตรฐานสรรพากร | BRD §9 R10/R11 |
| LD-07 | DoA ใช้ resolver placeholder {feature_id, cost_center, amount} — ไม่ hardcode tier | CUBE 4.0 governance | BRD §16, F-PC-DOA-01 |
| LD-08 | เลข po_no ออกเมื่อ approved เท่านั้น (draft ไม่มีเลข) | กัน gap ในเลขเอกสาร | BRD §9 R14 |
| LD-09 | approved → เอกสาร immutable (แก้ไม่ได้) | financial control (C-10) | BRD §16 |
| LD-10 | snapshot vendor/item/payment_term ตอนสร้าง | กัน master เปลี่ยนภายหลัง (E14/E15) | BRD §10 |
| LD-11 | PO PDF = 4 variants เลือกอัตโนมัติตามรูปแบบภาษีของ PO; ในหน้า prototype ใช้ตัวอย่าง 1 ชุด (VAT) | per PO_print-spec.md | decision |
| LD-12 | po-amount-engine, doa-resolver-engine, baht-text-engine = reusable engines (3 engines → FULL pack) | logic-placement matrix #6-8 | 03_LOGIC |

## §7.2 Convention Deviations
- ไม่มี deviation จาก naming conventions (camelCase functions, kebab-case engines, snake_case fields, UPPER_SNAKE errors) — ตรงตาม R4

## §7.3 Layout Decisions (inherit จาก BRD §14.6 — ห้าม override)
- P-01 list-view · P-02 create-drawer-wizard 920px · P-03 view-drawer-tabbed + doc/PDF/signature (G/H/I)
- 0 NON-STANDARD override · CI locked · html-generator-v3 v3.9

## §7.4 Global ID Registration Note
- Engine IDs (po-amount-engine ใหม่) จะได้ global CUBIC ID ตอน register ที่ CUBIC Registry
- doa-resolver-engine / baht-text-engine = existing CUBIC engines (reuse)

## §7.5 Pending (รอ stakeholder — ไม่ block FRD)
- Q1 SLA per tier · Q2 WHT table หมวด/rate · Q3 cancel ที่มี GRN บางส่วน
