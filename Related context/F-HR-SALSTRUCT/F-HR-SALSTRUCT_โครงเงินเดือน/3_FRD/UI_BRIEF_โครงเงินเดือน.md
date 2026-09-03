# UI BRIEF (AS-BUILT) — โครงเงินเดือน · `F-HR-SALSTRUCT`

> **AS-BUILT** — เอกสารนี้บันทึก "สิ่งที่อยู่ในไฟล์จริง" ไม่ใช่สิ่งที่ควรจะเป็น · ข้อเสนอทุกอย่างถูกกันไว้ที่ §13 เท่านั้น
> ผลิตโดย `html-ui-brief` (S7 ของ feature-lane-runner v2.3) จาก `1_HTML/โครงเงินเดือน.html`

## §0 Document Control + Pairing

| | |
|---|---|
| HTML | `output/2026-08-28/F-HR-SALSTRUCT_โครงเงินเดือน/1_HTML/โครงเงินเดือน.html` · 4,249 บรรทัด · 277,072 bytes · md5 `1980d75c6ce095a2c63598d1662ff10b` |
| Generator | `html-generator-v9` Pipeline Mode (PREBRIEF-as-pack) · archetype **master/config (A+B+C)** |
| Gate ที่ผ่านแล้ว | `audit.sh` FAIL=0 · `qc-ux-html-checker` BLOCK=0 (WARN 3 ที่อยู่ใน BASE-KIT) · `qc-coverage-checker` R1 65/65 FN · R2 BLOCK=0 |
| FRD ที่ pair | `3_FRD/` (00_OVERVIEW · 01_UI · 02_API · 03_LOGIC · 04_DB · 05_RULES · 06_TESTS · 07_LOCKED_DECISIONS · INDEX) — **pair ครบทุกหน้า** |
| สถานะ drift | **ไม่มี business drift** · มี 3 รายการเชิงถ้อยคำ/รายละเอียดที่บันทึกไว้ใน §11 |
| CI | Warm Light (Ivory / Charcoal / Red / Orange / Green) — ไม่มีสีน้ำเงินหรือม่วงหลุดเข้ามา |

## §1 Design Tokens AS-BUILT

**สี (ค่าจริงในไฟล์)**

| token | ค่า | ใช้กับ |
|---|---|---|
| `--c-navy` / `--c-navy-2` / `--c-ink` | `#111111` | ตัวอักษรหลัก · sidebar |
| `--c-primary` | `#FF3B30` | ปุ่มหลัก · จุดเน้น |
| `--c-primary-hover` | `#E62E24` | สถานะ hover ของปุ่มหลัก |
| `--c-teal` / `--c-teal-light` | `#FF9A1F` / `#FFB763` | จุดเน้นรอง (โทนส้ม) |
| `--c-mute` / `--c-mute-2` / `--c-mute-3` | `#54565C` / `#73757B` / `#9A9CA2` | ข้อความรอง 3 ระดับ |
| `--c-line` / `--c-line-2` / `--c-line-3` | `#DEDAD4` / `#E9E5E0` / `#F1EEEA` | เส้นขอบ 3 ระดับ |
| `--c-bg-off` | `#FAF8F5` | พื้นหลังรอง (ivory) |
| `--c-success` / `--c-warning` / `--c-danger` | `#1F9D55` / `#E8870F` / `#E62E24` | pill + note |

**ตัวอักษร:** `'Satoshi', 'Noto Sans Thai', system-ui, sans-serif` (heading ใช้ Satoshi · ข้อความไทยใช้ Noto Sans Thai) — **ไม่มีฟอนต์อื่น**
**ขนาดตัวอักษร:** `--fs-h1 22` · `--fs-h2 17` · `--fs-h3 15` · `--fs-body 14` · `--fs-sub 13` · `--fs-meta 12` · `--fs-cap 11` · `--fs-kpi 28`
**ระยะห่าง:** `--sp-xs 4` · `--sp-sm 8` · `--sp-md 12` · `--sp-lg 20` · `--sp-xl 28`
**มุมโค้ง:** `--r-xs 4` · `--r-sm 6` · `--r-md 8` · `--r-lg 12` · `--r-full 999`
**โครงร่าง:** `--sidebar-w 232px` · `--shell-h 52px`
**ชั้นซ้อน (z):** ใช้ token ของ kit ทั้งหมด — `--z-sticky` · `--z-shell` · `--z-dropdown` · `--z-backdrop` · `--z-drawer` · `--z-toast` · `--z-tooltip (60)` · `--z-demo (45)` — **ไม่มีการเขียนตัวเลข z-index ทับ token**

## §2 Route Map

| route | หน้า | refresh-safe | default |
|---|---|---|---|
| `#/salary-structure/grade` | ระดับ / กระบอกเงินเดือน | ✅ | ✅ (default เมื่อไม่มี hash) |
| `#/salary-structure/component` | องค์ประกอบค่าจ้าง | ✅ | — |
| `#/salary-structure/rate` | อัตราพนักงาน | ✅ | — |
| `#/salary-structure/recurring` | รายการประจำ | ✅ | — |
| `#/salary-structure/usage` | ทะเบียนการใช้งาน | ✅ | — |

ตัวจัดการเส้นทาง: `getRoute()` → `navigate()` → `actualRender()` · การสลับ tab ใช้ `goTab()` (เขียน hash ใหม่ ไม่ใช่ซ่อน/แสดง) → **รีเฟรชแล้วอยู่ที่เดิมทุกหน้า**
**1 feature = 1 เมนูซ้าย (#104):** sidebar มีรายการเดียวคือ "โครงเงินเดือน" · 5 หน้าเป็น `.tabs.page-tabs` ภายในหน้าเดียว

## §3 Layout Shell
- Sidebar กว้าง `232px` (charcoal) · แถบบน `52px` · breadcrumb + ชื่อหน้าอยู่บรรทัดเดียว
- `.demo-strip` อยู่ **ล่างซ้าย** (z = 45) — เป็นที่เดียวที่มีตัวสลับบทบาท (`demoInHeader = false` ทุก route ตาม `RENDER.json`)
- `body { min-width: 768px }` · `bodyScrollX = false` ทุก route (ตาราง P-03 ที่กว้าง 1120px scroll ภายใน `.table-wrap` ไม่ใช่ที่ body)

## §4 Page Anatomy (โครงเดียวใช้ทั้ง 5 tab)

```
page
├── page-header (ชื่อหน้า + ⓘ tip ขอบเขต + ปุ่มหลักของ tab)      ← ไม่มีตัวสลับบทบาท (#105)
├── stat cards (เฉพาะ tab ที่มีตัวเลขสรุป: grade / rate)          ← คลิกเพื่อกรองได้
├── filter-row (แถวเดียว 52px)                                    ← ค้นหา + ตัวกรอง + "มีผล ณ วันที่" + ล้างตัวกรอง
├── list-card > table-wrap > table (แถว ≤52px)                     ← .tbl-person inline สำหรับคอลัมน์คน
└── overlay-root
    ├── drawer (wizard 3 ขั้น / view drawer แบบ tab)
    └── modal (ยืนยัน + บังคับเหตุผล)
```
`#/salary-structure/usage` ต่างจาก 4 tab แรก: เป็น **workspace 6 ส่วน (SEC)** ไม่มีตาราง จึงไม่มี filter-row

| tab | ตัวนับด้านบน | คอลัมน์หลัก |
|---|---|---|
| grade | จำนวนระดับที่ใช้งาน · เวอร์ชันรอมีผล · พนักงานนอกกระบอก | รหัส · ชื่อ · ลำดับชั้น · ขอบเขตบริษัท · min/mid/max · พนักงานที่อ้าง · สถานะ |
| component | — | รหัส · ชื่อ · ประเภท · วิธีคิด · ความถี่ · รหัสส่งจ่ายเงิน · แฟล็ก · สถานะ |
| rate | มีอัตรา · ยังไม่กำหนดอัตรา · นอกกระบอก · รอมีผล · compa-ratio เฉลี่ย | พนักงาน · แผนก · ระดับ · เงินเดือนฐาน · ตำแหน่งในกระบอก · compa-ratio · วันมีผล · สถานะ |
| recurring | — | พนักงาน · องค์ประกอบ · ประเภท · จำนวน · ช่วงวัน · ยอดสะสม/เป้า · สถานะ |
| usage | — | (6 SEC — ดู §4.1) |

### §4.1 SEC ของหน้า "ทะเบียนการใช้งาน"
1. ค่าที่อ่านจากตั้งค่า HR (พร้อม `cfgQueryString()` + `version_id` + เวลาที่ดึง + ปุ่มจัดการ)
2. งวดจ่ายและงวดที่ปิดแล้ว (+ ปุ่มรับสัญญาณปิดงวด)
3. อัตราที่รอมีผลจากคำสั่งเปลี่ยนแปลงพนักงาน (`MV-2026-0148` · `MV-2026-0151`)
4. feature ที่อ่านโครงนี้ไปใช้ (`F-HR-PAYROLL` · `F-HR-MANPOWER` · `F-HR-CERT` · `F-HR-MOVEMENT` + `F-HR-ESS` อ่านผ่านต้นทาง)
5. งานที่ไม่ได้ทำที่นี่ (6 แถว ชี้ feature เจ้าของ)
6. บันทึกการใช้งานข้อมูลค่าจ้าง (audit ย่อ · เพิ่มอย่างเดียว)

## §5 Component Inventory

| component | anchor / ตัวช่วยในไฟล์ | สถานะที่รองรับ | หมายเหตุ |
|---|---|---|---|
| ตารางรายการ | `cellHTML()` · `COLS()` · `gradeRows()` / `componentRows()` / `currentRows()` | ปกติ · ว่าง (`emptyFor()` / `emptyStateHTML()`) · กรองแล้วไม่พบ | แถวสูงสุดวัดจริง 47.1–50.2px |
| แถบตัวกรอง | `filterRow()` | มีค่า / ล้างแล้ว | แถวเดียว 52px ทุก tab ที่มีตาราง |
| combobox master | `initSearchSelect()` · `COMBO()` · `comboPerson()` · `empOptions()` / `gradeOptions()` / `componentOptions()` / `companyOptions()` | ปกติ · ค้นหา · ไม่พบ · ปิดใช้(ซ่อนจากตัวเลือก) | 11 ตัว · option คน = avatar → ชื่อ → ตำแหน่ง · แผนก (#102) · `select_big = 0` |
| wizard (ฟอร์มหลายขั้น) | `gotoStep()` · `validateStep()` · `submitForm()` · `finishSave()` | ขั้น 1–3 · error รายช่อง (`clearFieldError`) · กำลังบันทึก | 4 ชุด (grade · component · rate · recurring) ปิดท้ายด้วย "ตรวจสอบและยืนยัน" |
| view drawer แบบ tab | `dwTabs()` · `.drawer-header.has-tabs` | ต่อ tab | grade 3 tab · component 2 tab · rate 3 tab · recurring 2 tab |
| แถบตำแหน่งในกระบอก | `bandBarHTML()` (ในตาราง) · `bandFullHTML()` (ใน drawer) | มีกระบอก / ไม่มีกระบอก (แสดง "—") | ไม่ทำให้แถวสูงเกิน 52px |
| ค่าที่ปิดบัง | `money(v, empId)` → `.msk` | เห็นเต็ม / ปิดบัง | ความกว้างคงที่ ตารางไม่กระโดด |
| pill สถานะ | `ST{}` (10 สถานะ) | ดู §8 | สูง 22px คำเดียวทุกตัว (#38.1) |
| note (เตือน/ผิดพลาด) | `errNote()` · `.note note-warn` | เตือน / บล็อก | ทุกอันมีปุ่มหรือทางออก — **ไม่ใช่ hint banner** (#106) |
| ⓘ tip | `.tip` (`PAYCODE_TIP` · `BAND_TIP` · `OUT_TIP`) | hover | ใช้แทน banner อธิบายระบบ |
| stat card | KPI kit | ปกติ · คลิกเพื่อกรอง | label 12 / value 22 |

## §6 Overlay Registry

| overlay | ขนาด | ปิดอย่างไร | z |
|---|---|---|---|
| drawer (wizard/view) | `min(920px, 100vw)` · `.standard` = `min(680px, 100vw)` · `.wide` = `min(1290px,100vw)` | ปุ่มปิด · Esc · คลิกนอก (เมื่อไม่ได้กำลังบันทึก) | `--z-drawer` |
| modal ยืนยัน | ขนาด kit (`mHead()` / `mReason()` / `mFoot()`) | ปุ่มยกเลิก · Esc | เหนือ drawer |
| dropdown ของ combobox | ลอยจาก portal (`portal_menu = true`) | เลือก · Esc · คลิกนอก | `--z-dropdown` |
| toast | มุมจอ (`showToast(message, variant, durationMs=2800)`) | หมดเวลาเอง | `--z-toast` |
| demo strip | แถบล่างซ้าย | ค้างไว้เสมอ (เป็นเครื่องมือทดสอบ) | `--z-demo` = 45 |

**modal ที่บังคับเหตุผล 8 จุด:** ถอนเวอร์ชัน · ปิดใช้ระดับ · เปิดใช้ระดับกลับ · ปิดใช้องค์ประกอบ · เปิดใช้องค์ประกอบกลับ · ถอนอัตรา · ปิดช่วงอัตรา · ถอนรายการประจำ (`askModal()` + `needReason()`)

## §7 Interaction Spec
- **Esc chain:** modal → drawer → dropdown (มี `escape_handler` เดียวจัดลำดับ)
- **คลิกนอก:** ปิด dropdown เสมอ · ปิด drawer เฉพาะเมื่อไม่ได้อยู่ระหว่างบันทึก (`state.drawer.busy`)
- **overlay ลอยไม่ดันเนื้อหา** (`overlay_root = true`) — เลื่อนหน้าไม่ขยับตอนเปิด/ปิด
- **การกรอง/เรียง render เฉพาะตาราง** ไม่ re-render ทั้งหน้า
- **กันกดซ้ำ:** `state.drawer.busy` + `is-disabled` + `loader-2 spin` + ข้อความ "กำลังบันทึก…"
- **as-of viewer:** ช่อง "มีผล ณ วันที่" (`asOfDate()`) มีผลกับทั้งตารางและค่าที่คำนวณ (`bandAt()` · `curRec()` · `gradeStatus()`)
- **ตารางกว้างเกินจอ (tab อัตราพนักงาน):** scroll ภายใน `.table-wrap` — body ไม่ scroll แนวนอน

## §8 State-Driven UI Matrix (จาก `ST{}` ในไฟล์ — 10 สถานะ)

| key | ป้ายบนจอ | คลาส pill | ใช้กับ |
|---|---|---|---|
| `draft` | ร่าง | `pill-muted` | เวอร์ชันกระบอก/องค์ประกอบ |
| `scheduled` | รอมีผล | `pill-warning` | เวอร์ชัน · อัตรา · รายการประจำ |
| `active` | ใช้งาน | `pill-success` | เวอร์ชัน · รายการประจำ |
| `current` | ปัจจุบัน | `pill-success` | อัตรารายคน |
| `superseded` | ถูกแทน | `pill-muted` | เวอร์ชัน |
| `history` | ประวัติ | `pill-muted` | อัตรารายคน |
| `cancelled` | ถอนแล้ว | `pill-muted` | ทุกวัตถุ |
| `inactive` | ปิดใช้ | `pill-danger` | ระดับ · องค์ประกอบ |
| `ended` | สิ้นสุด | `pill-muted` | อัตรา · รายการประจำ |
| `unassigned` | ยังไม่กำหนด | `pill-warning` | พนักงานที่ยังไม่มีอัตรา |

**ปุ่มที่โผล่ตามสถานะ:** `รอมีผล` → ถอน · `ใช้งาน` → สร้างเวอร์ชันใหม่ / ปิดใช้ · `ปิดใช้` → เปิดใช้กลับ · `ปัจจุบัน` → บันทึกอัตราใหม่ / ปิดช่วงอัตรา · `ประวัติ` → ไม่มีปุ่มใด (append-only)

## §9 Microcopy (verbatim — คัดจากโค้ดตรงตัว)

**ปุ่ม:** `สร้างเวอร์ชันใหม่` · `สร้างเวอร์ชันใหม่ของกระบอก` · `ผูกอัตราพนักงาน` · `บันทึกอัตราใหม่` · `ถอนเวอร์ชันที่รอมีผล` · `ถอนอัตราที่รอมีผล` · `ถอนรายการ` · `ปิดใช้` · `ปิดใช้ระดับ` · `ปิดใช้องค์ประกอบ` · `ปิดช่วงอัตราเมื่อพ้นสภาพ` · `เปิดใช้กลับ` · `เปิดใช้ระดับกลับ` · `ดูประวัติเวอร์ชัน` · `ดูประวัติอัตรา` · `ดูอัตราค่าจ้าง` · `จัดการที่ตั้งค่า HR`

**toast:**
- `ล้างตัวกรองแล้ว`
- `บันทึกองค์ประกอบค่าจ้างแล้ว`
- `บันทึกรายการประจำแล้ว`
- `เปิดใช้องค์ประกอบกลับแล้ว`
- `ตั้งวันมีผลเป็นวันที่เร็วที่สุดที่ทำได้แล้ว` · `ตั้งวันเริ่มมีผลเป็นวันที่เร็วที่สุดที่ทำได้แล้ว`
- `ล้างค่าที่ดึงไว้และถามค่าจากตั้งค่า HR ใหม่แล้ว · งวดที่ปิดถูกกันวันมีผลทันที`
- `ลงทะเบียนการใช้งานค่านโยบายกับตั้งค่า HR แล้ว`
- `ตั้งสถานะเชื่อมกับ … เองแล้ว` / `ยกเลิกสถานะเชื่อม…`
- `เปิดหน้าตั้งค่า HR เพื่อจัดการค่า “…” — ค่านโยบายทั้งหมดถูกจัดการที่นั่น`
- `“…” อยู่นอกขอบเขตต้นแบบรอบนี้`
- `บทบาทนี้ดูได้อย่างเดียว` / `บทบาทนี้ดูได้อย่างเดียว ไม่สามารถแก้ไขโครงเงินเดือนได้`
- `สลับเป็น HR Comp Admin — เห็นตัวเลขทุกคนและแก้ไขได้`

**note / error:**
- `กระบอกที่มีผลอยู่แก้ค่าตรงไม่ได้ ต้องสร้างเวอร์ชันใหม่พร้อมวันมีผล`
- `การอ้างอิงวนกลับมาที่ตัวเอง: X-PCT → Y-PCT → X-PCT`
- `… ปิดแล้ว ตั้งวันมีผลย้อนเข้างวดนี้ไม่ได้ · ตั้งได้ตั้งแต่ …`
- `… ปิดแล้ว ตั้งวันเริ่มมีผลย้อนเข้างวดนี้ไม่ได้`
- `… ปิดแล้วให้ตั้งวันมีผลข้างหน้าแทน`
- `… ของกระบอก บันทึกได้แต่ต้องกรอกเหตุผลนอกกระบอก`
- `ต่ำกว่าค่าแรงขั้นต่ำตามกฎหมายที่อ่านจากตั้งค่า HR ต้องกรอกเหตุผลก่อนบันทึก`
- `ต่ำกว่าค่าแรงขั้นต่ำตามกฎหมายที่อ่านจากตั้งค่า HR ต้องยืนยันพร้อมเหตุผลก่อนบันทึก`
- `ยังไม่ได้ตั้งค่าขั้นต่ำที่ตั้งค่า HR`
- `รหัสระดับนี้มีอยู่แล้ว` · `รหัสองค์ประกอบนี้มีอยู่แล้ว`

**hint ในกรอบ:** `อัตราเดิมกลายเป็นประวัติ แก้หรือลบไม่ได้` · `เวอร์ชันเดิมยังอยู่ครบ · ไม่มีขั้นอนุมัติ` · `ไม่แตะอัตราของพนักงาน` · `ไม่ใช่ยอดจ่ายสุทธิ การหักภาษีและประกันสังคมทำที่ระบบเงินเดือน`
**empty state:** `ยังไม่มีกระบอกที่มีผล ณ วันที่นี้` · `ยังไม่มีการเปิดดูที่ถูกบันทึกในรอบนี้` (รวม `emptyStateHTML` 17 จุด)
**ตัวเลือกประเภทการเปลี่ยน (`CHANGE_REASONS`):** `ปรับประจำปี` · `เลื่อนตำแหน่ง` · `ปรับกลางปี` · `รับโอน/ปรับโครงสร้าง` · `แก้ไขข้อผิดพลาด`

## §10 Data Binding & จุดต่อระบบจริง

| จุดในจอ | ตัวช่วยในไฟล์ (mock) | ต่อกับอะไรจริง (FRD) |
|---|---|---|
| ตารางระดับ/กระบอก | `gradeRows()` · `bandAt()` · `bandVer()` | `GET /grades` (API-01) · `resolveBandAt` |
| สร้าง/ประกาศเวอร์ชัน | `draftBand()` · `applyPct()` · `doSave()` | `POST /grades` (API-02) → `publish` (API-04) |
| ถอน/ปิดใช้/เปิดใช้กลับ | `doWithdrawBand()` · `doDeactivateGrade()` · `doReactivateGrade()` | API-05 / API-06 / API-07 |
| เทียบเวอร์ชัน | `renderDiffDrawer()` | `GET /grades/diff` (API-09) |
| ทะเบียนองค์ประกอบ | `componentRows()` · `cycleOf()` | API-10 / API-11 (+ `detectComponentCycle`) |
| อัตราพนักงาน | `currentRows()` · `curRec()` · `recState()` | `GET /rates` (API-13) · `resolveCurrentRate` |
| ตำแหน่งในกระบอก | `compaRatio()` · `fteAdj()` · `bandBase()` · `bandBarHTML()` | **ENG-SALBAND-01** (ผ่าน API-13 / API-24) |
| เตือนนอกกระบอก | `outBandPreview()` · `needReason()` | `evaluateOutOfRange` (API-14) |
| เตือนต่ำกว่ากฎหมาย | `legalMin()` → `resolveCfg('legal_minimum','wage.monthly_min')` → `belowLegal()` | `resolveLegalMinimum` + `evaluateBelowLegalMin` (P-8) |
| งวดที่ปิด | `closedPeriodOf()` · `earliestAllowed()` | `assertNotInClosedPeriod` + `earliestOpenDate` (P-7) |
| ค่าจากตั้งค่า HR | `HRCFG.items` · `resolveCfg()` · `cfgQueryString()` · `refreshCfg()` | `GET /api/v1/hr-config/resolve` (C-1…C-3) · `T_ss_cfg_ref` |
| รายการประจำ | `cellRecur()` · `recurState()` | API-18 / API-19 · **ENG-RECUR-01** |
| ปิดบังตัวเลข | `money(v, empId)` · `.msk` | `maskMoney` → **ENG-MASK-01** (Policy Center) |
| บันทึกการเปิดดู | `logAudit('เปิดดูอัตราค่าจ้างรายบุคคล', …)` ใน `openRateView()` | `logRestrictedView` → audit + event `salcomp.viewed_restricted` |
| ทะเบียน consumer | `toggleLink()` · รายการ `F-HR-*` | API-21 / API-22 / API-27 |

**ชุด mock ที่ต้องเปลี่ยนเป็นข้อมูลจริงตอนต่อระบบ:** พนักงาน 8 คน (สมชาย · ปรียา · วิชัย · มณีรัตน์ · ธนกร · กิตติ · ชูใจ · อรุณี) · โครง `SS-2025/2026/2027` · องค์ประกอบ 4 ตัว + คู่ทดสอบอ้างวน · งวด 2026-07 (ปิด) / 2026-08 (เปิด) · เลขที่คำสั่ง `MV-2026-0148` / `MV-2026-0151`

## §11 Traceability + ⚠️ Drift Log

| หน้าในจอ | route | FRD `01_UI` | FRD API | สถานะ |
|---|---|---|---|---|
| ระดับ / กระบอกเงินเดือน | `#/salary-structure/grade` | P-01 | API-01…API-08 | ✅ ตรงกัน |
| องค์ประกอบค่าจ้าง | `#/salary-structure/component` | P-02 | API-10…API-12 | ✅ |
| อัตราพนักงาน | `#/salary-structure/rate` | P-03 | API-13…API-17 | ✅ |
| รายการประจำ | `#/salary-structure/recurring` | P-04 | API-18…API-20 | ✅ |
| ทะเบียนการใช้งาน | `#/salary-structure/usage` | P-05 | API-21…API-23 · API-27 | ✅ |
| เทียบเวอร์ชัน (drawer) | ปุ่มใน P-01 | P-06 | API-09 | ✅ |

### ⚠️ Drift Log

| # | ชนิด | รายละเอียด | ผลกระทบ | ข้อเสนอ |
|---|---|---|---|---|
| D-01 | **FRD-only** (ไม่ใช่ drift ธุรกิจ) | `02_API` มี **API-24 `/resolve`** · **API-25 `/bands/resolve`** · **API-26 `/rates/from-movement`** · **API-27 `/usage`** ที่ **ไม่มีหน้าจอ** — เป็นสัญญาการอ่าน/เขียนของ consumer (`00_OVERVIEW §0.13`) | ไม่กระทบจอ · ตั้งใจให้เป็น service contract | คงไว้ · ในจอมีการ์ดอธิบายในหน้าทะเบียนการใช้งานแล้ว (P-05 SEC 4) |
| D-02 | **ถ้อยคำ** | ป้ายสถานะในจอใช้คำสั้น `ถูกแทน` / `ยังไม่กำหนด` ส่วนเอกสาร BRD/FRD เขียนเต็มว่า "ถูกแทนที่" / "ยังไม่กำหนดอัตรา" | ไม่กระทบพฤติกรรม (คำเดียวกัน · ตัดให้พอดี pill 22px) | **บันทึกเป็น drift ถ้อยคำ** · `06_TESTS §6.10` ใช้ข้อความจากจอเป็น expected แล้ว |
| D-03 | **รายละเอียดจอที่เอกสารไม่ได้ระบุ** | ตารางหน้าอัตราพนักงานถูกล็อกกว้าง 1120px แล้ว scroll ภายใน `.table-wrap` (แก้จาก Pass G-b) | ทำให้แถวคุมที่ ≤52px ได้ที่ viewport 1024 | บันทึกไว้แล้วใน `01_UI §1.0` ช่อง Deviation · ไม่ต้องแก้ทั้งสองฝั่ง |

**ไม่มี HTML-only ที่เป็น business** (ไม่มีความสามารถบนจอที่ FRD ไม่ได้เขียนถึง) · **ไม่มี FRD-only ที่เป็นหน้าจอหาย**

## §12 Diff จากเวอร์ชันก่อน
ไม่มี — นี่เป็นเวอร์ชันแรกของ feature (งานประเภท new · ไม่มี artifact เดิม)
ระหว่างรอบ S3b มีการแก้ 2 จุดที่บันทึกไว้แล้ว: G-a รวมบรรทัดรองในคอลัมน์ระดับ · G-b ล็อกความกว้างตาราง (ดู `UX_CHECK_REPORT` Pass G)

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT — ห้ามนำไป implement โดยไม่ผ่าน BA)
1. ตอนต่อระบบจริง ควรเพิ่ม **ตัวบอกเวลาที่ดึงค่าจากตั้งค่า HR ล่าสุด** ไว้ที่หัวหน้าอัตราพนักงานด้วย (ตอนนี้อยู่เฉพาะหน้าทะเบียนการใช้งาน) — ช่วยเรื่อง EC-20
2. เมื่อ **OQ-SS-01** เคาะว่าจะเปลี่ยนนอกกระบอกเป็น "บล็อก" ต้องเพิ่มสถานะปุ่มใหม่ในจอ (ตอนนี้ทางเดียวคือเตือน + บังคับเหตุผล)
3. ถ้าจำนวนพนักงานเกินหลักพัน แนะนำเพิ่ม **การเลือกหลายแถวเพื่อดูอย่างเดียว** (ไม่ใช่แก้หมู่ ซึ่งอยู่นอกขอบเขต) เพื่อให้ HR ตรวจรายการนอกกระบอกได้เร็วขึ้น
4. เมื่อมีเครื่องที่มี Chromium ให้ถ่ายภาพตาม `_lane/TC_work/shot-spec.json` (30 จุด) แล้ว build เอกสาร QA ใหม่

---

## 🔍 UI Brief Verification (Phase 4)

- [x] ทุก route ในไฟล์มีใน §2 (5/5) · refresh-safe ทุกเส้น
- [x] ทุกหน้ามี anatomy + component + overlay ที่อ้างของจริงในไฟล์ (§4–§6)
- [x] ทุก component มีสถานะครบ (§5) · pill ครบ 10 สถานะจาก `ST{}` (§8)
- [x] Microcopy คัดมา verbatim ไม่แต่งใหม่ (§9)
- [x] Data binding ชี้จุด plug จริงทุกจุด (§10)
- [x] ทุก P-xx มีแถว traceability + **Drift Log ไม่เงียบ** (§11 · 3 รายการ)
- [x] ข้อเสนออยู่ใน §13 เท่านั้น — ไม่ปนกับ AS-BUILT
- [x] ไม่มีการอ่านไฟล์ HTML ทั้งไฟล์เข้ามาเขียน (ใช้ grep เจาะเฉพาะจุดตามกติกาเลน)

## ชุด handoff ให้ dev
`01_UI.md` (spec + Layout Decision Log) → **ไฟล์นี้** (AS-BUILT ของจอจริง) → `02_API.md` + `03_LOGIC.md` (จุดต่อ) → `06_TESTS.md §6.10` (ข้อความที่ QA จะเทียบ)
