# UI BRIEF (AS-BUILT) — F-TMP-004 ใบเดินทาง : เขตการขาย General Trade

## §0 Document Control + Pairing
| หัวข้อ | ค่า |
|---|---|
| Feature | F-TMP-004 · REQ-TMP-004 (รหัสชั่วคราว) |
| ไฟล์ต้นแบบ | `feature.html` (html-generator-v9.2 · archetype **Q-form**) |
| คู่เอกสาร | `BRD_F-TMP-004.md` · `FRD_F-TMP-004_Pack/` · `DECISIONS.lock.md` · `print/TRV_print-spec.md` |
| ใบประกาศ | `DOCCFG_BRIEF_F-TMP-004.md` · `DOA_BRIEF_F-TMP-004.md` · `NTF_BRIEF_F-TMP-004.md` · `MDOC_BRIEF_TRV.md` |
| สถานะ | AS-BUILT จากต้นแบบ · audit FAIL 0 · **[NO-BROWSER] ยังไม่ได้รัน e2e / render-check** |
| วันที่ | 2026-10-07 |

## §2 Route Map
| route | หน้าจอ | refresh-safe |
|---|---|---|
| `#/travel-sheet` | ทะเบียนใบเดินทาง | ✓ |
| `#/travel-sheet/create` | drawer สร้างใบใหม่ (3 ขั้น) | ✓ |
| `#/travel-sheet/edit/:id` | drawer แก้ไขร่าง | ✓ |
| `#/travel-sheet/view` | ฐานของ route ดูรายละเอียด | ✓ |
| `#/travel-sheet/view/:id` | drawer ดูรายละเอียด (4 แท็บ) | ✓ |
`applyRoute()` อ่าน hash แล้วเปิด drawer ให้ตรง · `go()` เขียน hash กลับทุกครั้งที่เปลี่ยนหน้าจอ

## §3 Layout Shell
- Sidebar 232px (`--sidebar-w`) · module `Sales` › feature `ใบเดินทาง` + badge นับใบที่รอฉันพิจารณา
- Shell bar 52px (`--shell-h`) · breadcrumb `Core › Sales › ใบเดินทาง` · ปุ่มแจ้งเตือน · user chip + เมนูสลับ persona
- `#overlay-root` และ `#toast` ก่อน `</body>` (Rule #95 portal)

## §4 Page Anatomy
### 4.1 ทะเบียน (`#/travel-sheet`)
`.page-fill` → `.ph` (หัวข้อ + chip นับ + ปุ่ม ส่งออก CSV / สร้างใบเดินทาง) → `.stats` 3 ใบ → `.card.list-card` (filter-bar → `.table-wrap` → `.table-foot`)
คอลัมน์: เลขที่ · วันที่ขอ · ผู้รับผิดชอบเขต · เขต · รอบการขาย · ช่วงวันทำงาน · สถานะเอกสาร · ลายเซ็น · ยอดขายจริง (บาท) · ⋮
เมนู ⋮: แก้ไข (ร่างของตัวเอง) · พิมพ์ · ยกเลิกเอกสาร — **ไม่มีทำซ้ำ** (DEC-11)

### 4.2 drawer สร้าง/แก้ไข (`.drawer.drawer-panel.wide`)
`.dw-head` (eyebrow + title + `.d-stepper` 3 ขั้น) → `.drawer-body.is-soft` → `.dw-footer`
- ขั้น 1 `.wz-split` = `.wz-main` (การ์ด ① หัวเอกสาร · การ์ด ② ตารางวันทำงาน `.trv-tbl` 19 คอลัมน์ + แถวรวมยอด) + `.wz-sum` (การ์ดสรุปสด sticky)
- ขั้น 2 `.upload-zone` + `.file-row`
- ขั้น 3 `.review-card` 4 ใบ (ข้อมูลใบเดินทาง · วันทำงาน · รวมยอด · เอกสารแนบ)

### 4.3 drawer ดูรายละเอียด (`.drawer.drawer-panel`)
`.dw-head` (doc-ident + pill สถานะ + ป้าย "ส่งกลับแก้ไข") → `.drawer-tabs` 4 แท็บ → `.drawer-body` → `.dw-footer`
แท็บ: รายละเอียด · PDF Preview (`.pdf-slot > iframe.pdf-frame`) · ลายเซ็น / อนุมัติ (`.timeline`) · ประวัติ

## §5 Component Inventory
| component | class หลัก | ใช้ที่ |
|---|---|---|
| การ์ดสถิติ | `.stat` `.stat-label` `.stat-value` `.stat-meta` | ทะเบียน |
| ตารางข้อมูล | `.table` `.table-wrap` `.table-foot` | ทะเบียน · วันทำงาน |
| ตารางกรอกวันทำงาน | `.trv-tbl` `.trv-ed` `.in-num` `.in-txt` `.trv-total` | ขั้น 1 |
| การ์ดสรุปสด | `.wz-sum` `.wz-sum-row` `.wz-sum-total` | ขั้น 1 |
| การ์ดรวมยอด | `.trv-sum` `.pd-cell` `.pd-l` `.pd-v` | รายละเอียด · ขั้น 3 |
| search select | `.ss-list` `.menu-fixed` | ตัวกรอง · เขต · รอบการขาย · เลือกผู้พิจารณา |
| ตัวเลือกวัน พ.ศ. | `.bedate` `.bd-pop` `.bd-grid` `.bd-day` | ทุกช่องวันที่ (Rule #114) |
| stepper | `.d-stepper` `.stepper-item` `.stepper-circle` | drawer สร้าง/แก้ไข |
| timeline | `.timeline` `.tl-item` `.tl-dot` `.tl-acts` | ลายเซ็น · ประวัติ |
| pill สถานะ | `.pill` `.pill-muted/-warning/-success/-danger` | ทะเบียน · drawer |
| ความคืบหน้าลายเซ็น | `.sign-prog` `.sp-bar` `.sp-fill` | ทะเบียน · แท็บลายเซ็น |
| row menu | `.row-menu` `.rm-item` | ทะเบียน (portal) |
| modal | `.modal` `.modal-header` `.modal-body` `.modal-footer` `.slot-row` | ส่ง/อนุมัติ/ไม่อนุมัติ/ยกเลิก/ทิ้งข้อมูล |

## §7 Interaction Spec
- พิมพ์ในตารางวันทำงาน → อัปเดตแถวรวมยอดและการ์ดสรุปแบบ **soft** (`softSum()`) ไม่ rebuild ทั้งหน้า focus ไม่หลุด
- เลือกวันที่ → `bedateHTML()` เปิด `.bd-pop` ใน `#overlay-root` · Esc ปิดเฉพาะปฏิทิน ไม่ทะลุไปปิด drawer
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
สร้างใบเดินทาง · ส่งออก CSV · ล้างตัวกรอง · เพิ่มวันทำงาน · ย้อนกลับ · ถัดไป · ยกเลิก · บันทึกแบบร่าง · บันทึกและส่งอนุมัติ · แก้ไข · ส่งอนุมัติ · อนุมัติ · ไม่อนุมัติ · ยกเลิกเอกสาร · พิมพ์ · ดาวน์โหลด PDF · ปิด · กลับไปกรอกต่อ · ทิ้งข้อมูล · วันนี้

## §9.4 ป้ายช่องและหัวข้อ (คัดตรงจากกระดาษ — ห้ามเกลา)
TO : · CC : · ผู้รับผิดชอบเขต : · ตำแหน่ง : · เขต : · รอบการขาย : · วันทำงาน · วันที่ · เริ่มต้นตลาด · สิ้นสุดตลาด · จำนวน · วางบิล · Accual · รับเช็ค · เป้าหมายการขาย · บิล · บาท · ร้าน · จังหวัดที่ปฎิบัติงาน · ที่พัก (จังหวัด) · รวมยอด · ผู้นำเสนอ · ผู้อนุมัติ
> คำสะกด "Accual" และ "ปฎิบัติงาน" คงตามกระดาษตามมติ DEC-15 · DEC-16

## §9.5 ข้อความสถานะ / ว่าง / เตือน (verbatim)
- สถานะเอกสาร: ร่าง · รออนุมัติ · อนุมัติแล้ว · ยกเลิก · ส่งกลับแก้ไข
- สถานะขั้นอนุมัติ: ยังไม่ถึงขั้นนี้ · รอพิจารณา · อนุมัติ · ไม่อนุมัติ · ข้าม
- ว่าง: ยังไม่มีใบเดินทาง · ไม่พบรายการที่ค้นหา · ไม่มีเอกสารแนบ
- เตือน: กรุณากรอกข้อมูลให้ครบถ้วน · ใส่วันทำงานอย่างน้อย 1 บรรทัด · วันที่ซ้ำกับแถวที่ N · ตัวเลขต้องไม่ติดลบ · กรอกข้อมูลไว้แล้วแต่ยังไม่ได้เลือกวันที่ · ผลจริงมากกว่าแผนใน N กลุ่ม

## §10 Data Binding & BACKEND anchors
| หน้าจอ | ฟังก์ชัน | endpoint จริง (02_API) |
|---|---|---|
| ทะเบียน | `listRows()` · `renderPage()` | A1 `GET /sales/travel-sheets` |
| เปิดดู | `openView()` · `renderViewDrawer()` | A2 `GET /sales/travel-sheets/{id}` |
| บันทึกร่าง | `persist()` · `saveDraft()` | A3 `POST` · A4 `PUT` |
| ส่งอนุมัติ | `openSubmit()` · `confirmSubmit()` | A5 `POST /submit` |
| อนุมัติ | `confirmApprove()` | A6 `POST /approve` |
| ไม่อนุมัติ / ยกเลิก | `confirmReason()` | A7 `POST /reject` · A8 `POST /cancel` |
| แบบพิมพ์ | `docPrintData()` · `tplRender()` · `genPdf()` | A9 `GET /pdf` |
| ส่งออก | `exportCSV()` | A10 `GET /export.csv` |
| สายอนุมัติ | `resolveDoa()` · `resolveRole()` | DOA กลาง (F-DLG-001) |
| ยอดรวม | `totalsOf()` | คำนวณที่ server ด้วยสูตรเดียวกัน |

## §11 Traceability + Drift Log
| มติ | เห็นที่ไหนในต้นแบบ |
|---|---|
| DEC-03 | `MOCK_DOA_RESOLVED` 2 ขั้น + modal ส่ง 1 ช่องต่อขั้น |
| DEC-04 · DEC-12 | แถว `รวมยอด` อ่านอย่างเดียว + `totalsOf()` รวมทุกแถว + คำเตือน Accual > แผน |
| DEC-05 | ปุ่ม "เพิ่มวันทำงาน" ไม่จำกัด · แบบพิมพ์เติมครบ 31 แถว (`PDF_MIN_ROWS`) |
| DEC-06 | ช่องในขั้น 1 ตรงกระดาษ ไม่มีช่องหมายเหตุ |
| DEC-07 | `tplSignRows()` ผู้นำเสนอ + 1 ช่องต่อขั้น · ไม่มีภาพลายมือชื่อ |
| DEC-08 | `confirmReason()` kind=reject → `status='draft'` + `returned=true` เลขเดิม |
| DEC-09 | `canSee()` · `canAct()` · `isAdmin()` |
| DEC-10 | `DOC.prefix = 'TRV'` · ออกเลขใน `persist()` |
| DEC-11 | ไม่มีฟังก์ชันทำซ้ำเอกสารในไฟล์ (เมนู ⋮ มีแค่ แก้ไข · พิมพ์ · ยกเลิกเอกสาร) · มี `exportCSV()` |
**Drift:** ไม่มี — ต้นแบบตรงกับ FRD ทุกข้อ ณ รอบนี้

## §12 Diff จากเวอร์ชันก่อน
เวอร์ชันแรกของ feature นี้ — ไม่มี diff

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
1. เพิ่มการนำเข้าแถววันทำงานจาก Excel/CSV (ลดการพิมพ์ 31 แถว)
2. เพิ่มมุมมองเปรียบเทียบ แผน vs ผลจริง รายเขต/รายรอบ
3. ถ้าลูกค้าต้องการ "ทำซ้ำใบของรอบก่อน" ให้เปิดเป็น enhancement (รอบนี้ปิดตาม DEC-11)

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

- ค้นหาเลขที่ / ผู้รับผิดชอบเขต / เขต / รอบการขาย
- ผู้รับสำเนา (ถ้ามี)
- ผู้รับใบเดินทาง เช่น ฝ่ายขาย สำนักงานใหญ่
- ไม่บังคับ

## §9.8 Microcopy ภาษาไทยทั้งหมดในไฟล์ (verbatim · รวมข้อมูลตัวอย่างที่สมมติขึ้น)

- (ขั้น
- Accual รับเช็ค (บาท)
- Accual วางบิล (บาท)
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
- กันยายน 2569
- กาญจนบุรี
- กำลังเปิดหน้าต่างพิมพ์ ·
- กุมภาพันธ์
- ขั้นทดสอบ
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลรอบการขายไม่ครบ
- ข้อมูลหลักใบเดินทาง
- ข้าม
- คน
- คลิกเพื่อดูรายการ
- คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค่าเริ่มต้นจากสายอนุมัติ (DOA) และผังองค์กร
- ค้นหา...
- ค้นหาเลขที่ / ผู้รับผิดชอบเขต / เขต / รอบการขาย
- จำนวน (รวม)
- ชนิดไฟล์ไม่รองรับ
- ชื่อ-สกุล
- ชื่อฟังก์ชัน
- ดาวน์โหลด PDF
- ต.ค.
- ตรวจสอบและยืนยัน
- ตลาดกลางเขต A
- ตลาดกลางเขต B
- ตลาดชุมชน C
- ตลาดนัดเขต E
- ตลาดสดเขต D
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตัวเลขต้องไม่ติดลบ
- ตำแหน่ง
- ตุลาคม
- ตุลาคม 2569
- ต้อง
- ถึง
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ที่คุณเกี่ยวข้อง
- ทุกฝ่าย
- ทุกสถานะ
- ทุกเขต
- ธ.ค.
- ธนากร บริหารขาย
- ธบ
- ธันวาคม
- นครปฐม
- บอกผู้รับผิดชอบเขตว่าต้องแก้อะไร
- บันทึกผิดใบ
- บันทึกร่างแล้ว ·
- บาท
- บิล
- ปด
- ประวัติ
- ประวัติ (append-only)
- ปรีชา เดินตลาด
- ปิด
- ผลจริง
- ผู้จัดการฝ่ายขาย
- ผู้จัดการฝ่ายบัญชี
- ผู้นำเสนอ
- ผู้รับผิดชอบเขต
- ผู้รับสำเนา (ถ้ามี)
- ผู้รับใบเดินทาง เช่น ฝ่ายขาย สำนักงานใหญ่
- ผู้ส่ง
- ผู้อนุมัติ (ลำดับ 1)
- ผู้อนุมัติ (ลำดับ 2)
- ฝ่าย
- ฝ่ายขาย
- ฝ่ายขาย สำนักงานใหญ่
- ฝ่ายบัญชี
- พ.ค.
- พ.ย.
- พนักงานขายเขต
- พฤ
- พฤศจิกายน
- พฤศจิกายน 2569
- พฤษภาคม
- พิจารณาในระบบ
- พิมพ์
- ม.ค.
- มกราคม
- มบ
- มานพ บัญชีมั่น
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
- ยอดขายจริง (บาท)
- ยอดขายจริงรวม
- ยอดเป้าหมายไม่สอดคล้องกับแผนเขต
- ยังไม่ถึงขั้นนี้
- ยังไม่มีข้อมูล
- ยังไม่มีใบเดินทาง
- ยังไม่ระบุผู้พิจารณา
- ยังไม่ส่ง
- ย้อนกลับ
- รวม
- รอฉันพิจารณา
- รอบการขาย
- รอผล
- รอผู้อนุมัติพิจารณา
- รอพิจารณา
- รออนุมัติ
- รับเช็ค
- รับเช็ค (บาท)
- รับเช็ค (บิล)
- ราชบุรี
- รายการ
- รายละเอียด
- ร่าง
- ร้าน
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ลายเซ็น / อนุมัติ
- ลำดับการอนุมัติ
- ล้างตัวกรอง
- วด
- วัน
- วันทำงาน
- วันทำงานซ้ำซ้อน ขอให้ตรวจอีกครั้ง
- วันที่ ........./........./.........
- วันที่ขอ
- วางบิล
- วางบิล (บาท)
- วางบิล (บิล)
- วิไล ดูแลทีม
- ส.ค.
- สข
- สค
- สถานะ
- สถานะเอกสาร
- สมชาย ขยันขาย
- สร้าง PDF
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างโดย
- สร้างใบเดินทาง
- สร้างใบเดินทาง เขตการขาย
- สร้างใบเดินทางของรอบการขาย เพื่อวางแผนวันทำงานและส่งให้ผู้อนุมัติ
- สลับเป็น
- สิงหาคม
- สิงหาคม 2569
- สุพรรณบุรี
- สุรชัย คุมเขต
- ส่งกลับแก้ไข
- ส่งกลับแก้ไข — กลับเป็นร่างเลขที่เดิม
- ส่งกลับให้แก้ไขแล้ว ·
- ส่งอนุมัติ
- ส่งอนุมัติแล้ว ·
- ส่งอนุมัติใบเดินทาง?
- ส่งออก
- ส่งแล้วแก้ไขไม่ได้จนกว่าผู้อนุมัติจะส่งกลับแก้ไข
- ส่งในระบบ
- หัวหน้าหน่วยขาย
- อต
- อนุมัติ
- อนุมัติ (ขั้น
- อนุมัติแล้ว
- อนุมัติใบเดินทางครบทุกขั้น
- อา
- อารีย์ ตรวจสอบ
- เขต
- เขต GT-01 ภาคกลาง
- เขต GT-02 ภาคตะวันออก
- เขต GT-03 ภาคเหนือตอนล่าง
- เขต GT-04 ภาคอีสานตอนกลาง
- เขต GT-05 ภาคใต้ตอนบน
- เจ้าหน้าที่บัญชีลูกหนี้
- เดือนถัดไป
- เด้งกลับบน
- เปลี่ยนผู้รับผิดชอบเขต
- เป้าหมายการขาย
- เป้าหมายการขาย (บาท)
- เป้าหมายการขาย (ร้าน)
- เพชรบุรี
- เพิ่มเติม
- เม.ย.
- เมษายน
- เลขที่
- เลขที่เอกสาร
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกประเทศ
- เลือกผู้พิจารณา
- เลือกรอบการขาย
- เลือกวันที่
- เลือกเขตการขาย
- เลือกเขตและรอบการขาย แล้วใส่วันทำงานทีละบรรทัดเหมือนกระดาษเดิม — ยอดรวมระบบคำนวณให้
- เหตุผลที่ยกเลิก
- เอกสารแนบ
- แก้ไขร่าง
- แก้ไขล่าสุด
- แก้ไขเอกสาร
- แก้ไขใบเดินทาง
- แก้ไขได้เฉพาะร่างของตัวเอง
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- แผนเยี่ยมร้านประจำเดือน.pdf
- แล้ว ·
- ใบเดินทาง : เขตการขาย General Trade
- ใบเดินทางทั้งหมด
- ใส่วันทำงานอย่างน้อย 1 บรรทัด
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่มีรายการค้าง
- ไม่ยกเลิก
- ไม่อนุมัติ
- ไม่อนุมัติ — ส่งกลับแก้ไข
- — คุณเป็นผู้พิจารณาใบนี้
- — ส่งกลับแก้ไข
- — ส่งกลับให้แก้ไข?

## §10.1 ฟังก์ชันหลักในไฟล์ (anchor สำหรับ test case)

`LN()` · `ME()` · `SEC()` · `STEPH()` · `actualRender()` · `add()` · `addLine()` · `applyRoute()` · `bdById()` · `bdClose()` · `bdFmt()` · `bdIso()` · `bdNav()` · `bdOpenFor()` · `bdPick()` · `bdPlace()` · `bdRender()` · `bdToday()` · `bdToggle()` · `bedateHTML()` · `blankForm()` · `blankLine()` · `bootIfReady()` · `busyLabel()` · `canAct()` · `canCancel()` · `canSee()` · `cell()` · `clearFieldError()` · `closeDrawer()` · `closeModal()` · `closeOverlay()` · `closeRowMenu()` · `colText()` · `commitRejected()` · `confirmApprove()` · `confirmReason()` · `confirmSubmit()` · `curStep()` · `dSlash()` · `dirty()` · `docPill()` · `docPrintData()` · `empChip()` · `empOf()` · `emptyStateHTML()` · `ensureLineDateFns()` · `esc()` · `exportCSV()` · `fileRow()` · `findR()` · `fitPdf()` · `fmtDate()` · `fmtDateTime()` · `fmtMoney()` · `fmtNumber()` · `fmtSize()` · `gateFiles()` · `genPdf()` · `getRoute()` · `go()` · `goPage()` · `goStep()` · `hdrErr()` · `initSearchSelect()` · `initSelects()` · `int0()` · `isAdmin()` · `isOwner()` · `kv()` · `lineBad()` · `lineFilled()` · `lineHead()` · `lineRow()` · `linesTable()` · `listRows()` · `loadLucide()` · `mark()` · `mkRec()` · `modalBackdropClick()` · `modalShell()` · `money2()` · `nFilled()` · `navigate()` · `nowIso()` · `num()` · `onQ()` · `openApprove()` · `openCancel()` · `openDrawer()` · `openModal()` · `openModalCfg()` · `openOverlay()` · `openReject()` · `openRowMenu()` · `openSubmit()` · `openView()` · `pager()` · `persist()` · `pickFiles()` · `pill()` · `planWarn()` · `portalMenu()` · `positionMenu()` · `preserveRenderState()` · `preservedRender()` · `presetChips()` · `pushAudit()` · `rangeText()` · `removeFile()` · `removeLine()` · `render()` · `renderDetailTab()` · `renderHistoryTab()` · `renderIcons()` · `renderModal()` · `renderPage()` · `renderPdfTab()` · `renderSignProgress()` · `renderSignTab()` · `renderViewDrawer()` · `renderWizard()` · `reposition()` · `resetFilters()` · `resolveDoa()` · `resolveRole()` · `restoreRenderState()` · `rowClick()` · `saveAndSubmit()` · `saveDraft()` · `searchSelectHTML()` · `seedLines()` · `set()` · `setF()` · `setHdr()` · `setLine()` · `setReasonPreset()` · `setStat()` · `setTab()` · `showDrawer()` · `showToast()` · `signN()` · `softSum()` · `sortBy()` · `sortTh()` · `ssClear()` · `ssEscapeReg()` · `ssFiltered()` · `ssGet()` · `ssOnInput()` · `ssOnKey()` · `ssOpen()` · `ssPick()` · `ssPortal()` · `ssPurgePortals()` · `ssRenderList()` · `ssSetText()` · `ssSyncChrome()` · `startWizard()` · `statCard()` · `stepper()` · `sumCard()` · `switchPersona()` · `tShort()` · `tabBtn()` · `toggleModule()` · `toggleSidebar()` · `toggleUserMenu()` · `totalsBlock()` · `totalsOf()` · `tplGet()` · `tplRender()` · `tplSignRows()` · `trvPdfBody()` · `trvPdfDoc()` · `tryNext()` · `updateShell()` · `validateField()` · `validateMain()` · `viewBanner()` · `wf()` · `withRenderPreservation()` · `wizAttach()` · `wizBack()` · `wizMain()` · `wizNext()` · `wizReview()` · `wordsFor()`

## §11.1 Marker ที่ต้อง wire ตอนพัฒนาจริง

| marker | บริบท |
|---|---|
| `ENG-DOC-NUM` | /* doc_type ประกาศผ่าน doccfg-declaration / mdoc-declaration · เลขรันจาก ENG-DOC-NUM (F-DOCCFG) · ออกเลขตอนบันทึกครั้งแร |
| `DOA-ENGINE-HOOK` | /* DOA-ENGINE-HOOK — resolve จาก DOA entry ของ feature นี้ ณ เวลาส่ง แล้ว snapshot ลง approval_chain (DOA_BRIEF_F-TMP-00 |
| `ENG-DOC-NUM` | /* บันทึก = ENG-DOC-NUM.next() ออกเลขที่ครั้งแรก (DEC-10) · ข้อมูลผู้รับผิดชอบเขต snapshot ลงเอกสาร (ตำแหน่ง/ฝ่าย ณ วันท |
| `ENG-NOTIFY` | /* ENG-NOTIFY (ntf-declaration): trv_cancelled → ผู้พิจารณาขั้นปัจจุบัน · DOA engine เป็นเจ้าของ doa_pending/doa_result  |
| `DOA-ENGINE-HOOK` | doa: MOCK_DOA_RESOLVED 2 ขั้น (role-line-manager > role-mgr-sales) dynamic — resolveDoa() = DOA-ENGINE-HOOK · คำตัดสินผู |
| `ENG-DOC-NUM` | hooks: ENG-DOC-NUM.next() ตอนบันทึกครั้งแรก (DEC-10 · รหัส TRV) · F-DOCCFG status ก่อนออกเลข (DOC.active) · ENG-NOTIFY t |
| `ENG-NOTIFY` | hooks: ENG-DOC-NUM.next() ตอนบันทึกครั้งแรก (DEC-10 · รหัส TRV) · F-DOCCFG status ก่อนออกเลข (DOC.active) · ENG-NOTIFY t |

## §11.2 QA hook

`window.__QA__` archetype = `Q-form` · qa_hook = True

