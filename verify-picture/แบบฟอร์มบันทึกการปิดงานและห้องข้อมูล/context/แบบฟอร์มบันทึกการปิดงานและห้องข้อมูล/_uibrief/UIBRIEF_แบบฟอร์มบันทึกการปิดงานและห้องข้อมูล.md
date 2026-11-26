# UI_BRIEF — F-TMP-003 แบบฟอร์มบันทึกการปิดงานและห้องข้อมูล (AS-BUILT)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| Prototype | `01_Prototype/feature.html` (html-generator-v9.4 · Q-form · audit FAIL 0 · self_audit PASS · e2e ยังไม่รัน [NO-BROWSER] · jsdom smoke 22/22) |
| FRD | FRD_F-TMP-003_Pack (01_UI · 05_RULES · 06_TESTS) · BRD-IVM-IVMK-001 |
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
| #/ivm-closing | P-01 รายการ | `renderPage()` |
| #/ivm-closing/view/:id | P-03 ดู (drawer 920) | `openView()` |
| #/ivm-closing/create · /create/copy-:id | P-02 สร้าง (drawer wide) | `startWizard()` |
| #/ivm-closing/edit/:id | P-02 แก้ร่าง | `startWizard()` |
refresh-safe ผ่าน `applyRoute()` · hash เปลี่ยนด้วย `go()`

## §3 Layout Shell
sidebar 232px ดำ (module บริหารการลงทุน › บันทึกปิดงานและห้องข้อมูล + badge รอฉันพิจารณา) · shell-bar 52px (breadcrumb · bell · user chip วงกลมรูปคน + เมนูสลับ persona เดโม) · content `#page-content` · `#overlay-root` สำหรับ portal

## §4 Page Anatomy
### P-01 รายการ — `renderPage()`
`.ph` ชื่อเอกสาร + sub (คำอธิบาย + `.ph-count` จำนวน / รออนุมัติ / รอฉันพิจารณา — ไม่มี stat cards U1) · ปุ่ม ส่งออก CSV (`exportCSV()`) + สร้างบันทึก (`startWizard()`) · `.filter-bar` ค้นหา + combobox สถานะ/ความครบของรายการตรวจสอบ + รีเซ็ต (`resetFilters()`) · ตาราง (`sortTh()` · `rowClick()` · kebab `openRowMenu()`) · `pager()` page-size 10/25/50

### P-02 สร้าง/แก้ — `renderWizard()` (drawer `.drawer-panel.wide`)
stepper 3 ขั้น (`stepper()`) · ขั้น 1 `wizMain()`: การ์ด ① สรุปการปิดงาน (bedate วันที่ปิดงาน `pickClose()` · combobox ผู้รับผิดชอบหลังปิดงาน) ② รายการตรวจสอบ 8 การ์ด `checkCard()` (segmented สถานะ 4 ค่า `setCheck()` · แล้วเสร็จ = ผู้รับผิดชอบ + bedate วันที่ดำเนินการ `pickChk{i}()` · ไม่เกี่ยวข้อง = หมายเหตุ · แถบแดงกติกาส่ง) ③ บทเรียน `lessonCard()` (`addLesson()` / `removeLesson()` · bedate กำหนดส่ง `pickLes{i}()`) · การ์ดสรุปขวา `sumCard()` · ขั้น 2 `wizAttach()` · ขั้น 3 `wizReview()` · footer บันทึกแบบร่าง `saveDraft()` / บันทึกและส่งอนุมัติ `saveAndSubmit()`

### P-03 ดู — `renderViewDrawer()`
header (เลขที่ + pill สถานะ + sub วันที่ปิดงาน 1 fact U19 · ปุ่มตามสถานะ + ทำซ้ำ/พิมพ์/ดาวน์โหลด/ปิด) · แท็บ `tabBtn()`: รายละเอียด `renderDetailTab()` · PDF Preview `renderPdfTab()` · ลายเซ็น / อนุมัติ `renderSignTab()` · ประวัติ `renderHistoryTab()`

## §5 Component Inventory
| component | class / fn | ใช้ที่ |
|---|---|---|
| การ์ดรายการตรวจสอบ | `.trip` · `checkCard()` · `.ck-item` | P-02 |
| การ์ดบทเรียน | `.trip` · `lessonCard()` | P-02 |
| การ์ดสรุป | `.wz-sum` · `sumCard()` | P-02 |
| สถานะรายการ | `.seg-control` · `.seg-item` | P-02 |
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
- พิมพ์ในช่อง = soft update ไม่ rebuild (focus ไม่หลุด) · `setTop()` · `setCheck()` · `setLesson()` · `softSum()`
- กดถัดไป/บันทึกร่าง = `validateMain(false)` · บันทึกและส่ง = `validateMain(true)` + `submitGaps()` → ช่องแดง + แถบ + toast · เปลี่ยนสถานะรายการ = render ใหม่ · ส่งจาก view = `openSubmit()` ตรวจ `submitGaps()` ก่อนเปิด modal
- ส่ง → modal slot ต่อขั้น DOA (`resolveDoa()` · MOCK_DOA_RESOLVED) · อนุมัติเรียงขั้น `confirmApprove()` · ส่งกลับ/ยกเลิก `confirmReason()`
- จำลอง API ล้ม: `commitRejected()` (S.sim) · persona เดโม `switchPersona()`

## §8 State-Driven UI Matrix
| สถานะ | เจ้าของ | ผู้พิจารณาขั้นปัจจุบัน | ผู้ในสายอื่น | admin |
|---|---|---|---|---|
| draft | แก้ไข · ส่งอนุมัติ (บล็อกถ้ารายการไม่ครบ + แถบบอกสิ่งที่ขาด) · ยกเลิก | ไม่เห็น | ไม่เห็น | เห็น (ยกเลิกได้) |
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
- ยังส่งอนุมัติไม่ได้ —
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
- ปุ่ม: เพิ่มบทเรียน
- ปุ่ม: แก้ไข
- placeholder: ${ph}
- placeholder: ${rej ? 'แจ้งผู้จัดทำว่าต้องแก้อะไร' : 'เหตุผลที่ยกเลิก'}
- placeholder: ' + ph + '
- placeholder: คน / หน่วยงาน
- placeholder: ค้นหาเลขที่ / ชื่อโครงการ / ผู้จัดทำ / ที่จัดเก็บ
- placeholder: ชื่อโครงการหรือธุรกรรม
- placeholder: ประเด็น — เช่น การจัดเตรียมห้องข้อมูล
- placeholder: เกิดอะไร ครั้งหน้าควรทำอย่างไร
- placeholder: เช่น ลงนามสัญญาและโอนหุ้นครบถ้วน
- placeholder: เช่น ห้องข้อมูลโครงการ / 99_ปิดงาน หรือไดรฟ์ส่วนกลาง
- placeholder: ไม่บังคับ
- aria: ประเด็น
- aria: สถานะ
- aria: เดือนก่อน
- aria: เดือนถัดไป

### ข้อความอื่น (จากโค้ด)
- "บันทึกบทเรียนที่ได้รับ" แล้วเสร็จ ต้องมีบทเรียน ≥ 1 แถว
- (ขั้น
- : inp('owner', 'ผู้รับผิดชอบ', 'คน / หน่วยงาน') + inp('remark', 'หมายเหตุ', 'ถ้ามี'); return
- ; const fields = st === 'done' ? inp('owner', 'ผู้รับผิดชอบ', 'คน / หน่วยงาน', true) + date +
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
- การจัดเตรียมห้องข้อมูล
- การตอบคำถามผู้ซื้อ
- การส่งต่อประเด็นกฎหมาย
- กำลังดำเนินการ
- กำลังเปิดหน้าต่างพิมพ์ ·
- กำหนดผู้ตอบหลักต่อหมวดช่วยลดเวลาตอบลงครึ่งหนึ่ง
- กำหนดโครงโฟลเดอร์และสิทธิก่อนเปิดห้องข้อมูล ลดคำขอเอกสารซ้ำ
- กุมภาพันธ์
- ขั้นถัดไป
- ขั้นทดสอบ
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลหลักบันทึกปิดงาน
- ข้าม
- คน / หน่วยงาน
- ครบตามกติกา ส่งอนุมัติได้
- ครบทุกข้อ
- คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค่าเริ่มต้นจากสายอนุมัติ (DOA กลาง) และผังองค์กร
- ค้นหา...
- ค้นหาเลขที่ / ชื่อโครงการ / ผู้จัดทำ / ที่จัดเก็บ
- จัดตั้งบริษัทร่วมทุนแล้ว ส่งมอบงานให้ฝ่ายปฏิบัติการ
- จัดเก็บบันทึกสิทธิการเข้าถึงฉบับปิดงาน
- ชนิดไฟล์ไม่รองรับ
- ชลธร ใจทดสอบ
- ชำระราคาและโอนหุ้นครบ
- ชื่อฟังก์ชัน
- ชื่อโครงการ / ธุรกรรม
- ชื่อโครงการหรือธุรกรรม
- ดาวน์โหลด PDF
- ดำเนินการคืนหรือทำลายข้อมูลตามสัญญารักษาความลับ (ถ้ามี)
- ต.ค.
- ตรวจสอบและยืนยัน
- ตรวจสอบแล้ว
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตุลาคม
- ต้อง
- ถึง
- ถ้ามี
- ทะเบียนเอกสารห้องข้อมูล ฉบับปิดงาน โครงการ ก.xlsx
- ทำซ้ำ
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ทุกความครบของรายการ
- ทุกสถานะ
- ธ.ค.
- ธันวาคม
- ธีรวัฒน์ ระบบดี
- ธุรกรรมซื้อสินทรัพย์ตัวอย่าง จ
- ธุรกรรมซื้อหุ้นบริษัทตัวอย่าง ข
- ธุรกรรมซื้อหุ้นบริษัทตัวอย่าง ซ
- ธุรกรรมยังไม่ปิดจริง
- ธุรกรรมยังไม่ปิดจริง — รอโอนสินทรัพย์งวดสุดท้าย
- นิติกร
- บทเรียน
- บทเรียน (แถว)
- บริษัท ตัวอย่าง จำกัด (มหาชน)
- บริษัท ตัวอย่าง จำกัด (มหาชน) และบริษัทในเครือ
- บันทึกการปิดงานและห้องข้อมูล
- บันทึกซ้ำกับใบเดิม
- บันทึกบทเรียนที่ได้รับ
- บันทึกผล
- บันทึกผิดโครงการ
- บันทึกร่างแล้ว ·
- ประวัติ
- ประวัติ (append-only)
- ประวิทย์ สมมติกุล
- ประเด็น
- ประเด็น ข้อสังเกต / บทเรียน ผู้รับผิดชอบ กำหนดส่ง
- ประเด็น — เช่น การจัดเตรียมห้องข้อมูล
- ปรับหรือยกเลิกสิทธิของผู้เกี่ยวข้อง
- ปิด
- ปิดงานสมบูรณ์ · แจ้งผู้รับผิดชอบหลังปิดงาน
- ปิดธุรกรรมซื้อหุ้นโรงไฟฟ้าตามสัญญา
- ปิดธุรกรรมตามสัญญา
- ปิดธุรกรรมตามสัญญา ชำระราคาครบ
- ปิดหรือส่งต่อประเด็นคงค้าง
- ผลลัพธ์ของธุรกรรม
- ผู้จัดการฝ่ายบริหารการลงทุน
- ผู้จัดทำ
- ผู้ดูแลห้องข้อมูล
- ผู้ตรวจสอบ
- ผู้ประสานงานบริหารการลงทุน
- ผู้รับผิดชอบหลังปิดงาน
- ผู้รับผิดชอบโครงการ
- ผู้ส่ง
- ผู้อนุมัติ / รับทราบ
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
- ยกเลิก
- ยกเลิกเอกสาร
- ยกเลิกเอกสาร?
- ยกเลิกเอกสารแล้ว ·
- ยังมีประเด็นคงค้างที่ไม่ได้ส่งต่อ
- ยังส่งอนุมัติไม่ได้ —
- ยังส่งอนุมัติไม่ได้ — บันทึกร่างได้
- ยังไม่ครบ
- ยังไม่ดำเนินการ
- ยังไม่มีข้อมูล
- ยังไม่มีบทเรียนที่บันทึก
- ยังไม่มีบันทึกการปิดงานและห้องข้อมูล
- ยังไม่มีรายการตรวจสอบ
- ยังไม่ส่ง
- ยืนยันชุดเอกสารฉบับสมบูรณ์ครบถ้วน
- ยืนยันสถานที่จัดเก็บถาวร
- ยุติธุรกรรม ไม่ดำเนินการต่อ
- ย้อนกลับ
- รอขั้นก่อนหน้า
- รองกรรมการผู้จัดการ
- รอผล
- รอพิจารณา
- รออนุมัติ
- ระบบเลือกตอนส่ง
- รับโอนสินทรัพย์และจดทะเบียนกรรมสิทธิ์แล้ว
- รายการ
- รายการตรวจสอบ
- รายการตรวจสอบ (เสร็จ/ทั้งหมด)
- รายการตรวจสอบยังไม่ครบหลักฐาน
- รายละเอียด
- ร่าง
- ลงนามสัญญาซื้อขายหุ้นและโอนหุ้นครบถ้วน
- ลงนามสัญญาและโอนหุ้นแล้ว
- ลงนามสัญญาแล้ว
- ลงนามสัญญาแล้ว ส่งมอบงานหลังปิดให้ฝ่ายปฏิบัติการ
- ลบบทเรียนนี้
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ลายเซ็น / อนุมัติ
- ลำดับการอนุมัติ
- ล้างตัวกรอง
- วันที่ ........./........./.........
- วันที่ดำเนินการต้องไม่เกินวันที่ปิดงาน
- วันที่ปิดงาน
- วิภา ตัวอย่างงาม
- ศิริพร ข้อมูลจำลอง
- ส.ค.
- สถานที่จัดเก็บถาวรยังไม่ชัดเจน
- สถานที่จัดเก็บเอกสารถาวร
- สถานะ
- สถานะเอกสาร
- สรุปว่าธุรกรรมไหนปิดเมื่อไร เก็บเอกสารไว้ที่ไหน แล้วไล่รายการตรวจสอบทีละข้อ — ผู้จัดทำและสายอนุมัติระบบใส่ให้
- สร้าง PDF
- สร้างบันทึก
- สร้างบันทึกเมื่อธุรกรรมปิดงานและต้องจัดเก็บห้องข้อมูล
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างโดย
- สลับเป็น
- สำนักกรรมการผู้จัดการ
- สิงหาคม
- ส่งกลับ
- ส่งกลับเป็นร่างแล้ว ·
- ส่งประเด็นคงค้างให้ฝ่ายกฎหมายพร้อมสรุปภายในวันปิดงาน
- ส่งอนุมัติ
- ส่งอนุมัติ?
- ส่งอนุมัติแล้ว ·
- ส่งออก
- ส่งออกและจัดเก็บห้องข้อมูลฉบับสมบูรณ์
- ส่งแล้วแก้ไขไม่ได้ — ถ้าถูกส่งกลับ จะกลับเป็นร่างเลขเดิมให้แก้แล้วส่งใหม่
- ส่งในระบบ
- หมายเหตุ
- หมายเหตุ (เหตุที่ไม่เกี่ยวข้อง)
- ห้องข้อมูลโครงการ ก / 99_ปิดงาน
- ห้องข้อมูลโครงการ ค / 99_ปิดงาน
- ห้องข้อมูลโครงการ จ / 99_ปิดงาน
- ห้องข้อมูลโครงการ ฉ / 99_ปิดงาน
- ห้องข้อมูลโครงการ ช / 99_ปิดงาน
- ห้องข้อมูลโครงการ ฌ
- ห้องข้อมูลโครงการ ญ / 99_ปิดงาน
- ห้องข้อมูลโครงการ ฎ / 99_ปิดงาน
- อนุมัติ
- อนุมัติแล้ว
- อนุมัติแล้ว · ปิดงานสมบูรณ์
- อรุณี รองตัวอย่าง
- ออกใช้ครั้งแรก
- อา
- เจ้าหน้าที่ดูแลเอกสารการลงทุน
- เช่น ห้องข้อมูลโครงการ / 99_ปิดงาน หรือไดรฟ์ส่วนกลาง
- เช่น ไม่มีสัญญารักษาความลับกับคู่สัญญา
- เดือนถัดไป
- เด้งกลับบน
- เพิ่มเติม
- เม.ย.
- เมษายน
- เมื่ออนุมัติ
- เลขที่
- เลขที่เอกสาร
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกประเทศ
- เลือกผู้พิจารณา
- เลือกผู้รับผิดชอบ
- เลือกวันที่
- เลือกวันที่ดำเนินการ
- เหตุผลที่ยกเลิก
- เอกสารแนบ
- แก้ไขบันทึก
- แก้ไขร่าง
- แก้ไขล่าสุด
- แก้ไขเอกสาร
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งผู้จัดทำว่าต้องแก้อะไร
- แถว
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบฟอร์ม
- แบบฟอร์มบันทึกการปิดงานและห้องข้อมูล
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- แล้วเสร็จ
- โครงการ / ธุรกรรม
- โครงการขยายกำลังผลิตตัวอย่าง ง
- โครงการพลังงานตัวอย่าง ช
- โครงการร่วมทุนตัวอย่าง ค
- โครงการลงทุนตัวอย่าง ก
- โครงการลงทุนตัวอย่าง ฉ
- โครงการลงทุนตัวอย่าง ฌ
- โครงการลงทุนตัวอย่าง ญ
- โครงการลงทุนตัวอย่าง ฎ
- ใส่ข้อสังเกต / บทเรียน
- ใส่ประเด็น
- ใส่ผู้รับผิดชอบ
- ไดรฟ์ส่วนกลาง / ธุรกรรม ข / ปิดงาน
- ไดรฟ์ส่วนกลาง / ธุรกรรม ซ / ปิดงาน
- ไดรฟ์ส่วนกลาง / โครงการ ง
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่ยกเลิก
- ไม่อนุมัติ
- ไม่เกี่ยวข้อง
- ไม่เกี่ยวข้อง ต้องระบุหมายเหตุ
- — คุณเป็นผู้พิจารณาบันทึกนี้

## §10 Data Binding & BACKEND anchors
| จอ | ข้อมูล | anchor |
|---|---|---|
| P-01 | API-01 list (canSee) | `listRows()` · `canSee()` |
| P-02 | API-03/04 body (FRD 02 §2.2) · API-12 checklist-template | `persist()` · `validateMain()` · `CHECKLIST_CFG` |
| M-01 | API-05/06 doa-preview/submit | `openSubmit()` · `confirmSubmit()` · DOA-ENGINE-HOOK |
| M-02/03 | API-07 decide | `confirmApprove()` · `confirmReason()` |
| M-04 | API-08 cancel | `openCancel()` |
| P-03 PDF | API-09 · data contract print-spec §8 | `docPrintData()` · `tplRender()` · `tplSignRows()` |
| QA | e2e_standard | window.__QA__ |
markers: {'marker': 'ENG-DOC-NUM', 'line': '/* doc_type IVMK — ประกาศใน DOCCFG_BRIEF_F-TMP-003 · เลขรันจาก ENG-DOC-NUM ตอนบันทึกครั้งแรก · เช็คสถานะเปิดใช้ที่ F-DOC'}, {'marker': 'DOA-ENGINE-HOOK', 'line': '/* DOA-ENGINE-HOOK — resolve จาก DOA entry ของ F-TMP-003 ณ เวลาส่ง แล้ว snapshot ลง approval_chain (DOA_BRIEF_F-TMP-003.'}, {'marker': 'TODO', 'line': 'approver_role / approved_by / approval_chain ต่อขั้น · จำนวนขั้นตั้งที่ DOA กลาง (dynamic) — ห้าม fix · TODO: DOA engine'}, {'marker': 'ENG-DOC-NUM', 'line': "/* บันทึกครั้งแรก = ENG-DOC-NUM.next('IVMK') ออกเลขที่ (G9) · ผู้จัดทำ snapshot ตำแหน่ง/ฝ่าย ณ วันที่บันทึก */"}, {'marker': 'ENG-NOTIFY', 'line': '/* ENG-NOTIFY (NTF_BRIEF_F-TMP-003): ivmk_closed_handover → ผู้รับผิดชอบหลังปิดงาน + ผู้รับผิดชอบรายการ · ivmk_lesson_as'}, {'marker': 'ENG-NOTIFY', 'line': '/* อนุมัติครบ: ไม่เปลี่ยนค่าในระบบ ไม่ส่งต่อระบบอื่น (G1) — เก็บผลในเอกสาร · ENG-NOTIFY ivmk_closed_handover + ivmk_less'}, {'marker': 'DOA-ENGINE-HOOK', 'line': 'doa: MOCK_DOA_RESOLVED 2 ขั้น (role-line-manager → role-gm) = DOA-ENGINE-HOOK (DOA_BRIEF_F-TMP-003) · คำตัดสินผูก role ·'}, {'marker': 'TODO', 'line': 'doa: MOCK_DOA_RESOLVED 2 ขั้น (role-line-manager → role-gm) = DOA-ENGINE-HOOK (DOA_BRIEF_F-TMP-003) · คำตัดสินผูก role ·'}, {'marker': 'ENG-DOC-NUM', 'line': "hooks: ENG-DOC-NUM.next('IVMK') ตอนบันทึกครั้งแรก · F-DOCCFG status (DOC.active) · ENG-NOTIFY ivmk_closed_handover / ivm"}, {'marker': 'ENG-NOTIFY', 'line': "hooks: ENG-DOC-NUM.next('IVMK') ตอนบันทึกครั้งแรก · F-DOCCFG status (DOC.active) · ENG-NOTIFY ivmk_closed_handover / ivm"}

## §11 Traceability + Drift Log
| จอ/ส่วน | FRD | หมายเหตุ |
|---|---|---|
| P-01..P-03 | 01_UI §1.1 | ตรง |
| การ์ด ①②③ | 01_UI §1.2 · FORM_SPEC F01–F14 | ตรง 1:1 |
| กติกาส่ง | 05 BR-02..05 | ตรง |
Drift: ไม่มี (prototype = source of truth) · คำตัดสินขั้น 1 = ตรวจสอบแล้ว/ส่งกลับ (LD-01)

## §12 Diff จากเวอร์ชันก่อน
เวอร์ชันแรก

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- Phase 2: เลือกโครงการ/ห้องข้อมูลจากทะเบียน (FM-IVM-01/04) แทนพิมพ์ · ดึงประเด็นคงค้างจาก FM-IVM-03 · แจ้งเตือนบทเรียนเลยกำหนดส่ง
