# PRINT SPEC — ใบคำร้องขอดำเนินการด้านเอกสาร (DAR · FM-CCC-03)

> โหมด **Replica** (แบบฟอร์มลูกค้า · ตารางกรอบ R9 · 2 หน้า R10) · ไฟล์คู่: `DAR_template.html` · `form.tpl.html` · `profile.json` · `*.data.json` · `print_config.json` · `DAR_data-contract.md`
> มติทั้งหมด **AI-DEFAULT** (unattended) — ลูกค้ายืนยันในใบลงนามก่อน UAT

## 1. สรุป
- ประเภทเอกสาร: ใบคำร้องขอดำเนินการด้านเอกสาร / Document Action Request (DAR Form)
- ขนาด: A4 แนวตั้ง **2 หน้า** (ต้นฉบับ Excel A4 แนวนอน 1 หน้ากว้าง A1:DM32 → ถ้าบีบลงแนวตั้ง 1 หน้า ฟอนต์ < 8pt → R10)
- ฟอนต์ Sarabun 8.5pt (ไม่ต่ำกว่า 8pt) · หมึกเดียวตาม profile
- Renderer ทางการ: Playwright/Chromium (`render_pdf.py`) — **รอบนี้ NO-BROWSER** ใช้ weasyprint ทำ PDF พรีวิวนับหน้าเท่านั้น (ไม่ใช่ด่านทางการ)

## 2. Field Mapping → ดู `DAR_data-contract.md` (F01–F17 + ตัวเลือก 5 กลุ่ม + sign_rows)

## 3. กติกาคำนวณ
- ไม่มีสูตร/เงิน (DEC-04) · data layer: ☑☐ · แตกบรรทัดเดิม/ใหม่ · เติมแถวว่าง · แบ่งหน้าแถวเอกสารเกี่ยวข้องตาม `page1_row_budget`

## 4. กติกาการพิมพ์
- หน้า 1: หัว (โลโก้ · ชื่อเอกสาร · DAR.No.) · ถึง/วันที่/ผู้เขียน/ฝ่าย/แผนก · Document No./Revision/วัตถุประสงค์/ISSUE/ชื่อเอกสาร/วันบังคับใช้/ขั้นตอน PL/WI/ที่มา · หมายเหตุ "ใบ DAR 1 ใบ ต่อเอกสาร 1 ฉบับ" · รายละเอียดการแก้ไข (≥8 แถว) · รายการเอกสารที่ต้องจัดทำ/ทบทวน (≥14 แถวรวม) · "มีต่อหน้าถัดไป" · "หน้า 1/2"
- `.page-break` ตั้งใจก่อนส่วน "หน่วยงาน/ตำแหน่ง ที่ต้องได้รับการแจกจ่ายเอกสาร"
- หน้า 2: หัวย่อ (ชื่อเอกสาร + DAR.No. (ต่อ)) · ตารางเอกสารเกี่ยวข้อง (ต่อ) ถ้ามี (หัวตารางซ้ำ) · แจกจ่าย 27 ช่อง · หมายเหตุ · วิธีรับ/E-Mail · ลงนามรับเอกสารควบคุม · **บล็อกลงชื่อทั้งก้อน** (ผู้จัดทำ + 1 ช่อง/ขั้น DOA · แถวละ ≤4) · หมายเหตุตารางผู้มีอำนาจ · footer + "หน้า 2/2"
- ทุกสถานะ = 2 หน้า

## 5. วิธี build ใหม่
```bash
python $TD/scripts/parity_check.py form.tpl.html *.data.json
python $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "ใบคำร้องขอดำเนินการด้านเอกสาร" --max-pages 2
python $TD/scripts/compare_original.py ../orig/SAMPLE.pdf out/approved.pdf -o compare --region 0:0.72
```

## 6. Checklist
- [x] parity IDENTICAL 5/5 · ไม่มี {{}} หลง
- [x] 5 สถานะ = 2 หน้าเท่ากัน (พรีวิว weasyprint) · ฟอนต์ ≥ 8pt
- [x] ลายเซ็นครบสาย (4 ขั้น = 5 ช่อง 3+2 · 6 ขั้น = 7 ช่อง 4+3)
- [ ] PDF ทางการ Chromium + compare_original — **ค้างรอบเครื่องที่มี browser** (NO-BROWSER)

## 7. (Replica) ต้นฉบับ + ความต่างที่ตั้งใจ
- ต้นฉบับ: `orig/3. FM-CCC-03 … (DAR Form ).xlsx` · Doc No. FM-CCC-03 · Rev.00 : 01/07/2569
- Profile token ที่ต่างจาก default: form_fs 8.5pt · form_title_fs 12pt · form_logo_h 9mm · form_logo_align left · form_cb_fs 10pt · form_grid_row_h 6.4mm/5.6mm dense · form_grid_gap 3px
- ความต่างจากกระดาษ (ตั้งใจ): (1) แนวนอน 1 หน้า → แนวตั้ง 2 หน้า (R10) (2) หัวคอลัมน์แนวตั้ง 27 หน่วยงาน → ตาราง 4 คอลัมน์ ☐ + ชื่อ (อ่านได้บน A4 แนวตั้ง) · ชุดซ้ำติด "(2)" (DEC-12) (3) ลายเซ็นย้ายเป็นแถวล่างตาม DOA (ผู้จัดทำ + 4 ขั้น ค่าเริ่ม) แทน 3 ช่องบนกระดาษ (DEC-07) (4) "ลงนามรับเอกสารควบคุม" = ข้อความระบบ (5) footer เลขที่ · ร่าง · CUBE NATIVE + "หน้า x/2" (6) ISSUE เพิ่ม ☐ WI ตามหัวคอลัมน์ (DEC-14)
- compare_original: **[NO-BROWSER] ข้าม** (ต้องใช้ approved.pdf จาก Chromium) — คาด WARN เพราะเปลี่ยนแนวกระดาษ · ต้องให้คนดูภาพวางคู่ในรอบเต็ม

## 8. (Replica) Data contract + สถานะ
- contract: `DAR_data-contract.md` · parity JS ↔ Python: IDENTICAL 5/5
- สถานะ: ร่าง · อนุมัติแล้ว (ใกล้ตัวอย่าง) · ไม่อนุมัติ (ขึ้นทะเบียนใหม่/Policy/IA · ไม่มีเอกสารเกี่ยวข้อง) · ยาว (แก้ไข 10 แถว + เอกสารเกี่ยวข้อง 18 แถว + แจกจ่าย 21) · DOA 6 ขั้น (7 ช่อง 4+3 · dense) → 2 หน้าทุกสถานะ

## 9. (Replica) print_config
```json
{
  "doc_type": "DAR",
  "mode": "replica",
  "template_ref": "form.tpl.html",
  "template_version": "v1",
  "profile_ref": "profile.json",
  "form_code": "FM-CCC-03",
  "revision": "Rev.00 : 01/07/2569",
  "paper": "A4-portrait",
  "paper_note": "ต้นฉบับ A4 แนวนอน (Excel print area A1:DM32 · 1 หน้ากว้าง) · engine กลางรองรับ A4 แนวตั้งเท่านั้น → ออกแบบ 2 หน้าตาม R10 · หัวตารางซ้ำ",
  "pages": 2,
  "page_break": "ก่อนบล็อก หน่วยงาน/ตำแหน่ง ที่ต้องได้รับการแจกจ่ายเอกสาร (หน้า 2 มีบรรทัดชื่อเอกสาร + DAR.No. (ต่อ)) · บล็อกลงชื่อทั้งก้อนอยู่หน้า 2",
  "min_rows": 14,
  "rows_page1": 14,
  "rows_page2_max": 8,
  "change_min_rows": 8,
  "dist_cols": 4,
  "pad_rows_to_page": true,
  "dense_when_rows_over": 18,
  "header_source": "organization_snapshot_at_numbering",
  "sign_boxes": [
    {
      "box": "requester",
      "label": "ผู้จัดทำ",
      "show_date": true
    },
    {
      "box": "doa_step:*",
      "label": "from_doa_step",
      "show_decision": true,
      "show_date": true
    },
    {
      "box": "receipt",
      "label": "ลงนามรับเอกสารควบคุม",
      "show_date": true,
      "note": "ไม่ใช่ขั้น DOA — ผู้รับเอกสารกดลงนามรับหลังอนุมัติ (ข้อความระบบ)"
    }
  ],
  "decision_words": {
    "default": {
      "approve": "อนุมัติ",
      "reject": "ไม่อนุมัติ"
    },
    "by_role": {}
  },
  "config_reads": {},
  "footer_left": "เลขที่ {doc.no} · (ร่าง) · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE",
  "footer_right": "Doc. No. : {form_code} · {revision}",
  "sign_layout": {
    "source": "approval_chain snapshot (ผู้จัดทำ + จำนวนขั้นตามที่ตั้งใน DOA)",
    "max_per_row": 4,
    "split": "even",
    "dense_when_steps_over": 4,
    "keep_together": true
  },
  "page1_row_budget": 22,
  "page1_row_budget_note": "แถวรายละเอียดแก้ไข (ขั้นต่ำ 8) + แถวเอกสารเกี่ยวข้อง (ขั้นต่ำ 14) บนหน้า 1 รวม 22 · แก้ไขเกิน 8 แถว → เอกสารเกี่ยวข้องย้ายไปตารางต่อหน้า 2 (หัวตารางซ้ำ) · รวมทั้งเอกสารยังแสดงเอกสารเกี่ยวข้อง ≥ 14 แถว"
}
```
