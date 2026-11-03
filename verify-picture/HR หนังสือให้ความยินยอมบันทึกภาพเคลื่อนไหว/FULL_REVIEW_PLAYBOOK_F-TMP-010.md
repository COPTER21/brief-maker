# Full Review Playbook — F-TMP-010

ฟีเจอร์: หนังสือให้ความยินยอมในการบันทึกและเผยแพร่ภาพถ่าย หรือภาพเคลื่อนไหว  
วัตถุประสงค์: ตรวจ Logic / การทำงาน / สิทธิ์ / หลักฐาน / ความเสี่ยงทางธุรกิจ หลังฟีเจอร์ขึ้น Production แล้ว  
Baseline หลัก: `03_FRD/FRD_F-TMP-010_Pack` โดยใช้ `06_TESTS.md` เป็น acceptance baseline และใช้เอกสารอื่นเพื่ออธิบายรายละเอียดเท่านั้น

> เอกสารนี้เป็นแผนตรวจ ไม่ใช่ผลตรวจ ทุกช่อง Result ต้องมาจากสิ่งที่ผู้ตรวจทำหรือเห็นจริง ห้ามถือว่าผ่านจากผล QA เดิมหรือข้อความใน prototype

## 1. คำตอบสั้น ๆ ว่าควรตรวจอะไร

ไม่ต้องย้อนตรวจความสวยของ layout ทั้งหมดอีกครั้ง แต่ต้องตรวจ 6 แกนนี้:

1. State transition: ร่าง → ยืนยันแล้ว → ถอนความยินยอม และ ร่าง → ยกเลิก
2. Immutability: ใบยืนยันแล้วแก้ข้อมูลเดิมไม่ได้จริง รวมถึงยิง API ตรง
3. Consent semantics: เก็บผลแยกรายข้อ ถอนข้อหนึ่งแล้วข้ออื่นยังมีผล
4. Minor rule: ต่ำกว่าเกณฑ์ต้องมีผู้ปกครอง; เท่ากับเกณฑ์ไม่ถือเป็นผู้เยาว์
5. Permission / PDPA: ร่างของคนอื่นต้องไม่เห็น; เลขบัตรและข้อมูลผู้เยาว์ต้องไม่รั่วใน list, CSV, log หรือสิทธิ์ทั่วไป
6. Evidence integrity: เลขเอกสาร, snapshot, PDF, audit history และ notification ต้องสัมพันธ์กับเหตุการณ์จริง

## 2. จุดขัดกันใน FRD ที่ต้องให้ PM/BA ตัดสินก่อนใช้เป็น Expected

| Conflict | เอกสารฝั่ง A | เอกสารฝั่ง B | ผลกระทบ | คำถามที่ต้องล็อก |
|---|---|---|---|---|
| Reject แล้วไปสถานะใด | `03_LOGIC` FN-07, `06_TESTS` T-35, BRD state table: `rejected` | `05_RULES` BR-DOA-05 และ Governance: `back_to_draft` เลขเดิม | ตัดสินผิดไม่ได้ว่า Production ถูกหรือผิด | ไม่รับหนังสือแล้วต้องจบที่ `rejected` หรือกลับ `draft` เพื่อแก้ไข? |
| ถอนทั้งฉบับด้วย scope ว่าง | `02_API`, `03_LOGIC`, `04_DB`, BRD: scope ว่าง = ทั้งฉบับ | `05_RULES` VR-11, `06_TESTS` T-16: ไม่เลือกข้อแล้วต้องบล็อก | UI/API อาจให้ผลไม่ตรงกัน | ต้องมีปุ่ม “ถอนทั้งฉบับ” ที่ส่ง scope ทุกข้อ หรืออนุญาต empty scope? |
| Notification ตอนยืนยัน | `02_API`, `03_LOGIC`, `06_TESTS`: ยิง event ตอน confirmed | DEC-02 / `07_LOCKED_DECISIONS`: ประกาศ event แต่ไม่ยิงข้ามระบบ | อาจแจ้งเตือนเกิน scope หรือ QA คาดหวังผิด | รอบ Production นี้ event ไหนต้องยิงจริง และปลายทางใดต้องได้รับ? |
| DOA | FRD รองรับ dynamic และมีเคส 1/6 ขั้น | DEC-03 ระบุรอบนี้ 0 ขั้น; หลายจุดยัง `TODO: DOA engine` | ทดสอบ Production อาจแก้ config กระทบระบบจริง | DOA dynamic อยู่ใน scope ที่ deploy จริงหรือเป็น future-ready contract เท่านั้น? |
| กฎข้อมูลซ้ำ | EC-09 ระบุเตือน ไม่บล็อก | เป็น OQ-05 และชุด prototype ไม่ได้พิสูจน์ระดับ API | อาจสร้าง consent ซ้ำในกิจกรรมเดียวกัน | Production ตกลงให้เตือนหรือบล็อก และใช้ key ใดตรวจซ้ำ? |

หากยังไม่ได้คำตอบ ให้ลงผลเคสนั้นเป็น `BLOCKED — source conflict` ไม่ใช่ Pass หรือ Fail

## 3. ชุดข้อมูลและบัญชีที่ต้องเตรียม

ใช้ข้อมูลสมมติเท่านั้น ห้ามใช้เลขบัตรประชาชนจริง

| Code | สิ่งที่ต้องมี |
|---|---|
| U1 | เจ้าหน้าที่ประจำบูธ A — เจ้าของใบ |
| U2 | เจ้าหน้าที่ประจำบูธ B — ไม่ใช่เจ้าของ |
| HR | ผู้ใช้ `role-mgr-hr` |
| CP | ผู้ใช้ `role-compliance` |
| R-ADULT | บุคคลอายุมากกว่าเกณฑ์ พร้อมเลขบัตร test ที่ผ่าน checksum ตามระบบ |
| R-BOUNDARY | อายุเท่ากับ `PdpaPolicy.minor_age_threshold` |
| R-MINOR | อายุต่ำกว่าเกณฑ์ 1 ปี พร้อมข้อมูลผู้ปกครองสมมติ |
| DOC-OFF | วิธีปิด doc type `IMC` ใน environment ที่ปลอดภัย หรือหลักฐานจาก API test environment |
| OBS | สิทธิ์ดู network response, audit log, notification/event log และ stored PDF โดยไม่แก้ข้อมูล Production |

ก่อนเริ่ม บันทึก environment, build/version, วันที่เวลา, config เกณฑ์ผู้เยาว์, form revision, doc type status และบัญชีที่ใช้

## 4. ลำดับการตรวจที่แนะนำ

### Mission A — Adult happy path และหลักฐานปลายทาง (P0)

1. Login เป็น U1 และสร้างใบของ R-ADULT โดยเลือกข้อ 1–2 = ยินยอม, ข้อ 3 = ถอนความยินยอม
2. บันทึกร่างครั้งแรก
3. ตรวจเลขเอกสารถูกออกครั้งเดียว; save/edit ซ้ำแล้วเลขไม่เปลี่ยนและไม่ข้ามเลขเพิ่มจากการแก้ไข
4. ตรวจ list, search และ filter พบใบตามข้อมูลและสถานะร่าง
5. เปิด PDF ร่าง: มีป้าย “ร่าง”, checkbox ตรงกับข้อมูล, ไม่มี `{{...}}`, footer มี FM-HRM-51
6. ยืนยันใบ
7. ตรวจสถานะ `ยินยอมแล้ว/confirmed`, written date = signed date = วันที่ยืนยัน, ใบแก้ไม่ได้
8. เปิด PDF หลังยืนยันและเก็บ hash/เวลา/เลขเอกสารไว้เป็น evidence; PDF ต้องตรงกับค่าก่อนกดยืนยัน
9. ตรวจ History ว่ามี created/saved/confirmed พร้อมผู้ทำและเวลา
10. ตรวจ network/API ว่า mutation สำเร็จครั้งเดียว ไม่ duplicate จาก double-click

Expected สำคัญ: ข้อ 3 ไม่มีผลตั้งแต่ต้นแต่ข้อ 1–2 ยังมีผล; การเลือก “ถอนความยินยอม” ในแบบฟอร์มเริ่มต้นไม่ใช่ withdrawal event ภายหลัง

### Mission B — Immutability และป้องกันการยิงตรง (P0)

1. จากใบ confirmed ของ Mission A ตรวจว่าเมนู Edit ไม่แสดงหรือ disabled
2. ลองเปิด URL หน้าแก้ไขเดิมโดยตรง
3. หากมีสิทธิ์ทดสอบ API ให้ส่ง PUT โดยใช้ payload ที่เปลี่ยนชื่อ/ช่วงกิจกรรม/choice
4. ลองเปิดสอง session แก้ร่างเดียวกัน แล้วให้ session เก่าบันทึกทีหลัง

Expected: confirmed ตอบ `IMMUTABLE`; stale update ตอบ 409; ไม่มี field ใดเปลี่ยน, PDF snapshot ไม่เปลี่ยน และ audit ไม่บันทึกเป็น update สำเร็จ

### Mission C — ถอนความยินยอมรายข้อและทั้งฉบับ (P0)

1. สร้างและยืนยันใบใหม่ที่ยินยอมครบ 3 ข้อ
2. ถอนเฉพาะข้อ 3 พร้อมเหตุผล
3. ตรวจ record ผูกใบเดิม ไม่ออกเลขใหม่; สถานะ, ผู้ทำ, เวลา, เหตุผลอยู่ใน History
4. ตรวจข้อ 1–2 ยังมีผลและข้อ 3 ไม่มีผล
5. ตรวจ PDF มีบล็อก “บันทึกการถอนความยินยอม” และข้อมูล withdrawal ตรงกัน
6. ตรวจคำสั่งถอนซ้ำไม่แสดง/ทำไม่ได้
7. ทำเคส “ถอนทั้งฉบับ” ตามคำตอบ PM/BA จาก conflict list
8. ลองถอนโดยไม่ใส่เหตุผล และลองส่ง scope ของข้อที่เดิมเลือก withdraw

Expected: เหตุผลบังคับ; ถอนเฉพาะข้อที่เคย consent; ไม่สร้างใบใหม่; audit append-only; ไม่ลบหลักฐานเก่า

### Mission D — ผู้เยาว์และ boundary (P0)

1. อ่านค่าจริงของ `PdpaPolicy.minor_age_threshold` ก่อน ห้ามสมมติว่า 20
2. กรอก R-MINOR: ส่วนผู้ปกครองต้องเปิดเอง และยืนยันไม่ได้หากข้อมูลไม่ครบ
3. กรอกผู้ปกครองครบและยืนยัน: PDF ต้องมีชื่อผู้ปกครอง, ชื่อผู้เยาว์, วันที่จากระบบ
4. ตรวจข้อมูลผู้เยาว์ถูกจำกัดสิทธิ์มากกว่าข้อมูลทั่วไปตาม role matrix จริง
5. สร้างร่างด้วย R-BOUNDARY: อายุเท่ากับเกณฑ์ต้องไม่บังคับผู้ปกครอง
6. เริ่มจากอายุต่ำกว่าเกณฑ์ กรอกข้อมูลผู้ปกครอง แล้วแก้อายุเป็นผู้ใหญ่และ save
7. เปิดใหม่/ตรวจ response: ข้อมูล guardian/minor เดิมต้องถูกล้างจริง ไม่ใช่แค่ซ่อนบน UI
8. ทดสอบชื่อผู้เยาว์ต่างจากชื่อผู้ให้ความยินยอม: ต้องอนุญาต

### Mission E — Permission และ PDPA leakage (P0)

1. U1 สร้างร่าง; U2 ค้นหา, filter และเปิด URL ตรงด้วย id ของใบนั้น
2. U2 ลองแก้, ยกเลิก, ถอน และเรียก PDF/attachment endpoint ของ U1
3. HR และ CP เปิดใบทุกสถานะตามสิทธิ์ที่ FRD ระบุ
4. ผู้ใช้ที่ไม่มีสิทธิ์ Restricted ตรวจ detail และ network response ว่าเลขบัตรไม่ถูกส่งมาเต็มแล้วแค่ซ่อนด้วย CSS
5. Export CSV ทุก filter และเปิดไฟล์จริง ตรวจชื่อคอลัมน์และข้อมูลทุกแถว
6. ค้นหาเลขบัตร/บางส่วนของเลขบัตรใน search box และ URL/query/log ที่ผู้ใช้เห็น
7. ตรวจข้อมูลผู้เยาว์, guardian, choice ไม่รั่วใน notification, browser storage, downloadable filename หรือ error message

Expected: ร่างคนอื่นไม่อยู่ใน list และ URL ตรงตอบ 403/404; CSV ไม่มีเลขบัตรประชาชน; restricted field ต้องถูกตัด/ปิดบังตั้งแต่ response ตามสิทธิ์

### Mission F — Cancel และสถานะผิดเงื่อนไข (P1)

1. ยกเลิกร่างโดยไม่ใส่เหตุผล: ต้องบล็อก
2. ยกเลิกร่างพร้อมเหตุผล: เป็น cancelled และมี audit
3. ลองยกเลิก confirmed / withdrawn / cancelled ซ้ำ
4. U2 ลองยกเลิกใบของ U1; HR ลองยกเลิกตามสิทธิ์

Expected: ยกเลิกได้เฉพาะ draft/pending โดย owner หรือ HR; สถานะ terminal ทำ mutation ซ้ำไม่ได้

### Mission G — Validation และค่าขอบ (P1)

ตรวจทีละ field เพื่อให้รู้ว่ากฎใดเสีย ไม่กดทดสอบทุกช่องว่างพร้อมกัน:

- written place ว่าง
- ชื่อว่าง/ช่องว่างล้วน
- อายุ 0, 1, threshold-1, threshold, 120, 121, ทศนิยม, ตัวอักษร
- เลขบัตรว่าง, สั้น/ยาว, ตัวอักษร, checksum ผิด
- booth location ว่าง
- วันเริ่มว่าง, วันสิ้นสุดว่าง, วันสิ้นสุดก่อนวันเริ่ม, วันเดียวกัน
- consent line ว่างทีละข้อ, เลือกครบ, เลือก withdraw ครบทุกข้อ
- reason ว่าง/ช่องว่างล้วนในการ withdraw/cancel/reject
- string ยาวมาก, emoji, ไทย/อังกฤษผสม และข้อความคล้าย HTML/script ในช่องข้อความ

Expected: client และ server ให้กฎเดียวกัน; refresh แล้วข้อมูล invalid ไม่หลุดบันทึก; error ชี้ช่องที่แก้ได้ชัดเจน

### Mission H — Numbering, config และ snapshot (P1)

1. Save ครั้งแรกหลาย session พร้อมกัน ตรวจ doc_no ไม่ซ้ำ
2. แก้ร่างและ retry request ตรวจไม่ออกเลขใหม่
3. ปิด `IMC`: สร้างใหม่ไม่ได้ แต่ใบเดิมดูและพิมพ์ได้
4. หลังออกเลข เปลี่ยนชื่อ/ที่อยู่/โลโก้ config ใน environment ทดสอบ แล้วเปิดใบเก่าและสร้างใบใหม่
5. หลังออกใบ เปลี่ยน ConsentPurpose/form revision แล้วเปิด PDF ใบเก่า

Expected: ใบเก่าใช้ `header_snapshot` และ form revision เดิม; ใบใหม่ใช้ค่าปัจจุบัน; ไม่เกิดเลขซ้ำหรือเลขใบเดียวเปลี่ยนภายหลัง

### Mission I — Attachment (P1)

1. แนบชนิด/ขนาดที่อนุญาตและไม่อนุญาตตาม file policy
2. ลองแนบเมื่อ confirmed และโดยคนที่ไม่ใช่ owner
3. ตรวจดาวน์โหลดไฟล์ของใบคนอื่นด้วย URL ตรง
4. ตรวจชื่อไฟล์อันตราย, double extension และไฟล์ที่มีข้อมูลเกินจำเป็น

Expected: แนบได้เฉพาะ draft ผ่าน Document Center; permission ของ attachment สอดคล้องกับใบแม่; error ไม่เผย path ภายในระบบ

### Mission J — Search, filter, export และปริมาณข้อมูล (P2)

1. ใช้ข้อมูลหลายสถานะ หลายช่วงอายุ หลายบูธ แล้วทดสอบ filter เดี่ยว/ผสม/ล้าง
2. ตรวจ pagination และ total count ไม่เปลี่ยนผิดเมื่อ filter
3. Export ต้องตรงกับ filter ปัจจุบัน ไม่ใช่ทุกแถว
4. ตรวจ CSV injection ด้วยชื่อที่ขึ้นต้น `=`, `+`, `-`, `@`
5. ตรวจ encoding ภาษาไทย, comma, quote และ newline ใน CSV

### Mission K — Reliability / race / retry (P1)

1. Double-click Save, Confirm, Withdraw และ Cancel
2. กด back/refresh ระหว่าง mutation
3. ตัด network หลัง request ถูกส่งแล้วแต่ก่อน client ได้ response จากนั้น retry
4. Confirm พร้อมกันสอง session
5. Withdraw พร้อมกันสอง session

Expected: mutation สำคัญมีผลครั้งเดียว, ไม่สร้าง withdrawal/audit/notification ซ้ำ, UI หลัง refresh สะท้อน server truth

## 5. Business-sense probes ที่ FRD ยังไม่พิสูจน์ครบ

รายการนี้หากระบบทำไม่ตรง ไม่ควรเรียก Bug ทันที ให้ลงเป็น Gap / OQ และส่ง PM/BA/DPO ตัดสิน:

1. ผู้ให้ความยินยอมเป็นบุคคลภายนอกแต่เจ้าหน้าที่กรอกแทนทั้งหมด — หลักฐานใดพิสูจน์ว่าบุคคลนั้นยินยอมจริงเมื่อไม่มีภาพลายเซ็น?
2. เก็บเลขบัตรเต็มจำเป็นหรือไม่ และ retention/ลบ/ทำลายเมื่อครบกำหนดคืออะไร?
3. ใบ consent ไม่ได้ผูกกับ asset ภาพ/วิดีโอ — ฝ่ายการตลาดรู้ได้อย่างไรว่าภาพใดใช้ได้หรือถูกถอนแล้ว?
4. เมื่อถอนแล้ว notification ไปหาใครบ้าง และมี SLA หยุดเผยแพร่หรือไม่?
5. ผู้เยาว์: ระบบพิสูจน์ความสัมพันธ์/อำนาจของผู้ปกครองอย่างไร?
6. ถ้าผู้ให้ความยินยอมเลือก withdraw ทุกข้อตั้งแต่ต้น เหตุใดต้องสร้างใบ confirmed และมีผลธุรกิจอะไร?
7. การใช้สถานะเดียว `withdrawn` เมื่อถอนเพียงข้อเดียวทำให้ผู้ใช้เข้าใจผิดว่าใบทั้งฉบับไม่มีผลหรือไม่?
8. ถ้าพบ consent ซ้ำในกิจกรรมเดียวกัน ใบใดเป็น current truth และ precedence คืออะไร?
9. ช่องทางให้เจ้าของข้อมูลขอสำเนา แก้ข้อมูล หรือถอนโดยไม่ต้องกลับมาที่บูธคืออะไร?
10. ต้องมี retention, legal hold, access log และ breach response สำหรับเลขบัตร/ข้อมูลผู้เยาว์หรือไม่?

## 6. หลักฐานที่ต้องเก็บต่อหนึ่งเคส

- Test ID / เวลา / build / actor / record id / doc no
- Input ที่ใช้โดยปิดบังเลขบัตร
- Screenshot ก่อนและหลังเฉพาะจุดสำคัญ
- Actual status และข้อความบนจอ
- HTTP method/path/status/error code โดยไม่แนบ token หรือข้อมูลส่วนบุคคล
- Audit/history row ที่สัมพันธ์กัน
- PDF/CSV filename และ hash ถ้าต้องพิสูจน์ snapshot
- Result: PASS / FAIL / BLOCKED / NOT RUN
- หาก FAIL: ขั้นตอนทำซ้ำ, Expected, Actual, severity, workaround และขอบเขตข้อมูลที่อาจได้รับผล

## 7. เกณฑ์สรุปผล

- Critical: ข้ามสิทธิ์, ข้อมูล Restricted รั่ว, เปลี่ยน confirmed ได้, หลักฐาน/PDF ผิดหรือสูญหาย, mutation ซ้ำทำข้อมูลเสีย
- High: สถานะ/consent/withdrawal ผิด, minor rule ผิด, เลขเอกสารซ้ำ, ถอนแล้วข้อที่ไม่เกี่ยวถูกยกเลิก
- Medium: validation/audit/notification ผิดแต่มีทางเลี่ยงและไม่ทำให้ผล consent ผิด
- Low: ข้อความ/ตำแหน่ง/ความเรียบร้อยที่ไม่กระทบการตัดสินใจหรือหลักฐาน

ห้าม sign off เมื่อยังมี Critical, มี High ที่ยังไม่ถูกยอมรับความเสี่ยง, หรือ P0 มี `BLOCKED/NOT RUN` โดยไม่มีผู้รับผิดชอบและกำหนดปิด

## 8. Execution sheet

| Run | Mission / TC | Actor | Record / Doc No. | Expected | Actual | Result | Evidence | Bug/OQ |
|---|---|---|---|---|---|---|---|---|
| 1 | A — Adult happy path | U1 |  | ตาม Mission A |  | NOT RUN |  |  |
| 2 | B — Immutability | U1/U2 |  | ตาม Mission B |  | NOT RUN |  |  |
| 3 | C — Partial withdrawal | U1/HR |  | ตาม Mission C |  | NOT RUN |  |  |
| 4 | C — Full withdrawal | U1/HR |  | รอ PM/BA ล็อก scope semantics |  | BLOCKED |  | Conflict-02 |
| 5 | D — Minor | U1 |  | ตาม Mission D |  | NOT RUN |  |  |
| 6 | D — Boundary age | U1 |  | ตาม Mission D |  | NOT RUN |  |  |
| 7 | E — Permission/PDPA | U1/U2/HR/CP |  | ตาม Mission E |  | NOT RUN |  |  |
| 8 | F — Cancel | U1/U2/HR |  | ตาม Mission F |  | NOT RUN |  |  |
| 9 | G — Validation | U1 |  | ตาม Mission G |  | NOT RUN |  |  |
| 10 | H — Number/config/snapshot | U1/Config admin |  | ตาม Mission H |  | NOT RUN |  |  |
| 11 | I — Attachment | U1/U2 |  | ตาม Mission I |  | NOT RUN |  |  |
| 12 | J — Search/filter/export | U1/HR |  | ตาม Mission J |  | NOT RUN |  |  |
| 13 | K — Race/retry | U1 |  | ตาม Mission K |  | NOT RUN |  |  |
| 14 | Reject flow | Approver |  | รอ PM/BA ล็อกปลายทาง |  | BLOCKED |  | Conflict-01 |

## 9. เอกสารเดิมที่ควรเปิดคู่กัน

- `context/F-TMP-010_DevPack/F-TMP-010_DevPack/03_FRD/FRD_F-TMP-010_Pack/06_TESTS.md` — acceptance baseline 40 ข้อ
- `context/F-TMP-010_DevPack/F-TMP-010_DevPack/06_Test/testcases-F-TMP-010.md` — ขั้นตอนลงมือทำ 32 เคส
- `context/F-TMP-010_DevPack/F-TMP-010_DevPack/06_Test/testcase-F-TMP-010.html` — UAT ฉบับอ่านง่าย 29 เคส
- `context/F-TMP-010_DevPack/F-TMP-010_DevPack/03_FRD/FRD_F-TMP-010_Pack/05_RULES.md` — business rule, validation, edge case
- `context/F-TMP-010_DevPack/F-TMP-010_DevPack/03_FRD/FRD_F-TMP-010_Pack/02_API.md` — endpoint/error/event
- `context/F-TMP-010_DevPack/F-TMP-010_DevPack/03_FRD/FRD_F-TMP-010_Pack/04_DB.md` — snapshot, classification, audit, withdrawal record

