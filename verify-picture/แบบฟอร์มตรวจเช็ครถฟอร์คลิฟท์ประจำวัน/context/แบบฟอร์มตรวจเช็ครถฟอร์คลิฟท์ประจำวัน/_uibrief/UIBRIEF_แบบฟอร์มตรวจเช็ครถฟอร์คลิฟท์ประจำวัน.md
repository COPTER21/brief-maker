# UI BRIEF — F-TMP-002 แบบฟอร์มตรวจเช็ครถฟอร์คลิฟท์ประจำวัน

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| HTML | `feature.html` (html-generator-v9.4 · archetype `Q-form` · `window.__QA__` มี) · audit FAIL 0 · jsdom smoke 27/27 · [NO-BROWSER] e2e/screenshot ยังไม่รัน |
| FRD | FRD_F-TMP-002_Pack (00–07 · frd_lint BLOCK 0) |
| DECISIONS | DECISIONS.lock REQ-TMP-002 — 17 มติ (AI-DEFAULT 13 · VALID 4) |
| Prototype-only | `window.__QA__` · ตัวสลับผู้ใช้ (`switchPersona()`) · `S.sim` (`commitRejected()`) · seed `RECS` — ไม่ทำในระบบจริง (Drift Log) |
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
| ค่า | selector |
|---|---|
| `var(--z-shell)` | /* ============== SIDEBAR ============== */ .sidebar |
| `var(--z-sticky)` | /* ============== SHELL BAR ============== */ .shell-bar |
| `var(--z-dropdown)` | /* User dropdown menu */ .user-menu |
| `var(--z-sticky)` | .table-wrap thead th |
| `var(--z-popover)` | จาก scroll container (ใช้คู่ portalMenu util) */ .menu-fixed |
| `var(--z-backdrop)` | .ss-list |
| `var(--z-popover)` | (หลุด overflow ของ modal/drawer body) */ .ss-list.menu-fixed |
| `3` | .table-scroll.is-sticky thead th |
| `2` | .stepper-circle |
| `1` | .stepper-item:not(:last-child)::after |
| `var(--z-backdrop)` | .drawer-backdrop |
| `var(--z-drawer)` | .drawer |
| `var(--z-backdrop)` | */ /* ============== MODAL ============== */ .modal-backdrop |
| `var(--z-toast)` | /* ============== TOAST ============== */ .toast |
| `var(--z-sticky)` | .wizard-footer |
| `var(--z-dropdown)` | .info-tip::after |
| `var(--z-modal)` | /* v9.1 Rule #62 — modal เหนือ drawer */ .modal-backdrop |
| `var(--z-drawer)` | #drawer |
| `var(--z-backdrop)` | #drawerBackdrop |
| `var(--z-toast)` | #toast |
| `var(--z-popover)` | /* row menu ⋮ (portal ใน #overlay-root) */ .row-menu |

## §2 Route Map
| Route | หน้า | handler |
|---|---|---|
| `#/forklift` | P-01 รายการ (default) | `applyRoute()` · `renderPage()` |
| `#/forklift/create` · `#/forklift/create/copy-:id` | P-02 สร้าง | `startWizard()` |
| `#/forklift/edit/:id` | P-02 บันทึกผล/แก้ | `startWizard()` (เฉพาะเจ้าของ · draft/returned) |
| `#/forklift/view` · `#/forklift/view/:id` | P-03 ดู | `openView()` · `showDrawer()` (ไม่มีสิทธิ์ = ไม่เปิด) |
refresh-safe: `hashchange` → `applyRoute()` · ปิด drawer → `go('forklift')`

## §3 Layout Shell
sidebar `#sidebar` (โมดูล "คลังสินค้า" → "ตรวจเช็ครถฟอร์คลิฟท์" + `#sbBadge` = จำนวนใบรอฉันตรวจสอบ) · shell-bar (breadcrumb Core › คลังสินค้า › ตรวจเช็ครถฟอร์คลิฟท์ · กระดิ่ง · user chip `#ucAv` = icon คน + เมนูสลับผู้ใช้ `#userMenu`) · เนื้อหา `#page-content`

## §4 Page Anatomy
### P-01 รายการ — `renderPage()`
`.ph` (ชื่อ + `.ph-count` + `.ph-sub` · ปุ่ม `exportCSV()` · `#btnCreate`) → แถบแดงเมื่อ `DOC.active` = false → `.seg` (`segTabs()` · `.seg-btn` ทั้งหมด/รอฉันตรวจสอบ) → `.card` `.filter-bar` (ค้นหา `#fq` · `#ss-fst` สถานะ · search-select `fvt` ประเภทรถ · ล้างตัวกรอง `resetFilters()`) → `.table` (คอลัมน์ เลขที่ · ประจำเดือน · ผู้ตรวจสอบ `personInline()` · ประเภทรถ · ตรวจแล้ว · ผิดปกติ `.ng-n` · สถานะ · ลายเซ็น `renderSignProgress()` · ⋮ `openRowMenu()`) → `pager()` 25/หน้า · แถวว่าง = `emptyStateHTML()`
### P-02 สร้าง/บันทึกผล — `renderWizard()` (drawer `.wide`)
หัว + `stepper()` 3 ขั้น → ขั้น 1 `wizMain()`: `.wz-split` = ซ้าย การ์ด ① (`.track-card` ×2 `setVtype()` + `#ss-fmon` เดือน `setMonth()`) · การ์ด ② (`dayChips()` `.day-chip` → `pickDay()` · `dayChecklist()` `.ck-row` + `.ck-btn` `setRes()` · `allOk()` · `clearDay()`) · ขวา `sumCard()` `.wz-sum` → ขั้น 2 `wizAttach()` (upload `#fliFile` `pickFiles()`) → ขั้น 3 `wizReview()` (`monthGrid()` `.grid31`) · footer: ย้อนกลับ · ยกเลิก · `#btnDraft1`/`#btnDraft` `saveDraft()` · `#btnNext` `wizNext()` · `#btnSaveSubmit` `saveAndSubmit()`
### P-03 ดู — `renderViewDrawer()` (drawer 920)
หัว lean (เลขที่ + pill สถานะ + pill ประเภทรถ · sub ประจำเดือน · ตรวจแล้ว) + ปุ่มตามสถานะ → `.drawer-tabs` (`tabBtn()`) → `renderDetailTab()` (`viewBanner()` · ข้อมูลเอกสาร · ผู้ตรวจสอบ · `monthGrid()` · `ngTable()` · ไฟล์แนบ · ข้อมูลระบบ) / `renderPdfTab()` (`.pdf-slot` iframe `fitPdf()`) / `renderSignTab()` / `renderHistoryTab()`

## §5 Component Inventory
| Component | anchor | states |
|---|---|---|
| segmented tabs | `.seg-btn` · `setStat()` | default · `.on` (dot primary + count) · hover |
| day chip | `.day-chip` · `pickDay()` | `is-none` · `is-ok` (เขียว) · `is-ng` (แดง) · `is-part` (ส้ม) · `.is-sel` (ขอบ primary) · `.is-off` disabled (วันอนาคต) |
| เช็คลิสต์ | `.ck-row` · `.ck-btn` · `setRes()` | ว่าง · `.is-ok` · `.is-ng` · แถว `.is-bad` (ไม่ครบตอน validate) · กดซ้ำ = ล้าง |
| ประเภทรถ | `.track-card` · `setVtype()` | default · `.is-on` · `.track-grid.is-bad` (ยังไม่เลือก) |
| เลือกเดือน | `#ss-fmon` · `searchSelectHTML()` · `initSearchSelect()` | 12 เดือนล่าสุด · เดือนนี้ sub "ถึงวันที่ n" |
| สรุปขวา | `.wz-sum` · `sumCard()` | กล่องผิดปกติ `.is-off` (0) / `.is-bad` (>0) |
| ตารางทั้งเดือน | `.grid31` · `monthGrid()` | ✓ `.g-ok` · ✗ `.g-ng` · ว่าง |
| ปุ่มบันทึก | `#btnSaveSubmit` · `busyLabel()` | default · disabled + "กำลังบันทึก…" (`S.busy`) |
| คน | `personInline()` · `empChip()` | วงกลม icon `user` mono (ไม่มี initials) |
| เมนูแถว | `.row-menu` · `openRowMenu()` | portal ใน `#overlay-root` · ปิดเมื่อคลิกนอก/scroll |

## §6 Overlay Registry
| Overlay | ขนาด | เปิด | ปิด | ห้ามปิด |
|---|---|---|---|---|
| drawer view | 920 | `openView()` | ปุ่ม X · Esc · mousedown ที่ `#drawerBackdrop` | — |
| drawer wizard `.wide` | 1290 | `startWizard()` | ปุ่ม X/ยกเลิก · Esc · backdrop → ถ้ากรอกค้าง (`S.dw.dirty`) เปิด modal ทิ้งข้อมูล | dirty |
| modal (`#modalBackdrop`) | 520 / `.is-lg` 680 (ส่ง) | `openModalCfg()` | ปุ่ม · mousedown ที่ backdrop (`modalBackdropClick()`) | มีข้อความเหตุผล/ความเห็นค้าง |
| `.row-menu` | 200 | ⋮ | คลิกนอก · scroll | — |
| `.toast` (`#toast`) | — | `showToast()` | อัตโนมัติ | — |
| `.user-menu` | — | `toggleUserMenu()` | คลิกนอก | — |

## §7 Interaction Spec
- Esc chain (kit): ปิด search-select → modal → drawer ตามลำดับ handler
- backdrop ปิดด้วย `onmousedown` เมื่อ target = backdrop เท่านั้น (U25) — ลากจากในออกนอกไม่ปิด
- `render()` เก็บ/คืน scroll + focus (`preserveRenderState()`/`restoreRenderState()`)
- วันอนาคตกดไม่ได้ (`lastDay()`) · เปลี่ยนประเภทรถ/เดือน = ล้างผลส่วนที่ไม่ใช้ + toast
- PDF: `genPdf()` เปิดหน้าต่างพิมพ์จาก iframe ซ่อน `.pdf-gen` (ชื่อ = เลขที่)

## §8 State-Driven UI Matrix
| สถานะ | pill | ปุ่มหัว drawer (ตามผู้ใช้) |
|---|---|---|
| draft ร่าง | `pill-muted` | เจ้าของ: ยกเลิก · บันทึกผล / แก้ไข · ส่งตรวจสอบ |
| pending รอตรวจสอบ | `pill-warning` | ผู้พิจารณาขั้นปัจจุบัน: ส่งกลับแก้ไข · ตรวจสอบแล้ว (คำจาก `wordsOf()`) · เจ้าของ/admin: ยกเลิกเอกสาร |
| returned ส่งกลับแก้ไข | `pill-danger` | เหมือนร่าง + แถบแดงเหตุผล |
| approved ตรวจสอบแล้ว | `pill-success` | — (ล็อก) |
| cancelled ยกเลิก | `pill-muted` | — |
ประเภทรถ: fuel `pill-info` "ฟอร์คลิฟท์น้ำมัน" · electric `pill-warning` "ฟอร์คลิฟท์ไฟฟ้า"

## §9 Microcopy (verbatim)
### Toast
| variant | ข้อความ |
|---|---|
| info | `ไม่มีการแจ้งเตือนใหม่` |
| warning | `แบบเอกสารนี้ยังไม่เปิดใช้งาน` |
| warning | `แก้ไขได้เฉพาะร่างของตัวเอง` |
| warning | `ล้างผลรายการเฉพาะของประเภทเดิมแล้ว — กรอกรายการเฉพาะของประเภทใหม่` |
| warning | `เปลี่ยนเดือนแล้ว — ผลตรวจเดิมถูกล้าง` |
| warning | `กรุณากรอกข้อมูลให้ครบถ้วน` |
| warning | `กรุณากรอกข้อมูลให้ครบถ้วน` |
| warning | `กรุณากรอกข้อมูลให้ครบถ้วน` |
| info | `ส่งตรวจสอบแล้ว ·` |
| info | `ส่งออก` |
| info | `สลับเป็น` |
| error | `แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง` |
toast แบบประกอบ: "บันทึกร่างแล้ว · {เลขที่}" · "บันทึกร่างแล้ว · แจ้งหัวหน้างานเรื่องรายการผิดปกติแล้ว · {เลขที่}" · "ส่งตรวจสอบแล้ว · {เลขที่}" · "ตรวจสอบแล้ว · {เลขที่}" · "ส่งกลับแก้ไขแล้ว · {เลขที่}" · "ยกเลิกเอกสารแล้ว · {เลขที่}" · "ส่งออก {n} รายการ" · "สลับเป็น {ชื่อ}"
### Placeholder
`${rej ? 'แจ้งผู้ตรวจสอบว่าต้องแก้อะไร' : 'เหตุผลที่ยกเลิก'}` · `' + ph + '` · `ค้นหาเลขที่ / ผู้ตรวจสอบ / เดือน` · `ไม่บังคับ`
### ข้อความในจอ (สกัดจาก HTML)
- (ขั้น
- 99 อาคารตัวอย่าง ชั้น 9 ถนนตัวอย่าง แขวงตัวอย่าง เขตตัวอย่าง กรุงเทพฯ 10000
- [Lucide] All CDNs failed. Icons จะไม่แสดง but UI ยังใช้งานได้
- ]); if (canCancel(r)) items.push(['x-circle', 'ยกเลิกเอกสาร',
- ], ['printer', 'พิมพ์',
- ]]; if (isOwner(r) && isEditable(r)) items.splice(1, 0, ['pencil', 'แก้ไข / บันทึกผลต่อ',
- disabled title="ยังไม่ถึงวันนี้"
- showToast('ไม่มีการแจ้งเตือนใหม่','info')
- · กรอกไม่ครบ
- · ตรวจสอบแล้ว ล็อกแก้ไข
- · ผิดปกติ
- · เปิดอยู่
- · แก้แล้วส่งตรวจสอบใหม่ได้ (เลขที่เดิม)
- ก.ค.
- ก.พ.
- ก.ย.
- กมล ดูแลดี
- กรกฎาคม
- กรอกผลไม่ครบทุกรายการ — กด "ปกติทั้งหมด" หรือเลือกผลให้ครบ
- กรอกไม่ครบ
- กระจกมองหลัง
- กรุณากรอกข้อมูลให้ครบถ้วน
- กันยายน
- กำลังเปิดหน้าต่างพิมพ์ ·
- กุมภาพันธ์
- ขั้นทดสอบ
- ขั้วแบตเตอรี่
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลหลักแบบตรวจ
- ข้อมูลเอกสาร
- ข้าม
- ครบ · ปกติ
- คลังสินค้า
- คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
- ควันไอเสียผิดปกติ
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค่าเริ่มต้นจากสายอนุมัติ
- ค่าเริ่มต้นจากสายอนุมัติและผังองค์กร
- ค้นหา...
- ค้นหาเลขที่ / ผู้ตรวจสอบ / เดือน
- งาและชุดยก
- จำนวนวันของเดือน
- ชนิดไฟล์ไม่รองรับ
- ชื่อ-สกุล
- ช่อง
- ดาวน์โหลด PDF
- ต.ค.
- ตรวจสอบการรั่วซึม
- ตรวจสอบและยืนยัน
- ตรวจสอบแล้ว
- ตรวจแล้ว
- ตรวจแล้ว (วัน)
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตำแหน่ง
- ตุลาคม
- ต้อง
- ถึง
- ทำซ้ำ
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ทุกประเภทรถ
- ทุกรายการที่ตรวจปกติ / พร้อมใช้งาน
- ทุกสถานะ
- ธ.ค.
- ธันวาคม
- ธีรพงษ์ แรงดี
- บริษัท ตัวอย่าง จำกัด (มหาชน)
- บันทึกผลตรวจ
- บันทึกผลตรวจอย่างน้อย 1 วัน
- บันทึกผลไม่ครบทุกวันทำงาน
- บันทึกผิดประเภทรถ
- บันทึกผิดประเภทรถ — ทำใบใหม่แล้ว
- บันทึกผิดเดือน
- บันทึกร่างแล้ว ·
- บันทึกร่างแล้ว · แจ้งหัวหน้างานเรื่องรายการผิดปกติแล้ว ·
- บันทึกแบบร่าง
- บันทึกแบบร่างได้ทุกวัน · ส่งตรวจสอบแล้วแก้ไขไม่ได้จนกว่าหัวหน้างานส่งกลับ
- ประจำเดือน
- ประวัติ
- ประวัติ (append-only)
- ประเภทรถ
- ประเสริฐ ยกเก่ง
- ปิด
- ผิดปกติ
- ผิดปกติ (ช่อง)
- ผู้จัดการคลังสินค้า
- ผู้ตรวจสอบ
- ผู้ตรวจสอบ (ผู้บันทึก)
- ผู้ส่ง
- พ.ค.
- พ.ย.
- พนักงานขับรถฟอร์คลิฟท์
- พนักงานคลังสินค้า
- พฤศจิกายน
- พฤษภาคม
- พวงมาลัย
- พิมพ์
- ฟอร์คลิฟท์น้ำมัน
- ฟอร์คลิฟท์ไฟฟ้า
- ม.ค.
- มกราคม
- มิ.ย.
- มิถุนายน
- มี.ค.
- มีนาคม
- มีผิดปกติ
- ยกเลิก
- ยกเลิกเอกสาร
- ยกเลิกเอกสารแล้ว ·
- ยังไม่ตรวจ
- ยังไม่ถึงขั้นนี้
- ยังไม่มีข้อมูล
- ยังไม่มีแบบตรวจเช็ครถฟอร์คลิฟท์
- ยังไม่ส่ง
- ยังไม่เลือก
- ยางรถและล้อ
- ย้อนกลับ
- รถหยุดใช้งานทั้งเดือน
- รอตรวจสอบ
- รอผล
- รอพิจารณา
- ระดับน้ำมันเครื่อง
- ระดับน้ำมันเชื้อเพลิง
- ระดับน้ำมันเบรก
- ระดับน้ำมันไฮดรอลิก
- ระดับน้ำหล่อเย็น
- ระดับแบตเตอรี่
- ระบบ
- ระบบชาร์จไฟ
- ระบบตัดไฟฉุกเฉิน
- ระบบท่อเชื้อเพลิง
- ระบบเบรก
- ระบบไฮดรอลิก
- รายการ
- รายการตรวจสอบทั่วไป
- รายการตรวจสอบเฉพาะรถฟอร์คลิฟท์น้ำมัน
- รายการตรวจสอบเฉพาะรถฟอร์คลิฟท์ไฟฟ้า
- รายการผิดปกติยังไม่ได้แจ้งซ่อม
- รายละเอียด
- ร่าง
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ลายเซ็น / อนุมัติ
- ลำดับการอนุมัติ
- ล้างตัวกรอง
- ล้างผลรายการเฉพาะของประเภทเดิมแล้ว — กรอกรายการเฉพาะของประเภทใหม่
- วัน
- วันที่
- วันที่ ........./........./.........
- วันที่สร้าง
- วิทยา คุมงานดี
- ศิริพร จัดการดี
- ส.ค.
- สถานะ
- สถานะเอกสาร
- สภาพตัวรถโดยรวม
- สร้าง PDF
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างแบบตรวจ
- สร้างแบบตรวจของเดือนนี้ แล้วบันทึกผลทุกวันก่อนใช้งานรถ
- สร้างแบบตรวจเช็ครถฟอร์คลิฟท์
- สร้างโดย
- สลับเป็น
- สัญญาณถอยหลัง
- สายชาร์จไฟ
- สิงหาคม
- สุดา ตรวจไว
- ส่งกลับแก้ไข
- ส่งกลับแก้ไขแล้ว ·
- ส่งกลับให้ผู้ตรวจสอบแก้ไข
- ส่งตรวจสอบ
- ส่งตรวจสอบ?
- ส่งตรวจสอบแล้ว ·
- ส่งออก
- ส่งในระบบ
- หัวหน้างานคลังสินค้า
- หัวหน้างานคลังสินค้า (กะดึก)
- หัวหน้างานตรวจสอบ
- หัวหน้างานตรวจสอบแล้ว — ปิดใบประจำเดือน
- อนุชา ขยันดี
- อนุมัติ
- เข็มขัดนิรภัย
- เดือนนี้ · ถึงวันที่
- เดือนนี้ยังไม่เริ่ม — เลือกเดือนปัจจุบันหรือเดือนก่อนหน้า
- เด้งกลับบน
- เบรกมือ
- เปลี่ยนเดือนแล้ว — ผลตรวจเดิมถูกล้าง
- เพิ่มเติม
- เม.ย.
- เมษายน
- เลขที่
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกประเทศ
- เลือกประเภทรถ
- เลือกประเภทรถก่อน แล้วรายการตรวจจะขึ้นตามประเภท
- เลือกประเภทรถและเดือน แล้วบันทึกผลตรวจของแต่ละวัน — บันทึกร่างได้ทุกวัน ส่งตรวจสอบเมื่อสิ้นเดือน
- เลือกประเภทรถไม่ถูกต้อง
- เลือกผู้พิจารณา
- เลือกเดือน
- เลือกเดือนปัจจุบันหรือเดือนก่อนหน้า
- เสียงเครื่องยนต์ผิดปกติ
- เหตุผลที่ยกเลิก
- เอกสารแนบ
- แก้ไขล่าสุด
- แก้ไขเอกสาร
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งผู้ตรวจสอบว่าต้องแก้อะไร
- แจ้งพบรายการผิดปกติ
- แตร
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบฟอร์มตรวจเช็ครถฟอร์คลิฟท์ประจำวัน
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- แผนก
- โซ่ยกและสลักล็อก
- ใบแจ้งซ่อมรถฟอร์คลิฟท์ 8 ก.ย..pdf
- ไฟหน้า / ไฟท้าย
- ไฟหมุน / ไฟเตือน
- ไฟแสดงสถานะแบตเตอรี่
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่มี
- ไม่มีรายการผิดปกติ
- ไม่ยกเลิก
- ไม่อนุมัติ
- — คุณเป็นผู้ตรวจสอบใบนี้

## §10 Data Binding & BACKEND anchors
| จุดใน prototype | ระบบจริง |
|---|---|
| `RECS` / `mkRec()` | API-01/02 |
| `CHECKLIST_CONFIG` | API-12 ForkliftChecklistConfig (snapshot ลงใบ) |
| `persist()` | API-03/04 (ENG-DOC-NUM ตอนบันทึกครั้งแรก · fli_defect_found) |
| `MOCK_DOA_RESOLVED` · `resolveDoa()` (DOA-ENGINE-HOOK) | API-05/06 `GET /doa/resolve?feature_id=F-TMP-002` |
| `confirmApprove()` · `confirmReason()` | API-07/08 |
| `docPrintData()` + `FLI_TPL` + `tplRender()` | API-09 render ฝั่ง server (data contract เดียวกัน) |
| `exportCSV()` | API-10 |
| `DOC.active` | F-DOCCFG status |

## §11 Traceability + Drift Log
| Brief | FRD | HTML |
|---|---|---|
| §4 P-01 | 01 P-01 · API-01/10 · FN-11 | `renderPage()` |
| §4 P-02 | 01 P-02 · API-03/04/12 · FN-01..04 · BR-03..06 | `renderWizard()` |
| §4 P-03 | 01 P-03 · API-02/05..09 · FN-05..09 | `renderViewDrawer()` |
| §6 modal ส่ง/ตัดสิน/ยกเลิก | 05 §5.2 · BR-DOA-01..04 | `renderModal()` |
**Drift Log**
| # | ชนิด | รายการ | ข้อเสนอ |
|---|---|---|---|
| D-01 | HTML-only | ปุ่ม "ทำซ้ำ" (archetype) ขณะที่ DEC-13 = ทำซ้ำ ✗ | ซ่อนในระบบจริง หรือให้ลูกค้ายืนยัน (OQ-06) |
| D-02 | HTML-only (prototype) | `window.__QA__` · สลับผู้ใช้ · `S.sim` | ไม่ทำในระบบจริง |

## §12 Diff จากเวอร์ชันก่อน
— ไม่มีใน HTML นี้ (เวอร์ชันแรก)

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- เพิ่มช่องหมายเลข/ทะเบียนรถเมื่อมีทะเบียนรถ (OQ-03) · ปุ่ม "เปิดแจ้งซ่อม" จากรายการผิดปกติ (Phase 2)
