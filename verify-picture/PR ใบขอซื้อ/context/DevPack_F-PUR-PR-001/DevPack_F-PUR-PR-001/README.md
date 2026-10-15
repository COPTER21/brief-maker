# DevPack — F-PUR-PR-001 · PR ใบขอซื้อ (Purchase Requisition)

**Feature registry:** `F072` · module **Purchase** · wave **W2**
**`arch`:** `Q-document` · **`dec`:** `doa` ⚖ · `ntf` 🔔 · `csq` ◆ · `doccfg` · `pdfdoc` 📄 (**ครบ 5 ชิป**) · **`auto`:** `lite`
**เลนที่ใช้:** WF-01 **Mode B** — Phase A มาจาก BA lane (`CUBE-LANE-W2-PUR-LITE`) · เลนนี้เริ่มที่ **ขั้น 7R** แล้วทำ Phase B
**input:** `input/09132026-pr/` · **วันที่ทำ:** 2026-09-13 · **ปี ค.ศ. ทุกจุด**

> เปิดอ่านเร็วสุด: [`FEATURE_TLDR_F-PUR-PR-001.html`](FEATURE_TLDR_F-PUR-PR-001.html) (2 นาทีจบ) → [`03_FRD/INDEX.md`](03_FRD/INDEX.md)

---

## 1. สถานะรายขั้น

| ขั้น | งาน | skill / วิธี | ผล |
|---|---|---|---|
| 0 | อ่าน Feature Registry | `Cube_Feature_List.html` แถว F072 | ✅ `arch`/`dec`/`wave`/`auto` ตรงกับ pack |
| 1–6 | RIF → BASELINE → PREBRIEF → GAP → HTML → S3a/S3b/S3c | **BA lane (ต้นน้ำ)** | ✅ รับมาแล้ว |
| **7R** | **re-gate หลัง vibe** | `qc-ux-html-checker` + `qc-coverage-checker` | ✅ **PASS** — พบ **1 BLOCK + 14 WARN** แก้ครบ (ดู §3) |
| 8 | BRD | — | ⏭ **ข้าม** — `2_BRD/` APPROVED (C01–C23 · 23/23) คัดเข้า `02_BRD/` ตรง ๆ |
| 9 | FRD v.6 | `frd-generator-v6` | ✅ **FULL** (9 files + INDEX) · Phase 3.5 ผ่านทุก section |
| 9D | ใบประกาศตามชิป | รับจาก `5_DECLARATIONS/` | ✅ **ครบ 5 ใบ** |
| 10 | HTML UI Brief | `html-ui-brief` | ✅ extraction-based + Drift Log 5 ข้อ |
| 11 | AI MD Testcase | `ai-testcase-md-generator` | ✅ **AI-01..AI-45** |
| 12 | QA Friendly Testcase | `qa-friendly-html-generator` | ✅ **TC-01..TC-36** · `CAPTURE VERIFY OK 26 · SKIP/FAIL 0` |
| 12T | Feature TL;DR | `feature-tldr-html` | ✅ `check.sh` **PASS** |
| 13 | Pack + coverage รอบ 2 | `qc-coverage-checker` | ✅ **PASS** — พบช่องว่าง 3 จุด ปิดครบ (ดู §3) |
| 14 | ส่งขึ้น OPS | — | ⏳ **ยังไม่ทำ** — รอ go-ahead |

---

## 2. โครงสร้าง pack

```
DevPack_F-PUR-PR-001/
├── README.md                          ← ไฟล์นี้
├── FEATURE_TLDR_F-PUR-PR-001.html     หน้าปกสรุป อ่าน 2 นาที
├── 01_HTML/
│   ├── F-PUR-PR.html                  ต้นแบบ (แก้ 2 เรื่องตามด่าน — ดู §3)
│   ├── _UX_CHECK_REPORT.md            ผล re-gate ขั้น 7R
│   ├── _COVERAGE_REPORT.md            coverage รอบ 1 (7R) + รอบ 2 (ก่อนปิด pack)
│   └── _shots/                        14 ภาพหลักฐานที่รายงานอ้างถึง
├── 02_BRD/                            BRD APPROVED + PREBRIEF + FUNCTION_CHECKLIST
├── 03_FRD/                            00_OVERVIEW … 07_LOCKED + INDEX
│                                      + ใบประกาศ 5 ใบ + HTML_UI_BRIEF
└── 04_QA/
    ├── testcases-F-PUR-PR-001.md      TC สำหรับ AI agent (45 เคส)
    ├── testcase-F-PUR-PR-001.html     TC สำหรับคน (36 เคส · ภาพฝังในไฟล์)
    └── _build/                        cases.json · shot-spec.json · shots.report.json · DROP_LEDGER.md
```

---

## 3. ★ สิ่งที่ QC เจอจริงในเลนนี้ (ไม่ตกแต่ง)

### 3.1 BLOCK 1 ข้อ — ชื่อขั้นที่ 3 ของ wizard ผิดจากที่ล็อก

| | |
|---|---|
| พบ | `STEP_NAMES[2] = 'รายการที่ขอซื้อ'` |
| ต้องเป็น | **`'รายการสินค้า'`** |
| กติกาที่ขัด | **iron rule #100** (`iron-rules.md:1000`) + `Q_transaction-document-archetype.md:134` + `SKILL.md:549` |
| LOCK | HANDOFF §3 ข้อ 1 — *"เปลี่ยนที่นี่ = เอกสารทุกใบใน CUBE ไม่ตรงกัน"* |
| BRD ยืนยันฝั่งเดียวกัน | BRD §14.6 SC-2 เขียนว่า *"… › **รายการสินค้า** › …"* |
| การตัดสินใจ | **คืนค่าที่ล็อก** (ผู้ใช้ตัดสินใจ 2026-09-13) — เป็นการ *บังคับใช้* LOCK ไม่ใช่แตะ LOCK |
| หลักฐานหลังแก้ | Playwright อ่าน `.stepper .tx` index 2 = **`รายการสินค้า`** |

> ⚠️ **รายงาน S3a ของต้นน้ำติ๊กข้อนี้ว่า "ชื่อตรง … ✅ ตรงเป๊ะ" ซึ่งไม่ตรงกับไฟล์จริง**
> เป็นเหตุผลว่าทำไม §7R ถึงห้ามใช้รายงานเดิมแทนการรันเอง

### 3.2 WARN 14 จุด — ศัพท์ภายในรั่วขึ้นจอ (iron rule #81)

`ENG-NOTIFY` · `mock` · `soft-reference` · `My Approval` · `Phase A` · `backend` · `feature` · รหัสฟีเจอร์ (`F007` `F009` `F012` `F019` `F073`) · รหัส wave (`W3`)
โผล่ใน **toast · field-help · section title** ที่ผู้ใช้เห็นจริง — **static scan จับไม่ได้เลยสักจุด**
แก้ครบ 14 จุด (อยู่ในกรอบ "ถ้อยคำ" ที่ HANDOFF §4 อนุญาต) · รายการเต็ม: `01_HTML/_UX_CHECK_REPORT.md §3`

> จุดที่ร้ายแรงสุดคือ **ปุ่มในลิ้นชัก** (`เทียบราคาผู้ขาย (F073) — ยังไม่อยู่ในขอบเขตรอบนี้`) เพราะเป็น affordance จริงของฟีเจอร์ ไม่ใช่ scaffolding ของเมนูข้าง

### 3.3 ช่องว่าง 3 จุดที่ coverage รอบ 2 จับได้

| # | เจออะไร | ปิดอย่างไร |
|---|---|---|
| G1 | `FN-17..FN-24` ของ FUNCTION_CHECKLIST ไม่มีที่ลงใน FRD — เพราะ **รหัส `FN-xx` ชนกัน** ระหว่าง checklist (ธุรกิจ) กับ `03_LOGIC` (โค้ด) | เพิ่ม `00_OVERVIEW §0.12.1` ตาราง map ครบ 24 ข้อ + คำเตือนเรื่องรหัสชนกัน |
| G2 | `SC-01..SC-15` ของ PREBRIEF ขาดไป 10 ข้อจาก FRD | เพิ่ม `00_OVERVIEW §0.12.2` scenario coverage ครบ 15 ข้อ |
| G3 | `AT-14` · `AT-24` · `AT-27` (BR-06 ราคาประมาณ · BR-12 ผู้ขายที่แนะนำ) ประกาศไว้แต่ไม่มีเคสอ้างถึง | เติม trace + เพิ่มขั้นตอนจริง + เพิ่มเคสใหม่ **AI-45** แล้วยุบเข้า TC-10 |

> ปิดด้วยการ **เพิ่มเคสและเติม trace — ไม่ใช่ลดจำนวนกติกาลงให้ตัวเลขสวย**

### 3.4 สิ่งที่ตรวจแล้ว "ไม่พบปัญหา" (ต่างจากรอบก่อน ๆ)

- **`--z-*` tokens** — ไฟล์นี้ **ไม่ใช้ token indirection เลย** ใช้เลข z-index ตรง (19/20/50/51/60/70/80/90)
  → **ไม่ติดบั๊ก `z-index:auto`** ที่เจอทั้งใน F-SEC-TRANS และ F-SEC-LOCKOUT · ยืนยันด้วย `getComputedStyle` แล้ว
- **responsive** — วัด 7 ความกว้าง (1600→768) **ไม่มี horizontal overflow แม้แต่จุดเดียว** (ดีกว่ารอบ F-PUR-COMPARE ที่ 768 ล้น)
- **dead CSS** — เหลือ **1 คลาส** (`.line-collapse-panel`) เทียบกับ 50 คลาสในรอบ F-PUR-COMPARE
- **`class` ซ้ำใน tag เดียว** = 0 · **`+543`** = 0 · **runtime error** = 0 · **`node --check`** ผ่านทุกบล็อก
- **สิทธิ์ผู้อนุมัติเป็นของจริง** — `canActStep()` เทียบตัวตนผู้ใช้กับ slot ที่ค้างจริง ไม่ใช่ flag ตายแบบที่เจอใน F-PUR-COMPARE

---

## 4. ★ OQ / ASSUMED ที่ยังค้าง (ยกมาจาก HANDOFF §5 ครบ + เปิดใหม่ 3 ข้อ)

| OQ | เรื่อง | ค่าที่ใช้ไปก่อน | เจ้าของ |
|---|---|---|---|
| OQ-01 | ตัวเลขวงเงินอนุมัติ 3 ระดับ | 50,000 / 500,000 บาท `[ASSUMED]` | ผู้บริหารจัดซื้อ · **พี่เบิร์ด** |
| OQ-02 | แยกสายอนุมัติรายหน่วยงานไหม | ชุดเดียวทุกหน่วยงาน `[ASSUMED]` | เจ้าของกระบวนการจัดซื้อ |
| OQ-03 | ยกเลิกใบที่อนุมัติแล้วต้องอนุมัติซ้ำไหม | ไม่ต้อง (เหตุผล + ยืนยัน) `[ASSUMED]` | เจ้าของกระบวนการจัดซื้อ |
| OQ-04 | เมื่อ W7 พร้อม เปลี่ยน "เตือน" เป็น "บล็อก" ไหม | เตือนอย่างเดียว | เจ้าของ W7 + การเงิน |
| OQ-05 | หลายบริษัท/หลายสกุลเงินในเฟสถัดไป | หนึ่งบริษัท THB `[ASSUMED]` | สถาปนิกระบบ |
| OQ-06 | ผู้อนุมัติไม่อยู่ → ส่งต่อให้ใคร | ยังไม่มี | เจ้าของทะเบียน DOA |
| A-01 | รูปแบบผลตรวจงบ `{ok, remaining, budget_code}` | `[ASSUMED contract]` | เจ้าของ W7 |
| A-02 | เอกสารแนบ PDF/JPG/PNG/XLSX ≤10MB | `[ASSUMED]` | เจ้าของกระบวนการ |
| **OQ-07** ★ | **ถ้อยคำ SC-06 ใน PREBRIEF ไม่ตรงกับสิ่งที่ระบบทำ** — brief บอกว่าเตือนเมื่อยอดเกินวงเงินของขั้นที่เลือก แต่ระบบ resolve ชั้นอนุมัติจากยอดอัตโนมัติ สภาวะนั้นจึงเกิดไม่ได้ | ยึดพฤติกรรมระบบ · ตราไว้ที่ `07_LOCKED` LD-10 | **BA** |
| **OQ-08** ★ | ถ้าทีมอยากได้ชื่อขั้นที่ครอบ "บริการ/สินทรัพย์" ด้วย ต้องขอแก้ **iron rule #100 ระดับระบบ** ไม่ใช่แก้เฉพาะฟีเจอร์นี้ | คืนค่าที่ล็อก `รายการสินค้า` | **BA + เจ้าของ Pattern Q** |
| **OQ-09** ★ | **ปุ่มสาธิต 2 ปุ่มต้องถอดก่อน production** | **เก็บไว้** เพราะ QA ต้องใช้เข้าสถานะผิดพลาด (TC-04 · TC-18) | **ทีม dev ก่อน deploy** |

### `[AI-DEFAULT]` ที่เลนนี้ตัดสินแทน — **รอ BA ยืนยัน**
| Probe | default ที่ใช้ | อยู่ที่ |
|---|---|---|
| ผู้อนุมัติ 2 คนกดพร้อมกัน | optimistic lock · คนแรกชนะ · `PR_SLOT_ALREADY_DECIDED` | `05_RULES` CA-01 |
| ส่งอนุมัติซ้ำจากการกดรัว | idempotency key · `PR_DUPLICATE_SUBMIT` | `02_API` API-05 |
| แก้ใบชนกัน 2 หน้าต่าง | version check · `PR_VERSION_CONFLICT` | `02_API` API-04 |

### WARN ที่ไหลต่อ
- **#97 responsive** — sidebar ไม่ยุบเป็น rail ที่ 768px (ไม่มี overflow จึงไม่ block)
- **`Document Center`** ปรากฏบนจอ 2 จุด — เป็นชื่อโมดูลกลาง ไม่ใช่ศัพท์ภายใน · **ให้ BA เคาะว่าจะใช้ชื่อไทยแทนไหม** (ไม่แก้เองเพราะเป็นชื่อข้ามฟีเจอร์)
- **`.line-collapse-panel`** เป็น CSS ที่ไม่ถูกใช้ — animation ตอนยุบแถวไม่ได้ต่อ · ไม่กระทบการใช้งาน
- **รหัส `FN-xx` ถูกใช้ 2 ความหมาย** (checklist vs `03_LOGIC`) — รอบนี้แก้ด้วยตาราง map แต่ควรแก้ที่ต้นทาง

---

## 5. ยังไม่ได้ทำในเลนนี้

| # | เรื่อง | เหตุผล |
|---|---|---|
| 1 | **ส่งขึ้น OPS / zip / push** | ต้องรอ go-ahead จากผู้ใช้ — ห้ามทำเอง |
| 2 | **อัปเดต `st` ของ F072 ใน registry** | ทำหลังส่ง OPS จริงเท่านั้น |
| 3 | **BA sign-off ต่อ OQ-07 · OQ-08 และ `[AI-DEFAULT]` 3 ข้อ** | รอเจ้าของตอบ |
| 4 | **ถอดปุ่มสาธิต 2 ปุ่ม** | ตั้งใจเก็บไว้ให้ QA รอบนี้ (OQ-09) |
| 5 | **ทดสอบที่ต้องมี backend** | AT-20 · AT-22 · AT-23 · AT-25 · AT-30..AT-36 — ยอดฝั่งเซิร์ฟเวอร์ · optimistic lock · idempotency · version conflict · เลขเอกสารต่อเนื่อง · PO reference |
| 6 | **ต่อเครื่องกลางจริง** | DOA · เลขเอกสาร · แจ้งเตือน · 7C — เป็น Phase C |
| 7 | **เปลี่ยนตรวจงบจากจำลองเป็นจริง** | รอ F117 (W7) — Phase D |
| 8 | **`csq-declaration` / `pdfdoc` generator** | **ไม่มีใน repo นี้** — รอบนี้รับใบจาก BA lane แทน (ช่องว่างของ toolchain: 80 และ 28 ฟีเจอร์ใน registry) |

---

## 6. หมายเหตุเรื่องเครื่องมือ

**HANDOFF §7 อ้าง re-gate ชื่อ `html-review-fix-order`** ซึ่งเป็น skill ของ BA lane และ **ไม่มีใน repo นี้**
เลนนี้ใช้ **`qc-ux-html-checker` + `qc-coverage-checker`** ทำหน้าที่เดียวกัน (บันทึกไว้ที่ `07_LOCKED` LD-13)

**HTML ไม่ได้ regenerate ใหม่** — คัดจาก `1_HTML/` แล้วแก้เฉพาะ 2 เรื่องที่ด่านบังคับ (LD-08 · LD-09)
ไม่ได้รัน `html-generator-v9` เลย เพื่อให้ `_TECH_CHECK` ของต้นน้ำยังอ้างอิงได้ในส่วนที่ไม่ถูกแตะ
