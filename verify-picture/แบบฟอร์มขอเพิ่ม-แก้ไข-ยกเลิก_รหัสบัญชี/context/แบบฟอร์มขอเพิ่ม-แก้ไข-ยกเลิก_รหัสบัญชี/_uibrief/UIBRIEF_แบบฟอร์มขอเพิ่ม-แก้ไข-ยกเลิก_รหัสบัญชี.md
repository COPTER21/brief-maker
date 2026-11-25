# UI_BRIEF — F-TMP-003 แบบฟอร์มขอเพิ่ม-แก้ไข-ยกเลิก รหัสบัญชี (Account Code Request)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| HTML | `feature.html` · html-generator-v9.4 · archetype **Q-form** (`<meta name="cube-archetype" content="Q-form">`) · `window.__QA__` มี |
| FRD | FRD_F-TMP-003_Pack v1.0 (00–07 · frd_lint BLOCK 0) · BRD-ACC-ACR-001 APPROVED |
| DECISIONS | DECISIONS.lock 14 มติ (AI-DEFAULT 11 · VALID 3) |
| Gate | audit.sh FAIL 0 · self_audit PASS · e2e_standard 21/21 + flow 15/15 (Chromium ใน container — เครื่องผู้ใช้ NO-BROWSER) |
| Drift | ดู §11 — ไม่มี business drift · prototype-only = `window.__QA__` · ตัวสลับผู้ใช้ (`switchPersona()`) · `S.sim` |
| Date | 2026-10-11 |

## §1 Design Tokens AS-BUILT
- ฟอนต์: Noto Sans Thai + Satoshi (Google Fonts / Fontshare) · แบบพิมพ์ใช้ Sarabun (ใน PDF_CSS)
- สี/ระยะ/รัศมี = CSS variables ของ kit CUBE Warm Light (ตารางเต็มท้ายหัวข้อนี้) · ห้ามเพิ่มเฉดใหม่ (U10)
- scrollbar: custom `::-webkit-scrollbar` + `scrollbar-width: thin` · `scrollbar-gutter: stable`
- Page-specific CSS ของ feature นี้: `.person-ic` (วงกลม icon คน mono) · `.ph-count.is-warn` · `.cell-ellipsis` · `.pg-size` · `.track-grid.is-3` (track-card 3 ใบ) · `.acr-lines` / `.acr-line` / `.acr-no` / `.acr-err` (บรรทัดชื่อบัญชี) · `.acr-names` (รายการชื่อบัญชีในหน้าดู) · `.wz-card.is-muted` · `.alert-row.is-warning` · ตัวเลือกวัน `.bedate` / `.bd-pop`


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
| `#/account-code-request` | P-01 รายการ (default ของ feature) | `applyRoute()` · `renderPage()` |
| `#/account-code-request/view/:id` | P-03 drawer ดู (เปิดได้เฉพาะใบที่ `canSee()` · ไม่มีสิทธิ์ = ไม่เปิด) | `openView()` · `showDrawer()` |
| `#/account-code-request/create` | P-02 สร้าง (ไม่มีทำซ้ำ · DEC-11) | `startWizard()` |
| `#/account-code-request/edit/:id` | P-02 แก้ร่าง (เจ้าของ · draft) | `startWizard()` |
- refresh-safe: `hashchange` → `applyRoute()` · ปิด drawer → `go()` กลับ `#/account-code-request`

## §3 Layout Shell
- `.sidebar` (module Accounting › ขอเพิ่ม/แก้ไข/ยกเลิกรหัสบัญชี · badge `#sbBadge` = จำนวนรอฉันพิจารณา) · breadcrumb Core › Accounting › ขอเพิ่ม/แก้ไข/ยกเลิกรหัสบัญชี · `.user-chip` + `#userMenu` (สลับผู้ใช้ — prototype-only) · avatar ผู้ใช้ = `.person-ic`
- เนื้อหา `#page-content` · drawer `#drawer` + `#drawerBackdrop` · modal `#modalBackdrop` > `#modal` · `#toast` · portal `#overlay-root`

## §4 Page Anatomy
### P-01 รายการ (`renderPage()`)
- `.ph` → `.ph-title` "แบบฟอร์มขอเพิ่ม-แก้ไข-ยกเลิก รหัสบัญชี" + `.ph-en` "(Account Code Request)" · `.ph-count` จำนวน · `.ph-count.is-warn` "รอฉันพิจารณา n" · `.ph-count.is-warn` "รอบันทึกเข้าระบบ n" (admin · ค่า 0 ไม่แสดง · U22) · `.ph-sub` · `.ph-actions` [ส่งออก CSV `exportCSV()`] [สร้างคำขอ `#btnCreate` → `startWizard()`]
- ไม่มี stat card (U1)
- `.card.list-card` → `.filter-bar` (`#fq` ค้นหา · combobox `#ss-fst` สถานะ · `#ss-ftype` ประเภทคำขอ · ล้างตัวกรอง `resetFilters()`) → `.table-wrap` > `table.table` คอลัมน์: เลขที่ · วันที่ขอ · ผู้ขอ · ประเภทคำขอ (`typePill()`) · รหัส / ชื่อบัญชี (`.cell-ellipsis` · `summaryOf()`) · สถานะเอกสาร (`docPill()`) · ลายเซ็น (`renderSignProgress()`) · ⋮ `.ra-btn` → `openRowMenu()`
- `pager()` → `.table-footer` : `.pg-size` (10/25/50 · `setPageSize()`) · "x–y จาก N" · `.pagination`
- แถว `.is-clickable` → `rowClick()` → `openView()`
### P-02 สร้าง/แก้ (`renderWizard()` · drawer `.drawer-panel.wide`)
- หัว: eyebrow สร้างเอกสารใหม่/แก้ไขเอกสาร · `stepper()` 3 ขั้น `.d-stepper` (`STEPS`)
- ขั้น 1 `wizMain()` · `.wz-split` : `.wz-main` (การ์ด ① ขอทำอะไรกับผังบัญชี `#f_type` `.track-grid.is-3` > `.track-card` × 3 → `setType()` · การ์ด ② `typeSection()` : เพิ่ม = `#f_lines0` `.acr-lines` `addLineRow()` (`[name=ln-{i}]` · ลบ `removeLine()`) + `.add-row` เพิ่มอีกบัญชี `addLine()` + `fieldTa()` วัตถุประสงค์ในการเพิ่ม · แก้ไข = `fieldIn()` รหัสบัญชี/แก้ไขเป็น + วัตถุประสงค์ในการแก้ไข · ยกเลิก = รหัสบัญชี/ชื่อบัญชี + วัตถุประสงค์ในการยกเลิก · ยังไม่เลือก = `.wz-card.is-muted`) + `sumCard()` `.wz-sum`
- ขั้น 2 `wizAttach()` `.upload-zone` → `#acrFile` · `pickFiles()` / `removeFile()`
- ขั้น 3 `wizReview()` `.review-card` × 3 · `typeBlock()`
- `.dw-footer` : ย้อนกลับ `wizBack()` · ยกเลิก `closeDrawer()` · ถัดไป `#btnNext` `wizNext()` / บันทึกแบบร่าง `#btnDraft` `saveDraft()` · บันทึกและส่งอนุมัติ `#btnSaveSubmit` `saveAndSubmit()` (loading `.spin` loader-2)
### P-03 ดู (`renderViewDrawer()` · drawer 920)
- `.dw-head` lean: `.dw-eyebrow` ชื่อเอกสาร · `.dw-title` เลขที่ + `docPill()` · `.dw-sub` ประเภทคำขอ · `.dw-actions` ตามสถานะ (§8) + พิมพ์ `genPdf()` · ปิด
- `.drawer-tabs` `tabBtn()` : รายละเอียด `renderDetailTab()` · PDF Preview `renderPdfTab()` · ลายเซ็น / อนุมัติ `renderSignTab()` · ประวัติ `renderHistoryTab()`
- รายละเอียด: `viewBanner()` · `SEC()` ข้อมูลเอกสาร · ผู้ขอเพิ่ม/แก้ไข/ยกเลิกรหัสบัญชี · ส่วนตามประเภท `typeBlock()` · สำหรับผู้อนุมัติ `approverBlock()` · ผู้บันทึกเข้าระบบ `recordBlock()` · เอกสารแนบ `fileRow()` · ข้อมูลระบบ
- PDF: `.pv-bar` + `.a4` > `.pdf-slot` > `iframe.pdf-frame[srcdoc]` (`docPdfDoc()` · `fitPdf()`)

## §5 Component Inventory
| Component | anchor | states |
|---|---|---|
| Track-card ประเภทคำขอ | `.track-card` `.tc-radio` · `setType()` | default · hover · เลือกแล้ว `.is-on` · ยังไม่เลือกตอนกดถัดไป = `#f_type.is-invalid` + "กรุณาเลือกประเภทคำขอ" |
| บรรทัดชื่อบัญชี | `.acr-line` · `addLineRow()` | ปกติ · ชื่อซ้ำ `.is-bad` + `.acr-err` · 1 บรรทัด = ไม่มีปุ่มลบ (`.acr-sp`) · ทั้งหมดว่าง = `#f_lines0.is-invalid` |
| ช่องกรอก/ข้อความยาว | `fieldIn()` / `fieldTa()` · `.field` | ปกติ · `.is-invalid` + `.field-error` · พิมพ์แล้วหายแดงทันที (`setF2()`) |
| Search combobox | `searchSelectHTML()` / `initSearchSelect()` · `.search-select` | default · open · filtered · empty "ไม่พบ" · selected (clear ×) |
| ตัวเลือกวัน พ.ศ. | `bedateHTML()` · `.bedate` · popover `.bd-pop` | default · open · min (≥ วันที่อนุมัติ) · max (≤ วันนี้) · disabled day |
| คน | `empChip()` · `.emp-chip` + `.person-ic` | ชื่อ + ตำแหน่ง/บทบาท (ไม่มี initials · U17) |
| ลายเซ็น n/N | `renderSignProgress()` `.sign-prog` `.sp-bar` | ร่าง "—" · ระหว่างทาง · ยกเลิก `.is-bad` |
| Row menu ⋮ | `openRowMenu()` `.row-menu` `.rm-item` | รายการตามสิทธิ์ · ยกเลิก `.is-danger` |
| Toast | `showToast()` `#toast` | info · success · warning · error |
| Upload | `.upload-zone` · `gateFiles()` | ว่าง · มีไฟล์ · ไฟล์ผิดชนิด/ใหญ่เกิน (toast error) |

## §6 Overlay Registry
| Overlay | ขนาด | เปิด | ปิด / dismiss | z |
|---|---|---|---|---|
| drawer ดู `.drawer-panel` | 920 | `showDrawer()` | ปุ่มปิด · Esc · mousedown ที่ `#drawerBackdrop` (U25 — ลากจากในออกนอกไม่ปิด) | `var(--z-drawer)` |
| drawer สร้าง `.drawer-panel.wide` | 1290 | `startWizard()` | เหมือนบน · กรอกค้าง (`S.dw.dirty`) → modal ทิ้งข้อมูล | `var(--z-drawer)` |
| modal `#modal` (`.is-lg` สำหรับ ส่ง/บันทึกเข้าระบบ) | — | `openModalCfg()` | ปุ่ม · Esc · mousedown backdrop (`modalBackdropClick()` — มีเหตุผล/ความเห็นค้าง = **ไม่ปิด**) | `var(--z-modal)` |
| row-menu `.row-menu` | 180 | `openRowMenu()` | click ที่อื่น · scroll | `var(--z-popover)` |
| combobox list | ความกว้างช่อง | focus/พิมพ์ | click ที่อื่น · Esc (ไม่ทะลุปิด drawer) | `var(--z-popover)` |
| ปฏิทิน `.bd-pop` | 280 | `bedateHTML()` | click นอก · Esc (ปิดแค่ปฏิทิน) | `var(--z-popover)` |
| user-menu `#userMenu` | — | `toggleUserMenu()` | click นอก | `var(--z-dropdown)` |
| toast `#toast` | — | `showToast()` | อัตโนมัติ | `var(--z-toast)` |

## §7 Interaction Spec
- Esc chain: ปฏิทินเปิด → ปิดปฏิทินอย่างเดียว · combobox เปิด → ปิด list · มี modal → `closeModal()` · มี drawer → `closeDrawer()` (wizard กรอกค้าง → modal "ทิ้งข้อมูลที่กรอกไว้?")
- backdrop: `onmousedown` + `event.target===this` เท่านั้น (U25)
- row click เปิด view ยกเว้นคลิกใน `.row-actions-cell`
- พิมพ์ชื่อบัญชี/รหัส/วัตถุประสงค์ = soft update (`setLine()` · `setF2()` · `sumRefresh()`) ไม่ rebuild → focus ไม่หลุด
- เปลี่ยนประเภทคำขอ (`setType()`) → rebuild การ์ด ② · ค่าส่วนอื่นยังอยู่ในฟอร์มแต่ `persist()` ล้างทิ้งตอนบันทึก (DEC-13)
- เพิ่มบรรทัด `addLine()` → focus บรรทัดใหม่
- `render()` ใช้ `preserveRenderState()` / `restoreRenderState()` · `renderIcons()` หลังทุก render
- แก้ไขจาก view = ปิด view แล้วเปิด wizard (ไม่ซ้อน · U15)

## §8 State-Driven UI Matrix
| status | pill (`DOC_ST`) | ปุ่มหัว drawer | ⋮ |
|---|---|---|---|
| draft | ร่าง `pill-muted` | เจ้าของ: ยกเลิก · แก้ไข · ส่งอนุมัติ (`#btnSubmitView`) | แก้ไข · พิมพ์ · ยกเลิกเอกสาร |
| pending | รออนุมัติ `pill-warning` | ผู้พิจารณาขั้นปัจจุบัน: ไม่ผ่านการตรวจสอบ/ไม่อนุมัติ · ตรวจสอบแล้ว/อนุมัติ (`#btnApproveView` `.btn-success`) · เจ้าของ/admin: ยกเลิกเอกสาร | พิมพ์ · ยกเลิกเอกสาร[สิทธิ์] |
| approved | อนุมัติแล้ว · รอบันทึก `pill-success` | admin บัญชี: บันทึกเข้าระบบแล้ว (`#btnRecordView`) | พิมพ์ · บันทึกเข้าระบบแล้ว[admin] |
| recorded | บันทึกเข้าระบบแล้ว `pill-info` | — (ล็อก) | พิมพ์ |
| cancelled | ยกเลิก `pill-muted` | — | พิมพ์ |
- ประเภทคำขอ (`REQ_T` · `typePill()`): เพิ่มรหัสบัญชี `pill-success` · แก้ไขรหัสบัญชี `pill-info` · ยกเลิกรหัสบัญชี `pill-danger`
- แบนเนอร์ (`viewBanner()`): ร่างที่ถูกส่งกลับ `.alert-row.is-danger` · รอ · อนุมัติแล้วรอบันทึก `.alert-row.is-warning` · บันทึกแล้ว `.alert-row.is-success` · ยกเลิก
- คำตัดสินตาม role: `wordsOf()` จาก `DECISION_WORDS` (role-line-manager = ตรวจสอบแล้ว/ไม่ผ่านการตรวจสอบ · อื่น = อนุมัติ/ไม่อนุมัติ)


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
| info | บันทึกเข้าระบบแล้ว · |
| info | ส่งออก |
| info | สลับเป็น |
| error | แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง |
### ปุ่ม / label / placeholder / empty (ตรงจอ)
สร้างคำขอ · ส่งออก CSV · ล้างตัวกรอง · ส่งอนุมัติ · บันทึกแบบร่าง · บันทึกและส่งอนุมัติ · ถัดไป · ย้อนกลับ · ยกเลิก · ยกเลิกเอกสาร · ตรวจสอบแล้ว · ไม่ผ่านการตรวจสอบ · อนุมัติ · ไม่อนุมัติ · บันทึกเข้าระบบแล้ว · ทิ้งข้อมูล · กลับไปกรอกต่อ · เพิ่มอีกบัญชี · พิมพ์ · ดาวน์โหลด PDF
placeholder: ค้นหาเลขที่ / ผู้ขอ / รหัสหรือชื่อบัญชี · เช่น รายได้ค่าบริการติดตั้ง · ไม่บังคับ · aria: จำนวนต่อหน้า · ชื่อบัญชีที่ต้องการขอเพิ่ม ${i + 1} · เดือนก่อน · เดือนถัดไป
### Microcopy inventory (สกัดจาก HTML · verbatim)
```
(ขั้น
1 ใบต่อ 1 ประเภทคำขอ — เลือกว่าจะเพิ่ม แก้ไข หรือยกเลิกรหัสบัญชี แล้วกรอกเฉพาะส่วนนั้น
[Lucide] All CDNs failed. Icons จะไม่แสดง but UI ยังใช้งานได้
]); if (canCancel(r)) items.push(['x-circle', 'ยกเลิกเอกสาร',
]); if (canRecord(r)) items.push(['database', 'บันทึกเข้าระบบแล้ว',
]]; /* DEC-11 ทำซ้ำ ✗ */ if (isOwner(r) && r.status === 'draft') items.unshift(['pencil', 'แก้ไข',
showToast('ไม่มีการแจ้งเตือนใหม่','info')
· กด "บันทึกเข้าระบบแล้ว" เมื่อแก้ผังบัญชีเสร็จ
· ส่งต่อขั้น
· อนุมัติแล้ว ล็อกแก้ไข
ก.ค.
ก.พ.
ก.ย.
กรกฎาคม
กรณีขอเพิ่มรหัสบัญชี
กรุณากรอกข้อมูลให้ครบถ้วน
กรุณาระบุชื่อบัญชี
กรุณาระบุรหัสบัญชี
กรุณาระบุวัตถุประสงค์ในการยกเลิก
กรุณาระบุวัตถุประสงค์ในการเพิ่ม
กรุณาระบุวัตถุประสงค์ในการแก้ไข
กรุณาระบุว่าแก้ไขเป็นอะไร
กันยายน
กำลังเปิดหน้าต่างพิมพ์ ·
กิตติ ศรีสุข
กุมภาพันธ์
ขอเปิดบัญชีใหม่ในผังบัญชี
ขั้นทดสอบ
ขั้นสุดท้าย — ต่อไปฝ่ายบัญชีบันทึกเข้าระบบ
ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
ข้อมูลผิด จะทำใบใหม่
ข้อมูลหลักคำขอ
ข้อมูลไม่ครบ ขอรายละเอียดเพิ่ม
ข้อมูลไม่ครบ ขอรายละเอียดเพิ่ม — ระบุหมวดบัญชีที่ต้องการให้ชัด
ข้าม
คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
คุณไม่มีสิทธิ์ทำรายการนี้
ค่าขนส่งซื้อ – ต่างประเทศ (เดิม)
ค่าซ่อมแซมและบำรุงรักษา – อาคาร
ค่านายหน้าขายต่างประเทศ
ค่าระวางเรือ (เดิม)
ค่าเช่าคลังสินค้าจ่ายล่วงหน้า
ค่าเริ่มต้นจากสายอนุมัติ (DOA) และผังองค์กร
ค่าใช้จ่ายเบ็ดเตล็ดอื่น (เดิม)
ค้นหา...
ค้นหาเลขที่ / ผู้ขอ / รหัสหรือชื่อบัญชี
จำนวนต่อหน้า
ชนิดไฟล์ไม่รองรับ
ชยพล รุ่งเรือง
ชื่อบัญชี
ชื่อบัญชีตามผังบัญชี
ชื่อบัญชีที่ต้องการขอเพิ่ม
ชื่อบัญชีเดิมไม่สื่อความหมาย
ชื่อฟังก์ชัน
ดอกเบี้ยค้างรับ – เงินฝากประจำ
ดอกเบี้ยรับ – เงินฝากประจำ 12 เดือน
ต.ค.
ตรวจสอบและยืนยัน
ตรวจสอบแล้ว
ตัดสระบน-วรรณยุกต์-สระล่าง
ตำแหน่ง
ตุลาคม
ต้นทุนบริการติดตั้ง
ต้อง
ถึง
ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
ทุกประเภทคำขอ
ทุกสถานะ
ธ.ค.
ธนพล วงศ์ดี
ธันวาคม
บริษัท ตัวอย่าง จำกัด
บัญชี
บันทึกร่างแล้ว ·
บันทึกส่วนลดตามสัญญาคู่ค้าที่ได้รับปลายปี
บันทึกเข้าระบบแล้ว
บันทึกเข้าระบบแล้ว ·
บันทึกเข้าระบบแล้ว?
บันทึกแล้ว
ประวัติ
ประวัติ (append-only)
ประเภทคำขอ
ปิด
ปิดบัญชีที่ไม่ใช้แล้ว
ปิยะนุช แก้วมณี
ผลการพิจารณา
ผู้ขอ
ผู้ขอเพิ่ม/แก้ไข/ยกเลิกรหัสบัญชี
ผู้จัดการทั่วไป
ผู้จัดการฝ่ายการเงิน
ผู้จัดการฝ่ายขาย
ผู้จัดการฝ่ายจัดซื้อ
ผู้จัดการฝ่ายบัญชี
ผู้ตรวจสอบ
ผู้บันทึกเข้าระบบ
ผู้ส่ง
ผู้อนุมัติ
ฝ่าย/แผนก
ฝ่ายการเงิน
ฝ่ายขาย
ฝ่ายจัดซื้อ
ฝ่ายบริหาร
ฝ่ายบัญชี
พ.ค.
พ.ย.
พฤ
พฤศจิกายน
พฤษภาคม
พิมพ์
ภาษีหัก ณ ที่จ่ายดอกเบี้ยรับ
ม.ค.
มกราคม
มานี รักษ์ทรัพย์
มิ.ย.
มิถุนายน
มี.ค.
มีนาคม
มีรหัสบัญชีที่ใช้แทนได้อยู่แล้ว
ยกเลิก
ยกเลิกรหัสบัญชี
ยกเลิกเอกสาร
ยกเลิกเอกสาร?
ยกเลิกเอกสารแล้ว ·
ยังมีรายการค้างในบัญชีนี้
ยังไม่ถึงขั้นนี้
ยังไม่ถึงขั้นบันทึกเข้าระบบ
ยังไม่มีข้อมูล
ยังไม่มีคำขอเพิ่ม-แก้ไข-ยกเลิก รหัสบัญชี
ยังไม่ส่ง
ยังไม่ได้เลือก
ยังไม่ได้ใส่ชื่อบัญชี
ย้อนกลับ
ย้ายไปใช้บัญชีต้นทุนนำเข้า
รวมเข้าบัญชีค่าขนส่งซื้อ
รหัส / ชื่อบัญชี
รหัสบัญชี
รหัสหรือชื่อบัญชีใหม่
รองรับตัวแทนขายต่างประเทศ
รองรับสัญญาเช่าคลังสินค้าแห่งใหม่
รอบันทึกเข้าระบบ
รอฝ่ายบัญชีบันทึกเข้าระบบ
รอพิจารณา
รออนุมัติ
ระบุตอนส่ง
รายการ
รายงานเคลื่อนไหวบัญชี 5390-09.pdf
รายละเอียด
รายได้ค่าขนส่งเรียกเก็บลูกค้า
รายได้ค่าบริการติดตั้ง
ร่าง
ลงนามผู้อนุมัติ
ลบไฟล์
ลองปรับคำค้นหรือล้างตัวกรอง
ลายเซ็น / อนุมัติ
ลำดับการอนุมัติ
ลูกหนี้เงินทดรองจ่ายพนักงาน
ล้างตัวกรอง
วรวุฒิ ทองดี
วัตถุประสงค์
วัตถุประสงค์ในการยกเลิก
วัตถุประสงค์ในการเพิ่ม
วัตถุประสงค์ในการแก้ไข
วันที่
วันที่ ........./........./.........
วันที่ขอ
ศศิธร มีสุข
ส.ค.
สถานะ
สถานะเอกสาร
สร้าง PDF
สร้างคำขอ
สร้างคำขอเมื่อต้องการเปลี่ยนผังบัญชี
สร้างเอกสาร
สร้างเอกสารใหม่
สร้างโดย
สลับเป็น
สำหรับผู้อนุมัติ
สิงหาคม
สุนันทา ใจงาม
ส่งกลับเป็นร่างแล้ว ·
ส่งต่อให้ขั้นถัดไปพิจารณา
ส่งอนุมัติ
ส่งอนุมัติแล้ว ·
ส่งออก
ส่งแล้วแก้ไขไม่ได้ — ถ้าผู้ตรวจสอบหรือผู้อนุมัติไม่อนุมัติ เอกสารจะกลับเป็นร่างให้แก้แล้วส่งใหม่
ส่งในระบบ
ส่วนลดการค้าค้างรับจากคู่ค้า
อนุมัติ
อนุมัติแล้ว · รอบันทึก
อนุมัติแล้ว · รอบันทึกเข้าระบบ
อรุณ แสงทอง
อา
เงินมัดจำค่าเช่าคลังสินค้า
เจ้าหน้าที่การเงิน
เจ้าหน้าที่ขาย
เจ้าหน้าที่จัดซื้อ
เจ้าหน้าที่บัญชี
เช่น 5210-01
เช่น 5390-09
เช่น ชื่อบัญชีเดิมไม่สื่อความหมาย
เช่น รายงานเคลื่อนไหวบัญชี หรือบันทึกที่มาของคำขอ
เช่น รายได้ค่าบริการติดตั้ง
เช่น แยกรายได้งานบริการออกจากการขายสินค้า
เช่น ไม่มีการใช้งานเกิน 12 เดือน
เดือนถัดไป
เด้งกลับบน
เปลี่ยนชื่อให้ตรงกับนโยบายค่าขนส่งใหม่
เปลี่ยนรหัส/ชื่อบัญชีที่มีอยู่
เพิ่มรหัสบัญชี
เพิ่มเติม
เม.ย.
เมษายน
เลขที่
เลขที่เอกสาร
เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
เลือกตอนส่ง
เลือกประเทศ
เลือกประเภทคำขอผิด
เลือกประเภทคำขอผิด — ใช้บัญชีค่านายหน้าเดิมได้
เลือกผู้พิจารณา
เลือกวันที่
เหตุผลที่ยกเลิก
เอกสาร
เอกสารแนบ
แก้ไข
แก้ไขคำขอ
แก้ไขรหัสบัญชี
แก้ไขร่าง
แก้ไขล่าสุด
แก้ไขเป็น
แก้ไขเอกสาร
แก้ไขได้เฉพาะร่างของตัวเอง
แจ้งผู้ขอว่าเพราะอะไร
แนบเอกสารประกอบ (ถ้ามี)
แนบไฟล์เพิ่ม
แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
แบบฟอร์มขอเพิ่ม-แก้ไข-ยกเลิก รหัสบัญชี
แบบเอกสารนี้ยังไม่เปิดใช้งาน
แยกค่าซ่อมอาคารออกจากค่าซ่อมเครื่องจักรเพื่อวิเคราะห์ต้นทุน
แยกดอกเบี้ยเงินฝากประจำออกจากออมทรัพย์
แยกรายได้และต้นทุนงานติดตั้งออกจากการขายสินค้า
ไม่ต้องการแล้ว
ไม่ผ่านการตรวจสอบ
ไม่พบรายการ
ไม่พบรายการที่ค้นหา
ไม่มีการใช้งานเกิน 12 เดือน รวมเข้าบัญชีค่าใช้จ่ายเบ็ดเตล็ด
ไม่ยกเลิก
ไม่อนุมัติ
— คุณเป็นผู้พิจารณาคำขอนี้
```

## §10 Data Binding & BACKEND anchors
| mock (prototype) | ระบบจริง (02_API) |
|---|---|
| `RECS` + `mkRec()` (seed 11 ใบ ชื่อสมมติ) | API-01/02 `/account-code-requests` |
| `EMP` · `empOf()` | HR · Employee / Organization (อ่าน) |
| `MOCK_DOA_RESOLVED` · `resolveDoa()` (marker DOA-ENGINE-HOOK) | API-05 doa-preview · GET /doa/resolve |
| `persist()` (SEQ + เลข ACR · ล้างส่วนที่ไม่ได้เลือก) | API-03/04 · ENG-DOC-NUM (FN-03) · FN-02 |
| `validateMain()` | FN-01 · VR-01..06 |
| `confirmSubmit()` | API-06 |
| `confirmApprove()` | API-07 approve |
| `confirmReason()` | API-07 reject / API-08 cancel |
| `confirmRecord()` | API-09 record |
| `docPrintData()` + `tplRender()` + `DOC_TPL` | API-10 PDF (server render template เดียวกัน) |
| `exportCSV()` | API-11 |
| `gateFiles()` | API-12 Document Center |
| `DOC.active` | F-DOCCFG status ACR |
| `commitRejected()` + `S.sim` | จำลอง 409/403/500 (prototype-only) |

## §11 Traceability + Drift Log
| Brief | FRD | HTML anchor |
|---|---|---|
| §4 P-01 | 01_UI P-01 · API-01/11 · FN-10 | `renderPage()` |
| §4 P-02 | 01_UI P-02 · API-03/04/12 · FN-01/02/03 · VR-01..06 | `renderWizard()` `wizMain()` `validateMain()` |
| §4 P-03 | 01_UI P-03 · API-02/05..10 · FN-04..08/11 | `renderViewDrawer()` |
| §6 modal ส่ง | API-06 · FN-04 · VR-07 | `renderModal()` (submit · `.slot-row`) |
| §6 modal ตรวจสอบ/อนุมัติ | API-07 · FN-05 | `confirmApprove()` |
| §6 modal ไม่อนุมัติ/ยกเลิก | API-07/08 · FN-06/07 · VR-08 | `confirmReason()` |
| §6 modal บันทึกเข้าระบบแล้ว | API-09 · FN-11 · BR-11 · VR-09 | `confirmRecord()` |
**Drift Log:** HTML-only (prototype-only ไม่ build): `window.__QA__` · `switchPersona()` · `S.sim` / `commitRejected()` · FRD-only: ไม่มี — ไม่มี business drift

## §12 Diff จากเวอร์ชันก่อน
— ไม่มี (เวอร์ชันแรก)

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- เลือกรหัสบัญชีจาก COA (combobox) แทนพิมพ์เอง เมื่อ feature COA พร้อม (OQ-04)
- แก้ COA อัตโนมัติเมื่ออนุมัติ (Phase 2)
