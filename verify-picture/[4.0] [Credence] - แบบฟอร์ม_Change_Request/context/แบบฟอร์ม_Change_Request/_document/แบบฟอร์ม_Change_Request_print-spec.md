# PRINT SPEC — แบบฟอร์ม Change Request (ITCR)

> เอกสารประกอบสำหรับ Dev — คู่กับ FRD/UI Brief ของ F-TMP-005 · โหมด **Replica** (แบบฟอร์มลูกค้า FM-ITS-07)
> ไฟล์คู่: `ITCR_template.html` (master, fonts ฝัง) · `form.tpl.html` (template logic-less) · `*.data.json` (5 สถานะ) · `out/*.html`
> ⚠️ **[NO-BROWSER]** เครื่องที่ทำงานไม่มี browser → ยังไม่ได้ render PDF/PNG ด้วย `render_pdf.py` / `render_states.py` และยังไม่รัน `compare_original.py` — ต้องรันรอบเต็มบนเครื่องที่มี browser
> ทุกมติที่อ้าง = AI-DEFAULT รอลูกค้ายืนยัน (DECISIONS.lock)

## 1. สรุป
- **ประเภทเอกสาร:** แบบฟอร์ม Change Request / Change Request Form · Doc. No. FM-ITS-07 · Rev.00 : 01/07/2569
- **ขนาด:** A4 แนวตั้ง 1 หน้า (กระดาษต้นฉบับ 1 หน้า · ตรวจเบื้องต้นทุกสถานะ 1 หน้า → ไม่เข้าเงื่อนไข R10)
- **ฟอนต์:** Sarabun (ฝัง) · หมึกเดียวตาม profile · หัวช่องซ้ายพื้นเทาตาม R9
- **Renderer:** Playwright/Chromium (`prefer_css_page_size`, `print_background`)

## 2. Field Mapping
| ช่องในเอกสาร | Source | Format | บังคับ | หมายเหตุ |
|---|---|---|---|---|
| (ไม่มีบนกระดาษ) เลขที่ | ENG-DOC-NUM · doc_type ITCR | `ITCR-พ.ศ.-running` | ✓ | ออกตอนบันทึกครั้งแรก (DEC-10) · แสดงที่ footer ซ้าย (DEC-17) ไม่เพิ่มแถว |
| วันที่ | request_date (auto) | วัน เดือนไทย พ.ศ. | ✓ | |
| ตำแหน่ง | Employee.position | — | ✓ | แก้สะกด ตําแหน่ง→ตำแหน่ง (DEC-12) |
| ชื่อ-นามสกุล | Employee.full_name | — | ✓ | PDPA |
| วันที่ต้องการส่งมอบ | due_date | วันที่ไทย | ✓ | ≥ วันที่ขอ (เตือน · DEC-14) |
| สถานที่ส่งมอบ | delivery_location | — | ✓ | |
| เรื่องที่ต้องการ | subject | — | ✓ | |
| ประเภทของการเปลี่ยนแปลง ☐×5 | change_types[] (multi) | "☑"/"☐" | ✓ ≥1 | DEC-16 · อื่นๆ ต้องระบุ change_type_other (DEC-15) |
| รายละเอียดของการเปลี่ยนแปลง | change_detail → detail_lines[] | แตกบรรทัดตาม \n | ✓ | ขั้นต่ำ 1 แถว · คำอธิบายสีเทาบนกระดาษพิมพ์เป็นแถวคงที่ |
| วัตถุประสงค์ของการเปลี่ยนแปลง | objective → objective_lines[] | | ✓ | ขั้นต่ำ 1 แถว |
| ระบบที่ได้รับผลกระทบและ ผลกระทบที่อาจเกิดขึ้น | impact → impact_lines[] | | ✓ | ขั้นต่ำ 1 แถว |
| แผนการดำเนินการ | action_plan → plan_lines[] | | ✓ | ขั้นต่ำ 2 แถว |
| ผู้ขอซื้อ | requester + submitted_at | "ส่งในระบบ …" | ✓ | คำตามกระดาษ (DEC-13 · OQ ลูกค้า) |
| ตรวจสอบโดย / อนุมัติโดย (ช่องต่อขั้น DOA) | approval_chain[] | ☑ อนุมัติ / ☑ ไม่อนุมัติ + "พิจารณาในระบบ …" | ✓ | ค่าเริ่ม 2 ขั้น role-line-manager → role-mgr-it · จำนวนช่องตาม DOA กลาง (DEC-03/07) |

## 3. กติกาคำนวณ
- ไม่มีสูตร/ค่าคงที่บนกระดาษ · แตกข้อความหลายบรรทัดเป็น `*_lines[]` แล้วเติมแถวว่างให้ครบขั้นต่ำ · รวมบรรทัดเกินขั้นต่ำ > 6 หรือ DOA > 4 ขั้น → `layout.dense`

## 4. กติกาการพิมพ์
- ตารางกรอบ R9 · ลายเซ็น+footer ชิดล่าง (`.doc-bottom`) · `.signs-block` ไม่ตัดข้ามหน้า · แถวละ ≤4 ช่อง

## 5. วิธี build ใหม่
```bash
python3 make_data.py                                     # data 5 สถานะ (ข้อมูลสมมติ)
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "แบบฟอร์ม Change Request" --max-pages 1
python3 $TD/scripts/compare_original.py ../orig/SAMPLE.pdf out/approved.pdf -o out/compare --region 0:0.8
```

## 6. Checklist
- [x] parity JS ↔ Python IDENTICAL 5/5
- [x] ไม่มี {{…}} หลง · ไม่มี key ขาด (ทุกสถานะ)
- [ ] A4 1 หน้า ทุกสถานะ — **[NO-BROWSER] ยังไม่ยืนยันด้วย render_states บนเครื่องงาน** (ตรวจเบื้องต้นนอกเครื่องงานด้วย Chromium: 5/5 สถานะ = 1 หน้า · ไม่ใช่ผลด่านทางการ)
- [x] ลายเซ็นครบ: ผู้ขอซื้อ + ขั้น DOA

## 7. (Replica) ต้นฉบับ + ความต่างที่ตั้งใจ
- ต้นฉบับ: `7. FM-ITS-07 แบบฟอร์ม Change Request Form.xlsx` · Doc. No. FM-ITS-07 · Rev.00 : 01/07/2569 (footer)
- Profile: form_title_fs 15pt · form_logo_h 11mm · form_logo_align left · form_cb_fs 11pt
- ความต่างที่ตั้งใจ: (1) ชื่อเอกสารกลางหน้าใต้โลโก้ (กระดาษวางขวาของโลโก้) — R1/R2 มาตรฐาน (2) ช่องลงชื่อ = ผู้ขอซื้อ + 1 ช่องต่อขั้น DOA (ค่าเริ่ม ตรวจสอบโดย · อนุมัติโดย) (3) ใต้เส้นลงชื่อ = (ชื่อ) + "ส่ง/พิจารณาในระบบ …" แทน (…/…/…) (4) footer เลขที่/ร่าง + Doc. No. · Rev. (5) แก้สะกด ตำแหน่ง (6) คำอธิบายสีเทาใต้หัวข้อพิมพ์ด้วยหมึกเดียว (Replica ห้ามสีนอก profile) (7) ลายเซ็นชิดล่างหน้า
- compare_original: **[NO-BROWSER] ข้าม** (ต้องมี approved.pdf) — รันรอบเต็มบนเครื่องที่มี browser

## 8. (Replica) Data contract + สถานะ
| key | Source | ตัวอย่าง | หมายเหตุ |
|---|---|---|---|
| `company.name` · `company.logo` | Organization header_snapshot | data URI | ไม่ดึงสดหลังออกเลข |
| `doc.title` · `doc.no` · `doc.is_draft` | ค่าคงที่ (Change Request Form) · ENG-DOC-NUM · status | `ITCR-2569-0001` | |
| `doc.form_code` · `doc.revision` | F-DOCCFG print_config | `FM-ITS-07` · `Rev.00 : 01/07/2569` | |
| `req_date` · `due_date` | itcr.request_date / due_date | `10 ตุลาคม 2569` | string จัดรูปแล้ว |
| `employee.name` · `employee.position` | Employee snapshot | | PDPA |
| `delivery_location` · `subject` | itcr.* | | |
| `change_type.{software,hardware,network,security,other}` · `change_type_other` | itcr.change_types[] | "☑"/"☐" | |
| `detail_lines[]` · `objective_lines[]` · `impact_lines[]` · `plan_lines[]` → `text` | itcr.change_detail / objective / impact / action_plan | | เติมแถวว่าง 1/1/1/2 |
| `sign_rows[].signs[]` → role · name · position · date · decision | ผู้ขอซื้อ + approval_chain | | sign_rows.py / tplSignRows |
| `layout.dense` | บรรทัดเกินขั้นต่ำ > 6 หรือ DOA > 4 ขั้น | | |

- parity: IDENTICAL 5/5
- สถานะ: draft · approved · rejected (ขั้น 2 ไม่อนุมัติ) · long-text (4/2/2/4 บรรทัด → dense) · approved-doa6steps (7 ช่อง 4+3) → HTML ครบ · PDF [NO-BROWSER]

## 9. (Replica) print_config
```json
{
  "doc_type": "ITCR",
  "mode": "replica",
  "template_ref": "form.tpl.html",
  "template_version": "v1",
  "profile_ref": "profile.json",
  "form_code": "FM-ITS-07",
  "revision": "Rev.00 : 01/07/2569",
  "revision_note": "ตามท้ายกระดาษ Doc. No. : FM-ITS-07 Rev.00 : 01/07/2569",
  "paper": "A4-portrait",
  "pages": 1,
  "min_rows": 1,
  "text_min_rows": { "detail_lines": 1, "objective_lines": 1, "impact_lines": 1, "plan_lines": 2 },
  "dense_when_rows_over": 6,
  "header_source": "organization_snapshot_at_numbering",
  "sign_boxes": [
    { "box": "requester", "label": "ผู้ขอซื้อ", "show_date": true, "note": "คำตามกระดาษ (G5) — OQ ลูกค้า" },
    { "box": "doa_step:*", "label": "from_doa_step", "show_decision": true, "show_date": true }
  ],
  "decision_words": {
    "default": { "approve": "อนุมัติ", "reject": "ไม่อนุมัติ" },
    "by_role": {}
  },
  "config_reads": {},
  "footer_left": "เลขที่ {doc.no} · (ร่าง) · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE",
  "footer_right": "Doc. No. : {form_code} · {revision}",
  "sign_layout": {
    "source": "approval_chain snapshot (ผู้ขอซื้อ + จำนวนขั้นตามที่ตั้งใน DOA)",
    "max_per_row": 4,
    "split": "even",
    "dense_when_steps_over": 4,
    "keep_together": true
  }
}
```
