# 01_UI — F-TMP-008
> Source of truth = `01_Prototype/feature.html` (html-generator-v9.4 · Q-form) · ช่องตรง FORM_SPEC 1:1 (DEC-08)

## §1.1 Page Inventory
| ID | Route | หน้าที่ |
|---|---|---|
| P-01 | `#/csat-mt` | รายการ (no-scorecard · ตัวเลขเป็น badge ≤ 2 · ค้นหา · กรอง สถานะ/ปี · CSV · pagination 25) |
| P-02 | `#/csat-mt/create` · `#/csat-mt/edit/:id` | drawer wide wizard 4 ขั้น: คะแนนรายช่องทาง › ภาพรวมและข้อเสนอแนะ › เอกสารแนบ › ตรวจสอบและยืนยัน |
| P-03 | `#/csat-mt/view/:id` | drawer 920 · tabs รายละเอียด › PDF Preview › ลายเซ็น / อนุมัติ › ประวัติ |
| M-01..03 | modal | ยืนยันสรุป · ยกเลิก (เหตุผล) · ทิ้งข้อมูล |

## §1.2 P-01 คอลัมน์ (1 cell = 1 บรรทัด)
เลขที่ · ครั้งที่ · เอกสารประเมิน วันที่ · ผู้สรุป · ช่องทางที่ประเมิน (n/15) · ผ่านมาตรฐาน · ต่ำกว่ามาตรฐาน · ต่ำกว่า 80% · สถานะเอกสาร · ลายเซ็น x/y (ผู้สรุป) · ⋮ (ดูรายละเอียด · แก้ไข[ร่างของตน] · พิมพ์ · ยกเลิกเอกสาร)

## §1.3 P-02 ฟิลด์ (ป้ายตามกระดาษ)
| ขั้น/การ์ด | ป้าย | key | control | กติกา |
|---|---|---|---|---|
| 1 ① | ครั้งที่ | round_no | input text inputmode=numeric | required · จำนวนเต็ม ≥ 1 · ซ้ำในปี = เตือน |
| 1 ① | เอกสารประเมิน วันที่ | assessment_date | bedate (พ.ศ.) | required · ≤ วันนี้ |
| 1 ① | สรุปข้อมูล วันที่ | summary_date | bedate (พ.ศ.) ค่าเริ่มวันนี้ | required · ≥ assessment_date |
| 1 ② | หัวข้อประเมิน | criteria[].topic | ข้อความจาก config (อ่านอย่างเดียว) | snapshot |
| 1 ② | คะแนน (1-5) | criteria[].max_score | ข้อความจาก config | snapshot |
| 1 ② | หัวคอลัมน์ช่องทาง | channels[].name | ข้อความจาก config | snapshot |
| 1 ② | คะแนนรายช่องทาง | criteria[].scores[channel_id] | input text inputmode=numeric maxlength 1 | จำนวนเต็ม 1–5 · ว่าง = ยังไม่ประเมิน |
| 1 ② | รวม (แถวรวม) | max_total · channels[].total | ข้อความคำนวณสด (soft update ไม่ rebuild) | — |
| 1 ② | % (แถว 100%) | channels[].pct | ข้อความคำนวณสด + สีตามผล | "ยังไม่ครบ" / "ไม่ได้ประเมิน" |
| 1 ② | ผลเทียบมาตรฐาน | channels[].status | แถบสรุปจำนวนต่อกลุ่ม + pill | — |
| 2 ① | ช่องทางที่ ผ่านมาตรฐาน … ได้แก่ | summary.pass_channels | ข้อความคำนวณ | แก้ไม่ได้ |
| 2 ① | ข้อความแนะนำ (กลุ่มผ่านมาตรฐาน) | summary.pass_note | textarea ค่าเริ่มจาก config | — |
| 2 ① | ช่องทางที่ ต่ำกว่ามาตรฐานเล็กน้อย … ได้แก่ | summary.below_channels | ข้อความคำนวณ | แก้ไม่ได้ |
| 2 ① | ข้อความแนะนำ (กลุ่มต่ำกว่ามาตรฐานเล็กน้อย) | summary.below_note | textarea | — |
| 2 ① | ช่องทางที่ ต่ำกว่า 80% ได้แก่ | summary.far_channels | ข้อความคำนวณ | แก้ไม่ได้ |
| 2 ① | ข้อความแนะนำ (กลุ่มต่ำกว่า 80%) | summary.far_note | textarea (แสดงตัวหนาแดง) | — |
| 2 ② | ข้อเสนอแนะ | recommendations[].text | input ต่อข้อ + เพิ่ม/ลบ | ≥ 1 ข้อตอนยืนยัน |
| — | ผู้สรุปการประเมิณ / ตำแหน่ง | summarizer.name · summarizer.position | ระบบใส่ (ผู้สร้าง) | snapshot |

## §1.4 P-03 แท็บ
- รายละเอียด: แบนเนอร์ตามสถานะ (ร่าง/ยกเลิก/มีช่องทางต่ำกว่า 80%) · ข้อมูลเอกสาร · ตารางคะแนน + แถวรวม/% · ภาพรวมโดยสรุป · ข้อเสนอแนะ · เอกสารแนบ · ข้อมูลระบบ
- PDF Preview: iframe srcdoc จาก `form.tpl.html` + `docPrintData(r)` · 2 หน้า · ดาวน์โหลด/พิมพ์
- ลายเซ็น / อนุมัติ: summary card (ไม่มีขั้นอนุมัติ · x/1) + timeline สร้าง → ยืนยันสรุป → ผลลัพธ์ · ปุ่ม "ยืนยันสรุป" inline เฉพาะเจ้าของใบร่าง
- ประวัติ: append-only (รวมบันทึกแจ้งเตือนช่องทางต่ำกว่า 80%)

## §1.5 ปุ่มหัว drawer ตามสถานะ
ร่าง (เจ้าของ) = ยกเลิก · แก้ไข · ยืนยันสรุป · สรุปแล้ว (เจ้าของ/admin) = ยกเลิกเอกสาร · ยกเลิก = ไม่มีปุ่ม

## §1.6 UI Standard
CUBE Warm Light (html-generator-v9.4) · คน = วงกลม icon · backdrop ปิดด้วย mousedown · Esc: ปฏิทิน/combobox → modal → drawer · วันที่ใช้ bedate (Rule #114)
