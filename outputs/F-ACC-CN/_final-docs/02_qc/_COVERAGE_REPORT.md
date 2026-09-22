# _COVERAGE_REPORT (Round 1 · HTML) — F-ACC-CN ใบลดหนี้ลูกค้า

| | |
|---|---|
| Contract | `PREBRIEF_F-ACC-CN.md` + `FUNCTION_CHECKLIST_F-ACC-CN.md` (**22 FN** — BA เพิ่ม FN-19 ส่วนลดท้ายบิล 2026-09-22) · DECLARATION_INDEX (doa/ntf/csq/doccfg + contract chain) |
| HTML | `outputs/F-ACC-CN/F-ACC-CN_credit-note.html` (ไม่แตะรอบนี้ — end-bill implement อยู่แล้ว) |
| รอบ | **R1 re-gate หลัง BA formalize FN-19** (จาก governance flag เดิม → FN ทางการใน contract) — sync coverage denominator 21→22 |
| Evidence ร่วม | e2e `outputs/F-ACC-CN/_e2e/e2e-cn.py` — **33/33 PASS · FN ครอบ 22/22** (render-assert · console errors=0 · E18b-EB-VAT + E09b-EB-CAP tag FN-19) · qc-ux ไม่รันรอบนี้ (HTML ไม่แตะ) |
| **Verdict** | 🟢 **PASS · FN 22/22 · Declaration 5/5 · BLOCK = 0** · FN-19 (end-bill) = BA-approved + hook ครบใน HTML + e2e ครอบ · governance flag เดิม **ปิดแล้ว** (contract สะท้อน FN-19) |

> **สาระรอบนี้:** BA เคาะ **FN-19 ส่วนลดท้ายบิล (฿/%)** เข้า `FUNCTION_CHECKLIST` (หมวด 2) + `PREBRIEF` (BR-11 cap · BR-12 VAT ม.86/10 · §3.3) → นับ FN 21→22. HTML **implement end-bill อยู่แล้ว** (การ์ด step 3 + `totals()` cap/VAT recompute) จากรอบก่อน — รอบนี้จึงเป็น **sync coverage เท่านั้น** (denominator 21→22 · FN-19 hook = การ์ด toggle/totals ที่มีอยู่) · **ไม่แตะ HTML · ไม่แตะ handler ของ FN อื่น** → FN 22/22 ครบ

## FN Coverage Matrix (22/22 ✓ — evidence = HTML hook + e2e case)

| FN | ความสามารถ | HTML evidence | e2e |
|---|---|---|---|
| FN-01 | เลือกใบคงค้าง เห็นสุทธิ/ลดแล้ว/คงค้าง | `invList()` + `INV_COLS` · `pickInv` | E01 ✓ |
| FN-02 | tile "ลดหนี้ไม่อ้างใบ" ปิดไว้ (S-12) | tile `not-allowed` onclick=`showToast('…ปิดไว้')` — ไม่ผูก setSource | E02 ✓ |
| FN-03 | เลือกใบ→ลูกค้า/ที่อยู่/เลขภาษี/บรรทัด | `pickInv`→`buildLinesFromInv` · pdf taxId/branch | E03 ✓ |
| FN-04 | ใบ void/ชำระครบ ไม่โผล่ (S-13) | `invList()` filter `status!=='void' && invOutstanding>0.005` | E04 ✓ |
| FN-05 | RET ต้องเลือกใบรับคืน · จำนวนจาก SR | RET `needSR:true` · `pickSR` cap | E05 ✓ |
| FN-06 | DISC ปรับราคา ≤ ราคาเดิม | DISC `mode:'price'` · line price-mode validate | E06 ✓ |
| FN-07 | ลดเฉพาะบรรทัดที่เลือก · ลบ/เพิ่มกลับ | `removeLine`/`readdLine` | E07 ✓ |
| FN-08 | ลดหลายรอบ: เดิม/ลดแล้ว/ลดได้อีก | `cnApplied` · `invAvailable` · meta (SR-capped display) | E08 · E05b/E08b ✓ |
| FN-09 | ยอด/จำนวนเกิน→บล็อก+hard-warn · + end-bill เกินเพดาน (Rule 1/BR-11) | `submitGuard`/`blockReason` (grand>avail + `t.ebOver`) · `lineSummaryWarn` (cnOver + end-bill hard-warn) | E09 · E09b ✓ |
| FN-10 | คำอธิบาย ≥10 ตัว | `submitGuard` `reasonText.length<10` | E10 ✓ |
| **FN-19** | **ส่วนลดท้ายบิล (฿/%) เปิด/ปิดได้ · จำกัด net≥0 & ≤คงค้าง · ลด VAT ตาม ม.86/10 (ภ.พ.30/JE/PDF ลดตาม)** | **การ์ด `ebCard` step 3 (`step3Block` ~ln 632): toggle `endbill.enabled` + segmented `mode='amount'`/`'percent'` + input `endbill.value` + hint "ลดได้สูงสุด ฿X"** · **`totals()` (ln 726–734): `ebCap=max(0,after−coupon)` · `ebOver` · `ebAmt=min(ebRaw,ebCap)` · `grand=max(0,after−ebAmt−cp)` (net≥0) · `netBefore`/`netVat` (VAT ม.86/10 คิดใหม่)** · **block: `blockReason`/`submitGuard` `t.ebOver`** | **E18b-EB-VAT · E09b-EB-CAP ✓** |
| FN-11 | ส่งอนุมัติ สายตามมูลค่า · เลือกคนครบ | `resolveDoa` (อ่าน `totals().grand` ≥0 เสมอหลัง clamp) · `.slot-row` · `confirmSubmit` | E11 · C4 ✓ |
| FN-12 | อนุมัติครบ→เลข CN-ปี-ลำดับ | `onFinalApprove`→`nextCode()` (audit "ลดภาษีขาย ฿netVat") | E12 ✓ |
| FN-13 | ไม่อนุมัติต้องเหตุผล→ร่าง+รอบก่อน | `openRejectModal` · `approval_history` | E13 ✓ |
| FN-14 | SoD ผู้ส่งไม่เห็นปุ่มอนุมัติเอง | `canActStep` · `viewActions` | E14 ✓ |
| FN-17 | re-check คงค้างขั้นสุดท้าย → อนุมัติไม่ได้ | `approveGuard(s,isLast)` | E17 ✓ |
| FN-15 | ยกเลิกร่าง/รออนุมัติ+เหตุผล | `openCancelCN` guard | E15 · C1 ✓ |
| FN-16 | ส่งลูกค้า→sent+snapshot | `openSendCN` (approved→sent) | E16 · C2 ✓ |
| FN-18 | tab ใบอ้างอิง: คงค้างก่อน/หลัง+ภ.พ.30+JE · VAT ลดใหม่ (Rule 2) | `renderRefTab` — ฐานภาษีที่ลด=`netBefore` · ภาษีขายที่ลด=`netVat` · JE 2150=`netVat` (บาลานซ์ netBefore+netVat=grand) | E18 · E18b ✓ |
| FN-90 | ค้นหา/กรอง+empty state | `filterSelects` · `filterFn` · empty-state | E90 ✓ |
| FN-91 | ประวัติ append-only | `pushAudit` (unshift only) | E91 ✓ |
| FN-92 | PDF อ้างใบเดิม/มูลค่า/ผลต่าง/เหตุ ค.ศ. | `pdfParts` (refHtml · ภาษี=`netVat`) | E92 ✓ |

## ⭐ FN-19 · ส่วนลดท้ายบิล (end-bill) — hook ครบ (BR-11 cap + BR-12 VAT ม.86/10)

| | |
|---|---|
| สถานะ HTML | ✅ PRESENT — การ์ด `ebCard` ใน `step3Block` (~ln 632): toggle เปิด/ปิด (`endbill.enabled`) + segmented ฿/% (`mode='amount'`/`'percent'`) + input value bound `createWizard.data.endbill` · default off |
| **BR-11 (cap · net≥0 & ≤คงค้าง)** | `totals()` (ln 726–734): `ebCap = max(0, after − coupon)` · `ebOver = ebRaw > ebCap` · `ebAmt = min(ebRaw, ebCap)` → **`grand = max(0, after − ebAmt − cp)` ≥ 0 เสมอ** (clamp) + hard-warn (`lineSummaryWarn`) + block submit (`blockReason`/`submitGuard` `t.ebOver` "สูงสุด ฿ebCap") + hint "ลดได้สูงสุด ฿X" ใต้ input · คงค้างคุมโดย `cnOver` เดิม (end-bill ลด grand → ปลอดภัยฝั่ง block) |
| **BR-12 (VAT ม.86/10)** | `totals()`: แบ่งส่วนลดตามสัดส่วน VAT-inclusive (`ebVat = ebAmt·vat/after` · `ebBase = ebAmt−ebVat`) → `netBefore`/`netVat` (VAT คิดใหม่จากฐานที่ลด) · ทุกจุด "ภาษีขายที่ลด" (ภ.พ.30 · JE · PDF · list stat/row · csv · submit modal · detail) ใช้ `netVat` · **ตัวเลขจริง (INV-2026-0141): 10% → ฐาน 360,000→324,000 · VAT 25,200→22,680 · grand 346,680** (e2e E18b ยืนยัน) |
| ขอบเขต | **CN-level totals adjustment เท่านั้น** — per-line B2 v2 engine (`calcLineVat`/`migrateLine`) **ไม่แตะ** (verbatim · e2e ยืนยัน line-VAT gross คง 25,200) |
| ✅ Governance (ปิดแล้ว) | รอบก่อนขึ้น flag "BA ต้องอัปเดต PREBRIEF/FUNCTION_CHECKLIST ให้มี FN end-bill ทางการ" — **BA เคาะแล้ว 2026-09-22**: FN-19 อยู่ใน FUNCTION_CHECKLIST (หมวด 2 · S-14 · BR-11,BR-12) + PREBRIEF (BR-11/BR-12/§3.3) → contract สะท้อน · coverage denominator sync 21→22 |
| OQ-b (ยังเปิด) | end-bill ลด grand → **ลดชั้น tier DOA** — พฤติกรรมถูกต้อง (resolveDoa อ่าน grand) แต่ BA ควรยืนยันว่า "ลดส่วนลดท้ายบิลแล้วลดชั้นอนุมัติ" เป็นที่ต้องการ (ส่งต่อ R2/BA) |

## Declaration Coverage (Phase 0b) — 5/5 · chip=detect · DIVERGENCE = ไม่มี

`declarations` = {doa,ntf,csq,doccfg} = true = chip (F096) ทุกท่อ · anchor ครบ · **การเพิ่ม FN-19 ไม่แตะ declaration/anchor**

| ท่อ | chip=detect | brief (`5_DECLARATIONS/`) | HTML anchor |
|---|---|---|---|
| DOA | ✓/✓ | `DOA_BRIEF_F-ACC-CN.md` ✓ | `resolveDoa` 3-tier mock · `.slot-row` เลือกคน · ไม่ hardcode chain |
| NTF | ✓/✓ | `NTF_BRIEF_F-ACC-CN.md` ✓ | `// NTF: cn.issued/sent` · doa_pending/result จาก DOA engine |
| CSQ | ✓/✓ | `CSQ_BRIEF_F-ACC-CN.md` ✓ | `// CSQ: cn.issued → AC` + audit "7C" · DC จาก DOA engine |
| DOCCFG | ✓/✓ | `DOCCFG_BRIEF_F-ACC-CN.md` ✓ | `ENG-DOC-NUM.next()` · `nextCode` mock · ไม่ hardcode รูปแบบเลข |
| CONTRACT | — | (plan) | `F090→F096 · F096→F094 (ar_open_item) · JE→F093` |

## Archetype Surface (Phase 0c · Pattern Q) — ครบ

- **List**: statusMap/filterSelects ครบทุกสถานะ + docPill + กรอง reason/cust · stat "ภาษีขายที่ลดเดือนนี้" = `netVat`
- **Wizard**: step1 source → step2 field → step3 line (qty/price mode · block) + **การ์ดส่วนลดท้ายบิล FN-19 (toggle ฿/% · cap · VAT)** → review
- **View**: `viewActions` ครบทุกสถานะ · tab ลายเซ็น=DOA chain · ประวัติ=audit · ใบอ้างอิง=refTab (ภ.พ.30+JE `netVat`)
- **PDF**: `pdfParts` — ผู้เสียภาษี/สาขา · อ้างใบเดิม/มูลค่า/ผลต่าง · แถว ลดฐาน→มูลค่าหลังหักส่วนลด→VAT(ลดแล้ว) · 3 ช่องเซ็น
- **Modals**: reason modal ครบ (cancel · reject)

## Negatives / Scope Guard — enforce ครบ

| รายการ | สถานะ | Evidence |
|---|---|---|
| ลดหนี้ไม่อ้างใบ (standalone CN) (FN-02 · OQ-CN-01) | ✅ absent | tile ปิด onclick=toast · ไม่มี handler สร้าง CN ลอย |
| S-15 คืนเงิน (refund) | ✅ absent | grep `refund`/`คืนเงิน` = 0 · e2e N-REFUND |
| S-16 ยกเลิก CN หลังอนุมัติ | ✅ block | `openCancelCN` double-guard (FIX-01) · e2e N-CANCEL-APPROVED · C1 |
| หน้าจอรับคืนสินค้าจริง (SR) | ✅ mock lookup | `pickSR` เท่านั้น · ไม่มี CRUD SR · e2e N-SR-CRUD |
| end-bill grand ติดลบ (FN-19 · BR-11) | ✅ ป้องกัน | `grand = Math.max(0, after−ebAmt−cp)` + clamp `ebAmt≤ebCap` + block submit · e2e E09b (99,999,999 + 999% → grand=0) |

## Status-guard hardening (FIX-01/02/03) — คงเดิม (การเพิ่ม FN-19 ไม่แตะ)
cancel `['draft','pending_approval']` [FIX-01] · send `approved||sent` [FIX-02] · submit `status!=='draft'` [FIX-03] — e2e C1/C2/C4 PASS

## delta เทียบ R1 ก่อน
- **เปลี่ยน**: end-bill governance flag "รอ BA ทำ FN ทางการ" → **FN-19 เข้า contract แล้ว** (FUNCTION_CHECKLIST หมวด 2 · PREBRIEF BR-11/BR-12/§3.3) · coverage denominator **21→22** · e2e ครอบ FN-19 (E18b-EB-VAT + E09b-EB-CAP tag FN-19) · e2e "FN ครอบ 21/21" → **"22/22"**
- **คงเดิม**: HTML ไม่แตะ (end-bill implement อยู่แล้ว) · handler FN อื่น · Declaration 5/5 · FIX-01..03 · negatives อื่น · per-line VAT engine verbatim
- **ค้าง**: 0 gap (block) · OQ-b (tier DOA ลดตาม end-bill) = ส่งต่อ BA

## OQ ค้าง (ส่งต่อ BA)
OQ-CN-01..04 (เดิม) · **OQ-b end-bill**: end-bill ลด grand → ลด tier DOA เป็นที่ต้องการ? (พฤติกรรม FN-19 a+c เคาะแล้ว · tier interaction ยังเปิด)

## ⬜ NOT-CHECKED
- FRD Pack + testcases = รอบ 2 (R1 = HTML เท่านั้น) · FN-19 ↔ FRD/TC ผูกที่ R2 (FRD 05_RULES BR-11/BR-12 + TC end-bill)
