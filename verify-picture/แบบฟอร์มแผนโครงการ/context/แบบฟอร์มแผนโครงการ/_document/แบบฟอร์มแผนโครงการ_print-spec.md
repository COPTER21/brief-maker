# PRINT SPEC — แบบฟอร์มแผนโครงการ (PJP)

> โหมด **Replica** (แบบฟอร์มลูกค้า FM-PDM-01) · thai-doc-pdf-generator v2.2 · ไฟล์คู่: `แบบฟอร์มแผนโครงการ_template.html` · `form.tpl.html` · `profile.json` · `*.data.json`
> render PDF/compare รันแทนบน Chromium (Playwright) ใน container ของ agent — เครื่องผู้ใช้ไม่มี browser (NO-BROWSER) · ผลอยู่ใน `out/`

## 1. สรุป
- **ประเภทเอกสาร:** แบบฟอร์มแผนโครงการ / PROJECT PLAN FORM
- **ขนาด:** A4 แนวตั้ง · **ฟอนต์:** Sarabun (ฝัง) 8.6pt (≥ 8pt) · หมึกเดียวตาม profile
- **จำนวนหน้า: 2 หน้าทุกสถานะ (R10)** — ต้นฉบับ Excel พิมพ์ 3 หน้า (ตัดที่แถว 19/53) · ออกแบบใหม่ 2 หน้า ไม่บีบฟอนต์
  - หน้า 1 = หัว (โลโก้ + ชื่อเอกสาร + ฝ่ายพัฒนาโครงการ) + ส่วนที่ 1–5 · ท้ายหน้า "มีต่อหน้าถัดไป" · footer "หน้า 1/2"
  - หน้า 2 = หัวย่อ (ชื่อเอกสาร (ต่อ) + รหัสโครงการ) + ส่วนที่ 6–8 + **ส่วนที่ 9 ตารางอนุมัติทั้งก้อน** (`.signs-block` ชิดล่าง) · footer "หน้า 2/2"
  - จุดตัดหน้า: `.doc-page.page-break` ก่อนส่วนที่ 6 (ตั้งใจ) · หัวตารางทุกตาราง = thead (ซ้ำเมื่อข้ามหน้า) · tr ไม่ตัดกลาง

## 2. Field Mapping
ดู §A Data contract ท้ายไฟล์ (37 ช่องตาม FORM_SPEC 1:1)

## 3. กติกาคำนวณ / ตรวจ
- ระยะเวลา (โครงการ/กิจกรรม) = วันที่สิ้นสุด − วันที่เริ่ม + 1 → "N วัน" · รวมงบที่ขอ/อนุมัติ = ผลรวมรายการ `#,##0.00` (DEC-04)
- งบที่อนุมัติว่างจนผู้อนุมัติขั้นสุดท้ายพิจารณา (ร่าง/รออนุมัติ/ไม่อนุมัติ = ว่าง) · สถานะกิจกรรมตามค่า dropdown ต้นฉบับ (Not Started/In Progress/Completed/Delayed · DEC-18)

## 4. กติกาการพิมพ์
- แถวว่างเติมครบตามกระดาษ: KPI 3 · กิจกรรม 10 · งบ 6 · ความเสี่ยง 5 · เกินแล้ว `layout.dense` (แถว 4.8mm)
- ตารางอนุมัติ = 1 แถวต่อช่องลงชื่อ (ผู้จัดทำ + 1 แถวต่อขั้น DOA) — จำนวนตาม DOA ไม่ fix · DOA 6 ขั้น = 7 แถว ยัง 2 หน้า
- ข้อความยาวมากในส่วนที่ 2–3 (เกิน ~3 บรรทัดต่อช่อง) อาจดันหน้า 1 ล้น — ต้องทดสอบกับข้อมูลจริงรอบ UAT

## 5. วิธี build ใหม่
```bash
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "แบบฟอร์มแผนโครงการ" --max-pages 2
python3 $TD/scripts/compare_original.py ../orig/SAMPLE.pdf out/approved.pdf -o out/compare
```

## 6. Checklist
- [x] parity IDENTICAL 6/6 · ไม่มี {{}} หลง · ไม่มี key ขาด
- [x] 2 หน้าทุกสถานะ (6/6) · ฟอนต์ ≥ 8pt · ตัดหน้าตั้งใจก่อนส่วนที่ 6 · "หน้า 1/2" · "มีต่อหน้าถัดไป"
- [x] ตารางอนุมัติครบสาย (ผู้จัดทำ + ขั้น DOA) · คำตัดสินตาม role
- [x] ดูภาพ `_states_sheet.png` + `compare/compare_side.png` แล้ว

## 7. (Replica) ต้นฉบับลูกค้า + ความต่างที่ตั้งใจ
- ต้นฉบับ: `1. FM-PDM -01 แบบฟอร์มแผนโครงการ (PROJECT PLAN FORM).xlsx` (→ orig/SAMPLE.pdf ผ่าน LibreOffice · 3 หน้า) · Doc No. FM-PDM-01 · Rev.00 : 01/07/2569
- Profile: form_fs 8.6pt · lh 1.35 · title 13pt · logo 11mm ในช่องซ้ายหัวตาราง · grid row 5.4mm · หัวตารางพื้นขาว
- ความต่าง (ตั้งใจ): 3 หน้า → 2 หน้า (R10) ทำให้ช่องข้อความส่วนที่ 2–3 เตี้ยลง (ต้นฉบับเป็นกล่องเปล่าสูง ~30mm สำหรับเขียนมือ — ระบบพิมพ์ข้อความจริง สูงตามเนื้อหา) · หัวส่วนเป็นตัวหนาไม่มีแถบเทา (replica.css ไม่มี token แถบเทาชิดซ้าย) · ตารางอนุมัติแถวตาม DOA + คำตัดสิน ☐ ตรวจสอบแล้ว/☐ อนุมัติ · ข้อความ "ส่งในระบบ/พิจารณาในระบบ" แทนลายมือ · footer เลขที่ + CUBE NATIVE + หน้า · โลโก้ = Organization (ตัวอย่าง placeholder)
- compare_original (หน้า 1): **WARN 0.303** (บรรทัดตรงตำแหน่ง 1/5 · cols 0.54) — อธิบายได้: หน้า 1 ต้นฉบับมีแค่ส่วนที่ 1–2 กล่องเปล่าสูง ส่วนแบบพิมพ์รวมส่วนที่ 1–5 ตามการออกแบบ 2 หน้า · ดูภาพวางคู่แล้ว ลำดับ/ถ้อยคำ/คอลัมน์ตรงต้นฉบับ

## 8. (Replica) Data contract + สถานะที่ทดสอบ
- parity JS ↔ Python: IDENTICAL 6/6
- สถานะ: draft · pending (ตรวจสอบแล้ว รออนุมัติ) · approved · rejected (ผู้อนุมัติไม่อนุมัติ) · long-12rows (กิจกรรม 12 · KPI 4 · งบ 8 · ความเสี่ยง 6 · dense) · approved-doa6steps (7 แถว) → ทุกสถานะ 2 หน้า (`out/_states.json`)

## 9. (Replica) print_config
```json
{
  "doc_type": "PJP",
  "mode": "replica",
  "template_ref": "form.tpl.html",
  "template_version": "v1",
  "profile_ref": "profile.json",
  "form_code": "FM-PDM-01",
  "revision": "Rev.00 : 01/07/2569",
  "paper": "A4-portrait",
  "pages": 2,
  "page_break": "ก่อนส่วนที่ 6 งบประมาณ (หน้า 1 = ส่วนที่ 1–5 · หน้า 2 = ส่วนที่ 6–9 + ตารางอนุมัติ)",
  "min_rows": { "goals": 3, "actions": 10, "budget": 6, "risks": 5 },
  "dense_when_rows_over": { "goals": 3, "actions": 10, "budget": 6, "risks": 5 },
  "header_source": "organization_snapshot_at_numbering",
  "sign_boxes": [
    { "box": "requester", "label": "ผู้จัดทำ (Prepared by)", "show_date": true },
    { "box": "doa_step:*", "label": "from_doa_step", "show_decision": true, "show_date": true }
  ],
  "decision_words": {
    "default": { "approve": "อนุมัติ", "reject": "ไม่อนุมัติ" },
    "by_role": {
      "role-line-manager": { "approve": "ตรวจสอบแล้ว", "reject": "ไม่ผ่านการตรวจสอบ" },
      "role-gm": { "approve": "อนุมัติ", "reject": "ไม่อนุมัติ" }
    }
  },
  "footer_left": "เลขที่ {doc.no} · (ร่าง) · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE",
  "footer_right": "หน้า {page}/2 · Doc. No. : {form_code} · {revision}",
  "sign_layout": {
    "source": "approval_chain snapshot (ผู้จัดทำ + จำนวนขั้นตามที่ตั้งใน DOA)",
    "render": "ตารางอนุมัติ 1 แถวต่อช่อง (บทบาท · ชื่อ-นามสกุล · ลายเซ็น/คำตัดสิน · วันที่ลงนาม) ตามกระดาษ",
    "max_per_row": 4,
    "split": "even",
    "dense_when_steps_over": 4,
    "keep_together": true
  }
}
```

## §A DATA CONTRACT — แบบฟอร์มแผนโครงการ (PJP)

> สัญญาข้อมูลระหว่าง backend ↔ template (`form.tpl.html`) · ใช้ทั้ง prototype (tpl_render.js) และ server (render_doc.py)
> กติกา: ค่าแสดงทุกตัวเป็น string ที่จัดรูปแล้ว · boolean ใช้เป็นเงื่อนไขเท่านั้น · checkbox = "☑"/"☐" · ว่าง = "" · ไม่มี {} ว่าง

| key | Source (entity.field / engine) | ตัวอย่าง (สมมติ) | หมายเหตุ |
|---|---|---|---|
| `company.name` · `company.logo` | Organization → header_snapshot (ตอนออกเลข) | `บริษัท ตัวอย่าง จำกัด` · data URI | ไม่ดึงสดหลังออกเลข |
| `doc.title` · `doc.no` · `doc.is_draft` | ค่าคงที่ · ENG-DOC-NUM (PJP) · status = draft | `แบบฟอร์มแผนโครงการ (PROJECT PLAN FORM)` · `PJP-2569-0004` | ออกเลขตอนบันทึกครั้งแรก (DEC-13) |
| `doc.form_code` · `doc.revision` | F-DOCCFG `print_config` | `FM-PDM-01` · `Rev.00 : 01/07/2569` | |
| `project.name` | project_plan.project_name | `ปรับปรุงระบบจัดเก็บสินค้าคลังกลาง` | |
| `project.code` | project_plan.doc_no (= รหัสโครงการ) | `PJP-2569-0004` | |
| `project.owner_dept` | project_plan.owner_dept_id → OrgUnit.name | `ฝ่ายพัฒนาโครงการ` | |
| `project.manager` | project_plan.project_manager_id → Employee.full_name | `สมชาย ใจดี` | PDPA · snapshot ตอนส่ง |
| `project.start_date` · `project.end_date` | project_plan.start_date / end_date | `3 พฤศจิกายน 2569` | วันที่เต็ม พ.ศ. · end ≥ start |
| `project.duration` | computed end − start + 1 | `116 วัน` | |
| `background` · `problem_opportunity` · `justification` | project_plan.* | ข้อความ | |
| `objective_primary` · `objective_secondary` | project_plan.* | ข้อความ | |
| `goals[].quantitative/qualitative/kpi/method` | project_plan_goal.* | `ลดเวลาหยิบสินค้า 30%` | ≥ 3 แถว (เติมว่าง) |
| `actions[].no/activity/responsible/start_date/end_date/duration/status` | project_plan_action.* · responsible → Employee.full_name | `1` · `Completed` | ≥ 10 แถว · duration computed · status ค่าต้นฉบับ |
| `budget[].item/requested/approved/remark` | project_plan_budget.* | `150,000.00` | ≥ 6 แถว · approved ว่างจนอนุมัติ |
| `budget_total.requested` · `budget_total.approved` | SUM(budget[].requested/approved) | `475,000.00` · `445,000.00` | |
| `risks[].risk/impact/severity/mitigation/owner` | project_plan_risk.* · owner → Employee.full_name | `สูง` | ≥ 5 แถว · severity สูง/กลาง/ต่ำ |
| `benefit_financial` · `benefit_operational` · `benefit_strategic` | project_plan.* | ข้อความ | |
| `sign_rows[].signs[]` → `role` · `name` · `position` · `date` · `decision{approve_box,reject_box,approve_word,reject_word}` | ผู้จัดทำ + `approval_chain` (DOA snapshot) via sign_rows.py | `ผู้ตรวจสอบ (Reviewed by)` · `☑ ตรวจสอบแล้ว ☐ ไม่ผ่านการตรวจสอบ` | 1 แถวตารางต่อช่อง · จำนวน = 1 + ขั้น DOA · คำตัดสินตาม role |
| `layout.dense` | แถวใดเกิน min_rows หรือ ขั้น DOA > 4 | `true` | |
