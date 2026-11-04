# UI_BRIEF — F-FIN-ACL ใบเคลียร์เงินทดรองจ่าย (AS-BUILT)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| HTML (source of truth) | `F-FIN-ACL_ใบเคลียร์เงินทดรองจ่าย.html` (feature.html) · html-generator-v9.2 · archetype `Q-form` (`<meta name="cube-archetype">`) · audit FAIL 0 · e2e 21/21 · domain 13/13 |
| FRD | FRD_F-FIN-ACL_Pack v1.0 (FULL) · DECISIONS.lock 15 มติ (DEC-01..15) |
| Prototype-only | `window.__QA__` · ตัวสลับผู้ใช้ `switchPersona()` · `S.sim` / `commitRejected()` · `EMP`/`RECS` mock → ไม่ต้องสร้างในระบบจริง (Drift Log D-01) |
| Drift | 0 business drift · 2 prototype-only (§11) |

## §1 Design Tokens AS-BUILT
CI Warm Light (html-generator-v9) · font Satoshi + Noto Sans Thai (หน้าจอ) · Sarabun (PDF)
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
ค่าที่ใช้: `1`, `2`, `3`, `var(--z-backdrop)`, `var(--z-drawer)`, `var(--z-dropdown)`, `var(--z-modal)`, `var(--z-popover)`, `var(--z-shell)`, `var(--z-sticky)`, `var(--z-toast)`

## §2 Route Map
| Route | หน้า | handler |
|---|---|---|
| `#/advance-clearing` | P-01 รายการ (default) | `applyRoute()` · `renderPage()` |
| `#/advance-clearing/create` | P-02 สร้าง | `startWizard()` |
| `#/advance-clearing/edit/:id` | P-02 แก้ร่าง (เจ้าของ · draft) | `startWizard()` |
| `#/advance-clearing/view/:id` | P-03 ดู (เฉพาะ `canSee`) | `openView()` · `showDrawer()` |
refresh-safe ผ่าน `hashchange` → `applyRoute()` · route ใบไม่มีสิทธิ์ = ไม่เปิด drawer

## §3 Layout Shell
`.sidebar` (`--sidebar-w`) โมดูล Finance › เคลียร์เงินทดรองจ่าย + badge `#sbBadge` (= รอฉันพิจารณา) · `.shell-bar` (`--shell-h`) breadcrumb Core › Finance › เคลียร์เงินทดรองจ่าย · `.user-chip` + `.user-menu` · content `#page-content`

## §4 Page Anatomy
### P-01 รายการ — `renderPage()`
`.ph` (ชื่อ + `.ph-en` + `.ph-count`) · ปุ่ม `exportCSV()` / `#btnCreate` → `startWizard()` · `.stats` 3 ใบ `statCard()` → `setStat()` · `.filter-bar` (`#fq` `onQ()` · search select `fst` `fres` `fdept` ผ่าน `initSearchSelect()`) · `.table-wrap .table` คอลัมน์ `sortTh()` → `sortBy()` · แถว `rowClick()` · ⋮ `openRowMenu()` (portal `#overlay-root` `.row-menu`) · `pager()` `goPage()` · ว่าง `emptyStateHTML()`
### P-02 สร้าง/แก้ — `renderWizard()` (drawer `.drawer.wide`)
`stepper()` 3 ขั้น (`STEPS`) · ขั้น 1 `wizMain()`: `.wz-split` → `.wz-main` (การ์ด ① `[name=advRef]` `[name=advAmt]` · ② `.exp-list` `lineRow()` `[name=ld-i]` `[name=la-i]` + `.add-row` `addLine()` / `removeLine()` · ③ `#resLine` `#resText` `#resHint` `resultText()`) + `sumCard()` (`#sumRef` `#sumExp` `#sumCnt` `#sumAdv` `#sumTotal`) · อัปเดตสด `softSums()` (ไม่ rebuild) · blur จัดรูปเงิน `fmtAmt()` · ขั้น 2 `wizAttach()` (`#aclFile` `pickFiles()` `gateFiles()`) · ขั้น 3 `wizReview()` · footer `#btnNext` `wizNext()` / `#btnDraft` `saveDraft()` / `#btnSaveSubmit` `saveAndSubmit()`
### P-03 ดู — `renderViewDrawer()`
หัว `.dw-head` (เลขที่ · `docPill()` · ผลเคลียร์ `RES`) · ปุ่ม `#btnSubmitView` `openSubmit()` / `#btnApproveView` `openApprove()` / `openReject()` / `openCancel()` · `.drawer-tabs` `tabBtn()` → `renderDetailTab()` · `renderPdfTab()` (`.pdf-slot` iframe `fitPdf()` · `genPdf()`) · `renderSignTab()` · `renderHistoryTab()`

## §5 Component Inventory
| Component | anchor | states |
|---|---|---|
| ช่องเงิน | `.input-suffix` + `inputmode=decimal` | default · focus · `.is-bad` (invalid) · disabled — |
| แถวรายการ | `.exp-row` `lineRow()` | default · `.is-bad` ต่อช่อง · ลบ (เมื่อ >1 แถว) |
| บรรทัดผลเคลียร์ | `.pd-line` | ปกติ · `.is-warn` (ติดลบ) |
| การ์ดสรุป | `.wz-sum` `.wz-sum-total` | ปกติ · `.is-warn` (ติดลบ) |
| ยอดในตาราง | `.is-neg` | ติดลบ = สีแดง |
| progress ลายเซ็น | `renderSignProgress()` `.sign-prog` | ร่าง = — · n/N |
| slot ผู้พิจารณา | `.slot-row` + search select `slot{i}` | ค่าเริ่ม · `.is-invalid` |
| ปุ่ม busy | `busyLabel()` | loading "กำลังบันทึก…" · disabled |

## §6 Overlay Registry
| Overlay | anchor | ขนาด | ปิดด้วย |
|---|---|---|---|
| drawer สร้าง/แก้ | `#drawer.drawer.drawer-panel.wide` + `#drawerBackdrop` | wide | ปุ่ม/Esc/backdrop · **กรอกค้าง → modal ทิ้งข้อมูล** (`closeDrawer()` dirty) |
| drawer ดู | `#drawer.drawer-panel` | 920 | ปุ่ม ปิด/Esc/backdrop |
| modal ส่ง/อนุมัติ | `#modal.modal.is-lg` | lg | ยกเลิก · Esc · backdrop (`modalBackdropClick()` — มีข้อความค้างห้ามปิด) |
| modal ไม่อนุมัติ/ยกเลิก/ทิ้ง | `#modal` | md | เช่นเดียวกัน |
| เมนู ⋮ | `.row-menu` (portal) | 180px | คลิกนอก · scroll |
| search list | `.ss-list.menu-fixed` | | Esc · คลิกนอก |
| toast | `#toast.toast` | | อัตโนมัติ |
| user menu | `.user-menu` | | คลิกนอก |

## §7 Interaction Spec
Esc chain: search list เปิด → ปิด list ก่อน (stopPropagation) → `state.modal.open` → `closeModal()` → `state.drawer.open` → `closeDrawer()` · คลิกนอกปิด `.row-menu` / `.user-menu` · `addLine()` focus ช่องรายละเอียดแถวใหม่ (rAF) · พิมพ์เงินไม่ rebuild (focus ไม่หลุด) · `preserveRenderState()`/`restoreRenderState()` คืน scroll/focus หลัง render

## §8 State-Driven UI Matrix
| status | pill | ปุ่มหัว (ผู้มีสิทธิ์) |
|---|---|---|
| draft | ร่าง `pill-muted` | เจ้าของ: ยกเลิก · แก้ไข · ส่งอนุมัติ |
| pending | รออนุมัติ `pill-warning` | ผู้พิจารณาขั้นปัจจุบัน: คำปฏิเสธของขั้น · คำอนุมัติของขั้น · อื่น (เจ้าของ/การเงิน): ยกเลิกเอกสาร |
| approved | เคลียร์แล้ว `pill-success` | — (ล็อก) |
| cancelled | ยกเลิก `pill-muted` | — |
ผลเคลียร์: คืนบริษัท `pill-info` · พอดี `pill-muted` · ใช้เกิน `pill-warning`
คำตัดสินผูก role (`DECISION_WORDS` → `wordsOf()`): role-finance-officer = รับเคลียร์/ไม่รับเคลียร์ · role อื่น = อนุมัติ/ไม่อนุมัติ · จำนวน/ลำดับขั้นมาจาก DOA (`resolveDoa()`)

## §9 Microcopy (verbatim)
### toast
- `กรุณากรอกข้อมูลให้ครบถ้วน`
- `บันทึกร่างแล้ว ·`
- `ยังไม่มีสลิปโอนเงินคืน — ส่งกลับแก้ไขให้ผู้ขอแนบสลิป`
- `สลับเป็น`
- `ส่งอนุมัติแล้ว ·`
- `ส่งออก`
- `แก้ไขได้เฉพาะร่างของตัวเอง`
- `แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง`
- `แบบเอกสารนี้ยังไม่เปิดใช้งาน`
- `ไม่มีการแจ้งเตือนใหม่`
- ประกอบ: `ส่งกลับเป็นร่างแล้ว · {เลขที่}` · `ยกเลิกเอกสารแล้ว · {เลขที่}` · `เคลียร์เรียบร้อย · {เลขที่}` · `{คำอนุมัติ}แล้ว · {เลขที่}`
### ปุ่ม / placeholder / label
`Finance` · `กลับไปกรอกต่อ` · `ดาวน์โหลด PDF` · `ถัดไป` · `ทิ้งข้อมูล` · `บันทึกแบบร่าง` · `ปิด` · `พิมพ์` · `ยกเลิก` · `ยกเลิกเอกสาร` · `ย้อนกลับ` · `ล้างตัวกรอง` · `สร้างใบเคลียร์` · `ส่งอนุมัติ` · `ส่งออก CSV` · `เพิ่มรายการ` · `แก้ไข`

`0.00` · `ค้นหาเลขที่ / ผู้ขอ / ใบเบิก / รายการ` · `เช่น ADV-2569-0042` · `เช่น ค่าน้ำมันรถเดินทางพบลูกค้า` · `ไม่บังคับ`
### ข้อความอื่น (จากโค้ด)
- · เคลียร์แล้ว ล็อกแก้ไข
- ก.ค.
- ก.พ.
- ก.ย.
- กบ
- กรกฎาคม
- กรรมการผู้จัดการ
- กรุณากรอกข้อมูลให้ครบถ้วน
- กันยายน
- กานดา บัญชีงาม
- กำลังเปิดหน้าต่างพิมพ์ ·
- กุมภาพันธ์
- ขั้นทดสอบ
- ขาดใบเสร็จ/หลักฐาน
- ขาดใบเสร็จ/หลักฐาน — ค่าทางด่วนไม่มีใบเสร็จ
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลหลักใบเคลียร์
- ข้าม
- คน
- คลิกเพื่อดูรายการ
- คืนบริษัท
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค่าของที่ระลึก
- ค่าจัดสัมมนาลูกค้า
- ค่าตัวอย่างวัสดุ
- ค่าถ่ายเอกสารเข้าเล่ม
- ค่าทางด่วน
- ค่าที่พัก 1 คืน
- ค่าที่พัก 2 คืน
- ค่าน้ำมันรถ
- ค่าน้ำมันรถ จ.ชลบุรี
- ค่าน้ำมันรถเดินทางพบลูกค้า จ.สระบุรี
- ค่ารับรองลูกค้า
- ค่าส่งเอกสารด่วน
- ค่าอาหารรับรองลูกค้า
- ค่าอุปกรณ์ติดตั้งหน้างาน
- ค่าเครื่องมือวัดเช่า
- ค่าเช่ารถยก 1 วัน
- ค่าเดินทางไปพบผู้ขาย
- ค่าเริ่มต้นจากสายอนุมัติและผังองค์กร
- ค่าแท็กซี่ไปงานแสดงสินค้า
- ค่าแรงช่างภายนอก
- ค่าไปรษณีย์ส่งสัญญา
- ค้นหา...
- ค้นหาเลขที่ / ผู้ขอ / ใบเบิก / รายการ
- จะเคลียร์รวมกับใบอื่น
- จำนวนเงิน
- จำนวนเงินไม่ตรงหลักฐาน
- ชนิดไฟล์ไม่รองรับ
- ชื่อ-สกุล
- ดาวน์โหลด PDF
- ต.ค.
- ตรวจสอบและยืนยัน
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตุลาคม
- ต้อง
- ถึง
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ที่คุณเกี่ยวข้อง
- ทุกผลเคลียร์
- ทุกฝ่าย
- ทุกสถานะ
- ธ.ค.
- ธนพล ศรีวงศ์
- ธศ
- ธันวาคม
- บัญชีเงินฝากออมทรัพย์
- บันทึกซ้ำ
- บันทึกผิดใบเบิก
- บันทึกผิดใบเบิก — ใช้ ADV-2569-0037
- บันทึกร่างแล้ว ·
- บาท
- ปก
- ปม
- ประวัติ
- ประเสริฐ มั่นคง
- ปิด
- ปิยะนุช แก้วมณี
- ผู้ขอเคลียร์
- ผู้จัดการฝ่ายการเงิน
- ผู้จัดการฝ่ายขาย
- ผู้จัดการฝ่ายจัดซื้อ
- ผู้จัดการฝ่ายวิศวกรรม
- ผู้บริหาร
- ผู้รับเคลียร์เงิน
- ผู้ส่ง
- ผู้อนุมัติ/ตรวจสอบ
- ฝ่าย/แผนก
- ฝ่ายการเงิน
- ฝ่ายขาย
- ฝ่ายจัดซื้อ
- ฝ่ายวิศวกรรม
- พ.ค.
- พ.ย.
- พฤศจิกายน
- พฤษภาคม
- พอดี
- พิมพ์
- ม.ค.
- มกราคม
- มิ.ย.
- มิถุนายน
- มี.ค.
- มีนาคม
- ยกเลิก
- ยกเลิกเอกสาร
- ยกเลิกเอกสารแล้ว ·
- ยอดเบิก
- ยังไม่มีข้อมูล
- ยังไม่มีสลิปโอนเงินคืน — ส่งกลับแก้ไขให้ผู้ขอแนบสลิป
- ยังไม่มีใบเคลียร์เงินทดรองจ่าย
- ยังไม่มีใบเสร็จแนบ — ผู้อนุมัติอาจส่งกลับแก้ไข
- ยังไม่ส่ง
- ยี่สิบ
- ย้อนกลับ
- รวม
- รวมค่าใช้จ่าย
- รอขั้นก่อนหน้า
- รอฉันพิจารณา
- รอผล
- รอพิจารณา
- รออนุมัติ
- รับเคลียร์
- รายการ
- รายการไม่ใช่ค่าใช้จ่ายของงาน
- รายละเอียด
- รายละเอียดค่าใช้จ่าย
- ร่าง
- ลบ
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ลายเซ็น / อนุมัติ
- ลำดับการอนุมัติ
- ล้างตัวกรอง
- ล้าน
- วท
- วบ
- วรวุฒิ ทองดี
- วันที่
- วันที่ ........./........./.........
- วิชัย บริหารดี
- วิศวกรภาคสนาม
- ส.ค.
- สต
- สถานะ
- สถานะเอกสาร
- สมศักดิ์ ใหญ่ยิ่ง
- สมหญิง ตั้งใจงาน
- สร้าง PDF
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างโดย
- สร้างใบเคลียร์
- สลับเป็น
- สลิปโอนคืน 149.50.jpg
- สิงหาคม
- สิบ
- สใ
- ส่งกลับเป็นร่างแล้ว ·
- ส่งอนุมัติ
- ส่งอนุมัติแล้ว ·
- ส่งออก
- ส่งเคลียร์เงินทดรองจ่าย?
- ส่งแล้วแก้ไขไม่ได้ — ถ้าถูกส่งกลับแก้ไข จะกลับมาเป็นร่างเลขเดิม
- ส่งในระบบ
- ส่งได้ — ฝ่ายการเงินจะตรวจและจ่ายส่วนที่เกิน
- อนุชา พรหมสุข
- อนุมัติ
- อพ
- อยู่ระหว่างสายอนุมัติ
- อ้างอิงเลขที่ใบเบิกเงินทดรองจ่าย
- อ้างอิงใบเบิก
- เคลียร์เงินทดรองจ่าย
- เคลียร์เงินทดรองจ่ายเรียบร้อย
- เคลียร์เงินทดรองที่เบิกไปพร้อมรายการค่าใช้จ่ายจริง
- เคลียร์เรียบร้อย ·
- เคลียร์แล้ว
- เจ้าหน้าที่การเงิน
- เจ้าหน้าที่ขาย
- เจ้าหน้าที่จัดซื้อ
- เช่น ADV-2569-0042
- เช่น ค่าน้ำมันรถเดินทางพบลูกค้า
- เด้งกลับบน
- เพิ่มเติม
- เม.ย.
- เมษายน
- เลขที่
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกตอนส่ง
- เลือกประเทศ
- เลือกผู้พิจารณา
- เหตุผลที่ยกเลิก
- เหลือส่งคืน
- เอกสารแนบ
- เอ็ด
- แก้ไขร่าง
- แก้ไขล่าสุด
- แก้ไขเอกสาร
- แก้ไขใบเคลียร์
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งผู้ขอว่าต้องแก้อะไร
- แนบใบเสร็จ/ใบกำกับของค่าใช้จ่าย
- แนบใบเสร็จและหลักฐาน
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- และสลิปโอนเงินคืนบริษัท
- แล้ว ·
- ใช้เกิน
- ใบเคลียร์ทั้งหมด
- ใบเคลียร์เงินทดรองจ่าย
- ใบเสร็จค่าน้ำมัน-ทางด่วน.pdf
- ใบเสร็จค่าส่งเอกสาร.pdf
- ใส่ยอดที่เบิกไป แล้วระบบจะหักให้
- ใส่ใบเบิกที่จะเคลียร์ แล้วใส่ค่าใช้จ่ายจริงทีละรายการ — ระบบหักยอดเบิกให้
- ไฟล์
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่มีรายการค้าง
- ไม่ยกเลิก
- ไม่รับเคลียร์
- ไม่อนุมัติ
- ไม่อนุมัติ — ส่งกลับเป็นร่าง
- — คุณเป็นผู้พิจารณาใบนี้

## §10 Data Binding & BACKEND anchors
| จุดในโค้ด | API (02_API) |
|---|---|
| `listRows()` `RECS.filter(canSee)` | API-01 |
| `openView()` | API-02 |
| `persist()` (+ `ENG-DOC-NUM` ครั้งแรก) | API-03 / API-04 |
| `openSubmit()` `resolveDoa()` (DOA-ENGINE-HOOK) | API-05 |
| `confirmSubmit()` | API-06 |
| `confirmApprove()` · `openApprove()` ด่านสลิป | API-07 approve |
| `confirmReason()` reject | API-07 reject |
| `confirmReason()` cancel | API-08 |
| `docPrintData()` + `tplRender()` + `ACL_TPL` · `genPdf()` | API-09 (server render template เดียวกัน) |
| `chunkSigns()` · `SIGN_MAX_PER_ROW` · `DECISION_WORDS` / `wordsOf()` | ช่องลงชื่อ PDF = ผู้ขอ + ขั้นใน `approval_chain` (จำนวนตาม DOA) แถวละ ≤4 · คำตัดสินตาม role (print_config) |
| `exportCSV()` | API-10 |
| `pickFiles()` `gateFiles()` | API-11 |
| `POLICY.clearDueDay` · `REFUND_ACCT` | ExpensePolicy · Company.bank_accounts (อ่าน config) |
markers: ENG-DOC-NUM, DOA-ENGINE-HOOK, ENG-DOC-NUM, ENG-NOTIFY, DOA-ENGINE-HOOK, ENG-DOC-NUM, ENG-NOTIFY

## §11 Traceability + Drift Log
| Brief | FRD | HTML |
|---|---|---|
| §4 P-01 | 01 P-01 · API-01/10 | `renderPage()` |
| §4 P-02 | 01 P-02 · API-03/04/11 · BR-01..04 | `renderWizard()` |
| §4 P-03 | 01 P-03 · API-02/05..09 | `renderViewDrawer()` |
| §8 | 05 §5.2 state · LD-01/02 | `DOC_ST` · `curStep()` |
| Drift | ชนิด | ข้อเสนอ |
|---|---|---|
| D-01 | prototype-only: `__QA__` · `switchPersona()` · `S.sim` · mock `EMP`/`RECS` | ระบบจริงไม่ต้องมี |
| D-02 | prototype ตรวจสลิปจากชื่อไฟล์ · ระบบจริงใช้ `attachment.kind=refund_slip` (FRD LD-05) | dev ทำตาม FRD |

## §12 Diff จากเวอร์ชันก่อน
— ไม่มีใน HTML นี้ (เวอร์ชันแรก)

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- เลือกชนิดไฟล์ (ใบเสร็จ/สลิป) ตอนแนบ เพื่อรองรับ `attachment.kind`
- Phase 2: ช่องอ้างอิงใบเบิกเป็น search combobox เมื่อมี FM-FIN-01
