# DevPack F-PUR-PO-001 · ใบสั่งซื้อ (Purchase Order)

| | |
|---|---|
| **Feature** | `F-PUR-PO` · fid **F078** · module **Purchase** |
| **Registry** | `arch: Q-document` · `dec: [doa, ntf, csq, doccfg, pdfdoc]` · `wave: W3` · `auto: lite` |
| **เลน** | WF-01 **Mode B** (Phase A pack จาก BA lane → เลนนี้ทำ 7R + Phase B) |
| **วันที่ทำ** | 2026-09-14 |
| **input** | `input/09142026-po/` |

---

## เริ่มอ่านตรงไหน

| ถ้าคุณคือ | เปิดไฟล์นี้ |
|---|---|
| อยากเข้าใจภาพรวมใน 2 นาที | [`FEATURE_TLDR_F-PUR-PO-001.html`](FEATURE_TLDR_F-PUR-PO-001.html) |
| FE dev | [`03_FRD/01_UI.md`](03_FRD/01_UI.md) + [`03_FRD/HTML_UI_BRIEF_F-PUR-PO-001.md`](03_FRD/HTML_UI_BRIEF_F-PUR-PO-001.md) + `01_HTML/F-PUR-PO.html` |
| BE dev | [`03_FRD/02_API.md`](03_FRD/02_API.md) + [`03_FRD/03_LOGIC.md`](03_FRD/03_LOGIC.md) |
| DBA | [`03_FRD/04_DB.md`](03_FRD/04_DB.md) |
| QA | [`03_FRD/06_TESTS.md`](03_FRD/06_TESTS.md) + `04_QA/` |
| ทุกคน — **อ่านก่อนแก้อะไร** | [`03_FRD/07_LOCKED_DECISIONS.md`](03_FRD/07_LOCKED_DECISIONS.md) |
| หาไฟล์ไม่เจอ | [`03_FRD/INDEX.md`](03_FRD/INDEX.md) |

---

## สถานะรายขั้น

| ขั้น | งาน | สถานะ | หลักฐาน |
|---|---|---|---|
| 0 | อ่าน Feature Registry | ✅ | `F078` — `arch`/`dec`/`wave`/`auto` ตรงกับ HANDOFF ทุกช่อง |
| 1–6 | brief · HTML · gate รอบต้นน้ำ | ✅ **ทำมาแล้วจาก Phase A** | `input/09142026-po/0_DIRECTION/` |
| **7R** | **re-gate หลัง vibe** | ✅ **PASS** (หลังแก้ 2 BLOCK) | [`01_HTML/_UX_CHECK_REPORT.md`](01_HTML/_UX_CHECK_REPORT.md) · [`01_HTML/_COVERAGE_REPORT.md`](01_HTML/_COVERAGE_REPORT.md) |
| 8 | BRD | ✅ **ข้าม** — APPROVED มาแล้ว | `02_BRD/BRD_F-PUR-PO.md` (Quality Gate C01–C23 = 23/23) |
| 9 | FRD v6 **FULL** | ✅ | `03_FRD/` 9 ไฟล์ + INDEX |
| 9D | ใบประกาศตามชิป | ✅ **5/5** | `03_FRD/*_BRIEF_*.md` + `PRINT_SPEC_*` |
| 10 | HTML UI Brief | ✅ | `03_FRD/HTML_UI_BRIEF_F-PUR-PO-001.md` |
| 11 | Test case สำหรับ AI | ✅ **72 เคส** | `04_QA/testcases-F-PUR-PO-001.md` |
| 12 | Test case สำหรับคน | ✅ **57 เคส** | `04_QA/testcase-F-PUR-PO-001.html` |
| 12T | Feature TL;DR | ✅ gate PASS | `FEATURE_TLDR_F-PUR-PO-001.html` |
| 13 | Pack | ✅ | ไฟล์นี้ |
| 14 | ส่งขึ้น OPS | ⬜ **ยังไม่ทำ** — รอ go-ahead | — |

---

## ★ สิ่งที่ QC เจอจริงในรอบนี้ (ไม่ตกแต่ง)

ต้นน้ำรายงาน **S3a = PASS with 6 warnings · BLOCK = 0**
re-gate รอบนี้ **พบ BLOCK 2 ข้อที่ต้นน้ำไม่ได้จับ** — ทั้งคู่เป็นหมวดที่ script มองไม่เห็นโดยโครงสร้าง

### BLOCK ที่เจอ (แก้แล้วทั้งคู่ — ผู้ใช้อนุมัติ 2026-09-14)

| # | เรื่อง | ทำไม script ไม่จับ | หลักฐานตอนเจอ | หลังแก้ |
|---|---|---|---|---|
| **UX-01** | เมนูของแถวล่างสุดในหน้ารายการ **จมใต้ขอบจอ 104.5px** — รายการที่ 2 และ 3 กดไม่ได้เลย (Iron Rule #66) | `self_audit.menu_no_flip = 0` เพราะตัวตรวจดูเฉพาะเมนูของ kit (`.menu-fixed`) ส่วน `.row-menu` หน้านี้สร้างเอง | วัดด้วย Playwright ที่ 1440×900 และ ×768 → ล้น **+104.5px** ทั้งคู่ · ภาพ `_shots/21_bottom_edge_*.png` | `overflowPx` = **−49.5** (อยู่ในจอ) · เมนูพลิกขึ้นบน · กดครบทั้ง 3 รายการ |
| **UX-02** | marker ภายใน `FWD-WIRE` + รหัส wave `W7`/`W3P` **โผล่บนจอผู้ใช้ 3 จุด** (Iron Rule #81) | ต้นน้ำเปลี่ยน `TODO` → `FWD-WIRE` เพื่อให้ผ่าน `audit.sh` Rule #24 แต่วางไว้ใน**ข้อความที่ render** จึงผ่าน gate โดยปัญหาเดิมยังอยู่ | สแกน `innerText` ทุก surface (15 ใบ × 5 แท็บ + wizard 5 ขั้น + modal 5) → พบ 6 บริบท | สแกนซ้ำ **`FWD-WIRE` = 0 hit** |

**แก้ไป 4 จุด · ไม่แตะ L-01..L-09 เลย** — รายละเอียดใน `07_LOCKED LD-03`
→ ผลคือ **ไฟล์ HTML ในแพ็กนี้ไม่ byte-identical กับ `input/09142026-po/1_HTML/` อีกต่อไป**
`_TECH_CHECK.md` ของต้นน้ำยังใช้อ้างได้ในส่วนที่ไม่เกี่ยวกับ 4 จุดนี้

### สิ่งที่ตรวจแล้ว "ผ่านจริง" (ตรวจเองไม่ได้เชื่อรายงานต้นน้ำ)

| ตรวจ | ผล |
|---|---|
| PREFLIGHT stamp ตรงกับการนับจริง | ✅ ตรงทุกตัว (156/2/1/8/0/0) — **stamp เชื่อถือได้** |
| `audit.sh` | ✅ **FAIL = 0** (WARN 3) |
| Pass D — Pattern Q / B2 (27 ข้อ) | ✅ **27/27** |
| **Iron Rule #100** ชื่อขั้น wizard | ✅ **ตรงทุกตัวอักษร** — เทียบกับ `iron-rules.md` โดยตรง (รอบ F-PUR-PR เคยพบว่าผิด รอบนี้ถูก) |
| Iron Rule #101 ลำดับแท็บ | ✅ ตรง |
| Iron Rule #99 ความกว้าง grid B2 | ✅ `26/—/64/92/92/78/72/104/54` ตรงสัญญา |
| Rule #69 BASE-KIT verbatim | ✅ **diff กับ template = 0 บรรทัด** |
| JS syntax | ✅ 4/4 block ผ่าน `node --check` |
| pageerror ตลอดทุก surface | ✅ **0** |
| Responsive 7 ความกว้าง (รวม 768) | ✅ **ไม่มี h-scroll เลยสักความกว้าง** |
| z-index ประกาศ vs ใช้ | ✅ ประกาศ 9 ใช้ 8 — resolve ครบ (ไม่ใช่บั๊ก `--z-*` แบบรอบก่อน ๆ) |
| modal ซ้อนเหนือ drawer | ✅ 60 > 51 · ยืนยันด้วย `elementFromPoint` |
| Dropdown anatomy 4 ตัว (#102) | ✅ รูปแบบเดียวกันหมด |
| **L-09 hard vs soft** | ✅ **ยืนยันครบสองฝั่ง** — ยอดเกินใบขอซื้อได้ `disabled` จริง · งบเกินไม่ปิดปุ่ม |
| scope creep | ✅ **0** จาก 9 รายการนอกขอบเขต |
| DIVERGENCE เทียบ registry | ✅ **ไม่พบ** |

### WARN ที่ยังค้าง (8 ข้อ — จงใจไม่แก้)

| id | เรื่อง | ทำไมไม่แก้ |
|---|---|---|
| UX-03 | `.note.warn` ยาว 121 ตัวอักษร (เพดาน 120) | เกิน 1 ตัว · นอกขอบเขตที่ตกลง (แก้เฉพาะ BLOCK) |
| UX-04 | icon 2 จุดไม่มี class `w-/h-` | เหตุผลเดียวกัน |
| UX-05 | เซลล์ตารางมีบรรทัดรอง | เป็น meta ของข้อมูลเดียวกัน — ยอมรับได้ตาม #103 |
| UX-06 | `font-size` 5 จุดไม่ใช้ token | อยู่ใน shell CSS · ไม่กระทบ CI ที่ผู้ใช้เห็น |
| UX-07 | ตารางหน้ารายการล้น fold 130.5px (#96) | ไม่บล็อก — มี `overflow-y:auto` แล้วและไม่มี h-scroll |
| UX-08 | แถวสูง 63px (มาตรฐาน ~44px) | เป็นแถว 2 บรรทัดตาม archetype — สอดคล้อง golden reference |
| UX-09 | dead CSS 101 คลาส | **ตรวจไม่น่าเชื่อถือในไฟล์นี้** (มี `classList` 24 จุด + ต่อชื่อคลาส 10 จุด) และเกือบทั้งหมดเป็น BASE-KIT ที่ **Rule #69 ห้ามแก้** |
| UX-10 | inline layout 156 จุด | golden reference มี **444** (2.3×) — สืบทอดจาก archetype |

> 5 รายการที่ scanner รายงานแต่ตรวจแล้วเป็น false-positive (`long_banners` 14→1 · `missing_ids` · `fullwidth_select` · `spacing_off` · `hex_off`) แจกแจงไว้ที่ `_UX_CHECK_REPORT §4`

---

## ★ คำถามที่ยังไม่มีคำตอบ (ต้องเคาะก่อนขึ้น production)

### เคาะแล้วในรอบนี้ (2026-09-14)

| # | เรื่อง | มติ |
|---|---|---|
| **Q1** | เปอร์เซ็นต์รับเกิน ตั้งระดับใด | **คงตามที่ทำอยู่ — ตั้งต่อผู้เช่า ค่าเริ่มต้น 0% ปรับต่อบรรทัดได้** |
| **Q2** | ตรวจงบไม่ผ่าน บล็อกหรือเตือน | **คง soft — เตือนอย่างเดียว** (ตรง BR-15 + L-09) |

### ยังค้าง — เจ้าภาพหลัก **Strike**

| # | เรื่อง | กระทบอะไร |
|---|---|---|
| Q3 | เวลาที่ยอมรับได้ต่อขั้นอนุมัติ | R24 ยังไม่มีเคสทดสอบ |
| Q4 | เกณฑ์ "ใบซ้ำ" กว้างแค่ไหน | R20 (ไม่กระทบโครง) |
| Q5 | ใครปิดใบก่อนกำหนดได้ · ต้องอนุมัติไหม | `DOA_BRIEF §8` |
| Q6 | ใบขอซื้อต้นทางถูกยกเลิก บล็อกหรือเตือน | ปัจจุบันเตือน |
| Q7 | บรรทัดบริการรับของอย่างไร | E11 ยังไม่มีเคส · กระทบ GRN |
| Q8 | เก็บใบเป็นเวอร์ชันแยกใบไหม | **ถ้าเปลี่ยนต้องกลับไปแก้ BRD §6** |
| Q9 | เปลี่ยนผู้อนุมัติระหว่างรออนุมัติได้ไหม | กระทบ DOA + UI |

**ยังต้องเคาะฝั่งใบประกาศ:** `DOA_BRIEF §8` DOA-Q1..Q5 · `CSQ_BRIEF §6` CSQ-Q1..Q3 · `DOCCFG_BRIEF §5` DOC-Q1..Q2

### `[ASSUMED]` ที่ใช้ค่า default ไปก่อน

| # | เรื่อง | ค่าที่ใช้ | เจ้าภาพ |
|---|---|---|---|
| OQ-PO-01 | เพดานรับเกิน | config ต่อผู้เช่า · default 0% | Strike |
| PR contract | สัญญาข้อมูลจากใบขอซื้อ (F072) | ตามที่ระบุใน `00_OVERVIEW §0.4` | Strike + เจ้าของ F072 |
| Compare contract | สัญญาข้อมูลจากผลเทียบราคา (F073) | เลขที่ · ผู้ชนะ · ราคาที่ชนะ | Strike + เจ้าของ F073 |

### `[AI-DEFAULT]` — skill ตัดสินแทน BA (ต้องยืนยัน)

| probe | เรื่อง | ค่าที่ใช้ |
|---|---|---|
| PR-1 | แก้ใบเดียวกันพร้อมกัน | optimistic lock → `409 CONFLICT_VERSION` |
| PR-7 | กดส่ง/อนุมัติซ้ำ | บังคับ idempotency key |
| PR-9 | ผู้อนุมัติถูกถอดสิทธิ์หลังส่ง | ใช้ภาพนิ่งสายอนุมัติ ณ เวลาส่ง |

---

## ยังไม่ได้ทำในเลนนี้

| เรื่อง | สถานะ |
|---|---|
| **ส่งขึ้น OPS** | ⬜ **ยังไม่ทำ** — รอ go-ahead จากผู้ใช้ (ไม่ zip ไม่ push เอง) |
| **อัปเดต `st` ใน registry** | ⬜ ยังเป็น `wip` — เปลี่ยนหลังส่งจริงเท่านั้น |
| **BA sign-off** | ⬜ ยังไม่มี |
| `thai-doc-pdf-generator` (ออก `PO_template.html` + `PO_sample.pdf`) | ⬜ HANDOFF §6 แนะนำให้ทำก่อน S5 — **ยังไม่ได้ทำ** เพราะ repo นี้ไม่มี skill นั้น · สเปกอยู่ที่ `03_FRD/PRINT_SPEC_F-PUR-PO-001.md` แล้ว |
| ตั้งค่า DOA จริงที่หน้าทะเบียนกลาง (`wire_status: pending → wired`) | ⬜ เป็นงานของคนตั้งค่า ไม่ใช่เลนนี้ |
| Golden Compare เชิงสายตาทีละใบ | ⬜ เทียบเชิงกลแล้วตรงทุกข้อ · ยังไม่ได้วางภาพคู่กัน |
| ทดสอบการพิมพ์จริงของเอกสาร A4 | ⬜ ตรวจบนจอเท่านั้น |

### ช่องว่างของ toolchain (ไม่ใช่ของงาน)

| ขาดอะไร | ผลกระทบ |
|---|---|
| `csq-declaration` skill | **80 ฟีเจอร์ใน registry ติดชิปนี้** — รอบนี้ยก `CSQ_BRIEF` มาจาก Phase A |
| pdfdoc spec generator | **28 ฟีเจอร์** — รอบนี้ยก `print-spec-po.md` มาเป็น `PRINT_SPEC_*` |
| `html-review-fix-order` (re-gate ของ BA lane) | ไม่มีใน repo นี้ — ใช้ `qc-ux-html-checker` + `qc-coverage-checker` ทำหน้าที่แทน |

---

## โครงแพ็ก

```
DevPack_F-PUR-PO-001/
├── README.md                          ← ไฟล์นี้
├── FEATURE_TLDR_F-PUR-PO-001.html     หน้าปกสรุป อ่าน 2 นาที (gate PASS)
├── 01_HTML/
│   ├── F-PUR-PO.html                  ต้นแบบ (แก้ 4 จุดในรอบ re-gate)
│   ├── _UX_CHECK_REPORT.md            re-gate · PASS with 8 warnings
│   ├── _COVERAGE_REPORT.md            รอบ 1 + รอบ 2 (ต่อท้ายไฟล์เดียวกัน)
│   └── _shots/ (24 ภาพ)               หลักฐานของรอบนี้ทั้งหมด
├── 02_BRD/                            BRD APPROVED + PREBRIEF + checklist + baseline
├── 03_FRD/                            FRD FULL 9 ไฟล์ + INDEX + UI Brief + ใบประกาศ 5 ใบ
└── 04_QA/
    ├── testcases-F-PUR-PO-001.md      72 เคส (สำหรับ AI)
    ├── testcase-F-PUR-PO-001.html     57 เคส (สำหรับคน · ติ๊กได้ · พิมพ์ได้)
    └── _build/                        cases.json · shot-spec.json · shots.report.json · DROP_LEDGER.md
```

---

## ผลการตรวจก่อนปิดแพ็ก

| ตรวจ | ผล |
|---|---|
| ภาพที่รายงานอ้าง vs ไฟล์จริง | **MISSING 0 · ORPHAN 0** |
| `CAPTURE VERIFY` ของเอกสาร QA | **OK 27 · SKIP/FAIL 0** (pre-verify selector ก่อนถ่ายทุกตัว) |
| ทุกข้อใน HANDOFF §3 (L-01..L-09) อยู่ใน `07_LOCKED` | **9/9** |
| LOCK-01..07 จาก BRD §3.4 อยู่ใน `07_LOCKED` | **7/7** |
| ทุก OQ/ASSUMED จาก HANDOFF §4 อยู่ใน README | **ครบ** |
| R8 Logic traceability | **26/26 ไม่มี orphan** |
| ไฟล์ขยะ (`_qa_shots/` · `shots_b64.json` · `.bak` · `__pycache__`) | **ลบหมดแล้ว** |
| ขนาดแพ็ก | 8.4 MB |
