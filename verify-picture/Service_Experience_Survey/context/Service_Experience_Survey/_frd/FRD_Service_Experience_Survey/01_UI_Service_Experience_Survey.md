# 01_UI — F-TMP-006 Service Experience Survey (แบบประเมินความพึงพอใจ Sales Admin — ลูกค้าต่างประเทศ)
> Source of truth = `feature.html` (html-generator-v9.4 · Q-form · audit FAIL 0) — FRD สกัด+บันทึก ไม่เขียนสวนจอ

## §1.0 Layout Decision Log
| หน้า | Pattern | เหตุผล |
|---|---|---|
| P-01 | A list · **ไม่มี scorecard (#115)** · จำนวน = badge ใน sub · segmented tabs สถานะ (#117) · filter (ค้นหา · ประจำเดือน · ผู้บันทึก) · row action kebab ⋮ (#116) · pagination 10/25/50 | Q-form surface 1 · v9.4 Group 25 |
| P-02 | B drawer `.wide` · stepper 3 ขั้นล็อก (#100F) · `.wz-split` ฟอร์มซ้าย + `sumCard` ขวา | Q-form surface 2 |
| P-03 | C drawer 920 · tabs รายละเอียด › PDF Preview › ลายเซ็น / อนุมัติ › ประวัติ (#101) · header lean (#119) | Q-form surface 3 |
| M-01..03 | D modal · backdrop ปิดด้วย mousedown (#122) | บันทึกผล · ยกเลิก · ทิ้งข้อมูล |

## §1.1 Page Inventory
| ID | Route | ชื่อ | ผู้ใช้ |
|---|---|---|---|
| P-01 | `#/sa-csat-ovs` | รายการ Service Experience Survey (ต่างประเทศ) | Maker · role-mgr-sales (เห็นตาม 05 §5.3) |
| P-02 | `#/sa-csat-ovs/create` · `#/sa-csat-ovs/edit/:id` | สร้าง / แก้ร่าง | Maker |
| P-03 | `#/sa-csat-ovs/view/:id` | รายละเอียด | ผู้มีสิทธิ์เห็น |

## §1.2 Per-Page Detail
### P-01 รายการ
- หัว: "Service Experience Survey (แบบประเมินความพึงพอใจ Sales Admin — ลูกค้าต่างประเทศ)" · sub "บันทึกผลประเมินความพึงพอใจต่องาน Sales Admin ของลูกค้าต่างประเทศ" + badge "N รายการ · ร่าง n" · ปุ่ม ส่งออก CSV (secondary) · สร้างแบบประเมิน (primary · disabled + แถบ "แบบเอกสารนี้ยังไม่เปิดใช้งาน" เมื่อ F-DOCCFG ปิดใช้)
- segmented tabs: ทั้งหมด · ร่าง · บันทึกผลแล้ว · ยกเลิก (+count)
- คอลัมน์ (1 cell = 1 บรรทัด): เลขที่ · วันที่บันทึก · ประจำเดือน · ลูกค้า · ผู้บันทึก · คะแนนเฉลี่ย (แสดงผลเท่านั้น · BR-10) · สถานะเอกสาร · ⋮ (ดูรายละเอียด · แก้ไข[ร่างของตน] · พิมพ์ · ยกเลิกเอกสาร[ตามสิทธิ์])
- ค้นหา: เลขที่ / ลูกค้า / ผู้ติดต่อ / ผู้บันทึก
- empty: ไม่มีข้อมูล = แผง + ปุ่มสร้าง / กรองแล้วไม่พบ = ล้างตัวกรอง
### P-02 สร้าง / แก้ร่าง (STEPS = ข้อมูลหลักแบบประเมิน › เอกสารแนบ › ตรวจสอบและยืนยัน)
- ขั้น 1 การ์ด ① "ประจำเดือนและลูกค้า": ประจำเดือน (Month · combobox 12 เดือนล่าสุด · ค่าเริ่ม = เดือนปัจจุบัน) · ชื่อลูกค้า (Company Name · combobox Customer master ต่างประเทศ · option = icon → ชื่อ → รหัส · ประเทศ) · ผู้ติดต่อ (Contact Person · ข้อความ ≤ 120 ตัวอักษร · บังคับ)
- การ์ด ②③④ ต่อกลุ่ม: COMMUNICATION & RESPONSIVENESS (3) · DOCUMENTATION & EXECUTION (5) · PROFESSIONALISM (2) — แถวละข้อ (ถ้อยคำอังกฤษตรงกระดาษ) + ปุ่ม 1 · 2 · 3 · 4 · 5 (radiogroup · คีย์ `score.q1`…`score.q10`) · หัวแถว "1 = Very Dissatisfied · 5 = Very Satisfied" · "ตอบ x/n" ต่อกลุ่ม
- การ์ด ⑤ "Additional Feedback" (`comment` · ไม่บังคับ)
- ไม่มีช่องวันที่ (กระดาษไม่มี · DEC-12) — วันที่บันทึก = เวลาระบบ
- sumCard ขวา (อัปเดตสด ไม่ rebuild): ลูกค้า · ผู้บันทึก · ตอบแล้ว x/10 · จำนวนคะแนนต่ำ · เฉลี่ยต่อกลุ่ม · คะแนนเฉลี่ยรวม
- ขั้น 2 แนบไฟล์ (Document Center) · ขั้น 3 ตรวจสอบ: ตารางคะแนนต่อกลุ่ม + เตือนถ้ายังไม่ครบ 10 ข้อ
- footer: ย้อนกลับ · ยกเลิก · ถัดไป / บันทึกแบบร่าง + บันทึกผลแบบประเมิน · ปิดตอนกรอกค้าง = modal "ทิ้งข้อมูลที่กรอกไว้?"
### P-03 ดู
- header: kicker ชื่อเอกสาร · เลขที่ + pill สถานะ · sub ≤ 2 fact (ประจำเดือน · คะแนนเฉลี่ย) · ปุ่มตามสถานะ: ร่าง(เจ้าของ) = ยกเลิก · แก้ไข · บันทึกผล / บันทึกผลแล้ว(เจ้าของ/role-mgr-sales) = ยกเลิกเอกสาร · พิมพ์ · ดาวน์โหลด PDF · ปิด
- รายละเอียด: แบนเนอร์ (ร่าง: ตอบ x/10 · คะแนนต่ำ: แจ้งผู้จัดการแล้ว · ยกเลิก: เหตุผล) · ข้อมูลเอกสาร · ลูกค้า + ผู้ติดต่อ · ตารางคะแนน 3 กลุ่ม (✓ · ข้อ ≤ 2 สีแดง) · Additional Feedback · เอกสารแนบ · ข้อมูลระบบ
- PDF Preview: iframe A4 จาก `print/form.tpl.html` + `docPrintData()` (FN-07) · ดาวน์โหลด/พิมพ์
- ลายเซ็น / อนุมัติ: block มาตรฐาน §6.1 — สาย DOA "ไม่มี · 0 ขั้น" (DEC-03 · TODO: DOA engine) · timeline บันทึกผล → ผลลัพธ์
- ประวัติ: append-only

## §1.3 Microcopy หลัก
ปุ่ม: สร้างแบบประเมิน · บันทึกแบบร่าง · บันทึกผลแบบประเมิน · ยกเลิกเอกสาร · toast: บันทึกร่างแล้ว · บันทึกผลแล้ว · ยกเลิกเอกสารแล้ว · กรุณากรอกข้อมูลให้ครบถ้วน · ป้ายช่องข้อมูลใช้ "ไทย (English ตามกระดาษ)" · หัวข้อคะแนนเป็นภาษาอังกฤษตามกระดาษ (DEC-14)

## §1.4 Field Map — หัวข้อคะแนน (ถ้อยคำตรงกระดาษ → คีย์)
| กลุ่ม | หัวข้อ | คีย์ |
|---|---|---|
| COMMUNICATION & RESPONSIVENESS | Communication clarity | `score.q1` |
| COMMUNICATION & RESPONSIVENESS | Response time to inquiries | `score.q2` |
| COMMUNICATION & RESPONSIVENESS | Follow-up consistency | `score.q3` |
| DOCUMENTATION & EXECUTION | Accuracy of documents | `score.q4` |
| DOCUMENTATION & EXECUTION | Timeliness of document submission | `score.q5` |
| DOCUMENTATION & EXECUTION | Shipment coordination support | `score.q6` |
| DOCUMENTATION & EXECUTION | Effectiveness in resolving issues | `score.q7` |
| DOCUMENTATION & EXECUTION | Proactive service updates | `score.q8` |
| PROFESSIONALISM | Professionalism of our team | `score.q9` |
| PROFESSIONALISM | Overall service satisfaction | `score.q10` |
| — | Month | `period_month` |
| — | Company Name | `customer_id` / `customer_name_snapshot` |
| — | Contact Person | `contact_person` |
| — | Additional Feedback | `comment` |
