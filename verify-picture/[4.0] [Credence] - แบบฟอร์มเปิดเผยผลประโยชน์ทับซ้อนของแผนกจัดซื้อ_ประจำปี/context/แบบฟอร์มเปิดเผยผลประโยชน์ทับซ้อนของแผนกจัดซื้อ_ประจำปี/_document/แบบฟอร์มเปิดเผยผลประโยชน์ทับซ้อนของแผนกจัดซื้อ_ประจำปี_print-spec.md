# PRINT SPEC — แบบฟอร์มเปิดเผยผลประโยชน์ทับซ้อนของแผนกจัดซื้อ ประจำปี (COI · FM-PUR-04)

> เอกสารประกอบสำหรับ Dev — แนบคู่กับ FRD/Brief ของ F-TMP-006 · **โหมด Replica** · มติทั้งหมด AI-DEFAULT รอลูกค้ายืนยัน
> ไฟล์คู่: `FM-PUR-04_template.html` (master, fonts ฝัง) · `out/<state>.html` (5 สถานะ) · **ไม่มี PDF — [NO-BROWSER]**

## 1. สรุป
- **ประเภทเอกสาร:** แบบฟอร์มเปิดเผยผลประโยชน์ทับซ้อนของแผนกจัดซื้อ ประจำปี / Annual Conflict of Interest Disclosure Form (Purchasing)
- **ขนาด:** A4 แนวตั้ง 1 หน้า (ต้นฉบับ 1 หน้า · ไม่มีแถวซ้ำยาว → ไม่ใช้ R10)
- **ฟอนต์:** Sarabun 10pt (หัวเรื่อง 14pt) · ไม่ต่ำกว่า 8pt ทุกสถานะ
- **หมึก:** หมึกเดียวตาม profile (Replica)
- **ความลับ:** Confidential — ปุ่มพิมพ์/PDF เฉพาะเจ้าของ · ผู้พิจารณาของใบ · role-compliance · footer มีคำ "เอกสารลับ"

## 2. Field Mapping
ดู `COI_data-contract.md` (key ↔ entity.field ครบทุกช่อง)

## 3. กติกาคำนวณ
- ไม่มีสูตร · ปี = `CoiDisclosureConfig.current_year` snapshot ลงใบ · ☑ ไม่มี/มี จาก `has_conflict` · รายละเอียดแยกบรรทัด เติมว่างครบ 3

## 4. กติกาการพิมพ์
- A4 · ลายเซ็น+footer ชิดล่าง (.doc-bottom) · `.signs-block` ไม่ตัดข้ามหน้า · dense เมื่อรายละเอียด > 5 บรรทัด หรือ DOA > 4 ขั้น

## 5. วิธี build ใหม่
```bash
python3 $TD/scripts/render_doc.py form.tpl.html <state>.data.json -o out/_<state>.body.html --strict
python3 $TD/scripts/build_html.py out/_<state>.body.html --title "<state>" --mode replica --profile profile.json -o out/<state>.html
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --max-pages 1   # ต้องมี browser
```

## 6. Checklist
- [x] ไม่มี `{{}}` หลง (5/5) · missing key 0 (`--strict`)
- [x] ลายเซ็นครบตาม signs (2 · 2 · 2 · 3 · 4+3)
- [ ] A4 พอดี 1 หน้า ทุกสถานะ — **ยังไม่ได้วัด [NO-BROWSER]** (ประมาณการ: ยาว 12 บรรทัด + 3 ช่อง ≈ 230mm · DOA 6 ขั้น ≈ 205mm ต่ำกว่าพื้นที่พิมพ์) → รันรอบเต็มบนเครื่องที่มี browser ด้วย `--max-pages 1` ถ้าเกินให้ออกแบบ 2 หน้าตาม R10 (ตัดก่อนกรอบข้อคิดเห็น)

## 7. (Replica) ต้นฉบับลูกค้า + ความต่างที่ตั้งใจ
- ต้นฉบับ: `orig/4. FM-PUR-04 แบบฟอร์มเปิดเผยผลประโยชน์ทับซ้อนประจำปี 2569.docx` · Doc No. FM-PUR-04 · REV.00 : 01/07/2569
- Profile: `profile.json` — form_fs 10pt · title 14pt · logo 14mm กลาง · indent 0 · para gap 10px
- ความต่างจากกระดาษ (ตั้งใจ):
  1. "ประจำปี 2569" → "ประจำปี {{doc.year}}" (ตัวแปรรอบปี · DEC-04/12)
  2. ช่อง "ลงชื่อ: … วันที่: …" กลางหน้า + ช่องลงชื่อในกรอบผู้บังคับบัญชา → ย้ายเป็นแถวลงชื่อล่าง B6 (ผู้เปิดเผย + 1 ช่อง/ขั้น DOA) · ข้อความ "ส่งในระบบ/พิจารณาในระบบ" แทนลายมือ (DEC-07)
  3. คำ "ฝ่ายกฎหมาย" ใต้ช่องลงชื่อ → ใช้ป้ายขั้นจาก DOA (ค่าเริ่ม "ผู้บังคับบัญชา") · ถ้า DOA กลางเพิ่มขั้น role-compliance จะพิมพ์ "ฝ่ายกฎหมาย" เป็นช่องที่ 3 (ดูสถานะ long-12lines) — OQ ลูกค้า
  4. กรอบ "ข้อคิดเห็นของผู้บังคับบัญชา" แสดงข้อคิดเห็นรายขั้น (ป้ายขั้น : ข้อความ) เติมบรรทัดว่างครบ 3
  5. footer ซ้าย "เลขที่ … · ร่าง · แทนฉบับ … · เอกสารลับ · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE"
- compare_original: **[NO-BROWSER] ข้าม** (ต้องใช้ approved.pdf) — ไม่มีคะแนน · ต้องรันรอบเต็ม + ดู compare_side.png

## 8. (Replica) Data contract + สถานะที่ทดสอบ
- parity JS ↔ Python: IDENTICAL 5/5
- สถานะ: draft (☑ มี · ร่าง · ช่องวันที่เส้นประ) · approved (☑ ไม่มี · ☑ รับทราบ) · rejected (☑ มี · ☑ ส่งกลับแก้ไข) · long-12lines (รายละเอียด 12 บรรทัด · dense · 3 ช่อง · แทนฉบับเดิม) · approved-doa6steps (7 ช่อง 4+3 · dense) → จำนวนหน้า: ยังไม่วัด [NO-BROWSER] (ออกแบบ 1 หน้า)

## 9. (Replica) print_config
ดู `print_config.json`
