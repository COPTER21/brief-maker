# _UX_CHECK_REPORT — F-HR-WELFARE (สวัสดิการ / Welfare)

**Step:** WF-01 · Step 3 (`qc-ux-html-checker`) — **RE-RUN / Iteration 7** (C3.2 — re-gate หลังเพิ่ม **reversal feature (กลับรายการ)** + **exposure display** · research-approved by PM/BA)
**Target:** `outputs/F-HR-WELFARE/welfare.html` (3,268 บรรทัด) — MASTER + light-txn (**NOT Pattern Q**)
**Archetype:** MASTER + light transaction (4 tabs = 1 menu #104) — ไม่มีเลขรัน/PDF/doc-wizard/line-editor → **Pass D ไม่ trigger** (`is_document=false`) โดยเจตนา
**Sync Read from:** `html-generator-v9` (เวอร์ชันสูงสุดที่ติดตั้ง) · iron-rules #1–#103 + #81 · knowledge/ (ci-tokens, layout-integrity, component-contracts, page-anatomy, microcopy)
**Passes run:** audit.sh · static_scan.py · **Render Gate (playwright/venv — route sweep @1440 + targeted reversal-state render: requests tab / request-view approved-admin / modalReverse / error / Esc chain / post-reverse pill+detail+history / balance-exposure / employee-persona)** · Pass G geometry · Loop diff
**Date:** 2026-09-08

---

## คำตัดสิน / VERDICT: **PASS (with 4 warnings)** — BLOCK = 0 → ไปต่อ step 4 ได้

| Severity | จำนวน | หมายเหตุ |
|:--:|:--:|---|
| 🔴 BLOCK | **0** | ไม่มี iron-rule violation · audit.sh FAIL=0 · pageerrors/console-error = 0 ทุก state ที่เรนเดอร์ |
| 🟡 WARN | **4** | ทั้งหมด carried known-benign (task-declared) — UX-01/02/04/05 · ไม่ re-litigate |
| 🟢 BENIGN (documented) | 4 | audit.sh WARN residuals (kit) — ไม่เปลี่ยนจากรอบก่อน |

> **Gate criterion** (project memory `html-v8-self-audit-not-zero-tolerance`): gate = **audit.sh FAIL=0 + documented residuals** → ผ่าน · self_audit ไม่ใช่ zero-tolerance

---

## ✅ โฟกัสรอบนี้ — reversal feature + exposure display (VERIFIED · หลักฐาน rendered)

| # | สิ่งที่เพิ่ม | ตรวจ | สถานะ | หลักฐาน (rendered) |
|:--:|---|---|:--:|---|
| R1 | สถานะ `reversed` + pill "กลับรายการแล้ว" (pill-danger) + filter option | list pill + status filter option | ✅ | `rev_06`: `REVERSED_PILL_IN_LIST=true` · `rev_07/08` header pill "กลับรายการแล้ว" · `FILTER_OPTS_HAS_REVERSED=true` (welfare.html:2290/2437) |
| R2 | ปุ่ม "กลับรายการ" (undo-2) ใน **request-view header** — เห็นเฉพาะ `status==='approved' && canApprove()` | button placement + visibility gate | ✅ | `rev_02`: ปุ่มอยู่ header top-right ข้าง X (per #98 header actions) · admin+approved → **visible** · หลัง reverse (status≠approved) → **หาย** · employee+approved → **ไม่มี** (welfare.html:2793) |
| R3 | modalReverse — reason required + error · mirror modalReject · Payroll clawback line เมื่อ pay='sent' | modal render + reason field + error path | ✅ | `rev_04`: warning icon + title + effect bullets + textarea `*` · `MODAL_HAS_REASON_FIELD=true` · `MODAL_HAS_PAYROLL_CLAWBACK_LINE=true` · `rev_05`: submit ว่าง → `REASON_ERROR_VISIBLE_ON_EMPTY=visible` (welfare.html:2974/3178) |
| R4 | detail tab reversal note + history reversal + EC-reverse audit lines (append-only) | detail note + history timeline | ✅ | `rev_07` detail banner "กลับรายการแล้ว: …คืนมูลค่าเข้าเงินได้ (7C · EC) · แจ้ง Payroll ตั้งเบิกคืน" · `rev_08` history: "ตัดคงเหลือ + บันทึกมูลค่าเข้า 7C EC" → "กลับรายการ · คืนมูลค่าเข้าเงินได้ (7C · EC)" → "แจ้ง Payroll ตั้งเบิกคืน" · approval timeline เดิมคงไว้ (welfare.html:2812/2869–2871) |
| R5 | balance tab exposure line (display-only) "คำขอรออนุมัติอื่นของสิทธิ์นี้: N ใบ · รวม {amount}" | note render + display-only | ✅ | `rev_03`: info-note "คำขอรออนุมัติอื่นของสิทธิ์นี้: 0 ใบ · —" · `EXPOSURE_LINE_SHOWS=true` (welfare.html:2847–2851) |
| R6 | Esc chain (combobox → modal → drawer) | overlay dismiss order | ✅ | Esc1 → modal ปิด (drawer คงเปิด) · Esc2 → drawer ปิด · `[F,T]→[F,F]` · backdrop is-open ถอดทันที (welfare.html:1774–1778) |
| R7 | Runtime health | pageerrors + console-error | ✅ | **0 / 0** ตลอดทุก state ที่เรนเดอร์ (2 scripts, ทุก persona/tab/modal) |

> **Button placement per contract:** ปุ่ม "กลับรายการ" ต่อท้าย `acts` แล้วส่งเข้า `headView(...)` = drawer header (ไม่ใช่ page header #105/business-action ปกติ) — ตรง #98 header-actions-by-status · icon `undo-2` · class `btn btn-sm btn-danger` เหมือนกลุ่ม reject/cancel

---

## รายการ Finding (ทั้งหมด carried · known-benign ตาม task context · non-blocking — ไม่ re-litigate)

### 🟡 UX-01 · WARN · CI hex hygiene — note/banner tints นอก whitelist (carried · task-declared benign: "note-tint hex")
- **พบ:** note tints `#FFE9E7 #E6F0FF #E4F4EB #FFF1DD` + text `#1A5FCC #157A41 #B8690B` (info/success/warn note) · **พิสูจน์:** audit.sh (gate จริง) ไม่ตรวจ hex → FAIL=0

### 🟡 UX-02 · WARN · Row density — content-driven row height (carried · task-declared benign: "content-driven row height")
- **พบ:** registry benefit row = **81px** @1440 (แถวชื่อ + ช่วงวันมีผล 2 บรรทัด · เวอร์ชัน retired) · geometry gate `ROW_TOO_TALL` = false positive สำหรับ content-driven (`td_pad_fat=0`) · ยืนยันด้วยภาพ `route_welfare.png`

### 🟡 UX-04 · WARN · filter-bar height flag / report reset-btn wrap ≤1280 (carried · task-declared benign)
- **พบ:** geometry gate `FILTER_STACKED 69px` (>60 cap) บน list · **พิสูจน์:** ภาพ `route_welfare.png` = filter **แถวเดียว** (search + status select + ล้างตัวกรอง) — 69px = input 44px + filter-bar padding ไม่ใช่ wrap 2 แถว → threshold false-positive · report reset-btn wrap ≤1280 = graceful ชิดขวา (task-declared benign)

### 🟡 UX-05 · WARN · trace/domain terms บนจอ (carried · resolved-clean)
- **Rule ref:** #81 · **พบ:** "7C · EC" (รหัสภาษี/บัญชี domain · research-approved) ใน 7C EC note/history — **ไม่ใช่** bare internal identifier (E-xxx/hook/bucket) · scan `#81` (excl comments) = **0** bare identifier บน rendered strings · "hook"/trace codes อยู่ใน comment เท่านั้น (task context: already resolved)

---

## Phase 1 — Mechanical Scan

**`audit.sh`:** `FAIL=0 · WARN=4` → ✅ ผ่าน gate. WARN 4 = residual documented (ไม่เปลี่ยนจากรอบก่อน):
- Rule #21 — `<i data-lucide>` sized ด้วย CSS class (kit rendering · benign)
- Rule #40 — `.uc-email` sub-line CSS (unused · benign)
- Token — hardcoded `font-size` ใน BASE-KIT (#69 verbatim · ห้ามแก้ · benign)
- Rule #103/#40 — line 2547 eligible-pill = **ternary เลือก pill เดียว** ไม่ได้ซ้อน 2 pill → false positive (`td_multi_pill=1`)

**`static_scan.py` facts:** `select_big=0` (#102 ok) · `combobox_count=17` · `overlay_root=true · portal_menu=true` · `page_fill=true · body_minwidth_768=true · render_table_only=true · scrollbar_gutter_stable=true` · `540px=0` (ไม่มี legacy drawer) · `440px=1` (confirm modal) · `doc_archetype.is_document=false` (master · Pass D ไม่ trigger — ถูกต้อง) · fonts = Satoshi + Noto Sans Thai (ในสแตก) · `hex #102/#104/#105` = false positive (เลขอ้าง Rule ในคอมเมนต์)

**JS parse / runtime:** SPA รันจริง **pageerrors = 0 · console-error = 0** ทุก state (route sweep + reversal targeted render 2 scripts)

---

## Render Gate — evidence (playwright/venv)

| ตรวจ | ผล |
|---|:--:|
| pageerrors + console-error (route sweep + reversal targeted + Esc + employee persona) | **0 / 0** |
| body horizontal scroll | **false** ทุก state |
| reversal button (approved + admin) render placement/gate | ✅ header top-right · gate ถูกต้อง 3 ทาง (admin-approved✓ / post-reverse✗ / employee✗) |
| modalReverse reason field + error + Payroll clawback + mirror reject | ✅ ครบ · error visible on empty submit |
| reversed pill (list + header) + detail reversal note + history reversal/EC lines | ✅ ครบ · append-only (approval timeline เดิมคงไว้) |
| balance exposure line (display-only) | ✅ info-note render clean |
| Esc chain (modal → drawer) | ✅ `[F,T]→[F,F]` |
| geometry gate flags | ROW_TOO_TALL 81px (content-driven · UX-02) · FILTER_STACKED 69px (threshold false-pos · UX-04) — carried benign, ยืนยันด้วยภาพ |

**หลักฐานภาพ (`outputs/F-HR-WELFARE/_shots/`):** `rev_01_requests_tab.png` · `rev_02_reqview_approved_admin.png` · `rev_03_balance_exposure.png` · `rev_04_modalReverse.png` · `rev_05_modalReverse_error.png` · `rev_06_list_reversed_pill.png` · `rev_07_reversed_detail.png` · `rev_08_reversed_history.png` · `rev_09_employee_no_revbtn.png` · `route_welfare.png` · `route_welfare_registry.png`

---

## Loop Diff (Iteration 7)

| สถานะ | รายการ |
|---|---|
| ✓ ใหม่ / ยืนยัน (รอบนี้) | **R1–R7 reversal + exposure** — pill/filter · button placement+gate (3 ทาง) · modalReverse (reason+error+clawback) · detail note + history reversal/EC · exposure line · Esc chain · pageerror=0 |
| ⏳ คงอยู่ | UX-01 · UX-02 · UX-04 · UX-05 — ทั้งหมด carried known-benign ตาม task context (ไม่ re-litigate) |
| ✓ ไม่ regress | audit.sh FAIL=0/WARN=4 · pageerror=0 · combobox anatomy/#102/#104/#105 · Pass D ไม่ trigger (master) · #81 list surface สะอาด · ไม่มี geometry block ใหม่จาก reversal changes |

---

## NOT-CHECKED (ระบุตามกติกา — ไม่นับผ่านเงียบ)
- **Pass D (Document Archetype #98–#101):** ไม่ trigger — master โดยเจตนา (`is_document=false`) · **ถูกต้อง**
- **Golden Compare กับ SO reference:** ข้าม — archetype ต่างชนิด (master vs Q-document) · ใช้ Visual Checklist + geometry แทน

---

## สรุปสำหรับ pipeline
- **BLOCK = 0** → step 3 re-gate ผ่าน · ดำเนินต่อ step 4 (`qc-coverage-checker`) ได้
- **Reversal feature + exposure display = VERIFIED render clean** ด้วย rendered evidence: reversal button (approved+admin only, placement per contract) · modalReverse (reason field + error) · reversed pill · detail reversal note · history reversal+EC audit lines · exposure line · Esc chain intact
- **pageerrors / console-error = 0** ทุก state
- WARN 4 = carried known-benign (task-declared) — non-blocking
- **ห้ามแตะ `welfare.html`** ในรอบตรวจนี้ (report-only) — ถ้าแก้ WARN ภายหลัง ต้องย้อนรัน step 3·4·5 (C3.2)
