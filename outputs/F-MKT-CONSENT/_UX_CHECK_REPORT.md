# _UX_CHECK_REPORT — F-MKT-CONSENT · ความยินยอม PDPA (F058)

> WF-01 **step 3** · skill `qc-ux-html-checker` — ตรวจ "ทำ**ถูก**มั้ย" (form / iron-rules / CI / UX heuristics)
> ไฟล์: `outputs/F-MKT-CONSENT/consent-pdpa.html`
> วันที่ตรวจ: 2026-09-14 · **รอบ 8 (loop mode)** — re-run หลัง **BA-gate surgical fixes** (FIX-01..08)

---

## VERDICT: ✅ PASS with 5 warnings (BLOCK = 0)

**BLOCK = 0 · WARN = 5 (residual cosmetic/BASE-KIT ทั้งหมด — ไม่มีตัวใหม่จาก BA fixes) · INFO = 3**
`audit.sh` (ด่านชี้ขาด) = **FAIL=0 · WARN=3** — **ลดจากรอบ 7 (WARN=5)** เพราะ 2 fixes ปิด residual เดิม:
- Rule **#44** (submit ไม่มี loader-2) → **หายแล้ว** (FIX-04 เพิ่ม spinner จริง)
- Rule **#103/#40** (cell มี pill 2 ตัว บรรทัด 2530) → **หายแล้ว** (FIX-08 refactor เป็น single-pill helper)

**BA fixes ทุกตัวยืนยันด้วยภาพสด (1280 + 1024) + วัด DOM — ผ่านทั้งหมด · ไม่มี issue ใหม่ · ไม่มี console/page error**

---

## Sync Read (Phase 0)
- Generator: **html-generator-v9** (`.claude/skills/html-generator-v9`) — iron-rules #1–#103 (อ่านสด)
- อ่าน: `iron-rules.md` · `layout-integrity.md` · `component-contracts.md` · `page-anatomy.md` · `ci-tokens.md` · `microcopy.md` + scripts `audit.sh`/`self_audit.py` + qc-ux `static_scan.py`
- กฎ **#104–#106** ที่ SKILL.md ของ qc-ux อ้าง **ไม่มีในตัว generator v9 ที่ติดตั้ง (#1–#103)** → **NOT-APPLICABLE**

## Archetype
- `doc_archetype.is_document = false` → ไม่ใช่เอกสารธุรกรรม (Q) → **Pass D ไม่ทริกเกอร์** ✅ (สอดคล้อง LOCK-07 ห้าม Pattern Q)
- master/list + resolver + recipient surface · single-screen create (ไม่มี wizard stepper)

---

## ⭐ จุดโฟกัสรอบนี้ — ยืนยัน BA-gate fixes (RENDER + measure)

หลักฐานภาพ: `scratchpad/_shots/` — render สด 1280×900 และ 1024×768 + วัด getComputedStyle/class/z-index/animation ด้วย DOM eval

### FIX-04 · `_busy` double-submit guard + `loader-2` spinner (แก้ Rule #44) ✅
- CSS บรรทัด 1518–1519: `.spin{animation:spin360 .8s linear infinite}` + `@keyframes spin360{to{transform:rotate(360deg)}}`
- `guardBusy(ev)` (บรรทัด ~2151): เซ็ต `state._busy`, `b.disabled=true`, ปุ่ม → `<i data-lucide="loader-2" class="w-4 h-4 spin"></i> กำลังบันทึก…`, ปลด lock ที่ 500ms
- วางท้าย mutation ทุกตัว **หลัง perm/validation** (submitReqCreate · submitRecipient · sendVia→ไม่, guardBusy เฉพาะปุ่ม submit หลัก · doWithdraw · doPublishVersion · doClosePurpose)
- **วัด DOM ตอนกดจริง (mid-flight 120ms):** `found=true · disabled=true · hasSpin=true · animationName=spin360 · text="กำลังบันทึก…"` — spinner หมุนจริง
- **ภาพ:** `04_submit_spinner.png` (submit สำเร็จ → toast "สร้างคำขอ REQ-2605 พร้อมลิงก์และ QR แล้ว")

### FIX-08 · purposes status = single-pill (แก้ Rule #103/#40) ✅
- `purStatusPill(s)` (บรรทัด ~2540): คืน pill เดียว (ใช้งาน / ปิดแล้ว) · เรียกที่ purposesBody บรรทัด 2552
- **วัด DOM:** ทุกแถว status cell = **1 pill พอดี** (`[1,1,1,1]`) — ไม่มี cell ที่มี ≥2 pill
- **ภาพ:** `02_purposes_table.png` (PUR-01 ใช้งาน · PUR-04 ปิดแล้ว — pill เดียวทุกแถว)

### FIX-03 · policy-version snapshot ตอนส่ง + stale near-tag ✅
- `snapshotVers(r)` (บรรทัด ~2749) เก็บเวอร์ชันต่อ purpose ลง `sends[].vers` ตอน `sendVia` · reqView อ่าน `lastSent` ล่าสุดที่มี `vers`
- near-tag แสดงเมื่อ `sentVer < currentVer`: `.near-tag` (บรรทัด 1588 — `var(--c-warning)` 11.5px inline-flex)
- **สร้าง scenario จริง:** ส่ง REQ-2601 (snapshot v2) → ออกเวอร์ชัน PUR-01 เป็น v3 → เปิด reqView
- **วัด DOM:** near-tag text = `"ส่ง v2 · ปัจจุบัน v3 — พิจารณาส่งคำขอใหม่"` · color `rgb(232,135,15)` (warning) · row แสดง `v2 เวอร์ชันที่ส่ง` + ลิงก์ `นโยบาย-PUR-01-v2.pdf`
- **layout สะอาด — near-tag อยู่ใต้ doc-link ไม่ล้น ไม่ดันแถว · purpose ที่ไม่ stale (v1) ไม่มี near-tag**
- **viewPolicy(code, ver)** (บรรทัด 3015) + policyModal อ่าน `d.ver` (บรรทัด 3017) — เปิด v1 → modal แสดงเอกสาร v1 ถูกต้อง (`09_policy_version_modal.png`)
- **ภาพ:** `05_reqview_staletag.png` · `08_officer_preview_demoonly.png`

### FIX-01 · answered-once guard + recipient closed-state page ✅
- `applyAnswers` guard (บรรทัด ~2762): `if(!['draft','pending'].includes(r.status)) return` + `r.answeredAt` ตอนตอบ
- **วัด DOM:** เรียก `applyAnswers` ซ้ำบน REQ-2603 (answered) → status คงเป็น `answered` (blocked=true) ✅
- `recipientViewHTML` closed-branch (บรรทัด ~2828): non-pending → แสดงหน้า "คำขอนี้ปิดแล้ว" (ไม่มีฟอร์ม)
- **วัด DOM:** REQ-2603 (answered) → `showsClosed=true · hasSubmitForm=false · simbar demo-only present` · REQ-2604 (expired) → `showsClosed=true · hasSubmitForm=false` ทั้งคู่
- **ภาพ:** `07_recipient_closed.png` (card "คำขอนี้ปิดแล้ว" + subject chip + simbar demo-only บนสุด · ไม่มีฟอร์มยินยอม)

### FIX-02 · persona guards ใน mutation + FIX-05 · status guards ✅
- `PERM()` guard ต้นทุก mutation: submitReqCreate(reqCreate) · sendVia(send) · applyAnswers(sign) · doWithdraw(withdraw) · doPublishVersion/doClosePurpose(purpose=DPO)
- status guards: sendVia/applyAnswers เฉพาะ draft/pending · doWithdraw เฉพาะ granted (`effStatus`)
- ยืนยันทางโค้ด + live (answered-once + effStatus block ทำงาน) — ไม่มี jargon ภายในรั่วขึ้นจอ (#81) · ข้อความ warning เป็น microcopy ไทย

### demo-only elements (มองเห็นได้ตามปกติใน prototype) ✅
- `.demo-strip demo-only` (บรรทัด 1683) · `.rcp-simbar demo-only` (recipient) · officer preview section `<div class="demo-only">` (reqView)
- **วัด DOM:** ไม่มี CSS rule ซ่อน `.demo-only` (grep = ไม่พบ) · demo-strip = `display:flex, visibility:visible, h=44` · simbar = `display:flex` · officer preview = `display:block, h=152`
- **`demo_only_any_hidden = 0`** — ไม่มีตัวไหนถูกซ่อนโดยพลาด ✅ (production build เป็นคนตัด class นี้ ไม่ใช่ CSS)

### Contract anchor comments (F136/F031/F157) ✅
- HTML comment ใน `<head>` (บรรทัด 7–10) + เหนือ registry (บรรทัด ~2419) + เหนือ resolve (บรรทัด ~2561) — **ไม่ render ขึ้นจอ** · เป็น anchor เชิงเอกสารเท่านั้น

### DSP-01..04 — ยังครบ ✅
- **DSP-01** (modal เหนือ drawer): คลิก doc-link ใน drawer → policyModal เปิด · วัด `modalBackdrop z=60 > drawer z=55` · Esc ปิด modal ก่อน drawer ยังเปิด (`esc_chain: modal_still_open=false, drawer_still_open=true`) ✅
- **DSP-02/03/04** (combobox close-on-select/no-autoopen · portal/flip · bubble-phase outside-click): **diff ไม่แตะโค้ด combobox/overlay z เลย** — combos present (2 ใน reqCreate) · ยกผลรอบ 7 มา ยังใช้ได้

---

## Phase 1 — Mechanical Scan

### audit.sh (ด่านชี้ขาด) → FAIL=0 · WARN=3 (residual BASE-KIT — ไม่ re-flag)
| # | WARN | สถานะ |
|---|---|---|
| Rule #21 | `<i data-lucide>` บางตัวไม่มี class `w-/h-` (brand 1684 + combobox/empty helpers) | documented residual |
| Rule #40 | `.uc-email` sub-line ในเซลล์ (บรรทัด 700) | documented residual |
| Token | hardcoded font-size บรรทัด 86/133/134/149/172 (BASE-KIT) | documented residual |

> **หาย 2 ตัวจากรอบ 7:** Rule #44 (loader-2) และ Rule #103/#40 (double-pill) — จาก FIX-04 + FIX-08

### static_scan.py — ไม่มี hex/font นอก whitelist ตัวใหม่
- `#EAF2FF/#BBD3FF/#1A4F9E` (info-blue banner มุมมองผู้รับ) = **ของเดิม** (diff ย้ายตำแหน่ง ไม่ได้เพิ่มสีใหม่)
- `#104`/`#105` ที่ script รายงานเป็น "hex" = **false-positive** — เป็นเลขอ้างกฎในคอมเมนต์ (`(#105)` demo-strip ฯลฯ) ไม่ใช่สี

---

## Fix list (WARN — ไม่บล็อก gate · residual ยกจากรอบก่อน · ไม่แย่ลง · อยู่นอกขอบเขต BA fixes)

| id | severity | rule ref | ตำแหน่ง | พบอะไร | วิธีแก้ (concrete) |
|---|---|---|---|---|---|
| UX-03 | WARN (คงเดิม) | Pass G (numeric align) | purposes: `td.num` "อายุ (เดือน)" + "% ครอบคลุม" | ตัวเลขไม่ชิดขวา (`text-align:start`) / ไม่มี tabular-nums | `.num{ text-align:right; font-variant-numeric:tabular-nums; }` |
| UX-04 | WARN (คงเดิม) | H-overlay / #66 | `.demo-strip`(z90) vs `.dw-footer-left` ที่ ≤1024 | demo-strip อาจทับปุ่มซ้ายสุดของ footer — ไม่เกี่ยว BA fixes (ไม่แตะ z/position) | `body.drawer-open .demo-strip{display:none}` (fix เดิมยังไม่ได้ apply) |
| UX-01 | WARN | H-CI (token drift) | `.rz-json`/`.http-chip` (code viewer) | hex นอก whitelist ในบล็อกโค้ด | ยอมรับได้ในฐานะ code block — ถ้าเก็บ ย้ายเป็น `--code-*` |
| UX-02 | WARN | H-CI (token drift) | `.warn-banner` info-blue inline | ใช้สีใกล้ family แต่ไม่ตรง token | ปรับเป็น `--c-info-*` ถ้าต้องการ token-purity |

## INFO (ไม่ต้องแก้)
- `.doc-link` semantic เป็น `<button>` (ถูกต้องเพื่อ a11y/keyboard) style เป็นลิงก์ — ตรงเจตนา (ยกจากรอบ 7)
- policy modal / info-banner ใช้ info-blue inline (family เดียวกัน consistent) — ไม่ใช่ token drift ใหม่
- **PREFLIGHT stamp เปล่า** (template `_`) · gate ชี้ขาด = audit.sh (ไม่ตรวจ stamp) → ไม่บล็อก · แจ้งไว้ให้ผู้เขียน HTML กรอกจาก self_audit.py หากต้องการปิดช่องนี้

## NOT-CHECKED
- iron-rules #104–#106 — ไม่มีใน generator v9 ที่ติดตั้ง → ไม่นำมาตัดสิน

---

## สรุปสำหรับ WF-01
- **ผ่าน step 3** (BLOCK=0) — BA-gate fixes ยืนยันครบด้วยภาพสด 1280+1024 + วัด DOM:
  - **FIX-04 spinner** ✅ loader-2 + spin360 หมุนจริง · ปุ่ม disabled — **ปิด residual Rule #44**
  - **FIX-08 single-pill** ✅ status cell = 1 pill/แถว — **ปิด residual Rule #103/#40**
  - **FIX-03 stale near-tag** ✅ "ส่ง v2 · ปัจจุบัน v3" สีเตือน layout สะอาด + snapshot ver + viewPolicy(ver) ถูกเวอร์ชัน
  - **FIX-01 answered-once** ✅ guard block ตอบซ้ำ + recipient closed-state page (answered + expired) ไม่มีฟอร์ม
  - **FIX-02/05 persona+status guards** ✅ ทาง perm/effStatus/status ครบ
  - **demo-only** ✅ เห็นได้ตามปกติทุกตัว (demo-strip/simbar/officer-preview) ไม่มีตัวใดถูก CSS ซ่อนพลาด
- **ไม่พบ issue ใหม่** — z-tier ถูก (modal60>drawer55) · Esc chain ถูก · ไม่มี layout shift · ไม่มี console/page error · DSP-01..04 ครบ
- **ไม่พบ regression** — audit.sh WARN ลด 5→3 · WARN 3 ที่เหลือ = residual BASE-KIT เดิม
- WARN 5 (UX-01/02 token-drift cosmetic · UX-03 numeric align · UX-04 demo-strip overlap ≤1024) = ของเดิม non-blocking นอกขอบเขต BA fixes — ให้ผู้ใช้ตัดสินว่าจะเก็บก่อนส่ง dev หรือปล่อย
