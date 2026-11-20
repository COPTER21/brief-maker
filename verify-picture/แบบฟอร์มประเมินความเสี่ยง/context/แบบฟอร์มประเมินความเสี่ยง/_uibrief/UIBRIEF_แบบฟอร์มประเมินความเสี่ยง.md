# UI_BRIEF — F-TMP-002 แบบฟอร์มประเมินความเสี่ยง (AS-BUILT)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| HTML (source of truth) | `feature.html` · html-generator-v9.4 · archetype `Q-form` (`<meta name="cube-archetype">`) · audit FAIL 0 · e2e 21/21 (verify บน cloud container — เครื่อง user NO-BROWSER) |
| FRD | FRD_F-TMP-002_Pack v1.0 (FULL) · DECISIONS.lock 16 มติ (DEC-01..16 · AI-DEFAULT 11) |
| Prototype-only | `window.__QA__` · ตัวสลับผู้ใช้ `switchPersona()` · `S.sim` / `commitRejected()` · `EMP`/`RECS` mock → ไม่ต้องสร้างในระบบจริง (Drift Log D-01) |
| Drift | 0 business drift · 2 prototype-only (§11) |

## §1 Design Tokens AS-BUILT
CI Warm Light (html-generator-v9) · font Satoshi + Noto Sans Thai (หน้าจอ) · Sarabun (PDF) · ระดับความเสี่ยง: `.sc-chip.is-low/.is-mid/.is-high/.is-vhigh` + pill `pill-success/pill-info/pill-warning/pill-danger`
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
| `#/risk-assessment` | P-01 รายการ (default) | `applyRoute()` · `renderPage()` |
| `#/risk-assessment/create` | P-02 สร้าง | `startWizard()` |
| `#/risk-assessment/edit/:id` | P-02 แก้ร่าง (เจ้าของ · draft) | `startWizard()` |
| `#/risk-assessment/view/:id` | P-03 ดู (เฉพาะ `canSee`) | `openView()` · `showDrawer()` |
refresh-safe ผ่าน `hashchange` → `applyRoute()` · route ใบไม่มีสิทธิ์ = ไม่เปิด drawer

## §3 Layout Shell
`.sidebar` โมดูล Business Development › ประเมินความเสี่ยง + badge `#sbBadge` (= รอฉันพิจารณา) · `.shell-bar` breadcrumb Core › Business Development › ประเมินความเสี่ยง · user chip (icon คน · `toggleUserMenu()`) + `.user-menu` สลับผู้ใช้ (prototype) · `#page-content`

## §4 Page Anatomy
### P-01 รายการ — `renderPage()`
`.ph` (ชื่อ + `.ph-en` + `.ph-badge` ×≤3: รายการ · เปิดอยู่ · รอฉันพิจารณา — ค่า 0 ไม่แสดง · ไม่มี stat cards U1) · ปุ่ม `exportCSV()` / `#btnCreate` → `startWizard()` · `.filter-bar` (`#fq` `onQ()` · search select `fst` `flev` `fdept` ผ่าน `initSearchSelect()` · รีเซ็ต `resetFilters()`) · `.table-wrap .table` คอลัมน์ เลขที่ · วันที่ · ผู้จัดทำ (`personInline()`) · ฝ่าย · ความเสี่ยง · คะแนนสูงสุด · ระดับสูงสุด `levelPill()` · สถานะเอกสาร `docPill()` · ลายเซ็น `renderSignProgress()` · ⋮ `openRowMenu()` · `pager()` + `setSize()` (10/25/50 · ค่าเริ่ม 25) `goPage()`
### P-02 สร้าง/แก้ — `renderWizard()` (drawer `.drawer.wide`)
`stepper()` 3 ขั้น (`STEPS`) · ขั้น 1 `wizMain()`: `sumStrip()` (`#sumCnt` `#sumMax` `#sumHigh` + legend) · `.rk-tbl` แถว `riskRow()` ช่อง `[name=rc-i]` ประเภท · `[name=rd-i]` รายละเอียด · `[name=re-i]` สาเหตุ · `[name=rl-i]` โอกาสเกิด · `[name=ri-i]` ผลกระทบ · `#rs-i` คะแนน `scoreChip()` · `[name=rm-i]` มาตรการ · `[name=rr-i]` คงเหลือ · `[name=rt-i]` สถานะ · ลบ `removeRisk()` · `.add-row` `addRisk()` · `#rkWarn` เตือนคงเหลือ > ก่อนควบคุม · อัปเดตสด `setRisk()` → `softSums()` · ขั้น 2 `wizAttach()` `.upload-zone` `pickFiles()` · ขั้น 3 `wizReview()` (`riskTable()` · `levelSummary()`) · footer `wizBack()` `wizNext()` `saveDraft()` `saveAndSubmit()`
### P-03 ดู — `renderViewDrawer()`
หัว `.dw-head` (เลขที่ · `docPill()` · sub ≤2 fact) · ปุ่ม `#btnSubmitView` `openSubmit()` / `#btnApproveView` `openApprove()` / `openReject()` / `openCancel()` · `.drawer-tabs` `tabBtn()` → `renderDetailTab()` (`riskTable()` · `levelSummary()` · `criteriaTable()`) · `renderPdfTab()` (`.pdf-slot` iframe `.pdf-frame` srcdoc `docPdfDoc()` · `fitPdf()` · `genPdf()`) · `renderSignTab()` · `renderHistoryTab()`

## §5 Component Inventory
| Component | anchor | states |
|---|---|---|
| ตารางทะเบียน (แก้) | `.rk-tbl` `riskRow()` | default · `.is-bad` ต่อช่อง · `.is-warn` (คงเหลือ > ก่อนควบคุม) · ลบ (เมื่อ >1 แถว) |
| chip คะแนน | `scoreChip()` `.sc-chip` | ว่าง (—) · low · mid · high · vhigh |
| แถบสรุปสด | `.rk-strip` `sumStrip()` | อัปเดตแบบ soft (focus ไม่หลุด) |
| สรุประดับ | `levelSummary()` `.lv-grid` | ก่อนควบคุม/คงเหลือต่อช่วง + แนวทาง · เตือนเมื่อคงเหลือ > ก่อนควบคุม |
| ตารางทะเบียน (อ่าน) | `riskTable()` `.rk-view` | ว่าง = แผง "ไม่มีข้อมูล" (U23) |
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
Esc chain: search list เปิด → ปิด list ก่อน (stopPropagation) → modal → `closeModal()` → drawer → `closeDrawer()` · backdrop ปิดด้วย mousedown เท่านั้น (ลากจากข้างในไปปล่อยนอกไม่ปิด) · `addRisk()` focus ช่องประเภทของแถวใหม่ · เลือกโอกาส/ผลกระทบ → คะแนน + สรุปอัปเดตทันที · คงเหลือ > ก่อนควบคุม → ขอบส้ม + `#rkWarn`

## §8 State-Driven UI Matrix
| status | pill | ปุ่มหัว (ผู้มีสิทธิ์) |
|---|---|---|
| draft | ร่าง `pill-muted` | เจ้าของ: ยกเลิก · แก้ไข · ส่งอนุมัติ |
| pending | รออนุมัติ `pill-warning` | ผู้พิจารณาขั้นปัจจุบัน: คำปฏิเสธของขั้น · คำอนุมัติของขั้น · อื่น (เจ้าของ/admin): ยกเลิกเอกสาร |
| approved | อนุมัติแล้ว `pill-success` | — (ล็อก) |
| cancelled | ยกเลิก `pill-muted` | — |
ระดับความเสี่ยง (RiskMatrix.level_bands): ต่ำ `pill-success` · ปานกลาง `pill-info` · สูง `pill-warning` · สูงมาก `pill-danger`
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
- ประกอบ: `ส่งกลับเป็นร่างแล้ว · {เลขที่}` · `ยกเลิกเอกสารแล้ว · {เลขที่}` · `อนุมัติ / รับทราบเรียบร้อย · {เลขที่}` · `ส่งต่อขั้นถัดไปแล้ว · {เลขที่}` · `บันทึกร่างแล้ว · {เลขที่}`
### ปุ่ม / placeholder / label
`Business Development` · `กลับไปกรอกต่อ` · `ดาวน์โหลด PDF` · `ถัดไป` · `ทิ้งข้อมูล` · `บันทึกแบบร่าง` · `ปิด` · `พิมพ์` · `ยกเลิก` · `ยกเลิกเอกสาร` · `ย้อนกลับ` · `รีเซ็ต` · `สร้างแบบประเมิน` · `ส่งอนุมัติ` · `ส่งออก CSV` · `เพิ่มความเสี่ยง` · `แก้ไข`

`ความเสี่ยงคืออะไร` · `ค้นหาเลขที่ / ผู้จัดทำ / ความเสี่ยง` · `มาตรการควบคุม` · `สาเหตุ / ผลกระทบ` · `ไม่บังคับ` · aria: `คะแนนคงเหลือ` · `ประเภทความเสี่ยง` · `ผลกระทบก่อนควบคุม` · `มาตรการควบคุม` · `รายละเอียดความเสี่ยง` · `สถานะ` · `สาเหตุ / ผลกระทบ` · `แสดงต่อหน้า` · `โอกาสเกิดก่อนควบคุม`
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
- กฎหมาย / ข้อกำกับ
- กรรมการผู้จัดการ
- กรอกประเภท รายละเอียด โอกาสเกิด ผลกระทบ และสถานะให้ครบทุกรายการ
- กระทบต่อเป้าหมายสำคัญ
- กระทบต่อแผนงานบางส่วน
- กระทบรุนแรงต่อโครงการ
- กรุณากรอกข้อมูลให้ครบถ้วน
- กลยุทธ์
- การดำเนินงาน
- การเงิน
- กำลังเปิดหน้าต่างพิมพ์ ·
- กำหนดจุดตรวจรายสัปดาห์และผู้รับเหมาสำรอง
- กิตติพัฒน์ ทดลองงาน
- ขั้นตอนที่ 3 และขั้นตอนที่ 7: ประเมินและติดตามความเสี่ยงของโครงการ
- ขั้นทดสอบ
- ขาดความเสี่ยงสำคัญของโครงการ
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลหลักแบบประเมิน
- ข้อร้องเรียนจากชุมชนรอบพื้นที่
- ข้าม
- คน
- คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
- ความต้องการสินค้าต่ำกว่าประมาณการ
- คะแนนก่อนควบคุมสูงสุด
- คะแนนคงเหลือ
- คะแนนคงเหลือสูงกว่าคะแนนก่อนควบคุม รายการที่
- คุณไม่มีสิทธิ์ทำรายการนี้
- คู่แข่งตัดราคา / รายได้ไม่ถึงเป้า
- ค่าเริ่มต้นจากสายอนุมัติและผังองค์กร
- ค้นหา...
- ค้นหาเลขที่ / ผู้จัดทำ / ความเสี่ยง
- จัดทำครั้งแรก
- จัดทำคู่มือและมอบหมายผู้แทน
- จัดทำมาตรการและติดตาม
- จำนวนความเสี่ยง
- ชนิดไฟล์ไม่รองรับ
- ชยพล ตั้งระบบ
- ชื่อ
- ชื่อเสียง
- ดาวน์โหลด PDF
- ต.ค.
- ตรวจรายการเอกสารกับที่ปรึกษากฎหมาย
- ตรวจสอบและยืนยัน
- ตรวจสอบแล้ว
- ตลาด
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตำแหน่ง
- ติดตามตามปกติ
- ติดตามผล
- ต่ำ
- ต่ำมาก
- ต้นทุนโครงการเกินงบประมาณ
- ต้อง
- ถึง
- ทดสอบระบบก่อนใช้งานจริงและทำแผนสำรอง
- ทบทวนสัญญาและกำหนดเงื่อนไขการถอนตัว
- ทะเบียนและแบบประเมินความเสี่ยง
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ทำแผนการตลาดสำรองและทบทวนราคาไตรมาสละครั้ง
- ทุกฝ่าย
- ทุกระดับสูงสุด
- ทุกสถานะ
- ธ.ค.
- ธีรพงษ์ สมมติชื่อ
- นภัสสร ตัวอย่างดี
- บริษัท ตัวอย่าง จำกัด (มหาชน)
- บริษัท ตัวอย่าง จำกัด (มหาชน) และบริษัทในเครือ
- บันทึกซ้ำ
- บันทึกซ้ำ — ใช้ RSK-2569-0004
- บันทึกร่างแล้ว ·
- บุคลากร
- บุคลากรหลักลาออกระหว่างโครงการ
- ประชาสัมพันธ์ล่วงหน้าและติดตั้งแผงกันฝุ่น
- ประวัติ
- ประวัติ (append-only)
- ประเภทความเสี่ยง
- ประเมินคะแนนไม่สอดคล้องเกณฑ์
- ประเมินรวมกับใบอื่นแล้ว
- ปานกลาง
- ปิด
- ปิดแล้ว
- ผลกระทบก่อนควบคุม
- ผลกระทบจำกัด
- ผลกระทบเล็กน้อย
- ผู้จัดการฝ่ายพัฒนาธุรกิจ
- ผู้จัดการฝ่ายวิศวกรรม
- ผู้จัดทำ
- ผู้ตรวจสอบ
- ผู้บริหาร
- ผู้รับเหมาขาดกำลังคน / เสียค่าปรับ
- ผู้ส่ง
- ผู้อนุมัติ / รับทราบ
- ผู้เชี่ยวชาญด้านพัฒนาธุรกิจ
- ผู้ให้บริการระบบรายเดียว / ข้อมูลตกหล่น
- ฝ่าย
- ฝ่ายพัฒนาธุรกิจ
- ฝ่ายวิศวกรรม
- พ.ค.
- พ.ย.
- พันธมิตรถอนตัวจากโครงการ
- พิมพ์
- ภาระงานสูง / ความรู้ไม่ถูกส่งต่อ
- ม.ค.
- มาตรการควบคุมยังไม่ชัดเจน
- มาตรการควบคุมยังไม่ชัดเจน — ระบุผู้รับผิดชอบและกำหนดเวลา
- มาลัย ประสานงาน
- มิ.ย.
- มี.ค.
- มีแนวโน้มเกิด
- มีแนวโน้มเกิดสูง
- ยกระดับให้ผู้จัดการฝ่ายพิจารณา
- ยกเลิก
- ยกเลิกเอกสาร
- ยกเลิกเอกสารแล้ว ·
- ยังไม่มีข้อมูล
- ยังไม่มีรายการความเสี่ยง
- ยังไม่มีแบบประเมินความเสี่ยง
- ยังไม่ส่ง
- ย้อนกลับ
- รอขั้นก่อนหน้า
- รองกรรมการผู้จัดการ
- รอผล
- รอพิจารณา
- รออนุมัติ
- ระดับสูง / สูงมาก
- ระดับสูง/สูงมาก
- ระดับสูงสุด
- ระบบเชื่อมต่อข้อมูลลูกค้าไม่เสถียร
- ระบุ ประเมิน และติดตามความเสี่ยงก่อนและหลังมาตรการควบคุม
- ราคาวัสดุผันผวน / กำไรลดลง
- รายการ
- รายงานผู้บริหารและดำเนินการเร่งด่วน
- รายละเอียด
- ร่าง
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ลายเซ็น / อนุมัติ
- ลำดับการอนุมัติ
- ล็อกราคาวัสดุหลักล่วงหน้า 6 เดือน
- ล้างตัวกรอง
- วันที่
- วันที่ ........./........./.........
- วิศวกรโครงการ
- ศิริพร ตัวแทนดี
- ส.ค.
- สถานะ
- สถานะ "ปิดแล้ว" ต้องระบุคะแนนคงเหลือ
- สถานะเอกสาร
- สภาพคล่องโครงการ / ต้องชะลองาน
- สรุปประชุมประเมินความเสี่ยงโครงการ.pdf
- สร้าง PDF
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างแบบประเมิน
- สร้างโดย
- สลับเป็น
- สูง
- สูงมาก
- ส่งกลับเป็นร่างแล้ว ·
- ส่งต่อขั้นถัดไปแล้ว ·
- ส่งมอบงานล่าช้ากว่าแผน
- ส่งอนุมัติ
- ส่งอนุมัติแล้ว ·
- ส่งออก
- ส่งแบบประเมินความเสี่ยง?
- ส่งแล้วแก้ไขไม่ได้ — ถ้าถูกส่งกลับแก้ไข จะกลับมาเป็นร่างเลขเดิม
- ส่งในระบบ
- หนังสือแจ้งเงื่อนไขวงเงิน.pdf
- อนุมัติ
- อนุมัติ / รับทราบ
- อนุมัติ / รับทราบเรียบร้อย ·
- อนุมัติ / รับทราบแล้ว
- อนุมัติแล้ว
- อยู่ระหว่างจัดการ
- อรุณี ทดสอบระบบ
- อาจเกิดขึ้นได้
- อื่น
- เกิดขึ้นไม่บ่อย
- เกิดได้น้อยมาก
- เงื่อนไขสัญญาไม่ชัดเจน
- เจรจาแหล่งเงินสำรองสองราย
- เจ้าหน้าที่ประสานงานโครงการ
- เด้งกลับบน
- เทคโนโลยี
- เปิด
- เพิ่มเติม
- เม.ย.
- เลขที่
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกตอนส่ง
- เลือกประเทศ
- เลือกผู้พิจารณา
- เลือก…
- เสียงและฝุ่นจากงานก่อสร้าง
- เหตุผลที่ยกเลิก
- เอกสารแนบ
- เอกสารไม่ครบ / เริ่มงานไม่ได้
- แก้ไขร่าง
- แก้ไขล่าสุด
- แก้ไขเอกสาร
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งผู้จัดทำว่าต้องแก้อะไร
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบฟอร์มประเมินความเสี่ยง
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- แผนรับมือความเสี่ยง.xlsx
- แสดงต่อหน้า
- แหล่งเงินกู้ยกเลิกวงเงินสนับสนุน
- โครงการยกเลิก
- โอกาสเกิดก่อนควบคุม
- ใช้ในขั้นตอน
- ใบอนุญาตก่อสร้างออกช้า
- ใส่ความเสี่ยงทีละรายการ เลือกโอกาสเกิดและผลกระทบ (1–5) — ระบบคูณคะแนนก่อนควบคุมให้
- ไฟล์
- ไม่ผ่านการตรวจสอบ
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่มีข้อมูล
- ไม่ยกเลิก
- ไม่อนุมัติ
- — คุณเป็นผู้พิจารณาใบนี้
- — บันทึกได้ แต่ควรทบทวนมาตรการ
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
| `docPrintData()` + `tplRender()` + `RSK_TPL` · `genPdf()` | API-09 (server render template เดียวกัน · 2 หน้า) |
| `chunkSigns()` · `DECISION_WORDS` / `wordsOf()` | ตารางลงชื่อ PDF = ผู้จัดทำ + ขั้นใน `approval_chain` (จำนวนตาม DOA) · คำตัดสินตาม role (print_config) |
| `scoreOf()` · `bandOf()` · `RISK_MATRIX` | FN-02 คำนวณฝั่ง server + RiskMatrix config |
| `validateMain()` | FN-01 · VR-01/02 |
| `exportCSV()` | API-10 |
| `pickFiles()` `gateFiles()` | API-11 |
markers: ENG-DOC-NUM, DOA-ENGINE-HOOK, ENG-DOC-NUM, ENG-NOTIFY, DOA-ENGINE-HOOK, ENG-DOC-NUM, ENG-NOTIFY

## §11 Traceability + Drift Log
| Brief | FRD | HTML |
|---|---|---|
| §4 P-01 | 01 P-01 · API-01/10 | `renderPage()` |
| §4 P-02 | 01 P-02 · API-03/04/11 · BR-01..05 | `renderWizard()` |
| §4 P-03 | 01 P-03 · API-02/05..09 | `renderViewDrawer()` |
| §8 | 05 §5.2 state · LD-01/02 | `DOC_ST` · `curStep()` |
| Drift | ชนิด | ข้อเสนอ |
|---|---|---|
| D-01 | prototype-only: `__QA__` · `switchPersona()` · `S.sim` · mock `EMP`/`RECS` | ระบบจริงไม่ต้องมี |
| D-02 | prototype ถือ `RISK_MATRIX` เป็น const · ระบบจริงอ่าน RiskMatrix config (FRD BR-06) | dev ทำตาม FRD |

## §12 Diff จากเวอร์ชันก่อน
— ไม่มีใน HTML นี้ (เวอร์ชันแรก)

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- ช่องอ้างอิงโครงการ (FM-BDM-01) เมื่อลูกค้ายืนยัน OQ-05
- หน้าตั้งค่า RiskMatrix (Config Layout B) · dashboard ความเสี่ยงสูงมากที่ยังเปิด
