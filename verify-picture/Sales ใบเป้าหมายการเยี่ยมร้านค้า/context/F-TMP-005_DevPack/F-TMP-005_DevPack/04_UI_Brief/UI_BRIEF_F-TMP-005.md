# UI_BRIEF — F-TMP-005 ใบเป้าหมายการเยี่ยมร้านค้า : เขตการขาย General Trade

## §0 Document Control + Pairing
| รายการ | ค่า |
|---|---|
| HTML | feature.html (html-generator-v9.4 · archetype `Q-form` · `window.__QA__` มี) |
| FRD | FRD_F-TMP-005_Pack (01_UI P-01..P-03 · 02_API · 05_RULES) — pair แล้ว |
| DECISIONS.lock | 18 มติ (AI-DEFAULT 11 · VALID 7) — ทุกมติ AI-DEFAULT รอลูกค้ายืนยัน |
| แบบพิมพ์ | print/form.tpl.html (thai-doc v2.1 Replica FM-SAL-09) ฝังเป็น `SVT_TPL` |
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
| `#/visit-target` | หน้ารายการ (default) | `applyRoute()` |
| `#/visit-target/view/:id` | drawer ดู (ตรวจ `canSee()` ก่อน — ไม่มีสิทธิ์ = ไม่เปิด) | `showDrawer()` |
| `#/visit-target/create` | wizard สร้าง | `startWizard()` |
| `#/visit-target/edit/:id` | wizard แก้ร่าง (ตรวจ `canEdit()`) | `startWizard()` |
- refresh-safe: `hashchange` → `applyRoute()` · ปิด drawer → `go()` กลับ route รายการ

## §3 Layout Shell
- `.sidebar` ดำ (เมนู › ใบเป้าหมายการเยี่ยมร้านค้า + `#sbBadge` = จำนวนใบที่รอฉันอนุมัติ) · `.shell-bar` ขาว (breadcrumb › ใบเป้าหมายการเยี่ยมร้านค้า · กระดิ่ง · `.user-chip` + `#personaList` สลับผู้ใช้ — prototype-only)
- คน = `.avatar.is-person` วงกลมพื้นดำ icon user (U17) · `#page-content` = หน้ารายการ

## §4 Page Anatomy
### P-01 รายการ (`renderPage()`)
- `.ph`: `.ph-title` "ใบเป้าหมายการเยี่ยมร้านค้า" · `.ph-sub` คำอธิบาย + `.ph-badge` (รายการ · รออนุมัติ n · รอคุณ n — ค่า 0 ไม่แสดง) · `.ph-actions`: ส่งออก CSV (`exportCSV()`) · สร้างใบเป้าหมาย `#btnCreate` (`startWizard()` · disabled เมื่อ `DOC.active` false + `.alert-row.is-danger`)
- `.card.list-card` › `.filter-bar`: `#fq` ค้นหา (`onQ()`) · `searchSelectHTML` fst / fterr · รีเซ็ต (`resetFilters()`)
- `.table-wrap .table`: เลขที่ (`.code-strong`) · รอบการขาย · เขต · ผู้รับผิดชอบเขต (`personInline()`) · วันทำงาน · จำนวนลูกค้า · สถานะเอกสาร (`docPill()`) · ลายเซ็น (`renderSignProgress()` x/y + `.sp-bar`) · ⋮ `.ra-btn` (`openRowMenu()`)
- `pager()` → `.table-footer`: `.pg-size` แสดงต่อหน้า 10/25/50 (`setSize()`) · "x – y จาก N รายการ" · `.pagination` `.pg-btn`
### P-02 wizard (`renderWizard()` · `.drawer-panel.wide`)
- `.dw-head` + `stepper()` 3 ขั้น (`STEPS`) · ขั้น 1 `wizMain()` = `.wz-split` [ `.wz-main` การ์ด `cardHead()` · `cardDays()` | `sumCard()` `.wz-sum` sticky (`#sumDays` · `#sumCust`) ]
- `cardHead()` #sec-head: combobox `wterr` (`setTerr()` — นำร้านนอกเขตออก) · `wcycle` (`setCycle()`) · `.sys-fields` ผู้รับผิดชอบเขต/ตำแหน่ง · TO `wto` #fTo (`setTo()`) · CC `wcc` (`addCc()` · chip `.st-chip` `removeCc()`)
- `cardDays()` #sec-days: `#mkList` datalist ตลาด · `dayCard()` ต่อวัน `.trip.day-row` #day-N: `.day-head` (ลำดับ · จำนวนลูกค้า `.day-cnt` · ลบวัน `removeDay()`) · `.day-fields` [วันที่ `bedateHTML()` จำกัด min/max ตามรอบ → `setDayDate()` · เริ่มต้นตลาด · `.day-eq` "=" · สิ้นสุดตลาด (`setDay()` soft update) · ที่พัก (จังหวัด) combobox `provN` (`setProv()`)] · ร้านค้า combobox `custN` (`addStore()`) + `.st-chips` (`removeStore()`) · `.pd-line.is-warn` เมื่อร้าน > 7 · `.trip-err`
- `.add-row` #btnAddDay "เพิ่มวันทำงาน" (`addDay()` · disabled เมื่อครบ 31)
- ขั้น 2 `wizAttach()` `.upload-zone` + `#svtFile` (`pickFiles()` · `gateFiles()`) · ขั้น 3 `wizReview()` `.review-card` + `dayTable()`
- `.dw-footer`: ย้อนกลับ (`wizBack()`) · ยกเลิก (`closeDrawer()`) · ถัดไป `#btnNext` (`wizNext()`) / บันทึกแบบร่าง `#btnDraft` (`saveDraft()`) · บันทึกและส่งอนุมัติ `#btnSaveSubmit` (`saveAndSubmit()`)
### P-03 ดู (`renderViewDrawer()` · `.drawer-panel` 920)
- `.dw-head`: `.doc-ident` (eyebrow · `.dw-title` เลขที่ + pill · `.dw-sub` เขต · รอบ) · `.dw-actions` ปุ่มตามสถานะ (`#btnSubmitView` · `#btnApproveView`) + `.drawer-header-divider` + `.top-icon-btn` พิมพ์/ดาวน์โหลด (`genPdf()`)/ปิด
- `.drawer-tabs` (`tabBtn()`): รายละเอียด (`renderDetailTab()` · `viewBanner()` · ส่วนหัว · `dayTable()` + `.tbl-total` แถวรวม · แถบเตือนร้าน > 7) › PDF Preview (`renderPdfTab()` · `.pdf-slot` `iframe.pdf-frame` srcdoc = `svtPdfDoc()` · `fitPdf()`) › ลายเซ็น / อนุมัติ (`renderSignTab()` · อนุมัติ/ไม่อนุมัติ inline) › ประวัติ (`renderHistoryTab()`)

## §5 Component Inventory
| Component | anchor | states |
|---|---|---|
| การ์ดหัวข้อ | `.wz-card` | default · `.is-bad` ขอบแดงเมื่อ validate ไม่ผ่าน |
| การ์ดวันทำงาน | `.trip.day-row` | default · `.is-bad` + `.trip-err` ข้อความแรก · ลบวันเมื่อเหลือวันเดียว disabled |
| chip ร้าน/CC | `.st-chip` | ปุ่ม x นำออก |
| บรรทัดเตือน | `.pd-line.is-warn` | ร้าน > 7 (ไม่บล็อก) |
| ตัวเลือกวันที่ | `.bedate` + `#bd-pop` | พ.ศ. · จำกัด min/max ตามรอบการขาย · Esc ปิดเฉพาะปฏิทิน |
| combobox | `searchSelectHTML()` / `initSearchSelect()` `.ss-list` | เปิด/ค้นหา/เลือก/ล้าง · Esc ปิด · ร้าน: ว่าง = "ไม่พบร้านค้าในเขตนี้" / "เลือกเขตก่อน" |
| ปุ่มบันทึก | `#btnSaveSubmit` | loading `loader-2` "กำลังบันทึก…" · disabled ระหว่าง `S.busy` |
| ตารางว่าง | `emptyStateHTML()` / `.empty-sub` | รายการว่าง · ค้นหาไม่พบ · แผนรายวันว่าง |

## §6 Overlay Registry
| overlay | ขนาด | เปิด | dismiss |
|---|---|---|---|
| drawer ดู `.drawer` | 920 | `openView()` / `showDrawer()` | ปุ่ม x · Esc · mousedown ที่ `#drawerBackdrop` (`backdropDown()`) |
| drawer wizard `.drawer-panel.wide` | 1290 | `startWizard()` | เหมือนบน · กรอกค้าง = modal discard |
| modal `.modal` (`renderModal()`) | ส่ง = `.modal.is-lg` | `openModalCfg()` (submit · approve · reject · cancel · discard) | Esc · ปุ่ม · mousedown ที่ `#modalBackdrop` (ไม่ปิดถ้าพิมพ์เหตุผลแล้ว — `modalBackdropClick()`) |
| row menu ⋮ `.row-menu` | 180 | `openRowMenu()` (portal `#overlay-root`) | คลิกที่อื่น · scroll (`closeRowMenu()`) |
| ปฏิทิน `#bd-pop` | — | `bdToggle()` (portal) | เลือก · คลิกที่อื่น · Esc |
| user menu `.user-menu` | — | `toggleUserMenu()` | คลิกที่อื่น |
| combobox `.ss-list` | ตามช่อง | ช่อง | เลือก · คลิกที่อื่น · Esc |
| toast `#toast` | — | `showToast()` | อัตโนมัติ 2.8 วิ |

## §7 Interaction Spec
- Esc chain (`keydown` ใน base kit): ปฏิทิน/combobox (stopPropagation) → modal (`closeModal()`) → drawer (`closeDrawer()`)
- backdrop = mousedown เท่านั้น (U25): `backdropDown(event, 'drawer'|'modal')` ตรวจ `event.target === currentTarget`
- ปิด wizard ที่ dirty → modal "ทิ้งข้อมูลที่กรอกไว้?" · แก้จาก view = ปิด view ก่อนแล้วเปิด wizard (ไม่ซ้อน)
- validate เมื่อกด ถัดไป/บันทึก เท่านั้น → `validateMain()` (`dayErr()` ต่อวัน: วันที่นอกรอบ/ซ้ำ · ตลาดว่าง · ร้าน 0/ซ้ำ) + `failMain()` เลื่อนไปการ์ดแรกที่ผิด (`firstErrSec()`)
- soft update: `setDay()` (ตลาด) · `setTo()` — ไม่ rebuild focus ไม่หลุด · `refreshSum()` อัปเดตการ์ดสรุป
- เลือกร้านซ้ำในวันเดียว → toast "ร้านนี้อยู่ในวันนี้แล้ว" (ไม่เพิ่ม) · เปลี่ยนเขต → นำร้านนอกเขตออก + toast
- อนุมัติขั้นสุดท้าย → `supersedeOld()` เปลี่ยนใบเดิมของเขต+รอบเป็น "ถูกแทนที่" + บันทึก "แจ้ง TO/CC" ในประวัติ
- row menu render ไอคอนเฉพาะในเมนู (data-rmic) กันคลิกทะลุ

## §8 State-Driven UI Matrix
| status | pill (`DOC_ST`) | ปุ่มหัว drawer | ⋮ |
|---|---|---|---|
| draft | ร่าง `pill-muted` | เจ้าของ: ยกเลิก · แก้ไข · ส่งอนุมัติ | ดูรายละเอียด · แก้ไข · พิมพ์ · ยกเลิกเอกสาร |
| pending | รออนุมัติ `pill-warning` | ผู้อนุมัติขั้นปัจจุบัน: ไม่อนุมัติ · อนุมัติ / เจ้าของ·ผู้จัดการฝ่ายขาย: ยกเลิกเอกสาร | ดูรายละเอียด · อนุมัติ · พิมพ์ · ยกเลิกเอกสาร |
| approved | อนุมัติแล้ว `pill-success` | — | ดู · พิมพ์ |
| superseded | ถูกแทนที่ `pill-muted` | — | ดู · พิมพ์ |
| cancelled | ยกเลิก `pill-danger` | — | ดู · พิมพ์ |

## §9 Microcopy (verbatim)
### Toast (`showToast`)
| ข้อความ | variant |
|---|---|
| ไม่มีการแจ้งเตือนใหม่ | info |
| แบบเอกสารนี้ยังไม่เปิดใช้งาน | warning |
| แก้ไขได้เฉพาะร่างของตัวเอง | warning |
| นำร้านนอกเขตออก ${before - after} ร้าน | warning |
| ร้านนี้อยู่ในวันนี้แล้ว | warning |
| สูงสุด ${MAX_DAYS} วันต่อใบ | warning |
| กรุณากรอกข้อมูลให้ครบถ้วน | warning |
| บันทึกร่างแล้ว · | info |
| ส่งอนุมัติแล้ว · | info |
| อนุมัติแล้ว · | info |
| ส่งออก | info |
| สลับเป็น | info |
| แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง | error |
- toast ประกอบ: "บันทึกร่างแล้ว · " + เลขที่ · "ส่งอนุมัติแล้ว · " + เลขที่ · "อนุมัติแล้ว · " + เลขที่ · "ไม่อนุมัติ — ส่งกลับเป็นร่างแล้ว · " + เลขที่ · "ยกเลิกเอกสารแล้ว · " + เลขที่ · "นำร้านนอกเขตออก " + n + " ร้าน" · "สูงสุด 31 วันต่อใบ" · "ส่งออก " + n + " รายการ" · "สลับเป็น " + ชื่อ · "ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง" · "ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่" · "คุณไม่มีสิทธิ์ทำรายการนี้"
### ข้อความบนจอ (สกัดจาก HTML)
- · กลับเป็นร่างเลขเดิมให้ผู้นำเสนอแก้ไข
- · รออนุมัติอยู่ — ผู้อนุมัติจะได้รับแจ้ง
- · ส่งแล้ว ล็อกแก้ไข
- ก.ค.
- ก.พ.
- ก.ย.
- กรกฎาคม
- กรุณากรอกข้อมูลให้ครบถ้วน
- กรุณากรอกวันที่ · เริ่มต้นตลาด · สิ้นสุดตลาด และร้านค้าอย่างน้อย 1 ร้าน
- กันยายน
- กาฬสินธุ์
- กำลังเปิดหน้าต่างพิมพ์ ·
- กุมภาพันธ์
- ขอนแก่น
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลยังไม่ครบ — แก้ไขร่างให้ครบก่อนส่ง
- ข้อมูลเอกสาร
- ข้อมูลแผนเยี่ยม
- ข้อมูลแผนเยี่ยมร้านค้า
- ข้าม
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค้นหา...
- ค้นหาร้านค้าในเขตเพื่อเพิ่ม
- ค้นหาเลขที่ / เขต / รอบการขาย / ผู้รับผิดชอบเขต
- จำนวนร้านต่อวันน้อยเกินไป
- จำนวนลูกค้า
- ชนิดไฟล์ไม่รองรับ
- ชัยนาท
- ชัยภูมิ
- ชื่อฟังก์ชัน
- ชุมชนรอบนิคม
- ดาวน์โหลด PDF
- ต.ค.
- ตรวจสอบและยืนยัน
- ตลาด/พื้นที่สิ้นสุด
- ตลาด/พื้นที่เริ่มต้น
- ตลาดนัดชุมชน
- ตลาดสดเทศบาล
- ตลาดเช้า
- ตลาดโต้รุ่ง
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตำแหน่ง
- ตุลาคม
- ต้อง
- ต้องมีร้านค้าอย่างน้อย 1 ร้าน
- ต้องมีแผนเยี่ยมอย่างน้อย 1 วัน
- ถูกแทนที่
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ทุกสถานะ
- ทุกเขต
- ธ.ค.
- ธันวาคม
- นครพนม
- นครราชสีมา
- นำออก
- บันทึกซ้ำ
- บันทึกร่างแล้ว ·
- ประวัติ
- ผู้จัดการขาย ทดสอบสี่
- ผู้จัดการฝ่ายขาย
- ผู้นำเสนอ
- ผู้ประสานงานขาย ทดสอบห้า
- ผู้รับผิดชอบ
- ผู้รับผิดชอบเขต
- ผู้อนุมัติ
- ฝ่ายขาย
- พ.ค.
- พ.ย.
- พนักงานขาย ทดสอบสาม
- พนักงานขาย ทดสอบหก
- พนักงานขาย ทดสอบหนึ่ง
- พนักงานขายเขต GT
- พฤศจิกายน
- พฤษภาคม
- พิมพ์
- ม.ค.
- มกราคม
- มหาสารคาม
- มิ.ย.
- มิถุนายน
- มินิมาร์ทสมมติ
- มี.ค.
- มีนาคม
- มีร้านซ้ำในวันเดียวกัน
- ยกเลิก
- ยกเลิกเอกสาร
- ยกเลิกเอกสารแล้ว ·
- ยังเป็นร่าง — กรอกครบแล้วกดส่งอนุมัติ
- ยังไม่ครอบคลุมร้านหลักในเขต
- ยังไม่ถึง
- ยังไม่มีข้อมูล
- ยังไม่มีแผนเยี่ยมรายวัน
- ยังไม่มีใบเป้าหมายการเยี่ยมร้านค้า
- ยังไม่ส่ง
- ยังไม่ได้เลือก
- ย่านการค้าในเมือง
- ย้อนกลับ
- รอบการขาย
- รออนุมัติ
- ระบบ
- รายการ
- รายชื่อร้านค้า
- รายละเอียด
- ร่าง
- ร้อยเอ็ด
- ร้านขายส่งทดสอบ
- ร้านค้าตัวอย่าง
- ร้านค้าปลีกทดสอบ
- ร้านนี้อยู่ในวันนี้แล้ว
- ร้านสะดวกซื้อสมมติ
- ร้านโชห่วยตัวอย่าง
- ลบวันนี้
- ลบไฟล์
- ลพบุรี
- ลองปรับคำค้นหรือล้างตัวกรอง
- ลายเซ็น / อนุมัติ
- ลำดับการลงนาม
- ล้างตัวกรอง
- วันทำงาน
- วันที่
- วันที่ ........./........./.........
- วันที่ซ้ำกับวันทำงานอื่น
- วันที่ต้องอยู่ในรอบการขาย
- วางแผนเยี่ยมร้านรายวันของเขตคุณในรอบการขาย
- ส.ค.
- สกลนคร
- สถานะ
- สระบุรี
- สร้าง PDF
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างโดย
- สร้างใบเป้าหมาย
- สลับเป็น
- สิงหาคม
- สิงห์บุรี
- สิ้นสุดตลาด
- ส่งอนุมัติ
- ส่งอนุมัติแล้ว ·
- ส่งอนุมัติใบเป้าหมายการเยี่ยมร้านค้า?
- ส่งออก
- ส่งในระบบ
- ส่วนหัวเอกสาร
- หนองคาย
- หัวหน้าเขต ทดสอบสอง
- หัวหน้าเขตการขาย GT
- อนุมัติ
- อนุมัติแล้ว
- อนุมัติแล้ว ·
- อนุมัติใบเป้าหมายนี้?
- อยุธยา
- อุดรธานี
- อ่างทอง
- เขตตะวันออกเฉียงเหนือ 1
- เขตตะวันออกเฉียงเหนือ 2
- เขตภาคกลาง 1
- เจ้าหน้าที่ประสานงานขาย
- เดือนถัดไป
- เด้งกลับบน
- เปลี่ยนผู้รับผิดชอบเขต
- เปลี่ยนผู้รับผิดชอบเขต — ทำใบใหม่
- เพิ่มเติม
- เม.ย.
- เมษายน
- เริ่มต้นตลาด
- เลขที่
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกตอนส่ง
- เลือกประเทศ
- เลือกผู้รับใบเป้าหมาย
- เลือกผู้อนุมัติ
- เลือกรอบการขายผิด
- เลือกวันที่
- เลือกเขตการขายที่รับผิดชอบ
- เลือกเขตก่อน
- เลือกเดือน
- เส้นทางตลาดไม่ต่อเนื่อง ขอปรับลำดับวัน
- เหตุผลที่ยกเลิก
- เอกสารแนบ
- แก้ไขร่าง
- แก้ไขล่าสุด
- แก้ไขเอกสาร
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้ง TO/CC
- แจ้งผู้นำเสนอว่าต้องแก้อะไร
- แทนที่ด้วย
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- แผนที่เส้นทางตลาด-ตุลาคม.pdf
- ใบเป้าหมายการเยี่ยมร้านค้า
- ใบเป้าหมายการเยี่ยมร้านค้า : เขตการขาย General Trade
- ไม่ค้างคืน
- ไม่พบผู้อนุมัติ — เลือกตอนส่ง
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่พบร้านค้าในเขตนี้
- ไม่ยกเลิก
- ไม่อนุมัติ
- ไม่อนุมัติ — กลับเป็นร่าง
- ไม่อนุมัติ — ส่งกลับเป็นร่างแล้ว ·

## §10 Data Binding & BACKEND anchors
| prototype | ระบบจริง (02_API) |
|---|---|
| `TERR` + `terrOf()` · `EMP` + `empOf()` · `CUST` + `custOf()` | API-03 prefill (Sales Territory / Employee / Customer) |
| `RECS` + `listRows()` + `canSee()` | API-01/02 (FN-10) |
| `persist()` (`SEQ` + `DOC.prefix`) | API-04/05 · ENG-DOC-NUM (FN-03) |
| `MOCK_DOA_RESOLVED` / `resolveDoa()` (DOA-ENGINE-HOOK · 2 ขั้น) | API-06/07 GET /doa/resolve |
| `confirmSubmit()` / `confirmApprove()` / `confirmReason()` | API-07 / API-08 / API-09 |
| `supersedeOld()` + บันทึก "แจ้ง TO/CC" | FN-09 (ใน API-08) · ENG-NOTIFY svt_plan_published |
| `docPrintData()` + `tplRender()` + `SVT_TPL` · `storeCells()` | API-10 render ฝั่ง server (parity · A4 แนวนอน) |
| `exportCSV()` | API-11 |
| `gateFiles()` / `FILE_ACCEPT` | API-12 Document Center |
| `custTotal()` · `workDays()` · `validateMain()` · `dayErr()` | FN-02 (ทำซ้ำฝั่ง server) |

## §11 Traceability + Drift Log
| Brief | FRD | HTML |
|---|---|---|
| §4 P-01 | 01_UI P-01 · API-01/11 | `renderPage()` |
| §4 P-02 | 01_UI P-02 · API-03/04/05 · BR-01..07 | `renderWizard()` |
| §4 P-03 | 01_UI P-03 · API-02/08/09/10 | `renderViewDrawer()` |
| §8 | 05 §5.2 · §5.3 | `DOC_ST` · `canEdit()` · `canCancel()` · `canAct()` |
### ⚠️ Drift Log
| รายการ | ชนิด | ข้อเสนอ |
|---|---|---|
| `__QA__` · `switchPersona()` · `S.sim` · `commitRejected()` | HTML-only (prototype) | ไม่ทำในระบบจริง |
| role-line-manager resolve ด้วย `EMP.mgr` | HTML mock | ระบบจริงผ่าน DOA กลาง (OQ-02) |
| โลโก้ในแบบพิมพ์ = placeholder · แบบพิมพ์ prototype A4 แนวตั้ง | HTML-only | ระบบจริงใช้ header_snapshot · render แนวนอนตาม print_config (OQ-07) |
| `CYCLES` รายการเดือนคงที่ | HTML mock | ระบบจริงสร้างตามปฏิทิน/รอบการขาย (OQ-05) |

## §12 Diff จากเวอร์ชันก่อน
— ไม่มีใน HTML นี้ (เวอร์ชันแรก)

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- สร้างตารางเยี่ยม/เช็กอินใน Visit Operation จากแผนที่อนุมัติ — รอบถัดไป
