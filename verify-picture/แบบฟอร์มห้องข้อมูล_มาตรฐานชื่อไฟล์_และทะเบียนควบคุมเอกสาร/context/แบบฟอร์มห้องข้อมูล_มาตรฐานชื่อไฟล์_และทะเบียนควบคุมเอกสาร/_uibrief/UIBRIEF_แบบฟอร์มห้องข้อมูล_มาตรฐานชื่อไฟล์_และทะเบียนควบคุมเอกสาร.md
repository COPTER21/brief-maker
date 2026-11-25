# UI_BRIEF — F-TMP-006 แบบฟอร์มห้องข้อมูล มาตรฐานชื่อไฟล์ และทะเบียนควบคุมเอกสาร (AS-BUILT)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| Prototype | `01_Prototype/feature.html` (html-generator-v9.4 · Q-form · audit FAIL 0 · self_audit PASS · smoke 46/46 · jsdom 26/26 (NO-BROWSER)) |
| FRD | FRD_F-TMP-006_Pack (01_UI · 05_RULES · 06_TESTS) · BRD-IVM-IVMD-001 |
| แบบพิมพ์ | print/form.tpl.html (thai-doc v2.2 Replica · 2 หน้า) |
| Mode | AS-BUILT — สกัดจาก HTML จริง ห้ามแต่ง (R1/R3) · html-ui-brief extract_anchors → inventory.json |
| Date | 2026-10-11 |

## §1 Design Tokens AS-BUILT
CI = CUBE Warm Light (html-generator-v9 · ห้ามแก้) · ฟอนต์ Noto Sans Thai

| token | ค่า |
|---|---|
| --c-navy | #111111 |
| --c-navy-2 | #111111 |
| --c-primary | #FF3B30 |
| --c-primary-hover | #E62E24 |
| --c-teal | #FF9A1F |
| --c-teal-light | #FFB763 |
| --c-ink | #111111 |
| --c-mute | #54565C |
| --c-mute-2 | #73757B |
| --c-mute-3 | #9A9CA2 |
| --c-placeholder | rgb(180,182,188) |
| --z-content | 1 |
| --z-sticky | 10 |
| --z-shell | 10 |
| --z-dropdown | 30 |
| --z-backdrop | 50 |
| --z-drawer | 51 |
| --z-modal | 60 |
| --z-popover | 70 |
| --z-toast | 80 |
| --c-line | #DEDAD4 |
| --c-line-2 | #E9E5E0 |
| --c-line-3 | #F1EEEA |
| --c-bg-off | #FAF8F5 |
| --c-success | #1F9D55 |
| --c-warning | #E8870F |
| --c-danger | #E62E24 |
| --sidebar-w | 232px |
| --shell-h | 52px |
| --fs-h1 | 22px |
| --fs-h2 | 17px |
| --fs-h3 | 15px |
| --fs-body | 14px |
| --fs-sub | 13px |
| --fs-meta | 12px |
| --fs-cap | 11px |
| --fs-kpi | 28px |
| --sp-xs | 4px |
| --sp-sm | 8px |
| --sp-md | 12px |
| --sp-lg | 20px |
| --sp-xl | 28px |
| --r-xs | 4px |
| --r-sm | 6px |
| --r-md | 8px |
| --r-lg | 12px |
| --r-full | 999px |

### z-index map
| selector | z |
|---|---|
| /* ============== SIDEBAR ============== */ .sidebar | var(--z-shell) |
| /* ============== SHELL BAR ============== */ .shell-bar | var(--z-sticky) |
| /* User dropdown menu */ .user-menu | var(--z-dropdown) |
| .table-wrap thead th | var(--z-sticky) |
| * เมนูที่ portal ออกจาก scroll container (ใช้คู่ portalMenu util) */ .menu-fixed | var(--z-popover) |
| .ss-list | var(--z-backdrop) |
| verlay-root ตอนเปิด (หลุด overflow ของ modal/drawer body) */ .ss-list.menu-fixed | var(--z-popover) |
| .table-scroll.is-sticky thead th | 3 |
| .stepper-circle | 2 |
| .stepper-item:not(:last-child)::after | 1 |
| .drawer-backdrop | var(--z-backdrop) |
| .drawer | var(--z-drawer) |
| รมีปุ่ม action หลัก */ /* ============== MODAL ============== */ .modal-backdrop | var(--z-backdrop) |
| /* ============== TOAST ============== */ .toast | var(--z-toast) |
| .wizard-footer | var(--z-sticky) |
| .info-tip::after | var(--z-dropdown) |
| /* v9.1 Rule #62 — modal เหนือ drawer */ .modal-backdrop | var(--z-modal) |
| #drawer | var(--z-drawer) |
| #drawerBackdrop | var(--z-backdrop) |
| #toast | var(--z-toast) |
| /* row menu ⋮ (portal ใน #overlay-root) */ .row-menu | var(--z-popover) |
| .bd-pop | var(--z-portal) |

## §2 Route Map
| Route | จอ | เปิดด้วย |
|---|---|---|
| #/ivm-data-room | P-01 รายการ | `renderPage()` |
| #/ivm-data-room/view/:id | P-03 ดู (drawer 920) | `openView()` |
| #/ivm-data-room/create · /create/copy-:id | P-02 สร้าง (drawer wide) | `startWizard()` |
| #/ivm-data-room/edit/:id | P-02 แก้ร่าง | `startWizard()` |
refresh-safe ผ่าน `applyRoute()` · hash เปลี่ยนด้วย `go()`

## §3 Layout Shell
sidebar 232px ดำ (module บริหารการลงทุน › ห้องข้อมูลและทะเบียนเอกสาร + badge รอฉันพิจารณา) · shell-bar 52px (breadcrumb · bell · user chip วงกลมรูปคน + เมนูสลับ persona เดโม) · content `#page-content` · `#overlay-root` สำหรับ portal

## §4 Page Anatomy
### P-01 รายการ — `renderPage()`
`.ph` ชื่อเอกสาร + sub (คำอธิบาย + `.ph-count` จำนวน / รออนุมัติ / รอฉันพิจารณา — ไม่มี stat cards U1) · ปุ่ม ส่งออก CSV (`exportCSV()`) + สร้างทะเบียน (`startWizard()`) · `.filter-bar` ค้นหา + combobox สถานะ/สถานะทะเบียนเอกสาร + รีเซ็ต (`resetFilters()`) · ตาราง (`sortTh()` · `rowClick()` · kebab `openRowMenu()`) · `pager()` page-size 10/25/50

### P-02 สร้าง/แก้ — `renderWizard()` (drawer `.drawer-panel.wide`)
stepper 4 ขั้น (`stepper()`) · ขั้น 1 `wizRoom()`: การ์ด ① ชื่อโครงการ / ธุรกรรม (`setTop()`) ② โครงสร้างโฟลเดอร์ `fdEditor()` (ตั้งต้น 8 แถวจาก `DEFAULT_FOLDERS` · select ระดับสิทธิ `optSel()` · `addRow(fd)` / `removeRow()`) ③ มาตรฐานการตั้งชื่อไฟล์ `namingBlock()` (อ่านอย่างเดียว) · ขั้น 2 `wizDocs()`: ทะเบียนเอกสาร `dcEditor()` (bedate `bdCell()` · ชื่อไฟล์ตามมาตรฐาน `stdFileName()` สด) + การเปลี่ยนแปลง `chEditor()` · ขั้น 3 `wizAccess()`: สิทธิการเข้าถึง `acEditor()` + เอกสารแนบ · ขั้น 4 `wizReview()` · การ์ดสรุปขวา `sumCard()` + `warnList()` · footer บันทึกแบบร่าง `saveDraft()` / บันทึกและส่งอนุมัติ `saveAndSubmit()`

### P-03 ดู — `renderViewDrawer()`
header (เลขที่ + pill สถานะ + sub โฟลเดอร์ · เอกสาร (ค้าง) · สิทธิใช้งาน U19 · ปุ่มตามสถานะ + ทำซ้ำ/พิมพ์/ดาวน์โหลด/ปิด) · แท็บ `tabBtn()`: รายละเอียด `renderDetailTab()` · PDF Preview `renderPdfTab()` · ลายเซ็น / อนุมัติ `renderSignTab()` · ประวัติ `renderHistoryTab()`

## §5 Component Inventory
| component | class / fn | ใช้ที่ |
|---|---|---|
| ตารางกรอกแถวซ้ำ | `.ed-tbl` · `fdEditor()` · `dcEditor()` · `chEditor()` · `acEditor()` | P-02 |
| ตารางแสดง | `fdTable()` · `dcTable()` · `chTable()` · `acTable()` · `.fn-std` | P-02/P-03 |
| การ์ดสรุป | `.wz-sum` · `sumCard()` | P-02 |
| ตัวเลือก | `optSel()` · `ALV` `DST` `CST` `AST` pill | P-02/P-03 |
| คน | `.emp-chip` · `.emp-av` · `empChip()` | ทุกจอ |
| ลายเซ็นในตาราง | `.sign-prog` · `renderSignProgress()` | P-01 |
| slot ผู้พิจารณา | `.slot-row` | M-01 |
| PDF | `.pdf-frame` · `docPdfDoc()` · `genPdf()` | P-03 |
| วันที่ พ.ศ. | `.bedate` · `bedateHTML()` | P-02 |
| pill | `docPill()` · `pill()` | ทุกจอ |
| empty | `emptyStateHTML()` | P-01/P-03 |
| ไฟล์แนบ | `.upload-zone` · `.file-row` · `gateFiles()` | P-02/P-03 |

## §6 Overlay Registry
| overlay | เปิด | ปิด |
|---|---|---|
| drawer (view 920 / wizard wide) | `showDrawer()` | `closeDrawer()` · backdrop mousedown `drawerBackdropDown()` · Esc |
| modal (ส่ง/อนุมัติ/ส่งกลับ/ยกเลิก/ทิ้งข้อมูล) | `openModalCfg()` | `closeModal()` · backdrop mousedown `modalBackdropDown()` (กรอกค้างไม่ปิด) · Esc ก่อน drawer |
| row-menu (kebab) | `openRowMenu()` | `closeRowMenu()` · คลิกนอก · scroll |
| toast | `showToast()` | อัตโนมัติ |
| user-menu | `toggleUserMenu()` | คลิกนอก |
| ss-list combobox (portal) | `initSearchSelect()` | คลิกนอก · Esc |
| popover ปฏิทิน (bd-pop) | `bdToggle()` | `bdClose()` · Esc ปิดแค่ปฏิทิน |
overlay classes ที่พบ: drawer, drawer-avatar, drawer-backdrop, drawer-body, drawer-fields, drawer-footer, drawer-footer-meta, drawer-header, drawer-header-actions, drawer-header-divider, drawer-panel, drawer-section, drawer-section-title, drawer-stepper-band, drawer-subtitle, drawer-tab, drawer-tabs, drawer-title, menu-fixed, modal, modal-backdrop, modal-body, modal-footer, modal-header, modal-header-icon, modal-subtitle, modal-title, row-menu, toast, user-menu, user-menu-cap, user-menu-divider, user-menu-item

## §7 Interaction Spec
- พิมพ์ในช่อง = soft update ไม่ rebuild (focus ไม่หลุด) · `setTop()` · `setRow(…, soft)` + อัปเดตชื่อไฟล์ตามมาตรฐานสด
- กดถัดไป = `validateStep()` ต่อขั้น → ช่องแดง + ข้อความใต้แถว + toast · บันทึก = `validateUpTo(3)` กลับไปขั้นแรกที่ผิด · ฉบับ Vnn/Final บล็อก · นำไปใช้แล้วต้องมีวันที่มีผล · วันที่ยกเลิกสิทธิ บล็อก · ฉบับไม่ใช่ Final / วันที่มีผลก่อนวันที่ เตือน
- ส่ง → modal slot ต่อขั้น DOA (`resolveDoa()` · MOCK_DOA_RESOLVED) · อนุมัติเรียงขั้น `confirmApprove()` · ส่งกลับ/ยกเลิก `confirmReason()` · modal วาดใหม่เฉพาะ `state.modal.open` (ระหว่างปิดไม่ render ใบที่ตัดสินแล้ว)
- จำลอง API ล้ม: `commitRejected()` (S.sim) · persona เดโม `switchPersona()`

## §8 State-Driven UI Matrix
| สถานะ | เจ้าของ | ผู้พิจารณาขั้นปัจจุบัน | ผู้ในสายอื่น | admin |
|---|---|---|---|---|
| draft | แก้ไข · ส่งอนุมัติ · ยกเลิก | ไม่เห็น | ไม่เห็น | เห็น (ยกเลิกได้) |
| draft (ถูกส่งกลับ) | แถบแดง "ถูกส่งกลับแก้ไข — เหตุผล" + แก้ไข/ส่ง | ไม่เห็น | ไม่เห็น | เห็น |
| pending | ยกเลิกเอกสาร | ตรวจสอบแล้ว/ส่งกลับ (ขั้น 1) · อนุมัติ/ไม่อนุมัติ (ขั้นสุดท้าย) | ดูอย่างเดียว | ยกเลิกเอกสาร |
| approved | ดู · พิมพ์ · ล็อก | ดู | ดู | ดู |
| cancelled | ดู + แถบเหตุผล | ดู | ดู | ดู |

## §9 Microcopy (verbatim)
### toast
- ไม่มีการแจ้งเตือนใหม่
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- แก้ไขได้เฉพาะร่างของตัวเอง
- กรุณากรอกข้อมูลให้ครบถ้วน
- กรุณากรอกข้อมูลให้ครบถ้วน
- บันทึกร่างแล้ว ·
- ส่งอนุมัติแล้ว ·
- บันทึกผล
- ส่งออก
- สลับเป็น
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง

### ปุ่ม / placeholder / label
- ปุ่ม: ' + (cfg.actionIcon ? ' ' : '') + ' ' + cfg.actionLabel + '
- ปุ่ม: '+d+'
- ปุ่ม: กลับไปกรอกต่อ
- ปุ่ม: ดาวน์โหลด PDF
- ปุ่ม: ถัดไป
- ปุ่ม: ทิ้งข้อมูล
- ปุ่ม: บริหารการลงทุน
- ปุ่ม: บันทึกแบบร่าง
- ปุ่ม: ปิด
- ปุ่ม: พิมพ์
- ปุ่ม: ยกเลิก
- ปุ่ม: ยกเลิกเอกสาร
- ปุ่ม: ย้อนกลับ
- ปุ่ม: รีเซ็ต
- ปุ่ม: วันนี้
- ปุ่ม: สร้างทะเบียน
- ปุ่ม: ส่งอนุมัติ
- ปุ่ม: ส่งออก CSV
- ปุ่ม: แก้ไข
- placeholder: ${ph}
- placeholder: ${rej ? 'แจ้งผู้จัดทำว่าต้องแก้อะไร' : 'เหตุผลที่ยกเลิก'}
- placeholder: ' + ph + '
- placeholder: V01 / Final
- placeholder: ค้นหาเลขที่ / ชื่อโครงการ / ผู้จัดทำ
- placeholder: ชื่อโครงการหรือธุรกรรม
- placeholder: ไม่บังคับ
- aria: ${label}
- aria: ฉบับ
- aria: เดือนก่อน
- aria: เดือนถัดไป

### ข้อความอื่น (จากโค้ด)
- (ขั้น
- (ค้าง
- 02_การเงิน / ภาษี
- 03_กฎหมาย / สัญญา
- 04_การค้า / ธุรกิจ
- 06_การนำส่ง / การอนุมัติ
- [Lucide] All CDNs failed. Icons จะไม่แสดง but UI ยังใช้งานได้
- ]); if (canCancel(r)) items.push(['x-circle', 'ยกเลิกเอกสาร',
- ], ['printer', 'พิมพ์',
- ]]; if (isOwner(r) && r.status === 'draft') items.splice(1, 0, ['pencil', 'แก้ไข',
- showToast('ไม่มีการแจ้งเตือนใหม่','info')
- x–y จาก N
- · อนุมัติแล้ว ล็อกแก้ไข
- ก.ค.
- ก.พ.
- ก.ย.
- กฎหมาย / สัญญา
- กรกฎาคม
- กรรมการผู้จัดการ
- กรอก
- กรุณากรอกข้อมูลให้ครบถ้วน
- กันยายน
- กานต์ ทดลองดี
- การค้า / ธุรกิจ
- การนำส่ง / การอนุมัติ
- การเงิน / ภาษี
- การเปลี่ยนแปลง
- กำลังเปิดหน้าต่างพิมพ์ ·
- กำหนดโครงสร้างโฟลเดอร์ ผู้รับผิดชอบ และระดับสิทธิ — ใบใหม่ตั้งต้น 8 โฟลเดอร์มาตรฐาน แก้ชื่อหรือเพิ่มได้
- กุมภาพันธ์
- ก่อนวันที่
- ขอบเขตโฟลเดอร์ / เอกสาร
- ขั้น ·
- ขั้นตอนที่ 3 / ขั้นตอนที่ 5 / ขั้นตอนที่ 6 / ขั้นตอนที่ 8: การจัดห้องข้อมูลและการควบคุมเอกสาร
- ขั้นทดสอบ
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลบุคคล — จำกัดสิทธิ
- ข้อมูลบุคลากร / การกำกับดูแล
- ข้อเสนอที่ปรึกษา
- ข้าม
- คน / หน่วยงาน
- คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค่าเริ่มต้นจากสายอนุมัติ (DOA กลาง) และผังองค์กร
- ค้นหา...
- ค้นหาเลขที่ / ชื่อโครงการ / ผู้จัดทำ
- ค้าง
- ค้างตรวจทาน / อนุมัติ
- งบการเงิน 3 ปี · แบบแสดงรายการภาษี
- งบตรวจสอบออกแล้ว
- จำกัดเฉพาะกลุ่ม
- จำนวนเอกสาร
- จำนวนโฟลเดอร์
- ฉบับ
- ฉบับต้องเป็น V01, V02 … หรือ Final
- ฉบับต้องเป็น V01, V02 … หรือ Final · ระบบแสดงชื่อไฟล์ที่ควรเป็นตามมาตรฐานใต้ชื่อเอกสาร
- ฉบับทำงาน
- ฉบับสมบูรณ์
- ชนิดไฟล์ไม่รองรับ
- ชลธร ใจทดสอบ
- ชื่อผู้ใช้งาน
- ชื่อฟังก์ชัน
- ชื่อเอกสาร
- ชื่อเอกสาร / ฉบับ
- ชื่อโครงการ / ธุรกรรม
- ชื่อโครงการหรือธุรกรรม
- ชื่อโฟลเดอร์
- ชื่อไฟล์ตามมาตรฐาน
- ดาวน์โหลด PDF
- ต.ค.
- ตรวจสอบและยืนยัน
- ตรวจสอบแล้ว
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตัวอย่าง
- ตุลาคม
- ต้อง
- ต้องระบุวันที่ยกเลิกสิทธิ
- ถึง
- ถ้ามี
- ทรัพย์สิน
- ทะเบียนทรัพย์สิน
- ทะเบียนสถานะเอกสารและประวัติฉบับ
- ทะเบียนห้องข้อมูลและควบคุมเอกสาร
- ทะเบียนเอกสาร
- ทะเบียนเอกสารยังไม่ครบ
- ทำซ้ำ
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ที่ปรึกษา
- ที่ปรึกษากฎหมายภายนอก
- ที่ปรึกษาการเงินภายนอก
- ทุกสถานะ
- ทุกสถานะทะเบียนเอกสาร
- ทุกโฟลเดอร์
- ธ.ค.
- ธันวาคม
- ธีรวัฒน์ ระบบดี
- ธุรกรรมซื้อสินทรัพย์ตัวอย่าง จ
- ธุรกรรมซื้อหุ้นบริษัทตัวอย่าง ข
- ธุรกรรมซื้อหุ้นบริษัทตัวอย่าง ซ
- นักวิเคราะห์การลงทุน
- นำไปใช้แล้ว
- นิติกร
- บทบาท
- บริษัท ตัวอย่าง จำกัด (มหาชน)
- บริษัท ตัวอย่าง จำกัด (มหาชน) และบริษัทในเครือ
- บันทึกซ้ำกับใบเดิม
- บันทึกปิดงาน
- บันทึกผล
- บันทึกผิดโครงการ
- บันทึกร่างแล้ว ·
- บันทึกสิทธิการเข้าถึงข้อมูล
- บันทึกเป็นทะเบียน — ผู้ดูแลห้องข้อมูลนำไปตั้งสิทธิในไดรฟ์จริงหลังอนุมัติ
- ประวัติ
- ประวัติ (append-only)
- ประวิทย์ สมมติกุล
- ปรับตัวเลขรายได้ปีล่าสุด
- ปิด
- ผังห้องข้อมูลโครงการ ก.xlsx
- ผังองค์กร · นโยบายกำกับดูแล
- ผู้จัดการฝ่าย
- ผู้จัดการฝ่ายบริหารการลงทุน
- ผู้จัดทำ
- ผู้ดูแลระบบ
- ผู้ตรวจสอบ
- ผู้ประสานงาน
- ผู้ประสานงาน ก
- ผู้ประสานงานบริหารการลงทุน
- ผู้รับผิดชอบ
- ผู้รับผิดชอบที่ได้รับมอบหมาย
- ผู้ส่ง
- ผู้อนุมัติ / รับทราบ
- ผู้ใช้งาน
- ผู้ใช้งานภายนอกได้สิทธิกว้างเกินไป
- ผู้ใช้ตัวอย่าง 1
- ผู้ใช้ตัวอย่าง 2
- ผู้ใช้ตัวอย่าง 3
- ฝ่ายกฎหมาย
- ฝ่ายบริหารการลงทุน
- พ.ค.
- พ.ย.
- พฤ
- พฤศจิกายน
- พฤษภาคม
- พิมพ์
- ม.ค.
- มกราคม
- มิ.ย.
- มิถุนายน
- มี.ค.
- มีนาคม
- มีเอกสารค้างตรวจทาน / อนุมัติ
- มูลค่ากิจการ
- ยกเลิก
- ยกเลิกเอกสาร
- ยกเลิกเอกสาร?
- ยกเลิกเอกสารแล้ว ·
- ยังไม่มีการเปลี่ยนแปลงเอกสาร
- ยังไม่มีการเปลี่ยนแปลงเอกสาร — เพิ่มเมื่อมีการแก้ไขเอกสารในทะเบียน
- ยังไม่มีข้อมูล
- ยังไม่มีทะเบียนห้องข้อมูล
- ยังไม่มีบันทึกสิทธิ — เพิ่มผู้ใช้งานที่ได้รับสิทธิเข้าห้องข้อมูล
- ยังไม่มีโฟลเดอร์
- ยังไม่ส่ง
- ย้อนกลับ
- รอขั้นก่อนหน้า
- รองกรรมการผู้จัดการ
- รอตรวจทาน
- รอผล
- รอพิจารณา
- รออนุมัติ
- ระดับสิทธิ
- ระดับสิทธิของบางโฟลเดอร์ยังไม่เหมาะสม
- ระบบเลือกตอนส่ง
- รายการ
- รายงานตรวจสอบสถานะด้านกฎหมาย
- รายละเอียด
- รายละเอียดการเปลี่ยนแปลง
- รูปแบบฉบับเอกสาร
- รูปแบบวันที่
- ร่าง
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ลายเซ็น / อนุมัติ
- ลำดับการอนุมัติ
- ล้างตัวกรอง
- วันที่
- วันที่ ........./........./.........
- วันที่_ชื่อเอกสาร_ฉบับ_สถานะ
- วันที่จัดทำ
- วันที่ฉบับ
- วันที่ยกเลิกสิทธิต้องไม่ก่อนวันที่ให้สิทธิ
- วันที่ให้สิทธิ
- วิภา ตัวอย่างงาม
- ศิริพร ข้อมูลจำลอง
- ส.ค.
- สถานะ
- สถานะ นำไปใช้แล้ว ต้องระบุวันที่มีผล
- สถานะสิทธิ
- สถานะเอกสาร
- สร้าง PDF
- สร้างทะเบียน
- สร้างทะเบียนเมื่อเริ่มจัดห้องข้อมูลของธุรกรรม
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างโดย
- สลับเป็น
- สัญญาสำคัญ · สัญญาเช่า
- สายอนุมัติ
- สำนักกรรมการผู้จัดการ
- สิงหาคม
- สิทธิการเข้าถึงและเอกสารแนบ
- สิทธิใช้งาน
- ส่งกลับ
- ส่งกลับเป็นร่างแล้ว ·
- ส่งภายนอก
- ส่งอนุมัติ
- ส่งอนุมัติ?
- ส่งอนุมัติแล้ว ·
- ส่งออก
- ส่งแล้วแก้ไขไม่ได้ — ถ้าถูกส่งกลับ จะกลับเป็นร่างเลขเดิมให้แก้แล้วส่งใหม่
- ส่งในระบบ
- หนังสือรับรอง · อำนาจลงนาม
- หนังสือแสดงเจตจำนง
- หน่วยงาน
- หมดอายุ
- ห้องข้อมูลและมาตรฐานชื่อไฟล์
- อนุมัติ
- อนุมัติแล้ว
- อนุมัติแล้ว · ทะเบียนห้องข้อมูลมีผล
- อรุณี รองตัวอย่าง
- ออกใช้ครั้งแรก
- อา
- อ่านอย่างเดียว
- เจ้าหน้าที่ดูแลห้องข้อมูลการลงทุน
- เช่น 01, 03
- เช่น IM / V03
- เช่น งบการเงิน 3 ปี
- เดือนถัดไป
- เด้งกลับบน
- เพิ่มการเปลี่ยนแปลง
- เพิ่มผู้ใช้งาน
- เพิ่มสมมติฐานอัตราคิดลด
- เพิ่มเติม
- เพิ่มเอกสาร
- เพิ่มโฟลเดอร์
- เม.ย.
- เมษายน
- เลขที่
- เลขที่เอกสาร
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกประเทศ
- เลือกผู้พิจารณา
- เลือกวันที่
- เสนอแก้ไข
- เหตุผลที่ยกเลิก
- เอกสาร
- เอกสารบริษัท / อำนาจลงนาม
- เอกสารปิดงาน
- เอกสารเสนออนุมัติ
- แก้อะไร
- แก้ไข
- แก้ไขทะเบียน
- แก้ไขร่าง
- แก้ไขล่าสุด
- แก้ไขเอกสาร
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งผู้จัดทำว่าต้องแก้อะไร
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบจำลองทางการเงิน
- แบบจำลองทางการเงิน / V02
- แบบฟอร์ม
- แบบฟอร์มห้องข้อมูล มาตรฐานชื่อไฟล์ และทะเบียนควบคุมเอกสาร
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- แผนธุรกิจ · ลูกค้าหลัก
- โครงการ / ธุรกรรม
- โครงการขยายกำลังผลิตตัวอย่าง ง
- โครงการพลังงานตัวอย่าง ช
- โครงการร่วมทุนตัวอย่าง ค
- โครงการลงทุนตัวอย่าง ก
- โครงการลงทุนตัวอย่าง ฉ
- โครงการลงทุนตัวอย่าง ฌ
- โครงการลงทุนตัวอย่าง ญ
- โครงการลงทุนตัวอย่าง ฎ
- โครงการไม่ดำเนินการต่อ
- โครงการไม่ดำเนินการต่อ — ผู้บริหารให้ยุติที่ขั้นคัดกรอง
- โครงสร้างชื่อไฟล์
- โฟลเดอร์
- โฟลเดอร์ / ลิงก์
- โฟลเดอร์ / เอกสาร
- โฟลเดอร์ ·
- ใช้งาน
- ใช้ในขั้นตอน
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่มี
- ไม่มีเอกสารค้าง
- ไม่ยกเลิก
- ไม่อนุมัติ
- — คุณเป็นผู้พิจารณาบันทึกนี้

## §10 Data Binding & BACKEND anchors
| จอ | ข้อมูล | anchor |
|---|---|---|
| P-01 | API-01 list (canSee) | `listRows()` · `canSee()` |
| P-02 | API-03/04 body (FRD 02 §2.2) | `persist()` · `validateStep()` · `loadDefaults` = `NAMING` · `DEFAULT_FOLDERS` |
| M-01 | API-05/06 doa-preview/submit | `openSubmit()` · `confirmSubmit()` · DOA-ENGINE-HOOK |
| M-02/03 | API-07 decide | `confirmApprove()` · `confirmReason()` |
| M-04 | API-08 cancel | `openCancel()` |
| P-03 PDF | API-09 · data contract print-spec §8 | `docPrintData()` · `tplRender()` · `tplSignRows()` |
| QA | e2e_standard | window.__QA__ |
markers: {'marker': 'ENG-DOC-NUM', 'line': '/* doc_type IVMD — ประกาศใน DOCCFG_BRIEF_F-TMP-006 · เลขรันจาก ENG-DOC-NUM ตอนบันทึกครั้งแรก · เช็คสถานะเปิดใช้ที่ F-DOC'}, {'marker': 'DOA-ENGINE-HOOK', 'line': '/* DOA-ENGINE-HOOK — resolve จาก DOA entry ของ F-TMP-006 ณ เวลาส่ง แล้ว snapshot ลง approval_chain (DOA_BRIEF_F-TMP-006.'}, {'marker': 'TODO', 'line': 'approver_role / approved_by / approval_chain ต่อขั้น · จำนวนขั้นตั้งที่ DOA กลาง (dynamic) — ห้าม fix · TODO: DOA engine'}, {'marker': 'ENG-DOC-NUM', 'line': "/* บันทึกครั้งแรก = ENG-DOC-NUM.next('IVMD') ออกเลขที่ (DEC-13) · ผู้จัดทำ snapshot ตำแหน่ง/ฝ่าย ณ วันที่บันทึก */"}, {'marker': 'ENG-NOTIFY', 'line': '/* ENG-NOTIFY (NTF_BRIEF_F-TMP-006): ivmd_register_approved → ผู้จัดทำ + admin role (ไปตั้งสิทธิในไดรฟ์จริง) · ivmd_canc'}, {'marker': 'DOA-ENGINE-HOOK', 'line': 'doa: MOCK_DOA_RESOLVED 2 ขั้น (role-line-manager → role-gm) = DOA-ENGINE-HOOK (DOA_BRIEF_F-TMP-006) · คำตัดสินผูก role ·'}, {'marker': 'ENG-DOC-NUM', 'line': "hooks: ENG-DOC-NUM.next('IVMD') ตอนบันทึกครั้งแรก · F-DOCCFG status (DOC.active) · ENG-NOTIFY ivmd_register_approved / i"}, {'marker': 'ENG-NOTIFY', 'line': "hooks: ENG-DOC-NUM.next('IVMD') ตอนบันทึกครั้งแรก · F-DOCCFG status (DOC.active) · ENG-NOTIFY ivmd_register_approved / i"}

## §11 Traceability + Drift Log
| จอ/ส่วน | FRD | หมายเหตุ |
|---|---|---|
| P-01..P-03 | 01_UI §1.1 | ตรง |
| ขั้น 1–3 การ์ด | 01_UI §1.2 · FORM_SPEC F01–F37 | ตรง 1:1 (+ F01 ช่องเพิ่ม DEC-09) |
| ฉบับ / การเปลี่ยนแปลง / สิทธิ | 05 BR-04..08 | ตรง |
| ชื่อไฟล์ตามมาตรฐาน | 05 BR-06 | ตัวช่วยบนจอ ไม่อยู่บนกระดาษ (LD-07) |
Drift: ไม่มี (prototype = source of truth) · คำตัดสินขั้น 1 = ตรวจสอบแล้ว/ส่งกลับ (LD-01)

## §12 Diff จากเวอร์ชันก่อน
เวอร์ชันแรก

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- Phase 2: เลือกโครงการจากทะเบียน (FM-IVM-01) แทนพิมพ์ชื่อ · ฉบับแก้ไขทะเบียนหลังอนุมัติ (OQ-07) · เตือนสิทธิผู้ใช้ภายนอกใกล้หมดอายุ · ส่งต่อ FM-IVM-11 ตอนปิดงาน
