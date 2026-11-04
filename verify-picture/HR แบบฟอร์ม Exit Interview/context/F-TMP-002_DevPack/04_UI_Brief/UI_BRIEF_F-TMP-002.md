# UI_BRIEF — F-TMP-002 แบบสอบถามบุคลากรที่พ้นจากงาน (Exit Interview)

## §0 Document Control + Pairing
| รายการ | ค่า |
|---|---|
| HTML | feature.html (html-generator-v9.4 · archetype `Q-form` · `window.__QA__` มี) |
| FRD | FRD_F-TMP-002_Pack (01_UI P-01..P-03 · 02_API · 05_RULES) — pair แล้ว |
| DECISIONS.lock | 17 มติ (AI-DEFAULT 11 · VALID 6) — ทุกมติ AI-DEFAULT รอลูกค้ายืนยัน |
| แบบพิมพ์ | print/form.tpl.html (thai-doc v2.1 Replica FM-HRM-06) ฝังเป็น `EXI_TPL` |
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
| `#/exit-interview` | หน้ารายการ (default) | `applyRoute()` |
| `#/exit-interview/view/:id` | drawer ดู (ตรวจ `canSee()` ก่อน — ไม่มีสิทธิ์ = ไม่เปิด) | `showDrawer()` |
| `#/exit-interview/create` | wizard สร้าง | `startWizard()` |
| `#/exit-interview/edit/:id` | wizard แก้ร่าง (ตรวจ `canEdit()`) | `startWizard()` |
- refresh-safe: `hashchange` → `applyRoute()` · ปิด drawer → `go()` กลับ route รายการ

## §3 Layout Shell
- `.sidebar` ดำ (เมนู HR › Exit Interview + `#sbBadge` = จำนวนใบที่ HR ต้องรับทราบ/ผู้พิจารณาต้องทำ) · `.shell-bar` ขาว (breadcrumb Core › HR › แบบสอบถามผู้พ้นจากงาน · กระดิ่ง · `.user-chip` + `#personaList` สลับผู้ใช้ — prototype-only)
- คน = `.avatar.is-person` วงกลมพื้นดำ icon user (U17) · `#page-content` = หน้ารายการ

## §4 Page Anatomy
### P-01 รายการ (`renderPage()`)
- `.ph`: `.ph-title` + `.ph-en` "(Exit Interview)" · `.ph-sub` คำอธิบาย + `.ph-badge` (รายการ · ร่าง n · ส่งแล้ว n — ค่า 0 ไม่แสดง) · `.ph-actions`: ส่งออก CSV (`exportCSV()`) · สร้างแบบสอบถาม `#btnCreate` (`startWizard()` · disabled เมื่อ `DOC.active` false + `.alert-row.is-danger`)
- `.card.list-card` › `.filter-bar`: `#fq` ค้นหา (`onQ()`) · `searchSelectHTML` fst / fsep / fdiv · รีเซ็ต (`resetFilters()`)
- `.table-wrap .table`: เลขที่ (`.code-strong`) · วันที่สร้าง · ผู้ให้ข้อมูล (`personInline()`) · ฝ่าย · ลักษณะการพ้นงาน (pill `SEP`) · วันที่พ้นจากงาน · สถานะเอกสาร (`docPill()`) · ลายเซ็น (`renderSignProgress()` x/y + `.sp-bar`) · ⋮ `.ra-btn` (`openRowMenu()`)
- `pager()` → `.table-footer`: `.pg-size` แสดงต่อหน้า 10/25/50 (`setSize()`) · "x – y จาก N รายการ" · `.pagination` `.pg-btn`
### P-02 wizard (`renderWizard()` · `.drawer-panel.wide`)
- `.dw-head` + `stepper()` 3 ขั้น (`STEPS`) · ขั้น 1 `wizMain()` = `.wz-split` [ `.wz-main` การ์ด `card1()`..`card4()` | `sumCard()` `.wz-sum` sticky ]
- `card1()` #sec1: [HR] combobox `wemp` (`setEmp()`) · `.sys-fields` ข้อมูลจากระบบ · `.track-grid` 2 `.track-card` (`setSep()`) · `bedateHTML('resignDate')` (`pickResign()`) หรือ `.chip-row` ข้อ 5 (`setCe()`) + อื่น ๆ · `.calc-line` อายุตัว/อายุงาน + ปรับ (`toggleAdj()` → `.field-row.three` `setNumF()`) · `.seg-control` ทดลองงาน/ประเภทบุคลากร (`setF1()`) · คุณวุฒิ/สาขา
- `card2()` #sec2: `.rate-tbl` 8 แถวหัวหมวด `.rate-grp` + 26 แถว `#rq-${q}` (id = rq-q01..q26) × 5 `.rate-dot` (`setRate()` soft update ไม่ rebuild) · `#rateCount`
- `card3()` #sec3: `.reason-grid` 21 `.reason` (`toggleReason()`) + `.rk` หมายเลขลำดับ · อื่นๆ `#fOther` · `.rank-list` เลื่อน (`moveReason()`)
- `card4()` #sec4: `.trip.impr` ต่อแถว (`setImpr()` · `removeImpr()`) · `.add-row` "เพิ่มข้อเสนอแนะ" (`addImpr()`) · textarea ความเห็นเพิ่มเติม
- ขั้น 2 `wizAttach()` `.upload-zone` + `#exiFile` (`pickFiles()` · `gateFiles()`) · ขั้น 3 `wizReview()` `.review-card` × 5
- `.dw-footer`: ย้อนกลับ (`wizBack()`) · ยกเลิก (`closeDrawer()`) · ถัดไป `#btnNext` (`wizNext()`) / บันทึกแบบร่าง `#btnDraft` (`saveDraft()`) · บันทึกและส่งแบบสอบถาม `#btnSaveSubmit` (`saveAndSubmit()`)
### P-03 ดู (`renderViewDrawer()` · `.drawer-panel` 920)
- `.dw-head`: `.doc-ident` (eyebrow · `.dw-title` เลขที่ + pill · `.dw-sub` ลักษณะพ้นงาน · วันที่) · `.dw-actions` ปุ่มตามสถานะ + `.drawer-header-divider` + `.top-icon-btn` พิมพ์/ดาวน์โหลด (`genPdf()`)/ปิด
- `.drawer-tabs` (`tabBtn()`): รายละเอียด (`renderDetailTab()`) › PDF Preview (`renderPdfTab()` · `.pdf-slot` `iframe.pdf-frame` srcdoc = `exiPdfDoc()` · `fitPdf()`) › ลายเซ็น / อนุมัติ (`renderSignTab()`) › ประวัติ (`renderHistoryTab()`)

## §5 Component Inventory
| Component | anchor | states |
|---|---|---|
| ปุ่มระดับ (ส่วนที่ 2) | `.rate-dot` | default วงกลมเส้น · hover เส้นเข้ม · `.is-on` พื้น primary + ✓ · แถวขาด `.is-miss` (ข้อความแดง) · disabled — |
| ปุ่มปัจจัย (ส่วนที่ 3) | `.reason` + `.rk` | default · hover · `.is-on` ขอบ primary + เลขลำดับพื้น primary · disabled — |
| track card การพ้นงาน | `.track-card` | default · hover · `.is-on` |
| segmented | `.seg-control` `.seg-item` | `.is-active` |
| ช่องวันที่ พ.ศ. | `.bedate` + `.bd-pop` | ว่าง placeholder · เลือกแล้ว "31 ต.ค. 2569" · วันก่อน min disabled |
| การ์ดหัวข้อ | `.wz-card` | `.is-bad` ขอบแดงเมื่อ validate ไม่ผ่าน |
| combobox | `searchSelectHTML()` / `initSearchSelect()` `.ss-list` | เปิด/ค้นหา/เลือก/ล้าง · Esc ปิด |
| ปุ่มบันทึก | `#btnSaveSubmit` | loading `loader-2` "กำลังบันทึก…" · disabled ระหว่าง `S.busy` |
| ตารางว่าง | `emptyStateHTML()` / `.empty-sub` | รายการว่าง · ค้นหาไม่พบ · sub-table "ไม่มีข้อมูล" |

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
| toast `#toast` | — | `showToast()` | อัตโนมัติ 2.8 วิ |

## §7 Interaction Spec
- Esc chain (`keydown` ใน base kit): combobox/ปฏิทิน (stopPropagation) → modal (`closeModal()`) → drawer (`closeDrawer()`) — e2e S10 ผ่าน
- backdrop = mousedown เท่านั้น (U25): `backdropDown(event, 'drawer'|'modal')` ตรวจ `event.target === currentTarget`
- ปิด wizard ที่ dirty → modal "ทิ้งข้อมูลที่กรอกไว้?" · แก้จาก view = ปิด view ก่อนแล้วเปิด wizard (ไม่ซ้อน)
- validate เมื่อกด ถัดไป/บันทึก เท่านั้น → `validateMain()` + `failMain()` เลื่อนไปการ์ดแรกที่ผิด (`firstErrSec()`)
- soft update ส่วนที่ 2 (`setRate()`) และตัวเลขปรับเอง (`setNumF()`) — ไม่ rebuild focus ไม่หลุด
- row menu render ไอคอนเฉพาะในเมนู (data-rmic) กันคลิกทะลุ

## §8 State-Driven UI Matrix
| status | pill (`DOC_ST`) | ปุ่มหัว drawer (เจ้าของ) | ปุ่มหัว drawer (HR) | ⋮ |
|---|---|---|---|---|
| draft | ร่าง `pill-muted` | ยกเลิก · แก้ไข · ส่งแบบสอบถาม | ยกเลิกเอกสาร (ถ้าไม่ใช่ผู้สร้าง) / ชุดเจ้าของ (ถ้าสร้างแทน) | ดูรายละเอียด · แก้ไข · พิมพ์ · ยกเลิกเอกสาร |
| submitted | ส่งแล้ว `pill-success` | ยกเลิกเอกสาร | ยกเลิกเอกสาร | ดูรายละเอียด · พิมพ์ · ยกเลิกเอกสาร |
| pending (เมื่อตั้ง DOA) | รอพิจารณา `pill-warning` | ยกเลิกเอกสาร | ผู้พิจารณา: ส่งกลับแก้ไข · รับทราบ | — |
| approved (เมื่อตั้ง DOA) | พิจารณาแล้ว `pill-success` | — | — | ดู · พิมพ์ |
| cancelled | ยกเลิก `pill-danger` | — | — | ดู · พิมพ์ |
- ลักษณะการพ้นงาน (`SEP`): ลาออก `pill-info` · ไม่จ้างต่อ (ครบสัญญา) `pill-warning`

## §9 Microcopy (verbatim)
### Toast (`showToast`)
| ข้อความ | variant |
|---|---|
| ไม่มีการแจ้งเตือนใหม่ | info |
| แบบเอกสารนี้ยังไม่เปิดใช้งาน | warning |
| แก้ไขได้เฉพาะร่างของตัวเอง | warning |
| กรุณากรอกข้อมูลให้ครบถ้วน | warning |
| บันทึกร่างแล้ว · | info |
| ส่งแบบสอบถามแล้ว · | info |
| รับทราบแล้ว · | info |
| ส่งออก | info |
| สลับเป็น | info |
| แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง | error |
- toast ประกอบ: "บันทึกร่างแล้ว · " + เลขที่ · "ส่งแบบสอบถามแล้ว · " + เลขที่ · "ยกเลิกเอกสารแล้ว · " + เลขที่ · "ส่งกลับแล้ว · " + เลขที่ · "ส่งออก " + n + " รายการ" · "สลับเป็น " + ชื่อ · "ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง" · "ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่" · "คุณไม่มีสิทธิ์ทำรายการนี้"
### ข้อความบนจอ (สกัดจาก HTML)
- · กลับเป็นร่างเลขเดิม
- · ส่งแล้ว ล็อกแก้ไข
- · ส่งแล้ว — ยกเลิกแล้วใช้ต่อไม่ได้
- ก.ค.
- ก.พ.
- ก.ย.
- กมลชนก ใจงาม
- กรกฎาคม
- กรรมการผู้จัดการ
- กรุณากรอกข้อมูลให้ครบถ้วน
- กลับภูมิลำเนาเดิม
- กะการทำงาน
- กันยายน
- การจัดการทรัพยากรมนุษย์
- การจัดการโลจิสติกส์
- การตลาด
- การบัญชี
- การพ้นจากงาน
- การสื่อสารนโยบายใหม่
- กำลังเปิดหน้าต่างพิมพ์ ·
- กุมภาพันธ์
- ขอบคุณสำหรับโอกาสในการทำงาน
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลยังไม่ครบ — แก้ไขร่างให้ครบก่อนส่ง
- ข้อมูลเอกสาร
- ข้อมูลแบบสอบถาม
- ข้อมูลไม่ครบ ขอรายละเอียดเพิ่ม
- ข้าม
- ครบโครงการชั่วคราวตามสัญญา
- ความคิดเห็น/ข้อเสนอแนะอื่นๆ เพิ่มเติม
- ความคิดเห็นเพิ่มเติม
- คะแนนเฉลี่ย
- คำนวณอัตโนมัติถึง
- คุณภาพชีวิตการทำงานไม่ดี
- คุณวุฒิ / สาขา
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค้นหา...
- ค้นหาพนักงานที่พ้นจากงาน
- ค้นหาเลขที่ / ชื่อ / รหัสพนักงาน / แผนก
- งานน่าเบื่อ จำเจ ไม่มีโอกาสเรียนรู้งานใหม่ ๆ
- งานเสี่ยงอันตราย
- จาก 5
- ชนิดไฟล์ไม่รองรับ
- ชี้แจงก่อนประกาศใช้อย่างน้อย 2 สัปดาห์
- ชื่อ-นามสกุล
- ชื่อฟังก์ชัน
- ช่างกลโรงงาน
- ช่างซ่อมบำรุง
- ณัฐชา บุญมา
- ดาวน์โหลด PDF
- ต.ค.
- ตรวจสอบและยืนยัน
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตำแหน่ง
- ตุลาคม
- ต้อง
- ทดลองงาน / ประเภท
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ทุกฝ่าย
- ทุกลักษณะการพ้นงาน
- ทุกสถานะ
- ธ.ค.
- ธนพล ศรีวงศ์
- ธันวาคม
- นักวิเคราะห์ข้อมูล
- นโยบายการบริหารงานของหน่วยงาน
- น้อย
- น้อยที่สุด
- บริษัท ตัวอย่าง จำกัด
- บริหารธุรกิจ
- บันทึกซ้ำ
- บันทึกผิดคน
- บันทึกร่างแล้ว ·
- ประกอบธุรกิจ/อาชีพส่วนตัว
- ประกาศตารางกะล่วงหน้า 1 เดือน
- ประวัติ
- ประเภทบุคลากร
- ประเสริฐ มั่นคง
- ปรับ
- ปรับเอง
- ปริญญาตรี
- ปริญญาโท
- ปวส.
- ปัจจัย · อันดับ 1
- ปัจจัยอันดับ 1
- ปัจจัยอันดับ 2
- ปัจจัยอันดับ 3
- ปัญหาการเดินทาง
- ปัญหาสุขภาพ
- ปัญหาส่วนตัว/ปัญหาครอบครัว
- ปานกลาง
- ปิยะนุช แก้วมณี
- ผู้จัดการฝ่ายขาย
- ผู้จัดการฝ่ายบุคคล
- ผู้จัดการฝ่ายปฏิบัติการ
- ผู้ช่วยเจ้าหน้าที่คลังสินค้า
- ผู้รับเรื่อง
- ผู้ให้ข้อมูล
- ฝ่าย
- ฝ่ายกลยุทธ์
- ฝ่ายขายและการตลาด
- ฝ่ายทรัพยากรบุคคล
- ฝ่ายบัญชีและการเงิน
- ฝ่ายบุคคลรับทราบ
- ฝ่ายบุคคลได้รับแบบสอบถามแล้ว
- ฝ่ายปฏิบัติการ
- พ.ค.
- พ.ย.
- พนักงานขายหน้าร้าน
- พนักงานยื่นลาออก
- พนักงานเปลี่ยนใจไม่ลาออก
- พนักงานเปลี่ยนใจไม่ลาออก — ได้รับการปรับตำแหน่ง
- พฤศจิกายน
- พฤษภาคม
- พิจารณาแล้ว
- พิจารณาในระบบ
- พิมพ์
- พ้นทดลองงาน
- ม.ค.
- มกราคม
- มัธยมศึกษาตอนปลาย
- มากที่สุด
- มิ.ย.
- มิถุนายน
- มี.ค.
- มีนาคม
- มีปัญหาความสัมพันธ์กับหัวหน้างาน
- มีปัญหาความสัมพันธ์กับหัวหน้าหน่วยงาน
- มีปัญหาความสัมพันธ์กับเพื่อนร่วมงาน
- ยกเลิก
- ยกเลิกเอกสาร
- ยกเลิกเอกสารแล้ว ·
- ยังเป็นร่าง — ตอบครบแล้วกดส่งแบบสอบถาม
- ยังไม่ถึง
- ยังไม่พ้นทดลองงาน
- ยังไม่มีข้อมูล
- ยังไม่มีแบบสอบถาม
- ยังไม่ส่ง
- ยังไม่ได้ตอบ
- ยังไม่ได้เลือก
- ย้อนกลับ
- รหัสพนักงาน
- รอพิจารณา
- รอส่ง
- ระบุปัจจัยอื่น
- ระบุเหตุผล
- รับทราบ
- รับทราบแล้ว ·
- รายการ
- รายละเอียด
- ร่าง
- ลบข้อนี้
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ลักษณะการพ้นงาน
- ลักษณะการพ้นจากงาน
- ลายเซ็น / อนุมัติ
- ลาออก
- ลำดับการลงนาม
- ลูกจ้างชั่วคราว
- ลูกจ้างประจำ
- ล้างตัวกรอง
- วรวุฒิ ทองดี
- วันที่ ........./........./.........
- วันที่พ้นจากงาน
- วันที่พ้นจากงานไม่ตรงกับระบบ
- วันที่ลาออก
- วันที่สร้าง
- วันที่เริ่มปฏิบัติงาน
- วันสิ้นสุดสัญญา
- วิชัย บริหารดี
- วิศวกรรมอุตสาหการ
- ศศิธร มีสุข
- ศิลป์-คำนวณ
- ศึกษาต่อ
- ส.ค.
- สถานะ
- สถิติ
- สมชาย ทดสอบดี
- สร้าง PDF
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างแทน
- สร้างแบบสอบถาม
- สร้างแบบสอบถามเมื่อพนักงานแจ้งพ้นจากงาน
- สร้างโดย
- สลับเป็น
- สวัสดิการ/สิทธิประโยชน์น้อยกว่าที่ต้องการ
- สังกัด
- สังกัดฝ่าย
- สังกัดแผนก
- สัญญาจ้างสิ้นสุด
- สำนักกรรมการผู้จัดการ
- สิงหาคม
- ส่งกลับ
- ส่งกลับแก้ไข
- ส่งกลับแล้ว ·
- ส่งออก
- ส่งแบบสอบถาม
- ส่งแบบสอบถาม?
- ส่งแบบสอบถามแล้ว ·
- ส่งแล้ว
- ส่งแล้วแก้ไขไม่ได้ — ถ้าต้องเปลี่ยน ให้ฝ่ายบุคคลยกเลิกแล้วสร้างใหม่
- ส่งในระบบ
- ส่วนที่ 1 ข้อมูลบุคลากร
- อนุชา พรหมสุข
- อายุงาน
- อายุตัว
- อายุตัว / อายุงาน
- อื่น ๆ
- อื่นๆ โปรดระบุ
- อุปกรณ์ป้องกันอันตราย
- เงินเดือน/ค่าตอบแทนน้อยกว่าที่ต้องการ
- เจ้าหน้าที่ขาย
- เจ้าหน้าที่บัญชี
- เฉลี่ย
- เช่น บริหารธุรกิจ
- เช่น ปริญญาตรี
- เดือนถัดไป
- เด้งกลับบน
- เปลี่ยนรอบอุปกรณ์ตามอายุการใช้งาน
- เป็นความประสงค์ของพนักงานฯ
- เป็นความประสงค์ของหน่วยงาน/ส่วนงาน
- เพิ่มเติม
- เม.ย.
- เมษายน
- เลขที่
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกประเทศ
- เลือกผู้พิจารณา
- เลือกวันที่
- เลือกอย่างน้อย 1 ปัจจัย
- เลือกเหตุผลกรณีครบสัญญาจ้าง
- เลื่อนขึ้น
- เสร็จ
- เหตุผลที่ยกเลิก
- เอกสารลับ — เห็นได้เฉพาะผู้ให้ข้อมูลและฝ่ายบุคคล
- เอกสารแนบ
- แก้ไขร่าง
- แก้ไขล่าสุด
- แก้ไขเอกสาร
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งผู้ให้ข้อมูลว่าต้องแก้อะไร
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบสอบถามบุคลากรที่พ้นจากงาน
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- แผนก
- แผนกขายปลีก
- แผนกขายในประเทศ
- แผนกคลังสินค้า
- แผนกซ่อมบำรุง
- แผนกบัญชี
- แผนกบุคคล
- แผนกวางแผน
- โปรดกรอก
- ได้งานใหม่ที่ชอบมากกว่า
- ไม่ถนัดกับงานที่ได้รับมอบหมาย
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่มีพี่เลี้ยงช่วยสอน/แนะนำงาน ถ่ายทอดประสบการณ์
- ไม่มีสาย
- ไม่ยกเลิก
- ไม่เข้าใจ/ขาดทักษะในงาน
- ไม่เห็นโอกาสความก้าวหน้าในอาชีพการงาน
- ไม่ได้รับความเป็นธรรมจากผู้บังคับบัญชา

## §10 Data Binding & BACKEND anchors
| prototype | ระบบจริง (02_API) |
|---|---|
| `EMP` + `empOf()` | API-03 prefill (F-EMP-001 / F-ORG-001) |
| `RECS` + `listRows()` + `canSee()` | API-01/02 (FN-10 ความลับ) |
| `persist()` (`SEQ` + `DOC.prefix`) | API-04/05 · ENG-DOC-NUM (FN-03) |
| `MOCK_DOA_RESOLVED` / `resolveDoa()` (DOA-ENGINE-HOOK · steps = 0) | API-06/07 GET /doa/resolve |
| `confirmSubmit()` / `confirmApprove()` / `confirmReason()` | API-07 / API-08 / API-09 |
| `docPrintData()` + `tplRender()` + `EXI_TPL` | API-10 render ฝั่ง server (parity) |
| `exportCSV()` | API-11 |
| `gateFiles()` / `FILE_ACCEPT` | API-12 Document Center |
| `autoCalc()` / `ymd()` | FN-02 calc (ทำซ้ำฝั่ง server) |

## §11 Traceability + Drift Log
| Brief | FRD | HTML |
|---|---|---|
| §4 P-01 | 01_UI P-01 · API-01/11 | `renderPage()` |
| §4 P-02 | 01_UI P-02 · API-03/04/05 · BR-01..05 | `renderWizard()` |
| §4 P-03 | 01_UI P-03 · API-02/09/10 | `renderViewDrawer()` |
| §8 | 05 §5.2 · §5.3 | `DOC_ST` · `canEdit()` · `canCancel()` |
### ⚠️ Drift Log
| รายการ | ชนิด | ข้อเสนอ |
|---|---|---|
| `__QA__` · `switchPersona()` · `S.sim` · `commitRejected()` | HTML-only (prototype) | ไม่ทำในระบบจริง |
| pending/approved/รับทราบ | FRD+HTML รองรับแต่ค่าเริ่มไม่ใช้ (DEC-03) | เปิดเมื่อลูกค้าตั้งขั้นที่ DOA กลาง (OQ-02) |
| โลโก้ในแบบพิมพ์ = placeholder | HTML-only | ระบบจริงใช้ header_snapshot (Organization) |

## §12 Diff จากเวอร์ชันก่อน
— ไม่มีใน HTML นี้ (เวอร์ชันแรก)

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- รายงานสรุปคะแนนเฉลี่ยต่อหมวด/ปัจจัยยอดนิยม (ใช้ข้อมูล CSV) — รอบถัดไป
