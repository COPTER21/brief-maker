# PRINT SPEC — รายงานความคืบหน้าโครงการ (PPR)

> โหมด **Replica** (แบบฟอร์มลูกค้า FM-PDM-02) · thai-doc-pdf-generator v2.2 · ไฟล์คู่: `รายงานความคืบหน้าโครงการ_template.html` · `form.tpl.html` · `profile.json` · `*.data.json`
> render PDF/compare รันแทนบน Chromium (Playwright) ใน container ของ agent — เครื่องผู้ใช้ไม่มี browser (NO-BROWSER) · ผลอยู่ใน `out/`

## 1. สรุป
- **ประเภทเอกสาร:** รายงานความคืบหน้าโครงการ / PROJECT PROGRESS REPORT
- **ขนาด:** A4 แนวตั้ง · **ฟอนต์:** Sarabun (ฝัง) 8.6pt (≥ 8pt) · หมึกเดียวตาม profile
- **จำนวนหน้า: 2 หน้าทุกสถานะ (R10)** — ต้นฉบับ Word (Letter) 4 หน้า · ออกแบบใหม่ 2 หน้า ไม่บีบฟอนต์
  - หน้า 1 = โลโก้ + ชื่อเอกสาร (ไทย/อังกฤษ) + ข้อมูลโครงการ 5 แถว + ข้อ 1–3 · ท้ายหน้า "มีต่อหน้าถัดไป" · footer "หน้า 1/2"
  - หน้า 2 = หัวย่อ (ชื่อเอกสาร (ต่อ) + รหัสโครงการ) + ข้อ 4–6 + **บล็อกลงชื่อทั้งก้อน** (`.signs-block` ชิดล่าง) · footer "หน้า 2/2"
  - จุดตัดหน้า: `.doc-page.page-break` ก่อนข้อ 4 (ตั้งใจ · ก่อนบล็อกลงชื่อ) · หัวตารางทุกตาราง = thead (ซ้ำเมื่อข้ามหน้า) · tr ไม่ตัดกลาง

## 2. Field Mapping
ดู §A Data contract ท้ายไฟล์ (35 ช่องตาม FORM_SPEC 1:1)

## 3. กติกาคำนวณ / จัดรูป
- ไม่มีสูตรบนกระดาษ · ☐ สรุปสถานะ 3 ตัวเลือก → `status.*_box` ☑/☐ (เลือก 1)
- รอบการรายงาน = "d MMMM yyyy – d MMMM yyyy" (พ.ศ.) · งบประมาณ `#,##0.00`
- คอลัมน์ "ผู้รับผิดชอบ / กำหนดแล้วเสร็จ" = `ชื่อ / d MMM yyyy` (เก็บ owner + due_date แยก · แสดงรวม · DEC G5)

## 4. กติกาการพิมพ์
- แถวว่างเติมครบตามกระดาษ: ผลงาน 9 · KPI 8 (เลข 1.–8. คงที่) · ปัญหา 11 · แผนรอบถัดไป 10 · ประเด็นตัดสินใจ 11 · เกินแล้ว `layout.dense`
- บล็อกลงชื่อ = ผู้จัดทำรายงาน + ผู้จัดการโครงการ (ผู้ส่ง · "ส่งในระบบ") + 1 ช่องต่อขั้น DOA — จำนวนตาม DOA ไม่ fix · แถวละ ≤4 · DOA 6 ขั้น = 8 ช่อง 2 แถว ยัง 2 หน้า
- ข้อมูลจริงที่เกิน ~12 แถวพร้อมกันหลายตาราง หรือข้อความยาวหลายบรรทัดต่อช่อง อาจดันเกิน 2 หน้า — ต้องทดสอบกับข้อมูลจริงรอบ UAT

## 5. วิธี build ใหม่
```bash
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "รายงานความคืบหน้าโครงการ" --max-pages 2
python3 $TD/scripts/compare_original.py ../orig/SAMPLE.pdf out/approved.pdf -o out/compare
```

## 6. Checklist
- [x] parity IDENTICAL 6/6 · ไม่มี {{}} หลง · ไม่มี key ขาด
- [x] 2 หน้าทุกสถานะ (6/6) · ฟอนต์ ≥ 8pt · ตัดหน้าตั้งใจก่อนข้อ 4 · "หน้า 1/2" · "มีต่อหน้าถัดไป"
- [x] บล็อกลงชื่อครบ (ผู้จัดทำ + ผู้จัดการโครงการ + ขั้น DOA) · คำตัดสินตาม role
- [x] ดูภาพ `_states_sheet.png` + `compare_side.png` แล้ว

## 7. (Replica) ต้นฉบับลูกค้า + ความต่างที่ตั้งใจ
- ต้นฉบับ: `2. FM-PDM-02 แบบฟอร์มรายงานความคืบหน้าโครงการ.docx` (→ orig/SAMPLE.pdf ผ่าน LibreOffice · 4 หน้า Letter) · Doc No. FM-PDM-02 · Rev.00 : 01/07/2569
- Profile: form_fs 8.6pt · lh 1.3 · title 12pt · logo 8mm กลาง · grid row 4.8mm · หัวตารางพื้นเทาอ่อน #F2F2F2
- ความต่าง (ตั้งใจ): 4 หน้า → 2 หน้า (R10) · กล่อง "คำอธิบาย :" เตี้ยลง (ต้นฉบับกล่องเปล่าสูง ~110mm สำหรับเขียนมือ — ระบบพิมพ์ข้อความจริง สูงตามเนื้อหา) · ป้ายช่องข้อมูลโครงการ ไทย : อังกฤษ บรรทัดเดียว (ต้นฉบับ 2 บรรทัด ถ้อยคำเดิม) · โลโก้เฉพาะหน้า 1 (ต้นฉบับอยู่ header ทุกหน้า) · บล็อกลงชื่อ 1 แถว 4 ช่อง (ต้นฉบับ 2×2) + คำตัดสิน ☐ ตรวจสอบแล้ว/☐ อนุมัติ · "ส่งในระบบ/พิจารณาในระบบ" แทนลายมือ · footer เลขที่ + CUBE NATIVE + หน้า · ขนาด A4 แทน Letter · ถ้อยคำคำอธิบาย ☐ ล่าช้าฯ คงตามต้นฉบับ (มีประโยคซ้ำของ ☐ มีความเสี่ยง — OQ ให้ลูกค้ายืนยัน)
- compare_original (หน้า 1): **WARN 0.485** (บรรทัดตรงตำแหน่ง 6/15 · cols 0.68) — อธิบายได้: หน้า 1 ต้นฉบับมีแค่หัว + ข้อ 1 (กล่องเปล่าสูง) ส่วนแบบพิมพ์รวมข้อ 1–3 ตามการออกแบบ 2 หน้า · ดูภาพวางคู่แล้ว ลำดับ/ถ้อยคำ/คอลัมน์ตรงต้นฉบับ

## 8. (Replica) Data contract + สถานะที่ทดสอบ
- parity JS ↔ Python: IDENTICAL 6/6
- สถานะ: draft · pending (ตรวจสอบแล้ว รออนุมัติ) · approved · rejected (ผู้ตรวจสอบไม่ผ่าน · สถานะ ล่าช้า หรือมีปัญหา) · long-12rows (ผลงาน 12 · ปัญหา 12 · KPI 8 · แผนรอบถัดไป 10 · ประเด็น 6 · dense) · approved-doa6steps (8 ช่อง 2 แถว) → ทุกสถานะ 2 หน้า (`out/_states.json`)

## 9. (Replica) print_config
```json
{
  "doc_type": "PPR",
  "mode": "replica",
  "template_ref": "form.tpl.html",
  "template_version": "v1",
  "profile_ref": "profile.json",
  "form_code": "FM-PDM-02",
  "revision": "Rev.00 : 01/07/2569",
  "paper": "A4-portrait",
  "pages": 2,
  "page_break": "ก่อนข้อ 4 ปัญหา อุปสรรค และความเสี่ยง (หน้า 1 = ข้อมูลโครงการ + ข้อ 1–3 · หน้า 2 = ข้อ 4–6 + บล็อกลงชื่อ)",
  "min_rows": { "performance": 9, "kpis": 8, "issues": 11, "next_plan": 10, "decisions_needed": 11 },
  "dense_when_rows_over": { "performance": 9, "kpis": 8, "issues": 11, "next_plan": 10, "decisions_needed": 11 },
  "header_source": "organization_snapshot_at_numbering",
  "sign_boxes": [
    { "box": "requester", "label": "ผู้จัดทำรายงาน (Prepared by)", "show_date": true },
    { "box": "submitter", "label": "ผู้จัดการโครงการ (Project Manager)", "source": "project.manager (ผู้ส่งรายงาน)", "show_date": true },
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
    "source": "ผู้จัดทำ + ผู้จัดการโครงการ (ผู้ส่ง) + approval_chain snapshot (จำนวนขั้นตามที่ตั้งใน DOA)",
    "render": "B6 เส้นประ + (ชื่อ) + บทบาท + วันที่ ตามกระดาษ · แถวละ ≤4",
    "max_per_row": 4,
    "split": "even",
    "dense_when_steps_over": 4,
    "keep_together": true
  }
}
```

## §A DATA CONTRACT — รายงานความคืบหน้าโครงการ (PPR)

> สัญญาข้อมูลระหว่าง backend ↔ template (`form.tpl.html`) · ใช้ทั้ง prototype (tpl_render.js) และ server (render_doc.py)
> กติกา: ค่าแสดงทุกตัวเป็น string ที่จัดรูปแล้ว · boolean ใช้เป็นเงื่อนไขเท่านั้น · checkbox = "☑"/"☐" · ว่าง = "" · ไม่มี {} ว่าง

| key | Source (entity.field / engine) | ตัวอย่าง (สมมติ) | หมายเหตุ |
|---|---|---|---|
| `company.name` · `company.logo` | Organization → header_snapshot (ตอนออกเลข) | `บริษัท ตัวอย่าง จำกัด` · data URI | ไม่ดึงสดหลังออกเลข |
| `doc.title` · `doc.no` · `doc.is_draft` | ค่าคงที่ · ENG-DOC-NUM (PPR) · status = draft | `รายงานความคืบหน้าโครงการ` · `PPR-2569-0001` | ออกเลขตอนบันทึกครั้งแรก |
| `doc.form_code` · `doc.revision` | F-DOCCFG `print_config` | `FM-PDM-02` · `Rev.00 : 01/07/2569` | |
| `project.code` | progress_report.project_plan_id → project_plan.doc_no (F-TMP-004) | `PJP-2569-0004` | เลือกเฉพาะ PJP อนุมัติแล้ว |
| `project.name` | project_plan.project_name (snapshot ตอนส่ง) | `ปรับปรุงระบบจัดเก็บสินค้าคลังกลาง` | |
| `project.manager` | project_plan.project_manager_id → Employee.full_name | `สมชาย ใจดี` | PDPA · snapshot ตอนส่ง |
| `report.period` | progress_report.period_from / period_to | `1 พฤศจิกายน 2569 – 15 พฤศจิกายน 2569` | to ≥ from |
| `report.date` | progress_report.report_date | `18 พฤศจิกายน 2569` | |
| `status.on_track_box/at_risk_box/delayed_box` | progress_report.overall_status | `☑` / `☐` | เลือก 1 |
| `status_note` | progress_report.status_note | ข้อความ | |
| `performance[].no/activity/plan/actual/pct/remarks` | progress_report_performance.* | `1` · `70` | ≥ 9 แถว · pct 0–100 |
| `schedule.plan/actual/status` | progress_report.schedule_* | `3 พ.ย. 2569 – 26 ก.พ. 2570` | plan ค่าเริ่มจาก PJP |
| `budget.plan/actual/status` | progress_report.budget_* | `445,000.00` | plan ค่าเริ่ม = รวมงบอนุมัติ PJP |
| `kpis[].no/metric/plan/actual/status` | progress_report_kpi.* | `1` · `เวลาหยิบเฉลี่ยต่อใบ` | ≥ 8 แถว (เลข 1–8 คงที่) |
| `issues[].description/impact/resolution/owner_due` | progress_report_issue.* · owner → Employee.full_name + due_date | `กานดา จัดหา / 20 พ.ย. 2569` | ≥ 11 แถว |
| `next_plan[].description/owner_due` | progress_report_next.* | `มานพ วางแผน / 5 ธ.ค. 2569` | ≥ 10 แถว |
| `decisions_needed[].topic/options/recommendation/impact` | progress_report_decision.* | ข้อความ | ≥ 11 แถว |
| `sign_rows[].signs[]` → `role` · `name` · `position` · `date` · `decision{approve_box,reject_box,approve_word,reject_word}` | ผู้จัดทำ + ผู้จัดการโครงการ (ผู้ส่ง · submitted_by/submitted_at) + `approval_chain` (DOA snapshot) via sign_rows.py | `ผู้ตรวจสอบ (Reviewed by)` · `☑ ตรวจสอบแล้ว ☐ ไม่ผ่านการตรวจสอบ` | จำนวน = 2 + ขั้น DOA · คำตัดสินตาม role |
| `layout.dense` | แถวใดเกิน min_rows หรือ ขั้น DOA > 4 | `true` | |
