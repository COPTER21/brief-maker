# _COVERAGE_R2_REPORT — F-ACC-CN ใบลดหนี้ลูกค้า (Credit Note · F096)

> **Gate:** WF-01 Step 10 — Coverage Round 2 (FRD Pack + Test Cases, pre-dev-handoff)
> **Checker:** qc-coverage-checker (Round 2 mode) · 2026-09-22
> **Question ของรอบนี้:** "spec (FRD) และ test (TC) ผูกเรื่องครบมั้ย" — ไม่ใช่ HTML hooks (นั่นคือ R1)
> **Contract:** FUNCTION_CHECKLIST (22 FN incl FN-19) + PREBRIEF (S-01..16 · BR-01..15) + 4 declaration briefs
> **Artifacts checked:** `FRD_Pack/00,05,06,07` · `testcases-F-ACC-CN.md` (88 เคส · 13 group) · `5_DECLARATIONS/{DOA,NTF,CSQ,DOCCFG}`
> **R1 report:** `_COVERAGE_REPORT.md` — คงไว้ ไม่แก้ (ไฟล์นี้แยกต่างหาก)

---

## VERDICT: ✅ **PASS**

- Block-severity rules (BR-01..15) ครอบครบใน 05_RULES **และ** มี TC ≥1 ทุกข้อ — ไม่มี rule ที่ไม่มี test
- FN↔TC ledger = **22/22** (ทุก FN มี TC ที่ชี้ตำแหน่งได้จริงในไฟล์)
- Declaration coverage ครบ 4 ท่อ · chip = detect ทุกท่อ · **ไม่มี DIVERGENCE**
- WARN ทั้งหมดเป็น **doc-drift ใน FRD trace table** (§6.8) ไม่กระทบความครบของ spec/test — ไม่บล็อกส่ง dev

---

## 1 · FN ↔ TC Ledger — 22/22 ✅

ทุกแถวยืนยันแล้วว่า TC ที่อ้างมี `### TC-...` header จริงในไฟล์ (ไม่ใช่ phantom):

| FN | Rule text (05_RULES) | AC (06_TESTS) | TC (testcases md — verified มีจริง) |
|---|---|---|---|
| FN-01 | BR-01 | AC-01 | TC-S01, TC-S02, TC-01 |
| FN-02 | BR-14 | AC-14 | TC-S03, TC-14a |
| FN-03 | BR-01/pickInvoice | AC-01 | TC-S02, TC-01 |
| FN-04 | BR-01 · EC-03/04 | AC-13 | TC-S04, TC-13c |
| FN-05 | BR-06 | AC-02 | TC-R01, TC-R02, TC-R03, TC-01 |
| FN-06 | BR-04 | AC-06 | TC-06, TC-06b |
| FN-07 | BR-03 | AC-07 | TC-07, TC-07b |
| FN-08 | BR-03/BR-10 · EC-02 | AC-08 | TC-08 |
| FN-09 | BR-02 | AC-09 | TC-09, TC-09b, TC-09c |
| FN-10 | BR-05 | AC-10 | TC-10 |
| **FN-19** | **BR-11 + BR-12** | **AC-19(a/b/c)** | **TC-19a,b,c,d,e,f,g (7 เคส)** |
| FN-11 | BR-07 | AC-11 | TC-11a,b,c,d,e |
| FN-12 | BR-08 | AC-12 | TC-12, TC-12b |
| FN-13 | §5.2 · EC-06 | AC-13 | TC-13, TC-13b |
| FN-14 | BR-07/§5.3 (SoD) | AC-14 | TC-14b, TC-P05 |
| FN-17 | BR-02 · EC-01 | AC-17 | TC-17 |
| FN-15 | §5.2 · EC-05 | AC-15 | TC-15, TC-15b |
| FN-16 | §5.2 | AC-16 | TC-16, TC-16b |
| FN-18 | BR-09 | AC-18 | TC-18, TC-18b |
| FN-90 | กติกากลาง | AC-90 | TC-L01..TC-L10 |
| FN-91 | BR-13 | AC-91 | TC-91, TC-91b, TC-NEG-04 |
| FN-92 | ม.86/10 · BR-15 | AC-92 | TC-92 |

**FN ไม่มี TC: 0 ข้อ.** ทุก FN มี AC 1:1 ใน 06_TESTS §6.1 และ TC ≥1 ใน testcases md.

---

## 2 · Rule ↔ Test — ไม่มี rule ที่ไม่มี test ✅

BR-01..15 ทุกข้อมี TC (05_RULES §5.1 → testcases "Business Rules" ledger, verified):

| BR | เนื้อหา | TC |
|---|---|---|
| BR-01 | picker เฉพาะ issued/sent outstanding>0 | TC-S01, TC-S04, TC-13c |
| BR-02 | grand ≤ available (ส่ง) + ≤ outstanding (อนุมัติ) | TC-09, TC-09b, TC-17, TC-X01 |
| BR-03 | qty/net ≤ ที่ลดได้ ข้ามทุกใบ | TC-07, TC-08, TC-09c |
| BR-04 | price ≤ ราคาเดิม | TC-06, TC-06b |
| BR-05 | reason ∈ master · text ≥10 | TC-10, TC-R04 |
| BR-06 | RET ต้องอ้าง SR · qty ≤ SR | TC-R01/R02/R03 |
| BR-07 | DOA resolve ตาม grand · SoD | TC-11c, TC-14b, TC-19c, TC-P05 |
| BR-08 | เลข CN no-gap ตอน final approve | TC-12, TC-12b |
| BR-09 | approved → cn_applied + JE + ลดภาษีขาย | TC-18, TC-X01, TC-X03 |
| BR-10 | held ชั่วคราว · ยกเลิกคืน | TC-08, TC-15, TC-X04 |
| **BR-11** | **end-bill cap · net ≥0 ≤คงค้าง (บล็อก+เตือน)** | **TC-19b, TC-19e** |
| **BR-12** | **end-bill ลดฐานภาษี · VAT ม.86/10** | **TC-19a, TC-19d, TC-18b, TC-X02** |
| BR-13 | append-only · no hard delete · ค.ศ. | TC-91, TC-91b, TC-NEG-04 |
| BR-14 | tile ลดลอย ปิดไว้ | TC-S03 |
| BR-15 | legal_basis ต่อ reason · DISC warn | TC-R05, TC-06, TC-92 |

State-machine guards (§5.2) + error catalog (§5.6) + permission matrix (§5.3) + edge (§5.5) + cross-module (§6.9) — ทุกแถวมี TC (ตรวจใน testcases ledger §State Machine / Error / Permission / EC / XT). ไม่มี rule/guard/error ที่ค้างไม่มี TC.

---

## 3 · Focus Areas (BA-changed) — ครบทั้ง rule + TC ✅

| Focus | Rule text (05_RULES) | TC (evidence) |
|---|---|---|
| **FN-19 · BR-11 (cap, net≥0, บล็อก+เตือน)** | §5.1 BR-11 (ebCap, ebOver, "ยอดสุทธิห้ามติดลบ") + §5.4 endbill + §5.6 BR_ENDBILL_EXCEEDS_CAP | **TC-19b** (over cap → hard-warn + block submit, grand clamp=0, ไม่เปิด submit modal) · **TC-19e** (boundary net ≤ outstanding) |
| **FN-19 · BR-12 (VAT recompute ม.86/10)** | §5.1 BR-12 (`ebVat=ebAmt×(vat/after)` · `netVat=vat−ebVat` · ภ.พ.30/JE/PDF สะท้อน netVat) + §5.8 ม.86/10 | **TC-19a** (verify netBefore/netVat + verbatim summary rows "คิดจากฐานใหม่ (ม.86/10)") · **TC-19d** (mode %) · TC-18b · **TC-X02** (ภ.พ.30 netVat) |
| **Status guards** cancel/send/submit/edit | §5.2 guard block + verbatim error msg (BR_SUBMIT/EDIT/CANCEL/SEND_STATE_*) | **TC-GRD-01** (submit), **TC-GRD-02** (edit), **TC-GRD-03** (cancel), **TC-GRD-04** (send) |
| **"ออกเอกสารแก้ไข"** (display-only) | §5.2 approved/sent → ออกเอกสารแก้ไข (ไม่เปลี่ยน state) · LD-04 | **TC-NEG-05** (= XT-05 · revise-doc display-only ไม่ถอนยอด) |
| **legal_basis per reason** | §5.1 BR-15 (RET/DISC/PRICE/QTY แต่ละตัวมี legal_basis · ม.86/10) + §5.8 | **TC-R05** (legal_basis hint เปลี่ยนตาม reason + DISC trade_discount_warn) · TC-92 (legal_basis พิมพ์ลง PDF) |
| **DOA tier on NET after end-bill (LD-05)** | §5.1 BR-07 + DOA Tier Matrix note "คิดจาก `grand` หลัง end-bill — LD-05" · 07_LOCKED **LD-05** (OQ-b RESOLVED) | **TC-19c** (ปรับ end-bill → grand ข้าม tier → สายอนุมัติเปลี่ยน tier3→tier2, พิสูจน์คิดจาก grand หลังหัก) |

> หมายเหตุ: legal_basis ผูก **ม.86/10** (ออกใบลดหนี้อ้างใบกำกับเดิม) ถูกต้องตามกฎหมาย — ส่วน **ม.82/10** ใช้กับ "เดือนภาษี netVat ลง ภ.พ.30" (§5.8 · XT-02) แยกกันชัดเจน ไม่ปน.

---

## 4 · Declaration Coverage (Phase 0b + R2 Declaration↔FRD) — ครบ · ไม่มี DIVERGENCE ✅

| ท่อ | เข้าเงื่อนไข | Brief | chip vs detect | FRD sync / no-hardcode | สถานะ |
|---|---|---|---|---|---|
| **DOA** | approval + วงเงิน (3-tier) | `DOA_BRIEF` ✅ | detect ✓ (=chip) | matrix §3 ไม่ hardcode chain · resolveDoa→grand (LD-05) · sync 05_RULES BR-07/§5.2/§5.3 | ✅ |
| **NTF** | มอบหมาย/ส่งลูกค้า/ยกเลิก | `NTF_BRIEF` ✅ | detect ✓ | 3 event (ar_cn_approved_applied/sent/cancelled) = 06_TESTS §6.5 (FRD events ⊆ brief) · ตัด doa_pending/result (engine) · channel ไม่ hardcode | ✅ |
| **CSQ** | กระทบบัญชี/มูลค่า/VAT | `CSQ_BRIEF` ✅ | detect ✓ | ประกาศ AC+EC เท่านั้น · **ไม่ประกาศ OC/DC-document/SC** (กัน register 422) · SecC no-effect · sync FN-11/BR-09/BR-12 | ✅ |
| **DOCCFG** | เอกสารธุรกรรม + เลขรัน CN-YYYY-NNNN | `DOCCFG_BRIEF` ✅ | detect ✓ | BR-08 = ENG-DOC-NUM.next (no-gap) · LOCK-06 · ไม่ hardcode รูปแบบเลข | ✅ |

**DIVERGENCE: ไม่มี.** ทุก chip ตรงกับ detect · brief ทุกใบถูก sync read ใน FRD · ไม่พบ hardcoded chain / ช่องทางแจ้งเตือน / รูปแบบเลขรันใน FRD. (สอดคล้อง memory: declaration answered by plan chip + pack DECLARATION_INDEX, DIVERGENCE none.)

---

## 5 · Coverage Matrix (สรุป)

| Item | FRD (05/06) | TC | Evidence |
|---|:--:|:--:|---|
| FN-01..19 + FN-90/91/92 (22) | ✓ | ✓ | 00_OVERVIEW §0.12 Coverage Manifest 22/22 · 06 §6.1 AC 1:1 · testcases ledger 22/22 |
| BR-01..15 (15) | ✓ | ✓ | 05_RULES §5.1 · testcases "Business Rules" |
| State guards (submit/edit/cancel/send + revise) | ✓ | ✓ | 05_RULES §5.2 · TC-GRD-01..04, TC-NEG-05 |
| Error catalog (18 code) | ✓ | ✓ | 05_RULES §5.6 · testcases "Error Catalog" |
| Permission/SoD | ✓ | ✓ | 05_RULES §5.3 · TC-P01..P09, TC-14b |
| Edge EC-01..06 + PR probes | ✓ | ✓ | 05_RULES §5.5 · TC-17/08/13c/15/13 + TC-CC/ID/CALC/FU-01 |
| Cross-module XT-01..06 | ✓ | ✓ | 06 §6.9 · TC-X01..X06 |
| Scope Lock LOCK-01..10 / LD-01..06 | ✓ | ✓ | 07_LOCKED · TC-LK-01/06/09/10 |
| DECL-DOA/NTF/CSQ/DOCCFG | ✓ | ✓ | §4 ข้างบน |
| SURFACE list/wizard/view/pdf/modals (Pattern Q) | ✓ | ✓ | ยืนยันแล้วใน R1 (`_COVERAGE_REPORT.md`) — R2 ไม่ตรวจซ้ำ |

---

## 6 · Gaps / WARN carried for close-out (ไม่บล็อก — doc hygiene)

1. **[WARN · doc-drift] 06_TESTS §6.8 "Trace: AC → Logic" mapping เพี้ยน** — คอลัมน์ Functions จับคู่ผิด (เช่น AC-19→FN-05, AC-11→FN-06, AC-12→FN-07) และบรรทัดสรุปเขียน "ทุก FN-01..15" ทั้งที่ feature มีถึง FN-19 + FN-90/91/92. เป็นตารางสรุปเก่า/คลาดเคลื่อน — **ไม่กระทบความครบจริง** (FN↔TC ledger + Coverage Manifest §0.12 ถูกต้อง 22/22). แก้: ปรับ §6.8 ให้ FN ตรง AC และเขียน "FN-01..19 + 90/92".
2. **[WARN · count-drift] 06_TESTS §6.2 Test Inventory เป็น subset ของ testcases md** — §6.2 ลิสต์ ~26 TC หลัก แต่ testcases md มี 88 เคส (เพิ่ม TC-19d/e/f/g, TC-11d/e, TC-P0x, TC-X0x, TC-GRD-0x, TC-NEG-0x, TC-LK-0x). ทุก FN ยังมี TC ใน §6.2 อยู่แล้ว — การขยายใน md ไม่ทำให้ FN หล่น แต่จำนวนไม่ sync (R15). แก้: เติม TC ที่ขยายเข้า §6.2 inventory (หรือ tag ว่า md = expansion) ก่อน generate QA HTML/AI testset เพื่อให้ MD↔QA↔testset count ตรง.
3. **[INFO · carry OQ ไม่บล็อก]** OQ ที่ยังเปิด (business decision ไม่ใช่ requirement หล่น): OQ-CN-01 (legal reason master + จุดยืน trade-discount) · OQ-CN-02 (revise path DN vs CN) · OQ-CN-03 + CSQ FC (refund → RV/PV) · OQ-CN-04 (จุดตัดวงเงิน 50k/300k + tax month) · **OQ-AR-06 role-ids [ASSUMED]** (`role-mgr-acc` ยังไม่มีใน master). ทั้งหมด NO-block ต่อ FRD/TC แต่ dev ต้องได้คำตอบก่อนตั้งค่าจริง (DOA/CSQ/doccfg).

---

## 7 · Diff vs R1 (`_COVERAGE_REPORT.md`)

- **ปิดแล้ว:** R1 ตรวจ HTML hooks/surface (list/wizard/view/pdf/modals + FN handler เดินได้) → PASS. R2 ไม่ตรวจซ้ำ.
- **เพิ่มใน R2:** FN↔TC ledger 22/22 · Rule↔TC 15/15 · Declaration↔FRD sync (4 ท่อ) · focus BR-11/BR-12/guards/legal_basis/LD-05 มีทั้ง rule + TC.
- **เกิดใหม่:** 2 WARN doc-drift ใน 06_TESTS §6.8/§6.2 (cosmetic · ไม่บล็อก).

---

**Bottom line:** FRD Pack + Test Cases ผูก contract ครบก่อนส่ง dev — **PASS**. แก้ 2 WARN doc-drift ใน 06_TESTS ให้เนียน + ให้ BA เคลียร์ OQ ที่ dev ต้องใช้ตั้งค่าจริง (โดยเฉพาะ role-ids OQ-AR-06).
