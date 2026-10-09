# INDEX — FRD Pack · F-HR-ROSTER · Shift & Roster (จัดกะ)

**Variant: FULL (8 ไฟล์ + INDEX)** · สร้างโดย `frd-generator-v6` **Lane Mode v2** · 2026-08-29
**Phase 3.5: ✅ PASSED (A–M)** — รายงานเต็มอยู่ท้ายไฟล์นี้
⚠️ **แพ็กนี้ไม่มี `PRINT_SPEC.md` โดยเจตนา** — feature ไม่มีท่อ `pdfdoc` (ตารางกะไม่ใช่เอกสารที่คนถือ) · ดู `00_OVERVIEW §0.16.6` · `07_LOCKED §7.2 CD-01`

## 📂 Pack Contents

| ไฟล์ | Audience | เนื้อหาหลัก |
|---|---|---|
| `00_OVERVIEW.md` | ทุกคน | Document control · Scope · Roles · Dependencies · **§0.12 Coverage Manifest (73 FN)** · **§0.13 Published Roster Surface** · §0.14 Data Contract · §0.15 Soft Reference · **§0.16 Declaration Conformance** |
| `01_UI.md` | FE | **§1.0 Layout Decision Log (16 ข้อ)** · Page Inventory **5 หน้า** · รายละเอียดต่อหน้า · COSO touchpoints · empty state · microcopy |
| `02_API.md` | BE (HTTP) | 22 endpoint · **§2.3 Cross-Module Contract (Published Roster Surface)** · **§2.4 API → Logic Trace** · error response |
| **`03_LOGIC.md`** | BE (ตรรกะ) | **§3.0 กลไกของตัวตรวจข้อขัดแย้ง (หัวใจของแพ็ก)** · 60 Function · **10 Engine (ใหม่ 3)** · Trace Table · **§3.4 ลำดับที่ผิดแล้วพัง** |
| `04_DB.md` | DBA / BE | 5 ตาราง · classification ครบทุกคอลัมน์ · ER · index · migration · retention |
| `05_RULES.md` | BE + QA | BR-01…BR-33 · State machine (T-1…T-6 · W-1…W-6) · Permission · VR-01…VR-26 · Edge Case 57 · **Error catalog 27 code** · Security · Compliance |
| `06_TESTS.md` | QA | **AT-01…AT-97** · **IA-01…IA-10 (invariant · ตกข้อใดข้อหนึ่ง = หยุด release)** · test data 14 ชุด · DoD · **XT-01…XT-07** · **microcopy verbatim** |
| `07_LOCKED_DECISIONS.md` | ทุกคน | **§7.0 Scope Lock 14 ข้อ (IMMUTABLE)** · **LD-ROS-01…12** · Convention deviation · **OQ 30 ข้อ** · tradeoff |
| `INDEX.md` | ทุกคน | ไฟล์นี้ |
| `UI_BRIEF_จัดกะ.md` | FE + BA | (สร้างที่ S7) สรุปหน้าจอ + **Drift Log** |
| ~~`PRINT_SPEC.md`~~ | — | **ไม่มี — feature ไม่มีท่อ pdfdoc** |

## 🔍 Quick Nav by Question

| คำถาม | ไปที่ |
|---|---|
| **Attendance จะได้กะจากที่นี่อย่างไร ต้องทำอะไรบ้าง** | **`00_OVERVIEW §0.13.2` + `§0.13.4` + `§0.13.8`** |
| **ทำไม "สองกะในวันเดียว" ถึงไม่ใช่ข้อขัดแย้ง** | **`03_LOGIC §3.0.2`** · `07_LOCKED LD-ROS-03` |
| **กะข้ามคืนถูกจับได้อย่างไรทั้งที่อยู่คนละคอลัมน์** | **`03_LOGIC §3.0.1`** |
| **ทำไมกฎพัก/เพดาน/วันติดกันไม่ทำงาน** | **`03_LOGIC §3.0.4`** · `07_LOCKED OQ-STD-R6` · `06_TESTS IA-06` |
| **เผยแพร่ซ้ำแล้ววันที่ยืนยันไปแล้วจะเกิดอะไร** | **`03_LOGIC §3.0.5`** · `00_OVERVIEW §0.13.6` · `06_TESTS IA-04` |
| **ทำไมการสลับกะถึงหลุดกฎไม่ได้** | **`03_LOGIC §3.0.6`** · `06_TESTS IA-05` |
| **ทำไมไม่มีสายอนุมัติ** | **`00_OVERVIEW §0.16.4`** · `BRD §4.3` · `06_TESTS IA-08` |
| **ทำไมไม่มี `PRINT_SPEC.md`** | **`00_OVERVIEW §0.16.6`** · `07_LOCKED §7.2 CD-01` |
| หน้าจอมีกี่หน้า route อะไร | `01_UI §1.1` |
| endpoint ไหนเรียก function อะไร | `02_API §2.4` · `03_LOGIC §3.3` |
| คอลัมน์ไหนเป็นข้อมูลอ่อนไหว | `04_DB §4.6` |
| error code มีอะไรบ้าง | `05_RULES §5.6` |
| ทดสอบอะไรบ้างก่อน release | `06_TESTS §6.4` |
| อะไรที่ห้ามเปลี่ยน | `07_LOCKED §7.0` |
| ทำไมไม่มีตัวเลขเงินเลย | `05_RULES BR-27` · `06_TESTS IA-09` |
| ลำดับการเรียก function ที่ผิดแล้วพัง | **`03_LOGIC §3.4`** |

## 🔗 Cross-Reference Tables

### FN → ไฟล์
ตารางเต็ม **73 แถว** อยู่ที่ **`00_OVERVIEW §0.12.0`**

### BR → ไฟล์
ตารางเต็ม **33 แถว** อยู่ที่ **`00_OVERVIEW §0.12.2`** · ข้อความเต็มที่ `05_RULES §5.1`

### State → Transition → Event

| สถานะ | เข้าโดย | ออกโดย | event ที่ยิง |
|---|---|---|---|
| `draft` | T-1 | T-3 · T-6 | — (**ร่างไม่ยิง event ใดเลย**) |
| **`published`** | T-3 · T-4 | T-4 · T-5 | **`roster_published` (N1)** · **`roster.published` (EC estimated · E1)** |
| `superseded` | T-4 | — (ปลายทางถาวร) | **`roster_shift_changed` (N2)** · **`roster.republished` (EC estimated · E2 + `adjust_kind`)** |
| `locked` | T-5 | (ต้นทางเปิดงวดกลับ) | — (**ต้นทางเป็นผู้ประกาศ `hrconfig.period_closed`**) |
| `discarded` | T-6 | — (ปลายทางถาวร) | — |
| `requested` | W-1 | W-2 · W-4 · W-5 · W-6 | `roster_swap_requested` (N3) |
| `accepted` | W-2 | W-3 · W-4 · W-5 · W-6 | `roster_swap_accepted` (N4) |
| `confirmed` | W-3 | — | `roster_swap_decided` (N5) · **+ เกิด T-4 → E2 (`shift_swap`)** |
| `rejected` | W-4 | — | `roster_swap_decided` (N5) |
| `cancelled` | W-5 | — | — |
| `expired` | W-6 | — | `roster_swap_expired` (N6) |

### Engine → ผู้ใช้

| Engine | สถานะ | เรียกจาก |
|---|---|---|
| **`roster-conflict-engine`** ⭐ NEW | **candidate** | `F-14` `F-15` `F-16` `F-17` `F-18` `F-53` · **และ `F-36` (การสลับกะ) — ตัวเดียวกัน** |
| **`roster-publish-planner-engine`** ⭐ NEW | **candidate** | `F-24` |
| **`roster-version-chain-engine`** ⭐ NEW | **candidate** | `F-25` `F-28` `F-31` |
| `hr-config-resolve-client` | existing | `F-02` `F-06` `F-08` `F-20` |
| `attendance-resolve-client` | existing | `F-12` `F-24` |
| `leave-resolve-client` | existing | `F-19` |
| `ot-resolve-client` | existing | `F-21` |
| `notification-engine` (ENG-NOTIFY) | existing | `F-58` |
| `impact-valuation-engine` (ENG-CSQ) | existing | `F-59` |
| `role-scope-engine` (ENG-ROLESCOPE-01) | existing | `F-07` `F-41` `F-48` |

## 🚨 R8 Verification Matrix (mutation API → Function/Engine)

| API | Function/Engine | ✓ |
|---|---|:---:|
| API-01 · API-03 · API-04 · API-05 · API-06 · API-07 · API-08 · API-09 · API-11 · API-12 · API-13 · API-14 · API-15 · API-17 · API-20 · API-21 | ดู `03_LOGIC §3.3` (ครบทุกแถว) | ✅ |

**mutation API 16 ตัว · ทุกตัวมี trace · ไม่มี orphan Function/Engine · ไม่มี business logic ในชั้น API**

---

# 🔍 Phase 3.5 Verification Report — FRD F-HR-ROSTER

### A. Pack Completeness
- [x] Variant decision match Brief — **FULL** ✅
- [x] All expected files generated — **8 ไฟล์ + INDEX** ✅ · **`PRINT_SPEC.md` ไม่มีโดยเจตนา (ไม่มีท่อ pdfdoc) — ระบุไว้ชัดที่หัว `00_OVERVIEW` · `§0.10` · `§0.16.6` · `07_LOCKED CD-01` · และไฟล์นี้** ✅
- [x] `03_LOGIC.md` exists (mandatory ทุก variant) ✅
- [x] `INDEX.md` cross-references ครบทุกไฟล์ ✅

### B. Function/API Coverage
- [x] API 22 ตัว (mutation 16 · read 6) — **ทุกตัวมี contract** ✅
- [x] Function 60 ตัว — ทุกตัวมี input/output/สาระ/trace ✅

### C. R8 Logic Traceability ⭐
- [x] ทุก mutation API มี ≥1 Function/Engine ใน trace (`03_LOGIC §3.3`) ✅
- [x] ทุก Function ใน §3.1 ถูก trace อย่างน้อย 1 API (F-15…F-18 · F-53 · F-54 ผ่าน `F-14`/`F-36`) ✅
- [x] Engine ทั้ง 10 ตัวถูก trace ผ่าน Function ✅
- [x] **ไม่มี orphan Function/Engine** ✅

### D. API ↔ DB Linkage
- [x] API-01/03/04 → `T_roster_version` · `T_roster_cell` ✅
- [x] API-05/06/07/08 → `T_roster_version` ✅
- [x] API-09 → `T_roster_ack` ✅
- [x] API-11…14 → `T_roster_swap_request` ✅
- [x] API-18/19 → **view `v_roster_published_day` / `v_roster_period_summary`** ✅
- [x] ทุก mutation เขียน `T_roster_history` ผ่าน `F-49` ✅

### E. UI ↔ API Cross-reference
- [x] P-01 "กางตาราง" → `API-01` ✅ · P-01 drawer ช่อง → `API-03` ✅ · P-01 ทาช่วง → `API-04` ✅
- [x] P-02 "เผยแพร่" → `API-06` ✅ · "เผยแพร่ซ้ำ" → `API-07` ✅ · "ทิ้งร่าง" → `API-08` ✅
- [x] P-03 ยื่น/ตอบรับ/ปฏิเสธ/ยืนยัน/ถอน → `API-11`…`API-14` ✅
- [x] P-04 timeline → `API-22` ✅ · P-05 สวิตช์ → `API-20` · ตาราง read model → `API-18` ✅

### F. Engine Iron Rules (CUBIC 3-layer)
- [x] **ไม่มี Engine ใดอ้างถึง `req`/`res`/header/status code** ✅
- [x] Engine input/output = **pure object** ทั้งหมด ✅
- [x] **Feature ไม่ข้าม API ไปเรียก Engine ตรง** ✅

### G. Logic Placement Compliance ⭐
- [x] **ไม่มี `createX/updateX` แอบใน `02_API`** — ชั้น API เป็นเปลือก HTTP ล้วน ✅
- [x] **ไม่มี pure calculation แอบใน `02_API`** — การคำนวณทั้งหมดอยู่ใน `03_LOGIC §3.2` ✅
- [x] logic ที่ matrix #3–8 อยู่ใน `03_LOGIC` จริง ✅

### H. Security Bible Application
- [x] Trigger ที่ระบุ: HR/PII · read model เปิดให้ consumer · audit ที่แก้ไม่ได้
- [x] Domain ที่ apply: **P6 (15 controls) + ยืม P7 (3 controls)** — `05_RULES §5.7` ✅
- [x] Must 11 ข้ออยู่ใน Phase 1 ครบ ✅

### I. Convention Compliance
- [x] API path `/api/v1/roster/...` ✅
- [x] field_key = `snake_case` ✅
- [x] Function code = `camelCase` ✅
- [x] Engine code = `kebab-case` ✅
- [x] Error code = `UPPER_SNAKE` ✅

### J. Data Classification (R10) ⭐
- [x] ทุกคอลัมน์ใน `04_DB §4.2` มี `Classification` ✅
- [x] ทุกคอลัมน์มี `PII` flag ✅
- [x] `04_DB §4.5` Field Dictionary มี Classification ✅
- [x] `04_DB §4.6` ครบ 6 subsections (.1–.6) ✅
- [x] `00_OVERVIEW §0.7.1` ระบุชั้นสูงสุด = **Confidential** ✅
- [x] `05_RULES §5.7.B` มี subsection D-CLASS ✅
- [x] **ไม่มี default = Public** — ตรวจแล้ว **0 คอลัมน์เป็น Public** ✅
- [x] **ไม่มี Restricted fields** — จึงไม่ต้อง wire Restricted Resources ✅

### K. Coverage Manifest (R13) ⭐
- [x] ทุก Story ใน `BRD §7` (**73**) มีแถวใน `§0.12` ✅ (1:1 กับ FN)
- [x] ทุก Rule ใน `BRD §9.1` (**33**) มีแถวชี้ `05_RULES` + test ✅
- [x] ทุก Edge ☑ ใน `BRD §10.1` (**26**) มีแถว ✅ · ☐ AI-suggested (**31**) มีแถว ✅
- [x] **ไม่มีแถวที่ "อยู่ที่" ว่าง** ✅
- [x] **Functions Cut 19/19 อยู่ในแมนิเฟสต์** (`§0.12.3b`) ✅

### L. Scope Lock + Value Stream (R11/R12) ⭐
- [x] Scope Lock imported ครบ **14 ข้อ** ตาม `BRD §3.4` → `07_LOCKED §7.0` ✅
- [x] **ไม่มี spec ใดในแพ็กขัด LOCK** ✅
- [x] `02_API §2.3` มี Cross-Module Contract ครบตาม `BRD §12.1` downstream (Attendance · OT · ESS · 7C) ✅
- [x] `06_TESTS §6.6` มี cross-module case **7 เคส** — ครอบทุก downstream ที่มีข้อมูลไหล ✅

### M. HTML Alignment (v6.1) ⭐
- [x] จำนวนหน้าใน `01_UI` = **5** = จำนวนหน้าใน HTML = **5** — **ไม่มี invented/missing page** ✅
- [x] ทุก route ใน `01_UI` มีจริงใน HTML (`#/roster/grid` · `/publish` · `/swap` · `/history` · `/downstream`) ✅
- [x] Pattern (observed) ตรงกับที่จอใช้จริง — spot-check 3 หน้า: **P-01 = P (day-planner: `.pool-card[draggable]` + กริดคน×วัน + `.cal`)** · **P-03 = A+C (list + drawer 3 tab)** · **P-05 = A+K (ตาราง read model + ตารางขอบเขต 19 แถว)** ✅
- [x] `06_TESTS` expected text ตรง verbatim — spot-check 5 ข้อความ: **"ยังไม่มีค่าให้อ่าน"** · **"จัดการที่ ตั้งค่า HR"** · **"คืนค่าว่าง"** · **"ยืนยันไม่ได้ — ผลตรวจมีระดับห้าม"** · **"อ่านว่าเป็นวันหยุดของคนนั้น"** ✅
- [x] DIVERGENCE ที่ตั้งใจของ Pattern P **3 ข้อ** บันทึกไว้ที่ `01_UI §1.4` และจะถูกยกไป Drift Log ที่ S7 ✅

### Verdict
**✅ All checks passed (A–M) → deliver Pack**

**หมายเหตุที่ต้องส่งต่อ (ไม่บล็อก แต่ห้ามหาย):**
1. **`OQ-STD-R6` + `OQ-R15`** — คีย์ `shift_rule.*` ที่ HR Configuration ยังไม่เผยแพร่ ทำให้ **4 กฎจาก 33 ไม่ถูกบังคับใช้เลยในรอบนี้** · **เป็นคีย์ที่หายไปตัวที่สามของคลาสเดียวกันในโมดูล HR** ต่อจาก `OQ-STD-11` (Salary Structure) และ `OQ-STD-OT5` (OT) → **ควรเคาะรวมเป็นการเปลี่ยนแปลงเดียวของ HR Configuration ไม่ใช่สามใบงานแยก**
2. **Engine candidate 3 ตัว** — `roster-conflict-engine` · `roster-publish-planner-engine` · `roster-version-chain-engine` → เสนอ Architect ลง CUBIC · **ตัวแรกสำคัญที่สุด เพราะการแก้ด้วยมือกับการสลับกะต้องเรียกตัวเดียวกัน (`C-17`)**
3. **`CSQ_BRIEF §5` ให้ติ๊ก G4 + G5** — trigger อ้าง `03_LOGIC` จริงแล้ว และทุก payload field ยืนยันแล้วว่ามีจริงใน `04_DB` (หลักฐานที่ `00_OVERVIEW §0.16.2`) · **append ในใบเดิม ห้ามออกใบใหม่**
4. **`OQ-R19`** (หัวหน้าสูงสุดของสายยื่นคำขอสลับแล้วไม่มีใครยืนยันได้) — พบใหม่ตอนตรวจ SoD ที่ S4 · ต้องเคาะก่อน dev เริ่ม `#/roster/swap`
