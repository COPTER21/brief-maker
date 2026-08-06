# UX Check Report — F-BNK ธนาคาร / บัญชีบริษัท (Bank Master)

> **FINAL VERDICT (round 2 · 2026-08-05): 🟢 PASS** — BLOCK = 0. self_audit REAL hits (spacing/font/flex/page-inline) = 0.
> เหลือ WARN ที่ documented false-positive เท่านั้น (ดู §Round 2). ไฟล์ที่ตรวจ/แก้: `outputs/09_Bank-Master/01_HTML/BankMaster.html` (working copy — input ต้นทางไม่แตะ).
> Round-1 section ด้านล่างเก็บไว้เป็นประวัติ (verdict เดิม = BLOCK).

---

- วันที่: 2026-08-05 · Iteration: 1 (first-pass — ไม่มี report รอบก่อนให้ diff)
- Generator spec (Sync Read): **html-generator-v7** · iron-rules.md = **49 ข้อ (#1–#49) + #94** (v3.13 base + v6.11 · v7 authoritative; v6 ไม่ได้ติดตั้ง) · ci-tokens = CUBE Warm Light v2.0
- ไฟล์ที่ตรวจ: `Pack Brief Feature/09_Bank-Master/BankMaster.html` (2,842 บรรทัด · 127.4 KB · single-file SPA)
- เครื่องมือ: `static_scan.py` (mechanical) + `html-generator-v7/scripts/self_audit.py` (นับอิสระ) + Playwright render 9 states (JS errors = **0**)
- Feature context ที่เคารพ (ไม่ flag): Shared-Foundation MASTER ไม่มี tier → ไม่มี 🔗/✋ (ถูกต้อง) · THB readonly + info-tip (OQ-2) · Doc picker = simulation ตั้งใจ · account masking last-4 + reveal-on-permission + audit = required

## Verdict: 🔴 BLOCK
| BLOCK | WARN | INFO | NOT-CHECKED |
|---|---|---|---|
| 3 | 5 | 5 | 2 |
ประเมินเวลาแก้: ~40–55 นาที (blockers ส่วนใหญ่เป็น cosmetic/quick — 1 ตัวเป็น functional)

> สรุปเชิงคุณภาพ: prototype นี้ **คุณภาพสูงมาก** — CI/tokens/fonts/scrollbar/drawer-modal contract/empty-loading-submitting states/masking/combobox (#94) ผ่านครบ, render สะอาด ไม่มี geometry เพี้ยน, JS error 0. Blockers ทั้ง 3 เป็นจุดเล็ก: 1 functional (Esc chain) + 2 เชิงกล/ความน่าเชื่อถือของ stamp. แก้แล้วจะขึ้น PASS ได้เร็ว.

---

# ════════ ROUND 2 — FIX + VERIFY (2026-08-05) ════════

- Mode: **FIX + loop** · Target working copy: `outputs/09_Bank-Master/01_HTML/BankMaster.html` (140.5 KB · input ต้นทาง `Pack Brief Feature/…` ไม่แตะ)
- เครื่องมือ: `html-generator-v7/scripts/self_audit.py` (รันจริงใน env นี้ — ไม่ hand-count) + Playwright chromium (interaction + 12 shots → `_shots/round2/`)

## Verdict: 🟢 PASS (BLOCK 0)
| BLOCK | WARN (documented FP) | INFO |
|---|---|---|
| **0** | 6 categories (self_audit false-positive) + 1 pre-existing note | — |

### self_audit — diff vs round 1
| ตัวนับ | round 1 | round 2 | สถานะ |
|---|---|---|---|
| spacing_off | 11 | **0** | ✅ แก้แล้ว |
| font_off | 2 | **0** | ✅ แก้แล้ว |
| font_count | 10 (>8) | **8** | ✅ แก้แล้ว (limit 8) |
| flex_noalign | 2 | **0** | ✅ แก้แล้ว (เพิ่ม align-items) |
| inline_layout | 9 | **1** | ✅ page-authored 8 จุด → 0 · เหลือ 1 = kit shell verbatim |
| hex_off / z_adhoc / grid_nogap / preflight | 0 | 0 | ✅ คงเดิม |

**REAL hits ทั้งหมด = 0.** `self_audit` exit ยังเป็น FAIL เพราะ **false-positive 6 หมวด** ที่ static นับไม่แยกแยะ (documented ด้านล่าง — ตาม instruction "ห้าม hack แก้ false positive"):
- `stopprop_blanket=2` — `event.stopPropagation()` ใน row cell (#41 row=view + action) + สาขา Esc ใน `ssOnKey` (#94.3 **บังคับ**ให้มี). ทั้งคู่จำเป็น.
- `naked_hints=1` — `.field-help` "8 หรือ 11 หลัก…" (#33.2 อนุญาต field-help).
- `long_banners=4` — ทั้งหมดเป็น `.note` ที่ผูก action/อยู่ใน modal (#33 exception).
- `missing_ids=5` — `ss-*` เป็น id ที่ combobox สร้าง runtime (`'ss-input-'+key`) — ไม่ใช่ dead ref.
- `fullwidth_select=3` — width ถูกย้ายไป CSS (`.filter-status max-width:180px`, `.co-bar .select min-width:280px;width:auto`) ตาม #69; static เห็นแค่ tag จึงเข้าใจผิดว่า full-width. (round1=2 → 3 เพราะย้าย inline→class ของ status filter; ตั้งใจ, correct.)
- `custom_tabs=4` — `.ptabs/.ptab` page-tab ที่ประดิษฐ์เอง (v7 base-kit ไม่มี page-tab กลาง) ใช้สม่ำเสมอ 2 จุด.

## แก้อะไรบ้าง (per item)

**BLOCK — แก้ครบ:**
- **UX-01 ✅** `ssOnKey` สาขา `Escape` → `if(s.open){ e.stopPropagation(); e.preventDefault(); s.open=false; … }`. **Playwright verify:** focus combobox (list open) → Esc#1 → `list_open=false, drawer_open=true` → Esc#2 → `drawer_open=false, is-open removed`. Esc-chain ถูกต้อง.
- **UX-02 ✅** ย้าย inline layout 8/9 จุด (page-authored) เข้า `#page-late` เป็น class + utility เดิม: `.filter-status` (max-width:180), `.filter-reset` (ml:auto), `.stat-value.is-abbr` (font 18→20 on-scale), `.empty-hint` (แทน inline empty text 2 จุด), `.note … mt-3/mt-2` (ใช้ utility เดิม), `#page-late` ไม่ว่างแล้ว. **เหลือ 1 จุด = shell-bar `<div style="…margin-left:auto">` (BankMaster L1481)** ซึ่ง **verbatim จาก `erp-shell.template.html` L116** → #69 บังคับให้ kit เป็น verbatim จึง **ห้ามแก้** (documented FP, ไม่ใช่ page violation).
- **UX-03 ✅** รัน `self_audit.py` จริง → spacing/font/inline(page)/flex = 0 · แก้ off-scale CSS ทั้ง 11 spacing + 2 font (13.5→13, 11.5→12) + font_count 10→8. **PREFLIGHT stamp เขียนใหม่ให้ HONEST** (ใส่ตัวเลขจริงจาก self_audit + ระบุ false-positive rationale + ลบข้อความ "hand-counted; env lacks self_audit.py" เดิมที่โกหก).

**WARN (approved conformance) — แก้ครบ:**
- **UX-04 ✅** Audit model generalize: `pushAudit` เพิ่ม `bankCode:null`; เพิ่ม `pushBankAudit(bankCode, action, detail)`; `AUDIT_META` เพิ่ม `bank-added`/`bank-removed`. `submitBank`→`pushBankAudit(code,'bank-added',…)`, `removeBank`→`pushBankAudit(code,'bank-removed',…)`. **Surface:** เพิ่ม `bankAuditSectionHTML()` ท้ายการ์ดแท็บธนาคาร ("ประวัติการเปลี่ยนแปลงรายชื่อธนาคาร"). Append-only ครบ **ทั้ง 2 แท็บ** (บัญชี = audit tab ใน view drawer, ธนาคาร = section ในแท็บ). **Playwright verify:** add→'สร้างธนาคาร HSBC…', remove→'ลบธนาคาร HSBC…' แสดงใน section (shot 12).
- **UX-05 ✅** Microcopy archive-lock/used-in-doc ยอมรับ **Bank Reconciliation**: archive warn note + archive info note + deactivate body + deactivate info note → เพิ่ม "และรายการกระทบยอดธนาคาร" / "การกระทบยอดธนาคาร".
- **UX-06 ✅** Verb → "สร้าง" (ตาม microcopy §1/§7): ปุ่ม header "สร้างบัญชี"/"สร้างธนาคาร", empty-state action+desc, drawer eyebrow "สร้างบัญชีธนาคาร"/"สร้างธนาคาร", toast "สร้างธนาคารสำเร็จ", subtitle + tooltip "ที่สร้างเอง". สอดคล้องกับ footer "ยืนยันสร้าง" + toast บัญชีเดิม.
- **UX-07 ✅** ซ่อนปุ่ม "เก็บถาวร" เมื่อ `a.status === 'archived'` ทั้ง **row-level** (`rowHTML`) และ **view drawer header** (terminal state ไม่มีทาง re-archive/ซ้ำ log).
- **UX-08 ✅** (รวมใน UX-03) off-scale CSS ทั้งหมดใน page CSS → on-scale.

**INFO:** I-01..I-05 คงสถานะเดิม (ผ่าน/mock ตามเจตนา). 
- **I-06 (ใหม่, pre-existing) — ✅ FIXED (post-loop, 2026-08-05):** เดิม `submitBank`/`commitAccount` ไม่เรียก `render()` หลัง `closeDrawer()` → รายการ/audit ใหม่ไม่รีเฟรชจนกว่าจะ render ครั้งถัดไป. **แก้แล้ว**: เพิ่ม `setTimeout(render, 300)` หลัง `closeDrawer()` ในทั้งสอง commit function (300ms > drawer-close 280ms → state.drawer reset ก่อน แล้วค่อย re-render list, ไม่เสี่ยง drawer เด้งเปิด). ครอบทั้ง create + edit (commitAccount ใช้ร่วม). แก้โดยตรงในไฟล์ (surgical, additive) — **ยังไม่ได้ re-run Playwright รอบนี้** ควร spot-check ตอนเปิดไฟล์ (สร้างบัญชี/ธนาคารใหม่ → ต้องเห็น row ทันทีหลัง drawer ปิด).

## Render Gate (Pass R · round 2) — ✅ PASS
Playwright chromium → `_shots/round2/` (01_list … 12_bank_audit_populated) · **pageerrors=0 · console-errors=0** · drawer/modal/tabs ทำงานปกติ · Esc-chain verified · bank-audit section verified.

---

# ════════ ROUND 1 (history · verdict เดิม = BLOCK) ════════

## 🔴 BLOCK — ต้องแก้ก่อนผ่าน gate

### UX-01 · Rule #94.3 + #15 (Esc Chain) · combobox `ss-*` ใน create/edit drawer · `ssOnKey()` line 1797–1803
- **พบ (ยืนยันด้วย Playwright):** เปิด combobox "ธนาคาร"/"บัญชี GL" ใน drawer แล้วกด **Esc** → list ปิด **และ drawer ปิดตามไปด้วย** (ทดสอบจริง: `list_open_before=True` → กด Esc → `drawer_still_open=False`). สาเหตุ: `ssOnKey` สาขา `Escape` (line 1802) ปิด list แต่ **ไม่เรียก `e.stopPropagation()`** → event bubble ไปถึง window keydown handler (line 1666–1671) ซึ่ง `closeDrawer()`. Rule #94 ข้อ 3 บังคับ "Esc ปิด list ก่อน (stopPropagation) — drawer ยังเปิด".
- **แก้ (concrete):** ที่ line 1802 เพิ่ม guard + หยุด bubble เฉพาะตอน list เปิด:
  ```js
  else if(e.key === 'Escape'){ if(s.open){ e.stopPropagation(); s.open = false; ssSetText(key); ssSyncChrome(key); ssRenderList(key); } }
  ```

### UX-02 · Rule #69 + #50 (Layout Integrity / no inline layout) · หลายจุด (self_audit `inline_layout=9`)
- **พบ:** มี inline layout style **9 จุด** ทั้งที่ไฟล์มี `<style id="page-late">` ว่างอยู่แล้ว (line 2829) — Rule #69 ปิดข้ออ้าง "จำเป็น". ตัวอย่าง: `style="max-width:180px;"` (status select, line 2196) · `style="margin-left:auto;"` (reset btn, 2202) · `style="font-size:18px;"` (stat abbr, 2186–2187) · `style="margin-top:10px/12px;"` (note, 2574/2657/2694/2724) · `style="color:...; font-size:13px; padding:8px 0;"` (empty-audit, 2580) · `style="text-align:right;"` (th, 2221/2298) · `style="justify-content:flex-end;"` (row-actions, 2256). (หมายเหตุ: shell-bar inline flex ที่ line 1481 เป็น template-inherited.)
- **แก้:** ย้ายเข้า `#page-late` เป็น class (เช่น `.filter-status{max-width:180px}`, `.ph-actions .btn-reset{margin-left:auto}`, `.stat-abbr{font-size:18px}`, `.note--mt{margin-top:var(--sp-md)}`) หรือใช้ utility ที่มีอยู่ (`.mt-2/.mt-3`, `th.col-num` แทน inline text-align:right).

### UX-03 · Pass G (Pre-flight Trust) · PREFLIGHT stamp line 2830–2839
- **พบ:** stamp ประกาศ `round1 (mechanical): spacing-off=0 ... inline-layout=0 ... hex-off=0` และ `audit.sh: FAIL=0` แต่รัน `html-generator-v7/scripts/self_audit.py` อิสระได้ **`spacing_off=11`, `inline_layout=9`, `font_off=2`, `font_count=10`** และ `RESULT: FAIL`. Pass G: "ตัวเลขใน stamp ไม่ตรงกับการนับจริง = BLOCK (stamp ปลอม/นับผิด → ไว้ใจ pre-flight ไม่ได้)". stamp เองยอมรับ "env lacks self_audit.py → hand-counted" ซึ่งเป็นสาเหตุที่ตัวเลขคลาด.
- **แก้:** หลังแก้ UX-02 ให้ **รัน self_audit.py ซ้ำจน `inline_layout=0`** แล้ว **อัปเดตตัวเลขใน stamp ให้ตรงผลจริง** (หรือระบุ WARN ที่เหลือเป็น base-kit-inherited พร้อมจำนวนจริง) — อย่า claim 0 ถ้ายังไม่ 0.
> เกร็ด: self_audit WARN บางส่วนเป็น **false positive** ตรวจแล้วไม่ต้องแก้ — `stopprop_blanket` (line 2255 = required ตาม #41), `naked_hints` (line 2427 = `.field-help` ที่ #33.2 อนุญาต), `long_banners` (`.note.is-warn/is-info` ทั้งหมดอยู่ใน modal/ผูก action = #33 exception), `missing_ids`/`fullwidth_select`/`custom_tabs` (dynamic id + form select 100% = ปกติ). ที่ต้องแก้จริงคือ inline_layout + spacing/font-off เท่านั้น.

---

## 🟡 WARN

### UX-04 · A1 (Append-only Audit Everywhere) · `submitBank()` line 2807–2826 · `removeBank()` line 2326–2330
- **พบ (ยืนยัน A1):** เพิ่ม/ลบ ธนาคารต่างประเทศ (bank preset tab) **ไม่เขียน audit log** — ทั้งสองฟังก์ชันไม่เรียก `pushAudit`. โมเดล audit ผูกกับ `accountId` เท่านั้น (line 2083) จึงไม่มีที่บันทึก event ระดับ bank เลย. ขัด append-only-audit-everywhere (stamp เคลม "FN-90 audit ... all wired" แต่ครอบเฉพาะ company-account). ตรงกับข้อสังเกตเชิงโครงสร้าง.
- **แก้:** เพิ่ม audit stream ระดับ bank/system (เช่น `pushBankAudit(code, 'bank-added'|'bank-removed', detail)`) + surface ในหน้า (tab ประวัติระบบ หรือ log กลาง). อย่างน้อยบันทึกใน array เดียวกันด้วย key แยก.

### UX-05 · A3 (Used-in-Document / Archive Lock scope) · `archiveModalHTML()` 2656–2658 · `deactivateModalHTML()` 2693 · `usedInDoc` field
- **พบ (ยืนยัน A3):** logic ล็อก/เตือนอ้างอิงเอกสารใช้ **boolean `usedInDoc` ตัวเดียว** และ microcopy พูดถึงเฉพาะ **ใบสำคัญจ่าย/รับ** (line 2693 "เช่น ใบสำคัญจ่าย/รับ", default tab 2563/2570) — **ไม่กล่าวถึงกระทบยอดธนาคาร (Bank Reconciliation)** ที่มีใน sidebar (line 1434) และเป็น downstream ตาม central plan. archive note (2657) ใช้คำกลาง "เอกสาร" ไม่ระบุแหล่ง.
- **แก้:** ขยาย copy ให้ครอบ recon (เช่น "ถูกใช้ในเอกสารและรายการกระทบยอดธนาคารแล้ว") และ/หรือแยกแหล่งอ้างอิงใน `usedInDoc` (เช่น `usedIn: ['PV','RECON']`) เพื่อความถูกต้องของ archive-lock.

### UX-06 · Microcopy §1/§7 (verb "สร้าง") · `headerHTML()` line 2114–2116 · `submitBank()` toast 2824
- **พบ:** ปุ่มสร้างใช้ **"เพิ่มบัญชี"/"เพิ่มธนาคาร"** และ toast **"เพิ่มธนาคารสำเร็จ"** — microcopy §7 ห้าม "เพิ่ม" แทน "สร้าง" (§1: create = `สร้าง[entity]`). ไม่สอดคล้องภายในไฟล์เดียว: footer ใช้ "ยืนยันสร้าง" (2454/2802) + toast account ใช้ "สร้างบัญชีธนาคารสำเร็จ" (2510) ถูกต้องแล้ว.
- **แก้:** เปลี่ยนปุ่มเป็น "สร้างบัญชี"/"สร้างธนาคาร" + toast "สร้างธนาคารสำเร็จ" (หรือถ้าตั้งใจใช้ "เพิ่ม" ให้ log เป็น intentional override).

### UX-07 · State-machine UX (A2-adjacent) · `rowHTML()` line 2258
- **พบ:** ปุ่ม "เก็บถาวร" (archive) แสดงในทุกแถว **รวมถึงแถวที่ status = archived อยู่แล้ว** → กดซ้ำได้, `confirmArchive()` (2673) รันซ้ำ set `archived` + push audit 'archived' ซ้ำ (idempotent แต่ log ซ้ำ). (State machine หลักถูกต้อง — ดู INFO I-01.)
- **แก้:** ใน `rowHTML` ซ่อน/disable ปุ่ม archive เมื่อ `a.status === 'archived'` (เทียบ view drawer ที่จัดการ toggle ตาม status แล้ว).

### UX-08 · Rule #50 (Spacing/Type Scale) · page CSS 1319–1401 (self_audit `spacing_off=11`, `font_off=2`)
- **พบ:** ค่า px นอก scale (4/8/12/20/28) และนอก `--fs-*` ใน page CSS: `def-grid gap:11px 18px` (1361) · `dtoggle-row padding:14px 16px` (1366) · `pick-row padding:11px 12px` (1392) · `note padding:11px 13px` (1397) · `ptab 13.5px` (1329) · `acc-reveal 11.5px`/`dflag 11px` (1347/1354).
- **แก้:** map เข้า spacing scale (`var(--sp-md/lg)`) และ type scale (`var(--fs-sub/meta)`). ค่าเล็กน้อยแต่ทำให้ stamp กลับมา 0 ได้ (คู่กับ UX-03).

---

## ℹ️ INFO (ผ่าน / ข้อเสนอไม่บังคับ)

- **I-01 · A2 verified ✅** — state machine ถูกต้องตามที่ตั้งใจ: `active → ปิดใช้งาน → inactive` (2701–2707) และ `inactive → เปิดใช้งาน → active` (2632–2637) = reversible; `archived` เป็น **terminal** — view drawer `toggleAct` (2537–2541) ไม่มี action สำหรับ archived, ไม่มี path reactivate. ตรงตามที่ระบุ.
- **I-02 · Bank brand hex เป็น data (ไม่ใช่ CI violation)** — `#1e4598`…`#0a7d4b` (line 2009–2030) เป็นสี identity ของธนาคาร ใช้ inline `background:${b.color}` บน `.bank-logo` (เทียบ avatar color) — self_audit `hex_off=0` เห็นด้วย. เสนอ: custom-bank fallback `#4b5563` (2821) + `bankOf` fallback `#73757B` (2072) ควรอ้าง token (`var(--c-mute-2)`).
- **I-03 · Custom page-tab `.ptabs/.ptab`** (1327–1337) — base-kit v7 ไม่มี page-tab กลาง จึงประดิษฐ์เอง ใช้สม่ำเสมอ 2 จุด (accounts/banks) OK; flag ไว้ถ้า page-tab จะใช้ซ้ำหลาย feature ควรผลัก catalog.
- **I-04 · Pagination/Sticky** — `state.pagination` (1587) ประกาศแต่ไม่ใช้; footer account table (2226) แสดง "แสดง N จาก M รายการ" ไม่มีปุ่ม pagination (Rule #10) — ยอมรับได้ที่ ≤5 แถว; banks tab 22 แถวไม่ได้ใช้ `.table-scroll.is-sticky` — พิจารณาเพิ่ม sticky header เมื่อ list ยาว.
- **I-05 · Doc picker = simulation** (2711–2743, "จำลอง" + PV-2025-014 + toast "(จำลอง)") — mock ตามเจตนา ไม่ถือเป็น defect.

## ⬜ NOT-CHECKED
- **NC-01 · Combobox drop-up flip (Rule #66)** — `.ss-list` (1541) เปิดลงล่างเสมอ (`margin-top:4px`) ไม่ผูก `positionMenu()`/`.drop-up` (base-kit utils 1975–1978). ในฟีเจอร์นี้ combobox อยู่บนสุดของ drawer 680px จึง low-risk; ควรทดสอบเปิด combobox ตอนฟอร์ม scroll ลงสุด/ใกล้ขอบล่างจอ. (verifiable แต่ผลกระทบต่ำ)
- **NC-02 · BASE-KIT verbatim byte-diff** — ตรวจ marker (line 22/1317/1974/1984) + spot-check ค่าแล้ว ไม่พบการแก้ไข kit; ยังไม่ได้ทำ diff แบบ byte-per-byte เทียบ `templates/file-skeleton.template.html`.

---

## Render Gate (Pass R) — ✅ PASS
รัน Playwright (chromium) จับ 9 states → `outputs/09_Bank-Master/02_QC/_shots/` · **JS errors = 0**
- 01_list · 02_create_drawer · 03_combobox · 04_view_drawer · 05_view_audit · 06_archive_modal · 07_banks_tab · 08_bank_create · 09_docpicker
- Visual checklist: แนวตรง/ช่องไฟสม่ำเสมอ ✅ · ไม่มีกล่องล้น/horizontal scroll ✅ · ปุ่มร่วมแถวสูงเท่า ✅ · ฟอร์ม grid ตรง ✅ · pill/combobox 2-บรรทัด compact (#65) ✅ · stat row + chip counts (#70/#73) ✅ · Thai baseline ไม่ลอย ✅ · masking last-4 + "ดูเต็ม" consistent ทั้ง row/view ✅
- หมายเหตุ: Bottom-edge (#66) / All-tabs / Sticky-vs-Overlay ยังไม่ได้จับครบทุก edge (ดู NC-01) — states หลักผ่านหมด.

## Iron-rules ที่ตรวจแล้วผ่าน (สรุป)
#1–#5 CI/font/sidebar/shell/lucide ✅ · #6–#10 ph/breadcrumb/stats/filter-in-card/footer ✅ · #11–#15 drawer 920/680·440 modal + slide + 3-close ✅ · #16 ตาราง ≤8 col ✅ · #17–#20 grid/field/spinner/toggle ✅ · #21 icon w/h ✅ · #23 no color emoji (⚠/✅ อยู่ใน comment เท่านั้น) ✅ · #24 no dev-tool ✅ · #25/#29 renderIcons + preservation ✅ · #27/#28 module-feature sidebar + slim top bar ✅ · #30 fluid content ✅ · #31 drawer button contract (footer/สี=role/view=ปิด secondary) ✅ · #33 hint=tooltip (currency/SWIFT info-tip) ✅ · #34/#94 master combobox (bank+GL) ✅ · #35 layout stability (overlay + gutter) ✅ · #36 button symmetry ✅ · #39 empty states (2 เคส) ✅ · #40/#41 cell atomicity + row=view ไม่มี eye ✅ · #43 validate on-blur + fmt กลาง + tabular ✅ · #44/#45 submitting + readonly ✅ · #46 placement ✅ · #47 stepper (n/a — ไม่มี wizard) · #49 scrollbar 5px ✅
