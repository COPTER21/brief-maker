# Full Logic Review Plan — F-TMP-004

ฟีเจอร์: แบบประเมินและคัดเลือกผู้ขาย/ผู้ให้บริการ ประจำปี  
วัตถุประสงค์: ตรวจเก็บตก logic และการทำงานบน production โดยยึด FRD เป็นหลัก ไม่รับรอง UI layout ซ้ำ  
สถานะเอกสารนี้: แผนตรวจและ checklist เท่านั้น — ยังไม่ใช่ผล Pass/Fail

## 1. ข้อสรุปก่อนเริ่มตรวจ

ยังไม่ควรสรุปว่า logic ผ่านทั้งหมดจากคำว่า “tester test ผ่าน” เพราะ DevPack ระบุว่าเดิมเป็นรอบ `[NO-BROWSER]`, ไม่มี `e2e_standard report` และ UAT ฉบับคนตัดเคสหลังบ้าน/เทคนิคบางรายการออก เช่น การเปลี่ยน DOA ระหว่างรอ, config snapshot, stale update, 403 จาก API, การเก็บ approved PDF และการไม่ส่งต่อ Vendor master

การ review รอบนี้ควรพิสูจน์ 4 เรื่องหลัก:

1. คำนวณคะแนนและผลประเมินถูกต้องที่ server ไม่ใช่แค่บนจอ
2. สถานะและสายอนุมัติเดินถูกทุกทาง โดยเฉพาะกรณีไม่ผ่านและการส่งกลับ
3. สิทธิ์ไม่รั่ว ทั้งการมองเห็น แก้ไข ตัดสิน ยกเลิก ดาวน์โหลด และ export
4. ผลข้างเคียงถูกต้องและไม่ซ้ำ ได้แก่ notification, audit, PDF snapshot, Document Store และเลขเอกสาร

## 2. Source of truth ที่ใช้ตัดสิน

ใช้ตามลำดับนี้เมื่อเอกสารขัดกัน:

1. `07_LOCKED_DECISIONS` — มติที่ล็อก
2. `05_RULES` — business rule, state, permission, validation, edge case
3. `03_LOGIC` — การคำนวณและ transition
4. `02_API` และ `04_DB` — server-side contract, concurrency, audit, RLS
5. `06_TESTS` — acceptance criteria และ deny cases
6. `TC_*.md` — วิธีทดสอบประกอบ แต่ห้ามใช้ตัดสินขัด FRD

BRD, prototype และ UAT ใช้ช่วยทำความเข้าใจเท่านั้น ไม่ใช้ override FRD

## 3. ประเด็นเอกสารที่ต้องให้ PM/BA หรือ Dev แสดงคำตอบก่อนเซ็นรับรอง

| ID | ประเด็น | สิ่งที่เอกสารระบุ | สิ่งที่ต้องขอหลักฐาน/คำตอบ |
|---|---|---|---|
| DOC-GAP-01 | DOA บน production | DOA brief ยังเป็น `wire_status: pending` | entry จริงบน DOA กลาง, role และจำนวนขั้นที่ active อยู่ |
| DOC-GAP-02 | ผู้บริหารเมื่อผลไม่ผ่าน | เงื่อนไข `eval_result == fail` ยังเป็น `proposed/TODO` | หลักฐานว่า DOA production resolve เพิ่มผู้บริหารจริง โดย feature ไม่ hardcode |
| DOC-GAP-03 | role ผู้จัดทำ | `role-pur-officer` ไม่อยู่ใน DOA contract ตาม brief | role id จริงที่ใช้งาน และ mapping ผู้มีสิทธิ์จริง |
| DOC-GAP-04 | ค่าเริ่มสายอนุมัติ | 2 ขั้นยังถูกระบุ `[DEFAULT — รอยืนยัน]` | มติ BA/ลูกค้าที่อนุมัติสายจริง |
| DOC-GAP-05 | ปุ่มทำซ้ำ | FRD/DEC-11 บอก “ทำซ้ำ ✗” แต่ TC-L08 คาดว่ามีเมนู “ทำซ้ำ” | ให้ BA ตัดสิน; ระหว่างนี้ยึด FRD ว่าไม่ควรมี |
| DOC-GAP-06 | ยกเลิกใบ returned | FN-08/05_RULES อนุญาต `returned` แต่ DEC-08/DOA brief เขียนเฉพาะ draft,pending | ให้ BA ยืนยันว่าผู้ใช้ยกเลิก returned ได้หรือไม่ |
| DOC-GAP-07 | สถานะเมื่อ reject | FRD ล็อกเป็น `returned`; DOA brief บางส่วนเขียนกลับ `draft` และมี enum `rejected` | production ต้องแสดง/เก็บ `returned` ตาม FRD 07; หากไม่ใช่ให้เปิด defect/spec conflict |
| DOC-GAP-08 | AI-DEFAULT 11 มติ | DevPack ระบุรอลูกค้าเซ็นก่อน UAT | ขอหลักฐานว่ามติที่ขึ้น production ได้รับการรับรองแล้ว หรือบันทึกเป็น accepted risk |

ถ้า DOC-GAP-01 ถึง 04 ตอบไม่ได้ ห้ามเซ็นว่า approval logic ผ่านครบ ให้ลงผล `Blocked — ขาด production configuration evidence`

## 4. สิ่งที่ต้องเตรียมก่อนทดสอบ

- [ ] ระบุ production build/version และเวลาที่เริ่มตรวจ
- [ ] มี test tenant หรือข้อมูลทดสอบที่อนุญาตให้สร้าง/อนุมัติ/ยกเลิกบน production
- [ ] ผู้ใช้ทดสอบอย่างน้อย 5 แบบ: owner, ผู้จัดทำ, ผู้จัดการจัดซื้อ, ผู้บริหาร, คนนอกสาย
- [ ] มี owner คนที่ 2 เพื่อทดสอบการเห็นใบข้ามเจ้าของ
- [ ] ทราบ VendorEvaluationConfig ปัจจุบัน: หัวข้อ, max score, pass threshold, certifications, effective date
- [ ] ทราบ DOA entry ปัจจุบันและ assignee จริงทุกขั้น
- [ ] เข้าดู audit/history, notification center และ email ของผู้รับได้
- [ ] Dev/DBA ช่วยตรวจ API response, audit, Document Store, RLS และ event log ในเคสที่พิสูจน์ด้วย UI ไม่ได้
- [ ] เตรียม vendor code เฉพาะรอบนี้ เช่น `REV-VEV-YYYYMMDD-01`
- [ ] ห้ามใช้ข้อมูลผู้ขายจริงที่ส่งผลทางธุรกิจโดยไม่ได้รับอนุญาต

## 5. ชุดข้อมูลหลัก

ใช้ค่าจาก config จริง ไม่ hardcode 3/4/2/1 หรือ threshold 6 หาก production ถูกตั้งค่าไม่เหมือนเอกสารตัวอย่าง

| ชุด | คะแนนรวมเทียบ threshold | ใช้พิสูจน์ |
|---|---:|---|
| DATA-PASS-EDGE | เท่ากับ threshold พอดี | ต้องเป็น Pass |
| DATA-PASS-HIGH | มากกว่า threshold | Pass ปกติ |
| DATA-FAIL-EDGE | ต่ำกว่า threshold 0.1 | Fail + เพิ่มผู้บริหาร + แจ้งเตือน |
| DATA-DRAFT | กรอกคะแนนไม่ครบ | บันทึกร่างได้ แต่ส่งไม่ได้ |
| DATA-DUP | vendor code เดียวกัน ต่างตัวพิมพ์ ในปีเดียวกัน | เตือนแต่ไม่บล็อก |
| DATA-INVALID | -0.1, เกิน max 0.1, ทศนิยม 2 ตำแหน่ง, ตัวอักษร | server ต้องปฏิเสธ |

## 6. P0 — ต้องผ่านก่อนรับรอง logic

### P0-01 คำนวณคะแนนและผลที่ขอบเกณฑ์

- [ ] สร้างใบด้วยคะแนนครบและรวมเท่ากับ threshold
- [ ] หน้าจอแสดง Pass
- [ ] API/ข้อมูลที่อ่านกลับมี `score_total` ตรงผลรวม และ `eval_result=pass`
- [ ] เปลี่ยนคะแนนให้ต่ำกว่า threshold 0.1 แล้วผลเป็น Fail
- [ ] ส่ง request ที่แอบใส่ `score_total`/`eval_result` ขัดกับคะแนนจริง
- [ ] server เพิกเฉยหรือไม่รับค่าที่ client ปลอม และคำนวณใหม่เอง
- [ ] ค่า 0 ยอมรับได้; ค่าติดลบ, เกิน max, ทศนิยมเกิน 1 ตำแหน่ง และตัวอักษรถูกบล็อกทั้ง UI/API

หลักฐาน: ภาพคะแนนทุกหัวข้อ + Network response หรือ response จาก Dev + เลขเอกสาร

### P0-02 ร่างและ validation ตอนส่ง

- [ ] ชื่อและรหัสผู้ขายว่าง: บันทึกครั้งแรกไม่ได้
- [ ] คะแนนไม่ครบ: บันทึกร่างได้ แต่ส่งไม่ได้ด้วย `SCORE_INCOMPLETE`
- [ ] ไม่เลือกสินค้า/บริการ: ส่งไม่ได้
- [ ] เลือกสินค้า/บริการแต่ไม่กรอกรายละเอียด: ส่งไม่ได้
- [ ] เลือก “อื่นๆ” แต่ไม่ระบุชื่อมาตรฐาน: ส่งไม่ได้
- [ ] ยกเลิกการเลือกสินค้า/บริการแล้วค่ารายละเอียดเดิมถูกล้างจริงเมื่อบันทึกและเปิดใหม่
- [ ] ไม่มีทางข้าม validation ด้วย refresh, deep link หรือยิง API ตรง

### P0-03 Happy path ผลผ่าน

- [ ] owner สร้างร่าง ได้เลข VEV ตอนบันทึกครั้งแรก
- [ ] บันทึกซ้ำ/แก้ไขไม่ออกเลขใหม่
- [ ] ส่งใบ Pass แล้ว DOA resolve ตาม config จริง
- [ ] owner เลือกตัวเองเป็น approver ไม่ได้ทั้ง UI และ API
- [ ] ขั้น 1 เห็นใบหลังส่งและตัดสินได้เฉพาะตน
- [ ] อนุมัติขั้น 1 แล้วขั้น 2 จึงกลายเป็น current
- [ ] ผู้อนุมัติขั้นถัดไปกดก่อนเวลาไม่ได้
- [ ] ครบทุกขั้นแล้วเป็น approved
- [ ] approved ไม่มีแก้ไข/ยกเลิก/ส่งซ้ำ ทั้ง UI และ API
- [ ] approved_final ถูกเก็บใน Document Store จริง

### P0-04 ผลไม่ผ่านและขั้นผู้บริหาร

- [ ] สร้างใบ Fail โดยคะแนนต่ำกว่า threshold 0.1
- [ ] DOA preview/resolve เพิ่มขั้นผู้บริหารจาก DOA กลาง
- [ ] ไม่มีการ hardcode ผู้บริหารใน feature; Dev แสดง resolve response หรือ `doa_ref`
- [ ] chain ที่ snapshot มีผู้จัดทำ → ผู้จัดการจัดซื้อ → ผู้บริหาร ตาม config จริง
- [ ] notification `vev_evaluation_failed` ยิงครั้งเดียวต่อการส่ง
- [ ] role-mgr-pur และ role-gm ได้ทั้ง in-app และ email
- [ ] เนื้อหาแจ้งมีเลขเอกสาร, vendor, score/max ถูกต้อง
- [ ] คนอื่นที่ไม่ใช่ผู้รับไม่ได้เงินแจ้ง
- [ ] อนุมัติครบรวมผู้บริหารแล้วจึงเป็น approved

หากไม่เพิ่มผู้บริหาร ให้จัดระดับอย่างน้อย High; หากข้ามผู้อนุมัติหรือคนไม่มีสิทธิ์อนุมัติได้ ให้จัด Critical

### P0-05 Reject → returned → แก้ → ส่งใหม่

- [ ] reject โดยไม่ใส่เหตุผลไม่ได้
- [ ] reject แล้วสถานะเป็น `returned` ไม่ใช่ rejected ปลายทาง
- [ ] เลข VEV เดิมไม่เปลี่ยน
- [ ] owner เห็นเหตุผล ผู้อนุมัติและเวลาที่ส่งกลับ
- [ ] owner แก้ไข returned ได้
- [ ] ประวัติเดิมไม่ถูกลบ/เขียนทับ
- [ ] ขั้นที่เหลือของรอบเดิมเป็น skipped
- [ ] แก้จาก Fail เป็น Pass แล้วส่งใหม่: resolve ใหม่เหลือสาย Pass
- [ ] แก้จาก Pass เป็น Fail แล้วส่งใหม่: resolve ใหม่เพิ่มผู้บริหาร
- [ ] approval chain รอบใหม่ถูก freeze และรอบเก่ายังตรวจสอบย้อนหลังได้
- [ ] notification Fail ไม่ยิงในรอบที่ผลใหม่เป็น Pass และยิงครั้งเดียวในรอบที่เป็น Fail

### P0-06 Permission และข้อมูลรั่ว

ทดสอบทั้ง “ไม่มีปุ่ม” และ “ยิง URL/API ตรง” เพราะซ่อนปุ่มอย่างเดียวไม่ถือว่าผ่าน

- [ ] ผู้จัดทำ/approver มองไม่เห็นร่างของคนอื่น
- [ ] owner A มองไม่เห็นใบของ owner B
- [ ] คนนอกสายเปิด ID ที่เดาได้แล้วได้ 404 ไม่ใช่ 403 เพื่อไม่เปิดเผยว่ามีเอกสาร
- [ ] approver เห็นหลังส่งเท่านั้น
- [ ] role-mgr-pur เห็นทุกใบตาม FRD
- [ ] คนที่ไม่ใช่ current approver ตัดสินไม่ได้ (`NOT_CURRENT_APPROVER`)
- [ ] owner แก้ได้เฉพาะ draft/returned ของตน
- [ ] owner แก้ pending/approved ไม่ได้
- [ ] คนนอกสายยกเลิก/ดาวน์โหลด PDF/ไฟล์แนบ/export ข้อมูลไม่ได้
- [ ] ทดลองข้าม tenant โดยให้ Dev/DBA พิสูจน์ RLS: list/detail/export/attachment ต้องไม่รั่ว

### P0-07 Config snapshot และ DOA snapshot

ต้องประสาน admin/Dev ทำในช่วงทดสอบ:

- [ ] สร้างใบ A แล้วจด criteria, max score, threshold, certifications
- [ ] เปลี่ยน VendorEvaluationConfig
- [ ] เปิดใบ A ใหม่: ต้องใช้ค่า snapshot เดิมทั้งหมด รวมการคำนวณและ PDF
- [ ] สร้างใบ B หลังเปลี่ยน: ต้องใช้ config ใหม่
- [ ] ส่งใบ C แล้วเปลี่ยน DOA/assignee ระหว่าง pending
- [ ] ใบ C ต้องเดินตาม chain snapshot เดิม
- [ ] ใบใหม่หลังเปลี่ยนต้องใช้ DOA ใหม่

ถ้าใบเก่าเปลี่ยนตาม config/DOA ใหม่ ให้จัด High; ถ้าทำให้ข้ามผู้อนุมัติ ให้จัด Critical

### P0-08 Concurrency, retry และ double-submit

- [ ] เปิดใบเดียวกัน 2 browser/session ด้วย version เดียวกัน
- [ ] session A บันทึกสำเร็จ
- [ ] session B บันทึกค่าเก่า ต้องได้ 409 `STALE` และไม่ทับข้อมูล A
- [ ] กดส่งเร็วสองครั้ง/จำลอง retry ด้วย Idempotency-Key เดิม
- [ ] ต้องเกิด transition, notification, audit และเลขเอกสารเพียงครั้งเดียว
- [ ] retry approve/cancel ด้วย key เดิมไม่สร้าง audit/event ซ้ำ
- [ ] request write ที่ไม่มี/ผิด `If-Match` และ Idempotency-Key ต้องเป็นไปตาม API contract

### P0-09 Cancel

- [ ] owner ยกเลิก draft ได้เมื่อใส่เหตุผล
- [ ] owner ยกเลิก pending ได้เมื่อใส่เหตุผล
- [ ] role-mgr-pur ยกเลิกใบของคนอื่นได้ตาม FRD
- [ ] ผู้อนุมัติทั่วไป/คนนอกสายยกเลิกไม่ได้
- [ ] approved และ cancelled ยกเลิกซ้ำไม่ได้
- [ ] pending → cancelled ทำให้ขั้น pending/waiting เป็น skipped
- [ ] current approver ได้ `vev_cancelled` in-app เพียงครั้งเดียว
- [ ] non-current approver ไม่ได้แจ้งยกเลิก
- [ ] กรณี returned ให้ลง `Blocked` จน DOC-GAP-06 ได้ข้อยุติ แล้วทดสอบตามมติ

### P0-10 PDF และ approved snapshot

- [ ] PDF ทุกสถานะเปิดได้และเป็น 2 หน้า
- [ ] ไม่มี placeholder เช่น `{{...}}`, ตัวอักษรขาด หรือข้อมูลคนละใบ
- [ ] คะแนนรายข้อ, max, total, threshold และผลตรงกับข้อมูลในระบบ
- [ ] Pass/Fail checkbox ถูกต้องและผู้ใช้แก้เองไม่ได้
- [ ] ใบ Fail มีช่องผู้บริหารตาม chain จริง
- [ ] ช่องลงชื่อ = ผู้ประเมิน + 1 ช่องต่อ approval step; ทดสอบอย่างน้อย 2, 3 และ 6 ขั้นถ้าระบบรองรับ
- [ ] คำตัดสินผูก role: ผู้จัดทำใช้เห็นด้วย/ไม่เห็นด้วย; manager/GM ใช้อนุมัติ/ไม่อนุมัติ
- [ ] draft ไม่แสดงชื่อ/วันที่ผู้ประเมินเหมือนส่งแล้ว
- [ ] approved PDF ที่ดาวน์โหลดตรงกับ `approved_final` ใน Document Store
- [ ] เปลี่ยน config/โลโก้/ชื่อพนักงานภายหลังแล้ว approved snapshot เดิมไม่เปลี่ยน

## 7. P1 — ต้องตรวจเพื่อความครบของ FRD

### P1-01 เลขเอกสาร

- [ ] รูปแบบมาจาก F-DOCCFG ที่ active จริง ไม่ hardcode
- [ ] reset รายปีและ scope global เป็นไปตาม config
- [ ] เลข unique ต่อ tenant และไม่มีเลขซ้ำเมื่อสร้างพร้อมกัน
- [ ] ยกเลิก/ส่งกลับไม่ reuse หรือเปลี่ยนเลข
- [ ] no-gap เป็น false: ช่องว่างของเลขไม่ถือเป็น defect
- [ ] ปิด doc type แล้วปุ่มสร้าง disabled และ API ตอบ `DOC_TYPE_INACTIVE`

### P1-02 Duplicate vendor ในปีเดียวกัน

- [ ] vendor code เดียวกันและปีเดียวกันเตือน แต่ยังส่งได้
- [ ] เปรียบเทียบแบบไม่สนตัวพิมพ์
- [ ] ใบ cancelled ไม่นับเป็น duplicate
- [ ] ใบ approved/pending/returned/draft อื่นยังถูกเตือนตาม `status != cancelled`
- [ ] ข้ามปีไม่เตือนผิด
- [ ] ตรวจการ trim space หน้า/ท้าย; ถ้าไม่เท่ากันให้ถาม BA ว่าต้อง normalize หรือไม่

### P1-03 List, search, filter และ CSV

- [ ] list แสดงเฉพาะข้อมูลตามสิทธิ์
- [ ] “รอฉันพิจารณา” แสดงเฉพาะ current assignee
- [ ] ค้นหาเลขเอกสาร, vendor name/code และผู้ประเมินได้ตาม API
- [ ] filter status/result ใช้ร่วมกันถูกต้อง
- [ ] result `none` แสดงใบคะแนนไม่ครบ
- [ ] CSV ใช้ filter และสิทธิ์ชุดเดียวกับหน้ารายการ
- [ ] CSV มีคะแนนรายหัวข้อตาม config snapshot ไม่ใช่ fix 4 คอลัมน์เมื่อ config เปลี่ยนจำนวนข้อ
- [ ] ภาษาไทย/ทศนิยม/leading zero ไม่เพี้ยนเมื่อเปิด spreadsheet

### P1-04 Attachment

- [ ] เพิ่ม/ลบไฟล์ได้เฉพาะผู้มีสิทธิ์และสถานะที่อนุญาต
- [ ] เปิดไฟล์ของใบที่ไม่มีสิทธิ์ไม่ได้แม้รู้ URL/attachment id
- [ ] ไฟล์ผูก ref type VEV และใบถูกต้อง
- [ ] retry upload ไม่สร้างไฟล์ซ้ำโดยไม่ตั้งใจ
- [ ] approved แล้วพฤติกรรมเพิ่ม/ลบไฟล์ตรง policy ที่ BA ยืนยัน

### P1-05 Audit

- [ ] ทุก create/update/submit/approve/reject/resubmit/cancel มี actor, action, note, timestamp
- [ ] เหตุผล reject/cancel อยู่ครบและไม่ถูกแก้ย้อนหลัง
- [ ] ลำดับ audit ตรงกับสถานะจริง
- [ ] retry/idempotency ไม่เพิ่ม audit ซ้ำ
- [ ] Dev/DBA ยืนยัน audit เป็น append-only ไม่มี update/delete ผ่าน application

### P1-06 สิ่งที่ต้อง “ไม่เกิด”

- [ ] approved แล้วไม่อัปเดต Vendor master/AVL
- [ ] ไม่ยิง `vev.evaluation_approved` ในรอบนี้
- [ ] feature ไม่ยิง `doa_pending`/`doa_result` ซ้ำกับ DOA engine
- [ ] ไม่มีปุ่ม/ฟังก์ชัน “ทำซ้ำ” ตาม DEC-11 เว้นแต่ BA อนุมัติเปลี่ยน scope
- [ ] ไม่มีการดึงคะแนนจาก PO/GRN

## 8. Exploratory — business sense นอก checklist เดิม

รายการนี้ไม่ควรใช้เปิด bug ทันทีหาก FRD ไม่กำหนด; ให้บันทึกเป็น observation/OQ ก่อน

- [ ] ปีประเมินอิง timezone Asia/Bangkok ถูกต้องตรงรอยต่อ 31 ธ.ค./1 ม.ค.
- [ ] vendor code ภาษาไทย/อังกฤษ, ตัวพิมพ์, space และอักขระพิเศษไม่ทำให้ duplicate หลุด
- [ ] ชื่อ vendor ยาว, criteria จำนวนมาก และ DOA 6 ขั้นไม่ทำให้ PDF ตัดข้อมูล
- [ ] คะแนน decimal เช่น 0.1 + 0.2 ไม่เกิด float เพี้ยน เพราะ server ต้องใช้ numeric/string
- [ ] CSV ป้องกันค่าที่ขึ้นต้น `=`, `+`, `-`, `@` ไม่ให้กลายเป็น spreadsheet formula
- [ ] notification retry ไม่ส่ง email ซ้ำ
- [ ] approver ถูก disable/ลาออกหลัง submit: chain snapshot ยังจัดการต่อได้อย่างไร
- [ ] attachment ที่ลบจากใบยังมี retention/audit ตาม Document Center policy
- [ ] ข้อมูล PII ของผู้ประเมิน/ผู้อนุมัติไม่ปรากฏใน export/log แก่ผู้ไม่มีสิทธิ์

## 9. วิธีเก็บหลักฐานต่อเคส

ทุกเคสต้องบันทึกอย่างน้อย:

| ช่อง | ตัวอย่าง |
|---|---|
| Case ID | P0-05 |
| Build/เวลา | prod build + 2026-11-16 14:30 ICT |
| Actor | E01 owner / E02 approver |
| Doc No. | VEV-2026-xxxx |
| Input | คะแนน, config version, DOA entry |
| Expected | ข้อความ/สถานะ/ผู้รับที่ FRD กำหนด |
| Actual | สิ่งที่เห็นจริง ห้ามเขียนเพียง “ผ่าน” |
| Evidence | screenshot, network request id, audit/event id, PDF filename |
| Result | Pass / Fail / Blocked / Not Run |
| Defect | BUG-xx + severity |

ห้ามให้ Pass จาก UI อย่างเดียวในเรื่อง permission, server calculation, RLS, idempotency, snapshot, notification, Document Store และ side effect

## 10. เกณฑ์ severity และผลสรุป

| ระดับ | ตัวอย่างในฟีเจอร์นี้ |
|---|---|
| Critical | ข้ามสิทธิ์/ข้ามผู้อนุมัติ, ข้าม tenant, คนไม่ใช่ current approver ตัดสินได้, audit ถูกแก้/ลบ |
| High | คะแนน/ผล Pass-Fail ผิด, สาย Fail ไม่มีผู้บริหาร, approved ยังแก้ได้, notification ผู้รับผิด, PDF approved ผิดข้อมูล/ไม่ถูกเก็บ |
| Medium | validation ผิดแต่มีทางเลี่ยง, duplicate warning ไม่ทำงาน, audit บาง event หาย, CSV ผิด |
| Low | ข้อความ/format/ตำแหน่งที่ไม่กระทบ logic |

ผลการ review:

- `ผ่าน`: P0 ทุกข้อผ่าน, ไม่มี Critical/High ค้าง, DOC-GAP ที่กระทบ logic มีมติ/หลักฐานครบ
- `ผ่านแบบมีเงื่อนไข`: ไม่มี Critical, มี High ที่มี owner/กำหนดแก้ชัด หรือมี P0 บางข้อ Blocked ด้วยข้อจำกัดหลักฐาน
- `ไม่ผ่าน`: มี Critical หรือ logic fail หลายจุดจนไม่อาจรับรอง flow หลัก

## 11. ลำดับลงมือที่แนะนำ

1. ปิด DOC-GAP-01 ถึง 08 กับ PM/BA/Dev และเก็บคำตอบเป็นหลักฐาน
2. รัน P0-01 ถึง P0-05 ด้วยเอกสาร Pass, Fail และ Returned ที่สร้างใหม่
3. รัน P0-06 ด้วย 5 personas และทดสอบ direct URL/API
4. ให้ admin/Dev ช่วยรัน P0-07 และ P0-08
5. ตรวจ P0-09 ถึง P0-10 พร้อม notification, audit, PDF และ Document Store
6. รัน P1 ทั้งหมด แล้วทำ exploratory เฉพาะที่มีเวลา/ความเสี่ยงสูง
7. ค่อยสร้าง Feature Check Report จากผลจริง ห้ามเติม Pass ให้ข้อที่ไม่ได้รัน

## 12. เอกสารเดิมที่ใช้ประกอบการรัน

- `_frd/.../03_LOGIC_*.md`
- `_frd/.../05_RULES_*.md`
- `_frd/.../06_TESTS_*.md`
- `_frd/.../07_LOCKED_DECISIONS_*.md`
- `_tc/TC_*.md` — มี 62 เคสและขั้นตอน UI ละเอียด
- `_tc/QA_AUDIT_*.md` — ดูรายการเคสที่ UAT ฉบับคนตัดออก
- `_governance/DOA_BRIEF_*.md`, `DOCCFG_BRIEF_*.md`, `NTF_BRIEF_*.md`

หมายเหตุ: หลังทดสอบจริงแล้วจึงนำผลและหลักฐานไปสร้าง `FR_F-TMP-004_R1_YYYYMMDD.html` ด้วย feature-check-report เพื่อเป็นใบรับรองผลตรวจ
