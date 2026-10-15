# DevPack — F-PUR-COMPARE-001 · เทียบราคาผู้ขาย

**module:** Purchase (จัดซื้อ) · **registry:** [`Cube_Feature_List.html`](../../../Central%20Plan%20v2/Cube_Feature_List.html) **F073** · `arch: master` · `dec: ["csq"]` · `wave: W2` · `auto: lite`
**input:** `input/09132026-compare-vendors/` (Phase A pack จาก BA lane `CUBE-LANE-W2-PUR-LITE`)
**เลนที่ใช้:** [`feature-pack-workflow.md`](../../../feature-pack-workflow.md) · **Mode B** (เข้าที่ขั้น 7R re-gate)
**วันที่:** 2026-09-13

> **อ่านก่อน 2 นาที:** เปิด [`FEATURE_TLDR_F-PUR-COMPARE-001.html`](FEATURE_TLDR_F-PUR-COMPARE-001.html)

---

## 1. สถานะรายขั้น

| ขั้น (WF-01) | skill | ผล | หลักฐาน |
| --- | --- | --- | --- |
| 0 · อ่าน registry | — | ✅ | F073 · `arch: master` · chip `csq` · `auto: lite` |
| 1–3 · Central Plan / brief / อ่านบรีฟ | — | ✅ **ทำจากต้นน้ำ** | `0_DIRECTION/` (RIF · BASELINE · PREBRIEF · FN-01..20 · GAP_R0 · HANDOFF) |
| 4 · HTML | `html-generator-v9` | ✅ **ทำจากต้นน้ำ** | `1_HTML/F-PUR-COMPARE.html` |
| 5 · UX gate (S3a) | `qc-ux-html-checker` | ✅ **ทำจากต้นน้ำ** PASS | `0_DIRECTION/_UX_CHECK_REPORT.md` |
| 6 · Coverage gate (S3b) | `qc-coverage-checker` | ✅ **ทำจากต้นน้ำ** PASS | `0_DIRECTION/_COVERAGE_R1.md` |
| — · Tech gate (S3c) | — | ✅ **ทำจากต้นน้ำ** PASS | `0_DIRECTION/_TECH_CHECK.md` |
| 8 · BRD | `brd-generator-full` | ✅ **ทำจากต้นน้ำ** APPROVED 23/23 | `02_BRD/BRD_F-PUR-COMPARE.md` |
| **7R · re-gate** | `qc-ux-html-checker` + `qc-coverage-checker` | ✅ **PASS** · 0 BLOCK · 8 WARN | `01_HTML/_UX_CHECK_REPORT.md` · `_shots/` 42 ภาพ |
| **9 · FRD Pack** | `frd-generator-v6` | ✅ STANDARD · 8 ไฟล์ | `03_FRD/` |
| **9D · ใบประกาศ** | (csq มาจากต้นน้ำ) | ✅ 1 ใบ · อีก 4 ชิปตั้งใจไม่ทำ | `03_FRD/CSQ_BRIEF_*.md` · `00_OVERVIEW §0.10` |
| **10 · HTML UI Brief** | `html-ui-brief` | ✅ | `03_FRD/HTML_UI_BRIEF_*.md` |
| **6 รอบ 2 · Coverage** | `qc-coverage-checker` | ✅ **PASS** · 0 BLOCK · 3 WARN | `01_HTML/_COVERAGE_REPORT.md` (ท้ายไฟล์) |
| **11 · TC for AI** | `ai-testcase-md-generator` | ✅ 45 เคส | `04_QA/testcases-F-PUR-COMPARE-001.md` |
| **12 · TC for Tester** | `qa-friendly-html-generator` | ✅ 33 เคส · Lite | `04_QA/testcase-F-PUR-COMPARE-001.html` |
| **12T · Feature TL;DR** | `feature-tldr-html` | ✅ gate PASS | `FEATURE_TLDR_*.html` |
| **13 · Pack** | — | ✅ | ไฟล์นี้ |
| 14 · ส่งขึ้น OPS | — | ⏳ **ยังไม่ทำ** | รอ go-ahead |

---

## 2. ★ สิ่งที่ QC เจอจริงในรอบนี้ (ไม่ได้เขียนให้สวย)

HTML เข้ามาโดยผ่าน gate ของต้นน้ำมาแล้วทั้ง 3 ด่าน (S3a/S3b/S3c) — แต่ re-gate รอบนี้ยังเจอเพิ่ม **6 เรื่อง**
ทั้งหมดเป็นหมวดที่ **script จับไม่ได้** ต้องวัดด้วย Playwright หรืออ่านภาพจริง

| # | เจออะไร | ระดับ | หลักฐาน |
| --- | --- | --- | --- |
| 1 | **ศัพท์ภายในหลุดขึ้นจอ 11 จุด** — `soft-reference` · `chip = csq เท่านั้น` · รหัสฟีเจอร์ `F007/F009/F012/F019` · `อยู่นอกขอบเขต feature นี้ (W3)` · `คนละไฟล์ต้นแบบ` · chip `คอนโซลปฏิบัติงาน — ไม่ใช่เอกสารธุรกรรม` | WARN | grep markup หลังตัดคอมเมนต์ + อ่านภาพ `_shots/20 · 34 · 35 · 38` |
| 2 | ในนั้นมี **1 จุดที่ไม่ใช่ scaffolding** — ปุ่ม "ออกใบสั่งซื้อให้…" ขึ้น `ใบสั่งซื้อ (W3) — อยู่นอกขอบเขตรอบนี้` · คำว่า **"รอบ"** ชนกับ *รอบเทียบราคา* ของฟีเจอร์เอง | WARN | `_shots/34_toast_po_hook.png` |
| 3 | **หน้าเลื่อนแนวนอนที่ 768px** — `scrollWidth 796 > 768` เพราะ sidebar คงที่ 232 ไม่ยุบเป็น rail · ช่วง 900–1600 สะอาดหมด | WARN | ตารางวัด 7 ความกว้างใน `_UX_CHECK_REPORT §5 WARN-4` |
| 4 | **CSS ของ Pattern Q ค้างในไฟล์ 50 คลาส** (`line-tbl` · `drawer-panel` · `sign-prog` · `pdf-stage` · `a4` …) — เป็นเหตุให้ `static_scan` รายงาน `is_document=true` ผิด และเป็นช่องให้เผลอละเมิด LD-01 | WARN | สแกน 192 คลาสใน `<style>` เทียบ markup+JS · ไฟล์ไม่มี `classList` และไม่มีชื่อคลาสไดนามิก ผลจึงเชื่อถือได้ |
| 5 | **SC-11 (สิทธิ์) ไม่มีการทำงานเลย** — `grep role\|perm\|canEdit\|readonly\|viewer` = **0 ทุกคำ** ไม่ใช่ "hook ที่ยังไม่ผูกข้อมูล" อย่างที่รายงานต้นน้ำเขียน | WARN | `_COVERAGE_REPORT §6 WARN-B` |
| 6 | **SC-15 (ใบขอซื้อถูกยกเลิก) ไม่มีการทำงานเลย** — `const prCancelled=false;` (บรรทัด 939) **ไม่มีบรรทัดไหนอ่านค่านี้** · ที่มีคือ *ข้อความสำเร็จรูปในกล่องเหตุผลยกเลิก* เท่านั้น | WARN | เดียวกัน |

> **#5 และ #6 เป็นการแก้เกรดรายงานของต้นน้ำ** — `_COVERAGE_R1.md` ให้ ⚠ พร้อมคำว่า "hook ในโค้ด" ซึ่งตรวจแล้วไม่ตรงกับไฟล์
> รอบนี้จึงเปลี่ยนเป็น ❌ **ยังไม่ได้ทำ** และยกเป็นงานที่มีเจ้าของใน `03_FRD/05_RULES.md` (C-09 · EC-09) + เคสทดสอบ TC-49 · TC-50

### สิ่งที่ตรวจแล้ว **ไม่พบปัญหา** (บันทึกไว้กันตรวจซ้ำ)
- `--z-*` ไม่ประกาศค่า — **ไม่ใช่เคสนี้** ไฟล์ไม่ได้ใช้ `var(--z-*)` เลย ประกาศเป็นตัวเลขตรงทั้ง 9 จุด · ลำดับชั้นถูกต้อง
- toast ทับปุ่มใน modal footer — วัด rect เทียบปุ่มทั้ง 5 ตัว → `overlapped: []`
- ข้อความถูกตัดกลางคัน — `scrollWidth > clientWidth` บน `td * · .chip · .pill` → 0 จุด
- runtime error — 0 `pageerror` · 0 `console.error` ตลอด walk 42 ขั้น
- archetype guard — ไม่มี wizard · view tabs · docPill · signProgress · line editor แม้แต่ชิ้นเดียว
- BR-04 (กติกาสำคัญที่สุด) — ทดสอบ 5 สถานะจริง ผ่านหมด (ดู `03_LOGIC §4`)

### การตรวจ traceability ก็ไม่ผ่านรอบแรก
รัน set-difference จริงระหว่าง `05_RULES` ↔ `06_TESTS` แล้วพบขาด `E-CMP-404-ROUND` · `LD-08` · `LD-10` · `LD-12` · `FN-16` และ SC-01/03/04/06/14
→ แก้ด้วยการ **เพิ่ม TC-57..60 และเติม trace** แล้วรันซ้ำจนว่างทุกหมวด — **ไม่ได้แก้ด้วยการลดจำนวนกติกา**

---

## 3. โครงสร้าง pack

```
DevPack_F-PUR-COMPARE-001/
├── README.md                                  ไฟล์นี้
├── FEATURE_TLDR_F-PUR-COMPARE-001.html        อ่าน 2 นาทีเข้าใจทั้งฟีเจอร์ (gate PASS)
├── 01_HTML/
│   ├── CompareVendors.html                    ต้นแบบ (คัดจาก input · ไม่แก้เนื้อไฟล์)
│   ├── _UX_CHECK_REPORT.md                    re-gate — 0 BLOCK · 8 WARN
│   ├── _COVERAGE_REPORT.md                    รอบ 1 + รอบ 2 ในไฟล์เดียว
│   └── _shots/                                42 ภาพหลักฐานที่รายงานอ้างถึง
├── 02_BRD/
│   ├── BRD_F-PUR-COMPARE.md                   APPROVED 23/23 (จากต้นน้ำ)
│   ├── PREBRIEF_F-PUR-COMPARE.md
│   └── FUNCTION_CHECKLIST_F-PUR-COMPARE.md    FN-01..20
├── 03_FRD/
│   ├── INDEX.md · 00_OVERVIEW · 01_UI · 02_API · 03_LOGIC · 04_DB · 05_RULES · 06_TESTS · 07_LOCKED_DECISIONS
│   ├── HTML_UI_BRIEF_F-PUR-COMPARE-001.md     บรีฟ UI สกัดจาก HTML 1:1
│   └── CSQ_BRIEF_F-PUR-COMPARE-001.md         ใบประกาศ 7C (จากต้นน้ำ ไม่แก้)
└── 04_QA/
    ├── testcases-F-PUR-COMPARE-001.md         45 เคส สำหรับ AI agent
    ├── testcase-F-PUR-COMPARE-001.html        33 เคส สำหรับคนกดจริง (ติ๊กผล · บันทึกในเครื่อง · ดาวน์โหลด CSV)
    └── _build/                                cases.json · shot-spec.json · shots.report.json · DROP_LEDGER.md
```

---

## 4. ข้อที่ห้ามแตะ (LD-01..12)

อยู่ครบใน [`03_FRD/07_LOCKED_DECISIONS.md`](03_FRD/07_LOCKED_DECISIONS.md) — ยกมาจาก `HANDOFF.md §3` ครบทั้ง 9 ข้อ + เพิ่มจาก re-gate อีก 3

**3 ข้อที่พลาดแล้วเสียทั้งฟีเจอร์:**
1. **LD-01** — เป็นคอนโซลปฏิบัติงาน **ห้ามทำเป็นเอกสารธุรกรรม** (ห้าม wizard · view drawer 4 แท็บ · เลขที่เอกสาร · แบบพิมพ์/ลายเซ็น)
2. **LD-05** — **เหตุผลบังคับเมื่อไม่ใช่ราคาต่ำสุด หรือมีผู้เสนอรายเดียว** (≥3 ตัวอักษร · ปุ่มปิดจนกว่าจะกรอก) — จุดควบคุมหลักด้านการกำกับดูแล
3. **LD-06/07** — **ยืนยันแล้วล็อกถาวร** + **ประวัติเพิ่มอย่างเดียว**

> ถ้าตอนต่อระบบจริงมีใครใส่ **สายอนุมัติ · เลขที่เอกสาร · แบบพิมพ์ · แจ้งเตือน** เข้ามา = **DIVERGENCE** ต้องหยุดแล้วกลับไปที่ BA ทันที (registry F073 ประกาศชิปแค่ `csq`)

---

## 5. งานค้างที่ส่งต่อ (TD-01..06)

| # | งาน | จาก |
| --- | --- | --- |
| TD-01 | ทำสิทธิ์ตามบทบาท (C-09) — ผู้ขอซื้อ/ผู้ตรวจสอบ = อ่านอย่างเดียว | re-gate WARN-6 |
| TD-02 | ทำการเตือนเมื่อใบขอซื้อถูกยกเลิกหลังเปิดรอบ (EC-09) | re-gate WARN-6 |
| TD-03 | ลบ CSS ของ Pattern Q ที่ค้าง 50 คลาส + ถอดศัพท์ภายใน 11 จุด (LD-12) | re-gate WARN-3 · WARN-5 |
| TD-04 | แก้ h-scroll ที่ 768px — sidebar เป็น rail/off-canvas | re-gate WARN-4 |
| TD-05 | ต่อ upload ไฟล์แนบจริง | re-gate WARN-2 |
| TD-06 | ใส่ ARIA (`aria-live` ที่ toast · `role="dialog"` ที่ modal · `aria-label` ที่ปุ่มไอคอน) | re-gate WARN-7 |
| — | ถอดปุ่ม "สาธิตสถานะโหลดผิดพลาด" ก่อน production (LD-11) | เก็บไว้ให้ QA ทดสอบ FN-03 |
| — | เพิ่มข้อมูลตัวอย่างที่ยอดเท่ากันพอดี เพื่อให้ TC-25 (EC-03) กดเห็นบนจอ | coverage รอบ 2 WARN-E |

---

## 6. คำถามที่ยังไม่มีคำตอบ (OQ — ห้ามตัดสินเองในชั้น dev)

10 ข้ออยู่ท้าย [`03_FRD/07_LOCKED_DECISIONS.md`](03_FRD/07_LOCKED_DECISIONS.md) — ที่กระทบงานมากที่สุด:

| OQ | เรื่อง | ค่าที่ใช้ไปก่อน | เจ้าของ |
| --- | --- | --- | --- |
| **A-01** | รูปแบบข้อมูลส่งต่อใบสั่งซื้อ | `[ASSUMED]` — ดู `02_API §6` | เจ้าของ W3 |
| OQ-02 | บังคับจำนวนผู้ขายขั้นต่ำตามช่วงยอดไหม | แนะนำบนจอ ไม่บังคับ (BR-08) | ฝ่ายกำกับ/ตรวจสอบ |
| OQ-03 | ใบเสนอราคาหมดอายุควรบล็อกการยืนยันไหม | เตือนอย่างเดียว (BR-10) | เจ้าของกระบวนการ |
| OQ-04 | ผู้ขายแก้ราคา → ทับ หรือเก็บเวอร์ชัน | ทับ + ประวัติ | สถาปนิกระบบ |

---

## 7. ยังไม่ได้ทำในเลนนี้

- ❌ **ทีม vibe ยังไม่ได้ปรับหน้าจอ** — HANDOFF §7 ออกแบบไว้ว่าทีมปรับก่อนแล้วค่อย re-gate · รอบนี้ re-gate บนไฟล์ที่มาจาก BA ตรง ๆ
  ถ้ามีการ vibe เพิ่มภายหลัง **ต้องรัน §7R ใหม่ทั้งชุด** ไม่ใช้รายงานนี้แทน
- ❌ **BA ยังไม่เซ็นรับ pack นี้**
- ❌ **ยังไม่ zip · ยังไม่ส่งขึ้น OPS** — รอ go-ahead
- ❌ **ยังไม่อัปเดต `st` ของ F073 ใน registry** — ทำหลังส่งจริง
- ℹ️ re-gate `html-review-fix-order` ที่ HANDOFF §7 อ้างถึง **ไม่มีใน repo นี้** (เป็น skill ของ BA lane) — ใช้ `qc-ux-html-checker` + `qc-coverage-checker` ทำหน้าที่แทน
