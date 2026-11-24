# 05_RULES — F-TMP-004

## §5.1 Business Rules
| ID | Rule | Tag | ที่มา |
|---|---|---|---|
| BR-01 | ระยะเวลาดำเนินการ/กิจกรรม = end − start + 1 วัน (คำนวณ ไม่ให้กรอก) | FIXED [AI-DEFAULT] | DEC-04 · DEC-15 (VALID) |
| BR-02 | end_date ≥ start_date (โครงการ + กิจกรรม) = บล็อก | FIXED | DEC-15 (VALID) |
| BR-03 | กิจกรรมนอกช่วงวันที่โครงการ = เตือน ไม่บล็อก | CONFIGURABLE [AI-DEFAULT] | DEC-16 (VALID) |
| BR-04 | รวมงบที่ขอ/ที่อนุมัติ = SUM · จำนวนเงิน ≥ 0 | FIXED [AI-DEFAULT] | DEC-04 |
| BR-05 | งบที่อนุมัติ: ผู้อนุมัติขั้นสุดท้ายกรอก · ว่าง = เท่าที่ขอ · < 0 บล็อก · > ที่ขอ = เตือน | CONFIGURABLE [AI-DEFAULT] | DEC-04 · DEC-17 (VALID) |
| BR-06 | ส่ง/บันทึกได้เมื่อมีกิจกรรม ≥ 1 · KPI ≥ 1 · รายการงบ ≥ 1 | FIXED [AI-DEFAULT] | DEC-04 |
| BR-07 | ไม่จำกัดแถว · PDF ขั้นต่ำ KPI 3 · กิจกรรม 10 · งบ 6 · ความเสี่ยง 5 (print_config.min_rows) | CONFIGURABLE | DEC-05 · DEC-06 · DEC-07 · DEC-08 |
| BR-08 | ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง | FIXED [AI-DEFAULT] | DEC-09 |
| BR-09 | อนุมัติแล้วไม่เปลี่ยนค่าในระบบ · ไม่ส่งต่อ Budget/ระบบอื่น | FIXED [AI-DEFAULT] | DEC-01 · DEC-02 |
| BR-10 | แนบไฟล์ระดับใบ · ส่งออก CSV · ไม่มีทำซ้ำ/ประกาศ | FIXED [AI-DEFAULT] | DEC-14 |
| BR-11 | รหัสโครงการออกตอนบันทึกครั้งแรก (PJP) · กลับร่างใช้เลขเดิม | FIXED [AI-DEFAULT] | DEC-13 |
| BR-12 | หลังอนุมัติล็อกทุกช่อง ยกเว้นสถานะกิจกรรม (ผู้จัดทำ/ผู้รับผิดชอบหลัก) · บันทึกประวัติ · ไม่ต้องอนุมัติใหม่ | FIXED [AI-DEFAULT] | DEC-04 |
| BR-13 | ค่าสถานะกิจกรรม {Not Started, In Progress, Completed, Delayed} · ความรุนแรง {สูง, กลาง, ต่ำ} ตามต้นฉบับ | FIXED | DEC-18 (VALID) |
| BR-14 | แถวว่างทั้งแถวไม่บันทึก · แถวที่มีข้อมูลต้องครบช่องบังคับ | FIXED | DEC-09 |
| BR-15 | ตารางอนุมัติ PDF = ผู้จัดทำ + 1 แถวต่อขั้นที่ตั้งใน DOA (dynamic · ห้าม fix) · คำตัดสินตาม role · ข้อความ "ส่ง/พิจารณาในระบบ" ไม่ใช้ภาพ | FIXED (จำนวน = DOA) | DEC-03 · DEC-10 |
| BR-16 | การมองเห็น: เจ้าของ · ผู้อนุมัติเห็นหลังส่ง · admin ฝ่ายพัฒนาโครงการเห็นทั้งหมด · ร่างไม่เห็นโดยผู้อนุมัติ | FIXED [AI-DEFAULT] | DEC-12 |
| BR-17 | ยกเลิกได้เฉพาะ draft/pending โดยเจ้าของหรือ admin · เหตุผลบังคับ | FIXED [AI-DEFAULT] | DEC-11 |
| BR-DOA-01 | ส่งอนุมัติได้เฉพาะ draft | FIXED | DOA |
| BR-DOA-02 | resolve สายตอนส่งแล้ว freeze | FIXED | DOA · DEC-03 |
| BR-DOA-03 | reject → กลับ draft เลขเดิม แก้ได้ · ประวัติ append-only (ตรงกับ DEC-11 — ไม่มีข้อยกเว้น) | FIXED | DEC-11 |
| BR-DOA-04 | ผู้จัดทำพิจารณาใบตัวเองไม่ได้ | FIXED | DOA |
| BR-DOA-05 | ไม่ใช้ (ไม่มีวงเงิน DEC-03) | — | |

## §5.2 State Machine
| จาก | event | ไป | guard |
|---|---|---|---|
| — | save | draft | FN-03 ออกเลข · VR-01..06 |
| draft | submit | pending(1) | owner · assignees ครบ |
| pending(n<N) | approve | pending(n+1) | assignee ขั้น n |
| pending(N) | approve | approved | assignee ขั้น N · BR-05 |
| pending(n) | reject | draft | assignee ขั้น n · เหตุผล |
| approved | update_action_status | approved | owner/PM · BR-12/13 |
| draft/pending | cancel | cancelled | owner/admin · เหตุผล |

## §5.3 Permission Matrix
| Action | owner | ผู้พิจารณาขั้นปัจจุบัน | อยู่ในสาย (ไม่ใช่ขั้นปัจจุบัน) | ผู้รับผิดชอบหลัก (ไม่ใช่ owner) | admin ฝ่ายพัฒนาโครงการ | อื่น |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| ดู draft | ✓ | ✗ | ✗ | ✗ | ✓ | ✗ |
| ดู pending/approved/cancelled | ✓ | ✓ | ✓ | ✗ (OQ-07) | ✓ | ✗ |
| แก้ draft | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| ตัดสิน | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| กรอกงบที่อนุมัติ | ✗ | ✓ (ขั้นสุดท้าย) | ✗ | ✗ | ✗ | ✗ |
| อัปเดตสถานะกิจกรรม | ✓ (approved) | ✗ | ✗ | ✓ (approved · API) | ✗ | ✗ |
| ยกเลิก | ✓ | ✗ | ✗ | ✗ | ✓ | ✗ |

## §5.4 Validation
| VR | ช่อง | เงื่อนไข | ข้อความ |
|---|---|---|---|
| VR-01 | project_name · owner_dept · project_manager · start_date · end_date · background · problem_opportunity · justification · objective_primary | required | กรุณากรอก… / กรุณาเลือก… |
| VR-02 | end_date | ≥ start_date | วันที่สิ้นสุดต้องไม่ก่อนวันที่เริ่มต้น |
| VR-03 | goals / actions / budget | ≥ 1 แถวที่มีข้อมูล | ต้องมี…อย่างน้อย 1 รายการ |
| VR-04 | แถวที่มีข้อมูล (kpi · method · activity · responsible · start/end · item · requested · risk ทั้ง 5 ช่อง) | ครบ | กรอกให้ครบทุกช่องที่มี * |
| VR-05 | actions[].end_date | ≥ start_date | วันที่สิ้นสุดต้องไม่ก่อนวันที่เริ่ม |
| VR-06 | budget[].requested | ตัวเลข ≥ 0 | งบประมาณที่ขอต้องเป็นตัวเลข ≥ 0 |
| VR-07 | budget[].approved (ขั้นสุดท้าย) | ตัวเลข ≥ 0 | งบประมาณที่ได้รับอนุมัติต้องเป็นตัวเลขตั้งแต่ 0 ขึ้นไป |
| VR-08 | slot ผู้พิจารณา | ทุกขั้น · ≠ ผู้จัดทำ | กรุณาเลือกผู้พิจารณา |
| VR-09 | เหตุผล ไม่อนุมัติ/ยกเลิก | required | กรุณาระบุเหตุผล |

## §5.5 Edge Cases
| EC | กรณี | ผล |
|---|---|---|
| EC-01 | ผู้อนุมัติลดงบจากที่ขอ | total_approved < total_requested · pjp_budget_adjusted |
| EC-02 | ผู้อนุมัติให้งบเกินที่ขอ | เตือนในช่อง · บันทึกได้ (DEC-17) |
| EC-03 | แถวเกินกระดาษ (กิจกรรม 12 · KPI 4 · งบ 8 · ความเสี่ยง 6) | PDF dense ยัง 2 หน้า |
| EC-04 | DOA 6 ขั้น | ตารางอนุมัติ 7 แถว ยัง 2 หน้า |
| EC-05 | ผู้จัดทำเป็น role-gm เอง | resolve ข้ามตัวเอง · slot เลือกคนอื่น (BR-DOA-04) |
| EC-06 | แก้ DOA ระหว่างใบรออนุมัติ | ใบเดิมใช้สาย snapshot |
| EC-07 | ส่ง/อนุมัติชนกัน | 409 STALE → toast รีเฟรช |
| EC-08 | doc_type ปิดใช้ | ปุ่มสร้าง disabled + แถบแดง |
| EC-09 | ข้อความยาวมากส่วนที่ 2–3 | PDF อาจเกิน 2 หน้า (OQ-05) |
| EC-10 | ไม่มีความเสี่ยง | ส่งได้ · PDF แถวว่าง 5 แถว |
| EC-11 | กิจกรรมนอกช่วงโครงการ | ป้าย "นอกช่วง" + แถบเตือนขั้นตรวจสอบ · บันทึกได้ (DEC-16) |
