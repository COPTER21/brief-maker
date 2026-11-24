# 05_RULES — F-TMP-005

## §5.1 Business Rules
| ID | Rule | Tag | ที่มา |
|---|---|---|---|
| BR-01 | รหัสโครงการเลือกเฉพาะ PJP สถานะ approved · ชื่อ/PM snapshot จากแผน แก้ไม่ได้ | FIXED [AI-DEFAULT] | DEC-04 |
| BR-02 | เติมค่าเริ่มจาก PJP เฉพาะส่วนที่ยังว่าง · ไม่เขียนกลับแผน · ไม่ส่งต่อระบบอื่น | FIXED [AI-DEFAULT] | DEC-01 · DEC-02 · DEC-04 |
| BR-03 | period_to ≥ period_from = บล็อก | FIXED | DEC-19 (VALID) |
| BR-04 | pct 0–100 · budget_plan/actual ≥ 0 = บล็อก | FIXED | DEC-17 (VALID) · DEC-04 |
| BR-05 | delayed → issues ≥ 1 (บล็อก) · decisions ≥ 1 (เตือน) · at_risk → issues ≥ 1 (เตือน) | CONFIGURABLE [AI-DEFAULT] | DEC-18 (VALID) |
| BR-06 | เตือน: รอบทับรายงาน (≠ cancelled) ของโครงการเดียวกัน · report_date < period_to · budget_actual > budget_plan · due_date < report_date | CONFIGURABLE [AI-DEFAULT] | DEC-04 · DEC-19 (VALID) |
| BR-07 | ส่งอนุมัติได้เฉพาะ project_manager ของแผน · ผู้จัดทำอื่นใช้ "แจ้งผู้จัดการโครงการ" (ppr_draft_for_pm) | FIXED [AI-DEFAULT] | DEC-03 · DEC-04 |
| BR-08 | ไม่จำกัดแถว · PDF ขั้นต่ำ ผลงาน 9 · KPI 8 · ปัญหา 11 · แผนรอบถัดไป 10 · ประเด็น 11 (print_config.min_rows) | CONFIGURABLE | DEC-05 · DEC-06 · DEC-07 · DEC-08 · DEC-09 |
| BR-09 | ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง · ผู้รับผิดชอบ/กำหนดเสร็จ เก็บแยก แสดงรวม | FIXED [AI-DEFAULT] | DEC-10 · DEC-20 (VALID) |
| BR-10 | ถ้อยคำตัวเลือกสถานะตามกระดาษ 1:1 ในแบบพิมพ์ (รวมประโยคซ้ำของ ☐ ล่าช้าฯ) · หน้าจอแสดงส่วนเฉพาะ | FIXED | DEC-16 (VALID) · OQ-05 |
| BR-11 | แนบไฟล์ระดับใบ · ส่งออก CSV · ไม่มีทำซ้ำ/ประกาศ | FIXED [AI-DEFAULT] | DEC-15 |
| BR-12 | บล็อกลงชื่อ PDF = ผู้จัดทำ + ผู้จัดการโครงการ (ส่งในระบบ) + 1 ช่องต่อขั้นที่ตั้งใน DOA (dynamic · ห้าม fix) · คำตัดสินตาม role · ข้อความในระบบไม่ใช้ภาพ | FIXED [AI-DEFAULT] | DEC-03 · DEC-11 |
| BR-13 | เลขที่ออกตอนบันทึกครั้งแรก (PPR) · กลับร่างใช้เลขเดิม | FIXED [AI-DEFAULT] | DEC-14 |
| BR-14 | การมองเห็น: ผู้จัดทำ · PM ของโครงการ (รวมร่าง) · ผู้อนุมัติเห็นหลังส่ง · admin ฝ่ายพัฒนาโครงการเห็นทั้งหมด | FIXED [AI-DEFAULT] | DEC-13 |
| BR-15 | ยกเลิกได้เฉพาะ draft/pending โดยเจ้าของหรือ admin · เหตุผลบังคับ | FIXED [AI-DEFAULT] | DEC-12 |
| BR-16 | แถวว่างทั้งแถวไม่บันทึก · แถวที่มีข้อมูลต้องครบช่องบังคับ | FIXED | DEC-10 |
| BR-DOA-01 | ส่งอนุมัติได้เฉพาะ draft | FIXED | DOA |
| BR-DOA-02 | resolve สายตอนส่ง (relative ต่อ PM) แล้ว freeze | FIXED | DOA · DEC-03 |
| BR-DOA-03 | reject → กลับ draft เลขเดิม แก้ได้ · ประวัติ append-only (ตรงกับ DEC-12 — ไม่มีข้อยกเว้น) | FIXED | DEC-12 |
| BR-DOA-04 | ผู้ส่ง (PM) พิจารณาใบตัวเองไม่ได้ | FIXED | DOA |
| BR-DOA-05 | ไม่ใช้ (ไม่มีวงเงิน DEC-03) | — | |

## §5.2 State Machine
| จาก | event | ไป | guard |
|---|---|---|---|
| — | save | draft | FN-03 ออกเลข · VR-01..07 |
| draft | notify_pm | draft | owner ≠ PM |
| draft | submit | pending(1) | PM · assignees ครบ |
| pending(n<N) | approve | pending(n+1) | assignee ขั้น n |
| pending(N) | approve | approved | assignee ขั้น N |
| pending(n) | reject | draft | assignee ขั้น n · เหตุผล |
| draft/pending | cancel | cancelled | owner/admin · เหตุผล |

## §5.3 Permission Matrix
| Action | owner (ผู้จัดทำ) | PM ของโครงการ | ผู้พิจารณาขั้นปัจจุบัน | อยู่ในสาย (ไม่ใช่ขั้นปัจจุบัน) | admin | อื่น ๆ |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| ดู draft | ✓ | ✓ | ✗ | ✗ | ✓ | ✗ |
| ดู pending/approved/cancelled | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ |
| แก้ draft | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ |
| แจ้งผู้จัดการโครงการ | ✓ (ไม่ใช่ PM) | – | ✗ | ✗ | ✗ | ✗ |
| ส่งอนุมัติ | ✗ (เว้นเป็น PM) | ✓ | ✗ | ✗ | ✗ | ✗ |
| ตัดสิน | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ |
| ยกเลิก | ✓ | ✗ | ✗ | ✗ | ✓ | ✗ |

## §5.4 Validation
| VR | ช่อง | เงื่อนไข | ข้อความ |
|---|---|---|---|
| VR-01 | project_plan_id · period_from · period_to · report_date · overall_status · status_note · schedule_plan · schedule_actual · budget_plan · budget_actual | required | กรุณากรอก… / กรุณาเลือก… |
| VR-02 | period_to | ≥ period_from | วันสิ้นรอบต้องไม่ก่อนวันเริ่มรอบ |
| VR-03 | performance | ≥ 1 แถวที่มีข้อมูล | ต้องมีผลการดำเนินงาน อย่างน้อย 1 รายการ |
| VR-04 | แถวที่มีข้อมูล (performance activity/plan/actual/pct · kpi metric/plan/actual · issue ทั้ง 5 ช่อง · next ทั้ง 3 · decision ทั้ง 4) | ครบ | กรอกให้ครบทุกช่องในแถวนี้ |
| VR-05 | performance[].pct | 0–100 | % สำเร็จต้องอยู่ระหว่าง 0–100 |
| VR-06 | budget_plan · budget_actual | ตัวเลข ≥ 0 | กรุณากรอกตัวเลข ≥ 0 |
| VR-07 | issues (overall=delayed) | ≥ 1 | สถานะ ล่าช้า หรือมีปัญหา ต้องระบุปัญหา อุปสรรค และความเสี่ยงอย่างน้อย 1 รายการ |
| VR-08 | slot ผู้พิจารณา | ทุกขั้นต้องเลือก · ≠ PM | กรุณาเลือกผู้พิจารณา |
| VR-09 | เหตุผล ไม่อนุมัติ/ยกเลิก | required | กรุณาระบุเหตุผล |

## §5.5 Edge Cases
| EC | กรณี | ผล |
|---|---|---|
| EC-01 | แผนโครงการถูกยกเลิก/ปิดหลังมีร่าง | lookup ไม่แสดง · ส่งไม่ได้ 409 PROJECT_NOT_ACTIVE (OQ-06) |
| EC-02 | เปลี่ยน PM ในแผนระหว่างร่าง | สิทธิ์ส่งตาม PM ปัจจุบัน · ใบที่ส่งแล้วใช้ snapshot |
| EC-03 | ผู้จัดทำ = PM | ส่งได้เลย · ลงชื่อ 2 ช่องชื่อเดียวกัน |
| EC-04 | แถวเกินกระดาษ | PDF dense ยัง 2 หน้า (ทดสอบ ผลงาน 12 · ปัญหา 12) |
| EC-05 | DOA 6 ขั้น | ลงชื่อ 8 ช่อง 2 แถว ยัง 2 หน้า |
| EC-06 | PM = ผู้จัดการทั่วไป | resolve role-gm ข้ามตัวเอง · ต้องเลือกคนอื่น |
| EC-07 | stale | 409 → toast รีเฟรช |
| EC-08 | doc_type ปิดใช้ | ปุ่มสร้าง disabled |
| EC-09 | รอบทับรายงานเดิม | เตือน · บันทึก/ส่งได้ (DEC-19) |
| EC-10 | ข้อความยาวมาก | PDF อาจล้น 2 หน้า → UAT (OQ-07) |

## §5.6 Notification Rules
ppr_cancelled (FN-07) · ppr_draft_for_pm (FN-11) · ppr_urgent_decision (FN-04 · overall=delayed) — ผ่าน ENG-NOTIFY เท่านั้น · DOA events ไม่ประกาศซ้ำ
