# UI BRIEF — F-TMP-003 ฟอร์มแจ้งงานขนส่งนอก (AS-BUILT)

> ใช้คู่: **HTML `feature.html` (source of truth)** + **FRD_F-TMP-003_Pack** + บรีฟนี้ (design intent + แผนที่โค้ด)
> ทุกบรรทัดสกัดจาก HTML — anchor = selector / function / ข้อความจริง · ข้อเสนอที่ไม่ใช่ของจริงอยู่ §13 เท่านั้น

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| HTML | `feature.html` รอบ 1 (kit html-generator-v9.4 · archetype `Q-form` · `__QA__` มี) |
| Gate ของ HTML | audit.sh FAIL 0 (WARN 3 จาก kit) · self_audit PASS · e2e_standard **ไม่ได้รันบนเครื่อง user (NO-BROWSER)** — ตรวจเสริมในคอนเทนเนอร์ 21/21 |
| FRD | `FRD_F-TMP-003_Pack` v1.0 — paired ✅ (frd_lint BLOCK 0 · WARN 0) |
| มติ | DECISIONS.lock 15 ข้อ (AI-DEFAULT 10 · VALID 5) |
| Print | `print/form.tpl.html` + `print/FM-SAL-16_print-spec.md` (thai-doc v2.2 · Replica R9 · 1 หน้า) |
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
| `var(--z-portal)` | `.bd-pop` |

## §2 Route Map
| Route | หน้าที่ | เปิดด้วย | Refresh-safe |
|---|---|---|---|
| `#/outsourced-transport` | P-01 รายการ | sidebar `.sb-item` · `closeDrawer()` | ✓ `applyRoute()` |
| `#/outsourced-transport/view/:id` | P-03 ดูเอกสาร | `rowClick()` · `openView()` | ✓ เปิด drawer ถ้า `canSee()` — ไม่มีสิทธิ์ = ไม่เปิด |
| `#/outsourced-transport/create` | P-02 สร้าง | `startWizard()` | ✓ |
| `#/outsourced-transport/edit/:id` | P-02 แก้ร่าง | `startWizard('id')` | ✓ เฉพาะร่างของตน |
route ประกาศใน `ROUTES` (literal) · เปลี่ยนผ่าน `go()` · `navigate()` · `getRoute()` · `hashchange → applyRoute()`

## §3 Layout Shell
| ส่วน | Anchor | AS-BUILT |
|---|---|---|
| Sidebar | `.sidebar` · `.sb-module[data-module="sales"]` · `.sb-item` | Sales › แจ้งงานขนส่งนอก · badge `#sbBadge` = ร่างของฉัน |
| Topbar | `.shell-bar` · `.breadcrumb` | Core › Sales › ฟอร์มแจ้งงานขนส่งนอก · กระดิ่ง `#notifBtn` |
| User chip | `.user-chip` · `#ucAv` (วงกลม icon `.avatar.is-person`) · `#userMenu` · `#personaList` | สลับผู้ใช้เดโม `switchPersona()` (prototype-only) |
| Content | `#page-content` | `renderPage()` |

## §4 Page Anatomy
### P-01 รายการ (`renderPage()`)
```
.page-fill
 ├ .ph  (.ph-title · .ph-sub + .ph-badge "n รายการ · ร่าง n")
 │  └ .ph-actions: ส่งออก CSV (`exportCSV()`) · สร้างใบแจ้งงาน `#btnCreate` (`startWizard()` · disabled เมื่อ DOC.active=false)
 ├ .seg (`segTabs()` · `setTabList()`): ทั้งหมด · ร่าง · ส่งแจ้งงานแล้ว · ยกเลิก
 └ .card.list-card
    ├ .filter-bar: `#fq` ค้นหา (`onQ()`) · search-select `fcarrier` ผู้ขนส่ง · `femp` ผู้จัดทำ · รีเซ็ต (`resetFilters()`)
    ├ .table-wrap > table.table  (sort `sortTh()`/`sortBy()` · แถว `rowClick()` · ⋮ `openRowMenu()`)
    └ .table-footer (`pager()` · page-size 10/25/50 `setSize()` · `goPage()`)
```
### P-02 Wizard (`renderWizard()` · `.drawer-panel.wide`)
```
.dw-head (eyebrow · .dw-title · `stepper()` 3 ขั้น)
.drawer-body
 ├ ขั้น 1 `wizMain()`: .wz-split
 │   ├ .wz-card ① ผู้ขนส่ง (search-select `wcarrier` → `pickCarrier()`) · รอบวันที่ (`bedateHTML('wround')` → `pickRound()`)
 │   ├ .wz-card ② table.ln-tbl (`lineRow()` ×n: input origin/destination/po/qty → `setLine()` soft update · `bedateHTML('ld'+i)` → `setLineDate()` · ลบ `removeLine()`) · .ln-msg error/เตือนใต้แถว · `addLine()` · `trimLines()` · datalist `#dlOrigin`
 │   └ `sumCard()` (.wz-sum sticky: ผู้ขนส่ง · ผู้จัดทำ · `#sumRound` · `#sumLines` · `#sumEarly` · `#sumTotal`)
 ├ ขั้น 2 `wizAttach()` (.upload-zone · `pickFiles()` · `removeFile()`)
 └ ขั้น 3 `wizReview()` (.review-card ×3 · `linesTable()`)
.dw-footer: ย้อนกลับ (`wizBack()`) · ยกเลิก · ถัดไป `#btnNext` (`wizNext()`) / บันทึกแบบร่าง `#btnDraft` (`saveDraft()`) · บันทึกและส่งแจ้งงาน `#btnSaveSubmit` (`saveAndSubmit()`)
```
### P-03 View (`renderViewDrawer()` · drawer 920)
```
.dw-head: .doc-ident (eyebrow ชื่อเอกสาร · .dw-title.mono เลขที่ · `docPill()` · .dw-sub รอบวันที่ + จำนวนรายการ) · .dw-actions ตามสถานะ · พิมพ์/ดาวน์โหลด (`genPdf()`) · ปิด
.drawer-tabs (`tabBtn()`): รายละเอียด `renderDetailTab()` · PDF Preview `renderPdfTab()` · ลายเซ็น / อนุมัติ `renderSignTab()` · ประวัติ `renderHistoryTab()`
.dw-footer: แก้ไขล่าสุด … · ปิด
```

## §5 Component Inventory
| Component | Anchor | States |
|---|---|---|
| Line table (แก้ได้) | `lineRow()` · `.ln-tbl` · `.ln-msg` | default · focus · invalid `.is-bad` (ช่องว่าง/จำนวน ≤ 0) + ข้อความใต้แถว · เตือน `.ln-msg.is-warn` (นัดส่งก่อนรอบวันที่) |
| Line table (อ่าน) | `linesTable()` · `.view-ln` | ไม่มีรายการ = "ยังไม่มีรายการ" · วันที่ก่อนรอบ = `.is-warn` |
| Summary | `sumCard()` · `softSum()` | ไม่มีรายการ = `.wz-sum-total.is-off` |
| Search select | `searchSelectHTML()` · `initSearchSelect()` | เปิด/ปิด · ค้นหา · ล้าง · keyboard |
| Date picker (พ.ศ.) | `bedateHTML()` · `.bedate` · `.bd-pop` | ว่าง placeholder · เลือกแล้ว · วันนี้ |
| Person chip | `empChip()` · `.emp-av` | วงกลม icon + ชื่อ + ตำแหน่ง |
| Carrier chip | `carrierChip()` · `.org-ic` | ยังไม่ได้เลือก |
| Sign progress | `renderSignProgress()` | DOA 0 ขั้น = "ไม่มีขั้นอนุมัติ" |
| Status pill | `docPill()` | ร่าง · ส่งแจ้งงานแล้ว · ยกเลิก |
| Empty | `emptyStateHTML()` | list: ยังไม่มีใบแจ้งงานขนส่งนอก / ไม่พบรายการที่ค้นหา |
| Loading | `busyLabel()` · `.spin` | "กำลังบันทึก…" ปุ่ม disabled |

## §6 Overlay Registry
| Overlay | Anchor | ขนาด | เปิด | ปิด / dismiss |
|---|---|---|---|---|
| drawer (view) | `#drawer.drawer-panel` | 920 | `showDrawer()` | ปุ่มปิด · Esc · backdrop **mousedown** (`drawerBackdropDown()`) |
| drawer (wizard) | `#drawer.drawer-panel.wide` | 1290 | `startWizard()` | dirty → modal "ทิ้งข้อมูลที่กรอกไว้?" ก่อนปิด |
| modal | `#modalBackdrop` · `#modal` (`.is-lg` สำหรับส่ง) | 520 / lg | `openModalCfg()` | ปุ่ม · Esc · backdrop mousedown (`modalBackdropDown()` — มีเหตุผลค้าง = ไม่ปิด) |
| row-menu | `.row-menu` (portal `#overlay-root`) | 180 | `openRowMenu()` | คลิกที่อื่น · scroll (`closeRowMenu()`) |
| date-pop | `.bd-pop` (portal `#overlay-root`) | 280 | `bdToggle()` | เลือกวัน · คลิกนอก · Esc |
| user-menu | `#userMenu` | — | `toggleUserMenu()` | คลิกนอก |
| ss-list | search-select list (portal) | ตาม input | focus | เลือก · คลิกนอก · Esc |
| toast | `#toast` | — | `showToast()` | หายเอง |

## §7 Interaction Spec
- Esc chain (BASE-KIT `keydown`): date-pop → modal → drawer (search-select ปิดก่อนใน `ssOnKey`) · drawer wizard dirty → modal ทิ้งข้อมูล
- Soft update: `setLine()` → `softSum()` อัปเดต `#sumLines` `#lnCount` `#sumEarly` `#sumTotal` โดยไม่ render ใหม่ (focus ไม่หลุด) · เลือกวัน/ผู้ขนส่ง/เพิ่ม-ลบแถว = render
- `addLine()` ยกต้นทาง+วันที่นัดส่งจากแถวก่อน แล้ว focus `[name=destination{n}]`
- Render preservation: `render()` ใช้ `preserveRenderState()` / `restoreRenderState()`
- Row menu render icon เฉพาะในเมนู (`data-rmic`) กันคลิกทะลุ
- PDF: iframe `.pdf-frame` srcdoc · `fitPdf()` · ดาวน์โหลด/พิมพ์ผ่าน iframe ซ่อน `.pdf-gen`

## §8 State-Driven UI Matrix
| status | pill | ปุ่มหัว drawer (ผู้ใช้) | เมนู ⋮ |
|---|---|---|---|
| draft | ร่าง (pill-muted) | เจ้าของ: ยกเลิก · แก้ไข · ส่งแจ้งงาน | ดูรายละเอียด · แก้ไข (เจ้าของ) · พิมพ์ · ยกเลิกเอกสาร (เจ้าของ/admin) |
| submitted | ส่งแจ้งงานแล้ว (pill-success) | เจ้าของ/admin: ยกเลิกเอกสาร | ดูรายละเอียด · พิมพ์ · ยกเลิกเอกสาร |
| cancelled | ยกเลิก (pill-danger) | — | ดูรายละเอียด · พิมพ์ |
แบนเนอร์ `viewBanner()`: ร่าง (n รายการ · กรอกไม่ครบ n แถว) · ส่งแล้วมีแถวนัดส่งก่อนรอบวันที่ (เตือน) · ยกเลิก (เหตุผล)

## §9 Microcopy (verbatim)
### Toast
| ข้อความ | ชนิด |
|---|---|
| ไม่มีการแจ้งเตือนใหม่ | toast |
| แบบเอกสารนี้ยังไม่เปิดใช้งาน | toast |
| แก้ไขได้เฉพาะร่างของตัวเอง | toast |
| ล้างแถวว่าง | toast |
| กรุณากรอกข้อมูลให้ครบถ้วน | toast |
| กรอกรายการให้ครบ 5 ช่อง หรือลบแถวที่ไม่ใช้ | toast |
| บันทึกร่างแล้ว · | toast |
| ส่งแจ้งงานแล้ว · | toast |
| ยกเลิกเอกสารแล้ว · | toast |
| ส่งออก | toast |
| สลับเป็น | toast |
| แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง | toast |
### ข้อความอื่นในหน้าจอ (สกัดจาก HTML)
- (นัดส่งก่อนรอบวันที่
- [Lucide] All CDNs failed. Icons จะไม่แสดง but UI ยังใช้งานได้
- ]); if (canCancel(r)) items.push(['x-circle', 'ยกเลิกเอกสาร',
- ], ['printer', 'พิมพ์',
- showToast('ไม่มีการแจ้งเตือนใหม่','info')
- · ร่าง
- · ส่งแจ้งงานแล้ว ล็อกแก้ไข
- · ส่งแจ้งงานแล้ว — แจ้งผู้ขนส่งเองด้วยว่ายกเลิก
- · แจ้งผู้จัดการฝ่ายขาย
- ก.ค.
- ก.พ.
- ก.ย.
- กรกฎาคม
- กรอกต้นทาง
- กรอกปลายทาง
- กรอกรายการให้ครบ 5 ช่อง หรือลบแถวที่ไม่ใช้
- กรอกเลขที่PO
- กรุงเทพฯ และปริมณฑล
- กรุณากรอกข้อมูลให้ครบถ้วน
- กันยายน
- กำลังเปิดหน้าต่างพิมพ์ ·
- กิตติ สมมติ
- กุมภาพันธ์
- ขั้นทดสอบ
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลหลักใบแจ้งงาน
- คลังสินค้า บางนา
- คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
- ความคืบหน้า
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค้นหา...
- ค้นหาเลขที่ / ผู้ขนส่ง / เลขที่PO / ปลายทาง
- จำนวน
- จำนวนต้องเป็นจำนวนเต็มมากกว่า 0
- จำนวนรวม
- ชนิดไฟล์ไม่รองรับ
- ชื่อฟังก์ชัน
- ดาวน์โหลด PDF
- ต.ค.
- ตรวจสอบและยืนยัน
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตุลาคม
- ต้นทาง
- ต้อง
- ต้องมีรายการงานขนส่งอย่างน้อย 1 รายการ
- ต้องมีรายการอย่างน้อย 1 รายการที่กรอกครบ 5 ช่อง
- ทั่วประเทศ
- ทั้งหมด
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ธ.ค.
- ธันวาคม
- นัดส่งก่อนรอบวันที่
- บริษัท ขนส่งตัวอย่าง จำกัด
- บริษัท ตัวอย่าง จำกัด
- บริษัท ทั่วไทยโลจิสติกส์สมมติ จำกัด
- บริษัท มั่นคงค้าส่ง จำกัด (สระบุรี)
- บริษัท สยามสโตร์ จำกัด (นนทบุรี)
- บริษัท ส่งไวทดสอบ จำกัด
- บันทึกร่างแล้ว ·
- ประวัติ
- ประวัติ (append-only)
- ปลายทาง
- ปิด
- ผู้ขนส่ง
- ผู้ขนส่งทั้งหมด
- ผู้ขนส่งรับงานไม่ได้ — แจ้งใหม่
- ผู้จัดการฝ่ายขาย
- ผู้จัดทำ
- ผู้จัดทำทุกคน
- ฝ่ายขาย
- พ.ค.
- พ.ย.
- พฤ
- พฤศจิกายน
- พฤษภาคม
- พิจารณาในระบบ
- พิมพ์
- พิมพ์ชื่อหรือรหัสผู้ขนส่ง
- ฟอร์มแจ้งงานขนส่งนอก
- ภาคกลาง
- ภาคกลาง/ตะวันออก
- ม.ค.
- มกราคม
- มาลี ทดสอบ
- มิ.ย.
- มิถุนายน
- มี.ค.
- มีนาคม
- ยกเลิก
- ยกเลิกเอกสาร
- ยกเลิกเอกสารแล้ว ·
- ยังไม่มีข้อมูล
- ยังไม่มีรายการ
- ยังไม่มีใบแจ้งงานขนส่งนอก
- ยังไม่ส่ง
- ยังไม่ได้เลือก
- ย้อนกลับ
- รอบวันที
- รอบวันที่
- รอส่งแจ้งงาน
- รายการ
- รายการ — แจ้งผู้จัดการฝ่ายขาย
- รายการ)
- รายการนัดส่งก่อนรอบวันที่ — จะแจ้งผู้จัดการฝ่ายขาย
- รายละเอียด
- ร่าง
- ร่างของฉัน
- ร้านทองดีค้าปลีก (อยุธยา)
- ร้านสมใจการค้า (ชลบุรี)
- ร้านเจริญดีมาร์ท (ฉะเชิงเทรา)
- ร้านใจดีพาณิชย์ (ลพบุรี)
- ลบแถว
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ลายเซ็น / อนุมัติ
- ลำดับ
- ลำดับการลงชื่อ
- ลูกค้าเลื่อนนัดส่ง
- ล้างตัวกรอง
- ล้างแถวว่าง
- วรวุฒิ ทองดี
- วันที่ ........./........./.........
- วันที่นัดส่ง
- วันที่นัดส่งไม่ก่อนรอบวันที่
- ส.ค.
- สถานะ
- สถานะเอกสาร
- สร้าง PDF
- สร้างฟอร์มแจ้งงานขนส่งนอก
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างโดย
- สร้างใบแจ้งงาน
- สร้างใบแจ้งงานเมื่อต้องส่งงานให้ผู้ขนส่งภายนอก
- สลับเป็น
- สายอนุมัติ (DOA)
- สิงหาคม
- สุนิสา ตัวอย่าง
- ส่งออก
- ส่งแจ้งงาน
- ส่งแจ้งงานขนส่ง
- ส่งแจ้งงานขนส่ง?
- ส่งแจ้งงานแล้ว
- ส่งแจ้งงานแล้ว ·
- ส่งแจ้งงานแล้ว — แจ้งผู้จัดการฝ่ายขายในระบบ
- ส่งแจ้งงานแล้วแก้ไขไม่ได้ — ถ้าต้องเปลี่ยน ให้ยกเลิกแล้วสร้างใหม่
- หจก. รถร่วมตัวอย่าง
- หจก. รุ่งเรืองพาณิชย์ (ระยอง)
- หจก. ศรีสุขค้าส่ง (ปราจีนบุรี)
- อา
- เจ้าหน้าที่ประสานงานขาย
- เดือนถัดไป
- เด้งกลับบน
- เพิ่มเติม
- เม.ย.
- เมษายน
- เลขที่
- เลขที่PO
- เลขที่เอกสาร
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกประเทศ
- เลือกผู้ขนส่งก่อนส่งแจ้งงาน
- เลือกผู้พิจารณา
- เลือกรอบวันที่ก่อนส่งแจ้งงาน
- เลือกวันที่
- เลือกวันที่นัดส่ง
- เอกสารแนบ
- แก้ไขร่าง
- แก้ไขล่าสุด
- แก้ไขเอกสาร
- แก้ไขใบแจ้งงาน
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งงานซ้ำ
- แจ้งงานซ้ำ — ใบที่ถูกต้องคือ OTN-2569-0004
- แถว
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- โรงงาน วังน้อย
- ใบ (
- ใบยืนยันรับงานจากผู้ขนส่ง.pdf
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่มี · 0 ขั้น
- ไม่มีขั้นอนุมัติ

## §10 Data Binding & BACKEND anchors
| Prototype | API (02_API) | หมายเหตุ |
|---|---|---|
| `RECS` · `listRows()` · `canSee()` | API-01/02/08 | FN-08 |
| `persist()` (ENG-DOC-NUM ตอนบันทึกครั้งแรก) · `lineErrors()` | API-03/04 | FN-01/02 |
| `openSubmit()` · `confirmSubmit()` · `validateRec()` · `resolveDoa()` · `MOCK_DOA_RESOLVED` (DOA-ENGINE-HOOK · 0 ขั้น · TODO: DOA engine) | API-05 | FN-03/04/06 |
| `confirmReason()` | API-06 | FN-05/06 · ENG-NOTIFY |
| `docPrintData()` · `tplRender()` · `tplSignRows()` · `DOC_TPL` | API-07 | FN-07 · parity กับ render_doc.py |
| `CARRIERS` | Vendor master (อ่าน) | ระบบจริงใช้ API ของ Vendor master |
| `DOC.active` | F-DOCCFG status | |

## §11 Traceability + Drift Log
| Brief | FRD | HTML |
|---|---|---|
| §4 P-01 | 01_UI P-01 · API-01/08 | `renderPage()` |
| §4 P-02 | 01_UI P-02 · API-03/04/09 | `renderWizard()` |
| §4 P-03 | 01_UI P-03 · API-02/05..07 | `renderViewDrawer()` |
| §6 modal | 01_UI M-01..03 · 05 VR-06 | `renderModal()` |
| §5 line table | 05 BR-01..04 · VR-03..05 | `lineRow()` · `lineErrors()` |
**Drift Log:** business 0 · HTML-only (prototype-only ไม่ต้องสร้าง): `window.__QA__` · `switchPersona()` สลับผู้ใช้ · `S.sim` / `commitRejected()` จำลอง API ล้ม · `ORIGINS` datalist (คำแนะนำต้นทาง — ระบบจริงอาจดึงจากคลัง/ที่อยู่บริษัท)

## §12 Diff จากเวอร์ชันก่อน
— ไม่มี (รอบแรก)

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- ดึงรายการจาก Sales Order/ใบส่งของ (OQ-06) · กันเลขที่PO ซ้ำ · ส่ง PDF ให้ผู้ขนส่งทางอีเมล · หน่วยของจำนวน (OQ-05)
