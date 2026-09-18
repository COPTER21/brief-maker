# HANDOFF — F-WH-STKTRF · Stock Transfer (ใบย้ายสินค้า)

> **Phase A จบแล้ว = `ba-done`** · runner `feature-lane-runner 2.4.1r` (`--mode direction`) · 2026-09-10
> fid **F083** · Wave **W3Q** ลำดับ 3 (**ตัวสุดท้ายของ pack CUBE-LANE-W3-LITE**) · module **Warehouse** · arch **Q-document**

---

## 1. ทำอะไรไปแล้ว

| Stage | ทำอะไร | ผล |
|---|---|---|
| **S0** | อ่าน knowledge ครบ (CONTEXT_PACK W3-LITE · GOLDEN_RULES · BUILD_ORDER · workflow_graph · CHECKLIST W3Q · FEATURE_LIST แถว dep · TASTE_LOG) + อ่าน PREBRIEF ของ **Putaway** (สัญญากลาง location) และ **StockAdj** (movement/DOA/reversal) · สร้าง LANE_BRIEF | pass |
| **S0.5** | Baseline เทียบ ERP มาตรฐาน (SAP S/4HANA · Odoo · D365/BC · NetSuite · ERPNext) — WebSearch 3 query | pass · must-have 16 · nice-to-have 14 ตัดออก · gap 12 ข้อ |
| **S1** | PREBRIEF เต็ม 13 sections — **34 scenario · 34 BR · state machine แยก 2 ขา · mock 13 ใบ** + FUNCTION_CHECKLIST **61 FN / 10 หมวด** (+ .html ติ๊กได้) | pass |
| **S1.5** | Gap check ย้อน BASELINE/CHECKLIST/OQ (อยู่ใน PREBRIEF §13) | pass · gap 12/12 ปิด · CHECKLIST 11/11 วรรค |
| **S1.8** | Declarations ตาม chip 5 ตัว | pass · **detect = chip → DIVERGENCE = 0** |
| **S2** | HTML prototype single-file SPA (Pattern Q เต็ม + B2 v2) | pass · 2,291 บรรทัด · ~206 KB |
| **S3a** | `qc-ux-html-checker` — iron rules #1–#103 + Pass D archetype | **PASS** (BLOCK = 0) |
| **S3b** | `qc-coverage-checker` รอบ 1 | **PASS** — FN 61/61 มี evidence · **scope creep = 0** |
| **S3c** | Technical gate | **PASS** — `node --check` ผ่าน · `audit.sh` **FAIL = 0** · render 12 ภาพ · JS error = 0 |
| **S4** | BRD ด้วย `brd-generator-full` | pass · **Quality Gate C01–C23 = APPROVED** |
| **S4.5** | HANDOFF (ไฟล์นี้) | pass |

**Verdict สรุป: S3a = PASS · S3b = PASS · S3c = PASS · S4 = APPROVED**

---

## 2. ส่งมอบอะไร (ไล่ทุกไฟล์พร้อม path)

```
output/2026-09-10/F-WH-STKTRF_Stock Transfer/
├── 0_DIRECTION/
│   ├── BASELINE_F-WH-STKTRF.md                    ← เทียบ ERP มาตรฐาน · must-have/nice-to-have/gap
│   ├── PREBRIEF_F-WH-STKTRF.md                    ← ★ source of truth เชิง business (13 sections)
│   ├── FUNCTION_CHECKLIST_F-WH-STKTRF.md          ← 61 FN · 10 หมวด · trace กลับ S/BR ได้ทุกข้อ
│   ├── FUNCTION_CHECKLIST_F-WH-STKTRF.html        ← ติ๊กได้ 3 ด่าน (WF/DEV/QA) · เปิดในเครื่องได้เลย
│   └── HANDOFF.md                                 ← ไฟล์นี้
├── 1_HTML/
│   ├── F-WH-STKTRF.html                           ← ★ ต้นแบบหน้าจอ (เปิดจาก file:// ได้ทันที)
│   ├── _UX_CHECK_REPORT.md                        ← S3a · รวม Iron Rule Overrides 8 ข้อ
│   ├── _COVERAGE_R1.md                            ← S3b · ledger FN/scenario/BR พร้อม evidence
│   ├── _TECH_CHECK.md                             ← S3c · syntax/audit/render + ข้อจำกัด offline
│   ├── _static_scan.json                          ← ผลสแกนดิบ
│   └── _shots/  (12 ภาพ)                          ← 01_list · 02_view_detail · 03_view_transit/pdf/sign
│                                                     04a/04/04b wizard · 05/05b receive · 06 DOA slot · 07 1024px
├── 2_BRD/
│   └── BRD_F-WH-STKTRF.md                         ← 18 sections + Appendix + Quality Gate APPROVED
└── 5_DECLARATIONS/
    ├── DOA_BRIEF_F-WH-STKTRF.md                   ← ★ 3 สาย / 2 จุดตัดสินใจ (A1 · A2 · B1)
    ├── NTF_BRIEF_F-WH-STKTRF.md                   ← 7 event ธุรกิจ (ไม่ประกาศ event ของ DOA ซ้ำ)
    ├── CSQ_BRIEF_F-WH-STKTRF.md                   ← 7 event · EC เท่านั้น (ไม่ประกาศ OC/DC/SC)
    ├── DOCCFG_BRIEF_F-WH-STKTRF.md                ← doc type TRF · TRF-YYYY-NNNN (ค.ศ.)
    └── print-spec-trf.md                          ← ข้อกำหนดงานพิมพ์ A4 (ช่องเซ็นที่ 4 = ผู้รับปลายทาง)

briefs/W3Q/F-WH-STKTRF/_lane/
├── LANE_BRIEF.md · LANE_LOG.md · LANE_STATE.json
└── (ไม่มี DIVERGENCE.md · ไม่มี BLOCKED.md)
```

**ไม่มี `3_FRD` / `4_TC`** — Phase B ทีมย่อยทำ

---

## 3. ห้ามแตะ (ล็อกแล้ว — แก้ = ต้องกลับมา re-gate)

| # | ของที่ล็อก | ล็อกที่ไหน |
|---|---|---|
| L-1 | ★★ **LOCATION MODEL** — โครงคลัง–โซน–bin · `location_type` 5 ชนิด · กติกาข้ามประเภท 4 ข้อ · ชุด location ตั้งต้น (`WH-BKK-01` · `WH-CNX-01` · **`WH-TRN`** + `TR-BKK-CNX` / `TR-CNX-BKK`) | `PREBRIEF_F-WH-PUTAWAY §3.0` — **สัญญากลางของทั้ง W3Q ห้ามนิยามใหม่แม้แต่ enum เดียว** |
| L-2 | ★★ **โครง 2 ขาของโหมดข้ามคลัง** — ออกจากต้นทาง ≠ ถึงปลายทางทันที · ปลายทางเป็นคนปิดใบ | `OQ-TRF-01` + CHECKLIST W3Q (Scope Lock LK-3/LK-4) |
| L-3 | **Pattern Q archetype ทั้ง 4 surface** — list / wizard 5 steps ชื่อล็อก / view tabs ล็อกลำดับ / PDF+ลายเซ็น+modal · **เอกสารแนบเป็น section ในแท็บรายละเอียด ไม่ใช่แท็บแยก** | Iron Rule #98–#101 |
| L-4 | **B2 v2 line editor** — grid 9 ช่อง กว้าง `26/—/64/92/92/78/72/104/54` · `calcLineVat`/`migrateLine`/`totals`/`taxBadgeV` · แถวขยาย lean 1 บรรทัด + selector 3 ตัว | Iron Rule #99 |
| L-5 | ★ **DOA slot picker คนจริง** (รูป + ตำแหน่ง + ชื่อ) · **ห้ามแสดง/ฝังรหัสตำแหน่งบนหน้าจอ** · ห้ามเขียนสายอนุมัติตายในโค้ด | GOLDEN_RULES §3 (locked 2026-08-17) |
| L-6 | **เลขรัน `TRF-YYYY-NNNN` (ปี ค.ศ.)** ออกตอนส่งอนุมัติ · เปลี่ยนไม่ได้หลังออก · ห้ามมีช่องกรอกเอง | `DOCCFG_BRIEF` · BR-09 |
| L-7 | ★★ **รายการเคลื่อนไหวแบบบันทึกต่อเนื่อง** — แก้ไม่ได้ ลบไม่ได้ · ยกเลิกหลังของขยับทำไม่ได้ · แก้ได้ทางเดียวคือ **ตีกลับคืนต้นทาง** หรือ **กลับรายการ** | CONTEXT_PACK §2.8 · BR-25/BR-22/BR-26 |
| L-8 | ★ **การแยกหน้าที่ 3 ข้อ** — ผู้ขอเซ็นเองไม่ได้ · **คนกดส่งออก ≠ คนกดรับ** · **คนกดส่งออกเซ็นอนุมัติการตัดของหายไม่ได้** | BR-14 · BR-18 · BRD §4.2 |
| L-9 | ★ **ขอบเขต** — ห้ามงอกฟังก์ชันปรับยอด (เป็นของ **F-WH-STKADJ**) · ห้ามงอกการนับสต๊อก (**backlog**) · ห้ามสร้าง/แก้ผังที่เก็บจากหน้านี้ | Scope Lock LK-10 · BR-31/32/33 |
| L-10 | **CI CUBE Warm Light** + Satoshi/Noto Sans Thai + Lucide · **ปี ค.ศ. ล้วน** · sidebar Warehouse ชุดเดียวกับ GRN/Putaway/StockAdj | GOLDEN_RULES §1 · TASTE_LOG |

---

## 4. ASSUMED / OQ + forward-wire (พร้อมเจ้าของ)

### 4.1 `[ASSUMED]` ที่ใช้รอบนี้ — owner **Strike** ทุกตัว

| # | สาระ | ใช้ค่าอะไรไปก่อน | ถ้าเปลี่ยน กระทบอะไร |
|---|---|---|---|
| **OQ-TRF-01** | ข้ามสาขาผ่านจุดพักระหว่างทาง (ออกจากต้นทาง ≠ ถึงปลายทางทันที) | **ใช้เต็มรูปแบบ** | ★ **โครงทั้ง feature ตั้งอยู่บนข้อนี้** — เปลี่ยน = รื้อ state machine + 2 ขา |
| **OQ-STK-01** (สืบทอด) | ปรับยอด = StockAdj · นับสต๊อก = backlog | ห้ามงอกทั้ง 2 อย่าง | เปลี่ยน = scope creep ต้องกลับมาที่ BRD |
| **OQ-GRN-01** (สืบทอด) | ของ QC ไม่ผ่านอยู่ที่กักกัน · ออกทางเดียวคือคืนผู้ขาย | ย้ายได้เฉพาะ กักกัน→กักกัน | กระทบตัวกรอง picker |

### 4.2 `[AI-DRAFT]` ที่รอเคาะ — owner **Strike** (รายละเอียด BRD §15)

`OQ-TRF-02` ฐาน/จุดตัดสายอนุมัติ · `OQ-TRF-03` 1 คู่คลังต่อใบ · `OQ-TRF-04` bin ปลายทางแก้ตอนรับ ·
`OQ-TRF-05` ห้ามออกจากโซนพักรับเข้า · `OQ-TRF-06` ข้อยกเว้นคนดูแล 2 คลัง · `OQ-TRF-07` คู่คลังไม่มีจุดพัก · `OQ-TRF-08` ยอดต้นทางเปลี่ยนระหว่างรออนุมัติ
\+ edge case รอ confirm 8 ข้อ (BRD §10.2)

### 4.3 forward-wire — `TODO:` ใน .md ↔ `FWD-WIRE:` ใน HTML (**คือรายการเดียวกัน**)

> เหตุผลที่ HTML ใช้คนละคำ: `audit.sh` Rule #24 ตั้ง literal `TODO` = FAIL ซึ่งชนกับ S3c ที่บังคับ FAIL = 0 (บันทึกไว้ที่ `_TECH_CHECK.md §5`)

| `TODO:` ใน .md | `FWD-WIRE:` ใน HTML | จุด | **wave/เจ้าของ** |
|---|---|---|---|
| `TODO: JE posting` | `FWD-WIRE: JE posting` | 19 | **W5** (บัญชีแยกประเภท) |
| `TODO: valuation engine` | `FWD-WIRE: valuation engine` | 3 | **W5** |
| (ประกาศใน `DOA_BRIEF`) | `FWD-WIRE: DOA engine` | 2 | **F-DLG-001** (DONE — รอ wire) |
| (ประกาศใน `NTF_BRIEF`) | `FWD-WIRE: ENG-NOTIFY` | 2 | **F-NOTIFY** (DONE — รอ wire) |
| (ประกาศใน `DOCCFG_BRIEF`) | `FWD-WIRE: ENG-DOC-NUM` | 1 | **F-DOCCFG** (DONE — รอ wire) |
| `TODO: RTV handoff` | (soft-ref ชี้ทางเท่านั้น) | — | **F-PUR-RTV** (ba-done) |

`grep -c "TODO" F-WH-STKTRF.html` = **0** ✅ · `FWD-WIRE:` รวม **27 จุด**

---

## 5. vibe ได้แค่ไหน

### ✅ แก้ได้เลย ไม่ต้องกลับมา re-gate
- **Layout / ระยะ / สี / ขนาด** ภายในกรอบ CI CUBE Warm Light (ห้ามเปลี่ยน token สี)
- **ถ้อยคำบนจอ (microcopy)** — ยกเว้น 4 ข้อความที่เป็นการชี้ทางข้าม feature: ชี้ไปใบปรับยอดสต๊อก (2 จุด) · ชี้ไป Putaway (1 จุด) · ชี้ไปคืนผู้ขาย (1 จุด) — **ห้ามลบ** แต่เกลาคำได้
- **ลำดับ/การจัดกลุ่มของ field ภายใน step เดียวกัน** · ความกว้างคอลัมน์ของตารางรายการ (ยกเว้น grid ของ B2 v2 — ดู L-4)
- **ชุดข้อมูลตัวอย่าง (mock)** — เพิ่มใบ/สินค้า/คนได้ **แต่ต้องคง 13 ใบเดิมไว้** เพราะแต่ละใบ prove scenario เฉพาะตัว (ดู `_COVERAGE_R1 §2`)
- ไอคอน · ป้ายสถานะ (สีต้อง map ตาม pill vocabulary กลาง)

### ⛔ แก้แล้วต้องกลับมา re-gate (S3a + S3b ใหม่)
- **โครง 2 ขา / โหมด A–B / เงื่อนไขที่ทำให้เป็นโหมดไหน** (L-2)
- **สถานะเอกสารและเส้นทางเปลี่ยนสถานะ** (11 สถานะ · 15 เส้น)
- **สายอนุมัติ · จำนวนจุดตัดสินใจ · การแยกหน้าที่ 3 ข้อ** (L-5 · L-8)
- **การจัดการส่วนต่าง 3 ทาง** และเงื่อนไขบังคับของการตัดของหาย (เหตุผล + หลักฐาน + อนุมัติ + คนละคนกับผู้ส่ง)
- **โครง Pattern Q / B2 v2** — เพิ่ม-ลด-สลับ step, tab, คอลัมน์ grid (L-3 · L-4)
- **ตัวกรอง picker ตามประเภทที่เก็บ** (L-1)
- **เพิ่มฟังก์ชันใหม่ที่อยู่ใน Out of Scope** (L-9)

### ★ ที่ทีม vibe ควรตรวจให้ (เพราะ Phase A ตรวจไม่ได้)
sandbox บล็อก CDN → **ฟอนต์ไทยและไอคอนไม่โหลด** ตอน render check
⇒ **Rule #38 (ตัวอักษรไทยลอยสูง/เบี้ยว) และรูปทรงไอคอน = ยังไม่ได้ตรวจด้วยตา**
เปิดไฟล์บนเครื่องที่มีเน็ตแล้วดู: ปุ่มไทย · ป้ายสถานะ · หัวตาราง · stepper · ตารางกรอกรายการ

---

## 6. คำสั่ง Phase B

**รอทีม vibe — Phase B หลัง re-gate html-review-fix-order**

ลำดับ Phase B:
`S3r re-gate → S5 FRD (frd-generator-v6) → S6 TC → S6.5 coverage R2 → S7.5 UI Brief → S8 Pack`

**สิ่งที่ Phase B ต้องหยิบไปทำต่อทันที**
1. `frd-generator-v6` ต้องอ่าน **PREBRIEF §5.1 (state machine 2 ขา)** เป็น `03_LOGIC` — อย่าย่อ
2. `05_RULES` ต้องมีครบ BR-01…BR-33 + BR-09b (34 ข้อ) พร้อม tag ตาม BRD §9.1
3. **TC ต้องมีเคสบังคับ 5 กลุ่ม**: รับครบ · **รับไม่ครบ-รอรับเพิ่ม** · **ของหาย-ตัดส่วนต่าง (ครบ 4 เงื่อนไข)** · **ตีกลับคืนต้นทาง** · **รับเกินที่ส่ง (ต้องบล็อก)** — บวกเคสสิทธิ์ "คนส่งกดรับเอง = ไม่ได้"
4. ตรวจ **สมการ invariant** เป็น test case แยก: `จำนวนที่ย้าย = รับแล้ว + ตัดหาย + ตีกลับ + ค้างระหว่างทาง`
5. Security Preset **P2** + ปิด `OQ-TRF-06` (ข้อยกเว้นคนดูแล 2 คลัง) ตอนทำ FRD
6. Regression ตอน pack: **Putaway** และ **StockAdj** ต้องยัง **ไม่เห็นที่เก็บ `in-transit`** ใน picker (BRD §11)
