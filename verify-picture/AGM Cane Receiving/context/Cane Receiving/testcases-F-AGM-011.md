# AI Test Cases — F-AGM-011 Cane Receiving (การรับอ้อย / ออกใบรับอ้อย)

ชุด test case สำหรับ **AI agent (browser-use / vision)** รันบน prototype `cane-receiving-management.html`
ทุก anchor คือข้อความที่เห็นบนจอจริง (ยืนยันกับ FRD 06_TESTS §6.10 microcopy + 05_RULES + สแกน prototype แล้ว) · Expected เช็คได้ด้วยตา
เคสที่ prototype จำลองไม่ได้ (**Factory dump API (v2) จริง** · **CBM awaiting_payment + ปลดเหรียญชั่งจริง** · **PDF A4+QR จริง (server render)** · **Sync All idempotency 409 / ไม่รันซ้อน** · **Receiving = SoT ส่ง net_weight+cane_type ให้ Payment** · **void → CBM awaiting_dump_result reversal** · **ไฟล์ CSV จริง** · **filter ประเภทอ้อย + net cross-check debug** · **cane type ไม่รู้จัก → Payment adjustment 0**) ติด `(ต้อง simulate)` — รันซ้ำกับระบบจริงตอน SIT

> ⚠ **หมายเหตุ dump v2:** prototype fix ให้ **ดึงผลการเท (Auto) สำเร็จเสมอ** (deterministic) → card ล็อกค่า `05 - อ้อยสด (Fresh Cane)` · น.น.รวม `32,000.00` · น.น.รถเบา `12,000.00` · น.น.อ้อยสุทธิ `20,000.00` · **ไม่มี CCS** (ย้ายไป Payment) · ปุ่ม **จำลองไม่พบผล** = force fail → เข้า Manual mode. dump API จริง / net cross-check = `(ต้อง simulate)`

> ⚠ **หมายเหตุ manual validation:** ปุ่ม **ออกใบรับอ้อย** (footer) จะ **disabled จนกว่า** manual จะกรอกครบ 2 ช่อง (น.น.สุทธิ + เหตุผล) — ดังนั้น `กรุณากรอกน้ำหนักสุทธิ` (VR-01) / `กรุณากรอกเหตุผลการกรอกด้วยตนเอง` (VR-03) เป็น server-guard ที่ปุ่ม-disable บังคับไว้แล้ว (observable = ปุ่ม disabled) · ส่วน `กรุณากรอกน้ำหนักสุทธิเป็นจำนวนไม่ลบและ 2 ตำแหน่ง` (VR-02) reachable เต็ม (ค่าติดลบ / 3 ตำแหน่ง)

> ⚠ **หมายเหตุ role:** prototype fix `CURRENT_ROLE = 'เจ้าหน้าที่รับอ้อย'` · `canWrite = true` เสมอ · ปุ่ม ออกใบ/Sync All/Void แสดงครบ · RBAC ฝั่ง Viewer (ไม่เห็น Sync All/create) + Supervisor/Admin (manual override/void) = `(ต้อง simulate)` ที่ SIT

## Meta

| Field | Value |
|---|---|
| Feature ID | F-AGM-011 (AGM/RECEIVING — การรับอ้อย · ออกใบรับอ้อย) |
| App entry | เปิดไฟล์ `cane-receiving-management.html` ใน browser (Chrome desktop ≥1280px) |
| Routes | `#/receivings` (tab **รอผลเท** — default) · `#/receivings/issued` (tab **เทแล้ว**) · `#/receivings/void` (tab **ยกเลิก**) · `#/receivings/:id` (detail drawer 680px, refresh-safe) |
| Top tabs (page-level) | **รอผลเท** (Draft) · **เทแล้ว** (Issued) · **ยกเลิก** (Void) |
| Overlays | Issue drawer 920px (openForm — ผูก state) · detail drawer 680px (ผูก route) · modal: syncresult / void / pdf / qr / search |
| ที่มา | FRD_F-AGM-011_Pack (06_TESTS AC-01..22 + XT-01..05 · 05_RULES BR-CR-01..12 / VR-01..05 / EC-01..14) |
| จำนวนเคส | 54 เคส / 10 groups |
| Signature ⭐⭐⭐ | **factory dump-result v2 + ออกใบรับอ้อย + Sync All**: ดึงผลการเท (caneType + time in/out + gross/tare/net · ไม่มี CCS) → ออก CRN → CBM awaiting_payment · bulk Sync All auto-issue |
| หัวใจ 1 — Dump v2 | ดึงผลการเท (Auto) → card ล็อก read-only (ประเภทอ้อย + Time In/Out + น.น.รวม/รถเบา/สุทธิ) + badge Auto · **ไม่มี CCS** (moved to Payment) |
| หัวใจ 2 — Manual fallback | จำลองไม่พบผล → `ไม่พบผลการเทจากโรงงาน — กรุณาเปลี่ยนเป็นโหมด Manual` + กรอก น.น.สุทธิ (2 dec) + เหตุผล |
| หัวใจ 3 — ออกใบรับอ้อย | auto มีผล / manual ครบ → `ออกใบรับอ้อยสำเร็จ` + CRN-2568-##### + ย้ายไปแท็บ เทแล้ว + side effects (CBM awaiting_payment · ปลดเหรียญ · PDF) |
| หัวใจ 4 — Sync All | `Sync All & ออกใบรับอ้อยอัตโนมัติ`: ไม่เลือกวันที่ → block · เลือกวันที่ → result modal (ทั้งหมด/สำเร็จ/ล้มเหลว) + failed table |
| หัวใจ 5 — Void | `ยกเลิกใบรับอ้อย` (reason≥5) → rollback CBM awaiting_dump_result · **CHK-0006 ชำระเงินแล้ว → block** |
| หมายเหตุ mock | prototype in-memory: refresh (F5) = reset seed 4 Draft + 3 Issued + 1 Void — ใช้เป็นข้อดี: ทุกเคส independent โดย refresh ก่อนเริ่ม |
| Cross-module ⭐ | ออกใบ → **CBM (F-AGM-007) awaiting_payment + free coin** · → **Cane Payment (net_weight+cane_type SoT)** · void → **CBM awaiting_dump_result rollback** = `(ต้อง simulate)` ที่ SIT |

**Seed tab รอผลเท (Draft · 4 รายการ · receiving_id NULL · dumpResultSource `-` · ยังไม่ออกใบ):**

| id | รหัส Booking | เลขเหรียญชั่ง | Quota ID | เกษตรกร | ประเภทเข้า | action |
|---|---|---|---|---|---|---|
| CHK-0001 | CBM-2568-0101 | 10501 | Q10001 | นายสมชาย ใจดี | จองคิว | ปุ่ม **ออกใบรับอ้อย** + eye |
| CHK-0002 | NBM-2568-0102 | 10502 | Q10002 | นายเอก มั่นคง | ไม่จองคิว | ปุ่ม **ออกใบรับอ้อย** + eye |
| CHK-0003 | NBM-2568-0103 | 10503 | - | นายมานะ ขยัน | โควต้ากลาง | ปุ่ม **ออกใบรับอ้อย** + eye |
| CHK-0004 | CBM-2568-0104 | 10504 | Q10004 | นางสมหญิง รักดี | จองคิว | ปุ่ม **ออกใบรับอ้อย** + eye |

> Draft ทุกแถว dumpResultSource=`-` · caneType/timeIn/timeOut/น้ำหนัก = `-` · sourceType (Check-in section) = CBM/NBM/CENTRAL

**Seed tab เทแล้ว (Issued · 3 รายการ · dump v2 auto · มี CRN + PDF):**

| id | เลขที่ใบรับ | เกษตรกร | เลขเหรียญชั่ง | น้ำหนักสุทธิ | ประเภทการเทอ้อย | สถานะชำระ |
|---|---|---|---|---|---|---|
| CHK-0005 | CRN-2568-00001 | นายประสิทธิ์ ทองมา | 10490 | 20,000.00 กก. | อ้อยสด (Fresh Cane) | รอทำจ่าย |
| CHK-0006 | CRN-2568-00002 | นายวิรัตน์ สีทอง | 10491 | 28,000.00 กก. | อ้อยโรงงาน | **ชำระเงินแล้ว** (→ void block) |
| CHK-0007 | CRN-2568-00003 | นายสายชล ทุ่งกว้าง | 10492 | 17,000.00 กก. | อ้อยไฟไหม้ | รอทำจ่าย |

**Seed tab ยกเลิก (Void · 1 รายการ):** CHK-0008 · CRN=`-` · นายทดสอบ ยกเลิก · pdfUrl ว่าง (พิมพ์ → `ไม่พบ PDF`) · voidReason "ข้อมูลน้ำหนักไม่ถูกต้อง ต้องชั่งใหม่"

- **Stat cards (นับจากทั้งระบบ · เท่ากันทุก tab):** รอผลเท = **4** · ออกใบวันนี้ = **3** · ยกเลิก = **1** · น้ำหนักอ้อยรวมวันนี้ = **65,000.00** (meta `65,000.00 กก. (Issued)`) [= 20,000 + 28,000 + 17,000]

**VERBATIM microcopy (Expected anchors — copy เป๊ะจาก prototype):**
- top tabs: `รอผลเท` · `เทแล้ว` · `ยกเลิก` (แต่ละแท็บมี count badge)
- page header: title = ชื่อ tab + count `N รายการ` · sub `การรับอ้อย · ออกใบรับอ้อยหน้าโรงงาน (WKN)`
- header ปุ่ม: `Scan QR` · `ค้นหาเลขเหรียญ` · `Export CSV` · `Sync All & ออกใบรับอ้อยอัตโนมัติ` (เฉพาะ tab รอผลเท) · `ออกใบรับอ้อย` (primary → เปิด modal ค้นหาเลขเหรียญชั่ง)
- stat cards: `รอผลเท` (meta "เช็คอินแล้ว รอออกใบ") · `ออกใบวันนี้` ("ใบรับอ้อยที่ออกแล้ว") · `ยกเลิก` ("รายการที่ถูกยกเลิก") · `น้ำหนักอ้อยรวมวันนี้` ("… กก. (Issued)")
- Draft columns: `รหัสเกษตรกร · เลขเหรียญชั่ง · วัน/เวลาเข้า · ผู้ขนส่ง · เบอร์โทร · ทะเบียนรถ · ชื่อคนขับ · ประเภทเข้า · การกระทำ`
- Issued/Void columns: `เลขที่ใบรับ · เลขเหรียญชั่ง · วัน/เวลาเข้า · ผู้ขนส่ง · ทะเบียนรถ · น้ำหนักสุทธิ · ประเภทการเทอ้อย · สถานะ · การกระทำ`
- filter: search placeholder `ค้นหาเลขเหรียญ/รหัส/ทะเบียน` · สถานะ `ทุกสถานะ`/`รอผลเท`/`เทแล้ว`/`ยกเลิก` · ประเภทเข้า `ทุกประเภท`/`จองคิว`/`ไม่จองคิว`/`โควต้ากลาง` · date input · ปุ่ม `ล้าง`
- entry badge: `จองคิว` (info) · `ไม่จองคิว` (muted) · `โควต้ากลาง` (warning)
- status pill: `รอผลเท` (muted) · `เทแล้ว` (success) · `ยกเลิก` (danger)
- Issue drawer (920): eyebrow `ออกใบรับอ้อย · [CHK-id]` · section `ข้อมูล Check-in` cells `รหัส Check-in`/`ประเภทการจอง`/`รหัส Booking`/`เลขเหรียญชั่ง`/`เวลา Check-in`/`ประเภทเข้าโรงงาน`/`ชื่อเกษตรกร`/`ชื่อคนขับ`/`เบอร์โทร`/`ทะเบียนรถ`/`Quota ID` · section `ผลการเทจากโรงงาน (Dump Result)` + badge `Auto`/`Manual`
- dump buttons: `ดึงผลการเท (Auto)` · `จำลองไม่พบผล` · `สลับเป็นโหมดกรอกมือ` · `รีเซ็ต / กลับไป Auto`
- dump card (auto success): header `ดึงผลการเทสำเร็จ (ล็อกค่า)` + pill `Auto` · cells `ประเภทอ้อย` (`05 - อ้อยสด (Fresh Cane)`) · `เลขเหรียญชั่ง` · `เวลาเข้า (Time In)` (`08:15`) · `เวลาออก (Time Out)` (`08:32`) · `น.น. รวม (กก.)` (`32,000.00`) · `น.น. รถเบา (กก.)` (`12,000.00`) · `น.น. อ้อยสุทธิ (กก.)` (`20,000.00`)
- dump auto-idle note: `กดปุ่ม "ดึงผลการเท (Auto)" เพื่อดึงผลการเทจากระบบโรงงาน — ระบบจะล็อกค่าน้ำหนักและประเภทอ้อยอัตโนมัติ`
- manual fields: `น.น. อ้อยสุทธิ (กก.)` * (placeholder `เช่น 20000.00`) · `เหตุผล` * (placeholder `เหตุผลที่ต้องกรอกด้วยตนเอง...`) · warn note `ไม่พบผลการเทจากโรงงาน — กรุณาเปลี่ยนเป็นโหมด Manual`
- issue footer: meta = `[รหัส Booking]` · ปุ่ม `ปิด` / `ออกใบรับอ้อย` (disabled จนกว่ามีผล)
- Sync All modal: title `ผลการ Sync All` · sub `ดึงผลการเท + ออกใบรับอ้อยอัตโนมัติ` · chips `ทั้งหมด`/`สำเร็จ`/`ล้มเหลว` · failed table header `รายการที่ล้มเหลว` (checkInTime/coin/booking/farmer/error) · ปุ่ม `ดูรายการที่ล้มเหลว` / `ปิด`
- Void modal: title `ยกเลิกใบรับอ้อย` · warn note `การยกเลิกจะย้อนสถานะ CBM เป็น awaiting_dump_result และไม่สามารถชำระเงินต่อ` · field `เหตุผลการยกเลิก` * (placeholder `กรุณากรอกเหตุผลการยกเลิก (อย่างน้อย 5 ตัวอักษร)`) · ปุ่ม `ยกเลิก` / `ยืนยัน Void` · paid-block note `รายการนี้ชำระเงินแล้ว จึงไม่สามารถยกเลิก (Void) ได้`
- PDF modal: title `ใบรับอ้อย (PDF)` · sub `[CRN] · ตัวอย่างเอกสาร` · body head `ใบรับอ้อย (Cane Receiving)` + QR box · ปุ่ม `ปิด` / `พิมพ์`
- QR modal: title `สแกน QR` · sub `สแกน QR หรือป้อนรหัส Booking เพื่อเปิดใบรับอ้อย` · helper `เล็งกล้องไปที่ QR Code บนใบเช็คอิน` · field `หรือป้อนรหัส Booking` (placeholder `CBM-2568-....`) + ปุ่ม `ไป` · footer `ปิด`
- Search modal: title `ค้นหาเลขเหรียญชั่ง` · sub `ป้อนเลขเหรียญชั่งเพื่อเปิดใบรับอ้อย` · field `เลขเหรียญชั่ง / รหัส` (placeholder `เช่น 10501`) + ปุ่ม `ไป` · footer `ปิด`
- detail drawer (680): eyebrow `การรับอ้อย · [CRN หรือ CHK-id]` · sections `ข้อมูล Check-in` / `ผลการเทจากโรงงาน` / `ข้อมูลเอกสาร` · footer `Void`(issued) / `พิมพ์` / `ออกใบรับอ้อย`(draft) / `ปิด`
- toast success: `ดึงผลการเทสำเร็จ` · `ออกใบรับอ้อยสำเร็จ` (desc `CBM → awaiting_payment · ปลดเหรียญชั่ง · สร้าง PDF`) · `ส่งออกข้อมูลสำเร็จ` · `Void ใบรับอ้อยสำเร็จ`
- toast info: `กำลังส่งออกข้อมูล...` · `กำลังดึงผลการเท...` · `ดึงผลการเทเสร็จสิ้น` (desc `สำเร็จ X รายการ, ล้มเหลว Y รายการ`) · `กำลังส่งไปยังเครื่องพิมพ์...`
- toast warning/error: `ไม่พบผลการเทจากโรงงาน` · `กรุณากรอกน้ำหนักสุทธิ` · `กรุณากรอกน้ำหนักสุทธิเป็นจำนวนไม่ลบและ 2 ตำแหน่ง` · `กรุณากรอกเหตุผลการกรอกด้วยตนเอง` · `เหตุผลต้องมีความยาวอย่างน้อย 5 ตัวอักษร` · `กรุณาเลือกช่วงวันที่ก่อนทำ Sync All` · `ไม่สามารถยกเลิกรายการที่ชำระเงินแล้ว` · `ไม่พบ PDF` · `ไม่พบรายการ`
- failed-table error: `ไม่พบข้อมูลผลการเทในระบบโรงงาน`
- footer/pagination: `แสดง X-Y จาก Z รายการ`
- empty: filtered `ไม่พบรายการที่ค้นหา` (desc "ลองปรับคำค้นหรือล้างตัวกรอง" + ปุ่ม `ล้าง`) · no-data `ไม่มีรายการ` (desc "ยังไม่มีรายการในแท็บ [tab]")
- simulate: dump API v2 จริง · CBM awaiting_payment + free coin · PDF server render (A4+QR) · Sync All 409/ไม่รันซ้อน · Payment SoT (net+cane_type) · void reversal · CSV file · ประเภทอ้อย filter · net cross-check debug · unknown cane type

## Coverage

| Group | เคส | ความสำคัญ |
|---|---|---|
| A — List 3-tabs / stats / rows (Draft/Issued/Void) | TC-A01..A06 (6) | สูงสุด |
| B — Search / filter / CSV / empty / pagination | TC-B01..B07 (7) | สูงสุด |
| C — Issue drawer + Check-in info ⭐ | TC-C01..C04 (4) | สูงสุด |
| D — Dump Result v2 auto ⭐ | TC-D01..D03 (3) | สูงสุด |
| E — Manual fallback + validation | TC-E01..E06 (6) | สูงสุด |
| F — ออกใบรับอ้อย + side effects ⭐ | TC-F01..F05 (5) | สูงสุด |
| G — Sync All ⭐ | TC-G01..G06 (6) | สูงสุด |
| H — Detail drawer + PDF + QR/Search | TC-H01..H06 (6) | สูง |
| I — Void (+ blocked-if-paid) ⭐ | TC-I01..I05 (5) | สูงสุด |
| J — Cross-module XT-01..05 + simulate | TC-J01..J06 (6) | สูงสุด |

---

## Coverage Ledger

### Stories/AC (06_TESTS §6.1)
| AC | รายละเอียด (ย่อ) | cases |
|---|---|---|
| AC-01 | 3 แท็บ (รอผลเท/เทแล้ว/ยกเลิก) + count + 4 stats | TC-A01, TC-A02, TC-A06 |
| AC-02 | ค้นหา (เลขเหรียญ/รหัส/ทะเบียน) · filter สถานะ + ประเภทเข้า + date (ประเภทอ้อย = simulate) | TC-B01, TC-B02, TC-B03, TC-B04, TC-J06 |
| AC-03 | Draft columns · Issued/Void + น้ำหนัก/ประเภทการเท/สถานะ · pending action | TC-A01, TC-A03, TC-A04, TC-A05 |
| AC-04 | Export CSV → "กำลังส่งออกข้อมูล..." → "ส่งออกข้อมูลสำเร็จ" | TC-B06 |
| AC-05 | เปิด Issue drawer → checkin snapshot read-only ครบ | TC-C01, TC-C02 |
| AC-06 | ดึงผลการเท (Auto) → card v2 + lock read-only + badge Auto (ไม่มี CCS) | TC-D01, TC-D02, TC-D03 |
| AC-07 | ดึงผลการเท fail → "ไม่พบผลการเทจากโรงงาน — กรุณาเปลี่ยนเป็นโหมด Manual" + Manual | TC-E01 |
| AC-08 | manual net ว่าง → "กรุณากรอกน้ำหนักสุทธิ" (guard: ปุ่ม disabled) | TC-E04 |
| AC-09 | manual net ผิดรูปแบบ → "กรุณากรอกน้ำหนักสุทธิเป็นจำนวนไม่ลบและ 2 ตำแหน่ง" | TC-E03 |
| AC-10 | manual ไม่ใส่เหตุผล → "กรุณากรอกเหตุผลการกรอกด้วยตนเอง" (guard: ปุ่ม disabled) | TC-E05 |
| AC-11 | ออกใบรับอ้อย → "ออกใบรับอ้อยสำเร็จ" + CRN + ย้ายแท็บ + side effects | TC-F01, TC-F02, TC-F03 |
| AC-12 | ปุ่ม Sync All (RBAC) ในแท็บรอผลเท | TC-G01, TC-G02 |
| AC-13 | Sync All ไม่เลือกวันที่ → บังคับเลือกวันที่ก่อน | TC-G01 |
| AC-14 | Sync All → "กำลังดึงผลการเท..." → result modal (ทั้งหมด/สำเร็จ/ล้มเหลว) | TC-G02 |
| AC-15 | result modal failed table + "ไม่พบข้อมูลผลการเทในระบบโรงงาน" | TC-G03 |
| AC-16 | ปุ่ม [ดูรายการที่ล้มเหลว]/[ปิด] · toast "ดึงผลการเทเสร็จสิ้น" | TC-G04 |
| AC-17 | detail → block ผลการเท read-only + document info | TC-H01, TC-H02 |
| AC-18 | พิมพ์ → PDF A4+QR · ไม่มี PDF → "ไม่พบ PDF" | TC-H04, TC-H05 |
| AC-19 | void reason <5 → "เหตุผลต้องมีความยาวอย่างน้อย 5 ตัวอักษร" | TC-I02 |
| AC-20 | void สำเร็จ → "Void ใบรับอ้อยสำเร็จ" + Void + rollback CBM | TC-I03 |
| AC-21 | void ที่ชำระเงินแล้ว → block | TC-I04 |
| AC-22 | Scan QR / ค้นหาเลขเหรียญชั่ง → issue flow | TC-H06, TC-C02 |

### Cross-Module / Event (06_TESTS §6.9) ⭐
| XT | Scenario | Source | cases |
|---|---|---|---|
| XT-01 | Draft = checked-in ยังไม่ออกใบ | Check-in (F-AGM-010) | TC-A03, TC-J01 (source จริง = simulate) |
| XT-02 | ดึงผลการเท v2 (caneType+times+weights ไม่มี CCS) | Factory dump API | TC-D01, TC-J02 (API จริง = simulate) |
| XT-03 | ออกใบ → CBM awaiting_payment + free coin (idempotent) | → CBM (F-AGM-007) | TC-F01, TC-J03 (event จริง = simulate) |
| XT-04 | Receiving → Payment (net_weight + cane_type SoT) | → Cane Payment | TC-J04 (ต้อง simulate) |
| XT-05 | void → CBM awaiting_dump_result (rollback, ไม่ชำระต่อ) | → CBM | TC-I03, TC-J05 (reversal จริง = simulate) |

### Business Rules (05_RULES §5.1)
| BR | cases |
|---|---|
| BR-CR-01 Single Sync dump v2 (checkin+coin+quota → caneType/times/weights, ไม่มี CCS) | TC-D01, TC-J02 |
| BR-CR-02 Auto สำเร็จ → lock read-only · fail → manual | TC-D01, TC-E01 |
| BR-CR-03 net = gross − tare (หรือ manual) | TC-D01, TC-E03 |
| BR-CR-04 ออกใบ → CRN + Issued + CBM awaiting_payment + free coin + PDF | TC-F01, TC-J03 |
| BR-CR-05 POST idempotent (ไม่สร้างซ้ำ) | TC-F05, TC-J03 |
| BR-CR-06 Sync All bulk → result modal (success/failed) | TC-G02, TC-G03 |
| BR-CR-07 Sync All บังคับเลือกวันที่ + ไม่รันซ้อน | TC-G01, TC-G06 |
| BR-CR-08 Receiving = SoT (net_weight + cane_type ให้ Payment) | TC-J04 |
| BR-CR-09 Void → status Void + rollback CBM + reason≥5 | TC-I02, TC-I03, TC-J05 |
| BR-CR-10 Void ไม่ได้ถ้า paymentStatus=ชำระเงินแล้ว | TC-I04 |
| BR-CR-11 ดึงผลการเทเฉพาะรายการยังไม่ออกใบ (receiving_id NULL = Draft) | TC-C01, TC-D01 |
| BR-CR-12 cane type ไม่รู้จัก → คง code · Payment adj 0 (ฝั่ง Payment) | TC-J06 (ต้อง simulate) |

### Validation (05_RULES §5.4)
| VR | Message | cases |
|---|---|---|
| VR-01 | "กรุณากรอกน้ำหนักสุทธิ" (manual net required · guard) | TC-E04 |
| VR-02 | "กรุณากรอกน้ำหนักสุทธิเป็นจำนวนไม่ลบและ 2 ตำแหน่ง" | TC-E03 |
| VR-03 | "กรุณากรอกเหตุผลการกรอกด้วยตนเอง" (manual reason · guard) | TC-E05 |
| VR-04 | "เหตุผลต้องมีความยาวอย่างน้อย 5 ตัวอักษร" (void reason ≥5) | TC-I02 |
| VR-05 | "กรุณาเลือกช่วงวันที่ก่อนทำ Sync All" (Sync All date required) | TC-G01 |

### Edge Cases (05_RULES §5.5)
| EC | Case | cases |
|---|---|---|
| EC-01 | ดึงผลการเท auto สำเร็จ → dump v2 card + lock | TC-D01 |
| EC-02 | ดึงผลการเท auto fail → error + Manual | TC-E01 |
| EC-03 | manual net ว่าง → VR-01 (guard) | TC-E04 |
| EC-04 | manual net ผิดรูปแบบ → VR-02 | TC-E03 |
| EC-05 | manual ไม่ใส่เหตุผล → VR-03 (guard) | TC-E05 |
| EC-06 | ออกใบรับอ้อย → Issued + CRN + side effects + toast | TC-F01 |
| EC-07 | ออกใบซ้ำ (idempotent) → ไม่สร้างซ้ำ (409/no-op) | TC-F05 (ต้อง simulate) |
| EC-08 | Sync All ไม่เลือกวันที่ → VR-05 block | TC-G01 |
| EC-09 | Sync All สำเร็จบางส่วน → result modal (สำเร็จ/ล้มเหลว) | TC-G02, TC-G03 |
| EC-10 | Sync All fail item → error "ไม่พบข้อมูลผลการเทในระบบโรงงาน" | TC-G03 |
| EC-11 | Void reason <5 → VR-04 | TC-I02 |
| EC-12 | Void สำเร็จ → Void + rollback + "Void ใบรับอ้อยสำเร็จ" | TC-I03 |
| EC-13 | Void ที่จ่ายแล้ว → block | TC-I04 |
| EC-14 | net cross-check (gross-tare≠net) → เก็บสามค่า debug | TC-J06 (ต้อง simulate) |

### Error Catalog (05_RULES §5.6 — UI-observable)
| error | cases |
|---|---|
| VALIDATION_FAILED (net format / reason / void reason) | TC-E03, TC-E04, TC-E05, TC-I02 |
| DUMP_NOT_FOUND "ไม่พบผลการเทจากโรงงาน — กรุณาเปลี่ยนเป็นโหมด Manual" / "ไม่พบข้อมูลผลการเทในระบบโรงงาน" | TC-E01, TC-G03 |
| CONFLICT(409 dup) "รายการซ้ำ (idempotent)" | TC-F05, TC-J03 (ต้อง simulate) |
| VOID_BLOCKED_PAID "ไม่สามารถยกเลิกรายการที่ชำระเงินแล้ว" | TC-I04 |
| SYNC_ALL_DATE_REQUIRED "กรุณาเลือกช่วงวันที่ก่อนทำ Sync All" | TC-G01 |

### State Machine (05_RULES §5.2)
| entity | ข้อยืนยัน (ย่อ) | cases |
|---|---|---|
| Receiving | Draft(รอผลเท) → Issued(เทแล้ว) → Void(ยกเลิก) | TC-F01, TC-I03 |
| Dump | `-` → auto (SUCCESS lock) / fail → manual | TC-D01, TC-E01 |
| CBM sync | issue → awaiting_payment · void → awaiting_dump_result | TC-J03, TC-J05 (ต้อง simulate) |

### Permission (05_RULES §5.3)
| cell | cases |
|---|---|
| Receiving Staff (dump + ออกใบ + Sync All) — prototype user | TC-D01, TC-F01, TC-G02 |
| Supervisor/Admin (manual override + void) · Viewer (read, ไม่เห็น Sync All/create) — RBAC จริง | TC-J06 (ต้อง simulate) |

**Manifest cross-check (FRD §0.12):** AC 22/22 (AC-01..22) · XT-01..05 5/5 · BR-CR-01..12 12/12 · VR-01..05 5/5 · EC-01..14 14/14 → ทุกแถว manifest มีคู่ใน Ledger ✅

---

## Data Sets

### ชุด A — ออกใบ auto (happy)
| ฟิลด์ | ค่า |
|---|---|
| Draft row | CHK-0001 (นายสมชาย ใจดี · CBM-2568-0101 · เหรียญ 10501) |
| dump (auto) | 05 - อ้อยสด (Fresh Cane) · Time In 08:15 · Time Out 08:32 · รวม 32,000.00 · รถเบา 12,000.00 · สุทธิ 20,000.00 |
| CRN ที่คาด | CRN-2568-00004 |

### ชุด B — Manual fallback
| กรณี | net | เหตุผล | คาดหวัง (ข้อความจริง) |
|---|---|---|---|
| B1 (format ติดลบ) | -5 | "ชั่งใหม่" | กรุณากรอกน้ำหนักสุทธิเป็นจำนวนไม่ลบและ 2 ตำแหน่ง |
| B2 (format 3 ตำแหน่ง) | 20000.999 | "ชั่งใหม่" | กรุณากรอกน้ำหนักสุทธิเป็นจำนวนไม่ลบและ 2 ตำแหน่ง |
| B3 (net ว่าง) | *(เว้นว่าง)* | "ชั่งใหม่" | ปุ่ม ออกใบรับอ้อย ยัง disabled (guard VR-01) |
| B4 (reason ว่าง) | 20000.00 | *(เว้นว่าง)* | ปุ่ม ออกใบรับอ้อย ยัง disabled (guard VR-03) |
| B5 (manual happy) | 18500.00 | "เครื่องชั่งโรงงานออฟไลน์ ชั่งด้วยมือ" | ออกใบรับอ้อยสำเร็จ |

### ชุด C — Void
| กรณี | รายการ | เหตุผล | คาดหวัง |
|---|---|---|---|
| C1 (reason สั้น) | CHK-0007 (CRN-2568-00003) | "สั้น" (<5) | เหตุผลต้องมีความยาวอย่างน้อย 5 ตัวอักษร |
| C2 (happy) | CHK-0007 (CRN-2568-00003) | "น้ำหนักผิด ต้องชั่งใหม่" | Void ใบรับอ้อยสำเร็จ |
| C3 (paid block) | CHK-0006 (CRN-2568-00002) | — | ไม่สามารถยกเลิกรายการที่ชำระเงินแล้ว / ปุ่ม ยืนยัน Void disabled |

### ชุด D — Sync All
| กรณี | date filter | คาดหวัง |
|---|---|---|
| D1 (no date) | *(ว่าง)* | กรุณาเลือกช่วงวันที่ก่อนทำ Sync All |
| D2 (date set) | 2026-07-21 | result modal: ทั้งหมด 4 / สำเร็จ 3 / ล้มเหลว 1 (CHK-0003 · ไม่พบข้อมูลผลการเทในระบบโรงงาน) |

---

## Test Cases

## Group A — List 3-tabs / stats / rows (US-01)

### TC-A01 — เปิดหน้า tab รอผลเท + 4 stats + คอลัมน์ Draft (happy — AC-01/03)
- group: A · ความสำคัญ: สูงสุด · trace: AC-01, AC-03 / UI loaded
- Setup: seed=default (refresh) · files=—
- Start: OPEN `#/receivings`
- ผ่านเมื่อ: top tabs + stat cards + คอลัมน์ Draft ตรง seed

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/receivings` | — | top tabs **รอผลเท** (active · count **4**) · **เทแล้ว** (count **3**) · **ยกเลิก** (count **1**) · หัวข้อ **รอผลเท** + count **4 รายการ** · sub **การรับอ้อย · ออกใบรับอ้อยหน้าโรงงาน (WKN)** | ☐ |
| 2 | VERIFY แถบ stats 4 การ์ด | — | **รอผลเท 4** · **ออกใบวันนี้ 3** · **ยกเลิก 1** · **น้ำหนักอ้อยรวมวันนี้ 65,000.00** (meta **65,000.00 กก. (Issued)**) | ☐ |
| 3 | VERIFY หัวคอลัมน์ตาราง (tab รอผลเท) | — | เรียง: **รหัสเกษตรกร · เลขเหรียญชั่ง · วัน/เวลาเข้า · ผู้ขนส่ง · เบอร์โทร · ทะเบียนรถ · ชื่อคนขับ · ประเภทเข้า · การกระทำ** | ☐ |
| 4 | VERIFY แถว CHK-0001 | — | รหัสเกษตรกร **Q10001** (มี **CBM-2568-0101** ใต้) · เลขเหรียญชั่ง **10501** · ผู้ขนส่ง **นายสมชาย ใจดี** · ทะเบียน **80-1234** · คนขับ **สมชาย ใจดี** · badge **จองคิว** | ☐ |
| 5 | VERIFY ปุ่ม header + footer | — | ปุ่ม **Scan QR** · **ค้นหาเลขเหรียญ** · **Export CSV** · **Sync All & ออกใบรับอ้อยอัตโนมัติ** · **ออกใบรับอ้อย** (primary) · footer **แสดง 1-4 จาก 4 รายการ** | ☐ |

### TC-A02 — สลับ 3 แท็บ รอผลเท ↔ เทแล้ว ↔ ยกเลิก + count (AC-01)
- group: A · ความสำคัญ: สูง · trace: AC-01 / tab route
- Setup: seed=default · files=—
- Start: OPEN `#/receivings`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK top tab **เทแล้ว** | — | URL = **#/receivings/issued** · หัวข้อ **เทแล้ว** + count **3 รายการ** · คอลัมน์เปลี่ยนเป็นชุด Issued (**เลขที่ใบรับ … น้ำหนักสุทธิ … ประเภทการเทอ้อย … สถานะ**) · ปุ่ม Sync All หายไป | ☐ |
| 2 | CLICK top tab **ยกเลิก** | — | URL = **#/receivings/void** · หัวข้อ **ยกเลิก** + count **1 รายการ** · แถว **CHK-0008** (นายทดสอบ ยกเลิก) | ☐ |
| 3 | CLICK top tab **รอผลเท** | — | URL = **#/receivings** · หัวข้อ **รอผลเท** + count **4 รายการ** | ☐ |
| 4 | VERIFY count badge บนแท็บ (คงที่ทุก tab) | — | **รอผลเท 4** · **เทแล้ว 3** · **ยกเลิก 1** | ☐ |

### TC-A03 — Draft rows: entry badge + action button + XT-01 (AC-03 / XT-01)
- group: A · ความสำคัญ: สูงสุด · trace: AC-03 / XT-01 (checked-in read)
- Setup: seed=default · files=—
- Start: OPEN `#/receivings`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY 4 แถว Draft | — | CHK-0001 badge **จองคิว** · CHK-0002 badge **ไม่จองคิว** · CHK-0003 badge **โควต้ากลาง** · CHK-0004 badge **จองคิว** | ☐ |
| 2 | VERIFY row-actions แต่ละแถว Draft | — | มีปุ่ม **ออกใบรับอ้อย** (primary sm) + ปุ่ม eye (รายละเอียด) · ไม่มีปุ่ม พิมพ์/Void | ☐ |
| 3 | VERIFY แถว CHK-0003 (โควต้ากลาง · quota ว่าง) | — | รหัสเกษตรกร **-** (มี **NBM-2568-0103** ใต้) · เลขเหรียญชั่ง **10503** · ผู้ขนส่ง **นายมานะ ขยัน** · badge **โควต้ากลาง** | ☐ |

### TC-A04 — เปิด tab เทแล้ว + คอลัมน์ Issued + row-actions (AC-03)
- group: A · ความสำคัญ: สูงสุด · trace: AC-03 / issued columns
- Setup: seed=default · files=—
- Start: OPEN `#/receivings/issued`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/receivings/issued` | — | หัวข้อ **เทแล้ว** + count **3 รายการ** · footer **แสดง 1-3 จาก 3 รายการ** | ☐ |
| 2 | VERIFY หัวคอลัมน์ | — | **เลขที่ใบรับ · เลขเหรียญชั่ง · วัน/เวลาเข้า · ผู้ขนส่ง · ทะเบียนรถ · น้ำหนักสุทธิ · ประเภทการเทอ้อย · สถานะ · การกระทำ** | ☐ |
| 3 | VERIFY แถว CHK-0005 | — | เลขที่ใบรับ **CRN-2568-00001** (มี **Q10010** ใต้) · น้ำหนักสุทธิ **20,000.00 กก.** · ประเภทการเทอ้อย **อ้อยสด (Fresh Cane)** · สถานะ pill **เทแล้ว** | ☐ |
| 4 | VERIFY row-actions (Issued) | — | แต่ละแถวมีปุ่ม eye + ปุ่ม printer (**พิมพ์**) + ปุ่ม x-circle (**Void**) | ☐ |

### TC-A05 — เปิด tab ยกเลิก + row-actions (ไม่มี Void) (AC-03)
- group: A · ความสำคัญ: สูง · trace: AC-03 / void columns
- Setup: seed=default · files=—
- Start: OPEN `#/receivings/void`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/receivings/void` | — | หัวข้อ **ยกเลิก** + count **1 รายการ** · แถว **CHK-0008** · ผู้ขนส่ง **นายทดสอบ ยกเลิก** · น้ำหนักสุทธิ **-** · ประเภทการเทอ้อย **-** · สถานะ pill **ยกเลิก** | ☐ |
| 2 | VERIFY row-actions (Void tab) | — | มีปุ่ม eye + ปุ่ม printer (**พิมพ์**) · **ไม่มี** ปุ่ม x-circle (Void) | ☐ |

### TC-A06 — stats นับทั้งระบบ · เท่ากันทุก tab (AC-01)
- group: A · ความสำคัญ: สูง · trace: AC-01 / stats consistency
- Setup: seed=default · files=—
- Start: OPEN `#/receivings`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY stats บน tab รอผลเท | — | **รอผลเท 4 · ออกใบวันนี้ 3 · ยกเลิก 1 · น้ำหนักอ้อยรวมวันนี้ 65,000.00** | ☐ |
| 2 | CLICK tab **เทแล้ว** → VERIFY stats | — | ค่าเดิม **4 / 3 / 1 / 65,000.00** (นับจากทั้งระบบ ไม่ผูก tab) | ☐ |
| 3 | CLICK tab **ยกเลิก** → VERIFY stats | — | ค่าเดิม **4 / 3 / 1 / 65,000.00** | ☐ |

---

## Group B — Search / filter / CSV / empty / pagination (US-01)

### TC-B01 — ค้นหา (เลขเหรียญ/รหัส/ทะเบียน/เกษตรกร) (AC-02)
- group: B · ความสำคัญ: สูงสุด · trace: AC-02 / search
- Setup: seed=default · files=—
- Start: OPEN `#/receivings`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "10504" → ช่องค้นหา (placeholder **ค้นหาเลขเหรียญ/รหัส/ทะเบียน**) → WAIT | — | เหลือ 1 แถว **CHK-0004** (นางสมหญิง รักดี) | ☐ |
| 2 | CLICK **ล้าง** → TYPE "83-4567" (ทะเบียน) → WAIT | — | เหลือ 1 แถว CHK-0004 | ☐ |
| 3 | CLICK **ล้าง** → TYPE "มานะ" (เกษตรกร) → WAIT | — | เหลือ 1 แถว CHK-0003 | ☐ |
| 4 | CLICK **ล้าง** | — | กลับ 4 รายการ | ☐ |

### TC-B02 — filter สถานะ (AC-02)
- group: B · ความสำคัญ: สูง · trace: AC-02 / status filter
- Setup: seed=default · files=—
- Start: OPEN `#/receivings`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT dropdown สถานะ = **รอผลเท** | — | ยัง 4 แถว (Draft ทุกแถว = รอผลเท) | ☐ |
| 2 | SELECT สถานะ = **เทแล้ว** | — | ตารางว่าง + empty **ไม่พบรายการที่ค้นหา** (tab รอผลเท ไม่มี Issued) + ปุ่ม **ล้าง** | ☐ |
| 3 | CLICK **ล้าง** | — | กลับ 4 รายการ | ☐ |

### TC-B03 — filter ประเภทเข้า (AC-02)
- group: B · ความสำคัญ: สูง · trace: AC-02 / entry filter
- Setup: seed=default · files=—
- Start: OPEN `#/receivings`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT ประเภทเข้า = **จองคิว** | — | เหลือ 2 แถว (CHK-0001 + CHK-0004) | ☐ |
| 2 | CLICK **ล้าง** → SELECT ประเภทเข้า = **ไม่จองคิว** | — | เหลือ 1 แถว CHK-0002 | ☐ |
| 3 | CLICK **ล้าง** → SELECT ประเภทเข้า = **โควต้ากลาง** | — | เหลือ 1 แถว CHK-0003 | ☐ |

### TC-B04 — filter วันที่ + reset (AC-02) · ประเภทอ้อย filter = SIT
- group: B · ความสำคัญ: กลาง · trace: AC-02 / date filter · **prototype: ไม่มี ประเภทอ้อย dropdown → SIT**
- Setup: seed=default · files=—
- Start: OPEN `#/receivings`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SET date input = **2026-07-21** | — | ยัง 4 แถว (Draft ทุกแถว dateKey 2026-07-21) | ☐ |
| 2 | SET date input = **2026-07-20** | — | ตารางว่าง + empty **ไม่พบรายการที่ค้นหา** + ปุ่ม **ล้าง** | ☐ |
| 3 | CLICK **ล้าง** | — | กลับ 4 รายการ · date input ว่าง | ☐ |
| 4 | VERIFY (ระบบจริง — SIT): filter **ประเภทอ้อย** | — | มี dropdown ประเภทอ้อย (prototype ไม่มี — filter bar มีแค่ สถานะ/ประเภทเข้า/date) | ☐ (ต้อง simulate) |

### TC-B05 — empty state (filtered vs no-data) (AC-02)
- group: B · ความสำคัญ: กลาง · trace: AC-02 / empty variants
- Setup: seed=default · files=—
- Start: OPEN `#/receivings`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "ไม่มีรายการนี้แน่นอน" → ค้นหา → WAIT | — | ตารางว่าง + empty title **ไม่พบรายการที่ค้นหา** (desc **ลองปรับคำค้นหรือล้างตัวกรอง**) + ปุ่ม **ล้าง** | ☐ |
| 2 | CLICK **ล้าง** | — | กลับ 4 รายการ | ☐ |
| 3 | VERIFY (no-data variant · SIT): tab ที่ไม่มี record | — | empty title **ไม่มีรายการ** (desc **ยังไม่มีรายการในแท็บ …**) — prototype ทุก tab มี record เสมอ | ☐ (ต้อง simulate) |

### TC-B06 — Export CSV → toasts (AC-04) (ไฟล์จริง ต้อง simulate)
- group: B · ความสำคัญ: กลาง · trace: AC-04 · **prototype: toast จำลอง · ไฟล์จริง = SIT**
- Setup: seed=default · files=—
- Start: OPEN `#/receivings`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **Export CSV** → WAIT ~1s | — | toast **กำลังส่งออกข้อมูล...** → ตามด้วย toast **ส่งออกข้อมูลสำเร็จ** | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): ไฟล์ CSV จริง | — | ไฟล์ CSV ดาวน์โหลด · คอลัมน์ไทยตรงตาราง · encoding ถูก | ☐ (ต้อง simulate) |

### TC-B07 — pagination footer (AC-01)
- group: B · ความสำคัญ: กลาง · trace: AC-01 / pagination
- Setup: seed=default · files=—
- Start: OPEN `#/receivings/issued`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY pagination footer (tab เทแล้ว) | — | **แสดง 1-3 จาก 3 รายการ** (pageSize 25 · หน้าเดียว) · ปุ่มหน้า **1** active · chevron ซ้าย/ขวา disabled | ☐ |

---

## Group C — Issue drawer + Check-in info (US-02) ⭐

### TC-C01 — เปิด Issue drawer จากปุ่ม ออกใบรับอ้อย + Check-in snapshot (happy — AC-05 / BR-CR-11)
- group: C · ความสำคัญ: สูงสุด · trace: AC-05 / BR-CR-11 (dump เฉพาะ Draft)
- Setup: seed=default · files=—
- Start: OPEN `#/receivings`
- ผ่านเมื่อ: drawer 920 เปิด + section Check-in read-only ครบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ออกใบรับอ้อย** (บนแถว CHK-0001) | — | drawer เปิด · eyebrow **ออกใบรับอ้อย · CHK-0001** · title **นายสมชาย ใจดี** + badge **จองคิว** · sub **80-1234 · เหรียญ 10501 · เข้าเมื่อ 08:15 21/07/26** | ☐ |
| 2 | VERIFY section **ข้อมูล Check-in** | — | cells: รหัส Check-in **CHK-0001** · ประเภทการจอง **จองคิว** · รหัส Booking **CBM-2568-0101** · เลขเหรียญชั่ง **10501** · เวลา Check-in **08:15 21/07/26** · ประเภทเข้าโรงงาน **CBM** · ชื่อเกษตรกร **นายสมชาย ใจดี** · ชื่อคนขับ **สมชาย ใจดี** · เบอร์โทร **081-111-1111** · ทะเบียนรถ **80-1234** · Quota ID **Q10001** | ☐ |
| 3 | VERIFY section **ผลการเทจากโรงงาน (Dump Result)** เริ่มต้น | — | badge **Auto** · ปุ่ม **ดึงผลการเท (Auto)** + **จำลองไม่พบผล** + **สลับเป็นโหมดกรอกมือ** · note **กดปุ่ม "ดึงผลการเท (Auto)" เพื่อดึงผลการเทจากระบบโรงงาน — ระบบจะล็อกค่าน้ำหนักและประเภทอ้อยอัตโนมัติ** | ☐ |
| 4 | VERIFY ปุ่ม footer | — | meta **CBM-2568-0101** · ปุ่ม **ปิด** + **ออกใบรับอ้อย** (disabled — ยังไม่มีผลการเท) | ☐ |

### TC-C02 — เปิด Issue flow จาก header ออกใบรับอ้อย → modal ค้นหา → ไป (AC-05 / AC-22)
- group: C · ความสำคัญ: สูง · trace: AC-05, AC-22 / search-modal entry
- Setup: seed=default · files=—
- Start: OPEN `#/receivings`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ออกใบรับอ้อย** (header primary) | — | modal เปิด · title **ค้นหาเลขเหรียญชั่ง** · sub **ป้อนเลขเหรียญชั่งเพื่อเปิดใบรับอ้อย** · field **เลขเหรียญชั่ง / รหัส** (placeholder **เช่น 10501**) + ปุ่ม **ไป** | ☐ |
| 2 | TYPE **10502** → CLICK **ไป** → WAIT | — | modal ปิด · เปิด Issue drawer **ออกใบรับอ้อย · CHK-0002** (นายเอก มั่นคง) | ☐ |

### TC-C03 — Esc / ปิด issue drawer โดยไม่ออกใบ (AC-05)
- group: C · ความสำคัญ: กลาง · trace: AC-05 / dismiss
- Setup: seed=default · files=—
- Start: OPEN `#/receivings` → CLICK **ออกใบรับอ้อย** (แถว CHK-0001)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | กด **Esc** | — | drawer ปิด · กลับ list รอผลเท (4 รายการ) · CHK-0001 ยังเป็น Draft | ☐ |
| 2 | CLICK **ออกใบรับอ้อย** (แถว CHK-0001) อีกครั้ง → CLICK **ปิด** (footer) | — | drawer ปิด · CHK-0001 ยัง Draft (count รอผลเท = **4**) | ☐ |

### TC-C04 — dump section: BR-CR-11 dump เฉพาะ Draft (AC-05 / BR-CR-11)
- group: C · ความสำคัญ: สูง · trace: AC-05 / BR-CR-11
- Setup: seed=default · files=—
- Start: OPEN `#/receivings/issued`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แถว **CHK-0005** (Issued · เปิด detail drawer) | — | detail drawer (ไม่ใช่ issue drawer) · **ไม่มี** ปุ่ม ดึงผลการเท (Auto) — Issued แล้วดึงซ้ำไม่ได้ · footer มีปุ่ม **Void** / **พิมพ์** / **ปิด** | ☐ |
| 2 | VERIFY: ปุ่ม ออกใบรับอ้อย มีเฉพาะแถว Draft | — | tab รอผลเท เท่านั้นที่ row-action มี **ออกใบรับอ้อย** (Issued/Void ไม่มี) | ☐ |

---

## Group D — Dump Result v2 auto (US-02) ⭐

### TC-D01 — ดึงผลการเท (Auto) สำเร็จ → card v2 + lock + Auto badge (happy — AC-06 / EC-01 / BR-CR-01/02/03)
- group: D · ความสำคัญ: สูงสุด · trace: AC-06 / EC-01 / BR-CR-01/02/03 · XT-02
- Setup: seed=default · files=—
- Start: OPEN `#/receivings` → CLICK **ออกใบรับอ้อย** (แถว CHK-0001)
- ผ่านเมื่อ: card v2 read-only + ค่าตรง ชุด A

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ดึงผลการเท (Auto)** → WAIT ~1s | — | (ระหว่างรอ icon หมุน spin) จากนั้น toast **ดึงผลการเทสำเร็จ** | ☐ |
| 2 | VERIFY card v2 | — | header **ดึงผลการเทสำเร็จ (ล็อกค่า)** + pill **Auto** · cells: ประเภทอ้อย **05 - อ้อยสด (Fresh Cane)** · เลขเหรียญชั่ง **10501** · เวลาเข้า (Time In) **08:15** · เวลาออก (Time Out) **08:32** · น.น. รวม (กก.) **32,000.00** · น.น. รถเบา (กก.) **12,000.00** · น.น. อ้อยสุทธิ (กก.) **20,000.00** | ☐ |
| 3 | VERIFY ล็อก read-only | — | card ไม่มี input แก้ไขได้ (ค่าทั้งหมดเป็น text ล็อก) · badge Auto คงอยู่ | ☐ |

### TC-D02 — dump v2 ไม่มี CCS (AC-06 / XT-02)
- group: D · ความสำคัญ: สูงสุด · trace: AC-06 / XT-02 (CCS moved to Payment)
- Setup: seed=default · files=—
- Start: OPEN `#/receivings` → CLICK **ออกใบรับอ้อย** (แถว CHK-0001) → CLICK **ดึงผลการเท (Auto)** → WAIT

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY fields ใน card v2 | — | มีเฉพาะ ประเภทอ้อย + Time In/Out + น.น.รวม/รถเบา/สุทธิ · **ไม่มี** ช่อง CCS / ค่าความหวาน (ย้ายไป Cane Payment) | ☐ |

### TC-D03 — หลังดึงผล → ปุ่ม ออกใบรับอ้อย enabled (AC-06 / AC-11)
- group: D · ความสำคัญ: สูง · trace: AC-06, AC-11 / issue gate
- Setup: seed=default · files=—
- Start: OPEN `#/receivings` → CLICK **ออกใบรับอ้อย** (แถว CHK-0001)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ก่อนดึงผล | — | ปุ่ม footer **ออกใบรับอ้อย** = disabled | ☐ |
| 2 | CLICK **ดึงผลการเท (Auto)** → WAIT | — | หลัง card v2 ปรากฏ · ปุ่ม footer **ออกใบรับอ้อย** = enabled (คลิกได้) | ☐ |

---

## Group E — Manual fallback + validation (US-02)

### TC-E01 — จำลองไม่พบผล → error + Manual mode (negative — AC-07 / EC-02 / BR-CR-02)
- group: E · ความสำคัญ: สูงสุด · trace: AC-07 / EC-02 / BR-CR-02
- Setup: seed=default · files=—
- Start: OPEN `#/receivings` → CLICK **ออกใบรับอ้อย** (แถว CHK-0001)
- ผ่านเมื่อ: error + สลับ Manual + ช่องกรอกมือโผล่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **จำลองไม่พบผล** → WAIT | — | toast **ไม่พบผลการเทจากโรงงาน** · badge เปลี่ยนเป็น **Manual** | ☐ |
| 2 | VERIFY Manual mode | — | warn note **ไม่พบผลการเทจากโรงงาน — กรุณาเปลี่ยนเป็นโหมด Manual** · field **น.น. อ้อยสุทธิ (กก.)** (placeholder **เช่น 20000.00**) + **เหตุผล** (placeholder **เหตุผลที่ต้องกรอกด้วยตนเอง...**) · ปุ่ม **รีเซ็ต / กลับไป Auto** | ☐ |

### TC-E02 — สลับเป็นโหมดกรอกมือ (ไม่ผ่าน fail) (AC-07)
- group: E · ความสำคัญ: กลาง · trace: AC-07 / manual toggle
- Setup: seed=default · files=—
- Start: OPEN `#/receivings` → CLICK **ออกใบรับอ้อย** (แถว CHK-0002)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **สลับเป็นโหมดกรอกมือ** | — | badge **Manual** · field **น.น. อ้อยสุทธิ (กก.)** + **เหตุผล** โผล่ · **ไม่มี** warn note (ไม่ได้มาจาก fail) · ปุ่ม **รีเซ็ต / กลับไป Auto** | ☐ |

### TC-E03 — manual net ผิดรูปแบบ → block (negative — AC-09 / VR-02 / EC-04)
- group: E · ความสำคัญ: สูงสุด · trace: AC-09 / VR-02 / EC-04
- Setup: seed=default · files=—
- Start: OPEN `#/receivings` → CLICK **ออกใบรับอ้อย** (แถว CHK-0001) → CLICK **สลับเป็นโหมดกรอกมือ**
- ชุดข้อมูล: B1 / B2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE น.น. **-5** + เหตุผล **ชั่งใหม่** → CLICK **ออกใบรับอ้อย** → WAIT | B1 | toast **กรุณากรอกน้ำหนักสุทธิเป็นจำนวนไม่ลบและ 2 ตำแหน่ง** · ไม่ออกใบ (ยังอยู่ drawer) | ☐ |
| 2 | แก้ น.น. เป็น **20000.999** (3 ตำแหน่ง) → CLICK **ออกใบรับอ้อย** → WAIT | B2 | toast **กรุณากรอกน้ำหนักสุทธิเป็นจำนวนไม่ลบและ 2 ตำแหน่ง** | ☐ |

### TC-E04 — manual net ว่าง → guard (negative — AC-08 / VR-01 / EC-03)
- group: E · ความสำคัญ: สูง · trace: AC-08 / VR-01 / EC-03 · **guard: ปุ่ม disabled · toast กรุณากรอกน้ำหนักสุทธิ = server-guard (defensive)**
- Setup: seed=default · files=—
- Start: OPEN `#/receivings` → CLICK **ออกใบรับอ้อย** (แถว CHK-0001) → CLICK **สลับเป็นโหมดกรอกมือ**
- ชุดข้อมูล: B3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เว้น **น.น. อ้อยสุทธิ** ว่าง → TYPE เหตุผล **ชั่งใหม่** เท่านั้น | B3 | ปุ่ม footer **ออกใบรับอ้อย** ยัง **disabled** (กดไม่ได้) — บังคับกรอกน้ำหนักก่อน | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): submit ทั้งที่ net ว่าง | — | toast **กรุณากรอกน้ำหนักสุทธิ** (server-guard · UI disable ป้องกันไว้แล้ว) | ☐ (ต้อง simulate) |

### TC-E05 — manual ไม่ใส่เหตุผล → guard (negative — AC-10 / VR-03 / EC-05)
- group: E · ความสำคัญ: สูง · trace: AC-10 / VR-03 / EC-05 · **guard: ปุ่ม disabled · toast กรุณากรอกเหตุผลการกรอกด้วยตนเอง = server-guard**
- Setup: seed=default · files=—
- Start: OPEN `#/receivings` → CLICK **ออกใบรับอ้อย** (แถว CHK-0001) → CLICK **สลับเป็นโหมดกรอกมือ**
- ชุดข้อมูล: B4

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE **น.น. อ้อยสุทธิ 20000.00** → เว้น **เหตุผล** ว่าง | B4 | ปุ่ม footer **ออกใบรับอ้อย** ยัง **disabled** — บังคับกรอกเหตุผลก่อน | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): submit ทั้งที่ reason ว่าง | — | toast **กรุณากรอกเหตุผลการกรอกด้วยตนเอง** (server-guard) | ☐ (ต้อง simulate) |

### TC-E06 — รีเซ็ต / กลับไป Auto (AC-06/07)
- group: E · ความสำคัญ: กลาง · trace: AC-06, AC-07 / reset
- Setup: seed=default · files=—
- Start: OPEN `#/receivings` → CLICK **ออกใบรับอ้อย** (แถว CHK-0001) → CLICK **สลับเป็นโหมดกรอกมือ**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE น.น. **18500.00** + เหตุผล **ทดสอบ** → CLICK ปุ่ม **รีเซ็ต / กลับไป Auto** | — | badge กลับเป็น **Auto** · ช่อง manual หาย · กลับ note **กดปุ่ม "ดึงผลการเท (Auto)" …** · ปุ่ม footer ออกใบรับอ้อย = disabled อีกครั้ง | ☐ |

---

## Group F — ออกใบรับอ้อย + side effects (US-02) ⭐

### TC-F01 — ออกใบ auto สำเร็จ → CRN + ย้าย เทแล้ว + toast (happy — AC-11 / EC-06 / XT-03 / BR-CR-04) ★
- group: F · ความสำคัญ: สูงสุด · trace: AC-11 / EC-06 / XT-03 / BR-CR-04 · side effects
- Setup: seed=default · files=—
- Start: OPEN `#/receivings` → CLICK **ออกใบรับอ้อย** (แถว CHK-0001)
- ชุดข้อมูล: A
- ผ่านเมื่อ: ดึงผล → ออกใบ → ย้าย tab + CRN + toast desc

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ดึงผลการเท (Auto)** → WAIT → CLICK **ออกใบรับอ้อย** (footer) → WAIT | A | drawer ปิด + หน้าเด้งไป tab **เทแล้ว** + toast **ออกใบรับอ้อยสำเร็จ** (desc **CBM → awaiting_payment · ปลดเหรียญชั่ง · สร้าง PDF**) | ☐ |
| 2 | VERIFY แถวใหม่ (tab เทแล้ว) | — | เลขที่ใบรับ **CRN-2568-00004** (มี **Q10001** ใต้) · ผู้ขนส่ง **นายสมชาย ใจดี** · น้ำหนักสุทธิ **20,000.00 กก.** · ประเภทการเทอ้อย **อ้อยสด (Fresh Cane)** · สถานะ **เทแล้ว** | ☐ |

### TC-F02 — counts/stats หลังออกใบ (AC-01 / AC-11)
- group: F · ความสำคัญ: สูง · trace: AC-01, AC-11 / count reflect
- Setup: seed=default · files=—
- Start: OPEN `#/receivings` → ออกใบ CHK-0001 (ตาม TC-F01)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY counts หลังออกใบ | — | แท็บ **รอผลเท 3** · **เทแล้ว 4** · stat **รอผลเท 3** · **ออกใบวันนี้ 4** · **น้ำหนักอ้อยรวมวันนี้ 85,000.00** (65,000 + 20,000) | ☐ |

### TC-F03 — ออกใบ manual สำเร็จ (happy — AC-11 / BR-CR-04) ★
- group: F · ความสำคัญ: สูงสุด · trace: AC-11 / BR-CR-04 · manual path
- Setup: seed=default · files=—
- Start: OPEN `#/receivings` → CLICK **ออกใบรับอ้อย** (แถว CHK-0002)
- ชุดข้อมูล: B5

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **จำลองไม่พบผล** → TYPE น.น. **18500.00** + เหตุผล **เครื่องชั่งโรงงานออฟไลน์ ชั่งด้วยมือ** → CLICK **ออกใบรับอ้อย** → WAIT | B5 | drawer ปิด + toast **ออกใบรับอ้อยสำเร็จ** · เด้งไป tab **เทแล้ว** | ☐ |
| 2 | VERIFY แถวใหม่ (manual) | — | เลขที่ใบรับ **CRN-2568-00004** · ผู้ขนส่ง **นายเอก มั่นคง** · น้ำหนักสุทธิ **18,500.00 กก.** · ประเภทการเทอ้อย **-** (manual ไม่มี caneType) · สถานะ **เทแล้ว** | ☐ |

### TC-F04 — side effects (CBM awaiting_payment · ปลดเหรียญ · PDF) (AC-11 / XT-03) (ต้อง simulate)
- group: F · ความสำคัญ: สูง · trace: AC-11 / XT-03 · **prototype: toast desc เท่านั้น · side effect จริง = SIT**
- Setup: seed=default (prototype = TC-F01) + **simulate — ระบบจริง**
- Start: OPEN `#/receivings` → ออกใบ CHK-0001

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (prototype) ออกใบ CHK-0001 → VERIFY toast desc | — | toast desc **CBM → awaiting_payment · ปลดเหรียญชั่ง · สร้าง PDF** · แถวใหม่ paymentStatus (detail) = **รอทำจ่าย** | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): side effects | — | CBM (F-AGM-007) → **awaiting_payment** · เหรียญชั่งถูกปลด (free coin) · PDF A4+QR ถูกสร้างที่ server | ☐ (ต้อง simulate) |

### TC-F05 — ออกใบซ้ำ (idempotent) → 409/no-op (EC-07 / BR-CR-05) (ต้อง simulate)
- group: F · ความสำคัญ: สูง · trace: EC-07 / BR-CR-05 · **prototype single-session · ไม่มี server — SIT**
- Setup: **simulate — ระบบจริง:** POST /cane-receivings ซ้ำ idempotency-key เดิม
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): ออกใบซ้ำด้วย checkin เดิม | — | 409 **รายการซ้ำ (idempotent)** / no-op · ไม่สร้าง CRN ซ้ำ | ☐ (ต้อง simulate) |

---

## Group G — Sync All (US-03) ⭐

### TC-G01 — Sync All ไม่เลือกวันที่ → block (negative — AC-12/13 / VR-05 / EC-08 / BR-CR-07)
- group: G · ความสำคัญ: สูงสุด · trace: AC-12, AC-13 / VR-05 / EC-08 / BR-CR-07
- Setup: seed=default (date filter ว่าง) · files=—
- Start: OPEN `#/receivings`
- ชุดข้อมูล: D1

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ปุ่ม Sync All | — | tab รอผลเท มีปุ่ม **Sync All & ออกใบรับอ้อยอัตโนมัติ** (header) | ☐ |
| 2 | CLICK **Sync All & ออกใบรับอ้อยอัตโนมัติ** (date ว่าง) → WAIT | D1 | toast **กรุณาเลือกช่วงวันที่ก่อนทำ Sync All** · ไม่มี modal · ไม่มีการออกใบ | ☐ |

### TC-G02 — Sync All (date set) → toasts + result modal summary (happy — AC-14 / EC-09 / BR-CR-06) ★
- group: G · ความสำคัญ: สูงสุด · trace: AC-14 / EC-09 / BR-CR-06 · bulk auto-issue
- Setup: seed=default · files=—
- Start: OPEN `#/receivings`
- ชุดข้อมูล: D2
- ผ่านเมื่อ: modal ผลการ Sync All + summary 4/3/1

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SET date input = **2026-07-21** → CLICK **Sync All & ออกใบรับอ้อยอัตโนมัติ** → WAIT | D2 | toast **กำลังดึงผลการเท...** → (หลัง ~1.2s) modal **ผลการ Sync All** เปิด (sub **ดึงผลการเท + ออกใบรับอ้อยอัตโนมัติ**) | ☐ |
| 2 | VERIFY summary chips | — | **ทั้งหมด 4** · **สำเร็จ 3** · **ล้มเหลว 1** | ☐ |
| 3 | VERIFY toast ปิดท้าย | — | toast **ดึงผลการเทเสร็จสิ้น** (desc **สำเร็จ 3 รายการ, ล้มเหลว 1 รายการ**) | ☐ |

### TC-G03 — Sync All failed table + error string (AC-15 / EC-10 / BR-CR-06)
- group: G · ความสำคัญ: สูงสุด · trace: AC-15 / EC-10 / BR-CR-06
- Setup: seed=default · files=—
- Start: OPEN `#/receivings` → SET date 2026-07-21 → Sync All → WAIT (modal เปิด)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY failed table | — | header **รายการที่ล้มเหลว** · 1 แถว: เวลาเข้า **09:05 21/07/26** · เหรียญ **10503** · **NBM-2568-0103** · เกษตรกร **นายมานะ ขยัน** · error **ไม่พบข้อมูลผลการเทในระบบโรงงาน** | ☐ |
| 2 | VERIFY ปุ่ม modal | — | ปุ่ม **ดูรายการที่ล้มเหลว** + **ปิด** | ☐ |

### TC-G04 — ปุ่ม ดูรายการที่ล้มเหลว / ปิด (AC-16)
- group: G · ความสำคัญ: สูง · trace: AC-16 / modal actions
- Setup: seed=default · files=—
- Start: OPEN `#/receivings` → SET date 2026-07-21 → Sync All → WAIT (modal เปิด)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **ดูรายการที่ล้มเหลว** | — | modal ปิด · กลับ tab **รอผลเท** (URL #/receivings) · เหลือรายการที่ล้มเหลว (CHK-0003) ใน list | ☐ |

### TC-G05 — Sync All ย้ายรายการสำเร็จไป เทแล้ว (AC-14 / EC-09)
- group: G · ความสำคัญ: สูง · trace: AC-14 / EC-09 · state移动
- Setup: seed=default · files=—
- Start: OPEN `#/receivings` → SET date 2026-07-21 → Sync All → WAIT → CLICK **ปิด**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY tab รอผลเท หลัง Sync | — | เหลือ 1 แถว **CHK-0003** (ล้มเหลว) · แท็บ **รอผลเท 1** | ☐ |
| 2 | CLICK tab **เทแล้ว** → VERIFY | — | count **เทแล้ว 6** (3 เดิม + 3 auto-issued) · มีแถวใหม่ CRN-2568-00004..00006 (ประเภทการเทอ้อย **อ้อยสด (Fresh Cane)** · น้ำหนักสุทธิ **20,000.00 กก.**) | ☐ |

### TC-G06 — Sync All idempotency / ไม่รันซ้อน (BR-CR-07) (ต้อง simulate)
- group: G · ความสำคัญ: กลาง · trace: BR-CR-07 · **prototype single-run · 409/concurrency = SIT**
- Setup: **simulate — ระบบจริง:** Sync All async batch · POST ซ้ำ idempotency-key เดิม
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): กด Sync All ซ้อนตอนกำลังรัน | — | ไม่รันซ้อน (บล็อค/คิว) · batch idempotent · รายการที่ออกใบแล้วไม่ออกซ้ำ (409/no-op) | ☐ (ต้อง simulate) |

---

## Group H — Detail drawer + PDF + QR/Search (US-04/05/07)

### TC-H01 — detail drawer Draft (dump = "-") (AC-17)
- group: H · ความสำคัญ: สูง · trace: AC-17 / detail draft
- Setup: seed=default · files=—
- Start: OPEN `#/receivings`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK รหัสเกษตรกร **Q10001** (แถว CHK-0001) | — | detail drawer เปิด · URL = **#/receivings/CHK-0001** · eyebrow **การรับอ้อย · CHK-0001** · title **นายสมชาย ใจดี** + pill **รอผลเท** | ☐ |
| 2 | VERIFY section ผลการเทจากโรงงาน (Draft) | — | badge **-** · ประเภทอ้อย **-** · เวลาเข้า/ออก **-** · น.น.รวม/รถเบา/สุทธิ **-** | ☐ |
| 3 | VERIFY footer (Draft) | — | ปุ่ม **ออกใบรับอ้อย** (primary) + **ปิด** · ไม่มี Void/พิมพ์ | ☐ |

### TC-H02 — detail drawer Issued (dump v2 read-only + doc info) (AC-17)
- group: H · ความสำคัญ: สูงสุด · trace: AC-17 / detail issued
- Setup: seed=default · files=—
- Start: OPEN `#/receivings/issued`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK เลขที่ใบรับ **CRN-2568-00001** (แถว CHK-0005) | — | detail drawer · eyebrow **การรับอ้อย · CRN-2568-00001** · title **นายประสิทธิ์ ทองมา** + pill **เทแล้ว** | ☐ |
| 2 | VERIFY section ผลการเทจากโรงงาน | — | badge **Auto** · ประเภทอ้อย **05 - อ้อยสด (Fresh Cane)** · น.น. รวม **30,000.00** · น.น. รถเบา **10,000.00** · น.น. อ้อยสุทธิ **20,000.00** (read-only) | ☐ |
| 3 | VERIFY section ข้อมูลเอกสาร | — | เลขที่ใบรับอ้อย **CRN-2568-00001** · สถานะ pill **เทแล้ว** · สถานะการชำระเงิน **รอทำจ่าย** · คืนเหรียญชั่ง **คืนแล้ว** · ออกใบเมื่อ **07:50 21/07/26** · ออกใบโดย **สมพร วงศ์ทะเบียน** | ☐ |
| 4 | VERIFY footer (Issued) | — | ปุ่ม **Void** + **พิมพ์** + **ปิด** | ☐ |

### TC-H03 — detail refresh-safe route (AC-17)
- group: H · ความสำคัญ: กลาง · trace: AC-17 / route refresh-safe
- Setup: seed=default · files=—
- Start: OPEN `#/receivings/issued`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK เลขที่ใบรับ **CRN-2568-00003** (CHK-0007) → VERIFY URL | — | URL = **#/receivings/CHK-0007** · drawer เปิด | ☐ |
| 2 | F5 (refresh) | — | drawer CHK-0007 เปิดใหม่อัตโนมัติ (refresh-safe) | ☐ |
| 3 | CLICK **ปิด** | — | drawer ปิด · กลับ tab เทแล้ว (3 รายการ) | ☐ |

### TC-H04 — PDF viewer จากปุ่ม พิมพ์ (Issued) (AC-18 / BR-CR-04)
- group: H · ความสำคัญ: สูง · trace: AC-18 / BR-CR-04 · **PDF จริง (A4+QR server) = SIT**
- Setup: seed=default · files=—
- Start: OPEN `#/receivings/issued`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม printer (**พิมพ์**) บนแถว CHK-0005 | — | modal · title **ใบรับอ้อย (PDF)** · sub **CRN-2568-00001 · ตัวอย่างเอกสาร** · body หัว **ใบรับอ้อย (Cane Receiving)** + มี QR box · ปุ่ม **ปิด** / **พิมพ์** | ☐ |
| 2 | CLICK ปุ่ม **พิมพ์** (ใน modal) | — | toast **กำลังส่งไปยังเครื่องพิมพ์...** | ☐ |
| 3 | VERIFY (ระบบจริง — SIT): PDF A4+QR จริง | — | PDF ไทย A4 + QR render จาก server (prototype = HTML mockup) | ☐ (ต้อง simulate) |

### TC-H05 — พิมพ์ ไม่มี PDF → "ไม่พบ PDF" (AC-18)
- group: H · ความสำคัญ: กลาง · trace: AC-18 / no pdf
- Setup: seed=default (CHK-0008 pdfUrl ว่าง) · files=—
- Start: OPEN `#/receivings/void`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม printer (**พิมพ์**) บนแถว **CHK-0008** | — | ไม่มี modal · toast **ไม่พบ PDF** | ☐ |

### TC-H06 — Scan QR + ค้นหาเลขเหรียญชั่ง → issue flow (AC-22)
- group: H · ความสำคัญ: สูง · trace: AC-22 / QR + search entry
- Setup: seed=default · files=—
- Start: OPEN `#/receivings`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **Scan QR** (header) | — | modal · title **สแกน QR** · sub **สแกน QR หรือป้อนรหัส Booking เพื่อเปิดใบรับอ้อย** · helper **เล็งกล้องไปที่ QR Code บนใบเช็คอิน** · field **หรือป้อนรหัส Booking** (placeholder **CBM-2568-....**) + ปุ่ม **ไป** | ☐ |
| 2 | TYPE **CBM-2568-0104** → CLICK **ไป** → WAIT | — | modal ปิด · เปิด Issue drawer **ออกใบรับอ้อย · CHK-0004** (นางสมหญิง รักดี) | ☐ |
| 3 | Esc → CLICK **ค้นหาเลขเหรียญ** (header) → TYPE **10503** → CLICK **ไป** | — | modal ค้นหาปิด · เปิด Issue drawer **ออกใบรับอ้อย · CHK-0003** (นายมานะ ขยัน) | ☐ |

---

## Group I — Void (+ blocked-if-paid) (US-06) ⭐

### TC-I01 — เปิด void modal + note (AC-20 / BR-CR-09)
- group: I · ความสำคัญ: สูง · trace: AC-20 / BR-CR-09 / void form
- Setup: seed=default · files=—
- Start: OPEN `#/receivings/issued`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม x-circle (**Void**) บนแถว **CHK-0007** (CRN-2568-00003) | — | modal · title **ยกเลิกใบรับอ้อย** · sub **CRN-2568-00003** · warn note **การยกเลิกจะย้อนสถานะ CBM เป็น awaiting_dump_result และไม่สามารถชำระเงินต่อ** · field **เหตุผลการยกเลิก** (placeholder **กรุณากรอกเหตุผลการยกเลิก (อย่างน้อย 5 ตัวอักษร)**) · ปุ่ม **ยกเลิก** / **ยืนยัน Void** | ☐ |

### TC-I02 — void reason <5 → block (negative — AC-19 / VR-04 / EC-11)
- group: I · ความสำคัญ: สูงสุด · trace: AC-19 / VR-04 / EC-11
- Setup: seed=default · files=—
- Start: OPEN `#/receivings/issued` → CLICK **Void** (แถว CHK-0007)
- ชุดข้อมูล: C1

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE เหตุผล **สั้น** (4 ตัว) → CLICK **ยืนยัน Void** → WAIT | C1 | toast **เหตุผลต้องมีความยาวอย่างน้อย 5 ตัวอักษร** · ไม่ void (ยังอยู่ modal) | ☐ |

### TC-I03 — void สำเร็จ → Void tab + toast (happy — AC-20 / EC-12 / XT-05 / BR-CR-09) ★
- group: I · ความสำคัญ: สูงสุด · trace: AC-20 / EC-12 / XT-05 / BR-CR-09
- Setup: seed=default · files=—
- Start: OPEN `#/receivings/issued` → CLICK **Void** (แถว CHK-0007)
- ชุดข้อมูล: C2
- ผ่านเมื่อ: void → toast + ย้ายไป ยกเลิก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE เหตุผล **น้ำหนักผิด ต้องชั่งใหม่** → CLICK **ยืนยัน Void** → WAIT | C2 | modal ปิด · เด้งไป tab **ยกเลิก** (URL #/receivings/void) · toast **Void ใบรับอ้อยสำเร็จ** | ☐ |
| 2 | VERIFY tab ยกเลิก + counts | — | มีแถว CHK-0007 (CRN-2568-00003) สถานะ pill **ยกเลิก** · แท็บ **เทแล้ว 2** · **ยกเลิก 2** · stat **ออกใบวันนี้ 2** · **ยกเลิก 2** | ☐ |

### TC-I04 — void ที่ชำระเงินแล้ว → block (negative — AC-21 / EC-13 / BR-CR-10) ★
- group: I · ความสำคัญ: สูงสุด · trace: AC-21 / EC-13 / BR-CR-10
- Setup: seed=default (CHK-0006 paymentStatus=ชำระเงินแล้ว) · files=—
- Start: OPEN `#/receivings/issued` → CLICK **Void** (แถว CHK-0006)
- ชุดข้อมูล: C3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม x-circle (**Void**) บนแถว **CHK-0006** (CRN-2568-00002) | C3 | modal **ยกเลิกใบรับอ้อย** · body = paid-block note **รายการนี้ชำระเงินแล้ว จึงไม่สามารถยกเลิก (Void) ได้** · ปุ่ม **ยืนยัน Void** = **disabled** | ☐ |
| 2 | (ถ้า bypass) attempt ยืนยัน Void | C3 | toast **ไม่สามารถยกเลิกรายการที่ชำระเงินแล้ว** · CHK-0006 ยังสถานะ **เทแล้ว** | ☐ |

### TC-I05 — void cancel (ปิด modal ไม่ยืนยัน) (AC-20)
- group: I · ความสำคัญ: กลาง · trace: AC-20 / void cancel
- Setup: seed=default · files=—
- Start: OPEN `#/receivings/issued` → CLICK **Void** (แถว CHK-0005)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ใน modal CLICK **ยกเลิก** (ghost) | — | modal ปิด · แถว CHK-0005 ยัง **เทแล้ว** · แท็บ เทแล้ว = **3** (ไม่ลด) | ☐ |
| 2 | CLICK **Void** (CHK-0005) อีกครั้ง → กด **Esc** | — | modal ปิด · CHK-0005 ยัง เทแล้ว | ☐ |

---

## Group J — Cross-module / event XT-01..05 + simulate (06_TESTS §6.9) ⭐

### TC-J01 — XT-01: Draft = checked-in ยังไม่ออกใบ (Check-in F-AGM-010) (ต้อง simulate)
- group: J · ความสำคัญ: สูง · trace: XT-01 · **prototype: seed fixed · Check-in source จริง = SIT**
- Setup: seed=default (prototype) + **simulate — ระบบจริง:** อ่าน checked-in ที่ยังไม่ออกใบ
- Start: OPEN `#/receivings`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (prototype) VERIFY tab รอผลเท | — | 4 แถว Draft (receiving_id NULL · dumpResultSource `-`) = รายการ checked-in รอออกใบ | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): source Check-in | — | รายการ Draft ตรงกับ Check-in (F-AGM-010) ที่ status=checked-in · receiving_id ยัง NULL | ☐ (ต้อง simulate) |

### TC-J02 — XT-02: ดึงผลการเท v2 จาก Factory dump API (ต้อง simulate)
- group: J · ความสำคัญ: สูง · trace: XT-02 / BR-CR-01 · **prototype: mock deterministic · dump API จริง = SIT**
- Setup: **simulate — ระบบจริง:** query checkin_datetime + weigh_coin + quota_id → dump v2
- Start: — (SIT) (prototype = TC-D01)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): ดึงผลการเทจากโรงงานจริง | — | คืน caneType + Time In/Out + gross/tare/net (**ไม่มี CCS**) จาก factory scale จริง (prototype = ค่า fix 05/32000/12000/20000) | ☐ (ต้อง simulate) |

### TC-J03 — XT-03: ออกใบ → CBM awaiting_payment + free coin (idempotent) (ต้อง simulate)
- group: J · ความสำคัญ: สูงสุด · trace: XT-03 / BR-CR-04/05 · **prototype: toast desc · event จริง = SIT**
- Setup: seed=default (prototype = TC-F01) + **simulate — ระบบจริง:** event → CBM (F-AGM-007)
- Start: OPEN `#/receivings` → ออกใบ CHK-0001

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (prototype) ออกใบ CHK-0001 → VERIFY | — | toast desc **CBM → awaiting_payment · ปลดเหรียญชั่ง · สร้าง PDF** | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): CBM + coin | — | CBM ปลายทาง → **awaiting_payment** · ปลดเหรียญ (free coin) · ยิงซ้ำ = idempotent (ไม่เปลี่ยนซ้ำ / 409) | ☐ (ต้อง simulate) |

### TC-J04 — XT-04: Receiving → Payment (net_weight + cane_type SoT) (ต้อง simulate)
- group: J · ความสำคัญ: สูงสุด · trace: XT-04 / BR-CR-08 · **prototype: local only · Payment handoff = SIT**
- Setup: **simulate — ระบบจริง:** Receiving = SoT ส่ง net_weight + cane_type ให้ Cane Payment
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): ส่งต่อ Payment | — | Cane Payment รับ **net_weight + cane_type** จาก Receiving (SoT) · CCS คำนวณที่ Payment (ไม่ใช่ Receiving) | ☐ (ต้อง simulate) |

### TC-J05 — XT-05: void → CBM awaiting_dump_result rollback (ต้อง simulate)
- group: J · ความสำคัญ: สูง · trace: XT-05 / BR-CR-09 · **prototype: void local · reversal จริง = SIT**
- Setup: seed=default (prototype = TC-I03) + **simulate — ระบบจริง:** void ยิง rollback event
- Start: OPEN `#/receivings/issued` → void CHK-0007

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (prototype) void CHK-0007 → VERIFY | — | toast **Void ใบรับอ้อยสำเร็จ** · สถานะ **ยกเลิก** · detail note "ยกเลิกเมื่อ … · เหตุผล: …" | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): CBM rollback | — | CBM ปลายทาง → **awaiting_dump_result** · block ชำระเงินต่อ · reversal event append | ☐ (ต้อง simulate) |

### TC-J06 — ประเภทอ้อย filter · net cross-check · unknown cane type · RBAC (ต้อง simulate)
- group: J · ความสำคัญ: กลาง · trace: AC-02 (ประเภทอ้อย) / EC-14 / BR-CR-12 / §5.3 · **prototype ทำไม่ได้ — SIT**
- Setup: **simulate — ระบบจริง**
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): filter ประเภทอ้อย | — | มี dropdown ประเภทอ้อย กรองตาม caneType (prototype filter bar ไม่มี) | ☐ (ต้อง simulate) |
| 2 | VERIFY (ระบบจริง): net cross-check (gross-tare≠net) | — | เก็บทั้ง gross/tare/net เพื่อ debug (EC-14) | ☐ (ต้อง simulate) |
| 3 | VERIFY (ระบบจริง): cane type ไม่รู้จัก | — | คง code · Payment adjustment 0 + เตือน (ฝั่ง Payment · BR-CR-12) | ☐ (ต้อง simulate) |
| 4 | VERIFY (ระบบจริง): RBAC Viewer/Supervisor | — | Viewer ไม่เห็น Sync All/create · Supervisor/Admin manual override + void (prototype = Receiving Staff allow ครบ) | ☐ (ต้อง simulate) |

---

## วิธีที่ agent รัน (Run protocol)

1. เปิด `cane-receiving-management.html` ใน browser (desktop ≥1280px) — รอ ~2s ให้ font/icon โหลด
2. **ทุกเคสเริ่มด้วย refresh (F5)** แล้ว OPEN route ตาม `Start:` — mock in-memory, refresh = reset seed 4 Draft + 3 Issued + 1 Void (ทำให้เคส independent)
3. ทำตาม step ตามลำดับ — Action ขึ้นต้น verb (OPEN/CLICK/TYPE/SET/SELECT/VERIFY/WAIT)
4. `WAIT` = รอ ≤3s จน Expected ปรากฏ (toast มุมขวาล่าง · ดึงผลการเท (Auto) ~1s · Sync All ~1.2s · toast แสดง ~3.2-4.2s)
5. **Dump v2:** ดึงผลการเท (Auto) → card ล็อก `05 - อ้อยสด (Fresh Cane)` + Time In/Out + รวม/รถเบา/สุทธิ (**ไม่มี CCS**) · จำลองไม่พบผล → Manual (net 2-dec + เหตุผล)
6. **ออกใบ:** auto มีผล / manual ครบ → `ออกใบรับอ้อยสำเร็จ` + CRN-2568-##### + ย้าย Draft → Issued · desc `CBM → awaiting_payment · ปลดเหรียญชั่ง · สร้าง PDF`
7. **Manual validation:** ปุ่ม ออกใบรับอ้อย disabled จนกรอกครบ (net+เหตุผล) → VR-01/VR-03 เป็น guard ที่ปุ่ม-disable · VR-02 (format ติดลบ/3 ตำแหน่ง) reachable เต็ม
8. **Sync All:** date ว่าง → `กรุณาเลือกช่วงวันที่ก่อนทำ Sync All` · date set → `กำลังดึงผลการเท...` → modal `ผลการ Sync All` (4/3/1) → `ดึงผลการเทเสร็จสิ้น (สำเร็จ 3, ล้มเหลว 1)` · CHK-0003 = ล้มเหลว (`ไม่พบข้อมูลผลการเทในระบบโรงงาน`)
9. **Void:** reason≥5 · CHK-0007 = void ได้ · **CHK-0006 (ชำระเงินแล้ว) → ปุ่ม ยืนยัน Void disabled + `ไม่สามารถยกเลิกรายการที่ชำระเงินแล้ว`**
10. **PDF:** พิมพ์ (Issued) → modal PDF A4+QR · CHK-0008 (void · ไม่มี pdf) → `ไม่พบ PDF`
11. step ไหน Expected ไม่ตรง = FAIL เคสนั้น → บันทึก `failed_step` + `evidence` แล้วไปเคสถัดไป
12. เคส `(ต้อง simulate)` — ถ้ารันบน prototype ทำไม่ได้ ให้ status = `blocked` + note "SIT case"

## Coverage Audit

| หมวด | covered / total |
|---|---|
| Stories/AC (06_TESTS §6.1) | 22 / 22 (AC-01..22 · AC-08/10 = guard, message defensive = simulate) |
| Cross-Module / Event (XT-01..05) | 5 / 5 (event/API/handoff จริง = simulate) |
| Business rules (BR-CR-01..12) | 12 / 12 (BR-CR-08/12 = simulate) |
| Validation (VR-01..05) | 5 / 5 (VR-01/03 = guard + defensive) |
| Edge cases (EC-01..14) | 14 / 14 (EC-07/14 = simulate) |
| Error catalog (UI-observable) | ครบ · DUMP_NOT_FOUND/VALIDATION/VOID_BLOCKED_PAID/SYNC_ALL_DATE บน prototype · 409 dup = simulate |
| Permission cells | Receiving Staff allow ครบ · Viewer/Supervisor RBAC = simulate |
| Dump v2 + ออกใบ + Sync All + Void | ครบทุกชั้น (auto/manual + issue side-effects + bulk + void/paid-block) |

- **Manifest cross-check (FRD §0.12): ✅ 22 AC + 5 XT + 12 BR + 5 VR + 14 EC — ทุกแถวมีคู่ใน Ledger**

### เคส (ต้อง simulate) / SIT
- TC-B04 step 4 (filter ประเภทอ้อย — ไม่มีใน prototype)
- TC-B05 step 3 (no-data variant — seed มี record เสมอ)
- TC-B06 step 2 (ไฟล์ CSV จริง — server-side)
- TC-E04 step 2 / TC-E05 step 2 (VR-01/VR-03 message — guarded by button-disable)
- TC-F04 step 2 (CBM awaiting_payment + ปลดเหรียญ + PDF server จริง)
- TC-F05 (ออกใบซ้ำ 409/no-op idempotent)
- TC-G06 (Sync All ไม่รันซ้อน / idempotency 409)
- TC-H04 step 3 (PDF A4+QR server render จริง)
- TC-J01..J05 (Check-in source / dump API / CBM event / Payment SoT / void reversal จริง)
- TC-J06 (ประเภทอ้อย filter · net cross-check · unknown cane type · RBAC)

## Result Report (schema)

```json
{
  "feature_id": "F-AGM-011",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-A01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 54, "pass": 0, "fail": 0, "blocked": 0 }
}
```
</content>
</invoke>
