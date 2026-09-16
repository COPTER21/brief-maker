# PROPOSALS / ปิดงาน — F-WH-STKADJ (Stock Adjustment · ปรับยอดสต๊อก · F082)

> WF-01 step 12 · ปิดงานรอบ pipeline `6→12` · วันที่ 2026-09-16
> สถานะ: **ครบ 12 step — หยุดรอสั่ง commit** · ยังไม่ commit
> Gate ล่าสุด (บน bytes สุดท้ายของ `.html`): qc-ux **PASS** (BLOCK=0 · 5 WARN cosmetic) · coverage R1 **PASS** FN 55/55 · coverage R2 **PASS** (0 BLOCK · 3 WARN doc-drift) · e2e **58/58** FN 55/55

---

## A. เรื่องที่ต้องให้ BA/PM เคาะ (สำคัญ — ยกเป็น OQ ไม่เลือกข้างเอง)

### A1. 🔴 BA reference declaration brief เก่าค้าง ขัดมติ re-gate ของ BA เอง (2 จุด)
ตอนรัน declaration หลัง step 7 เจอว่า **ไฟล์อ้างอิงของ BA ใน `5_DECLARATIONS/` ยังเป็นสถานะก่อน re-gate** (FIX-02/FIX-03 ที่ผู้ใช้เคาะ "เชื่อ BA" ไปแล้ว) — pack ของเรายึด **มติล่าสุดที่ล็อก** และยกเป็น OQ ให้ BA อัปเดตไฟล์ตัวเอง (ไม่เลือกข้างเงียบ):

| OQ | ไฟล์ BA ที่เก่าค้าง | เขียนไว้ (เก่า) | มติล่าสุดที่ถูกต้อง | ของเรายึด |
|---|---|---|---|---|
| **DOA-Q3** | `5_DECLARATIONS/DOA_BRIEF_F-WH-STKADJ.md` §2/DOA-Q3 | กลับรายการ **ไม่** ผ่าน DOA (ใช้ warehouse-chief + เหตุผลบังคับ) | **FIX-03 / FRD LD-05**: กลับรายการ **ผ่าน DOA** ตาม tier มูลค่าตัวเอง (ไม่ auto-post) | ผ่าน DOA ✅ |
| **NTF-Q5** | `5_DECLARATIONS/NTF_BRIEF_F-WH-STKADJ.md` | `adj_cancelled` trigger รวม `อนุมัติแล้ว→ยกเลิก` | **BR-27 / FIX-02**: ยกเลิกได้เฉพาะ `ร่าง/รออนุมัติ` · อนุมัติแล้วยกเลิกไม่ได้ (ต้องกลับรายการ) | draft/pending only ✅ |

→ **ขอ BA อัปเดตไฟล์ reference 2 ตัวใน `5_DECLARATIONS/` ให้ตรงมติ re-gate** (pack ของเราถูกแล้ว แต่ 2 เอกสารในแพ็กจะขัดกันจนกว่า BA จะแก้)

### A2. Coverage R2 — 3 WARN (doc cross-reference drift · ไม่บล็อก · แก้ตอน doc-cleanup)
| WARN | รายละเอียด | ผลกระทบ |
|---|---|---|
| **W-1** | FN↔TC ledger อ้าง `TC-W204` ที่ไม่มีจริง (header ข้าม W203→W205) — FN-06 ยัง cover ด้วย TC-W201 | ไม่มี coverage gap · แค่ลบ cite ที่ค้าง |
| **W-2** | `VR-16`/`VR-17` ถูกอ้างใน FRD `07_LOCKED_DECISIONS` (LD-06) + INDEX ("17 VR") แต่ `05_RULES §5.4` นิยามแค่ `VR-01..15` — BR-27/cancel-reason cover ด้วย VR-14+BR-27 อยู่แล้ว | ไม่มี rule หาย · แก้ cross-ref หรือเพิ่มนิยาม VR-16/17 |
| **W-3** | ตาราง coverage-summary ใน testcases อ้าง W2=14 เคส (จริง 13 · ผลพวง W-1) → sub-table รวม 117 แต่ header จริง 116 | ตัวเลขสรุปคลาด 1 |

→ ทั้งหมด non-blocking · แนะนำแก้รอบ frd-generator/tc รอบหน้า หรือ doc-cleanup ก่อนส่ง dev

### A3. เรื่องที่ BA รับทราบ/รับไว้แล้วในรอบ manual-test (บันทึกไว้กันลืม)
- **PREBRIEF §5.1/S-09/FN-24 reconciled แล้ว** (ผู้ใช้อนุญาตให้ผมแก้ 2026-09-15): ยกเลิกเฉพาะร่าง/รออนุมัติ + เพิ่ม **BR-27**
- **FIX-04 edge เพิ่มแล้ว**: PREBRIEF §3.1 (field แหล่งที่มา + `ref_count_doc`), S-26, **BR-26**, §9 edge-in F084/F086, **FN ใหม่ FN-52** → FUNCTION_CHECKLIST = **55 FN**
- **Filter toolbar** จัด 2 แถว + คอลัมน์ 9 ช่อง (เพิ่ม ผู้จัดทำ) → qc-ux WARN (ต่างจาก Lane iron #106 toolbar แถวเดียว) — **BA รับเป็น WARN** (ผู้ใช้ยืนยัน layout นี้)
- **DOA threshold (20k/200k/1M)** → เคาะผ่าน `doa-declaration` (ผู้ใช้เลือกที่ kickoff: "รัน /skill doa แล้วเอามาอ้างอิงตามนั้น")

---

## B. Open Questions จาก declaration (ส่งให้ owner ปลายทาง — dev เอาไปตั้งค่าจริง ห้ามเดา)

**DOA** (owner: Strike + F-DLG-001)
- DOA-Q1 ค่าจริง cut-point 20k/200k/1M + ควรอยู่ต่ำกว่า RTV/PO ไหม `[DEFAULT — รอยืนยัน]`
- DOA-Q2 base = Σ|abs| **ล็อกแล้ว (LD-04)** · เลข cut-point ยัง tunable (Strike + บัญชี)
- DOA-Q4 per_dept vs merged (ตอนนี้ merged) `[DEFAULT]`
- DOA-Q5 write-off ของเสีย ต้องบังคับ tier บัญชีเสมอไหม ไม่ว่ามูลค่า (Strike + บัญชี)
- DOA-Q6 DOA `role-*` master ไม่มีใน lane นี้ → slot→role-id mapping (ผจก.บัญชี/ผอ.สายงาน) ต้องให้เจ้าของ F-DLG-001 เคาะ
- (DOA-Q3 = ดู A1)

**DOCCFG** (owner: Strike + F-DOCCFG + บัญชี)
- DOC-Q1 ออกเลขที่ submit (ปัจจุบัน) vs ย้ายไป `ผ่านรายการ` เพื่อ no-gap
- DOC-Q2 scope global vs branch (1 ADJ = 1 คลัง · BR-04)
- DOC-Q3 internal-only จริง vs เปิด `sent_external` ให้ผู้ตรวจภายนอก
- DOC-Q4 write-off ต้อง retention แยก/นานกว่าไหม
- DOC-Q5 กลับรายการใช้ series `ADJ` เดิม (ปัจจุบัน) vs prefix แยก `ADJR`
- **DOC-Q6 (พบใหม่)** BA brief §3 วาง `store('approved_final')` ที่ state `อนุมัติแล้ว` แต่ FRD `03_LOGIC` FN-13 (`postDocument`) เรียกตอน `approved→posted` → **pack ยึด FRD (posted)** · ขอ Strike+F-DOCCFG ยืนยัน trigger จริง (approved vs posted)

**NTF** (owner: BA + F-NOTIFY + บัญชี)
- NTF-Q1 เลข "high value" จริงใน NC rules สำหรับ `adj_high_value_submitted`
- NTF-Q2 บัญชีรับ `adj_posted` ทุกใบ vs เฉพาะเกิน threshold (กัน noise)
- NTF-Q3 `adj_reversed` แจ้งทุก slot อนุมัติของใบเดิมไหม (รอบนี้ = yes)
- NTF-Q4 aged-pending reminder จงใจ **ไม่** ประกาศ (เป็นของ DOA escalate) — ขอยืนยัน
- (NTF-Q5 = ดู A1)

**CSQ / 7C** (owner: BA + F-CSQ-01 + internal audit)
- CSQ-Q1 แยก event increase/decrease vs event เดียว
- CSQ-Q2 เจ้าของ **AC** (JE) เป็น StockAdj หรือ GL เมื่อ W5 มา (กัน double-count) — ตอนนี้ JE = mock `FWD-WIRE`
- CSQ-Q3 cost basis: Item Master (mock) vs FIFO/avg จาก Valuation (W5)
- CSQ-Q4 quarantine/damage adjustment ควรเป็น **SecC** (fraud risk) ไหม
- CSQ-Q5 register แถวเปล่าสำหรับ no-effect `adj_cancelled` vs ข้าม
- **CSQ-Q6 (พบใหม่)** `event_id` ใช้ `adj_posted_increase` (ตาม FRD FN emit) แต่ `references/csq-contract.md` ไม่มีในสกิลที่ติดตั้ง → verify กับ catalog F-CSQ-01 ไม่ได้ (ถ้า catalog ใช้ dotted-prefix `adj.posted` ต้อง rename) — tag `[ASSUMED]`

**FRD (15 OQ ใน `00_OVERVIEW §0.8` · non-blocking · มี owner/แผนปิดครบ)**
- DOA cut-offs `[DEFAULT — รอยืนยัน]` · R26 threshold · R27 valuation basis · reversal-DOA tier (Q13) · 3 ตัว `[AI-DEFAULT]` Phase-2.5 (optimistic-lock / idempotency / permission-recheck = OQ-08/09) · OQ-10 ยืนยันไม่มี Restricted fields — **ต้องปิดก่อน go-live แต่ไม่บล็อกส่งต่อ**

**UI Brief drift (yield ให้ BA)**
- OQ-ADJ-01 reversal fast-track ต้องมี ruling (`doReverse`) · OQ-ADJ-02 CSQ pipe on post (`doPost`)

---

## C. Declaration รอบนี้ (C3.10)
เลือกไว้ตั้งแต่ `/kickoff` = **doa · ntf · csq · doccfg** (4 ตัว · สั่งแล้ว) — รันหลัง step 7 ครบทั้ง 4:

| Brief | ไฟล์ | verdict | สาระ |
|---|---|---|---|
| DOA | `DOA_BRIEF_F-WH-STKADJ.md` | PASS (G2–G7) · G1 = role master absent (OQ) | tier Σ\|abs\| 20k/200k/1M · reversal ผ่าน DOA · SoD · real-person slot |
| DOCCFG | `DOCCFG_BRIEF_F-WH-STKADJ.md` | PASS | doc_type `ADJ` · `ADJ-YYYY-NNNN` ค.ศ. · snapshot `approved_final` |
| NTF | `NTF_BRIEF_F-WH-STKADJ.md` | PASS | 6 feature events · DOA events excluded ถูกต้อง |
| CSQ | `CSQ_BRIEF_F-WH-STKADJ.md` | PASS (พร้อม register) | 5 EC events · OC/DC/SC ไม่ประกาศซ้ำ (กัน 422) · AC รอ W5 |

---

## D. PENDING_REGISTRY — 2 รายการใหม่ (C3.8 · แก้สำเนา feature + เพิ่ม uikit check + prove-by-revert แล้ว)
ลงทะเบียนที่ `outputs/_SHARED/DESIGN_SYSTEM_PENDING.md`:
- **DSP-05** combopop จมใต้ modal: `.combo-pop/.menu-fixed` z=`--z-portal`(60) < modal(70) → dropdown ผู้อนุมัติในกล่องส่งอนุมัติจมใต้ modal · แก้: เพิ่ม `--z-combopop:75` · uikit `assert_pop_above_modal` (DSP-01 family)
- **DSP-06** scroll-lock leak: navigate ไป view ใหม่ก่อน `closeModal`/`openViewDrawer` ไม่ release trap เดิม → `_trapStack` ค้าง → `body.is-overlay-open` ค้าง scroll ล็อกหลังปิด · แก้: `releaseFocus()` ใน openViewDrawer + reverse callback order · uikit `assert_no_scroll_lock_leak`

## E. ของที่ควรส่งต่อ feature อื่น
- **F083 Stock Transfer**: ใช้ pattern เดียวกัน → ควรเรียก `assert_no_native_dialog` · `assert_pop_above_modal` · `assert_no_scroll_lock_leak` ใน e2e ด้วย
- `ref_count_doc` (display-only) ชี้ **F084/F086** (ใบนับ/นับรอบ) — ยังเป็น backlog ยังไม่มีจอ (simulate ใน XT)

---

## F. ไฟล์ส่งมอบ (path เต็ม — เปิดใบเดียวจบ อยู่นอกสุด)
```
outputs/F-WH-STKADJ/
├─ F-WH-STKADJ.html                         ต้นแบบ (source of truth · 167KB)
├─ BRD_F-WH-STKADJ.md / .docx                BRD (APPROVED)
├─ FRD_Pack/  (00_OVERVIEW..07_LOCKED + INDEX)  FRD 9 ไฟล์ (เป็นชุด · ในโฟลเดอร์)
├─ UI_BRIEF_ปรับยอดสต๊อก.md                    UI Brief (verifier PASS)
├─ DOA_BRIEF / DOCCFG_BRIEF / NTF_BRIEF / CSQ_BRIEF_F-WH-STKADJ.md   declaration 4 ตัว
├─ testcases-ปรับยอดสต๊อก.md                   AI Test Case (116 เคส · FN 55/55)
├─ ปรับยอดสต๊อก HTML Testcase.html            🔴 UAT (เปิดทดสอบ · 96 เคส Lite)
├─ FEATURE_TLDR_F-WH-STKADJ.html              หน้าปกสรุป (ELI5)
├─ _UX_CHECK_REPORT.md                        qc-ux PASS
├─ _COVERAGE_R1.md / _COVERAGE_R2_REPORT.md   coverage R1/R2 PASS
├─ _coverage_wf_ticks.md                      WF ticks
├─ _e2e/ (e2e-adj.py)                         e2e 58/58 (ในโฟลเดอร์)
├─ _print/ (ADJ_sample.pdf ฯลฯ)               เอกสารพิมพ์ A4 (ในโฟลเดอร์)
└─ _qa/ (cases.json · shot-spec)              UAT set (ในโฟลเดอร์)
```

---
**สถานะ: ครบ 12 step · หยุดรอสั่ง commit** (C3.3 จุดหยุด 3 · ห้าม commit เอง)
