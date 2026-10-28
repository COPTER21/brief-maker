# UI BRIEF (AS-BUILT) — F-TMP-005 แบบฟอร์มสำรวจสมรรถนะ

## §0 Document Control + Pairing
| | |
|---|---|
| Feature | F-TMP-005 · REQ-TMP-005 · module HR |
| Prototype | `feature.html` (html-generator-v9.2 · Pattern Q2 Q-form) · `<meta name="cube-archetype" content="Q-form">` |
| แบบพิมพ์ | `print/form.tpl.html` (thai-doc-pdf-generator v2.1 · Replica · FM-HRM-40 REV.00) |
| คู่เอกสาร | `BRD_F-TMP-005.md` · `FRD_F-TMP-005_Pack/` · `DOCCFG_BRIEF_F-TMP-005.md` · `DOA_BRIEF_F-TMP-005.md` · `NTF_BRIEF_F-TMP-005.md` · `MDOC_BRIEF_CMP.md` |
| สถานะมติ | `[AI-DEFAULT]` ทั้ง 12 ข้อ — รอลูกค้ายืนยัน |
| รอบนี้ | โหมดไม่เฝ้า · NO-BROWSER (ยังไม่ได้ render จริง) |

## §2 Route Map
| route | หน้าจอ |
|---|---|
| `#/cmp` | รายการแบบฟอร์มสำรวจสมรรถนะ |
| `#/cmp/create` | ลิ้นชักสร้างใหม่ (wizard 3 ขั้น) |
| `#/cmp/edit/:id` | ลิ้นชักแก้ไขร่าง |
| `#/cmp/view` | ลิ้นชักดูเอกสาร (ฐาน route) |
| `#/cmp/view/:id` | ลิ้นชักดูเอกสารรายใบ (4 แท็บ) |

refresh-safe ทุก route — `applyRoute()` อ่าน hash แล้วเปิด surface เดิม

## §3 Layout Shell
Sidebar (module HR › สำรวจสมรรถนะ) + topbar + breadcrumb + `page-content` เต็มความสูง
`.page-fill` + `.table-wrap` scroll ภายใน + `thead` sticky + `.table-foot` ติดล่าง (Rule #96)
responsive desktop-base: ≥1180 เต็ม · 768–1180 adaptive · `overlay-root` + `toast-root` ก่อน `</body>`

## §4 Page Anatomy — หน้ารายการ
1. `.ph` หัวเรื่อง + จำนวนรายการ + ปุ่มขวา (`ส่งออก CSV` · `สร้างแบบฟอร์ม`)
2. แถบเตือนเมื่อแบบเอกสารยังไม่เปิดใช้งาน
3. `.stats` การ์ดสถิติ 3 ใบ คลิกเพื่อกรอง
4. `.filter-bar` ค้นหา + ตัวกรอง 3 ช่อง + ล้างตัวกรอง
5. ตาราง 10 คอลัมน์ + `.row-menu` (⋮) + pager

## §5 Component Inventory
| component | ใช้ที่ |
|---|---|
| `.stat` การ์ดสถิติคลิกได้ | หน้ารายการ |
| `.input-search` + search-select ×3 | ตัวกรอง |
| `.table` + `.sign-prog` + `.pill` | ตารางรายการ |
| `.row-menu` (portal ใน `#overlay-root`) | เมนู ⋮ |
| `.drawer-panel` / `.drawer-panel.wide` | ดูเอกสาร / wizard |
| `.d-stepper` 3 ขั้น | wizard |
| `.wz-card` + `.wz-sum` | ขั้น 1 ของ wizard |
| `.trv` การ์ดรายการสมรรถนะ + `.lv-row` ปุ่มระดับ 1–4 | สมรรถนะหลัก / สมรรถนะเฉพาะสายงาน |
| `.chip` เลือกหลายข้อ | แนวทางการพัฒนา · chip เหตุผล |
| `.upload-zone` + `.file-row` | เอกสารแนบ |
| `.drawer-tabs` 4 แท็บ | ลิ้นชักดูเอกสาร |
| `.pdf-slot` + `.pdf-frame` (iframe A4) | แท็บ PDF Preview |
| `.timeline` | แท็บลายเซ็น และแท็บประวัติ |
| `.modal` / `.modal.is-lg` + `.slot-row` | modal ส่งอนุมัติ และ modal อื่น |
| `.bedate` + `.bd-pop` | ตัวเลือกวัน พ.ศ. (Rule #114) |

## §7 Interaction Spec
- คลิกแถวในตาราง → เปิดลิ้นชักดูเอกสาร (คลิกที่คอลัมน์ ⋮ ไม่เปิด)
- ปุ่มระดับ 1–4: กดเลือก · กดซ้ำที่ค่าเดิมเพื่อยกเลิก · แสดงคำอธิบายระดับจาก config ข้างปุ่ม
- `เพิ่มรายการสมรรถนะ` → เพิ่มการ์ดใหม่แล้ว focus ช่องแรก · ลบได้เมื่อเหลือมากกว่า 1 การ์ด
- ปิด wizard ขณะมีข้อมูลยังไม่บันทึก → modal ยืนยันก่อนทิ้ง
- ปุ่มบันทึกและส่งอนุมัติ disable + loader ระหว่างทำงาน (กันกดซ้ำ)
- สลับผู้ใช้ (persona) จากเมนูมุมขวาบน — เดโมสายอนุมัติเท่านั้น

## §8 State-Driven UI Matrix
| สถานะ | แบนเนอร์ | ปุ่มในหัวลิ้นชัก | ⋮ |
|---|---|---|---|
| ร่าง (เจ้าของ) | ยังเป็นร่าง | ยกเลิก · แก้ไข · ส่งอนุมัติ | แก้ไข · พิมพ์ · ยกเลิกเอกสาร |
| รออนุมัติ (ผู้พิจารณาขั้นปัจจุบัน) | รอ … พิจารณา | ส่งกลับแก้ไข · เห็นชอบ | พิมพ์ |
| รออนุมัติ (เจ้าของ/admin) | รอ … พิจารณา | ยกเลิกเอกสาร | พิมพ์ · ยกเลิกเอกสาร |
| อนุมัติแล้ว | — | — (ล็อกแก้ไข) | พิมพ์ |
| ไม่อนุมัติ (ขั้นถูกส่งกลับ) | ส่งกลับแก้ไข — เหตุผล | ตามสถานะร่าง | ตามสถานะร่าง |
| ยกเลิก | ยกเลิกแล้ว — เหตุผล | — | พิมพ์ |

## §9.1 ปุ่ม (verbatim)
`สร้างแบบฟอร์ม` · `ส่งออก CSV` · `ล้างตัวกรอง` · `ถัดไป` · `ย้อนกลับ` · `บันทึกแบบร่าง` · `บันทึกและส่งอนุมัติ` ·
`ส่งอนุมัติ` · `เห็นชอบ` · `ส่งกลับแก้ไข` · `ยกเลิกเอกสาร` · `แก้ไข` · `พิมพ์` · `ดาวน์โหลด PDF` · `ปิด` ·
`เพิ่มรายการสมรรถนะ` · `กลับไปกรอกต่อ` · `ทิ้งข้อมูล` · `ยกเลิก` · `วันนี้`

## §9.4 ป้ายช่องและหัวข้อ (คัดตรงจากกระดาษ FM-HRM-40 — ห้ามเกลา)
`ข้อมูลทั่วไป` · `ชื่อ–สกุล` · `ตำแหน่ง` · `แผนก` · `วันที่ประเมิน` · `ระดับการประเมินสมรรถนะ` · `ระดับ` · `คำอธิบาย` ·
`สมรรถนะหลัก (Core Competency)` · `สมรรถนะเฉพาะสายงาน (Functional Competency)` · `รายการสมรรถนะ` · `ระดับประเมิน (1–4)` ·
`สรุปผลและแผนพัฒนา` · `จุดแข็งของพนักงาน` · `สมรรถนะที่ควรพัฒนาเพิ่มเติม` · `แนวทางการพัฒนา` · `อบรมเพิ่มเติม` ·
`Coaching` · `On-the-job Training` · `รายละเอียดเพิ่มเติม` · `ลงชื่อผู้ประเมิน` · `ลงชื่อผู้รับประเมิน`

## §9.5 ข้อความสถานะ / ว่าง / เตือน (verbatim)
- สถานะ: `ร่าง` · `รออนุมัติ` · `อนุมัติแล้ว` · `ไม่อนุมัติ` · `ยกเลิก`
- ว่าง: `ยังไม่มีแบบฟอร์มสำรวจสมรรถนะ` · `ไม่พบรายการที่ค้นหา` · `ไม่มีเอกสารแนบ`
- เตือนในฟอร์ม: `ใส่รายการสมรรถนะ หรือลบบรรทัดนี้` · `เลือกระดับประเมิน 1–4 ของรายการนี้` · `เลือกวันที่ประเมิน` · `กรุณาระบุเหตุผล` · `กรุณาเลือกผู้พิจารณา`

## §10 Data Binding & BACKEND anchors
| หน้าจอ | ฟังก์ชันใน prototype | ระบบจริง |
|---|---|---|
| รายการ | `listRows()` | `GET /api/hr/competency-survey` |
| ดูเอกสาร | `renderDetailTab()` | `GET /api/hr/competency-survey/{id}` |
| บันทึก | `persist()` | `POST /` · `PUT /{id}` (FN-01) |
| ส่งอนุมัติ | `confirmSubmit()` | `POST /{id}/submit` (FN-03) |
| เห็นชอบ | `confirmApprove()` | `POST /{id}/approve` (FN-04) |
| ส่งกลับแก้ไข และ ยกเลิก | `confirmReason()` | `POST /{id}/reject` · `POST /{id}/cancel` (FN-05 · FN-06) |
| แบบพิมพ์ | `docPrintData()` · `tplRender()` · `tplSignRows()` | `GET /{id}/pdf` (FN-07) |
| สายอนุมัติ | `resolveDoa()` | `GET /api/doa/resolve` (DOA-ENGINE-HOOK) |
| สิทธิ์การมองเห็น | `canSee()` · `canAct()` | กรองที่ชั้น service (FN-08) |
| ส่งออก CSV | `exportCSV()` | `GET /export.csv` |

## §11 Traceability + Drift Log
| มติ | เห็นที่หน้าจอ |
|---|---|
| DEC-03 | modal ส่งอนุมัติสร้าง slot ตามจำนวนขั้นที่ `resolveDoa()` คืน — ไม่ fix จำนวน |
| DEC-04 | `LEVEL_CONFIG` ใช้ทั้ง legend ในฟอร์ม ตารางในลิ้นชัก และแบบพิมพ์ |
| DEC-05 · DEC-06 | เพิ่มรายการสมรรถนะได้ไม่จำกัด · แบบพิมพ์เติมแถวว่างครบขั้นต่ำ |
| DEC-07 | ไม่มีช่องคะแนนรวมหรือคะแนนเฉลี่ยในทุกหน้าจอ |
| DEC-08 | `tplSignRows()` แบ่งช่องลงชื่อแถวละไม่เกิน 4 |
| DEC-09 | `confirmReason()` ตั้งสถานะกลับเป็นร่างโดยใช้เลขเดิม |
| DEC-10 | `canSee()` กันร่างของคนอื่นไม่ให้ผู้พิจารณาเห็น |
| DEC-11 | `persist()` ออกเลขเฉพาะตอนสร้างใบใหม่ |
| DEC-12 | มีปุ่มส่งออก CSV และเอกสารแนบ · ไม่มีคำสั่งทำซ้ำในไฟล์ |

Drift: ไม่มี — prototype รอบนี้สร้างครั้งเดียวจาก FORM_SPEC + DECISIONS.lock ไม่มีรอบ vibe

## §12 Diff จากเวอร์ชันก่อน
เวอร์ชันแรก (v1) — ไม่มี diff

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
1. ทำ master ชุดสมรรถนะต่อตำแหน่ง แล้วให้เลือกแทนการพิมพ์ชื่อเอง — ลดความต่างของคำระหว่างพนักงาน
2. เพิ่มมุมมองสรุปรายฝ่ายให้ฝ่ายบุคคล (จำนวนคนต่อระดับในแต่ละสมรรถนะ) เป็น feature รายงานแยก
3. เชื่อมแนวทางการพัฒนาไปยังแผนอบรมประจำปี — ต้องเปิดมติ G1 ใหม่ (รอบนี้ปิดไว้ตาม DEC-02)

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
| ระบุสมรรถนะที่ควรพัฒนาแล้ว แต่ยังไม่ได้เลือกแนวทางการพัฒนา | warning |
| กรุณากรอกข้อมูลให้ครบถ้วน | warning |
| กรุณากรอกข้อมูลให้ครบถ้วน | warning |
| บันทึกร่างแล้ว · | info |
| กรุณากรอกข้อมูลให้ครบถ้วน | warning |
| ส่งอนุมัติแล้ว · | info |
| ส่งออก | info |
| สลับเป็น | info |
| แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง | error |

## §9.3 Placeholder (verbatim)

- คำอธิบาย
- ค้นหาเลขที่ / ผู้รับประเมิน / ตำแหน่ง / รายการสมรรถนะ
- รายการสมรรถนะ
- เช่น การใช้ระบบงานและการแก้ปัญหาเฉพาะหน้า
- เช่น ทำงานร่วมกับทีมได้ดี รับผิดชอบงานจนเสร็จตามกำหนด
- ไม่บังคับ

## §9.8 Microcopy ภาษาไทยทั้งหมดในไฟล์ (verbatim · รวมข้อมูลตัวอย่างที่สมมติขึ้น)

- [Lucide] All CDNs failed. Icons จะไม่แสดง but UI ยังใช้งานได้
- ]); if (canCancel(r)) items.push(['x-circle', 'ยกเลิกเอกสาร',
- ]]; if (isOwner(r) && r.status === 'draft') items.unshift(['pencil', 'แก้ไข',
- showToast('ไม่มีการแจ้งเตือนใหม่','info')
- · อนุมัติแล้ว ล็อกแก้ไข
- ก.ค.
- ก.พ.
- ก.ย.
- กบ
- กรกฎาคม
- กรุณากรอกข้อมูลให้ครบถ้วน
- กลับเป็นร่าง
- กลับไปกรอกต่อ ทิ้งข้อมูล
- กันยายน
- กานดา บุคลากร
- การควบคุมคุณภาพงาน
- การควบคุมคุณภาพงานเอกสาร
- การจัดทำรายงานสรุปผลการซ่อมบำรุง
- การจัดเก็บเอกสารตามระบบ
- การทำงานเป็นทีม
- การบริการลูกค้าภายใน
- การประสานงานข้ามหน่วยงาน
- การปรับตัวต่อการเปลี่ยนแปลง
- การมุ่งผลสัมฤทธิ์
- การวางแผนงาน
- การวางแผนงานล่วงหน้า
- การวางแผนงานล่วงหน้าให้ครอบคลุมทั้งรอบ
- การสื่อสาร
- การสื่อสารกับหน่วยงานอื่น
- การเรียนรู้และพัฒนาตนเอง
- การแก้ปัญหาเฉพาะหน้า
- การใช้ระบบงานบัญชีโมดูลใหม่
- การใช้ระบบงานและการแก้ปัญหาเฉพาะหน้า ควรฝึกเพิ่มเติม
- การใช้เครื่องมือวิเคราะห์ข้อมูล
- การใช้เครื่องมือและระบบงาน
- กำลังเปิดหน้าต่างพิมพ์ ·
- กุมภาพันธ์
- ขอเพิ่มสมรรถนะเฉพาะสายงานให้ครบ
- ขอเพิ่มสมรรถนะเฉพาะสายงานให้ครบ — ใส่มาเพียง 2 รายการ
- ขั้นทดสอบ
- ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
- ข้อมูลทั่วไป
- ข้อมูลเอกสาร
- ข้อมูลและผลประเมิน
- ข้อมูลในแบบฟอร์มนี้ยังไม่ได้บันทึก
- ข้าม
- คน
- คลิกเพื่อดูรายการ
- คลิกเพื่อแนบไฟล์ (เลือกได้หลายไฟล์)
- ความรับผิดชอบต่อหน้าที่
- ความรู้เชิงเทคนิคแน่น ถ่ายทอดให้ทีมได้
- ความรู้ในงานที่รับผิดชอบ
- คำอธิบาย
- คำอธิบายสมรรถนะยังไม่ชัดเจน
- คุณไม่มีสิทธิ์ทำรายการนี้
- ค่าเริ่มต้นจากสายอนุมัติที่ตั้งไว้ที่ DOA กลางและผังองค์กร
- ค้นหา...
- ค้นหาเลขที่ / ผู้รับประเมิน / ตำแหน่ง / รายการสมรรถนะ
- งานบัญชีถูกต้องตรงเวลา
- จัดลำดับงานและบริหารเวลาได้เหมาะสม
- จัดเก็บและค้นคืนเอกสารได้ตามมาตรฐาน
- จุดแข็งของพนักงาน
- ชนิดไฟล์ไม่รองรับ
- ชื่อฟังก์ชัน
- ชื่อ–สกุล
- ดาวน์โหลด PDF
- ต.ค.
- ตรวจสอบงานก่อนส่งมอบทุกครั้ง
- ตรวจสอบและยืนยัน
- ตอบสนองคำขอของหน่วยงานอื่นได้ทันเวลา
- ตัดสระบน-วรรณยุกต์-สระล่าง
- ตัดสินใจแก้ปัญหาได้ทันเวลา
- ตำแหน่ง
- ติดต่อประสานงานกับหน่วยงานอื่นได้ราบรื่น
- ตุลาคม
- ต้อง
- ถึง
- ทบทวนผลอีกครั้งในรอบถัดไป 6 เดือน
- ทำงานภาคสนามได้ดี
- ทำงานร่วมกับทีมได้ดี รับผิดชอบงานที่ได้รับมอบหมายจนเสร็จตามกำหนด
- ทำงานให้สำเร็จตามเป้าหมายที่กำหนด
- ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- ทิ้งข้อมูลที่กรอกไว้?
- ที่คุณเกี่ยวข้อง
- ทุกฝ่าย
- ทุกสถานะ
- ทุกแนวทางการพัฒนา
- ธ.ค.
- ธนา มั่งมี
- ธม
- ธันวาคม
- บริษัท ตัวอย่าง จำกัด
- บันทึกผลสำรวจสมรรถนะของตนเอง แล้วส่งให้ผู้ประเมินพิจารณา
- บันทึกผิด
- บันทึกร่างแล้ว ·
- ปข
- ปม
- ประวัติ
- ประวัติ (append-only)
- ประสานงานกับหลายฝ่ายได้ราบรื่น
- ประเมินผิดรอบ
- ประเสริฐ มั่นคง
- ปรับวิธีทำงานตามสถานการณ์ได้
- ปรีชา ขยันดี
- ปิด
- ผลประเมินยังไม่ตรงกับงานจริง
- ผลสำรวจสมรรถนะได้รับความเห็นชอบ
- ผู้จัดการทั่วไป
- ผู้จัดการฝ่ายขาย
- ผู้จัดการฝ่ายทรัพยากรบุคคล
- ผู้จัดการแผนกซ่อมบำรุง
- ผู้จัดการแผนกธุรการ
- ผู้ประเมิน
- ผู้รับประเมิน
- ผู้รับประเมินแก้ไขแล้วส่งใหม่ได้
- ผู้ส่ง
- ฝ่าย
- ฝ่ายขาย
- ฝ่ายทรัพยากรบุคคล
- ฝ่ายบัญชี
- ฝ่ายปฏิบัติการ
- พ.ค.
- พ.ย.
- พนักงานย้ายหน่วยงาน
- พฤ
- พฤศจิกายน
- พฤษภาคม
- พิจารณาในระบบ
- พิมพ์
- ม.ค.
- มกราคม
- มร
- มานี รักเรียน
- มิ.ย.
- มิถุนายน
- มี.ค.
- มีนาคม
- ยกเลิก
- ยกเลิกเอกสาร
- ยกเลิกเอกสาร?
- ยกเลิกเอกสารแล้ว ·
- ยังเป็นร่าง — ส่งอนุมัติเมื่อข้อมูลครบ
- ยังไม่ถึงขั้นนี้
- ยังไม่มีข้อมูล
- ยังไม่มีแบบฟอร์มสำรวจสมรรถนะ
- ยังไม่ส่ง
- ยังไม่เลือกระดับ
- ยังไม่ได้ใส่สมรรถนะหลัก
- ยังไม่ได้ใส่สมรรถนะเฉพาะสายงาน
- ย้อนกลับ
- รอฉันพิจารณา
- รอผล
- รอผู้ประเมินพิจารณา
- รอพิจารณา
- รออนุมัติ
- ระดับการประเมินสมรรถนะ
- ระบุสมรรถนะที่ควรพัฒนาแล้ว แต่ยังไม่ได้เลือกแนวทางการพัฒนา
- รับงานข้ามหน่วยได้ดีมาก และช่วยสอนงานน้องใหม่
- รับผิดชอบงานที่ได้รับมอบหมายจนเสร็จ
- รายการ
- รายการสมรรถนะ
- รายละเอียด
- รายละเอียดเพิ่มเติม
- ร่วมมือกับเพื่อนร่วมงานเพื่อเป้าหมายเดียวกัน
- ร่าง
- ลบไฟล์
- ลองปรับคำค้นหรือล้างตัวกรอง
- ละเอียดรอบคอบในงานเอกสาร
- ลายเซ็น / อนุมัติ
- ลำดับการอนุมัติ
- ล้างตัวกรอง
- วบ
- วันที่ ........./........./.........
- วันที่ประเมิน
- วิชัย บริหารดี
- วิศวกรบริการ
- ส.ค.
- สต
- สถานะ
- สมชาย ใจดี
- สมรรถนะที่ควรพัฒนาเพิ่มเติม
- สมรรถนะที่พนักงานทุกตำแหน่งต้องมี
- สมรรถนะหลัก
- สมรรถนะหลัก (Core Competency)
- สมรรถนะเฉพาะของตำแหน่งงานนี้
- สมรรถนะเฉพาะสายงาน
- สมรรถนะเฉพาะสายงาน (Functional Competency)
- สมหญิง ตั้งใจงาน
- สรุปผลงานรอบปี 2569.pdf
- สรุปผลและแผนพัฒนา
- สร้าง PDF
- สร้างเอกสาร
- สร้างเอกสารใหม่
- สร้างแบบฟอร์ม
- สร้างโดย
- สลับเป็น
- สำนักผู้บริหาร
- สิงหาคม
- สื่อสารชัดเจน
- สื่อสารชัดเจน ตรงประเด็น ทั้งพูดและเขียน
- สใ
- ส่งกลับแก้ไข
- ส่งกลับแก้ไข — กลับเป็นร่าง
- ส่งกลับแก้ไขแล้ว ·
- ส่งอนุมัติ
- ส่งอนุมัติแล้ว ·
- ส่งออก
- ส่งแบบฟอร์มสำรวจสมรรถนะให้พิจารณา?
- ส่งแล้วแก้ไขไม่ได้ — ถ้าผู้ประเมินส่งกลับแก้ไข เอกสารจะกลับเป็นร่างให้แก้แล้วส่งใหม่
- ส่งในระบบ
- อนุชา พัฒนา
- อนุมัติ
- อนุมัติแล้ว
- อบรมเพิ่มเติม
- อพ
- อย่างน้อย 1 รายการ
- อา
- เข้าใจกระบวนการและข้อกำหนดของงาน
- เจ้าหน้าที่ขาย
- เจ้าหน้าที่บัญชี
- เจ้าหน้าที่ประสานงาน
- เดือนถัดไป
- เด้งกลับบน
- เปิดรับความรู้ใหม่และนำมาปรับใช้
- เพิ่มเติม
- เม.ย.
- เมษายน
- เรียนรู้งานใหม่ได้เร็ว
- เลขที่
- เลือก "บันทึกเป็น PDF" ในหน้าต่างพิมพ์ ·
- เลือกประเทศ
- เลือกผู้พิจารณา
- เลือกวันที่
- เลือกวันที่ประเมิน
- เสนอให้เป็นพี่เลี้ยงของพนักงานใหม่ในรอบถัดไป
- เหตุผลที่ยกเลิก
- เห็นชอบ
- เอกสารแนบ
- แก้ปัญหาหน้างานได้เร็ว
- แก้ไขร่าง
- แก้ไขล่าสุด
- แก้ไขเอกสาร
- แก้ไขแบบฟอร์ม
- แก้ไขได้เฉพาะร่างของตัวเอง
- แจ้งผู้รับประเมินว่าเพราะอะไร
- แนบไฟล์เพิ่ม
- แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
- แนวทางการพัฒนา
- แบบฟอร์มทั้งหมด
- แบบฟอร์มสำรวจสมรรถนะ
- แบบเอกสารนี้ยังไม่เปิดใช้งาน
- แผนก
- แผนกขายในประเทศ
- แผนกซ่อมบำรุง
- แผนกธุรการ
- แผนกบัญชีทั่วไป
- แผนกบุคคล
- แล้ว ·
- ใช้ระบบงานได้ถูกต้องครบถ้วน
- ใส่
- ให้เข้าอบรมหลักสูตรการเขียนรายงานเชิงเทคนิค
- ไม่พบรายการ
- ไม่พบรายการที่ค้นหา
- ไม่มีรายการค้าง
- ไม่ยกเลิก
- ไม่อนุมัติ
- — คุณเป็นผู้พิจารณาขั้นนี้

## §10.1 ฟังก์ชันหลักในไฟล์ (anchor สำหรับ test case)

`D()` · `LN()` · `ME()` · `SEC()` · `STEPH()` · `T3()` · `actualRender()` · `addLine()` · `applyRoute()` · `bdById()` · `bdClose()` · `bdFmt()` · `bdIso()` · `bdNav()` · `bdOpenFor()` · `bdPick()` · `bdPlace()` · `bdRender()` · `bdToday()` · `bdToggle()` · `bedate()` · `bedateHTML()` · `blankForm()` · `blankLine()` · `bootIfReady()` · `box()` · `buildSigns()` · `busyLabel()` · `canAct()` · `canCancel()` · `canSee()` · `clearFieldError()` · `closeDrawer()` · `closeModal()` · `closeOverlay()` · `closeRowMenu()` · `cmpPdfBody()` · `cmpPdfDoc()` · `commitRejected()` · `confirmApprove()` · `confirmReason()` · `confirmSubmit()` · `curStep()` · `devList()` · `devPills()` · `dirty()` · `docPill()` · `docPrintData()` · `empChip()` · `empOf()` · `emptyStateHTML()` · `esc()` · `exportCSV()` · `fileRow()` · `findR()` · `fitPdf()` · `fmtD()` · `fmtDate()` · `fmtDateTime()` · `fmtMoney()` · `fmtNumber()` · `fmtSize()` · `gateFiles()` · `genPdf()` · `getRoute()` · `go()` · `goPage()` · `goStep()` · `groupCard()` · `grp()` · `initSearchSelect()` · `initSelects()` · `isAdmin()` · `isOwner()` · `kv()` · `levelLegend()` · `lineCard()` · `lineRows()` · `lineTable()` · `listRows()` · `loadLucide()` · `lvDesc()` · `lvRow()` · `mkLines()` · `mkRec()` · `modalBackdropClick()` · `modalShell()` · `nCore()` · `nFunc()` · `named()` · `navigate()` · `nowIso()` · `onPickADate()` · `onQ()` · `openApprove()` · `openCancel()` · `openDrawer()` · `openModal()` · `openModalCfg()` · `openOverlay()` · `openReject()` · `openRowMenu()` · `openSubmit()` · `openView()` · `pager()` · `persist()` · `pickFiles()` · `pill()` · `portalMenu()` · `positionMenu()` · `preserveRenderState()` · `preservedRender()` · `presetChips()` · `pushAudit()` · `removeFile()` · `removeLine()` · `render()` · `renderDetailTab()` · `renderHistoryTab()` · `renderIcons()` · `renderModal()` · `renderPage()` · `renderPdfTab()` · `renderSignProgress()` · `renderSignTab()` · `renderViewDrawer()` · `renderWizard()` · `reposition()` · `resetFilters()` · `resolveDoa()` · `resolveRole()` · `restoreRenderState()` · `rowClick()` · `saveAndSubmit()` · `saveDraft()` · `searchSelectHTML()` · `setADate()` · `setF()` · `setLevel()` · `setLine()` · `setReasonPreset()` · `setStat()` · `setTab()` · `setText()` · `showDrawer()` · `showToast()` · `signN()` · `sortBy()` · `sortTh()` · `ssClear()` · `ssEscapeReg()` · `ssFiltered()` · `ssGet()` · `ssOnInput()` · `ssOnKey()` · `ssOpen()` · `ssPick()` · `ssPortal()` · `ssPurgePortals()` · `ssRenderList()` · `ssSetText()` · `ssSyncChrome()` · `stText()` · `startWizard()` · `statCard()` · `stepper()` · `sumCard()` · `switchPersona()` · `tShort()` · `tabBtn()` · `thFull()` · `toggleDev()` · `toggleModule()` · `toggleSidebar()` · `toggleUserMenu()` · `tplGet()` · `tplRender()` · `tplSignRows()` · `tryNext()` · `updateShell()` · `validateField()` · `validateMain()` · `viewBanner()` · `wf()` · `withRenderPreservation()` · `wizAttach()` · `wizBack()` · `wizMain()` · `wizNext()` · `wizReview()` · `wordsFor()`

## §11.1 Marker ที่ต้อง wire ตอนพัฒนาจริง

| marker | บริบท |
|---|---|
| `ENG-DOC-NUM` | /* doc_type ประกาศผ่าน doccfg-declaration / mdoc-declaration · เลขรันจาก ENG-DOC-NUM (F-DOCCFG) |
| `DOA-ENGINE-HOOK` | /* DOA-ENGINE-HOOK — resolve จาก DOA entry ของ feature นี้ ณ เวลาส่ง แล้ว snapshot ลง approval_chain (DOA_BRIEF_F-TMP-00 |
| `ENG-DOC-NUM` | /* บันทึก = ENG-DOC-NUM.next() ออกเลขที่ครั้งแรก (DEC-11) · ข้อมูลผู้รับประเมิน snapshot ลงเอกสาร (ตำแหน่ง/แผนก ณ วันที่ |
| `ENG-NOTIFY` | /* ENG-NOTIFY (NTF_BRIEF_F-TMP-005): cmp_cancelled เท่านั้น — doa_pending/doa_result เป็นของ DOA engine ห้ามยิงซ้ำ */ |
| `DOA-ENGINE-HOOK` | doa: MOCK_DOA_RESOLVED 1 ขั้น (role-line-manager · ป้าย "ผู้ประเมิน") dynamic — resolveDoa() = DOA-ENGINE-HOOK · คำตัดสิ |
| `ENG-DOC-NUM` | hooks: ENG-DOC-NUM.next() ตอนบันทึกครั้งแรก (DEC-11 · รหัส CMP) · F-DOCCFG status ก่อนออกเลข (DOC.active) · ENG-NOTIFY c |
| `ENG-NOTIFY` | hooks: ENG-DOC-NUM.next() ตอนบันทึกครั้งแรก (DEC-11 · รหัส CMP) · F-DOCCFG status ก่อนออกเลข (DOC.active) · ENG-NOTIFY c |

## §11.2 QA hook

`window.__QA__` archetype = `Q-form` · qa_hook = True

