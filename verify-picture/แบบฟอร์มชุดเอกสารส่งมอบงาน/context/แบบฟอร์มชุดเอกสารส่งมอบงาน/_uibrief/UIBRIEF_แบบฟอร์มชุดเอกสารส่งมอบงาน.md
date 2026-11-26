# UI_BRIEF — F-TMP-008 แบบฟอร์มชุดเอกสารส่งมอบงาน (AS-BUILT)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| Prototype | `01_Prototype/feature.html` (html-generator-v9.4 · Q-form · audit FAIL 0 · self_audit PASS · smoke jsdom 53/53 (NO-BROWSER)) |
| FRD | FRD_F-TMP-008_Pack (01_UI · 05_RULES · 06_TESTS) · BRD-IVM-IVMF-001 |
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
| #/ivm-handover | P-01 รายการ | `renderPage()` |
| #/ivm-handover/view/:id | P-03 ดู (drawer 920) | `openView()` |
| #/ivm-handover/create | P-02 สร้าง (drawer wide) | `startWizard()` |
| #/ivm-handover/edit/:id | P-02 แก้ร่าง | `startWizard()` |
refresh-safe ผ่าน `applyRoute()` · hash เปลี่ยนด้วย `go()`

## §3 Layout Shell
sidebar 232px ดำ (module บริหารการลงทุน › ชุดเอกสารส่งมอบงาน + badge รอฉันพิจารณา) · shell-bar 52px (breadcrumb · bell · user chip วงกลมรูปคน + เมนูสลับ persona เดโม) · content `#page-content` · `#overlay-root` สำหรับ portal

## §4 Page Anatomy
### P-01 รายการ — `renderPage()`
`.ph` ชื่อเอกสาร + sub (คำอธิบาย + `.ph-count` จำนวน / รออนุมัติ / รอฉันพิจารณา — ไม่มี stat cards U1) · ปุ่ม ส่งออก CSV (`exportCSV()`) + สร้างแบบฟอร์ม (`startWizard()`) · `.filter-bar` ค้นหา + combobox สถานะ/ผลการรับมอบ + รีเซ็ต (`resetFilters()`) · ตาราง (`sortTh()` · `rowClick()` · kebab `openRowMenu()`) · `pager()` page-size 10/25/50

### P-02 สร้าง/แก้ — `renderWizard()` (drawer `.drawer-panel.wide`)
stepper 3 ขั้น (`stepper()`) · ขั้น 1 `wizMain()`: การ์ด ① ข้อมูลการรับมอบ (`fieldTop()` · `setTop()` · วันที่ `bdCell()` + เวลา HH:mm · ผลการรับมอบ select + "ระบบแนะนำ" `resultHint()`) ② ผลการตรวจรับเอกสาร `itemEditor()` (ตารางกรอก · ลำดับระบบรัน · select ได้รับแล้ว/ความครบถ้วน `optSel()` (ไม่ได้รับ → ครบถ้วน disabled) · กำหนดส่ง bedate · `addItem()` / `removeItem()`) ③ ประเด็นค้างและข้อตกลงการติดตาม (`setFu()` · ดอกจันตามผลการรับมอบ) · การ์ดสรุปขวา `sumCard()` (ระบบแนะนำ + เตือน `resultWarn()`) · ขั้น 2 `wizAttach()` · ขั้น 3 `wizReview()` · footer บันทึกแบบร่าง `saveDraft()` / บันทึกและส่งอนุมัติ `saveAndSubmit()`

### P-03 ดู — `renderViewDrawer()`
header (เลขที่ + pill สถานะ + sub ผลการรับมอบ · เอกสารครบ x/y U19 · ปุ่มตามสถานะ + พิมพ์/ดาวน์โหลด/ปิด) · แท็บ `tabBtn()`: รายละเอียด `renderDetailTab()` · PDF Preview `renderPdfTab()` · ลายเซ็น / อนุมัติ `renderSignTab()` · ประวัติ `renderHistoryTab()`

## §5 Component Inventory
| component | class / fn | ใช้ที่ |
|---|---|---|
| ตารางกรอกแถวซ้ำ | `.ed-tbl` · `itemEditor()` | P-02 |
| ตารางแสดง | `itemTable()` · `fuFields()` | P-02/P-03 |
| การ์ดสรุป | `.wz-sum` · `sumCard()` | P-02 |
| ตัวเลือก | `optSel()` · `RES` / `REC` / `CMP` pill | P-02/P-03 |
| คน | `.emp-chip` · `.emp-av` · `empChip()` · `nameChip()` | ทุกจอ |
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
- พิมพ์ในช่อง = soft update ไม่ rebuild (focus ไม่หลุด) · `setTop()` · `setFu()` · `setItem(…, soft)` + `softSum()` อัปเดตการ์ดสรุป
- กดถัดไป = `validateMain()` → ช่องแดง + ข้อความใต้แถว + toast · เลือกวันที่/ตัวเลือก = render ใหม่ · ไม่ได้รับ → ไม่ครบถ้วนอัตโนมัติ · แถวไม่ครบไม่มีประเด็น/ผู้รับผิดชอบ/กำหนดส่ง บล็อก · กำหนดส่งก่อนวันรับมอบ บล็อก · รับมอบครบถ้วนแต่มีแถวค้าง บล็อก · มีเงื่อนไข/ยังไม่รับมอบ ช่องติดตามบังคับ · ไม่ตรงคำแนะนำ เตือน
- ส่ง → modal slot ต่อขั้น DOA (`resolveDoa()` · MOCK_DOA_RESOLVED) · อนุมัติเรียงขั้น `confirmApprove()` · ส่งกลับ/ยกเลิก `confirmReason()` · modal render เฉพาะตอนเปิด (state.modal.open) กันพังระหว่างปิด
- จำลอง API ล้ม: `commitRejected()` (S.sim) · persona เดโม `switchPersona()`

## §8 State-Driven UI Matrix
| สถานะ | เจ้าของ | ผู้พิจารณาขั้นปัจจุบัน | ผู้ในสายอื่น | admin |
|---|---|---|---|---|
| draft | แก้ไข · ส่งอนุมัติ · ยกเลิก | ไม่เห็น | ไม่เห็น | เห็น (ยกเลิกได้) |
| draft (ถูกส่งกลับ) | แถบแดง "ถูกส่งกลับแก้ไข — เหตุผล" + แก้ไข/ส่ง | ไม่เห็น | ไม่เห็น | เห็น |
| pending | ยกเลิกเอกสาร | ตรวจสอบแล้ว/ส่งกลับ (ขั้น 1) · รับทราบ/ส่งกลับ (ขั้นสุดท้าย) | ดูอย่างเดียว | ยกเลิกเอกสาร |
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
- ปุ่ม: สร้างแบบฟอร์ม
- ปุ่ม: ส่งอนุมัติ
- ปุ่ม: ส่งออก CSV
- ปุ่ม: เพิ่มเอกสาร
- ปุ่ม: แก้ไข
- placeholder: ${cond ? 'เช่น วันนัดติดตาม / รอบติดตาม' : 'ถ้ามี'}
- placeholder: ${ph}
- placeholder: ${rej ? 'แจ้งผู้จัดทำว่าต้องแก้อะไร' : 'เหตุผลที่ยกเลิก'}
- placeholder: ' + ph + '
- placeholder: HH:mm เช่น 10:30
- placeholder: ค้นหาเลขที่ / ชื่อโครงการ / ผู้ส่งมอบ
- placeholder: ไม่บังคับ
- aria: ${label}
- aria: เดือนก่อน
- aria: เดือนถัดไป

### ข้อความอื่น (จากโค้ด)
- (ขั้น
- [Lucide] All CDNs failed. Icons จะไม่แสดง but UI ยังใช้งานได้
- ]); if (canCancel(r)) items.push(['x-circle', 'ยกเลิกเอกสาร',
- ], ['printer', 'พิมพ์',
- ]]; if (isOwner(r) && r.status === 'draft') items.splice(1, 0, ['pencil', 'แก้ไข',
- showToast('ไม่มีการแจ้งเตือนใหม่','info')
- x–y จาก N
- · ต้องส่งเพิ่ม
- · อนุมัติแล้ว ล็อกแก้ไข
- ก.ค.
- ก.พ.
- ก.ย.
- กรกฎาคม
- กรอก
- กรุณากรอกข้อมูลให้ครบถ้วน
- กรุณากรอกฉบับชุดเอกสาร
- กรุณากรอกชื่อโครงการ
- กรุณากรอกผู้รับมอบ
- กรุณากรอกผู้ส่งมอบ
- กรุณากรอกเวลาแบบ HH:mm
- กรุณาเลือกวันที่รับมอบ
- กันยายน
- กานต์ ทดลองดี
- กำลังเปิดหน้าต่างพิมพ์ ·
- กำหนดการติดตาม
- กำหนดส่งเพิ่มเติม
- กำหนดส่งเพิ่มเติมต้องไม่ก่อนวันที่รับมอบ
- กำหนดส่งเร็วสุด
- กุมภาพันธ์
- ขอแก้ไขฉบับชุดเอกสาร
- ขั้นตอนที่ 6: จัดทำและส่งต่องานให้ฝ่ายบริหารการลงทุน
- ขั้นทดสอบ
- ขาดภาคผนวกใบอนุญาต
- ข้อมูลการรับมอบและผลการตรวจรับ
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้าม
- คน / หน่วยงาน
- ครบถ้วน
- คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
- ความครบถ้วน
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค่าเริ่มต้น = ผู้จัดทำ
- ค่าเริ่มต้นจากสายอนุมัติ (DOA กลาง) และผังองค์กร
- ค้นหา...
- ค้นหาเลขที่ / ชื่อโครงการ / ผู้ส่งมอบ
- จำนวนเอกสาร
- ฉบับชุดเอกสาร
- ชนิดไฟล์ไม่รองรับ
- ชลธร ใจทดสอบ
- ชื่อผู้รับมอบ
- ชื่อผู้ส่งมอบ
- ชื่อฟังก์ชัน
- ชื่อเอกสาร
- ชื่อโครงการ
- ณัฐพล สมมติกุล
- ดาวน์โหลด PDF
- ต.ค.
- ตรวจสอบและยืนยัน
- ตรวจสอบแล้ว
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ติดตามทุกวันศุกร์จนได้รับครบ
- ตุลาคม
- ต้อง
- ต้องตรวจสอบเพิ่มเติม
- ต้องมีรายการเอกสารอย่างน้อย 1 รายการ
- ต้องส่งเพิ่ม
- ถึง
- ถ้ามี
- ทะเบียนความเสี่ยงโครงการ
- ทะเบียนความเสี่ยงโครงการ (RR-01)
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ทุกผลการรับมอบ
- ทุกสถานะ
- ธ.ค.
- ธันวาคม
- ธีรวัฒน์ ระบบดี
- ธุรกรรมซื้อสินทรัพย์ตัวอย่าง จ
- ธุรกรรมซื้อหุ้นบริษัทตัวอย่าง ข
- ธุรกรรมซื้อหุ้นบริษัทตัวอย่าง ซ
- นัดส่งมอบใหม่ภายใน 2 สัปดาห์
- บริษัท ตัวอย่าง จำกัด (มหาชน)
- บริษัท ตัวอย่าง จำกัด (มหาชน) และบริษัทในเครือ
- บันทึกการรับมอบเอกสาร ประเด็นค้าง และข้อตกลงการติดตามระหว่างฝ่ายพัฒนาธุรกิจกับฝ่ายบริหารการลงทุน
- บันทึกซ้ำกับใบเดิม
- บันทึกผล
- บันทึกผิดโครงการ
- บันทึกร่างแล้ว ·
- ประวัติ
- ประวัติ (append-only)
- ประเด็นค้างจากการรับมอบ
- ประเด็นค้างยังไม่มีกำหนดส่งที่ชัดเจน
- ประเด็นที่พบ
- ปิด
- ผลการตรวจรับไม่ตรงกับเอกสารที่ส่งมอบจริง
- ผลการรับมอบ
- ผลการรับมอบไม่ตรงกับคำแนะนำจากตาราง (เตือน ส่งได้)
- ผู้จัดการฝ่ายบริหารการลงทุน
- ผู้จัดการฝ่ายพัฒนาธุรกิจ
- ผู้จัดทำ
- ผู้ตรวจสอบ
- ผู้รับผิดชอบแก้ไข
- ผู้รับมอบจากฝ่ายบริหารการลงทุน
- ผู้ส่ง
- ผู้ส่งมอบ
- ผู้ส่งมอบจากฝ่ายพัฒนาธุรกิจ
- ผู้อนุมัติ / รับทราบ
- ฝ่ายบริหารการลงทุน
- ฝ่ายพัฒนาธุรกิจ
- พ.ค.
- พ.ย.
- พฤ
- พฤศจิกายน
- พฤษภาคม
- พิมพ์
- ภาคผนวกใบอนุญาต (LDD-01) · ทะเบียนความเสี่ยงโครงการ (RR-01)
- ม.ค.
- มกราคม
- มติคณะกรรมการลงทุน
- มิ.ย.
- มิถุนายน
- มี.ค.
- มีนาคม
- ยกเลิก
- ยกเลิกเอกสาร
- ยกเลิกเอกสาร?
- ยกเลิกเอกสารแล้ว ·
- ยังไม่มีข้อมูล
- ยังไม่มีรายการเอกสาร
- ยังไม่มีแบบฟอร์มชุดเอกสารส่งมอบงาน
- ยังไม่รับมอบ
- ยังไม่รับมอบ ต้องระบุหมายเหตุจากฝ่ายบริหารการลงทุน
- ยังไม่รับมอบจนกว่าจะได้รับทะเบียนความเสี่ยงฉบับสมบูรณ์
- ยังไม่ส่ง
- ยังไม่ได้รับไฟล์
- ย้อนกลับ
- รอขั้นก่อนหน้า
- รองกรรมการผู้จัดการ
- รอผล
- รอพิจารณา
- รออนุมัติ
- ระบบเลือกตอนส่ง
- ระบุประเด็น
- ระบุประเด็นค้าง
- ระบุเหตุผลที่ยังไม่รับมอบ
- รับทราบ
- รับมอบครบถ้วน
- รับมอบครบถ้วน ต้องได้รับและครบถ้วนทุกรายการ (ค้าง
- รับมอบแบบมีเงื่อนไข
- รับมอบแบบมีเงื่อนไข ต้องระบุกำหนดการติดตาม
- รับมอบแบบมีเงื่อนไข ต้องระบุประเด็นค้างจากการรับมอบ
- รายการ
- รายการ)
- รายการเอกสารส่งมอบ.xlsx
- รายงานตรวจสอบสถานะทางกฎหมาย
- รายงานตรวจสอบสถานะทางกฎหมายขาดภาคผนวก · ทะเบียนความเสี่ยงยังไม่ได้รับ
- รายงานผลการศึกษาความเป็นไปได้
- รายละเอียด
- ร่าง
- ลบรายการนี้
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ลายเซ็น / อนุมัติ
- ลำดับการอนุมัติ
- ล้างตัวกรอง
- วันที่ ........./........./.........
- วันที่ / เวลารับมอบ
- วันที่รับมอบ
- วิภา ตัวอย่างงาม
- ศิริพร ข้อมูลจำลอง
- ส.ค.
- สถานะ
- สถานะเอกสาร
- สรุปเงื่อนไขสัญญาหลัก
- สร้าง PDF
- สร้างเมื่อรับมอบชุดเอกสารจากฝ่ายพัฒนาธุรกิจ
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างแบบฟอร์ม
- สร้างโดย
- สลับเป็น
- สำนักกรรมการผู้จัดการ
- สิงหาคม
- ส่งกลับ
- ส่งกลับเป็นร่างแล้ว ·
- ส่งอนุมัติ
- ส่งอนุมัติแล้ว ·
- ส่งออก
- ส่งแล้วแก้ไขไม่ได้ — ถ้าถูกส่งกลับ จะกลับเป็นร่างเลขเดิมให้แก้แล้วส่งใหม่
- ส่งในระบบ
- หมายเหตุจากฝ่ายบริหารการลงทุน
- อนุมัติ
- อนุมัติแล้ว
- อนุมัติแล้ว · ผลการรับมอบมีผล
- อรุณี รองตัวอย่าง
- ออกใช้ครั้งแรก
- อา
- เจ้าหน้าที่ดูแลเอกสารการลงทุน
- เจ้าหน้าที่บริหารการลงทุน
- เจ้าหน้าที่พัฒนาธุรกิจ
- เช่น FS-01 / V02
- เช่น V01 / V02 / Final
- เดือนถัดไป
- เด้งกลับบน
- เพิ่มเติม
- เพิ่มเอกสาร
- เม.ย.
- เมษายน
- เลขที่
- เลขที่เอกสาร
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกประเทศ
- เลือกผู้พิจารณา
- เลือกวันที่
- เวลารับมอบ
- เหตุผลที่ยกเลิก
- เอกสาร / ข้อมูลที่ต้องส่งเพิ่มเติม
- เอกสารครบ
- เอกสารหลักยังไม่ครบ
- เอกสารแนบ
- แก้ไขร่าง
- แก้ไขล่าสุด
- แก้ไขเอกสาร
- แก้ไขแบบฟอร์ม
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งผู้จัดทำว่าต้องแก้อะไร
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบจำลองทางการเงิน
- แบบฟอร์ม
- แบบฟอร์มชุดเอกสารส่งมอบงาน
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
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
- ใช้ในขั้นตอน
- ได้รับ
- ได้รับและครบถ้วน
- ได้รับแล้ว
- ไม่ครบถ้วน
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่ยกเลิก
- ไม่อนุมัติ
- ไม่ได้รับ
- ไม่ได้รับ เลือก ครบถ้วน ไม่ได้
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
markers: {'marker': 'ENG-DOC-NUM', 'line': '/* doc_type IVMF — ประกาศใน DOCCFG_BRIEF_F-TMP-008 · เลขรันจาก ENG-DOC-NUM ตอนบันทึกครั้งแรก · เช็คสถานะเปิดใช้ที่ F-DOC'}, {'marker': 'DOA-ENGINE-HOOK', 'line': '/* DOA-ENGINE-HOOK — resolve จาก DOA entry ของ F-TMP-008 ณ เวลาส่ง แล้ว snapshot ลง approval_chain (DOA_BRIEF_F-TMP-008.'}, {'marker': 'TODO', 'line': 'approver_role / approved_by / approval_chain ต่อขั้น · จำนวนขั้นตั้งที่ DOA กลาง (dynamic) — ห้าม fix · TODO: DOA engine'}, {'marker': 'ENG-DOC-NUM', 'line': "/* บันทึกครั้งแรก = ENG-DOC-NUM.next('IVMF') ออกเลขที่ (DEC-10) · ผู้จัดทำ snapshot ตำแหน่ง/ฝ่าย ณ วันที่บันทึก */"}, {'marker': 'ENG-NOTIFY', 'line': '/* ENG-NOTIFY (NTF_BRIEF_F-TMP-008): ivmf_handover_followup → ผู้จัดทำ + admin role (อนุมัติครบ และผล = รับมอบแบบมีเงื่อ'}, {'marker': 'ENG-NOTIFY', 'line': '/* อนุมัติครบ: ไม่เปลี่ยนค่าในระบบ ไม่ส่งต่อระบบอื่น (DEC-01/02) — ผลการรับมอบมีผลในเอกสาร · มีเงื่อนไข/ยังไม่รับมอบ → E'}, {'marker': 'DOA-ENGINE-HOOK', 'line': 'doa: MOCK_DOA_RESOLVED 2 ขั้น (role-line-manager → role-mgr-bu) = DOA-ENGINE-HOOK (DOA_BRIEF_F-TMP-008) · คำตัดสินผูก ro'}, {'marker': 'ENG-DOC-NUM', 'line': "hooks: ENG-DOC-NUM.next('IVMF') ตอนบันทึกครั้งแรก · F-DOCCFG status (DOC.active) · ENG-NOTIFY ivmf_handover_followup / i"}, {'marker': 'ENG-NOTIFY', 'line': "hooks: ENG-DOC-NUM.next('IVMF') ตอนบันทึกครั้งแรก · F-DOCCFG status (DOC.active) · ENG-NOTIFY ivmf_handover_followup / i"}

## §11 Traceability + Drift Log
| จอ/ส่วน | FRD | หมายเหตุ |
|---|---|---|
| P-01..P-03 | 01_UI §1.1 | ตรง |
| การ์ด ①②③ | 01_UI §1.2 · FORM_SPEC F01–F18 | ตรง 1:1 (DEC-06 ไม่เพิ่มช่อง) |
| ลำดับ · ได้รับแล้ว↔ความครบถ้วน · แถวค้าง · กำหนดส่ง · ผลการรับมอบ · คำแนะนำ | 05 BR-01..07 | ตรง |
Drift: ไม่มี (prototype = source of truth) · คำตัดสินขั้น 1 = ตรวจสอบแล้ว/ส่งกลับ · ขั้น 2 = รับทราบ/ส่งกลับ (LD-01)

## §12 Diff จากเวอร์ชันก่อน
เวอร์ชันแรก

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- Phase 2: เลือกโครงการจากทะเบียน (FM-IVM-01) แทนพิมพ์ชื่อ · ดึงรายการเอกสารจากคำขอเอกสาร FM-IVM-05 (OQ-07) · ปิดรายการค้างส่งหลังอนุมัติ (OQ-08) · แจ้งเตือนก่อนกำหนดส่งเพิ่มเติม
