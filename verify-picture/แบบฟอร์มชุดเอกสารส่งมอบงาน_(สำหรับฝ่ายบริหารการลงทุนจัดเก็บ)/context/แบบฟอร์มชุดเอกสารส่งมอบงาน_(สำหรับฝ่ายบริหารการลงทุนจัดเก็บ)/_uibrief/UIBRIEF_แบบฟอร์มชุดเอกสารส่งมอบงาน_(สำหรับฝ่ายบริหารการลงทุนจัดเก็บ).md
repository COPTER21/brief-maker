# UI_BRIEF — F-TMP-008 แบบฟอร์มชุดเอกสารส่งมอบงาน (สำหรับฝ่ายบริหารการลงทุนจัดเก็บ) (AS-BUILT)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| HTML (source of truth) | `feature.html` · html-generator-v9.4 · archetype `Q-form` (`<meta name="cube-archetype">`) · audit FAIL 0 · e2e 21/21 (verify บน cloud container — เครื่อง user NO-BROWSER) |
| FRD | FRD_F-TMP-008_Pack v1.0 (FULL) · DECISIONS.lock 17 มติ (DEC-01..17 · AI-DEFAULT 11) |
| Prototype-only | `window.__QA__` · ตัวสลับผู้ใช้ `switchPersona()` · `S.sim` / `commitRejected()` · `EMP`/`RECS` mock → ไม่ต้องสร้างในระบบจริง (Drift Log D-01) |
| Drift | 0 business drift · 2 prototype-only (§11) |

## §1 Design Tokens AS-BUILT
CI Warm Light (html-generator-v9) · font Satoshi + Noto Sans Thai (หน้าจอ) · Sarabun (PDF) · ผลการรับมอบ: `pill-success` (รับมอบครบถ้วน) · `pill-warning` (รับมอบแบบมีเงื่อนไข) · `pill-danger` (ยังไม่รับมอบ) · ความครบถ้วน: `pill-success/pill-danger/pill-warning` · ได้รับแล้ว: `pill-success/pill-danger`
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
| `#/handover-investment` | P-01 รายการ (default) | `applyRoute()` · `renderPage()` |
| `#/handover-investment/create` | P-02 สร้าง | `startWizard()` |
| `#/handover-investment/edit/:id` | P-02 แก้ร่าง (เจ้าของ · draft) | `startWizard()` |
| `#/handover-investment/view/:id` | P-03 ดู (เฉพาะ `canSee`) | `openView()` · `showDrawer()` |
refresh-safe ผ่าน `hashchange` → `applyRoute()` · route ใบไม่มีสิทธิ์ = ไม่เปิด drawer

## §3 Layout Shell
`.sidebar` โมดูล Business Development › รับมอบงาน (บริหารการลงทุน) + badge `#sbBadge` (= รอฉันพิจารณา) · `.shell-bar` breadcrumb Core › Business Development › รับมอบงาน (บริหารการลงทุน) · user chip (icon คน · `toggleUserMenu()`) + `.user-menu` สลับผู้ใช้ (prototype) · `#page-content`

## §4 Page Anatomy
### P-01 รายการ — `renderPage()`
`.ph` (ชื่อ + `.ph-en` + `.ph-badge` ×≤3: รายการ · เปิดอยู่ · รอฉันพิจารณา — ค่า 0 ไม่แสดง · ไม่มี stat cards U1) · ปุ่ม `exportCSV()` / `#btnCreate` → `startWizard()` · `.filter-bar` (`#fq` `onQ()` · search select `fst` `ffin` (ผลการรับมอบ) `fdept` ผ่าน `initSearchSelect()` · รีเซ็ต `resetFilters()`) · `.table-wrap .table` คอลัมน์ เลขที่ · วันที่รับมอบ · ชื่อโครงการ (`.proj-cell` ตัดท้าย) · ผู้จัดทำ (`personInline()`) · เอกสาร · ค้างส่ง (`failCount()` · `.is-warn-t`) · ผลการรับมอบ `rsPill()` · สถานะเอกสาร `docPill()` · ลายเซ็น `renderSignProgress()` · ⋮ `openRowMenu()` · `pager()` + `setSize()` (10/25/50 · ค่าเริ่ม 25) `goPage()`
### P-02 สร้าง/แก้ — `renderWizard()` (drawer `.drawer.wide`)
`stepper()` 3 ขั้น (`STEPS`) · ขั้น 1 `wizMain()`: `hoForm()` (`[name=hproject]` ชื่อโครงการ · `[name=hsender]` ผู้ส่งมอบ (`#dlEmp`) · `[name=hreceiver]` ผู้รับมอบ · `.bedate` (key `hdate`) + `[name=htime]` วันที่ / เวลารับมอบ (`.dt-pair`) · `[name=hversion]` ฉบับชุดเอกสาร · `[name=hresult]` ผลการรับมอบ + `#hoResErr`) · `sumStrip()` (`#sumCnt` `#sumOpen` + legend ความครบถ้วน) · `.it-tbl` แถว `itemRow()` ช่อง `[name=id-i]` ชื่อเอกสาร · `[name=ic-i]` รหัส / ฉบับ · `[name=ir-i]` ได้รับแล้ว · `[name=ip-i]` ความครบถ้วน · `[name=is-i]` ประเด็นที่พบ · `[name=io-i]` ผู้รับผิดชอบแก้ไข · `.bedate` (key `iu{i}`) กำหนดส่งเพิ่มเติม (`bedateHTML()` min = วันที่รับมอบ) · ลบ `removeIt()` · `.add-row` `addIt()` · อัปเดตสด `setIt()` → `softSums()` · ขั้น 2 `wizFollow()`: `.fin-grid` (`[name=fissues]` · `[name=fpending]` · `.bedate` (key `fdate`) · `[name=fremark]` · `setFu()`) · `wizAttach()` `.upload-zone` `pickFiles()` · ขั้น 3 `wizReview()` (`hoBlock()` · `itemTable()` · `fuBlock()`) · footer `wizBack()` `wizNext()` `saveDraft()` `saveAndSubmit()`
### P-03 ดู — `renderViewDrawer()`
หัว `.dw-head` (เลขที่ · `docPill()` · sub 2 fact: ชื่อโครงการ · ค้างส่ง n) · ปุ่ม `#btnSubmitView` `openSubmit()` / `#btnApproveView` `openApprove()` / `openReject()` / `openCancel()` · `.drawer-tabs` `tabBtn()` → `renderDetailTab()` (`viewBanner()` · `hoBlock()` · `itemTable()` · `fuBlock()`) · `renderPdfTab()` (`.pdf-slot` iframe `.pdf-frame` srcdoc `docPdfDoc()` · `fitPdf()` · `genPdf()`) · `renderSignTab()` · `renderHistoryTab()`

## §5 Component Inventory
| Component | anchor | states |
|---|---|---|
| ข้อมูลการรับมอบ (แก้) | `hoForm()` `.ho-grid` | `.field.is-invalid` ต่อช่อง · ผลการรับมอบแดง + ข้อความเมื่อขัดกับตาราง (DEC-12) |
| ตารางตรวจรับ (แก้) | `.it-tbl` `itemRow()` | default · `.is-bad` ต่อช่อง · ความครบถ้วนแดงเมื่อ ไม่ได้รับ+ครบถ้วน · placeholder "(บังคับ)" เมื่อแถวไม่ผ่าน · ลบ (เมื่อ >1 แถว) |
| ตัวเลือกวัน พ.ศ. | `bedateHTML()` `.bedate` `.bd-pop` (portal) | ว่าง · เลือกแล้ว · `.bd-wrap.is-bad` · วันก่อน min ถูกปิด |
| ประเด็นค้าง | `.fin-grid` `fuBlock()` | `.field.is-invalid` (ประเด็นค้างเมื่อไม่ครบถ้วน · กำหนดการติดตาม < วันรับมอบ) |
| แถบสรุปสด | `.rk-strip.rv-strip` `sumStrip()` | อัปเดตแบบ soft (focus ไม่หลุด) |
| ตารางตรวจรับ (อ่าน) | `itemTable()` `.rk-view` | ว่าง = แผง "ไม่มีข้อมูล" (U23) · ไอคอนเตือนแถวไม่ผ่าน |
| คน | `empChip()` `personInline()` `nameInline()` `.emp-av` | วงกลมพื้นดำ + icon คน (U17) |
| progress ลายเซ็น | `renderSignProgress()` `.sign-prog` | ร่าง = — · n/N |
| slot ผู้พิจารณา | `.slot-row` + search select `slot{i}` | ค่าเริ่ม · `.is-invalid` |
| ปุ่ม busy | `busyLabel()` | loading "กำลังบันทึก…" · disabled |

## §6 Overlay Registry
| Overlay | anchor | ขนาด | ปิดด้วย |
|---|---|---|---|
| drawer สร้าง/แก้ | `#drawer` `.drawer-panel.wide` + `#drawerBackdrop` | wide | ปุ่ม/Esc/backdrop (`onmousedown` U25) · **กรอกค้าง → modal ทิ้งข้อมูล** (`closeDrawer()` dirty) |
| drawer ดู | `#drawer` `.drawer-panel` | 920 | ปุ่ม ปิด/Esc/backdrop |
| modal ส่ง/ตรวจสอบ-รับทราบ | `#modal` `.modal.is-lg` | lg | ยกเลิก · Esc · backdrop mousedown (`modalBackdropClick()` — มีข้อความค้างห้ามปิด) |
| modal ไม่ผ่าน/ยกเลิก/ทิ้ง | `#modal` | md | เช่นเดียวกัน |
| ปฏิทิน พ.ศ. | `.bd-pop` (portal `#overlay-root`) | 280px | เลือกวัน · คลิกนอก · Esc (ปิดแค่ปฏิทิน) |
| เมนู ⋮ | `.row-menu` (portal) | 180px | คลิกนอก · scroll |
| search list | `.ss-list.menu-fixed` | | Esc · คลิกนอก |
| toast | `#toast` `.toast` | | อัตโนมัติ |
| user menu | `.user-menu` | | คลิกนอก |

## §7 Interaction Spec
Esc chain: ปฏิทินเปิด → ปิดปฏิทินก่อน (capture · stopPropagation) → search list → modal → `closeModal()` → drawer → `closeDrawer()` · backdrop ปิดด้วย mousedown เท่านั้น · `addIt()` focus ช่องชื่อเอกสารของแถวใหม่ · เลือกได้รับแล้ว/ความครบถ้วน → วาดแถวใหม่ (placeholder บังคับ) + จำนวนค้างส่งอัปเดต · เปลี่ยนผลการรับมอบ/วันที่รับมอบ → `setHo()` วาดใหม่ (min ของกำหนดส่ง · ประเด็นค้างบังคับในขั้น 2) · ตรวจกฎ DEC-12..16 ตอนกดถัดไป (`validateMain()` · `validateFollow()`)

## §8 State-Driven UI Matrix
| status | pill | ปุ่มหัว (ผู้มีสิทธิ์) |
|---|---|---|
| draft | ร่าง `pill-muted` | เจ้าของ: ยกเลิก · แก้ไข · ส่งอนุมัติ |
| pending | รออนุมัติ `pill-warning` | ผู้พิจารณาขั้นปัจจุบัน: คำปฏิเสธของขั้น · คำอนุมัติของขั้น · อื่น (เจ้าของ/admin): ยกเลิกเอกสาร |
| approved | รับทราบแล้ว `pill-success` | — (ล็อก) · มีค้างส่ง = แถบเตือนในรายละเอียด |
| cancelled | ยกเลิก `pill-muted` | — |
ผลการรับมอบ (HandoverConfig.handover_results): รับมอบครบถ้วน `pill-success` · รับมอบแบบมีเงื่อนไข `pill-warning` · ยังไม่รับมอบ `pill-danger`
คำตัดสินผูก role (`DECISION_WORDS` → `wordsOf()`): role-line-manager = ตรวจสอบแล้ว/ไม่ผ่านการตรวจสอบ · role-mgr-bu = รับทราบผลการรับมอบ/ไม่รับทราบ · อื่น = อนุมัติ/ไม่อนุมัติ · จำนวน/ลำดับขั้นมาจาก DOA

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
- ประกอบ: `กลับเป็นร่างแล้ว · {เลขที่}` · `ยกเลิกเอกสารแล้ว · {เลขที่}` · `รับทราบผลการรับมอบเรียบร้อย · {เลขที่}` · `ส่งต่อขั้นถัดไปแล้ว · {เลขที่}` · `บันทึกร่างแล้ว · {เลขที่}` · `… · แจ้งผู้จัดทำ: เอกสารค้างส่ง {n} รายการ`
### ปุ่ม / placeholder / label
`Business Development` · `กลับไปกรอกต่อ` · `ดาวน์โหลด PDF` · `ถัดไป` · `ทิ้งข้อมูล` · `บันทึกแบบร่าง` · `ปิด` · `พิมพ์` · `ยกเลิก` · `ยกเลิกเอกสาร` · `ย้อนกลับ` · `รีเซ็ต` · `วันนี้` · `สร้างบันทึก` · `ส่งอนุมัติ` · `ส่งออก CSV` · `เพิ่มเอกสาร` · `แก้ไข`

`ค้นหาเลขที่ / โครงการ / ผู้จัดทำ / ชื่อเอกสาร` · `ชม:นาที เช่น 10:30` · `ชื่อผู้รับมอบ` · `ชื่อผู้ส่งมอบ` · `ชื่อเอกสาร` · `ชื่อโครงการที่ส่งมอบ` · `รหัส / ฉบับ` · `เช่น ชุดส่งมอบ ฉบับ 1` · `ไม่บังคับ` · aria: `ความครบถ้วน` · `ชื่อเอกสาร` · `ประเด็นที่พบ` · `ผลการรับมอบ` · `ผู้รับผิดชอบแก้ไข` · `รหัส / ฉบับ` · `เดือนก่อน` · `เดือนถัดไป` · `เวลารับมอบ` · `แสดงต่อหน้า` · `ได้รับแล้ว`
### ข้อความอื่น (จากโค้ด)
- (ขั้น
- Due_Diligence_ฉบับ2.pdf
- FIN-PRJ-01 / ฉบับ 3
- LEG-JV-01 / ฉบับ 1
- [Lucide] All CDNs failed. Icons จะไม่แสดง but UI ยังใช้งานได้
- ]); if (canCancel(r)) items.push(['x-circle', 'ยกเลิกเอกสาร',
- ]]; if (isOwner(r) && r.status === 'draft') items.unshift(['pencil', 'แก้ไข',
- showToast('ไม่มีการแจ้งเตือนใหม่','info')
- · รับทราบแล้ว ล็อกแก้ไข
- · แจ้งผู้จัดทำ: เอกสารค้างส่ง
- ก.ค.
- ก.พ.
- ก.ย.
- กรกฎาคม
- กรรมการผู้จัดการ
- กรอกชื่อเอกสาร ได้รับแล้ว และความครบถ้วนให้ครบทุกรายการ
- กรอกเมื่อมีประเด็นค้างหรือข้อตกลงเพิ่มเติม (ไม่บังคับ)
- กรุณากรอกข้อมูลให้ครบถ้วน
- กรุณาเลือกผลการรับมอบ
- กลับเป็นร่างแล้ว ·
- กันยายน
- กำลังเปิดหน้าต่างพิมพ์ ·
- กำหนดการติดตาม
- กำหนดส่งเพิ่มเติมต้องไม่ก่อนวันที่รับมอบ
- กิตติ ข้อมูลสมมติ
- กุมภาพันธ์
- ขั้นตอนที่ 6: จัดทำและส่งต่องานให้ฝ่ายบริหารการลงทุน
- ขั้นทดสอบ
- ข้อมูลการรับมอบ
- ข้อมูลการรับมอบและผลการตรวจรับ
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้าม
- คน
- ครบถ้วน
- คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
- ความครบถ้วน
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค่าเริ่มต้นจากสายอนุมัติและผังองค์กร
- ค้นหา...
- ค้นหาเลขที่ / โครงการ / ผู้จัดทำ / ชื่อเอกสาร
- ค้างส่ง
- จัดทำครั้งแรก
- จัดเก็บต้นฉบับที่ตู้เอกสารฝ่ายบริหารการลงทุน
- จำนวนเอกสาร
- ชนิดไฟล์ไม่รองรับ
- ชื่อ
- ชื่อผู้รับมอบ
- ชื่อผู้ส่งมอบ
- ชื่อฟังก์ชัน
- ชื่อโครงการ
- ชื่อโครงการที่ส่งมอบ
- ชุดส่งมอบ ฉบับ
- ดาวน์โหลด PDF
- ต.ค.
- ตรวจสอบและยืนยัน
- ตรวจสอบและรับทราบแล้ว
- ตรวจสอบแล้ว
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตำแหน่ง
- ตุลาคม
- ต้อง
- ต้องตรวจสอบเพิ่มเติม
- ถึง
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ทุกผลการรับมอบ
- ทุกฝ่าย
- ทุกสถานะเอกสาร
- ธ.ค.
- ธันวาคม
- ธีรพงษ์ ทดสอบระบบ
- นักวิเคราะห์การลงทุน
- บริษัท ตัวอย่าง จำกัด (มหาชน)
- บริษัท ตัวอย่าง จำกัด (มหาชน) และบริษัทในเครือ
- บันทึกการรับมอบเอกสาร ประเด็นค้าง และข้อตกลงการติดตาม
- บันทึกซ้ำ
- บันทึกซ้ำ — ใช้ HOI-2569-0004
- บันทึกร่างแล้ว ·
- ปกรณ์ ทดลองงาน
- ประมาณการทางการเงิน 5 ปี (ไฟล์ Excel)
- ประวัติ
- ประวัติ (append-only)
- ประเด็นค้างจากการรับมอบ
- ประเด็นค้างและการติดตาม
- ประเด็นค้างและข้อตกลงการติดตาม
- ประเด็นค้างไม่มีกำหนดส่ง
- ประเด็นค้างไม่มีกำหนดส่ง — ระบุผู้รับผิดชอบและวันที่ให้ครบ
- ประเด็นที่พบ
- ปิด
- ผลการตรวจรับเอกสาร
- ผลการตรวจรับไม่ตรงกับเอกสารที่ได้รับจริง
- ผลการรับมอบ
- ผลการรับมอบไม่ครบถ้วน — ต้องระบุประเด็นค้างจากการรับมอบ
- ผลการรับมอบไม่สอดคล้องกับตาราง
- ผู้จัดการฝ่ายบริหารการลงทุน
- ผู้จัดการฝ่ายพัฒนาธุรกิจ
- ผู้จัดทำ
- ผู้ตรวจสอบ
- ผู้บริหาร
- ผู้รับผิดชอบแก้ไข
- ผู้ส่ง
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
- ภาคผนวกด้านภาษีไม่ครบ ต้องยืนยันกับที่ปรึกษา
- ม.ค.
- มกราคม
- มณีรัตน์ สมมติชื่อ
- มาลัย ประสานงาน
- มิ.ย.
- มิถุนายน
- มี.ค.
- มีนาคม
- มีเอกสารไม่ได้รับหรือไม่ครบถ้วน — เลือก "รับมอบแบบมีเงื่อนไข" หรือ "ยังไม่รับมอบ"
- ยกเลิก
- ยกเลิกเอกสาร
- ยกเลิกเอกสารแล้ว ·
- ยังไม่มีข้อมูล
- ยังไม่มีบันทึกการรับมอบ
- ยังไม่รับมอบ
- ยังไม่ส่ง
- ยังไม่ได้รับสัญญาฉบับลงนามจากคู่สัญญา
- ย้อนกลับ
- รวมกับใบอื่นแล้ว
- รหัส / ฉบับ
- รอขั้นก่อนหน้า
- รอผล
- รอพิจารณา
- รออนุมัติ
- รอเอกสารที่ยังไม่ครบตามตาราง
- ระบุประเด็น (บังคับ)
- ระบุโครงการ ผู้ส่งมอบ ผู้รับมอบ และผลการรับมอบ
- รับทราบผลการรับมอบ
- รับทราบผลการรับมอบเรียบร้อย ·
- รับทราบแล้ว
- รับมอบครบถ้วน
- รับมอบแบบมีเงื่อนไข
- รายการ
- รายการที่ "ไม่ได้รับ" เลือกความครบถ้วนเป็น "ครบถ้วน" ไม่ได้
- รายการที่ไม่ได้รับหรือไม่ครบถ้วน ต้องระบุประเด็นที่พบ ผู้รับผิดชอบแก้ไข และกำหนดส่งเพิ่มเติม
- รายการเอกสารส่งมอบ.xlsx
- รายงานตรวจสอบสถานะกิจการ (Due Diligence)
- รายละเอียด
- ร่าง
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ลายเซ็น / อนุมัติ
- ลำดับการอนุมัติ
- ล้างตัวกรอง
- วันที่
- วันที่ ........./........./.........
- วันที่รับมอบ
- วิภา ทดลองใช้
- ศุภชัย ตัวอย่างดี
- ส.ค.
- สถานะเอกสาร
- สร้าง PDF
- สร้างบันทึก
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างโดย
- สลับเป็น
- สำเนาสัญญาร่วมทุนฉบับลงนาม
- สิงหาคม
- ส่งต่อขั้นถัดไปแล้ว ·
- ส่งบันทึกการรับมอบเอกสาร?
- ส่งอนุมัติ
- ส่งอนุมัติแล้ว ·
- ส่งออก
- ส่งแล้วแก้ไขไม่ได้ — ถ้าผู้พิจารณาไม่ผ่าน จะกลับมาเป็นร่างเลขเดิม
- ส่งในระบบ
- อนุมัติ
- อรุณี ผู้บริหารสมมติ
- อา
- เจ้าหน้าที่ธุรการการลงทุน
- เจ้าหน้าที่บริหารการลงทุน
- เจ้าหน้าที่พัฒนาธุรกิจ
- เช่น ชุดส่งมอบ ฉบับ 1
- เดือนถัดไป
- เด้งกลับบน
- เพิ่มเติม
- เม.ย.
- เมษายน
- เลขที่
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกตอนส่ง
- เลือกประเทศ
- เลือกผลการรับมอบ…
- เลือกผู้พิจารณา
- เลือกวันที่
- เลือกวันที่ (บังคับ)
- เลือก…
- เลื่อนการส่งมอบ
- เหตุผลที่ยกเลิก
- เอกสารที่ตรวจรับ
- เอกสารแนบ
- แก้ไขร่าง
- แก้ไขล่าสุด
- แก้ไขเอกสาร
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งผู้จัดทำว่าต้องปรับอะไร
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบฟอร์มชุดเอกสารส่งมอบงาน (สำหรับฝ่ายบริหารการลงทุนจัดเก็บ)
- แบบฟอร์มบทสรุปผู้บริหารและบันทึกการลงทุน
- แบบฟอร์มบันทึกการตรวจทานและอนุมัติภายใน
- แบบฟอร์มบันทึกภาพรวมและเริ่มต้นโครงการ
- แบบฟอร์มประเมินความเสี่ยง
- แบบฟอร์มสรุปผลการคัดกรองโครงการเบื้องต้น
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- แสดงต่อหน้า
- โครงการขยายโรงงานแปรรูปสมมติ
- โครงการร่วมทุนพลังงานแสงอาทิตย์
- โครงการศูนย์กระจายสินค้าภาคเหนือ
- โครงการโรงไฟฟ้าชีวมวลตัวอย่าง
- ใช้ในขั้นตอน
- ใบรับมอบเอกสาร_ลงนาม.pdf
- ใส่เอกสารที่ได้รับทีละรายการ — รายการที่ไม่ได้รับหรือไม่ครบถ้วนต้องระบุประเด็น ผู้รับผิดชอบ และกำหนดส่ง
- ได้รับ
- ได้รับแล้ว
- ไฟล์
- ไม่ครบถ้วน
- ไม่ผ่านการตรวจสอบ
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่ยกเลิก
- ไม่รับทราบ
- ไม่อนุมัติ
- ไม่ได้รับ
- — กลับเป็นร่าง
- — กลับเป็นร่าง (ขั้น
- — คุณเป็นผู้พิจารณาใบนี้

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
| `docPrintData()` + `tplRender()` + `HOI_TPL` · `genPdf()` | API-09 (server render template เดียวกัน · 2 หน้า) |
| `chunkSigns()` · `DECISION_WORDS` / `wordsOf()` | ตารางลงชื่อ PDF = ผู้จัดทำ + ขั้นใน `approval_chain` (จำนวนตาม DOA) · คำตัดสินตาม role (print_config) |
| `failCount()` · `rowFail()` · `rowClash()` · `completeClash()` · `HO_CFG` | FN-02 คำนวณฝั่ง server + HandoverConfig |
| `validateMain()` · `validateFollow()` | FN-01 · VR-01..08 |
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
| D-02 | prototype ถือ `HO_CFG` เป็น const · ระบบจริงอ่าน HandoverConfig (FRD BR-01) | dev ทำตาม FRD |

## §12 Diff จากเวอร์ชันก่อน
— ไม่มีใน HTML นี้ (เวอร์ชันแรก)

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- ช่องอ้างอิง FM-BDM-07 / โครงการ เมื่อลูกค้ายืนยัน OQ-05
- dashboard ติดตามเอกสารค้างส่งข้ามใบ · แจ้งเตือนก่อนถึงกำหนดส่ง
