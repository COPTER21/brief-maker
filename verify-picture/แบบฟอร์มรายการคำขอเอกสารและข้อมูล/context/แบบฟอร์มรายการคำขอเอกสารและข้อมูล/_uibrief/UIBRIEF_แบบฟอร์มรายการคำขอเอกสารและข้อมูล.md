# UI_BRIEF — F-TMP-007 แบบฟอร์มรายการคำขอเอกสารและข้อมูล (AS-BUILT)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| Prototype | `01_Prototype/feature.html` (html-generator-v9.4 · Q-form · audit FAIL 0 · self_audit PASS · jsdom 42/42 (NO-BROWSER)) |
| FRD | FRD_F-TMP-007_Pack (01_UI · 05_RULES · 06_TESTS) · BRD-IVM-IVME-001 |
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
| #/ivm-doc-request | P-01 รายการ | `renderPage()` |
| #/ivm-doc-request/view/:id | P-03 ดู (drawer 920) | `openView()` |
| #/ivm-doc-request/create | P-02 สร้าง (drawer wide) | `startWizard()` |
| #/ivm-doc-request/edit/:id | P-02 แก้ร่าง | `startWizard()` |
refresh-safe ผ่าน `applyRoute()` · hash เปลี่ยนด้วย `go()`

## §3 Layout Shell
sidebar 232px ดำ (module บริหารการลงทุน › รายการคำขอเอกสารและข้อมูล + badge รอฉันพิจารณา) · shell-bar 52px (breadcrumb · bell · user chip วงกลมรูปคน + เมนูสลับ persona เดโม) · content `#page-content` · `#overlay-root` สำหรับ portal

## §4 Page Anatomy
### P-01 รายการ — `renderPage()`
`.ph` ชื่อเอกสาร + sub (คำอธิบาย + `.ph-count` จำนวน / รออนุมัติ / รอฉันพิจารณา — ไม่มี stat cards U1) · ปุ่ม ส่งออก CSV (`exportCSV()` 1 แถวต่อคำขอ) + สร้างรายการคำขอ (`startWizard()`) · `.filter-bar` ค้นหา + combobox สถานะ/การติดตาม + รีเซ็ต (`resetFilters()`) · ตาราง (`sortTh()` · `rowClick()` · `overCell()` · kebab `openRowMenu()` ไม่มีทำซ้ำ) · `pager()` page-size 10/25/50

### P-02 สร้าง/แก้ — `renderWizard()` (drawer `.drawer-panel.wide`)
stepper 3 ขั้น (`stepper()`) · ขั้น 1 `wizRequests()`: การ์ด ① ชื่อโครงการ / ธุรกรรม (`setTop()`) ② รายการคำขอ `rqEditor()` (ตั้งต้น 1 แถว `BLANK_RQ()` รหัส `nextCode()` · bedate `bdCell()` · select สถานะ `stSel()` · ป้ายเกินกำหนด `isOver()` · `addRow()` / `removeRow()`) ③ หมายเหตุการใช้งาน (`POLICY.usage_note` อ่านอย่างเดียว) · ขั้น 2 `wizFiles()` เอกสารแนบ · ขั้น 3 `wizReview()` · การ์ดสรุปขวา `sumCard()` + `warnList()` · footer บันทึกแบบร่าง `saveDraft()` / บันทึกและส่งอนุมัติ `saveAndSubmit()`

### P-03 ดู — `renderViewDrawer()`
header (เลขที่ + pill สถานะ + sub คำขอ n รายการ · ได้รับครบ n (U19) · ปุ่มตามสถานะ + พิมพ์/ดาวน์โหลด/ปิด) · แท็บ `tabBtn()`: รายละเอียด `renderDetailTab()` (ตารางคำขอ `rqTable()` · สรุป `sumLine()` · หมายเหตุการใช้งาน) · PDF Preview `renderPdfTab()` · ลายเซ็น / อนุมัติ `renderSignTab()` · ประวัติ `renderHistoryTab()`

## §5 Component Inventory
| component | class / fn | ใช้ที่ |
|---|---|---|
| ตารางกรอกแถวซ้ำ | `.ed-tbl` · `rqEditor()` · `rowMsg()` | P-02 |
| ตารางแสดง | `rqTable()` · `.rs-view` | P-02/P-03 |
| การ์ดสรุป | `.wz-sum` · `sumCard()` · `summary()` | P-02 |
| ตัวเลือกสถานะ | `stSel()` · `RST` pill | P-02/P-03 |
| ป้ายเกินกำหนด / ตรวจรหัสผ่าน | `isOver()` · `hasPw()` · `.pill-danger` / `.pill-warning` | P-01/P-02/P-03 |
| คน | `.emp-chip` · `.emp-av` · `empChip()` | ทุกจอ |
| ลายเซ็นในตาราง | `.sign-prog` · `renderSignProgress()` | P-01 |
| slot ผู้พิจารณา | `.slot-row` | M-01 |
| PDF | `.pdf-frame` · `docPdfDoc()` · `genPdf()` | P-03 |
| วันที่ พ.ศ. | `.bedate` · `bedateHTML()` | P-02 |
| pill | `docPill()` · `pill()` | ทุกจอ |
| empty | `emptyStateHTML()` · `emptyTbl()` | P-01/P-03 |
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
- พิมพ์ในช่อง = soft update ไม่ rebuild (focus ไม่หลุด) · `setTop()` · `setRow(…, soft)` · เปลี่ยนสถานะ/วันที่ = render ใหม่ (ป้ายเกินกำหนด/การ์ดสรุปอัปเดต)
- กดถัดไป = `validateStep()` → ช่องแดง + ข้อความใต้แถว (`rowErrors()`) + toast · สถานะ↔วันที่ · ลำดับวันที่ · หมายเหตุเมื่อปิดรายการ · ลิงก์ path/URL บล็อก · เกินกำหนด / คำว่ารหัสผ่าน เตือน · บันทึกและส่ง = `guardAll(true)` ต้องมีคำขอ ≥1
- ส่ง → modal slot ต่อขั้น DOA (`resolveDoa()` · MOCK_DOA_RESOLVED) · อนุมัติเรียงขั้น `confirmApprove()` · ส่งกลับ/ยกเลิก `confirmReason()` · modal วาดใหม่เฉพาะ `state.modal.open` + `renderModal()` คืนว่างเมื่อไม่มีขั้นรอพิจารณา (ระหว่างปิดไม่ render ใบที่ตัดสินแล้ว)
- จำลอง API ล้ม: `commitRejected()` (S.sim) · persona เดโม `switchPersona()`

## §8 State-Driven UI Matrix
| สถานะ | เจ้าของ | ผู้พิจารณาขั้นปัจจุบัน | ผู้ในสายอื่น | admin |
|---|---|---|---|---|
| draft | แก้ไข · ส่งอนุมัติ · ยกเลิก | ไม่เห็น | ไม่เห็น | เห็น (ยกเลิกได้) |
| draft (ถูกส่งกลับ) | แถบแดง ถูกส่งกลับแก้ไข + เหตุผล + แก้ไข/ส่ง | ไม่เห็น | ไม่เห็น | เห็น |
| pending | ยกเลิกเอกสาร | ตรวจสอบแล้ว/ส่งกลับ (ขั้น 1) · อนุมัติ/ไม่อนุมัติ (ขั้นสุดท้าย) | ดูอย่างเดียว | ยกเลิกเอกสาร |
| approved | ดู · พิมพ์ · ล็อก | ดู | ดู | ดู |
| cancelled | ดู + แถบเหตุผล | ดู | ดู | ดู |

## §9 Microcopy (verbatim)
### toast
- ไม่มีการแจ้งเตือนใหม่
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- แก้ไขได้เฉพาะร่างของตัวเอง
- กรุณากรอกข้อมูลให้ครบถ้วน
- บันทึกร่างแล้ว ·
- ต้องมีรายการคำขออย่างน้อย 1 รายการก่อนส่ง
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
- ปุ่ม: สร้างรายการคำขอ
- ปุ่ม: ส่งอนุมัติ
- ปุ่ม: ส่งออก CSV
- ปุ่ม: เพิ่มคำขอ
- ปุ่ม: แก้ไข
- placeholder: ${ph}
- placeholder: ${rej ? 'แจ้งผู้จัดทำว่าต้องแก้อะไร' : 'เหตุผลที่ยกเลิก'}
- placeholder: ' + ph + '
- placeholder: ค้นหาเลขที่ / ชื่อโครงการ / ผู้จัดทำ
- placeholder: ชื่อโครงการหรือธุรกรรม
- placeholder: ไม่บังคับ
- aria: สถานะ
- aria: เดือนก่อน
- aria: เดือนถัดไป

### ข้อความอื่น (จากโค้ด)
- (ขั้น
- SOP-04: การขอข้อมูลและการรับมอบงาน
- [Lucide] All CDNs failed. Icons จะไม่แสดง but UI ยังใช้งานได้
- ]); if (canCancel(r)) items.push(['x-circle', 'ยกเลิกเอกสาร',
- ], ['printer', 'พิมพ์',
- ]]; if (isOwner(r) && r.status === 'draft') items.splice(1, 0, ['pencil', 'แก้ไข',
- path หรือ URL
- showToast('ไม่มีการแจ้งเตือนใหม่','info')
- x–y จาก N
- · อนุมัติแล้ว ล็อกแก้ไข
- ก.ค.
- ก.พ.
- ก.ย.
- กรกฎาคม
- กรรมการผู้จัดการ
- กรอก
- กรุณากรอกข้อมูลให้ครบถ้วน
- กันยายน
- กานต์ ทดลองดี
- กำลังเปิดหน้าต่างพิมพ์ ·
- กำหนดส่ง
- กำหนดส่งต้องไม่ก่อนวันที่ขอ
- กำหนดส่งไม่สอดคล้องกับแผนงาน
- กุมภาพันธ์
- ขอแล้ว
- ขั้น ·
- ขั้นทดสอบ
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้าม
- คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
- คำขอ
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค่าเริ่มต้นจากสายอนุมัติ (DOA กลาง) และผังองค์กร
- ค้นหา...
- ค้นหาเลขที่ / ชื่อโครงการ / ผู้จัดทำ
- งบการเงินตรวจสอบย้อนหลัง 3 ปี
- ชนิดไฟล์ไม่รองรับ
- ชลธร ใจทดสอบ
- ชื่อฟังก์ชัน
- ชื่อโครงการ / ธุรกรรม
- ชื่อโครงการหรือธุรกรรม
- ดาวน์โหลด PDF
- ต.ค.
- ตรวจสอบและยืนยัน
- ตรวจสอบแล้ว
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตุลาคม
- ต้อง
- ต้องมีรายการคำขออย่างน้อย 1 รายการก่อนส่ง
- ต้องระบุวันที่ขอ
- ถึง
- ถ้ามี
- ทะเบียนทรัพย์สินถาวร
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ที่ปรึกษาการเงินภายนอก
- ทุกการติดตาม
- ทุกสถานะ
- ธ.ค.
- ธันวาคม
- ธีรวัฒน์ ระบบดี
- ธุรกรรมซื้อสินทรัพย์ตัวอย่าง จ
- ธุรกรรมซื้อหุ้นบริษัทตัวอย่าง ข
- ธุรกรรมซื้อหุ้นบริษัทตัวอย่าง ซ
- นักวิเคราะห์ ค
- นักวิเคราะห์การลงทุน
- บริษัท ตัวอย่าง จำกัด (มหาชน)
- บริษัท ตัวอย่าง จำกัด (มหาชน) และบริษัทในเครือ
- บันทึกซ้ำกับใบเดิม
- บันทึกผล
- บันทึกผิดโครงการ
- บันทึกร่างแล้ว ·
- บันทึกสิ่งที่ต้องขอ จากใคร ใครติดตาม และกำหนดส่ง — ระบบไม่ส่งคำขอถึงผู้ถูกขอข้อมูลให้ (ติดตามนอกระบบ)
- ประมาณการรายได้ 5 ปี
- ประวัติ
- ประวัติ (append-only)
- ประวิทย์ สมมติกุล
- ปิด
- ผู้จัดการฝ่ายบริหารการลงทุน
- ผู้จัดทำ
- ผู้ดูแลระบบฝ่ายบริหารการลงทุน
- ผู้ตรวจสอบ
- ผู้ติดตาม
- ผู้ถูกขอข้อมูล
- ผู้ถูกขอข้อมูลไม่ถูกต้อง
- ผู้ประสานงาน ก
- ผู้ประสานงานบริหารการลงทุน
- ผู้รับผิดชอบ
- ผู้รับผิดชอบที่ได้รับมอบหมาย
- ผู้ส่ง
- ผู้อนุมัติ / รับทราบ
- ฝ่ายกฎหมาย ข
- ฝ่ายกฎหมายบริษัทเป้าหมาย
- ฝ่ายบริหารการลงทุน
- ฝ่ายบัญชีบริษัทเป้าหมาย
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
- มีรายการเกินกำหนด
- ยกเลิก
- ยกเลิกเอกสาร
- ยกเลิกเอกสาร?
- ยกเลิกเอกสารแล้ว ·
- ยังไม่ขอ
- ยังไม่มีข้อมูล
- ยังไม่มีรายการคำขอ
- ยังไม่มีรายการคำขอ — เพิ่มอย่างน้อย 1 รายการก่อนส่งอนุมัติ
- ยังไม่มีรายการคำขอเอกสารและข้อมูล
- ยังไม่ส่ง
- ย้อนกลับ
- รหัสคำขอ
- รอขั้นก่อนหน้า
- รองกรรมการผู้จัดการ
- รอผล
- รอพิจารณา
- รออนุมัติ
- ระบบเลือกตอนส่ง
- ระบุเหตุผล
- รายการ
- รายการคำขอ
- รายการคำขอข้อมูลโครงการ ก.xlsx
- รายการคำขอยังไม่ครบตามขอบเขตการตรวจสอบ
- รายการคำขอเอกสารและข้อมูล
- รายละเอียด
- ร่าง
- ลบคำขอนี้
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ลายเซ็น / อนุมัติ
- ลำดับการอนุมัติ
- ลิงก์เอกสาร
- ล้างตัวกรอง
- วันที่ ........./........./.........
- วันที่ขอ
- วันที่จัดทำ
- วันที่ได้รับ
- วันที่ได้รับต้องไม่ก่อนวันที่ขอ
- วิภา ตัวอย่างงาม
- ศิริพร ข้อมูลจำลอง
- ส.ค.
- สถานะ
- สถานะ ยังไม่ขอ ต้องไม่มีวันที่ได้รับ
- สถานะ ได้รับครบ ต้องระบุวันที่ได้รับ
- สถานะเอกสาร
- สรุปรายการคำขอ
- สร้าง PDF
- สร้างรายการคำขอ
- สร้างรายการเมื่อเริ่มขอข้อมูลของโครงการ
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างโดย
- สลับเป็น
- สัญญาเช่าและสัญญาการค้าสำคัญ
- สายอนุมัติ
- สำนักกรรมการผู้จัดการ
- สิงหาคม
- ส่งกลับ
- ส่งกลับเป็นร่างแล้ว ·
- ส่งอนุมัติ
- ส่งอนุมัติ?
- ส่งอนุมัติแล้ว ·
- ส่งออก
- ส่งแล้วแก้ไขไม่ได้ — ถ้าถูกส่งกลับ จะกลับเป็นร่างเลขเดิมให้แก้แล้วส่งใหม่
- ส่งในระบบ
- หนังสือรับรองบริษัท + บอจ.5
- หน่วยงานภายใน — ฝ่ายวิศวกรรม
- หมายเหตุ
- อนุมัติ
- อนุมัติแล้ว
- อนุมัติแล้ว · รายการคำขอมีผล เริ่มติดตามการรับมอบ
- อรุณี รองตัวอย่าง
- ออกใช้ครั้งแรก
- อา
- เกินกำหนด
- เจ้าของโครงการ
- เจ้าของโครงการ / หน่วยงาน
- เช่น งบการเงิน 3 ปี
- เดือนถัดไป
- เด้งกลับบน
- เพิ่มเติม
- เม.ย.
- เมษายน
- เลขที่
- เลขที่เอกสาร
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกประเทศ
- เลือกผู้พิจารณา
- เลือกวันที่
- เหตุผลที่ยกเลิก
- เอกสาร / ข้อมูลที่ขอ
- เอกสาร ·
- เอกสารแนบ
- เอกสารแนบ (ถ้ามี)
- แก้ไขรายการคำขอ
- แก้ไขร่าง
- แก้ไขล่าสุด
- แก้ไขเอกสาร
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งผู้จัดทำว่าต้องแก้อะไร
- แนบไฟล์ประกอบ เช่น อีเมลขอข้อมูล หรือรายการจากที่ปรึกษา
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบฟอร์ม
- แบบฟอร์มรายการคำขอเอกสารและข้อมูล
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
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
- ใบอนุญาตประกอบกิจการโรงงาน
- ได้รับครบ
- ได้รับครบ / บางส่วน
- ได้รับบางส่วน
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่มี
- ไม่มีรายการเกินกำหนด
- ไม่ยกเลิก
- ไม่อนุมัติ
- ไม่เกี่ยวข้อง
- — คุณเป็นผู้พิจารณาเอกสารนี้

## §10 Data Binding & BACKEND anchors
| จอ | ข้อมูล | anchor |
|---|---|---|
| P-01 | API-01 list (canSee) | `listRows()` · `canSee()` · `summary()` |
| P-02 | API-03/04 body (FRD 02 §2.2) | `persist()` · `validateStep()` · `rowErrors()` · loadDefaults = `POLICY` (code_prefix · usage_note) |
| M-01 | API-05/06 doa-preview/submit | `openSubmit()` · `confirmSubmit()` · DOA-ENGINE-HOOK |
| M-02/03 | API-07 decide | `confirmApprove()` · `confirmReason()` |
| M-04 | API-08 cancel | `openCancel()` |
| P-03 PDF | API-09 · data contract print-spec §8 | `docPrintData()` · `tplRender()` · `tplSignRows()` |
| QA | e2e_standard | window.__QA__ |
markers: {'marker': 'ENG-DOC-NUM', 'line': '/* doc_type IVME — ประกาศใน DOCCFG_BRIEF_F-TMP-007 · เลขรันจาก ENG-DOC-NUM ตอนบันทึกครั้งแรก · เช็คสถานะเปิดใช้ที่ F-DOC'}, {'marker': 'DOA-ENGINE-HOOK', 'line': '/* DOA-ENGINE-HOOK — resolve จาก DOA entry ของ F-TMP-007 ณ เวลาส่ง แล้ว snapshot ลง approval_chain (DOA_BRIEF_F-TMP-007.'}, {'marker': 'TODO', 'line': 'approver_role / approved_by / approval_chain ต่อขั้น · จำนวนขั้นตั้งที่ DOA กลาง (dynamic) — ห้าม fix · TODO: DOA engine'}, {'marker': 'ENG-DOC-NUM', 'line': "/* บันทึกครั้งแรก = ENG-DOC-NUM.next('IVME') ออกเลขที่ (DEC-10) · ผู้จัดทำ snapshot ตำแหน่ง/ฝ่าย + usage_note ณ วันที่บั"}, {'marker': 'ENG-NOTIFY', 'line': '/* ENG-NOTIFY (NTF_BRIEF_F-TMP-007): ivme_request_list_approved → ผู้จัดทำ + admin role (เริ่มส่งคำขอนอกระบบ) · ivme_can'}, {'marker': 'DOA-ENGINE-HOOK', 'line': 'doa: MOCK_DOA_RESOLVED 2 ขั้น (role-line-manager → role-gm) = DOA-ENGINE-HOOK (DOA_BRIEF_F-TMP-007) · คำตัดสินผูก role ·'}, {'marker': 'ENG-DOC-NUM', 'line': "hooks: ENG-DOC-NUM.next('IVME') ตอนบันทึกครั้งแรก · F-DOCCFG status (DOC.active) · DocRequestPolicy (code_prefix · usage"}, {'marker': 'ENG-NOTIFY', 'line': "hooks: ENG-DOC-NUM.next('IVME') ตอนบันทึกครั้งแรก · F-DOCCFG status (DOC.active) · DocRequestPolicy (code_prefix · usage"}

## §11 Traceability + Drift Log
| จอ/ส่วน | FRD | หมายเหตุ |
|---|---|---|
| P-01..P-03 | 01_UI §1.1 | ตรง |
| ขั้น 1 การ์ด | 01_UI §1.2 · FORM_SPEC F01–F11 | ตรง 1:1 (+ F01 ช่องเพิ่ม DEC-06) |
| สถานะ↔วันที่ / ลำดับวันที่ / ปิดรายการ / ลิงก์ | 05 BR-04..09 | ตรง |
| สรุปรายการคำขอ | 05 BR-17 · LD-08 | ค่าคำนวณ ไม่ใช่ช่องกรอก |
Drift: ไม่มี (prototype = source of truth) · คำตัดสินขั้น 1 = ตรวจสอบแล้ว/ส่งกลับ (LD-01) · ไม่มีทำซ้ำ (LD-09)

## §12 Diff จากเวอร์ชันก่อน
เวอร์ชันแรก

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- Phase 2: เลือกโครงการจากทะเบียน (FM-IVM-01) แทนพิมพ์ชื่อ · อัปเดตสถานะการรับมอบหลังอนุมัติ (OQ-07) · แจ้งเตือนผู้รับผิดชอบเมื่อใกล้กำหนดส่ง · ลิงก์เอกสารที่ได้รับไปยังห้องข้อมูล FM-IVM-04
