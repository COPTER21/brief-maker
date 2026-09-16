# _COVERAGE_R2_REPORT — F082 F-WH-STKADJ ใบปรับยอดสต๊อก (Stock Adjustment)

> **Gate:** qc-coverage-checker · **ROUND 2** (FRD Pack + Test Cases · ก่อนส่ง dev) — ไม่ตรวจ HTML ซ้ำ (รอบ 1 PASS แล้ว ที่ `_COVERAGE_R1.md`)
> **Date:** 2026-09-16 · **Checked by:** qc-coverage-checker (read-only · ไม่แก้ artifact · ไม่ commit)
> **Contract:** FUNCTION_CHECKLIST 55 FN · PREBRIEF (S-01..S-26 · BR-01..BR-27) · Declaration briefs (DOA/NTF/CSQ/DOCCFG) · BA re-gate 2026-09-15 (FIX-02/03/04)
> **Artifacts:** FRD_Pack/ (00–07 + INDEX) · testcases-ปรับยอดสต๊อก.md (116 TC)

---

## ⭐ VERDICT: **PASS** (0 BLOCK · 3 WARN — เอกสาร cross-reference drift ล้วน ไม่ใช่ coverage gap)

- **FN ↔ TC ledger: 55/55** ทั้งสองทิศ — ทุก FN มี rule/logic home (05_RULES/03_LOGIC) **และ** ≥1 TC ที่มีจริง · ไม่มี orphan FN · ไม่มี orphan TC ที่ลอย
- **BR-01..BR-27 (+BR-17.1): 28/28** อยู่ใน 05_RULES §5.1 เนื้อหาตรง ไม่เจือจาง + มี TC ทุกข้อ
- **VR (ที่นิยามไว้) VR-01..VR-15: 15/15** อยู่ใน 05_RULES §5.4 + มี TC ทุกข้อ
- **Declaration coverage: 4/4** — DOA · NTF · CSQ · DOCCFG brief ครบ · chip = detect (ไม่มี DIVERGENCE) · sync-read FRD · ไม่ hardcode
- **BA-locked decisions (FIX-02/03/04): traceable end-to-end ครบ 3/3**
- **Negatives หมวด 7 (prove-absent): 9/9** documented as cut + มี render-and-assert TC

WARN ทั้ง 3 เป็น **cross-reference drift** (TC id ที่อ้างถึงแต่ไม่มี · VR id ที่อ้างถึงแต่ไม่นิยาม · count-summary คลาดจากจำนวนจริง 1 เคส) — ทุก item ที่ drift ยัง **มี coverage สำรองครบ** จึงไม่เป็น BLOCK แต่ควรเก็บก่อน/ตอนส่ง dev เพื่อความสะอาดของ ledger

---

## 1. Diff กับรอบ 1 (`_COVERAGE_R1.md`)

| ประเด็น | รอบ 1 (HTML) | รอบ 2 (FRD + TC) |
|---|---|---|
| Verdict | PASS (จาก prior BLOCK ที่ BR-26 · RESOLVED แล้ว) | **PASS** |
| จุดสนใจ | BR-26 enforce ใน HTML 2 guard (L898+L916) · e2e 58/58 · FN 55/55 hooked | rule ทุกข้อลง 05_RULES · FN↔TC ledger 55/55 · declaration sync |
| Gap ปิดจากรอบ 1 | BR-26 (prior BLOCK) | ยืนยันตกผลึกใน 05 BR-26/VR-05 + TC-W106/W107/V02/NG10 ✓ |
| WARN คงค้างจากรอบ 1 | HTML preflight comment "54/54" stale (cosmetic · ไม่ render) | ไม่ใช่ item รอบ 2 (แตะ .html ต้องวน step 3·4·5 · C3.2) — ปล่อยตามเดิม |
| WARN เกิดใหม่รอบ 2 | — | W-1 (TC-W204 stale cite) · W-2 (VR-16/17 อ้างแต่ไม่นิยาม) · W-3 (W2 count 14≠13) |

---

## 2. FN ↔ TC Ledger (55/55 · forward + reverse)

**Forward (ทุก FN → rule home + TC):** ครบ 55/55 — ตรวจทีละข้อกับ FUNCTION_CHECKLIST 8 หมวด (FN-01..FN-52 ต่อเนื่อง + FN-90/91/92) เทียบ ledger ใน testcases §Coverage Ledger + 05_RULES BR mapping. ทุก FN มี BR/VR/§ home และ TC id ที่ **มีอยู่จริง** (verify ด้วยการ enumerate `#### TC-*` headers ทั้ง 116 หัว).

ตัวอย่าง evidence (จุดสำคัญ):

| FN | Rule home (05_RULES/03_LOGIC) | TC | สถานะ |
|---|---|---|---|
| FN-08/43 (Σabs vs สุทธิ ฐาน DOA) | BR-09 · §5.4 computed (abs_total) | TC-W209, TC-W406 | ✓ |
| FN-17/42 (slot คนจริง ห้าม role ID) | BR-10 · VR-12 | TC-W404, TC-W503, TC-W405 | ✓ |
| FN-24 (ยกเลิกเฉพาะ ร่าง/รออนุมัติ) ★FIX-02 | BR-27 · §5.2 · VR-14 | TC-CX01/CX02/CX03 | ✓ |
| FN-25/44 (posted→reversal ผ่าน DOA) ★FIX-03 | BR-17/17.1/18 | TC-RV01/RV02/RV03/RV04 | ✓ |
| FN-27 (ตรวจยอดซ้ำก่อน post) | BR-15 · EC-04 | TC-PO03, TC-PO04 | ✓ |
| FN-52 (count-doc trace display-only) ★FIX-04 | BR-26 · VR-05 | TC-W106/W107, TC-V02, TC-NG10 | ✓ |
| FN-39 (audit append-only) | BR-25 | TC-HS03 | ✓ |
| FN-90/91/92 (general) | §6.1 · BR-16/17 · §5.1 | TC-L03/L04, TC-GN05, TC-W504/GN06 | ✓ |

**Reverse (ไม่มี TC ลอย):** TC ที่ไม่ได้อยู่ใน FN-ledger (V01/V03/V06 · W108 · W214 · AP05 · PO05 · PD04 · RV02/RV04 · NG10 · GN02-04/07/08 · XT01-11 · SL01-10) — **ตรวจแล้วทุกตัว trace กลับ** VR/BR/EC/Error/XT/LOCK/cross-cutting ledger ใน testcases §Coverage Ledger → เป็น coverage เสริม ไม่ใช่ orphan

**สรุปนับ:** headers จริง = **116 TC** (ตรงกับ Meta "116") · ครอบ 55 FN + 28 BR + 15 VR + 7 EC + 11 XT + 10 LOCK

---

## 3. Declaration Coverage (Phase 0b · 4/4 · ไม่มี DIVERGENCE)

| ท่อ | chip (PREBRIEF/CONTEXT) | brief present | sync-read FRD | ไม่ hardcode | event/slot map กลับ FN/S | Verdict |
|---|---|---|---|---|---|---|
| **DOA** | มีวงเงิน (Σ\|มูลค่า\|) · pending_approval | ✅ `DOA_BRIEF` 24.1K | 05 BR-09/10/17 · 03 FN-08/09/14 · 07 LD-04/05/06 · 02 API-10 | ✅ slot คนจริง ห้าม role ID · matrix ไปตั้งที่ DOA กลาง | Action①②③ ↔ S-07/08/09/10 · FIX-03 reversal ผ่าน DOA | ✅ |
| **NTF** | 🔔 ntf | ✅ `NTF_BRIEF` 13.6K | 03 state machine emit points · 05 §5.5 · 06 §6.5 | ✅ ยิงผ่าน ENG-NOTIFY · ไม่ประกาศ doa_pending/result/escalate | 6 event ↔ FN-13/11/12/08 · S-07/09/10/15/17/19 · XT-03/04/06/07/08 | ✅ |
| **CSQ** | ◆ csq | ✅ `CSQ_BRIEF` 18.8K | 03 FN-13/11/14 emit · 05 S-07/09/10/17 · 04 §4.2 | ✅ ไม่ประกาศ OC/DC-document/SC (กัน reject 422) | 5 EC event ↔ FN-13(post +/−/writeoff)/14(reversed)/11(cancelled no-effect) · XT-04/05/06/07 | ✅ PASS (self-gate) |
| **DOCCFG** | doc ADJ (Pattern Q · เลขรัน) | ✅ `DOCCFG_BRIEF` 10.2K | 05 BR-21 · 02 API-05 · 07 LD-05 | ✅ ADJ-YYYY-NNNN จาก ENG-DOC-NUM · ห้าม format/+1 เอง | doc_type ADJ ↔ FN-08/20 · ออกตอนส่งอนุมัติ · ใบกลับได้เลขใหม่ | ✅ ไม่ชน registry |

**Known stale-reference OQs (pass-through · ไม่ใช่ coverage gap — ตามที่ระบุใน task):**
- **DOA-Q3** — reference file เดิมเขียนว่า reversal "ไม่ผ่าน DOA" แต่ brief แก้ตาม locked **FIX-03/LD-05** (reversal ผ่าน DOA · ไม่ auto-post) แล้ว · DOA brief §2 Action③ + §8 note ระบุชัดว่าแก้จุด reference เก่า → **OQ pass-through** ให้ owner (Strike) รับทราบ ไม่บล็อก
- **NTF-Q5 / NTF-Q4** — escalate ใบค้างอายุเป็นของ DOA engine (BR-20 NC rules) · brief ไม่ประกาศซ้ำ → **OQ pass-through**

ไม่มี chip≠detect → **ไม่มีหมวด DIVERGENCE**

---

## 4. BA-Locked Decisions — traceable end-to-end (3/3)

| มติ (BA re-gate 2026-09-15) | 05_RULES | 07_LOCKED | 06_TESTS AC | testcases TC | Declaration | สถานะ |
|---|---|---|---|---|---|---|
| **FIX-02 / BR-27** — ยกเลิกเฉพาะ ร่าง/รออนุมัติ · ไม่มี approved→cancelled | BR-27 · §5.2 state machine · VR-14 · Error `ERR_CANCEL_NOT_ALLOWED` | LD-06 | AC-17 | TC-CX01/CX02/CX03 (+ TC-RV01 guard) | NTF `adj_cancelled` (draft/pending only) · CSQ no-effect | ✅ ครบสาย |
| **FIX-03 / BR-17·17.1·18** — reversal สร้างใบใหม่ วิ่ง DOA ตาม abs · ไม่ auto-post | BR-17/17.1/18 · §5.2 · Error `ERR_ALREADY_REVERSED` | LD-05 | AC-18 | TC-RV01/RV02/RV03/RV04 | DOA Action③ (matrix เดียวกัน · abs ของใบกลับ) · NTF `adj_reversed` · CSQ `adj_reversed` avoided | ✅ ครบสาย |
| **FIX-04 / BR-26 · FN-52** — count-doc trace display-only (source=count → ref บังคับ · ไม่เปิดหน้าใบนับ) | BR-26 · VR-05 · Error `ERR_COUNT_DOC_REQUIRED` | LD-07 | AC-24 | TC-W106/W107 · TC-V02 · TC-NG10 (display-only prove) | — | ✅ ครบสาย |

---

## 5. Negatives หมวด 7 (prove-absent · render-and-assert · 9/9)

> WF-01 C3.5: หมวด 7 = negative 7 FN (ไม่ใช่ FN-40) — FN-40 ที่นี่เป็น FN บวก (เหตุผล "อื่น ๆ" บังคับคำอธิบาย → TC-W303) ✓ mapping ถูก

| FN (negative) | ประกาศ "ไม่รองรับ" | Rule (05_RULES) | 06_TESTS §6.7 | TC (prove-absent) |
|---|---|---|---|---|
| FN-32 in-transit ไม่โผล่ | checklist ✓ · BR-13 | BR-13 (negative) | NEG-01 | TC-NG01 (ค้น TR-* → ไม่เจอ) |
| FN-35 ไม่มีนับสต๊อก | checklist ✓ · [OQ-STK-01 backlog] | BR-24 (negative) | NEG-02 | TC-NG02 |
| FN-36 ไม่มี bin ปลายทาง/ย้าย | checklist ✓ · [F-WH-STKTRF] | BR-05 (negative) | NEG-03 | TC-NG03 |
| FN-46 quarantine ปรับได้ ย้ายออกไม่ได้ | checklist ✓ | BR-12 | NEG-04 | TC-NG04 |
| FN-47 ไม่มีช่องเลขเอง/ตั้งเลขรัน | checklist ✓ · [GOLDEN §3] | BR-20/21 | NEG-05 | TC-NG05 |
| FN-48 ไม่มี threshold/% | checklist ✓ | BR-20 (negative) | NEG-06 | TC-NG06 |
| FN-49 ไม่มีคอลัมน์ VAT/ส่วนลด | checklist ✓ · §3.6 | §3.6 | NEG-07 | TC-NG07 |
| FN-45 ไม่มีปุ่มลบ/แก้ movement | checklist ✓ | BR-16 (append-only) | NEG-08 | TC-NG08 |
| FN-50 sidebar module map | checklist ✓ | OB-14 | NEG-09 | TC-NG09 |

ทุกเคส render จริงแล้ว assert ว่าไม่มีบนจอ (ไม่ใช่แค่ grep code) ✓

---

## 6. WARN List (เรียงตามความเสี่ยง · ทั้งหมด NON-BLOCKING · เก็บก่อน/ตอนส่ง dev)

| # | อะไร drift | อยู่ที่ไหน | ทำไมไม่ BLOCK | ต้องแก้ยังไง |
|---|---|---|---|---|
| **W-1** | FN-ledger อ้าง **TC-W204** ที่ไม่มีอยู่ (header จริงข้ามจาก TC-W203 → TC-W205) | `testcases-ปรับยอดสต๊อก.md` §Coverage Ledger บรรทัด `FN-06 … TC-W201, TC-W204` | FN-06 (มูลค่า=ผลต่าง×ต้นทุน) ยังมี **TC-W201** ที่ครอบจริง → coverage ครบ | ลบ `TC-W204` ออกจากบรรทัด FN-06 (หรือเพิ่มเคส W204 จริงถ้าตั้งใจแยก) |
| **W-2** | อ้าง **VR-16 / VR-17** ที่ไม่ได้นิยามใน 05_RULES §5.4 (ตารางจริงหยุดที่ VR-15) | `07_LOCKED_DECISIONS` LD-06 ("05 BR-27/**VR-16**") · `INDEX.md` ("VR-01..**17**" / "**17** VR") | BR-27/cancel-reason ถูกครอบด้วย **VR-14** (reason required) + BR-27 อยู่แล้ว → ไม่มี rule หาย | เปลี่ยน cross-ref เป็น VR-14/BR-27 หรือเพิ่มนิยาม VR-16/17 ใน §5.4 ให้ตรง |
| **W-3** | count-summary ระบุ **W2 = 14 เคส** (TC-W201..W214) แต่จริง **13** (W204 หาย) · sub-total ตาราง = 117 แต่ headers จริง = 116 | `testcases` §Coverage ตาราง group (บรรทัด W2) | รวมยัง = 116 ตรง Meta · เป็นผลพวงของ W-1 | แก้พร้อม W-1 (นับ W2 = 13 หรือเติมเคส W204) |
| (ref) | HTML preflight comment "FN wired: 54/54" stale (รอบ 1 · cosmetic) | `F-WH-STKADJ.html` L1154 (comment · ไม่ render) | ไม่ใช่ round-2 artifact · แตะ .html = ต้องวน step 3·4·5 (C3.2) | เก็บตอนแตะ HTML รอบหน้าเท่านั้น (อย่าแตะเพื่อสิ่งนี้อย่างเดียว) |

---

## 7. Coverage Matrix (สรุป)

| Item class | นับ | HTML (R1) | FRD (05/03) | TC | ผล |
|---|---|---|---|---|---|
| FN-01..52 + FN-90/91/92 | 55 | ✓ (R1 55/55) | ✓ BR/VR/§ home | ✓ ≥1 TC (มีจริง) | **55/55** |
| BR-01..27 + BR-17.1 | 28 | ✓ | ✓ 05 §5.1 | ✓ | **28/28** |
| VR (นิยามไว้) VR-01..15 | 15 | — | ✓ 05 §5.4 | ✓ | **15/15** |
| EC-01..07 | 7 | — | ✓ 05 §5.5 | ✓ TC-GN/PO/V/W | **7/7** |
| XT-01..11 | 11 | — | ✓ 06 §6.9 | ✓ TC-XT01..11 | **11/11** |
| DECL (DOA/NTF/CSQ/DOCCFG) | 4 | ✓ (R1 slot/marker) | ✓ sync-read | ✓ XT/AP/CX/RV/W | **4/4** |
| LOCK-01..10 | 10 | ✓ | ✓ 07 §7.0 | ✓ TC-SL01..10 | **10/10** |
| Negative (หมวด 7) | 9 | ✓ | ✓ negative BR | ✓ TC-NG01..09 | **9/9** |

---

## 8. Checker self-gates

- [x] ทุก ✓ มี evidence ระบุตำแหน่ง (ไฟล์ + §/BR/VR/FN + TC id) — ไม่มีช่องเดา
- [x] ไม่ invent เกณฑ์นอก contract — เกณฑ์มาจาก FUNCTION_CHECKLIST + PREBRIEF + 05_RULES + declaration briefs
- [x] item ที่ตรวจไม่ได้ = ระบุชัด (ไม่มี — ครบทุก artifact รอบ 2)
- [x] scope creep — ไม่พบ (ของใน "สิ่งที่ไม่รองรับ" ถูกยืนยันเป็น negative TC ไม่หลุดเข้ามา)
- [x] BLOCK เมื่อ block-severity ไม่ครอบ — ไม่มี block rule/BA-locked หายสักตัว → ไม่ BLOCK
- [x] Declaration coverage ตรวจครบ 4 ท่อ — ไม่มี chip≠detect
- [x] Read-only · ไม่แก้ HTML/FRD/TC/skills · ไม่ commit

**สรุป: PASS — พร้อมส่ง dev.** WARN 3 ข้อเป็น ledger/cross-ref hygiene ล้วน (ทุกจุดยังมี coverage สำรอง) เก็บได้ในรอบแก้เอกสาร ไม่ต้องวน gate ใหม่
