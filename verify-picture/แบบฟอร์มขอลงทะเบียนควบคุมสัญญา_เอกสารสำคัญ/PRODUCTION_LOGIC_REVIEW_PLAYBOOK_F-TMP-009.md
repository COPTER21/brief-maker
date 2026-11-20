# Production Logic Review Playbook — F-TMP-009

ฟีเจอร์: แบบฟอร์มขอลงทะเบียนควบคุมสัญญา/เอกสารสำคัญ  
วัตถุประสงค์: ตรวจเก็บตกหลังขึ้น Production โดยเน้น business logic, state, permission, data integrity และ integration ไม่ใช่ตรวจ layout ซ้ำ  
แหล่งตัดสินหลัก: FRD `00_OVERVIEW` ถึง `07_LOCKED_DECISIONS` และ declaration ที่ FRD อ้าง  
วันที่จัดทำ: 20 พฤศจิกายน 2569

## 1. วิธีใช้เอกสารนี้

- สิ่งที่ FRD ระบุชัด: ใช้ตัดสิน Pass/Fail ได้
- สิ่งที่อยู่ในหัวข้อ “Business-risk probe”: ควรลองเพื่อหา defect แต่ถ้า FRD ไม่กำหนดผลชัด ให้บันทึกเป็น Observation/OQ ก่อน ไม่ฟันธงเป็น Bug
- สิ่งที่เป็น `AI-DEFAULT`, OQ หรือข้อความขัดกัน: ให้ BA/PM ยืนยันก่อนใช้เป็นเกณฑ์รับรอง
- Existing TC 41 เคสใน `_tc/TC_...md` เขียนสำหรับ prototype มี seed, `__QA__`, เลขเอกสาร และวันที่จำลอง ห้ามคัดลอก expected value เหล่านั้นไปใช้กับ Production ตรง ๆ ให้ใช้เฉพาะเจตนาของเคส
- ทุกเคสต้องเก็บ: ผู้ใช้/role, เลขเอกสาร, เวลา, input, expected ตาม FRD, actual, screenshot/clip และ request/response หรือ log เมื่อมีสิทธิ์เข้าถึง

## 2. ข้อสรุปจากการอ่านแพ็กก่อนเริ่มทดสอบ

### 2.1 จุดที่เสี่ยงที่สุด

1. สายอนุมัติเป็น dynamic DOA และต้อง freeze ตอนส่ง ไม่ใช่ hardcode 2 ขั้น
2. สิทธิ์ต้องบังคับที่ server; การ “ไม่มีปุ่ม” อย่างเดียวไม่พอ
3. เลขคำขอ CTR ออกตั้งแต่บันทึกครั้งแรกและเลขเดิมต้องอยู่ต่อเมื่อส่งกลับ
4. ทะเบียนควบคุมออกเฉพาะตอนผู้ดูแลลงทะเบียน และห้ามซ้ำแม้กดซ้ำ/เปิดสองหน้าต่าง
5. ผู้พิจารณาต้องตัดสินตามลำดับ และผู้ขอห้ามอนุมัติใบตนเอง
6. การเปลี่ยน DOA/ผังองค์กร/ข้อมูลพนักงานภายหลังต้องไม่เปลี่ยน snapshot ของเอกสารที่ส่งแล้ว
7. PDF approved_final ต้องตรงข้อมูลและสายอนุมัติ ณ เวลาที่อนุมัติครบ และไม่เปลี่ยนย้อนหลัง
8. การส่งกลับต้องกลับเป็นร่าง เลขเดิม ล้างสาย active แล้ว resolve ใหม่เมื่อส่งซ้ำ แต่ประวัติเก่าต้องยังอยู่
9. การแจ้งเตือนต้องถูก event, ผู้รับ และจำนวนครั้ง; DOA event ห้ามยิงซ้ำจาก feature
10. Draft และเอกสารของคนอื่นต้องไม่รั่วทั้ง list, direct URL, API, CSV และ attachment

### 2.2 จุดที่ต้องให้ BA/PM ยืนยันก่อนใช้เป็นเกณฑ์

| ประเด็น | หลักฐานในแพ็ก | วิธีปฏิบัติระหว่าง review |
|---|---|---|
| มติ 11 ข้อยังเป็น `AI-DEFAULT` | FRD 07 §7.0 และ TC ระบุรอลูกค้าเซ็น OQ-02 | ถ้า Production ใช้ไม่ตรง อย่ารีบเปิด bug; ขอใบยืนยันมติล่าสุดก่อน |
| DOA declaration ระบุ `wire_status: pending` และค่าเริ่ม 2 ขั้นยังรอยืนยัน | `DOA_BRIEF` §1, §3, §6, §8 | ตรวจ config จริงใน Production ว่า wired แล้วและผู้รับผิดชอบธุรกิจยืนยันสายแล้ว |
| MDOC ระบุ DOA pending และ taxonomy ยังไม่อนุมัติ | `MDOC_BRIEF` ผลตรวจ G04/G09 | ตรวจว่าเป็นข้อมูลเก่าหรือ Production ยังมี config debt |
| รูปแบบเลขทะเบียนควบคุมยังเป็น OQ-06 | FRD 00 §0.4 และ FN-08 | ตรวจ uniqueness/การออกเลขได้ แต่ห้ามยึด `CR-2569-xxxx` เป็นรูปแบบที่ถูกจน BA ยืนยัน |
| “ทำซ้ำ” ขัดกัน | FRD 00 Scope เขียนว่ามี “ทำซ้ำ (DEC-11)” แต่ FRD 07 DEC-11 และ TC-K01 ระบุไม่มีปุ่มทำซ้ำ | เปิดเป็น Spec Conflict/OQ ไม่ใช่ product bug จน BA ตัดสิน |
| DEC-02 เขียนว่า event ประกาศไว้แต่ “ไม่ยิง” แต่ FN-10/NTF/AC-08 กำหนดให้ยิง event | FRD 07 DEC-02 เทียบ FRD 03 FN-10 และ NTF_BRIEF | แยก “ไม่ส่งต่อระบบธุรกิจอื่น” ออกจาก notification; ให้ BA/SA ยืนยันข้อความ DEC-02 |
| เอกสารสำคัญอื่น ๆ ไม่มีช่องชื่อเอกสาร | EC-07 / OQ-05 | การไม่มีช่องไม่ใช่ bug ตาม FRD ปัจจุบัน; ทดสอบว่าระบุผ่านชื่อไฟล์/ไฟล์แนบได้จริง |
| อ้างทะเบียนเดิมไม่มีช่อง | EC-08 / OQ-04 | ไม่ใช่ bug ตาม FRD ปัจจุบัน; บันทึก pain point หากค้นทะเบียนเดิมใช้งานจริงลำบาก |

## 3. สิ่งที่ต้องเตรียม

### 3.1 บัญชีทดสอบขั้นต่ำ

| บัญชี | Role/เงื่อนไข |
|---|---|
| Maker A | ผู้ขอ หน่วยงาน A มี line manager |
| Maker B | ผู้ขอคนอื่น สำหรับทดสอบ isolation |
| Approver 1 | ผู้พิจารณาขั้น 1 ของ Maker A |
| Approver 2 | role-compliance หรือผู้พิจารณาขั้น 2 |
| Custodian | ผู้ดูแลสัญญา แต่ไม่อยู่ใน chain ของเคสหนึ่ง |
| Outsider | ไม่ใช่เจ้าของ ไม่อยู่ใน chain ไม่ใช่ผู้ดูแล |
| Self-role user | ถ้าจัดได้: ผู้ขอที่ resolve แล้วมีชื่อตนเองเป็นผู้ถือ role เพื่อทดสอบ self-approval |

อย่าใช้บัญชีเดียวสลับ role แบบ prototype เพราะจะพิสูจน์ permission isolation ไม่ได้จริง

### 3.2 ข้อมูลทดสอบ

- ชุดปกติ: สัญญาว่าจ้าง, จัดทำใหม่, วันเริ่มวันนี้หรืออนาคต, วันสิ้นสุดหลังวันเริ่ม
- ชุด amend: แก้ไข/เปลี่ยนแปลง + เหตุผล
- ชุดหมดอายุ: วันสิ้นสุดก่อนวันนี้ แต่ยัง `end >= start`
- ชุด boundary: ชื่อคู่สัญญา 300 ตัวอักษร, 301 ตัวอักษร, เหตุผล 1,000 และ 1,001 ตัวอักษร
- ชุดไฟล์: PDF เล็ก, หลายไฟล์, ไฟล์พอดี 20MB, เกิน 20MB, ชนิดที่อนุญาต และชนิดที่ควรถูก 415
- ข้อความไทย/อังกฤษ, comma, quote, newline และตัวขึ้นต้น `=`, `+`, `-`, `@` สำหรับ CSV safety probe

### 3.3 หลักฐานที่ต้องเปิดดูได้

- หน้ารายการ/รายละเอียด/ประวัติ/PDF
- Notification ของผู้รับจริง
- Network response หรือ API client สำหรับ deny cases
- ถ้าเข้าถึงได้: audit log, Document Store approved_final, DOA resolve snapshot และเลข sequence

## 4. ลำดับรันที่แนะนำ

ให้สร้างข้อมูลใหม่ต่อ flow อย่าใช้ใบ Production ของผู้ใช้จริง และอย่าทำ approve/cancel/register กับเอกสารจริง

### Run A — Golden path แบบครบวงจร (P0)

| # | ผู้ทำ | การทดสอบ | Expected ตาม FRD | Trace |
|---:|---|---|---|---|
| A01 | Maker A | เปิดรายการ | เห็นเฉพาะใบของตนและใบที่ตนอยู่ใน chain; draft คนอื่นไม่ปรากฏ | BR-11, FN-11 |
| A02 | Maker A | สร้างคำขอใหม่ | owner unit default จากหน่วยงานผู้ขอ; ช่องบังคับครบ; ประเภท 8 ค่าและ purpose 5 ค่า | BR-01, BR-04, VR-01..06 |
| A03 | Maker A | กดไปต่อทั้งที่ว่าง | ไปต่อไม่ได้และแต่ละช่องมี error ที่ตรวจสอบได้ | AC-02 |
| A04 | Maker A | เลือก amend กรอกเหตุผล แล้วเปลี่ยน purpose เป็นค่าอื่น | ช่องเหตุผลหายและค่าต้องถูกล้าง ไม่หลงไป DB/PDF/CSV | BR-02, FN-01 |
| A05 | Maker A | ใส่ end ก่อน start และลอง bypass ด้วย request | UI เลือกไม่ได้; server ตอบ validation เมื่อ bypass | BR-03, VR-05, API-03 |
| A06 | Maker A | บันทึกร่างครั้งแรก | ได้เลข CTR จาก engine, status=draft, snapshot ผู้ขอ/หน่วยงาน/หัวเอกสารครบ | FN-02, FN-03, BR-08 |
| A07 | Maker A | reload และแก้ร่าง | ข้อมูลไม่หาย; เลขเดิม; version เปลี่ยน; audit มีผู้แก้/เวลา | API-04, DB audit |
| A08 | Maker A | แนบหลายไฟล์ | ไฟล์เปิด/ดาวน์โหลดได้เฉพาะผู้มีสิทธิ์; ชื่อ/ขนาด/ชนิดตรง | API-13 |
| A09 | Maker A | ส่งพิจารณา | จำนวน slot ตรง DOA resolve จริง; ผู้ขอไม่อยู่ในตัวเลือก; assignee ครบ; chain ถูก freeze | FN-04, BR-05, BR-14, VR-07 |
| A10 | Approver 2 | ลองตัดสินก่อนขั้น 1 ทั้งผ่าน UI และ API | ไม่มี action; API ปฏิเสธ `NOT_CURRENT_APPROVER`; state ไม่เปลี่ยน | BR-15, TC-D03 |
| A11 | Approver 1 | อนุมัติขั้น 1 | ขั้น 1 approved; ขั้น 2 pending; status ยัง pending; note/audit ถูกคนถูกเวลา | FN-05 |
| A12 | Approver 2 | รับทราบขั้นสุดท้าย | ใช้คำตาม role; status=approved/รอลงทะเบียน; สร้างและเก็บ PDF approved_final | BR-06, FN-05, FN-09 |
| A13 | Maker A | ลองแก้/ลงทะเบียนใบ approved | ไม่มีปุ่มและ server ปฏิเสธ; ข้อมูลไม่เปลี่ยน | State machine, TC-D04/D06 |
| A14 | Custodian | ลงทะเบียนควบคุม | ทำได้เฉพาะ approved; เลขทะเบียนไม่ซ้ำ; status=registered; ผู้ขอได้ `ctr_registered` ครั้งเดียว | BR-09, FN-08, FN-10 |
| A15 | Custodian | บันทึกรับต้นฉบับโดยเว้นวัน/ใส่อนาคต/ใส่วันนี้ | ว่างและอนาคตถูกบล็อก; วันที่ถูกต้องทำให้ status=completed; ผู้ขอได้ `ctr_original_received` | BR-10, VR-09, FN-10 |
| A16 | ทุก role ที่ควรเห็น | ตรวจ PDF/ประวัติ/CSV หลังจบ | ค่า business, ผู้ตัดสิน, เลขทะเบียน, วันที่รับ และสถานะตรงกันทุกช่องทาง | AC-10, AC-12 |

### Run B — ส่งกลับ แก้ และส่งใหม่ (P0)

| # | ผู้ทำ | การทดสอบ | Expected ตาม FRD | Trace |
|---:|---|---|---|---|
| B01 | Approver 1 | reject โดยไม่ใส่เหตุผล | บันทึกไม่ได้; เหตุผลบังคับ | VR-08 |
| B02 | Approver 1 | reject พร้อมเหตุผล | status กลับ draft, เลข CTR เดิม, ผู้พิจารณามองไม่เห็น draft แล้ว, owner เห็นแถบเหตุผล | FN-06, BR-07 |
| B03 | Maker A | ตรวจ history | chain เก่าถูกเก็บใน audit; คน/เวลา/เหตุผลครบ; ไม่มี record เดิมถูกแก้ทับ/หาย | FN-06, audit append-only |
| B04 | Maker A | แก้ข้อมูลแล้วส่งใหม่ | resolve DOA ใหม่, ล้าง returned fields จาก active view, เลขเดิม, history รอบแรกยังอยู่ | FN-04, FN-06 |
| B05 | ทีมระบบ | เปลี่ยน DOA หลังรอบแรกก่อนส่งใหม่ ถ้าทำได้อย่างปลอดภัย | รอบใหม่ใช้ chain ใหม่; รอบเก่ายังคง snapshot เดิม | BR-05, EC-04 |
| B06 | Approver 2 | ส่งกลับจาก role-compliance | ปุ่ม/คำตัดสินเป็น “ส่งกลับแก้ไข”; กลับ draft เลขเดิม | BR-06, BR-07 |

### Run C — ยกเลิกและ state transition (P0/P1)

| # | การทดสอบ | Expected |
|---:|---|---|
| C01 | owner ยกเลิก draft โดยไม่ใส่เหตุผล แล้วใส่เหตุผล | ครั้งแรกถูกบล็อก; ครั้งหลัง status=cancelled |
| C02 | owner ยกเลิก pending | cancelled; current pending step ถูก skipped; current approver ได้ `ctr_cancelled` |
| C03 | Custodian ยกเลิก draft/pending ของผู้อื่น | ทำได้ตาม permission matrix และต้องมีเหตุผล |
| C04 | owner/Custodian ลองยกเลิก approved, registered, completed | ปฏิเสธ `INVALID_STATE`; state และข้อมูลคงเดิม |
| C05 | ผู้พิจารณาที่ไม่ใช่ owner/Custodian ลองยกเลิก | server ปฏิเสธ; ไม่มีผลข้างเคียง |

Trace: FN-07, FN-10, BR-07, AC-11, state machine

### Run D — Permission และ data isolation (P0)

ทดสอบทั้ง UI, direct URL, API, CSV และ attachment URL; “เมนูไม่ขึ้น” ยังไม่ถือว่าผ่าน server authorization

| # | ผู้ทำ/เป้าหมาย | Expected |
|---:|---|---|
| D01 | Approver เปิด draft ของ Maker A | ไม่อยู่ใน list; GET detail เป็น 404 ไม่เปิดเผยว่ามีใบ |
| D02 | Maker B/Outsider เปิดใบ Maker A | ไม่อยู่ใน list; direct URL/API เป็น 404 |
| D03 | ผู้ไม่ใช่ owner PUT draft | 403 `NOT_OWNER`; ค่า/version/audit ไม่เปลี่ยน |
| D04 | owner PUT ใบที่ส่งแล้ว | 409 `NOT_DRAFT`; ค่า/version/audit ไม่เปลี่ยน |
| D05 | คนที่ไม่ใช่ current approver approve/reject | 403; state ไม่เปลี่ยน |
| D06 | owner/approver register หรือ receive | 403 `NOT_CUSTODIAN` |
| D07 | requester ถูกเลือกเป็น approver ด้วย crafted request | 422 `SELF_APPROVAL` |
| D08 | ผู้ที่ไม่มีสิทธิ์ดาวน์โหลด attachment/PDF | 404/deny และไม่เห็น metadata ที่รั่วข้อมูล |
| D09 | CSV ของแต่ละ role | มีเฉพาะรายการที่ role นั้นมองเห็น และใช้ filter เดียวกับหน้าจอ |
| D10 | ถ้ามีหลาย tenant/company | ID จาก tenant อื่นต้อง 404; เลข sequence/snapshot ไม่ข้าม tenant |

Trace: FRD 02 API errors, BR-11, §5.3, §6.2, FN-11

### Run E — เลขเอกสาร ความซ้ำ และ concurrency (P0 business-risk probe)

| # | วิธีลอง | ผลที่ปลอดภัยทางธุรกิจ |
|---:|---|---|
| E01 | double-click บันทึกร่าง/กด Enter ซ้ำ/รีเฟรชหลัง timeout | ไม่ควรสร้าง 2 ใบโดยผู้ใช้ไม่ตั้งใจ; ถ้าสร้างจริงให้เก็บ request id/เวลาเป็น High risk observation |
| E02 | สองผู้ใช้สร้างพร้อมกัน | doc_no ไม่ซ้ำและไม่ใช้การ +1 เอง |
| E03 | เปิดใบเดียวกันสองแท็บ แก้ทั้งคู่แล้วบันทึก | แท็บหลังต้องได้ 409 STALE และไม่ทับข้อมูลแท็บแรก |
| E04 | Approver เปิดสองแท็บแล้ว approve/reject แข่งกัน | มีผลลัพธ์เดียว; state/audit/notification ไม่ซ้ำ |
| E05 | Custodian สองคนกด register พร้อมกัน | register_no เดียว ไม่ซ้ำ ไม่ข้ามเลขจาก race; event ไม่ซ้ำ |
| E06 | กด receive ซ้ำหรือยิง request ซ้ำ | วันที่/actor/audit/event ไม่เกิดซ้ำอย่างเสียหาย |

FRD ระบุ optimistic lock และ unique/tenant แต่ไม่ได้เขียน idempotency contract ครบ จึงให้แยก defect ที่ทำข้อมูลเสีย/เลขซ้ำออกจากข้อเสนอเรื่อง UX ป้องกันกดซ้ำ

### Run F — Snapshot, audit และ PDF immutability (P0/P1)

| # | การทดสอบ | Expected |
|---:|---|---|
| F01 | หลังบันทึกร่าง เปลี่ยนชื่อ/ตำแหน่ง/หน่วยงานของ requester ใน master | เอกสารเดิมยังแสดง snapshot ตามจังหวะที่ FRD กำหนด ไม่เปลี่ยนย้อนหลัง |
| F02 | หลังส่ง เปลี่ยน DOA/ผู้ถือ role/หัวหน้า | ใบ pending ใช้ approval_chain snapshot เดิม |
| F03 | หลังออกเลข เปลี่ยนชื่อบริษัท/โลโก้ | header ของเอกสารเดิมคง snapshot เดิม |
| F04 | หลัง approved_final เปลี่ยน master/DOA แล้วเปิด PDF ใหม่ | approved_final เดิมต้องเหมือนเดิม ไม่ถูก render ด้วย master ล่าสุด |
| F05 | ตรวจ history ตั้งแต่ create, edit, submit, approve, reject/resubmit, register, receive/cancel | append-only; actor/time/action/note ถูกต้อง; ไม่มีรายการหายหรือถูกแก้ทับ |
| F06 | DOA 1, 2 และมากกว่า 4 ขั้น ถ้าจัด config test ได้ | ช่องลงชื่อ = requester + 1/step; แถวละไม่เกิน 4; >4 dense; ยัง 1 หน้า |
| F07 | ข้อความยาวสุดและชื่อไทย/อังกฤษ | PDF ไม่ตัดสาระ ไม่ทับช่อง ไม่หลุดหน้า; HTML render กับ server PDF มีข้อมูลเท่ากัน |

Trace: FN-02, FN-04, FN-05, FN-09, BR-05, BR-12, EC-03/04, DB audit

### Run G — Validation และไฟล์แนบ (P1)

| # | การทดสอบ | Expected/การจำแนก |
|---:|---|---|
| G01 | contract_type/purpose ส่งค่าที่ไม่อยู่ใน enum ผ่าน API | 422; ไม่บันทึกบางส่วน |
| G02 | counterparty 300/301 ตัวอักษร | 300 ผ่าน; 301 ถูก reject ตาม VR-04 |
| G03 | change_reason 1,000/1,001 ตัวอักษร | ตรวจตาม DB contract; หาก UI รับแต่ DB ตัด/500 = defect |
| G04 | owner_unit ว่าง/ID ไม่มีจริง/อยู่นอกสิทธิ์ | ว่างต้อง reject; ID และ scope ที่ FRD ไม่ชัดให้บันทึก OQ หากเสี่ยงเลือกหน่วยงานผิด |
| G05 | end=start | ผ่าน เพราะกฎคือ `end >= start` |
| G06 | สัญญาหมดอายุแล้ว | เตือนแต่ไม่บล็อก และบันทึกได้ |
| G07 | received_date รอบเที่ยงคืน/พรุ่งนี้ตาม timezone กรุงเทพ | อนาคตต้อง reject; วันนี้ต้องผ่าน ไม่มี off-by-one |
| G08 | ไฟล์ 20MB และเกิน 20MB | ตาม UI/API ต้องบังคับ limit; ระบุให้ชัดว่าระบบตีความต่อไฟล์หรือรวมทั้งหมด |
| G09 | unsupported file type | API 415 และไม่มีไฟล์ตกค้าง |
| G10 | upload หลายไฟล์แล้ว request หลัก fail/cancel | ไม่มี orphan ที่คนอื่นเข้าถึงได้; retention ที่ FRD ไม่กำหนดให้บันทึก observation |

### Run H — List, filter, CSV และ notification (P1)

| # | การทดสอบ | Expected |
|---:|---|---|
| H01 | ค้นด้วย doc_no, ผู้ขอ, คู่สัญญา, register_no | ผลตรงคำค้นและ permission |
| H02 | ผสม status/type/unit/search + เปลี่ยนหน้า/page size | filter ไม่หลุด; count/pagination ตรงจำนวนจริง |
| H03 | CSV หลังตั้ง filter | row set ตรง list ที่ role นั้นเห็น; field/encoding ไทยเปิดได้; ไม่รั่วข้อมูล |
| H04 | CSV มี comma/quote/newline | escaping ถูก ไม่แตกคอลัมน์ |
| H05 | CSV ค่าเริ่ม `=`, `+`, `-`, `@` | Business-risk probe: ไม่ควรถูก spreadsheet ตีความเป็นสูตรอันตราย |
| H06 | register สำเร็จ | requester ได้ `ctr_registered` in-app+email ตาม config บังคับ เพียงครั้งเดียว |
| H07 | receive สำเร็จ | requester ได้ `ctr_original_received` ตาม preference/channel config |
| H08 | cancel จาก pending | current approver ได้ `ctr_cancelled`; cancel จาก draft ไม่ต้องยิง event นี้ |
| H09 | approve แต่ละขั้น | DOA engine เป็นเจ้าของ doa_pending/doa_result; feature ต้องไม่ยิงซ้ำ |

## 5. ชุดขั้นต่ำถ้าเวลาน้อย

หากมีเวลาเพียงรอบเดียว ให้ทำตามลำดับนี้:

1. Run A ทั้งชุด — พิสูจน์ lifecycle จริงจาก draft ถึง completed
2. Run B01–B04 — พิสูจน์ reject/resubmit และเลขเดิม
3. Run D01–D09 — พิสูจน์สิทธิ์ที่ server ไม่ใช่แค่ UI
4. E03–E05 — พิสูจน์ stale และเลขทะเบียนไม่ซ้ำ
5. F02, F04, F05 — พิสูจน์ snapshot, PDF และ audit
6. G01, G05, G06, G07, G08, G09 — validation ที่มีผลธุรกิจ
7. H03, H06–H09 — CSV/notification ไม่รั่วและไม่ซ้ำ

อย่าตัด permission, concurrency และ snapshot ออก เพราะ tester ปกติมักผ่าน happy path/UI แล้ว แต่ defect ร้ายแรงมักอยู่สามกลุ่มนี้

## 6. วิธีตัดสินผล

### Bug

- Critical: ข้ามสิทธิ์/ข้ามลำดับอนุมัติ, ข้อมูลคนอื่นรั่ว, ข้อมูลเสีย/หาย, approved PDF เปลี่ยนย้อนหลัง
- High: สถานะผิด, เลขซ้ำ, ลงทะเบียนหรือรับต้นฉบับผิด state, notification ส่งผิดคน, CSV รั่วข้อมูล
- Medium: ผิด FRD แต่มีทางเลี่ยง, audit/history ไม่ครบ, validation บาง boundary ไม่ตรง
- Low: ข้อความ/หน้าตา ซึ่งไม่ใช่เป้าหมายหลักรอบนี้

### Spec conflict / OQ

ใช้เมื่อ implementation เลือกหนึ่งในหลายความหมายที่ FRD ขัดกันหรือยังเป็น OQ เช่น ปุ่มทำซ้ำ, รูปแบบทะเบียน, สาย DOA ที่ยังไม่เซ็นยืนยัน ห้ามนับเป็น product fail จน BA/PM ตอบ

### Suggestion

ใช้เมื่อระบบทำตาม FRD แต่มี business risk หรือ UX ที่ควรปรับ เช่น กัน double-click, CSV formula safety หรือการค้นทะเบียนเดิม

## 7. แบบบันทึกผลต่อเคส

| ช่อง | ต้องกรอก |
|---|---|
| Case/Trace | เช่น D05 · BR-15 · API-06 |
| เวลา/Environment | Production build/version + เวลา Asia/Bangkok |
| Actor | ชื่อบัญชีและ role จริง |
| Test data | doc_no/register_no และข้อมูลสำคัญ |
| Steps | ขั้นที่ทำจริง สั้นและทำซ้ำได้ |
| Expected | ข้อความ/สถานะ/ค่าตาม FRD |
| Actual | สิ่งที่เห็นจริง ห้ามเขียนแค่ “ไม่ผ่าน” |
| Evidence | screenshot/clip/request-response/log |
| Result | Pass / Fail / Blocked / Observation / Spec conflict |
| Severity | Critical/High/Medium/Low เฉพาะ Bug |

## 8. Exit criteria ของ full review

- AC 14/14 มีผลจริง ไม่ใช่อ้างผล prototype
- BR 15/15 และ VR 9/9 มีหลักฐาน หรือระบุ Blocked พร้อมเหตุผล
- Deny cases 7/7 พิสูจน์ server-side อย่างน้อยหนึ่งวิธี
- Lifecycle หลัก, reject/resubmit, cancel, register, receive ผ่านด้วยบัญชีจริงหลาย role
- ไม่พบ Critical/High ค้าง
- Spec conflict/OQ ทุกข้อมี owner และคำตอบหรือ acceptance เป็นลายลักษณ์อักษร
- รายการที่ไม่ได้ตรวจระบุชัด ห้ามสรุปครอบคลุมเกินหลักฐาน

เมื่อรันจริงเสร็จ ให้นำผลและหลักฐานมาสร้าง Feature Check Report รอบ 1; ข้อที่ไม่ได้รันต้องเป็น `ไม่ได้ตรวจ` ไม่ใช่ Pass
