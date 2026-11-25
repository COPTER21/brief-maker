# UI_BRIEF — F-TMP-002 แบบฟอร์มยืมสินทรัพย์ (Asset Borrowing)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| HTML | `feature.html` · html-generator-v9.4 · archetype **Q-form** (`<meta name="cube-archetype" content="Q-form">`) · `window.__QA__` มี |
| FRD | FRD_F-TMP-002_Pack v1.0 (00–07 · frd_lint BLOCK 0) · BRD-ASM-ALN-001 APPROVED |
| DECISIONS | DECISIONS.lock 13 มติ (AI-DEFAULT 11 · VALID 2) |
| Gate | audit.sh FAIL 0 · self_audit PASS · e2e: [NO-BROWSER] → jsdom 32/32 (ต้องรัน e2e_standard.py บนเครื่องที่มี browser) |
| Drift | ดู §11 — ไม่มี business drift · prototype-only = `window.__QA__` · ตัวสลับผู้ใช้ (`switchPersona()`) · `S.sim` |
| Date | 2026-10-11 |

## §1 Design Tokens AS-BUILT
- ฟอนต์: Noto Sans Thai + Satoshi (Google Fonts / Fontshare) · แบบพิมพ์ใช้ Sarabun (ใน PDF_CSS)
- สี/ระยะ/รัศมี = CSS variables ของ kit CUBE Warm Light (ตารางเต็มท้ายหัวข้อนี้) · ห้ามเพิ่มเฉดใหม่ (U10)
- scrollbar: custom `::-webkit-scrollbar` + `scrollbar-width: thin` · `scrollbar-gutter: stable`
- Page-specific CSS ของ feature นี้: `.person-ic` (วงกลม icon คน mono) · `.ph-count.is-warn` / `.ph-count.is-danger` · `.cell-ellipsis` · `.cell-danger` · `.pg-size` · `.aln-items-view` · `.aln-items-edit` · `.bd-bad` · `.ss-bad` · `.alert-row.is-warning` · ตัวเลือกวัน `.bedate` / `.bd-pop`


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
| `#/asset-borrow` | P-01 รายการ (default ของ feature) | `applyRoute()` · `renderPage()` |
| `#/asset-borrow/view/:id` | P-03 drawer ดู (เปิดได้เฉพาะใบที่ `canSee()` · ไม่มีสิทธิ์ = ไม่เปิด) | `openView()` · `showDrawer()` |
| `#/asset-borrow/create` | P-02 สร้าง (ไม่มีทำซ้ำ · DEC-11) | `startWizard()` |
| `#/asset-borrow/edit/:id` | P-02 แก้ร่าง (เจ้าของ · draft) | `startWizard()` |
- refresh-safe: `hashchange` → `applyRoute()` · ปิด drawer → `go()` กลับ `#/asset-borrow`

## §3 Layout Shell
- `.sidebar` (module Asset Management › ยืมสินทรัพย์ · badge `#sbBadge` = จำนวนรอฉันพิจารณา) · `.shell-bar` breadcrumb Core › Asset Management › ยืมสินทรัพย์ · `.user-chip` + `#userMenu` (สลับผู้ใช้ — prototype-only) · avatar ผู้ใช้ = `.person-ic`
- เนื้อหา `#page-content` · drawer `#drawer` + `#drawerBackdrop` · modal `#modalBackdrop` > `#modal` · `#toast` · portal `#overlay-root`

## §4 Page Anatomy
### P-01 รายการ (`renderPage()`)
- `.ph` → `.ph-title` "แบบฟอร์มยืมสินทรัพย์" + `.ph-en` "(Asset Borrowing)" · `.ph-count` จำนวน · `.ph-count.is-warn` "รอฉันพิจารณา n" · `.ph-count.is-danger` "เลยกำหนดคืน n" (ค่า 0 ไม่แสดง · U22) · `.ph-sub` · `.ph-actions` [ส่งออก CSV `exportCSV()`] [สร้างคำขอยืม `#btnCreate` → `startWizard()`]
- ไม่มี stat card (U1)
- `.card.list-card` → `.filter-bar` (`#fq` ค้นหา · combobox `#ss-fst` สถานะ · `#ss-fdept` ฝ่าย · ล้างตัวกรอง `resetFilters()`) → `.table-wrap` > `table.table` คอลัมน์: เลขที่ · วันที่ขอ · ผู้ยืม · เพื่อใช้ (`.cell-ellipsis`) · รายการ · กำหนดคืน (`.cell-danger` เมื่อเลยกำหนด) · สถานะเอกสาร (`docPill()`) · ลายเซ็น (`renderSignProgress()`) · ⋮ `.ra-btn` → `openRowMenu()`
- `pager()` → `.table-footer` : `.pg-size` (10/25/50 · `setPageSize()`) · "x–y จาก N" · `.pagination`
- แถว `.is-clickable` → `rowClick()` → `openView()`
### P-02 สร้าง/แก้ (`renderWizard()` · drawer `.drawer-panel.wide`)
- หัว: eyebrow สร้างเอกสารใหม่/แก้ไขเอกสาร · `stepper()` 3 ขั้น `.d-stepper` (`STEPS`)
- ขั้น 1 `wizMain()` · `.wz-split` : `.wz-main` (การ์ด ① ยืมไปใช้ทำอะไร `#fPurpose` · การ์ด ② ยืมอะไรบ้าง `.aln-items-edit` ตาราง `itemRow()` : ทะเบียน combobox `#ss-ia{i}` · รายการ (ตามทะเบียน) · จำนวน `[name=iq-{i}]` · วันที่ยืม/ส่งคืน `bedateHTML()` via `dateCell()` · หมายเหตุ · ลบ `removeItem()` · `.add-row` เพิ่มรายการ `addItem()`) + `sumCard()` `.wz-sum`
- ขั้น 2 `wizAttach()` `.upload-zone` → `#alnFile` · `pickFiles()` / `removeFile()`
- ขั้น 3 `wizReview()` `.review-card` × 3 · ตาราง `itemsTable()`
- `.dw-footer` : ย้อนกลับ `wizBack()` · ยกเลิก `closeDrawer()` · ถัดไป `#btnNext` `wizNext()` / บันทึกแบบร่าง `#btnDraft` `saveDraft()` · บันทึกและส่งอนุมัติ `#btnSaveSubmit` `saveAndSubmit()` (loading `.spin` loader-2)
### P-03 ดู (`renderViewDrawer()` · drawer 920)
- `.dw-head` lean: `.dw-eyebrow` ชื่อเอกสาร · `.dw-title` เลขที่ + `docPill()` · `.dw-sub` "กำหนดคืน …" · `.dw-actions` ตามสถานะ (§8) + พิมพ์ `genPdf()` · ปิด
- `.drawer-tabs` `tabBtn()` : รายละเอียด `renderDetailTab()` · PDF Preview `renderPdfTab()` · ลายเซ็น / อนุมัติ `renderSignTab()` · ประวัติ `renderHistoryTab()`
- รายละเอียด: `viewBanner()` · `SEC()` ข้อมูลเอกสาร · ผู้ยืม · ขอยืมสินทรัพย์ เพื่อใช้ · รายการสินทรัพย์ `itemsTable()` · การรับคืน `returnBlock()` · เอกสารแนบ `fileRow()` · ข้อมูลระบบ
- PDF: `.pv-bar` + `.a4` > `.pdf-slot` > `iframe.pdf-frame[srcdoc]` (`docPdfDoc()` · `fitPdf()`)

## §5 Component Inventory
| Component | anchor | states |
|---|---|---|
| Search combobox | `searchSelectHTML()` / `initSearchSelect()` · `.search-select` · list portal `.ss-list` | default · focus/open · filtered · empty "ไม่พบ" · selected (clear ×) · error `.ss-bad` (แถวรายการ) |
| ตัวเลือกวัน พ.ศ. | `bedateHTML()` · `.bedate` · popover `#bd-pop` `.bd-pop` | default/placeholder "เลือกวันที่" · open · min (วันส่งคืน ≥ วันยืม · รับคืน ≤ วันนี้) · disabled day · error `.bd-bad` |
| ตารางรายการ (แก้ไข) | `.aln-items-edit` · `itemRow()` | ปกติ · แถวผิด `.is-bad-row` + `.row-err` `.trip-err` · 1 แถว = ไม่มีปุ่มลบ |
| ตารางรายการ (ดู) | `.aln-items-view` · `itemsTable()` | มีข้อมูล · ว่าง = `emptyStateHTML()` "ไม่มีข้อมูล" (U23) · จำนวนที่ให้ยืมว่าง = "—" |
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
| modal `#modal` (`.is-lg` สำหรับ ส่ง/ให้ยืม/รับคืน) | — | `openModalCfg()` | ปุ่ม · Esc · mousedown backdrop (`modalBackdropClick()` — มีเหตุผล/ความเห็นค้าง = **ไม่ปิด**) | `var(--z-modal)` |
| row-menu `.row-menu` | 180 | `openRowMenu()` | click ที่อื่น · scroll | `var(--z-popover)` |
| combobox list `.ss-list` | ความกว้างช่อง | focus/พิมพ์ | click ที่อื่น · Esc (ไม่ทะลุปิด drawer) | `var(--z-popover)` |
| ปฏิทิน `.bd-pop` | 280 | `bdToggle()` | click นอก · Esc (capture · ปิดแค่ปฏิทิน) | `var(--z-popover)` |
| user-menu `#userMenu` | — | `toggleUserMenu()` | click นอก | `var(--z-dropdown)` |
| toast `#toast` | — | `showToast()` | อัตโนมัติ 2.8 วินาที | `var(--z-toast)` |

## §7 Interaction Spec
- Esc chain (keydown ระดับ window): ปฏิทินเปิด → ปิดปฏิทินอย่างเดียว (capture + stopPropagation) · combobox เปิด → ปิด list · มี modal → `closeModal()` · มี drawer → `closeDrawer()` (wizard กรอกค้าง → modal "ทิ้งข้อมูลที่กรอกไว้?")
- backdrop: `onmousedown` + `event.target===this` เท่านั้น (U25)
- row click เปิด view ยกเว้นคลิกใน `.row-actions-cell`
- พิมพ์ "เพื่อใช้"/จำนวน/หมายเหตุ = soft update (`setPurpose()` · `setItem()` soft) ไม่ rebuild → focus ไม่หลุด
- เลือกวันที่ยืมหลังวันส่งคืน → วันส่งคืนเลื่อนตาม · เพิ่มรายการยกวันที่แถวก่อน + focus combobox แถวใหม่
- `render()` ใช้ `preserveRenderState()` / `restoreRenderState()` (scroll + focus) · `renderIcons()` หลังทุก render
- แก้ไขจาก view = ปิด view แล้วเปิด wizard (ไม่ซ้อน · U15)

## §8 State-Driven UI Matrix
| status | pill (`DOC_ST`) | ปุ่มหัว drawer | ⋮ |
|---|---|---|---|
| draft | ร่าง `pill-muted` | เจ้าของ: ยกเลิก · แก้ไข · ส่งอนุมัติ (`#btnSubmitView`) | แก้ไข · พิมพ์ · ยกเลิกเอกสาร |
| pending | รออนุมัติ `pill-warning` | ผู้พิจารณาขั้นปัจจุบัน: ไม่ให้ยืม · ให้ยืม (`#btnApproveView` `.btn-success`) · เจ้าของ/admin: ยกเลิกเอกสาร | พิมพ์ · ยกเลิกเอกสาร[สิทธิ์] |
| approved | ให้ยืมแล้ว `pill-success` | ผู้ให้ยืม/admin: บันทึกรับคืน (`#btnReturnView`) | พิมพ์ · บันทึกรับคืน[สิทธิ์] |
| returned | รับคืนแล้ว `pill-info` | — (ล็อก) | พิมพ์ |
| cancelled | ยกเลิก `pill-muted` | — | พิมพ์ |
- แบนเนอร์ (`viewBanner()`): ร่างที่ถูกส่งกลับ `.alert-row.is-danger` · รอ · เลยกำหนดคืน `.alert-row.is-warning` · ให้ยืมแล้ว `.alert-row.is-success` · ยกเลิก
- คำตัดสินตาม role: `wordsOf()` จาก `DECISION_WORDS` (role-mgr-acc = ให้ยืม/ไม่ให้ยืม)


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
| warning | จำนวนที่ให้ยืมไม่ถูกต้อง |
| info | บันทึกรับคืนแล้ว · |
| info | ส่งออก |
| info | สลับเป็น |
| error | แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง |
### ปุ่ม / label / placeholder / empty (ตรงจอ)
สร้างคำขอยืม · ส่งออก CSV · ล้างตัวกรอง · ส่งอนุมัติ · บันทึกแบบร่าง · บันทึกและส่งอนุมัติ · ถัดไป · ย้อนกลับ · ยกเลิก · ยกเลิกเอกสาร · ให้ยืม · ไม่ให้ยืม · บันทึกรับคืน · ทิ้งข้อมูล · กลับไปกรอกต่อ · เพิ่มรายการ · พิมพ์ · ดาวน์โหลด PDF
placeholder: ค้นหาเลขที่ / ผู้ยืม / สินทรัพย์ · เช่น จัดอบรมสินค้าให้ลูกค้า ณ ห้องประชุมสาขา · ไม่บังคับ · — · aria: จำนวนต่อหน้า · จำนวนที่ยืม · จำนวนที่ให้ยืม · หมายเหตุ · เดือนก่อน · เดือนถัดไป
### Microcopy inventory (สกัดจาก HTML · verbatim)
```
(ขั้น
[Lucide] All CDNs failed. Icons จะไม่แสดง but UI ยังใช้งานได้
]); if (canCancel(r)) items.push(['x-circle', 'ยกเลิกเอกสาร',
]); if (canReturn(r)) items.push(['package-check', 'บันทึกรับคืน',
]]; /* DEC-11 ทำซ้ำ ✗ */ if (isOwner(r) && r.status === 'draft') items.unshift(['pencil', 'แก้ไข',
showToast('ไม่มีการแจ้งเตือนใหม่','info')
· อนุมัติแล้ว ล็อกแก้ไข
ก.ค.
ก.พ.
ก.ย.
กรกฎาคม
กรอกให้ครบ:
กรุณากรอกข้อมูลให้ครบถ้วน
กล้องถ่ายภาพดิจิทัล
กันยายน
กำลังเปิดหน้าต่างพิมพ์ ·
กำหนดการอบรมลูกค้า.pdf
กำหนดคืน
กิตติ ศรีสุข
กุมภาพันธ์
ขั้นทดสอบ
ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
ข้อมูลหลักการยืม
ข้อมูลไม่ครบ ขอรายละเอียดเพิ่ม
ข้าพเจ้า
ข้าม
คงเหลือ 15 ตัว
คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
คุณไม่มีสิทธิ์ทำรายการนี้
ค่าเริ่มต้นจากสายอนุมัติ (DOA) และผังองค์กร
ค้นหา...
ค้นหาทะเบียน / ชื่อ
ค้นหาเลขที่ / ผู้ยืม / สินทรัพย์
งานออกบูธแสดงสินค้า
จัดอบรมสินค้าให้ลูกค้า ณ ห้องประชุมสาขา
จำนวนต่อหน้า
จำนวนที่ยืม
จำนวนที่ให้ยืม
จำนวนที่ให้ยืมต้องอยู่ระหว่าง 1 ถึงจำนวนที่ยืม
จำนวนที่ให้ยืมไม่ถูกต้อง
ชนิดไฟล์ไม่รองรับ
ชิ้น
ชื่อฟังก์ชัน
ช่วงที่ยืม
ซ่อมบำรุงตามรอบที่โรงงานลูกค้า
ต.ค.
ตรวจรับงานติดตั้ง
ตรวจสอบและยืนยัน
ตัดสระบน-วรรณยุกต์-สระล่าง
ตามทะเบียน
ตำแหน่ง
ตุลาคม
ต้อง
ถึง
ถ่ายภาพสินค้าทำสื่อโฆษณา
ถ่ายวิดีโอรีวิวสินค้า
ทะเบียนสินทรัพย์
ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
ทุกฝ่าย
ทุกสถานะ
ธ.ค.
ธนพล วงศ์ดี
ธันวาคม
นำเสนอสินค้าที่สำนักงานลูกค้า
บริษัท ตัวอย่าง จำกัด
บอกว่ายืมไปใช้ทำอะไร แล้วเลือกสินทรัพย์จากทะเบียน พร้อมวันที่ยืมและวันที่ส่งคืน
บันทึกผลขั้น
บันทึกผิด
บันทึกรับคืน
บันทึกรับคืนแล้ว ·
บันทึกร่างแล้ว ·
ประชุมเชิงปฏิบัติการทีมขาย
ประวัติ
ประวัติ (append-only)
ปิด
ปิยะนุช แก้วมณี
ผู้จัดการทั่วไป
ผู้จัดการฝ่ายขาย
ผู้จัดการฝ่ายบัญชี
ผู้ยืม
ผู้รับคืน
ผู้ส่ง
ผู้ส่งคืน
ผู้ให้ยืม
ฝ่าย/แผนก
ฝ่ายการตลาด
ฝ่ายขาย
ฝ่ายบริหาร
ฝ่ายบริหารสินทรัพย์
ฝ่ายบัญชี
ฝ่ายผลิต
พ.ค.
พ.ย.
พร้อมกระเป๋า
พร้อมสาย HDMI
พฤ
พฤศจิกายน
พฤษภาคม
พิมพ์
ม.ค.
มกราคม
มานี รักษ์ทรัพย์
มิ.ย.
มิถุนายน
มี.ค.
มีนาคม
ยกเลิก
ยกเลิกเอกสาร
ยกเลิกเอกสาร?
ยกเลิกเอกสารแล้ว ·
ยังเป็นร่าง — ส่งอนุมัติเมื่อข้อมูลครบ
ยังไม่ถึงขั้นนี้
ยังไม่ถึงขั้นรับคืน
ยังไม่มีข้อมูล
ยังไม่มีรายการสินทรัพย์
ยังไม่มีแบบฟอร์มยืมสินทรัพย์
ยังไม่ส่ง
ยังไม่ได้รับคืน
ยังไม่ได้เลือกสินทรัพย์
ย้อนกลับ
รวมจำนวนที่ยืม
รอพิจารณา
รออนุมัติ
ระบุตอนส่ง
ระยะเวลายืมนานเกินไป
รับคืนแล้ว
รายการ
รายการ · รวม
รายละเอียด
ร่าง
ลบไฟล์
ลองปรับคำค้นหรือล้างตัวกรอง
ลายเซ็น / อนุมัติ
ลำดับ
ลำดับการอนุมัติ
ลำโพงพกพาพร้อมไมโครโฟน
ล้างตัวกรอง
วรวุฒิ ทองดี
วันที่ ........./........./.........
วันที่ขอ
วันที่ยืม
วันที่รับคืน
วันที่ส่งคืน
วันที่ส่งคืนต้องไม่ก่อนวันที่ยืม
วิศวกรภาคสนาม
ศศิธร มีสุข
ส.ค.
สถานะ
สถานะเอกสาร
สร้าง PDF
สร้างคำขอยืม
สร้างคำขอยืมก่อนนำสินทรัพย์ออกไปใช้งาน
สร้างเอกสาร
สร้างเอกสารใหม่
สร้างโดย
สลับเป็น
สว่านไฟฟ้าไร้สาย
สัมมนาลูกค้ารายใหญ่
สำรวจพื้นที่ติดตั้งเครื่องจักรที่โรงงานลูกค้า
สิงหาคม
สินทรัพย์ไม่ว่างในช่วงวันที่ขอ
สุนันทา ใจงาม
ส่งกลับเป็นร่างแล้ว ·
ส่งอนุมัติ
ส่งอนุมัติแล้ว ·
ส่งออก
ส่งแล้วแก้ไขไม่ได้ — ถ้าผู้ให้ยืมไม่อนุมัติ เอกสารจะกลับเป็นร่างให้แก้แล้วส่งใหม่
ส่งในระบบ
หมายเหตุ
อนุมัติ
อนุมัติให้ยืม
อา
เก้าอี้พับ
เครื่องคอมพิวเตอร์โน้ตบุ๊ก
เครื่องฉายภาพโปรเจกเตอร์
เครื่องมือ
เครื่องวัดระยะเลเซอร์
เจ้าหน้าที่การตลาด
เจ้าหน้าที่ขาย
เจ้าหน้าที่บริหารสินทรัพย์
เดือนถัดไป
เด้งกลับบน
เปลี่ยนวันที่ใช้งาน
เปลี่ยนวันที่ใช้งาน — เลื่อนถ่ายทำ
เพิ่มเติม
เพื่อใช้
เฟอร์นิเจอร์
เม.ย.
เมษายน
เลขที่
เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
เลือกตอนส่ง
เลือกประเทศ
เลือกผู้พิจารณา
เลือกวันที่
เหตุผลที่ยกเลิก
เอกสาร
เอกสารแนบ
แก้ไข
แก้ไขคำขอ
แก้ไขร่าง
แก้ไขล่าสุด
แก้ไขเอกสาร
แก้ไขได้เฉพาะร่างของตัวเอง
แจ้งผู้ยืมว่าเพราะอะไร
แท็บเล็ต
แนบไฟล์เพิ่ม
แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
แบบฟอร์มยืมสินทรัพย์
แบบเอกสารนี้ยังไม่เปิดใช้งาน
แล้ว
โต๊ะพับอเนกประสงค์
ใช้สาธิตระบบให้ลูกค้าหน้างาน
ให้ยืม
ให้ยืมแล้ว
ไม่ต้องใช้สินทรัพย์แล้ว
ไม่พบรายการ
ไม่พบรายการที่ค้นหา
ไม่มีข้อมูล
ไม่ยกเลิก
ไม่อนุมัติ
ไม่อนุมัติ · กลับเป็นร่าง
ไม่ให้ยืม
ไอที
```

## §10 Data Binding & BACKEND anchors
| mock (prototype) | ระบบจริง (02_API) |
|---|---|
| `RECS` + `mkRec()` (seed 11 ใบ ชื่อสมมติ) | API-01/02 `/asset-borrows` |
| `EMP` · `empOf()` | HR · Employee / Organization (อ่าน) |
| `ASSETS` · `assetOf()` | API-13 Asset Master `/assets?q` |
| `MOCK_DOA_RESOLVED` · `resolveDoa()` (marker DOA-ENGINE-HOOK) | API-05 doa-preview · GET /doa/resolve |
| `persist()` (SEQ + เลข ALN) | API-03/04 · ENG-DOC-NUM (FN-03) |
| `confirmSubmit()` | API-06 |
| `confirmApprove()` (`setLent()`) | API-07 approve + qty_lent[] |
| `confirmReason()` | API-07 reject / API-08 cancel |
| `confirmReturn()` | API-09 return |
| `docPrintData()` + `tplRender()` + `DOC_TPL` | API-10 PDF (server render template เดียวกัน) |
| `exportCSV()` | API-11 |
| `gateFiles()` | API-12 Document Center |
| `DOC.active` | F-DOCCFG status ALN |
| `commitRejected()` + `S.sim` | จำลอง 409/403/500 (prototype-only) |

## §11 Traceability + Drift Log
| Brief | FRD | HTML anchor |
|---|---|---|
| §4 P-01 | 01_UI P-01 · API-01/11 · FN-10 | `renderPage()` |
| §4 P-02 | 01_UI P-02 · API-03/04/12/13 · FN-01/02/03 · VR-01..04 | `renderWizard()` `wizMain()` `validateMain()` |
| §4 P-03 | 01_UI P-03 · API-02/05..10 · FN-04..08/11 | `renderViewDrawer()` |
| §6 modal ส่ง | API-06 · FN-04 · VR-06 | `renderModal()` (submit · `.slot-row`) |
| §6 modal ให้ยืม | API-07 · FN-05 · BR-02 · VR-05 | `lentTable()` `confirmApprove()` |
| §6 modal ไม่ให้ยืม/ยกเลิก | API-07/08 · FN-06/07 · VR-07 | `confirmReason()` |
| §6 modal รับคืน | API-09 · FN-11 · BR-13 · VR-08 | `confirmReturn()` |
| §8 เลยกำหนดคืน | BR-05 · FN-09/10 · EC-09 | `isOverdue()` |
**Drift Log:** HTML-only (prototype-only ไม่ build): `window.__QA__` · `switchPersona()` · `S.sim` / `commitRejected()` · FRD-only: งานรายวัน aln_overdue (scheduler · ไม่มีใน prototype) · API-13 Asset Master (mock `ASSETS`) — ไม่มี business drift

## §12 Diff จากเวอร์ชันก่อน
— ไม่มี (เวอร์ชันแรก)

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- แสดงสถานะว่าง/ถูกยืมของสินทรัพย์ใน combobox ทะเบียน (รอ OQ-05)
- รับคืนบางส่วน/หลายครั้ง (Phase 2)
