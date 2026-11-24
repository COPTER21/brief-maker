# UI_BRIEF — F-TMP-005 รายงานความคืบหน้าโครงการ (Project Progress Report)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| HTML | `feature.html` · html-generator-v9.4 · archetype **Q-form** (`<meta name="cube-archetype" content="Q-form">`) · `window.__QA__` มี |
| FRD | FRD_F-TMP-005_Pack v1.0 (00–07 · frd_lint BLOCK 0) · BRD-PDM-PPR-001 APPROVED |
| DECISIONS | DECISIONS.lock 20 มติ (AI-DEFAULT 15 · VALID 5) |
| Gate | audit.sh FAIL 0 · self_audit PASS · e2e_standard 21/21 + flow 20/20 (Chromium ใน container ของ agent — เครื่องผู้ใช้ NO-BROWSER) |
| Drift | ดู §11 — ไม่มี business drift · prototype-only = `window.__QA__` · ตัวสลับผู้ใช้ (`switchPersona()`) · `S.sim` · mock `PROJECTS` (แทน API F-TMP-004) |
| Date | 2026-10-11 |

## §1 Design Tokens AS-BUILT
- ฟอนต์: Noto Sans Thai + Satoshi (Google Fonts / Fontshare) · แบบพิมพ์ใช้ Sarabun (ใน PDF_CSS)
- สี/ระยะ/รัศมี = CSS variables ของ kit CUBE Warm Light (ตารางเต็มท้ายหัวข้อนี้) · ห้ามเพิ่มเฉดใหม่ (U10)
- scrollbar: custom `::-webkit-scrollbar` + `scrollbar-width: thin` · `scrollbar-gutter: stable`
- Page-specific CSS ของ feature นี้: `.person-ic` · `.ph-count.is-warn` · `.cell-ellipsis` · `.cell-warn` · `.pg-size` · `.pj-tbl` (ตารางดู) · `.pj-edit` (ตารางแก้ไข) · `.pj-pct` · `.pj-total` · `.pj-grid2` · `.pj-dash` / `.pj-dash-h` (แผน vs ผลจริง) · `.track-grid.is-3` (☐ สถานะ 3 ตัวเลือก) · `.field-static` · `.bd-bad` · `.ss-bad` · `.alert-row.is-warning` · ตัวเลือกวัน `.bedate` / `.bd-pop`


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
| `#/project-progress` | P-01 รายการ (default ของ feature) | `applyRoute()` · `renderPage()` |
| `#/project-progress/view/:id` | P-03 drawer ดู (เปิดได้เฉพาะใบที่ `canSee()` · ไม่มีสิทธิ์ = ไม่เปิด) | `openView()` · `showDrawer()` |
| `#/project-progress/create` | P-02 สร้าง (ไม่มีทำซ้ำ · DEC-15) | `startWizard()` |
| `#/project-progress/edit/:id` | P-02 แก้ร่าง (ผู้จัดทำ/PM · draft · `canEdit()`) | `startWizard()` |
- refresh-safe: `hashchange` → `applyRoute()` · ปิด drawer → `go()` กลับ `#/project-progress`

## §3 Layout Shell
- `.sidebar` (module Project › รายงานความคืบหน้า · badge `#sbBadge` = จำนวนรอฉันพิจารณา) · breadcrumb Core › Project › รายงานความคืบหน้าโครงการ · `.user-chip` + `#userMenu` (สลับผู้ใช้ — prototype-only · `#personaList`) · avatar ผู้ใช้ = `.person-ic`
- เนื้อหา `#page-content` · drawer `#drawer` + `#drawerBackdrop` · modal `#modalBackdrop` > `#modal` · `#toast` · portal `#overlay-root`

## §4 Page Anatomy
### P-01 รายการ (`renderPage()`)
- `.ph` → `.ph-title` "รายงานความคืบหน้าโครงการ" + `.ph-en` "(Project Progress Report)" · `.ph-count` จำนวน · `.ph-count.is-warn` "รอฉันพิจารณา n" · "รอฉันส่ง n" (ค่า 0 ไม่แสดง · U22) · `.ph-sub` · `.ph-actions` [ส่งออก CSV `exportCSV()`] [สร้างรายงาน `#btnCreate` → `startWizard()`]
- ไม่มี stat card (U1)
- `.card.list-card` → `.filter-bar` (`#fq` ค้นหา · combobox `#ss-fst` สถานะเอกสาร · `#ss-fov` สถานะโครงการ · ล้างตัวกรอง `resetFilters()`) → `table.table` คอลัมน์: เลขที่ · วันที่รายงาน · รหัสโครงการ · ชื่อโครงการ (`.cell-ellipsis`) · รอบการรายงาน (`periodText()`) · สถานะโครงการ (`ovPill()`) · สถานะเอกสาร (`docPill()`) · ลายเซ็น (`renderSignProgress()`) · ⋮ `.ra-btn` → `openRowMenu()`
- `pager()` → `.table-footer` : `.pg-size` (10/25/50 · `setPageSize()`) · "x–y จาก N" · `.pagination`
- แถว `.is-clickable` → `rowClick()` → `openView()`
### P-02 สร้าง/แก้ (`renderWizard()` · drawer `.drawer-panel.wide`)
- หัว: eyebrow สร้างเอกสารใหม่/แก้ไขเอกสาร · `stepper()` 3 ขั้น `.d-stepper` (`STEPS`)
- ขั้น 1 `wizMain()` · `.wz-split` : `.wz-main` การ์ด `CARD()` ①–⑦ ตามข้อของกระดาษ
  - ① `.pj-grid2`: รหัสโครงการ combobox `#ss-wproj` (PJP อนุมัติแล้ว · เลือกแล้ว `prefillFromProject()`) · ชื่อโครงการ / ผู้จัดการโครงการ / เลขที่ `.field-static` · รอบการรายงาน ตั้งแต่/ถึง + วันที่รายงาน `bedateHTML()` via `dateField()` · รอบทับ `.pd-line.is-warn` (`overlapOf()`)
  - ② `.track-grid.is-3` `.track-card` × 3 (`OVERALL` · `setFv('overall')`) + คำอธิบาย `fld()` / `tArea()`
  - ③ ตาราง `.pj-edit` `perfRows()` (% `.pj-pct`) · `.pd-line` % เฉลี่ย `#wAvg` (`wizAvg()`)
  - ④ `.pj-dash` ระยะเวลา/งบ แผน-ผลจริง-สถานะ (`tIn()`) + ตาราง KPI `kpiRows()`
  - ⑤⑥ ตาราง `issueRows()` / `nextRows()` (ผู้รับผิดชอบ combobox `ownerCell()` → `searchSelectHTML()` · กำหนดเสร็จ `dateField()`) · ⑦ `decRows()`
  - `.add-row` `addRow()` · ลบ `removeRow()` · error `.trip-err` (แถว/กลุ่ม) · `sumCard()` `.wz-sum` : ผู้จัดทำ · ผู้จัดการโครงการ (ผู้ส่ง) · ผู้พิจารณาต่อขั้นจาก DOA ของ PM · `#sumPeriod` · `#sumPct` · สถานะโครงการ
- ขั้น 2 `wizAttach()` `.upload-zone` → `#ppFile` · `pickFiles()` / `removeFile()`
- ขั้น 3 `wizReview()` คำเตือน `warnsOf()` `.alert-row.is-warning` · `.review-card` × 8 · ตาราง `perfTable()` `dashTable()` `issuesTable()` `nextTable()` `decTable()`
- `.dw-footer` : ย้อนกลับ `wizBack()` · ยกเลิก `closeDrawer()` · ถัดไป `#btnNext` `wizNext()` / บันทึกแบบร่าง `#btnDraft` `saveDraft()` · `#btnSaveSubmit` `saveAndSubmit()` = "บันทึกและส่งอนุมัติ" (PM) หรือ "บันทึกและแจ้งผู้จัดการโครงการ" (ไม่ใช่ PM) (loading `.spin` loader-2)
### P-03 ดู (`renderViewDrawer()` · drawer 920)
- `.dw-head` lean: `.dw-eyebrow` ชื่อเอกสาร · `.dw-title` เลขที่ + `docPill()` · `.dw-sub` รหัสโครงการ · รอบ · `.dw-actions` ตามสถานะ (§8) + พิมพ์ `genPdf()` · ปิด
- `.drawer-tabs` `tabBtn()` : รายละเอียด `renderDetailTab()` · PDF Preview `renderPdfTab()` · ลายเซ็น / อนุมัติ `renderSignTab()` · ประวัติ `renderHistoryTab()`
- รายละเอียด: `viewBanner()` + คำเตือน (ร่าง) · `SEC()` ข้อมูลเอกสาร · ข้อมูลโครงการ · ข้อ 1–6 (ตาราง `.pj-tbl` · `.pj-total` หัว KPI) · เอกสารแนบ `fileRow()` · ข้อมูลระบบ
- PDF: `.pv-bar` + `.a4` > `.pdf-slot` > `iframe.pdf-frame[srcdoc]` (`docPdfDoc()` · `fitPdf()`) · A4 2 หน้า
- ลายเซ็น: timeline ผู้จัดทำ → ผู้จัดการโครงการ (ส่ง) → ขั้น DOA 1..N · ปุ่มตัดสิน inline

## §5 Component Inventory
| Component | anchor | states |
|---|---|---|
| Search combobox | `searchSelectHTML()` / `initSearchSelect()` · `.search-select` · list portal `.ss-list` | default · open · filtered · empty "ไม่พบ" · selected (clear ×) · error `.ss-bad` (แถวตาราง) |
| ตัวเลือกวัน พ.ศ. | `bedateHTML()` · `.bedate` · popover `.bd-pop` | placeholder "เลือกวันที่" · open · min (ถึง ≥ ตั้งแต่) · error `.bd-bad` |
| การ์ดเลือกสถานะ | `.track-card` `.tc-ic` `.tc-radio` | ปกติ · `.is-on` · กลุ่มผิด `.track-grid.is-bad` + `.trip-err` |
| ตารางแก้ไข 5 กลุ่ม | `.pj-edit` | ปกติ · ช่องผิด `.is-bad` + `.row-err` `.trip-err` · ถึงขั้นต่ำ = ไม่มีปุ่มลบ |
| ตารางดู | `.pj-tbl` | มีข้อมูล · ว่าง = `emptyStateHTML()` "ไม่มีข้อมูล" (U23) · งบจริงเกินแผน `.cell-warn` |
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
| modal `#modal` (`.is-lg` สำหรับ ส่ง/อนุมัติ) | — | `openModalCfg()` | ปุ่ม · Esc · mousedown backdrop (`modalBackdropClick()` — มีเหตุผล/ความเห็นค้าง = **ไม่ปิด**) | `var(--z-modal)` |
| row-menu `.row-menu` | 200 | `openRowMenu()` | click ที่อื่น · scroll | `var(--z-popover)` |
| combobox list `.ss-list` | ความกว้างช่อง | focus/พิมพ์ | click ที่อื่น · Esc | `var(--z-popover)` |
| ปฏิทิน `.bd-pop` | 280 | `bdToggle()` | click นอก · Esc (ปิดแค่ปฏิทิน) | `var(--z-popover)` |
| user-menu `#userMenu` | — | `toggleUserMenu()` | click นอก | `var(--z-dropdown)` |
| toast `#toast` | — | `showToast()` | อัตโนมัติ | `var(--z-toast)` |

## §7 Interaction Spec
- Esc chain: ปฏิทินเปิด → ปิดปฏิทินอย่างเดียว · combobox เปิด → ปิด list · มี modal → `closeModal()` · มี drawer → `closeDrawer()` (wizard กรอกค้าง → modal "ทิ้งข้อมูลที่กรอกไว้?")
- backdrop: `onmousedown` + `event.target===this` เท่านั้น (U25)
- row click เปิด view ยกเว้นคลิกใน `.row-actions-cell`
- พิมพ์ข้อความ/ตัวเลข = soft update (`setFv()` · `setRow()` soft · `softSum()`) ไม่ rebuild → focus ไม่หลุด · % เฉลี่ย/รอบอัปเดตสด
- เลือกโครงการ → `prefillFromProject()` เติมเฉพาะส่วนที่ว่าง · เลือกวันเริ่มรอบหลังวันสิ้นรอบ → วันสิ้นรอบเลื่อนตาม · เพิ่มแถว `addRow()` focus ช่องแรกแถวใหม่
- `render()` ใช้ `preserveRenderState()` / `restoreRenderState()` · `renderIcons()` หลังทุก render
- แก้ไขจาก view = ปิด view แล้วเปิด wizard (ไม่ซ้อน · U15)

## §8 State-Driven UI Matrix
| status | pill (`DOC_ST`) | ปุ่มหัว drawer | ⋮ |
|---|---|---|---|
| draft | ร่าง `pill-muted` | ผู้จัดทำ/PM: ยกเลิก (เจ้าของ) · แก้ไข · ส่งอนุมัติ `#btnSubmitView` (PM) หรือ แจ้งผู้จัดการโครงการ `#btnNotifyPm` (ไม่ใช่ PM) | แก้ไข · พิมพ์ · ส่งอนุมัติ[PM] · ยกเลิกเอกสาร |
| pending | รออนุมัติ `pill-warning` | ผู้พิจารณาขั้นปัจจุบัน: คำปฏิเสธ · คำอนุมัติ ตาม role (`#btnApproveView` `.btn-success`) · เจ้าของ/admin: ยกเลิกเอกสาร | พิมพ์ · ยกเลิกเอกสาร[สิทธิ์] |
| approved | อนุมัติแล้ว `pill-success` | — | พิมพ์ |
| cancelled | ยกเลิก `pill-muted` | — | พิมพ์ |
- สถานะโครงการ (`OVERALL`): เป็นไปตามแผน `pill-success` · มีความเสี่ยง `pill-warning` · ล่าช้า หรือมีปัญหา `pill-danger`
- แบนเนอร์ (`viewBanner()`): ร่างที่ถูกส่งกลับ `.alert-row.is-danger` · ร่างรอ PM ส่ง · รอ (ขั้น n) · อนุมัติแล้ว `.alert-row.is-success` · ยกเลิก
- คำตัดสินตาม role: `wordsOf()` จาก `DECISION_WORDS` (role-line-manager = ตรวจสอบแล้ว/ไม่ผ่านการตรวจสอบ · role-gm = อนุมัติ/ไม่อนุมัติ)
- modal ส่ง: slot ต่อขั้น `.slot-row` (ค่าเริ่มจาก `resolveDoa(PM)`) · ล่าช้าฯ = แถบแจ้ง GM · คำเตือน `warnsOf()`


## §9 Microcopy (verbatim)
### Toast (`showToast()`)
| variant | ข้อความ |
|---|---|
| info | ไม่มีการแจ้งเตือนใหม่ |
| warning | แบบเอกสารนี้ยังไม่เปิดใช้งาน |
| warning | แก้ไขได้เฉพาะร่างของตัวเอง หรือร่างของโครงการที่คุณเป็นผู้จัดการ |
| warning | กรุณากรอกข้อมูลให้ครบถ้วน |
| warning | กรุณากรอกข้อมูลให้ครบถ้วน |
| info | บันทึกร่างแล้ว · |
| warning | กรุณากรอกข้อมูลให้ครบถ้วน |
| info | แจ้ง |
| warning | ส่งอนุมัติได้เฉพาะผู้จัดการโครงการ |
| info | ส่งอนุมัติแล้ว · |
| info | ส่งออก |
| info | สลับเป็น |
| error | แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง |
### ปุ่ม / label / placeholder / empty (ตรงจอ)
สร้างรายงาน · ส่งออก CSV · ล้างตัวกรอง · ส่งอนุมัติ · แจ้งผู้จัดการโครงการ · บันทึกแบบร่าง · บันทึกและส่งอนุมัติ · บันทึกและแจ้งผู้จัดการโครงการ · ถัดไป · ย้อนกลับ · ยกเลิก · ยกเลิกเอกสาร · ตรวจสอบแล้ว · ไม่ผ่านการตรวจสอบ · อนุมัติ · ไม่อนุมัติ · ทิ้งข้อมูล · กลับไปกรอกต่อ · เพิ่มกิจกรรม · เพิ่ม KPI · เพิ่มปัญหา / ความเสี่ยง · เพิ่มแผนงาน · เพิ่มประเด็น · พิมพ์ · ดาวน์โหลด PDF
placeholder: ค้นหาเลขที่ / โครงการ / ผู้จัดทำ · ไม่บังคับ เช่น ผลการตัดสินใจต่อประเด็นที่เสนอ · aria: ${ph || k} · จำนวนต่อหน้า · เดือนก่อน · เดือนถัดไป
### Microcopy inventory (สกัดจาก HTML · verbatim)
```
% สำเร็จ
(ขั้น
22 นาที
24 นาที
[Lucide] All CDNs failed. Icons จะไม่แสดง but UI ยังใช้งานได้
]); if (canCancel(r)) items.push(['x-circle', 'ยกเลิกเอกสาร',
]); if (canSubmit(r)) items.push(['send', 'ส่งอนุมัติ',
]]; /* G10 ทำซ้ำ ✗ */ if (canEdit(r)) items.unshift(['pencil', 'แก้ไข',
showToast('ไม่มีการแจ้งเตือนใหม่','info')
· กลับเป็นร่าง
· อนุมัติแล้ว ล็อกแก้ไข
· แจ้งผู้จัดการทั่วไปเรื่องต้องการการตัดสินใจเร่งด่วนแล้ว
ก. ขยาย 1 เดือน
ก. ขยาย 1 เดือน · ข. รับราคาผู้รับเหมารายเดียว
ก. ราคาต่ำสุด · ข. ส่งเร็วสุด
ก.ค.
ก.พ.
ก.ย.
กรกฎาคม
กรอกตามข้อของแบบฟอร์ม FM-PDM-02 · เลือกโครงการแล้วระบบเติมกิจกรรม ระยะเวลา งบ และ KPI จากแผนโครงการให้
กรอกให้ครบทุกช่องในแถวนี้
กรุณากรอกข้อมูลให้ครบถ้วน
กรุณากรอกตัวเลข ≥ 0
กรุณาเลือกวันสิ้นรอบ
กรุณาเลือกสถานะโครงการ
กันยายน
กานดา จัดหา
กำลังเปิดหน้าต่างพิมพ์ ·
กิจกรรม
กิจกรรม · เฉลี่ย
กุมภาพันธ์
ขยายเวลาโครงการ
ขอรายละเอียดงบที่ใช้จริงแยกตามรายการ
ขอแนวทางแก้ไขปัญหาที่ชัดเจนกว่านี้
ขอใบเสนอราคาอุปกรณ์สแกนบาร์โค้ด
ขอให้ผู้ขายส่งบางส่วนก่อน
ขั้นทดสอบ
ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
ข้อมูลผลงานไม่ครบ ขอรายละเอียดเพิ่ม
ข้อมูลหลักรายงาน
ข้อเสนอแนะ
ข้าม
คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
ความคลาดเคลื่อนสต๊อก
คัดเลือกผู้รับเหมา
คาดว่าช้า 3 สัปดาห์
คำอธิบาย
คุณไม่มีสิทธิ์ทำรายการนี้
คุณไม่ใช่ผู้จัดการโครงการนี้ — บันทึกร่างแล้วแจ้งผู้จัดการโครงการตรวจและส่งอนุมัติ
ค่าเริ่มต้นจาก DOA และผังองค์กรของผู้จัดการโครงการ
ค่าใช้จ่ายเพิ่ม 8,000 บาท แต่ไม่เลื่อนแผนติดตั้ง
ค้นรหัส / ชื่อโครงการที่อนุมัติแล้ว
ค้นหา...
ค้นหาเลขที่ / โครงการ / ผู้จัดทำ
งบประมาณ — ผลจริง
งบประมาณ — แผนงาน
งบผลจริง
งบแผน
งานติดตั้งเลื่อน
งานสำรวจเสร็จตามแผน เริ่มออกแบบผังจัดเก็บใหม่แล้ว งบประมาณใช้ตามแผน
จัดซื้อหลอด LED
จัดทำในระบบ
จัดหาอุปกรณ์สแกนบาร์โค้ด
จำนวนต่อหน้า
จำนวนสายสอบถามสถานะ
ชนิดไฟล์ไม่รองรับ
ชื่อฟังก์ชัน
ชื่อโครงการ
ช้ากว่าแผน 5 วัน
ช้ากว่าแผน 7 วัน
ซ้ำกับรายงานเดิม
ซ้ำกับรายงานเดิม — ใช้ PPR-2569-0001 แทน
ดึงจากแผนโครงการ
ต.ค.
ตรวจสอบและยืนยัน
ตรวจสอบแล้ว
ตัดสระบน-วรรณยุกต์-สระล่าง
ตัวชี้วัด
ตัวเลขงบประมาณไม่ตรงกับบัญชี
ตามแผน
ติดตั้ง
ติดตั้งหลอด LED ครบทุกอาคาร ปิดโครงการ
ติดตั้งอุปกรณ์ในรถ
ติดตั้งเลื่อน
ติดตั้งแผงและอินเวอร์เตอร์
ติดตั้งแผงโซลาร์เซลล์หลังคาโรงงาน
ติดตั้งและทดสอบระบบ
ตุลาคม
ต่ำกว่าแผน
ต้อง
ถึง
ถึงเป้า
ทางเลือก
ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
ธ.ค.
ธนากร ช่างคิด
ธันวาคม
บริษัท ตัวอย่าง จำกัด
บันทึกซ้ำ
บันทึกผลขั้น
บันทึกผิดรอบ
บันทึกร่างแล้ว ·
ประกวดราคารอบใหม่
ประวัติ
ประวัติ (append-only)
ประเด็นที่ต้องการการตัดสินใจ
ประเสริฐ บริหารดี
ปรับปรุงระบบจัดเก็บสินค้าคลังกลาง
ปัญหา / ความเสี่ยง
ปิด
ปิยะดา วางแผน
ผลกระทบ
ผลการดำเนินงาน
ผลงานจริง
ผลงานเป็นไปตามแผนงาน งบประมาณ และระยะเวลาที่กำหนด ไม่มีปัญหาที่ส่งผลกระทบต่อเป้าหมายโครงการ
ผลจริง
ผลจริง (Actual)
ผังจัดเก็บใหม่เสร็จตามแผน · การจัดหาอุปกรณ์สแกนช้ากว่าแผนประมาณ 1 สัปดาห์ เพราะผู้ขายส่งใบเสนอราคาล่าช้า
ผู้ขายส่งล่าช้า
ผู้ขายอุปกรณ์ส่งใบเสนอราคาล่าช้า
ผู้จัดการทั่วไป
ผู้จัดการฝ่ายพัฒนาโครงการ
ผู้จัดการฝ่ายวางแผน
ผู้จัดการโครงการ
ผู้จัดการโครงการ (Project Manager)
ผู้จัดการโครงการ (ผู้ส่ง)
ผู้จัดทำรายงาน
ผู้จัดทำรายงาน (Prepared by)
ผู้ตรวจสอบ (Reviewed by)
ผู้รับเหมา 2 จาก 3 รายถอนตัว การคัดเลือกผู้รับเหมาจะไม่เสร็จตามแผน ต้องการให้ผู้บริหารตัดสินใจขยายเวลาหรือเพิ่มงบ
ผู้รับเหมาถอนตัว
ผู้รับเหมาถอนตัว 2 ราย
ผู้ส่ง (ผู้จัดการโครงการ)
ผู้อนุมัติ (Approved by)
ฝ่ายจัดซื้อ
ฝ่ายบริหาร
ฝ่ายพัฒนาโครงการ
ฝ่ายวางแผน
พ.ค.
พ.ย.
พฤ
พฤศจิกายน
พฤษภาคม
พิมพ์
ภาพรวม ความก้าวหน้าหลัก ปัญหาสำคัญ และสิ่งที่ต้องการจากผู้บริหาร
ม.ค.
มกราคม
มานพ ประสานงาน
มิ.ย.
มิถุนายน
มี.ค.
มีความล่าช้าหรือปัญหาที่ส่งผลกระทบชัดเจนต่อแผนงาน งบประมาณ หรือเป้าหมายโครงการ ต้องการการตัดสินใจเร่งด่วน
มีความเสี่ยง
มีความเสี่ยงหรือประเด็นที่อาจส่งผลกระทบต่อแผนงาน/งบประมาณ ต้องเฝ้าติดตามอย่างใกล้ชิด
มีนาคม
ยกเลิก
ยกเลิกเอกสาร
ยกเลิกเอกสาร?
ยกเลิกเอกสารแล้ว ·
ยังไม่ถึงขั้นนี้
ยังไม่ถึงเป้า
ยังไม่มีข้อมูล
ยังไม่มีผลการดำเนินงาน
ยังไม่มีรายงานความคืบหน้า
ยังไม่ส่ง
ยังไม่เบิกจ่าย
ยังไม่เริ่มวัดผล
ย้อนกลับ
รหัสโครงการ
รอบการรายงาน
รอบการรายงาน (ตั้งแต่)
รอบการรายงาน (ถึง)
รอบการรายงานทับกับ
รอบตั้งแต่
รอบถึง
รอพิจารณา
รออนุมัติ
ระบบติดตามรถขนส่งแบบเรียลไทม์
ระบบออกให้เมื่อบันทึก (PPR-ปี-ลำดับ)
ระบุตอนส่ง
ระยะเวลา — ผลจริง
ระยะเวลา — แผนงาน
รับมอบและตรวจรับอุปกรณ์
รายการ
รายการมีกำหนดแล้วเสร็จก่อนวันที่รายงาน
รายงานความคืบหน้าโครงการ
รายละเอียด
ร่าง
ร่างผังแล้ว
ร่างรายงาน
ลด 40%
ลด 43%
ลด 50%
ลบแถว
ลบไฟล์
ลองปรับคำค้นหรือล้างตัวกรอง
ลายเซ็น / อนุมัติ
ลำดับ
ลำดับการลงนาม (บล็อกลงชื่อท้ายรายงาน)
ล่าช้า
ล่าช้า หรือมีปัญหา
ล้างตัวกรอง
วันที่ ........./........./.........
วันที่รายงาน
วันที่รายงานอยู่ก่อนวันสิ้นรอบการรายงาน
วันสิ้นรอบต้องไม่ก่อนวันเริ่มรอบ
วิภาวี ตรวจดี
วิศวกรโครงการ
ศศิธร ดูแลงาน
ส.ค.
สถานะ
สถานะ (Status)
สถานะ มีความเสี่ยง แต่ยังไม่ระบุปัญหา อุปสรรค และความเสี่ยง
สถานะ ล่าช้า หรือมีปัญหา ต้องระบุปัญหา อุปสรรค และความเสี่ยงอย่างน้อย 1 รายการ
สถานะ ล่าช้า หรือมีปัญหา แต่ยังไม่มีประเด็นที่ต้องการการตัดสินใจจากผู้บริหาร
สถานะ ล่าช้า หรือมีปัญหา — ระบบแจ้งผู้จัดการทั่วไปทันทีเมื่อส่ง
สถานะเอกสาร
สถานะโครงการ
สมพร ตั้งใจ
สรุปผังจัดเก็บใหม่และขออนุมัติผัง
สรุปสถานะโครงการ
สรุปสถานะโครงการ (PROJECT STATUS SUMMARY)
สร้าง PDF
สร้างรายงาน
สร้างรายงานความคืบหน้าของโครงการที่อนุมัติแล้ว
สร้างเอกสาร
สร้างเอกสารใหม่
สร้างโดย
สลับเป็น
สั่งซื้อภายใน 30 ก.ย. 69
สั่งซื้ออุปกรณ์สแกนแล้ว รอส่งมอบ
สั่งซื้อเลื่อน 1 สัปดาห์
สั่งซื้อแล้ว 7 ต.ค. 69
สายอนุมัติ
สำรวจกระบวนการคลังปัจจุบัน
สำรวจโครงสร้างหลังคา
สำรวจโครงสร้างหลังคาเสร็จ รับน้ำหนักได้ตามที่ออกแบบ
สิงหาคม
สิ้นสุดโครงการเลื่อนเป็น ก.พ. 2570
ส่งกลับเป็นร่างแล้ว ·
ส่งอนุมัติ
ส่งอนุมัติ?
ส่งอนุมัติแล้ว ·
ส่งอนุมัติได้เฉพาะผู้จัดการโครงการ
ส่งออก
ส่งแล้วแก้ไขไม่ได้ — ถ้าไม่ผ่านการพิจารณา เอกสารจะกลับเป็นร่างให้แก้แล้วส่งใหม่
หน่วยไฟฟ้าที่ผลิตได้ต่อเดือน
หน่วยไฟฟ้าแสงสว่าง
หมายเหตุ
อนุชา นำทาง
อนุมัติ
อนุมัติรายงานแล้ว
อนุมัติแล้ว
อบรมพนักงานคลัง
ออกแบบผังจัดเก็บใหม่
ออกใบสั่งซื้ออุปกรณ์สแกนบาร์โค้ด
อา
อุปกรณ์ส่งมอบล่าช้า 1 สัปดาห์
เจ้าหน้าที่จัดซื้อ
เจ้าหน้าที่ธุรการโครงการ
เจ้าหน้าที่พัฒนาโครงการ
เจ้าหน้าที่วางแผน
เช่น ช้ากว่าแผน 5 วัน
เช่น ภาพความคืบหน้าหน้างาน ใบเสนอราคา หรือรายงานทดสอบ
เดือนถัดไป
เด้งกลับบน
เตรียม TOR แล้ว
เตรียมรายชื่อผู้ให้บริการ
เตรียมเอกสารคัดเลือกผู้ให้บริการ GPS
เปลี่ยนหลอดไฟ LED ทั้งโรงงาน
เปิดประกวดราคารอบใหม่
เปิดประกวดราคารอบใหม่แล้ว รอผู้เสนอราคา
เปิดใช้งานและอบรม
เป็นไปตามแผน
เฝ้าติดตาม
เพิ่ม KPI
เพิ่มกิจกรรม
เพิ่มประเด็น
เพิ่มปัญหา / ความเสี่ยง
เพิ่มผู้ขายรายที่ 4 และเร่งติดตาม
เพิ่มเติม
เพิ่มแผนงาน
เม.ย.
เมษายน
เริ่ม 2 พ.ย. 69
เรื่อง
เรื่องที่เสนอ
เลขที่
เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
เลือก ข. ส่งเร็วสุด
เลือกประเทศ
เลือกผู้ขายอุปกรณ์สแกน
เลือกผู้พิจารณา
เลือกผู้ให้บริการ GPS
เลือกวันที่
เลือกโครงการก่อน
เวลาหยิบเฉลี่ยต่อใบ
เสร็จ
เสร็จ 2 ต.ค. 69
เสร็จ 24 ก.ค. 69
เสร็จ 25 ก.ย. 69
เสร็จ 27 ส.ค. 69
เสร็จ 28 ส.ค. 69
เสร็จ 30 ต.ค. 69
เสร็จก่อนแผน 1 วัน
เหตุผลที่ยกเลิก
เหลือผู้เสนอราคา 1 ราย
เอกสาร
เอกสารแนบ
แก้ไข
แก้ไขรายงาน
แก้ไขร่าง
แก้ไขล่าสุด
แก้ไขเอกสาร
แก้ไขได้เฉพาะร่างของตัวเอง หรือร่างของโครงการที่คุณเป็นผู้จัดการ
แจ้ง
แจ้งผู้จัดการโครงการ
แจ้งผู้จัดทำว่าเพราะอะไร
แนบเอกสารประกอบ (ถ้ามี)
แนบไฟล์เพิ่ม
แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
แนวทางแก้ไข
แบบเอกสารนี้ยังไม่เปิดใช้งาน
แผนงาน
แผนงาน (Plan)
โครงการ
โครงการถูกยกเลิก
โครงการและรอบการรายงาน
ใบเสนอราคาอุปกรณ์สแกน.pdf
ให้ตรวจและส่งอนุมัติแล้ว ·
ได้ใบเสนอราคา 2 จาก 3 ราย
ไม่บังคับ
ไม่ผ่านการตรวจสอบ
ไม่พบรายการ
ไม่พบรายการที่ค้นหา
ไม่มีการแข่งขันราคา · งานติดตั้งเลื่อน
ไม่มีข้อมูล
ไม่มีประเด็นที่ต้องการการตัดสินใจ
ไม่ยกเลิก
ไม่อนุมัติ
ไม่ได้ระบุปัญหา อุปสรรค และความเสี่ยง
ไม่ได้ระบุแผนงานในรอบถัดไป
— คุณเป็นผู้พิจารณารายงานนี้
≤ 17 นาที
```

## §10 Data Binding & BACKEND anchors
| mock (prototype) | ระบบจริง (02_API) |
|---|---|
| `RECS` + `mkRec()` (seed 10 ใบ ชื่อสมมติ) | API-01/02 `/progress-reports` |
| `PROJECTS` · `projOf()` · `pmOf()` | API-13 F-TMP-004 `/project-plans?status=approved` (อ่าน) |
| `EMP` · `empOf()` | HR · Employee (API-14 อ่าน) |
| `MOCK_DOA_RESOLVED` · `resolveDoa()` (marker DOA-ENGINE-HOOK) | API-05 doa-preview · GET /doa/resolve |
| `persist()` (SEQ + เลข PPR) | API-03/04 · ENG-DOC-NUM (FN-03) |
| `validateMain()` · `warnsOf()` · `overlapOf()` · `prefillFromProject()` | FN-01 / FN-02 (server ตรวจซ้ำ) |
| `confirmSubmit()` | API-06 (PM เท่านั้น) |
| `notifyPm()` | API-09 notify-pm |
| `confirmApprove()` | API-07 approve |
| `confirmReason()` | API-07 reject / API-08 cancel |
| `docPrintData()` + `tplRender()` + `DOC_TPL` | API-10 PDF (server render template เดียวกัน) |
| `exportCSV()` | API-11 |
| `gateFiles()` | API-12 Document Center |
| `DOC.active` | F-DOCCFG status PPR |
| `commitRejected()` + `S.sim` | จำลอง 409/403/500 (prototype-only) |

## §11 Traceability + Drift Log
| Brief | FRD | HTML anchor |
|---|---|---|
| §4 P-01 | 01_UI P-01 · API-01/11 · FN-10 | `renderPage()` |
| §4 P-02 | 01_UI P-02 · API-03/04/12/13/14 · FN-01/02/03 · VR-01..07 | `renderWizard()` `wizMain()` `validateMain()` |
| §4 P-03 | 01_UI P-03 · API-02/05..10 · FN-04..08/11 | `renderViewDrawer()` |
| §6 modal ส่ง | API-06 · FN-04 · VR-08 · BR-07 | `renderModal()` (submit · `.slot-row`) |
| §6 modal อนุมัติ | API-07 · FN-05 | `confirmApprove()` |
| §6 modal ไม่อนุมัติ/ยกเลิก | API-07/08 · FN-06/07 · VR-09 | `confirmReason()` |
| §8 แจ้งผู้จัดการโครงการ | API-09 · FN-11 · BR-07 | `notifyPm()` |
| §4 คำเตือน | BR-05/06 · DEC-18/19 | `warnsOf()` |
**Drift Log:** HTML-only (prototype-only ไม่ build): `window.__QA__` · `switchPersona()` · `S.sim` / `commitRejected()` · `PROJECTS` mock แทน F-TMP-004 API · ไม่มี business drift

## §12 Diff จากเวอร์ชันก่อน
— ไม่มี (เวอร์ชันแรก)

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- dashboard สถานะทุกโครงการ (รวมสถานะโครงการล่าสุดต่อ PJP) — Phase 2
- ลิงก์จากแผนโครงการ (F-TMP-004) ไปรายงานความคืบหน้าของโครงการนั้น
