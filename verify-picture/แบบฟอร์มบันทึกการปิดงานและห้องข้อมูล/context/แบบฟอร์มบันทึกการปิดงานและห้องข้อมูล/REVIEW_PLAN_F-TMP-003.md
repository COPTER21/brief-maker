# แผน Full Review — F-TMP-003 แบบฟอร์มบันทึกการปิดงานและห้องข้อมูล

> สถานะเอกสารนี้: แผนตรวจและ checklist สำหรับ production review — **ยังไม่ใช่ผลการทดสอบ**
>
> Baseline: FRD-F-TMP-003 v1.0 ลงวันที่ 2026-10-11 โดยยึด `03_LOGIC`, `05_RULES`, `06_TESTS`, `07_LOCKED_DECISIONS` เป็นหลัก

## 1. คำตอบสั้น ๆ ว่าควรตรวจอย่างไร

PM/BA บอกให้ “อิงแค่ FRD” ถือว่าถูกสำหรับการตัดสินว่าเป็น defect หรือไม่ แต่ไม่ควรอ่าน FRD แล้วเล่นเฉพาะ happy path ควรแปลง FRD เป็น 5 กลุ่มตรวจ:

1. กฎธุรกิจและ validation
2. วงจรสถานะตั้งแต่ร่างจนอนุมัติ/ส่งกลับ/ยกเลิก
3. สิทธิ์และการมองเห็นข้อมูล
4. ผลข้างเคียง เช่น เลขเอกสาร PDF audit notification attachment และ CSV
5. กรณีผิดปกติ เช่น กดซ้ำ เปิดสองหน้าจอ config เปลี่ยนระหว่างทาง และบริการภายนอกล้ม

เกณฑ์ตัดสิน:

- พฤติกรรมต่างจาก FRD ที่ระบุชัด = Bug
- FRD ไม่ได้ระบุ แต่เสี่ยงธุรกิจ/ข้อมูล = Observation หรือ OQ ให้ BA ตัดสิน ห้ามตีเป็น Bug เอง
- พฤติกรรมตรง FRD แต่ใช้งานไม่เหมาะ = Improvement
- ตรวจไม่ได้เพราะไม่มี role/log/config/access = Not tested พร้อมระบุ blocker

## 2. ข้อควรรู้ก่อนเริ่ม

- Test case เดิม 48 เคสเขียนสำหรับ prototype `feature.html` และใช้ seed/ชื่อ/จำนวนรายการตายตัว จึงใช้เป็นแนวทางได้ แต่ห้ามนำ expected เช่น “7 รายการ”, “เลข 0012” ไปเทียบ production ตรง ๆ
- DevPack ระบุว่าเดิมเป็น `NO-BROWSER` และไม่มี `e2e_standard` report จึงไม่ควรถือว่าหลักฐานใน pack ยืนยัน production แล้ว
- กฎหลายข้อเป็น `[AI-DEFAULT]` และเอกสารระบุว่ารอลูกค้าเซ็นยืนยัน OQ-02 หาก production ทำไม่ตรง ให้เปิดเป็น “Deviation from FRD” ก่อน และแจ้ง BA ว่าต้นทางเป็น AI-DEFAULT
- ทดสอบ production ด้วยบัญชี/โครงการทดสอบที่ได้รับอนุญาตเท่านั้น ห้ามใช้ข้อมูลลงทุนจริง ห้ามอนุมัติหรือส่ง notification ถึงคนจริงโดยไม่ประสาน owner
- ก่อนทดสอบเคสที่สร้างเอกสาร แจ้งผู้ดูแลเรื่องเลข IVMK เพราะ FRD ยอมให้เลขขาด (`no-gap = false`) และใบยกเลิกอาจคงอยู่ถาวร

## 3. สิ่งที่ต้องขอให้พร้อม

- [ ] บัญชี 5 แบบ: owner, approver ขั้น 1, approver ขั้น 2, admin ฝ่ายบริหารการลงทุน, บุคคลนอกสาย
- [ ] tenant ทดสอบอย่างน้อย 2 tenant สำหรับยืนยัน RLS หรือหลักฐานจากผู้ดูแลระบบ
- [ ] สิทธิ์ดู audit log, notification delivery, Document Center และ approved PDF ที่เก็บจริง
- [ ] ชุด DOA ทดสอบ 1, 2 และ 6 ขั้น หรือผู้ดูแลช่วยสลับ config
- [ ] สิทธิ์เปลี่ยน `ivmk.checklist_items` และปิด/เปิด doc type IVMK ในช่วงทดสอบ
- [ ] ไฟล์ทดสอบ: PDF/DOC/XLS/รูปที่ถูกต้อง, ไฟล์เกิน 20 MB, ไฟล์นามสกุลปลอม, ชนิดไม่รองรับ
- [ ] ช่องทาง cleanup ที่ไม่ลบ audit และไม่กระทบข้อมูลจริง

ถ้าขอได้ไม่ครบ ให้ทดสอบเท่าที่มีและเขียน “ไม่ได้ตรวจ” แยก อย่าลงชื่อรับรองทั้ง feature

## 4. ลำดับการตรวจที่แนะนำ

### รอบ A — Production smoke แบบเสี่ยงต่ำ

- [ ] เปิดหน้ารายการ ค้นหา กรอง pagination และเปิดรายละเอียดได้
- [ ] owner สร้างร่างขั้นต่ำหนึ่งใบ ได้เลข IVMK และ checklist จาก config
- [ ] แก้ร่าง บันทึก ปิดหน้า แล้วเปิดใหม่ ข้อมูลไม่หาย
- [ ] preview PDF ของร่างและดาวน์โหลดได้
- [ ] ยกเลิกร่างทดสอบโดยระบุเหตุผล และตรวจ audit

ถ้ารอบนี้มีข้อมูลหาย เลขซ้ำ 5xx สิทธิ์รั่ว หรือกระทบใบจริง ให้หยุดและ escalate ก่อนทำ flow หนัก

### รอบ B — Core business flow

ทำอย่างน้อย 4 ใบแยกกัน ไม่ใช้ใบเดียววนทุกกรณี:

| ใบ | Flow | จุดพิสูจน์หลัก |
|---|---|---|
| A | draft → submit → approve ขั้น 1 → approve ขั้นสุดท้าย | happy path, chain, notification, final PDF, lock |
| B | draft → submit → reject → edit → resubmit → approve | เลขเดิม, เหตุผล, audit เดิม, resolve DOA ใหม่ |
| C | draft → cancel | owner/admin, เหตุผล, state lock |
| D | draft → submit → cancel | pending steps เป็น skipped, current approver ได้แจ้งเตือน |

### รอบ C — Negative, permission และ resilience

เน้นกรณีที่ tester มักพลาด: direct URL, กดซ้ำ, สอง tab, role ผิด, config เปลี่ยน และ downstream ล้ม

## 5. Detailed review matrix

ช่องผลใช้ `Pass / Fail / Not tested` พร้อมแนบหลักฐานทุกแถวที่ Fail

### 5.1 สร้างและแก้ร่าง

| ID | วิธีตรวจ | Expected ตาม FRD | ผล |
|---|---|---|---|
| CR-01 | สร้างใบใหม่ด้วย owner | ได้เลข `IVMK-...` ตอน save ครั้งแรก; checklist มาจาก config; ทุกข้อเริ่ม “ยังไม่ดำเนินการ” | ☐ |
| CR-02 | refresh/เปิดใหม่หลัง save | เลขและข้อมูลเดิม ไม่สร้างใบหรือเลขซ้ำ | ☐ |
| CR-03 | บันทึกร่างทั้งที่ checklist ยังไม่ครบ | บันทึกได้ แต่ส่งไม่ได้ | ☐ |
| CR-04 | แก้ถ้อยคำ/เพิ่ม/ลบ checklist ผ่าน UI และ request | ทำไม่ได้; server ยึด snapshot | ☐ |
| CR-05 | เปลี่ยน `done` กลับเป็นสถานะอื่น | `done_date` ถูกล้าง; ข้อมูลไม่ค้างหลอก | ☐ |
| CR-06 | lesson แถวว่างทั้งหมด | ไม่ถูกบันทึกเป็นแถวข้อมูล | ☐ |
| CR-07 | กรอกช่องอื่นของ lesson แต่ไม่กรอก topic | ถูกบล็อกและบอกให้ใส่ประเด็น | ☐ |
| CR-08 | owner สอง tab แก้ใบเดียวกัน แล้ว save tab เก่า | ได้ 409 STALE; ข้อมูลใหม่ไม่ถูกทับ | ☐ |
| CR-09 | กด save ซ้ำ/เน็ตช้าแล้วกดซ้ำ | ได้ผลครั้งเดียวจาก Idempotency-Key; ไม่เกิดใบ/เลขซ้ำ | ☐ |
| CR-10 | doc type IVMK ถูกปิด | สร้างไม่ได้; 409 DOC_TYPE_INACTIVE; ไม่มีใบครึ่งสำเร็จ | ☐ |

### 5.2 Validation และกฎ checklist

| ID | วิธีตรวจ | Expected ตาม FRD | ผล |
|---|---|---|---|
| VR-01 | เว้น project name, outcome, archive location, closing date หรือ post owner | บล็อกด้วยข้อความตรงช่อง | ☐ |
| VR-02 | เลือก closing date อนาคต | บล็อก เพราะ closing date ต้องไม่เกินวันนี้ | ☐ |
| VR-03 | status = done แต่ไม่กรอก owner/done date | บล็อกทั้งสองช่อง | ☐ |
| VR-04 | done date หลัง closing date | บล็อกด้วยข้อความ “วันที่ดำเนินการต้องไม่เกินวันที่ปิดงาน” | ☐ |
| VR-05 | บันทึก done date ไว้ แล้วเลื่อน closing date ย้อนก่อนวันดังกล่าว | save/submit ต้องถูกบล็อก ไม่ปล่อยข้อมูลผิด | ☐ |
| VR-06 | status = na แต่ไม่กรอก remark | บล็อกด้วยข้อความ “ไม่เกี่ยวข้อง ต้องระบุหมายเหตุ” | ☐ |
| VR-07 | submit ขณะมี not_started/in_progress | 422 CHECKLIST_INCOMPLETE และบอกจำนวนที่ยังไม่ครบ | ☐ |
| VR-08 | ข้อ CK08 “บันทึกบทเรียนที่ได้รับ” = done แต่ไม่มี lesson | 422 LESSON_REQUIRED | ☐ |
| VR-09 | CK08 = na พร้อม remark แต่ไม่มี lesson | ส่งได้ เพราะ FRD บังคับ lesson เฉพาะ CK08 = done | ☐ |
| VR-10 | ทุกข้อ done/na ครบ | submit ผ่าน หาก assignee ถูกต้อง | ☐ |

### 5.3 DOA และสถานะเอกสาร

| ID | วิธีตรวจ | Expected ตาม FRD | ผล |
|---|---|---|---|
| WF-01 | เปิด preview ผู้อนุมัติ | จำนวน slot เท่า DOA ปัจจุบัน; resolve ค่าเริ่มถูก role | ☐ |
| WF-02 | เลือกผู้จัดทำเป็น approver หรือปล่อย slot ว่าง | ถูกบล็อก SELF_APPROVAL/ASSIGNEE_REQUIRED | ☐ |
| WF-03 | submit | status เป็น pending ขั้น 1; chain ถูก freeze | ☐ |
| WF-04 | approver ขั้น 2 พยายาม approve ก่อนขั้น 1 | ไม่มีปุ่มและ server ตอบ 403 NOT_CURRENT_APPROVER | ☐ |
| WF-05 | ขั้น 1 approve | คำตัดสิน “ตรวจสอบแล้ว”; ขั้น 2 เป็น current | ☐ |
| WF-06 | ขั้นสุดท้าย approve | status approved; approved_by/at ถูกคนและเวลา | ☐ |
| WF-07 | reject โดยไม่ใส่เหตุผล | บล็อก REASON_REQUIRED | ☐ |
| WF-08 | reject พร้อมเหตุผล | กลับ draft เลขเดิม; แสดงเหตุผล; chain เดิมลง audit แล้วล้าง | ☐ |
| WF-09 | เปลี่ยน DOA หลัง reject แล้ว resubmit | resolve chain ใหม่ตาม DOA ใหม่ | ☐ |
| WF-10 | เปลี่ยน DOA ระหว่างใบ pending | chain ใบเดิมไม่เปลี่ยน | ☐ |
| WF-11 | approved แล้วลอง edit/submit/reject/cancel/เปลี่ยน attachment | ถูกล็อกทั้งหมด; ถ้า attachment ยังแก้ได้ให้เปิด OQ/High risk เพราะ FRD ระบุ approved = locked แต่ API attachment ไม่เขียนข้อจำกัดสถานะชัด | ☐ |
| WF-12 | กด approve/submit ซ้ำหรือ replay request | ผลเกิดครั้งเดียว; ไม่มี notification/PDF/audit ซ้ำ | ☐ |

### 5.4 สิทธิ์ ความลับ และ tenant

| ID | วิธีตรวจ | Expected ตาม FRD | ผล |
|---|---|---|---|
| PM-01 | owner เปิดร่างของ owner คนอื่นด้วย direct URL | 404 NOT_FOUND ไม่ใช่ 403 และไม่เผยว่ามีใบ | ☐ |
| PM-02 | approver เปิดร่างก่อน submit | ไม่เห็นและได้ 404 | ☐ |
| PM-03 | คนใน chain หลัง submit เปิดใบ | ดูได้ แต่ตัดสินได้เฉพาะ current approver | ☐ |
| PM-04 | คนนอกสายลองดู/แก้/ยกเลิก/ดาวน์โหลด PDF/attachment | ดูเป็น 404; write ถูกปฏิเสธ; ไม่มีข้อมูลรั่วใน error | ☐ |
| PM-05 | admin | เห็นทุกใบ แต่แก้/submit/approve ไม่ได้; ยกเลิกได้เฉพาะ draft/pending | ☐ |
| PM-06 | owner | แก้/submit ได้เฉพาะ draft ของตน; ยกเลิก draft/pending ของตน | ☐ |
| PM-07 | สลับ tenant หรือแก้ ID/request | RLS กัน list/detail/CSV/PDF/attachment ทุกทาง | ☐ |
| PM-08 | ค้นหา/CSV ด้วยคำที่ตรงใบไม่มีสิทธิ์ | จำนวนและข้อมูลของใบต้องไม่รั่ว | ☐ |
| PM-09 | session หมดอายุขณะ save/approve | ไม่เปลี่ยนสถานะครึ่งเดียวและไม่แสดงข้อมูลต่อหลัง logout | ☐ |

### 5.5 ยกเลิก

| ID | วิธีตรวจ | Expected ตาม FRD | ผล |
|---|---|---|---|
| CX-01 | owner/admin ยกเลิก draft โดยไม่ใส่เหตุผล | ถูกบล็อก | ☐ |
| CX-02 | owner/admin ยกเลิก draft พร้อมเหตุผล | status cancelled; แก้/ส่งต่อไม่ได้; audit ครบ | ☐ |
| CX-03 | owner/admin ยกเลิก pending | current/waiting steps เป็น skipped; ยิง ivmk_cancelled ถึง current approver | ☐ |
| CX-04 | approver/คนนอกยกเลิก | 403 NOT_OWNER | ☐ |
| CX-05 | ยกเลิก approved/cancelled | 409 NOT_CANCELLABLE | ☐ |

### 5.6 PDF เอกสารเลขที่ และ snapshot

| ID | วิธีตรวจ | Expected ตาม FRD | ผล |
|---|---|---|---|
| DOC-01 | เปิด PDF draft/pending/approved/cancelled | 2 หน้า; หน้า 1/2 และ 2/2; form code FM-IVM-11 | ☐ |
| DOC-02 | เทียบทุก field กับหน้าจอ/ฐานข้อมูล | ชื่อบริษัท โครงการ วันที่ไทย ผลลัพธ์ owner ที่จัดเก็บ checklist lesson ตรงกัน | ☐ |
| DOC-03 | ตรวจ checklist และ lesson | checklist ตาม snapshot อย่างน้อย 8; lesson เติมว่างอย่างน้อย 10 | ☐ |
| DOC-04 | DOA 1/2/6 ขั้น | แถวลงชื่อ = ผู้จัดทำ + จำนวนขั้น (2/3/7 แถว) และคำตัดสินตาม role | ☐ |
| DOC-05 | lesson 14 แถวหรือข้อความยาวมาก + DOA 6 ขั้น | ยัง 2 หน้า; ไม่ตัดข้อความ/ลายเซ็น; header ตารางซ้ำ; dense ตามกฎ | ☐ |
| DOC-06 | เปลี่ยนชื่อ/โลโก้บริษัทหรือ config checklist หลังสร้าง | ใบเดิมใช้ header/checklist snapshot; ใบใหม่ใช้ค่าใหม่ | ☐ |
| DOC-07 | เปลี่ยนชื่อ/ตำแหน่ง maker หรือ post owner หลังสร้าง | PDF/ใบเดิมแสดง snapshot ตามที่ FRD กำหนด | ☐ |
| DOC-08 | approved final | PDF ถูกเก็บใน Document Store เป็น `approved_final`; ดาวน์โหลดซ้ำได้ไฟล์เดิม ไม่ regenerate ตาม config ใหม่ | ☐ |
| DOC-09 | retry สร้าง/save | doc no ไม่ซ้ำ; tenant อื่นไม่ชน; เลขขาดยอมรับได้ | ☐ |

### 5.7 Notification และผลข้างเคียง

| ID | วิธีตรวจ | Expected ตาม FRD | ผล |
|---|---|---|---|
| NT-01 | pending ถูกยกเลิก | `ivmk_cancelled` ไป current approver หนึ่งครั้ง | ☐ |
| NT-02 | อนุมัติขั้นสุดท้าย | `ivmk_closed_handover` ไป post owner และ checklist owners | ☐ |
| NT-03 | อนุมัติขั้นสุดท้ายและ lesson มีกำหนดส่ง | `ivmk_lesson_assigned` ไป lesson owner ของแต่ละแถว | ☐ |
| NT-04 | owner ซ้ำหลายรายการ/หลายบทเรียน | ตรวจ dedup ตาม contract; หาก FRD ไม่ชัดให้บันทึก OQ ไม่เดา | ☐ |
| NT-05 | อนุมัติ | ไม่ยิง `ivmk.approved`; ไม่ยิง DOA pending/result ซ้ำเอง | ☐ |
| NT-06 | notification service ล้ม | การอนุมัติและ audit ต้องไม่อยู่ในสถานะครึ่งสำเร็จ; behavior retry ต้องมีหลักฐานจาก log | ☐ |

### 5.8 Attachment, CSV, audit และความทนทาน

| ID | วิธีตรวจ | Expected ตาม FRD | ผล |
|---|---|---|---|
| EX-01 | อัปโหลด PDF/DOC/XLS/รูปต่ำกว่า 20 MB | แนบผ่าน Document Center ด้วย ref_type IVMK | ☐ |
| EX-02 | ไฟล์เกิน 20 MB/ชนิดไม่รองรับ/นามสกุลปลอม | ถูกปฏิเสธ; ไม่เหลือ orphan file | ☐ |
| EX-03 | ผู้ไม่มีสิทธิ์เปิด/ลบ attachment ด้วย URL/API | ถูกปฏิเสธและไม่รั่วชื่อไฟล์ | ☐ |
| EX-04 | CSV หลังใช้ search/status/checklist/mine_to_act | ได้เฉพาะผลตาม filter และสิทธิ์เดียวกับหน้ารายการ | ☐ |
| EX-05 | เปิด CSV ใน Excel | ภาษาไทย วันที่ และอักขระพิเศษไม่เพี้ยน; formula-like input ไม่กลายเป็นสูตรอันตราย | ☐ |
| EX-06 | ทุก write ใน flow A-D | audit append-only ครบ actor/action/เวลา/before-after/reason; ไม่มีทางแก้/ลบ | ☐ |
| EX-07 | API/เครือข่ายล้มระหว่าง save/submit/approve | UI ไม่แสดงสำเร็จหลอก; refresh แล้ว state ตรง server | ☐ |
| EX-08 | กด Back/refresh ระหว่างกรอก | เตือนข้อมูลค้างหรือรักษาร่างตามพฤติกรรมที่ออกแบบ; ไม่เกิด duplicate | ☐ |

## 6. Exploratory flow ที่ควร “ลองเล่น” เพิ่มด้วย business sense

1. ทำใบที่มีข้อความไทย/อังกฤษยาวมาก ตัวเลข ชื่อไฟล์ยาว และอักขระ `& < > " ' /` เพื่อจับข้อมูลขาดและ injection
2. เปิดใบเดียวกันด้วย owner และ approver พร้อมกัน เปลี่ยนสถานะจากอีกหน้าหนึ่ง แล้วกด action ในหน้าที่ stale
3. submit ตอน 23:59 และเปิดวันถัดไป เพื่อตรวจ timezone Asia/Bangkok วันที่ไทย และ notification time
4. ให้ owner/checklist owner/lesson owner เป็นคนเดียวกันหลายช่อง ดูว่า notification ซ้ำจนรบกวนหรือไม่
5. เปลี่ยน config checklist หลังสร้างแต่ก่อน submit และเปลี่ยน DOA หลัง submit เพื่อพิสูจน์ snapshot คนละชนิด
6. สร้าง lesson เกิน 10 แถวและ DOA 6 ขั้นพร้อมกัน เพราะเป็นคู่ที่เสี่ยงทำ PDF 2 หน้าไม่สำเร็จที่สุด
7. ลองค้นหา/CSV/PDF/attachment ด้วย direct URL จากบัญชีที่ไม่มีสิทธิ์ ไม่ตรวจแค่ปุ่มถูกซ่อน
8. หลัง approved ให้ลองทุก write path รวม attachment เพราะ “approved = ล็อก” แต่สัญญา API ของ attachment ไม่ระบุ state guard ชัด

## 7. จุดที่ต้องส่งกลับ BA/PM เป็นคำถาม ไม่ควรตัดสินเอง

1. กฎ DEC-04/14–17 หลายข้อเป็น AI-DEFAULT และรอลูกค้าเซ็น: ลูกค้ายืนยันแล้วหรือยัง และ production baseline ถือ FRD v1.0 นี้จริงหรือไม่
2. approved แล้ว attachment เพิ่ม/ลบได้หรือไม่ — state machine บอกล็อก แต่ API attachment ไม่ระบุ
3. notification recipient ที่เป็นข้อความอิสระใน checklist/lesson จะ map เป็นผู้ใช้จริงอย่างไร โดยเฉพาะ “หน่วยงาน/ที่ปรึกษาภายนอก”
4. ถ้า notification หรือ Document Store ล้ม การ approve ต้อง rollback ทั้งหมด หรือ approve แล้ว retry ภายหลัง
5. PDF ต้อง 2 หน้าเสมอแม้ lesson “ไม่จำกัดจำนวน” จริงหรือไม่ เพราะ FRD ทดสอบตัวอย่าง 14 แถว แต่ไม่ได้กำหนดเพดาน
6. retention จริงอิง Policy Center ข้อใด และ cancelled/draft เก็บนานเท่าไร
7. CSV มีข้อมูล Confidential/PII ต้อง mask, watermark, audit download หรือจำกัด role เพิ่มหรือไม่

## 8. วิธีบันทึกหลักฐานและรายงาน

ทุก Fail ควรมี:

- Case ID จาก matrix นี้ และอ้าง FRD เช่น `BR-07 / FN-04 / API-06`
- เวลาและ environment/build
- actor/role และเลขเอกสารทดสอบ
- ขั้นตอนทำซ้ำสั้น ๆ
- Expected ตาม FRD เทียบ Actual ที่เห็นจริง
- screenshot หรือคลิป พร้อม request/response และ log หากมี
- ผลกระทบทางธุรกิจ ไม่ใช่แค่ “ปุ่มไม่ทำงาน”

ระดับแนะนำ:

- Critical: ข้าม tenant/สิทธิ์/สายอนุมัติ, ข้อมูลหาย, approved ถูกแก้ได้
- High: เงิน/สถานะ/เลข/PDF/ผู้รับแจ้งผิด, เอกสารซ้ำ, submit/approve ซ้ำ
- Medium: ผิด FRD แต่มีทางเลี่ยง, audit ขาด, filter/CSV ผิดบางกรณี
- Low: ข้อความ/format เล็กน้อยที่ไม่ทำให้ตัดสินใจผิด

เมื่อทดสอบเสร็จจึงค่อยสร้าง Feature Check Report โดยใส่เฉพาะผลที่ตรวจจริง; แถวที่ไม่ได้แตะต้องเป็น `Not tested` ห้ามสรุปผ่านแทน

## 9. Definition of review complete

ถือว่า review รอบนี้ครบเมื่อ:

- [ ] AC-01..14, TC-D01..07, BR-01..15, VR-01..11 และ EC-01..11 มีผลหรือเหตุผลที่ Not tested
- [ ] flow A-D มีหลักฐานครบตั้งแต่ UI → status → audit → notification/PDF
- [ ] ทดสอบอย่างน้อย owner/current approver/non-current approver/admin/outsider
- [ ] direct URL/API permission และ tenant isolation มีหลักฐาน
- [ ] idempotency, stale update และ downstream failure มีหลักฐานหรือ owner ระบบรับรอง
- [ ] แยก Bug / Observation / Improvement / OQ ชัดเจน
- [ ] PM/BA รับทราบ scope ที่ไม่ได้ตรวจและ AI-DEFAULT ที่ยังไม่ยืนยัน

