# Review Playbook — F-TMP-003 แบบฟอร์มการขอทำลายข้อมูล

วันที่จัดทำ: 11 พฤศจิกายน 2569  
วัตถุประสงค์: ตรวจ logic และการทำงานของระบบจริงหลังขึ้น Production โดยยึด FRD เป็นหลัก และใช้ business sense ตรวจความเสี่ยงที่ test เดิมอาจไม่ครอบคลุม  
สถานะเอกสารนี้: แผนตรวจ ไม่ใช่ผลรับรองผ่าน/ไม่ผ่าน

## 1. ข้อสรุปสำหรับผู้ตรวจ

อย่าเริ่มจากการไล่กดทุกหน้าจอซ้ำกับ tester เดิม ให้เริ่มจาก 5 เรื่องที่ถ้าผิดแล้วกระทบธุรกิจสูงสุด:

1. คนที่ไม่มีสิทธิ์ต้องดูหรือเปลี่ยนคำขอไม่ได้ แม้เปิด URL ตรงหรือยิง request เอง
2. สายอนุมัติต้องเรียงลำดับ ถูกคน และ freeze หลังส่ง แม้ตั้งค่า DOA เปลี่ยนภายหลัง
3. การไม่อนุมัติ ยกเลิก และส่งใหม่ ต้องรักษาเลขเดิม/ประวัติเดิม และไม่เปิดช่องให้ข้ามขั้น
4. การกด “บันทึกการทำลายแล้ว” ต้องทำได้เฉพาะ IT หลังอนุมัติครบ และต้องมีหลักฐานตรวจย้อนหลังได้
5. PDF, CSV, notification และ audit log ต้องสะท้อนข้อมูล/สถานะเดียวกับหน้าจอจริง

รอบนี้ไม่ควรรับรองว่า “ผ่าน” จากผล tester เดิม เพราะแพ็กต้นทางระบุเองว่า test หลายส่วนเป็น prototype/simulation และมีรายการที่ยังไม่ได้พิสูจน์บนระบบจริง

## 2. สิ่งที่พบจากการ review เอกสารก่อนทดสอบ

### 2.1 ประเด็นที่ต้องให้ PM/BA ยืนยันย้อนหลัง

| ประเด็น | หลักฐานในแพ็ก | ความเสี่ยง |
|---|---|---|
| DEC-01..11 เป็น AI-DEFAULT และระบุว่าต้องให้ลูกค้ายืนยันก่อน UAT | FRD 05, 07 และ BRD OQ-02 | ระบบอาจทำตรง FRD แต่ FRD ไม่ตรงมติธุรกิจจริง |
| ค่าเริ่มสายอนุมัติ 2 ขั้นยัง “รอยืนยัน” | DOA_BRIEF | ผู้อนุมัติผิดคนหรือผิดลำดับ |
| `role-mgr-it` และ `role-it-officer` ไม่อยู่ใน DOA contract ตอนจัดทำแพ็ก | FRD 00 และ DOA_BRIEF | resolve role ไม่ได้, เลือกคนผิด, หรือใช้สิทธิ์กว้างเกิน |
| ตำแหน่ง “เจ้าหน้าที่ IT” บนกระดาษยังมี OQ ว่าเป็นผู้ทำหลังอนุมัติหรือเป็นขั้นก่อนอนุมัติ | FRD 07 OQ-04 / BRD OQ-04 | flow Production อาจผิดเจตนาของแบบฟอร์มเดิม |
| “อนุมัติ” คือผู้จัดการ IT หรือเจ้าของข้อมูล/ผู้บริหารยังเป็น OQ | BRD OQ-05 | segregation of duties อาจไม่ถูกต้อง |
| รหัส `F-TMP-003` ระบุว่าเป็นรหัสชั่วคราว | FRD 00 / BRD OQ-05 | DOA, notification, document config อาจ wire ด้วยรหัสที่ไม่ใช่ production code |

คำแนะนำ: ขอหลักฐานสั้น ๆ จาก PM/BA เช่น sign-off, ticket หรือ minutes ที่ปิด OQ เหล่านี้ ถ้าไม่มี ให้บันทึกเป็น “Business decision not evidenced” แยกจาก bug ระบบ

### 2.2 ช่องว่างของ test เดิมที่ควรเก็บตก

- ไม่มี e2e_standard report ในแพ็ก และต้นทางระบุ NO-BROWSER
- UAT ฉบับคนตัดออก 11 เคส รวม notification จริง, stale, API failure, doc type ปิด, route ตรง และ PDF long text
- TC ระบุว่าข้าม EC-06 ผู้ขอไม่มีหัวหน้า/ผู้ขอเป็นผู้จัดการ IT และ EC-07 เปลี่ยน DOA ระหว่างรอ
- notification ใน test เดิมตรวจเพียงสถานะหน้าจอหรือใช้ simulation ไม่ได้ยืนยันว่าผู้รับจริงได้รับเพียงครั้งเดียว
- PDF เคยตรวจจาก HTML/prototype แต่แพ็กระบุว่าไม่ได้ render/compare ทางการบนเครื่องงาน
- ไม่พบ test ที่พิสูจน์ว่า audit table เป็น append-only หรือข้อมูลข้ามบริษัทไม่รั่ว

### 2.3 ความเสี่ยงทางธุรกิจที่ FRD ยังตอบไม่พอ

1. `done_note` ไม่บังคับ และ FRD ไม่บังคับแนบหลักฐานตอนทำลายจริง คน IT จึงอาจกด “ทำลายแล้ว” โดยไม่มีหลักฐานว่าทำอะไร ที่ไหน ด้วยวิธีใด หรือใครเป็นพยาน
2. FRD บอก “ห้ามแนบตัวข้อมูลที่จะทำลาย” แต่ไม่ได้ระบุกลไกป้องกัน/เตือน/ตรวจไฟล์ ผู้ใช้อาจแนบข้อมูลส่วนบุคคลหรือข้อมูลลับเข้าเอกสารคำขอ
3. ฟีเจอร์นี้ไม่ลบข้อมูลในระบบปลายทางอัตโนมัติ เป็นเพียง workflow และบันทึกผล ผู้ใช้ต้องไม่เข้าใจผิดว่ากดอนุมัติหรือกดทำลายแล้วเท่ากับข้อมูลถูกลบจริง
4. สถานะในเอกสารไม่ใช้คำเดียวกันทุกที่ (`pending`/`pending_approval`, `done`/`destroyed`, rejected file แต่ DB ไม่มี rejected) ต้องตรวจ integration จริงว่า mapping ไม่ทำ notification/audit/PDF พลาด
5. ไม่มี SLA, escalation, หรือการจัดการกรณี approver ลาออก/ถูกปิดบัญชีระหว่างรอ จึงอาจมีคำขอค้างถาวร

## 3. ขอบเขตการทดสอบที่ปลอดภัยบน Production

- ใช้ข้อมูลสมมติเท่านั้น และขึ้นต้นรายละเอียด/โปรแกรมด้วย `REVIEW-YYYYMMDD-<case>`
- ห้ามแนบข้อมูลจริงที่จะทำลาย, PII จริง, secret, export ลูกค้า หรือไฟล์ executable
- เตรียมบัญชีทดสอบอย่างน้อย 5 บทบาท: ผู้ร้องขอ, ผู้พิจารณาขั้น 1, ผู้พิจารณาขั้น 2, เจ้าหน้าที่ IT, บุคคลนอกสาย
- ให้ PM/BA และ IT รับรู้เลขเอกสารที่สร้างเพื่อ review เพราะ audit เป็น append-only และไม่ควรลบข้อมูล Production
- เคส fault injection เช่น API 500, stale race, ปิด doc type หรือแก้ DOA ให้ทำใน UAT/controlled tenant หากกระทบผู้ใช้ Production
- บันทึกเวลาไทย, เลขเอกสาร, actor, expected, actual, screenshot และ request/response ID ทุกเคสที่ผิด

## 4. ชุดข้อมูลขั้นต่ำ

| ชุด | ใช้ทดสอบ |
|---|---|
| D1 Happy path | รายละเอียดสั้น, เลือก data type 2 ค่า, เหตุผล 2 ค่า, วิธี 2 ค่า, ช่วงวันที่ปกติ |
| D2 Boundary | วันที่ถึงเท่ากับวันที่จาก และวันที่ถึงหลังวันที่ขอ |
| D3 Other | ติ๊ก “อื่น ๆ” ของเหตุผลและวิธีการ ทั้งว่าง/มีข้อความ |
| D4 Long text | detail หลายบรรทัด, program ยาว, other ยาว เพื่อทดสอบ PDF 1 หน้า |
| D5 Attachment | PDF/PNG ที่ไม่มีข้อมูลจริง, ไฟล์เกินขนาด, นามสกุลปลอม, .exe |
| D6 Role exception | ผู้ขอไม่มีหัวหน้า, ผู้ขอเป็น approver, approver ถูก disable ถ้าสภาพแวดล้อมรองรับ |

## 5. Test run หลัก — ทำตามลำดับ

### P0 — ต้องผ่านก่อนรับรอง

| ID | วิธีตรวจ | Expected ตาม FRD | หลักฐาน |
|---|---|---|---|
| P0-01 | ผู้ร้องขอสร้าง D1 แล้วบันทึกร่าง | ออกเลข DRITS ตอนบันทึกครั้งแรก, สถานะร่าง, ชื่อ/ตำแหน่ง/header ถูก snapshot | ภาพหน้าจอ + เลขเอกสาร |
| P0-02 | แก้ร่างแล้วบันทึกหลายครั้ง/กดปุ่มซ้ำเร็ว ๆ | ใช้เลขเดิม ไม่เกิดเอกสารซ้ำ ไม่ข้าม running ซ้ำจาก request เดียว | รายการเอกสาร + network log |
| P0-03 | ส่งอนุมัติ | resolve DOA ตาม Production config, ทุก slot มีคน, ผู้ขอเลือกตัวเองไม่ได้, status pending ขั้น 1 | modal + timeline |
| P0-04 | ผู้พิจารณาขั้น 2 เปิดใบก่อนขั้น 1 | ดูได้แต่ไม่มีสิทธิ์ตัดสิน; request ตัดสินต้องถูกปฏิเสธ | UI + status code |
| P0-05 | ขั้น 1 อนุมัติ แล้วขั้น 2 อนุมัติ | ทำตามลำดับ, timestamp/actor ถูก, ครบแล้ว status “รอทำลายข้อมูล” | timeline ก่อน/หลัง |
| P0-06 | เจ้าหน้าที่ IT กดบันทึกการทำลายแล้ว | ทำได้เฉพาะ status approved และ role IT; บันทึก performer/time; status done | detail + audit + PDF |
| P0-07 | ผู้ร้องขอ/approver/คนนอกลองกด destroyed ผ่าน UI และ request ตรง | ไม่มีปุ่ม และ backend ตอบ 403 NOT_IT_OFFICER/409 NOT_APPROVED ตามกรณี; state ไม่เปลี่ยน | response + state ก่อน/หลัง |
| P0-08 | คนนอกสายค้นหา/เปิด URL/เรียก API detail/PDF/attachment ของใบ | ไม่พบข้อมูล (404) และไม่รั่วชื่อ โปรแกรม รายละเอียด หรือไฟล์ | response/หน้า 404 |
| P0-09 | ผู้ร้องขอเปิดร่างของคนอื่นผ่าน URL/API | 404 NOT_FOUND; ร่างไม่อยู่ใน list/search/CSV | list + response |
| P0-10 | ผู้ใช้อยู่คนละ company/tenant ลองใช้ id หรือ doc_no เดียวกัน | ไม่เห็น detail, PDF, attachment, audit, CSV ของอีก tenant | response ทั้ง 5 ช่องทาง |
| P0-11 | ขั้น 2 ไม่อนุมัติพร้อมเหตุผล | กลับ draft, เลขเดิม, เหตุผล/ผู้ทำ/เวลาอยู่ใน audit, chain เดิมไม่ active | before/after + audit |
| P0-12 | ส่งใบ P0-11 ใหม่ | resolve DOA ใหม่และเริ่มขั้น 1; ประวัติรอบเก่ายังอยู่; ห้ามเริ่มต่อขั้น 2 | timeline/audit |
| P0-13 | เปลี่ยน DOA หลังส่งใบ A แล้วส่งใบ B | A ใช้ snapshot เก่า; B ใช้ config ใหม่; A ห้ามเปลี่ยนคน/จำนวนขั้น | เทียบ A/B |
| P0-14 | owner ยกเลิกใบรออนุมัติพร้อมเหตุผล | status cancelled, current pending step เป็น skipped, ตัดสินต่อไม่ได้ | timeline/audit |
| P0-15 | ลองยกเลิกใบ approved/done | ไม่มีปุ่มและ backend ปฏิเสธ; state ไม่เปลี่ยน | UI + response |
| P0-16 | ตรวจ notification จริง 3 event | ready_for_it ไป role IT, cancelled ไป current approver, destroyed ไป owner; ref เปิดใบถูก; ไม่ซ้ำ | กล่องผู้รับ + event/log id |
| P0-17 | ตรวจ audit ทั้ง lifecycle | create/update/submit/approve/reject/resubmit/cancel/done มี actor/time/note ครบ, เรียงถูก, แก้หรือลบย้อนหลังไม่ได้ | history tab + audit query โดยผู้มีสิทธิ์ |
| P0-18 | PDF draft/approved/done/rejected-history/DOA หลายขั้น | ข้อมูลตรงหน้าจอ, checkbox ตรง, ผู้ลงนาม/เวลา/ลำดับถูก, 1 หน้า A4, ไม่มี template token, draft มีคำว่าร่าง | PDF ที่ดาวน์โหลดจริง |

### P1 — validation, resilience และข้อมูลประกอบ

| ID | วิธีตรวจ | Expected |
|---|---|---|
| P1-01 | ส่งฟอร์มว่าง แล้วไล่เว้นแต่ละ required field | แสดงข้อความ VR-01..09 ที่ช่องถูกต้องและ backend ไม่รับข้อมูลไม่ครบ |
| P1-02 | period_to ก่อน period_from | บล็อกทั้ง UI และ API |
| P1-03 | period_to เท่ากับ period_from | บันทึกและส่งได้ |
| P1-04 | period_to หลัง req_date | เตือนแต่ส่งได้; warning ไม่กลายเป็น error |
| P1-05 | ติ๊ก other โดยไม่กรอก แล้วกรอก whitespace อย่างเดียว | บล็อก; เมื่อมีข้อความจริงจึงผ่าน |
| P1-06 | ส่ง array ว่าง/enum ปลอมผ่าน API | 422; ไม่บันทึกค่าที่ FRD ไม่รู้จัก |
| P1-07 | สร้าง/แก้/ส่งด้วยสองหน้าต่างพร้อมกัน | request เก่าตอบ 409 STALE; ไม่ทับข้อมูลใหม่และไม่ตัดสินซ้ำ |
| P1-08 | double-click submit/approve/reject/destroyed | transition และ notification เกิดครั้งเดียว; ไม่มี audit ซ้ำ |
| P1-09 | API submit/approve ล้มเหลวระหว่างทาง | transaction rollback; state, chain, PDF snapshot, notification ไม่ค้างครึ่งเดียว |
| P1-10 | doc type DRITS ถูกปิด | สร้างใหม่ไม่ได้ทั้ง UI/API แต่เอกสารเดิมยังดูได้ตามสิทธิ์ |
| P1-11 | ผู้ขอไม่มี line manager | slot ว่างและต้องเลือกผู้พิจารณาที่ถูกสิทธิ์; ห้ามส่งแบบไม่มีคน |
| P1-12 | ผู้ขอเป็นผู้จัดการ IT/มีหลาย role | ห้าม self-approve ทุกขั้น; ตรวจ separation of duties ตามมติ BA |
| P1-13 | approver ถูก disable/ย้ายหน่วยงานหลังส่ง | ใบเดิมไม่เปลี่ยน snapshot; มีวิธี operationally reassign/escalate หรือบันทึกว่า blocked |
| P1-14 | แนบไฟล์ที่รองรับแล้วลองเปิด/ดาวน์โหลดด้วยทุก role | เฉพาะ canSee เปิดได้; filename/content type ถูก; URL ไม่ public |
| P1-15 | แนบ .exe, file เกินขนาด, นามสกุลปลอม, zero-byte | 413/415 หรือข้อความตาม file policy; ไม่เกิด orphan file |
| P1-16 | แก้ไฟล์แนบหลังส่ง/หลังอนุมัติ | ต้องแก้ไม่ได้เพราะ API จำกัด owner+draft; audit ไม่สูญ |
| P1-17 | CSV ภายใต้แต่ละ role/tab/filter | มีเฉพาะแถวที่ role มองเห็น, filter ตรง, UTF-8 BOM, ไม่มีคอลัมน์ลับ/ข้อมูลข้าม tenant |
| P1-18 | ค่า text เริ่มด้วย `=`, `+`, `-`, `@` แล้ว export CSV | ต้องไม่เกิด spreadsheet formula execution เมื่อเปิดไฟล์ |
| P1-19 | search ด้วยเลข/ชื่อ/โปรแกรม/รายละเอียด และ pagination/sort | ผลตรงสิทธิ์, count ไม่รั่วจำนวนเอกสารที่มองไม่เห็น, ไม่ซ้ำ/ตกหล่นข้ามหน้า |
| P1-20 | เปลี่ยนชื่อ/ตำแหน่ง/โลโก้องค์กรหลังออกเลข | เอกสารเดิมใช้ snapshot เดิม; เอกสารใหม่ใช้ค่าปัจจุบัน |

### P2 — business usability ที่ไม่ควรปล่อยผ่านแม้ UI ถูกบอกว่าเสร็จแล้ว

| ID | คำถามที่ต้องพิสูจน์ | เกณฑ์พิจารณา |
|---|---|---|
| P2-01 | IT ใช้อะไรเป็นหลักฐานก่อนกด “ทำลายแล้ว” | ควรมี note/attachment/checklist ที่ audit ได้; ถ้าไม่มีให้เปิด business gap |
| P2-02 | ผู้ใช้เข้าใจหรือไม่ว่าระบบไม่ได้ลบข้อมูลปลายทาง | ต้องมีข้อความชัดในจุดอนุมัติ/ทำลาย ไม่ทำให้เข้าใจผิด |
| P2-03 | ใครรับผิดชอบตรวจว่าข้อมูลครบ retention และ legal hold แล้ว | ต้องมี owner/ขั้นตอนนอกระบบชัด หรือเพิ่ม rule ในอนาคต |
| P2-04 | คำขอค้างมี SLA/escalation หรือ dashboard ให้ IT ติดตามหรือไม่ | หากไม่มี ให้บันทึก operational risk ไม่ใช่ bug ตาม FRD |
| P2-05 | ผู้ใช้แนบข้อมูลจริงที่จะทำลายโดยผิดนโยบายได้ง่ายหรือไม่ | ควรมีคำเตือนชัดและ control ตาม data classification |
| P2-06 | “ยกเลิก”, “ไม่อนุมัติ”, “ทำลายแล้ว” ใช้ถ้อยคำที่คนเข้าใจตรงกันหรือไม่ | สถานะต้องไม่ทำให้เชื่อว่าข้อมูลถูกลบโดยระบบอัตโนมัติ |

## 6. เกณฑ์หยุดและระดับความรุนแรง

- Critical: ข้ามสิทธิ์/ข้ามสายอนุมัติ, ข้อมูลข้าม tenant, คนอื่นดาวน์โหลดไฟล์/PDF ได้, audit ถูกแก้/ลบ, state ผิดจนรับรองการทำลายเท็จ
- High: อนุมัติผิดลำดับ, document/notification ซ้ำ, reject/resubmit ใช้ chain ผิด, PDF/CSV/สถานะผิด, ทำลายแล้วโดย role หรือ state ผิด
- Medium: validation ผิดแต่มีทางเลี่ยง, notification หายแต่หน้าจอถูก, ประวัติไม่ครบ, snapshot ผิด
- Low: ข้อความ/ตำแหน่ง/ความสม่ำเสมอของ UI ที่ไม่เปลี่ยนผลธุรกิจ

หยุดการทดสอบทันทีถ้าพบ Critical หรือการทดสอบกำลังจะกระทบข้อมูล/ผู้ใช้ Production จริง

## 7. วิธีบันทึกผลต่อหนึ่งเคส

```text
Case ID:
วันที่/เวลา (Asia/Bangkok):
Environment/build:
Actor/role/company:
Doc no / request id:
Precondition:
Steps:
Expected (อ้าง FRD/BR/VR/EC):
Actual:
Result: Pass / Fail / Blocked / Not run
Severity (ถ้า Fail):
Evidence: screenshot, PDF, CSV, notification id, request id
หมายเหตุเรื่องข้อมูล Production:
```

ห้ามรวมหลาย rule เป็นผลเดียว เช่น “สร้าง-ส่ง-อนุมัติผ่าน” ต้องแยกผลอย่างน้อย create, submit, approve step 1, approve final, destroyed เพื่อให้รู้ว่าพังตรงไหน

## 8. เกณฑ์จบรอบ review

รับรองได้เมื่อ:

- P0 ทุกข้อผ่าน หรือมีข้อ Blocked ที่ PM/BA ยอมรับเป็นลายลักษณ์อักษร
- ไม่มี Critical/High ค้าง
- P1 เรื่อง permission, stale/idempotency, attachment, CSV และ snapshot ผ่าน
- PM/BA ให้หลักฐานปิด AI-DEFAULT/OQ ที่มีผลต่อ flow จริง
- ระบุสิ่งที่ไม่ได้ตรวจอย่างตรงไปตรงมา โดยเฉพาะ fault injection ที่ทำบน Production ไม่ได้
- ออกรายงานผลตรวจแยก Logic, UI, UX, Bug โดยไม่เติม Pass ให้เคสที่ไม่ได้รัน

## 9. ลำดับทำงานที่แนะนำ

1. ขอ sign-off/OQ closure และ production config ของ DOA/Document/Notification
2. ทำ P0-01 ถึง P0-10 ด้วยชุด happy path และสิทธิ์
3. ทำ reject/resubmit, DOA freeze, cancel, notification, audit และ PDF
4. ทำ P1 บน UAT/controlled tenant สำหรับ fault/race/config cases
5. สัมภาษณ์ BA/IT สั้น ๆ ตาม P2 แล้วแยก business gap ออกจาก bug
6. นำผลจริงมาสร้าง Feature Check Report รอบ 1; เคสที่ไม่รันต้องเป็น Not run ไม่ใช่ Pass
