# Full Review Plan — F-TMP-008

## แบบฟอร์มชุดเอกสารส่งมอบงาน (สำหรับฝ่ายบริหารการลงทุนจัดเก็บ)

> จุดประสงค์: ตรวจเก็บตกบนระบบ Production หลัง UI และ UAT ผ่านแล้ว โดยเน้น business logic, workflow, permission, data integrity และ integration
>
> Baseline ตัดสินว่าถูก/ผิด: FRD v1.0 เป็นหลัก โดยเฉพาะ `03_LOGIC`, `05_RULES`, `06_TESTS`, `07_LOCKED_DECISIONS` หาก business sense พบเรื่องนอก FRD ให้บันทึกเป็น **Observation / คำถาม BA** ไม่ตัดสินเป็น defect จนกว่า PM/BA ยืนยัน

## 1. คำตอบสั้น ๆ ว่าควรตรวจอย่างไร

อย่าเริ่มจากการกดทุกปุ่มแบบสุ่ม ให้ตรวจเป็น 5 ชั้นตามลำดับ:

1. **ยืนยัน configuration ก่อน** — HOI เปิดใช้งาน, สาย DOA จริง, HandoverConfig และสิทธิ์ของผู้ทดสอบต้องรู้ค่าแน่นอน
2. **เล่น happy path ให้จบหนึ่งใบ** — สร้าง → บันทึกร่าง → ส่ง → ตรวจสอบ → รับทราบ → PDF/notification
3. **เล่น business-negative cases** — จงใจกรอกข้อมูลขัดกัน แล้วดูว่าทั้ง UI และ server บล็อกจริง
4. **สลับ role ตรวจ permission/SoD** — คนผิดต้องมองไม่เห็นหรือทำไม่ได้ แม้พยายามเปิด URL ตรง/ส่ง request ซ้ำ
5. **ตรวจผลข้างเคียงหลัง transaction** — เลขเอกสาร, audit, PDF snapshot, notification, CSV และข้อมูลหลัง refresh/login ใหม่

การที่ toast ขึ้นว่า “สำเร็จ” ยังไม่ถือว่าผ่าน ต้อง refresh แล้วตรวจสถานะ/ข้อมูล/ประวัติ/ผู้รับแจ้งเตือนอีกครั้งเสมอ

## 2. เรื่องที่ต้องถาม PM/BA หรือ Admin ก่อนเริ่ม

FRD ระบุรายการต่อไปนี้เป็น AI-default, pending หรือ open question จึงต้องยืนยันค่าบน Production ก่อน มิฉะนั้นผลทดสอบอาจตีความผิด:

| # | ต้องยืนยัน | ค่าใน FRD | เหตุผล |
|---|---|---|---|
| C-01 | สาย DOA Production และจำนวนขั้น | ค่าเริ่ม 2 ขั้น: `role-line-manager` → `role-mgr-bu`; DOA brief ยัง `wire_status: pending` | ถ้าสายจริงไม่ตรง ห้ามสรุปว่า defect จนทราบ config ที่อนุมัติแล้ว |
| C-02 | role ผู้รับทราบฝ่ายพัฒนาธุรกิจ | `role-mgr-bu` เป็นค่าชั่วคราว | เสี่ยงส่งงานผิดคนหรือไม่มีคนรับงาน |
| C-03 | HandoverConfig ที่เปิดใช้จริง | ผลรับมอบ 3 ค่า, ได้รับ/ไม่ได้รับ, ความครบถ้วน 3 ค่า | ระบบต้องอ่าน config ไม่ hardcode และค่าที่เลิกใช้ต้องไม่หลุดมา |
| C-04 | รหัสเอกสาร HOI และสถานะ doc type | HOI, ออกเลขตอนบันทึกครั้งแรก, reset รายปี | ป้องกันเลขชน/ออกเลขจาก logic ภายใน feature |
| C-05 | การเชื่อม F185 / Master Document | MDOC ระบุ taxonomy ว่างและ DOA pending | Production แล้วควรทราบว่าปิด WARN สองข้อนี้หรือยัง |
| C-06 | ใบ FM-BDM-08 ต้องผูก FM-BDM-07/โครงการหรือไม่ | Out of scope / OQ-05 | เป็น business gap ที่สำคัญ แต่ไม่ใช่ defect ตาม FRD ปัจจุบัน |
| C-07 | กำหนดการติดตามเป็นวันที่หรือข้อความ | FRD ใช้วันที่, OQ-06 ยังเปิด | ตรวจตามระบบได้ แต่ต้องยืนยันว่าตรงการใช้งานจริง |
| C-08 | AI-default 11 ข้อได้รับการ sign-off หรือยัง | OQ-02 ระบุให้ลูกค้ายืนยันก่อน UAT | หากยังไม่มีหลักฐาน ให้ลงเป็น governance risk |

หาก C-01–C-05 ตอบไม่ได้ ให้ตรวจต่อได้เฉพาะ behavior ที่เห็น แต่ให้สถานะผลเป็น `Blocked — configuration baseline not confirmed` ไม่ควรลงนามว่า logic ถูกครบ

## 3. ชุดผู้ใช้และข้อมูลที่ต้องเตรียม

### 3.1 ผู้ใช้ขั้นต่ำ

| Persona | สิทธิ์ | ใช้ตรวจ |
|---|---|---|
| U1 Maker A | ผู้จัดทำ ฝ่ายบริหารการลงทุน | สร้าง/แก้/ส่ง/ยกเลิกใบตนเอง |
| U2 Maker B | ผู้จัดทำอีกคน | cross-owner permission |
| U3 Checker | ผู้พิจารณาขั้น 1 จริง | ตรวจสอบ/ไม่ผ่าน |
| U4 Acknowledger | ผู้พิจารณาขั้นสุดท้ายจริง | รับทราบ/ไม่รับทราบ |
| U5 Admin | admin ฝ่ายบริหารการลงทุน | เห็นทั้งหมด/ยกเลิกได้แต่ห้ามแก้หรือตัดสินแทน |
| U6 Outsider | ไม่อยู่ในสายและไม่ใช่ admin | ตรวจ data leakage/URL ตรง |

ห้ามใช้ account เดียวสลับ role ถ้าระบบจริงผูกหลายสิทธิ์ในคนเดียว เพราะจะพิสูจน์ segregation of duties ไม่ได้

### 3.2 ข้อมูลทดสอบ

- โครงการชื่อเฉพาะรอบ เช่น `PROD-REVIEW-HOI-20261124-A` เพื่อค้นหาและ cleanup/อ้างหลักฐานได้
- เอกสารครบ 2 แถว, เอกสารไม่ครบ 1 แถว และชุด 13–24 แถว
- ไฟล์แนบชื่อเฉพาะ: PDF ปกติ, ชื่อไทย/เว้นวรรค, ไฟล์ขนาดใกล้ limit ที่ระบบกำหนด
- วันที่รับมอบวันนี้/ย้อนหลัง, วันที่อนาคต, due date ก่อน/เท่ากับ/หลังวันรับมอบ
- เวลา `10:30`, `00:00`, `23:59`, `1030`, `25:00`, ค่าว่าง
- เปิด Network log หรือหลักฐาน request/response เฉพาะกรณีที่ทีมอนุญาต โดยปกปิด token และ PII

## 4. ลำดับรันทดสอบ

ให้ทำตามลำดับ P0 → P1 → P2 หาก P0 fail ให้หยุด transaction ที่อาจทำข้อมูลเสีย/ส่งคนจริง และแจ้งทีมทันที

### P0 — ความเสี่ยงสูงสุด / ต้องตรวจทุกข้อ

#### R-01 Configuration และหน้าเริ่มต้น

- [ ] เปิด route `#/handover-investment` ด้วย U1: เห็นรายการตามสิทธิ์และสร้างบันทึกได้เมื่อ HOI active
- [ ] ตรวจค่าตัวเลือกผลรับมอบ/ได้รับแล้ว/ความครบถ้วนว่าตรง HandoverConfig ที่ยืนยันไว้
- [ ] ตรวจว่า U6 ไม่เห็นเมนูหรือข้อมูลของ feature เกินสิทธิ์
- [ ] ถ้ามี environment สำหรับปิด HOI: เมื่อ doc type inactive ต้องสร้างไม่ได้และได้ `DOC_TYPE_INACTIVE`; ห้ามทดสอบโดยปิด config บน Production โดยไม่ได้รับอนุญาต

Expected หลัก: ไม่มีค่าตัวเลือกที่ hardcode เพิ่มเอง, ไม่มีข้อมูลข้าม tenant/ข้ามสิทธิ์, ไม่มีการออกเลขก่อนบันทึกครั้งแรก

หลักฐาน: screenshot ตัวเลือกและ config reference/build/time ที่ทดสอบ

#### R-02 Happy path — เอกสารครบถ้วน

1. U1 สร้างใบ กรอก 6 ช่องบังคับและอย่างน้อย 2 แถว โดยทุกแถว `ได้รับ + ครบถ้วน`
2. เลือกผล `รับมอบครบถ้วน`; จำนวนค้างส่งต้องเป็น 0
3. บันทึกร่างครั้งแรก; จดเลข HOI และ refresh/login ใหม่
4. แก้ร่างหนึ่งครั้ง; เลขต้องเดิมและข้อมูลต้อง persist
5. ส่งอนุมัติ; modal ต้องมีจำนวน slot เท่ากับ DOA ที่ resolve จริง และ U1 ต้องไม่อยู่ในรายชื่อผู้พิจารณา
6. U3 ตรวจสอบแล้ว; ใบต้องไปขั้นถัดไป ไม่ใช่ approved ทันที
7. U4 รับทราบผล; ใบเป็น `รับทราบแล้ว/approved`, ล็อกแก้และยกเลิก
8. เปิด PDF และประวัติ; ตรวจเลข/ข้อมูล/ชื่อ/เวลา/คำตัดสิน/จำนวนแถวลงชื่อ

Expected หลัก:

- เลข HOI ออกครั้งเดียวจาก engine กลาง รูปแบบตาม Document Configuration และไม่เปลี่ยนเมื่อแก้/ส่ง
- approval เรียง sequential; มีเพียง current assignee ที่ตัดสินได้
- approved แล้วแก้ไข/ยกเลิกไม่ได้ทั้งจากปุ่มและ direct request
- PDF final ถูกเก็บเป็น `approved_final`; จำนวนลายเซ็น = ผู้จัดทำ 1 + จำนวนขั้น DOA
- กรณีครบถ้วนไม่ยิง `hoi_acknowledged_open_items`

#### R-03 Happy path — มีเอกสารค้าง

1. U1 สร้างใบมี 3 แถว: ผ่าน 2, ไม่ได้รับหรือไม่ครบถ้วน 1
2. แถวที่ไม่ผ่านต้องกรอกประเด็น, ผู้รับผิดชอบ, due date
3. เลือก `รับมอบแบบมีเงื่อนไข` และกรอกประเด็นค้าง/วันติดตาม
4. ส่งผ่าน approval จนครบ

Expected หลัก:

- open items = 1 ทั้งหน้า list, detail, toast และ payload notification
- หลังรับทราบ U1 ได้ in-app event `hoi_acknowledged_open_items` เพียงครั้งเดียว
- ข้อความมีเลขใบ, count=1 และวันติดตามตรงใบ
- U3/U4 ไม่ควรได้ event นี้แทน requester
- PDF/CSV แสดงผลรับมอบและข้อมูลค้างตรงกับข้อมูลที่บันทึก

#### R-04 Business validation matrix

ทดสอบแต่ละกรณีแยกกันและต้องตรวจหลัง refresh ว่า record/status ไม่ถูกเปลี่ยนหากระบบบล็อก:

| ID | ข้อมูลที่จงใจผิด | Expected ตาม FRD |
|---|---|---|
| V-01 | ไม่กรอก project/sender/receiver/package/result | บล็อกและชี้ช่องที่ขาด |
| V-02 | ไม่มีแถวตรวจรับ หรือแถวไม่มีชื่อ/received/completeness | บล็อก; ต้องเหลืออย่างน้อย 1 แถว |
| V-03 | วันที่รับมอบอนาคต | บล็อก |
| V-04 | เวลา `1030`, `25:00`, ค่าว่าง | บล็อกพร้อมข้อความรูปแบบ 10:30 |
| V-05 | `ไม่ได้รับ + ครบถ้วน` | บล็อกเพราะข้อมูลขัดกัน |
| V-06 | แถวไม่ผ่านแต่ขาด issue | บล็อกเฉพาะช่อง issue |
| V-07 | แถวไม่ผ่านแต่ขาด fix owner | บล็อกเฉพาะช่องผู้รับผิดชอบ |
| V-08 | แถวไม่ผ่านแต่ขาด due date | บล็อกเฉพาะ due date |
| V-09 | due date ก่อนวันรับมอบ | บล็อก |
| V-10 | follow-up date ก่อนวันรับมอบ | บล็อก |
| V-11 | มีแถวไม่ผ่านแต่เลือก `รับมอบครบถ้วน` | บล็อกที่ผลรับมอบ |
| V-12 | ผลไม่ใช่ครบถ้วนแต่ไม่กรอก open issues | บล็อก |
| V-13 | เปลี่ยนวันรับมอบให้หลัง due/follow-up ที่กรอกไว้แล้ว | revalidate และบล็อก ไม่ปล่อยข้อมูลเก่าที่ผิด |
| V-14 | เลือก `ยังไม่รับมอบ` พร้อมข้อมูลค้างครบ | ส่งได้ ไม่ควรถูกบล็อกเพราะชื่อสถานะ |

ข้อสำคัญ: ถ้า UI บล็อกอย่างเดียว ให้ทีมทดสอบ API หรือ request tampering เพื่อยืนยันว่า server ใช้กฎเดียวกัน โดยเฉพาะ V-05–V-13 และการคำนวณ `open_items`

#### R-05 Permission และ segregation of duties

| ID | Actor / การกระทำ | Expected |
|---|---|---|
| P-01 | U3/U4 เปิด URL ร่างของ U1 ก่อนส่ง | 404/ไม่เห็นใบ ไม่เปิดเผยว่ามี record |
| P-02 | U2 เปิดร่างของ U1 | ไม่เห็น/404 |
| P-03 | U6 เปิด pending/approved ด้วย URL ตรง | ไม่เห็น/404 |
| P-04 | U4 พยายามตัดสินก่อน U3 | ไม่มีปุ่มและ server ตอบ `NOT_CURRENT_APPROVER` |
| P-05 | U3 พยายามตัดสินซ้ำหลังผ่านขั้น 1 | ถูกปฏิเสธ สถานะไม่เปลี่ยน |
| P-06 | U1 เลือกตัวเองเป็น approver | ไม่มีใน list และ server บล็อก `SELF_APPROVAL` |
| P-07 | U1 แก้ใบ pending/approved | ไม่มีปุ่ม; direct request ถูกปฏิเสธ |
| P-08 | U5 admin แก้เนื้อหา/อนุมัติแทน | ทำไม่ได้; admin มีสิทธิ์ดูและยกเลิกเท่านั้น |
| P-09 | U6/U3 ยกเลิกใบ | ถูกปฏิเสธ `NOT_OWNER` |
| P-10 | U1/U5 ยกเลิกใบ approved | ถูกปฏิเสธ `NOT_CANCELLABLE` |
| P-11 | ตรวจรายการของทุก persona | draft เห็นเฉพาะ owner+admin; หลังส่งคนใน chain เห็น; คนนอกไม่เห็น |

หาก UI ซ่อนปุ่มแต่ API ยังทำได้ ให้จัดเป็น Critical/High ตามผลกระทบ ไม่ใช่ UI issue

#### R-06 Reject / return to draft

- [ ] U3 กดไม่ผ่านโดยไม่ใส่เหตุผล → บล็อก
- [ ] U3 ไม่ผ่านพร้อมเหตุผล → ใบกลับ draft, เลขเดิม, owner แก้ได้
- [ ] approval chain เดิมต้องอยู่ใน audit แต่ chain active ถูกล้าง
- [ ] U3/U4 ต้องไม่เห็นร่างหลังถูกตีกลับ ตาม visibility rule
- [ ] U1 ส่งใหม่ → resolve DOA ใหม่; ห้ามนำ assignee เก่ามาใช้เงียบ ๆ ถ้า config เปลี่ยน
- [ ] ทำซ้ำกับ U4 `ไม่รับทราบ` หลัง U3 ผ่านแล้ว → กลับ draft เช่นกัน
- [ ] เหตุผล/ผู้ตีกลับ/เวลาต้องตรงและ append-only

#### R-07 Cancel flow

- [ ] U1 ยกเลิกร่างโดยไม่ใส่เหตุผล → บล็อก; ใส่เหตุผลแล้ว cancelled
- [ ] U1 ยกเลิก pending → current approver ได้ `hoi_cancelled` เพียงครั้งเดียว
- [ ] U5 admin ยกเลิก pending → ได้ผลเดียวกันและ audit ระบุ admin จริง
- [ ] pending step ต้องกลายเป็น skipped; ห้ามค้างใน My Approval
- [ ] cancelled แล้วแก้/ส่ง/ตัดสิน/ยกเลิกซ้ำไม่ได้
- [ ] ยกเลิกร่างไม่ควรแจ้ง approver เพราะยังไม่มี current step

#### R-08 Concurrent / duplicate action

ใช้สอง browser session เปิดใบและ version เดียวกัน:

- [ ] U1 เปิดแก้ร่างสองหน้าต่าง; หน้าต่างแรก save สำเร็จ หน้าต่างที่สอง save ต้องได้ `STALE` และไม่ทับข้อมูล
- [ ] U3 เปิดตัดสินสองหน้าต่าง; action แรกสำเร็จ action ที่สองต้องไม่อนุมัติซ้ำ/ไม่ยิง event ซ้ำ
- [ ] double click ส่ง/อนุมัติ/ยกเลิก หรือ retry request ด้วย Idempotency-Key เดิม ต้องเกิด transaction เดียว
- [ ] network หลุดหลังคลิกแล้ว retry: ตรวจสถานะจาก server ก่อนคลิกซ้ำ
- [ ] เลข HOI ห้ามซ้ำแม้สร้างพร้อมกันสองคน

### P1 — Integration และความถูกต้องของเอกสาร

#### R-09 DOA snapshot และ dynamic chain

- [ ] ตอนส่ง ให้บันทึก `doa_ref`, role, assignee และ decision words ครบทุกขั้น
- [ ] หลังส่ง หาก admin เปลี่ยน DOA กลาง ใบที่ pending ต้องใช้ chain snapshot เดิม
- [ ] ใบใหม่หลังเปลี่ยน config ต้องใช้ chain ใหม่
- [ ] ถ้าทำได้ใน test environment ให้ตรวจ 1, 2 และ 6 ขั้น: PDF มี 2, 3 และ 7 แถวลงชื่อตามลำดับ
- [ ] role-line-manager ใช้คำ `ตรวจสอบแล้ว/ไม่ผ่านการตรวจสอบ`; role-mgr-bu ใช้ `รับทราบผลการรับมอบ/ไม่รับทราบ`
- [ ] chain 6 ขั้นต้องยังเป็น PDF 2 หน้าและบล็อกลายเซ็นไม่ถูกตัดกลาง

ห้ามเปลี่ยน DOA Production เพียงเพื่อทดสอบโดยไม่ได้รับอนุญาต; ใช้หลักฐานจากใบจริง/config history หรือ environment ทดสอบแทน

#### R-10 PDF และ snapshot

ตรวจ PDF ในสถานะ draft, pending, approved, cancelled อย่างน้อยสถานะละหนึ่งใบ:

- [ ] ทุกสถานะเป็น 2 หน้า, มี `หน้า 1/2` และ `หน้า 2/2`, ไม่มีหน้าที่ 3
- [ ] หน้า 1 มีหัว/ข้อมูลรับมอบ/แถวตรวจรับ; หน้า 2 มีส่วนต่อ/ประเด็นค้าง/ลงชื่อ/ประวัติแบบ
- [ ] อย่างน้อย 12 แถว; เมื่อ 13–24 แถวต้องต่อหน้า 2 และหัวตารางซ้ำ
- [ ] วันที่เป็น พ.ศ. และเวลา `HH:MM น.` ตรงข้อมูล
- [ ] ข้อมูล/จำนวนค้าง/ผลรับมอบตรง detail ทุกจุด รวมภาษาไทยยาวและชื่อบุคคล
- [ ] header บริษัท/โลโก้/กลุ่มบริษัทเป็น snapshot ณ ตอนออกเลข; เปลี่ยน Company Master ภายหลังไม่ควรเปลี่ยนใบเก่า
- [ ] ประวัติการแก้ไขบน PDF คือ revision ของแบบฟอร์ม ไม่ใช่ audit ต่อใบ
- [ ] approved PDF ที่เก็บใน Document Store ต้องตรง final view/download และไม่เปลี่ยนภายหลัง
- [ ] ไม่มีภาพลายเซ็น; แสดงชื่อ/ตำแหน่ง/คำตัดสิน/วันที่จากระบบ

#### R-11 เลขเอกสารและ Document Configuration

- [ ] เลขออกตอน create/save ครั้งแรก ไม่ใช่ตอนเปิดหน้า create
- [ ] save/edit/reject/resubmit ไม่ออกเลขใหม่
- [ ] cancel แล้วเลขไม่ถูก reuse
- [ ] สร้างพร้อมกันหลายใบไม่ชนกัน
- [ ] format และปีตรง config Production; ถ้าข้ามปีให้ตรวจ reset ด้วยหลักฐาน config/test environment ไม่แก้เวลาระบบ Production
- [ ] เมื่อ HOI inactive ต้องไม่สร้างใบใหม่ แต่ใบเดิมยังอ่านได้ตาม policy
- [ ] F185 แสดงแบบ HOI, route และ version ที่ใช้งานจริง; WARN taxonomy/DOA มีสถานะปิดตามที่ทีมยืนยัน

#### R-12 Attachment

- [ ] แนบ/เปิด/ดาวน์โหลด/ลบไฟล์ใน draft ได้ตามสิทธิ์
- [ ] ชื่อไทย, เว้นวรรค และไฟล์มากกว่า 1 ไฟล์ไม่เสียชื่อ/สลับไฟล์
- [ ] U2/U6 เดา URL ไฟล์แนบแล้วเปิดไม่ได้
- [ ] pending/approved/cancelled ต้องไม่แก้ชุดไฟล์แนบผ่าน direct request หาก record ถูกล็อก
- [ ] upload fail ต้องไม่ผูก attachment ค้างหรือทำให้ใบถูกบันทึกครึ่งเดียว
- [ ] scan/type/size policy ของ Document Center ทำงานตามมาตรฐานองค์กร (นอก FRD ให้บันทึกเป็น observation หากไม่มี baseline)

#### R-13 CSV / filter / list consistency

- [ ] filter สถานะ/ผลรับมอบ/ฝ่าย/ค้นหาให้ได้ subset ที่ทราบจำนวน
- [ ] CSV ต้องตรง filter และสิทธิ์ของผู้ export; ห้ามมี draft/PII ของคนอื่นหลุด
- [ ] open items, owner, date, result, status ตรงกับ detail
- [ ] ภาษาไทย/เลข HOI เปิดใน spreadsheet ได้ไม่เพี้ยน
- [ ] pagination/page size ไม่ทำให้ CSV export แค่หน้าปัจจุบัน เว้นแต่ spec ระบุเช่นนั้น
- [ ] badge `เปิดอยู่` และ `รอฉันพิจารณา` เปลี่ยนถูกหลัง submit/decide/reject/cancel และหลัง refresh

#### R-14 Notification / My Approval

- [ ] submit ทำให้ current approver เห็นใบใน My Approval ผ่าน DOA engine
- [ ] ผ่านขั้นหนึ่งแล้ว งานหายจาก U3 และไป U4
- [ ] reject/cancel/approve แล้วงานค้างถูกนำออกจาก queue
- [ ] ระบบไม่ยิง `doa_pending/doa_result` ซ้ำเองนอก DOA engine
- [ ] `hoi_acknowledged_open_items` ยิงเฉพาะ final approved ที่มี open item หรือ result ไม่ครบถ้วน
- [ ] `hoi_cancelled` ยิงเฉพาะ pending→cancelled ไป current approver
- [ ] retry/double click ไม่สร้าง notification ซ้ำ
- [ ] link จาก notification เปิดใบได้เฉพาะผู้มีสิทธิ์; คนอื่นได้ 404

#### R-15 Audit และ data integrity

- [ ] ทุก write มี actor/time/action; save, submit, approve, reject, resubmit, cancel ครบลำดับ
- [ ] audit append-only ไม่มีรายการเก่าหายหลัง reject/resubmit
- [ ] snapshot ชื่อ/ตำแหน่ง/ฝ่าย/approver ยังคงเดิมเมื่อ Employee/Org master เปลี่ยน
- [ ] server คำนวณ open_items ใหม่ ไม่เชื่อค่าจาก browser
- [ ] ลบ/เรียงแถวแล้ว seq ต่อเนื่องและข้อมูลไม่สลับ
- [ ] ข้อมูลข้าม tenant ไม่พบทั้ง list, URL ตรง, CSV, PDF และ attachment
- [ ] ไม่มี hard delete; cancelled ยังคง audit/หลักฐานตาม retention policy

### P2 — Business sense / exploratory review

รายการนี้ไม่ได้ถูกล็อกเป็น requirement ทุกข้อ จึงบันทึกเป็น Observation หรือถาม BA ก่อนเปิด Bug:

| ID | คำถามที่ควรลองคิด/ลองเล่น | ความเสี่ยงธุรกิจ |
|---|---|---|
| B-01 | FM-BDM-08 เชื่อมกับ FM-BDM-07 หรือโครงการอย่างไร ถ้าชื่อโครงการพิมพ์ไม่ตรงกัน | จับคู่ใบส่งมอบสองฝั่งไม่ได้/พิสูจน์ chain of custody ยาก |
| B-02 | หลัง approved แต่ยังมีเอกสารค้าง ใครติดตามจนปิด และปิดค้างที่ไหน | ระบบแจ้งครั้งเดียวแต่ไม่มี closure loop/dashboard |
| B-03 | due date เลยกำหนดแล้วมี reminder/escalation หรือไม่ | เอกสารค้างถูกลืม |
| B-04 | sender/receiver/fix owner เป็น free text ได้ ค้นหา/รายงาน/เปลี่ยนชื่อพนักงานอย่างไร | duplicate name และ accountability ไม่ชัด |
| B-05 | `ยังไม่รับมอบ` แต่อนุมัติจนเป็น `รับทราบแล้ว` ทำให้ผู้ใช้อ่านผิดว่าได้รับมอบแล้วหรือไม่ | workflow status กับ business result สื่อความคนละเรื่อง |
| B-06 | ผู้จัดทำแก้เนื้อหาหลัง reject แล้ว approver เห็น diff จากรอบก่อนหรือไม่ | ไม่รู้ว่าแก้อะไร อาจรับทราบข้อมูลที่เปลี่ยนมาก |
| B-07 | ไฟล์แนบเป็นหลักฐานสำคัญ ควร freeze/hash/version ตอนส่งหรือ approved หรือไม่ | เปลี่ยนหลักฐานภายหลัง |
| B-08 | approved PDF และ attachment ต้องเก็บนานเท่าไร/ใคร export ได้ | compliance/retention/PDPA |
| B-09 | ถ้า approver ลาออกหรือ role ว่างระหว่าง pending มี delegation/escalation อย่างไร | เอกสารค้างถาวร |
| B-10 | ถ้า HandoverConfig เปลี่ยน label/value ใบเก่าแสดง snapshot หรือแปลด้วย config ใหม่ | ประวัติใบเก่าเปลี่ยนความหมาย |
| B-11 | CSV มี PII และข้อมูลภายใน ควรมี permission/audit/watermark หรือไม่ | data exfiltration |
| B-12 | ชื่อโครงการ/ข้อความยาว/อักขระพิเศษ/สูตร spreadsheet (`=`, `+`, `-`, `@`) | PDF ล้นและ CSV injection |
| B-13 | timezone ของ received/approved/audit ตรง Asia/Bangkok หรือไม่ | หลักฐานเวลาคลาดวัน โดยเฉพาะใกล้เที่ยงคืน |
| B-14 | ผู้ใช้เปิดใบเก่านานแล้ว config/permission เปลี่ยนก่อน submit จะ revalidate หรือไม่ | ใช้ assignee/option ที่หมดอายุ |

## 5. Smoke test ที่ควรรันหลังทุก deployment

ถ้าเวลามีน้อย ให้รันอย่างน้อย 12 ข้อนี้:

1. สร้างใบครบถ้วนและบันทึกได้เลข HOI
2. มีแถวไม่ผ่านแล้วเลือกครบถ้วนต้องถูกบล็อก
3. แถวไม่ผ่านต้องบังคับ issue/owner/due date
4. ส่งแล้ว approval chain ตรง DOA Production และห้าม self-approve
5. คนที่ไม่ใช่ current approver ตัดสินไม่ได้
6. reject กลับ draft เลขเดิมและ audit ไม่หาย
7. approve ครบแล้วล็อกแก้/ยกเลิก
8. approved ที่มีค้างส่งแจ้ง maker ครั้งเดียว
9. cancel pending แจ้ง current approver และเอาออกจาก queue
10. PDF 2 หน้า ข้อมูลตรง จำนวน sign row ตรง DOA
11. U6 เปิด URL/attachment/CSV ของใบไม่ได้
12. double action/หน้าต่างชนกันไม่สร้างเลข การอนุมัติ หรือ notification ซ้ำ

## 6. วิธีบันทึกผลให้รายงานได้จริง

หนึ่ง scenario ต้องมีอย่างน้อย:

- Test ID และ FRD trace เช่น `V-11 → BR-02 / VR-07 / AC-07`
- ผู้ใช้/role, environment/build, วันเวลา, เลข HOI
- ข้อมูลที่กรอก (mask PII)
- Expected ตาม FRD และ Actual ที่เห็นจริง
- ผล `Pass / Fail / Blocked / Not Run`
- หลักฐาน screenshot หรือ clip; สำหรับ permission/concurrency ควรมี response code หรือ audit เพิ่ม

ตัวอย่างบันทึก defect:

```text
BUG-HOI-01 — U4 อนุมัติก่อน U3 ได้
Trace: FRD 05 §5.2, §5.3; TC-D03
Precondition: HOI-2569-xxxx อยู่ pending ขั้น 1
Steps: login U4 → เปิด URL ใบ → ส่ง decide=approve
Expected: ไม่มีปุ่มและ server ตอบ 403 NOT_CURRENT_APPROVER
Actual: ตอบ success และใบไป approved
Impact: ข้ามสายอนุมัติ / SoD
Severity: Critical
Evidence: screenshot..., response..., audit...
```

## 7. หลักการตัดสิน Bug กับ Observation

- **Bug**: ขัด FRD/locked decision/config ที่ได้รับการยืนยัน และทำซ้ำได้
- **Blocked**: config, role, test data หรือสิทธิ์ที่จำเป็นยังไม่พร้อม
- **Observation / Improvement**: ระบบทำตาม FRD แต่เสี่ยงหรือใช้งานจริงไม่ดี เช่น ไม่มี closure loop ของเอกสารค้าง
- **Requirement gap**: business ต้องการสิ่งที่ FRD ระบุ out of scope หรือ open question เช่นผูก FM-BDM-07; ส่งให้ BA ตัดสินก่อน ไม่กล่าวหาว่า dev ทำผิด

แนว severity:

- Critical: ข้ามสิทธิ์/ข้าม approval, ข้อมูลข้าม tenant, ข้อมูลหาย/เสีย
- High: status, open-items, เลขเอกสาร, PDF final หรือผู้รับแจ้งเตือนผิด; transaction ซ้ำ
- Medium: ผิด FRD แต่มีทางเลี่ยง, audit ขาด, filter/CSV ผิดบางกรณี
- Low: ข้อความ/ตำแหน่ง/ความเรียบร้อยที่ไม่กระทบ logic (UI layout รอบนี้ไม่ใช่ focus)

## 8. Exit criteria ก่อนบอกว่า “review logic ครบแล้ว”

- [ ] C-01–C-05 มี baseline ที่ยืนยันได้
- [ ] P0 ทุกข้อ Pass หรือมี defect ที่เปิดและระบุ owner/แผน retest
- [ ] AC-01..14 และ permission deny TC-D01..D07 มีผลจริง ไม่ใช่อ้าง UAT เดิม
- [ ] server-side validation/permission พิสูจน์อย่างน้อยกรณีความเสี่ยงสูง
- [ ] happy path ครบถ้วนและมีค้างส่งจบทั้ง flow
- [ ] reject, resubmit, cancel, stale/idempotency ผ่าน
- [ ] PDF final, document number, Document Store, DOA, notification และ attachment มีหลักฐาน
- [ ] business observations B-01..B-14 ส่งให้ PM/BA ตัดสินและไม่ปนเป็น bug
- [ ] ระบุสิ่งที่ไม่ได้ตรวจชัดเจน เช่น cross-tenant, เปลี่ยน DOA, ปิด doc type, year reset
- [ ] สรุปผลด้วยจำนวน Pass/Fail/Blocked/Not Run และห้ามใช้คำว่า “ผ่านทั้งหมด” หากยังมี Not Run

## 9. แหล่งอ้างอิงที่ใช้จัดทำแผนนี้

- FRD `00_OVERVIEW`, `01_UI`, `02_API`, `03_LOGIC`, `04_DB`, `05_RULES`, `06_TESTS`, `07_LOCKED_DECISIONS`
- DOA_BRIEF, DOCCFG_BRIEF, NTF_BRIEF, MDOC_BRIEF
- AI test cases 30 เคสและ QA audit ใน feature context

หมายเหตุ: DevPack ระบุ `e2e_standard` ไม่มี report และ MDOC/DOA เคยมีสถานะ pending/WARN จึงควรตรวจ wiring บน Production จากหลักฐานจริง แม้ tester จะทดสอบ UI/UAT ผ่านแล้ว
