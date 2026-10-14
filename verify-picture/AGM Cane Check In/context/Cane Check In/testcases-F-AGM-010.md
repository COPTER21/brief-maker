# AI Test Cases — F-AGM-010 Cane Check-In (เช็คอินรับอ้อยที่โรงงาน)

ชุด test case สำหรับ **AI agent (browser-use / vision)** รันบน prototype `cane-checkin-management.html`
ทุก anchor คือข้อความที่เห็นบนจอจริง (ยืนยันกับ FRD 06_TESTS §6.10 microcopy + 05_RULES + สแกน prototype แล้ว) · Expected เช็คได้ด้วยตา
เคสที่ prototype จำลองไม่ได้ (**Booking API 200 / event CHECK_IN จริง** · **sync 409/no-op idempotent** · **retry ล้มซ้ำ (backoff จริง)** · **scale-hardware weighToken จริง** · **Quota/Member master lookup จริง** · **NBM doc gen ฝั่ง server** · **Booking reversal event ตอน void** · **ไฟล์ CSV จริง** · **filter วันที่**) ติด `(ต้อง simulate)` — รันซ้ำกับระบบจริงตอน SIT

> ⚠ **หมายเหตุ sync retry:** prototype fix ให้ **retry ครั้งแรกสำเร็จเสมอ** (deterministic) → seed CBM-2568-0000006 กด retry 1 ครั้งได้ `ซิงก์สถานะ Booking สำเร็จ` · ครั้งถัด ๆ ไปสุ่ม 50/50 → เคส `ซิงก์ล้มเหลว กรุณาลองใหม่` + backoff/auto-retry จริง = `(ต้อง simulate)`

> ⚠ **หมายเหตุ role:** prototype fix `CURRENT_ROLE = 'เจ้าหน้าที่ชั่ง'` · `canWrite = true` เสมอ · ปุ่ม เช็คอิน/retry/void แสดงครบ · RBAC ฝั่งหัวหน้ากะ/permission จริง = `(ต้อง simulate)` ที่ SIT

## Meta

| Field | Value |
|---|---|
| Feature ID | F-AGM-010 (AGM/CHECKIN — เช็คอินรับอ้อยที่โรงงาน) |
| App entry | เปิดไฟล์ `cane-checkin-management.html` ใน browser (Chrome desktop ≥1280px) |
| Routes | `#/checkins` (tab **ต้องส่ง** — default) · `#/checkins/checked-in` (tab **เช็คอินแล้ว**) · `#/checkins/:id` (detail drawer 680px, refresh-safe) |
| Top tabs (page-level) | **ต้องส่ง** (pending) · **เช็คอินแล้ว** (checked-in) |
| Overlays (ไม่ผูก route) | method chooser modal · cbm / member / central / qr / void modal · view drawer (ผูก route) |
| ที่มา | FRD_F-AGM-010_Pack (06_TESTS AC-01..22 + XT-01..05 · 05_RULES BR-CI-01..10 / VR-01..05 / EC-01..15) |
| จำนวนเคส | 54 เคส / 10 groups |
| Signature ⭐⭐⭐ | **factory-gate/scale check-in + Booking sync**: 3 วิธีเช็คอิน (CBM/สมาชิก/โควต้ากลาง) → CBM sync กลับ Cane Booking (F-AGM-007) |
| หัวใจ 1 — CBM sync | เช็คอิน CBM booked → event CHECK_IN → booking `รอผลการเท` (idempotent checkin_id) |
| หัวใจ 2 — สถานะ Booking column | เฉพาะ tab เช็คอินแล้ว · CBM (โควต้าจองคิว) โชว์ badge · sync ล้ม = `ซิงก์ล้มเหลว` + retry · non-CBM = `-` |
| หัวใจ 3 — weighToken บังคับ | ทุกวิธีต้องมีเลขเหรียญชั่ง · CBM ว่าง → `กรุณาใส่เลขเหรียญชั่ง` |
| หัวใจ 4 — payment bill | Member/Central ต้องเลือก งวดที่ 1 + งวดที่ 2 (บิลเขียว/บิลขาว) → ไม่ครบ = `กรุณาเลือกประเภทการชำระเงินให้ครบถ้วน` |
| หัวใจ 5 — entry-type → doc | จองคิว = CBM (sync) · ไม่จองคิว/กลาง = NBM (สร้างใหม่ · no sync) |
| หมายเหตุ mock | prototype in-memory: refresh (F5) = reset seed 3 pending + 5 checked-in — ใช้เป็นข้อดี: ทุกเคส independent โดย refresh ก่อนเริ่ม · void ลบ record ออกจริง (ไม่ soft-delete) |
| Cross-module ⭐ | CBM check-in → **Cane Booking รับ event (F-AGM-007)** · member → **Quota/Member master (read)** · void → **Booking reversal** = `(ต้อง simulate)` ที่ SIT |

**Seed tab ต้องส่ง (pending · 3 รายการ · status จัดส่ง · entryType โควต้าจองคิว · ยังไม่เช็คอิน):**

| รหัสเอกสาร | โควต้า | เกษตรกร/ผู้ส่ง | ทะเบียนรถ | ประเภทรถ | คนขับ | สถานะ | action |
|---|---|---|---|---|---|---|---|
| CBM-2568-0000001 | Q10001 | สมชาย ใจดี | 80-1234 | 10 ล้อ | สมชาย ใจดี | จัดส่ง | ปุ่ม **เช็คอิน** + eye |
| CBM-2568-0000002 | Q10002 | สมหญิง แสงดี | 81-2345 | 6 ล้อ | สมหญิง แสงดี | จัดส่ง | ปุ่ม **เช็คอิน** + eye |
| CBM-2568-0000003 | Q10003 | สมศักดิ์ มั่นคง | 82-3456 | 16 ล้อ | มานพ ขับดี | จัดส่ง | ปุ่ม **เช็คอิน** + eye |

> pending ทุกแถว bookingStatus (in detail) = **อยู่ระหว่างจัดส่ง** · weighToken/checkInTime = ว่าง

**Seed tab เช็คอินแล้ว (checked-in · 5 รายการ · มี weighToken/checkInTime):**

| รหัสเอกสาร | โควต้า | เกษตรกร | เลขเหรียญชั่ง | ประเภทการเข้าโรงงาน | สถานะ | สถานะ Booking |
|---|---|---|---|---|---|---|
| NBM-2568-0000101 | โควต้ากลาง | Walk-in | 10501 | โควต้ากลาง | รอทำจ่าย | **-** |
| CBM-2568-0000004 | Q10004 | ประสิทธิ์ ทองมา | 10502 | โควต้าจองคิว | รอทำจ่าย | **รอผลการเท** |
| NBM-2568-0000102 | Q10006 | สายชล ทุ่งกว้าง | 10503 | โควต้าไม่ได้จองคิว | รอทำจ่าย | **-** |
| CBM-2568-0000005 | Q10005 | วิรัตน์ สีทอง | 10504 | โควต้าจองคิว | เสร็จสิ้น | **รอผลการเท** |
| CBM-2568-0000006 | Q10007 | ทดสอบ ซิงก์ล้มเหลว | 10505 | โควต้าจองคิว | รอทำจ่าย | **ซิงก์ล้มเหลว** (+ ปุ่ม retry) |

- **Stat cards (นับจากทั้งระบบ · ทั้ง 2 tab):** รอเช็คอิน = **3** · เช็คอินวันนี้ = **5** · ซิงก์ล้มเหลว = **1** · เสร็จสิ้น = **1**

**Member/Quota master (สำหรับ สมาชิก lookup — MEMBER_QUOTAS):**

| โควต้า | เกษตรกร | เบอร์โทร |
|---|---|---|
| Q12345 | บุญมา รักไร่ | 085-234-5678 |
| Q10006 | สายชล ทุ่งกว้าง | 086-345-6789 |
| Q22222 | ประยูร นางาม | 087-456-7890 |

> โควต้าอื่น (เช่น Q99999) = ไม่พบ → `ไม่พบโควต้านี้`

**VERBATIM microcopy (Expected anchors — copy เป๊ะจาก prototype):**
- top tabs: `ต้องส่ง` · `เช็คอินแล้ว` (แต่ละแท็บมี count badge)
- page header: title = ชื่อ tab (`ต้องส่ง`/`เช็คอินแล้ว`) + count `N รายการ` · sub `เช็คอินรับอ้อยหน้าโรงงาน · จุดชั่งน้ำหนัก (WKN)`
- ปุ่ม header: `Scan QR` · `Export CSV` · `เช็คอิน` (primary → method chooser)
- stat cards: `รอเช็คอิน` (meta "รถที่รอเข้าเช็คอิน") · `เช็คอินวันนี้` ("รถที่เช็คอินแล้ว") · `ซิงก์ล้มเหลว` ("รอซิงก์สถานะ Booking") · `เสร็จสิ้น` ("ปิดรายการแล้ว")
- list columns: `รหัสเอกสาร · วันที่/เวลาเข้า · โควต้า · เกษตรกร/ผู้ส่ง · ทะเบียนรถ · ประเภทรถ · ชื่อคนขับ · เลขเหรียญชั่ง · ประเภทการเข้าโรงงาน · สถานะ` (+ `สถานะ Booking` เฉพาะ tab เช็คอินแล้ว) + `การกระทำ`
- filter: search placeholder `ค้นหา CBM/NBM/ทะเบียน/เหรียญ/โควต้า/คนขับ` · สถานะ `ทุกสถานะ`/`จัดส่ง`/`รอทำจ่าย`/`เสร็จสิ้น` · แผนก `ทุกแผนก`/`โควต้าจองคิว`/`โควต้าไม่ได้จองคิว`/`โควต้ากลาง` · ปุ่ม `ล้าง`
- entry-type badge: `โควต้าจองคิว` (info) · `โควต้าไม่ได้จองคิว` (muted) · `โควต้ากลาง` (warning)
- status pill: `จัดส่ง` (muted) · `รอทำจ่าย` (warning) · `เสร็จสิ้น` (success)
- booking cell: `รอผลการเท` · `อยู่ระหว่างจัดส่ง` · `ซิงก์ล้มเหลว` (red + retry) · `-` (non-CBM)
- method chooser: title `เช็คอิน` · sub `เลือกวิธีการเช็คอิน` · `เช็คอินจาก CBM` (sub `ป้อนรหัส CBM หรือสแกน QR`) · `เช็คอินแบบไม่มีคิว — สมาชิก` (sub `ค้นหาโควต้าของสมาชิก`) · `เช็คอินแบบไม่มีคิว — โควต้ากลาง` (sub `ไม่มีโควต้า`)
- CBM modal: title `เช็คอินจาก CBM` · sub `ป้อนรหัส CBM แล้วค้นหา เพื่อดึงข้อมูลการจอง` · field `รหัส CBM` + ปุ่ม `ค้นหา` · card `พบรายการจอง` (เกษตรกร/โควต้า/ทะเบียนรถ/ประเภทรถ) · field `เลขเหรียญชั่ง` · `หมายเหตุ` · footer `ยกเลิก` / `ยืนยันเช็คอิน`
- member modal: title `เช็คอินแบบไม่มีคิว — สมาชิก` · sub `ค้นหาโควต้าของสมาชิก แล้วกรอกข้อมูลรถและการชำระเงิน` · field `ค้นหาโควต้า` · found `พบข้อมูลสมาชิก` · fields `เลขเหรียญชั่ง`/`ทะเบียนรถ`/`ชื่อคนขับ`/`เบอร์โทร`/`ประเภทรถ` · section `ประเภทการชำระเงิน` `งวดที่ 1`/`งวดที่ 2` radios `บิลเขียว`/`บิลขาว`
- central modal: title `เช็คอินแบบไม่มีคิว — โควต้ากลาง` · sub `ไม่มีโควต้า · กรอกข้อมูลรถและการชำระเงิน`
- vehicle types: `อีแต๋น` · `6 ล้อ` · `10 ล้อ` · `16 ล้อ`
- QR modal: title `สแกน QR — CBM` · sub `สแกน QR Code หรือป้อนรหัส CBM` · helper `เล็งกล้องไปที่ QR Code บนใบจอง` · field `หรือป้อนรหัส CBM` placeholder `CBM-.............` + ปุ่ม `ไป` · footer `ปิด`
- void modal: title `ยกเลิกเช็คอิน (Void)` · sub `ต้องการยกเลิกเช็คอินรายการนี้หรือไม่? · [รหัสเอกสาร]` · field `เหตุผล (ไม่บังคับ)` · footer `ยกเลิก` / `ยืนยัน`
- detail drawer: eyebrow `เช็คอินรับอ้อย · [รหัสเอกสาร]` · section `ข้อมูลการเช็คอิน` · cells `เวลาเข้า`/`โควต้า`/`เกษตรกร/ผู้ส่ง`/`ทะเบียนรถ`/`ประเภทรถ`/`ชื่อคนขับ`/`เลขเหรียญชั่ง`/`ประเภทการเข้าโรงงาน`/`สถานะ` (+ `สถานะ Booking` เฉพาะ CBM) · footer `ปิด`
- toast success: `เช็คอินสำเร็จ` · `พบข้อมูลสมาชิก` · `ซิงก์สถานะ Booking สำเร็จ` · `ยกเลิกเช็คอินสำเร็จ` · info `กำลังดาวน์โหลดไฟล์ CSV`
- toast warning/error: `ไม่พบรหัส CBM นี้` · `ไม่พบโควต้านี้` · `กรุณาใส่เลขเหรียญชั่ง` · `กรุณากรอกข้อมูลให้ครบถ้วน` · `กรุณาเลือกประเภทการชำระเงินให้ครบถ้วน` · `ซิงก์ล้มเหลว กรุณาลองใหม่`
- footer/pagination: `แสดง X-Y จาก Z รายการ`
- empty: `ไม่พบรายการที่ค้นหา` (desc "ลองปรับคำค้นหรือล้างตัวกรอง" + ปุ่ม `ล้างตัวกรอง`) · no-data `ยังไม่มีรายการเช็คอิน` (desc pending "ยังไม่มีรถที่รอเข้าเช็คอิน" / checked "ยังไม่มีรถเข้าเช็คอินในวันนี้")
- simulate: server event CHECK_IN / booking 200 · sync 409 `รายการซ้ำ (idempotent)` · scale weighToken จริง · Quota/Member master จริง · NBM doc server · Booking reversal · CSV file · filter วันที่

## Coverage

| Group | เคส | ความสำคัญ |
|---|---|---|
| A — List ต้องส่ง / tabs / stats / pending row | TC-A01..A06 (6) | สูงสุด |
| B — List เช็คอินแล้ว + สถานะ Booking column / search / filter / CSV / empty ⭐ | TC-B01..B07 (7) | สูงสุด |
| C — Method chooser (3 วิธี) | TC-C01..C05 (5) | สูง |
| D — CBM check-in + sync ⭐ | TC-D01..D06 (6) | สูงสุด |
| E — Sync-fail retry ⭐ | TC-E01..E05 (5) | สูงสุด |
| F — Member check-in (ไม่มีคิว-สมาชิก) | TC-F01..F06 (6) | สูงสุด |
| G — Central check-in (ไม่มีคิว-โควต้ากลาง) | TC-G01..G04 (4) | สูง |
| H — QR scan | TC-H01..H03 (3) | สูง |
| I — Detail drawer + Void | TC-I01..I06 (6) | สูงสุด |
| J — Cross-module XT-01..05 + simulate | TC-J01..J06 (6) | สูงสุด |

---

## Coverage Ledger

### Stories/AC (06_TESTS §6.1)
| AC | รายละเอียด (ย่อ) | cases |
|---|---|---|
| AC-01 | 2 แท็บ (ต้องส่ง/เช็คอินแล้ว) + count "N รายการ" + 4 stats | TC-A01, TC-A02, TC-E03 |
| AC-02 | ค้นหา (CBM/NBM/ทะเบียน/เหรียญ/โควต้า/คนขับ) · filter สถานะ + แผนก (+ วันที่) | TC-A04, TC-A05, TC-B04, TC-B05, TC-J06 (วันที่ = simulate) |
| AC-03 | columns ครบ · entry-type badge · status badge · pending: ปุ่มเช็คอิน | TC-A01, TC-A03, TC-D06 |
| AC-04 | checked-in tab: คอลัมน์ "สถานะ Booking" (CBM only) · non-CBM = "-" | TC-B01, TC-B02, TC-B03 |
| AC-05 | Export CSV → "กำลังดาวน์โหลดไฟล์ CSV" · pagination · empty → "ไม่พบรายการที่ค้นหา" | TC-B06, TC-B07 |
| AC-06 | เช็คอิน → modal 3 วิธี | TC-C01, TC-C02, TC-C03, TC-C04, TC-C05, TC-D01, TC-F01 |
| AC-07 | รหัส CBM ไม่มีจริง → "ไม่พบรหัส CBM นี้" | TC-D02 |
| AC-08 | รหัส CBM มีจริง → farmer info แสดง | TC-D03, TC-D06 |
| AC-09 | weighToken ว่าง → "กรุณาใส่เลขเหรียญชั่ง" | TC-D04 |
| AC-10 | ยืนยันเช็คอิน → check-in + sync booking → "รอผลการเท" | TC-D05, TC-J01 |
| AC-11 | sync ล้ม → badge "ซิงก์ล้มเหลว" + ปุ่ม retry | TC-E01, TC-E03 |
| AC-12 | retry สำเร็จ → "ซิงก์สถานะ Booking สำเร็จ" · ล้ม → "ซิงก์ล้มเหลว กรุณาลองใหม่" | TC-E02, TC-E04 (ล้ม = simulate) |
| AC-13 | ค้นโควต้าไม่พบ → "ไม่พบโควต้านี้" | TC-F02 |
| AC-14 | ค้นพบ → "พบข้อมูลสมาชิก" + auto-fill | TC-F03, TC-J03 |
| AC-15 | ข้อมูลไม่ครบ → "กรุณากรอกข้อมูลให้ครบถ้วน" | TC-F04 |
| AC-16 | payment bill (งวด1/2) ไม่ครบ → "กรุณาเลือกประเภทการชำระเงินให้ครบถ้วน" | TC-F05 |
| AC-17 | เช็คอินสำเร็จ → "เช็คอินสำเร็จ" (NBM doc) | TC-F06 |
| AC-18 | เช็คอินโควต้ากลาง (ข้อมูลรถ + payment bill) → "เช็คอินสำเร็จ" | TC-G01, TC-G02, TC-G03, TC-G04 |
| AC-19 | entryType กลาง → badge "โควต้ากลาง" · phaseA "-" | TC-G04 |
| AC-20 | Scan QR → modal "สแกน QR — CBM" · ป้อนรหัส → ไป → CBM flow | TC-H01, TC-H02, TC-H03 |
| AC-21 | คลิกรหัสเอกสาร → detail drawer (fields ครบ) | TC-A06, TC-I01, TC-I02, TC-I03, TC-I04 |
| AC-22 | void → "ยกเลิกเช็คอิน (Void)" · เหตุผล(ไม่บังคับ) → "ยกเลิกเช็คอินสำเร็จ" | TC-I05, TC-I06 |

### Cross-Module / Event (06_TESTS §6.9) ⭐
| XT | Scenario | Source | cases |
|---|---|---|---|
| XT-01 | CBM check-in → event CHECK_IN → booking "รอผลการเท" (idempotent) | → Cane Booking (F-AGM-007) | TC-D05, TC-J01 (event จริง = simulate) |
| XT-02 | pending list = CBM dispatching (read) รอเข้าโรงงาน | CBM dispatching (read) | TC-A03, TC-J02 (read จริง = simulate) |
| XT-03 | member check-in → ค้นโควต้า + auto-fill | Quota/Member (read) | TC-F03, TC-J03 (master จริง = simulate) |
| XT-04 | sync retry ซ้ำ (same checkin_id) → 409/no-op | external Booking | TC-E05, TC-J04 (ต้อง simulate) |
| XT-05 | void → Booking reversal event | → Booking reversal | TC-I05, TC-J05 (reversal จริง = simulate) |

### Business Rules (05_RULES §5.1)
| BR | cases |
|---|---|
| BR-CI-01 3 วิธีเช็คอิน (CBM/สมาชิก/กลาง) | TC-C01, TC-D05, TC-F06, TC-G04 |
| BR-CI-02 weighToken บังคับทุกวิธี | TC-D04, TC-F04, TC-G02 |
| BR-CI-03 CBM → event CHECK_IN → booking รอผลการเท (idempotent) | TC-D05, TC-J01, TC-J04 |
| BR-CI-04 Sync fail → syncPending + badge + retry (idempotent) | TC-E01, TC-E02, TC-E04 |
| BR-CI-05 entry type → doc (จองคิว=CBM · ไม่จองคิว/กลาง=NBM) | TC-F06, TC-G04 |
| BR-CI-06 Member/Central payment bill งวด1+2 บังคับ | TC-F05, TC-G03 |
| BR-CI-07 Void + เหตุผล (ไม่บังคับ) | TC-I05, TC-I06 |
| BR-CI-08 2-tab: ต้องส่ง → เช็คอินแล้ว | TC-A02, TC-D05 |
| BR-CI-09 สถานะ Booking column (checked-in · CBM only · non-CBM "-") | TC-B02, TC-B03 |
| BR-CI-10 QR scan / manual CBM entry | TC-H02, TC-D06 |

### Validation (05_RULES §5.4)
| VR | Message | cases |
|---|---|---|
| VR-01 | "กรุณาใส่เลขเหรียญชั่ง" (weighToken CBM) | TC-D04 |
| VR-02 | "ไม่พบรหัส CBM นี้" (CBM code valid) | TC-D02 |
| VR-03 | "ไม่พบโควต้านี้" (quota member) | TC-F02 |
| VR-04 | "กรุณากรอกข้อมูลให้ครบถ้วน" (Member/Central) | TC-F04, TC-G02 |
| VR-05 | "กรุณาเลือกประเภทการชำระเงินให้ครบถ้วน" (bill งวด1+2) | TC-F05, TC-G03 |

### Edge Cases (05_RULES §5.5)
| EC | Case | cases |
|---|---|---|
| EC-01 | CBM check-in สำเร็จ → sync รอผลการเท | TC-D03, TC-D05 |
| EC-02 | CBM code ไม่มี → VR-02 | TC-D02 |
| EC-03 | weighToken ว่าง → VR-01 | TC-D04 |
| EC-04 | sync ล้ม → syncPending + badge ซิงก์ล้มเหลว + retry | TC-E01 |
| EC-05 | retry สำเร็จ → "ซิงก์สถานะ Booking สำเร็จ" (idempotent no dup) | TC-E02 |
| EC-06 | retry ล้มอีก → "ซิงก์ล้มเหลว กรุณาลองใหม่" | TC-E04 (ต้อง simulate) |
| EC-07 | member quota ไม่พบ → VR-03 | TC-F02 |
| EC-08 | member พบ → "พบข้อมูลสมาชิก" + auto-fill | TC-F03 |
| EC-09 | ข้อมูลไม่ครบ → VR-04 | TC-F04, TC-G02 |
| EC-10 | payment bill ไม่ครบ → VR-05 | TC-F05, TC-G03 |
| EC-11 | central check-in สำเร็จ → "เช็คอินสำเร็จ" (NBM · no sync) | TC-G04 |
| EC-12 | void → "ยกเลิกเช็คอินสำเร็จ" | TC-I05 |
| EC-13 | QR scan/manual → เปิด CBM check-in flow | TC-H01, TC-H02 |
| EC-14 | checked-in non-CBM สถานะ Booking → "-" | TC-B03, TC-I03 |
| EC-15 | sync dup (same checkin_id) → 409/no-op | TC-E05, TC-J04 (ต้อง simulate) |

### Error Catalog (05_RULES §5.6 — UI-observable)
| error | cases |
|---|---|
| VALIDATION_FAILED (token/bill/basic) | TC-D04, TC-F04, TC-F05, TC-G02, TC-G03 |
| NOT_FOUND "ไม่พบรหัส CBM นี้" | TC-D02 |
| NOT_FOUND "ไม่พบโควต้านี้" | TC-F02 |
| SYNC_FAILED(retryable) "ซิงก์ล้มเหลว กรุณาลองใหม่" | TC-E04 (simulate) |
| CONFLICT(409 dup) "รายการซ้ำ (idempotent)" | TC-E05, TC-J04 (simulate) |

### State Machine (05_RULES §5.2)
| entity | ข้อยืนยัน (ย่อ) | cases |
|---|---|---|
| CheckIn | ต้องส่ง(จัดส่ง) → เช็คอินแล้ว(รอทำจ่าย) → เสร็จสิ้น · void: เช็คอินแล้ว → ยกเลิก | TC-D05, TC-A02, TC-I05 |
| Booking sync | (no sync) → syncing → success(รอผลการเท) / fail(syncPending+retry) | TC-D05, TC-E01, TC-E02 |

### Permission (05_RULES §5.3)
| cell | cases |
|---|---|
| เจ้าหน้าที่ชั่ง (เช็คอิน+retry+void) — prototype user | TC-D05, TC-E02, TC-I05 |
| หัวหน้ากะ (void) · Cane Booking (รับ event) — RBAC จริง | TC-J01, TC-J05 (ต้อง simulate) |

**Manifest cross-check (FRD §0.12):** AC 22/22 (AC-01..22) · XT-01..05 5/5 · BR-CI-01..10 10/10 · VR-01..05 5/5 · EC-01..15 15/15 → ทุกแถว manifest มีคู่ใน Ledger ✅

---

## Data Sets

### ชุด A — CBM check-in ถูกต้อง (happy)
| ฟิลด์ (ป้ายบนจอ) | ค่า |
|---|---|
| รหัส CBM | CBM-2568-0000001 |
| เลขเหรียญชั่ง | 20001 |
| หมายเหตุ | เช็คอินจาก test case |

### ชุด B — CBM negative
| กรณี | รหัส CBM | เลขเหรียญชั่ง | คาดหวัง (ข้อความจริง) |
|---|---|---|---|
| B1 (ไม่พบ) | CBM-2568-9999999 | — | ไม่พบรหัส CBM นี้ |
| B2 (token ว่าง) | CBM-2568-0000002 (พบ) | *(เว้นว่าง)* | กรุณาใส่เลขเหรียญชั่ง |

### ชุด C — Member check-in
| กรณี | โควต้า | ข้อมูลรถ | bill งวด1/2 | คาดหวัง |
|---|---|---|---|---|
| C1 (happy) | Q12345 (พบ) | token 30001 · ทะเบียน 1กก-1234 · คนขับ auto | บิลเขียว / บิลขาว | เช็คอินสำเร็จ |
| C2 (quota ไม่พบ) | Q99999 | — | — | ไม่พบโควต้านี้ |
| C3 (ไม่ครบ) | Q12345 (พบ) | token ว่าง | — | กรุณากรอกข้อมูลให้ครบถ้วน |
| C4 (bill ไม่ครบ) | Q12345 (พบ) | token/ทะเบียน/คนขับ ครบ | *(ไม่เลือกงวด2)* | กรุณาเลือกประเภทการชำระเงินให้ครบถ้วน |

### ชุด D — Central check-in (โควต้ากลาง)
| กรณี | ข้อมูลรถ | bill งวด1/2 | คาดหวัง |
|---|---|---|---|
| D1 (happy) | token 40001 · ทะเบียน 2ขข-2345 · คนขับ ชูใจ พาส่ง | บิลขาว / บิลเขียว | เช็คอินสำเร็จ |
| D2 (ไม่ครบ) | token ว่าง | — | กรุณากรอกข้อมูลให้ครบถ้วน |
| D3 (bill ไม่ครบ) | รถครบ | *(ไม่เลือกงวด1)* | กรุณาเลือกประเภทการชำระเงินให้ครบถ้วน |

---

## Test Cases

## Group A — List ต้องส่ง / tabs / stats / pending row (US-01)

### TC-A01 — เปิดหน้า tab ต้องส่ง + 4 stats + คอลัมน์ (happy — AC-01/03)
- group: A · ความสำคัญ: สูงสุด · trace: AC-01, AC-03 / UI loaded
- Setup: seed=default (refresh) · files=—
- Start: OPEN `#/checkins`
- ผ่านเมื่อ: top tabs + stat cards + คอลัมน์แสดงตรง seed

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/checkins` | — | top tabs **ต้องส่ง** (active · count **3**) · **เช็คอินแล้ว** (count **5**) · หัวข้อ **ต้องส่ง** + count **3 รายการ** · sub **เช็คอินรับอ้อยหน้าโรงงาน · จุดชั่งน้ำหนัก (WKN)** | ☐ |
| 2 | VERIFY แถบ stats 4 การ์ด | — | **รอเช็คอิน 3** · **เช็คอินวันนี้ 5** · **ซิงก์ล้มเหลว 1** · **เสร็จสิ้น 1** | ☐ |
| 3 | VERIFY หัวคอลัมน์ตาราง (tab ต้องส่ง) | — | เรียง: **รหัสเอกสาร · วันที่/เวลาเข้า · โควต้า · เกษตรกร/ผู้ส่ง · ทะเบียนรถ · ประเภทรถ · ชื่อคนขับ · เลขเหรียญชั่ง · ประเภทการเข้าโรงงาน · สถานะ · การกระทำ** (ไม่มีคอลัมน์ สถานะ Booking) | ☐ |
| 4 | VERIFY แถว CBM-2568-0000001 | — | โควต้า **Q10001** · เกษตรกร **สมชาย ใจดี** · ทะเบียน **80-1234** · ประเภทรถ **10 ล้อ** · เลขเหรียญชั่ง **-** · badge **โควต้าจองคิว** · สถานะ **จัดส่ง** | ☐ |
| 5 | VERIFY ปุ่ม header + footer | — | ปุ่ม **Scan QR** · **Export CSV** · **เช็คอิน** (primary) · footer **แสดง 1-3 จาก 3 รายการ** | ☐ |

### TC-A02 — สลับแท็บ ต้องส่ง ↔ เช็คอินแล้ว + count (AC-01 / BR-CI-08)
- group: A · ความสำคัญ: สูง · trace: AC-01 / BR-CI-08 / tab route
- Setup: seed=default · files=—
- Start: OPEN `#/checkins`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK top tab **เช็คอินแล้ว** | — | URL = **#/checkins/checked-in** · หัวข้อเปลี่ยนเป็น **เช็คอินแล้ว** + count **5 รายการ** · ตารางมีคอลัมน์ **สถานะ Booking** เพิ่ม | ☐ |
| 2 | CLICK top tab **ต้องส่ง** | — | URL = **#/checkins** · หัวข้อ **ต้องส่ง** + count **3 รายการ** · คอลัมน์ สถานะ Booking หาย | ☐ |
| 3 | VERIFY count badge บนแท็บ | — | แท็บ **ต้องส่ง** badge **3** · แท็บ **เช็คอินแล้ว** badge **5** (คงที่ทั้ง 2 tab) | ☐ |

### TC-A03 — pending rows: badge + status + ปุ่มเช็คอิน (AC-03 / XT-02)
- group: A · ความสำคัญ: สูงสุด · trace: AC-03 / XT-02 (dispatching read)
- Setup: seed=default · files=—
- Start: OPEN `#/checkins`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ทุกแถว pending | — | 3 แถว (CBM-...0001/0002/0003) · badge **โควต้าจองคิว** ทุกแถว · สถานะ **จัดส่ง** ทุกแถว · เลขเหรียญชั่ง **-** | ☐ |
| 2 | VERIFY row-actions แต่ละแถว pending | — | มีปุ่ม **เช็คอิน** (primary sm) + ปุ่ม eye (รายละเอียด) · ไม่มีปุ่มยกเลิก | ☐ |
| 3 | VERIFY แถว CBM-2568-0000003 (ต่างคนขับ) | — | เกษตรกร **สมศักดิ์ มั่นคง** · คนขับ **มานพ ขับดี** · ประเภทรถ **16 ล้อ** | ☐ |

### TC-A04 — ค้นหา (CBM/ทะเบียน/โควต้า/คนขับ) tab ต้องส่ง (AC-02)
- group: A · ความสำคัญ: สูง · trace: AC-02 / search (within tab)
- Setup: seed=default · files=—
- Start: OPEN `#/checkins`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "0000002" → ช่องค้นหา (placeholder **ค้นหา CBM/NBM/ทะเบียน/เหรียญ/โควต้า/คนขับ**) | — | เหลือ 1 แถว **CBM-2568-0000002** (สมหญิง แสงดี) | ☐ |
| 2 | CLICK **ล้าง** → TYPE "มานพ" (คนขับ) | — | เหลือ 1 แถว CBM-2568-0000003 (คนขับ มานพ ขับดี) | ☐ |
| 3 | CLICK **ล้าง** → TYPE "Q10001" (โควต้า) | — | เหลือ 1 แถว CBM-2568-0000001 | ☐ |
| 4 | CLICK **ล้าง** | — | กลับ 3 รายการ | ☐ |

### TC-A05 — filter สถานะ + แผนก tab ต้องส่ง (AC-02)
- group: A · ความสำคัญ: สูง · trace: AC-02 / filter (วันที่ = simulate)
- Setup: seed=default · files=—
- Start: OPEN `#/checkins`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT dropdown สถานะ = **จัดส่ง** | — | ยัง 3 แถว (pending ทุกแถว = จัดส่ง) | ☐ |
| 2 | SELECT สถานะ = **เสร็จสิ้น** | — | ตารางว่าง + empty **ไม่พบรายการที่ค้นหา** (pending ไม่มีเสร็จสิ้น) + ปุ่ม **ล้างตัวกรอง** | ☐ |
| 3 | CLICK **ล้างตัวกรอง** → SELECT แผนก = **โควต้ากลาง** | — | ตารางว่าง + **ไม่พบรายการที่ค้นหา** (pending = โควต้าจองคิว ล้วน) | ☐ |
| 4 | CLICK **ล้างตัวกรอง** | — | กลับ 3 รายการ | ☐ |

### TC-A06 — เปิด detail จากแถว pending + refresh-safe route (AC-21)
- group: A · ความสำคัญ: กลาง · trace: AC-21 / route `#/checkins/:id`
- Setup: seed=default · files=—
- Start: OPEN `#/checkins`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK รหัสเอกสาร **CBM-2568-0000001** (หรือปุ่ม eye) | — | drawer เปิด · URL = **#/checkins/ci-1** · eyebrow **เช็คอินรับอ้อย · CBM-2568-0000001** | ☐ |
| 2 | F5 (refresh) ที่ URL #/checkins/ci-1 | — | drawer CBM-2568-0000001 เปิดใหม่อัตโนมัติ (refresh-safe) | ☐ |
| 3 | CLICK ปุ่ม **ปิด** (footer) | — | drawer ปิด · กลับ `#/checkins` (list ต้องส่ง 3 รายการ) | ☐ |

---

## Group B — List เช็คอินแล้ว + สถานะ Booking column (US-01) ⭐

### TC-B01 — เปิด tab เช็คอินแล้ว + คอลัมน์ สถานะ Booking (AC-04)
- group: B · ความสำคัญ: สูงสุด · trace: AC-04 / checked-in columns
- Setup: seed=default · files=—
- Start: OPEN `#/checkins/checked-in`
- ผ่านเมื่อ: คอลัมน์ สถานะ Booking โผล่ + 5 แถว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/checkins/checked-in` | — | หัวข้อ **เช็คอินแล้ว** + count **5 รายการ** · footer **แสดง 1-5 จาก 5 รายการ** | ☐ |
| 2 | VERIFY หัวคอลัมน์ | — | มีคอลัมน์ **สถานะ Booking** แทรกก่อน **การกระทำ** | ☐ |
| 3 | VERIFY row-actions (checked-in) | — | แต่ละแถวมีปุ่ม eye (รายละเอียด) + ปุ่ม x-circle (ยกเลิก) · ไม่มีปุ่ม เช็คอิน | ☐ |
| 4 | VERIFY แถว NBM-2568-0000101 | — | โควต้า **โควต้ากลาง** (badge warning) · เกษตรกร **Walk-in** · เลขเหรียญชั่ง **10501** · badge **โควต้ากลาง** · สถานะ **รอทำจ่าย** | ☐ |

### TC-B02 — สถานะ Booking column: CBM (โควต้าจองคิว) โชว์ badge (AC-04 / BR-CI-09) ⭐
- group: B · ความสำคัญ: สูงสุด · trace: AC-04 / BR-CI-09 (CBM booking status)
- Setup: seed=default · files=—
- Start: OPEN `#/checkins/checked-in`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แถว CBM-2568-0000004 (synced) | — | คอลัมน์ สถานะ Booking = pill **รอผลการเท** · สถานะ **รอทำจ่าย** | ☐ |
| 2 | VERIFY แถว CBM-2568-0000005 (done) | — | สถานะ Booking = **รอผลการเท** · สถานะ **เสร็จสิ้น** (pill success) | ☐ |
| 3 | VERIFY แถว CBM-2568-0000006 (sync fail) | — | สถานะ Booking = badge แดง **ซิงก์ล้มเหลว** + ปุ่ม retry (refresh icon) | ☐ |

### TC-B03 — สถานะ Booking column: non-CBM = "-" (AC-04 / EC-14)
- group: B · ความสำคัญ: สูง · trace: AC-04 / EC-14 (non-CBM dash)
- Setup: seed=default · files=—
- Start: OPEN `#/checkins/checked-in`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แถว NBM-2568-0000101 (โควต้ากลาง) | — | คอลัมน์ สถานะ Booking = **-** (ไม่มี badge) | ☐ |
| 2 | VERIFY แถว NBM-2568-0000102 (โควต้าไม่ได้จองคิว) | — | คอลัมน์ สถานะ Booking = **-** | ☐ |

### TC-B04 — ค้นหา (NBM/เหรียญ/เกษตรกร) tab เช็คอินแล้ว (AC-02)
- group: B · ความสำคัญ: สูง · trace: AC-02 / search checked-in
- Setup: seed=default · files=—
- Start: OPEN `#/checkins/checked-in`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE "10505" (เลขเหรียญชั่ง) | — | เหลือ 1 แถว CBM-2568-0000006 (ทดสอบ ซิงก์ล้มเหลว) | ☐ |
| 2 | CLICK **ล้าง** → TYPE "วิรัตน์" (เกษตรกร) | — | เหลือ 1 แถว CBM-2568-0000005 | ☐ |
| 3 | CLICK **ล้าง** → TYPE "NBM" | — | เหลือ 2 แถว (NBM-...0101 + NBM-...0102) | ☐ |

### TC-B05 — filter สถานะ + แผนก tab เช็คอินแล้ว (AC-02)
- group: B · ความสำคัญ: สูง · trace: AC-02 / filter checked-in
- Setup: seed=default · files=—
- Start: OPEN `#/checkins/checked-in`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT แผนก = **โควต้าจองคิว** | — | เหลือ 3 แถว (CBM-...0004/0005/0006) · ทุกแถวมี badge สถานะ Booking | ☐ |
| 2 | CLICK **ล้าง** → SELECT สถานะ = **เสร็จสิ้น** | — | เหลือ 1 แถว CBM-2568-0000005 (เสร็จสิ้น) | ☐ |
| 3 | CLICK **ล้าง** → SELECT แผนก = **โควต้ากลาง** | — | เหลือ 1 แถว NBM-2568-0000101 (Walk-in) | ☐ |

### TC-B06 — Export CSV → toast (AC-05) (ไฟล์จริง ต้อง simulate)
- group: B · ความสำคัญ: กลาง · trace: AC-05 · **prototype: toast จำลอง · ไฟล์จริง = SIT**
- Setup: seed=default · files=—
- Start: OPEN `#/checkins/checked-in`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **Export CSV** → WAIT | — | toast **กำลังดาวน์โหลดไฟล์ CSV** | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): ไฟล์ CSV จริง | — | ไฟล์ CSV ดาวน์โหลด · คอลัมน์ไทยตรงตาราง · encoding ถูก | ☐ (ต้อง simulate) |

### TC-B07 — pagination footer + empty state (AC-05)
- group: B · ความสำคัญ: กลาง · trace: AC-05 / pagination + empty (filter vs no-data)
- Setup: seed=default · files=—
- Start: OPEN `#/checkins/checked-in`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY pagination footer | — | **แสดง 1-5 จาก 5 รายการ** (pageSize 25 · หน้าเดียว) | ☐ |
| 2 | TYPE "ไม่มีรายการนี้แน่นอน" → ค้นหา | — | ตารางว่าง + empty **ไม่พบรายการที่ค้นหา** (desc "ลองปรับคำค้นหรือล้างตัวกรอง") + ปุ่ม **ล้างตัวกรอง** | ☐ |
| 3 | CLICK **ล้างตัวกรอง** | — | กลับ 5 รายการ | ☐ |
| 4 | VERIFY (no-data variant · ต้อง simulate): tab ที่ไม่มี record | — | empty **ยังไม่มีรายการเช็คอิน** (desc "ยังไม่มีรถเข้าเช็คอินในวันนี้") — prototype seed มี 5 เสมอ | ☐ (ต้อง simulate) |

---

## Group C — Method chooser (3 วิธี) (US-02..04)

### TC-C01 — เช็คอิน → method chooser 3 วิธี (AC-06 / BR-CI-01)
- group: C · ความสำคัญ: สูง · trace: AC-06 / BR-CI-01
- Setup: seed=default · files=—
- Start: OPEN `#/checkins`
- ผ่านเมื่อ: modal 3 option ครบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **เช็คอิน** (header primary) | — | modal เปิด · title **เช็คอิน** · sub **เลือกวิธีการเช็คอิน** | ☐ |
| 2 | VERIFY 3 ตัวเลือก | — | **เช็คอินจาก CBM** (sub "ป้อนรหัส CBM หรือสแกน QR") · **เช็คอินแบบไม่มีคิว — สมาชิก** (sub "ค้นหาโควต้าของสมาชิก") · **เช็คอินแบบไม่มีคิว — โควต้ากลาง** (sub "ไม่มีโควต้า") | ☐ |

### TC-C02 — method → เช็คอินจาก CBM (AC-06)
- group: C · ความสำคัญ: สูง · trace: AC-06 / route to CBM modal
- Setup: seed=default · files=—
- Start: OPEN `#/checkins` → CLICK **เช็คอิน**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เช็คอินจาก CBM** | — | modal เปลี่ยนเป็น title **เช็คอินจาก CBM** · field **รหัส CBM** + ปุ่ม **ค้นหา** | ☐ |

### TC-C03 — method → เช็คอินแบบไม่มีคิว — สมาชิก (AC-06)
- group: C · ความสำคัญ: สูง · trace: AC-06 / route to member modal
- Setup: seed=default · files=—
- Start: OPEN `#/checkins` → CLICK **เช็คอิน**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เช็คอินแบบไม่มีคิว — สมาชิก** | — | modal title **เช็คอินแบบไม่มีคิว — สมาชิก** · field **ค้นหาโควต้า** | ☐ |

### TC-C04 — method → เช็คอินแบบไม่มีคิว — โควต้ากลาง (AC-06)
- group: C · ความสำคัญ: สูง · trace: AC-06 / route to central modal
- Setup: seed=default · files=—
- Start: OPEN `#/checkins` → CLICK **เช็คอิน**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **เช็คอินแบบไม่มีคิว — โควต้ากลาง** | — | modal title **เช็คอินแบบไม่มีคิว — โควต้ากลาง** · sub **ไม่มีโควต้า · กรอกข้อมูลรถและการชำระเงิน** · ไม่มีช่องค้นหาโควต้า | ☐ |

### TC-C05 — ปิด method chooser (Esc / ปุ่ม x) (AC-06)
- group: C · ความสำคัญ: กลาง · trace: AC-06 / dismiss
- Setup: seed=default · files=—
- Start: OPEN `#/checkins` → CLICK **เช็คอิน**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | กด **Esc** | — | modal ปิด · กลับหน้า list ต้องส่ง (3 รายการ) | ☐ |
| 2 | CLICK **เช็คอิน** อีกครั้ง → CLICK ปุ่ม x (มุมขวาบน modal) | — | modal ปิด | ☐ |

---

## Group D — CBM check-in + sync (US-02) ⭐

### TC-D01 — เปิด CBM modal จาก method chooser (AC-06)
- group: D · ความสำคัญ: สูง · trace: AC-06 / open CBM
- Setup: seed=default · files=—
- Start: OPEN `#/checkins` → CLICK **เช็คอิน** → CLICK **เช็คอินจาก CBM**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY modal CBM | — | title **เช็คอินจาก CBM** · sub **ป้อนรหัส CBM แล้วค้นหา เพื่อดึงข้อมูลการจอง** · field **รหัส CBM** (placeholder CBM-2568-0000001) + ปุ่ม **ค้นหา** · field **เลขเหรียญชั่ง** · **หมายเหตุ** · footer **ยกเลิก** / **ยืนยันเช็คอิน** | ☐ |

### TC-D02 — รหัส CBM ไม่มีจริง → block (negative — AC-07 / VR-02 / EC-02)
- group: D · ความสำคัญ: สูง · trace: AC-07 / VR-02 / EC-02
- Setup: seed=default · files=—
- Start: OPEN `#/checkins` → CLICK **เช็คอิน** → **เช็คอินจาก CBM**
- ชุดข้อมูล: B1

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE รหัส **CBM-2568-9999999** → CLICK **ค้นหา** → WAIT | B1 | toast **ไม่พบรหัส CBM นี้** · ไม่มี card "พบรายการจอง" | ☐ |

### TC-D03 — รหัส CBM มีจริง → farmer info card (happy — AC-08 / EC-01)
- group: D · ความสำคัญ: สูงสุด · trace: AC-08 / EC-01 (found card)
- Setup: seed=default · files=—
- Start: OPEN `#/checkins` → CLICK **เช็คอิน** → **เช็คอินจาก CBM**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE รหัส **CBM-2568-0000001** → CLICK **ค้นหา** → WAIT | — | card **พบรายการจอง** แสดง: เกษตรกร **สมชาย ใจดี** · โควต้า **Q10001** · ทะเบียนรถ **80-1234** · ประเภทรถ **10 ล้อ** | ☐ |

### TC-D04 — เลขเหรียญชั่งว่าง → block (negative — AC-09 / VR-01 / EC-03 / BR-CI-02)
- group: D · ความสำคัญ: สูงสุด · trace: AC-09 / VR-01 / EC-03 / BR-CI-02
- Setup: seed=default · files=—
- Start: OPEN `#/checkins` → CLICK **เช็คอิน** → **เช็คอินจาก CBM**
- ชุดข้อมูล: B2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE รหัส **CBM-2568-0000002** → CLICK **ค้นหา** (พบ card) | B2 | card พบรายการจอง (สมหญิง แสงดี) | ☐ |
| 2 | เว้น **เลขเหรียญชั่ง** ว่าง → CLICK **ยืนยันเช็คอิน** → WAIT | B2 | toast **กรุณาใส่เลขเหรียญชั่ง** · ไม่เช็คอิน (ยังอยู่ modal) | ☐ |

### TC-D05 — ยืนยันเช็คอิน CBM สำเร็จ + sync → รอผลการเท (happy — AC-10 / XT-01 / EC-01 / BR-CI-03) ★
- group: D · ความสำคัญ: สูงสุด · trace: AC-10 / XT-01 / EC-01 / BR-CI-03/08 · sync to booking
- Setup: seed=default · files=—
- Start: OPEN `#/checkins` → CLICK **เช็คอิน** → **เช็คอินจาก CBM**
- ชุดข้อมูล: A
- ผ่านเมื่อ: ค้น CBM → ใส่ token → ยืนยัน → ย้าย tab + booking รอผลการเท

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE รหัส **CBM-2568-0000001** → CLICK **ค้นหา** | A | card **พบรายการจอง** (สมชาย ใจดี) | ☐ |
| 2 | TYPE เลขเหรียญชั่ง **20001** → (option) หมายเหตุ "เช็คอินจาก test case" → CLICK **ยืนยันเช็คอิน** → WAIT | A | modal ปิด + toast **เช็คอินสำเร็จ** (desc **ส่งสถานะ Booking ไป "รอผลการเท" แล้ว**) · หน้าเด้งไป tab **เช็คอินแล้ว** | ☐ |
| 3 | VERIFY แถวใหม่ CBM-2568-0000001 (tab เช็คอินแล้ว) | — | เลขเหรียญชั่ง **20001** · สถานะ **รอทำจ่าย** · คอลัมน์ สถานะ Booking = **รอผลการเท** | ☐ |
| 4 | VERIFY counts | — | แท็บ **ต้องส่ง** count = **2** · แท็บ **เช็คอินแล้ว** count = **6** · stat **รอเช็คอิน 2** · **เช็คอินวันนี้ 6** | ☐ |

### TC-D06 — CBM check-in จากปุ่ม เช็คอิน บนแถว pending (prefilled — AC-03/08 / BR-CI-10)
- group: D · ความสำคัญ: สูง · trace: AC-03, AC-08 / BR-CI-10 · direct row check-in
- Setup: seed=default · files=—
- Start: OPEN `#/checkins`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **เช็คอิน** (บนแถว CBM-2568-0000003) | — | modal **เช็คอินจาก CBM** เปิด · รหัส CBM **CBM-2568-0000003** เติมไว้แล้ว · card **พบรายการจอง** (สมศักดิ์ มั่นคง · Q10003) แสดงทันที (auto-lookup) | ☐ |
| 2 | TYPE เลขเหรียญชั่ง **20003** → CLICK **ยืนยันเช็คอิน** → WAIT | — | toast **เช็คอินสำเร็จ** · ย้าย tab เช็คอินแล้ว · booking **รอผลการเท** | ☐ |

---

## Group E — Sync-fail retry (US-02) ⭐

### TC-E01 — seed sync-fail badge + retry button (AC-11 / EC-04 / BR-CI-04)
- group: E · ความสำคัญ: สูงสุด · trace: AC-11 / EC-04 / BR-CI-04
- Setup: seed=default (CBM-2568-0000006 · syncPending=true) · files=—
- Start: OPEN `#/checkins/checked-in`
- ผ่านเมื่อ: badge แดง + retry ปรากฏ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แถว CBM-2568-0000006 | — | คอลัมน์ สถานะ Booking = badge แดง **ซิงก์ล้มเหลว** + ปุ่ม retry (refresh icon) ข้าง ๆ | ☐ |
| 2 | OPEN detail CBM-2568-0000006 (คลิกรหัสเอกสาร) → VERIFY | — | drawer cell **สถานะ Booking** = **ซิงก์ล้มเหลว** + note **ซิงก์สถานะ Booking ล้มเหลว: Network timeout** | ☐ |

### TC-E02 — retry sync สำเร็จ (ครั้งแรก deterministic) → รอผลการเท (AC-12 / EC-05 / BR-CI-04) ★
- group: E · ความสำคัญ: สูงสุด · trace: AC-12 / EC-05 / BR-CI-04 (idempotent no dup)
- Setup: seed=default (CBM-2568-0000006 · retryCount=0) · files=—
- Start: OPEN `#/checkins/checked-in`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม retry (refresh) บนแถว CBM-2568-0000006 → WAIT ~1s | — | (ระหว่างรอ icon หมุน spin) จากนั้น toast **ซิงก์สถานะ Booking สำเร็จ** | ☐ |
| 2 | VERIFY แถว CBM-2568-0000006 หลัง retry | — | คอลัมน์ สถานะ Booking เปลี่ยนเป็น pill **รอผลการเท** (ไม่มี badge แดง/ปุ่ม retry แล้ว) | ☐ |

### TC-E03 — stat ซิงก์ล้มเหลว สะท้อนหลัง retry (AC-01 / AC-11)
- group: E · ความสำคัญ: สูง · trace: AC-01, AC-11 / stat count
- Setup: seed=default · files=—
- Start: OPEN `#/checkins/checked-in`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY stat ก่อน retry | — | **ซิงก์ล้มเหลว 1** (meta "รอซิงก์สถานะ Booking" · สีเตือน) | ☐ |
| 2 | CLICK retry บน CBM-2568-0000006 → WAIT (สำเร็จ) → VERIFY stat | — | **ซิงก์ล้มเหลว 0** (meta กลับเป็นสีปกติ) | ☐ |

### TC-E04 — retry ล้มซ้ำ → "ซิงก์ล้มเหลว กรุณาลองใหม่" (AC-12 / EC-06) (ต้อง simulate)
- group: E · ความสำคัญ: สูง · trace: AC-12 / EC-06 · **prototype: retry ครั้งแรกสำเร็จเสมอ · ครั้งถัดสุ่ม — backoff จริง = SIT**
- Setup: **simulate — ระบบจริง:** sync ล้มเนื่องจาก network/booking API error
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): retry แล้ว booking API ยังตอบ error | — | toast **ซิงก์ล้มเหลว กรุณาลองใหม่** · badge ยัง **ซิงก์ล้มเหลว** · syncPending คงอยู่ · auto-retry/backoff ทำงาน | ☐ (ต้อง simulate) |

### TC-E05 — sync dup (same checkin_id) → 409/no-op (XT-04 / EC-15) (ต้อง simulate)
- group: E · ความสำคัญ: สูง · trace: XT-04 / EC-15 · **prototype single-session · ไม่มี server — SIT**
- Setup: **simulate — ระบบจริง:** POST sync ซ้ำ checkin_id เดิม
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): retry/sync ซ้ำด้วย checkin_id เดิม | — | 409 **รายการซ้ำ (idempotent)** / no-op · booking ไม่เกิดผลซ้ำ (idempotent) | ☐ (ต้อง simulate) |

---

## Group F — Member check-in (ไม่มีคิว — สมาชิก) (US-03)

### TC-F01 — เปิด member modal + fields ครบ (AC-06)
- group: F · ความสำคัญ: สูง · trace: AC-06 / member form
- Setup: seed=default · files=—
- Start: OPEN `#/checkins` → CLICK **เช็คอิน** → **เช็คอินแบบไม่มีคิว — สมาชิก**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY modal member | — | title **เช็คอินแบบไม่มีคิว — สมาชิก** · field **ค้นหาโควต้า** + ปุ่ม **ค้นหา** · fields **เลขเหรียญชั่ง**/**ทะเบียนรถ**/**ชื่อคนขับ**/**เบอร์โทร**/**ประเภทรถ** | ☐ |
| 2 | VERIFY section payment | — | section **ประเภทการชำระเงิน** · **งวดที่ 1** radios (บิลเขียว/บิลขาว) · **งวดที่ 2** radios (บิลเขียว/บิลขาว) | ☐ |
| 3 | VERIFY dropdown ประเภทรถ | — | ตัวเลือก **อีแต๋น** / **6 ล้อ** / **10 ล้อ** / **16 ล้อ** | ☐ |

### TC-F02 — ค้นโควต้าไม่พบ → block (negative — AC-13 / VR-03 / EC-07)
- group: F · ความสำคัญ: สูง · trace: AC-13 / VR-03 / EC-07
- Setup: seed=default · files=—
- Start: OPEN `#/checkins` → CLICK **เช็คอิน** → **เช็คอินแบบไม่มีคิว — สมาชิก**
- ชุดข้อมูล: C2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE โควต้า **Q99999** → CLICK **ค้นหา** → WAIT | C2 | toast **ไม่พบโควต้านี้** · ไม่มี card "พบข้อมูลสมาชิก" | ☐ |

### TC-F03 — ค้นพบ → "พบข้อมูลสมาชิก" + auto-fill (happy — AC-14 / EC-08 / XT-03) ★
- group: F · ความสำคัญ: สูงสุด · trace: AC-14 / EC-08 / XT-03 (Member master read)
- Setup: seed=default · files=—
- Start: OPEN `#/checkins` → CLICK **เช็คอิน** → **เช็คอินแบบไม่มีคิว — สมาชิก**
- ชุดข้อมูล: C1

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE โควต้า **Q12345** → CLICK **ค้นหา** → WAIT | C1 | card **พบข้อมูลสมาชิก · บุญมา รักไร่ · 085-234-5678** | ☐ |
| 2 | VERIFY auto-fill | — | ช่อง **ชื่อคนขับ** = **บุญมา รักไร่** · **เบอร์โทร** = **085-234-5678** (เติมอัตโนมัติ) | ☐ |

### TC-F04 — ข้อมูลไม่ครบ → block (negative — AC-15 / VR-04 / EC-09 / BR-CI-02)
- group: F · ความสำคัญ: สูง · trace: AC-15 / VR-04 / EC-09
- Setup: seed=default · files=—
- Start: OPEN `#/checkins` → CLICK **เช็คอิน** → **เช็คอินแบบไม่มีคิว — สมาชิก**
- ชุดข้อมูล: C3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE โควต้า **Q12345** → CLICK **ค้นหา** (พบ) → เว้น **เลขเหรียญชั่ง** ว่าง → CLICK **ยืนยันเช็คอิน** → WAIT | C3 | toast **กรุณากรอกข้อมูลให้ครบถ้วน** · ไม่สร้างเช็คอิน | ☐ |

### TC-F05 — payment bill ไม่ครบ → block (negative — AC-16 / VR-05 / EC-10 / BR-CI-06)
- group: F · ความสำคัญ: สูงสุด · trace: AC-16 / VR-05 / EC-10 / BR-CI-06
- Setup: seed=default · files=—
- Start: OPEN `#/checkins` → CLICK **เช็คอิน** → **เช็คอินแบบไม่มีคิว — สมาชิก**
- ชุดข้อมูล: C4

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ค้น Q12345 (พบ) → กรอก เลขเหรียญชั่ง **30001** · ทะเบียน **1กก-1234** · คนขับ (auto) → เลือก **งวดที่ 1 = บิลเขียว** · เว้น **งวดที่ 2** → CLICK **ยืนยันเช็คอิน** → WAIT | C4 | toast **กรุณาเลือกประเภทการชำระเงินให้ครบถ้วน** · ไม่สร้างเช็คอิน | ☐ |

### TC-F06 — เช็คอินสมาชิกสำเร็จ → NBM doc (happy — AC-17 / BR-CI-01/05) ★
- group: F · ความสำคัญ: สูงสุด · trace: AC-17 / BR-CI-01/05 (NBM gen)
- Setup: seed=default · files=—
- Start: OPEN `#/checkins` → CLICK **เช็คอิน** → **เช็คอินแบบไม่มีคิว — สมาชิก**
- ชุดข้อมูล: C1

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | ค้น **Q12345** (พบ) → เลขเหรียญชั่ง **30001** · ทะเบียน **1กก-1234** · คนขับ (auto บุญมา รักไร่) · เลือก **งวดที่ 1 = บิลเขียว** · **งวดที่ 2 = บิลขาว** → CLICK **ยืนยันเช็คอิน** → WAIT | C1 | modal ปิด + toast **เช็คอินสำเร็จ** · เด้งไป tab **เช็คอินแล้ว** | ☐ |
| 2 | VERIFY แถวใหม่ (บนสุด tab เช็คอินแล้ว) | — | รหัสเอกสาร **NBM-2568-0000103** · เกษตรกร **บุญมา รักไร่** · badge **โควต้าไม่ได้จองคิว** · คอลัมน์ สถานะ Booking = **-** (non-CBM ไม่ sync) · count เช็คอินแล้ว = **6** | ☐ |

---

## Group G — Central check-in (ไม่มีคิว — โควต้ากลาง) (US-04)

### TC-G01 — เปิด central modal (ไม่มีช่องค้นหาโควต้า) (AC-18)
- group: G · ความสำคัญ: สูง · trace: AC-18 / central form
- Setup: seed=default · files=—
- Start: OPEN `#/checkins` → CLICK **เช็คอิน** → **เช็คอินแบบไม่มีคิว — โควต้ากลาง**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY modal central | — | title **เช็คอินแบบไม่มีคิว — โควต้ากลาง** · sub **ไม่มีโควต้า · กรอกข้อมูลรถและการชำระเงิน** · **ไม่มีช่องค้นหาโควต้า** · fields **เลขเหรียญชั่ง**/**ทะเบียนรถ**/**ชื่อคนขับ**/**เบอร์โทร**/**ประเภทรถ** + งวดที่ 1/2 | ☐ |

### TC-G02 — ข้อมูลไม่ครบ → block (negative — AC-18 / VR-04 / BR-CI-02)
- group: G · ความสำคัญ: สูง · trace: AC-18 / VR-04
- Setup: seed=default · files=—
- Start: OPEN `#/checkins` → CLICK **เช็คอิน** → **เช็คอินแบบไม่มีคิว — โควต้ากลาง**
- ชุดข้อมูล: D2

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เว้น **เลขเหรียญชั่ง** ว่าง → CLICK **ยืนยันเช็คอิน** → WAIT | D2 | toast **กรุณากรอกข้อมูลให้ครบถ้วน** | ☐ |

### TC-G03 — payment bill ไม่ครบ → block (negative — AC-18 / VR-05 / BR-CI-06)
- group: G · ความสำคัญ: สูง · trace: AC-18 / VR-05 / BR-CI-06
- Setup: seed=default · files=—
- Start: OPEN `#/checkins` → CLICK **เช็คอิน** → **เช็คอินแบบไม่มีคิว — โควต้ากลาง**
- ชุดข้อมูล: D3

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | กรอก token **40001** · ทะเบียน **2ขข-2345** · คนขับ **ชูใจ พาส่ง** → เลือก **งวดที่ 2 = บิลเขียว** · เว้น **งวดที่ 1** → CLICK **ยืนยันเช็คอิน** → WAIT | D3 | toast **กรุณาเลือกประเภทการชำระเงินให้ครบถ้วน** | ☐ |

### TC-G04 — เช็คอินโควต้ากลางสำเร็จ + badge (happy — AC-18/19 / EC-11 / BR-CI-05) ★
- group: G · ความสำคัญ: สูงสุด · trace: AC-18, AC-19 / EC-11 / BR-CI-05 (NBM · no sync)
- Setup: seed=default · files=—
- Start: OPEN `#/checkins` → CLICK **เช็คอิน** → **เช็คอินแบบไม่มีคิว — โควต้ากลาง**
- ชุดข้อมูล: D1

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | กรอก token **40001** · ทะเบียน **2ขข-2345** · คนขับ **ชูใจ พาส่ง** · ประเภทรถ **อีแต๋น** · **งวดที่ 1 = บิลขาว** · **งวดที่ 2 = บิลเขียว** → CLICK **ยืนยันเช็คอิน** → WAIT | D1 | modal ปิด + toast **เช็คอินสำเร็จ** · เด้งไป tab **เช็คอินแล้ว** | ☐ |
| 2 | VERIFY แถวใหม่ | — | รหัสเอกสาร **NBM-2568-0000103** · โควต้า **โควต้ากลาง** · badge **โควต้ากลาง** · คอลัมน์ สถานะ Booking = **-** (no sync) · สถานะ **รอทำจ่าย** | ☐ |

---

## Group H — QR scan (US-05)

### TC-H01 — เปิด QR modal (AC-20 / EC-13 / BR-CI-10)
- group: H · ความสำคัญ: สูง · trace: AC-20 / EC-13 / BR-CI-10
- Setup: seed=default · files=—
- Start: OPEN `#/checkins`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม **Scan QR** (header) | — | modal · title **สแกน QR — CBM** · sub **สแกน QR Code หรือป้อนรหัส CBM** · helper **เล็งกล้องไปที่ QR Code บนใบจอง** · field **หรือป้อนรหัส CBM** (placeholder CBM-.............) + ปุ่ม **ไป** · footer **ปิด** | ☐ |

### TC-H02 — ป้อนรหัส → ไป → เปิด CBM flow (AC-20 / EC-13)
- group: H · ความสำคัญ: สูง · trace: AC-20 / EC-13 · QR → CBM
- Setup: seed=default · files=—
- Start: OPEN `#/checkins` → CLICK **Scan QR**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE รหัส **CBM-2568-0000002** ในช่อง "หรือป้อนรหัส CBM" → CLICK **ไป** → WAIT | — | modal เปลี่ยนเป็น **เช็คอินจาก CBM** · รหัส CBM = **CBM-2568-0000002** เติมไว้ · card **พบรายการจอง** (สมหญิง แสงดี) แสดง | ☐ |

### TC-H03 — QR รหัสว่าง → ไป → CBM flow ว่าง (AC-20)
- group: H · ความสำคัญ: กลาง · trace: AC-20 / QR empty → CBM
- Setup: seed=default · files=—
- Start: OPEN `#/checkins` → CLICK **Scan QR**

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เว้นช่องว่าง → CLICK **ไป** | — | เปิด modal **เช็คอินจาก CBM** (ช่องรหัส CBM ว่าง · ยังไม่มี card) — พร้อมให้ค้นเอง | ☐ |

---

## Group I — Detail drawer + Void (US-07/08)

### TC-I01 — detail รายการ pending (CBM · ยังไม่เช็คอิน) (AC-21)
- group: I · ความสำคัญ: สูง · trace: AC-21 / detail pending
- Setup: seed=default · files=—
- Start: OPEN `#/checkins`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK รหัสเอกสาร **CBM-2568-0000002** | — | drawer · eyebrow **เช็คอินรับอ้อย · CBM-2568-0000002** · title **สมหญิง แสงดี** + pill **จัดส่ง** · sub มี **ยังไม่เช็คอิน** | ☐ |
| 2 | VERIFY grid **ข้อมูลการเช็คอิน** | — | เวลาเข้า **-** · โควต้า **Q10002** · ทะเบียนรถ **81-2345** · ประเภทรถ **6 ล้อ** · เลขเหรียญชั่ง **-** · ประเภทการเข้าโรงงาน **โควต้าจองคิว** · สถานะ Booking (CBM) = **อยู่ระหว่างจัดส่ง** | ☐ |
| 3 | VERIFY ปุ่ม footer (pending) | — | ปุ่ม **เช็คอิน** (primary · ไม่ใช่ยกเลิก) + ปุ่ม **ปิด** | ☐ |

### TC-I02 — detail รายการ checked-in (CBM · สถานะ Booking) (AC-21)
- group: I · ความสำคัญ: สูง · trace: AC-21 / detail checked-in
- Setup: seed=default · files=—
- Start: OPEN `#/checkins/checked-in`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK รหัสเอกสาร **CBM-2568-0000004** | — | drawer · title **ประสิทธิ์ ทองมา** + pill **รอทำจ่าย** · sub มี **เข้าเมื่อ 08:40 21/07/26** | ☐ |
| 2 | VERIFY grid | — | เวลาเข้า **08:40 21/07/26** · เลขเหรียญชั่ง **10502** · ประเภทการเข้าโรงงาน **โควต้าจองคิว** · cell **สถานะ Booking** = pill **รอผลการเท** | ☐ |
| 3 | VERIFY ปุ่ม footer (checked-in) | — | ปุ่ม **ยกเลิก** (danger) + ปุ่ม **ปิด** (ไม่มีปุ่มเช็คอิน) | ☐ |

### TC-I03 — detail รายการ non-CBM (ไม่มี cell สถานะ Booking) (AC-21 / EC-14)
- group: I · ความสำคัญ: กลาง · trace: AC-21 / EC-14 (non-CBM detail)
- Setup: seed=default · files=—
- Start: OPEN `#/checkins/checked-in`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK รหัสเอกสาร **NBM-2568-0000101** (โควต้ากลาง) | — | drawer title **Walk-in** · grid **ไม่มี cell "สถานะ Booking"** (non-CBM ซ่อน) · ประเภทการเข้าโรงงาน **โควต้ากลาง** | ☐ |

### TC-I04 — detail refresh-safe (checked-in) (AC-21)
- group: I · ความสำคัญ: กลาง · trace: AC-21 / route refresh-safe
- Setup: seed=default · files=—
- Start: OPEN `#/checkins/checked-in`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK รหัสเอกสาร **CBM-2568-0000005** → VERIFY URL | — | URL = **#/checkins/ci-7** · drawer เปิด | ☐ |
| 2 | F5 (refresh) | — | drawer CBM-2568-0000005 เปิดใหม่อัตโนมัติ (refresh-safe) | ☐ |
| 3 | CLICK **ปิด** | — | drawer ปิด · กลับ tab เช็คอินแล้ว (5 รายการ) | ☐ |

### TC-I05 — void เช็คอิน → success (happy — AC-22 / EC-12 / BR-CI-07) ★
- group: I · ความสำคัญ: สูงสุด · trace: AC-22 / EC-12 / BR-CI-07
- Setup: seed=default · files=—
- Start: OPEN `#/checkins/checked-in`
- ผ่านเมื่อ: void → toast + record ถูกลบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่ม x-circle (ยกเลิก) บนแถว **NBM-2568-0000102** | — | modal · title **ยกเลิกเช็คอิน (Void)** · sub **ต้องการยกเลิกเช็คอินรายการนี้หรือไม่? · NBM-2568-0000102** · field **เหตุผล (ไม่บังคับ)** · footer **ยกเลิก** / **ยืนยัน** | ☐ |
| 2 | (option) TYPE เหตุผล "รถผิดคิว" → CLICK **ยืนยัน** → WAIT | — | modal ปิด + toast **ยกเลิกเช็คอินสำเร็จ** | ☐ |
| 3 | VERIFY list | — | แถว NBM-2568-0000102 หายไป · count เช็คอินแล้ว = **4** · stat **เช็คอินวันนี้ 4** | ☐ |

### TC-I06 — void ยกเลิก (ปิด modal ไม่ยืนยัน) (AC-22)
- group: I · ความสำคัญ: กลาง · trace: AC-22 / void cancel
- Setup: seed=default · files=—
- Start: OPEN `#/checkins/checked-in`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK x-circle (ยกเลิก) บนแถว **NBM-2568-0000101** → ใน modal CLICK **ยกเลิก** (ghost) | — | modal ปิด · แถว NBM-2568-0000101 ยังอยู่ · count เช็คอินแล้ว = **5** (ไม่ลด) | ☐ |

---

## Group J — Cross-module / event XT-01..05 + simulate (06_TESTS §6.9) ⭐

### TC-J01 — XT-01: CBM check-in → event CHECK_IN → booking รอผลการเท (idempotent) (ต้อง simulate)
- group: J · ความสำคัญ: สูงสุด · trace: XT-01 / BR-CI-03 · **prototype: local sync only · event จริง = SIT**
- Setup: seed=default (บน prototype) + **simulate — ระบบจริง:** Cane Booking รับ event
- Start: OPEN `#/checkins` → เช็คอิน CBM-2568-0000001 (TC-D05)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (prototype) ยืนยันเช็คอิน CBM-2568-0000001 → VERIFY booking | — | toast desc **ส่งสถานะ Booking ไป "รอผลการเท" แล้ว** · แถวโชว์ **รอผลการเท** | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): event CHECK_IN → Cane Booking (F-AGM-007) | — | booking ปลายทางเปลี่ยนเป็น **รอผลการเท** · ยิง event ซ้ำ checkin_id เดิม = idempotent (ไม่เปลี่ยนซ้ำ) | ☐ (ต้อง simulate) |

### TC-J02 — XT-02: pending list = CBM dispatching (read) (ต้อง simulate)
- group: J · ความสำคัญ: สูง · trace: XT-02 · **prototype: seed fixed · CBM dispatching จริง = SIT**
- Setup: **simulate — ระบบจริง:** อ่าน CBM ที่ dispatching รอเข้าโรงงาน
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): tab ต้องส่ง อ่านรายการรถ dispatching จาก Cane Booking | — | รถที่ booking = dispatching/รอเข้าโรงงาน โผล่ใน tab ต้องส่ง (read-only sync) | ☐ (ต้อง simulate) |

### TC-J03 — XT-03: member check-in → Quota/Member master (read) (ต้อง simulate)
- group: J · ความสำคัญ: สูง · trace: XT-03 · **prototype: MEMBER_QUOTAS mock · master จริง = SIT**
- Setup: **simulate — ระบบจริง:** ค้นโควต้าจาก Member/Quota master
- Start: — (SIT) (prototype = TC-F03)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): ค้นโควต้าสมาชิก อ่านจาก master จริง | — | auto-fill ชื่อ/เบอร์ ตรงต้นทาง Member master (prototype = 3 โควต้า mock) · GET only | ☐ (ต้อง simulate) |

### TC-J04 — XT-04: sync retry ซ้ำ (same checkin_id) → 409/no-op (ต้อง simulate)
- group: J · ความสำคัญ: สูง · trace: XT-04 / EC-15 · **prototype single-session — SIT**
- Setup: **simulate — ระบบจริง:** POST sync/retry ซ้ำ idempotency-key เดิม
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): retry ซ้ำ checkin_id เดิม | — | 409 **รายการซ้ำ (idempotent)** / no-op · ไม่เกิดผลซ้ำที่ booking | ☐ (ต้อง simulate) |

### TC-J05 — XT-05: void → Booking reversal event (ต้อง simulate)
- group: J · ความสำคัญ: สูง · trace: XT-05 / BR-CI-07 · **prototype: void ลบ record local · reversal จริง = SIT**
- Setup: seed=default (prototype = TC-I05) + **simulate — ระบบจริง:** void ยิง reversal event
- Start: OPEN `#/checkins/checked-in`

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | (prototype) void CBM-2568-0000004 → VERIFY | — | toast **ยกเลิกเช็คอินสำเร็จ** · record หาย | ☐ |
| 2 | VERIFY (ระบบจริง — SIT): void ยิง reversal ไป Cane Booking | — | booking ปลายทาง reverse (ยกเลิกสถานะ รอผลการเท) · reversal event append | ☐ (ต้อง simulate) |

### TC-J06 — filter วันที่ + scale weighToken + NBM doc server (ต้อง simulate)
- group: J · ความสำคัญ: กลาง · trace: AC-02 (วันที่) / AC-17 (NBM server) / BR-CI-02 · **prototype: ไม่มี date filter · token กรอกมือ · NBM gen client — SIT**
- Setup: **simulate — ระบบจริง**
- Start: — (SIT)

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY (ระบบจริง): filter วันที่ | — | กรองรายการตามช่วงวันที่เข้าโรงงาน (prototype ไม่มี date filter) | ☐ (ต้อง simulate) |
| 2 | VERIFY (ระบบจริง): weighToken จาก scale hardware | — | เลขเหรียญชั่งดึงจากเครื่องชั่งจริง (prototype = กรอกมือ) | ☐ (ต้อง simulate) |
| 3 | VERIFY (ระบบจริง): NBM doc gen ฝั่ง server | — | เลขเอกสาร NBM ออกจาก server (unique · sequence กันชน) · ไม่ชนกันหลาย session (prototype = client nextNbmId) | ☐ (ต้อง simulate) |

---

## วิธีที่ agent รัน (Run protocol)

1. เปิด `cane-checkin-management.html` ใน browser (desktop ≥1280px) — รอ ~2s ให้ font/icon โหลด
2. **ทุกเคสเริ่มด้วย refresh (F5)** แล้ว OPEN route ตาม `Start:` — mock in-memory, refresh = reset seed 3 pending + 5 checked-in (ทำให้เคส independent)
3. ทำตาม step ตามลำดับ — Action ขึ้นต้น verb (OPEN/CLICK/TYPE/SELECT/VERIFY/WAIT)
4. `WAIT` = รอ ≤3s จน Expected ปรากฏ (toast มุมขวาล่าง · retry sync ~0.7s · toast แสดง ~3.2-3.6s)
5. **CBM sync:** เช็คอิน CBM booked → status `รอทำจ่าย` + สถานะ Booking `รอผลการเท` + toast desc `ส่งสถานะ Booking ไป "รอผลการเท" แล้ว` · row ย้ายจาก ต้องส่ง → เช็คอินแล้ว
6. **weighToken บังคับ:** CBM ว่าง → `กรุณาใส่เลขเหรียญชั่ง` · Member/Central ข้อมูลรถไม่ครบ → `กรุณากรอกข้อมูลให้ครบถ้วน`
7. **payment bill:** Member/Central ต้องเลือก งวดที่ 1 + งวดที่ 2 → ไม่ครบ = `กรุณาเลือกประเภทการชำระเงินให้ครบถ้วน`
8. **สถานะ Booking column:** โผล่เฉพาะ tab เช็คอินแล้ว · CBM (โควต้าจองคิว) โชว์ badge · sync ล้ม = `ซิงก์ล้มเหลว` + retry · non-CBM = `-`
9. **retry sync:** ครั้งแรกสำเร็จเสมอ → `ซิงก์สถานะ Booking สำเร็จ` + badge → `รอผลการเท` · ล้มซ้ำ + 409 idempotent = `(ต้อง simulate)`
10. **void:** ลบ record ออกจาก list จริง (count ลด) · reversal event จริง = `(ต้อง simulate)`
11. step ไหน Expected ไม่ตรง = FAIL เคสนั้น → บันทึก `failed_step` + `evidence` แล้วไปเคสถัดไป
12. เคส `(ต้อง simulate)` — ถ้ารันบน prototype ทำไม่ได้ ให้ status = `blocked` + note "SIT case"

## Coverage Audit

| หมวด | covered / total |
|---|---|
| Stories/AC (06_TESTS §6.1) | 22 / 22 (AC-01..22 · AC-12 ล้ม = simulate) |
| Cross-Module / Event (XT-01..05) | 5 / 5 (XT-01/02/03/04/05 event/read จริง = simulate) |
| Business rules (BR-CI-01..10) | 10 / 10 |
| Validation (VR-01..05) | 5 / 5 |
| Edge cases (EC-01..15) | 15 / 15 (EC-06/15 = simulate) |
| Error catalog (UI-observable) | ครบ · NOT_FOUND/VALIDATION บน prototype · 409/SYNC_FAILED retry = simulate |
| Permission cells | เจ้าหน้าที่ชั่ง allow ครบ · Booking-receiver/หัวหน้ากะ = simulate |
| 3 วิธีเช็คอิน + CBM sync + booking column | ครบทุกชั้น (CBM/สมาชิก/กลาง + sync/retry + void) |

- **Manifest cross-check (FRD §0.12): ✅ 22 AC + 5 XT + 10 BR + 5 VR + 15 EC — ทุกแถวมีคู่ใน Ledger**

### เคส (ต้อง simulate) / SIT
- TC-B06 step 2 (ไฟล์ CSV จริง — server-side)
- TC-B07 step 4 (no-data variant — seed มี record เสมอ)
- TC-E04 (retry ล้มซ้ำ "ซิงก์ล้มเหลว กรุณาลองใหม่" — prototype retry แรกสำเร็จเสมอ)
- TC-E05 / TC-J04 (sync dup 409/no-op idempotent)
- TC-J01 (event CHECK_IN → Cane Booking จริง)
- TC-J02 (pending = CBM dispatching read จริง)
- TC-J03 (Quota/Member master lookup จริง)
- TC-J05 step 2 (Booking reversal event ตอน void)
- TC-J06 (filter วันที่ · scale weighToken · NBM doc server gen)

## Result Report (schema)

```json
{
  "feature_id": "F-AGM-010",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-A01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 54, "pass": 0, "fail": 0, "blocked": 0 }
}
```
