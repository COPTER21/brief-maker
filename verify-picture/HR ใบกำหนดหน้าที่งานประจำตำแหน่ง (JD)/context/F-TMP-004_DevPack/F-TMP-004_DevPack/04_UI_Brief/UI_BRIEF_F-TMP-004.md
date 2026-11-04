# UI_BRIEF — F-TMP-004 ใบกำหนดหน้าที่งานประจำตำแหน่ง (Job Description)

## §0 Document Control + Pairing
| รายการ | ค่า |
|---|---|
| HTML | feature.html (html-generator-v9.4 · archetype `Q-form` · `window.__QA__` มี) |
| FRD | FRD_F-TMP-004_Pack (01_UI P-01..P-03 · 02_API · 05_RULES) — pair แล้ว |
| DECISIONS.lock | 17 มติ (AI-DEFAULT 12 · VALID 5) — ทุกมติ AI-DEFAULT รอลูกค้ายืนยัน |
| แบบพิมพ์ | print/form.tpl.html (thai-doc v2.1 Replica FM-HRM-32) ฝังเป็น `JD_TPL` |
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
| `#/job-description` | หน้ารายการ (default) | `applyRoute()` |
| `#/job-description/view/:id` | drawer ดู (ตรวจ `canSee()` ก่อน — ไม่มีสิทธิ์ = ไม่เปิด) | `showDrawer()` |
| `#/job-description/create` | wizard สร้าง | `startWizard()` |
| `#/job-description/edit/:id` | wizard แก้ร่าง (ตรวจ `canEdit()`) | `startWizard()` |
- refresh-safe: `hashchange` → `applyRoute()` · ปิด drawer → `go()` กลับ route รายการ

## §3 Layout Shell
- `.sidebar` ดำ (เมนู HR › ใบกำหนดหน้าที่งาน (JD) + `#sbBadge` = จำนวนใบที่รอฉันอนุมัติ/รับทราบ) · `.shell-bar` ขาว (breadcrumb Core › HR › ใบกำหนดหน้าที่งานประจำตำแหน่ง · กระดิ่ง · `.user-chip` + `#personaList` สลับผู้ใช้ — prototype-only)
- คน = `.avatar.is-person` วงกลมพื้นดำ icon user (U17) · `#page-content` = หน้ารายการ

## §4 Page Anatomy
### P-01 รายการ (`renderPage()`)
- `.ph`: `.ph-title` + `.ph-en` "(Job Description)" · `.ph-sub` คำอธิบาย + `.ph-badge` (รายการ · รออนุมัติ n · รอคุณ n — ค่า 0 ไม่แสดง) · `.ph-actions`: ส่งออก CSV (`exportCSV()`) · สร้างใบกำหนดหน้าที่งาน `#btnCreate` (`startWizard()` · disabled เมื่อ `DOC.active` false + `.alert-row.is-danger`)
- `.card.list-card` › `.filter-bar`: `#fq` ค้นหา (`onQ()`) · `searchSelectHTML` fst / fdiv · รีเซ็ต (`resetFilters()`)
- `.table-wrap .table`: เลขที่ (`.code-strong`) · วันที่สร้าง · ตำแหน่ง · แผนก · ฝ่าย · ผู้จัดทำ (`personInline()`) · สถานะเอกสาร (`docPill()`) · ลายเซ็น (`renderSignProgress()` x/y + `.sp-bar`) · ⋮ `.ra-btn` (`openRowMenu()`)
- `pager()` → `.table-footer`: `.pg-size` แสดงต่อหน้า 10/25/50 (`setSize()`) · "x – y จาก N รายการ" · `.pagination` `.pg-btn`
### P-02 wizard (`renderWizard()` · `.drawer-panel.wide`)
- `.dw-head` + `stepper()` 3 ขั้น (`STEPS`) · ขั้น 1 `wizMain()` = `.wz-split` [ `.wz-main` การ์ด `card1()` · `cardText()` ×5 · `cardOrg()` · `cardAck()` | `sumCard()` `.wz-sum` sticky ]
- `card1()` #sec1: combobox `wpos` (`setPos()`) · `.sys-fields` แผนก/ฝ่าย · ชื่อตำแหน่งอังกฤษ `#fNameEn` (`setF1()`) · รายงานต่อ `#fRep` (`setRep()`) · `.calc-line` ผู้ใต้บังคับบัญชา `#cSub`
- `cardText()` #sec-purpose / #sec-resp / #sec-spec / #sec-kpi / #sec-other: textarea (`setText()` soft update · `#sumSec`)
- `cardOrg()` #sec-org: `#repWarn` เตือนหัวหน้าแถวแรกไม่ตรงรายงานต่อ (`repWarnHTML()`) · `.org-2col` 2 คอลัมน์ `rowCards()` → `.trip.org-row` (ตำแหน่ง: · จำนวน (คน) `inputmode=numeric` · `setRow()` soft update) · ลบแถว `removeRow()` · `.add-row` เพิ่มหัวหน้า/เพิ่มลูกน้อง (`addRow()`) · `#posList` datalist
- `cardAck()` #sec-ack: combobox `wack` (`setAck()`)
- ขั้น 2 `wizAttach()` `.upload-zone` + `#jdFile` (`pickFiles()` · `gateFiles()`) · ขั้น 3 `wizReview()` `.review-card`
- `.dw-footer`: ย้อนกลับ (`wizBack()`) · ยกเลิก (`closeDrawer()`) · ถัดไป `#btnNext` (`wizNext()`) / บันทึกแบบร่าง `#btnDraft` (`saveDraft()`) · บันทึกและส่งอนุมัติ `#btnSaveSubmit` (`saveAndSubmit()`)
### P-03 ดู (`renderViewDrawer()` · `.drawer-panel` 920)
- `.dw-head`: `.doc-ident` (eyebrow · `.dw-title` เลขที่ + pill · `.dw-sub` ชื่อตำแหน่ง) · `.dw-actions` ปุ่มตามสถานะ (`#btnSubmitView` · `#btnApproveView` · `#btnAckView`) + `.drawer-header-divider` + `.top-icon-btn` พิมพ์/ดาวน์โหลด (`genPdf()`)/ปิด
- `.drawer-tabs` (`tabBtn()`): รายละเอียด (`renderDetailTab()` · `viewBanner()` · `orgTable()` · `.jd-text`) › PDF Preview (`renderPdfTab()` · `.pdf-slot` `iframe.pdf-frame` srcdoc = `jdPdfDoc()` · `fitPdf()`) › ลายเซ็น / อนุมัติ (`renderSignTab()` · อนุมัติ/ไม่อนุมัติ inline · รับทราบ · ระบุผู้ดำรงตำแหน่ง `openAssignAck()`) › ประวัติ (`renderHistoryTab()`)

## §5 Component Inventory
| Component | anchor | states |
|---|---|---|
| การ์ดหัวข้อ | `.wz-card` | default · `.is-bad` ขอบแดงเมื่อ validate ไม่ผ่าน |
| การ์ดแถวหัวหน้า/ลูกน้อง | `.trip.org-row` | default · `.is-bad` + `.trip-err` ข้อความแรก · ลบแถวหัวหน้าแถวเดียว disabled |
| บรรทัดคำนวณ/เตือน | `.pd-line` | ปกติ · `.is-warn` (หัวหน้าไม่ตรงรายงานต่อ — ไม่บล็อก) |
| combobox | `searchSelectHTML()` / `initSearchSelect()` `.ss-list` | เปิด/ค้นหา/เลือก/ล้าง · Esc ปิด |
| ปุ่มบันทึก | `#btnSaveSubmit` | loading `loader-2` "กำลังบันทึก…" · disabled ระหว่าง `S.busy` |
| ข้อความหลายบรรทัด (ดู) | `.jd-text` | white-space pre-line |
| ตารางว่าง | `emptyStateHTML()` / `.empty-sub` | รายการว่าง · ค้นหาไม่พบ · sub-table "ไม่มี" |

## §6 Overlay Registry
| overlay | ขนาด | เปิด | dismiss |
|---|---|---|---|
| drawer ดู `.drawer` | 920 | `openView()` / `showDrawer()` | ปุ่ม x · Esc · mousedown ที่ `#drawerBackdrop` (`backdropDown()`) |
| drawer wizard `.drawer-panel.wide` | 1290 | `startWizard()` | เหมือนบน · กรอกค้าง = modal discard |
| modal `.modal` (`renderModal()`) | ส่ง = `.modal.is-lg` | `openModalCfg()` (submit · approve · reject · cancel · ack · assignAck · discard) | Esc · ปุ่ม · mousedown ที่ `#modalBackdrop` (ไม่ปิดถ้าพิมพ์เหตุผลแล้ว — `modalBackdropClick()`) |
| row menu ⋮ `.row-menu` | 180 | `openRowMenu()` (portal `#overlay-root`) | คลิกที่อื่น · scroll (`closeRowMenu()`) |
| user menu `.user-menu` | — | `toggleUserMenu()` | คลิกที่อื่น |
| combobox `.ss-list` | ตามช่อง | ช่อง | เลือก · คลิกที่อื่น · Esc |
| toast `#toast` | — | `showToast()` | อัตโนมัติ 2.8 วิ |

## §7 Interaction Spec
- Esc chain (`keydown` ใน base kit): combobox (stopPropagation) → modal (`closeModal()`) → drawer (`closeDrawer()`) — e2e S10 ผ่าน
- backdrop = mousedown เท่านั้น (U25): `backdropDown(event, 'drawer'|'modal')` ตรวจ `event.target === currentTarget`
- ปิด wizard ที่ dirty → modal "ทิ้งข้อมูลที่กรอกไว้?" · แก้จาก view = ปิด view ก่อนแล้วเปิด wizard (ไม่ซ้อน)
- validate เมื่อกด ถัดไป/บันทึก เท่านั้น → `validateMain()` + `failMain()` เลื่อนไปการ์ดแรกที่ผิด (`firstErrSec()`)
- soft update: `setText()` · `setRow()` · `setRep()` — ไม่ rebuild focus ไม่หลุด · จำนวน (คน) ตัดเหลือตัวเลข
- อนุมัติขั้นสุดท้าย → `supersedeOld()` เปลี่ยนฉบับเดิมของตำแหน่งเป็น "ถูกแทนที่"
- row menu render ไอคอนเฉพาะในเมนู (data-rmic) กันคลิกทะลุ

## §8 State-Driven UI Matrix
| status | pill (`DOC_ST`) | ปุ่มหัว drawer | ⋮ |
|---|---|---|---|
| draft | ร่าง `pill-muted` | เจ้าของ: ยกเลิก · แก้ไข · ส่งอนุมัติ | ดูรายละเอียด · แก้ไข · พิมพ์ · ยกเลิกเอกสาร |
| pending | รออนุมัติ `pill-warning` | ผู้อนุมัติขั้นปัจจุบัน: ไม่อนุมัติ · อนุมัติ / เจ้าของ·HR: ยกเลิกเอกสาร | ดูรายละเอียด · พิมพ์ · ยกเลิกเอกสาร |
| approved | อนุมัติแล้ว `pill-success` | ผู้ดำรงตำแหน่ง: รับทราบ · HR: ระบุ/เปลี่ยนผู้ดำรงตำแหน่ง (แท็บลายเซ็น) | ดูรายละเอียด · รับทราบ · พิมพ์ |
| acknowledged | รับทราบแล้ว `pill-info` | — | ดู · พิมพ์ |
| superseded | ถูกแทนที่ `pill-muted` | — | ดู · พิมพ์ |
| cancelled | ยกเลิก `pill-danger` | — | ดู · พิมพ์ |

## §9 Microcopy (verbatim)
### Toast (`showToast`)
| ข้อความ | variant |
|---|---|
| ไม่มีการแจ้งเตือนใหม่ | info |
| แบบเอกสารนี้ยังไม่เปิดใช้งาน | warning |
| แก้ไขได้เฉพาะร่างของตัวเอง | warning |
| กรุณากรอกข้อมูลให้ครบถ้วน | warning |
| บันทึกร่างแล้ว · | info |
| ส่งอนุมัติแล้ว · | info |
| อนุมัติแล้ว · | info |
| รับทราบแล้ว · | info |
| แจ้งผู้ดำรงตำแหน่งให้รับทราบแล้ว · | info |
| ส่งออก | info |
| สลับเป็น | info |
| แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง | error |
- toast ประกอบ: "บันทึกร่างแล้ว · " + เลขที่ · "ส่งอนุมัติแล้ว · " + เลขที่ · "อนุมัติแล้ว · " + เลขที่ · "รับทราบแล้ว · " + เลขที่ · "ไม่อนุมัติ — ส่งกลับเป็นร่างแล้ว · " + เลขที่ · "ยกเลิกเอกสารแล้ว · " + เลขที่ · "แจ้งผู้ดำรงตำแหน่งให้รับทราบแล้ว · " + ชื่อ · "ส่งออก " + n + " รายการ" · "สลับเป็น " + ชื่อ · "ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง" · "ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่" · "คุณไม่มีสิทธิ์ทำรายการนี้"
### ข้อความบนจอ (สกัดจาก HTML)
- 1 บรรทัดต่อ 1 ตัวชี้วัด พร้อมเป้าหมาย
- 1 บรรทัดต่อ 1 หน้าที่ เช่น 1. ตรวจสอบเอกสาร…
- 1. ความถูกต้องของสต๊อก ≥ 99.5%
- 1. ปิดอัตราภายใน 45 วัน ≥ 80%
- KPI ยังวัดผลไม่ได้ ขอปรับให้มีตัวเลข
- · กลับเป็นร่างเลขเดิมให้ผู้จัดทำแก้ไข
- · รออนุมัติอยู่ — ผู้อนุมัติจะได้รับแจ้ง
- · ส่งแล้ว ล็อกแก้ไข
- ก.ค.
- ก.พ.
- ก.ย.
- กมลชนก ใจงาม
- กรกฎาคม
- กรรมการผู้จัดการ
- กรอกจำนวนแล้วต้องระบุตำแหน่ง
- กรุณากรอกขอบเขตความรับผิดชอบหลัก
- กรุณากรอกข้อมูลให้ครบถ้วน
- กรุณากรอกคุณสมบัติประจำตำแหน่ง
- กรุณากรอกตัวชี้วัดผลการดำเนินงาน
- กรุณากรอกวัตถุประสงค์ของตำแหน่งงาน
- กรุณาระบุตำแหน่งหัวหน้าอย่างน้อย 1 แถว
- กันยายน
- กำลังเปิดหน้าต่างพิมพ์ ·
- กุมภาพันธ์
- ขอบเขตความรับผิดชอบยังไม่ครบ
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลยังไม่ครบ — แก้ไขร่างให้ครบก่อนส่ง
- ข้อมูลใบกำหนดหน้าที่
- ข้อมูลใบกำหนดหน้าที่งาน
- ข้าม
- ควบคุมงานคลังสินค้าให้รับ-จ่ายถูกต้องและทันเวลา
- ควบคุมงานบัญชีทั่วไป เจ้าหนี้ ลูกหนี้ ให้ปิดบัญชีได้ตามกำหนด
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค้นหา...
- ค้นหาตำแหน่งจากผังองค์กร
- ค้นหาเลขที่ / ตำแหน่ง / แผนก / ผู้จัดทำ
- ชนิดไฟล์ไม่รองรับ
- ชื่อตำแหน่ง
- ชื่อตำแหน่งอังกฤษ
- ชื่อฟังก์ชัน
- ณัฐชา บุญมา
- ดาวน์โหลด PDF
- ดูแลการวางบิล ติดตามรับชำระ และควบคุมอายุลูกหนี้ให้อยู่ในเกณฑ์
- ต.ค.
- ตรวจสอบและยืนยัน
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตำแหน่ง
- ตำแหน่งที่รายงานต่อ
- ตำแหน่งนี้มีไว้เพื่อ…
- ตุลาคม
- ต้อง
- ถูกแทนที่
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ทุกฝ่าย
- ทุกสถานะ
- ธ.ค.
- ธนพล ศรีวงศ์
- ธันวาคม
- บริษัท ตัวอย่าง จำกัด
- บริหารงานปฏิบัติการคลังสินค้าและขนส่งให้บรรลุเป้าหมายต้นทุนและบริการ
- บังคับ
- บันทึกซ้ำ
- บันทึกร่างแล้ว ·
- ประวัติ
- ประเสริฐ มั่นคง
- ปริญญาตรี · ประสบการณ์คลังสินค้า 3 ปีขึ้นไป
- ปริญญาตรี สาขาการจัดการทรัพยากรมนุษย์ หรือที่เกี่ยวข้อง
- ปริญญาตรี สาขาการบัญชี · ประสบการณ์ 1 ปีขึ้นไป
- ปริญญาตรี สาขาการบัญชี · ประสบการณ์ 5 ปีขึ้นไป · ผู้ทำบัญชีตามกฎหมาย
- ปริญญาตรีขึ้นไป · ประสบการณ์บริหาร 8 ปีขึ้นไป
- ปิยะนุช แก้วมณี
- ผังโครงสร้างแผนกบัญชี.pdf
- ผู้จัดการฝ่ายบัญชีและการเงิน
- ผู้จัดการฝ่ายบุคคล
- ผู้จัดการฝ่ายปฏิบัติการ
- ผู้จัดทำ
- ผู้ดำรงตำแหน่ง
- ผู้ดำรงตำแหน่งรับทราบ
- ผู้บังคับบัญชาโดยตรงไม่ตรงผังองค์กร
- ผู้ใต้บังคับบัญชา
- ฝ่าย
- ฝ่ายทรัพยากรบุคคล
- ฝ่ายบัญชีและการเงิน
- ฝ่ายบุคคล
- ฝ่ายปฏิบัติการ
- พ.ค.
- พ.ย.
- พนักงานคลังสินค้า
- พฤศจิกายน
- พฤษภาคม
- พิมพ์
- ม.ค.
- มกราคม
- มัธยมศึกษาตอนปลายขึ้นไป · ขับรถยกได้จะพิจารณาเป็นพิเศษ
- มิ.ย.
- มิถุนายน
- มี.ค.
- มีนาคม
- ยกเลิก
- ยกเลิกเอกสาร
- ยกเลิกเอกสารแล้ว ·
- ยังเป็นร่าง — กรอกครบแล้วกดส่งอนุมัติ
- ยังไม่ถึง
- ยังไม่มีข้อมูล
- ยังไม่มีใบกำหนดหน้าที่งาน
- ยังไม่รับทราบ
- ยังไม่ส่ง
- ยังไม่ได้เลือก
- ยุบ/ปรับโครงสร้างตำแหน่ง
- ย้อนกลับ
- รอรับทราบ
- รออนุมัติ
- ระบบ
- ระบุผู้ดำรงตำแหน่ง
- รับ จัดเก็บ และจ่ายสินค้าให้ถูกต้องตามเอกสาร
- รับทราบ
- รับทราบแล้ว
- รับทราบแล้ว ·
- รับทราบในระบบ
- รายการ
- รายงานต่อ
- รายละเอียด
- ร่าง
- ลบแถว
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ละเอียดรอบคอบ · ทำงานเป็นทีม
- ลายเซ็น
- ลายเซ็น / อนุมัติ
- ลำดับการลงนาม
- ลูกน้อง
- ล้างตัวกรอง
- วรวุฒิ ทองดี
- วันที่ ........./........./.........
- วันที่สร้าง
- วิชัย บริหารดี
- วุฒิการศึกษา · ประสบการณ์ · ทักษะ
- ศศิธร มีสุข
- ส.ค.
- สถานะ
- สถานะเอกสาร
- สมศรี ทดสอบงาน
- สรรหาและคัดเลือกบุคลากรให้ทันตามแผนอัตรากำลัง
- สร้าง PDF
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างโดย
- สร้างใบกำหนดหน้าที่งาน
- สร้างใบกำหนดหน้าที่งานให้ตำแหน่งในหน่วยงานของคุณ
- สลับเป็น
- สำนักกรรมการผู้จัดการ
- สิงหาคม
- สุขภาพแข็งแรง
- ส่งอนุมัติ
- ส่งอนุมัติแล้ว ·
- ส่งอนุมัติใบกำหนดหน้าที่งาน?
- ส่งออก
- ส่งในระบบ
- หัวหน้า
- หัวหน้าแผนกคลังสินค้า
- หัวหน้าแผนกบัญชี
- อนุชา พรหมสุข
- อนุมัติ
- อนุมัติแล้ว
- อนุมัติแล้ว ·
- อนุมัติใบกำหนดหน้าที่งานนี้?
- เจ้าหน้าที่บัญชีลูกหนี้
- เจ้าหน้าที่บัญชีเจ้าหนี้
- เจ้าหน้าที่สรรหาบุคลากร
- เช่น Accounts Payable Officer
- เดือนถัดไป
- เด้งกลับบน
- เพิ่มลูกน้อง
- เพิ่มหัวหน้า
- เพิ่มเติม
- เม.ย.
- เมษายน
- เลขที่
- เลขที่เอกสาร
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกตำแหน่งผิด
- เลือกประเทศ
- เลือกผู้อนุมัติ
- เลือกพนักงาน
- เลือกวันที่
- เหตุผลที่ยกเลิก
- เอกสารแนบ
- แก้ไขร่าง
- แก้ไขล่าสุด
- แก้ไขเอกสาร
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งผู้จัดทำว่าต้องแก้อะไร
- แจ้งผู้ดำรงตำแหน่งให้รับทราบแล้ว ·
- แทนที่ด้วย
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- แผนก
- แผนกคลังสินค้า
- แผนกบัญชี
- แผนกบุคคล
- ใบกำหนดหน้าที่งานประจำตำแหน่ง
- ไม่บังคับ
- ไม่พบผู้บังคับบัญชา — เลือกตอนส่ง
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่มี
- ไม่ยกเลิก
- ไม่ระบุ
- ไม่อนุมัติ
- ไม่อนุมัติ — กลับเป็นร่าง
- ไม่อนุมัติ — ส่งกลับเป็นร่างแล้ว ·
- — กดรับทราบได้ที่ปุ่มด้านบน

## §10 Data Binding & BACKEND anchors
| prototype | ระบบจริง (02_API) |
|---|---|
| `POS` + `posOf()` · `EMP` + `empOf()` | API-03 prefill (Position & Tier / OrgUnit / Employee) |
| `RECS` + `listRows()` + `canSee()` | API-01/02 (FN-12) |
| `persist()` (`SEQ` + `DOC.prefix`) | API-04/05 · ENG-DOC-NUM (FN-03) |
| `MOCK_DOA_RESOLVED` / `resolveDoa()` (DOA-ENGINE-HOOK · 1 ขั้น) | API-06/07 GET /doa/resolve |
| `confirmSubmit()` / `confirmApprove()` / `confirmReason()` | API-07 / API-08 / API-09 |
| `supersedeOld()` | FN-09 (ใน API-08) |
| `confirmAssignAck()` / `confirmAck()` | API-13 / API-14 |
| `docPrintData()` + `tplRender()` + `JD_TPL` | API-10 render ฝั่ง server (parity) |
| `exportCSV()` | API-11 |
| `gateFiles()` / `FILE_ACCEPT` | API-12 Document Center |
| `subSummary()` · `validateMain()` · `rowErr()` | FN-02 (ทำซ้ำฝั่ง server) |

## §11 Traceability + Drift Log
| Brief | FRD | HTML |
|---|---|---|
| §4 P-01 | 01_UI P-01 · API-01/11 | `renderPage()` |
| §4 P-02 | 01_UI P-02 · API-03/04/05 · BR-01..06 | `renderWizard()` |
| §4 P-03 | 01_UI P-03 · API-02/08/09/10/13/14 | `renderViewDrawer()` |
| §8 | 05 §5.2 · §5.3 | `DOC_ST` · `canEdit()` · `canCancel()` · `canAck()` · `canAssignAck()` |
### ⚠️ Drift Log
| รายการ | ชนิด | ข้อเสนอ |
|---|---|---|
| `__QA__` · `switchPersona()` · `S.sim` · `commitRejected()` | HTML-only (prototype) | ไม่ทำในระบบจริง |
| role-line-manager resolve ด้วย `EMP.mgr` | HTML mock | ระบบจริงผ่าน DOA กลาง (OQ-02) |
| โลโก้ในแบบพิมพ์ = placeholder | HTML-only | ระบบจริงใช้ header_snapshot (Organization) |

## §12 Diff จากเวอร์ชันก่อน
— ไม่มีใน HTML นี้ (เวอร์ชันแรก)

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- เชื่อม KPI ใน JD กับ Performance และส่ง JD ไปประกาศรับสมัคร (Recruit) — รอบถัดไป
