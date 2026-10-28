# UI BRIEF (AS-BUILT) — F-TMP-006 หนังสือสัญญายืม (กล่องบรรจุกระดาษ)

## §0 Document Control + Pairing
| หัวข้อ | ค่า |
|---|---|
| Feature | F-TMP-006 · REQ-TMP-006 (รหัสชั่วคราว) |
| ไฟล์ต้นแบบ | `feature.html` (html-generator-v9.2 · archetype **Q-form**) |
| คู่เอกสาร | `BRD_F-TMP-006.md` · `FRD_F-TMP-006_Pack/` · `DECISIONS.lock.md` · `print/LOA_print-spec.md` |
| ใบประกาศ | `DOCCFG_BRIEF_F-TMP-006.md` · `DOA_BRIEF_F-TMP-006.md` · `NTF_BRIEF_F-TMP-006.md` · `MDOC_BRIEF_LOA.md` |
| ชนิดเอกสาร | หนังสือสัญญา 2 ฝ่าย (ผู้รับมอบ = ลูกค้า · ผู้ส่งมอบ = บริษัท) · แบบพิมพ์ FM-SAL-14 Rev.00 |
| สถานะ | AS-BUILT จากต้นแบบ · audit FAIL 0 · **[NO-BROWSER] ยังไม่ได้รัน e2e / render-check** |
| วันที่ | 2026-10-07 |

## §2 Route Map
| route | หน้าจอ | refresh-safe |
|---|---|---|
| `#/loan-agreement` | ทะเบียนหนังสือสัญญายืม | ✓ |
| `#/loan-agreement/create` | drawer สร้างเอกสารใหม่ (3 ขั้น) | ✓ |
| `#/loan-agreement/edit/:id` | drawer แก้ไขร่าง | ✓ |
| `#/loan-agreement/view` | ฐานของ route ดูรายละเอียด | ✓ |
| `#/loan-agreement/view/:id` | drawer ดูรายละเอียด (4 แท็บ) | ✓ |
`applyRoute()` อ่าน hash แล้วเปิด drawer ให้ตรง · `go()` เขียน hash กลับทุกครั้งที่เปลี่ยนหน้าจอ

## §3 Layout Shell
- Sidebar 232px (`--sidebar-w`) · module `Sales` › feature `หนังสือสัญญายืม` + badge นับใบที่รอฉันพิจารณา
- Shell bar 52px (`--shell-h`) · breadcrumb `Core › Sales › หนังสือสัญญายืม` · ปุ่มแจ้งเตือน · user chip + เมนูสลับ persona
- `#overlay-root` และ `#toast` ก่อน `</body>` (Rule #95 portal)

## §4 Page Anatomy
### 4.1 ทะเบียน (`#/loan-agreement`)
`.page-fill` → `.ph` (หัวข้อ + chip นับ + ปุ่ม ส่งออก CSV / สร้างหนังสือสัญญา) → `.stats` 3 ใบ → `.card.list-card` (filter-bar → `.table-wrap` → `.table-foot`)
คอลัมน์: เลขที่ · วันที่ · ลูกค้าผู้ยืม · ผู้จัดทำ · รายการกล่อง · สถานะเอกสาร · ลายเซ็น · ⋮
เมนู ⋮: แก้ไข (ร่างของตัวเอง) · พิมพ์ · ยกเลิกเอกสาร — ตามมติ DEC-11 ไม่มีเมนูสร้างใบใหม่จากใบเดิม

### 4.2 drawer สร้าง/แก้ไข (`.drawer.drawer-panel.wide`)
`.dw-head` (eyebrow + title + `.d-stepper` 3 ขั้น) → `.drawer-body.is-soft` → `.dw-footer`
- ขั้น 1 `.wz-split` = `.wz-main` (การ์ด ① ลูกค้าผู้ยืมและที่ตั้งกล่อง · การ์ด ② รายละเอียดกล่องที่สนับสนุน · การ์ด ③ คู่สัญญาผู้รับมอบและข้อความในเงื่อนไข) + `.wz-sum` (การ์ดสรุปสด)
- ขั้น 2 `.upload-zone` + `.file-row`
- ขั้น 3 `.review-card` 4 ใบ (ข้อมูลหนังสือสัญญา · รายละเอียดกล่อง · คู่สัญญาผู้รับมอบ · เอกสารแนบ)

### 4.3 drawer ดูรายละเอียด (`.drawer.drawer-panel`)
`.dw-head` (doc-ident + pill สถานะ) → `.drawer-tabs` 4 แท็บ → `.drawer-body` → `.dw-footer`
แท็บ: รายละเอียด · PDF Preview (`.pdf-slot` + `iframe.pdf-frame` + `.copy-seg` สลับชุด) · ลายเซ็น (`.timeline`) · ประวัติ

## §5 Component Inventory
| component | class หลัก | ใช้ที่ |
|---|---|---|
| การ์ดสถิติ | `.stat` `.stat-label` `.stat-value` `.stat-meta` | ทะเบียน |
| ตารางข้อมูล | `.table` `.table-wrap` `.table-foot` | ทะเบียน · รายละเอียดกล่อง |
| การ์ดกรอกรายการกล่อง | `.trip` `.trip-h` `.trip-no` `.trip-why` `.trip-err` | ขั้น 1 |
| การ์ดสรุปสด | `.wz-sum` `.wz-sum-row` `.wz-sum-total` | ขั้น 1 |
| เนื้อสัญญา (ข้อความคงที่) | `.loa-terms` `.lt-item` `.lt-no` | แท็บรายละเอียด |
| ปุ่มสลับชุดเอกสาร | `.copy-seg` `.cs-btn` | แท็บ PDF Preview |
| บรรทัดบอกที่มาของค่า | `.sync-line` | ขั้น 1 · แท็บรายละเอียด |
| ฟอร์ม 2 คอลัมน์ | `.form-grid-2` | ขั้น 1 |
| search select | `.ss-list` `.menu-fixed` | ตัวกรอง · เลือกลูกค้า · เลือกผู้พิจารณา |
| ตัวเลือกวัน พ.ศ. | `.bedate` `.bd-pop` `.bd-grid` `.bd-day` | ช่องวันที่ของหนังสือ (Rule #114) |
| stepper | `.d-stepper` `.stepper-item` `.stepper-circle` | drawer สร้าง/แก้ไข |
| timeline | `.timeline` `.tl-item` `.tl-dot` `.tl-acts` | ลายเซ็น · ประวัติ |
| pill สถานะ | `.pill` `.pill-muted` `.pill-warning` `.pill-success` | ทะเบียน · drawer |
| ความคืบหน้าลายเซ็น | `.sign-prog` `.sp-bar` `.sp-fill` | ทะเบียน · แท็บลายเซ็น |
| row menu | `.row-menu` `.rm-item` | ทะเบียน (portal) |
| modal | `.modal` `.modal-header` `.modal-body` `.modal-footer` `.slot-row` | ส่ง/ลงนาม/ส่งกลับแก้ไข/ยกเลิก/ทิ้งข้อมูล |

## §7 Interaction Spec
- เลือกลูกค้า → `setCust()` เติมรหัส ที่อยู่ และชื่อผู้รับมอบจากทะเบียนให้ทันที (แก้ต่อได้)
- พิมพ์รายละเอียดกล่อง → `setLine()` อัปเดตตัวนับและการ์ดสรุปแบบ soft ไม่ rebuild ทั้งหน้า focus ไม่หลุด
- เลือกวันที่ → `bedateHTML()` เปิด `.bd-pop` ใน `#overlay-root` · Esc ปิดเฉพาะปฏิทิน ไม่ทะลุไปปิด drawer
- สลับชุดเอกสารในแท็บ PDF → `setCopy()` render ใหม่เฉพาะ iframe ของชุดนั้น
- ปิด drawer ขณะแก้ไขค้าง → modal `ทิ้งข้อมูลที่กรอกไว้?`
- ปุ่มบันทึก/ส่ง ระหว่างทำงาน = disabled + loader + `กำลังบันทึก…` (กัน double-submit)
- คลิกนอก row menu หรือ user menu → ปิดอัตโนมัติ · scroll → ปิด row menu
- `S.sim` = จำลองผลตอบกลับ API (`stale` · `denied` · `error` · `upload_fail`)

## §8 State-Driven UI Matrix
| สถานะ · ผู้ใช้ | ปุ่มหัว drawer | เมนู ⋮ | แก้ไขได้ |
|---|---|---|---|
| ร่าง · เจ้าของ | ยกเลิก · แก้ไข · ส่งให้ลงนาม | แก้ไข · พิมพ์ · ยกเลิกเอกสาร | ✓ |
| ร่าง (ถูกส่งกลับแก้ไข) · เจ้าของ | เหมือนร่าง + แบนเนอร์เหตุผล | เหมือนร่าง | ✓ |
| รอลงนาม · ผู้พิจารณาขั้นปัจจุบัน | ไม่ลงนาม · ลงนาม | พิมพ์ · ยกเลิกเอกสาร (ถ้ามีสิทธิ์) | ✗ |
| รอลงนาม · เจ้าของ | ยกเลิกเอกสาร | พิมพ์ · ยกเลิกเอกสาร | ✗ |
| ลงนามแล้ว | ยกเลิกเอกสาร (ถ้ามีสิทธิ์) | พิมพ์ | ✗ |
| ยกเลิก | — | พิมพ์ | ✗ |

## §9.1 ปุ่ม (verbatim)
สร้างหนังสือสัญญา · ส่งออก CSV · ล้างตัวกรอง · เพิ่มรายการกล่อง · ย้อนกลับ · ถัดไป · ยกเลิก · บันทึกแบบร่าง · บันทึกและส่งให้ลงนาม · แก้ไข · ส่งให้ลงนาม · ลงนาม · ไม่ลงนาม · ยกเลิกเอกสาร · พิมพ์ · ดาวน์โหลด PDF · ปิด · กลับไปกรอกต่อ · ทิ้งข้อมูล · ต้นฉบับ · สำเนา

## §9.4 ป้ายช่องและหัวข้อ (คัดตรงจากกระดาษ — ห้ามเกลา)
หนังสือสัญญายืม · วันที่ · ขอสนับสนุนกล่องบรรจุกระดาษสำหรับ · (รหัสลูกค้า · ซึ่งตั้งอยู่เลขที่ · เพื่อใช้ในกิจการ โดยไม่คิดมูลค่า ดังมีรายละเอียดต่อไปนี้ · เงื่อนไข : · แตกหักโดยมิใช่การใช้ · ผู้รับมอบ · ผู้ส่งมอบ · ลงนาม · ต้นฉบับ · สำเนา · Doc. No. : FM-SAL-14 · Rev.00 : 01/07/2569
> ป้ายในหน้าจอที่ตั้งชื่อใหม่เพื่อให้อ่านรู้เรื่อง: ลูกค้าผู้ยืม · รหัสลูกค้า · ที่อยู่ที่ตั้งกล่อง · รายละเอียดกล่องที่สนับสนุน · ชื่อผู้รับมอบ · ตำแหน่งผู้รับมอบ · ข้อความในเงื่อนไขข้อ 1 (ช่องเติมในเนื้อสัญญา) · วันที่ของหนังสือ

## §9.5 ข้อความสถานะ / ว่าง / เตือน (verbatim)
- สถานะเอกสาร: ร่าง · รอลงนาม · ลงนามแล้ว · ยกเลิก
- สถานะขั้นลงนาม: ยังไม่ส่ง · รอพิจารณา · ลงนาม · ไม่ลงนาม · ข้าม
- ว่าง: ยังไม่มีหนังสือสัญญายืม · ไม่พบรายการที่ค้นหา · ไม่มีเอกสารแนบ · ยังไม่ได้ใส่รายละเอียดกล่อง
- เตือน: กรุณากรอกข้อมูลให้ครบถ้วน · กรุณาเลือกลูกค้า · กรุณาใส่ที่อยู่ที่ตั้งกล่อง · กรุณาใส่ชื่อผู้รับมอบ · กรุณาระบุเหตุผล · กรุณาเลือกผู้พิจารณา

## §10 Data Binding & BACKEND anchors
| หน้าจอ | ฟังก์ชัน | endpoint จริง (02_API) |
|---|---|---|
| ทะเบียน | `listRows()` · `renderPage()` | A1 `GET /sales/loan-agreements` |
| เปิดดู | `openView()` · `renderViewDrawer()` | A2 `GET /sales/loan-agreements/{id}` |
| บันทึกร่าง | `persist()` · `saveDraft()` | A3 `POST` · A4 `PUT` |
| ส่งให้ลงนาม | `openSubmit()` · `confirmSubmit()` | A5 `POST /submit` |
| ลงนาม | `confirmApprove()` | A6 `POST /sign` |
| ส่งกลับแก้ไข / ยกเลิก | `confirmReason()` | A7 `POST /return` · A8 `POST /cancel` |
| แบบพิมพ์ | `loaPdfData()` · `tplRender()` · `genPdf()` | A9 `GET /pdf` |
| ไฟล์แนบ | `pickFiles()` · `gateFiles()` | A10 `POST /attachments` |
| ส่งออก | `exportCSV()` | A11 `GET /export.csv` |
| สายอนุมัติ | `resolveDoa()` · `resolveRole()` | DOA กลาง (F-DLG-001) |
| ช่องลงชื่อบนแบบพิมพ์ | `tplSignRows()` | ผลต้องเท่ากับ `sign_rows.py` ฝั่ง server |

## §11 Traceability + Drift Log
| มติ | เห็นที่ไหนในต้นแบบ |
|---|---|
| DEC-01 · DEC-02 | `confirmApprove()` ปิดงานที่สถานะเอกสารอย่างเดียว ไม่แตะข้อมูลระบบอื่น |
| DEC-03 | `MOCK_DOA_RESOLVED` 1 ขั้น + modal ส่ง 1 ช่องต่อขั้น + `resolveDoa()` |
| DEC-04 | เนื้อสัญญาอ่านค่าร้อยละจาก `POLICY` และชื่อบริษัทจาก `DOC` แล้วส่งเข้า data ของแบบพิมพ์ ไม่ฝังใน template |
| DEC-05 | ปุ่ม "เพิ่มรายการกล่อง" ไม่จำกัด · แบบพิมพ์เติมอย่างน้อย 1 แถว (`PDF_MIN_ROWS`) |
| DEC-06 | ช่องในขั้น 1 ตรงกระดาษ · เนื้อสัญญาแสดงเป็นข้อความคงที่ แก้รายฉบับไม่ได้ |
| DEC-07 | `tplSignRows()` ผู้รับมอบ + 1 ช่องต่อขั้น · ไม่มีภาพลายมือชื่อ |
| DEC-08 | `confirmReason()` kind=reject → `status='draft'` + บันทึก `returned` ด้วยเลขเดิม |
| DEC-09 | `canSee()` · `canAct()` · `isAdmin()` |
| DEC-10 | `DOC.prefix = 'LOA'` · ออกเลขใน `persist()` |
| DEC-11 | เมนู ⋮ มีแค่ แก้ไข · พิมพ์ · ยกเลิกเอกสาร · มี `exportCSV()` · ไม่มีการประกาศเมื่อลงนามครบ |
| DEC-12 | `COPIES` 2 ชุดใช้ template เดียวกัน เลขข้อในเนื้อสัญญาเป็นข้อความคงที่ของ template |
**Drift:** ไม่มี — ต้นแบบตรงกับ FRD ทุกข้อ ณ รอบนี้

## §12 Diff จากเวอร์ชันก่อน
เวอร์ชันแรกของ feature นี้ — ไม่มี diff

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
1. เพิ่มรายงานจำนวนกล่องที่ปล่อยไปรายลูกค้า/รายเขต เพื่อดูมูลค่าทรัพย์สินที่อยู่นอกบริษัท
2. เพิ่มการติดตามการคืนกล่องเมื่อลูกค้าหยุดใช้ผลิตภัณฑ์ (เงื่อนไขข้อ 2 ของสัญญา) — รอบนี้ปิดตาม DEC-16
3. ให้แนบไฟล์สแกนฉบับที่ลงนามครบแล้วเป็นขั้นบังคับก่อนปิดเอกสาร (ตอนนี้เป็นทางเลือก)

## §1.1 Design Tokens AS-BUILT (ครบทุกตัวใน `:root`)

| token | ค่า |
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

## §6.1 Z-Index Registry AS-BUILT (ทุกค่าที่ประกาศในไฟล์)

| selector | z-index |
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

## §6.2 Overlay / Layer classes AS-BUILT

`drawer` · `drawer-avatar` · `drawer-backdrop` · `drawer-body` · `drawer-fields` · `drawer-footer` · `drawer-footer-meta` · `drawer-header` · `drawer-header-actions` · `drawer-header-divider` · `drawer-panel` · `drawer-section` · `drawer-section-title` · `drawer-stepper-band` · `drawer-subtitle` · `drawer-tab` · `drawer-tabs` · `drawer-title` · `menu-fixed` · `modal` · `modal-backdrop` · `modal-body` · `modal-footer` · `modal-header` · `modal-header-icon` · `modal-subtitle` · `modal-title` · `row-menu` · `toast` · `user-menu` · `user-menu-cap` · `user-menu-divider` · `user-menu-item`

## §9.2 Toast (ข้อความคงที่ — verbatim)

| ข้อความ | variant |
|---|---|
| ไม่มีการแจ้งเตือนใหม่ | info |
| แบบเอกสารนี้ยังไม่เปิดใช้งาน | warning |
| แก้ไขได้เฉพาะร่างของตัวเอง | warning |
| กรุณากรอกข้อมูลให้ครบถ้วน | warning |
| กรุณากรอกข้อมูลให้ครบถ้วน | warning |
| บันทึกร่างแล้ว · | info |
| กรุณากรอกข้อมูลให้ครบถ้วน | warning |
| ส่งให้ลงนามแล้ว · | info |
| ส่งออก | info |
| สลับเป็น | info |
| แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง | error |

## §9.3 Placeholder (verbatim)

- ค้นหาเลขที่ / ลูกค้า / รายละเอียดกล่อง
- ชนิด ขนาด และจำนวนกล่อง — เช่น กล่องบรรจุกระดาษ ขนาด 40 x 30 x 30 ซม. จำนวน 50 ใบ
- ชื่อผู้ลงนามฝ่ายลูกค้า
- ที่อยู่ที่จะนำกล่องไปตั้ง
- ไม่บังคับ
- ไม่บังคับ — เว้นว่างได้

## §9.8 Microcopy ภาษาไทยทั้งหมดในไฟล์ (verbatim · รวมข้อมูลตัวอย่างที่สมมติขึ้น)

- (ขั้น
- 12/3 ถนนสมมติ แขวงตัวอย่าง เขตทดสอบ กรุงเทพมหานคร 10100
- 456 หมู่ 1 ถนนทดสอบ ตำบลสมมติ อำเภอสมมติ จังหวัดสมมติ 20000
- 7/7 ถนนทดสอบ ตำบลตัวอย่าง อำเภอสมมติ จังหวัดทดสอบ 30000
- 888 อาคารตัวอย่าง ถนนสมมติ แขวงทดสอบ เขตสมมติ กรุงเทพมหานคร 10200
- 99/9 หมู่ 5 ถนนตัวอย่าง ตำบลสมมติ อำเภอเมือง จังหวัดสมมติ 10000
- [Lucide] All CDNs failed. Icons จะไม่แสดง but UI ยังใช้งานได้
- ]); if (canCancel(r)) items.push(['x-circle', 'ยกเลิกเอกสาร',
- ]]; if (isOwner(r) && r.status === 'draft') items.unshift(['pencil', 'แก้ไข',
- showToast('ไม่มีการแจ้งเตือนใหม่','info')
- · กลับเป็นร่างเลขเดิม
- · ลงนามแล้ว ล็อกแก้ไข
- · ลงนามแล้ว — ยกเลิกแล้วใช้ต่อไม่ได้
- ก.ค.
- ก.พ.
- ก.ย.
- กธ
- กรกฎาคม
- กรุณากรอกข้อมูลให้ครบถ้วน
- กล่องบรรจุกระดาษ ขนาด 40 x 30 x 30 ซม. จำนวน 120 ใบ
- กล่องบรรจุกระดาษ ขนาด 40 x 30 x 30 ซม. จำนวน 20 ใบ
- กล่องบรรจุกระดาษ ขนาด 40 x 30 x 30 ซม. จำนวน 25 ใบ
- กล่องบรรจุกระดาษ ขนาด 40 x 30 x 30 ซม. จำนวน 30 ใบ
- กล่องบรรจุกระดาษ ขนาด 40 x 30 x 30 ซม. จำนวน 300 ใบ (สาขาในเขตกรุงเทพมหานคร)
- กล่องบรรจุกระดาษ ขนาด 40 x 30 x 30 ซม. จำนวน 50 ใบ
- กล่องบรรจุกระดาษ ขนาด 40 x 30 x 30 ซม. จำนวน 500 ใบ (กระจาย 25 สาขา)
- กล่องบรรจุกระดาษ ขนาด 40 x 30 x 30 ซม. จำนวน 60 ใบ
- กล่องบรรจุกระดาษ ขนาด 40 x 30 x 30 ซม. จำนวน 80 ใบ
- กล่องบรรจุกระดาษ ขนาด 60 x 40 x 40 ซม. จำนวน 200 ใบ (ศูนย์กระจายสินค้า)
- กล่องบรรจุกระดาษ ขนาด 60 x 40 x 40 ซม. จำนวน 40 ใบ
- กันยายน
- กัลยา ธรรมรักษ์
- กำลังเปิดหน้าต่างพิมพ์ ·
- กุมภาพันธ์
- ขั้นทดสอบ
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลหนังสือสัญญา
- ข้าม
- คน
- คลิกเพื่อดูรายการ
- คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค่าเริ่มต้นจากสายอนุมัติและผังองค์กร
- ค้นหา...
- ค้นหาเลขที่ / ลูกค้า / รายละเอียดกล่อง
- งานตามปกติ
- ชนิด ขนาด และจำนวนกล่อง — เช่น กล่องบรรจุกระดาษ ขนาด 40 x 30 x 30 ซม. จำนวน 50 ใบ
- ชนิดไฟล์ไม่รองรับ
- ชื่อผู้รับมอบ
- ชื่อผู้ลงนามฝ่ายลูกค้า
- ชื่อฟังก์ชัน
- ชื่อลูกค้า
- ชูชาติ สมมติชัย
- ณบ
- ณัฐชา บุญมา
- ดาวน์โหลด PDF
- ต.ค.
- ตรวจสอบและยืนยัน
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตุลาคม
- ต้นฉบับ
- ต้อง
- ถึง
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ทำหนังสือสัญญายืมก่อนส่งมอบกล่องบรรจุกระดาษให้ลูกค้า
- ทำเอกสารซ้ำ
- ที่คุณเกี่ยวข้อง
- ที่อยู่ที่ตั้งกล่อง
- ที่อยู่ที่ตั้งกล่องไม่ตรงกับทะเบียนลูกค้า
- ทุกฝ่าย
- ทุกลูกค้า
- ทุกสถานะ
- ธ.ค.
- ธนพล ศรีวงศ์
- ธศ
- ธันวาคม
- บรรทัดนี้ยังว่าง — ใส่ข้อความหรือลบรายการนี้ออก
- บริษัท ครีเดนซ์ จำกัด (มหาชน)
- บริษัท ตัวอย่างกระจายสินค้า จำกัด
- บริษัท ตัวอย่างค้าปลีก จำกัด
- บริษัท ตัวอย่างซัพพลาย จำกัด
- บริษัท ตัวอย่างโมเดิร์นเทรด จำกัด (มหาชน)
- บันทึกผิดฉบับ
- บันทึกร่างแล้ว ·
- ปก
- ประวัติ
- ประวัติ (append-only)
- ปิด
- ปิยะนุช แก้วมณี
- ผู้จัดการจัดซื้อ
- ผู้จัดการฝ่ายจัดซื้อ
- ผู้จัดการร้าน
- ผู้จัดทำ
- ผู้รับมอบ
- ผู้รับมอบ (ฝ่ายลูกค้า)
- ผู้ส่ง
- ผู้ส่งมอบ (บริษัท ครีเดนซ์ จำกัด (มหาชน))
- ผู้ส่งมอบตามสายอนุมัติ
- ผู้อำนวยการฝ่ายจัดซื้อ
- พ.ค.
- พ.ย.
- พฤ
- พฤศจิกายน
- พฤษภาคม
- พิจารณาในระบบ
- พิมพ์
- ม.ค.
- มกราคม
- มานี ตัวอย่างงาม
- มิ.ย.
- มิถุนายน
- มี.ค.
- มีนาคม
- ยกเลิก
- ยกเลิกเอกสาร
- ยกเลิกเอกสารแล้ว ·
- ยังไม่มีข้อมูล
- ยังไม่มีหนังสือสัญญายืม
- ยังไม่ส่ง
- ยังไม่ใส่
- ยังไม่ได้ใส่รายละเอียดกล่อง
- ย้อนกลับ
- รหัสลูกค้า
- รอฉันพิจารณา
- รอผล
- รอผู้ส่งมอบพิจารณา
- รอพิจารณา
- รอลงนาม
- รายการ
- รายการกล่อง
- รายการที่
- รายชื่อสาขาและจำนวนกล่อง.xlsx
- รายละเอียด
- รายละเอียดกล่อง
- รายละเอียดกล่องไม่ครบ
- รายละเอียดกล่องไม่ครบ — ระบุขนาดและจำนวนต่อสาขา
- ร่าง
- ลงนาม
- ลงนามครบแล้ว พิมพ์ส่งคู่สัญญาได้
- ลงนามแล้ว
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ลายเซ็น
- ลำดับการลงนาม
- ลูกค้าผู้ยืม
- ลูกค้ายกเลิกการขอยืม
- ลูกค้ายกเลิกการขอยืม — เปลี่ยนไปใช้บรรจุภัณฑ์ของตนเอง
- ลูกค้ายังไม่ยืนยันจำนวน
- ล้างตัวกรอง
- วท
- วรวุฒิ ทองดี
- วันที่
- วันที่ ........./........./.........
- ศม
- ศศิธร มีสุข
- ส.ค.
- สถานะ
- สถานะเอกสาร
- สบ
- สมพร ตัวอย่างใจดี
- สมศักดิ์ บริหารดี
- สร้าง PDF
- สร้างหนังสือสัญญา
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างโดย
- สลับเป็น
- สำเนา
- สิงหาคม
- สิบ
- สุชาติ ทดสอบระบบ
- ส่งกลับแก้ไข — แก้แล้วส่งใหม่ด้วยเลขเดิม
- ส่งกลับแก้ไขแล้ว ·
- ส่งออก
- ส่งแล้วแก้ไขไม่ได้จนกว่าผู้ส่งมอบจะส่งกลับแก้ไข
- ส่งให้ผู้ส่งมอบลงนาม
- ส่งให้ผู้ส่งมอบลงนาม?
- ส่งให้ลงนาม
- ส่งให้ลงนามแล้ว ·
- หนังสือสัญญาทั้งหมด
- หนังสือสัญญายืม
- หนังสือสัญญายืมกล่องบรรจุกระดาษ
- ห้างหุ้นส่วนจำกัด ตัวอย่างการค้า
- อนุชา พรหมสุข
- อพ
- ออกให้ตอนบันทึก
- อา
- อารี ตัวอย่างเจริญ
- เจ้าของกิจการ
- เดือนถัดไป
- เด้งกลับบน
- เพิ่มเติม
- เม.ย.
- เมษายน
- เลขที่
- เลขที่บนแบบพิมพ์
- เลขที่เอกสาร
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกประเทศ
- เลือกผู้พิจารณา
- เลือกลูกค้าจากทะเบียน
- เลือกลูกค้าผู้ยืม ใส่ที่อยู่ที่ตั้งกล่อง แล้วใส่รายละเอียดกล่องที่สนับสนุน
- เลือกวันที่
- เหตุผลที่ยกเลิก
- เอกสารแนบ
- แก้ไข
- แก้ไขร่าง
- แก้ไขล่าสุด
- แก้ไขหนังสือสัญญา
- แก้ไขเอกสาร
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งผู้จัดทำว่าต้องแก้อะไร
- แตกหักโดยมิใช่การใช้
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- แล้ว ·
- ใส่ชนิด ขนาด และจำนวนกล่อง
- ไม่บังคับ
- ไม่บังคับ — เว้นว่างได้
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่มีรายการค้าง
- ไม่ยกเลิก
- ไม่ลงนาม
- — คุณเป็นผู้พิจารณาเอกสารนี้
- — ส่งกลับแก้ไข
- — ไม่ได้ระบุ —

## §10.1 ฟังก์ชันหลักในไฟล์ (anchor สำหรับ test case)

`LN()` · `ME()` · `SEC()` · `STEPH()` · `actualRender()` · `addLine()` · `applyRoute()` · `bdById()` · `bdClose()` · `bdFmt()` · `bdIso()` · `bdNav()` · `bdOpenFor()` · `bdPick()` · `bdPlace()` · `bdRender()` · `bdToday()` · `bdToggle()` · `bedateHTML()` · `blankForm()` · `blankLine()` · `bootIfReady()` · `box()` · `boxCard()` · `boxCount()` · `busyLabel()` · `canAct()` · `canCancel()` · `canSee()` · `clearFieldError()` · `closeDrawer()` · `closeModal()` · `closeOverlay()` · `closeRowMenu()` · `commitRejected()` · `confirmApprove()` · `confirmReason()` · `confirmSubmit()` · `curStep()` · `custName()` · `custOf()` · `dirty()` · `docPill()` · `empChip()` · `empOf()` · `emptyStateHTML()` · `esc()` · `exportCSV()` · `fileRow()` · `filledLines()` · `findR()` · `fitPdf()` · `fmtDate()` · `fmtDateTime()` · `fmtMoney()` · `fmtNumber()` · `fmtSize()` · `gateFiles()` · `genPdf()` · `getRoute()` · `go()` · `goPage()` · `goStep()` · `initSearchSelect()` · `initSelects()` · `isAdmin()` · `isOwner()` · `kv()` · `lineErr()` · `linesTable()` · `listRows()` · `loaPdfBody()` · `loaPdfData()` · `loaPdfDoc()` · `loadLucide()` · `mark()` · `mkRec()` · `modalBackdropClick()` · `modalShell()` · `navigate()` · `nowIso()` · `onQ()` · `openApprove()` · `openCancel()` · `openDrawer()` · `openModal()` · `openModalCfg()` · `openOverlay()` · `openReject()` · `openRowMenu()` · `openSubmit()` · `openView()` · `pager()` · `persist()` · `pickFiles()` · `pill()` · `portalMenu()` · `positionMenu()` · `preserveRenderState()` · `preservedRender()` · `presetChips()` · `pushAudit()` · `removeFile()` · `removeLine()` · `render()` · `renderDetailTab()` · `renderHistoryTab()` · `renderIcons()` · `renderModal()` · `renderPage()` · `renderPdfTab()` · `renderSignProgress()` · `renderSignTab()` · `renderViewDrawer()` · `renderWizard()` · `reposition()` · `resetFilters()` · `resolveDoa()` · `resolveRole()` · `restoreRenderState()` · `rowClick()` · `saveAndSubmit()` · `saveDraft()` · `searchSelectHTML()` · `setCopy()` · `setCust()` · `setDocDate()` · `setF()` · `setF2()` · `setLine()` · `setReasonPreset()` · `setStat()` · `setTab()` · `showDrawer()` · `showToast()` · `signN()` · `sortBy()` · `sortTh()` · `ssClear()` · `ssEscapeReg()` · `ssFiltered()` · `ssGet()` · `ssOnInput()` · `ssOnKey()` · `ssOpen()` · `ssPick()` · `ssPortal()` · `ssPurgePortals()` · `ssRenderList()` · `ssSetText()` · `ssSyncChrome()` · `stText()` · `startWizard()` · `statCard()` · `stepper()` · `sumCard()` · `switchPersona()` · `tShort()` · `tabBtn()` · `termsBlock()` · `thFull()` · `toggleModule()` · `toggleSidebar()` · `toggleUserMenu()` · `tplGet()` · `tplRender()` · `tplSignRows()` · `tryNext()` · `updateShell()` · `validateField()` · `validateMain()` · `viewBanner()` · `wf()` · `withRenderPreservation()` · `wizAttach()` · `wizBack()` · `wizMain()` · `wizNext()` · `wizReview()` · `wordsFor()`

## §11.1 Marker ที่ต้อง wire ตอนพัฒนาจริง

| marker | บริบท |
|---|---|
| `ENG-DOC-NUM` | /* doc_type ประกาศผ่าน doccfg-declaration / mdoc-declaration · เลขรันจาก ENG-DOC-NUM (F-DOCCFG) |
| `DOA-ENGINE-HOOK` | /* DOA-ENGINE-HOOK — resolve จาก DOA entry ของ feature นี้ ณ เวลาส่ง แล้ว snapshot ลง approval_chain (ดู DOA_BRIEF_F-TMP |
| `ENG-DOC-NUM` | /* บันทึก = ENG-DOC-NUM.next() ออกเลขที่ (ครั้งแรก · DEC-10) · ค่านโยบายและข้อมูลลูกค้า snapshot ลงเอกสาร */ |
| `ENG-NOTIFY` | /* ENG-NOTIFY (ntf-declaration): loa_cancelled · loa_signed_copy_attached — DOA engine เป็นเจ้าของ doa_pending/doa_resul |
| `DOA-ENGINE-HOOK` | doa: MOCK_DOA_RESOLVED 1 ขั้น (role-mgr-sales = ผู้ส่งมอบ) dynamic — resolveDoa() = DOA-ENGINE-HOOK · คำตัดสินผูก role ( |
| `ENG-DOC-NUM` | hooks: ENG-DOC-NUM.next() ตอนบันทึกครั้งแรก (DEC-10 · รหัส LOA) · F-DOCCFG status ก่อนออกเลข (DOC.active) · ENG-NOTIFY l |
| `ENG-NOTIFY` | hooks: ENG-DOC-NUM.next() ตอนบันทึกครั้งแรก (DEC-10 · รหัส LOA) · F-DOCCFG status ก่อนออกเลข (DOC.active) · ENG-NOTIFY l |

## §11.2 QA hook

`window.__QA__` archetype = `Q-form` · qa_hook = True

