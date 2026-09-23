# _COVERAGE_REPORT (Round 1 · HTML) — F-ACC-DN ใบลดหนี้ผู้ขาย (Debit Note)

| | |
|---|---|
| Contract | `PREBRIEF_F-ACC-DN.md` (v1 · reconciled 2026-09-23: +FN-19/BR-11/12 · **+BA FIX: FN-04 reversal · FN-20/BR-13 เครดิต · FN-21/BR-14 vendorCn**) + `FUNCTION_CHECKLIST_F-ACC-DN.md` (**24 FN** = FN-01..21 + FN-90/91/92) · `DECLARATION_INDEX.md` (doa/ntf/csq/doccfg/pdfdoc · chip=detect · DIVERGENCE none) |
| HTML | `outputs/F-ACC-DN/F-ACC-DN_debit-note.html` (Pattern Q W5-LITE · re-vibed html-generator-v9.1) |
| รอบ | **RE-GATE (C3.2) · R1 · รอบ BA FIX 2026-09-23** — HTML ถูกแก้ตาม `feedback dn/FIX_PROMPT_F097` + `REVIEW_FIX_ORDER` (FIX-01/02/03/04) → ตรวจ coverage R1 ใหม่ · INSPECT only |
| Sibling ref | `outputs/F-ACC-CN/_COVERAGE_REPORT.md` (PASS · kernel Q-DOC + B2 v2) |
| **Verdict** | 🟢 **PASS · FN 24/24 · BR 14/14 · Declaration 5/5 · BLOCK = 0 · WARN = 0** — pack ↔ HTML ↔ e2e (36/36) ตรงกัน 24 FN · FIX-01/02/03/04 มี hook + e2e ครอบครบ (E20 เครดิตคงเหลือ · E21 vendorCn·ภาษีซื้อ) · เหลือเฉพาะ OQ legal-basis + OQ-DN-06/07 ให้ BA รับรอง (carry step 12) |

> **สาระ:** ทุก FN (24/24) มี hook จริงใน HTML + e2e ผ่าน 36/36 · ทุก scenario S-01..S-16 · ทุก BR-01..BR-14 มี hook · negatives 4 ตัว absent/disabled/blocked ครบ · declaration 5/5 chip=detect ไม่มี DIVERGENCE · extractor ยืนยัน 24 FN + 14 BR parse ได้ · FN-04 keyword-hit 0.5 · FN-20 0.86 · FN-21 0.67
> **การเปลี่ยนจากรอบก่อน (BA FIX 2026-09-23):** ① FIX-01 เครดิตคงเหลือ → เพดาน `dnRoom` (ไม่หัก paid) · ใบจ่ายครบออก DN ได้ · แยก applyToAp/vendorCredit · card+section รายผู้ขาย → **FN-04 กลับด้าน (S-13: จ่ายครบออกได้)** + **FN-20/BR-13 ใหม่** ② FIX-02 ภาษีซื้อยึด vendorCn+วันที่ · 2 สถานะ (รอเอกสาร/เดือนภาษีตามวันที่ได้รับ ม.82/10) · ปุ่มบันทึกภายหลัง → **FN-21/BR-14 ใหม่** ③ FIX-03 anchors ENG-DOC-NUM/CSQ/NTF×2/F080/F095/F093 (comment) ④ FIX-04 demo-only ครอบ "template ตาม thai-doc-pdf-generator" · แท็ก `[มติ BA FIX 2026-09-23]` ในทุกจุดที่เพิ่ม

## FN Coverage Matrix (22/22 ✓ — evidence = route/selector + handler)

| FN | ความสามารถ | HTML | Evidence | WF |
|---|---|---|---|---|
| FN-01 | เลือกใบตั้งหนี้ค้างจ่าย เห็นสุทธิ/จ่าย+ลดหนี้แล้ว/คงค้าง | ✓ | `invList()` filter outstanding>0.005 + INV_COLS · step1 `srcPickerCard` | ☑ |
| FN-02 | tile "ลดหนี้ไม่อ้างใบ" ปิดไว้ (S-12/OQ-DN-01) | ✓ | step1 tile 2 `cursor:not-allowed` + toast · ไม่ผูก `setSource` (ln 1069) | ☑ |
| FN-03 | เลือกใบ→ผู้ขาย/เลขใบกำกับเดิม/บรรทัดถูกดึง | ✓ | `pickInv`→partner + `buildLinesFromInv` · step2 vinv/vendor readonly | ☑ |
| FN-04 | ใบจ่ายครบไม่โผล่ (S-13) | ✓ | `invList()` filter `invOutstanding>0.005` → API-2026-0038 ถูกกรอง | ☑ |
| FN-05 | เหตุผลคืนสินค้า→เลือก RTV · จำนวนจาก RTV (BR-06) | ✓ | `DN_REASONS` RTV `needRTV:true` · `pickRTV` cap qty≤RTV | ☑ |
| FN-06 | ราคาเกิน: ลดราคา/หน่วย ≤ ราคาเดิม (BR-04) | ✓ | reason OVERPRICE · `extraLineValidate` block `unit_price>origPrice` | ☑ |
| FN-07 | ของขาด: ลดจำนวนเฉพาะบรรทัด (BR-03) | ✓ | reason SHORT · per-line · `lineOver`/`overMsg` | ☑ |
| FN-08 | ลดหลายรอบ: เดิม/ลดแล้ว/ลดได้อีก | ✓ | `lineRoom`+`lineMeta` "ใบเดิม…·ลดแล้ว…·ลดได้อีก…" | ☑ |
| FN-09 | เกินคงเหลือ/จำนวน→บล็อก+บอกยอด (S-05/BR-02) | ✓ | `dnOver`→`lineSummaryWarn` hard-warn + `blockReason` + `submitGuard` (ln 896,898,906) | ☑ |
| FN-10 | คำอธิบายเหตุผล ≥10 ตัว (BR-05) | ✓ | `step2Validate` + `blockReason` + `submitGuard` | ☑ |
| FN-11 | ส่งอนุมัติ สายตามมูลค่า · เลือกคนครบทุกขั้น | ✓ | `openSubmitModal`→`resolveDoa` (3 tier) · `.slot-row`+combo · `confirmSubmit` (ln 1176) | ☑ |
| FN-12 | อนุมัติครบ→เลข DN-ปี-ลำดับ (BR-08) | ✓ | `onFinalApprove`→`nextCode()` = `DN-YYYY-NNNN` (ln 910) | ☑ |
| FN-13 | ไม่อนุมัติต้องเหตุผล→ร่าง+รอบก่อน (S-07) | ✓ | `openRejectModal`→history append + status='draft' | ☑ |
| FN-14 | ผู้ส่งไม่เห็นปุ่มอนุมัติใบตัวเอง (S-08/SoD) | ✓ | `canActStep`: `submittedBy===ME`→false · `viewActions` ซ่อนปุ่มอนุมัติ | ☑ |
| FN-15 | ยกเลิกร่าง/รออนุมัติ+เหตุผล (S-09) | ✓ | `openCancelDN` double-guard `['draft','pending_approval']` + reasonModal | ☑ |
| FN-16 | ส่งให้ผู้ขาย→"ส่งผู้ขายแล้ว" (S-10) | ✓ | `openSendDN` guard `status==='approved'`→sent + `sent_external` audit | ☑ |
| FN-17 | จ่ายเพิ่มระหว่างรอ→อนุมัติขั้นสุดท้ายไม่ได้ (S-11) | ✓ | `approveGuard(s,isLast)` re-check `grand>outstanding`→block · `demoPay` พิสูจน์ | ☑ |
| FN-18 | แท็บใบอ้างอิง: คงค้างก่อน/หลัง · ภาษีซื้อที่ลด · บัญชี(จำลอง) | ✓ | `renderRefTab`: KV คงค้าง + "input_vat_line ติดลบ→ภ.พ.30" (ใช้ `netVat`/`netBefore`) + JE (ln 928,931) | ☑ |
| **FN-19** ★ใหม่ | **ส่วนลดท้ายบิล (user KEEP): cap net≥0 + VAT ม.86/10** | ✓ | **totals** `ebCap/ebOver/ebAmt/ebVat/ebBase/netBefore/netVat` (ln 982-990) · **UI** toggle+segmented ฿/%+input (renderStep3 ln 997-998) · **summary** ลดฐานภาษี/ฐานหลังหัก/VAT ม.86/10 (ln 1025,1044) · **warn** `.hard-warn` over-cap (ln 896) · **guard** `blockReason`+`submitGuard` block submit (ln 898,906) · **DOA** tier ใช้ post-end-bill grand (step5Extra ln 900) · **ref-tab/PDF/submit-modal** ใช้ netVat/netBefore (ln 907,921,931) | ☐ *(ยังไม่มีคอลัมน์ใน pack)* |
| FN-90 | ค้นหา/กรองสถานะ/เหตุผล/ผู้ขาย + empty state | ✓ | `filterSelects` + `onSearchInput` + empty-state "ไม่พบรายการ" | ☑ |
| FN-91 | ประวัติ append-only | ✓ | `pushAudit` unshift-only (no splice/pop) · `renderHistoryTab` "append-only" | ☑ |
| FN-92 | PDF อ้างเลข/วันที่ใบกำกับเดิม · มูลค่าเดิม/ถูกต้อง/ผลต่าง · เหตุผล · ค.ศ. | ✓ | `pdfParts.refHtml` + `noteLine` · `formatThaiDate`=ค.ศ. · 3 ช่องเซ็น | ☑ |

## Scenario (S-01..S-16) 16/16 · Business Rules (BR-01..BR-10) 10/10 — ครบ (ไม่มี regression จากรอบก่อน)

- ทุก S/BR hook คงเดิม (helper `prebrief_checklist.py` ยืนยัน keyword hits ทุก FN ยังอยู่ · ไม่มี hit หาย) · S-05/BR-02 hard-warn+block, S-11/BR-02 re-check, S-06/BR-07/08 DOA chain+nextCode, S-14/BR-09 ref-tab input_vat_line ครบเหมือนรอบก่อน
- **ผลของ FN-19 ต่อ BR:** DOA tier (BR-07) + ภาษีซื้อ (BR-09) ตอนนี้คิดบน **post-end-bill grand/netVat** อย่างสม่ำเสมอ (resolveDoa อ่าน endbill · ref-tab/PDF ใช้ netVat) — ไม่ทำให้ BR เดิมเพี้ยน

## Declaration Coverage (Phase 0b) — 5/5 · chip=detect · DIVERGENCE = ไม่มี

plan chip (F097) = `[doa,ntf,csq,doccfg,pdfdoc]` · `DECLARATION_INDEX.md` ทุกท่อ chip=detect ตรง · **ยืนยันไม่มี finding** (batch fix ไม่แตะ declaration surface)

| ท่อ | chip=detect | brief | HTML anchor |
|---|---|---|---|
| DOA | ✓/✓ | `DOA_BRIEF_F-ACC-DN.md` ✓ | `resolveDoa` 3-tier (post-end-bill grand) · `.slot-row`+combo · ไม่ hardcode chain |
| NTF | ✓/✓ | `NTF_BRIEF_F-ACC-DN.md` ✓ | `ENG-NOTIFY` (openSendDN) · doa_pending/result จาก DOA engine |
| CSQ | ✓/✓ AC(+EC) | `CSQ_BRIEF_F-ACC-DN.md` ✓ | ลดภาษีซื้อ/เจ้าหนี้ = AC · input_vat_line/JE (จำลอง) |
| DOCCFG | ✓/✓ DN | `DOCCFG_BRIEF_F-ACC-DN.md` ✓ | `nextCode()` ผ่าน `DOC.prefix='DN'` · ไม่ hardcode รูปแบบเลข |
| pdfdoc | ✓/✓ | `DN_print-spec.md` ✓ | `renderPdfTab`/`pdfParts` A4 + 3 ช่องเซ็น (netVat/netBefore) |

## Archetype Surface (Phase 0c · Pattern Q) — ครบ

- **List/Wizard/View/PDF/Modals** ครบเหมือนรอบก่อน · **Wizard step 4 เอกสารแนบ = real `<input type="file">`** (renderStep4 ln 1073-1078 · `pickAttachments`/`triggerAttachPick`/`fmtFileSize` · mockUpload ถอดแล้ว) — ยังเป็น surface เดียวกัน ไม่กระทบ business coverage · **step 3 line rule** ครบ + การ์ด end-bill (FN-19)

## Negatives / Scope Guard — enforce ครบ 4/4

| รายการ | สถานะ | Evidence |
|---|---|---|
| ① ลดหนี้ไม่อ้างใบ (OQ-DN-01) | ✅ disabled tile | step1 tile 2 `not-allowed`+toast · ไม่มี handler สร้าง DN ลอย |
| ② เรียกเงินคืน (S-15/OQ-DN-03) | ✅ absent | grep `refund`/`เรียกเงินคืน` = 0 |
| ③ ยกเลิก DN หลังอนุมัติ (S-16/OQ-DN-04) | ✅ block | `openCancelDN` double-guard draft/pending เท่านั้น |
| ④ หน้าจอ RTV จริง (W3-LITE mock) | ✅ mock lookup | `RTVS` + `pickRTV` เท่านั้น · ไม่มี RTV CRUD/route |

## ✅ Governance doc-lag — RESOLVED 2026-09-23 (pack reconciled to 22 FN)

| รายการ | สถานะ | หลักฐาน |
|---|---|---|
| **FN-19 ส่วนลดท้ายบิล** | **RESOLVED เต็มรูป** — user KEEP + มี BR-cap (net≥0/≤คงค้าง) + VAT ม.86/10 + hard-warn + submit guard + DOA tier post-end-bill + **e2e ครอบแล้ว (FN 22/22 · 34/34)** · **pack docs ตรงแล้ว** | `FUNCTION_CHECKLIST` +FN-19 (trace S-05·S-14·BR-11,12·[มติ 2026-09-23]) · `PREBRIEF` +BR-11/BR-12 (§4) +§3.3 computed +allow-list #67.1 ④ +coverage matrix S-14→FN-18,19 · extractor ยืนยัน **22 FN parsed · BR-11/12 present · FN-19 keyword-hit 0.67 ใน HTML** |
| legal-basis ภาษีซื้อฝั่งซื้อ (input-VAT reduction ม.86/10) | **OQ — carry step 12** | แท็ก `[มติ 2026-09-23 · legal basis ฝั่งซื้อรอ BA รับรอง]` ใน BR-12 · เป็น [ASSUMED mirror ของ CN] → BA รับรองอย่างเป็นทางการก่อน dev ตั้งค่าจริง |

> `couponAmt` ใน `totals()` (kernel) = dormant (ไม่มี UI ผูก) → ไม่ actionable · ไม่นับ scope creep (เหมือนรอบก่อน)

## Gap list (เรียงตามความเสี่ยง)

1. gap ระดับ BLOCK: **0** · gap ระดับ WARN: **0**
2. FN (24/24 incl. FN-19/20/21) / S (16/16) / BR (14/14 incl. BR-11..14) / declaration (5/5) / negatives (4/4): **ครบทั้งหมด · ไม่มี regression · pack ↔ HTML ↔ e2e (36/36) ตรงกัน**
3. anchors (FIX-03) grep ครบ: ENG-DOC-NUM=1 · CSQ=3 · NTF:=2 · F080=1 · F095=1 · F093=3 · ม.82/10=3 · ม.86/10=4
4. เหลือเฉพาะ OQ ให้ BA รับรอง (ไม่บล็อก · carry step 12): legal-basis ภาษีซื้อ (OQ-DN-05) · OQ-DN-06 (flow เครดิต) · OQ-DN-07 (CSQ profile)

## Diff vs รอบก่อน (BA FIX 2026-09-23)
- **FIX-01 เครดิตคงเหลือ:** เพดาน `dnRoom` (ไม่หัก paid) · ใบจ่ายครบออก DN ได้ · แยก applyToAp/vendorCredit · card+section → **FN-04 กลับด้าน + FN-20/BR-13 ใหม่** (e2e E20)
- **FIX-02 ภาษีซื้อ vendorCn:** 2 สถานะ (รอเอกสาร / เดือนภาษี=วันที่ได้รับ ม.82/10) · ปุ่ม `openVendorCn` · ตัด [ASSUMED] visible → **FN-21/BR-14 ใหม่** (e2e E21)
- **FIX-03 anchors** (comment) · **FIX-04 demo-only** ครอบ "template ตาม thai-doc-pdf-generator"
- **regression:** ไม่มี (e2e เดิม 34 เคสยังผ่าน + เพิ่ม E20/E21 = 36/36)

## ⬜ NOT-CHECKED (รอบ 2)
- FRD Pack (05_RULES BR ↔ FRD · ต้องรวม BR-11..14) + testcases-*.md (FN↔TC ledger รวม FN-19/20/21 · R15) = รอบ 2
- Declaration ↔ FRD sync read = รอบ 2

---
**สรุป:** VERDICT = **PASS · BLOCK = 0 · WARN = 0** · FN **24/24** (incl. FN-19/20/21 · ทุกตัว hook จริง + e2e 36/36) · Scenario 16/16 · BR **14/14** (incl. BR-11..14) · Declaration **5/5** (chip=detect · **ไม่มี DIVERGENCE**) · Negatives 4/4 · anchors ครบ (FIX-03) · **BA FIX-01/02/03/04 = แก้ครบ** · เหลือเฉพาะ OQ legal-basis + OQ-DN-06/07 → carry step 12
