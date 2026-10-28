# 07_LOCKED_DECISIONS — F-TMP-003

## §7.0 DECISIONS.lock (immutable — ที่มา prebrief-to-devpack v2 · unattended)
> ทุกข้อ AI-DEFAULT ต้องให้ลูกค้ายืนยันในใบลงนาม (newfeature-signoff-generator) ก่อน UAT — OQ-01
| DEC | หมวด | มติ | ที่มา | ใช้ใน FRD |
|---|---|---|---|---|
| DEC-01 | G1 | อนุมัติแล้วไม่เปลี่ยนค่าในระบบ | AI-DEFAULT | 00 §0.3 |
| DEC-02 | G1 | ไม่ส่งต่อระบบอื่นรอบนี้ | AI-DEFAULT | 00 §0.5 |
| DEC-03 | G2 | DOA dynamic · ค่าเริ่ม 1 ขั้น role-line-manager · ไม่มีวงเงิน | AI-DEFAULT | 03 FN-04/05 · 05 BR-04 |
| DEC-04 | G3 | ชื่อบริษัทจาก Organization · host/ฝ่าย/ผู้บังคับบัญชาจากผังองค์กร · ไม่อนุมัติต้องมีความเห็น · วันที่ลงนามก่อน = เตือน · ผู้ขอ = host | AI-DEFAULT | 03 FN-01/02 · 05 BR-02/03/08 |
| DEC-05 | G4 | ไม่มีรายการซ้ำ (ไม่มีผล) | AI-DEFAULT | — |
| DEC-06 | G5 | ช่องตรงกระดาษ 1:1 | AI-DEFAULT | 01 §1.2 · 05 BR-01 |
| DEC-07 | G6 | ลงชื่อแถวล่าง 1 ช่องต่อขั้น DOA · ข้อความแทนลายมือ | AI-DEFAULT | 03 FN-07 · 05 BR-DOA |
| DEC-08 | G7 | ไม่อนุมัติ = กลับร่างเลขเดิม · ยกเลิก owner/admin ที่ draft/pending · เหตุผลบังคับ | AI-DEFAULT | 03 FN-05/06 · 05 §5.2 |
| DEC-09 | G8 | เห็น: เจ้าของ · ผู้อนุมัติหลังส่ง · role-mgr-hr ทั้งหมด | AI-DEFAULT | 05 §5.3 · 06 §6.2 |
| DEC-10 | G9 | เลข VAR ออกตอนบันทึกครั้งแรก | AI-DEFAULT | 03 FN-03 |
| DEC-11 | G10 | แนบ ✓ CSV ✓ ทำซ้ำ ✗ ประกาศ ✗ | AI-DEFAULT | 05 BR-12 |
| DEC-12 | VALID | ชื่อผู้รับการติดต่อ = พนักงานที่ติดต่อ | FORM_SPEC | 05 BR-02 · VR-05 |
| DEC-13 | VALID | ชื่อบริษัท 2 จุดค่าเดียว | FORM_SPEC | 05 BR-03 |
| DEC-14 | VALID | ไม่อนุมัติต้องมีความเห็น (บล็อก) | FORM_SPEC | 05 VR-07 · EC-04 |
| DEC-15 | VALID | วันที่ลงนาม ≥ วันที่เข้าพื้นที่ (เตือน) | FORM_SPEC | 05 VR-08 · EC-03 |

## §7.1 Locked Design Decisions
| LD | เรื่อง | มติ |
|---|---|---|
| LD-01 | ผู้มาติดต่อไม่มีบัญชี | host เป็นผู้บันทึก/ส่ง · ผู้มาติดต่อเซ็นมือบนแบบพิมพ์ |
| LD-02 | ☐ อนุมัติ/ไม่อนุมัติ ในกรอบเจ้าหน้าที่ | = ผลพิจารณาสุดท้ายของสาย · ช่องลงชื่อแถวล่างแสดงคำตัดสินต่อขั้น |
| LD-03 | role-line-manager | resolve จาก line_manager ของ host (ไม่ใช่ของผู้บันทึก) |
| LD-04 | CSV | ไม่ส่งออก visitor_phone (PDPA) |
