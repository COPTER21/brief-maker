# 07_LOCKED_DECISIONS — F-TMP-006

## §7.0 Scope Lock — IMMUTABLE (= DECISIONS.lock REQ-TMP-006 · แทนใบเซ็นจนลูกค้าเซ็น · OQ-02)
> โหมดไม่เฝ้า — ทุก DEC (ยกเว้น VALID) เป็น **AI-DEFAULT** ต้องให้ลูกค้ายืนยันในใบลงนาม (newfeature-signoff-generator) ก่อน UAT
| DEC | หมวด | มติ | ที่มา | ใช้ที่ |
|---|---|---|---|---|
| DEC-01 | G1 | ไม่เปลี่ยนค่าในระบบ | AI-DEFAULT | html, thai-doc, brd, frd, tests, ntf-declaration |
| DEC-02 | G1 | ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง) | AI-DEFAULT | brd, frd |
| DEC-03 | G2 | ไม่มีการอนุมัติ (กระดาษไม่มีช่องลงชื่อผู้อนุมัติ · DOA 0 ขั้น · ไม่มี DOA_BRIEF) | AI-DEFAULT | html, frd |
| DEC-04 | G3 | ข้อละ 1 คะแนน (1 = Very Dissatisfied … 5 = Very Satisfied) · ครบ 10 ข้อ (3 กลุ่ม) จึงบันทึกผล · ร่างไม่ครบได้ · Month ค่าเริ่ม = เดือนปัจจุบัน · ไม่มีช่องวันที่ → วันที่บันทึก = เวลาระบบ | AI-DEFAULT | html, thai-doc, brd, frd, tests |
| DEC-05 | G4 | ไม่มีรายการซ้ำ (หัวข้อคงที่ 10 ข้อ) | AI-DEFAULT | html, thai-doc, frd |
| DEC-06 | G5 | ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง · ป้ายภาษาอังกฤษตามกระดาษ | AI-DEFAULT | html, thai-doc, brd, frd |
| DEC-07 | G6 | ไม่มีช่องลงชื่อ (กระดาษไม่มี) · ไม่ใช้ภาพลายมือชื่อ | AI-DEFAULT | thai-doc, html, doccfg-declaration, frd |
| DEC-08 | G8 | เจ้าของ · admin role (role-mgr-sales) เห็นทั้งหมด | AI-DEFAULT | html, frd, tests |
| DEC-09 | G9 | ออกเลขตอนบันทึกครั้งแรก · รหัส SEA | AI-DEFAULT | doccfg-declaration, html, frd |
| DEC-10 | G10 | แนบไฟล์ ✓ · ส่งออก CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗ | AI-DEFAULT | html, brd, frd, ntf-declaration |
| DEC-11 | VALID | 1 ข้อเลือกได้ 1 คะแนน · ครบ 10 ข้อจึงบันทึกผลได้ | FORM_SPEC | html, frd, tests |
| DEC-12 | VALID | ไม่มีช่องวันที่บนกระดาษ → วันที่บันทึก = เวลาระบบ (created_at) · ไม่เพิ่มช่อง | FORM_SPEC | html, frd, tests |
| DEC-13 | VALID | Month เลือกเดือน/ปี · ค่าเริ่ม = เดือนปัจจุบัน | FORM_SPEC | html, frd, tests |
| DEC-14 | VALID | ป้ายช่อง/หัวข้อ/แบบพิมพ์ภาษาอังกฤษตามกระดาษ · ปุ่ม/สถานะระบบภาษาไทย · สองภาษารอยืนยัน (OQ-08) | FORM_SPEC | html, thai-doc, frd |

## §7.1 การใช้มติใน FRD
- DEC-03 → 03 FN-03 (resolve 0 ขั้น · approver_role/approved_by/approval_chain ว่างใน API · TODO: DOA engine) · archetype Q-form คงโครง DOA-ENGINE-HOOK แต่ไม่มีปุ่มพิจารณา
- DEC-04/11/12/13 → 05 BR-01..04 · VR-04 · DEC-14 → 05 BR-11 · DEC-09 → 03 FN-02 · DEC-08 → 05 §5.3 · 06 §6.2
- G7 ยกเลิก (decisions.yaml · ไม่มี DEC แยกเพราะไม่มีการอนุมัติ) → 05 BR-07
