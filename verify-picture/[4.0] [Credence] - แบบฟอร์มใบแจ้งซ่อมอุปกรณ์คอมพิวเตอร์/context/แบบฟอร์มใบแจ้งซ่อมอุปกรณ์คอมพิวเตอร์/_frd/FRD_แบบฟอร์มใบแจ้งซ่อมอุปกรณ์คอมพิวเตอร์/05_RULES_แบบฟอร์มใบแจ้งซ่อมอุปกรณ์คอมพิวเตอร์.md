# 05_RULES — F-TMP-004
> [AI-DEFAULT] = มติที่ AI ตอบตาม unattended-policy — ต้องให้ลูกค้ายืนยันในใบลงนามก่อน UAT

## §5.1 Business Rules
| ID | Rule | Tag | อ้าง |
|---|---|:-:|---|
| BR-01 | ประเภทอุปกรณ์เลือก 1 ข้อ (1 ใบ = 1 อุปกรณ์) [AI-DEFAULT] | FIXED | DEC-04 |
| BR-02 | ติ๊ก อื่นๆ ต้องระบุข้อความ | FIXED | DEC-18 |
| BR-03 | วันที่ต้องการส่งมอบก่อนวันที่แจ้ง · วันสิ้นสุด (ถึง) ก่อนวันเริ่ม (ระยะเวลา) = เตือน ไม่บล็อก [AI-DEFAULT] | CONFIGURABLE | DEC-04 · DEC-16 · DEC-17 |
| BR-04 | ผลตรวจเช็ค 3 ตัวเลือกล่าง ต้องกรอก ระยะเวลา-ถึง · ร้านค้า · วันที่ส่งเคลม · ตัวเลือกอื่นล้างชุดเคลม [AI-DEFAULT] | FIXED | DEC-04 |
| BR-05 | สายอนุมัติ resolve จาก DOA ตอนส่งอนุมัติผลตรวจเช็คแล้ว freeze · จำนวนขั้นตาม DOA (ค่าเริ่ม 1 ขั้น role-line-manager ของผู้ส่ง) [AI-DEFAULT] | FIXED | DEC-03 |
| BR-06 | ไม่อนุมัติ → กลับร่างผลตรวจเช็ค (inspecting) เลขเดิม · ล้างสาย (BR-DOA-03) [AI-DEFAULT] | FIXED | DEC-08 |
| BR-07 | เลข CRR ออกตอนบันทึกครั้งแรก · no-gap ✗ | CONFIGURABLE | DEC-10 |
| BR-08 | ร่างเห็นเฉพาะเจ้าของ + role-it-officer · ผู้อนุมัติเห็นเมื่ออยู่ในสาย | FIXED | DEC-09 |
| BR-09 | ช่องลงชื่อ PDF: คู่ส่วนที่ 1 · ผู้ดำเนินการ + 1 ช่อง/ขั้น DOA · คู่ผลการซ่อม · ข้อความในระบบ ไม่ใช้ภาพ | FIXED | DEC-07 |
| BR-10 | รับแจ้ง · ผลตรวจเช็ค · ส่งอนุมัติ · ผลการซ่อม = role-it-officer ตามสถานะ · รับทราบผล = เจ้าของ [AI-DEFAULT] | FIXED | DEC-03 · DEC-09 |
| BR-11 | ผลการซ่อม ไม่สามารถแก้ไขได้ ต้องระบุรายละเอียด [AI-DEFAULT] | FIXED | DEC-04 |
| BR-12 | ไม่เปลี่ยนค่าในระบบ · ไม่ส่งต่อระบบอื่น (ทะเบียนทรัพย์สิน/PR) | FIXED | DEC-01 · DEC-02 |
| BR-13 | ช่อง/ป้ายตามกระดาษ 1:1 · แก้สะกด ตำแหน่ง · ส่งเคลม · สั่งซื้อ · คงคำ "ร้านค้าที่ส่งเคลม" ใต้ตัวเลือกสั่งซื้อ | FIXED | DEC-06 · DEC-12 · DEC-13 · DEC-14 · DEC-15 |
| BR-14 | Rev. แบบพิมพ์จาก print_config (Rev.00 : 01/07/2569) · 2 หน้า A4 | CONFIGURABLE | DEC-07 |
| BR-15 | แนบไฟล์ ✓ · CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗ | FIXED | DEC-11 |
| BR-16 | ไม่มีรายการซ้ำบนแบบฟอร์ม | FIXED | DEC-05 |
| BR-DOA-01..05 | ส่งได้เฉพาะร่าง (ที่นี่ = inspecting ร่างผลตรวจเช็ค) · resolve ตอนส่ง freeze · ไม่อนุมัติ→ร่าง · ผู้ส่งอนุมัติตัวเองไม่ได้ · (ไม่มีวงเงิน) | FIXED | DOA contract |

## §5.2 ENG-NOTIFY
| event | trigger | ผู้รับ |
|---|---|---|
| crr_reported | draft → reported | role-it-officer |
| crr_received | reported → inspecting | ผู้แจ้งซ่อม |
| crr_cancelled | pending → cancelled | ผู้พิจารณาขั้นปัจจุบัน |
| crr_repaired | approved → repaired | ผู้แจ้งซ่อม |

## §5.3 สิทธิ์ (DEC-09)
| Action | เจ้าของ | ผู้พิจารณาขั้นปัจจุบัน | ผู้อยู่ในสาย (ไม่ใช่ขั้นปัจจุบัน) | role-it-officer | คนอื่น |
|---|:-:|:-:|:-:|:-:|:-:|
| ดูร่าง | ✓ | ✗ | ✗ | ✓ | ✗ |
| ดูหลังส่งอนุมัติ | ✓ | ✓ | ✓ | ✓ | ✗ |
| แก้ไข (ส่วนที่ 1) | ร่าง | ✗ | ✗ | ✗ | ✗ |
| ส่งแจ้งซ่อม | ร่าง | ✗ | ✗ | ✗ | ✗ |
| รับแจ้ง · ผลตรวจเช็ค · ส่งอนุมัติ | ✗ | ✗ | ✗ | ตามสถานะ | ✗ |
| อนุมัติ/ไม่อนุมัติ | ✗ | ✓ | ✗ | ✗ (ใบที่ตนส่ง) | ✗ |
| บันทึกผลการซ่อม | ✗ | ✗ | ✗ | approved | ✗ |
| รับทราบผล | repaired | ✗ | ✗ | ✗ | ✗ |
| ยกเลิก | ก่อนอนุมัติ | ✗ | ✗ | ก่อนอนุมัติ | ✗ |

## §5.4 Validation
| VR | ช่อง | เงื่อนไข | ข้อความ |
|---|---|---|---|
| VR-01 | device_type | required | เลือกประเภทอุปกรณ์ |
| VR-02 | device_type_other | required เมื่อ other | ระบุประเภทอุปกรณ์อื่นๆ |
| VR-03 | item_name | required | ระบุรายการ |
| VR-04 | problem | required | ระบุอาการเสีย / ปัญหา |
| VR-05 | due_date | required | เลือกวันที่ต้องการส่งมอบ |
| VR-06 | delivery_location | required | ระบุสถานที่ส่งมอบ |
| VR-07 | repair_date | required | เลือกวันที่ดำเนินการซ่อม |
| VR-08 | check_result | required | เลือกผลของการตรวจเช็ค/ซ่อม |
| VR-09 | claim_period_from · claim_period_to · claim_vendor · claim_date | required เมื่อ 3 ตัวเลือกล่าง | เลือกวันเริ่ม · เลือกวันสิ้นสุด · ระบุร้านค้าที่ส่งเคลม · เลือกวันที่ส่งเคลม |
| VR-10 | assignees | ครบทุกขั้น · ≠ ผู้ส่ง | กรุณาเลือกผู้พิจารณา |
| VR-11 | repair_result | required | เลือกผลการซ่อม |
| VR-12 | repair_note | required เมื่อ unfixable | ระบุรายละเอียดเมื่อแก้ไขไม่ได้ |
| VR-13 | reason (ไม่อนุมัติ/ยกเลิก) | required | กรุณาระบุเหตุผล |

## §5.5 Edge Cases
| EC | กรณี | ผล |
|---|---|---|
| EC-01 | due_date < report_date (DEC-17) | warning ส่งได้ |
| EC-02 | other ไม่ระบุ (DEC-18) | VR-02 |
| EC-03 | ส่งเคลมไม่กรอกชุดเคลม | VR-09 |
| EC-04 | claim_period_to < claim_period_from (DEC-16) | warning บันทึกได้ |
| EC-05 | เปลี่ยนผลตรวจเช็คเป็นซ่อมเสร็จ | ล้าง claim_* |
| EC-06 | ข้อความเกินบรรทัดกระดาษ | PDF dense 2 หน้า |
| EC-07 | DOA 6 ขั้น | ลายเซ็นส่วนที่ 2 = 7 ช่อง 4+3 · 2 หน้า |
| EC-08 | ผู้ส่งไม่มีผู้บังคับบัญชา | slot ว่างให้เลือก |
| EC-09 | แก้ DOA ระหว่างรอ | ใช้ snapshot |
| EC-10 | stale | 409 STALE |
| EC-11 | doc_type ปิด | 409 DOC_TYPE_INACTIVE · ปุ่มแจ้งซ่อม disabled |
| EC-12 | เปิดใบที่ไม่มีสิทธิ์ | 404 / ไม่เปิด drawer |
| EC-13 | ไม่สามารถแก้ไขได้ | VR-12 · ปิดงานได้หลังรับทราบ |
| EC-14 | ไม่มีรหัสทรัพย์สิน | บันทึกได้ · PDF ช่องว่าง |

## §5.6 Errors
DOC_TYPE_INACTIVE · NOT_OWNER · NOT_DRAFT · NOT_REPORTED · NOT_INSPECTING · INSPECTION_INCOMPLETE · STALE · ASSIGNEE_REQUIRED · SELF_APPROVE · NOT_CURRENT_APPROVER · REASON_REQUIRED · NOT_IT_OFFICER · NOT_APPROVED · NOT_REPAIRED · NOTE_REQUIRED · NOT_FOUND
