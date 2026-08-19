# AI Test Cases — F-WH-PACK Packing

ชุดทดสอบสำหรับ AI browser/vision agent ยึดข้อความที่เห็นใน `f-wh-packing.html`; backend-only/fault cases ระบุว่าต้อง simulate.

## Meta

| Field | Value |
|---|---|
| Feature | F-WH-PACK — Packing |
| Version | 1.0 · 2026-08-19 |
| App entry | เปิดไฟล์/แอปที่ route `#/list` |
| Routes | `#/list`; detail เปิดจากแถว/ลิงก์ Packing |
| Sources | BRD, FRD FULL pack, root HTML, Picking contract, print specs, NTF brief |
| Cases | 40 cases · Queue 5 · Pack 16 · Lifecycle 7 · Print 3 · Permission 4 · Integration/Security 5 |

## Coverage

| Group | Cases | Priority |
|---|---:|---|
| Queue/intake/list | 5 | high |
| Carton/scan/weight | 14 | high |
| Finish/reopen/cancel/state | 7 | high |
| Print/audit | 3 | high |
| Permission/UX | 4 | high/medium |
| Cross-module/security/fault | 5 | high |

## Coverage Ledger

### Acceptance (06_TESTS)

| Item | Cases |
|---|---|
| AT-01..03 | TC-Q01..Q04, TC-P01 |
| AT-04..08 | TC-P02..P14 |
| AT-09..12 | TC-L01..L07 |
| AT-13..15 | TC-D01..D03 |
| AT-16..20 | TC-X01, TC-U01..U04, TC-X03..X05 |

### Business Rules

| Rule | Cases |
|---|---|
| BR-PACK-01/03 | TC-Q01,Q02,X01,X02 |
| BR-PACK-02 | TC-P10,D01,D02 |
| BR-PACK-04 | TC-P02,P03 |
| BR-PACK-05 | TC-P05..P09,X03 |
| BR-PACK-06/07 | TC-P02,P04,P11..P14 |
| BR-PACK-08 | TC-P15,P16 |
| BR-PACK-09 | TC-L01..L03 |
| BR-PACK-10 | TC-L04,L05,D03 |
| BR-PACK-11 | TC-L07,X02 |
| BR-PACK-12 | TC-L06 |
| BR-PACK-13 | TC-D01,D02,X04 |
| BR-PACK-14 | TC-U01..U03,L07 |
| BR-PACK-15/16 | TC-D03,X05 |

### Edge Cases and Errors

| Item | Cases |
|---|---|
| EC-01 / idempotency mismatch | TC-X01 |
| EC-02/04 stale/concurrent allocation | TC-X03 |
| EC-03 permission revoked | TC-U04 |
| EC-05 compensation/reopen/cancel | TC-L04..L06 |
| EC-06 missing weight | TC-P14 |
| EC-07 print outage | TC-X04 |
| EC-08 notify outage | TC-X05 |
| EC-09 DN outage/replay | TC-X02 |
| EC-10 Transfer gated | TC-Q05 |
| `BR_SOURCE_NOT_ELIGIBLE` | TC-Q05 |
| `BR_JOB_UNAVAILABLE` | TC-Q04 |
| `BR_ACTIVE_BOX_EXISTS` | TC-P03 |
| `BR_QTY_EXCEEDS_PICKED` | TC-P07,P08,X03 |
| `BR_INVALID_CARTON` | TC-P04 |
| `BR_WEIGHT_SOURCE_MISSING` | TC-P14 |
| `BR_EMPTY_CARTON` | TC-P15 |
| `BR_PACK_INCOMPLETE` | TC-L02,L03 |
| `BR_PACK_LOCKED_BY_DN` | TC-L05,L07 |
| `BR_CANCEL_REASON_REQUIRED` | TC-L06 |
| `ERR_STALE_DATA` | TC-X03 |
| `ERR_PERMISSION_REVOKED` | TC-U04 |
| print/event/dependency errors | TC-X02,X04,X05 |

### Permission cells

| Cell group | Cases |
|---|---|
| wh_lead view/start/edit/finish/reopen/cancel/DN/export allow | TC-U01,L04,L07 |
| packer own view/start/edit/finish/cancel allow | TC-U02,P01,L01,L06 |
| packer other-job/reopen/DN deny | TC-U02,U03 |
| viewer view allow; all mutations/export-sensitive deny | TC-U03 |
| all roles edit shipped deny | TC-L07 |

### Cross-module / LOCK / States / UI

| Item | Cases |
|---|---|
| XT-01 Picking wave | TC-Q02 |
| XT-02 Transfer gated | TC-Q05 |
| XT-03 DN fail/retry/success | TC-X02 |
| XT-04 notify retry/dedupe | TC-X05 |
| XT-05 master snapshot | TC-P11 |
| LOCK-PACK-01 HTML unchanged behavior | TC-U01,U04 |
| LOCK-PACK-02 Picking contract | TC-Q01,Q02,X01 |
| LOCK-PACK-03 no invented DN | TC-X02 |
| LOCK-PACK-04 NTF only/no approval | TC-X05,U01 |
| LOCK-PACK-05 UX debt verified in production | TC-U04 |
| queue→in_progress→packed→shipped | TC-P01,L01,L07 |
| packed→in_progress; active↔closed; cancel | TC-L04,P16,L06 |
| list loading/empty/filter/export | TC-Q03,Q04,U01 |
| keyboard/focus/Esc/responsive | TC-U04 |

## Data Sets

### DS-A — standard

| Field | Value |
|---|---|
| actor | packer “สมชาย ใจดี” |
| source | PICK-2026-0890 / SO-2026-0201 / WH-01 |
| item | FG-1001 · 24 ขวด · lot L260819-A |
| carton | BOX-M; custom “กล่องทดสอบ QA”, tare 0.50 กก. |

### DS-B — special

Wave PICK-2026-0892 with two SO refs; cold product; free item; pickup order; large order for auto split; job assigned to another user; packed and shipped packs.

### DS-N — invalid/boundary

Unknown scan `NOT-FOUND-999`; qty `-1`, `0`, and remaining+1; blank reason; custom name blank; tare negative; stale version; wrong tenant; Transfer PICK-0889 mock.

## Test Cases

### TC-Q01 — งาน Picking ที่พร้อมปรากฏในคิว
- group: Queue · priority: P0 · trace: AT-01 / BR-PACK-01 / LOCK-02
- Setup: role=packer · seed=PICK-2026-0890 status to_pack · files=—
- Start: OPEN `#/list`
- ผ่านเมื่อ: พบงานและรายละเอียดต้นทางตรง seed

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/list` | — | เห็นแท็บ **คิวรอแพ็ค** และ **ใบแพ็ค** | ☐ |
| 2 | CLICK แท็บ **คิวรอแพ็ค** | — | เห็นแถว PICK-2026-0890 พร้อม SO/คลัง/ผู้หยิบ/จำนวน | ☐ |
| 3 | CLICK แถว PICK-2026-0890 | — | overlay แสดงสินค้า ล็อต วันหมดอายุ ตำแหน่ง และปุ่ม **เริ่มแพ็ค** | ☐ |

### TC-Q02 — wave แตกสองงานและไม่ซ้ำ
- group: Queue/XT · priority: P0 · trace: AT-02 / BR-PACK-03 / XT-01
- Setup: role=wh_lead · seed=PICK-2026-0892 มี 2 source SO และส่งซ้ำด้วย idempotency key เดิม · files=—
- Start: OPEN `#/list`
- ผ่านเมื่อ: มี 2 งานต่าง SO และไม่มีแถวที่สามหลัง refresh

| # | Action | Input | Expected | Result |
|---|---|---|---|---|
| 1 | OPEN `#/list` | — | เห็นงานจาก PICK-2026-0892 จำนวน 2 แถว แยก source ref | ☐ |
| 2 | VERIFY รหัสอ้างอิงทั้งสองแถว | DS-B | source SO ไม่ซ้ำกัน | ☐ |
| 3 | OPEN `#/list` อีกครั้งหลัง retry | — | ยังคง 2 แถว ไม่มี duplicate | ☐ |

### TC-Q03 — search/filter/no-result/reset
- group: List · priority: P1 · trace: FN-90 / UI states
- Setup: role=wh_lead · seed=queue หลายคลัง/สถานะ · files=—
- Start: OPEN `#/list`
- ผ่านเมื่อ: filter ทำงานและ reset คืนรายการ

| 1 | TYPE `ไม่มีรหัสนี้` → ช่องค้นหา | — | ตารางแสดง no-result/ไม่พบรายการ | ☐ |
| 2 | CLICK ปุ่มล้างตัวกรอง/ล้างคำค้นที่มองเห็น | — | รายการกลับมา | ☐ |
| 3 | SELECT `WH-02` → ตัวกรองคลัง | — | ทุกแถวที่เห็นเป็น WH-02 | ☐ |

### TC-Q04 — job ถูกเริ่มไปแล้ว
- group: Queue · priority: P1 · trace: AT-03 / BR_JOB_UNAVAILABLE
- Setup: role=packer · seed=job ที่มี pack active แล้ว · files=—
- Start: OPEN `#/list`
- ผ่านเมื่อ: ไม่สร้างใบซ้ำและเปิดใบเดิมหรือไม่แสดง start

| 1 | CLICK แถว job ที่ active | — | เห็นสถานะ/ลิงก์ไปใบแพ็คเดิม | ☐ |
| 2 | CLICK action เริ่ม/เปิดที่มี | — | เปิด pack เดิม; ไม่มี PACK ใหม่เพิ่มในแท็บ **ใบแพ็ค** | ☐ |

### TC-Q05 — Transfer ยังไม่เป็น contract
- group: Scope guard · priority: P0 · trace: EC-10 / XT-02 / BR_SOURCE_NOT_ELIGIBLE
- Setup: role=wh_lead · seed=PICK-0889 type Transfer; production adapter disabled · files=—
- Start: OPEN `#/list`
- ผ่านเมื่อ: production ไม่สร้างงานจาก Transfer โดยเงียบ

| 1 | OPEN `#/list` | — | Transfer อาจปรากฏเฉพาะ mock/demo ตาม HTML | ☐ |
| 2 | CLICK **เริ่มแพ็ค** บน Transfer ใน environment production-like | — | ถูก block/feature-disabled; ไม่เกิด PACK production | ☐ |

### TC-P01 — เริ่มแพ็ค happy
- group: Lifecycle · priority: P0 · trace: AT-03 / FN-05
- Setup: role=packer · seed=job DS-A ยังไม่ active · files=—
- Start: OPEN `#/list`
- ผ่านเมื่อ: เห็น toast เปิด PACK และ workspace ไม่มีกล่อง

| 1 | CLICK แถว DS-A | — | overlay งานเปิด | ☐ |
| 2 | CLICK ปุ่ม **เริ่มแพ็ค** | — | toast ขึ้นต้น **เปิด PACK-** และบอกเริ่มขั้นที่ 1 เปิดกล่อง | ☐ |
| 3 | VERIFY workspace | — | สถานะกำลังแพ็ค, progress 0%, ยังไม่มีกล่อง active | ☐ |

### TC-P02 — เปิดกล่องจาก master
- group: Carton · priority: P0 · trace: AT-04 / BR-PACK-04,06
- Setup: role=packer · seed=pack in_progress ไม่มี active carton · files=—
- Start: OPEN pack detail
- ผ่านเมื่อ: BOX-M เปิดเป็นกล่อง active พร้อม tare/capacity

| 1 | CLICK control เปิด/เลือกกล่อง | — | dropdown แสดงชนิดกล่องพร้อมชื่อ/ขนาด/tare | ☐ |
| 2 | SELECT `BOX-M` | — | กล่องใหม่ปรากฏเป็นกล่องกำลังแพ็ค หมายเลขถัดไป | ☐ |

### TC-P03 — ห้ามเปิดสองกล่อง
- group: Carton negative · priority: P0 · trace: BR-PACK-04 / BR_ACTIVE_BOX_EXISTS
- Setup: role=packer · seed=pack มี active carton 1 ใบ · files=—
- Start: OPEN pack detail
- ผ่านเมื่อ: กล่องยังมีใบเดียว

| 1 | CLICK action เปิดกล่องใหม่/F3 | — | เห็นข้อความ **ปิดกล่องปัจจุบันก่อน** หรือ action disabled | ☐ |
| 2 | VERIFY จำนวน active carton | — | เท่ากับ 1 | ☐ |

### TC-P04 — custom carton validation
- group: Carton validation · priority: P1 · trace: BR-PACK-06 / BR_INVALID_CARTON
- Setup: role=packer · seed=pack ไม่มี active carton · files=—
- Start: OPEN pack detail
- ผ่านเมื่อ: blank ถูก block; valid custom ถูกใช้

| 1 | CLICK ตัวเลือก **กำหนดเอง** | — | modal ชื่อกล่อง/tare เปิด | ☐ |
| 2 | CLICK ปุ่มยืนยันโดยไม่กรอกชื่อ | — | toast **ใส่ชื่อกล่อง** | ☐ |
| 3 | TYPE `กล่องทดสอบ QA` → ช่องชื่อ | DS-A | ช่องแสดงค่า | ☐ |
| 4 | TYPE `0.50` → ช่องน้ำหนักเปล่า | DS-A | แสดงค่าที่กรอก | ☐ |
| 5 | CLICK ปุ่มยืนยัน | — | toast **ใช้กล่อง "กล่องทดสอบ QA" แล้ว** และชื่อปรากฏใน active carton | ☐ |

### TC-P05 — scan รหัส happy
- group: Scan · priority: P0 · trace: AT-05 / BR-PACK-05
- Setup: role=packer · seed=active carton + FG-1001 remaining 24 · files=—
- Start: OPEN pack detail
- ผ่านเมื่อ: เพิ่มหนึ่งหน่วยและ remaining ลดหนึ่ง

| 1 | VERIFY+บันทึก remaining ของ FG-1001 | seed=24 | จดค่า 24 | ☐ |
| 2 | TYPE `FG-1001` → ช่องสแกน | — | ช่องแสดงรหัส | ☐ |
| 3 | PRESS Enter | — | toast ขึ้นต้น **ใส่** และระบุกล่อง | ☐ |
| 4 | VERIFY remaining/qty ในกล่อง | — | remaining=23 และ qty ในกล่อง=1 | ☐ |

### TC-P06 — scan จำนวนและหน่วยขาย
- group: Scan · priority: P0 · trace: FN-08 / AT-05
- Setup: role=packer · seed=active carton; item รองรับหน่วยขาย factor · files=—
- Start: OPEN pack detail
- ผ่านเมื่อ: แปลงหน่วยเป็น base qty ถูก

| 1 | TYPE `2 ลัง FG-1001` → ช่องสแกน | — | ช่องแสดงข้อความ | ☐ |
| 2 | PRESS Enter | — | qty ในกล่องเพิ่มตาม factor ของ 2 ลังและ remaining ลดเท่ากัน | ☐ |

### TC-P07 — over-pack clamp/block
- group: Scan negative · priority: P0 · trace: AT-06 / BR_QTY_EXCEEDS_PICKED
- Setup: role=packer · seed=FG-1001 remaining 3 · files=—
- Start: OPEN pack detail
- ผ่านเมื่อ: packed ไม่เกิน 3

| 1 | VERIFY+บันทึก remaining | — | จดค่า 3 | ☐ |
| 2 | TYPE `10 FG-1001` → ช่องสแกน | — | พร้อม submit | ☐ |
| 3 | PRESS Enter | — | UI แจ้งส่วนเกินหรือ clamp; remaining เป็น 0 ไม่ติดลบ | ☐ |

### TC-P08 — qty ศูนย์/ลบ
- group: Validation · priority: P1 · trace: BR-PACK-05
- Setup: role=packer · seed=active carton qty FG-1001=1 · files=—
- Start: OPEN pack detail
- ผ่านเมื่อ: ค่าลบ/ศูนย์ไม่สร้าง allocation ติดลบ

| 1 | TYPE `-1` → ช่องจำนวนรายการ FG-1001 | DS-N | ค่าไม่ถูกยอมรับหรือ clamp เป็น 0 | ☐ |
| 2 | CLICK ปุ่ม **ใส่** | — | qty/remaining ไม่เกิดค่าติดลบ | ☐ |

### TC-P09 — เอาออกและ undo
- group: Adjustment · priority: P0 · trace: FN-10,11 / BR-PACK-05
- Setup: role=packer · seed=active carton FG-1001 qty=5 remaining=19 · files=—
- Start: OPEN pack detail
- ผ่านเมื่อ: remove คืน remaining; Ctrl+Z คืนการเปลี่ยนครั้งล่าสุด

| 1 | VERIFY+บันทึก qty/remaining | — | จด 5/19 | ☐ |
| 2 | CLICK ปุ่มลบ/ลดหนึ่งที่รายการในกล่อง | — | qty=4; remaining=20 | ☐ |
| 3 | PRESS Ctrl+Z | — | toast **เลิกทำแล้ว**; qty=5; remaining=19 | ☐ |

### TC-P10 — free/cold/pickup rendering
- group: Special · priority: P1 · trace: BR-PACK-02 / FN-22
- Setup: role=wh_lead · seed=pack มี free item+cold item+pickup · files=—
- Start: OPEN pack detail
- ผ่านเมื่อ: รายการแพ็คได้และ print preview แสดง note ที่เหมาะสม

| 1 | CLICK แท็บ **รายละเอียด·อ้างอิง** | — | free/cold/pickup facts ปรากฏตาม seed | ☐ |
| 2 | CLICK แท็บ **ป้ายกล่อง·ใบแพ็ค** | — | เห็นข้อความของแถมไม่มีมูลค่าภาษี, อุณหภูมิ, ลูกค้ามารับเองตามเงื่อนไข | ☐ |

### TC-P11 — master snapshot ไม่เปลี่ยนย้อนหลัง
- group: Data integrity · priority: P1 · trace: XT-05 / BR-PACK-06
- Setup: role=wh_lead · seed=เปิด BOX-M แล้วแก้ชื่อ/tare master ผ่าน fixture ก่อน refresh · files=—
- Start: OPEN pack detail
- ผ่านเมื่อ: กล่องเดิมคง snapshot

| 1 | VERIFY+บันทึกชื่อ/tare กล่องเดิม | — | จดค่าก่อน master change | ☐ |
| 2 | OPEN pack detail หลัง master change | — | กล่องเดิมยังแสดงค่าที่จดไว้; กล่องใหม่ใช้ค่าใหม่ | ☐ |

### TC-P12 — น้ำหนักคำนวณใหม่
- group: Weight · priority: P0 · trace: AT-08 / BR-PACK-07
- Setup: role=packer · seed=active carton tare และ item weight known · files=—
- Start: OPEN pack detail
- ผ่านเมื่อ: ค่าตรงสูตร

| 1 | CLICK ปุ่มคำนวณน้ำหนัก | — | toast ขึ้นต้น **คำนวณน้ำหนักโดยประมาณ** | ☐ |
| 2 | VERIFY ช่องน้ำหนัก | — | เท่ากับ tare + Σ(qty×weight) ตาม seed | ☐ |

### TC-P13 — actual weight override
- group: Weight · priority: P1 · trace: BR-PACK-07
- Setup: role=packer · seed=active carton computed 10.0 kg · files=—
- Start: OPEN pack detail
- ผ่านเมื่อ: 10.4 ถูกเก็บ/แสดงและ audit trace ได้

| 1 | TYPE `10.4` → ช่องน้ำหนัก | — | ช่องแสดง 10.4 | ☐ |
| 2 | CLICK ปุ่มปิดกล่อง | — | closed carton แสดง 10.4 กก. | ☐ |
| 3 | CLICK แท็บ **ประวัติ** | — | เห็น action ปิดกล่อง/น้ำหนักที่ใช้ | ☐ |

### TC-P14 — missing unit weight `(ต้อง simulate)`
- group: Weight negative · priority: P0 · trace: EC-06 / BR_WEIGHT_SOURCE_MISSING
- Setup: role=packer · seed=item ไม่มี weight_per_base_uom · inject production mode (no mock fallback) · files=—
- Start: OPEN pack detail
- ผ่านเมื่อ: ไม่ silently ใช้ mock/zero

| 1 | CLICK ปุ่มคำนวณน้ำหนัก | — | UI แจ้งว่าไม่มีข้อมูลน้ำหนักหรือขอกรอก actual ตามสิทธิ์ | ☐ |
| 2 | VERIFY ปุ่มปิดกล่อง | — | ถูก block จนมีน้ำหนักที่ policy ยอมรับ | ☐ |

### TC-P15 — ปิดกล่องว่าง
- group: Carton negative · priority: P0 · trace: BR-PACK-08 / BR_EMPTY_CARTON
- Setup: role=packer · seed=active carton empty · files=—
- Start: OPEN pack detail
- ผ่านเมื่อ: กล่องยัง active

| 1 | PRESS F2 | — | toast **กล่องว่าง** | ☐ |
| 2 | VERIFY กล่อง | — | ยังเปิดอยู่และไม่มี label valid | ☐ |

### TC-P16 — ปิดและ reopen กล่อง
- group: Carton lifecycle · priority: P0 · trace: AT-07,11 / BR-PACK-08,10
- Setup: role=wh_lead · seed=active carton non-empty; no DN · files=—
- Start: OPEN pack detail
- ผ่านเมื่อ: ปิดแล้วมี label; reopen invalidate ป้ายเดิม

| 1 | PRESS F2 | — | toast **ปิดกล่อง 1 แล้ว**; กล่องย้ายไป closed section | ☐ |
| 2 | CLICK ปุ่ม **เปิดแก้ไข** ของกล่อง 1 | — | กล่องกลับ active และประวัติบอก **ป้ายเดิมยกเลิก** | ☐ |

### TC-L01 — finish happy
- group: Lifecycle · priority: P0 · trace: AT-09 / BR-PACK-09
- Setup: role=packer · seed=remaining 0, all cartons closed, no DN · files=—
- Start: OPEN pack detail
- ผ่านเมื่อ: packed summary replaces editor

| 1 | CLICK ปุ่ม **ปิดงานแพ็ค** | — | toast **แพ็คเสร็จ — พร้อมออกใบส่งของ** | ☐ |
| 2 | VERIFY workspace | — | stepper/editor/active carton หาย; summary+closed cartons อยู่ | ☐ |

### TC-L02 — finish ยังเหลือสินค้า
- group: Lifecycle negative · priority: P0 · trace: AT-10 / BR_PACK_INCOMPLETE
- Setup: role=packer · seed=remaining 5, no active carton · files=—
- Start: OPEN pack detail
- ผ่านเมื่อ: status ไม่เปลี่ยน

| 1 | VERIFY ปุ่ม **ปิดงานแพ็ค** | — | disabled และบอกว่ายังแพ็คไม่ครบ 5 หน่วย | ☐ |

### TC-L03 — finish มีกล่องเปิด
- group: Lifecycle negative · priority: P0 · trace: AT-10 / BR_PACK_INCOMPLETE
- Setup: role=packer · seed=remaining 0, carton 2 active · files=—
- Start: OPEN pack detail
- ผ่านเมื่อ: ต้องปิดกล่องก่อน

| 1 | CLICK/VERIFY ปุ่ม **ปิดงานแพ็ค** | — | disabled/ข้อความ **ปิดกล่อง 2 ก่อน** | ☐ |

### TC-L04 — reopen pack ก่อน DN
- group: Lifecycle · priority: P1 · trace: BR-PACK-10
- Setup: role=wh_lead · seed=pack packed ไม่มี dn_ref · files=—
- Start: OPEN pack detail
- ผ่านเมื่อ: กลับ in_progress พร้อม audit

| 1 | CLICK ปุ่ม **แก้ไขกล่อง** | — | มี confirm/reason ตาม UI | ☐ |
| 2 | TYPE `ตรวจพบสินค้าผิดกล่อง` → ช่องเหตุผล | — | ช่องแสดงค่า | ☐ |
| 3 | CLICK ปุ่มยืนยัน | — | workspace editable; ประวัติมีเหตุผล | ☐ |

### TC-L05 — reopen หลัง DN ถูกห้าม
- group: Lifecycle negative · priority: P0 · trace: BR_PACK_LOCKED_BY_DN
- Setup: role=wh_lead · seed=pack shipped มี dn_ref · files=—
- Start: OPEN pack detail
- ผ่านเมื่อ: ไม่มี mutation

| 1 | VERIFY header actions | — | ไม่มีปุ่มแก้ไข/reopen/cancel | ☐ |
| 2 | VERIFY summary | — | เห็น DN ref และสถานะออกใบส่งของแล้ว | ☐ |

### TC-L06 — cancel reason/return queue
- group: Lifecycle · priority: P0 · trace: AT-12 / BR-PACK-12
- Setup: role=packer owner · seed=pack in_progress no DN · files=—
- Start: OPEN pack detail
- ผ่านเมื่อ: blank block; valid cancel returns source job

| 1 | CLICK ปุ่ม **ยกเลิก** | — | modal **ยกเลิกใบแพ็ค ...?** เปิด | ☐ |
| 2 | CLICK ปุ่ม **ยืนยันยกเลิก** โดยเหตุผลว่าง | — | toast **กรุณาระบุเหตุผล** | ☐ |
| 3 | TYPE `กล่องเสียหาย` → ช่อง **เหตุผล / หมายเหตุ** | — | แสดงค่า | ☐ |
| 4 | CLICK ปุ่ม **ยืนยันยกเลิก** | — | toast **ยกเลิกแล้ว — งานกลับเข้าคิว** | ☐ |
| 5 | OPEN `#/list` | — | งานต้นทางกลับแท็บคิว; ใบเดิม cancelled | ☐ |

### TC-L07 — DN mock boundary / shipped lock
- group: Lifecycle/lock · priority: P0 · trace: BR-PACK-11,14 / LOCK-03
- Setup: role=wh_lead · seed=pack packed; demo vs production environments identifiable · files=—
- Start: OPEN pack detail
- ผ่านเมื่อ: demo may show mock; production uses disabled/gated adapter only

| 1 | CLICK ปุ่ม **ออกใบส่งของ** ใน demo | — | toast ระบุว่าเป็น **mock ใบส่งของ** | ☐ |
| 2 | VERIFY production-like environment | — | action disabled/returns contract unavailable until OQ-DN-01 | ☐ |
| 3 | VERIFY shipped pack | — | all edit/cancel/reopen actions absent for all roles | ☐ |

### TC-D01 — BOXLABEL content/dimension
- group: Print · priority: P0 · trace: AT-13 / BR-PACK-13
- Setup: role=wh_lead · seed=closed carton with cold/free/pickup variants · files=—
- Start: OPEN pack detail
- ผ่านเมื่อ: label has required visible content and one page per carton

| 1 | CLICK แท็บ **ป้ายกล่อง·ใบแพ็ค** | — | เห็น label previews ตามจำนวนกล่อง | ☐ |
| 2 | CLICK ปุ่ม **พิมพ์ป้ายกล่อง** | — | print output 150×100 มม. แนวนอน; กล่อง n/N, refs, recipient, items, lot/expiry, weight, barcode/QR, signatures | ☐ |

### TC-D02 — PACKSLIP content/A4
- group: Print · priority: P0 · trace: AT-14 / BR-PACK-13
- Setup: role=wh_lead · seed=packed pack DS-B · files=—
- Start: OPEN pack print tab
- ผ่านเมื่อ: A4 ไม่แสดงราคา/VAT

| 1 | CLICK ปุ่ม **พิมพ์ใบแพ็ค** | — | preview/PDF A4 แนวตั้ง | ☐ |
| 2 | VERIFY เอกสาร | — | หัวบริษัท/meta/ผู้รับ/รายการ/กล่อง/qty/weight/summary/4 signatures ครบ และระบุไม่ใช่เอกสารภาษี | ☐ |

### TC-D03 — audit/reprint invalidation
- group: Audit · priority: P0 · trace: AT-15 / BR-PACK-10,15
- Setup: role=wh_lead · seed=carton closed→reopened→closed/reprinted · files=—
- Start: OPEN pack detail
- ผ่านเมื่อ: history chronological and old label invalid

| 1 | CLICK แท็บ **ประวัติ** | — | เห็น close, reopen reason, reclose, reprint แยก events | ☐ |
| 2 | CLICK แท็บ **ป้ายกล่อง·ใบแพ็ค** | — | ใช้ label version ใหม่; version เก่าไม่ใช่ valid output | ☐ |

### TC-U01 — wh_lead permissions/export
- group: Permission · priority: P0 · trace: permission matrix
- Setup: role=wh_lead · seed=own and others jobs/packs · files=—
- Start: OPEN `#/list`
- ผ่านเมื่อ: lead access/action set complete

| 1 | VERIFY queue/packs rows | — | เห็นทุกงานใน warehouse scope | ☐ |
| 2 | CLICK action Export CSV | — | export เริ่มและข้อมูลไม่ข้าม warehouse/tenant | ☐ |
| 3 | CLICK pack ของคนอื่น | — | lead เห็น edit/reopen/cancel/DN actions ตาม state | ☐ |

### TC-U02 — packer own vs other
- group: Permission · priority: P0 · trace: BR-PACK-14
- Setup: role=packer · seed=own active pack + other pack · files=—
- Start: OPEN `#/list`
- ผ่านเมื่อ: own editable, other read-only

| 1 | CLICK own pack | — | scan/carton/finish controls visible | ☐ |
| 2 | CLICK other pack | — | mutation controls absentหรือ toast **ใบนี้มอบหมายให้ ...** | ☐ |

### TC-U03 — viewer read-only
- group: Permission · priority: P0 · trace: BR-PACK-14
- Setup: role=viewer/Sales · seed=queue+packs · files=—
- Start: OPEN `#/list`
- ผ่านเมื่อ: view allowed, mutation denied

| 1 | CLICK queue row | — | details visible; no **เริ่มแพ็ค** | ☐ |
| 2 | CLICK pack row | — | tabs/details/print previewตามสิทธิ์; no edit/finish/cancel/DN | ☐ |

### TC-U04 — keyboard/Esc/responsive/permission revoke
- group: UX/security · priority: P1 · trace: AT-18,20 / EC-03 / LOCK-05
- Setup: role=packer then revoke role via fixture; viewport 1024×768 and 1280×800 · files=—
- Start: OPEN active pack
- ผ่านเมื่อ: interaction works and server rejects revoked mutation

| 1 | PRESS F3 | — | opens carton or shows **ปิดกล่องปัจจุบันก่อน (F2)** correctly | ☐ |
| 2 | CLICK cancel/custom modal then PRESS Esc | — | modal closes before drawer | ☐ |
| 3 | PRESS Esc อีกครั้ง | — | drawer closes | ☐ |
| 4 | VERIFY viewport 1024/1280 | — | no horizontal body scrollbar; controls remain reachable | ☐ |
| 5 | CLICK mutation after role revoked | — | action denied; no state/data change | ☐ |

### TC-X01 — idempotency/network replay `(ต้อง simulate)`
- group: Integration · priority: P0 · trace: AT-16 / EC-01
- Setup: role=packer · seed=eligible job · inject lost first response then resend same/different body · files=—
- Start: OPEN queue job
- ผ่านเมื่อ: one business result

| 1 | CLICK **เริ่มแพ็ค** while response is dropped | — | UI may remain pending/error but server creates at most one pack | ☐ |
| 2 | CLICK retry with same key/body | — | opens same PACK; no duplicate audit/create | ☐ |
| 3 | CLICK retry fixture with same key/different body | — | conflict shown; original pack unchanged | ☐ |

### TC-X02 — DN outage/retry `(ต้อง simulate)`
- group: Cross-module · priority: P0 · trace: XT-03 / BR-PACK-11
- Setup: role=wh_lead · seed=packed; DN adapter fixture fail then stable success · files=—
- Start: OPEN packed pack
- ผ่านเมื่อ: fail remains packed; success once

| 1 | CLICK **ออกใบส่งของ** with DN down | — | error/retry feedback; status remains packed, dn_ref empty | ☐ |
| 2 | CLICK retry after adapter restored | — | one stable dn_ref appears; status shipped | ☐ |
| 3 | CLICK/replay same request | — | same dn_ref; no duplicate DN | ☐ |

### TC-X03 — concurrent allocation `(ต้อง simulate)`
- group: Concurrency · priority: P0 · trace: EC-02/04 / ERR_STALE_DATA
- Setup: role=two packer sessions · seed=remaining 1 same line/pack/version · files=—
- Start: OPEN same pack in both sessions
- ผ่านเมื่อ: total allocation=1

| 1 | CLICK/submit add 1 nearly simultaneously in both sessions | — | one succeeds; other sees stale/conflict | ☐ |
| 2 | VERIFY refreshed quantities | — | packed=1, remaining=0, never 2 or negative | ☐ |

### TC-X04 — print renderer failure `(ต้อง simulate)`
- group: Fault · priority: P1 · trace: EC-07 / ERR_PRINT_FAILED
- Setup: role=wh_lead · seed=packed/closed; inject renderer 503 · files=—
- Start: OPEN print tab
- ผ่านเมื่อ: state unaffected and retry exists

| 1 | CLICK **พิมพ์ใบแพ็ค** | — | failure/retry feedback visible | ☐ |
| 2 | VERIFY pack/carton status | — | remains packed/closed; no reopen/cancel side effect | ☐ |

### TC-X05 — notification outage/dedupe `(ต้อง simulate)`
- group: Event · priority: P1 · trace: XT-04 / BR-PACK-16 / LOCK-04
- Setup: role=packer · seed=pack ready to finish; ENG-NOTIFY down then restored · files=—
- Start: OPEN pack detail
- ผ่านเมื่อ: business commits once and one notification is delivered eventually

| 1 | CLICK **ปิดงานแพ็ค** while notify down | — | toast **แพ็คเสร็จ — พร้อมออกใบส่งของ**; status packed | ☐ |
| 2 | WAIT จน outbox retry หลัง notify restored | — | exactly one `pack_done` notification for same event key | ☐ |

## วิธีที่ agent รัน (Run protocol)

1. Run each case independently from its Start route and stated seed/role.
2. Do not reuse state from a prior case unless fixture explicitly creates it.
3. For delta cases, record baseline values before action.
4. Mark `blocked` when required fault injection/backend/contract is unavailable; capture visible evidence.
5. Do not treat demo `mock` DN/Transfer behavior as production pass.

## Coverage Audit

| Category | covered / total |
|---|---:|
| Acceptance AT | 20 / 20 |
| Business rules | 16 / 16 |
| Edge cases | 10 / 10 |
| Named error groups | 15 / 15 |
| Important permission cells | 24 / 24 |
| Cross-module XT | 5 / 5 |
| Scope locks | 5 / 5 |
| States/UI/cross-cutting | 100% mapped |

- Manifest cross-check: ✅ 10/10 rows in FRD §0.12
- Skipped implementation assertions: Transfer production happy path and concrete DN schema — guarded OQ/out of current contract; negative/gating tests remain.

## Result Report (schema)

```json
{"feature_id":"F-WH-PACK","run_at":"<iso datetime>","results":[{"id":"TC-Q01","status":"pass|fail|blocked","failed_step":null,"evidence":"","note":""}],"summary":{"total":40,"pass":0,"fail":0,"blocked":0}}
```
