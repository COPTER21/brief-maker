# STANDARD_BASELINE — F-HR-EXPENSE · เบิกค่าใช้จ่าย (Expense Claim)
> S0.5 baseline · Odoo Expenses · Dynamics 365 Expense management · SAP Concur/T&E → matrix + lifecycle + archetype
> grounding: D365 Expense management (expense report + line items · per-line approval · policy caps · itemization · reimbursement · journal posting)

## 1. Capability matrix (MUST = ที่ทั้ง 3 ค่ายมีเหมือนกัน)
| # | Capability | Odoo | D365 | SAP Concur | CUBE-fit | เหตุผล/มติ |
|---|---|---|---|---|---|---|
| 1 | ใบเบิก header + หลายรายการ (line items) | ✓ | ✓ report+lines | ✓ | **MUST** | Q-document + B2 line editor |
| 2 | รายการ: วันที่·หมวด·รายละเอียด·จำนวนเงิน·VAT | ✓ | ✓ | ✓ | **MUST** | B2 grid + calcLineVat |
| 3 | แนบใบเสร็จ (รายบรรทัด/หัว) | ✓ | ✓ | ✓ (OCR) | **MUST** | upload-zone (OCR = ไม่รองรับ) |
| 4 | เพดาน/นโยบายหมวด (policy cap) เตือน/บล็อกเกิน | △ | ✓ policies | ✓ compliance | **MUST** | อ่าน HR Config เพดานหมวด (HR-1) |
| 5 | อนุมัติตามวงเงิน (approval by amount threshold) | ✓ | ✓ | ✓ | **MUST** | = **DOA threshold** (doa · มีวงเงิน) |
| 6 | เลขที่เอกสาร + PDF ใบเบิก | ✓ | ✓ | ✓ | **MUST** | doccfg EXP-YYYY-NNNN + pdfdoc |
| 7 | VAT/ภาษีต่อบรรทัด | ✓ | ✓ | ✓ | **MUST** | VAT segmented (none/add/included) |
| 8 | ลายเซ็น/ความคืบหน้าอนุมัติ | ✓ | ✓ | ✓ | **MUST** | Q sign tab + renderSignProgress |
| 9 | แจ้งเตือน (ยื่น/ผล/จ่าย/เกินเพดาน) | ✓ | ✓ | ✓ | **MUST** | ENG-NOTIFY (ntf) |
| 10 | มูลค่าค่าใช้จ่าย = ผลกระทบ 7C | △ | ✓ | ✓ | **MUST** | CSQ FC(commit)·AC(ตั้งหนี้)·EC(มูลค่า) |
| 11 | audit append-only + RESTRICTED masking | — | ✓ | ✓ | **MUST** | เงิน RESTRICTED · Policy Center |
| 12 | ศูนย์ต้นทุน/มิติ (จากตำแหน่ง ณ วันเบิก) | ✓ | ✓ dimensions | ✓ | SHOULD | อ่าน Movement assignment/resolve |
| 13 | ช่องทางจ่าย (ผ่านเงินเดือน/โอนตรง) | ✓ | ✓ | ✓ | SHOULD | เลือกต่อใบ [A-EXP-01] · จ่ายจริง=hook |
| 14 | ลงบัญชี/GL posting | ✓ | ✓ | ✓ | **SKIP→hook** | Accounting ยังไม่มี (HK-1 payload) |
| 15 | จ่ายคืนจริง (reimbursement payout) | ✓ | ✓ | ✓ | **SKIP→OQ** | Finance/Payroll (A-EXP-02) |
| 16 | per diem / mileage | ✓ | ✓ | ✓ | NICE→ไม่รองรับ | OQ |
| 17 | คำขออนุมัติเดินทางล่วงหน้า (travel request) | △ | ✓ | ✓ | NICE→ไม่รองรับ | OQ |
| 18 | เงินทดรองจ่าย/เคลียร์ (cash advance) | △ | ✓ | ✓ | NICE→ไม่รองรับ | OQ |
| 19 | หลายสกุลเงิน (multi-currency) | ✓ | ✓ | ✓ | NICE→ไม่รองรับ | THB only รอบนี้ |

**MUST = 11 ข้อ (≥5 ✅)**

## 2. Lifecycle (state machine + actor + เอกสาร)
`ร่าง(draft)` → `ยื่น(submitted)` → `รออนุมัติ(pending·DOA threshold)` → `อนุมัติ(approved → ออกเลข EXP-YYYY-NNNN + PDF)` → `ส่งจ่าย(sent_to_pay·hook)` → `จ่ายแล้ว(paid·hook status)` → `ปิด(closed)`
แยก: `ไม่อนุมัติ/ตีกลับ(rejected → แก้ยื่นใหม่)` · `ยกเลิก(cancelled)`
actor: ผู้เบิก (สร้าง/ยื่น) · ผู้อนุมัติตามวงเงิน (DOA) · ระบบ (เลข/PDF/hook/เตือน) · Finance/Payroll (จ่ายจริง — นอก scope) — **≥3 state ✅ (8 state)**

## 3. Archetype + surfaces
- **archetype = Q-document** (ยืนยันตาม LANE_BRIEF) + **B2 v2 line editor** · Iron Rules #98–101 บังคับ
- surfaces: **สร้าง** ✓ (wizard 5 steps) · **ส่ง** ✓ (submit) · **เซ็น/อนุมัติ** ✓ (DOA sign tab) · **PDF** ✓ (a4 ใบเบิก) · **เตือน** ✓ (NTF) · **รายงาน** ✓ (list docPill + sign progress)

## 4. Declarations
doa ✓ (**threshold · มีวงเงิน**) · ntf ✓ · csq ✓ (FC·AC·EC) · doccfg ✓ (EXP-YYYY-NNNN) · pdfdoc ✓ (ใบเบิก)

## 5. scope note ตัด แต่ standard = MUST → OQ
- **A-EXP-02** จ่ายคืนจริง (cap.15 MUST) · GL posting (cap.14) — CUBE hook display-only · Finance/Accounting ทำ · owner Strike
- per diem/mileage · travel request · cash advance · multi-currency (cap.16–19) = NICE → "ไม่รองรับ" + OQ
