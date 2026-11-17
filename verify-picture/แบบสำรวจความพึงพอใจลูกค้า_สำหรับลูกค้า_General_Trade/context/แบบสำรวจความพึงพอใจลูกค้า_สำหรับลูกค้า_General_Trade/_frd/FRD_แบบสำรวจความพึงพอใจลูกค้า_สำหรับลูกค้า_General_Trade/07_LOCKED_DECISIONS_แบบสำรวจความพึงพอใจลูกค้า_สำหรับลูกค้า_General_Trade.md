# 07_LOCKED_DECISIONS — F-TMP-001

## §7.0 Scope Lock — IMMUTABLE (= DECISIONS.lock REQ-TMP-001 · แทนใบเซ็นจนลูกค้าเซ็น · OQ-02)
> โหมดไม่เฝ้า — ทุก DEC (ยกเว้น VALID) เป็น **AI-DEFAULT** ต้องให้ลูกค้ายืนยันในใบลงนาม (newfeature-signoff-generator) ก่อน UAT
| DEC | หมวด | มติ | ที่มา | ใช้ที่ |
|---|---|---|---|---|
| DEC-01 | G1 | ไม่เปลี่ยนค่าในระบบ | AI-DEFAULT | html, thai-doc, brd, frd, tests, ntf-declaration |
| DEC-02 | G1 | ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง) | AI-DEFAULT | brd, frd |
| DEC-03 | G2 | ไม่มีการอนุมัติ (กระดาษไม่มีช่องลงชื่อผู้อนุมัติ · DOA 0 ขั้น · ไม่มี DOA_BRIEF) | AI-DEFAULT | html, frd |
| DEC-04 | G3 | คะแนนข้อละ 1 ค่า (5–1) · ครบ 16 ข้อจึงบันทึกผล · ร่างไม่ครบได้ · ประจำเดือนค่าเริ่มจากวันที่ · วันที่นอกเดือน = เตือน | AI-DEFAULT | html, thai-doc, brd, frd, tests |
| DEC-05 | G4 | ไม่มีรายการซ้ำ (หัวข้อคงที่ 16 ข้อ) | AI-DEFAULT | html, thai-doc, frd |
| DEC-06 | G5 | ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง | AI-DEFAULT | html, thai-doc, brd, frd |
| DEC-07 | G6 | ไม่มีช่องลงชื่อ (กระดาษไม่มี) · ไม่ใช้ภาพลายมือชื่อ | AI-DEFAULT | thai-doc, html, doccfg-declaration, frd |
| DEC-08 | G8 | เจ้าของ · admin role (role-mgr-sales) เห็นทั้งหมด | AI-DEFAULT | html, frd, tests |
| DEC-09 | G9 | ออกเลขตอนบันทึกครั้งแรก · รหัส CSG | AI-DEFAULT | doccfg-declaration, html, frd |
| DEC-10 | G10 | แนบไฟล์ ✓ · ส่งออก CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗ | AI-DEFAULT | html, brd, frd, ntf-declaration |
| DEC-11 | VALID | ถ้อยคำ "การส่งมอบตามเวลาที่ได้นัดหมายไว้" (แก้ "ไว้่") | FORM_SPEC | html, frd, tests |
| DEC-12 | VALID | แบบพิมพ์แสดงช่องคะแนน 5 4 3 2 1 ครบในหน้าเดียวกับหัวข้อ | FORM_SPEC | html, frd, tests |
| DEC-13 | VALID | ประจำเดือนบังคับ · ค่าเริ่ม = เดือนของวันที่ · วันที่นอกเดือน = เตือน | FORM_SPEC | html, frd, tests |

## §7.1 การใช้มติใน FRD
- DEC-03 → 03 FN-03 (resolve 0 ขั้น) · 04 ไม่มีคอลัมน์สายพิจารณา · archetype Q-form คงโครง DOA-ENGINE-HOOK แต่ไม่มีปุ่มพิจารณา (OQ-07)
- DEC-04/13 → 05 BR-01..04 · VR-04 · DEC-11/12 → 05 BR-11/12 · DEC-09 → 03 FN-02 · DEC-08 → 05 §5.3 · 06 §6.2
- G7 ยกเลิก (decisions.yaml · ไม่มี DEC แยกเพราะไม่มีการอนุมัติ) → 05 BR-07
