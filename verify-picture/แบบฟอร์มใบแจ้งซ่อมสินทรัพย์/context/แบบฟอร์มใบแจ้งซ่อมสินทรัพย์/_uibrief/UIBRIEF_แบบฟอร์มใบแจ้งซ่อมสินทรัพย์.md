# UI BRIEF — F-TMP-001 แบบฟอร์มใบแจ้งซ่อมสินทรัพย์ (Asset Repair Request)

> html-ui-brief v1.1 · EXTRACTION-BASED — ทุกบรรทัด trace กลับหา selector/function/ข้อความจริงใน `feature.html`
> ชุด handoff: **feature.html (source of truth) + FRD_F-TMP-001_Pack + UI Brief นี้**

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| HTML | `feature.html` · html-generator-v9.4 · archetype **Q-form** (`<meta name="cube-archetype" content="Q-form">`) · `window.__QA__` มี |
| Gate | audit.sh FAIL 0 · e2e_standard 21/21 (Chromium cloud container — เครื่อง user NO-BROWSER) |
| FRD | FRD_F-TMP-001_Pack v1.0 (01_UI P-01..03 · M-01..05) — pair แล้ว |
| DECISIONS | DECISIONS.lock REQ-TMP-001 — 16 มติ (AI-DEFAULT 12 · VALID 4) |
| Prototype-only | `window.__QA__` · ตัวสลับผู้ใช้ (`switchPersona()` ใน `.user-menu`) · `S.sim` (จำลอง 409/403/500) · seed `RECS` → ระบบจริงลบ/แทนด้วย API (Drift Log) |
| Date | 2026-10-11 |

## §1 Design Tokens AS-BUILT
- CI: CUBE Warm Light (BASE-KIT v6.4 ของ html-generator-v9 — ห้ามแก้) · ฟอนต์ Noto Sans Thai + Satoshi · ไอคอน Lucide 0.469.0 (multi-CDN loader) mono currentColor
- สีหลัก: `--c-primary` (action) · `--c-success` (ปุ่มอนุมัติ `.btn-success`) · `--c-danger` (ยกเลิก/ไม่อนุมัติ) · `--c-warning` · พื้น `--c-bg-off`
- คน = วงกลม `#111111` + icon user (`.emp-av`) · page tabs ราง `#F1EEE9` (`.seg`)
### z-index map (สูง → ต่ำ)
| ค่า | ใช้กับ |
|---|---|
| var(--z-toast) 80 | `#toast` |
| var(--z-popover) 70 | `.row-menu` · `.bd-pop` (ปฏิทิน พ.ศ.) · search-select list (portal ใน `#overlay-root`) |
| var(--z-modal) 60 | `.modal-backdrop` |
| var(--z-drawer) 51 | `#drawer` |
| var(--z-backdrop) 50 | `#drawerBackdrop` |
| var(--z-dropdown) 30 | dropdown ใน kit |
| var(--z-sticky) 10 · var(--z-shell) 10 | หัวตาราง sticky · shell bar |
| 3 · 2 · 1 | ชั้นภายใน component ของ kit (stepper เส้น/วงกลม · content) |
### CSS variables (ทั้งชุดจาก `:root`)
| var | ค่า |
|---|---|
| `--c-navy` | #111111 |
| `--c-navy-2` | #111111 |
| `--c-primary` | #FF3B30 |
| `--c-primary-hover` | #E62E24 |
| `--c-teal` | #FF9A1F |
| `--c-teal-light` | #FFB763 |
| `--c-ink` | #111111 |
| `--c-mute` | #54565C |
| `--c-mute-2` | #73757B |
| `--c-mute-3` | #9A9CA2 |
| `--c-placeholder` | rgb(180,182,188) |
| `--z-content` | 1 |
| `--z-sticky` | 10 |
| `--z-shell` | 10 |
| `--z-dropdown` | 30 |
| `--z-backdrop` | 50 |
| `--z-drawer` | 51 |
| `--z-modal` | 60 |
| `--z-popover` | 70 |
| `--z-toast` | 80 |
| `--c-line` | #DEDAD4 |
| `--c-line-2` | #E9E5E0 |
| `--c-line-3` | #F1EEEA |
| `--c-bg-off` | #FAF8F5 |
| `--c-success` | #1F9D55 |
| `--c-warning` | #E8870F |
| `--c-danger` | #E62E24 |
| `--sidebar-w` | 232px |
| `--shell-h` | 52px |
| `--fs-h1` | 22px |
| `--fs-h2` | 17px |
| `--fs-h3` | 15px |
| `--fs-body` | 14px |
| `--fs-sub` | 13px |
| `--fs-meta` | 12px |
| `--fs-cap` | 11px |
| `--fs-kpi` | 28px |
| `--sp-xs` | 4px |
| `--sp-sm` | 8px |
| `--sp-md` | 12px |
| `--sp-lg` | 20px |
| `--sp-xl` | 28px |
| `--r-xs` | 4px |
| `--r-sm` | 6px |
| `--r-md` | 8px |
| `--r-lg` | 12px |
| `--r-full` | 999px |

## §2 Route Map
| Route | หน้า | handler |
|---|---|---|
| `#/asset-repair` | P-01 รายการ | `applyRoute()` · `renderPage()` |
| `#/asset-repair/create` | P-02 สร้าง | `startWizard()` |
| `#/asset-repair/edit/:id` | P-02 แก้ร่าง (เจ้าของ · draft) | `startWizard(id)` |
| `#/asset-repair/view/:id` | P-03 ดู | `openView(id)` → `showDrawer()` |
- refresh-safe: `hashchange` → `applyRoute()` · route ใบที่ไม่มีสิทธิ์ (`canSee()` false) = ไม่เปิด drawer · ปิด drawer → `go(BASE)`

## §3 Layout Shell
- `.sidebar` (โมดูล Asset › "แจ้งซ่อมสินทรัพย์" + `#sbBadge` = จำนวนรอฉันพิจารณา) · `.shell-bar` breadcrumb Core › Asset › แจ้งซ่อมสินทรัพย์ · `.user-chip` (`#ucName` · `#ucRole` · `#ucAv` = icon คน) · `#page-content` · `#drawer` · `#modal` · `#toast` · `#overlay-root`

## §4 Page Anatomy
### P-01 รายการ (`renderPage()`)
- `.ph` → `.ph-title` "แบบฟอร์มใบแจ้งซ่อมสินทรัพย์" + `.ph-en` "(Asset Repair Request)" + `.ph-count` · `.ph-sub` · `.ph-actions` [ส่งออก CSV `exportCSV()`] [สร้างใบแจ้งซ่อม `#btnCreate` → `startWizard()` · disabled เมื่อ `DOC.active` false + `.alert-row.is-danger`]
- `.seg` → `.seg-btn` ×2 (`segTab()` · `setListTab()`): ทั้งหมด · รอฉันพิจารณา + `.seg-n` (ซ่อนเมื่อ 0)
- `.card.list-card` → `.filter-bar` (`#fq` ค้นหา `onQ()` · `searchSelectHTML('fst')` สถานะ · `searchSelectHTML('fdept')` ฝ่าย/แผนก · ล้างตัวกรอง `resetFilters()`) → `.table` (`sortTh()` เลขที่/วันที่แจ้ง/ผู้แจ้งซ่อม/จำนวน) → `pager()` `.table-foot`
- แถว `tr.is-clickable` → `rowClick()` → `openView()` · คอลัมน์สุดท้าย `.row-actions-cell` `.ra-btn` ⋮ → `openRowMenu()`
### P-02 สร้าง/แก้ (`renderWizard()` · `#drawer.wide`)
- `.dw-head` (eyebrow · `.dw-title` "แจ้งซ่อมสินทรัพย์" / "แก้ไขใบแจ้งซ่อม {เลขที่}") + `stepper()` `.d-stepper` 3 ขั้น (`STEPS`)
- ขั้น 1 `wizMain()`: `.wz-split` → ซ้าย `.wz-card` ① "แจ้งซ่อมอะไร ที่ไหน" `.it-tbl` (แถว `itemRow()`: `it-d-i` รายการ · `it-a-i` ทะเบียนสินทรัพย์ · `it-q-i` จำนวน · `it-s-i` อาการชำรุด · `it-l-i` สถานที่ตั้ง · `it-r-i` หมายเหตุ · ลบ `removeItem()`) + `.add-row` `addItem()` + `.it-help` · ขวา `sumCard()` `.wz-sum` (`#sumItems` `#sumQty` อัปเดตสดใน `setItem()`)
- ขั้น 2 `wizAttach()`: `.upload-zone` → `#rprFile` `pickFiles()` · `.file-row` ลบ `removeFile()`
- ขั้น 3 `wizReview()`: `.review-card` ×3 (ข้อมูลใบแจ้งซ่อม · รายการแจ้งซ่อม `itemsTable()` · เอกสารแนบ)
- `.dw-footer`: ย้อนกลับ `wizBack()` · ยกเลิก `closeDrawer()` · `#btnNext` `wizNext()` / `#btnDraft` `saveDraft()` · `#btnSaveSubmit` `saveAndSubmit()`
### P-03 ดู (`renderViewDrawer()` · `#drawer` 920)
- `.dw-head` `.doc-ident` (เลขที่ `.dw-title` + `docPill()`) · `.dw-sub` 1 fact (n รายการ · x ชิ้น) · `.dw-actions` ตามสถานะ (`#btnSubmitView` / `#btnApproveView` `.btn-success` / ยกเลิก) + ไอคอนพิมพ์/ดาวน์โหลด `genPdf()` · ปิด
- `.drawer-tabs` (`tabBtn()`): รายละเอียด `renderDetailTab()` · PDF Preview `renderPdfTab()` · ลายเซ็น / อนุมัติ `renderSignTab()` · ประวัติ `renderHistoryTab()` (+ `.dt-count`)
- `.dw-footer` แก้ไขล่าสุด · ปิด

## §5 Component Inventory
| Component | anchor | states |
|---|---|---|
| ตารางกรอกรายการ | `.it-tbl` · `itemRow()` · `setItem()` (soft update ไม่ rebuild) | default · invalid (`.is-bad` + `.it-err-row` ข้อความแรก) · ลบได้เมื่อ ≥2 แถว |
| การ์ดสรุป | `.wz-sum` · `sumCard()` | สด (จำนวนรายการ/ชิ้น) · ผู้พิจารณาต่อขั้นจาก `resolveDoa()` |
| emp-chip (คน) | `.emp-chip` `.emp-av` · `empChip()` · `personIc()` | — |
| pill สถานะ | `docPill()` · `DOC_ST` · `RETURNED` | ร่าง · ตีกลับแก้ไข · รออนุมัติ · อนุมัติแล้ว · ยกเลิก |
| ลายเซ็น n/N | `.sign-prog` `.sp-bar` `.sp-fill` · `renderSignProgress()` | ร่าง = — |
| sub-table + แผงว่าง | `.sub-tbl` · `.sub-empty` · `subEmpty()` · `itemsTable()` · `histTable()` | มีข้อมูล / ว่าง |
| ตัวเลือกวัน พ.ศ. | `.bedate` · `bedateHTML()` · `.bd-pop` | ว่าง (placeholder) · เลือกแล้ว · วันเกิน max disabled |
| ตาราง ประวัติการซ่อม (modal) | `.hist-ed` · `histEditor()` | จำนวนครั้งผิด = `.is-bad` |
| slot ผู้พิจารณา | `.slot-row` · `searchSelectHTML('slot'+i)` | ค่าเริ่ม resolve · ว่าง = `.is-invalid` |
| preset เหตุผล | `.chip-row` `.chip` · `presetChips()` `setReasonPreset()` | is-on |
| PDF slot | `.pdf-slot` `.pdf-frame` (iframe srcdoc) · `fitPdf()` · `.pdf-gen` ซ่อน | — |
| upload | `.upload-zone` · `gateFiles()` | ชนิด/ขนาดผิด = toast error |
| seg tabs | `.seg` `.seg-btn.on` `.seg-n` | active (dot primary) |

## §6 Overlay Registry
| Overlay | anchor | ขนาด | เปิด | ปิด |
|---|---|---|---|---|
| drawer ดู | `#drawer.drawer-panel` | 920 | `showDrawer()` | ปุ่มปิด · Esc · mousedown ที่ `#drawerBackdrop` (`drawerBackdropDown()`) |
| drawer สร้าง/แก้ | `#drawer.drawer-panel.wide` | 1290 | `startWizard()` | dirty → modal "ทิ้งข้อมูลที่กรอกไว้?" ก่อน |
| modal | `#modal` (`.modal.is-lg` 720 สำหรับส่ง/ตรวจสอบขั้นแรก) | 520 / 720 | `openModalCfg()` | ปุ่ม · Esc · mousedown ที่ `#modalBackdrop` (`modalBackdropDown()` — **มีข้อความเหตุผล/ความเห็นค้าง = ห้ามปิด**) |
| row-menu ⋮ | `.row-menu` (portal `#overlay-root`) | 180 | `openRowMenu()` | คลิกที่อื่น · scroll · `closeRowMenu()` |
| user-menu | `#userMenu` `.user-menu` | — | `toggleUserMenu()` | คลิกที่อื่น |
| search-select list | `ss-list` (portal) | — | focus | click-outside / Esc |
| ปฏิทิน พ.ศ. | `.bd-pop` | 280 | `bdToggle()` | คลิกนอก · Esc (ปิดแค่ปฏิทิน) · `bdClose()` ตอนปิด modal/drawer |
| toast | `#toast` | — | `showToast()` | อัตโนมัติ 2.8 วิ |

## §7 Interaction Spec
- **Esc chain** (BASE-KIT keydown): ปฏิทิน (`bdClose()` capture + stopPropagation) → search-select list → modal (`closeModal()`) → drawer (`closeDrawer()` · dirty = modal ทิ้งข้อมูล)
- backdrop ปิดด้วย `onmousedown` เท่านั้น (ลากจากในไปปล่อยนอก ไม่ปิด · Rule #122)
- `setItem()` ไม่ re-render ระหว่างพิมพ์ (focus ไม่หลุด) · `addItem()` focus ช่องรายการแถวใหม่
- `openRowMenu()` render ไอคอนเฉพาะในเมนู (กันคลิกทะลุไปเปิดแถว)
- บันทึก/ส่ง/ตัดสิน: `S.busy` → ปุ่ม disabled + "กำลังบันทึก…" (กัน double-submit)
- `render()` ห่อ `preserveRenderState()`/`restoreRenderState()` คืน scroll/focus

## §8 State-Driven UI Matrix
| สถานะ | pill | ปุ่มหัว drawer (ใคร) | ⋮ |
|---|---|---|---|
| draft | ร่าง | ยกเลิก · แก้ไข · ส่งขออนุมัติ (เจ้าของ) | ดูรายละเอียด · แก้ไข · พิมพ์ · ยกเลิกเอกสาร |
| draft + returned | ตีกลับแก้ไข (`pill-danger`) | เหมือน draft + แถบเหตุผล `viewBanner()` | เหมือน draft |
| pending | รออนุมัติ | [คำปฏิเสธ] · [คำอนุมัติ] `.btn-success` (ผู้พิจารณาขั้นปัจจุบัน) / ยกเลิกเอกสาร (เจ้าของ/admin) | ดู · พิมพ์ · ยกเลิก (สิทธิ์) |
| approved | อนุมัติแล้ว | — (ล็อก "อนุมัติแล้ว ล็อกแก้ไข") | ดู · พิมพ์ |
| cancelled | ยกเลิก | — | ดู · พิมพ์ |
คำตัดสินผูก role (`wordsOf()` · `DECISION_WORDS`): role-line-manager = ตรวจสอบแล้ว / ไม่ผ่านการตรวจสอบ · default = อนุมัติ / ไม่อนุมัติ

## §9 Microcopy (verbatim)
### toast
- ไม่มีการแจ้งเตือนใหม่ · แบบเอกสารนี้ยังไม่เปิดใช้งาน · แก้ไขได้เฉพาะร่างของตัวเอง · กรุณากรอกข้อมูลให้ครบถ้วน · บันทึกร่างแล้ว · {เลขที่} · ส่งขออนุมัติแล้ว · {เลขที่} · จำนวนครั้งที่ซ่อมต้องเป็นตัวเลข · ส่งออก {n} รายการ · สลับเป็น {ชื่อ} · แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ตรวจสอบแล้ว · {เลขที่} / อนุมัติแล้ว · {เลขที่} · ตีกลับเป็นร่างแล้ว · {เลขที่} · ยกเลิกเอกสารแล้ว · {เลขที่} · ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่ · คุณไม่มีสิทธิ์ทำรายการนี้ · ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
### ข้อความในหน้า (สกัดจาก HTML)
- (ขั้น
- : 'ยกเลิกเอกสาร?',
- [Lucide] All CDNs failed. Icons จะไม่แสดง but UI ยังใช้งานได้
- ]); if (canCancel(r)) items.push(['x-circle', 'ยกเลิกเอกสาร',
- ], ['printer', 'พิมพ์',
- ]]; if (isOwner(r) && r.status === 'draft') items.splice(1, 0, ['pencil', 'แก้ไข',
- showToast('ไม่มีการแจ้งเตือนใหม่','info')
- · ผู้แจ้งแก้แล้วส่งใหม่ได้ เลขที่เดิม
- · อนุมัติแล้ว ล็อกแก้ไข
- · เปิดอยู่
- ก.ค.
- ก.พ.
- ก.ย.
- กมล ขยันดี
- กรกฎาคม
- กรอก
- กรอกทรัพย์สินที่ชำรุดทีละรายการ — ชื่อ ตำแหน่ง ฝ่าย ระบบใส่ให้
- กระดาษติดบ่อย พิมพ์เป็นเส้น
- กรุณากรอกข้อมูลให้ครบถ้วน
- กันยายน
- กำลังเปิดหน้าต่างพิมพ์ ·
- กุญแจล็อกไม่ได้
- กุมภาพันธ์
- ขั้นทดสอบ
- ขาโต๊ะโยก
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลรายการไม่ครบ
- ข้อมูลหลักใบแจ้งซ่อม
- ข้าม
- คน
- คลังสินค้า
- คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค่าเริ่มต้นจากสายอนุมัติ (DOA กลาง) และผังองค์กร
- ค้นหา...
- ค้นหาเลขที่ / ผู้แจ้ง / รายการ / ทะเบียนสินทรัพย์
- จำนวน
- จำนวนครั้งที่ซ่อมต้องเป็นตัวเลข
- จำนวนชิ้น
- จำนวนรายการ
- ชนิดไฟล์ไม่รองรับ
- ชื่อ-นามสกุล
- ชื่อทรัพย์สิน
- ชื่อฟังก์ชัน
- ช่างซ่อมบำรุง
- ซ่อมเองได้แล้ว
- ซ่อมเองได้แล้ว — เปลี่ยนล้อจากอะไหล่ที่มี
- ณัฐชา บุญมา
- ดาวน์โหลด PDF
- ต.ค.
- ตรวจสอบและยืนยัน
- ตรวจสอบแล้ว
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตีกลับเป็นร่าง — รอผู้แจ้งแก้แล้วส่งใหม่
- ตีกลับเป็นร่างแล้ว ·
- ตีกลับแก้ไข
- ตุลาคม
- ตู้เย็นห้องพักพนักงาน
- ตู้เอกสารเหล็ก
- ต้อง
- ตําแหน่ง
- ถึง
- ถ่านมอเตอร์หมด
- ทะเบียนสินทรัพย์
- ทั้งหมด
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ทุกฝ่าย/แผนก
- ทุกสถานะ
- ธ.ค.
- ธันวาคม
- บันทึกผิด
- บันทึกร่างแล้ว ·
- ประตูกระจกทางเข้า
- ประวัติ
- ประวัติ (append-only)
- ประเสริฐ มั่นคง
- ปั๊มน้ำหล่อเย็น
- ปิด
- ผู้จัดการทั่วไป
- ผู้จัดการฝ่ายขาย
- ผู้จัดการฝ่ายบัญชี
- ผู้ตรวจสอบ
- ผู้ส่ง
- ผู้อนุมัติ
- ผู้แจ้งซ่อม
- ฝ่าย/แผนก
- ฝ่ายขาย
- ฝ่ายขาย ชั้น 3
- ฝ่ายธุรการ
- ฝ่ายบริหาร
- ฝ่ายบริหารสินทรัพย์
- ฝ่ายบัญชี
- ฝ่ายผลิต
- พ.ค.
- พ.ย.
- พนักงานขาย
- พฤ
- พฤศจิกายน
- พฤษภาคม
- พัดลมระบายอากาศ
- พิมพ์
- พิมพ์ไม่ออก ไฟสีส้มกะพริบ
- ภาพอาการเครื่องถ่ายเอกสาร.jpg
- ภาพไม่ชัด สีเพี้ยน
- ม.ค.
- มกราคม
- มอเตอร์ไม่หมุน
- มิ.ย.
- มิถุนายน
- มี.ค.
- มีนาคม
- มีเสียงดัง น้ำรั่วที่ซีล
- ยกเลิก
- ยกเลิกเอกสาร
- ยกเลิกเอกสารแล้ว ·
- ยังไม่มีข้อมูล
- ยังไม่มีใบแจ้งซ่อมสินทรัพย์
- ยังไม่ส่ง
- ยังไม่ได้เลือกผู้พิจารณา
- ย้อนกลับ
- รถยกไฟฟ้า
- รอครบสาย
- รอคิว
- รอฉันพิจารณา
- รอพิจารณา — ขั้นปัจจุบัน
- รออนุมัติ
- รายการ
- รายละเอียด
- ร่าง
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ลายเซ็น
- ลายเซ็น / อนุมัติ
- ลำดับการอนุมัติ
- ล้อหัก
- ล้างตัวกรอง
- วรวุฒิ ทองดี
- วันที่ ........./........./.........
- วันที่แจ้ง
- วิไล บริหารทรัพย์
- ศศิธร มีสุข
- ส.ค.
- สถานที่ตั้ง
- สถานะ
- สถานะเอกสาร
- สมชาย ตรวจงาน
- สมศรี ใจดี
- สร้าง PDF
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างโดย
- สร้างใบแจ้งซ่อม
- สลับเป็น
- สว่านไฟฟ้า
- สายอนุมัติ
- สิงหาคม
- ส่งขออนุมัติ
- ส่งขออนุมัติ?
- ส่งขออนุมัติแล้ว ·
- ส่งซ่อมภายนอกแทน
- ส่งออก
- ส่งแล้วแก้ไขไม่ได้ — ถ้าถูกตีกลับจะกลับเป็นร่างให้แก้แล้วส่งใหม่
- หมายเหตุ
- หัวหน้าฝ่ายธุรการ
- หัวหน้าฝ่ายผลิต
- ห้องช่าง
- ห้องธุรการ
- อนุชา พรหมสุข
- อนุมัติ
- อนุมัติแล้ว
- อนุมัติให้ซ่อม — แจ้งผู้ดูแลงานซ่อม (rpr_ready_for_repair)
- อา
- อาการชำรุด
- อาคาร / ห้อง
- อาคาร A ชั้น 1
- อาคาร A ชั้น 2
- อาคารผลิต 1
- เก้าอี้สำนักงาน
- เครื่องถ่ายเอกสาร
- เครื่องปรับอากาศ ห้องประชุม 2
- เครื่องพิมพ์เลเซอร์
- เจ้าหน้าที่ธุรการ
- เจ้าหน้าที่บริหารสินทรัพย์
- เช่น ไม่เย็น มีน้ำหยด
- เดือนถัดไป
- เด้งกลับบน
- เบรกไม่อยู่ ยกของไม่ขึ้น
- เปิดไม่ติด แบตเตอรี่บวม
- เพิ่มเติม
- เม.ย.
- เมษายน
- เลขที่
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกคนตอนส่ง
- เลือกประเทศ
- เลือกผู้พิจารณา
- เลือกวันที่
- เหตุผลที่ยกเลิก
- เอกสารแนบ
- แก้ไขร่าง
- แก้ไขล่าสุด
- แก้ไขเอกสาร
- แก้ไขใบแจ้งซ่อม
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งซ่อมทรัพย์สินที่ชำรุดเพื่อส่งผู้ตรวจสอบและผู้อนุมัติ
- แจ้งซ่อมสินทรัพย์
- แจ้งซ้ำกับใบอื่น
- แจ้งผู้แจ้งซ่อมว่าต้องแก้อะไร
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบพิมพ์
- แบบฟอร์มใบแจ้งซ่อมสินทรัพย์
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- และจำนวน (มากกว่า 0)
- แล้ว ·
- โต๊ะทำงาน
- โน้ตบุ๊กพนักงานขาย
- โปรเจกเตอร์ห้องประชุม
- ไฟส่องสว่างคลัง
- ไม่ผ่านการตรวจสอบ
- ไม่พบทะเบียนสินทรัพย์ที่ระบุ
- ไม่พบทะเบียนสินทรัพย์ที่ระบุ — ตรวจเลข AS อีกครั้ง
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่มีข้อมูล
- ไม่ยกเลิก
- ไม่อนุมัติ
- ไม่เย็น
- ไม่เย็น มีน้ำหยด
- — คุณเป็นผู้พิจารณาขั้นนี้
- — ตีกลับเป็นร่าง

## §10 Data Binding & BACKEND anchors
| prototype | ระบบจริง (02_API) |
|---|---|
| `RECS` / `mkRec()` seed | API-01/02 |
| `persist()` (`SEQ` + `DOC.prefix`) | API-03/04 · ENG-DOC-NUM.next('RPR') (FN-03) |
| `resolveDoa()` · `MOCK_DOA_RESOLVED` (DOA-ENGINE-HOOK) | API-05 · GET /doa/resolve |
| `confirmSubmit()` | API-06 |
| `confirmApprove()` (+ history ขั้นแรก) · `confirmReason()` reject | API-07 |
| `confirmReason()` cancel | API-08 |
| `docPrintData()` + `tplRender()` + `RPR_TPL` + `PDF_CSS` | API-09 (server render template เดียวกัน · parity) |
| `exportCSV()` | API-10 |
| `pickFiles()` / `gateFiles()` | API-11 Document Center |
| `DOC.active` | F-DOCCFG status ของ RPR |
| `commitRejected()` + `S.sim` | 409 STALE / 403 / 500 (prototype-only) |

## §11 Traceability + Drift Log
| Brief | FRD | HTML anchor |
|---|---|---|
| §4 P-01 | 01_UI P-01 · API-01/10 | `renderPage()` |
| §4 P-02 | 01_UI P-02 · API-03/04/11 | `renderWizard()` |
| §4 P-03 | 01_UI P-03 · API-02/05..09 | `renderViewDrawer()` |
| §6 modal ส่ง | M-01 · API-06 · BR-05 | `renderModal()` kind submit |
| §6 modal ตรวจสอบ | M-02 · API-07 · BR-04 | `histEditor()` |
| §6 modal ไม่อนุมัติ/ยกเลิก | M-03/04 · API-07/08 · BR-06 | `confirmReason()` |
### ⚠️ Drift Log
| ประเภท | รายการ | ข้อเสนอ |
|---|---|---|
| HTML-only (prototype) | `window.__QA__` · ตัวสลับผู้ใช้ · `S.sim` · seed | ลบตอน build จริง |
| HTML-only | ปุ่ม "ไม่มีการแจ้งเตือนใหม่" (bell) เป็น placeholder ของ shell | ใช้ Notification Center จริง |
| FRD-only | `rpr.approved` domain event (ไม่ยิง DEC-02) | ไม่มีใน UI — ถูกต้อง |
ไม่มี business drift

## §12 Diff จากเวอร์ชันก่อน
— ไม่มีใน HTML นี้ (เวอร์ชันแรก)

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- Phase 2: ช่องทะเบียนสินทรัพย์เป็น search combobox จาก Asset Master + เติมรายการ/สถานที่ตั้งให้ (OQ-04)
- ดึงประวัติการซ่อมอัตโนมัติจาก Maintenance Schedule แทนให้ผู้ตรวจสอบกรอก
