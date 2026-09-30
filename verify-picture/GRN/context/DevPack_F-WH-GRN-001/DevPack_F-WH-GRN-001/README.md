# DevPack — F-WH-GRN · GRN รับของ (Goods Receipt Note)

> เลน **WF-01 · Mode B** (Phase A pack · `auto: lite`) · registry **F079** · arch **Q-document** · wave **W3**
> ใบประกาศตามชิป: `ntf` · `csq` · `doccfg` · `pdfdoc` — **ไม่มี `doa`**
> สร้างเมื่อ 2026-09-14/15 · input: `input/09142026-grn/`

---

## 1. อ่านอะไรก่อน

| ถ้าคุณคือ | เปิดไฟล์นี้ |
|---|---|
| อยากรู้ว่าฟีเจอร์นี้คืออะไร (2 นาที) | [`FEATURE_TLDR_F-WH-GRN-001.html`](FEATURE_TLDR_F-WH-GRN-001.html) |
| อยากลองกดเอง | [`01_HTML/F-WH-GRN.html`](01_HTML/F-WH-GRN.html) |
| FE dev | [`03_FRD/01_UI.md`](03_FRD/01_UI.md) + [`03_FRD/HTML_UI_BRIEF_F-WH-GRN-001.md`](03_FRD/HTML_UI_BRIEF_F-WH-GRN-001.md) |
| BE dev | [`03_FRD/02_API.md`](03_FRD/02_API.md) + [`03_FRD/03_LOGIC.md`](03_FRD/03_LOGIC.md) |
| DBA | [`03_FRD/04_DB.md`](03_FRD/04_DB.md) |
| QA | [`03_FRD/06_TESTS.md`](03_FRD/06_TESTS.md) + [`04_QA/`](04_QA/) |
| ทุกคน (ข้อห้าม) | [`03_FRD/07_LOCKED_DECISIONS.md`](03_FRD/07_LOCKED_DECISIONS.md) |
| ไล่ดูทั้งแพ็ก | [`03_FRD/INDEX.md`](03_FRD/INDEX.md) |

---

## 2. สถานะรายขั้น

| ขั้น | งาน | skill | สถานะ |
|---|---|---|---|
| 0 | Feature Registry (F079) | — | ✅ `arch` Q-document · `dec` ntf/csq/doccfg/pdfdoc · `wave` W3 · `auto` lite |
| 1–3 | Central Plan · PREBRIEF · อ่านบรีฟ | — | ✅ **ทำมาแล้วจากต้นน้ำ** (BA lane) |
| 4 | HTML v9 | `html-generator-v9` | ✅ **ทำมาแล้วจากต้นน้ำ** — เลนนี้ไม่ได้ generate ใหม่ |
| 5–6 | UX gate · Coverage gate รอบ 1 | — | ✅ ทำมาแล้ว (`1_HTML/_UX_CHECK_REPORT.md` · `_COVERAGE_R1.md`) — **ไม่ได้ใช้แทน re-gate** |
| **7R** | **re-gate หลัง vibe** | `qc-ux-html-checker` + `qc-coverage-checker` | ✅ **รันใหม่ทั้งหมด → เจอ BLOCK 4 จุด แก้แล้ว** |
| 8 | BRD | — | ✅ **ข้าม** — `2_BRD/BRD_F-WH-GRN.md` APPROVED (23/23) คัดเข้า `02_BRD/` ตรง ๆ |
| 9 | FRD v.6 | `frd-generator-v6` | ✅ **FULL** (9 ไฟล์ + INDEX) |
| 9D | ใบประกาศตามชิป | — | ✅ 4 ใบ คัดจาก `5_DECLARATIONS/` |
| 10 | HTML UI Brief | `html-ui-brief` | ✅ `03_FRD/HTML_UI_BRIEF_F-WH-GRN-001.md` |
| 11 | AI MD Testcase | `ai-testcase-md-generator` | ✅ 49 เคส |
| 12 | QA Friendly Testcase | `qa-friendly-html-generator` | ✅ 38 เคส · 22 ภาพ · `CAPTURE VERIFY OK 22 · SKIP/FAIL 0` |
| 12T | Feature TL;DR | `feature-tldr-html` | ✅ `check.sh` **PASS** |
| 13 | Pack | — | ✅ ไฟล์นี้ |
| 14 | ส่งขึ้น OPS | — | ⏳ **ยังไม่ทำ — รอ go-ahead** |

---

## 3. ★ สิ่งที่ QC เจอจริง (ไม่ตกแต่ง)

re-gate ขั้น 7R **รันเครื่องมือเองทุกตัว ไม่รับค่าจากรายงานต้นน้ำ** แล้วเจอของจริง 4 จุดที่ gate ต้นน้ำมองไม่เห็น
ทั้ง 4 จุด **ผู้ใช้อนุมัติให้แก้ก่อนแก้** · ผลคือ **HTML ในแพ็กนี้ไม่ byte-identical กับ `input/`** (3,372 → 3,400 บรรทัด)

### BLOCK-1 ★ CSS ตายเงียบ 64 selector — ร้ายแรงที่สุดของรอบนี้

`@keyframes` 2 บล็อก (`line-expand-slide` · `line-collapse-slide`) **ขาดปีกกาปิด** → parser กลืนกฎที่เหลือทั้งบล็อก

- กฎที่ parse ได้จริง **45 จาก 108** — หายไป 63 กฎ
- surface ที่ตายรวม **ของที่ Pattern Q บังคับ**: `.a4` (แท็บ PDF) · `.tl` (ไทม์ไลน์ลายเซ็น) · `.note*` (แบนเนอร์ทุกใบ) · `.hard-warn` · `.field-error` (การแจ้ง error ของฟอร์ม) · `.combo-pop` (Rule #94) · `.upload-zone` · `.line-expand-panel` · `.drawer-panel.wide`
- **อาการบนจอ:** ใบพิมพ์ A4 เป็นบล็อกเทาไม่มีพื้นขาว คอลัมน์เบียดทับกัน · ลิ้นชัก wizard กว้าง **920 แทนที่จะเป็น 1290** (ผิด Rule #99)
- **ทำไมไม่มีใครเห็น:** `audit.sh` / `self_audit.py` / `static_scan.py` เป็น regex ล้วน **ไม่ได้ parse CSS** · `node --check` ดูแค่ JS · CSS ที่ parse ไม่ผ่าน **ไม่ throw error** → console error = 0
- **หลังแก้:** 108 กฎ · `.a4` พื้นขาว · wizard 1290 · หลักฐาน `01_HTML/_shots/13_view_pdf.png`

### BLOCK-2 · marker `FWD-WIRE:` รั่วขึ้นจอผู้ใช้ (Iron Rule #81 · รูปแบบนี้ครั้งที่ 3)

ต้นน้ำเปลี่ยน `TODO` → `FWD-WIRE` เพื่อเลี่ยง `audit.sh` Rule #24 แต่ marker **ยังอยู่ในข้อความที่ render**
รั่วจริง **7 บรรทัด / 8 จุด** เห็นได้ที่ wizard ขั้น 3 และ **ขั้น 5 (4 จุด)** · แท็บรายละเอียด · แท็บตรวจคุณภาพ · ใบที่กลับรายการ
`self_audit.jargon_leak = 0` จับไม่ได้ — จับได้จาก sweep `innerText` **17 สถานะ**
แก้โดยย้าย marker ไปเป็น**คอมเมนต์ในซอร์ส** → ledger ของ HANDOFF §4.3 ยังครบ · หลังแก้ sweep ได้ **0 hit**

### BLOCK-3 · toast จมใต้ลิ้นชัก (`--z-*` ถูกใช้ 12 จุดแต่ไม่ได้ประกาศเลย)

พิสูจน์บนเส้นทางผู้ใช้จริง: wizard ขั้น 1 → กดใบสั่งซื้อที่เลือกไม่ได้ → toast *"เลือกไม่ได้ — ถูกปิดใบก่อนรับครบ"* ขึ้นจริง
แต่ `elementFromPoint` กลาง toast คืน element ของลิ้นชัก → **ผู้ใช้ไม่เห็นเหตุผลเลยว่าทำไมเลือกไม่ได้**
แก้โดยประกาศ 6 token ใน `:root` + ยก toast เมื่อมี overlay เปิด · หลังแก้ `reachesUser: true` และไม่ทับปุ่มใน footer

### BLOCK-4 · เมนูแถวไม่ flip ขึ้นบน — กดรายการล่างสุดไม่ได้

`openRowMenu()` clamp เฉพาะ `left` ไม่ clamp `top` → แถวสุดท้ายเมนูล้นขอบล่าง **49px** ทั้งจอสูง 900 และ 768
ปุ่มล่างสุด (`กลับรายการ` / `ทิ้งร่าง` = action อันตราย) **กดไม่ได้จริง** · `self_audit.menu_no_flip = 0` ครอบเฉพาะเมนูของ kit
หลังแก้ `overflowBottom = 0` · `lastItemClickable = true`

### สิ่งที่ตรวจแล้ว "ผ่านจริง" (ไม่ใช่ผ่านเพราะไม่ได้ตรวจ)

- ชื่อ wizard 5 ขั้น + ลำดับแท็บ 5 แท็บ **ตรง Iron Rule #100/#101 ตัวอักษรต่อตัวอักษร** (เทียบกับ `iron-rules.md` ไม่ใช่เทียบกับรายงานต้นน้ำ)
- ตารางกรอกรายการ B2 v2 กว้าง `26/—/64/92/92/78/72/104/54` **ตรงเป๊ะ**
- **ปี ค.ศ. ล้วน** — วัด `innerText` ทุกสถานะ: ค.ศ. 31 ครั้ง · **พ.ศ. 0 ครั้ง**
- **ไม่มี DIVERGENCE** — ไม่มีปุ่มอนุมัติ/สายอนุมัติ (ชิปไม่มี `doa`) · ไม่ได้ออก `DOA_BRIEF`
- responsive **ล้นแนวนอน 0 ทุกความกว้าง รวม 768**
- `audit.sh` **FAIL=0** · `node --check` ผ่านทุก script · console error **0**
- ชุดข้อมูลตัวอย่างเดินถึงทุก branch (ผลตรวจครบ 3 ค่า · มีใบที่มีของไม่ผ่าน 2 ใบ · มีใบที่กลับรายการ) — **ไม่เจอกรณี "โค้ดมีแต่ mock เดินไปไม่ถึง"**

### coverage รอบ 2 เจอช่องว่างจริง 9 รายการ — แก้ครบแล้ว

ที่หนักสุดคือ **`IS-02`..`IS-12` (11 ข้อ) และ `OS-02`..`OS-07` (6 ข้อ) ไม่มีที่ลงเลย** เพราะ `02_API §2.7` เขียนสัญญาเป็นร้อยแก้วโดยไม่อ้างรหัส
แก้โดยเพิ่มตาราง `IS` และ `OS` ครบทุกข้อ · รายละเอียดทั้งหมดอยู่ใน `01_HTML/_COVERAGE_REPORT.md §รอบที่ 2`

---

## 4. โครงแพ็ก

```
DevPack_F-WH-GRN-001/
├── README.md                              ← ไฟล์นี้
├── FEATURE_TLDR_F-WH-GRN-001.html         สรุป 2 นาที (check.sh PASS)
├── 01_HTML/
│   ├── F-WH-GRN.html                      ต้นแบบ (แก้ 4 จุดจาก input — ดู §3)
│   ├── _UX_CHECK_REPORT.md                ผล re-gate ขั้น 7R
│   ├── _COVERAGE_REPORT.md                รอบ 1 (HTML) + รอบ 2 (FRD+TC)
│   └── _shots/ (18 ภาพ)                   หลักฐาน ถ่ายใหม่ทั้งชุดหลังแก้
├── 02_BRD/
│   ├── BRD_F-WH-GRN.md                    APPROVED 23/23
│   ├── PREBRIEF_F-WH-GRN.md               source of truth เชิง business
│   ├── FUNCTION_CHECKLIST_F-WH-GRN.md/.html   44 FN
│   └── BASELINE_F-WH-GRN.md               เทียบมาตรฐาน ERP
├── 03_FRD/
│   ├── 00_OVERVIEW … 07_LOCKED_DECISIONS + INDEX   FRD FULL 9+1
│   ├── HTML_UI_BRIEF_F-WH-GRN-001.md      บรีฟ UI สกัดจาก HTML 1:1
│   └── NTF/CSQ/DOCCFG_BRIEF + print-spec-grn.md    ใบประกาศ 4 ใบ
└── 04_QA/
    ├── testcases-F-WH-GRN-001.md          49 เคส (AI)
    ├── testcase-F-WH-GRN-001.html         38 เคส (คน · 22 ภาพฝังในไฟล์)
    └── _build/                            cases.json · shot-spec.json · shots.report.json · DROP_LEDGER.md
```

---

## 5. ข้อห้ามที่ต้องรู้ก่อนแตะโค้ด

| # | ห้าม | เพราะ |
|---|---|---|
| 1 | เพิ่มปุ่มอนุมัติ / สายอนุมัติ / ออก `DOA_BRIEF` | registry F079 ไม่มีชิป `doa` — ใส่เกิน = **DIVERGENCE** ต้องกลับไปแก้ registry ก่อน |
| 2 | เปลี่ยนชื่อ/ลำดับขั้น wizard หรือลำดับแท็บ | ล็อกด้วย Iron Rule #100/#101 + HANDOFF §3.1 |
| 3 | เพิ่ม/ลด/สลับคอลัมน์ตารางกรอกรายการ | ล็อกด้วย Rule #99 (B2 v2) |
| 4 | ให้ feature ตั้งเลขเอกสารเอง | ต้องมาจากศูนย์ตั้งค่าเอกสารเท่านั้น (LOCK-05) |
| 5 | แก้/ลบ movement หรือ audit | ต่อท้ายอย่างเดียว (LOCK-02) · ยกเลิก = กลับรายการทั้งใบ |
| 6 | เขียน `PO.received` จากที่อื่นนอกจากใบรับของ | ทางเดียวคือ `ENG-GRN-04` (R13) |
| 7 | ใช้ปี พ.ศ. แม้จุดเดียว | LOCK-06 — รวมไฟล์ที่ส่งออกด้วย (`DR-09`) |

---

## 6. OQ / ข้อสมมติที่ยังค้าง (ยกจาก HANDOFF §4 + BRD §15 — ห้ามเงียบ)

| # | เรื่อง | ค่าที่ใช้ไปก่อน | ต้องเคาะเมื่อไร |
|---|---|---|---|
| **Q1 / OQ-PO-01** ★ | เปอร์เซ็นต์รับเกิน ตั้งระดับไหน | **0% (รับเกินไม่ได้)** `[ASSUMED]` | **ก่อน FRD — ยังไม่เคาะ** |
| **Q1b / OQ-GRN-01** ★ | ของไม่ผ่านเข้าโซนกักเสมอ หรือปฏิเสธหน้าประตูได้ | **เข้าโซนกักเสมอ** `[ASSUMED]` | **ก่อน FRD — ยังไม่เคาะ** |
| **Q2 / OQ-GRN-03** ★ | คืนของแล้วเปิดยอดค้างรับกลับที่ใบสั่งซื้อไหม | **ไม่เปิดกลับ** | ก่อนเริ่ม RTV |
| Q3 / OQ-GRN-04 | ใครกลับรายการได้ · ภายในกี่วัน | หัวหน้าคลัง · ไม่จำกัดวันแต่ของต้องยังไม่ถูกใช้ต่อ | ก่อน P4 |
| Q4 / OQ-GRN-02 · OQ-PO-06 | บรรทัดบริการอยู่ในใบรับ หรือแยกใบ | อยู่ในใบเดียวกัน (`IS-13`) | ตอบแล้ว |
| Q5 / OQ-GRN-08 | รับย้อนหลังข้ามงวดบัญชีที่ปิดแล้ว | อนุญาตตามเกณฑ์กลาง | เมื่อบัญชี (W5) พร้อม |
| Q6 | มูลค่ารับเข้าใช้ราคาใบสั่งซื้อ หรือรอต้นทุนแฝง | ราคาจากใบสั่งซื้อ | W4 |
| Q7 / OQ-GRN-06 | เจ้าของทะเบียนเหตุผลไม่ผ่านตรวจ | คอนฟิกกลาง 5 ค่า | ก่อน RTV |
| OQ-GRN-05 | เกณฑ์เลขใบส่งของซ้ำ | กติกากลาง (NC rules) | ก่อน P4 |
| OQ-GRN-07 | รับเกินต้องมีคนอนุมัติไหม | **ไม่มี** (ถ้ามี = ต้องเพิ่มชิป `doa` ที่ registry ก่อน) | ก่อน P4 |
| **OQ-7R-01** ⭐ ใหม่จากเลนนี้ | ต้นแบบมี CSS ตายเงียบ 64 selector — เลนนี้แก้ให้แล้ว **ต้นน้ำต้อง sync กลับ** | แก้ในแพ็กนี้ + แจ้ง BA | ก่อน P4 |

> `[ASSUMED]` ทั้งสองตัวถูกทำเป็น **ค่าคอนฟิก** (`CF-01` · `BR-10`) ไม่ใช่ค่าตายในโค้ด — เคาะแล้วเปลี่ยนค่าได้โดยไม่ต้องรื้อ logic

---

## 7. ยังไม่ได้ทำในเลนนี้

- **ส่งขึ้น OPS / zip / push** — รอ go-ahead จากผู้ใช้
- **อัปเดต `st` ของ F079 ใน `Cube_Feature_List.html`** — ทำหลังส่งจริง (ตอนนี้ยังเป็น `wip`)
- **แจ้ง BA lane เรื่อง `OQ-7R-01`** (CSS ตายเงียบ) ให้ sync กลับต้นแบบต้นน้ำ
- **การต่อ engine จริง** — GR/IR (W5) · Putaway (F081 · W3Q) · RTV (F080) ยังเป็นการจำลองตาม LOCK-07 · สัญญาประกาศครบใน `02_API §2.7`
- **ทดสอบข้ามโมดูลกับ PO จริง** — `AT-X-01` · `AT-X-02` ต้องรันร่วมกับทีม F078 ตอนต่อระบบ
- `csq-declaration` และ `pdfdoc` **ยังไม่มี skill ในเรโปนี้** — 2 ใบนี้รับมาจาก `5_DECLARATIONS/` ตามที่ต้นน้ำทำไว้

### หมายเหตุเรื่องความสะอาดของเรโป

แพ็กนี้ไม่มีไฟล์ขยะ (`_qa_shots/` · `shots_b64.json` · `*.bak` · `__pycache__/` = 0 ไฟล์) — การถ่ายภาพทั้งหมดส่งออกไปที่ scratchpad แล้วค่อยฝังเข้าไฟล์
แต่ที่ **รากเรโปมี `_qa_shots/` ค้างอยู่จากรอบ F-WH-PUTAWAY** (ไฟล์ `actor_picker` · `bin_cards`) — ไม่ได้เกิดจากรอบนี้ และยังไม่ได้ลบเพราะอยู่นอกขอบเขตแพ็กนี้
