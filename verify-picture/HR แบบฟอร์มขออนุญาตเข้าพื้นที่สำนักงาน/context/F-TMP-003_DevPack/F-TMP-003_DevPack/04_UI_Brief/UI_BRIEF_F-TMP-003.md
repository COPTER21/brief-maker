# UI_BRIEF — F-TMP-003 แบบฟอร์มขออนุญาตเข้าพื้นที่สำนักงาน

## §0 Document Control + Pairing
| รายการ | ค่า |
|---|---|
| HTML | feature.html (html-generator-v9.4 · archetype `Q-form` · `window.__QA__` มี) |
| FRD | FRD_F-TMP-003_Pack (01_UI P-01..P-03 · 02_API · 05_RULES) — pair แล้ว |
| DECISIONS.lock | 15 มติ (AI-DEFAULT 11 · VALID 4) — ทุกมติ AI-DEFAULT รอลูกค้ายืนยัน |
| แบบพิมพ์ | print/form.tpl.html (thai-doc v2.1 Replica FM-HRM-05) ฝังเป็น `VAR_TPL` |
| สถานะ drift | ไม่มี business drift · prototype-only: `__QA__`, ตัวสลับผู้ใช้ `switchPersona()`, `S.sim` (ดู §11 Drift Log) |

## §1 Design Tokens AS-BUILT
- ฟอนต์: Satoshi + Noto Sans Thai (UI) · Sarabun (แบบพิมพ์ใน iframe) · ไอคอน Lucide 0.469.0 (multi-CDN loader + `renderIcons()`)
- CI: CUBE Warm Light (ห้ามแก้) · primary #FF3B30
### CSS Variables (ทั้งชุด)
| var | ค่า |
|---|---|
| `--c-navy` | #111111 |
| `--c-navy-2` | #111111 |
| `--c-primary` | #FF3B30 |
| `--c-primary-hover` | #E62E24 |
| `--c-teal` | #FF9A1F |
| `--c-teal-light` | #FFB763 |
| `--c-ink` | #111111 |
| `--c-mute` | #54565C |
| `--c-mute-2` | #73757B |
| `--c-mute-3` | #9A9CA2 |
| `--c-placeholder` | rgb(180,182,188) |
| `--z-content` | 1 |
| `--z-sticky` | 10 |
| `--z-shell` | 10 |
| `--z-dropdown` | 30 |
| `--z-backdrop` | 50 |
| `--z-drawer` | 51 |
| `--z-modal` | 60 |
| `--z-popover` | 70 |
| `--z-toast` | 80 |
| `--c-line` | #DEDAD4 |
| `--c-line-2` | #E9E5E0 |
| `--c-line-3` | #F1EEEA |
| `--c-bg-off` | #FAF8F5 |
| `--c-success` | #1F9D55 |
| `--c-warning` | #E8870F |
| `--c-danger` | #E62E24 |
| `--sidebar-w` | 232px |
| `--shell-h` | 52px |
| `--fs-h1` | 22px |
| `--fs-h2` | 17px |
| `--fs-h3` | 15px |
| `--fs-body` | 14px |
| `--fs-sub` | 13px |
| `--fs-meta` | 12px |
| `--fs-cap` | 11px |
| `--fs-kpi` | 28px |
| `--sp-xs` | 4px |
| `--sp-sm` | 8px |
| `--sp-md` | 12px |
| `--sp-lg` | 20px |
| `--sp-xl` | 28px |
| `--r-xs` | 4px |
| `--r-sm` | 6px |
| `--r-md` | 8px |
| `--r-lg` | 12px |
| `--r-full` | 999px |
| `--z-portal` | 90 |
### z-index map
| ค่า | ใช้ที่ |
|---|---|
| var(--z-shell) | .sidebar |
| var(--z-sticky) | .shell-bar, .table-wrap thead th, .wizard-footer |
| var(--z-dropdown) | .user-menu, .info-tip::after |
| var(--z-popover) | .menu-fixed, .ss-list.menu-fixed, .row-menu |
| var(--z-backdrop) | .ss-list, .drawer-backdrop, .modal-backdrop, #drawerBackdrop |
| 3 | .table-scroll.is-sticky thead th |
| 2 | .stepper-circle |
| 1 | .stepper-item:not(:last-child)::after |
| var(--z-drawer) | .drawer, #drawer |
| var(--z-toast) | .toast, #toast |
| var(--z-modal) | .modal-backdrop |
| var(--z-portal) | .bd-pop |

## §2 Route Map
| Route | เปิดอะไร | handler |
|---|---|---|
| `#/visitor-access` | หน้ารายการ (default) | `applyRoute()` |
| `#/visitor-access/view/:id` | drawer ดู (ตรวจ `canSee()` ก่อน — ไม่มีสิทธิ์ = ไม่เปิด) | `showDrawer()` |
| `#/visitor-access/create` | wizard สร้าง | `startWizard()` |
| `#/visitor-access/edit/:id` | wizard แก้ร่าง (ตรวจ `canEdit()`) | `startWizard()` |
- refresh-safe: `hashchange` → `applyRoute()` · ปิด drawer → `go()` กลับ route รายการ

## §3 Layout Shell
- `.sidebar` ดำ (เมนู HR › ขอเข้าพื้นที่สำนักงาน + `#sbBadge` = จำนวนใบที่ผู้ใช้ต้องพิจารณา) · `.shell-bar` ขาว (breadcrumb › ขอเข้าพื้นที่สำนักงาน · `.user-chip` + `#personaList` สลับผู้ใช้ — prototype-only)
- คน = `.avatar.is-person` วงกลมพื้นดำ icon user (U17) รวมผู้มาติดต่อ (`visitorInline()`) · `#page-content` = หน้ารายการ

## §4 Page Anatomy
### P-01 รายการ (`renderPage()`)
- `.ph`: `.ph-title` · `.ph-sub` คำอธิบาย + `.ph-badge` (รายการ · ร่าง n · รอพิจารณา n — ค่า 0 ไม่แสดง) · `.ph-actions`: ส่งออก CSV (`exportCSV()`) · สร้างคำขอ `#btnCreate` (`startWizard()` · disabled เมื่อ `DOC.active` false + `.alert-row.is-danger`)
- `.card.list-card` › `.filter-bar`: `#fq` ค้นหา (`onQ()`) · `searchSelectHTML` fst / fdiv · รีเซ็ต (`resetFilters()`)
- `.table-wrap .table`: เลขที่ (`.code-strong`) · วันที่เข้าพื้นที่ · ผู้มาติดต่อ (`visitorInline()`) · บริษัท / หน่วยงาน · ผู้รับการติดต่อ (`personInline()`) · สถานะเอกสาร (`docPill()`) · ลายเซ็น (`renderSignProgress()` x/y + `.sp-bar`) · ⋮ `.ra-btn` (`openRowMenu()`)
- `pager()` → `.table-footer`: `.pg-size` แสดงต่อหน้า 10/25/50 (`setSize()`) · "x – y จาก N รายการ" · `.pagination` `.pg-btn`
### P-02 wizard (`renderWizard()` · `.drawer-panel.wide`)
- `.dw-head` + `stepper()` 3 ขั้น (`STEPS`) · ขั้น 1 `wizMain()` = `.wz-split` [ `.wz-main` การ์ด `card1()` + `card2()` | `sumCard()` `.wz-sum` ]
- `card1()` #sec1: `bedateHTML('visitDate')` #fVisit (`pickVisit()`) · `.seg-control` คำนำหน้า #fTitle (`setF1('vTitle')`) · ชื่อ #fName · โทรศัพท์ #fPhone · บริษัท #fCompany · combobox `whost` #fHost (`setHost()`) · textarea วัตถุประสงค์ #fPurpose · `bedateHTML('vSignDate')` #fSign (`pickSign()`) + `.field-warn`
- `card2()` #sec2: `.sys-fields` ชื่อผู้รับการติดต่อ · สังกัดฝ่าย · ผู้บังคับบัญชาต้นสังกัด (อ่านอย่างเดียว) · ยังไม่เลือก host = `.empty-sub`
- ขั้น 2 `wizAttach()` `.upload-zone` + `#varFile` (`pickFiles()` · `gateFiles()`) · ขั้น 3 `wizReview()` `.review-card` × 3
- `.dw-footer`: ย้อนกลับ (`wizBack()`) · ยกเลิก (`closeDrawer()`) · ถัดไป `#btnNext` (`wizNext()`) / บันทึกแบบร่าง `#btnDraft` (`saveDraft()`) · บันทึกและส่งขออนุมัติ `#btnSaveSubmit` (`saveAndSubmit()`)
### P-03 ดู (`renderViewDrawer()` · `.drawer-panel` 920)
- `.dw-head`: `.doc-ident` (eyebrow · `.dw-title` เลขที่ + pill · `.dw-sub` ผู้มาติดต่อ · วันที่) · `.dw-actions` ปุ่มตามสถานะ + `.drawer-header-divider` + `.top-icon-btn` พิมพ์/ดาวน์โหลด (`genPdf()`)/ปิด
- `.drawer-tabs` (`tabBtn()`): รายละเอียด (`renderDetailTab()` · `viewBanner()` · `decisionText()`) › PDF Preview (`renderPdfTab()` · `.pdf-slot` `iframe.pdf-frame` srcdoc = `varPdfDoc()` · `fitPdf()`) › ลายเซ็น / อนุมัติ (`renderSignTab()` ปุ่ม อนุมัติ/ไม่อนุมัติ ใน timeline) › ประวัติ (`renderHistoryTab()`)

## §5 Component Inventory
| Component | anchor | states |
|---|---|---|
| segmented คำนำหน้า | `.seg-control` `.seg-item` | default · `.is-active` · กลุ่มผิด = `.field.is-invalid` |
| ช่องวันที่ พ.ศ. | `.bedate` + `.bd-pop` | ว่าง placeholder · เลือกแล้ว "20 ต.ค. 2569" · เตือน `.field-warn` |
| การ์ดหัวข้อ | `.wz-card` | `.is-bad` ขอบแดงเมื่อ validate ไม่ผ่าน |
| combobox พนักงาน | `searchSelectHTML('whost')` / `initSearchSelect()` `.ss-list` | เปิด/ค้นหา/เลือก/ล้าง · Esc ปิด |
| ปุ่มบันทึก | `#btnSaveSubmit` | loading `loader-2` "กำลังบันทึก…" · disabled ระหว่าง `S.busy` |
| แถบสถานะ | `.alert-row` (`viewBanner()`) | ร่าง · ไม่อนุมัติ (`is-danger` + เหตุผล) · รอพิจารณา · อนุมัติแล้ว · ยกเลิก |
| ตารางว่าง | `emptyStateHTML()` / `.empty-sub` | รายการว่าง · ค้นหาไม่พบ · section ว่าง |

## §6 Overlay Registry
| overlay | ขนาด | เปิด | dismiss |
|---|---|---|---|
| drawer ดู `.drawer` | 920 | `openView()` / `showDrawer()` | ปุ่ม x · Esc · mousedown ที่ `#drawerBackdrop` (`backdropDown()`) |
| drawer wizard `.drawer-panel.wide` | 1290 | `startWizard()` | เหมือนบน · กรอกค้าง = modal discard |
| modal `.modal` (`renderModal()`) | ส่ง = `.modal.is-lg` | `openModalCfg()` | Esc · ปุ่ม · mousedown ที่ `#modalBackdrop` (ไม่ปิดถ้าพิมพ์เหตุผลแล้ว — `modalBackdropClick()`) |
| row menu ⋮ `.row-menu` | 180 | `openRowMenu()` (portal `#overlay-root`) | คลิกที่อื่น · scroll (`closeRowMenu()`) |
| user menu `.user-menu` | — | `toggleUserMenu()` | คลิกที่อื่น |
| combobox `.ss-list` | ตามช่อง | ช่อง | เลือก · คลิกที่อื่น · Esc |
| ปฏิทิน `.bd-pop` | 280 | `bdToggle()` | เลือกวัน · Esc (ปิดแค่ปฏิทิน) |
| toast `#toast` | — | `showToast()` | อัตโนมัติ |

## §7 Interaction Spec
- Esc chain (`keydown` ใน base kit): combobox/ปฏิทิน → modal (`closeModal()`) → drawer (`closeDrawer()`)
- backdrop = mousedown เท่านั้น (U25): `backdropDown(event, 'drawer'|'modal')` ตรวจ `event.target === currentTarget`
- ปิด wizard ที่ dirty → modal "ทิ้งข้อมูลที่กรอกไว้?" · แก้จาก view = ปิด view ก่อนแล้วเปิด wizard (ไม่ซ้อน)
- validate เมื่อกด ถัดไป/บันทึก เท่านั้น → `validateMain()` + `failMain()` เลื่อนไปช่องแรกที่ผิด · เลือกวันที่เข้าพื้นที่ = ตั้งวันที่ลงนามค่าเริ่ม (`pickVisit()`)
- พิมพ์ชื่อ/บริษัท → การ์ดสรุปอัปเดตทันที (`syncSum()`) ไม่ rebuild focus ไม่หลุด
- ไม่อนุมัติ/ยกเลิก: chip เหตุผลสำเร็จรูป (`setReasonPreset()`) + textarea บังคับ (`confirmReason()`)

## §8 State-Driven UI Matrix
| status | pill (`DOC_ST`) | ปุ่มหัว drawer (เจ้าของ) | ปุ่มหัว drawer (ผู้พิจารณา) | ⋮ |
|---|---|---|---|---|
| draft | ร่าง `pill-muted` (+ แถบแดงถ้าเคยไม่อนุมัติ) | ยกเลิก · แก้ไข · ส่งขออนุมัติ | — (ไม่เห็นร่าง) | ดูรายละเอียด · แก้ไข · พิมพ์ · ยกเลิกเอกสาร |
| pending | รอพิจารณา `pill-warning` | ยกเลิกเอกสาร | ไม่อนุมัติ · อนุมัติ | ดูรายละเอียด · พิมพ์ · ยกเลิกเอกสาร (เจ้าของ/HR) |
| approved | อนุมัติแล้ว `pill-success` | — | — | ดู · พิมพ์ |
| cancelled | ยกเลิก `pill-danger` | — | — | ดู · พิมพ์ |

## §9 Microcopy (verbatim)
### Toast (`showToast`)
| ข้อความ | variant |
|---|---|
| ไม่มีการแจ้งเตือนใหม่ | info |
| แบบเอกสารนี้ยังไม่เปิดใช้งาน | warning |
| แก้ไขได้เฉพาะร่างของตัวเอง | warning |
| กรุณากรอกข้อมูลให้ครบถ้วน | warning |
| บันทึกร่างแล้ว · | info |
| ส่งขออนุมัติแล้ว · | info |
| อนุมัติแล้ว · | info |
| ส่งออก | info |
| สลับเป็น | info |
| แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง | error |
- toast ประกอบ: "บันทึกร่างแล้ว · " + เลขที่ · "ส่งขออนุมัติแล้ว · " + เลขที่ · "อนุมัติแล้ว · " + เลขที่ · "ไม่อนุมัติ — กลับเป็นร่าง · " + เลขที่ · "ยกเลิกเอกสารแล้ว · " + เลขที่ · "ส่งออก " + n + " รายการ" · "สลับเป็น " + ชื่อ · "ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง" · "ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่" · "คุณไม่มีสิทธิ์ทำรายการนี้"
### ข้อความบนจอ (สกัดจาก HTML)
- 0 ไม่มีขั้นพิจารณา DOA กลางไม่ได้ตั้งขั้น — ส่งแล้วอนุมัติอัตโนมัติ
- · กลับเป็นร่างเลขเดิม
- · รอพิจารณาอยู่ — ผู้พิจารณาจะได้รับแจ้ง
- · ส่งแล้ว ล็อกแก้ไข
- ก.ค.
- ก.พ.
- ก.ย.
- กมลชนก ใจงาม
- กรกฎาคม
- กรรมการผู้จัดการ
- กรอกตามแบบฟอร์ม
- กรุณากรอกข้อมูลให้ครบถ้วน
- กรุณาเลือกพนักงานที่ติดต่อ
- กันยายน
- กำลังเปิดหน้าต่างพิมพ์ ·
- กุมภาพันธ์
- ข้อมูลคำขอ
- ข้อมูลคำขอเข้าพื้นที่
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลบุคคล / บริษัท / หน่วยงาน ผู้มาติดต่อ
- ข้อมูลยังไม่ครบ — แก้ไขร่างให้ครบก่อนส่ง
- ข้อมูลเอกสาร
- ข้าม
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค้นหา...
- ค้นหาพนักงานที่ผู้มาติดต่อขอพบ
- ค้นหาเลขที่ / ผู้มาติดต่อ / บริษัท / ผู้รับการติดต่อ
- ชนิดไฟล์ไม่รองรับ
- ชาตรี ทดลองส่ง
- ชื่อ นามสกุล ผู้มาติดต่อ
- ชื่อผู้บังคับบัญชาต้นสังกัด
- ชื่อผู้รับการติดต่อ
- ชื่อฟังก์ชัน
- ณัฐชา บุญมา
- ดาวน์โหลด PDF
- ต.ค.
- ตรวจสอบเอกสารประกอบงบการเงินไตรมาส 3
- ตรวจสอบและยืนยัน
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ติดตั้งอุปกรณ์เครือข่ายไร้สายชั้น 3 และทดสอบสัญญาณ
- ติดต่อกับพนักงานใน
- ตุลาคม
- ต้อง
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ทุกฝ่าย
- ทุกสถานะ
- ธ.ค.
- ธนพล ศรีวงศ์
- ธันวาคม
- นางสาว
- นำเสนอสินค้าและตรวจสอบสเปกวัสดุสำนักงาน
- บริษัท / หน่วยงาน
- บริษัท ตัวอย่างขนส่ง จำกัด
- บริษัท ตัวอย่างซอฟต์แวร์ จำกัด
- บริษัท ตัวอย่างซัพพลาย จำกัด
- บริษัท ตัวอย่างเน็ตเวิร์ค จำกัด
- บริษัท ตัวอย่างแอร์เซอร์วิส จำกัด
- บริษัท ลูกค้าตัวอย่าง จำกัด
- บริษัทหรือหน่วยงานของผู้มาติดต่อ
- บันทึกคำขอเมื่อมีบุคคลภายนอกนัดเข้าพบ
- บันทึกซ้ำ
- บันทึกร่างแล้ว ·
- บันทึกแทน
- ประชุมสรุปรอบการจัดส่งวัสดุสำนักงานไตรมาส 4
- ประยุทธ ทดสอบงาน
- ประวัติ
- ประเสริฐ มั่นคง
- ปิยะนุช แก้วมณี
- ผลพิจารณา
- ผู้จัดการฝ่ายขาย
- ผู้จัดการฝ่ายจัดซื้อ
- ผู้จัดการฝ่ายบัญชี
- ผู้จัดการฝ่ายบุคคล
- ผู้จัดการฝ่ายเทคโนโลยีสารสนเทศ
- ผู้บังคับบัญชาต้นสังกัด
- ผู้บังคับบัญชาพิจารณา
- ผู้มาติดต่อ
- ผู้มาติดต่อ —
- ผู้มาติดต่อยกเลิกนัด
- ผู้มาติดต่อลงนามด้วยมือบนแบบพิมพ์
- ผู้รับการติดต่อ
- ฝ่ายขาย
- ฝ่ายจัดซื้อ
- ฝ่ายทรัพยากรบุคคล
- ฝ่ายบัญชีและการเงิน
- ฝ่ายเทคโนโลยีสารสนเทศ
- พ.ค.
- พ.ย.
- พนักงานนี้ไม่มีผู้บังคับบัญชาต้นสังกัดในผังองค์กร — ส่งพิจารณาไม่ได้
- พนักงานผู้รับการติดต่อ
- พฤศจิกายน
- พฤษภาคม
- พิมพ์
- พิมพ์ใจ ตัวอย่างลูกค้า
- ม.ค.
- มกราคม
- มาลี ตัวอย่างดี
- มิ.ย.
- มิถุนายน
- มี.ค.
- มีนาคม
- ยกเลิก
- ยกเลิกเอกสาร
- ยกเลิกเอกสารแล้ว ·
- ยังเป็นร่าง — กรอกครบแล้วกดส่งขออนุมัติ
- ยังไม่ถึง
- ยังไม่มีข้อมูล
- ยังไม่มีคำขอเข้าพื้นที่
- ยังไม่ส่ง
- ยังไม่ได้เลือก
- ย้อนกลับ
- รอผลพิจารณา
- รอพิจารณา
- รอส่ง
- รายการ
- รายละเอียด
- ร่าง
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ลายเซ็น / อนุมัติ
- ลำดับการลงนาม
- ล้างตัวกรอง
- ล้างและตรวจเช็กเครื่องปรับอากาศห้องเซิร์ฟเวอร์
- วรวุฒิ ทองดี
- วัตถุประสงค์
- วัตถุประสงค์เพื่อ
- วัตถุประสงค์ไม่ชัดเจน ขอรายละเอียดเพิ่ม
- วันที่
- วันที่ ........./........./.........
- วันที่ขอตรงกับกิจกรรมภายใน กรุณาเลื่อนนัด
- วันที่ผ่านมาแล้ว
- วันที่ลงนามก่อนวันที่เข้าพื้นที่
- วันที่เข้าพื้นที่
- วิชัย บริหารดี
- วีระ ทดสอบระบบ
- ศศิธร มีสุข
- ส.ค.
- สถานะ
- สมศักดิ์ ทดลองใช้
- สมหญิง ตัวอย่างงาน
- สร้าง PDF
- สร้างคำขอ
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างโดย
- สลับเป็น
- สังกัดฝ่าย
- สาธิตระบบจัดซื้อออนไลน์
- สำนักกรรมการผู้จัดการ
- สำนักงานบัญชีตัวอย่าง
- สิงหาคม
- สุดา ตัวอย่างใหม่
- ส่งขออนุมัติ
- ส่งขออนุมัติเข้าพื้นที่?
- ส่งขออนุมัติแล้ว ·
- ส่งออก
- ส่งแล้วแก้ไขไม่ได้ — ถ้าไม่อนุมัติ เอกสารกลับเป็นร่างเลขเดิมให้แก้แล้วส่งใหม่
- ห้างหุ้นส่วนจำกัด ตัวอย่างการค้า
- อนุชา พรหมสุข
- อนุญาต มีพนักงานพาตลอดเวลา
- อนุญาตเข้าพื้นที่ห้องประชุมเล็ก ชั้น 2
- อนุมัติ
- อนุมัติแล้ว
- อนุมัติแล้ว ·
- อนุมัติให้เข้าพื้นที่
- อนุมัติให้เข้าพื้นที่แล้ว — พิมพ์แบบฟอร์มให้ผู้มาติดต่อลงนามที่จุดรับแขก
- อรุณี ตัวอย่างบัญชี
- อำนาจ ตัวอย่างช่าง
- เจรจาเงื่อนไขการสั่งซื้อรายปี
- เจ้าหน้าที่ขาย
- เจ้าหน้าที่จัดซื้อ
- เจ้าหน้าที่บัญชี
- เจ้าหน้าที่ไอที
- เดือนถัดไป
- เด้งกลับบน
- เพิ่มเติม
- เม.ย.
- เมษายน
- เยี่ยมชมโชว์รูมและหารือแผนการสั่งซื้อ
- เลขที่
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกประเทศ
- เลือกผู้พิจารณา
- เลือกวันที่
- เลื่อนนัดเป็นวันอื่น
- เหตุผล
- เหตุผลที่ยกเลิก
- เอกสารแนบ
- แก้ไขร่าง
- แก้ไขล่าสุด
- แก้ไขเอกสาร
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งผู้รับการติดต่อว่าทำไมไม่อนุมัติ
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบฟอร์มขออนุญาตเข้าพื้นที่สำนักงาน
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- ใบเสนอราคาอุปกรณ์เครือข่าย.pdf
- ไม่จำเป็นต้องเข้าพื้นที่สำนักงาน
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่มีขั้นพิจารณา
- ไม่ยกเลิก
- ไม่อนุมัติ
- ไม่อนุมัติ — กลับเป็นร่าง
- ไม่อนุมัติ — กลับเป็นร่าง ·
- — ผู้รับการติดต่อเป็นผู้ส่งขออนุมัติ

## §10 Data Binding & BACKEND anchors
| prototype | ระบบจริง (02_API) |
|---|---|
| `EMP` + `empOf()` | API-03 prefill (F-EMP-001 / F-ORG-001) |
| `RECS` + `listRows()` + `canSee()` | API-01/02 (FN-09) |
| `persist()` (`SEQ` + `DOC.prefix`) | API-04/05 · ENG-DOC-NUM (FN-03) |
| `MOCK_DOA_RESOLVED` / `resolveDoa()` (DOA-ENGINE-HOOK · 1 ขั้น role-line-manager) | API-06/07 GET /doa/resolve |
| `confirmSubmit()` / `confirmApprove()` / `confirmReason()` | API-07 / API-08 / API-09 |
| `docPrintData()` + `tplRender()` + `VAR_TPL` | API-10 render ฝั่ง server (parity) |
| `exportCSV()` | API-11 (ไม่มีโทรศัพท์) |
| `gateFiles()` / `FILE_ACCEPT` | API-12 Document Center |
| `validateMain()` / `phoneOk()` | FN-02 (ทำซ้ำฝั่ง server) |

## §11 Traceability + Drift Log
| Brief | FRD | HTML |
|---|---|---|
| §4 P-01 | 01_UI P-01 · API-01/11 | `renderPage()` |
| §4 P-02 | 01_UI P-02 · API-03/04/05 · BR-01..05 | `renderWizard()` |
| §4 P-03 | 01_UI P-03 · API-02/08/09/10 | `renderViewDrawer()` |
| §8 | 05 §5.2 · §5.3 | `DOC_ST` · `canEdit()` · `canAct()` · `canCancel()` |
### ⚠️ Drift Log
| รายการ | ชนิด | ข้อเสนอ |
|---|---|---|
| `__QA__` · `switchPersona()` · `S.sim` · `commitRejected()` | HTML-only (prototype) | ไม่ทำในระบบจริง |
| โลโก้ในแบบพิมพ์ = placeholder | HTML-only | ระบบจริงใช้ header_snapshot (Organization) |
| ชื่อบริษัท `DOC.company` = ค่าสมมติ | HTML-only | ระบบจริง Company.name_th (DEC-13) |

## §12 Diff จากเวอร์ชันก่อน
— ไม่มีใน HTML นี้ (เวอร์ชันแรก)

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- ส่งรายชื่อผู้มาติดต่อที่อนุมัติแล้วให้จุดรับแขก/ระบบแลกบัตร (OQ-05) — รอบถัดไป
