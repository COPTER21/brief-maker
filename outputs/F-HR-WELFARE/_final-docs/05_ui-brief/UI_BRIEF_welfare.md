# UI Brief — F-HR-WELFARE · สวัสดิการ (Welfare)

> **EXTRACTION-BASED (Iron Rule R1)** — ทุกบรรทัดในบรีฟนี้ trace กลับหา selector / function / ข้อความจริงใน `welfare.html` ได้
> อ้าง `Lxxxx` = เลขบรรทัดใน HTML · ข้อเสนอที่ไม่มีในจอ อยู่ท้ายไฟล์ §13 เท่านั้น
> คู่กับ: **HTML (source of truth)** + **FRD Pack** (ระบบ) + บรีฟนี้ (design intent)

---

## §0 · Document Control + Pairing

| | |
|---|---|
| Feature | F-HR-WELFARE · สวัสดิการ (Welfare) |
| HTML source | `outputs/F-HR-WELFARE/welfare.html` · `<title>` = "สวัสดิการ (Welfare) · CUBE NATIVE" (L6) · 3267 บรรทัด · BASE-KIT v6.4 |
| Archetype | **MASTER + light transaction** — จงใจ **NOT Pattern Q** (ไม่มี running-no / PDF / doc-wizard) · PREFLIGHT L3264 |
| FRD Pack | `FRD_F-HR-WELFARE_Pack/` (01_UI · 02_API · 03_LOGIC · 04_DB · 05_RULES · 06_TESTS · 07_LOCKED) — **paired** |
| BRD | `BRD_welfare.md` |
| HTML เก่า (diff) | — ไม่มี (บรีฟนี้เป็น full AS-BUILT รอบแรก · §12 = N/A) |
| Gate สถานะ | PREFLIGHT L3258: `audit.sh FAIL=0 · WARN=4` · `node --check OK` · role sweep 7/7 |
| Drift | มี drift ที่บันทึกใน §11 (ทั้งหมดเป็น HTML-only display-only surface หรือ FRD-only cross-module) — ไม่มี business drift ที่ block |

**สถาปัตยกรรม:** Single-file vanilla-JS SPA · state-driven `render()` (L2320) · innerHTML rebuild + Render Preservation (Rule #29) · Lucide icon (multi-CDN fallback pin 0.469.0 · L1629) · ฟอนต์ Satoshi + Noto Sans Thai (L11–12).

---

## §1 · Design Tokens AS-BUILT (`:root` L24–67)

### Palette (CUBE Warm Light rebrand v2.0)
| token | ค่า | ใช้ |
|---|---|---|
| `--c-navy` / `--c-navy-2` | `#111111` | sidebar / heading |
| `--c-primary` / `--c-primary-hover` | `#FF3B30` / `#E62E24` | ปุ่มหลัก |
| `--c-teal` / `--c-teal-light` | `#FF9A1F` / `#FFB763` | accent |
| `--c-ink` | `#111111` | ตัวอักษรหลัก |
| `--c-mute` / `--c-mute-2` / `--c-mute-3` | `#54565C` / `#73757B` / `#9A9CA2` | ตัวอักษรรอง / masked |
| `--c-line` / `--c-line-2` / `--c-line-3` | `#DEDAD4` / `#E9E5E0` / `#F1EEEA` | เส้น |
| `--c-bg-off` | `#FAF8F5` | พื้นหลังหน้า |
| `--c-success` / `--c-warning` / `--c-danger` | `#1F9D55` / `#E8870F` / `#E62E24` | สถานะ |

### Type scale (fixed · Iron Rule L54–62)
`--fs-h1:22px` · `--fs-h2:17px` · `--fs-h3:15px` · `--fs-body:14px` · `--fs-sub:13px` · `--fs-meta:12px` · `--fs-cap:11px` · `--fs-kpi:28px`
font stack (L91): `'Satoshi','Noto Sans Thai',system-ui,sans-serif` · body 14px · line-height 1.5

### Spacing / Radius (L64–66)
`--sp-xs:4px --sp-sm:8px --sp-md:12px --sp-lg:20px --sp-xl:28px` · `--r-xs:4px --r-sm:6px --r-md:8px --r-lg:12px --r-full:999px`

### Shell dims
`--sidebar-w:232px` (L42) · `--shell-h:52px` (L43) · body `min-width:768px` (L99) · `scrollbar-gutter:stable` (L74 · Rule #35 กัน jank) · scrollbar 5px (L81)

### ⭐ Z-INDEX MAP (สูง → ต่ำ · L47–53)
| token | ค่า | ใช้กับ |
|---|---:|---|
| `--z-toast` | **90** | toast (สูงสุด — เห็นเหนือทุกอย่าง) |
| `--z-portal` | **60** | เมนู portal `#overlay-root` (Rule #95) · **`.modal-backdrop` ใช้ค่านี้** (ดูหมายเหตุ) |
| `--z-drawer` | **55** | ตัวลิ้นชัก `.drawer` |
| `--z-backdrop` | **50** | ฉากหลัง drawer/modal · search list |
| `--z-dropdown` | **40** | user menu · tooltip · **`.demo-strip`** |
| `--z-sticky` | **30** | shell-bar · thead sticky |
| `--z-shell` | **20** | sidebar |

> **หมายเหตุ z-index สำคัญ (extract L1111):** `.modal-backdrop` ตั้ง `z-index:var(--z-portal)` = **60** (ไม่ใช่ backdrop 50) — จงใจให้ modal เหนือ drawer(55) และให้ combobox portal ใน modal โผล่เหนือ modal ได้ตาม DOM order · comment ระบุว่าแก้ latent BASE-KIT bug U01 ("modal จมใต้ drawer") · **ห้ามตั้ง > portal** ไม่งั้น dropdown ใน modal จะจม
> `.drawer-backdrop` = `--z-backdrop`(50) · `.drawer` = `--z-drawer`(55) · `.demo-strip` = `--z-dropdown`(40)

---

## §2 · Route Map (hash-based · refresh-safe)

**1 feature = 1 เมนู (#104):** ทั้ง feature ใช้ route base เดียว `#/welfare/*` แล้วสลับ **4 tabs ในหน้าเดียว** (ไม่ใช่ 4 เมนู)

| route | tab | render fn | default |
|---|---|---|---|
| `#/welfare/registry` | ทะเบียนสวัสดิการ | `renderRegistry()` L2383 | ✅ (fallback) |
| `#/welfare/requests` | คำขอใช้สิทธิ์ | `renderRequests()` L2428 | |
| `#/welfare/balance` | คงเหลือรายคน | `renderBalance()` L2502 | |
| `#/welfare/report` | รายงาน | `renderReport()` L2583 | |

- **Router:** `currentTab()` L2310 = อ่าน `location.hash`, strip `#/`, split `/`, seg[1] → หา TABS · ไม่รู้จัก → fallback `registry`
- **Tab switch:** `goTab(t)` L2315 → `location.hash='#/welfare/'+t`
- **Refresh-safe / default:** L3254 — ถ้า `!location.hash || '#/' || '#'` → set `#/welfare/registry`
- **hashchange:** `window.addEventListener('hashchange', ()=>render())` L2048 (late-binding ชี้ render() ที่ feature override)
- skeleton router `getRoute()` L1686 / `navigate()` L1691 ยังคงอยู่ (base-kit) แต่ feature ใช้ `currentTab()`/`goTab()` แทน

---

## §3 · Layout Shell

| region | selector | หมายเหตุ |
|---|---|---|
| Sidebar | `.sidebar` L111 (fixed · w=`--sidebar-w`232px · bg `#111`) | โมดูล "ทรัพยากรบุคคล" > item `data-feature="welfare"` `.is-active` (L1525) · เมนูข้างเคียง (ทะเบียนพนักงาน/เข้า-ออกงาน/เงินเดือน/ตั้งค่า HR) = `stubNav()` L3216 |
| Sidebar footer | `.sb-footer` L1546 | "UAT · v1.0.0" + pulse-dot |
| Module toggle | `toggleModule(this)` L1676 | collapse ผ่าน `data-expanded` |
| Topbar | `.shell-bar` L1551 | nav-toggle (mobile) · breadcrumb "ทรัพยากรบุคคล › สวัสดิการ" (L1556) |
| Notif bell | `.icon-btn` L1562 | คลิก → toast (ดู §9) · มี `.notif-dot` |
| User chip | `.user-chip` #uc-name/#uc-role/#uc-av (L1567) | sync ตาม persona ผ่าน `syncPersona()` L2336 |
| User menu | `.user-menu` #userMenu (L1574) | toggle `toggleUserMenu()` L3217 · click-outside ปิด L3218 · items: โปรไฟล์ของฉัน · การตั้งค่า · ออกจากระบบ |
| Page host | `.content #page-content` L1584 | `render()` เขียน `renderPage()` ลงตรงนี้ |
| **Demo strip** | `.demo-strip` #demoRole L1588 | **persona/masking switch อยู่ที่นี่ที่เดียว (#105)** — ปุ่ม 3 role: `HR สวัสดิการ`(admin) · `หัวหน้า`(manager) · `พนักงาน`(employee) → `setRole()` L3215 |

**Page header (`renderPage()` L2347):** `.ph` title+sub ต่อ tab (L2356–2361) + `.ph-actions` (ปุ่มขวาบนต่อ tab) + `.tabs` (4 tab buttons + count chip `.tab-ct` จาก `counts` L2348) + tab body.

---

## §4 · Page Anatomy (ต่อ tab)

### P-01 · ทะเบียนสวัสดิการ (`renderRegistry` L2383) — FN-01..04
- **Action bar:** ปุ่ม `สร้างประเภทสวัสดิการ` (btn-primary → `openDrawer('benefit-create')`) L2365
- **Filter bar** `.filter-bar` L2413: search `ค้นหาชื่อ/รหัสสวัสดิการ` (oninput → `renderTableOnly('registry')`) · select สถานะ `[ทุกสถานะ|มีผล|ร่าง|เก็บถาวร]` L2389 · ปุ่ม `ล้างตัวกรอง` → `resetRegFilter()` L2423
- **Table** `#tbl-registry` L2417: คอลัมน์ ชื่อสวัสดิการ · หมวด · โควตา/วงเงินต่อปี · กลุ่มที่มีสิทธิ์ · วันมีผล · สถานะ · จัดการ(90px)
  - row `.is-clickable` → `openDrawer('benefit-view',id)` L2398 · ชื่อ+code+เวอร์ชัน · `benUnitLabel()` L2193 · pill `benPill()` L2298
  - row-actions (td `stopPropagation`): แก้ไข `openDrawer('benefit-edit')` · ปิดใช้ `openModal('archiveBenefit')` (ซ่อนเมื่อ archived) L2406-07
- **Footer:** `ทั้งหมด N รายการ` · `แสดง 1 – N จาก N` L2420
- **Empty:** `ไม่พบรายการที่ค้นหา` (ดู §9)

### P-02 · คำขอใช้สิทธิ์ (`renderRequests` L2428) — FN-07..15,17
- **Action bar:** `งานอนุมัติของฉัน` (`toggleMyApproval()` L2483 · filter status=pending) + `สร้างคำขอใช้สิทธิ์` (`openDrawer('request-create')`) L2367-68
- **Filter bar** L2471: search `ค้นหาเลขที่/ชื่อผู้ยื่น/ประเภท` · select สถานะ (8 ค่า L2437) · select ประเภท (จาก BENEFITS claimable L2439) · `ล้างตัวกรอง` → `resetReqFilter()`
- myApproval banner `.note is-info` L2467: "แสดงเฉพาะ **งานที่รออนุมัติ** (กล่อง "งานอนุมัติของฉัน" · DOA)"
- **Table** `#tbl-requests` L2476: เลขที่คำขอ(140px) · ผู้ยื่น(`personCell()` L2484 · masked) · ผู้ใช้สิทธิ์ · ประเภทสวัสดิการ · มูลค่า(`money()` masked) · วันที่ใช้สิทธิ์ · สถานะคำขอ(`reqPill()`) · สถานะจ่าย(`payPill()`)
  - row → `openDrawer('request-view',id)` L2454
- **Empty:** `ยังไม่มีคำขอ`

### P-03 · คงเหลือรายคน (`renderBalance` L2502) — FN-05,06,09,16,18
- **Person picker** `.person-pick-card` L2505: combobox `balEmp` (`searchSelectHTML` · placeholder `พิมพ์ชื่อ/ตำแหน่งพนักงาน`)
- ยังไม่เลือก → empty `เลือกพนักงานเพื่อดูสิทธิ์คงเหลือ` L2511
- เลือกแล้ว:
  - joiner note (ถ้า `emp.joiner`) `.note is-success` L2537: "พนักงานเข้าใหม่ … **สิทธิ์เปิดอัตโนมัติ** ตาม joiner signal"
  - `.person-hero` L2568: avatar + ชื่อ(masked) + meta(masked) + ปุ่ม `เปลี่ยนพนักงาน` (L2571 · reset empId)
  - card "สิทธิ์ · โควตา · คงเหลือ (ปีสิทธิ์ 2569)" L2572: table mini + qbar (`near`/`full` L2526) + tag `ใกล้เต็มโควตา` (≥80% L2527)
  - **payrollCard** (ถ้ามี benefit unit=percent & ไม่ ended) L2552-63: "จ่ายประจำผ่านเงินเดือน (สมทบ/หักอัตโนมัติ)" + input % (`setPayrollPct()` L2636) + note "ค่าตั้งต้นฝั่งสวัสดิการ (display-only) — การสมทบ/หักจริงทำงานที่ **Payroll (F065)**"
  - leaver → benRows แทนที่ด้วย note `.is-warn` "พนักงานพ้นสภาพ … สิทธิ์สวัสดิการสิ้นสุด" L2519
  - card ผู้ติดตาม L2575: ปุ่ม `เพิ่มผู้ติดตาม` (เฉพาะ `canSeeDependent()`) → `openDrawer('dependent-create',empId)` · ลบ → `openModal('removeDep',{emp,dep})` L2548 · masked ถ้าไม่ใช่ admin L2542

### P-04 · รายงาน (`renderReport` L2583) — FN-19
- **Stats** `.stats` L2613: คำขอทั้งหมด · อนุมัติแล้ว(+รออนุมัติ) · มูลค่าสวัสดิการรวม(masked→`•••`) · ใกล้เต็มโควตา(`nearLimitCount()` L2637)
- **Filter bar** L2620: select ประเภท · select กลุ่มพนักงาน · date from/to (`ตั้งแต่/ถึงวันที่ใช้สิทธิ์`) · `ล้างตัวกรอง` → `resetRep()` L2633
- **Table** L2629: ประเภทสวัสดิการ · หมวด · จำนวนคำขออนุมัติ · มูลค่ารวม(masked) — aggregate เฉพาะ status=`approved` (L2585)
- footer hint: `ตัวเลข = เฉพาะคำขอสถานะ "อนุมัติแล้ว"` L2630
- **Empty:** `ไม่พบข้อมูลตามตัวกรอง`
- **ข้อสังเกต:** ไม่มีปุ่ม export/print (report = view only · ตรงกับ 01_UI P-04 · NS-5)

---

## §5 · Component Inventory (anchor + states)

### Combobox / Search-select (`.search-select` · Rule #34/#94/#102 · L1837)
- markup `searchSelectHTML(key,opt)` L1837 · init `initSearchSelect(key,cfg)` L1850 · state `window.__ss[key]`
- โครง: `.ss-lead`(search icon) + `input.ss-input` + `.ss-clear`(hidden) + `.ss-caret` + `.ss-list`(hidden overlay)
- **#102 person anatomy (L1892):** option render — `avatar`(initials) หรือ `icon` + `.ss-opt-main`(label + `.ss-opt-sub`) + `.ss-opt-right`
  - person options `empOptions()` L3223: `{label:ชื่อ, sub:'ตำแหน่ง · แผนก', avatar:initials}` → avatar+name+position·dept
  - benefit options L3237: `{label, sub:'มีสิทธิ์/ไม่มีสิทธิ์ · '+benUnitLabel, icon:'heart-pulse', right: ✕ ถ้าไม่มีสิทธิ์}`
- **instances (`initCombos()` L3226):** `balEmp`(balance) · `reqEmp`/`reqDep`/`reqType`(request drawer) · `doaSlot1`/`doaSlot2`(DOA modal)
- **states:** default(ปิด) / open(query='') / typing(filter+`<mark>` highlight L1889) / picked(caret→clear) / empty(`ไม่พบรายการ` L1854) / keyboard(↑↓ hi, Enter pick, Esc ปิดเฉพาะเมนู L1906)
- **guard #29/#94:** `ssBlurActive()` L3225 blur ก่อน render (กัน focus-restore เด้งเปิด dropdown ซ้ำ) · `guardOverlayAutoCombo()` L1736 ปิด auto-focus combo ตอนเปิด overlay

### Status pills
| fn | enum → label · class |
|---|---|
| `reqPill()` L2287 | draft→`ร่าง`·pill-muted · pending→`รออนุมัติ`·pill-warning · approved→`อนุมัติแล้ว`·pill-success · rejected→`ไม่อนุมัติ`·pill-danger · cancelled→`ยกเลิก`·pill-muted · revoked→`ระงับ (พ้นสภาพ)`·pill-muted · **reversed→`กลับรายการแล้ว`·pill-danger** |
| `payPill()` L2293 | (เฉพาะ status=approved) none→`—` · pending→`รอจ่าย`·pill-warning · sent→`ส่งจ่ายแล้ว`·pill-info |
| `benPill()` L2298 | active→`มีผล`·pill-success · draft→`ร่าง`·pill-muted · archived→`เก็บถาวร`·pill-muted |

### ปุ่ม (buttons) — inventory verbatim
`สร้างประเภทสวัสดิการ` · `สร้างคำขอใช้สิทธิ์` · `งานอนุมัติของฉัน` · `ล้างตัวกรอง` · `บันทึกร่าง` · `ยืนยันสร้าง` · `บันทึกการแก้ไข` · `แก้ไข` · `ปิดใช้` · `ส่งอนุมัติ` · `อนุมัติ` · `ไม่อนุมัติ` · `กลับรายการ` · `ยกเลิกคำขอ` · `เพิ่มผู้ติดตาม` · `เปลี่ยนพนักงาน`
- footer สร้าง/แก้ (`footCreate()` L2911): ยกเลิก · บันทึกร่าง · `ยืนยันสร้าง`/`บันทึกการแก้ไข` (ternary `isEdit`)
- **loading state:** `lockBtn(btn,label)` L3214 — disable + spinner `loader-2 spin` + label เช่น `กำลังบันทึก…` / `กำลังอนุมัติ…` / `กำลังกลับรายการ…` / `กำลังบันทึก…`

### Form fields
- `fld(label,req,inner,err,help)` L2914 — label + `req`* + inner + field-help + field-error
- `selEnum()` L2918 / `selUnit()` L2689 (money|times|percent) · checkbox `.cb .is-checked` · seg-radio (ตัวเอง/ผู้ติดตาม L2724 · ผู้ติดตาม disabled ถ้า benefit ไม่ coversDep)
- upload zone `.upload-zone` → `mockUpload()` L2776 (mock ไฟล์) · file-item + ปุ่มลบ
- validate: `validateField()` L1942 · `clearFieldError()` L1950 · per-form `validateBenefit()` L3016 / `validateRequest()` L3092 / `submitDependent()` L3199

### Table / list
- `.table` (list-card) + `.mini` (in-card) · `renderTableOnly(tab)` L2493 = full render (lists เล็ก · Rule #103C) · qbar progress · near-tag

---

## §6 · Overlay Registry (9 overlays · dismiss rules + z)

| overlay | selector | ขนาด/position | เปิด | ปิด (dismiss) | z |
|---|---|---|---|---|---|
| Sidebar | `.sidebar` L111 | fixed 232px | เปิดตลอด (mobile toggle `.open`) | — | `--z-shell` 20 |
| Demo strip | `.demo-strip` L1375 | fixed left/bottom 16px | เปิดตลอด | — (ควบคุม persona) | `--z-dropdown` 40 |
| User menu | `.user-menu` L317 | absolute ใต้ chip | `toggleUserMenu()` L3217 | click-outside L3218 · toggle | `--z-dropdown` 40 |
| Search list | `.ss-list` L585 | absolute overlay | `ssOpen()` L1902 | click-outside L1915 · Esc(เฉพาะเมนู) L1913 · pick | (คู่ backdrop) |
| Portal menu | `.menu-fixed` L386 | fixed (portal `#overlay-root`) | `portalMenu()` L2088 | `closeOverlay()` L2114 | `--z-portal` 60 |
| **Drawer backdrop** | `.drawer-backdrop` #drawerBackdrop L877 | fixed inset0 · rgba(17,17,17,0.40) | `openDrawer()` L1698 add `.is-open` | **คลิก → `closeDrawer()`** L1599 | `--z-backdrop` 50 |
| **Drawer** | `.drawer` #drawer L887 | fixed right · **920px** / max 96vw · slide 280ms | `openDrawer(mode,recordId)` L1698 | ปุ่ม X/ปิด · Esc · คลิก backdrop | `--z-drawer` 55 |
| **Modal backdrop** | `.modal-backdrop` #modalBackdrop L1107 | fixed center · rgba(17,17,17,0.50) | `openModal()` L1723 | **คลิก → `closeModal()`** L1605 | `--z-portal` **60** (เหนือ drawer · ดู §1) |
| **Modal** | `.modal` L1120 | 440px / max 92vw · scale 200ms · `stopPropagation` L1606 | `openModal(type,data)` L1723 | ปุ่ม ยกเลิก/OK · Esc · คลิก backdrop | (ใน backdrop 60) |
| Toast | `.toast` #toast L1198 | fixed · max-width 380px · auto-hide | `showToast(msg,variant,2800)` L1761 | auto (durationMs) | `--z-toast` 90 |

### Drawers (เนื้อหา render โดย `renderDrawer()` L2642)
| mode | fn | หมายเหตุ |
|---|---|---|
| `benefit-create` / `benefit-edit` | `drawerBenefitForm()` L2653 | edit note ต่างกัน draft vs active (L2662) |
| `benefit-view` | `drawerBenefitView()` L2695 | sec ข้อมูล + กลุ่ม + ตารางเวอร์ชัน (effective dating) · header actions แก้ไข/ปิดใช้ |
| `request-create` | `drawerRequestForm()` L2716 | combobox reqEmp/reqDep/reqType + eligibility note (`reqCalcHtml()` L2758) + upload |
| `request-view` | `drawerRequestView()` L2779 | **4 tabs:** รายละเอียด · หลักฐาน · คงเหลือ · ประวัติ (L2783) |
| `dependent-create` | `drawerDependentForm()` L2880 | ชื่อ · ความสัมพันธ์ · วันเกิด · เกณฑ์บุตร ≤20 ปี |

### Modals (render โดย `renderModal()` L2927)
| type | fn | รูปแบบ |
|---|---|---|
| `archiveBenefit` | `modalConfirm` L2929 | is-warning · แจ้งจำนวนคำขอค้าง (FIX-06 · BR-DOA-8) → `doArchiveBenefit()` |
| `cancel` | `modalConfirm` L2934 | is-warning · draft/pending only → `doCancelRequest()` |
| `removeDep` | `modalConfirm` L2936 | is-danger · irreversible → `doRemoveDep()` |
| `approve` | `modalApprove()` L2950 | list ผลลัพธ์ 4 ข้อ → `doApprove()` |
| `reject` | `modalReject()` L2963 | reason **บังคับ** (`#rejectReason` + `#rejectErr`) → `doReject()` |
| **`reverse`** | **`modalReverse()` L2974** | **is-warning · undo-2 · reason บังคับ (`#reverseReason`+`#reverseErr`) · append-only · clawback line ถ้า pay=sent → `doReverse()`** |
| `doa` | `modalDoa()` L2991 | **DOA slot picker 2 ขั้น** — เลือก "คน" ต่อ slot (`DOA_SLOTS` L2242) → `confirmDoa()` |

---

## §7 · Interaction Spec

### ⭐ Esc chain (ลำดับจริงจาก handler)
1. **L1913** — `ssOnKey()` combobox: `else if(e.key === 'Escape'){ e.stopPropagation(); s.open=false; … }` → Esc **ปิดเฉพาะ dropdown** ก่อน (stopPropagation กันทะลุ · Rule #94 ข้อ3)
2. **L1775** — global `keydown`: `if(e.key === 'Escape'){ if(state.modal.open) closeModal(); else if(state.drawer.open) closeDrawer(); }` → **modal ก่อน drawer**

> ลำดับปิด: combobox → modal → drawer (modal ซ้อนบน drawer ได้ · closeModal คง lockScroll ถ้า drawer ยังเปิด L1752)

### Overlay lifecycle
- **openDrawer** L1698: set state → render → rAF add `.is-open` + `lockScroll(true)` + `trapFocus(dw)` + `guardOverlayAutoCombo()`
- **closeDrawer** L1712: remove `.is-open` + `releaseFocus` + `lockScroll(false)` + setTimeout 280ms reset state · patch L3250 reset `state.form` หลัง 290ms
- **openModal** L1723 / **closeModal** L1747: rAF add is-open + trapFocus(.modal) · closeModal คง scroll-lock เมื่อ drawer ยังเปิด (L1752) + setTimeout 200ms reset
- **scroll lock:** `lockScroll(on)` L2121 = toggle `body.is-overlay-open` (L76 `overflow:hidden`) — **มี**
- **focus trap:** `trapFocus()` L2123 / `releaseFocus()` L2142 — **มี**
- **focus/scroll restore:** `preserveRenderState()` L1995 / `restoreRenderState()` L2013 / `withRenderPreservation()` L2039 (Rule #29) — **มี**
- click-outside: user-menu L3218 · search-select L1915

### Positioning
- drawer = fixed right slide (translateX) · modal = fixed center scale · portal menu = fixed via `positionMenu()` L2108 (getBoundingClientRect) — portal ออก `#overlay-root` ให้เหนือ drawer (Rule #95)

---

## §8 · State-Driven UI Matrix

### Request status → pill + footer actions (`drawerRequestView` L2786-93)
| status | pill (reqPill) | header actions (ตาม persona) |
|---|---|---|
| draft | ร่าง | `ส่งอนุมัติ`(→submitDraftDoa) + `ยกเลิกคำขอ`(ถ้า canCancelReq) |
| pending | รออนุมัติ | `ไม่อนุมัติ` + `อนุมัติ` (เฉพาะ `canApprove()`) + `ยกเลิกคำขอ`(ถ้า canCancelReq) |
| approved | อนุมัติแล้ว | **`กลับรายการ`** (เฉพาะ `canApprove()` · OQ-WEL-01) |
| rejected | ไม่อนุมัติ | — (detail note is-danger + เหตุผล) |
| cancelled | ยกเลิก | — |
| revoked | ระงับ (พ้นสภาพ) | — (detail note is-warn + revokeReason) |
| **reversed** | **กลับรายการแล้ว** | — (detail note is-danger append-only L2812) |

### Governance gates (persona guards)
| ฟังก์ชัน | เงื่อนไข (L2254-61) | ผล |
|---|---|---|
| `canSeeValue()` / `canSeePerson()` | admin \|\| manager | มูลค่า/บุคคล — ไม่ผ่าน → `maskEl('RESTRICTED')` L2262 |
| `canSeeDependent()` | admin เท่านั้น | ผู้ติดตาม — ไม่ผ่าน → mask + ซ่อนปุ่มเพิ่ม |
| `canApprove()` | admin \|\| manager | อนุมัติ/ไม่อนุมัติ/**กลับรายการ**/ปิดใช้/สร้าง type · ทั้ง UI (ซ่อนปุ่ม) และ mutation guard (`สิทธิ์ไม่พอ`) |
| `canCancelReq(r)` | admin \|\| เจ้าของคำขอ (`r.empId===currentEmpId()`) | ปุ่มยกเลิก |

- **masking demo strip:** persona = admin(HR สวัสดิการ) / manager(หัวหน้า) / employee(พนักงาน) → `setRole()` L3215 · employee = สมชาย EMP-001 (L2260) · masking แสดง `•••••` (ชื่อ) / `maskEl` (lock icon + ข้อความ) ทั่วทั้ง P-02/P-03/P-04
- **pending-exposure line (OQ-WEL-03 · `reqBalanceTab` L2843):** note is-info "คำขอรออนุมัติอื่นของสิทธิ์นี้: **N ใบ** · รวม …" — **display-only ไม่ soft-reserve** · masked ตาม canSeeValue (L2850)

### Benefit edit → publish state machine (`submitBenefit` L3038)
- edit draft + กด primary → publish (ร่าง → มีผล) L3050 · edit active → **ออกเวอร์ชันใหม่** (active เดิม → archived + effTo=วันก่อนวันมีผลใหม่) L3056-62 · overlap guard `validateBenefit` L3021 (BR-03)

### Payroll-recurring section (FIX-07 · `renderBalance` L2552)
- แสดงเมื่อ benefit `unit==='percent'` & ไม่ ended · input % → `setPayrollPct()` L2636 (clamp 0–100) · pill `ส่งเข้ารอบเงินเดือนถัดไป` · **display-only hook → Payroll F065**

### Approval flow (`doApprove` L3135)
- one-step advance: current step → approved · ไม่ใช่ขั้นสุดท้าย → next=current (r.status คง pending) · ขั้นสุดท้าย → r.status=approved + pay=pending + **re-check eligibility+เพดาน ก่อน finalize (FIX-02)** L3142

---

## §9 · Microcopy (verbatim)

### Toasts (`showToast` — 27 ข้อความ · variant)
| variant | ข้อความ |
|---|---|
| warning | กรุณากรอกข้อมูลให้ครบถ้วน |
| success | กลับรายการแล้ว · คืนสิทธิ์และมูลค่าให้พนักงาน · แจ้งเตือนผู้ยื่น |
| warning | กลับรายการได้เฉพาะคำขอที่อนุมัติแล้ว |
| warning | คงเหลือไม่พอ ณ วันอนุมัติ |
| warning | ตรวจสอบข้อมูลผู้ติดตาม |
| success | บันทึกการแก้ไข (ออกเวอร์ชันใหม่) แล้ว |
| info | บันทึกร่างแล้ว |
| info | บันทึกสัดส่วน % (mock · display-only) — ส่งเข้ารอบเงินเดือนถัดไป |
| success | บันทึกไม่อนุมัติ · แจ้งเตือนผู้ยื่น |
| success | ปิดใช้ (เก็บถาวร) แล้ว |
| success | ยกเลิกคำขอแล้ว |
| warning | ยกเลิกได้เฉพาะร่าง/รออนุมัติ |
| warning | ยื่นไม่ได้: |
| success | ลบผู้ติดตามแล้ว |
| info | ศูนย์แจ้งเตือนอยู่ที่ระบบ Notification (F-NOTIFY) — นอกขอบเขต feature นี้ |
| success | สร้างประเภทสวัสดิการสำเร็จ |
| warning | สิทธิ์ไม่พอ |
| success | ส่งอนุมัติแล้ว · แจ้งเตือน HR อัตโนมัติ |
| success | อนุมัติขั้น |
| success | อนุมัติแล้ว · ตัดคงเหลือ + บันทึกมูลค่าเข้า 7C EC |
| warning | อนุมัติได้เฉพาะคำขอสถานะรออนุมัติ |
| warning | อนุมัติไม่ได้: |
| success | เผยแพร่ประเภทสวัสดิการแล้ว (ร่าง → มีผล) |
| success | เพิ่มผู้ติดตามแล้ว |
| warning | เลือกผู้อนุมัติให้ครบทุกขั้น |
| warning | เลือกพนักงานก่อนบันทึกร่าง |
| success | แล้ว · ส่งต่อขั้นถัดไป |

> หมายเหตุ: `ยื่นไม่ได้:` / `อนุมัติไม่ได้:` / `อนุมัติขั้น` / `แล้ว · ส่งต่อขั้นถัดไป` เป็นสตริงที่ต่อกับตัวแปร (เหตุผล/เลขขั้น) ใน `submitRequestForm` L3109 · `doApprove` L3145/3162
> download mock: `ดาวน์โหลดไฟล์ (mock)` (L2841) · stub เมนูข้างเคียง: `"…" เป็น feature ข้างเคียง (context) — อยู่นอกขอบเขตรอบนี้` (`stubNav` L3216)

### Empty states (`emptyStateHTML` L1955) — verbatim (title / desc)
| title | desc |
|---|---|
| ไม่พบรายการที่ค้นหา | ลองปรับคำค้นหรือล้างตัวกรอง |
| ยังไม่มีคำขอ | เริ่มต้นด้วยการสร้างคำขอใช้สิทธิ์แรก |
| เลือกพนักงานเพื่อดูสิทธิ์คงเหลือ | ค้นหาแล้วเลือกพนักงาน 1 คน เพื่อดูสิทธิ์ · โควตา · ยอดใช้ · คงเหลือ ต่อประเภท และรายชื่อผู้ติดตาม |
| ไม่พบข้อมูลตามตัวกรอง | ยังไม่มีคำขอที่อนุมัติแล้วตรงกับเงื่อนไข |
| ไม่มีไฟล์แนบ | คำขอนี้ยังไม่มีเอกสารหลักฐานแนบ |

### Key inline messages (verbatim)
- **reverse modal** (L2977): "กลับรายการคำขอ {id}?" · "คำขอที่อนุมัติแล้วไม่ถูกลบ — บันทึกการกลับรายการแบบ append-only" · reason placeholder "ระบุเหตุผล เช่น อนุมัติผิดคน / ยอดผิด / เอกสารเป็นเท็จ" · error "กรุณาระบุเหตุผล"
- **reversed detail note** (L2812): "**กลับรายการแล้ว:** {reason} — คืนสิทธิ์การใช้ + คืนมูลค่าเข้าเงินได้ (7C · EC) … (ข้อมูลเดิมคงไว้ · append-only)"
- **approve modal** (L2954): "อนุมัติคำขอ {id}?" · list: ตัดคงเหลือ · บันทึกมูลค่า … เข้า 7C · EC · ส่งสถานะจ่ายให้ปลายทาง Payroll/Expense (เชื่อมปลายทาง · ไม่จ่ายเอง) · แจ้งเตือนผู้ยื่นอัตโนมัติ
- **DOA modal** (L3003): "ส่งอนุมัติคำขอ {id}" · "เลือกผู้อนุมัติแต่ละขั้น (สายจาก DOA · ไม่มีวงเงิน · resolve แล้ว freeze)" · note "สายอนุมัติมาจาก **DOA กลาง** (GET /doa/resolve) — เลือก "คน" … ไม่ hardcode"
- **eligibility notes** (`reqCalcHtml` L2758): บล็อก "**ยื่นไม่ได้:** {reason}" · "**เกินคงเหลือ:** คงเหลือ … ตัดคงเหลือไม่ได้" · ผ่าน "มีสิทธิ์ · คงเหลือ **{rem}** (ปีสิทธิ์ 2569) — ตัดคงเหลือเมื่ออนุมัติเท่านั้น"

---

## §10 · Data Binding & BACKEND anchors

> HTML ใช้ mock in-memory (`BENEFITS` L2185 · `EMPLOYEES` L2171 · `REQUESTS` L2197 · `APPROVERS` L2235 · `DOA_SLOTS` L2242) — ไม่มี `// BACKEND:` comment marker แต่ทุก action mock มีจุด plug ชัดเจน

| UI action (fn) | plug → FRD API |
|---|---|
| list registry (`renderRegistry`) | GET `/benefit-types` (API-01) |
| create/edit benefit (`submitBenefit` L3038) | POST `/benefit-types` (API-02) · PUT `/benefit-types/:id` (API-04 · publish/version) |
| archive (`doArchiveBenefit` L3089) | POST `/benefit-types/:id/archive` (API-05) |
| add/remove dependent (`submitDependent` L3199 / `doRemoveDep` L3211) | POST/DELETE `/employees/:empId/dependents` (API-06/07) |
| list/detail requests (`renderRequests`/`drawerRequestView`) | GET `/requests` (API-08) · GET `/requests/:id` (API-10 · 4-tab payload) |
| create/draft (`makeRequest` L3116) | POST `/requests` (API-09) |
| submit + DOA (`confirmDoa` L3124) | POST `/requests/:id/submit` (API-11) · GET `/doa/resolve?feature=F-HR-WELFARE` (freeze chain) |
| approve (`doApprove` L3135) | POST `/requests/:id/approve` (API-12 · ENG-WEL-02/ENG-CSQ/ENG-NOTIFY) |
| reject (`doReject` L3166) | POST `/requests/:id/reject` (API-13) |
| cancel (`doCancelRequest` L3191) | POST `/requests/:id/cancel` (API-14) |
| **reverse (`doReverse` L3175)** | **POST `/requests/:id/reverse` (API-15 · EC reverse + clawback flag)** |
| balance (`renderBalance`) | GET `/balance?employee_id=` (API-16 · + exposure + ผู้ติดตาม) |
| report (`renderReport`) | GET `/report?type=&group=&from=&to=` (API-17) |
| payroll % (`setPayrollPct` L2636) | display-only hook → Payroll **F065** (อ่านค่าตอนปิดงวด) |
| joiner/leaver | GET `/onboard/employment-window/resolve` (soft ref) |
| person combobox | GET `/employees` (Employee Master #102 soft ref) |

- masking (`canSee*`) enforce ที่ backend (RLS/role) — FE = display guard เท่านั้น (BR-08)
- append-only audit (`buildAudit` L2865) → T_welfare_audit_log (BR-07) · snapshot person/company/config_version (BR-10)

---

## §11 · Traceability (Brief ↔ FRD ↔ HTML) + Drift Log

| Brief § | FRD (P-xx / API / BR / FN) | HTML anchor |
|---|---|---|
| §2 route registry | P-01 · `#/welfare/registry` | `renderRegistry()` L2383 |
| §2 route requests | P-02 · `#/welfare/requests` | `renderRequests()` L2428 |
| §2 route balance | P-03 · `#/welfare/balance` | `renderBalance()` L2502 |
| §2 route report | P-04 (Pattern K · view only) | `renderReport()` L2583 |
| §4 create benefit | API-02 · FN-01 | `submitBenefit()` L3038 |
| §4/§8 edit=version | API-04 · BR-03 · FN-02/03 | `validateBenefit()` L3021 |
| §6 archive | API-05 · EC-05 · FN-04 | `doArchiveBenefit()` L3089 |
| §4 dependent | API-06/07 · FN-05/06 | `drawerDependentForm()` L2880 |
| §4 request create | API-09 · BR-01/02 · FN-07/08 | `drawerRequestForm()` L2716 |
| §6 DOA submit | API-11 · BR-04 · FN-10 | `modalDoa()` L2991 · `confirmDoa()` L3124 |
| §8 approve | API-12 · BR-02/05/09 · FN-11 | `doApprove()` L3135 |
| §8 reject | API-13 · FN-12 | `doReject()` L3166 |
| §8 cancel | API-14 · BR-DOA-7 · FN-13 | `doCancelRequest()` L3191 |
| **§8 reverse** | **API-15 · BR-11 · EC-06/11 · FN-14 · OQ-WEL-01** | **`doReverse()` L3175 · `modalReverse()` L2974** |
| §8 balance+exposure | API-16 · BR-12 · FN-16 · OQ-WEL-03 | `reqBalanceTab()` L2843 |
| §4 report | API-17 · FN-19 | `renderReport()` L2583 |
| §8 masking | BR-08 · FN-94 | `canSee*()` L2255-57 · `maskEl()` L2262 |
| §8 leaver/joiner | BR-06 · FN-18 | `eligibility()` L2278 · balance notes L2519/2537 |
| §8 payroll % | FN-16/F065 (FIX-07) | `setPayrollPct()` L2636 |

### ⚠️ Drift Log
| # | ชนิด | รายการ | หมายเหตุ / ข้อเสนอ |
|---|---|---|---|
| D-1 | HTML-only | **payroll-recurring % section** (`setPayrollPct` L2552) | display-only surface ของ Payroll F065 — FRD ระบุเป็น hook/soft-ref ไม่มี API ของ welfare เอง · ตรงเจตนา (ไม่ block) |
| D-2 | HTML-only | toast `ศูนย์แจ้งเตือนอยู่ที่ระบบ Notification (F-NOTIFY) — นอกขอบเขต feature นี้` (L1562) | ยืนยัน notification นอก scope (ENG-NOTIFY external · 02_API) — สอดคล้อง |
| D-3 | FRD-only | EC-07..EC-14 (concurrent lock · idempotency · permission mid-flight · fiscal reset · attachment policy) | เป็น backend contract (`[AI-DEFAULT]`) — HTML mock ไม่จำลอง · dev ต้อง implement ฝั่ง server (ไม่ใช่ UI gap) |
| D-4 | note | `.modal-backdrop` z = `--z-portal`(60) ไม่ใช่ backdrop(50) | จงใจ (แก้ latent BASE-KIT U01 · L1111) — ระบุใน §1/§6 ป้องกัน dev ตั้งผิด |
| D-5 | note | route extractor เห็น hash เดียว (`welfare`) | จริง — feature ใช้ base route เดียว + 4 tabs (segment `/registry|requests|balance|report` · `currentTab()` L2310) · ไม่ใช่ 4 route แยก |

**สรุป: ไม่มี business drift ที่ทำให้ HTML ขัด FRD** — drift ทั้งหมดเป็น display-only surface, cross-module hook, หรือ backend-contract ที่ mock ไม่จำลอง

---

## §12 · Diff จากเวอร์ชันก่อน

— ไม่มี HTML เวอร์ชันก่อนให้เทียบ (บรีฟ AS-BUILT รอบแรก · N/A)

---

## §13 · 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)

> ที่เดียวที่อนุญาตให้คิดเอง (R1) — ต่อไปนี้ **ไม่มีในจอ** เป็นข้อเสนอให้ทีมพิจารณา ไม่ใช่สเปคที่ต้องทำ

1. **Report export** — P-04 ไม่มีปุ่ม export/print (ตรง NS-5) · ถ้าธุรกิจต้องการส่งออก ควรยกเป็น enhancement (ยิง OQ ก่อน)
2. **Reverse guard ซ้อน** — ปัจจุบัน `doReverse` block reversed→reverse โดยธรรมชาติ (VR-11/EC-11) · หากเพิ่ม audit "พยายาม reverse ซ้ำ" จะช่วย forensics
3. **Exposure → soft-reserve** — ปัจจุบัน pending-exposure เป็น display-only (OQ-WEL-03) · หากธุรกิจต้องการกันยอดจริง ต้องเปลี่ยนเป็น reserve model (กระทบ concurrency EC-07)
4. **attachment validation** — upload เป็น mock (`mockUpload` L2776) · จริงต้องมี type/size/virus policy (EC-14 deferred)
