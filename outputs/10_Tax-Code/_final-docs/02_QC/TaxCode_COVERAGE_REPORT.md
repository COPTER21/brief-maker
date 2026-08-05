# Coverage Report — F-TAX (รอบ 1: HTML) · R2 re-run

- วันที่: 2026-08-05 · re-run ของ `TaxCode_COVERAGE_REPORT_R1.md` (R1 verdict = PASS 28/28)
- Contract: `PREBRIEF_F-TAX_TaxCode.md` (node-level) + `CENTRAL_PLAN_CORE_ERP.md` v1.4 (global/edge authority) + approved `AI_DEFAULTS.md` + `DECISION_LOG.md`
- Node: F-TAX · Accounting · Shared Foundation · W1
- Artifact: `outputs/10_Tax-Code/01_HTML/TaxCode.html` (2839 บรรทัด) · route `#/accounting/setup/tax-codes` (L2086)
- Checklist (สืบทอดจาก R1): edge in 1 · edge out 5 · obligations/rules 14 · exception paths 5 · scope guards 3 = **28 รายการ**
- Contract health: ไม่มี `workflow_graph.json`/ไฟล์ชื่อ `NODE_BRIEF` — ใช้ PREBRIEF F-TAX เป็น node-level contract ตามขอบเขตที่ผู้ใช้อนุมัติ (ไม่หยุด ตาม instruction) และ Central Plan เป็น edge authority
- รอบนี้ = HTML only · FRD/TC ยังไม่มี → คอลัมน์ FRD/TC = "—" (NOT-CHECKED ไม่ใช่ fail)
- โฟกัส re-run: การเปลี่ยนแปลง HTML ตั้งแต่ R1 — คอลัมน์ "การใช้งาน" ถูกถอดจาก list (9→8 คอลัมน์), ข้อมูล usage ย้ายไป View Drawer + KPI "ถูกอ้างอิงแล้ว", วันมีผลเริ่ม/สิ้นสุดแยกคอลัมน์, ปรับ CI/density

## Verdict: 🟢 PASS

สรุป: HTML ครอบ **28/28** รายการ · gap block 0 · gap warn 0 · NOT-CHECKED (HTML) 0 · scope creep 0
ทุก evidence citation ของ R1 ยังยืนหยัด (พร้อม line ปัจจุบัน); การถอดคอลัมน์ไม่ทำให้ item ใดหลุด — usage info ยังเข้าถึงได้ครบ

## Coverage Matrix — Edges (1 in · 5 out)

| Item | ประเภท | HTML | FRD | TC | Evidence / หมายเหตุ |
|---|---|---:|---:|---:|---|
| CoA → Tax Code | edge in `[config]` | ✓ | — | — | GL master combobox `initSearchSelect` L2575/2578/2581; `GL_ACCOUNTS` filter current company + active + posting_allowed L2101 (seed GL-099 inactive + GL-X01 COMP-002 ถูกกรองทิ้ง — พิสูจน์ filter); `isAllowedGL` บังคับก่อน active L2606-2609 |
| Tax Code → SO / AR Invoice | edge out `[config]` | ✓ | — | — | picker modal context "เอกสารขาย (SO / AR Invoice)" L2807; กรอง VAT `sale/both` L2792; `captureSnapshot` บันทึก snapshot L2820-2824 |
| Tax Code → PO / AP Invoice | edge out `[config]` | ✓ | — | — | context "เอกสารซื้อ (PO / AP Invoice)" L2807; กรอง VAT `purchase/both` L2793; WHT แสดง pill "แนะนำ · ยืนยันตอนจ่าย" L2800, ยังไม่ final (block snapshot L2822) |
| Tax Code → Payment Voucher / WHT | edge out `[config]` | ✓ | — | — | context "ใบสำคัญจ่าย (ยืนยัน WHT)" L2807; WHT `PAYMENT` เลือกได้จริง L2796 + captureSnapshot; เป็นจุด final ตาม AI-DEFAULT #6 |
| Tax Code → VAT Return (PP.30) | edge out/report | ✓ | — | — | `vatReportCategory` STANDARD/ZERO_RATED/EXEMPT L2173/2627; sidebar link `#/accounting/reports/vat-return` "ภ.พ.30" L1496-1497; view drawer "หมวดรายงาน VAT" L2734 |
| Tax Code → WHT report | edge out/report | ✓ | — | — | WHT `incomeCategoryCode` + `reportMappingRule='RESOLVE_BY_PAYEE_AND_PAYMENT_CONTEXT'` L2174-2175/2628-2629; sidebar link `#/accounting/reports/withholding-tax` "ภงด.3 / 53" L1499-1500; Payment context เป็น source |

## Coverage Matrix — Rules / Obligations (14)

| Item | ประเภท | HTML | FRD | TC | Evidence / หมายเหตุ |
|---|---|---:|---:|---:|---|
| OB-1 VAT + WHT | obligation | ✓ | — | — | family tabs VAT/WHT L2333-2334; conditional form fields L2438-2469; picker แยก VAT/WHT group L2809-2810 |
| FN-01 preset ไทย 7 code พร้อม GL | block | ✓ | — | — | mock TX-01/02/03 (VAT) + TX-05/06/07/08 (WHT) พร้อม GL L2121-2155; รวม TX-04 inactive + TX-09 draft = 9 records; KPI "รหัสทั้งหมด" nTotal L2326 |
| BR-01 code unique | block | ✓ | — | — | `validateForm()` L2596-2597 ตรวจ company + case-insensitive; inline error "รหัสนี้มีอยู่แล้วในบริษัทปัจจุบัน" |
| BR-02 used rate immutable | block | ✓ | — | — | `rateLocked = isEdit && rec.used>0` L2424; rate input `disabled` + ป้าย "อ่านอย่างเดียว" L2453-2455; family/kind/direction ก็ล็อก L2431/2441/2464 |
| BR-02 replacement lineage | block | ✓ | — | — | `openReplacement()` L2394-2410 (eyebrow "สร้างรหัสแทน"); commit ตั้ง `replacedByTaxCodeId` + ปิด effEnd เดิม = วันก่อน effStart ใหม่ (`previousDate`) L2648-2650; view drawer "ใช้แทนรหัส"/"ถูกแทนด้วย" L2738-2739 |
| BR-03 WHT income type required | block | ✓ | — | — | searchable income type L2582-2585; `validateForm()` block เมื่อว่าง "WHT ต้องระบุประเภทเงินได้" L2604 |
| BR-04 GL required before active | block | ✓ | — | — | `validateForm(forActive)` บังคับ GL ตาม direction L2606-2609 (VAT sale/purchase, WHT payable); draft บันทึกได้โดยไม่บังคับ (forActive=false) |
| BR-05 / global no hard delete | block | ✓ | — | — | ไม่มี record deletion mutation (grep `delete/splice` = เฉพาะ formErrors/Set/classList); active→`confirmDeactivate`, draft→`confirmArchiveDraft` L2307-2308; modal ยืนยัน "ระบบไม่มีการลบถาวรสำหรับรหัสภาษี" L2776 |
| State draft→active→inactive/archived | rule | ✓ | — | — | status filter + pills L2341-2347; submit activate L2672-2673; `doArchive` draft→archived / active→inactive L2757-2765 |
| Effective-date picker | block | ✓ | — | — | `isPickable(r, documentDate)` ตรวจ company/status/effStart/effEnd L2219-2224; picker ใช้วันที่เอกสาร `setPickerDate` L2808/2817; วันมีผลเริ่ม/สิ้นสุดแยก 2 คอลัมน์ L2302-2303 |
| Config snapshot / soft reference | global block | ✓ | — | — | `captureSnapshot()` เก็บ id/company/code/name/family/vatKind/rate/direction/context/documentDate L2823; ข้อความ deactivate "เอกสารเดิม...ยังใช้งานได้ตามปกติ" L2783 |
| Append-only audit | global block | ✓ | — | — | `audit.unshift(...)` ทุก event create/update/deactivate/archive/replacement L2640/2643/2650/2762; view drawer timeline L2703-2705/2742 (guard `view_audit`) |
| Company scope | `[AI-DEFAULT]` | ✓ | — | — | `CURRENT_COMPANY=COMP-001` L2066; records/uniqueness/GL lookup ผูก company L2101/2231/2596; footer "· THB · ประเทศไทย" L2354; ไม่มี company switcher ในฟอร์ม |
| Permissions | `[AI-DEFAULT]` | ✓ | — | — | `CURRENT_PERMISSIONS` 6 สิทธิ์ L2068-2069, `can()` L2071; gate create/update/deactivate/activate/view_audit L2306-2308/2321/2664/2672-2673/2708-2712/2742 |

## Coverage Matrix — Exception Paths (5)

| Path | HTML | FRD | TC | Evidence |
|---|---:|---:|---:|---|
| อัตราเปลี่ยนหลังถูกใช้ | ✓ | — | — | rate read-only (L2424/2453) → `openReplacement` L2394 → lineage + effEnd split L2648-2650 |
| GL ไม่ครบแต่ต้องเก็บงาน | ✓ | — | — | active validation block GL L2606-2609 + ปุ่ม "บันทึกร่าง" (draft ไม่บังคับ GL); demo TX-09 draft ไม่ผูก GL L2156-2160 |
| inactive / หมดช่วงวันที่ | ✓ | — | — | `isPickable` คัดออกจาก picker L2219-2224/2790-2796; demo TX-04 inactive+effEnd อดีต L2134-2138; deactivate modal อธิบายเอกสารเดิมใช้ได้ L2783 |
| ปิด active / เลิก draft | ✓ | — | — | `confirmDeactivate`/`confirmArchiveDraft` L2755-2756 → `doArchive` L2757; ไม่มี physical deletion |
| WHT ที่ AP ยังไม่ final | ✓ | — | — | PURCHASE context pill "แนะนำ · ยืนยันตอนจ่าย" L2800; `captureSnapshot` block WHT ใน PURCHASE (toast เตือน) L2822; final ที่ PAYMENT L2796 |

## Scope Guard (3)

| Guard | ผล | Evidence |
|---|---:|---|
| ไทย/THB เท่านั้น (S-06) | ✓ ไม่หลุด | footer "· THB · ประเทศไทย" L2354; `CURRENT_COMPANY.country='TH'` L2066; ไม่มี jurisdiction/currency selector |
| Default code ต่อเอกสาร (OQ-1) | ✓ ไม่หลุด | ไม่มี config/default-assignment UI; picker ให้ผู้ใช้เลือกตาม context เท่านั้น L2787-2814 |
| Incoming WHT ฝั่งลูกค้าหักเรา (OQ-2) | ✓ ไม่หลุด | WHT direction = `pay` เท่านั้น L2622/2140-2158; context final อยู่ Payment Voucher ฝั่งจ่าย ไม่มี incoming flow |

## Gaps

ไม่มี gap ในรอบ HTML (R2)

## Warnings / Scope Creep

ไม่พบ scope creep — ทุก route/เมนู/action อยู่ในขอบเขต PREBRIEF; company scope, permission, replacement lineage เป็น `[AI-DEFAULT]` ที่อนุมัติแล้ว

## R1 → R2 Diff (การเปลี่ยนแปลง HTML)

**ปิดแล้ว:** ไม่มี (R1 ไม่มี gap)
**ยังค้าง:** ไม่มี
**gap ใหม่:** ไม่มี

### การย้าย evidence จากการแก้ HTML — ตรวจแล้วยังครอบครบ

1. **คอลัมน์ "การใช้งาน" ถูกถอดจาก list (9→8 คอลัมน์)** — row rendering ปัจจุบัน (L2296-2310) มี 8 คอลัมน์: รหัส · ชื่อ · อัตรา · ทิศทาง/ประเภทเงินได้ · วันมีผลเริ่ม · วันมีผลสิ้นสุด · สถานะ · actions (header L2352, `colspan=8` L2293). ฟังก์ชัน `usedCell()` ยังนิยามอยู่ (L2225-2228) แต่**ไม่ถูกเรียกในแถวตารางแล้ว**.
   - ⚠️ **Evidence relocation (ไม่ใช่ gap):** ข้อมูล usage / "badge ใช้แล้ว N เอกสาร" (PREBRIEF §6 / FN-06) ที่เดิมอยู่ในคอลัมน์ list ตอนนี้เข้าถึงผ่าน 2 ทาง: (a) **KPI "ถูกอ้างอิงแล้ว"** = จำนวนรหัสที่ used>0 (L2329, `nUsed` L2285) และ (b) **View Drawer** used-chip "ใช้แล้ว N เอกสาร" (L2692 → render L2726). ยืนยันข้อมูล reachable ครบ → item ที่พึ่ง usage info (FN-06, BR-02 used-immutable, soft-reference) ยังคง ✓.
2. **วันมีผลเริ่ม/สิ้นสุดแยก 2 คอลัมน์** (DECISION C1) — ยืนยัน header L2352 + cells L2302-2303 (`class="effective-date"`). สอดคล้อง contract §3, ไม่กระทบ item ใด.
3. **CI colors + density ปรับ** (DECISION C6) — อยู่นอกขอบเขต coverage-checker (เป็นงาน `qc-ux-html-checker`); ไม่กระทบ business coverage. ไม่ประเมินที่นี่.

**สรุป diff:** R1 matrix ไม่มีแถวใดที่อ้าง evidence เป็น "คอลัมน์การใช้งาน" โดยตรง (R1 อ้าง KPI/drawer/JS logic อยู่แล้ว) → **ไม่มี evidence citation ของ R1 ที่พังจากการถอดคอลัมน์**; รายการที่พึ่งข้อมูล usage ถูกยืนยันซ้ำว่ายังเข้าถึงได้ผ่าน View Drawer + KPI.

## ⬜ NOT-CHECKED (รอรอบ 2)

- FRD Pack และ testcases-*.md ยังไม่ถูกสร้าง → ทุกคอลัมน์ FRD/TC = "—". รอบ 2 ต้องยืนยัน:
  - backend-only enforcement: uniqueness/concurrency, active-GL validation, immutable used-rate, effective overlap, soft-reference snapshot immutability, append-only audit
  - ทุก block rule มี TC ≥ 1 · ทุก exception path มี TC ≥ 1
  - WHT report contract ต้องระบุว่าอ่านรายการหักที่ final จาก Payment Voucher ไม่อ่าน suggestion จาก AP Invoice (AI-DEFAULT #6)

## 💡 เสนอเข้า contract (ไม่กระทบ verdict)

- ระหว่างตรวจไม่พบ flow มาตรฐานที่ contract ขาด — ไม่มีข้อเสนอเพิ่มเข้า graph รอบนี้
- FLAG-1 (DECISION_LOG C2/F1): WHT GL picker filter เฉพาะ `WHT_PAYABLE` (HTML ทำแบบนี้ L2581/2609, สอดคล้อง AI-DEFAULT #3) — ยังรอ user เคาะข้อความ msg #1571 ที่กำกวม ก่อน BRD; ไม่กระทบ coverage verdict
