# UI_BRIEF — F-TMP-010 แบบฟอร์มบันทึกการอนุมัตินำส่ง (AS-BUILT)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| Prototype | `01_Prototype/feature.html` (html-generator-v9.4 · Q-form · audit FAIL 0 · self_audit PASS · smoke jsdom 58/58 (NO-BROWSER)) |
| FRD | FRD_F-TMP-010_Pack (01_UI · 05_RULES · 06_TESTS) · BRD-IVM-IVMH-001 |
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
| #/ivm-submission-approval | P-01 รายการ | `renderPage()` |
| #/ivm-submission-approval/view/:id | P-03 ดู (drawer 920) | `openView()` |
| #/ivm-submission-approval/create | P-02 สร้าง (drawer wide) | `startWizard()` |
| #/ivm-submission-approval/edit/:id | P-02 แก้ร่าง | `startWizard()` |
refresh-safe ผ่าน `applyRoute()` · hash เปลี่ยนด้วย `go()`

## §3 Layout Shell
sidebar 232px ดำ (module บริหารการลงทุน › บันทึกการอนุมัตินำส่ง + badge รอฉันพิจารณา) · shell-bar 52px (breadcrumb · bell · user chip วงกลมรูปคน + เมนูสลับ persona เดโม) · content `#page-content` · `#overlay-root` สำหรับ portal

## §4 Page Anatomy
### P-01 รายการ — `renderPage()`
`.ph` ชื่อเอกสาร + sub (คำอธิบาย + `.ph-count` จำนวน / รออนุมัติ / รอฉันพิจารณา — ไม่มี stat cards U1) · ปุ่ม ส่งออก CSV (`exportCSV()`) + สร้างแบบฟอร์ม (`startWizard()`) · `.filter-bar` ค้นหา + combobox สถานะ/ระดับอำนาจอนุมัติ + รีเซ็ต (`resetFilters()`) · ตาราง เลขที่ · วันที่ขอ · ชื่อโครงการ / ธุรกรรม · เรื่องที่ขออนุมัติ · ระดับอำนาจอนุมัติ · สถานะเอกสาร · ผลการพิจารณา (`resultKey()`) · ลายเซ็น (`sortTh()` · `rowClick()` · kebab `openRowMenu()`) · `pager()` page-size 10/25/50

### P-02 สร้าง/แก้ — `renderWizard()` (drawer `.drawer-panel.wide`)
stepper 3 ขั้น (`stepper()`) · ขั้น 1 `wizMain()`: การ์ด ① ขออนุมัติเรื่องอะไร (`fieldTop()` · `setTop()` · ชื่อโครงการ / ธุรกรรม · เรื่องที่ขออนุมัติ · เอกสารประกอบ) ② ระดับอำนาจอนุมัติ (`levelCards()` track-card 2 ค่า → render ใหม่) ③ ข้อเสนอและเงื่อนไข (ข้อเสนอของฝ่ายบริหารการลงทุน · เงื่อนไขการอนุมัติ) ④ ผลการพิจารณา `chainPreview()` (อ่านอย่างเดียว · ป้ายขั้นตามระดับ) · การ์ดสรุปขวา `sumCard()` · ขั้น 2 `wizAttach()` · ขั้น 3 `wizReview()` · footer บันทึกแบบร่าง `saveDraft()` / บันทึกและส่งอนุมัติ `saveAndSubmit()`

### P-03 ดู — `renderViewDrawer()`
header (เลขที่ + pill สถานะ + sub ระดับอำนาจอนุมัติ · ผลการพิจารณา U19 · ปุ่มตามสถานะ + พิมพ์/ดาวน์โหลด/ปิด) · แท็บ `tabBtn()`: รายละเอียด `renderDetailTab()` (ข้อมูลเอกสาร · รายละเอียดการขออนุมัติ `reqFields()` · ผลการพิจารณา `reviewTable()` · เงื่อนไขจากผู้อนุมัติ · เอกสารแนบ · ข้อมูลระบบ) · PDF Preview `renderPdfTab()` · ลายเซ็น / อนุมัติ `renderSignTab()` · ประวัติ `renderHistoryTab()`

## §5 Component Inventory
| component | class / fn | ใช้ที่ |
|---|---|---|
| ตารางผลการพิจารณา | `reviewTable()` | P-02/P-03 |
| รายละเอียดการขออนุมัติ | `reqFields()` | P-02/P-03 |
| การ์ดสรุป | `.wz-sum` · `sumCard()` | P-02 |
| ตัวเลือกระดับ / ผลการพิจารณา | `.track-card` · `levelCards()` · `decCards()` · `LEVEL` / `DECS` pill | P-02/M-02/M-03 |
| คน | `.emp-chip` · `.emp-av` · `empChip()` | ทุกจอ |
| ลายเซ็นในตาราง | `.sign-prog` · `renderSignProgress()` | P-01 |
| slot ผู้พิจารณา | `.slot-row` | M-01 |
| PDF | `.pdf-frame` · `docPdfDoc()` · `genPdf()` | P-03 |
| pill | `docPill()` · `lvPill()` · `decPill()` | ทุกจอ |
| empty | `emptyStateHTML()` | P-01/P-02/P-03 |
| ไฟล์แนบ | `.upload-zone` · `.file-row` · `gateFiles()` | P-02/P-03 |

## §6 Overlay Registry
| overlay | เปิด | ปิด |
|---|---|---|
| drawer (view 920 / wizard wide) | `showDrawer()` | `closeDrawer()` · backdrop mousedown `drawerBackdropDown()` · Esc |
| modal (ส่ง/พิจารณา/ส่งกลับ/ยกเลิก/ทิ้งข้อมูล) | `openModalCfg()` | `closeModal()` · backdrop mousedown `modalBackdropDown()` (กรอกค้างไม่ปิด) · Esc ก่อน drawer |
| row-menu (kebab) | `openRowMenu()` | `closeRowMenu()` · คลิกนอก · scroll |
| toast | `showToast()` | อัตโนมัติ |
| user-menu | `toggleUserMenu()` | คลิกนอก |
| ss-list combobox (portal) | `initSearchSelect()` | คลิกนอก · Esc |
overlay classes ที่พบ: drawer, drawer-avatar, drawer-backdrop, drawer-body, drawer-fields, drawer-footer, drawer-footer-meta, drawer-header, drawer-header-actions, drawer-header-divider, drawer-panel, drawer-section, drawer-section-title, drawer-stepper-band, drawer-subtitle, drawer-tab, drawer-tabs, drawer-title, menu-fixed, modal, modal-backdrop, modal-body, modal-footer, modal-header, modal-header-icon, modal-subtitle, modal-title, row-menu, toast, user-menu, user-menu-cap, user-menu-divider, user-menu-item

## §7 Interaction Spec
- พิมพ์ในช่อง = soft update ไม่ rebuild (focus ไม่หลุด) · `setTop()` + `softSum()` · เลือกระดับอำนาจอนุมัติ = render ใหม่ (สายอนุมัติ/ตารางผลการพิจารณาเปลี่ยน)
- กดถัดไป = `validateMain()` → ช่องแดง + toast · 5 ช่องบังคับ + ระดับอำนาจอนุมัติ · เงื่อนไขการอนุมัติไม่บังคับ
- ส่ง → modal slot ต่อขั้น DOA (`resolveDoa(emp, level)` · MOCK_DOA_RESOLVED · ขั้น 3 only:md) · พิจารณาเรียงขั้น `confirmApprove()` (ผลการพิจารณา `passOptions()` · รับทราบเฉพาะขั้นกลาง · มีเงื่อนไขต้องมีข้อสั่งการ) · ส่งกลับ `confirmReason()` (ให้แก้ไข / ไม่อนุมัติ · ข้อสั่งการบังคับ → ร่างเลขเดิม) · modal render เฉพาะตอนเปิด (state.modal.open) + guard `curStep()` ใน `renderModal()` กันพังระหว่างปิด
- จำลอง API ล้ม: `commitRejected()` (S.sim) · persona เดโม `switchPersona()`

## §8 State-Driven UI Matrix
| สถานะ | เจ้าของ | ผู้พิจารณาขั้นปัจจุบัน | ผู้ในสายอื่น | admin |
|---|---|---|---|---|
| draft | แก้ไข · ส่งอนุมัติ · ยกเลิก | ไม่เห็น | ไม่เห็น | เห็น (ยกเลิกได้) |
| draft (ถูกส่งกลับ) | แถบแดง "ถูกส่งกลับ (ให้แก้ไข / ไม่อนุมัติ) — ข้อสั่งการ" + แก้ไข/ส่ง | ไม่เห็น | ไม่เห็น | เห็น |
| pending | ยกเลิกเอกสาร | ตรวจสอบแล้ว/ส่งกลับ (ขั้น 1) · อนุมัติ / รับทราบ/ส่งกลับ (ขั้น 2–3) | ดูอย่างเดียว | ยกเลิกเอกสาร |
| approved | ดู · พิมพ์ · ล็อก (+ แถบอนุมัติแบบมีเงื่อนไข) | ดู | ดู | ดู |
| cancelled | ดู + แถบเหตุผล | ดู | ดู | ดู |

## §9 Microcopy (verbatim)
### toast
- ไม่มีการแจ้งเตือนใหม่
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- แก้ไขได้เฉพาะร่างของตัวเอง
- กรุณากรอกข้อมูลให้ครบถ้วน
- กรุณากรอกข้อมูลให้ครบถ้วน
- บันทึกร่างแล้ว ·
- กรุณากรอกข้อมูลให้ครบถ้วน
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
- ปุ่ม: สร้างแบบฟอร์ม
- ปุ่ม: ส่งอนุมัติ
- ปุ่ม: ส่งออก CSV
- ปุ่ม: แก้ไข
- placeholder: ${needNote ? 'ระบุเงื่อนไขที่ต้องดำเนินการก่อนนำส่ง' : 'ไม่บังคับ'}
- placeholder: ${ph}
- placeholder: ${rej ? 'แจ้งผู้จัดทำว่าต้องแก้อะไร' : 'เหตุผลที่ยกเลิก'}
- placeholder: ' + ph + '
- placeholder: ค้นหาเลขที่ / ชื่อโครงการ / เรื่องที่ขออนุมัติ
- aria: เดือนก่อน
- aria: เดือนถัดไป

### ข้อความอื่น (จากโค้ด)
- (ขั้น
- 2 ขั้น · ผู้จัดการฝ่ายบริหารการลงทุน → รองกรรมการผู้จัดการ
- 3 ขั้น · ผู้จัดการฝ่ายบริหารการลงทุน → รองกรรมการผู้จัดการ → กรรมการผู้จัดการ / ผู้มีอำนาจ
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
- กรกฎาคม
- กรรมการผู้จัดการ
- กรรมการผู้จัดการ / ผู้มีอำนาจ
- กรุณากรอกข้อมูลให้ครบถ้วน
- กรุณากรอกข้อเสนอของฝ่ายบริหารการลงทุน
- กรุณากรอกชื่อโครงการ / ธุรกรรม
- กรุณากรอกเรื่องที่ขออนุมัติ
- กรุณาระบุเงื่อนไข / ข้อสั่งการ
- กรุณาระบุเหตุผล
- กรุณาระบุเอกสารประกอบ
- กรุณาเลือกระดับอำนาจอนุมัติ
- กลับเป็นร่าง ผู้จัดทำแก้หรือยกเลิกได้
- กลับเป็นร่างให้ผู้จัดทำแก้ไข
- กันยายน
- กานต์ ทดลองดี
- กำลังเปิดหน้าต่างพิมพ์ ·
- กุมภาพันธ์
- ขออนุมัติดำเนินการยื่นข้อเสนอผูกพัน
- ขออนุมัติดำเนินการลงนามบันทึกความเข้าใจ
- ขออนุมัตินำส่งข้อเสนอการลงทุนให้พันธมิตร
- ขออนุมัตินำส่งข้อเสนอทางการเงินรอบสุดท้าย
- ขออนุมัตินำส่งข้อเสนอราคาเบื้องต้น
- ขออนุมัตินำส่งชุดเอกสารตรวจสอบสถานะ
- ขออนุมัตินำส่งชุดเอกสารเสนอราคาให้คู่สัญญาตัวอย่าง
- ขออนุมัตินำส่งรายงานความคืบหน้าให้ผู้ร่วมลงทุน
- ขออนุมัตินำส่งร่างสัญญาซื้อขายสินทรัพย์
- ขออนุมัตินำส่งหนังสือแสดงเจตจำนงให้ผู้ขาย
- ขออนุมัตินำส่งเอกสารประกวดราคา
- ขออนุมัตินำส่งแผนการลงทุนให้คณะกรรมการบริษัทย่อย
- ขั้น
- ขั้น ·
- ขั้นตอนที่ 6: การอนุมัติก่อนนำส่งหรือก่อนดำเนินการ
- ขั้นถัดไป
- ขั้นทดสอบ
- ขั้นที่พิจารณาแล้ว
- ขั้นสุดท้าย — อนุมัติครบ
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลระบบ
- ข้อเสนอของฝ่ายบริหารการลงทุน
- ข้อเสนอให้ผู้อนุมัติพิจารณา
- ข้าม
- คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค่าเริ่มต้นจากสายอนุมัติ (DOA กลาง) ตามระดับอำนาจอนุมัติ
- ค้นหา...
- ค้นหาเลขที่ / ชื่อโครงการ / เรื่องที่ขออนุมัติ
- จำนวนขั้น
- ชนิดไฟล์ไม่รองรับ
- ชลธร ใจทดสอบ
- ชื่อฟังก์ชัน
- ชื่อโครงการ / ธุรกรรม
- ณัฐพล สมมติกุล
- ดาวน์โหลด PDF
- ต.ค.
- ตรวจสอบและยืนยัน
- ตรวจสอบแล้ว
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตามตารางอำนาจอนุมัติ — กำหนดจำนวนขั้นพิจารณา
- ตุลาคม
- ต้อง
- ต้องแนบความเห็นฝ่ายกฎหมายก่อนนำส่ง
- ถึง
- ถ้ามี
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ทุกระดับอำนาจอนุมัติ
- ทุกสถานะ
- ธ.ค.
- ธันวาคม
- ธีรวัฒน์ ระบบดี
- ธุรกรรมซื้อสินทรัพย์ตัวอย่าง จ
- ธุรกรรมซื้อหุ้นบริษัทตัวอย่าง ข
- ธุรกรรมซื้อหุ้นบริษัทตัวอย่าง ซ
- นำส่งได้เมื่อได้รับความเห็นฝ่ายกฎหมายแล้ว
- บริษัท ตัวอย่าง จำกัด (มหาชน)
- บริษัท ตัวอย่าง จำกัด (มหาชน) และบริษัทในเครือ
- บันทึกซ้ำกับใบเดิม
- บันทึกผล
- บันทึกผิดโครงการ
- บันทึกร่างแล้ว ·
- ประวัติ
- ประวัติ (append-only)
- ปิด
- ผลการพิจารณา
- ผู้จัดการฝ่ายบริหารการลงทุน
- ผู้จัดการฝ่ายพัฒนาธุรกิจ
- ผู้จัดทำ
- ผู้ประสานงานบริหารการลงทุน
- ผู้ส่ง
- ผ่านขั้นนี้
- ผ่านขั้นนี้ + ต้องระบุเงื่อนไข
- ฝ่ายบริหารการลงทุน
- ฝ่ายพัฒนาธุรกิจ
- พ.ค.
- พ.ย.
- พฤ
- พฤศจิกายน
- พฤษภาคม
- พิจารณาในระบบ
- พิมพ์
- ม.ค.
- มกราคม
- มิ.ย.
- มิถุนายน
- มี.ค.
- มีนาคม
- ยกเลิก
- ยกเลิกเอกสาร
- ยกเลิกเอกสาร?
- ยกเลิกเอกสารแล้ว ·
- ยังไม่มีข้อมูล
- ยังไม่มีแบบฟอร์มบันทึกการอนุมัตินำส่ง
- ยังไม่ส่ง
- ย้อนกลับ
- รอขั้นก่อนหน้า
- รองกรรมการผู้จัดการ
- รอผล
- รอพิจารณา
- รออนุมัติ
- ระดับอำนาจอนุมัติ
- ระดับอำนาจอนุมัติไม่ถูกต้อง
- ระบบเลือกตอนส่ง
- รับทราบ
- รับทราบ ส่งต่อขั้นถัดไป
- รายการ
- รายการเอกสารประกอบ (แนบไฟล์ได้ในขั้นถัดไป)
- รายละเอียด
- รายละเอียดการขออนุมัติ
- ร่าง
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ลายเซ็น / อนุมัติ
- ลำดับการอนุมัติ
- ล้างตัวกรอง
- วันที่ ........./........./.........
- วันที่ขอ
- วิภา ตัวอย่างงาม
- ศิริพร ข้อมูลจำลอง
- ส.ค.
- สถานะ
- สถานะเอกสาร
- สมศักดิ์ ใหญ่ทดสอบ
- สรุปเงื่อนไขสัญญาหลัก · แบบจำลองทางการเงิน · หนังสือนำส่ง
- สรุปเงื่อนไขสัญญาหลัก.docx
- สร้าง PDF
- สร้างเมื่อต้องขออนุมัติก่อนนำส่งเอกสารหรือก่อนดำเนินการสำคัญ
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างแบบฟอร์ม
- สลับเป็น
- สายอนุมัติ
- สำนักกรรมการผู้จัดการ
- สิงหาคม
- สิ่งที่ขออนุมัติก่อนนำส่งหรือก่อนดำเนินการ
- ส่งกลับ
- ส่งกลับเป็นร่างแล้ว ·
- ส่งอนุมัติ
- ส่งอนุมัติ?
- ส่งอนุมัติแล้ว ·
- ส่งออก
- ส่งแล้วแก้ไขไม่ได้ — ถ้าถูกส่งกลับ (ให้แก้ไข / ไม่อนุมัติ) จะกลับเป็นร่างเลขเดิมให้แก้แล้วส่งใหม่
- ส่งในระบบ
- หนังสือนำส่ง.pdf
- อนุมัติ
- อนุมัติ (ขั้น 1)
- อนุมัติ / รับทราบ
- อนุมัติแบบมีเงื่อนไข
- อนุมัติแบบมีเงื่อนไข · ดำเนินการตามเงื่อนไขก่อนนำส่ง
- อนุมัติแล้ว
- อนุมัติแล้ว · นำส่งหรือดำเนินการได้
- อรุณี รองตัวอย่าง
- ออกใช้ครั้งแรก
- อา
- เงื่อนไข / ข้อสั่งการ
- เงื่อนไขการอนุมัติ
- เงื่อนไขจากผู้อนุมัติ
- เจ้าหน้าที่ดูแลเอกสารการลงทุน
- เจ้าหน้าที่พัฒนาธุรกิจ
- เดือนถัดไป
- เด้งกลับบน
- เพิ่มเติม
- เม.ย.
- เมษายน
- เรื่องที่ขออนุมัติ
- เลขที่
- เลขที่เอกสาร
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกประเทศ
- เลือกผู้พิจารณา
- เลือกระดับอำนาจอนุมัติก่อน
- เลือกระดับอำนาจอนุมัติเพื่อดูขั้นพิจารณา
- เลือกวันที่
- เหตุผล
- เหตุผลที่ยกเลิก
- เห็นควรอนุมัติให้นำส่งตามกรอบที่คณะทำงานสรุป
- เอกสารประกอบ
- เอกสารประกอบไม่ครบ
- เอกสารแนบ
- แก้ไขร่าง
- แก้ไขเอกสาร
- แก้ไขแบบฟอร์ม
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งผู้จัดทำว่าต้องแก้อะไร
- แนบตารางเปรียบเทียบเงื่อนไขก่อนลงนาม
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบฟอร์ม
- แบบฟอร์มบันทึกการอนุมัตินำส่ง
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- โครงการขยายกำลังผลิตตัวอย่าง ง
- โครงการพลังงานตัวอย่าง ช
- โครงการร่วมทุนตัวอย่าง ค
- โครงการลงทุนตัวอย่าง ก
- โครงการลงทุนตัวอย่าง ฉ
- โครงการลงทุนตัวอย่าง ฌ
- โครงการลงทุนตัวอย่าง ญ
- โครงการลงทุนตัวอย่าง ฎ
- โครงการโครงสร้างพื้นฐานตัวอย่าง ฏ
- ใช้เป็นหลักฐานการตรวจทานและอนุมัติก่อนส่งเอกสารหรือดำเนินการสำคัญตามตารางอำนาจอนุมัติ
- ใช้ในขั้นตอน
- ให้ปรับข้อเสนอและแนบตารางเปรียบเทียบ
- ให้แก้ไข
- ให้แก้ไข (ขั้น 2)
- ไม่นำส่ง / ไม่ดำเนินการแล้ว
- ไม่นำส่ง / ไม่ดำเนินการแล้ว — ผู้บริหารให้ยุติที่ขั้นคัดกรอง
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่มีข้อมูล
- ไม่ยกเลิก
- ไม่อนุมัติ
- — คุณเป็นผู้พิจารณาบันทึกนี้

## §10 Data Binding & BACKEND anchors
| จอ | ข้อมูล | anchor |
|---|---|---|
| P-01 | API-01 list (canSee) | `listRows()` · `canSee()` |
| P-02 | API-03/04 body (FRD 02 §2.2) | `persist()` · `validateMain()` |
| M-01 | API-05/06 doa-preview/submit | `openSubmit()` · `confirmSubmit()` · DOA-ENGINE-HOOK |
| M-02/03 | API-07 decide | `confirmApprove()` · `confirmReason()` |
| M-04 | API-08 cancel | `openCancel()` |
| P-03 PDF | API-09 · data contract print-spec §8 | `docPrintData()` · `tplRender()` · `tplSignRows()` |
| QA | e2e_standard | window.__QA__ |
markers: {'marker': 'ENG-DOC-NUM', 'line': '/* doc_type IVMH — ประกาศใน DOCCFG_BRIEF_F-TMP-010 · เลขรันจาก ENG-DOC-NUM ตอนบันทึกครั้งแรก · เช็คสถานะเปิดใช้ที่ F-DOC'}, {'marker': 'DOA-ENGINE-HOOK', 'line': '/* DOA-ENGINE-HOOK — resolve จาก DOA entry ของ F-TMP-010 ณ เวลาส่ง แล้ว snapshot ลง approval_chain (DOA_BRIEF_F-TMP-010.'}, {'marker': 'TODO', 'line': "approver_role / approved_by / approval_chain ต่อขั้น · จำนวนขั้นตั้งที่ DOA กลาง (dynamic) — ห้าม fix · ขั้นที่มี only:'"}, {'marker': 'ENG-DOC-NUM', 'line': "/* บันทึกครั้งแรก = ENG-DOC-NUM.next('IVMH') ออกเลขที่ (DEC-10) · ผู้จัดทำ snapshot ตำแหน่ง/ฝ่าย ณ วันที่บันทึก */"}, {'marker': 'ENG-NOTIFY', 'line': '/* ENG-NOTIFY (NTF_BRIEF_F-TMP-010): ivmh_conditional_approved → ผู้จัดทำ + admin role (อนุมัติครบ และมีขั้น อนุมัติแบบม'}, {'marker': 'DOA-ENGINE-HOOK', 'line': 'doa: MOCK_DOA_RESOLVED ค่าเริ่ม 3 ขั้น (role-line-manager → role-gm → role-gm · ขั้น 3 เฉพาะระดับกรรมการผู้จัดการ) = DOA'}, {'marker': 'ENG-DOC-NUM', 'line': "hooks: ENG-DOC-NUM.next('IVMH') ตอนบันทึกครั้งแรก · F-DOCCFG status (DOC.active) · ENG-NOTIFY ivmh_conditional_approved "}, {'marker': 'ENG-NOTIFY', 'line': "hooks: ENG-DOC-NUM.next('IVMH') ตอนบันทึกครั้งแรก · F-DOCCFG status (DOC.active) · ENG-NOTIFY ivmh_conditional_approved "}

## §11 Traceability + Drift Log
| จอ/ส่วน | FRD | หมายเหตุ |
|---|---|---|
| P-01..P-03 | 01_UI §1.1 | ตรง |
| การ์ด ①②③④ | 01_UI §1.2 · FORM_SPEC F01–F13 | ตรง 1:1 (DEC-06 ไม่เพิ่มช่อง) |
| ระดับ → 2/3 ขั้น · ผลการพิจารณา 5 ค่า · ข้อสั่งการบังคับ · รับทราบขั้นกลาง · เรียงขั้น | 05 BR-01..07 | ตรง |
Drift: ไม่มี (prototype = source of truth) · คำตัดสินช่องลงชื่อ: role-line-manager = ตรวจสอบแล้ว/ส่งกลับ · role-gm = อนุมัติ / รับทราบ/ส่งกลับ (LD-04)

## §12 Diff จากเวอร์ชันก่อน
เวอร์ชันแรก

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- Phase 2: เลือกโครงการจากทะเบียน (FM-IVM-01) แทนพิมพ์ชื่อ · อ้างชุดเอกสารนำส่ง FM-IVM-07 (OQ-07) · บันทึกการปฏิบัติตามเงื่อนไขหลังอนุมัติ (OQ-08)
