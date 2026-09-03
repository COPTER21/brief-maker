# UI Brief (AS-BUILT) — ตั้งค่า HR · F-HR-CONFIG

> **EXTRACTION-BASED** — ทุกบรรทัดในเอกสารนี้ trace กลับ selector / function / ข้อความจริงใน HTML ได้
> ข้อเสนอที่ไม่มีใน HTML อยู่ที่ **§13 เท่านั้น**

---

## §0 Document Control + Pairing

| | |
|---|---|
| **HTML (source of truth)** | `1_HTML/ตั้งค่าHR.html` · 3,498 บรรทัด · 206,864 bytes · sha256 `426bc21d…` |
| **PREFLIGHT stamp ในไฟล์** | `PREFLIGHT v6.4` · round1 `spacing-off=7 font-sizes=5 flex-noalign=1 inline-layout=0 z-adhoc=0 hex-off=3` · round2 `7/7 checked` · note: ค่าที่เหลืออยู่ใน **BASE-KIT (Rule #69 ห้ามแก้)** · **page CSS = 0 ทุกตัวนับ** |
| **Gate ที่ผ่านแล้ว** | `audit.sh` FAIL=0 WARN=3 (kit) · `node --check` OK · render gate `GEOMETRY_BLOCK=0` `pageerror=0` · UX_CHECK 🟢 · COVERAGE_R1 🟢 (FN 53/53) |
| **FRD Pack ที่ pair** | `3_FRD/` (FULL · 9 ไฟล์) — pair แล้ว ✅ |
| **BRD** | `2_BRD/BRD_ตั้งค่าHR.md` (APPROVED) |
| **Generator** | `html-generator-v9` · archetype **master/config (A+B+C)** |
| **HTML เวอร์ชันก่อน** | ไม่มี (feature ใหม่) → **§12 ไม่มีเนื้อหา** |
| **สถานะ drift** | **1 รายการ (microcopy · แก้ปลายทางแล้ว)** — ดู §11 Drift Log |
| วันที่ | 2026-08-28 · S7 |

---

## §1 Design Tokens AS-BUILT

### §1.1 สี (จาก BASE-KIT `:root`)

| Token | ค่า | ใช้ที่ |
|---|---|---|
| `--c-primary` | `#FF3B30` | ปุ่มหลัก · toast info |
| `--c-primary-hover` | `#E62E24` | hover ของปุ่มหลัก |
| `--c-danger` | `#E62E24` | ปุ่มปิดใช้ · pill `pill-danger` |
| `--c-success` | `#1F9D55` | pill `pill-success` · toast success |
| `--c-warning` | `#E8870F` | pill `pill-warning` (รอมีผล) |
| `--c-teal` / `--c-teal-light` | `#FF9A1F` / `#FFB763` | accent (warm) |
| `--c-ink` | `#111111` | ข้อความหลัก |
| `--c-navy` / `--c-navy-2` | `#111111` | sidebar charcoal · `.demo-strip` |
| `--c-mute` / `--c-mute-2` / `--c-mute-3` | `#54565C` / `#73757B` / `#9A9CA2` | ข้อความรอง 3 ระดับ |
| `--c-line` / `--c-line-2` / `--c-line-3` | `#DEDAD4` / `#E9E5E0` / `#F1EEEA` | เส้นคั่น 3 ระดับ |
| `--c-bg-off` | `#FAF8F5` | พื้นหลัง off-white (Warm Light) |

> **ไม่มีสีนอก token ใน page CSS** (PREFLIGHT `hex-off=3` ทั้งหมดอยู่ใน BASE-KIT) · **ไม่มีม่วง/น้ำเงิน** ตาม CI Warm Light

### §1.2 ตัวอักษร / ระยะ / มุม

| กลุ่ม | Token | ค่า |
|---|---|---|
| Font size | `--fs-h1` `--fs-h2` `--fs-h3` `--fs-body` `--fs-sub` `--fs-meta` `--fs-cap` `--fs-kpi` | 22 / 17 / 15 / 14 / 13 / 12 / 11 / 28 px |
| Spacing | `--sp-xs` `--sp-sm` `--sp-md` `--sp-lg` `--sp-xl` | 4 / 8 / 12 / 20 / 28 px |
| Radius | `--r-xs` `--r-sm` `--r-md` `--r-lg` `--r-full` | 4 / 6 / 8 / 12 / 999 px |
| Font stack | Satoshi (Fontshare) + Noto Sans Thai (Google Fonts) | โหลดจาก CDN · มี fallback |

### §1.3 z-index map (สูง → ต่ำ)

| ระดับ | ตัวแปร | ใช้กับ |
|---|---|---|
| สูงสุด | `--z-toast` | `.toast` (แถบแจ้งเตือน) |
| ↑ | `--z-tooltip` (fallback `60`) | `.tip` ⓘ hover |
| ↑ | `--z-dropdown` | `.menu-fixed` · combobox list (`portalMenu`) |
| ↑ | `--z-drawer` | `#drawer` (แผงด้านข้าง) |
| ↑ | `--z-backdrop` | `#drawerBackdrop` · `#modalBackdrop` |
| **45** | **`--z-demo`** (ประกาศใน page CSS) | `.demo-strip` — **ตัวเดียวที่ page CSS ประกาศเอง** |
| ↓ | `--z-shell` | sidebar + shell-bar |
| ↓ | `--z-sticky` | `thead` sticky ของตาราง |
| ต่ำสุด | `1` / `2` / `3` | ชั้นภายใน component (เช่น overlay ของ stat card) |

> **`z-adhoc=0`** — ไม่มี z-index ตัวเลขลอยใน page CSS นอกจาก 1/2/3 ระดับ component

### §1.4 CSS ที่ page ประกาศเพิ่ม (utility · อยู่ใน `#page-late`)

`.content{padding-bottom:56px}` (กัน `.demo-strip` ทับ pagination) · `.page-fill{min-height/max-height:calc(100dvh - 148px)}` (≤1180px ใช้ 140px) · `.bar-right` `.mla` `.min0` `.tar` `.pos-rel` `.ta-auto` `.row-wrap` `.chips` · `.field-error.on{visibility:visible}` (ใช้ `visibility` ไม่ใช่ `display` — **ฟอร์มไม่กระตุกตอน error โผล่**) · `.row-bad{background:#FFE9E7}` · `.w44/.w110/.w120/.w150/.w168`

---

## §2 Route Map

| # | Route | หน้า | refresh-safe |
|---|---|---|---|
| 1 | `#/hr-config` | เข้าหน้า → ตกไป tab แรก | ✅ |
| 2 | `#/hr-config/leave` | ประเภทการลา | ✅ |
| 3 | `#/hr-config/ot` | อัตรา OT / กะ | ✅ |
| 4 | `#/hr-config/holiday` | ปฏิทินวันหยุด | ✅ |
| 5 | `#/hr-config/period` | รอบเวลา / รอบจ่าย | ✅ |
| 6 | `#/hr-config/appraisal` | รอบประเมิน | ✅ |
| 7 | `#/hr-config/company` | ขอบเขตบริษัท | ✅ |

- **นิยาม route:** `const TABS = [...]` (บรรทัด 2040) — แต่ละแถวมี `k` · `label` · `icon` (lucide) · `route`
- **handler:** `window.addEventListener('hashchange', function(){ state.pagination.page = 1; render(); })` → **เปลี่ยน tab รีเซ็ตหน้าของ pagination เป็น 1 เสมอ**
- `routeTab()` map hash → `state.tab` · `getRoute()` / `goTab()` / `goPage()` / `navigate()` เป็นตัวช่วยนำทาง
- **1 feature = 1 เมนูซ้าย (#104)** — sidebar มีรายการ "ตั้งค่า HR" รายการเดียว · 6 กลุ่มค่าเป็น tab ในหน้า
- เมนู sidebar อื่น = context เท่านั้น → `outOfScope()` → toast `“<ชื่อ>” อยู่นอกขอบเขตต้นแบบรอบนี้`

---

## §3 Layout Shell

| ส่วน | selector | สเปกจริง |
|---|---|---|
| Sidebar | `.sidebar` | กว้าง `--sidebar-w: 232px` · พื้น charcoal (`--c-navy`) flat · ที่ ≤ breakpoint ใช้ `transform: translateX(-100%)` + transition `.18s ease` (ซ่อน/เลื่อนเข้า) |
| Shell bar | `.shell-bar` | แถบบนสีขาว · เนื้อหา = breadcrumb + ไอคอนแจ้งเตือน + user chip เท่านั้น (slim) |
| Breadcrumb | ใน `.shell-bar` | `HR > ตั้งค่า HR > <ชื่อ tab>` · คั่นด้วย chevron-right |
| Content | `.content` | fluid — **ไม่มี max-width** · `padding-bottom:56px` |
| Page fill | `.page-fill` | สูงคงที่ `calc(100dvh - 148px)` → ตารางเลื่อนภายในตัวเอง ไม่ดันหน้าให้ยาว |
| Demo strip | `.demo-strip` | `position:fixed` มุมล่างซ้าย (`left:12px; bottom:12px`) · pill charcoal · `z-index:var(--z-demo)=45` · `font-size:11px` |

---

## §4 Page Anatomy (โครงเดียวใช้ทั้ง 6 tab)

หน้าเดียวสร้างจาก `renderPage()` → เนื้อหาต่างกันตาม `state.tab` (มาจาก `routeTab()`)

```
#page-content
├─ .page-header
│   ├─ .ph-title            → "ตั้งค่า HR"  (h1)
│   ├─ .tip ⓘ               → data-tip = OUT_TIP (ประกาศขอบเขต 11 ข้อ)
│   └─ .ph-actions          → ปุ่มหลักเดียว "สร้างค่าใหม่"  (Rule #46)
├─ .tabs > .tab × 6         → TABS[] (ชิดซ้าย · active ตาม state.tab)
├─ .stats > .stat.is-click × 4   → statCards(rows)  ★ กดเพื่อกรอง
├─ .filter-row              → ค้นหา · สถานะ · ขอบเขต · "มีผล ณ วันที่"  (แถวเดียว · วัดได้ 52px)
├─ .dt-band (เงื่อนไข)       → "กำลังดูค่าที่มีผล ณ <วันที่>" + ปุ่ม "กลับมาวันนี้"
├─ .page-fill > .table-wrap → ตาราง (thead sticky) · แถวสูง 47.1px
│   └─ COLS() 8 คอลัมน์
└─ .table-foot              → pagination + "แสดง x–y จาก z"
```

**คอลัมน์ (จาก `COLS()` บรรทัด 2412):**

| key | หัวคอลัมน์ | sort ได้ | หมายเหตุ |
|---|---|:---:|---|
| `name` | ค่า | ✅ | `.tbl-item` — ไอคอนกลุ่ม + ชื่อ + `.ti-code` (รหัส) เป็นบรรทัดรอง |
| `value` | ค่าปัจจุบัน | ✗ | `sumOf(r)` — สรุปค่าของเวอร์ชันที่ใช้อยู่ |
| `scope` | ขอบเขต | ✅ | มี `.tip` = `SCOPE_TIP` (อธิบายลำดับ resolve) |
| `status` | สถานะ | ✅ | `pill(st)` |
| `eff` | วันมีผล | ✅ | — |
| `next` | เวอร์ชันถัดไป | ✗ | badge วันที่ของเวอร์ชัน scheduled |
| `used` | ใช้ค่านี้ | ✅ | ชิดขวา — จำนวน consumer |
| `act` | (ว่าง) | ✗ | ชิดขวา — ปุ่ม action ต่อแถว |

> **tab `company` สลับคอลัมน์ที่ 2** จาก `ค่าปัจจุบัน` เป็น **`กลุ่มค่า`** (`base[1] = { k:'group', lb:'กลุ่มค่า' }`) — คุมจำนวนคอลัมน์ให้ ≤ 8 เท่าเดิม

**Stat cards (`statCards()` บรรทัด 2396):** 4 ใบ — `ค่าที่ใช้อยู่` (check-circle-2) · `รอมีผล` (clock-4) · `ร่าง` (file-pen-line) · `ปิดใช้` (archive)
- นับจาก `itemStatus(r)` ของแถวจริง — **ตัวเลข sync กับข้อมูล ไม่ hardcode**
- คลิกได้: `setStatFilter(k)` → `.stat.is-on` · meta เปลี่ยนจาก **"กดเพื่อกรอง"** → **"กำลังกรองอยู่"**

---

## §5 Component Inventory

| Component | anchor (selector / function) | โครง | States ที่มีจริง |
|---|---|---|---|
| Page tabs | `.tabs > .tab` · `goTab()` | 6 tab ชิดซ้าย | default / active (`is-on`) · **ไม่มี** disabled |
| Stat card | `.stat.is-click` · `statCards()` · `setStatFilter()` | label + value + meta | default / `is-on` (กรองอยู่) · hover (pointer) |
| Filter row | `.filter-row` · `filteredRows()` · `resetFilters()` | ค้นหา + 2 select + date picker | default / มีค่ากรอง / ล้างแล้ว (toast `ล้างตัวกรองแล้ว`) |
| As-of band | `.dt-band` · `setAsOf()` | ข้อความ + ปุ่มกลับ | แสดงเฉพาะเมื่อ `state.asOf` ไม่ใช่วันนี้ |
| Data table | `.table-wrap` + `thead` sticky · `actualRender()` · `sortBy()` | 8 คอลัมน์ · แถว 47.1px | loading / loaded / empty / filtered-empty |
| Empty state | `emptyStateHTML()` | ไอคอน + หัวข้อ + `desc` + ปุ่ม `actionLabel` | 2 แบบ: ยังไม่มีข้อมูล / **กรองแล้วไม่พบ** (`actionLabel:'ล้างตัวกรอง'` · desc มี "ลองล้างตัวกรอง หรือสร้างค่าใหม่ในกลุ่ม …") |
| Status pill | `pill(st)` · map `ST` | 22px · คำเดียว | 6 ค่า (ดู §8) |
| Person cell | `.tbl-person` · `.emp-av` · `comboPerson()` · `ini()` | ไอคอน/ตัวย่อ → ชื่อ → ตำแหน่ง · แผนก | default เท่านั้น |
| Search combobox | `searchSelectHTML(key)` · `initSearchSelect()` · `ssOpen/ssPick/ssOnInput/ssOnKey/ssRenderList/ssClear` | input + list + `<mark>` highlight คำค้น | closed / open / typing (highlight) / no-result / picked |
| Company chips | `.chips` · `dropCompany()` · `companyOptions()` | chip ถอดออกได้ | มีค่า / ว่าง (`ยังไม่ได้เลือกบริษัท`) |
| Stepper | `.stepper-row` + `.step-dot` · `STEPS` · `gotoStep()` · `stepBand()` | **3 ขั้น**: `ข้อมูลค่า` › `ค่าที่ใช้` › `ตรวจสอบและยืนยัน` | ขั้นปัจจุบัน / ผ่านแล้ว / ยังไม่ถึง |
| Milestone grid | `msGrid()` · `msAdd()` · `msDel()` · `msSet()` | ตารางขั้นอายุงาน | ว่าง / มีแถว / error (BR-16) · มี `.tip` "ถ้าใส่ ช่วงอายุงานต้องต่อเนื่อง ไม่ทับซ้อน และไม่มีช่องว่าง" |
| Holiday grid | `hdGrid()` · `hdAdd()` · `hdDel()` · `hdSet()` | ตารางวันหยุด | ว่าง / มีแถว / error · ปุ่ม `เพิ่มวันหยุด` |
| Period grid | `genPeriods()` · `doPeriod()` · `closedPeriods()` · `lockedPeriodOf()` · `lockedUntil()` | ตารางงวด 12 แถว | เปิดอยู่ / ปิดแล้ว · ปุ่ม `สร้างงวดทั้งปี` |
| Week chips | `weekChips()` · `toggleDay()` | จ–อา | เลือก / ไม่เลือก · error เมื่อ 0 วัน |
| Field error | `.field-error.on` · `validateField()` · `clearFieldError()` · `errNote()` | ข้อความใต้ช่อง | ซ่อน (`visibility:hidden`) / แสดง — **ไม่ดันเลย์เอาต์** |
| Tip | `.tip[data-tip]` | ⓘ hover | มี 5 ข้อความหลัก (§9.4) — **ไม่มี hint banner (#106)** |
| Toast | `#toast` · `showToast(msg, variant, durationMs=2800)` | ไอคอน + ข้อความ | 4 variant: `success` `info` `warning` `error` |
| Demo strip | `.demo-strip` · `setPersona()` | สลับ persona | HR Admin / HR Staff |
| Submit button | `submitVersion()` · `state.drawer.busy` | ปุ่มหลักล่างขวา | ปกติ / **busy** (`is-disabled` + `loader-2 spin` + ข้อความ `กำลังบันทึก…`) |

---

## §6 Overlay Registry

| Overlay | anchor | ขนาด | backdrop | เปิดด้วย | ปิดด้วย | z |
|---|---|---|---|---|---|---|
| **Drawer (สร้าง/แก้)** | `#drawer` · `.drawer` · `openDrawer('create'|'edit')` · `openEdit()` · `openCreate()` | `width: min(920px, 100vw)` (kit ยังมี `.standard` 680 และ `.wide` 1290 แต่ **feature นี้ใช้ 920 อย่างเดียว**) | `#drawerBackdrop` | ปุ่ม `สร้างค่าใหม่` / `แก้ไข` | ปุ่ม `ยกเลิก` · ปุ่ม X · **Esc** · `closeDrawer()` (มี transition 280ms ก่อน reset state) | `--z-drawer` |
| **Drawer (ดูค่า)** | `#drawer` · `openView()` · `renderViewDrawer()` · `.drawer-header.has-tabs` | 920px | เดียวกัน | คลิกแถวในตาราง | ปุ่ม `ปิด` · X · **Esc** | `--z-drawer` |
| **Modal** × 6 ชนิด | `#modalBackdrop .modal` · `openModal(type, data)` · `renderModal()` · `closeModal()` | modal มาตรฐาน kit | `#modalBackdrop` | ปุ่มบนแถว / ปุ่มใน drawer | ปุ่ม ghost · **Esc** | `--z-backdrop` + modal |
| **Combobox menu** | `portalMenu()` · `positionMenu()` · `.menu-fixed` · `openOverlay()` / `closeOverlay()` | ตามความกว้าง trigger | ไม่มี | คลิก/พิมพ์ที่ช่อง | เลือกตัวเลือก · Esc (ปิดเฉพาะ list) · คลิกนอก · เปิดตัวอื่น (ปิดตัวเดิมอัตโนมัติ) | `--z-dropdown` |
| **Toast** | `#toast` | แถบ | ไม่มี | `showToast()` | **auto-dismiss 2,800ms** — ไม่มีปุ่มปิด | `--z-toast` |
| **Tooltip** | `.tip[data-tip]` | ตามข้อความ | ไม่มี | hover | ออกจาก hover | `--z-tooltip` (fallback 60) |

### Modal ทั้ง 6 ชนิด (จาก `openModal('<type>')`)

| type | หัวข้อบนจอ (verbatim) | ปุ่มหลัก | ปุ่มรอง | เนื้อหาเด่น |
|---|---|---|---|---|
| `deactivate` | `ปิดใช้ “<ชื่อค่า>”` | **`ปิดใช้`** (danger · `doDeactivate()`) | `ยกเลิก` | **รายการ consumer ที่อ้างอยู่** + pill `พร้อมใช้`/`ยังไม่ทำ` · ถ้าไม่มี → `ยังไม่มี feature ใดอ้างค่านี้` · ช่องเหตุผล placeholder `เช่น ไม่มีการใช้สิทธิ์ต่อเนื่อง 3 ปี` |
| `reactivate` | `เปิดใช้ “<ชื่อค่า>” กลับ` | **`ต่อไป`** (primary · `doReactivate()`) | `ยกเลิก` | subtitle: `การเปิดใช้กลับต้องสร้างเวอร์ชันใหม่พร้อมวันมีผล เพื่อให้ย้อนดูได้ว่าเปิดกลับตั้งแต่วันไหน` · hint: `กดต่อไปเพื่อกรอกค่าและวันมีผลของเวอร์ชันใหม่` → **เปิดฟอร์มเวอร์ชันใหม่ ไม่ได้กรอกวันในหน้าต่างนี้** |
| `cancelver` | `ยกเลิกเวอร์ชันที่รอมีผล` | **`ยกเลิกเวอร์ชัน`** (`doCancelVersion()`) | **`ไม่ยกเลิก`** | แสดงเวอร์ชันที่รอมีผล + ข้อความว่าค่าที่ใช้อยู่ปัจจุบันจะใช้ต่อไป |
| `closeper` / `reopenper` | `ปิดงวด <งวด>` / `เปิดงวด <งวด> กลับ` | **`ปิดงวด`** / **`เปิดงวดกลับ`** (`doPeriod()`) | `ยกเลิก` | เปิดกลับต้องมีเหตุผล |
| `quota` | `โควตาต่ำกว่าขั้นต่ำตามกฎหมาย` | **`ยืนยันบันทึก`** (`ackQuota()`) | **`กลับไปแก้`** | subtitle: `โควตาลาพักร้อน <n> วันต่อปี ต่ำกว่าขั้นต่ำ <m>` · body: `รายการนี้จะถูกบันทึกไว้ในประวัติเวอร์ชันพร้อมผู้ยืนยัน` |

> **ไม่มี overlay ที่ "ห้ามปิด"** — ทุก overlay ปิดได้ด้วย Esc/ปุ่ม ยกเว้น toast ที่หายเอง

---

## §7 Interaction Spec

### §7.1 Esc chain (ตามลำดับใน handler จริง · บรรทัด 1691–1696)
```js
window.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    if (state.modal.open) closeModal();       // ← ชั้นนอกสุดก่อน
    else if (state.drawer.open) closeDrawer();
  }
});
```
1. **modal ก่อนเสมอ** — Esc ตอนมี modal ซ้อนบน drawer จะปิดเฉพาะ modal (drawer ยังอยู่)
2. **drawer เป็นชั้นถัดไป**
3. **combobox list มี handler ของตัวเอง** (`ssOnKey`): `Escape` → `s.open=false` + `ssSetText/ssSyncChrome/ssRenderList` — ปิดเฉพาะ list ไม่ปิด drawer

### §7.2 Overlay dismiss / click-outside
- `openOverlay(menu, trigger)` — เปิดตัวใหม่จะ **ปิดตัวอื่นที่เปิดอยู่ทั้งหมด** (`querySelectorAll('[data-overlay].open')`)
- `closeOverlay(menu)` — คืน focus ให้ trigger (`menu._trigger.focus()`)
- `positionMenu()` + `.menu-fixed` — เมนูใช้ **fixed positioning** ผ่าน portal (`portalMenu`) เพื่อไม่ให้ถูก `overflow` ของตารางตัด

### §7.3 Focus / RAF / animation
- `openPanel()` — `render()` ก่อน แล้ว `requestAnimationFrame` ค่อยเพิ่ม `.is-open` ให้ backdrop + drawer → **transition ทำงานจริง ไม่กระโดด**
- `closeDrawer()` — ถอด `.is-open` แล้ว `setTimeout(…, 280)` จึง reset `state.drawer` และ `render()` → รอ animation จบก่อนล้าง DOM
- `showToast()` — `requestAnimationFrame` เพิ่ม `.is-visible` · `setTimeout` ถอดออกที่ `durationMs` (default **2800ms**)

### §7.4 Render preservation (Iron Rule #29)
`render()` ทำ `innerHTML` rebuild ทั้ง page/drawer/modal → ครอบด้วย
`preserveRenderState()` → … → `restoreRenderState(snap)` (มี `withRenderPreservation()` / `preservedRender()` เป็นตัวช่วย)
→ **scroll position · focus · ค่าที่พิมพ์ค้าง ไม่หายตอน re-render** · `initCombos()` + `renderIcons()` ถูกเรียกใหม่ทุกครั้ง

### §7.5 Scroll / geometry
- `.page-fill` ล็อกความสูง → `.table-wrap` เลื่อนในตัวเอง + `thead` sticky (`--z-sticky`)
- `.content{padding-bottom:56px}` — กัน `.demo-strip` (fixed ล่างซ้าย) ทับ pagination
- ตรวจแล้ว: **ไม่มี body h-scroll** ที่ 1440 และ 1024 · drawer 920px ที่ viewport 1024 ยังอยู่ในกรอบ

### §7.6 Validation timing
- `gotoStep(n)` — ถ้าไปข้างหน้าและ `validateStep(step)` ไม่ผ่าน → `render()` + toast `ยังกรอกไม่ครบ ตรวจข้อความสีแดง` แล้ว **return (ไม่ข้ามขั้น)**
- ย้อนกลับไม่ validate
- `validateField()` / `clearFieldError()` — error รายช่องใช้ `visibility` (ไม่ดันเลย์เอาต์)
- `submitVersion()` — ตั้ง `state.drawer.busy = true` → ปุ่มเป็น `is-disabled` + `loader-2 spin` + ข้อความ `กำลังบันทึก…` → **กันกดซ้ำ**

---

## §8 State-Driven UI Matrix

### §8.1 สถานะเวอร์ชัน (`const ST` บรรทัด 2076 · แสดงผ่าน `pill(st)`)

| enum | label บนจอ | class | สี | ปุ่มที่ปรากฏบนแถว |
|---|---|---|---|---|
| `draft` | **ร่าง** | `pill-muted` | เทา | แก้ไข · ทิ้งร่าง |
| `scheduled` | **รอมีผล** | `pill-warning` | ส้ม | แก้ไข · **ยกเลิกเวอร์ชันที่รอมีผล** · ปิดใช้ |
| `active` | **ใช้อยู่** | `pill-success` | เขียว | แก้ไข (→ สร้างเวอร์ชันใหม่) · ปิดใช้ |
| `superseded` | **ถูกแทน** | `pill-muted` | เทา | — (อ่านอย่างเดียว) |
| `inactive` | **ปิดใช้** | `pill-danger` | แดง | **เปิดใช้กลับ** เท่านั้น |
| `cancelled` | **ยกเลิก** | `pill-muted` | เทา | — |

### §8.2 สถานะงวด (`hr_pay_period`)

| ค่า | pill บนจอ | ปุ่ม |
|---|---|---|
| เปิด | **เปิดอยู่** (`pill-success`) | `ปิดงวด` |
| ปิด | **ปิดแล้ว** (`pill-muted`) | `เปิดใช้กลับ` → modal `reopenper` (ปุ่ม `เปิดงวดกลับ`) |

### §8.3 สถานะการเชื่อม consumer (`CONSUMERS` บรรทัด 2065)

| `ready` | pill | หมายเหตุ |
|---|---|---|
| `true` | **พร้อมใช้** (`pill-success`) | ปัจจุบันมีตัวเดียว: `F-SALARY` โครงสร้างเงินเดือน |
| `false` | **ยังไม่ทำ** (`pill-muted`) | อีก 7 ตัว: การลา · OT/กะทำงาน · จัดกะและตารางเวร · ลงเวลาทำงาน · เงินเดือน · ประเมินผลงาน · สวัสดิการ |

### §8.4 persona (demo)

| persona | ผลบนจอ |
|---|---|
| HR Admin | ปุ่มทุกตัวใช้งานได้ · toast `สลับเป็น HR Admin — แก้ไขได้` |
| HR Staff | ปุ่มที่ต้องสิทธิ์ `is-disabled` · กดแล้ว toast `บทบาท HR Staff ดูได้อย่างเดียว` (warning) · toast ตอนสลับ `สลับเป็น HR Staff — อ่านอย่างเดียว` |

---

## §9 Microcopy (verbatim — คัดจากโค้ดตรงตัว)

### §9.1 Toast ทุกตัว (`showToast(...)` ทั้ง 15 call)

| ข้อความ | variant | ยิงจาก |
|---|---|---|
| `“<ชื่อเมนู>” อยู่นอกขอบเขตต้นแบบรอบนี้` | info | `outOfScope()` — เมนู sidebar นอก scope |
| `สลับเป็น HR Admin — แก้ไขได้` | info | `setPersona('admin')` |
| `สลับเป็น HR Staff — อ่านอย่างเดียว` | info | `setPersona('staff')` |
| `ล้างตัวกรองแล้ว` | info | `resetFilters()` |
| `บทบาท HR Staff ดูได้อย่างเดียว` | warning | ทุก action ที่ต้องสิทธิ์ (7 จุด) |
| `ยังกรอกไม่ครบ ตรวจข้อความสีแดง` | error | `gotoStep()` เมื่อ `validateStep()` ไม่ผ่าน |
| `บันทึกร่างแล้ว — ยังไม่มีผลกับ feature ใด` | success | `saveDraft()` |
| `ยังตั้งวันมีผลไม่ได้ ตรวจข้อความสีแดง` | error | `submitVersion()` เมื่อ validate ขั้น 3 ไม่ผ่าน |
| `บันทึกแล้ว — มีผลตั้งแต่วันนี้` | success | `submitVersion()` เมื่อ `effective_date` = วันนี้ |
| `บันทึกแล้ว — จะมีผล <วันที่>` | success | `submitVersion()` เมื่อวันมีผลอนาคต (`be(f.eff)`) |
| `สร้างงวดปี <ปี พ.ศ.> ครบ 12 งวดแล้ว` | success | `genPeriods()` |
| `ปิดใช้แล้ว — ข้อมูลเดิมที่อ้างค่านี้ยังอ่านได้` | success | `doDeactivate()` |
| `ยกเลิกเวอร์ชันที่รอมีผลแล้ว` | success | `doCancelVersion()` |
| `ปิดงวด <งวด> แล้ว` | success | `doPeriod()` (closing = true) |
| `เปิดงวด <งวด> กลับแล้ว` | success | `doPeriod()` (closing = false) |

### §9.2 ปุ่ม (verbatim)

| บริบท | ปุ่ม |
|---|---|
| Page header | `สร้างค่าใหม่` |
| Drawer footer (ทุกขั้น) | `ยกเลิก` (ghost) · `ย้อนกลับ` (secondary · เฉพาะขั้น ≥2) · `บันทึกร่าง` (secondary) |
| Drawer footer ขั้นที่ไม่ใช่ขั้นสุดท้าย | **`ถัดไป`** (primary · chevron-right) |
| Drawer footer ขั้นสุดท้าย | **`บันทึกและตั้งวันมีผล`** (primary · check) → ระหว่างบันทึก: **`กำลังบันทึก…`** (loader-2 spin · disabled) |
| View drawer | `แก้ไข` · `ดูประวัติเวอร์ชัน` · `ปิดใช้` · `ปิด` |
| แถวในตาราง | `ปิดใช้` (title="ปิดใช้") · `เปิดใช้กลับ` (title="เปิดใช้กลับ") · `ยกเลิกเวอร์ชันที่รอมีผล` |
| tab รอบเวลา/รอบจ่าย | `สร้างงวดทั้งปี` · `ปิดงวด` · `เปิดกลับ` |
| grid | `เพิ่มขั้น` (milestone) · `เพิ่มวันหยุด` (ปฏิทิน) |
| as-of band | `กลับมาวันนี้` |
| empty state (กรองแล้วไม่พบ) | `ล้างตัวกรอง` |
| modal | `ปิดใช้` · `ต่อไป` · `ยกเลิกเวอร์ชัน` · `ไม่ยกเลิก` · `ปิดงวด` · `เปิดงวดกลับ` · `ยืนยันบันทึก` · `กลับไปแก้` · `ยกเลิก` |

### §9.3 ข้อความ validation (verbatim — คู่กับ VR ใน `05_RULES`)

| ข้อความบนจอ | VR |
|---|---|
| `กรอกชื่อค่า (ไทย)` | VR-24 |
| `กรอกชื่อค่าก่อนบันทึกร่าง` | (บันทึกร่าง) |
| `กรอกรหัสค่า` | VR-23 |
| `รหัสค่าใช้ได้เฉพาะตัวพิมพ์ใหญ่ ตัวเลข และเครื่องหมาย -` | VR-23 |
| `รหัสค่านี้มีอยู่แล้วในกลุ่ม <กลุ่ม>` | VR-23 |
| `เลือกบริษัทอย่างน้อย 1 บริษัท` | VR-22 |
| `โควตาต้องไม่ติดลบ` | VR-09 |
| `เปอร์เซ็นต์ที่จ่ายต้องอยู่ระหว่าง 1–99` | VR-10 |
| `ยกยอดต้องไม่ติดลบ` | VR-12 |
| `ยกยอดมากกว่า 0 ต้องระบุวันหมดอายุยกยอด` | VR-12 |
| `ระบุเอกสารที่ต้องแนบ` | VR-11 |
| `ขั้นที่ <n> มีปีสิ้นสุดน้อยกว่าปีเริ่ม` | VR-13 |
| `ช่วงอายุงานทับซ้อนกันที่ขั้นที่ <n>` | VR-13 |
| `ช่วงอายุงานมีช่องว่างระหว่างขั้นที่ <n>` | VR-13 |
| `กรอกตัวคูณ` | VR-06 |
| `ตัวคูณต่ำกว่าขั้นต่ำตามกฎหมายแรงงาน — <ขั้นต่ำ>` | VR-06 |
| `เพดานชั่วโมงต้องมากกว่า 0` | VR-07 |
| `เวลาออกต้องมากกว่าเวลาเข้า หรือติ๊ก “กะข้ามวัน”` | VR-14 |
| `ช่วงพักต้องอยู่ในช่วงเวลาของกะ` | VR-15 |
| `เลือกวันทำงานอย่างน้อย 1 วัน` | VR-16 |
| `กรอกปี` | (ปฏิทิน/รอบประเมิน) |
| `วันที่ <วันที่> …` (วันหยุดซ้ำ) | VR-17 |
| `วันตัดเวลาต้องอยู่ระหว่าง 1–31` | VR-19 |
| `วันจ่ายต้องอยู่ระหว่าง 1–31` | VR-19 |
| `วันตัดเวลาต้องไม่เกินวันจ่ายในงวดเดียวกัน` | VR-19 |
| `ช่วงประเมินต้องเริ่มก่อนสิ้นสุด` | VR-20 |
| `ช่วงเปิดกรอกต้องเริ่มก่อนสิ้นสุด` | VR-21 |
| `ช่วงเปิดกรอกต้องอยู่หลังหรือคร่อมช่วงประเมิน` | VR-21 |
| `ช่วงวันทับซ้อนกับรอบ “<ชื่อรอบ>”` | VR-20 |
| `ต้องกรอกวันมีผลก่อนบันทึก (บันทึกร่างไว้ก่อนได้)` | VR-01 |
| `ตั้งวันมีผลย้อนเข้างวด <งวด> ที่ปิดแล้วไม่ได้ — วันที่ตั้งได้เร็วที่สุดคือ <วันที่>` | VR-03 |
| `มีเวอร์ชันที่ใช้วันมีผลนี้อยู่แล้ว — เลือกวันอื่น` | VR-02 |
| `กรอกเหตุผลการเปลี่ยนอย่างน้อย 10 ตัวอักษร` | VR-04 |
| `กรอกเหตุผลอย่างน้อย 10 ตัวอักษร` | VR-05 |

### §9.4 `.tip` ⓘ (ข้อความอธิบาย — แทน hint banner ตาม #106)

| ที่ | ข้อความ (verbatim) |
|---|---|
| ข้างชื่อหน้า (`OUT_TIP`) | `ขอบเขตรอบนี้: ไม่มีขั้นอนุมัติ · ไม่คำนวณย้อนหลัง · ไม่มีสูตรเงินเดือน · ไม่มียอดวันลารายคน · ไม่มีตัวสลับบริษัทบนหัวจอ · ไม่ดึงวันหยุดราชการให้ · ไม่แจ้งเตือนพนักงาน · ไม่มีนำเข้า/ส่งออกค่าเป็นชุด · ไม่มีระยะทดลองงาน · ไม่มีความถี่คำนวณจ่าย · ไม่มีการมัดชุดค่าให้กลุ่มพนักงาน` — **ครบ 11 ข้อ (FN-40…FN-47, FN-51…FN-53)** |
| ตัวกรองวันที่ | `เลือกวันย้อนหลังเพื่อดูว่าวันนั้นบริษัทใช้ค่าอะไร` |
| ช่องขอบเขตการใช้ | `รอบนี้กำหนดได้ระดับบริษัทเท่านั้น ยังไม่เปิดให้เลือกกลุ่มพนักงาน` |
| ช่องรหัสอ้างอิงจ่ายเงิน | `ช่องอ้างอิงเท่านั้น ไม่ผูกสูตรคำนวณเงิน` |
| ช่องตัวคูณ OT | `ขั้นต่ำตามกฎหมายแรงงาน: OT วันทำงาน 1.5 · ทำงานวันหยุด 1.0 · OT วันหยุด 3.0` |
| ล็อกงวด | `งวดที่ปิดแล้วจะแก้ค่าที่กระทบงวดนั้นไม่ได้` |
| ช่องวันมีผล | `ทุกค่าต้องมีวันมีผล เพื่อย้อนดูได้ว่าวันนั้นบริษัทใช้กติกาอะไร` |
| ตาราง milestone | `ถ้าใส่ ช่วงอายุงานต้องต่อเนื่อง ไม่ทับซ้อน และไม่มีช่องว่าง` |
| คอลัมน์ขอบเขต | `SCOPE_TIP` (อธิบายลำดับ resolve — บริษัทลูกทับค่ากลาง) |

### §9.5 ข้อความสถานะ / empty / hint

| ที่ | ข้อความ |
|---|---|
| แถวที่ปิดใช้ | `ปิดใช้แล้ว — เลือกใหม่ไม่ได้` |
| tab ใครใช้ค่านี้ (ว่าง) | `ยังไม่มี feature ใดอ้างค่านี้` |
| หัวข้อในกลุ่มปลายทาง | `feature ที่อ่านค่านี้ไปใช้` |
| ช่องบริษัทว่าง | `ยังไม่ได้เลือกบริษัท` |
| ช่องที่ไม่บังคับ | `ไม่ใส่ก็ได้` |
| ตั้งวันมีผลได้เร็วสุด | `ตั้งได้เร็วสุด <วันที่>` |
| แถบดูย้อนหลัง | `กำลังดูค่าที่มีผล ณ <วันที่>` |
| เวอร์ชันรอมีผลบนแถว | `มีเวอร์ชันรอมีผล <วันที่>` |
| ในไทม์ไลน์ประวัติ | `เวอร์ชัน <n>` / `เหตุผล: <ข้อความ>` |
| pagination | `แสดง <x>–<y> จาก <z>` |
| stat card | `กดเพื่อกรอง` / `กำลังกรองอยู่` |
| หัวข้อกลุ่มฟิลด์ในฟอร์ม | `ชื่อและรหัสของค่า` · `ขอบเขตการใช้ค่า` · `ผู้รับผิดชอบ` · `สิทธิ์และโควตา` · `ขั้นโควตาตามอายุงาน` · `ยกยอดและ prorate` · `กติกาการนับวันลาและเอกสาร` · `อัตราและฐานคำนวณ` · `เวลาทำงานของกะ` · `ชุดปฏิทิน` · `วันหยุดในชุดปฏิทิน` · `กติการอบตัดเวลาและรอบจ่าย` · `ช่วงรอบประเมิน` · `ประเภทค่าในกลุ่มนี้` · `วันที่ค่านี้เริ่มมีผล` · `ตรวจสอบก่อนบันทึก` |
| loader ของไอคอน | `[Lucide] All CDNs failed. Icons จะไม่แสดง but UI ยังใช้งานได้` (console เท่านั้น) |

---

## §10 Data Binding & จุดต่อระบบจริง

> **หมายเหตุสำคัญ:** ไฟล์นี้ **ไม่มีคอมเมนต์ `// BACKEND:` และไม่มีศัพท์ engine บนจอเลย** (ตรวจแล้ว — เป็นไปตาม #81/#106 และ CSQ_BRIEF ที่ห้ามศัพท์ท่อโผล่บนจอ) · จุดต่อจึงระบุจาก **mock structure + function ที่ mutate state**

| Mock ในไฟล์ | โครง | ต่อกับ (FRD) |
|---|---|---|
| `TABS[]` (6 แถว) | `k · label · icon · route` | `01_UI §1.1` P-02…P-07 |
| `COMPANIES[]` | `id · name · code · meta` (เช่น `C-2BS` `2BSimple Group` `บริษัทแม่`) | soft ref → Organization · `04_DB` `T_hr_config_item_company` |
| `EMPLOYEES[]` | `id · name · pos · dept` (เช่น `E-1005` กมลชนก ใจดี) | soft ref → Employee Master · `04_DB` `owner_employee_id` + snapshot |
| `CONSUMERS[]` (8 แถว) | `code · name · wave · ready · uses[]` | `04_DB` `T_hr_config_usage` · `02_API` API-11 |
| `ST{}` | 6 สถานะ → `lb` + `cls` | `05_RULES §5.2` state machine |
| `OT_MIN{}` | `{'OT วันทำงาน':1.5, 'ทำงานวันหยุด':1.0, 'OT วันหยุด':3.0}` | **`04_DB` `T_hr_legal_minimum`** — ⚠️ ในต้นแบบเป็นค่าคงที่ · **ระบบจริงต้องอ่านจากตารางที่มี `effective_date`** (BR-05 · P-8) |
| `LEAVE_MIN_VAC = 6` | ขั้นต่ำโควตาลาพักร้อน | **`T_hr_legal_minimum` `leave.annual_min_days`** — เงื่อนไขเดียวกัน (BR-06) |
| `STEPS[]` | `['ข้อมูลค่า','ค่าที่ใช้','ตรวจสอบและยืนยัน']` | `01_UI §1.0` P-08 (Stepper #47) |
| `state{}` | `tab · filters · asOf · pagination · sort · drawer{open,mode,recordId,step,tab,form,err,busy} · modal{open,type,data} · persona` | — (client state) |

### จุดที่ FE ต้อง plug API (map จาก function → `02_API`)

| function ในต้นแบบ | ทำอะไร | API จริง |
|---|---|---|
| `filteredRows()` · `sortBy()` · `setStatFilter()` · `setAsOf()` | กรอง/เรียง/ดู ณ วันที่ (ทำในหน่วยความจำ) | **`API-01`** `GET /hr-config/items` (`group`, `status`, `company_id`, `q`, `as_of`, `sort`, `limit`, `offset`) |
| `openView()` · `rec(id)` | เปิดรายละเอียด | **`API-02`** |
| `saveDraft()` | บันทึกร่าง | **`API-03`** (สร้าง) / **`API-05`** (แก้ร่าง) |
| `openEdit()` → `isNewVersion:true` | เปิดฟอร์มเวอร์ชันใหม่ (copy payload) | **`API-04`** |
| `submitVersion()` | ตั้งวันมีผล → publish | **`API-06`** (+ `Idempotency-Key`, `If-Match`) |
| `doCancelVersion()` | ยกเลิกเวอร์ชันรอมีผล | **`API-07`** |
| (ทิ้งร่าง) | discard | **`API-08`** |
| `doDeactivate()` | ปิดใช้ (ต้องส่ง `acknowledged_usage`) | **`API-09`** |
| `doReactivate()` | เปิดใช้กลับ → เปิดฟอร์มเวอร์ชันใหม่ | **`API-10`** |
| `usedBy(r)` | รายการ consumer | **`API-11`** |
| `verAt()` · `lastVer()` · `curVer()` · `nextVer()` · `effTo()` | ประวัติ/ช่วงมีผล | **`API-12`** + `03_LOGIC` FN-19 |
| (ไม่มีใน UI — server-to-server) | ปลายทางอ่านค่า | **`API-13`** `GET /hr-config/resolve` |
| `genPeriods()` | สร้างงวดทั้งปี | **`API-14`** + `ENG-HRCFG-02` |
| `doPeriod()` (closing=true / false) | ปิด / เปิดงวดกลับ | **`API-15`** / **`API-16`** |
| `closedPeriods()` · `lockedPeriodOf()` · `lockedUntil()` | หา "งวดที่ปิดแล้ว" + วันแรกที่ตั้งได้ | **`API-17`** + `03_LOGIC` **FN-20** (⚠️ ระบบจริงต้อง re-validate ตอน commit ด้วย — LD-07) |
| `validateStep()` · `validateField()` | validate ฝั่ง UI | **`03_LOGIC` FN-05** ต้อง validate ซ้ำฝั่ง server เสมอ |
| `showToast()` | ข้อความผลลัพธ์ | map กับ error code ใน `05_RULES §5.6` |

### สิ่งที่ต้องเพิ่มตอนต่อของจริง (ไม่มีในต้นแบบ — โดยเจตนา)

1. **การยิง event ให้ ENG-CSQ (SecC) 6 ตัว** — ต้นแบบไม่มีศัพท์ engine บนจอเลย (ถูกต้องตาม #81) · ระบบจริงยิงที่ `03_LOGIC` FN-16
2. **การเขียน audit** — `03_LOGIC` FN-17 (เขียนไม่สำเร็จ = rollback)
3. **สิทธิ์จริงจาก Policy Center** — ต้นแบบใช้ `persona` ใน `.demo-strip` เท่านั้น (ระบบจริงบังคับที่ระดับ API — `05_RULES §5.3`)
4. **`OT_MIN` / `LEAVE_MIN_VAC` ต้องย้ายเข้า `T_hr_legal_minimum`** (ห้าม hardcode — BR-05/BR-06 · OQ-10)

### Assets / ข้อจำกัด

- ไอคอน: **Lucide** โหลดผ่าน `loadLucide()` (multi-CDN + fallback no-op) · `renderIcons()` เรียกทุกครั้งหลัง render
- **ไม่มีเน็ต → ไอคอนไม่แสดง แต่ UI ใช้งานได้ปกติ** (console แจ้ง `[Lucide] All CDNs failed…`) — ตรวจแล้วไม่เกิด error
- ฟอนต์: Satoshi (Fontshare) + Noto Sans Thai (Google Fonts) · ไฟล์เดียว ไม่มี build step

---

## §11 Traceability + ⚠️ Drift Log

### §11.1 Brief ↔ FRD ↔ HTML

| Brief § | FRD | HTML anchor |
|---|---|---|
| §2 Route Map | `01_UI §1.1` P-01…P-07 | `TABS[]` (บรรทัด 2040) · `hashchange` handler |
| §3 Layout Shell | `01_UI §1.2` ERP Context | `.sidebar` (`--sidebar-w:232px`) · `.shell-bar` · `.demo-strip` |
| §4 Page Anatomy | `01_UI §1.2` (Components/Actions) | `renderPage()` · `COLS()` (2412) · `statCards()` (2396) |
| §5 Component Inventory | `01_UI §1.2` · `05_RULES §5.4` | function ต่อ component ตามตาราง §5 |
| §6 Overlay Registry | `01_UI §1.0` P-08/P-09/P-10 | `openDrawer()`/`closeDrawer()` (1645/3151) · `openModal()` (3424) · `openOverlay()` (2026) |
| §7 Interaction | `01_UI §1.7` · `06_TESTS` AT-33/AT-34 | Esc handler (1691) · `openPanel()` RAF · `preserveRenderState()` |
| §8 State Matrix | `05_RULES §5.2` (state machine) | `ST` (2076) · `CONSUMERS` (2065) |
| §9 Microcopy | **`06_TESTS §6.10`** (ตารางเดียวกัน) | `showToast()` calls · `e.<field> = '...'` |
| §10 Data Binding | `02_API §2.1–2.2` · `03_LOGIC §3.1` · `04_DB` | mock arrays + function names |
| P-01…P-10 ทุกหน้า | `01_UI §1.1` | ครบทั้ง 10 แถว ✅ |

### §11.2 ⚠️ Drift Log

| # | ชนิด | รายละเอียด | สถานะ |
|---|---|---|---|
| **D-01** | **Microcopy drift (brief ↔ HTML)** | **ปุ่มหลักขั้นสุดท้ายบนจอเขียนว่า `บันทึกและตั้งวันมีผล`** แต่ `PREBRIEF §6` (และ BRD §14.6 ที่ยกมา) เขียนว่า "บันทึก + ตั้งวันมีผล" | **แก้ปลายทางแล้ว** — ตามกติกา anchor (HTML ชนะ) จึงแก้ `3_FRD/01_UI.md` · `3_FRD/06_TESTS.md` · `4_TC/*` ทั้ง 3 ไฟล์ให้ verbatim ตามจอ (regenerate แล้ว 88/348/12 ยังตรงกัน) · **ไม่ใช่ business drift** (ต่างเฉพาะถ้อยคำ ไม่ใช่พฤติกรรม) → ไม่ต้องส่ง `html-to-frd-sync` · เอกสารต้นน้ำ (PREBRIEF/BRD) คงถ้อยคำเชิงธุรกิจไว้ตามเดิม |
| **D-02** | **HTML-only (โดยตั้งใจ)** | `.demo-strip` + `setPersona()` — ตัวสลับ persona สำหรับ demo | **ไม่ใช่ drift ที่ต้องแก้** — เป็นข้อบังคับของ #105 · ระบบจริงไม่มีตัวสลับนี้ (สิทธิ์มาจาก login) · ระบุไว้ที่ `01_UI §1.2` แล้ว |
| **D-03** | **HTML-only (ค่าคงที่ที่ต้องย้าย)** | `OT_MIN` และ `LEAVE_MIN_VAC` เป็นค่าคงที่ในไฟล์ต้นแบบ | **ระบบจริงต้องอ่านจาก `T_hr_legal_minimum`** (BR-05/BR-06 · P-8 · **OQ-10**) — ระบุไว้แล้วที่ `04_DB` และ §10 ของบรีฟนี้ · ต้นแบบเป็นค่าคงที่ได้ (ไม่มี backend) แต่ **ห้ามลอกลงระบบจริง** |
| **D-04** | **FRD-only (ยังไม่มีบนจอ)** | `API-13 GET /hr-config/resolve` · `API-17 GET /hr-config/periods` — เป็นช่องทาง server-to-server ไม่มี UI | **ถูกต้องตามออกแบบ** — ปลายทาง 8 ตัวเรียกโดยไม่ผ่านหน้าจอ (`00_OVERVIEW §0.13`) |
| **D-05** | **FRD-only (ยังไม่มีบนจอ · โดยเจตนา)** | การยิง event SecC 6 ตัว · การเขียน audit · การบังคับสิทธิ์ระดับ API | **ถูกต้อง** — #81/#106 ห้ามศัพท์ engine โผล่บนจอ · CSQ_BRIEF §5 ระบุให้ dev wire ตอนต่อจริง |

> **สรุป Drift:** ไม่มี **business drift** — มีเพียง microcopy 1 รายการ (แก้แล้ว) + 4 รายการที่เป็นความต่างโดยเจตนาระหว่างต้นแบบกับระบบจริง

---

## §12 Diff จากเวอร์ชันก่อน

**— ไม่มีใน feature นี้** (เป็น feature ใหม่ · ไม่มี HTML เวอร์ชันก่อนให้เทียบ)

---

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT — ห้ามนำไป implement โดยไม่ผ่าน BA)

1. **แสดงช่วงมีผลเป็นช่วง (from–to) บนแถว list** — ปัจจุบันแสดงเฉพาะ `วันมีผล` + `เวอร์ชันถัดไป` · การเห็น `effective_to` ตรง ๆ จะช่วยตอนตรวจย้อนหลัง (ต้องระวังไม่ให้คอลัมน์เกิน 8 · #103)
2. **ปุ่ม "เทียบสองเวอร์ชัน" ใน tab ประวัติ** — ตอนนี้เห็น diff เป็นข้อความในไทม์ไลน์ · การเทียบแบบเคียงกันจะช่วยตอนสอบทานนโยบาย
3. **ตัวกรอง "กลุ่มค่า" ใน tab ขอบเขตบริษัท** — tab นี้รวมทุกกลุ่ม การมีตัวกรองกลุ่มจะหาค่าได้เร็วขึ้น (ต้องคุม `.filter-row` ให้ยังเป็นแถวเดียว · #40.1)
4. **แสดงจำนวนงวดที่ยังไม่ปิดบน stat card ของ tab รอบเวลา** — ผูกกับ KPI K-09 (งวดค้างไม่ปิด) ใน BRD §17.3
5. **i18n key ทุก label** — ต้นแบบเป็นไทยล้วน · ระบบจริงต้องผ่าน i18n (ระบุไว้ที่ `01_UI §1.7` แล้ว)

---

## 🔍 UI Brief Verification (Phase 4)

| เกณฑ์ | ผล |
|---|---|
| ทุก route ใน HTML มี section | **7/7 ✅** (§2 + §4) |
| ทุก modal/drawer/popover/toast มีแถวใน Overlay Registry | **6/6 ✅** (drawer create/edit · drawer view · modal 6 ชนิด · combobox menu · toast · tooltip) |
| ทุก `showToast` ปรากฏใน Microcopy verbatim | **15/15 ✅** (§9.1) |
| ทุก component ใน anatomy มี selector/function anchor | **✅** (§5 — 19 component ทุกตัวมี anchor) |
| state matrix ครอบทุกค่า enum ในโค้ด | **✅** — `ST` 6 ค่า · สถานะงวด 2 ค่า · `ready` 2 ค่า · persona 2 ค่า |
| Esc chain ตรงลำดับ handler จริง | **✅** อ้างบรรทัด 1691–1696 + `ssOnKey` |
| z-index map ครบทุกตัวที่ประกาศ | **✅** (§1.3 — 8 ระดับ + `--z-demo:45` ที่ page CSS ประกาศเอง) |
| (FRD) ทุก P-xx มีแถว traceability + Drift Log ไม่เงียบ | **✅** P-01…P-10 ครบ · Drift 5 รายการบันทึกครบ |
| ไม่มีสเปคที่ trace ไม่ได้ (R1) — sample audit 10 จุด | **✅** — สุ่มตรวจ: `--z-demo:45` (page CSS) · `.drawer width min(920px,100vw)` · `STEPS[]` 3 ขั้น · `OUT_TIP` 11 ข้อ · `showToast` default 2800ms · `closeDrawer` setTimeout 280ms · `COLS()` 8 คอลัมน์ · `statCards` 4 ใบ · `CONSUMERS` 8 แถว (ready=true 1) · `OT_MIN` 3 ค่า — **ทุกจุดชี้ตำแหน่งในไฟล์ได้** |

**Verdict: ✅ PASS (FAIL = 0)**

---

## ชุด handoff ให้ dev

| ไฟล์ | บทบาท |
|---|---|
| `1_HTML/ตั้งค่าHR.html` | **source of truth ของหน้าจอ** |
| `3_FRD/` (9 ไฟล์) | สเปกระบบ (UI/API/LOGIC/DB/RULES/TESTS/LOCKED) |
| **`3_FRD/UI_BRIEF_ตั้งค่าHR.md`** (ไฟล์นี้) | design intent + anchor map |
| `4_TC/` (3 ไฟล์) | ชุดทดสอบ (คน / AI) |
| `5_DECLARATIONS/` | CSQ (SecC) + ท่อที่ไม่ต้องประกาศ |
| `2_BRD/` | ที่มาเชิงธุรกิจ + OQ |
