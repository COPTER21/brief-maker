# Full Logic Review Plan — F-TMP-009

## 1. จุดประสงค์และหลักตัดสิน

เอกสารนี้เป็นแผนตรวจระบบจริงสำหรับ **แบบฟอร์มชุดเอกสารนำส่งและหลักฐานการนำส่ง (FM-IVM-07)** หลังขึ้น Production แล้ว โดยเน้น Logic, Workflow, Permission, Data Integrity, Integration และผลลัพธ์ทางธุรกิจ ไม่ใช่การตรวจ layout ซ้ำ

หลักตัดสินเรียงตามลำดับ:

1. FRD Pack โดยเฉพาะ `03_LOGIC`, `05_RULES`, `06_TESTS`, `07_LOCKED_DECISIONS`
2. Governance declarations: DOA, DOCCFG, NTF
3. พฤติกรรมจริงและหลักฐานจาก Production
4. Business-sense exploratory checks ในเอกสารนี้ใช้ค้นหาความเสี่ยง แต่ถ้า FRD ไม่ระบุ ห้ามฟันธงเป็น Bug จน PM/BA ยืนยัน

ข้อควรระวัง: DevPack ระบุว่ามีมติ `AI-DEFAULT` 12 ข้อ, เดิมเป็น `NO-BROWSER` และไม่มีรายงาน `e2e_standard` จึงต้องแยกให้ชัดระหว่าง “ผิด FRD” กับ “FRD/มติเดิมอาจไม่ตอบโจทย์ธุรกิจ”

## 2. สิ่งที่ต้องเตรียมก่อนตรวจ

- บัญชีแยกอย่างน้อย 6 ตัวตน: owner A, owner B, ผู้ตรวจสอบขั้น 1, ผู้อนุมัติขั้น 2, ผู้ที่อยู่ในสายแต่ยังไม่ถึงขั้น, admin ฝ่ายบริหารการลงทุน
- ถ้าทำได้ เพิ่มผู้ใช้นอกสายและ tenant/company อื่นสำหรับทดสอบการไม่เห็นข้อมูล
- สิทธิ์ดู audit log, notification log, document store และรายการตั้งค่า DOA/DOCCFG หรือมีผู้ดูแลช่วยตรวจหลักฐานหลังบ้าน
- ไฟล์ทดสอบ: PDF, DOCX, XLSX, JPG/PNG, EML/MSG, ไฟล์เกิน 20 MB และชนิดต้องห้าม
- ชุดข้อมูลที่ไม่ใช่ข้อมูลลูกค้าจริง และข้อความเฉพาะตัวเพื่อค้นใน CSV/PDF/log ได้
- บันทึก build/version, วันเวลา, timezone, ผู้ทดสอบ และเลขเอกสารทุกใบที่สร้าง

ห้ามทดสอบ destructive case กับเอกสารธุรกิจจริง ให้สร้างใบเฉพาะสำหรับ review และตกลงกับผู้ดูแลก่อนทดสอบ notification หรือการตั้งค่า DOA/DOCCFG บน Production

## 3. วิธีเก็บผล

แต่ละเคสให้บันทึก `PASS / FAIL / BLOCKED / NOT RUN` พร้อม:

- เลขเอกสารและ actor ที่ใช้
- ขั้นตอนย่อที่ทำซ้ำได้
- Expected ตาม FRD ID
- Actual ที่เห็นจริง
- Screenshot/clip และเวลาเกิดเหตุ
- ถ้าเกี่ยวกับ integration ให้แนบ event ID, audit entry, notification หรือ stored document reference

ระดับปัญหาแนะนำ:

- Critical: ข้าม tenant/สิทธิ์/สายอนุมัติ, ข้อมูลหาย, ปิดงานหรืออนุมัติโดยคนไม่มีสิทธิ์
- High: สถานะ, เลขเอกสาร, PDF, หลักฐาน, notification หรือผลทางธุรกิจผิด
- Medium: ผิด FRD แต่มีทางเลี่ยง, audit/history ไม่ครบ, validation ไม่สม่ำเสมอ
- Low: ข้อความ/การแสดงผลที่ไม่ทำให้ผลธุรกิจผิด
- Question/Improvement: FRD ไม่ชัดหรือระบบทำตาม FRD แต่เสี่ยงเชิงธุรกิจ

## 4. ชุด P0 — ต้องผ่านก่อนจึงถือว่า workflow ใช้ได้

### P0-01 สร้างจนปิดการนำส่งครบหนึ่งเส้นทาง

1. Owner A สร้างใบ มีเอกสารอย่างน้อย 2 แถวต่างระดับความลับ
2. บันทึกร่าง ตรวจเลข IVMG, ผู้จัดทำ snapshot, ลำดับแถว และค่าที่บันทึกกลับมา
3. ส่งอนุมัติ เลือกผู้ตรวจสอบและผู้อนุมัติคนละคนกับ owner
4. ขั้น 1 ตรวจสอบแล้ว จากนั้นขั้น 2 อนุมัติ
5. ตรวจสถานะ `approved`, PDF, ลายเซ็น/วันเวลา, stored `approved_final`
6. Owner บันทึกหลักฐานอย่างน้อย 2 แถว: `received` 1 แถว และ `failed` 1 แถว
7. ตรวจว่าสถานะยังเป็น `approved`, มี audit และมี `ivmg_delivery_failed`
8. ปิดการนำส่ง ตรวจสถานะ `closed`, ล็อกทั้งใบ, audit และ `ivmg_dispatch_closed`

Expected: FRD AC-01, AC-06, AC-08, AC-10, AC-11; FN-01..06, FN-09..13

### P0-02 ส่งกลับ แก้ และส่งใหม่

- ส่งกลับจากขั้น 1 โดยไม่กรอกเหตุผลต้องไม่ได้
- กรอกเหตุผลแล้วต้องกลับ `draft`, เลขเดิม, เห็นเหตุผลและประวัติ
- แก้ข้อมูลแล้วส่งใหม่ ต้อง resolve DOA ใหม่ ไม่ใช้ chain เดิมแบบเงียบ ๆ
- chain รอบเก่าต้องยังอยู่ใน audit แต่ไม่เป็น chain ปัจจุบัน

Expected: BR-12, FN-07, AC-07

### P0-03 สิทธิ์และการซ่อนข้อมูล

- Owner B ต้องไม่เห็นหรือเปิด draft ของ Owner A
- ผู้อนุมัติต้องไม่เห็น draft ก่อนถูกส่ง
- ผู้ที่ไม่ใช่ current approver ต้องตัดสินไม่ได้ทั้งจาก UI และ direct request
- ผู้ตรวจสอบ/ผู้อนุมัติต้องบันทึกหลักฐานหรือปิดการนำส่งไม่ได้
- คนนอกต้องยกเลิกไม่ได้
- เอกสารที่ไม่มีสิทธิ์ต้องตอบแบบไม่เปิดเผยการมีอยู่ของใบ (`404 NOT_FOUND`)

Expected: §5.3, TC-D01..D08, FN-12

### P0-04 ปิดการนำส่ง

ทดสอบอย่างน้อย 5 ชุด:

| หลักฐาน | Expected |
|---|---|
| ไม่มีแถว | ปิดไม่ได้ |
| มีแต่ `pending` | ปิดไม่ได้ |
| มีแต่ `failed/cancelled` | ปิดไม่ได้ เพราะไม่มี `received` |
| มี `received` และยังมี `pending` | ปิดไม่ได้ |
| มี `received` อย่างน้อย 1 และแถวอื่นเป็น `failed/cancelled` ไม่มี `pending` | ปิดได้ตาม FRD |

Expected: BR-09, VR-10, FN-13

### P0-05 ป้องกันการกดซ้ำและข้อมูลชนกัน

- Double-click บันทึกร่าง/ส่งอนุมัติ/อนุมัติ/ปิด ต้องไม่สร้างใบ, decision, event หรือเลขซ้ำ
- เปิดใบเดียวกันสองหน้าต่าง แก้จากหน้าต่างแรก แล้วบันทึกหน้าต่างที่สอง ต้องได้ `409 STALE` และไม่ทับข้อมูลใหม่
- Retry ด้วย Idempotency-Key เดิมต้องได้ผลเดิม ไม่ทำรายการซ้ำ

Expected: API §2.3, EC-15

## 5. ชุด P1 — Validation และขอบเขตข้อมูล

### 5.1 ก่อนส่งอนุมัติ

- ช่องหลัก 4 ช่องว่างทีละช่องและว่างพร้อมกัน
- ไม่มีรายการเอกสาร, ชื่อเอกสารว่าง, ฉบับว่าง
- `missing` และ `limited` ไม่มีหมายเหตุ ต้องบล็อก
- `missing` มีหมายเหตุ ต้องเตือนแต่ส่งได้
- `complete` และ `na` ไม่ควรถูกบังคับหมายเหตุ
- เพิ่ม 3 แถว ลบแถวกลาง ลำดับต้องรันใหม่ 1..N และไม่ใช้ลำดับเป็น key
- ทดสอบระดับความลับทั้ง 4 ค่าและตรวจ `top_confidentiality`
- ข้อความยาว, ภาษาไทย/อังกฤษ, emoji, เครื่องหมาย `< > & " '`, ช่องว่างล้วน และขึ้นบรรทัดใหม่ ต้องไม่ทำ UI/PDF/CSV เสียและไม่ bypass required

Expected: BR-01..04, BR-10, VR-01..04, FN-01/02

### 5.2 หลักฐานการนำส่ง

- `sent_at` ว่าง, เวลาไม่ครบ, เวลาอนาคต 1 นาที, เท่ากับเวลาปัจจุบัน, ก่อน `dispatch_date`
- sender/receiver/receiver_org/docs_sent ว่างทีละช่อง
- `received` ไม่มีทั้งลิงก์และไฟล์ ต้องบล็อก; มีไฟล์อย่างเดียวต้องผ่าน
- channel=`other` ไม่มีหมายเหตุ ต้องบล็อก
- receipt=`failed` หรือ `cancelled` ไม่มีหมายเหตุ ต้องบล็อก
- บันทึกก่อนวันที่นำส่งต้องเตือนแต่บันทึกได้
- ลบแถวกลางและตรวจลำดับใหม่
- บันทึกแบบ replace ทั้งชุดแล้วตรวจว่าแถวเดิมที่ไม่ได้แก้ไม่หาย/ไม่สลับผิด

Expected: BR-06..08, VR-05..09, FN-10

### 5.3 ไฟล์แนบ

- ชนิดที่อนุญาตทุกกลุ่มและไฟล์เกิน 20 MB
- เปลี่ยนชื่อไฟล์ให้ extension หลอกหรือ content type ไม่ตรง
- แนบระดับใบและแนบหลักฐานต่อแถว ตรวจว่าไม่สลับ reference
- ผู้ไม่มีสิทธิ์ต้องดาวน์โหลดไฟล์จาก URL โดยตรงไม่ได้
- หลังปิดใบ ต้องเพิ่ม/ลบ/แทนไฟล์ไม่ได้
- ถ้าลบแถวหลักฐาน ต้องตรวจว่าไฟล์เดิมไม่กลายเป็น orphan ที่คนอื่นเข้าถึงได้

Expected: FN-03, BR-05; ประเด็น orphan/secure download เป็น exploratory security check

## 6. ชุด P1 — State และ Permission Matrix

ตรวจทุก action ทั้ง “ปุ่มไม่แสดง” และ “ยิง request ตรงแล้วถูกปฏิเสธ”

| State | ดู | แก้/ส่ง | ตัดสิน | หลักฐาน/ปิด | ยกเลิก |
|---|---|---|---|---|---|
| draft | owner/admin ตาม FRD visibility | owner เท่านั้น | ไม่ได้ | ไม่ได้ | owner/admin |
| pending | owner, chain, admin | ไม่ได้ | current approver เท่านั้น | ไม่ได้ | owner/admin |
| approved | owner, chain, admin | ไม่ได้ | ไม่ได้ | owner/admin | ไม่ได้ |
| closed | ผู้มีสิทธิ์ดู | ไม่ได้ | ไม่ได้ | ไม่ได้ | ไม่ได้ |
| cancelled | ผู้มีสิทธิ์ดู | ไม่ได้ | ไม่ได้ | ไม่ได้ | ไม่ได้ |

ตรวจ transition ต้องไม่มีทางลัด: `draft → approved`, `pending → closed`, `closed → approved`, `cancelled → draft` ต้องทำไม่ได้

Expected: §5.2, §5.3, API error contracts

## 7. ชุด P1 — DOA และ Snapshot

- ตอนส่ง จำนวน slot ต้องตรง DOA ที่ resolve ได้จริง
- ผู้จัดทำต้องไม่อยู่ในรายชื่อผู้พิจารณาและ API ต้องปฏิเสธ self-approval
- เปลี่ยน DOA หลังส่งแล้ว ใบที่ pending ต้องใช้ chain snapshot เดิม
- ใบถูกส่งกลับแล้วส่งใหม่ ต้อง resolve chain ใหม่
- ทดสอบอย่างน้อย 1, 2 และถ้าสภาพแวดล้อมปลอดภัย 6 ขั้น; PDF ต้องมี requester + N ขั้น
- ผู้ใช้ใน chain ถูก disable/ย้ายหน่วยงานระหว่าง pending: บันทึก actual และถาม owner ว่ามีกลไก reassign/escalate หรือไม่ เพราะ FRD ไม่ระบุ
- ตรวจ My Approval และ notification ของ DOA engine ไม่ถูก feature ยิงซ้ำ

Expected: BR-11/12/15, FN-05/06/07, AC-05/06/15

## 8. ชุด P1 — เลขเอกสาร, PDF, CSV และ Archive

### เลขเอกสาร

- ออกเลขเมื่อบันทึกครั้งแรกเท่านั้น; validation ที่บล็อกก่อนบันทึกต้องไม่สร้างใบสำเร็จ
- ส่งกลับ/แก้/ส่งใหม่ใช้เลขเดิม
- สร้างพร้อมกันหลายผู้ใช้ เลขต้องไม่ซ้ำ
- ปิด doc type IVMG แล้วสร้างไม่ได้; ใบเก่าควรยังเปิดอ่านได้
- ตรวจ company context, reset รายปี และรูปแบบ `{PREFIX}-{YYYY}-{run:4}` ตามการตั้งค่าจริง

### PDF

- เทียบ PDF กับค่าบนจอและฐานข้อมูลในทุก state: draft, pending, approved, closed, cancelled
- ต้อง 2 หน้า; แถวขั้นต่ำ docs 10, deliveries 15; เกินขั้นต่ำแล้วข้อมูลไม่หายและหัวตารางอ่านได้
- วันที่ พ.ศ., เวลา, ชื่อบริษัท/logo/header snapshot, FM-IVM-07 Rev.00 และเลขหน้า
- ชื่อผู้จัดทำ/ผู้ตรวจทาน/ผู้อนุมัติต้องมาจาก snapshot/chain จริง ไม่ใช่ชื่อปัจจุบันที่ถูกแก้ภายหลัง
- PDF server-side และ preview/download ต้องให้ข้อมูลชุดเดียวกัน
- ลายเซ็น/decision word/วันเวลาตรงกับแต่ละขั้นและไม่ตัดกลาง

### CSV

- export ต้องใช้ filter และ permission เดียวกับหน้ารายการ
- จำนวนแถวและค่าต้องตรง, ภาษาไทยไม่เพี้ยน, วันที่/เลขเอกสารไม่ถูกโปรแกรมตารางคำนวณแปลงผิด
- ค่าที่ขึ้นต้น `=`, `+`, `-`, `@` ต้องไม่กลายเป็น spreadsheet formula ที่อันตราย (exploratory security)

Expected: BR-13, BR-15/16/18, FN-04/09/12

## 9. ชุด P1 — Audit, Notification และ Integration

### Audit

ต้องมี actor/time/action และ before/after ที่สอดคล้องกันสำหรับ create, edit, submit, approve แต่ละขั้น, return, cancel, save deliveries, close และ stale failure ที่ไม่ควรเกิด write ตรวจว่า audit เป็น append-only และผู้ใช้ทั่วไปแก้/ลบไม่ได้

### Notification

- ยกเลิกจาก `pending` → `ivmg_cancelled` ถึง current approver คนเดียวตาม template
- เพิ่มหรือเปลี่ยนแถวเป็น `failed` → `ivmg_delivery_failed` ถึง owner + admin
- กดบันทึกซ้ำโดยแถวยังคง failed → ต้องไม่ยิงซ้ำทุกครั้ง; FRD ระบุยิงเมื่อ “แถวใหม่หรือเปลี่ยนเป็น failed”
- ปิด → `ivmg_dispatch_closed` ถึง approval chain + admin โดยไม่ส่งซ้ำให้คนเดียวกันหลายฉบับถ้าอยู่หลาย role
- ห้ามยิง `ivmg.approved` และ `ivmg.closed`; DOA event ต้องมาจาก DOA engine ไม่ยิงซ้ำ

### Document Store

- เมื่ออนุมัติครบ ต้องมี `approved_final` เพียงหนึ่งผลที่ถูกต้อง
- retry/double approve ต้องไม่เก็บ archive ซ้ำ
- ตรวจว่า archive เปิดได้เฉพาะผู้มีสิทธิ์และข้อมูลตรง PDF ณ เวลาอนุมัติ

Expected: FN-06/10/11, XT-01..03, DOCCFG/NTF declarations

## 10. Business-sense exploratory flows

หัวข้อต่อไปนี้ควร “ลองเล่น” และบันทึกเป็น Question/Improvement ก่อน เว้นแต่พบว่าขัด FRD ชัดเจน:

1. **Approved final ไม่มีหลักฐานหลังนำส่ง:** ระบบเก็บ `approved_final` ตอนอนุมัติ แต่หลักฐานถูกกรอกภายหลังในใบเดียวกัน แล้วปิดงานภายหลัง ต้องถาม PM/BA ว่าเอกสาร archive ที่ต้องใช้ตรวจสอบจริงควรเป็นเวอร์ชันตอนอนุมัติ หรือควรมี `closed_final` เพิ่ม มิฉะนั้น archive อาจไม่มีหลักฐานการนำส่ง
2. **ปิดได้แม้มี failed/cancelled:** FRD อนุญาตให้ปิดเมื่อมี received ≥1 และไม่มี pending แม้บางแถว failed/cancelled ให้ยืนยันว่า business ยอมรับ “ปิดสำเร็จบางส่วน” และรายงานแยกได้
3. **หลักฐานแก้ได้หลังอนุมัติโดยไม่อนุมัติซ้ำ:** ถูกตาม FRD แต่ต้องตรวจ audit before/after และจำกัด owner/admin จริง เพราะเป็นข้อมูลใช้พิสูจน์การนำส่ง
4. **ไม่มี reopen:** closed ล็อกถาวร หากพบหลักฐานผิดหลังปิด มี process แก้อย่างไร—ออกใบใหม่, admin correction หรือ incident process
5. **ยกเลิกหลังอนุมัติไม่ได้:** FRD มี OQ-10 แต่กฎปัจจุบันไม่ให้ยกเลิก approved/closed ต้องยืนยัน operational process เมื่อโครงการหยุดหลังอนุมัติแต่ก่อนนำส่ง
6. **Admin เห็นข้อมูลลับทั้งหมด:** ยืนยัน least privilege, audit การเข้าดู/ดาวน์โหลด และ role id จริง เพราะ FRD เดิมยังมี OQ-04
7. **ระดับความลับไม่มีผลต่อช่องทาง:** อยู่ Out of Scope ตาม OQ-09 แต่เป็น risk สำคัญ เช่น “ลับมาก” ยังส่งอีเมลได้ ควรให้ PM/BA ยอมรับ risk เป็นลายลักษณ์อักษร
8. **ผู้รับ/วันที่นำส่งเป็นแผนหรือเหตุการณ์จริง:** ก่อนอนุมัติเรียก “วันที่นำส่ง” แต่หลักฐานอาจเกิดก่อน/หลัง ต้องยืนยันความหมายทางธุรกิจเพื่อไม่ให้ผู้ใช้เข้าใจผิด
9. **Failed event ซ้ำ:** API บันทึก deliveries แบบแทนทั้งชุด หาก frontend ไม่รักษา row id อาจมองแถว failed เดิมเป็นแถวใหม่และแจ้งซ้ำ ต้องทดสอบโดยบันทึกใบเดิมหลายครั้ง
10. **ผู้พิจารณาหายระหว่างทาง:** ไม่มี reassign/delegate/escalate ใน FRD ถ้าคนลาออก/ลางาน ใบอาจค้างถาวร
11. **Retention และสิทธิ์ลบ:** FRD ระบุไม่ hard delete แต่ retention ยังต้องยืนยัน Policy Center; ตรวจว่าผู้ใช้ไม่มีทางลบใบหรือ audit ผ่าน API
12. **Timezone:** ทดสอบช่วง 23:59–00:01 และผู้ใช้ timezone ต่างกัน เพราะ validation อนาคต/ก่อนวันที่นำส่งและวันที่ พ.ศ. อาจคลาดวัน

## 11. ความขัดแย้ง/คำถามในเอกสารที่ต้องไม่รีบฟันธงเป็น Bug

- FRD หลักใช้ state `pending` แต่ DOA declaration บางส่วนใช้ `pending_approval`; ให้ dev/BA ยืนยัน canonical state และ mapping
- FRD ระบุ OQ-03 role DOA, OQ-04 admin role id และ OQ-10 การยกเลิกหลังอนุมัติยังต้องยืนยัน
- สาย DOA ค่าเริ่ม 2 ขั้นและหลาย locked decisions เป็น `AI-DEFAULT`; ถ้ายังไม่มีลูกค้าเซ็น ให้รายงานเป็น requirement risk ไม่ใช่สรุปว่าระบบถูกธุรกิจแล้ว
- README เดิมบอกว่าไม่มี browser E2E/PDF verification; ผลทดสอบ prototype ไม่ใช่หลักฐาน production integration

## 12. ลำดับรันที่แนะนำ

### รอบ 1 — Smoke + Full lifecycle (60–90 นาที)

รัน P0-01 ถึง P0-04 หาก fail เรื่องสิทธิ์/state/ข้อมูล ให้หยุดและเปิด defect ก่อน

### รอบ 2 — Negative + Permission (90–120 นาที)

รัน §5 และ §6 ด้วยหลายบัญชี โดยตรวจทั้ง UI และ API response ถ้าเข้าถึงได้

### รอบ 3 — Integration + Evidence (90–120 นาที)

รัน §7–§9 พร้อมผู้ดูแลหลังบ้าน ตรวจ DOA, notification, audit, document store, PDF และ CSV

### รอบ 4 — Exploratory business review (60 นาที)

เดินตาม §10 แล้วประชุม PM/BA เฉพาะข้อที่ระบบทำตาม FRDแต่มีผลธุรกิจน่าสงสัย

## 13. เกณฑ์สรุปผล

- ผ่าน: P0 ผ่านทั้งหมด, ไม่มี Critical/High ค้าง, P1 ที่รันผ่านหรือมีข้อยกเว้นที่ PM/BA ยอมรับ
- ผ่านแบบมีเงื่อนไข: ไม่มี Critical แต่มี High/logic fail 1–2 จุดพร้อม owner และกำหนดแก้/retest
- ไม่ผ่าน: มี Critical หรือ logic fail ตั้งแต่ 3 จุดขึ้นไป
- ทุกหัวข้อที่ยังไม่รันต้องระบุ ไม่ถือว่าผ่านโดยปริยาย

เมื่อทดสอบเสร็จ ให้นำผลจริงและหลักฐานมาสร้าง Feature Check Report; ห้ามใช้เอกสารแผนนี้เป็นใบรับรองผลตรวจ
