# _UX_CHECK_REPORT — F-HR-EXPENSE (`expense.html`)

**Skill:** `qc-ux-html-checker` · WF-01 step 3 ("ทำถูกมั้ย" / form) · **RE-GATE รอบ 11 (mandatory หลังแก้ HTML · C3.2)**
**Date:** 2026-09-10
**Generator (Sync Read):** `html-generator-v9` (`.claude/skills/html-generator-v9`) — iron-rules #1–#103 + #104/#105 + Pattern Q + B2 v2 + drawer-standard · `knowledge/*` + `patterns/Q_*` + `patterns/B2_*`
**Archetype:** Q-document (transaction) — `line-tbl` + `calcLineVat` + `renderSignTab` + `docPill`/`signProgress` + `a4` ⇒ **Pass D triggered**
**Passes run:** `audit.sh` (mechanical gate · **FAIL=0 WARN=4**) · `static_scan.py` (facts) · `self_audit.py` (geometry/overlay counters · residuals = documented baseline stamp · overlay/z/flip/jargon counters **เขียวหมด**) · manual iron-rule review (Pass D/G + heuristics + consistency) · **Render Gate (venv playwright · drive role/wizard/drawer จริง 4 scenario · `pageerrors=NONE` · `console.error=NONE` · หลักฐานภาพ `_shots/A|B|C|D.png` + `_shots/RG.json`)**

**การเปลี่ยนแปลงรอบนี้ (3 touchpoint · PM/BA เคาะ 2026-09-10 · display-only/enum เท่านั้น · ไม่แตะ z-index/layout/line-engine/FN scope):**
- **Δ1 · pay-channel enum +2** — `PAY_OPTS` (`:2165`) เพิ่ม `['pv','ใบสำคัญจ่าย (PV)']` + `['petty','เงินสดย่อย (F091)']` (เดิม payroll/transfer) · แสดงใน wizard step-2 `<select class="input">` (`:2298`) + `payLabel()`/`payDownstream()` display-only (BR-09: F101 ไม่จ่ายเงินเอง)
- **Δ2 · F103 clearing hookbox (display-only)** — `advanceHookHTML()` (`:2231`) `.sec`+`<h4>`+`.hookbox` แสดง "เคลียร์เงินทดรอง (F103)" · เรียกใน wizard review (step 5 · `:2309`) + view-drawer detail (`:2379`) · `maskM()` mask ตาม role (SoD) · mock `F103_ADVANCE_MOCK` — F101 ไม่ปรับยอดทดรองเอง
- **Δ3 · role ที่ 3 "เจ้าหน้าที่ (HR/Finance)"** — `EXP.roles` (`:2123`) `{id:'officer', scope:'all', approver:false, mask:false}` · อยู่ใน `.demo-strip` seg-control (`:2250`) **ไม่ใช่** page-header (#105 OK) · list-scope ผ่าน `visibleDocs()` (`:2173`) — requester/admin (scope:self) เห็นเฉพาะใบตน · officer (scope:all) เห็นทั้งหมด เห็นเงินเต็ม แต่ไม่ใช่ผู้อนุมัติ

---

## VERDICT: **PASS with 1 warning (carry-over OQ)** — BLOCK = 0 → re-gate ผ่าน, ไปต่อ step 4·5 (ต้องรันใหม่ตาม C3.2)

| Severity | Count | สรุป |
|:--:|:--:|---|
| 🔴 BLOCK | **0** | `audit.sh` FAIL=0 · Render Gate 4/4 scenario `pageerrors=NONE · console.error=NONE` · 3 touchpoint = display-only/enum เพิ่มบน BASE-KIT pattern เดิม (select enum <7 = ไม่ต้อง combobox #102 · hookbox = `.sec/.hookbox` เดียวกับ hook เดิมที่ accept แล้ว · role ที่ 3 อยู่ใน `.demo-strip` ไม่ใช่ header #105) · self_audit overlay/z/flip/jargon counters เขียวหมด · **ไม่มี regression** |
| 🟡 WARN | **1** | **UX-01** (carry-over จากรอบก่อน · B2 grid-contract deviation → OQ ให้ BA/PM เคาะ) — ไม่แตะรอบนี้ (task-accepted domain adaptation, remains WARN not BLOCK) |
| 🟢 BENIGN (documented) | 13 | benign เดิม 11 (drawer is-open lifecycle · SoD mask · hookbox display-only · chain approval · #100 label override · DOA slot picker · over-cap warn · reject-reason required · combo flip-up · 7 unsupported chips ฯลฯ) + **รอบนี้ +2**: (12) pay-channel enum +2 (display-only · render-verified 4 opts) · (13) F103 clearing hookbox (display-only · masked · render-verified) · plus `audit.sh` WARN=4 (kit-verbatim/optional) + `self_audit` residuals = **baseline stamp เดิม ไม่มีตัวใหม่** |

---

## Phase 1 — Mechanical Scan

### `audit.sh` → **FAIL=0 · WARN=4** (ไม่มี iron-rule violation)
- WARN #21 — `<i data-lucide>` บางตัวไม่มี `w-{N}/h-{N}` (kit template lines · benign)
- WARN #40 — `.uc-email` sub-line ใน cell (person cell meta ของข้อมูลเดียวกัน · #40-compliant · benign)
- WARN Token — hardcoded `font-size` บางจุด (11px/13px sidebar chrome · = baseline residual)
- WARN #99 — endbill segmented ฿/% (mode) — Pattern Q optional, domain expense ไม่ใช้ end-bill discount (benign)

### `self_audit.py` (Pass G geometry/overlay) → residuals = **documented baseline stamp**
`spacing_off=6 · font_off=3 · font_count=11 · flex_noalign=1 · inline_layout=0 · z_adhoc=0 · hex_off=3` — **ตรงกับ PREFLIGHT stamp เป๊ะ** (`round1 self_audit: spacing_off=6 font_off=3 font_count=11 flex_noalign=1 inline_layout=0 z_adhoc=0`) → stamp ไม่ปลอม · **ไม่มีตัวเลขใหม่จาก 3 touchpoint** (ตาม MEMORY: self_audit ≠ zero-tolerance · gate = audit.sh FAIL=0 + documented residuals)
- `hex_off=3 → #104/#106/#E7E2DB` — `#104`/`#106` = false-positive (comment อ้างเลข iron-rule #104/#106 ไม่ใช่สี) · `#E7E2DB` = near-token divider (audit.sh hex-whitelist ผ่าน = FAIL 0)
- overlay/handler counters **เขียวหมด**: `overlay_no_z=0 · z_adhoc=0 · menu_no_flip=0 · menu_no_bg_z=0 · no_global_outside_close=0 · undefined_handlers=0 · missing_ids=0 · jargon_leak=0 · duplicate_counts=0 · img_placeholders=0`

### `static_scan.py` facts (ตีความเทียบ token/rule สด)
- hex ทั้งหมดผ่าน whitelist (audit.sh ยืนยัน) · font-families = Satoshi/Noto stack + inherit เท่านั้น · fonts ผ่าน
- `540px=0` (ไม่มี legacy drawer) · `920/680` drawer มาตรฐาน · `1290px` = `.wide` wizard (allowed) · `440px` modal (allowed)
- `select_big=0` · `combobox_count=12` (master fields เป็น combobox ครบ) · `overlay_root=true · portal_menu=true · page_fill=true · body_minwidth_768=true · scrollbar_gutter_stable=true` — heuristics #95/#96/#97 ผ่าน
- `td_multi_pill=0` (#103 ok) · `hashchange_listener=true · escape_handler=true · drawer_translate=true · backdrop=true · scrollbar_width=5px`
- doc_archetype: `is_document · line_tbl · view_tabs=[detail,pdf,sign,history]` (ลำดับ #101 ถูก · ไม่มี tab attachments) · `attach_in_detail=true` · `calcLineVat/totals/taxBadgeV/docPill/signProgress/a4/slot_row/vat_segmented_3` = true ครบ
- **หมายเหตุ:** `wizard_steps=[]` ใน scanner = false-negative (ไฟล์ใช้ `stepper()`+`STEP_KEYS` ไม่ใช่ `renderStepperItem(`) — ยืนยันด้วยมือ: `STEP_KEYS` (`:2285`) = `เลือกแหล่งที่มา › ข้อมูลหลัก › รายการค่าใช้จ่าย › เอกสารแนบ › ตรวจสอบและยืนยัน` (5 step · #100 label override `รายการค่าใช้จ่าย` มี comment กำกับ) — **render-verified** (ดู Render Gate S-C)

## Phase 2–3 — Heuristic + Consistency (3 touchpoint review)
| touchpoint | ตรวจ | ผล |
|---|---|---|
| Δ1 pay-channel enum | select 4 options (<7 → ไม่บังคับ combobox #102) · เป็น enum ไม่ใช่ master-list · display-only (`payDownstream` ไม่ trigger จ่ายจริง · BR-09) | ✅ consistent · ไม่ใช่ violation |
| Δ2 F103 hookbox | `.sec`+`<h4>`(lucide banknote)+`.hookbox` = โครงเดียวกับ hookbox เดิม (F117/F102 accepted benign) · `maskM()` mask เงินตาม role (SoD) · แสดงใน review+detail สอดคล้อง | ✅ consistent · display-only |
| Δ3 role ที่ 3 | อยู่ใน `.demo-strip` seg-control (ล่าง) **ไม่ใช่** `.ph-right` → #105 OK · seg-item เหมือน 2 role เดิม · scope filter `visibleDocs()` clean | ✅ #105/#104 OK |

**#105 demo-persona control:** ทั้ง 3 role อยู่ใน `.demo-strip` (`:2248`) — page-header actions = business เท่านั้น ✅
**Component consistency:** seg-item / hookbox / select — ทั้งหมด reuse class เดิม ไม่มี divergent variant ✅

---

## 🔁 Render Gate — role scope + wizard enum + F103 hookbox (venv playwright · viewport 1280×860)
หลักฐานภาพ `_shots/*.png` + `_shots/RG.json` · drive DOM จริง · `pageerrors=NONE · console.error=NONE`

| # | scenario | drive | สังเกต (จริงจาก DOM) | expect | ผล |
|:--:|---|---|---|:--:|:--:|
| **S-A** | list default (role=admin scope:self) | load | `role=admin` · **rows=2** (เฉพาะใบ E01) · demo-strip 3 ปุ่ม `[ผู้เบิก/ธุรการ · ผู้อนุมัติ (DOA) · เจ้าหน้าที่ (HR/Finance)]` | scope self เห็นเฉพาะตน · role ที่ 3 โผล่ | ✅ (`A_list_default.png`) |
| **S-B** | switch role → officer (scope:all) | `setRole('officer')` | `role=officer` · **rows=6** (เห็นทั้งหมด) · active seg = `เจ้าหน้าที่ (HR/Finance)` | scope all + role switch ทำงาน | ✅ (`B_role_officer_scope_all.png`) |
| **S-C** | create wizard → step 2 | `openCreate()`→step2 | pay `<select>` opts = **`[ผ่านรอบเงินเดือน · โอนตรง · ใบสำคัญจ่าย (PV) · เงินสดย่อย (F091)]`** · stepper 5 = `เลือกแหล่งที่มา/ข้อมูลหลัก/รายการค่าใช้จ่าย/เอกสารแนบ/ตรวจสอบและยืนยัน` | enum +2 เรนเดอร์ · #100 stepper ถูก | ✅ (`C_wizard_step2_paychannel.png`) |
| **S-D** | view drawer d4 (E03 · มีทดรอง) | `openView('d4')` | `hasF103=true` (เคลียร์เงินทดรอง (F103) sec เรนเดอร์) · `hasAdvanceAmt=true` (เงินทดรองค้าง แสดง) · view tabs = รายละเอียด/PDF/ประวัติ(+sign) | F103 hookbox โผล่ใน detail | ✅ (`D_view_d4_F103_hookbox.png`) |

**สรุปหลักฐาน:** 4/4 PASS · `PAGE_ERRORS: NONE` · `CONSOLE.ERROR: NONE` — 3 touchpoint เรนเดอร์จริงถูกต้อง ไม่ก่อ page error / overlay regression → ไม่ตั้ง BLOCK

---

## 🟡 WARN — actionable (เหลือ 1 · carry-over OQ · ไม่แตะรอบนี้)

### UX-01 · WARN(→OQ) · Rule #83/#99 (B2 v2) — line grid ไม่ตรง grid-contract v2 (domain adaptation)
- **ตำแหน่ง:** `lineEditor()` / `.line-tbl` header — คอลัมน์ = `วันที่ · หมวด · รายละเอียด · จำนวนเงิน · VAT · รวม · (ลบ)`
- **พบ:** B2 v2 ล็อก grid 9-slot `26/—/64/92/92/78/72/104/54` (สินค้า/qty/หน่วย/ราคา/ส่วนลด%). ไฟล์นี้ใช้คอลัมน์ตามโดเมน expense — ไม่มี qty/หน่วย/สินค้า/UoM (ค่าใช้จ่าย = 1 รายการ 1 จำนวนเงิน ไม่มีปริมาณ×ราคา)
- **ตัดสิน:** WARN ไม่ใช่ BLOCK — เป็น domain adaptation ที่สมเหตุผล (VAT engine/totals order ยังตรง B2 v2) · **carry-over OQ ให้ PM/BA เคาะ** ว่ายอมรับ grid โดเมนนี้ · task-accepted จากรอบก่อน ไม่แก้รอบนี้

---

## NOT-CHECKED (ระบุชัด ไม่นับผ่านเงียบ)
- **Golden Compare (Pass R 3.6):** ไม่มี `TASTE_LOG.md` ในโฟลเดอร์งาน + archetype เป็น expense (ไม่มี golden expense reference ตรงตัว) → เทียบเชิงโครงกับ SO-reference ทำได้บางส่วน (list/wizard/view/pdf/sign block ครบตาม Pattern Q) · density/ordering ผ่านสายตาใน render shots — **ไม่ block** (โครงตรง archetype)
- อื่น ๆ ตรวจครบตาม Pass 0–4 + D + G + R

---

## สรุปเวลาแก้
- **BLOCK: 0** → ไม่มีงานแก้บังคับ · gate ผ่าน
- **WARN: 1** (UX-01 carry-over OQ) → ~0 (รอ PM/BA เคาะ ไม่ใช่งาน dev รอบนี้)
- ทั้ง 3 touchpoint (PM/BA 2026-09-10) render-verified ✅ · ไป step 4 (coverage รอบ 2 ตาม C3.2 ต้อง re-run) + step 5 (e2e) ต่อได้
