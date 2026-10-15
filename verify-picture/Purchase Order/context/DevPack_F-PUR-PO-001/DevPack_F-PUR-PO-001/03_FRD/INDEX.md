# INDEX — FRD Pack F-PUR-PO · ใบสั่งซื้อ (F078)

**Variant:** FULL (9 files + INDEX) · **FRD v6.1** (HTML-first · Mode B)

---

## ไฟล์ในแพ็ก

| ไฟล์ | ใครอ่าน | เนื้อหา |
|---|---|---|
| [`00_OVERVIEW.md`](00_OVERVIEW.md) | ทุกคน | Document Control · Scope · Roles · Dependencies · **Coverage Manifest** · Open Questions |
| [`01_UI.md`](01_UI.md) | **FE dev** | Layout Decision Log · 8 หน้า/ส่วน · B2 line editor · microcopy verbatim · responsive |
| [`02_API.md`](02_API.md) | **BE dev (HTTP)** | 15 endpoint · authz matrix · **cross-module contract** · error catalog |
| [`03_LOGIC.md`](03_LOGIC.md) | **BE dev (logic)** | 26 Function · Engines · **API ↔ Logic trace table** |
| [`04_DB.md`](04_DB.md) | **DBA / BE dev** | 5 ตาราง · **Data Classification ทุกคอลัมน์** · index · ความสัมพันธ์ |
| [`05_RULES.md`](05_RULES.md) | **BE dev + QA** | R01–R24 · VR01–VR18 · E01–E11 + `[AI-DEFAULT]` · D-CLASS |
| [`06_TESTS.md`](06_TESTS.md) | **QA** | AT-01..30 · PT-01..05 · **XT-01..15 cross-module** · scenario coverage · DoD |
| [`07_LOCKED_DECISIONS.md`](07_LOCKED_DECISIONS.md) | **ทุกคน** | LOCK-01..07 · **L-01..L-09** · LD-01..12 · สิ่งที่ยังไม่ล็อก |
| [`HTML_UI_BRIEF_F-PUR-PO-001.md`](HTML_UI_BRIEF_F-PUR-PO-001.md) | **FE dev** | สกัด UI จาก HTML 1:1 — token · selector · anatomy · overlay |

### ใบประกาศตามชิป (5/5 — ครบ)

| ไฟล์ | ชิป | ใครเอาไปใช้ |
|---|---|---|
| [`DOA_BRIEF_F-PUR-PO-001.md`](DOA_BRIEF_F-PUR-PO-001.md) | ⚖ `doa` | คนตั้งค่าที่หน้า DOA กลาง |
| [`NTF_BRIEF_F-PUR-PO-001.md`](NTF_BRIEF_F-PUR-PO-001.md) | 🔔 `ntf` | คน wire ENG-NOTIFY |
| [`CSQ_BRIEF_F-PUR-PO-001.md`](CSQ_BRIEF_F-PUR-PO-001.md) | ◆ `csq` | deploy pipeline (auto-register) |
| [`DOCCFG_BRIEF_F-PUR-PO-001.md`](DOCCFG_BRIEF_F-PUR-PO-001.md) | `doccfg` | deploy pipeline (auto-register) |
| [`PRINT_SPEC_F-PUR-PO-001.md`](PRINT_SPEC_F-PUR-PO-001.md) | 📄 `pdfdoc` | dev ที่ bind data เข้า template |

---

## Function Trace (R8)

| Function | เรียกจาก API | Engines ที่ใช้ |
|---|---|---|
| FN-01 `createPurchaseOrder` | API-02 | ENG-PO-CALC |
| FN-02 `hydrateFromPurchaseRequest` | API-02 | — |
| FN-03 `hydrateFromCompareResult` | API-02 | — |
| FN-04 `checkSourceDocumentStatus` | API-02 · 04 · 05 | — |
| FN-05 `validatePoDraft` | API-02 · 04 · 05 | — |
| FN-06 `checkPrRemaining` ★ hard | API-05 | — |
| FN-07 `checkBudgetAvailability` ★ soft | API-05 · 15 | — |
| FN-08 `checkVendorStatus` | API-02 · 05 | — |
| FN-09 `findSimilarPurchaseOrders` | API-14 · 05 | — |
| FN-10 `resolveDoaChain` | API-05 · 15 | ENG-DOA |
| FN-11 `snapshotApprovalChain` | API-05 | — |
| FN-12 `approveStep` | API-06 | — |
| FN-13 `rejectApproval` | API-07 | ENG-NOTIFY |
| FN-14 `issueDocumentNumber` | API-06 | ENG-DOC-NUM |
| FN-15 `sendToVendor` | API-08 | ENG-DOC-STORE · ENG-NOTIFY |
| FN-16 `applyTransitionGuard` | API-04 | — |
| FN-17 `revertToDraft` | API-04 | — |
| FN-18 `cancelPurchaseOrder` | API-09 | ENG-CSQ · ENG-NOTIFY |
| FN-19 `shortClosePurchaseOrder` | API-10 | ENG-CSQ · ENG-NOTIFY |
| FN-20 `calcPoTotals` | API-02 · 04 · 05 | ENG-PO-CALC |
| FN-21 `computeLineReceiptStatus` | API-03 · 10 · callback | — |
| FN-22 `syncHeaderStatusFromLines` | callback ใบรับของ | — |
| FN-23 `buildReceiptContract` | `GET /receivable` | — |
| FN-24 `pushAudit` | ทุก mutation | — |
| FN-25 `calcOpenCommitment` | API-01 | — |
| FN-26 `emitPoEvents` | API-04 · 05 · 06 · 07 · 08 · 09 · 10 | ENG-CSQ · ENG-NOTIFY |

**ไม่มี orphan** — ทุก Function ถูกเรียก · ทุก mutation API มี Function ≥ 1

---

## Quick Nav — "ฉันอยากรู้เรื่องนี้ ไปอ่านที่ไหน"

| คำถาม | ไปที่ |
|---|---|
| หน้าจอมีอะไรบ้าง · ปุ่มชื่ออะไร | `01_UI §1.2`–`§1.6` · `§1.10` microcopy |
| ตารางกรอกรายการทำงานยังไง | `01_UI §1.4` (B2 v2) |
| สูตรคำนวณยอด | `03_LOGIC` ENG-PO-CALC · `05_RULES R23` |
| **อะไรบล็อก อะไรแค่เตือน** | `05_RULES §5.2` (VR12 vs VR13) · `07_LOCKED L-09` |
| สายอนุมัติมาจากไหน | `03_LOGIC FN-10` · `DOA_BRIEF` · **ไม่ได้อยู่ในโค้ด feature** |
| เลขเอกสารออกตอนไหน | `03_LOGIC FN-14` · `DOCCFG_BRIEF` · `05_RULES R22` |
| ใบรับของต้องได้อะไรจาก PO | `02_API §2.7.1` · `03_LOGIC FN-23` |
| ทำไมไม่มีการลงบัญชี | `07_LOCKED LOCK-07 · LD-07` |
| ทำไม tolerance ตั้งได้แต่ไม่บังคับ | `05_RULES §5.4` · `07_LOCKED LD-05` |
| อะไรยังไม่ตัดสิน | `00_OVERVIEW §0.13` · `07_LOCKED §7.4` |
| HTML ถูกแก้อะไรไปบ้าง | `07_LOCKED LD-03` · `01_HTML/_UX_CHECK_REPORT.md` |

---

## Chain ถัดไป

`04_QA/testcases-F-PUR-PO-001.md` (AI) → `04_QA/testcase-F-PUR-PO-001.html` (คน) → `FEATURE_TLDR_F-PUR-PO-001.html` → coverage รอบ 2 → pack → OPS
