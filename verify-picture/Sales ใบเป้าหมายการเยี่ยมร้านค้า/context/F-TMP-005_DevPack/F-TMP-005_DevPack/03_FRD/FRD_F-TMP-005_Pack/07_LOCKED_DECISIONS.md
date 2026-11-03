# 07_LOCKED_DECISIONS — F-TMP-005

## §7.0 Scope Lock — IMMUTABLE (= DECISIONS.lock REQ-TMP-005 · แทนใบเซ็นจนลูกค้าเซ็น · OQ-01)
> โหมดไม่เฝ้า — มติ AI-DEFAULT ทุกหมวด ต้องให้ลูกค้ายืนยันในใบลงนาม (newfeature-signoff-generator) ก่อน UAT

| DEC | หมวด | มติ | ที่มา | ใช้ใน FRD |
|---|---|---|---|---|
| DEC-01 | G1 | ไม่เปลี่ยนค่าในระบบ (ไม่แก้ Customer / Sales Territory) | AI-DEFAULT | 05 BR-01 |
| DEC-02 | G1 | ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้) | AI-DEFAULT | 02 §2.X · 05 BR-15 |
| DEC-03 | G2 | DOA กลาง dynamic · ค่าเริ่ม 2 ขั้น role-line-manager → role-mgr-sales · ไม่มีวงเงิน | AI-DEFAULT | 03 FN-04/05 · 05 BR-08/09 |
| DEC-04 | G3 | ผู้รับผิดชอบเขตจาก master · TO/CC · วันที่ในรอบ · ร้านจาก Customer · นับลูกค้า · ร้าน >7 เตือน · เขต+รอบใบเดียว | AI-DEFAULT | 03 FN-01/02/09 · 05 BR-01/02/03/05/07/11 |
| DEC-05 | G4 | แผนรายวัน สูงสุด 31 แถว · PDF ≥31 | AI-DEFAULT | 05 BR-03 · EC-07 |
| DEC-06 | G5 | ช่องตรงกระดาษ 1:1 ไม่เพิ่มช่อง | AI-DEFAULT | 05 BR-15 · 01 §1.0 |
| DEC-07 | G6 | ลงชื่อแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพ | AI-DEFAULT | 05 BR-14 · 03 FN-08 |
| DEC-08 | G7 | ไม่อนุมัติ = กลับร่าง · ยกเลิก owner/admin draft·pending · เหตุผลบังคับ | AI-DEFAULT | 03 FN-06/07 · 05 BR-10/15 |
| DEC-09 | G8 | เห็น: เจ้าของ · ผู้อนุมัติหลังส่ง · role-mgr-sales ทั้งหมด · TO/CC ใบอนุมัติแล้ว | AI-DEFAULT | 05 §5.3 · 03 FN-10 |
| DEC-10 | G9 | เลข SVT ออกตอนบันทึกครั้งแรก | AI-DEFAULT | 03 FN-03 · 05 BR-13 |
| DEC-11 | G10 | แนบไฟล์ ✓ · CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗ | AI-DEFAULT | 05 BR-15 |
| DEC-12 | VALID | คอลัมน์ย่อยว่างใต้ "วันทำงาน" ไม่ใช่ช่อง | FORM_SPEC | 05 BR-15 |
| DEC-13 | VALID | ทุกแถวรูปแบบเดียวกัน (มี "=") | FORM_SPEC | 05 BR-15 · 03 FN-08 |
| DEC-14 | VALID | จำนวนลูกค้านับจากรายชื่อร้าน | FORM_SPEC | 05 BR-06 · 03 FN-02 |
| DEC-15 | VALID | ร้านไม่จำกัด · PDF ต่อชื่อช่องที่ 7 · เตือน >7 | FORM_SPEC | 05 BR-07 · W-01 |
| DEC-16 | VALID | วันที่ในรอบ ไม่ซ้ำ (บล็อก) · มีวันที่ต้องมีร้าน ≥1 | FORM_SPEC | 05 BR-04/05 · VR-05/06/08 |
| DEC-17 | VALID | แถวท้ายตาราง = แถวรวม | FORM_SPEC | 05 BR-06 · 04 total_customer_count |
| DEC-18 | VALID | ผู้อนุมัติ 2 ช่อง = DOA dynamic 2 ขั้น (ค่าเริ่ม) | FORM_SPEC | 05 BR-08 |

## §7.1 Locked Decisions (LD)
| LD | เรื่อง | ตัดสิน |
|---|---|---|
| LD-01 | TO / CC | ไม่ใช่ขั้น DOA — เป็นผู้รับแจ้งเมื่ออนุมัติขั้นสุดท้าย (svt_plan_published) · เห็นเฉพาะใบอนุมัติแล้ว |
| LD-02 | ใบใช้งานต่อเขต+รอบ | 1 ใบ (approved) · ใบใหม่อนุมัติ → เดิม superseded (ไม่ลบ) |
| LD-03 | "จำนวนลูกค้า" ซ้ำกับรายชื่อร้าน | เก็บเป็น computed (customer_count) |
| LD-04 | ไม่อนุมัติ | กลับร่างเลขเดิม = BR-DOA-03 มาตรฐาน (DOA_BRIEF on_reject: back_to_draft) |
| LD-05 | role ผู้อนุมัติขั้น 1 ค่าเริ่ม | role-line-manager (relative role นอก DOA master 14 role) — รอยืนยัน OQ-02 |

## §7.2 Convention Deviations
- ไม่มีปุ่ม "ทำซ้ำ" (DEC-11) · แบบพิมพ์ prototype เป็น A4 แนวตั้ง (thai-doc v2.1 ไม่มี orientation — OQ-07) · server ต้อง render แนวนอนตาม print_config.paper

## §7.3 Open Questions → 00 §0.8 (OQ-01..07)

## §7.5 Deferred
- เชื่อม Visit Operation (สร้างตารางเยี่ยม/เช็กอินจากแผนที่อนุมัติ) · เป้ายอดขายรายร้าน — รอบถัดไป
