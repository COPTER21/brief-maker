# UI Brief — F-HR-ESS · F059 · ESS Portal (พนักงานทำเอง)

> **EXTRACTION-BASED (Iron Rule R1)** — ทุกบรรทัดในบรีฟนี้ trace กลับหา selector / function / ข้อความจริงใน `ess.html` ได้
> อ้าง `Lxxxx` = เลขบรรทัดใน HTML · ข้อเสนอที่ไม่มีในจอ อยู่ท้ายไฟล์ §13 เท่านั้น
> คู่กับ: **HTML (source of truth)** + **FRD Pack** (ระบบ) + บรีฟนี้ (design intent)
> 🔴 **HARD LOCK (L2146):** ESS = DISPLAY-ONLY · no CRUD · no form/submit · no doc/running-number/PDF/DOA ของตัวเอง · "ยื่นคำขอ" = **navigate-out (deep-link) เสมอ**

---

## §0 · Document Control + Pairing

| | |
|---|---|
| Feature | F-HR-ESS · F059 · ESS Portal ("ESS ของฉัน — พนักงานทำเอง") |
| HTML source | `outputs/F-HR-ESS/ess.html` · `<title>` = "ESS ของฉัน — พนักงานทำเอง · CUBE NATIVE" (L6) · 2710 บรรทัด · BASE-KIT v6.4 |
| Archetype | **Portal (aggregate) · DISPLAY-ONLY · deep-link · self-access (SecC)** — จงใจ **NOT Pattern Q** (ไม่มี running-no / PDF / doc-wizard / mutation) · HARD LOCK L2143–2148 |
| FRD Pack | `FRD_F-HR-ESS_Pack/` (00_OVERVIEW · 01_UI · 02_API · 03_LOGIC · 04_DB · 05_RULES · 06_TESTS) — **paired** |
| BRD | `BRD_ess.md` |
| HTML เก่า (diff) | — ไม่มี (บรีฟนี้เป็น full AS-BUILT รอบแรก · §12 = N/A) |
| Gate สถานะ | PREFLIGHT v6.4 L2696: `audit.sh FAIL=0 · WARN=3` · round2 7/7 · date 2026-09-10 |
| Drift | บันทึกใน §11 — ทั้งหมดเป็น HTML-only display surface / cross-module ASSUMED / backend-contract ที่ mock ไม่จำลอง · **ไม่มี business drift ที่ block** |
| Carry OQ | **OQ-ESS-02** — deep-link routes ทั้ง 5 ยัง `[ASSUMED contract]` (ยืนยัน route จริงกับ owner ก่อน dev) |

**สถาปัตยกรรม:** Single-file vanilla-JS SPA · state-driven `render()` (L2249) · innerHTML rebuild + Render Preservation (Rule #29 · `preserveRenderState()` L1986) · **4 tabs สลับด้วย `state.tab`** (ไม่ใช่ hash route — DSP-02 keep-state L2234) · Lucide icon multi-CDN fallback (unpkg→jsdelivr→cdnjs · L14–19) · ฟอนต์ Satoshi + Noto Sans Thai (L11–12).

---

## §1 · Design Tokens AS-BUILT (`:root` L24–67)

### Palette (CUBE CI v2.0 Warm Light rebrand)
| token | ค่า | ใช้ |
|---|---|---|
| `--c-navy` / `--c-navy-2` | `#111111` | sidebar · launcher · heading |
| `--c-primary` / `--c-primary-hover` | `#FF3B30` / `#E62E24` | ปุ่มหลัก · qcard icon · ap-row hover |
| `--c-teal` / `--c-teal-light` | `#FF9A1F` / `#FFB763` | accent · quota bar · sec-head icon |
| `--c-ink` | `#111111` | ตัวอักษรหลัก |
| `--c-mute` / `--c-mute-2` / `--c-mute-3` | `#54565C` / `#73757B` / `#9A9CA2` | ตัวอักษรรอง / meta / masked |
| `--c-line` / `--c-line-2` / `--c-line-3` | `#DEDAD4` / `#E9E5E0` / `#F1EEEA` | เส้น / card border / divider |
| `--c-bg-off` | `#FAF8F5` | พื้นหลังหน้า · nrow hover |
| `--c-success` / `--c-warning` / `--c-danger` | `#1F9D55` / `#E8870F` / `#E62E24` | pill สถานะ · qc-badge · deny-code |

### Type scale (fixed · Iron Rule L54–62)
`--fs-h1:22px` · `--fs-h2:17px` · `--fs-h3:15px` · `--fs-body:14px` · `--fs-sub:13px` · `--fs-meta:12px` · `--fs-cap:11px` · `--fs-kpi:28px`
font stack (L91): `'Satoshi','Noto Sans Thai',system-ui,sans-serif` · body 14px · line-height 1.5 · ตัวเลข KPI/quota ใช้ `'Noto Sans Thai'` (L1435/1472/1480)

### Spacing / Radius (L64–66)
`--sp-xs:4px --sp-sm:8px --sp-md:12px --sp-lg:20px --sp-xl:28px` · `--r-xs:4px --r-sm:6px --r-md:8px --r-lg:12px --r-full:999px`

### Shell dims
`--sidebar-w:232px` (L42) · `--shell-h:52px` (L43) · body `min-width:768px` (L99) · `scrollbar-gutter:stable` (L74 · Rule #35 กัน jank) · scrollbar 5px (L81)

### ⭐ Z-INDEX MAP (สูง → ต่ำ · L47–53) + DSP-01 override
| token | ค่า | ใช้กับ |
|---|---:|---|
| `--z-toast` | **90** | `.toast` (สูงสุด — เห็นเหนือทุกอย่าง) |
| `--z-portal` | **60** | เมนู portal `#overlay-root` (Rule #95) · **`.modal-backdrop` ใช้ค่านี้** (ดูหมายเหตุ DSP-01) |
| `--z-drawer` | **55** | `.drawer` (ตัวลิ้นชัก/หน้าต่าง view) |
| `--z-backdrop` | **50** | `.drawer-backdrop` · `.ss-list` search list |
| `--z-dropdown` | **40** | `.user-menu` · tooltip |
| `--z-sticky` | **30** | `.shell-bar` · thead sticky |
| `--z-shell` | **20** | `.sidebar` |

> ⭐ **DSP-01 (extract L1369–1372):** BASE-KIT เดิมตั้ง `.modal-backdrop = --z-backdrop(50)` แต่ไฟล์นี้ **override เป็น `z-index: var(--z-portal)` = 60** (comment `/* 60 > drawer 55 */`) — จงใจให้ **modal (action-picker / 403) โผล่เหนือ drawer(55)** เพราะ D-02 profile drawer มีปุ่ม "ยื่นคำขอ" ที่เปิด action-picker **ทับ** drawer · **ห้ามตั้ง > --z-portal** ไม่งั้น combobox portal ใน modal จะจม
> **BUG-6 guard (late-style L2695):** `.drawer:not(.is-open){ pointer-events:none }` — กันลิ้นชักที่กำลัง slide-out 280ms ดักคลิกกลางจอ · **ห้ามลบ** (precedent F-HR-EXPENSE · uikit `assert_overlay_cleared_after_close`)

---

## §2 · Route Map (⚠️ tab = state-driven · deep-link = ASSUMED)

> **1 feature = 1 เมนู (#104):** ทั้ง feature = เมนูเดียว "ESS ของฉัน" · ภายในสลับ **4 tabs** ด้วย `state.tab` — **ไม่ใช้ hash route ต่อ tab** (ต่างจาก welfare `#/welfare/*`)

### 2.1 · Internal tabs (state-driven · ไม่มี hash)
| tab | label (segItem) | render fn | trigger | default |
|---|---|---|---|---|
| `home` | หน้าหลัก | `renderHome()` L2308 | `goTab('home')` L2237 | ✅ (fallback L2301) |
| `pay` | เงินเดือน & เวลา | `renderPay()` L2345 | `goTab('pay')` | |
| `docs` | เอกสาร & สิทธิ์ | `renderDocs()` L2402 | `goTab('docs')` | |
| `notify` | แจ้งเตือน | `renderNotify()` L2462 | `goTab('notify')` (+ bell icon L1587) | |

- `goTab(t)` L2237 = set `state.tab=t` · ถ้า drawer เปิดอยู่ → `closeDrawer()` · `render()`
- `render()` L2298–2301 = ternary ตาม `state.tab` → renderHome/Pay/Docs/Notify (fallback `renderHome`)
- `state.tab` persist ข้าม re-render (L2234 · DSP-02) · **ไม่ sync กับ URL** — refresh = กลับ `home`
- **hashchange** L2039 (base-kit late-binding `render()`) ยังผูกอยู่ แต่ feature ไม่ push hash ต่อ tab

### 2.2 · ⭐ Deep-link routes (navigate-out · **[ASSUMED contract] · OQ-ESS-02**)
`LINKS` L2225 — ปลายทาง 5 owner feature · **prod = navigate จริง · route ต้องยืนยันกับ owner ก่อน FRD**
| key | label | route [ASSUMED] | owner รับ form/submit |
|---|---|---|---|
| `leave` | การลา | `#/leave/new` | การลา |
| `ot` | ขอทำงานล่วงเวลา | `#/ot/new` | OT |
| `expense` | เบิกค่าใช้จ่าย | `#/expense/new` | Expense (F101) |
| `profile` | แก้ไขข้อมูลพนักงาน (ขออนุมัติ) | `#/profile/edit-request` | Employee Master |
| `cert` | หนังสือรับรอง | `#/cert/new` | หนังสือรับรอง |

- `deepLink(key)` L2675 = lookup `LINKS[key]` → ปิด modal/drawer ที่เปิดค้าง → `showToast('กำลังนำทางไปหน้า "'+label+'"','info',3200)` · **HTML เป็น stub** (โชว์ toast แทน navigate จริง · ไม่โชว์ route ใน toast)
- **Fallback (OQ-ESS-03 `[AI-DEFAULT]`):** route ไม่พร้อม → graceful notice, คงหน้า ESS เดิม (02_API §2.4)

---

## §3 · Layout Shell

| region | selector | หมายเหตุ |
|---|---|---|
| Sidebar | `.sidebar` L1553 (fixed · w=`--sidebar-w`232px · bg `#111111`) | โมดูล "ทรัพยากรบุคคล" > item `data-feature="ess"` `.is-active` (L1566 · onclick `goTab('home')`) |
| Sibling menus | `.sb-item.is-disabled` L1570–1572 | "การลา · เบิกค่าใช้จ่าย · เงินเดือน" = **context only** (owner features · mock · not built) · title="ฟีเจอร์เจ้าของ — ปลายทาง deep-link (ไม่ได้ทำในรอบนี้)" |
| Sidebar footer | `.sb-footer` L1576 | pulse-dot + "โหมดพนักงาน · self-service" |
| Module toggle | `toggleModule(this)` L1560 | collapse ผ่าน `data-expanded` |
| Topbar | `.shell-bar` L1580 | nav-toggle (mobile L1581) · breadcrumb "ทรัพยากรบุคคล › ESS ของฉัน" (L1582–1584) |
| Notif bell | `.icon-btn` L1587 | `onclick="goTab('notify')"` · มี `.notif-dot` (static) |
| User chip | `.user-chip` L1588 | **static** "สมชาย ใจดี" / "พนักงาน · EMP-00123" / avatar "สจ" (ไม่มี persona sync — single self persona) |
| Page host | `.content #appContent` L1594–1595 | `render()` เขียน `renderPage()` ลงตรงนี้ |

**Page header (`renderPage()` L2269):** `.ph` — title "ESS ของฉัน" + `.ph-count` "พนักงานทำเอง" (L2272–2273) + `.ph-sub` (L2274) + `.ph-actions` ปุ่ม **ยื่นคำขอ** → `openModal('actionPicker')` (L2276).
ตามด้วย: **self-banner** (L2280 · SecC) → **demo-strip** (L2285 · `.demo-only`) → **ess-tabs** seg-control 4 ปุ่ม (L2291–2296) → tab body.

- **self-banner** `.self-banner` L2280 (SecC · FIX-03 · **ไม่ใช่ demo-only** — compliance messaging): "คุณกำลังดูข้อมูลของตนเอง (**สมชาย ใจดี · EMP-00123**) — ข้อมูลส่วนตัว/เงินเดือนแสดงเฉพาะของคุณเท่านั้น"

---

## §4 · Page Anatomy (ต่อ tab)

### P-01 · หน้าหลัก / dashboard (`renderHome` L2308) — FN-01
- **launcher band** `.launcher` L2314 (bg navy): "ต้องการยื่นคำขอใช่ไหม?" + p อธิบาย + ปุ่ม primary **ยื่นคำขอ** → `openModal('actionPicker')`
- **5 KPI cards** `.qgrid` → `qcard(icon,label,value,sub,badge,onclick)` L2334 (L2319–2323):
  | card | value | onclick |
  |---|---|---|
  | สลิปล่าสุด | `baht(last.net)` = ฿38,250.00 | `openView('payslip','PS-2568-07')` |
  | โควตาลาคงเหลือ | รวม `total-used` = 38 วัน | `goTab('pay')` |
  | OT เดือนนี้ | 12 ชม. | `goTab('pay')` |
  | ใบเบิกค้าง | นับ status='รออนุมัติ' = 1 ใบ | `goTab('docs')` |
  | แจ้งเตือน | นับ unread = 2 รายการ | `goTab('notify')` · **badge** `.qc-badge` (แดง · เฉพาะ unread>0) |
- **"ทางลัดของฉัน"** `.ess-sec` L2325: chip `CH_RO` · def-grid (พนักงาน · แผนก/สาขา · ปุ่ม `btn-link` "ดูโปรไฟล์ของฉัน" → `openView('profile',EMP.id)` L2331)

### P-02 · เงินเดือน & เวลา (`renderPay` L2345) — FN-02/03/04
- **สลิปเงินเดือน** (`sec()` L2348 · chip `CH_ASSUMED+CH_RO`): table (รอบเดือน/วันที่จ่าย/ยอดสุทธิ/สถานะ/›) · row `.is-clickable` → `openView('payslip',id)` L2351 · money `baht()` · pill `status='จ่ายแล้ว'` success
- **วันลา & โควตา** L2360 (chip `CH_ASSUMED` + ปุ่ม **ยื่นลา** → `deepLink('leave')`): `.quota-grid` 3 mini bar (คงเหลือ `total-used` / total · `.q-bar` teal) + ตารางประวัติลา (ประเภท/ช่วง/จำนวน/สถานะ) row → `openView('leave',id)` L2373
- **OT & เวลาทำงาน** L2379 (chip `CH_ASSUMED+CH_RO`): def-grid "OT รวมเดือนนี้ 12 ชั่วโมง (อนุมัติ 8 · รออนุมัติ 4)" + ตารางสแกน (วันที่/เข้า/ออก/หมายเหตุ) — **read-only, ไม่มี row click**
- **ตารางกะของฉัน** (`sec()` L2391 · chip `CH_ASSUMED+CH_RO`): table (วันที่/กะ) สัปดาห์นี้ · source ระบบกะ/บันทึกเวลา (Time · W2) · **ESS ไม่แก้กะ** (L2184/2390)

### P-03 · เอกสาร & สิทธิ์ (`renderDocs` L2402) — FN-05/06/07/08
- **ใบเบิกค่าใช้จ่าย** L2405 (chip `CH_ASSUMED` + ปุ่ม **ยื่นเบิก** → `deepLink('expense')`): table (เรื่อง/วันที่/จำนวนเงิน/สถานะ) row → `openView('expense',id)` L2410
- **หนังสือรับรอง / เอกสาร** (`sec()` L2416 · chip `CH_ASSUMED` + ปุ่ม **ขอหนังสือ** → `deepLink('cert')`): table (เอกสาร/วันที่ออก/ผู้ออก/สถานะ) row → `openView('cert',id)` L2420
- **สวัสดิการ & อบรม** L2426 (chip `CH_ASSUMED+CH_RO`): `.bal-row` แต่ละสวัสดิการ — มี total → q-bar + "เหลือ/total" (baht ตัด `.00`) · ไม่มี total → note (เช่น "คุ้มครอง · วงเงิน 500,000 บาท") · ตามด้วยตารางอบรม (หลักสูตร/วันที่/ชั่วโมง/ใบรับรอง/สถานะ) row → `openView('training',id)` L2440
- **ข้อมูลส่วนตัว / โปรไฟล์** L2446 (chip `CH_ASSUMED` + ปุ่ม **ดูโปรไฟล์** → `openView('profile',EMP.id)` + ปุ่ม **ขอแก้ข้อมูล** → `deepLink('profile')`): def-grid (ชื่อ/ตำแหน่ง/อีเมล/เลขบัตร ปชช. `.masked` + chip "ปิดบัง") + note "การแก้ไขข้อมูลต้องยื่นผ่านหน้าฟีเจอร์เจ้าของเพื่อขออนุมัติ — ESS แก้ไขข้อมูลเองไม่ได้"

### P-04 · แจ้งเตือน (`renderNotify` L2462) — FN-09/90
- **sec-head** L2482 (chip `CH_ASSUMED+CH_RO`) — consume feed จาก ENG-NOTIFY (ESS ไม่ยิง event)
- **filter row** L2485: `.input-search` placeholder "ค้นหาการแจ้งเตือน" (`oninput` → `state.notif.q`; render) + toggle `ทั้งหมด` / `ยังไม่อ่าน` (`state.notif.unread`)
- **feed** `.nfeed` L2473: `.nrow` (`.unread` = พื้นแดงจาง + dot) → `openView('notif',id)` · client-side filter (q + unread) L2463–2468
- **empty** (`emptyStateHTML` L2471): "ไม่พบการแจ้งเตือน" / "ลองล้างคำค้นหรือตัวกรอง"

---

## §5 · Component Inventory (anchor + states)

### KPI card (`.qcard` · `qcard()` L2334)
- โครง: `.qc-top`(icon `.qc-ic` + `.qc-label` + `.qc-badge` optional) + `.qc-value` + `.qc-sub` · เป็น `<button>` เต็มใบ
- **states:** default / hover (L1426 · border + shadow + translateY(-1px)) / badge (เฉพาะ unread>0 · แดง) / **ไม่มี** disabled/loading/empty (mock data นิ่ง)

### Section block (`.ess-sec` · `sec()` L2494)
- `.ess-sec-head` (icon `.sh-ic` + h3 + `.sh-sub` + `.sh-right` chips/ปุ่ม) + `.ess-sec-body[.flush]`
- `.sh-right` = จุดวาง chip `CH_ASSUMED` / `CH_RO` + ปุ่ม deep-link (`btn-sm`)

### Read-only tables (`.table` in `.table-scroll`)
- `tableRows(heads,rowsHtml)` L2500 / inline tables · row `.is-clickable` → `openView(mode,id)` · pill `pill(text,variant)` L2241
- **states:** default / hover (base-kit) / clickable(cursor) / **ไม่มี** sort/select/pagination/inline-edit (display-only lists · Rule #103)

### Quota mini-bar (`.quota` L1469)
- `.q-name` + `.q-val`(คงเหลือ b / total) + `.q-bar > i`(width=pct% teal) · read-only

### Chips (demo-only · ดู §DEMO-ONLY)
- `CH_ASSUMED` L2243 = `.chip-assumed.demo-only` "[ASSUMED contract]" (link-2 icon · สีส้ม) — soft-ref marker FN-11
- `CH_RO` L2244 = `.chip-ro.demo-only` "อ่านอย่างเดียว" (lock icon · เทา)

### Status pills (`pill()` L2241 · variant → base-kit `.pill-*`)
| variant | ใช้กับ (data) |
|---|---|
| success | จ่ายแล้ว · อนุมัติแล้ว · ผ่าน · ออกแล้ว |
| warning | รออนุมัติ |
| (อื่นตาม `variant` field ใน DATA) | — |

### Masked value + reveal (profile drawer)
- `.masked` L1486 (letterspacing) · `.reveal-btn` L1487 · toggle `state.drawer.reveal` L2573 (แสดง↔ซ่อน) — **ค่าเต็มมากับ payload อยู่แล้ว** (client toggle) · prod: reveal log `reveal_restricted` (API-06)
- **states:** masked(default `EMP.nationalId`=`X-XXXX-XXXXX-56-7`) / revealed(`EMP.nationalIdFull`=`1-2345-67890-56-7` + label "ซ่อน") · bank เช่นเดียวกัน (`••••••3456` ↔ `123-4-53456-7`)

### Buttons — inventory verbatim
`ยื่นคำขอ` · `ยื่นลา` · `ยื่นเบิก` · `ขอหนังสือ` · `ขอแก้ข้อมูล` · `ดูโปรไฟล์` · `ดูโปรไฟล์ของฉัน`(btn-link) · `ปิด` · `เข้าใจแล้ว` · `แสดง`/`ซ่อน`(reveal) · `ทั้งหมด`/`ยังไม่อ่าน`(filter) · `ทดสอบเข้าถึงข้อมูลพนักงานอื่น`(demo-only)
- **ไม่มีปุ่ม** บันทึก/สร้าง/แก้ไข/ส่ง/อนุมัติ/ลบ ที่ไหนเลย — DISPLAY-ONLY lock (L2146) · read-only สื่อผ่าน **การไม่มีปุ่ม edit/save** (28.L2242 comment)

---

## §6 · Overlay Registry (8 overlays · dismiss rules + z)

| overlay | selector | ขนาด/position | เปิด | ปิด (dismiss) | z |
|---|---|---|---|---|---|
| Sidebar | `.sidebar` L1553 | fixed 232px | เปิดตลอด (mobile `.open` toggle L1581) | — | `--z-shell` 20 |
| User menu | `.user-menu` (base-kit) | absolute ใต้ chip | — (base-kit · **ไม่ถูก wire ในหน้านี้** — user-chip static ไม่มี toggle) | click-outside (base-kit) | `--z-dropdown` 40 |
| Search list | `.ss-list` (base-kit combobox) | absolute overlay | — (**ไม่มี combobox ในหน้านี้** · base-kit เหลือค้าง) | Esc (เฉพาะเมนู) L1904 · click-outside | `--z-backdrop` 50 |
| Portal menu | `.menu-fixed` (base-kit) | fixed (portal `#overlay-root` L1599) | — (**ไม่ใช้ในหน้านี้** · base-kit) | `closeOverlay()` (base-kit) | `--z-portal` 60 |
| **Drawer backdrop** | `.drawer-backdrop` #drawerBackdrop L877/L1605 | fixed inset0 · rgba(17,17,17,.40) | `openView()` add `.is-open` L2514 | **คลิก → `closeDrawer()`** L1605 | `--z-backdrop` 50 |
| **Drawer (view)** | `.drawer.standard` #drawer L887/L1606 | fixed right · **680px** (L901) / max 100vw · slide translateX 280ms | `openView(mode,id)` L2510 | ปุ่ม X (L2524) · ปุ่ม "ปิด" (L2529) · Esc · คลิก backdrop | `--z-drawer` 55 |
| **Modal backdrop** | `.modal-backdrop` #modalBackdrop L1107/L1611 | fixed center · rgba(17,17,17,.50) | `openModal()` L1728 | **คลิก → `closeModal()`** L1611 | `--z-portal` **60** (⭐ เหนือ drawer · DSP-01 L1372) |
| **Modal** | `.modal` L1120/L1612 | 440px / max 92vw · scale 200ms · `event.stopPropagation()` L1612 | `openModal(type,data)` L1728 | ปุ่ม "ปิด"/"เข้าใจแล้ว" · Esc · คลิก backdrop | (ใน backdrop 60) |
| Toast | `.toast` #toast L1618 | fixed · auto-hide | `showToast(msg,variant,ms)` L1752 | auto (durationMs · default 2800 · deepLink 3200) | `--z-toast` 90 |

### Read-only Drawers (view only · render โดย `renderDrawer()` L2531 · **ไม่มี edit/save ที่ไหน**)
| mode | fn / anchor | หมายเหตุ |
|---|---|---|
| `payslip` | L2533 | **2 sub-tabs:** รายละเอียด (L2543) · **สะสมทั้งปี (YTD)** (L2551 · `state.drawer.sub`) · footer `drawerFoot()` = "ปิด" อย่างเดียว |
| `profile` | L2561 | **3 sections:** ข้อมูลทั่วไป · RESTRICTED (reveal masking L2573) · **ประวัติการเข้าถึง (append-only)** L2576 · footer **มีปุ่ม "ยื่นคำขอ"** → `openModal('actionPicker')` (เปิดทับ drawer → DSP-01) L2584 |
| `leave` | L2586 | def-grid + note "อ่านจากระบบการลา (ต้นทาง)" · footer "ปิด" |
| `expense` | L2597 | def-grid + note "อ่านจากระบบเบิกค่าใช้จ่าย (ต้นทาง)" · footer "ปิด" |
| `cert` | L2608 | def-grid + note "ไฟล์ PDF ออกจากฝ่ายบุคคล (ต้นทาง)" · footer "ปิด" |
| `training` | L2619 | def-grid (หลักสูตร/วันที่/ชั่วโมง/ใบรับรอง/สถานะ) · footer "ปิด" |
| `notif` | L2630 | ข้อความแจ้งเตือนเต็ม · footer "ปิด" |
| *(fallback)* | L2636 | "ไม่พบข้อมูล" |

- `drawerHead(eyebrow,title,sub)` L2519 (eyebrow + `CH_RO` + X button) · `drawerFoot()` L2526 = `.ro-strip` "อ่านอย่างเดียว · แก้ไขไม่ได้ในพอร์ทัล" + ปุ่ม **ปิด** เท่านั้น

### Modals (render โดย `renderModal()` L2642)
| type | fn / anchor | รูปแบบ |
|---|---|---|
| `actionPicker` (M-01) | L2643 | **choice list — LINK ONLY** · 5 `apRow()` (ขอลา/OT/เบิก/แก้ข้อมูล/หนังสือรับรอง) → `deepLink(key)` · note OQ-HR-04 · footer "ปิด" · **ไม่มี form/submit** |
| `accessDenied` (M-02 · 403) | L2656 | error 403 · `.deny-code` "403" + ข้อความปิดบัง self-access · footer "เข้าใจแล้ว" · **เป็น real guard** (trigger สาธิต = ปุ่ม demo-only) |

---

## §7 · Interaction Spec

### ⭐ Esc chain (ลำดับจริงจาก handler)
1. **L1904** — combobox `ssOnKey()` (base-kit): `else if(e.key === 'Escape'){ e.stopPropagation(); s.open=false; … }` → Esc ปิดเฉพาะ dropdown ก่อน (stopPropagation) — *หน้านี้ไม่มี combobox จริง แต่ handler ยังผูก*
2. **L1766** — global `keydown`: `if(e.key === 'Escape'){ if(state.modal.open) closeModal(); else if(state.drawer.open) closeDrawer(); }` → **modal ก่อน drawer**

> ลำดับปิด: (combobox) → modal → drawer · modal ซ้อนบน drawer ได้ (DSP-01) — `closeModal()` คง `lockScroll` ถ้า drawer ยังเปิด (L1743)

### Overlay lifecycle
- **openView** L2510: set `state.drawer` (mode/recordId/step/sub/reveal) → render → rAF add `.is-open` + `lockScroll(true)` + `trapFocus(dw)`
- **closeDrawer** L1717 (base-kit): remove `.is-open` + `releaseFocus` + `lockScroll(false)` + setTimeout 280ms reset state
- **openModal** L1728 / **closeModal** L1738: rAF add is-open + `trapFocus(.modal)` · closeModal คง scroll-lock เมื่อ drawer ยังเปิด (L1743) + setTimeout 200ms reset
- **scroll lock:** `lockScroll(on)` L2112 = toggle `body.is-overlay-open` (L76 `overflow:hidden`) — **มี**
- **focus trap:** `trapFocus()` L2114 / `releaseFocus()` L2133 — **มี**
- **focus/scroll restore:** `preserveRenderState()` L1986 / `restoreRenderState()` (Rule #29 · DSP-02) — **มี** (คง sub-tab/reveal/scroll ข้าม innerHTML rebuild)
- click-outside: drawer backdrop L1605 · modal backdrop L1611
- **stopPropagation guard** L2684: คลิกใน `.ap-row / .qcard` → stopPropagation (Rule #68)

### Positioning
- drawer = fixed right slide (translateX) · modal = fixed center scale · toast = fixed · **ไม่มี** popover/portal positioning ที่ feature ใช้เอง (base-kit เหลือค้าง)

### Tab / state persistence (DSP-02)
- `state.tab` L2234 · `state.notif{q,unread}` L2235 — เก็บใน state object ข้าม `render()` (innerHTML rebuild ไม่ล้าง) · drawer sub-tab/reveal อยู่ใน `state.drawer` (L2511) เช่นกัน

---

## §8 · State-Driven UI Matrix

### Persona / access model — **single self persona (ไม่มี role switch)**
- Persona เดียว = **สมชาย ใจดี · EMP-00123 · พนักงาน (self)** (`EMP` L2151) — ต่างจาก welfare ที่มี 3 role
- self-access (SecC): ทุก surface = "เฉพาะของตนเอง" · เข้า id คนอื่น → **403** (M-02 · FN-10)
- masking: `national_id` / `bank_account_no` masked by default → reveal = client toggle (self · L2573) → prod log audit

### Notification filter states (`renderNotify` L2463)
| state | ผล |
|---|---|
| `q` ว่าง + `unread=false` | แสดงทุกรายการ (4) |
| `q` มีคำ | filter `(title+desc).indexOf(q)` |
| `unread=true` | เฉพาะ `n.unread===true` (2 ใบ) |
| filter → 0 แถว | empty state "ไม่พบการแจ้งเตือน" |

### Payslip drawer sub-tab (`state.drawer.sub` L2538)
| sub | เนื้อหา |
|---|---|
| 0 (รายละเอียด) | รอบเดือน/รายได้รวม/รายการหัก/ยอดสุทธิ/สถานะ + note all-or-nothing self |
| 1 (สะสมทั้งปี YTD) | รายได้สะสม/ภาษีสะสม/ประกันสังคมสะสม/สุทธิสะสม (`DATA.ytd`) |

### Profile reveal (`state.drawer.reveal` L2563)
| reveal | national_id | bank_account |
|---|---|---|
| false (default) | `X-XXXX-XXXXX-56-7` + ปุ่ม "แสดง" | `••••••3456` |
| true | `1-2345-67890-56-7` + ปุ่ม "ซ่อน" | `123-4-53456-7` |

### Deep-link result (`deepLink` L2675) — HTML stub
- ทุก key → ปิด overlay ที่ค้าง → toast "กำลังนำทางไปหน้า "{label}"" (3200ms) · **prod = navigate จริง** (route ASSUMED)

---

## §9 · Microcopy (verbatim)

### Toast (`showToast` — 1 call site · L2680)
| variant | ข้อความ (label = LINKS[key].label) |
|---|---|
| info | `กำลังนำทางไปหน้า "การลา"` · `…"ขอทำงานล่วงเวลา"` · `…"เบิกค่าใช้จ่าย"` · `…"แก้ไขข้อมูลพนักงาน (ขออนุมัติ)"` · `…"หนังสือรับรอง"` |

> ต่อกับตัวแปร `t.label` — ตัว literal คือ `กำลังนำทางไปหน้า "…"` (extractor เห็น 0 toast literal เพราะเป็น concat)

### Empty state (`emptyStateHTML` L2471 · verbatim)
| title | desc |
|---|---|
| ไม่พบการแจ้งเตือน | ลองล้างคำค้นหรือตัวกรอง |

### Header / banner (verbatim)
- page title "ESS ของฉัน" · `.ph-count` "พนักงานทำเอง" · sub "ดูข้อมูลของคุณจากทุกระบบไว้ที่เดียว — สลิป · ลา · OT · เบิก · หนังสือรับรอง · สวัสดิการ · อบรม · แจ้งเตือน" (L2274)
- **self-banner** (L2281): "คุณกำลังดูข้อมูลของตนเอง (**สมชาย ใจดี · EMP-00123**) — ข้อมูลส่วนตัว/เงินเดือนแสดงเฉพาะของคุณเท่านั้น"
- **launcher** (L2315): "ต้องการยื่นคำขอใช่ไหม?" / "เลือกประเภทคำขอ แล้วระบบจะพาไปยังหน้าฟีเจอร์เจ้าของเพื่อกรอกและส่ง (ESS ไม่รับคำขอเอง)"

### action-picker modal (M-01 · L2646–2653 verbatim)
- title "ยื่นคำขอ" · subtitle "เลือกประเภทคำขอ — ระบบจะพาไปยังหน้าฟีเจอร์เจ้าของเพื่อกรอกและส่ง"
- rows (title / sub): "ขอลา"/"ไปที่หน้า "การลา"" · "ขอทำงานล่วงเวลา (OT)"/"ไปที่หน้า "ขอ OT"" · "ขอเบิกค่าใช้จ่าย"/"ไปที่หน้า "เบิกค่าใช้จ่าย"" · "ขอแก้ข้อมูลส่วนตัว"/"ไปที่หน้าขออนุมัติแก้ข้อมูล" · "ขอหนังสือรับรอง"/"ไปที่หน้า "หนังสือรับรอง""
- note (L2653): "ESS ไม่รับหรือบันทึกคำขอเอง — ทุกการยื่นทำที่หน้าฟีเจอร์เจ้าของ (deep-link) ตามมติ OQ-HR-04"

### 403 modal (M-02 · L2660–2662 verbatim)
- title "เข้าถึงถูกปฏิเสธ" · subtitle "พนักงานเห็นได้เฉพาะข้อมูลของตนเอง" · deny-code "403"
- body: "คุณ (สมชาย ใจดี) ไม่มีสิทธิ์เข้าถึงข้อมูลของพนักงานคนอื่น ระบบปิดบังและไม่แสดงข้อมูลนอกขอบเขตของคุณ" · ปุ่ม "เข้าใจแล้ว"

### Notification titles/desc (verbatim · `DATA.notifications` L2209–2214)
| title | desc | time |
|---|---|---|
| สลิปเงินเดือนเดือนกรกฎาคมออกแล้ว | ดูสลิป PS-2568-07 ได้ที่แท็บเงินเดือน & เวลา | 31 ก.ค. 2568 |
| คำขอลาพักร้อนได้รับการอนุมัติ | LV-2568-014 · 12–13 มิ.ย. 2568 | 10 มิ.ย. 2568 |
| ใบเบิก EX-2568-028 อนุมัติแล้ว | ค่ารับรองลูกค้า 3,400 บาท | 9 ก.ค. 2568 |
| แจ้งเตือนอบรมประจำปี | ลงทะเบียนหลักสูตรบังคับภายใน 31 ส.ค. 2568 | 1 ก.ค. 2568 |

### Key inline notes (verbatim)
- drawer footer (L2528): "อ่านอย่างเดียว · แก้ไขไม่ได้ในพอร์ทัล"
- payslip note (L2550): "สลิปฉบับ PDF ออกจากระบบเงินเดือน (ต้นทาง) — ESS แสดงผลอ่านอย่างเดียว เห็นเฉพาะสลิปของตนเองแบบ all-or-nothing"
- profile RESTRICTED section (L2572): "ข้อมูลจำกัดสิทธิ์ (RESTRICTED · ปิดบังตามตนเอง)" · audit (L2578): "บันทึกการเข้าถึงถูกเพิ่มอัตโนมัติ (แก้/ลบไม่ได้)"
- profile page note (L2456): "การแก้ไขข้อมูลต้องยื่นผ่านหน้าฟีเจอร์เจ้าของเพื่อขออนุมัติ — ESS แก้ไขข้อมูลเองไม่ได้"
- sidebar footer: "โหมดพนักงาน · self-service" · sibling title: "ฟีเจอร์เจ้าของ — ปลายทาง deep-link (ไม่ได้ทำในรอบนี้)"

---

## §10 · Data Binding & BACKEND anchors

> HTML ใช้ mock in-memory · **self-scope เดียว** (`EMP` L2151 · `DATA` L2161 · `LINKS` L2225) — **GET-only aggregate** ไม่มี mutation ธุรกิจ

**`EMP` (self mock · L2151):** id `EMP-00123` · name `สมชาย ใจดี` · initials `สจ` · position `เจ้าหน้าที่การตลาด` · dept `ฝ่ายการตลาด` · branch `สำนักงานใหญ่` · email `somchai.j@cube.co.th` · startDate `1 มี.ค. 2562` · bank `ธนาคารกสิกรไทย` · nationalId masked `X-XXXX-XXXXX-56-7` (full `1-2345-67890-56-7`).

| UI action (fn) | plug → FRD API |
|---|---|
| dashboard cards (`renderHome`) | GET `/ess/dashboard` (API-01 · FN-01 · per-card degrade OQ-ESS-04) |
| payslip list/detail/YTD (`openView('payslip')`) | GET `/ess/payslips` · `/:id` · `/ytd` (API-02 · all-or-nothing self) |
| surface read leave/ot/shift/expense/cert/welfare/training (`renderPay`/`renderDocs`/`openView`) | GET `/ess/surface/:type[/:id]` (API-03 · [ASSUMED] owner read-model) |
| notifications feed + search/filter (`renderNotify`) | GET `/ess/notifications?q=&unread=` (API-05 · **consume ENG-NOTIFY** · ESS ไม่ยิง event) |
| profile (`openView('profile')`) | GET `/ess/profile` (API-06 · masked · reveal → log `reveal_restricted`) |
| access audit (`DATA.accessAudit` in profile) | GET `/ess/access-audit` (API-07 · append-only read · `T_ess_access_audit`) |
| deep-link ยื่นคำขอ 5 ตัว (`deepLink`) | **NO API** — client navigate (API-04 · §2.4 · route ASSUMED OQ-ESS-02) |
| ทุก read (side-effect) | server hook: append access-audit + emit **CSQ self-access (SecC)** event (FN-93/10 · event id ASSUMED OQ-ESS-01) |

- **self-scope enforce ที่ backend** — endpoint ไม่รับ `employee_id` param; id คนอื่น → 403 (05_RULES ERR-403 · FN-10)
- **ไม่มี** `// BACKEND:` comment marker ในโค้ด — mock ทุกตัวมีจุด plug ชัดตามตารางบน

---

## §11 · Traceability (Brief ↔ FRD ↔ HTML) + Drift Log

| Brief § | FRD (P/M/D · API · FN · OQ) | HTML anchor |
|---|---|---|
| §2.1 tab home | P-01 · API-01 · FN-01 | `renderHome()` L2308 |
| §2.1 tab pay | P-02 · API-02/03 · FN-02/03/04 | `renderPay()` L2345 |
| §2.1 tab docs | P-03 · API-03/06 · FN-05/06/07/08 | `renderDocs()` L2402 |
| §2.1 tab notify | P-04 · API-05 · FN-09/90 | `renderNotify()` L2462 |
| §2.2 deep-link ×5 | §2.4 · API-04 · FN-11 · **OQ-ESS-02** | `LINKS` L2225 · `deepLink()` L2675 |
| §6 D-01 payslip (YTD) | D-01 · API-02 · FN-02 | `renderDrawer` payslip L2533 |
| §6 D-02 profile (reveal+audit) | D-02 · API-06/07 · FN-08/93 | profile L2561 · reveal L2573 |
| §6 D-03 leave/expense/cert/training/notif | D-03 · API-03/05 · FN-03/05/06/07/09 | L2586–2635 |
| §6 M-01 action-picker | M-01 · API-04 · FN-11 · OQ-HR-04 | `renderModal` actionPicker L2643 |
| §6 M-02 403 | M-02 · ERR-403 · FN-10/94 · OQ-ESS-05 | accessDenied L2656 |
| §8 masking / reveal | FN-94 · API-06 | `.masked` L2455/2573 |
| §8 self-access (SecC) | FN-10/93 · CSQ · **OQ-ESS-01** | self-banner L2280 · accessAudit L2215 |
| §1 z / DSP-01 | §1.6 · DSP-01 precedent | `.modal-backdrop` z=`--z-portal` L1372 |
| §7 DSP-02 keep-state | §1.6 · Rule #29/DSP-02 | `state.tab`/`state.notif` L2234 · `preserveRenderState` L1986 |
| §5 responsive | FN-92 · BR-05 | `@media` L1536/1544 |

### ⚠️ Drift Log
| # | ชนิด | รายการ | หมายเหตุ / ข้อเสนอ |
|---|---|---|---|
| D-1 | note (by-design) | tab สลับด้วย `state.tab` (L2234) **ไม่ push hash** — extractor เห็นแค่ 5 deep-link route ไม่เห็น hash ต่อ tab | จงใจ (1 feature = 1 เมนู · #104) · refresh = กลับ `home` (ไม่มี URL deep-link เข้า tab) — ตรง 01_UI P-01..04 |
| D-2 | HTML-only (ASSUMED) | deep-link routes 5 ตัว `#/leave/new` ฯลฯ = **[ASSUMED contract]** | route ปลายทางยังไม่ยืนยันกับ owner — **carry OQ-ESS-02** · prod ต้องยืนยันก่อน wire (ไม่ block) |
| D-3 | HTML-only (base-kit ค้าง) | overlay `.user-menu` · `.ss-list` · `.menu-fixed` มี CSS/handler แต่ **ไม่ถูก wire** ในหน้านี้ | base-kit residual (combobox/portal ไม่ใช้ · user-chip static) — ไม่ใช่ UI gap · dev ไม่ต้อง implement |
| D-4 | note (by-design) | `.modal-backdrop` z = `--z-portal`(60) ไม่ใช่ backdrop(50) | จงใจ (DSP-01 · L1372) ให้ action-picker เปิดทับ profile drawer — ระบุใน §1/§6 กัน dev ตั้งผิด |
| D-5 | FRD-only | CSQ self-access event id · owner surface field-level schema | `[ASSUMED soft-ref]` (OQ-ESS-01/LK-5) — backend/owner contract · HTML mock ไม่จำลอง (ไม่ใช่ UI gap) |
| D-6 | FRD-only | EC-07..EC-11 · ERR-404 · degrade path (Payroll down) OQ-ESS-04 | backend contract (`[AI-DEFAULT]`) — HTML แสดง happy path · dev implement ฝั่ง server |

**สรุป: ไม่มี business drift ที่ทำให้ HTML ขัด FRD** — drift ทั้งหมดเป็น by-design (state-tab / DSP-01), ASSUMED cross-module (routes/CSQ/owner schema), หรือ backend-contract ที่ mock ไม่จำลอง

---

## §DEMO-ONLY · 🔴 รายการที่ prod build ต้อง strip (`.demo-only`)

> **prod build = ซ่อน/ลบทุก `.demo-only`** (ใส่ `.demo-only{display:none!important}` หรือ strip ออกตอน build · L1394–1397) — dev ต้องส่ง **prod ที่ไม่มีของสาธิตเหล่านี้**

| # | element | anchor | render ที่ไหน | prod behavior |
|:--:|---|---|---|---|
| 1 | **persona/demo strip** `.demo-strip.demo-only` (label "ตัวอย่าง (persona)" + avatar + ปุ่มทดสอบ) | L2285 | ใต้ self-banner ทุก tab | **ลบทั้งแถบ** — persona เดียว (self) มาจาก JWT จริง |
| 2 | **ปุ่ม "ทดสอบเข้าถึงข้อมูลพนักงานอื่น"** → `openModal('accessDenied')` | L2288 (ใน demo-strip) | ในแถบ #1 | **ลบ** (เป็น demo trigger ของ 403) · ⚠️ **แต่ modal 403 (M-02) เอง = real guard ห้ามลบ** — prod ทริกเกอร์จาก backend 403 จริง |
| 3 | **chip `[ASSUMED contract]`** `CH_ASSUMED` = `.chip-assumed.demo-only` | L2243 (ใช้ซ้ำหลายจุด: L2348/2362/2381/2391/2407/2417/2428/2448/2484/2537…) | ทุก section head + drawer head | **ลบ chip** — soft-ref marker สำหรับ BA/dev รอบนี้เท่านั้น (route ยืนยันแล้ว = ไม่ต้องมี) |
| 4 | **chip "อ่านอย่างเดียว"** `CH_RO` = `.chip-ro.demo-only` | L2244 (ใช้ซ้ำหลายจุด: L2327/2348/2381/2391/2428/2484/2537/2562…) | section head + drawer head/eyebrow | **ลบ chip** — read-only สื่อด้วย "การไม่มีปุ่มแก้/บันทึก" แทน (comment L2242) · ⚠️ chip "ปิดบัง" ใน profile (L2455) เป็น `.chip-ro` **ไม่มี `.demo-only`** = คงไว้ |
| 5 | **CSS rule** `.demo-only{}` | L1397 | `<style>` | ตั้ง `display:none!important` ตอน build (หรือ strip element) |

**ไม่ใช่ demo-only (คงไว้ใน prod):** self-banner SecC (L2280) · 403 modal M-02 (L2656 · real guard) · chip "ปิดบัง" profile (L2455) · ปุ่ม deep-link ทั้งหมด · read-only drawer footer strip (L2528)

**นับ demo-only:** 3 ชนิด element (persona strip + ปุ่มทดสอบ 403 · [ASSUMED] chip · อ่านอย่างเดียว chip) จาก 4 source line (L2243/2244/2285/2288) + 1 CSS rule (L1397) · grep `demo-only` = 6 hit (รวม 2 comment)

---

## §12 · Diff จากเวอร์ชันก่อน

— ไม่มี HTML เวอร์ชันก่อนให้เทียบ (บรีฟ AS-BUILT รอบแรก · N/A)

---

## §13 · 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)

> ที่เดียวที่อนุญาตให้คิดเอง (R1) — ต่อไปนี้ **ไม่มีในจอ** เป็นข้อเสนอ ไม่ใช่สเปคที่ต้องทำ

1. **Deep-link route confirm (OQ-ESS-02)** — 5 route ยัง ASSUMED · ก่อน dev ควรยืนยัน route จริง + fallback (OQ-ESS-03) กับ owner แต่ละ feature (การลา/OT/Expense F101/Employee Master/หนังสือรับรอง)
2. **Tab deep-link เข้า URL** — ปัจจุบัน tab = `state.tab` ล้วน (refresh กลับ home) · ถ้าธุรกิจต้องการ bookmark/แชร์ลิงก์ tab ควรผูก hash `#/ess/<tab>` (กระทบ hashchange L2039) — ยิง OQ ก่อน
3. **CSQ self-access event id (OQ-ESS-01)** — event id/SecC pipe ยัง ASSUMED · ต้องให้ทีม security เคาะก่อน wire (ห้าม hardcode)
4. **Degrade UX ต่อ card/surface (OQ-ESS-04)** — HTML แสดง happy path · prod ควรมี per-surface error/loading state (owner down) ตาม `[AI-DEFAULT]` per-card try/catch
5. **base-kit residual cleanup** — `.user-menu` / `.ss-list` / `.menu-fixed` ไม่ถูกใช้ · ถ้าต้องการไฟล์ prod ผอม อาจตัด CSS/handler ที่ไม่ wire (ไม่กระทบพฤติกรรม)
