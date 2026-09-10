# UI Brief — F-HR-EXPENSE · เบิกค่าใช้จ่าย (Expense Claim)

> **AS-BUILT UI spec** สกัดจาก HTML prototype แบบ 1:1 (Extraction-based · Iron Rule R1)
> ทุกบรรทัด trace กลับ selector / function / ข้อความจริงใน `expense.html` ได้
> ใช้คู่กับ **HTML (source of truth) + FRD Pack (สเปคระบบ)** — บรีฟนี้ = design intent handoff

---

## §0 · Document Control + Pairing

| หัวข้อ | ค่า |
|---|---|
| Feature | F-HR-EXPENSE · เบิกค่าใช้จ่าย (Expense Claim · F101) |
| HTML source | `outputs/F-HR-EXPENSE/expense.html` (2513 บรรทัด · `<title>เบิกค่าใช้จ่าย (Expense Claim) · CUBE NATIVE`) |
| Archetype | **Pattern Q — Transaction Document** (list + wizard 5 ขั้น + view 4 tabs + PDF a4 + ลายเซ็น/ประวัติ) |
| BASE-KIT | v6.4 (CUBE Warm Light · Iron Rule #104 "1 feature = 1 เมนู" · DSP-01/02 pre-wire) |
| Shell | 1 module "ทรัพยากรบุคคล" → feature "เบิกค่าใช้จ่าย" · **หน้าเดียว** (list view เดียว · overlay = wizard/view/modal ไม่มี route แยก) |
| จอทั้งหมด | 8 จอ (1 list + 1 wizard drawer 5 ขั้น + 1 view drawer 4 tab + 4 modal type + 1 PDF a4) |
| FRD Pair | `FRD_F-HR-EXPENSE_Pack/` (01_UI P-01..P-07 · 02_API API-01..20 · 05_RULES BR-01..18 / LOCK-01..10) — **paired ✅** |
| Drift status | ไม่มี business-blocking drift · HTML-only = prototype scaffolding (Iron Rule #105) — ดู §11 Drift Log |
| ไลบรารี | Lucide (multi-CDN fallback: unpkg → jsdelivr → cdnjs · pinned · loader ท้าย body + 5000ms safety net) · ฟอนต์ Satoshi (fontshare) + Noto Sans Thai (googleapis) |
| ⚠️ CDN dependency | ฟอนต์ 2 แหล่ง + Lucide 3 CDN — **offline จะ fallback ฟอนต์/ไม่มี icon** (UI ยังใช้งานได้ · `renderIcons()` no-op guard + 5s timeout) |
| ⭐ Touchpoint (PM/BA 2026-09-10) | (1) 4 ช่องทางจ่าย (+PV +เงินสดย่อย F091) · (2) hookbox เคลียร์เงินทดรอง F103 (display-only) ใน view-detail + wizard review · (3) demo-strip role ที่ 3 "เจ้าหน้าที่ (HR/Finance)" + scope filtering — ดู §4/§8/§10 |

---

## §1 · Design Tokens AS-BUILT

**Selector anchor:** `<style>` `:root` (บรรทัด 24-57 · BASE-KIT v6.4 — DO NOT EDIT Rule #69) + page-late `:root` (บรรทัด 1386 · z-index override)

### สี (CUBE CI · Warm Light — ห้าม hardcode hex ในระบบจริง ใช้ var)
| token | ค่า | ใช้ |
|---|---|---|
| `--c-primary` | `#FF3B30` | ปุ่มหลัก · active · error accent |
| `--c-primary-hover` | `#E62E24` | hover ปุ่มหลัก |
| `--c-teal` | `#FF9A1F` | accent รอง (gradient logo/avatar) |
| `--c-ink` / `--c-navy` | `#111111` | ตัวอักษรหลัก · sidebar bg · toast bg |
| `--c-mute` / `--c-mute-2` / `--c-mute-3` | `#54565C` / `#73757B` / `#9A9CA2` | ตัวอักษรรอง 3 ระดับ |
| `--c-line` / `--c-line-2` / `--c-line-3` | `#DEDAD4` / `#E9E5E0` / `#F1EEEA` | เส้นขอบ 3 ระดับ |
| `--c-bg-off` | `#FAF8F5` | พื้นหลังหน้า · thead |
| `--c-success` / `--c-warning` / `--c-danger` | `#1F9D55` / `#E8870F` / `#E62E24` | pill/toast/note สถานะ |

### Type scale (Iron Rule locked · บรรทัด 44-52)
`--fs-h1:22px` · `--fs-h2:17px` · `--fs-h3:15px` · `--fs-body:14px` · `--fs-sub:13px` · `--fs-meta:12px` · `--fs-cap:11px` · `--fs-kpi:28px`
Font stack: `'Satoshi','Noto Sans Thai',system-ui,sans-serif` · หัวข้อ/ตัวเลขใหญ่ = `'Noto Sans Thai'`

### Spacing / Radius (บรรทัด 53-56)
`--sp-xs:4px … --sp-xl:28px` · `--r-xs:4px … --r-lg:12px · --r-full:999px`

### Layout tokens
`--sidebar-w:232px` · `--shell-h:52px` · scrollbar 5px (Iron Rule #49) · `scrollbar-gutter:stable` (Rule #35 กัน jank) · `body{min-width:768px}` (Rule #97 desktop-base)

### ⭐ Z-INDEX MAP (สูง → ต่ำ · page-late `:root` บรรทัด 1386 · Rule: ขาด var = computed auto = overlay ซ้อนพัง)
| token | ค่า | ใช้กับ |
|---|---|---|
| `--z-toast` | **80** | toast (สูงสุด — เห็นเหนือทุกอย่าง) |
| `--z-tooltip` | **65** | `.tip`/`.tip-pop` tooltip |
| `--z-portal` | **60** | `.menu-fixed` portal → `#overlay-root` (Rule #95) · **`.modal-backdrop` ก็ = 60** (DSP-01) |
| `--z-drawer` | **55** | ตัว drawer `.drawer` |
| `--z-backdrop` | **50** | ฉากหลัง drawer `.drawer-backdrop` + `.ss-list` (search-select list) |
| `--z-dropdown` | **40** | user menu · `.menu-fixed` default |
| `--z-shell` | **19** | sidebar |
| `--z-sticky` | **5** | shell-bar · thead sticky |

> **⭐ สำคัญ (DSP-01 · บรรทัด 1428):** `.modal-backdrop` ตั้ง z = `--z-portal` (**60**) **สูงกว่า** drawer (55) โดยตั้งใจ — modal "ส่งอนุมัติ" ที่เปิด**จากในลิ้นชัก** (view drawer draft) ต้องลอยเหนือลิ้นชัก · combobox slot-picker ที่ portal ออก (z-portal 60) จึงยังโผล่เหนือ modal ได้ · **ห้ามลดต่ำกว่า drawer** ไม่งั้น modal จมใต้ลิ้นชัก

---

## §2 · Route Map

**Anchor:** `getRoute()` (บรรทัด 1625 · BASE-KIT) · `navigate()` (1630) · feature `render()` (**บรรทัด 2500 · override**) · `window.hashchange` (2032)

| route | จอ | default | refresh-safe |
|---|---|---|---|
| (ไม่มี hash route) | list view เดียว (`pageHTML()` L2247 → `listView()` L2261) | ✅ | ✅ |

- **ไม่มี hash routing ในระดับ feature** — feature `render()` (L2500) เขียน `#page-content` เป็น `pageHTML()` เสมอ ไม่อ่าน `getRoute()`. FRD อ้าง `#/expense` เป็น **route เชิงแนวคิด** (P-01 default) แต่ HTML ไม่ผูก hash จริง
- **`hashchange` → `render()`** (L2032 · late-binding) — เป็น full re-render ไม่เปลี่ยนจอ (no-op ต่อเนื้อหา)
- **Overlays ไม่มี route** — wizard/view drawer + modal เปิดผ่าน state (`state.drawer` / `state.modal` + `state.view.tab` + `state.wizard.step`) ไม่ผูก hash · refresh แล้ว overlay หาย (ตั้งใจ · ตรง FRD "tabs = drawer-tabs ไม่ใช่ route")

---

## §3 · Layout Shell

**Anchor:** `<aside class="sidebar">` (บรรทัด 1485) · `<header class="shell-bar">` (1514) · `<main class="main">` (1513)

| region | selector | ขนาด/พฤติกรรม |
|---|---|---|
| Sidebar | `.sidebar` (fixed · z=`--z-shell` 19) | width `--sidebar-w` 232px · bg `#111111` · 2 module "ทรัพยากรบุคคล" + "ระบบ" collapsible (`toggleModule()` L1615 · Rule #27 header ไม่ navigable) |
| Feature item | `.sb-item[data-feature="expense"]` | active = `.is-active` (แถบ ::before ซ้าย) · sibling `payroll`/`welfare`/`leave`/`hrconfig` = `<a>` ไม่มี onclick (placeholder · นอก scope) |
| Shell bar | `.shell-bar` (sticky top · z=`--z-sticky` 5) | height `--shell-h` 52px · breadcrumb `ทรัพยากรบุคคล › เบิกค่าใช้จ่าย` · bell (`toggleNotif()` no-op L2189) · user-chip |
| Main | `.main` | `margin-left:232px` · `<1180px` → sidebar off-canvas (`.nav-toggle` โผล่ · Rule #97) |
| Content host | `#page-content` | render โดย `render()` L2500 → `pageHTML()` · list ใช้ `.table-wrap` (scroll) |
| Demo strip | `.demo-strip` (`pageHTML()` L2248 · อยู่บนสุดของ content · bg warm `#FFF7EC`) | persona switch 3 บทบาท (prototype · Iron Rule #105 — **ไม่ใช่ส่วนของ feature จริง** · จริงมาจากล็อกอิน) |

---

## §4 · Page Anatomy (ต่อจอ)

โครงหน้า: `render()` (L2500) → `applyRole()` (เขียนชื่อ/บทบาท user-chip) → `pageHTML()` (L2247) = demo-strip + `.ph` (title + actions) + `#view` (`listView()`) + `unsupportedNote()`

**Page action (`.ph-actions` · L2253):**
- `ส่งออก` (secondary · ไม่มี handler — placeholder)
- `สร้างใบเบิก` (primary · `openCreate()` L2287 → เปิด wizard drawer)

### P-01 · รายการใบเบิก (`listView()` บรรทัด 2261)
- **Filter bar** (`.filter-bar` L2268): search (เลขที่/ชื่อผู้เบิก · `state.filters.search` → `refreshView()`) · select สถานะ (ทุกสถานะ/ฉบับร่าง/รออนุมัติ/อนุมัติแล้ว/จ่ายแล้ว/ตีกลับ) · ปุ่ม `ล้างตัวกรอง` (`clearFilters()` L2279)
- **Table 6 คอลัมน์:** เลขที่/สถานะ (`d.code` + chip "เกินเพดาน" ถ้า `overCap`) · ผู้เบิก (`personCell` avatar+ตำแหน่ง) · วันที่ · ยอดรวม (`col-num` · `maskM()`) · ลายเซ็น (`renderSignProgress` L2185 = `done/total` + bar) · สถานะ (`docPill`)
- แถว `onclick` → `openView(id)` (P-03)
- **⭐ Scope filtering (touchpoint 3 · `visibleDocs()` L2173):** role `scope:'self'` (ผู้เบิก/ธุรการ) เห็นเฉพาะใบของตน (`d.emp===r.self` · demo self=E01) · role `scope:'all'` (ผู้อนุมัติ/เจ้าหน้าที่) เห็นทุกใบ
- Empty: `emptyStateHTML` title `ยังไม่มีใบเบิก` desc `สร้างใบเบิกใหม่ ระบบจะตรวจเพดานหมวดและ resolve สายอนุมัติตามวงเงินให้` + ปุ่ม `สร้างใบเบิก`
- ท้ายหน้า: `unsupportedNote()` (L2258) = กล่อง "ไม่รองรับรอบนี้" 7 chip (FN-40 negatives · ของที่ห้ามมีปุ่ม)

### P-02 · สร้างใบเบิก — Wizard 5 ขั้น (`dwWizard()` บรรทัด 2343 · wide drawer)
`STEP_KEYS` (L2285): `เลือกแหล่งที่มา · ข้อมูลหลัก · รายการค่าใช้จ่าย · เอกสารแนบ · ตรวจสอบและยืนยัน` · `stepper()` L2289 · body = `wizStepBody()` L2290
1. **เลือกแหล่งที่มา** — radio "สร้างใหม่ (สำรองจ่ายเอง)" (checked) · "จากใบขออนุมัติเดินทาง" (disabled · ไม่รองรับรอบนี้)
2. **ข้อมูลหลัก** — search-select `wizemp` (ผู้เบิก* · `initSearchSelect` L2487) → hookbox ตำแหน่ง/แผนก/ศูนย์ต้นทุน (ดึงจากตำแหน่ง ณ วันเบิก · Movement) · วันที่เอกสาร (พ.ศ.) · **⭐ ช่องทางจ่าย** `<select>` 4 ตัวเลือก (touchpoint 1 · `PAY_OPTS` L2165)
3. **รายการค่าใช้จ่าย** — `lineEditor()` L2312 (B2 v2 grid): วันที่ · หมวด (`EXP.cats`) · รายละเอียด · จำนวนเงิน · VAT segmented (`vatSeg` — ไม่คิด/VAT/รวมแล้ว NET) · รวม · ลบ · ปุ่ม เพิ่มรายการ · `.totbox` (รวมเป็นเงิน/ภาษีมูลค่าเพิ่ม/รวมทั้งสิ้น) · **over-cap → panel เตือน + input เหตุผลบังคับ** (`overCapLines` L2216 · FN-04)
4. **เอกสารแนบ** — hookbox หมวดบังคับแนบใบเสร็จ (`receiptRequiredCats` L2219 · FN-12) · `.upload-zone` (PDF/JPG/PNG · OCR ไม่รองรับ)
5. **ตรวจสอบและยืนยัน** — kv สรุป · เตือน over-cap เหตุผลครบ/ไม่ครบ · **`budgetHookHTML`** (งบ F117 + สิทธิ์สวัสดิการ F102 · display-only L2237) · **⭐ `advanceHookHTML`** (เคลียร์เงินทดรอง F103 · touchpoint 2 · L2232) · สายอนุมัติ DOA resolve ตามวงเงิน
- **Step-advance gate** (`wizNext()` L2338 · FN-92): ขั้น 2 ต้องเลือกผู้เบิก · ขั้น 3 ต้องมี ≥1 รายการ + `grand>0`
- **Footer** (L2350): ย้อนกลับ/ยกเลิก · `ถัดไป` (disabled จน `canNext`) · ขั้น 5 → `บันทึกและส่งอนุมัติ` (disabled + `title` เตือน · `openSubmit()` → P-04)

### P-03 · รายละเอียดใบเบิก — View drawer 4 tabs (`dwView()` บรรทัด 2367)
Tabs (`setVtab()` L2361 · **ไม่ใช่ route**): `รายละเอียด › PDF Preview › ลายเซ็น / อนุมัติ › ประวัติ` (L2369)
- **รายละเอียด (detail):** kv (เลขที่/ผู้เบิก/ศูนย์ต้นทุน ณ วันเบิก/วันที่/ช่องทางจ่าย/สถานะ+เหตุผล) · ตารางรายการ (VAT badge `taxBadgeV` + รวม · `maskM`) · totbox · **เอกสารแนบ** section (`receipt_*.pdf · 3 ไฟล์ · 620 KB`) · **สถานะการจ่าย** hookbox (`d.payHook` + "อ่านจากปลายทาง … display-only — Expense ไม่จ่าย/ไม่ลงบัญชีเอง" · `payDownstream` L2167) · **`budgetHookHTML`** (F117/F102) · **⭐ `advanceHookHTML`** (F103 เคลียร์เงินทดรอง · touchpoint 2 · L2379)
- **PDF Preview (pdf):** `a4Doc(d)` L2399 (→ P-07)
- **ลายเซ็น / อนุมัติ (sign):** สายอนุมัติ DOA (`resolveDoa` + ช่วงวงเงิน) · timeline `.tl` ต่อขั้น (อนุมัติแล้ว/ไม่อนุมัติ/รอพิจารณา) · note ช่วงวงเงิน = ตัวอย่าง (mock)
- **ประวัติ (history):** `EXP.audit[d.id]` timeline (append-only)
- **Header actions** (L2397): ทำสำเนา (toast mock) · พิมพ์/PDF (`setVtab('pdf')`) · ดาวน์โหลด PDF (toast mock) · ปิด
- **Footer state-driven** (L2390-2396): ดู §8 State Matrix

### P-04 · ส่งอนุมัติ — DOA slot picker (`modalHTML() type==='submit'` บรรทัด 2411)
- resolve สายตามวงเงิน (`resolveDoa` L2213) → 1-3 slot ต่อขั้น · แต่ละ slot = `searchSelectHTML('slot-i')` (เลือกผู้อนุมัติจริงจาก `APPROVERS` L2204 · **ไม่ prefill** L2493)
- note: ช่วงวงเงินเป็น **ตัวอย่าง/mock** — ตั้งค่าจริงที่ DOA กลาง · ไม่ hardcode สาย
- ปุ่ม `ส่งอนุมัติ` (`submitConfirmBtn`) **disabled** จนเลือกครบทุก slot (`submitReady()` L2472 · `onSlotPickChange` L2473) → `doSubmit()` L2428
- เปิดได้ 2 ทาง: wizard ขั้น 5 (`openSubmit` L2409) · ใบร่างในลิ้นชัก (`openSubmitDraft` L2421 · มี `docId`)

### P-05 · ไม่อนุมัติ / ตีกลับ (`modalHTML() type==='reject'` บรรทัด 2416)
- textarea เหตุผล (`m_reason`) · ปุ่ม `ยืนยันตีกลับ` (`rejectConfirmBtn`) **disabled** จนกรอก (`onRejectReasonInput` L2470) → `doReject()` L2474 (role guard `canApprove`)

### P-06 · ยกเลิกใบเบิก (`modalHTML() type==='cancel'` บรรทัด 2417)
- `modShell` confirm (soft archive) → `doCancel()` L2480 (guard: เฉพาะ draft)

### P-04b · อนุมัติ (`modalHTML() type==='approve'` บรรทัด 2415)
- `modShell` confirm "อนุมัติแล้วระบบจะออกเลข EXP-YYYY-NNNN + PDF + บันทึกเข้า 7C ตาม CSQ_BRIEF_F101 + ส่งสถานะจ่าย" → `doApprove()` L2440 (chain advance ทีละขั้น · ครบ → เลข+PDF+7C)

### P-07 · PDF Preview a4 (`a4Doc()` บรรทัด 2399 · Pattern K print)
- หัวบริษัท + เลขที่/วันที่ · ผู้เบิก/ศูนย์ต้นทุน/ช่องทางจ่าย · ตารางรายการ · a4-tot (รวมเป็นเงิน/VAT/รวมทั้งสิ้น) · ช่องลายเซ็น 3 ช่อง (ผู้เบิก/ผู้อนุมัติ DOA/การเงิน)

---

## §5 · Component Inventory (anchor + states)

| component | selector / fn | states (R4) |
|---|---|---|
| Table row | `.tbl tbody tr` (`onclick=openView`) | default · hover (`bg-off`) · ไม่มี selected/checkbox (single-list) |
| Filter search | `.filter-bar input` (`oninput` → `refreshView()`) | default · focus (primary ring) — ไม่มี debounce (client filter) |
| Status select | `.input.w160` (`onchange`) | default · focus · **ไม่มี** loading/error (client mock) |
| Doc pill | `docPill(st)` (`DST` L2182) | 7 สถานะ → `.pill-muted/warning/success/info/converted/danger` (ดู §8) |
| Over-cap chip | `.chip-tag` (warning) | แสดงเมื่อ `overCap(d)` — บรรทัดใดมี `unit_price > cap` |
| Sign progress | `renderSignProgress(d)` (`.signprog`) | `done/total` + `.bar` fill (% อนุมัติแล้ว) |
| Person cell | `personCell(e)` (`.tbl-person`) | avatar (อักษรแรก) + ชื่อ + ตำแหน่ง · แผนก |
| VAT segmented | `vatSeg(i,l)` (`.seg-vat`) | 3 ปุ่ม ไม่คิด/VAT/รวมแล้ว NET · active = `.on` (`l.vat_mode`) |
| VAT badge (view) | `taxBadgeV(l)` (`.chip-tag`) | none="ไม่คิด" · included="NET 7%" (primary) · add="VAT 7%" (warning) |
| Line editor row | `lineEditor()` L2312 (`.line-tbl`) | default · over-cap → expand panel เตือน + input เหตุผล (`.ocap-reason` · `.is-warn-border` จนกรอก) |
| Search-select | `searchSelectHTML(key)` + `initSearchSelect()` (Iron Rule #34) | closed · open (`.ss-list`) · typing (highlight `<mark>`) · empty (`.ss-empty` "ไม่พบรายการ") · selected (ปุ่ม X `.ss-clear` โผล่ · caret ซ่อน) · keyboard (↑↓ Enter Esc · L2891) · เด้งขึ้น (`.ss-up` เมื่อพื้นที่ล่างไม่พอ) |
| Stepper | `stepper()` L2289 (`.step-dot`) | `.done` (✓) · `.on` (ปัจจุบัน) · ว่าง (ยังไม่ถึง) |
| Demo persona seg | `.seg-control` + `.seg-item` (`setRole()` L2188) | active = `.is-active` (3 บทบาท) |
| Busy button | `state._busy` → ทุก mutation กัน double-submit (FN-92) | idle · busy (500ms guard) |
| Empty state | `emptyStateHTML()` (Iron Rule #39) | icon + title + desc + action button |

---

## §6 · Overlay Registry

**Anchor:** container HTML บรรทัด 1535-1548 · toggle fn บรรทัด 1637-1691 · `modalHTML()` 2410 · `portalMenu()` 2072

| overlay | selector | ขนาด | เปิด | ปิด (dismiss) | z-index |
|---|---|---|---|---|---|
| **Sidebar** | `.sidebar` | 232px (fixed) | เสมอ (off-canvas <1180px) | — (nav-toggle บนจอเล็ก) | `--z-shell` 19 |
| **User menu** | `.user-menu` | 240px | `toggleUserMenu()` L2190 (คลิก user-chip) | click-outside (L2191) | `--z-dropdown` 40 |
| **Drawer** | `.drawer` + `.drawer-backdrop` | wizard 1290px (wide) · view standard · max 100vw | `openDrawer()` L1637 — slide `transform 280ms` | Esc · คลิก `.drawer-backdrop` → `closeDrawer()` L1650 · ปุ่ม X/ปิด/ยกเลิก | drawer `--z-drawer` 55 · backdrop `--z-backdrop` 50 |
| **Modal** | `.modal` + `.modal-backdrop` | ตาม content (max 92vw) | `openModal()` L1665 — `scale(0.96)→1` | Esc · คลิก `.modal-backdrop` → `closeModal()` L1675 · ปุ่มยกเลิก/ปิด | **`--z-portal` 60** (>drawer · DSP-01 L1428) |
| **Search-select list** | `.ss-list` | ตาม input (portal → `.menu-fixed` ใน modal) | focus/พิมพ์ในช่อง search-select (`ssOpen` L1887) | click-outside (L1899) · Esc (ปิดแค่ list · L1897) · เลือก option | `--z-backdrop` 50 (portal ยกเป็น `--z-portal` 60) |
| **Portal menu** | `.menu-fixed` (`#overlay-root`) | ตาม trigger | `portalMenu()` L2072 (Rule #95 · หนี overflow clip + reposition ตอน scroll/resize) | คืนที่เดิมตอนปิด | `--z-portal` 60 |
| **Toast** | `.toast` | max 380px (fixed) | `showToast(msg,variant,dur)` L1734 | auto-hide (default 2800ms) | `--z-toast` 80 |
| **Demo strip** | `.demo-strip` | inline บนสุดของ content | เสมอ (prototype) | — (scaffolding) | (ในสาย content · ไม่ลอย) |

**Backdrop click map:**
- `.drawer-backdrop #drawerBackdrop` → `closeDrawer()`
- `.modal-backdrop #modalBackdrop` → `closeModal()` · ตัว `.modal` มี `event.stopPropagation()` (คลิกในกล่องไม่ปิด · L1542)

**Drawer modes (2 · `drawerHTML()` บรรทัด 2408):**
1. `wizard` — `dwWizard()` L2343 (สร้างใบเบิก 5 ขั้น · wide)
2. `view` — `dwView()` L2367 (รายละเอียด + 4 drawer-tabs)

**Modal types (4 · `modalHTML()` บรรทัด 2410):**
1. `submit` — ส่งอนุมัติ (P-04 · DOA slot picker + search-select ผู้อนุมัติ portal)
2. `approve` — อนุมัติ (P-04b · confirm · `modShell`)
3. `reject` — ไม่อนุมัติ/ตีกลับ (P-05 · textarea เหตุผลบังคับ)
4. `cancel` — ยกเลิกใบเบิก (P-06 · confirm soft archive)

---

## §7 · Interaction Spec

### Esc chain (anchor: handler จริง)
1. **บรรทัด 1748** — `window keydown` `if (e.key === 'Escape')`: ถ้า `state.modal.open` → `closeModal()` · else if `state.drawer.open` → `closeDrawer()` (modal ก่อน drawer — ปิดชั้นบนสุดก่อน)
2. **บรรทัด 1897** — `ssOnKey()` `else if(e.key === 'Escape')`: `e.stopPropagation()` + ปิดแค่ search-select list (ห้ามทะลุไปปิด drawer/modal · Rule #94 Esc chain)

### Click-outside
- User menu: `document click` ถ้าไม่อยู่ใน `.user-chip`/`.user-menu` → ปิด (บรรทัด 2191)
- Search-select: `document click` ถ้าไม่อยู่ใน `ss-<key>` → ปิด list (บรรทัด 1899)
- Backdrop click = ปิด overlay (ดู §6)

### Focus / scroll management (BASE-KIT)
- `trapFocus(box)` L1693 → กัน Tab หลุด + โฟกัสตัวแรก + คืนโฟกัสเดิมตอนปิด (`releaseFocus` L1709)
- **DSP-02 guard** (`guardOverlayAutoCombo` L1717): หลัง trapFocus auto-focus ถ้าช่องแรกเป็น `.ss-input` → บังคับปิด dropdown + blur (กัน combobox เผลอเปิดเองตอน auto-focus) · `ssBlurActive()` L1729 blur ก่อน render ตอนเลือกค่า
- `preserveRenderState()`/`restoreRenderState()` (Rule #29 · L1979/1997) → เก็บ scrollTop drawer/modal/page + focus+selection ข้าม innerHTML rebuild
- ⚠️ **ไม่มี scroll-lock** (`lockScroll`/`is-overlay-open`) ใน feature นี้ — เปิด overlay แล้ว body หลังยัง scroll ได้ (ต่างจาก feature อื่นที่ใช้ lockScroll · ดู §13 ข้อเสนอ)

### Positioning
- Drawer/modal/toast/backdrop = `position:fixed`
- `.ss-list` ปกติ = `position:absolute` (ไม่ดันเนื้อหา · Rule #35) · เด้งขึ้น `.ss-up` เมื่อล่างไม่พอ (`ssPlaceList` L1878) · ใน modal → portal เป็น `.menu-fixed` (`portalMenu`) หนี overflow clip
- `#modalBackdrop.has-combo` (L2506): เมื่อ modal ส่งอนุมัติเปิด → ปล่อย dropdown ลอยทับ ไม่ดัน scroll

### Render pattern
- `render()` (L2500 · full) — rebuild `#page-content` + drawer + modal · เรียก `applyRole()` + `initSelects()` + `renderIcons()` + `restoreRenderState()`
- `renderDrawerOnly()` (L2334) — rebuild เฉพาะ `#drawer` (ใช้ตอน wizard step/line edit)
- `refreshView()` (L2277) — rebuild เฉพาะ `#view` (ใช้ตอน filter)

---

## §8 · State-Driven UI Matrix

**Anchor status map:** `DST` (บรรทัด 2182) · `EXP.roles` (2120) · `maskM()` (2171) · footer view (2390-2396)

### Document status (`DST` · 7 states)
| enum | label | pill |
|---|---|---|
| `draft` | ฉบับร่าง | `pill-muted` |
| `pending_approval` | รออนุมัติ | `pill-warning` |
| `approved` | อนุมัติแล้ว | `pill-success` |
| `sent_to_pay` | ส่งจ่าย | `pill-info` |
| `paid` | จ่ายแล้ว | `pill-converted` |
| `rejected` | ตีกลับ | `pill-danger` |
| `cancelled` | ยกเลิก | `pill-danger` |

### View drawer footer (P-03 · state-driven · บรรทัด 2390)
| เงื่อนไข | ปุ่ม/สถานะที่แสดง |
|---|---|
| `pending_approval` + `canApprove()` | `ไม่อนุมัติ` (→reject modal) + `อนุมัติ` (→approve modal) |
| `pending_approval` + **non-approver** | ข้อความ "รออนุมัติ — เฉพาะผู้อนุมัติ (DOA) ดำเนินการได้" (RO) |
| `draft` | `ยกเลิก` (→cancel modal) + `ส่งอนุมัติ` (`openSubmitDraft` →submit modal) |
| `rejected` | `แก้ไขและยื่นใหม่` (`doReopen` L2422 → draft) |
| อื่น (approved/paid/cancelled) | `ปิด` อย่างเดียว |

### Persona / Scope / Masking (Iron Rule #105 · `EXP.roles` L2120 · `maskM` L2171 · `visibleDocs` L2173)
| persona (id) | บทบาท | approver | mask | scope | เห็นใบ |
|---|---|:--:|:--:|:--:|---|
| `admin` (สมชาย ใจดี) | ผู้เบิก/ธุรการ | ❌ | ✅ | `self` (E01) | เฉพาะใบของตน |
| `mgr` (วิไล ประสงค์) | ผู้อนุมัติ (DOA) | ✅ | ❌ | `all` | ทุกใบ |
| `officer` (อรทัย แสนสุข) | **⭐ เจ้าหน้าที่ (HR/Finance)** | ❌ | ❌ | `all` | ทุกใบ (touchpoint 3) |
- **money mask (FN-94):** role `mask:true` (admin) เห็นยอด**ใบของคนอื่น** = `฿ •••••` · ใบของตน (self) + ผู้อนุมัติ/เจ้าหน้าที่ เห็นเต็ม (`maskM` = `(mask && !isSelf) ? '฿ •••••' : fmtM`)
- **SoD:** อนุมัติ/ตีกลับ เฉพาะ `approver:true` (`canApprove` L2169) · เจ้าหน้าที่เห็นทุกใบแต่กดอนุมัติไม่ได้ (BR-12/13) · action guard ที่ mutation (`doApprove`/`doReject`) แสดง toast สิทธิ์ไม่พอ

---

## §9 · Microcopy (verbatim — R2 · คัดตรงตัวจากโค้ด)

### Toast ทั้งหมด (`showToast()` — ห้าม paraphrase · บางข้อความมีตัวแปรแทรก แสดง fragment คงที่)
| variant | ข้อความ (verbatim) |
|---|---|
| info | `ตีกลับ + แจ้งผู้เบิกแล้ว (แก้แล้วยื่นใหม่ได้)` |
| info | `ยกเลิกใบเบิกแล้ว (soft archive)` |
| info | `เปิดแก้ไขใบเบิก — แก้แล้วส่งอนุมัติใหม่ได้` |
| success | `ส่งคำขออนุมัติแล้ว — resolve สายตามวงเงิน + แจ้งผู้อนุมัติ` |
| success | `อนุมัติขั้น {n} แล้ว — รอขั้นถัดไป` *(fragment: `อนุมัติขั้น` + `แล้ว — รอขั้นถัดไป`)* |
| success | `อนุมัติครบสาย · ออกเลข {code} · บันทึกเข้า 7C ตาม CSQ_BRIEF_F101 · ส่งสถานะจ่าย (hook)` |
| warning | `ยกเลิกไม่ได้ — ทำได้เฉพาะใบฉบับร่าง` |
| warning | `สิทธิ์ไม่พอ — เฉพาะผู้อนุมัติ (DOA) ตีกลับได้` |
| warning | `สิทธิ์ไม่พอ — เฉพาะผู้อนุมัติ (DOA) อนุมัติได้` |
| warning | `อนุมัติไม่ได้ — ใบนี้ไม่ได้อยู่สถานะรออนุมัติ` |
| warning | `เปิดแก้ไขไม่ได้ — ทำได้เฉพาะใบที่ถูกตีกลับ` |
| info | `ทำสำเนาใบเบิก (mock)` · `ดาวน์โหลด PDF (mock)` *(header actions)* |

> **หมายเหตุ verbatim:** em-dash `—` · middot `·` ทุกตัวคงตามต้นฉบับ · `{n}`/`{code}` = ตัวแปร runtime (นับขั้น / เลขเอกสาร)

### Empty state (1 · `emptyStateHTML` L2274)
| จอ | title | desc |
|---|---|---|
| รายการใบเบิก | `ยังไม่มีใบเบิก` | สร้างใบเบิกใหม่ ระบบจะตรวจเพดานหมวดและ resolve สายอนุมัติตามวงเงินให้ (+ปุ่ม สร้างใบเบิก) |

### ปุ่มหลัก (verbatim)
`สร้างใบเบิก` · `ส่งออก` · `ถัดไป` · `ย้อนกลับ` · `ยกเลิก` · `บันทึกและส่งอนุมัติ` · `ส่งอนุมัติ` · `อนุมัติ` · `ไม่อนุมัติ` · `ยืนยันตีกลับ` · `ยกเลิกใบเบิก` · `แก้ไขและยื่นใหม่` · `ปิด` · `ล้างตัวกรอง` · `เพิ่มรายการ`

### ⭐ ช่องทางจ่าย (touchpoint 1 · `PAY_OPTS` L2165 · verbatim)
`ผ่านรอบเงินเดือน` · `โอนตรง` · `ใบสำคัญจ่าย (PV)` · `เงินสดย่อย (F091)`
ปลายทาง (`payDownstream` L2167): `เงินสดย่อย (hook F091 · Finance)` · `ใบสำคัญจ่าย PV (Finance)` · `รอบเงินเดือน (Payroll HK-1)` · `โอนตรง (Finance)`

### Note/hookbox สำคัญ (display-only · verbatim ย่อ)
- **⭐ F103 (touchpoint 2 · `advanceHookHTML` L2232):** `เคลียร์เงินทดรอง (F103 · soft-ref · display-only)` · "เงินทดรองค้างของผู้เบิก … หักลบอัตโนมัติกับยอดใบเบิก → ยอดจ่ายสุทธิ … (F101 ไม่ปรับยอดทดรองเอง · ส่งค่าหักลบให้ F103 · display-only)"
- **F117/F102** (`budgetHookHTML` L2237): "ตรวจงบประมาณ (Budget Control F117 — W7 ยังไม่ dev · hook display-only)" · "สิทธิ์คงเหลือจาก F102 …"
- **DOA:** "สายอนุมัติ (DOA · resolve ตามวงเงิน)" · "ช่วงวงเงินเป็น **ตัวอย่าง (mock)** — ตั้งค่าจริงที่ DOA กลาง · resolve ตอนส่ง แล้ว freeze · แก้ยอดข้ามช่วง = re-resolve อัตโนมัติ (BR-05)"
- **สถานะการจ่าย:** "display-only — Expense ไม่จ่าย/ไม่ลงบัญชีเอง"
- **over-cap:** "เกินเพดานหมวด {cat} ({cap}) — **เตือน แต่ยังส่งได้** · ต้องระบุเหตุผล"

---

## §10 · Data Binding & BACKEND Anchors

**Mock structures (แทน API จริง):** `EXP.docs`/`emps`/`cats`/`roles`/`audit` (บรรทัด 2115) · `DOA_RANGES` (2198) · `APPROVERS` (2204) · hook mock `F117_BUDGET_MOCK`/`F102_WELFARE_REMAIN`/`F103_ADVANCE_MOCK` (2222-2229)

| UI action | fn | API (FRD 02_API) | หมายเหตุ plug |
|---|---|---|---|
| list + filter (scope) | `listView`/`visibleDocs` | API-01 GET /expenses (scope self/all) | client filter → server scope+mask |
| ดูใบเบิก | `openView`/`dwView` | API-03 GET /expenses/:id (+ mask) | |
| สร้างใบเบิก (draft) | `openCreate`/`doSubmit` | API-02 POST /expenses | Idempotency-Key |
| แก้ไข (draft) | (wizard edit) | API-04 PUT /expenses/:id | |
| ส่งอนุมัติ (DOA) | `doSubmit`/`submitReady` | API-05 submit (→resolve DOA + NTF) | slot ไม่ hardcode · สายจาก F-DLG-001 |
| อนุมัติ (chain advance) | `doApprove` | API-06 approve (ครบ → เลข+PDF+7C) | re-check `canApprove` ที่ mutation |
| ตีกลับ (เหตุผลบังคับ) | `doReject` | API-07 reject (reason req · BR-18) | |
| ยกเลิก (draft) | `doCancel` | API-08 cancel (soft archive) | |
| แก้ไขและยื่นใหม่ | `doReopen` | API-09 reopen (rejected → draft) | |
| resolve DOA ตามวงเงิน | `resolveDoa` | API-12 GET /doa/resolve?amount= (ext F-DLG-001) | ช่วง = FREE ranges · ไม่ผูกโค้ด |
| หมวด/เพดาน | `EXP.cats` | API-13 GET /hr-config/expense-categories (ref F164 #107) | A-EXP-04 mock |
| ผู้เบิก/ผู้อนุมัติ combobox | `initSearchSelect` | API-14 GET /employees · Movement API-15 | snapshot cc ณ วันเบิก (BR-08) |
| ⭐ เคลียร์เงินทดรอง (F103) | `advanceHookHTML` | **API-16 GET /advances/outstanding (hook · display-only)** | FN-18 · ไม่ปรับยอดเอง (BR-11) |
| ตรวจงบ / สวัสดิการ | `budgetHookHTML` | **API-17/18 (hook · display-only mock)** | OQ-EXP-04 · จน F117 W7 พร้อม |
| ช่องทางจ่าย (hook) | `payDownstream` | API-10 pay-channel · API-11 pay-status (display-only) | ไม่จ่าย/ไม่ post (BR-09) |
| PDF สำเนา | `a4Doc` | API-20 GET /expenses/:id/pdf (snapshot ตอนอนุมัติ) | เลขจาก ENG-DOC-NUM · สำเนา ENG-DOC-STORE (BR-06) |

**Notification anchors (`<!-- NTF: … -->` inline · wire `ENG-NOTIFY` ตอน dev):**
1. `exp.submitted` — ยื่น (API-05 · L2435) → ผู้อนุมัติขั้นแรก
2. `exp.approved` — อนุมัติครบสาย (API-06 final · L2464) → ผู้เบิก
3. `exp.rejected` — ตีกลับ (API-07 · L2478) → ผู้เบิก
> `doa_pending`/`doa_result` มาจาก DOA engine อัตโนมัติ — **ห้ามประกาศซ้ำ** (L2436 · NTF_BRIEF_F101)

**Cross-module hooks (ทั้งหมด display-only · soft-ref):** F091 เงินสดย่อย · F103 เงินทดรอง (`advanceHookHTML`) · F117 Budget · F102 Welfare · DOA F-DLG-001 (resolve chain) · 7C posting (FC/EC ตาม CSQ_BRIEF_F101 · ไม่มี AC · BR-07) · เลขเอกสาร DOCCFG_BRIEF_F101

---

## §11 · Traceability + Drift Log

### Brief ↔ FRD ↔ HTML
| Brief § | FRD (P-xx / API / BR) | HTML anchor |
|---|---|---|
| §2 Route (no hash) | 01_UI §1.0 (P-01 `#/expense` เชิงแนวคิด) | `render` 2500 · `pageHTML` 2247 |
| §4 P-01 list | P-01 · API-01/03 · FN-19/94 | `listView` 2261 · `visibleDocs` 2173 |
| §4 P-02 wizard | P-02 · API-02 · BR-01/02/03/14 · FN-04/05/12/92 | `dwWizard` 2343 · `lineEditor` 2312 |
| §4 P-03 view 4 tabs | P-03 · API-03/16 · BR-08/11/16 | `dwView` 2367 · `advanceHookHTML` 2232 |
| §4 P-04 submit/DOA | P-04 · API-05/12 · BR-04/05 · FN-08/11 | `modalHTML submit` 2411 · `doSubmit` 2428 |
| §4 P-04b approve | (P-03 action) · API-06 · BR-06/07 · FN-11/22/23 | `doApprove` 2440 |
| §4 P-05 reject | P-05 · API-07 · BR-18 | `modalHTML reject` 2416 · `doReject` 2474 |
| §4 P-06 cancel | P-06 · API-08 | `modalHTML cancel` 2417 · `doCancel` 2480 |
| §4 P-07 PDF a4 | P-07 · API-20 | `a4Doc` 2399 |
| §8 State matrix | 05_RULES §5.x state machine | `DST` 2182 · footer 2390 |
| §8 Permission/scope/mask | 05_RULES BR-12/13 · FN-20/94 | `EXP.roles` 2120 · `maskM` 2171 · `canApprove` 2169 |
| §10 hooks (F103/F117/F102) | API-16/17/18 · BR-11/15 · OQ-EXP-04 | `advanceHookHTML` 2232 · `budgetHookHTML` 2237 |
| §10 pay-channel | API-10/11 · BR-09 · LOCK-03 | `PAY_OPTS` 2165 · `payDownstream` 2167 |

### ⚠️ Drift Log (HTML ↔ FRD)
| # | ประเภท | รายการ | ประเมิน | สถานะ |
|---|---|---|---|---|
| D-01 | HTML-only | Demo strip persona switch 3 บทบาท (`.demo-strip`) | Prototype scaffolding (Iron Rule #105) — จริงมาจากล็อกอิน · FRD ระบุ role matrix ถูกต้อง | **non-blocking** ✅ |
| D-02 | HTML-only | Bell icon `toggleNotif()` = no-op · header "ทำสำเนา/ดาวน์โหลด PDF" = toast mock | stub ของ shell · จริงต่อ Notification Center / doc engine | **non-blocking** ✅ |
| D-03 | HTML-only | Sidebar sibling (เงินเดือน/สวัสดิการ/การลา/ตั้งค่า HR) `<a>` ไม่มี onclick | placeholder feature ข้างเคียง module · นอก scope | **non-blocking** ✅ |
| D-04 | ตรงกัน (note) | F103/F117/F102 = display-only hook (mock) | HTML + FRD API-16/17/18 · BR-11/15 ตรงกัน — ห้าม hardcode · F117 รอ W7 (OQ-EXP-04) | **ตรง** ✅ |
| D-05 | ตรงกัน (note) | DOA slot ไม่ hardcode สาย · ช่วงวงเงิน FREE ranges · reject/over-cap ต้องระบุเหตุผล | ตรง BR-04/05/18 · LOCK-01 · role-id ปลายทาง (สาย DOA) = **OQ ให้ BA/DOA-declaration เคาะ** | **non-blocking** (OQ ค้าง) |
| D-06 | HTML-only (R4) | **ไม่มี scroll-lock** ตอนเปิด overlay (มี trapFocus + preserveRenderState) | prototype ยอมรับได้ · production ควรเพิ่ม (ดู §13) | **non-blocking** ✅ |

> **ไม่พบ business-blocking drift** · HTML สกัดจาก FRD เดียวกัน (P-01..P-07 ครบ) · verdict qc = PASS (coverage FN 22/22 · e2e ตามรายงาน step 5)

---

## §12 · Diff จากเวอร์ชันก่อน
— ไม่มี (ไม่ได้รับ HTML เวอร์ชันเก่ามา diff)

---

## §13 · 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT · R1 · คิดเพิ่ม)

> ต่อไปนี้ **ไม่มีใน HTML** — เสนอให้ dev/BA พิจารณา ห้ามถือเป็นสเปค
1. **ส่งออก (Export) จริง** (ปัจจุบันปุ่ม `ส่งออก` ไม่มี handler) — ต้อง mask money ตาม role (§8)
2. **scroll-lock ตอนเปิด overlay** — feature นี้ไม่มี `lockScroll`/`is-overlay-open` (D-06) · production ควรล็อก body scroll กัน scroll ทะลุใต้ drawer/modal
3. **Hook wiring จริง (F103/F117/F102/F091)** — เมื่อ module ปลายทาง dev เสร็จ → เปลี่ยน hookbox จาก mock เป็นค่าจริง (API-16/17/18/10)
4. **Loading/error state จริง** — mock ไม่มี network state · production ต้องมี skeleton/retry + map error codes (05_RULES: `ERR_NOT_APPROVER` 403 · `BR_DOA_SLOTS_INCOMPLETE` 422 ฯลฯ)
5. **OQ ค้างให้ BA/SEC เคาะ:** OQ-EXP-03 (scope self/all — เคาะแล้ว 2026-09-10) · OQ-EXP-04 (F117/F102 hook จน W7 พร้อม) · DOA role-id ปลายทาง (สาย + วงเงิน · /doa-declaration)

---
*Generated by html-ui-brief v1.0 · Extraction-based · source: expense.html (2513 บรรทัด)*
