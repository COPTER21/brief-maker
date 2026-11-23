# Full Review Plan — แบบฟอร์มประเมินความเสี่ยง (F-TMP-002)

> เอกสารนี้เป็นแผนตรวจ production logic รอบเก็บตก ไม่ใช่ผลรับรองผ่าน/ไม่ผ่าน
> เกณฑ์ตัดสิน defect ใช้ FRD v1.0 เป็นหลัก ส่วน business sense ใช้เลือกข้อมูลและลำดับความเสี่ยงเท่านั้น

## 1. ข้อสรุปจากการอ่าน context

- Test case เดิม 30 เคสออกแบบให้รันบน prototype `feature.html` ไม่ใช่หลักฐานว่า backend/integration บน production ผ่านแล้ว
- QA Audit เดิมตัดเคสหลังบ้านบางส่วนออก เช่น การชนกันของข้อมูล และการไม่ส่งต่อระบบอื่น
- จุดที่ต้องเจาะเพิ่มจึงเป็น permission/RLS, server-side validation, optimistic lock, idempotency, audit, DOA snapshot, notification, Document Store, PDF จริง และ config จริง
- UI/layout ถือว่าตรวจแบบ exception-based: ไม่ต้องไล่ pixel ใหม่ แต่ถ้า UI ทำให้ logic ใช้ผิดหรือเห็นข้อมูลผิดสิทธิ์ ต้องเปิด defect

## 2. Source of truth และวิธีตัดสิน

1. **FRD เป็นเกณฑ์ Pass/Fail**: 00 Overview → 07 Locked Decisions
2. **Locked Decision มาก่อนความคาดเดา** แต่ถ้าเอกสารขัดกันให้พักผลและถาม BA/PM ห้ามเดา
3. **Business sense ไม่ใช้สร้าง requirement ใหม่**: สิ่งที่ควรมีแต่ FRD ไม่ได้กำหนด ให้ลงเป็น OQ/ข้อเสนอแนะ ไม่ใช่ bug
4. ทุกผลต้องมีหลักฐาน: ผู้ใช้/role, เลขเอกสาร, เวลา, input, expected, actual, screenshot และ response/error code ถ้ามี
5. เคสที่ไม่ได้รันให้ระบุ `ไม่ได้ตรวจ` ห้ามเหมารวมว่าผ่านจาก tester รอบก่อน

## 3. ประเด็นที่ต้องให้ BA/PM ยืนยันก่อนปิดผล

| ID | ประเด็น | หลักฐานที่ขัดกัน | ผลกระทบ |
|---|---|---|---|
| OQ-R01 | Production ต้องยิง `rsk_cancelled` และ `rsk_very_high_approved` หรือไม่ | FN-09, API §2.X, AC-08 ระบุให้ยิง แต่ DEC-02 ระบุ “ประกาศ event ไว้ใน FRD แต่ไม่ยิง” | ตัดสิน notification เป็น pass/fail ไม่ได้จนกว่าจะยืนยัน |
| OQ-R02 | AI-DEFAULT 11 ข้อได้รับการเซ็นยืนยันแล้วหรือยัง | Overview OQ-02 ระบุว่าต้องยืนยันก่อน UAT แต่ pack ยังแสดงเป็น OQ | ถ้ายังไม่ยืนยัน พฤติกรรม production อาจตรง FRD แต่ไม่ตรงมติธุรกิจจริง |
| OQ-R03 | role-gm ชั่วคราวถูกแทนด้วย role จริงแล้วหรือยัง | OQ-03 และ LD-05 | เสี่ยงส่งผิดคน/ผิดสายอนุมัติ |
| OQ-R04 | RiskMatrix และ doc type `RSK` ใน production ใครเป็น owner และค่าปัจจุบันคืออะไร | OQ-04/OQ-06 | คะแนน ระดับ ประเภท และเลขเอกสารอาจผิด config |

## 4. Test data ที่ต้องเตรียม

บัญชีอย่างน้อย 6 แบบ: owner, owner คนที่สอง, checker ขั้น 1, approver ขั้น 2, ผู้ที่อยู่ในสายแต่ไม่ใช่ขั้นปัจจุบัน, admin ฝ่ายพัฒนาธุรกิจ และถ้าทำได้เพิ่มผู้ใช้คนละ tenant หนึ่งบัญชี

ข้อมูลทดสอบหลัก:

- ชุดคะแนนขอบเขตระดับ: 4, 5, 9, 10, 16, 17, 25
- residual ที่ถูกต้อง: 1,2,3,4,5,6,8,9,10,12,15,16,20,25 และค่าผิด 7
- ใบ 1 แถว, 2 แถว, 18 แถว และ 24 แถว
- DOA 1, 2 และ 6 ขั้น (อย่างน้อย 2 ขั้นต้องรัน end-to-end; 1/6 ขั้นใช้ตรวจ dynamic/PDF)
- ไฟล์แนบชนิดที่อนุญาต, ชนิดผิด, ไฟล์ใหญ่เกินกำหนด และชื่อไฟล์ภาษาไทย/อักขระพิเศษ

## 5. ชุดทดสอบหลัก — ต้องรันก่อน

### A. คะแนนและ validation

| ID | Pri | วิธีทดสอบย่อ | Expected ตาม FRD |
|---|---:|---|---|
| RV-A01 | P0 | สร้างใบ 2 แถว กรอก likelihood/impact เป็น 4×4 และ 5×5 | server คำนวณ 16/25 เอง ระดับตรง RiskMatrix; FE ส่งค่าคะแนนปลอมแล้ว server ต้องไม่เชื่อ |
| RV-A02 | P0 | ทดสอบคะแนนขอบเขต 4/5/9/10/16/17/25 | เปลี่ยนระดับตรง `RiskMatrix.level_bands` ทุก boundary |
| RV-A03 | P0 | เว้น likelihood หรือ impact ทีละช่องแล้วบันทึก/ถัดไป | คะแนนว่าง ไม่เป็น 0 และ required ถูกบังคับตอนทำรายการให้ครบ |
| RV-A04 | P0 | ส่ง residual=7 ผ่าน UI และยิง request โดยตรง | UI ไม่มีค่า 7; API ตอบ 422 และไม่บันทึก |
| RV-A05 | P0 | ตั้งสถานะรายการ “ปิดแล้ว” โดยไม่มี residual | บล็อกทั้ง UI และ server พร้อมข้อความตาม VR-02 |
| RV-A06 | P1 | residual มากกว่า inherent | เตือนระดับแถวและสรุป แต่ยังบันทึกได้ |
| RV-A07 | P1 | ใส่ 0, 6, ค่าติดลบ, decimal, null และ category ที่ไม่อยู่ใน config ผ่าน request | server ปฏิเสธค่าที่ผิด contract; ไม่มีข้อมูลเสียเข้าฐาน |
| RV-A08 | P1 | เปลี่ยน RiskMatrix config ในสภาพแวดล้อมทดสอบแล้วอ่าน/สร้างใหม่ | ตัวเลือก คะแนน และระดับอ่านจาก config ไม่มีค่าฝังในโค้ด |

### B. State, เลขเอกสาร และ lifecycle

| ID | Pri | วิธีทดสอบย่อ | Expected ตาม FRD |
|---|---:|---|---|
| RV-B01 | P0 | บันทึกครั้งแรก กดซ้ำ/refresh แล้วแก้ร่างหลายครั้ง | ออกเลข RSK ครั้งเดียว เลขไม่เปลี่ยน ไม่สร้างใบซ้ำ |
| RV-B02 | P0 | ไล่ draft → pending ขั้น 1 → pending ขั้น 2 → approved | สถานะและผู้มี action ถูกต้องทีละขั้น; approved ล็อกแก้/ยกเลิก |
| RV-B03 | P0 | reject จากขั้น 1 และอีกใบ reject จากขั้น 2 พร้อมเหตุผล | กลับ draft, ใช้เลขเดิม, เก็บผู้/เวลา/เหตุผล, chain เดิมลง audit แล้วล้าง |
| RV-B04 | P0 | แก้ใบที่ถูกส่งกลับแล้ว submit ใหม่ | resolve chain ใหม่, ล้าง `returned_*`, ประวัติเก่ายังอยู่ |
| RV-B05 | P0 | cancel draft และ pending โดย owner/admin; ลองกับ approved/cancelled | draft/pending สำเร็จเมื่อมีเหตุผล; approved/cancelled ตอบ NOT_CANCELLABLE |
| RV-B06 | P1 | ปิด doc type RSK แล้วสร้างใบใหม่ | 409 DOC_TYPE_INACTIVE และไม่มีเลข/ใบค้างครึ่งทาง |
| RV-B07 | P1 | จำลอง engine ออกเลขหรือ save ล้มเหลวกลาง transaction | ไม่เกิดเลขซ้ำ ใบ orphan หรือข้อมูลบันทึกครึ่งเดียว |

### C. DOA และ segregation of duties

| ID | Pri | วิธีทดสอบย่อ | Expected ตาม FRD |
|---|---:|---|---|
| RV-C01 | P0 | submit โดยไม่เลือก assignee ครบ และลองเลือก owner เอง | 422 ASSIGNEE_REQUIRED/SELF_APPROVAL; owner ไม่อยู่ในตัวเลือก |
| RV-C02 | P0 | ผู้ไม่ใช่ current approver ยิง approve/reject โดยตรง | 403 NOT_CURRENT_APPROVER และ state/audit ไม่เปลี่ยน |
| RV-C03 | P0 | submit แล้วแก้ DOA master ระหว่าง pending | ใบเดิมใช้ chain snapshot; ใบใหม่ใช้ chain ใหม่ |
| RV-C04 | P0 | current approver เปิดสองหน้าต่าง กดตัดสินชนกัน | หนึ่งครั้งสำเร็จ อีกครั้ง 409 STALE; ไม่ข้ามขั้น/ไม่อนุมัติซ้ำ |
| RV-C05 | P1 | ตั้ง DOA 1/2/6 ขั้นและ submit | จำนวน slot/ลำดับ/role/คำตัดสิน dynamic ตรง config ไม่มีการ fix 2 ขั้น |
| RV-C06 | P1 | owner เป็น line manager ของตนเอง | slot ขั้นแรกว่างและบังคับเลือกคนอื่น ไม่ self-approve |

### D. Permission, data privacy และ tenant isolation

| ID | Pri | วิธีทดสอบย่อ | Expected ตาม FRD |
|---|---:|---|---|
| RV-D01 | P0 | owner คนที่สองค้นหาและเปิด direct URL ของ draft คนอื่น | ไม่พบใน list และ GET detail เป็น 404 NOT_FOUND |
| RV-D02 | P0 | คนนอก chain เปิด pending/approved/cancelled ด้วย direct URL/API | 404 NOT_FOUND ไม่เปิดเผยว่ามีเอกสาร |
| RV-D03 | P0 | ผู้ใน chain ที่ไม่ใช่ขั้นปัจจุบันดูและลองตัดสิน | ดูได้หลังส่ง แต่ไม่มีปุ่มและ API ตอบ 403 เมื่อตัดสิน |
| RV-D04 | P0 | admin ดูทุกสถานะและลองแก้/ตัดสิน | ดู/ยกเลิกตามสิทธิ์ แต่ห้ามแก้ draft ของคนอื่นและห้ามตัดสินแทน |
| RV-D05 | P0 | ใช้ token คนละ tenant กับ id/doc_no ของ tenant เป้าหมาย | list/detail/PDF/attachment/CSV ไม่รั่วข้าม tenant |
| RV-D06 | P1 | ตรวจชื่อผู้จัดทำ/ผู้พิจารณาใน API, export, PDF และ log | PII แสดงเฉพาะผู้มีสิทธิ์และไม่หลุดใน error/log ที่ผู้ใช้เห็น |

### E. Concurrency และ duplicate protection

| ID | Pri | วิธีทดสอบย่อ | Expected ตาม FRD |
|---|---:|---|---|
| RV-E01 | P0 | เปิด draft เดียวกันสองแท็บ แก้แท็บ A แล้ว save แท็บ B ด้วย version เก่า | 409 STALE; ไม่ overwrite ข้อมูลใหม่เงียบ ๆ |
| RV-E02 | P0 | ส่ง POST submit/decide/cancel ซ้ำด้วย Idempotency-Key เดิม | ผลทางธุรกิจเกิดครั้งเดียว audit/event ไม่ซ้ำ |
| RV-E03 | P0 | ส่ง payload เดิมด้วย Idempotency-Key ต่างกันหลัง action สำเร็จ | state guard ปฏิเสธ action ซ้ำ ไม่สร้าง side effect ซ้ำ |
| RV-E04 | P1 | network timeout หลังคลิกบันทึกแล้วผู้ใช้ retry | กลับมาเห็นผลเดิม ไม่สร้างเลข/ใบ/ไฟล์ซ้ำ |

### F. PDF, attachment, CSV และ integration

| ID | Pri | วิธีทดสอบย่อ | Expected ตาม FRD |
|---|---:|---|---|
| RV-F01 | P0 | เปิด PDF ใน draft/pending/approved/cancelled | ทุกสถานะ 2 หน้า, หน้า N/2, header ซ้ำ, ข้อมูลตรงหน้าจอและ snapshot |
| RV-F02 | P0 | PDF 1, 18 และ 24 แถว | อย่างน้อย min_rows; รายการไม่หาย/ซ้ำ; 24 แถวยังจัด 2 หน้าและอ่านได้ |
| RV-F03 | P0 | PDF ของ DOA 1/2/6 ขั้น | แถวลงชื่อ = ผู้จัดทำ + 1 ต่อขั้น, role/ชื่อ/คำตัดสินถูก, block ไม่ถูกตัดข้ามหน้า |
| RV-F04 | P0 | อนุมัติสุดท้ายแล้วดาวน์โหลดใหม่หลายครั้ง | approved_final ถูกเก็บครั้งเดียวใน Document Store และเนื้อหาคงเดิม |
| RV-F05 | P1 | แนบ/ลบไฟล์ก่อนและหลังเปลี่ยนสถานะ รวมไฟล์ผิดชนิด/ใหญ่/ชื่อพิเศษ | อนุญาตตาม policy, ref_type=RSK, ไม่มีไฟล์ orphan หรือเข้าถึงข้ามสิทธิ์ |
| RV-F06 | P1 | filter หลายเงื่อนไขแล้ว export CSV | แถวใน CSV ตรงผลกรองและสิทธิ์, encoding ไทยถูก, ไม่มีข้อมูลคนนอก scope |
| RV-F07 | P1 | approved ที่มีคะแนนระดับสูงสุด และ cancel ใบ pending | ทำตามมติ OQ-R01; ถ้าต้องยิง ผู้รับ/channel/payload ถูกและไม่ซ้ำกับ DOA engine |

### G. Audit และความถูกต้องของข้อมูล

| ID | Pri | วิธีทดสอบย่อ | Expected ตาม FRD |
|---|---:|---|---|
| RV-G01 | P0 | ไล่ create/edit/submit/approve/reject/resubmit/cancel | ทุก write มี actor/time/action/note ที่ถูกต้อง เรียงเวลาและไม่มีช่วงหาย |
| RV-G02 | P0 | พยายามแก้/ลบ audit ผ่านช่องทางที่มี | audit append-only ไม่มี update/delete |
| RV-G03 | P1 | เปลี่ยนชื่อ/ตำแหน่ง/ฝ่าย/โลโก้องค์กรหลังออกเลข | เอกสารเดิมใช้ snapshot ตาม FRD; เอกสารใหม่ใช้ค่าปัจจุบัน |
| RV-G04 | P1 | ลบ/แก้รายการหลายแถวใน draft แล้วบันทึก | seq ต่อเนื่อง ข้อมูลไม่สลับแถว ไม่มี item orphan |

## 6. Exploratory business flows

หลังชุดหลัก ให้เล่นอย่างน้อย 45–60 นาทีโดยไม่เดินตาม test case ตรง ๆ:

1. **งานเร่ง**: สร้างหลายรายการ, save กลางทาง, refresh, กลับมาแก้, submit, approver เปิดจาก notification แล้วตัดสิน
2. **งานถูกตีกลับ**: checker reject, owner แก้เฉพาะหนึ่งแถว, resubmit หลัง DOA เปลี่ยน, ตรวจเลขเดิมและประวัติครบ
3. **งานยกเลิกระหว่างรอ**: owner กับ admin เปิดใบเดียวกันพร้อมกัน, คนหนึ่ง cancel ขณะอีกคน approve
4. **ข้อมูลสุดขอบ**: 24 แถว, ข้อความยาว/ภาษาไทย/อักขระพิเศษ, ไฟล์หลายชนิด, คะแนนทุก boundary, PDF และ CSV
5. **เจาะสิทธิ์**: สลับ persona แล้วใช้ URL เดิม, browser back, cached tab และ request เดิมหลัง logout/login เป็นคนอื่น

## 7. หลักฐานและรูปแบบบันทึกผล

ต่อหนึ่งเคสเก็บ: `Case ID | เวลา | env/build | user/role | doc_no | input | expected | actual | PASS/FAIL/NA | evidence`

เมื่อพบ defect ให้บันทึก:

- Steps สั้นและทำซ้ำได้
- Expected อ้าง FRD section/BR/FN/AC
- Actual เป็นข้อความ/สถานะ/error code ที่เห็นจริง
- Severity: Critical = ข้ามสิทธิ์/ข้าม DOA/ข้อมูลหาย; High = คะแนน/สถานะ/เอกสารซ้ำผิด; Medium = ผิด spec แต่มีทางเลี่ยงหรือ audit ขาด; Low = หน้าตา/ข้อความ
- แยก “ข้อเสนอแนะ” ออกจาก “bug” ถ้าระบบทำตรง FRD

## 8. Exit criteria สำหรับการ review รอบนี้

- P0 ทุกเคสมีผลจริงและหลักฐาน ไม่มี Critical/High ค้าง
- Business Rules BR-01..14, DOA-01..04, FN-01..10, AC-01..13 และ deny D01..D06 ถูก trace ไปยังผลทดสอบอย่างน้อยหนึ่งรายการ
- ทดสอบอย่างน้อยหนึ่งครั้งผ่าน API/Network evidence สำหรับ server-side validation และ permission; ห้ามรับรองจาก UI อย่างเดียว
- notification conflict และ AI-DEFAULT/OQ สำคัญได้รับคำตอบเป็นลายลักษณ์อักษร
- สิ่งที่ไม่ได้ตรวจถูกระบุชัด ไม่ใช้ผล prototype หรือคำว่า “tester ผ่านแล้ว” มาทดแทนหลักฐาน production
- เมื่อรันเสร็จ ค่อยสร้าง Feature Check Report รอบ 1 จากผลจริง; ห้ามเติม pass ให้เคสที่ไม่ได้รัน
