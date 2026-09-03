# UI Brief (AS-BUILT) — F-HR-RECRUIT (F127) · สรรหา / Recruit

> **สกัดจาก HTML 1:1 (extraction-based · Iron Rule R1)** — ทุกบรรทัดในไฟล์นี้ trace กลับหา selector / function / literal string ใน `สรรหา.html` ได้
> ใช้คู่กับ **HTML (source of truth)** + **FRD Pack** ให้ dev สร้างระบบจริงตรง prototype โดยไม่ต้องแกะโค้ดเอง
> ข้อเสนอที่เกิน AS-BUILT อยู่ **§13 เท่านั้น**

---

## §0 · Document Control + Pairing

| field | value |
|---|---|
| Feature | F-HR-RECRUIT (F127) · สรรหา / Recruit |
| Source HTML (SoT) | `outputs/F-HR-RECRUIT/สรรหา.html` · `<title>` = "สรรหา (Recruit) · CUBE NATIVE" · footer `PREFLIGHT v6.4` (date 2026-09-02) · sidebar footer "Prototype · v1.0.0" |
| Archetype | **master + kanban** (ไม่ใช่ Pattern Q เอกสาร — ไม่มี PDF/เลขรัน) · BASE-KIT v6.4 · vanilla-JS single-file SPA · hash routes |
| FRD Pack paired | `FRD_F-HR-RECRUIT_Pack/` — 01_UI (P-xx), 02_API (F127-API-xx), 05_RULES (BR/EC/VR), 00_OVERVIEW (FN) |
| Declaration briefs (reference) | `DOA_BRIEF_F-HR-RECRUIT.md` (2 สาย: req + offer · ไม่มีวงเงิน) · `NTF_BRIEF_F-HR-RECRUIT.md` (4 business events) · `CSQ_BRIEF_F-HR-RECRUIT.md` |
| Drift status | ดู §11 — พบ drift เชิง prototype-scope (mock ยังไม่ครบทุก state/endpoint) · ไม่มี business drift ที่บล็อก |
| Personas | 3 ตัว (Iron Rule #105 demo-strip): recruiter (unmask · ไม่อนุมัติ) · manager (mask · อนุมัติได้) · viewer (mask · read-only) |
| **Helper scripts** | ⚠️ install นี้มีเฉพาะ `SKILL.md` — `scripts/extract_anchors.py`, `templates/ui-brief.template.md`, `references/extraction-checklist.md` และ `ui-brief-check.py --verify` **ไม่มีในการติดตั้งนี้** → ทำ extraction ด้วยการ **อ่าน HTML เต็มไฟล์** (2,871 บรรทัด) · Verification Gate (§ท้ายไฟล์) รันเป็น **checklist แบบ manual** |

---

## §1 · Design Tokens AS-BUILT

### 1.1 CSS Variables (`:root` — สกัดครบชุด, บรรทัด 24–67)

| กลุ่ม | token → ค่า |
|---|---|
| Brand | `--c-navy #111111` · `--c-navy-2 #111111` · `--c-primary #FF3B30` · `--c-primary-hover #E62E24` · `--c-teal #FF9A1F` · `--c-teal-light #FFB763` |
| Ink / mute | `--c-ink #111111` · `--c-mute #54565C` · `--c-mute-2 #73757B` · `--c-mute-3 #9A9CA2` |
| Lines | `--c-line #DEDAD4` · `--c-line-2 #E9E5E0` · `--c-line-3 #F1EEEA` |
| Surface | `--c-bg-off #FAF8F5` |
| Semantic | `--c-success #1F9D55` · `--c-warning #E8870F` · `--c-danger #E62E24` |
| Shell | `--sidebar-w 232px` · `--shell-h 52px` |
| Type scale | `--fs-h1 22` · `--fs-h2 17` · `--fs-h3 15` · `--fs-body 14` · `--fs-sub 13` · `--fs-meta 12` · `--fs-cap 11` · `--fs-kpi 28` (px) |
| Spacing | `--sp-xs 4` · `--sp-sm 8` · `--sp-md 12` · `--sp-lg 20` · `--sp-xl 28` (px) |
| Radius | `--r-xs 4` · `--r-sm 6` · `--r-md 8` · `--r-lg 12` · `--r-full 999` (px) |

- **Fonts:** body `'Satoshi','Noto Sans Thai',system-ui,sans-serif` · หัวเรื่องไทย (`.ph-title`,`.stat-value`,`.empty-title`,`.modal-title`,`.drawer-title`) = `'Noto Sans Thai',sans-serif`. โหลดจาก Google Fonts + Fontshare (CDN).
- **Scrollbar** (Iron Rule #49): 5px, thumb `rgba(17,17,17,.14)`; บนพื้นเข้ม (`.sidebar`,`.slide`) = `rgba(255,255,255,.28)`.
- **Layout stability:** `html{scrollbar-gutter:stable}` · `body.is-overlay-open{overflow:hidden}` (scroll lock) · `body{min-width:768px}`.

### 1.2 Z-INDEX MAP ⭐ (เรียงสูง→ต่ำ · บรรทัด 44–53 + จุดใช้จริง)

| token | ค่า | ใช้กับ (selector) |
|---|---|---|
| `--z-toast` | **90** | `.toast` (#toast) — สูงสุด เห็นเหนือทุกอย่าง |
| `--z-portal` | **60** | `.menu-fixed` (portal menu → #overlay-root) · **`.modal-backdrop` (บรรทัด 1111)** |
| `--z-drawer` | **55** | `.drawer` (#drawer) |
| `--z-backdrop` | **50** | `.drawer-backdrop` · `.ss-list` (search-select dropdown) |
| `--z-dropdown` | **40** | `.user-menu` · `.info-tip::after` (tooltip) · `.demo-strip` |
| `--z-sticky` | **30** | `.shell-bar` · `.table-wrap thead th` / `.table-scroll.is-sticky thead th` · `.wizard-footer` |
| `--z-shell` | **20** | `.sidebar` |

> ⭐ **AS-BUILT ที่ต้องคัดลอกให้ถูก:** `.modal-backdrop` ใช้ `z-index:var(--z-portal)` = **60** (ไม่ใช่ backdrop=50) — **จงใจ** เพื่อให้ modal อยู่เหนือ drawer(55) และให้ combobox ที่ portal ออกมาใน modal โผล่เหนือ modal ได้ตาม DOM order (comment ในโค้ด: "ห้ามตั้ง > portal ไม่งั้น dropdown ใน modal จะจม"). **ไม่ใช่บั๊ก** — เป็นค่าที่ระบบต้องคง.

---

## §2 · Route Map

Hash-based · refresh-safe · `window.addEventListener('hashchange', render)` (บรรทัด 2016, late-binding).

| route (hash) | derived `RC.tab` | render fn | หน้า (FRD) |
|---|---|---|---|
| `#/recruit/req` | `req` | `renderReqTab()` | P-01 ตำแหน่งที่เปิด |
| `#/recruit/pool` | `pool` | `renderPoolTab()` | P-02 คลังผู้สมัคร |
| `#/recruit/board` | `board` | `renderBoardTab()` | P-03 บอร์ดสรรหา |
| `#/recruit/report` | `report` | `renderReportTab()` | P-04 รายงาน |

- **Nav helper:** `go(route)` → `navigate(route)` → `location.hash = '#/' + route` (บรรทัด 1667–1669, 2282).
- **Derive logic** (`render()` บรรทัด 2301–2303): `RC.tab = rt.indexOf('recruit/')===0 ? rt.split('/')[1] : 'req'` · whitelist `['req','pool','board','report']` · **fallback `req`**.
- **Default:** `getRoute()` คืน `'home'` เมื่อ hash ว่าง/`#`/`#/` (บรรทัด 1664) → แต่ render บังคับ tab เป็น `req` เสมอ → เปิดไฟล์สด ๆ ลงที่แท็บ "ตำแหน่งที่เปิด".
- Drawer/Modal **ไม่ผูก route** (ไม่มี deep-link) — state อยู่ใน `state.drawer` / `state.modal` + `RC.dctx` / `RC.mctx` เท่านั้น. Refresh ขณะเปิด overlay = overlay หาย, กลับหน้า list.

---

## §3 · Layout Shell

| region | selector | ค่า AS-BUILT |
|---|---|---|
| Sidebar | `.sidebar` (#sidebar) | fixed ซ้าย · width `--sidebar-w` (232px) · พื้น `#111111` · `z-index:var(--z-shell)` (20) |
| — brand | `.sb-brand` / `.sb-logo` / `.sb-name` "CUBE NATIVE" / `.sb-sub` "ทรัพยากรบุคคล" | โลโก้ gradient primary→teal |
| — module | `.sb-module[data-module="hr"][data-expanded]` header `บุคคล & สรรหา` (`toggleModule()`) | collapsible, header **non-navigable** (Iron Rule #27) |
| — features | `.sb-item[data-feature]` | `recruit` (active, `go('recruit/req')`) + 3 context stub: `onboard`,`employee`,`hr-config` (`ctxStub()` → toast "นอก scope รอบนี้") |
| — footer | `.sb-footer` `.pulse-dot` "Prototype · v1.0.0" | |
| Main | `.main` | `margin-left:var(--sidebar-w)` |
| Shell bar | `.shell-bar` | sticky top · height `--shell-h` (52px) · `z-index:var(--z-sticky)` (30) |
| — breadcrumb | `.breadcrumb` | `บุคคล & สรรหา › สรรหา` (`.breadcrumb-current`) |
| — notif | `.icon-btn` + `.notif-dot` | onclick toast "ศูนย์แจ้งเตือน (ENG-NOTIFY) — เชื่อมจริงตอน dev" |
| — user chip | `.user-chip` (#uc-name/#uc-role/#uc-av) `toggleUserMenu()` | sync ตาม persona (`syncPersonaChip()`) |
| — user menu | `.user-menu` (#userMenu) `z-index:var(--z-dropdown)` (40) | โปรไฟล์ของฉัน · ตั้งค่า · **ออกจากระบบ** (is-danger) — decorative (ไม่มี handler) |
| Content host | `.content` (#page-content) | render โดย `renderPage()` |
| **Demo strip** | `.demo-strip` (#demoStrip) `z-index:var(--z-dropdown)` | Iron #105 prototype scaffolding · persona seg 3 ปุ่ม `setPersona('recruiter'\|'manager'\|'viewer')` — **prototype เท่านั้น, prod ผูก role master** |

- **Responsive** (`@media max-width:1180px`, บรรทัด 358): sidebar off-canvas (`.sidebar.open` + `.nav-toggle`), `.main{margin-left:0}`, drawer widths หด.

---

## §4 · Page Anatomy (ต่อหน้า)

โครงร่วมทุกแท็บ (`renderPage()` บรรทัด 2315): `.ph` (page header: title + sub + `.ph-actions`) → `.tabs` (4 แท็บ) → body ต่อแท็บ.

**Tab bar** (`.tabs` / `.tab`): `ตำแหน่งที่เปิด`(clipboard-list, ct=จำนวน req) · `คลังผู้สมัคร`(users, ct=จำนวน cand) · `บอร์ดสรรหา`(columns-3, ct=จำนวน in-pipeline) · `รายงาน`(bar-chart-3, ct=null). แต่ละแท็บ `go('recruit/<id>')`.

**Primary action (ต่อแท็บ · ซ่อนจาก viewer):**
- req → `เปิดอัตราใหม่` (plus) `openReqCreate()`
- pool → `เพิ่มผู้สมัคร` (user-plus) `openCandCreate()`
- report → `Export CSV` (download) stub toast

### P-01 · ตำแหน่งที่เปิด — `renderReqTab()` (บรรทัด 2339)
- **My-Approval hook** (`.note.is-info`, เฉพาะ persona=manager + มี req status `pending`): "งานรออนุมัติของฉัน · N รายการ" (trace DOA_BRIEF §5 approvalHook).
- **Filter bar** (`.filter-bar`): search (`RC.f.req.q`, placeholder `ค้นหาตำแหน่ง / เลขที่ / แผนก`) · status `.select` (ทุกสถานะ + REQ_STATUS labels) · `ล้างตัวกรอง` (`RC.f.req={q:'',status:'all'}`). ทุกตัว → `renderPageOnly()`.
- **Table** (`.table` ใน `.card.page-fill`): คอลัมน์ เลขที่/ตำแหน่ง · แผนก · ระดับ(band) · อัตรา(`filled/count`, col-num) · ผู้จัดการสายงาน · Manpower (`.num` หรือ chip amber "ไม่มีแผน") · สถานะ (`reqStatusPill`). Row `.is-clickable` → `openReqView(id)`.
- **Empty:** `emptyStateHTML({title:'ไม่พบอัตราที่เปิด',...actionLabel:'ล้างตัวกรอง'})`.

### P-02 · คลังผู้สมัคร — `renderPoolTab()` (บรรทัด 2378)
- Filter: search (placeholder `ค้นหาชื่อ / รหัส / อีเมล`) · stage `.select` (ทุกระยะ + STAGES + TERMINAL) · ล้างตัวกรอง.
- Table: ผู้สมัคร (`.user-cell` avatar+ชื่อ+รหัส, chip "เคยสมัคร" ถ้า dup) · ตำแหน่งที่สมัคร · **ช่องทางติดต่อ** (`contactCell()` — state-driven mask) · ระยะ (`stagePill`) · ความยินยอม (`consentChip`) · คะแนน (col-num). Row → `openCandView(id)`.
- **Empty:** "ไม่พบผู้สมัคร" + CTA "เพิ่มผู้สมัคร".

### P-03 · บอร์ดสรรหา (kanban · FN-06) — `renderBoardTab()` (บรรทัด 2426)
- `.kanban` 5 คอลัมน์ = STAGES (`.kb-col` head: dot สี + ชื่อ + `.kb-count`). การ์ด `kbCard()`:
  - `.kc-top` (avatar+ชื่อ+ตำแหน่ง) · `.kc-meta` (consentChip + chip dup + score) · `.kc-move` 2 ปุ่ม.
  - ปุ่ม **`←`** (`candMoveStage(id,-1)`, `canBack = idx>0 && !viewer`) · **`ถัดไป`** (`candMoveStage(id,1)`, `canFwd = idx<last && consent.ok && !viewer`).
  - คอลัมน์สุดท้าย (hired) → แสดง "✓ รับเข้าทำงานแล้ว" (ไม่มีปุ่ม forward).
  - คอลัมน์ว่าง → `.kb-empty` "— ว่าง —".
- **Terminal note** (`.note.is-info` ล่างบอร์ด): "นอกไปป์ไลน์ · N รายการ" ไล่ชื่อ + label (rejected/withdrawn/talent_pool).

### P-04 · รายงาน (funnel · FN-15) — `renderReportTab()` (บรรทัด 2454)
- Filter `.select` "กรองตามอัตรา" (`RC.f.report.req`: ทุกอัตรา + reqs) → `renderPageOnly()`.
- **Stat cards** (`.stats`): ผู้สมัครทั้งหมด · กำลังสัมภาษณ์ · ข้อเสนอ · รับเข้าทำงาน · **Time-to-hire เฉลี่ย = "23 วัน" (mock hardcode**, ดู §10).
- **Funnel** (`.funnel` bars): 5 STAGES cumulative reached · แสดง "N คน" ต่อขั้น.
- Note สรุปผล: รับเข้าทำงาน / ไม่ผ่าน+Talent Pool / ถอนตัว.

### D-01 · ลิ้นชักผู้สมัคร (4 tabs) — `candViewDrawer()` (บรรทัด 2640)
Header: avatar + ชื่อ + `stagePill` + chip "ส่งเข้า onboarding แล้ว" (ถ้า onboardSent) · action `ไม่ผ่าน/ถอนตัว` (เมื่อ ไม่ viewer + ไม่ terminal + ไม่ hired).
Tabs (`setCandTab` whitelist `detail/assess/offer/history`, fallback detail):
- **detail** (`candDetail`): consent banner (info/danger + ปุ่ม `บันทึกความยินยอม` `candSetConsent`) · dup note · KV ข้อมูล (mask ตาม role · chip "RESTRICTED · ปิดบังตามบทบาท" เมื่อ mask) · retention `retentionLabel()`.
- **assess** (`candAssess`): gate consent (danger ถ้า !consent) · list สัมภาษณ์ + scorecard (`.score-pick` 1–5 `pickScore`/`saveScore`) · ปุ่ม `นัดสัมภาษณ์` (`openInterviewModal`).
- **offer** (`candOffer`): ถ้ามี offer → KV + band scale + timeline อนุมัติ + acts ตาม status · ถ้ายังไม่มี → ฟอร์มสร้าง (grade/วันเริ่ม/เงินเดือน + band resolve + เหตุผลนอกช่วง) `submitOffer`. Gate consent.
- **history** (`historySection`): "ประวัติ (append-only)" timeline.

### D-02 · ลิ้นชักอัตรา — `reqViewDrawer()` (view) / `reqFormDrawer()` (create/edit)
View: header + `.secwrap` ข้อมูลอัตรา (KV) + `approvalSection()` (DOA timeline) + "ผู้สมัครในอัตรานี้" (bm-card linked) + `historySection()`. Footer meta "อัปเดตล่าสุด …" + lock icon ถ้า approved. Acts ตาม status (ดู §8).

---

## §5 · Component Inventory (anchor + states · Iron Rule R4)

| component | anchor (selector / fn) | states |
|---|---|---|
| Button | `.btn` + `.btn-primary/secondary/ghost/danger/link/sm` · `.btn-eq/.btn-truncate` | default · hover · `:disabled/.is-disabled` (opacity .55) · **busy** = `loader-2 .spin` + disabled (submitReq/submitCand เมื่อ `RC.busy`) |
| Table row | `.table tbody tr.is-clickable` | hover (`bg-off`) · `.is-selected` (มี CSS, **ไม่ได้ใช้ใน feature นี้**) |
| Status pill (req) | `reqStatusPill()` → `.pill .pill-*` | ดู §8.1 |
| Stage pill | `stagePill()` — inline `style="background:${color}1f;color:${color}"` (in-pipeline) หรือ `.pill.pill-danger/pill-muted` (terminal) | ดู §8.3 |
| Consent chip | `consentChip()` `.chip-soft.is-consent/.is-noconsent` | ยินยอมแล้ว (เขียว) / รอความยินยอม (แดง) |
| Dup chip | `.chip-soft.is-dup` "เคยสมัคร"/"ไม่มีแผน" | amber |
| Masked cell | `.masked` + lock icon | ดู §8.4 |
| Search-select | `searchSelectHTML(key)` + `initSearchSelect(key,cfg)` (Iron #34) · `.search-select`/`.ss-list`/`.ss-opt` | closed · open (list) · typing (highlight `<mark>`, `is-active` hi) · selected (`.ss-clear` โผล่ / `.ss-caret` ซ่อน) · empty (`ss-empty` "ไม่พบ…") · keyboard ArrowUp/Down/Enter/Esc |
| Field | `.field` + `.field-label .req` + `.field-error` | default · `.is-invalid` (border danger + error visible) ผ่าน `markInvalidFields()` / `validateField()` · focus (ring primary) |
| Score picker | `.score-pick button` `pickScore()` | off · `.on` (fill warning) เมื่อ n≤ที่เลือก |
| Consent toggle (form) | `.bm-card` + `.cb.is-checked` (candFormDrawer) | on/off toggle (`RC.draft.consent`) |
| Upload zone | `.upload-zone` (candFormDrawer) | empty ("คลิกเพื่อแนบไฟล์ (mock)") · filled (`.file-pill` ชื่อไฟล์) — **mock** สร้างชื่อไฟล์เอง |
| Band card | `.band-card` `.band-scale`/`.band-seg.is-mid` | read-only (ต่ำสุด/กลาง/สูงสุด) |
| Empty state | `emptyStateHTML(cfg)` `.empty` | icon+title+desc+(action) |
| Toast | `showToast(msg,variant,durationMs=2800)` `.toast.is-*` | success/info/warning/error · auto-dismiss เท่านั้น |
| Timeline | `.timeline` `.tl-item` `.tl-dot.is-success/.is-warning` | ใช้ใน approvalSection + historySection |
| Funnel | `.funnel-row` `.funnel-fill` | width % ตาม reached |
| KPI stat | `.stat` `.stat-value` | static |

---

## §6 · Overlay Registry + Dismiss Rules (Iron Rule R5)

| overlay | selector / เปิดด้วย | ขนาด | z-index | dismiss rules |
|---|---|---|---|---|
| **Drawer** | `#drawer` + `#drawerBackdrop` · `openDrawer()`/`rcOpen()` | 920px (wide) · `.standard`=680 · max 96vw | drawer 55 / backdrop 50 | Esc (ถ้าไม่มี modal เปิด) · **คลิก backdrop** (`onclick="closeDrawer()"`) · ปุ่ม X (`.top-icon-btn`/`.icon-btn`) · ปุ่ม "ปิด"/"ยกเลิก" footer. → `closeDrawer()` + `lockScroll(false)` + `releaseFocus` + clear `RC.dctx` (หลัง 300ms) |
| **Modal** | `#modalBackdrop` + `.modal` · `openModal()`/`rcOpenModal()` | 440px · max 92vw / 90vh | **backdrop 60 (portal)** · modal เอง centered | Esc (มาก่อน drawer ใน chain) · **คลิก backdrop** (`onclick="closeModal()"`; `.modal` มี `stopPropagation`) · ปุ่ม "ยกเลิก". → `closeModal()` · **ปลด scroll lock เฉพาะเมื่อไม่มี drawer เหลือ** (บรรทัด 1713) · clear `RC.mctx` (หลัง 220ms) |
| **Toast** | `#toast` · `showToast()` | max 380px มุมล่างขวา | 90 | **auto-dismiss** (`durationMs`, default 2800ms) — **ปิดเองไม่ได้** (ไม่มีปุ่ม X · R5: "ห้ามปิด" แบบ manual) |
| **User menu** | `#userMenu` · `toggleUserMenu()` | 240px | 40 | คลิกนอก `.user-chip`/`.user-menu` (document click listener บรรทัด 2285) |
| **Search-select list** | `.ss-list` · `ssOpen()` | absolute, max-h 280px | 50 | คลิกนอก wrap (document click บรรทัด 1876) · Esc (`stopPropagation` — ปิดแค่เมนู) · เลือก option |
| **Portal menu** | `.menu-fixed` → `#overlay-root` · `portalMenu()` | ตาม trigger | 60 | BASE-KIT util (ไม่ถูกเรียกใน feature logic นี้ — มีไว้เป็น infra) |

**Modal ย่อย 4 ชนิด** (`renderModal()` บรรทัด 2804 · type ใน `RC.mctx`):
1. `confirm` (`openConfirm`) — ปิดอัตรา / รับเข้าทำงาน · ปุ่มยืนยัน (danger/primary) `rcConfirmYes()`.
2. `reason` (`openReasonModal`) — ไม่ผ่าน/ถอนตัว, reject · textarea เหตุผล **บังคับ** (`rcReasonYes()` block ถ้าว่าง) + select ผลลัพธ์ (ถ้า withKind).
3. `interview` (`openInterviewModal`) — วันที่/เวลา/ผู้สัมภาษณ์(combobox iv_emp)/สถานที่ · `saveInterview()`.
4. `doa` (`openDoaModal`) — DOA slot picker · `.slot` ต่อขั้น + combobox `slot_N` · `submitDoa()` บังคับเลือกครบทุกขั้น.

---

## §7 · Interaction Spec

- **Esc chain** (window keydown, บรรทัด 1735): `if modal.open → closeModal()` `else if drawer.open → closeDrawer()` — **modal มาก่อน drawer เสมอ**. ภายใน combobox: `ssOnKey` Escape → `e.stopPropagation()` + ปิดเฉพาะ list (กัน Esc ทะลุไปปิด drawer · Iron #94 comment บรรทัด 1872).
- **Click-outside:** user menu, search-select list — document-level listener (ปิดตัวเองเมื่อคลิกนอก).
- **Scroll lock:** `lockScroll(on)` toggle `body.is-overlay-open`. Modal ปิดแล้ว **คงล็อกไว้ถ้า drawer ยังเปิด** (นับชั้น overlay).
- **Focus management:** `trapFocus(box)` — Tab วนใน overlay + โฟกัสตัวแรก (RAF) · `releaseFocus` คืนโฟกัสเดิม. เรียกตอน open drawer/modal.
- **Render preservation** (Iron #29): `preserveRenderState()`/`restoreRenderState()` ครอบ `render()` — เก็บ scroll (drawer-body/modal-body/page) + focus + selection range ของ input ที่กำลังพิมพ์ (match ด้วย placeholder+type+name).
- **`renderPageOnly()`** (บรรทัด 2483): re-render เฉพาะ `#page-content` (filter/search) — ไม่ rebuild drawer/modal, ไม่กระตุก (Rule #103C).
- **Positioning:** drawer `position:fixed` ขวา, transform slide-in 280ms · modal centered fixed, scale 0.96→1 · toast fixed มุมล่างขวา translateY.
- **Boot:** รอ `domReady && lucideReady` ก่อน first render (บรรทัด 2023) · safety net 5s ถ้า Lucide timeout · Lucide multi-CDN fallback (unpkg→jsdelivr→cdnjs, pinned 0.469.0).

---

## §8 · State-Driven UI Matrix

### 8.1 Requisition status (`REQ_STATUS` บรรทัด 2179) → footer acts (`reqViewDrawer` บรรทัด 2557)

| status | label (verbatim) | pill | footer actions (ไม่ใช่ viewer) |
|---|---|---|---|
| `draft` | ร่าง | pill-muted | `แก้ไข` (openReqEdit) · `ส่งอนุมัติเปิด` (reqSubmitApproval→DOA modal) |
| `pending` | รออนุมัติเปิด | pill-warning | (เฉพาะ `canApprove`) `ไม่อนุมัติ` (reqReject) · `อนุมัติ` (reqApprove) |
| `approved` | อนุมัติแล้ว · รอประกาศ | pill-info | `ประกาศรับ` (reqAnnounce) · `ปิดอัตรา` (reqClose) |
| `open` | เปิดรับ | pill-success | `ปิดอัตรา` (reqClose) |
| `closed` | ปิดแล้ว | pill-muted | — |

### 8.2 Offer status (`OFFER_STATUS` บรรทัด 2186) → acts (`candOffer` บรรทัด 2694)

| status | label | pill | acts (ไม่ใช่ viewer) |
|---|---|---|---|
| `draft` | ร่างข้อเสนอ | pill-muted | — |
| `pending` | รออนุมัติ | pill-warning | (canApprove) `ไม่อนุมัติ` (offerReject) · `อนุมัติข้อเสนอ` (offerApprove) |
| `approved` | อนุมัติแล้ว · พร้อมส่ง | pill-info | `ส่งข้อเสนอให้ผู้สมัคร` (offerSend) |
| `sent` | ส่งข้อเสนอแล้ว | pill-info | `ผู้สมัครปฏิเสธ` (offerResult declined) · `ผู้สมัครตอบรับ` (offerResult accepted) |
| `accepted` | ตอบรับ | pill-success | (ถ้า !onboardSent) `รับเข้าทำงาน → ส่ง On/Offboard` (candHireHandoff) |
| `declined` | ปฏิเสธข้อเสนอ | pill-danger | — (candidate.stage → withdrawn) |

### 8.3 Candidate stage (`STAGES` + `TERMINAL`)

| id | label | สี / pill | เลื่อนได้ |
|---|---|---|---|
| `applied` | สมัครใหม่ | #9A9CA2 | fwd (ถ้า consent) |
| `screening` | คัดกรอง | #1A5FCC | fwd/back |
| `interview` | สัมภาษณ์ | #E8870F | fwd/back |
| `offer` | ข้อเสนอ | #FF9A1F | ต้องมี offer object |
| `hired` | รับเข้าทำงาน | #157A41 | terminal (ผ่าน hire route เท่านั้น) |
| `rejected` | ไม่ผ่าน | pill-danger | terminal |
| `withdrawn` | ถอนตัว | pill-muted | terminal |
| `talent_pool` | เก็บ Talent Pool | pill-muted | terminal |

**Board move guards** (`candMoveStage` บรรทัด 2749): dir>0 + `!consent.ok` → toast block · เข้า offer + ไม่มี offer → route ไป offer tab · เข้า hired → ต้อง `offer.status==='accepted'` แล้ววิ่งผ่าน `candHireHandoff()` เท่านั้น (FIX-01) · viewer → `viewerRO()` block.

### 8.4 PII masking (`contactCell` บรรทัด 2418 · `PERSONAS.unmask`)

| เงื่อนไข | ผลบนจอ |
|---|---|
| `!consent.ok` | `.masked` lock "ต้องได้รับความยินยอมก่อน" (ไม่แสดงเลย) |
| consent + persona `unmask=true` (recruiter) | email/phone เต็ม |
| consent + `unmask=false` (manager/viewer) | `maskEmail` = `x•••@domain` · `maskPhone` = `•••-•••-1234` + lock icon · chip "RESTRICTED · ปิดบังตามบทบาท" |

### 8.5 Persona capability (`PERSONAS` บรรทัด 2129)

| persona | name/av | unmask | canApprove | ผล |
|---|---|---|---|---|
| recruiter | มณีรัตน์ ก. / มร | ✅ | ✗ | สร้าง/แก้/เลื่อน/offer/hire ได้ · เห็น PII เต็ม |
| manager | ธีรภัทร ว. / ธว | ✗ | ✅ | อนุมัติ req/offer ได้ · PII masked · เห็น My-Approval hook |
| viewer | ผู้ชมทั่วไป / ผช | ✗ | ✗ | **read-only** — ปุ่มสร้างซ่อน + `viewerRO()` guard ต้นทุก mutation (toast "สิทธิ์อ่านอย่างเดียว") |

---

## §9 · Microcopy (verbatim · Iron Rule R2)

### 9.1 Toasts (`showToast` ทุก call — คัดตรงตัว)

| ข้อความ | variant | จุดเรียก |
|---|---|---|
| ศูนย์แจ้งเตือน (ENG-NOTIFY) — เชื่อมจริงตอน dev | info | ปุ่ม bell |
| `<ชื่อ feature>` — feature ข้างเคียงของ module (นอก scope รอบนี้) | warning | ctxStub (sidebar stub) |
| สิทธิ์อ่านอย่างเดียว | warning | viewerRO() |
| กรุณาเลือกผู้จัดการสายงาน | warning | submitReq (ไม่มี HM) |
| กรุณากรอกข้อมูลที่ไฮไลต์ให้ครบ | warning | submitReq / submitCand |
| บันทึกการแก้ไขแล้ว | success | submitReq (edit) |
| บันทึกร่างแล้ว | success | submitReq (draft) |
| สร้างอัตราแล้ว (ร่าง) — ส่งอนุมัติเปิดได้จากหน้ารายละเอียด | success | submitReq (create) |
| สร้างผู้สมัครสำเร็จ | success | submitCand |
| กรุณาให้คะแนนก่อน | warning | saveScore |
| บันทึกผลประเมินแล้ว | success | saveScore |
| กรุณากรอกวันเริ่มงานและเงินเดือน | warning | submitOffer |
| เงินนอกช่วง band — กรุณาระบุเหตุผล | warning | submitOffer |
| ยังไม่ได้รับความยินยอม PDPA — เลื่อนสถานะไม่ได้ | warning | candMoveStage |
| ไปขั้น "ข้อเสนอ" ให้สร้างข้อเสนอในลิ้นชักผู้สมัคร | info | candMoveStage |
| ต้องให้ผู้สมัครตอบรับข้อเสนอก่อน | info | candMoveStage / (hired guard) |
| บันทึกความยินยอมแล้ว | success | candSetConsent |
| บันทึกแล้ว | success | candTerminate |
| ส่งเข้า onboarding แล้ว | success | candHireHandoff |
| อนุมัติแล้ว | success | reqApprove / offerApprove |
| ไม่อนุมัติแล้ว | info | reqReject / offerReject |
| ประกาศรับแล้ว | success | reqAnnounce |
| ปิดอัตราแล้ว | success | reqClose |
| ส่งข้อเสนอแล้ว | success | offerSend |
| บันทึกผลข้อเสนอแล้ว | success | offerResult |
| ส่งออกรายงาน (CSV) — ต่อ dev | info | Export CSV stub |
| กรุณาระบุเหตุผล | warning | rcReasonYes |
| กรุณากรอกข้อมูลให้ครบถ้วน | warning | saveInterview |
| นัดสัมภาษณ์แล้ว | success | saveInterview |
| กรุณาเลือกผู้อนุมัติให้ครบทุกขั้น | warning | submitDoa |
| ส่งอนุมัติแล้ว | success | submitDoa |

### 9.2 NTF toasts (`ntf(msg)` → info · ต้อง wire ENG-NOTIFY จริง)

| template | จุดเรียก | NTF event (NTF_BRIEF) |
|---|---|---|
| แจ้งเตือน: `<ชื่อ>` → `<stage>` | candMoveStage | `recruit_stage_changed` |
| แจ้งเตือน: อัปเดตผลผู้สมัคร `<ชื่อ>` | candTerminate | (—, ไม่อยู่ใน 4 events หลัก) |
| แจ้งเตือน: ส่ง `<ชื่อ>` เข้ากระบวนการ onboarding | candHireHandoff | handoff event (ไม่ใช่ NTF) |
| แจ้งเตือน: อนุมัติเปิดอัตรา `<code>` | reqApprove | (DOA engine — ห้ามประกาศซ้ำ) |
| แจ้งเตือน: ประกาศรับ `<position>` | reqAnnounce | (—) |
| แจ้งเตือน: อนุมัติข้อเสนอ `<ชื่อ>` | offerApprove | (DOA engine) |
| แจ้งเตือน: ส่งข้อเสนอให้ `<ชื่อ>` | offerSend | `recruit_offer_sent` |
| แจ้งเตือน: ผลข้อเสนอ `<ชื่อ>` — ตอบรับ/ปฏิเสธ | offerResult | `recruit_offer_result` |
| แจ้งเตือน: นัดสัมภาษณ์ `<ชื่อ>` | saveInterview | `recruit_interview_scheduled` |
| แจ้งเตือน: ส่งอนุมัติเปิดอัตรา `<code>` / ส่งอนุมัติข้อเสนอ `<ชื่อ>` | submitDoa | (DOA engine) |

### 9.3 Placeholders / labels / banners (verbatim)

- **Placeholders:** `ค้นหาตำแหน่ง / เลขที่ / แผนก` · `ค้นหาชื่อ / รหัส / อีเมล` · `เช่น Senior Frontend Developer` · `เช่น เทคโนโลยีสารสนเทศ` · `ค้นหาพนักงาน...` · `เช่น MP-2569-IT-07 (เว้นว่างได้)` · `หน้าที่หลัก / คุณสมบัติ` · `ชื่อจริง นามสกุล` · `name@example.com` · `08x-xxx-xxxx` · `ค้นหาอัตราที่เปิด...` · `เช่น 62000` · `เหตุผลที่เสนอเกิน/ต่ำกว่าช่วง band` · `ความเห็น` · `ระบุเหตุผล` · `เช่น ห้องประชุม 3 · Google Meet` · `เลือกผู้อนุมัติ...`
- **PDPA banner (candForm):** "ข้อมูลผู้สมัครเป็นข้อมูลชั้นความลับ (RESTRICTED) · เก็บได้เมื่อได้รับความยินยอม PDPA และเก็บตามระยะเวลาที่ประกาศในนโยบายความเป็นส่วนตัว (ตั้งค่าที่ Policy Center)"
- **Consent-missing warn:** "ยังไม่ได้รับความยินยอม — บันทึกเข้าคลังได้ แต่จะ **ดำเนินการต่อ (คัดกรอง / สัมภาษณ์ / ข้อเสนอ) ไม่ได้** จนกว่าจะได้รับความยินยอม"
- **retention (FIX-03):** `retentionLabel()` = "ตามนโยบาย Policy Center (รอกำหนดระยะ)" — **ห้ามระบุ "ไม่มีวันหมดอายุ"**.
- **Manpower warn:** "ยังไม่ได้ระบุแผนอัตรากำลัง (Manpower) — เปิดอัตราได้ แต่โปรดตรวจสอบกับแผนกำลังคน (hook · ไม่บังคับ)"
- **Hire confirm body:** "ระบบจะยิง event ส่งผู้สมัครเข้ากระบวนการ onboarding (soft-linkage) และตั้งสถานะ "ส่งเข้า onboarding แล้ว" — ไม่สร้าง employee และไม่เชื่อมจริงในรอบนี้"
- **Close req confirm:** "อัตราจะถูกปิด (รับครบ/ยกเลิก) และเก็บถาวรแบบ soft archive — ประวัติยังอยู่ครบ"
- **DOA modal:** "สายอนุมัติมาจากระบบ DOA กลาง (F-DLG-001) — เลือก "คน" ในแต่ละ slot ที่ระบบ resolve มาให้"
- **Field-error inline:** `กรุณากรอกตำแหน่ง` · `กรุณากรอกแผนก` · `อย่างน้อย 1` · `กรุณากรอกชื่อ` · `กรุณากรอกอีเมล` · `กรุณากรอกเบอร์โทร`

---

## §10 · Data Binding & BACKEND Anchors

ทุก mock ในไฟล์ = จุดที่ dev ต้อง plug API (ดู 02_API):

| mock (บรรทัด) | ผูก API / engine | หมายเหตุ |
|---|---|---|
| `EMPLOYEES` (2136) · `empOpts()` | `EXT-EMP` GET `/api/v1/employees?status=active&q=` | picker ผู้สัมภาษณ์/HM/approver · เก็บ **snapshot** (BR-09) |
| `BANDS` (2150) · `bandResolve(grade,date)` | `EXT-BAND` GET `/api/v1/salary-structure/bands/resolve` | grade+date → band + `version_id` · **freeze** คู่ offer (BR-09) |
| `doaResolve(kind)` (2160) | `EXT-DOA` Policy Center resolve | คืน slot เปล่า (role-hiring-manager → role-hr-recruit-head) · **ไม่ hardcode คน** (VR-04) |
| `DB.reqs/cands` (2196) | F127-API-01/03/09/11 (GET) + mutations | in-memory · replace ด้วย REST |
| `audit(entity,...)` (2273) | `T_recruit_audit` append-only (FN-21/FN-93) | `history.unshift` — prod = append middleware |
| `ntf(msg)` (2275) | `ENG-NOTIFY.emit(...)` (FN-07) | ปัจจุบัน = info toast · 4 events ต้อง wire (NTF_BRIEF §1) |
| `retentionLabel()` (2290) | Policy Center PDPA retention config | display-only · **OQ-16 ยังไม่เคาะระยะ** (FIX-03) |
| Export CSV (2327) | F127-API-25 GET `/recruit/report/export` | stub toast |
| Time-to-hire "23 วัน" (2467) | F127-API-24 funnel | **hardcode mock** — dev คำนวณจริง applied_at→hired_at |
| `RC.busy` (2278) | double-submit guard | loader-2 spin (VR-02/FIX-07) |

**Base path:** `/api/v1/recruit` · ทุก mutation ต้องมี `X-Tenant-Id` + `Idempotency-Key` · state-change ใช้ `If-Match` (optimistic lock).

---

## §11 · Traceability (3 ทาง) + Drift Log

### 11.1 Brief ↔ FRD ↔ HTML

| Brief § | หน้า/action | FRD (P / API / BR / FN) | HTML anchor |
|---|---|---|---|
| §4 P-01 | list req | P-01 · API-01/03 · — | `renderReqTab()` (2339) |
| §8.1 | เปิดอัตรา | API-02 · BR-08 · FN-01 | `openReqCreate`/`submitReq` (2487/2536) |
| §8.1 | ส่งอนุมัติเปิด | API-05 · BR-01 · FN-03 | `reqSubmitApproval`→`openDoaModal('req')` (2781) |
| §8.1 | อนุมัติ/ไม่อนุมัติ req | API-06 · BR-01 · FN-04 | `reqApprove`/`reqReject` (2782/2788) |
| §8.1 | ประกาศรับ | API-07 · §5.2 · FN-06 | `reqAnnounce` (2789) |
| §8.1 | ปิดอัตรา | API-08 · BR-07 · FN-07/FN-16 | `reqClose` (2790) |
| §4 P-02 | list cand (masked) | P-02 · API-09 · BR-06 · FN-94 | `renderPoolTab`/`contactCell` (2378/2418) |
| §9.3 | เพิ่มผู้สมัคร + consent + dup | API-10/13 · BR-02/BR-10 · FN-03/05/09 | `openCandCreate`/`submitCand`/`findDuplicate` (2490/2622/2621) |
| §8.3 | เลื่อน stage (guard) | P-03 · API-14 · BR-02 · FN-06/FN-12 | `candMoveStage` (2749) |
| §6 M-04 | นัดสัมภาษณ์ + NTF | D-01 assess · API-15 · BR-09 · FN-07/FN-13 | `openInterviewModal`/`saveInterview` (2800/2827) |
| §4 D-01 assess | scorecard 1–5 | API-16 · FN-14 | `pickScore`/`saveScore` (2692/2693) |
| §4 D-01 offer | สร้าง offer (band freeze) | API-17 · BR-09 · VR-03 · FN-15 | `candOffer`/`submitOffer` (2694/2734) |
| §8.2 | offer lifecycle | API-18–21 · BR-04 · FN-16/17/18/18a | `offerApprove/Reject/Send/Result` (2792–2795) |
| §9.3 | รับเข้าทำงาน (handoff) | API-22 · BR-05 · FN-19 · **OQ-15** | `candHireHandoff` (2771) |
| §6 M-05 | ไม่ผ่าน/ถอนตัว | API-23 · BR-07 · FN-20 | `candTerminate`→reason modal (2763) |
| §4 P-04 | funnel report | P-04 · API-24/25 · FN-15 | `renderReportTab` (2454) |
| §6 M-03 | DOA slot picker | M-03 · API-05/18 · VR-04 · FN-26 | `openDoaModal`/`submitDoa` (2801/2828) · DOA_BRIEF §5 |
| §8.4 | PII mask ตาม role | BR-06 · D7 · FN-23/FN-94 | `maskEmail/maskPhone`/`PERSONAS.unmask` (2416/2129) |
| §5 history | audit append-only | BR-03/BR-07 · FN-21/FN-93 | `audit`/`historySection` (2273/2588) |
| §8.5 | viewer read-only | VR-05 · EC-06 · FN-24 | `viewerRO` (2288) — guard 15 จุด |

### 11.2 ⚠️ Drift Log (ไม่เงียบ · Iron Rule R6)

| # | ทิศทาง | รายการ | รายละเอียด | ข้อเสนอ |
|---|---|---|---|---|
| DR-01 | **FRD-only** | สถานะ req `cancelled` แยกจาก `closed` | 05_RULES §5.2 มี `cancelled` (close mode=cancelled + reason/warn · EC-08) แต่ HTML `reqClose()` ตั้ง `status='closed'` เท่านั้น (ไม่มี mode/branch cancelled, ไม่ warn "มีผู้สมัครค้าง") | dev: เพิ่ม mode filled/cancelled + guard active-candidate ตอน bind API-08 (OQ-17) |
| DR-02 | **FRD-only** | Loading / error states (skeleton, 403, 500, stale-409) | FRD §1.6 ระบุ skeleton/`ERR_*`; HTML mock in-memory ไม่มี loading skeleton หรือ error path (มีแค่ empty + validation toast) | dev bind async + skeleton + error toast/retry ตอนต่อ API จริง |
| DR-03 | **FRD-only** | Idempotency / optimistic-lock UI (409 stale) | EC-07/EC-09 · API §2.3; HTML ไม่มี concurrency handling | UI ต้องจับ 409 ERR_STALE_DATA → toast + refresh (dev) |
| DR-04 | **HTML-only** | `candTerminate` ยิง `ntf('อัปเดตผลผู้สมัคร…')` | NTF_BRIEF ไม่มี event สำหรับ terminate (มีแค่ 4: interview/stage/offer_sent/offer_result) | ยืนยันกับ BA ว่า terminate ต้องมี NTF หรือไม่ · ถ้าไม่ → เอา ntf ออกตอน wire (ปัจจุบันเป็น toast mock ไม่บล็อก) |
| DR-05 | **HTML-only** | `RC.f.pool` มีตัวเลือก `pipeline` (`fs==='pipeline'?inPipeline`) | `stageOpts` ไม่ render option "pipeline" — โค้ด filter รองรับแต่ไม่มี UI ให้เลือก | dead branch — dev ลบหรือเพิ่ม option ได้ (ไม่กระทบ business) |
| DR-06 | **HTML-only** | submitReq: ทั้ง "บันทึกร่าง" และ "ยืนยันสร้าง" ตั้ง `status:'draft'` เหมือนกัน | `asDraft?'draft':'draft'` (บรรทัด 2548) — สร้างใหม่ลง draft เสมอ ต้องไปกด "ส่งอนุมัติเปิด" ในหน้า view | ตรงตาม flow (draft → submit-approval) · dev คง 2 ปุ่มไว้ (ต่างกันที่ audit label + toast) |
| DR-07 | **note** | `FN-40` (negative test "ของที่ห้ามมี") | FN checklist ของ feature นี้ = FN-01–16 + FN-90–94 · **ไม่มี FN-40**. ของที่ "ห้ามมี" = ทางลัดข้าม offer.accepted ไป hired + สร้าง employee ตรง — บังคับโดย FIX-01 (`candMoveStage` block → route ผ่าน `candHireHandoff` เท่านั้น · ไม่สร้าง employee) | ตรวจแล้ว AS-BUILT: ไม่มีปุ่ม/ทางลัดสร้าง employee หรือ set hired ตรง ๆ ในโค้ด |

> ไม่พบ **business drift ที่บล็อก** — หน้า/route/action ใน HTML = 01_UI Layout Decision Log = BRD (ยืนยันโดย _UX_CHECK_REPORT PASS + _COVERAGE_REPORT). Drift ทั้งหมดเป็น prototype-scope (mock ยังไม่ครอบ async/error/cancelled) หรือ dead-branch เล็ก.

---

## §12 · Diff จากเวอร์ชันก่อน

— ไม่มี HTML เวอร์ชันเก่าให้ diff ในรอบนี้ (single version). FIX-01…FIX-07 ที่ฝังในคอมเมนต์ = การแก้ภายในเวอร์ชันเดียวกัน (ดู §11 DR-06/07 + §8.3 guard).

---

## §13 · 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT · ที่เดียวที่คิดเองได้ · R1)

1. **Toast ปิดเองได้:** ปัจจุบัน toast auto-dismiss เท่านั้น (ไม่มี X) — เสนอเพิ่มปุ่มปิดสำหรับ error toast ที่ผู้ใช้ควรอ่านช้า ๆ (dev-time decision).
2. **Deep-link drawer/candidate:** ผูก drawer กับ hash (`#/recruit/pool/C3`) เพื่อ refresh-safe + แชร์ลิงก์ — ตอนนี้ refresh ขณะเปิด drawer จะเด้งกลับ list.
3. **Terminate NTF:** ถ้า BA ยืนยันว่าการ "ไม่ผ่าน/ถอนตัว" ต้องแจ้งผู้สมัคร → ประกาศ event ใหม่ใน NTF_BRIEF (ปัจจุบัน DR-04 = HTML-only mock).
4. **`cancelled` แยก UI:** ทำปุ่ม "ยกเลิกอัตรา" แยกจาก "ปิด (รับครบ)" + guard active-candidate ให้ตรง EC-08/OQ-17 (ตอนนี้รวมเป็น `reqClose` เดียว).
5. **Pool filter "pipeline":** เพิ่ม option ที่ตรงกับ dead-branch (DR-05) หรือถอด branch ออกเพื่อความสะอาด.

---

## 🔍 Verification Gate (manual · FAIL=0)

> helper `ui-brief-check.py` ไม่มีในการติดตั้งนี้ → นับด้วยมือจากการอ่าน HTML เต็ม

| เช็ค | ผล |
|---|---|
| ทุก route ใน HTML มี section | **4/4** (req/pool/board/report → §2 + §4) ✅ |
| ทุก overlay มีแถวใน Overlay Registry | **6/6** (drawer·modal·toast·user-menu·ss-list·portal) + 4 modal ย่อย → §6 ✅ |
| ทุก `showToast(...)` อยู่ใน Microcopy verbatim | **31/31** (§9.1) + 10 ntf (§9.2) ✅ |
| ทุก component ใน anatomy มี selector/fn anchor | ✅ (§5 + §4 ทุกแถวมี anchor) |
| state matrix ครอบ enum ที่เจอ | REQ_STATUS 5/5 · OFFER_STATUS 6/6 · STAGES 5/5 · TERMINAL 3/3 · persona 3/3 ✅ |
| Esc chain ตรง handler จริง | ✅ (§7 — modal→drawer, combobox stopPropagation) |
| z-index map ครบทุก token ที่ประกาศ | **7/7** (§1.2, รวม modal-backdrop=portal) ✅ |
| (FRD) ทุก P-xx + action หลักมี traceability + Drift ไม่เงียบ | P-01…P-04 + D-01/D-02 + M-01…M-06 → §11.1 · Drift 7 แถว §11.2 ✅ |
| ไม่มีสเปคที่ trace ไม่ได้ (sample 10 จุด) | ตรวจ 10 จุดสุ่ม (z-index modal, retentionLabel, FIX-01 guard, mask, DOA slot, band freeze, busy loader, terminal note, My-Approval hook, Export stub) — trace ได้ทุกจุด ✅ |

**Verdict: PASS** (FAIL=0)
