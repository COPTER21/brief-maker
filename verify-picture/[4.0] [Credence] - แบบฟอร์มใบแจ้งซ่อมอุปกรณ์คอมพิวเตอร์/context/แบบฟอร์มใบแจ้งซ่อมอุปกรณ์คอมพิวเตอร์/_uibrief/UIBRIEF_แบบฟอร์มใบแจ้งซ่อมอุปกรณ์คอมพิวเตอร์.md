# UI_BRIEF — F-TMP-004 แบบฟอร์มใบแจ้งซ่อมอุปกรณ์คอมพิวเตอร์ (AS-BUILT)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| HTML (source of truth) | feature.html · html-generator-v9.4 Golden Skeleton · archetype `Q-form` (`<meta name="cube-archetype">`) · audit FAIL 0 · [NO-BROWSER] e2e_standard ข้าม → jsdom smoke 54/54 |
| FRD | FRD_F-TMP-004_Pack v1.0 (FULL) · DECISIONS.lock 18 มติ (DEC-01..11 AI-DEFAULT · DEC-12..18 VALID) |
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

### z-index
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
| `.bd-pop` | `var(--z-portal)` |
ค่าที่ใช้: `1`, `2`, `3`, `var(--z-backdrop)`, `var(--z-drawer)`, `var(--z-dropdown)`, `var(--z-modal)`, `var(--z-popover)`, `var(--z-portal)`, `var(--z-shell)`, `var(--z-sticky)`, `var(--z-toast)`

## §2 Route Map
| Route | หน้า | handler |
|---|---|---|
| `#/repair-request` | P-01 รายการ (default) | `applyRoute()` · `renderPage()` |
| `#/repair-request/create` | P-02 แจ้งซ่อม (สร้าง) | `startWizard()` |
| `#/repair-request/edit/:id` | P-02 แก้ร่าง (เจ้าของ · draft) | `startWizard()` |
| `#/repair-request/view/:id` | P-03 ดู (เฉพาะ `canSee`) | `openView()` · `showDrawer()` |
refresh-safe ผ่าน `hashchange` → `applyRoute()` · route ใบไม่มีสิทธิ์ = ไม่เปิด drawer

## §3 Layout Shell
`.sidebar` โมดูล IT Support › แจ้งซ่อมอุปกรณ์คอมพิวเตอร์ + badge `#sbBadge` (= งานที่ต้องทำ) · breadcrumb Core › IT Support › แจ้งซ่อมอุปกรณ์คอมพิวเตอร์ · `.user-chip` (วงกลมรูปคน `.emp-av`) + `.user-menu` (`#personaList`) · content `#page-content`

## §4 Page Anatomy
### P-01 รายการ — `renderPage()`
`.ph` (ชื่อ · sub + `.ph-badge` จำนวน/งานที่ต้องทำ/ระหว่างดำเนินการ — **ไม่มี scorecard** U1) · ปุ่ม `exportCSV()` / `#btnCreate` → `startWizard()` · แท็บ `segTabs()` `.seg` `.seg-btn` `.seg-n` → `setListTab()` (ทั้งหมด · งานที่ต้องทำ · ใบแจ้งซ่อมของฉัน) · `.filter-bar` (`#fq` `onQ()` · search select `fst` `fdt` ผ่าน `initSearchSelect()` · รีเซ็ต `resetFilters()`) · `.table-wrap .table` คอลัมน์ `sortTh()` → `sortBy()` · ผู้แจ้งซ่อม `personInline()` · ลายเซ็น `renderSignProgress()` · แถว `rowClick()` · ⋮ `openRowMenu()` (portal `#overlay-root` `.row-menu`) · `pager()` (`.pg-size` `setSize()` · `.pg-info` · `goPage()`) · ว่าง `emptyStateHTML()`
### P-02 แจ้งซ่อม/แก้ — `renderWizard()` (drawer `.drawer.wide`)
`stepper()` 3 ขั้น (`STEPS`) · ขั้น 1 `wizMain()`: `.wz-split` → `.wz-main` (การ์ด ① ประเภท radio `[name=devType]` `pickDev()` · อื่นๆ `[name=devOther]` · `[name=item]` `[name=asset]` · ② `[name=problem]` · ③ วันที่ `bedateHTML()` `pickDue()` · `[name=place]`) + `sumCard()` (`#sumDev` `#sumDue` `#sumPlace`) · พิมพ์ไม่ rebuild `setF2()` · ขั้น 2 `wizAttach()` (`#crrFile` `pickFiles()` `gateFiles()` `removeFile()`) · ขั้น 3 `wizReview()` · footer `#btnNext` `wizNext()` / `#btnDraft` `saveDraft()` / `#btnSaveSubmit` `saveAndSubmit()` → `openReport()`
### P-03 ดู — `renderViewDrawer()`
หัว `.dw-head` (เลขที่ · `docPill()` · sub 1 fact: รายการ) · ปุ่มตามสถานะ `#btnReportView` `openReport()` / `#btnReceiveView` `openReceive()` / `#btnInspectView` `openInspect()` / `#btnApproveView` `openApprove()` + `openReject()` / `#btnRepairView` `openRepair()` / `#btnAckView` `openAck()` / `openCancel()` · `.drawer-tabs` `tabBtn()` → `renderDetailTab()` (`viewBanner()` · `claimKv()`) · `renderPdfTab()` (`.pdf-slot` iframe `fitPdf()` · `genPdf()`) · `renderSignTab()` (timeline 6 จุดลงชื่อ `.timeline` `.tl-item` `empChip()`) · `renderHistoryTab()` (`.tl-q`)

## §5 Component Inventory
| Component | anchor | states |
|---|---|---|
| radio ประเภท | `.jt-grid` `.chk` | ยังไม่เลือก · เลือกแล้ว · อื่นๆ → `.jt-other` โผล่ · `.is-invalid` |
| ตัวเลือกผลตรวจเช็ค/ผลการซ่อม | `.opt-list` `.chk` | 5 / 2 ตัวเลือก · `.is-invalid` |
| ชุดเคลม | `.claim-box` | โผล่เมื่อเลือก 3 ตัวเลือกล่าง · เตือนวันสิ้นสุดก่อนวันเริ่ม `.is-warn` |
| ตัวเลือกวัน พ.ศ. | `.bedate` | ว่าง · เลือกแล้ว · `.is-invalid` |
| การ์ดสรุป | `.wz-sum` | อัปเดตสด |
| คน | `.emp-av` `empChip()` `personInline()` | วงกลมรูปคน mono (U17) |
| แท็บ | `.seg-btn` | ปกติ · `.on` (dot primary + count) |
| progress ลายเซ็น | `renderSignProgress()` `.sign-prog` `.sp-bar` | ก่อนส่งอนุมัติ = — · n/N · `.is-bad` (ยกเลิก) |
| slot ผู้พิจารณา | `.slot-row` + search select slot{i} | 1 แถวต่อขั้น DOA · `.is-invalid` |
| ปุ่ม busy | `busyLabel()` | loading "กำลังบันทึก…" · disabled |
| แบนเนอร์สถานะ | `.alert-row` | ทุกสถานะ · `.is-danger` (ไม่อนุมัติ/ยกเลิก) · `.is-success` (ปิดงาน) |

## §6 Overlay Registry
| Overlay | anchor | ขนาด | ปิดด้วย |
|---|---|---|---|
| drawer สร้าง/แก้ | `#drawer.drawer.drawer-panel.wide` + `#drawerBackdrop` | wide 1290 | ปุ่ม/Esc/mousedown ที่ backdrop (`drawerBackdropDown()`) · **กรอกค้าง → modal ทิ้งข้อมูล** |
| drawer ดู | `#drawer.drawer-panel` | 920 | ปุ่ม ปิด/Esc/backdrop |
| modal ผลตรวจเช็ค/ส่งอนุมัติ | `#modal.modal.is-lg` | lg | ยกเลิก · Esc · mousedown ที่ backdrop (`modalBackdropDown()` — มีข้อมูลค้างห้ามปิด · ลากจากในกล่องไม่ปิด U25) |
| modal ส่งแจ้งซ่อม/รับแจ้ง/อนุมัติ/ไม่อนุมัติ/ยกเลิก/ผลการซ่อม/รับทราบ/ทิ้ง | `#modal` | md | เช่นเดียวกัน |
| เมนู ⋮ | `.row-menu` (portal) | 200px | คลิกนอก · scroll |
| search list | `.ss-list` | | Esc · คลิกนอก |
| ปฏิทิน พ.ศ. | `.bedate` popup (portal) | | Esc · คลิกนอก |
| toast | `#toast.toast` | | อัตโนมัติ |
| user menu | `.user-menu` | | คลิกนอก |

## §7 Interaction Spec
Esc chain: ปฏิทิน/search list เปิด → ปิดก่อน → `state.modal.open` → `closeModal()` → `state.drawer.open` → `closeDrawer()` · คลิกนอกปิด `.row-menu` / `.user-menu` · พิมพ์ใน wizard ไม่ rebuild (`setF2()`) · เลือก radio/วันที่ = rebuild · บันทึกผลตรวจเช็คและส่งอนุมัติ = ปิด modal ผลตรวจเช็คแล้วเปิด modal ส่งอนุมัติ (`saveInspect()` → `openSubmit()`) · แก้ร่างจาก view = ปิด view ก่อน (U15) · `preserveRenderState()`/`restoreRenderState()` คืน scroll/focus หลัง render

## §8 State-Driven UI Matrix
| status | pill | ปุ่มหัว (ผู้มีสิทธิ์) |
|---|---|---|
| draft | ร่าง `pill-muted` | เจ้าของ: ยกเลิกเอกสาร · แก้ไข · ส่งแจ้งซ่อม |
| reported | รอรับแจ้ง `pill-warning` | IT: ยกเลิกเอกสาร · รับแจ้ง |
| inspecting | ตรวจเช็ค `pill-info` | IT: ยกเลิกเอกสาร · บันทึกผลตรวจเช็ค (→ ส่งอนุมัติ) · ไม่อนุมัติกลับมา = แบนเนอร์เหตุผล |
| pending | รออนุมัติ `pill-warning` | ผู้พิจารณาขั้นปัจจุบัน: ไม่อนุมัติ · อนุมัติ |
| approved | รอผลซ่อม `pill-info` | IT: บันทึกผลการซ่อม |
| repaired | รอผู้แจ้งรับทราบ `pill-info` | เจ้าของ: รับทราบผล |
| closed | ปิดงาน `pill-success` | — (ล็อก) |
| cancelled | ยกเลิก `pill-muted` | — |
จำนวนขั้นมาจาก DOA (`resolveDoa()` · `MOCK_DOA_RESOLVED` = 1 ขั้น "อนุมัติโดย" ตาม DEC-03) · สายว่างจนส่งอนุมัติ (`blankChain()`)

## §9 Microcopy (verbatim)
### toast
- `กรุณากรอกข้อมูลให้ครบถ้วน`
- `กรุณากรอกผลตรวจเช็คให้ครบถ้วน`
- `บันทึกผลตรวจเช็คแล้ว ·`
- `บันทึกร่างแล้ว ·`
- `สลับเป็น`
- `ส่งอนุมัติได้เฉพาะใบที่บันทึกผลตรวจเช็คแล้ว`
- `ส่งออก`
- `แก้ไขได้เฉพาะร่างของตัวเอง`
- `แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง`
- `แบบเอกสารนี้ยังไม่เปิดใช้งาน`
- `ไม่มีการแจ้งเตือนใหม่`
- ประกอบ: `ส่งแจ้งซ่อมแล้ว · {เลขที่}` · `รับแจ้งแล้ว · {เลขที่}` · `ส่งอนุมัติแล้ว · {เลขที่}` · `อนุมัติแล้ว · {เลขที่}` · `ไม่อนุมัติ — ส่งกลับร่างผลตรวจเช็ค · {เลขที่}` · `บันทึกผลการซ่อมแล้ว · {เลขที่}` · `ปิดงานแล้ว · {เลขที่}` · `ยกเลิกเอกสารแล้ว · {เลขที่}` · `บันทึกร่างแล้ว · {เลขที่}` · `บันทึกผลตรวจเช็คแล้ว · {เลขที่}` · `ส่งออก {n} รายการ` · `สลับเป็น {ชื่อ}`
### ข้อความบนจอ (สกัดจาก HTML)
- 2 ฝ่ายขาย
- 3 ฝ่ายบัญชี
- 4 ฝ่ายบุคคล
- [Lucide] All CDNs failed. Icons จะไม่แสดง but UI ยังใช้งานได้
- ]); if (canAck(r)) items.push(['check-check', 'รับทราบผลการซ่อม',
- ]); if (canAct(r)) items.push(['check', 'พิจารณาอนุมัติ',
- ]); if (canCancel(r)) items.push(['x-circle', 'ยกเลิกเอกสาร',
- ]); if (canInspect(r)) items.push(['stethoscope', 'บันทึกผลตรวจเช็ค',
- ]); if (canReceive(r)) items.push(['inbox', 'รับแจ้ง',
- ]); if (canRepair(r)) items.push(['wrench', 'บันทึกผลการซ่อม',
- ], ['printer', 'พิมพ์',
- ]]; if (isOwner(r) && r.status === 'draft') items.splice(1, 0, ['pencil', 'แก้ไข',
- showToast('ไม่มีการแจ้งเตือนใหม่','info')
- · กด "รับทราบผล" เพื่อปิดงาน
- · กด "รับแจ้ง" เพื่อเริ่มตรวจเช็ค
- · กลับเป็นร่างผลตรวจเช็คเลขเดิม ให้ฝ่าย IT แก้แล้วส่งใหม่
- · บันทึกผลตรวจเช็คแล้วส่งอนุมัติ
- · ปิดงานแล้ว ล็อกแก้ไข
- ก.ค.
- ก.พ.
- ก.ย.
- กรกฎาคม
- กรุณากรอกข้อมูลให้ครบถ้วน
- กรุณากรอกผลตรวจเช็คให้ครบถ้วน
- กันยายน
- กำลังตรวจเช็ค
- กำลังเปิดหน้าต่างพิมพ์ ·
- กำหนดผู้พิจารณาตอนส่งอนุมัติ
- กิตติพงษ์ สมมติชื่อ
- กุมภาพันธ์
- ก่อนวันที่แจ้ง
- ก่อนวันที่แจ้ง — ตรวจอีกครั้ง (เตือน ไม่บล็อก)
- ขอให้ตรวจเช็คเพิ่มเติมก่อน
- ขั้นทดสอบ
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลระบบ
- ข้อมูลแจ้งซ่อม
- ข้าม
- คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค่าเริ่มต้นจากสายอนุมัติและผังองค์กร
- ค้นหา...
- ค้นหาเลขที่ / ผู้แจ้งซ่อม / รายการ / รหัสทรัพย์สิน
- งานที่ต้องทำ
- จอดับเองเป็นระยะ
- จอภาพ (Monitor)
- จอภาพ 24 นิ้ว โต๊ะบัญชี 3
- จอแสดงผลเป็นเส้น
- ชนิดไฟล์ไม่รองรับ
- ชัยวัฒน์ สมมุติ
- ชาร์จไฟไม่เข้า
- ชื่อ-นามสกุล
- ชื่อฟังก์ชัน
- ซ่อมไม่ได้ต้องส่งไปที่บริษัทเนื่องจากอยู่ระยะประกัน
- ซ่อมไม่ได้ต้องส่งไปที่บริษัทแต่ไม่อยู่ระยะในประกัน
- ดาวน์โหลด PDF
- ดำเนินการซ่อมแล้วเสร็จ
- ดูจากป้ายบนเครื่อง เช่น IT-NB-0123
- ต.ค.
- ตรวจสอบและยืนยัน
- ตรวจเช็ค
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตำแหน่ง
- ติดตั้งไดรเวอร์เสียงใหม่ ทดสอบประชุมออนไลน์ได้
- ตุลาคม
- ต้อง
- ถึง
- ถึงฝ่าย IT
- ทั้งหมด
- ทำความสะอาดลูกยางดึงกระดาษ ทดสอบพิมพ์ปกติ
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ทุกประเภท
- ทุกสถานะ
- ธ.ค.
- ธนพล ไอทีดี
- ธันวาคม
- นภัสสร ตัวอย่าง
- บริษัทตัวอย่าง
- บอกว่าอุปกรณ์อะไรเสีย อาการเป็นอย่างไร ต้องการรับคืนเมื่อไหร่ที่ไหน — ชื่อและตำแหน่งระบบใส่ให้
- บันทึกผลการซ่อม
- บันทึกผลตรวจเช็ค
- บันทึกผลตรวจเช็คแล้ว ·
- บันทึกผิด
- บันทึกร่างแล้ว ·
- บันทึกเมื่อ
- บันทึกในระบบ
- ประวัติ
- ประวัติ (append-only)
- ประเภท
- ประเสริฐ ผู้บริหาร
- ปรียา ตัวอย่างงาม
- ปิด
- ปิดงาน
- ปิดงาน ·
- ผลการซ่อม
- ผลตรวจเช็ค
- ผู้จัดการทั่วไป
- ผู้จัดการฝ่ายขาย
- ผู้จัดการฝ่ายบัญชี
- ผู้จัดการฝ่ายบุคคล
- ผู้ดำเนินการ
- ผู้ดำเนินการ (ผลการซ่อม)
- ผู้ดำเนินการ (ส่วนที่ 2 · ส่งอนุมัติ)
- ผู้รับแจ้ง
- ผู้รับแจ้ง (ฝ่าย IT)
- ผู้ส่งอนุมัติ
- ผู้แจ้งซ่อม
- ผู้แจ้งซ่อม (รับทราบผล)
- ผู้แจ้งซ่อม (ส่วนที่ 1)
- ผู้แจ้งซ่อมรับทราบ
- ผู้แจ้งซ่อมรับทราบผล — ปิดงาน
- ฝ่าย IT
- ฝ่ายขาย
- ฝ่ายบัญชี
- ฝ่ายบุคคล
- ฝ่ายผลิต
- ฝ่ายเทคโนโลยีสารสนเทศ
- พ.ค.
- พ.ย.
- พฤ
- พฤศจิกายน
- พฤษภาคม
- พิมพ์
- พิมพ์ออกมาซีดจาง มีแถบดำ
- พิมพ์แล้วกระดาษติดทุกแผ่น
- ม.ค.
- มกราคม
- มิ.ย.
- มิถุนายน
- มี.ค.
- มีนาคม
- ยกเลิก
- ยกเลิกเอกสาร
- ยกเลิกเอกสารแล้ว
- ยังไม่มีข้อมูล
- ยังไม่มีใบแจ้งซ่อม
- ยังไม่ระบุสถานที่
- ยังไม่ส่ง
- ยังไม่อนุมัติสั่งซื้อ ให้ซ่อมก่อน
- ยังไม่อนุมัติสั่งซื้อ ให้ซ่อมก่อน — ขอใบเสนอราคาเปลี่ยนชุดดรัม
- ย้อนกลับ
- รหัสทรัพย์สิน
- รอขั้นก่อนหน้า
- รอดำเนินการ/ยังไม่แล้วเสร็จ
- รอบันทึกผลการซ่อม
- รอผลซ่อม
- รอผู้แจ้งซ่อมรับทราบ
- รอผู้แจ้งรับทราบ
- รอฝ่าย IT รับแจ้ง
- รอพิจารณา
- รอรับทราบ
- รอรับแจ้ง
- รออนุมัติ
- ระบุประเภทอุปกรณ์อื่นๆ
- ระบุรายการ
- ระบุร้านค้าที่ส่งเคลม
- ระบุสถานที่ส่งมอบ
- ระบุสาเหตุที่แก้ไขไม่ได้ และข้อเสนอ
- ระบุอาการเสีย / ปัญหา
- ระยะเวลา
- ระหว่างดำเนินการ
- รับทราบในระบบ
- รับแจ้ง
- รับแจ้งแล้ว
- รับแจ้งในระบบ
- รายการ
- รายละเอียด
- รายละเอียดผลการซ่อม
- ร่าง
- ร้านซ่อมคอมพิวเตอร์ตัวอย่าง
- ร้านอุปกรณ์คอมพิวเตอร์ตัวอย่าง
- ร้านอุปกรณ์สำนักงานตัวอย่าง
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ลายเซ็น / อนุมัติ
- ลำดับการลงชื่อ
- ล้างตัวกรอง
- วันที่
- วันที่ ........./........./.........
- วันที่ดำเนินการซ่อม
- วันที่ต้องการส่งมอบ
- วันที่ต้องการส่งมอบอยู่ก่อนวันที่แจ้ง — ส่งได้ แต่ตรวจอีกครั้ง
- วันที่ส่งเคลม
- วันสิ้นสุด
- วันสิ้นสุดก่อนวันเริ่ม
- วันสิ้นสุดก่อนวันเริ่ม — ตรวจอีกครั้ง (เตือน ไม่บล็อก)
- วันเริ่ม
- วิศวกรโรงงาน
- วิไลวรรณ ทดสอบงาน
- ศูนย์บริการตัวอย่าง (ในประกัน)
- ศูนย์บริการเปลี่ยนแผงวงจรหลัก ทดสอบเปิดใช้งานปกติ
- ส.ค.
- สถานที่ส่งมอบ
- สถานะ
- สถานะเอกสาร
- สมชาย ตัวอย่างดี
- สร้าง PDF
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สลับเป็น
- สั่งซื้ออุปกรณ์ / เปลี่ยนอุปกรณ์
- สำนักงานผู้บริหาร
- สำนักงานใหญ่ ชั้น
- สิงหาคม
- สุรชัย หัวหน้างานไอที
- สแกนแล้วภาพเอียง
- ส่งอนุมัติผลตรวจเช็ค
- ส่งอนุมัติแล้ว
- ส่งอนุมัติได้เฉพาะใบที่บันทึกผลตรวจเช็คแล้ว
- ส่งออก
- ส่งแจ้งซ่อม
- ส่งแจ้งซ่อม?
- ส่งแจ้งซ่อมแล้ว
- ส่งแจ้งซ่อมแล้วแก้ไขไม่ได้ — ฝ่าย IT จะรับแจ้งและตรวจเช็ค
- ส่งในระบบ
- ส่วนที่ 1 : สำหรับผู้แจ้งซ่อม
- หัวหน้าฝ่าย IT
- ห้องควบคุม อาคารผลิต 1
- ห้องประชุมใหญ่ ชั้น 5
- อธิบายอาการ เช่น เปิดไม่ติด จอดับ พิมพ์ไม่ออก
- อนุมัติ
- อนุมัติ (ขั้น
- อนุมัติโดย
- อรุณี ทดลองใช้
- อา
- อาการเสีย / ปัญหา
- อาคารผลิต 2
- อื่นๆ
- อื่นๆ:
- อุปกรณ์กลับมาใช้งานได้แล้ว
- ฮาร์ดดิสก์มีเสียงดัง เครื่องค้างบ่อย
- เครื่อง Workstation ห้องควบคุม
- เครื่องคอมพิวเตอร์ห้องประชุม
- เครื่องพิมพ์ฝ่ายบัญชี
- เครื่องพิมพ์เลเซอร์ ฝ่ายขาย
- เครื่องสแกนเอกสาร
- เจ้าหน้าที่ IT
- เจ้าหน้าที่ขาย
- เจ้าหน้าที่บัญชี
- เจ้าหน้าที่บุคคล
- เช่น สำนักงานใหญ่ ชั้น 3 ฝ่ายบัญชี
- เช่น โน้ตบุ๊ก 14 นิ้ว (เครื่องประจำตำแหน่ง)
- เดือนถัดไป
- เด้งกลับบน
- เปิดโปรแกรมประชุมออนไลน์แล้วไม่มีเสียง
- เพิ่มเติม
- เม.ย.
- เมษายน
- เมาส์ไร้สาย
- เมาส์ไร้สาย ฝ่ายบุคคล
- เลขที่เอกสาร
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกประเทศ
- เลือกประเภทอุปกรณ์
- เลือกผลการซ่อม
- เลือกผลของการตรวจเช็ค/ซ่อม
- เลือกผู้พิจารณา
- เลือกวันที่
- เลือกวันที่ดำเนินการซ่อม
- เลือกวันที่ต้องการส่งมอบ
- เลือกวันที่ส่งเคลม
- เลือกวันสิ้นสุด
- เลือกวันเริ่ม
- เหตุผลที่ยกเลิก
- เอกสารแนบ
- แก้ไขร่าง
- แก้ไขเรียบร้อย
- แก้ไขเอกสาร
- แก้ไขใบแจ้งซ่อม
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งซ่อม
- แจ้งซ่อมซ้ำกับใบอื่น
- แจ้งซ่อมอุปกรณ์คอมพิวเตอร์
- แจ้งซ่อมเมื่ออุปกรณ์คอมพิวเตอร์มีปัญหา
- แจ้งฝ่าย IT ว่าต้องแก้อะไร
- แท็บเล็ตบันทึกการผลิต
- แท็บเล็ตไลน์ผลิต 3
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบตเตอรี่บวม ฝาเครื่องปิดไม่สนิท
- แบบฟอร์มใบแจ้งซ่อมอุปกรณ์คอมพิวเตอร์
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- แป้นพิมพ์บางปุ่มกดไม่ติด
- โน้ตบุ๊ก 14 นิ้ว (เครื่องประจำตำแหน่ง)
- โน้ตบุ๊กทีมขาย เครื่องที่ 2
- โน้ตบุ๊กผู้จัดการฝ่ายขาย
- โน้ตบุ๊กสำรองฝ่ายบัญชี
- ใบรับเครื่องซ่อม ร้านตัวอย่าง.pdf
- ใบแจ้งซ่อมของฉัน
- ใส่เมื่อส่งแจ้งซ่อม
- ให้หาร้านซ่อมเทียบราคา
- ไม่บังคับ — บางอุปกรณ์ไม่มีป้ายทรัพย์สิน
- ไม่บังคับ — เช่น เปลี่ยนอะไหล่อะไร
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่ยกเลิก
- ไม่สามารถแก้ไขได้
- ไม่อนุมัติ
- ไม่อนุมัติ — กลับร่างผลตรวจเช็ค
- ไม่อนุมัติ — ส่งกลับร่างผลตรวจเช็ค
- — คุณเป็นผู้พิจารณาใบนี้

## §10 Data Binding & BACKEND anchors
| จุดในโค้ด | API (02_API) |
|---|---|
| `listRows()` `listBase()` `RECS.filter(canSee)` | API-01 |
| `openView()` | API-02 |
| `persist()` (+ ENG-DOC-NUM ครั้งแรก) | API-03 / API-04 |
| `confirmReport()` | API-05 (crr_reported) |
| `confirmReceive()` | API-06 (crr_received) |
| `saveInspect()` `validateInspect()` | API-07 |
| `openSubmit()` · `confirmSubmit()` (`resolveDoa()`) | API-08 / API-09 |
| `confirmApprove()` · `confirmReason()` reject | API-10 |
| `confirmRepair()` | API-11 (crr_repaired) |
| `confirmAck()` | API-12 |
| `confirmReason()` cancel | API-13 (crr_cancelled) |
| `docPrintData()` + `tplRender()` + `CRR_TPL` · `genPdf()` · `exportCSV()` | API-14 (server render template เดียวกัน) |
| `tplSignRows()` | sign_rows = ผู้ดำเนินการ + 1 ช่อง/ขั้น DOA (DEC-07) |
| `pickFiles()` `gateFiles()` | API-15 |
markers: DOA-ENGINE-HOOK, ENG-DOC-NUM, ENG-NOTIFY

## §11 Traceability + Drift Log
| Brief | FRD | HTML |
|---|---|---|
| §4 P-01 | 01 P-01 · API-01/14 | `renderPage()` |
| §4 P-02 | 01 P-02 · API-03/04/15 · BR-01..03 | `renderWizard()` |
| §4 P-03 | 01 P-03 · API-02/05..13 | `renderViewDrawer()` · `renderModal()` |
| §8 | 05 §5.3 · 07 §7.2 | `DOC_ST` · `curStep()` |
| Drift | ชนิด | ข้อเสนอ |
|---|---|---|
| D-01 | prototype-only: `__QA__` · `switchPersona()` · `S.sim` · mock `EMP`/`RECS` | ระบบจริงไม่ต้องมี |
| D-02 | prototype-only: `__QA__.openSubmit` เปิด modal ส่งอนุมัติแบบ preview จากใบที่ไม่ใช่ inspecting (ให้ e2e_standard นับช่อง DOA ได้) — ยืนยันส่งไม่เปลี่ยนสถานะ | ระบบจริงส่งอนุมัติจาก inspecting เท่านั้น (FRD FN-06) |

## §12 Diff จากเวอร์ชันก่อน
— ไม่มีใน HTML นี้ (เวอร์ชันแรก)

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- ค้นประวัติซ่อมตามรหัสทรัพย์สิน (Phase 2 · ผูกทะเบียนทรัพย์สิน · DEC-02)
- ปุ่ม "เปิดใบขอซื้อ" เมื่อผลตรวจเช็ค = สั่งซื้ออุปกรณ์ (Phase 2 · OQ-05)
- ตัวนับวันรอ (SLA) ในรายการสำหรับฝ่าย IT
