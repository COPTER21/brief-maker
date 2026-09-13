# UI Brief — F-MKT-CONSENT · F058 · ความยินยอม PDPA (Consent Management)

> **EXTRACTION-BASED (Iron Rule R1)** — ทุกบรรทัดในบรีฟนี้ trace กลับหา selector / function / ข้อความจริงใน `consent-pdpa.html` ได้
> อ้าง `Lxxxx` = เลขบรรทัดใน HTML · ข้อเสนอที่ไม่มีในจอ อยู่ท้ายไฟล์ §13 เท่านั้น
> คู่กับ: **HTML (source of truth)** + **FRD Pack** (ระบบ) + บรีฟนี้ (design intent)
> 🔵 **สถาปัตยกรรมสำคัญ:** ทั้งฟีเจอร์ = **เมนูเดียว** `#navConsent` (#104) · H1 = **"ความยินยอม PDPA" คงที่ทุกแท็บ** (L2385) · ภายในสลับ **4 route-tab** (`#/consent/<tab>` — hash-based refresh-safe) · **มุมมองผู้รับ** = surface เต็มจอนอก shell (z=`--z-recipient` 70)

---

## §0 · Document Control + Pairing

| | |
|---|---|
| Feature | F-MKT-CONSENT · F058 · ความยินยอม PDPA (Consent Management) · plan `Marketing · W1 · dec=["csq"] · dep=""` (standalone) |
| HTML source | `outputs/F-MKT-CONSENT/consent-pdpa.html` · `<title>` = "ความยินยอม PDPA · F-MKT-CONSENT · CUBE NATIVE" (L6) · ~3080 บรรทัด · BASE-KIT v6.4 (L22) |
| Archetype | **Pattern A (list-view) ×3 + Pattern K (read-only simulator) ×1** ในเมนูเดียว 4 tab + **Full-screen recipient surface** (P-05) · เนื้อหา = **เอกสารอัปโหลด versioned** ต่อวัตถุประสงค์ (ไม่ใช่ข้อความพิมพ์) |
| FRD Pack | `FRD_Pack/` (00_OVERVIEW · 01_UI · 02_API · 03_LOGIC · 04_DB · 05_RULES · 06_TESTS · 07_LOCKED_DECISIONS · INDEX) — **paired** |
| BRD | `BRD_F-MKT-CONSENT.md` (Gate APPROVED · upload model = DECLARED-01 · 6 OQ) |
| FUNCTION_CHECKLIST | `FUNCTION_CHECKLIST_F-MKT-CONSENT.md` — 20 FN บวก + FN-40 (10 ข้อห้ามมี) · e2e 32/32 · FN 20/20 |
| Declaration | **csq** ✅ (`CSQ_BRIEF_F-MKT-CONSENT.md` · declare-only 7 events → 7C Engine · ห้ามประกาศ OC/DC/SC) · doa/doccfg/ntf = ไม่เลือก |
| HTML เก่า (diff) | — ไม่มี (บรีฟนี้เป็น full AS-BUILT รอบแรก · §12 = N/A) |
| Gate สถานะ | qc-ux PASS · coverage R1 PASS (FN 20/20) · e2e 32/32 · W1 fixed (≥40) |
| Drift | บันทึกใน §11 — z-token label mapping (FRD vs observed), base-kit residual overlays, OQ cross-module · **ไม่มี business drift ที่ block** |
| Carry OQ | **OQ-03/OQ-04 BLOCKING** (id-verify จริง, ขึ้นทะเบียน F143) · OQ-CSQ-01/02 · BR-21/22 (→ PROPOSALS step 12) |

**สถาปัตยกรรม:** Single-file vanilla-JS SPA · state-driven `render()` (L2335) · innerHTML rebuild + Render Preservation (Rule #29 · `preserveRenderState()`/`restoreRenderState()` L2337/2370) · **4 tab สลับด้วย hash route** `#/consent/<tab>` (`getRoute()` L1784 · `navigate()` L1789 · refresh-safe) · combobox = **custom `.combo`** (`cx_*` ids · DSP-02/03/04 · L2237+ แทน searchSelect ของ BASE-KIT) · Lucide icon multi-CDN fallback unpkg→jsdelivr→cdnjs pin 0.469.0 (L1725–1749) · ฟอนต์ Noto Sans Thai (Google) + Satoshi (Fontshare · L11–12).

---

## §1 · Design Tokens AS-BUILT (`:root` L24–57 + z-block L1356–1365)

### Palette (CUBE CI v2.0 Warm Light rebrand · L25–41)
| token | ค่า | ใช้ |
|---|---|---|
| `--c-navy` / `--c-navy-2` | `#111111` | sidebar · heading |
| `--c-primary` / `--c-primary-hover` | `#FF3B30` / `#E62E24` | ปุ่มหลัก · doc-link · stat icon · ptab active |
| `--c-teal` / `--c-teal-light` | `#FF9A1F` / `#FFB763` | accent · demo-strip brand icon |
| `--c-ink` | `#111111` | ตัวอักษรหลัก |
| `--c-mute` / `--c-mute-2` / `--c-mute-3` | `#54565C` / `#73757B` / `#9A9CA2` | ตัวอักษรรอง / meta / placeholder |
| `--c-line` / `--c-line-2` / `--c-line-3` | `#DEDAD4` / `#E9E5E0` / `#F1EEEA` | เส้น / card border / divider |
| `--c-bg-off` | `#FAF8F5` | พื้นหลังหน้า · thead · row hover |
| `--c-success` / `--c-warning` / `--c-danger` | `#1F9D55` / `#E8870F` / `#E62E24` | pill สถานะ · verdict allow/deny |

### Type scale (fixed · Iron Rule L44–52)
`--fs-h1:22px` · `--fs-h2:17px` · `--fs-h3:15px` · `--fs-body:14px` · `--fs-sub:13px` · `--fs-meta:12px` · `--fs-cap:11px` · `--fs-kpi:28px`
font stack (L79): `'Satoshi','Noto Sans Thai',system-ui,sans-serif` · body 14px · line-height 1.5 · ตัวเลข stat ใช้ `'Noto Sans Thai'` (L480)

### Spacing / Radius (L53–56)
`--sp-xs:4px --sp-sm:8px --sp-md:12px --sp-lg:20px --sp-xl:28px` · `--r-xs:4px --r-sm:6px --r-md:8px --r-lg:12px --r-full:999px`

### Shell dims
`--sidebar-w:232px` (L42) · `--shell-h:52px` (L43) · `scrollbar-gutter:stable` (L64 · Rule #35 กัน jank) · scrollbar 5px (L69) · `.drawer` responsive `min(920px,100vw)` @≤bp (L348) · standard width ที่ตั้งใน `render()` (`.drawer.standard`)

### ⭐ Z-INDEX MAP (สูง → ต่ำ · L1356–1365) + DSP override
| token | ค่า | ใช้กับ | หมายเหตุ |
|---|---:|---|---|
| `--z-toast` | **90** | `.toast` (L1709) | สูงสุด — เห็นเหนือทุกอย่าง |
| `--z-pop` | **80** | `.combo-list` (portal · L1472) | combobox list ไป `#overlay-root` → ลอยเหนือ modal/drawer (DSP-03) · comment L1364 "เหนือ modal(60) เมื่อ portal" |
| `--z-recipient` | **70** | `.recipient-root` (L1402) | มุมมองผู้รับ (mock ลิงก์) — surface แยกเหนือ drawer/modal ของ ERP |
| `--z-portal` | **60** | portal menu context · **`.modal-backdrop` override เป็นค่านี้** (L1368) | ⭐ DSP-01 — modal เปิด **เหนือ drawer(55)** |
| `--z-drawer` | **55** | `.drawer` (L1370) | ลิ้นชัก view/create |
| `--z-backdrop` | **50** | `.drawer-backdrop` · `.ss-list` (base-kit residual) | |
| `--z-dropdown` | **40** | `.user-menu` · `.menu-fixed` (base-kit residual) · thead sticky ที่ table-wrap | |
| `--z-sticky` | **30** | `.shell-bar` · thead sticky · **`.demo-strip`** (L1495) | demo-strip = persona switch มุมซ้ายล่าง |
| `--z-shell` | **20** | `.sidebar` (L105) | |

> ⭐ **DSP-01 (L1368):** `.modal-backdrop{ z-index: var(--z-portal) }` = **60 > drawer 55** — จงใจให้ modal (document viewer `viewPolicy`, withdraw, new-version, close-purpose) โผล่ **ทับ** drawer ได้ (pre-wire กัน bug in-drawer modal ที่ qc-ux เคยพลาด — precedent DSP-01)
> ⭐ **DSP-03 (L1472 + `comboPosition` L2285):** `.combo-list` portal ไป `#overlay-root` (L1671) ที่ z=`--z-pop`(80) + flip-up เมื่อพื้นที่ล่างไม่พอ — ให้ combobox list ลอยเหนือทั้ง modal(60) และ drawer(55) ไม่ถูก clip

---

## §2 · Route Map (⚠️ hash-based · 4 tab = 1 เมนู)

> **1 feature = 1 เมนู (#104):** ทั้ง feature = เมนูเดียว "ความยินยอม PDPA" (`#navConsent` L1610) · ภายในสลับ **4 route-tab** ด้วย hash `#/consent/<tab>` — **refresh-safe** (ต่างจาก ESS/welfare) · **H1 คงที่ "ความยินยอม PDPA" ทุกแท็บ** (L2385) — สิ่งที่เปลี่ยนต่อ tab คือ `.ph-sub` + breadcrumb + `.ph-actions` + body

### 2.1 · Router (observed · L1784–1791 · refresh-safe)
- `getRoute()` L1784 = `location.hash.replace('#/','')` · default `home` เมื่อ hash ว่าง/`#`/`#/`
- `navigate(route)` L1789 = set `location.hash = '#/' + route`
- ใน `render()` L2338–2343: `route.indexOf('consent/')===0` → `tab = route.split('/')[1]` · `route==='consent'||'home'` → `registry` · tab ที่ไม่อยู่ใน `['registry','requests','purposes','resolve']` → fallback `registry`
- **hashchange** ผูก `render()` (base-kit late-binding) — refresh หรือ paste URL `#/consent/purposes` เข้าตรง tab ได้

### 2.2 · 4 tabs (`pageHeadHTML` L2375 · def L2380–2381)
| tab | route | ptab label | icon | render fn | `.ph-sub` (verbatim L2376–2379) |
|---|---|---|---|---|---|
| `registry` (default) | `#/consent/registry` | ทะเบียน | `table-2` | `registryBody()` L2427 | ทะเบียนความยินยอมทั้งหมด · กรองตามเจ้าของข้อมูล วัตถุประสงค์ ช่องทาง |
| `requests` | `#/consent/requests` | คำขอ | `send` | `requestsBody()` L2493 | คำขอความยินยอมและการส่งแต่ละครั้ง |
| `purposes` | `#/consent/purposes` | วัตถุประสงค์ | `target` | `purposesBody()` L2520 | วัตถุประสงค์ · นโยบาย (เวอร์ชัน) · สถิติความครอบคลุม |
| `resolve` | `#/consent/resolve` | ตรวจสิทธิ์ | `shield-question` | `resolveBody()` L2540 | ตรวจสิทธิ์การส่ง — จำลองคำตอบเหมือนที่ API /consent/resolve จะให้ |

- ptab render `.ptab` L2382–2383 → `onclick="navigate('consent/<tab>')"` · active = `is-active`
- breadcrumb `#bcCurrent` = `"ความยินยอม PDPA · " + bcMap[tab]` (L2348–2349 · bcMap: ทะเบียน/คำขอ/วัตถุประสงค์/ตรวจสิทธิ์) — **breadcrumb เปลี่ยน แต่ H1 ไม่เปลี่ยน**

### 2.3 · มุมมองผู้รับ (P-05 · ไม่ใช่ route — เปิดจากในคำขอ)
- `openRecipientView(reqId)` L2759 = surface เต็มจอ (`.recipient-root` #recipientRoot L1706 · z=70) · **ไม่มี hash** · เปิดจากปุ่มใน reqView drawer (L2708) · ปิด `closeRecipientView()` L2765 (Esc = ปิดตัวแรกสุด · L1844)

---

## §3 · Layout Shell

| region | selector / anchor | หมายเหตุ |
|---|---|---|
| Sidebar | `.sidebar` #sidebar (fixed · w=`--sidebar-w`232px · bg `#111111` · z=`--z-shell`20 L105) | โมดูล "การตลาด" > **item เดียวของฟีเจอร์** `.sb-item#navConsent[data-feature="consent"]` L1610 → `navigate('consent/registry')` · set `.is-active` ใน render (L2347) |
| Sibling menus | `.sb-item` onclick `decorativeNav()` (L1613/1614/1623/1624/1633/1634/1643) | "แคมเปญส่งข้อความ · จดหมายข่าว · ทะเบียนลูกค้า · เคสบริการ · ใบเสนอราคา · ใบสั่งขาย · ข้อมูลองค์กร" = **context only** · คลิก → toast "เมนูนี้เป็นบริบทของโมดูลอื่น (เดโมไม่รวมขอบเขต)" |
| Module toggle | `toggleModule(headerEl)` L1774 | collapse ผ่าน `data-expanded` (Rule #27) |
| Topbar | `.shell-bar` L1651 (z=`--z-sticky`30) | nav-toggle (mobile L1652) · breadcrumb "การตลาด › ความยินยอม PDPA · <tab>" (L1653–1657) |
| Notif bell | `.icon-btn` L1659 | มี `.notif-dot` (static · ไม่ wire — ฟีเจอร์นี้ **ไม่มี notification** ตาม 01_UI §1.6) |
| User chip | `.user-chip` L1660 | "สุดา ใจดี" / `.user-role#userRole` (sync ตาม persona L3035) / avatar "สด" |
| Page host | `.content #page-content` L1665–1666 | `render()` เขียน `pageHTML(tab)` ลงตรงนี้ (L2351) |
| Overlay host | `#overlay-root` L1671 | portal สำหรับ `.combo-list` (DSP-03) |

**Page header (`pageHeadHTML` L2385):** `.ph` — `.ph-title-row > h1.ph-title` = **"ความยินยอม PDPA" (คงที่)** + `.ph-sub` (ต่อ tab) + `.ph-actions` = `headActions(tab)` L2388 (ปุ่มตาม persona · ดู §8) ตามด้วย `.ptabs` (4 ปุ่ม).

---

## §4 · Page Anatomy (ต่อ tab)

### P-01 · ทะเบียน (`registryBody` L2427) — FN-13/14/16
- **stat cards (toggle filter)** L2432–2434 `.stat.is-filter` × 4: ทั้งหมด (`database`) · ยินยอมอยู่ (`check-circle-2` · `isActive`) · ใกล้หมดอายุ (`clock-alert` · `nearExpiry` v='near') · ถอนแล้ว (`undo-2`) — คลิก → `toggleStat(k,v)` L2424 (คลิกซ้ำ = ล้างกลับ 'all')
- **Filter bar:** search + status + channel + purpose (`setFilter(k,v)` L2423 · `resetFilters()` L2425 · `state.filters` L2120)
- **Toolbar actions (`headActions` registry):** ปุ่ม **ส่งออก CSV** (`exportCsv()` L2480) + **สร้างคำขอ** (`openReqCreate({})` · เฉพาะ `perm.reqCreate`)
- **Data Table triple** (`filteredConsents()` L2403 → rows) — เจ้าของข้อมูล × วัตถุประสงค์ × ช่องทาง + `statusPill(eff)` (L2472) + วันหมดอายุ · row คลิก → `openConsentView(id)` L2903 · sort `sortBy(col)` L2422
- **Empty:** `emptyStateHTML` → title **"ไม่พบความยินยอม"** / desc "ลองล้างตัวกรอง หรือสร้างคำขอความยินยอมใหม่"

### P-02 · คำขอ (`requestsBody` L2493) — FN-05/06/07/08/09/10/11
- list คำขอ (`state.requests` L2214) + `reqStatusPill(s)` L2226 (ร่าง/รอตอบ/ตอบแล้ว/คำขอหมดอายุ) · row → `openReqView(id)` L2675
- **Toolbar action:** **สร้างคำขอ** (`openReqCreate({})` · เฉพาะ `perm.reqCreate`)
- **Empty:** title **"ยังไม่มีคำขอ"** / desc "สร้างคำขอความยินยอมให้ลูกค้า"

### P-03 · วัตถุประสงค์ (`purposesBody` L2520) — FN-01/02/03/04
- การ์ด/แถว purpose (`state.purposes` L2167) + `purposeStats()` (ยินยอมอยู่/ถอน/หมดอายุ/%ครอบคลุม) · row → `openPurView(code)` L2867
- **Toolbar action:** **สร้างวัตถุประสงค์** (`openPurCreate()` · เฉพาะ `perm.purpose`=dpo) · ไม่มีสิทธิ์ → chip **"เฉพาะ DPO แก้ไขได้"** (L2392)
- **Empty:** title **"ไม่พบวัตถุประสงค์"** / desc "ลองค้นด้วยคำอื่น"

### P-04 · ตรวจสิทธิ์ (`resolveBody` L2540) — FN-19/20 · **read-only simulator (Pattern K)**
- `.rz-layout` 2 คอลัมน์: ซ้าย = ฟอร์ม 3 combobox (`rzSubject`/`rzPurpose`/`rzChannel`) + ปุ่ม **ตรวจสิทธิ์การส่ง** (`runResolve()` L2552) · field-help "ค่าเริ่มต้นคือ **ส่งไม่ได้** … การไม่ตอบ ≠ ปฏิเสธ (BR-08)"
- ขวา = result card (`resolveResultHTML` L2579): badge `ส่งได้`/`ส่งไม่ได้` + `HTTP 200` chip + เหตุผล + `statusPill` + **ตัวอย่าง JSON** (`jsonColor()` L2593 · ฟิลด์ล็อก BR-19/20) — **ไม่มี mutation** (LOCK #9)
- **Empty (ก่อนกรอก):** `.rz-empty` "เลือกเจ้าของข้อมูล · วัตถุประสงค์ · ช่องทาง แล้วกดตรวจสิทธิ์" (L2542)

### P-05 · มุมมองผู้รับ (`recipientViewHTML` L2780) — FN-10/11 · **full-screen surface**
- `.recipient-root` (fixed inset0 · z=`--z-recipient`70 · bg `#EEF1F5` · **ไม่มี sidebar/shell**)
- `.rcp-simbar` (แถบ "จำลอง — นี่คือหน้าที่เจ้าของข้อมูลเห็นเมื่อเปิดลิงก์ (ไม่ใช่การส่งจริง)" + ปุ่ม `.rcp-close` "ปิด")
- `.rcp-brandcard`: "CUBE Consent" + h1 "คำขอความยินยอม PDPA" + subject chip
- **ต่อวัตถุประสงค์** `.rcp-pcard`: ชื่อ + "เอกสารเวอร์ชันปัจจุบัน vN" + **doc toggle** (`toggleRecipientDoc(code)` L2771 → ปุ่ม "อ่านเอกสาร · <docName>" ↔ `.doc-frame` body + ปุ่ม "ย่อ") + `.rcp-choices` (ยินยอม/ไม่ยินยอม · `setRecipientChoice` L2769)
- `.rcp-verify` checkbox (`toggleRecipientVerify` L2770) "ฉันคือเจ้าของข้อมูลและได้อ่านเอกสารแล้ว" / "ยืนยันตัวตน (ต้นแบบ) — จำเป็นก่อนส่งคำตอบ"
- ปุ่ม `.rcp-submit` "ยืนยันการตอบ" → `submitRecipient()` L2772

---

## §5 · Component Inventory (anchor + states)

### Page tabs (`.ptab` · `pageHeadHTML` L2382)
- โครง: `.ptabs > button.ptab` (icon + label) · **states:** default / `.is-active` (tab ปัจจุบัน) / hover (base-kit)

### Stat / filter cards (`.stat.is-filter` · L2432)
- โครง: `.stat-label`(icon+label) + `.stat-value` · **states:** default / hover (L469) / `.is-on` (ตัวกรองที่เลือก) · toggle ซ้ำ = ล้าง

### Status pills (`statusPill(eff)` L2229 · `pill(text,variant)`)
| eff (ทะเบียน) | label | variant |
|---|---|---|
| `never_asked` | ยังไม่เคยขอ | muted |
| `pending` | รอตอบ | warning |
| `granted` | ยินยอม | success |
| `declined` | ไม่ยินยอม | danger |
| `withdrawn` | ถอนแล้ว | muted |
| `expired` | หมดอายุ | warning |

| request status (`reqStatusPill` L2226) | label | variant |
|---|---|---|
| `draft` | ร่าง | muted |
| `pending` | รอตอบ | warning |
| `answered` | ตอบแล้ว | success |
| `expired` | คำขอหมดอายุ | muted |

### Custom combobox (`.combo` · `comboHTML(key,ph)` L2239 · ids `cx_<key>[_part]` L2238)
- แทน searchSelect ของ BASE-KIT — ประกาศ `CB={}` L2237 · list `.combo-list` portal (DSP-03)
- **states:** closed / open (`comboOpen` L2257) / typing filter (`comboInput` L2258 + `<mark>` highlight L2273) / `.is-active` highlighted item / empty "ไม่พบรายการ" (L2274) / picked (`comboPick` L2259 · blur ก่อน onSelect · DSP-02)
- ใช้ที่: resolve (rzSubject/rzPurpose/rzChannel) · reqCreate (subject/channel) · reqView (resendCh)

### doc-link / document viewer (`.doc-link` L1389 · `.doc-frame` L1394)
- `.doc-link` = **ชื่อไฟล์เอกสารที่คลิกได้** (`viewPolicy(code[,ver])` L2967 → เปิด modal `policyModal` L2968 z=60 เหนือ drawer) · icon = `docIcon(docType)` L2182
- `.doc-frame` = กล่องแสดง body เอกสาร (ในผู้รับ view L2794 + policy modal) · **เนื้อหา = เอกสารอัปโหลด versioned** (`curDoc(p)` L2180 · currentVer)

### Read-only table
- row `.is-clickable` → `openConsentView`/`openReqView`/`openPurView` · **ไม่มี** inline-edit/pagination ที่ wire (state.pagination มีแต่ไม่ใช้)

### Buttons — inventory (verbatim)
`ส่งออก CSV` · `สร้างคำขอ` · `สร้างวัตถุประสงค์` · `ตรวจสิทธิ์การส่ง` · `คัดลอก` · `ดาวน์โหลด QR` · `ดาวน์โหลดเอกสาร` · `ส่งซ้ำ` · `ส่งทาง<ช่องทาง> (จำลอง)` · `เปิดมุมมองผู้รับ (จำลองลิงก์)` · `ออกเวอร์ชันใหม่` · `ปิดวัตถุประสงค์` · `ถอนความยินยอม` · `สร้างคำขอต่ออายุ` · `ขอความยินยอมใหม่ (N รายที่กระทบ)` · `อ่านเอกสาร · <docName>` / `ย่อ` · `ยินยอม` / `ไม่ยินยอม` · `ยืนยันการตอบ` · `ดู` · `ปิด` · `เข้าใจแล้ว`(modal)

---

## §6 · Overlay Registry (11 overlays · dismiss rules + z)

| overlay | selector / anchor | position / เปิด | ปิด (dismiss) | z |
|---|---|---|---|---|
| Sidebar | `.sidebar` #sidebar L105 | fixed 232px · เปิดตลอด (mobile `.open` toggle L1652) | — | `--z-shell` 20 |
| **demo-strip** | `.demo-strip` #demoStrip L1495/L1674 | **fixed มุมซ้ายล่าง** · เปิดตลอด (prototype only #105) | — (persona switch เท่านั้น) | `--z-sticky` 30 |
| User menu | `.user-menu` (base-kit L307) | absolute ใต้ chip | click-outside (base-kit) | `--z-dropdown` 40 |
| Portal menu | `.menu-fixed` (base-kit L374) | fixed portal | `closeOverlay()` (base-kit) | `--z-dropdown` 40 |
| Search list | `.ss-list` (base-kit L576) | absolute overlay | base-kit | `--z-backdrop` 50 |
| **Drawer backdrop** | `.drawer-backdrop` #drawerBackdrop L1693 | fixed inset0 | **คลิก → `closeDrawer()`** L1693 | `--z-backdrop` 50 |
| **Drawer** | `.drawer` #drawer L878/L1694 | fixed right · `min(920px,100vw)` (L348) · slide translateX | ปุ่ม X (`dwHead` L2606) · ปุ่ม "ปิด" (`dwFoot`) · Esc · คลิก backdrop | `--z-drawer` 55 |
| **Modal backdrop** | `.modal-backdrop` #modalBackdrop L1099/L1699 | fixed center · z override 60 (L1368) | **คลิก → `closeModal()`** L1699 | `--z-portal` **60** (⭐ เหนือ drawer · DSP-01) |
| **Modal** | `.modal` L1700 | `event.stopPropagation()` L1700 | ปุ่มใน modal · Esc · คลิก backdrop | (ใน backdrop 60) |
| **Recipient view** | `.recipient-root` #recipientRoot L1402/L1706 | fixed inset0 · full-screen · `openRecipientView` L2759 | ปุ่ม `.rcp-close` "ปิด" (L2784) · Esc (**ตัวแรกสุด** L1844) | `--z-recipient` **70** |
| **Combo list** | `.combo-list` L1472 | absolute→portal `#overlay-root` · flip-up (DSP-03) | เลือก / Esc (`comboKey` L2269) / คลิกนอก (DSP-04 bubble-phase) | `--z-pop` **80** |
| Toast | `.toast` #toast L1709 | fixed · auto-hide | auto (durationMs · default 2800) | `--z-toast` 90 |

### Drawers (render โดย `drawerHTML()` L2610 · switch `state.drawer.mode`)
| mode | fn / anchor | เนื้อหา |
|---|---|---|
| `req-create` (D-reqCreate) | `openReqCreate` L2621 / `reqCreateDrawer` L2623 / `submitReqCreate` L2658 | **single-screen (LOCK-07 · ไม่ wizard)** — subject + purposes[] (checkbox list ค้นได้) + channel → ลิงก์+QR |
| `req-view` (D-reqView) | `openReqView` L2675 / `reqViewDrawer` L2676 | ข้อมูลคำขอ + เนื้อหาที่ให้เซ็น (doc-link) + ลิงก์/QR (copy/ดาวน์โหลด QR/ดาวน์โหลดเอกสาร) + การส่ง (ส่ง/ส่งซ้ำช่องอื่น) + ปุ่ม **เปิดมุมมองผู้รับ** |
| `pur-create` (D-purCreate) | `openPurCreate` L2811 / `purCreateDrawer` L2812 / `submitPurCreate` L2831 | ชื่อ + ช่องทาง (checkbox) + อายุ 1–120 + **อัปโหลดเอกสาร PDPA (จำเป็น)** |
| `pur-view` (D-purView) | `openPurView` L2867 / `purViewDrawer` L2868 | สถิติ 4 + รายละเอียด + **เอกสารรายเวอร์ชัน (doc-link · แก้ไม่ได้)** + re-consent banner + ออกเวอร์ชันใหม่/ปิดวัตถุประสงค์ |
| `consent-view` (D-consentView) | `openConsentView` L2903 / `consentViewDrawer` L2904 | รายละเอียด + **หลักฐาน 5 อย่าง** + **timeline (append-only)** + ถอน/ต่ออายุ |
| `c360` (D-c360) | `openC360` L2937 / `c360Drawer` L2938 | **Customer 360** (E1) — consent ทุก purpose×channel ของลูกค้ารายเดียว |

- `dwHead(eyebrow,title,sub)` L2603 (eyebrow + X button) · `dwFoot(left,right)` L2607 (actions ซ้าย + ปุ่ม "ปิด" ขวา) · `sec(title,inner)` L2608

### Modals (render โดย `modalHTML()` L2960 · switch `state.modal.type`)
| type | fn / anchor | รูปแบบ |
|---|---|---|
| `policy` (M-policy/doc · **DSP-01**) | `viewPolicy` L2967 / `policyModal` L2968 | **document viewer** — `.doc-frame` เนื้อหาเอกสารเวอร์ชันที่เลือก (z=60 เหนือ drawer) |
| `withdraw` (M-withdraw) | `withdrawModal` L2978 / `doWithdraw` L2984 | ถอนแทนลูกค้า — เหตุผล (จำเป็น) + ช่องทางที่ลูกค้าแจ้ง → มีผลทันที (ไม่อนุมัติ) |
| `new-version` (M-newVersion) | `openNewVersion` L2993 / `newVersionModal` L2997 / `doPublishVersion` L3003 | ออกเวอร์ชันเอกสารใหม่ + upload → v+1 + เตือน stale |
| `close-purpose` (M-closePurpose) | `closePurposeModal` / `doClosePurpose` L3016 | confirm ปิดวัตถุประสงค์ |
| ต่ออายุ (M-renew) | `openRenew` L2933 | ปิด drawer → เปิด reqCreate อ้างรายการเดิม (คำขอใหม่ · ไม่แก้วันหมดอายุเดิม) |

---

## §7 · Interaction Spec

### ⭐ Esc chain (ลำดับจริงจาก handler)
1. **L1843** — global `keydown` (`window.addEventListener`): `if (e.key === 'Escape')` →
   - `state.recipient.open` → `closeRecipientView()` (**recipient = surface บนสุด · ปิดก่อน**)
   - else `state.modal.open` → `closeModal()`
   - else `state.drawer.open` → `closeDrawer()`
2. **L2269** — combobox `comboKey()`: `else if(e.key==='Escape'){ comboClose(key); }` — Esc ปิดเฉพาะ combobox list ที่ focus อยู่ (ผูกต่อ `onkeydown` ของ input แต่ละตัว)

> ลำดับปิด: (combobox list ที่ focus) → recipient → modal → drawer

### Overlay lifecycle
- **openDrawer** L1796: set `state.drawer` → `render()` → rAF add `.is-open` ให้ backdrop+drawer
- **closeDrawer** L1805/L3075: remove `.is-open` + `setTimeout 280ms` reset state + `state.dd={}` + render
- **openModal** L1812 / **closeModal** L1819/L3078: rAF add is-open · closeModal `teardownCombos()` + `setTimeout 200ms` reset
- **openRecipientView** L2759 / **closeRecipientView** L2765: rAF add `.is-open` · close = remove + `setTimeout 240ms` reset
- **combobox teardown:** `teardownCombos()` เรียกต้น `render()` (L2336) — combo ถูก re-init `initPageCombos()` ท้าย render (L2371)
- **focus/scroll restore:** `preserveRenderState()` L2337 / `restoreRenderState()` L2370 (Rule #29 — คง scroll/focus ข้าม innerHTML rebuild)
- click-outside: drawer backdrop L1693 · modal backdrop L1699 · combo DSP-04 bubble-phase outside-click

### recipient submit guard (`submitRecipient` L2772)
1. `!verified` → toast "กรุณายืนยันตัวตนก่อนส่งคำตอบ" (warning) → หยุด
2. เลือกไม่ครบทุก purpose (`missing.length`) → toast "กรุณาเลือกยินยอม/ไม่ยินยอมให้ครบทุกวัตถุประสงค์" (warning) → หยุด
3. ผ่าน → snapshot choices → `closeRecipientView()` → `applyAnswers()` L2724 (สร้างทะเบียน granted/declined รายข้อ + supersede คู่เดิม L2749 + evidence 5 + history + `emitConsequence` CSQ)

### Positioning
- drawer = fixed right slide · modal = fixed center · recipient = fixed inset0 · toast = fixed · combo-list = portal absolute (flip-up)

---

## §8 · State-Driven UI Matrix

### Persona / permission model (`.demo-strip` L1674 · `PERM()` L2137)
> demo-strip มุมซ้ายล่าง = **persona switch (prototype only #105)** — 3 ปุ่ม Officer/DPO/Auditor (`setPersona(p)` L3031 → `state.persona` L2116 → `render()` + `syncPersonaUI` L3032)

| persona | reqCreate | send | sign | withdraw | purpose (สร้าง/แก้/ปิด) |
|---|:--:|:--:|:--:|:--:|:--:|
| `officer` (default) | ✅ | ✅ | ✅ | ✅ | ❌ |
| `dpo` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `auditor` | ❌ | ❌ | ❌ | ❌ | ❌ (read only) |

- `PERM()` L2137–2138: `reqCreate/send/sign/withdraw = p!=='auditor'` · `purpose = p==='dpo'`
- ผลต่อ UI: auditor → ไม่มีปุ่มสร้างคำขอ/ถอน/ส่ง · non-dpo ใน tab purposes → chip **"เฉพาะ DPO แก้ไขได้"** (L2392) · `userRole` sync ข้อความตาม persona (L3035)

### resolve verdict (`resolveConsent` L2557 · ตอบ HTTP 200 เสมอ)
| กรณี | allowed | status | reason (verbatim ย่อ) |
|---|:--:|---|---|
| ไม่มีรายการคู่นี้ | false | `never_asked` | "ยังไม่เคยขอความยินยอมสำหรับคู่นี้ — ค่าเริ่มต้นคือส่งไม่ได้" (FN-20) |
| granted + policy ปัจจุบัน | true | granted | "ยินยอมอยู่ (นโยบาย vN) หมดอายุ …" |
| granted + policy เก่า (stale) | false | granted | "ยินยอมไว้กับนโยบายเวอร์ชัน N แต่เวอร์ชันปัจจุบันคือ M — ต้องขอความยินยอมใหม่" |
| expired | false | expired | "เคยยินยอมแต่หมดอายุแล้ว … ต้องต่ออายุก่อน" |
| withdrawn | false | withdrawn | "ถอนความยินยอมแล้ว … ห้ามส่งจนกว่าจะได้รับความยินยอมใหม่" |
| declined | false | declined | "เจ้าของข้อมูลปฏิเสธชัดแจ้ง — ห้ามส่ง" |
| pending | false | pending | "ส่งคำขอไปแล้วแต่ยังไม่ได้รับคำตอบ … การไม่ตอบไม่ใช่การยินยอม" |
| purpose closed | false | (append) | "· วัตถุประสงค์นี้ถูกปิดใช้งานแล้ว" |

### consent effective status (`effStatus` L2208)
- `granted` + `expiresAt` เลยวันนี้ → **`expired`** (คำนวณสด) · `policyStale` L2209 = granted แต่ `policyVersion < currentVer` · `nearExpiry` L2210 = granted และเหลือ 0–30 วัน · `isActive` L2211 = `effStatus==='granted'`

### recipient choice (`state.recipient.choices` L2761)
- ต่อ purpose = `null` (default) / `'grant'` / `'decline'` (`setRecipientChoice` L2769) · verify = false/true · expanded (doc) ต่อ code

---

## §9 · Microcopy (verbatim)

### Toast (`showToast(message,variant,durationMs=2800)` L1829 · templates verbatim)
| variant | ข้อความ (literal · `+ ตัวแปร` = concat) | anchor |
|---|---|---|
| success | `ส่งออก {n} รายการเป็น CSV แล้ว` | L2486 |
| warning | `เลือกให้ครบทั้ง 3 ช่องก่อนตรวจสิทธิ์` | L2553 |
| warning | `เลือกเจ้าของข้อมูลก่อน` | L2659 |
| warning | `เลือกช่องทางก่อน` | L2660/2716 |
| warning | `เลือกวัตถุประสงค์ที่รองรับช่องทางนี้อย่างน้อย 1 ข้อ` | L2662 |
| success | `สร้างคำขอ {r.id} พร้อมลิงก์และ QR แล้ว` | L2665 |
| success | `บันทึกการส่งทาง{ช่องทาง} (จำลอง — ไม่ส่งจริง)` | L2715 |
| success | `บันทึกคำตอบแล้ว · ยินยอม {n} · ปฏิเสธ {m} (เก็บหลักฐานครบ 5 อย่าง)` | L2747 |
| warning | `กรุณายืนยันตัวตนก่อนส่งคำตอบ` | L2773 |
| warning | `กรุณาเลือกยินยอม/ไม่ยินยอมให้ครบทุกวัตถุประสงค์` | L2775 |
| warning | `กรอกชื่อวัตถุประสงค์` | L2832 |
| warning | `เลือกช่องทางอย่างน้อย 1` | L2833 |
| warning | `อายุต้องอยู่ระหว่าง 1–120 เดือน` | L2834 |
| warning | `ต้องแนบเอกสาร PDPA` | L2835/3004 |
| success | `สร้างวัตถุประสงค์ {code} แล้ว` | L2839 |
| info | `ไม่มีรายการที่กระทบ` | L2895 |
| success | `สร้างคำขอความยินยอมใหม่ {n} รายการ (นโยบายเวอร์ชันปัจจุบัน)` | L2899 |
| warning | `กรอกเหตุผล` | L2986 |
| warning | `เลือกช่องทางที่ลูกค้าแจ้งมา` | L2987 |
| success | `ถอนความยินยอมแล้ว — มีผลทันทีในคำขอถัดไป` | L2991 |
| success | `ออกเอกสาร v{nv} แล้ว · {stale} รายการต้องขอความยินยอมใหม่` | L3009 |
| success | `ปิดวัตถุประสงค์ {code} แล้ว` | L3018 |
| warning | `ไม่มีคำขอที่รอตอบ — สร้างคำขอก่อน` | L3027 |
| info | `เมนูนี้เป็นบริบทของโมดูลอื่น (เดโมไม่รวมขอบเขต)` | L3037 |
| error | `ดาวน์โหลดไม่สำเร็จในสภาพแวดล้อมนี้` | L3065 |
| success | `ดาวน์โหลด QR ของ {id} แล้ว (บันทึกการนำลิงก์ออก)` | L3068 |
| success | `ดาวน์โหลดเอกสาร (ต้นแบบ): {names}` | L3071 |
| success | `คัดลอกลิงก์แล้ว` | L3072 |
| error | `คัดลอกไม่สำเร็จ` | L3072 |

### Empty states (verbatim)
| title | desc | ที่ไหน |
|---|---|---|
| ไม่พบความยินยอม | ลองล้างตัวกรอง หรือสร้างคำขอความยินยอมใหม่ | registry |
| ยังไม่มีคำขอ | สร้างคำขอความยินยอมให้ลูกค้า | requests |
| ไม่พบวัตถุประสงค์ | ลองค้นด้วยคำอื่น | purposes |
| เลือกเจ้าของข้อมูล · วัตถุประสงค์ · ช่องทาง แล้วกดตรวจสิทธิ์ | ระบบจะจำลองคำตอบเหมือนที่ API `/consent/resolve` ให้ · ตอบ HTTP 200 เสมอ | resolve (ก่อนกรอก · L2542) |
| ไม่พบรายการ | — | combobox list ว่าง (L2274) |

### Key labels / notes (verbatim)
- H1 (คงที่ทุกแท็บ · L2385): **"ความยินยอม PDPA"**
- resolve field-help (L2549): "ค่าเริ่มต้นคือ **ส่งไม่ได้** — ไม่มีรายการในทะเบียน = ไม่อนุญาต (BR-04) · การไม่ตอบ ≠ ปฏิเสธ (BR-08)"
- resolve result note (L2591): "สัญญาผลลัพธ์ล็อกแล้ว (BR-20) — เพิ่มฟิลด์ได้ ห้ามเปลี่ยนชื่อ/ความหมายฟิลด์เดิม · ผู้เรียกแคชได้ ≤5 นาที และต้องล้างแคชทันทีเมื่อถอน (BR-21)"
- **หลักฐาน 5 อย่าง (BR-15 · `consentViewDrawer` L2909–2914):** เวลาที่ตอบ · ช่องทางที่ส่งคำขอ · วิธียืนยันตัวตน · เวอร์ชันนโยบาย · ไอพีและอุปกรณ์
- recipient (L2783/2787): "**จำลอง** — นี่คือหน้าที่เจ้าของข้อมูลเห็นเมื่อเปิดลิงก์ (ไม่ใช่การส่งจริง)" · "โปรดอ่านเอกสารแต่ละวัตถุประสงค์ แล้วเลือกว่าจะยินยอมหรือไม่ยินยอม"
- recipient verify (L2804): "ฉันคือเจ้าของข้อมูลและได้อ่านเอกสารแล้ว" / "ยืนยันตัวตน (ต้นแบบ) — จำเป็นก่อนส่งคำตอบ"
- purpose versions section (L2881): "เอกสาร (เวอร์ชัน — แก้ไม่ได้ · BR-05)" · timeline (L2922): "ประวัติ (เพิ่มอย่างเดียว · BR-16)"

---

## §10 · Data Binding & BACKEND anchors

> HTML ใช้ mock in-memory (`state.purposes` L2167 · `state.consents` L2187 · `state.requests` L2214 · `SUBJECTS` L2152 · `CHANNELS` L2141) · **เนื้อหา = เอกสารอัปโหลด versioned** (`versions[].docName/docType/body` · `curDoc` L2180)

| UI action (fn) | plug → FRD API |
|---|---|
| ทะเบียน list + filter (`registryBody`/`filteredConsents`) | GET `/consent/registry?...` (F058-API-14) |
| consent detail (`openConsentView`) — หลักฐาน 5 + timeline | GET `/consent/registry/:id` (F058-API-15) |
| requests list / view (`requestsBody`/`openReqView`) | GET `/consent/requests[/:id]` (F058-API-08) |
| สร้างคำขอ single-screen (`submitReqCreate`) | POST `/consent/requests` (F058-API-07) |
| ส่ง/ส่งซ้ำ (`sendVia`/`resendOther`) | POST `/consent/requests/:id/send` (F058-API-09) |
| copy link / ดาวน์โหลด QR (`copyLink`/`downloadQR`) | log นำลิงก์ออก (F058-API-10) |
| ดาวน์โหลดเอกสาร (`downloadPdfForm`) | เอกสารเวอร์ชันปัจจุบันของแต่ละ purpose (F058-API-11) |
| purpose list + stats (`purposesBody`) · สร้าง (`submitPurCreate`) | GET / POST `/consent/purposes` (F058-API-01/02 · dpo) |
| purpose view (`openPurView`) · ออกเวอร์ชัน (`doPublishVersion`) · ปิด (`doClosePurpose`) | GET `/consent/purposes/:code` · POST `/versions` · POST `/close` (F058-API-03/04/05) |
| document viewer (`viewPolicy`) | โหลด body เอกสาร (F058-API-03) |
| recipient load / submit (`openRecipientView`/`submitRecipient`→`applyAnswers`) | GET `/consent/recipient/:token` · POST `/answer` (F058-API-12/13) |
| ถอน (`doWithdraw`) | POST withdraw (F058-API-17) + CSQ `consent.withdrawn` (reversal_of=grantEvent) |
| ต่ออายุ (`openRenew`→reqCreate refOld) | POST (F058-API-19) — คำขอใหม่อ้างเดิม ไม่แก้ expiresAt เดิม |
| resolve (`resolveConsent`) | POST `/consent/resolve` (F058-API-20 · ตอบ 200 · never_asked ≠ 404) |
| ทุก grant/decline/withdraw/version | `emitConsequence(...)` L2737/2742/... → **CSQ event → 7C Engine** (declare-only) |

- **ไม่มี** `// BACKEND:` comment marker ในโค้ด — mock ทุกตัวมีจุด plug ตามตารางบน (map ↔ FRD 02_API)
- `exportCsv` L2480 · `downloadQR`/`downloadPdfForm`/`copyLink` = client-side utility (เดโม · toast จำลอง · **ไม่ส่งจริง** ตาม FN-40.3)

---

## §11 · Traceability (Brief ↔ FRD ↔ HTML) + Drift Log

| Brief § | FRD (P/D/M · API · FN) | HTML anchor |
|---|---|---|
| §2.2 tab registry | P-01 · API-14/15 · FN-13/14/16 | `registryBody()` L2427 |
| §2.2 tab requests | P-02 · API-07/08/09 · FN-05/06/07/08/09 | `requestsBody()` L2493 |
| §2.2 tab purposes | P-03 · API-01/02/03/04/05 · FN-01/02/03/04 | `purposesBody()` L2520 |
| §2.2 tab resolve | P-04 · API-20 · FN-19/20 | `resolveBody()` L2540 · `resolveConsent()` L2557 |
| §4/§6 recipient view | P-05 · API-12/13 · FN-10/11 | `recipientViewHTML()` L2780 · `submitRecipient()` L2772 |
| §6 D-reqCreate (single-screen) | D-reqCreate · API-07 · FN-05 · **LOCK-07** | `reqCreateDrawer()` L2623 |
| §6 D-reqView (send/QR/doc) | D-reqView · API-09/10/11 · FN-06/07/08/09 | `reqViewDrawer()` L2676 |
| §6 D-purCreate (upload) | D-purCreate · API-02 · FN-01 | `purCreateDrawer()` L2812 |
| §6 D-purView (versions) | D-purView · API-03/04/05 · FN-02/03/04 | `purViewDrawer()` L2868 |
| §6 D-consentView (evidence5+timeline) | D-consentView · API-15/17/19 · FN-12/15/17/18 | `consentViewDrawer()` L2904 |
| §6 D-c360 (Customer 360) | D-c360 · FN-14 (E1) | `c360Drawer()` L2938 |
| §6 M-policy (DSP-01) | M-policy/doc · API-03 · DSP-01 | `viewPolicy()` L2967 · `policyModal()` L2968 |
| §6 M-withdraw / M-newVersion / M-closePurpose / M-renew | M-* · API-04/05/17/19 · FN-02/04/15/17 | L2978/2997/3016/2933 |
| §8 persona/PERM | §1.5 COSO · roles | `.demo-strip` L1674 · `PERM()` L2137 |
| §1 z / DSP-01/03 | §1.0 z-registry · DSP-01/03 | `.modal-backdrop` z=`--z-portal` L1368 · `.combo-list` z=`--z-pop` L1472 |

### ⚠️ Drift Log
| # | ชนิด | รายการ | หมายเหตุ / ข้อเสนอ |
|---|---|---|---|
| D-1 | note (label mismatch) | 01_UI §1.0 z-registry เขียน "`--z-pop` 80 = document viewer modal (DSP-01)" แต่ **observed:** doc viewer modal ใช้ `.modal-backdrop` z=`--z-portal`**60** (L1368) ส่วน `--z-pop`**80** = `.combo-list` portal (L1472) | ทั้งคู่ยัง**เหนือ drawer(55)** — DSP-01 satisfied · ไม่ใช่ bug UI · เสนอ BA แก้ label ใน 01_UI ให้ตรง observed (doc modal=60 · combo portal=80) |
| D-2 | note (by-design) | route แบบ hash `#/consent/<tab>` — extractor เห็นแค่ `consent` (ตัด segment หลัง) | จงใจ · refresh-safe (ต่างจาก ESS ที่ใช้ state.tab) · H1 คงที่ · ตรง 01_UI P-01..04 |
| D-3 | HTML-only (base-kit ค้าง) | overlay `.user-menu` · `.ss-list` · `.menu-fixed` มี CSS/handler แต่ **ไม่ถูก wire** (ฟีเจอร์ใช้ custom `.combo` แทน searchSelect) | base-kit residual — ไม่ใช่ UI gap · dev ไม่ต้อง implement · prod อาจตัด CSS ที่ไม่ใช้ |
| D-4 | HTML-only (prototype) | `.demo-strip` persona switch (Officer/DPO/Auditor) + sidebar sibling `decorativeNav()` | prototype-only (#105) — prod: persona จาก JWT/role จริง · sibling = เมนูโมดูลอื่น (นอก scope) · ดู §DEMO-ONLY |
| D-5 | FRD-only (ASSUMED) | id-verify จริง (OQ-03) · ขึ้นทะเบียนด่านบังคับสิทธิ์ F143 (OQ-04 · BR-22) · CSQ SecC pipe (OQ-CSQ-02) · caller cache ≤5 นาที (BR-21) | **BLOCKING/backend contract** — HTML mock: verify=checkbox ต้นแบบ · resolve=simulator · CSQ=declare-only · ต้องเคาะก่อน prod (→ PROPOSALS) |
| D-6 | FRD-only | notification | 01_UI §1.6 = **ไม่มี notification event** (ntf ไม่เลือก) · การส่ง = mock toast เท่านั้น — ตรงกับ observed (bell static · ไม่มี ENG-NOTIFY) |

**สรุป: ไม่มี business drift ที่ทำให้ HTML ขัด FRD** — drift ทั้งหมดเป็น label mismatch เล็กน้อยใน z-registry (D-1), by-design routing (D-2), base-kit residual (D-3), prototype persona (D-4), backend/ASSUMED contract ที่ mock ไม่จำลอง (D-5), และ notification ที่จงใจไม่มี (D-6)

---

## §DEMO-ONLY · 🔴 รายการที่ prod build ต้อง strip / เปลี่ยนแหล่งข้อมูล

| # | element | anchor | prod behavior |
|:--:|---|---|---|
| 1 | **demo-strip persona switch** `.demo-strip#demoStrip` (Officer/DPO/Auditor · `setPersona`) | L1674 | **ลบทั้งแถบ** — persona/role มาจาก JWT/สิทธิ์จริง (PERM ต่อ role จริง) |
| 2 | **sidebar sibling menus** `decorativeNav()` (แคมเปญ/จดหมายข่าว/ทะเบียนลูกค้า/เคส/ใบเสนอราคา/ใบสั่งขาย/องค์กร) | L1613/1614/1623/1624/1633/1634/1643 | เมนูโมดูลอื่นจริง (นอก scope รอบนี้) — ไม่ใช่ toast stub |
| 3 | **client-side utility** exportCsv / downloadQR / downloadPdfForm / copyLink (toast จำลอง) | L2480/3060+ | prod = เรียก API จริง (F058-API-10/11) · ไม่ใช่ toast "จำลอง" |
| 4 | **recipient verify = checkbox ต้นแบบ** (`toggleRecipientVerify`) | L2770/2805 | prod = id-method จริง (OQ-03 BLOCKING) — "ยืนยันตัวตน (ต้นแบบ)" |
| 5 | **resolve = simulator** (`resolveConsent` in-memory) | L2557 | prod = POST `/consent/resolve` จริง (สัญญาฟิลด์ล็อก BR-20) |

**คงไว้ใน prod:** ทะเบียน/หลักฐาน 5/timeline · document viewer (versioned) · recipient read+sign flow · resolve UI · statusPill vocabulary · default-deny (never_asked)

---

## §12 · Diff จากเวอร์ชันก่อน
— ไม่มี HTML เวอร์ชันก่อนให้เทียบ (บรีฟ AS-BUILT รอบแรก · N/A)

---

## §13 · 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)

> ที่เดียวที่อนุญาตให้คิดเอง (R1) — ต่อไปนี้ **ไม่มีในจอ** เป็นข้อเสนอ ไม่ใช่สเปคที่ต้องทำ

1. **แก้ label z-registry ใน 01_UI (D-1)** — สอดคล้อง observed: doc viewer modal = `--z-portal`(60), combo portal = `--z-pop`(80) — กัน dev ตั้ง z ผิดตอน implement
2. **id-verify จริง (OQ-03 · BLOCKING)** — recipient verify ปัจจุบัน = checkbox ต้นแบบ · ต้องเคาะวิธียืนยันตัวตน (OTP/e-KYC/ลิงก์เฉพาะตัว) ก่อน dev
3. **ขึ้นทะเบียนด่านบังคับสิทธิ์ (OQ-04 · BR-22)** — `/consent/*` ผูก Security wave W2 (ยังไม่ทำ) — resolve เป็น gate ก่อนส่งทุกครั้ง
4. **caller cache contract (BR-21)** — สัญญาฝั่งผู้เรียก cache ≤5 นาที + ล้างเมื่อถอน (document ใน FRD API · ไม่ทำ UI)
5. **base-kit residual cleanup (D-3)** — `.user-menu`/`.ss-list`/`.menu-fixed` ไม่ถูก wire (ใช้ `.combo` แทน) — prod ผอมลงได้ถ้าตัด CSS ที่ไม่ใช้
6. **consent receipt PDF (E3)** — scope ใหม่ เลื่อน (ทำได้ที่ step 2 / wave DSAR)
