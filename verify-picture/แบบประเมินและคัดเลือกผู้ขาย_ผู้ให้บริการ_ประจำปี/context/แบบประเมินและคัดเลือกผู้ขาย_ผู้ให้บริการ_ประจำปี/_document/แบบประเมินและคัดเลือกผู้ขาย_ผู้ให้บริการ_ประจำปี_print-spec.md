# PRINT SPEC — แบบประเมินและคัดเลือกผู้ขาย/ผู้ให้บริการ ประจำปี (VEV)

> เอกสารประกอบสำหรับ Dev — แนบคู่กับ FRD/Brief ของ F-TMP-004
> ไฟล์คู่: `FM-PUR-01_template.html` (template build แล้ว · fonts ฝัง) · `out/<state>.html` (5 สถานะ)
> **โหมด:** Replica (แบบฟอร์มลูกค้า · ตารางกรอบ R9) · **2 หน้า** (thai-doc R10)
> ⚠ **[NO-BROWSER]** รอบนี้เครื่องไม่มี browser → ยังไม่ได้ render PDF / `_states_sheet.png` / compare_original — ต้องรัน `render_states.py --max-pages 2` + `compare_original.py` บนเครื่องที่มี browser ก่อนส่งมอบจริง

## 1. สรุป
- **ประเภทเอกสาร:** แบบประเมินและคัดเลือกผู้ขาย/ผู้ให้บริการ ประจำปี / Annual Vendor/Service Provider Evaluation and Selection
- **ขนาด:** A4 แนวตั้ง · **2 หน้า ทุกสถานะ**
- **ฟอนต์:** Sarabun ฝัง · เนื้อ 8.5pt (ไม่ต่ำกว่า 8pt) · หัวเรื่อง 11.5pt
- **หมึก:** เดียว ตาม profile (`profile.json`) — แถบสีหัว/ท้ายของ Excel ไม่ใช้ (Replica หมึกเดียว)

## 2. Field Mapping
| ช่องในเอกสาร | Source | Format | บังคับ | หมายเหตุ |
|---|---|---|---|---|
| โลโก้ | Organization snapshot | data URI | ✓ | ตอนออกเลข |
| ชื่อผู้ขาย/ผู้ให้บริการ · รหัสผู้ขาย | evaluation.vendor_name · vendor_code | ข้อความ | ✓ | กรอกเอง (ยังไม่มี Vendor master) |
| ☐ สินค้า : … · ☐ บริการ : … | evaluation.supply_types · goods_specific · service_specific | ☑/☐ + ข้อความ | ≥1 | ไม่เลือก = ช่องว่าง |
| เลขที่อ้างอิง · เงื่อนไขการชำระเงิน | evaluation.reference_no · credit_term | ข้อความ | — | |
| ตารางหัวข้อการประเมิน | VendorEvaluationConfig.criteria[] (snapshot) + evaluation_scores[] | หัวข้อ + "- เกณฑ์ย่อย" · คะแนนเต็ม · คะแนนที่ได้ | ✓ | คอลัมน์ "คะแนนเฉลี่ย" = คะแนนเต็ม (DEC-12) |
| คะแนนรวม | Σ คะแนนเต็ม · Σ คะแนนที่ได้ | ตัวเลขทศนิยม ≤1 | ✓ | คำนวณ |
| ระบบการบริหารงานที่ได้รับรองมาตรฐานต่างๆ | VendorEvaluationConfig.certifications[] + evaluation.certifications[] | ☑/☐ (+ อื่นๆ ข้อความ) | — | 2 คอลัมน์ 4 แถว |
| สรุปผลการประเมิน | คำนวณจาก คะแนนรวม vs pass_threshold | ☑ ไม่ผ่าน / ☑ ผ่าน | ✓ | ร่างที่คะแนนไม่ครบ = ☐ ทั้งคู่ |
| ผู้ประเมิน · Date | ผู้สร้างใบ · วันที่ส่ง | ชื่อ · วันที่ไทย | ✓ | ว่างในสถานะร่าง |
| ความคิดเห็นผู้ประเมิน (เพิ่มเติม) | evaluation.evaluator_comment | ข้อความ | — | |
| ลงชื่อ ผู้ประเมิน | ผู้สร้างใบ | "ส่งในระบบ วันที่ เวลา" | ✓ | |
| ลงชื่อ ผู้จัดทำ (แผนกจัดซื้อ) / อนุมัติ (ผู้จัดการแผนกจัดซื้อ) (+ ผู้บริหาร กรณีไม่ผ่าน + ขั้น DOA อื่น) | approval_chain | ☑ เห็นด้วย/ไม่เห็นด้วย · ☑ อนุมัติ/ไม่อนุมัติ (ผูก role) + "พิจารณาในระบบ …" | ✓ | 1 ช่องต่อขั้น DOA |
| DOC.No. / REV. | print_config | `FM-PUR-01 · REV.00 : 01/07/2569` | ✓ | footer ขวา + "หน้า n/2" |

## 3. กติกาคำนวณ
- คะแนนรวม = Σ คะแนนที่ได้ · คะแนนเต็มรวม = Σ max_score · ตัวเลขส่งเป็น string (ตัด .0)
- สรุปผล: คะแนนครบทุกหัวข้อ และ รวม < pass_threshold (6) → ☑ ไม่ผ่าน · ≥ 6 → ☑ ผ่าน · ไม่ครบ → ☐ ☐ (DEC-13)

## 4. กติกาการพิมพ์ (R10 — 2 หน้า)
- หน้า 1: โลโก้ + ชื่อเอกสาร (ไทย/อังกฤษ) + ตารางข้อมูลผู้ขาย 3 แถว + ตารางหัวข้อการประเมิน + คะแนนรวม + "มีต่อหน้าถัดไป"
- `.page-break` ตั้งใจก่อน "ระบบการบริหารงานที่ได้รับรองมาตรฐานต่างๆ"
- หน้า 2: หัวย่อ (ชื่อเอกสาร (ต่อ) + เลขที่ + ผู้ขาย) + มาตรฐาน + สรุปผล + หมายเหตุ + ความคิดเห็นผู้ประเมิน + บล็อกลงชื่อทั้งก้อน (`.signs-block`)
- หัวตารางหัวข้อการประเมินซ้ำเมื่อข้ามหน้า (`thead`) · footer ทุกหน้า: เลขที่ · (ร่าง) · DOC.No. · REV. · "หน้า n/2"
- ประมาณการความสูง (ยังไม่ได้วัดจริง — NO-BROWSER): หน้า 1 ≈ 140mm (4 หัวข้อ) / ≈ 215mm (12 หัวข้อ dense) · หน้า 2 ≈ 150mm (3 ช่องลงชื่อ) / ≈ 185mm (DOA 6 ขั้น 2 แถว) จาก ≈ 269mm
- เหตุผล 2 หน้า: ต้นฉบับ 1 หน้าเต็มหน้าแล้ว — DOA 6 ขั้น (7 ช่อง 2 แถว) หรือหัวข้อจาก config 12 ข้อ จะเกิน A4 ที่ฟอนต์ ≥ 8pt → ทุกสถานะ 2 หน้าเท่ากัน

## 5. วิธี build ใหม่
```bash
python3 make_data.py
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "แบบประเมินและคัดเลือกผู้ขาย/ผู้ให้บริการ ประจำปี" --max-pages 2
python3 $TD/scripts/compare_original.py ../orig/SAMPLE.pdf out/approved.pdf -o out/compare --region 0:0.55
```
(ต้นฉบับเป็น .xls — แปลงเป็น PDF ด้วย LibreOffice ก่อน compare)

## 6. Checklist ก่อนส่งมอบ
- [x] parity IDENTICAL 5/5 · ไม่มี `{{}}` หลง · render --strict ไม่มี key ขาด
- [x] โครง 2 หน้าเท่ากันทุกสถานะ (นับจาก `.doc-page` + `.page-break`)
- [ ] **ยังไม่ได้ทำ (NO-BROWSER):** PDF จริง · `_states_sheet.png` · compare_original

## 7. (Replica) ต้นฉบับลูกค้า + ความต่างที่ตั้งใจ
- ต้นฉบับ: `1. FM-PUR-01 แบบประเมินและคัดเลือกผู้ขายผู้ให้บริการ ประจำปี.xlsx` (จริงเป็น .xls) · DOC.No. FM-PUR-01 · REV.00 : 01/07/2569
- Profile token ที่ต่างจาก default: form_fs 8.5pt · form_lh 1.35 · title 11.5pt · logo 12mm กลาง · grid pad 4px · row 5.5mm (dense 4.6mm)
- ความต่างจากกระดาษ (ตั้งใจ):
  1. แบ่ง 2 หน้า (R10) — ดู §4
  2. ลายเซ็นเป็นแถวล่าง 1 ช่องต่อขั้น DOA (ผู้ประเมิน + ผู้จัดทำ + ผู้อนุมัติ [+ ผู้บริหารเมื่อไม่ผ่าน]) · ข้อความ "ส่งในระบบ/พิจารณาในระบบ" แทนลายมือ · ☐ เห็นด้วย/ไม่เห็นด้วย และ ☐ อนุมัติ/ไม่อนุมัติ ย้ายเข้าช่องลงชื่อของ role นั้น
  3. ช่อง "ผู้ประเมิน / Evaluated by / Date" คงที่เดิม (ขวาของสรุปผล) แสดงชื่อ+วันที่จากระบบ และมีช่องลงชื่อผู้ประเมินที่แถวล่างด้วย
  4. "ความคิดเห็นผู้ประเมิน (เพิ่มเติม)" ย้ายมาก่อนบล็อกลงชื่อ (กระดาษอยู่ท้ายสุด) เพื่อให้บล็อกลงชื่ออยู่ล่างสุดตาม B6
  5. แก้สะกด Pratice→Practice · เครื่อหมาย→เครื่องหมาย · มาตราฐาน→มาตรฐาน · อุสาหกรรม→อุตสาหกรรม · Quatation→Quotation (DEC-16) · คงคำ "คะแนนเฉลี่ย" (DEC-12)
  6. ไม่ใช้สีพื้นแถบหัว/ท้าย (หมึกเดียว)
- ผล compare_original: **ยังไม่ได้รัน [NO-BROWSER]** — ต้องรันรอบเต็ม

## 8. (Replica) Data contract + สถานะที่ทดสอบ
- ตาราง contract: `VEV_data-contract.md`
- parity JS ↔ Python: IDENTICAL 5/5
- สถานะ: ร่าง (คะแนน 2/4 หัวข้อ · สรุปผล ☐☐) · อนุมัติแล้ว (ผ่าน 9/10) · ไม่อนุมัติ (ไม่ผ่าน 4.5/10 · ผู้จัดทำเห็นด้วย → ผู้จัดการไม่อนุมัติ · ขั้นผู้บริหารรอ) · ยาว 12 หัวข้อ (dense) · DOA 6 ขั้น (7 ช่อง 4+3)

## 9. (Replica) print_config
```json
{
  "doc_type": "VEV",
  "mode": "replica",
  "template_ref": "form.tpl.html",
  "template_version": "v1",
  "profile_ref": "profile.json",
  "form_code": "FM-PUR-01",
  "revision": "REV.00 : 01/07/2569",
  "paper": "A4-portrait",
  "pages": 2,
  "min_rows": {
    "criteria": 4
  },
  "dense_when_rows_over": 6,
  "header_source": "organization_snapshot_at_numbering",
  "sign_boxes": [
    {
      "box": "requester",
      "label": "ผู้ประเมิน (Evaluated by)",
      "show_date": true
    },
    {
      "box": "doa_step:*",
      "label": "from_doa_step",
      "show_decision": true,
      "show_date": true
    }
  ],
  "decision_words": {
    "default": {
      "approve": "อนุมัติ (Approve)",
      "reject": "ไม่อนุมัติ ( Not Approve)"
    },
    "by_role": {
      "role-pur-officer": {
        "approve": "เห็นด้วย (Agree / Acknowledge)",
        "reject": "ไม่เห็นด้วย (Not Agree)"
      },
      "role-mgr-pur": {
        "approve": "อนุมัติ (Approve)",
        "reject": "ไม่อนุมัติ ( Not Approve)"
      },
      "role-gm": {
        "approve": "อนุมัติ (Approve)",
        "reject": "ไม่อนุมัติ ( Not Approve)"
      }
    }
  },
  "config_reads": {
    "criteria": "VendorEvaluationConfig.criteria[] (text · details[] · max_score)",
    "pass_threshold": "VendorEvaluationConfig.pass_threshold",
    "certifications": "VendorEvaluationConfig.certifications[]"
  },
  "footer_left": "เลขที่ {doc.no} · (ร่าง) · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE",
  "footer_right": "DOC.No. : {form_code} · {revision} · หน้า n/2",
  "sign_layout": {
    "source": "approval_chain snapshot (ผู้ประเมิน + จำนวนขั้นตามที่ตั้งใน DOA · ผลไม่ผ่าน = DOA กลางเพิ่มขั้นผู้บริหาร)",
    "max_per_row": 4,
    "split": "even",
    "dense_when_steps_over": 4,
    "keep_together": true
  },
  "page_break": "ก่อนส่วน 'ระบบการบริหารงานที่ได้รับรองมาตรฐานต่างๆ' — หน้า 1 = หัว + ข้อมูลผู้ขาย + ตารางหัวข้อประเมิน/คะแนนรวม · หน้า 2 = มาตรฐาน + สรุปผล + หมายเหตุ + ความคิดเห็น + บล็อกลงชื่อทั้งก้อน (R10 · DOA 6 ขั้น/หัวข้อ 12 ข้อ เกิน A4)"
}```
