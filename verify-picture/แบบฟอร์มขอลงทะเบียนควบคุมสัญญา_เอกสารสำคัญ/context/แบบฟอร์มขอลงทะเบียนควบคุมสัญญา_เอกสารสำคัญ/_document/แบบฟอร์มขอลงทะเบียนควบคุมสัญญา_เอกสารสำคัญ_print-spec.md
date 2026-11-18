# PRINT SPEC — แบบฟอร์มขอลงทะเบียนควบคุมสัญญา/เอกสารสำคัญ (CTR)
> โหมด **Replica** · ไฟล์คู่: `form.tpl.html` (logic-less) · `CTR_template.html` (build แล้ว ฝัง Sarabun) · `profile.json` · `print_config.json` · `*.data.json` 5 สถานะ
> ⚠ [NO-BROWSER] เครื่องที่ทำไม่มี browser → ยังไม่มี PDF / จำนวนหน้า / compare_original — ต้องรัน render_states.py + compare_original.py รอบเต็มบนเครื่องที่มี browser ก่อนส่งมอบจริง

## 1. สรุป
- A4 แนวตั้ง · Sarabun · หมึกเดียวตาม profile · 1 หน้า (ต้นฉบับ 1 หน้า)
- มติอ้างอิง: DEC-06 (1:1) · DEC-07 (ลายเซ็นแถวล่างต่อขั้น DOA) · DEC-10 (เลข CTR) — ทั้งหมด AI-DEFAULT

## 2. Field Mapping
ดู `CTR_data-contract.md`

## 3. กติกาคำนวณ
- ไม่มีสูตร · `contract_period` = จัดรูปวันที่เริ่ม–สิ้นสุดเป็นบรรทัดเดียวที่ backend · end ≥ start

## 4. กติกาการพิมพ์
- บล็อกลงชื่อ `.signs-block` ไม่ตัดข้ามหน้า · DOA > 4 ขั้น → `layout.dense` · แถวละ ≤ 4 ช่อง
- กล่อง "ส่วนของผู้ดูแลสัญญา" อยู่ใต้บล็อกลงชื่อ (ตำแหน่งตามกระดาษ) ใน `.doc-bottom`

## 5. วิธี build ใหม่
```bash
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "แบบฟอร์มขอลงทะเบียนควบคุมสัญญา/เอกสารสำคัญ" --max-pages 1
python3 $TD/scripts/compare_original.py ../orig/SAMPLE.pdf out/approved.pdf -o compare --region 0:0.62
```

## 6. Checklist
- [x] ถ้อยคำตามกระดาษทุกบรรทัด (ยึด content.html + document.xml)
- [x] parity JS↔Python IDENTICAL 5/5 · ไม่มี `{{}}` หลง · ไม่มี key ขาด
- [ ] A4 1 หน้าทุกสถานะ — รอรันบนเครื่องที่มี browser (ประเมินความสูง ~230mm < 269mm พื้นที่ใช้ได้)
- [ ] compare_original — รอ browser

## 7. (Replica) ต้นฉบับ + ความต่างที่ตั้งใจ
- ต้นฉบับ: `1. FM-AGM-01 แบบฟอร์มลงทะเบียนควบคุมสัญญา.docx` · Doc. No. FM-AGM-01 · Rev.00 : 01/07/2569 (footer docx)
- Profile: form_fs 10pt · form_logo_h 14mm · form_row_gap 7px
- ความต่างที่ตั้งใจ: ลายเซ็น 3 จุด (ผู้รับผิดชอบ · หัวหน้า/ผู้จัดการ · ผู้เชี่ยวชาญด้านบริหารสัญญา) → แถวล่างวนจาก DOA (จำนวนตาม DOA) · ช่องผู้อนุมัติมี ☐ คำตัดสิน (หัวหน้า: อนุมัติ/ไม่อนุมัติ · ผู้เชี่ยวชาญ: รับทราบ/ส่งกลับแก้ไข) · ข้อความ "ส่งในระบบ/พิจารณาในระบบ" แทนลายมือ · footer ซ้าย เลขที่ CTR · ตัวเลือกข้อ 1–2 จัดเรียง inline (กระดาษเป็น 3 คอลัมน์)
- compare_original: ไม่ได้รัน ([NO-BROWSER] ไม่มี approved.pdf) · ภาพต้นฉบับที่ได้ไม่มีฟอนต์ไทย (□) ใช้ดูตำแหน่งเท่านั้น

## 8. (Replica) Data contract + สถานะ
- parity: IDENTICAL 5/5
- สถานะ: ร่าง · อนุมัติแล้ว · ไม่อนุมัติ (จุดประสงค์ แก้ไข + สาเหตุ) · ข้อความยาว · DOA 6 ขั้น (7 ช่อง 4+3 dense) → จำนวนหน้า: ยังไม่วัด ([NO-BROWSER])

## 9. print_config
ดู `print_config.json` (doc_type CTR · sign_boxes requester + doa_step:* · decision_words.by_role role-compliance)
