# 05_RULES — F-TMP-003

## §5.1 Business Rules
| BR | กฎ | ระดับ | ที่มา |
|---|---|---|---|
| BR-01 | ช่องบังคับ (ส่ง): วันที่ · คำนำหน้า · ชื่อ · โทรศัพท์ · บริษัท/หน่วยงาน · พนักงานที่ติดต่อ · วัตถุประสงค์ | FIXED | DEC-06 |
| BR-02 | host.full_name = พนักงานที่ติดต่อ · ฝ่าย/ผู้บังคับบัญชา snapshot จากผังองค์กร (อ่านอย่างเดียว) | FIXED | DEC-12 · DEC-04 [AI-DEFAULT] |
| BR-03 | ชื่อบริษัททุกจุด = header_snapshot.company.name_th — ห้าม hardcode | CONFIGURABLE (Organization) | DEC-04 · DEC-13 |
| BR-04 | สายอนุมัติจาก DOA กลาง · ค่าเริ่ม 1 ขั้น role-line-manager ของ host · ไม่มีวงเงิน · ห้าม fix จำนวนขั้น | CONFIGURABLE (DOA กลาง) [AI-DEFAULT] | DEC-03 |
| BR-05 | host ไม่มีผู้บังคับบัญชา → บล็อกส่ง (HOST_NO_MANAGER) | FIXED | DEC-03 · OQ-02 |
| BR-06 | ผู้บันทึก/host พิจารณาใบตัวเองไม่ได้ | FIXED | BR-DOA-04 |
| BR-07 | ไม่อนุมัติ → ความเห็นบังคับ · กลับเป็นร่างเลขเดิม | FIXED [AI-DEFAULT] | DEC-08 · DEC-14 |
| BR-08 | sign_date < request_date → เตือน · request_date < วันนี้ → เตือน (ไม่บล็อก) | CONFIGURABLE [AI-DEFAULT] | DEC-15 · DEC-04 |
| BR-09 | สิทธิ์เห็นตาม §5.3 | FIXED [AI-DEFAULT] | DEC-09 |
| BR-10 | เลข VAR จาก ENG-DOC-NUM ตอนบันทึกครั้งแรก · ตรวจ F-DOCCFG เปิดใช้ก่อน | FIXED | DEC-10 |
| BR-11 | ยกเลิก: owner/host/role-mgr-hr · status draft/pending · เหตุผลบังคับ | CONFIGURABLE [AI-DEFAULT] | DEC-08 |
| BR-12 | แนบไฟล์ ✓ (pdf/doc/xls/รูป ≤20MB) · CSV ✓ ไม่มีโทรศัพท์ · ทำซ้ำ ✗ · ประกาศ ✗ | FIXED [AI-DEFAULT] | DEC-11 |
### BR-DOA (มาตรฐาน DOA กลาง)
- BR-DOA-01 สายมาจาก DOA entry ของ F-TMP-003 เท่านั้น · BR-DOA-02 resolve ตอนส่งแล้ว freeze ลง approval_chain · BR-DOA-03 ไม่อนุมัติ = กลับร่าง (on_reject: back_to_draft ตาม DEC-08 — ไม่ใช่จบใบ) · BR-DOA-04 ห้ามพิจารณาใบตัวเอง · BR-DOA-05 sequential ทีละขั้น
- ช่องลงชื่อในแบบพิมพ์ = ผู้ขอ + 1 ช่องต่อขั้น (DEC-07) · แถวละ ≤4

## §5.2 State Machine
| จาก | action | ไป | ใคร |
|---|---|---|---|
| (ใหม่) | บันทึก | draft | พนักงาน / HR |
| draft | แก้ไข | draft | owner |
| draft | ส่งขออนุมัติ | pending (หรือ approved ถ้า DOA 0 ขั้น) | owner |
| pending | อนุมัติ (ขั้นสุดท้าย) | approved | assignee ขั้นปัจจุบัน |
| pending | อนุมัติ (ยังมีขั้น) | pending (ขั้นถัดไป) | assignee ขั้นปัจจุบัน |
| pending | ไม่อนุมัติ | draft (เลขเดิม) | assignee ขั้นปัจจุบัน |
| draft / pending | ยกเลิก | cancelled | owner / host / role-mgr-hr |
- approved · cancelled = ปลายทาง (ยกเลิกหลังอนุมัติ → OQ-04)

## §5.3 Permission Matrix (G8 · DEC-09)
| action | owner | host | ผู้อนุมัติ (ขั้นใน chain) | role-mgr-hr | อื่น |
|---|---|---|---|---|---|
| เห็นร่าง | ✓ | ✓ | ✗ | ✓ | ✗ (404) |
| เห็นหลังส่ง | ✓ | ✓ | ✓ | ✓ | ✗ (404) |
| แก้ร่าง | ✓ | ✗ | ✗ | ✗ (ถ้าไม่ใช่ผู้บันทึก) | ✗ |
| ส่ง | ✓ | ✗ | ✗ | ✗ | ✗ |
| อนุมัติ/ไม่อนุมัติ | ✗ | ✗ | ✓ ขั้นปัจจุบัน | ✗ (ถ้าไม่ใช่ assignee) | ✗ |
| ยกเลิก | ✓ | ✓ | ✗ | ✓ | ✗ |
| CSV | ใบที่เห็น | ใบที่เห็น | ใบที่เห็น | ทั้งหมด | — |

## §5.4 Validation
| VR | ช่อง | กฎ | ข้อความ |
|---|---|---|---|
| VR-01 | visitor.phone | ตัวเลข/ขีด/ช่องว่าง · 9–10 หลัก | กรุณากรอกหมายเลขโทรศัพท์ 9–10 หลัก |
| VR-02 | visit.request_date | บังคับ | กรุณาเลือกวันที่ |
| VR-03 | visitor.title | บังคับ ∈ {นาง, นางสาว, นาย} | กรุณาเลือกคำนำหน้า |
| VR-04 | visitor.full_name · visitor.company | บังคับ | กรุณากรอกชื่อผู้มาติดต่อ / ชื่อบริษัท / หน่วยงาน |
| VR-05 | host.employee_id | บังคับ · ต้องมี line_manager (DEC-12 · BR-05) | กรุณาเลือกพนักงานที่ติดต่อ / ไม่มีผู้บังคับบัญชาต้นสังกัด |
| VR-06 | visit.purpose | บังคับ ≤190 | กรุณาระบุวัตถุประสงค์ |
| VR-07 | approval.comment | บังคับเมื่อไม่อนุมัติ (DEC-14) | กรุณาระบุเหตุผล |
| VR-08 | visitor.sign_date | ≥ request_date (เตือน · DEC-15) | วันที่ลงนามก่อนวันที่เข้าพื้นที่ |
- DEC-13 (ชื่อบริษัทค่าเดียว) → BR-03 · DEC-12 → VR-05/BR-02

## §5.5 Edge Cases
| EC | กรณี | ผล | อ้าง |
|---|---|---|---|
| EC-01 | host = กรรมการผู้จัดการ (ไม่มีผู้บังคับบัญชา) | บล็อก HOST_NO_MANAGER | BR-05 |
| EC-02 | โทรศัพท์ไม่ครบ/มีตัวอักษร | บล็อก VR-01 | VR-01 |
| EC-03 | sign_date ก่อน request_date | เตือน ส่งได้ | VR-08 |
| EC-04 | ไม่อนุมัติไม่ใส่เหตุผล | บล็อก VR-07 | DEC-14 |
| EC-05 | ไม่อนุมัติแล้วแก้ส่งใหม่ | เลขเดิม · chain resolve ใหม่ · audit ครบ | DEC-08 |
| EC-06 | DOA กลางตั้ง 6 ขั้น | PDF 7 ช่อง 2 แถว (4+3) dense · modal 6 slot | DEC-03 · DEC-07 |
| EC-07 | ผู้บังคับบัญชาเปิด URL ร่าง | 404 | BR-09 |
| EC-08 | ยกเลิกระหว่าง pending | ขั้น pending = skipped · var_cancelled | BR-11 |
| EC-09 | F-DOCCFG ปิด VAR | 409 DOC_TYPE_INACTIVE · ปุ่มสร้าง disabled | BR-10 |
| EC-10 | วัตถุประสงค์ยาว | PDF 2 บรรทัด · ≤190 | VR-06 |
| EC-11 | แก้พร้อมกัน/API ล้ม | 409 STALE_VERSION / toast · สถานะไม่เปลี่ยน | — |

## §5.6 Notification
| event | trigger | ผู้รับ |
|---|---|---|
| var_cancelled | pending → cancelled | ผู้อนุมัติขั้นปัจจุบัน + ผู้สร้าง |
| doa_pending / doa_result | DOA engine | (ไม่ประกาศซ้ำ) |
