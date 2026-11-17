# Full Review Plan — ใบตรวจเช็คถังดับเพลิง (F-TMP-001)

> เอกสารนี้เป็น **แผนตรวจ** ไม่ใช่ผลตรวจ และยังไม่มีข้อใดเป็น Pass/Fail จนกว่าจะรันบนระบบจริงพร้อมหลักฐาน
>
> Baseline หลัก: FRD v1.0 ใน `context/ใบตรวจเช็คถังดับเพลิง/_frd/FRD_ใบตรวจเช็คถังดับเพลิง/`
>
> วันที่จัดทำแผน: 17 พฤศจิกายน 2569

## 1. เป้าหมายของรอบ review

รอบนี้ไม่ใช่การตรวจ layout ซ้ำ แต่เป็นการพิสูจน์ว่า feature ทำงานถูกต้องตาม FRD ใน 7 มิติ:

1. กฎธุรกิจและ validation
2. สถานะเอกสารและผลล่าสุด
3. สิทธิ์ทั้งบนจอและฝั่ง server
4. ความครบถ้วน/ความคงสภาพของข้อมูลและ audit
5. การแจ้งเตือนและการเชื่อมระบบกลาง
6. ความทนต่อการกดซ้ำ งานชนกัน และ API ล้ม
7. PDF, CSV และไฟล์แนบในฐานะผลลัพธ์ทางธุรกิจ

UI ให้ตรวจเฉพาะจุดที่ทำให้ logic ใช้ไม่ได้ หรือแสดงค่าธุรกิจผิด เช่น ปุ่มที่คนไม่มีสิทธิ์เห็น, ผลล่าสุดผิด, หรือข้อความ error ไม่ตรง FRD

## 2. หลักตัดสิน

| สิ่งที่พบ | จัดเป็น | วิธีรายงาน |
|---|---|---|
| พฤติกรรมขัด FRD/BR/VR/AC ชัดเจน | Bug | มีขั้นตอนทำซ้ำ Expected ตาม FRD Actual และหลักฐาน |
| FRD เขียนไม่ชัดหรือเอกสารต้นทางขัดกัน | Open Question | ห้ามเดาคำตอบแทน BA |
| ระบบทำตรง FRD แต่มีความเสี่ยงต่อธุรกิจ/ความปลอดภัย | Suggestion / Business risk | ไม่ปนกับ Bug |
| ยังเตรียม role/config/fault injection ไม่ได้ | Blocked / Not tested | ห้ามให้ Pass |

## 3. สิ่งที่ชุดทดสอบเดิมยังไม่พิสูจน์

ชุดเดิมมี 22 เคสและประกาศ coverage AC 10/12 แต่ยังไม่พิสูจน์ครบเรื่องต่อไปนี้:

- AC-11: ปิด doc type FEC แล้วสร้างไม่ได้
- AC-12/EC-06: API error และ optimistic-lock stale แล้วข้อมูลต้องไม่เปลี่ยน
- EC-02: PDF 24 แถวแบบ dense 1 หน้า
- การกดซ้ำ/retry ต้องไม่สร้างใบ แถว เลขที่ หรือ notification ซ้ำ
- การสร้างใบของสถานที่เดียวกันพร้อมกันสองคน
- สิทธิ์ฝั่ง API, tenant isolation และ IDOR ของ PDF/CSV/attachment
- audit before/after และความเป็น append-only
- snapshot ชื่อสถานที่ องค์กร และผู้ตรวจหลัง master ถูกแก้
- notification จริงทั้งผู้รับ payload ช่องทาง และกรณีแก้ไขแถว
- CSV ตาม filter/permission และการ mask PII
- lifecycle ของ attachment โดยเฉพาะหลังยกเลิก
- ผลล่าสุดเมื่อเพิ่มผลตรวจย้อนหลังหรือแก้วันที่
- boundary ของคำว่า “วันนี้” ตาม tenant timezone

## 4. Test setup ที่ต้องขอก่อนเริ่ม

### 4.1 บัญชีทดสอบ

| Persona | ต้องใช้ทำอะไร |
|---|---|
| A — warehouse_staff ผู้สร้างใบ | สร้าง ดูทุกใบ บันทึกผล แก้แถวตนเอง ยกเลิกใบตนเอง |
| B — warehouse_staff คนที่สอง | ทดสอบบันทึกในใบเดียวกัน แก้แถวคนอื่น และงานชนกัน |
| C — role-mgr-wh | ดูทุกใบ ยกเลิกใบคนอื่น รับ notification |
| D — พนักงานนอกแผนก | เห็นเฉพาะใบตน สร้างใบ และถูกปฏิเสธใบคนอื่น |
| E — พนักงานนอกแผนกคนที่สอง | ทดสอบ owner isolation |
| F — tenant อื่น (ถ้ามี UAT multi-tenant) | ทดสอบ RLS/tenant isolation |

### 4.2 ข้อมูลและสิทธิ์ช่วยทดสอบ

- สถานที่ว่างอย่างน้อย 6 จุด และสถานที่ที่มี active card แล้ว 1 จุด
- สิทธิ์อ่าน log/audit, notification center และ email sandbox
- วิธีเปิด/ปิด doc type `FEC` ใน F-DOCCFG
- วิธีจำลอง 409 STALE, 500 และ network retry หรือให้ dev ช่วย fault-inject
- ไฟล์แนบทดสอบ: PDF เล็ก, รูปภาพ, ไฟล์ชื่อภาษาไทย, ไฟล์ชนิด/ขนาดที่ระบบไม่อนุญาต
- ใบที่มี 0, 1, 12, 13 และ 24 checks
- ถ้า production ห้ามสร้างข้อมูลทดสอบ ให้ใช้ UAT ที่ config เหมือน production; ห้ามทำ destructive test บนข้อมูลจริง

### 4.3 หลักฐานขั้นต่ำต่อเคส

- screenshot ก่อน/หลังที่เห็นเลขที่ สถานที่ ผลล่าสุด สถานะ และข้อความ error
- เวลาและผู้ใช้ที่รัน
- request/response หรือ correlation ID สำหรับ permission, 409, 422, 500 และ notification
- ไฟล์ PDF/CSV ที่ดาวน์โหลดจริง
- audit/notification evidence เมื่อเคสเกี่ยวข้อง

## 5. ลำดับรันที่แนะนำ

1. รัน P0 ก่อน ถ้า fail ให้หยุดเฉพาะ flow ที่ข้อมูลอาจเสียหรือข้ามสิทธิ์
2. รัน P1 ครบทุกข้อ
3. รัน P2 เมื่อมีเวลาและ environment รองรับ
4. Retest bug ด้วยข้อมูลชุดใหม่ ไม่ใช้แถวเดิมที่อาจมี state ค้าง

## 6. Test scenarios — ต้องรัน

### A. สร้างใบ เลขที่ และข้อบังคับพื้นฐาน

| ID | Pri | วิธีทดสอบย่อ | Expected ตาม FRD | Trace |
|---|---:|---|---|---|
| R-A01 | P0 | A สร้างใบพร้อมผลปกติครบ 4 หัวข้อ | ได้ active card 1 ใบ เลข FEC 1 เลข ผู้ตรวจ=A ผลล่าสุด=ปกติ จำนวนครั้ง=1 | AC-01, BR-01, BR-06, FN-03/04 |
| R-A02 | P0 | สร้างโดยไม่เลือกสถานที่ | บันทึกไม่ได้; `กรุณาเลือกสถานที่`; ไม่มีใบ/เลขถูกสร้าง | VR-01 |
| R-A03 | P0 | เลือกผลเพียง 1–3 หัวข้อ | บันทึกไม่ได้; `เลือกผลให้ครบทั้ง 4 หัวข้อ`; ไม่มีข้อมูลบางส่วนค้าง | VR-05, BR-01 |
| R-A04 | P0 | สร้างใบซ้ำในสถานที่ที่มี active card | 409/ข้อความ `สถานที่นี้มีใบตรวจที่ใช้งานอยู่แล้ว`; เปิดใบเดิมได้; ไม่มีเลขใหม่ | VR-02, BR-04 |
| R-A05 | P1 | สร้างใบเปล่า | active, last_result=ยังไม่ตรวจ/none, last_check_date ว่าง, จำนวนครั้ง=0, PDF มีแถวว่างอย่างน้อย 12 | AC-04, EC-01 |
| R-A06 | P1 | ปิด doc type FEC แล้วเข้า list/create | ปุ่มสร้าง disabled + ข้อความตาม FRD; เรียก create ตรงถูก 409 `DOC_TYPE_INACTIVE` | AC-11, EC-07, FN-03 |
| R-A07 | P1 | ขณะ FEC ปิด เปิดใบเดิมและลองดู/พิมพ์/เพิ่มผล | บันทึกผลเดิมต้องตัดสินตาม FRD ที่ scope การปิดระบุเฉพาะ “สร้าง”; ถ้าระบบบล็อกส่วนอื่นให้เปิด OQ ไม่เดา | FN-03, AC-11 |
| R-A08 | P1 | เปิด FEC กลับแล้วสร้างใบ | สร้างได้ตามปกติ; เลขมาจาก engine ไม่ใช่เลขที่หน้าเว็บคำนวณเอง | BR-08, FN-03 |
| R-A09 | P1 | ตรวจเลขสองใบเรียงกันและข้ามปี/config ตามที่ environment ทำได้ | เลข unique ใน tenant และ reset ตาม config รายปี; ช่องว่างเลขยอมรับได้เพราะ no-gap=false | BR-08, DOCCFG |
| R-A10 | P1 | ตรวจเลขปีที่แสดงว่าเป็น ค.ศ. หรือ พ.ศ. | บันทึกค่าจริงเป็นหลักฐาน; FRD/ตัวอย่างยังต้องให้ BA ยืนยันถ้าความหมาย `YYYY` ไม่ชัด | FN-03, AC-01 |

### B. บันทึกผล ตรวจย้อนหลัง และคำนวณผลล่าสุด

| ID | Pri | วิธีทดสอบย่อ | Expected ตาม FRD | Trace |
|---|---:|---|---|---|
| R-B01 | P0 | เพิ่ม check ปกติใน active card | เพิ่ม 1 แถว; inspector เป็นผู้ login จริงและ client เปลี่ยนค่าไม่ได้ | BR-06, FN-04 |
| R-B02 | P0 | เพิ่ม check มี x เพียง 1 หัวข้อ | แถวนั้น abnormal; last_result=ผิดปกติ; abnormal_items ระบุหัวข้อถูก | BR-02, FN-04/07 |
| R-B03 | P0 | เพิ่ม check มี x หลายหัวข้อ | abnormal_items ครบทุกหัวข้อ ไม่ซ้ำ/ไม่ตก; PDF/จอทำเครื่องหมายตรง | BR-02, FN-07/09 |
| R-B04 | P0 | บันทึกวันที่ซ้ำในใบเดียวกัน | 409 `DATE_DUPLICATE`; ไม่เพิ่มแถว/notification/audit success ซ้ำ | VR-04 |
| R-B05 | P0 | บันทึกวันอนาคตผ่าน UI และยิง API ตรง | UI กันและ server ตอบ 422 `DATE_IN_FUTURE`; ไม่มีข้อมูลเปลี่ยน | VR-03 |
| R-B06 | P1 | เพิ่ม check ย้อนหลังที่เก่ากว่าแถวล่าสุด | เพิ่มได้ แต่ last_check_date/last_result ยังอิงแถววันที่ล่าสุด ไม่ใช่แถวที่เพิ่งกดบันทึก | EC-04, BR-02 |
| R-B07 | P1 | เพิ่ม check ย้อนหลังที่ใหม่กว่าแถวเดิมแต่ไม่เกินวันนี้ | last_* เปลี่ยนไปอิงวันที่ใหม่ที่สุด | BR-02, FN-04 |
| R-B08 | P1 | ตรวจเที่ยงคืนด้วย timezone tenant | “วันนี้” และ edit window ใช้ tenant timezone สม่ำเสมอทั้ง UI/API | FN-02, BR-07 |
| R-B09 | P1 | ส่ง enum อื่น/ค่าว่าง/null ผ่าน API | server ปฏิเสธ; ไม่มีการแปลงเป็น normal โดยอัตโนมัติ | FN-02, DB enum |
| R-B10 | P1 | เพิ่ม check ใน cancelled card ผ่าน route/API ตรง | ไม่มีปุ่มและ API 409 `CARD_CANCELLED`; ไม่มี audit/notification แบบสำเร็จ | TC-D06, state machine |

### C. การแก้ไข การยกเลิก และ audit

| ID | Pri | วิธีทดสอบย่อ | Expected ตาม FRD | Trace |
|---|---:|---|---|---|
| R-C01 | P0 | A แก้แถวที่ A บันทึกวันนี้ | แก้ได้; audit เก็บ before/after; last_* คำนวณใหม่ | BR-07, FN-05 |
| R-C02 | P0 | B แก้แถวของ A ผ่าน UI และ API | ไม่มีปุ่ม; API 403 `NOT_RECORDER`; ข้อมูลไม่เปลี่ยน | TC-D03 |
| R-C03 | P0 | A แก้แถวของตนหลังพ้นวัน tenant | ไม่มีปุ่ม; API 403 `EDIT_WINDOW_CLOSED` | TC-D04, EC-05 |
| R-C04 | P1 | แก้แถวล่าสุดจากปกติเป็นผิดปกติ | last_result เปลี่ยนผิดปกติ; audit ถูก; notification ผิดปกติถูกยิง | FN-05/07 |
| R-C05 | P1 | แก้แถวล่าสุดจากผิดปกติเป็นปกติ | last_result คำนวณใหม่เป็นปกติ; ไม่มี event “resolved” เพราะ FRD ไม่ประกาศ; บันทึกเป็น business risk | BR-02, FN-05/07 |
| R-C06 | P1 | แก้แถวเก่าที่ไม่ใช่วันที่ล่าสุด | แถวนั้นเปลี่ยน แต่ last_* ยังอิงแถววันที่ล่าสุด | BR-02 |
| R-C07 | P0 | owner ยกเลิกโดยไม่ใส่เหตุผล | 422 `REASON_REQUIRED`; สถานะยัง active | VR-06 |
| R-C08 | P0 | owner ยกเลิกพร้อมเหตุผล | active→cancelled; เก็บเหตุผล/actor/time; ล็อกการบันทึกผล | BR-12, FN-06 |
| R-C09 | P0 | role-mgr-wh ยกเลิกใบคนอื่น | ทำได้และมี audit/notification cancelled ถูกผู้รับ | Permission §5.3, FN-07 |
| R-C10 | P0 | warehouse_staff ที่ไม่ใช่ owner ยกเลิกใบคนอื่น | ไม่มี action; API 403 `NOT_OWNER` | TC-D05 |
| R-C11 | P1 | ยกเลิกแล้วลองยกเลิกซ้ำ | 409 `NOT_CANCELLABLE`; reason เดิมไม่ถูกทับ; ไม่แจ้งซ้ำ | API-06, state machine |
| R-C12 | P1 | ยกเลิกใบ แล้วสร้างใบใหม่สถานที่เดิม | สร้าง active card ใหม่ได้ตาม EC-03; ใบเก่ายังอยู่และประวัติไม่หาย | EC-03, BR-04 |
| R-C13 | P1 | ตรวจ audit ทุก write | create/add/edit/cancel/attachment ที่กำหนดมี actor+เวลา; edit มี before/after; ไม่มีการแก้/ลบ log เดิม | API §2.3, DB audit |

### D. สิทธิ์และการแยกข้อมูล

| ID | Pri | วิธีทดสอบย่อ | Expected ตาม FRD | Trace |
|---|---:|---|---|---|
| R-D01 | P0 | warehouse_staff ดู list | เห็นทุกใบตาม permission matrix ไม่ใช่เฉพาะของตน | BR-09, §5.3 |
| R-D02 | P0 | พนักงานนอกแผนกดู list | เห็นเฉพาะใบที่ตนเป็น owner | BR-09, TC-D02 |
| R-D03 | P0 | พนักงานนอกแผนกเปิด URL/id ใบคนอื่น | 404 `NOT_FOUND` ไม่ใช่ 403 และไม่เผยข้อมูลเอกสาร | TC-D01 |
| R-D04 | P0 | ผู้ไม่มีสิทธิ์เรียก detail/pdf/attachment ด้วย id ใบคนอื่น | ทุกช่องทางปฏิเสธแบบไม่เผยว่ามี id นั้น | BR-09, API-02/07/09 |
| R-D05 | P0 | พนักงานนอกแผนกสร้างใบตนเองแล้วดู/เพิ่ม check/ยกเลิก | ทำได้ตาม matrix; บันทึก owner ถูกคน | §5.3 |
| R-D06 | P0 | role-mgr-wh ดู list/detail ทุก owner | เห็นทั้งหมดและ action ถูกต้อง | §5.3 |
| R-D07 | P0 | สลับ tenant หรือใช้ id จาก tenant อื่น | list/detail/pdf/csv/attachment ไม่รั่วข้าม tenant | API §2.3, DB RLS |
| R-D08 | P1 | เปลี่ยน inspector_id/owner_id ใน request | server ไม่รับค่าปลอม; inspector=current user, owner=creator | FN-04, DB |
| R-D09 | P1 | CSV ด้วย persona ต่างกัน | จำนวน/แถวใน CSV ไม่เกินสิทธิ์ของ persona | FN-08, BR-09 |
| R-D10 | P1 | ตรวจ response 404 | body/log ฝั่ง client ไม่เผยชื่อสถานที่ ผู้ตรวจ หรือข้อมูล tenant อื่น | BR-09, D-CLASS |

### E. งานชนกัน การกดซ้ำ และ failure handling

| ID | Pri | วิธีทดสอบย่อ | Expected ตาม FRD | Trace |
|---|---:|---|---|---|
| R-E01 | P0 | double-click ปุ่มสร้าง/ส่ง request เดิมด้วย Idempotency-Key เดิม | ได้ใบเดียว เลขเดียว แถวแรกเดียว notification เดียว | API §2.3 |
| R-E02 | P0 | A และ B สร้าง active card สถานที่เดียวกันพร้อมกัน | สำเร็จเพียงหนึ่ง; อีกคำขอ 409; ไม่มี active ซ้ำ | BR-04, DB partial unique |
| R-E03 | P0 | A และ B เพิ่ม check วันเดียวกันพร้อมกัน | สำเร็จหนึ่ง; อีกคำขอ 409 duplicate/stale; ไม่มีสองแถววันเดียวกัน | VR-04, DB unique |
| R-E04 | P0 | A เปิด version เก่า ขณะ B เปลี่ยนใบ แล้ว A บันทึก | 409 `STALE`; ต้องไม่ทับข้อมูล B | EC-06, API §2.3 |
| R-E05 | P0 | จำลอง 500 ตอน create/add/edit/cancel | แสดง error; ข้อมูลธุรกิจไม่เปลี่ยนแบบครึ่งเดียว; refresh แล้ว state ถูก | AC-12 |
| R-E06 | P1 | network timeout แล้ว client retry Idempotency-Key เดิม | ไม่สร้างผลซ้ำและให้ผลเดิมอย่างปลอดภัย | API §2.3 |
| R-E07 | P1 | notification service ล้มขณะบันทึก abnormal | เก็บหลักฐานว่าธุรกรรมหลัก/การ retry notification ทำอย่างไร; FRD ไม่กำหนด atomicity จึงเป็น OQ ถ้าพฤติกรรมไม่ชัด | FN-07 |
| R-E08 | P1 | กดบันทึกระหว่าง session หมดอายุ | ไม่บันทึกในชื่อผิดคน; แจ้งให้ login ใหม่; ไม่เกิด partial write | BR-06, security baseline |

### F. Notification

| ID | Pri | วิธีทดสอบย่อ | Expected ตาม FRD | Trace |
|---|---:|---|---|---|
| R-F01 | P0 | บันทึก abnormal ใหม่ | role-mgr-wh tenant เดียวกันได้รับ in-app+email | BR-03, NTF |
| R-F02 | P0 | เปิด notification | doc_no, location, abnormal_items, check_date ถูกและลิงก์ไม่ข้ามสิทธิ์ | FN-07 |
| R-F03 | P1 | บันทึก normal | ไม่เกิด `fec_abnormal_found` | FN-07 |
| R-F04 | P1 | แก้ normal→abnormal | เกิด `fec_abnormal_found` 1 ครั้งพร้อมค่าหลังแก้ | FN-05/07 |
| R-F05 | P1 | แก้ abnormal→abnormal โดยเปลี่ยนหัวข้อ | ตามถ้อยคำ FRD จะ emit เมื่อค่าหลังแก้ยังมี x; ตรวจการยิงซ้ำและเปิด OQ หากเสี่ยง spam | FN-07 |
| R-F06 | P1 | ปิด preference ของผู้จัดการแล้วบันทึก abnormal | event บังคับยังส่ง in-app+email เพราะปิดไม่ได้ | NTF |
| R-F07 | P1 | ยกเลิกใบ | role-mgr-wh ได้ in-app พร้อม actor/reason ถูก; preference อาจปิด event นี้ได้ | BR-12, NTF |
| R-F08 | P1 | ผู้จัดการหลายคน/ไม่มีผู้จัดการ | ทุกผู้รับตาม role ได้ตาม engine; กรณีไม่มีผู้รับต้องมี trace/retry/alert ไม่เงียบหาย (ส่วนหลังเป็น business observation) | NTF |

### G. PDF, CSV และไฟล์แนบ

| ID | Pri | วิธีทดสอบย่อ | Expected ตาม FRD | Trace |
|---|---:|---|---|---|
| R-G01 | P0 | PDF ใบเปล่า/1/12 checks | 1 หน้า A4, อย่างน้อย 12 แถว, 1 สถานที่, ค่า/และxตรงข้อมูล | BR-10, FN-09 |
| R-G02 | P0 | PDF 13 และ 24 checks | dense 1 หน้า A4, ไม่ตัดแถว/ซ้อน/เล็กจนอ่านค่าธุรกิจไม่ได้ | EC-02, AC-08 |
| R-G03 | P0 | PDF cancelled | ระบุ cancelled ชัด; ประวัติ/ข้อมูลเดิมไม่หาย; บันทึกเพิ่มไม่ได้ | FN-09, state machine |
| R-G04 | P1 | ตรวจลำดับแถว PDF | เรียงตามวันที่อย่างสม่ำเสมอและตรงกับ checks; เก็บหลักฐานทิศทางการเรียงเพราะ FRD ไม่ระบุ asc/desc | FN-09 |
| R-G05 | P1 | ตรวจภาษา/วันที่/ข้อความท้าย | วันที่ พ.ศ. `d MMM yy`; ข้อความใช้ `ผู้จำหน่าย`; ไม่มีช่องลงชื่อ | BR-10/11, FN-09 |
| R-G06 | P1 | เปลี่ยนชื่อสถานที่/ชื่อองค์กรหลังออกเลขแล้วพิมพ์ใหม่ | PDF ใช้ location/header snapshot เดิม | FN-03/09, DB |
| R-G07 | P1 | เปลี่ยนชื่อพนักงานหลังบันทึก check | แถวประวัติ/PDF ใช้ inspector_name_snapshot เดิม | DB §4.2 |
| R-G08 | P0 | กรองสถานะ/ผล/โซนแล้ว export CSV | CSV มีเฉพาะผลตาม filter และสิทธิ์ จำนวนตรง list/query | API-08, AC-10 |
| R-G09 | P1 | เปิด CSV ใน Excel | UTF-8 ภาษาไทยไม่เพี้ยน; วันที่/เลขที่ไม่ถูกตีความเสีย; คอลัมน์มีค่าธุรกิจตรงระบบ | API-08 |
| R-G10 | P0 | export ด้วย role ที่ไม่ควรเห็นชื่อทั้งหมด | inspector_name_snapshot ถูกแสดง/mask ตาม Policy Center และสิทธิ์ | §5.7, DB §4.6 |
| R-G11 | P1 | แนบ PDF/รูป/ชื่อไฟล์ไทยตอนสร้าง | แนบกับใบถูกใบ เปิด/ดาวน์โหลดได้ตามสิทธิ์; refresh แล้วยังอยู่ | API-09, DEC-10 |
| R-G12 | P0 | ใช้ attachment_id ของใบ/tenant อื่น | attach/read/delete ไม่ได้; ไม่มี IDOR | API-09, RLS |
| R-G13 | P1 | แนบ/ลบไฟล์หลัง card cancelled | state machine บอก cancelled=ล็อก แต่ API attachment ไม่ระบุ guard; เก็บพฤติกรรมและเปิด OQ หากยังแก้ได้ | §5.2, API-09 |
| R-G14 | P1 | ไฟล์ชนิด/ขนาดต้องห้ามและชื่อซ้ำ | ระบบปฏิเสธอย่างปลอดภัยตาม Document Center; ไม่เหลือ orphan/ไฟล์ครึ่งเดียว | Document Center dependency |

### H. รายการ ค้นหา กรอง และความถูกต้องหลัง refresh

| ID | Pri | วิธีทดสอบย่อ | Expected ตาม FRD | Trace |
|---|---:|---|---|---|
| R-H01 | P1 | ค้นด้วยเลขที่/สถานที่/ผู้สร้าง | ได้เฉพาะรายการตรงคำค้นและยังถูก scope ด้วยสิทธิ์ | UI P-01, FN-08 |
| R-H02 | P1 | กรอง status+last_result+zone พร้อมกัน | เงื่อนไขทำงานร่วมกัน; badge/count/pagination ตรงผลจริง | FN-08 |
| R-H03 | P1 | เปลี่ยน page size/page และย้อนหน้า | ไม่ซ้ำ/ไม่ตก; total และช่วง x–y ถูก | UI P-01 |
| R-H04 | P1 | หลัง add/edit/cancel ให้ refresh และ login ใหม่ | list/detail/result/count/status ยังตรงฐานข้อมูล ไม่ใช่ค่า cache หน้าเดิม | FN-04/05/06 |
| R-H05 | P1 | ใบที่ผลล่าสุดผิดปกติ แล้วเพิ่มผลใหม่ปกติ | badge “ผิดปกติ” และ filter อัปเดตตามผลวันที่ล่าสุด | BR-02, FN-08 |

## 7. Business-sense challenges — ต้องคุยกับ PM/BA แต่ยังไม่ถือเป็น bug

1. **พนักงานนอกแผนกสร้างใบได้และยกเลิกใบของตนได้** — ตรง permission matrix แต่สามารถยึดสถานที่ไว้ด้วย active card ทำให้คลังสร้างซ้ำไม่ได้ ควรยืนยันว่าเป็นเจตนาจริง
2. **abnormal ไม่มีขั้นรับทราบ/แก้ไข/ปิดประเด็น** — รอบนี้ out of scope งานซ่อม จึงแจ้งแล้วจบ ต้องยืนยันเจ้าของ operational follow-up ว่าใครติดตามต่อที่ไหน
3. **แก้ abnormal กลับเป็น normal ได้ภายในวันเดียวกัน** — ผลล่าสุดและแถบเตือนอาจหาย แต่ไม่มี `resolved` event และไม่มี manager acknowledgement; audit มีแต่ผู้รับอาจไม่รู้ว่าค่าถูกแก้
4. **แก้ abnormal เป็น abnormal อีกรอบอาจแจ้งซ้ำ** — FN-07 ระบุให้ยิงเมื่อแถวหลังแก้มี x แต่ไม่ได้กำหนด deduplication
5. **บันทึกย้อนหลังได้ไม่จำกัด** — FRD อนุญาตทุกวันที่ ≤ วันนี้ อาจกระทบความน่าเชื่อถือของบันทึกความปลอดภัย แม้ audit จะบอกวันบันทึกจริง
6. **ไม่มีหมายเหตุความผิดปกติ** — เป็น scope lock เพื่อให้กระดาษ 1:1 แต่ notification รู้เพียงหัวข้อที่ผิดปกติ ไม่รู้รายละเอียดอาการ
7. **24 แถวต้องบีบใน A4 หน้าเดียว** — ตรง FRD แต่ต้องพิสูจน์ว่าอ่านได้จริง มิฉะนั้นเป็น business usability risk ของเอกสาร ไม่ใช่ layout หน้าเว็บ
8. **เลขปี `FEC-YYYY-NNNN`** — ตัวอย่าง test เดิมคาด พ.ศ. แต่คำว่า YYYY ใน config ยังไม่ระบุชัด ควรยืนยันก่อนตัดสิน bug
9. **attachment หลังยกเลิก** — state machine บอกล็อก แต่ API attachment ไม่ระบุชัดว่าห้ามเพิ่ม/ลบ
10. **notification ล้มระหว่าง save** — FRD ไม่บอกว่าต้อง rollback ใบตรวจหรือใช้ outbox/retry จึงต้องถาม expected operational behavior

## 8. จุดขัด/คลุมเครือในชุดเอกสารที่ควรยึด FRD ก่อน

- FRD 05/06/01 ระบุ **ไม่มีช่องลงชื่อ** แต่ DEC-07/DOCCFG บางข้อความกล่าวถึงช่องลงชื่อ; ในการทดสอบรอบนี้ให้ใช้ FRD AC-08/BR-10 เป็นหลัก คือ PDF ไม่มีช่องลงชื่อ และเปิด OQ แทนการเดา
- Overview ยังแสดง OQ-03/OQ-04 แม้สถานะเขียนว่า Ready for Dev หลัง OQ ปิดแล้ว; ถ้า production ใช้ master/location จริง ให้บันทึกรหัส integration ที่ใช้อยู่เพื่อปิดช่องว่างเอกสาร
- DEC-02 กล่าว “ไม่ส่งต่อระบบอื่น” แต่ FRD บังคับ ENG-NOTIFY; ตีความว่าไม่ส่ง Asset/Maintenance แต่ยังต้องส่ง notification ตาม BR-03/FN-07

## 9. Exit criteria ของ full review

ถือว่ารอบ review เสร็จเมื่อ:

- P0 ทุกเคสมี Pass/Fail/Blocked และหลักฐานครบ
- P1 ทุกเคสที่ environment รองรับมีผล; ข้อที่รันไม่ได้ระบุ blocker/owner ชัด
- ทุก BR-01..13, VR-01..06, AC-01..12 และ deny case TC-D01..06 มีผลอย่างน้อยหนึ่งเคส
- ทุก bug ผูกกับ FRD และทำซ้ำได้
- ทุก OQ/suggestion แยกจาก bug
- ไม่ใช้คำว่า “ผ่านทั้งหมด” หาก concurrency, permission server-side, notification หรือ data integrity ยังไม่ได้ตรวจ

## 10. แบบบันทึกผลย่อ

| Case | Result (Pass/Fail/Blocked) | Actual | Evidence | Bug/OQ | ผู้ทดสอบ | เวลา |
|---|---|---|---|---|---|---|
| R-A01 |  |  |  |  |  |  |

เมื่อรันเสร็จให้นำผลจริงมาสร้าง Feature Check Report โดยแยก Logic · UI · UX · Bug และห้ามเติม Pass ให้เคสที่ไม่ได้รัน
