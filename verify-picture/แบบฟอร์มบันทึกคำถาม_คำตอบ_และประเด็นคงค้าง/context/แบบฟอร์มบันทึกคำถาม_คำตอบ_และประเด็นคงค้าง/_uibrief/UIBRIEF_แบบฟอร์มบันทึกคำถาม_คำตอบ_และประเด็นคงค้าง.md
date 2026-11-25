# UI_BRIEF — F-TMP-005 แบบฟอร์มบันทึกคำถาม คำตอบ และประเด็นคงค้าง (AS-BUILT)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| Prototype | `01_Prototype/feature.html` (html-generator-v9.4 · Q-form · audit FAIL 0 · self_audit PASS · smoke jsdom 47/47 (NO-BROWSER)) |
| FRD | FRD_F-TMP-005_Pack (01_UI · 05_RULES · 06_TESTS) · BRD-IVM-IVMC-001 |
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
| #/ivm-qa-log | P-01 รายการ | `renderPage()` |
| #/ivm-qa-log/view/:id | P-03 ดู (drawer 920) | `openView()` |
| #/ivm-qa-log/create | P-02 สร้าง (drawer wide) | `startWizard()` |
| #/ivm-qa-log/edit/:id | P-02 แก้ร่าง | `startWizard()` |
refresh-safe ผ่าน `applyRoute()` · hash เปลี่ยนด้วย `go()`

## §3 Layout Shell
sidebar 232px ดำ (module บริหารการลงทุน › บันทึกคำถามและประเด็นคงค้าง + badge รอฉันพิจารณา) · shell-bar 52px (breadcrumb · bell · user chip วงกลมรูปคน + เมนูสลับ persona เดโม) · content `#page-content` · `#overlay-root` สำหรับ portal

## §4 Page Anatomy
### P-01 รายการ — `renderPage()`
`.ph` ชื่อเอกสาร + sub (คำอธิบาย + `.ph-count` จำนวน / รออนุมัติ / รอฉันพิจารณา — ไม่มี stat cards U1) · ปุ่ม ส่งออก CSV (`exportCSV()`) + สร้างบันทึก (`startWizard()`) · `.filter-bar` ค้นหา + combobox สถานะ/กำหนดเวลา + รีเซ็ต (`resetFilters()`) · ตาราง (`sortTh()` · `rowClick()` · kebab `openRowMenu()`) · `pager()` page-size 10/25/50

### P-02 สร้าง/แก้ — `renderWizard()` (drawer `.drawer-panel.wide`)
stepper 3 ขั้น (`stepper()`) · ขั้น 1 `wizMain()`: การ์ด ① ชื่อโครงการ / ธุรกรรม (`setTop()`) ② บันทึกคำถามและคำตอบ `qEditor()` (ตารางกรอก · เลขที่คำถามระบบรัน `qNo()` · bedate ต่อช่อง `bdCell()` · select สถานะ `optSel()` · `addRow(qs)` / `removeRow()`) ③ รายการประเด็นคงค้าง `iEditor()` (ตารางกรอก · รหัสรายการ `oiNo()` · select ระดับความสำคัญ/สถานะ/ยกระดับ · `addRow(is)`) · การ์ดสรุปขวา `sumCard()` · ขั้น 2 `wizAttach()` · ขั้น 3 `wizReview()` · footer บันทึกแบบร่าง `saveDraft()` / บันทึกและส่งอนุมัติ `saveAndSubmit()`

### P-03 ดู — `renderViewDrawer()`
header (เลขที่ + pill สถานะ + sub คำถามค้างตอบ/ประเด็นยังไม่ปิด/เลยกำหนด U19 · ปุ่มตามสถานะ + พิมพ์/ดาวน์โหลด/ปิด) · แท็บ `tabBtn()`: รายละเอียด `renderDetailTab()` · PDF Preview `renderPdfTab()` · ลายเซ็น / อนุมัติ `renderSignTab()` · ประวัติ `renderHistoryTab()`

## §5 Component Inventory
| component | class / fn | ใช้ที่ |
|---|---|---|
| ตารางกรอกแถวซ้ำ | `.ed-tbl` · `qEditor()` · `iEditor()` | P-02 |
| ตารางแสดง | `qTable()` · `iTable()` · `dueCell()` | P-02/P-03 |
| การ์ดสรุป | `.wz-sum` · `sumCard()` | P-02 |
| ตัวเลือก | `optSel()` · `QST` / `IST` / `PRI` / `YN` pill | P-02/P-03 |
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
- พิมพ์ในช่อง = soft update ไม่ rebuild (focus ไม่หลุด) · `setTop()` · `setRow(…, soft)` + `softSum()` อัปเดตการ์ดสรุป
- กดถัดไป = `validateMain()` → ช่องแดง + ข้อความใต้แถว + toast · เลือกวันที่/ตัวเลือก = render ใหม่ (คำนวณเลยกำหนด) · ตอบแล้ว/ปิดไม่มีคำตอบ บล็อก · กำหนดก่อนวันเปิด บล็อก · ยกระดับไม่มีหมายเหตุ บล็อก · เลยกำหนด เตือน
- ส่ง → modal slot ต่อขั้น DOA (`resolveDoa()` · MOCK_DOA_RESOLVED) · อนุมัติเรียงขั้น `confirmApprove()` · ส่งกลับ/ยกเลิก `confirmReason()` · modal render เฉพาะตอนเปิด (state.modal.open) กันพังระหว่างปิด
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
- ปุ่ม: สร้างบันทึก
- ปุ่ม: ส่งอนุมัติ
- ปุ่ม: ส่งออก CSV
- ปุ่ม: เพิ่มคำถาม
- ปุ่ม: เพิ่มประเด็น
- ปุ่ม: แก้ไข
- placeholder: ${ph}
- placeholder: ${rej ? 'แจ้งผู้จัดทำว่าต้องแก้อะไร' : 'เหตุผลที่ยกเลิก'}
- placeholder: ' + ph + '
- placeholder: ค้นหาเลขที่ / ชื่อโครงการ / ผู้จัดทำ
- placeholder: ชื่อโครงการหรือธุรกรรม
- placeholder: ไม่บังคับ
- aria: ${label}
- aria: เดือนก่อน
- aria: เดือนถัดไป

### ข้อความอื่น (จากโค้ด)
- (ขั้น
- DR/02-กฎหมาย/สัญญาเช่า.pdf
- DR/03-การเงิน/งบทดลอง.xlsx
- [Lucide] All CDNs failed. Icons จะไม่แสดง but UI ยังใช้งานได้
- ]); if (canCancel(r)) items.push(['x-circle', 'ยกเลิกเอกสาร',
- ], ['printer', 'พิมพ์',
- ]]; if (isOwner(r) && r.status === 'draft') items.splice(1, 0, ['pencil', 'แก้ไข',
- showToast('ไม่มีการแจ้งเตือนใหม่','info')
- x–y จาก N
- · ต้องยกระดับ
- · อนุมัติแล้ว ล็อกแก้ไข
- · เลยกำหนด
- ก.ค.
- ก.พ.
- ก.ย.
- กรกฎาคม
- กรรมการผู้จัดการ
- กรอก
- กรุณากรอกข้อมูลให้ครบถ้วน
- กลาง
- กันยายน
- กานต์ ทดลองดี
- การเงิน
- กำลังดำเนินการ
- กำลังเปิดหน้าต่างพิมพ์ ·
- กำหนดตอบต้องไม่ก่อนวันที่
- กำหนดเสร็จ
- กำหนดเสร็จต้องไม่ก่อนวันที่เปิด
- กำหนดเสร็จยังไม่สมเหตุผล
- กุมภาพันธ์
- ขอสำเนาสัญญาเช่าที่ดินฉบับล่าสุด
- ขั้น ·
- ขั้นตอนที่ 2 / ขั้นตอนที่ 7: ติดตามคำถาม คำตอบ และประเด็นคงค้าง
- ขั้นถัดไป
- ขั้นทดสอบ
- ข้อ
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลหลักบันทึกคำถามและประเด็น
- ข้าม
- คน / หน่วยงาน
- คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
- คำตอบ
- คำตอบบางข้อยังไม่มีหลักฐานอ้างอิง
- คำถาม / คำขอ
- คำถาม / ประเด็น
- คำถาม ·
- คำถามค้างตอบ
- คำถามหรือคำขอ
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค่าเริ่มต้นจากสายอนุมัติ (DOA กลาง) และผังองค์กร
- ค้นหา...
- ค้นหาเลขที่ / ชื่อโครงการ / ผู้จัดทำ
- งบการเงินปีล่าสุดยังไม่ผ่านผู้สอบ
- จำนวนคำถาม
- จำนวนประเด็นคงค้าง
- ชนิดไฟล์ไม่รองรับ
- ชลธร ใจทดสอบ
- ชื่อฟังก์ชัน
- ชื่อโครงการ / ธุรกรรม
- ชื่อโครงการหรือธุรกรรม
- ดาวน์โหลด PDF
- ต.ค.
- ตรวจสอบและยืนยัน
- ตรวจสอบแล้ว
- ตอบแล้ว
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตามงบทดลองเดือนล่าสุด
- ตุลาคม
- ต่ำ
- ต้อง
- ต้องกรอกคำตอบ
- ต้องมีคำถามหรือประเด็นคงค้างอย่างน้อย 1 รายการ
- ต้องยกระดับ
- ต้องยกระดับ = ใช่ ต้องระบุเหตุผลในหมายเหตุ
- ต้องยกระดับหรือไม่
- ถึง
- ถ้ามี
- ทรัพย์สิน
- ทะเบียนทรัพย์สินไม่ตรงบัญชี
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ที่ปรึกษากฎหมาย ก
- ทุกกำหนดเวลา
- ทุกสถานะ
- ธ.ค.
- ธันวาคม
- ธีรวัฒน์ ระบบดี
- ธุรกรรมซื้อสินทรัพย์ตัวอย่าง จ
- ธุรกรรมซื้อหุ้นบริษัทตัวอย่าง ข
- ธุรกรรมซื้อหุ้นบริษัทตัวอย่าง ซ
- นักวิเคราะห์การลงทุน
- นิติกร
- นโยบายการรับรู้รายได้
- บริษัท ตัวอย่าง จำกัด (มหาชน)
- บริษัท ตัวอย่าง จำกัด (มหาชน) และบริษัทในเครือ
- บันทึกคำถาม คำตอบ และประเด็นคงค้าง
- บันทึกคำถาม คำตอบ และประเด็นคงค้างของธุรกรรม — ผู้จัดทำและสายอนุมัติระบบใส่ให้
- บันทึกซ้ำกับใบเดิม
- บันทึกผล
- บันทึกผิดโครงการ
- บันทึกยกระดับ ESC-001
- บันทึกร่างแล้ว ·
- ประวัติ
- ประวัติ (append-only)
- ประวิทย์ สมมติกุล
- ประเด็น
- ประเด็นคงค้าง
- ประเด็นที่ค้าง
- ประเด็นยังไม่ปิด
- ปรับปรุงแล้ว
- ปิด
- ปิดแล้ว
- ผู้จัดการฝ่ายบริหารการลงทุน
- ผู้จัดทำ
- ผู้ตรวจสอบ
- ผู้ถาม
- ผู้ประสานงานบริหารการลงทุน
- ผู้รับผิดชอบ
- ผู้รับผิดชอบตอบ
- ผู้รับผิดชอบที่ได้รับมอบหมาย
- ผู้รับผิดชอบบางประเด็นยังไม่ชัดเจน
- ผู้สอบบัญชีภายนอก
- ผู้ส่ง
- ผู้อนุมัติ / รับทราบ
- ฝ่ายกฎหมาย
- ฝ่ายบริหารการลงทุน
- ฝ่ายบัญชี
- ฝ่ายวางแผน
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
- มีรายการเลยกำหนด
- ยกระดับ
- ยกเลิก
- ยกเลิกเอกสาร
- ยกเลิกเอกสาร?
- ยกเลิกเอกสารแล้ว ·
- ยอดหนี้สินหมุนเวียน ณ สิ้นไตรมาส
- ยังไม่มีข้อมูล
- ยังไม่มีคำถาม
- ยังไม่มีบันทึกคำถามและประเด็นคงค้าง
- ยังไม่มีประเด็นคงค้าง
- ยังไม่มีประเด็นคงค้าง — กด "เพิ่มประเด็น"
- ยังไม่ส่ง
- ย้อนกลับ
- รอขั้นก่อนหน้า
- รอข้อมูล
- รองกรรมการผู้จัดการ
- รอตรวจทาน
- รอผล
- รอพิจารณา
- รออนุมัติ
- ระดับความสำคัญ
- ระบบเลือกตอนส่ง
- รายการ
- รายการคำถามจากผู้ซื้อ.xlsx
- รายละเอียด
- ร่าง
- ร่างคำตอบส่งผู้จัดการแล้ว
- ลบคำถามนี้
- ลบประเด็นนี้
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ลายเซ็น / อนุมัติ
- ลำดับการอนุมัติ
- ล้างตัวกรอง
- วันที่
- วันที่ ........./........./.........
- วันที่จัดทำ
- วันที่เปิด
- วิภา ตัวอย่างงาม
- ศิริพร ข้อมูลจำลอง
- ส.ค.
- สถานะ
- สถานะคดีความที่ค้างอยู่
- สถานะเอกสาร
- สร้าง PDF
- สร้างบันทึก
- สร้างบันทึกเมื่อเริ่มรับคำถามหรือพบประเด็นของธุรกรรม
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างโดย
- สลับเป็น
- สัญญา
- สัญญาลูกค้ารายใหญ่มีเงื่อนไขเปลี่ยนผู้ถือหุ้น
- สายอนุมัติ
- สำนักกรรมการผู้จัดการ
- สิงหาคม
- สูง
- ส่งกลับ
- ส่งกลับเป็นร่างแล้ว ·
- ส่งอนุมัติ
- ส่งอนุมัติแล้ว ·
- ส่งออก
- ส่งแล้วแก้ไขไม่ได้ — ถ้าถูกส่งกลับ จะกลับเป็นร่างเลขเดิมให้แก้แล้วส่งใหม่
- ส่งในระบบ
- อนุมัติ
- อนุมัติครบ — บันทึกมีผล
- อนุมัติแล้ว
- อนุมัติแล้ว · บันทึกมีผล
- อยู่ระหว่างจัดทำคำตอบ
- อรุณี รองตัวอย่าง
- ออกใช้ครั้งแรก
- อัปโหลดในห้องข้อมูลแล้ว
- อา
- เจ้าหน้าที่ดูแลเอกสารการลงทุน
- เช่น กฎหมาย
- เดือนถัดไป
- เด้งกลับบน
- เปิด
- เพิ่มคำถาม
- เพิ่มเติม
- เม.ย.
- เมษายน
- เลขที่
- เลขที่เอกสาร
- เลยกำหนด
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกประเทศ
- เลือกผู้พิจารณา
- เลือกวันที่
- เหตุผล / เลขที่บันทึกยกระดับ
- เหตุผลที่ยกเลิก
- เอกสารแนบ
- แก้ไขบันทึก
- แก้ไขร่าง
- แก้ไขล่าสุด
- แก้ไขเอกสาร
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งผู้จัดทำว่าต้องแก้อะไร
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบฟอร์ม
- แบบฟอร์มบันทึกคำถาม คำตอบ และประเด็นคงค้าง
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- แผนลงทุนเครื่องจักร 3 ปี
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
- ใช่
- ใช้ในขั้นตอน
- ใบอนุญาต
- ใบอนุญาตโรงงานหมดอายุสิ้นปี
- ไฟล์ / ตำแหน่ง
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่มี
- ไม่มีรายการเลยกำหนด
- ไม่ยกเลิก
- ไม่อนุมัติ
- ไม่ใช่
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
markers: {'marker': 'ENG-DOC-NUM', 'line': '/* doc_type IVMC — ประกาศใน DOCCFG_BRIEF_F-TMP-005 · เลขรันจาก ENG-DOC-NUM ตอนบันทึกครั้งแรก · เช็คสถานะเปิดใช้ที่ F-DOC'}, {'marker': 'DOA-ENGINE-HOOK', 'line': '/* DOA-ENGINE-HOOK — resolve จาก DOA entry ของ F-TMP-005 ณ เวลาส่ง แล้ว snapshot ลง approval_chain (DOA_BRIEF_F-TMP-005.'}, {'marker': 'TODO', 'line': 'approver_role / approved_by / approval_chain ต่อขั้น · จำนวนขั้นตั้งที่ DOA กลาง (dynamic) — ห้าม fix · TODO: DOA engine'}, {'marker': 'ENG-DOC-NUM', 'line': "/* บันทึกครั้งแรก = ENG-DOC-NUM.next('IVMC') ออกเลขที่ (DEC-11) · ผู้จัดทำ snapshot ตำแหน่ง/ฝ่าย ณ วันที่บันทึก */"}, {'marker': 'ENG-NOTIFY', 'line': '/* ENG-NOTIFY (NTF_BRIEF_F-TMP-005): ivmc_log_approved → ผู้รับผิดชอบตอบ/ผู้รับผิดชอบประเด็น · ivmc_escalation_flagged →'}, {'marker': 'DOA-ENGINE-HOOK', 'line': 'doa: MOCK_DOA_RESOLVED 2 ขั้น (role-line-manager → role-gm) = DOA-ENGINE-HOOK (DOA_BRIEF_F-TMP-005) · คำตัดสินผูก role ·'}, {'marker': 'ENG-DOC-NUM', 'line': "hooks: ENG-DOC-NUM.next('IVMC') ตอนบันทึกครั้งแรก · F-DOCCFG status (DOC.active) · ENG-NOTIFY ivmc_log_approved / ivmc_e"}, {'marker': 'ENG-NOTIFY', 'line': "hooks: ENG-DOC-NUM.next('IVMC') ตอนบันทึกครั้งแรก · F-DOCCFG status (DOC.active) · ENG-NOTIFY ivmc_log_approved / ivmc_e"}

## §11 Traceability + Drift Log
| จอ/ส่วน | FRD | หมายเหตุ |
|---|---|---|
| P-01..P-03 | 01_UI §1.1 | ตรง |
| การ์ด ①②③ | 01_UI §1.2 · FORM_SPEC F01–F21 | ตรง 1:1 (+ F01 ช่องเพิ่ม DEC-07) |
| เลข Q/OI · คำตอบบังคับ · กำหนด · ยกระดับ · เลยกำหนด | 05 BR-01..05 | ตรง |
Drift: ไม่มี (prototype = source of truth) · คำตัดสินขั้น 1 = ตรวจสอบแล้ว/ส่งกลับ (LD-01)

## §12 Diff จากเวอร์ชันก่อน
เวอร์ชันแรก

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- Phase 2: เลือกโครงการจากทะเบียน (FM-IVM-01) แทนพิมพ์ชื่อ · เปิดบันทึกยกระดับ FM-IVM-09 จากแถวยกระดับ (OQ-07) · อัปเดตคำตอบหลังอนุมัติ (OQ-08) · แจ้งเตือนก่อนกำหนดตอบ
