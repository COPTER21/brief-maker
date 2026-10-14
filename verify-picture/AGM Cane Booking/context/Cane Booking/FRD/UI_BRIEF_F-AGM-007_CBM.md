# UI BRIEF — F-AGM-007 Cane Booking Management (CBM) (AS-BUILT)

## §0 Document Control + Pairing
| Field | Value |
|---|---|
| Source HTML | `cane-booking-management.html` (v1.0, 2026-07-21 — html-generator-v6, audit FAIL=0 · WARN=2 inherited: font-size + custom stepper) |
| FRD Pack | `FRD_F-AGM-007_Pack/` (7 ไฟล์ STANDARD) — paired ✅ |
| BRD | BRD_F-AGM-007 APPROVED (LOCK-01..11) |
| Reverse | RIF v2 + invariants.md LOCKED 🔒 (synthesized v1.1→v1.7, AS-BUILT = legacy zip2 ≈ v1.7) |
| Cross-module | read Quota/Season/Crop snapshot + Debt Mgt (outstanding) · **system events** check-in/receiving/payment (non-manual) ปิดแกน B + payment |
| กติกา | ทุก claim ชี้ anchor ได้ (selector/function/ข้อความ verbatim) — HTML = source of truth |

## §1 Design Tokens AS-BUILT
เหมือน F-AGM-001..006 100% (CUBE Warm Light — Ivory #FAF8F5 · Charcoal #111 · Red #FF3B30 action · Orange #FF9A1F connection = snapshot card + ลิงก์โควตา). Fonts Satoshi + Noto Sans Thai · Lucide 0.469.0 loader (`loadLucide`/`bootIfReady` fallback 5s). Thai optical centering (Rule #36). Z-index: Toast 80 · ss-list 70 · modal 60 · drawer 50 · sidebar/shell 20/19 · sticky th 3.

## §2 Route Map
| Route | หน้า | Handler |
|---|---|---|
| `#/bookings` (default) | P-01 list | `render()` (`getRoute()` บรรทัด 266 default 'bookings' · `navigate`) |
| `#/bookings/:booking_id` | P-01 + detail drawer (P-02) | parse `parts[1]` → `findBooking()` → `mountViewDrawer()` refresh-safe · `openView(id)=navigate('bookings/'+id)` · ไม่พบ → toast "ไม่พบข้อมูลการจองที่เลือก" + กลับ list |
Overlay ไม่ผูก route: create drawer (`openForm`) + reason modal (`openReasonModal`)

## §3 Layout Shell
Sidebar 232px: module เกษตรกรรม → สมาชิก/โควตา/แปลงที่ดิน/รอบปลูก/สัญญาส่งอ้อย/แบบสำรวจ (disabled), **จัดการจองรอบส่งอ้อย (is-active)** + system→Settings · Breadcrumb "เกษตรกรรม › จัดการจองรอบส่งอ้อย" · User chip "สมพร วงศ์ทะเบียน / เจ้าหน้าที่จองรอบ · WKN" · `.content` fluid

## §4 P-01 Booking List (`render()` → `#page-content`)
```
.ph h1 "จัดการจองรอบส่งอ้อย" + count + sub "ทะเบียนการจองส่งอ้อย · สถานะ 3 แกน (อนุมัติ · ตัด&ขนส่ง · ชำระเงิน) · พิมพ์เอกสาร"
    .ph-actions: [ตรวจสอบที่เลือก (N) disabled@0] [สร้างการจอง primary ขวาสุด]
.stats 4: การจองทั้งหมด(sub ทุกสถานะในระบบ) · รออนุมัติ(รอเจ้าหน้าที่ตรวจสอบ) · กำลังตัด/ขนส่ง(แกนตัด&ขนส่งยังไม่ปิด) · เสร็จสิ้น(จ่ายเงินเสร็จแล้ว)
.card
 ├ filter-bar: search (debounce — booking/quota/farmer/ทะเบียนรถ) + select ฤดูกาล + select การอนุมัติ + select ตัด&ขนส่ง (มี "ยังไม่เริ่ม") + select การชำระเงิน (มี "ยังไม่เริ่ม") + ล้างตัวกรอง
 ├ bulk-bar (waiting selected): เลือก N + ตรวจสอบที่เลือก + ยกเลิกการเลือก
 ├ table คอลัมน์: ☑(waiting) · เลขจอง(mono แดง link) · เกษตรกร/โควตา · ฤดูกาล · วันเวลา/เลน · รถ(ทะเบียน) · **การอนุมัติ** (pill/-) · **ตัด&ขนส่ง** (pill/- derived) · **การชำระเงิน** (pill/-) · **ความคืบหน้า** (combined pill) · ดาวน์โหลด (ใบสั่งตัด/ใบส่งอ้อย ตาม gate)
 │  row .is-clickable → openView(booking_id) · sortable: booking_id/booking_datetime/updated_at
 └ footer: pagination + "X – Y จาก Z รายการ"
```
Empty: "ยังไม่มีการจอง" +สร้าง · filter empty: "ไม่พบรายการที่ค้นหา — ลองปรับคำค้นหรือล้างตัวกรอง" + ล้างตัวกรอง

## §5 Component Inventory (R4 states)
| Component | Anchor | States |
|---|---|---|
| **3-axis pills ⭐** | `displayApproval()`/`displayCut()`/`displayPayment()` | A: รออนุมัติ(warn)/อนุมัติรอบจองแล้ว(success)/ปฏิเสธ(danger)/ยกเลิก(neutral) · B(derived): "-"(ยังไม่เริ่ม)/รอส่งอนุมัติตัด/รออนุมัติตัด/รอตัด/รอจัดส่ง/อยู่ระหว่างจัดส่ง · C: "-"/รอทำจ่าย/เสร็จสิ้น |
| **Combined progress ⭐** | `combinedProgress()`/`combinedPill()` | 10-step derived: รออนุมัติ→อนุมัติรอบจองแล้ว→รอส่งอนุมัติตัด→รออนุมัติตัด→รอตัด→รอจัดส่ง→อยู่ระหว่างจัดส่ง→รอผลการเท→รอทำจ่าย→เสร็จสิ้น (+ ปฏิเสธ/ยกเลิก terminal) |
| **10-step stepper ⭐** | detail `renderViewDrawer` "ความคืบหน้ารวม (10 ขั้น)" | dot: done(เขียว)/current(แดง+เลข)/future(เทา+เลข) · 🔒 บน 3 ขั้น system (รอผลการเท/รอทำจ่าย/เสร็จสิ้น) |
| Quota search | `initQuotaSearch/selectBookingQuota/clearBookingQuota` · `findQuota/cropsForQuota` | เลือกโควตา → farmer snapshot + debt outstanding หรือ "ไม่มีแฟ้มลูกหนี้" |
| Debt field | `.field` debt_deduction_percent | 0-100 · นอกช่วง "กรุณาใส่ค่าที่ถูกต้อง" · note offset จริงที่ Payment |
| **System-event sim ⭐** | `simCheckin/simReceiving/simPayment` | ปุ่มจำลอง (เฉพาะทางเข้าสู่ system state) → รอผลการเท / ปิดแกน B+รอทำจ่าย / เสร็จสิ้น · badge "ระบบกำหนด" |
| Status pill | `statusPill()`/`combinedPill()` | success/warning/danger/neutral/info |
| Snapshot card | renderFormDrawer/renderViewDrawer | teal "โควตา [QT] · [farmer]" + ลิงก์โควตา |
| Toast | `showToast` | success/info/warning/error |

## §6 Overlay Registry
| Overlay | ขนาด | Mount | z |
|---|---|---|---|
| Detail drawer (P-02) | 920px | `mountViewDrawer()`/`renderViewDrawer()` — stepper + 3-axis + ข้อมูลจอง + รายละเอียดตัด/จัดส่ง + system-event panel + prints + actions | 50 |
| Create drawer | 920px | `openForm('create')`/`renderFormDrawer()` — quota search + รอบเวลา/เลน + รถ + ประเภทบิล + หักหนี้ % | 50 |
| Reason modal | 440px | `openReasonModal()`/`renderReasonModal()` — reject/cancel/void reason บังคับ + `doReverse()` | 60 |

## §7 Interaction Spec
- **No-skip pipeline ⭐:** ทุก action re-check precondition. `approveBooking`(A=verified→Gate B) · `sendCutApproval`(verified&cut=null→awaiting_cut_approval) · `approveCut`(→awaiting_cutting) · `finishCut`(→awaiting_dispatch) · `startDispatch`(→dispatching + dispatch_started_at) · ข้ามขั้น → toast "ไม่สามารถข้ามขั้นตอนได้"
- **System-controlled states ⭐:** รอผลการเท/รอทำจ่าย/เสร็จสิ้น เข้าได้เฉพาะ `simCheckin/simReceiving/simPayment` (ไม่มีปุ่ม manual) · manual/out-of-order → toast "สถานะนี้ระบบจะอัปเดตให้อัตโนมัติ เมื่อข้อมูลจากระบบอื่นเสร็จสิ้น"
- **Reverse/void ⭐:** `openReasonModal`→`doReverse` void 1 ขั้น + reason บังคับ ("กรุณาระบุเหตุผล") · block เมื่อ completed (read-only)
- **Print gate ⭐:** `canPrintCut()` (≥awaiting_cutting) → `printCut` CBM-CUT + QR · `canPrintDlv()` (≥awaiting_dispatch) → `printDlv` CBM-DLV + QR · ก่อน gate → toast "ต้องอนุมัติตัดก่อน…" / "ต้องอยู่สถานะรอจัดส่งขึ้นไป…"
- validation create: quota/รอบ/เลน/รถ required ("กรุณากรอกข้อมูลให้ครบถ้วน") · คนขับ ("กรุณาระบุคนขับ") · ตัน>0 ("กรุณากรอกปริมาณคาดส่ง") · debt 0-100
- Esc chain · debounce · Render preservation (`preserveState/restoreState`) · Row click=view · Double-submit guard (`submitting`)

## §8 State-Driven UI Matrix (3-axis → combined)
| Combined | แกน A | แกน B | แกน C | Detail actions |
|---|---|---|---|---|
| รออนุมัติ | waiting_for_verify | - | - | อนุมัติ · ปฏิเสธ · ยกเลิก |
| อนุมัติรอบจองแล้ว | verified | null | - | ขออนุมัติตัด · ย้อนสถานะ |
| รอส่งอนุมัติตัด (derived) | verified | null | - | ขออนุมัติตัด |
| รออนุมัติตัด | verified | awaiting_cut_approval | - | อนุมัติตัด (+ พิมพ์ใบสั่งตัด disabled) |
| รอตัด | verified | awaiting_cutting | - | จบการตัด · พิมพ์ใบสั่งตัด |
| รอจัดส่ง | verified | awaiting_dispatch | - | เริ่มจัดส่ง · พิมพ์ใบสั่งตัด · พิมพ์ใบส่งอ้อย |
| อยู่ระหว่างจัดส่ง (derived) | verified | dispatching | - | (รอ system) · ย้อนสถานะ · prints · **จำลอง: เช็คอินโรงงาน** |
| รอผลการเท 🔒 | verified | dispatching(checkin) | - | (system) **จำลอง: รับอ้อยเสร็จ** |
| รอทำจ่าย 🔒 | verified | closed_at | awaiting_payment | (system) **จำลอง: จ่ายเงินเสร็จ** |
| เสร็จสิ้น 🔒 | verified | closed_at | completed | read-only (lock) |
| ปฏิเสธ/ยกเลิก | rejected/cancelled | - | - | read-only + reason box |

## §9 Microcopy (verbatim)
**ปุ่ม:** `สร้างการจอง` · `ยืนยันสร้าง` · `อนุมัติ` · `ปฏิเสธ` · `ยกเลิก` · `ขออนุมัติตัด` · `อนุมัติตัด` · `จบการตัด` · `เริ่มจัดส่ง` · `ย้อนสถานะ` · `พิมพ์ใบสั่งตัด` · `พิมพ์ใบส่งอ้อย` · `ปิด` · `ยืนยันย้อนสถานะ`
**Sim events:** `จำลอง: เช็คอินโรงงาน` · `จำลอง: รับอ้อยเสร็จ` · `จำลอง: จ่ายเงินเสร็จ` · badge `ระบบกำหนด`
**Combined labels:** `รออนุมัติ` · `อนุมัติรอบจองแล้ว` · `รอส่งอนุมัติตัด` · `รออนุมัติตัด` · `รอตัด` · `รอจัดส่ง` · `อยู่ระหว่างจัดส่ง` · `รอผลการเท` · `รอทำจ่าย` · `เสร็จสิ้น` · `ปฏิเสธ`
**Toast:** `สร้างการจองสำเร็จ — [เลขจอง]` · `อนุมัติแล้ว` · `ดำเนินการแล้ว` · `ย้อนสถานะแล้ว` · `ไม่สามารถข้ามขั้นตอนได้` · `สถานะนี้ระบบจะอัปเดตให้อัตโนมัติ เมื่อข้อมูลจากระบบอื่นเสร็จสิ้น` · `กรุณาระบุเหตุผล` · `กรุณากรอกข้อมูลให้ครบถ้วน` · `กรุณาระบุคนขับ` · `กรุณากรอกปริมาณคาดส่ง` · `ไม่พบรายการที่ค้นหา`
**Print gate:** `ต้องอนุมัติตัดก่อน จึงจะพิมพ์ใบสั่งตัดได้` · `ต้องอยู่สถานะรอจัดส่งขึ้นไป จึงจะพิมพ์ใบนำส่งได้`
**Quota search:** placeholder `พิมพ์เลขโควตา หรือ ชื่อเกษตรกร` · help `ระบบจะดึงข้อมูลเจ้าของโควตา + ยอดหนี้ค้างให้อัตโนมัติ` · debt `ไม่มีแฟ้มลูกหนี้`
**Bill/debt:** `บิลเขียว`/`บิลขาว` · หักหนี้ note `การหักหนี้จริงจะคำนวณตอน Payment (ยอดจ่ายได้ × %/100) · ยอดหนี้ค้างดึงจาก Debt Mgt`

## §10 Data Binding & BACKEND anchors
| Anchor | API |
|---|---|
| `QUOTAS` const + `findQuota/cropsForQuota` ⭐ | **API-D debt + API-02 create-read (F-AGM-002/004/core read)** |
| `state.records` seed (`seedBooking`) | API-01 GET /cbm/bookings (+ derived phase_flags) |
| `captureForm/submitForm` create | API-02 POST (FN-01) + Idempotency-Key |
| `approveBooking/doReverse` (reject/cancel) | API-A1/A2/A3 (FN-A + guardTransition) |
| `sendCutApproval/approveCut/finishCut/startDispatch` | API-B1..B4 (FN-B no-skip) |
| `simCheckin/simReceiving/simPayment` ⭐ | API-E1/E2/E3 (FN-E ingestSystemEvent, non-manual, idempotent) |
| `doReverse` (void) | API-V (FN-V revert 1 ขั้น + reason) |
| `printCut/printDlv` | API-P1/P2 (FN-P doc-generator + QR, gate) |
| detail history | API-12 |
Mock: **10 bookings** CBM-2568-0000001..0000010 (ครอบทั้ง 10 combined states เรียงตาม pipeline + 1 ปฏิเสธ) · **4 quotas** QUO-2568-0001..0004 (2 มีหนี้ค้าง · 2 "ไม่มีแฟ้มลูกหนี้") · doc no CBM-CUT/CBM-DLV-2568-000000N

## §11 Traceability + Drift Log
| FRD | HTML anchor | Brief |
|---|---|---|
| 01_UI P-01 list 3-axis | render → #page-content + displayApproval/Cut/Payment | §4/§5 |
| 01_UI P-02 detail (stepper) | renderViewDrawer + combinedProgress + 10-step | §6/§5 |
| 01_UI OV create | openForm + initQuotaSearch + debt | §6/§7 |
| 01_UI OV reason | openReasonModal + doReverse | §6 |
| 02_API A1..A3 | approveBooking/doReverse | §10 |
| 02_API B1..B4 (no-skip) | sendCutApproval/approveCut/finishCut/startDispatch | §7/§10 |
| 02_API E1..E3 (system) | simCheckin/simReceiving/simPayment | §7/§10 |
| 02_API P1/P2 (gate) | canPrintCut/canPrintDlv + printCut/printDlv | §7/§10 |
| 03_LOGIC FN-06 derived | combinedProgress (รอส่งอนุมัติตัด/อยู่ระหว่างจัดส่ง/รอผลการเท) | §5/§8 |
| 05_RULES state machine | detailActions + no-skip guards | §8 |
| 06_TESTS AC-01..36 / XT-01..05 | ครบ (see §8) | §8/§10 |

### ⚠️ Drift Log
| # | รายการ | ทาง | หมายเหตุ |
|---|---|---|---|
| D-01 | Stats 4 การ์ด | HTML-only | ตรง BRD §18 |
| D-02 | Quota/Season/Crop/Debt อ่านจาก mock | HTML sim | ระบบจริง = ENG-EXT-SRC read F-AGM-002/004 + Debt Mgt |
| D-03 | System events = ปุ่มจำลอง (simCheckin/Receiving/Payment) | HTML sim | ระบบจริง = ENG-EVT รับ event จริง (check-in/receiving/payment) idempotent |
| D-04 | Print = alert/HTML preview | HTML sim | ระบบจริง = ENG-PDF A4 ไทย + QR (CBM-CUT/CBM-DLV) |
| D-05 | optimistic CONFLICT (EC-16) ไม่มี demo (single-user) | FRD-only | 409 ที่ server (row_version) |
| D-06 | ไม่มี hard 'dispatched' — ปิดแกน B ด้วย closed_at | AS-BUILT | invariants §7 (v1.3 removed) |
| D-07 | verified label = "อนุมัติรอบจองแล้ว" | AS-BUILT | invariants §7 (v1.5 rename) |

## §12 Diff จากเวอร์ชันก่อน
เทียบ legacy (booking/etcd zip — Next.js ≈ v1.7) + spec chain v1.1→v1.7: คงไว้ 100% (LOCK-01) — 3-axis state machine, no-skip pipeline, system-controlled states via event, debt %, 2 prints + QR, void + reason, optimistic lock · **สังเคราะห์ final** (invariants §0/§7): ETCD→CBM rename · ลบ 'dispatched' (v1.3) · verified→"อนุมัติรอบจองแล้ว" (v1.5) · derived "รอส่งอนุมัติตัด" (v1.5) · "รอผลการเท" (v1.6) · "อยู่ระหว่างจัดส่ง"+"เริ่มจัดส่ง" (v1.7) → **10-step visible** · CI → CUBE Warm Light · เพิ่ม stats + snapshot + combined stepper + audit governance

## §13 💡 ข้อเสนอ
1. snapshot ลิงก์โควตา deep-link ไป Quota detail จริง (ตอนนี้ mock)
2. Print preview → PDF จริง + QR verify `/:id/view` (ตอนนี้ preview)
3. System-event log panel แสดง event_id + timestamp จริงจากระบบภายนอก (idempotency audit)
4. "ยังไม่เริ่ม" filter ต่อแกน → chips สรุปจำนวนต่อ phase บน list
