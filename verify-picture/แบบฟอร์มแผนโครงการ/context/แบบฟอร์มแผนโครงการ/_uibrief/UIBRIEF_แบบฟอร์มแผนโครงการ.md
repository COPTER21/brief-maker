# UI_BRIEF — F-TMP-004 แบบฟอร์มแผนโครงการ (Project Plan)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| HTML | `feature.html` · html-generator-v9.4 · archetype **Q-form** (`<meta name="cube-archetype" content="Q-form">`) · `window.__QA__` มี |
| FRD | FRD_F-TMP-004_Pack v1.0 (00–07 · frd_lint BLOCK 0) · BRD-PDM-PJP-001 APPROVED |
| DECISIONS | DECISIONS.lock 18 มติ (AI-DEFAULT 14 · VALID 4) |
| Gate | audit.sh FAIL 0 · self_audit PASS · e2e_standard 21/21 + flow 17/17 (Chromium ใน container ของ agent — เครื่องผู้ใช้ NO-BROWSER) |
| Drift | ดู §11 — ไม่มี business drift · prototype-only = `window.__QA__` · ตัวสลับผู้ใช้ (`switchPersona()`) · `S.sim` |
| Date | 2026-10-11 |

## §1 Design Tokens AS-BUILT
- ฟอนต์: Noto Sans Thai + Satoshi (Google Fonts / Fontshare) · แบบพิมพ์ใช้ Sarabun (ใน PDF_CSS)
- สี/ระยะ/รัศมี = CSS variables ของ kit CUBE Warm Light (ตารางเต็มท้ายหัวข้อนี้) · ห้ามเพิ่มเฉดใหม่ (U10)
- scrollbar: custom `::-webkit-scrollbar` + `scrollbar-width: thin` · `scrollbar-gutter: stable`
- Page-specific CSS ของ feature นี้: `.person-ic` · `.ph-count.is-warn` / `.ph-count.is-danger` · `.cell-ellipsis` · `.cell-warn` · `.pg-size` · `.pj-tbl` (ตารางดู) · `.pj-edit` (ตารางแก้ไข) · `.pj-total` · `.pj-grid2` · `.field-static` · `.trip-warn` · `.bd-bad` · `.ss-bad` · `.alert-row.is-warning` · ตัวเลือกวัน `.bedate` / `.bd-pop`


| CSS variable | ค่า |
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

**z-index map** (ค่าที่ประกาศ · registry `--z-*` ใน :root)

| z | selector |
|---|---|
| 1 | .stepper-item:not(:last-child)::after |
| 2 | .stepper-circle |
| 3 | .table-scroll.is-sticky thead th |
| var(--z-backdrop) | .ss-list, .drawer-backdrop, รมีปุ่ม action หลัก */  .modal-backdrop, #drawerBackdrop |
| var(--z-drawer) | .drawer, #drawer |
| var(--z-dropdown) | .user-menu, .info-tip::after |
| var(--z-modal) | .modal-backdrop |
| var(--z-popover) | * เมนูที่ portal ออกจาก scroll container (ใช้คู่ portalMenu , verlay-root ตอนเปิด (หลุด overflow ของ modal/drawer body)  |
| var(--z-portal) | .bd-pop |
| var(--z-shell) | .sidebar |
| var(--z-sticky) | .shell-bar, .table-wrap thead th, .wizard-footer |
| var(--z-toast) | .toast, #toast |
## §2 Route Map
| Route | หน้า/สถานะ | handler |
|---|---|---|
| `#/project-plan` | P-01 รายการ (default ของ feature) | `applyRoute()` · `renderPage()` |
| `#/project-plan/view/:id` | P-03 drawer ดู (เปิดได้เฉพาะใบที่ `canSee()` · ไม่มีสิทธิ์ = ไม่เปิด) | `openView()` · `showDrawer()` |
| `#/project-plan/create` | P-02 สร้าง (ไม่มีทำซ้ำ · DEC-14) | `startWizard()` |
| `#/project-plan/edit/:id` | P-02 แก้ร่าง (เจ้าของ · draft) | `startWizard()` |
- refresh-safe: `hashchange` → `applyRoute()` · ปิด drawer → `go()` กลับ `#/project-plan`

## §3 Layout Shell
- `.sidebar` (module Project › แผนโครงการ · badge `#sbBadge` = จำนวนรอฉันพิจารณา) · breadcrumb Core › Project › แผนโครงการ · `.user-chip` + `#userMenu` (สลับผู้ใช้ — prototype-only · `#personaList`) · avatar ผู้ใช้ = `.person-ic`
- เนื้อหา `#page-content` · drawer `#drawer` + `#drawerBackdrop` · modal `#modalBackdrop` > `#modal` · `#toast` · portal `#overlay-root`

## §4 Page Anatomy
### P-01 รายการ (`renderPage()`)
- `.ph` → `.ph-title` "แบบฟอร์มแผนโครงการ" + `.ph-en` "(Project Plan)" · `.ph-count` จำนวน · `.ph-count.is-warn` "รอฉันพิจารณา n" · `.ph-count.is-danger` "มีกิจกรรมล่าช้า n" (ค่า 0 ไม่แสดง · U22) · `.ph-sub` · `.ph-actions` [ส่งออก CSV `exportCSV()`] [สร้างแผนโครงการ `#btnCreate` → `startWizard()`]
- ไม่มี stat card (U1)
- `.card.list-card` → `.filter-bar` (`#fq` ค้นหา · combobox `#ss-fst` สถานะ · `#ss-fdept` หน่วยงาน · ล้างตัวกรอง `resetFilters()`) → `.table-wrap` > `table.table` คอลัมน์: รหัสโครงการ · วันที่ขอ · ชื่อโครงการ (`.cell-ellipsis`) · ผู้รับผิดชอบหลัก · ระยะเวลาโครงการ · งบประมาณที่ขอ · สถานะเอกสาร (`docPill()` + ป้าย "ล่าช้า n") · ลายเซ็น (`renderSignProgress()`) · ⋮ `.ra-btn` → `openRowMenu()`
- `pager()` → `.table-footer` : `.pg-size` (10/25/50 · `setPageSize()`) · "x–y จาก N" · `.pagination`
- แถว `.is-clickable` → `rowClick()` → `openView()`
### P-02 สร้าง/แก้ (`renderWizard()` · drawer `.drawer-panel.wide`)
- หัว: eyebrow สร้างเอกสารใหม่/แก้ไขเอกสาร · `stepper()` 3 ขั้น `.d-stepper` (`STEPS`)
- ขั้น 1 `wizMain()` · `.wz-split` : `.wz-main` การ์ด `CARD()` ①–⑧ ตามส่วนของกระดาษ
  - ① `.pj-grid2`: ชื่อโครงการ (`fld()` · `tIn()`) · รหัสโครงการ `.field-static` (ระบบออกให้) · หน่วยงาน combobox `#ss-wdept` · ผู้รับผิดชอบหลัก combobox `#ss-wpm` · วันที่เริ่มต้น/สิ้นสุด `bedateHTML()` via `dateField()` · บรรทัดคำนวณ `.pd-line` ระยะเวลา `#wDur`
  - ②③⑧ textarea ผ่าน `fld()` / `tArea()` (soft update `setFv()`)
  - ④⑤⑥⑦ ตาราง `.pj-edit` : `goalRows()` · `actRows()` (ผู้รับผิดชอบ `#ss-ar{i}` · วันที่ `dateField()` · ระยะเวลา `#adur-{i}` · สถานะ select) · `budgetRows()` (รวม `#wTotal`) · `riskRows()` (ความรุนแรง select · ผู้รับผิดชอบ `#ss-rk{i}`) · `.add-row` `addRow()` · ลบ `removeRow()` · เตือนนอกช่วง `.trip-warn` · error `.trip-err`
  - `sumCard()` `.wz-sum` : ผู้จัดทำ · ผู้พิจารณาต่อขั้นจาก DOA · `#sumDur` · `#sumActs` · `#sumBud`
- ขั้น 2 `wizAttach()` `.upload-zone` → `#pjFile` · `pickFiles()` / `removeFile()`
- ขั้น 3 `wizReview()` `.review-card` × 7 · ตาราง `goalsTable()` `actsTable()` `budgetTable()` `risksTable()`
- `.dw-footer` : ย้อนกลับ `wizBack()` · ยกเลิก `closeDrawer()` · ถัดไป `#btnNext` `wizNext()` / บันทึกแบบร่าง `#btnDraft` `saveDraft()` · บันทึกและส่งอนุมัติ `#btnSaveSubmit` `saveAndSubmit()` (loading `.spin` loader-2)
### P-03 ดู (`renderViewDrawer()` · drawer 920)
- `.dw-head` lean: `.dw-eyebrow` ชื่อเอกสาร · `.dw-title` รหัสโครงการ + `docPill()` · `.dw-sub` ชื่อโครงการ · `.dw-actions` ตามสถานะ (§8) + พิมพ์ `genPdf()` · ปิด
- `.drawer-tabs` `tabBtn()` : รายละเอียด `renderDetailTab()` · PDF Preview `renderPdfTab()` · ลายเซ็น / อนุมัติ `renderSignTab()` · ประวัติ `renderHistoryTab()`
- รายละเอียด: `viewBanner()` · `SEC()` ข้อมูลเอกสาร · ส่วนที่ 1–8 (`.drawer-fields.fields-1` สำหรับข้อความยาว · ตาราง `.pj-tbl` 4 กลุ่ม · `.pj-total`) · เอกสารแนบ `fileRow()` · ข้อมูลระบบ
- PDF: `.pv-bar` + `.a4` > `.pdf-slot` > `iframe.pdf-frame[srcdoc]` (`docPdfDoc()` · `fitPdf()`) · A4 2 หน้า

## §5 Component Inventory
| Component | anchor | states |
|---|---|---|
| Search combobox | `searchSelectHTML()` / `initSearchSelect()` · `.search-select` · list portal `.ss-list` | default · open · filtered · empty "ไม่พบ" · selected (clear ×) · error `.ss-bad` (แถวตาราง) |
| ตัวเลือกวัน พ.ศ. | `bedateHTML()` · `.bedate` · popover `.bd-pop` | placeholder "เลือกวันที่" · open · min (สิ้นสุด ≥ เริ่ม · กิจกรรม ≥ วันเริ่มโครงการ) · error `.bd-bad` |
| ตารางแก้ไข 4 กลุ่ม | `.pj-edit` | ปกติ · ช่องผิด `.is-bad` + `.row-err` `.trip-err` · นอกช่วง `.trip-warn` · ถึงขั้นต่ำ = ไม่มีปุ่มลบ |
| ตารางดู | `.pj-tbl` | มีข้อมูล · ว่าง = `emptyStateHTML()` "ไม่มีข้อมูล" (U23) · ป้ายสถานะ `ACT_ST` / ความรุนแรง `SEV` · "นอกช่วง" |
| คน | `empChip()` · `.emp-chip` + `.person-ic` | ชื่อ + ตำแหน่ง (ไม่มี initials · U17) |
| ลายเซ็น n/N | `renderSignProgress()` `.sign-prog` `.sp-bar` | ร่าง "—" · ระหว่างทาง · ยกเลิก `.is-bad` |
| Row menu ⋮ | `openRowMenu()` `.row-menu` `.rm-item` | รายการตามสิทธิ์ · ยกเลิก `.is-danger` |
| Toast | `showToast()` `#toast` | info · success · warning · error |
| Upload | `.upload-zone` · `gateFiles()` | ว่าง · มีไฟล์ · ไฟล์ผิดชนิด/ใหญ่เกิน (toast error) |

## §6 Overlay Registry
| Overlay | ขนาด | เปิด | ปิด / dismiss | z |
|---|---|---|---|---|
| drawer ดู `.drawer-panel` | 920 | `showDrawer()` | ปุ่มปิด · Esc · mousedown ที่ `#drawerBackdrop` (U25) | `var(--z-drawer)` |
| drawer สร้าง `.drawer-panel.wide` | 1290 | `startWizard()` | เหมือนบน · กรอกค้าง (`S.dw.dirty`) → modal ทิ้งข้อมูล | `var(--z-drawer)` |
| modal `#modal` (`.is-lg` สำหรับ ส่ง/อนุมัติ/อัปเดตสถานะ) | — | `openModalCfg()` | ปุ่ม · Esc · mousedown backdrop (`modalBackdropClick()` — มีเหตุผล/ความเห็นค้าง = **ไม่ปิด**) | `var(--z-modal)` |
| row-menu `.row-menu` | 200 | `openRowMenu()` | click ที่อื่น · scroll | `var(--z-popover)` |
| combobox list `.ss-list` | ความกว้างช่อง | focus/พิมพ์ | click ที่อื่น · Esc | `var(--z-popover)` |
| ปฏิทิน `.bd-pop` | 280 | `bdToggle()` | click นอก · Esc (ปิดแค่ปฏิทิน) | `var(--z-popover)` |
| user-menu `#userMenu` | — | `toggleUserMenu()` | click นอก | `var(--z-dropdown)` |
| toast `#toast` | — | `showToast()` | อัตโนมัติ 2.8 วินาที | `var(--z-toast)` |

## §7 Interaction Spec
- Esc chain: ปฏิทินเปิด → ปิดปฏิทินอย่างเดียว · combobox เปิด → ปิด list · มี modal → `closeModal()` · มี drawer → `closeDrawer()` (wizard กรอกค้าง → modal "ทิ้งข้อมูลที่กรอกไว้?")
- backdrop: `onmousedown` + `event.target===this` เท่านั้น (U25)
- row click เปิด view ยกเว้นคลิกใน `.row-actions-cell`
- พิมพ์ข้อความ/ตัวเลข = soft update (`setFv()` · `setRow()` soft · `softSum()`) ไม่ rebuild → focus ไม่หลุด · ระยะเวลา/รวมงบ/สรุปอัปเดตสด
- เลือกวันเริ่มหลังวันสิ้นสุด → วันสิ้นสุดเลื่อนตาม (โครงการและกิจกรรม) · เพิ่มแถว `addRow()` focus ช่องแรกแถวใหม่
- `render()` ใช้ `preserveRenderState()` / `restoreRenderState()` · `renderIcons()` หลังทุก render
- แก้ไขจาก view = ปิด view แล้วเปิด wizard (ไม่ซ้อน · U15)

## §8 State-Driven UI Matrix
| status | pill (`DOC_ST`) | ปุ่มหัว drawer | ⋮ |
|---|---|---|---|
| draft | ร่าง `pill-muted` | เจ้าของ: ยกเลิก · แก้ไข · ส่งอนุมัติ (`#btnSubmitView`) | แก้ไข · พิมพ์ · ยกเลิกเอกสาร |
| pending | รออนุมัติ `pill-warning` | ผู้พิจารณาขั้นปัจจุบัน: คำปฏิเสธ · คำอนุมัติ ตาม role (`#btnApproveView` `.btn-success`) · เจ้าของ/admin: ยกเลิกเอกสาร | พิมพ์ · ยกเลิกเอกสาร[สิทธิ์] |
| approved | อนุมัติแล้ว `pill-success` (+ `pill-danger` "ล่าช้า n") | ผู้จัดทำ/ผู้รับผิดชอบหลัก: อัปเดตสถานะกิจกรรม (`#btnStatusView`) | พิมพ์ · อัปเดตสถานะกิจกรรม[สิทธิ์] |
| cancelled | ยกเลิก `pill-muted` | — | พิมพ์ |
- แบนเนอร์ (`viewBanner()`): ร่างที่ถูกส่งกลับ `.alert-row.is-danger` · รอ (ขั้น n) · มีกิจกรรม Delayed `.alert-row.is-warning` · อนุมัติแล้ว (งบที่อนุมัติ) `.alert-row.is-success` · ยกเลิก
- คำตัดสินตาม role: `wordsOf()` จาก `DECISION_WORDS` (role-line-manager = ตรวจสอบแล้ว/ไม่ผ่านการตรวจสอบ · role-gm = อนุมัติ/ไม่อนุมัติ)
- modal อนุมัติขั้นสุดท้าย (`isLastStep()`): ตาราง `apprTable()` งบที่ได้รับอนุมัติต่อรายการ `setAppr()` · เกินที่ขอ = `.trip-warn` "เกินงบที่ขอ" · รวม `#apTot`
- modal อัปเดตสถานะ: `statusTable()` → `confirmStatus()`


## §9 Microcopy (verbatim)
### Toast (`showToast()`)
| variant | ข้อความ |
|---|---|
| info | ไม่มีการแจ้งเตือนใหม่ |
| warning | แบบเอกสารนี้ยังไม่เปิดใช้งาน |
| warning | แก้ไขได้เฉพาะร่างของตัวเอง |
| warning | กรุณากรอกข้อมูลให้ครบถ้วน |
| warning | กรุณากรอกข้อมูลให้ครบถ้วน |
| info | บันทึกร่างแล้ว · |
| warning | กรุณากรอกข้อมูลให้ครบถ้วน |
| info | ส่งอนุมัติแล้ว · |
| warning | งบประมาณที่ได้รับอนุมัติไม่ถูกต้อง |
| info | ไม่มีสถานะที่เปลี่ยน |
| info | อัปเดตสถานะ |
| info | ส่งออก |
| info | สลับเป็น |
| error | แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง |
### ปุ่ม / label / placeholder / empty (ตรงจอ)
สร้างแผนโครงการ · ส่งออก CSV · ล้างตัวกรอง · ส่งอนุมัติ · บันทึกแบบร่าง · บันทึกและส่งอนุมัติ · ถัดไป · ย้อนกลับ · ยกเลิก · ยกเลิกเอกสาร · ตรวจสอบแล้ว · ไม่ผ่านการตรวจสอบ · อนุมัติ · ไม่อนุมัติ · อัปเดตสถานะกิจกรรม · บันทึกสถานะ · ทิ้งข้อมูล · กลับไปกรอกต่อ · เพิ่มเป้าหมาย · เพิ่มกิจกรรม · เพิ่มรายการค่าใช้จ่าย · เพิ่มความเสี่ยง · พิมพ์ · ดาวน์โหลด PDF
placeholder: ค้นหารหัส / ชื่อโครงการ / ผู้รับผิดชอบ · ไม่บังคับ · aria: ${ph || k} · งบประมาณที่ได้รับอนุมัติ · จำนวนต่อหน้า · ระดับความรุนแรง · สถานะ · เดือนก่อน · เดือนถัดไป
### Microcopy inventory (สกัดจาก HTML · verbatim)
```
(ขั้น
[Lucide] All CDNs failed. Icons จะไม่แสดง but UI ยังใช้งานได้
]); if (canCancel(r)) items.push(['x-circle', 'ยกเลิกเอกสาร',
]); if (canUpdateStatus(r)) items.push(['list-checks', 'อัปเดตสถานะกิจกรรม',
]]; /* DEC-14 ทำซ้ำ ✗ */ if (isOwner(r) && r.status === 'draft') items.unshift(['pencil', 'แก้ไข',
showToast('ไม่มีการแจ้งเตือนใหม่','info')
· กลับเป็นร่าง
· งบที่อนุมัติต่างจากที่ขอ แจ้งผู้จัดทำแล้ว
· อนุมัติแล้ว ล็อกแก้ไข (ยกเว้นสถานะกิจกรรม)
· แจ้งผู้รับผิดชอบหลักและผู้บังคับบัญชาแล้ว
ก.ค.
ก.พ.
ก.ย.
กรกฎาคม
กรอกตามส่วนของแบบฟอร์ม FM-PDM-01 · ระยะเวลาและยอดรวมระบบคำนวณให้
กรอกให้ครบทุกช่องที่มี *
กระทบการผลิต
กรุณากรอกข้อมูลให้ครบถ้วน
กรุณาเลือกวันที่สิ้นสุด
กลาง
กันยายน
กานดา จัดหา
กำลังเปิดหน้าต่างพิมพ์ ·
กิจกรรม
กิจกรรม ·
กุมภาพันธ์
ขั้นทดสอบ
ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
ข้อมูลทั่วไปของโครงการ
ข้อมูลสต๊อกเชื่อถือได้
ข้อมูลหลักแผนโครงการ
ข้อมูลไม่ครบ ขอรายละเอียดเพิ่ม
ข้อมูลไม่ต่อเนื่อง
ข้าม
คลังกลางจัดเก็บสินค้าตามพื้นที่ว่าง ไม่มีผังตำแหน่งที่แน่นอน
คลังเดิมใกล้เต็ม
คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
ความคลาดเคลื่อนสต๊อก
ความถูกต้องสต๊อก ≥ 99%
ความปลอดภัยสูงขึ้น
ความผิดพลาดช่วงแรก
ความเป็นมา
ความเป็นมา (Background)
ความเสี่ยง
คัดเลือกผู้รับเหมา
คืนทุนภายใน 2 ปี
คุณไม่มีสิทธิ์ทำรายการนี้
ค่าติดตั้ง
ค่าที่ปรึกษา
ค่าที่ปรึกษาออกแบบผัง
ค่าบริการรายปี
ค่าสแกนเอกสารเก่า
ค่าอบรมพนักงาน
ค่าเริ่มต้นจากสายอนุมัติ (DOA) และผังองค์กร
ค่าแรงติดตั้ง
ค่าไฟฟ้าคิดเป็น 12% ของต้นทุนผลิต
ค่าไฟฟ้าโรงงานสูงขึ้นทุกปี
ค่าไฟส่วนแสงสว่างสูง
ค้นหา...
ค้นหารหัส / ชื่อโครงการ / ผู้รับผิดชอบ
ค้นหาเอกสารยาก
งบประมาณที่ขอ
งบประมาณที่ได้รับอนุมัติต้องเป็นตัวเลขตั้งแต่ 0 ขึ้นไป
งบประมาณที่ได้รับอนุมัติไม่ถูกต้อง
งบประมาณสูงเกินความจำเป็น
งบประมาณสูงเกินความจำเป็น — ขอเทียบราคาห้องอบรม 2 ราย
จัดงานสัมมนาคู่ค้าประจำปี
จัดซื้อหลอด LED
จัดทุกปี
จัดผังคลังและใช้บาร์โค้ดระบุตำแหน่ง ให้หยิบสินค้าเร็วและถูกต้อง
จัดหลักสูตรปฐมนิเทศมาตรฐาน
จัดหาอุปกรณ์สแกนบาร์โค้ด
จำนวนครั้งไฟดับ
จำนวนงานเร่งต่อเดือน
จำนวนต่อหน้า
จำนวนสายสอบถามสถานะ
ชนิดไฟล์ไม่รองรับ
ชั้นวางสินค้าใหม่
ชื่อฟังก์ชัน
ชื่อโครงการ
ชื่อโครงการ (Project Name)
ด้านกลยุทธ์องค์กร
ด้านกลยุทธ์องค์กร (Strategic)
ด้านการดำเนินงาน
ด้านการดำเนินงาน (Operational)
ด้านการเงิน
ด้านการเงิน (Financial)
ต.ค.
ตรวจนับรายเดือน
ตรวจสอบและยืนยัน
ตรวจสอบแล้ว
ตัดสระบน-วรรณยุกต์-สระล่าง
ติดตั้ง
ติดตั้ง GPS และหน้าจอติดตามรถทุกคัน
ติดตั้งช่วงหยุดผลิต
ติดตั้งระบบแจ้งเตือนความร้อน
ติดตั้งอุปกรณ์ในรถ
ติดตั้งเลื่อน
ติดตั้งแผงและอินเวอร์เตอร์
ติดตั้งแผงโซลาร์เซลล์หลังคาโรงงาน
ติดตั้งและทดสอบระบบ
ติดตั้งไม่เสร็จในช่วงหยุดผลิต
ตุลาคม
ตู้ควบคุมไฟฟ้า
ตู้ควบคุมไฟฟ้าอายุเกิน 15 ปี
ต่อรองราคา
ต่ำ
ต้อง
ต้องเสริมโครงสร้าง
ถึง
ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
ทำไมต้องทำตอนนี้
ที่มาของโครงการ
ทุกสถานะ
ทุกหน่วยงาน
ธ.ค.
ธนากร ช่างคิด
ธันวาคม
นอกช่วง
บริษัท ตัวอย่าง จำกัด
บันทึกซ่อมบำรุง
บันทึกผลขั้น
บันทึกผิด
บันทึกร่างแล้ว ·
บาท
ประวัติ
ประวัติ (append-only)
ประหยัดค่าไฟ 120,000 บาทต่อปี
ประหยัดค่าไฟประมาณ 450,000 บาทต่อปี
ประเสริฐ บริหารดี
ปรับปรุงกระบวนการวางแผนการผลิต
ปรับปรุงระบบจัดเก็บสินค้าคลังกลาง
ปรับปรุงห้องควบคุมไฟฟ้าโรงงาน 2
ปรับปรุงห้องอบรม
ปัญหาที่พบ หรือโอกาสที่ต้องการ
ปัญหาหรือโอกาสทางธุรกิจ
ปัญหาหรือโอกาสทางธุรกิจ (Problem / Business Opportunity)
ปิด
ปิยะดา วางแผน
ป้องกันการหยุดผลิต
ผลกระทบ
ผลตอบแทนและประโยชน์ที่คาดว่าจะได้รับ
ผลิตไฟฟ้าใช้เองอย่างน้อย 30% ของการใช้ไฟกลางวัน
ผังคลังสินค้าใหม่.pdf
ผู้ขายส่งอุปกรณ์ล่าช้า
ผู้จัดการทั่วไป
ผู้จัดการฝ่ายพัฒนาโครงการ
ผู้จัดการฝ่ายวางแผน
ผู้จัดทำ
ผู้จัดทำ (Prepared by)
ผู้ตรวจสอบ (Reviewed by)
ผู้รับผิดชอบ
ผู้รับผิดชอบหลัก
ผู้อนุมัติ (Approved by)
ผู้เข้าร่วม 120 คน
ฝ่ายจัดซื้อ
ฝ่ายบริหาร
ฝ่ายพัฒนาโครงการ
ฝ่ายวางแผน
พ.ค.
พ.ย.
พนักงานคลังทำงานสะดวกขึ้น
พนักงานใหม่มั่นใจขึ้น
พนักงานใหม่เรียนรู้หน้างานโดยไม่มีหลักสูตร
พนักงานไม่คุ้นเคยระบบใหม่
พฤ
พฤศจิกายน
พฤษภาคม
พิมพ์
ภาพลักษณ์องค์กรสีเขียว
ม.ค.
มกราคม
มิ.ย.
มิถุนายน
มิเตอร์ไฟฟ้าแยก
มี.ค.
มีนาคม
ยกเลิก
ยกเลิกเอกสาร
ยกเลิกเอกสาร?
ยกเลิกเอกสารแล้ว ·
ยกเลิกโครงการ
ยอดสั่งซื้อเพิ่มขึ้นต่อเนื่อง ระบบเดิมรองรับไม่ไหว
ยังไม่ถึงขั้นนี้
ยังไม่มีกิจกรรม
ยังไม่มีข้อมูล
ยังไม่มีรายการงบประมาณ
ยังไม่มีเป้าหมายและ KPI
ยังไม่มีแผนโครงการ
ยังไม่ส่ง
ย้อนกลับ
รถติดตั้ง GPS ครบ 25 คัน
รวมกับโครงการอื่น
รวมงบประมาณที่ขอ
รวมงบประมาณที่ได้รับอนุมัติ
รวมแผนการผลิตไว้ที่เดียว
รหัสโครงการ
รองรับการขยายสาขาและยอดขายออนไลน์
รอพิจารณา
รออนุมัติ
ระดับความรุนแรง
ระบบติดตามรถขนส่งแบบเรียลไทม์
ระบบออกให้เมื่อบันทึก (PJP-ปี-ลำดับ)
ระบุตอนส่ง
ระยะคืนทุนประมาณ 5 ปี
ระยะเวลา
ระยะเวลา (วัน)
ระยะเวลาดำเนินการ
ระยะเวลาโครงการ
รายการ
รายการค่าใช้จ่าย
รายงาน HR
รายงานฝ่ายผลิต
รายละเอียด
ร่าง
ลดกระดาษ 50%
ลดการปล่อยคาร์บอน
ลดการใช้กระดาษในสำนักงาน
ลดของเสียและงานเร่ง
ลดค่าน้ำมันจากการวางเส้นทาง
ลดค่าล่วงเวลาประมาณ 180,000 บาทต่อปี
ลดค่าไฟ 30%
ลดค่าไฟแสงสว่าง 40%
ลดงานตอบคำถามและวางแผนเส้นทางได้ดีขึ้น
ลดงานเร่ง 50%
ลดต้นทุนสรรหาซ้ำ
ลดต้นทุนและพื้นที่จัดเก็บ
ลดภาระไฟฟ้าช่วงพีค
ลดสต๊อกคลาดเคลื่อน · ลดงานล่วงเวลาช่วงสิ้นเดือน
ลดสายสอบถาม
ลดเวลาหยิบสินค้า 30%
ลบแถว
ลบไฟล์
ลองปรับคำค้นหรือล้างตัวกรอง
ลายเซ็น / อนุมัติ
ลาออกช่วงทดลองงานลด 20%
ลำดับ
ลำดับการอนุมัติ (ส่วนที่ 9)
ลูกค้าพึงพอใจขึ้น
ลูกค้าโทรถามสถานะวันละกว่า 40 สาย
ล่าช้า
ล้างตัวกรอง
วัตถุประสงค์
วัตถุประสงค์รอง
วัตถุประสงค์รอง (Secondary Objectives)
วัตถุประสงค์หลัก
วัตถุประสงค์หลัก (Primary Objective)
วัน
วันที่ ........./........./.........
วันที่ขอ
วันที่สิ้นสุด
วันที่สิ้นสุดกิจกรรม
วันที่สิ้นสุดต้องไม่ก่อนวันที่เริ่ม
วันที่สิ้นสุดต้องไม่ก่อนวันที่เริ่มต้น
วันที่เริ่ม
วันที่เริ่มต้น
วางแผนการผลิตด้วยสเปรดชีตแยกไฟล์
วิภาวี ตรวจดี
วิศวกรโครงการ
ศศิธร ดูแลงาน
ศูนย์ฝึกอบรมพนักงานใหม่
ส.ค.
สถานะ
สถานะกิจกรรม
สถานะเอกสาร
สถิติคอลเซ็นเตอร์
สนับสนุนเป้าหมาย ESG
สมพร ตั้งใจ
สร้าง PDF
สร้างเอกสาร
สร้างเอกสารใหม่
สร้างแผนโครงการ
สร้างแผนโครงการเพื่อเสนอขออนุมัติ
สร้างโดย
สลับเป็น
สัญญาณขาดในพื้นที่ห่างไกล
สั่งซื้อล่วงหน้า 4 สัปดาห์
สายอนุมัติ
สำรวจกระบวนการคลังปัจจุบัน
สำรวจทำเลคลังสินค้าแห่งที่ 2
สำรวจแบบฟอร์มที่ใช้
สำรวจโครงสร้างหลังคา
สิงหาคม
สิ่งที่โครงการต้องทำให้สำเร็จ
สื่อการสอน
สูง
ส่งกลับเป็นร่างแล้ว ·
ส่งอนุมัติ
ส่งอนุมัติแล้ว ·
ส่งออก
ส่งแล้วแก้ไขไม่ได้ — ถ้าไม่ผ่านการพิจารณา เอกสารจะกลับเป็นร่างให้แก้แล้วส่งใหม่
ส่งในระบบ
หน่วยงานเจ้าของโครงการ
หน่วยไฟฟ้าที่ผลิตได้ต่อเดือน
หมายเหตุ
หยิบสินค้าช้าเฉลี่ย 25 นาทีต่อใบ และสต๊อกคลาดเคลื่อนทุกเดือน
หยิบสินค้าเร็วขึ้น 30% · ตรวจนับสต๊อกได้ภายใน 1 วัน
หลอด LED 600 หลอด
หลอดไฟเดิมเป็นฟลูออเรสเซนต์
หลักการและเหตุผล
อนุชา นำทาง
อนุมัติ
อนุมัติแผนโครงการแล้ว
อนุมัติแล้ว
อบรมพนักงานคลัง
อบรมและมีพี่เลี้ยงหน้างาน
ออกแบบผังจัดเก็บใหม่
ออกแบบระบบใหม่
ออกแบบหลักสูตร
อัตราลาออก 3 เดือนแรก
อัตราลาออกช่วงทดลองงานสูง
อัปเดตสถานะ
อัปเดตสถานะกิจกรรม
อา
อุปกรณ์ GPS 25 ชุด
อุปกรณ์สแกนบาร์โค้ด 10 ชุด
เก็บความต้องการ
เจ้าหน้าที่จัดซื้อ
เจ้าหน้าที่ธุรการโครงการ
เจ้าหน้าที่พัฒนาโครงการ
เจ้าหน้าที่วางแผน
เช่น ปรับปรุงระบบจัดเก็บสินค้าคลังกลาง
เดือนถัดไป
เด้งกลับบน
เตรียมอุปกรณ์ครบก่อนหยุดผลิต
เทียบเวลาก่อน-หลัง
เปลี่ยนตู้ควบคุมและระบบป้องกัน
เปลี่ยนหลอดไฟ LED ครบทุกอาคาร
เปลี่ยนหลอดไฟ LED ทั้งโรงงาน
เปลี่ยนแบบฟอร์มหลักเป็นระบบ
เปิดใช้งานและอบรม
เป้าหมายและ KPI
เพิ่มความเสี่ยง
เพิ่มรายการค่าใช้จ่าย
เพิ่มเติม
เพิ่มเป้าหมาย
เม.ย.
เมษายน
เลือก
เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
เลือกประเทศ
เลือกผู้พิจารณา
เลือกผู้รับผิดชอบ
เลือกผู้ให้บริการ GPS
เลือกพนักงาน
เลือกวันที่
เลือกหน่วยงาน
เลือกอุปกรณ์ที่เก็บข้อมูลออฟไลน์ได้
เวลาหยิบเฉลี่ยต่อใบ
เหตุผลที่ยกเลิก
เหตุผลในการดำเนินโครงการ
เหตุผลในการดำเนินโครงการ (Justification)
เอกสาร
เอกสารแนบ
แก้ไข
แก้ไขร่าง
แก้ไขล่าสุด
แก้ไขเอกสาร
แก้ไขแผนโครงการ
แก้ไขได้เฉพาะร่างของตัวเอง
แจ้งผู้จัดทำว่าเพราะอะไร
แนบไฟล์เพิ่ม
แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
แนวทางป้องกัน
แบบฟอร์มแผนโครงการ
แบบเอกสารนี้ยังไม่เปิดใช้งาน
แผงโซลาร์และอุปกรณ์
แผนงานไม่สอดคล้องกับระยะเวลา
แผนเชื่อถือได้
แผนไม่ตรงกับกำลังการผลิตจริง
โครงสร้างหลังคารับน้ำหนักไม่พอ
ใช้กระดาษเดือนละกว่า 60 รีม
ให้วิศวกรโครงสร้างตรวจก่อนออกแบบ
ไฟดับฉุกเฉิน 0 ครั้ง
ไฟดับฉุกเฉิน 3 ครั้งในปีนี้
ไม่ทราบตำแหน่งรถขนส่งระหว่างทาง
ไม่บังคับ
ไม่ผ่านการตรวจสอบ
ไม่พบรายการ
ไม่พบรายการที่ค้นหา
ไม่มีข้อมูล
ไม่มีสถานะที่เปลี่ยน
ไม่ยกเลิก
ไม่อนุมัติ
— คุณเป็นผู้พิจารณาแผนนี้
```

## §10 Data Binding & BACKEND anchors
| mock (prototype) | ระบบจริง (02_API) |
|---|---|
| `RECS` + `mkRec()` (seed 10 ใบ ชื่อสมมติ) | API-01/02 `/project-plans` |
| `EMP` · `empOf()` · `DEPTS` | HR · Employee / Organization (API-13 อ่าน) |
| `MOCK_DOA_RESOLVED` · `resolveDoa()` (marker DOA-ENGINE-HOOK) | API-05 doa-preview · GET /doa/resolve |
| `persist()` (SEQ + รหัส PJP) | API-03/04 · ENG-DOC-NUM (FN-03) |
| `validateMain()` · `dayDiff()` · `durTxt()` · `sumReq()` · `sumAppr()` | FN-01 / FN-02 (server คำนวณซ้ำ) |
| `confirmSubmit()` | API-06 |
| `confirmApprove()` (`setAppr()`) | API-07 approve + approved_budget[] (ขั้นสุดท้าย) |
| `confirmReason()` | API-07 reject / API-08 cancel |
| `confirmStatus()` | API-09 สถานะกิจกรรม |
| `docPrintData()` + `tplRender()` + `DOC_TPL` | API-10 PDF (server render template เดียวกัน) |
| `exportCSV()` | API-11 |
| `gateFiles()` | API-12 Document Center |
| `DOC.active` | F-DOCCFG status PJP |
| `commitRejected()` + `S.sim` | จำลอง 409/403/500 (prototype-only) |

## §11 Traceability + Drift Log
| Brief | FRD | HTML anchor |
|---|---|---|
| §4 P-01 | 01_UI P-01 · API-01/11 · FN-10 | `renderPage()` |
| §4 P-02 | 01_UI P-02 · API-03/04/12/13 · FN-01/02/03 · VR-01..06 | `renderWizard()` `wizMain()` `validateMain()` |
| §4 P-03 | 01_UI P-03 · API-02/05..10 · FN-04..08/11 | `renderViewDrawer()` |
| §6 modal ส่ง | API-06 · FN-04 · VR-08 | `renderModal()` (submit · `.slot-row`) |
| §6 modal อนุมัติ | API-07 · FN-05 · BR-05 · VR-07 | `apprTable()` `confirmApprove()` |
| §6 modal ไม่อนุมัติ/ยกเลิก | API-07/08 · FN-06/07 · VR-09 | `confirmReason()` |
| §6 modal อัปเดตสถานะ | API-09 · FN-11 · BR-12/13 | `openStatus()` `confirmStatus()` |
| §8 กิจกรรมล่าช้า | BR-12 · FN-09/10 | `nDelayed()` |
| §4 นอกช่วงโครงการ | BR-03 · DEC-16 | `outOfRange()` |
**Drift Log:** HTML-only (prototype-only ไม่ build): `window.__QA__` · `switchPersona()` · `S.sim` / `commitRejected()` · FRD-only: API-09 รองรับผู้รับผิดชอบหลักที่ไม่ใช่เจ้าของ (prototype: ต้องเห็นใบก่อน — OQ-07) · ไม่มี business drift

## §12 Diff จากเวอร์ชันก่อน
— ไม่มี (เวอร์ชันแรก)

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- มุมมอง Gantt ของแผนการดำเนินงาน (Phase 2)
- ลิงก์ไปรายงานความคืบหน้า (FM-PDM-02) จากใบที่อนุมัติแล้ว
