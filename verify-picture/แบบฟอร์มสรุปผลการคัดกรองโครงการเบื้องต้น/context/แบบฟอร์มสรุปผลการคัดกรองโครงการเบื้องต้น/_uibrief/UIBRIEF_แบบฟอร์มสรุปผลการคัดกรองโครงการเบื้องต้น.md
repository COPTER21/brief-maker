# UI_BRIEF — F-TMP-003 แบบฟอร์มสรุปผลการคัดกรองโครงการเบื้องต้น (AS-BUILT)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| HTML (source of truth) | `feature.html` · html-generator-v9.4 · archetype `Q-form` (`<meta name="cube-archetype">`) · audit FAIL 0 · e2e 21/21 (verify บน cloud container — เครื่อง user NO-BROWSER) |
| FRD | FRD_F-TMP-003_Pack v1.0 (FULL) · DECISIONS.lock 17 มติ (DEC-01..17 · AI-DEFAULT 11) |
| Prototype-only | `window.__QA__` · ตัวสลับผู้ใช้ `switchPersona()` · `S.sim` / `commitRejected()` · `EMP`/`RECS` mock → ไม่ต้องสร้างในระบบจริง (Drift Log D-01) |
| Drift | 0 business drift · 2 prototype-only (§11) |

## §1 Design Tokens AS-BUILT
CI Warm Light (html-generator-v9) · font Satoshi + Noto Sans Thai (หน้าจอ) · Sarabun (PDF) · ผลเสนอ/ผลการพิจารณา: pill `pill-success/pill-warning/pill-danger`
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
ค่าที่ใช้: `1`, `2`, `3`, `var(--z-backdrop)`, `var(--z-drawer)`, `var(--z-dropdown)`, `var(--z-modal)`, `var(--z-popover)`, `var(--z-shell)`, `var(--z-sticky)`, `var(--z-toast)`


## §2 Route Map
| Route | หน้า | handler |
|---|---|---|
| `#/project-screening` | P-01 รายการ (default) | `applyRoute()` · `renderPage()` |
| `#/project-screening/create` | P-02 สร้าง | `startWizard()` |
| `#/project-screening/edit/:id` | P-02 แก้ร่าง (เจ้าของ · draft) | `startWizard()` |
| `#/project-screening/view/:id` | P-03 ดู (เฉพาะ `canSee`) | `openView()` · `showDrawer()` |
refresh-safe ผ่าน `hashchange` → `applyRoute()` · route ใบไม่มีสิทธิ์ = ไม่เปิด drawer

## §3 Layout Shell
`.sidebar` โมดูล Business Development › คัดกรองโครงการ + badge `#sbBadge` (= รอฉันพิจารณา) · `.shell-bar` breadcrumb Core › Business Development › คัดกรองโครงการ · user chip (icon คน · `toggleUserMenu()`) + `.user-menu` สลับผู้ใช้ (prototype) · `#page-content`

## §4 Page Anatomy
### P-01 รายการ — `renderPage()`
`.ph` (ชื่อ + `.ph-en` + `.ph-badge` ×≤3: รายการ · เปิดอยู่ · รอฉันพิจารณา — ค่า 0 ไม่แสดง · ไม่มี stat cards U1) · ปุ่ม `exportCSV()` / `#btnCreate` → `startWizard()` · `.filter-bar` (`#fq` `onQ()` · search select `fst` `fdec` `fdept` ผ่าน `initSearchSelect()` · รีเซ็ต `resetFilters()`) · `.table-wrap .table` คอลัมน์ เลขที่ · วันที่ · ผู้จัดทำ (`personInline()`) · คะแนนรวม (`totalOf()`) · ผลเสนอจากคะแนน `recPill()` · ผลการพิจารณา `decPill()` · สถานะเอกสาร `docPill()` · ลายเซ็น `renderSignProgress()` · ⋮ `openRowMenu()` · `pager()` + `setSize()` (10/25/50 · ค่าเริ่ม 25) `goPage()`
### P-02 สร้าง/แก้ — `renderWizard()` (drawer `.drawer.wide`)
`stepper()` 3 ขั้น (`STEPS`) · ขั้น 1 `wizMain()`: `sumStrip()` (`#sumCnt` `#sumTotal` `#sumRec` + legend `SCREENING.bands`) · `.ck-tbl` แถว `critRow()` — เกณฑ์ประเมิน/น้ำหนัก อ่านอย่างเดียว · `[name=cs-i]` คะแนน (1-5) · `#cw-i` คะแนนถ่วงน้ำหนัก · `[name=cy-i]` เหตุผล / หลักฐาน · `[name=cr-i]` ความเสี่ยง / เงื่อนไข · แถว `.sc-total` (`#ckTotal` `#ckRec`) · การ์ดข้อสรุป `taField()` `[name=sm-strengths]` `[name=sm-concerns]` `[name=sm-info]` · `.track-card` ×3 `setDecision()` · `#mmWarn` เตือนผลขัดคะแนน · `[name=sm-cond]` + `#condReq` (ดาวขึ้นเมื่อ `condNeeded()`) · `[name=sm-next]` · อัปเดตสด `setCrit()` / `setSum()` → `softSums()` · ขั้น 2 `wizAttach()` `.upload-zone` `pickFiles()` · ขั้น 3 `wizReview()` (`critTable()` · `sumTable()`) · footer `wizBack()` `wizNext()` `saveDraft()` `saveAndSubmit()`
### P-03 ดู — `renderViewDrawer()`
หัว `.dw-head` (เลขที่ · `docPill()` · sub = คะแนนรวม · ผลการพิจารณา) · ปุ่ม `#btnSubmitView` `openSubmit()` / `#btnApproveView` `openApprove()` / `openReject()` / `openCancel()` · `.drawer-tabs` `tabBtn()` → `renderDetailTab()` (`viewBanner()` · `critTable()` · `sumTable()`) · `renderPdfTab()` (`.pdf-slot` iframe `.pdf-frame` srcdoc `docPdfDoc()` · `fitPdf()` · `genPdf()`) · `renderSignTab()` · `renderHistoryTab()`

## §5 Component Inventory
| Component | anchor | states |
|---|---|---|
| ตารางเกณฑ์ (แก้) | `.ck-tbl` `critRow()` | default · `.is-bad` ที่ select คะแนน · ถ่วงน้ำหนัก "—" จนให้คะแนน · ไม่มีเพิ่ม/ลบแถว (8 แถวคงที่) |
| แถวคะแนนรวม | `.sc-total` `#ckTotal` `#ckRec` | ว่าง (—) จนให้คะแนนครบ · pill ผลเสนอ success/warning/danger |
| แถบสรุปสด | `.rk-strip` `sumStrip()` | อัปเดตแบบ soft (focus ไม่หลุด) |
| ผลการพิจารณา | `.track-card` `setDecision()` | default · `.is-on` · `.field.is-invalid` (ไม่เลือก) |
| เตือนผลขัดคะแนน | `#mmWarn` `.rk-warn` | hidden · แสดงเมื่อ `mismatch()` |
| ช่องข้อสรุป | `taField()` `.field` | default · `.is-invalid` + `.field-error` |
| ตารางอ่าน | `critTable()` `sumTable()` `.rk-view` | ค่าว่าง = — |
| คน | `empChip()` `personInline()` `.emp-av` | วงกลมพื้นดำ + icon คน (U17) |
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
| เมนู ⋮ | `.row-menu` (portal) | 180px | คลิกนอก · scroll |
| search list | `.ss-list.menu-fixed` | | Esc · คลิกนอก |
| toast | `#toast` `.toast` | | อัตโนมัติ |
| user menu | `.user-menu` | | คลิกนอก |

## §7 Interaction Spec
Esc chain: search list เปิด → ปิด list ก่อน (stopPropagation) → modal → `closeModal()` → drawer → `closeDrawer()` · backdrop ปิดด้วย mousedown เท่านั้น (ลากจากข้างในไปปล่อยนอกไม่ปิด) · เลือกคะแนน → ถ่วงน้ำหนัก/คะแนนรวม/ผลเสนอ อัปเดตทันที (`softSums()`) · เลือกผลการพิจารณา → re-render การ์ด (`setDecision()`) · ผลขัดผลเสนอ → `#mmWarn` + `#condReq`

## §8 State-Driven UI Matrix
| status | pill | ปุ่มหัว (ผู้มีสิทธิ์) |
|---|---|---|
| draft | ร่าง `pill-muted` | เจ้าของ: ยกเลิก · แก้ไข · ส่งอนุมัติ |
| pending | รออนุมัติ `pill-warning` | ผู้พิจารณาขั้นปัจจุบัน: คำปฏิเสธของขั้น · คำอนุมัติของขั้น · อื่น (เจ้าของ/admin): ยกเลิกเอกสาร |
| approved | อนุมัติแล้ว `pill-success` | — (ล็อก) |
| cancelled | ยกเลิก `pill-muted` | — |
ผลเสนอจากคะแนน (`SCREENING.bands`): เสนอให้ดำเนินการต่อ `pill-success` (≥80) · ดำเนินการต่อแบบมีเงื่อนไข `pill-warning` (≥60) · ไม่เสนอให้ดำเนินการต่อ `pill-danger`
ผลการพิจารณา (`SCREENING.decisions`): ดำเนินการต่อ `pill-success` · ดำเนินการต่อแบบมีเงื่อนไข `pill-warning` · ไม่ดำเนินการต่อ `pill-danger`
คำตัดสินผูก role (`DECISION_WORDS` → `wordsOf()`): role-line-manager = ตรวจสอบแล้ว/ไม่ผ่านการตรวจสอบ · role-gm = อนุมัติ / รับทราบ/ไม่อนุมัติ · อื่น = อนุมัติ/ไม่อนุมัติ · จำนวน/ลำดับขั้นมาจาก DOA

## §9 Microcopy (verbatim)
### toast
- `ไม่มีการแจ้งเตือนใหม่`
- `แบบเอกสารนี้ยังไม่เปิดใช้งาน`
- `แก้ไขได้เฉพาะร่างของตัวเอง`
- `กรุณากรอกข้อมูลให้ครบถ้วน`
- `บันทึกร่างแล้ว ·`
- `กรอกข้อมูลให้ครบก่อนส่งอนุมัติ — ให้คะแนนครบ 8 เกณฑ์และสรุปผล`
- `ส่งอนุมัติแล้ว ·`
- `ส่งออก`
- `สลับเป็น`
- `แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง`
- ประกอบ: `ส่งกลับเป็นร่างแล้ว · {เลขที่}` · `ยกเลิกเอกสารแล้ว · {เลขที่}` · `อนุมัติ / รับทราบเรียบร้อย · {เลขที่}` · `ส่งต่อขั้นถัดไปแล้ว · {เลขที่}` · `บันทึกร่างแล้ว · {เลขที่}`
### ปุ่ม / placeholder / label
`Business Development` · `กลับไปกรอกต่อ` · `ดาวน์โหลด PDF` · `ถัดไป` · `ทิ้งข้อมูล` · `บันทึกแบบร่าง` · `ปิด` · `พิมพ์` · `ยกเลิก` · `ยกเลิกเอกสาร` · `ย้อนกลับ` · `รีเซ็ต` · `สร้างแบบสรุปผล` · `ส่งอนุมัติ` · `ส่งออก CSV` · `แก้ไข`

`ความเสี่ยง / เงื่อนไข` · `ค้นหาเลขที่ / ผู้จัดทำ / จุดเด่น / ข้อกังวล` · `เงื่อนไขก่อนเดินต่อ หรือเหตุผลที่ผลพิจารณาต่างจากคะแนน` · `เหตุผล / หลักฐาน` · `ไม่บังคับ` · aria: `ความเสี่ยง / เงื่อนไข ${esc(c.name)}` · `คะแนน (1-5) ${esc(c.name)}` · `เหตุผล / หลักฐาน ${esc(c.name)}` · `แสดงต่อหน้า`
### ข้อความอื่น (จากโค้ด)
- (ขั้น
- ) — บันทึกได้ แต่ต้องระบุเหตุผลในเงื่อนไข / ข้อสั่งการ
- + STEPH('clipboard-check', 'ข้อสรุปการคัดกรอง', 'สรุปผลจากการประเมิน แล้วเลือกผลการพิจารณา') +
- [Lucide] All CDNs failed. Icons จะไม่แสดง but UI ยังใช้งานได้
- ]); if (canCancel(r)) items.push(['x-circle', 'ยกเลิกเอกสาร',
- ]]; if (isOwner(r) && r.status === 'draft') items.unshift(['pencil', 'แก้ไข',
- showToast('ไม่มีการแจ้งเตือนใหม่','info')
- · อนุมัติแล้ว ล็อกแก้ไข
- ก.ค.
- ก.พ.
- ก.ย.
- กฎหมายและข้อกำกับ
- กรอกข้อมูลให้ครบก่อนส่งอนุมัติ — ให้คะแนนครบ 8 เกณฑ์และสรุปผล
- กรุณากรอกข้อมูลให้ครบถ้วน
- การประเมินและคัดกรองโครงการ
- กำลังเปิดหน้าต่างพิมพ์ ·
- กิตติพัฒน์ ทดลองงาน
- ขั้นตอนถัดไปที่เสนอ
- ขั้นตอนที่ 4: คัดกรองและประเมินเบื้องต้น
- ขั้นทดสอบ
- ข้อกังวลหรือประเด็นเสี่ยงสำคัญ
- ข้อกังวลหลัก
- ข้อมูลตลาดยังไม่ครบบางส่วน
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลที่ต้องจัดหาเพิ่ม
- ข้อมูลที่ยังขาด (ถ้ามี)
- ข้อมูลประกอบยังไม่ครบ
- ข้อมูลหลักแบบสรุปผล
- ข้อเสนอแนะขั้นตอนถัดไป
- ข้าม
- คน
- คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
- ความครบถ้วนของข้อมูล
- ความคุ้มค่าทางการเงิน
- ความสอดคล้องเชิงกลยุทธ์
- ความเป็นไปได้ในการดำเนินงาน
- ความเสี่ยงหลักควบคุมได้
- ความแข็งแรงของรูปแบบธุรกิจ
- คะแนนรวม
- คะแนนรวมถ่วงน้ำหนัก
- คะแนนไม่สอดคล้องกับหลักฐาน
- คัดกรองรวมกับใบอื่นแล้ว
- คืนทุนประมาณ 4 ปี
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค่าเริ่มต้นจากสายอนุมัติและผังองค์กร
- ค้นหา...
- ค้นหาเลขที่ / ผู้จัดทำ / จุดเด่น / ข้อกังวล
- จัดทำครั้งแรก
- จัดทำแผนธุรกิจและประเมินความเสี่ยงโดยละเอียด
- จัดหาข้อมูลเพิ่มเติม
- จุดเด่นของโครงการ
- จุดเด่นหลักของโครงการ
- ชนิดไฟล์ไม่รองรับ
- ชยพล ตั้งระบบ
- ชื่อ
- ดาวน์โหลด PDF
- ดำเนินการต่อ
- ดำเนินการต่อแบบมีเงื่อนไข
- ต.ค.
- ตรวจสอบและยืนยัน
- ตรวจสอบแล้ว
- ตลาดเติบโต · รายได้ประจำจากสัญญาบริการ
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตำแหน่ง
- ติดตามราคาวัสดุ
- ต้นทุนก่อสร้างอาจสูงกว่าประมาณการ
- ต้อง
- ต้องยืนยันต้นทุนก่อสร้าง
- ต้องระบุเงื่อนไข / ข้อสั่งการ ก่อนเดินต่อ
- ถึง
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ทำเลดี
- ทุกผลการพิจารณา
- ทุกฝ่าย
- ทุกสถานะ
- ธ.ค.
- ธีรพงษ์ สมมติชื่อ
- นภัสสร ตัวอย่างดี
- นักวิเคราะห์การลงทุน
- บริษัท ตัวอย่าง จำกัด (มหาชน)
- บริษัท ตัวอย่าง จำกัด (มหาชน) และบริษัทในเครือ
- บันทึกซ้ำ
- บันทึกซ้ำ — ใช้ SCR-2569-0004
- บันทึกร่างแล้ว ·
- ประมาณการทางการเงินเบื้องต้น.xlsx
- ประวัติ
- ประวัติ (append-only)
- ประเมินความเหมาะสมเชิงกลยุทธ์ เชิงพาณิชย์ การเงิน การดำเนินงาน และความเสี่ยง
- ปิด
- ผลการพิจารณา
- ผลการพิจารณาไม่ตรงกับคะแนน
- ผลการพิจารณาไม่ตรงกับคะแนน — ทบทวนคะแนนความคุ้มค่าทางการเงิน
- ผลการพิจารณาไม่ตรงกับผลเสนอจากคะแนน (
- ผลตอบแทนต่ำกว่าเกณฑ์ · ตลาดอิ่มตัว
- ผลตอบแทนสูง · พันธมิตรพร้อมลงทุนร่วม
- ผลสำรวจตลาด.pdf
- ผลสำรวจตลาดฉบับสมบูรณ์
- ผลเสนอจากคะแนน
- ผู้จัดการฝ่ายกลยุทธ์องค์กร
- ผู้จัดการฝ่ายพัฒนาธุรกิจ
- ผู้จัดทำ
- ผู้ตรวจสอบ
- ผู้บริหาร
- ผู้ส่ง
- ผู้อนุมัติ / รับทราบ
- ผู้เชี่ยวชาญด้านพัฒนาธุรกิจ
- ฝ่าย
- ฝ่ายกลยุทธ์องค์กร
- ฝ่ายพัฒนาธุรกิจ
- พ.ค.
- พ.ย.
- พิมพ์
- ม.ค.
- มาลัย ประสานงาน
- มิ.ย.
- มี.ค.
- มีทีมงานและพันธมิตรพร้อม
- ยกเลิก
- ยกเลิกเอกสาร
- ยกเลิกเอกสารแล้ว ·
- ยังไม่มีข้อมูล
- ยังไม่มีแบบสรุปผลการคัดกรอง
- ยังไม่ส่ง
- ยืนยันต้นทุนก่อสร้างกับผู้รับเหมาอย่างน้อย 2 ราย
- ยุติโครงการ — บันทึกเหตุผลใน FM-BDM-04
- ย้อนกลับ
- รอขั้นก่อนหน้า
- รองกรรมการผู้จัดการ
- รอผล
- รอพิจารณา
- รออนุมัติ
- ระดับความเสี่ยง
- ระยะเวลาก่อสร้างยาว
- รายการ
- รายละเอียด
- ร่าง
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ลายเซ็น / อนุมัติ
- ลำดับการอนุมัติ
- ล้างตัวกรอง
- วันที่
- วันที่ ........./........./.........
- ศักยภาพตลาด
- ศิริพร ตัวแทนดี
- ส.ค.
- สถานะ
- สถานะเอกสาร
- สรุปประชุมคัดกรองโครงการ.pdf
- สร้าง PDF
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างแบบสรุปผล
- สร้างโดย
- สลับเป็น
- สอดคล้องแผนขยายธุรกิจบริการ 3 ปี
- ส่งกลับเป็นร่างแล้ว ·
- ส่งต่อขั้นถัดไปแล้ว ·
- ส่งอนุมัติ
- ส่งอนุมัติแล้ว ·
- ส่งออก
- ส่งแบบสรุปผลการคัดกรอง?
- ส่งแล้วแก้ไขไม่ได้ — ถ้าผู้พิจารณาไม่อนุมัติ จะกลับมาเป็นร่างเลขเดิม
- ส่งในระบบ
- อนุมัติ
- อนุมัติ / รับทราบ
- อนุมัติ / รับทราบเรียบร้อย ·
- อนุมัติ / รับทราบแล้ว
- อนุมัติแล้ว
- อรุณี ทดสอบระบบ
- เกณฑ์
- เงื่อนไข / ข้อสั่งการ
- เจ้าหน้าที่ประสานงานโครงการ
- เด้งกลับบน
- เพิ่มเติม
- เม.ย.
- เลขที่
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกตอนส่ง
- เลือกประเทศ
- เลือกผู้พิจารณา
- เสนอให้ดำเนินการต่อ
- เหตุผลที่ยกเลิก
- เอกสารแนบ
- แก้ไขร่าง
- แก้ไขล่าสุด
- แก้ไขเอกสาร
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งผู้จัดทำว่าต้องแก้อะไร
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบฟอร์มสรุปผลการคัดกรองโครงการเบื้องต้น
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- แสดงต่อหน้า
- โครงการผ่านการคัดกรอง เข้าสู่ขั้นตอนถัดไป
- โครงการยกเลิกก่อนคัดกรอง
- ใช้ในขั้นตอน
- ให้คะแนน (1-5) ให้ครบทั้ง
- ไฟล์
- ไม่ดำเนินการต่อ
- ไม่ผ่านการตรวจสอบ
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่ยกเลิก
- ไม่อนุมัติ
- ไม่เสนอให้ดำเนินการต่อ
- — กลับเป็นร่าง
- — คุณเป็นผู้พิจารณาใบนี้
- — ส่งกลับเป็นร่าง (ขั้น

## §10 Data Binding & BACKEND anchors
| จุดในโค้ด | API (02_API) |
|---|---|
| `listRows()` `RECS.filter(canSee)` | API-01 |
| `openView()` | API-02 |
| `persist()` (+ `ENG-DOC-NUM` ครั้งแรก · snapshot เกณฑ์/น้ำหนัก) | API-03 / API-04 |
| `openSubmit()` `resolveDoa()` (DOA-ENGINE-HOOK) | API-05 |
| `confirmSubmit()` | API-06 |
| `confirmApprove()` | API-07 approve |
| `confirmReason()` reject | API-07 reject |
| `confirmReason()` cancel | API-08 |
| `docPrintData()` + `tplRender()` + `SCR_TPL` · `genPdf()` | API-09 (server render template เดียวกัน · 2 หน้า) |
| `chunkSigns()` · `DECISION_WORDS` / `wordsOf()` | ตารางลงชื่อ PDF = ผู้จัดทำ + ขั้นใน `approval_chain` (จำนวนตาม DOA) · คำตัดสินตาม role (print_config) |
| `wScore()` · `totalOf()` · `bandOfT()` · `mismatch()` · `SCREENING` | FN-02 คำนวณฝั่ง server + ScreeningCriteria config |
| `validateMain()` | FN-01 · VR-01..03 |
| `exportCSV()` | API-10 |
| `pickFiles()` `gateFiles()` | API-11 |
markers: ENG-DOC-NUM, DOA-ENGINE-HOOK, ENG-DOC-NUM, ENG-NOTIFY, DOA-ENGINE-HOOK, ENG-DOC-NUM, ENG-NOTIFY

## §11 Traceability + Drift Log
| Brief | FRD | HTML |
|---|---|---|
| §4 P-01 | 01 P-01 · API-01/10 | `renderPage()` |
| §4 P-02 | 01 P-02 · API-03/04/11 · BR-01..07 | `renderWizard()` |
| §4 P-03 | 01 P-03 · API-02/05..09 | `renderViewDrawer()` |
| §8 | 05 §5.2 state · LD-01/02/06 | `DOC_ST` · `curStep()` · `SCREENING` |
| Drift | ชนิด | ข้อเสนอ |
|---|---|---|
| D-01 | prototype-only: `__QA__` · `switchPersona()` · `S.sim` · mock `EMP`/`RECS` | ระบบจริงไม่ต้องมี |
| D-02 | prototype ถือ `SCREENING` เป็น const · ระบบจริงอ่าน ScreeningCriteria config + snapshot ลงใบ (FRD BR-04) | dev ทำตาม FRD |

## §12 Diff จากเวอร์ชันก่อน
— ไม่มีใน HTML นี้ (เวอร์ชันแรก)

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- ช่องอ้างอิงโครงการ (FM-BDM-01) เมื่อลูกค้ายืนยัน OQ-05
- ปุ่ม "สร้างแบบบันทึกเหตุผลการไม่ดำเนินโครงการต่อ (FM-BDM-04)" จากใบที่ผล = ไม่ดำเนินการต่อ (OQ-07)
- หน้าตั้งค่า ScreeningCriteria (Config Layout B)
