# 05_RULES — F-TMP-006

## §5.1 Business Rules
| ID | Rule | Tag | ที่มา |
|---|---|---|---|
| BR-01 | ปีรอบ = CoiDisclosureConfig.current_year (ค่าเริ่ม = ปี พ.ศ. ปัจจุบัน) snapshot ลงใบ · ห้าม hardcode | CONFIGURABLE [AI-DEFAULT] | DEC-04 · DEC-12 (VALID) |
| BR-02 | ถ้อยคำรับรองอ่านจาก config · snapshot ตอนส่ง (ใบเก่าแสดงถ้อยคำเดิม) | CONFIGURABLE [AI-DEFAULT] | DEC-04 · DEC-18 (VALID) |
| BR-03 | เลือก ไม่มี/มี ได้ 1 ข้อ · ต้องเลือกก่อนส่ง | FIXED | DEC-14 (VALID) |
| BR-04 | มี → รายละเอียดบังคับ ≥ detail_min · ไม่มี → ล้างรายละเอียด | FIXED (ความยาว CONFIGURABLE) | DEC-15 (VALID) |
| BR-05 | ต้องยืนยันถ้อยคำรับรองก่อนส่ง | FIXED [AI-DEFAULT] | DEC-04 |
| BR-06 | คำนำหน้า/ชื่อ/ตำแหน่งจากข้อมูลพนักงาน snapshot · แก้เองไม่ได้ | FIXED [AI-DEFAULT] | DEC-04 |
| BR-07 | 1 คนมีใบที่มีผล 1 ใบต่อปี · มีใบปีเดียวกัน (ไม่นับยกเลิก/ถูกแทนที่) → เตือน ไม่บล็อก · ใบใหม่อ้างใบเดิม · ใบใหม่รับทราบ → ใบเดิม superseded | FIXED [AI-DEFAULT] | DEC-04 · DEC-12/17 (VALID) |
| BR-08 | ส่งใบที่ตอบ มี → coi_conflict_declared ถึง role-compliance (in-app · ไม่มีรายละเอียด) | CONFIGURABLE | DEC-13/16 · NTF |
| BR-09 | สายพิจารณา resolve จาก DOA ตอนส่ง แล้ว freeze · ค่าเริ่ม 1 ขั้น role-line-manager · "ฝ่ายกฎหมาย" = เพิ่มขั้น role-compliance ที่ DOA กลาง (OQ-03) | CONFIGURABLE [AI-DEFAULT] | DEC-03 · DEC-13 (VALID) |
| BR-10 | เลขออกตอนบันทึกครั้งแรก · ส่งกลับใช้เลขเดิม · no-gap ✗ | FIXED | DEC-10 |
| BR-11 | approved ล็อกแก้ไขและยกเลิกไม่ได้ (เปลี่ยนแปลง = ยื่นใบใหม่) | FIXED | DEC-08 · DEC-17 |
| BR-12 | ไม่เปลี่ยนค่าในระบบ · ไม่ส่งต่อระบบอื่น (coi.disclosure_acknowledged ประกาศไม่ยิง) | FIXED [AI-DEFAULT] | DEC-01/02 |
| BR-13 | มองเห็น: owner · ผู้อยู่ในสายหลังส่ง · role-compliance ทั้งหมด · ผู้จัดการฝ่ายจัดซื้อไม่เห็นทั้งหมดโดยตำแหน่ง · list/CSV/notification ไม่มีรายละเอียดและข้อคิดเห็น · PDF/ไฟล์แนบตรวจสิทธิ์ | FIXED | DEC-09 · DEC-16 (VALID) |
| BR-14 | ช่องลงชื่อใน PDF = ผู้เปิดเผย + 1 ช่องต่อขั้นที่ตั้งใน DOA (dynamic · ห้าม fix จำนวน) · คำตัดสินตาม role (รับทราบ/ส่งกลับแก้ไข) · ข้อความ "ส่ง/พิจารณาในระบบ" | FIXED | DEC-03 · DEC-07 |
| BR-15 | ข้อคิดเห็นของผู้บังคับบัญชากรอกเฉพาะผู้พิจารณาตอนพิจารณา (ไม่บังคับ) · พิมพ์ในกรอบรายขั้น | FIXED [AI-DEFAULT] | DEC-04 |
| BR-16 | ช่องตามกระดาษ 1:1 ไม่เพิ่มช่อง · แนบไฟล์ ✓ · CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗ | FIXED [AI-DEFAULT] | DEC-05/06/11 |
| BR-DOA-01 | ส่งได้เฉพาะ draft/returned | FIXED | DOA |
| BR-DOA-02 | resolve สายตอนส่งแล้ว freeze | FIXED | DOA |
| BR-DOA-03 | reject (ส่งกลับแก้ไข) → กลับร่าง (status returned) แก้ได้ · ประวัติ append-only (ตรงกับ DEC-08 — ไม่มีข้อยกเว้น) | FIXED | DOA · DEC-08 |
| BR-DOA-04 | ผู้เปิดเผย (ผู้ส่ง) พิจารณาใบตัวเองไม่ได้ | FIXED | DOA |
| BR-DOA-05 | ไม่ใช้ (ไม่มีวงเงิน DEC-03) | — | |

## §5.2 State Machine
| จาก | event | ไป | guard |
|---|---|---|---|
| — | save | draft | FN-03 ออกเลข · doc_type เปิดใช้ |
| draft/returned | save | (เดิม) | owner |
| draft/returned | submit | pending(1) | owner · VR-01..03 · assignees ครบ · ≠ owner |
| pending(n) | approve (รับทราบ) | pending(n+1) / approved (+ ใบเดิม superseded) | assignee ขั้น n |
| pending(n) | reject (ส่งกลับแก้ไข) | returned | assignee ขั้น n · เหตุผล |
| draft/pending/returned | cancel | cancelled | owner / role-compliance · เหตุผล |

## §5.3 Permission Matrix (DEC-09 · DEC-16)
| Action | owner | ผู้อยู่ในสาย | role-compliance | ผู้จัดการฝ่ายจัดซื้อ (ไม่อยู่ในสาย) / อื่น |
|---|:-:|:-:|:-:|:-:|
| ดูร่างของตน | ✓ | ✗ ไม่เห็นร่าง | ✓ | ✗ |
| ดูหลังส่ง (รวมรายละเอียด/PDF) | ✓ | ✓ | ✓ | ✗ (404) |
| แก้ไข | ✓ draft/returned | ✗ | ✗ | ✗ |
| ตัดสิน | ✗ | ขั้นปัจจุบันเท่านั้น | ขั้นของตน (ถ้าเพิ่ม) | ✗ |
| ยกเลิก | ✓ | ✗ | ✓ | ✗ |
| CSV | ใบที่เห็น (ไม่มีรายละเอียด) | ใบที่เห็น | ทั้งหมด (ไม่มีรายละเอียด) | ✗ |

## §5.4 Validation Rules
| VR | ช่อง | เงื่อนไข | ข้อความ | ผูก |
|---|---|---|---|---|
| VR-01 | has_conflict | required ตอนส่ง · เลือก 1 | กรุณาเลือก ไม่มี หรือ มี | DEC-14 |
| VR-02 | conflict_detail | required ≥ detail_min (10) เมื่อ has | ระบุรายละเอียดอย่างน้อย 10 ตัวอักษร | DEC-15 |
| VR-03 | confirmed | required ตอนส่ง | กรุณายืนยันถ้อยคำรับรองก่อนส่ง | DEC-04 |
| VR-04 | slot ผู้พิจารณา | ครบทุกขั้น · ≠ owner | กรุณาเลือกผู้พิจารณา | BR-DOA-04 |
| VR-05 | เหตุผล ส่งกลับแก้ไข/ยกเลิก | required | กรุณาระบุเหตุผล | DEC-08 |
| VR-06 | ส่งร่างไม่ครบจากหน้าดู | VR-01..03 | เลือก ไม่มี/มี กรอกรายละเอียด และยืนยันถ้อยคำรับรองก่อนส่ง | DEC-14/15 |

## §5.5 Edge Cases
| EC | กรณี | ผล | ผูก |
|---|---|---|---|
| EC-01 | มี → เปลี่ยนเป็น ไม่มี | ล้าง/ซ่อนรายละเอียด | DEC-15 |
| EC-02 | มี + รายละเอียด 9 ตัวอักษร | บล็อก + ช่องแดง | VR-02 |
| EC-03 | ส่งร่างที่ยังไม่ยืนยันจากหน้าดู | toast + เปิดแก้ไข · API 422 CONFIRM_REQUIRED | VR-06 |
| EC-04 | ยื่นใหม่ในปีที่มีใบรับทราบแล้ว | เตือน · supersedes_no · รับทราบ → ใบเดิม superseded | DEC-12/17 |
| EC-05 | ไม่มีผู้บังคับบัญชาในผังองค์กร | slot ว่าง → ต้องเลือกเอง | VR-04 |
| EC-06 | DOA เพิ่มขั้นฝ่ายกฎหมาย | slot/ช่องลงชื่อเพิ่มตามจริง | DEC-13 |
| EC-07 | แก้ DOA ระหว่างรอพิจารณา | ใช้สาย snapshot | BR-DOA-02 |
| EC-08 | stale | 409 → toast รีเฟรช | |
| EC-09 | doc_type ปิด | ปุ่มสร้าง disabled · API 409 DOC_TYPE_INACTIVE | DEC-10 |
| EC-10 | ข้ามปี / ถ้อยคำเปลี่ยน | ใบเดิมคงปีและถ้อยคำ snapshot | DEC-04/18 |
| EC-11 | ผู้จัดการฝ่ายจัดซื้อเปิดลิงก์ใบที่ไม่ได้พิจารณา | 404 ไม่เห็น | DEC-09/16 |
| EC-12 | รายละเอียดเกิน 3 บรรทัด | PDF ต่อบรรทัด + dense · 1 หน้า | DEC-05 |

## §5.6 Notification
| Event | Trigger | ผู้รับ | ช่องทาง | อ้าง |
|---|---|---|---|---|
| coi_conflict_declared | draft→pending และ has_conflict=has (FN-05 → FN-10) | role-compliance | in-app (บังคับ · ไม่มีรายละเอียด) | BR-08 |
| coi_cancelled | pending→cancelled (FN-08 → FN-10) | ผู้พิจารณาขั้นปัจจุบัน | in-app | BR-DOA |
| doa_pending / doa_result | DOA engine | — | — | ไม่ประกาศซ้ำ |
