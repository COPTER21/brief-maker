# UI_BRIEF — F-TMP-006 รายงานการเข้า-ออก ห้อง server (AS-BUILT)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| HTML (source of truth) | feature.html · html-generator-v9.4 Golden Skeleton · archetype `Q-form` (`<meta name="cube-archetype">`) · audit FAIL 0 · [NO-BROWSER] e2e_standard ข้าม → jsdom smoke 46/46 |
| FRD | FRD_F-TMP-006_Pack v1.0 (STANDARD) · DECISIONS.lock 14 มติ (DEC-01..14 · AI-DEFAULT) |
| Prototype-only | `window.__QA__` · ตัวสลับผู้ใช้ `switchPersona()` · `S.sim` / `commitRejected()` · `EMP`/`RECS` mock → ไม่ต้องสร้างในระบบจริง (Drift Log D-01) |
| Drift | 0 business drift · 3 prototype-only (§11) |

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
| `--z-portal` | `1000` |

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
| `#/server-room-access` | P-01 รายการ (default) | `applyRoute()` · `renderPage()` |
| `#/server-room-access/create` | P-02 สร้าง | `startWizard()` |
| `#/server-room-access/edit/:id` | P-02 แก้ร่าง (เจ้าของ · draft) | `startWizard()` |
| `#/server-room-access/view/:id` | P-03 ดู (เฉพาะ `canSee`) | `openView()` · `showDrawer()` |
refresh-safe ผ่าน `hashchange` → `applyRoute()` · route ใบไม่มีสิทธิ์ = ไม่เปิด drawer

## §3 Layout Shell
`.sidebar` (`--sidebar-w`) โมดูล IT Support › เข้า-ออกห้อง server + badge `#sbBadge` (= ร่างของฉัน) · `.shell-bar` (`--shell-h`) breadcrumb Core › IT Support › เข้า-ออกห้อง server · `.user-chip` (วงกลมรูปคน `.avatar-person`) + `.user-menu` · content `#page-content`

## §4 Page Anatomy
### P-01 รายการ — `renderPage()`
`.ph` (ชื่อ + `.ph-en` · sub + `.ph-badge` จำนวน — **ไม่มี scorecard** U1) · ปุ่ม `exportCSV()` / `#btnCreate` → `startWizard()` · แท็บสถานะ `segTabs()` `.seg` `.seg-btn` `.seg-n` → `setListTab()` (U20 · ไม่มี dropdown สถานะซ้ำ) · `.filter-bar` (`#fq` `onQ()` · search select `fres` (สถานะรับรอง) `fby` ผ่าน `initSearchSelect()` · รีเซ็ต `resetFilters()`) · `.table-wrap .table` คอลัมน์ `sortTh()` → `sortBy()` · ผู้บันทึก `personInline()` · รอรับรอง `.is-flag` · แถว `rowClick()` · ⋮ `openRowMenu()` (portal `#overlay-root` `.row-menu`) · `pager()` (`.pg-size` `setPageSize()` · `.tf-info` · `goPage()` · `.pg-dots`) · ว่าง `emptyStateHTML()`
### P-02 สร้าง/แก้ — `renderWizard()` (drawer `.drawer.wide`)
`stepper()` 3 ขั้น (`STEPS`) · ขั้น 1 `wizMain()`: `.wz-split` → `.wz-main` (การ์ด ① `.chk-edit` `.chk-tbl` แถว `entRow()` `#cr-i` · ชื่อ `[name=name-i]` + `datalist#empNames` → `setName()` (พนักงาน = เติมฝ่าย) · `[name=dept-i]` · วันที่เข้า/ออก `bedateHTML()` (`ci`/`co` · พ.ศ. · max วันนี้ · `setRowDate()`) · เวลา `[name=inTime-i]` `[name=outTime-i]` blur `fmtTimeEl()` (`normTime()` HH:MM) · `[name=purpose-i]` · `setRow()` · ลายเซ็น `.sig-at` อ่านอย่างเดียว · `.add-row` `addRow()` / `removeRow()` · ② `#resLine` `#resText` `#resHint` `entSentence()` `entHint()`) + `sumCard()` (`#sumPeriod` `#sumDays` `#sumAbn`) · อัปเดตสด `softSums()` (ไม่ rebuild · ไฮไลต์ `.is-warnrow`) · ตรวจ `validateMain()` (`entryOrderBad()` บล็อก) · ขั้น 2 `wizAttach()` (`#sralFile` `pickFiles()` `gateFiles()`) · ขั้น 3 `wizReview()` · footer `#btnNext` `wizNext()` / `#btnDraft` `saveDraft()` / `#btnSaveSubmit` `saveAndSubmit()`
### P-03 ดู — `renderViewDrawer()`
หัว `.dw-head` (เลขที่ · `docPill()` · sub 2 fact: ช่วงวันที่ · รอรับรอง) · ปุ่ม `#btnSubmitView` `openSubmit()` / `openCancel()` · `.drawer-tabs` `tabBtn()` → `renderDetailTab()` (`entriesTable()` `.chk-view` · `certCell()` ปุ่ม `#btnCert-{entryId}` → `openCertify()` · `resultBlock()` `.abn-list`) · `renderPdfTab()` (`.pdf-slot` iframe `fitPdf()` · `genPdf()`) · `renderSignTab()` (`.checker-list` `.sig-pair`) · `renderHistoryTab()` (`.tl-q`)

## §5 Component Inventory
| Component | anchor | states |
|---|---|---|
| ตารางกรอกการเข้า-ออก | `.chk-tbl` `entRow()` | default · `.is-warnrow` (เกินเวลา — เตือน) · `.is-bad` ต่อช่อง (invalid) · แถวรับรองแล้ว = disabled · ลบ (เมื่อ >1 แถวและยังไม่รับรอง) |
| ช่องชื่อผู้เข้า | `[name=name-i]` + `#empNames` | พนักงาน (เติมฝ่าย · `empId`) · บุคคลภายนอก (พิมพ์เอง) |
| ตัวเลือกวัน พ.ศ. | `.bedate` + `.bd-pop` | ว่าง · เลือกแล้ว · `.is-bad` (ใน `.cr-date`) |
| ช่องลายเซ็นผู้รับรอง | `certCell()` | รับรองแล้ว (`.sig-cell` ชื่อ + เวลา) · ปุ่มรับรอง (มีสิทธิ์) · ป้าย "ยังอยู่ในห้อง"/"รอรับรอง" `pill-warning` |
| บรรทัดผลรวม | `.pd-line` | ปกติ · `.is-warn` (เกินเวลา) |
| การ์ดสรุป | `.wz-sum` `.wz-sum-total` | ปกติ · `.is-warn` (ยังอยู่ในห้อง) |
| คน | `.emp-av` `empChip()` `nameChip()` `personInline()` | วงกลมรูปคน mono (U17) |
| แท็บสถานะ | `.seg-btn` | ปกติ · `.on` (dot primary + count) |
| progress ลายเซ็น | `renderSignProgress()` | 0 ขั้น = "ไม่มีขั้นอนุมัติ" · ร่าง = — · n/N |
| slot ผู้พิจารณา | `.slot-row` + search select slot{i} | แสดงเมื่อ DOA มีขั้น · `.is-invalid` |
| ปุ่ม busy | `busyLabel()` | loading "กำลังบันทึก…" · disabled |

## §6 Overlay Registry
| Overlay | anchor | ขนาด | ปิดด้วย |
|---|---|---|---|
| drawer สร้าง/แก้ | `#drawer.drawer.drawer-panel.wide` + `#drawerBackdrop` | wide 1290 | ปุ่ม/Esc/mousedown ที่ backdrop (`drawerBackdropDown()`) · **กรอกค้าง → modal ทิ้งข้อมูล** |
| drawer ดู | `#drawer.drawer-panel` | 920 | ปุ่ม ปิด/Esc/backdrop |
| modal รับรอง/ส่งปิดรอบ | `#modal.modal.is-lg` (`#btnCertify` · `#btnSubmit` · `#submitBlock`) | lg | ยกเลิก · Esc · mousedown ที่ backdrop (`modalBackdropDown()` — มีข้อความค้างห้ามปิด · ลากจากในกล่องไม่ปิด U25) |
| modal ยกเลิก/ทิ้ง | `#modal` | md | เช่นเดียวกัน |
| เมนู ⋮ | `.row-menu` (portal) | 180px | คลิกนอก · scroll |
| search list | `.ss-list.menu-fixed` | | Esc · คลิกนอก |
| ปฏิทิน พ.ศ. | `.bd-pop` (portal `--z-portal`) | 280px | Esc (ปิดแค่ปฏิทิน) · คลิกนอก |
| toast | `#toast.toast` | | อัตโนมัติ |
| user menu | `.user-menu` | | คลิกนอก |

## §7 Interaction Spec
Esc chain: ปฏิทิน/ search list เปิด → ปิดก่อน (capture · stopPropagation) → `state.modal.open` → `closeModal()` → `state.drawer.open` → `closeDrawer()` · คลิกนอกปิด `.row-menu` / `.user-menu` · `addRow()` focus ช่องชื่อแถวใหม่ (rAF) · พิมพ์ในตารางไม่ rebuild (`softSums()` · focus ไม่หลุด) · เลือกวันที่ = rebuild (`setRowDate()`) · กรอกเวลาออกโดยไม่มีวันที่ออก → วันที่ออก = วันที่เข้า · แก้ร่างจาก view = ปิด view ก่อน (U15) · รับรองไม่มีสิทธิ์ → toast เหตุผล (`certBlockReason()`) · `preserveRenderState()`/`restoreRenderState()` คืน scroll/focus หลัง render

## §8 State-Driven UI Matrix
| status | pill | ปุ่มหัว (ผู้มีสิทธิ์) |
|---|---|---|
| draft | ร่าง `pill-muted` | เจ้าของ: ยกเลิก · แก้ไข · ส่งปิดรอบ · ปุ่มรับรองต่อแถว (role-it-officer ≠ ผู้เข้า) |
| pending (โครง archetype · dormant — DEC-03) | รอตรวจทาน `pill-warning` | ไม่เกิดในรอบนี้ (ไม่มีขั้นพิจารณา) |
| submitted | ปิดรอบแล้ว `pill-success` | เจ้าของ/admin: ยกเลิกเอกสาร · (ล็อกแก้ไข/รับรอง) |
| cancelled | ยกเลิก `pill-danger` | — |
จำนวนขั้นมาจาก DOA (`resolveDoa()` · `MOCK_DOA_RESOLVED` = 0 ขั้น ตาม DEC-03) · ส่งปิดรอบบล็อกตาม `submitBlockers()`

## §9 Microcopy (verbatim)
### toast
- `กรุณากรอกข้อมูลให้ครบถ้วน`
- `บันทึกร่างแล้ว ·`
- `ยังส่งปิดรอบไม่ได้ —`
- `รับรองแล้ว ·`
- `สลับเป็น`
- `ส่งออก`
- `แก้ไขได้เฉพาะร่างของตัวเอง`
- `แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง`
- `แบบเอกสารนี้ยังไม่เปิดใช้งาน`
- `ไม่มีการแจ้งเตือนใหม่`
- ประกอบ: `ปิดรอบแล้ว · {เลขที่}` · `รับรองแล้ว · {ชื่อ}` · `ยกเลิกเอกสารแล้ว · {เลขที่}` · `ยังส่งปิดรอบไม่ได้ — …` · `ส่งออก {n} รายการ` · `สลับเป็น {ชื่อ}`
### ข้อความบนจอ (สกัดจาก HTML)
- (ขั้น
- 0 รายการ
- [Lucide] All CDNs failed. Icons จะไม่แสดง but UI ยังใช้งานได้
- ]); if (canCancel(r)) items.push(['x-circle', 'ยกเลิกเอกสาร',
- ], ['printer', 'พิมพ์',
- ]]; if (isOwner(r) && r.status === 'draft') items.splice(1, 0, ['pencil', 'แก้ไข',
- showToast('ไม่มีการแจ้งเตือนใหม่','info')
- · ปิดรอบแล้ว ล็อกแก้ไข
- · ออกครบทุกคน
- ก.ค.
- ก.พ.
- ก.ย.
- กมล ใจดี
- กรกฎาคม
- กรรมการผู้จัดการ
- กรุณากรอกข้อมูลให้ครบถ้วน
- กันยายน
- กำลังเปิดหน้าต่างพิมพ์ ·
- กุมภาพันธ์
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลผิดทั้งใบ จะทำใบใหม่
- ข้อมูลหลักการเข้า-ออก
- ข้อมูลเวลาออกไม่ครบ
- ข้าม
- คน
- ครั้ง
- คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค่าเริ่มต้นจากสายอนุมัติและผังองค์กร
- ค้นหา...
- ค้นหาเลขที่ / ผู้บันทึก / ผู้เข้า / เหตุผล
- จำนวนครั้ง
- ชนิดไฟล์ไม่รองรับ
- ชม. (ตั้งค่าห้อง server)
- ชื่อผู้เข้าไม่ตรงบัตร
- ชื่อฟังก์ชัน
- ชื่อ–นามสกุล
- ช่วงวันที่เข้า
- ช่างบี (หจก. แอร์สมมุติ)
- ช่างเอก (บจก. ระบบไฟตัวอย่าง)
- ซ่อมบำรุง UPS ตามสัญญา
- ดาวน์โหลด PDF
- ต.ค.
- ตรวจระบบแอร์ห้อง server
- ตรวจสอบและยืนยัน
- ตรวจเช็คอุปกรณ์ประจำวัน
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ติดตั้งสาย LAN เพิ่ม
- ตุลาคม
- ต้อง
- ถึง
- ทั้งหมด
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ทุกผู้บันทึก
- ทุกสถานะรับรอง
- ธ.ค.
- ธันวาคม
- บริษัท ตัวอย่าง จำกัด
- บันทึกการเข้าห้องอย่างน้อย 1 ครั้ง
- บันทึกซ้ำกับใบอื่น
- บันทึกซ้ำกับใบอื่น — ใช้ SRAL-2569-0003
- บันทึกทุกครั้งที่มีคนเข้าห้อง server 1 แถวต่อ 1 ครั้ง — เวลาออกเว้นว่างได้ระหว่างอยู่ในห้อง แล้วกลับมาบันทึกเมื่อออก
- บันทึกร่างแล้ว ·
- บันทึกแบบร่างเพื่อบันทึกการเข้า-ออกครั้งถัดไปต่อ · ส่งปิดรอบเมื่อทุกแถวมีเวลาออกและรับรองครบ (ส่งแล้วแก้ไขไม่ได้)
- ประวัติ
- ประเสริฐ มั่นคง
- ปิด
- ปิดรอบรายงานแล้ว
- ปิดรอบแล้ว
- ปิดรอบแล้ว ·
- ผู้จัดการฝ่ายบัญชี
- ผู้ตรวจทาน
- ผู้บริหาร
- ผู้บันทึก
- ผู้รับรอง
- ผู้รับเหมา — บจก. ระบบไฟตัวอย่าง
- ผู้รับเหมา — หจก. แอร์สมมุติ
- ผู้เข้า
- ผู้เข้ารับรองแถวของตัวเองไม่ได้
- ฝ่าย / บริษัท
- ฝ่าย/แผนก
- ฝ่ายบัญชี
- ฝ่ายเทคโนโลยีสารสนเทศ
- พ.ค.
- พ.ย.
- พฤ
- พฤศจิกายน
- พฤษภาคม
- พิมพ์
- พิมพ์หรือเลือกพนักงาน
- ม.ค.
- มกราคม
- มิ.ย.
- มิถุนายน
- มี.ค.
- มีนาคม
- มีรายการรอรับรอง
- ยกเลิก
- ยกเลิกเอกสาร
- ยกเลิกเอกสารแล้ว ·
- ยังส่งปิดรอบไม่ได้ —
- ยังไม่ปิดรอบ
- ยังไม่มีข้อมูล
- ยังไม่มีรายการเข้า-ออก
- ยังไม่มีรายงานการเข้า-ออกห้อง server
- ยังไม่ส่ง
- ยังไม่ออก
- ย้อนกลับ
- รอขั้นก่อนหน้า
- รอตรวจทาน
- รอบันทึกเวลาออกก่อนรับรอง
- รอพิจารณา
- รอรับรอง
- รอรับรองหลังบันทึก
- ระบบ
- ระบบแจ้งผู้ดูแลห้อง server — อยู่ในห้องเกินเวลา
- ระบบแจ้งเจ้าหน้าที่ IT — รอรับรอง
- รับรอง
- รับรองการเข้า-ออก
- รับรองครบ
- รับรองแล้ว
- รับรองแล้ว ·
- รับรองในระบบ (ข้อความ ไม่ใช้ภาพลายมือชื่อ)
- รับรองได้เฉพาะเจ้าหน้าที่ IT ผู้ดูแลห้อง
- รายการ
- รายการ (sral_certify_pending)
- รายการ (sral_overstay)
- รายการ · รับรองครบ
- รายการ · รับรองครบ (sral_submitted)
- รายงานการเข้า-ออก ห้อง server
- รายละเอียด
- ร่าง
- ลงชื่อ
- ลงชื่อในระบบ
- ลงชื่อในระบบเมื่อบันทึก
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ลายเซ็น / รับรอง
- ล้างตัวกรอง
- วันที่
- วันที่ ........./........./.........
- วันที่สร้าง
- วันที่ออก
- วันที่เข้า
- วันเวลาที่ออกต้องไม่ก่อนวันเวลาที่เข้า
- วิภา ดูแลระบบ
- ส.ค.
- สถานะ
- สถานะเอกสาร
- สมชาย ตัวอย่าง
- สมศรี ทดสอบ
- สมศักดิ์ ใหญ่ยิ่ง
- สร้าง PDF
- สร้างรายงาน
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างโดย
- สลับเป็น
- สำรองข้อมูลลงเทป
- สิงหาคม
- ส่งกลับเป็นร่างแล้ว ·
- ส่งตรวจทาน
- ส่งตรวจทานแล้ว ·
- ส่งปิดรอบ
- ส่งปิดรอบรายงาน
- ส่งปิดรอบรายงาน?
- ส่งออก
- หัวหน้าฝ่ายเทคโนโลยีสารสนเทศ
- อนุมัติ
- อา
- เกณฑ์เวลาอยู่ในห้อง
- เจ้าหน้าที่บัญชี
- เจ้าหน้าที่ระบบเครือข่าย
- เจ้าหน้าที่ไอที
- เช่น เปลี่ยน HDD ใน server
- เดือนถัดไป
- เด้งกลับบน
- เปลี่ยน HDD ใน server
- เปิดรายงานใหม่แล้วบันทึกทุกครั้งที่มีคนเข้าห้อง
- เปิดใบผิดรอบ
- เพิ่มเติม
- เม.ย.
- เมษายน
- เลขที่
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกตอนส่ง
- เลือกประเทศ
- เลือกผู้พิจารณา
- เลือกวันที่
- เวลาที่ออก
- เวลาที่เข้า
- เหตุผลการเข้าใช้
- เหตุผลการเข้าใช้ไม่ชัดเจน
- เหตุผลที่ยกเลิก
- เอกสารแนบ
- แก้ไข
- แก้ไขรายงาน
- แก้ไขร่าง
- แก้ไขล่าสุด
- แก้ไขเอกสาร
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งผู้บันทึกว่าต้องแก้อะไร
- แถว
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบฟอร์ม
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- แล้ว ·
- ใบงานซ่อมบำรุง UPS ต.ค.pdf
- ใบอนุญาตเข้าพื้นที่ผู้รับเหมา ส.ค.pdf
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่มีขั้นอนุมัติ
- ไม่มีข้อมูล
- ไม่ยกเลิก
- ไม่อนุมัติ
- — คุณเป็นผู้ตรวจทานใบนี้
- — ส่งกลับเป็นร่าง (ขั้น

## §10 Data Binding & BACKEND anchors
| จุดในโค้ด | API (02_API) |
|---|---|
| `listRows()` `listBase()` `RECS.filter(canSee)` | API-01 |
| `openView()` | API-02 |
| `persist()` (+ ENG-DOC-NUM ครั้งแรก · sral_certify_pending · sral_overstay) | API-03 / API-04 |
| `openSubmit()` · `confirmSubmit()` (`submitBlockers()` · `resolveDoa()` = 0 ขั้น → ปิดรอบ) | API-05 |
| `openCertify()` · `confirmCertify()` (`canCertify()` · `sameAsVisitor()`) | API-06 |
| `confirmApprove()` · `confirmReason()` reject | — โครง archetype dormant (ไม่มี API · DEC-03 · Drift D-03) |
| `confirmReason()` cancel | API-07 |
| `docPrintData()` + `tplRender()` + `SRAL_TPL` · `genPdf()` | API-08 (server render template เดียวกัน) |
| `tplSignRows()` · `SIGN_MAX_PER_ROW` | sign_rows ว่าง = ไม่มีบล็อกลงชื่อ (DEC-07) |
| `exportCSV()` | API-09 |
| `pickFiles()` `gateFiles()` | API-10 |
| `SRAL_CFG` · `entryIssues()` · `stayHours()` | ServerRoomAccessConfig (อ่าน config · FN-02) |
markers: DOA-ENGINE-HOOK, ENG-DOC-NUM, ENG-NOTIFY, TODO

## §11 Traceability + Drift Log
| Brief | FRD | HTML |
|---|---|---|
| §4 P-01 | 01 P-01 · API-01/09 | `renderPage()` |
| §4 P-02 | 01 P-02 · API-03/04/10 · BR-01..06 · BR-14 | `renderWizard()` |
| §4 P-03 | 01 P-03 · API-02/05..08 · BR-05 | `renderViewDrawer()` |
| §8 | 05 §5.2 state · LD-01 | `DOC_ST` · `curStep()` |
| Drift | ชนิด | ข้อเสนอ |
|---|---|---|
| D-01 | prototype-only: `__QA__` · `switchPersona()` · `S.sim` · mock `EMP`/`RECS` | ระบบจริงไม่ต้องมี |
| D-02 | prototype คำนวณ issues/สิทธิ์รับรองฝั่ง FE · ระบบจริงตรวจซ้ำฝั่ง server (FRD FN-02 · FN-10) | dev ทำตาม FRD |
| D-03 | prototype-only: โครง DOA ของ archetype (`MOCK_DOA_RESOLVED` 0 ขั้น · `.slot-row` · modal ตรวจทาน/ส่งกลับ · แท็บรอตรวจทาน) — dormant (FRD LD-08) | ระบบจริงไม่ต้องสร้างรอบนี้ |

## §12 Diff จากเวอร์ชันก่อน
— ไม่มีใน HTML นี้ (เวอร์ชันแรก)

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- ปุ่ม "บันทึกเวลาออก" ด่วนจากแท็บรายละเอียด (ไม่ต้องเข้าแก้ร่าง)
- เชื่อมระบบประตู/บัตรผ่าน (Phase 2 · DEC-02)
- ช่องห้อง server (ถ้าลูกค้ามีหลายห้อง · OQ-06)
