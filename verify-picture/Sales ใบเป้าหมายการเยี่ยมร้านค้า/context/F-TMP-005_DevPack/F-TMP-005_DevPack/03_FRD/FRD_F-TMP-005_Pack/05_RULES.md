# 05_RULES — F-TMP-005

## §5.1 Business Rules
| BR | กฎ | ระดับ | ที่มา |
|---|---|---|---|
| BR-01 | ผู้รับผิดชอบเขต/ตำแหน่ง จาก Sales Territory + Employee (snapshot ตอนบันทึก) · เขตที่เลือกได้ = เขตที่ตนรับผิดชอบ (role-mgr-sales ทุกเขต) · ไม่แก้ master | CONFIGURABLE [AI-DEFAULT] | DEC-04 · DEC-01 |
| BR-02 | territory · sales_cycle · to_recipient บังคับก่อนส่ง · cc_recipients ไม่บังคับ · TO ค่าเริ่ม = ผู้อนุมัติขั้นแรก | FIXED [AI-DEFAULT] | DEC-04 |
| BR-03 | days ≥ 1 และ ≤ 31 (PDF 31 แถวเสมอ) | FIXED [AI-DEFAULT] | DEC-04 · DEC-05 |
| BR-04 | visit_date อยู่ใน sales_cycle และไม่ซ้ำกันในใบ (บล็อก) | FIXED | DEC-16 (VALID) |
| BR-05 | วันที่มีแผน: market_start · market_end · stores ≥ 1 บังคับ · lodging_province ไม่บังคับ | FIXED [AI-DEFAULT] | DEC-04 · DEC-16 |
| BR-06 | customer_count = count(stores) (ไม่ให้กรอกเอง) · แถวรวม = work_days + total_customer_count | FIXED | DEC-14 · DEC-17 (VALID) |
| BR-07 | stores จาก Customer (customerId) ในเขตที่เลือก · ร้านซ้ำในวันเดียว = บล็อก · stores > 7 = เตือน ไม่บล็อก (PDF ต่อชื่อในช่องที่ 7) | FIXED [AI-DEFAULT] | DEC-04 · DEC-15 (VALID) |
| BR-08 | สายอนุมัติ resolve จาก DOA กลางตอนส่ง แล้ว freeze ใน approval_chain · ค่าเริ่ม 2 ขั้น role-line-manager → role-mgr-sales · ห้าม hardcode | CONFIGURABLE (DOA กลาง) [AI-DEFAULT] | DEC-03 · DEC-18 |
| BR-09 | ผู้นำเสนออนุมัติใบตัวเองไม่ได้ (BR-DOA-04) | FIXED | DEC-03 |
| BR-10 | ไม่อนุมัติ (ขั้นใดก็ได้) = กลับร่างเลขเดิม (BR-DOA-03 มาตรฐาน) · เหตุผลบังคับ | FIXED [AI-DEFAULT] | DEC-08 |
| BR-11 | อนุมัติขั้นสุดท้าย → ใบ approved อื่นของ territory_id + sales_cycle เดียวกัน → superseded · แจ้ง TO + CC | FIXED [AI-DEFAULT] | DEC-04 |
| BR-12 | เห็น: owner · ผู้อนุมัติหลังส่ง · role-mgr-sales ทั้งหมด · TO/CC เฉพาะใบ approved/superseded ที่ตนถูกระบุ | FIXED [AI-DEFAULT] | DEC-09 |
| BR-13 | เลข SVT ออกตอนบันทึกครั้งแรก · ไม่อนุมัติใช้เลขเดิม | FIXED | DEC-10 |
| BR-14 | ช่องลงชื่อ PDF = ผู้นำเสนอ + 1 ช่องต่อขั้น DOA · ข้อความ "ส่งในระบบ/พิจารณาในระบบ วันที่ เวลา" ไม่ใช้ภาพ | FIXED | DEC-07 |
| BR-15 | ยกเลิก: owner/role-mgr-sales · draft/pending · เหตุผลบังคับ · แนบไฟล์ ✓ · CSV ✓ (ตามสิทธิ์) · ทำซ้ำ ✗ · ประกาศ ✗ · ไม่ส่งต่อระบบอื่น · ถ้อยคำตามกระดาษ 1:1 (คอลัมน์ว่างใต้ "วันทำงาน" ไม่ใช่ช่อง · ทุกแถวมี "=") | CONFIGURABLE [AI-DEFAULT] | DEC-08 · DEC-11 · DEC-02 · DEC-06 · DEC-12 · DEC-13 |

## §5.2 State Machine
| จาก | การกระทำ | ไป | ผู้ทำ |
|---|---|---|---|
| — | บันทึกครั้งแรก | draft | owner |
| draft | ส่งอนุมัติ | pending | owner |
| pending | อนุมัติ (ไม่ใช่ขั้นสุดท้าย) | pending (ขั้นถัดไป) | ผู้อนุมัติขั้นปัจจุบัน |
| pending | อนุมัติขั้นสุดท้าย | approved | ผู้อนุมัติขั้นปัจจุบัน |
| pending | ไม่อนุมัติ | draft (เลขเดิม) | ผู้อนุมัติขั้นปัจจุบัน |
| approved | ใบใหม่ของเขต+รอบเดียวกันอนุมัติ | superseded | ระบบ |
| draft/pending | ยกเลิก | cancelled | owner · role-mgr-sales |

## §5.3 Permission Matrix
| action | owner | ผู้อนุมัติ (ใน chain) | TO / CC | role-mgr-sales | อื่น ๆ |
|---|---|---|---|---|---|
| ดูรายการ/ใบ | ✓ | ✓ หลังส่ง (ไม่เห็นร่าง) | ✓ เฉพาะ approved/superseded ที่ระบุตน | ✓ ทุกใบ | ✗ (404) |
| สร้าง | ✓ (เขตของตน) | ✓ (เขตของตน) | ✓ (เขตของตน) | ✓ ทุกเขต | ✗ ถ้าไม่มีเขต |
| แก้ร่าง / ส่ง | ✓ | ✗ | ✗ | ✗ (เว้นร่างที่ตัวเองสร้าง) | ✗ |
| อนุมัติ / ไม่อนุมัติ | ✗ (BR-09) | ✓ เฉพาะขั้นปัจจุบัน | ✗ | ✓ เมื่อเป็นขั้นปัจจุบัน | ✗ |
| ยกเลิก | ✓ (draft/pending) | ✗ | ✗ | ✓ | ✗ |
| พิมพ์ / CSV | ✓ (ใบที่เห็น) | ✓ | ✓ | ✓ | ✗ |

## §5.4 Validation
| VR | field | กฎ | ข้อความ |
|---|---|---|---|
| VR-01 | territory | required | กรุณาเลือกเขต |
| VR-02 | sales_cycle | required | กรุณาเลือกรอบการขาย |
| VR-03 | to_recipient | required | กรุณาเลือกผู้รับ (TO) |
| VR-04 | days | ≥1 วัน · ≤31 | ต้องมีแผนเยี่ยมอย่างน้อย 1 วัน |
| VR-05 | days[].visit_date | required · ∈ sales_cycle (DEC-16) | วันที่ต้องอยู่ในรอบการขาย {เดือน ปี} |
| VR-06 | days[].visit_date | ไม่ซ้ำกัน (DEC-16) | วันที่ซ้ำกับวันทำงานอื่น |
| VR-07 | days[].market_start · market_end | required | กรุณากรอกวันที่ · เริ่มต้นตลาด · สิ้นสุดตลาด และร้านค้าอย่างน้อย 1 ร้าน |
| VR-08 | days[].stores | ≥1 · ไม่ซ้ำในวัน | ต้องมีร้านค้าอย่างน้อย 1 ร้าน / มีร้านซ้ำในวันเดียวกัน |
| VR-09 | assignees (submit) | ครบทุกขั้น · ≠ owner | กรุณาเลือกผู้อนุมัติ |
| VR-10 | reason (cancel/reject) | required | กรุณาระบุเหตุผล |
- เตือน (ไม่บล็อก) W-01: stores > 7 — "เกิน 7 ร้าน — แบบพิมพ์มี 7 ช่อง ชื่อที่เกินจะต่อในช่องสุดท้าย" (DEC-15)
- DEC-12/13 → BR-15 · DEC-14/17 → BR-06 · DEC-18 → BR-08

## §5.5 Edge Cases
| EC | กรณี | ผล | อ้าง |
|---|---|---|---|
| EC-01 | เปลี่ยนเขตหลังเลือกร้าน | นำร้านนอกเขตออก + toast จำนวน | BR-07 |
| EC-02 | resolve role-line-manager ไม่ได้ | slot ว่าง บังคับเลือกตอนส่ง | BR-08 |
| EC-03 | เขต+รอบมีใบใช้งานอยู่ | เตือนตอนสร้าง/ส่ง · อนุมัติแล้วใบเดิม superseded | BR-11 |
| EC-04 | 31 วัน + บางวัน 12 ร้าน | PDF 31 แถว · ช่องที่ 7 ต่อชื่อ · บล็อกลงนามไม่ตัดกลาง | BR-03 · BR-07 |
| EC-05 | DOA ตั้ง 6 ขั้น | ลงนาม 7 ช่อง 2 แถว (4+3) | BR-14 |
| EC-06 | CC เปิดใบที่ยังรออนุมัติ | 404 | BR-12 |
| EC-07 | เพิ่มวันที่ 32 | ปุ่ม disabled · API 422 | BR-03 |
| EC-08 | ส่งแล้วต้องแก้ | ผู้อนุมัติไม่อนุมัติ → ร่าง หรือยกเลิกแล้วสร้างใหม่ | BR-10 · BR-15 |
| EC-09 | F-DOCCFG ปิด SVT | 409 DOC_TYPE_INACTIVE · ปุ่มสร้าง disabled | BR-13 |
| EC-10 | วันที่ซ้ำ 2 แถว | บล็อกทั้งสองแถว VR-06 | BR-04 |

## §5.6 การอนุมัติ (DOA)
- ดู `declarations/DOA_BRIEF_F-TMP-005.md` (entry DOA-SVT-01 · document_sign · dynamic · ไม่มีวงเงิน · merged · 2 ขั้น) · field approval_required / approver_role / approved_by / approval_chain / approved_at / doa_ref · `TODO: DOA engine`
