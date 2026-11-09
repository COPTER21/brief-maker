# BRD: แบบฟอร์มร้องขอดำเนินการด้าน IT (IT Request Form)

| Field | Value |
|---|---|
| BRD ID | BRD-TMP-001 (ชั่วคราว) |
| Feature | F-TMP-001 แบบฟอร์มร้องขอดำเนินการด้าน IT (รหัส feature ชั่วคราว — รอรหัสจริง) |
| BRD Type | New Feature (แบบ 2 · ดึงข้อมูลเดิม — ชื่อ/ตำแหน่งจาก HR · Employee) |
| Version | 1.0 |
| Status | **APPROVED (Prebrief Mode · Lane/unattended)** — DEC แทน Scope Lock จนมีใบเซ็นลูกค้า |
| Module | IT Support (Core Cube) — ใกล้เคียง FEATURE_REGISTRY "IT Support › Ticket (—)" |
| Customer form | FM-ITS-01 แบบฟอร์มร้องขอดำเนินการด้าน IT (IT Request Form) · ไม่มี Rev. บนกระดาษ |
| Request | REQ-TMP-001 (ชั่วคราว — รอเลขจริงจาก F186) |
| Input | PREBRIEF_REQ-TMP-001_v2 · FORM_SPEC.json (11 ช่อง) · DECISIONS.lock (15 DEC · พร้อมเริ่มทำ · AI-DEFAULT 11) · feature.html (html-generator v9.4 · audit FAIL 0) |
| Created / Updated | 2026-10-10 |

## Changelog
- v1.0 (2026-10-10): สร้างผ่าน brd-generator-full v2.3 Prebrief Mode (doc-master-pipeline ขั้น 7 · โหมดไม่เฝ้า)

---

## 1. Business Context
### 1.1 ปัญหา / โอกาส
พนักงานขออุปกรณ์/โปรแกรม/บริการ IT ด้วยแบบฟอร์มกระดาษ FM-ITS-01 (xlsx) — ลงนาม 3 ช่อง (ผู้ร้องขอ · ตรวจสอบโดย · ดำเนินการโดย) ส่งต่อด้วยมือ · ไม่มีเลขที่รันจริง (ช่อง "ITRS." เว้นว่าง) · ติดตามสถานะไม่ได้ว่าอนุมัติแล้ว/IT ทำเสร็จหรือยัง
### 1.2 เป้าหมาย
1. ขึ้นแบบฟอร์มเป็นเอกสารในระบบ ช่องตรงกระดาษ 1:1 · PDF Replica ลูกค้าจำแบบเดิมได้
2. ตรวจสอบ/อนุมัติตามสาย DOA กลาง (dynamic) แทนการเดินเอกสาร
3. ฝ่าย IT เห็นคิวคำขอที่อนุมัติแล้ว และบันทึก "ดำเนินการโดย" ให้ผู้ร้องขอเห็นผล
### 1.3 ตัวชี้วัด
ไม่มีใน input → **OQ-01** (ห้ามแต่งตัวเลข) · เสนอให้วัด: เวลาตั้งแต่ส่งถึงดำเนินการแล้ว · % คำขอที่ส่งมอบตามวันที่ต้องการ — ต้องเก็บ baseline ก่อน launch
### 1.4 ที่มา
แบบฟอร์มลูกค้า FM-ITS-01 (xlsx · ชื่อไฟล์ "แบบฟอร์มขอรับบริการด้านเทคโนโลยีสารสนเทศ" · หัวฟอร์ม "แบบฟอร์มร้องขอดำเนินการด้าน IT") → FORM_SPEC 11 ช่อง + ☐ ประเภทงาน 6 · gate 10 หมวดตอบเองตาม unattended-policy (AI-DEFAULT ทุกหมวด)

## 2. Scope
### 2.1 In Scope
- รายการคำขอ (ค้นหา · กรองสถานะ/ประเภทงาน · แท็บ ทั้งหมด/รอฉันพิจารณา/คำขอของฉัน · CSV) · สร้าง/แก้ร่าง wizard 3 ขั้น · ดูรายละเอียด 4 แท็บ (รายละเอียด › PDF › ลายเซ็น/อนุมัติ › ประวัติ)
- ส่งอนุมัติ DOA (ค่าเริ่ม 1 ขั้น "ตรวจสอบโดย" · เลือกคนต่อขั้น) · อนุมัติ / ไม่อนุมัติ→กลับร่าง · ยกเลิก (เหตุผลบังคับ)
- ฝ่าย IT บันทึก "ดำเนินการแล้ว" (ช่อง ดำเนินการโดย) หลังอนุมัติครบ
- แนบไฟล์ · PDF FM-ITS-01 Replica ทุกสถานะ · เลขที่ ITRS จาก ENG-DOC-NUM
### 2.2 Out of Scope
- สร้างใบขอซื้อ/PR จากคำขอ "ขอซื้ออุปกรณ์" · สร้าง User/E-Mail อัตโนมัติ · ทะเบียนทรัพย์สิน IT · มอบหมายงานรายคน/SLA ของฝ่าย IT · ทำซ้ำเอกสาร (DEC-11) · ประกาศ (DEC-11) · ส่งต่อระบบอื่น (DEC-02)
### 2.3 Assumptions
- ชื่อ-นามสกุล/ตำแหน่ง/ผู้บังคับบัญชามีใน HR · Employee + ผังองค์กร · มี role สำหรับเจ้าหน้าที่ฝ่าย IT (role-it-officer — ยังไม่อยู่ใน DOA contract → OQ-03)
### 2.4 Scope Lock (ชั่วคราว = DECISIONS.lock · ยังไม่มีใบเซ็น → OQ-02)
| DEC | หมวด | มติ | ที่มา |
|---|---|---|---|
| DEC-01 | G1 | อนุมัติแล้วไม่เปลี่ยนค่าในระบบ | AI-DEFAULT |
| DEC-02 | G1 | ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง) | AI-DEFAULT |
| DEC-03 | G2 | DOA dynamic · ค่าเริ่ม 1 ขั้น role-line-manager ("ตรวจสอบโดย") · ไม่มีวงเงิน | AI-DEFAULT |
| DEC-04 | G3 | คำนวณอัตโนมัติ · เกินเกณฑ์ = เตือน · วันที่ส่งมอบ ≥ วันที่ขอ (เตือน) · อื่นๆ ต้องระบุ · ประเภทงาน ≥ 1 (เลือกได้หลายข้อ) | AI-DEFAULT |
| DEC-05 | G4 | ไม่มีรายการซ้ำบนกระดาษ (ไม่เกี่ยว) | AI-DEFAULT |
| DEC-06 | G5 | ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง | AI-DEFAULT |
| DEC-07 | G6 | ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA · ข้อความ "ส่ง/พิจารณาในระบบ" ไม่ใช้ภาพ | AI-DEFAULT |
| DEC-08 | G7 | ไม่อนุมัติ = กลับร่างเลขเดิม · ยกเลิก: เจ้าของ + admin role · ร่าง/รออนุมัติ · เหตุผลบังคับ | AI-DEFAULT |
| DEC-09 | G8 | เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin role (ฝ่าย IT) เห็นทั้งหมด | AI-DEFAULT |
| DEC-10 | G9 | ออกเลขตอนบันทึกครั้งแรก · รหัส ITRS | AI-DEFAULT |
| DEC-11 | G10 | แนบไฟล์ ✓ · CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗ | AI-DEFAULT |
| DEC-12 | VALID | Rev. ไม่มีบนกระดาษ → Rev.00 รอลูกค้ายืนยัน | FORM_SPEC |
| DEC-13 | VALID | แก้คำสะกด ตําแหน่ง → ตำแหน่ง | FORM_SPEC |
| DEC-14 | VALID | วันที่ต้องการส่งมอบ ≥ วันที่ขอ (เตือน) | FORM_SPEC |
| DEC-15 | VALID | ติ๊ก อื่นๆ = ต้องระบุข้อความ | FORM_SPEC |

## 3. Roles & Permissions (COSO)
| Role | COSO | ทำอะไร |
|---|---|---|
| พนักงาน (ผู้ร้องขอ) | Maker | สร้าง/แก้ร่างของตน · ส่ง · ยกเลิกของตน (ร่าง/รออนุมัติ) |
| role-line-manager ("ตรวจสอบโดย") | Approver | ขั้น DOA: อนุมัติ/ไม่อนุมัติ |
| role-it-officer (เจ้าหน้าที่ IT · admin role ฝ่าย IT) | Executor + admin view | เห็นทุกใบ · บันทึก "ดำเนินการแล้ว" · ยกเลิกได้ (ร่าง/รออนุมัติ) [AI-DEFAULT · role ยังไม่อยู่ใน contract] |

| Action | Maker | L-Mgr | IT |
|---|:-:|:-:|:-:|
| ดูใบ | ของตน | หลังส่ง (อยู่ในสาย) | ทั้งหมด |
| สร้าง/แก้ร่าง | ✓ ของตน | – | – |
| อนุมัติ/ไม่อนุมัติ | – | ขั้นที่ตนเป็นผู้พิจารณา | – |
| ดำเนินการแล้ว | – | – | ✓ (สถานะรอดำเนินการ) |
| ยกเลิก | ✓ ของตน | – | ✓ |
SoD: ผู้ร้องขออนุมัติใบตัวเองไม่ได้ (BR-DOA-04) · ผู้ดำเนินการ ≠ ผู้อนุมัติ (บทบาทแยก)

## 4. User Journey
### 4.1 Happy Path
| # | Step | Maker | Checker/Approver | System |
|---|---|---|---|---|
| 1 | กด "สร้างคำขอ" → กรอกเรื่อง · ติ๊กประเภทงาน · วันที่/สถานที่ส่งมอบ · รายละเอียด · เหตุผล · Spec | ผู้ร้องขอ | – | ดึงชื่อ/ตำแหน่ง/ผู้ตรวจสอบเริ่มต้น |
| 2 | แนบไฟล์ (ถ้ามี) → ตรวจสอบและยืนยัน → บันทึก | ผู้ร้องขอ | – | ออกเลข ITRS (ENG-DOC-NUM) |
| 3 | ส่งอนุมัติ เลือกผู้พิจารณาต่อขั้น | ผู้ร้องขอ | – | resolve DOA + freeze approval_chain |
| 4 | ตรวจสอบ → อนุมัติ | – | role-line-manager | ครบทุกขั้น → รอดำเนินการ · แจ้งฝ่าย IT (itrs_ready_for_it) |
| 5 | ทำงานเสร็จ → กด "ดำเนินการแล้ว" | – | role-it-officer (Executor) | บันทึก performed_by/at · แจ้งผู้ร้องขอ (itrs_completed) · เก็บ PDF |
### 4.2 Alternative
- ไม่อนุมัติ → กลับร่างเลขเดิม + เหตุผล → ผู้ร้องขอแก้ ส่งใหม่ (resolve สายใหม่)
- ยกเลิก (ร่าง/รออนุมัติ) โดยเจ้าของหรือฝ่าย IT · เหตุผลบังคับ · ถ้ารออนุมัติ แจ้งผู้พิจารณา (itrs_cancelled)
- วันที่ต้องการส่งมอบก่อนวันที่ขอ → เตือน ส่งได้
```mermaid
flowchart LR
A[ร่าง] -->|ส่ง| B[รออนุมัติ]
B -->|อนุมัติครบ| C[รอดำเนินการ]
C -->|IT ดำเนินการแล้ว| D[ดำเนินการแล้ว]
B -->|ไม่อนุมัติ| A
A & B -->|ยกเลิก| X[ยกเลิก]
```

## 5. Data (จาก FORM_SPEC — ป้ายตามกระดาษ)
### 5.1 it_request (header)
| ช่องบนกระดาษ | field | ชนิด | ที่มา | บังคับ |
|---|---|---|---|:-:|
| ITRS. (เลขที่) | doc_no | text | auto ENG-DOC-NUM | ✓ |
| วันที่ | req_date | date | auto | ✓ |
| ตำแหน่ง | position_snapshot | text | system HR · Employee (อ่านอย่างเดียว) | ✓ |
| ชื่อ-นามสกุล | employee_id → name_snapshot | ref | system HR · Employee | ✓ |
| วันที่ต้องการส่งมอบ | due_date | date | user | ✓ |
| สถานที่ส่งมอบ | delivery_location | text(200) | user | ✓ |
| เรื่องที่ต้องการ | subject | text(200) | user | ✓ |
| ประเภทงาน ☐×6 | job_types | enum[] (buy_device · user_email · install_software · install_accessory · internet_wifi · other) | user | ✓ ≥1 |
| อื่นๆ ….. | job_type_other | text(200) | user | เมื่อติ๊ก อื่นๆ |
| รายละเอียดการร้องขอ | detail | text | user | ✓ |
| เหตุผล วัตถุประสงค์ หรือ ความจำเป็น | reason | text | user | ✓ |
| มาตรฐาน หรือ Spec ที่ต้องการ | spec | text | user | – |
| ดำเนินการโดย | performed_by · performed_at · done_note | ref/datetime/text | system (IT) | หลังอนุมัติ |
| + DOA fields | approval_status · doa_ref · approval_chain (jsonb snapshot) · approved_by · approved_at | | DOA | |
| + returned_reason · returned_by · returned_at · header_snapshot | | | DEC-08 · DOCCFG | |
### 5.2 attachments → Document Center (ไฟล์ระดับใบ)

## 6. User Stories
| ID | Story | AC หลัก |
|---|---|---|
| S-01 | ผู้ร้องขอสร้างคำขอดำเนินการด้าน IT | ช่องบังคับครบตาม VR · ชื่อ/ตำแหน่งระบบใส่ · บันทึกได้เลข ITRS |
| S-02 | ผู้ร้องขอเลือกประเภทงานได้หลายข้อ | ต้องเลือก ≥1 · ติ๊ก อื่นๆ ต้องระบุข้อความ · PDF ติ๊กตรงที่เลือก |
| S-03 | ผู้ร้องขอแนบไฟล์ประกอบ | ไฟล์ pdf/doc/xls/รูป ≤20MB · ผิดชนิดแจ้งเตือน |
| S-04 | ผู้ร้องขอส่งอนุมัติ | slot ต่อขั้นตาม DOA · ค่าเริ่มจากผัง · ผู้ร้องขอไม่อยู่ในรายชื่อ · บังคับเลือกครบ |
| S-05 | ผู้ตรวจสอบอนุมัติคำขอ | ปุ่มเฉพาะผู้พิจารณาขั้นปัจจุบัน · ครบทุกขั้น = รอดำเนินการ |
| S-06 | ผู้ตรวจสอบไม่อนุมัติคำขอ | เหตุผลบังคับ · กลับร่างเลขเดิม · แบนเนอร์เหตุผลในร่าง |
| S-07 | เจ้าหน้าที่ IT บันทึกดำเนินการแล้ว | เฉพาะ role-it-officer · สถานะรอดำเนินการ · ช่อง ดำเนินการโดย ใน PDF มีชื่อ+เวลา |
| S-08 | ผู้ร้องขอยกเลิกคำขอ | ร่าง/รออนุมัติ · เหตุผลบังคับ |
| S-09 | พิมพ์ PDF FM-ITS-01 | ทุกสถานะ 1 หน้า A4 · ลายเซ็น = ผู้ร้องขอ + 1 ช่องต่อขั้น DOA + ดำเนินการโดย |
| S-10 | ฝ่าย IT ดูคำขอทุกใบ | กรองสถานะ/ประเภทงาน · ส่งออก CSV |

## 7. Status & Lifecycle
| จาก | Action | ไป | ใคร |
|---|---|---|---|
| — | บันทึกครั้งแรก | draft | Maker |
| draft | ส่ง | pending (ขั้น 1) | Maker |
| pending | อนุมัติขั้น n<N | pending (ขั้น n+1) | ผู้พิจารณาขั้น n |
| pending | อนุมัติขั้น N | approved (รอดำเนินการ) | ขั้น N |
| pending | ไม่อนุมัติ | draft (เลขเดิม · returned_*) | ผู้พิจารณาขั้นปัจจุบัน |
| approved | ดำเนินการแล้ว | done | role-it-officer |
| draft / pending | ยกเลิก | cancelled | Maker / role-it-officer |
approved/done = ล็อกแก้ไข · ไม่มียกเลิกหลังอนุมัติ (DEC-08)

## 8. Business Rules + Validation
| ID | Rule | Tag | Type |
|---|---|:-:|---|
| BR-01 | ประเภทงานเลือกได้หลายข้อ อย่างน้อย 1 ข้อ | FIXED | Validation (DEC-04) [AI-DEFAULT] |
| BR-02 | ติ๊ก อื่นๆ ต้องระบุข้อความ | FIXED | Validation (DEC-15) |
| BR-03 | วันที่ต้องการส่งมอบก่อนวันที่ขอ = เตือน ไม่บล็อก | CONFIGURABLE | Policy (DEC-04/14) [AI-DEFAULT] |
| BR-04 | สายอนุมัติ resolve จาก DOA ตอนส่ง แล้ว freeze · จำนวนขั้นตาม DOA กลาง | FIXED | DOA (BR-DOA-02 · DEC-03) |
| BR-05 | ไม่อนุมัติ → draft เลขเดิม · resolve ใหม่ตอนส่งรอบถัดไป | FIXED | DEC-08 (BR-DOA-03) [AI-DEFAULT] |
| BR-06 | ออกเลขตอนบันทึกครั้งแรก · รหัส ITRS · no-gap ✗ | CONFIGURABLE | DOCCFG (DEC-10) |
| BR-07 | ร่างเห็นเฉพาะเจ้าของ (+ admin IT) | FIXED | Visibility #109 (DEC-09) |
| BR-08 | ช่องลงชื่อ PDF = ผู้ร้องขอ + 1 ช่องต่อขั้น DOA + ดำเนินการโดย · แถวละ ≤4 | FIXED (จำนวน = DOA) | DEC-07 |
| BR-09 | "ดำเนินการแล้ว" ทำได้เมื่อ approved และเป็น role-it-officer เท่านั้น | FIXED | Control [AI-DEFAULT] |
| BR-10 | อนุมัติแล้วไม่เปลี่ยนค่าในระบบ · ไม่ส่งต่อระบบอื่น | FIXED | DEC-01/02 |
| BR-11 | ป้ายช่องตามกระดาษ 1:1 · แก้สะกด "ตำแหน่ง" | FIXED | DEC-06/13 |
| BR-12 | Rev. ของแบบพิมพ์อ่านจาก F-DOCCFG print_config (ค่าเริ่ม Rev.00) | CONFIGURABLE | DEC-12 |

| VR | ช่อง | เงื่อนไข | ข้อความ |
|---|---|---|---|
| VR-01 | subject | required | ระบุเรื่องที่ต้องการ |
| VR-02 | job_types | ≥1 | เลือกประเภทงานอย่างน้อย 1 ข้อ |
| VR-03 | job_type_other | required เมื่อ other | ระบุงานอื่นๆ |
| VR-04 | due_date | required | เลือกวันที่ต้องการส่งมอบ |
| VR-05 | delivery_location | required | ระบุสถานที่ส่งมอบ |
| VR-06 | detail | required | ระบุรายละเอียดการร้องขอ |
| VR-07 | reason | required | ระบุเหตุผล วัตถุประสงค์ หรือความจำเป็น |
| VR-08 | slot ผู้พิจารณา | ทุกขั้นต้องเลือก · ≠ ผู้ร้องขอ | กรุณาเลือกผู้พิจารณา |
| VR-09 | เหตุผล ไม่อนุมัติ/ยกเลิก | required | กรุณาระบุเหตุผล |

### 8.5 ระดับความยืดหยุ่น
BR-03 → Admin Panel (นโยบายคำขอ IT) · BR-04 → DOA กลาง · BR-06/12 → F-DOCCFG

## 9. Edge Cases
| EC | กรณี | ผล |
|---|---|---|
| EC-01 | วันที่ต้องการส่งมอบก่อนวันที่ขอ (DEC-14) | เตือนในฟอร์ม/ตรวจสอบ · ส่งได้ · view แสดงป้าย "ก่อนวันที่ขอ" |
| EC-02 | ติ๊ก อื่นๆ แต่ไม่ระบุ (DEC-15) | บล็อกถัดไป · ช่อง invalid |
| EC-03 | ข้อความรายละเอียดยาวเกิน 4 บรรทัดบนกระดาษ | PDF เพิ่มบรรทัด + dense ยัง 1 หน้า (ทดสอบ 7/4/6 บรรทัด) |
| EC-04 | DOA ตั้ง 6 ขั้น | ช่องลงชื่อ 8 ช่อง 2 แถว (4+4) · 1 หน้า |
| EC-05 | ผู้ร้องขอเป็นผู้บังคับบัญชาสูงสุด (ไม่มี mgr) | slot ว่าง ต้องเลือกเอง |
| EC-06 | แก้ DOA ระหว่างใบรออนุมัติ | ใบเดิมใช้สาย snapshot |
| EC-07 | ส่ง/อนุมัติชนกัน (stale) | 409 → toast รีเฟรช สถานะไม่เปลี่ยน |
| EC-08 | แบบเอกสารปิดใช้ (F-DOCCFG) | ปุ่มสร้าง disabled |
| EC-09 | ผู้อนุมัติเปิด route ใบร่างของคนอื่น | ไม่เปิด (ไม่มีสิทธิ์) |
| EC-10 | ไม่มี Rev. บนกระดาษ (DEC-12) | footer แสดง Rev.00 จาก print_config |

## 10. Value Stream & Downstream Impact
Positioning: IT Service Request — คำขอ (feature นี้) → อนุมัติ → ฝ่าย IT ดำเนินการ
| ปลายทาง | ข้อมูล | Trigger | หมายเหตุ |
|---|---|---|---|
| ฝ่าย IT (คิวงาน) | คำขอที่อนุมัติ | approved | ENG-NOTIFY itrs_ready_for_it — ภายใน feature |
| ผู้ร้องขอ | ผลดำเนินการ | done | ENG-NOTIFY itrs_completed |
| PR / จัดซื้อ (ขอซื้ออุปกรณ์) | รายการที่ต้องซื้อ | approved | **ปิดรอบนี้ (DEC-02)** — ประกาศ event `itrs.approved` ใน FRD ไม่ยิง |
| IT Support › Ticket | งานบริการ | approved | ปิดรอบนี้ → OQ-05 |
| F-DOCCFG / ENG-DOC-STORE | PDF snapshot | approved_final | |
แล้วไงต่อ: ทุกแถวที่ปิดรอบนี้ = ฝ่าย IT/จัดซื้อทำนอกระบบตามเดิม (ไม่มีข้อมูลหาย เพราะเอกสารเก็บครบในระบบ)

## 11. Delivery
Phase 1 = ทุกอย่างใน §2.1 · Phase 2 (เสนอ) = เชื่อม PR (ขอซื้ออุปกรณ์) + IT Ticket (มอบหมาย/SLA)

## 12. Dev Summary "ใบสั่ง"
- Config: DOA entry F-TMP-001 (doa_type itrs) · doc_type ITRS (F-DOCCFG · print_config FM-ITS-01) · role-it-officer
- Declaration: DOA_BRIEF · NTF_BRIEF · DOCCFG_BRIEF · MDOC_BRIEF (ฉบับจริงหลัง FRD)
- Screen Inventory: P-01 รายการ `#/it-request` · P-02 สร้าง/แก้ `#/it-request/create` · `#/it-request/edit/:id` (drawer wide 3 ขั้น) · P-03 ดู `#/it-request/view/:id` (drawer 4 แท็บ) · M-01..06 modal ส่ง/อนุมัติ/ไม่อนุมัติ/ยกเลิก/ดำเนินการแล้ว/ทิ้งข้อมูล
- UI Signals: เอกสาร + พิมพ์ + ลายเซ็น = ใช่ · archetype Q-form

## 13. Open Questions
| OQ | คำถาม | เจ้าของ | Block? |
|---|---|---|---|
| OQ-01 | ตัวชี้วัดความสำเร็จ + baseline | ลูกค้า | ไม่ |
| OQ-02 | ลูกค้าเซ็นยืนยัน DEC-01..11 (AI-DEFAULT ทุกข้อ) — โดยเฉพาะ 1 ขั้น "ตรวจสอบโดย" = ผู้บังคับบัญชา · ประเภทงานเลือกหลายข้อ · ไม่อนุมัติกลับร่าง | ทีม BA → ลูกค้า | ก่อน UAT |
| OQ-03 | role-it-officer (เจ้าหน้าที่ IT / admin ฝ่าย IT) ไม่อยู่ใน DOA roles contract — ต้องเพิ่มที่ DOA กลาง/RBAC | ทีม BA + พี่เบิร์ด | ก่อน wire |
| OQ-04 | "ตรวจสอบโดย" บนกระดาษ คือผู้บังคับบัญชาหรือหัวหน้าฝ่าย IT? (ตั้งค่าเริ่มเป็น role-line-manager) | ลูกค้า | ก่อน UAT |
| OQ-05 | เชื่อม IT Support › Ticket / PR เมื่อไร · รหัส feature จริงแทน F-TMP-001 | ทีม BA | ไม่ |
| OQ-06 | Rev. ของแบบฟอร์ม (กระดาษไม่มี) · function_code taxonomy ของ MDOC | ลูกค้า / ทีม BA | ก่อน register |

## 14. Security & Compliance
Preset: Standard Internal · PII: ชื่อผู้ร้องขอ (pdpa) — ข้อมูลตัวอย่างใน prototype/แบบพิมพ์เป็นชื่อสมมติ · ห้ามกรอกรหัสผ่านในคำขอ (คำขอ User/E-Mail ส่งรหัสนอกเอกสาร) · Audit append-only ทุก action · SoD ผู้ร้องขอ≠ผู้อนุมัติ · ไฟล์แนบตาม file_policy Document Center

## 15. Health Check / Monitoring
SLA: ไม่กำหนดรอบนี้ (WARNING → OQ-01) · KPI เสนอ: คำขอรออนุมัติเกิน N วัน · คำขอรอดำเนินการเกินวันที่ต้องการส่งมอบ · Widget: คิวงาน IT ตามประเภทงาน

## Appendix — Screen List
P-01 `#/it-request` · P-02 `#/it-request/create` · `#/it-request/edit/:id` · P-03 `#/it-request/view/:id`

---

## AI Review Report (brd-generator-full v2.3 · Prebrief Mode)
| ข้อ | ผล |
|---|---|
| C01 Business objective | ✅ §1.2 |
| C02 Roles ครบ | ✅ §3 |
| C03–C04 Scope in/out | ✅ §2 |
| C05 Story ไม่มี "และ" | ✅ S-01..S-10 |
| C06–C09 AC ≥2 · Journey · Status · Data | ✅ |
| C10 Rule มี Tag | ✅ BR-01..12 |
| C11–C13 VR · Edge cases ครบหมวด | ✅ VR-01..09 · EC-01..10 |
| C14–C17 Flexibility · Delivery · Registry (WARN: feature ใหม่ ไม่มีรหัส → OQ-05) | ✅ / ⚠️ C16 ยอมรับใน Prebrief Mode |
| C18 WARNING มีแผน | ✅ OQ-01..06 |
| C19 ใบสั่ง | ✅ §12 |
| C20 Scope Lock = DEC ครบ 15 + OQ-02 รอใบเซ็น | ✅ |
| C21 Value stream ตอบ "แล้วไงต่อ" | ✅ §10 |
| C22 ตัวชี้วัด | ✅ (Prebrief Mode: ไม่มีใน input → OQ-01 ห้ามแต่ง) |
| C23 marker | ✅ [AI-DEFAULT] ที่ BR |
| PE01 COSO ทุก step · PE02 SoD · PE03 Security · PE04 SLA/KPI (WARNING→OQ) · PE05 cross-section | ✅ |

**สถานะ: ✅ APPROVED** → พร้อมเข้า frd-generator-v6
