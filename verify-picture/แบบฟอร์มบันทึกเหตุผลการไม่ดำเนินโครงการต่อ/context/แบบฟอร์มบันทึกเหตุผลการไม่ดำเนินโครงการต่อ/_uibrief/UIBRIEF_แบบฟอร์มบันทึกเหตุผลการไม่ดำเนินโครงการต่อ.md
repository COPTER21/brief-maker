# UI_BRIEF — F-TMP-004 แบบฟอร์มบันทึกเหตุผลการไม่ดำเนินโครงการต่อ (AS-BUILT)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| HTML (source of truth) | `feature.html` · html-generator-v9.4 · archetype `Q-form` (`<meta name="cube-archetype">`) · audit FAIL 0 · e2e 21/21 (verify บน cloud container — เครื่อง user NO-BROWSER) |
| FRD | FRD_F-TMP-004_Pack v1.0 (FULL) · DECISIONS.lock 16 มติ (DEC-01..16 · AI-DEFAULT 11) |
| Prototype-only | `window.__QA__` · ตัวสลับผู้ใช้ `switchPersona()` · `S.sim` / `commitRejected()` · `EMP`/`RECS` mock → ไม่ต้องสร้างในระบบจริง (Drift Log D-01) |
| Drift | 0 business drift · 2 prototype-only (§11) |

## §1 Design Tokens AS-BUILT
CI Warm Light (html-generator-v9) · font Satoshi + Noto Sans Thai (หน้าจอ) · Sarabun (PDF) · สถานะการปิดโครงการ: pill `pill-success` (ปิดโครงการแล้ว) · `pill-info` (รอจัดเก็บเอกสาร) · `pill-warning` (ติดตามเงื่อนไขในอนาคต) · ตัวเลือกวัน พ.ศ. `.bedate` + `.bd-pop` (Rule #114)
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
| `.bd-pop` | `var(--z-portal)` |
ค่าที่ใช้: `1`, `2`, `3`, `var(--z-backdrop)`, `var(--z-drawer)`, `var(--z-dropdown)`, `var(--z-modal)`, `var(--z-popover)`, `var(--z-portal)`, `var(--z-shell)`, `var(--z-sticky)`, `var(--z-toast)`

## §2 Route Map
| Route | หน้า | handler |
|---|---|---|
| `#/project-discontinuation` | P-01 รายการ (default) | `applyRoute()` · `renderPage()` |
| `#/project-discontinuation/create` | P-02 สร้าง | `startWizard()` |
| `#/project-discontinuation/edit/:id` | P-02 แก้ร่าง (เจ้าของ · draft) | `startWizard()` |
| `#/project-discontinuation/view/:id` | P-03 ดู (เฉพาะ `canSee`) | `openView()` · `showDrawer()` |
refresh-safe ผ่าน `hashchange` → `applyRoute()` · route ใบไม่มีสิทธิ์ = ไม่เปิด drawer

## §3 Layout Shell
`.sidebar` โมดูล Business Development › บันทึกไม่ดำเนินโครงการต่อ + badge `#sbBadge` (= รอฉันพิจารณา) · `.shell-bar` breadcrumb Core › Business Development › บันทึกไม่ดำเนินโครงการต่อ · user chip (icon คน · `toggleUserMenu()`) + `.user-menu` สลับผู้ใช้ (prototype) · `#page-content`

## §4 Page Anatomy
### P-01 รายการ — `renderPage()`
`.ph` (ชื่อ + `.ph-en` + `.ph-badge` ×≤3: รายการ · เปิดอยู่ · รอฉันพิจารณา — ค่า 0 ไม่แสดง · ไม่มี stat cards U1) · ปุ่ม `exportCSV()` / `#btnCreate` → `startWizard()` · `.filter-bar` (`#fq` `onQ()` · search select `fst` `fcls` `fdept` ผ่าน `initSearchSelect()` · รีเซ็ต `resetFilters()`) · `.table-wrap .table` คอลัมน์ เลขที่ · วันที่ · ผู้จัดทำ (`personInline()`) · ชื่อโครงการ (`.cell-trunc` ตัด … 1 บรรทัด U18) · เหตุผล (`selCount()`) · สถานะการปิดโครงการ `closurePill()` · สถานะเอกสาร `docPill()` · ลายเซ็น `renderSignProgress()` · ⋮ `openRowMenu()` · `pager()` + `setSize()` (10/25/50 · ค่าเริ่ม 25) `goPage()`
### P-02 สร้าง/แก้ — `renderWizard()` (drawer `.drawer.wide`)
`stepper()` 3 ขั้น (`STEPS`) · ขั้น 1 `wizMain()`: `sumStrip()` `.pc-strip` (`#sumCnt` `#sumNames` + สถานะการปิด) · การ์ด `.wz-card` ① ข้อมูลโครงการ `.pc-grid`: ช่อง id `in-` + key (`fieldTxt()` · name) · search select `pjOwner` (`setOwner()`) · `bedateHTML()` `pjDate` → `pickDecisionDate()` · ช่อง stage (`fieldTxt()`) · ② `.pc-tbl` แถว `reasonRow()`: `[name=rsel-i]` เลือก (`setSel()`) · `[name=rdetail-i]` · `[name=revidence-i]` · `[name=rimpact-i]` · `[name=rrevisit-i]` (`setR()` · disabled เมื่อ ไม่ใช่) · `.trip-err` ข้อความรวม · ③ `fieldTxt()` key summary · docs · lessons · archive · follow (textarea id `in-` + key · `setC()`) · `.pc-st` `.pc-st-card` ×3 `setStatus()` · ขั้น 2 `wizAttach()` `.upload-zone` `pickFiles()` · ขั้น 3 `wizReview()` (`projectFields()` · `reasonTable()` · `closureFields()`) · footer `wizBack()` `wizNext()` `saveDraft()` `saveAndSubmit()`
### P-03 ดู — `renderViewDrawer()`
หัว `.dw-head` (เลขที่ · `docPill()` · sub ≤2 fact: เหตุผล n ข้อ · สถานะการปิด) · ปุ่ม `#btnSubmitView` `openSubmit()` / `#btnApproveView` `openApprove()` / `openReject()` / `openCancel()` · `.drawer-tabs` `tabBtn()` → `renderDetailTab()` (`projectFields()` · `reasonTable()` · `closureFields()`) · `renderPdfTab()` (`.pdf-slot` iframe `.pdf-frame` srcdoc `docPdfDoc()` · `fitPdf()` · `genPdf()`) · `renderSignTab()` · `renderHistoryTab()`

## §5 Component Inventory
| Component | anchor | states |
|---|---|---|
| ตารางเหตุผล (แก้) | `.pc-tbl` `reasonRow()` | ไม่ใช่ (ช่อง disabled ว่าง) · ใช่ (`tr.is-on` ชื่อเหตุผลสี primary) · `.is-bad` ที่ช่องเลือก/รายละเอียด |
| ตารางเหตุผล (อ่าน) | `reasonTable()` `.pc-view` | แถว ไม่ใช่ = `tr.is-off` จาง · `selPill()` ใช่/ไม่ใช่/— · 8 แถวเสมอ (U23 ไม่มีกรณีว่าง) |
| track card สถานะการปิด | `.pc-st-card` `setStatus()` | default · hover · `.is-on` · `.field.is-invalid` ขอบแดง |
| ช่องกรอก | `fieldTxt()` `.field` | default · `.is-invalid` + `.field-error` · ข้อเสนอให้ติดตาม: * เมื่อสถานะ follow |
| ตัวเลือกวัน พ.ศ. | `bedateHTML()` `.bedate` `.bd-pop` | ว่าง (placeholder) · มีค่า `bdFmt()` · วันหลังวันนี้ disabled (`max`) |
| แถบสรุปสด | `.pc-strip` `sumStrip()` · `softSums()` | อัปเดตแบบ soft (focus ไม่หลุด) |
| คน | `empChip()` `personInline()` `.emp-av` | วงกลมพื้นดำ + icon คน (U17) |
| progress ลายเซ็น | `renderSignProgress()` `.sign-prog` | ร่าง = — · n/N |
| slot ผู้พิจารณา | `.slot-row` + search select `slot{i}` | ค่าเริ่ม · `.is-invalid` |
| สรุปในหน้าต่างอนุมัติ | `closureBrief()` | โครงการ · เหตุผลหลัก · สรุปเหตุผล · สถานะการปิด |
| ปุ่ม busy | `busyLabel()` | loading "กำลังบันทึก…" · disabled |

## §6 Overlay Registry
| Overlay | anchor | ขนาด | ปิดด้วย |
|---|---|---|---|
| drawer สร้าง/แก้ | `#drawer` `.drawer-panel.wide` + `#drawerBackdrop` | wide | ปุ่ม/Esc/backdrop (`onmousedown` U25) · **กรอกค้าง → modal ทิ้งข้อมูล** (`closeDrawer()` dirty) |
| drawer ดู | `#drawer` `.drawer-panel` | 920 | ปุ่ม ปิด/Esc/backdrop |
| modal ส่ง/อนุมัติ | `#modal` `.modal.is-lg` | lg | ยกเลิก · Esc · backdrop mousedown (`modalBackdropClick()` — มีข้อความค้างห้ามปิด) |
| modal ไม่ผ่าน/ยกเลิก/ทิ้ง | `#modal` | md | เช่นเดียวกัน |
| เมนู ⋮ | `.row-menu` (portal) | 180px | คลิกนอก · scroll |
| search list | `.ss-list.menu-fixed` | | Esc · คลิกนอก |
| ปฏิทิน พ.ศ. | `#bd-pop` `.bd-pop` (portal `#overlay-root`) | | Esc (ปิดแค่ปฏิทิน) · คลิกนอก · `bdClose()` ก่อน render |
| toast | `#toast` `.toast` | | อัตโนมัติ |
| user menu | `.user-menu` | | คลิกนอก |

## §7 Interaction Spec
Esc chain: ปฏิทิน พ.ศ. เปิด → ปิดปฏิทินก่อน (capture · stopPropagation) → search list → modal `closeModal()` → drawer `closeDrawer()` · backdrop ปิดด้วย mousedown เท่านั้น · เลือก ใช่ → render แถว + focus `[name=rdetail-i]` · เลือก ไม่ใช่ → ล้างข้อความในแถว · พิมพ์ในตาราง/ช่อง → `softSums()` + ลบ `.is-bad`/`.is-invalid` ทีละช่อง · เลือกสถานะ → render (แสดง * ที่ข้อเสนอให้ติดตามเมื่อ follow)

## §8 State-Driven UI Matrix
| status | pill | ปุ่มหัว (ผู้มีสิทธิ์) |
|---|---|---|
| draft | ร่าง `pill-muted` | เจ้าของ: ยกเลิก · แก้ไข · ส่งอนุมัติ |
| pending | รออนุมัติ `pill-warning` | ผู้พิจารณาขั้นปัจจุบัน: คำปฏิเสธของขั้น · คำอนุมัติของขั้น · อื่น (เจ้าของ/admin): ยกเลิกเอกสาร |
| approved | อนุมัติแล้ว `pill-success` | — (ล็อก) |
| cancelled | ยกเลิก `pill-muted` | — |
สถานะการปิดโครงการ (`CLOSURE_CFG.statuses` = ProjectClosure.closure_statuses): ปิดโครงการแล้ว `pill-success` · รอจัดเก็บเอกสาร `pill-info` · ติดตามเงื่อนไขในอนาคต `pill-warning`
คำตัดสินผูก role (`DECISION_WORDS` → `wordsOf()`): role-line-manager = ตรวจสอบแล้ว/ไม่ผ่านการตรวจสอบ · role-gm = อนุมัติ / รับทราบ/ไม่อนุมัติ · อื่น = อนุมัติ/ไม่อนุมัติ · จำนวน/ลำดับขั้นมาจาก DOA

## §9 Microcopy (verbatim)
### toast
- `ไม่มีการแจ้งเตือนใหม่`
- `แบบเอกสารนี้ยังไม่เปิดใช้งาน`
- `แก้ไขได้เฉพาะร่างของตัวเอง`
- `กรุณากรอกข้อมูลให้ครบถ้วน`
- `กรุณากรอกข้อมูลให้ครบถ้วน`
- `บันทึกร่างแล้ว ·`
- `กรุณากรอกข้อมูลให้ครบถ้วน`
- `ส่งอนุมัติแล้ว ·`
- `ส่งออก`
- `สลับเป็น`
- `แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง`
- ประกอบ: `ส่งกลับเป็นร่างแล้ว · {เลขที่}` · `ยกเลิกเอกสารแล้ว · {เลขที่}` · `อนุมัติ / รับทราบเรียบร้อย · {เลขที่}` · `ส่งต่อขั้นถัดไปแล้ว · {เลขที่}` · `บันทึกร่างแล้ว · {เลขที่}` · `ส่งอนุมัติแล้ว · {เลขที่}`
### ปุ่ม / placeholder / label
`Business Development` · `กลับไปกรอกต่อ` · `ดาวน์โหลด PDF` · `ถัดไป` · `ทิ้งข้อมูล` · `บันทึกแบบร่าง` · `ปิด` · `พิมพ์` · `ยกเลิก` · `ยกเลิกเอกสาร` · `ย้อนกลับ` · `รีเซ็ต` · `วันนี้` · `สร้างบันทึก` · `ส่งอนุมัติ` · `ส่งออก CSV` · `แก้ไข`

`ค้นหาเลขที่ / โครงการ / ผู้จัดทำ` · `ไม่บังคับ` · aria: `เดือนก่อน` · `เดือนถัดไป` · `แสดงต่อหน้า`
### ข้อความอื่น (จากโค้ด)
- (ขั้น
- [Lucide] All CDNs failed. Icons จะไม่แสดง but UI ยังใช้งานได้
- ]); if (canCancel(r)) items.push(['x-circle', 'ยกเลิกเอกสาร',
- ]]; if (isOwner(r) && r.status === 'draft') items.unshift(['pencil', 'แก้ไข',
- showToast('ไม่มีการแจ้งเตือนใหม่','info')
- · อนุมัติแล้ว ล็อกแก้ไข
- ก.ค.
- ก.พ.
- ก.ย.
- กรกฎาคม
- กรรมการผู้จัดการ
- กรอกข้อมูลโครงการ เลือกเหตุผลที่ไม่ดำเนินการต่อ แล้วสรุปการปิดโครงการ
- กระทบแผนงานหลัก
- กรุณากรอก
- กรุณากรอกข้อมูลให้ครบถ้วน
- กันยายน
- กำลังเปิดหน้าต่างพิมพ์ ·
- กิตติพัฒน์ ทดลองงาน
- กุมภาพันธ์
- ขนาดตลาดในพื้นที่เป้าหมายต่ำกว่าประมาณการร้อยละ 30
- ขั้นตอนที่ 4: คัดกรองและประเมินเบื้องต้น
- ขั้นตอนที่ยุติ
- ขั้นทดสอบ
- ขาดหลักฐานอ้างอิง
- ข้อ
- ข้อจำกัดด้านกฎหมาย
- ข้อจำกัดด้านทรัพยากร
- ข้อมูลต้นทุนและความต้องการยังไม่ครบ
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลหลักบันทึกการไม่ดำเนินโครงการ
- ข้อมูลหลักบันทึกการไม่ดำเนินโครงการต่อ
- ข้อมูลไม่เพียงพอ
- ข้อเสนอให้ติดตามในอนาคต
- ข้าม
- คน
- คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
- ควรระบุเงื่อนไขที่จะพิจารณาใหม่
- ควรสำรวจตลาดเบื้องต้นก่อนจัดทำประมาณการ
- ความเสี่ยงด้านการดำเนินงานอยู่ระดับสูงมาก
- ความเสี่ยงสูง
- ความเห็นฝ่ายกฎหมาย
- ความเห็นฝ่ายกฎหมาย.pdf
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค่าเริ่มต้นจากสายอนุมัติและผังองค์กร
- ค้นหา...
- ค้นหาเลขที่ / โครงการ / ผู้จัดทำ
- งานหลักล่าช้า
- จัดทำครั้งแรก
- จัดเก็บที่ไหน อย่างไร
- จัดเก็บในระบบเอกสารฝ่ายพัฒนาธุรกิจ แฟ้มโครงการที่ปิดแล้ว
- ชนิดไฟล์ไม่รองรับ
- ชยพล ตั้งระบบ
- ชื่อ
- ชื่อฟังก์ชัน
- ชื่อโครงการ
- ชื่อโครงการที่ไม่ดำเนินการต่อ
- ดาวน์โหลด PDF
- ต.ค.
- ตรวจสอบและยืนยัน
- ตรวจสอบแล้ว
- ตลาดไม่น่าสนใจ
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตัดสินใจไม่ได้ตามกำหนด
- ตำแหน่ง
- ติดตามเงื่อนไขในอนาคต
- ติดตามเมื่อผู้ร่วมทุนยืนยันแผนลงทุน
- ตุลาคม
- ต้นทุนก่อสร้างลดลงร้อยละ 15
- ต้อง
- ต้องขอใบอนุญาตที่ยังไม่มีแนวทางชัดเจน
- ต้องระบุ — ติดตามอะไร เมื่อไร
- ต้องระบุเมื่อสถานะเป็น "ติดตามเงื่อนไขในอนาคต"
- ถึง
- ถ้ามี
- ทบทวนผลสำรวจตลาดในไตรมาส 2 ปี 2570
- ทบทวนเมื่อมีแนวทางใบอนุญาตจากหน่วยงานรัฐ
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ทีมโครงการไม่เพียงพอในปีนี้
- ทุกฝ่าย
- ทุกสถานะ
- ทุกสถานะการปิด
- ธ.ค.
- ธันวาคม
- ธีรพงษ์ สมมติชื่อ
- นภัสสร ตัวอย่างดี
- บทเรียนที่ได้รับ
- บริษัท ตัวอย่าง จำกัด (มหาชน)
- บริษัท ตัวอย่าง จำกัด (มหาชน) และบริษัทในเครือ
- บริษัททบทวนกลยุทธ์ใหม่
- บันทึกการประชุมคัดกรอง
- บันทึกซ้ำ
- บันทึกซ้ำ — ใช้ PCL-2569-0004
- บันทึกผิดโครงการ
- บันทึกร่างแล้ว ·
- บันทึกเหตุผลและปิดโครงการที่ไม่ดำเนินการต่อ
- ประวัติ
- ประวัติ (append-only)
- ปิด
- ปิดโครงการและจัดเก็บเอกสารครบ
- ปิดโครงการแล้ว
- ปิดโครงการแล้ว รอจัดเก็บเอกสารให้ครบ
- ผลกระทบ
- ผลการคัดกรองไม่ผ่านเกณฑ์ตามเหตุผลที่เลือก จึงไม่ดำเนินโครงการต่อ
- ผลตอบแทนต่ำกว่าเกณฑ์
- ผลตอบแทนไม่เพียงพอ
- ผลวิเคราะห์ความคุ้มค่า
- ผลวิเคราะห์ความคุ้มค่า.xlsx
- ผลสำรวจตลาดรอบถัดไปดีขึ้น
- ผู้จัดการฝ่ายพัฒนาธุรกิจ
- ผู้จัดการฝ่ายวิศวกรรม
- ผู้จัดทำ
- ผู้ตรวจสอบ
- ผู้บริหาร
- ผู้รับผิดชอบ
- ผู้ร่วมทุนขอเลื่อนการตัดสินใจไม่มีกำหนด
- ผู้ร่วมทุนยืนยันแผนลงทุน
- ผู้ส่ง
- ผู้อนุมัติ / รับทราบ
- ผู้เชี่ยวชาญด้านพัฒนาธุรกิจ
- ฝ่าย
- ฝ่ายพัฒนาธุรกิจ
- ฝ่ายวิศวกรรม
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
- มีทีมว่างในปีถัดไป
- มีนาคม
- มีพันธมิตรร่วมรับความเสี่ยง
- ยกเลิก
- ยกเลิกเอกสาร
- ยกเลิกเอกสารแล้ว ·
- ยังไม่มีข้อมูล
- ยังไม่มีบันทึกการไม่ดำเนินโครงการต่อ
- ยังไม่ระบุสถานะการปิด
- ยังไม่ส่ง
- ย้อนกลับ
- รอขั้นก่อนหน้า
- รองกรรมการผู้จัดการ
- รอจัดเก็บเอกสาร
- รอผล
- รอพิจารณา
- รออนุมัติ
- ระบุเหตุผลอื่น
- ระยะคืนทุนเกิน 7 ปี เกินเกณฑ์ที่บริษัทกำหนด
- รายการ
- รายงานสำรวจตลาด · ผลวิเคราะห์ความคุ้มค่า
- รายงานสำรวจตลาด ก.ย. 2569
- รายงานสำรวจตลาด.pdf
- รายละเอียด
- รายละเอียดประกอบ
- รายได้ไม่ถึงเป้า
- ร่าง
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ลายเซ็น / อนุมัติ
- ลำดับการอนุมัติ
- ล้างตัวกรอง
- วันที่
- วันที่ ........./........./.........
- วันที่มีมติไม่ดำเนินการต่อ
- วิศวกรโครงการ
- ศิริพร ตัวแทนดี
- ส.ค.
- สถานะการปิดโครงการ
- สถานะเอกสาร
- สรุปสั้น ๆ ว่าทำไมไม่ดำเนินการต่อ
- สรุปเหตุผล
- สร้าง PDF
- สร้างบันทึก
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างโดย
- สลับเป็น
- สำรวจความต้องการอีกครั้งปี 2570
- สิงหาคม
- สิ่งที่ควรทำต่างไปในโครงการถัดไป
- ส่งกลับเป็นร่างแล้ว ·
- ส่งต่อขั้นถัดไปแล้ว ·
- ส่งบันทึกการไม่ดำเนินโครงการต่อ?
- ส่งอนุมัติ
- ส่งอนุมัติแล้ว ·
- ส่งออก
- ส่งแล้วแก้ไขไม่ได้ — ถ้าไม่ผ่านการพิจารณา จะกลับมาเป็นร่างเลขเดิม
- ส่งในระบบ
- หนังสือแจ้งจากผู้ร่วมทุน
- หน่วยงานรัฐออกแนวทางชัดเจน
- หลักฐานอ้างอิง
- อนุมัติ
- อนุมัติ / รับทราบ
- อนุมัติ / รับทราบเรียบร้อย ·
- อนุมัติ / รับทราบแล้ว
- อนุมัติแล้ว
- อรุณี ทดสอบระบบ
- อา
- เก็บไว้พิจารณาใหม่ — ต้องระบุข้อเสนอให้ติดตาม
- เงื่อนไขที่จะพิจารณาใหม่
- เจ้าหน้าที่ประสานงานโครงการ
- เช่น ขั้นตอนที่ 4: คัดกรองและประเมินเบื้องต้น
- เช่น รายงานสำรวจตลาด
- เดือนถัดไป
- เด้งกลับบน
- เพิ่มเติม
- เม.ย.
- เมษายน
- เริ่มโครงการไม่ได้
- เลขที่
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือก "เหตุผลอื่น" ต้องระบุว่าเหตุผลอื่นคืออะไร · แถวที่เลือก "ใช่" ต้องกรอกรายละเอียดประกอบ
- เลือก "ใช่" อย่างน้อย 1 เหตุผล
- เลือกตอนส่ง
- เลือกประเทศ
- เลือกผู้พิจารณา
- เลือกผู้รับผิดชอบ
- เลือกวันที่
- เลือกวันที่มีมติ
- เหตุผลที่ยกเลิก
- เหตุผลที่เลือก
- เหตุผลประกอบยังไม่ชัดเจน
- เหตุผลประกอบยังไม่ชัดเจน — แนบผลสำรวจตลาดเพิ่ม
- เหตุผลหลัก
- เหตุผลหลักที่เลือก
- เหตุผลอื่น
- เอกสารที่ใช้ประกอบการตัดสินใจ
- เอกสารแนบ
- แก้ไขร่าง
- แก้ไขล่าสุด
- แก้ไขเอกสาร
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งผู้จัดทำว่าต้องแก้อะไร
- แถวที่เลือก "ใช่" ต้องกรอกรายละเอียดประกอบ
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แนวทางจัดเก็บเอกสาร
- แบบฟอร์มบันทึกเหตุผลการไม่ดำเนินโครงการต่อ
- แบบฟอร์มประเมินความเสี่ยง
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- แผนกลยุทธ์ 2568–2572
- แผนอัตรากำลัง 2569
- แสดงต่อหน้า
- โครงการกลับมาดำเนินการต่อ
- โครงการท่าเรือขนถ่ายสินค้า
- โครงการพัฒนาที่ดินชานเมือง
- โครงการพื้นที่เช่าในศูนย์การค้า
- โครงการฟาร์มอัจฉริยะ
- โครงการร่วมทุนโรงงานบรรจุภัณฑ์
- โครงการร้านกาแฟในอาคารสำนักงาน
- โครงการศูนย์กระจายสินค้าภาคตะวันออก
- โครงการสถานีชาร์จรถไฟฟ้า
- โครงการห้องเย็นภาคเหนือ
- โครงการแอปสมาชิกสะสมแต้ม
- โครงการโซลาร์รูฟท็อปสำหรับลูกค้าอุตสาหกรรม
- โครงการโรงแรมขนาดเล็ก
- ใช่
- ใช้ทรัพยากรผิดทิศทาง
- ใช้ในขั้นตอน
- ได้ข้อมูลครบภายในไตรมาสถัดไป
- ไฟล์
- ไม่ผ่านการตรวจสอบ
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่มีผู้ร่วมลงทุน
- ไม่ยกเลิก
- ไม่สอดคล้องกับกลยุทธ์
- ไม่สอดคล้องกับแผนกลยุทธ์ 5 ปีของบริษัท
- ไม่อนุมัติ
- ไม่ใช่
- — คุณเป็นผู้พิจารณาใบนี้
- — ส่งกลับเป็นร่าง
- — ส่งกลับเป็นร่าง (ขั้น

## §10 Data Binding & BACKEND anchors
| จุดในโค้ด | API (02_API) |
|---|---|
| `listRows()` `RECS.filter(canSee)` | API-01 |
| `openView()` | API-02 |
| `persist()` (+ `ENG-DOC-NUM` ครั้งแรก) | API-03 / API-04 |
| `openSubmit()` `resolveDoa()` (DOA-ENGINE-HOOK) | API-05 |
| `confirmSubmit()` | API-06 |
| `confirmApprove()` | API-07 approve |
| `confirmReason()` reject | API-07 reject |
| `confirmReason()` cancel | API-08 |
| `docPrintData()` + `tplRender()` + `PCL_TPL` · `genPdf()` | API-09 (server render template เดียวกัน · 2 หน้า) |
| `chunkSigns()` · `DECISION_WORDS` / `wordsOf()` | ตารางลงชื่อ PDF = ผู้จัดทำ + ขั้นใน `approval_chain` (จำนวนตาม DOA) · คำตัดสินตาม role (print_config) |
| `CLOSURE_CFG` · `stOf()` · `isFollow()` | ProjectClosure config (reason_types · closure_statuses) — FN-01/02 |
| `validateMain()` · `setSel()` | FN-01 · FN-02 · VR-01..05 |
| `exportCSV()` | API-10 |
| `pickFiles()` `gateFiles()` | API-11 |
markers: ENG-DOC-NUM, DOA-ENGINE-HOOK, ENG-DOC-NUM, ENG-NOTIFY, DOA-ENGINE-HOOK, ENG-DOC-NUM, ENG-NOTIFY

## §11 Traceability + Drift Log
| Brief | FRD | HTML |
|---|---|---|
| §4 P-01 | 01 P-01 · API-01/10 | `renderPage()` |
| §4 P-02 | 01 P-02 · API-03/04/11 · BR-01..08 | `renderWizard()` |
| §4 P-03 | 01 P-03 · API-02/05..09 | `renderViewDrawer()` |
| §8 | 05 §5.2 state · LD-01/02 | `DOC_ST` · `curStep()` |
| Drift | ชนิด | ข้อเสนอ |
|---|---|---|
| D-01 | prototype-only: `__QA__` · `switchPersona()` · `S.sim` · mock `EMP`/`RECS` | ระบบจริงไม่ต้องมี |
| D-02 | prototype ถือ `CLOSURE_CFG` เป็น const · ระบบจริงอ่าน ProjectClosure config (FRD BR-01/06) | dev ทำตาม FRD |

## §12 Diff จากเวอร์ชันก่อน
— ไม่มีใน HTML นี้ (เวอร์ชันแรก)

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- ช่องอ้างอิงโครงการ (FM-BDM-01) / ผลคัดกรอง (FM-BDM-03) เมื่อลูกค้ายืนยัน OQ-05
- หน้าตั้งค่า ProjectClosure (Config Layout B) · รายงานเหตุผล No-Go · เตือนเมื่อถึงเงื่อนไขพิจารณาใหม่
