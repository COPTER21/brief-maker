# DevPack — F-WH-PUTAWAY · จัดเก็บเข้าที่ (Putaway)

| ช่อง | ค่า |
|---|---|
| Feature | `F-WH-PUTAWAY` (fid **F081**) · Putaway — จัดเก็บเข้าที่ |
| Module / Wave | Warehouse (คลังสินค้า) · **W3Q ลำดับ 1** · pack `CUBE-LANE-W3-LITE` |
| Registry F081 | `arch = master` · **`dec = csq`** · `wave = W3Q` · **`auto = lite`** → **Mode B** |
| Input | `input/09142026-putaway/` (Phase A pack จาก BA lane · `feature-lane-runner 2.4.1r`) |
| เลนนี้ทำอะไร | **ขั้น 7R re-gate → Phase B** (FRD → UI Brief → TC → TL;DR → Pack) |
| วันที่ | **2026-09-14** (ปี ค.ศ. ล้วนทั้งแพ็ก) |
| FRD Variant | **FULL** (00…07 + INDEX) |

> **อ่านก่อน 3 ไฟล์:** `03_FRD/00_OVERVIEW.md` (โดยเฉพาะ **§0.12.5 ตาราง map รหัสที่ชนกัน**) → `03_FRD/07_LOCKED_DECISIONS.md` (ของที่แตะไม่ได้) → `FEATURE_TLDR_F-WH-PUTAWAY-001.html` (สรุป 2 นาทีสำหรับคนที่ไม่อ่าน FRD)

---

## โครงแพ็ก

```
DevPack_F-WH-PUTAWAY-001/
├── README.md                                ไฟล์นี้
├── FEATURE_TLDR_F-WH-PUTAWAY-001.html       หน้าปกสรุปภาษาคน (อ่าน 2 นาที)
├── 01_HTML/
│   ├── F-WH-PUTAWAY.html                    ★ ต้นแบบ (แก้ 2 บรรทัดจากต้นน้ำ — LD-03)
│   ├── _UX_CHECK_REPORT.md                  7R re-gate · UX gate
│   ├── _COVERAGE_REPORT.md                  coverage รอบ 1 (7R) + รอบ 2 (ขั้น 13) ต่อกันในไฟล์เดียว
│   └── _shots/                              20 ภาพหลักฐาน (ถ่ายใหม่ทั้งหมดหลังแก้)
├── 02_BRD/                                  BRD APPROVED + PREBRIEF + FUNCTION_CHECKLIST (.md/.html) + BASELINE
├── 03_FRD/                                  00…07 + INDEX + HTML_UI_BRIEF + CSQ_BRIEF
└── 04_QA/
    ├── testcases-F-WH-PUTAWAY-001.md        39 เคส · สำหรับ AI agent
    ├── testcase-F-WH-PUTAWAY-001.html       35 เคส · สำหรับคนทดสอบ (ภาพฝังในไฟล์)
    └── _build/                              cases.json · shot-spec.json · shots.report.json · DROP_LEDGER.md
```

---

## สถานะรายขั้น

| ขั้น | งาน | สถานะ | ผลจริง |
|---|---|---|---|
| 0 | Feature Registry | ✅ | F081 · `arch=master` · `dec=csq` · `wave=W3Q` · `auto=lite` |
| 1–6 | Central Plan → brief → HTML → UX/Coverage gate | ✅ **ทำมาจากต้นน้ำ** | BA lane · S3a/S3b/S3c PASS |
| **7R** | **re-gate หลัง vibe** | ✅ **PASS** | **BLOCK 1 → 0** (แก้ Iron Rule #81) · WARN 5 · 20 ช็อตใหม่ |
| 8 | BRD | ✅ **ข้าม** (Mode B) | `BRD_F-WH-PUTAWAY.md` **APPROVED C01–C23 = 23/23** จากต้นน้ำ |
| 9 | FRD v6 (FULL) | ✅ | 00…07 + INDEX · 25 ฟังก์ชัน · 16 API · 6 ตาราง · 2 engine |
| 9D | ใบประกาศตามชิป | ✅ | **1 ใบ** (`csq`) — 4 ใบที่ไม่ออกมีเหตุผลรายใบ (LD-01/LD-02) |
| 10 | HTML UI Brief | ✅ | design tokens · z-index map · overlay registry · selector anchors · **Drift Log 10 ข้อ** |
| 11 | TC for AI | ✅ | 39 เคส · ทุกเคส trace กลับ FN/R/AT |
| 12 | TC for Tester | ✅ | 35 เคส · 186 ขั้น · **`CAPTURE VERIFY OK 23 · SKIP/FAIL 0` ตั้งแต่รอบแรก** |
| 12T | Feature TL;DR | ✅ | `check.sh` **PASS** — ไม่มีศัพท์ระบบหลุด · self-contained |
| 13 | coverage รอบ 2 + pack | ✅ | ปิดช่องว่าง 3 จุด (DR-10 · CF-01 · CF-04) · traceability ครบทุกตระกูล |
| 14 | ส่งขึ้น OPS | ⏳ **ยังไม่ทำ** | **รอ go-ahead จากผู้ใช้** · ยังไม่ zip ยังไม่ push ยังไม่อัปเดต `st` ใน registry |

---

## ★ สิ่งที่ QC เจอ (ตามจริง — ไม่ตัดทอน)

### 1. BLOCK · Iron Rule #81 — marker ภายในรั่วขึ้นหน้าจอผู้ใช้ (แก้แล้ว · อนุมัติโดยผู้ใช้)

รายงาน S3a ของต้นน้ำเขียนว่า `jargon_leak = 0` และยก 2 element นี้เป็น **หลักฐานผ่าน** ของ FN-15 / FN-33
ตรวจด้วย `innerText` จริงทุกสถานะ (ไม่ใช่ grep source) พบว่า marker **ถูก render ให้ผู้ใช้เห็นจริง 2 จุด**

| ที่ไหน | ข้อความก่อนแก้ |
|---|---|
| แถบยืนยัน (เห็น **ทุกงาน**) | `ไม่กระทบบัญชี — ย้ายภายในคลังเดียวกัน (FWD-WIRE: JE posting)` |
| คำเตือนคิวกักกัน | `…ออกจากการกักกันได้ทางเดียวคือใบคืนผู้ขาย (FWD-WIRE: RTV handoff)` |

**ทำไม gate ต้นน้ำมองไม่เห็น:** `self_audit.jargon_leak` ไม่รู้จักคำว่า `FWD-WIRE` · `audit.sh` Rule #24 จับแค่ literal `TODO` — ซึ่งเป็นเหตุผลที่ต้นน้ำเปลี่ยนมาใช้ `FWD-WIRE` ตั้งแต่แรก → **ผ่านทั้งสอง gate แต่ marker ยังโผล่บนจอ**

**แก้:** ถอด marker ออกจากข้อความ ย้ายไปเป็นคอมเมนต์ท้ายบรรทัดเดิม (บรรทัด 2561 · 2584)
**ผล:** `FWD-WIRE` ในซอร์สยังครบ 5 จุด ทั้งหมดอยู่ในคอมเมนต์ · forward-wire ledger ของ HANDOFF §4.3 ไม่หาย
**ยืนยัน:** `audit.sh` FAIL=0 · `self_audit` เท่าเดิม · `node --check` OK · console/pageerror 0 · jargon sweep 13 สถานะ = **0 hit** · behaviour test 7 กรณีให้ผลเดิมทุกข้อ
→ **`07_LOCKED` LD-03 · ไฟล์ไม่ byte-identical กับ `input/09142026-putaway/1_HTML/` อีกต่อไป**

### 2. PARTIAL · R18 (soft lock) ครบแค่ 1 ใน 3 วรรค

ต้นน้ำให้ FN-21 = ✅ โดยไม่มีช็อตอ้างอิง — ตรวจทีละวรรคแล้วพบว่า:

| วรรค | โค้ด | เดินถึงด้วย mock ที่ส่งมา | เกรดจริง |
|---|---|---|---|
| งานที่คนอื่นถือ กดรับไม่ได้ | ✅ มีจริง | ❌ **ไม่ถึง** | ⚠ |
| หัวหน้าคลังปลดล็อกได้ | ✅ มีจริง | ❌ **ไม่ถึง** | ⚠ |
| หมดเวลาแล้วคืนคิวเอง | ❌ **ไม่มีโค้ด** | — | ❌ |

**เหตุ:** งานเดียวที่ถูกถือครองในชุด mock (`PT-0011`) **ถือโดย `u-anucha` ซึ่งเป็นผู้ใช้ปัจจุบันเอง** → สาขา "ถือโดยคนอื่น" render ไม่ได้เลย
และ `NC.softLockMinutes = 30` **ถูกประกาศแต่ไม่มีโค้ดไหนอ่าน** (grep = 1 ครั้ง คือบรรทัดที่ประกาศเอง · ไม่มี `setInterval`) — ต่างจาก `NC.agingWarnHours` ที่ถูกใช้จริง 4 จุด
→ **`07_LOCKED` LD-05** · `06_TESTS` AT-15 · `DROP_LEDGER` TC-13

### 3. ความขัดแย้งในเอกสารต้นทาง — PREBRIEF vs CSQ_BRIEF

`PREBRIEF §2/§6.2` เขียนว่ามี event `csq putaway.confirmed` · `CSQ_BRIEF §2/§3` เขียนชัดว่า **ห้ามประกาศ** (นับซ้ำกับ `grn_posted`)
**HTML ทำตาม `CSQ_BRIEF` ซึ่งถูกแล้ว** → ตราไว้ที่ **LD-04** + เปิด **`OQ-PUT-10`** ให้ BA แก้ถ้อยคำ

### 4. ช่องว่างที่ coverage รอบ 2 จับได้ (แก้แล้ว)

| รหัส | เนื้อหา | หายไปเพราะ |
|---|---|---|
| `DR-10` | ปี ค.ศ. **ใน export** ไม่ใช่แค่บนจอ | `05_RULES` R22 เขียนแค่ "บนจอ" |
| `CF-01` | เจ้าของ config ผังคลัง + ต้องพร้อมก่อน P2 | `04_DB` อธิบายโครงข้อมูลครบ แต่ไม่ได้ระบุเจ้าของ config |
| `CF-04` | โซนกักกันต่อคลัง | ไม่เคยถูกกล่าวถึงเลย — **จุดที่พังเงียบได้** ถ้าตั้งคนละค่ากับที่ใบรับของใช้ |

### 5. WARN ที่บันทึกไว้ ไม่ได้แก้ (ผู้ใช้ตัดสิน)

| # | เรื่อง | ท่าที |
|---|---|---|
| W-1 | `เกิน 24 ชม. (เกณฑ์จาก NC rules)` ในป้าย KPI — `NC rules` เป็นชื่อกลไกภายใน | **ทบทวนถ้อยคำก่อน production** (LD-06) |
| W-2 | `ต้นแบบ Phase A · 2026` ใน sidebar footer | **ถอดก่อน production** (LD-06) |
| W-3 | ลิสต์ `ผู้จัดเก็บ` ล้นขอบล่าง ~17px ที่ 1440×900 | ไม่ใช่บั๊ก (อยู่ใน pane ที่ scroll ได้ + `max-height` ของ kit) |
| W-4 | `PEOPLE[].ini` (อักษรย่อ) เป็น dead data · `.is-done` เป็น dead CSS | dev ตัดสินตอนทำจริง (Drift Log DR-U1/DR-U2) |
| W-5 | รายงานต้นน้ำอ้างขนาดไฟล์ 2,987 บรรทัด แต่ไฟล์จริง 2,995 | รายงานเขียนก่อนแก้รอบสุดท้าย — **เหตุผลรูปธรรมว่าทำไม §7R ห้ามใช้รายงานเดิมแทน re-gate** |

### 6. สิ่งที่ยืนยันแล้วว่า **ถูกต้อง** (ไม่ใช่ปัญหา)

| เช็ค | ผล |
|---|---|
| **ห้าม Pattern Q (L1)** | `doc_archetype` **false ครบ 14 flag** · grep surface ต้องห้าม 10 ตัว = 0 · dead CSS รูปทรง Q ทั้ง 27 คลาส **อยู่ใน BASE-KIT เท่านั้น** (ต่างจาก F-PUR-COMPARE ที่ทำให้ flag รายงานผิด) |
| **`--z-*` registry** | ประกาศ 8 · ใช้ 6 → **ครบทุกตัวที่ใช้** · ยืนยันด้วย `getComputedStyle` (ไม่ใช่บั๊กแบบ F-SEC-TRANS) |
| **เกณฑ์แนะนำช่องเก็บ** | ไล่ 12 งาน × ทุกการ์ด = **29 คู่ · violation 0** ทั้ง hard filter F-1…F-5 และ rank R1…R4 |
| **ของกักกัน** | `pickerOptions()` ทุกงานกักกัน = `quarantine` **100%** |
| **`in-transit` / `damage`** | ไล่ทุกงาน — **ไม่เคยถูกคืนเลยแม้แต่ครั้งเดียว** |
| **append-only** | `MOVES.splice/shift/pop` = 0 · ปุ่มลบทั้ง 3 มุมมอง = **0** |
| **Responsive** | สะอาดครบ **7 ความกว้าง รวม 768** (ดีกว่า F-PUR-COMPARE) |
| **ปี ค.ศ.** | สแกน 4 สถานะ → พบปีเดียวคือ `2026` · `has_BE` = false |
| **PAGE CSS ของผู้เขียน** | 83 คลาส · dead เพียง **1** (`.is-done`) — สะอาดผิดปกติ |

---

## OQ / ข้อสมมติที่ยังค้าง

### `[ASSUMED]` ที่ใช้ค่าตั้งต้นไปแล้ว (5) — owner **Strike**
`OQ-GRN-01` ของกักกันออกทางใบคืนผู้ขาย · `OQ-TRF-01` in-transit เป็นของใบย้ายสินค้า · `OQ-PUT-01` override ฝืนเกณฑ์ = บังคับเหตุผล · `OQ-PUT-02` ความจุ = เกณฑ์แนะนำ · `OQ-PUT-03` soft lock มีกลไก ค่าอยู่ NC rules

### รอเคาะ (6 + CSQ 5)
`OQ-PUT-04` สิทธิ์+อายุการกลับรายการ · `OQ-PUT-05` เจ้าของ config ผังคลัง · `OQ-PUT-06` เกณฑ์ aging · `OQ-PUT-07` โซนกักกันเป็นโซนหรือช่องพิเศษ · `OQ-PUT-08` ข้ามเขตตีมูลค่า · `OQ-PUT-09` บาร์โค้ด
`CSQ-Q1`…`CSQ-Q5`

### ★ OQ ใหม่ที่เลนนี้เปิด (3)

| # | เรื่อง | เจ้าภาพ |
|---|---|---|
| **`OQ-PUT-10`** | PREBRIEF เขียนว่ามี event `putaway.confirmed` แต่ CSQ_BRIEF ห้ามประกาศ — ต้องแก้ถ้อยคำฝั่ง PREBRIEF | Strike + เจ้าของ F-CSQ-01 |
| **`OQ-PUT-11`** | ชุด mock ให้ `PT-0011` ถือครองโดยผู้ใช้ปัจจุบันเอง → S-15 / FN-21 เดินไม่ถึง · **ข้อเสนอ: เปลี่ยนเป็น `u-somchai`** แล้วทดสอบได้ทันทีโดยไม่ต้องแก้โค้ด | Strike (BA lane) |
| **`OQ-PUT-12`** | `PREBRIEF §8` `PT-0005` ตั้งใจให้เป็นตัวอย่าง override ข้ามหมวด แต่เกณฑ์ R1 จับได้ก่อน — mock ไม่ตรงพฤติกรรมจริง | Strike (BA lane) |

> **`OQ-PO-01` และ `OQ-STK-01` ไม่ใช่ของฟีเจอร์นี้** (อยู่ที่ใบสั่งซื้อ/ใบรับของ และใบปรับยอดสต๊อก) — ระบุไว้กันเข้าใจว่าตกหล่น

---

## ยังไม่ได้ทำในเลนนี้

| # | อะไร | ทำไม |
|---|---|---|
| 1 | **BA sign-off ของ OQ ที่รอเคาะ 14 ข้อ** | ต้องรอ Strike และเจ้าของ F-CSQ-01 / F008 / GL (W5) |
| 2 | **ส่งขึ้น OPS** | รอ go-ahead จากผู้ใช้ — **ยังไม่ zip ยังไม่ push** |
| 3 | **อัปเดต `st` ของ F081 ใน `Cube_Feature_List.html`** | ทำหลังส่งจริงเท่านั้น |
| 4 | **`FN-08` soft-lock timeout** | ต้อง implement ฝั่งเซิร์ฟเวอร์ — ต้นแบบ in-memory ทำ timer ที่มีความหมายไม่ได้ (LD-05) |
| 5 | **ทดสอบ cross-module `XT-01…XT-15`** | ต้องมี F079 / F082 / F083 / F080 / ENG-CSQ / NC rules ที่ใช้งานได้จริง |
| 6 | **ทดสอบสิทธิ์รายบทบาท** | ต้นแบบไม่มีตัวสลับบทบาท (`06_TESTS` §6.2) |
| 7 | **ขยาย schema ของ F008 (ทะเบียนคลัง)** | ต้องเพิ่มระดับ `Bin` ทั้งระดับ + 9 ฟิลด์ (`04_DB` §4.7.6) — **เงื่อนไขเริ่ม P2** |

---

## ★ ของที่ต้องส่งต่อให้ 2 ฟีเจอร์ถัดไปทันที (LOCK-08 · HANDOFF L5)

**`F-WH-STKADJ` (F082)** และ **`F-WH-STKTRF` (F083)** ถูกบังคับให้ใช้สัญญาชุดนี้ — **ห้ามนิยาม location ใหม่**

| ของที่ส่งต่อ | อยู่ที่ |
|---|---|
| โครง คลัง › โซน › ช่องเก็บ + รูปแบบรหัส | **`04_DB` §4.7.1** |
| **`location_type` 5 ชนิด + กติกาข้ามประเภท** | **`04_DB` §4.7.2** |
| คุณสมบัติโซน/ช่องเก็บ (ความจุ · หมวดที่รับ · ห้ามปน · สถานะล็อก) | `04_DB` §4.2 |
| **ชุด location ตั้งต้น (mock ร่วม)** — ห้ามสร้างชุดใหม่ | **`04_DB` §4.7.3** |
| ยอดคงเหลือราย bin เป็นค่า derive จาก movement | `04_DB` `v_bin_stock` · DR-06 |
| movement append-only + คู่ reversal | `04_DB` `t_inv_movement` · `03_LOGIC` `ENG-INV-MOVE` |
| **checklist ก่อนเริ่มงาน** | **`04_DB` §4.7.4** |

> **F083 เป็นเจ้าของ `in-transit`** · **F082 เป็นเจ้าของ `damage`** — Putaway จองประเภทไว้ให้แต่ไม่เขียน

---

## หมายเหตุกระบวนการ

| # | เรื่อง |
|---|---|
| 1 | HANDOFF §6 สั่ง re-gate ด้วย `html-review-fix-order` ซึ่งเป็น **skill ของ BA lane ไม่มีใน repo นี้** → ใช้ `qc-ux-html-checker` + `qc-coverage-checker` ทำหน้าที่แทน (**LD-07**) · ผลลัพธ์เทียบเท่า: จับ BLOCK ได้ 1 ข้อ + PARTIAL 1 ข้อ ที่ gate ต้นน้ำมองไม่เห็น |
| 2 | **repo นี้ไม่มี `csq-declaration` skill** → `CSQ_BRIEF` รับมาจาก `5_DECLARATIONS/` ของต้นน้ำโดยตรง (ช่องว่างจริงของ toolchain — 80 ฟีเจอร์ใน registry ติดชิปนี้) |
| 3 | ภาพในแพ็ก **ถ่ายใหม่ทั้งหมดหลังแก้ HTML** — ชุดก่อนแก้ถูกลบทิ้ง (ตรวจ md5 ซ้ำ = 0 · refs vs on-disk: missing 0 · orphan 0) |
| 4 | ไฟล์ระหว่างทางของการจับภาพ (`shots_b64.json` · `_qa_shots/`) ถูกสร้างไว้ **นอกแพ็ก** และไม่ได้คัดลอกเข้ามา — ภาพฝังอยู่ในไฟล์ HTML แล้ว |
