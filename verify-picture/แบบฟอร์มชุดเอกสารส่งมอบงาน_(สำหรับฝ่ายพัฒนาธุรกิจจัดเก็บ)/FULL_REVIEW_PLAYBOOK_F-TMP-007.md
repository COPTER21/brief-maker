# Full Review Playbook — F-TMP-007

ฟีเจอร์: แบบฟอร์มชุดเอกสารส่งมอบงาน (สำหรับฝ่ายพัฒนาธุรกิจจัดเก็บ)  
วัตถุประสงค์: ตรวจ Logic / Workflow / Permission / Integration / Evidence / ความเสี่ยงทางธุรกิจ หลังขึ้น Production แล้ว  
Baseline หลัก: FRD Pack ของ F-TMP-007 โดยใช้ `05_RULES` และ `06_TESTS` เป็น expected behavior; ใช้ BRD, Governance, Test Case และแบบพิมพ์เพื่อขยายรายละเอียดเท่านั้น

> เอกสารนี้เป็นแผนตรวจ ไม่ใช่ผลตรวจ ทุก Result ต้องมาจากสิ่งที่ผู้ตรวจทำหรือเห็นจริง ห้ามถือว่าผ่านจากผล QA เดิม, prototype, README หรือคำบอกเล่าว่าเคยทดสอบแล้ว

## 1. คำตอบสั้น ๆ ว่าควรตรวจอะไร

ไม่ต้องย้อนตรวจ layout ทั้งหมด แต่ต้องตรวจ 8 แกนนี้:

1. Workflow จริง: ร่าง → รออนุมัติทีละขั้น → อนุมัติแล้ว รวมทั้งตีกลับ → ร่างเลขเดิม → ส่งใหม่ และยกเลิก
2. Business rules: สถานะข้อมูล, สถานะเอกสารรายแถว, จำนวนเอกสารขาด, ข้อจำกัดบังคับ และ warning ที่ต้องเตือนแต่ไม่บล็อก
3. DOA: จำนวนขั้น dynamic, ผู้พิจารณาปัจจุบันเท่านั้นที่ตัดสินได้, ผู้จัดทำอนุมัติเองไม่ได้ และผู้รับมอบต้องเป็นค่าเริ่มของขั้นรับทราบ
4. Permission: ร่างคนอื่นต้องไม่รั่ว; คนนอกสาย/คนผิดขั้นห้ามดูหรือทำ action; admin เห็นและยกเลิกได้แต่แก้ร่างคนอื่นไม่ได้
5. Evidence integrity: เลข HOB, audit, approval snapshot, PDF 2 หน้า, ตารางลงชื่อตาม DOA และ approved final ที่เก็บใน Document Store
6. Integration: Document Configuration, DOA engine, Notification, Document Store และ Document Center ต้องถูกเรียกจริง ไม่ใช่แค่ UI จำลองสำเร็จ
7. Reliability: double-click, retry, stale version, เปิดสอง session และการส่ง request ซ้ำต้องไม่สร้างเลข/การอนุมัติ/notification ซ้ำ
8. Business completeness: หลังรับมอบทั้งที่ยังขาดเอกสาร ระบบช่วยติดตามให้ “ปิด gap” ได้จริงหรือแค่แจ้งแล้วจบ

## 2. สิ่งที่พบจาก context ก่อนเริ่มตรวจ

| Finding | หลักฐานในชุดเอกสาร | ความหมายต่อรอบ Review |
|---|---|---|
| ชุดเอกสารไม่ได้พิสูจน์ Production | `00_อ่านก่อน.md` ระบุไม่มี `e2e_standard` และรอบเดิมเป็น `NO-BROWSER` | ผล QA เดิมหรือไฟล์ UAT ไม่ใช่หลักฐานว่า integration บน Production ทำงานครบ |
| DOA ในเอกสารยังค้าง wire | `DOA_BRIEF` ระบุ `wire_status: pending`, ค่าเริ่ม 2 ขั้น `[DEFAULT — รอยืนยัน]` | ต้องอ่านค่าจริงจาก Production และพิสูจน์ flow ข้ามบัญชี ห้ามสรุปจากหน้าจอผู้จัดทำคนเดียว |
| Document Master ยังมี WARN | `MDOC_BRIEF` ระบุ `taxonomy_def_id: null` และ `doa: pending` | อาจเป็นเอกสารเก่ากว่า deploy; ต้องเทียบค่าจริง ไม่ควรฟันธงเป็น Bug จากเอกสารอย่างเดียว |
| FRD มี OQ ก่อน UAT/Dev/Register | OQ-02, OQ-03, OQ-04, OQ-07 | ขอ PM/BA/Dev ระบุ decision ที่ใช้ตอน deploy หรือเก็บ screenshot/config เป็น baseline รอบนี้ |
| สถานะในเอกสารเรียกไม่เหมือนกัน | FRD ใช้ `pending`; DOA brief บางจุดใช้ `pending_approval` และมี enum `rejected` แต่ locked flow ให้ reject กลับ `draft` | ตัดสินจาก behavior และ locked decision: reject ต้องกลับร่างเลขเดิม; ชื่อ field ภายในไม่ควรเป็นเกณฑ์ UI |
| Permission ของ attachment ไม่ละเอียด | API ระบุ POST/DELETE attachment แต่ FRD ไม่ล็อก role/state ของการเพิ่มหรือลบ | หากเจอพฤติกรรมคลุมเครือให้ลง Gap/OQ ก่อน ไม่ตั้งเป็น Bug จน PM/BA ล็อกกฎ |

ก่อน sign-off ต้องมีคำตอบหรือหลักฐานค่าจริงอย่างน้อย 5 เรื่อง: DOA ที่ wired, role ฝ่ายบริหารการลงทุน, HandoverPackageConfig, doc type `HOB`, และ event/Document Store ที่เปิดใช้จริง

## 3. ขอบเขตและความปลอดภัยในการทดสอบ Production

- ใช้ชื่อโครงการขึ้นต้น `REVIEW-F-TMP-007-YYYYMMDD-` เพื่อค้นหาและเก็บกวาดง่าย
- ใช้บุคคลและเอกสารสมมติ ห้ามแนบเอกสารธุรกิจจริงหรือข้อมูลส่วนบุคคลจริง
- ระบุทุก record ที่สร้าง, เลข HOB, ผู้สร้าง, เวลา และสถานะสุดท้าย
- ไม่แก้ global DOA, Document Configuration, HandoverPackageConfig หรือปิด doc type บน Production เพียงเพื่อทดสอบ เว้นแต่มี change window และผู้มีอำนาจอนุมัติ
- เคส config 1/6 ขั้น, ปิด doc type, concurrent numbering และ tenant isolation ให้ทำใน UAT/Staging หรือใช้ read-only log/config evidence บน Production
- ใบที่ยังไม่จบหลังทดสอบให้ยกเลิกตาม flow พร้อมเหตุผล `Production review cleanup`; ห้ามลบ DB ตรง
- ห้ามทดสอบ API โดยใช้ token ของผู้อื่นหรือ bypass สิทธิ์ที่ไม่ได้รับอนุญาต

## 4. บัญชีและข้อมูลที่ต้องเตรียม

| Code | สิ่งที่ต้องมี |
|---|---|
| MK1 | Maker ฝ่ายพัฒนาธุรกิจ — เจ้าของใบ |
| MK2 | Maker อีกคน — ใช้พิสูจน์ร่างไม่รั่ว |
| CK | ผู้ตรวจสอบขั้น 1 (`role-line-manager`) |
| RC | ผู้รับมอบ/ผู้พิจารณาขั้นรับทราบ (`role-mgr-bu` หรือ role จริงที่ Production ใช้) |
| AD | `admin_role` ฝ่ายพัฒนาธุรกิจ |
| OUT | ผู้ใช้ที่ไม่ใช่เจ้าของ ไม่อยู่ในสาย และไม่ใช่ admin |
| OBS | ผู้มีสิทธิ์ดู network response, audit, notification log และ Document Store แบบ read-only |
| CFG | ผู้ดูแล config สำหรับยืนยันค่าเท่านั้น; การเปลี่ยนค่าทำใน UAT/Staging |

ชุดข้อมูลขั้นต่ำ:

- D1: สถานะข้อมูล “สมบูรณ์”; เอกสาร 2 แถว “ครบถ้วน”
- D2: สถานะข้อมูล “สมบูรณ์”; มี 1 แถว “ขาดเอกสาร” เพื่อพิสูจน์ warning + notification
- D3: สถานะข้อมูลหรือแถวเป็น “มีข้อจำกัด”; ใช้ทดสอบ `ข้อจำกัดของข้อมูล` บังคับ
- D4: วันที่เอกสารหลังวันที่ส่งมอบ 1 วัน; ใช้ทดสอบ warning ที่ไม่บล็อก
- D5: 24 แถว; ใช้ทดสอบ PDF ต่อหน้าและหัวตารางซ้ำ
- F1: ไฟล์ข้อความ/PDF สมมติที่อนุญาต และไฟล์ชนิด/ขนาดที่ policy ไม่อนุญาต

## 5. ลำดับการตรวจที่แนะนำ

### Mission A — Production preflight และ baseline จริง (P0)

1. บันทึก URL/environment, build/version, วันที่เวลา และบัญชีแต่ละ role
2. อ่านค่าจริงของ doc type `HOB`: active, format, reset policy, form revision และ print config
3. อ่านค่าจริงของ HandoverPackageConfig: `data_statuses`, `doc_statuses`, `complete_data`, `limited_data`, `gap_doc`
4. อ่าน DOA resolve ของ MK1: จำนวนขั้น, role, assignee และคำตัดสินแต่ละขั้น
5. ยืนยันว่า RC ที่เลือกในฟอร์มสามารถ map เป็นผู้พิจารณาขั้นรับทราบได้จริง
6. ยืนยัน event catalog มี `hob_cancelled` และ `hob_received_with_gaps`
7. ยืนยัน Document Store รองรับ event `approved_final` ของ doc type HOB

Expected: ค่าจริงต้องเพียงพอให้ flow ทำงานโดยไม่ hardcode; หากเอกสาร context กับ Production ต่าง ให้เก็บ config ปัจจุบันและขอ PM/BA ระบุว่าเป็น approved deployment baseline หรือ config drift

### Mission B — Happy path ครบวงจรแบบข้ามบัญชี (P0)

1. MK1 สร้าง D1; ตรวจผู้ส่งมอบค่าเริ่มเป็น MK1, ผู้รับมอบค่าเริ่มถูกฝ่าย และวันที่เป็นวันนี้
2. เพิ่ม/ลบ/แก้แถว ตรวจลำดับเรียงใหม่และจำนวนรายการสดถูกต้อง
3. บันทึกร่างครั้งแรก; จดเลข HOB และ version
4. แก้ร่างแล้วบันทึกซ้ำ; เลขต้องไม่เปลี่ยนและไม่ออกเลขใหม่
5. กดส่ง; modal ต้องมี slot เท่าจำนวนขั้น DOA, MK1 ไม่อยู่ในรายชื่อผู้พิจารณา และ RC เป็นค่าเริ่มของขั้นรับทราบ
6. Login CK; ต้องเห็นใน “รอฉันพิจารณา” และมีปุ่มของขั้น 1 เท่านั้น
7. CK กด “ตรวจสอบแล้ว”; สถานะยังรอขั้นถัดไปและ CK ตัดสินซ้ำไม่ได้
8. Login RC; กด “รับมอบ / รับทราบ”; สถานะเป็นอนุมัติแล้ว
9. ตรวจ MK1, CK, RC และ AD เห็นผลตามสิทธิ์; OUT ไม่เห็น
10. ตรวจ History ตั้งแต่ create, update, submit, approve step 1, approve step 2 ครบ actor/time/note

Expected สำคัญ: action ทุกขั้นเกิดครั้งเดียว, ลำดับห้ามข้าม, approved แก้และยกเลิกไม่ได้, approval chain เป็น snapshot ของตอนส่ง

### Mission C — Validation, warning และค่าขอบ (P0)

ตรวจทีละกฎเพื่อรู้ว่าจุดใดเสีย:

1. ชื่อโครงการว่าง/ช่องว่างล้วน
2. ผู้ส่งมอบหรือผู้รับมอบว่าง
3. วันที่ส่งมอบ, ฉบับชุดเอกสาร หรือสถานะข้อมูลว่าง
4. ไม่มีรายการเอกสาร; มีแถวแต่ชื่อว่าง; มีชื่อแต่สถานะว่าง
5. D2: “สมบูรณ์” แต่มีแถวขาด/มีข้อจำกัด — ต้องเตือน, นับ gap ถูก และไปต่อได้
6. D3: เว้น “ข้อจำกัดของข้อมูล” — ต้องบล็อกทั้ง UI และ server; กรอกแล้วไปต่อได้
7. D4: วันที่เอกสารหลังวันที่ส่งมอบ — ต้องเตือนระบุแถว แต่บันทึก/ส่งได้
8. ใส่ข้อความไทย/อังกฤษ, emoji, newline, ข้อความยาว และข้อความคล้าย HTML/script ในช่องข้อความ
9. เปลี่ยนสถานะไปมา แล้วกลับมากรอกใหม่; refresh และเปิดแก้ ต้องไม่เกิดค่าเก่าซ่อนค้างผิดกฎ
10. ลบแถวกลาง ตรวจ `seq`, gap count, PDF และ CSV ไม่เหลือข้อมูลแถวที่ลบ

Expected: client/server ใช้กฎเดียวกัน; warning ห้ามกลายเป็น blocker; validation ที่บังคับห้าม bypass ด้วย API

### Mission D — Reject, edit และ resubmit (P0)

1. สร้างและส่งใบใหม่
2. CK กดไม่ผ่านโดยไม่ใส่เหตุผล — ต้องบล็อก
3. CK ใส่เหตุผลแล้วไม่ผ่าน — กลับ `draft`, เลขเดิม, มีแถบเหตุผลและ audit
4. ตรวจ RC มองไม่เห็นร่างที่ถูกตีกลับ และ approval chain เดิมไม่ถูกใช้ตัดสินต่อ
5. MK1 แก้ข้อมูล รวมถึงเปลี่ยน RC แล้วส่งใหม่
6. ตรวจระบบ resolve สายใหม่; ขั้นรับทราบค่าเริ่มต้องเปลี่ยนตาม RC ใหม่
7. ให้ผ่านขั้น 1 แล้ว RC กด “ไม่รับมอบ”; ต้องกลับร่างเลขเดิมพร้อมเหตุผล/audit
8. ส่งรอบสามและอนุมัติครบ; ตรวจ History แยกรอบและไม่สูญเสียเหตุผลเดิม

Expected: reject ไม่มี terminal status `rejected`; ห้ามออกเลขใหม่; chain เก่าย้ายเป็นประวัติและ chain ใหม่ freeze ตอนส่งใหม่

### Mission E — Permission และการรั่วข้อมูล (P0)

1. MK1 สร้างร่าง; MK2, CK, RC และ OUT ค้นหา/กรอง/เปิด URL ตรงด้วย id
2. ผู้ไม่มีสิทธิ์ลอง detail, edit, PDF, attachment, submit, decide และ cancel endpoint ตามขอบเขตที่ได้รับอนุญาต
3. หลังส่ง ให้ CK/RC ที่อยู่ในสายเห็น; คนในสายแต่ไม่ใช่ขั้นปัจจุบันต้องไม่มีปุ่มและตัดสินไม่ได้
4. AD เห็นทุกใบและยกเลิกได้ แต่แก้ร่างของ MK1 ไม่ได้
5. ตรวจ API ตอบ 404 สำหรับใบที่ห้ามรู้ว่ามี และไม่ส่ง payload มาแล้วซ่อนด้วย CSS
6. ตรวจชื่อผู้จัดทำ/ผู้ส่งมอบ/ผู้รับมอบ/ผู้รับผิดชอบไม่รั่วใน search suggestion, error, URL, notification หรือ export ของผู้ไม่มีสิทธิ์
7. หากระบบ multi-tenant มี environment ทดสอบ ให้พิสูจน์ tenant อื่นเปิด id ตรงไม่ได้

Expected: permission ต้องป้องกันที่ server; การไม่มีปุ่มบน UI อย่างเดียวไม่ถือว่าผ่าน

### Mission F — Cancel ทุกสถานะและผู้กระทำ (P0)

1. MK1 ยกเลิกร่างโดยไม่ใส่เหตุผล — ต้องบล็อก; ใส่เหตุผลแล้วเป็น cancelled
2. ส่งใบใหม่แล้ว MK1 ยกเลิกระหว่าง pending — ขั้น pending เป็น skipped และผู้พิจารณาปัจจุบันได้รับ `hob_cancelled`
3. AD ยกเลิกร่าง/ใบรอของ MK1; ตรวจ actor/reason ใน audit
4. CK, RC, MK2 และ OUT ลองยกเลิก — ต้องถูกปฏิเสธ
5. ลองยกเลิก approved, cancelled ซ้ำ และ request ที่ stale

Expected: ยกเลิกได้เฉพาะ owner/admin ใน draft/pending; approved และ cancelled เป็น terminal สำหรับ action นี้

### Mission G — Numbering, idempotency, stale และ race (P1)

ทำใน UAT/Staging หรือภายใต้แผนที่ได้รับอนุมัติ:

1. สอง session บันทึกร่างพร้อมกัน; doc no ต้องไม่ซ้ำ
2. double-click Save/Submit/Approve/Reject/Cancel
3. ส่ง request แล้วตัด network ก่อนรับ response จากนั้น retry ด้วย idempotency key เดิม
4. เปิดร่างเดียวกันสอง session; session A บันทึกก่อน แล้ว session B บันทึก version เก่า
5. CK เปิดใบเดียวกันสองหน้าต่างและตัดสินพร้อมกัน

Expected: mutation มีผลครั้งเดียว; stale ตอบ 409; ไม่มีเลข, audit, approval หรือ notification ซ้ำ

### Mission H — PDF, snapshot และหลักฐานปลายทาง (P0)

1. เปิด PDF ของ draft, pending, approved, cancelled/rejected-returned scenario ตามที่ระบบรองรับ
2. ทุกสถานะต้องเป็น 2 หน้า, มีหน้า N/2, ไม่มี placeholder หรือข้อความล้น/ถูกตัดจนความหมายหาย
3. D5 24 แถว: หน้า 2 ต่อตาราง, หัวตารางซ้ำ, ลำดับและข้อมูลตรงกับจอ
4. ตรวจวันที่เป็น พ.ศ., เลข HOB, form code FM-BDM-07, revision, company header และข้อมูลทุกช่อง
5. ตรวจ sign rows = ผู้จัดทำ + 1 แถวต่อ DOA step; คำตัดสินตรง role และบล็อกลงชื่อไม่ถูกตัดกลางหน้า
6. หลังอนุมัติ ตรวจไฟล์ `approved_final` ถูกเก็บจริงใน Document Store และเปิดได้
7. เปรียบเทียบ PDF ที่ดาวน์โหลดซ้ำ; approved snapshot ต้องไม่เปลี่ยนเพราะ config/ชื่อพนักงานเปลี่ยนภายหลัง
8. ตรวจร่างที่ตีกลับและส่งใหม่ไม่ทำให้หลักฐานรอบก่อนหายจาก audit

Expected: PDF เป็น evidence จาก server truth ไม่ใช่ HTML ฝั่ง client; approved final ต้องสัมพันธ์กับ version ที่อนุมัติจริง

### Mission I — Notification และ integration (P1)

1. อนุมัติ D2 ครบ; MK1 ต้องได้ `hob_received_with_gaps` พร้อมเลขเอกสารและจำนวน gap ถูกต้อง
2. ใช้ data status ไม่สมบูรณ์แต่ไม่มี gap row; ตรวจ event ยังยิงตาม FRD FN-09/NTF brief
3. ยกเลิก pending; เฉพาะ current approver ได้ `hob_cancelled`
4. ตรวจ DOA pending/result ไม่ถูก feature ยิงซ้ำกับ DOA engine
5. double-click/retry action; notification ต้องไม่ซ้ำ
6. กด notification แล้วต้องเปิด record ที่ผู้รับมีสิทธิ์; ผู้ที่สิทธิ์ถูกถอนแล้วต้องเปิดไม่ได้

### Mission J — List, search, filter, pagination และ CSV (P1)

1. สร้างข้อมูลหลายสถานะ/สถานะข้อมูล/เจ้าของ แล้วทดสอบ filter เดี่ยว ผสม และล้าง
2. ตรวจ total, page size 25, pagination และ sort ไม่ทำแถวซ้ำ/หาย
3. `mine_to_act` ต้องนับเฉพาะขั้นปัจจุบันของฉัน
4. ค้นชื่อโครงการและเลข HOB; ตรวจผลตาม permission หลัง filter
5. Export ต้องตรง filter และสิทธิ์ปัจจุบัน ไม่ใช่ export ทุก tenant/ทุก record
6. เปิด CSV จริง ตรวจภาษาไทย, comma, quote, newline และ encoding
7. ทดสอบค่าที่ขึ้นต้น `=`, `+`, `-`, `@` เพื่อดูการป้องกัน CSV formula injection
8. ตรวจไฟล์ไม่มีข้อมูลส่วนบุคคลหรือ field ภายในเกินสิ่งที่หน้ารายการอนุญาต

### Mission K — Attachment และ Document Center (P1)

1. แนบ F1 ตอน draft; ตรวจชื่อไฟล์/ขนาด/ชนิดตาม policy และเปิดดาวน์โหลดได้
2. ลบไฟล์แล้ว refresh; metadata และไฟล์ต้องไม่ค้างผิดสถานะ
3. MK2/OUT เปิด attachment URL ของ MK1 โดยตรง — ต้องไม่ได้
4. ลองเพิ่ม/ลบ attachment ตอน pending/approved/cancelled และโดย AD
5. ตรวจไฟล์อันตราย, double extension, ชื่อยาว, ชื่อภาษาไทย และไฟล์ซ้ำ

Expected ที่ FRD ล็อกไม่ครบ: หาก state/role ของการเพิ่มลบไฟล์ยังไม่มี decision ให้บันทึก `BLOCKED — business rule not defined` ไม่ตัดสินเอง

### Mission L — Dynamic DOA และ config variants (P1, UAT/Staging)

1. ทดสอบ DOA 1, 2 และ 6 ขั้น
2. ตรวจ modal, timeline, current approver, decision word และ PDF sign rows ปรับตามจำนวนขั้น
3. เปลี่ยน DOA หลังส่ง; ใบเดิมต้องใช้ snapshot ใบใหม่ใช้ config ใหม่
4. เปลี่ยน receiver ใน draft; preview ขั้นรับทราบต้องเปลี่ยนตาม
5. ปิด doc type HOB; สร้างใหม่ไม่ได้ 409 แต่ใบเดิมยังดู/พิมพ์ได้
6. เปลี่ยน company header/form revision หลังออกเลข; ใบเก่าใช้ snapshot เดิม ใบใหม่ใช้ค่าปัจจุบัน
7. เปลี่ยน HandoverPackageConfig แล้วพิสูจน์ว่า server อ่าน config ไม่ hardcode และ record เก่าแสดงความหมายไม่เพี้ยน

## 6. Business-sense probes ที่ FRD ยังตอบไม่ครบ

ถ้าระบบทำไม่ตรงรายการนี้ อย่าเพิ่งเรียก Bug ให้ลงเป็น Gap/OQ และส่ง PM/BA/Business Owner ตัดสิน:

1. ใบอนุมัติแล้วถูก lock แต่ยังมีเอกสารขาด — ผู้จัดทำส่งเอกสารเติมอย่างไร, ปิด gap อย่างไร และใครรับรองว่าครบภายหลัง?
2. ถ้าต้องออกชุดใหม่เพื่อเติมเอกสาร ระบบผูกฉบับใหม่กับ HOB เดิมหรือไม่ และฉบับใดเป็น current truth?
3. ช่อง “ฉบับชุดเอกสาร” เป็นข้อความอิสระ — ใครควบคุมเลขฉบับ, การซ้ำ และการ supersede?
4. สถานะ workflow ชื่อ “อนุมัติแล้ว” แต่ธุรกิจคือ “รับมอบ/รับทราบ” — ผู้ใช้จะเข้าใจผิดว่าเนื้อหาครบ/ถูกต้องแล้วหรือไม่?
5. ระบบยอม “สถานะข้อมูลสมบูรณ์” ทั้งที่มีเอกสารขาดโดยแค่เตือน — dashboard/report แยกความขัดแย้งนี้ชัดพอสำหรับผู้บริหารหรือไม่?
6. `hob_received_with_gaps` แจ้งผู้จัดทำครั้งเดียว แต่ไม่มี SLA, due date, escalation หรือผู้รับผิดชอบติดตาม — gap อาจค้างถาวรหรือไม่?
7. FM-BDM-07 ฝั่งพัฒนาธุรกิจกับ FM-BDM-08 ฝั่งบริหารการลงทุนเป็นเอกสารเดียวสองมุมมองหรือคนละฉบับ และต้อง reconcile กันอย่างไร?
8. ผู้รับมอบใน header กับผู้พิจารณาขั้นรับทราบต่างคนกันได้หรือไม่; ถ้าเปลี่ยน assignee ใน modal ใครถือว่าเป็นผู้รับมอบตามกฎหมาย/กระบวนการ?
9. ผู้รับผิดชอบเอกสารเก็บเป็น text snapshot — ถ้าพิมพ์ผิด/พนักงานย้ายฝ่าย ใครตามงานต่อและค้นด้วย employee id ได้หรือไม่?
10. ตำแหน่งจัดเก็บ/ลิงก์ต้องจำกัด domain, ตรวจ URL, อายุลิงก์ และสิทธิ์ปลายทางหรือไม่?
11. Attachment หลังอนุมัติควรถูก lock และ snapshot ไปกับ approved final หรืออนุญาตให้เพิ่มเอกสารภายหลัง?
12. Admin ยกเลิกใบรอได้โดยไม่ผ่านผู้รับมอบ — ต้องมี notification ถึง owner และผู้พิจารณาทุกคนหรือไม่?
13. Retention, legal hold, การลบไฟล์แนบ และ access log ของชื่อบุคคล/เอกสารภายในใช้นโยบายใด?
14. เมื่อพนักงานใน approval chain ลาออกหรือถูกปิดบัญชี ใบรอเดิม reassign อย่างไรโดยยังรักษา audit?
15. เลข HOB และ function/taxonomy code ที่เอกสารเดิมยัง WARN ได้รับอนุมัติจริงก่อน deploy หรือไม่?

## 7. หลักฐานที่ต้องเก็บต่อหนึ่งเคส

- Test ID, เวลา, environment/build, actor/role, record id และเลข HOB
- Config ที่เกี่ยวข้อง ณ เวลาทดสอบ โดยไม่เปิดเผย secret/token
- Screenshot ก่อน/หลังเฉพาะจุดสำคัญและข้อความที่เห็นบนจอ
- HTTP method/path/status/error code เมื่อมีสิทธิ์ตรวจ network
- Actual status, version, current step และ gap count
- Audit/history row ที่สัมพันธ์กับ action
- Notification event id/ผู้รับ/จำนวนครั้ง และ Document Store reference
- PDF/CSV filename และ hash เมื่อใช้พิสูจน์ snapshot
- Result: PASS / FAIL / BLOCKED / NOT RUN
- หาก FAIL: steps ทำซ้ำ, Expected จาก FRD ข้อใด, Actual, severity, workaround และขอบเขต record ที่อาจกระทบ

## 8. เกณฑ์ Severity และ Sign-off

- Critical: ข้ามสิทธิ์/tenant, คนผิดขั้นอนุมัติได้, approved ถูกแก้ได้, เลขซ้ำ, audit/PDF evidence สูญหายหรือปลอมความจริง, ข้อมูลเสียจาก retry
- High: state transition ผิด, reject ไม่กลับร่างเลขเดิม, gap/ข้อจำกัดคำนวณผิด, PDF/ผู้ลงชื่อผิด, final PDF ไม่ถูกเก็บ, notification สำคัญไม่ถึงผู้รับ
- Medium: validation, filter, CSV, attachment, history หรือ warning ผิดแต่ไม่ทำให้ผลรับมอบ/หลักฐานผิดและมีทางเลี่ยง
- Low: ข้อความ/ความเรียบร้อยที่ไม่กระทบ decision, permission, evidence หรือข้อมูล

ห้าม sign off เมื่อ:

- ยังมี Critical
- มี High ที่ยังไม่แก้หรือไม่มีผู้มีอำนาจยอมรับความเสี่ยง
- Mission P0 มี `BLOCKED`/`NOT RUN` โดยไม่มี owner และกำหนดปิด
- ยังพิสูจน์ DOA, Document Store หรือ notification บน environment ที่ deploy จริงไม่ได้
- ไม่มีหลักฐานว่ากฎ permission ถูกบังคับที่ server

## 9. Execution sheet

| Run | Mission | Actor | Record / Doc No. | Expected | Actual | Result | Evidence | Bug/OQ |
|---|---|---|---|---|---|---|---|---|
| 1 | A — Production preflight | CFG/OBS |  | config/wiring พร้อมตาม FRD |  | NOT RUN |  |  |
| 2 | B — Happy path | MK1/CK/RC |  | draft→pending→approved ตามลำดับ |  | NOT RUN |  |  |
| 3 | C — Validation/warnings | MK1 |  | VR-01..07 + warning ไม่บล็อก |  | NOT RUN |  |  |
| 4 | D — Reject/resubmit ขั้น 1 | MK1/CK |  | กลับ draft เลขเดิม |  | NOT RUN |  |  |
| 5 | D — ไม่รับมอบ/resubmit ขั้น 2 | MK1/CK/RC |  | กลับ draft เลขเดิม + chain ใหม่ |  | NOT RUN |  |  |
| 6 | E — Permission/server deny | MK1/MK2/CK/RC/AD/OUT |  | ตาม §5.3 และ TC-D01..07 |  | NOT RUN |  |  |
| 7 | F — Cancel | MK1/CK/RC/AD/OUT |  | owner/admin เฉพาะ draft/pending |  | NOT RUN |  |  |
| 8 | G — Idempotency/stale/race | MK1/CK |  | mutation ครั้งเดียว + 409 stale |  | NOT RUN |  |  |
| 9 | H — PDF/evidence | MK1/CK/RC/OBS |  | 2 หน้า + sign rows dynamic + final stored |  | NOT RUN |  |  |
| 10 | I — Notification/integration | MK1/CK/RC/OBS |  | event/recipient/count ถูกและไม่ซ้ำ |  | NOT RUN |  |  |
| 11 | J — List/filter/CSV | MK1/AD |  | filter/permission/export ตรงกัน |  | NOT RUN |  |  |
| 12 | K — Attachment | MK1/MK2/OUT |  | policy/permission ตาม rule ที่ยืนยัน |  | BLOCKED |  | Attachment rule |
| 13 | L — DOA/config variants | CFG/MK1/OBS |  | dynamic + snapshot; ทำ UAT/Staging |  | NOT RUN |  |  |
| 14 | Business gap closure | PM/BA/Owner |  | ตอบข้อ 6.1–6.15 ที่มีผลต่อ sign-off |  | NOT RUN |  |  |

## 10. เอกสารเดิมที่ควรเปิดคู่กัน

- `_frd/.../05_RULES_...md` — business rule, state, permission, validation, edge case
- `_frd/.../06_TESTS_...md` — acceptance 13 ข้อ + deny 7 ข้อ
- `_frd/.../03_LOGIC_...md` — FN-01..10 และ integration behavior
- `_frd/.../02_API_...md` — endpoint, idempotency, optimistic lock และ error code
- `_frd/.../07_LOCKED_DECISIONS_...md` — decision ที่ห้ามตีความสวน
- `_tc/TC_...md` — ขั้นตอนทดสอบเดิม 30 เคส ใช้เป็น checklist เสริม
- `_governance/DOA_BRIEF_...md`, `DOCCFG_BRIEF_...md`, `NTF_BRIEF_...md`, `MDOC_BRIEF_...md` — จุด wiring ที่ต้องพิสูจน์กับ Production

## 11. วิธีใช้ playbook นี้ให้จบงาน

1. เริ่ม Mission A และขอ PM/BA ยืนยันค่าที่ deploy จริง
2. ทำ P0 ก่อน: B, C, D, E, F, H
3. ทำ P1: G, I, J, K, L ตาม environment ที่ปลอดภัย
4. ทุก FAIL ผูกกับ FRD rule/AC/FN และเปิด Bug ที่ทำซ้ำได้
5. ทุกเรื่องที่ FRD ไม่ล็อกให้เปิด OQ/Gap แทน Bug
6. เมื่อมีผลจริงครบแล้วจึงสร้าง Feature Check Report รอบ 1; ห้ามนำไฟล์แผนนี้ไปใช้เป็นใบรับรองว่าผ่าน
