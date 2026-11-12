# Logic & Business Review Guide — F-TMP-008 ใบรายงานการแก้ไขและป้องกันเพื่อการควบคุม (CAR)

วันที่จัดทำ: 12 พฤศจิกายน 2569  
ฐานอ้างอิงหลัก: FRD-F-TMP-008 v1.0 (`00_OVERVIEW` ถึง `07_LOCKED_DECISIONS`)  
วัตถุประสงค์: ตรวจรอบเก็บตกบนระบบ Production โดยเน้น business logic, workflow, permission, data integrity, integration และผลลัพธ์เอกสาร ไม่ตรวจความสวยงามของ layout ซ้ำ

## 1. ข้อสรุปก่อนเริ่ม

การอิง FRD เป็นหลักตามที่ PM/BA กำหนดเป็นแนวทางที่ถูกต้อง แต่ต้องอิงแบบมี version และหลักฐาน sign-off ไม่ใช่ถือทุกข้อความใน pack ว่าเป็นข้อยุติ เพราะ FRD ชุดนี้ระบุเองว่า:

- รหัส `F-TMP-008` เป็นรหัสชั่วคราว
- DEC-01..28 เป็น `AI-DEFAULT` และรอลูกค้ายืนยัน
- OQ-02/03 ต้องปิดก่อน Ready for Dev แต่ยังปรากฏใน Open Questions
- DOA brief มี verdict `WARN`, `wire_status: pending` และ role บางตัวไม่อยู่ใน contract
- API/DB ยังมีข้อความ `TODO: DOA engine`
- DevPack ถูกสร้างในโหมด NO-BROWSER และไม่มี `e2e_standard` report

ดังนั้นหน้าที่ของผู้ review รอบนี้มี 2 ชั้น:

1. พิสูจน์ว่าระบบทำงานตรงกับ FRD/version/config ที่ Production ใช้จริง
2. ใช้ business sense หา failure mode ที่ test case ปกติไม่ครอบ แต่ถ้า FRD ไม่ได้ตัดสินไว้ ให้รายงานเป็น `Requirement question / Business risk` ก่อน ไม่ควรฟันธงเป็น bug

จุดเสี่ยงสูงสุดของฟีเจอร์นี้คือ:

1. การออกเลข CAR ครั้งแรกและความไม่ซ้ำเมื่อกดซ้ำหรือสร้างพร้อมกัน
2. การแยกหน้าที่ผู้จัดทำ, ผู้ตรวจสอบ IC, ผู้ลงนามตรวจสอบ 7 จุด และผู้อนุมัติ DOA
3. การตีกลับ/ไม่อนุมัติแล้วกลับร่างเลขเดิม ล้างลายเซ็น แต่เก็บ audit เดิม
4. DOA แบบ dynamic, freeze สายเดิม และ resolve สายใหม่เมื่อส่งรอบใหม่
5. การคำนวณจำนวน/% ทั้งช่วงการจัดทำและ 6.3 รวมถึง warning ที่ต้องไม่กลายเป็น block
6. สิทธิ์มองเห็น route, PDF, attachment และ CSV โดยเฉพาะร่างที่ถูกส่งกลับ
7. PDF final, snapshot, จุดลงนาม และจำนวนช่องตาม DOA
8. notification ที่ต้องไปถูกคน ถูก event และไม่ซ้ำ
9. concurrency/double action ที่อาจทำให้สถานะ, audit หรือลายเซ็นเสียหาย

## 2. Baseline ที่ต้องขอ PM/BA/Dev ยืนยัน

- [ ] FRD-F-TMP-008 v1.0 ลงวันที่ 10 ต.ค. 2569 คือ baseline ของ Production build ที่กำลังตรวจจริง
- [ ] มี sign-off หรือ ticket ยืนยัน DEC-01..28 ที่เป็น `AI-DEFAULT`; ถ้ามี decision ใหม่กว่าให้แนบและใช้ฉบับใหม่
- [ ] รหัส feature จริงใน Production คืออะไร และ endpoint/permission ใช้รหัสชั่วคราวหรือรหัสจริง
- [ ] OQ-02 และ OQ-03 ปิดด้วยคำตอบอะไร โดยเฉพาะ role `role-md`, `role-ic-officer`, `role-ic-mgr`, `role-line-manager`
- [ ] DOA กลางถูก wire แล้วหรือไม่; entry ปัจจุบันมีกี่ขั้น, ใครเป็นผู้รับ, และ `wire_status` เปลี่ยนจาก pending แล้วหรือยัง
- [ ] ค่า `CarConfig.analysis_start_minutes` บน Production ปัจจุบันเท่าไร
- [ ] `doc_type=CAR` ใช้ format/reset/revision/template ใด และสถานะเปิดใช้อยู่หรือไม่
- [ ] OQ-05 ตกลงอย่างไรเมื่อข้อมูลยาวเกิน 2 หน้า
- [ ] OQ-06 ตกลงว่าใครเป็นผู้กรอกค่า 6.3 และแก้ไขได้ในสถานะใด
- [ ] file policy กลางกำหนดชนิด ขนาด จำนวนไฟล์ และการลบไฟล์ไว้อย่างไร
- [ ] อนุญาตให้สร้าง test data บน Production หรือไม่, ใช้บัญชีใด, ปิด notification จริงอย่างไร และล้าง/ยกเลิกข้อมูลหลังทดสอบอย่างไร

ถ้าข้อใดมีผลต่อ expected result แล้วยังไม่มีคำตอบ ให้ลงผล `Blocked — baseline/config ไม่ครบ` ไม่ใช้ Pass/Fail

## 2.1 Source conflicts ที่ต้องปิดก่อนฟันธง bug

| ID | เอกสารที่ขัดกัน | ประเด็นที่ต้องให้ PM/BA/Dev ยืนยัน |
|---|---|---|
| BC-01 | `03_LOGIC FN-08`, state machine และ `05_RULES BR-08` เทียบกับ `DOA_BRIEF §4/§5` | FRD หลักบอกส่งอนุมัติจาก `in_review` หลังลงนามครบ 7 จุด แต่ DOA brief บางบรรทัดบอกส่งได้เฉพาะ `draft`/ปุ่มส่งอนุมัติใน draft |
| BC-02 | `03_LOGIC FN-12` เทียบกับ `DOA_BRIEF §5.1` | FN-12 บอกช่องข้อ 12 มาจาก approval chain และ “ไม่มีช่องผู้จัดทำ” แต่ DOA brief บอก “ผู้ขอ + 1 ช่องต่อขั้น” |
| BC-03 | `04_DB`/state machine เทียบกับ DOA/NTF declaration | สถานะหลักใช้ `pending` แต่ declaration ใช้ `pending_approval`; ต้องยืนยัน mapping จริงและไม่ให้ filter/event พลาด |
| BC-04 | `03_LOGIC FN-11`/`05_RULES §5.6` เทียบกับ `NTF_BRIEF` | ยกเลิกจาก `in_review` ควรแจ้ง reviewer ส่วน `pending` แจ้ง current approver แต่ NTF table ระบุ recipient แบบ current approver เป็นหลัก |
| BC-05 | `00_OVERVIEW` | สถานะเขียน Ready for Dev หลัง OQ-02/03 ปิด แต่ Open Questions และ DOA quality gate ยังระบุว่ายังไม่ยืนยัน |

สิ่งเหล่านี้เป็น defect ของ specification/traceability ก่อน ยังไม่ใช่หลักฐานว่าระบบ Production ผิด

## 2.2 Finding จากการตรวจ Production

### CAR-LOGIC-001 — Upload file แล้วกดบันทึกเกิด API error

**สถานะ:** Candidate defect — ต้องยืนยัน Network request/response ก่อนออก Feature Check Report  
**ระดับเสนอ:** Medium หากยังบันทึกข้อมูลได้ด้วยการไม่แนบไฟล์หรือมีทางเลี่ยง; High หากไฟล์เป็นส่วนจำเป็นหรือทำให้ create/edit ใช้งานไม่ได้  
**อ้างอิง:** `02_API API-03`, `API-04`, `API-13` และ `00_OVERVIEW §0.3`

**สิ่งที่ผู้ตรวจพบ**

- Create, Edit และ View drawer เลือก upload file ได้
- เมื่อกดบันทึก ระบบเกิด API error
- ผู้ตรวจสังเกต payload คล้าย `{file: {}}`

**ข้อวิเคราะห์**

`{file:{}}` ยังไม่ยืนยัน bug เพียงลำพัง เพราะ JavaScript `File` object เมื่อผ่าน `JSON.stringify()` มักกลายเป็น `{}` แม้ตัวไฟล์จะยังอยู่ใน `FormData` ได้ ต้องดู request จริงใน Network:

- ถ้า `Content-Type: application/json` และ Request Payload เป็น `{"file":{}}` จริง → frontend serialize ไฟล์ผิด
- ถ้า `Content-Type: multipart/form-data; boundary=...` และ Form Data แสดงชื่อไฟล์/type/size หรือ `(binary)` → payload ไฟล์อาจถูกต้อง ต้องดู status และ response error ต่อ

ตาม FRD การบันทึก CAR และ upload เป็นคนละ API: `POST /car` หรือ `PUT /car/{id}` เก็บข้อมูลเอกสาร ส่วนไฟล์ต้องส่งแยกด้วย `POST /car/{id}/attachments` แบบ multipart หลังมี `car_id` แล้ว ไม่ควรฝัง raw `File` object ลง JSON ของ create/edit

**ขั้นตอนทำซ้ำและหลักฐานที่ต้องเก็บ**

1. เปิด DevTools → Network และเปิด Preserve log
2. Create CAR ใหม่ เลือกไฟล์ PDF ขนาดเล็ก แล้วกดบันทึก
3. เก็บลำดับ request ทั้งหมดว่าเรียก `POST /car` ก่อนหรือเรียก attachment ก่อนมี id
4. เปิด request ที่ fail แล้วเก็บ URL, method, status code, Request Headers, Payload/Form Data และ Response body
5. ทำซ้ำใน Edit และ View drawer ด้วยไฟล์เดียวกัน เพื่อดูว่าใช้ endpoint/service เดียวกันหรือไม่
6. ทำ control case โดยไม่เลือกไฟล์; ถ้าบันทึกได้ แสดงว่าปัญหาผูกกับ attachment path
7. ทำ control caseด้วยไฟล์ `.exe` และไฟล์เกินขนาด เพื่อแยก 415/413 ที่เป็น expected behavior

**Expected flow**

- Create: บันทึก CAR ให้ได้ `id` ก่อน แล้ว upload ด้วย `/car/{id}/attachments` แบบ multipart; หาก upload ล้มเหลวต้องแจ้งเฉพาะไฟล์และไม่ทำข้อมูล CAR สูญหายหรือสร้างซ้ำ
- Edit/View drawer: ส่งไฟล์ไป attachment endpoint โดยมี `car_id`; ไม่ส่ง raw File ใน JSON ของ `PUT /car/{id}`
- Request multipart ต้องมี filename/content type/binary และห้ามตั้ง `Content-Type` เองโดยไม่มี boundary

**เกณฑ์ตัดสิน**

- Confirmed frontend defect: request เป็น JSON `{"file":{}}`, ไม่มี multipart boundary หรือเรียก upload ก่อนมี `car_id`
- Confirmed backend/contract defect: multipart ถูกต้องแต่ endpoint ปฏิเสธไฟล์ที่ policy อนุญาต หรือ response ไม่ตรง 413/415/permission contract
- UX/transaction defect เพิ่มเติม: CAR ถูกสร้างซ้ำ, ข้อมูลที่กรอกหาย, toast บอกบันทึกสำเร็จทั้งที่ upload ล้มเหลว หรือ upload สำเร็จแต่ไฟล์ไม่ผูกกับ CAR
- Not a defect: request ถูกต้องและ response เป็น 413/415 จากไฟล์ที่เกิน policy/ชนิดไม่รองรับ พร้อมข้อความผู้ใช้ที่ถูกต้อง

## 3. บัญชีและข้อมูลทดสอบที่ต้องเตรียม

ควรมี identity แยกเพื่อพิสูจน์ SoD และ permission อย่างน้อยดังนี้ (คนเดียวอาจถือหลาย role ในระบบจริง แต่บัญชีทดสอบควรแยกเมื่อทำได้):

| บัญชี | บทบาท | ใช้พิสูจน์ |
|---|---|---|
| U1 | ผู้จัดทำ แผนก A | สร้าง/แก้ร่าง/ส่ง/ยกเลิก/เห็นของตน |
| U2 | ผู้ตรวจสอบ IC | กรอกช่วงตรวจสอบ, ตีกลับ, ส่งอนุมัติ |
| U3 | HOD/line manager ของ U1 | ลงนามจุด HOD และ/หรือ DOA ขั้น 1 |
| U4 | MD | ลงนาม 2 จุดและพิจารณาเฉพาะขั้นของตน |
| U5 | IC Manager | ลงนาม 4 จุดและพิจารณาเฉพาะขั้นของตน |
| U6 | ผู้ใช้ทั่วไปที่ไม่เกี่ยวข้อง | direct URL/data leakage/deny |
| U7 | admin role IC | เห็นทุกใบและยกเลิกตามสิทธิ์ แต่ห้ามอนุมัติแทนโดยไม่มี DOA |
| U8 | ผู้ใช้ต่างบริษัท/tenant | tenant isolation ถ้าระบบรองรับ |

เตรียมเอกสารอย่างน้อย 10 ใบ: ร่างขั้นต่ำ, ร่างข้อมูลเต็ม, รอตรวจสอบ, ลงนามบางส่วน, รออนุมัติขั้น 1, รอขั้นกลาง, ใบตีกลับจาก review, ใบ reject จาก DOA, ใบ approved, ใบ cancelled และใบข้อความ/ตารางยาว

หลักฐานขั้นต่ำต่อเคส: environment/build, user/role, เลข CAR, เวลา, precondition/config, input สำคัญ, expected พร้อม FRD ref, actual, screenshot ก่อน–หลัง และ request/response หรือ audit/log เมื่อเข้าถึงได้

## 4. ลำดับทดสอบแบบ End-to-End

อย่ารันเฉพาะเคสสั้นแยกกัน เพราะ bug สำคัญมักเกิดจากข้อมูลค้างข้ามสถานะ ให้ทำ flow ต่อเนื่องดังนี้

### Flow A — Draft, validation และ calculation

- [ ] U1 เปิดสร้างแล้วปิดก่อนบันทึก ต้องยังไม่ใช้เลข CAR
- [ ] กรอกเฉพาะข้อมูลขั้นต่ำของการบันทึกร่าง แล้วบันทึกครั้งแรก ได้เลขจาก Document Config เพียงเลขเดียว
- [ ] กดบันทึกซ้ำ/รีเฟรช/retry ต้องไม่ออกเลขใหม่หรือสร้างใบซ้ำ
- [ ] กรอก `total_qty=40`, อาการ qty=6 ต้องได้ 15.00%; ตรวจ 6.3 แบบเดียวกัน
- [ ] เปลี่ยน `total_qty` แล้วทุก % และผลรวมต้องคำนวณใหม่จาก server ไม่เชื่อค่าที่ client ส่ง
- [ ] `total_qty` ว่างหรือ 0 ต้องแสดง % ว่างและไม่เกิดหารศูนย์
- [ ] ผลรวม qty หรือ eff_qty เกิน total ต้องเตือนแต่ยังบันทึก/ส่งได้หาก required อื่นครบ
- [ ] วันเวลาที่พบในอนาคตต้อง block; เกินเกณฑ์เวลาเริ่มวิเคราะห์ต้อง warning ไม่ block
- [ ] เกิดใหม่กับเกิดซ้ำต้อง mutually exclusive ตาม BR-05
- [ ] ส่งตรวจสอบโดยขาด required ทีละรายการ ต้อง block และชี้รายการที่ขาดจริง

### Flow B — Happy path ครบวงจร

- [ ] U1 ส่งตรวจสอบ ระบบ resolve reviewer, ผู้ลงนาม 7 จุด และ DOA ตาม config ปัจจุบัน
- [ ] สถานะเป็น `in_review`; U2 และผู้ลงนามเห็นใบ แต่ผู้ไม่มีส่วนเกี่ยวข้องไม่เห็น
- [ ] U2 กรอกช่วงการตรวจสอบและข้อ 10; U1 แก้ช่วงนี้ไม่ได้
- [ ] U3 ลงนาม HOD 1 จุด, U4 ลงนาม MD 2 จุด, U5 ลงนาม IC Mgr 4 จุด; count ต้องรวมเป็น 7/7
- [ ] ก่อนครบ 7 จุดส่งอนุมัติไม่ได้ทั้ง UI และ API
- [ ] U2 ส่งอนุมัติเมื่อครบ 7 จุด; DOA ขั้น 1 pending เพียงขั้นเดียว
- [ ] ผู้อนุมัติแต่ละขั้นอนุมัติตามลำดับ; ขั้นถัดไปห้ามกดก่อนถึงคิว
- [ ] ครบขั้นแล้ว status approved, lock การแก้ไข, เก็บ PDF `approved_final` และไม่มี downstream action ที่อยู่นอก scope

### Flow C — ตีกลับจาก Review

- [ ] U2 ตีกลับโดยไม่กรอกเหตุผลต้อง block
- [ ] ตีกลับพร้อมเหตุผลแล้วกลับ `draft` ด้วยเลขเดิม
- [ ] ล้าง `car_review_signs` และ approval chain ปัจจุบัน แต่ audit รอบเดิมต้องยังอยู่
- [ ] U1 เห็นเหตุผลและได้รับ `car_review_returned` เพียงครั้งเดียว
- [ ] reviewer/approver เดิมต้องไม่เห็นร่างที่ถูกตีกลับ เว้นแต่มี admin role
- [ ] แก้แล้วส่งใหม่ต้อง resolve reviewer/signers/DOA ใหม่และเริ่มวงจรใหม่

### Flow D — Reject จาก DOA แล้วส่งใหม่

- [ ] ผู้อนุมัติขั้นปัจจุบัน reject โดยไม่ใส่เหตุผลต้อง block
- [ ] reject พร้อมเหตุผลแล้วกลับ draft เลขเดิมและล้างลายเซ็นตรวจสอบทั้ง 7 จุด
- [ ] approval decision/chain เดิมยังอยู่ใน audit แบบ append-only
- [ ] เปลี่ยน DOA config ก่อนส่งใหม่ แล้วตรวจว่าสายใหม่ถูก resolve แต่เอกสารที่ยัง pending เดิมไม่เปลี่ยนสาย
- [ ] ส่งใหม่ต้องกลับผ่าน review และลงนาม 7 จุดใหม่ ห้ามข้ามตรงไป approval

### Flow E — Cancel ทุกสถานะที่อนุญาต

- [ ] Owner/Admin ยกเลิก draft, in_review, pending ได้เมื่อมีเหตุผล
- [ ] reviewer/signer/current approver ที่ไม่ใช่ owner/admin ยกเลิกเองไม่ได้
- [ ] pending step เปลี่ยนเป็น skipped/หยุดดำเนินการ และ approve ต่อไม่ได้
- [ ] ยกเลิกจาก in_review แจ้ง reviewer; ยกเลิกจาก pending แจ้ง current approver; ต้องไม่ส่งผิดคนหรือซ้ำ
- [ ] approved ยกเลิกไม่ได้ทั้ง UI และ direct API

### Flow F — Permission และข้อมูลรั่วไหล

- [ ] U6 ค้นเลข, เปิด route ตรง, PDF URL, attachment URL และ export CSV แล้วต้องไม่เห็นข้อมูล
- [ ] ร่างเห็นเฉพาะ owner และ admin role IC; reviewer/signer/approver เริ่มเห็นหลังส่งตาม FN-14
- [ ] ผู้ลงนามแต่ละ role ลงได้เฉพาะจุดของตน; MD ลงจุด IC Mgr ต้อง 403 `NOT_SIGNER`
- [ ] owner ที่บังเอิญ map เป็น signer/approver ต้องถูก block ด้วย SoD
- [ ] approver ขั้นถัดไปอาจเห็นใบหลังส่ง แต่ action approve/reject ต้องไม่มีและ API ต้อง 403
- [ ] U7 เห็นทุกใบในบริษัท แต่ไม่อนุมัติแทน current approver หากไม่ได้อยู่ใน chain
- [ ] U8 ห้ามเห็น list/count/PDF/attachment/CSV ของอีก tenant แม้เดา UUID หรือ URL ได้

### Flow G — Concurrency และ idempotency

- [ ] เปิดร่างสองแท็บ: A บันทึกก่อน, B บันทึกทีหลังต้อง 409 STALE และไม่ทับข้อมูล A
- [ ] ดับเบิลคลิกบันทึกครั้งแรกต้องได้เลขเดียวและ record เดียว
- [ ] ดับเบิล submit-review ต้องเกิด transition/notification/ชุด signer/approval chain ชุดเดียว
- [ ] signer เปิดสองหน้าต่างแล้วลงนามพร้อมกัน ต้องได้ signature เดียวต่อ point
- [ ] approver กด approve ซ้ำหรือสองหน้าต่าง ต้องได้ decision เดียวและไม่ข้ามขั้น
- [ ] cancel พร้อมกับ approve ต้องจบเพียงสถานะเดียว พร้อม audit ที่อธิบายผลได้
- [ ] network timeout/500 ต้องไม่ทิ้ง partial state, partial chain, PDF หรือ notification ที่ไม่สอดคล้องกับสถานะ

## 5. Checklist รายหมวดตาม FRD

### 5.1 Validation และ boundary values

- [ ] ผู้พบปัญหาว่าง → `ระบุผู้พบปัญหา`
- [ ] วันที่ว่าง → `เลือกวันที่พบปัญหา`
- [ ] เวลาไม่ใช่ HH:MM, `24:00`, `12:60`, ตัวอักษร และช่องว่างล้วนต้องถูกปฏิเสธ
- [ ] ทดสอบเวลาเท่ากับปัจจุบัน/ก่อน 1 นาที/หลัง 1 นาที และ timezone ของ server เทียบ browser
- [ ] หัวข้อปัญหาว่างหรือช่องว่างล้วนต้อง block
- [ ] จำนวนลอง `-1`, `0`, `1`, `1.5`, `01`, ค่าสูงมาก, ตัวเลขไทย และข้อความ; ต้องรับเฉพาะจำนวนเต็ม ≥0 ตาม FRD
- [ ] เกิดใหม่=true ต้องล้าง/ไม่ส่งค่า recur_no เก่า; เกิดใหม่=false ต้อง recur_no ≥1
- [ ] อาการที่มีแต่ช่องว่างต้องไม่นับเป็นหนึ่งแถว
- [ ] มี Why 2/3 แต่ระดับก่อนหน้าไม่มี proven=true ต้อง warning ไม่ block
- [ ] ไม่มี root cause proven=true ต้อง block ตอน submit-review
- [ ] due date ก่อน found_date ต้อง warning ไม่ block
- [ ] ภาษาไทย/อังกฤษ, emoji, quote, newline, `<script>` และข้อความยาวต้องเก็บ/แสดง/PDF โดยไม่เพี้ยนหรือ execute

### 5.2 Calculation และ data integrity

- [ ] % ปัด 2 ตำแหน่ง เช่น 1/3 = 33.33 และผลรวมใช้ผลรวมค่าจริงตาม FRD ไม่บังคับเป็น 100
- [ ] qty หลายแถวรวมเท่ากับ/ต่ำกว่า/สูงกว่า total ให้ warning ถูกเงื่อนไข
- [ ] qty และ eff_qty ต้องคำนวณแยกกัน ไม่เอาค่าชุดหนึ่งไปทับอีกชุด
- [ ] ลบ/เรียง/เพิ่มแถวแล้ว seq, ผลรวม และ PDF ต้องตรงหน้าจอ
- [ ] ปลอมค่า pct ใน request แล้ว server ต้องคำนวณใหม่
- [ ] reopen/refresh แล้วค่าคำนวณต้องตรงก่อน refresh
- [ ] ข้อมูลช่วง prep กับ rev ต้องไม่ปนหรือเขียนทับกัน

### 5.3 เลขเอกสารและ Document Config

- [ ] เลขออกตอนบันทึกครั้งแรก ไม่ใช่ตอนเปิดฟอร์มหรือตอน submit
- [ ] สร้างพร้อมกันอย่างน้อย 2 ผู้ใช้ เลขต้อง unique ภายใน company
- [ ] format `CAR-{YYYY}-{run:4}`/ปี/การ reset ต้องตรง config จริง ไม่ hardcodeจาก FRD ตัวอย่าง
- [ ] ปิด doc_type CAR: ปุ่มสร้าง disabled และ API ตอบ 409 `DOC_TYPE_INACTIVE`
- [ ] rejected/returned/resubmitted ใช้เลขเดิมเสมอ
- [ ] ยกเลิกร่างแล้วเลขขาดได้ เพราะ declaration ระบุ no-gap=false; ไม่ถือเป็น bug
- [ ] เปลี่ยนชื่อบริษัท/โลโก้/หน่วยงานหลังออกเลข เอกสารเดิมต้องใช้ header/department snapshot เดิม

### 5.4 Review signs และ DOA

- [ ] resolve ผู้ลงนาม 7 จุดถูกคนตาม owner organization และ role master
- [ ] คนเดียวถือหลายจุดลงนามพร้อมกันได้ แต่ระบบต้องเก็บ point แยกและเวลา/actor ถูกต้อง
- [ ] signer ถูก disable/ย้ายแผนกหลัง resolve: พฤติกรรมต้องมีข้อยุติจาก BA/DOA ไม่ควรเดา
- [ ] จำนวน slot DOA เท่ากับ config จริง และ PDF ปรับตามจำนวนขั้น
- [ ] assignee ทุกขั้นต้องครบและไม่ใช่ owner; resolve ไม่ได้ต้อง block พร้อมข้อความที่แก้ไขได้
- [ ] เปลี่ยน DOA หลัง submit ไม่เปลี่ยน chain ของใบเดิม
- [ ] reject/resubmit ต้อง resolve chain ใหม่ ไม่ reuse chain เก่า
- [ ] approver ซ้ำหลายขั้น, approver เป็น reviewer/signer และ owner ไม่มี line manager เป็น business probes ที่ต้องถาม BA หาก FRD ไม่ชัด
- [ ] audit ระบุ actor, role, point/step, decision, note และเวลาอย่างถูกต้อง

### 5.5 List, search, filter และ CSV

- [ ] แท็บทั้งหมด/รอฉันดำเนินการ/รายงานของฉันตรง FN-14 สำหรับทุก role
- [ ] `รอฉันดำเนินการ` รวม reviewer, signer ที่ยังไม่ลง และ current approver เท่านั้น
- [ ] ค้นด้วยเลข CAR, ผู้จัดทำ, หัวข้อ, DOC NO.; ลองบางคำ, ไทย/อังกฤษ, space และไม่พบ
- [ ] filter status+department ทำร่วมกันได้; reset/pagination/count ถูกหลังสถานะเปลี่ยน
- [ ] badge/count ต้องนับเฉพาะข้อมูลที่ user มีสิทธิ์เห็น
- [ ] CSV เคารพ filter และ permission, UTF-8 BOM ภาษาไทยไม่เพี้ยน
- [ ] ค่าเริ่ม `=`, `+`, `-`, `@` ต้องไม่ทำให้เกิด CSV formula injection
- [ ] PII เช่น found_by/attendees ต้องไม่รั่วไป role/tenant ที่ไม่มีสิทธิ์

### 5.6 Attachment

- [ ] owner แนบไฟล์ที่อนุญาตได้และเปิด/ดาวน์โหลดกลับได้
- [ ] `.exe` ต้อง 415; ไฟล์เกินขนาดต้อง 413; ตรวจ MIME จริง ไม่ใช่เฉพาะนามสกุล
- [ ] ไฟล์ชื่อไทย/ยาว/ซ้ำ/อักขระพิเศษต้องไม่ทับไฟล์อื่น
- [ ] upload ล้มเหลวต้องไม่เหลือ metadata หรือไฟล์ orphan ที่หน้าแสดงผิด
- [ ] คนไม่มีสิทธิ์และ tenant อื่นห้ามเปิด direct URL
- [ ] สิทธิ์เพิ่ม/ลบไฟล์ใน draft/in_review/pending/approved/cancelled ต้องยืนยันกับ PM/BA เพราะ FRD ระบุ endpoint แต่ไม่ล็อก state contract ชัดเจน

### 5.7 PDF / Print / Snapshot

- [ ] ตรวจ draft, in_review, pending, returned/rejected draft, approved, cancelled, long text และ DOA 6 ขั้น
- [ ] เทียบ 87 ช่องกับข้อมูลจริงอย่างน้อยหนึ่งใบเต็ม ไม่ใช่ดูเพียง layout
- [ ] A4 ตามข้อยุติ OQ-05, ไม่มี `{{...}}`, ข้อความหาย/ซ้อน, แถวขาดกลางหน้า หรือข้อมูลคนละใบ
- [ ] draft มีเครื่องหมายร่างและเลขหน้า; label `7.:` และ 6.1 ซ้ำตรงข้อกำหนด
- [ ] ตารางทุกกลุ่มไม่จำกัดแถวและเติม blank rows ถึงขั้นต่ำเฉพาะตอนพิมพ์
- [ ] จุดลงนาม review 7 จุดแสดง actor/เวลา/สถานะตรง audit
- [ ] ช่องข้อ 12 ต้องตรง baseline ที่ปิด BC-02 และจำนวนต้อง dynamic ตาม approval chain
- [ ] final PDF ถูกเก็บตอน approved และไม่เปลี่ยนเมื่อ master/template/config เปลี่ยนภายหลัง
- [ ] company/department/approval chain ใช้ snapshot ที่ถูกเวลา

### 5.8 Notification และ integration

- [ ] submit-review → `car_submitted_for_review` ถึง reviewer ที่ resolve จริงเพียงครั้งเดียว
- [ ] return-review → `car_review_returned` ถึง owner พร้อมเหตุผล/ลิงก์ถูกใบเพียงครั้งเดียว
- [ ] cancel จาก in_review/pending ส่งผู้รับตาม baseline ที่ปิด BC-04
- [ ] DOA pending/result/escalate มาจาก DOA engine ไม่ถูกยิงซ้ำโดย feature
- [ ] notification link เคารพ permission; ผู้รับที่หมดสิทธิ์แล้วเปิดไม่ได้
- [ ] approved แล้วไม่เปลี่ยนค่าระบบอื่นและไม่ยิง downstream event ตาม DEC-01/02
- [ ] PDF final ถูกเก็บผ่าน Document Center และสิทธิ์ดาวน์โหลดตรงกับใบ

### 5.9 Audit, history และ state consistency

- [ ] create/update/submit/review/sign/return/send/approve/reject/resubmit/cancel มี audit ครบ
- [ ] audit append-only; reject/return ห้ามลบประวัติ signer/chain เดิม
- [ ] refresh หลังทุก transition ต้องได้ค่าเดียวกับก่อน refresh ไม่ใช่เปลี่ยนแค่ UI
- [ ] status, current step, signature count, approval count, returned fields และ cancelled fields ต้องไม่ขัดกัน
- [ ] เวลาในหน้า, PDF, notification และ audit ใช้ timezone เดียวกันหรือแปลงอย่างถูกต้อง
- [ ] สลับเปิดหลายใบเร็ว ๆ แล้วข้อมูล/attachment/PDF ต้องไม่ค้างข้ามใบ
- [ ] approved/cancelled ต้อง immutable ตาม action ที่ FRD อนุญาต

## 6. Business probes นอก acceptance เดิม

รายการนี้ควรทดลองหรือถาม เพราะมีผลธุรกิจสูง แต่หาก FRD/sign-off ไม่กำหนด ห้ามเปิดเป็น defect โดยอัตโนมัติ

- ถ้า reviewer/signer/approver ลาออก ปิดบัญชี หรือย้ายหน่วยงานระหว่างงาน จะ reassign อย่างไร
- ถ้าคนเดียวถือ HOD, MD, IC Mgr หรือหลาย DOA steps ระบบยอมให้ทำหลายหน้าที่หรือควร block ตาม SoD
- ถ้า owner ไม่มี line manager หรือ organization data ขาด ระบบเลือกใครและใครแก้ได้
- ค่า 6.3 ถูกกรอกโดย owner หรือ reviewer และแก้ได้หลังผ่านการอนุมัติบางขั้นหรือไม่
- owner แก้ field ใดได้บ้างหลัง return/reject; attachment เก่าควรถูกเก็บหรือแทนที่
- cancelled document ควรพิมพ์/ดาวน์โหลดได้หรือไม่ และต้องมี watermark หรือไม่
- retention ของ CAR/PDF/attachment/audit และสิทธิ์หลังพนักงานพ้นสภาพ
- CSV ควรรวมเหตุผล return/reject/cancel และข้อมูล PII ใดบ้าง
- เมื่อ template revision เปลี่ยน เอกสารเก่าใช้ template snapshot เดิมหรือ render ใหม่
- การแก้ไขและป้องกันใน CAR ต้องมี workflow ติดตามผล/ปิด action ต่อหรือไม่; FRD รอบนี้ระบุว่าอนุมัติแล้วไม่เปลี่ยนระบบอื่น จึงอาจเป็น scope gap ไม่ใช่ bug

## 7. ช่องว่างของ Test Pack เดิมที่รอบนี้ต้องอุด

Coverage ledger ของ `TC_...md` ระบุเองว่ายังไม่มีเคสตรงสำหรับ BR-04, BR-12, BR-13, BR-14, VR-02, VR-04, VR-06, EC-01 และ EC-06 ขณะที่ QA-friendly UAT ตัดเคสหลังบ้านอีก 6 เคส จึงต้องเพิ่มอย่างน้อย:

- ค่า analysis_start_minutes ก่อน/เท่ากับ/เกิน threshold
- เลขเดิมหลัง return/reject และเลข unique ภายใต้ concurrency
- กลุ่มแถวทุกชนิดมากกว่าขั้นต่ำและข้อความยาวเกิน 2 หน้า
- form/PDF 87 ช่องและจุดลงนามทั้งหมด ไม่ใช่ดูแค่ภาพรวม
- วันที่ว่าง, หัวข้อว่าง/space-only, แถวอาการว่าง
- total_qty ว่าง/0 และ server-side recalculation
- 409 STALE, 500 partial failure, direct URL deny และ self-sign ผ่าน API
- dynamic DOA, Document Config inactive, snapshot และ final PDF storage

## 8. เกณฑ์จัดระดับสิ่งที่พบ

| ระดับ | ตัวอย่างในฟีเจอร์นี้ |
|---|---|
| Critical | ข้ามลำดับอนุมัติ, self-approve/self-sign ที่ผิด SoD, ข้าม tenant, คนไม่มีสิทธิ์เห็น/ดาวน์โหลด PII, audit สูญหาย, state corruption |
| High | เลขซ้ำ, approved/rejected/cancelled ผิดสถานะ, reject แล้วเลขเปลี่ยน, ลายเซ็นไม่ครบแต่ส่งได้, final PDF ผิดข้อมูล, notification ไปผิดคน, double action |
| Medium | validation/calculation ไม่ตรง FRD แต่มีทางเลี่ยง, warning กลายเป็น block, filter/count/CSV ผิดบางกรณี, audit ขาดรายการที่ไม่กระทบ decision |
| Low | ข้อความ, label, format หรือรายละเอียดแสดงผลที่ไม่กระทบ logic (และไม่ใช่เป้าหมายหลักรอบนี้) |
| Spec/OQ | เอกสารขัดกัน, AI-DEFAULT ไม่ยืนยัน, behavior ที่ FRD ไม่กำหนด |

Bug ทุกใบต้องมี: role/บัญชี, เลข CAR, environment/build, precondition/config, steps ทำซ้ำ, expected พร้อม FRD section/BR/VR/EC, actual, เวลา และหลักฐาน ห้ามเขียนเพียงว่า “ทำงานผิด”

## 9. ชุดขั้นต่ำเมื่อมีเวลาจำกัด

ถ้ามีเวลาเพียงครึ่งวัน ให้ทำตามลำดับนี้:

1. Flow B happy path ครบ review signs 7 จุดและ DOA จน approved
2. Reject ขั้นกลาง → draft เลขเดิม → เปลี่ยน DOA → ส่งใหม่
3. Return จาก review → ล้าง signer/chain → ส่งใหม่
4. Permission deny: direct route/PDF/attachment/CSV + self-sign + approve ก่อนคิว
5. เปิดสองแท็บ + double submit/sign/approve
6. เลขพร้อมกัน 2 ผู้ใช้ + doc_type inactive
7. Calculation: 0, ทศนิยม, sum เกิน total, 6.3, root cause warning/block
8. PDF approved + long text + DOA 6 ขั้น + snapshot
9. Notification ของ submit/return/cancel และตรวจไม่ซ้ำ
10. Tenant isolation ถ้ามีบัญชีทดสอบ

## 10. แบบบันทึกผล

| ID | FRD ref | Scenario | Role/Test data | Expected | Actual | Result | Evidence/Bug |
|---|---|---|---|---|---|---|---|
| LR-001 | 03 FN-02 / 05 BR-12 | บันทึกครั้งแรกและ retry | U1 / CAR-... | ได้เลขเดียวและ record เดียว |  | ☐ Pass ☐ Fail ☐ Blocked ☐ Not Run |  |
| LR-002 | 03 FN-04 / BR-DOA-02 | Submit และ freeze DOA | U1 / CAR-... | chain ตรง config และไม่เปลี่ยนระหว่าง pending |  | ☐ Pass ☐ Fail ☐ Blocked ☐ Not Run |  |
| LR-003 | 03 FN-06 / BR-08/10 | ลงนาม 7 จุดและ SoD | U3/U4/U5 | ลงได้เฉพาะจุดตน; owner ลงไม่ได้ |  | ☐ Pass ☐ Fail ☐ Blocked ☐ Not Run |  |
| LR-004 | 03 FN-09/10 | Approve/Reject ตามลำดับ | Approvers | ไม่ข้ามขั้น; reject กลับ draft เลขเดิม |  | ☐ Pass ☐ Fail ☐ Blocked ☐ Not Run |  |
| LR-005 | 03 FN-14 / DEC-26 | Permission/direct URL | U6/U8 | ไม่เห็น list/detail/PDF/file/CSV |  | ☐ Pass ☐ Fail ☐ Blocked ☐ Not Run |  |

ใช้ `Pass` ได้เมื่อรันจริงและมีหลักฐานเท่านั้น เอกสาร/prototype/test case เดิมไม่ใช่หลักฐานว่าระบบ Production ผ่าน

