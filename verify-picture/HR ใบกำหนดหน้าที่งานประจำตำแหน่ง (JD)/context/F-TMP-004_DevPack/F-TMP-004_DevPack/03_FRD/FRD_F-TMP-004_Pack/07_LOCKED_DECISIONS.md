# 07_LOCKED_DECISIONS — F-TMP-004

## §7.0 Scope Lock — IMMUTABLE (= DECISIONS.lock REQ-TMP-004 · แทนใบเซ็นจนลูกค้าเซ็น · OQ-01)
> โหมดไม่เฝ้า — มติ AI-DEFAULT ทุกหมวด ต้องให้ลูกค้ายืนยันในใบลงนาม (newfeature-signoff-generator) ก่อน UAT

| DEC | หมวด | มติ | ที่มา | ใช้ใน FRD |
|---|---|---|---|---|
| DEC-01 | G1 | ไม่เปลี่ยนค่าในระบบ (ไม่แก้ Position master) | AI-DEFAULT | 05 BR-01 |
| DEC-02 | G1 | ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้) | AI-DEFAULT | 02 §2.X · 05 BR-15 |
| DEC-03 | G2 | DOA กลาง dynamic · ค่าเริ่ม 1 ขั้น role-line-manager · ไม่มีวงเงิน | AI-DEFAULT | 03 FN-04/05 · 05 BR-07/09 |
| DEC-04 | G3 | ดึงจาก master · กฎบล็อก/เตือน · ฉบับใหม่แทนฉบับเดิม · ผู้ดำรงตำแหน่งรับทราบ | AI-DEFAULT | 03 FN-01/02/09/10/11 · 05 BR-01/02/10/11 |
| DEC-05 | G4 | หัวหน้า ไม่จำกัดแถว · PDF ≥3 | AI-DEFAULT | 05 BR-06 |
| DEC-06 | G4 | ลูกน้อง ไม่จำกัดแถว · PDF ≥3 | AI-DEFAULT | 05 BR-06 · EC-04 |
| DEC-07 | G5 | ช่องตรงกระดาษ 1:1 ไม่เพิ่มช่อง | AI-DEFAULT | 05 BR-16 · 01 §1.0 |
| DEC-08 | G6 | ลงชื่อแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพ | AI-DEFAULT | 05 BR-14 · 03 FN-08 |
| DEC-09 | G7 | ไม่อนุมัติ = กลับร่าง · ยกเลิก owner/HR draft·pending · เหตุผลบังคับ | AI-DEFAULT | 03 FN-06/07 · 05 BR-08/15 |
| DEC-10 | G8 | เห็น: เจ้าของ · ผู้อนุมัติหลังส่ง · HR ทั้งหมด · ผู้ดำรงตำแหน่งฉบับอนุมัติของตน | AI-DEFAULT | 05 §5.3 · 03 FN-12 |
| DEC-11 | G9 | เลข JD ออกตอนบันทึกครั้งแรก | AI-DEFAULT | 03 FN-03 · 05 BR-13 |
| DEC-12 | G10 | แนบไฟล์ ✓ · CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗ | AI-DEFAULT | 05 BR-15 |
| DEC-13 | VALID | ผู้ใต้บังคับบัญชาคำนวณจากตาราง | FORM_SPEC | 05 BR-05 |
| DEC-14 | VALID | หัวหน้า ≥1 แถว · แถวแรกไม่ตรงรายงานต่อ = เตือน | FORM_SPEC | 05 BR-03 · VR-05 · W-01 |
| DEC-15 | VALID | จำนวน (คน) จำนวนเต็ม ≥1 (บล็อก) | FORM_SPEC | 05 BR-04 · VR-06/07 |
| DEC-16 | VALID | รับทราบเฉพาะใบอนุมัติแล้ว · ไม่บังคับ | FORM_SPEC | 05 BR-11 · EC-06 |
| DEC-17 | VALID | ถ้อยคำตรงตัว ("ชื่อตำแหน่งอังกฤษ") | FORM_SPEC | 05 BR-16 |

## §7.1 Locked Decisions (LD)
| LD | เรื่อง | ตัดสิน |
|---|---|---|
| LD-01 | ช่อง Acknowledged By | ไม่ใช่ขั้น DOA — เป็นการรับทราบหลังอนุมัติ (status acknowledged) · PDF ช่องท้ายสุด |
| LD-02 | ฉบับใช้งานต่อตำแหน่ง | 1 ฉบับ (approved/acknowledged) · ฉบับใหม่อนุมัติ → เดิม superseded (ไม่ลบ) |
| LD-03 | "ผู้ใต้บังคับบัญชา" ส่วนที่ 1 ซ้ำกับตาราง | เก็บเป็น computed (subordinate_summary) |
| LD-04 | ไม่อนุมัติ | กลับร่างเลขเดิม = BR-DOA-03 มาตรฐาน (DOA_BRIEF on_reject: back_to_draft) |
| LD-05 | role ผู้อนุมัติค่าเริ่ม | role-line-manager (relative role นอก DOA master 14 role) — รอยืนยัน OQ-02 |

## §7.2 Convention Deviations
- ไม่มีปุ่ม "ทำซ้ำ" (DEC-12) · ตาราง 4 คอลัมน์ PDF กว้างเท่ากัน (replica ห้าม style ใน body)

## §7.3 Open Questions → 00 §0.8 (OQ-01..05)

## §7.5 Deferred
- เชื่อม KPI กับ Performance · ส่ง JD ไป Recruit (ประกาศรับสมัคร) — รอบถัดไป
