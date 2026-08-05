# Coverage Report — F-TAX (รอบ 1: HTML)

- วันที่: 2026-08-05
- Contract: `PREBRIEF_F-TAX_TaxCode.md` + `CENTRAL_PLAN_CORE_ERP.md` v1.4 + approved `AI_DEFAULTS.md`
- Node: F-TAX · Accounting · Shared Foundation · W1
- Artifact: `01_HTML/TaxCode.html` · route `#/accounting/setup/tax-codes`
- Checklist: edge in 1 · edge out 5 · obligations/rules 14 · exception paths 5 · scope guards 3
- หมายเหตุ contract health: ไม่มี `workflow_graph.json`/ไฟล์ชื่อ `NODE_BRIEF`; รอบนี้ใช้ PREBRIEF F-TAX เป็น node-level contract ตามขอบเขตที่ผู้ใช้อนุมัติ และใช้ Central Plan เป็น global/edge authority

## Verdict: 🟢 PASS

สรุป: HTML ครอบ 28/28 รายการ · gap block 0 · gap warn 0 · NOT-CHECKED 0

## Coverage Matrix — Edges

| Item | ประเภท | HTML | FRD | TC | Evidence / หมายเหตุ |
|---|---|---:|---:|---:|---|
| CoA → Tax Code | edge in `[config]` | ✓ | — | — | create/edit drawer ใช้ searchable GL master combobox; `GL_ACCOUNTS` กรอง current company + active + posting allowed; GL required ก่อน active |
| Tax Code → SO / AR Invoice | edge out `[config]` | ✓ | — | — | modal “ตัวเลือกตามวันที่เอกสาร” context “เอกสารขาย (SO / AR Invoice)” กรอง VAT `sale/both` และบันทึก snapshot |
| Tax Code → PO / AP Invoice | edge out `[config]` | ✓ | — | — | context “เอกสารซื้อ (PO / AP Invoice)” กรอง VAT `purchase/both`; WHT แสดงเป็นคำแนะนำและยังไม่ final |
| Tax Code → Payment Voucher / WHT | edge out `[config]` | ✓ | — | — | context “ใบสำคัญจ่าย (ยืนยัน WHT)” เลือก WHT และบันทึก snapshot; มีข้อความว่า Payment เป็นแหล่ง WHT report |
| Tax Code → VAT Return (PP.30) | edge out/report | ✓ | — | — | VAT records มี `vatReportCategory`; sidebar link `#/accounting/reports/vat-return`; view drawer แสดงหมวดรายงาน |
| Tax Code → WHT report | edge out/report | ✓ | — | — | WHT records มี income category + downstream mapping rule; sidebar link `#/accounting/reports/withholding-tax`; Payment context เป็น source |

## Coverage Matrix — Rules / Obligations

| Item | ประเภท | HTML | FRD | TC | Evidence / หมายเหตุ |
|---|---|---:|---:|---:|---|
| OB-1 VAT + WHT | obligation | ✓ | — | — | VAT/WHT tabs และ conditional form fields |
| FN-01 preset ไทย 7 code พร้อม GL | block | ✓ | — | — | mock TX-01/02/03/05/06/07/08; KPI 9 records = preset 7 + inactive + draft |
| BR-01 code unique | block | ✓ | — | — | `validateForm()` ตรวจ company + case-insensitive code; inline error |
| BR-02 used rate immutable | block | ✓ | — | — | edit used record: rate disabled; CTA “สร้างรหัสแทน” |
| BR-02 replacement lineage | block | ✓ | — | — | `replacesTaxCodeId` + `replacedByTaxCodeId`; ปิดช่วงรหัสเดิมเป็นวันก่อน effective start ใหม่ |
| BR-03 WHT income type required | block | ✓ | — | — | searchable income type + `validateForm()` block เมื่อว่าง |
| BR-04 GL required before active | block | ✓ | — | — | VAT บังคับ sale/purchase GL ตาม direction; WHT บังคับ payable GL; draft ยังบันทึกได้ |
| BR-05 / global no hard delete | block | ✓ | — | — | ไม่มี delete mutation/action; active → deactivate, draft → archive; confirmation modal |
| State draft→active→inactive/archived | rule | ✓ | — | — | lifecycle filter/pills, submit activate, deactivate/archive actions |
| Effective-date picker | block | ✓ | — | — | `isPickable(record, documentDate)` ตรวจ status/company/start/end; modal เปลี่ยนวันที่ได้ |
| Config snapshot / soft reference | global block | ✓ | — | — | `captureSnapshot()` เก็บ id/company/code/name/family/kind/rate/direction/context/date; ข้อความไม่คำนวณย้อนหลังจาก master |
| Append-only audit | global block | ✓ | — | — | audit timeline + append events สำหรับ create/update/deactivate/archive/replacement |
| Company scope | `[AI-DEFAULT]` | ✓ | — | — | shell แสดงบริษัทปัจจุบัน; records/uniqueness/GL lookup ผูก `COMP-001` |
| Permissions | `[AI-DEFAULT]` | ✓ | — | — | guards `view/create/update/activate/deactivate/view_audit`; actions render ตามสิทธิ์ |

## Coverage Matrix — Exception Paths

| Path | HTML | Evidence |
|---|---:|---|
| อัตราเปลี่ยนหลังถูกใช้ | ✓ | rate read-only → replacement flow → lineage + effective-date split |
| GL ไม่ครบแต่ต้องเก็บงาน | ✓ | active validation block + “บันทึกร่าง” |
| inactive/หมดช่วงวันที่ | ✓ | ไม่เข้า picker ใหม่; view drawer อธิบายว่าเอกสารเดิมใช้ snapshot ได้ |
| ปิด active / เลิก draft | ✓ | confirm deactivate / archive; ไม่มี physical deletion |
| WHT ที่ AP ยังไม่ final | ✓ | purchase context แสดง pill “แนะนำ · ยืนยันตอนจ่าย”; Payment context เป็นจุด snapshot |

## Scope Guard

| Guard | ผล | Evidence |
|---|---:|---|
| ไทย/THB เท่านั้น | ✓ | footer company · THB · ประเทศไทย; ไม่มี jurisdiction selector |
| Default code ต่อเอกสาร (OQ-1) | ✓ ไม่หลุด scope | ไม่มี config/default assignment; picker ให้ผู้ใช้เลือกตาม context |
| Incoming WHT ฝั่งลูกค้าหักเรา (OQ-2) | ✓ ไม่หลุด scope | WHT direction เป็นจ่ายและ context final อยู่ Payment Voucher เท่านั้น |

## Gaps

ไม่มี gap ในรอบ HTML

## Warnings / Scope Creep

ไม่พบ scope creep; company scope, permission และ replacement lineage เป็น `[AI-DEFAULT]` ที่ผู้ใช้อนุมัติแล้ว

## ข้อส่งต่อรอบ 2

- FRD ต้องเก็บ backend-only enforcement ของ uniqueness/concurrency, active GL validation, immutable used rate, effective overlap, soft-reference snapshot และ append-only audit
- Test cases ต้องมีอย่างน้อย 1 เคสตรงต่อ block rule และทุก exception path ในตารางนี้
- WHT report ต้องยืนยัน contract ว่าอ่านรายการหักที่ final จาก Payment Voucher ไม่อ่าน suggestion จาก AP Invoice

