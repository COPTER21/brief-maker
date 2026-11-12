# UI BRIEF — F-TMP-005 แบบฟอร์มรายงานผลการสอบทานคำขอซื้อและใบสั่งซื้อค้างนาน (PR/PO Outstanding)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| HTML | `feature.html` (html-generator-v9.4 · archetype `Q-form` · `window.__QA__` มี) · audit FAIL 0 · jsdom smoke 47/47 · [NO-BROWSER] e2e/screenshot ยังไม่รัน |
| FRD | FRD_F-TMP-005_Pack (00–07 · frd_lint BLOCK 0 · WARN 0) |
| DECISIONS | DECISIONS.lock REQ-TMP-005 — 16 มติ (AI-DEFAULT 11 · VALID 5) |
| Prototype-only | `window.__QA__` · ตัวสลับผู้ใช้ (`switchPersona()`) · `S.sim` (`commitRejected()`) · seed `RECS` · `ORG_UNITS` / `UOMS` mock — ไม่ทำในระบบจริง (Drift Log) |
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
| `#/pr-po-outstanding` | P-01 รายการ (default) | `applyRoute()` · `renderPage()` |
| `#/pr-po-outstanding/create` | P-02 สร้าง | `startWizard()` |
| `#/pr-po-outstanding/edit/:id` | P-02 แก้ไข | `startWizard()` (เฉพาะเจ้าของ · draft/returned) |
| `#/pr-po-outstanding/view/:id` | P-03 ดู | `openView()` · `showDrawer()` (ไม่มีสิทธิ์ = ไม่เปิด) |
refresh-safe: `hashchange` → `applyRoute()` · ปิด drawer → `go(RT)` (RT = `pr-po-outstanding`) · ไม่มี route ทำซ้ำ (DEC-11)

## §3 Layout Shell
sidebar `#sidebar` (โมดูล "จัดซื้อ" → "สอบทาน PR/PO ค้างนาน" + `#sbBadge` = จำนวนรายงานรอฉันอนุมัติ) · shell-bar (breadcrumb Core › จัดซื้อ › สอบทาน PR/PO ค้างนาน · กระดิ่ง · user chip `#ucAv` = icon คน + เมนูสลับผู้ใช้ `#userMenu`) · เนื้อหา `#page-content`

## §4 Page Anatomy
### P-01 รายการ — `renderPage()`
`.ph` (ชื่อ `DOC_SHORT` + `.ph-count` + `.ph-sub` · ปุ่ม `exportCSV()` · `#btnCreate`) → แถบแดงเมื่อ `DOC.active` = false → `.seg` (`segTabs()` · `.seg-btn` ทั้งหมด/รอฉันอนุมัติ) → `.card` `.filter-bar` (ค้นหา `#fq` · `#ss-fst` สถานะ · search-select `fmo` เดือน · ล้างตัวกรอง `resetFilters()`) → `.table` (คอลัมน์ เลขที่ · วันที่รายงาน · ผู้จัดทำ `personInline()` · หน่วยงาน · รายการ · ยังไม่ออก PO · สถานะ · ลายเซ็น `renderSignProgress()` · ⋮ `openRowMenu()`) → `pager()` 25/หน้า · แถวว่าง = `emptyStateHTML()`
### P-02 สร้าง/แก้ไข — `renderWizard()` (drawer `.wide`)
หัว + `stepper()` 3 ขั้น → ขั้น 1 `wizMain()`: `.wz-split` = ซ้าย การ์ด ① `.wz-row2` (`bedateHTML()` key `rdate` วันที่รายงาน `bdPick_rdate` → `setHead()` · `#ss-forg` หน่วยงาน) · การ์ด ② ตาราง `.ln-wrap` > `.ln-table` (`lineRow()` ต่อแถว: `#pr{i}` เลขที่ PR · `#po{i}` เลขที่ PO · key `od{i}` วันที่สั่งซื้อ · key `rd{i}` วันที่รับ · `#vendor{i}` ผู้ผลิต · `#desc{i}` รายละเอียด · `#qty{i}` จำนวน · `#ss-iu{i}` หน่วย · `#ss-idp{i}` ฝ่าย/แผนก · `#reason{i}` · `#cur{i}` · `#fix{i}` · ปุ่มลบ `removeItem()`) · `.ln-err` / `.ln-warn` ใต้ช่อง · `.ln-foot` ปุ่ม `#btnAddItem` `addItem()` · ขวา `sumCard()` `.wz-sum` → ขั้น 2 `wizAttach()` (upload `#ppoFile` `pickFiles()`) → ขั้น 3 `wizReview()` (`itemsTable()` · แถบเตือนเกิน 24 แถว) · footer: ย้อนกลับ · ยกเลิก · `#btnDraft1`/`#btnDraft` `saveDraft()` · `#btnNext` `wizNext()` · `#btnSaveSubmit` `saveAndSubmit()`
### P-03 ดู — `renderViewDrawer()` (drawer 920)
หัว lean (eyebrow `DOC_SHORT (DOC_EN)` · เลขที่ + pill สถานะ · sub วันที่รายงาน · n รายการ) + ปุ่มตามสถานะ + พิมพ์/ดาวน์โหลด (ไม่มีทำซ้ำ) → `.drawer-tabs` (`tabBtn()`) → `renderDetailTab()` (`viewBanner()` · แถบเลขซ้ำ · ข้อมูลเอกสาร · ผู้จัดทำรายงาน · `itemsTable()` · ไฟล์แนบ · ข้อมูลระบบ) / `renderPdfTab()` (`.pdf-slot` iframe `fitPdf()`) / `renderSignTab()` / `renderHistoryTab()`

## §5 Component Inventory
| Component | anchor | states |
|---|---|---|
| segmented tabs | `.seg-btn` · `setStat()` | default · `.on` (dot primary + count) · hover |
| ตารางกรอกรายการ | `.ln-table` · `lineRow()` · `lnTxt()` | แถวปกติ · `tr.is-bad` (มี error) · `.ln-err` ข้อความแดงใต้ช่อง · `.ln-warn` ส้ม (เลข PR/PO ซ้ำ) · ปุ่มลบ disabled เมื่อเหลือ 1 แถว · เลื่อนแนวนอน (min-width 1760) |
| เลขที่ PO | `#po{i}` | ว่าง placeholder "ยังไม่ออก PO" · มีค่า → placeholder วันที่สั่งซื้อ "เลือกวันที่ *" + ผู้ผลิต "… *" (render ตอน change) |
| หน่วย | `#ss-iu{i}` · `searchSelectHTML()` · `initSearchSelect()` | UOM Master (`UOMS`) |
| ฝ่าย/แผนก · หน่วยงาน | `#ss-idp{i}` · `#ss-forg` | ผังองค์กร (`ORG_UNITS`) · หน่วยงาน sub "หน่วยงานของคุณ" |
| วันที่ พ.ศ. | `.bedate` · `bedateHTML()` · `.bd-pop` | ว่าง (placeholder) · มีค่า · วัน disabled ตาม min/max · ปุ่ม "วันนี้" |
| สรุปขวา | `.wz-sum` · `sumCard()` | กล่อง "ยังไม่ออก PO" `.is-off` (0) / `.is-bad` (>0) |
| ตารางรายการ (อ่าน) | `itemsTable()` | pill `pill-muted` "ยังไม่ออก PO" · `pill-warning` "ซ้ำ" · ว่าง = แผงไม่มีรายการ |
| ปุ่มบันทึก | `#btnSaveSubmit` · `busyLabel()` | default · disabled + "กำลังบันทึก…" (`S.busy`) |
| คน | `personInline()` · `empChip()` | วงกลม icon `user` mono (ไม่มี initials) |
| เมนูแถว | `.row-menu` · `openRowMenu()` | portal ใน `#overlay-root` · พิมพ์ · แก้ไข (ร่างของตน) · ยกเลิกเอกสาร · ปิดเมื่อคลิกนอก/scroll |

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
- `render()` เก็บ/คืน scroll + focus (`preserveRenderState()`/`restoreRenderState()`) · ช่องข้อความ (`setTxt()`) ไม่ render ระหว่างพิมพ์ · เลขที่ PO/จำนวน render ตอน change
- `addItem()` ยกฝ่าย/แผนกจากแถวก่อน + focus ช่องเลขที่ PR แถวใหม่ · แถวว่างทั้งแถวตัดทิ้งตอน `validateMain()`
- วันที่รายงาน/วันที่สั่งซื้อ: ปฏิทิน max = วันนี้ · วันที่รับ min = วันที่สั่งซื้อ (อนาคตได้)
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
toast แบบประกอบ: "บันทึกร่างแล้ว · {เลขที่}" · "ส่งอนุมัติแล้ว · {เลขที่}" · "อนุมัติ · {เลขที่}" · "ไม่อนุมัติ — ส่งกลับให้แก้ไขแล้ว · {เลขที่}" · "ยกเลิกเอกสารแล้ว · {เลขที่}" · "ส่งออก {n} รายงาน · {m} รายการ" · "สลับเป็น {ชื่อ}"
### Placeholder
`${ph || ''}` · `${rej ? 'แจ้งผู้จัดทำว่าต้องแก้อะไร' : 'เหตุผลที่ยกเลิก'}` · `' + ph + '` · `ค้นหาเลขที่ / ผู้จัดทำ / เลข PR-PO / ผู้ขาย` · `ไม่บังคับ`
### ข้อความในจอ (สกัดจาก HTML)
- (ขั้น
- [Lucide] All CDNs failed. Icons จะไม่แสดง but UI ยังใช้งานได้
- ]); if (canCancel(r)) items.push(['x-circle', 'ยกเลิกเอกสาร',
- ]]; if (isOwner(r) && isEditable(r)) items.splice(1, 0, ['pencil', 'แก้ไข',
- showToast('ไม่มีการแจ้งเตือนใหม่','info')
- · ยังไม่ออก PO
- · รายการเกิน
- · อนุมัติแล้ว ล็อกแก้ไข
- · เปิดอยู่
- ก.ค.
- ก.พ.
- ก.ย.
- กมลา ดูแลดี
- กรกฎาคม
- กรุณากรอกข้อมูลให้ครบถ้วน
- กล่อง
- กันยายน
- กำลังเปิดหน้าต่างพิมพ์ ·
- กิโลกรัม
- กุมภาพันธ์
- ขอใบเสนอราคาเพิ่ม 2 ราย
- ขั้นทดสอบ
- ข้อมูล PR/PO ไม่ครบ
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลหลักรายงาน
- ข้อมูลเอกสาร
- ข้อมูลไม่ครบหรือไม่ถูกต้อง
- ข้าม
- คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
- คำขอซื้อและใบสั่งซื้อค้างนาน (PR/PO Outstanding)
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค่าเริ่มต้นจากสายอนุมัติ
- ค่าเริ่มต้นจากสายอนุมัติและผังองค์กร
- ค้นหา...
- ค้นหาเลขที่ / ผู้จัดทำ / เลข PR-PO / ผู้ขาย
- ค้างนาน
- งาน
- จำนวนสั่งซื้อ
- ชนิดไฟล์ไม่รองรับ
- ชิ้น
- ชื่อ-สกุล
- ชื่อผู้ผลิต/ผู้จัดจำหน่าย *
- ชื่อฟังก์ชัน
- ชุด
- ซ้ำ
- ดาวน์โหลด PDF
- ต.ค.
- ตรวจสอบและยืนยัน
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตำแหน่ง
- ติดตามผู้ขายแล้ว นัดส่งใหม่
- ตุลาคม
- ต้อง
- ถึง
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ทุกสถานะ
- ทุกเดือน
- ธ.ค.
- ธนา บริหารดี
- ธันวาคม
- บรรจุภัณฑ์ตัวอย่าง ขนาดกลาง
- บริการซ่อมบำรุงตัวอย่าง
- บริษัท ซัพพลายตัวอย่าง ซี จำกัด
- บริษัท ตัวอย่าง จำกัด (มหาชน)
- บริษัท ผู้ขายตัวอย่าง เอ จำกัด
- บันทึก PR/PO ค้างอย่างน้อย 1 รายการ
- บันทึกผิดหน่วยงาน
- บันทึกร่างแล้ว ·
- บันทึกแบบร่าง
- บันทึกแบบร่างได้ · ส่งอนุมัติแล้วแก้ไขไม่ได้จนกว่าผู้มีอำนาจอนุมัติส่งกลับ
- ประวัติ
- ประวัติ (append-only)
- ประเสริฐ มั่นคง
- ปิด
- ผู้ขายส่งของล่าช้า
- ผู้ขายแจ้งเลื่อนส่ง
- ผู้จัดการฝ่ายจัดซื้อ
- ผู้จัดการแผนกจัดซื้อต่างประเทศ
- ผู้จัดการแผนกจัดซื้อในประเทศ
- ผู้จัดทำ
- ผู้จัดทำ :
- ผู้จัดทำรายงาน
- ผู้ผลิต/ผู้จัดจำหน่าย
- ผู้มีอำนาจอนุมัติ
- ผู้ส่ง
- ฝ่าย/แผนก ขอซื้อสินค้า/บริการ
- ฝ่าย/แผนกขอซื้อ
- ฝ่ายขาย
- ฝ่ายจัดซื้อ
- ฝ่ายบริหารทั่วไป
- ฝ่ายบัญชีและการเงิน
- ฝ่ายผลิต
- พ.ค.
- พ.ย.
- พฤ
- พฤศจิกายน
- พฤษภาคม
- พิมพ์
- ม.ค.
- มกราคม
- มาลี ใจดี
- มิ.ย.
- มิถุนายน
- มี.ค.
- มีนาคม
- มีเลขที่ PO ต้องระบุผู้ผลิต/ผู้จัดจำหน่าย
- มีเลขที่ PO ต้องระบุวันที่สั่งซื้อ
- มีเลขที่ PR/PO ซ้ำในรายงานนี้ — ตรวจว่าเป็นคนละรายการ
- ม้วน
- ยกเลิก
- ยกเลิกเอกสาร
- ยกเลิกเอกสารแล้ว ·
- ยังเป็นร่าง — ตรวจรายการ PR/PO ค้างให้ครบ แล้วส่งอนุมัติ
- ยังไม่ถึงขั้นนี้
- ยังไม่มีข้อมูล
- ยังไม่มีรายงานสอบทาน PR/PO ค้างนาน
- ยังไม่ส่ง
- ยังไม่ออก PO
- ยังไม่ได้บันทึก PR/PO ค้างในรายงานนี้
- ย้อนกลับ
- รอผล
- รอผู้ขอยืนยัน
- รอผู้ขอยืนยันสเปก
- รอพิจารณา
- รออนุมัติ
- รอใบเสนอราคาเปรียบเทียบ
- ระบุรายละเอียด
- ระบุวันที่รายงานและหน่วยงาน แล้วบันทึก PR/PO ที่ค้างนาน พร้อมสาเหตุคงค้าง สถานะปัจจุบัน และแนวทางการแก้ไข
- ระบุสถานะปัจจุบัน
- ระบุสาเหตุคงค้าง
- ระบุเลขที่ PR หรือ PO อย่างน้อย 1
- ระบุแนวทางการแก้ไข
- รายการ
- รายการ · ยังไม่ออก PO
- รายงาน ·
- รายงานสอบทาน PR/PO ค้างนาน
- รายละเอียด
- รายละเอียดสินค้า/บริการ
- ร่าง
- ลบรายการ
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ลายเซ็น / อนุมัติ
- ลำดับ
- ลำดับการอนุมัติ
- ลิตร
- ล้างตัวกรอง
- วรรณา ขยันยิ่ง
- วันที่ ........./........./.........
- วันที่รับต้องไม่ก่อนวันที่สั่งซื้อ
- วันที่รับสินค้า/บริการ
- วันที่รายงาน
- วันที่รายงานเป็นวันในอนาคตไม่ได้
- วันที่สั่งซื้อ
- วันที่สั่งซื้อต้องไม่หลังวันที่รายงาน
- วันที่สั่งซื้อเป็นวันในอนาคตไม่ได้
- วัสดุสิ้นเปลืองสำนักงาน ชุด A
- ศิริพร จัดการดี
- ส.ค.
- สถานะ
- สถานะปัจจุบัน
- สถานะเอกสาร
- สมศักดิ์ รอบคอบ
- สรุปรายการ PR-PO ค้างจากระบบเดิม ส.ค..xlsx
- สร้าง PDF
- สร้างรายงาน
- สร้างรายงาน แล้วบันทึก PR/PO ที่ค้าง พร้อมสาเหตุและแนวทางการแก้ไข
- สร้างรายงานสอบทาน PR/PO ค้างนาน
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างโดย
- สลับเป็น
- สังกัด
- สารเคมีตัวอย่าง เกรด B
- สาเหตุคงค้าง
- สาเหตุคงค้างไม่ตรงข้อเท็จจริง
- สำนักบริหาร
- สิงหาคม
- สินค้าขาดตลาด
- ส่งอนุมัติ
- ส่งอนุมัติ?
- ส่งอนุมัติแล้ว ·
- ส่งออก
- ส่งในระบบ
- หน่วย
- หน่วยงาน
- หน่วยงานของคุณ
- หัวหน้าหน่วยธุรกิจ
- หาผู้ขายทดแทน
- ห้างหุ้นส่วน ตัวอย่าง บี
- อนุมัติ
- อนุมัติแล้ว
- อนุมัติแล้ว — ปิดรายงานสอบทาน (ไม่ปิด/ยกเลิก PR-PO)
- อยู่ระหว่างเปรียบเทียบราคา
- ออกรายงานซ้ำ
- ออกรายงานซ้ำ — ใช้ใบ PPO-2569-0003
- อะไหล่เครื่องจักรตัวอย่าง รุ่น X
- อา
- อุปกรณ์ความปลอดภัยตัวอย่าง
- เจ้าหน้าที่จัดซื้อ
- เดือน
- เดือนถัดไป
- เด้งกลับบน
- เพิ่มเติม
- เม.ย.
- เมตร
- เมษายน
- เร่งรัดผู้ขาย กำหนดส่งใหม่
- เลขที่
- เลขที่ PO
- เลขที่ PO ซ้ำในรายงานนี้
- เลขที่ PR
- เลขที่ PR ซ้ำในรายงานนี้
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกประเทศ
- เลือกผู้พิจารณา
- เลือกฝ่าย/แผนก
- เลือกวันที่
- เลือกวันที่ *
- เลือกวันที่รายงาน
- เลือกหน่วย
- เลือกหน่วยงาน
- เหตุผลที่ยกเลิก
- เอกสารแนบ
- แก้ไข
- แก้ไขข้อมูล
- แก้ไขล่าสุด
- แก้ไขเอกสาร
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งผู้ขอให้ยืนยันภายในสัปดาห์
- แจ้งผู้จัดทำว่าต้องแก้อะไร
- แถว
- แถว แสดงในแบบพิมพ์
- แถวแรก — ส่งออก CSV แนบประกอบ
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แนวทางการแก้ไข
- แนวทางการแก้ไขไม่ชัดเจน
- แนวทางการแก้ไขไม่ชัดเจน — แถว 2 ระบุวันที่ผู้ขายจะส่งด้วย
- แบบฟอร์มรายงานผลการสอบทาน
- แบบฟอร์มรายงานผลการสอบทานคำขอซื้อและใบสั่งซื้อค้างนาน (PR/PO Outstanding)
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- แผนกคลังสินค้า
- แผนกจัดซื้อต่างประเทศ
- แผนกจัดซื้อในประเทศ
- แผนกซ่อมบำรุง
- แพ็ก
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่มี
- ไม่มีรายการ
- ไม่มีรายการค้างในรอบนี้
- ไม่ยกเลิก
- ไม่อนุมัติ
- ไม่อนุมัติ · แก้ไข
- ไม่อนุมัติ — กลับให้ผู้จัดทำแก้ไข
- ไม่อนุมัติ — ส่งกลับให้แก้ไขแล้ว ·

## §10 Data Binding & BACKEND anchors
| จุดใน prototype | ระบบจริง |
|---|---|
| `RECS` / `mkRec()` | API-01/02 |
| `ORG_UNITS` | API-12 ผังองค์กร (F-ORG-001 · snapshot ลงรายงาน/แถว) |
| `UOMS` | API-13 UOM Master (F-PRODUCT-MASTER-001 · snapshot ลงแถว) |
| `itemErrors()` · `validateMain()` · `dupNos()` | FN-01 (422 + warnings) |
| `persist()` | API-03/04 (ENG-DOC-NUM ตอนบันทึกครั้งแรก) |
| `MOCK_DOA_RESOLVED` · `resolveDoa()` (DOA-ENGINE-HOOK) | API-05/06 `GET /doa/resolve?feature_id=F-TMP-005` |
| `confirmApprove()` · `confirmReason()` | API-07/08 |
| `docPrintData()` + `PPO_TPL` + `tplRender()` + `PRINT_CFG` | API-09 render ฝั่ง server (data contract + print_config เดียวกัน) |
| `exportCSV()` | API-10 (ระดับรายการ) |
| `DOC.active` · `DOC.form` · `DOC.rev` | F-DOCCFG status + print_config |

## §11 Traceability + Drift Log
| Brief | FRD | HTML |
|---|---|---|
| §4 P-01 | 01 P-01 · API-01/10 · FN-11 | `renderPage()` |
| §4 P-02 | 01 P-02 · API-03/04/12/13 · FN-01..04 · BR-01..08 | `renderWizard()` |
| §4 P-03 | 01 P-03 · API-02/05..09 · FN-05..09 | `renderViewDrawer()` |
| §6 modal ส่ง/ตัดสิน/ยกเลิก | 05 §5.2 · BR-DOA-01..04 | `renderModal()` |
**Drift Log**
| # | ชนิด | รายการ | ข้อเสนอ |
|---|---|---|---|
| D-01 | HTML-only (prototype) | `window.__QA__` · สลับผู้ใช้ `switchPersona()` · `S.sim` (`commitRejected()`) · seed `RECS` · mock `ORG_UNITS`/`UOMS` | ไม่ทำในระบบจริง |
| D-02 | FRD-only | 02 API-12/13 อ่าน master จริง · warnings `PRINT_ROWS_EXCEEDED` ฝั่ง API | prototype ใช้ mock · เตือนเกิน 24 แถวในขั้นตรวจสอบ |

## §12 Diff จากเวอร์ชันก่อน
— ไม่มีใน HTML นี้ (เวอร์ชันแรก)

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- คอลัมน์อายุค้าง (วัน) + เกณฑ์จาก PurchaseConfig (OQ-03) · เลขที่ PR/PO/ผู้ขาย เป็น search-select เมื่อ F072/F078/Supplier ขึ้นระบบ + ดึงรายการค้างอัตโนมัติ (OQ-04) · แบบพิมพ์ใบต่อหน้า 3+ (OQ-08)
