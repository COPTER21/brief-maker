# UI BRIEF (AS-BUILT) — F-TMP-007 ใบเดินทางและสถานที่ปฎิบัติงาน  สำหรับ General Trade

## §0 Document Control + Pairing
| หัวข้อ | ค่า |
|---|---|
| Feature | F-TMP-007 · REQ-TMP-007 (รหัสชั่วคราว) |
| ไฟล์ต้นแบบ | `feature.html` (html-generator-v9.2 · archetype **Q-form**) |
| คู่เอกสาร | `BRD_F-TMP-007.md` · `FRD_F-TMP-007_Pack/` · `DECISIONS.lock.md` · `print/TWP_print-spec.md` |
| ใบประกาศ | `DOCCFG_BRIEF_F-TMP-007.md` · `DOA_BRIEF_F-TMP-007.md` · `NTF_BRIEF_F-TMP-007.md` · `MDOC_BRIEF_TWP.md` |
| สถานะ | AS-BUILT จากต้นแบบ · audit FAIL 0 · **[NO-BROWSER] ยังไม่ได้รัน e2e / render-check** |
| วันที่ | 2026-10-07 |

## §2 Route Map
| route | หน้าจอ | refresh-safe |
|---|---|---|
| `#/travel-workplace-sheet` | ทะเบียนใบเดินทางและสถานที่ปฏิบัติงาน | ✓ |
| `#/travel-workplace-sheet/create` | drawer สร้างใบใหม่ (3 ขั้น) | ✓ |
| `#/travel-workplace-sheet/edit/:id` | drawer แก้ไขร่าง | ✓ |
| `#/travel-workplace-sheet/view` | ฐานของ route ดูรายละเอียด | ✓ |
| `#/travel-workplace-sheet/view/:id` | drawer ดูรายละเอียด (4 แท็บ) | ✓ |
`applyRoute()` อ่าน hash แล้วเปิด drawer ให้ตรง · `go()` เขียน hash กลับทุกครั้งที่เปลี่ยนหน้าจอ

## §3 Layout Shell
- Sidebar 232px (`--sidebar-w`) · module `Sales` › feature `ใบเดินทางและสถานที่ปฏิบัติงาน` + badge นับใบที่รอฉันพิจารณา
- Shell bar 52px (`--shell-h`) · breadcrumb `Core › Sales › ใบเดินทางและสถานที่ปฏิบัติงาน` · ปุ่มแจ้งเตือน · user chip + เมนูสลับ persona
- `#overlay-root` และ `#toast` ก่อน `</body>` (Rule #95 portal)

## §4 Page Anatomy
### 4.1 ทะเบียน (`#/travel-workplace-sheet`)
`.page-fill` → `.ph` (หัวข้อ + chip นับ + ปุ่ม ส่งออก CSV / สร้างใบเดินทาง) → `.stats` 3 ใบ → `.card.list-card` (filter-bar → `.table-wrap` → `.table-foot`)
คอลัมน์: เลขที่ · วันที่ขอ · ผู้จัดทำ · รอบการขายที่ · ช่วงวันทำงาน · สถานะเอกสาร · ลายเซ็น · รวมค่าใช้จ่ายทั้งสิ้น (บาท) · คงเหลือ (บาท) · ⋮
เมนู ⋮: แก้ไข (ร่างของตัวเอง) · พิมพ์ · ยกเลิกเอกสาร — **ไม่มีทำซ้ำ** (DEC-12)

### 4.2 drawer สร้าง/แก้ไข (`.drawer.drawer-panel.wide`)
`.dw-head` (eyebrow + title + `.d-stepper` 3 ขั้น) → `.drawer-body.is-soft` → `.dw-footer`
- ขั้น 1 `.wz-split` = `.wz-main` (การ์ด ① หัวเอกสาร · การ์ด ② ตารางวันทำงาน `.twp-tbl` 21 คอลัมน์ + แถวรวมยอด · การ์ด ③ สรุปค่าใช้จ่ายท้ายใบ) + `.wz-sum` (การ์ดสรุปสด sticky)
- ขั้น 2 การ์ด ① รายการเอกสารที่แนบ 3 บรรทัด + การ์ด ② `.upload-zone` + `.file-row`
- ขั้น 3 `.review-card` 5 ใบ (ข้อมูลใบเดินทาง · วันทำงาน · สรุปค่าใช้จ่าย · เอกสารที่แนบ · ไฟล์แนบ)

### 4.3 drawer ดูรายละเอียด (`.drawer.drawer-panel`)
`.dw-head` (doc-ident + pill สถานะ + ป้าย "ส่งกลับแก้ไข") → `.drawer-tabs` 4 แท็บ → `.drawer-body` → `.dw-footer`
แท็บ: รายละเอียด · PDF Preview (`.pdf-slot > iframe.pdf-frame`) · ลายเซ็น / อนุมัติ (`.timeline`) · ประวัติ

## §5 Component Inventory
| component | class หลัก | ใช้ที่ |
|---|---|---|
| การ์ดสถิติ | `.stat` `.stat-label` `.stat-value` `.stat-meta` | ทะเบียน |
| ตารางข้อมูล | `.table` `.table-wrap` `.table-foot` | ทะเบียน · วันทำงาน |
| ตารางกรอกวันทำงาน | `.twp-tbl` `.twp-ed` `.in-num` `.in-txt` `.twp-total` | ขั้น 1 |
| การ์ดสรุปสด | `.wz-sum` `.wz-sum-row` `.wz-sum-total` | ขั้น 1 |
| การ์ดสรุปค่าใช้จ่าย | `.twp-sum` `.pd-cell` `.pd-l` `.pd-v` | รายละเอียด · ขั้น 3 |
| search select | `.ss-list` `.menu-fixed` | ตัวกรอง · รอบการขายที่ · เลือกผู้พิจารณา |
| ตัวเลือกวัน พ.ศ. | `.bedate` `.bd-pop` `.bd-grid` `.bd-day` | ทุกช่องวันที่ (Rule #114) |
| stepper | `.d-stepper` `.stepper-item` `.stepper-circle` | drawer สร้าง/แก้ไข |
| timeline | `.timeline` `.tl-item` `.tl-dot` `.tl-acts` | ลายเซ็น · ประวัติ |
| pill สถานะ | `.pill` `.pill-muted/-warning/-success/-danger` | ทะเบียน · drawer |
| ความคืบหน้าลายเซ็น | `.sign-prog` `.sp-bar` `.sp-fill` | ทะเบียน · แท็บลายเซ็น |
| row menu | `.row-menu` `.rm-item` | ทะเบียน (portal) |
| modal | `.modal` `.modal-header` `.modal-body` `.modal-footer` `.slot-row` | ส่ง/อนุมัติ/ไม่อนุมัติ/ยกเลิก/ทิ้งข้อมูล |

## §7 Interaction Spec
- พิมพ์ในตารางวันทำงาน → อัปเดตช่อง "รวมค่าใช้จ่ายที่เบิก" ของแถวนั้น แถวรวมยอด และการ์ดสรุปแบบ **soft** (`softSum()`) ไม่ rebuild ทั้งหน้า focus ไม่หลุด
- เลือกวันที่ → `bedateHTML()` เปิด `.bd-pop` ใน `#overlay-root` · ระบบเติมช่อง "วันทำงาน" (ชื่อวัน) ให้อัตโนมัติถ้ายังไม่ได้พิมพ์เอง · Esc ปิดเฉพาะปฏิทิน ไม่ทะลุไปปิด drawer
- กรอกค่าโทรศัพท์หรือเงินสำรอง → การ์ดสรุปอัปเดต "รวมค่าใช้จ่ายทั้งสิ้น" และ "คงเหลือ" ทันที
- ปิด drawer ขณะแก้ไขค้าง → modal `ทิ้งข้อมูลที่กรอกไว้?`
- ปุ่มบันทึก/ส่ง ระหว่างทำงาน = disabled + loader + `กำลังบันทึก…` (กัน double-submit)
- คลิกนอก row menu / user menu → ปิดอัตโนมัติ · scroll → ปิด row menu
- `S.sim` = จำลองผลตอบกลับ API (`stale` · `denied` · `error` · `upload_fail`)

## §8 State-Driven UI Matrix
| สถานะ · ผู้ใช้ | ปุ่มหัว drawer | เมนู ⋮ | แก้ไขได้ |
|---|---|---|---|
| ร่าง · เจ้าของ | ยกเลิก · แก้ไข · ส่งอนุมัติ | แก้ไข · พิมพ์ · ยกเลิกเอกสาร | ✓ |
| ร่าง (ส่งกลับแก้ไข) · เจ้าของ | เหมือนร่าง + แบนเนอร์เหตุผล | เหมือนร่าง | ✓ |
| รออนุมัติ · ผู้พิจารณาขั้นปัจจุบัน | ไม่อนุมัติ · อนุมัติ | พิมพ์ · ยกเลิกเอกสาร (ถ้ามีสิทธิ์) | ✗ |
| รออนุมัติ · เจ้าของ | ยกเลิกเอกสาร | พิมพ์ · ยกเลิกเอกสาร | ✗ |
| อนุมัติแล้ว | — (ล็อกแก้ไข) | พิมพ์ | ✗ |
| ยกเลิก | — | พิมพ์ | ✗ |

## §9.1 ปุ่ม (verbatim)
สร้างใบเดินทาง · ส่งออก CSV · ล้างตัวกรอง · เพิ่มวันทำงาน · เพิ่มบรรทัด · ย้อนกลับ · ถัดไป · ยกเลิก · บันทึกแบบร่าง · บันทึกและส่งอนุมัติ · แก้ไข · ส่งอนุมัติ · อนุมัติ · ไม่อนุมัติ · ยกเลิกเอกสาร · พิมพ์ · ดาวน์โหลด PDF · ปิด · กลับไปกรอกต่อ · ทิ้งข้อมูล · วันนี้

## §9.4 ป้ายช่องและหัวข้อ (คัดตรงจากกระดาษ — ห้ามเกลา)
เรียน : · จาก  : · Date : · โทรศัพท์ : · รอบการขายที่ : · รอบวันทำงาน · วันทำงาน · วันที่ · ใบเดินทาง/ตลาดที่ปฏิบัติงาน · เริ่มต้น · สิ้นสุด · สถานที่พัก · ค่าใช้จ่ายที่พัก · ที่พัก · ค่าโรงแรม · ค่าใช้จ่ายในการทำงาน · เบี้ยเลี้ยง · ซักรีด · ธรรมเนียม · ไปรษณีย์ · จอดรถ · อื่นๆ · รวมค่าใช้จ่าย · ที่เบิก · หมายเหตุ · บิลน้ำมัน · เลขไมล์ · ลิตร · บาท · รวมค่าใช้จ่ายในการเดินทาง · ค่าโทรศัพท์ · รวมค่าใช้จ่ายทั้งสิ้นเป็นเงิน · เบิกเงินสำรองของบริษัทฯ · คงเหลือ (เบิกเพิ่มบริษัทฯ) · สำเนา  : · เอกสารที่แนบ · ผู้จัดทำ · ผู้อนุมัติ
> คำสะกด "ปฎิบัติงาน" ในหัวเรื่องของแบบพิมพ์คงตามกระดาษตามมติ DEC-17

## §9.5 ข้อความสถานะ / ว่าง / เตือน (verbatim)
- สถานะเอกสาร: ร่าง · รออนุมัติ · อนุมัติแล้ว · ยกเลิก · ส่งกลับแก้ไข
- สถานะขั้นอนุมัติ: ยังไม่ถึงขั้นนี้ · รอพิจารณา · อนุมัติ · ไม่อนุมัติ · ข้าม
- ว่าง: ยังไม่มีใบเดินทาง · ไม่พบรายการที่ค้นหา · ไม่มีไฟล์แนบ · ไม่มีรายการ
- เตือน: กรุณากรอกข้อมูลให้ครบถ้วน · ใส่วันทำงานอย่างน้อย 1 บรรทัด · วันที่ซ้ำกับแถวที่ N · ตัวเลขต้องไม่ติดลบ · กรอกข้อมูลไว้แล้วแต่ยังไม่ได้เลือกวันที่

## §10 Data Binding & BACKEND anchors
| หน้าจอ | ฟังก์ชัน | endpoint จริง (02_API) |
|---|---|---|
| ทะเบียน | `listRows()` · `renderPage()` | A1 `GET /sales/travel-workplace-sheets` |
| เปิดดู | `openView()` · `renderViewDrawer()` | A2 `GET /sales/travel-workplace-sheets/{id}` |
| บันทึกร่าง | `persist()` · `saveDraft()` | A3 `POST` · A4 `PUT` |
| ส่งอนุมัติ | `openSubmit()` · `confirmSubmit()` | A5 `POST /submit` |
| อนุมัติ | `confirmApprove()` | A6 `POST /approve` |
| ไม่อนุมัติ / ยกเลิก | `confirmReason()` | A7 `POST /reject` · A8 `POST /cancel` |
| แบบพิมพ์ | `docPrintData()` · `tplRender()` · `genPdf()` | A9 `GET /pdf` |
| ส่งออก | `exportCSV()` | A10 `GET /export.csv` |
| สายอนุมัติ | `resolveDoa()` · `resolveRole()` | DOA กลาง (F-DLG-001) |
| ยอดรวม | `totalsOf()` · `lineTotal()` · `grandOf()` · `balanceOf()` | คำนวณที่ server ด้วยสูตรเดียวกัน |

## §11 Traceability + Drift Log
| มติ | เห็นที่ไหนในต้นแบบ |
|---|---|
| DEC-03 | `MOCK_DOA_RESOLVED` 1 ขั้น + modal ส่ง 1 ช่องต่อขั้น |
| DEC-04 · DEC-13 · DEC-14 | แถว `รวมค่าใช้จ่ายในการเดินทาง` และช่อง `รวมค่าใช้จ่ายที่เบิก` อ่านอย่างเดียว + `totalsOf()` / `lineTotal()` / `grandOf()` / `balanceOf()` |
| DEC-05 | ปุ่ม "เพิ่มวันทำงาน" ไม่จำกัด · แบบพิมพ์เติมครบ 27 แถว (`PDF_MIN_ROWS`) |
| DEC-06 | ปุ่ม "เพิ่มบรรทัด" ในเอกสารที่แนบ · แบบพิมพ์เติมครบ 3 บรรทัด (`PDF_MIN_ATT`) |
| DEC-07 | ช่องในขั้น 1 ตรงกระดาษ ไม่มีช่องที่กระดาษไม่มี |
| DEC-08 · DEC-16 | `tplSignRows()` ผู้จัดทำ + 1 ช่องต่อขั้น · ไม่มีภาพลายมือชื่อ |
| DEC-09 | `confirmReason()` kind=reject → `status='draft'` + `returned=true` เลขเดิม |
| DEC-10 | `canSee()` · `canAct()` · `isAdmin()` |
| DEC-11 | `DOC.prefix = 'TWP'` · ออกเลขใน `persist()` |
| DEC-12 | ไม่มีฟังก์ชันทำซ้ำเอกสารในไฟล์ (เมนู ⋮ มีแค่ แก้ไข · พิมพ์ · ยกเลิกเอกสาร) · มี `exportCSV()` |
| DEC-15 | `dayNameOf()` เติมชื่อวันอัตโนมัติ · คอลัมน์ `route_mid` และเลขไมล์ 2 ช่องมีป้ายกำกับในหน้าจอ |
**Drift:** ไม่มี — ต้นแบบตรงกับ FRD ทุกข้อ ณ รอบนี้

## §12 Diff จากเวอร์ชันก่อน
เวอร์ชันแรกของ feature นี้ — ไม่มี diff

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
1. เพิ่มการนำเข้าแถววันทำงานจาก Excel/CSV (ลดการพิมพ์ 27 แถว)
2. เติมค่าเบี้ยเลี้ยง/ค่าที่พักอัตโนมัติจากตารางอัตราของบริษัท แล้วเตือนเมื่อเกินอัตรา
3. ถ้าลูกค้าต้องการ "ทำซ้ำใบของรอบก่อน" ให้เปิดเป็น enhancement (รอบนี้ปิดตาม DEC-12)

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
| บันทึกร่างแล้ว · | info |
| กรุณากรอกข้อมูลให้ครบถ้วน | warning |
| ส่งอนุมัติแล้ว · | info |
| ส่งออก | info |
| สลับเป็น | info |
| แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง | error |

## §9.3 Placeholder (verbatim)

- ค้นหาเลขที่ / ผู้จัดทำ / รอบการขายที่ / เรียน
- ชื่อเอกสารที่แนบ
- บรรทัดต่อ (ถ้ามี)
- ผู้รับสำเนา (ถ้ามี)
- ผู้รับเอกสาร เช่น ผู้จัดการฝ่ายขาย สำนักงานใหญ่
- หมายเหตุท้ายใบ (ถ้ามี)
- ไม่บังคับ

## §9.8 Microcopy ภาษาไทยทั้งหมดในไฟล์ (verbatim · รวมข้อมูลตัวอย่างที่สมมติขึ้น)

- (ขั้น
- [Lucide] All CDNs failed. Icons จะไม่แสดง but UI ยังใช้งานได้
- ]); if (canCancel(r)) items.push(['x-circle', 'ยกเลิกเอกสาร',
- ]]; if (isOwner(r) && r.status === 'draft') items.unshift(['pencil', 'แก้ไข',
- showToast('ไม่มีการแจ้งเตือนใหม่','info')
- · อนุมัติแล้ว ล็อกแก้ไข
- ก.ค.
- ก.พ.
- ก.ย.
- กข
- กนกวรรณ ขายดี
- กรกฎาคม
- กรอกข้อมูลไว้แล้วแต่ยังไม่ได้เลือกวันที่
- กรุณากรอกข้อมูลให้ครบถ้วน
- กันยายน
- กำลังเปิดหน้าต่างพิมพ์ ·
- กุมภาพันธ์
- ขั้นทดสอบ
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลระบบ
- ข้อมูลหลักใบเดินทาง
- ข้อมูลเอกสาร
- ข้าม
- คงเหลือ
- คงเหลือ (เบิกเพิ่มบริษัทฯ)
- คน
- คลิกเพื่อดูรายการ
- คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค่าเริ่มต้นจากสายอนุมัติ (DOA) และผังองค์กร
- ค่าโทรศัพท์
- ค่าโรงแรม
- ค่าใช้จ่ายที่พัก
- ค่าใช้จ่ายในการทำงาน
- ค้นหา...
- ค้นหาเลขที่ / ผู้จัดทำ / รอบการขายที่ / เรียน
- จอดรถ
- จันทร์
- จาก
- จาก (ผู้จัดทำ)
- ชนิดไฟล์ไม่รองรับ
- ชื่อฟังก์ชัน
- ซักรีด
- ดาวน์โหลด PDF
- ต.ค.
- ตรวจสอบและยืนยัน
- ตลาดกลางเขต A
- ตลาดกลางเขต E
- ตลาดชุมชน B
- ตลาดนัดเขต D
- ตลาดสดเขต C
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตัวเลขต้องไม่ติดลบ
- ตำแหน่ง
- ตุลาคม
- ต้อง
- ถึง
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ที่คุณเกี่ยวข้อง
- ที่พัก
- ที่พักสหกรณ์
- ทุกฝ่าย
- ทุกรอบการขาย
- ทุกสถานะ
- ธ.ค.
- ธนากร บริหารขาย
- ธบ
- ธรรมเนียม
- ธันวาคม
- บรรทัดต่อ (ถ้ามี)
- บริษัท ตัวอย่าง จำกัด (มหาชน)
- บอกผู้จัดทำว่าต้องแก้อะไร
- บันทึกผิดใบ
- บันทึกร่างแล้ว ·
- บาท
- บิลน้ำมัน
- บิลน้ำมัน (บาท)
- บิลน้ำมัน (ลิตร)
- บ้านพักเครือข่าย
- ปด
- ประวัติ
- ประวัติ (append-only)
- ปรีชา เดินตลาด
- ปิด
- ผู้จัดการฝ่ายการเงิน
- ผู้จัดการฝ่ายขาย
- ผู้จัดการฝ่ายขาย สำนักงานใหญ่
- ผู้จัดทำ
- ผู้รับสำเนา (ถ้ามี)
- ผู้รับเอกสาร เช่น ผู้จัดการฝ่ายขาย สำนักงานใหญ่
- ผู้ส่ง
- ผู้อนุมัติ
- ฝ่าย
- ฝ่ายการเงิน
- ฝ่ายขาย
- ฝ่ายบัญชี
- ฝ่ายบัญชีและการเงิน
- พ.ค.
- พ.ย.
- พนักงานขายเขต
- พฤ
- พฤศจิกายน
- พฤษภาคม
- พฤหัสบดี
- พิจารณาในระบบ
- พิมพ์
- พุธ
- ม.ค.
- มกราคม
- มง
- มานพ การเงินมั่น
- มิ.ย.
- มิถุนายน
- มี.ค.
- มีนาคม
- ยกเลิก
- ยกเลิกรอบการขายนี้
- ยกเลิกรอบการขายนี้ — ปรับแผนเขตใหม่
- ยกเลิกเอกสาร
- ยกเลิกเอกสาร?
- ยกเลิกเอกสารแล้ว ·
- ยอดค่าใช้จ่ายไม่สอดคล้องกับวันทำงาน
- ยังเป็นร่าง — ส่งอนุมัติเมื่อข้อมูลครบ
- ยังไม่ถึงขั้นนี้
- ยังไม่มีข้อมูล
- ยังไม่มีใบเดินทาง
- ยังไม่ระบุผู้พิจารณา
- ยังไม่ส่ง
- ยังไม่ได้เลือกรอบ
- ย้อนกลับ
- รวม
- รวม บิลน้ำมัน บาท
- รวม บิลน้ำมัน ลิตร
- รวมค่าใช้จ่าย
- รวมค่าใช้จ่ายทั้งสิ้น
- รวมค่าใช้จ่ายทั้งสิ้น (บาท)
- รวมค่าใช้จ่ายทั้งสิ้นเป็นเงิน
- รวมค่าใช้จ่ายในการเดินทาง
- รอฉันพิจารณา
- รอบ
- รอบการขายที่
- รอผล
- รอผู้อนุมัติพิจารณา
- รอพิจารณา
- รออนุมัติ
- ระบุผู้รับและรอบการขาย แล้วใส่วันทำงานทีละบรรทัดเหมือนกระดาษเดิม — ยอดรวมระบบคำนวณให้
- รายการ
- รายละเอียด
- ร่าง
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ลายเซ็น / อนุมัติ
- ลำดับการอนุมัติ
- ลิตร
- ล้างตัวกรอง
- วด
- วัน
- วันทำงาน
- วันทำงาน (ชื่อวัน)
- วันที่ ........./........./.........
- วันที่ขอ
- วิไล ดูแลทีม
- ศุกร์
- ส.ค.
- สข
- สค
- สถานที่พัก
- สถานะ
- สมชาย ขยันขาย
- สร้าง PDF
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างใบเดินทาง
- สร้างใบเดินทางและสถานที่ปฏิบัติงาน
- สร้างใบเดินทางและสถานที่ปฏิบัติงานของรอบการขาย เพื่อบันทึกวันทำงานและขอเบิกค่าใช้จ่าย
- สลับเป็น
- สิงหาคม
- สุรชัย คุมเขต
- ส่งกลับแก้ไข
- ส่งกลับแก้ไข — กลับเป็นร่างเลขที่เดิม
- ส่งกลับให้แก้ไขแล้ว ·
- ส่งอนุมัติ
- ส่งอนุมัติแล้ว ·
- ส่งออก
- ส่งแล้วแก้ไขไม่ได้จนกว่าผู้อนุมัติจะส่งกลับแก้ไข
- ส่งในระบบ
- หมายเหตุ
- หมายเหตุ / สำเนา
- หมายเหตุท้ายใบ (ถ้ามี)
- หัวหน้าหน่วยขาย
- อต
- อนุมัติ
- อนุมัติ (ขั้น
- อนุมัติแล้ว
- อนุมัติใบเดินทางครบทุกขั้น
- อังคาร
- อา
- อาทิตย์
- อารีย์ ตรวจสอบ
- อื่นๆ
- เจ้าหน้าที่การเงิน
- เดินทางตามแผนรอบการขาย
- เดือนถัดไป
- เด้งกลับบน
- เบิกเงินสำรองของบริษัทฯ
- เบี้ยเลี้ยง
- เปลี่ยนผู้เดินทาง
- เพิ่มเติม
- เม.ย.
- เมษายน
- เยี่ยมร้านค้าตามแผน
- เรียน
- เรียน (บรรทัดที่ 2)
- เลขที่
- เลขไมล์ (สิ้นสุด)
- เลขไมล์ (เริ่มต้น)
- เลขไมล์ไม่สัมพันธ์กับเส้นทาง
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกประเทศ
- เลือกผู้พิจารณา
- เลือกรอบการขาย
- เลือกวันที่
- เสาร์
- เหตุผลที่ยกเลิก
- เอกสารที่แนบ
- เอกสารที่แนบ (ตามกระดาษ 3 บรรทัด)
- แก้ไขร่าง
- แก้ไขเอกสาร
- แก้ไขใบเดินทาง
- แก้ไขได้เฉพาะร่างของตัวเอง
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- แล้ว ·
- โทรศัพท์
- โรงแรมตัวอย่าง 1
- โรงแรมตัวอย่าง 2
- ใบเดินทาง/ตลาดที่ปฏิบัติงาน ช่องกลาง
- ใบเดินทาง/ตลาดที่ปฏิบัติงาน สิ้นสุด
- ใบเดินทาง/ตลาดที่ปฏิบัติงาน เริ่มต้น
- ใบเดินทางทั้งหมด
- ใบเดินทางและสถานที่ปฎิบัติงาน สำหรับ General Trade
- ใบเสร็จค่าที่พัก
- ใบเสร็จค่าที่พักรวม.pdf
- ใบเสร็จค่าน้ำมัน
- ใบเสร็จไม่ครบตามที่เบิก
- ใส่วันทำงานอย่างน้อย 1 บรรทัด
- ไปรษณีย์
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่มีรายการ
- ไม่มีรายการค้าง
- ไม่ยกเลิก
- ไม่อนุมัติ
- ไม่อนุมัติ — ส่งกลับแก้ไข
- — ส่งกลับแก้ไข
- — ส่งกลับให้แก้ไข?

## §10.1 ฟังก์ชันหลักในไฟล์ (anchor สำหรับ test case)

`LN()` · `ME()` · `SEC()` · `STEPH()` · `actualRender()` · `add()` · `addAtt()` · `addLine()` · `applyRoute()` · `attList()` · `balanceOf()` · `bdById()` · `bdClose()` · `bdFmt()` · `bdIso()` · `bdNav()` · `bdOpenFor()` · `bdPick()` · `bdPlace()` · `bdRender()` · `bdToday()` · `bdToggle()` · `bedateHTML()` · `blankForm()` · `blankLine()` · `bootIfReady()` · `busyLabel()` · `canAct()` · `canCancel()` · `canSee()` · `cell()` · `clearFieldError()` · `closeDrawer()` · `closeModal()` · `closeOverlay()` · `closeRowMenu()` · `colText()` · `commitRejected()` · `confirmApprove()` · `confirmReason()` · `confirmSubmit()` · `curStep()` · `dSlash()` · `dayNameOf()` · `dirty()` · `docPill()` · `docPrintData()` · `empChip()` · `empOf()` · `emptyStateHTML()` · `ensureLineDateFns()` · `esc()` · `exportCSV()` · `fileRow()` · `findR()` · `fitPdf()` · `fmtDate()` · `fmtDateTime()` · `fmtMoney()` · `fmtNumber()` · `fmtSize()` · `gateFiles()` · `genPdf()` · `getRoute()` · `go()` · `goPage()` · `goStep()` · `grandOf()` · `hdrErr()` · `initSearchSelect()` · `initSelects()` · `int0()` · `isAdmin()` · `isOwner()` · `kv()` · `lineBad()` · `lineFilled()` · `lineHead()` · `lineRow()` · `lineTotal()` · `linesTable()` · `listRows()` · `loadLucide()` · `mark()` · `mkRec()` · `modalBackdropClick()` · `modalShell()` · `money2()` · `nFilled()` · `navigate()` · `nowIso()` · `num()` · `odoWarn()` · `onQ()` · `openApprove()` · `openCancel()` · `openDrawer()` · `openModal()` · `openModalCfg()` · `openOverlay()` · `openReject()` · `openRowMenu()` · `openSubmit()` · `openView()` · `pager()` · `persist()` · `pickFiles()` · `pill()` · `portalMenu()` · `positionMenu()` · `preserveRenderState()` · `preservedRender()` · `presetChips()` · `pushAudit()` · `rangeText()` · `removeFile()` · `removeLine()` · `render()` · `renderDetailTab()` · `renderHistoryTab()` · `renderIcons()` · `renderModal()` · `renderPage()` · `renderPdfTab()` · `renderSignProgress()` · `renderSignTab()` · `renderViewDrawer()` · `renderWizard()` · `reposition()` · `resetFilters()` · `resolveDoa()` · `resolveRole()` · `restoreRenderState()` · `rowClick()` · `saveAndSubmit()` · `saveDraft()` · `searchSelectHTML()` · `seedLines()` · `set()` · `setAtt()` · `setF()` · `setHdr()` · `setLine()` · `setLineDate()` · `setReasonPreset()` · `setStat()` · `setTab()` · `showDrawer()` · `showToast()` · `signN()` · `softSum()` · `sortBy()` · `sortTh()` · `ssClear()` · `ssEscapeReg()` · `ssFiltered()` · `ssGet()` · `ssOnInput()` · `ssOnKey()` · `ssOpen()` · `ssPick()` · `ssPortal()` · `ssPurgePortals()` · `ssRenderList()` · `ssSetText()` · `ssSyncChrome()` · `startWizard()` · `statCard()` · `stepper()` · `sumCard()` · `switchPersona()` · `tShort()` · `tabBtn()` · `toggleModule()` · `toggleSidebar()` · `toggleUserMenu()` · `totalsBlock()` · `totalsOf()` · `tplGet()` · `tplRender()` · `tplSignRows()` · `tryNext()` · `twpPdfBody()` · `twpPdfDoc()` · `txt()` · `updateShell()` · `validateField()` · `validateMain()` · `viewBanner()` · `wf()` · `withRenderPreservation()` · `wizAttach()` · `wizBack()` · `wizMain()` · `wizNext()` · `wizReview()` · `wordsFor()`

## §11.1 Marker ที่ต้อง wire ตอนพัฒนาจริง

| marker | บริบท |
|---|---|
| `ENG-DOC-NUM` | /* doc_type ประกาศผ่าน doccfg-declaration / mdoc-declaration · เลขรันจาก ENG-DOC-NUM (F-DOCCFG) · ออกเลขตอนบันทึกครั้งแร |
| `DOA-ENGINE-HOOK` | /* DOA-ENGINE-HOOK — resolve จาก DOA entry ของ feature นี้ ณ เวลาส่ง แล้ว snapshot ลง approval_chain (DOA_BRIEF_F-TMP-00 |
| `ENG-DOC-NUM` | /* บันทึก = ENG-DOC-NUM.next() ออกเลขที่ครั้งแรก (DEC-11) · ข้อมูลผู้จัดทำ snapshot ลงเอกสาร (ตำแหน่ง/ฝ่าย/โทรศัพท์ ณ วั |
| `ENG-NOTIFY` | /* ENG-NOTIFY (ntf-declaration): twp_cancelled → ผู้พิจารณาขั้นปัจจุบัน · DOA engine เป็นเจ้าของ doa_pending/doa_result  |
| `DOA-ENGINE-HOOK` | doa: MOCK_DOA_RESOLVED 1 ขั้น (role-line-manager) dynamic — resolveDoa() = DOA-ENGINE-HOOK · คำตัดสินผูก role (DECISION_ |
| `ENG-DOC-NUM` | hooks: ENG-DOC-NUM.next() ตอนบันทึกครั้งแรก (DEC-11 · รหัส TWP) · F-DOCCFG status ก่อนออกเลข (DOC.active) · ENG-NOTIFY t |
| `ENG-NOTIFY` | hooks: ENG-DOC-NUM.next() ตอนบันทึกครั้งแรก (DEC-11 · รหัส TWP) · F-DOCCFG status ก่อนออกเลข (DOC.active) · ENG-NOTIFY t |

## §11.2 QA hook

`window.__QA__` archetype = `Q-form` · qa_hook = True

