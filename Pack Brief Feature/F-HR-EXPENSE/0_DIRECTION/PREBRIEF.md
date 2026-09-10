# PREBRIEF · Expense Claim — เบิกค่าใช้จ่าย
archetype_confirmed: Q-document  (เอกสารธุรกรรมมีเลขรัน + PDF + line editor B2 v2 · ยืนยันตาม STANDARD_BASELINE §3 · Iron Rules #98–101 บังคับ)
source: LANE_BRIEF + STANDARD_BASELINE (MUST 11 · lifecycle 8 state) · dep CONFIG/MOVE/PAYROLL
lang: business ไทยล้วน · [แผน]/[มติ]/[AI-DRAFT]/[STD]/[ASSUMED]

## 0. Obligations
| # | พันธะ | จาก | ตอบที่ § |
|---|---|---|---|
| OB-1 | ผู้เบิก/ตำแหน่ง = soft ref Employee + Movement assignment ณ วันเบิก (snapshot) | LD-4C-02 · F-HR-MOVE §0.13 | §3, S-05, BR-08 |
| OB-2 | เพดานหมวด/นโยบาย = อ่าน HR Configuration (effective_date · #107) | HR-1 · F-HR-CONFIG | §3.4, S-03, BR-02 |
| OB-3 | อนุมัติตามวงเงิน = DOA threshold (GET /doa/resolve · slot picker 17ส.ค.) | current-state §3 | S-08, BR-04, §12 |
| OB-4 | เลข EXP-YYYY-NNNN + สำเนา = ENG-DOC-NUM/STORE (doccfg) | F-DOCCFG | S-01, BR-06, §12 |
| OB-5 | อนุมัติ/ส่ง GL → CSQ FC·AC·EC | STANDARD_BASELINE cap.10 | BR-07, §12 |
| OB-6 | จ่ายจริง/ลงบัญชี = hook (Payroll HK-1 · Accounting ยังไม่มี) | F-HR-PAYROLL §0.13.5 | S-10, S-14, §9 |
| OB-7 | audit append-only · เงิน RESTRICTED masking · ไม่มี hard delete | current-state §3 | BR-10 |

## 1. สรุป + ผู้ใช้ + สิทธิ์
- **ทำอะไร:** ใบเบิกค่าใช้จ่ายพนักงาน (หลายรายการ) → ตรวจเพดานหมวด → อนุมัติตามวงเงิน (DOA) → เลข EXP + PDF → เลือกช่องทางจ่าย → hook GL/Payroll. **ไม่จ่ายเงิน/ไม่ post บัญชีเอง**
- **ผู้ใช้:** พนักงาน (สร้าง/ยื่น) · ผู้อนุมัติตามวงเงิน (หัวหน้า/ผจก./ผอ. ตาม DOA) · HR/Finance (ติดตามสถานะ)
- **สิทธิ์:** จำนวนเงิน = RESTRICTED masking · role จาก login (demo = .demo-strip #105)

## 2. Scenarios (D1-D6)
> D1 ยอด=เพดาน/vat/totals · D2 state doc · D3 อนุมัติ=DOA threshold · D4 อ้างอิง=หมวด/ตำแหน่ง ณ วันเบิก · D5 ปลายทาง=จ่าย/GL/CSQ · D6 STD=itemize/VAT
| S-XX | ประเภท | เรื่อง | ข้อมูลที่ต้องมี |
|---|---|---|---|
| S-01 | Happy | สร้างใบเบิก → เพิ่มรายการ → เพดานผ่าน → ส่ง DOA → อนุมัติ → เลข EXP+PDF → เลือกจ่าย → hook | header(ผู้เบิก·วันที่·ศูนย์ต้นทุน) · lines(วันที่·หมวด·รายละเอียด·เงิน·vat·ใบเสร็จ) · ยอดรวม |
| S-02 | Alt | หลายรายการหลายหมวด · VAT รวม/แยก/ไม่มี · totals ถูกต้อง | vat_mode ต่อบรรทัด · subtotal/vat/grand |
| S-03 | Exception | รายการเกินเพดานหมวด → เตือน/บล็อกตามนโยบาย | เพดานจาก HR Config · ยอดหมวด · policy(warn/block) |
| S-04 | Exception | ไม่มีรายการ/ยอด=0 → ส่งไม่ได้ | validation |
| S-05 | Alt | ตำแหน่ง/ศูนย์ต้นทุน ณ วันเบิก จาก Movement resolve (snapshot) | position/cost_center snapshot |
| S-06 | Alt | ไม่อนุมัติ/ตีกลับ (rejected) → แก้ยื่นใหม่ | เหตุผล · กลับ draft |
| S-07 | Alt | ยกเลิกใบเบิกก่อนอนุมัติ (cancelled) | สถานะ |
| S-08 | Exception | ยอดต่างช่วงวงเงิน → DOA resolve สายต่างกัน (threshold) — ประกาศ ไม่ hardcode | ยอดรวม · matrix threshold |
| S-09 | Happy | อนุมัติ → FC(commit งบ) + เลข/PDF/สำเนา(DOCCFG) + EC(มูลค่า) | events |
| S-10 | Alt | เลือกช่องทางจ่าย: ผ่านรอบเงินเดือน (Payroll HK-1) / โอนตรง [A-EXP-01] | pay_method · hook |
| S-11 | Exception | แก้ยอดหลังส่งอนุมัติ → re-resolve DOA ถ้าข้ามช่วง (BR-DOA-05) | re-resolve chain |
| S-12 | Alt | itemize รายบรรทัด · VAT none/add/included | B2 line editor |
| S-13 | Exception | แนบใบเสร็จไม่ครบตามนโยบายหมวด → เตือนก่อนส่ง | attach required by category |
| S-14 | Alt | จ่ายแล้ว (paid) — hook status อ่านจาก Payroll/Finance (display-only) | pay_status hook |
| S-15 | Alt | PDF ใบเบิก + ลายเซ็นอนุมัติ (sign tab) | a4 + signature |

## 3. Data — full data dict
### 3.1 Header
| field | ชนิด | บังคับ | ที่มา |
|---|---|---|---|
| doc_no (EXP-YYYY-NNNN) | text | auto ตอนอนุมัติ | ENG-DOC-NUM (doccfg) |
| ผู้เบิก | ref Employee (snapshot ชื่อ/รหัส) | ✓ | Employee Master |
| ตำแหน่ง·แผนก·ศูนย์ต้นทุน | snapshot ณ วันเบิก | ✓ | Movement assignment/resolve [OB-1] |
| วันที่เอกสาร | date (พ.ศ.) | ✓ | — |
| ช่องทางจ่าย | enum: ผ่านเงินเดือน/โอนตรง | ✓ | [A-EXP-01] |
| สถานะ | enum §5 | auto | state machine |
| ยอดรวม (computed) | money | auto | totals() |
| config_version_id | snapshot | auto | HR Config resolve |
### 3.2 Lines (grid B2 v2)
| field | ชนิด | บังคับ | หมายเหตุ |
|---|---|---|---|
| วันที่ | date (พ.ศ.) | ✓ | ต่อรายการ |
| หมวดค่าใช้จ่าย | ref (จาก HR Config เพดานหมวด) | ✓ | combobox |
| รายละเอียด | text | ✓ | — |
| จำนวนเงิน | money >0 | ✓ | BR-01 |
| VAT mode | segmented none/add/included | ✓ | calcLineVat |
| แนบใบเสร็จ | file | ตามนโยบายหมวด | BR-03/S-13 |
| computed: net/vat/line_total | money | auto | migrateLine/renderLineSummary |
### 3.3 Computed: subtotal · vat รวม · grand total (totals · single source) · เกินเพดานต่อหมวด (flag)
### 3.4 Config ที่อ่าน (ไม่ CRUD · #107)
- HR Configuration `resolve(date, company_id)` — **เพดานหมวด/รายการหมวด [ASSUMED A-EXP-04: ยังไม่มี group นี้ใน HR Config → mock · โครงอ้าง resolve]** · effective_date
- Movement `assignment/resolve(as_of=วันเบิก)` — ตำแหน่ง/ศูนย์ต้นทุน (snapshot · null≠ไม่มี)
- Employee Master — ผู้เบิก (combobox #102)

## 4. Business Rules
| BR | กฎ | trace |
|---|---|---|
| BR-01 | line: เงิน>0 · หมวดจาก HR Config · VAT คำนวณกลาง (calcLineVat) | S-01,S-02,S-12 |
| BR-02 | เพดานหมวด (HR Config resolve) — เกิน = เตือน/บล็อกตามนโยบาย | S-03 |
| BR-03 | ≥1 รายการ + แนบใบเสร็จตามนโยบายหมวด ก่อนส่ง | S-04,S-13 |
| BR-04 | ส่งอนุมัติ = DOA resolve ตามยอดรวม (threshold) · ไม่ hardcode chain (17ส.ค.) | S-01,S-08 |
| BR-05 | แก้ยอดหลังส่ง → re-resolve DOA ถ้าข้ามช่วง (BR-DOA-05) | S-11 |
| BR-06 | เลข EXP-YYYY-NNNN + สำเนา = ENG-DOC-NUM/STORE · ออกตอนอนุมัติ | S-01,S-09 |
| BR-07 | อนุมัติ→FC(commit งบ) · ส่ง GL→AC(ตั้งหนี้/ลงบัญชี) · EC(มูลค่า) | S-09 · §12 |
| BR-08 | ตำแหน่ง/ศูนย์ต้นทุน = snapshot Movement ณ วันเบิก (soft ref) | S-05 |
| BR-09 | จ่ายจริง/post = hook (Payroll/โอน/Accounting) display-only · Expense ไม่ทำเอง | S-10,S-14 |
| BR-10 | audit append-only · เงิน RESTRICTED masking · ไม่มี hard delete | ทุก S |

## 5. State Machine
`ร่าง` → `ยื่น(submitted)` → `รออนุมัติ(pending·DOA)` → `อนุมัติ(approved · เลข+PDF)` → `ส่งจ่าย(sent_to_pay·hook)` → `จ่ายแล้ว(paid·hook)` → `ปิด(closed)`
แยก: `ไม่อนุมัติ/ตีกลับ(rejected)`→draft · `ยกเลิก(cancelled)`
ผู้กด: ผู้เบิก (สร้าง/ยื่น/แก้/ยกเลิก) · DOA approver (อนุมัติ/ตีกลับ) · ระบบ (เลข/PDF/hook/เตือน)

## 6. Actions ต่อหน้า (Q-document · 1 เมนูซ้าย #104)
- **List**: ใบเบิกทั้งหมด · docPill สถานะ · renderSignProgress · filter-row · + สร้างใบเบิก · เอกสารแนบใน landing
- **Wizard 5 steps** (STEPH): เลือกแหล่งที่มา › ข้อมูลหลัก › รายการสินค้า(=รายการค่าใช้จ่าย · B2 line editor) › เอกสารแนบ › ตรวจสอบและยืนยัน
- **View drawer tabs**: รายละเอียด › PDF Preview(a4 ใบเบิก) › ลายเซ็น/อนุมัติ(DOA timeline + sign) › ประวัติ(audit) · เอกสารแนบ = section ใน tab รายละเอียด
- ส่งอนุมัติ = DOA slot picker (threshold) · ตีกลับ/ยกเลิก = confirm

## 7. Data behaviour
totals = single source (totals()) · แก้ยอดหลังอนุมัติ = re-resolve DOA · PDF/เลข = ตอนอนุมัติ (immutable snapshot) · จ่าย = อ่าน hook

## 8. Mock Data Spec
- 5 หมวด: เดินทาง(เพดาน 5,000/ครั้ง) · ที่พัก(2,000/คืน) · รับรอง(3,000) · วัสดุ(ไม่จำกัด) · อื่นๆ
- ผู้เบิก 4 คน (ต่างศูนย์ต้นทุน) · ใบเบิก: ร่าง · รออนุมัติ(ต่างวงเงิน→สายต่าง) · อนุมัติ(มีเลข EXP+PDF) · ตีกลับ · จ่ายแล้ว(hook) · เกินเพดาน(S-03)
- VAT 7% · วันที่ พ.ศ. (2569)

## 9. Edges + ปลายทาง
- แก้ยอดข้ามช่วง DOA → re-resolve (S-11) · เพดานหมวด warn vs block ตามนโยบาย · null cost_center · ปลายทาง: FC/AC/EC + hook จ่าย + NTF + DOCCFG

## 10. OQ + [AI-DRAFT]
| id | เรื่อง | default | owner |
|---|---|---|---|
| A-EXP-01 | ช่องทางจ่ายเลือกต่อใบ | ผ่านเงินเดือน/โอนตรง | Strike |
| A-EXP-02 | จ่ายจริง/GL = hook display-only | [ASSUMED contract รอ FRD Phase B] | Strike |
| A-EXP-03 | DOA threshold ช่วงวงเงิน | <5k หัวหน้า · 5k–50k ผจก. · >50k ผอ. [DEFAULT] | พี่เบิร์ด |
| A-EXP-04 | เพดานหมวดยังไม่มี group ใน HR Config | mock · โครงอ้าง resolve | Strike |
| A-EXP-05 | เกินเพดาน = warn หรือ block | [AI-DRAFT] warn + ต้องเหตุผล (ไม่ hard block) | Strike |

## 11. Coverage Matrix
| S-XX | BR | transition | หน้าจอ/field | FN |
|---|---|---|---|---|
| S-01 | BR-01,04,06 | ร่าง→approved | wizard + list | FN-01,FN-02,FN-07,FN-08 |
| S-02 | BR-01 | — | line editor VAT/totals | FN-03 |
| S-03 | BR-02 | — | เพดานหมวด warn | FN-04 |
| S-04 | BR-03 | บล็อก | validation ส่ง | FN-05 |
| S-05 | BR-08 | — | header cost center snapshot | FN-06 |
| S-06 | BR-04 | pending→rejected | ตีกลับ + แก้ | FN-13 |
| S-07 | BR-10 | →cancelled | ยกเลิก | FN-14 |
| S-08 | BR-04 | pending | DOA threshold slot picker | FN-08 |
| S-09 | BR-06,07 | approved | เลข+PDF+CSQ | FN-09,FN-15 |
| S-10 | BR-09 | approved→sent_to_pay | ช่องทางจ่าย hook | FN-10 |
| S-11 | BR-05 | re-resolve | แก้ยอด | FN-11 |
| S-12 | BR-01 | — | B2 itemize/VAT | FN-03 |
| S-13 | BR-03 | — | แนบใบเสร็จ required | FN-12 |
| S-14 | BR-09 | sent_to_pay→paid | pay status hook | FN-16 |
| S-15 | BR-06 | — | PDF tab + sign tab | FN-15,FN-17 |

## §12 สัญญาณประกาศ (Declaration signals)
| ท่อ | สัญญาณใน PREBRIEF | chip | สรุป |
|---|---|---|---|
| DOA | S-01/S-08 ส่งอนุมัติ **ตามวงเงิน (threshold · มีวงเงิน)** · GET /doa/resolve | ✓ | need |
| NTF | S-01 ยื่น · S-06 ผล/ตีกลับ · S-14 จ่ายแล้ว · S-03 เกินเพดาน (ไม่นับ doa_*) | ✓ | need |
| CSQ | S-09 อนุมัติ→**FC**(commit งบ) · ส่ง GL→**AC**(ตั้งหนี้) · **EC**(มูลค่าค่าใช้จ่าย) | ✓ | need |
| DOCCFG | doc_type **EXP-YYYY-NNNN** + สำเนา (S-01/S-09) | ✓ | need |
| PDF DOC | ใบเบิกค่าใช้จ่าย (a4 · S-15) → thai-doc-pdf-generator | ✓ | need |
DIVERGENCE: — (chip = detect ทุกท่อ)
