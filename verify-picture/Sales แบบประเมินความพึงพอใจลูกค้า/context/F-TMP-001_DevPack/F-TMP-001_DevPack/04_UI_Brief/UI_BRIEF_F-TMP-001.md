# UI_BRIEF — F-TMP-001 แบบประเมินความพึงพอใจลูกค้า (AS-BUILT)
> html-ui-brief v1.1 · สกัดจาก `feature.html` 1:1 (extraction-based) · คู่กับ FRD_F-TMP-001_Pack · ข้อมูลใน HTML เป็นข้อมูลสมมติทั้งหมด

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| HTML | `feature.html` · html-generator-v9.4 Golden Skeleton · `<meta cube-archetype=Q-form>` · `window.__QA__` มี |
| FRD | FRD_F-TMP-001_Pack v1.0 (Mode 0) · P-01..P-03 · API-01..10 |
| DECISIONS | DECISIONS.lock 13 มติ (AI-DEFAULT 10 · VALID 3) |
| Gate | audit.sh FAIL 0 · e2e_standard: **[NO-BROWSER] ยังไม่รัน** · jsdom smoke 26/26 (ไม่ใช่ด่านทางการ) |
| Drift | ดู §11 — prototype-only 4 รายการ · ไม่มี business drift |

## §1 Design Tokens AS-BUILT
CI = CUBE Warm Light (ห้ามแก้) · font `Noto Sans Thai` + `Satoshi` · base 13px/1.55 · ตัวเลข `.num` tabular-nums · Charcoal #111111 · scrollbar บาง 8px (`::-webkit-scrollbar` + `scrollbar-width: thin`) · `scrollbar-gutter: stable`
| Token | ค่า |
|---|---|
| `--c-off-white` | `#FAF8F5` |
| `--c-white` | `#FFF` |
| `--c-text` | `#111` |
| `--c-text-mute` | `#73757B` |
| `--c-text-soft` | `#9A9CA2` |
| `--c-primary` | `#FF3B30` |
| `--c-primary-h` | `#E62E24` |
| `--c-teal` | `#1F9D55` |
| `--c-warning` | `#E8870F` |
| `--c-danger` | `#E62E24` |
| `--c-orange` | `#FF9A1F` |
| `--c-border` | `#DEDAD4` |
| `--c-border-soft` | `#EFEBE6` |
| `--c-primary-08` | `rgba(255,59,48,.08)` |
| `--c-primary-12` | `rgba(255,59,48,.12)` |
| `--c-primary-18` | `rgba(255,59,48,.18)` |
| `--c-teal-08` | `rgba(31,157,85,.10)` |
| `--c-warning-08` | `rgba(232,135,15,.12)` |
| `--c-danger-08` | `rgba(230,46,36,.10)` |
| `--r-sm` | `6px` |
| `--r` | `10px` |
| `--r-lg` | `14px` |
| `--sw` | `224px` |
| `--hh` | `52px` |
| `--sh-md` | `0 4px 8px rgba(17,17,17,.04),0 2px 4px rgba(17,17,17,.06)` |
| `--sh-lg` | `0 10px 30px rgba(17,17,17,.08),0 4px 10px rgba(17,17,17,.04)` |

### z-index map (สูง → ต่ำ)
| z | selector |
|---|---|
| 100 | .toast |
| 90 | .combo-pop |
| 80 | .menu |
| 60 | .modal-backdrop · .modal-overlay |
| 50 | .overlay · .top |
| 40 | .savebar |
| 2 | .st-c · .stepper-item .st-c |
| 1 | .st-item:not(:last-child)::after · .stepper-item:not(:last-child)::after |

## §2 Route Map
| Route | หน้า | หมายเหตุ |
|---|---|---|
| `#/customer-satisfaction` | P-01 รายการ (default — ไม่มี hash จะตั้งให้) | `applyRoute()` ฟัง `hashchange` |
| `#/customer-satisfaction/view/:id` | P-03 drawer ดู (`viewRoute()`) | ไม่มีสิทธิ์/ไม่พบ → toast + กลับรายการ (ไม่เปิด drawer) |
| `#/customer-satisfaction/new` | P-02 drawer สร้าง | doc_type ปิดใช้ → toast + กลับรายการ |
Refresh-safe: route ดูเปิด drawer ใหม่ได้ · ปิด drawer = `setHashSilent()` กลับ `#/customer-satisfaction` โดยไม่ re-render ซ้ำ

## §3 Layout Shell
- `.shell` grid 224px + 1fr · `.sb` sidebar ดำ #111 sticky (กลุ่ม "งานขาย" · "ลูกค้าสัมพันธ์" — เมนูอื่นเรียก `outScope()` = toast)
- `.top` 52px ขาว: breadcrumb ขาย › แบบประเมินความพึงพอใจลูกค้า · ขวา `#topUser` ชื่อ/ตำแหน่ง + `.avatar.person` (วงกลม #111 + icon คน) → `toggleUserMenu()` สลับผู้ใช้ (prototype-only)
- `.page` padding 22/24/40

## §4 Page Anatomy
### P-01 รายการ (`renderPage()`)
- `.ph`: `.ph-title` "แบบประเมินความพึงพอใจลูกค้า (Customer Satisfaction)" · `.ph-sub` + `#ph-count` badge "N รายการ · ร่าง n" (ร่าง 0 ไม่แสดง · ไม่มี scorecard) · `.ph-right` ปุ่ม ส่งออก CSV (`exportCSV()`) + `#btnCreate` สร้างแบบประเมิน (`openCreate()` · disabled เมื่อ `DOC.active` = false)
- `#docInactive` `.note.danger` แถบแบบเอกสารยังไม่เปิดใช้งาน
- `.filter-card`: `.search-wrap` `#q` (`onQ()`) · `#f-status` · `#f-bt` (`setF()`) · รีเซ็ต (`resetFilters()`)
- `.tbl`: `#thead` (`sortTh()` เลขที่/วันที่/ความพึงพอใจโดยรวม) · `#tbody` แถว `tr.is-clickable` → `rowClick()` · คอลัมน์ เลขที่ · วันที่ · ห้าง/ร้านค้า · ประเภทธุรกิจ · ความพึงพอใจโดยรวม · ผู้บันทึก (`personInline()`) · สถานะ (`docPill()`) · ลายเซ็น (`renderSignProgress()`) · ⋮ (`openRowMenu()`)
- `.tfoot`: `#pgSize` (`setSize()` 10/25/50 · default 25) · `#info` · `#pager` (`pager()` / `goPage()`)
- ว่าง: `emptyStateHTML()` "ไม่พบรายการที่ตรงกับเงื่อนไข" / "ยังไม่มีแบบประเมิน"
### P-02 สร้าง/แก้ (`#cdrawer` `.drawer.wide` · `startWizard()` · `renderWizard()`)
- head: `#wzKicker` (สร้างเอกสารใหม่ / แก้ไขเอกสาร) · `#wzTitle` · `#wzStepper` (`stepper()` → `.stepper-item` 3 ขั้น: `STEPS`)
- ขั้น 1 `wizMain()` `.wz-split`: การ์ด `.wz-card` 1 ส่วนที่ 1 (`#f-store` combobox `openCombo()` · `optCards()` ประเภทธุรกิจ/ระยะเวลา `.opt-row` `.opt`) · 2 ส่วนที่ 2 (`scoreRow()` × 9 · `.score-btns` `.sc` 5..1 · `setScore()`) · 3 ส่วนที่ 3 (`#f-sug`) · ขวา `sumCard()` `#sumCard` (sticky)
- ขั้น 2 `wizAttach()` `.upload-zone` → `#filePick` (`pickFiles()` · `gateFiles()`) · `fileRow()` + ลบ `removeFile()`
- ขั้น 3 `wizReview()` แถบไม่มีสายพิจารณา · KV · `scoreTable()` · ข้อเสนอแนะ · ไฟล์
- `#wzFoot` `.dw-footer`: ย้อนกลับ (`wizBack()`) · ยกเลิก (`closeCreate()`) · บันทึกแบบร่าง (`saveDraft()`) · `#btnNext` ถัดไป (`wizNext()`) / `#btnSave` บันทึกและส่ง (`saveAndSubmit()`)
### P-03 ดู (`#drawer` 920 · `openView()` · `renderViewDrawer()`)
- head lean: `.dw-kicker` · `#dwCode` + `#dwPill` · `#dwSub` "ความพึงพอใจโดยรวม x/5" · `#dwActions` `.dw-actions` · `#dwTabs` (`tabBtn()` × 4)
- body `#dwBody`: `renderDetailTab()` (`viewBanner()` · KV · `scoreTable()` · ข้อเสนอแนะ · เอกสารแนบ · ข้อมูลระบบ) · `renderPdfTab()` (`.pdf-slot` `.pdf-frame` srcdoc · `fitPdf()` · `genPdf()`) · `renderSignTab()` (summary + `.tl`) · `renderHistoryTab()`
- foot `#dwFoot` "แก้ไขล่าสุด … · ผู้บันทึก"

## §5 Component Inventory
| Component | anchor | states |
|---|---|---|
| ปุ่ม | `.btn` `.btn-primary` `.btn-secondary` `.btn-ghost` `.btn-link` `.btn-danger` `.btn-success` `.icon-btn` | default · hover · disabled (opacity .5) · busy (`busyLabel()` + `.loader-2` "กำลังดำเนินการ…") |
| pill สถานะ | `docPill()` `.pill` + `.dot` | draft (เทา) · pending (ส้ม) · submitted (เขียว) · cancelled (แดง) |
| คน | `empChip()` `.emp-chip` `.emp-av` (วงกลม #111 + icon คน) · `personInline()` | — |
| ลายเซ็นในตาราง | `renderSignProgress()` `.sig-mini` `.sig-bar` | 0/1 (ร่าง · ไม่มีแถบ) · 1/1 เขียว |
| การ์ดเลือก | `.opt` `.choice-dot` | default · on (ขอบ primary) · invalid (`.opt-row.is-invalid` ขอบแดง + `.err`) |
| ปุ่มคะแนน | `.sc` | default · hover · on (primary) · แถว invalid `.score-row.is-invalid` |
| combobox | `openCombo()` `.combo-pop` `.combo-row` `.combo-empty` · `pickCustomer()` | เปิด (focus/click/พิมพ์) · ว่าง "ไม่พบในทะเบียนลูกค้า — ใช้ชื่อที่พิมพ์ได้เลย" · drop-up เมื่อที่ล่างไม่พอ |
| stepper | `.stepper` `.stepper-item` `.st-c` `.step-dot` `.st-l` | active · done (คลิกย้อน `goStep()`) · รอ |
| ช่องกรอก | `.input` `.select` `textarea.input` | focus (ring primary) · `.is-invalid` |
| แถบ | `.note` `.note.warn` `.note.danger` `.note.ok` | ตามสถานะ (`viewBanner()`) |
| ตาราง | `.tbl` `.score-tbl` `.empty` `.empty-sub` | ว่าง = แผง "ไม่มีข้อมูล" |
| ไฟล์ | `.upload` `.file-row` | ว่าง "ยังไม่มีเอกสารแนบ" |

## §6 Overlay Registry
| Overlay | anchor | ขนาด | z | dismiss |
|---|---|---|---|---|
| drawer ดู | `#ovView` `.overlay` + `#drawer` `.drawer` (`.is-open`) | 920 | 50 | Esc · backdrop `onmousedown` · ปุ่ม x (`closeDrawer()`) |
| drawer สร้าง/แก้ | `#ovCreate` + `#cdrawer` `.drawer.wide` | 1290 | 50 | Esc · backdrop mousedown · x — กรอกค้าง = modal "ทิ้งข้อมูลที่กรอกไว้?" (`closeCreate()`) |
| modal | `#modal` `.modal-backdrop` (`.is-open`) + `#modalCard` `.modal` (`.wide` 640) | 520/640 | 60 | Esc · backdrop `modalBackdropDown()` (mousedown ที่ backdrop เท่านั้น) · ปุ่มยกเลิก/ปิด |
| เมนูแถว ⋮ (row-menu) | `#rowMenu` `.menu` (`openRowMenu()` / `closeRowMenu()`) | 190 | 80 | คลิกที่อื่น (mousedown) · Esc |
| เมนูผู้ใช้ (user-menu) | `#userMenu` `.menu` (`toggleUserMenu()`) | 230 | 80 | คลิกที่อื่น · Esc · prototype-only |
| combobox | `.combo-pop` (portal ที่ body) | ตาม input | 90 | เลือก · คลิกที่อื่น · Esc · scroll นอก popup |
| toast | `#toast` `.toast` (`.is-visible` `.is-ok` `.is-error` `.is-warn`) | ≤420 | 100 | หายเอง 2.8s (`showToast()`) |

## §7 Interaction Spec
- Esc chain (handler keydown ใน document): combobox → เมนู (row/user) → modal → drawer สร้าง → drawer ดู
- click-outside: mousedown ระดับ document ปิด combobox / เมนู · backdrop ทุกตัวใช้ mousedown (ลากจากข้างในออกมาปล่อย = ไม่ปิด)
- soft update: กดคะแนน = แทนเฉพาะแถว (`setScore()`) + `softSums()` · พิมพ์ชื่อร้าน/ข้อเสนอแนะไม่ re-render (focus ไม่หลุด) · เลือกการ์ด = `renderWizardKeepScroll()`
- เลือกร้านจากทะเบียน → เติมประเภทธุรกิจให้ถ้ายังว่าง (`pickCustomer()`)
- ส่ง: `openSubmit()` → `resolveDoa()` → `.slot-row` ต่อขั้น (ค่าเริ่ม 0 ขั้น · DEC-03) → `confirmSubmit()` (busy 450ms · `S.simErr` = จำลองล้มเหลว)
- ยกเลิก: `openCancel()` → `presetChips()` + `#mdReason` → `confirmReason()`
- พิมพ์: `printDoc()` / `genPdf()` iframe ซ่อน · title = เลขที่

## §8 State-Driven UI Matrix
| status | pill | `.dw-actions` (เจ้าของ) | role-mgr-sales | อื่น |
|---|---|---|---|---|
| draft | ร่าง (เทา) | ยกเลิกเอกสาร · แก้ไข · ส่งแบบประเมิน | ยกเลิกเอกสาร | ไม่เห็น |
| submitted | ส่งแล้ว (เขียว) | ยกเลิกเอกสาร | ยกเลิกเอกสาร | ไม่เห็น |
| cancelled | ยกเลิก (แดง) | — | — | ไม่เห็น |
| pending (เฉพาะเมื่อ DOA มีขั้น) | รอพิจารณา (ส้ม) | ยกเลิกเอกสาร | ผู้พิจารณาขั้นปัจจุบัน: ไม่อนุมัติ · อนุมัติ (`.btn-success`) | — |
ไอคอนท้าย: พิมพ์ (`printDoc()`) · ปิด — ทุกสถานะ

## §9 Microcopy (verbatim)
### Toast
- [] ไม่มีรายการให้ส่งออก
- [] ส่งออก ${rows.length} รายการแล้ว
- [] "${n}" อยู่นอกขอบเขต prototype นี้
- [] ไม่พบเอกสาร หรือคุณไม่มีสิทธิ์เห็นเอกสารนี้
- [] เปิดหน้าต่างพิมพ์ไม่ได้
- [] ไม่มีสิทธิ์
- [] ไม่มีสิทธิ์เห็นเอกสารนี้
- [] แบบเอกสาร CSE ยังไม่เปิดใช้งาน (F-DOCCFG)
- [] แก้ไขได้เฉพาะร่างของตัวเอง
- [] กรอกข้อมูลไม่ครบ —
- [] ไฟล์ไม่ผ่านเงื่อนไข:
- [] บันทึกร่าง ${r.code} แล้ว
- [] กรอกข้อมูลไม่ครบ —
- [] ส่งได้เฉพาะร่างของตัวเอง
- [] ข้อมูลยังไม่ครบ — กลับไปแก้ไขก่อนส่ง
- [] เลือกผู้พิจารณาให้ครบทุกขั้น
- [] ส่งไม่สำเร็จ — ระบบขัดข้อง กรุณาลองใหม่ (สถานะเอกสารไม่เปลี่ยน)
- [] ส่ง ${r.code} แล้ว
- [] อนุมัติแล้ว
- [] ไม่มีสิทธิ์ยกเลิกเอกสารนี้
- [] กรุณาระบุเหตุผล
- [] ยกเลิก ${r.code} แล้ว
- [] ไม่อนุมัติ ${r.code} — กลับเป็นร่าง
- [] สลับเป็น
### ปุ่ม
ถัดไป · บันทึกแบบร่าง · ยกเลิก · ยกเลิกเอกสาร · ย้อนกลับ · รีเซ็ต · สร้างแบบประเมิน · ส่งออก CSV · อนุมัติ · ไม่อนุมัติ · ส่งแบบประเมิน · บันทึกและส่ง · ยืนยันส่ง · ทิ้งข้อมูล · แก้ไข · ดาวน์โหลด · พิมพ์
### Placeholder
- ค้นหาเลขที่ / ห้าง-ร้านค้า / ผู้บันทึก...
- พิมพ์ชื่อหรือรหัสลูกค้า เพื่อเลือกจากทะเบียน หรือพิมพ์ชื่อร้านเอง
### ข้อความไทยทั้งหมดที่สกัดได้ (รวมข้อมูล seed สมมติ · หัวข้อคะแนนตามกระดาษ)
(ออกเลขตอนบันทึกครั้งแรก · DEC-09) · 1. ชื่อห้าง/ร้านค้า · 3. ประเภทธุรกิจของบริษัทคู่ค้า · 4. ระยะเวลาที่ทำธุรกิจกับบริษัทคู่ค้า · · ร่าง · ก.ค. · ก.พ. · ก.ย. · กรอกข้อมูลไม่ครบ — · กรุณาระบุชื่อห้าง/ร้านค้า · กรุณาระบุเหตุผล · กรุณาเลือกประเภทธุรกิจ 1 ข้อ · กรุณาเลือกระยะเวลาที่ทำธุรกิจ 1 ข้อ · การจัดการสต็อกสินค้าและการเติมสินค้า · การสนับสนุนด้านการตลาดและส่งเสริมการขาย · การสื่อสารและการให้ข้อมูลข่าวสาร · การแก้ไขปัญหาและการให้บริการหลังการขาย · กำลังดำเนินการ… · ขอสื่อส่งเสริมการขายหน้าร้านเพิ่ม · ขั้น · ข้อมูลที่ยังไม่บันทึกจะหายไป · ข้อมูลยังไม่ครบ — กลับไปแก้ไขก่อนส่ง · ข้อมูลระบบ · ข้อมูลเอกสาร · ข้อมูลแบบประเมิน · ข้อมูลไม่ถูกต้อง · ข้อเสนอแนะ · ควรปรับปรุง · ความตรงต่อเวลาในการส่งสินค้า · ความพึงพอใจโดยรวม · ความพึงพอใจโดยรวมต่อบริษัทคู่ค้า · ความเป็นมืออาชีพของพนักงานขาย/ทีมงาน · คุณภาพของสินค้า/บริการ · ค้าส่งสมมติการค้า · ซูเปอร์มาร์เก็ตสมมติ · ดี · ดีมาก · ต.ค. · ตรวจสอบและยืนยัน · ตรวจให้ครบ 9 หัวข้อแล้วกด "ส่งแบบประเมิน" · ทิ้งข้อมูลที่กรอกไว้? · ธ.ค. · นำออก · น้อยกว่า 1 ปี · บริษัท · บริษัท ตัวอย่างการค้า จำกัด (มหาชน) · บริษัทคู่ค้า · บันทึกซ้ำ · บันทึกและส่ง · ประวัติ · ประเภทธุรกิจ · ประเสริฐ มั่นคง · ปานกลาง · ปิด · ผู้จัดการฝ่ายขาย · ผู้บันทึก · ผู้บันทึก สถานะ ลายเซ็น · ผู้ประเมิน · ผู้ประเมิน · · ฝ่ายขาย · พ.ค. · พ.ย. · พนักงานขาย · พอใช้ · พิมพ์ · พิมพ์/ดาวน์โหลด PDF · พิมพ์ชื่อหรือรหัสลูกค้า เพื่อเลือกจากทะเบียน หรือพิมพ์ชื่อร้านเอง · ภาพหน้าร้าน.jpg · ม.ค. · มากกว่า 5 ปี · มาร์เก็ตทดลอง · มิ.ย. · มี.ค. · ยกเลิก · ยกเลิก: · ยกเลิกเอกสาร · ยังไม่มีแบบประเมิน · ยังไม่สิ้นสุด · ยังไม่ส่ง · ยังไม่ให้คะแนน · ยืนยันส่ง · รอผู้บันทึกกดส่ง · รอพิจารณา · ระยะเวลาที่ทำธุรกิจ · รายละเอียด · ร่าง · ร้านค้าขอยกเลิก · ร้านค้าส่งตัวอย่าง · ร้านตัวอย่างมินิมาร์ท · ร้านสะดวกซื้อตัวอย่าง · ร้านใหม่ยังไม่อยู่ในทะเบียน · ลายเซ็น / อนุมัติ · วันที่ · วันที่ ........./........./......... · วิชัย ขายดี · ส.ค. · สถานะ · สมหญิง ตั้งใจงาน · สร้างเมื่อ · สร้างเอกสาร · ออกเลขที่ · สร้างเอกสารใหม่ · สลับผู้ใช้ (prototype) · สลับเป็น · สาย DOA (snapshot) · สินค้าขาดสต็อกบ่อย ควรปรับรอบเติมสินค้า · ส่งเมื่อ · ส่งแบบประเมิน · ส่งแบบประเมิน (ผู้ประเมิน) — ไม่มีสายพิจารณา (DEC-03) · ส่งแบบประเมิน (ผู้ประเมิน) — ไม่มีสายพิจารณา (DEC-03) · เสร็จสิ้น · ส่งแล้ว · ส่งแล้วแก้ไขไม่ได้ · ลงชื่อผู้ประเมินเป็น "ส่งในระบบ" พร้อมวันเวลา · ส่งในระบบแล้ว · ส่งได้เฉพาะร่างของตัวเอง · ส่งไม่สำเร็จ — ระบบขัดข้อง กรุณาลองใหม่ (สถานะเอกสารไม่เปลี่ยน) · ส่วนที่ 2: การประเมินความพึงพอใจ · ส่วนที่ 3: ข้อเสนอแนะเพิ่มเติม · ห้าง/ร้านค้า · ห้าง/ร้านค้า ประเภทธุรกิจ · ห้างสรรพสินค้าสมมติ สาขาตัวอย่าง · อนุมัติ · อยากให้แจ้งรอบส่งสินค้าล่วงหน้าอย่างน้อย 2 วัน · ออกเมื่อบันทึกครั้งแรก · เงื่อนไขทางการค้า (ราคา โปรโมชั่น การชำระเงิน) · เจ้าหน้าที่ขาย · เปิดหน้าต่างพิมพ์ไม่ได้ · เม.ย. · เมนู · เลขที่ · เลือกจากทะเบียนลูกค้า (Customer) ได้ — ร้านที่ยังไม่อยู่ในทะเบียนพิมพ์ชื่อเองได้ · เลือกผู้พิจารณาให้ครบทุกขั้น · เสร็จสิ้น — เก็บผลประเมินในเอกสารนี้ (ไม่ส่งต่อระบบอื่น · DEC-01/02) · เหตุผล · เอกสารกลับเป็นร่างเลขเดิม ให้ผู้บันทึกแก้แล้วส่งใหม่ (G7) · เอกสารแนบ · แก้ไขร่าง · แก้ไขล่าสุด · แก้ไขเอกสาร · แก้ไขได้เฉพาะร่างของตัวเอง · แบบประเมินความพึงพอใจลูกค้า · แบบฟอร์ม · แบบฟอร์มประเมินความพึงพอใจของ · แบบเอกสาร CSE ยังไม่เปิดใช้งาน (F-DOCCFG) · ไฟล์ไม่ผ่านเงื่อนไข: · ไม่พบรายการที่ตรงกับเงื่อนไข · ไม่พบเอกสาร หรือคุณไม่มีสิทธิ์เห็นเอกสารนี้ · ไม่มี (DEC-03) · ไม่มีข้อเสนอแนะ · ไม่มีรายการให้ส่งออก · ไม่มีสายพิจารณา (DEC-03) · ไม่มีสิทธิ์ · ไม่มีสิทธิ์ยกเลิกเอกสารนี้ · ไม่มีสิทธิ์เห็นเอกสารนี้ · ไม่อนุมัติ · ไม่อนุมัติ — กลับเป็นร่างเลขเดิม · ไฮเปอร์ทดสอบ สาขาหนึ่ง

## §10 Data Binding & BACKEND anchors
| Mock | API (FRD 02) |
|---|---|
| `RECS` (seed 10 ใบ) · `listRows()` · `canSee` | API-01/02 (FN-08) |
| `persist()` · `nextCode()` (ออกเลขตอนบันทึกครั้งแรก) | API-03/04 (FN-01/02) |
| `openSubmit()` · `resolveDoa()` (DOA-ENGINE-HOOK · `MOCK_DOA_RESOLVED` steps [] — TODO: DOA engine) · `confirmSubmit()` | API-05 (FN-03) |
| `confirmReason()` (cancel) | API-06 (FN-04) |
| `docPrintData()` + `tplRender()` + `DOC_TPL` (= print/form.tpl.html) + `PDF_CSS` | API-07 (FN-06) |
| `exportCSV()` | API-08 (FN-07) |
| `pickFiles()` · `gateFiles()` | API-09 (FN-09) |
| `CUSTOMERS` · `openCombo()` | API-10 (Customer master) |
| `ORG.legal_name` · `DOC` (form_code/revision/active) · `ADMIN_ROLE` | Organization · F-DOCCFG · DEC-08 |

## §11 Traceability + Drift Log
| Brief | FRD | HTML anchor |
|---|---|---|
| §4 P-01 | 01_UI P-01 · API-01/08 | `renderPage()` |
| §4 P-02 | 01_UI P-02 · API-03/04/09/10 | `startWizard()` |
| §4 P-03 | 01_UI P-03 · API-02/05/06/07 | `openView()` |
| §8 | 05 §5.2/§5.3 | `canSee` `canEdit` `canCancel` `canAct` |
### ⚠️ Drift Log
| # | ชนิด | รายการ | ข้อเสนอ |
|---|---|---|---|
| D-01 | HTML-only (prototype) | ตัวสลับผู้ใช้ `toggleUserMenu()` / `switchPersona()` | ไม่ build |
| D-02 | HTML-only (prototype) | `window.__QA__` · `S.simErr` | ไม่ build |
| D-03 | HTML-only (hook) | state รอพิจารณา + อนุมัติ/ไม่อนุมัติ เมื่อ DOA มีขั้น | นอก scope (FRD EC-08) — build เมื่อมี enhancement + DOA_BRIEF |
| D-04 | HTML-only (prototype) | เมนูอื่นใน sidebar = toast นอกขอบเขต (`outScope()`) | ไม่ build |

## §12 Diff จากเวอร์ชันก่อน
— ไม่มีใน HTML นี้ (เวอร์ชันแรก)

## §13 💡 ข้อเสนอ (ไม่ใช่ AS-BUILT)
- รายงานคะแนนเฉลี่ยต่อหัวข้อ/ประเภทธุรกิจ (Phase 2) · ลิงก์ให้ร้านค้าตอบเอง (OQ-04)

## 🔍 UI Brief Verification
ดู `reports/brief_check` ใน RUN_LOG (brief_check.py)
