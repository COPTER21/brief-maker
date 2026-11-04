# 07_LOCKED_DECISIONS — F-HR-OSW แบบขออนุญาตออกปฏิบัติงานนอกสถานที่

> Audience: ทุกคน · สิ่งที่ห้ามเปลี่ยนโดยไม่ผ่าน DA

## §7.0 Scope Lock (Imported from BRD §3.4) — IMMUTABLE
Scope Lock Ref: **N/A — ยังไม่มีใบเซ็น** → ใช้มติ DA (`DECISIONS_F-HR-OSW_2026-10-05.md`) แทนจนกว่า Sign-off (OQ-01)
| ID | มติ | ผลใน pack |
|---|---|---|
| DEC-01 | อนุญาตแล้วไม่เปลี่ยนค่าในระบบ | ไม่มี write ไป feature อื่น |
| DEC-02 | ไม่ส่งต่อเวลาทำงาน/เบิกจ่าย/เงินเดือน | `osw.approved` ประกาศไว้แต่ไม่ยิง (02 §2.X) |
| DEC-03 | DOA dynamic ที่ DOA กลาง · ค่าเริ่ม 1 ขั้น ผู้บังคับบัญชาตรง · ไม่มีวงเงิน | FN-07/08/09 · ไม่ส่งยอดเงินให้ DOA |
| DEC-04 | เบี้ยเลี้ยงเฉพาะค้างคืน · อัตรานโยบาย snapshot · คืนอัตโนมัติ ปรับได้ · เกินช่วง = เตือน | BR-OSW-04..07 |
| DEC-05 | ช่วงวันที่ไม่จำกัด | ไม่มี max lines · PDF ≥5 แถว |
| DEC-06 | "เพื่อ" ช่องเดียว · ไม่มีหมายเหตุ | T_osw_line.purpose · ไม่มี note |
| DEC-07 | wizard 3 ขั้น · ทำซ้ำ = ปุ่มมาตรฐาน | 01 §1.0 P-02 |
| DEC-08 | PDF แบบ FM-HRM-02 (thai-doc FORM REPLICA) · ลายเซ็นแถวล่าง 1 ช่องต่อขั้น DOA | BR-OSW-17 · FN-11/12 |
| DEC-09 | ไม่ใช้ลายมือชื่อภาพ | sign date = "ส่งในระบบ / พิจารณาในระบบ วันที่ เวลา" |
| DEC-10 | ไม่อนุญาต = จบใบ · HR รับทราบ = เพิ่มขั้นที่ DOA | BR-OSW-10 · state machine |
ตรวจแล้ว: ไม่มี spec ใดใน pack ขัด DEC ✅

## §7.1 Locked Decisions (LD)
| LD | ตัดสิน | เหตุผล | ทางเลือกที่ไม่เลือก |
|---|---|---|---|
| LD-01 | อนุมัติผ่าน DOA engine แบบ sequential · feature เก็บ snapshot เอง + รับ callback | DOA = ทะเบียนกลาง · ตัดสินได้ทั้งในหน้า feature และ My Approval | feature เก็บสายเอง (ห้าม — doa-declaration) |
| LD-02 | ออกเลขตอนบันทึกครั้งแรก (ร่าง) | เอกสารภายใน non no-gap · ผู้ขอใช้เลขประสานงานก่อนส่ง (DOCCFG_BRIEF) | ออกเลขตอนส่ง |
| LD-03 `[AI-DEFAULT]` | rate snapshot ตอนสร้าง | ผู้ขอเห็นยอดตั้งแต่กรอก ไม่เปลี่ยนใต้เท้า (OQ-10) | snapshot ตอนส่ง |
| LD-04 | PDF = logic-less template + data contract ชุดเดียวทั้ง prototype และ server | parity ตรวจได้ทุก byte · ไม่มี logic ซ่อนในแบบพิมพ์ | สร้าง PDF ด้วยโค้ดเฉพาะ feature |
| LD-05 | Pattern Q แบบตัด "เลือกแหล่งที่มา" + "รายการสินค้า" | ไม่มีเอกสารต้นทาง/สินค้า | คง 5 ขั้น |
| LD-06 | ขั้นข้อมูลหลักใช้การ์ดต่อช่วง (วันที่ + เพื่อ + เวลาซ่อน) แทนตาราง | DA สั่งให้กรอกง่ายที่สุด | ตารางกรอกหลายคอลัมน์ (iron #104 "รายการย่อยเป็นตาราง") |
| LD-07 | ไม่มีวงเงิน DOA แม้มียอดเบี้ยเลี้ยง | มติ DA — ยอดไม่ใช่เกณฑ์ผู้อนุมัติ | tier ตามยอด |

## §7.2 Convention Deviations
| CD | Deviation | เหตุผล |
|---|---|---|
| CD-01 | Feature ID `F-HR-OSW` / scope ID `F-OSW-API-NN` แทน `F-XX` ตัวเลข | ยังไม่ได้เลข feature — แทนที่ทั้ง pack ตอนเริ่มพัฒนา (find/replace) |
| CD-02 | action endpoints `POST /{id}/submit · approve · reject · cancel` แทน PATCH status | state transition ที่มี guard/สิทธิ์ต่างกัน |
| CD-03 | audit.sh doc_archetype FAIL 9 ข้อ (B2 line editor · step "รายการสินค้า") | เอกสารไม่มีรายการสินค้า — Pattern Q §When to Use อนุญาต · ควรเพิ่มข้อยกเว้นใน audit.sh |
| CD-04 | iron #104 (รายการย่อยเป็นตาราง) — ใช้การ์ด | LD-06 |

## §7.3 Open Questions Promoted from 00_OVERVIEW
OQ-01 (Sign-off) · OQ-03 (ExpensePolicy owner) · OQ-06 (code OSW) — ต้องปิดก่อน dev handoff / deploy

## §7.4 Architecture Tradeoffs Acknowledged
- AT-01: snapshot chain ใน jsonb (อ่านง่าย/แสดงลายเซ็นตรง) แลกกับ query "รอฉัน" ที่ต้อง index jsonb หรือ materialize `current_assignee`
- AT-02: PDF approved_final เก็บครั้งเดียว (หลักฐาน) · ร่าง/รอ render สดทุกครั้ง (ไม่ stale)
- AT-03: store PDF ล้มไม่ rollback การอนุญาต → retry queue (การตัดสินของคนสำคัญกว่าไฟล์)

## §7.5 Decisions Deferred to Implementation
- เลือก renderer PDF (Chromium/Gotenberg) ตาม platform · ขนาด page/pool
- materialize `current_assignee` หรือไม่ ตาม perf test
- `[AI-DEFAULT]` retention (OQ-08)

## §7.6 References
BRD v1.0 · DECISIONS_F-HR-OSW_2026-10-05 · DOA_BRIEF v1.0 · DOCCFG_BRIEF v1.0 · MDOC_BRIEF_OSW · print-spec · HTML รอบ 4
