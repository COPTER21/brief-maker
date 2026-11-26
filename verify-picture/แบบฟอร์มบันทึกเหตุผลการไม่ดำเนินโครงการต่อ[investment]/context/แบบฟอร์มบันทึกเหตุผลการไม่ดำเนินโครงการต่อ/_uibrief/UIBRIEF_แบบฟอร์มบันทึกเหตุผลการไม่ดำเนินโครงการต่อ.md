# UI_BRIEF — F-TMP-002 แบบฟอร์มบันทึกเหตุผลการไม่ดำเนินโครงการต่อ (AS-BUILT)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| Prototype | `01_Prototype/feature.html` (html-generator-v9.4 · Q-form · audit FAIL 0 · self_audit PASS · e2e 21/21) |
| FRD | FRD_F-TMP-002_Pack (01_UI · 05_RULES · 06_TESTS) · BRD-IVM-IVMJ-001 |
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
| #/ivm-discontinue | P-01 รายการ | `renderPage()` |
| #/ivm-discontinue/view/:id | P-03 ดู (drawer 920) | `openView()` |
| #/ivm-discontinue/create · /create/copy-:id | P-02 สร้าง (drawer wide) | `startWizard()` |
| #/ivm-discontinue/edit/:id | P-02 แก้ร่าง | `startWizard()` |
refresh-safe ผ่าน `applyRoute()` · hash เปลี่ยนด้วย `go()`

## §3 Layout Shell
sidebar 232px ดำ (module บริหารการลงทุน › บันทึกไม่ดำเนินโครงการต่อ + badge รอฉันพิจารณา) · shell-bar 52px (breadcrumb · bell · user chip วงกลมรูปคน + เมนูสลับ persona เดโม) · content `#page-content` · `#overlay-root` สำหรับ portal

## §4 Page Anatomy
### P-01 รายการ — `renderPage()`
`.ph` ชื่อเอกสาร + sub (คำอธิบาย + `.ph-count` จำนวน / รออนุมัติ / รอฉันพิจารณา — ไม่มี stat cards U1) · ปุ่ม ส่งออก CSV (`exportCSV()`) + สร้างบันทึก (`startWizard()`) · `.filter-bar` ค้นหา + combobox สถานะ/ผลการพิจารณา + รีเซ็ต (`resetFilters()`) · ตาราง (`sortTh()` · `rowClick()` · kebab `openRowMenu()`) · `pager()` page-size 10/25/50

### P-02 สร้าง/แก้ — `renderWizard()` (drawer `.drawer-panel.wide`)
stepper 3 ขั้น (`stepper()`) · ขั้น 1 `wizMain()`: การ์ด ① ข้อมูลโครงการ (bedate วันที่เสนอ `pickProposed()` · combobox ผู้รับผิดชอบ) ② เหตุผล `reasonCard()` (segmented ใช่/ไม่ใช่ · ช่องรายละเอียดเมื่อ ใช่ · `addReason()` / `removeReason()`) ③ สรุปและปิดงาน (`setResult()` track-card 4 ค่า · ข้อสั่งการ `showInstr()`) · การ์ดสรุปขวา `sumCard()` · ขั้น 2 `wizAttach()` · ขั้น 3 `wizReview()` · footer บันทึกแบบร่าง `saveDraft()` / บันทึกและส่งอนุมัติ `saveAndSubmit()`

### P-03 ดู — `renderViewDrawer()`
header (เลขที่ + pill สถานะ + sub ผลการพิจารณา 1 fact U19 · ปุ่มตามสถานะ + ทำซ้ำ/พิมพ์/ดาวน์โหลด/ปิด) · แท็บ `tabBtn()`: รายละเอียด `renderDetailTab()` · PDF Preview `renderPdfTab()` · ลายเซ็น / อนุมัติ `renderSignTab()` · ประวัติ `renderHistoryTab()`

## §5 Component Inventory
| component | class / fn | ใช้ที่ |
|---|---|---|
| การ์ดเหตุผล | `.trip` · `reasonCard()` | P-02 |
| ตัวเลือกผล | `.track-card` · `.track-grid` | P-02 |
| การ์ดสรุป | `.wz-sum` · `sumCard()` | P-02 |
| ใช่/ไม่ใช่ | `.seg-control` · `.seg-item` | P-02 |
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
- พิมพ์ในช่อง = soft update ไม่ rebuild (focus ไม่หลุด) · `setTop()` · `setSum()` · `setReason()`
- กดถัดไป = `validateMain()` → ช่องแดง + toast · เลือก ใช่/ไม่ใช่ / ผล = render ใหม่
- ส่ง → modal slot ต่อขั้น DOA (`resolveDoa()` · MOCK_DOA_RESOLVED) · อนุมัติเรียงขั้น `confirmApprove()` · ส่งกลับ/ยกเลิก `confirmReason()`
- จำลอง API ล้ม: `commitRejected()` (S.sim) · persona เดโม `switchPersona()`

## §8 State-Driven UI Matrix
| สถานะ | เจ้าของ | ผู้พิจารณาขั้นปัจจุบัน | ผู้ในสายอื่น | admin |
|---|---|---|---|---|
| draft | แก้ไข · ส่งอนุมัติ · ยกเลิก | ไม่เห็น | ไม่เห็น | เห็น (ยกเลิกได้) |
| draft (ถูกส่งกลับ) | แถบแดง "ถูกส่งกลับแก้ไข — เหตุผล" + แก้ไข/ส่ง | ไม่เห็น | ไม่เห็น | เห็น |
| pending | ยกเลิกเอกสาร | ตรวจสอบแล้ว/ส่งกลับ (ขั้น 1) · อนุมัติ/ไม่อนุมัติ + เลือกผล (ขั้นสุดท้าย) | ดูอย่างเดียว | ยกเลิกเอกสาร |
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
- ปุ่ม: + ข้อสั่งการ / เงื่อนไข
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
- ปุ่ม: เพิ่มเหตุผล
- ปุ่ม: แก้ไข
- ปุ่ม: ใช่
- ปุ่ม: ไม่ใช่
- placeholder: ${cond ? 'ต้องระบุเมื่อดำเนินการต่อแบบมีเงื่อนไข' : 'ไม่บังคับ'}
- placeholder: ${ph}
- placeholder: ${rej ? 'แจ้งผู้จัดทำว่าต้องแก้อะไร' : 'เหตุผลที่ยกเลิก'}
- placeholder: ' + ph + '
- placeholder: ค้นหาเลขที่ / ชื่อโครงการ / ผู้จัดทำ
- placeholder: ชื่อโครงการหรือธุรกรรม
- placeholder: เช่น ขั้นตอนที่ 4: การตรวจสอบสถานะ
- placeholder: เหตุผลหลัก — เช่น ผลตอบแทนต่ำกว่าเกณฑ์
- placeholder: ไม่บังคับ
- aria: เดือนก่อน
- aria: เดือนถัดไป
- aria: เลือก
- aria: เหตุผลหลัก

### ข้อความอื่น (จากโค้ด)
- (ขั้น
- + ข้อสั่งการ / เงื่อนไข
- IRR ต่ำกว่าเกณฑ์ขั้นต่ำที่ตั้งไว้
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
- กรุณากรอกข้อมูลให้ครบถ้วน
- กันยายน
- กานต์ ทดลองดี
- กำลังเปิดหน้าต่างพิมพ์ ·
- กุมภาพันธ์
- ขั้นตอนที่ 2: การคัดกรองเบื้องต้น
- ขั้นตอนที่ 3: การวิเคราะห์ความเป็นไปได้
- ขั้นตอนที่ 4: การตรวจสอบสถานะ
- ขั้นตอนที่ 5: การเจรจาเงื่อนไข
- ขั้นตอนที่ยุติ
- ขั้นถัดไป
- ขั้นทดสอบ
- ข้อ
- ข้อมูล / เอกสารที่ใช้ประกอบการตัดสินใจ
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลประกอบยังไม่พอ ขอหลักฐานเพิ่ม
- ข้อมูลหลักบันทึกเหตุผล
- ข้อสั่งการ / เงื่อนไข
- ข้าม
- คน / หน่วยงาน
- คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
- ควรทบทวนเงื่อนไขที่จะพิจารณาใหม่
- ความเสี่ยงทางกฎหมาย
- ความเสี่ยงหลังปิดดีล
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค่าเริ่มต้นจากสายอนุมัติ (DOA กลาง) และผังองค์กร
- ค้นหา...
- ค้นหาเลขที่ / ชื่อโครงการ / ผู้จัดทำ
- จะกลับมาพิจารณาเมื่อ…
- จัดเก็บในห้องข้อมูลโครงการ
- ชนิดไฟล์ไม่รองรับ
- ชลธร ใจทดสอบ
- ชื่อฟังก์ชัน
- ชื่อรายงาน / เอกสาร
- ชื่อโครงการ / ธุรกรรม
- ชื่อโครงการหรือธุรกรรม
- ดาวน์โหลด PDF
- ดำเนินการต่อเมื่อคู่สัญญาลดราคาตามเกณฑ์ภายใน 60 วัน
- ดำเนินการต่อแบบมีเงื่อนไข
- ต.ค.
- ตรวจสอบและยืนยัน
- ตรวจสอบแล้ว
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตัดสินใจดำเนินโครงการต่อ
- ติดตามข้อเสนอราคาใหม่
- ตุลาคม
- ต้อง
- ต้องมีเหตุผลที่เลือก ใช่ อย่างน้อย 1 ข้อ
- ถึง
- ถ้ามี
- ทำซ้ำ
- ทำต่อได้เมื่อทำตามข้อสั่งการ / เงื่อนไข
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ทำอะไร ภายในเมื่อไร
- ทุกผลการพิจารณา
- ทุกสถานะ
- ธ.ค.
- ธันวาคม
- ธีรวัฒน์ ระบบดี
- ธุรกรรมซื้อสินทรัพย์ตัวอย่าง จ
- ธุรกรรมซื้อหุ้นบริษัทตัวอย่าง ข
- ธุรกรรมซื้อหุ้นบริษัทตัวอย่าง ซ
- นิติกร
- บริษัท ตัวอย่าง จำกัด (มหาชน)
- บริษัท ตัวอย่าง จำกัด (มหาชน) และบริษัทในเครือ
- บอกว่าโครงการไหนหยุดที่ขั้นไหน เพราะอะไร แล้วสรุปผลที่เสนอ — ผู้จัดทำและผู้มีอำนาจพิจารณาระบบใส่ให้
- บันทึกการคัดกรอง
- บันทึกซ้ำกับใบเดิม
- บันทึกผล
- บันทึกผิดโครงการ
- บันทึกร่างแล้ว ·
- บันทึกเหตุผลการไม่ดำเนินโครงการต่อ
- ประวัติ
- ประวัติ (append-only)
- ประวิทย์ สมมติกุล
- ประเด็นที่ต้องติดตามในอนาคต
- ปิด
- ผลกระทบ
- ผลการพิจารณา
- ผลการพิจารณา (เสนอ)
- ผลตอบแทนต่ำกว่าเกณฑ์
- ผลตอบแทนไม่ถึงเกณฑ์
- ผลตอบแทนไม่ถึงเกณฑ์และพบประเด็นกฎหมาย
- ผลต่อบริษัท
- ผลที่เสนอ
- ผู้ขายยอมรับเงื่อนไขรับประกัน
- ผู้ขายแก้ไขประเด็นครบ
- ผู้ขายไม่ยอมรับเงื่อนไขรับประกัน
- ผู้จัดการฝ่ายบริหารการลงทุน
- ผู้จัดทำ
- ผู้ตรวจสอบ
- ผู้ประสานงานบริหารการลงทุน
- ผู้มีอำนาจพิจารณา
- ผู้รับผิดชอบ
- ผู้รับผิดชอบโครงการ
- ผู้ส่ง
- ผู้อนุมัติ / รับทราบ
- ฝ่ายกฎหมาย
- ฝ่ายบริหารการลงทุน
- พ.ค.
- พ.ย.
- พบประเด็นกฎหมายที่แก้ไม่ได้ในกรอบเวลา
- พบประเด็นจากการตรวจสอบสถานะ
- พบภาระผูกพันที่ไม่ได้เปิดเผย
- พบภาระผูกพันและเงื่อนไขสัญญาไม่ยอมรับได้
- พฤ
- พฤศจิกายน
- พฤษภาคม
- พักโครงการ
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
- ยังไม่มีบันทึกเหตุผลการไม่ดำเนินโครงการต่อ
- ยังไม่มีเหตุผล
- ยังไม่ส่ง
- ยุติโครงการ ปิดงานและจัดเก็บเอกสาร
- ย้อนกลับ
- รอขั้นก่อนหน้า
- รองกรรมการผู้จัดการ
- รอผล
- รอพิจารณา
- รออนุมัติ
- ระบบกำหนดจากสายอนุมัติเมื่อส่ง
- ระบบเลือกตอนส่ง
- ราคาซื้อขายลดลงตามเกณฑ์
- รายการ
- รายงานตรวจสอบสถานะ
- รายงานตรวจสอบสถานะ · ร่างสัญญา
- รายงานประเมินมูลค่า
- รายงานประเมินมูลค่า · รายงานตรวจสอบสถานะ
- รายงานประเมินมูลค่า โครงการ ก.pdf
- รายละเอียด
- รายละเอียดประกอบ
- ร่าง
- ร่างสัญญา · บันทึกการเจรจา
- ร่างสัญญา · แบบจำลองทางการเงิน
- ร่างสัญญาฉบับล่าสุด
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ลายเซ็น / อนุมัติ
- ลำดับการอนุมัติ
- ล้างตัวกรอง
- วันที่ ........./........./.........
- วันที่เสนอ
- วันที่เสนอไม่ดำเนินการต่อ
- วิภา ตัวอย่างงาม
- ศิริพร ข้อมูลจำลอง
- ส.ค.
- สถานะ
- สถานะเอกสาร
- สรุปเหตุผล
- สรุปเหตุผลหลักในประโยคเดียว
- สร้าง PDF
- สร้างบันทึก
- สร้างบันทึกเมื่อเสนอไม่ดำเนินโครงการหรือธุรกรรมต่อ
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างโดย
- สลับเป็น
- สำนักกรรมการผู้จัดการ
- สิงหาคม
- ส่งกลับ
- ส่งกลับเป็นร่างแล้ว ·
- ส่งกลับให้ทบทวนข้อมูลก่อนตัดสิน
- ส่งอนุมัติ
- ส่งอนุมัติแล้ว ·
- ส่งออก
- ส่งแล้วแก้ไขไม่ได้ — ถ้าถูกส่งกลับ จะกลับเป็นร่างเลขเดิมให้แก้แล้วส่งใหม่
- ส่งในระบบ
- หมายเหตุ
- หยุดไว้ก่อน รอเงื่อนไขที่จะพิจารณาใหม่
- หลักฐานอ้างอิง
- อธิบายสั้น ๆ
- อนุมัติ
- อนุมัติแล้ว
- อนุมัติแล้ว ·
- อนุมัติไม่ดำเนินการต่อ
- อรุณี รองตัวอย่าง
- ออกใช้ครั้งแรก
- อา
- เก็บไว้ที่ไหน ในห้องข้อมูล / ไดรฟ์ส่วนกลาง
- เงื่อนไขที่จะพิจารณาใหม่
- เงื่อนไขสัญญาและผลตอบแทนไม่ถึงเกณฑ์
- เงื่อนไขสัญญาไม่ยอมรับได้
- เงื่อนไขสัญญาไม่เป็นที่ยอมรับ
- เจรจาแล้ว 3 รอบ
- เจ้าหน้าที่ดูแลเอกสารการลงทุน
- เช่น ขั้นตอนที่ 4: การตรวจสอบสถานะ
- เช่น รายงานประเมินมูลค่า · รายงานตรวจสอบสถานะ
- เช่น รายงานประเมินมูลค่า รายงานตรวจสอบสถานะ หรือบันทึกการประชุม
- เดือนถัดไป
- เด้งกลับบน
- เพิ่มเติม
- เม.ย.
- เมษายน
- เลขที่
- เลขที่เอกสาร
- เลือก
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือก ใช่ ต้องมีรายละเอียดประกอบ
- เลือกประเทศ
- เลือกผู้พิจารณา
- เลือกผู้รับผิดชอบ
- เลือกวันที่
- เหตุผลที่ยกเลิก
- เหตุผลที่เลือก ใช่
- เหตุผลยังไม่ชัดเจน
- เหตุผลหลัก
- เหตุผลหลัก — เช่น ผลตอบแทนต่ำกว่าเกณฑ์
- เอกสารแนบ
- แก้ไขบันทึก
- แก้ไขร่าง
- แก้ไขล่าสุด
- แก้ไขเอกสาร
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งผู้จัดทำว่าต้องแก้อะไร
- แนบเอกสารประกอบ (ถ้ามี)
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แนวทางจัดเก็บเอกสารและปิดงาน
- แบบจำลองทางการเงิน
- แบบฟอร์ม
- แบบฟอร์มบันทึกเหตุผลการไม่ดำเนินโครงการต่อ
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
- ใช่
- ใส่เหตุผลหลัก
- ใส่เหตุผลหลักและรายละเอียดประกอบ
- ให้ทบทวนข้อมูลเพิ่มเติม
- ไม่คุ้มค่าการลงทุน
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่มีข้อมูล
- ไม่ยกเลิก
- ไม่สอดคล้องกลยุทธ์
- ไม่สอดคล้องกลยุทธ์ปีนี้
- ไม่อนุมัติ
- ไม่ใช่
- — คุณเป็นผู้พิจารณาบันทึกนี้

## §10 Data Binding & BACKEND anchors
| จอ | ข้อมูล | anchor |
|---|---|---|
| P-01 | API-01 list (canSee) | `listRows()` · `canSee()` |
| P-02 | API-03/04 body (FRD 02 §2.2) | `persist()` · `validateMain()` |
| M-01 | API-05/06 doa-preview/submit | `openSubmit()` · `confirmSubmit()` · DOA-ENGINE-HOOK |
| M-02/03 | API-07 decide (result/instruction ขั้นสุดท้าย) | `confirmApprove()` · `confirmReason()` |
| M-04 | API-08 cancel | `openCancel()` |
| P-03 PDF | API-09 · data contract print-spec §8 | `docPrintData()` · `tplRender()` · `tplSignRows()` |
| QA | e2e_standard | window.__QA__ |
markers: {'marker': 'ENG-DOC-NUM', 'line': '/* doc_type IVMJ — ประกาศใน DOCCFG_BRIEF_F-TMP-002 · เลขรันจาก ENG-DOC-NUM ตอนบันทึกครั้งแรก · เช็คสถานะเปิดใช้ที่ F-DOC'}, {'marker': 'DOA-ENGINE-HOOK', 'line': '/* DOA-ENGINE-HOOK — resolve จาก DOA entry ของ F-TMP-002 ณ เวลาส่ง แล้ว snapshot ลง approval_chain (DOA_BRIEF_F-TMP-002.'}, {'marker': 'ENG-DOC-NUM', 'line': "/* บันทึกครั้งแรก = ENG-DOC-NUM.next('IVMJ') ออกเลขที่ (DEC-10) · ผู้จัดทำ snapshot ตำแหน่ง/ฝ่าย ณ วันที่บันทึก */"}, {'marker': 'ENG-NOTIFY', 'line': '/* ENG-NOTIFY (NTF_BRIEF_F-TMP-002): ivmj_result_recorded → ผู้รับผิดชอบ · ivmj_cancelled → ผู้พิจารณาขั้นปัจจุบัน · DOA'}, {'marker': 'DOA-ENGINE-HOOK', 'line': 'doa: MOCK_DOA_RESOLVED 2 ขั้น (role-line-manager → role-gm) = DOA-ENGINE-HOOK (DOA_BRIEF_F-TMP-002) · คำตัดสินผูก role ·'}, {'marker': 'ENG-DOC-NUM', 'line': "hooks: ENG-DOC-NUM.next('IVMJ') ตอนบันทึกครั้งแรก · F-DOCCFG status (DOC.active) · ENG-NOTIFY ivmj_result_recorded / ivm"}, {'marker': 'ENG-NOTIFY', 'line': "hooks: ENG-DOC-NUM.next('IVMJ') ตอนบันทึกครั้งแรก · F-DOCCFG status (DOC.active) · ENG-NOTIFY ivmj_result_recorded / ivm"}

## §11 Traceability + Drift Log
| จอ/ส่วน | FRD | หมายเหตุ |
|---|---|---|
| P-01..P-03 | 01_UI §1.1 | ตรง |
| การ์ด ①②③ | 01_UI §1.2 · FORM_SPEC F01–F19 | ตรง 1:1 |
| M-02 เลือกผล | 05 BR-03/04 | ตรง |
Drift: ไม่มี (prototype = source of truth) · คำตัดสินขั้น 1 เปลี่ยนเป็น ตรวจสอบแล้ว/ส่งกลับ (LD-01)

## §12 Diff จากเวอร์ชันก่อน
เวอร์ชันแรก

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- Phase 2: เลือกโครงการจากทะเบียน (FM-IVM-01) แทนพิมพ์ชื่อ · ปุ่มส่งต่อ FM-IVM-11 ปิดงาน · แจ้งเตือนประเด็นติดตามตามวันที่
