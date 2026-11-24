# UI_BRIEF — F-TMP-005 แบบฟอร์มบทสรุปผู้บริหารและบันทึกการลงทุน (AS-BUILT)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| HTML (source of truth) | `feature.html` · html-generator-v9.4 · archetype `Q-form` (`<meta name="cube-archetype">`) · audit FAIL 0 · e2e 21/21 (verify บน cloud container — เครื่อง user NO-BROWSER) |
| FRD | FRD_F-TMP-005_Pack v1.0 (FULL) · DECISIONS.lock 16 มติ (DEC-01..16 · AI-DEFAULT 11) |
| Prototype-only | `window.__QA__` · ตัวสลับผู้ใช้ `switchPersona()` · `S.sim` / `commitRejected()` · `EMP`/`RECS` mock → ไม่ต้องสร้างในระบบจริง (Drift Log D-01) |
| Drift | 0 business drift · 2 prototype-only (§11) |

## §1 Design Tokens AS-BUILT
CI Warm Light (html-generator-v9) · font Satoshi + Noto Sans Thai (หน้าจอ) · Sarabun (PDF) · สถานะเงื่อนไข: pill `pill-muted` (ยังไม่เริ่ม) · `pill-info` (กำลังดำเนินการ) · `pill-success` (แล้วเสร็จ) · `pill-warning` (พักงาน) · แถบเตือน `.alert-row.is-warning` · ตัวเลือกวัน พ.ศ. `.bedate` + `.bd-pop` (Rule #114)
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
| `#/investment-memo` | P-01 รายการ (default) | `applyRoute()` · `renderPage()` |
| `#/investment-memo/create` | P-02 สร้าง | `startWizard()` |
| `#/investment-memo/edit/:id` | P-02 แก้ร่าง (เจ้าของ · draft) | `startWizard()` |
| `#/investment-memo/view/:id` | P-03 ดู (เฉพาะ `canSee`) | `openView()` · `showDrawer()` |
refresh-safe ผ่าน `hashchange` → `applyRoute()` · route ใบไม่มีสิทธิ์ = ไม่เปิด drawer

## §3 Layout Shell
`.sidebar` โมดูล Business Development › บทสรุปผู้บริหาร + badge `#sbBadge` (= รอฉันพิจารณา) · `.shell-bar` breadcrumb Core › Business Development › บทสรุปผู้บริหาร / การลงทุน · user chip (icon คน · `toggleUserMenu()`) + `.user-menu` สลับผู้ใช้ (prototype) · `#page-content`

## §4 Page Anatomy
### P-01 รายการ — `renderPage()`
`.ph` (ชื่อ + `.ph-en` + `.ph-badge` ×≤3: รายการ · เปิดอยู่ · รอฉันพิจารณา — ค่า 0 ไม่แสดง · ไม่มี stat cards U1) · ปุ่ม `exportCSV()` / `#btnCreate` → `startWizard()` · `.filter-bar` (`#fq` `onQ()` · search select `fst` `fcnd` `fdept` ผ่าน `initSearchSelect()` · รีเซ็ต `resetFilters()`) · `.table-wrap .table` คอลัมน์ เลขที่ · วันที่ · ผู้จัดทำ (`personInline()`) · ชื่อโครงการ (`.cell-trunc` ตัด … 1 บรรทัด U18) · วงเงิน (บาท) (`fmtAmt()` ชิดขวา) · เงื่อนไขประกอบ `condCell()` · สถานะเอกสาร `docPill()` · ลายเซ็น `renderSignProgress()` · ⋮ `openRowMenu()` · `pager()` + `setSize()` (10/25/50 · ค่าเริ่ม 25) `goPage()`
### P-02 สร้าง/แก้ — `renderWizard()` (drawer `.drawer.wide`)
`stepper()` 3 ขั้น (`STEPS`) · ขั้น 1 `wizMain()`: `sumStrip()` `.pc-strip` (`#sumAmt` `#sumMemo` `#sumCond`) · การ์ด `.wz-card` ① ข้อมูลสรุปโครงการ/การลงทุน `.pc-grid`: ช่อง id `in-` + key (`fieldTxt()` · name · type · amount (`fmtAmtInput()` ตอน blur)) · search select `pjProposer` (`setProposer()`) · ② บทสรุปผู้บริหาร `memoTxt()` textarea id `in-m_` + key 13 ช่องตาม `MEMO_TOPICS` (`setM()`) · ③ `.pc-tbl.is-cond` แถว `condRow()`: `[name=citem-i]` (`setCd()`) · search select `cdOwner{i}` (`setCdOwner()`) · `bedateHTML()` `cdDue{i}` → `pickDue{i}` (`ensureDueHandlers()`) · `[name=cst-i]` สถานะ (`setCdSt()`) · `[name=crem-i]` · ปุ่มลบแถว `removeCond()` · `#btnAddCond` `addCond()` · `.trip-err` ข้อความรวม · ขั้น 2 `wizAttach()` `.upload-zone` `pickFiles()` · ขั้น 3 `wizReview()` (`openWarn()` · `projectFields()` · `memoFields()` · `condTable()`) · footer `wizBack()` `wizNext()` `saveDraft()` `saveAndSubmit()`
### P-03 ดู — `renderViewDrawer()`
หัว `.dw-head` (เลขที่ · `docPill()` · sub ≤2 fact: วงเงิน · เงื่อนไขค้าง n/N) · ปุ่ม `#btnSubmitView` `openSubmit()` / `#btnApproveView` `openApprove()` / `openReject()` / `openCancel()` · `.drawer-tabs` `tabBtn()` → `renderDetailTab()` (`projectFields()` · `memoFields()` · `condTable()`) · `renderPdfTab()` (`.pdf-slot` iframe `.pdf-frame` srcdoc `docPdfDoc()` · `fitPdf()` · `genPdf()`) · `renderSignTab()` · `renderHistoryTab()`

## §5 Component Inventory
| Component | anchor | states |
|---|---|---|
| ตารางเงื่อนไข (แก้) | `.pc-tbl.is-cond` `condRow()` | แถวว่าง (ไม่บันทึก) · มีข้อมูล · `.is-bad` ที่ช่องรายการ/ผู้รับผิดชอบ/กำหนดเสร็จ/สถานะ · ปุ่มลบแถว |
| ตารางเงื่อนไข (อ่าน) | `condTable()` `.pc-view` | มีแถว · ว่าง = `emptyStateHTML` "ไม่มีรายการเอกสารและเงื่อนไขประกอบ" (U23) |
| pill สถานะเงื่อนไข | `condPill()` · `condCell()` | 4 ค่าจาก `COND_CFG` · รายการ: "ค้าง n/N" `pill-warning` / "ครบ N/N" `pill-success` / — |
| แถบเตือนเงื่อนไขค้าง | `openWarn()` `.alert-row.is-warning` | แสดงเมื่อมีเงื่อนไขยังไม่แล้วเสร็จ (review · modal ส่ง · modal อนุมัติ) |
| ช่องกรอก | `fieldTxt()` · `memoTxt()` `.field` | default · `.is-invalid` + `.field-error` · วงเงิน `.num` จัดรูปแบบตอน blur |
| ตัวเลือกวัน พ.ศ. | `bedateHTML()` `.bedate` `.bd-pop` | ว่าง (placeholder) · มีค่า `bdFmt()` |
| แถบสรุปสด | `.pc-strip` `sumStrip()` · `softSums()` | อัปเดตแบบ soft (focus ไม่หลุด) |
| คน | `empChip()` `personInline()` `.emp-av` | วงกลมพื้นดำ + icon คน (U17) |
| progress ลายเซ็น | `renderSignProgress()` `.sign-prog` | ร่าง = — · n/N |
| slot ผู้พิจารณา | `.slot-row` + search select `slot{i}` | ค่าเริ่ม · `.is-invalid` |
| สรุปในหน้าต่างอนุมัติ | `memoBrief()` | โครงการ · ข้อเสนอ · วงเงิน · ผลวิเคราะห์ทางการเงิน · ข้อเสนอแนะ |
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
Esc chain: ปฏิทิน พ.ศ. เปิด → ปิดปฏิทินก่อน (capture · stopPropagation) → search list → modal `closeModal()` → drawer `closeDrawer()` · backdrop ปิดด้วย mousedown เท่านั้น · เพิ่มรายการ → render + focus `[name=citem-n]` · ลบแถว → render ลำดับรันใหม่ · เลือกสถานะ → render (แล้วเสร็จ = ปลดบังคับผู้รับผิดชอบ/กำหนดเสร็จ) · พิมพ์ในตาราง/ช่อง → `softSums()` + ลบ `.is-bad`/`.is-invalid` ทีละช่อง · วงเงิน blur → จัดรูปแบบ #,##0.00

## §8 State-Driven UI Matrix
| status | pill | ปุ่มหัว (ผู้มีสิทธิ์) |
|---|---|---|
| draft | ร่าง `pill-muted` | เจ้าของ: ยกเลิก · แก้ไข · ส่งอนุมัติ |
| pending | รออนุมัติ `pill-warning` | ผู้พิจารณาขั้นปัจจุบัน: คำปฏิเสธของขั้น · คำอนุมัติของขั้น · อื่น (เจ้าของ/admin): ยกเลิกเอกสาร |
| approved | อนุมัติแล้ว `pill-success` | — (ล็อก) |
| cancelled | ยกเลิก `pill-muted` | — |
สถานะเงื่อนไข (`COND_CFG.statuses` = InvestmentMemo.condition_statuses): ยังไม่เริ่ม `pill-muted` · กำลังดำเนินการ `pill-info` · แล้วเสร็จ `pill-success` · พักงาน `pill-warning`
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
`Business Development` · `กลับไปกรอกต่อ` · `ดาวน์โหลด PDF` · `ถัดไป` · `ทิ้งข้อมูล` · `บันทึกแบบร่าง` · `ปิด` · `พิมพ์` · `ยกเลิก` · `ยกเลิกเอกสาร` · `ย้อนกลับ` · `รีเซ็ต` · `วันนี้` · `สร้างบันทึก` · `ส่งอนุมัติ` · `ส่งออก CSV` · `เพิ่มรายการ` · `แก้ไข`

`ค้นหาเลขที่ / โครงการ / ผู้จัดทำ` · `รายการเอกสาร / เงื่อนไข` · `หมายเหตุ` · `ไม่บังคับ` · aria: `เดือนก่อน` · `เดือนถัดไป` · `แสดงต่อหน้า`
### ข้อความอื่น (จากโค้ด)
- (ขั้น
- IRR ร้อยละ 12.4 · NPV 18.6 ล้านบาท · ระยะคืนทุน 6.2 ปี
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
- กรอกข้อมูลสรุปโครงการ บทสรุปผู้บริหาร 13 หัวข้อ และเอกสาร/เงื่อนไขประกอบ
- กรอบลงทุน
- กรุณากรอก
- กรุณากรอกข้อมูลให้ครบถ้วน
- กรุณาระบุวงเงินเป็นตัวเลขตั้งแต่ 0 ขึ้นไป
- กันยายน
- กำลังดำเนินการ
- กำลังเปิดหน้าต่างพิมพ์ ·
- กิตติพัฒน์ ทดลองงาน
- กุมภาพันธ์
- ขออนุมัติลงทุน
- ขั้นตอนถัดไป
- ขั้นตอนที่ 5: จัดทำเอกสารเสนอผู้บริหาร
- ขั้นทดสอบ
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลหลักบทสรุปผู้บริหาร
- ข้อมูลหลักบทสรุปผู้บริหารและบันทึกการลงทุน
- ข้อเสนอ / การตัดสินใจที่ต้องการ
- ข้อเสนอแนะของฝ่ายพัฒนาธุรกิจ
- ข้าม
- คน
- คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
- ควรระบุทางเลือกที่พิจารณาเพิ่ม
- ความต้องการในพื้นที่เป้าหมายเติบโตเฉลี่ยร้อยละ 8 ต่อปี
- ความเสี่ยงสำคัญและแนวทางจัดการ
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค่าเริ่มต้นจากสายอนุมัติและผังองค์กร
- ค้นหา...
- ค้นหาเลขที่ / โครงการ / ผู้จัดทำ
- ค้าง
- จัดทำครั้งแรก
- ชนิดไฟล์ไม่รองรับ
- ชยพล ตั้งระบบ
- ชื่อ
- ชื่อฟังก์ชัน
- ชื่อโครงการ
- ชื่อโครงการที่เสนอ
- ซื้อกิจการ (M&A)
- ดาวน์โหลด PDF
- ดำเนินงาน 14 เดือน แบ่ง 3 ระยะ
- ต.ค.
- ตรวจสอบและยืนยัน
- ตรวจสอบแล้ว
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตำแหน่ง
- ตุลาคม
- ต้นทุนก่อสร้างเพิ่มขึ้น — ทำสัญญาราคาคงที่
- ต้อง
- ถึง
- ทางเลือกที่พิจารณา
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ทุกฝ่าย
- ทุกสถานะ
- ทุกสถานะเงื่อนไข
- ธ.ค.
- ธนกร ทดลองใจ
- ธันวาคม
- ธีรพงษ์ สมมติชื่อ
- ธุรกิจใหม่ / ร่วมลงทุน
- ธุรกิจใหม่ / ลงทุนเอง
- นภัสสร ตัวอย่างดี
- นักวิเคราะห์การลงทุน
- นำเสนอคณะกรรมการบริษัทในการประชุมครั้งถัดไป
- บทสรุปโครงการ
- บริษัท ตัวอย่าง จำกัด (มหาชน)
- บริษัท ตัวอย่าง จำกัด (มหาชน) และบริษัทในเครือ
- บริษัทลงทุนผ่านบริษัทในเครือ
- บันทึกซ้ำ
- บันทึกซ้ำ — ใช้ IVM-2569-0004
- บันทึกผิดโครงการ
- บันทึกร่างแล้ว ·
- บาท
- บาท แบ่งจ่าย 3 งวด
- ประวัติ
- ประวัติ (append-only)
- ประเภทโครงการ / ธุรกรรม
- ปิด
- ผลการวิเคราะห์ทางการเงิน
- ผลวิเคราะห์ทางการเงินยังไม่ครบ
- ผลวิเคราะห์ทางการเงินยังไม่ครบ — เพิ่มกรณีอ่อนไหว
- ผลสำรวจตลาดสถานีชาร์จ.pdf
- ผู้จัดการฝ่ายการเงิน
- ผู้จัดการฝ่ายพัฒนาธุรกิจ
- ผู้จัดการฝ่ายวิศวกรรม
- ผู้จัดทำ
- ผู้ตรวจสอบ
- ผู้บริหาร
- ผู้ส่ง
- ผู้อนุมัติ / รับทราบ
- ผู้เชี่ยวชาญด้านพัฒนาธุรกิจ
- ผู้เสนอ / ผู้รับผิดชอบ
- ฝ่าย
- ฝ่ายการเงิน
- ฝ่ายพัฒนาธุรกิจ
- ฝ่ายวิศวกรรม
- พ.ค.
- พ.ย.
- พฤ
- พฤศจิกายน
- พฤษภาคม
- พักงาน
- พัฒนาอสังหาริมทรัพย์
- พิมพ์
- ม.ค.
- มกราคม
- มาลัย ประสานงาน
- มิ.ย.
- มิถุนายน
- มี.ค.
- มีนาคม
- มีเงื่อนไขค้าง
- มูลค่าหรือกรอบการลงทุน
- ยกเลิก
- ยกเลิกการเสนอโครงการ
- ยกเลิกเอกสาร
- ยกเลิกเอกสารแล้ว ·
- ยังไม่มีข้อมูล
- ยังไม่มีบทสรุปผู้บริหารและบันทึกการลงทุน
- ยังไม่ระบุวงเงิน
- ยังไม่ส่ง
- ยังไม่เริ่ม
- ย้อนกลับ
- รอขั้นก่อนหน้า
- รอผล
- รอพิจารณา
- รออนุมัติ
- รายการ
- รายงานการศึกษาความเป็นไปได้.pdf
- รายงานผลกระทบสิ่งแวดล้อม
- รายงานผลการศึกษาความเป็นไปได้
- รายละเอียด
- รูปแบบธุรกิจ / โครงสร้างธุรกรรม
- ร่วมทุน (Joint Venture)
- ร่าง
- ลงทุนระบบดิจิทัล
- ลงทุนสินทรัพย์ถาวร
- ลงทุนสินทรัพย์ถาวร / ขยายธุรกิจ
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ลายเซ็น / อนุมัติ
- ลำดับการอนุมัติ
- ล้างตัวกรอง
- วงเงิน (บาท)
- วงเงินหรือมูลค่าโดยประมาณ
- วงเงินหรือมูลค่าโดยประมาณ (บาท)
- วรรณา บัญชีดี
- วันที่
- วันที่ ........./........./.........
- วิศวกรโครงการ
- ศิริพร ตัวแทนดี
- ส.ค.
- สถานะเอกสาร
- สรุปสาระสำคัญของโครงการเพื่อเสนอผู้บริหารตัดสินใจ
- สร้าง PDF
- สร้างบันทึก
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างโดย
- สลับเป็น
- สอดคล้องกับแผนกลยุทธ์ 2568–2572 ด้านการขยายธุรกิจหลัก
- สิงหาคม
- ส่งกลับเป็นร่างแล้ว ·
- ส่งต่อขั้นถัดไปแล้ว ·
- ส่งบทสรุปผู้บริหารและบันทึกการลงทุน?
- ส่งอนุมัติ
- ส่งอนุมัติแล้ว ·
- ส่งออก
- ส่งแล้วแก้ไขไม่ได้ — ถ้าไม่ผ่านการพิจารณา จะกลับมาเป็นร่างเลขเดิม
- ส่งในระบบ
- อนุมัติ
- อนุมัติ / รับทราบ
- อนุมัติ / รับทราบเรียบร้อย ·
- อนุมัติ / รับทราบแล้ว
- อนุมัติแล้ว
- อรุณี ทดสอบระบบ
- อา
- เงื่อนไขก่อนอนุมัติยังไม่ชัดเจน
- เงื่อนไขค้าง
- เงื่อนไขประกอบ
- เงื่อนไขสำคัญก่อนอนุมัติ
- เงื่อนไขแล้วเสร็จทั้งหมด
- เจ้าหน้าที่ประสานงานโครงการ
- เช่น ลงทุนสินทรัพย์ถาวร / ร่วมทุน / ซื้อกิจการ
- เช่าระยะยาว
- เช่าแทนการลงทุนเอง (ต้นทุนระยะยาวสูงกว่า)
- เดือนถัดไป
- เด้งกลับบน
- เพิ่มรายการ
- เพิ่มเติม
- เม.ย.
- เมษายน
- เลขที่
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกตอนส่ง
- เลือกประเทศ
- เลือกผู้พิจารณา
- เลือกผู้รับผิดชอบ
- เลือกผู้เสนอ / ผู้รับผิดชอบ
- เลือกวันที่
- เหตุผลที่ยกเลิก
- เหตุผลเชิงกลยุทธ์
- เห็นควรอนุมัติภายใต้เงื่อนไขก่อนอนุมัติ
- เอกสารแนบ
- แก้ไขร่าง
- แก้ไขล่าสุด
- แก้ไขเอกสาร
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งผู้จัดทำว่าต้องแก้อะไร
- แถวที่กรอกต้องมีรายการเอกสาร / เงื่อนไข และสถานะ · สถานะที่ยังไม่ "แล้วเสร็จ" ต้องมีผู้รับผิดชอบและกำหนดเสร็จ
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบจำลองการเงิน.xlsx
- แบบฟอร์มบทสรุปผู้บริหารและบันทึกการลงทุน
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- แผนดำเนินงาน
- แล้วเสร็จ
- แสดงต่อหน้า
- โครงการ
- โครงการซื้อกิจการผู้จัดจำหน่ายท้องถิ่น
- โครงการท่าเรือขนถ่ายสินค้า
- โครงการพัฒนาที่ดินชานเมือง
- โครงการพื้นที่เช่าในศูนย์การค้า
- โครงการฟาร์มอัจฉริยะ
- โครงการร่วมทุนโรงงานบรรจุภัณฑ์
- โครงการศูนย์กระจายสินค้าภาคตะวันออก
- โครงการสถานีชาร์จรถไฟฟ้า
- โครงการห้องเย็นภาคเหนือ
- โครงการแอปสมาชิกสะสมแต้ม
- โครงการโซลาร์รูฟท็อปสำหรับลูกค้าอุตสาหกรรม
- โครงการโรงแรมขนาดเล็ก
- โอกาสทางธุรกิจและตลาด
- ใช้ในขั้นตอน
- ใบนี้ไม่ได้ระบุเอกสาร/เงื่อนไขประกอบ
- ได้รับใบอนุญาตก่อนเบิกจ่ายงวดแรก
- ไม่ผ่านการตรวจสอบ
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่มีรายการเงื่อนไข
- ไม่มีรายการเอกสารและเงื่อนไขประกอบ
- ไม่ยกเลิก
- ไม่อนุมัติ
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
| `docPrintData()` + `tplRender()` + `IVM_TPL` · `genPdf()` | API-09 (server render template เดียวกัน · 2 หน้า) |
| `chunkSigns()` · `DECISION_WORDS` / `wordsOf()` | ตารางลงชื่อ PDF = ผู้จัดทำ + ขั้นใน `approval_chain` (จำนวนตาม DOA) · คำตัดสินตาม role (print_config) |
| `COND_CFG` · `cstOf()` · `isDone()` · `openConds()` | InvestmentMemo config (condition_statuses) — FN-01/02 |
| `MOCK_DOA_RESOLVED` (amount → DOA กลาง) | FN-04 · TODO: DOA engine |
| `validateMain()` · `addCond()` · `removeCond()` | FN-01 · FN-02 · VR-01..05 |
| `exportCSV()` | API-10 |
| `pickFiles()` `gateFiles()` | API-11 |
markers: ENG-DOC-NUM, DOA-ENGINE-HOOK, TODO, ENG-DOC-NUM, ENG-NOTIFY, DOA-ENGINE-HOOK, ENG-DOC-NUM, ENG-NOTIFY

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
| D-02 | prototype ถือ `COND_CFG` / `MEMO_TOPICS` เป็น const · ระบบจริงอ่าน InvestmentMemo config (FRD BR-06) | dev ทำตาม FRD |

## §12 Diff จากเวอร์ชันก่อน
— ไม่มีใน HTML นี้ (เวอร์ชันแรก)

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- ช่องอ้างอิงโครงการ (FM-BDM-01) / ผลคัดกรอง (FM-BDM-03) / ส่งต่อ FM-BDM-06 เมื่อลูกค้ายืนยัน OQ-05
- หน้าตั้งค่า InvestmentMemo (Config Layout B) · ติดตาม/อัปเดตสถานะเงื่อนไขหลังอนุมัติ · เตือนเงื่อนไขใกล้กำหนด
