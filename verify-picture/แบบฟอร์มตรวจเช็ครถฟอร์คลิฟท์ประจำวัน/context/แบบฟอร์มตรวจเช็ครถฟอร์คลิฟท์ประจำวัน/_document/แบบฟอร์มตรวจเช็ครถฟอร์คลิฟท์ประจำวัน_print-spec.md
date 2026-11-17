# PRINT SPEC — แบบฟอร์มตรวจเช็ครถฟอร์คลิฟท์ประจำวัน (FLI)

> เอกสารประกอบสำหรับ Dev — แนบคู่กับ FRD/Brief ของ F-TMP-002
> ไฟล์คู่: `FM-WHS-04_template.html` (template build แล้ว · fonts ฝัง) · `out/<state>.html` (5 สถานะ)
> **โหมด:** Replica (แบบฟอร์มลูกค้า) · **2 หน้า** (thai-doc R10)
> ⚠ **[NO-BROWSER]** รอบนี้เครื่องไม่มี browser → ยังไม่ได้ render PDF / `_states_sheet.png` / compare_original — ต้องรัน `render_states.py --max-pages 2` + `compare_original.py` บนเครื่องที่มี browser ก่อนส่งมอบจริง

## 1. สรุป
- **ประเภทเอกสาร:** แบบฟอร์มตรวจเช็ครถฟอร์คลิฟท์ประจำวัน / FORKLIFT DAILY INSPECTION CHECKLIST
- **ขนาด:** A4 แนวตั้ง (210×297mm) ขอบ 14mm · **2 หน้า ทุกสถานะ**
- **ฟอนต์:** Sarabun ฝัง · เนื้อ 8.5pt (ไม่ต่ำกว่า 8pt) · หัวเรื่อง 11pt
- **หมึก:** ตาม profile ลูกค้า (`profile.json`)

## 2. Field Mapping
| ช่องในเอกสาร | Source | Format | บังคับ | หมายเหตุ |
|---|---|---|---|---|
| หัวกระดาษ (โลโก้ · ชื่อบริษัท · ที่อยู่) | Organization snapshot | — | ✓ | ตอนออกเลข |
| ประเภทรถ ☐ น้ำมัน ☐ ไฟฟ้า | inspection.vehicle_type | ☑/☐ | ✓ | |
| ประจำเดือน | inspection.inspection_month | เดือนไทย พ.ศ. | ✓ | |
| ตาราง 3 กลุ่ม × วันที่ 1–31 | ForkliftChecklistConfig.items + inspection_results | ✓ / ✗ / ว่าง | — | ดู data contract |
| ลงชื่อ ผู้ตรวจสอบ | ผู้สร้างใบ | "ส่งในระบบ วันที่ เวลา" | ✓ | |
| ลงชื่อ หัวหน้างานตรวจสอบ (+ขั้น DOA อื่น) | approval_chain | ☑ ตรวจสอบแล้ว / ☑ ส่งกลับแก้ไข + "พิจารณาในระบบ …" | ✓ | 1 ช่องต่อขั้น DOA |
| Doc. No. / Rev. | print_config | `FM-WHS-04 · Rev.00 : 01/07/2569` | ✓ | footer ขวา + "หน้า n/2" |

## 3. กติกาคำนวณ
- ไม่มีสูตรตัวเลข · ช่องวันที่ > จำนวนวันของเดือน = ว่าง · วันในอนาคต = ว่าง (DEC-15)

## 4. กติกาการพิมพ์ (R10 — 2 หน้า)
- หน้า 1: หัวกระดาษ + ประเภทรถ/ประจำเดือน + เกณฑ์ + ตารางรายการทั่วไป (หัวตาราง 1–31) + ตารางเฉพาะรถน้ำมัน + "มีต่อหน้าถัดไป"
- `.page-break` ตั้งใจก่อน "รายการตรวจสอบเฉพาะรถฟอร์คลิฟท์ไฟฟ้า"
- หน้า 2: หัวย่อ (ชื่อเอกสาร (ต่อ) + เลขที่ + ประจำเดือน) + ตารางเฉพาะรถไฟฟ้า (หัววันที่ 1–31 ซ้ำ) + หมายเหตุ + บล็อกลงชื่อทั้งก้อน (`.signs-block`)
- footer ทุกหน้า: เลขที่ · (ร่าง) · Doc. No. · Rev. · "หน้า n/2"
- ตารางใช้ 41 คอลัมน์ฐานเท่ากัน (ลำดับ 2 · รายการ 8 · วันที่ 31 × 1) — ไม่มี style ใน body
- ประมาณการความสูง (ยังไม่ได้วัดจริง — NO-BROWSER): หน้า 1 ≈ 190mm (ยาว 20 รายการ dense) · หน้า 2 ≈ 130mm (DOA 6 ขั้น 2 แถว) จาก 269mm

## 5. วิธี build ใหม่
```bash
python3 make_data.py
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "แบบฟอร์มตรวจเช็ครถฟอร์คลิฟท์ประจำวัน" --max-pages 2
python3 $TD/scripts/compare_original.py ../orig/SAMPLE.pdf out/approved.pdf -o out/compare --region 0:0.72
```

## 6. Checklist ก่อนส่งมอบ
- [x] parity IDENTICAL 5/5 · ไม่มี `{{}}` หลง · ไม่มี key ขาด
- [x] โครง 2 หน้าเท่ากันทุกสถานะ (นับจาก `.doc-page` + `.page-break`)
- [ ] **ยังไม่ได้ทำ (NO-BROWSER):** PDF จริง · `_states_sheet.png` · compare_original

## 7. (Replica) ต้นฉบับลูกค้า + ความต่างที่ตั้งใจ
- ต้นฉบับ: `4. FM-WHS-04 แบบฟอร์มตรวจเช็ครถฟอร์คลิฟท.xlsx` · Doc No. FM-WHS-04 · Rev.00 : 01/07/2569
- Profile token ที่ต่างจาก default: form_fs 8.5pt · form_lh 1.3 · title 11pt · logo 11mm ชิดซ้าย · grid pad 1px · row 4.8mm (dense 4.4mm)
- ความต่างจากกระดาษ (ตั้งใจ):
  1. แบ่ง 2 หน้า (R10) เพราะลงชื่อแบบ DOA N ขั้น + ตาราง 29 แถว × 31 วัน ไม่พอ 1 หน้าที่ฟอนต์ ≥ 8pt
  2. หัวคอลัมน์วันที่ 1–31 ซ้ำที่ตารางรถไฟฟ้าหน้า 2 (หัวตารางซ้ำ) — กระดาษมีหัววันที่เฉพาะตารางแรก
  3. "ประจำเดือน" ขึ้นบรรทัดของตัวเองชิดขวา (กระดาษอยู่บรรทัดเดียวกับประเภทรถ)
  4. ลายเซ็นเป็นแถวล่าง 1 ช่องต่อขั้น DOA · ข้อความ "ส่งในระบบ/พิจารณาในระบบ" แทนลายมือ · คำตัดสิน ตรวจสอบแล้ว/ส่งกลับแก้ไข (AI-DEFAULT)
  5. แก้สะกด "ปฎิบัติ" → "ปฏิบัติ" (G5)
- ผล compare_original: **ยังไม่ได้รัน [NO-BROWSER]** — ต้องรันรอบเต็ม

## 8. (Replica) Data contract + สถานะที่ทดสอบ
- ตาราง contract: `FLI_data-contract.md`
- parity JS ↔ Python: IDENTICAL 5/5
- สถานะ: ร่าง (น้ำมัน · ต.ค. 69 ถึงวันที่ 9) · อนุมัติแล้ว (น้ำมัน · ก.ย. 69 ครบ 30 วัน) · ส่งกลับแก้ไข (ไฟฟ้า · มี ✗ 3 ช่อง) · ยาว 20 รายการทั่วไป (ก.พ. 69 = 29 วัน · dense) · DOA 6 ขั้น (7 ช่อง 4+3) → 2 หน้าทุกสถานะ (ตามโครง)

## 9. (Replica) print_config
```json
{
  "doc_type": "FLI",
  "mode": "replica",
  "template_ref": "form.tpl.html",
  "template_version": "v1",
  "profile_ref": "profile.json",
  "form_code": "FM-WHS-04",
  "revision": "Rev.00 : 01/07/2569",
  "paper": "A4-portrait",
  "pages": 2,
  "page_break": "ก่อนส่วน 'รายการตรวจสอบเฉพาะรถฟอร์คลิฟท์ไฟฟ้า' — หน้า 2 = รายการรถไฟฟ้า + หมายเหตุ + บล็อกลงชื่อทั้งก้อน (R10)",
  "min_rows": {"gen_items": 15, "fuel_items": 8, "elec_items": 6},
  "dense_when_rows_over": 15,
  "day_columns": 31,
  "header_source": "organization_snapshot_at_numbering",
  "sign_boxes": [
    { "box": "requester", "label": "ผู้ตรวจสอบ", "show_date": true },
    { "box": "doa_step:*", "label": "from_doa_step", "show_decision": true, "show_date": true }
  ],
  "decision_words": {
    "default": { "approve": "อนุมัติ", "reject": "ไม่อนุมัติ" },
    "by_role": { "role-supervisor": { "approve": "ตรวจสอบแล้ว", "reject": "ส่งกลับแก้ไข" } }
  },
  "config_reads": {
    "gen_items": "ForkliftChecklistConfig.items[section=general]",
    "fuel_items": "ForkliftChecklistConfig.items[section=fuel]",
    "elec_items": "ForkliftChecklistConfig.items[section=electric]",
    "days": "Calendar(inspection_month).days"
  },
  "footer_left": "เลขที่ {doc.no} · (ร่าง) · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE",
  "footer_right": "Doc. No. : {form_code} · {revision} · หน้า n/2",
  "sign_layout": {
    "source": "approval_chain snapshot (ผู้ขอ + จำนวนขั้นตามที่ตั้งใน DOA)",
    "max_per_row": 4, "split": "even", "dense_when_steps_over": 4, "keep_together": true
  }
}

```
