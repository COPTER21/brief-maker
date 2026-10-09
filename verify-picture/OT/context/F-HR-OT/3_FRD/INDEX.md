# INDEX — FRD Pack · F-HR-OT · OT / Shift (โอที)

**Variant: FULL (9 ไฟล์ + INDEX + PRINT_SPEC)** · สร้างโดย `frd-generator-v6` Lane Mode v2 · 2026-08-29
**Phase 3.5: ✅ PASSED (A–M)** — รายงานเต็มอยู่ท้ายไฟล์นี้

## 📂 Pack Contents

| ไฟล์ | Audience | เนื้อหาหลัก |
|---|---|---|
| `00_OVERVIEW.md` | ทุกคน | Document control · Scope · Roles · Dependencies · **§0.12 Coverage Manifest (65 FN)** · **§0.13 Published OT Surface** · §0.14 Data Contract · §0.15 Soft Reference · **§0.16 Declaration Conformance** |
| `01_UI.md` | FE | **§1.0 Layout Decision Log (16 ข้อ)** · Page Inventory 4 หน้า · รายละเอียดต่อหน้า · COSO touchpoints · empty state |
| `02_API.md` | BE (HTTP) | 26 endpoint · contract ของ 8 ตัวที่มีสัญญาเฉพาะ · **§2.4 API → Logic Trace** · Cross-Module Contract |
| **`03_LOGIC.md`** | BE (ตรรกะ) | **§3.0 กลไกเพดานกับการเลือกสาย (หัวใจของแพ็ก)** · 67 Function · **12 Engine (ใหม่ 4)** · Trace Table |
| `04_DB.md` | DBA / BE | 7 ตาราง · classification ครบทุกคอลัมน์ · ER · migration · retention · performance |
| `05_RULES.md` | BE + QA | BR-01…BR-30 · State machine · Permission · VR-01…VR-22 · Edge Case 52 · **Error catalog 27 code** · Security · Compliance |
| `06_TESTS.md` | QA | **AT-01…AT-58** · **IA-01…IA-11 (invariant · ตกข้อใดข้อหนึ่ง = หยุด release)** · test data · DoD · cross-module 11 เคส · **microcopy verbatim** |
| `07_LOCKED_DECISIONS.md` | ทุกคน | **§7.0 Scope Lock 11 ข้อ (IMMUTABLE)** · LD-OT-01…12 · Convention deviation · **OQ 33 ข้อ** · tradeoff |
| **`PRINT_SPEC.md`** | ทีมทำเอกสาร | field mapping ของใบ OT · กติกาการพิมพ์ · **ช่องลายเซ็น 3/4 ช่อง** · checklist ก่อนส่งมอบ |
| `INDEX.md` | ทุกคน | ไฟล์นี้ |
| `UI_BRIEF_โอที.md` | FE + BA | (สร้างที่ S7) สรุปหน้าจอ + **Drift Log** |

## 🔍 Quick Nav by Question

| คำถาม | ไปที่ |
|---|---|
| **ทำไมชั้นที่ 3 ไม่ได้มาจากตัวเลขใน matrix ของ DOA** | **`03_LOGIC §3.0.2`** |
| **ใบถูกตีกลับกลางทางตอนไหน ทำไม** | **`03_LOGIC §3.0.3`** |
| **ขอเกินเวลาจริงแล้วต้องทำอย่างไร** | **`03_LOGIC §3.0.4`** |
| **Payroll ต้องอ่านอะไร ตรวจอะไรก่อนใช้** | **`00_OVERVIEW §0.13.3` + `§0.13.7`** |
| ทำไมใบที่ `approved` ยังไม่ถูกเผยแพร่ | `05_RULES BR-17` · `06_TESTS IA-01` |
| ทำไมไม่มีเพดานรายวัน/รายเดือน | `07_LOCKED §7.3 OQ-STD-OT5` · `05_RULES CA-08` |
| ทำไมไม่ปัดเศษชั่วโมง | `07_LOCKED LD-OT-07 · OQ-OT-16` |
| หน้าจอมีกี่หน้า route อะไร | `01_UI §1.1` |
| endpoint ไหนเรียก function อะไร | `02_API §2.4` · `03_LOGIC §3.3` |
| คอลัมน์ไหนเป็นข้อมูลอ่อนไหว | `04_DB §4.6` |
| error code มีอะไรบ้าง | `05_RULES §5.6` |
| ทดสอบอะไรบ้างก่อน release | `06_TESTS §6.4` |
| อะไรที่ห้ามเปลี่ยน | `07_LOCKED §7.0` |
| ใบ OT พิมพ์อย่างไร | **`PRINT_SPEC`** |

## 🔗 Cross-Reference Tables

### FN → ไฟล์
ตารางเต็ม **65 แถว** อยู่ที่ **`00_OVERVIEW §0.12.0`**

### BR → ไฟล์
ตารางเต็ม **30 แถว** อยู่ที่ **`00_OVERVIEW §0.12.2`** · ข้อความเต็มที่ `05_RULES §5.1`

### State → Transition → Event

| สถานะ | เข้าโดย | ออกโดย | event ที่ยิง |
|---|---|---|---|
| `draft` | T-1 | T-2 | — |
| `pending_approval` | T-2 · T-7 | T-3 · T-4 · T-5 · T-6 · T-7 | `ot_submitted` (+`ot_cap_exceeded`) |
| `approved` | T-4 | T-8 · T-9 | `ot_decided` · **`ot.approved` (FC)** |
| **`time_confirmed`** | T-8 | T-9 | **`ot.time_confirmed` (EC + FC)** |
| `rejected` | T-5 | — | `ot_decided` · **`ot.rejected` (FC avoided)** |
| `cancelled` | T-6 | — | `ot_cancelled` |
| `withdrawn` | T-9 | — | `ot_withdrawn` · **`ot.withdrawn` (EC + FC)** |
| *(ธง)* `needs_review` | T-11 | ถูกเคลียร์โดยการตัดสิน | `ot_confirm_pending` · **`ot.hours_adjusted`** เมื่อปรับ |
| *(ธง)* `period_locked` | T-10 | เปิดงวดที่ต้นทาง | — |

### Engine → ผู้ใช้

| Engine | สถานะ | เรียกจาก |
|---|---|---|
| `ot-cap-evaluation-engine` ⭐ NEW | candidate | `resolveCap` · `computeWeeklyAccumulated` · `computeOverCap` · `computeCapWarning` |
| `time-variance-engine` ⭐ NEW | candidate | `computeVariance` · `classifyVariance` |
| `overlap-detection-engine` ⭐ NEW | candidate | `checkOtOverlap` |
| `period-snapshot-freeze-engine` ⭐ NEW | candidate | `freezePeriodSummary` |
| `doa-resolution-engine` | existing | `resolveApprovalChain` |
| `document-numbering-engine` | existing | `issueDocNumber` |
| `document-store-engine` | existing | `storeApprovedCopy` |
| `notification-engine` | existing | `emitNotification` |
| `impact-valuation-engine` | existing | `emitImpactEvent` |
| `hr-config-resolve-client` | existing | `resolveOtRate` · `resolveCap` · `resolveDayType` |
| `attendance-resolve-client` | existing | `fetchAttendanceDay` |
| `leave-resolve-client` | existing | `checkLeaveConflict` |

## 🚨 R8 Verification Matrix

| เกณฑ์ | ผล |
|---|---|
| ทุก mutation API มี ≥1 Function/Engine | ✅ 26/26 |
| ทุก Function ใน `03_LOGIC §3.1` ถูก trace | ✅ 67/67 |
| ทุก Engine ใน `03_LOGIC §3.2` ถูก trace | ✅ 12/12 |
| ไม่มี orphan Function/Engine | ✅ |
| ไม่มี `createX`/`updateX`/สูตรคำนวณ ซ่อนใน `02_API` | ✅ |

## 📊 Pack Statistics

| มิติ | จำนวน |
|---|---:|
| ไฟล์ในแพ็ก | **11** (9 + INDEX + PRINT_SPEC) |
| หน้าจอ / route | 4 / 4 |
| API endpoint | 26 |
| Function | 67 |
| Engine | 12 (**ใหม่ 4**) |
| ตาราง DB | 7 |
| Business Rule | 30 |
| Validation Rule | 22 |
| Error code | 27 |
| Edge Case | 52 (☑ 24 · ☐ 28) |
| Acceptance Test | 58 |
| **Invariant Assertion** | **11** |
| Cross-module test | 11 |
| FN ที่ครอบ | **65 / 65** |
| Story ที่ครอบ | **65 / 65** |
| Functions Cut (ไม่รองรับ) | **17 / 17** |
| Open Question | **33** (31 จาก BRD + OQ-FRD-01 + OQ-FRD-02) |
| `[ASSUMED]` จาก HTML | 6 |
| `[AI-DEFAULT]` จาก Phase 2.5 | 7 |
| NTF event | 7 |
| CSQ event | 5 (ท่อ EC + FC) |
| DOA action / matrix | 6 / 2 |

## 🎯 Reading Order Recommendation

1. `00_OVERVIEW §0.3` (ขอบเขต) → `§0.13` (สิ่งที่ feature อื่นอ่านได้)
2. **`03_LOGIC §3.0`** — กลไกเพดานกับการเลือกสาย (**อ่านก่อนเขียนโค้ดใด ๆ ที่แตะ `over_cap`**)
3. `01_UI §1.0` + `§1.2` (จอจริงหน้าตาอย่างไร)
4. `04_DB` → `02_API` → `03_LOGIC §3.1–§3.3`
5. `05_RULES` (ทั้งไฟล์) → `06_TESTS §6.2 IA` (สิ่งที่ห้ามพลาด)
6. `07_LOCKED §7.0` + `§7.3` (อะไรห้ามเปลี่ยน · อะไรยังไม่เคาะ)
7. `PRINT_SPEC` (เมื่อถึงงานเอกสาร)

## Coverage Manifest Pointer ⭐
**`00_OVERVIEW §0.12`** — FN 65/65 · Story 65/65 · BR 30/30 · Edge 52/52 · Functions Cut 17/17 · **ไม่มีแถวที่ "อยู่ที่" ว่าง**

---

## 🔍 Phase 3.5 Verification Report — FRD F-HR-OT

```
### A. Pack Completeness
- [x] Variant decision (FULL) match เกณฑ์ fallback จาก BRD ✅ (states=7 ≥ 4 · approval=Yes)
- [x] All expected files generated (9 + INDEX) ✅
- [x] 03_LOGIC.md exists ✅
- [x] INDEX.md cross-references all files ✅
- [x] **PRINT_SPEC.md present** ✅ (feature มีท่อเอกสาร PDF → บังคับ)

### B. Function/API Coverage
- [x] 26 endpoint มี contract ครบ (8 ตัวที่มีสัญญาเฉพาะเขียนเต็ม · ที่เหลืออยู่ในตาราง §2.1 + §2.4) ✅
- [x] ทุก mutation API ระบุ Idempotency + row_version ✅

### C. R8 Logic Traceability
- [x] ทุก mutation API มี ≥1 Function/Engine ✅ 26/26
- [x] ทุก Function ถูก trace ✅ 67/67
- [x] ทุก Engine ถูก trace ✅ 12/12
- [x] ไม่มี orphan ✅

### D. API ↔ DB Linkage
- [x] ทุก API ที่เขียนข้อมูล ชี้ตารางที่มีอยู่จริงใน 04_DB ✅
- [x] read model (API-20/21) map กับ T_ot_request(+line) · T_ot_period_summary ✅

### E. UI ↔ API Cross-reference
- [x] P-01 ปุ่ม "ส่งอนุมัติ" → API-06 ✅
- [x] P-01 modal 10 ตัว → API-06/08/09/10/11/12/13/15/24/26 ✅
- [x] P-02 → API-05 ✅ · P-03 → API-13/14 ✅ · P-04 → API-21/22 ✅

### F. Engine Iron Rules (CUBIC 3-layer)
- [x] ไม่มี Engine อ้างอิงสิ่งที่เป็น HTTP ✅
- [x] input/output เป็น object ล้วน ✅
- [x] feature ไม่ข้าม API ไปเรียก Engine ตรง ✅
- [x] **Engine ใหม่ทั้ง 4 ตัวไม่มีค่านโยบายอยู่ข้างใน (ค่าเป็น input เสมอ)** ✅

### G. Logic Placement Compliance
- [x] ไม่มี createX/updateX แอบใน 02_API ✅
- [x] ไม่มี pure calculation แอบใน 02_API ✅
- [x] logic ที่ควรอยู่ 03_LOGIC อยู่จริงทั้งหมด ✅

### H. Security Bible Application
- [x] Preset P6 เลือกแล้ว + Must 9 ควบคุมครบ ✅ (05_RULES §5.7)
- [x] บันทึกเหตุผลที่ไม่เลือก P2/P4/P9 ✅ (BRD §16.1)

### I. Convention Compliance
- [x] API path `/api/v1/ot/*` ✅
- [x] field_key = snake_case ✅
- [x] Function = camelCase ✅
- [x] Engine = kebab-case ✅
- [x] Error code = UPPER_SNAKE ✅

### J. Data Classification (R10)
- [x] ทุกคอลัมน์ใน 04_DB §4.2 มี Classification ✅
- [x] ทุกคอลัมน์มี PII flag ✅
- [x] §4.5 Field Dictionary มีคอลัมน์ Classification ✅
- [x] §4.6 ครบ 6 subsection (.1–.6) ✅
- [x] 00_OVERVIEW §0.7.1 ระบุระดับสูงสุด (Confidential) ✅
- [x] 05_RULES §5.7 มีส่วน masking/classification ✅
- [x] ไม่มี default = Public ✅ (ไม่มีคอลัมน์ Public เลย)
- [x] **ไม่มี Restricted → ไม่ต้อง wire Restricted Resources** ✅ (บันทึกเหตุผลไว้ที่ §0.7.1)

### K. Coverage Manifest (R13)
- [x] ทุก Story ใน BRD §7 (65) มีแถว ✅
- [x] ทุก Rule ใน BRD §9 (30) มีแถว ✅
- [x] ทุก Edge ☑ (24) มีแถว ✅ · ☐ (28) มีแถว ✅
- [x] **ทุก FN (65) มีแถวพร้อมคอลัมน์ UI/API/LOGIC/RULES/TESTS** ✅
- [x] **Functions Cut 17/17 อยู่ในแมนิเฟสต์** ✅
- [x] ไม่มีแถวที่ "อยู่ที่" ว่าง ✅

### L. Scope Lock + Value Stream (R11/R12)
- [x] Scope Lock 11 ข้อ import ครบจาก BRD §3.4 → 07_LOCKED §7.0 ✅
- [x] ไม่มี spec ใดในแพ็กขัด LOCK ✅
- [x] 02_API มี Cross-Module Contract ครบตาม BRD §12.1 ✅
- [x] 06_TESTS มี cross-module case ≥1 ต่อ downstream ที่มี data ไหล ✅ (CM-01…CM-11)

### M. HTML Alignment (v6.1)
- [x] จำนวนหน้าใน 01_UI = จำนวน route ใน HTML **เป๊ะ (4 = 4)** ✅
- [x] ทุก route ใน 01_UI มีจริงใน HTML (`TAB_HASH`) ✅
- [x] Pattern (observed) ตรงกับที่จอใช้จริง — spot-check 5 จุด: `WSTEPS` 5 ขั้น ✅ · `VTABS` 4 แท็บ ✅ · `table.dline` 10 คอลัมน์ไม่มีเงิน ✅ · `.slot-row` ผันตาม `over_cap` ✅ · `filterRow()` 1 แถว ✅
- [x] 06_TESTS expected text ตรง verbatim — spot-check ≥5 ข้อความ: `ยังไม่ออกเลข` ✅ · `ยังไม่ได้เลือกคนในตำแหน่งนี้` ✅ · `ไม่พบใบขอ OT ตามเงื่อนไข` ✅ · `เกินเพดาน — สาย 3 ขั้น` ✅ · `ขั้นที่เพิ่มจากธงเกินเพดาน` ✅
- [x] ไม่พบ HTML-STANDARD CONFLICT ✅
- [!] **บันทึก 1 ข้อขัดแย้งที่ต้องให้คนตัดสิน (ไม่ใช่ conflict ของ spec):** `pill-info` โทนน้ำเงินของชุดฐานถูกใช้กับสถานะ "ยืนยันแล้ว" ซึ่งอยู่นอกจานสี CI ของบ้าน แต่ **Rule 69 ห้ามแก้ชุดฐาน** → `01_UI LD-UI-14` · `07_LOCKED CV-02` · ยกเข้า Drift Log ที่ S7 + `_NOTIFY.md`

### Declaration Conformance (Lane Mode v2)
- [x] NTF 7 = 7 ✅ · CSQ 5 = 5 (EC+FC) ✅ · DOA 6 action/2 matrix ✅ · DOCCFG 1 ✅ · PDFDOC 1 ✅
- [x] **ไม่มี event ใหม่ที่ FRD คิดขึ้นเอง** ✅
- [x] **สองชุด event disjoint — ไม่มีชื่อซ้ำแม้แต่ตัวเดียว** ✅
- [x] **ไม่มีใบใดประกาศซ้ำ `doa_pending` / `doa_result` / DC ระดับเอกสาร** ✅

### Verdict
✅ **All checks passed (A–M + Declaration Conformance) → deliver Pack**
   หมายเหตุ 1 ข้อ (UX-01) เป็นความขัดแย้งระหว่างมาตรฐานสองข้อที่ต้องให้คนตัดสิน — ไม่ใช่ข้อบกพร่องของแพ็ก
```
