# Full Review Playbook — F-TMP-003 คำขอมีและใช้ลายเซ็นดิจิทัล (DSR)

วันที่จัดทำ: 5 พฤศจิกายน 2569  
ฐานอ้างอิงหลัก: `03_FRD/FRD_F-TMP-003_Pack` โดยเฉพาะ `03_LOGIC.md`, `05_RULES.md`, `06_TESTS.md`, `07_LOCKED_DECISIONS.md`

## 1. เป้าหมายของรีวิวรอบนี้

รีวิวรอบนี้ไม่ใช่การตรวจความสวยของ layout ซ้ำ แต่เป็นการตอบให้ได้ว่า:

1. ทุก state เปลี่ยนถูกทางและไม่มีทางลัดที่ผิดกฎ
2. ผู้ใช้แต่ละ role เห็นและทำได้เฉพาะสิ่งที่ควรทำ
3. ข้อมูลบนหน้าจอ, API, PDF, CSV, audit และ notification ตรงกัน
4. การ reject, แก้ไข, ส่งใหม่, ยกเลิก และอนุมัติหลายขั้นไม่ทำข้อมูลหรือเลขเอกสารเพี้ยน
5. ระบบไม่แก้ทะเบียนพนักงานหรือส่งข้อมูลข้ามระบบเกินขอบเขต FRD
6. มีหลักฐานพอให้ผู้รีวิวรับรองเฉพาะสิ่งที่ได้ตรวจจริง

## 2. ข้อสรุปจาก desk review ที่ต้องจัดการก่อนกดทดสอบ

สถานะเอกสารมีความไม่สอดคล้องกับคำบอกว่า feature ขึ้น production แล้ว:

- `QA_AUDIT_F-TMP-003.md` ระบุชัดว่าเคสจริง **ยังไม่เคยรัน** ใน artifact ชุดนี้ และ UAT HTML ก็ยังไม่สร้าง
- `RUN_LOG.md` ระบุว่า e2e, browser render, PDF comparison และ anchor verification ถูกข้ามเพราะเป็นโหมด `NO-BROWSER`
- FRD ระบุ `F-TMP-003` และ `REQ-TMP-003` เป็นรหัสชั่วคราว
- DEC-01 ถึง DEC-11 เป็น `AI-DEFAULT` และระบุว่าต้องให้ลูกค้ายืนยันก่อน UAT
- role เจ้าหน้าที่ใช้ `role-mgr-hr` แทน role จริง และยังเป็นคำถามค้าง
- FRD ระบุว่า doc type, DOA, document registration และ notification event เคยยังไม่ wire หรือยังไม่ทำ
- ชื่อ-นามสกุลภาษาอังกฤษในทะเบียนพนักงานเป็น dependency ที่ต้องมี แต่ยังเป็นคำถามค้าง

ก่อนเทส ให้ PM/BA หรือ owner ยืนยันหลักฐานว่า production ใช้ค่าจริงอะไรใน 5 เรื่องนี้:

| เรื่อง | ต้องได้คำตอบ/หลักฐาน |
|---|---|
| Scope baseline | FRD revision นี้คือ as-built/current baseline จริงหรือไม่ |
| รหัสจริง | feature code, request code, function/taxonomy code ที่ production ใช้ |
| ผู้พิจารณา | role จริง, DOA entry จริง, จำนวนขั้นจริง และผู้มีสิทธิ์ admin |
| Document config | `DSR` เปิดใช้, รูปแบบเลข, reset รายปี, timezone และปี ค.ศ./พ.ศ. |
| Notification | event ที่เปิดใช้จริง, ผู้รับจริง และมี retry/deduplication หรือไม่ |

ถ้าไม่มีคำยืนยัน ให้บันทึกเป็น **Business/Configuration Gap** ไม่ควรสรุปว่า logic ผ่านเพียงเพราะหน้าจอทำงานได้

ดังนั้นคำว่า “tester ผ่านแล้ว” ต้องขอ test run/result/evidence จากระบบจริงแยกต่างหาก; ไฟล์ใน context ชุดนี้พิสูจน์เพียงว่าเอกสารและต้นแบบผ่าน lint/consistency ไม่ได้พิสูจน์ว่า production logic ผ่าน

## 3. แยกขอบเขต Production กับ UAT

### ทำบน Production ได้เมื่อได้รับอนุญาต

- เปิด list/detail และตรวจสิทธิ์ด้วยบัญชีทดสอบ
- สร้างเอกสารทดสอบที่ระบุชัดว่าเป็น TEST และไม่มีข้อมูลบุคคลจริง
- เดิน happy path ด้วยผู้ขอและผู้พิจารณาที่กำหนด
- ตรวจ PDF, CSV, audit, attachment และ notification ของเอกสารทดสอบ
- ทดสอบ reject/resubmit/cancel เฉพาะเอกสารทดสอบที่สร้างเอง
- ตรวจ direct URL และ API denial ด้วยบัญชีทดสอบ

### ควรทำใน UAT/Staging เท่านั้น

- ปิด/เปิด doc type `DSR`
- เปลี่ยน DOA เป็น 3 หรือ 6 ขั้น หรือสลับลำดับ role
- เปลี่ยนชื่อบริษัท/โลโก้ master เพื่อทดสอบ snapshot
- ทดสอบ concurrency, double submit, replay request, malformed payload
- ทดสอบไฟล์อันตราย, spoof MIME, ไฟล์เกินขนาด และปริมาณมาก
- ทดสอบ notification failure/retry หรือหยุด dependency
- ทดสอบ reset เลขเอกสารข้ามปี/ข้าม timezone

ห้ามใช้ข้อมูลพนักงานจริงหรือทำให้ notification ไปถึงผู้รับจริงที่ไม่ได้อยู่ในแผนทดสอบ

## 4. ชุดผู้ใช้และข้อมูลที่ต้องเตรียม

| ชุด | บทบาท | ใช้ตรวจ |
|---|---|---|
| U1 | ผู้ขอ A | owner flow, draft, submit, cancel |
| U2 | ผู้ขอ B | ทดสอบข้ามเจ้าของ |
| U3 | ผู้พิจารณาขั้น 1 | current approver |
| U4 | ผู้พิจารณาขั้น 2 | future/non-current approver |
| U5 | HR admin | เห็นทั้งหมดและยกเลิกตามสิทธิ์ |
| U6 | ผู้ใช้ทั่วไปไม่เกี่ยวข้อง | data leakage และ direct URL/API denial |

ข้อมูลพนักงาน U1 ต้องมีชื่อไทย/อังกฤษ, ตำแหน่ง, หน่วยงาน, email, โทร และสถานที่ทำงานครบ เพื่อพิสูจน์ snapshot จากทะเบียนพนักงาน

เตรียมไฟล์แนบอย่างน้อย: PDF, DOCX, XLSX, PNG ที่ถูกต้อง, ไฟล์ใกล้ 20 MB, ไฟล์เกิน 20 MB และไฟล์นามสกุล/ชนิดเนื้อหาไม่ตรงกันสำหรับ UAT

## 5. ลำดับทดสอบที่แนะนำ

### Gate A — Configuration reconciliation (P0)

1. ยืนยัน doc type `DSR` active และรูปแบบเลขจริง
2. ยืนยัน DOA entry และ role จริง ไม่ใช่ค่า placeholder โดยไม่ตั้งใจ
3. ยืนยัน admin role ที่เห็นเอกสารทุกใบ
4. ยืนยัน event `dsr_cancelled` และ `dsr_name_change_requested` พร้อมผู้รับ
5. ยืนยันแบบพิมพ์ revision ที่ production ใช้
6. ยืนยันว่า DEC-01 ถึง DEC-11 ถูก business owner ยอมรับแล้ว

ถ้าข้อใดไม่ชัด ให้หยุดการรับรอง business correctness และเปิด gap ก่อน

### Flow 1 — สร้างคำขอครั้งแรกและ snapshot (TC-01, TC-02, TC-10, TC-14)

1. Login เป็น U1 แล้วเริ่มคำขอใหม่
2. ตรวจค่าเริ่มต้น: `case_kind = first`, `certified = false`, `made_at` มาจากสถานที่ทำงาน
3. ตรวจข้อมูลผู้ขอทุกช่องเป็น read-only และตรงทะเบียน ณ เวลานั้น
4. ลองไปต่อโดยไม่กรอก `made_at` และไม่ติ๊กคำรับรอง ต้องถูกบล็อก
5. กรอกครบ บันทึกร่างครั้งแรก
6. ตรวจเลขออกครั้งเดียว, วันที่เป็นวันบันทึกครั้งแรก, สถานะ `draft`
7. แก้และบันทึกซ้ำหลายครั้ง เลขและวันที่เดิมต้องไม่เปลี่ยน
8. ตรวจ audit ว่ามี create/edit พร้อมคนและเวลา

หลักฐาน: หน้าก่อนบันทึก, เลขเอกสารหลังบันทึก, detail, history และ request/response ถ้าเข้าถึงได้

### Flow 2 — กรณีต่ออายุทั้ง 3 เหตุผล (TC-03)

ทดสอบ `expired`, `file_lost`, `forgot_password` ทีละใบ ตรวจว่าเลือกได้ครั้งละหนึ่งเหตุผลและช่องเปลี่ยนชื่อทั้งหมดว่างทั้ง UI, detail, PDF และ payload ที่อ่านกลับ

### Flow 3 — เปลี่ยนชื่อ/นามสกุล (TC-04 ถึง TC-09, TC-27)

ทดสอบแยก 3 ชุด:

- `first_name`: บังคับชื่อเดิมไทย + ชื่อใหม่ไทย/อังกฤษ และช่องนามสกุลต้องว่าง
- `last_name`: บังคับนามสกุลเดิมไทย + ใหม่ไทย/อังกฤษ และช่องชื่อต้องว่าง
- `both`: ต้องครบทั้ง 6 ช่อง

ทุกชุดต้องตรวจ:

1. ค่าใหม่เท่าค่าเดิมต้องถูกบล็อก
2. เปลี่ยน case/change type ไปมาแล้วค่าที่ไม่เกี่ยวต้องถูกล้างจริงใน server ไม่ใช่แค่ซ่อนบนจอ
3. ส่งแล้วเกิด event `dsr_name_change_requested` หนึ่งครั้งต่อ transition ที่กำหนด
4. ระบบต้องไม่แก้ชื่อในทะเบียนพนักงานอัตโนมัติ
5. PDF ต้องติ๊กและแสดงเฉพาะช่องที่สัมพันธ์กับ change type

### Flow 4 — ส่งอนุมัติและ chain freeze (TC-15 ถึง TC-20)

1. ส่ง draft โดยไม่เลือก approver ให้ครบ ต้องถูกบล็อกเป็นรายช่อง
2. เลือกครบและส่ง ต้องเป็น `pending`, ขั้นแรก `pending`, ขั้นถัดไป `waiting`
3. เปลี่ยน DOA master หลังส่งเอกสาร A แล้วเปิด A ใหม่: chain ของ A ต้องไม่เปลี่ยน
4. สร้างและส่งเอกสาร B หลังเปลี่ยน DOA: B ต้องใช้ chain ใหม่
5. U4 ซึ่งยังไม่ใช่ current approver ต้อง approve/reject ไม่ได้ทั้ง UI และ API
6. U1 ผู้ขออนุมัติใบตัวเองไม่ได้
7. U3 อนุมัติแล้ว ขั้นถัดไปจึงเปิดให้ U4; ขั้นสุดท้ายผ่านแล้วเอกสารเป็น `approved`
8. เมื่อ approved แล้วห้ามแก้, ส่งซ้ำ, reject, cancel หรือ approve ซ้ำ

### Flow 5 — Reject → แก้ → ส่งใหม่ (TC-21 ถึง TC-23)

1. Reject โดยไม่ใส่เหตุผลต้องถูกบล็อก
2. Reject พร้อมเหตุผล เอกสารต้องกลับ `draft` และเลขเดิม
3. `submitted_at` ของรอบค้างต้องถูกล้างตาม FRD แต่ประวัติรอบเก่าต้องยังอยู่
4. เหตุผลล่าสุดต้องตรงกับ PDF ช่อง “เนื่องจาก”
5. แก้ข้อมูลแล้วส่งใหม่ ต้อง resolve DOA ใหม่ แต่ไม่ออกเลขใหม่
6. ตรวจว่าผู้พิจารณารอบเก่าไม่สามารถใช้ลิงก์/หน้าค้างทำรายการกับ chain รอบใหม่ได้

### Flow 6 — Cancel (TC-24 ถึง TC-26)

ทดสอบ owner และ HR admin ยกเลิกทั้ง `draft` และ `pending` โดยบังคับเหตุผล ตรวจ `cancelled`, ขั้นค้างเป็น `skipped`, audit ครบ และ event `dsr_cancelled` ส่งครั้งเดียว

ทดสอบผู้ใช้ไม่เกี่ยวข้องยกเลิกไม่ได้ และ `approved`/`cancelled` แล้วต้องทำซ้ำไม่ได้

### Flow 7 — สิทธิ์และการรั่วข้อมูล (TC-12, TC-13, TC-25, TC-28 ถึง TC-33, TC-41)

ต้องตรวจ 4 ชั้น ไม่ใช่แค่ปุ่ม:

1. List: รายการและตัวนับไม่รวมใบที่ไม่มีสิทธิ์
2. Search/filter: ค้นเลขหรือชื่อของคนอื่นแล้วต้องไม่พบ
3. Direct URL/detail/PDF/attachment: เปิด ID ที่เดา/คัดลอกมาต้องได้ 403
4. API/CSV: response ต้องไม่มี row หรือ field ของเอกสารที่ไม่มีสิทธิ์

กรณีสำคัญ: approver เห็นเอกสารหลัง submit แต่ห้ามเห็น draft ของคนอื่น; admin เห็นทั้งหมด; owner เห็นของตนทุกสถานะ

### Flow 8 — PDF, CSV และ document snapshot (TC-34 ถึง TC-46)

ตรวจอย่างน้อย draft, pending, approved, rejected-then-draft และ cancelled:

- draft มีคำว่า “ร่าง”; ผลพิจารณาและลายเซ็นยังไม่ถูกติ๊กเกินจริง
- approved แสดงคำตัดสิน, ผู้พิจารณา และวันเวลาตรง audit
- rejected-then-draft แสดงเหตุผลถูกใบ/ถูกรอบ ไม่ดึงเหตุผลเก่าไปใส่ใบใหม่
- กรณี 1/2 ช่องชื่อเดิม/ใหม่ว่าง; กรณี 3 แสดงตาม change type
- ช่องลงชื่อ = ผู้ขอ + 1 ต่อ DOA step, แถวละไม่เกิน 4
- ชื่อบริษัท/โลโก้มาจาก `header_snapshot` ตอนออกเลข ไม่เปลี่ยนตาม master ภายหลัง
- CSV ใช้ filter ปัจจุบันและสิทธิ์เดียวกับหน้าจอ; encoding ภาษาไทยเปิดใน Excel ได้
- ข้อมูลส่วนบุคคลและไฟล์แนบเข้าถึงได้เฉพาะผู้มีสิทธิ์
- approved PDF ถูกเก็บใน document store ตามกติกา และเปิดซ้ำได้เป็นฉบับเดิม

### Flow 9 — Attachment

1. upload/download/delete ก่อนและหลัง submit ตามสิทธิ์ที่ระบบกำหนด
2. บล็อกไฟล์เกิน 20 MB ทั้ง UI และ server
3. ตรวจชนิดไฟล์จริง ไม่เชื่อเฉพาะนามสกุลหรือ MIME จาก client
4. ชื่อไฟล์ไทย, ชื่อยาว, จุดหลายตัว, อักขระพิเศษ และชื่อซ้ำไม่ทำไฟล์หาย/ทับกัน
5. ไฟล์ของใบ A ห้ามดาวน์โหลดผ่านใบ B หรือโดย U6
6. ไฟล์แนบของ approved/cancelled ไม่ควรถูกแก้ย้อนหลัง

### Flow 10 — Audit, notification และ side effects

ทุก action สำคัญต้องมี actor, timestamp, action, document id และเหตุผล/หมายเหตุที่เกี่ยวข้อง โดยประวัติเดิมแก้หรือลบไม่ได้

ตรวจ event อย่างน้อย:

- `dsr_name_change_requested` เฉพาะกรณี change ตอน `draft → pending`
- `dsr_cancelled` เมื่อยกเลิกสำเร็จ
- action ที่ fail/403 หรือกดซ้ำต้องไม่สร้าง business event ซ้ำ
- approve สำเร็จต้องไม่แก้ทะเบียนพนักงานและไม่ส่งข้ามระบบตาม DEC-01/DEC-02

## 6. Exploratory cases ที่ FRD 46 เคสยังไม่ระบุชัด

| ID | ลองทำ | สิ่งที่ควรพิสูจน์ |
|---|---|---|
| XR-01 | double-click บันทึก/ส่ง/อนุมัติ/ยกเลิก | ไม่มีเอกสาร, audit, event หรือเลขซ้ำ |
| XR-02 | เปิดสอง tab แก้ draft เดียวกันแล้ว save สลับกัน | มีการป้องกัน lost update หรือแจ้ง conflict |
| XR-03 | approver สอง session ทำรายการพร้อมกัน | มีเพียงผลแรกที่สำเร็จ ผลหลังถูก reject อย่างปลอดภัย |
| XR-04 | session หมดอายุระหว่างกรอกหรือก่อน approve | ไม่เกิด action โดยไม่มีสิทธิ์และผู้ใช้ไม่เข้าใจผิดว่าบันทึกแล้ว |
| XR-05 | refresh/back/forward ระหว่าง wizard | ไม่สร้าง draft หรือเลขเอกสารเพิ่มโดยไม่ตั้งใจ |
| XR-06 | payload ส่ง field ที่ UI ซ่อนอยู่ | server ล้าง/ปฏิเสธค่าที่ไม่สัมพันธ์กับ case kind |
| XR-07 | payload พยายามแก้ requester/owner/status/doc_no | server ไม่รับ mass assignment |
| XR-08 | made_at/ชื่อ/เหตุผลเป็นช่องว่างล้วน, ยาวเกิน limit, emoji, HTML/script | validation ถูกต้องและไม่เกิด XSS ใน list/detail/PDF/CSV |
| XR-09 | เปลี่ยนข้อมูลพนักงานหลังสร้าง draft | เอกสารใช้ snapshot ตามจุดเวลาที่ FRD กำหนดอย่างสม่ำเสมอ |
| XR-10 | เปลี่ยนแผนก/role ของ approver หลัง submit | chain ที่ freeze และสิทธิ์ทำรายการมีพฤติกรรมที่ business ยืนยันแล้ว |
| XR-11 | approver ถูก disable/ลาออกระหว่าง pending | มีทางจัดการ ไม่ค้างถาวรโดยไม่มี audit |
| XR-12 | notification ส่งไม่สำเร็จ | transaction หลักไม่ครึ่งสำเร็จและมี retry/monitoring ที่ตรวจได้ |
| XR-13 | document store ล้มเหลวตอน final approve | ไม่แสดง approved แบบไม่มี PDF ถาวรโดยไม่แจ้ง/กู้คืน |
| XR-14 | CSV ด้วย formula prefix เช่น `=`, `+`, `-`, `@` | ไม่เปิดช่อง CSV formula injection |
| XR-15 | เดา attachment/file id | ถูก authorize ที่ resource ไม่ใช่แค่ document UI |
| XR-16 | เวลาใกล้เที่ยงคืนและสิ้นปี | doc date, audit time, ปีในเลข และ reset ใช้ timezone Asia/Bangkok ถูกต้อง |
| XR-17 | แก้ URL id เป็นค่าที่ไม่มี/รูปแบบผิด | แยก 404/validation อย่างปลอดภัย ไม่ leak รายละเอียด |
| XR-18 | filter + pagination + export หลังข้อมูลเปลี่ยน | total, rows และ CSV สอดคล้อง ไม่ตก/ซ้ำ |
| XR-19 | ชื่อไทย/อังกฤษยาวและฟอนต์ผสม | ไม่ตัดข้อมูลสำคัญใน PDF/CSV แม้ layout ผ่านแล้ว |
| XR-20 | approved/cancelled ถูกเรียก endpoint write โดยตรง | server ปฏิเสธทุก transition ที่ state machine ไม่อนุญาต |

XR-02, XR-03, XR-10, XR-11, XR-12 และ XR-13 เป็น **FRD gap / business decision** หากระบบไม่มีพฤติกรรมกำหนดไว้ ไม่ควรเดา expected result เอง ให้เปิดคำถามกับ BA/PM

## 7. วิธีบันทึกผลต่อหนึ่งเคส

ใช้หนึ่งแถวต่อหนึ่งกฎ/สถานการณ์ ห้ามรวมว่า “flow ผ่านทั้งหมด”:

| Field | บันทึก |
|---|---|
| Case ID | TC-xx หรือ XR-xx |
| Preconditions | env/build, user/role, config, document id/state |
| Steps | ขั้นสั้นที่ทำซ้ำได้ |
| Expected | ข้อความ/ค่า/state ที่ตรวจด้วยตาหรือ response |
| Actual | สิ่งที่เกิดจริง |
| Result | Pass / Fail / Blocked / Not Tested |
| Evidence | screenshot, video, request id, response, notification id |
| FRD ref | FN/VR/BR/DEC/TC ที่รองรับ |
| Bug | BUG-xx และ severity ถ้ามี |

ห้ามใส่ Pass หากตรวจเพียง UI แต่กฎกำหนดให้บังคับที่ service/API ด้วย

## 8. Severity และเกณฑ์หยุด

- **Critical:** ข้ามสิทธิ์, เห็นข้อมูลส่วนบุคคลของคนอื่น, ข้าม approver, ข้อมูลหาย/แก้ผิดคน, state/เลขเอกสารเสีย
- **High:** ผลพิจารณาผิด, approve/reject/cancel ซ้ำ, PDF/CSV ผิดสาระสำคัญ, notification ไปผิดคน, approved แต่ไม่มีหลักฐานเก็บ
- **Medium:** ผิด FRD แต่มี workaround, audit ไม่ครบ, filter/export ไม่ตรงกัน
- **Low:** ข้อความ/ตำแหน่ง/ความเรียบร้อยที่ไม่กระทบการตัดสินใจ

หยุดชุดทดสอบและแจ้งทันทีเมื่อพบ Critical, ข้อมูลจริงเสี่ยงรั่ว, notification ยิงหาคนจริงผิดกลุ่ม หรือ config production ถูกเปลี่ยนโดยไม่ตั้งใจ

## 9. Definition of Done สำหรับการรีวิว

จะสรุปว่า review ครบได้เมื่อ:

1. Gate A มีคำตอบและหลักฐานทุกข้อ
2. TC-01 ถึง TC-46 มีสถานะรายเคส ไม่ใช่สรุปรวม
3. P0/P1 exploratory cases ถูกทดสอบหรือมีเหตุผลว่า Not Tested/Blocked
4. ทุก role ผ่านทั้ง UI และ service-level authorization
5. ทุก state transition ตรวจทั้งข้อมูล, audit, PDF/CSV และ event ที่เกี่ยวข้อง
6. Bug Critical/High ปิดและ retest แล้ว; Medium/Low มี owner และกำหนดรอบ
7. รายงานระบุสิ่งที่ไม่ได้ตรวจอย่างตรงไปตรงมา

## 10. ลำดับทำงานแบบสั้นสำหรับผู้ตรวจ

1. ขอ baseline/config ยืนยันจาก PM/BA
2. เตรียม 6 บัญชีและ test data
3. ทำ happy path 3 case kind
4. ทำ reject/resubmit และ cancel
5. ทำ multi-step approval และ permission matrix
6. ตรวจ PDF/CSV/attachment/audit/notification
7. ทำ negative, direct API และ concurrency ใน UAT
8. ผูกทุก Fail กับ bug ที่ทำซ้ำได้
9. ออกรายงาน Feature Check Report จากผลจริงเท่านั้น

