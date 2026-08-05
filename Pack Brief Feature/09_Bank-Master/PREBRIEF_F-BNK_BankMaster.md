# PREBRIEF · F-BNK Bank Master — ธนาคาร/บัญชีบริษัท
> W1 · Finance · Shared Foundation (master กลาง — Lite/Full: มากับทุก package ที่มี Finance? **ไม่ — เป็น master กลางที่ Finance/AP/AR ใช้ · ไม่มี tier**) · prior: reg · 2026-08-04

## 0. Obligations
| # | พันธะ | จาก | ตอบที่ |
|---|---|---|---|
| OB-1 | 2 ชั้น: ธนาคาร (lookup มาตรฐาน ธปท.) + บัญชีธนาคารของบริษัท (ต่อ company) | [STD] | §3 |
| OB-2 | ผู้บริโภค: Payment Voucher/Receipt Voucher (จ่าย-รับผ่านบัญชีไหน) · Bank Reconciliation · Payroll | เส้นในแผน | §9 |
| OB-3 | soft reference — เอกสารเก็บ snapshot ชื่อบัญชี · master แก้ไม่ย้อนเอกสารเดิม | LD-4C-02 | BR-03 |
| OB-4 | บัญชีผูก GL account (Chart of Accounts) เพื่อ posting | [STD] | §3 |

## 1. สรุป: master 2 ระดับ — รายชื่อธนาคาร (แก้น้อย มี preset ไทย) + บัญชีบริษัท (เลขบัญชี/สาขา/สกุล/GL) · Admin การเงินจัดการ

## 2. Scenarios
| S | ประเภท | ชื่อ | ที่มา |
|---|---|---|---|
| S-01 | Happy | เพิ่มบัญชีบริษัท: เลือกธนาคาร (preset ธนาคารไทย ~20) + เลขบัญชี + ประเภท (ออมทรัพย์/กระแส) + สาขา + สกุล THB + ผูก GL | [STD] |
| S-02 | Alt | หลายบริษัท — บัญชีแยกตาม company · ตั้งบัญชี default จ่าย/รับ ต่อบริษัท | [แผน] |
| S-03 | Alt | ปิดใช้บัญชี (inactive) — เอกสารใหม่เลือกไม่ได้ ของเดิมโชว์ปกติ | soft ref |
| S-04 | Exception | เลขบัญชีซ้ำในบริษัทเดียว = บล็อก · format เลขตรวจตามธนาคาร [AI-DRAFT — ตรวจแค่ตัวเลข 10-15 หลัก] | [AI-DRAFT] |
| S-05 | Alt | เพิ่มธนาคารนอก preset (ธนาคารต่างประเทศ) — กรอกเอง + swift [AI-DRAFT] | [AI-DRAFT] |
| S-06 | **ไม่รองรับ** | เชื่อม bank API/statement อัตโนมัติ — เฟสถัดไป (ของ Bank Reconciliation) | [มติ] |

## 3. Data — Bank: code ธปท./ชื่อ/swift · CompanyBankAccount: company · bank · เลขบัญชี · ชื่อบัญชี · ประเภท · สาขา · สกุลเงิน (THB เท่านั้น เฟสนี้ [AI-DRAFT — โยง OQ-6 currency ของ PO]) · GL account (combobox จาก CoA) · default จ่าย/รับ flag · สถานะ active/inactive
## 4. BR: BR-01 เลขบัญชี unique ต่อบริษัท · BR-02 default จ่าย/รับ มีได้อย่างละ 1 ต่อบริษัท · BR-03 soft ref (แก้ชื่อไม่ย้อนเอกสาร) · BR-04 inactive = หายจาก picker เอกสารใหม่ · BR-05 บัญชีที่ถูกใช้ในเอกสารแล้วลบไม่ได้ (soft archive เท่านั้น)
## 5. State: active ⇄ inactive → archived — จบ
## 6. Actions: list บัญชีต่อบริษัท (สลับ company) + เพิ่ม/แก้ drawer 680 + toggle default + แท็บ "ธนาคาร" (preset list, เพิ่มพิเศษ)
## 7. Data behaviour: soft archive · audit · masking เลขบัญชีในหน้า list (โชว์ 4 ตัวท้าย, กดดูเต็ม = สิทธิ์+log [AI-DRAFT — data classification])
## 8. Mock: 2 บริษัท · บัญชี 5 (KBank กระแส default จ่าย, SCB ออม default รับ, BBL, inactive 1, บริษัทที่สอง 1) · preset ธนาคารไทย 20 ราย
## 9. Edges (ออก [config] ทั้งหมด — โหมดเดียว): → Payment/Receipt Voucher (picker) · → Bank Reconciliation · → Payroll (บัญชีจ่ายเงินเดือน) · เข้า: ← CoA (ผูก GL)
## 10. OQ: OQ-1 masking เลขบัญชี+สิทธิ์ดูเต็ม (Strike/Policy) · OQ-2 รองรับสกุลอื่นเมื่อไหร่ (Strike — โยง multi-currency)
## 11. Coverage ✓

---
# Function Checklist · F-BNK
| FN | ต้องทำอะไรได้ | trace | WF | DEV | QA |
|---|---|---|---|---|---|
| FN-01 | เพิ่มบัญชี: ธนาคาร combobox (Rule #94) + validate เลข + ผูก GL จาก CoA | S-01 | ☐ | ☐ | ☐ |
| FN-02 | สลับดูตามบริษัท + default จ่าย/รับ อย่างละ 1 | S-02 BR-02 | ☐ | ☐ | ☐ |
| FN-03 | เลขซ้ำในบริษัท = บล็อก | BR-01 | ☐ | ☐ | ☐ |
| FN-04 | inactive → หายจาก picker (mock เอกสาร) ของเดิมโชว์ปกติ | S-03 | ☐ | ☐ | ☐ |
| FN-05 | masking เลขบัญชี + ดูเต็มตามสิทธิ์ (ตามมติ OQ-1) | §7 | ☐ | ☐ | ☐ |
| FN-06 | ใช้แล้วลบไม่ได้ — soft archive + audit | BR-05 | ☐ | ☐ | ☐ |
| FN-90 | audit + validation ครบ | กติกากลาง | ☐ | ☐ | ☐ |

ไม่รองรับ: bank API/statement (S-06) · multi-currency
