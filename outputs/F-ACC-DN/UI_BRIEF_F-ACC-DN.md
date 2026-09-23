# UI Brief (AS-BUILT) — ใบลดหนี้ผู้ขาย (Debit Note) · F-ACC-DN / F097

> **EXTRACTION-BASED (Iron Rule R1)** — ทุกบรรทัดสกัดจาก `F-ACC-DN_debit-note.html` (source of truth) เท่านั้น · ทุก claim ชี้ selector / function / ข้อความจริง (+เลขบรรทัด) ได้ · ข้อเสนอที่ไม่ได้ AS-BUILT อยู่ §13 เท่านั้น
> คู่กับ: **HTML (จอจริง)** + **FRD Pack** (`FRD_Pack/` — anchor ระบบ) + บรีฟนี้ (design intent)
> โครง/ความลึก mirror จากพี่น้อง **F-ACC-CN** (Credit Note · ฝั่งขาย) ที่อนุมัติแล้ว — ฝั่งนี้คือ Debit Note (ฝั่งซื้อ/AP)

---

## §0 · Document Control + Pairing

| | |
|---|---|
| Feature | F-ACC-DN · F097 · ใบลดหนี้ผู้ขาย (Debit Note · ฝั่งซื้อ/AP) |
| HTML source | `outputs/F-ACC-DN/F-ACC-DN_debit-note.html` · 1268 บรรทัด · single-file SPA (vanilla JS) |
| `<title>` | `ใบลดหนี้ผู้ขาย (Debit Note) · CUBE 4.0` (บรรทัด 6) |
| Generator | html-generator-v9.1 · Pattern Q Transaction Document Archetype (locked to SO) · B2 v2 line editor · Z-Index Registry (#62) |
| PREFLIGHT | บรรทัด 1263–1267 · `audit.sh FAIL=0 WARN=2` (Token font-size raw + Rule#47 stepper .step-dot = canonical residual) · `node --check PASS` · self_audit z_adhoc=0 · undefined_handlers=0 |
| FRD Pack | `FRD_Pack/` (00_OVERVIEW · 01_UI · 02_API · 03_LOGIC · 04_DB · 05_RULES · 06_TESTS · 07_LOCKED · INDEX) — paired ✅ · 17 API · 17 BR · 21 FN (FN-01..18 + FN-90/91/92 · **NO FN-40**) |
| Kernel | Q-DOC KERNEL (บรรทัด 953–1258) generic · feature file ให้ config object `DOC` (บรรทัด 874–939) + data + hooks |
| Personas | 4 คน (บรรทัด 754–759) — DEMO harness สลับบทบาท (flag §5.9): เจ้าหน้าที่เจ้าหนี้ / ผจก.จัดซื้อ / ผจก.บัญชี / CFO |
| สถานะ drift | ดู §11 Drift Log — 0 blocking; 6 informational (dead CSS `.suggest-list`; `couponAmt` engine-carry; no `:has` scroll-lock; FRD-only API-14 revise-doc; FRD-only resend; API-15 config inline mock) |
| Mirror delta vs CN | +FN-20 (เครดิตคงเหลือกับผู้ขาย) · +FN-21 (vendorCn → กลับภาษีซื้อ ม.82/10) · เพดาน = `dnRoom` ไม่หัก `paid` (FIX-01) · reason RTV/OVERPRICE/SHORT · ไม่มี revise-doc/resend |

---

## §1 · Design Tokens AS-BUILT

**`:root`** (บรรทัด 32–68) — CUBE NATIVE Admin CI v2 / Warm Light

| กลุ่ม | token → ค่า |
|---|---|
| Brand | `--c-primary` #FF3B30 · `--c-primary-h` #E62E24 · `--c-navy` #111111 · `--c-teal` #1F9D55 · `--c-purple` #FF9A1F (ใช้เป็นสีตัวเลขภาษี/สถานะ sent) · `--c-slate` #73757B |
| พื้น/เส้น | `--c-off-white` #FAF8F5 · `--c-white` #FFFFFF · `--c-border` #DEDAD4 · `--c-border-soft` #EFEBE6 |
| ตัวอักษร | `--c-text` #111111 · `--c-text-mute` #73757B · `--c-text-soft` #9A9CA2 |
| สถานะ | `--c-warning` #E8870F · `--c-danger` #E62E24 + alpha ramps `--c-primary-08/12/18`, `--c-teal-08`, `--c-warning-08`, `--c-danger-08` |
| รัศมี | `--r-sm` 6px · `--r` 10px · `--r-lg` 14px |
| เงา | `--sh-sm` · `--sh-md` · `--sh-lg` · `--sh-xl` (drawer/modal ใช้ xl) (บรรทัด 58–61) |
| shell | `--sw` 224px (sidebar) · `--hh` 52px (topbar) |

**Fonts** (บรรทัด 7–8): Noto Sans Thai (fonts.googleapis.com) + Satoshi (api.fontshare.com) · body stack `'Noto Sans Thai','Satoshi',…` (บรรทัด 72) · หัวข้อ h1–h4 = Noto Sans Thai ก่อน (บรรทัด 79) · **CDN 0 แหล่งสำหรับ JS/icon** (icon inline `ICONS` object บรรทัด 744–745, ไม่มี Tailwind/lucide CDN — shim `.w-*/.h-*` บรรทัด 11–18)

**Scrollbar** (บรรทัด 85–92): `scrollbar-gutter: stable` (บรรทัด 86) กันหน้าขยับ · webkit thumb 8px (บรรทัด 85–88) · number spinner ปิด (90–92)

### z-index map (สูง → ต่ำ) — v9.1 Z-Index Registry (บรรทัด 64–67)

| token | ค่า | ใช้กับ |
|---|--:|---|
| `--z-toast` | **100** | `#toast-root` (บรรทัด 742) |
| `--z-portal` | 70 | `.combo-pop` combobox portal (637) · row-menu `.menu-fixed` (openRowMenu 1241) · `.suggest-list` legacy (374) · `.hint` tooltip (23) |
| `--z-modal` | 60 | `.modal-overlay` + modal card (`> *:not(.backdrop)` บรรทัด 506) |
| `--z-drawer` | 51 | `.overlay-wrap` + `.drawer-panel` (487/496) |
| `--z-backdrop` | 50 | `.backdrop` (488) |
| `--z-dropdown` | 40 | (reserved — inline dropdown) |
| `--z-shell` | 20 | `.sb` sidebar (บรรทัด 99 `position:sticky` แต่ z มาจาก registry) |
| `--z-sticky` | 10 | `.top` topbar (196) |
| `--z-content` | 1 | base |

> **ต่างจาก CN:** CN ตั้ง `--z-toast:80` และ row-menu hard-code 80 · **DN ตั้ง `--z-toast:100`** และ row-menu ใช้ `var(--z-portal)` 70 (บรรทัด 1241) — ทั้ง toast/portal/modal/drawer/backdrop มาจาก registry ใน `:root` ล้วน (self_audit `z_adhoc=0`)

**กฎ overlay ordering (DSP-01/DSP-08, บรรทัด 485–506):** toast(100) > portal(70) > modal(60) > drawer(51) > backdrop(50) — combobox / DOA slot-picker ต้องลอยเหนือ **ทั้ง** modal และ drawer เสมอ (slot-picker เปิดในกล่อง submit modal) · modal card ต้องเหนือ `.backdrop` (บรรทัด 506, fix DSP-08 v9.1 regression: การ์ด z:auto ทำให้คลิกทะลุ backdrop แล้ว modal ปิดเอง)

---

## §2 · Route Map (hash SPA)

Router: `getRoute()` (บรรทัด 1250) · `navigate(path)` = `location.hash = '#/'+path` (บรรทัด 1251) · `hashchange → render()` (บรรทัด 1252) · boot guarded `__booted` (บรรทัด 1253–1255)

| Route | name | หน้าจอ | handler |
|---|---|---|---|
| `#/list` (หรือว่าง) | `list` | หน้ารายการ (default) | `renderListPage()` (บรรทัด 1213) |
| `#/create` · `#/create/dup-<id>` | `create` | drawer wizard 5 ขั้น (ใหม่/ทำสำเนา) | `openCreateDrawer(null, from)` (บรรทัด 1065) |
| `#/edit/:id` | `edit` | drawer wizard (แก้ร่าง เริ่ม step 2) | `openCreateDrawer(id)` (บรรทัด 1065–1066) |
| `#/view/:id` | `view` | drawer 5 แท็บ | `openViewDrawer(id)` (บรรทัด 1123) |

**Refresh-safety:** `render()` (บรรทัด 1256) เรนเดอร์ list page เป็น base เสมอ แล้ว `closeAllOverlays()` (1257) → เปิด overlay ตาม route — refresh ที่ `#/view/:id` = เห็น list + drawer ซ้อน (ไม่ค้างจอเปล่า) · route ที่ไม่รู้จัก → `{name:'list'}` (fallback บรรทัด 1250) · boot ครอบ `try/catch` โชว์ "Boot error:" (บรรทัด 1254)

---

## §3 · Layout Shell

`.shell` = grid `224px 1fr` (บรรทัด 97) · full-height, overflow ในแต่ละ pane

- **Sidebar `.sb`** (บรรทัด 99–183, 690–728): navy #111111, `--z-shell`, sticky · logo `CUBE 4.0 / Accounting` · เมนู `.sb-item` จัดกลุ่ม `.sb-grp` (accounting / บัญชี·ตั้งค่า / เจ้าหนี้ AP / บัญชีทั่วไป / การเงิน / Policy Center) · item ที่ active = `data-feature="dn"` "ใบลดหนี้ผู้ขาย" (บรรทัด 709) · badge "My Approval 3" (บรรทัด 698) · footer `© 2026 CUBE 4.0 · F-ACC-DN` (บรรทัด 727) · **One-Feature-One-Menu** (PREFLIGHT: AR group removed)
- **Topbar `.top`** (บรรทัด 189–197, 730–737): 52px, breadcrumb `Accounting › ใบลดหนี้ผู้ขาย` (`.top-bc`) · ปุ่มแจ้งเตือน (`.top-icon-btn` + red dot บรรทัด 733) · **DEMO persona switch** (`.demo-wrap.demo-only[data-demo="persona-switch"]` บรรทัด 734 — flag §5.9) · user chip `#uc-n/#uc-r/#uc-av` (บรรทัด 735, อัปเดตโดย `switchPersona`)
- **Page host** `#page-content` (บรรทัด 738) · overlay host `#overlay-root` (บรรทัด 741) · toast host `#toast-root` (บรรทัด 742)
- **Adaptive** (บรรทัด 657, 684): `body { min-width: 768px }` (v9.1 #97 desktop-base) · `.main { height:100vh; overflow:hidden }` (#96 · บรรทัด 658 — body ไม่ scroll, เนื้อ scroll ใน `.page`/`.table-wrap`/`.cw-body`/`.vw-body`) · ≤1180px → stat clamp 140px + drawer width `min(…,100vw)` (บรรทัด 684)

---

## §4 · Page Anatomy

### §4.1 · List (`#/list`) — `renderListPage()` (บรรทัด 1213–1226)
`.page-fill` → ph (title `DOC.titleFull` + sub `DOC.sub` + chip "N รายการ · รออนุมัติ N") → actions → stat-row → list-card

- **ph-actions** (บรรทัด 1216): `ส่งออก CSV` (`exportCSV()`) · `สร้างใบลดหนี้` (`DOC.createLabel`, `navigate('create')`)
- **stat-row `.stat-row`** (บรรทัด 669 · auto-fit `minmax(150px,1fr)` · `flex-shrink:0` เพื่อให้ตาราง list เต็มความกว้าง) — **5 การ์ด** (`.stat-card`, `DOC.listStats()` บรรทัด 884–885) คลิก = filter (`setStat`, toggle) ยกเว้นการ์ดเครดิต:
  1. `รออนุมัติ` (pen-tool · จำนวน + ฿ยอด)
  2. `ลดหนี้เดือนนี้ (อนุมัติแล้ว)` (file-minus · ฿ + N ใบ)
  3. `ฉบับร่าง` (file-text · "ยังไม่ส่งอนุมัติ")
  4. `ภาษีซื้อที่ลดเดือนนี้` (scale · ฿ + "ภ.พ.30 เดือน MM/YYYY")
  5. `เครดิตคงเหลือกับผู้ขาย` (wallet · ฿ + "N ราย · คลิกดู") — **`click: 'showVendorCreditDetail()'`** เปิด **modal** (ไม่ใช่ setStat filter) ⭐ DN-specific FN-20
- **toolbar `.toolbar`** (บรรทัด 1220–1224): search `#searchInput` placeholder `ค้นหาเลขที่ / ผู้ขาย / ใบตั้งหนี้ / RTV…` (prefix "ค้นหา" + `DOC.searchPh`) + 3 select filter (สถานะเอกสาร / เหตุผล / ผู้ขาย — `DOC.filterSelects()` บรรทัด 886) + `ล้างตัวกรอง` (`clearFilters`)
- **table `.table-wrap`** sticky thead (บรรทัด 663): head **10 คอลัมน์** (`DOC.listHead()` บรรทัด 890) เลขที่ · วันที่ · ผู้ขาย · ใบตั้งหนี้อ้างอิง · เหตุผล · สถานะเอกสาร · ลายเซ็น · ยอดลดหนี้ · ภาษีซื้อที่ลด · (เมนู) · sort ได้ที่ เลขที่/วันที่/ยอดลดหนี้ (`sortBy`) · row cells `DOC.rowCells()` (บรรทัด 891) · row click → `navigate('view/id')` · kebab `openRowMenu` (บรรทัด 1241)
- **table-foot**: page-size select 10/25/50 (default 25) + page info `N – M จาก K รายการ` (`getPageInfo` บรรทัด 1232)
- **empty**: `.empty-state` inbox icon + `ไม่พบรายการที่ตรงกับเงื่อนไข` + ปุ่ม `ล้างตัวกรอง` (บรรทัด 1227)

### §4.2 · Create/Edit wizard (`#/create`, `#/edit/:id`) — 5 ขั้น (locked)
`openCreateDrawer` (บรรทัด 1065) → `.overlay-wrap > .backdrop + .drawer-panel.wide` (max 1290px, บรรทัด 622) · stepper `renderStepperItem` (บรรทัด 1071, labels บรรทัด 1076) · body `.cw-body` · footer ย้อนกลับ/ยกเลิก/ถัดไป หรือ (step 5) บันทึกแบบร่าง/submit (บรรทัด 1079–1082)

| # | ขั้น (stepper label บรรทัด 1076) | render | สาระ |
|---|---|---|---|
| 1 | เลือกแหล่งที่มา | `renderStep1()` (บรรทัด 851) | 2 การ์ด: **"จากใบตั้งหนี้ (AP Invoice)"** (active) · "ลดหนี้ไม่อ้างใบ **ปิดไว้**" (disabled, คลิก → toast OQ-DN-01) + ตารางเลือกใบตั้งหนี้ที่ยังค้าง (`srcPickerCard` + `INV_COLS` บรรทัด 845 · กรอง `dnRoom>0` ผ่าน `invList` 844) |
| 2 | ข้อมูลหลักใบลดหนี้ | `renderStep2()` (บรรทัด 855) | ใบตั้งหนี้อ้างอิง(ro) · **มูลค่าที่ลดได้ของใบ**(ro, `dnRoom` + คงค้างจ่าย) · ผู้ขาย(ro) · วันที่ใบลดหนี้ · **เหตุผล** (select `DN_REASONS` 804) · ใบคืนสินค้า RTV (เฉพาะ RTV, `needRTV`) หรือ "วิธีลด" · **เลขที่ใบลดหนี้จากผู้ขาย** (`vendorCn`) ⭐ · **วันที่ได้รับใบลดหนี้ผู้ขาย** (`vendorCnDate`) ⭐ · เลขที่(ro "(ออกเลขเมื่ออนุมัติครบ)") · คำอธิบายเหตุผล(≥10) · หมายเหตุภายใน |
| 3 | รายการสินค้า | `renderStep3()` (บรรทัด 1009) | B2 v2 line editor (§5.3) — บรรทัด lock (มาจากใบเดิม), line-cap meta, `step3Block` ปุ่ม re-add บรรทัดที่ไม่ได้ลด (903), **ส่วนลดท้ายบิล** (§4.4), summary |
| 4 | เอกสารแนบ | `renderStep4()` (บรรทัด 1089) | `.upload-zone` + `<input type="file" id="att-file-input" multiple>` (real, บรรทัด 1090) · list ไฟล์ + `แนบไฟล์เพิ่ม` / ลบ (`pickAttachments`/`removeAttachment`) |
| 5 | ตรวจสอบและยืนยัน | `renderStep5()` (บรรทัด 1096) | review pairs (`DOC.reviewPairs` 908) + **DOA tier preview** (`DOC.step5Extra` บรรทัด 909) + ตารางรายการ + แนบ |

Validation ต่อขั้น: `wizardNext` (บรรทัด 1104) → step1 `DOC.step1Validate` (896) · step2 `DOC.step2Validate` (897, mark `.is-error` ราย field id `f-dnDate/f-reason/f-rtv/f-reasonText`) · step3 `validateLines` (บรรทัด 1109). Submit ปุ่ม (`#btn-primary-submit`) ถูก disable เมื่อ `createWizard._block` (บรรทัด 1081) = `DOC.blockReason()` (บรรทัด 907, ใส่ใน `title`).

### §4.3 · View drawer (`#/view/:id`) — 5 แท็บ (locked order) — `renderViewDrawer()` (บรรทัด 1127–1153)
`.drawer-panel` (max 920px, บรรทัด 492) · header: `DOC.titleFull` + `s.code || (ร่าง · ยังไม่ออกเลข)` + `docPill(status)` + head-chip "ถูกตีกลับ N ครั้ง" (`DOC.headChips` 923) + summary (`DOC.viewSummary` 924) · header icon-btn: ทำสำเนา(`dupRec`)/พิมพ์(→pdf tab)/ดาวน์โหลด PDF(mock toast)/ปิด (บรรทัด 1140–1143) · **status-guarded action buttons** `DOC.viewActions` (§8, บรรทัด 925, วางก่อน icon-btn + `VDIV`) · footer "แก้ไขล่าสุด … · [lock] อนุมัติแล้ว ล็อกแก้ไข" เมื่อ status ∈ approved/sent (บรรทัด 1151)

แท็บ (บรรทัด 1146, `tabBtn` บรรทัด 1125; domain tab แทรกจาก `DOC.domainTabs` 937):
1. **รายละเอียด** (`detail`, file-text) — `DOC.renderDetailTab` (บรรทัด 926): warn เกินคงเหลือ / cancel note / ข้อมูลเอกสาร (รวม vendorCn+วันที่รับ) / สถานะ / เอกสารอ้างอิง / ผู้ขาย / หมายเหตุ / สรุปยอด / รายการที่ลดหนี้ / แนบ / ข้อมูลระบบ
2. **ใบตั้งหนี้อ้างอิง · ภาษีซื้อ** (`ref`, git-compare) — `renderRefTab` (บรรทัด 940): ยอดใบเดิม/จ่ายแล้ว(PV)/ลดหนี้แล้ว/คงค้างก่อน-หลัง/ใบที่รอ(กันยอด)/**หักจากหนี้ค้าง**/**เครดิตคงเหลือกับผู้ขาย** · ตารางบรรทัดใบเดิม ลดแล้ว/ใบนี้ · **ผลกระทบภาษีซื้อ (2-state)**: "รอใบลดหนี้ผู้ขาย" vs "เดือนภาษี" ตาม `s.vendorCn && s.vendorCnDate` (ม.82/10, ปุ่ม `openVendorCn` 946) · **DEMO** จำลองอนุมัติใบลดหนี้อื่น (§5.9, `demoPay` 948) · รายการบัญชี (JE mock, demo-only note)
3. **PDF Preview** (`pdf`, file) — `renderPdfTab` (บรรทัด 1162): A4 `.a4` — หัวบริษัท 2BSimple · ผู้ขาย/อ้างอิง · ตาราง line + totals (มี end-bill row) · เหตุผล · 3 ช่องเซ็น (`ผู้จัดทำ/ผู้อนุมัติ/ผู้ขาย (ผู้รับ)` จาก `pdfParts.signLabels` 938) · ปุ่ม `ดาวน์โหลด`(mock toast) / `พิมพ์`(`window.print()`)
4. **ลายเซ็น / อนุมัติ** (`sign`, pen-tool) — `renderSignTab` (บรรทัด 1169): DOA entry + tier · timeline `.tl` ส่งอนุมัติ → ขั้น 1..N (roles + assignee chip + pill สถานะ + ปุ่ม อนุมัติ/ไม่อนุมัติ ที่ขั้นปัจจุบันถ้ามีสิทธิ) → ผลลัพธ์ · รอบก่อนหน้า (ตีกลับ, append-only)
5. **ประวัติ** (`history`, history) — `renderHistoryTab` (บรรทัด 1181): timeline `s.audit` (append-only, สีตามชนิด act)

### §4.4 · End-bill (ส่วนลดท้ายบิล) — FN-19 · `DOC.step3Block`/`renderStep3` (บรรทัด 1013–1014) + `totals()` (บรรทัด 996–1006)
- **การ์ด toggle** ใน step 3: `.toggle` เปิด/ปิด `createWizard.data.endbill.enabled` · ปิด → `value=0` (บรรทัด 1013)
- **โหมด ฿/%**: segmented 2 ปุ่ม `จำนวนเงิน (฿)` (`amount`) · `เปอร์เซ็นต์ (%)` (`percent`) เขียน `endbill.mode` · input `type=number` (+ป้าย ฿ หรือ %) → `updateLineSummaryOnly()` (บรรทัด 1014)
- **เพดาน (cap) + hard-warn**: `ebCap = max(0, after − coupon)` (บรรทัด 999) · แสดง "ลดได้สูงสุด ฿{ebCap}" · เกิน → `ebOver` (บรรทัด 1000) → ข้อความแดง "— ที่กรอกเกินเพดาน (ยอดสุทธิห้ามติดลบ)" + `.hard-warn` "**ส่วนลดท้ายบิลเกินยอดที่ลดได้**" (`DOC.lineSummaryWarn` บรรทัด 905) + **block submit** (`blockReason`/`submitGuard`)
- **VAT คิดใหม่ (ม.86/10)**: end-bill ลดฐานภาษีตามสัดส่วน — `ebVat = ebAmt*(vat/after)`, `ebBase = ebAmt−ebVat`, `netBefore = before−ebBase`, `netVat = vat−ebVat` (บรรทัด 1002–1005) → summary/PDF โชว์แถว "ส่วนลดท้ายบิล · ลดฐานภาษี", "ฐานภาษีหลังหักส่วนลด", "ภาษีซื้อ (VAT) · คิดจากฐานใหม่ (ม.86/10)" (บรรทัด 1041, 1060)

---

## §5 · Component Inventory (anchor + states)

### §5.1 · Buttons `.btn` (บรรทัด 264–295)
variants: `.btn-primary/-secondary/-ghost/-success/-danger/-link` · sizes `.sm`/`.lg` · states: hover (เฉพาะ `:not(:disabled)`), `:focus-visible` outline primary (280), `:disabled` opacity .6 + not-allowed (281). ปุ่ม/label ที่สกัดได้: ส่งออก CSV · สร้างใบลดหนี้ · ล้างตัวกรอง · ถัดไป · ย้อนกลับ · ยกเลิก · บันทึกแบบร่าง · บันทึกและส่งอนุมัติ · เลือกไฟล์ · แนบไฟล์เพิ่ม · ใช้ราคาระบบ · ทำสำเนา · พิมพ์ · ดาวน์โหลด · ปิด · แก้ไข · ส่งอนุมัติ · อนุมัติ · ไม่อนุมัติ · ส่งให้ผู้ขาย · ยืนยันยกเลิก · เปลี่ยน · บันทึก · บันทึก (จำลอง) · บันทึกใบลดหนี้ผู้ขาย · ใช้ใบนี้. (ปุ่ม "เพิ่มรายการ" มี template แต่ `DOC.lineAddAllowed → false` บรรทัด 898 → **ไม่แสดง**)

### §5.2 · Pills `.pill` (บรรทัด 300–314)
`draft` (slate) · `pending` (warning #8A5200) · `approved` (teal) · `sent` (purple) · `rejected` (danger) · `cancelled` (slate). map สถานะเอกสาร ↔ pill = `DOC.statusMap` (§8, บรรทัด 879), แสดงผ่าน `docPill()` (บรรทัด 1183).

### §5.3 · B2 v2 Line editor — `renderLineRow` (บรรทัด 1016–1036)
ตาราง `.line-tbl`: # · สินค้า (combobox item, §5.4) · จำนวน (`number`, `.qty-over` แดงเมื่อเกิน cap 679/1022) · หน่วย (select ถ้ามีหลาย unit และไม่ lock) · ราคา/หน่วย (`CFG.allowPriceOverride`, override → เส้นขอบ warning) · ส่วนลด % · ภาษี badge (`taxBadgeV` บรรทัด 1007 — ไม่คิด/NET/VAT) · จำนวนเงิน · expand(ขั้นสูง)/ลบ.
- **แถวจากใบเดิม lock**: `l.lock=true` → input สินค้า `readonly` (บรรทัด 1021), ไม่มีปุ่ม "เพิ่มรายการ" (`DOC.lineAddAllowed → false` บรรทัด 898)
- **line-cap display** (`DOC.lineMeta` บรรทัด 900): "ใบเดิม {qty} × ฿{price} · ลดแล้ว ฿{netDone} · ลดจำนวนได้อีก {capLeft} (ตามใบรับคืน) · ลดมูลค่าได้อีก ฿{netLeft}" + ข้อความ over "— เกินจำนวนที่ลดได้ / — ราคาลดเกินราคาเดิม / — เกินมูลค่าที่ลดได้" (`.line-meta.bad` 681)
- **expand panel** (บรรทัด 1030–1036): VAT segmented `ไม่คิด/บวกเพิ่ม/รวมแล้ว (NET)` + `%` + หมายเหตุ + "ระบบเสนอ ฿… (price_src)" + ปุ่ม `ใช้ราคาระบบ` (undo, เมื่อ override)
- states: default / focus (border primary + shadow 349–353) / over (`.qty-over`) / lock (readonly bg off-white) / expanded (bg primary-08)

### §5.4 · Combobox (2 ชนิด — portal)
- **สินค้า** (`.item-combo` + `#item-pop`): `onItemInput/Focus/Key` (บรรทัด 1050–1052) → `showItemSuggestions` สร้าง `.combo-pop` แนบ `document.body` position fixed คำนวณ up/down (บรรทัด 1053) · `paintItemPop` แสดง code·หมวด·ชื่อ·ราคา/หน่วย·สินค้า/บริการ (บรรทัด 1054) · เลือก `pickItem` (1055) · keyboard ↑↓/Enter/Esc (บรรทัด 1052) · click-outside close (listener หน่วง setTimeout 0)
- **คน (rep / slot อนุมัติ)** (`#combo-pop`): `combo()` (บรรทัด 1114) → `comboOpen` (บรรทัด 1117) portal fixed · `comboItems` (บรรทัด 1115): `rep`=พนักงาน (filter `DOC.repRoles` ถ้ามี) · `slot-N`=พนักงานตาม role ของขั้น (ตัด `ME.name` ออก) · `comboKey` ↑↓/Enter/Esc (บรรทัด 1119) · empty = "ไม่พบรายการ" (บรรทัด 1118)
- **`.suggest-list` / `.combo-option*`** (บรรทัด 370–382): legacy inline suggest (portal `--z-portal`, `.hidden` toggle) — **นิยามไว้แต่ JS ปัจจุบันใช้ `.combo-pop` แทน ไม่มีจุดเรียก** → §11 drift D-1

### §5.5 · Empty-state chip พนักงาน `.emp-chip.is-empty` (บรรทัด 625) → `empChip()` "ยังไม่ระบุคน" (บรรทัด 1182)

### §5.6 · Stat cards / Toggle / Stepper / Upload-zone / Notes / Slot-row — ตาม token §1
`.stat-card` (670–675) · `.hard-warn` (บรรทัด 634) = กล่องแดงเตือนแบบ block · `.note / .note.warn/.danger/.ok` (บรรทัด 635–636) · `.stepper-item.active/.done` (บรรทัด 461–474) · `.upload-zone.has-files` (บรรทัด 564) · `.slot-row.is-err` (DOA submit modal, บรรทัด 630–631)

### §5.7 · Timeline `.tl` (บรรทัด 641–644) — ใช้ทั้ง sign tab และ history tab (dot ok/warn/bad)

### §5.8 · Row kebab menu `.menu-fixed` (`openRowMenu` บรรทัด 1241–1245) — ดูรายละเอียด/แก้ไข(ร่าง)/ทำสำเนา/พิมพ์/ยกเลิก(ร่าง·pending จาก `DOC.rowCancel` 894) · z-index `var(--z-portal)` 70 (inline · ไม่มี CSS rule `.menu-fixed` — style ทั้งหมด inline) · click-outside close (setTimeout 0)

### §5.9 · DEMO-only elements (flag — prod inject `.demo-only{display:none}`, บรรทัด 676)
- **Persona switch** (`.demo-wrap.demo-only[data-demo="persona-switch"]` บรรทัด 734) → `switchPersona()` (บรรทัด 976) — สลับ 4 บทบาทรีวิวสิทธิ์
- **จำลองอนุมัติใบลดหนี้อื่น (กินเพดาน)** (`.demo-wrap.demo-only[data-demo="room-simulate"]` บรรทัด 944) → `demoPay()` (บรรทัด 948) — พิสูจน์ S-11 (`approveGuard` re-check `dnRoom` ตอนอนุมัติขั้นสุดท้าย) · **หน้าจริงไม่มีปุ่มนี้** (comment บรรทัด 947)
- ป้ายกำกับ demo-only ใน PDF tab ("template ตาม thai-doc-pdf-generator" 1162) + ref tab ("จำลอง · รอเชื่อม Journal Entry F093" 945)
> **dev: ห้าม render `.demo-only` ใน production build** — ไม่ใช่ฟีเจอร์จริง (PREFLIGHT: prod strips)

---

## §6 · Overlay Registry + Dismiss Rules

| Overlay (selector) | ชนิด | z-index | เปิดโดย | ปิดโดย | scroll-lock |
|---|---|--:|---|---|---|
| `.overlay-wrap` | ตัวห่อ drawer | `--z-drawer` 51 | `openCreateDrawer`/`openViewDrawer` (บรรทัด 1068/1123) | — (ห่อ backdrop+panel) | body ไม่ scroll เพราะ `.main{height:100vh;overflow:hidden}` (658) · **ไม่มี `:has()` rule** (ต่างจาก CN) |
| `.backdrop` | ฉากหลัง | `--z-backdrop` 50 | ภายใน overlay-wrap / modal | **คลิก backdrop** → `closeCreateDrawer`/`closeViewDrawer` (drawer, บรรทัด 1068/1123) หรือ `this.parentElement.remove()` (modal, บรรทัด 1188) | — |
| `.drawer-panel` | drawer ขวา | `--z-drawer` 51 | create(`.wide` 1290px 622) · view(920px 492) | ปุ่มปิด / backdrop / **Esc** | (ผ่าน .main overflow) |
| `.modal-overlay` | modal กลางจอ | `--z-modal` 60 | `modalShell()` (บรรทัด 1188) | backdrop / ปุ่มยกเลิก·ปิด / **Esc** · `closeModal()` (บรรทัด 1189) | — (ไม่มี overlay-wrap → ไม่ล็อก scroll เพิ่ม · §11) |
| `.combo-pop` | combobox portal | `--z-portal` 70 | `showItemSuggestions`/`comboOpen` แนบ body (1053/1117) | เลือก / click-outside / **Esc (ชั้นแรก)** | — |
| `.menu-fixed` (`#row-menu`) | row kebab | `--z-portal` 70 (inline) | `openRowMenu` (1241) | คลิกเมนู / click-outside | — |
| `.suggest-list` | legacy suggest | `--z-portal` 70 | (ไม่ถูกเรียกใน JS ปัจจุบัน) | `.hidden` | — |

**modal card เหนือ backdrop:** `.modal-overlay > *:not(.backdrop){position:relative; z-index:var(--z-modal)}` (บรรทัด 506) — fix v9.1 DSP-08 regression.

**Modals (สร้างผ่าน `modalShell`/`confirmModal`/`reasonModal`):** submit (`#submit-modal` DOA slot-picker · `openSubmitModal` 1192 / `renderSubmitModal` 1193) · approve (`openApproveModal` 1200) · reject (`openRejectModal` 1206, reasonModal) · cancel (`openCancelDN` 949, reasonModal) · send (`openSendDN` 951, confirmModal) · vendorCn (`openVendorCn` 946, confirmModal) · demoPay (948) · **เครดิตคงเหลือรายผู้ขาย** (`showVendorCreditDetail` 1237, modalShell — ปุ่มเดียว "ปิด" · **ไม่ใช่ confirmModal**) ⭐ · (row-menu = `.menu-fixed` ไม่ใช่ modal). ทุกตัวเป็น `.modal-overlay` เดี่ยว, ปิดด้วย `closeModal()` เคลียร์ทั้งหมด.

**Toast** `#toast-root` (บรรทัด 742, `showToast` บรรทัด 974): มุมขวาบน `--z-toast` 100 · auto-dismiss 3500ms fade 200ms · ชนิด success/error/warning/info (สี+ไอคอน) · ไม่มีปุ่มปิด.

---

## §7 · Interaction Spec

### §7.1 · Esc chain (global handler บรรทัด 1258) — ลำดับปิดทีละชั้น
`document.addEventListener('keydown', …)` ที่ **บรรทัด 1258**: ถ้า key ≠ Escape → return; มิฉะนั้นปิดตามลำดับ (ปิดชั้นบนสุดชั้นเดียวต่อการกด 1 ครั้ง):
1. มี `.combo-pop` → ลบ combo-pop ทั้งหมด แล้ว return (combobox ปิดก่อน)
2. มี `.modal-overlay` → `m.remove()` return (modal ปิดก่อน drawer)
3. มี `#create-drawer` → `closeCreateDrawer()`
4. มิฉะนั้น `#view-drawer` → `closeViewDrawer()`

Esc ระดับ combobox (กันไม่ให้ทะลุไปปิด drawer): `onItemKey` **บรรทัด 1052** และ `comboKey` **บรรทัด 1119** ดัก `e.key==='Escape'` → ลบ `.combo-pop` + `e.stopPropagation()` (ปิดเฉพาะ popup, ไม่ลามถึง global handler). สาม anchor ของ `'Escape'` = บรรทัด **1052 · 1119 · 1258**.

### §7.2 · Click-outside
combobox (item + คน): เพิ่ม `document.addEventListener('click', close)` แบบหน่วง `setTimeout(…,0)` กันจับ event เปิดตัวเอง (บรรทัด 1053, 1117) · row-menu (บรรทัด 1245) เช่นเดียวกัน · modal/drawer ปิดผ่าน backdrop คลิก.

### §7.3 · Focus / render preservation
- `updateLine` (บรรทัด 1044–1047) เก็บ `oninput` + `selectionStart` ของ input ที่ focus ก่อน re-render ทั้ง drawer แล้วคืน focus/caret (กัน caret เด้งตอนพิมพ์)
- `renderCreateDrawer`/`renderViewDrawer` เก็บ `scrollTop` ของ body แล้วคืนหลัง re-render (บรรทัด 1072/1083, 1129/1152)
- `addLine` (บรรทัด 1042) focus ช่องสินค้าแถวใหม่หลัง 30ms
- **ไม่มี** focus-trap / focus-restore หลังปิด overlay · ไม่มี `inert` (extractor: focus_trap ❌, focus_restore ❌) — R4: ไม่มี (—)

### §7.4 · Combobox positioning (บรรทัด 1053, 1117)
`getBoundingClientRect()` → position fixed; ถ้าพื้นที่ล่างเหลือ < 260px (item) / 280px (คน) → เปิดขึ้นบน (`bottom:…`) มิฉะนั้นเปิดลง (`top:…`). ป้องกัน popup ล้นจอ.

### §7.5 · Re-entrancy guard `busyGate()` (บรรทัด 963, FIX-08) — กัน double-submit ของ commit action (confirmSubmit/confirmApprove/reject/cancel/send/vendorCn); dev = idempotency key + version (FRD §2.3).

---

## §8 · State-Driven UI Matrix

`DOC.statusMap` (บรรทัด 879) · action buttons `DOC.viewActions(s, st)` (บรรทัด 925) · guards.

| status | pill (docPill) | ปุ่มใน view header (`viewActions`) | แก้ไข? | ยกเลิก? |
|---|---|---|---|---|
| `draft` | ฉบับร่าง (draft) | `ยกเลิก`(openCancelDN) · `แก้ไข`(→edit) · `ส่งอนุมัติ`(openSubmitModal) | ✅ | ✅ |
| `pending_approval` | รออนุมัติ (pending) | ผู้มีสิทธิ์ขั้นปัจจุบัน (`canActStep`): `ไม่อนุมัติ`·`อนุมัติ` · ผู้ส่ง (`submittedBy===ME`): `ยกเลิก` | ❌ | ✅ (owner/pending) |
| `approved` | อนุมัติแล้ว · รอส่ง (approved) | `ส่งให้ผู้ขาย`(openSendDN) | ❌ lock | ❌ |
| `sent` | ส่งผู้ขายแล้ว (sent) | — (`viewActions` คืน `''` · **ไม่มี resend**) | ❌ lock | ❌ |
| `cancelled` | ยกเลิก (cancelled) | — (ไม่มีปุ่ม) | ❌ | ❌ |

**Guards (ยึด HTML):**
- `openCreateDrawer` แก้ non-draft → toast `แก้ไขได้เฉพาะฉบับร่าง` + เด้งไป view (บรรทัด 1066)
- `submitGuard` (บรรทัด 915) / `openSubmitModal` (บรรทัด 1192) / `confirmSubmit` (บรรทัด 1199): non-draft → `ส่งอนุมัติได้เฉพาะฉบับร่าง` · ebOver → block · grand > `dnRoom` → block · reasonText<10 → block · slot ว่าง → `เลือกผู้อนุมัติให้ครบทุกขั้น`
- `confirmApprove`/`confirmSubmit` re-check `canActStep`: ไม่ใช่ผู้มีสิทธิ์ → `ไม่ใช่ผู้มีสิทธิ์ในขั้นปัจจุบัน` (บรรทัด 1203) · `approveGuard` ขั้นสุดท้าย re-check `dnRoom` (S-11, บรรทัด 918)
- `openCancelDN` (บรรทัด 949): status นอก draft/pending → `ยกเลิกได้เฉพาะฉบับร่าง / รออนุมัติ — ใบที่อนุมัติแล้วยกเลิกไม่ได้ (OQ-DN-04)`
- `openSendDN` (บรรทัด 951): ไม่ approved → `ต้องอนุมัติครบก่อนส่งให้ผู้ขาย`
- `openVendorCn` (บรรทัด 946): ไม่ approved/sent → `บันทึกใบลดหนี้ผู้ขายได้เฉพาะใบที่อนุมัติแล้ว` (บันทึกเลขที่+วันที่ → กลับภาษีซื้อ ม.82/10)

**เพดานลดหนี้ (FIX-01, BA 2026-09-23 · บรรทัด 831–834):** `dnRoom = grand − ลดหนี้แล้ว(approved/sent) − กันยอด(draft/pending)` **ไม่หัก `paid`** → ใบที่จ่ายครบแล้วยังออกใบลดหนี้ได้ (คืนของหลังจ่าย) · `dnSplit`: `applyToAp = min(ยอดลดหนี้, คงค้าง)` · `vendorCredit = ส่วนเกินคงค้าง` = **เครดิตคงเหลือกับผู้ขาย** (FN-20).

**DOA tier (มีวงเงิน) — `MOCK_DOA_ENTRY`/`resolveDoa` (บรรทัด 807–808):** ≤฿50,000 = 1 ขั้น (ผจก.จัดซื้อ) · ฿50,000.01–300,000 = 2 ขั้น (+ผจก.บัญชี) · >฿300,000 = 3 ขั้น (+CFO). tier คิดจาก `totals().grand` (หลัง end-bill). Sequential chain, เลือก "คน" ต่อขั้นใน submit modal (`.slot-row` บรรทัด 1196).

**Reason master `DN_REASONS` (บรรทัด 804):** RTV (คืนสินค้า อ้าง RTV, mode qty, `needRTV`) · OVERPRICE (ผู้ขายคิดราคาเกิน, mode price) · SHORT (ของขาด/ไม่ครบ, mode qty).

---

## §9 · Microcopy (verbatim)

### §9.1 · Toasts — `showToast(msg, type)` (สกัดครบทุก call · บรรทัด anchor)
| ข้อความ (คัดตรงตัว) | ชนิด | บรรทัด |
|---|---|---|
| ลดหนี้ไม่อ้างใบตั้งหนี้ถูกปิดไว้ (OQ-DN-01) | warning | 853 |
| บันทึกใบลดหนี้ผู้ขายได้เฉพาะใบที่อนุมัติแล้ว | warning | 946 |
| บันทึกได้เฉพาะใบที่อนุมัติแล้ว | warning | 946 |
| กรอกทั้งเลขที่และวันที่ใบลดหนี้ผู้ขาย | warning | 946 |
| บันทึกใบลดหนี้ผู้ขายแล้ว — ลดภาษีซื้อตามเดือนที่ได้รับ | success | 946 |
| ยกเลิกได้เฉพาะฉบับร่าง / รออนุมัติ — ใบที่อนุมัติแล้วยกเลิกไม่ได้ (OQ-DN-04) | warning | 949 |
| ยกเลิกได้เฉพาะฉบับร่าง / รออนุมัติ (OQ-DN-04) | warning | 949 |
| ยกเลิกเรียบร้อย | success | 949 |
| ต้องอนุมัติครบก่อนส่งให้ผู้ขาย | warning | 951 |
| ดาวน์โหลด PDF (mock) | info / success | 1142 / 1162 |
| แก้ไขได้เฉพาะฉบับร่าง | warning | 1066 |
| กรุณากรอกข้อมูลให้ครบถ้วน | warning | 1106 |
| กรุณาระบุเหตุผล | warning | 1190 |
| เลือกผู้อนุมัติให้ครบทุกขั้น | warning | 1199 |
| ส่งอนุมัติได้เฉพาะฉบับร่าง | warning | 1199 |
| ไม่ใช่ผู้มีสิทธิ์ในขั้นปัจจุบัน | warning | 1203 / 1206 |
| ตีกลับเพื่อแก้ไข | info | 1206 |

Toast ประกอบตัวแปร (verbatim template): `อนุมัติครบสาย — ออกใบลดหนี้ {code} · ลดยอดคงค้าง {inv}` (922) · `ส่ง {code} ให้ผู้ขายแล้ว` (951) · `สลับบทบาทเป็น {roleLabel} (DEMO)` (976) · `บันทึกแบบร่างใบลดหนี้เรียบร้อย` (1112) · `ส่งเพื่ออนุมัติแล้ว — My Approval ของ {ชื่อ}` (1199) · `อนุมัติขั้น {n} แล้ว — ส่งต่อ {ชื่อ}` (1204) · `ส่งออก CSV {n} รายการ` (1240) · `เพดานที่ลดได้ของ {inv} เหลือ ฿{x}` (948, DEMO).

Guard/validate ที่ส่งเป็น toast (return string จาก DOC/validateLines): `กรุณาเลือกใบตั้งหนี้ที่จะลดหนี้` (896) · `กรุณาเพิ่มรายการอย่างน้อย 1 รายการ (จำนวน > 0 · ราคา > 0)` · `มีแถวที่ยังไม่ได้เลือกสินค้า — เลือกหรือลบแถวก่อน` · `สินค้า+หน่วยซ้ำ: {name}` (1109) · `จำนวนลดเกินที่ลดได้: …` (overMsg 901) · `ราคาลดต่อหน่วยเกินราคาเดิม: {name}` · `มูลค่าลดเกินมูลค่าที่ลดได้ของบรรทัด: {name}` (902) · submitGuard: `ส่วนลดท้ายบิลเกินยอดที่ลดได้ (สูงสุด ฿…) — แก้ไขร่างก่อน` · `ยอดลดหนี้เกินมูลค่าที่ลดได้ของใบตั้งหนี้ (ลดได้ ฿…) — แก้ไขร่างก่อน` · `ระบุคำอธิบายเหตุผลก่อนส่งอนุมัติ` (915) · approveGuard(error): `อนุมัติไม่ได้ — มูลค่าที่ลดได้ของ {inv} เหลือ ฿… น้อยกว่ายอดลดหนี้ … ให้ไม่อนุมัติกลับไปแก้` (918).

### §9.2 · ปุ่มหลัก / label (verbatim)
สร้างใบลดหนี้ · บันทึกแบบร่าง · บันทึกและส่งอนุมัติ (`DOC.submitLabel` 877) · ส่งอนุมัติ · อนุมัติ · ไม่อนุมัติ · ยกเลิก · ส่งให้ผู้ขาย · บันทึกใบลดหนี้ผู้ขาย · เพิ่มรายการ · แนบไฟล์เพิ่ม · เลือกไฟล์ · ใช้ราคาระบบ · เปลี่ยน · ล้างตัวกรอง · ส่งออก CSV · ถัดไป · ย้อนกลับ · ยืนยันยกเลิก · ใช้ใบนี้ · ปิด.

### §9.3 · Placeholder / hint / empty / hard-warn / blockReason
- ค้นหาใบตั้งหนี้ (step 1): `พิมพ์เลขที่ใบตั้งหนี้ / ใบกำกับ / ผู้ขาย…` (บรรทัด 854)
- ค้นหาสินค้า: `ค้นหารหัสหรือชื่อสินค้า...` (บรรทัด 1021) · คน: `ค้นหาชื่อคนในตำแหน่ง … …` (1196)
- vendorCn placeholder: `เช่น TFS-6650` (บรรทัด 864) · reasonText placeholder: `เช่น คืนสินค้าชำรุด 2 กล่อง ตามใบคืนสินค้า RTV-…` (บรรทัด 867)
- field-error (step2): `ต้องไม่ก่อนวันที่ใบกำกับเดิม` (861) · `เลือกเหตุผล` (862) · `เลือกใบคืนสินค้าของใบตั้งหนี้นี้` (863) · `ระบุคำอธิบายอย่างน้อย 10 ตัวอักษร` (867)
- helper vendorCnDate: `ใช้กำหนดเดือนภาษีที่ลดภาษีซื้อใน ภ.พ.30` (865)
- empty list: `ไม่พบรายการที่ตรงกับเงื่อนไข` (1227) · empty src: `ไม่พบเอกสารที่ตรงเงื่อนไข` (1088) · combobox empty: `ไม่พบรายการ` (1118)
- lock footer: `อนุมัติแล้ว ล็อกแก้ไข` (`DOC.lockedLabel` 878)
- hard-warn: `ส่วนลดท้ายบิลเกินยอดที่ลดได้` (905) · `ยอดลดหนี้เกินมูลค่าที่ลดได้ของใบตั้งหนี้อ้างอิง` (905) · `ยอดลดหนี้เกินยอดคงเหลือของใบตั้งหนี้อ้างอิง` (detail tab, 927)
- blockReason (title ปุ่ม disabled): `ส่วนลดท้ายบิลเกินยอดที่ลดได้ (สูงสุด ฿…)` · `ยอดลดหนี้เกินมูลค่าที่ลดได้ (บันทึกร่างได้)` · `ระบุคำอธิบายเหตุผลอย่างน้อย 10 ตัวอักษร` · `เหตุผลคืนสินค้าต้องอ้างใบคืนสินค้า` (907)
- ref tab 2-state: `รอใบลดหนี้ผู้ขาย` (ยังไม่มี vendorCn) vs `เดือนภาษีที่ลด MM/YYYY` (มี vendorCn+วันที่) (943)
- summary line labels: `หักจากหนี้ค้าง {inv}` · `เครดิตคงเหลือกับผู้ขาย` · `ภาษีซื้อที่ลด (เมื่อได้รับใบลดหนี้ผู้ขาย)` (906) · cap wording = **"มูลค่าที่ลดได้"** (ไม่ใช่ "ยอดคงเหลือ")

---

## §10 · Data Binding & BACKEND anchors

**ไม่มี `// BACKEND:` literal** — ไฟล์นี้ใช้ mock in-file + คอมเมนต์ผูก engine กลาง (สกัดตรง ๆ):
- **เลขเอกสาร**: `nextCode()` (บรรทัด 990) mock max-based; คอมเมนต์ "เลขจริงจาก **ENG-DOC-NUM.next()** ตาม doc_type DN ใน DOCCFG_BRIEF_F097 (F003) — ห้าม feature รันเลขเอง" → FRD API-06 (issue) / DOCCFG declaration
- **สำเนา PDF**: ENG-DOC-STORE (คอมเมนต์ 989 · pdf tab 1162) → FRD API-13
- **DOA resolve**: `resolveDoa`/`MOCK_DOA_ENTRY` mock (บรรทัด 807–808); จริง = **ENG-DOA** freeze ตอน submit → FRD API-05
- **CSQ**: `pushAudit(s,'…บันทึกเข้า 7C ตาม CSQ_BRIEF_F097 (จำลอง)')` (บรรทัด 922); event `dn.issued → AC` (ลด AP) · `dn.vat_applied` (เมื่อมี vendorCn) → AC ภาษีซื้อ (คอมเมนต์ 921, รอเคาะ OQ-DN-07) → CSQ_BRIEF_F097
- **NTF**: คอมเมนต์ `dn.issued → ผู้สร้าง + ทีม AP` (บรรทัด 920), `dn.sent → ผู้ขาย` (บรรทัด 950); doa_pending/doa_result มาจาก DOA engine ห้ามซ้ำ → NTF_BRIEF_F097
- **ap_open_item (F095/APINV)**: `INVOICES` mock (บรรทัด 788–794) contract `ap_open_item`; `invGrand/dnApplied/dnHeld/invOutstanding/invAvailable/dnRoom` (บรรทัด 826–832) → FRD API-11 / cross-module write `dn_applied += applyToAp`
- **RTV / คืนสินค้า (F080, W3-LITE)**: `RTVS` mock [ASSUMED] (บรรทัด 797–801) → FRD API-12
- **input_vat_line (ภ.พ.30, ม.82/10)**: `openVendorCn` (946) บันทึก vendorCn+วันที่ → กลับภาษีซื้อเดือนที่ได้รับ → FRD API-16 ⭐
- **vendor credit ledger (FN-20)**: `vendorCreditRows` (837) display-only → FRD API-17 ⭐ (flow ใช้เครดิต รอเคาะ OQ-DN-06)
- **Journal Entry (F093)**: JE mock ใน ref tab (บรรทัด 940) demo-only → cross-module event
- **Idempotency/version**: HTML `busyGate` (บรรทัด 963); dev = Idempotency-Key + If-Match (FRD §2.3)

Master mock: `PERSONAS`(754) `EMPLOYEES`(761) `PRODUCTS`(771) `PARTNERS`(780) `PAYMENT_TERMS`(778) `TAX_CODES`(779) `DN_REASONS`(804) `RTVS`(797) `CFG`(753, vatPct 7) · `TODAY_ISO='2026-09-20'` (752).

---

## §11 · Traceability + Drift Log

### §11.1 · Brief ↔ FRD ↔ HTML
| Brief § | FRD (01_UI P-xx / 02_API) | HTML anchor |
|---|---|---|
| §2 route list | P-01 · API-01/10 | `renderListPage` (1213) · `getRoute` (1250) |
| §4.1 vendor-credit KPI card | P-01 · API-17 · FN-20 | `listStats` credit (885) · `showVendorCreditDetail` (1237) · `vendorCreditRows` (837) |
| §4.2 create s1 (invoice picker) | P-02 · API-11 | `renderStep1` (851) · `invList` (844) |
| §4.2 create s2 (reason/RTV/vendorCn) | P-02 · API-12/15 | `renderStep2` (855) · `DN_REASONS` (804) |
| §4.2 create s3 lines | P-02 · API-03 | `renderStep3`/`renderLineRow` (1009/1016) |
| §4.4 end-bill (FN-19) | 05_RULES ม.86/10 · API-05 (tier=grand) | `totals` (996) · `renderStep3` (1013) |
| §4.3 view/edit | P-03/P-04 · API-02/04 | `renderViewDrawer` (1127) · `openCreateDrawer` (1065) |
| §4.3 ref tab · ภาษีซื้อ ม.82/10 | P-04 · API-16 · FN-21 · BR-14 | `renderRefTab` (940) · `openVendorCn` (946) |
| §8 submit + DOA | API-05 · ENG-DOA | `openSubmitModal`/`confirmSubmit` (1192/1199) |
| §8 approve/reject | API-06/07 | `confirmApprove`/`openRejectModal` (1203/1206) |
| §8 cancel | API-08 | `openCancelDN` (949) |
| §8 send | API-09 | `openSendDN` (951) |
| §4.3 PDF tab | API-13 · DN_print-spec | `renderPdfTab` (1162) |
| §10 issue/ap_open_item | API-06 side-effect · cross-module F095/F093 | `onFinalApprove` (919) · `renderRefTab` (940) |

ครบ 4 route + 15/17 API มี anchor. FN-19 (end-bill) + FN-20 (vendor credit) + FN-21 (vendorCn VAT) จับคู่ครบ.

### §11.2 · ⚠️ Drift Log
| # | ประเภท | รายละเอียด | ข้อเสนอ |
|---|---|---|---|
| D-1 | HTML-only (dead CSS) | `.suggest-list` (370–376) + `.combo-option*` (377–382) นิยามไว้แต่ JS ใช้ `.combo-pop` (637) แทน — ไม่มีจุดเรียก | ไม่กระทบ dev; ตัดออกรอบ cleanup (ยืนยัน grep ก่อน) |
| D-2 | engine-carry | `totals()` อ้าง `so.couponAmt` (บรรทัด 996/999) แต่ feature DN ไม่มี UI คูปอง (=0 เสมอ) — ตกทอดจาก B2 v2 SO engine | ไม่กระทบ; ห้ามแก้ engine (kernel locked) |
| D-3 | FRD-only (endpoint) | FRD **API-14** revise-doc ("ออกเอกสารแก้ไข") มีใน 02_API + cross-ref P-04 แต่ **HTML ไม่มี** function/ปุ่ม (grep `revise`/`ออกเอกสารแก้ไข` = 0) — `viewActions` approved คืนแค่ "ส่งให้ผู้ขาย" | dev เคาะ: DN รอบนี้ตัด revise-doc ออกจริง (ต่าง CN) หรือ FRD ต้องอัปเดตให้ตรง HTML |
| D-4 | FRD-only (behavior) | API-09 summary เขียน "send · **resend**" แต่ HTML `viewActions` สถานะ `sent` คืน `''` — **ไม่มีปุ่มส่งสำเนาซ้ำ** (ต่าง CN ที่มี resend) | dev เคาะ: resend อยู่นอก scope รอบนี้ หรือเพิ่มปุ่มให้ตรง API-09 |
| D-5 | HTML behavior (scroll-lock) | `.modal-overlay` ไม่ห่อ `.overlay-wrap` และไม่มี `body:has()` rule (ต่าง CN) — body ไม่ scroll เพราะ `.main{height:100vh;overflow:hidden}` (658) แทน | ปกติสำหรับ layout นี้; ตรวจว่า modal ยาวเกินจอ scroll ได้ (modal-overlay ไม่มี overflow) |
| D-6 | FRD-only (config) | API-15 (GET dn-reasons config) — HTML ใช้ `DN_REASONS` inline mock (804) | ปกติ (config master, dev wire endpoint) |
| D-7 | declare | FRD INDEX Declarations = `doa+ntf+csq+doccfg+pdfdoc` — HTML เห็นเป็นคอมเมนต์ผูก engine เท่านั้น | ปกติ (declaration = ประกาศ, dev wire ภายนอก) |

> ไม่มี drift ระดับ business ที่บล็อก · **D-3/D-4 ให้ dev/BA เคาะ** (FRD ระบุ revise-doc/resend แต่ HTML ไม่ทำ — ตัดสินใจว่าใครถูก) · ที่เหลือ informational.

---

## §12 · Diff จากเวอร์ชันก่อน
— ไม่มี HTML เก่าให้ diff ในรอบนี้ · (สำหรับ reviewer: delta เทียบพี่น้อง F-ACC-CN อยู่ใน §0 + FRD INDEX §Mirror Delta — DN เพิ่ม FN-20/21, `dnRoom` ไม่หัก paid, ตัด revise-doc/resend, reason RTV/OVERPRICE/SHORT, z-toast 100)

---

## §13 · 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
1. **D-3/D-4**: sync FRD ↔ HTML เรื่อง revise-doc (API-14) และ resend (API-09) — ถ้ารอบนี้ตั้งใจตัดออก ให้ปรับ 02_API/01_UI ให้ตรง; ถ้าต้องมี ให้เพิ่ม `openReviseDocDN`/resend ใน `viewActions` (mirror CN).
2. **D-1**: ตัด `.suggest-list`/`.combo-option*` ที่ไม่ถูกเรียก เพื่อลดขนาดไฟล์ (ยืนยัน grep ก่อนตัด — เป็น dead CSS จริง).
3. เพิ่มนิยาม CSS `.menu-fixed` (ปัจจุบัน style inline ล้วน) หรือคง inline ก็ได้ — เพื่อความสม่ำเสมอกับ registry.
4. เพิ่ม focus-trap + focus-restore + `inert` ให้ drawer/modal (ปัจจุบันไม่มี) เพื่อ a11y (นอกขอบเขต AS-BUILT).
> ทั้งหมดนี้เป็นข้อเสนอ — ห้ามถือเป็นสเปคที่ต้องสร้าง จนกว่าจะเคาะ.
