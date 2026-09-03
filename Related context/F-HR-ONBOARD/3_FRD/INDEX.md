# INDEX — FRD Pack · F-HR-ONBOARD · On/Offboard (เข้าออกงาน)

> **variant: FULL** · 9 ไฟล์ · `frd-generator-v6` Lane Mode v2 · 2026-08-29
> ⭐ **แพ็กนี้ไม่มี `PRINT_SPEC.md`** — feature ไม่มีท่อ `doccfg` และ `pdfdoc` (`5_DECLARATIONS/NOT_NEEDED.md`) · **ไม่ใช่ไฟล์ที่หาย แต่คือไฟล์ที่ไม่มีตั้งแต่ต้น**

---

## 📂 Pack Contents

| ไฟล์ | เนื้อหา | ขนาดโดยประมาณ |
|---|---|---|
| `00_OVERVIEW.md` | Document Control · Scope · COSO · Dependencies · Stack · Security · **§0.12 Coverage Manifest (88 FN)** · **§0.13 Published Employment Window** · **§0.14 Access Revocation Contract** · §0.15 Soft-Reference · **§0.16 Declaration Conformance** | ~88 KB |
| `01_UI.md` | **§1.0 Layout Decision Log (14 ข้อ)** · Page Inventory 5 หน้า · รายละเอียดต่อหน้า · **§1.3 Microcopy** · **§1.4 สิ่งที่ไม่มี (18 ข้อ)** | ~36 KB |
| `02_API.md` | กติกา 10 ข้อ · endpoint 24 ตัว · **§2.2.1 ทำไมไม่มี endpoint เขียนสิทธิ์** · **§2.3 Cross-Module Contract** · Error catalog | ~22 KB |
| `03_LOGIC.md` | ⭐ **§3.0 กลไกการเพิกถอนทั้งหมด** · Functions 48 ตัว · **Engines 7 ตัว** · §3.3 Trace Table (R8) · §3.4 ลำดับที่ผิดแล้วพัง | ~50 KB |
| `04_DB.md` | 6 ตาราง · **§4.6 Data Classification** · ER · Index · Migration | ~24 KB |
| `05_RULES.md` | BR-01…BR-32 · State Machine · Permission Matrix · **Edge 45 ข้อ** · VR-01…VR-20 · Security | ~33 KB |
| `06_TESTS.md` | Test Data 14 ชุด · **IA-01…IA-10 (invariant)** · **AT-01…AT-88 (1 ต่อ FN)** · AT-89…AT-133 (edge) · DoD · XT-01…XT-07 · Microcopy verbatim | ~47 KB |
| `07_LOCKED_DECISIONS.md` | **§7.0 Scope Lock 11 ข้อ (IMMUTABLE)** · LD-ONB-01…14 · Convention Deviation · OQ 30 ข้อ · Tradeoff | ~22 KB |
| `INDEX.md` | ไฟล์นี้ + **Phase 3.5 Verification Report** | — |
| *(S7)* `UI_BRIEF_เข้าออกงาน.md` | สรุปหน้าจอสำหรับ FE + Drift Log | — |

---

## 🔍 Quick Nav by Question

| คำถาม | ไปที่ |
|---|---|
| **"การเพิกถอนทำงานอย่างไร"** ⭐ | `03_LOGIC §3.0` (ทั้งส่วน) |
| "ทำไมการเพิกถอนไม่ต้องมีใครอนุมัติ" | `2_BRD §4.3.2` · `00_OVERVIEW §0.14 AR-7` · `07_LOCKED LD-ONB-02` |
| "รายการสิทธิ์ปิดได้เมื่อไร" | `03_LOGIC §3.0.4` · `05_RULES BR-04` · `06_TESTS IA-01` |
| "ธงเพิกถอนค้างทำงานอย่างไร" | `03_LOGIC §3.0.5` · `05_RULES §5.2.3` |
| "ยกเลิกหลังเพิกถอนแล้วเกิดอะไร" | `03_LOGIC §3.0.7 · §3.4.4` |
| **"ปลายทางอ่านอะไรจากที่นี่"** | `00_OVERVIEW §0.13` · `02_API §2.3` |
| "ทำไมไม่ประกาศท่อ OC" | `00_OVERVIEW §0.16.3` |
| "ทำไมไม่มี `PRINT_SPEC.md`" | หัวไฟล์นี้ · `00_OVERVIEW` หัวไฟล์ · `NOT_NEEDED.md` |
| "หน้าจอมีอะไรบ้าง" | `01_UI §1.1 · §1.2` |
| "อะไรที่ระบบตั้งใจไม่ทำ" | `01_UI §1.4` · `00_OVERVIEW §0.12.3b` (24 ข้อ) |
| "ตารางและชั้นข้อมูล" | `04_DB §4.2 · §4.6` |
| "จะทดสอบอะไรก่อน" | `06_TESTS §6.1` (invariant) |
| "อะไรที่ห้ามเปลี่ยน" | `07_LOCKED §7.0` |
| "อะไรที่ยังไม่มีคำตอบ" | `07_LOCKED §7.3` (30 ข้อ) |

---

## 🔗 Cross-Reference Tables

### FN → ที่อยู่ในแพ็ก
ตารางเต็ม **88 แถว** อยู่ที่ `00_OVERVIEW §0.12.1` — ทุก FN มี Story · ที่อยู่ · เคสทดสอบ

### BR → rule → test
`00_OVERVIEW §0.12.2` (32 แถว) · นิยามเต็มที่ `05_RULES §5.1`

### API → Function/Engine → ตาราง
`03_LOGIC §3.3` (28 แถว · R8 anchor)

### Declaration → trigger ใน FRD
`00_OVERVIEW §0.16.1` (NTF 9) · `§0.16.2` (CSQ 7) · `§0.16.5` (DOA 3 action + 1 non-action)

### Scope Lock → พิสูจน์ที่ → ทดสอบที่
`07_LOCKED §7.0` (11 แถว)

---

## 🚨 R8 Verification Matrix (mutation API → Function/Engine)

| # | ตรวจ | ผล |
|---|---|---|
| 1 | ทุก mutation API มี ≥1 Function/Engine | ✅ **21/21** |
| 2 | ทุก Function ใน `§3.1` ถูก trace ≥1 API | ✅ **48/48** |
| 3 | ทุก Engine ใน `§3.2` ถูกใช้จริง | ✅ **7/7** |
| 4 | ไม่มี orphan Function/Engine | ✅ |
| 5 | ไม่มี "createX/updateX" แอบอยู่ใน `02_API` | ✅ — `02_API` มีแต่ contract · logic อยู่ที่ `03_LOGIC` ทั้งหมด |
| 6 | Engine ไม่อ้าง HTTP | ✅ — ทั้ง 7 ตัวรับ/คืน object ล้วน |

---

# 🔍 Phase 3.5 Verification Report — FRD F-HR-ONBOARD

## A. Pack Completeness
- [x] Variant decision (FULL) สอดคล้องกับความซับซ้อน (2 state machine · สายอนุมัติจริง · read model · ทะเบียนหลักฐาน) ✅
- [x] ไฟล์ครบตาม variant — **9/9** ✅ · **`PRINT_SPEC.md` ไม่อยู่ในรายการโดยเจตนา** (ไม่มีท่อ pdfdoc) ✅
- [x] `03_LOGIC.md` มีอยู่ (บังคับทุก variant) ✅
- [x] `INDEX.md` อ้างอิงครบทุกไฟล์ ✅

## B. Function/API Coverage
- [x] mutation API ทั้ง 21 ตัวมี contract ครบ (request · response · error) ✅
- [x] read API 7 ตัวมี contract ครบ ✅

## C. R8 Logic Traceability ⭐
- [x] ทุก mutation API มี ≥1 Function/Engine ✅ 21/21
- [x] ทุก Function ถูก trace ≥1 API ✅ 48/48
- [x] ทุก Engine ถูก trace ✅ 7/7
- [x] ไม่มี orphan ✅

## D. API ↔ DB Linkage
- [x] ทุก API ระบุตารางที่แตะ และทุกตารางมีอยู่ใน `04_DB` ✅ (6 ตาราง + 1 view)

## E. UI ↔ API Cross-reference
- [x] ทุก action ในหน้าจอชี้ไปที่ API ที่มีอยู่จริง ✅
- [x] **ปุ่มที่ "ไม่มี" (ปิดรายการสิทธิ์ · เลื่อนเวลาเพิกถอน · ลบถาวร) ไม่มี API รองรับเช่นกัน** ✅

## F. Engine Iron Rules (CUBIC 3-layer)
- [x] ไม่มี Engine อ้าง HTTP ✅
- [x] input/output เป็น object ล้วน ✅
- [x] feature ไม่ข้าม API ไปเรียก Engine ตรง ✅

## G. Logic Placement Compliance
- [x] ไม่มี `createX/updateX` แอบใน `02_API` ✅
- [x] ไม่มีการคำนวณบริสุทธิ์แอบใน `02_API` ✅ (`severityOf` · `computeDueDate` อยู่ใน Engine)
- [x] logic ทุกตัวอยู่ใน `03_LOGIC` ✅

## H. Security Bible Application
- [x] trigger ที่ระบุได้: **PII · access lifecycle · approval workflow · cross-module read model** → ใช้ P6 + ยืม P7 ✅
- [x] Control 18 ข้อมี Control Point คู่ใน `05_RULES §5.7.2` ✅

## I. Convention Compliance
- [x] API path `/api/v1/onboard/...` ✅
- [x] `field_key` = snake_case ✅
- [x] Function code = camelCase ✅
- [x] Engine code = kebab-case ✅
- [x] Error code = UPPER_SNAKE ✅

## J. Data Classification (R10)
- [x] ทุกคอลัมน์ใน `04_DB §4.2` มี Classification ✅
- [x] ทุกคอลัมน์มี PII flag ✅
- [x] `§4.5` Field Dictionary มีคอลัมน์ Classification ✅
- [x] `§4.6` ครบ 6 หัวข้อ (.1–.6) ✅
- [x] `00_OVERVIEW §0.7.1` ระบุระดับสูงสุด = **Confidential** ✅
- [x] `05_RULES §5.7.1` มี D-CLASS ✅
- [x] **ไม่มีคอลัมน์ Public** ✅
- [x] **ไม่มีคอลัมน์ Restricted** → ไม่ต้อง wire Restricted Resources ✅

## K. Coverage Manifest (R13) ⭐
- [x] ทุก Story ใน BRD §7 มีแถวใน `§0.12.1` ✅ **88/88**
- [x] ทุก Rule ใน BRD §9 มีแถว ✅ **32/32**
- [x] ทุก Edge (☑) มีแถว ✅ **18/18** (+ ☐ 27 ข้อ)
- [x] **Functions Cut ครบใน `§0.12.3b`** ✅ **24/24**
- [x] **ไม่มีแถวที่ "อยู่ที่" ว่าง** ✅

## L. Scope Lock + Value Stream (R11/R12) ⭐
- [x] Scope Lock imported ครบ **11/11** → `07_LOCKED §7.0` ✅
- [x] **ไม่มี spec ใดในแพ็กขัด LOCK** ✅
- [x] `02_API §2.3` มี Cross-Module Contract ครบตาม BRD §12.1 downstream ✅ (7 คู่)
- [x] `06_TESTS §6.6` มี cross-module case ≥1 ต่อ downstream ที่มีข้อมูลไหล ✅ **XT-01…XT-07**

## M. HTML Alignment (v6.1) ⭐
- [x] **จำนวนหน้าใน `01_UI` = จำนวนหน้าใน HTML เป๊ะ** — 5 route ✅ ไม่มีหน้าที่แต่งขึ้น ไม่มีหน้าที่หาย
- [x] ทุก route ใน `01_UI` มีจริงใน HTML — `#/onboard/on` · `/off` · `/watch` · `/templates` · `/downstream` ✅
- [x] Pattern (observed) ตรงกับที่จอใช้จริง (spot-check 5 หน้า) ✅ — list-view · stat · definition list · drawer 920 · modal 440
- [x] `06_TESTS §6.7` microcopy ตรง verbatim (spot-check 21 ข้อความ) ✅
- [x] แท็บในลิ้นชักตรงกับ HTML — `ภาพรวม · งานในชุด · สิทธิ์และบัญชี · ทรัพย์สิน · ประวัติ` ✅
- [x] modal 14 ตัวตรงกับ HTML ✅
- [x] **ป้าย `กำลังเพิกถอน` ที่พบใน HTML ถูกบันทึกเป็นสถานะเชิงการแสดงผลที่ `05_RULES §5.2.3` และ `01_UI §1.3`** ✅ (ไม่ปล่อยผ่านเงียบ)

## Declaration Conformance (Lane Mode v2)
- [x] **NTF 9 = 9** ✅ · ไม่มี `doa_pending`/`doa_result`/`doa_escalate` ✅ · ไม่มี `sow.*` ✅
- [x] **CSQ 7 = 7 · SecC ท่อเดียว** ✅ · ไม่มี `oc`/`dc`/`sc` ✅
- [x] **NTF ∩ CSQ = ∅** (ชุด event ไม่ทับกัน — คนละท่อ คนละวัตถุประสงค์) ✅
- [x] DOA 3 action + **1 จุดที่จงใจไม่มี action (T-11)** ✅

## Verdict

> ✅ **Phase 3.5 A–M ผ่านครบ — ส่งต่อ S6 (`ai-testcase-md-generator`) ได้**
> **ประเด็นที่ยังต้องเคาะและถูกยกไว้ที่ `07_LOCKED §7.3`:** **OQ-01 สัญญาผลตอบกลับจาก Roles & Permissions (บล็อกแกนหลัก)** และ **OQ-02 `employment_term.*` ที่ HR Configuration (ครั้งที่ 4 ของอาการเดียวกันในโมดูลนี้)**
