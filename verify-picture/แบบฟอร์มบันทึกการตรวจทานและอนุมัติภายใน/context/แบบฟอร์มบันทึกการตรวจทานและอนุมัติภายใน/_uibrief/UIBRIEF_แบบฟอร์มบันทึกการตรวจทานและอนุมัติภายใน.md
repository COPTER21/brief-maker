# UI_BRIEF — F-TMP-006 แบบฟอร์มบันทึกการตรวจทานและอนุมัติภายใน (AS-BUILT)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| HTML (source of truth) | `feature.html` · html-generator-v9.4 · archetype `Q-form` (`<meta name="cube-archetype">`) · audit FAIL 0 · e2e 21/21 (verify บน cloud container — เครื่อง user NO-BROWSER) |
| FRD | FRD_F-TMP-006_Pack v1.0 (FULL) · DECISIONS.lock 18 มติ (DEC-01..18 · AI-DEFAULT 12) |
| Prototype-only | `window.__QA__` · ตัวสลับผู้ใช้ `switchPersona()` · `S.sim` / `commitRejected()` · `EMP`/`RECS` mock → ไม่ต้องสร้างในระบบจริง (Drift Log D-01) |
| Drift | 0 business drift · 2 prototype-only (§11) |

## §1 Design Tokens AS-BUILT
CI Warm Light (html-generator-v9) · font Satoshi + Noto Sans Thai (หน้าจอ) · Sarabun (PDF) · สถานะข้อแก้ไข: pill `pill-warning` (เปิด) · `pill-info` (กำลังดำเนินการ) · `pill-success` (ปิด) · สถานะการอนุมัติ: `pill-success/pill-info/pill-warning/pill-danger`
| Variable | Value |
|---|---|
| `--c-navy` | `#111111` |
| `--c-navy-2` | `#111111` |
| `--c-primary` | `#FF3B30` |
| `--c-primary-hover` | `#E62E24` |
| `--c-teal` | `#FF9A1F` |
| `--c-teal-light` | `#FFB763` |
| `--c-ink` | `#111111` |
| `--c-mute` | `#54565C` |
| `--c-mute-2` | `#73757B` |
| `--c-mute-3` | `#9A9CA2` |
| `--c-placeholder` | `rgb(180,182,188)` |
| `--z-content` | `1` |
| `--z-sticky` | `10` |
| `--z-shell` | `10` |
| `--z-dropdown` | `30` |
| `--z-backdrop` | `50` |
| `--z-drawer` | `51` |
| `--z-modal` | `60` |
| `--z-popover` | `70` |
| `--z-toast` | `80` |
| `--c-line` | `#DEDAD4` |
| `--c-line-2` | `#E9E5E0` |
| `--c-line-3` | `#F1EEEA` |
| `--c-bg-off` | `#FAF8F5` |
| `--c-success` | `#1F9D55` |
| `--c-warning` | `#E8870F` |
| `--c-danger` | `#E62E24` |
| `--sidebar-w` | `232px` |
| `--shell-h` | `52px` |
| `--fs-h1` | `22px` |
| `--fs-h2` | `17px` |
| `--fs-h3` | `15px` |
| `--fs-body` | `14px` |
| `--fs-sub` | `13px` |
| `--fs-meta` | `12px` |
| `--fs-cap` | `11px` |
| `--fs-kpi` | `28px` |
| `--sp-xs` | `4px` |
| `--sp-sm` | `8px` |
| `--sp-md` | `12px` |
| `--sp-lg` | `20px` |
| `--sp-xl` | `28px` |
| `--r-xs` | `4px` |
| `--r-sm` | `6px` |
| `--r-md` | `8px` |
| `--r-lg` | `12px` |
| `--r-full` | `999px` |

### z-index map
| selector | z |
|---|---|
| `.sidebar` | `var(--z-shell)` |
| `.shell-bar` | `var(--z-sticky)` |
| `.user-menu` | `var(--z-dropdown)` |
| `.table-wrap thead th` | `var(--z-sticky)` |
| `* เมนูที่ portal ออกจาก scroll container (ใช้คู่ portalMenu util) */ .menu-fixed` | `var(--z-popover)` |
| `.ss-list` | `var(--z-backdrop)` |
| `verlay-root ตอนเปิด (หลุด overflow ของ modal/drawer body) */ .ss-list.menu-fixed` | `var(--z-popover)` |
| `.table-scroll.is-sticky thead th` | `3` |
| `.stepper-circle` | `2` |
| `.stepper-item:not(:last-child)::after` | `1` |
| `.drawer-backdrop` | `var(--z-backdrop)` |
| `.drawer` | `var(--z-drawer)` |
| `รมีปุ่ม action หลัก */  .modal-backdrop` | `var(--z-backdrop)` |
| `.toast` | `var(--z-toast)` |
| `.wizard-footer` | `var(--z-sticky)` |
| `.info-tip::after` | `var(--z-dropdown)` |
| `.modal-backdrop` | `var(--z-modal)` |
| `#drawer` | `var(--z-drawer)` |
| `#drawerBackdrop` | `var(--z-backdrop)` |
| `#toast` | `var(--z-toast)` |
| `.row-menu` | `var(--z-popover)` |
| `.bd-pop` | `var(--z-popover)` |
ค่าที่ใช้: `1`, `2`, `3`, `var(--z-backdrop)`, `var(--z-drawer)`, `var(--z-dropdown)`, `var(--z-modal)`, `var(--z-popover)`, `var(--z-shell)`, `var(--z-sticky)`, `var(--z-toast)`

## §2 Route Map
| Route | หน้า | handler |
|---|---|---|
| `#/internal-review` | P-01 รายการ (default) | `applyRoute()` · `renderPage()` |
| `#/internal-review/create` | P-02 สร้าง | `startWizard()` |
| `#/internal-review/edit/:id` | P-02 แก้ร่าง (เจ้าของ · draft) | `startWizard()` |
| `#/internal-review/view/:id` | P-03 ดู (เฉพาะ `canSee`) | `openView()` · `showDrawer()` |
refresh-safe ผ่าน `hashchange` → `applyRoute()` · route ใบไม่มีสิทธิ์ = ไม่เปิด drawer

## §3 Layout Shell
`.sidebar` โมดูล Business Development › ตรวจทานและอนุมัติภายใน + badge `#sbBadge` (= รอฉันพิจารณา) · `.shell-bar` breadcrumb Core › Business Development › ตรวจทานและอนุมัติภายใน · user chip (icon คน · `toggleUserMenu()`) + `.user-menu` สลับผู้ใช้ (prototype) · `#page-content`

## §4 Page Anatomy
### P-01 รายการ — `renderPage()`
`.ph` (ชื่อ + `.ph-en` + `.ph-badge` ×≤3: รายการ · เปิดอยู่ · รอฉันพิจารณา — ค่า 0 ไม่แสดง · ไม่มี stat cards U1) · ปุ่ม `exportCSV()` / `#btnCreate` → `startWizard()` · `.filter-bar` (`#fq` `onQ()` · search select `fst` `ffin` `fdept` ผ่าน `initSearchSelect()` · รีเซ็ต `resetFilters()`) · `.table-wrap .table` คอลัมน์ เลขที่ · วันที่ · ผู้จัดทำ (`personInline()`) · ฝ่าย · รายการตรวจทาน · ข้อแก้ไขค้าง (`openItems()` · `.is-warn-t`) · สถานะการอนุมัติ `fnPill()` · สถานะเอกสาร `docPill()` · ลายเซ็น `renderSignProgress()` · ⋮ `openRowMenu()` · `pager()` + `setSize()` (10/25/50 · ค่าเริ่ม 25) `goPage()`
### P-02 สร้าง/แก้ — `renderWizard()` (drawer `.drawer.wide`)
`stepper()` 3 ขั้น (`STEPS`) · ขั้น 1 `wizMain()`: `sumStrip()` (`#sumCnt` `#sumOpen` + legend สถานะ) · `.rv-tbl` แถว `reviewRow()` ช่อง `[name=vi-i]` รายการเอกสาร / ประเด็น · `[name=vr-i]` ผู้ตรวจทาน (`#dlEmp`) · `.bedate` (key `vd{i}`) วันที่ตรวจทาน (`bedateHTML()`) · `[name=vs-i]` ผลการตรวจทาน (`#dlResult`) · `[name=vc-i]` ข้อคิดเห็น / ข้อแก้ไข · `[name=vo-i]` ผู้รับผิดชอบแก้ไข · `[name=vt-i]` สถานะ · ลบ `removeRv()` · `.add-row` `addRv()` · `#rvWarn` เตือนปิดแล้วไม่มีผู้รับผิดชอบ · อัปเดตสด `setRv()` → `softSums()` · ขั้น 2 `wizApproval()`: `.ap-tbl` แถว `apRow()` (`[name=an-i]` `[name=ap-i]` `[name=ad-i]` `.bedate` (key `at{i}`) `[name=ae-i]` · `addAp()` · `removeAp()`) · สถานะสุดท้าย `.fin-grid` (`[name=fst]` · `.bedate` (key `feff`) · `[name=fremark]` · `setFin()` · `#finWarn`) · `wizAttach()` `.upload-zone` `pickFiles()` · ขั้น 3 `wizReview()` (`reviewTable()` · `approvalTable()` · `finalBlock()`) · footer `wizBack()` `wizNext()` `saveDraft()` `saveAndSubmit()`
### P-03 ดู — `renderViewDrawer()`
หัว `.dw-head` (เลขที่ · `docPill()` · sub ≤2 fact: ตรวจทาน n · ข้อแก้ไขค้าง n) · ปุ่ม `#btnSubmitView` `openSubmit()` / `#btnApproveView` `openApprove()` / `openReject()` / `openCancel()` · `.drawer-tabs` `tabBtn()` → `renderDetailTab()` (`reviewTable()` · `approvalTable()` · `finalBlock()`) · `renderPdfTab()` (`.pdf-slot` iframe `.pdf-frame` srcdoc `docPdfDoc()` · `fitPdf()` · `genPdf()`) · `renderSignTab()` · `renderHistoryTab()`

## §5 Component Inventory
| Component | anchor | states |
|---|---|---|
| ตารางตรวจทาน (แก้) | `.rv-tbl` `reviewRow()` | default · `.is-bad` ต่อช่อง · `.is-warn` (ปิดแล้วไม่มีผู้รับผิดชอบ/ข้อคิดเห็น) · ลบ (เมื่อ >1 แถว) |
| ตารางอนุมัติภายใน (แก้) | `.ap-tbl` `apRow()` | ว่าง = แผง "ไม่มีข้อมูล" · `.is-bad` · แถว auto (DOA) ไม่มีปุ่มลบ |
| ตัวเลือกวัน พ.ศ. | `bedateHTML()` `.bedate` `.bd-pop` (portal) | ว่าง · เลือกแล้ว · `.bd-wrap.is-bad` · disabled (วันที่มีผลเมื่อสถานะไม่ต้องใช้) |
| สถานะสุดท้าย | `.fin-grid` `finalBlock()` | `.field.is-invalid` · เตือน `#finWarn` / alert ในรายละเอียด |
| แถบสรุปสด | `.rk-strip.rv-strip` `sumStrip()` | อัปเดตแบบ soft (focus ไม่หลุด) |
| ตารางตรวจทาน/อนุมัติ (อ่าน) | `reviewTable()` `approvalTable()` `.rk-view` | ว่าง = แผง "ไม่มีข้อมูล" (U23) |
| คน | `empChip()` `personInline()` `nameInline()` `.emp-av` | วงกลมพื้นดำ + icon คน (U17) |
| progress ลายเซ็น | `renderSignProgress()` `.sign-prog` | ร่าง = — · n/N |
| slot ผู้พิจารณา | `.slot-row` + search select `slot{i}` | ค่าเริ่ม · `.is-invalid` |
| ปุ่ม busy | `busyLabel()` | loading "กำลังบันทึก…" · disabled |

## §6 Overlay Registry
| Overlay | anchor | ขนาด | ปิดด้วย |
|---|---|---|---|
| drawer สร้าง/แก้ | `#drawer` `.drawer-panel.wide` + `#drawerBackdrop` | wide | ปุ่ม/Esc/backdrop (`onmousedown` U25) · **กรอกค้าง → modal ทิ้งข้อมูล** (`closeDrawer()` dirty) |
| drawer ดู | `#drawer` `.drawer-panel` | 920 | ปุ่ม ปิด/Esc/backdrop |
| modal ส่ง/อนุมัติ | `#modal` `.modal.is-lg` | lg | ยกเลิก · Esc · backdrop mousedown (`modalBackdropClick()` — มีข้อความค้างห้ามปิด) |
| modal ไม่ผ่าน/ยกเลิก/ทิ้ง | `#modal` | md | เช่นเดียวกัน |
| ปฏิทิน พ.ศ. | `.bd-pop` (portal `#overlay-root`) | 280px | เลือกวัน · คลิกนอก · Esc (ปิดแค่ปฏิทิน) |
| เมนู ⋮ | `.row-menu` (portal) | 180px | คลิกนอก · scroll |
| search list | `.ss-list.menu-fixed` | | Esc · คลิกนอก |
| toast | `#toast` `.toast` | | อัตโนมัติ |
| user menu | `.user-menu` | | คลิกนอก |

## §7 Interaction Spec
Esc chain: ปฏิทินเปิด → ปิดปฏิทินก่อน (capture · stopPropagation) → search list → modal → `closeModal()` → drawer → `closeDrawer()` · backdrop ปิดด้วย mousedown เท่านั้น · `addRv()` focus ช่องรายการของแถวใหม่ · `addAp()` focus ช่องผู้พิจารณา · เลือกสถานะ → จำนวนข้อแก้ไขค้างอัปเดตทันที · เปลี่ยนสถานะการอนุมัติ → วันที่มีผล enable/disable + ล้างค่า (`setFin()`) · ผลพิจารณา DOA เติมแถวอนุมัติภายใน (`apRowOf()`)

## §8 State-Driven UI Matrix
| status | pill | ปุ่มหัว (ผู้มีสิทธิ์) |
|---|---|---|
| draft | ร่าง `pill-muted` | เจ้าของ: ยกเลิก · แก้ไข · ส่งอนุมัติ |
| pending | รออนุมัติ `pill-warning` | ผู้พิจารณาขั้นปัจจุบัน: คำปฏิเสธของขั้น · คำอนุมัติของขั้น · อื่น (เจ้าของ/admin): ยกเลิกเอกสาร |
| approved | อนุมัติแล้ว `pill-success` | — (ล็อก) |
| cancelled | ยกเลิก `pill-muted` | — |
สถานะการอนุมัติ (ReviewApprovalConfig.final_statuses): อนุมัติครบถ้วน `pill-success` · อนุมัติแบบมีเงื่อนไข `pill-info` · อยู่ระหว่างแก้ไข `pill-warning` · ไม่อนุมัติ `pill-danger`
คำตัดสินผูก role (`DECISION_WORDS` → `wordsOf()`): role-line-manager = ตรวจสอบแล้ว/ไม่ผ่านการตรวจสอบ · role-gm = อนุมัติ / รับทราบ/ไม่อนุมัติ · อื่น = อนุมัติ/ไม่อนุมัติ · จำนวน/ลำดับขั้นมาจาก DOA

## §9 Microcopy (verbatim)
### toast
- `ไม่มีการแจ้งเตือนใหม่`
- `แบบเอกสารนี้ยังไม่เปิดใช้งาน`
- `แก้ไขได้เฉพาะร่างของตัวเอง`
- `กรุณากรอกข้อมูลให้ครบถ้วน`
- `บันทึกร่างแล้ว ·`
- `ส่งอนุมัติแล้ว ·`
- `ส่งออก`
- `สลับเป็น`
- `แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง`
- ประกอบ: `กลับเป็นร่างแล้ว · {เลขที่}` · `ยกเลิกเอกสารแล้ว · {เลขที่}` · `อนุมัติ / รับทราบเรียบร้อย · {เลขที่}` · `ส่งต่อขั้นถัดไปแล้ว · {เลขที่}` · `บันทึกร่างแล้ว · {เลขที่}` · `… · แจ้งผู้จัดทำ: ข้อแก้ไขค้าง {n} รายการ`
### ปุ่ม / placeholder / label
`Business Development` · `กลับไปกรอกต่อ` · `ดาวน์โหลด PDF` · `ถัดไป` · `ทิ้งข้อมูล` · `บันทึกแบบร่าง` · `ปิด` · `พิมพ์` · `ยกเลิก` · `ยกเลิกเอกสาร` · `ย้อนกลับ` · `รีเซ็ต` · `วันนี้` · `สร้างบันทึก` · `ส่งอนุมัติ` · `ส่งออก CSV` · `เพิ่มผู้พิจารณานอกระบบ` · `เพิ่มรายการตรวจทาน` · `แก้ไข` · `ใช้เมื่ออนุมัติครบถ้วน / แบบมีเงื่อนไข`

`ข้อคิดเห็น / ข้อแก้ไข` · `ค้นหาเลขที่ / ผู้จัดทำ / รายการเอกสาร` · `ชื่อผู้ตรวจทาน` · `ชื่อผู้พิจารณา` · `ตำแหน่ง` · `ผลการตรวจทาน` · `ผลการพิจารณา` · `ผู้รับผิดชอบ` · `เช่น อีเมล / บันทึกประชุม` · `เอกสาร / ประเด็นที่ตรวจทาน` · `ไม่บังคับ` · `ไม่บังคับ — บันทึกลงผลการพิจารณา` · aria: `ข้อคิดเห็น / ข้อแก้ไข` · `ตำแหน่ง` · `ผลการตรวจทาน` · `ผลการพิจารณา` · `ผู้ตรวจทาน` · `ผู้พิจารณา / ผู้อนุมัติ` · `ผู้รับผิดชอบแก้ไข` · `รายการเอกสาร / ประเด็น` · `ลายมือชื่อ / หลักฐาน` · `สถานะ` · `สถานะการอนุมัติ` · `เดือนก่อน` · `เดือนถัดไป` · `แสดงต่อหน้า`
### ข้อความอื่น (จากโค้ด)
- (ขั้น
- [Lucide] All CDNs failed. Icons จะไม่แสดง but UI ยังใช้งานได้
- ]); if (canCancel(r)) items.push(['x-circle', 'ยกเลิกเอกสาร',
- ]]; if (isOwner(r) && r.status === 'draft') items.unshift(['pencil', 'แก้ไข',
- showToast('ไม่มีการแจ้งเตือนใหม่','info')
- · อนุมัติแล้ว ล็อกแก้ไข
- · แจ้งผู้จัดทำ: ข้อแก้ไขค้าง
- ก.ค.
- ก.พ.
- ก.ย.
- กรกฎาคม
- กรรมการผู้จัดการ
- กรอกผู้พิจารณา ตำแหน่ง ผลการพิจารณา และวันที่ให้ครบทุกแถว (หรือลบแถวที่ไม่ใช้)
- กรอกรายการเอกสาร ผู้ตรวจทาน วันที่ ผลการตรวจทาน และสถานะให้ครบทุกรายการ
- กรุณากรอกข้อมูลให้ครบถ้วน
- กลับเป็นร่างแล้ว ·
- กันยายน
- กำลังดำเนินการ
- กำลังเปิดหน้าต่างพิมพ์ ·
- กิตติพัฒน์ ทดลองงาน
- กุมภาพันธ์
- ขั้นตอนที่ 5: จัดทำเอกสารเสนอผู้บริหาร
- ขั้นทดสอบ
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อแก้ไขค้าง
- ข้อแก้ไขยังไม่ปิดครบ
- ข้อแก้ไขยังไม่ปิดครบ — ทบทวนแผนการดำเนินงานก่อนเสนอ
- ข้าม
- คน
- คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค่าเริ่มต้นจากสายอนุมัติและผังองค์กร
- ค้นหา...
- ค้นหาเลขที่ / ผู้จัดทำ / รายการเอกสาร
- จัดทำครั้งแรก
- ชนิดไฟล์ไม่รองรับ
- ชยพล ตั้งระบบ
- ชื่อ
- ชื่อผู้ตรวจทาน
- ชื่อผู้พิจารณา
- ชื่อฟังก์ชัน
- ดาวน์โหลด PDF
- ต.ค.
- ตรวจสอบและยืนยัน
- ตรวจสอบแล้ว
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตารางเปรียบเทียบทางเลือก
- ตำแหน่ง
- ตุลาคม
- ต้อง
- ต้องแนบสัญญาฉบับลงนามก่อนเบิกจ่ายงวดแรก
- ถึง
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ทุกฝ่าย
- ทุกสถานะการอนุมัติ
- ทุกสถานะเอกสาร
- ธ.ค.
- ธันวาคม
- ธีรพงษ์ สมมติชื่อ
- นภัสสร ตัวอย่างดี
- นักวิเคราะห์การลงทุน
- บทสรุปผู้บริหาร (ร่าง 1)
- บทสรุปผู้บริหาร_ฉบับเสนอ.pdf
- บริษัท ตัวอย่าง จำกัด (มหาชน)
- บริษัท ตัวอย่าง จำกัด (มหาชน) และบริษัทในเครือ
- บันทึกการตรวจทาน
- บันทึกการอนุมัติภายใน
- บันทึกซ้ำ
- บันทึกซ้ำ — ใช้ IRV-2569-0004
- บันทึกประชุมตรวจทาน.docx
- บันทึกผลการตรวจทาน ข้อแก้ไข และการอนุมัติภายใน
- บันทึกร่างแล้ว ·
- ประมาณการทางการเงิน 5 ปี
- ประมาณการทางการเงิน.xlsx
- ประวัติ
- ประวัติ (append-only)
- ปิด
- ผลการตรวจทาน
- ผลการตรวจทานไม่สอดคล้องกับข้อคิดเห็น
- ผลการพิจารณา
- ผลพิจารณาในระบบเติมให้อัตโนมัติ — ใส่เพิ่มเฉพาะการพิจารณานอกระบบ (เช่น ที่ประชุม อีเมล) พร้อมหลักฐาน
- ผู้จัดการฝ่ายการเงิน
- ผู้จัดการฝ่ายพัฒนาธุรกิจ
- ผู้จัดทำ
- ผู้ตรวจทาน
- ผู้ตรวจสอบ
- ผู้บริหาร
- ผู้พิจารณา / ผู้อนุมัติ
- ผู้รับผิดชอบ
- ผู้รับผิดชอบแก้ไข
- ผู้ส่ง
- ผู้อนุมัติ / รับทราบ
- ผู้เชี่ยวชาญด้านพัฒนาธุรกิจ
- ผ่าน
- ผ่านแบบมีข้อแก้ไข
- ฝ่าย
- ฝ่ายการเงิน
- ฝ่ายพัฒนาธุรกิจ
- พ.ค.
- พ.ย.
- พฤ
- พฤศจิกายน
- พฤษภาคม
- พิมพ์
- ม.ค.
- มกราคม
- มาลัย ประสานงาน
- มิ.ย.
- มิถุนายน
- มี.ค.
- มีนาคม
- ยกเลิก
- ยกเลิกการเสนอผู้บริหาร
- ยกเลิกเอกสาร
- ยกเลิกเอกสารแล้ว ·
- ยังไม่มีข้อมูล
- ยังไม่มีบันทึกการตรวจทาน
- ยังไม่มีผลการพิจารณา — ระบบเติมให้เมื่อผู้พิจารณาตัดสินในระบบ
- ยังไม่มีรายการตรวจทาน
- ยังไม่ส่ง
- ย้อนกลับ
- รวมกับใบอื่นแล้ว
- รอขั้นก่อนหน้า
- รองกรรมการผู้จัดการ
- รอผล
- รอพิจารณา
- รออนุมัติ
- ระบุแหล่งเงินทุนและเงื่อนไขการเบิกจ่ายให้ชัดเจน
- รับทราบ — ไม่มีข้อสังเกตเพิ่ม
- รายการ
- รายการตรวจทาน
- รายการเอกสาร / ประเด็น
- รายละเอียด
- ร่าง
- ร่างบันทึกการลงทุน
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ลายมือชื่อ / หลักฐาน
- ลายเซ็น / อนุมัติ
- ลำดับ
- ลำดับการอนุมัติ
- ล้างตัวกรอง
- วันที่
- วันที่ ........./........./.........
- วันที่ตรวจทานต้องไม่เกินวันนี้
- วันที่มีผล
- วันที่มีผลกรอกได้เมื่อสถานะเป็น อนุมัติครบถ้วน หรือ อนุมัติแบบมีเงื่อนไข
- ศิริพร ตัวแทนดี
- ส.ค.
- สถานะ
- สถานะ "ปิด" แต่ไม่มีผู้รับผิดชอบแก้ไขหรือข้อคิดเห็น รายการที่
- สถานะการอนุมัติ
- สถานะสุดท้าย
- สถานะเอกสาร
- สมศักดิ์ ตัวอย่าง
- สร้าง PDF
- สร้างบันทึก
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างโดย
- สลับเป็น
- สิงหาคม
- ส่งต่อขั้นถัดไปแล้ว ·
- ส่งบันทึกการตรวจทานและอนุมัติภายใน?
- ส่งอนุมัติ
- ส่งอนุมัติแล้ว ·
- ส่งออก
- ส่งแล้วแก้ไขไม่ได้ — ถ้าผู้พิจารณาไม่อนุมัติ จะกลับมาเป็นร่างเลขเดิม
- ส่งในระบบ
- อนุมัติ
- อนุมัติ / รับทราบ
- อนุมัติ / รับทราบเรียบร้อย ·
- อนุมัติ / รับทราบแล้ว
- อนุมัติครบถ้วน
- อนุมัติภายในและสถานะสุดท้าย
- อนุมัติแบบมีเงื่อนไข
- อนุมัติแล้ว
- อยู่ระหว่างแก้ไข
- อรุณี ทดสอบระบบ
- อา
- อีเมลยืนยัน 23 ก.ย. 2569
- เจ้าหน้าที่ประสานงานโครงการ
- เช่น อีเมล / บันทึกประชุม
- เดือนถัดไป
- เด้งกลับบน
- เปิด
- เพิ่มทางเลือกไม่ลงทุน (base case)
- เพิ่มสรุปผลตอบแทนและระยะคืนทุนในหน้าแรก
- เพิ่มเติม
- เม.ย.
- เมษายน
- เลขที่
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกตอนส่ง
- เลือกประเทศ
- เลือกผู้พิจารณา
- เลือกวันที่
- เลือกสถานะ…
- เลือก…
- เสนอคณะกรรมการบริษัทในการประชุมครั้งถัดไป
- เหตุผลที่ยกเลิก
- เอกสารประกอบด้านกฎหมาย
- เอกสารประกอบไม่ครบถ้วน
- เอกสารแนบ
- แก้ไขร่าง
- แก้ไขล่าสุด
- แก้ไขเอกสาร
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งผู้จัดทำว่าต้องปรับอะไร
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบประเมินความเสี่ยงโครงการ
- แบบฟอร์มบันทึกการตรวจทานและอนุมัติภายใน
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- แผนการดำเนินงานและกำหนดเวลา
- แผนงานไตรมาส 2 ไม่สอดคล้องกับงบประมาณ ต้องทบทวน
- แสดงต่อหน้า
- ใช้ในขั้นตอน
- ใส่เอกสาร/ประเด็นที่ตรวจทานทีละรายการ พร้อมผลการตรวจทาน ข้อแก้ไข และสถานะ
- ไฟล์
- ไม่ผ่าน
- ไม่ผ่านการตรวจสอบ
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่มีข้อแก้ไข
- ไม่ยกเลิก
- ไม่อนุมัติ
- — กลับเป็นร่าง
- — กลับเป็นร่าง (ขั้น
- — คุณเป็นผู้พิจารณาใบนี้
- — บันทึกได้ แต่ควรระบุ

## §10 Data Binding & BACKEND anchors
| จุดในโค้ด | API (02_API) |
|---|---|
| `listRows()` `RECS.filter(canSee)` | API-01 |
| `openView()` | API-02 |
| `persist()` (+ `ENG-DOC-NUM` ครั้งแรก) | API-03 / API-04 |
| `openSubmit()` `resolveDoa()` (DOA-ENGINE-HOOK) | API-05 |
| `confirmSubmit()` | API-06 |
| `confirmApprove()` (+ `apRowOf()` เติมแถวอนุมัติภายใน) | API-07 approve |
| `confirmReason()` reject | API-07 reject |
| `confirmReason()` cancel | API-08 |
| `docPrintData()` + `tplRender()` + `IRV_TPL` · `genPdf()` | API-09 (server render template เดียวกัน · 2 หน้า) |
| `chunkSigns()` · `DECISION_WORDS` / `wordsOf()` | ตารางลงชื่อ PDF = ผู้จัดทำ + ขั้นใน `approval_chain` (จำนวนตาม DOA) · คำตัดสินตาม role (print_config) |
| `openItems()` · `completeWithOpen()` · `closedNoOwner()` · `RV_CFG` | FN-02 คำนวณฝั่ง server + ReviewApprovalConfig |
| `validateMain()` · `validateApproval()` | FN-01 · VR-01..04 |
| `exportCSV()` | API-10 |
| `pickFiles()` `gateFiles()` | API-11 |
markers: ENG-DOC-NUM, DOA-ENGINE-HOOK, ENG-DOC-NUM, ENG-NOTIFY, DOA-ENGINE-HOOK, ENG-DOC-NUM, ENG-NOTIFY

## §11 Traceability + Drift Log
| Brief | FRD | HTML |
|---|---|---|
| §4 P-01 | 01 P-01 · API-01/10 | `renderPage()` |
| §4 P-02 | 01 P-02 · API-03/04/11 · BR-01..06 | `renderWizard()` |
| §4 P-03 | 01 P-03 · API-02/05..09 | `renderViewDrawer()` |
| §8 | 05 §5.2 state · LD-01/02 | `DOC_ST` · `curStep()` |
| Drift | ชนิด | ข้อเสนอ |
|---|---|---|
| D-01 | prototype-only: `__QA__` · `switchPersona()` · `S.sim` · mock `EMP`/`RECS` | ระบบจริงไม่ต้องมี |
| D-02 | prototype ถือ `RV_CFG` เป็น const · ระบบจริงอ่าน ReviewApprovalConfig (FRD BR-01) | dev ทำตาม FRD |

## §12 Diff จากเวอร์ชันก่อน
— ไม่มีใน HTML นี้ (เวอร์ชันแรก)

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- ช่องอ้างอิงโครงการ / FM-BDM-05 เมื่อลูกค้ายืนยัน OQ-05
- ผลการตรวจทานเป็นรายการตัวเลือก (OQ-06) · dashboard ข้อแก้ไขค้างข้ามใบ
