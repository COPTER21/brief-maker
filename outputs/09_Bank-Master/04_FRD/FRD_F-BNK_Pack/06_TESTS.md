# 06_TESTS — F-BNK Bank Master

> **Audience:** QA engineer + ai-testcase-md-generator (downstream)
> **Purpose:** Acceptance Criteria + DoD + Cross-Module + Permission/Negative set
> **Coverage source:** 02_API + 03_LOGIC + 05_RULES + HTML (source of truth for expected text)
> **Expected text:** verbatim from HTML (see §6.10) — never guessed.

---

## §6.1 Acceptance Criteria (AC)

### AC-01: Create account — happy path
**Given** finance_admin on `#/bank-master`, company C1
**When** open "สร้างบัญชี", pick ธนาคาร + accNo `0012345678` + ชื่อบัญชี + ประเภท + สาขา + GL, click "ยืนยันสร้าง"
**Then** 201; row appears; toast **"สร้างบัญชีธนาคารสำเร็จ"**; audit `created`; number shows masked `••••••5678`.

### AC-02: Create — account number format
**Given** create drawer
**When** accNo = `12A` or `123` (too short)
**Then** blocked; inline **"เลขบัญชีต้องเป็นตัวเลข 10-15 หลัก"**; toast **"กรุณากรอกข้อมูลให้ครบถ้วน"**. (Non-digits stripped live.)

### AC-02b: Create — duplicate account per company (EC-01)
**Given** C1 already has accNo `0012345678`
**When** create another `0012345678` in C1
**Then** 422 BR_ACCNO_DUPLICATE; inline **"เลขบัญชีนี้มีอยู่แล้วในบริษัทนี้"**. (Same number in C2 = allowed.)

### AC-02c: Create — GL required (BR-BNK-11)
**When** submit without GL → inline **"กรุณาเลือกบัญชี GL"**.

### AC-03: Company switch (US-02)
**Given** ≥2 companies
**When** change company switcher → list shows only that company's accounts; empty company shows **"ยังไม่มีบัญชีธนาคาร"** + "สร้างบัญชี".

### AC-04: Default pay/receive unique per company (US-03/EC-03)
**Given** BA-001 is default_pay
**When** set BA-003 as default_pay → BA-001 default_pay cleared automatically (≤1/company); toast **"ตั้งเป็นบัญชีจ่ายเริ่มต้นแล้ว"**; audit `set-default`. default_pay + default_receive may coexist on different accounts.

### AC-04b: Concurrent default set (EC-12)
**When** two users set different accounts as default_pay simultaneously → last-write-wins; exactly one remains default_pay (partial-unique index); both writes audited.

### AC-05: Deactivate / activate (US-06)
**When** deactivate active account (modal "ปิดใช้งานบัญชีนี้?") → status inactive; toast **"ปิดใช้งานบัญชีแล้ว"**; audit `deactivated`. Activate inactive → active; toast **"เปิดใช้งานบัญชีแล้ว"**.

### AC-05b: Inactive gone from picker (EC-04)
**When** account inactive → absent from API-16 pickable + doc picker; existing doc `PV-2025-014` still shows it (soft-ref).

### AC-05c: Default account deactivated/archived (EC-14 / OQ-BNK-05 — RESOLVED 2026-08-06: warn + clear)
**Given** a default_pay and/or default_receive account
**When** deactivated or archived → the confirm modal shows an explicit default-loss warning note, and on confirm the `defaultPay`/`defaultReceive` flag **is cleared**; new-doc picker has no auto-default until re-selected. **Confirmed rule (not `[AI-DEFAULT]`).**

### AC-06: Archive used account (US-07/EC-06)
**Given** `used_in_doc=true`
**When** archive (modal shows used-in-doc lock note) → status archived; toast **"เก็บถาวรบัญชีแล้ว"**; audit `archived`. **No hard-delete path exists.**

### AC-06b: Archived is terminal (EC-09)
**Given** archived account → no "เปิดใช้งาน"/"เก็บถาวร" buttons; no API path to reactivate; API-07 on archived → 422 BR_INVALID_TRANSITION.

### AC-07: Reveal WITH permission (US-05) ⭐
**Given** finance_admin with `canRevealFull=true`
**When** click "ดูเต็ม" → full number shown; toast **"บันทึกการเข้าถึงเลขบัญชีเต็มแล้ว"**; **audit `revealed` written (actor + timestamp + account_id)**. "ซ่อน" re-masks.

### AC-08: Reveal WITHOUT permission (US-04/EC-05) ⭐ **P0 negative**
**Given** user with `canRevealFull=false`
**When** click "ดูเต็ม" → **denied**; number **stays masked**; toast **"คุณไม่มีสิทธิ์ดูเลขบัญชีเต็ม"** (warning). Full number never leaves the server. (Also verify no full number in list/detail/API-01/03 payloads.)

### AC-09: Export/print masking (EC-15/OQ-BNK-03) ⭐ **P0 negative**
**When** export/print account list as a user without permission → account numbers masked to last-4; full reveal requires permission + writes audit. `[AI-DEFAULT]`.

### AC-10: Create custom bank (US-08)
**When** banks tab → "สร้างธนาคาร", name + abbr + SWIFT `HSBCTHBK` (8) + type foreign → 201; toast **"สร้างธนาคารสำเร็จ"**; audit `bank-added`; appears in bank-audit section.

### AC-11: Custom bank SWIFT format (EC-07)
**When** SWIFT = `HSBC` (4 chars) → blocked; inline **"SWIFT ต้องมี 8 หรือ 11 หลัก"**. Duplicate SWIFT → **"รหัส SWIFT นี้มีอยู่แล้ว"**.

### AC-12: Delete custom bank used>0 (US-09/EC-08) ⭐ W1
**Given** custom bank with `used_count>0`
**Then** delete button **disabled**, tooltip **"มี {N} บัญชีอ้างอิงธนาคารนี้ — ลบไม่ได้"**; forced API-13 → 422 BR_BANK_IN_USE, toast **"ลบไม่ได้ — มี {N} บัญชีอ้างอิงธนาคารนี้อยู่ (ย้าย/ปิดบัญชีก่อน)"**.

### AC-13: Delete custom bank used=0 + preset read-only (US-09/BR-BNK-12) ⭐ W1
**Given** custom bank `used_count=0` → delete succeeds; audit `bank-removed`; toast **"ลบธนาคารแล้ว"**.
**Given** preset ธปท. bank → no edit/delete buttons (cell "มาตรฐาน"); edit attempt → toast **"ธนาคารมาตรฐาน ธปท. แก้ไขไม่ได้"**; API-12/13 → 403 ERR_PRESET_READONLY.

### AC-14: Every action audited (BR-BNK-07)
**Then** create/edit/reveal/set-default/deactivate/activate/archive/bank-added/bank-edited/bank-removed each produce exactly one append-only entry; audit is never editable/deletable; view drawer "ประวัติ ({n})" and bank section show newest-first.

### AC-15: Currency THB lock (BR-BNK-10)
**Then** currency field readonly `THB — บาทไทย` + info-tip; API ignores any other currency sent; stored `THB`.

### AC-16: Backend permission gate (EC-13/OQ-BNK-04) ⭐ **P0 negative**
**Given** user without edit permission
**When** call API-04/API-02 directly (bypassing hidden UI) → 403 ERR_INSUFFICIENT_ROLE / ERR_PERMISSION_REVOKED. Hiding the button is NOT the control.

### AC-17: Idempotent create (EC-16)
**When** double-submit create with same `Idempotency-Key` → single account; second returns cached; no duplicate audit.

### AC-18: Stale edit (EC-17)
**When** edit with stale `If-Match` version → 409 ERR_STALE_DATA.

---

## §6.2 Test Case Inventory

| TC ID | Name | Type | Maps to AC | Priority |
|---|---|---|---|---|
| TC-01 | Create account happy | API/UI | AC-01 | P0 |
| TC-02 | AccNo format block | API neg | AC-02 | P0 |
| TC-02b | AccNo duplicate/company | API neg | AC-02b | P0 |
| TC-02c | GL required | API neg | AC-02c | P1 |
| TC-03 | Company switch scope | UI | AC-03 | P1 |
| TC-04 | Default unique/company | API | AC-04 | P0 |
| TC-04b | Concurrent default | stress | AC-04b | P2 |
| TC-05 | Deactivate/activate | API | AC-05 | P0 |
| TC-05b | Inactive gone from picker | API/XT | AC-05b | P1 |
| TC-05c | Default deactivated/archived → warn + clear flag | API | AC-05c | P2 |
| TC-06 | Archive used account | API | AC-06 | P0 |
| TC-06b | Archived terminal | API neg | AC-06b | P1 |
| **TC-07** | **Reveal WITH permission + audit** | API/UI | AC-07 | **P0** |
| **TC-08** | **Reveal WITHOUT permission (masked stays)** | **API neg — security** | AC-08 | **P0** |
| **TC-09** | **Export/print masking** | neg — security | AC-09 | **P0** |
| TC-10 | Create custom bank | API | AC-10 | P1 |
| TC-11 | SWIFT format/dup | API neg | AC-11 | P1 |
| **TC-12** | **Delete custom bank used>0 blocked** | API neg — W1 | AC-12 | **P0** |
| TC-13 | Delete used=0 + preset read-only | API | AC-13 | P1 |
| TC-14 | Full audit coverage | API | AC-14 | P1 |
| TC-15 | Currency THB lock | API/UI | AC-15 | P2 |
| **TC-16** | **Backend permission gate (direct call)** | neg — security | AC-16 | **P0** |
| TC-17 | Idempotent create | API | AC-17 | P2 |
| TC-18 | Stale edit 409 | API | AC-18 | P2 |
| XT-01..04 | Cross-module pickers | integration | §6.9 | P1 |

> **Permission / negative set (the security spine — all P0):** TC-07, TC-08, TC-09, TC-12, TC-16. These MUST pass before release.

---

## §6.3 Test Data Setup
- 2 companies: C1 `บริษัท ทูบี ซิมเปิล จำกัด`, C2 `บริษัท คิวบ์ เทค โซลูชันส์ จำกัด`.
- 22 preset banks (5 foreign) + ≥1 custom bank (one with used>0, one with used=0).
- 6 CoA GL codes incl. `1010-06 เงินฝากธนาคาร - บัญชีเงินเดือน` (payroll).
- 5 seed accounts across statuses (active/inactive; used_in_doc mix) as in HTML (BA-001..005).
- Users: `qa_finance_admin` (canRevealFull=true), `qa_finance_admin_noreveal` (canRevealFull=false), `qa_finance_user` (view-only), `qa_accounting`.

---

## §6.4 Definition of Done (DoD)
**Code:** all AC implemented + unit tests; masking never leaks full number in list/detail/picker/export; reveal audit-first; `accNo_length_range` from config (not hardcoded); `canRevealFull` from RBAC (not hardcoded `true`).
**QA:** all P0 (incl. security set TC-07/08/09/12/16) + P1 pass; no P0/P1 open bugs.
**Security:** D-CLASS verified; `acc_no` encrypted at rest; Restricted Resources registration confirmed (OQ-BNK-06) or explicitly waived.
**Docs:** 07_LOCKED reflects final; ENG-BNK-01/02 registered with CUBIC (or LD-02 defer noted).
**Deploy:** migration + preset seed tested in staging; audit append-only privileges verified (no UPDATE/DELETE grant).

---

## §6.5 WebSocket Events
None — no realtime in this master. (Reveal anomaly surfaces via monitoring dashboard, BRD §18, not push.)

## §6.6 Performance Benchmarks
| Endpoint | Target |
|---|---|
| GET /bank-accounts (list, masked) | < 500ms (SLA save<2s, reveal<1s — BRD §17.1) |
| POST /bank-accounts | < 2000ms |
| POST …/reveal (+audit write) | < 1000ms, audit success 100% |

## §6.7 Test Environment Notes
- Reveal denial only reachable by flipping `canRevealFull=false` (prototype ships `true` per OQ-1 mock) — QA MUST test with the no-reveal user.
- Doc picker (M-03) is a mock; real cross-module flow tested against API-16.
- No print/PDF surface in prototype — AC-09 tested at API/export layer.

## §6.8 Trace: AC → Logic Coverage
| AC | API | Functions | Engines |
|---|---|---|---|
| AC-01 | API-02 | FN-01, FN-03, FN-06, FN-12 | ENG-BNK-01 (last-4) |
| AC-02/02b/02c | API-02 | FN-03 (neg) | — |
| AC-04/04b | API-09 | FN-06, FN-12 | — |
| AC-05/06/06b | API-06/07/08 | FN-07, FN-12 | — |
| AC-07 | API-05 | FN-05, FN-12 | **ENG-BNK-01** |
| AC-08/09/16 | API-05/01/04 | FN-05 (deny), FN-04 | ENG-BNK-01 |
| AC-10/11 | API-11 | FN-08, FN-12 | **ENG-BNK-02** |
| AC-12/13 | API-13/12 | FN-10, FN-09, FN-12 | — |
| AC-14 | all mutations | FN-12 | — |
| AC-17/18 | API-02/04 | FN-01/FN-02 | — |

> Coverage: every Function (FN-01..12) + both Engines traced ≥1 AC. ✅

---

## §6.9 Cross-Module Test Cases ⭐ (R12 — from BRD §12.1)

| ID | Scenario | Downstream | Expected |
|---|---|---|---|
| XT-01 | PV picks pay-from account | Payment Voucher | API-16 returns active accounts (masked); PV snapshots values; later account edit does NOT change issued PV |
| XT-02 | RV auto-selects default-receive | Receipt Voucher | pickable includes `is_default_receive`; RV pre-selects it |
| XT-03 | Bank Recon references account then account archived | Bank Reconciliation | recon history preserved (no cascade); archived account absent from new recon picker |
| XT-04 | **Payroll picks disbursement account (GL 1010-06)** ⭐ | Payroll | API-16 (purpose=pay) returns active account bound to payroll GL; payroll run snapshots; account inactive → next run can't pick, prior run intact |

> Every downstream in BRD §12.1 has ≥1 case. Payroll named explicitly (closes W2).

---

## §6.10 Microcopy-Aware Expected Text (verbatim from HTML — source of truth)

**Toasts:** create `สร้างบัญชีธนาคารสำเร็จ` · edit `บันทึกการแก้ไขแล้ว` · reveal ok `บันทึกการเข้าถึงเลขบัญชีเต็มแล้ว` · reveal denied `คุณไม่มีสิทธิ์ดูเลขบัญชีเต็ม` · validation `กรุณากรอกข้อมูลให้ครบถ้วน` · set-default `ตั้งเป็นบัญชีจ่ายเริ่มต้นแล้ว` / `ตั้งเป็นบัญชีรับเริ่มต้นแล้ว` / `ยกเลิกค่าเริ่มต้นแล้ว` · default-on-nonactive `บัญชีต้องอยู่สถานะใช้งานก่อนตั้งเป็นค่าเริ่มต้น` · activate `เปิดใช้งานบัญชีแล้ว` · deactivate `ปิดใช้งานบัญชีแล้ว` · archive `เก็บถาวรบัญชีแล้ว` · bank create `สร้างธนาคารสำเร็จ` · bank delete `ลบธนาคารแล้ว` · bank delete blocked `ลบไม่ได้ — มี {N} บัญชีอ้างอิงธนาคารนี้อยู่ (ย้าย/ปิดบัญชีก่อน)` · preset edit `ธนาคารมาตรฐาน ธปท. แก้ไขไม่ได้` · doc pick `เลือกบัญชี {abbr} {maskedNo} แล้ว (จำลอง)`.

**Buttons:** `สร้างบัญชี` · `สร้างธนาคาร` · `ยืนยันสร้าง` · `บันทึกการแก้ไข` · `ยกเลิก` · `แก้ไข` · `ปิดใช้งาน` / `เปิดใช้งาน` · `เก็บถาวร` · `ดูเต็ม` / `ซ่อน` · `ปิด` · `เลือก` · `ล้างตัวกรอง` · `จำลองเลือกในเอกสาร` · submitting `กำลังบันทึก…`.

**Modal confirms:** archive title `เก็บถาวรบัญชีนี้?` · deactivate title `ปิดใช้งานบัญชีนี้?` · doc picker `จำลอง: เลือกบัญชีในเอกสาร`.

**Inline validation:** `กรุณาเลือกธนาคาร` · `กรุณากรอกเลขที่บัญชี` · `เลขบัญชีต้องเป็นตัวเลข 10-15 หลัก` · `เลขบัญชีนี้มีอยู่แล้วในบริษัทนี้` · `กรุณากรอกชื่อบัญชี` · `กรุณาเลือกบัญชี GL` · `กรุณากรอกชื่อธนาคาร` · `กรุณากรอกชื่อย่อ` · `กรุณากรอกรหัส SWIFT` · `SWIFT ต้องมี 8 หรือ 11 หลัก` · `รหัส SWIFT นี้มีอยู่แล้ว` · `รหัส ธปท. ต้องเป็นตัวเลข 3 หลัก`.

**Empty:** `ยังไม่มีบัญชีธนาคาร` / `ไม่พบรายการที่ค้นหา` / `ไม่พบธนาคารที่ค้นหา` / `ยังไม่มีประวัติ` / `ยังไม่มีการสร้างหรือลบธนาคารที่สร้างเอง`.

**Tooltips:** reveal `ต้องมีสิทธิ์ · ระบบจะบันทึกการเข้าถึง` · delete-disabled `มี {N} บัญชีอ้างอิงธนาคารนี้ — ลบไม่ได้`.

> Value display: masked = `••••••NNNN` (bullets = count of hidden digits + last-4); empty = `—`. Downstream ai-testcase-md-generator must match these 1:1.
