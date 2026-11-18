# UI BRIEF — F-TMP-005 แบบฟอร์มสรุปประเมินความพึงพอใจ (Sale admin) สำหรับลูกค้าในประเทศ (AS-BUILT)

> ใช้คู่: **HTML `feature.html` (source of truth)** + **FRD_F-TMP-005_Pack** + บรีฟนี้ (design intent + แผนที่โค้ด)
> ทุกบรรทัดสกัดจาก HTML — anchor = selector / function / ข้อความจริง · ข้อเสนอที่ไม่ใช่ของจริงอยู่ §13 เท่านั้น

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| HTML | `feature.html` รอบ 1 (kit html-generator-v9.4 · archetype `Q-form` · `__QA__` มี) |
| Gate ของ HTML | audit.sh FAIL 0 (WARN 3 จาก kit) · self_audit PASS · e2e_standard บนเครื่อง user **ยังไม่รัน (NO-BROWSER)** · ตรวจเสริมในคอนเทนเนอร์ 21/21 |
| FRD | `FRD_F-TMP-005_Pack` v1.0 — paired ✅ (frd_lint BLOCK 0 · WARN 0) |
| มติ | DECISIONS.lock 16 ข้อ (AI-DEFAULT 11 · VALID 5) |
| Print | `print/form.tpl.html` + `FM-SAL-21_print-spec.md §2` (thai-doc v2.2 · Replica R9 + R10 2 หน้า) |
| Drift | business drift 0 · HTML-only (prototype) 4 — §11 |
| วันที่ | 2026-10-10 |

## §1 Design Tokens AS-BUILT
| ตัวแปร | ค่า |
|---|---|
| `--c-navy` | `#111111` |
| `--c-navy-2` | `#111111` |
| `--c-primary` | `#FF3B30` |
| `--c-primary-hover` | `#E62E24` |
| `--c-teal` | `#FF9A1F` |
| `--c-teal-light` | `#FFB763` |
| `--c-ink` | `#111111` |
| `--c-mute` | `#54565C` |
| `--c-mute-2` | `#73757B` |
| `--c-mute-3` | `#9A9CA2` |
| `--c-placeholder` | `rgb(180,182,188)` |
| `--z-content` | `1` |
| `--z-sticky` | `10` |
| `--z-shell` | `10` |
| `--z-dropdown` | `30` |
| `--z-backdrop` | `50` |
| `--z-drawer` | `51` |
| `--z-modal` | `60` |
| `--z-popover` | `70` |
| `--z-toast` | `80` |
| `--c-line` | `#DEDAD4` |
| `--c-line-2` | `#E9E5E0` |
| `--c-line-3` | `#F1EEEA` |
| `--c-bg-off` | `#FAF8F5` |
| `--c-success` | `#1F9D55` |
| `--c-warning` | `#E8870F` |
| `--c-danger` | `#E62E24` |
| `--sidebar-w` | `232px` |
| `--shell-h` | `52px` |
| `--fs-h1` | `22px` |
| `--fs-h2` | `17px` |
| `--fs-h3` | `15px` |
| `--fs-body` | `14px` |
| `--fs-sub` | `13px` |
| `--fs-meta` | `12px` |
| `--fs-cap` | `11px` |
| `--fs-kpi` | `28px` |
| `--sp-xs` | `4px` |
| `--sp-sm` | `8px` |
| `--sp-md` | `12px` |
| `--sp-lg` | `20px` |
| `--sp-xl` | `28px` |
| `--r-xs` | `4px` |
| `--r-sm` | `6px` |
| `--r-md` | `8px` |
| `--r-lg` | `12px` |
| `--r-full` | `999px` |

**Font:** Noto Sans Thai + Satoshi (Google Fonts / Fontshare) · **Icons:** Lucide 0.469.0 (multi-CDN loader · `renderIcons()`) · **PDF:** Sarabun

**z-index map (ตามที่ประกาศ):**
| z | ใช้กับ |
|---|---|
| `var(--z-shell)` | `.sidebar` |
| `var(--z-sticky)` | `.shell-bar` |
| `var(--z-dropdown)` | `.user-menu` |
| `var(--z-sticky)` | `.table-wrap thead th` |
| `var(--z-popover)` | `* เมนูที่ portal ออกจาก scroll container (ใช้คู่ portalMenu util) */ .` |
| `var(--z-backdrop)` | `.ss-list` |
| `var(--z-popover)` | `verlay-root ตอนเปิด (หลุด overflow ของ modal/drawer body) */ .ss-list.` |
| `3` | `.table-scroll.is-sticky thead th` |
| `2` | `.stepper-circle` |
| `1` | `.stepper-item:not(:last-child)::after` |
| `var(--z-backdrop)` | `.drawer-backdrop` |
| `var(--z-drawer)` | `.drawer` |
| `var(--z-backdrop)` | `รมีปุ่ม action หลัก */  .modal-backdrop` |
| `var(--z-toast)` | `.toast` |
| `var(--z-sticky)` | `.wizard-footer` |
| `var(--z-dropdown)` | `.info-tip::after` |
| `var(--z-modal)` | `.modal-backdrop` |
| `var(--z-drawer)` | `#drawer` |
| `var(--z-backdrop)` | `#drawerBackdrop` |
| `var(--z-toast)` | `#toast` |
| `var(--z-popover)` | `.row-menu` |

## §2 Route Map
| Route | หน้าที่ | เปิดด้วย | Refresh-safe |
|---|---|---|---|
| `#/csat-domestic-summary` | P-01 รายการ | sidebar `.sb-item` · `closeDrawer()` | ✓ `applyRoute()` |
| `#/csat-domestic-summary/view/:id` | P-03 ดูเอกสาร | `rowClick()` · `openView()` | ✓ เปิด drawer ถ้า `canSee()` — ไม่มีสิทธิ์ = ไม่เปิด |
| `#/csat-domestic-summary/create` | P-02 สร้าง | `startWizard()` | ✓ |
| `#/csat-domestic-summary/edit/:id` | P-02 แก้ร่าง | `startWizard('id')` | ✓ เฉพาะร่างของตน |
route ประกอบจากค่าคงที่ `BASE = 'csat-domestic-summary'` (+ `ROUTES` literal) ผ่าน `go()` · `navigate()` · `getRoute()` · `hashchange → applyRoute()`

## §3 Layout Shell
| ส่วน | Anchor | AS-BUILT |
|---|---|---|
| Sidebar | `.sidebar` · `.sb-module[data-module="sales"]` · `.sb-item` | Sales › สรุปความพึงพอใจ ในประเทศ · badge `#sbBadge` = จำนวนรอฉันพิจารณา |
| Topbar | `.shell-bar` · `.breadcrumb` | Core › Sales › สรุปความพึงพอใจ ในประเทศ · กระดิ่ง `#notifBtn` |
| User chip | `.user-chip` · `#ucAv` (วงกลม icon `.avatar.pc`) · `#userMenu` · `#personaList` | สลับผู้ใช้เดโม `switchPersona()` (prototype-only) |
| Content | `#page-content` | `renderPage()` |

## §4 Page Anatomy
### P-01 รายการ (`renderPage()`)
```
.page-fill
 ├ .ph  (.ph-title · .ph-sub + .ph-badge ≤3: "n รายการ" · "รออนุมัติ n" · "รอฉันพิจารณา n" — ค่า 0 ซ่อน)
 │  └ .ph-actions: ส่งออก CSV (`exportCSV()`) · สร้างใบสรุป `#btnCreate` (`startWizard()` · disabled เมื่อ DOC.active=false)
 └ .card.list-card
    ├ .filter-bar: `#fq` ค้นหา (`onQ()`) · search-select `fst` สถานะ · `fper` เดือน · รีเซ็ต (`resetFilters()`)
    ├ .table-wrap > table.table  (sort `sortTh()`/`sortBy()` · คอลัมน์ระดับต่ำ `lowPill()` · แถว `rowClick()` · ⋮ `openRowMenu()`)
    └ .table-footer (`pager()` · page-size 10/25/50 `setPs()` · `goPage()`)
```
### P-02 Wizard (`renderWizard()` · `.drawer-panel.wide`)
```
.dw-head (eyebrow · .dw-title · `stepper()` 3 ขั้น)
.drawer-body
 ├ ขั้น 1 `wizMain()`: .wz-split
 │   ├ .wz-card ① ประจำเดือน (search-select `wper` → `setPeriod()` · เปลี่ยนเดือน = ล้างคอลัมน์)
 │   ├ .wz-card ② ลูกค้าที่ประเมิน: ปุ่ม `#btnPull` (`pullCols()`) · search-select `wcu` (`addCol()`) · `colRows()` (.cu-row · `removeCol()`) · `matrixView()` (.mx-tbl · `.is-low`)
 │   ├ .wz-card ③ สรุปผลการประเมิน `textarea[name=conclusion]` · ข้อเสนอแนะ `textarea[name=suggestion]` (`setText()` · `.char-cnt`)
 │   └ `sumCard()` (.wz-sum sticky: ผู้สรุป · ผู้รับทราบและอนุมัติ DOA · เดือน · `#sumCust` · `#sumLow`)
 ├ ขั้น 2 `wizAttach()` (.upload-zone · `pickFiles()` · `removeFile()`)
 └ ขั้น 3 `wizReview()` (.review-card ×5 · `matrixView()` · `textBlock()`)
.dw-footer: ย้อนกลับ (`wizBack()`) · ยกเลิก · ถัดไป `#btnNext` (`wizNext()`) / บันทึกแบบร่าง `#btnDraft` (`saveDraft()`) · บันทึกและส่งอนุมัติ `#btnSaveSubmit` (`saveAndSubmit()`)
```
### P-03 View (`renderViewDrawer()` · drawer 920)
```
.dw-head: .doc-ident (eyebrow "ใบสรุปความพึงพอใจ ลูกค้าในประเทศ (Sale admin)" · .dw-title.mono เลขที่ · `docPill()` · .dw-sub เดือน + จำนวนลูกค้า) · .dw-actions ตามสถานะ · พิมพ์/ดาวน์โหลด (`genPdf()`) · ปิด
.drawer-tabs (`tabBtn()`): รายละเอียด `renderDetailTab()` · PDF Preview `renderPdfTab()` · ลายเซ็น / อนุมัติ `renderSignTab()` · ประวัติ `renderHistoryTab()`
.dw-footer: แก้ไขล่าสุด … · ปิด
```

## §5 Component Inventory
| Component | Anchor | States |
|---|---|---|
| Matrix หัวข้อ × ลูกค้า (อ่าน) | `matrixView()` · `.mx-tbl` · `.mx-v` | ปกติ · `.is-low` (ระดับ ≤ 2) · ว่าง "—" · ไม่มีลูกค้า → `.empty-mini` |
| Customer row | `.cu-row` · `colRows()` | ปกติ · `.is-bad` + `.field-error` (ลูกค้าซ้ำ / SDA ถูกยกเลิก) · ป้าย "มีหลายใบ ใช้ใบล่าสุด" · "ระดับต่ำ" |
| Textarea + ตัวนับ | `setText()` · `.char-cnt` | ปกติ · `#fConcl.is-invalid` (สรุปผลว่างตอนถัดไป/ส่ง) |
| Search select | `searchSelectHTML()` · `initSearchSelect()` | เปิด/ปิด · ค้นหา · ล้าง · keyboard |
| Person chip | `empChip()` · `.avatar.pc` | วงกลม icon + role + ชื่อ |
| Sign progress | `renderSignProgress()` · `.sign-prog` · `.sp-bar` | ร่าง "—" · x/y |
| Status pill | `docPill()` | ร่าง · รออนุมัติ · อนุมัติแล้ว · ยกเลิก |
| Low pill | `lowPill()` | "ระดับต่ำ n ช่อง" (pill-warning) · 0 = "—" |
| Empty | `emptyStateHTML()` · `.empty-mini` | list: ไม่มีข้อมูล / ไม่พบรายการที่ค้นหา · wizard: ยังไม่มีลูกค้า |
| Loading | `busyLabel()` · `.spin` | "กำลังบันทึก…" ปุ่ม disabled |

## §6 Overlay Registry
| Overlay | Anchor | ขนาด | เปิด | ปิด / dismiss |
|---|---|---|---|---|
| drawer (view) | `#drawer.drawer-panel` | 920 | `showDrawer()` | ปุ่มปิด · Esc · backdrop **mousedown** (`drawerBackdropDown()`) |
| drawer (wizard) | `#drawer.drawer-panel.wide` | 1290 | `startWizard()` | dirty → modal "ทิ้งข้อมูลที่กรอกไว้?" ก่อนปิด |
| modal | `#modalBackdrop` · `#modal` (`.is-lg` สำหรับส่ง) | 520 / lg | `openModalCfg()` | ปุ่ม · Esc · backdrop mousedown (`modalBackdropDown()` — มีเหตุผล/ความเห็นค้าง = ไม่ปิด) |
| row-menu | `.row-menu` (portal `#overlay-root`) | 180 | `openRowMenu()` | คลิกที่อื่น · scroll (`closeRowMenu()`) |
| user-menu | `#userMenu` | — | `toggleUserMenu()` | คลิกนอก |
| ss-list | search-select list (portal) | ตาม input | focus | เลือก · คลิกนอก · Esc |
| toast | `#toast` | — | `showToast()` | หายเองราว 2.8 วินาที |

## §7 Interaction Spec
- Esc chain (handler ใน BASE-KIT `keydown`): modal → drawer (search-select ปิดก่อนใน `ssOnKey`) · drawer wizard dirty → modal ทิ้งข้อมูล
- Soft update: `setText()` อัปเดตตัวนับ `.char-cnt` และล้าง `#fConcl.is-invalid` โดยไม่ render ใหม่ (focus ไม่หลุด)
- `pullCols()` เติมคอลัมน์จาก SDA ที่บันทึกผลแล้วจนครบ `CFG.max_cols` แล้ว toast จำนวนที่เพิ่ม/ที่เหลือ · `addCol()` บล็อกซ้ำ/เกินด้วย toast
- `openSubmit()` จากหน้าดู: มีคอลัมน์ SDA ถูกยกเลิก → toast · ไม่มีสรุปผล → เปิด wizard ให้แก้
- Render preservation: `render()` ใช้ `preserveRenderState()` / `restoreRenderState()`
- PDF: iframe `.pdf-frame` srcdoc · `fitPdf()` สูงขั้นต่ำ 2 หน้า · ดาวน์โหลด/พิมพ์ผ่าน iframe ซ่อน `.pdf-gen`

## §8 State-Driven UI Matrix
| status | pill | ปุ่มหัว drawer (ผู้ใช้) | เมนู ⋮ |
|---|---|---|---|
| draft | ร่าง (pill-muted) | เจ้าของ: ยกเลิก · แก้ไข · ส่งอนุมัติ | ดูรายละเอียด · แก้ไข (เจ้าของ) · พิมพ์ · ยกเลิกเอกสาร (เจ้าของ/admin) |
| pending | รออนุมัติ (pill-warning) | ผู้พิจารณาขั้นปัจจุบัน: ไม่อนุมัติ · รับทราบและอนุมัติ (`.btn-success`) · เจ้าของ/admin: ยกเลิกเอกสาร | ดูรายละเอียด · พิมพ์ · ยกเลิกเอกสาร |
| approved | อนุมัติแล้ว (pill-success) | — (ล็อก) | ดูรายละเอียด · พิมพ์ |
| cancelled | ยกเลิก (pill-muted) | — | ดูรายละเอียด · พิมพ์ |
draft ที่ถูกไม่อนุมัติ: แบนเนอร์ "ไม่อนุมัติ — กลับเป็นร่าง (เลขเดิม): เหตุผล" · draft ที่มี SDA ถูกยกเลิก: แบนเนอร์เตือน (`viewBanner()` · `staleCols()`)

## §9 Microcopy (verbatim)
### Toast
| ข้อความ | ชนิด |
|---|---|
| ไม่มีการแจ้งเตือนใหม่ | toast |
| แบบเอกสารนี้ยังไม่เปิดใช้งาน | toast |
| แก้ไขได้เฉพาะร่างของตัวเอง | toast |
| เปลี่ยนเดือนแล้ว — ล้างรายชื่อลูกค้าเดิม | toast |
| ลูกค้านี้อยู่ในใบสรุปแล้ว | toast |
| ใบสรุป 1 ใบมีลูกค้าได้สูงสุด ${CFG.max_cols} ราย — ทำใบสรุปเพิ่ม | toast |
| กรุณากรอกข้อมูลให้ครบถ้วน | toast |
| บันทึกร่างแล้ว · | toast |
| มีแบบประเมินที่ถูกยกเลิก — แก้ไขแล้วเอาคอลัมน์นั้นออกก่อนส่ง | toast |
| กรอกลูกค้าและสรุปผลการประเมินให้ครบก่อนส่ง | toast |
| ส่งอนุมัติแล้ว · | toast |
| อนุมัติแล้ว · | toast |
| ส่งออก | toast |
| สลับเป็น | toast |
| แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง | toast |
### ข้อความอื่นในหน้าจอ (สกัดจาก HTML)
- 1. ความรวดเร็วในการตอบคำถาม
- 2. การให้ข้อมูลสินค้า
- 3. การแก้ไขปัญหา (สินค้าเสียหาย)
- 4. ความเหมาะสมในการแก้ปัญหา
- 5. คุณภาพสินค้า
- [Lucide] All CDNs failed. Icons จะไม่แสดง but UI ยังใช้งานได้
- ]); if (canCancel(r)) items.push(['x-circle', 'ยกเลิกเอกสาร',
- ], ['printer', 'พิมพ์',
- showToast('ไม่มีการแจ้งเตือนใหม่','info')
- · อนุมัติแล้ว ล็อกแก้ไข
- · เอกสารจะกลับเป็นร่าง (เลขเดิม) ให้ผู้สรุปแก้แล้วส่งใหม่
- · แจ้งฝ่ายขาย: ระดับต่ำ
- ก.ค.
- ก.พ.
- ก.ย.
- กรกฎาคม
- กรุณากรอกข้อมูลให้ครบถ้วน
- กลับเป็นร่าง (เลขเดิม)
- กันยายน
- กำลังเปิดหน้าต่างพิมพ์ ·
- กำหนดขั้นตอนรับเรื่องสินค้าเสียหายให้ตอบรับภายใน 24 ชั่วโมง
- กุมภาพันธ์
- ขอข้อเสนอแนะเพิ่มเติม
- ขั้นทดสอบ
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลหลักใบสรุป
- ข้าม
- คงมาตรฐานการตอบกลับภายในวันเดียวกัน และแจ้งข้อมูลสินค้าใหม่ให้ลูกค้าล่วงหน้า
- คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
- ควรปรับปรุง
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค่าเริ่มต้นจากสายอนุมัติ (DOA) และผังองค์กร
- ค้นหา...
- ค้นหาเลขที่ / ผู้สรุป / เดือน / ลูกค้า
- จำลอง ดูแลดี
- ชนิดไฟล์ไม่รองรับ
- ช่อง
- ดาวน์โหลด PDF
- ต.ค.
- ตรวจสอบและยืนยัน
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตัวอย่าง บริหารงาน
- ตุลาคม
- ต้อง
- ถึง
- ทดสอบ รักงาน
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ทุกสถานะ
- ทุกเดือน
- ธ.ค.
- ธันวาคม
- ธุรการขาย
- น้อย
- บริษัท ตัวอย่าง จำกัด
- บริหาร
- บันทึกผลแล้ว
- บันทึกร่างแล้ว ·
- ประกอบ ตั้งใจ
- ประจำเดือน
- ประวัติ
- ประวัติ (append-only)
- ปานกลาง
- ปิด
- ผู้จัดการทั่วไป
- ผู้จัดการฝ่ายขาย
- ผู้รับทราบและอนุมัติ
- ผู้รับทราบและอนุมัติ (ค่าเริ่ม)
- ผู้สรุปผล
- ผู้สรุปผลการประเมิน
- ผู้ส่ง
- ฝ่ายขาย
- พ.ค.
- พ.ย.
- พฤศจิกายน
- พฤษภาคม
- พิมพ์
- ภาพรวมดีขึ้นจากเดือนก่อน ลูกค้าพอใจการให้ข้อมูลสินค้ามากขึ้น
- ม.ค.
- มกราคม
- มาก
- มากที่สุด
- มิ.ย.
- มิถุนายน
- มี.ค.
- มีนาคม
- มีแบบประเมินที่ถูกยกเลิก — แก้ไขแล้วเอาคอลัมน์นั้นออกก่อนส่ง
- ยกเลิก
- ยกเลิกเอกสาร
- ยกเลิกเอกสารแล้ว ·
- ยังไม่มีข้อมูล
- ยังไม่มีลูกค้า — ดึงแบบประเมินของเดือนนี้ หรือเพิ่มทีละราย
- ยังไม่มีลูกค้าในใบสรุป
- ยังไม่ส่ง
- ย้อนกลับ
- รอผล
- รอพิจารณา
- รออนุมัติ
- ระดับต่ำ
- ระบบ
- รับทราบและอนุมัติ
- รับทราบและอนุมัติ (ขั้น
- ราย
- รายการ
- รายละเอียด
- รีเซ็ต
- ร่าง
- ลบไฟล์
- ลองปรับคำค้นหรือรีเซ็ตตัวกรอง
- ลายเซ็น / อนุมัติ
- ลำดับการอนุมัติ
- ลูกค้า
- ลูกค้าซ้ำกับคอลัมน์ที่
- ลูกค้าที่ประเมิน
- ลูกค้านี้อยู่ในใบสรุปแล้ว
- ลูกค้ามีแบบประเมิน
- ลูกค้าไม่ครบ
- ลูกค้าไม่ครบ — ขาดลูกค้าที่ตอบแบบประเมินปลายเดือน
- วันที่ ........./........./.........
- วันที่ประเมิน
- ส.ค.
- สถานะ
- สถานะเอกสาร
- สมมติ ใจดี
- สรุปผลไม่สอดคล้องกับคะแนน
- สรุปแบบประเมิน FM-SAL-20 มิ.ย. 2569.xlsx
- สร้าง PDF
- สร้างซ้ำเดือนเดียวกัน
- สร้างซ้ำเดือนเดียวกัน — ใช้ SDS-2569-0002
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างโดย
- สร้างใบสรุป
- สร้างใบสรุปผลการประเมินความพึงพอใจของเดือนแรก
- สลับเป็น
- สาธิต มั่นคง
- สิงหาคม
- ส่งอนุมัติ
- ส่งอนุมัติ?
- ส่งอนุมัติแล้ว ·
- ส่งออก
- ส่งแล้วแก้ไขไม่ได้ — ถ้าไม่อนุมัติ เอกสารจะกลับเป็นร่างเลขเดิมให้แก้แล้วส่งใหม่
- ส่งในระบบ
- ส่งได้ — ระบุแนวทางแก้ไขในข้อเสนอแนะ
- หน่วยงาน
- หัวข้อการแก้ไขปัญหาสินค้าเสียหายยังมีลูกค้าบางรายให้ระดับน้อย ต้องติดตามใกล้ชิด
- อนุมัติ
- อนุมัติแล้ว
- อนุมัติแล้ว ·
- เด้งกลับบน
- เปลี่ยนเดือนแล้ว — ล้างรายชื่อลูกค้าเดิม
- เพิ่มลูกค้าทีละราย
- เพิ่มลูกค้าที่ประเมินอย่างน้อย 1 ราย
- เพิ่มเติม
- เม.ย.
- เมษายน
- เลขที่
- เลขที่เอกสาร
- เลขที่แบบประเมิน
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกตอนส่ง
- เลือกตอนส่งอนุมัติ
- เลือกประเทศ
- เลือกผู้พิจารณา
- เลือกเดือน
- เลือกเดือนก่อน
- เลือกเดือนก่อน แล้วดึงแบบประเมินที่บันทึกผลแล้ว
- เลือกเดือนผิด
- เหตุผลที่ยกเลิก
- เอกสารแนบ
- เอาลูกค้านี้ออก
- แก้ไขร่าง
- แก้ไขล่าสุด
- แก้ไขเอกสาร
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งผู้สรุปว่าต้องแก้อะไร
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบประเมินถูกยกเลิก — เอาออก
- แบบประเมินถูกยกเลิกแล้ว — เอาคอลัมน์นี้ออก
- แบบฟอร์มสรุปประเมินความพึงพอใจ (Sale admin) สำหรับลูกค้าในประเทศ
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- ใบสรุปความพึงพอใจ ลูกค้าในประเทศ
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่มีข้อมูล
- ไม่มีช่องระดับต่ำ
- ไม่มีลูกค้าเหลือ
- ไม่ยกเลิก
- ไม่อนุมัติ
- ไม่อนุมัติ — กลับเป็นร่าง ·
- ไม่ใช้เอกสารนี้แล้ว
- — คุณเป็นผู้พิจารณาเอกสารนี้

## §10 Data Binding & BACKEND anchors
| Prototype | API (02_API) | หมายเหตุ |
|---|---|---|
| `RECS` · `listRows()` · `canSee()` | API-01/02/10 | FN-09 |
| `persist()` (ENG-DOC-NUM ตอนบันทึกครั้งแรก) | API-03/04 | FN-01..03 |
| `SDA` · `sdaFor()` · `custsWithSda()` · `colFromSda()` · `pullCols()` | API-05 | FN-02 · อ่าน F-TMP-004 สถานะ recorded |
| `openSubmit()` · `confirmSubmit()` · `resolveDoa()` · `MOCK_DOA_RESOLVED` (DOA-ENGINE-HOOK) · `DECISION_WORDS` | API-06 | FN-04 |
| `confirmApprove()` · `confirmReason()` | API-07/08 | FN-05/06 · ENG-NOTIFY |
| `docPrintData()` · `pdfLines()` · `tplRender()` · `tplSignRows()` · `DOC_TPL` | API-09 | FN-07 · parity กับ render_doc.py 11/11 |
| `CFG` (topics · scale · low_max · max_cols · text_max) | SalesConfig (อ่าน) | ห้าม hardcode ในระบบจริง |
| `DOC.active` | F-DOCCFG status | |

## §11 Traceability + Drift Log
| Brief | FRD | HTML |
|---|---|---|
| §4 P-01 | 01_UI P-01 · API-01/10 | `renderPage()` |
| §4 P-02 | 01_UI P-02 · API-03/04/05 | `renderWizard()` |
| §4 P-03 | 01_UI P-03 · API-02/06..09 | `renderViewDrawer()` |
| §6 modal | 01_UI M-01..05 · 05 VR-06/07 | `renderModal()` |
| §5 matrix | 05 BR-01..06 | `matrixView()` · `lowCount()` |
**Drift Log:** business 0 · HTML-only (prototype-only ไม่ต้องสร้าง): `window.__QA__` · `switchPersona()` สลับผู้ใช้ · `S.sim` / `commitRejected()` จำลอง API ล้ม · `SDA` mock seed (ระบบจริงใช้ API-05)

## §12 Diff จากเวอร์ชันก่อน
— ไม่มี (รอบแรก)

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- กันสร้างซ้ำเดือน (OQ-06) · ปุ่ม "สร้างใบสรุปต่อ" เมื่อลูกค้าเกิน 12 ราย · กราฟแนวโน้มระดับต่อหัวข้อ 12 เดือนใน Report area
