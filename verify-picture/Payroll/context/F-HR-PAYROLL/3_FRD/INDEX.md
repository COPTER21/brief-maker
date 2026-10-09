# INDEX — FRD Pack · F-HR-PAYROLL · Payroll (เงินเดือน)

> **Pack Variant: FULL** (9 ไฟล์ + INDEX + PRINT_SPEC) · `frd-generator-v6.1` Lane Mode v2 · 2026-08-30
> **ประโยคที่นิยาม pack นี้:** ต้นทางทั้งหกส่ง **ชั่วโมง วัน และธง — ไม่มีเงินเลย** · **ที่นี่คือที่ที่ชั่วโมงกลายเป็นเงิน** · และเพราะยังไม่มีค่าตามกฎหมายให้อ่าน **ระบบจึงถูกออกแบบให้ไม่จ่ายเลย แทนที่จะจ่ายผิด**

## 📂 Pack Contents

| ไฟล์ | ขนาด | ใครอ่าน | สาระสำคัญ |
|---|---:|---|---|
| `00_OVERVIEW.md` | ~84 KB | ทุกคน | scope · roles · dependencies · **§0.12 Coverage Manifest (80 FN)** · **§0.13 Published Payroll Surface** · **§0.14 invariant `PI-1…PI-10`** · §0.16 declaration conformance |
| `01_UI.md` | ~34 KB | FE | 4 route + 3 overlay · **Layout Decision Log 15 ข้อ** · §1.6 ตารางขอบเขต 10 แถว · **§1.7 microcopy 28 ข้อ** |
| `02_API.md` | ~21 KB | BE (HTTP) | 34 endpoint + 7 cross-module read + 6 outbound surface · **§2.6 error catalog 18 code** |
| `03_LOGIC.md` ⭐ | ~80 KB | BE (logic) | **§3.0 กติกาแกน 4 ข้อ** · §3.1 Functions 59 ตัว · **§3.2 Engines (7 candidate ใหม่)** · §3.3 Trace |
| `04_DB.md` | ~21 KB | DBA / BE | 7 ตาราง + Classification ทุกคอลัมน์ + **CHECK constraint ที่บังคับ fail-closed ที่ระดับฐาน** |
| `05_RULES.md` | ~39 KB | BE + QA | BR 43 · VR 24 · transition 15 · edge 35 · **§5.9 event catalog (7 NTF + 8 CSQ)** |
| `06_TESTS.md` | ~76 KB | QA | **AT-01…AT-120** · **IA-01…IA-22 (invariant)** · CM-01…CM-12 · §6.7 microcopy verbatim |
| `07_LOCKED_DECISIONS.md` | ~19 KB | ทุกคน | **§7.0 Scope Lock 16 ข้อ** · §7.1 LD-01…LD-18 · §7.2 DIVERGENCE · §7.3 `[AI-DEFAULT]` 12 ข้อ |
| `PRINT_SPEC.md` | ~19 KB | FE + BE + QA | สลิป A4 1 หน้า · field mapping · **§P.5 all-or-nothing** |
| `INDEX.md` | (ไฟล์นี้) | ทุกคน | cross-reference · R8 matrix · **Phase 3.5 Verification Report** |
| `UI_BRIEF_เงินเดือน.md` | (S7) | FE + BA | Drift Log · สกัดจาก HTML สุดท้าย |

## 🔍 Quick Nav by Question

| คำถาม | ไปที่ |
|---|---|
| **ทำไมตัวเลขเป็นช่องว่างไม่ใช่ 0?** | `03_LOGIC §3.0.1` (G-2) · `05_RULES BR-15` · `06_TESTS IA-08` |
| **ทำไมส่งอนุมัติไม่ได้?** | `03_LOGIC §3.0.1` (G-6) · `F-36` · `05_RULES VR-12` · `06_TESTS IA-11` |
| **27 คีย์ที่ขาดคืออะไรบ้าง?** | `03_LOGIC §3.0.1` ตาราง 6 กลุ่ม · `00_OVERVIEW §0.8` |
| **รอบที่ปิดแล้วแก้อะไรได้บ้าง?** | `03_LOGIC §3.0.3` (C-1…C-7) · `F-44` · `06_TESTS IA-15 · IA-17` |
| **"retro" ในระบบนี้แปลว่าอะไร?** | `03_LOGIC §3.0.3` แผนภาพรอบปรับปรุง · `F-47` · `ENG-PAY-05` |
| **ทำไมไม่ส่งยอดเงินเข้า DOA?** | `03_LOGIC §3.0.4` · `BRD §5.4.2` · `06_TESTS IA-12 · IA-13` |
| **เลขรอบกับเลขสลิปออกเมื่อไร?** | `03_LOGIC §3.0.4` ตารางเปรียบเทียบ · `F-01` · `F-41` |
| **ใครเห็นสลิปของใครได้?** | `PRINT_SPEC §P.5` · `F-54` · `06_TESTS PT-01…PT-04` |
| **ปลายทางอ่านอะไรจากที่นี่ได้?** | `00_OVERVIEW §0.13` (PS-1 · PS-2 · PS-3 · HK-1) |
| **feature นี้เขียนกลับต้นทางไหม?** | `02_API §2.5.1` — **ไม่มีเลย** · `06_TESTS IA-04` |
| **ลำดับการคำนวณเป็นอย่างไร?** | `03_LOGIC §3.0.5` · `ENG-PAY-01` |
| **ต้องลงทะเบียนอะไรที่ baseline บ้าง?** | `BRD §14.1` (14 รายการ) · `00_OVERVIEW §0.16` |
| **อะไรบ้างที่ยังต้องเคาะ?** | `BRD §15` (28 OQ) · `07_LOCKED §7.3` (12 `[AI-DEFAULT]`) |

## 🔗 Cross-Reference Tables

### FN → ไฟล์
`00_OVERVIEW §0.12.0` — **80 แถวครบ**

### BR → ไฟล์
`00_OVERVIEW §0.12.1` — **43 แถวครบ**

### API → Function/Engine (R8 anchor)
`03_LOGIC §3.3` — **34 endpoint + 1 event listener**

### Function → API (ย้อนกลับ)

| Function | ถูกเรียกจาก |
|---|---|
| `F-01` · `F-02` | API-03 |
| `F-03` | API-04 · API-06 |
| `F-04` | API-05 |
| `F-05` · `F-06` · `F-07` | API-06 · API-07 · API-08 |
| `F-08` | API-08 |
| `F-09` | API-09 |
| `F-10` | API-06 · API-11 |
| `F-11` · `F-12` · `F-13` · `F-14` | API-10 · API-14 |
| `F-15`…`F-27` · `F-29` | API-12 · API-13 |
| `F-28` | API-15 |
| `F-30` · `F-31` | API-12 · API-16 |
| `F-32` | API-17 |
| `F-33` | API-18 · API-29 |
| `F-34` · `F-35` · `F-36` | API-19 · API-20 |
| `F-37` | API-21 |
| `F-38` · `F-39` | API-22 |
| `F-40`…`F-43` | API-23 |
| **`F-44`** | **ทุก mutation API (14 ตัว)** |
| `F-45` | EVT-01 · API-31 |
| `F-46` · `F-47` · `F-48` · `F-49` | API-03 · API-32 |
| `F-50` · `F-51` | API-27 · API-28 |
| `F-52` | API-29 |
| `F-53` | API-23 · API-25 · API-33 |
| `F-54` | API-24 · API-25 · API-26 · API-34 |
| `F-55` · `F-56` | API-23 · API-25 · API-26 · API-27 |
| `F-57` | ทุก mutation · API-30 |
| `F-58` | EVT-01 |
| `F-59` | ทุก read API ที่มี field เป็นเงิน |

### Engine → Function

| Engine | ถูกเรียกผ่าน |
|---|---|
| `ENG-PAY-01` gross-to-net | `F-15` (ผ่าน `F-16`…`F-25`) |
| `ENG-PAY-02` statutory-deduction | `F-22` · `F-23` · `F-24` |
| `ENG-PAY-03` input-snapshot | `F-05` · `F-06` |
| `ENG-PAY-04` variance-compare | `F-30` · `F-31` |
| `ENG-PAY-05` retro-difference | `F-47` |
| `ENG-PAY-06` bank-file | `F-50` |
| `ENG-PAY-07` gl-payload | `F-52` |
| `doa-resolve` (baseline) | `F-35` |
| `ENG-DOC-NUM` (baseline) | `F-01` · `F-41` |
| `ENG-DOC-STORE` (baseline) | `F-42` · `F-54` |
| `ENG-NOTIFY` (baseline) | `F-55` |
| `ENG-CSQ` (baseline) | `F-56` |
| Policy Center (baseline) | `F-54` · `F-59` |

## 🚨 R8 Verification Matrix

| เกณฑ์ | ผล |
|---|:---:|
| mutation API ทุกตัวมี Function ≥ 1 ใน trace | ✅ **14 / 14** |
| Function ทุกตัวใน §3.1 ถูก trace อย่างน้อย 1 API | ✅ **59 / 59** |
| Engine ทุกตัวถูก trace ผ่าน Function (ไม่มี API เรียก engine ตรง) | ✅ **13 / 13** |
| orphan Function / Engine | ✅ **0** |
| logic ซ่อนใน `02_API` | ✅ **0** |
| ⭐ mutation ทุกตัวเรียก `F-44` เป็นบรรทัดแรก | ✅ **14 / 14** |

## 📊 Pack Statistics

| ตัววัด | จำนวน |
|---|---:|
| ไฟล์ใน pack | **10** (+ UI_BRIEF ที่ S7) |
| FN ที่ครอบ | **80 / 80** |
| Business Rules | **43** |
| Validation Rules | **24** |
| Transition | **15** (รอบ 12 + T-∅ + สลิป 2) |
| Edge Cases | **35** (☑ 26 · ☐ 9) |
| Error Codes | **18** |
| Functions | **59** |
| **Engines (candidate ใหม่)** | **7** |
| Engines (baseline ที่เรียกใช้) | **6** |
| API endpoint | **34** + 7 cross-read + 6 outbound + 1 listener |
| ตาราง | **7** |
| Acceptance Tests | **120** |
| **Invariant Assertions** | **22** |
| Cross-Module Tests | **12** |
| Scope Lock | **16** |
| Locked Decisions | **18** |
| `[AI-DEFAULT]` | **12** |
| DIVERGENCE | **2** (+ CV 3 ข้อ) |
| NTF events | **7** |
| CSQ events | **8** (FC · AC · EC · SecC) |

## 🎯 Reading Order Recommendation

1. `00_OVERVIEW §0.3.3` — สามข้อที่ต้องแม่นที่สุด
2. **`03_LOGIC §3.0`** ⭐ — กติกาแกนสี่ข้อ (อ่านก่อนเขียนโค้ดบรรทัดแรก)
3. `07_LOCKED_DECISIONS §7.0` — 16 LOCK
4. `01_UI` (FE) / `02_API` + `04_DB` (BE) / `05_RULES` + `06_TESTS` (QA)
5. `00_OVERVIEW §0.13` — สิ่งที่ปลายทางจะมาอ่าน
6. `PRINT_SPEC` — เมื่อทำสลิป

## Coverage Manifest Pointer ⭐

`00_OVERVIEW §0.12` — §0.12.0 FN 80 แถว · §0.12.1 BR 43 แถว · §0.12.2 Edge · §0.12.3 Story

---

## 🔍 Phase 3.5 Verification Report — FRD F-HR-PAYROLL

### A. Pack Completeness
- [x] Variant decision = **FULL** — fallback จาก BRD: `pages=7 · states=9 · approval=Yes · money=Yes` ✅
- [x] ไฟล์ครบตาม FULL (9 + INDEX) **+ `PRINT_SPEC.md`** (pdfdoc present → บังคับ) ✅ **10 / 10**
- [x] `03_LOGIC.md` มี (บังคับทุก variant) ✅
- [x] `INDEX.md` cross-reference ครบทุกไฟล์ ✅

### B. Function/API Coverage
- [x] mutation API ทั้ง 14 ตัว มีสัญญาครบ (body · response · error) ✅
- [x] read API ทั้ง 20 ตัว มี response shape ✅
- [x] cross-module read 7 ตัว ระบุพารามิเตอร์บังคับครบ ✅

### C. R8 Logic Traceability ⭐
- [x] ทุก mutation API มี Function/Engine ≥ 1 ใน trace ✅ 14/14
- [x] ทุก Function ใน §3.1 ถูก trace ≥ 1 API ✅ 59/59
- [x] Engine ทุกตัวถูก trace ผ่าน Function ✅ 13/13
- [x] ไม่มี orphan Function/Engine ✅

### D. API ↔ DB Linkage
- [x] ทุก API ระบุตารางที่อ่าน/เขียน และตารางนั้นมีใน `04_DB` ✅ (7 ตาราง)

### E. UI ↔ API Cross-reference
- [x] ทุก action บน `01_UI` มี API รองรับ — สร้างรอบ→API-03 · ดึง→API-06 · คำนวณ→API-12 · ส่งอนุมัติ→API-19 · ปิดรอบ→API-23 · ไฟล์โอน→API-27 · สลิป→API-25/26 ✅
- [x] ไม่มีปุ่มบน UI ที่ไม่มี API และไม่มี API ที่ไม่มีที่ยืนบนจอ (ยกเว้น outbound surface ซึ่งเป็นของปลายทาง) ✅

### F. Engine Iron Rules (CUBIC 3-layer)
- [x] ไม่มี engine ตัวใดอ้าง HTTP term (`req`/`res`/`header`/`status`) ✅
- [x] input/output ของทุก engine เป็น pure object ✅
- [x] ไม่มี API ที่เรียก engine ตรงโดยข้าม Function ✅

### G. Logic Placement Compliance ⭐
- [x] ไม่มี `createX/updateX` ซ่อนใน `02_API` — ทั้งหมดอยู่ `03_LOGIC §3.1` ✅
- [x] ไม่มี pure calculation ซ่อนใน `02_API` — ทั้งหมดอยู่ `§3.2` ✅
- [x] logic ที่เข้าเกณฑ์ matrix #3–8 อยู่ใน `03_LOGIC` จริง ✅

### H. Security Bible Application
- [x] trigger ที่พบ: ข้อมูลการเงินส่วนบุคคล · PII · สายอนุมัติหลายขั้น · การส่งออกไฟล์ · การเข้าถึงเอกสารข้ามบุคคล
- [x] domain ที่ใช้: COSO (SoD · Maker-Checker) · ISO 27001 (masking · classification) · PDPA (PII บนสลิป) · preset `P6` + `P4` + `P2` ✅ (`BRD §16`)

### I. Convention Compliance
- [x] API path `/api/v1/payroll/...` ✅ · `field_key` = `snake_case` ✅ · Function code = `camelCase` ✅ · Engine code = `kebab-case` ✅ · Error code = `UPPER_SNAKE` ✅

### J. Data Classification (R10) ⭐
- [x] ทุกคอลัมน์ใน `04_DB §4.2` มี `Classification` ✅ · มีธง `PII` ✅
- [x] `§4.5` Field Dictionary มีคอลัมน์ Classification ✅
- [x] `§4.6` ครบ 6 subsections (.1–.6) ✅
- [x] `00_OVERVIEW §0.7.1` ระบุระดับสูงสุด = **Restricted** ✅
- [x] `05_RULES §5.7` มี subsection `D-CLASS` (7 ข้อ) ✅
- [x] ⭐ **ไม่มีคอลัมน์ใดเป็น `Public`** ✅ (`§4.6.6`)
- [x] Restricted fields → flag ใน Open Questions (**wire Restricted Resources ก่อน go-live**) ✅ (`§0.8`)

### K. Coverage Manifest (R13) ⭐
- [x] ทุก Story ใน `BRD §7` มีแถวใน `§0.12` ✅ (62 Story ผ่านคอลัมน์ Story ของ §0.12.0)
- [x] ทุก Rule ใน `BRD §9` มีแถว ✅ **43 / 43**
- [x] ทุก Edge ☑ ใน `BRD §10.1` มีแถว ✅ **26 / 26** · Edge ☐ 9 ข้ออยู่ใน `§0.12.2` + OQ
- [x] ⭐ **ทุก FN 80 ข้อมีแถวครบ** ✅ **80 / 80**
- [x] ไม่มีแถวที่ "อยู่ที่" ว่างทั้งแถว ✅

### L. Scope Lock + Value Stream (R11/R12) ⭐
- [x] Scope Lock imported ครบตาม `BRD §3.4` → `07_LOCKED §7.0` ✅ **16 / 16**
- [x] ไม่มี spec ใดใน pack ขัด LOCK ✅
- [x] `02_API` มี Cross-Module Contract ครบตาม `BRD §12.1` downstream ✅ (`§2.5.2` 6 surface)
- [x] `06_TESTS` มี cross-module case ≥ 1 ต่อ downstream ที่มี data ไหล ✅ (`CM-01…CM-12`)

### M. HTML Alignment (v6.1) ⭐
- [x] **จำนวนหน้าใน `01_UI` = จำนวน route ใน HTML เป๊ะ** — 4 route (`#/payroll/runs` · `#/payroll/queue` · `#/payroll/slips` · `#/payroll/run/<no>`) ✅ **ไม่มีหน้าที่แต่งขึ้น ไม่มีหน้าที่หายไป**
  - หมายเหตุ: `BRD §14.6` นับ overlay รวมเป็น 7 "หน้าจอ" — บันทึกไว้ที่ `LD-UI-02` · `07_LOCKED CV-03` · **ไม่ใช่ drift**
- [x] ทุก route ใน `01_UI` มีจริงใน HTML ✅ (`_lane/COVERAGE_MAP.md §1`)
- [x] Pattern (observed) ตรงกับที่จอใช้จริง — spot-check 3 หน้า: **P-04 แท็บ 7 ตัว** (`RTABS`) · **OV-02 drawer สลิป 4 แท็บล็อก** (`dwSlip`) · **OV-01 wizard 4 ขั้น** (`dwCreate` · `STEPS`) ✅
- [x] `06_TESTS` expected text ตรง verbatim — spot-check 6 ข้อความ: `รอบ <เลขที่> ปิดแล้ว แก้ไม่ได้` · `ไม่มีเส้นทางออกจากสถานะปิดรอบแล้วในเครื่องสถานะ ไม่ใช่แค่ซ่อนปุ่ม` · `ไม่มีการลบในระบบนี้ — ทุกอย่างเก็บแบบเพิ่มอย่างเดียว` · `ต้องแก้ก่อน — ไม่มีอัตราค่าจ้าง ณ วันจ่าย` · `คุณไม่มีสิทธิ์เปิดสลิปของพนักงานคนอื่น` · `ดึงข้อมูลใหม่แล้ว — ผลการคำนวณเดิมถูกล้างทิ้ง` ✅
- [x] ชื่อสถานะ 9 ค่า · ชื่อแท็บ 7+3 · ชื่อ 4 ขั้นของ wizard ตรงกับค่าคงที่ใน HTML (`RST` · `RTABS` · `TABS` · `STEPS`) ✅

### N. Declaration Conformance (Lane Mode v2 — เพิ่มเติมจาก A–M)
- [x] **event ⊆ brief** ✅ — NTF **7 = 7** · CSQ **8 = 8** · **ไม่มี event ที่ FRD คิดขึ้นเอง**
- [x] ⭐ สองชุด **disjoint** — ไม่มีชื่อซ้ำที่เป็นการประกาศซ้ำ · `payroll.run_closed`/`payroll.run_reversed` ที่ปรากฏทั้งสองชุดเป็น **เหตุการณ์เดียวที่ fan-out** (ยืนยันที่ `IA-21`) ✅
- [x] ⭐ **ไม่ re-declare `doa_pending` / `doa_result`** ✅
- [x] ⭐ **ไม่ประกาศ OC · DC ระดับเอกสาร · SC** ✅
- [x] DOA 5 action = 5 · matrix 5 set = 5 · **0 วงเงิน** ✅ · DOCCFG 2 = 2 ✅ · PDFDOC 1 rendition = 1 ✅
- [x] DIVERGENCE ของท่อประกาศ: **ไม่มี** (`DECL.json.divergence = []`) ✅

### Verdict

```
═══════════════════════════════════════════════════════
Phase 3.5 Mechanical Verification — FRD F-HR-PAYROLL
───────────────────────────────────────────────────────
A ✅  B ✅  C ✅  D ✅  E ✅  F ✅  G ✅
H ✅  I ✅  J ✅  K ✅  L ✅  M ✅  (+N ✅)

ผ่าน 13 / 13 section (A–M) + N (Lane Mode v2)
ไม่ผ่าน 0

สถานะ: ✅ PASSED — deliver Pack
═══════════════════════════════════════════════════════
```

**หมายเหตุถึงทีมถัดไป (S6 TC · S7 UI Brief):**
1. ⭐ **`IA-01…IA-22` ต้องกลายเป็นเคสทดสอบจริง** — โดยเฉพาะ `IA-07` (grep หาอัตราที่ hardcode) · `IA-08` (5 ชั้นที่ `NULL` อาจกลายเป็น `0`) · `IA-12` (อ่าน payload จริง) · `IA-15` · `IA-17` (`updated_at` ไม่ขยับ)
2. **เส้นทางที่ต้องไม่พลาดใน TC:** บล็อกส่งอนุมัติ · `amount = null` ไม่เป็น 0 · ทั้ง 6 คำสั่งถูกปฏิเสธบนรอบที่ปิด · event หลังปิดรอบเข้าคิว · รอบปรับปรุงอ้างรอบเดิม · ดึงใหม่ล้างผลคำนวณ · การเลือกสายตามธง · สลิป 403 · ไฟล์โอนยิง SecC
3. **DIVERGENCE-1 · DIVERGENCE-2 · `PAY-DEMO-1` · `A-1…A-8` ต้องเดินทางต่อไปถึง UI Brief** — ห้ามหายระหว่างทาง
