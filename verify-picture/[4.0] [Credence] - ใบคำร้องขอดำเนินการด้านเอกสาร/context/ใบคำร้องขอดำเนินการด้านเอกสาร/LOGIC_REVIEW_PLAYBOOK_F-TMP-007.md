# Logic & Business Review Playbook — F-TMP-007 ใบคำร้องขอดำเนินการด้านเอกสาร (DAR)

วันที่จัดทำ: 12 พฤศจิกายน 2569  
ฐานอ้างอิงหลัก: FRD-F-TMP-007 v1.0 (`00_OVERVIEW` ถึง `07_LOCKED_DECISIONS`)  
วัตถุประสงค์: ใช้ตรวจ production รอบเก็บตกด้าน business logic, workflow, permission, data integrity และ integration โดยไม่รับรอง layout/UI ที่ทีมเดิมปิดงานแล้ว

## 1. ข้อสรุปก่อนเริ่มตรวจ

1. ใช้ FRD เป็น expected result หลักตามคำสั่ง PM/BA ได้ แต่ห้ามถือว่าทุกกฎใน FRD ผ่านการยืนยันทางธุรกิจแล้ว เพราะ `07_LOCKED_DECISIONS` ระบุว่า DEC-01..11 เป็น `AI-DEFAULT` และ `00_OVERVIEW §0.13` ยังมี OQ-01..07 ค้างอยู่
2. เอกสารใน context แสดงว่า test design ครอบคลุม 69 เคส แต่ไม่ได้เป็นหลักฐานว่าระบบ production ผ่าน 69 เคส: `RUN_LOG` ระบุ `[NO-BROWSER]` และมีเคสที่ถูกตัดจาก UAT เพราะต้องตรวจหลังบ้าน/ระบบเชื่อมต่อ
3. รอบนี้ควรเน้น P0/P1 ด้านสิทธิ์, สายอนุมัติ, สถานะ, เลขเอกสาร, notification, audit, concurrency และข้อมูลใน PDF/CSV มากกว่าตำแหน่งหน้าจอ
4. ห้ามใช้ข้อมูลจริงหรือส่งอีเมลถึงหน่วยงานจริงโดยไม่ตกลงก่อน ให้ใช้ test company/test recipients และตั้งชื่อเอกสารขึ้นต้น `[LOGIC-REVIEW-YYYYMMDD]`

## 2. ประเด็นที่ต้องให้ PM/BA รับทราบก่อนเซ็นผล

| ID | ประเด็นจาก FRD | สิ่งที่ต้องยืนยัน |
|---|---|---|
| BQ-01 | อนุมัติครบแล้วระบบเพียงแจ้งหน่วยงาน แต่ไม่ขึ้นทะเบียน/แก้ทะเบียนเอกสารควบคุมจริง (Out of Scope, DEC-01/02, OQ-06) | นี่คือ process ที่ production ต้องการจริงหรือยังมีงาน manual ต่อ |
| BQ-02 | DOA ค่าเริ่ม 4 ขั้น และ `role-doc-controller`, `role-mgr-ocs` เคยอยู่นอก DOA contract (OQ-03) | role จริงใน production resolve ได้ทุกบริษัท/BU หรือไม่ |
| BQ-03 | ไม่อนุมัติทุกขั้น = กลับ Draft เลขเดิม ล้างสายเดิม และส่งใหม่เริ่มขั้น 1 (BR-09, EC-16) | ต้องการ restart ทั้งสายจริงหรือควรย้อนเพียงบางขั้น |
| BQ-04 | ผู้พิจารณาเห็นเอกสารหลังส่งทุกคนในสาย ไม่ใช่เฉพาะ current approver (BR-11) | การเปิดเผยข้อมูลล่วงหน้าให้ขั้นถัดไปยอมรับได้หรือไม่ |
| BQ-05 | ผู้ควบคุมเอกสารเป็นผู้บันทึกชื่อผู้รับ; ผู้รับไม่ได้กดยืนยันเอง (OQ-05) | หลักฐานการรับเพียงพอต่อ audit หรือไม่ |
| BQ-06 | หน่วยงานแจกจ่ายมี 27 ช่อง และบางชื่อซ้ำติด `(2)` (OQ-04) | mapping ไปยังหน่วยงานจริงและผู้รับ notification ถูกต้องหรือไม่ |
| BQ-07 | เลขออกตั้งแต่บันทึกร่างครั้งแรกและยอมให้เลขขาดได้ (BR-10) | ฝ่ายควบคุมเอกสารยอมรับ gap จากร่าง/ยกเลิกหรือไม่ |
| BQ-08 | คนเดียวอาจถือหลาย role ในหลายขั้น; FRD ห้ามเฉพาะผู้จัดทำอนุมัติตัวเอง | อนุญาตให้ approver คนเดียวอนุมัติหลายขั้นติดกันหรือไม่ |
| BQ-09 | วันที่บังคับใช้ก่อนวันที่เขียน DAR แค่เตือนและยังส่งได้ (BR-06) | ยอมรับย้อนหลังได้จริงหรือไม่ และต้องเก็บเหตุผลหรือไม่ |

หากคำตอบต่างจาก FRD ให้รายงานเป็น `Specification / Business Decision Gap` ไม่ควรตีเป็น bug ของระบบทันที

## 3. ชุดบัญชีและข้อมูลที่ต้องเตรียม

| ชุด | ต้องมี |
|---|---|
| Accounts | Maker A, Maker B, Approver Step 1–4, Document Controller, ผู้ใช้ไม่เกี่ยวข้อง และถ้าเป็นไปได้ผู้ใช้คนเดียวที่ถือ 2 approval roles |
| Organization | หน่วยงานแจกจ่ายอย่างน้อย 2 หน่วยงาน พร้อมผู้รับ notification ที่ตรวจ inbox/log ได้ |
| DOA | สายมาตรฐาน 4 ขั้น และสายทดสอบ 5/6 ขั้น หรือสิทธิ์ให้ผู้ดูแลเปลี่ยน configuration ชั่วคราวใน test tenant |
| Document Config | doc type `DAR` แบบ active; เคส inactive ให้ทำเฉพาะ test tenant หรือ staging ห้ามปิด production จริง |
| Data | เอกสารใหม่, แก้ไข, ยกเลิก, อื่น ๆ; related documents 0/1/14/18+ แถว; email เดี่ยว/หลายค่า/ผิดรูปแบบ |
| Evidence | screen recording หรือภาพก่อน-หลัง, DAR.No., เวลา, user/role, request ID, notification ID, PDF/CSV และ audit log |

## 4. ลำดับตรวจที่แนะนำ

### Phase A — Smoke flow ที่ต้องผ่านก่อน (P0)

| ID | วิธีตรวจ | ผลที่ต้องได้ตาม FRD | อ้างอิง |
|---|---|---|---|
| P0-01 | Maker A สร้างข้อมูลครบและบันทึกร่าง | ได้เลข DAR ทันที, status Draft, เลขไม่เปลี่ยนเมื่อแก้ไข | FN-02, BR-10, AT-01 |
| P0-02 | ส่งอนุมัติด้วยสาย 4 ขั้น | resolve คนครบทุกขั้น, Maker ไม่อยู่ในรายชื่อ, status Pending step 1 | FN-03, BR-08, VR-11 |
| P0-03 | Step 1→4 อนุมัติตามลำดับ | มีเพียง current approver ที่กดได้; ขั้นถัดไปเปิดทีละขั้น; ขั้นสุดท้ายเป็น Approved | FN-04, EC-11, DN-04 |
| P0-04 | ตรวจหลังอนุมัติครบ | สร้างและเก็บ approved PDF, ส่ง `dar_distributed`, ไม่สร้าง/แก้ทะเบียนเอกสารควบคุม | FN-04, BR-13, DEC-01/02 |
| P0-05 | Document Controller บันทึกผู้รับ | ต้องเลือก receiver, receiver ต้องไม่ใช่ Maker, status Received, มี audit และ `dar_received` | FN-08, VR-13 |
| P0-06 | เปิดประวัติและ PDF จากใบ Received | เห็น actor/time/decision ครบ; PDF แสดงผู้จัดทำ ทุกขั้นอนุมัติ และข้อความลงนามรับตรงข้อมูลจริง | FN-07/08, BR-12/15 |

หยุดและแจ้งทันทีถ้า P0 ข้อใดทำให้ข้ามผู้อนุมัติ, คนไม่มีสิทธิ์เห็น/ตัดสิน, สถานะผิด, ข้อมูลสูญหาย, เลขซ้ำ หรือส่ง notification ผิดคน

### Phase B — Validation และ conditional logic (P1)

| ID | กรณีที่ต้องเล่น | Expected |
|---|---|---|
| P1-01 | ไม่เลือก Purpose / ISSUE / ไม่กรอกชื่อเอกสาร | บล็อกด้วย VR-01/02/03 |
| P1-02 | Purpose = แก้ไข; เว้นเดิมหรือใหม่ทีละช่อง | บล็อก VR-05/06 |
| P1-03 | Purpose = ขึ้นทะเบียนใหม่ | Document No. เว้นได้; `change_after` บังคับ |
| P1-04 | Purpose = ยกเลิก | Document No. เว้นได้ตาม EC-17; เดิม/ใหม่ไม่บังคับ |
| P1-05 | Purpose = อื่น ๆ | ต้องอธิบายใน `Revision / ISSUE ใหม่` |
| P1-06 | Origin = อื่น ๆ แล้วไม่กรอกรายละเอียด | บล็อก VR-04; เมื่อเปลี่ยน origin ให้ตรวจว่าค่าเก่าถูกล้างหรือไม่ถูกส่งแบบซ่อน |
| P1-07 | วันที่บังคับใช้ก่อนวัน DAR | แสดง warning แต่บันทึก/ส่งได้; warning ไม่กลายเป็น error |
| P1-08 | related row กรอกเพียง Document No. และสลับกรอกเพียงชื่อ | บล็อกทั้งสองทิศ; แถวว่างทั้งแถวไม่บล็อก |
| P1-09 | related 18+ แถวและข้อความยาว | บันทึกครบ ลำดับไม่สลับ PDF ยังครบ 2 หน้า/ตารางต่อเนื่องตาม FRD |
| P1-10 | ไม่เลือกหน่วยงาน / ไม่เลือกวิธีรับ | บล็อก VR-08/09 |
| P1-11 | Email: ว่าง, ผิด, หลายค่าคั่น comma/semicolon/space, มีช่องว่างหัวท้าย, ซ้ำกัน | ทุกค่าต้อง validate ตาม FN-01; ค่าที่ถูกส่งจริงไม่ควรมี duplicate/ช่องว่างผิดรูป |
| P1-12 | เลือก Email กรอกค่า แล้วเอาติ๊ก Email ออก | ค่า email ถูกล้างและไม่ติดไป PDF/API/notification |
| P1-13 | Paper only | ส่งได้โดยไม่ต้องมี email; notification ไม่ควรยิงไป email เก่าที่ซ่อน |
| P1-14 | เหตุผล reject/cancel เป็นช่องว่างล้วนหรือข้อความยาวมาก | ช่องว่างล้วนต้องถือว่าไม่กรอก; ข้อความที่รับต้องไม่ตัด/พัง audit โดยเงียบ |

### Phase C — State machine และการย้อน flow (P0/P1)

| ID | วิธีตรวจ | Expected |
|---|---|---|
| ST-01 | Step 3 Reject พร้อมเหตุผล | ทั้งใบกลับ Draft, เลขเดิม, เก็บเหตุผล/ผู้กระทำ/เวลา, ผู้อนุมัติเดิมไม่เห็น Draft |
| ST-02 | Maker แก้ข้อมูลหลัง Reject แล้วส่งใหม่ | resolve DOA ใหม่, เริ่ม Step 1, approval chain รอบเก่าอยู่ใน audit ไม่ปนกับรอบใหม่ |
| ST-03 | เปลี่ยน DOA หลังส่งแต่ก่อนอนุมัติ | ใบที่ Pending ใช้ snapshot เดิมทั้งหมด |
| ST-04 | เปลี่ยน DOA หลัง Reject ก่อนส่งใหม่ | รอบใหม่ต้อง resolve configuration ใหม่ |
| ST-05 | Owner Cancel ตอน Draft และตอน Pending | ต้องใส่เหตุผล; เป็น Cancelled; Pending step ถูก skipped; Pending case ส่ง `dar_cancelled` |
| ST-06 | Admin Cancel ใบคนอื่นตอน Pending | ทำได้ตาม FRD, actor/reason ถูก audit, แจ้ง current approver คนเดียวตาม spec |
| ST-07 | Cancel กับ Approve เกิดใกล้กันจาก 2 session | สำเร็จได้เพียง action เดียว; อีก action ได้ stale/conflict; ไม่มีสถานะผสม |
| ST-08 | Approver double-click/refresh/replay approve | ไม่เกิดการอนุมัติสองครั้งหรือข้ามขั้น; endpoint ต้อง idempotent ในผลธุรกิจ |
| ST-09 | Approved แล้วลอง Cancel/Edit/Reject ผ่านปุ่มและ direct request | ถูกปฏิเสธ, status/PDF/audit ไม่เปลี่ยน |
| ST-10 | Received แล้ว replay receive หรือ approve | ถูกปฏิเสธ; ไม่เกิด notification/audit ซ้ำ |

### Phase D — Permission และข้อมูลรั่ว (P0)

ทดสอบทั้งจากหน้าจอและ direct URL/API; การซ่อนปุ่มอย่างเดียวไม่ถือว่าผ่าน

| ID | Actor / Action | Expected |
|---|---|---|
| SEC-01 | Maker B ค้นหา/เปิด Draft ของ Maker A | ไม่เห็นใน list และ direct route/API ตอบเสมือน Not Found |
| SEC-02 | ผู้ใช้ไม่เกี่ยวข้องเปิดใบ Pending/Approved | ไม่เห็นและ 404 ตาม `canSee` |
| SEC-03 | Approver ในสายแต่ยังไม่ถึงขั้นเปิดใบ Pending | ดูได้ แต่ approve/reject ไม่ได้ |
| SEC-04 | Approver ขั้นปัจจุบันแก้ข้อมูล/ไฟล์/ยกเลิก | ทำไม่ได้ |
| SEC-05 | Maker อนุมัติใบตัวเองผ่าน direct request | 403 `NOT_CURRENT_APPROVER` หรือ `SELF_APPROVE`; สถานะไม่เปลี่ยน |
| SEC-06 | Admin ดูทุกสถานะ | เห็นได้ทั้งหมด แต่แก้ Draft ของคนอื่นไม่ได้ตาม matrix |
| SEC-07 | ผู้ไม่ใช่ Admin เรียก receive | 403 `NOT_ADMIN`; ไม่มี audit/notification |
| SEC-08 | สลับ company/tenant แล้วใช้ id หรือ DAR.No. เดิม | ห้ามเห็น ค้นหา ดาวน์โหลด PDF หรือ export ข้าม tenant |
| SEC-09 | ดาวน์โหลด attachment/PDF ด้วย URL เดิมหลัง logout/สลับ user | ต้องตรวจสิทธิ์ทุกครั้ง ไม่ใช่ public URL ถาวร |
| SEC-10 | CSV export ในแต่ละ role | มีเฉพาะรายการที่ role นั้นมองเห็น; filter ที่เลือกต้องมีผลกับ export ตาม behavior ที่ BA ยืนยัน |

### Phase E — เลขเอกสาร, consistency และ audit (P0/P1)

| ID | วิธีตรวจ | Expected |
|---|---|---|
| DATA-01 | สอง user บันทึกร่างพร้อมกัน | DAR.No. ไม่ซ้ำภายใต้ company; ไม่มีใบที่บันทึกสำเร็จแต่เลขว่าง |
| DATA-02 | Save ครั้งแรก fail/timeout แล้ว retry | ไม่สร้างใบซ้ำโดยไม่แจ้ง; เลขที่หายยอมรับได้ตาม no-gap แต่ต้อง trace ได้ |
| DATA-03 | ข้ามปี พ.ศ. หรือใช้ test clock/staging | format `DAR-ปีพ.ศ.-running` และ reset/carry running ตรง Document Config |
| DATA-04 | เปลี่ยนชื่อ/ฝ่าย/แผนก/โลโก้หลังออกเลข | ใบเดิมและ PDF ใช้ requester/header snapshot เดิมตาม FN-02 |
| DATA-05 | เปิดแก้ Draft สอง session | session เก่าบันทึกทีหลังได้ 409 STALE และไม่ทับข้อมูลใหม่ |
| DATA-06 | ทุก transition | `dar_audit` append-only มี action, actor, timestamp, note/reason ครบและเรียงถูก |
| DATA-07 | Reject → Resubmit หลายรอบ | ประวัติแต่ละ approval chain แยกชัด; ไม่มี signature เก่าปนใน PDF ปัจจุบัน |
| DATA-08 | ค้นหา/กรอง/paging | ผลรวม count, แถว, page และ tab สอดคล้องกัน; ไม่มีรายการหลุด/ซ้ำ |
| DATA-09 | CSV ภาษาไทยและค่าที่ขึ้นต้น `=`, `+`, `-`, `@` | UTF-8 BOM; เปิด Excel แล้วไทยไม่เพี้ยน; ค่าจากผู้ใช้ไม่กลายเป็น formula injection |

### Phase F — Integration / notification (P0/P1)

| ID | Trigger | ตรวจอะไรนอกจาก toast |
|---|---|---|
| INT-01 | Final approval | มี `approved_final` เพียงหนึ่งไฟล์, เปิดได้, checksum/version สัมพันธ์กับใบที่อนุมัติ |
| INT-02 | Final approval | `dar_distributed` ถึงหน่วยงานที่เลือกและ external email ที่ถูกต้องเท่านั้น; ไม่ส่งซ้ำเมื่อ refresh/retry |
| INT-03 | Cancel Pending | `dar_cancelled` ถึง current approver ณ ขณะยกเลิก ไม่ใช่ผู้อนุมัติทั้งสาย |
| INT-04 | Receive | `dar_received` ถึง owner + Document Controller ตาม event contract; ไม่มี recipient เกิน |
| INT-05 | Notification preference ปิด/เปิด | ตัว feature ส่ง event ให้ engine เสมอ; engine เป็นผู้ตัดสิน preference ตาม FN-09 |
| INT-06 | Notification service ล่ม/ช้า | ต้องตกลง expected กับ BA/Tech: transaction หลัก rollback หรือสำเร็จพร้อม retry; ห้ามเงียบจนไม่มี trace |
| INT-07 | Document Store ล้มตอน final approve | ห้ามเกิด Approved ที่ไม่มี final PDF โดยไม่มี recovery/audit; behavior ต้องชัดเจน |
| INT-08 | Approve ครบ | ยืนยันว่าไม่มี `dar.approved` ไปเปลี่ยนทะเบียนเอกสารตาม DEC-02 แต่ยังมี `dar_distributed` notification |

### Phase G — Attachment และ input abuse (P1)

| ID | กรณี | Expected |
|---|---|---|
| FILE-01 | ไฟล์ที่อนุญาต, 0 byte, ใหญ่เกิน, `.exe`, double extension, MIME ไม่ตรงนามสกุล | ใช้ file policy กลาง; error 413/415 ตาม API; ไม่เก็บไฟล์ต้องห้าม |
| FILE-02 | PDF/ZIP ที่มี password/key | ปฏิเสธตาม DB §4.5 |
| FILE-03 | ชื่อไฟล์ภาษาไทย/ยาว/มีอักขระพิเศษ/ชื่อซ้ำ | เก็บและดาวน์โหลดได้อย่างปลอดภัย ไม่ทับไฟล์เดิม |
| FILE-04 | Reject กลับ Draft แล้วเพิ่ม/ลบ attachment | owner ทำได้; approver ทำไม่ได้; audit/visibility ถูกต้อง |
| FILE-05 | Cancel/Approved/Received แล้วลองเพิ่มหรือลบไฟล์ผ่าน direct API | ปฏิเสธและไม่แก้ข้อมูล |
| INPUT-01 | ใส่ `<script>`, HTML, quote, newline ในชื่อเอกสาร/เหตุผล/หมายเหตุ | แสดงเป็นข้อความ ไม่ execute ทั้งหน้า detail, audit, PDF, CSV และ notification |

## 5. เคสสำคัญที่ชุด UAT เดิมตัดออก — รอบนี้ควรนำกลับมาตรวจ

จาก `QA_AUDIT` มี 11 เคสที่ไม่ได้อยู่ใน UAT คน ได้แก่ DOA dynamic, PDF ตาม 6 ขั้น, API 500, stale, doc type inactive, notification จริง, direct route และการไม่ส่งต่อระบบอื่น รอบ review production ควรตรวจอย่างน้อย:

- DOA 5/6 ขั้นและ PDF signature layout/data
- stale/concurrent update และ approve/cancel race
- direct URL/API permission
- notification recipient, duplicate และ delivery log
- approved PDF ใน Document Store
- doc type inactive เฉพาะ environment ที่ปลอดภัย
- ยืนยันว่าไม่มี downstream registration event ตาม DEC-02

## 6. วิธีตัดสินผล

| ระดับ | เกณฑ์ตัวอย่าง | การตัดสินรอบ review |
|---|---|---|
| Critical | ข้ามสิทธิ์/ข้ามขั้นอนุมัติ, ข้อมูลข้าม tenant, ข้อมูลหาย, เลขซ้ำ, script execution | ไม่ผ่านและหยุด rollout/จำกัดการใช้งานทันที |
| High | สถานะผิด, คนผิดได้รับ notification/PDF, final PDF หาย, cancel/approve race ทำให้ผลสองทาง | ไม่ผ่านหรือผ่านแบบมีเงื่อนไขตาม risk acceptance ที่ลงชื่อ |
| Medium | validation/audit/history ผิดแต่มีทางเลี่ยงและไม่ทำข้อมูลเสีย | เปิด defect และกำหนด retest |
| Low | ข้อความ/ตำแหน่ง/ความเรียบร้อยที่ไม่กระทบ flow | เก็บ backlog เพราะ UI layout อยู่นอก focus รอบนี้ |
| Spec Gap | ระบบตรง FRD แต่ business ไม่ยอมรับ หรือ FRD/OQ ไม่ชัด | ส่ง PM/BA ตัดสิน; ห้ามฟันธงเป็น bug จนได้คำตอบ |

เงื่อนไขขั้นต่ำก่อนสรุป “ผ่าน”: P0 ทุกข้อผ่าน, ไม่มี Critical/High ค้าง, P1 ที่ไม่ได้ตรวจต้องระบุเป็น `Not Tested` พร้อมเหตุผล และ BQ-01..09 ต้องมี owner รับทราบ

## 7. รูปแบบบันทึกผลต่อเคส

```text
Case ID:
Environment / build:
วันที่-เวลา:
User / role / company:
DAR.No.:
ข้อมูลตั้งต้น:
Steps:
Expected (FRD ref):
Actual:
Result: PASS / FAIL / NOT TESTED / SPEC GAP
Severity:
Evidence: screenshot/video/request-id/notification-id/file
หมายเหตุ / ผู้รับผิดชอบ:
```

## 8. แผนทำงานแบบใช้เวลาคุ้ม

- รอบ 1 (ประมาณ 2–3 ชม.): P0-01..06, ST-01/05/07/08, SEC-01..08, DATA-01/05, INT-01/02/08
- รอบ 2 (ประมาณครึ่งวัน): Validation ทั้งชุด, Reject/Resubmit, PDF/CSV, attachment, audit และ notification ทุก event
- รอบ 3 (ต้องมี admin/technical support): DOA dynamic, doc type inactive, service failure, concurrency, tenant isolation และตรวจ log/storage/event
- ปิดงาน: สรุปเฉพาะผลที่มีหลักฐาน; รายการที่ทำไม่ได้ให้เป็น `Not Tested` ไม่ถือว่าผ่าน

