# PRINT SPEC — แบบฟอร์มใบแจ้งซ่อมสินทรัพย์ (RPR · FM-ASM-03)

> เอกสารประกอบสำหรับ Dev — แนบคู่ FRD/UI Brief ของ F-TMP-001
> ไฟล์คู่: `FM-ASM-03_template.html` (master, fonts ฝัง) · `form.tpl.html` (logic-less) · `*.data.json` 5 สถานะ · `out/*.html`
> **โหมด:** Replica (แบบฟอร์มลูกค้า) · [NO-BROWSER บนเครื่อง user] PDF 5 สถานะ render ด้วย render_pdf.py ของสกิลบน Chromium ใน cloud container

## 1. สรุป
- **ประเภทเอกสาร:** แบบฟอร์มใบแจ้งซ่อมสินทรัพย์ / Asset Repair Request
- **ขนาด:** A4 แนวตั้ง · ฟอนต์ Sarabun (ฝังใน HTML) · หมึกเดียวตาม profile
- **จำนวนหน้าเป้าหมาย:** 1 หน้าทุกสถานะ (`--max-pages 1`) — ต้นฉบับ 1 หน้า · แถวสูงสุดที่ทดสอบ 14+8 แถว (dense) — ประเมินความสูง ≈ 230mm < 267mm พื้นที่พิมพ์ → PDF จริง 1 หน้าทุกสถานะ

## 2. Field Mapping
| ช่องในเอกสาร | Source (entity.field) | Format | บังคับ | หมายเหตุ |
|---|---|---|---|---|
| เลขที่ | ENG-DOC-NUM (RPR) | `RPR-YYYY-NNNN` | ✓ | ออกตอนบันทึกครั้งแรก (DEC-11) |
| ชื่อ-นามสกุล · ตําแหน่ง · ฝ่าย/แผนก | Employee / Position & Tier / Department (snapshot) | — | ✓ | PDPA |
| รายการ (loop 10 แถว) | RepairRequest.items[] | ลำดับ 1–10 พิมพ์ตายตัว | ≥1 แถว | ทะเบียนสินทรัพย์ · จำนวน (>0) · อาการชำรุด · สถานที่ตั้ง · หมายเหตุ |
| ลงชื่อ…ผู้แจ้งซ่อม · วันที่…เดือน…พ.ศ… | ผู้แจ้ง + submitted_at | วัน / เดือนเต็ม / พ.ศ. | ✓ เมื่อส่ง | DEC-13 แสดงซ้ำในแถวลงชื่อล่าง |
| ประวัติการซ่อม (loop 6 แถว) | RepairRequest.history[] | วันที่ไทยย่อ · จำนวนครั้ง | — | ผู้ตรวจสอบกรอก |
| ผู้แจ้งซ่อม · ผู้ตรวจสอบ · ผู้อนุมัติ | ผู้แจ้ง + approval_chain (DOA) | "ส่งในระบบ / พิจารณาในระบบ วันที่ เวลา" | ✓ | 1 ช่องต่อขั้น DOA (ไม่ fix) |

## 3. กติกาคำนวณ
- ไม่มีสูตร/ค่าคงที่บนกระดาษ · `layout.dense` = items > 10 หรือ history > 6 หรือ DOA > 4 ขั้น

## 4. กติกาการพิมพ์
- หัวตารางซ้ำ (`thead`) · ไม่ตัดแถวกลาง · บล็อกลงชื่อ `.signs-block` ไม่ตัดข้ามหน้า · footer ซ้าย "เลขที่ … · ร่าง · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE" ขวา "Doc. No. : FM-ASM-03"

## 5. วิธี build ใหม่
```bash
python3 make_data.py
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "แบบฟอร์มใบแจ้งซ่อมสินทรัพย์" --max-pages 1
python3 $TD/scripts/compare_original.py ../orig/SAMPLE.pdf out/approved.pdf -o out/compare --region 0:0.75
```

## 7. (Replica) ต้นฉบับลูกค้า + ความต่างที่ตั้งใจ
- ต้นฉบับ: `3. FM-ASM-03 แบบฟอร์มใบแจ้งซ่อมสินทรัพย์.xlsx` · Doc No. FM-ASM-03 · ไม่มี Rev.
- Profile: font 9pt · title 16pt · โลโก้ซ้าย 11mm · ระยะแถวกระชับ
- ความต่างที่ตั้งใจ: ชื่อเอกสารอยู่กลางใต้โลโก้ (ต้นฉบับอยู่ขวาของโลโก้) · ช่องลงชื่อล่างเป็นตารางกรอบ 1 ช่องต่อขั้น DOA + คำตัดสิน · footer เลขที่เอกสาร · ข้อความ "ส่งในระบบ/พิจารณาในระบบ" แทนลายมือ · โลโก้มาจาก Organization (ตัวอย่างใช้ placeholder)
- compare_original: score 0.139 **WARN** · region 0:0.75 · `out/compare/compare_side.png` — เหตุผล: ภาพต้นฉบับจาก Excel scale 56% ฟอนต์ไทยแสดงเป็นกล่อง และสเกลเนื้อหาต่างกัน → line match ต่ำ · ดูภาพวางคู่แล้ว ลำดับบล็อก/คอลัมน์/ถ้อยคำตรงครบ

## 8. (Replica) Data contract + สถานะที่ทดสอบ
- contract: `FM-ASM-03_data-contract.md`
- parity JS ↔ Python: IDENTICAL 5/5
- สถานะ: draft (2 รายการ ไม่มีประวัติ) · approved (3 + ประวัติ 2) · rejected (ผู้ตรวจสอบไม่ผ่าน) · long-14rows (14 + ประวัติ 8 · dense) · approved-doa6steps (7 ช่อง 4+3) → ไม่มี `{{}}` หลง · PDF 1 หน้าทุกสถานะ

## 9. (Replica) print_config
```json
{
  "doc_type": "RPR",
  "mode": "replica",
  "template_ref": "form.tpl.html",
  "template_version": "v1",
  "profile_ref": "profile.json",
  "form_code": "FM-ASM-03",
  "revision": "",
  "paper": "A4-portrait",
  "min_rows": 10,
  "min_rows_by_group": { "items": 10, "history": 6 },
  "dense_when_rows_over": 10,
  "header_source": "organization_snapshot_at_numbering",
  "sign_boxes": [
    { "box": "requester", "label": "ผู้แจ้งซ่อม", "show_date": true, "also_inline": "ลงชื่อ…ผู้แจ้งซ่อม ใต้ตารางรายการ (DEC-13)" },
    { "box": "doa_step:*", "label": "from_doa_step", "show_decision": true, "show_date": true }
  ],
  "decision_words": {
    "default": { "approve": "อนุมัติ", "reject": "ไม่อนุมัติ" },
    "by_role": { "role-line-manager": { "approve": "ตรวจสอบแล้ว", "reject": "ไม่ผ่านการตรวจสอบ" } }
  },
  "config_reads": {},
  "footer_left": "เลขที่ {doc.no} · (ร่าง) · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE",
  "footer_right": "Doc. No. : {form_code}",
  "sign_layout": { "source": "approval_chain snapshot (ผู้แจ้งซ่อม + จำนวนขั้นตามที่ตั้งใน DOA)", "max_per_row": 4, "split": "even", "dense_when_steps_over": 4, "keep_together": true }
}
```
