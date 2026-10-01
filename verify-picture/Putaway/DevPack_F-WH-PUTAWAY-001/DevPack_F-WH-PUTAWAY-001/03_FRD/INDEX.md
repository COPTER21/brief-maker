# INDEX — FRD Pack · F-WH-PUTAWAY · จัดเก็บเข้าที่ (F081)

> Variant **FULL** (00…07 + INDEX) · Mode B (HTML-first) · เลน WF-01 Phase B · 2026-09-14
> registry F081: `arch = master` · **`dec = csq`** · `wave = W3Q` · `auto = lite`

---

## ไฟล์ในแพ็ก

| ไฟล์ | เนื้อหา | อ่านเมื่อ |
|---|---|---|
| **`00_OVERVIEW.md`** | scope · roles · dependencies · data classification · ใบประกาศตามชิป · **Coverage Manifest + ตาราง map รหัสที่ชนกัน (§0.12.5)** · OQ ทั้งหมด | **อ่านก่อนทุกไฟล์** |
| `01_UI.md` | Layout Decision Log · routing · anatomy รายมุมมอง · component states · Esc chain · responsive · **microcopy verbatim (§1.11)** | ทำหน้าจอ |
| `02_API.md` | 16 endpoint · cross-module contract · authorization matrix · concurrency · **error catalog 20 รหัส** | ทำ backend |
| `03_LOGIC.md` | 25 ฟังก์ชันชั้นโค้ด · **2 engine (`ENG-PUT-SUGGEST` · `ENG-INV-MOVE`)** · Logic Placement Matrix · R8 trace | ทำ backend |
| **`04_DB.md`** | 6 ตาราง/view · indexes · data classification · ★ **§4.7 สัญญากลางของ location** | ทำ DB · **F082/F083 ต้องอ่าน §4.7** |
| `05_RULES.md` | R01–R25 · VR01–VR14 · Edge Cases · **§5.5 ผลกระทบ 7C (CSQ)** · สิ่งที่ไม่ทำโดยเจตนา | ทุกคน |
| `06_TESTS.md` | AT-01…AT-38 · PT-01…PT-14 · XT-01…XT-16 · scenario coverage 28/28 · **traceability set-check** | QA |
| **`07_LOCKED_DECISIONS.md`** | LOCK-01…08 · **L1–L10 (HANDOFF ห้ามแตะ)** · LD-01…LD-07 · convention deviations · **§7.4 สิ่งที่ยังไม่ล็อก** | **อ่านก่อนแก้อะไรก็ตาม** |
| `HTML_UI_BRIEF_F-WH-PUTAWAY-001.md` | สกัด UI จาก HTML 1:1 — design tokens · z-index map · overlay registry · selector anchors · Drift Log | FE/dev |

### ใบประกาศตามชิป — **1/1 ตาม `dec = csq`**

| ไฟล์ | ชิป | สถานะ |
|---|---|---|
| `CSQ_BRIEF_F-WH-PUTAWAY-001.md` | ◆ `csq` | ✅ **ออก** — 2 event (`putaway_forced_override` · `putaway_reversed`) |
| ~~`DOA_BRIEF`~~ | ⚖ `doa` | ❌ **ไม่ออกโดยเจตนา** — ไม่มีสายอนุมัติเลย (`07_LOCKED` LD-01) |
| ~~`NTF_BRIEF`~~ | 🔔 `ntf` | ❌ **ไม่ออกโดยเจตนา** — registry ไม่ติดชิป (LD-01) |
| ~~`DOCCFG_BRIEF`~~ | `doccfg` | ❌ **ไม่ออกโดยเจตนา** — ไม่ใช่เอกสาร ไม่มีเลขรัน (LD-02) |
| ~~`PRINT_SPEC`~~ | 📄 `pdfdoc` | ❌ **ไม่ออกโดยเจตนา** — ไม่มีใบพิมพ์ (LD-01) |

> **4 ใบที่ไม่ออก = เจตนา ไม่ใช่ตกหล่น** — เหตุผลรายใบอยู่ที่ `00_OVERVIEW` §0.10 และ `07_LOCKED` LD-01/LD-02
> `_COVERAGE_REPORT.md` §5 ยืนยันเชิงกล: detect = chip → **ไม่มี DIVERGENCE**

---

## Function Trace (R8) — 25 ฟังก์ชัน · 16 API · 2 engine

| Function | ชื่อ | เรียกจาก |
|---|---|---|
| FN-01 | `buildPutawayQueue` | API-01 |
| FN-02 | `computeTaskProgress` | API-01/02/08/14/16 |
| FN-03 | `deriveTaskStatus` | API-01/02/08/14 · event จาก GRN |
| FN-04 | `computeTaskAge` | API-01/02/15 |
| FN-05 | `claimTask` | API-03 |
| FN-06 | `releaseTask` | API-04 |
| FN-07 | `forceReleaseTask` | API-05 |
| **FN-08** | `expireHeldTasks` | **scheduler ⚠️ ยังไม่ implement (LD-05)** |
| FN-09 | `suggestBins` | API-06 → `ENG-PUT-SUGGEST` |
| FN-10 | `filterEligibleBins` | API-06 (F-1…F-5) |
| FN-11 | `rankBins` | API-06 (R1…R4 + tie-break) |
| FN-12 | `searchBinsForOverride` | API-07 |
| FN-13 | `classifyViolation` | API-08 |
| FN-14 | `validateDestinations` | API-08 |
| FN-15 | `confirmPutaway` | API-08 |
| FN-16 | `appendMovement` | API-08/14 → `ENG-INV-MOVE` |
| FN-17 | `recomputeBinStock` | API-08/09/10/14 |
| FN-18 | `reversePutaway` | API-14 |
| FN-19 / FN-20 | `lockBin` / `unlockBin` | API-11 / API-12 |
| FN-21 | `withdrawTasksOnGrnReversal` | event จาก GRN |
| FN-22 | `guardGrnReversal` | API-16 |
| FN-23 | `computeKpi` | API-15 |
| FN-24 | `pushAudit` | API-03/04/05/08/11/12/14 |
| FN-25 | `emitCsqEvents` | API-08/14 → ENG-CSQ |

| Engine | ระดับ | ใครใช้ต่อ |
|---|---|---|
| `ENG-PUT-SUGGEST` | scope-local | Putaway เท่านั้น |
| **`ENG-INV-MOVE`** | **module-level** | ★ **Putaway + F-WH-STKADJ + F-WH-STKTRF ต้องใช้ตัวเดียวกัน** (LOCK-08) |

**R8 verification:** function orphan = 0 · API ที่ไม่มี logic = 0 · engine ทุกตัวมี iron rule กำกับ · **ฟังก์ชันที่ยังไม่ implement = 1 (FN-08)**

---

## Quick Nav — "ฉันอยากรู้เรื่องนี้ ไปอ่านที่ไหน"

| คำถาม | ไปที่ |
|---|---|
| ทำไมไม่มีปุ่มพิมพ์ / เลขที่เอกสาร / สายอนุมัติ | `07_LOCKED` §7.1 **L1/L2/L3** · `05_RULES` R01 |
| **ฉันทำ F-WH-STKADJ / F-WH-STKTRF ต้องหยิบอะไรไปใช้** | ★ **`04_DB` §4.7 ทั้งหัวข้อ** + checklist **§4.7.4** |
| เกณฑ์แนะนำช่องเก็บทำงานยังไง | `03_LOGIC` FN-10/FN-11 + `ENG-PUT-SUGGEST` · `02_API` §2.4 |
| ทำไมยืนยันไม่ได้ / ข้อความบล็อกมีอะไรบ้าง | `01_UI` §1.11 · `05_RULES` §5.2 |
| ของกักกันทำอะไรได้บ้าง | `05_RULES` R04 · `04_DB` §4.7.2 · `06_TESTS` AT-13 |
| ทำไมยอดคงเหลือแก้มือไม่ได้ | `04_DB` §4.2 `v_bin_stock` · DR-06 · `05_RULES` §5.4 |
| กลับรายการทำงานยังไง | `03_LOGIC` FN-18 · `02_API` §2.7 · `06_TESTS` AT-21/22 |
| **ทำไม R18 (soft lock) ยังไม่ครบ** | ★ `05_RULES` **§5.1.1** · `07_LOCKED` **LD-05** · `06_TESTS` AT-15 |
| **ทำไม PREBRIEF กับ CSQ_BRIEF พูดไม่ตรงกัน** | ★ `07_LOCKED` **LD-04** · `05_RULES` §5.5.3 |
| **HTML ถูกแก้ตรงไหนบ้าง** | ★ `07_LOCKED` **LD-03** · `01_HTML/_UX_CHECK_REPORT.md` §1.1 |
| `S-xx` / `FN-xx` หมายถึงชุดไหน | ★ `00_OVERVIEW` **§0.12.5** |
| อะไรยังไม่ตัดสิน ห้าม implement | `07_LOCKED` **§7.4** · `05_RULES` §5.3.3 · `00_OVERVIEW` §0.13 |
| ต้องถอดอะไรก่อนขึ้น production | `07_LOCKED` **LD-06** |
| สิทธิ์ใครทำอะไรได้ | `02_API` §2.9 · `06_TESTS` §6.2 |

---

## Chain ถัดไป

| ขั้น | ผลลัพธ์ | สถานะ |
|---|---|---|
| 7R re-gate | `01_HTML/_UX_CHECK_REPORT.md` + `_COVERAGE_REPORT.md` (รอบ 1) + 20 ช็อต | ✅ **PASS** (BLOCK 0 หลังแก้ 2 บรรทัด) |
| 9 · FRD | แพ็กนี้ | ✅ |
| 9D · ใบประกาศ | `CSQ_BRIEF_F-WH-PUTAWAY-001.md` (1/1 ตามชิป) | ✅ |
| 10 · HTML UI Brief | `HTML_UI_BRIEF_F-WH-PUTAWAY-001.md` | ✅ |
| 11 · TC for AI | `04_QA/testcases-F-WH-PUTAWAY-001.md` | ✅ |
| 12 · TC for Tester | `04_QA/testcase-F-WH-PUTAWAY-001.html` + `_build/` | ✅ |
| 12T · Feature TL;DR | `FEATURE_TLDR_F-WH-PUTAWAY-001.html` (รากแพ็ก) | ✅ |
| 13 · coverage รอบ 2 | ต่อท้าย `01_HTML/_COVERAGE_REPORT.md` | ✅ |
| 14 · ส่งขึ้น OPS | — | ⏳ **ยังไม่ทำ — รอ go-ahead จากผู้ใช้** |
