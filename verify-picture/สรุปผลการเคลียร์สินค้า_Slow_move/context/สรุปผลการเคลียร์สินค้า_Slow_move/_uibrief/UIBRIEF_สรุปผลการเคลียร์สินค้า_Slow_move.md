# UI BRIEF — F-TMP-003 สรุปผลการเคลียร์สินค้า Slow move

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| HTML | `feature.html` (html-generator-v9.4 · archetype `Q-form` · `window.__QA__` มี) · audit FAIL 0 · jsdom smoke 44/44 · [NO-BROWSER] e2e/screenshot ยังไม่รัน |
| FRD | FRD_F-TMP-003_Pack (00–07 · frd_lint BLOCK 0 · WARN 0) |
| DECISIONS | DECISIONS.lock REQ-TMP-003 — 15 มติ (AI-DEFAULT 11 · VALID 4) |
| Prototype-only | `window.__QA__` · ตัวสลับผู้ใช้ (`switchPersona()`) · `S.sim` (`commitRejected()`) · seed `RECS` · `PRODUCTS` / `SLOWMOVE_CONFIG` mock — ไม่ทำในระบบจริง (Drift Log) |
| Drift | 2 รายการ (ดู §11) |

## §1 Design Tokens AS-BUILT
CI CUBE Warm Light (BASE-KIT ห้ามแก้) · font Noto Sans Thai + Satoshi · icon Lucide 0.469.0 (multi-CDN loader) · scrollbar 5px
| CSS variable | ค่า |
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
| `--c-placeholder` | `#B4B6BC` |
| `--z-content` | `1` |
| `--z-sticky` | `10` |
| `--z-shell` | `10` |
| `--z-dropdown` | `30` |
| `--z-backdrop` | `50` |
| `--z-drawer` | `51` |
| `--z-modal` | `60` |
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
| ค่า | selector |
|---|---|
| `var(--z-shell)` | /* ============== SIDEBAR ============== */ .sidebar |
| `var(--z-sticky)` | /* ============== SHELL BAR ============== */ .shell-bar |
| `var(--z-dropdown)` | /* User dropdown menu */ .user-menu |
| `var(--z-sticky)` | .table-wrap thead th |
| `var(--z-dropdown)` | * เมนูที่ portal ออกจาก scroll container (ใช้คู่ portalMenu util) */ .menu-fixed |
| `var(--z-backdrop)` | .ss-list |
| `3` | .table-scroll.is-sticky thead th |
| `2` | .stepper-circle |
| `1` | .stepper-item:not(:last-child)::after |
| `var(--z-backdrop)` | .drawer-backdrop |
| `var(--z-drawer)` | .drawer |
| `var(--z-backdrop)` | รมีปุ่ม action หลัก */ /* ============== MODAL ============== */ .modal-backdrop |
| `var(--z-toast)` | /* ============== TOAST ============== */ .toast |
| `var(--z-sticky)` | .wizard-footer |
| `var(--z-dropdown)` | .info-tip::after |
| `var(--z-modal)` | ทัดนี้เท่านั้น ===== */ /* v9.1 Rule #62 — modal เหนือ drawer */ .modal-backdrop |
| `var(--z-drawer)` | #drawer |
| `var(--z-backdrop)` | #drawerBackdrop |
| `var(--z-toast)` | #toast |
| `var(--z-portal)` | .bd-pop |
| `var(--z-popover)` | /* row menu ⋮ (portal ใน #overlay-root) */ .row-menu |
| `var(--z-modal)` | /* v9.1 Rule #62 — modal เหนือ drawer */ .modal-backdrop |
| `var(--z-drawer)` | #drawer |
| `var(--z-backdrop)` | #drawerBackdrop |
| `var(--z-toast)` | #toast |
| `var(--z-popover)` | /* row menu ⋮ (portal ใน #overlay-root) */ .row-menu |

## §2 Route Map
| Route | หน้า | handler |
|---|---|---|
| `#/slow-move` | P-01 รายการ (default) | `applyRoute()` · `renderPage()` |
| `#/slow-move/create` · `#/slow-move/create/copy-:id` | P-02 สร้าง | `startWizard()` |
| `#/slow-move/edit/:id` | P-02 แก้ไข | `startWizard()` (เฉพาะเจ้าของ · draft/returned) |
| `#/slow-move/view/:id` | P-03 ดู | `openView()` · `showDrawer()` (ไม่มีสิทธิ์ = ไม่เปิด) |
refresh-safe: `hashchange` → `applyRoute()` · ปิด drawer → `go(RT)` (RT = `slow-move`)

## §3 Layout Shell
sidebar `#sidebar` (โมดูล "คลังสินค้า" → "เคลียร์สินค้า Slow move" + `#sbBadge` = จำนวนใบรอฉันอนุมัติ) · shell-bar (breadcrumb Core › คลังสินค้า › เคลียร์สินค้า Slow move · กระดิ่ง · user chip `#ucAv` = icon คน + เมนูสลับผู้ใช้ `#userMenu`) · เนื้อหา `#page-content`

## §4 Page Anatomy
### P-01 รายการ — `renderPage()`
`.ph` (ชื่อ + `.ph-count` + `.ph-sub` · ปุ่ม `exportCSV()` · `#btnCreate`) → แถบแดงเมื่อ `DOC.active` = false → `.seg` (`segTabs()` · `.seg-btn` ทั้งหมด/รอฉันอนุมัติ) → `.card` `.filter-bar` (ค้นหา `#fq` · `#ss-fst` สถานะ · search-select `fmo` เดือน · ล้างตัวกรอง `resetFilters()`) → `.table` (คอลัมน์ เลขที่ · ประจำเดือน · ผู้จัดทำ `personInline()` · รายการ · เคลียร์แล้ว · หมดอายุแล้ว `.ng-n` · สถานะ · ลายเซ็น `renderSignProgress()` · ⋮ `openRowMenu()`) → `pager()` 25/หน้า · แถวว่าง = `emptyStateHTML()`
### P-02 สร้าง/แก้ไข — `renderWizard()` (drawer `.wide`)
หัว + `stepper()` 3 ขั้น → ขั้น 1 `wizMain()`: `.wz-split` = ซ้าย การ์ด ① (`#ss-fmon` เดือน `setMonth()`) · การ์ด ② ตาราง `.ln-wrap` > `.ln-table` (`lineRow()` ต่อแถว: `#ss-ip{i}` สินค้า `setItem()` + `.ln-sub` รายละเอียด/หน่วย · `bedateHTML()` key `fd{i}` วันที่ติดตาม · `#ss-im{i}` แนวทาง + `.ln-note` · key `cd{i}` วันที่ · `#qt{i}` จำนวน · key `ed{i}` วันหมดอายุ · `#rm{i}` หมายเหตุ · ปุ่มลบ `removeItem()`) · `.ln-err` / `.ln-warn` ใต้ช่อง · `.ln-foot` ปุ่ม `#btnAddItem` `addItem()` · ขวา `sumCard()` `.wz-sum` → ขั้น 2 `wizAttach()` (upload `#smcFile` `pickFiles()`) → ขั้น 3 `wizReview()` (`itemsTable()`) · footer: ย้อนกลับ · ยกเลิก · `#btnDraft1`/`#btnDraft` `saveDraft()` · `#btnNext` `wizNext()` · `#btnSaveSubmit` `saveAndSubmit()`
### P-03 ดู — `renderViewDrawer()` (drawer 920)
หัว lean (เลขที่ + pill สถานะ · sub ประจำเดือน · เคลียร์แล้ว) + ปุ่มตามสถานะ → `.drawer-tabs` (`tabBtn()`) → `renderDetailTab()` (`viewBanner()` · แถบหมดอายุ · ข้อมูลเอกสาร · ผู้จัดทำ · `itemsTable()` · ไฟล์แนบ · ข้อมูลระบบ) / `renderPdfTab()` (`.pdf-slot` iframe `fitPdf()`) / `renderSignTab()` / `renderHistoryTab()`

## §5 Component Inventory
| Component | anchor | states |
|---|---|---|
| segmented tabs | `.seg-btn` · `setStat()` | default · `.on` (dot primary + count) · hover |
| ตารางกรอกรายการ | `.ln-table` · `lineRow()` | แถวปกติ · `tr.is-bad` (มี error) · `.ln-err` ข้อความแดงใต้ช่อง · `.ln-warn` ส้ม (หมดอายุแล้ว/รหัสซ้ำ) · ปุ่มลบ disabled เมื่อเหลือ 1 แถว |
| เลือกสินค้า | `#ss-ip{i}` · `searchSelectHTML()` · `initSearchSelect()` | Product Master active · label "รหัส · ชื่อ" sub หน่วย |
| แนวทางการเคลียร์ | `#ss-im{i}` + `.ln-note` | ตัวเลือก SlowMoveConfig · "อื่น ๆ (ระบุ)" → placeholder "ระบุแนวทาง *" |
| วันที่ พ.ศ. | `.bedate` · `bedateHTML()` · `.bd-pop` | ว่าง (placeholder) · มีค่า · วัน disabled ตาม min/max · ปุ่ม "วันนี้" |
| เลือกเดือน | `#ss-fmon` | 12 เดือนล่าสุด · เดือนนี้ sub "เดือนนี้" |
| สรุปขวา | `.wz-sum` · `sumCard()` | กล่องหมดอายุ `.is-off` (0) / `.is-bad` (>0) |
| ตารางรายการ (อ่าน) | `itemsTable()` | pill `pill-danger` "หมดอายุแล้ว" · `pill-warning` "ซ้ำ" · ว่าง = แผงไม่มีรายการ |
| ปุ่มบันทึก | `#btnSaveSubmit` · `busyLabel()` | default · disabled + "กำลังบันทึก…" (`S.busy`) |
| คน | `personInline()` · `empChip()` | วงกลม icon `user` mono (ไม่มี initials) |
| เมนูแถว | `.row-menu` · `openRowMenu()` | portal ใน `#overlay-root` · ปิดเมื่อคลิกนอก/scroll |

## §6 Overlay Registry
| Overlay | ขนาด | เปิด | ปิด | ห้ามปิด |
|---|---|---|---|---|
| drawer view | 920 | `openView()` | ปุ่ม X · Esc · mousedown ที่ `#drawerBackdrop` | — |
| drawer wizard `.wide` | 1290 | `startWizard()` | ปุ่ม X/ยกเลิก · Esc · backdrop → ถ้ากรอกค้าง (`S.dw.dirty`) เปิด modal ทิ้งข้อมูล | dirty |
| modal (`#modalBackdrop`) | 520 / `.is-lg` 680 (ส่ง) | `openModalCfg()` | ปุ่ม · mousedown ที่ backdrop (`modalBackdropClick()`) | มีข้อความเหตุผล/ความเห็นค้าง |
| ปฏิทิน `.bd-pop` | 280 | `bdToggle()` | คลิกนอก · Esc (ปิดแค่ปฏิทิน) · เลือกวัน | — |
| `.row-menu` | 200 | ⋮ | คลิกนอก · scroll | — |
| `.toast` (`#toast`) | — | `showToast()` | อัตโนมัติ | — |
| `.user-menu` | — | `toggleUserMenu()` | คลิกนอก | — |

## §7 Interaction Spec
- Esc chain (kit): ปิดปฏิทิน/search-select → modal → drawer ตามลำดับ handler
- backdrop ปิดด้วย `onmousedown` เมื่อ target = backdrop เท่านั้น (U25) — ลากจากในออกนอกไม่ปิด
- `render()` เก็บ/คืน scroll + focus (`preserveRenderState()`/`restoreRenderState()`) · ช่องข้อความ (`setTxt()`) ไม่ render ระหว่างพิมพ์ · จำนวน render ตอน change
- `addItem()` ยกวันที่ติดตามจากแถวก่อน + focus ช่องสินค้าแถวใหม่ · แถวว่างทั้งแถวตัดทิ้งตอน `validateMain()`
- วันที่ติดตาม/วันที่เคลียร์: ปฏิทิน max = วันนี้ · วันที่เคลียร์ min = วันที่ติดตาม · วันหมดอายุไม่จำกัด
- PDF: `genPdf()` เปิดหน้าต่างพิมพ์จาก iframe ซ่อน `.pdf-gen` (ชื่อ = เลขที่)

## §8 State-Driven UI Matrix
| สถานะ | pill | ปุ่มหัว drawer (ตามผู้ใช้) |
|---|---|---|
| draft ร่าง | `pill-muted` | เจ้าของ: ยกเลิก · แก้ไข · ส่งอนุมัติ |
| pending รออนุมัติ | `pill-warning` | ผู้พิจารณาขั้นปัจจุบัน: ไม่อนุมัติ · อนุมัติ (คำจาก `wordsOf()`) · เจ้าของ/admin: ยกเลิกเอกสาร |
| returned ไม่อนุมัติ · แก้ไข | `pill-danger` | เหมือนร่าง + แถบแดงเหตุผล |
| approved อนุมัติแล้ว | `pill-success` | — (ล็อก) |
| cancelled ยกเลิก | `pill-muted` | — |

## §9 Microcopy (verbatim)
### Toast
| variant | ข้อความ |
|---|---|
| info | `ไม่มีการแจ้งเตือนใหม่` |
| warning | `แบบเอกสารนี้ยังไม่เปิดใช้งาน` |
| warning | `แก้ไขได้เฉพาะร่างของตัวเอง` |
| warning | `กรุณากรอกข้อมูลให้ครบถ้วน` |
| warning | `กรุณากรอกข้อมูลให้ครบถ้วน` |
| info | `บันทึกร่างแล้ว ·` |
| warning | `กรุณากรอกข้อมูลให้ครบถ้วน` |
| info | `ส่งอนุมัติแล้ว ·` |
| info | `ส่งออก` |
| info | `สลับเป็น` |
| error | `แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง` |
toast แบบประกอบ: "บันทึกร่างแล้ว · {เลขที่}" · "ส่งอนุมัติแล้ว · {เลขที่}" · "อนุมัติ · {เลขที่}" · "ไม่อนุมัติ — ส่งกลับให้แก้ไขแล้ว · {เลขที่}" · "ยกเลิกเอกสารแล้ว · {เลขที่}" · "ส่งออก {n} รายการ" · "สลับเป็น {ชื่อ}"
### Placeholder
`${m && m.need_note ? 'ระบุแนวทาง *' : 'ระบุเพิ่มเติม (ถ้ามี)'}` · `${rej ? 'แจ้งผู้จัดทำว่าต้องแก้อะไร' : 'เหตุผลที่ยกเลิก'}` · `' + ph + '` · `0` · `ค้นหาเลขที่ / ผู้จัดทำ / รหัสสินค้า` · `ไม่บังคับ`
### ข้อความในจอ (สกัดจาก HTML)
- (ขั้น
- 99 อาคารตัวอย่าง ชั้น 9 ถนนตัวอย่าง แขวงตัวอย่าง เขตตัวอย่าง กรุงเทพฯ 10000
- [Lucide] All CDNs failed. Icons จะไม่แสดง but UI ยังใช้งานได้
- ]); if (canCancel(r)) items.push(['x-circle', 'ยกเลิกเอกสาร',
- ], ['printer', 'พิมพ์',
- ]]; if (isOwner(r) && isEditable(r)) items.splice(1, 0, ['pencil', 'แก้ไข',
- showToast('ไม่มีการแจ้งเตือนใหม่','info')
- · ค้าง
- · รายการเกิน
- · หมดอายุแล้ว
- · อนุมัติแล้ว ล็อกแก้ไข
- · เปิดอยู่
- · แก้แล้วส่งอนุมัติใหม่ได้ (เลขที่เดิม)
- ก.ค.
- ก.พ.
- ก.ย.
- กมลา ดูแลดี
- กรกฎาคม
- กรอกจำนวนคู่กับวันที่
- กรุณากรอกข้อมูลให้ครบถ้วน
- กล่อง
- กันยายน
- กำลังเปิดหน้าต่างพิมพ์ ·
- กุมภาพันธ์
- ขวด
- ขั้นทดสอบ
- ขายรวมล็อตให้ตัวแทน
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลหลักสรุปผล
- ข้อมูลไม่ครบหรือไม่ถูกต้อง
- ข้าม
- คลังสาขา 2
- คลังสินค้า 1
- คลังสินค้า 2
- คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
- คืนผู้ขาย
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค่าเริ่มต้นจากสายอนุมัติ
- ค่าเริ่มต้นจากสายอนุมัติและผังองค์กร
- ค้นหา...
- ค้นหารหัส / ชื่อสินค้า
- ค้นหาเลขที่ / ผู้จัดทำ / รหัสสินค้า
- จัดโปรโมชันลดราคา
- จำนวนต้องมากกว่า 0
- จำนวนที่เคลียร์ไม่ตรงหลักฐาน
- ชนิดไฟล์ไม่รองรับ
- ชิ้น
- ชื่อ-สกุล
- ชื่อฟังก์ชัน
- ซอง
- ซ้ำ
- ดาวน์โหลด PDF
- ต.ค.
- ตรวจสอบและยืนยัน
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตำแหน่ง
- ตุลาคม
- ต้อง
- ต้องระบุแนวทาง
- ถึง
- ถุง
- ทำซ้ำ
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ทำลายตามขั้นตอน
- ทุกสถานะ
- ทุกเดือน
- ธ.ค.
- ธนา บริหารดี
- ธันวาคม
- บริษัท ตัวอย่าง จำกัด (มหาชน)
- บันทึกผิดเดือน
- บันทึกร่างแล้ว ·
- บันทึกสินค้าอย่างน้อย 1 รายการ
- บันทึกแบบร่าง
- บันทึกแบบร่างได้ · ส่งอนุมัติแล้วแก้ไขไม่ได้จนกว่าผู้อนุมัติส่งกลับ
- ประจำเดือน
- ประวัติ
- ประวัติ (append-only)
- ประเสริฐ มั่นคง
- ปิด
- ผลการเคลียร์ไม่ครบ
- ผลิตภัณฑ์ตัวอย่าง A ขนาด 500 มล.
- ผลิตภัณฑ์ตัวอย่าง B ขนาด 1 ลิตร
- ผลิตภัณฑ์ตัวอย่าง C แพ็ก 6
- ผลิตภัณฑ์ตัวอย่าง D ขนาด 250 กรัม
- ผลิตภัณฑ์ตัวอย่าง E กล่อง 12 ชิ้น
- ผลิตภัณฑ์ตัวอย่าง F ขนาด 2 กก.
- ผลิตภัณฑ์ตัวอย่าง G ถุง 1 กก.
- ผลิตภัณฑ์ตัวอย่าง H ขวด 750 มล.
- ผลิตภัณฑ์ตัวอย่าง J ขนาด 5 ลิตร
- ผลิตภัณฑ์ตัวอย่าง K รุ่นเก่า
- ผู้จัดการคลังสินค้า 1
- ผู้จัดการคลังสินค้า 2
- ผู้จัดการฝ่ายคลังสินค้า
- ผู้จัดทำ
- ผู้ส่ง
- ผู้อนุมัติ
- ฝ่ายคลังสินค้า
- พ.ค.
- พ.ย.
- พฤ
- พฤศจิกายน
- พฤษภาคม
- พิมพ์
- ภาพทำลายสินค้าหมดอายุ ส.ค..pdf
- ม.ค.
- มกราคม
- มาลี ใจดี
- มิ.ย.
- มิถุนายน
- มี.ค.
- มีนาคม
- ยกเลิก
- ยกเลิกเอกสาร
- ยกเลิกเอกสารแล้ว ·
- ยังไม่ถึงขั้นนี้
- ยังไม่มีข้อมูล
- ยังไม่มีสรุปผลการเคลียร์สินค้า Slow move
- ยังไม่ส่ง
- ยังไม่ได้บันทึกสินค้า Slow move ในใบนี้
- ย้อนกลับ
- รอผล
- รอพิจารณา
- รออนุมัติ
- ระบุวันที่คู่กับจำนวน
- ระบุวันที่ติดตาม
- รายการ
- รายการ · เคลียร์แล้ว
- รายละเอียด
- ร่าง
- ลบรายการ
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ลายเซ็น / อนุมัติ
- ลำดับการอนุมัติ
- ล้างตัวกรอง
- วรรณา ขยันยิ่ง
- วันที่ ........./........./.........
- วันที่ติดตามเป็นวันในอนาคตไม่ได้
- วันที่ต้องไม่ก่อนวันที่ติดตาม
- วันที่สร้าง
- วันที่เป็นวันในอนาคตไม่ได้
- ศิริพร จัดการดี
- ส.ค.
- สถานะ
- สถานะเอกสาร
- สมศักดิ์ รอบคอบ
- สรุปผลการเคลียร์สินค้า Slow move
- สร้าง PDF
- สร้างสรุปผลการเคลียร์สินค้า Slow move
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างโดย
- สร้างใบสรุป
- สร้างใบสรุปของเดือนนี้ แล้วบันทึกสินค้าที่ติดตามและผลการเคลียร์
- สลับเป็น
- สำนักบริหาร
- สิงหาคม
- สินค้านี้ปิดใช้งานแล้ว
- ส่งอนุมัติ
- ส่งอนุมัติ?
- ส่งอนุมัติแล้ว ·
- ส่งออก
- ส่งในระบบ
- หน่วย
- หน่วยงาน
- หมดอายุแล้ว
- หัวหน้าหน่วยธุรกิจ
- อนุมัติ
- อนุมัติแล้ว
- อนุมัติแล้ว — ปิดใบสรุปประจำเดือน (ไม่ตัดสต็อก)
- ออกใบซ้ำ
- ออกใบซ้ำ — ใช้ใบ SMC-2569-0003
- อา
- อื่น ๆ (ระบุ)
- เคลียร์แล้ว
- เจ้าหน้าที่คลังสินค้า
- เดือนถัดไป
- เดือนนี้
- เด้งกลับบน
- เพิ่มเติม
- เม.ย.
- เมษายน
- เลขที่
- เลขที่เอกสาร
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกประเทศ
- เลือกผู้พิจารณา
- เลือกวันที่
- เลือกสินค้า
- เลือกเดือน
- เลือกเดือน แล้วบันทึกสินค้า Slow move ที่ติดตาม พร้อมผลการเคลียร์ (วันที่ + จำนวน) — ยังเคลียร์ไม่ได้ เว้นว่างไว้ได้
- เลือกแนวทาง
- เลือกแนวทางการเคลียร์
- เหตุผลที่ยกเลิก
- เอกสารแนบ
- แกลลอน
- แก้ไข
- แก้ไขข้อมูล
- แก้ไขล่าสุด
- แก้ไขเอกสาร
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งผู้จัดทำว่าต้องแก้อะไร
- แถว
- แถว หน้า 2 อาจล้น
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แนวทางการเคลียร์ไม่เหมาะสม
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- แพ็ก
- โอนย้ายไปคลัง/สาขาที่ขายได้
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่มี
- ไม่มีรายการสินค้า
- ไม่มีสินค้า Slow move เดือนนี้
- ไม่ยกเลิก
- ไม่อนุมัติ
- ไม่อนุมัติ · แก้ไข
- ไม่อนุมัติ — กลับให้ผู้จัดทำแก้ไข
- ไม่อนุมัติ — ส่งกลับให้แก้ไขแล้ว ·
- — คุณเป็นผู้อนุมัติใบนี้

## §10 Data Binding & BACKEND anchors
| จุดใน prototype | ระบบจริง |
|---|---|
| `RECS` / `mkRec()` | API-01/02 |
| `PRODUCTS` · `prodOf()` | API-13 Product Master (F-PRODUCT-MASTER-001 · snapshot ลงแถว) |
| `SLOWMOVE_CONFIG` · `methodOf()` · `methodText()` | API-12 SlowMoveConfig.clearance_methods (snapshot ลงแถว) |
| `itemErrors()` · `validateMain()` | FN-01 (422 + warnings) |
| `persist()` | API-03/04 (ENG-DOC-NUM ตอนบันทึกครั้งแรก) |
| `MOCK_DOA_RESOLVED` · `resolveDoa()` (DOA-ENGINE-HOOK) | API-05/06 `GET /doa/resolve?feature_id=F-TMP-003` |
| `confirmApprove()` · `confirmReason()` | API-07/08 |
| `docPrintData()` + `SMC_TPL` + `tplRender()` + `PRINT_CFG` | API-09 render ฝั่ง server (data contract + print_config เดียวกัน) |
| `exportCSV()` | API-10 |
| `DOC.active` | F-DOCCFG status |

## §11 Traceability + Drift Log
| Brief | FRD | HTML |
|---|---|---|
| §4 P-01 | 01 P-01 · API-01/10 · FN-11 | `renderPage()` |
| §4 P-02 | 01 P-02 · API-03/04/12/13 · FN-01..04 · BR-01..07 | `renderWizard()` |
| §4 P-03 | 01 P-03 · API-02/05..09 · FN-05..09 | `renderViewDrawer()` |
| §6 modal ส่ง/ตัดสิน/ยกเลิก | 05 §5.2 · BR-DOA-01..04 | `renderModal()` |
**Drift Log**
| # | ชนิด | รายการ | ข้อเสนอ |
|---|---|---|---|
| D-01 | HTML-only | ปุ่ม "ทำซ้ำ" (archetype · ยกแถวที่ยังเคลียร์ไม่ได้) ขณะที่ DEC-11 = ทำซ้ำ ✗ | ซ่อนในระบบจริง หรือให้ลูกค้ายืนยัน (OQ-06) |
| D-02 | HTML-only (prototype) | `window.__QA__` · สลับผู้ใช้ · `S.sim` | ไม่ทำในระบบจริง |

## §12 Diff จากเวอร์ชันก่อน
— ไม่มีใน HTML นี้ (เวอร์ชันแรก)

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- ช่องคลัง/คงเหลือก่อนเคลียร์/หน่วยนับ (OQ-03) · ปุ่ม "สร้างใบปรับปรุงสต็อก/โอนย้าย/คืนผู้ขาย" จากแถวที่อนุมัติ (Phase 2) · ดึงรายการ Slow move อัตโนมัติจาก Inventory
