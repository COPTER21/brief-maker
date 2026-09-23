# _COVERAGE_R2_REPORT — F-ACC-DN ใบลดหนี้ผู้ขาย (Debit Note · F097)

> **Gate:** WF-01 Step 10 — Coverage Round 2 (FRD Pack + Test Cases, pre-dev-handoff)
> **Checker:** qc-coverage-checker (Round 2 mode) · 2026-09-23
> **Question ของรอบนี้:** "spec (FRD) และ test (TC) ผูกเรื่องครบมั้ย" — ไม่ใช่ HTML hooks (นั่นคือ R1)
> **Contract:** FUNCTION_CHECKLIST (24 FN) + PREBRIEF (S-01..14 · BR-01..17) + 4 declaration briefs (+pdfdoc)
> **Artifacts checked:** `FRD_Pack/00,01,02,03,04,05,06,07` · `testcases-F-ACC-DN.md` (102 เคส · 14 group) · `5_DECLARATIONS/{DOA,NTF,CSQ,DOCCFG,INDEX}`
> **R1 report:** `_COVERAGE_REPORT.md` — คงไว้ ไม่แก้ (ไฟล์นี้แยกต่างหาก)
> **Mirror:** โครง/verdict style = `../F-ACC-CN/_COVERAGE_R2_REPORT.md`

---

## VERDICT: ✅ **PASS**

- Block-severity rules (BR-01..17) ครอบครบใน 05_RULES **และ** มี TC ≥1 ทุกข้อ — ไม่มี rule ที่ไม่มี test
- FN↔TC ledger = **24/24** (ทุก FN มี TC ที่ยืนยันแล้วว่ามี `### TC-...` header จริงในไฟล์ — ไม่ใช่ phantom)
- Declaration coverage ครบ 4 ท่อ (+pdfdoc) · chip = detect ทุกท่อ · **ไม่มี DIVERGENCE** (ตรง DECLARATION_INDEX)
- Known drift D-3 (revise-doc API-14) / D-4 (resend API-09) = tag forward ภายใต้ **OQ-DN-04** ครบทุก layer (01_UI/02_API/03_LOGIC/04_DB/05_RULES) + UI Brief §11 Drift Log — **governance note ไม่ใช่ BLOCK**
- WARN ทั้งหมดเป็น **doc-drift/count-drift ใน 06_TESTS** ไม่กระทบความครบของ spec/test — ไม่บล็อกส่ง dev

---

## 1 · FN ↔ TC Ledger — 24/24 ✅

ทุกแถวยืนยันแล้วว่า TC ที่อ้างมี `### TC-...` header จริงในไฟล์ (verified — no phantom):

| FN | Rule / S trace | AC (06_TESTS §6.1) | TC (testcases md — verified มีจริง) |
|---|---|---|---|
| FN-01 | S-01 · BR-01 | AC-01 | TC-S01, TC-S02, TC-01 |
| FN-02 | S-12 · BR-16 · OQ-DN-01 | AC-14 | TC-S03, TC-14a |
| FN-03 | S-01 | AC-01 | TC-S02, TC-01 |
| FN-04 | S-13 · BR-13 · FIX-01 | AC-13, AC-20 | TC-S04, TC-13c, TC-20a |
| FN-05 | S-01 · BR-06 | AC-02 | TC-R01, TC-R02, TC-R03, TC-01, TC-X06 |
| FN-06 | S-02 · BR-04 | AC-06 | TC-06, TC-06b |
| FN-07 | S-03 · BR-03 | AC-07 | TC-07, TC-07b |
| FN-08 | S-04 · BR-03/10 | AC-08 | TC-08 |
| FN-09 | S-05 · BR-02 | AC-09 | TC-09, TC-09b, TC-09c |
| FN-10 | BR-05 | AC-10 | TC-10 |
| **FN-19** | **S-05/S-14 · BR-11/BR-12 · LD-05** | **AC-19(a/b/c)** | **TC-19a,b,c,d,e,f,g (7 เคส)** |
| FN-11 | S-06 · BR-07 | AC-11 | TC-11a,b,c,d,e |
| FN-12 | S-06 · BR-08 | AC-12 | TC-12, TC-12b |
| FN-13 | S-07 | AC-13 | TC-13, TC-13b |
| FN-14 | S-08 · BR-07 (SoD) | AC-14 | TC-14b, TC-P05 |
| FN-17 | S-11 · BR-02/13 · FIX-01 | AC-17 | TC-17, TC-17b |
| FN-15 | S-09 | AC-15 | TC-15, TC-15b |
| FN-16 | S-10 | AC-16 | TC-16, TC-16b |
| FN-18 | S-14 · BR-09 | AC-18 | TC-18, TC-18b |
| **FN-20** | **S-13/S-14 · BR-13 · FIX-01** | **AC-20** | **TC-20a, TC-20b, TC-X07** |
| **FN-21** | **S-14 · BR-14 · FIX-02** | **AC-21** | **TC-21a, TC-21b, TC-21c, TC-X02** |
| FN-90 | กติกากลาง | AC-90 | TC-L01..TC-L10 |
| FN-91 | GR-4 · BR-15 | AC-91 | TC-91, TC-91b |
| FN-92 | OB-6 | AC-92 | TC-92 |

**FN ไม่มี TC: 0 ข้อ.** ทุก FN มี AC ใน §6.1 (21 AC ครอบ 24 FN — AC-01=FN-01/03 · AC-13=FN-13/04 · AC-14=FN-02/14 · AC-20=FN-04/20) และ TC ≥1 ใน testcases md.
**ไม่มี orphan TC** ที่อ้าง FN ที่ไม่มีอยู่จริง — `FN-40` ปรากฏเป็นข้อความ "ไม่มี FN-40 เดี่ยว" ใน Meta เท่านั้น (ถูกต้อง — negatives เป็น bundle ไม่ใช่ FN เดี่ยว).

---

## 2 · Rule ↔ Test — ไม่มี rule ที่ไม่มี test ✅

BR-01..17 ทุกข้อมี TC (05_RULES §5.1 → testcases "Business Rules" ledger §5.1, verified):

| BR | เนื้อหา | TC |
|---|---|---|
| BR-01 | picker เฉพาะ approved/posted · dnRoom>0 | TC-S01, TC-S04, TC-13c |
| BR-02 | grand ≤ dnRoom (ส่ง + อนุมัติขั้นสุดท้าย) | TC-09, TC-09b, TC-17, TC-X01 |
| BR-03 | qty/net ≤ ที่ลดได้ (ข้ามทุกใบ) | TC-07, TC-08, TC-09c |
| BR-04 | price ≤ ราคาเดิม (mode price) | TC-06, TC-06b |
| BR-05 | reason ∈ master · text ≥10 | TC-10, TC-R04 |
| BR-06 | RTV ต้องอ้างใบคืนสินค้า · qty ≤ RTV | TC-R01, TC-R02, TC-R03 |
| BR-07 | DOA resolve ตาม grand · SoD | TC-11c, TC-14b, TC-19c, TC-P05 |
| BR-08 | เลข DN no-gap ตอน final approve | TC-12, TC-12b |
| BR-09 | approved → dn_applied + JE + ลดภาษีซื้อ | TC-18, TC-X01, TC-X03 |
| BR-10 | held ชั่วคราว · ยกเลิกคืน held | TC-08, TC-15, TC-X04 |
| **BR-11** | **end-bill cap · net ≥0 ≤dnRoom (บล็อก+เตือน)** | **TC-19b, TC-19e** |
| **BR-12** | **end-bill ลดฐานภาษี · input VAT ม.86/10** | **TC-19a, TC-19d, TC-18b, TC-X02** |
| **BR-13** | **dnRoom ไม่หัก paid · vendorCredit split (FIX-01)** | **TC-20a, TC-20b, TC-S04, TC-X07** |
| **BR-14** | **input VAT gated by vendorCn · ม.82/10 (FIX-02)** | **TC-21a, TC-21b, TC-21c, TC-X02** |
| BR-15 | append-only · no hard delete · ค.ศ. | TC-91, TC-91b, TC-NEG-04 |
| BR-16 | tile ลดลอย ปิดไว้ | TC-S03, TC-14a |
| BR-17 | legal_basis ต่อ reason (PDF) | TC-R05, TC-92 |

State-machine guards (§5.2 → TC-GRD-01..05) + error catalog (§5.6, 22 code) + permission matrix (§5.3 → TC-P01..P09) + edge (§5.5 → EC-01..07 + PR probes) + cross-module (§6.9 → TC-X01..X07) — ทุกแถวมี TC (ตรวจใน testcases ledger). **ไม่มี rule/guard/error/edge ที่ค้างไม่มี TC.**

---

## 3 · Focus Areas (BA FIX-01/FIX-02 · corrected drift) — ครบทั้ง rule + TC ✅

| Focus | Rule text (05_RULES) | TC (evidence) |
|---|---|---|
| **FN-19 · BR-11 (cap, net≥0, บล็อก+เตือน)** | §5.1 BR-11 (ebOver → blockReason/submitGuard "ส่วนลดท้ายบิลเกินยอดที่ลดได้ (สูงสุด ฿X)") + §5.4 endbill + §5.6 BR_ENDBILL_EXCEEDS_CAP | **TC-19b** (over cap → block submit) · **TC-19e** (boundary net ≤ dnRoom) |
| **FN-19 · BR-12 (input VAT recompute ม.86/10)** | §5.1 BR-12 (`ebVat=ebAmt×(vat/after)` · `netVat=vat−ebVat` · ภ.พ.30/JE/PDF สะท้อน netVat) + §5.8 ม.86/10 | **TC-19a** (calc netBefore/netVat verbatim "ภาษีซื้อที่ลด · คิดจากฐานใหม่") · **TC-19d** (mode %) · **TC-19g** (หลายอัตรา) · TC-18b · **TC-X02** |
| **FN-04/FN-20 · BR-13 (dnRoom ไม่หัก paid · vendorCredit) — FIX-01 semantic reversal** | §5.1 BR-13 (`dnRoom = invGrand − dn_applied − dn_held` **ไม่หัก paid** · `dnSplit`: applyToAp=min(grand,outstanding) · vendorCredit=ส่วนเกิน) + 07 **LD-07** | **TC-20a** (ใบจ่ายครบยังออก DN → vendorCredit) · **TC-20b** (credit ledger card/modal **display-only**) · **TC-S04** (ใบ dnRoom=0 ไม่โผล่ · จ่ายครบยังโผล่) · **TC-X07** |
| **FN-21 · BR-14 (input VAT gated by vendorCn · ม.82/10) — FIX-02** | §5.1 BR-14 (gate vendorCn+date · เดือนภาษี=vendorCnDate · ไม่มี→"รอเอกสาร") + §5.4 vendor_cn gate + 07 **LD-08** | **TC-21a** ("รอเอกสาร" read-only) · **TC-21b** (บันทึก vendorCn → ภ.พ.30 เดือน vendorCnDate) · **TC-21c** (openVendorCn บนใบ sent) · **TC-X02** |
| **Status guards** submit/edit/cancel/send/vendorCn | §5.2 guard block + verbatim error (BR_SUBMIT/EDIT/CANCEL/SEND/VENDORCN_STATE_*) | **TC-GRD-01** (submit), **TC-GRD-02** (edit), **TC-GRD-03** (cancel), **TC-GRD-04** (send), **TC-GRD-05** (vendorCn) |
| **DOA tier on NET after end-bill (LD-05)** | §5.1 BR-07 + DOA Tier Matrix "คิดจาก `grand` หลัง end-bill — LD-05" · 07 LD-05 | **TC-19c** (ปรับ end-bill → grand ข้าม tier → สายอนุมัติเปลี่ยน) · TC-11c, TC-11e (boundary 50k) |
| **"ออกเอกสารแก้ไข" / resend (D-3/D-4 · forward)** | §5.2 approved/sent → ออกเอกสารแก้ไข (display-only, ไม่เปลี่ยน state) · LD-04 · tag OQ-DN-04 | **TC-NEG-05 / TC-X05** (revise-doc display-only ไม่ถอนยอด) · TC-16b (resend) |
| **legal_basis per reason** | §5.1 BR-17 (RTV/OVERPRICE/SHORT แต่ละตัวมี legal_basis · ม.86/10) + §5.8 | **TC-R05** (legal_basis hint ต่อ reason) · TC-92 (พิมพ์ลง PDF) |

> หมายเหตุ legal basis: **ม.86/10** = ออกใบลดหนี้อ้างใบกำกับเดิม (BR-17/FN-92 · confirmed). **ม.82/10** = เดือนภาษีฝั่งซื้อ (input VAT ลง ภ.พ.30 เดือน vendorCnDate) — **[ASSUMED · mirror CN ฝั่ง AR → OQ-DN-05]** รอ BA/Finance รับรองก่อน dev ตั้งค่า.

---

## 4 · Declaration Coverage (Phase 0b + R2 Declaration↔FRD) — ครบ · ไม่มี DIVERGENCE ✅

| ท่อ | เข้าเงื่อนไข | Brief | chip vs detect | FRD sync / no-hardcode | สถานะ |
|---|---|---|---|---|---|
| **DOA** | approval + วงเงิน (3-tier) | `DOA_BRIEF` ✅ | detect ✓ (=chip) | matrix ไม่ hardcode chain · resolveDoa→grand (LD-05) · approveGuard→dnRoom (FIX-01) · sync 05_RULES BR-07/§5.2/§5.3 | ✅ |
| **NTF** | ส่งผู้ขาย/ยกเลิก/ออกเลข | `NTF_BRIEF` ✅ | detect ✓ (3 event) | dn.issued/dn.sent/dn.cancelled = 06_TESTS §6.5 (FRD events ⊆ brief) · ตัด doa_pending/result (engine) · channel ไม่ hardcode | ✅ |
| **CSQ** | กระทบบัญชี/มูลค่า/VAT | `CSQ_BRIEF` ✅ | detect ✓ (AC+EC) | ประกาศ AC+EC เท่านั้น · **ไม่ประกาศ OC/DC-document/SC** (กัน register 422) · input-VAT gated vendorCn · sync FN-18/BR-09/BR-12/BR-14 | ✅ |
| **DOCCFG** | เอกสารธุรกรรม + เลขรัน DN-YYYY-NNNN | `DOCCFG_BRIEF` ✅ | detect ✓ | BR-08 = ENG-DOC-NUM.next (no-gap) · LOCK-06 · ไม่ hardcode รูปแบบเลข | ✅ |
| **pdfdoc** | เอกสารพิมพ์ A4 (step 2) | `../_print/` ✅ | detect ✓ | template + sample.pdf + print-spec · PDF อ้างเลข/วันที่ใบกำกับเดิม (ม.86/10) FN-92 | ✅ |

**DIVERGENCE: ไม่มี.** ทุก chip ตรงกับ detect (ตรง `DECLARATION_INDEX.md`) · brief ทุกใบถูก sync read ใน FRD · ไม่พบ hardcoded chain / ช่องทางแจ้งเตือน / รูปแบบเลขรันใน FRD. (สอดคล้อง memory: declaration answered by plan chip + pack DECLARATION_INDEX, DIVERGENCE none.)

---

## 5 · Coverage Matrix (สรุป)

| Item | FRD (05/06) | TC | Evidence |
|---|:--:|:--:|---|
| FN-01..21 + FN-90/91/92 (24) | ✓ | ✓ | 00_OVERVIEW Coverage · 06 §6.1 AC · testcases ledger 24/24 |
| BR-01..17 (17) | ✓ | ✓ | 05_RULES §5.1 · testcases "Business Rules" |
| State guards (submit/edit/cancel/send/vendorCn + revise) | ✓ | ✓ | 05_RULES §5.2 · TC-GRD-01..05, TC-NEG-05 |
| Error catalog (22 code) | ✓ | ✓ | 05_RULES §5.6 · testcases "Field Validation/Error" |
| Permission/SoD | ✓ | ✓ | 05_RULES §5.3 · TC-P01..P09, TC-14b |
| Edge EC-01..07 + PR probes (CC/ID/CALC/FU/CA) | ✓ | ✓ | 05_RULES §5.5 · TC-17/08/20a/13c/15/13 + TC-CC/ID/CALC/FU/CA-01 |
| Cross-module XT-01..07 | ✓ | ✓ | 06 §6.9 · TC-X01..X07 |
| Scope Lock LOCK-01..10 / LD-01..08 | ✓ | ✓ | 07_LOCKED · TC-LK-01/06/09/10 |
| DECL-DOA/NTF/CSQ/DOCCFG/pdfdoc | ✓ | ✓ | §4 ข้างบน |
| SURFACE list/wizard/view/pdf/modals (Pattern Q) | ✓ | ✓ | ยืนยันแล้วใน R1 (`_COVERAGE_REPORT.md`) — R2 ไม่ตรวจซ้ำ |

---

## 6 · Gaps / WARN carried for close-out (ไม่บล็อก — doc hygiene)

1. **[WARN · doc-drift] 06_TESTS §6.8 "Trace: AC → Logic" Functions column เพี้ยน** — แถว **AC-20** เขียน `FN-11,17` (ควรมี FN-04/FN-20) และแถว **AC-21** เขียน `FN-16` (ควรเป็น FN-21) ทั้งที่ header §6.1 ระบุ AC-20=FN-04/FN-20 · AC-21=FN-21 ถูกต้อง · บรรทัดสรุปเขียน "ทุก FN-01..21 ... ถูก trace ≥1 AC ✅" แต่ตารางไม่ได้ลิสต์ FN-20/FN-21 ในคอลัมน์ Functions. **ไม่กระทบความครบจริง** (AC header §6.1 + FN↔TC ledger ถูกต้อง 24/24). แก้: ปรับ §6.8 ให้ Functions ตรง AC (AC-20→FN-04,11,17,20 · AC-21→FN-16,21).

2. **[WARN · count-drift R15] 06_TESTS §6.2 Test Inventory เป็น subset ของ testcases md** — §6.2 ลิสต์ ~30 core TC (1 ต่อ AC หลัก) แต่ testcases md มี **102 เคส** (แตกย่อย TC-19d/e/f/g · TC-11d/e · TC-P0x · TC-X0x · TC-GRD-0x · TC-NEG-0x · TC-LK-0x · TC-R0x). §6.2 มี note รับทราบว่าเป็น core inventory + md expansion แล้ว — ทุก FN ยังครบทั้งสองระดับ แต่จำนวน MD↔QA HTML↔AI-testset ยังไม่ sync (R15). แก้: reconcile count (เติม expansion เข้า §6.2 หรือ tag expansion) ก่อน generate QA HTML/AI testset.

3. **[INFO · carry OQ ไม่บล็อก]** OQ ที่ยังเปิด (business decision ไม่ใช่ requirement หล่น — ยกไป step-12 PROPOSALS):
   - **OQ-DN-02** — จุดตัดวงเงิน DOA 50k/300k + role ต่อ tier [DEFAULT]
   - **OQ-AP-06** — role-ids `role-mgr-pur`/`role-mgr-acc`/`role-cfo` [ASSUMED]
   - **OQ-DN-05** ⭐ — legal basis input-VAT ม.82/10 ฝั่งซื้อ [ASSUMED · mirror CN] — dev ต้องได้คำตอบก่อนตั้งค่า reversal เดือนภาษี
   - **OQ-DN-04** — เส้นทาง "ออกเอกสารแก้ไข"/resend (D-3/D-4 · ปัจจุบัน display-only/forward) — dev **อย่า build** จนกว่า BA เคาะ
   - **OQ-DN-03 / OQ-DN-06** — refund / flow ใช้-ตัดยอดเครดิตคงเหลือกับผู้ขาย (display-only รอบนี้)
   - **OQ-DN-07** — CSQ profile-id + event (dn.issued vs dn.vat_applied)
   - **CA-01** — vendorCn ซ้ำ / เดือนภาษีปิดงวด (flag warn ไม่ block รอบนี้)
   ทั้งหมด NO-block ต่อ FRD/TC แต่ dev ต้องได้คำตอบก่อนตั้งค่าจริง (DOA/CSQ/VAT reversal).

---

## 7 · Diff vs R1 (`_COVERAGE_REPORT.md`)

- **ปิดแล้ว:** R1 ตรวจ HTML hooks/surface (list/wizard/view/pdf/modals + FN handler เดินได้ · e2e 36/36) → PASS. R2 ไม่ตรวจซ้ำ.
- **เพิ่มใน R2:** FN↔TC ledger 24/24 (verified no-phantom) · Rule↔TC 17/17 · Declaration↔FRD sync (4 ท่อ +pdfdoc) · focus BR-11/12/13/14 + guards + LD-05/07/08 มีทั้ง rule + TC · ยืนยัน D-3/D-4 tag forward ครบทุก layer.
- **เกิดใหม่:** 2 WARN (06_TESTS §6.8 trace-drift + §6.2 count-drift) — cosmetic · ไม่บล็อก.

---

**Bottom line:** FRD Pack + Test Cases ผูก contract ครบก่อนส่ง dev — **PASS**. แก้ 2 WARN ใน 06_TESTS (§6.8 trace Functions + §6.2 count-sync) ให้เนียน + ให้ BA เคลียร์ OQ ที่ dev ต้องใช้ตั้งค่าจริง (โดยเฉพาะ role-ids OQ-AP-06 · legal basis ม.82/10 OQ-DN-05 · revise-doc path OQ-DN-04).
