# Coverage Report — F-HR-EXPENSE (F101) · รอบ 1: HTML

- วันที่: 2026-09-10 · Feature: Expense Claim — เบิกค่าใช้จ่าย · archetype: Q-document
- Artifact ที่ตรวจ: `outputs/F-HR-EXPENSE/expense.html` (2512 บรรทัด)
- Contract: `Pack Brief Feature/F-HR-EXPENSE/0_DIRECTION/PREBRIEF.md` + `FUNCTION_CHECKLIST.html`
- Checklist จาก contract: **FN 22 ข้อ** (FN-01..17 ธุรกิจ 17 + FN-90..94 กลาง 5) · **S-01..S-15** (15 scenarios) · BR-01..BR-10 · unsupported 7 · declaration 4 ท่อ (DOA/NTF/CSQ/DOCCFG chip ✓)

## Verdict: 🟢 PASS (รอบ 1 · HTML)
สรุป: FN ครอบ **22/22** · S-scenario ครอบ **15/15** · block gap 0 · WARN 2 (scope-note ของเพิ่มที่เคาะแล้ว + hook display-only เสริม) · NOT-CHECKED: declaration briefs (สร้างหลัง step 7 — ตรวจรอบ 2)

> ของที่เพิ่มเกิน 22 FN (touchpoint ใหม่ 2026-09-10) = **PM/BA-approved additions รอ FN assignment ใน BRD** — บันทึกเป็น note ไม่ใช่ BLOCK ตามคำสั่งงาน

---

## Coverage Matrix — FN (22/22)

| FN | grp | ต้องทำอะไรได้ | HTML | Evidence (route/selector/handler) |
|---|---|---|:--:|---|
| FN-01 | g1 | wizard 5 ขั้น | ✓ | `STEP_KEYS` 5 ขั้น (เลือกแหล่งที่มา›ข้อมูลหลัก›รายการค่าใช้จ่าย›เอกสารแนบ›ตรวจสอบและยืนยัน) L2285 · `wizardBody()` L2292-2305 |
| FN-02 | g1 | หัวเอกสาร: ผู้เบิก combobox·วันที่·ช่องทางจ่าย | ✓ | step2 `emp` searchSelect + hookbox ตำแหน่ง/cc L2294-2296 · `PAY_OPTS` L2165 |
| FN-03 | g2 | รายการ + VAT none/add/included + totals | ✓ | `calcLineVat`/`migrateLine`/`totals()` L2177-2179 · `taxBadgeV` L2180 · `lineEditor()` step3 L2299 |
| FN-04 | g2 | เกินเพดานหมวด → เตือน + บังคับเหตุผล | ✓ | `overCapLines`/`overCapReasonsOk` L2215-2217 · gate ที่ review L2307 · canSubmit L2346-2347 |
| FN-05 | g2 | ไม่มีรายการ/ยอด=0 → ส่งไม่ได้ | ✓ | `canSubmit = t.grand>0 && t.n>0` L2346 · submitTitle L2347 |
| FN-06 | g2 | ตำแหน่ง/ศูนย์ต้นทุน snapshot ณ วันเบิก | ✓ | hookbox "ดึงจากตำแหน่ง ณ วันเบิก · Movement" L2296 · detail "(ณ วันเบิก)" L2372 |
| FN-12 | g2 | แนบใบเสร็จรายบรรทัด — หมวดบังคับ | ✓ | `receiptRequired` (mock resolve HR Config) L2218 · step4 upload-zone L2301-2303 |
| FN-07 | g3 | ส่งอนุมัติจาก wizard/ใบเบิก | ✓ | `doSubmit()` L2428 · `openSubmitDraft` footer L2394 |
| FN-08 | g3 | DOA slot picker ตามวงเงิน · ไม่ hardcode | ✓ | `DOA_RANGES` mock + comment "ไม่ hardcode สายใน logic" L2196-2198 · `.slot-row` + `searchSelectHTML('slot-i')` L2413 · `APPROVERS` L2204 |
| FN-11 | g3 | แก้ยอดหลังส่ง → re-resolve ถ้าข้ามช่วง | ✓ | `resolveDoa` เรียกซ้ำได้ + comment BR-05 L2212-2213 · microcopy "re-resolve อัตโนมัติ" L2310,2386 |
| FN-13 | g3 | ตีกลับ → แก้แล้วยื่นใหม่ | ✓ | `doReject` เหตุผลบังคับ L2477 · `doReopen` "แก้ไขและยื่นใหม่" footer L2395 |
| FN-14 | g3 | ยกเลิกก่อนอนุมัติ | ✓ | modal `cancel` confirm L2417 · `doCancel` soft archive L2480-2483 |
| FN-09 | g4 | อนุมัติ → เลข EXP-YYYY-NNNN + สำเนา + 7C (FC/EC) | ✓ | `doApprove` `d.code='EXP-2569-'+seq.padStart(4)` L2463 · toast 7C ตาม CSQ_BRIEF L2467 |
| FN-15 | g4 | PDF tab (a4) + tab ลายเซ็น | ✓ | tab `pdf`→`a4Doc(d)` L2380-2381 · tab `sign` DOA timeline L2382-2386 |
| FN-17 | g4 | view tabs รายละเอียด›PDF›ลายเซ็น›ประวัติ + เอกสารแนบใน detail | ✓ | `tabs` 4 แท็บ L2369 · เอกสารแนบ section ใน detail L2376 |
| FN-10 | g4 | เลือกช่องทางจ่าย → ส่งจ่าย (hook) | ✓ | `PAY_OPTS` (payroll/transfer/pv/petty) L2165 · `payDownstream` hook L2167 |
| FN-16 | g4 | "จ่ายแล้ว" อ่านจากปลายทาง display-only | ✓ | detail "สถานะการจ่าย" `payHook` + "display-only — Expense ไม่จ่าย/ไม่ลงบัญชีเอง" L2377 · state `paid` L2153,2182 |
| FN-90 | g5 | list docPill + signprog + filter + empty | ✓ | `docPill`/`renderSignProgress` L2183-2185 · filter select L2269 · `emptyStateHTML` L2274 |
| FN-91 | g5 | ตีกลับ/ยกเลิกผ่าน confirm + soft archive | ✓ | modal reject/cancel confirm L2415-2417 · "soft archive" L2417,2483 |
| FN-92 | g5 | validate + กัน double-submit + wizard ล็อก | ✓ | `if(state._busy)return` L2428,2480 · submit btn disabled จนครบ slot L2472-2473 · `STEP_KEYS` ล็อกลำดับ L2285 |
| FN-93 | g5 | audit ทุก create/แก้/อนุมัติ/ยกเลิก · append-only | ✓ | tab ประวัติ "(audit · append-only)" `EXP.audit` L2388 |
| FN-94 | g5 | ปิดบังจำนวนเงิน (RESTRICTED) ตาม role | ✓ | `maskM()` ใช้ทุกจุดยอดเงิน L2374-2377 · roles `mask:true/false` L2121-2123 |

## Coverage Matrix — S-scenarios (15/15)

| S | เรื่อง | HTML | Evidence |
|---|---|:--:|---|
| S-01 | happy สร้าง→อนุมัติ→เลข+PDF→จ่าย | ✓ | wizard+doSubmit+doApprove |
| S-02 | หลายรายการ/หมวด · VAT รวม/แยก | ✓ | mock d1 3 หมวด · `totals()` |
| S-03 | เกินเพดานหมวด → เตือน | ✓ | `overCap`/`overCapLines` · chip "เกินเพดาน" L2272 |
| S-04 | ไม่มีรายการ/ยอด=0 → ส่งไม่ได้ | ✓ | canSubmit L2346 |
| S-05 | ตำแหน่ง/cc ณ วันเบิก (snapshot) | ✓ | hookbox Movement L2296 |
| S-06 | ตีกลับ → แก้ยื่นใหม่ | ✓ | doReject + doReopen |
| S-07 | ยกเลิกก่อนอนุมัติ | ✓ | doCancel |
| S-08 | ยอดต่างช่วง → สาย DOA ต่าง | ✓ | `DOA_RANGES.find` resolve L2213 · mock d3/d4 ต่างช่วง |
| S-09 | อนุมัติ → FC+เลข/PDF/สำเนา+EC | ✓ | doApprove toast 7C L2463-2467 |
| S-10 | ช่องทางจ่าย payroll/transfer(+pv/petty) | ✓ | PAY_OPTS L2165 |
| S-11 | แก้ยอดข้ามช่วง → re-resolve | ✓ | resolveDoa เรียกซ้ำ + microcopy BR-05 |
| S-12 | itemize VAT none/add/included | ✓ | vat_mode segmented `taxBadgeV` |
| S-13 | แนบใบเสร็จตามนโยบายหมวด | ✓ | receiptRequired L2218 |
| S-14 | จ่ายแล้ว hook display-only | ✓ | payHook L2377 · state paid |
| S-15 | PDF + sign tab | ✓ | a4Doc + sign tab |

## Coverage Matrix — DECLARATION (รอบ 1 = HTML-side เท่านั้น)

| DECL | เข้าเงื่อนไข | HTML-side | Brief | หมายเหตุ |
|---|:--:|:--:|:--:|---|
| DECL-DOA | ✓ (อนุมัติตามวงเงิน) | ✓ slot picker `.slot-row` + ไม่ hardcode chain (L2196-2198,2413) | NOT-CHECKED | brief สร้างหลัง step 7 — ตรวจรอบ 2 |
| DECL-NTF | ✓ (ยื่น/ตีกลับ/จ่าย/เกินเพดาน) | ✓ มี transition รองรับ (submit/reject/paid/overcap) | NOT-CHECKED | brief สร้างหลัง step 7 |
| DECL-CSQ | ✓ (FC/EC มูลค่า·งบ) | ✓ microcopy "บันทึกเข้า 7C ตาม CSQ_BRIEF_F101" ไม่ hardcode ชื่อท่อ (L2466-2467) | NOT-CHECKED | brief สร้างหลัง step 7 · OQ-EXP-02: 7C = FC/EC (no AC) |
| DECL-DOCCFG | ✓ (EXP-YYYY-NNNN) | ✓ `EXP.docSeq.padStart(4)` ไม่ hardcode รูปแบบเลข (L2463) | NOT-CHECKED | brief สร้างหลัง step 7 |

> รอบ 1 (HTML ก่อน FRD/step 7) ยังไม่มีไฟล์ `*_BRIEF_F101.md` — เป็นไปตามลำดับ WF-01 (declaration รันหลัง step 7 · C3.10). HTML-side ครบทุกท่อ (slot picker จริง · ไม่ hardcode chain/รูปแบบเลข/ชื่อท่อ) → **ไม่ BLOCK** · ยกไปตรวจ brief ที่รอบ 2

## Coverage Matrix — SURFACE (Pattern Q)

| Surface | HTML | Evidence |
|---|:--:|---|
| List | ✓ | docPill ครบ 7 state (DST L2182) + filter สถานะ + empty state + signprog |
| Wizard | ✓ | 5 steps ตรง PREBRIEF · step1 แหล่งที่มา · step2 field · step3 line rule VAT · step4 แนบ · step5 review ทุก field |
| View | ✓ | tabs รายละเอียด/PDF/ลายเซ็น/ประวัติ · เอกสารแนบ section · edge-out ปุ่ม ส่ง/อนุมัติ/ตีกลับ/ยกเลิก/ยื่นใหม่ (footer L2390-2396) |
| PDF | ✓ | `a4Doc(d)` tab pdf |
| Modals | ✓ | reason modal ที่ reject (บังคับเหตุผล L2477) · confirm ที่ cancel/approve/submit |

---

## 🟡 WARN / Notes

### NOTE-01 · Touchpoint ใหม่ (PM/BA-approved 2026-09-10 · รอ FN ใน BRD) — ไม่ BLOCK
มติเคาะแล้วแต่ยังไม่สะท้อนใน PREBRIEF/FUNCTION_CHECKLIST (จะ formalize ที่ BRD step 6). HTML เพิ่ม 3 touchpoint เกิน 22 FN:
- **OQ-EXP-01** · pay channel เพิ่ม `pv` (ใบสำคัญจ่าย PV) + `petty` (เงินสดย่อย F091) — hook display-only ต่อจาก FN-10 (L2164-2167) · และ "เคลียร์เงินทดรอง หักลบอัตโนมัติ" (soft-ref F103 · display-only · `advanceHookHTML` L2226-2236) แสดงยอดจ่ายสุทธิ — F101 ไม่ปรับยอดทดรองเอง. unsupported chip ถูก narrow แล้ว: "ระบบเงินสดย่อย/ออกเงินทดรองเต็มรูป (อยู่ที่ F091/F103 — F101 ต่อแค่จุดเชื่อม)" (L2259)
- **OQ-EXP-02** · 7C = FC/EC (ไม่มี AC) — ตรงกับ microcopy doApprove (unchanged)
- **OQ-EXP-03** · scope การมองเห็น: `roles[]` (L2118-2123) — ผู้เบิก/ธุรการ `scope:'self'` เห็นเฉพาะใบตน (`isSelf`/`visibleDocs` L2170-2172) · role ใหม่ **เจ้าหน้าที่ (HR/Finance)** `scope:'all'`+`mask:false`+`approver:false` (เห็นทั้งหมด·ไม่มาสก์·ไม่ใช่ผู้อนุมัติ)
→ **แนะนำ**: ให้ BA เพิ่ม FN สำหรับ touchpoint เหล่านี้ใน FUNCTION_CHECKLIST ตอนทำ BRD (step 6) เพื่อปิด gap เอกสาร-vs-จอ

### NOTE-02 · Hook cross-feature display-only เสริม (ยืนยัน scope)
HTML มี hook display-only เพิ่มที่ไม่อยู่ในรายการ 3 touchpoint ข้างต้น: **F117 Budget Control** (`budgetHookHTML` L2239) และ **F102 Welfare สิทธิ์คงเหลือ** (L2243) — ทั้งคู่ mock/display-only มีป้ายกำกับชัด สอดคล้อง BR-07 (FC commit งบ). เป็นของเสริม ไม่กระทบ verdict → **เสนอให้ผู้ใช้ยืนยันว่าตั้งใจคงไว้** (หรือถอดถ้าเกิน scope รอบนี้)

## ⬜ NOT-CHECKED
- Declaration briefs (DOA/NTF/CSQ/DOCCFG `*_BRIEF_F101.md`) — ยังไม่สร้าง (หลัง step 7) → ตรวจรอบ 2 พร้อม FRD Pack + TC
- Golden rules ระดับ FRD (05_RULES), FN↔TC ledger, XT cross-module — เป็นงานรอบ 2

## Scope Guard (ผ่าน)
unsupported 7 ข้อใน FUNCTION_CHECKLIST ไม่มีข้อไหนหลุดเข้ามาเป็นฟังก์ชันจริงใน HTML: ไม่จ่ายเงินจริง/GL posting (hook only) · ไม่มี mileage/travel-request/OCR · ไม่มี CRUD เพดานหมวด (อ่าน HR Config) · THB only. cash-advance ถูก narrow เป็น touchpoint display-only ตามมติ (ไม่ใช่ระบบทดรองเต็มรูป) — ถูกต้อง
