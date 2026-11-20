# 05_RULES — F-TMP-001

## §5.1 Business Rules
| BR | กติกา | อ้าง |
|---|---|---|
| BR-01 | ช่องบังคับครบก่อนบันทึก: ชื่อโครงการ · ที่มา · ประเภท · ผู้รับผิดชอบหลัก · วันที่เริ่มต้น/เป้าหมาย · ระดับความสำคัญ/สถานะ · ปัญหา · วัตถุประสงค์ · ขอบเขต · ผลลัพธ์ | FORM_SPEC · DEC-07 |
| BR-02 | วันที่เป้าหมาย ≥ วันที่เริ่มต้น (บล็อก) | DEC-04 · DEC-13 |
| BR-03 | แผนงาน ≥ 1 แถว · ไม่จำกัด · PDF ≥ 6 แถว · ทุกแถวมีกิจกรรม ผู้รับผิดชอบ วันเริ่มต้น วันครบกำหนด สถานะ · วันครบกำหนด ≥ วันเริ่มต้น | DEC-05 · DEC-14 |
| BR-04 | เลข PJI ออกตอนบันทึกครั้งแรกจาก ENG-DOC-NUM · เช็คเปิดใช้ที่ F-DOCCFG | DEC-11 |
| BR-05 | สาย DOA resolve ตอนส่งแล้ว freeze · ผู้จัดทำพิจารณาใบตัวเองไม่ได้ (BR-DOA-04) | DEC-03 |
| BR-06 | อนุมัติเรียงขั้น · ครบ = approved + ประวัติการแก้ไข 1 ฉบับ + pji_owner_assigned | DEC-03 · DEC-06 |
| BR-07 | ส่งกลับแก้ไข/ไม่อนุมัติ = กลับร่างเลขเดิม (BR-DOA-03) · เหตุผลบังคับ · ยกเลิก: owner/admin · draft/pending · เหตุผลบังคับ | DEC-09 |
| BR-08 | PDF แถวลงชื่อ = ผู้จัดทำ + 1 ต่อขั้น DOA (ไม่ fix) · คำตัดสินตาม role · 2 หน้าทุกสถานะ · ข้อความ "พิจารณาในระบบ" ไม่ใช้ภาพ | DEC-08 |
| BR-09 | ไม่เปลี่ยนค่าในระบบ ไม่ส่งต่อ · แนบไฟล์ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗ | DEC-01 · DEC-02 · DEC-12 |

## §5.2 State Machine
| จาก | action | ไป | ใคร |
|---|---|---|---|
| — | create | draft | owner |
| draft | update | draft | owner |
| draft | submit | pending (ขั้น 1) | owner |
| pending | approve (ไม่ใช่ขั้นสุดท้าย) | pending (ขั้นถัดไป) | assignee ขั้นปัจจุบัน |
| pending | approve (ขั้นสุดท้าย) | approved | assignee ขั้นปัจจุบัน |
| pending | reject | draft | assignee ขั้นปัจจุบัน |
| draft / pending | cancel | cancelled | owner · admin_role |

## §5.3 Permission Matrix
| action | owner | ผู้พิจารณาขั้นปัจจุบัน | อยู่ในสาย (ไม่ใช่ขั้นปัจจุบัน) | admin_role | อื่น |
|---|---|---|---|---|---|
| ดูร่าง | ✓ (ของตัวเอง) | ✗ ไม่เห็นร่างของคนอื่น | ✗ | ✓ | ✗ |
| ดูหลังส่ง | ✓ | ✓ | ✓ | ✓ | ✗ |
| แก้ร่าง / ส่ง | ✓ | ✗ | ✗ | ✗ | ✗ |
| อนุมัติ / ส่งกลับ | ✗ | ✓ | ✗ (403) | ✗ | ✗ |
| ยกเลิก | ✓ | ✗ | ✗ | ✓ | ✗ |
| CSV | ✓ (ที่เห็น) | ✓ | ✓ | ✓ | ✗ |

## §5.4 Validation
| VR | ช่อง | กฎ | ข้อความ |
|---|---|---|---|
| VR-01 | ช่องบังคับ header | ไม่ว่าง | กรุณากรอก{ป้าย} |
| VR-02 | target_date | ≥ start_date (DEC-13) | วันที่เป้าหมายต้องไม่ก่อนวันที่เริ่มต้น |
| VR-03 | plan[] | ≥ 1 แถว · ช่องบังคับครบ | กรอกกิจกรรม ผู้รับผิดชอบ วันเริ่มต้น และวันครบกำหนดให้ครบทุกแถว |
| VR-04 | plan[].due_date | ≥ plan[].start_date (DEC-14) | วันครบกำหนดต้องไม่ก่อนวันเริ่มต้น |
| VR-05 | submit.assignees | ครบทุกขั้น · ≠ ผู้จัดทำ | กรุณาเลือกผู้พิจารณา |

## §5.5 Edge Cases
| EC | กรณี | ผล |
|---|---|---|
| EC-01 | วันที่เป้าหมายก่อนวันที่เริ่มต้น | VR-02 บล็อก |
| EC-02 | แผนงาน > 6 แถว / > 14 แถว | หน้าจอไม่จำกัด · PDF หน้า 2 ครบทุกแถว · > 14 = dense |
| EC-03 | DOA 6 ขั้น | PDF 7 แถวลงชื่อ · .signs-block ไม่ตัดข้ามหน้า |
| EC-04 | resolve ได้ผู้จัดทำเอง | ว่าง ให้เลือก |
| EC-05 | doc_type PJI ปิดใช้ | 409 DOC_TYPE_INACTIVE · ปุ่มสร้าง disabled |
| EC-06 | version ชน | 409 VERSION_CONFLICT |
| EC-07 | ผู้รับผิดชอบซ้ำหลายแถว | pji_owner_assigned ส่งคนละครั้งเดียว |
| EC-08 | ตัวเลือกระดับความสำคัญ (DEC-15) | ค่าเริ่ม สูง/กลาง/ต่ำ อ่านจาก config ของ doc_type · เปลี่ยนได้หลังลูกค้ายืนยัน |

## §5.6 Error Catalog
400 VALIDATION · 403 NOT_OWNER · 403 NOT_CURRENT_APPROVER · 404 NOT_FOUND · 409 VERSION_CONFLICT · 409 DOC_TYPE_INACTIVE · 422 INVALID_STATE

## §5.7 Security
RLS tenant · สิทธิ์ตาม §5.3 ฝั่ง server ทุก API · audit append-only · ไม่มีรหัสผ่าน/credential ในเอกสาร

## §5.8 Notifications (NTF_BRIEF)
pji_cancelled (pending→cancelled → ผู้พิจารณาขั้นปัจจุบัน · in-app) · pji_owner_assigned (→approved → ผู้รับผิดชอบหลัก + ผู้รับผิดชอบกิจกรรม · in-app+email) · doa_pending/doa_result = DOA engine
