# _COVERAGE_REPORT — F-HR-WELFARE · สวัสดิการ (Welfare)

- **WF-01 Step:** 4 (round 1 — HTML vs business contract · "ทำครบมั้ย") · **RE-RUN / re-gate (C3.2)** หลังเพิ่ม reversal (กลับรายการ) + exposure display จาก OQ resolution (PM/BA delegated)
- **Skill:** qc-coverage-checker (round 1 = HTML vs contract)
- **Target:** `outputs/F-HR-WELFARE/welfare.html` (3,268 บรรทัด · single-file SPA · master + light transaction)
- **Contract:**
  - `Pack Brief Feature/F-HR-WELFARE/0_DIRECTION/PREBRIEF.md` (S-01..S-16 · BR-01..BR-10 · §5 state machine · matrix §11 · §12 declaration signals)
  - `Pack Brief Feature/F-HR-WELFARE/0_DIRECTION/FUNCTION_CHECKLIST.html` (24 FN = FN-01..19 + FN-90..94 · `unsupported[]` 5)
  - `outputs/F-HR-WELFARE/_DECISION_LOG_OQ.md` (OQ-WEL-01..03 + A-WEL-03 + declaration additions — AUTHORIZED, delegated by PM/BA 2026-09-08)
  - Declarations = doa + ntf + csq (`Pack Brief Feature/F-HR-WELFARE/5_DECLARATIONS/{DOA,NTF,CSQ}_BRIEF.md` มีจริง · `NOT_NEEDED.md` = doccfg/pdfdoc)
- **Date:** 2026-09-08
- **Checklist จาก contract:** FN 24 · scenarios (S-XX) 16 · BR 10 · declarations 3 (+1 N/A) · unsupported (scope guard) 5

## VERDICT: **PASS** 🟢
สรุป: FN ครอบ **24/24** · scenarios **16/16** · declarations **3/3** (+DOCCFG N/A) · unsupported 5 ยัง absent · gap block 0 · gap warn 0 · NOT-CHECKED 0
> Authorized scope addition (per `_DECISION_LOG_OQ.md`): reversal (`reversed` state) + pending-exposure display. **ไม่ใช่ scope creep** — เป็นการปิด OQ-WEL-01/03 ที่ PM/BA มอบหมาย. ขยาย §5 state machine ด้วย `reversed` (approved→reversed) แบบ append-only.

---

## Coverage Matrix (FN × WF)

| FN | ประเภท | WF | Evidence ใน welfare.html |
|---|---|:--:|---|
| FN-01 สร้างประเภทสวัสดิการ + กลุ่ม/โควตา/effective | S-01·BR-03 | ✓ | `renderRegistry` + benefit form modal (L2660–2690: ชื่อ/หน่วยนับ/quota/groups/effFrom) → `doSaveBenefit` (L3056+) |
| FN-02 แก้ = ออกเวอร์ชันใหม่ ไม่ทับ [STD] | S-02·BR-03 | ✓ | L3056–3059: active เดิม→archived + `effTo=benDayBefore(fm.effFrom)`; verRows table (L2710) |
| FN-03 ปิดใช้ (soft archive) ไม่ hard delete | S-03·BR-07 | ✓ | `doArchiveBenefit` (L3089) status=archived; row action power-off (L2407) |
| FN-04 quota≤0 / ช่วง effective ทับ → บล็อก+เหตุ | S-04·BR-03 | ✓ | validate `err.quota` + overlap check L3022–3029 ("ช่วงมีผลทับกันไม่ได้") |
| FN-05 เพิ่มผู้ติดตาม (rel/dob/eligible) | S-05·BR-10 | ✓ | `submitDependent` L3199–3209; sub-list ใน balance tab (L2575) |
| FN-06 ผู้ติดตามเกิน/อายุบุตรเกิน → เตือน/บล็อก | S-06·BR-01 | ✓ | บุตร age>20 บล็อก L3204; depCount≥3 warn note L2887 |
| FN-07 สร้างคำขอ เลือก type "มีสิทธิ์ ณ วันยื่น" + self/dep + แนบไฟล์ | S-07·BR-01 | ✓ | reqType combobox "เฉพาะที่มีสิทธิ์ ณ วันยื่น" L2736; useFor self/dependent; files; `submitRequestForm` L3107 |
| FN-08 ส่งอนุมัติผ่าน DOA slot picker (เลือกคน · ไม่ hardcode) | S-07·BR-04 | ✓ | `modalDoa` L2990–3005 slot picker 2 ขั้น (avatar+ตำแหน่ง+ชื่อ) + note "GET /doa/resolve"; `confirmDoa` L3124 |
| FN-09 ใช้บางส่วน — คงเหลือถูกต้อง ใช้ต่อได้ | S-08·BR-02 | ✓ | `usedByPerson`/`remaining` (L2266) นับเฉพาะ approved; balance table L2853–2855 |
| FN-10 ขอเกินคงเหลือ → บล็อก + แสดงยอด | S-09·BR-02 | ✓ | `validateRequest` L3104 `want>rem`; reqEligNote "เกินคงเหลือ: คงเหลือ …" L2767 |
| FN-11 ยื่น type ไม่มีสิทธิ์ (นอกกลุ่ม/ช่วง/พ้นสภาพ) → บล็อก+เหตุ | S-10·BR-01,06 | ✓ | `eligibility()` L2275–2279 (group/leaver) + L3102 block reason |
| FN-12 ดูสถานะ + สาย DOA ปัจจุบัน (อ่าน) | S-07 | ✓ | view drawer DOA timeline L2822–2830 "สายอนุมัติ (จาก DOA กลาง)" |
| FN-13 อนุมัติ → ตัดคงเหลือ + 7C EC + ส่งสถานะจ่าย (hook) | S-07·BR-05,09 | ✓ | `doApprove` isLast L3154–3157 (status=approved · pay=pending · EC stamp); history "ตัดคงเหลือ + บันทึกมูลค่าเข้า 7C EC + ส่งสถานะจ่าย" L2869 |
| FN-14 ไม่อนุมัติ → ไม่ตัดคงเหลือ + เหตุ + แจ้งผู้ยื่น | S-11·BR-05 | ✓ | `doReject` L3166–3173 (reason required · toast "แจ้งเตือนผู้ยื่น") |
| FN-15 ยกเลิกคำขอก่อนอนุมัติ ไม่กระทบคงเหลือ | S-12·BR-05 | ✓ | `doCancelRequest` L3191–3195 status guard `['draft','pending']` |
| FN-16 leaver → คำขอค้างระงับ + คงเหลือหยุด (revoked) · null≠ทำงาน | S-13·BR-06 | ✓ | seed REQ revoked L2217; balance leaver note L2519; `eligibility` emp.ended block L2278 |
| FN-17 สถานะจ่าย = อ่าน Payroll/Expense display-only | S-14·BR-10 | ✓ | `payPill` L2295; view "อ่านจาก Payroll/Expense · display-only · Welfare ไม่จ่ายเอง" L2835 |
| FN-18 joiner → เข้ากลุ่ม → สิทธิ์เปิดอัตโนมัติ [STD] | S-15·BR-06 | ✓ | EMP-006 joiner L2180; joinerNote "สิทธิ์เปิดอัตโนมัติ ตาม joiner signal" L2537 |
| FN-19 รายงานใช้สิทธิ์ ตามแผน/กลุ่ม/ช่วง + filter จริง | S-16·BR-08 | ✓ | `renderReport` L2583–2631: filter type/group/from/to ทำงานจริง + agg + empty state |
| FN-90 ค้นหา/filter + empty state | กลาง | ✓ | `searchSelectHTML`; statusOpts filter (L2389,2437); `emptyStateHTML` (report/balance) |
| FN-91 ปิดใช้/ยกเลิกผ่าน confirm + soft archive | กลาง | ✓ | confirm modals `archiveBenefit`/`cancel` (L2925+, L2935); doArchive soft |
| FN-92 field บังคับ validate + กัน double-submit | กลาง | ✓ | `validateRequest`/`validateBenefit`; `lockBtn` is-disabled (L3214) ทุก action |
| FN-93 audit append-only ทุก create/แก้/อนุมัติ/ยกเลิก | กลาง | ✓ | history timeline `histTab` L2860–2876 (approve/reject/cancel/revoke/reverse ต่อท้าย) |
| FN-94 ปิดบัง RESTRICTED (บุคคล/ผู้ติดตาม/มูลค่า) ตาม role | BR-08 | ✓ | `canSeeValue()`/`canSeePerson()`/`maskEl` (L2616,2815,2852) → '•••' |

**FN ครอบ 24/24 · ทุกข้อ ✓ (WF ติ๊กได้)** — ไม่มี △ partial, ไม่มี ✗, ไม่มี dead button.

## Scenario Coverage (S-01..S-16)

ทุก scenario เดินได้ครบใน UI ผ่าน FN ที่ trace ไว้ (matrix §11): S-01→FN-01 · S-02→FN-02 · S-03→FN-03 · S-04→FN-04 · S-05→FN-05 · S-06→FN-06 · S-07→FN-07/08/12/13 · S-08→FN-09 · S-09→FN-10 · S-10→FN-11 · S-11→FN-14 · S-12→FN-15 · S-13→FN-16 · S-14→FN-17 · S-15→FN-18 · S-16→FN-19. **16/16 ✓** ทุก BR-01..10 ปรากฏใน ≥1 scenario · ทุก transition ใน §5 มีผู้กด.

## Declaration Coverage (Phase 0b)

| ท่อ | เข้าเงื่อนไข | brief | HTML evidence | WF |
|---|---|---|---|:--:|
| DOA | S-07 ส่งอนุมัติ · ไม่มีวงเงิน 2 ขั้น | `5_DECLARATIONS/DOA_BRIEF.md` ✓ | slot picker เลือกคน (L2990) · `DOA_SLOTS` 2 ขั้น หัวหน้า→HR (L2242) · ไม่ hardcode chain | ✓ |
| NTF | S-07 ยื่น · S-11 ผล · ใกล้เต็มโควตา · S-13 สิ้นสุด | `5_DECLARATIONS/NTF_BRIEF.md` ✓ | toast/note "แจ้งเตือนผู้ยื่น" (L3132,3173,3188) · near-quota note (L2858) · wording ทั่วไป ไม่มี raw event id (#81) | ✓ |
| CSQ | BR-09 มูลค่าอนุมัติ = ผลได้ → EC | `5_DECLARATIONS/CSQ_BRIEF.md` ✓ | "บันทึกมูลค่าเข้า 7C · EC" (L2616,2834,2957) · ท่อ EC เท่านั้น (ไม่มี OC/DC/SC) | ✓ |
| DOCCFG | ไม่มีเลขรัน/เอกสารทางการ | `NOT_NEEDED.md` (N/A) | request_no = internal display id ('REQ-2569-'+seq) ไม่ใช่เลขรันทางการ (PREBRIEF §3.1) · ไม่มี PDF/doc wizard | N/A |

> **หมายเหตุ script false-positive:** `prebrief_checklist.py` ตรวจ `doccfg=true` จาก keyword "snapshot/สำเนา" — เป็น false positive. PREBRIEF §12 chip = DOCCFG `—` (no) · request_no เป็น id ภายในโดยเจตนา ไม่ใช่ doccfg. **ไม่ใช่ DIVERGENCE** (chip = detect หลังหักลบ false-positive). Declarations ที่ต้องมีจริง = 3 → มีครบ 3.

## Reversal (กลับรายการ) — AUTHORIZED ADDITION (OQ-WEL-01)

ตรวจตามที่ decision log ประกาศ — **ปิดครบทุกเงื่อนไข**:

| เกณฑ์ | ✓ | Evidence |
|---|:--:|---|
| append-only (คงข้อมูลเดิม เพิ่มเฉพาะสถานะ+เหตุ+เวลา) | ✓ | `doReverse` L3185 `r.status='reversed'; r.reverseReason; r.reversedAt` — ไม่ลบ/ไม่แก้ของเดิม; history เก็บทั้งบรรทัดอนุมัติเดิม + บรรทัดกลับรายการ (L2869–2872) |
| admin-guarded | ✓ | L3176 `if(!canApprove())` guard สิทธิ์; ปุ่ม "กลับรายการ" โผล่เฉพาะ `status==='approved' && canApprove()` (L2793) |
| status guard (approved เท่านั้น) | ✓ | L3178 `if(!r || r.status!=='approved') return` |
| reason บังคับ (mirror doReject) | ✓ | L3180 reason required + error banner |
| balance-restoring (คืนคงเหลืออัตโนมัติ) | ✓ | `usedByPerson` นับเฉพาะ `approved` (L2266) → เปลี่ยนเป็น `reversed` = ลดยอดใช้เอง ไม่ปรับซ้ำ |
| EC reverse (คืนมูลค่าเข้าเงินได้ 7C·EC) | ✓ | history "กลับรายการ · คืนมูลค่าเข้าเงินได้ (7C · EC)" (L2871) · view banner (L2812) |
| payroll clawback = display-only (ไม่จ่ายจริง) | ✓ | L3186 `if(wasSent) r.payrollClawback=true` → flag เท่านั้น; note "แจ้ง Payroll ตั้งเบิกคืน (display-only · Welfare ไม่จ่ายเอง)" (L2872,2982) |
| new state `reversed` เข้า state machine/filter/pill | ✓ | reqPill `reversed` (L2290) · statusOpts filter (L2437) · pill "กลับรายการแล้ว" |
| แยกจาก cancel (FIX-05) — ไม่ทับ | ✓ | cancel = draft/pending เท่านั้น (L3194) · reverse = approved เท่านั้น สองขอบเขตแยกกัน |

**ไม่ reintroduce "real payout":** reversal ไม่มี pay action — ยังคง display-only hook ไป Payroll/Expense เหมือนเดิม; clawback เป็นเพียง flag แจ้งปลายทาง (F065) ไม่จำลองจอ payroll. ✅

## Exposure display (OQ-WEL-03) — AUTHORIZED ADDITION

`reqBalanceTab` เพิ่มบรรทัด "คำขอรออนุมัติอื่นของสิทธิ์นี้: N ใบ · รวม {amount}" (L2847–2851) — คำนวณจาก `REQUESTS.filter(empId & benefitId & status==='pending' & id!==r.id)` · **display-only** ไม่แตะ hard re-check ที่อนุมัติ (FIX-02 คงอยู่ `doApprove` L2142–2148 ยัง re-check eligibility+เพดาน). ✅ ไม่สร้าง soft-reserve/lock.

## Negative / Scope-Guard note

Feature นี้เป็น **master + light transaction (ไม่ใช่ Pattern Q)** → ไม่มี `FN-40` (negative doc-archetype case). Scope guard ที่ต้องตรวจ = `unsupported[]` 5 ข้อ — **ยัง absent ครบทุกตัว** (grep ยืนยัน ไม่โผล่ใน HTML):
1. จ่ายเงินจริง/เบิก/หักผ่านเงินเดือน → พบเฉพาะ "**ไม่**จ่ายเงินเอง" + hook display-only · ไม่มีปุ่ม/action จ่ายจริง ✓ absent
2. จัดการผู้ให้บริการ (โรงพยาบาล/ประกัน) → ไม่มี ✓
3. สวัสดิการยืดหยุ่น/แต้ม (flex credits) → ไม่มี ✓
4. สร้าง/แก้ค่านโยบาย HR กลาง → อ่านอย่างเดียว ไม่มี CRUD config ✓
5. ออกเอกสารเลขรัน/PDF ทางการ → ไม่มี running-number/PDF (self_audit tail L3264 ยืนยัน "no running-no/PDF/doc-wizard") ✓

## ⬜ NOT-CHECKED
— ไม่มี (round 1 = HTML เท่านั้น; rules ฝั่ง FRD/TC จะตรวจรอบ 2)

## Diff จากรอบก่อน (re-gate FIX-01..09 · PASS)
- **ปิดแล้ว/ยังคง:** FN 24/24 · declarations 3/3 · unsupported 5 absent — ทุกอย่างยังครบ ไม่มีอะไรหาย
- **ใหม่ (authorized):** เพิ่ม state `reversed` + `doReverse`/`modalReverse` (OQ-WEL-01) · exposure note ใน balance tab (OQ-WEL-03) — ทั้งคู่มี hook จริง เดินได้ครบ 3 ชั้น
- **ไม่มี gap ใหม่ · ไม่มี scope creep**

## 🚩 Flag ส่งต่อ step 7 (declaration skills — ไม่กระทบ verdict รอบนี้)
reversal เพิ่ม event ที่ต้อง **append** ตอน step 7 (ตาม `_DECISION_LOG_OQ.md`):
- **CSQ:** event `EC-reverse` (negative offsetting entry) คู่กับ EC-forward → append `CSQ_BRIEF.md`
- **NTF:** event `ntf-reversed` (แจ้งพนักงานคำขอถูกกลับรายการ) → append `NTF_BRIEF.md`
- Payroll clawback = display-only flag ปลายทาง F065 (ไม่ใช่ event ของ F102)
> รอบนี้ **ไม่แก้** 5_DECLARATIONS (round 1 = HTML) — brief 3 ใบยังมีครบ = ผ่าน 0b. การ append เป็นงาน step 7.

---
_ตรวจโดย: qc-coverage-checker (round 1) · 2026-09-08 · evidence จาก welfare.html (3,268 บรรทัด) + `_DECISION_LOG_OQ.md` + 5_DECLARATIONS/*_
