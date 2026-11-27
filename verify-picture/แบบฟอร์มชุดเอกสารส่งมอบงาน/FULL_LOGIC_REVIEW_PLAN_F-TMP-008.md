# Full Logic Review Plan — F-TMP-008 แบบฟอร์มชุดเอกสารส่งมอบงาน

> เป้าหมาย: ตรวจเก็บตกระบบที่ขึ้น Production แล้ว โดยยึด FRD เป็นเกณฑ์ตัดสินหลัก และใช้ business sense เพิ่มเฉพาะการหา defect/risk ที่ FRD อาจไม่ได้เขียนไว้
>
> เอกสารนี้เป็นแผนทดสอบ ไม่ใช่ผลรับรอง เนื่องจากยังไม่ได้รับ URL, บัญชีผู้ใช้, build/version และหลักฐานจากระบบ Production

## 1. สรุปสำหรับผู้ตรวจ

ฟีเจอร์นี้ไม่ควร review ด้วยการกรอกฟอร์มหนึ่งใบแล้วกดอนุมัติจนจบเท่านั้น จุดเสี่ยงจริงอยู่ที่ความสัมพันธ์ของข้อมูลในแต่ละแถว, การ freeze/resolve สายอนุมัติ, การกันสิทธิ์ทั้ง UI และ API, การคงเลข/ประวัติเมื่อส่งกลับ, PDF ที่สร้างจริงหลังอนุมัติ, notification และการชนกันของหลายคำสั่ง

ลำดับที่แนะนำ:

1. **P0 — ต้องผ่านก่อนรับรอง:** validation สำคัญ, สิทธิ์, state transition, ส่งกลับ/ยกเลิก, ป้องกัน approve ซ้ำ, PDF final, DOA จริง
2. **P1 — ต้องตรวจให้ครบ:** เลขเอกสาร, audit, notification, attachment, CSV/filter, ข้อมูลยาว/หลายแถว
3. **P2 — exploratory:** double click, stale tab, network retry, CSV injection, boundary date/time, production configuration drift

## 2. เกณฑ์ตัดสินและขอบเขต

### 2.1 Source of truth

- ใช้ FRD `00_OVERVIEW`, `02_API`, `03_LOGIC`, `04_DB`, `05_RULES`, `06_TESTS`, `07_LOCKED_DECISIONS` เป็นเกณฑ์ Pass/Fail
- ใช้ declaration ของ DOA, DOCCFG, NTF เพื่อทดสอบ integration/configuration จริง
- BRD, prototype และ test case เดิมใช้ช่วยทำความเข้าใจ แต่ไม่ใช้ล้ม FRD
- ถ้า behavior ต่างจาก FRD: ลงเป็น defect หรือ spec conflict ห้ามตีความว่า “production ทำแบบนี้อยู่แล้วจึงถูก”
- เคส business-sense ที่ FRD ไม่ได้ระบุ ให้ลงเป็น `Observation/Risk` ก่อน ไม่ตัดสิน Fail จน PM/BA ยืนยัน

### 2.2 สิ่งที่ไม่ควรสรุปจากหลักฐานเดิม

- Test case เดิม 42 เคสเขียนให้รันกับ `feature.html` ซึ่งเป็น prototype ไม่ใช่หลักฐานของ Production
- DevPack ระบุ `NO-BROWSER`, ไม่มี e2e_standard report และยังไม่ได้ render PDF/UAT ในรอบสร้างเอกสาร
- QA audit ตัดเคส API fail, DOA หลังบ้าน, doc type ปิด และ backend verification บางส่วนออกจากเอกสารคน
- ดังนั้นต้องตรวจของจริงซ้ำเฉพาะ logic/integration แม้ layout จะได้รับการรับรองแล้ว

## 3. จุดขัดแย้ง/จุดเสี่ยงที่ต้องยืนยันก่อนรับรอง

| ID | สิ่งที่พบในเอกสาร | สิ่งที่ต้องเช็กบน Production | การจัดการ |
|---|---|---|---|
| GAP-01 | DOA brief ยังระบุ `wire_status: pending` และ role/จำนวนขั้นเป็น default รอยืนยัน | DOA entry ของ `F-TMP-008` ถูก wire จริง, role ถูกฝ่าย, ผู้จัดทำไม่อนุมัติตัวเอง | ถ้ายัง mock/hardcode หรือ role ผิด = Critical |
| GAP-02 | FRD ใช้สถานะ `pending` แต่ DOA/NTF บางจุดใช้ `pending_approval` | ค่า state/event mapping จริงต้องไม่ทำให้ notification หรือ permission หลุด | ถ้า transition/event ไม่ทำงาน = High/Critical ตามผลกระทบ |
| GAP-03 | Overview ยังแสดง OQ-03/OQ-04/OQ-06 แม้สถานะบอก Ready หลังปิด OQ | ยืนยัน role id ของ approver/admin และ feature/doc code ที่ deploy จริง | บันทึกเป็น spec/config conflict หากยังไม่ปิด |
| GAP-04 | FRD กำหนด optimistic lock และ idempotency ทุก write | ตรวจ retry/double click/stale tab แล้วไม่สร้างเลขซ้ำ ไม่ตัดสินซ้ำ | ผลเงิน/เลข/สถานะซ้ำ = High |
| GAP-05 | Attachment API ไม่เขียน state restriction ชัด แต่ state machine บอก approved ล็อก | ลองเพิ่ม/ลบไฟล์หลัง approved/cancelled | ถ้าแก้สาระเอกสาร final ได้ = High |

## 4. Test accounts และข้อมูลที่ต้องเตรียม

ต้องมีอย่างน้อย 6 บัญชีที่เป็นคนละ user จริง:

| Persona | ใช้ทดสอบ |
|---|---|
| Owner A | สร้าง/แก้/ส่ง/ยกเลิกใบตัวเอง |
| Owner B | ทดสอบร่างของผู้อื่นและ data isolation |
| Approver Step 1 | ตรวจสอบแล้ว/ส่งกลับ |
| Approver Step 2 | รับทราบ/ส่งกลับ |
| Admin ฝ่ายบริหารการลงทุน | เห็นทุกใบและยกเลิกตามสิทธิ์ |
| Outsider | ไม่อยู่ในสาย/ไม่ใช่เจ้าของ ทดสอบ deny |

ข้อมูลทดสอบขั้นต่ำ:

- ใบครบถ้วน 1 แถว, 2 แถว และ 16 แถว
- ใบมีเงื่อนไขที่มี due date หลายวัน เพื่อเช็ก `earliest_due`
- ใบยังไม่รับมอบ
- ไฟล์ PDF/DOC/XLS/รูปที่ถูกชนิด, ไฟล์ผิดชนิด, ไฟล์ต่ำกว่าและเกิน 20 MB
- DOA 2 ขั้นตาม production และ test configuration 1/6 ขั้นถ้ามี environment ที่ปรับได้
- เปิด DevTools Network หรือมี API client เพื่อยืนยัน status code/payload; การซ่อนปุ่มอย่างเดียวไม่พอ

> บน Production ให้ใช้ชื่อโครงการขึ้นต้น `REVIEW-F-TMP-008-YYYYMMDD-` และขออนุมัติ PM ก่อนสร้าง/ยกเลิกข้อมูลทดสอบ ห้ามเปลี่ยน DOA หรือ Document Configuration กลางบน Production เพื่อทดสอบ edge case

## 5. P0 — Core business logic ที่ต้องผ่านทั้งหมด

### R01 — สร้างร่างและเลขเอกสาร

1. Owner A สร้างใบครบถ้วน 1 แถว แล้วบันทึกร่างครั้งแรก
2. ตรวจว่าได้เลขจากรูปแบบ IVMF ของ Production เพียงหนึ่งเลข
3. แก้และบันทึกซ้ำหลายครั้ง เลขต้องไม่เปลี่ยน
4. เปิดสองแท็บแล้วกดสร้าง/บันทึกเกือบพร้อมกัน ตรวจว่าแต่ละใบเลขไม่ซ้ำ
5. กดปุ่มบันทึกซ้ำเร็ว ๆ หรือ retry request เดิมด้วย Idempotency-Key เดิม

ผ่านเมื่อ: ไม่เกิดใบ/เลขซ้ำ, เลขไม่เปลี่ยนหลังแก้, audit ระบุผู้สร้างถูกคน

### R02 — Validation รายแถวและผลรับมอบ

ทดสอบทุก combination สำคัญ:

| ได้รับแล้ว | ความครบถ้วน | Expected |
|---|---|---|
| ได้รับ | ครบถ้วน | ไม่บังคับ issue/fix owner/due date |
| ได้รับ | ไม่ครบถ้วน | บังคับทั้ง 3 ช่อง |
| ได้รับ | ต้องตรวจสอบเพิ่มเติม | บังคับทั้ง 3 ช่อง |
| ไม่ได้รับ | พยายามเลือกครบถ้วน | UI ต้องเปลี่ยน/ปิดตัวเลือก และ API ต้อง 422 |
| ไม่ได้รับ | ไม่ครบถ้วน | บังคับทั้ง 3 ช่อง |

ตรวจเพิ่ม:

- due date ก่อนวันรับมอบต้องบล็อก; วันเดียวกันต้องผ่าน
- ลบแถวกลางแล้ว `seq` ต้องรันใหม่ 1..N และผู้ใช้แก้ seq ไม่ได้
- ไม่มีรายการเอกสารต้องบล็อกทั้งบันทึก/ส่งตาม BR-09
- `รับมอบครบถ้วน` ต้องผ่านเฉพาะเมื่อทุกแถวได้รับ+ครบถ้วน
- `รับมอบแบบมีเงื่อนไข` ต้องบังคับ open issues และ follow-up schedule
- `ยังไม่รับมอบ` ต้องบังคับหมายเหตุฝ่ายบริหารการลงทุน
- ทุกแถวครบแต่เลือกมีเงื่อนไข: ต้องเตือนแต่ยังส่งได้
- เวลาผิดรูปแบบ เช่น 25:00 ต้องถูกปฏิเสธทั้ง UI และ API

### R03 — ส่งอนุมัติและ snapshot DOA

1. ส่งใบจาก draft ตรวจจำนวน slot และ role จาก DOA จริง ไม่ใช่ค่าคงที่ในหน้า
2. Owner ต้องไม่ปรากฏ/เลือกตัวเองไม่ได้; ยิง API โดยใส่ owner ต้องได้ 422
3. ไม่เลือก assignee ให้ครบทุกขั้นต้องส่งไม่ได้
4. หลังส่ง เปลี่ยน DOA กลางใน environment ที่ปลอดภัย หรือใช้หลักฐาน config revision แล้วตรวจว่าใบเดิมยังใช้ chain snapshot เดิม
5. ใบใหม่หลัง config เปลี่ยนต้องใช้ chain ใหม่
6. ผู้พิจารณาขั้น 2 เห็นใบได้ แต่ยังไม่มีสิทธิ์ตัดสินก่อนขั้น 1

ผ่านเมื่อ: chain ถูก resolve จริง, freeze ต่อใบ, ไม่มี self-approval และไม่มีการข้ามขั้น

### R04 — Approve sequential และ final lock

1. Step 1 กด “ตรวจสอบแล้ว” สถานะย่อยต้องเลื่อนไป Step 2 เพียงครั้งเดียว
2. Step 2 กด “รับทราบ” สถานะรวมเป็น approved
3. หลัง approved ลองแก้ header, item, attachment, cancel และยิง API เดิมโดยตรง
4. ตรวจ final PDF ถูกเก็บหนึ่งฉบับใน `approved_final`
5. เปิดใบด้วย Owner/Approver/Admin ตรวจข้อมูลและ chain ตรงกัน

ผ่านเมื่อ: approve ตามลำดับ, final action ครั้งเดียว, approved ถูกล็อกทุกช่องทาง, final PDF เก็บสำเร็จ

### R05 — ส่งกลับ แก้ และส่งใหม่

1. Step 1 และ Step 2 ทดสอบส่งกลับแยกคนละใบ
2. ไม่ใส่เหตุผลต้องบล็อก; ใส่เหตุผลแล้วกลับ draft
3. เลขเอกสารเดิม, ข้อความเหตุผล/คน/เวลาแสดงถูกต้อง, chain รอบเดิมอยู่ใน audit
4. Owner แก้ข้อมูลแล้วส่งใหม่ ต้อง resolve chain ใหม่ตาม DOA ปัจจุบัน
5. Approver รอบเก่าที่ไม่อยู่ chain ใหม่ต้องตัดสินไม่ได้

ผ่านเมื่อ: ไม่เกิดเลขใหม่, audit ไม่หาย, chain ใหม่ไม่ปน chain เก่า

### R06 — ยกเลิกและ race condition

1. Owner ยกเลิก draft และ pending ได้เมื่อมีเหตุผล
2. Admin ยกเลิก draft/pending ได้; Outsider ทำไม่ได้
3. Approved/cancelled ยกเลิกซ้ำไม่ได้
4. เปิดสอง session: Approver กด approve ขณะ Owner กดยกเลิกเกือบพร้อมกัน
5. Request ที่มาทีหลังต้องได้ 409 STALE/NOT_CANCELLABLE และเหลือ final state เดียว

ผ่านเมื่อ: ไม่มี state กึ่งกลาง, ไม่มีทั้ง approved และ cancelled พร้อมกัน, audit เรียงเหตุการณ์ถูกต้อง

### R07 — Permission/RLS ต้องตรวจทั้ง UI และ API

| Actor/สถานะ | Expected |
|---|---|
| Owner B เปิด URL/API draft ของ Owner A | 404 ไม่เปิดเผยว่ามีเอกสาร |
| Outsider เปิดใบ pending/approved ที่ไม่เกี่ยวข้อง | 404 |
| คนใน chain แต่ไม่ใช่ current step ยิง decide | 403 |
| Outsider ยิง cancel/edit/attachment | 403/404 ตาม contract |
| Approver ลองแก้ body ของใบ | ปฏิเสธ |
| Admin ดูทุกใบ | เห็นตาม admin role จริง แต่ไม่มีสิทธิ์ approve แทนถ้าไม่ใช่ assignee |

ห้ามให้ Pass จากการ “ไม่เห็นปุ่ม” เท่านั้น ต้องยิง direct route/API ด้วย

### R08 — PDF final ที่ใช้เป็นเอกสารธุรกิจ

ตรวจ PDF จาก server ไม่ใช่เฉพาะ preview HTML:

- 2 หน้า, หน้า 1/2 และ 2/2, form code `FM-IVM-06`, revision จาก Document Configuration
- ปี พ.ศ./วัน/เวลาและ timezone Asia/Bangkok ถูกต้อง
- รายการอย่างน้อย 12 แถว; 16 แถวไม่ตัดข้อความ/ไม่หาย/หัวตารางซ้ำตามแบบ
- ลำดับแถวตรงข้อมูลจริง; แถวว่างไม่กลายเป็นข้อมูลจริง
- ลายเซ็นเป็นผู้จัดทำ + 1 แถวต่อ DOA step, คำ “ตรวจสอบแล้ว/รับทราบ” ตรง role
- rejected/returned ต้องไม่แสดงว่า approved
- company header/logo เป็น snapshot ณ ออกเลข ไม่เปลี่ยนตาม master ภายหลัง
- PDF final ที่ดาวน์โหลดซ้ำต้องเป็นข้อมูลชุด approved ไม่ใช่ draft ล่าสุดจาก client

## 6. P1 — Integration และความครบถ้วนเชิงธุรกิจ

### R09 — Notification

- pending → cancelled: ส่ง `ivmf_cancelled` ให้ current approver คนเดียว ข้อความมี doc no, actor, reason
- approved แบบ conditional/not accepted: ส่ง `ivmf_handover_followup` ให้ requester + admin role
- `pending_count` นับเฉพาะแถวค้าง; `earliest_due` เป็นวันที่เร็วสุดจริง
- approved แบบ full ต้องไม่ยิง follow-up
- ต้องไม่ยิง `ivmf.approved` และไม่ยิง DOA pending/result ซ้ำกับ engine
- retry/refresh ต้องไม่สร้าง notification ซ้ำ

### R10 — Audit trail และ snapshot

ตรวจทุก write: create, edit, submit, approve แต่ละขั้น, return, resubmit, cancel, attachment add/delete

ผ่านเมื่อ: actor/time/action/before-after ถูกต้อง, audit append-only, ผู้ใช้ทั่วไปแก้/ลบไม่ได้, เหตุผลส่งกลับ/ยกเลิกไม่หาย, ชื่อ/ตำแหน่งผู้จัดทำและ header เป็น snapshot

### R11 — Attachment

- รองรับ PDF/DOC/XLS/รูปตาม policy; ชนิดอื่นและไฟล์ >20 MB ต้องปฏิเสธฝั่ง server
- ลบ/เพิ่มไฟล์ใน draft ได้ตามสิทธิ์
- URL ไฟล์ต้องตรวจสิทธิ์ ไม่แชร์ข้าม user/tenant โดยเดา URL
- ชื่อไฟล์ไทย, ชื่อยาว, ชื่อซ้ำต้องไม่ทำไฟล์ทับกัน
- หลัง submit/approved/cancelled ต้องเป็นไปตาม lock ของเอกสาร; ถ้า FRD/implementation ไม่ตรงให้ยก spec question

### R12 — List, filter และ CSV

- จำนวนรายการและ pagination ตรงข้อมูลจริงหลังสร้าง/เปลี่ยนสถานะ
- filter status/result/search ใช้ร่วมกันได้และ reset ถูก
- `mine_to_act` แสดงเฉพาะ current assignee
- CSV ต้องใช้ filter และ permission ชุดเดียวกับหน้ารายการ
- CSV ต้องไม่รวม draft ของคนอื่น/ข้อมูล tenant อื่น
- ภาษาไทยเปิดใน Excel ไม่เพี้ยน; วันเวลา/ผล/สถานะตรงจอ

### R13 — Production configuration

- Document type `IVMF` active, numbering format/reset scope ตรงค่าที่อนุมัติ
- ปิด doc type ใน environment ทดสอบแล้วสร้างไม่ได้และไม่กินเลข
- DOA role IDs และ admin role ID เป็นค่าจริง ไม่ใช่ mock/default
- notification event catalog มีทั้งสอง event และ template variables ครบ
- storage เก็บ approved_final ได้และ retrieval ไม่คืนไฟล์ผิด version

## 7. P2 — Business-sense exploratory tests

ข้อเหล่านี้ใช้หา risk เพิ่ม ไม่ควรตัดสิน Fail ถ้า FRD ไม่รองรับโดยไม่ถาม PM/BA:

- เปิดแก้ใบเดียวกันสองแท็บ แท็บเก่าบันทึกทีหลังต้องได้ 409 STALE และไม่ทับข้อมูลใหม่
- network หลุดหลังคลิก submit/approve แล้วผู้ใช้กดซ้ำ: ต้องตรวจสถานะจริงและไม่ทำ action ซ้ำ
- กด Back/refresh ระหว่าง modal หรือหลัง approve: ปุ่มและสถานะต้อง refresh จาก server
- ข้อความ 300/500 ตัวอักษร, emoji, ขึ้นบรรทัดใหม่, อักขระ `& < > " '` ต้องไม่พัง PDF/CSV
- ค่า CSV ที่ขึ้นต้น `=`, `+`, `-`, `@` ควรถูกป้องกัน formula injection
- วันที่สิ้นปี/ปีใหม่ เพื่อดูการ reset เลขและปี พ.ศ.; เวลา 00:00/23:59
- ผู้ใช้ถูก deactivate หรือย้ายหน่วยงานระหว่างรออนุมัติ: ระบบต้องมีวิธีจัดการ ไม่ค้างถาวร
- attachment ถูกลบ/scan fail จาก Document Center: ใบและ PDF ต้องไม่แสดงว่าทุกอย่างสำเร็จแบบเงียบ ๆ
- notification service หรือ PDF store ล้มใน final approval: ต้องไม่เกิด approved แต่ไม่มี final document โดยไม่มี retry/alert
- ตรวจ log/metric ว่าตามหา doc no แล้ว trace create→approve→store→notify ได้

## 8. วิธีรันให้คุ้มเวลา

### รอบ A — 60–90 นาที: Smoke เชิงธุรกิจ

รัน R01 happy, R02 combinations หลัก, R03, R04, R05, R07 direct deny และ R08 PDF final หากข้อใดพังให้หยุดรับรองและเปิด defect

### รอบ B — 2–3 ชั่วโมง: Negative + integration

รัน R02 ทุก negative, R06 race, R09–R13 พร้อมเก็บ network/audit/notification evidence

### รอบ C — 60–90 นาที: Exploratory

รัน stale tab, retry, long data, date boundary, CSV security และ failure recovery ตาม P2

## 9. หลักฐานที่ต้องเก็บต่อเคส

อย่างน้อยหนึ่งชุดต่อ scenario:

- เลขเอกสารและ test data ที่ใช้
- actor/role และเวลาทดสอบ
- screenshot ก่อน/หลัง + Network request/response สำหรับ deny/validation/concurrency
- PDF/CSV/notification ที่เกิดจริง
- audit history ของใบเดียวกัน
- Expected อ้าง FRD (`BR/VR/EC/FN/AC`) และ Actual ที่สังเกตได้
- ถ้า fail: steps ทำซ้ำ, severity, ผลกระทบธุรกิจ, workaround, environment/build

## 10. เกณฑ์ severity

| ระดับ | ตัวอย่าง |
|---|---|
| Critical | ข้ามสิทธิ์/ข้ามลำดับอนุมัติ, เห็นข้อมูลข้าม tenant, approve ตัวเอง, ข้อมูลหาย/แก้ final ได้ |
| High | ผล/สถานะ/เลข/PDF/notification ผู้รับผิด, สร้างเลขซ้ำ, final PDF ไม่ถูกเก็บ |
| Medium | validation ผิดแต่มีทางเลี่ยง, audit ขาด, filter/CSV ผิดบางกรณี |
| Low | ข้อความ/ตำแหน่ง/ความเรียบร้อยที่ไม่เปลี่ยนผลธุรกิจ |

## 11. Exit criteria ก่อนลงชื่อรับรอง

- P0 ผ่านทั้งหมด และมีหลักฐานจาก Production หรือ environment ที่ใช้ config เดียวกับ Production
- ไม่มี Critical/High เปิดค้าง
- ทุก BR-01..17, VR-01..12, EC-01..16 และ permission deny cases มีผล Pass/Fail/Not Run ชัดเจน
- DOA/DOCCFG/NTF wiring ถูกยืนยันจากของจริง ไม่ใช่ prototype
- PDF final, audit, notification และ direct API permission ถูกตรวจอย่างน้อยหนึ่ง end-to-end flow
- รายการที่ไม่ได้ตรวจต้องระบุชัด ห้ามนับเป็น Pass

## 12. คำถามที่ควรถาม PM/BA ก่อนปิด review

1. Production ยืนยันสาย DOA จริงเป็นกี่ขั้นและ role ใดบ้าง? ค่า 2 ขั้นใน FRD เคยได้รับการเซ็นยืนยันแล้วหรือยัง?
2. Admin role ID ที่ใช้จริงคืออะไร และ admin มีสิทธิ์ยกเลิกแต่ไม่มีสิทธิ์แก้/approve ใช่หรือไม่?
3. สถานะ canonical คือ `pending` หรือ `pending_approval` และ event mapping ได้ทดสอบจริงแล้วหรือยัง?
4. หลัง submit/approved อนุญาตให้เพิ่มหรือลบ attachment หรือถือว่าล็อกทั้งเอกสาร?
5. ถ้า PDF store หรือ notification ล้มตอน approve ต้อง rollback, retry หรือขึ้น approved พร้อมงานค้างแบบใด?
6. ข้อมูลทดสอบบน Production ต้องลบ/เก็บ/ติดป้ายอย่างไร และใครอนุมัติให้สร้าง?

---

หลังทดสอบ ให้แปลงผลเป็น Feature Check Report โดยแยก 1 แถวต่อ rule/scenario; สิ่งที่ไม่ได้รันให้ระบุ `Not Run` และห้ามเติม Pass จากการคาดเดา
