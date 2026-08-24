# AI Test Cases — F-WH-DN Delivery Note

เอกสารนี้ให้ AI browser/vision ทดสอบ prototype และ production binding โดยใช้ route/ข้อความที่เห็นจริงจาก HTML. เคสที่ต้องตรวจ service/database ระบุ `(ต้อง simulate)` ชัดเจน.

## Meta

| Item | Value |
|---|---|
| Feature ID | F-WH-DN |
| ชื่อ | Delivery Note — ใบส่งของ |
| Version | 1.0 · 2026-08-20 |
| App entry | `f-wh-delivery-note.html#/list` |
| Routes | `#/list`, `#/create/:packIds`, `#/view/:dnId` |
| ที่มา | BRD, FRD_Pack 00–07, approved HTML, Step-5 E2E |
| จำนวน | 50 cases / 7 groups |

## Coverage

| Group | Cases | Priority |
|---|---:|---|
| List / Reference create | TC-Q01..Q08 | สูง |
| Assignment / transport | TC-A01..A09 | สูง |
| Lifecycle / POD | TC-L01..L15 | สูง |
| Stock Transfer | TC-T01..T04 | สูง |
| Manual DN | TC-M01..M07 | สูง |
| Permission / UX / print | TC-U01..U04 | กลาง |
| Engineering / cross-module | TC-X01..X03 | สูง |

## Coverage Ledger

### FR / Acceptance (06_TESTS)

| Items | Cases |
|---|---|
| AT-01..04 | TC-Q01..Q08 |
| AT-05..10 | TC-A01..A09 |
| AT-11..27 | TC-L01..L15, TC-X01 |
| AT-28..30 | TC-T01..T04 |
| AT-31..35 | TC-M01..M07 |
| AT-36..40 | TC-U01..U04, TC-X02 |

### Business Rules (05_RULES)

| Rules | Cases |
|---|---|
| BR-DN-01..03 | TC-Q01,Q03,Q05,Q07 |
| BR-DN-04..06 | TC-A01..A09, TC-L01,L03 |
| BR-DN-07..12 | TC-L04..L10 |
| BR-DN-13..17 | TC-L11..L15, TC-U01,U03 |
| BR-DN-18..20 | TC-M01..M07, TC-A02,A04,A06,A08 |
| BR-DN-21..22 | TC-X01,X03 |

### Edge Cases

| EC | Cases / status |
|---|---|
| EC-01 | TC-Q04,Q06 |
| EC-02 | TC-U02 |
| EC-03 | TC-L06 |
| EC-04 | TC-L11 |
| EC-05 | TC-L12,L13 |
| EC-06 | TC-T01..T04 |
| EC-07 | TC-M04 |
| EC-08 | TC-A04,A06,A08 |
| EC-09 | TC-U03 |
| EC-10 `[AI-DEFAULT]` | TC-X02 `(ต้อง simulate)` |
| EC-11 `[AI-DEFAULT]` | TC-X01 `(ต้อง simulate)` |
| EC-12 `[AI-DEFAULT]` | TC-X03 `(ต้อง simulate)` |
| EC-13 `[AI-DEFAULT]` | TC-X03 `(ต้อง simulate)` |
| EC-14 `[AI-DEFAULT]` | TC-X01 `(ต้อง simulate)` |

### Error Codes

| Errors | Cases |
|---|---|
| ERR_VALIDATION_FAILED | TC-A04,A06,A08,TC-M02 |
| ERR_FORBIDDEN / ERR_NOT_ASSIGNED | TC-U04 |
| ERR_DN_NOT_FOUND | TC-U02 |
| ERR_STALE_DATA / ERR_IDEMPOTENCY_CONFLICT | TC-X01,X02 |
| BR_DN_COMBINE_MISMATCH / PACK_UNAVAILABLE | TC-Q04,Q06 |
| BR_DN_EMPLOYEE_REQUIRED / TRANSPORT_REQUIRED | TC-A02,A04,A06,A08,TC-L03 |
| BR_DN_REASON_REQUIRED | TC-L06,L11,L12,L13,TC-M04 |
| BR_DN_POD_INVALID | TC-L08,L09 |
| BR_DN_TRANSITION_INVALID | TC-L02,L05,TC-X02 |
| BR_DN_MANUAL_AUTOMATION_FORBIDDEN | TC-M06,X01 |
| ERR_DOWNSTREAM_UNAVAILABLE | TC-X03 |

### Permission Matrix

| Cell | Cases |
|---|---|
| wh_lead create/manage/destructive = allow | TC-Q05,TC-L01,L11..L15,TC-M01,M03 |
| driver assigned dispatch/tracking/fail/POD = allow | TC-L02,L04,L06,L07 |
| driver unassigned / viewer mutation = deny | TC-U04 |
| viewer read/print = allow | TC-U03,U04 |

### Cross-Module (XT)

| XT | Downstream | Cases |
|---|---|---|
| XT-01 | Packing | TC-Q07,TC-L11..L13 |
| XT-02 | Inventory | TC-L02,L10..L13,TC-X01 |
| XT-03 | Sales | TC-L10,L14,L15 |
| XT-04 | Stock Transfer | TC-T01..T04 |
| XT-05 | AR | TC-L10,L14,L15 |
| XT-06 | Document Config/Store | TC-Q07,TC-U03,TC-X03 |
| XT-07 | Notification | TC-L01..L15,TC-X03 |

### Scope Lock

| LOCK | Verify case |
|---|---|
| LOCK-01,02 | artifact/process check outside browser; HTML source hash unchanged, output route used |
| LOCK-03 | TC-Q03,Q04,Q06 |
| LOCK-04 | TC-T01..T04 |
| LOCK-05..07 | TC-M01..M07 |
| LOCK-08,09 | TC-A01..A09 |
| LOCK-10,11 | TC-L02,L11..L13 |
| LOCK-12 | TC-L06 |

### Cross-cutting / Events / States

| Item | Cases |
|---|---|
| all reference states | TC-L01..L15 |
| all manual target states | TC-M03,M05 |
| refresh/Esc/read-only | TC-U01,U02,U04 |
| PII/tenant/idempotency/outbox | TC-U04,TC-X01..X03 |

## Data Sets

### DS-REF — Reference SO

| Field | Value |
|---|---|
| pack | ใช้ใบ PACK ที่พร้อมส่งและเป็น Sales Order จากแถวแรกของคิว |
| assignee | ค้น “วิภาวี” |
| vehicle search | `1123` |
| manual vehicle | `3ฒก-4455 กรุงเทพมหานคร` |
| driver search | “ประเสริฐ” หรือเบอร์ที่แสดง |
| manual driver | ชื่อ `กิตติ`, นามสกุล `ขนส่งดี`, โทร `08 1234 5678` |
| reason | `ทดสอบตามแผน UAT` |

### DS-TRANSFER

| Field | Value |
|---|---|
| pack/ref | `PACK-2026-0460 / TR-2026-0012` |
| route | `WH-01 → WH-02` |

### DS-MANUAL

| Field | Value |
|---|---|
| reference | `EXT-DLV-UAT-001` |
| recipient | `ร้านทดสอบ Manual` |
| address | `99 ถนนสุขุมวิท กรุงเทพมหานคร` |
| reason | `เปลี่ยนสถานะเพื่อทดสอบ Manual` |

## Test Cases

### Group Q — List / Reference create

### TC-Q01 — เปิดคิวและแท็บ (happy)
- group: List · priority: สูง · trace: AT-01/BR-DN-01 · actor: wh_lead
- Setup: role=wh_lead · seed=fresh prototype · files=—
- Start: OPEN `#/list`
- ผ่านเมื่อ: เห็นสองแท็บและคิว Packing

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/list` | — | เห็นหัวข้อใบส่งของและแท็บ **รอออกใบส่งของ** | ☐ |
| 2 | CLICK แท็บ **ใบส่งของ** | — | ตารางเปลี่ยนเป็นรายการ DN | ☐ |
| 3 | CLICK แท็บ **รอออกใบส่งของ** | — | กลับมาเห็นแถว PACK พร้อมปุ่ม **ออกใบส่งของ** | ☐ |

### TC-Q02 — ค้นหาและรีเซ็ตคิว
- group: List · priority: กลาง · trace: UI P-01 · actor: wh_lead
- Setup: role=wh_lead · seed=fresh · files=—
- Start: OPEN `#/list`
- ผ่านเมื่อ: filter เปลี่ยนผลและรีเซ็ตกลับ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE ช่องค้นหา | รหัส PACK ที่เห็นในตาราง | เหลือแถวที่มีรหัสนั้น | ☐ |
| 2 | CLICK **รีเซ็ต** | — | รายการคิวทั้งหมดกลับมา | ☐ |

### TC-Q03 — เลือก PACK compatible หลายใบ
- group: Create · priority: สูง · trace: BR-DN-02/LOCK-03 · actor: wh_lead
- Setup: role=wh_lead · seed=มี PACK key เดียวกัน ≥2 · files=—
- Start: OPEN `#/list`
- ผ่านเมื่อ: เลือกหลายใบและเปิด confirm ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox PACK ใบแรก | — | checkbox ติดและปุ่ม **ออกใบส่งของ** พร้อมใช้ | ☐ |
| 2 | CLICK checkbox PACK ที่ลูกค้า/ที่ส่ง/source เดียวกัน | — | checkbox ติดทั้งสอง | ☐ |
| 3 | CLICK **ออกใบส่งของ** | — | route เป็น `#/create/...`; modal สรุปสอง PACK | ☐ |

### TC-Q04 — ห้ามรวมคนละ key (negative)
- group: Create · priority: สูง · trace: EC-01/BR_DN_COMBINE_MISMATCH · actor: wh_lead
- Setup: role=wh_lead · seed=PACK ต่าง customer/ship-to/source · files=—
- Start: OPEN `#/list`
- ผ่านเมื่อ: checkbox ที่ขัดกันเลือกไม่ได้หรือมีคำเตือนตรงตัว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK checkbox PACK ใบแรก | — | ใบแรกถูกเลือก | ☐ |
| 2 | CLICK checkbox PACK ที่ key ต่าง | — | ไม่ถูกเลือก; เห็น **รวมได้เฉพาะประเภทต้นทาง ลูกค้า และที่ส่งเดียวกัน** | ☐ |

### TC-Q05 — เปิด confirm จากปุ่มรายแถว
- group: Create · priority: สูง · trace: AT-02/03 · actor: wh_lead
- Setup: role=wh_lead · seed=fresh · files=—
- Start: OPEN `#/list`
- ผ่านเมื่อ: modal เปิดและยังไม่สร้างเอกสาร

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ออกใบส่งของ** ที่แถว PACK | — | route `#/create/<pack>`; เห็น **ยืนยันออกใบส่งของ** | ☐ |
| 2 | PRESS Escape | — | modal ปิด; กลับ list; PACK ยังอยู่คิว | ☐ |

### TC-Q06 — PACK ถูกผูกแล้วใช้ซ้ำไม่ได้ (negative)
- group: Create · priority: สูง · trace: BR_DN_PACK_UNAVAILABLE · actor: wh_lead
- Setup: role=wh_lead · seed=PACK ถูกสร้าง DN แล้ว · files=—
- Start: OPEN `#/list`
- ผ่านเมื่อ: PACK นั้นไม่อยู่ในคิวและเปิด create ซ้ำไม่ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY ตารางคิว | PACK ที่ผูกแล้ว | ไม่พบ PACK ดังกล่าว | ☐ |
| 2 | OPEN `#/create/<pack-that-is-bound>` | — | เห็น **ไม่พบใบแพ็คที่พร้อมออกใบส่งของ** และไม่มี DN ซ้ำ | ☐ |

### TC-Q07 — ยืนยันสร้าง Reference draft
- group: Create · priority: สูง · trace: AT-04/BR-DN-03/XT-01/06 · actor: wh_lead
- Setup: role=wh_lead · seed=DS-REF; fresh page · files=—
- Start: OPEN `#/create/<eligible-pack>`
- ผ่านเมื่อ: draft ถูกสร้าง, PACK ออกจากคิว, ยังไม่ GI

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT ผู้รับผิดชอบ/ขนส่ง/รถ/คนขับ/วันนัด | DS-REF | ค่าที่เลือกแสดงใน modal | ☐ |
| 2 | CLICK **ยืนยันออกใบส่งของ** | — | modal ปิด; เปิด `#/view/<dn>`; สถานะ **ร่าง** | ☐ |
| 3 | CLICK แท็บ **ประวัติ** | — | เห็นสร้างใบส่งของ; ไม่เห็น Goods Issue | ☐ |

### TC-Q08 — ยกเลิก confirm ไม่สร้างอะไร
- group: Create · priority: สูง · trace: BR-DN-03 · actor: wh_lead
- Setup: role=wh_lead · seed=fresh · files=—
- Start: OPEN `#/create/<eligible-pack>`
- ผ่านเมื่อ: cancel กลับ listและ PACK ยังอยู่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่มยกเลิก/ปิดใน modal | — | modal ปิดและ route กลับ list | ☐ |
| 2 | VERIFY PACK เดิม | — | ยังอยู่คิว; ไม่มี DN ใหม่ในแท็บ **ใบส่งของ** | ☐ |

### Group A — Assignment / transport

### TC-A01 — ค้นผู้รับผิดชอบ Employee
- group: Assignment · priority: สูง · trace: AT-05/BR-DN-20 · actor: wh_lead
- Setup: role=wh_lead · seed=open create modal · files=—
- Start: OPEN `#/create/<eligible-pack>`
- ผ่านเมื่อ: ค้นและเลือกพนักงานได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ช่อง **ผู้รับผิดชอบ** | — | search dropdown เปิด | ☐ |
| 2 | TYPE | วิภาวี | เห็นพนักงานที่ตรงคำค้น | ☐ |
| 3 | CLICK ผลลัพธ์พนักงาน | — | ชื่อพนักงานแสดงเป็นค่าที่เลือก | ☐ |

### TC-A02 — ผู้รับผิดชอบไม่มี Manual (negative)
- group: Assignment · priority: สูง · trace: LOCK-08/BR_DN_EMPLOYEE_REQUIRED · actor: wh_lead
- Setup: role=wh_lead · seed=open create modal · files=—
- Start: OPEN `#/create/<eligible-pack>`
- ผ่านเมื่อ: ไม่มีตัวเลือกกรอกเอง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ช่อง **ผู้รับผิดชอบ** | — | dropdown เปิด | ☐ |
| 2 | TYPE ชื่อที่ไม่มีในบริษัท | คนภายนอกทดสอบ | ไม่เห็นตัวเลือกกรอกเอง/สร้างคนใหม่ | ☐ |

### TC-A03 — ค้นรถ
- group: Transport · priority: สูง · trace: AT-06 · actor: wh_lead
- Setup: role=wh_lead · seed=carrier รถบริษัท · files=—
- Start: OPEN `#/create/<eligible-pack>`
- ผ่านเมื่อ: ค้นทะเบียนและเลือกได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ช่องรถแล้ว TYPE | 1123 | เห็นทะเบียนที่มี 1123 | ☐ |
| 2 | CLICK ผลลัพธ์ | — | ทะเบียนแสดงในช่อง | ☐ |

### TC-A04 — รถ Manual บังคับทะเบียน (negative)
- group: Transport · priority: สูง · trace: AT-07/EC-08 · actor: wh_lead
- Setup: role=wh_lead · seed=carrier รถบริษัท · files=—
- Start: OPEN `#/create/<eligible-pack>`
- ผ่านเมื่อ: ว่างถูกบล็อก แล้วค่าถูกบันทึกเมื่อกรอกครบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT **กรอกเลขรถเอง** | — | ฟอร์มเลขทะเบียนปรากฏ | ☐ |
| 2 | CLICK บันทึกโดยเว้นว่าง | — | เห็น **กรุณาระบุเลขทะเบียน / เลขรถ** | ☐ |
| 3 | TYPE แล้วบันทึก | `3ฒก-4455 กรุงเทพมหานคร` | ค่าทะเบียนแสดงเป็น selected value | ☐ |

### TC-A05 — ค้นคนขนส่ง
- group: Transport · priority: สูง · trace: AT-08 · actor: wh_lead
- Setup: role=wh_lead · seed=carrier รถบริษัท · files=—
- Start: OPEN `#/create/<eligible-pack>`
- ผ่านเมื่อ: ค้นด้วยชื่อหรือเบอร์ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ช่องคนขนส่งแล้ว TYPE | ประเสริฐ | เห็นผลลัพธ์ชื่อ/เบอร์ | ☐ |
| 2 | CLICK ผลลัพธ์ | — | คนขนส่งแสดงเป็น selected value | ☐ |

### TC-A06 — คนขนส่ง Manual บังคับ 3 ช่อง
- group: Transport · priority: สูง · trace: AT-09/LOCK-09 · actor: wh_lead
- Setup: role=wh_lead · seed=carrier รถบริษัท · files=—
- Start: OPEN `#/create/<eligible-pack>`
- ผ่านเมื่อ: ว่างถูกบล็อก; ครบแล้วเลือกได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT **กรอกคนขนส่งเอง** | — | ช่องชื่อ นามสกุล เบอร์โทรปรากฏ | ☐ |
| 2 | CLICK บันทึกโดยเว้นว่าง | — | เห็น **กรอกชื่อ นามสกุล และเบอร์โทรให้ครบ** | ☐ |
| 3 | TYPE ทั้งสามช่องแล้วบันทึก | DS-REF manual driver | ชื่อเต็มและเบอร์แสดงในช่อง | ☐ |

### TC-A07 — เบอร์โทร Manual ผิดรูปแบบ
- group: Transport · priority: สูง · trace: ERR_VALIDATION_FAILED · actor: wh_lead
- Setup: role=wh_lead · seed=manual driver form · files=—
- Start: OPEN `#/create/<eligible-pack>`
- ผ่านเมื่อ: รูปแบบผิดถูกบล็อก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE ชื่อ/นามสกุล/โทร | กิตติ / ขนส่งดี / abc | ค่าแสดง | ☐ |
| 2 | CLICK บันทึก | — | เห็น **รูปแบบเบอร์โทรไม่ถูกต้อง**; dropdownไม่รับค่า | ☐ |

### TC-A08 — ข้อมูล assignment ขาด (negative)
- group: Assignment · priority: สูง · trace: BR-DN-04/TRANSPORT_REQUIRED · actor: wh_lead
- Setup: role=wh_lead · seed=Reference draft ไม่มี required · files=—
- Start: OPEN `#/view/<draft-dn>`
- ผ่านเมื่อ: ready ถูกบล็อกด้วย visible warning

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ยืนยันพร้อมส่ง** | — | เห็น **กรอกข้อมูลที่มี * ให้ครบก่อนยืนยันพร้อมส่ง**; ช่องขาดมี error | ☐ |
| 2 | VERIFY สถานะ | — | ยังเป็น **ร่าง** | ☐ |

### TC-A09 — รถเกินพิกัดเป็น warning
- group: Transport · priority: กลาง · trace: BR-DN-05 · actor: wh_lead
- Setup: role=wh_lead · seed=DN น้ำหนักมากกว่ารถที่เลือก · files=—
- Start: OPEN `#/create/<heavy-pack>`
- ผ่านเมื่อ: เตือนแต่ไม่ล็อกการสร้าง/ready

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT รถพิกัดต่ำกว่า total weight | — | เห็นข้อความเตือนน้ำหนัก/พิกัด | ☐ |
| 2 | VERIFY ปุ่มยืนยัน | — | ปุ่มยังใช้งานได้เมื่อ required อื่นครบ | ☐ |

### Group L — Lifecycle / POD

### TC-L01 — Draft → Ready
- group: Lifecycle · priority: สูง · trace: AT-11/BR-DN-04 · actor: wh_lead
- Setup: role=wh_lead · seed=Reference draft valid · files=—
- Start: OPEN `#/view/<draft-dn>`
- ผ่านเมื่อ: ready และ read-only

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ยืนยันพร้อมส่ง** | — | toast **พร้อมส่ง — รอออกรถ**; pill **พร้อมส่ง** | ☐ |
| 2 | VERIFY แท็บข้อมูลจัดส่ง | — | ฟอร์มเป็น read-only และมี **แก้ไขข้อมูลส่ง** | ☐ |

### TC-L02 — Ready → In transit + GI
- group: Lifecycle · priority: สูง · trace: AT-13/LOCK-10/XT-02 · actor: assigned driver
- Setup: role=assigned driver · seed=Reference ready, own carrier · files=—
- Start: OPEN `#/view/<ready-dn>`
- ผ่านเมื่อ: dispatchครั้งเดียวและมีประวัติ GI

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ออกรถ / ส่งมอบขนส่ง** | — | modal ยืนยันแสดงผลตัดสต๊อก | ☐ |
| 2 | CLICK **ยืนยันออกรถ · ตัดสต๊อก** | — | toast **ออกรถแล้ว — ตัดสต๊อกจริงและแจ้งลูกค้าแล้ว**; สถานะกำลังจัดส่ง | ☐ |
| 3 | CLICK **ประวัติ** | — | เห็น Goods Issue/ออกรถหนึ่งครั้ง | ☐ |

### TC-L03 — 3PL ไม่มี tracking (negative)
- group: Lifecycle · priority: สูง · trace: AT-12/BR-DN-06 · actor: wh_lead
- Setup: role=wh_lead · seed=ready 3PL tracking blank · files=—
- Start: OPEN `#/view/<ready-3pl-dn>`
- ผ่านเมื่อ: dispatch ถูกบล็อก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ออกรถ / ส่งมอบขนส่ง** แล้ว confirm | — | เห็น **กรอกเลขติดตามพัสดุก่อนส่งมอบขนส่ง** | ☐ |
| 2 | VERIFY สถานะ/ประวัติ | — | ยังพร้อมส่ง; ไม่มี GI | ☐ |

### TC-L04 — Tracking เดินหน้า
- group: Lifecycle · priority: สูง · trace: AT-14/BR-DN-07 · actor: assigned driver
- Setup: role=assigned driver · seed=in_transit · files=—
- Start: OPEN `#/view/<in-transit-dn>`
- ผ่านเมื่อ: timeline เพิ่ม stage ถัดไป

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ปุ่มอัปเดตสถานะขนส่ง | — | timeline เพิ่ม stage ถัดไปและ toast ลงท้าย **— แจ้งลูกค้าแล้ว** | ☐ |
| 2 | CLICK ซ้ำจนถึงก่อน delivered | — | stage เดินหน้า ไม่ย้อน/ซ้ำ | ☐ |

### TC-L05 — ห้ามกด Tracking สุดท้ายแทน POD
- group: Lifecycle · priority: สูง · trace: BR-DN-07/TRANSITION_INVALID · actor: driver
- Setup: role=driver · seed=tracking at last pre-delivery stage · files=—
- Start: OPEN `#/view/<in-transit-dn>`
- ผ่านเมื่อ: บังคับใช้ POD

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK อัปเดตสถานะขนส่ง | — | เห็น **สถานะสุดท้าย — บันทึกผลส่ง (POD) แทน** | ☐ |
| 2 | VERIFY สถานะ | — | ยังไม่เป็นส่งสำเร็จ | ☐ |

### TC-L06 — Failed ครั้งแรกเริ่ม 1
- group: Lifecycle · priority: สูง · trace: AT-15/LOCK-12 · actor: driver
- Setup: role=driver · seed=in_transit attempts=[] · files=—
- Start: OPEN `#/view/<in-transit-dn>`
- ผ่านเมื่อ: modal/history นับครั้งที่ 1

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ส่งไม่สำเร็จ** | — | modal แสดง **ครั้งที่ 1** | ☐ |
| 2 | SELECT เหตุผล, TYPE note, CLICK บันทึก | DS-REF reason | toast **บันทึกส่งไม่สำเร็จ — นัดส่งใหม่หรือตีกลับทั้งใบ** | ☐ |
| 3 | VERIFY ประวัติ | — | เห็น **ส่งไม่สำเร็จ ครั้งที่ 1** | ☐ |

### TC-L07 — นัดส่งใหม่
- group: Lifecycle · priority: สูง · trace: AT-16 · actor: wh_lead
- Setup: role=wh_lead · seed=failed attempt 1 · files=—
- Start: OPEN `#/view/<failed-dn>`
- ผ่านเมื่อ: ready และ attempts ไม่หาย

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **พร้อมส่งอีกครั้ง** | — | toast **นัดส่งใหม่แล้ว — รอออกรถ**; สถานะพร้อมส่ง | ☐ |
| 2 | CLICK **ประวัติ** | — | attempt ครั้งที่ 1 ยังอยู่และมี event นัดใหม่ | ☐ |

### TC-L08 — POD บังคับชื่อผู้รับ
- group: POD · priority: สูง · trace: AT-17/BR-DN-09 · actor: driver
- Setup: role=driver · seed=in_transit · files=—
- Start: OPEN `#/view/<in-transit-dn>`
- ผ่านเมื่อ: ชื่อว่างถูกบล็อก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **บันทึกผลส่ง (POD)** | — | POD modal เปิด | ☐ |
| 2 | CLICK ยืนยันโดยไม่กรอกชื่อผู้รับ | — | เห็น **ระบุชื่อผู้รับสินค้า** | ☐ |

### TC-L09 — POD rejected ต้องมีเหตุผล
- group: POD · priority: สูง · trace: AT-18/BR_DN_POD_INVALID · actor: driver
- Setup: role=driver · seed=in_transit · files=—
- Start: OPEN `#/view/<in-transit-dn>`
- ผ่านเมื่อ: rejected line ไม่มีเหตุผลผ่านไม่ได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **บันทึกผลส่ง (POD)** | — | modal เปิด | ☐ |
| 2 | TYPE ชื่อผู้รับและจำนวนไม่รับ >0 แต่ไม่เลือกเหตุผล | — | summary แสดงรับบางส่วน | ☐ |
| 3 | CLICK ยืนยัน | — | บรรทัดที่ขาดเหตุผลถูกบล็อก; modal ยังเปิด | ☐ |

### TC-L10 — POD รับครบ
- group: POD · priority: สูง · trace: AT-19/XT-02/03/05 · actor: driver
- Setup: role=driver · seed=in_transit SO source · files=—
- Start: OPEN `#/view/<in-transit-dn>`
- ผ่านเมื่อ: delivered และ print/historyอัปเดต

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **บันทึกผลส่ง (POD)** | — | modal เปิด; ไม่รับทุกบรรทัด=0 | ☐ |
| 2 | TYPE ชื่อผู้รับแล้ว CLICK ยืนยัน | ผู้รับทดสอบ | สถานะส่งสำเร็จ; timeline completed | ☐ |
| 3 | CLICK แท็บ **ใบส่งของ** | — | เห็นจำนวนรับจริงและผลรับครบ | ☐ |

### TC-L11 — ตีกลับทั้งใบ
- group: Return · priority: สูง · trace: AT-21/EC-04/LOCK-11 · actor: wh_lead
- Setup: role=wh_lead · seed=failed with GI · files=—
- Start: OPEN `#/view/<failed-dn>`
- ผ่านเมื่อ: เหตุผลบังคับ, reverse และ Packing คืนคิว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ตีกลับทั้งใบ** | — | modal เตือนคืนสต๊อก/SO/คิว | ☐ |
| 2 | CLICK ยืนยันโดยไม่กรอกเหตุผล | — | เห็น **กรุณาระบุเหตุผล** | ☐ |
| 3 | TYPE เหตุผลแล้ว confirm | DS-REF reason | toast **ตีกลับทั้งใบ — คืนสต๊อกและแจ้ง Sales แล้ว** | ☐ |
| 4 | OPEN `#/list` | — | PACK เดิมกลับแท็บคิว | ☐ |

### TC-L12 — ยกเลิกก่อนออกรถ
- group: Cancel · priority: สูง · trace: AT-22/EC-05 · actor: wh_lead
- Setup: role=wh_lead · seed=draft/ready reference no GI · files=—
- Start: OPEN `#/view/<pre-dispatch-dn>`
- ผ่านเมื่อ: cancelคืนคิวและไม่มี reverse

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ยกเลิกใบส่งของ | — | modal ขอเหตุผล | ☐ |
| 2 | TYPE เหตุผลแล้ว confirm | DS-REF reason | toast **ยกเลิกแล้ว — ใบแพ็คกลับเข้าคิวรอออกใบส่งของ** | ☐ |
| 3 | VERIFY ประวัติ | — | มี cancel; ไม่มี reverse Goods Issue | ☐ |

### TC-L13 — ยกเลิกหลังออกรถ
- group: Cancel · priority: สูง · trace: AT-23/LOCK-11 · actor: wh_lead
- Setup: role=wh_lead · seed=in_transit reference with GI · files=—
- Start: OPEN `#/view/<in-transit-dn>`
- ผ่านเมื่อ: reverse มาก่อนคืนคิว

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ยกเลิกใบส่งของ | — | modal ระบุว่าจะคืนสต๊อก | ☐ |
| 2 | TYPE เหตุผลแล้ว confirm | DS-REF reason | toast ยกเลิกสำเร็จและ PACK กลับคิว | ☐ |
| 3 | VERIFY ประวัติ | — | เห็น reverse Goods Issue ก่อน event ยกเลิก/คืนคิว | ☐ |

### TC-L14 — POD บางส่วนเลือก backorder
- group: POD · priority: สูง · trace: AT-20/25 · actor: wh_lead
- Setup: role=wh_lead · seed=in_transit SO source · files=—
- Start: OPEN `#/view/<in-transit-dn>`
- ผ่านเมื่อ: partial และเปิดงานค้างส่ง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | บันทึก POD ด้วยจำนวนไม่รับบางส่วนและเหตุผล | — | modal ถามจัดส่งซ้ำหรือปิดจบ | ☐ |
| 2 | CLICK **จัดส่งซ้ำ (backorder)** | — | toast **เปิดงานค้างส่งแล้ว — กลับคิวหยิบ/แพ็ค (mock)** | ☐ |
| 3 | VERIFY ประวัติ | — | มี partial และ backorder decision | ☐ |

### TC-L15 — POD บางส่วนเลือก close-short
- group: POD · priority: สูง · trace: AT-26/XT-05 · actor: wh_lead
- Setup: role=wh_lead · seed=in_transit SO source · files=—
- Start: OPEN `#/view/<in-transit-dn>`
- ผ่านเมื่อ: close-short และไม่สร้าง Credit Note อัตโนมัติ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | บันทึก POD บางส่วนพร้อมเหตุผล | — | modal decision เปิด | ☐ |
| 2 | CLICK **ปิดจบเท่าที่ส่งได้** | — | toast **ปิดจบเท่าที่ส่งได้ — แจ้ง Sales/บัญชี** | ☐ |
| 3 | VERIFY ประวัติ | — | มี close-short/ส่งต่อ Credit Note ถ้าวางบิลแล้ว; ไม่มีเลข CN ใหม่ | ☐ |

### Group T — Stock Transfer

### TC-T01 — เห็น Transfer fixture และปลายทาง
- group: Transfer · priority: สูง · trace: AT-28/LOCK-04 · actor: wh_lead
- Setup: role=wh_lead · seed=fresh prototype · files=—
- Start: OPEN `#/list`
- ผ่านเมื่อ: แถว fixture แสดงต้นทางและปลายทางครบ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แถว `PACK-2026-0460` | — | เห็น `TR-2026-0012` และ `WH-01 → WH-02` | ☐ |
| 2 | CLICK รหัส/แถว PACK | — | modal รายละเอียดแสดงข้อมูล Transfer ไม่ใช่ลูกค้า SO | ☐ |

### TC-T02 — สร้าง Transfer DN
- group: Transfer · priority: สูง · trace: AT-28/29/BR-DN-15 · actor: wh_lead
- Setup: role=wh_lead · seed=DS-TRANSFER fresh · files=—
- Start: OPEN `#/list`
- ผ่านเมื่อ: DN สร้างได้และ header/detail คง from→to

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **ออกใบส่งของ** ที่ `PACK-2026-0460` | — | confirm แสดง `TR-2026-0012` | ☐ |
| 2 | กรอก assignment แล้ว CLICK **ยืนยันออกใบส่งของ** | DS-REF | drawer เปิดสถานะร่าง | ☐ |
| 3 | VERIFY ส่วนหัวและแท็บ **ข้อมูลจัดส่ง** | — | เห็น `WH-01 → WH-02` | ☐ |

### TC-T03 — Transfer dispatch ไม่ sync SO
- group: Transfer · priority: สูง · trace: AT-29/XT-04 · actor: wh_lead
- Setup: role=wh_lead · seed=Transfer DN ready · files=—
- Start: OPEN `#/view/<transfer-dn>`
- ผ่านเมื่อ: dispatch/GI ปกติแต่ไม่มี SO document flow

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK dispatch และ **ยืนยันออกรถ · ตัดสต๊อก** | — | สถานะกำลังจัดส่งและมี GI | ☐ |
| 2 | VERIFY แท็บข้อมูล/ประวัติ | — | มี Transfer ref/from→to; ไม่มีข้อความอัปเดต SO | ☐ |

### TC-T04 — Transfer return/cancel ไม่แตะ SO
- group: Transfer · priority: สูง · trace: AT-30/EC-06 · actor: wh_lead
- Setup: role=wh_lead · seed=Transfer DN in_transit/failed · files=—
- Start: OPEN `#/view/<transfer-dn>`
- ผ่านเมื่อ: reverse + transfer path เท่านั้น

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK ตีกลับหรือยกเลิก แล้วกรอกเหตุผล | DS-REF reason | การยืนยันสำเร็จ; PACK กลับคิว | ☐ |
| 2 | VERIFY ประวัติ | — | มี reverse/Transfer event; ไม่มี SO status/counter event | ☐ |

### Group M — Manual DN

### TC-M01 — เปิดฟอร์ม Manual แยกจาก Reference
- group: Manual · priority: สูง · trace: AT-31/LOCK-05 · actor: wh_lead
- Setup: role=wh_lead · seed=fresh · files=—
- Start: OPEN `#/list`
- ผ่านเมื่อ: ปุ่ม/ฟอร์ม Manual ชัดเจนและไม่ขอ PACK

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างแบบ Manual** | — | modal หัวข้อสร้างเอกสาร Manual เปิด | ☐ |
| 2 | VERIFY ฟอร์ม | — | มีเลขอ้างอิง ผู้รับ ที่อยู่; ไม่มีขั้นเลือก PACK | ☐ |

### TC-M02 — Manual create required (negative)
- group: Manual · priority: สูง · trace: ERR_VALIDATION_FAILED · actor: wh_lead
- Setup: role=wh_lead · seed=open Manual form blank · files=—
- Start: OPEN `#/list` แล้ว CLICK **สร้างแบบ Manual**
- ผ่านเมื่อ: blank ถูกบล็อก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **สร้างเอกสาร Manual** | — | เห็น **กรอกเลขอ้างอิง ผู้รับ และที่อยู่จัดส่งให้ครบ** | ☐ |
| 2 | VERIFY modal | — | ยังเปิดและไม่มี DN ใหม่ | ☐ |

### TC-M03 — สร้าง Manual สำเร็จ
- group: Manual · priority: สูง · trace: AT-32/BR-DN-18 · actor: wh_lead
- Setup: role=wh_lead · seed=fresh · files=—
- Start: OPEN `#/list` แล้ว CLICK **สร้างแบบ Manual**
- ผ่านเมื่อ: Manual draft/audit-only

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | TYPE เลขอ้างอิง ผู้รับ ที่อยู่ | DS-MANUAL | ค่าปรากฏครบ | ☐ |
| 2 | CLICK **สร้างเอกสาร Manual** | — | toast มีคำว่า **สร้าง** และ **แบบ Manual แล้ว**; drawer เปิด | ☐ |
| 3 | CLICK **ประวัติ** | — | เห็นสร้างแบบ Manual; ไม่มี PACK/Goods Issue/source sync | ☐ |

### TC-M04 — Manual transition บังคับเหตุผล
- group: Manual · priority: สูง · trace: AT-33/EC-07 · actor: wh_lead
- Setup: role=wh_lead · seed=Manual draft · files=—
- Start: OPEN `#/view/<manual-dn>`
- ผ่านเมื่อ: blank reason ไม่เปลี่ยนสถานะ

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **อัปเดตสถานะ Manual** | — | modal target/status/reason เปิด | ☐ |
| 2 | SELECT สถานะใหม่แล้ว CLICK confirm โดยเว้นเหตุผล | ready | เห็น **กรุณาระบุเหตุผล** | ☐ |
| 3 | VERIFY pill/history | — | สถานะเดิมและไม่มี transition ใหม่ | ☐ |

### TC-M05 — Manual เปลี่ยนหลายสถานะ
- group: Manual · priority: สูง · trace: AT-34/LOCK-06 · actor: wh_lead
- Setup: role=wh_lead · seed=Manual draft · files=—
- Start: OPEN `#/view/<manual-dn>`
- ผ่านเมื่อ: เลือกหลาย target ได้และเหตุผลทุกครั้งอยู่ใน history

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | อัปเดต Manual เป็น ready พร้อมเหตุผล | DS-MANUAL reason | toast **อัปเดตสถานะ Manual แล้ว**; pill ready | ☐ |
| 2 | อัปเดตเป็น in_transit พร้อมเหตุผลใหม่ | — | pill in_transit | ☐ |
| 3 | อัปเดตเป็น delivered พร้อมเหตุผลใหม่ | — | pill delivered | ☐ |
| 4 | CLICK **ประวัติ** | — | เห็น 3 transition และเหตุผลแต่ละครั้ง | ☐ |

### TC-M06 — Manual ไม่มี automation
- group: Manual · priority: สูง · trace: AT-35/LOCK-07 · actor: wh_lead
- Setup: role=wh_lead · seed=Manual draft · files=—
- Start: OPEN `#/view/<manual-dn>`
- ผ่านเมื่อ: in_transit/delivered ไม่มี GI/source sync

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | อัปเดตเป็น in_transit แล้ว delivered พร้อมเหตุผล | — | สถานะเปลี่ยนตามที่เลือก | ☐ |
| 2 | VERIFY ประวัติ/Document Flow | — | ไม่มี Goods Issue, reverse, SO, Transfer หรือ AR automation | ☐ |

### TC-M07 — Manual เลือก returned/cancelled ได้
- group: Manual · priority: กลาง · trace: all manual target states · actor: wh_lead
- Setup: role=wh_lead · seed=Manual record · files=—
- Start: OPEN `#/view/<manual-dn>`
- ผ่านเมื่อ: terminal status ผ่าน manual actionและยังไม่มี automation

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK **อัปเดตสถานะ Manual** แล้ว SELECT returned | reason | pill returned; auditเพิ่ม | ☐ |
| 2 | ทำกับ Manual record อีกใบ SELECT cancelled | reason | pill cancelled; auditเพิ่ม | ☐ |
| 3 | VERIFY ทั้งสองใบ | — | ไม่มี stock/source event | ☐ |

### Group U — Permission / UX / print

### TC-U01 — Reference non-draft read-only
- group: UX · priority: สูง · trace: AT-36/BR-DN-16 · actor: wh_lead
- Setup: role=wh_lead · seed=Reference ready · files=—
- Start: OPEN `#/view/<ready-dn>`
- ผ่านเมื่อ: ไม่มี textbox จนกด edit

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY แท็บ **ข้อมูลจัดส่ง** | — | ข้อมูลแสดงแบบอ่านอย่างเดียวและมี **แก้ไขข้อมูลส่ง** | ☐ |
| 2 | CLICK **แก้ไขข้อมูลส่ง** | — | ช่องแก้ไขปรากฏเฉพาะสถานะพร้อมส่ง | ☐ |

### TC-U02 — Refresh ปิด drawer
- group: UX · priority: สูง · trace: AT-39/EC-02 · actor: wh_lead
- Setup: role=wh_lead · seed=เปิด drawer DN · files=—
- Start: OPEN `#/view/<existing-dn>`
- ผ่านเมื่อ: full refresh ไม่ค้าง drawer stale

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY drawer เปิด | — | เห็นหัว DN และแท็บ | ☐ |
| 2 | PRESS browser refresh | — | route/list base แสดง; drawer ไม่ค้างเปิด | ☐ |

### TC-U03 — A4 ก่อน/หลัง POD และข้อความยาว
- group: Print · priority: กลาง · trace: AT-37/EC-09/XT-06 · actor: viewer
- Setup: role=viewer · seed=DN ก่อน POD และอีกใบหลัง POD · files=—
- Start: OPEN `#/view/<dn>`
- ผ่านเมื่อ: preview เปลี่ยนตาม POD และพิมพ์ไม่ตัดข้อมูลหลัก

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | CLICK แท็บ **ใบส่งของ** ของใบก่อน POD | — | ตารางมีช่องตรวจรับ/checkbox | ☐ |
| 2 | OPEN ใบหลัง POD แล้ว CLICK แท็บ **ใบส่งของ** | — | เห็นจำนวนรับ/ไม่รับจริงและผล | ☐ |
| 3 | CLICK **พิมพ์** | — | print preview A4 มีหัวเอกสาร รายการ totals และลายเซ็น; ข้อความไทยไม่ล้น | ☐ |

### TC-U04 — สิทธิ์ viewer/driver
- group: Permission · priority: สูง · trace: AT-40/ERR_FORBIDDEN · actor: viewer + unassigned driver
- Setup: role switch available · seed=Reference DN · files=—
- Start: OPEN `#/view/<dn>`
- ผ่านเมื่อ: read allowed; mutations denied by persona

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | SELECT role viewer | — | เห็นข้อมูล/พิมพ์ แต่ไม่มีปุ่ม create/ready/dispatch/cancel/manual status | ☐ |
| 2 | SELECT role driver ที่ไม่ได้รับมอบหมาย | — | mutation ของใบนี้ไม่ปรากฏ/ทำไม่ได้ | ☐ |
| 3 | SELECT role wh_lead | — | action ที่สถานะอนุญาตกลับมา | ☐ |

### Group X — Engineering / cross-module

### TC-X01 — `[AI-DEFAULT]` idempotency และ atomic movement (ต้อง simulate)
- group: Engineering · priority: สูง · trace: EC-11/14/XT-02 · actor: integration tester
- Setup: role=wh_lead · seed=ready Reference DN + Inventory baseline captured · files=—
- Start: OPEN `#/view/<ready-dn>`
- ผ่านเมื่อ: duplicate/partial failureไม่สร้างผลซ้ำหรือครึ่งกลาง

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFY+จด baseline | stock/source counters/audit count | เก็บค่าก่อน dispatch | ☐ |
| 2 | CLICK dispatch แล้วส่ง request ซ้ำด้วย idempotency key เดิม `(ต้อง simulate)` | — | ได้ผลเดิม; UI/historyมี GI ครั้งเดียว | ☐ |
| 3 | ฉีด failure กลาง movement แล้ว retryด้วย keyใหม่ `(ต้อง simulate)` | — | รอบล้มเหลวไม่เปลี่ยน state/stock; retryสำเร็จครบทั้งชุด | ☐ |

### TC-X02 — `[AI-DEFAULT]` stale version และ invalid transition (ต้อง simulate)
- group: Engineering · priority: สูง · trace: EC-10/ERR_STALE_DATA/TRANSITION_INVALID · actor: wh_lead
- Setup: role=wh_lead · seed=เปิด DN เดียวกันสอง session · files=—
- Start: OPEN `#/view/<dn>`
- ผ่านเมื่อ: stale session ไม่ทับข้อมูลใหม่

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | เปลี่ยนสถานะจาก session A | — | A สำเร็จและ version เพิ่ม | ☐ |
| 2 | ส่ง mutation จาก session B version เก่า `(ต้อง simulate)` | — | 409/reload prompt; state ไม่ย้อน | ☐ |
| 3 | ส่ง transition ที่สถานะปัจจุบันไม่อนุญาต `(ต้อง simulate)` | — | ถูกปฏิเสธ; auditไม่เพิ่ม business success | ☐ |

### TC-X03 — `[AI-DEFAULT]` master/outbox/document failure (ต้อง simulate)
- group: Engineering · priority: สูง · trace: EC-12/13/XT-06/07 · actor: integration tester
- Setup: role=wh_lead · seed=master ถูก inactive หลัง draft; outbox worker down · files=—
- Start: OPEN `#/view/<draft-dn>`
- ผ่านเมื่อ: active master ถูก revalidate; historical snapshotคงอยู่; outbox retryได้

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | VERIFYค่า driver/vehicle snapshotเดิม | — | ยังแสดงประวัติเดิม | ☐ |
| 2 | CLICK ready/dispatchหลัง master inactive `(ต้อง simulate)` | — | transitionถูกบล็อกจนเลือก active master | ☐ |
| 3 | ทำ transitionเมื่อ notification worker down `(ต้อง simulate)` | — | business state commit + outbox pending; retryไม่ยิงซ้ำ | ☐ |
| 4 | พิมพ์/ส่งเอกสารเมื่อ store ชั่วคราวล้ม `(ต้อง simulate)` | — | แสดง failure/retry; เลขเอกสารเดิม immutable | ☐ |

## วิธีที่ agent รัน (Run protocol)

1. เริ่ม fresh browser context ต่อกลุ่ม เพราะ prototype state อยู่ใน memory; ห้าม refresh ระหว่างเคสที่พึ่งข้อมูลที่สร้างใน session เว้นแต่เคสระบุให้ refresh.
2. ตั้ง role/seed ตาม Setup และจด DN/PACK ที่ใช้จริงใน evidence.
3. ทำ Action ทีละ step; ติ๊ก Result เฉพาะเมื่อ Expected ที่เห็นตรงตัว.
4. หาก anchor ไม่อยู่ ให้บันทึกข้อความ/routeที่เห็นจริงและ mark blocked; ห้ามเดาปุ่มแทน.
5. เคส `(ต้อง simulate)` รันกับ production API/test double; prototype ใช้ตรวจเพียง UI/state anchor.

## Coverage Audit

| หมวด | covered / total |
|---|---|
| Acceptance AT | 40 / 40 |
| Business rules | 22 / 22 |
| Edge cases | 14 / 14 |
| Error codes/catalog groups | 13 / 13 |
| Permission cells สำคัญ | 8 / 8 |
| Cross-module XT | 7 / 7 |
| Scope Lock | 12 / 12 |
| Routes / reference+manual states | 3/3 routes; all states |

- AI-default: 5/5 covered; 3 cases require service simulation.
- OOS skipped: real 3PL API, route optimization, multi-vehicle split, mobile e-POD/GPS, automatic freight/Credit Note and master maintenance — outside Scope Lock.
- Manifest cross-check (FRD `00_OVERVIEW §0.12`): ✅ 8/8 rows.

## Result Report (schema)

```json
{
  "feature_id": "F-WH-DN",
  "run_at": "<iso datetime>",
  "results": [
    { "id": "TC-Q01", "status": "pass|fail|blocked", "failed_step": null, "evidence": "", "note": "" }
  ],
  "summary": { "total": 50, "pass": 0, "fail": 0, "blocked": 0 }
}
```
