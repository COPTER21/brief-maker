# 07_LOCKED_DECISIONS — F-TMP-002

## §7.0 Scope Lock — IMMUTABLE (= DECISIONS.lock REQ-TMP-002 · แทนใบเซ็นจนลูกค้าเซ็น · OQ-01)
> โหมดไม่เฝ้า — มติ AI-DEFAULT ทุกหมวด ต้องให้ลูกค้ายืนยันในใบลงนาม (newfeature-signoff-generator) ก่อน UAT

| DEC | หมวด | มติ | ที่มา | ใช้ใน FRD |
|---|---|---|---|---|
| DEC-01 | G1 | ไม่เปลี่ยนค่าในระบบ | AI-DEFAULT | 05 BR-10 |
| DEC-02 | G1 | ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้แต่ไม่มี downstream) | AI-DEFAULT | 02 §2.X · 05 BR-10 |
| DEC-03 | G2 | ไม่มีการอนุมัติ — DOA กลางค่าเริ่ม 0 ขั้น · รองรับ N ขั้น | AI-DEFAULT | 03 FN-04 · 05 BR-08 |
| DEC-04 | G3 | คำนวณอายุตัว/อายุงาน ปรับได้ · กฎบล็อก · HR สร้างแทนได้ | AI-DEFAULT | 03 FN-02 · 05 BR-01 |
| DEC-05 | G4 | ปัจจัยที่เลือก ไม่จำกัด (≤21 ตามกระดาษ) | AI-DEFAULT | 05 BR-04 · EC-04 |
| DEC-06 | G4 | ข้อเสนอแนะ ไม่จำกัดแถว · PDF ≥5 แถว | AI-DEFAULT | 05 BR-05 · EC-05 |
| DEC-07 | G5 | ช่องตรงกระดาษ 1:1 ไม่เพิ่มช่อง | AI-DEFAULT | 05 BR-13/14 · 01 §1.0 |
| DEC-08 | G6 | ลงชื่อแถวล่าง 1 ช่องต่อขั้น DOA · ไม่ใช้ภาพ | AI-DEFAULT | 05 BR-09 · 03 FN-08 |
| DEC-09 | G8 | เห็น: เจ้าของ · admin role (role-mgr-hr) ทั้งหมด · ไม่มีผู้อนุมัติ | AI-DEFAULT | 05 §5.3 · 03 FN-10 |
| DEC-10 | G9 | เลข EXI ออกตอนบันทึกครั้งแรก | AI-DEFAULT | 03 FN-03 · 05 BR-07 |
| DEC-11 | G10 | แนบไฟล์ ✓ · CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗ | AI-DEFAULT | 05 BR-12 |
| DEC-12 | VALID | "โปรดกรอก" (แก้คำสะกด) | FORM_SPEC | 05 BR-13 |
| DEC-13 | VALID | ✓ แทน "P" (Wingdings) | FORM_SPEC | 05 BR-13 |
| DEC-14 | VALID | ลักษณะพ้นงานเลือก 1 · ข้อ 5 เฉพาะครบสัญญา (บล็อก) | FORM_SPEC | 05 BR-02 · VR-02..04 |
| DEC-15 | VALID | rank ≥1 ไม่ซ้ำ ต่อเนื่อง · ≥1 ปัจจัย (บล็อก) | FORM_SPEC | 05 BR-04 · VR-07/08 |
| DEC-16 | VALID | ส่วนที่ 2 ครบ 26 ข้อ ข้อละ 1 ระดับ | FORM_SPEC | 05 BR-03 · VR-06 |
| DEC-17 | VALID | ผู้บังคับบัญชาห้ามเห็นใบ — เจ้าของ + HR เท่านั้น | FORM_SPEC | 05 BR-06 · 06 TC-D01/D02 |

## §7.1 Locked Decisions (LD)
| LD | เรื่อง | ตัดสิน |
|---|---|---|
| LD-01 | status หลังส่งเมื่อ 0 ขั้น | `submitted` (ไม่ใช่ approved) — ไม่มีผู้อนุมัติจึงไม่เรียกว่าอนุมัติ |
| LD-02 | owner vs ผู้ให้ข้อมูล | owner_id = ผู้สร้าง (แก้ร่าง/ส่ง) · employee_id = ผู้ให้ข้อมูล (ดู/ยกเลิก) |
| LD-03 | ส่วนที่ 3 บนกระดาษเขียนเลขในกล่อง | ระบบเก็บ {reason, rank} · UI กดตามลำดับ · PDF แสดง [n] |
| LD-04 | ส่งกลับ (ถ้าตั้ง DOA) | กลับร่างเลขเดิม = BR-DOA-03 มาตรฐาน (ไม่ใช่ข้อยกเว้น) |

## §7.2 Convention Deviations
- ไม่มี DOA_BRIEF (doa-declaration ไม่ประกาศ feature ที่ไม่มีอนุมัติ) แต่ prototype/FRD รองรับ N ขั้นผ่าน DOA กลาง (e2e S8)
- ไม่มีปุ่ม "ทำซ้ำ" (DEC-11)

## §7.3 Open Questions → 00 §0.8 (OQ-01..05)

## §7.5 Deferred
- รายงานวิเคราะห์ภาพรวม Exit Interview (dashboard) — รอบถัดไป (ใช้ CSV แทน)
