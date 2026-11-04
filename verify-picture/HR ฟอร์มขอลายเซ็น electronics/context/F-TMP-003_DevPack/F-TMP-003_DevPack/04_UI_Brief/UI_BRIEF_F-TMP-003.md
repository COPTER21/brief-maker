# UI BRIEF (AS-BUILT) — F-TMP-003 คำขอมีและใช้ลายเซ็นดิจิทัล (Digital Signature)

## §0 Document Control + Pairing
| | |
|---|---|
| HTML file | `feature.html` · html-generator-v9.3 · archetype **Q-form** (`<meta name="cube-archetype" content="Q-form">`) |
| QA hook | `window.__QA__` มีครบตาม Rule #111 |
| FRD ref | `FRD_F-TMP-003_Pack/` (00–07) · BRD `BRD_F-TMP-003.md` (APPROVED) |
| มติที่ยึด | `DECISIONS.lock.json` (REQ-TMP-003) DEC-01…DEC-17 — AI-DEFAULT 11 ข้อ + VALID 6 ข้อ |
| แบบพิมพ์ | `print/form.tpl.html` + `print/print_config.json` (thai-doc-pdf-generator v2.1 โหมด Replica) |
| สถานะ drift | ไม่มี — HTML สร้างหลัง FORM_SPEC/DECISIONS และ FRD เขียนตาม HTML ที่ผ่าน audit แล้ว |
| ด่านที่ผ่าน | `audit.sh` FAIL 0 · `prune_css.py` แล้ว audit ซ้ำ FAIL 0 · template ใน HTML ตรงกับ `print/form.tpl.html` ทุกไบต์ |
| ด่านที่ยังค้าง | `e2e_standard.py` · `render-check.py` — **[NO-BROWSER]** ต้องรันบนเครื่องที่มี Chromium ก่อน UAT |

---

## §1 Design Tokens AS-BUILT
**Font:** Satoshi + Noto Sans Thai (shell) · Sarabun (เอกสาร A4 ใน iframe)

**CSS variables ทั้งชุด (47 ตัว)**
```
--c-navy --c-navy-2 --c-primary --c-primary-hover --c-teal --c-teal-light
--c-ink --c-mute --c-mute-2 --c-mute-3 --c-placeholder
--c-line --c-line-2 --c-line-3 --c-bg-off --c-success --c-warning --c-danger
--sidebar-w --shell-h
--fs-h1 --fs-h2 --fs-h3 --fs-body --fs-sub --fs-meta --fs-cap --fs-kpi
--sp-xs --sp-sm --sp-md --sp-lg --sp-xl
--r-xs --r-sm --r-md --r-lg --r-full
--z-content --z-sticky --z-shell --z-dropdown --z-backdrop --z-drawer --z-modal --z-popover --z-portal --z-toast
```
CI ล็อก: Navy `#0B1D3A` · Primary `#0B5CFF` · Teal `#00A88E` (ใช้ในเอกสาร A4) · shell ใช้ CUBE Warm Light

**z-index map (ค่าที่ใช้จริงในไฟล์)**
| ชั้น | ค่า |
|---|---|
| เนื้อหา | ค่าเฉพาะจุด `1` `2` `3` |
| sticky / shell | `var(--z-sticky)` · `var(--z-shell)` |
| dropdown (search-select · user-menu) | `var(--z-dropdown)` |
| backdrop | `var(--z-backdrop)` |
| drawer | `var(--z-drawer)` |
| modal | `var(--z-modal)` |
| popover (row-menu · ปฏิทิน พ.ศ.) | `var(--z-popover)` |
| portal overlay root | `var(--z-portal)` |
| toast | `var(--z-toast)` |

---

## §2 Route Map
| route | หน้า | refresh-safe |
|---|---|---|
| `#/dsr` | ทะเบียนคำขอมีและใช้ลายเซ็นดิจิทัล (default) | ✅ |
| `#/dsr/create` | drawer สร้างคำขอ | ✅ เปิด drawer ให้เองผ่าน `applyRoute()` |
| `#/dsr/create/copy-:id` | สร้างจากใบเดิม (เส้นทางมีอยู่ แต่ปุ่มทำซ้ำปิดตาม DEC-11) | ✅ |
| `#/dsr/edit/:id` | drawer แก้ไขร่าง | ✅ |
| `#/dsr/view/:id` | drawer ดูรายละเอียด (แท็บ detail · pdf · sign · history) | ✅ |
ไม่มีสิทธิ์เห็นใบ → ไม่เปิด drawer และกลับไป `#/dsr`

---

## §3 Layout Shell
- `#sidebar` กว้าง `--sidebar-w` · กลุ่มเมนู **HR** → รายการ "ลายเซ็นดิจิทัล" + `#sbBadge` (จำนวนใบที่รอฉันพิจารณา)
- แถบบนสูง `--shell-h` · breadcrumb `Core › HR › คำขอมีและใช้ลายเซ็นดิจิทัล` · ปุ่มแจ้งเตือน `#notifBtn` · การ์ดผู้ใช้ (`#ucName` · `#ucRole` · `#ucAv`) + `#userMenu` (`#personaList` สำหรับสลับผู้ใช้ตัวอย่าง)
- เนื้อหาอยู่ใน `#page-content` · overlay ทั้งหมด portal ไป `#overlay-root`

---

## §4 Page Anatomy

### 4.1 ทะเบียน (`#/dsr`)
```
.page-fill
├─ .ph           หัวหน้า: ชื่อ + จำนวน + ปุ่ม ส่งออก CSV / สร้างคำขอ (#btnCreate)
├─ .alert-row    แถบแดงเมื่อแบบเอกสารยังไม่เปิดใช้งาน
├─ .stats        3 การ์ด (คลิกเพื่อกรอง)
└─ .card.list-card
   ├─ .filter-bar  ค้นหา (#fq) + สถานะ + กรณี + ฝ่าย + ล้างตัวกรอง
   ├─ .table-wrap > .table   9 คอลัมน์
   └─ .table-footer          ตัวแบ่งหน้า .pg-btn
```

### 4.2 drawer สร้าง/แก้ไข (`.drawer.wide`)
```
.dw-head (stepper 3 ขั้น)
.drawer-body.is-soft
└─ .wz-split
   ├─ .wz-main
   │  ├─ .wz-card ① ทำคำขอที่ไหน เมื่อไหร่   → ช่อง "ทำที่" + วันที่ที่ระบบใส่ให้
   │  ├─ .wz-card ② ขอกรณีไหน               → .track-grid.is-3 (.track-card ×3) + #leg-sub (.chip-row ตัวเลือกย่อย) + บล็อกชื่อเดิม/ชื่อใหม่
   │  └─ .wz-card ③ คำรับรองและตัวอย่างลายมือชื่อ → #certBox
   └─ .wz-sum (sticky)  #sumSub · #sumCert
.dw-footer  ย้อนกลับ · ยกเลิก · ถัดไป (#btnNext) / บันทึกแบบร่าง (#btnDraft) + บันทึกและส่งอนุมัติ (#btnSaveSubmit)
```

### 4.3 drawer ดูรายละเอียด (`.drawer`)
```
.dw-head  (ชื่อเอกสาร · เลขที่ · pill สถานะ + pill กรณี · ปุ่มตามสถานะ)
.drawer-tabs  .drawer-tab ×4
.drawer-body
├─ detail   .alert-row + .drawer-section ×7 (ข้อมูลเอกสาร · ผู้ยื่นคำขอ · ความประสงค์ · ชื่อเดิม/ชื่อใหม่ · ตัวอย่างลายมือชื่อ · เอกสารแนบ · ข้อมูลระบบ)
├─ pdf      .pv-bar + .a4 > .pdf-slot > .pdf-frame (iframe srcdoc)
├─ sign     .review-card + .timeline (ขั้น 1..N) + ปุ่มตัดสินในขั้นปัจจุบัน
└─ history  .timeline แบบ append-only
.dw-footer
```

---

## §5 Component Inventory
| component | anchor | โครง | states |
|---|---|---|---|
| การ์ดสถิติ | `.stat` + `statCard()` | ป้าย + ตัวเลข + คำอธิบาย | ปกติ / `is-click` / `is-on` (กำลังกรอง) |
| ตารางทะเบียน | `.table` + `listRows()` | 9 คอลัมน์ · แถวคลิกเปิด drawer | ว่าง (`emptyStateHTML()`) / มีข้อมูล / กรองแล้วไม่พบ |
| แถบลายเซ็น | `.sign-prog` + `renderSignProgress()` | n/N + แถบ | ปกติ / `is-bad` เมื่อไม่สามารถดำเนินการได้ |
| เมนูแถว | `.row-menu` + `openRowMenu()` | แก้ไข · พิมพ์ · ยกเลิกเอกสาร | เปิดบน/ล่างตามพื้นที่จอ |
| การ์ดกรณี | `.track-card` + `setCase()` | ไอคอน + ชื่อ + คำอธิบาย + วงกลมเลือก | ปกติ / `is-on` |
| ชิปตัวเลือกย่อย | `.chip` + `setSub()` | เหตุผล (กรณี 2) / ประเภทการเปลี่ยน (กรณี 3) | ปกติ / `is-on` · กรอบแดงเมื่อยังไม่เลือก |
| บล็อกชื่อเดิม/ชื่อใหม่ | `.leg` + `changeCard()` · `setName()` | การ์ด `.trv` แยกชื่อ/นามสกุล · เปิดเฉพาะส่วนที่เลือกเปลี่ยน | แสดง / ซ่อน / `is-bad` |
| คำรับรอง | `#certBox` + `setCertified()` | checkbox + ข้อความรับรองตามกระดาษ | ยังไม่ติ๊ก (บล็อก) / ติ๊กแล้ว |
| การ์ดสรุปสด | `.wz-sum` + `sumCard()` | ผู้ยื่นคำขอ · ผู้พิจารณาต่อขั้น · ชื่อภาษาอังกฤษ · กรณี · คำรับรอง | อัปเดตสดระหว่างกรอก |
| แท็บ PDF | `.pdf-slot` · `.pdf-frame` + `docPrintData()` · `tplRender()` · `fitPdf()` | iframe A4 | ร่าง (footer มี "ร่าง") / ดำเนินการแล้ว / ไม่สามารถดำเนินการได้ |
| บล็อกลงชื่อในแบบพิมพ์ | `.signs-block` + `buildSigns()` · `tplSignRows()` | ผู้ยื่นคำขอ + 1 ช่องต่อขั้น DOA · แถวละ ≤4 | 2 ช่อง (ค่าเริ่ม) / 7 ช่อง 2 แถว (DOA 6 ขั้น) |
| บล็อกเทียบชื่อ | `.cmp-grid` · `.pd-cell` + `nameBlock()` | ชื่อเดิม → ชื่อใหม่ (ไทย/อังกฤษ) 4 ช่อง | ใช้งาน / `is-off-leg` (ไม่ได้เปลี่ยนส่วนนี้) / ทั้งบล็อกปิดเมื่อไม่ใช่กรณีที่ 3 |
| modal เลือกผู้พิจารณา | `.slot-row` + `openSubmit()` · `confirmSubmit()` | 1 แถวต่อขั้น | ปกติ / `is-invalid` เมื่อยังไม่เลือก |
| ชิปเหตุผล | `.chip-row` + `presetChips()` | ปุ่มเหตุผลสำเร็จรูป | ปกติ / `is-on` |
| เขตแนบไฟล์ | `.upload-zone` + `pickFiles()` · `gateFiles()` | เลือกหลายไฟล์ · ตรวจชนิด/ขนาด | ว่าง / มีไฟล์ / ไฟล์ไม่ผ่าน |

---

## §6 Overlay Registry
| overlay | anchor | ขนาด | dismiss | z |
|---|---|---|---|---|
| drawer ดูรายละเอียด | `#drawer` `.drawer` · `.drawer-panel` | 920px | ปุ่มปิด · Esc · คลิก `#drawerBackdrop` | `var(--z-drawer)` |
| drawer สร้าง/แก้ไข | `#drawer` `.drawer.wide` | ≤1290px | เหมือนข้างบน แต่ถ้ากรอกค้างจะขึ้น modal ยืนยันก่อน (`closeDrawer()`) | `var(--z-drawer)` |
| modal | `#modal` `.modal` (`.is-lg` สำหรับ modal ส่งอนุมัติ) | 480px / 680px | ปุ่มยกเลิก · Esc · คลิก `#modalBackdrop` (ยกเว้นเมื่อพิมพ์เหตุผลไว้แล้ว) | `var(--z-modal)` |
| backdrop | `.drawer-backdrop` · `.modal-backdrop` | เต็มจอ | — | `var(--z-backdrop)` |
| row-menu | `.row-menu` | 180px | คลิกนอก · scroll · เลือกเมนู | `var(--z-popover)` |
| ปฏิทิน พ.ศ. (kit กลาง · ฟอร์มนี้ไม่มีช่องวันที่ให้กรอก) | `.bd-pop` + `bedateHTML()` | 280×320px | คลิกนอก · Esc · เลือกวัน | `var(--z-popover)` |
| search-select list | `.ss-list` | เท่าช่อง | คลิกนอก · Esc · เลือกค่า | `var(--z-dropdown)` |
| user-menu | `#userMenu` `.user-menu` | 260px | คลิกนอก · เลือกผู้ใช้ | `var(--z-dropdown)` |
| toast | `#toast` `.toast` | มุมขวาล่าง | หายเอง | `var(--z-toast)` |
| portal overlay root | `#overlay-root` `.menu-fixed` | — | — | `var(--z-portal)` |

---

## §7 Interaction Spec
- **Esc chain:** popover → modal → drawer (Esc ที่ popover ไม่ทะลุไปปิด drawer)
- **คลิกนอก:** row-menu · search-select · user-menu ปิดทันที · drawer/modal ปิดผ่าน backdrop
- **กรอกค้างแล้วปิด drawer:** ขึ้น modal "ทิ้งข้อมูลที่กรอกไว้?" (ปุ่ม `#btnDiscard`)
- **เปลี่ยนกรณี:** `setCase()` ล้างข้อมูลของกรณีเดิมทิ้งทันที (กรณี 1/2 ต้องไม่มีชื่อเดิม/ชื่อใหม่ค้าง · DEC-13)
- **เปลี่ยนประเภทการเปลี่ยน:** `setSub()` เปิด/ปิดการ์ดชื่อให้ตรงกับที่เลือก และล้างช่องที่ไม่เกี่ยว (DEC-14)
- **อัปเดตแบบนุ่ม (ไม่ rebuild):** ติ๊กคำรับรองแล้ว `#sumCert` เปลี่ยนโดย focus ไม่หลุด · พิมพ์ชื่อใหม่แล้วเคลียร์กรอบแดงอย่างเดียว
- **Positioning:** row-menu วางบน/ล่างตามพื้นที่จอที่เหลือ
- **render ใหม่ปิด popover ก่อน** เพื่อไม่ให้ค้างลอย

---

## §8 State-Driven UI Matrix
| สถานะ | pill | ปุ่มบนหัว drawer | แถบแจ้ง |
|---|---|---|---|
| `draft` | ร่าง (เทา) | เจ้าของ: ยกเลิก · แก้ไข · ส่งอนุมัติ (`#btnSubmitView`) | "ยังเป็นร่าง — ส่งอนุมัติเมื่อข้อมูลครบ" |
| `pending` | รออนุมัติ (เหลือง) | ผู้พิจารณาขั้นปัจจุบัน: ไม่สามารถดำเนินการได้ · ดำเนินการได้ (`#btnApproveView`) · เจ้าของ/admin: ยกเลิกเอกสาร | "รอ … (เจ้าหน้าที่) พิจารณา" |
| `approved` | ดำเนินการแล้ว (เขียว) | พิมพ์ · ดาวน์โหลด PDF | — |
| `rejected` | ไม่สามารถดำเนินการได้ (แดง) | — (ใบกลับเป็นร่างทันทีตาม DEC-08) | เหตุผล + "เอกสารกลับเป็นร่างให้แก้แล้วส่งใหม่ได้" |
| `cancelled` | ยกเลิก (เทา) | — | "ยกเลิกแล้ว — เหตุผล" |

**กรณี:** 1. ขอมีลายเซ็นดิจิทัลครั้งแรก · 2. ขอมีลายเซ็นดิจิทัลใหม่ · 3. ขอเปลี่ยนลายเซ็นดิจิทัล
**คำตัดสินตาม role:** `role-mgr-hr` → ดำเนินการได้ / ไม่สามารถดำเนินการได้ · role อื่น → อนุมัติ / ไม่อนุมัติ (ค่าเริ่ม)

---

## §9 Microcopy (verbatim)

### 9.1 ปุ่ม
`สร้างคำขอ` · `ส่งออก CSV` · `ถัดไป` · `ย้อนกลับ` · `ยกเลิก` · `บันทึกแบบร่าง` · `บันทึกและส่งอนุมัติ` · `แก้ไข` · `พิมพ์` · `ดาวน์โหลด PDF` · `ปิด` · `ยกเลิกเอกสาร` · `ล้างตัวกรอง` · `ทิ้งข้อมูล` · `กลับไปกรอกต่อ` · `ส่งอนุมัติ`

### 9.2 Toast (ข้อความคงที่ — verbatim)
```
ไม่มีการแจ้งเตือนใหม่
แบบเอกสารนี้ยังไม่เปิดใช้งาน
แก้ไขได้เฉพาะร่างของตัวเอง
กรุณากรอกข้อมูลให้ครบถ้วน
แนบไฟล์ไม่สำเร็จ กรุณาลองใหม่อีกครั้ง
ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่
คุณไม่มีสิทธิ์ทำรายการนี้
ทำรายการไม่สำเร็จ กรุณาลองใหม่
บันทึกร่างแล้ว ·
ส่งอนุมัติแล้ว ·
บันทึกผลแล้ว ·
ยกเลิกเอกสารแล้ว ·
ส่งออก
สลับเป็น
```

### 9.3 Placeholder
`ค้นหาเลขที่ / ผู้ขอ / อีเมล / ชื่อใหม่` · `ทำที่ — เช่น สำนักงานใหญ่ กรุงเทพมหานคร` ·
`ชื่อเดิม (ภาษาไทย)` · `ชื่อใหม่ (ภาษาไทย)` · `ชื่อใหม่ (ภาษาอังกฤษ)` · `นามสกุลเดิม (ภาษาไทย)` · `นามสกุลใหม่ (ภาษาไทย)` · `นามสกุลใหม่ (ภาษาอังกฤษ)` ·
`แจ้งผู้ขอว่าเพราะอะไร (ขึ้นในช่อง เนื่องจาก ของแบบพิมพ์)` · `เหตุผลที่ยกเลิก` · `ไม่บังคับ` · `เลือกผู้พิจารณา` · `ทุกสถานะ` · `ทุกกรณี` · `ทุกฝ่าย`

### 9.4 ป้ายช่องและหัวข้อ (คัดตรงจากกระดาษ)
`ทำที่` · `วันที่` · `ข้าพเจ้าชื่อ (ภาษาไทย)` · `นามสกุล (ภาษาไทย)` · `ชื่อ (ภาษาอังกฤษ)` · `นามสกุล (ภาษาอังกฤษ)` · `ตำแหน่ง` · `สังกัดหน่วยงาน` · `Email` · `โทร` ·
`กรณี` · `เนื่องจาก` · `ประเภทการเปลี่ยน` · `โปรดระบุ ชื่อเดิม / ชื่อใหม่` · `ตัวอย่างลายมือชื่อ` · `ข้อมูลเอกสาร` · `ผู้ยื่นคำขอ` · `ความประสงค์` · `ลำดับการพิจารณา` · `ขั้นที่` · `ผู้ส่ง` · `สร้างเอกสาร` · `พิจารณาในระบบ` · `ข้อมูลระบบ`

### 9.5 ข้อความสถานะ / ว่าง / เตือน
```
ยังไม่มีคำขอลายเซ็นดิจิทัล
ยื่นคำขอเพื่อให้เจ้าหน้าที่ออกหรือเปลี่ยนลายเซ็นดิจิทัล (CA) ให้
ไม่พบรายการที่ค้นหา
ลองปรับคำค้นหรือล้างตัวกรอง
รอเจ้าหน้าที่พิจารณา
ค่าเริ่มต้นจากสายอนุมัติที่ตั้งไว้ที่ DOA กลางและผังองค์กร
ใส่สถานที่ที่ทำคำขอ
ติ๊กคำรับรองก่อนส่งคำขอ
ชื่อใหม่ต้องไม่ซ้ำกับชื่อเดิม
นามสกุลใหม่ต้องไม่ซ้ำกับนามสกุลเดิม
ไม่ใช่กรณีขอเปลี่ยนลายเซ็นดิจิทัล — ไม่ต้องระบุชื่อเดิม/ชื่อใหม่
ไม่ได้เปลี่ยนส่วนนี้
ดำเนินการออก/เปลี่ยนลายเซ็นดิจิทัลตามคำขอ
ผู้ขอแก้ไขแล้วส่งใหม่ได้
ยังไม่ถึงขั้นนี้
ยังไม่ระบุ
ข้าม
ทิ้งข้อมูลที่กรอกไว้?
ส่งคำขอลายเซ็นดิจิทัล?
ข้าพเจ้าขอรับรองว่าข้อความข้างต้นเป็นความจริงทุกประการ
```

### 9.6 เดือนไทย (ใช้ในแบบพิมพ์)
`มกราคม` `กุมภาพันธ์` `มีนาคม` `เมษายน` `พฤษภาคม` `มิถุนายน` `กรกฎาคม` `สิงหาคม` `กันยายน` `ตุลาคม` `พฤศจิกายน` `ธันวาคม` ·
`ม.ค.` `ก.พ.` `มี.ค.` `เม.ย.` `พ.ค.` `มิ.ย.` `ก.ค.` `ส.ค.` `ก.ย.` `ต.ค.` `พ.ย.` `ธ.ค.`

### 9.7 ข้อมูลตัวอย่างในต้นแบบ (สมมติทั้งหมด — ห้ามใช้ข้อมูลจริงของลูกค้า)
ชื่อ: `สมชาย ใจดี` · `กานดา บุคลากร` · `มานี รักเรียน` · อังกฤษ: `Somchai` `Jaidee` · อีเมลตัวอย่าง `somchai.j@example.co.th` · โทร `02-000-0000 ต่อ 123`
สถานที่: `สำนักงานใหญ่ กรุงเทพมหานคร` · `สำนักงานสาขาภาคตะวันออก นิคมอุตสาหกรรมอมตะซิตี้ จังหวัดชลบุรี`
เหตุผลตัวอย่าง: `ยังไม่ได้แนบหลักฐานการเปลี่ยนชื่อ-นามสกุล` · `ยื่นซ้ำกับคำขอก่อนหน้า` · ไฟล์แนบ: `ใบสำคัญการเปลี่ยนชื่อ.pdf`

---

## §10 Data Binding & BACKEND anchors
| จุดในต้นแบบ | mock ในไฟล์ | API จริง (02_API) |
|---|---|---|
| รายการทะเบียน | `RECS` + `listRows()` | `GET /api/hr/digital-signature-request` |
| ใบเดียว | `findR()` | `GET /api/hr/digital-signature-request/{id}` |
| บันทึกร่าง / แก้ไข | `persist()` | `POST` / `PUT /api/hr/digital-signature-request` |
| ส่งอนุมัติ | `confirmSubmit()` | `POST …/{id}/submit` |
| ดำเนินการได้ | `confirmApprove()` | `POST …/{id}/approve` |
| ไม่สามารถดำเนินการได้ / ยกเลิก | `confirmReason()` | `POST …/{id}/reject` · `POST …/{id}/cancel` |
| ผู้ใช้/ผังองค์กร | `EMP` · `empOf()` | `GET /api/hr/employees` |
| สายอนุมัติ | `MOCK_DOA_RESOLVED` · `resolveDoa()` · marker `DOA-ENGINE-HOOK` | `GET /doa/resolve` (F-DLG-001) |
| เลขที่เอกสาร + สถานะเปิดใช้ | `DOC` (prefix `DSR` · `DOC.active`) · marker `ENG-DOC-NUM` | F-DOCCFG + ENG-DOC-NUM |
| แจ้งเตือน | marker `ENG-NOTIFY` (`dsr_cancelled` · `dsr_name_change_requested`) | ENG-NOTIFY |
| ข้อมูลแบบพิมพ์ | `docPrintData()` → `tplRender()` | `GET …/{id}/pdf` (render ฝั่ง server จาก template เดียวกัน) |
| ส่งออก CSV | `exportCSV()` | `GET …/export.csv` |
| จำลอง API ล้ม | `commitRejected()` · `window.__QA__.sim` | — (prototype เท่านั้น) |

**กฎที่ dev ห้ามพลาด:** จำนวนขั้นและชื่อผู้พิจารณาต้องมาจาก DOA เสมอ — ในต้นแบบไม่มี array ของ role ที่ fix ไว้ และมี marker `DOA-ENGINE-HOOK` กำกับจุดที่ต้องต่อ engine

---

## §11 Traceability + Drift Log
| ส่วนของ UI | FRD | มติ |
|---|---|---|
| ช่องทั้งหมดในขั้น 1 | 01_UI §2.1 · 04_DB §1 | DEC-06 |
| เลือกกรณีได้ 1 ข้อ + ตัวเลือกย่อยบังคับ | 03_LOGIC FN-02 | DEC-16 |
| ช่องชื่อเปิดเฉพาะกรณีที่ 3 | 03_LOGIC FN-03 | DEC-13 |
| บังคับเฉพาะส่วนที่เลือกเปลี่ยน | 05_RULES VR-05/VR-06/VR-07 | DEC-14 |
| ชื่อเดิมภาษาอังกฤษจากทะเบียน | 03_LOGIC FN-03 | DEC-15 |
| คำรับรองก่อนส่ง | 03_LOGIC FN-05 | DEC-07 |
| modal เลือกผู้พิจารณา 1 แถวต่อขั้น | 03_LOGIC FN-06 | DEC-03 |
| คำตัดสินตาม role | 03_LOGIC FN-11 · 05_RULES BR-13 | DEC-07 |
| ไม่สามารถดำเนินการได้ = กลับเป็นร่าง | 03_LOGIC FN-08 | DEC-08 |
| การมองเห็น | 03_LOGIC FN-10 · 05_RULES §4 | DEC-09 |
| แท็บ PDF | 03_LOGIC FN-11 | DEC-07 · DEC-12 |
| ส่งออก CSV · ไม่มีปุ่มทำซ้ำ | 03_LOGIC FN-12 · 05_RULES BR-11 | DEC-11 |

**Drift Log:** ไม่มีรายการ

---

## §12 Diff จากเวอร์ชันก่อน
ไม่มี — นี่เป็นต้นแบบรอบแรกของ feature นี้

---

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
1. ทะเบียนผู้ถือลายเซ็นดิจิทัล + แจ้งเตือนก่อนใบรับรองหมดอายุ (ลดกรณีที่ 2 "ลายเซ็นหมดอายุ")
2. บล็อกการยื่นซ้ำขณะใบเดิมยังค้าง — รอคำตอบ OQ-03
3. บังคับแนบหลักฐานการเปลี่ยนชื่อ-นามสกุลในกรณีที่ 3 — รอคำตอบ OQ-04
4. ให้ระบบเปิดคำขอแก้ชื่อในทะเบียนพนักงานให้อัตโนมัติเมื่อใบนี้ผ่าน — ต้องแก้ DEC-01/DEC-02 ก่อน
5. ปุ่ม "ทำซ้ำ" (เส้นทาง `#/dsr/create/copy-:id` พร้อมใช้อยู่แล้ว) เปิดได้ทันทีถ้าลูกค้าต้องการ (ตอนนี้ปิดตาม DEC-11)
