# UI_BRIEF — F-TMP-007 แบบฟอร์มชุดเอกสารส่งมอบงาน (สำหรับฝ่ายพัฒนาธุรกิจจัดเก็บ) (AS-BUILT)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| HTML (source of truth) | `feature.html` · html-generator-v9.4 · archetype `Q-form` (`<meta name="cube-archetype">`) · audit FAIL 0 · e2e 21/21 (verify บน cloud container — เครื่อง user NO-BROWSER) |
| FRD | FRD_F-TMP-007_Pack v1.0 (FULL) · DECISIONS.lock 16 มติ (DEC-01..16 · AI-DEFAULT 11) |
| Prototype-only | `window.__QA__` · ตัวสลับผู้ใช้ `switchPersona()` · `S.sim` / `commitRejected()` · `EMP`/`RECS` mock → ไม่ต้องสร้างในระบบจริง (Drift Log D-01) |
| Drift | 0 business drift · 2 prototype-only (§11) |

## §1 Design Tokens AS-BUILT
CI Warm Light (html-generator-v9) · font Satoshi + Noto Sans Thai (หน้าจอ) · Sarabun (PDF) · สถานะเอกสารในชุด: `pill-success` (ครบถ้วน) · `pill-warning` (มีข้อจำกัด) · `pill-danger` (ขาดเอกสาร) · `pill-muted` (ไม่เกี่ยวข้อง) · สถานะข้อมูล: `pill-success` (สมบูรณ์) · `pill-warning` (มีข้อจำกัด) · `pill-info` (รอข้อมูลเพิ่มเติม)
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
| `.menu-fixed` | `var(--z-popover)` |
| `.ss-list` | `var(--z-backdrop)` |
| `.ss-list.menu-fixed` | `var(--z-popover)` |
| `.table-scroll.is-sticky thead th` | `3` |
| `.stepper-circle` | `2` |
| `.stepper-item:not(:last-child)::after` | `1` |
| `.drawer-backdrop` | `var(--z-backdrop)` |
| `.drawer` | `var(--z-drawer)` |
| `.modal-backdrop` | `var(--z-backdrop)` |
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
| `#/handover-package-bd` | P-01 รายการ (default) | `applyRoute()` · `renderPage()` |
| `#/handover-package-bd/create` | P-02 สร้าง | `startWizard()` |
| `#/handover-package-bd/edit/:id` | P-02 แก้ร่าง (เจ้าของ · draft) | `startWizard()` |
| `#/handover-package-bd/view/:id` | P-03 ดู (เฉพาะ `canSee`) | `openView()` · `showDrawer()` |
refresh-safe ผ่าน `hashchange` → `applyRoute()` · route ใบไม่มีสิทธิ์ = ไม่เปิด drawer

## §3 Layout Shell
`.sidebar` โมดูล Business Development › ชุดเอกสารส่งมอบงาน (BD) + badge `#sbBadge` (= รอฉันพิจารณา) · `.shell-bar` breadcrumb Core › Business Development › ชุดเอกสารส่งมอบงาน (สำหรับฝ่ายพัฒนาธุรกิจจัดเก็บ) · user chip (icon คน · `toggleUserMenu()`) + `.user-menu` สลับผู้ใช้ (prototype) · `#page-content`

## §4 Page Anatomy
### P-01 รายการ — `renderPage()`
`.ph` (ชื่อ + `.ph-en` + `.ph-badge` ×≤3: รายการ · เปิดอยู่ · รอฉันพิจารณา — ค่า 0 ไม่แสดง · ไม่มี stat cards U1) · ปุ่ม `exportCSV()` / `#btnCreate` → `startWizard()` · `.filter-bar` (`#fq` `onQ()` · search select `fst` `fds` `fdept` ผ่าน `initSearchSelect()` · รีเซ็ต `resetFilters()`) · `.table-wrap .table` คอลัมน์ เลขที่ · วันที่ · ผู้จัดทำ (`personInline()`) · ชื่อโครงการ (`.ell`) · ผู้รับมอบ (`personInline()`) · รายการเอกสาร · ขาด / มีข้อจำกัด (`gapItems()` · `.is-warn-t`) · สถานะข้อมูล `dtPill()` · สถานะเอกสาร `docPill()` · ลายเซ็น `renderSignProgress()` · ⋮ `openRowMenu()` · `pager()` + `setSize()` (10/25/50 · ค่าเริ่ม 25) `goPage()`
### P-02 สร้าง/แก้ — `renderWizard()` (drawer `.drawer.wide`)
`stepper()` 3 ขั้น (`STEPS`) · ขั้น 1 `wizMain()`: ข้อมูลการส่งมอบ `.ho-grid` (`[name=hoProject]` ชื่อโครงการ · search select `hoSender` ผู้ส่งมอบ · `hoRecv` ผู้รับมอบ / ฝ่ายบริหารการลงทุน · `.bedate` (key `hodate`) วันที่ส่งมอบ · `[name=hoVer]` ฉบับชุดเอกสาร · `[name=hoDs]` สถานะข้อมูล · `setHo()` · `#gapWarn`) · `sumStrip()` (`#sumCnt` `#sumGap` + legend สถานะเอกสาร) · `.dc-tbl` แถว `docRow()` ช่อง `[name=dn-i]` ชื่อเอกสาร · `[name=dr-i]` รหัส / ฉบับ · `.bedate` (key `dd{i}`) วันที่เอกสาร · `[name=do-i]` ผู้รับผิดชอบ (`#dlEmp`) · `[name=dt-i]` สถานะ · `[name=dl-i]` ตำแหน่งจัดเก็บ / ลิงก์ · `[name=dm-i]` หมายเหตุ · ลบ `removeDoc()` · `.add-row` `addDoc()` · `#lateWarn` · อัปเดตสด `setDoc()` → `softSums()` · ขั้น 2 `wizNotes()`: `[name=nAssm]` `[name=nIssues]` `[name=nLimits]` (`#fNl` บังคับเมื่อ `needLimits()`) `[name=nSupport]` · `setNote()` · `wizAttach()` `.upload-zone` `pickFiles()` · ขั้น 3 `wizReview()` (`handoverBlock()` · `docTable()` · `notesBlock()`) · footer `wizBack()` `wizNext()` `saveDraft()` `saveAndSubmit()`
### P-03 ดู — `renderViewDrawer()`
หัว `.dw-head` (เลขที่ · `docPill()` · sub ≤2 fact: เอกสาร n · ขาด / มีข้อจำกัด n) · ปุ่ม `#btnSubmitView` `openSubmit()` / `#btnApproveView` `openApprove()` / `openReject()` / `openCancel()` · `.drawer-tabs` `tabBtn()` → `renderDetailTab()` (`handoverBlock()` · `docTable()` · `notesBlock()`) · `renderPdfTab()` (`.pdf-slot` iframe `.pdf-frame` srcdoc `docPdfDoc()` · `fitPdf()` · `genPdf()`) · `renderSignTab()` · `renderHistoryTab()`

## §5 Component Inventory
| Component | anchor | states |
|---|---|---|
| ข้อมูลการส่งมอบ (แก้) | `.ho-grid` `wizMain()` | `.field.is-invalid` ต่อช่อง · เตือน `#gapWarn` (DEC-13) |
| ตารางรายการเอกสาร (แก้) | `.dc-tbl` `docRow()` | default · `.is-bad` ต่อช่อง · ลบ (เมื่อ >1 แถว) · เตือน `#lateWarn` (DEC-16) |
| ตัวเลือกวัน พ.ศ. | `bedateHTML()` `.bedate` `.bd-pop` (portal) | ว่าง · เลือกแล้ว · `.field.is-invalid` |
| สมมติฐาน/ข้อจำกัด | `wizNotes()` `notesBlock()` | ข้อจำกัดของข้อมูล `#fNl` บังคับเมื่อมีข้อจำกัด (DEC-14) |
| แถบสรุปสด | `.rk-strip.ho-strip` `sumStrip()` | อัปเดตแบบ soft (focus ไม่หลุด) |
| ตารางรายการ (อ่าน) | `docTable()` `.rk-view` | ว่าง = แผง "ไม่มีข้อมูล" (U23) · ไอคอนเตือนวันที่ |
| คน | `empChip()` `personInline()` `nameInline()` `.emp-av` | วงกลมพื้นดำ + icon คน (U17) |
| progress ลายเซ็น | `renderSignProgress()` `.sign-prog` | ร่าง = — · n/N |
| slot ผู้พิจารณา | `.slot-row` + search select `slot{i}` | ค่าเริ่ม (ขั้นรับทราบ = ผู้รับมอบ) · `.is-invalid` |
| ปุ่ม busy | `busyLabel()` | loading "กำลังบันทึก…" · disabled |

## §6 Overlay Registry
| Overlay | anchor | ขนาด | ปิดด้วย |
|---|---|---|---|
| drawer สร้าง/แก้ | `#drawer` `.drawer-panel.wide` + `#drawerBackdrop` | wide | ปุ่ม/Esc/backdrop (`onmousedown` U25) · **กรอกค้าง → modal ทิ้งข้อมูล** (`closeDrawer()` dirty) |
| drawer ดู | `#drawer` `.drawer-panel` | 920 | ปุ่ม ปิด/Esc/backdrop |
| modal ส่ง/รับมอบ | `#modal` `.modal.is-lg` | lg | ยกเลิก · Esc · backdrop mousedown (`modalBackdropClick()` — มีข้อความค้างห้ามปิด) |
| modal ไม่ผ่าน/ยกเลิก/ทิ้ง | `#modal` | md | เช่นเดียวกัน |
| ปฏิทิน พ.ศ. | `.bd-pop` (portal `#overlay-root`) | 280px | เลือกวัน · คลิกนอก · Esc (ปิดแค่ปฏิทิน) |
| เมนู ⋮ | `.row-menu` (portal) | 180px | คลิกนอก · scroll |
| search list | `.ss-list.menu-fixed` | | Esc · คลิกนอก |
| toast | `#toast` `.toast` | | อัตโนมัติ |
| user menu | `.user-menu` | | คลิกนอก |

## §7 Interaction Spec
Esc chain: ปฏิทินเปิด → ปิดปฏิทินก่อน (capture · stopPropagation) → search list → modal → `closeModal()` → drawer → `closeDrawer()` · backdrop ปิดด้วย mousedown เท่านั้น · `addDoc()` focus ช่องชื่อเอกสารของแถวใหม่ · เลือกสถานะเอกสาร → จำนวนขาด/มีข้อจำกัดอัปเดตทันที + เตือนสมบูรณ์แต่ขาด · เลือกวันที่เอกสาร/วันที่ส่งมอบ → เตือนวันที่เอกสารหลังวันส่งมอบ · ผู้รับมอบที่เลือก → ค่าเริ่ม slot ขั้นรับทราบ (`resolveDoa()` DEC-15)

## §8 State-Driven UI Matrix
| status | pill | ปุ่มหัว (ผู้มีสิทธิ์) |
|---|---|---|
| draft | ร่าง `pill-muted` | เจ้าของ: ยกเลิก · แก้ไข · ส่งอนุมัติ |
| pending | รออนุมัติ `pill-warning` | ผู้พิจารณาขั้นปัจจุบัน: คำปฏิเสธของขั้น · คำอนุมัติของขั้น · อื่น (เจ้าของ/admin): ยกเลิกเอกสาร |
| approved | อนุมัติแล้ว `pill-success` | — (ล็อก) |
| cancelled | ยกเลิก `pill-muted` | — |
สถานะข้อมูล (HandoverPackageConfig.data_statuses): สมบูรณ์ `pill-success` · มีข้อจำกัด `pill-warning` · รอข้อมูลเพิ่มเติม `pill-info`
คำตัดสินผูก role (`DECISION_WORDS` → `wordsOf()`): role-line-manager = ตรวจสอบแล้ว/ไม่ผ่านการตรวจสอบ · role-mgr-bu = รับมอบ / รับทราบ/ไม่รับมอบ · อื่น = อนุมัติ/ไม่อนุมัติ · จำนวน/ลำดับขั้นมาจาก DOA

## §9 Microcopy (verbatim)
### toast
- `ไม่มีการแจ้งเตือนใหม่`
- `แบบเอกสารนี้ยังไม่เปิดใช้งาน`
- `แก้ไขได้เฉพาะร่างของตัวเอง`
- `กรุณากรอกข้อมูลให้ครบถ้วน`
- `กรุณาระบุข้อจำกัดของข้อมูล`
- `กรุณากรอกข้อมูลให้ครบถ้วน`
- `บันทึกร่างแล้ว ·`
- `กรุณากรอกข้อมูลให้ครบถ้วน`
- `ส่งอนุมัติแล้ว ·`
- `ส่งออก`
- `สลับเป็น`
- `แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง`
- ประกอบ: `กลับเป็นร่างแล้ว · {เลขที่}` · `ยกเลิกเอกสารแล้ว · {เลขที่}` · `รับมอบ / รับทราบเรียบร้อย · {เลขที่}` · `ส่งต่อขั้นถัดไปแล้ว · {เลขที่}` · `บันทึกร่างแล้ว · {เลขที่}` · `… · แจ้งผู้จัดทำ: เอกสารขาด / มีข้อจำกัด {n} รายการ`
### ปุ่ม / placeholder / label
`Business Development` · `กลับไปกรอกต่อ` · `ดาวน์โหลด PDF` · `ถัดไป` · `ทิ้งข้อมูล` · `บันทึกแบบร่าง` · `ปิด` · `พิมพ์` · `ยกเลิก` · `ยกเลิกเอกสาร` · `ย้อนกลับ` · `รีเซ็ต` · `วันนี้` · `สร้างชุดส่งมอบ` · `ส่งอนุมัติ` · `ส่งออก CSV` · `เพิ่มรายการเอกสาร` · `แก้ไข`

`ค้นหาเลขที่ / โครงการ / ผู้จัดทำ / ชื่อเอกสาร` · `ชื่อเอกสารในชุด` · `ชื่อโครงการที่ส่งมอบ` · `ผู้รับผิดชอบ` · `รหัส / ฉบับ` · `หมายเหตุ` · `เช่น ฉบับที่ 1` · `โฟลเดอร์ / ลิงก์` · `ไม่บังคับ` · `ไม่บังคับ — บันทึกลงประวัติการพิจารณา` · aria: `ชื่อเอกสาร` · `ตำแหน่งจัดเก็บ / ลิงก์` · `ผู้รับผิดชอบ` · `รหัส / ฉบับ` · `สถานะ` · `สถานะข้อมูล` · `หมายเหตุ` · `เดือนก่อน` · `เดือนถัดไป` · `แสดงต่อหน้า`
### ข้อความอื่น (จากโค้ด)
- (ขั้น
- CUBE › BD › แฟ้มโครงการ
- [Lucide] All CDNs failed. Icons จะไม่แสดง but UI ยังใช้งานได้
- ]); if (canCancel(r)) items.push(['x-circle', 'ยกเลิกเอกสาร',
- ]]; if (isOwner(r) && r.status === 'draft') items.unshift(['pencil', 'แก้ไข',
- showToast('ไม่มีการแจ้งเตือนใหม่','info')
- · อนุมัติแล้ว ล็อกแก้ไข
- · แจ้งผู้จัดทำ: เอกสารขาด / มีข้อจำกัด
- ก.ค.
- ก.พ.
- ก.ย.
- กรกฎาคม
- กรรมการผู้จัดการ
- กรอกชื่อเอกสารและสถานะให้ครบทุกรายการ (หรือลบแถวที่ไม่ใช้)
- กรุณากรอกข้อมูลให้ครบถ้วน
- กรุณาระบุข้อจำกัดของข้อมูล
- กลับเป็นร่างแล้ว ·
- กันยายน
- กำลังเปิดหน้าต่างพิมพ์ ·
- กิตติพัฒน์ ทดลองงาน
- กุมภาพันธ์
- ขั้นตอนที่ 6: จัดทำและส่งต่องานให้ฝ่ายบริหารการลงทุน
- ขั้นทดสอบ
- ขาด / มีข้อจำกัด
- ขาดเอกสาร
- ข้อจำกัดของข้อมูลบังคับเมื่อสถานะข้อมูลหรือรายการเอกสารใด "มีข้อจำกัด"
- ข้อมูลการส่งมอบ
- ข้อมูลการส่งมอบและรายการเอกสาร
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้าม
- คน
- ครบถ้วน
- คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค่าเริ่มต้น = ผู้รับมอบที่เลือกในเอกสาร
- ค่าเริ่มต้นจากสายอนุมัติและผังองค์กร
- ค้นหา...
- ค้นหาเลขที่ / โครงการ / ผู้จัดทำ / ชื่อเอกสาร
- จัดทำครั้งแรก
- ฉบับชุดเอกสาร
- ฉบับที่ 2
- ฉบับที่ผ่านอนุมัติ
- ชนิดไฟล์ไม่รองรับ
- ชยพล ตั้งระบบ
- ชื่อ
- ชื่อฟังก์ชัน
- ชื่อเอกสาร
- ชื่อโครงการ
- ชื่อโครงการที่ส่งมอบ
- ชุดเอกสารส่งมอบ_โครงการA.pdf
- ชุดเอกสารส่งมอบงาน
- ดาวน์โหลด PDF
- ต.ค.
- ตรวจสอบและยืนยัน
- ตรวจสอบแล้ว
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตำแหน่ง
- ตำแหน่งจัดเก็บ / ลิงก์
- ตุลาคม
- ต้อง
- ถึง
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ทุกฝ่าย
- ทุกสถานะข้อมูล
- ทุกสถานะเอกสาร
- ธ.ค.
- ธันวาคม
- ธีรพงษ์ สมมติชื่อ
- นภัสสร ตัวอย่างดี
- นักวิเคราะห์การลงทุน
- บทสรุปผู้บริหารและบันทึกการลงทุน
- บริษัท ตัวอย่าง จำกัด (มหาชน)
- บริษัท ตัวอย่าง จำกัด (มหาชน) และบริษัทในเครือ
- บันทึกการตรวจทานและอนุมัติภายใน
- บันทึกซ้ำ
- บันทึกซ้ำ — ใช้ HOB-2569-0004
- บันทึกประชุมส่งมอบ.docx
- บันทึกร่างแล้ว ·
- ประมาณการทางการเงิน 5 ปี (ไฟล์คำนวณ)
- ประมาณการทางการเงิน.xlsx
- ประวัติ
- ประวัติ (append-only)
- ประเสริฐ สมมติ
- ปิด
- ผู้จัดการฝ่ายบริหารการลงทุน
- ผู้จัดการฝ่ายพัฒนาธุรกิจ
- ผู้จัดการส่วนบริหารพอร์ตการลงทุน
- ผู้จัดทำ
- ผู้ตรวจสอบ
- ผู้บริหาร
- ผู้รับผิดชอบ
- ผู้รับมอบ
- ผู้รับมอบเป็นผู้พิจารณาขั้นรับทราบโดยค่าเริ่ม (เปลี่ยนได้ตอนส่งอนุมัติ)
- ผู้ส่ง
- ผู้ส่งมอบ
- ผู้อนุมัติ / รับทราบ
- ผู้เชี่ยวชาญด้านพัฒนาธุรกิจ
- ฝ่าย
- ฝ่ายบริหารการลงทุน
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
- มีข้อจำกัด
- มีนาคม
- ยกเลิก
- ยกเลิกการส่งมอบโครงการ
- ยกเลิกเอกสาร
- ยกเลิกเอกสารแล้ว ·
- ยังไม่มีข้อมูล
- ยังไม่มีชุดเอกสารส่งมอบ
- ยังไม่มีรายการเอกสาร
- ยังไม่ส่ง
- ย้อนกลับ
- รวบรวมและตรวจสอบความครบถ้วนของเอกสารก่อนส่งมอบให้ฝ่ายบริหารการลงทุน
- รวมกับชุดส่งมอบอื่นแล้ว
- รหัส / ฉบับ
- รอขั้นก่อนหน้า
- รอข้อมูลเพิ่มเติม
- รอผล
- รอพิจารณา
- รออนุมัติ
- รับมอบ / รับทราบ
- รับมอบ / รับทราบเรียบร้อย ·
- รับมอบ / รับทราบแล้ว
- รายการ
- รายการเอกสาร
- รายงานสำรวจพื้นที่
- รายละเอียด
- ร่าง
- ร่างสัญญาร่วมทุนยังไม่ได้รับจากฝ่ายกฎหมาย
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ลายเซ็น / อนุมัติ
- ลำดับ
- ลำดับการอนุมัติ
- ลิงก์ / ตำแหน่งจัดเก็บเปิดไม่ได้
- ล้างตัวกรอง
- วันที่
- วันที่ ........./........./.........
- วันที่ส่งมอบ
- วันที่เอกสารหลังวันที่ส่งมอบ
- ศิริพร ตัวแทนดี
- ส.ค.
- สถานะ
- สถานะข้อมูล
- สถานะเอกสาร
- สมบูรณ์
- สมมติฐาน ข้อจำกัด และเอกสารแนบ
- สมมติฐาน ประเด็นค้าง และข้อจำกัด
- สมมติฐานสำคัญ
- สมมติฐานและข้อจำกัดยังไม่ชัดเจน
- สร้าง PDF
- สร้างชุดส่งมอบ
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างโดย
- สลับเป็น
- สัญญาร่วมทุน (ร่าง)
- สิงหาคม
- ส่งชุดเอกสารส่งมอบงานเพื่ออนุมัติ?
- ส่งต่อขั้นถัดไปแล้ว ·
- ส่งสัญญาร่วมทุนฉบับร่างเมื่อได้รับจากฝ่ายกฎหมาย · ตอบข้อซักถามภายใน 30 วัน
- ส่งอนุมัติ
- ส่งอนุมัติแล้ว ·
- ส่งออก
- ส่งแล้วแก้ไขไม่ได้ — ถ้าผู้พิจารณาไม่อนุมัติ จะกลับมาเป็นร่างเลขเดิม
- ส่งในระบบ
- อนุมัติ
- อนุมัติแล้ว
- อรุณี ทดสอบระบบ
- อัตราแลกเปลี่ยน 35 บาท/ดอลลาร์ · อัตราคิดลด 8%
- อา
- เจ้าหน้าที่ประสานงานโครงการ
- เช่น ฉบับที่ 1
- เดือนถัดไป
- เด้งกลับบน
- เพิ่มเติม
- เม.ย.
- เมษายน
- เลขที่
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกตอนส่ง
- เลือกประเทศ
- เลือกผู้พิจารณา
- เลือกผู้รับมอบ
- เลือกผู้ส่งมอบ
- เลือกวันที่
- เลือกสถานะ…
- เลือก…
- เหตุผลที่ยกเลิก
- เอกสารแนบ
- เอกสารในชุดไม่ครบถ้วน
- เอกสารในชุดไม่ครบถ้วน — แนบสัญญาร่วมทุนก่อนส่งมอบ
- แก้ไขร่าง
- แก้ไขล่าสุด
- แก้ไขเอกสาร
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งผู้จัดทำว่าต้องปรับอะไร
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบฟอร์มชุดเอกสารส่งมอบงาน (สำหรับฝ่ายพัฒนาธุรกิจจัดเก็บ)
- แบบฟอร์มบันทึกภาพรวมและเริ่มต้นโครงการ
- แบบฟอร์มประเมินความเสี่ยง
- แบบฟอร์มสรุปผลการคัดกรองโครงการเบื้องต้น
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- แสดงต่อหน้า
- โครงการขยายกำลังการผลิต B
- โครงการขยายกำลังการผลิต B (ฉบับปรับปรุง)
- โครงการคลังสินค้าภาคตะวันออก D
- โครงการปรับปรุงสายการผลิต I
- โครงการพลังงานชีวมวล C
- โครงการพลังงานแสงอาทิตย์ G
- โครงการระบบน้ำอุตสาหกรรม F
- โครงการร่วมทุนโลจิสติกส์ E
- โครงการศูนย์กระจายสินค้า H
- โครงการโรงงานต้นแบบ A
- โครงการโรงงานต้นแบบ A (ระยะ 2)
- โฟลเดอร์ / ลิงก์
- ใช้ในขั้นตอน
- ไดรฟ์กลาง › BD › Model
- ไฟล์
- ไม่ผ่านการตรวจสอบ
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่มี
- ไม่ยกเลิก
- ไม่รับมอบ
- ไม่อนุมัติ
- ไม่เกี่ยวข้อง
- — กลับเป็นร่าง
- — กลับเป็นร่าง (ขั้น
- — คุณเป็นผู้พิจารณาใบนี้

## §10 Data Binding & BACKEND anchors
| จุดในโค้ด | API (02_API) |
|---|---|
| `listRows()` `RECS.filter(canSee)` | API-01 |
| `openView()` | API-02 |
| `persist()` (+ `ENG-DOC-NUM` ครั้งแรก) | API-03 / API-04 |
| `openSubmit()` `resolveDoa()` (DOA-ENGINE-HOOK · ขั้นรับทราบ = ผู้รับมอบ) | API-05 |
| `confirmSubmit()` | API-06 |
| `confirmApprove()` (+ toast แจ้งผู้จัดทำเมื่อยังมีเอกสารขาด) | API-07 approve |
| `confirmReason()` reject | API-07 reject |
| `confirmReason()` cancel | API-08 |
| `docPrintData()` + `tplRender()` + `HOB_TPL` · `genPdf()` | API-09 (server render template เดียวกัน · 2 หน้า) |
| `chunkSigns()` · `DECISION_WORDS` / `wordsOf()` | ตารางลงชื่อ PDF = ผู้จัดทำ + ขั้นใน `approval_chain` (จำนวนตาม DOA) · คำตัดสินตาม role (print_config) |
| `gapItems()` · `completeWithGap()` · `needLimits()` · `lateDocs()` · `HO_CFG` | FN-02 คำนวณฝั่ง server + HandoverPackageConfig |
| `validateMain()` · `validateNotes()` | FN-01 · VR-01..05 |
| `exportCSV()` | API-10 |
| `pickFiles()` `gateFiles()` | API-11 |
markers: ENG-DOC-NUM, DOA-ENGINE-HOOK, ENG-NOTIFY

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
| D-02 | prototype ถือ `HO_CFG` เป็น const · ระบบจริงอ่าน HandoverPackageConfig (FRD BR-01) | dev ทำตาม FRD |

## §12 Diff จากเวอร์ชันก่อน
— ไม่มีใน HTML นี้ (เวอร์ชันแรก)

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- ดึงรายการเอกสารจากเอกสาร BDM ในระบบ (FM-BDM-01..06) เป็นตัวเลือกเมื่อลูกค้ายืนยัน OQ-05
- เชื่อมกับฉบับฝ่ายบริหารการลงทุน FM-BDM-08 (OQ-06)
