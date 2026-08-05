# PREBRIEF · F-TAX Tax Code — รหัสภาษี
> W1 · Accounting · Shared Foundation · prior: reg · [STD] ภาษีไทย: VAT 7%/0%/ยกเว้น · WHT ภงด. 1/2/3/5% ตามประเภทเงินได้ · 2026-08-04

## 0. Obligations
| # | พันธะ | จาก | ตอบที่ |
|---|---|---|---|
| OB-1 | ครอบ 2 ตระกูล: VAT (ขาย/ซื้อ) + Withholding Tax (หัก ณ ที่จ่าย) | [STD] | §3 |
| OB-2 | ผู้บริโภคหนัก: ทุกเอกสารเงิน (SO/PO/Invoice line VAT mode, บิล WHT), VAT Return (PP.30), Withholding Tax report (W13) | เส้นในแผน | §9 |
| OB-3 | ผูก GL account (ภาษีขาย/ภาษีซื้อ/WHT ค้างจ่าย) เพื่อ posting อัตโนมัติ | [STD] | §3 |
| OB-4 | soft ref + อัตราเปลี่ยนตามกฎหมาย = เพิ่ม code ใหม่/กำหนดวันมีผล ไม่แก้ของเดิม | [STD] | BR-02 |

## 1. สรุป: master รหัสภาษีที่เอกสารทุกใบอ้าง — มี preset ไทยครบ ตั้งแต่วันแรก · Admin บัญชีจัดการ

## 2. Scenarios
| S | ประเภท | ชื่อ | ที่มา |
|---|---|---|---|
| S-01 | Happy | preset ตั้งต้น: VAT7 (ขาย/ซื้อ) · VAT0 (ส่งออก) · VAT-EX (ยกเว้น) · WHT1% (ขนส่ง) · WHT2% (โฆษณา) · WHT3% (บริการ/จ้างทำของ) · WHT5% (เช่า) — พร้อม GL ผูก | [STD] |
| S-02 | Alt | เพิ่ม code ใหม่: ตระกูล/อัตรา/ทิศ (ขาย-ซื้อ-ทั้งคู่)/GL/วันมีผล | [แผน] |
| S-03 | Exception | อัตราเปลี่ยนตามกฎหมาย (เช่น VAT กลับ 10%): สร้าง code ใหม่ + วันมีผล — **ห้ามแก้อัตราใน code เดิม** (เอกสารเก่าอ้างอยู่) | [STD] BR-02 |
| S-04 | Alt | ปิดใช้ code — เอกสารใหม่เลือกไม่ได้ ของเดิมคำนวณ/รายงานได้ปกติ | soft ref |
| S-05 | Exception | ลบ code ที่ถูกใช้แล้ว → บล็อก (soft archive เท่านั้น) | กติกากลาง |
| S-06 | **ไม่รองรับ** | ภาษีต่างประเทศ/multi-jurisdiction — THB/ไทยเท่านั้น | [มติ] |

## 3. Data — TaxCode: code · ชื่อ · ตระกูล (VAT/WHT) · อัตรา % · ทิศ (output ขาย/input ซื้อ/both — WHT: จ่าย) · ประเภทเงินได้ (WHT — เพื่อ ภงด.3/53) · GL account (combobox CoA) · วันมีผลเริ่ม-สิ้นสุด · สถานะ
## 4. BR: BR-01 code unique · BR-02 อัตราแก้ไม่ได้หลังถูกใช้ — เปลี่ยน = code ใหม่+วันมีผล · BR-03 WHT ต้องระบุประเภทเงินได้ (โยงรายงาน ภงด.) · BR-04 ทุก code ต้องผูก GL ก่อน active · BR-05 soft archive
## 5. State: draft → active → inactive/archived
## 6. Actions: list แยกแท็บ VAT/WHT + เพิ่ม/แก้ drawer 680 + badge "ใช้แล้ว N เอกสาร" (mock)
## 7. Data behaviour: soft archive · audit · วันมีผลคุมการโผล่ใน picker
## 8. Mock: preset 7 code ตาม S-01 + code ปิดใช้ 1 + ใช้แล้วลบไม่ได้ demo
## 9. Edges (ออก [config] — โหมดเดียว): → ทุกเอกสารเงิน (VAT mode/line tax picker) · → PP.30 · → WHT report (ภงด.3/53) · เข้า: ← CoA
## 10. OQ: OQ-1 default code ต่อเอกสาร (SO default VAT7?) เก็บที่ config module ไหน (Strike) · OQ-2 WHT ฝั่งถูกหัก (ลูกค้าหักเรา) เฟสนี้ไหม (Strike)
## 11. Coverage ✓

---
# Function Checklist · F-TAX
| FN | ต้องทำอะไรได้ | trace | WF | DEV | QA |
|---|---|---|---|---|---|
| FN-01 | preset ไทย 7 code ครบพร้อม GL ตั้งแต่ mock แรก | S-01 | ☐ | ☐ | ☐ |
| FN-02 | เพิ่ม code + validate GL บังคับก่อน active | S-02 BR-04 | ☐ | ☐ | ☐ |
| FN-03 | อัตราของ code ที่ใช้แล้ว = read-only + flow "สร้างตัวแทน+วันมีผล" | S-03 | ☐ | ☐ | ☐ |
| FN-04 | WHT บังคับประเภทเงินได้ | BR-03 | ☐ | ☐ | ☐ |
| FN-05 | inactive/วันหมดผล → หายจาก picker ใหม่ ของเดิมปกติ | S-04 | ☐ | ☐ | ☐ |
| FN-06 | ใช้แล้วลบไม่ได้ + badge จำนวนเอกสารที่อ้าง | S-05 | ☐ | ☐ | ☐ |
| FN-90 | audit + soft archive | กติกากลาง | ☐ | ☐ | ☐ |

ไม่รองรับ: ภาษีต่างประเทศ (S-06) · ฝั่งถูกหัก (รอ OQ-2)
