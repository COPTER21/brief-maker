# 06_TESTS — F-PG GL Posting Group

> **Audience:** QA engineer
> **Coverage source:** `02_API.md` contracts + `03_LOGIC.md` functions/engine + `05_RULES.md` rules/edge cases
> **Expected text policy (§6.10):** every expected UI text below is taken **verbatim from `f-postgrp.html`** (Mode A — HTML is source of truth for exact strings), not invented.

---

## §6.1 Acceptance Criteria (AC)

### AC-01: Create Specific Posting Group — happy path
**Given** Finance Lead on tab "Posting Groups", drawer open, kind="vendor" selected
**When** all required fields filled (code, name_th, account_1 = a liability leaf/postable/active account) and "ยืนยันสร้าง" clicked
**Then** response 201, new row appears in list with `used=0`, toast **"สร้าง Posting Group แล้ว"**

### AC-02: Create — duplicate code
**Given** `code` already exists in registry
**When** submit
**Then** field `code` shows invalid state, toast **"รหัสกลุ่มนี้มีอยู่แล้ว"**, no record created

### AC-03: Create — account type mismatch
**Given** kind="vendor", `account_1` set to an `asset`-type account instead of required `liability`
**When** submit (server-side, since dropdown pre-filters client-side)
**Then** 422 `BR_ACCOUNT_TYPE_MISMATCH`

### AC-04: Create General Posting Setup — happy path
**Given** tab "General Posting Setup", drawer open, `bus_group`+`prod_group` combination not yet in registry, all 3 accounts filled with correctly-typed accounts
**When** "ยืนยันสร้าง" clicked
**Then** 201, toast **"สร้าง Posting Setup แล้ว"**

### AC-05: Create Setup — duplicate combination
**Given** combination already exists
**When** submit
**Then** both `bus_group` and `prod_group` fields show invalid, toast **"ชุดกลุ่มนี้มีอยู่แล้ว"**

### AC-06: Edit — `used=0`
**Given** a record with `used=0` open in edit drawer
**When** any field except `kind` is changed and "บันทึกการแก้ไข" clicked
**Then** 200, toast **"บันทึกการแก้ไขกลุ่มแล้ว"** (tab1) / **"บันทึกการแก้ไข setup แล้ว"** (tab2)

### AC-07: Edit — IR-PG-01 lock on `code` (tab1, `used>0`)
**Given** a record with `used>0` open in edit drawer
**When** the code field (rendered as a static locked box + `.lock-tag` "ล็อก — มีการบันทึกบัญชีแล้ว") is attempted to change and submit is clicked with a different code value
**Then** 422 `BR_CODE_LOCKED_USED`, toast **"กลุ่มนี้มีการบันทึกบัญชีผ่านแล้ว — เปลี่ยนรหัสไม่ได้ (แก้ชื่อ/บัญชี/สถานะได้)"**

### AC-08: Edit — IR-PG-01 lock on combination (tab2, `used>0`)
**Given** a setup record with `used>0`
**When** `bus_group` or `prod_group` is attempted to change and submit clicked
**Then** 422 `BR_COMBINATION_LOCKED_USED`, toast **"ชุดกลุ่มนี้มีการบันทึกบัญชีผ่านแล้ว — เปลี่ยนกลุ่มธุรกิจ/สินค้าไม่ได้ (แก้บัญชี/สถานะได้)"**

### AC-08b: Edit — R05 lock on `kind` (independent of `used`, even `used=0`)
**Given** any record, `used=0`, in edit drawer
**When** the kind field is inspected
**Then** it is rendered as a static disabled box (not a dropdown) — **kind can never be changed via UI in edit mode, regardless of `used`** — and server rejects any `kind` value in the PUT body that differs from current with `BR_KIND_LOCKED`
**This AC exists specifically to prove BR-03/R05 does not depend on `used`, unlike AC-07/AC-08.**

### AC-09: Status change — free, no approval
**Given** any record, any current status
**When** a different status is picked from the "เปลี่ยนสถานะ" menu or bulk bar
**Then** status changes immediately, no confirmation/approval step, toast **"เปลี่ยนสถานะเป็น [label] แล้ว"** (single) or **"เปลี่ยนสถานะ N รายการเป็น [label] แล้ว"** (bulk)

### AC-10: Bulk delete — skip used>0
**Given** N rows selected, M of which have `used>0`
**When** bulk-delete confirmed
**Then** only (N−M) rows deleted, toast **"ลบแล้ว [N−M] รายการ · ข้าม [M] (มีการบันทึกบัญชีผ่านแล้ว)"** (skip clause only shown if M>0)

### AC-11: Import — happy path (groups)
**Given** valid CSV file matching template columns, all rows valid
**When** file picked → preview shows all ✓ → "นำเข้า N แถว" clicked
**Then** N new rows created (`used=0`, DOA null×4), existing rows untouched, toast **"นำเข้าแล้ว N รายการ"**

### AC-12: Import — mixed valid/invalid rows
**Given** CSV with some rows failing REQUIRED/BAD_KIND/CODE_DUPLICATE/BAD_STATUS/account-not-in-COA
**When** preview renders
**Then** invalid rows show `✗ [first error]` (full list on hover), valid rows show `✓ พร้อมนำเข้า`; only valid rows import; toast on commit shows **"นำเข้าแล้ว N รายการ · ข้าม M แถว"**

### AC-13: Import — blank status defaults to draft (BR-07)
**Given** a valid row with blank `status` cell
**When** imported
**Then** new record's `status = 'draft'`

### AC-14: Import — no replace mode exists (LOCK-03)
**Given** the import modal at step "pick"
**When** inspecting available UI options
**Then** there is **no** mode selector of any kind — only an upload box and a template-download button. **This is a negative test: the absence of a Replace/Merge-overwrite option is itself the pass condition.**

### AC-15: Export — filtered CSV, roundtrip columns
**Given** a filter applied on the list (e.g. kind=vendor)
**When** "ส่งออก CSV" clicked
**Then** downloaded file contains only matching rows, columns match the import template exactly, `status` in Thai, file has UTF-8 BOM

### AC-16: COA resolver — OQ-PG-02 resolution
**Given** the real `ENG-PG-01 coa-account-resolver` wired to `GET /api/v1/coa/accounts` (replacing the mock)
**When** opening the account dropdown for `kind=vendor, account_1`
**Then** only accounts that are leaf+postable+active+type=liability appear — an inactive or non-leaf liability account must **not** appear

### AC-17: `kind` immutable — no UI path at all
**Given** edit mode, any `used` value
**When** attempting to find any control to change `kind`
**Then** none exists — the field renders as a static label, not an input/dropdown (see AC-08b)

### AC-18: Kind-change clears accounts (R07, create mode only)
**Given** create drawer, kind=vendor, `account_1` filled
**When** kind switched to inventory
**Then** all account fields reset to empty and the field set re-renders for inventory's 2 fields

---

## §6.2 Test Case Inventory

| TC ID | Name | Type | Maps to AC | Priority |
|---|---|---|---|---|
| TC-01 | Create group — happy | API | AC-01 | P0 |
| TC-02 | Create group — dup code | API negative | AC-02 | P0 |
| TC-03 | Create group — type mismatch | API negative | AC-03 | P0 |
| TC-04 | Create setup — happy | API | AC-04 | P0 |
| TC-05 | Create setup — dup combination | API negative | AC-05 | P0 |
| TC-06 | Edit used=0 | API | AC-06 | P0 |
| TC-07 | Edit — IR-PG-01 code lock | API negative | AC-07 | P0 |
| TC-08 | Edit — IR-PG-01 combination lock | API negative | AC-08 | P0 |
| TC-09 | Edit — kind always locked (used=0) | API negative | AC-08b | P0 |
| TC-10 | Edit — kind always locked (used>0) | API negative | AC-08b | P0 |
| TC-11 | Status change, any direction, no approval | API | AC-09 | P0 |
| TC-12 | Bulk delete, mixed used | API | AC-10 | P0 |
| TC-13 | Import happy | Integration | AC-11 | P0 |
| TC-14 | Import mixed valid/invalid | Integration | AC-12 | P0 |
| TC-15 | Import blank status→draft | Integration | AC-13 | P1 |
| TC-16 | Import — no replace mode UI | UI negative | AC-14 | P1 |
| TC-17 | Export roundtrip | Integration | AC-15 | P1 |
| TC-18 | COA resolver filter accuracy | Engine (ENG-PG-01) | AC-16 | P0 |
| TC-19 | Kind-change clears accounts | UI | AC-18 | P1 |
| TC-CA-01 | Concurrent edit — optimistic lock `[AI-DEFAULT]` | API stress | 05_RULES CA-01 | P2 |
| TC-CA-07 | Concurrent create — dup code race | API stress | 05_RULES CA-07 | P1 |
| TC-PM-03 | Non-Finance role direct API call | API negative | 05_RULES PM-03 | P1 |

---

## §6.3 Test Data Setup

### Required test data (mirrors as-built mock, `f-postgrp.html`)
- Tab 1 seed: 7 groups across all 4 kinds, mixed status (5 active, 1 draft, 1 inactive), one bank kind with `used=203` (highest — good for CA/ST edge tests)
- Tab 2 seed: 3 setups (2 active with `used>0`, 1 draft with `used=0` — `FOREIGN×GOODS`)
- COA mock: 16 accounts across asset/liability/income/expense types (per `f-postgrp.html` `COA_ACCOUNTS`) — until ENG-PG-01 is wired to real F-COA-001

### Roles for testing
- `qa_finance_lead` (Finance Lead — full access)
- `qa_auditor` (Auditor/Watcher — view+export only)
- `qa_no_role` (for PM-03 negative test — direct API call without Finance role)

---

## §6.4 Definition of Done (DoD)

### Code
- [ ] AC-01..18 implemented + unit tests pass
- [ ] IR-PG-01 (BR-05) and R05 (BR-03) implemented and tested as **two separate guards** — TC-07/08 vs TC-09/10 must be distinguishable in test naming and both must pass independently
- [ ] `ENG-PG-01` implemented against real `GET /api/v1/coa/accounts` (OQ-PG-02 resolved in code, not just in mock)
- [ ] No critical/high security findings
- [ ] Test coverage ≥ 80% on `03_LOGIC.md` functions/engine

### Documentation
- [ ] API docs published from `02_API.md`
- [ ] `04_DB.md` §4.4 migration note (lookup table, not hardcoded enum, for bus/prod groups) followed by actual DDL

### QA
- [ ] All P0 test cases pass
- [ ] AC-14 (negative — no replace-mode UI) explicitly checked, not skipped as "trivially true"
- [ ] Cross-module cases §6.9 pass

### Deployment
- [ ] Migration script tested in staging
- [ ] Monitoring: GL Resolve Success Rate dashboard wired (BRD §18.2) — depends on OQ-PG-03 resolution, may ship as "N/A — pending real `used` sync" initially

---

## §6.5 WebSocket Events

None. BRD confirms no real-time/NOTIF requirement (OB-5).

---

## §6.6 Performance Benchmarks

| Endpoint | P95 latency | Notes |
|---|---|---|
| GET /gl/posting-groups (list) | < 500ms | Low volume (~500 combos designed capacity, BRD §17.5) |
| POST /gl/posting-groups | < 800ms | includes ENG-PG-01 COA-resolve round trip |
| POST /gl/posting-groups/import/commit | < 3s for 100 rows | Merge-only insert, no update path to slow it down |

---

## §6.7 Test Environment Notes

- Mock `ENG-PG-01` in TEST mode against a seeded COA fixture matching the 16-account mock set, until F-COA-001's real endpoint is available in staging.
- Seed script must include at least one record per kind with `used>0` and one with `used=0`, to exercise both IR-PG-01 branches.

---

## §6.8 Trace: AC → Logic Coverage

| AC | API tested | Functions tested | Engine tested |
|---|---|---|---|
| AC-01 | F-PG-API-02 | FN-01, FN-03 | ENG-PG-01 |
| AC-02 | F-PG-API-02 | FN-03 (negative) | — |
| AC-03 | F-PG-API-02 | FN-03 (negative) | ENG-PG-01 |
| AC-04 | F-PG-API-11 | FN-07, FN-09 | ENG-PG-01 |
| AC-05 | F-PG-API-11 | FN-09 (negative) | — |
| AC-06 | F-PG-API-04/13 | FN-02/FN-08 | — |
| AC-07 | F-PG-API-04 | FN-02 (negative — IR-PG-01) | — |
| AC-08 | F-PG-API-13 | FN-08 (negative — IR-PG-01) | — |
| AC-08b | F-PG-API-04/13 | FN-02/FN-08 (negative — R05) | — |
| AC-09 | F-PG-API-05/14 | FN-05/FN-11 | — |
| AC-10 | F-PG-API-06/15 | FN-06/FN-12 | — |
| AC-11..14 | F-PG-API-07/08/16/17 | FN-13/FN-14 | ENG-PG-01 |
| AC-15 | F-PG-API-09/18 | FN-15 | — |
| AC-16 | — (engine-level test) | — | ENG-PG-01 |
| AC-18 | — (client-only) | (client `onKindChange`, no server function) | — |

> Coverage check: FN-01..FN-17 and ENG-PG-01 all appear above or in §6.2 — no orphan.

---

## §6.9 Cross-Module Test Cases

| ID | Scenario | Downstream checked | Expected |
|---|---|---|---|
| XT-01 | Item Master calls `GET /gl/posting-groups?type=product` | Item Master (F-PDM) | Returns current 2-value set (`GOODS`,`SERVICE`) — test must assert this is the **as-built gap**, not fail the test as a bug (see OQ-PG-04) |
| XT-02 | Item Master calls `GET /gl/vat-groups` | Item Master (F-PDM) | Returns `[]` + gap metadata, HTTP 200 (not an error) — confirms graceful-degradation contract (OQ-PG-01) |
| XT-03 | Edit `account_1` on a `used>0` group, then simulate a new document post | GL/Journal Engine (mocked/stubbed) | New posts resolve to the **new** account; a pre-existing (already-posted) journal line reference is **not** altered — confirms "new postings only, no retroactive re-resolve" (BRD §5.2.2) |
| XT-04 | Set a group's status to `inactive`, then simulate a new document trying to resolve it | GL/Journal Engine (mocked/stubbed) | Resolve fails (by design, BR-06) — GL Engine's own error surface is out of scope, but this feature's data state (inactive → excluded from active-only resolve set) is what's under test here |

---

## §6.10 Microcopy-Aware Expected Text (verbatim from `f-postgrp.html`)

| Context | Exact text (Thai, as-built) |
|---|---|
| Create submit button | `ยืนยันสร้าง` |
| Edit submit button | `บันทึกการแก้ไข` |
| Submitting state | `กำลังบันทึก…` |
| Cancel button | `ยกเลิก` |
| Close view drawer | `ปิด` |
| Toast — group created | `สร้าง Posting Group แล้ว` |
| Toast — setup created | `สร้าง Posting Setup แล้ว` |
| Toast — group edited | `บันทึกการแก้ไขกลุ่มแล้ว` |
| Toast — setup edited | `บันทึกการแก้ไข setup แล้ว` |
| Toast — dup code | `รหัสกลุ่มนี้มีอยู่แล้ว` |
| Toast — dup combination | `ชุดกลุ่มนี้มีอยู่แล้ว` |
| Toast — IR-PG-01 block (tab1) | `กลุ่มนี้มีการบันทึกบัญชีผ่านแล้ว — เปลี่ยนรหัสไม่ได้ (แก้ชื่อ/บัญชี/สถานะได้)` |
| Toast — IR-PG-01 block (tab2) | `ชุดกลุ่มนี้มีการบันทึกบัญชีผ่านแล้ว — เปลี่ยนกลุ่มธุรกิจ/สินค้าไม่ได้ (แก้บัญชี/สถานะได้)` |
| Lock tag (inline, both tabs) | `ล็อก — มีการบันทึกบัญชีแล้ว` |
| Status change toast (single) | `เปลี่ยนสถานะเป็น [label] แล้ว` |
| Status change toast (bulk) | `เปลี่ยนสถานะ N รายการเป็น [label] แล้ว` |
| Delete confirm modal body | `ยืนยันการลบ — รายการที่มี journal post ผ่าน mapping แล้วจะไม่ถูกลบ (R06 soft-delete) ใช้วิธีเปลี่ยนสถานะเป็น "ไม่ใช้งาน" แทน` |
| Bulk delete toast (with skip) | `ลบแล้ว N รายการ · ข้าม M (มีการบันทึกบัญชีผ่านแล้ว)` |
| Empty state title | `ไม่พบรายการที่ตรงกับเงื่อนไข` |
| Empty state desc | `ลองปรับคำค้นหรือล้างตัวกรอง` |
| Import — file picked, valid summary | `ตรวจแล้ว N แถว — นำเข้าได้ OK · ติดปัญหา M (แถวผิดจะถูกข้าม)` |
| Import — row valid | `✓ พร้อมนำเข้า` |
| Import commit button | `นำเข้า N แถว` |
| Import commit toast | `นำเข้าแล้ว N รายการ` (+ `· ข้าม M แถว` if any skipped) |
| Import — download template button | `ดาวน์โหลด template ตัวอย่าง` |
| Export button | `ส่งออก CSV` |
| Export toast | `ส่งออก N รายการเป็น CSV แล้ว` |

> All of the above are exact matches to strings found in `f-postgrp.html` (grep-verified during Phase 3.5). No microcopy was invented for this feature; the central `microcopy.md` (html-generator-v7 knowledge) was consulted only as a fallback pattern-check (e.g. confirming "ยืนยันสร้าง"/"บันทึกการแก้ไข" match the lane standard) — the screen's own text always wins per HTML-first policy.
