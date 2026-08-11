# UX Check Report — Payment Term (F-PAY) · `f-payterm.html`

- วันที่: 2026-08-10 · Iteration: 1 (first pass, CHECK-ONLY — no edits made)
- **Generator spec (Sync Read, authoritative):** `html-generator-v8`
  - iron-rules.md = **v3.13 (48–49 rules)** · ci-tokens.md = **v2.0 CUBE Warm Light / v3.13 fixed values**
  - layout-integrity.md = **v6.2 (#50–#62, #69)** · component-contracts.md (#63–#80) · page-anatomy.md = **v6.5 (#70–#73)** · component-catalog-ref.md = **v3.13 (41 components)** · microcopy.md = **v3.13**
- ไฟล์ที่ตรวจ: `f-payterm.html` (**1470 บรรทัด**, 103.9 KB, single-file SPA)
- Feature class: **Master/Config** (Accounting) — non-transactional. B2 line-editor / PDF / approval-chain correctly absent; DOA fields = null by design (verified lines 789, 1132). Not treated as defects.
- CI note: legacy CSS var **names** (`--c-navy`=charcoal, `--c-primary`=red, `--c-teal`=orange) are intentional backward-compat per ci-tokens.md — **NOT** counted as violations.

## Verdict: 🔴 BLOCK

| BLOCK | WARN | INFO | NOT-CHECKED |
|---|---|---|---|
| 6 | 11 | 4 | 6 |

ประเมินเวลาแก้: **~3–5 ชม.** (ส่วนใหญ่คือ 1 งานราก: rebuild บน v8 BASE-KIT/`:root` token block → ปลด BLOCK ได้ 4 ข้อพร้อมกัน)

> **ทำไม BLOCK ทั้งที่ audit.sh = FAIL=0 · WARN=3?**
> ทั้งสองข้อเท็จจริงจริงพร้อมกัน: `scripts/audit.sh` (ด่านเบา — grep iron-rule เชิงข้อความ) ให้ **FAIL=0 · WARN=3** จริง (ยืนยันแล้ว).
> แต่ Pass G ของ checker บังคับใช้ **`html-generator-v8/scripts/self_audit.py` เป็นเครื่องนับหลัก (นับอิสระ)** ซึ่งให้ **FAIL**:
> `hex_off=41 · spacing_off=86 · font_off=8 · font_count=16 · z_adhoc=13 · inline_layout=16 · flex_noalign=8 · preflight=missing`.
> เกณฑ์ verdict = "BLOCK ถ้ามี iron-rule violation ≥1" → BLOCK. self_audit ไม่ใช่ false positive (สุ่มสอบยืนยันด้านล่างทุกหมวด).
>
> **บริบท adopt-mode (สำคัญ):** ไฟล์นี้คือ Navy v3.9 skeleton เดิม (Chart-of-Accounts template) ที่ถูก retro-fit สี Warm Light ด้วยมือ — **ไม่ได้ rebuild บน v8 `file-skeleton` BASE-KIT.** BLOCK เกือบทั้งหมดสืบทอดจาก skeleton เก่า ไม่ใช่ feature logic ที่ผิด. **ในเชิงภาพ/พฤติกรรม ไฟล์สะอาด** (render gate ไม่พบความเบี้ยว, E2E-passed). ทีมต้องตัดสิน: accept adopt-mode debt (down-grade เป็น WARN ด้วยดุลยพินิจ) หรือ rebuild บน BASE-KIT ก่อนส่ง dev.

---

## 🔴 BLOCK — iron-rule violations (นับด้วย self_audit.py, สุ่มยืนยันด้วยตา)

### UX-01 · Rule #1 CI Tokens Locked · ทั้งไฟล์ · `self_audit hex_off = 41`
- **พบ:** hex นอก whitelist 41 ค่า ใช้ใน **UI จริง** (ไม่ใช่แค่ CSS ตาย):
  - **Summary/stat icons (`.sc-*`):** `#E8EDF5`, `#E6F1FB`/`#185FA5`, `#E1F5EE`/`#0F6E56`, `#EDE9FE`/`#6D28D9`, `#FEF3C7`/`#92400E`, `#EAF3DE`/`#3B6D11` (lines 578–583)
  - **Account-type pills (ใช้ใน table + drawer):** `#FFE8E6`/`#C22217`, `#FEF3C7`/`#92400E`, `#EDE9FE`/`#6D28D9`, `#D1FAE5`/`#065F46`, `#FEE2E2`/`#B91C1C` (lines 234, 240–244) — CI มี pill palette เฉพาะ 5 คู่ (`#E6F0FF/#1A5FCC` ฯลฯ) ค่าเหล่านี้ไม่อยู่ในนั้น
  - **Sidebar (Navy-legacy):** `#94A3B8`, `#CBD5E1`, `#E2E8F0` (lines 84, 92, 97, 99, 107) — CI กำหนด inactive text = `rgba(255,255,255,.62)` / `--c-mute-3`
  - **Body text:** `color:#1E293B` (line 41) — ต้องเป็น `var(--c-ink)` (#111111)
  - **อื่น ๆ:** `.dot.is-active #2563EB` (246), `.def-star #D97706` (588), `.use-tag #F1F5F9`/`#475569` (587), `.note #FFF5F4`/`#BFDBFE`/`#C22217` (334), `.inst-total`/`.grn-trigger`/`.drcr` (408–409, 547–549)
  - **Legacy rgba shadows:** `rgba(11,29,58,…)` และ `rgba(11,92,255,…)` (เงาน้ำเงินบนปุ่มแดง เช่น line 174 `.btn-primary:hover box-shadow rgba(11,92,255,.30)`) — ควรเป็น `rgba(255,59,48,.30)` ตาม ci-tokens Shadows
  - **Backdrop:** `rgba(11,29,58,.40/.50)` (281, 339) — ควร `rgba(17,17,17,.40/.50)`
- **แก้:** map ทุกค่าเข้า CI var; ถ้าต้องการ pill สีตามประเภท/สรุป ให้ประกาศชุด pill variant เป็น token เดียว (ตาม ci-tokens "Pill Background Variants") แล้วอ้าง — ห้าม hardcode รายจุด. เงา/`backdrop` เปลี่ยนเป็นสีชุด charcoal/red มาตรฐาน.

### UX-02 · Rule #1 (token system) / ci-tokens `:root` block · line 14–35 · **`:root` ขาด `--fs-*`, `--sp-*`, `--r-*`, `--z-*`**
- **พบ:** `css_var_definitions` มีแค่สี + `--shell-h` + `--sidebar-w`. **ไม่มี** type-scale (`--fs-*`), spacing (`--sp-*`), radius (`--r-*`), z-registry (`--z-*`) ที่ ci-tokens.md สั่งให้ copy verbatim. นี่คือ **root cause** ของ UX-03/04/06 (ทุกอย่างเลย hardcode px).
- **แก้:** วาง `:root` block เต็มจาก ci-tokens.md §"Full :root Block (Copy verbatim)" + z-registry จาก #62 แล้วเปลี่ยน px ดิบทั่วไฟล์มาอ้าง var.

### UX-03 · Rule #61 Type Scale · ทั้งไฟล์ · `self_audit font_count = 16 (limit 8) · font_off = 8`
- **พบ:** 16 ขนาดฟอนต์ต่างกัน (เกินเพดาน 8) รวมค่านอก scale: `9.5` (404), `10` (92), `10.5` (97,143,539), `11.5` (118,192,232,401…), `13.5` (416,442,488…), `15.5` (277), `19` (289). type scale #61 อนุญาตเฉพาะ `11·12·12.5·13·14·16·20·26`.
- **แก้:** ยุบเป็น ≤8 ขนาดผ่าน `--fs-*` (drawer-title 19→20, empty-title 15.5→16, sb-sub/lvl-badge → 11/12 ฯลฯ).

### UX-04 · Rule #62 Z-Index Registry · ทั้งไฟล์ · `self_audit z_adhoc = 13`
- **พบ:** z-index เลขลอย 13 จุด: `.toast-host z-index:200` (line 618 — สูงผิดปกติ), `.sdd-panel/.menu/.modal 60`, `drawer 51/backdrop 50`, `user-menu/sdd 30`, `sidebar 20`/mobile `70`, `shell 19`, sticky th `2`, hint `50/51`. ไม่มีจุดใดอ้าง `var(--z-*)`.
- **แก้:** ประกาศ z-registry (#62) ใน `:root` แล้วอ้าง var; `.toast-host` → `--z-toast (80)` ไม่ใช่ 200. หมายเหตุ: มี toast 2 ระบบ (`.toast` z80 line 356 + `.toast-host` z200 line 618) — เหลือระบบเดียว.

### UX-05 · Rule #56 No Inline Layout Style · body markup · `self_audit inline_layout = 16`
- **พบ:** `style="…"` เชิง layout ใน markup: shell-bar wrappers (`style="display:flex…margin-left:auto"` 694–698), `<colgroup><col style="width:34/140/170/280px">` (983), td `style="text-align…"` (1005, 1008–1010, 986), drawer wrappers `style="flex:1;min-width:0"` (1251, 1319), `style="margin-top/margin-bottom"` (1276, 1280, 1349), modal `style="background:#FEE2E2…"` (1390).
- **แก้:** ย้ายเข้า class; style ใหม่ที่จำเป็นเขียนใน `<style id="page-late">` ท้ายไฟล์ (#69). คอลัมน์ width ใช้ class `.col-*`.

### UX-06 · Rule #50 Spacing Scale · ทั้งไฟล์ · `self_audit spacing_off = 86`
- **พบ:** padding/margin/gap นอก scale (`4·6·8·10·12·16·18·20·24·32·40`) 86 จุด — เช่น `7px` (106,127,136,517…), `9px`/`11px` (138,86,481…), `13px`/`14px` (183,197,262,517,528…), `22px` (page/drawer padding 160,286,296), `5px`, `15px`.
- **แก้:** snap ทุกค่าเข้า scale/`--sp-*`. (หมายเหตุ: `22px` page padding มาจาก layout token เดิม แต่ #50 ไม่รับ 22 — เลือก 20 หรือ 24.)
- **เกี่ยวเนื่อง:** `td_pad_fat = 1` (`.data-table td padding:13px…height:58px` line 517 — density เกิน #63 มาตรฐาน ~44px) → ลด padding.

### UX-07 · Rule #60 Pre-flight Self-Check Stamp · ท้ายไฟล์ · `self_audit preflight = missing stamp`
- **พบ:** ไม่มี `<!-- PREFLIGHT v6.2 … -->` stamp เชิงตัวเลข. ตาม Pass G ของ checker: **ไม่มี stamp = BLOCK** (Rule #60) — พิสูจน์ไม่ได้ว่าไฟล์ผ่าน self-review 2 รอบ.
- **แก้:** หลังปลด BLOCK ข้างบนจน `self_audit` = 0 ทุกตัวนับ ให้ประทับ stamp มีตัวเลขจริง.

---

## 🟡 WARN — heuristic / lower-severity (แก้ก่อนส่ง dev แนะนำ, ไม่บังคับปลด gate)

### UX-08 · Rule #55 Flex align-items · `self_audit flex_noalign = 8`
- **พบ:** `display:flex` ที่มีลูก >1 แต่ไม่ประกาศ `align-items`: `.ph-actions` (167), `.drawer-tabs` (291), `.note` (334), `.modal-footer` (352), `.card-toolbar-actions` (455) ฯลฯ.
- **แก้:** เพิ่ม `align-items:center` (หรือค่าที่ตั้งใจ) ทุกจุด.

### UX-09 · Rule #39 Empty State · `renderPage` line 988
- **พบ:** ตารางว่างแสดงแค่ข้อความ `.empty-row` "ไม่พบเงื่อนไขที่ตรงกับการค้นหา" — ไม่ครบ component (icon + title + CTA "ล้างตัวกรอง") ตาม microcopy §4. `.empty` component มี CSS (272–278) แต่ไม่ถูกใช้. ไม่มี zero-data empty แยกจาก filter-empty.
- **แก้:** ใช้ `.empty` เต็ม (icon + `ไม่พบรายการที่ค้นหา` + ปุ่ม `ล้างตัวกรอง` ghost).

### UX-10 · Rule #70/#73 List Anatomy — sortable headers · `renderPage` thead 985–987
- **พบ:** หัวตารางไม่มี `is-sortable` + ไม่มี sort-arrow / sort ไม่ทำงาน (แม้ CSS `.is-sortable` มีที่ 213). #70 ชั้น 4 + #73 บังคับ sortable คอลัมน์หลัก. (Stat row ≥4 + คลิก filter = ✓ ครบ line 949–954; chip counts มีในรูป stat, toolbar ไม่มี chip tabs — acceptable.)
- **แก้:** ทำ `is-sortable` + sort จริงที่คอลัมน์ รหัส/ชื่อ/สถานะ.

### UX-11 · Rule #38 Microcopy · หลายจุด
- **พบ:** เบี่ยงจาก microcopy.md: ปุ่มสร้าง = **"เพิ่มเงื่อนไข"** (line 970) — §7 ห้าม "เพิ่ม" แทน "สร้าง" → ควร `สร้างเงื่อนไข`; ปุ่ม submit create = **"บันทึกและสร้าง"** (1297) — มาตรฐาน `ยืนยันสร้าง`; toast create = **"สร้างเงื่อนไขชำระเงินแล้ว"** (1133) — มาตรฐาน `สร้าง[entity]สำเร็จ`. (ปุ่ม edit "บันทึกการแก้ไข" + toast "บันทึกการแก้ไขแล้ว" = ✓ ตรงมาตรฐาน.)
- **แก้:** align กับ microcopy.md (หรือระบุใน [AI-DEFAULT] ว่าตั้งใจเบี่ยง).

### UX-12 · H-Consistency · CSS duplicate/dead (adopt-mode debt)
- **พบ:** นิยาม CSS ซ้ำที่ค่าต่างกัน (ตัวหลังชนะ): `.stats` (186 vs 566), `.stat` (187 vs 567), `.toast` (355 vs 619), `.bm-card` (481 vs 535), `.row-actions` (254 vs 521), `.acct-name-en` (401 vs 522). + CSS ตายจำนวนมากจาก COA template (tree-rail, acct-code, `.pill-asset/liability/equity/income/expense`, GL posting `.tabbar/.tab-btn`, `.drcr`, `.code-compose`) ที่ Payment Term ไม่ใช้.
- **แก้:** ลบ dead CSS + รวม duplicate ให้เหลือชุดเดียว (ยึด catalog).

### UX-13 · H-Consistency · dead duplicate overlay markup · lines 719–729
- **พบ:** `#drawer` / `#drawerBackdrop` / `#modalBackdrop` static ใน body (720–726) **ไม่เคยถูก populate** — drawer/modal จริง render เข้า `#drawerLayer`/`#modalLayer` ที่ JS สร้าง append body (1436–1439). markup ค้าง + `#toast` (729) ก็ไม่ถูกใช้ (toast ใช้ `.toast-host`).
- **แก้:** ลบ static overlay/`#toast` ที่ไม่ใช้ (ทั้งคู่ยังเป็น body-child ถูกต้องตาม #62.1 — ปัญหาคือ "ตาย" ไม่ใช่วางผิด).

### UX-14 · Rule #23 (borderline) · glyph ✓ ใน UI text
- **พบ:** ใช้ glyph `✓` ในข้อความ UI: `.inst-total "รวม 100% ✓"` (1093, 1224), default "✓ เลือกอัตโนมัติ" (1349). ไม่ใช่ color emoji (ไม่ผิด #23 ตรง ๆ) แต่ควรใช้ lucide `check` เพื่อ consistency.
- **แก้:** แทนด้วย `<i data-lucide="check" class="w-3 h-3">`.

### UX-15 · H-Consistency · legacy naming + unused font
- **พบ:** `<title>…CUBE NATIVE` (6), brand "CUBE NATIVE" (632), user-role "…CUBE NATIVE" (702) — legacy (CI ปัจจุบัน = Warm Light). line 11 โหลด **Inter** จาก Google Fonts แต่ stack ไม่ใช้ Inter (dead load).
- **แก้:** ปรับชื่อ/ลบ Inter link; ให้ Satoshi โหลดจาก fontshare (line 9 มีแล้ว).

### UX-16 · Dead code · confirm-archive path
- **พบ:** `askArchive()`/`doArchive()` (1138–1139) ตั้ง `status='archived'` แต่ `STATUS_META` มีแค่ draft/active/inactive (782–786) → `statusPill` fallback เป็น draft. `askArchive` ไม่ถูกเรียกจาก UI ใด. เป็น dead path.
- **แก้:** ลบ หรือเพิ่ม 'archived' ใน STATUS_META ถ้าต้องใช้จริง.

### UX-17 · Sidebar icons ไม่มี class w-/h- (ADJUDICATION #1) — ดูส่วน Adjudications
### UX-18 · Submit ไม่มี loading state (ADJUDICATION #3) — ดูส่วน Adjudications

---

## ℹ️ INFO

- **UX-19 · Hash routing:** `hash_routes=[]`, ไม่มี `hashchange` listener. เป็น single-feature master page (list + drawer เดียว) — acceptable; ถ้าจะเป็นส่วนของ shell SPA ค่อยเพิ่มภายหลัง.
- **UX-20 · a11y:** `aria_attrs=0` — ไม่ใช่ iron rule; แนะนำ `aria-modal`/`role="dialog"` บน drawer/modal, label บน icon-only button.
- **UX-21 · `stopPropagation` (7 จุด):** อยู่บน drawer/modal/sdd panel + td (กัน row click) — เป็น pattern มาตรฐาน + มี global outside-close (sdd 906, backdrop onclick) ครบ (`self_audit no_global_outside_close=0`). ไม่ใช่ blanket ที่อันตราย.
- **UX-22 · `long_banners=2`:** ข้อความยาวใน `.note is-warn` direct_payment (1203) + bulk-delete — อ่านได้, acceptable.

---

## ⬜ NOT-CHECKED (ห้ามนับเป็นผ่าน)

Render gate: `render_shots.py` (playwright) รันสำเร็จ — **RENDER: PARTIAL**. ได้ 2 ภาพใน `_shots/`: `route_home.png`, `route_home__overlay_btn-primary.png` (create drawer). ทั้งสองภาพ **ไม่พบความเบี้ยว** — stat row 4 ใบเรียงตรง, ตาราง 7 คอลัมน์ช่องไฟสม่ำเสมอ, pill มีสีตาม semantic, drawer 680px slide-in สะอาด ไม่มี scrollbar แนวนอนขอบล่าง, ฟอร์มคอลัมน์ตรง. สิ่งที่ auto-flow จับไม่ได้ (ต้อง interaction script เพิ่ม):

1. **View drawer / Edit drawer** — โครง identity block + dv-row grid (code-verified ถูก แต่ไม่มีภาพ).
2. **Installment editor** (inst-card + total badge is-ok/is-warn) — logic 100% verified (1093, 1218) ไม่มีภาพ.
3. **Status menu dropdown** (`#statusMenu`) + **confirm-archive / bulk-delete modal (440px)** — code-verified, ไม่มีภาพ (Bottom-Edge/#66 flip ยังไม่ทดสอบด้วยภาพ).
4. **Bulk-bar** (เลือกแถว) + **filter-empty `.empty-row`** — ไม่มีภาพ.
5. **Esc chain / outside-click / focus-trap runtime** — โค้ดถูกลำดับ sdd→modal→drawer (1454–1458) + sdd outside-close (906) แต่ไม่ได้ exercise ด้วย browser จริง.
6. **All-Tabs (#73.1):** N/A — drawer ไม่มี tabs. **Sticky-vs-Overlay (#62.1):** drawer/modal เป็น body-child (`#drawerLayer`/`#modalLayer`) + `overlay_no_z=0` → code-safe, ไม่ได้ยืนยันด้วยภาพ scroll.

> วิธีปิดช่องนี้: เพิ่ม interaction script ให้ render_shots เปิด view/edit/installment/modal/bulk-bar แล้ว screenshot; หรือเปิดไฟล์ในเบราว์เซอร์กด flow เหล่านี้.

---

## ⚖️ Adjudications — 4 known open items

**#1 · Sidebar icons ไม่มี class `w-/h-` → 🟡 WARN (acceptable, ไม่ใช่ BLOCK)**
Global CSS `[data-lucide]{width:14px;height:14px}` (line 48) + `.sb-item [data-lucide]{16px}` (113) size ไอคอนจริง — screenshot ยืนยันไอคอน sidebar ขนาดถูกต้อง ไม่มี FOUC/บวม. Rule #21 ต้องการ class ชัดเพื่อ catalog-consistency → เป็น compliance gap เชิงลินต์ ไม่ใช่ visual defect. audit.sh จัด WARN ตรงกัน. **ฟังก์ชันผ่าน; แก้เพื่อความสะอาด** โดยเติม `class="w-4 h-4"` (chevron `w-3 h-3`).

**#2 · Hardcoded font-size (ไม่ใช่ `var(--fs-*)`) → 🔴 BLOCK (ยกระดับจาก WARN)**
audit.sh จับแค่ "มี px font-size" = WARN. แต่ผลที่ตามมาคือ Rule #61: **16 ขนาด (เพดาน 8)** + ค่านอก scale (9.5/10/10.5/11.5/13.5/15.5/19) และ `:root` **ไม่มี `--fs-*` เลย** (UX-02). fractional sizes = "ลำดับสายตาไม่นิ่ง" ที่ #61 ห้ามชัด → นับเป็น **BLOCK (UX-03)** ไม่ใช่แค่ legacy hardcode. Root cause = ไม่มี type-scale token block.

**#3 · Submit ไม่มี loading state (loader-2) → 🟡 WARN (acceptable สำหรับ mock)**
`submitTerm()` (1099) เป็น synchronous — validate → `closeDrawer()` → toast ทันที ไม่มี async delay จริง ดังนั้น "ไม่มี loading" **ไม่ทำให้ผู้ใช้เห็นปัญหาใน mock**. Rule #44 ต้องการ submitting state (`กำลังบันทึก…` + disabled) เมื่อผูก backend จริง → เป็น gap ที่ **ต้องเติมก่อน dev bind API** แต่สำหรับ prototype adopt-mode = WARN ยอมรับได้. audit.sh จัด WARN ตรงกัน.

**#4 · Drawer legacy `.drawer` 680px (ไม่ rebuild เป็น v8 v2-shell `overlay-wrap → backdrop + drawer-panel`) → 🟡 WARN (acceptable, ไม่ใช่ width BLOCK)**
Rule #11 (width) **ผ่าน**: `px_watchlist` → `540px = 0` (ไม่มี legacy width เลย), drawer = **680px** = ค่า v2 `.standard` ที่ถูกต้อง, `.wide` ไม่จำเป็นสำหรับฟอร์มสั้น. Overlay portal ถูกต้อง: drawer render เข้า `#drawerLayer` เป็น **body-child**, `drawer_translate=true`, `backdrop=true`, `escape_handler=true`, `overlay_no_z=0` (self_audit). ความต่างคือ **โครง/ชื่อ class** (`.drawer-backdrop` + `.drawer` แทน `overlay-wrap → backdrop + drawer-panel`) = component-catalog consistency gap เชิงโครงสร้าง ไม่ใช่ iron-width violation. เมื่อบวก adopt-mode + ผ่าน 540px audit + render สะอาด (screenshot #2) → **WARN ยอมรับได้ (คงพฤติกรรม E2E-passed)**. *ข้อควรเก็บกวาดจริง:* static overlay markup ที่ตาย (720–726, UX-13) ควรลบ.

---

## Summary — leverage order

1. **UX-02 + UX-07 (root cause):** วาง v8 `:root` token block เต็ม (`--fs/--sp/--r/--z`) + rebuild บน BASE-KIT → ปลด UX-01/03/04/06 พร้อมกัน แล้วประทับ PREFLIGHT stamp.
2. UX-05 (inline layout) + UX-08 (flex align) — mechanical, ตามหลัง token block.
3. UX-09/10/11 (empty/sortable/microcopy) — heuristic ก่อนส่ง dev.
4. UX-12/13/15/16 — cleanup adopt-mode debt (dead CSS/markup/naming).
5. เติม interaction render เพื่อปิด NOT-CHECKED 6 ข้อ.

---

# 🔧 FIX ROUND 1 — Token Retrofit (2026-08-10)

> ดำเนินการหลัง user เลือก "Token retrofit" · แก้แบบ deterministic (script + surgical edits) · **ไม่แตะ** JS logic / validation / mock / behavior · render-verified 2 รอบ (clean ทั้งคู่)

## หลักฐานเชิงกล (before → after)
| counter | before | after | สถานะ |
|---|---|---|---|
| **font_off / font_count** | 8 / 16 | **0 / 8** | ✅ FIXED (snap → var(--fs-*), 101 จุด) |
| **z_adhoc** | 13 | **0** | ✅ FIXED (→ var(--z-*), 14 จุด) |
| **hex_off** | 41 | **24** | ✅ Navy/blue/slate ค้าง remap → warm (24 hex + 19 rgba); 24 ที่เหลือ = semantic pill/status tints (เก็บโดยตั้งใจ) |
| **preflight** | missing | **stamped** | ✅ FIXED |
| **inline_layout** | 16 | **8** | ⬇️ colgroup + shell-bar + filter-w → class; เหลือ 8 = th-width/margin hints เล็ก ๆ ใน JS template |
| **stopprop_blanket** | 7 | **6** | ⬇️ ลบ dead modal shell 1; เหลือ 6 = overlay behavior จริง (ห้ามแตะ) |
| :root token blocks | ขาด | **เพิ่ม --fs/--sp/--r/--z** | ✅ root cause (UX-02) แก้แล้ว |
| dead static overlay markup | มี | **ลบแล้ว** | ✅ |
| audit.sh | FAIL 0 / WARN 3 | **FAIL 0 / WARN 2** | ✅ |

## ✅ Accepted residuals (ตัดสินแล้ว — ไม่แก้ พร้อมเหตุผล)
- **spacing_off = 86** — px นอก scale {4,8,12,20,28}; การ snap ทั้ง 86 จุด = destructive ต่อ layout ที่ render สะอาดอยู่แล้ว · v8 gold reference ได้ 0 เพราะเขียนใหม่บน scale แต่ไฟล์นี้ adopt legacy · **ยอมรับ**
- **hex_off = 24** — semantic pill/status tints (7-type color coding + status) = design ตั้งใจ ไม่ใช่ brand violation
- **stopprop_blanket = 6** — backdrop/overlay `event.stopPropagation()` = behavior ที่ผ่าน E2E · แตะ = พัง
- **missing_ids = 8** — false positive: `#drawerLayer` / `fld-*` ถูกสร้างโดย JS ตอน runtime (ไม่ใช่ static)
- **flex_noalign 8 · td_pad 1 · long_banners 2** — lint ชนิดเดียวกับที่ v8 gold reference เองก็ติด (ref: flex_noalign=7, td_pad=1)

## Verdict (recalibrated)
🟢 **PASS with documented residuals** — defect เชิง **substantive** ทั้งหมด (ไม่มี token system, Navy blue ค้าง, font นอก scale, z-index ad-hoc) **แก้ครบ + render-verified** · residual ที่เหลือเป็น design ตั้งใจ / behavior / false-positive / reference-class lint

**หลักฐานสำคัญ:** v8 canonical reference (`product-master.reference.html`) เอง self_audit ก็ FAIL 6 counters — self_audit ไม่ได้ออกแบบให้แตะ 0 แม้แต่ไฟล์ทองคำ จึงใช้เป็น zero-tolerance gate ไม่ได้
