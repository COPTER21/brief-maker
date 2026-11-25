# PRINT SPEC — แบบฟอร์มยืมสินทรัพย์ (ALN)

> โหมด **Replica** (แบบฟอร์มลูกค้า FM-ASM-04) · thai-doc-pdf-generator v2.2 · ไฟล์คู่: `แบบฟอร์มยืมสินทรัพย์_template.html` · `form.tpl.html` · `profile.json` · `*.data.json`
> **[NO-BROWSER]** รอบนี้ไม่ได้ render PDF (ไม่มี Chromium บนเครื่อง) — ต้องรัน render_states.py + compare_original.py รอบเต็มบนเครื่องที่มี browser

## 1. สรุป
- **ประเภทเอกสาร:** แบบฟอร์มยืมสินทรัพย์ / Asset Borrowing Form
- **ขนาด:** A4 แนวตั้ง · **ฟอนต์:** Sarabun (ฝัง) · หมึกเดียวตาม profile
- **จำนวนหน้า (ออกแบบ):** 1 หน้าทุกสถานะ (ต้นฉบับ 1 หน้า · 11 แถว) — ประเมินจากโครง: หัว ~45mm + ตาราง 14 แถว×7mm ~110mm + ลงชื่อ 2 แถว ~50mm + ส่วนรับคืน ~35mm + footer < 273mm · ยังไม่ได้ยืนยันด้วย PDF

## 2. Field Mapping
ดู §A Data contract ท้ายไฟล์ (13 ช่องตาม FORM_SPEC 1:1)

## 3. กติกาคำนวณ / ตรวจ
- ไม่มีสูตรเงิน · จำนวน `#,##0` · qty_lent ≤ qty_requested · return_date ≥ borrow_date (DEC-04/12/13)

## 4. กติกาการพิมพ์
- thead ซ้ำทุกหน้า · tr ไม่ตัดกลาง · `.signs-block` ไม่ตัดข้ามหน้า · ลายเซ็น + ส่วนรับคืน + footer ชิดล่าง (.doc-bottom)
- ถ้าภายหลังพบเกิน A4 (แถวจริง > ~20) → R10 ออกแบบ 2 หน้า (`.page-break` ก่อนบล็อกลงชื่อ · "หน้า 1/2") แล้ว `--max-pages 2`

## 5. วิธี build ใหม่
```bash
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "แบบฟอร์มยืมสินทรัพย์"
python3 $TD/scripts/compare_original.py ../orig/SAMPLE.pdf out/approved.pdf -o out/compare --region 0:0.62
```

## 6. Checklist
- [x] parity IDENTICAL 6/6 · ไม่มี {{}} หลง · ไม่มี key ขาด (render_doc)
- [ ] A4 พอดี — [NO-BROWSER] รอ render
- [x] ลายเซ็นครบสาย (ผู้ยืม + ขั้น DOA) + ส่วนรับคืน 2 ช่อง

## 7. (Replica) ต้นฉบับลูกค้า + ความต่างที่ตั้งใจ
- ต้นฉบับ: `4. FM-ASM-04 แบบฟอร์มยืมสินทรัพย์.xlsx` (→ orig/SAMPLE.pdf ผ่าน LibreOffice) · Doc No. FM-ASM-04 · Rev.00 : 01/07/2569
- Profile: form_fs 9pt · title 14pt · logo ชิดซ้าย 12mm · grid row 7mm · หัวตารางพื้นขาว
- ความต่าง (ตั้งใจ): ชื่อเอกสารกึ่งกลาง (ต้นฉบับชิดขวาข้างโลโก้ — replica.css ไม่มี token ชิดขวา) · ช่องลงชื่อส่วนยืมวนตาม DOA (ผู้ยืม + ขั้น) พร้อมคำตัดสิน ☐ ให้ยืม ☐ ไม่ให้ยืม · ข้อความ "ส่งในระบบ/พิจารณาในระบบ/รับคืนในระบบ" แทนลายมือ · footer เลขที่ + CUBE NATIVE · โลโก้ = Organization (ตัวอย่างใช้ placeholder)
- compare_original: **[NO-BROWSER] ข้าม** (ไม่มี PDF ของแบบพิมพ์) — ภาพต้นฉบับ orig/page-1.png

## 8. (Replica) Data contract + สถานะที่ทดสอบ
- parity JS ↔ Python: IDENTICAL 6/6
- สถานะ: draft · approved · rejected · returned (รับคืนแล้ว) · long-14rows (dense) · approved-doa6steps (7 ช่อง 4+3) → HTML ใน out/ · จำนวนหน้า: ออกแบบ 1 หน้า (รอ PDF ยืนยัน)

## 9. (Replica) print_config
```json
{
  "doc_type": "ALN",
  "mode": "replica",
  "template_ref": "form.tpl.html",
  "template_version": "v1",
  "profile_ref": "profile.json",
  "form_code": "FM-ASM-04",
  "revision": "Rev.00 : 01/07/2569",
  "paper": "A4-portrait",
  "min_rows": 11,
  "dense_when_rows_over": 11,
  "header_source": "organization_snapshot_at_numbering",
  "sign_boxes": [
    { "box": "requester", "label": "ผู้ยืม", "show_date": true },
    { "box": "doa_step:*", "label": "from_doa_step", "show_decision": true, "show_date": true }
  ],
  "return_boxes": [
    { "box": "return_sender", "label": "ผู้ส่งคืน", "source": "return_record.returned_by", "show_date": true },
    { "box": "return_receiver", "label": "ผู้รับคืน", "source": "return_record.received_by", "show_date": true }
  ],
  "decision_words": {
    "default": { "approve": "อนุมัติ", "reject": "ไม่อนุมัติ" },
    "by_role": { "role-mgr-acc": { "approve": "ให้ยืม", "reject": "ไม่ให้ยืม" } }
  },
  "footer_left": "เลขที่ {doc.no} · (ร่าง) · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE",
  "footer_right": "Doc. No. : {form_code} · {revision}",
  "sign_layout": {
    "source": "approval_chain snapshot (ผู้ยืม + จำนวนขั้นตามที่ตั้งใน DOA)",
    "max_per_row": 4,
    "split": "even",
    "dense_when_steps_over": 4,
    "keep_together": true
  }
}
```


## §A DATA CONTRACT — แบบฟอร์มยืมสินทรัพย์ (ALN)

> สัญญาข้อมูลระหว่าง backend ↔ template (`form.tpl.html`) · ใช้ทั้ง prototype (tpl_render.js) และ server (render_doc.py)
> กติกา: ค่าแสดงทุกตัวเป็น string ที่จัดรูปแล้ว · boolean ใช้เป็นเงื่อนไขเท่านั้น · checkbox = "☑"/"☐" · ว่าง = "" · ไม่มี {} ว่าง
> ตรวจ: `python scripts/parity_check.py form.tpl.html *.data.json` → IDENTICAL 6/6

| key | Source (entity.field / engine) | ตัวอย่าง (สมมติ) | หมายเหตุ |
|---|---|---|---|
| `company.name` · `company.logo` | Organization → header_snapshot (ตอนออกเลข) | `บริษัท ตัวอย่าง จำกัด` · data URI | ไม่ดึงสดหลังออกเลข |
| `doc.title` · `doc.no` · `doc.is_draft` | ค่าคงที่ · ENG-DOC-NUM (ALN) · status = draft | `แบบฟอร์มยืมสินทรัพย์` · `ALN-2569-0007` | ออกเลขตอนบันทึกครั้งแรก (DEC-10) |
| `doc.form_code` · `doc.revision` | F-DOCCFG `print_config` | `FM-ASM-04` · `Rev.00 : 01/07/2569` | |
| `employee.name` · `employee.position` · `employee.dept` | Employee.full_name · Employee.position · OrgUnit.name (ผู้ยืม) | `สมชาย ใจดี` | snapshot ตอนส่ง |
| `purpose` | asset_borrow.purpose | `จัดอบรมสินค้าให้ลูกค้า …` | |
| `lines[].no` | ลำดับรายการ | `1` | |
| `lines[].asset_name` | Asset.name (ตามทะเบียนที่เลือก) | `เครื่องคอมพิวเตอร์โน้ตบุ๊ก` | |
| `lines[].asset_code` | asset_borrow_line.asset_code → Asset Master | `AST-IT-0012` | ห้ามซ้ำในใบเดียว |
| `lines[].qty_requested` · `lines[].qty_lent` | asset_borrow_line.qty_requested / qty_lent | `20` · `15` | `#,##0` · qty_lent ว่างจนผู้ให้ยืมพิจารณา · ≤ qty_requested |
| `lines[].borrow_date` · `lines[].return_date` | asset_borrow_line.borrow_date / return_date | `13 ต.ค. 69` | วันที่ย่อไทย พ.ศ. 2 หลัก · return ≥ borrow |
| `lines[].remark` | asset_borrow_line.remark | | |
| `sign_rows[].signs[]` → `role` · `name` · `position` · `date` · `decision{approve_box,reject_box,approve_word,reject_word}` | ผู้ยืม + `approval_chain` (DOA snapshot) via sign_rows.py | `ผู้ให้ยืม` · `☑ ให้ยืม ☐ ไม่ให้ยืม` | จำนวนช่อง = 1 + จำนวนขั้น DOA · แถวละ ≤4 · คำตัดสินตาม role |
| `return_signs[]` → `role` · `name` · `position` · `date` | return_record.returned_by / received_by (+ เวลา) | `ผู้ส่งคืน` · `ผู้รับคืน` | 2 ช่องคงที่ตามกระดาษ (ไม่ใช่ขั้น DOA) · ว่าง = เส้นประวันที่ |
| `layout.dense` | lines.length > 11 หรือ ขั้น DOA > 4 | `true` | |
