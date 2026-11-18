# PREBRIEF — Service Experience Survey (REQ-TMP-006)

> PREBRIEF v2 — สร้างจาก FORM_SPEC (อ่านแบบฟอร์มลูกค้าระดับช่อง) · ไม่มี PREBRIEF จาก CMS · prebrief-to-devpack v2

## 0. สรุป
- **เอกสารนี้คืออะไร:** Service Experience Survey — แบบฟอร์มของลูกค้า ขึ้นเป็นเอกสารในระบบ
- **หมวด / Module:** FRM · SALES
- **ประเภทงานพัฒนา: แบบ 2 · ดึงข้อมูลเดิม** — มีช่องที่อ่านจาก feature เดิม (อ่านอย่างเดียว)
- **ช่องข้อมูล 14 ช่อง:** ดึงจากระบบ 1 · ผู้ใช้กรอก 13 · คำนวณ 0 · ระบบใส่ให้ 0 · รายการซ้ำ 0 กลุ่ม · ตัวเลือก 10 · ลายเซ็น 0
- **รูปแบบ:** เอกสารเดี่ยว · แบบพิมพ์ 1: FM-SAL-22 Service Experience Survey (Rev.00 : 01/07/2569) · โหมดแบบพิมพ์ Replica (thai-doc-pdf-generator v2) · เลขที่เดียว

## 1. คำขอ
- ลูกค้า: — · ผู้ขอ — · — · ความเร่ง — · ต้องการใช้ —
- ไฟล์ตัวอย่าง: 22. FM-SAL-22 แบบประเมินความพึงพอใจ Sales Admin (ต่างประเทศ).docx · sha256 1bdb05eeb2207d964db5ba47a778035534bd277c5ca4701c0c8c8ad8c4369d61

## 3. ช่องข้อมูลทั้งหมด (จาก FORM_SPEC — ตามกระดาษ)
| # | ช่อง | ชนิด (เอกสาร) | ในระบบ | ใช้เป็น | entity.field | feature เจ้าของ | AI มั่นใจ | ยืนยันโดยคน | ตัวอย่าง | PDPA |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Month | month | ไม่มี · เก็บในเอกสารนี้ | ให้ผู้ใช้กรอก | `survey.period_month` | — | อ่านจากฟอร์ม | — |  |  |
| 2 | Company Name | lookup | มีในระบบ · ตรง | ดึงจากระบบ | Customer.name (customerId) | Customer master (Sales · sales-module · Customer ref contract) | อ่านจากฟอร์ม | — |  |  |
| 3 | Contact Person | ข้อความ | ไม่มี · เก็บในเอกสารนี้ | ให้ผู้ใช้กรอก | `survey.contact_person` | — | อ่านจากฟอร์ม | — | (ข้อมูลส่วนบุคคล) | ใช่ |
| 4 | Communication clarity | rating | ไม่มี · เก็บในเอกสารนี้ | ให้ผู้ใช้กรอก | `score.q1` | — | อ่านจากฟอร์ม | — |  |  |
| 5 | Response time to inquiries | rating | ไม่มี · เก็บในเอกสารนี้ | ให้ผู้ใช้กรอก | `score.q2` | — | อ่านจากฟอร์ม | — |  |  |
| 6 | Follow-up consistency | rating | ไม่มี · เก็บในเอกสารนี้ | ให้ผู้ใช้กรอก | `score.q3` | — | อ่านจากฟอร์ม | — |  |  |
| 7 | Accuracy of documents | rating | ไม่มี · เก็บในเอกสารนี้ | ให้ผู้ใช้กรอก | `score.q4` | — | อ่านจากฟอร์ม | — |  |  |
| 8 | Timeliness of document submission | rating | ไม่มี · เก็บในเอกสารนี้ | ให้ผู้ใช้กรอก | `score.q5` | — | อ่านจากฟอร์ม | — |  |  |
| 9 | Shipment coordination support | rating | ไม่มี · เก็บในเอกสารนี้ | ให้ผู้ใช้กรอก | `score.q6` | — | อ่านจากฟอร์ม | — |  |  |
| 10 | Effectiveness in resolving issues | rating | ไม่มี · เก็บในเอกสารนี้ | ให้ผู้ใช้กรอก | `score.q7` | — | อ่านจากฟอร์ม | — |  |  |
| 11 | Proactive service updates | rating | ไม่มี · เก็บในเอกสารนี้ | ให้ผู้ใช้กรอก | `score.q8` | — | อ่านจากฟอร์ม | — |  |  |
| 12 | Professionalism of our team | rating | ไม่มี · เก็บในเอกสารนี้ | ให้ผู้ใช้กรอก | `score.q9` | — | อ่านจากฟอร์ม | — |  |  |
| 13 | Overall service satisfaction | rating | ไม่มี · เก็บในเอกสารนี้ | ให้ผู้ใช้กรอก | `score.q10` | — | อ่านจากฟอร์ม | — |  |  |
| 14 | Additional Feedback | textarea | ไม่มี · เก็บในเอกสารนี้ | ให้ผู้ใช้กรอก | `survey.comment` | — | อ่านจากฟอร์ม | — |  |  |

### 3.1 รายการซ้ำ
- ไม่มี

### 3.2 ตัวเลือก
- **Communication clarity** (เลือกได้ข้อเดียว): 1 · 2 · 3 · 4 · 5
- **Response time to inquiries** (เลือกได้ข้อเดียว): 1 · 2 · 3 · 4 · 5
- **Follow-up consistency** (เลือกได้ข้อเดียว): 1 · 2 · 3 · 4 · 5
- **Accuracy of documents** (เลือกได้ข้อเดียว): 1 · 2 · 3 · 4 · 5
- **Timeliness of document submission** (เลือกได้ข้อเดียว): 1 · 2 · 3 · 4 · 5
- **Shipment coordination support** (เลือกได้ข้อเดียว): 1 · 2 · 3 · 4 · 5
- **Effectiveness in resolving issues** (เลือกได้ข้อเดียว): 1 · 2 · 3 · 4 · 5
- **Proactive service updates** (เลือกได้ข้อเดียว): 1 · 2 · 3 · 4 · 5
- **Professionalism of our team** (เลือกได้ข้อเดียว): 1 · 2 · 3 · 4 · 5
- **Overall service satisfaction** (เลือกได้ข้อเดียว): 1 · 2 · 3 · 4 · 5

### 3.3 สูตร + ค่าคงที่บนกระดาษ

### 3.4 ลายเซ็น + control
- Doc No. บนกระดาษ Doc No.FM-SAL-22 · Rev.00 : 01/07/2569 · เลขรันบนกระดาษ: ไม่มี (ระบบออกเลขเอง)

### 3.5 ข้อมูลตัวอย่างที่ขัดกัน → กฎตรวจที่ควรมี
- กระดาษมี ☐ 5 ช่องต่อข้อ ไม่ระบุว่าเลือกได้กี่ช่อง → **1 ข้อเลือกได้ 1 คะแนน · ครบ 10 ข้อจึงบันทึกผลได้**
- มีแค่ Month ไม่มีช่องวันที่ (ต่างจาก FM-SAL-20) → **วันที่บันทึก = เวลาระบบ (created_at) · ไม่เพิ่มช่องวันที่บนกระดาษ (1:1)**
- บรรทัด 'Month : …….' สั้นมาก ไม่ระบุรูปแบบ → **เลือกเดือน/ปี (MMM YYYY) · ค่าเริ่ม = เดือนปัจจุบัน**
- ฟอร์มทั้งใบเป็นภาษาอังกฤษ (ลูกค้าต่างประเทศ) → **ป้ายช่อง/หัวข้อ/แบบพิมพ์ใช้ภาษาอังกฤษตามกระดาษ 1:1 · ส่วนควบคุมระบบ (ปุ่ม/สถานะ) ใช้ภาษาไทยตาม CI · แบบพิมพ์สองภาษาให้ลูกค้ายืนยันใน OQ**

## 4. ผลกระทบ feature เดิม
### 4.1 ต้องเพิ่มฟิลด์ (แบบ 3)
- ไม่ต้องเพิ่มฟิลด์ใน feature เดิม (ยืนยันใน gate ถ้ามีช่องไม่ตรง)

### 4.2 อ่านข้อมูลจาก feature เดิม (แบบ 2 · อ่านอย่างเดียว)
- Company Name ← `Customer.name (customerId)` (Customer master (Sales · sales-module · Customer ref contract))

### 4.3 มีในระบบแต่ไม่ตรง — คำถามค้าง (ต้องตัดสินก่อน FRD)
- ไม่มี

## 5. Scenario (ร่าง — ยืนยันตอนทำ HTML)
| # | ประเภท | Scenario |
|---|---|---|
| S1 | ปกติ | สร้างService Experience Survey — ระบบดึง Company Name ให้ → กรอก Month, Contact Person, Communication clarity, Response time to inquiries, Follow-up consistency, Accuracy of documents, Timeliness of document submission, Shipment coordination support, Effectiveness in resolving issues, Proactive service updates, Professionalism of our team, Overall service satisfaction, Additional Feedback → บันทึก → ได้เลขที่ |
| S2 | ทางเลือก | Communication clarity = 1 |
| S3 | ทางเลือก | Communication clarity = 2 |
| S4 | ทางเลือก | Communication clarity = 3 |
| S5 | ทางเลือก | Communication clarity = 4 |
| S6 | ทางเลือก | Communication clarity = 5 |
| S7 | ทางเลือก | Response time to inquiries = 1 |
| S8 | ทางเลือก | Response time to inquiries = 2 |
| S9 | ทางเลือก | Response time to inquiries = 3 |
| S10 | ทางเลือก | Response time to inquiries = 4 |
| S11 | ทางเลือก | Response time to inquiries = 5 |
| S12 | ทางเลือก | Follow-up consistency = 1 |
| S13 | ทางเลือก | Follow-up consistency = 2 |
| S14 | ทางเลือก | Follow-up consistency = 3 |
| S15 | ทางเลือก | Follow-up consistency = 4 |
| S16 | ทางเลือก | Follow-up consistency = 5 |
| S17 | ทางเลือก | Accuracy of documents = 1 |
| S18 | ทางเลือก | Accuracy of documents = 2 |
| S19 | ทางเลือก | Accuracy of documents = 3 |
| S20 | ทางเลือก | Accuracy of documents = 4 |
| S21 | ทางเลือก | Accuracy of documents = 5 |
| S22 | ทางเลือก | Timeliness of document submission = 1 |
| S23 | ทางเลือก | Timeliness of document submission = 2 |
| S24 | ทางเลือก | Timeliness of document submission = 3 |
| S25 | ทางเลือก | Timeliness of document submission = 4 |
| S26 | ทางเลือก | Timeliness of document submission = 5 |
| S27 | ทางเลือก | Shipment coordination support = 1 |
| S28 | ทางเลือก | Shipment coordination support = 2 |
| S29 | ทางเลือก | Shipment coordination support = 3 |
| S30 | ทางเลือก | Shipment coordination support = 4 |
| S31 | ทางเลือก | Shipment coordination support = 5 |
| S32 | ทางเลือก | Effectiveness in resolving issues = 1 |
| S33 | ทางเลือก | Effectiveness in resolving issues = 2 |
| S34 | ทางเลือก | Effectiveness in resolving issues = 3 |
| S35 | ทางเลือก | Effectiveness in resolving issues = 4 |
| S36 | ทางเลือก | Effectiveness in resolving issues = 5 |
| S37 | ทางเลือก | Proactive service updates = 1 |
| S38 | ทางเลือก | Proactive service updates = 2 |
| S39 | ทางเลือก | Proactive service updates = 3 |
| S40 | ทางเลือก | Proactive service updates = 4 |
| S41 | ทางเลือก | Proactive service updates = 5 |
| S42 | ทางเลือก | Professionalism of our team = 1 |
| S43 | ทางเลือก | Professionalism of our team = 2 |
| S44 | ทางเลือก | Professionalism of our team = 3 |
| S45 | ทางเลือก | Professionalism of our team = 4 |
| S46 | ทางเลือก | Professionalism of our team = 5 |
| S47 | ทางเลือก | Overall service satisfaction = 1 |
| S48 | ทางเลือก | Overall service satisfaction = 2 |
| S49 | ทางเลือก | Overall service satisfaction = 3 |
| S50 | ทางเลือก | Overall service satisfaction = 4 |
| S51 | ทางเลือก | Overall service satisfaction = 5 |
| S52 | ปกติ | พิมพ์ / ออก PDF รูปแบบ FM-SAL-22 (Replica) ทุกสถานะ |
| S53 | ผิดปกติ | กระดาษมี ☐ 5 ช่องต่อข้อ ไม่ระบุว่าเลือกได้กี่ช่อง → 1 ข้อเลือกได้ 1 คะแนน · ครบ 10 ข้อจึงบันทึกผลได้ |
| S54 | ผิดปกติ | มีแค่ Month ไม่มีช่องวันที่ (ต่างจาก FM-SAL-20) → วันที่บันทึก = เวลาระบบ (created_at) · ไม่เพิ่มช่องวันที่บนกระดาษ (1:1) |
| S55 | ผิดปกติ | บรรทัด 'Month : …….' สั้นมาก ไม่ระบุรูปแบบ → เลือกเดือน/ปี (MMM YYYY) · ค่าเริ่ม = เดือนปัจจุบัน |
| S56 | ผิดปกติ | ฟอร์มทั้งใบเป็นภาษาอังกฤษ (ลูกค้าต่างประเทศ) → ป้ายช่อง/หัวข้อ/แบบพิมพ์ใช้ภาษาอังกฤษตามกระดาษ 1:1 · ส่วนควบคุมระบบ (ปุ่ม/สถานะ) ใช้ภาษาไทยตาม CI · แบบพิมพ์สองภาษาให้ลูกค้ายืนยันใน OQ |

## 6. Function checklist (ร่าง)
- [ ] FN-01 รายการเอกสาร + ค้นหา/กรอง
- [ ] FN-02 สร้าง/แก้ไขเอกสาร (ช่องตามกระดาษ 1:1)
- [ ] FN-03 เลขที่จาก ENG-DOC-NUM · เช็คสถานะเปิดใช้ที่ F-DOCCFG (F003) ก่อนออกเลข
- [ ] FN-06 พิมพ์ / PDF แบบ Replica (template + data contract)
- [ ] FN-07 ยกเลิก + ประวัติ

## 7. หน้าจอ (ร่าง)
- P-01 รายการService Experience Survey
- P-02 สร้าง/แก้ไขService Experience Survey
- P-03 รายละเอียด (PDF · ลายเซ็น/อนุมัติ · ประวัติ)

## 8. กติกา / declaration
- DOA: ไม่มีช่องผู้อนุมัติบนกระดาษ — ยืนยันใน gate G2
- DOCCFG: ประกาศ doc_type + print_config (form_code/revision/min_rows/sign_boxes) — ร่างก่อน HTML
- MDOC: ลงทะเบียนแบบเอกสาร (F-DOCCFG / F003) · source=request
- NTF: ตาม gate G10 (ประกาศ)
