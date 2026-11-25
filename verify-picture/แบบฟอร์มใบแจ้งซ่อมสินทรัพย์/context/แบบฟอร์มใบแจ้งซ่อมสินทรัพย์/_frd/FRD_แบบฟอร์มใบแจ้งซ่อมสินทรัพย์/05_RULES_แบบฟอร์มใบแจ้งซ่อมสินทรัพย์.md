# 05_RULES — F-TMP-001

## §5.1 Business Rules
| ID | Rule | Tag | อ้าง |
|---|---|:-:|---|
| BR-01 | ≥1 รายการ · ทุกแถวกรอก รายการ/จำนวน/อาการชำรุด/สถานที่ตั้ง | FIXED | DEC-15 |
| BR-02 | จำนวน = จำนวนเต็ม > 0 | FIXED | DEC-15 |
| BR-03 | ทะเบียนสินทรัพย์ = ข้อความกรอกเอง ว่างได้ (ยังไม่มี Asset Master) | CONFIGURABLE | DEC-04 [AI-DEFAULT] |
| BR-04 | ประวัติการซ่อม: กรอกโดยผู้พิจารณาขั้นแรกของ approval_chain ตอนตัดสิน · ไม่บังคับ · แทนที่ทั้งชุด | CONFIGURABLE | DEC-04 [AI-DEFAULT] |
| BR-05 | สายอนุมัติ resolve จาก DOA ตอนส่ง แล้ว freeze | FIXED | DEC-03 · BR-DOA-02 |
| BR-06 | ไม่อนุมัติ/ไม่ผ่านการตรวจสอบ → draft เลขเดิม (returned_*) · resolve ใหม่ตอนส่ง | FIXED | DEC-09 · BR-DOA-03 |
| BR-07 | ออกเลขตอนบันทึกครั้งแรก (ENG-DOC-NUM · RPR) · no-gap ✗ · ปิดใช้ที่ F-DOCCFG = สร้างไม่ได้ | CONFIGURABLE | DEC-11 |
| BR-08 | ร่างเห็นเฉพาะเจ้าของ (+ admin) · ผู้อนุมัติเห็นหลังส่ง | FIXED | DEC-10 · #109 |
| BR-09 | ช่องลงชื่อ PDF = ผู้แจ้งซ่อม + 1 ช่องต่อขั้นใน DOA (dynamic) · แถวละ ≤4 · คำตัดสินตาม role (role-line-manager = ตรวจสอบแล้ว/ไม่ผ่านการตรวจสอบ) · ไม่ใช้ภาพลายมือ | FIXED (จำนวน = DOA) | DEC-03 · DEC-08 |
| BR-10 | ผู้แจ้งบันทึกครั้งเดียวตอนส่ง แสดง 2 จุดบนแบบพิมพ์ | FIXED | DEC-13 |
| BR-11 | ป้ายทุกช่องตามกระดาษ 1:1 · ไม่เพิ่มช่อง | FIXED | DEC-07 · DEC-16 |
| BR-12 | อนุมัติครบสาย: ไม่เปลี่ยนค่าในระบบ · ไม่ส่งต่อระบบอื่น (event `rpr.approved` ประกาศแต่ไม่ยิง) | FIXED | DEC-01 · DEC-02 |
| BR-13 | ไฟล์แนบระดับใบ (Document Center) · CSV ตามตัวกรอง · ไม่มีทำซ้ำ/ประกาศ | FIXED | DEC-12 |
| BR-DOA-01 | ส่งได้เฉพาะ draft | FIXED | doa-declaration |
| BR-DOA-02 | resolve ตอนส่ง แล้ว freeze ลง approval_chain | FIXED | doa-declaration |
| BR-DOA-03 | ไม่อนุมัติ → กลับ draft (ตรงค่าเริ่ม · on_reject = back_to_draft) | FIXED | DEC-09 |
| BR-DOA-04 | ผู้แจ้งอนุมัติใบตัวเองไม่ได้ | FIXED | SoD |
| BR-DOA-05 | ไม่มีวงเงิน → ไม่ re-resolve | — | DEC-03 |

## §5.2 State Machine
| จาก | Action | ไป | ใคร | API |
|---|---|---|---|---|
| — | บันทึกครั้งแรก | draft | owner | API-03 |
| draft | ส่ง | pending (ขั้น 1) | owner | API-06 |
| pending | approve ขั้น n<N | pending (n+1) | assignee ขั้น n | API-07 |
| pending | approve ขั้น N | approved | assignee ขั้น N | API-07 |
| pending | reject | draft (returned) | assignee ขั้นปัจจุบัน | API-07 |
| draft / pending | cancel | cancelled | owner / admin | API-08 |

## §5.3 Permission Matrix (DEC-10)
| Action | owner | assignee ในสาย | admin role | คนอื่น |
|---|:-:|:-:|:-:|:-:|
| ดู (draft) | ✓ ของตน | ✗ (ไม่เห็นร่างของคนอื่น) | ✓ | ✗ |
| ดู (pending/approved/cancelled) | ✓ | ✓ | ✓ | ✗ (404) |
| สร้าง/แก้ร่าง | ✓ ของตน | ✗ | ✗ | ✗ |
| ส่ง | ✓ ของตน (draft) | ✗ | ✗ | ✗ |
| ตัดสิน | ✗ | เฉพาะขั้นปัจจุบัน | ✗ | ✗ |
| ยกเลิก | ✓ (draft/pending) | ✗ | ✓ (draft/pending) | ✗ |

## §5.4 Validation
| VR | ช่อง | เงื่อนไข | ข้อความ |
|---|---|---|---|
| VR-01 | items[] | ≥1 แถว · description/symptom/location ไม่ว่าง | กรอกรายการ · อาการชำรุด · สถานที่ตั้ง |
| VR-02 | items[].qty | จำนวนเต็ม > 0 | จำนวนต้องเป็นตัวเลขมากกว่า 0 |
| VR-03 | assignees[] | ทุกขั้นต้องเลือก · ≠ ผู้แจ้ง | กรุณาเลือกผู้พิจารณา |
| VR-04 | reason (reject/cancel) | required (DEC-14) | กรุณาระบุเหตุผล |
| VR-05 | history[].repair_count | ว่าง หรือ จำนวนเต็ม ≥0 | จำนวนครั้งที่ซ่อมต้องเป็นตัวเลข |

## §5.5 Edge Cases
| EC | กรณี | ผล |
|---|---|---|
| EC-01 | ไม่มีทะเบียนสินทรัพย์ | เว้นว่างได้ (BR-03) |
| EC-02 | รายการ > 10 / ประวัติ > 6 | PDF dense 1 หน้า (ทดสอบ 14 + 8) |
| EC-03 | ผู้แจ้งถือ role-mgr-acc | slot ว่าง ต้องเลือกคนอื่น |
| EC-04 | แก้ DOA ระหว่างรอ | ใช้ snapshot |
| EC-05 | stale | 409 STALE |
| EC-06 | doc_type ปิดใช้ | 409 DOC_TYPE_INACTIVE · ปุ่มสร้าง disabled |
| EC-07 | DOA 1/3/6 ขั้น | ช่องลงชื่อ 2/4/7 · ประวัติยังกรอกที่ขั้นแรก |
| EC-08 | แจ้งซ้ำทรัพย์สินเดิม | ไม่ตรวจรอบนี้ (OQ-04) |
| EC-09 | ผู้ตรวจสอบไม่กรอกประวัติ | ผ่านได้ · ตาราง PDF ว่าง |

## §5.6 Notifications (NTF_BRIEF_F-TMP-001)
| Event | Trigger | ผู้รับ | ช่องทาง |
|---|---|---|---|
| rpr_cancelled | pending → cancelled (FN-07) | ผู้พิจารณาขั้นปัจจุบัน | in-app · ปิดได้ |
| rpr_ready_for_repair | → approved (FN-05) | admin role ฝ่ายบริหารสินทรัพย์ | in-app · บังคับ |
DOA engine ยิง doa_pending / doa_result เอง

## §5.7 การอนุมัติ (DOA)
ดู `declarations/DOA_BRIEF_F-TMP-001.md` — feature ไม่ hardcode สาย · `approval_chain` snapshot ตอนส่ง
