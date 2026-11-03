# UI BRIEF — บันทึกภายใน (F-TMP-002)

## §0 Document Control
| หัวข้อ | ค่า |
|---|---|
| Feature | F-TMP-002 บันทึกภายใน (Internal Memo) *(รหัสชั่วคราว)* |
| Source of truth | `feature.html` (html-generator-v9.3) · archetype `Q-form` (`<meta name="cube-archetype">`) |
| Pair FRD | `FRD_F-TMP-002_Pack` (01_UI · 02_API · 05_RULES) — pair แล้ว |
| Scope Lock | `DECISIONS.lock` REQ-TMP-002 · **15 มติ** (AI-DEFAULT 11 + VALID 4) |
| prototype-only (ไม่ไปของจริง) | `window.__QA__` · ตัวสลับผู้ใช้ (`switchPersona()`) · `S.sim` จำลอง API ล้ม — ดู §13 Drift Log |
| วันที่ | 2026-10-07 |

## §1 Design Tokens
CSS variables ที่ประกาศใน `:root` (47 ตัว):
- **สี:** `--c-navy` `--c-navy-2` `--c-primary` `--c-primary-hover` `--c-teal` `--c-teal-light` `--c-ink` `--c-mute` `--c-mute-2` `--c-mute-3` `--c-placeholder` `--c-line` `--c-line-2` `--c-line-3` `--c-bg-off` `--c-success` `--c-warning` `--c-danger`
- **เลย์เอาต์:** `--sidebar-w` `--shell-h`
- **ตัวอักษร:** `--fs-h1` `--fs-h2` `--fs-h3` `--fs-body` `--fs-sub` `--fs-meta` `--fs-cap` `--fs-kpi`
- **ระยะ:** `--sp-xs` `--sp-sm` `--sp-md` `--sp-lg` `--sp-xl`
- **มุมมน:** `--r-xs` `--r-sm` `--r-md` `--r-lg` `--r-full`
- **z-index:** `--z-content` `--z-sticky` `--z-shell` `--z-dropdown` `--z-backdrop` `--z-drawer` `--z-modal` `--z-popover` `--z-toast`
- Font: Satoshi + Noto Sans Thai (Fontshare + Google Fonts) · ไอคอน Lucide 0.469.0 multi-CDN fallback
- Scrollbar: custom 5px มุมมน (`::-webkit-scrollbar` + `scrollbar-width`) — ห้าม default

## §2 Z-index map (สูง → ต่ำ)
| ชั้น | token | ใช้ที่ |
|---|---|---|
| toast | `var(--z-toast)` | `.toast` · `#toast` |
| popover | `var(--z-popover)` | `.menu-fixed` · `.row-menu` · `.ss-list.menu-fixed` |
| modal | `var(--z-modal)` | `.modal-backdrop` (v9.1 Rule #62 — modal เหนือ drawer) |
| drawer | `var(--z-drawer)` | `.drawer` · `#drawer` |
| backdrop | `var(--z-backdrop)` | `.drawer-backdrop` · `#drawerBackdrop` · `.ss-list` |
| dropdown | `var(--z-dropdown)` | `.user-menu` · `.info-tip::after` |
| sticky | `var(--z-sticky)` | `.shell-bar` · `.table-wrap thead th` · `.wizard-footer` |
| shell | `var(--z-shell)` | `.sidebar` |
| content | `var(--z-content)` | พื้นหน้าปกติ |
| ภายใน stepper | `3` · `2` · `1` | `.table-scroll.is-sticky thead th` · `.stepper-circle` · `.stepper-item:not(:last-child)::after` |

## §3 Route map
| route | หน้าจอ | refresh-safe |
|---|---|---|
| `#/memo` | รายการบันทึกภายใน | ✓ |
| `#/memo/create` | drawer สร้างบันทึก (wizard 3 ขั้น) | ✓ |
| `#/memo/edit/:id` | drawer แก้ไขร่าง | ✓ |
| `#/memo/view/:id` | drawer ดูเอกสาร (4 แท็บ) | ✓ |

- hash router: `getRoute()` → `applyRoute()` · ผูกกับ `hashchange`
- default route = `memo` · route ที่ไม่รู้จัก → ปิด drawer กลับรายการ
- เปลี่ยน route จากในแอปผ่าน `go()` (กัน error เมื่อ host ไม่รองรับ hash)

## §4 Anatomy — หน้ารายการ (`#/memo`)
| region | selector | สาระ |
|---|---|---|
| shell | `.sidebar` · `.shell-bar` · `#page-content` | เมนูซ้าย (HR › บันทึกภายใน) + breadcrumb + ผู้ใช้ปัจจุบัน |
| page header | `.ph` · `.ph-title` · `.ph-sub` · `.ph-count` | ชื่อไทย + (Internal Memo) + chip นับ |
| ปุ่มหลัก | `.ph-actions` | "ส่งออก CSV" · "สร้างบันทึก" (`#btnCreate`) — ปุ่มสร้างอยู่ขวาสุดเสมอ (Rule #46) |
| แถบเตือน | `.alert-row` | ขึ้นเมื่อ `DOC.active = false` |
| สถิติ | `.stats` · `.stat` (`.is-click` / `.is-on`) | บันทึกทั้งหมด · รออนุมัติ · รอฉันพิจารณา — กดเพื่อกรอง |
| ตัวกรอง | `.filter-bar` · `#fq` · `.fb-field` · `.fb-spacer` | ค้นหา · สถานะ · หน่วยงาน · ปุ่มล้างตัวกรอง |
| ตาราง | `.table-wrap` · `.table` · `.is-sortable` | เลขที่ · วันที่ · จาก · เรียน · เรื่อง · สถานะเอกสาร · ลายเซ็น · ⋮ |
| ความคืบหน้าลายเซ็น | `.sign-prog` · `.sp-bar` · `.sp-fill` | n/N + แถบ · `.is-bad` เมื่อไม่อนุมัติ |
| เมนูแถว | `.row-menu` · `.ra-btn` | portal ไป `#overlay-root` ด้วย `portalMenu()` (Rule #95) |
| ท้ายตาราง | `.table-footer` · `.pagination` · `.pg-btn` | หน้าละ 20 รายการ |
| ว่าง | empty state 2 แบบ ผ่าน `emptyStateHTML()` | "ไม่พบรายการที่ค้นหา" / "ยังไม่มีบันทึกภายใน" |

render โดย `renderPage()` · กดแถว = `rowClick()` → `openView()`

## §5 Anatomy — Wizard สร้าง/แก้ไข (`.drawer-panel.wide`)
`renderWizard()` · ขั้นตอนล็อก `['ข้อมูลหลักบันทึก', 'เอกสารแนบ', 'ตรวจสอบและยืนยัน']`

| ขั้น | selector | ช่อง |
|---|---|---|
| หัว | `.dw-head` · `.dw-eyebrow` · `.dw-title` · `.d-stepper` · `.stepper-item` · `.stepper-circle` | "สร้างเอกสารใหม่" / "แก้ไขเอกสาร" |
| 1 | `.wz-split` · `.wz-main` · `.wz-card` · `.wz-card-h` · `.wz-no` | `#mTo` เรียน · `#mSubject` เรื่อง · `#mBody` เนื้อความ (textarea 10 แถว) |
| 1 (ขวา) | `.wz-sum` · `.wz-sum-row` · `.wz-sum-total` · `.wz-sum-foot` | จาก · วันที่ · เลขที่ · `#sumTo` · `#sumSubj` · `#sumLen` — soft update ผ่าน `setF2()` |
| 2 | `.upload-zone` · `.uz-ic` · `.uz-t` · `.uz-d` · `#memFile` · `.file-row` | แนบไฟล์หลายไฟล์ · ลบรายไฟล์ |
| 3 | `.review-card` · `.review-title` · `.memo-subject` · `.memo-prose` | สรุปก่อนส่ง |
| footer | `.dw-footer` · `.dw-footer-right` · `#btnNext` · `#btnDraft` · `#btnSaveSubmit` | ย้อนกลับ · ยกเลิก · ถัดไป / บันทึกแบบร่าง + บันทึกและส่งอนุมัติ |

- หัวข้อขั้น: `.step-h` + `.step-hint`
- error: `.field.is-invalid` + `.input.is-bad` + `.field-error` — ตรวจด้วย `validateMain()` เรียกจาก `wizNext()` / `saveDraft()` / `saveAndSubmit()`
- **ไม่มีช่องวันที่ของเบราว์เซอร์** (Rule #114) — ฟอร์มนี้ไม่มีช่องวันที่ให้ผู้ใช้กรอก

## §6 Anatomy — View drawer (`#/memo/view/:id`)
`renderViewDrawer()` · drawer 920 · แท็บล็อก 4 ตัวผ่าน `.drawer-tabs` · `.drawer-tab`

| แท็บ | function | selector เด่น |
|---|---|---|
| รายละเอียด | `renderDetailTab()` | `.drawer-section` · `.drawer-fields` · `.memo-subject` · `.memo-prose` · `.file-row` |
| PDF Preview | `renderPdfTab()` | `.pv-bar` · `.pv-meta` · `.pv-actions` · `.a4` · `.pdf-slot` · `.pdf-frame` |
| ลายเซ็น / อนุมัติ | `renderSignTab()` | `.review-card` · `.sp-bar.is-wide` · `.timeline` · `.tl-item` · `.tl-dot` · `.tl-acts` |
| ประวัติ | `renderHistoryTab()` | `.timeline` (append-only · เรียงใหม่→เก่า) |

- หัว drawer: `.doc-ident` · `.doc-ident-ic` · `.dw-sub` · ปุ่มไอคอน `.top-icon-btn` (พิมพ์ · ดาวน์โหลด PDF · ปิด)
- ปุ่มตามสถานะ: ร่าง → ยกเลิก · แก้ไข · `#btnSubmitView` | รอ (ผู้พิจารณาขั้นปัจจุบัน) → ไม่อนุมัติ · `#btnApproveView` | ไม่อนุมัติ (เจ้าของ) → "แก้แล้วส่งใหม่" (`reopenDraft()`)
- แบนเนอร์สถานะ: `.alert-row` / `.alert-row.is-danger`

## §7 Overlay registry + dismiss rules
| overlay | selector | เปิดด้วย | ปิดด้วย | หมายเหตุ |
|---|---|---|---|---|
| drawer | `.drawer` / `#drawer` + `.drawer-backdrop` / `#drawerBackdrop` | `showDrawer()` | คลิก backdrop · ปุ่ม "ปิด" · `closeDrawer()` | wizard ที่แก้ค้าง → เด้ง modal "ทิ้งข้อมูลที่กรอกไว้?" ก่อน |
| modal | `.modal` / `#modal` + `.modal-backdrop` / `#modalBackdrop` | `openModalCfg()` | `closeModal()` · คลิก backdrop | **ห้ามปิดด้วย backdrop** เมื่อกรอกเหตุผล/ความเห็นค้าง (`modalBackdropClick()`) |
| row menu ⋮ | `.row-menu` | `openRowMenu()` | คลิกที่อื่น · scroll · `closeRowMenu()` | portal ไป `#overlay-root` + position fixed |
| search-select | `.ss-list` (+ `.menu-fixed` เมื่อ portal) | `initSearchSelect()` | คลิกนอก · เลือกค่า | ใช้แทน `<select>` ตาม Rule #34 |
| user menu | `.user-menu` · `#userMenu` | `toggleUserMenu()` | คลิกนอก · เลือกผู้ใช้ | เดโมสลับผู้ใช้เท่านั้น |
| toast | `.toast` · `#toast` | `showToast()` | หายเอง | ชนิด info / success / warning / error |

**Esc chain:** modal → drawer → overlay (`.ss-list` / `.row-menu`) — ปิดทีละชั้นจากบนลงล่าง

## §8 State-driven UI
| สถานะ (`DOC_ST`) | ป้าย | pill class | ปุ่มบนหัว drawer | เมนู ⋮ |
|---|---|---|---|---|
| `draft` | ร่าง | `pill-muted` | ยกเลิก · แก้ไข · ส่งอนุมัติ (เฉพาะเจ้าของ) | แก้ไข · พิมพ์ · ยกเลิกเอกสาร |
| `pending` | รออนุมัติ | `pill-warning` | ไม่อนุมัติ · อนุมัติ (เฉพาะผู้พิจารณาขั้นปัจจุบัน) · ยกเลิกเอกสาร (เจ้าของ/admin) | พิมพ์ · ยกเลิกเอกสาร |
| `approved` | อนุมัติแล้ว | `pill-success` | ยกเลิกเอกสาร (เจ้าของ/admin) | พิมพ์ · ยกเลิกเอกสาร |
| `rejected` | ไม่อนุมัติ | `pill-danger` | แก้แล้วส่งใหม่ (เจ้าของ) | แก้แล้วส่งใหม่ · พิมพ์ |
| `cancelled` | ยกเลิก | `pill-muted` | — | พิมพ์ |

สถานะขั้นในสาย DOA: `approved` อนุมัติ · `rejected` ไม่อนุมัติ · `pending` รอพิจารณา · `waiting` ยังไม่ถึงขั้น · `skipped` ข้าม
สิทธิ์: `canSee()` · `canAct()` · `isOwner()` · `isAdmin()` · `canCancel()` — ตรงกับ DEC-09

## §9 Microcopy (verbatim จากโค้ด — ห้าม paraphrase)
**Toast คงที่:** `ไม่มีการแจ้งเตือนใหม่` · `แบบเอกสารนี้ยังไม่เปิดใช้งาน` · `แก้ไขได้เฉพาะร่างของตัวเอง` · `กรุณากรอกข้อมูลให้ครบถ้วน` · `แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง` · `ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง` · `ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่` · `คุณไม่มีสิทธิ์ทำรายการนี้`
**Toast แบบประกอบ (ต่อท้ายด้วยเลขที่/ชื่อ):** `บันทึกร่างแล้ว ·` · `ส่งอนุมัติแล้ว ·` · `อนุมัติแล้ว ·` · `ไม่อนุมัติแล้ว ·` · `ยกเลิกเอกสารแล้ว ·` · `กำลังเปิดหน้าต่างพิมพ์ ·` · `ส่งออก` (+ จำนวน + `รายการ`) · `สลับเป็น` (+ ชื่อ)
**ปุ่ม:** `สร้างบันทึก` · `ส่งออก CSV` · `ล้างตัวกรอง` · `ถัดไป` · `ย้อนกลับ` · `ยกเลิก` · `บันทึกแบบร่าง` · `บันทึกและส่งอนุมัติ` · `ส่งอนุมัติ` · `อนุมัติ` · `ไม่อนุมัติ` · `ยกเลิกเอกสาร` · `ไม่ยกเลิก` · `แก้แล้วส่งใหม่` · `แก้ไข` · `พิมพ์` · `ดาวน์โหลด PDF` · `ปิด` · `เพิ่มเติม` · `กลับไปกรอกต่อ` · `ทิ้งข้อมูล` · `แนบไฟล์เพิ่ม`
**หัวข้อ/ป้าย:** `บันทึกภายใน` · `สร้างเอกสารใหม่` · `แก้ไขเอกสาร` · `ข้อมูลหลักบันทึก` · `เอกสารแนบ` · `ตรวจสอบและยืนยัน` · `ส่งถึงใคร เรื่องอะไร` · `เนื้อหาบันทึก` · `เนื้อความ` · `เรียน` · `เรื่อง` · `จาก (ผู้จัดทำ)` · `วันที่` · `เลขที่` · `สถานะ` · `สถานะเอกสาร` · `ลายเซ็น` · `ข้อมูลเอกสาร` · `ข้อมูลระบบ` · `ข้อคิดเห็นฝ่ายกฎหมาย` · `ลำดับการอนุมัติ` · `ประวัติ (append-only)` · `สรุปบันทึก` · `บันทึกทั้งหมด` · `รออนุมัติ` · `รอฉันพิจารณา` · `ร่าง` · `อนุมัติแล้ว ·` · `ยังไม่ถึงขั้น` · `รอผล` · `ทุกหน่วยงาน` · `ทุกสถานะ` · `ฝ่ายกฎหมาย` · `ย่อหน้า ·` · `คลิกเพื่อดูรายการ` · `ไม่มีรายการค้าง`
**Placeholder / hint:** `ค้นหาเลขที่ / ผู้จัดทำ / เรียน / เรื่อง` · `เช่น ผู้จัดการฝ่ายกฎหมาย` · `เช่น ขอให้ตรวจร่างสัญญาจ้างเหมาบริการ` · `เขียนเนื้อความของบันทึก — ขึ้นบรรทัดใหม่เพื่อแยกย่อหน้า` · `เลือกผู้พิจารณา` · `ค่าเริ่มต้นจากสายอนุมัติ (DOA) และผังองค์กร` · `กรอกตามแบบ` (+ `FM-HRM-54`) · `เหตุผลที่ยกเลิก` · `แจ้งผู้จัดทำว่าต้องแก้อะไร — ข้อความนี้ขึ้นบนแบบพิมพ์`
**ข้อความว่าง/ผิดพลาด:** `ไม่พบรายการ` (+ `ที่ค้นหา`) · `ลองปรับคำค้นหรือล้างตัวกรอง` · `ยังไม่มีบันทึกภายใน` · `ยังไม่มีเนื้อหา` · `ไม่มีเอกสารแนบ` · `กรุณาระบุผู้รับบันทึก` · `กรุณาระบุเรื่อง` · `กรุณาเขียนเนื้อหาบันทึก` · `กรุณาระบุเหตุผล` · `กรุณาเลือกผู้พิจารณา`
**ชิปเหตุผลสำเร็จรูป:** `เอกสารแนบไม่ครบ` · `ข้อความยังไม่ชัดเจน` · `ต้องแก้เงื่อนไขก่อนเสนอลงนาม` · `เรื่องยกเลิกหรือเลื่อนออกไป` · `ส่งผิดหน่วยงาน` · `บันทึกผิด`
**แบบพิมพ์:** `วันที่ ........./........./.........` · `พิจารณาในระบบ` · `เอกสารนี้จัดทำโดยระบบ CUBE NATIVE` · `Doc No. FM-HRM-54`
**เดือนไทยในแบบพิมพ์ (`TH_MONTH`):** `มกราคม` `กุมภาพันธ์` `มีนาคม` `เมษายน` `พฤษภาคม` `มิถุนายน` `กรกฎาคม` `สิงหาคม` `กันยายน` `ตุลาคม` `พฤศจิกายน` `ธันวาคม` · แบบย่อ `ม.ค.` `ก.พ.` `มี.ค.` `เม.ย.` `พ.ค.` `มิ.ย.` `ก.ค.` `ส.ค.` `ก.ย.` `ต.ค.` `พ.ย.` `ธ.ค.`

## §10 Data binding + BACKEND anchors
| จุด | anchor ใน HTML | ของจริงต้องต่อกับ |
|---|---|---|
| ออกเลขที่ | `persist()` — `DOC.prefix + '-2569-' + …` | `ENG-DOC-NUM.next('MEM')` (API-03 · MEM-FN-01) |
| เปิด/ปิดแบบเอกสาร | `DOC.active` | F-DOCCFG status |
| สายอนุมัติ | `MOCK_DOA_RESOLVED` · `resolveDoa()` · `resolveRole()` (marker **DOA-ENGINE-HOOK**) | DOA กลาง F-DLG-001 (API-05) |
| คำตัดสินบนแบบพิมพ์ | `DECISION_WORDS` · `wordsFor()` | `print_config.decision_words` |
| ข้อมูล PDF | `docPrintData()` → `tplRender()` + `tplSignRows()` | API-10 (server render template เดียวกัน) |
| แจ้งเตือนยกเลิก | `confirmReason()` (kind `cancel`) | `ENG-NOTIFY.emit('mem_cancelled')` (API-08) |
| ไฟล์แนบ | `gateFiles()` · `pickFiles()` | Document Center (API-12) |
| จำลอง API ล้ม | `commitRejected()` · `S.sim` | — (prototype เท่านั้น) |

## §11 Traceability (Brief ↔ FRD ↔ HTML)
| หน้าจอ / action | FRD | HTML |
|---|---|---|
| รายการ `#/memo` | 01_UI §1.2 · API-01/11 · MEM-FN-07 | `renderPage()` · `listRows()` |
| สร้าง/แก้ร่าง | 01_UI §1.3 · API-03/04 · MEM-FN-01/02 | `startWizard()` · `persist()` |
| ส่งอนุมัติ | API-05 · MEM-FN-03 · BR-MEM-07/08 | `openSubmit()` · `confirmSubmit()` |
| อนุมัติ | API-06 · MEM-FN-04 · BR-MEM-10 | `openApprove()` · `confirmApprove()` |
| ไม่อนุมัติ | API-07 · MEM-FN-05 · BR-MEM-04 | `openReject()` · `confirmReason()` |
| ยกเลิก | API-08 · MEM-FN-06 · BR-MEM-05 | `openCancel()` · `confirmReason()` |
| แก้แล้วส่งใหม่ | API-09 · MEM-FN-08 | `reopenDraft()` |
| PDF | API-10 · MEM-FN-09 · VR-01…03 | `renderPdfTab()` · `genPdf()` · `fitPdf()` |
| การมองเห็น | 05_RULES BR-MEM-06 · 06_TESTS §6.3 | `canSee()` · `canAct()` |

## §12 Diff จากเวอร์ชันก่อน
ไม่มี — เป็นรอบแรกของ feature นี้

## §13 Drift Log
| # | เรื่อง | สถานะ |
|---|---|---|
| D-01 | `window.__QA__` · `switchPersona()` · `S.sim` เป็นของ prototype เท่านั้น ระบบจริงลบออก | ตั้งใจ |
| D-02 | กระดาษไม่มี ☐ อนุมัติ/ไม่อนุมัติ แต่แบบพิมพ์แสดงคำตัดสินในช่องลงชื่อ (DEC-07 · AI-DEFAULT) | **รอลูกค้ายืนยัน** — ปิดได้ที่ `print_config.sign_boxes[].show_decision` |
| D-03 | แบบพิมพ์ไม่มีช่องลงชื่อผู้จัดทำ ต่างจากค่าเริ่มของสกิล (ผู้ขอ + ต่อขั้น) | ตั้งใจตาม DEC-14 |
| D-04 | ไม่มีปุ่ม "ทำซ้ำ" ที่ archetype มีให้ | ตั้งใจตาม DEC-11 (copy = ✗) |
| D-05 | WARN จาก `audit.sh` 3 ข้อตกทอดจาก BASE-KIT ของสกิล (Rule #21 · Rule #40 · hardcoded font-size ใน sidebar) | ตามไฟล์ canonical |
| D-06 | ยังไม่ได้รัน `e2e_standard.py` และ `render-check.py` (เครื่องไม่มี browser) | **ต้องรันก่อน UAT** |

## 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- ถ้าลูกค้าต้องการให้ "เรียน" ผูกกับผู้ใช้ในระบบ (ส่งแจ้งเตือนถึงผู้รับได้) ต้องแก้มติ G1/G10 แล้วล็อกใหม่ก่อน
- ถ้าต้องการให้บันทึกที่อนุมัติแล้วเข้าสารบรรณกลางอัตโนมัติ = เปลี่ยน DEC-02 (`post_to`)
