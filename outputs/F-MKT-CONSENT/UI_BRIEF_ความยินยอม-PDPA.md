# UI Brief — F-MKT-CONSENT · F058 · ความยินยอม PDPA (Consent Management)

> **EXTRACTION-BASED (Iron Rule R1)** — ทุกบรรทัดในบรีฟนี้ trace กลับหา selector / function / ข้อความจริงใน `consent-pdpa.html` ได้
> อ้าง `Lxxxx` = เลขบรรทัดใน HTML · ข้อเสนอที่ไม่มีในจอ อยู่ท้ายไฟล์ §13 เท่านั้น
> คู่กับ: **HTML (source of truth)** + **FRD Pack v1.1** (ระบบ) + บรีฟนี้ (design intent)
> 🔵 **สถาปัตยกรรมสำคัญ:** ทั้งฟีเจอร์ = **เมนูเดียว** `#navConsent` (#104) · H1 = **"ความยินยอม PDPA" คงที่ทุกแท็บ** (L2394) · ภายในสลับ **4 route-tab** (`#/consent/<tab>` — hash-based refresh-safe) · **มุมมองผู้รับ** = surface เต็มจอนอก shell (z=`--z-recipient` 70)
> 🟠 **รอบนี้ = re-run step 8 หลัง BA-gate HTML fixes** — AS-BUILT หลังแก้ FIX-01..08 (spinner busy-state · sent-version stale-warn · recipient closed-state · demo-only marker · purStatusPill helper · persona guards render+in-function · contract anchors) · diff สรุป §12

---

## §0 · Document Control + Pairing

| | |
|---|---|
| Feature | F-MKT-CONSENT · F058 · ความยินยอม PDPA (Consent Management) · plan `Marketing · W1 · dec=["csq"] · dep=""` (standalone) |
| HTML source | `outputs/F-MKT-CONSENT/consent-pdpa.html` · `<title>` = "ความยินยอม PDPA · F-MKT-CONSENT · CUBE NATIVE" (L6) · **3142 บรรทัด** (โต ~60 บรรทัดจาก BA-gate fixes) · BASE-KIT v6.4 |
| Archetype | **Pattern A (list-view) ×3 + Pattern K (read-only simulator) ×1** ในเมนูเดียว 4 tab + **Full-screen recipient surface** (P-05) · เนื้อหา = **เอกสารอัปโหลด versioned** ต่อวัตถุประสงค์ (ไม่ใช่ข้อความพิมพ์) |
| FRD Pack | `FRD_Pack/` v1.1 (00_OVERVIEW · 01_UI · 02_API · 03_LOGIC · 04_DB · 05_RULES · 06_TESTS · 07_LOCKED_DECISIONS · INDEX) — **paired** |
| BRD | `BRD_F-MKT-CONSENT.md` (Gate APPROVED · upload model = DECLARED-01 · 6 OQ) |
| FUNCTION_CHECKLIST | 20 FN บวก + FN-40 (10 ข้อห้ามมี) · e2e 32/32 · FN 20/20 |
| Declaration | **csq** ✅ (`CSQ_BRIEF_F-MKT-CONSENT.md` · declare-only 7 events → 7C Engine · ห้ามประกาศ OC/DC/SC) · doa/doccfg/ntf = ไม่เลือก |
| รอบก่อนหน้า (diff) | HTML ก่อน BA-gate fixes (ไม่มีสำเนาแยกให้ diff เชิงบรรทัด) — §12 บันทึกชุด FIX-01..08 แทน |
| Gate สถานะ | qc-ux PASS · coverage R1 PASS (FN 20/20) · e2e 32/32 · **BA-gate fixes FIX-01..08 applied** (ต้อง re-run step 3·4·5 ตาม C3.2 ก่อนปิดงาน) |
| Drift | บันทึกใน §11 — z-token label mapping (FRD vs observed), base-kit residual overlays, OQ cross-module · **ไม่มี business drift ที่ block** |
| Carry OQ | **OQ-03/OQ-04 BLOCKING** (id-verify จริง, ขึ้นทะเบียน F143) · OQ-CSQ-01/02 · BR-21/22 (→ PROPOSALS step 12) |

**สถาปัตยกรรม:** Single-file vanilla-JS SPA · state-driven `render()` (L2352) · innerHTML rebuild + Render Preservation (Rule #29 · `preserveRenderState()`/`restoreRenderState()` L1986/2004 · wrapper `withRenderPreservation()` L2030) · **4 tab สลับด้วย hash route** `#/consent/<tab>` (`getRoute()` L1794 · `navigate()` L1799 · refresh-safe) · combobox = **custom `.combo`** (`cx_*` ids ผ่าน `ssId()` L2255 · DSP-02/03/04 · L2256+ แทน searchSelect ของ BASE-KIT) · Lucide icon multi-CDN fallback unpkg→jsdelivr→cdnjs · ฟอนต์ Noto Sans Thai (Google) + Satoshi (Fontshare).

---

## §1 · Design Tokens AS-BUILT (`:root` L28+ + z-block L1360–1369)

### Palette (CUBE CI v2.0 Warm Light rebrand · L28+)
| token | ค่า | ใช้ |
|---|---|---|
| `--c-navy` / `--c-navy-2` | `#111111` | sidebar · heading |
| `--c-primary` / `--c-primary-hover` | `#FF3B30` / `#E62E24` | ปุ่มหลัก · doc-link · stat icon · ptab active |
| `--c-teal` / `--c-teal-light` | `#FF9A1F` / `#FFB763` | accent · demo-strip brand icon |
| `--c-ink` | `#111111` | ตัวอักษรหลัก |
| `--c-mute` / `--c-mute-2` / `--c-mute-3` | `#54565C` / `#73757B` / `#9A9CA2` | ตัวอักษรรอง / meta / placeholder |
| `--c-line` / `--c-line-2` / `--c-line-3` | `#DEDAD4` / `#E9E5E0` / `#F1EEEA` | เส้น / card border / divider · `.pill-muted` bg |
| `--c-bg-off` | `#FAF8F5` | พื้นหลังหน้า · thead · row hover |
| `--c-success` / `--c-warning` / `--c-danger` | `#1F9D55` / `#E8870F` / `#E62E24` | pill สถานะ · verdict allow/deny · **`.near-tag` warning** (L1588) |

### Type scale (fixed · Iron Rule)
`--fs-h1:22px` · `--fs-h2:17px` · `--fs-h3:15px` · `--fs-body:14px` · `--fs-sub:13px` · `--fs-meta:12px` · `--fs-cap:11px` · `--fs-kpi:28px`
font stack: `'Satoshi','Noto Sans Thai',system-ui,sans-serif` · body 14px · line-height 1.5

### Spacing / Radius
`--sp-xs:4px --sp-sm:8px --sp-md:12px --sp-lg:20px --sp-xl:28px` · `--r-xs:4px --r-sm:6px --r-md:8px --r-lg:12px --r-full:999px`

### Shell dims
`--sidebar-w:232px` (L46) · `--shell-h:52px` (L47) · `scrollbar-gutter:stable` (Rule #35 กัน jank) · **drawer widths:** base `min(920px,100vw)` (L352) · `.drawer.standard` `min(680px,100vw)` / 680px (L353/L896) · `.drawer.wide` `min(1290px,100vw)` (L354) — `drawerWidth()` L2350 คืน `wide` เฉพาะ `req-view`/`pur-view` มิฉะนั้น `standard` (className set L2372)

### ⭐ Loading spinner (FIX-04 · Iron Rule #44/45 · L1518–1519 + base-kit L727–728)
- `@keyframes spin360{ to{ transform:rotate(360deg); } }` (L1519) · `.spin{ animation:spin360 .8s linear infinite; }` (L1518) — override ตัว base-kit `@keyframes spin` / `.spin` (L727–728) ด้วย cascade order
- ใช้กับ **busy-state ของปุ่ม submit** — `guardBusy()` (L2151) สลับปุ่มเป็น `<i data-lucide="loader-2" class="w-4 h-4 spin"></i> กำลังบันทึก…` + `disabled` ขณะ `state._busy` (ดู §5 · §7)

### `.near-tag` warning inline (L1588–1589 · FIX-03)
`display:inline-flex; gap:4px; color:var(--c-warning); font-size:11.5px; font-weight:700` · icon 12px — ใช้เป็น badge เตือนใน table/drawer (ใกล้หมดอายุ · นโยบายเก่า · ต่ออายุ · **stale sent-version**)

### ⭐ Z-INDEX MAP (สูง → ต่ำ · L1360–1369) + DSP override
| token | ค่า | ใช้กับ | หมายเหตุ |
|---|---:|---|---|
| `--z-toast` | **90** | `.toast` (#toast L1718) | สูงสุด — เห็นเหนือทุกอย่าง |
| `--z-pop` | **80** | `.combo-list` (portal L1476/1480) | combobox list ไป `#overlay-root` → ลอยเหนือ modal/drawer (DSP-03) · comment "เหนือ modal(60) เมื่อ portal" |
| `--z-recipient` | **70** | `.recipient-root` (L1406) | มุมมองผู้รับ (mock ลิงก์) — surface แยกเหนือ drawer/modal ของ ERP |
| `--z-portal` | **60** | portal menu context · **`.modal-backdrop` override เป็นค่านี้** (L1372) | ⭐ DSP-01 — modal เปิด **เหนือ drawer(55)** |
| `--z-drawer` | **55** | `.drawer` (L1374) | ลิ้นชัก view/create |
| `--z-backdrop` | **50** | `.drawer-backdrop` (L1373) · `.ss-list` (base-kit residual) | |
| `--z-dropdown` | **40** | `.user-menu` · `.menu-fixed` (base-kit residual) · thead sticky | |
| `--z-sticky` | **30** | `.shell-bar` · thead sticky · **`.demo-strip`** (L1499) | demo-strip = persona switch มุมซ้ายล่าง |
| `--z-shell` | **20** | `.sidebar` (L109) | |

> ⭐ **DSP-01 (L1372):** `.modal-backdrop{ z-index: var(--z-portal) }` = **60 > drawer 55** — จงใจให้ modal (document viewer `viewPolicy`, withdraw, new-version, close-purpose) โผล่ **ทับ** drawer ได้ (pre-wire กัน bug in-drawer modal ที่ qc-ux เคยพลาด — precedent DSP-01)
> ⭐ **DSP-03 (L1476 + `comboPosition` L2302):** `.combo-list` portal ไป `#overlay-root` (L1679) ที่ z=`--z-pop`(80) + flip-up เมื่อพื้นที่ล่างไม่พอ — ให้ combobox list ลอยเหนือทั้ง modal(60) และ drawer(55) ไม่ถูก clip

---

## §2 · Route Map (⚠️ hash-based · 4 tab = 1 เมนู)

> **1 feature = 1 เมนู (#104):** ทั้ง feature = เมนูเดียว "ความยินยอม PDPA" (`#navConsent` L1618) · ภายในสลับ **4 route-tab** ด้วย hash `#/consent/<tab>` — **refresh-safe** · **H1 คงที่ "ความยินยอม PDPA" ทุกแท็บ** (L2394) — สิ่งที่เปลี่ยนต่อ tab คือ `.ph-sub` + breadcrumb + `.ph-actions` + body

### 2.1 · Router (observed · L1794–1801 · refresh-safe)
- `getRoute()` L1794 = `location.hash.replace('#/','')` · default `home` เมื่อ hash ว่าง/`#`/`#/`
- `navigate(route)` L1799 = set `location.hash = '#/' + route`
- ใน `render()` L2355+: `route.indexOf('consent/')===0` → `tab = route.split('/')[1]` · `route==='consent'||'home'` → `registry` · tab ที่ไม่อยู่ใน `['registry','requests','purposes','resolve']` → fallback `registry`
- **hashchange** ผูก `render()` (base-kit late-binding) — refresh หรือ paste URL `#/consent/purposes` เข้าตรง tab ได้

### 2.2 · 4 tabs (`pageHeadHTML` L2392 · ptab def L2400)
| tab | route | ptab label | icon | render fn | `.ph-sub` (verbatim) |
|---|---|---|---|---|---|
| `registry` (default) | `#/consent/registry` | ทะเบียน | `table-2` | `registryBody()` L2446 | ทะเบียนความยินยอมทั้งหมด · กรองตามเจ้าของข้อมูล วัตถุประสงค์ ช่องทาง |
| `requests` | `#/consent/requests` | คำขอ | `send` | `requestsBody()` L2512 | คำขอความยินยอมและการส่งแต่ละครั้ง |
| `purposes` | `#/consent/purposes` | วัตถุประสงค์ | `target` | `purposesBody()` L2542 | วัตถุประสงค์ · นโยบาย (เวอร์ชัน) · สถิติความครอบคลุม |
| `resolve` | `#/consent/resolve` | ตรวจสิทธิ์ | `shield-question` | `resolveBody()` L2565 | ตรวจสิทธิ์การส่ง — จำลองคำตอบเหมือนที่ API /consent/resolve จะให้ |

- ptab render `.ptab` L2400 → `onclick="navigate('consent/<tab>')"` · active = `is-active`
- breadcrumb `#bcCurrent` = `"ความยินยอม PDPA · " + bcMap[tab]` (bcMap: ทะเบียน/คำขอ/วัตถุประสงค์/ตรวจสิทธิ์) — **breadcrumb เปลี่ยน แต่ H1 ไม่เปลี่ยน**

### 2.3 · มุมมองผู้รับ (P-05 · ไม่ใช่ route — เปิดจากในคำขอ)
- `openRecipientView(reqId)` L2799 = surface เต็มจอ (`.recipient-root` #recipientRoot L1715 · z=70) · **ไม่มี hash** · เปิดจากปุ่มใน reqView drawer (L2741) · ปิด `closeRecipientView()` L2805 (Esc = ปิดตัวแรกสุด · L1854)

---

## §3 · Layout Shell

| region | selector / anchor | หมายเหตุ |
|---|---|---|
| Sidebar | `.sidebar` #sidebar (fixed · w=`--sidebar-w`232px · bg `#111111` · z=`--z-shell`20 L109) L1604 | โมดูล "การตลาด" > **item เดียวของฟีเจอร์** `.sb-item#navConsent[data-feature="consent"]` L1618 → `navigate('consent/registry')` · set `.is-active` ใน render |
| Sibling menus | `.sb-item` onclick `decorativeNav()` (L3094) | "แคมเปญส่งข้อความ · จดหมายข่าว · ทะเบียนลูกค้า · เคสบริการ · ใบเสนอราคา · ใบสั่งขาย · ข้อมูลองค์กร" = **context only** · คลิก → toast "เมนูนี้เป็นบริบทของโมดูลอื่น (เดโมไม่รวมขอบเขต)" |
| Module toggle | `toggleModule(headerEl)` L1784 | collapse ผ่าน `data-expanded` (Rule #27) |
| Topbar | `.shell-bar` L1659 (z=`--z-sticky`30) | nav-toggle (mobile) · breadcrumb "การตลาด › ความยินยอม PDPA · <tab>" (L1662) |
| Notif bell | `.icon-btn` L1667 | มี `.notif-dot` (static · ไม่ wire — ฟีเจอร์นี้ **ไม่มี notification** ตาม 01_UI §1.6) |
| User chip | `.user-chip` L1668 | "สุดา ใจดี" / `.user-role#userRole` (sync ตาม persona · `syncPersonaUI` L3089) / avatar |
| Page host | `.content #page-content` L1673–1674 | `render()` เขียน `pageHTML(tab)` ลงตรงนี้ |
| Overlay host | `#overlay-root` L1679 | portal สำหรับ `.combo-list` (DSP-03) |

**Page header (`pageHeadHTML` L2392):** `.ph` — `.ph-title-row > h1.ph-title` = **"ความยินยอม PDPA" (คงที่ · L2394)** + `.ph-sub` (ต่อ tab) + `.ph-actions` = `headActions(tab)` L2405 (ปุ่มตาม persona · ดู §8) ตามด้วย `.ptabs` (4 ปุ่ม).

---

## §4 · Page Anatomy (ต่อ tab)

### P-01 · ทะเบียน (`registryBody` L2446) — FN-13/14/16
- **stat cards (toggle filter)** `.stat.is-filter` × 4: ทั้งหมด (`database`) · ยินยอมอยู่ (`check-circle-2` · `isActive`) · ใกล้หมดอายุ (`clock-alert` · `nearExpiry`) · ถอนแล้ว (`undo-2`) — คลิก → `toggleStat(k,v)` L2443 (คลิกซ้ำ = ล้างกลับ 'all')
- **Filter bar:** search + status + channel + purpose (`setFilter(k,v)` L2442 · `resetFilters()` L2444 · `state.filters`)
- **Toolbar actions (`headActions` registry L2405):** ปุ่ม **ส่งออก CSV** (`exportCsv()` L2499 · E4) + **สร้างคำขอ** (`openReqCreate({})` · เฉพาะ `perm.reqCreate`)
- **Data Table triple** (`filteredConsents()` L2422 → `registryRowsHTML()` L2481) — เจ้าของข้อมูล × วัตถุประสงค์ × ช่องทาง + `statusPill(eff)` (L2246) + วันหมดอายุ (`.near-tag` เตือนใกล้หมด) + คอลัมน์ policy `v{n}` + `.near-tag`"เก่า" ถ้า stale · row คลิก → `openConsentView(id)` L2951 · ปุ่มขวา "ดูรายคน" → `openC360()` · sort `sortBy(col)` L2441
- **Empty:** title **"ไม่พบความยินยอม"** / desc "ลองล้างตัวกรอง หรือสร้างคำขอความยินยอมใหม่"

### P-02 · คำขอ (`requestsBody` L2512) — FN-05/06/07/08/09/10/11
- list คำขอ (`state.requests`) + `reqStatusPill(s)` L2243 (ร่าง/รอตอบ/ตอบแล้ว/คำขอหมดอายุ) + `.near-tag`"ต่ออายุ" ถ้า `refOld` · row → `openReqView(id)` L2703
- **Toolbar action:** **สร้างคำขอ** (`openReqCreate({})` · เฉพาะ `perm.reqCreate`)
- **Empty:** title **"ยังไม่มีคำขอ"** / desc "สร้างคำขอความยินยอมให้ลูกค้า"

### P-03 · วัตถุประสงค์ (`purposesBody` L2542) — FN-01/02/03/04
- แถว purpose (`state.purposes`) + `purposeStats()` L2532 (ยินยอมอยู่/ถอน/หมดอายุ/%ครอบคลุม) + `.near-tag`"N รายการผูกเวอร์ชันเก่า" (`staleCount` L2537) + **`purStatusPill(s)` L2540** (FIX-08 · pill สถานะเดียวต่อ cell: `active`→"ใช้งาน"(success) / อื่น→"ปิดแล้ว"(muted)) · row → `openPurView(code)` L2915
- **Toolbar action:** **สร้างวัตถุประสงค์** (`openPurCreate()` · เฉพาะ `perm.purpose`=dpo) · ไม่มีสิทธิ์ → chip **"เฉพาะ DPO แก้ไขได้"** (L2410)
- **Empty:** title **"ไม่พบวัตถุประสงค์"** / desc "ลองค้นด้วยคำอื่น"

### P-04 · ตรวจสิทธิ์ (`resolveBody` L2565) — FN-19/20 · **read-only simulator (Pattern K)**
- `.rz-layout` 2 คอลัมน์: ซ้าย = ฟอร์ม 3 combobox (`rzSubject`/`rzPurpose`/`rzChannel`) + ปุ่ม **ตรวจสิทธิ์การส่ง** (`runResolve()` L2577) · field-help "ค่าเริ่มต้นคือ **ส่งไม่ได้** … การไม่ตอบ ≠ ปฏิเสธ (BR-08)"
- ขวา = result card (`resolveResultHTML` L2604): badge `ส่งได้`/`ส่งไม่ได้` + `HTTP 200` chip + เหตุผล + `statusPill` + **ตัวอย่าง JSON** (`jsonColor()` L2618 · ฟิลด์ล็อก BR-19/20) — **ไม่มี mutation** (LOCK #9)
- **Empty (ก่อนกรอก):** `.rz-empty` "เลือกเจ้าของข้อมูล · วัตถุประสงค์ · ช่องทาง แล้วกดตรวจสิทธิ์"

### P-05 · มุมมองผู้รับ (`recipientViewHTML` L2821) — FN-10/11 · **full-screen surface**
- `.recipient-root` (fixed inset0 · z=`--z-recipient`70 · bg `#EEF1F5` · **ไม่มี sidebar/shell**)
- `.rcp-simbar.demo-only` (FIX-07 · L2823 — แถบ "จำลอง — นี่คือหน้าที่เจ้าของข้อมูลเห็นเมื่อเปิดลิงก์ (ไม่ใช่การส่งจริง)" + ปุ่ม `.rcp-close` "ปิด" · มี `<!-- DEMO-ONLY -->` comment ห้าม render ใน prod)
- 🔴 **Closed-state page (FIX-01 · L2826–2831):** ถ้า `r.status` **ไม่ใช่ `draft`/`pending`** → `recipientViewHTML()` return หน้า `.rcp-brandcard` h1 **"คำขอนี้ปิดแล้ว"** + `.rcp-sub` "คำขอความยินยอมนี้ได้รับคำตอบ เมื่อ {answeredAt} — หากต้องการเปลี่ยนแปลง โปรดติดต่อบริษัท" + subject chip — **ไม่มีฟอร์ม/choices/submit** (กันลูกค้าเปิดลิงก์ซ้ำแล้วเขียนทับ evidence chain)
- **สถานะปกติ (draft/pending):** `.rcp-brandcard` "CUBE Consent" + h1 "คำขอความยินยอม PDPA" + subject chip
- **ต่อวัตถุประสงค์** `.rcp-pcard`: ชื่อ + `.rcp-pver`"เอกสารเวอร์ชันปัจจุบัน vN · {date}" + **doc toggle** (`toggleRecipientDoc(code)` L2811 → ปุ่ม "อ่านเอกสาร · <docName>" ↔ `.doc-frame` body + ปุ่ม "ย่อ") + `.rcp-choices` (ยินยอม/ไม่ยินยอม · `setRecipientChoice` L2809)
- `.rcp-verify` checkbox (`toggleRecipientVerify` L2810) "ฉันคือเจ้าของข้อมูลและได้อ่านเอกสารแล้ว" / "ยืนยันตัวตน (ต้นแบบ) — จำเป็นก่อนส่งคำตอบ"
- ปุ่ม `.rcp-submit` "ยืนยันการตอบ" → `submitRecipient(event)` L2812

---

## §5 · Component Inventory (anchor + states)

### Page tabs (`.ptab` · L2400)
- โครง: `.ptabs > button.ptab` (icon + label) · **states:** default / `.is-active` (tab ปัจจุบัน) / hover (base-kit)

### Stat / filter cards (`.stat.is-filter` · L2446+)
- โครง: `.stat-label`(icon+label) + `.stat-value` · **states:** default / hover / `.is-on` (ตัวกรองที่เลือก) · toggle ซ้ำ = ล้าง

### ⭐ Submit button — busy/loading state (FIX-04 · `guardBusy(ev)` L2151)
- ทุกปุ่ม submit ที่เขียนข้อมูล เรียก `guardBusy(event)` เป็นด่านแรกหลัง validation:
  - ถ้า `state._busy` อยู่แล้ว → return `false` (กัน double-submit) ·
  - มิฉะนั้น set `state._busy=true`, ปุ่ม (`ev.currentTarget` tagName BUTTON) → `disabled=true` + `innerHTML='<i data-lucide="loader-2" class="w-4 h-4 spin"></i> กำลังบันทึก…'` + `renderIcons()` · ปลดล็อก `state._busy=false` หลัง **500ms**
- **states:** default → **busy** (disabled + spinner `loader-2 .spin` + "กำลังบันทึก…") → (หลัง submit สำเร็จ ปุ่มถูก render ใหม่/overlay ปิด)
- ผูกที่ 5 จุด: `submitReqCreate` (L2689) · `submitRecipient` (L2816) · `doWithdraw` (L3038) · `doPublishVersion` (L3058) · `doClosePurpose` (L3072)

### Status pills (`statusPill(eff)` L2246 · `pill(text,variant)`)
| eff (ทะเบียน) | label | variant |
|---|---|---|
| `never_asked` | ยังไม่เคยขอ | muted |
| `pending` | รอตอบ | warning |
| `granted` | ยินยอม | success |
| `declined` | ไม่ยินยอม | danger |
| `withdrawn` | ถอนแล้ว | muted |
| `expired` | หมดอายุ | warning |

| request status (`reqStatusPill` L2243) | label | variant |
|---|---|---|
| `draft` | ร่าง | muted |
| `pending` | รอตอบ | warning |
| `answered` | ตอบแล้ว | success |
| `expired` | คำขอหมดอายุ | muted |

**purpose pill (`purStatusPill(s)` L2540 · FIX-08):** `active` → "ใช้งาน" (success) · อื่น ๆ → "ปิดแล้ว" (muted) — helper แยกให้ pill สถานะเดียวต่อ cell (ก่อนหน้า inline ซ้ำ)

### Custom combobox (`.combo` · `comboHTML(key,ph)` L2256 · ids `cx_<key>[_part]` ผ่าน `ssId()` L2255)
- แทน searchSelect ของ BASE-KIT — list `.combo-list` portal (DSP-03 · L1476)
- **states:** closed / open (`comboOpen` L2274) / typing filter (`comboInput` L2275 + `<mark>` highlight `hl()` L2290) / highlighted item (`comboKey` L2282) / empty "ไม่พบรายการ" / picked (`comboPick` L2276 · DSP-02 ไม่ auto-open ตอน drawer เปิด `comboFocus` L2273)
- ใช้ที่: resolve (rzSubject/rzPurpose/rzChannel) · reqCreate (reqSubject/reqChannel) · reqView (resendCh) · withdraw modal (wdVia)

### doc-link / document viewer (`.doc-link` · `viewPolicy(code, ver)` L3015)
- `.doc-link` = **ชื่อไฟล์เอกสารที่คลิกได้** → `viewPolicy(code[,ver])` เปิด modal `policyModal` (L3016) z=60 เหนือ drawer · icon = `docIcon(docType)` L2199
- **FIX-03:** ใน reqView panel doc-link ส่ง `viewPolicy(code, sentVer)` (เวอร์ชัน ณ ตอนส่ง) · ใน purView ส่ง `viewPolicy(code, v.v)` ต่อเวอร์ชัน · `policyModal` เลือก doc จาก `d.ver` (fallback `curDoc`) + subtitle บอก "ปัจจุบัน" เฉพาะเวอร์ชันล่าสุด
- `.doc-frame` = กล่องแสดง body เอกสาร (ใน recipient view + policy modal) · **เนื้อหา = เอกสารอัปโหลด versioned** (`curDoc(p)` L2197 · currentVer)

### Read-only table
- row `.is-clickable` → `openConsentView`/`openReqView`/`openPurView` · **ไม่มี** inline-edit/pagination ที่ wire

### Buttons — inventory (verbatim)
`ส่งออก CSV` · `สร้างคำขอ` · `สร้างวัตถุประสงค์` · `ตรวจสิทธิ์การส่ง` · `คัดลอก` · `ดาวน์โหลด QR` · `ดาวน์โหลดเอกสาร` · `ส่งซ้ำ` · `ส่งทาง<ช่องทาง>` · `เปิดมุมมองผู้รับ (จำลองลิงก์)` · `ออกเวอร์ชันใหม่` · `ปิดวัตถุประสงค์` · `ถอนความยินยอม` · `สร้างคำขอต่ออายุ` · `ขอความยินยอมใหม่ (N รายที่กระทบ)` · `อ่านเอกสาร · <docName>` / `ย่อ` · `ยินยอม` / `ไม่ยินยอม` · `ยืนยันการตอบ` · `ดู` / `ดูรายคน` · `ปิด` · `ยกเลิก` · `ยืนยันถอน` · `ยืนยันปิด` · busy → `กำลังบันทึก…` (FIX-04)

---

## §6 · Overlay Registry (11 overlays · dismiss rules + z)

| overlay | selector / anchor | position / เปิด | ปิด (dismiss) | z |
|---|---|---|---|---|
| Sidebar | `.sidebar` #sidebar L1604 | fixed 232px · เปิดตลอด (mobile toggle) | — | `--z-shell` 20 |
| **demo-strip** | `.demo-strip.demo-only` #demoStrip L1683 | **fixed มุมซ้ายล่าง** · เปิดตลอด (prototype only #105) | — (persona switch เท่านั้น) | `--z-sticky` 30 |
| User menu | `.user-menu` (base-kit) | absolute ใต้ chip | click-outside (base-kit) | `--z-dropdown` 40 |
| Portal menu | `.menu-fixed` (base-kit) | fixed portal | `closeOverlay()` (base-kit) | `--z-dropdown` 40 |
| Search list | `.ss-list` (base-kit) | absolute overlay | base-kit | `--z-backdrop` 50 |
| **Drawer backdrop** | `.drawer-backdrop` #drawerBackdrop L1702 | fixed inset0 | **คลิก → `closeDrawer()`** L1702 | `--z-backdrop` 50 |
| **Drawer** | `.drawer` #drawer L1703 | fixed right · `standard`680px / `wide`1290px (L2350/2372) · slide translateX | ปุ่ม X (`dwHead`) · ปุ่ม "ปิด" (`dwFoot`) · Esc · คลิก backdrop | `--z-drawer` 55 |
| **Modal backdrop** | `.modal-backdrop` #modalBackdrop L1708 | fixed center · z override 60 (L1372) | **คลิก → `closeModal()`** L1708 | `--z-portal` **60** (⭐ เหนือ drawer · DSP-01) |
| **Modal** | `.modal` | `event.stopPropagation()` | ปุ่มใน modal · Esc · คลิก backdrop | (ใน backdrop 60) |
| **Recipient view** | `.recipient-root` #recipientRoot L1715 | fixed inset0 · full-screen · `openRecipientView` L2799 | ปุ่ม `.rcp-close` "ปิด" · Esc (**ตัวแรกสุด** L1854) | `--z-recipient` **70** |
| **Combo list** | `.combo-list` L1476/1480 | absolute→portal `#overlay-root` · flip-up (DSP-03) | เลือก / Esc (`comboKey` L2286) / คลิกนอก (DSP-04 bubble-phase) | `--z-pop` **80** |
| Toast | `.toast` #toast L1718 | fixed · auto-hide | auto (durationMs · default 2800) | `--z-toast` 90 |

### Drawers (render โดย `drawerHTML()` L2635 · switch `state.drawer.mode`)
| mode | fn / anchor | width | เนื้อหา |
|---|---|---|---|
| `req-create` (D-reqCreate) | `openReqCreate` L2646 / `reqCreateDrawer` L2648 / `submitReqCreate` L2683 | standard | **single-screen (LOCK-07 · ไม่ wizard)** — subject + purposes[] (`reqPurRowsHTML` L2665 checkbox ค้นได้) + channel |
| `req-view` (D-reqView) | `openReqView` L2703 / `reqViewDrawer` L2703 | **wide** | ข้อมูลคำขอ + **"เนื้อหาที่ให้เซ็น (BR-06)"** sent-version panel (FIX-03 · ดูล่าง) + ลิงก์/QR (copy/QR/เอกสาร) + การส่ง (ส่ง/ส่งซ้ำ) + `.demo-only` **เปิดมุมมองผู้รับ** |
| `pur-create` (D-purCreate) | `openPurCreate` L2859 / `purCreateDrawer` L2860 / `submitPurCreate` | standard | ชื่อ + ช่องทาง (checkbox) + อายุ 1–120 + **อัปโหลดเอกสาร PDPA (จำเป็น)** |
| `pur-view` (D-purView) | `openPurView` L2915 / `purViewDrawer` L2916 | **wide** | สถิติ 4 + re-consent banner + รายละเอียด + **เอกสารรายเวอร์ชัน (doc-link `viewPolicy(code,v.v)` · แก้ไม่ได้ BR-05)** + ออกเวอร์ชันใหม่/ปิดวัตถุประสงค์ (dpo) |
| `consent-view` (D-consentView) | `openConsentView` L2951 / `consentViewDrawer` L2952 | standard | รายละเอียด + **หลักฐาน 5 อย่าง** (`evItem` L2980) + **timeline (append-only BR-16)** + ถอน/ต่ออายุ |
| `c360` (D-c360) | `openC360` L2985 / `c360Drawer` L2986 | standard | **Customer 360** (E1 · S-14) — consent ทุก purpose×channel ของลูกค้ารายเดียว |

- `dwHead(eyebrow,title,sub)` L2628 (eyebrow + X button) · `dwFoot(left,right)` L2632 (actions ซ้าย + ปุ่ม "ปิด" ขวา) · `sec(title,inner)` L2633

### ⭐ Sent-version + stale warning panel (FIX-03 · `reqViewDrawer` L2711–2720)
- section **"เนื้อหาที่ให้เซ็น (BR-06)"** (L2720) แสดงเอกสารที่เจ้าของข้อมูลเห็น **ณ เวอร์ชันที่ส่งจริง** ไม่ใช่ปัจจุบัน:
  - `lastSent` = การส่งล่าสุดที่ snapshot เวอร์ชันไว้ (`r.sends` filter `.vers` · L2711) · `sentVer` = `lastSent.vers[code]` (คำขอที่ยังไม่ส่งใช้ `currentVer`) · snapshot เขียนใน `snapshotVers(r)` L2748 ตอน `sendVia` (L2752)
  - แต่ละ purpose row: ชื่อ + `<span class="ver-tag">v{sentVer}</span>` + label **"เวอร์ชันที่ส่ง"** (แสดงเมื่อมี lastSent) + doc-link `viewPolicy(code, sentVer)`
  - ถ้า `sentVer < currentVer` (`newer` L2715) → `.near-tag` warning **"ส่ง v{sentVer} · ปัจจุบัน v{currentVer} — พิจารณาส่งคำขอใหม่"** (L2716)

### Modals (render โดย `modalHTML()` L3008 · switch `state.modal.type`)
| type | fn / anchor | รูปแบบ |
|---|---|---|
| `policy` (M-policy/doc · **DSP-01**) | `viewPolicy` L3015 / `policyModal` L3016 | **document viewer** — `.doc-frame` เนื้อหาเอกสารเวอร์ชันที่เลือก (`d.ver` fallback current · z=60 เหนือ drawer) |
| `withdraw` (M-withdraw) | `withdrawModal` L3026 / `doWithdraw` L3032 | ถอนแทนลูกค้า — เหตุผล (จำเป็น) + ช่องทาง (`wdVia`) → มีผลทันที (BR-09) |
| `new-version` (M-newVersion) | `openNewVersion` L3044 / `newVersionModal` L3048 / `doPublishVersion` L3054 | ออกเวอร์ชันเอกสารใหม่ + upload → v+1 + เตือน N รายการ stale |
| `close-purpose` (M-closePurpose) | `closePurposeModal` L3065 / `doClosePurpose` L3070 | confirm ปิดวัตถุประสงค์ (BR-14/17) |
| ต่ออายุ (M-renew) | `openRenew` L2981 | ปิด drawer → เปิด reqCreate อ้างรายการเดิม (คำขอใหม่ · ไม่แก้วันหมดอายุเดิม) |

---

## §7 · Interaction Spec

### ⭐ Esc chain (ลำดับจริงจาก handler)
1. **L1853** — global `keydown` (`window.addEventListener`): `if (e.key === 'Escape') {` →
   - `state.recipient.open` → `closeRecipientView()` (**recipient = surface บนสุด · ปิดก่อน** · L1854)
   - else `state.modal.open` → `closeModal()`
   - else `state.drawer.open` → `closeDrawer()`
2. **L2286** — combobox `comboKey()`: `else if(e.key==='Escape'){ comboClose(key); }` — Esc ปิดเฉพาะ combobox list ที่ focus อยู่

> ลำดับปิด: (combobox list ที่ focus) → recipient → modal → drawer

### Overlay lifecycle
- **openDrawer** L1806: set `state.drawer` → `render()` → rAF add `.is-open`
- **closeDrawer** L3133: remove `.is-open` + `setTimeout 280ms` reset state + `state.dd={}` + render
- **openModal** L1822 / **closeModal** L3135: rAF add is-open · closeModal `setTimeout 200ms` reset
- **openRecipientView** L2799 / **closeRecipientView** L2805: rAF add `.is-open` · close = remove + `setTimeout 240ms` reset
- **combobox teardown:** `teardownCombos()` L2312 (เคลียร์ `#overlay-root` + `CB={}`) เรียกต้น `render()`
- **focus/scroll restore:** `preserveRenderState()` L1986 / `restoreRenderState()` L2004 (Rule #29)
- click-outside: drawer backdrop L1702 · modal backdrop L1708 · combo DSP-04 bubble-phase

### ⭐ Double-submit guard (FIX-04 · `guardBusy(ev)` L2151)
ปุ่ม submit เขียนข้อมูลทุกตัวเรียก `guardBusy(event)` หลัง validation ผ่าน → ถ้ากำลัง busy คืน false (ไม่ทำซ้ำ) · มิฉะนั้นตั้ง busy + ปุ่ม disabled + spinner "กำลังบันทึก…" · ปลด 500ms (ดู §5)

### recipient submit guard (`submitRecipient(ev)` L2812)
1. `!verified` → toast "กรุณายืนยันตัวตนก่อนส่งคำตอบ" (warning) → หยุด
2. เลือกไม่ครบทุก purpose (`missing.length`) → toast "กรุณาเลือกยินยอม/ไม่ยินยอมให้ครบทุกวัตถุประสงค์" (warning) → หยุด
3. `guardBusy(ev)` (FIX-04) → ถ้า busy หยุด
4. ผ่าน → snapshot choices → `closeRecipientView()` → (60ms) `applyAnswers()` L2762 (สร้างทะเบียน granted/declined + supersede คู่เดิม L2789 + evidence 5 + history + `emitConsequence` CSQ)

### ⭐ Closed-request guards (FIX-01/FIX-05)
- `applyAnswers` L2764: ถ้า status ไม่ใช่ draft/pending → toast **"คำขอนี้ปิดแล้ว — ตอบซ้ำไม่ได้"** (กัน evidence chain ถูกเขียนทับ) · ตอบสำเร็จ set `r.status='answered'` + `r.answeredAt` (L2785)
- `sendVia` L2751: ถ้าไม่ใช่ draft/pending → toast **"คำขอนี้ปิดแล้ว"**
- `recipientViewHTML` L2826: ถ้าไม่ใช่ draft/pending → หน้า "คำขอนี้ปิดแล้ว" (ดู §4 P-05)
- `doWithdraw` L3034: ถ้า `effStatus!=='granted'` → toast **"รายการนี้ไม่อยู่ในสถานะยินยอม"** (กัน history/CSQ ซ้ำ)

### Positioning
- drawer = fixed right slide · modal = fixed center · recipient = fixed inset0 · toast = fixed · combo-list = portal absolute (flip-up)

---

## §8 · State-Driven UI Matrix

### Persona / permission model (`.demo-strip` L1683 · `PERM()` L2147)
> demo-strip มุมซ้ายล่าง = **persona switch (prototype only #105)** — 3 ปุ่ม Officer/DPO/Auditor (`setPersona(p)` L3088 → `state.persona` → `render()` + `syncPersonaUI` L3089)

| persona | reqCreate | send | sign | withdraw | purpose (สร้าง/แก้/ปิด) |
|---|:--:|:--:|:--:|:--:|:--:|
| `officer` (default) | ✅ | ✅ | ✅ | ✅ | ❌ |
| `dpo` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `auditor` | ❌ | ❌ | ❌ | ❌ | ❌ (read only) |

- `PERM()` L2147: `reqCreate/send/sign/withdraw = p!=='auditor'` · `purpose = p==='dpo'`

### ⭐ Persona guards — สองชั้น (FIX-02 · defence-in-depth)
1. **Render-level (ซ่อนปุ่ม):** `headActions` L2405 (ปุ่มสร้างคำขอ/วัตถุประสงค์) · reqView send buttons (`p.send` L2730) · reqView sim block (`p.sign` L2738) · purView action (`perm.purpose` L2934) · consentView ถอน/ต่ออายุ (`perm.withdraw`/`perm.reqCreate` L2975/2976) · chip "เฉพาะ DPO แก้ไขได้" (L2410)
2. **In-function guard (กันเรียกตรง):** ทุก mutation ตรวจ `PERM()` ซ้ำเป็นด่านแรก แล้ว toast **"สิทธิ์ไม่พอสำหรับบทบาทนี้"** — `submitReqCreate` L2684 · `sendVia` L2750 · `applyAnswers` L2763 · `doWithdraw` L3033 · `doPublishVersion` L3055 · `doClosePurpose` L3071 (comment: prototype mirror ของ `sec.can()` จริงตอน prod)

### resolve verdict (`resolveConsent` L2582 · ตอบ HTTP 200 เสมอ)
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

### consent effective status (`effStatus` L2225)
- `granted` + `expiresAt` เลยวันนี้ → **`expired`** (คำนวณสด) · `policyStale` L2226 = granted แต่ `policyVersion < currentVer` · `nearExpiry` L2227 = granted และเหลือ 0–30 วัน · `isActive` L2228 = `effStatus==='granted'`

### recipient choice (`state.recipient.choices` L2801)
- ต่อ purpose = `null` (default) / `'grant'` / `'decline'` (`setRecipientChoice` L2809) · verify = false/true · expanded (doc) ต่อ code · `_busy` (FIX-04) = double-submit guard flag

---

## §9 · Microcopy (verbatim)

### Toast (`showToast(message,variant,durationMs=2800)` L1839 · templates verbatim · `+ ตัวแปร` = concat)
| variant | ข้อความ | anchor |
|---|---|---|
| success | `ส่งออก {n} รายการเป็น CSV แล้ว` | L2505 |
| warning | `เลือกให้ครบทั้ง 3 ช่องก่อนตรวจสิทธิ์` | L2578 |
| warning | `สิทธิ์ไม่พอสำหรับบทบาทนี้` (FIX-02) | L2684/2750/2763/3033/3055/3071 |
| warning | `เลือกเจ้าของข้อมูลก่อน` | L2685 |
| warning | `เลือกช่องทางก่อน` | L2686/2754 |
| warning | `เลือกวัตถุประสงค์ที่รองรับช่องทางนี้อย่างน้อย 1 ข้อ` | L2688 |
| success | `สร้างคำขอ {r.id} พร้อมลิงก์และ QR แล้ว` | L2692 |
| warning | `คำขอนี้ปิดแล้ว` (FIX-05) | L2751 |
| success | `บันทึกการส่งทาง{ช่องทาง} (จำลอง — ไม่ส่งจริง)` (`SIM_NOTE` L2155) | L2753 |
| warning | `คำขอนี้ปิดแล้ว — ตอบซ้ำไม่ได้` (FIX-01) | L2764 |
| success | `บันทึกคำตอบแล้ว · ยินยอม {n} · ปฏิเสธ {m} (เก็บหลักฐานครบ 5 อย่าง)` | L2787 |
| warning | `กรุณายืนยันตัวตนก่อนส่งคำตอบ` | L2813 |
| warning | `กรุณาเลือกยินยอม/ไม่ยินยอมให้ครบทุกวัตถุประสงค์` | L2815 |
| warning | `กรอกชื่อวัตถุประสงค์` | (submitPurCreate) |
| warning | `เลือกช่องทางอย่างน้อย 1` | (submitPurCreate) |
| warning | `อายุต้องอยู่ระหว่าง 1–120 เดือน` | (submitPurCreate) |
| warning | `ต้องแนบเอกสาร PDPA` | (submitPurCreate / L3057) |
| success | `สร้างวัตถุประสงค์ {code} แล้ว` | L2887 |
| info | `ไม่มีรายการที่กระทบ` | L2943 |
| success | `สร้างคำขอความยินยอมใหม่ {n} รายการ (นโยบายเวอร์ชันปัจจุบัน)` | L2947 |
| warning | `รายการนี้ไม่อยู่ในสถานะยินยอม` (FIX-05) | L3034 |
| warning | `กรอกเหตุผล` | L3036 |
| warning | `เลือกช่องทางที่ลูกค้าแจ้งมา` | L3037 |
| success | `ถอนความยินยอมแล้ว — มีผลทันทีในคำขอถัดไป` | L3042 |
| success | `ออกเอกสาร v{nv} แล้ว · {stale} รายการต้องขอความยินยอมใหม่` | L3063 |
| success | `ปิดวัตถุประสงค์ {code} แล้ว` | L3075 |
| warning | `ไม่มีคำขอที่รอตอบ — สร้างคำขอก่อน` | L3084 |
| info | `เมนูนี้เป็นบริบทของโมดูลอื่น (เดโมไม่รวมขอบเขต)` | L3094 |
| error | `ดาวน์โหลดไม่สำเร็จในสภาพแวดล้อมนี้` | (util) |
| success | `ดาวน์โหลด QR ของ {id} แล้ว (บันทึกการนำลิงก์ออก)` | (util) |
| success | `ดาวน์โหลดเอกสาร (ต้นแบบ): {names}` | (util) |
| success | `คัดลอกลิงก์แล้ว` | (util) |
| error | `คัดลอกไม่สำเร็จ` | (util) |

> **busy-state label (FIX-04):** ปุ่ม submit ขณะทำงาน → `กำลังบันทึก…` (`guardBusy` L2152)
> **SIM_NOTE (FIX-07 · L2155):** ` (จำลอง — ไม่ส่งจริง)` = ค่าคงที่ต่อท้าย toast การส่ง (demo) — prod ตัดออก

### Empty states (verbatim)
| title | desc | ที่ไหน |
|---|---|---|
| ไม่พบความยินยอม | ลองล้างตัวกรอง หรือสร้างคำขอความยินยอมใหม่ | registry |
| ยังไม่มีคำขอ | สร้างคำขอความยินยอมให้ลูกค้า | requests |
| ไม่พบวัตถุประสงค์ | ลองค้นด้วยคำอื่น | purposes |
| (resolve ก่อนกรอก) | เลือกเจ้าของข้อมูล · วัตถุประสงค์ · ช่องทาง แล้วกดตรวจสิทธิ์ | resolve (`.rz-empty`) |
| (combobox ว่าง) | ไม่พบรายการ | `.combo-list` |

### Key labels / notes (verbatim)
- H1 (คงที่ทุกแท็บ · L2394): **"ความยินยอม PDPA"**
- resolve field-help: "ค่าเริ่มต้นคือ **ส่งไม่ได้** — ไม่มีรายการในทะเบียน = ไม่อนุญาต (BR-04) · การไม่ตอบ ≠ ปฏิเสธ (BR-08)"
- **หลักฐาน 5 อย่าง (BR-15 · `consentViewDrawer` L2957–2962 · `evItem` L2980):** เวลาที่ตอบ · ช่องทางที่ส่งคำขอ · วิธียืนยันตัวตน · เวอร์ชันนโยบาย · ไอพีและอุปกรณ์
- recipient (L2824/2835): "**จำลอง** — นี่คือหน้าที่เจ้าของข้อมูลเห็นเมื่อเปิดลิงก์ (ไม่ใช่การส่งจริง)" · "โปรดอ่านเอกสารแต่ละวัตถุประสงค์ แล้วเลือกว่าจะยินยอมหรือไม่ยินยอม"
- recipient closed (FIX-01 · L2829–2830): "คำขอนี้ปิดแล้ว" / "คำขอความยินยอมนี้ได้รับคำตอบ เมื่อ {answeredAt} — หากต้องการเปลี่ยนแปลง โปรดติดต่อบริษัท"
- recipient verify (L2852–2853): "ฉันคือเจ้าของข้อมูลและได้อ่านเอกสารแล้ว" / "ยืนยันตัวตน (ต้นแบบ) — จำเป็นก่อนส่งคำตอบ"
- purpose versions section (L2929): "เอกสาร (เวอร์ชัน — แก้ไม่ได้ · BR-05)" · timeline (L2970): "ประวัติ (เพิ่มอย่างเดียว · BR-16)"
- reqView sent-version (FIX-03 · L2717/2718): "เวอร์ชันที่ส่ง" · "เอกสารที่เจ้าของข้อมูลเห็นตอนเซ็น" · warning "ส่ง v{n} · ปัจจุบัน v{m} — พิจารณาส่งคำขอใหม่" (L2716)

---

## §10 · Data Binding & BACKEND anchors

> HTML ใช้ mock in-memory (`state.purposes` · `state.consents` · `state.requests` · `SUBJECTS` · `CHANNELS`) · **เนื้อหา = เอกสารอัปโหลด versioned** (`versions[].docName/docType/body` · `curDoc` L2197)

| UI action (fn) | plug → FRD API |
|---|---|
| ทะเบียน list + filter (`registryBody`/`filteredConsents`) | GET `/consent/registry?...` (F058-API-14) |
| consent detail (`openConsentView`) — หลักฐาน 5 + timeline | GET `/consent/registry/:id` (F058-API-15) |
| requests list / view (`requestsBody`/`openReqView`) | GET `/consent/requests[/:id]` (F058-API-08) |
| สร้างคำขอ single-screen (`submitReqCreate`) | POST `/consent/requests` (F058-API-07) |
| ส่ง/ส่งซ้ำ (`sendVia`/`resendOther`) · **snapshot policy ver ณ ส่ง** (`snapshotVers` FIX-03) | POST `/consent/requests/:id/send` (F058-API-09) |
| copy link / ดาวน์โหลด QR (`copyLink`/`downloadQR`) | log นำลิงก์ออก (F058-API-10) |
| ดาวน์โหลดเอกสาร (`downloadPdfForm`) | เอกสารเวอร์ชันปัจจุบัน (F058-API-11) |
| purpose list + stats (`purposesBody`) · สร้าง (`submitPurCreate`) | GET / POST `/consent/purposes` (F058-API-01/02 · dpo) |
| purpose view (`openPurView`) · ออกเวอร์ชัน (`doPublishVersion`) · ปิด (`doClosePurpose`) | GET `/consent/purposes/:code` · POST `/versions` · POST `/close` (F058-API-03/04/05) |
| document viewer (`viewPolicy(code,ver)`) | โหลด body เอกสารเวอร์ชันที่ระบุ (F058-API-03) |
| recipient load / submit (`openRecipientView`/`submitRecipient`→`applyAnswers`) | GET `/consent/recipient/:token` · POST `/answer` (F058-API-12/13) |
| ถอน (`doWithdraw`) | POST withdraw (F058-API-17) + CSQ `consent.withdrawn` (reversal_of=grantEvent · L3041) |
| ต่ออายุ (`openRenew`→reqCreate refOld) · ขอใหม่ (`reConsent` L2941) | POST (F058-API-19) — คำขอใหม่อ้างเดิม ไม่แก้ expiresAt เดิม |
| resolve (`resolveConsent`) | POST `/consent/resolve` (F058-API-20 · ตอบ 200 · never_asked ≠ 404) |
| ทุก grant/decline/withdraw/version/reconsent/close | `emitConsequence(...)` L2332 → **CSQ event → 7C Engine** (declare-only) |

- **Persona ↔ backend (FIX-02):** in-function `PERM()` guard = prototype mirror ของ `sec.can()` — prod ต้องบังคับสิทธิ์ที่ backend ตาม role จาก JWT (ไม่ใช่ `state.persona`)
- `exportCsv`/`downloadQR`/`downloadPdfForm`/`copyLink` = client-side utility (เดโม · toast จำลอง · **ไม่ส่งจริง** ตาม FN-40.3)

### Contract anchor comments (FIX-06 · **non-rendered** — comment ในโค้ด ไม่ใช่ UI)
- L7 (head): `<!-- CONTRACT (Feature List F058): resolveConsent = API ให้ F136 Broadcast … + F031 Customer 360 … · ทะเบียน consent + evidence = ฐานข้อมูลให้ F157 DSAR … display-only ไม่ mock หน้าจอ feature อื่น -->`
- L2561 (เหนือ `resolveBody`): comment ย้ำ `resolveConsent` เป็น API ให้ F136 ตรวจ opt-in ก่อนส่ง
- เป็น **cross-module contract anchor** ให้ dev/BA เห็นสัญญาข้ามฟีเจอร์ — ไม่มีผลต่อจอ (ไม่ต้อง render / ไม่ต้อง test บนหน้า)

---

## §11 · Traceability (Brief ↔ FRD ↔ HTML) + Drift Log

| Brief § | FRD (P/D/M · API · FN) | HTML anchor |
|---|---|---|
| §2.2 tab registry | P-01 · API-14/15 · FN-13/14/16 | `registryBody()` L2446 |
| §2.2 tab requests | P-02 · API-07/08/09 · FN-05/06/07/08/09 | `requestsBody()` L2512 |
| §2.2 tab purposes | P-03 · API-01/02/03/04/05 · FN-01/02/03/04 | `purposesBody()` L2542 · `purStatusPill()` L2540 |
| §2.2 tab resolve | P-04 · API-20 · FN-19/20 | `resolveBody()` L2565 · `resolveConsent()` L2582 |
| §4/§6 recipient view + closed-state | P-05 · API-12/13 · FN-10/11 | `recipientViewHTML()` L2821 (closed L2826) · `submitRecipient()` L2812 |
| §6 D-reqCreate (single-screen) | D-reqCreate · API-07 · FN-05 · **LOCK-07** | `reqCreateDrawer()` L2648 |
| §6 D-reqView (send/QR/doc + sent-version) | D-reqView · API-09/10/11 · FN-06/07/08/09 | `reqViewDrawer()` L2703 · sent-version panel L2711 |
| §6 D-purCreate (upload) | D-purCreate · API-02 · FN-01 | `purCreateDrawer()` L2860 |
| §6 D-purView (versions) | D-purView · API-03/04/05 · FN-02/03/04 | `purViewDrawer()` L2916 |
| §6 D-consentView (evidence5+timeline) | D-consentView · API-15/17/19 · FN-12/15/17/18 | `consentViewDrawer()` L2952 |
| §6 D-c360 (Customer 360) | D-c360 · FN-14 (E1) | `c360Drawer()` L2986 |
| §6 M-policy (DSP-01) | M-policy/doc · API-03 · DSP-01 | `viewPolicy()` L3015 · `policyModal()` L3016 |
| §6 M-withdraw / M-newVersion / M-closePurpose / M-renew | M-* · API-04/05/17/19 · FN-02/04/15/17 | L3026/3048/3065/2981 |
| §5/§7 busy-state (FIX-04) | 05_RULES double-submit / usability | `guardBusy()` L2151 · `.spin`/`spin360` L1518 |
| §7/§8 persona guards (FIX-02) | §1.5 COSO · roles · sec.can() | `PERM()` L2147 · in-fn guards (§8) |
| §8 persona/PERM | §1.5 COSO · roles | `.demo-strip` L1683 · `PERM()` L2147 |
| §1 z / DSP-01/03 | §1.0 z-registry · DSP-01/03 | `.modal-backdrop` z=`--z-portal` L1372 · `.combo-list` z=`--z-pop` L1476 |

### ⚠️ Drift Log
| # | ชนิด | รายการ | หมายเหตุ / ข้อเสนอ |
|---|---|---|---|
| D-1 | note (label mismatch) | 01_UI §1.0 z-registry เขียน "`--z-pop` 80 = document viewer modal" แต่ **observed:** doc viewer modal ใช้ `.modal-backdrop` z=`--z-portal`**60** (L1372) ส่วน `--z-pop`**80** = `.combo-list` portal (L1476) | ทั้งคู่ยัง**เหนือ drawer(55)** — DSP-01 satisfied · ไม่ใช่ bug · เสนอ BA แก้ label ใน 01_UI |
| D-2 | note (by-design) | route แบบ hash `#/consent/<tab>` — extractor เห็นแค่ `consent` | จงใจ · refresh-safe · H1 คงที่ · ตรง 01_UI P-01..04 |
| D-3 | HTML-only (base-kit ค้าง) | overlay `.user-menu` · `.ss-list` · `.menu-fixed` มี CSS/handler แต่ **ไม่ถูก wire** (ใช้ custom `.combo`) | base-kit residual — ไม่ใช่ gap · prod อาจตัด CSS ที่ไม่ใช้ |
| D-4 | HTML-only (prototype) | `.demo-strip.demo-only` persona switch + sidebar sibling `decorativeNav()` + `SIM_NOTE`/`.demo-only` blocks (FIX-07) | prototype-only (#105) — prod strip `.demo-only` · persona จาก JWT · ดู §DEMO-ONLY |
| D-5 | FRD-only (ASSUMED) | id-verify จริง (OQ-03) · ขึ้นทะเบียนด่านบังคับสิทธิ์ F143 (OQ-04 · BR-22) · CSQ SecC pipe (OQ-CSQ-02) · caller cache ≤5 นาที (BR-21) | **BLOCKING/backend contract** — mock: verify=checkbox · resolve=simulator · CSQ=declare-only · เคาะก่อน prod (→ PROPOSALS) |
| D-6 | FRD-only | notification | 01_UI §1.6 = ไม่มี notification event (ntf ไม่เลือก) · bell static — ตรง observed |
| D-7 | note (BA-gate fix) | FIX-01..08 (busy-state · sent-version stale-warn · recipient closed-state · demo-only marker · purStatusPill · persona guards render+in-fn · contract anchors · closed-request guards) | **AS-BUILT รอบนี้สะท้อนครบ** · contract anchors (FIX-06) = non-rendered comment · ต้อง re-run step 3·4·5 (C3.2) ก่อนปิด |

**สรุป: ไม่มี business drift ที่ทำให้ HTML ขัด FRD** — drift = label mismatch (D-1), by-design routing (D-2), base-kit residual (D-3), prototype persona/demo-only (D-4), backend/ASSUMED contract (D-5), notification จงใจไม่มี (D-6), BA-gate fixes ที่สะท้อนครบแล้ว (D-7)

---

## §DEMO-ONLY · 🔴 รายการที่ prod build ต้อง strip / เปลี่ยนแหล่งข้อมูล (FIX-07)

> prod build **ลบทุก element ที่มี class `.demo-only`** + คอมเมนต์ `<!-- DEMO-ONLY -->`

| # | element | anchor | prod behavior |
|:--:|---|---|---|
| 1 | **demo-strip** `.demo-strip.demo-only#demoStrip` (Officer/DPO/Auditor · `setPersona`) | L1683 | **ลบทั้งแถบ** (`.demo-only`) — persona/role จาก JWT/สิทธิ์จริง |
| 2 | **in-drawer preview** `.demo-only` block "มุมมองผู้รับ (จำลองลิงก์)" + ปุ่ม `openRecipientView` | L2739 | ลบทั้ง block — prod ส่งลิงก์ให้เจ้าของข้อมูลเปิดเอง |
| 3 | **recipient sim-bar** `.rcp-simbar.demo-only` ("จำลอง — …") | L2823 | ลบแถบ — หน้าจริงเปิดจากลิงก์ที่ส่งให้เจ้าของข้อมูล (ไม่มี ERP chrome) |
| 4 | **SIM_NOTE** ` (จำลอง — ไม่ส่งจริง)` ต่อท้าย toast การส่ง | L2155/2753 | ตัดออก — การส่งจริงผ่าน API (F058-API-09) |
| 5 | **sidebar sibling menus** `decorativeNav()` | L3094 | เมนูโมดูลอื่นจริง (นอก scope) — ไม่ใช่ toast stub |
| 6 | **client-side utility** exportCsv / downloadQR / downloadPdfForm / copyLink (toast จำลอง) | L2499/util | prod = API จริง (F058-API-10/11) |
| 7 | **recipient verify = checkbox ต้นแบบ** (`toggleRecipientVerify`) | L2810 | prod = id-method จริง (OQ-03 BLOCKING) |
| 8 | **resolve = simulator** (`resolveConsent` in-memory) | L2582 | prod = POST `/consent/resolve` จริง (สัญญาฟิลด์ล็อก BR-20) |

**คงไว้ใน prod:** ทะเบียน/หลักฐาน 5/timeline · document viewer (versioned) · recipient read+sign flow + closed-state page (FIX-01) · sent-version stale-warn (FIX-03) · busy-state (FIX-04) · resolve UI · statusPill vocabulary · default-deny (never_asked) · closed-request/persona guards (FIX-01/02/05)

---

## §12 · Diff จากเวอร์ชันก่อน (BA-gate fixes FIX-01..08)

> ไม่มีสำเนา HTML ก่อน BA-gate แยกไว้ให้ diff เชิงบรรทัด — สรุปชุด FIX ที่ทำให้ HTML โต ~60 บรรทัด (จาก ~3080 → 3142)

| FIX | สิ่งที่เพิ่ม/แก้ | anchor | ผลต่อ UI |
|:--:|---|---|---|
| FIX-01 | recipient closed-state page + `applyAnswers` ปิดคำขอเมื่อตอบ (`answeredAt`) + guard ตอบซ้ำ | L2826/2764/2785 | ลูกค้าเปิดลิงก์ซ้ำ = หน้า "คำขอนี้ปิดแล้ว" (ไม่มีฟอร์ม) — กัน evidence เขียนทับ |
| FIX-02 | persona guard สองชั้น (render + in-function `PERM()`) + toast "สิทธิ์ไม่พอสำหรับบทบาทนี้" | §8 · L2684+ | mutation ทุกตัวกันสิทธิ์ทั้งซ่อนปุ่มและกันเรียกตรง |
| FIX-03 | sent-version panel + `snapshotVers` + `.near-tag` stale warning + `viewPolicy(code,ver)` | L2711–2720/2748 | reqView แสดงเวอร์ชัน ณ ส่ง + เตือนเมื่อมีเวอร์ชันใหม่กว่า |
| FIX-04 | `guardBusy` + spinner `loader-2 .spin`/`@keyframes spin360` + "กำลังบันทึก…" | L2151/1518 | ปุ่ม submit disabled + spinner ระหว่างบันทึก (กัน double submit) |
| FIX-05 | closed-request guards (`sendVia`/`doWithdraw`) | L2751/3034 | ส่ง/ถอน เฉพาะสถานะที่ถูกต้อง — toast เตือน |
| FIX-06 | contract anchor comments (non-rendered) | L7/L2561 | สัญญาข้ามฟีเจอร์ในคอมเมนต์ — ไม่มีผลจอ |
| FIX-07 | `.demo-only` class marker + `SIM_NOTE` const + DEMO-ONLY comments | L1683/2155/2739/2823 | prod strip ได้ทีเดียวด้วย `.demo-only` |
| FIX-08 | `purStatusPill()` helper | L2540 | pill สถานะเดียวต่อ cell ใน purposes tab |

---

## §13 · 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)

> ที่เดียวที่อนุญาตให้คิดเอง (R1) — ต่อไปนี้ **ไม่มีในจอ** เป็นข้อเสนอ ไม่ใช่สเปคที่ต้องทำ

1. **แก้ label z-registry ใน 01_UI (D-1)** — doc viewer modal = `--z-portal`(60), combo portal = `--z-pop`(80) — กัน dev ตั้ง z ผิด
2. **id-verify จริง (OQ-03 · BLOCKING)** — recipient verify ปัจจุบัน = checkbox ต้นแบบ · ต้องเคาะวิธียืนยันตัวตน (OTP/e-KYC/ลิงก์เฉพาะตัว) ก่อน dev
3. **ขึ้นทะเบียนด่านบังคับสิทธิ์ (OQ-04 · BR-22)** — `/consent/*` ผูก Security wave W2 — resolve เป็น gate ก่อนส่งทุกครั้ง
4. **caller cache contract (BR-21)** — สัญญาฝั่งผู้เรียก cache ≤5 นาที + ล้างเมื่อถอน (document ใน FRD API)
5. **base-kit residual cleanup (D-3)** — `.user-menu`/`.ss-list`/`.menu-fixed` ไม่ถูก wire — prod ตัด CSS ที่ไม่ใช้ได้
6. **backend enforce persona (FIX-02 ต่อยอด)** — in-function `PERM()` เป็น mirror เท่านั้น · prod ต้องบังคับที่ backend ตาม JWT role ไม่พึ่ง `state.persona`
7. **consent receipt PDF (E3)** — scope ใหม่ เลื่อน (ทำได้ที่ step 2 / wave DSAR)
