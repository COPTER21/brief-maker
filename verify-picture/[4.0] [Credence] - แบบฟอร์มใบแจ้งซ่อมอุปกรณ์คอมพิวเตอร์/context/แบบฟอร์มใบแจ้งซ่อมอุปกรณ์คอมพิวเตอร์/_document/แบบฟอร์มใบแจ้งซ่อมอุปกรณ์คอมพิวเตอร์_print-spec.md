# PRINT SPEC — แบบฟอร์มใบแจ้งซ่อมอุปกรณ์คอมพิวเตอร์ (CRR)

> เอกสารประกอบสำหรับ Dev — คู่กับ FRD/UI Brief ของ F-TMP-004 · โหมด **Replica** (แบบฟอร์มลูกค้า FM-ITS-06)
> ไฟล์คู่: `แบบฟอร์มใบแจ้งซ่อมอุปกรณ์คอมพิวเตอร์_template.html` (master, fonts ฝัง) · `form.tpl.html` (template logic-less) · `*.data.json` (5 สถานะ) · `out/*.html`
> ⚠️ **[NO-BROWSER]** เครื่องที่ทำงานไม่มี browser → ยังไม่ได้ render PDF/PNG ด้วย `render_pdf.py` / `render_states.py` และยังไม่รัน `compare_original.py` — ต้องรันรอบเต็มบนเครื่องที่มี browser (`--max-pages 2`)
> ทุกมติที่อ้าง = AI-DEFAULT รอลูกค้ายืนยัน (DECISIONS.lock)

## 1. สรุป
- **ประเภทเอกสาร:** แบบฟอร์มใบแจ้งซ่อมอุปกรณ์คอมพิวเตอร์ · Doc. No. FM-ITS-06 · Rev.00 : 01/07/2569
- **ขนาด:** A4 แนวตั้ง **2 หน้า (R10)** — ต้นฉบับ 1 หน้าเต็ม (เหลือที่ ~15%) แต่ระบบแสดงชื่อ/วันที่ในระบบใต้ลายเซ็นทุกจุด + สายอนุมัติ dynamic (ทดสอบ 6 ขั้น = 7 ช่อง 2 แถว) → 1 หน้าล้น · ออกแบบ 2 หน้าตั้งใจ: **หน้า 1** = หัว + ส่วนที่ 1 + ลงชื่อ ผู้แจ้งซ่อม/ผู้รับแจ้ง · **หน้า 2** = หัวย่อ (ชื่อเอกสาร + แถว เลขที่เอกสาร/วันที่ ซ้ำ) + ส่วนที่ 2 + บล็อก ผู้ดำเนินการ/อนุมัติโดย (ทั้งก้อน) + ผลการซ่อม + ลงชื่อ ผู้ดำเนินการ/ผู้แจ้งซ่อม
- จุดตัดหน้า: `.doc-page.page-break` ก่อน "ส่วนที่ 2" · ท้ายหน้า 1 มี `.cont-note` "มีต่อหน้าถัดไป" · footer ทุกหน้ามี `.page-no` "หน้า 1/2" / "หน้า 2/2" + เลขที่เอกสาร · ทุกสถานะ 2 หน้าเท่ากัน · ฟอนต์เนื้อหา 9.6pt (ไม่ต่ำกว่า 8pt)
- **ฟอนต์:** Sarabun (ฝัง) · หมึกเดียวตาม profile
- **Renderer:** Playwright/Chromium (`prefer_css_page_size`, `print_background`)

## 2. Field Mapping
| ช่องในเอกสาร | Source | Format | บังคับ | หมายเหตุ |
|---|---|---|---|---|
| เลขที่เอกสาร | ENG-DOC-NUM · doc_type CRR | `CRR-พ.ศ.-running` | ✓ | ออกตอนบันทึกครั้งแรก (DEC-10) |
| วันที่ (หัวตาราง) | crr.doc_date (auto) | วัน เดือนไทย พ.ศ. | ✓ | วันที่บันทึกครั้งแรก |
| วันที่ (ส่วนที่ 1) | crr.report_date (auto) | วันที่ไทย | ✓ | วันที่ส่งแจ้งซ่อม · ร่าง = ว่าง |
| ตำแหน่ง | Employee.position | — | ✓ | แก้สะกด ตําแหน่ง→ตำแหน่ง (DEC-12) |
| ชื่อ-นามสกุล | Employee.full_name | — | ✓ | PDPA |
| วันที่ต้องการส่งมอบ | crr.due_date | วันที่ไทย | ✓ | ≥ วันที่แจ้ง (เตือน · DEC-17) |
| สถานที่ส่งมอบ | crr.delivery_location | — | ✓ | |
| ประเภท ☐×4 | crr.device_type (เลือก 1) | "☑"/"☐" | ✓ | อื่นๆ → device_type_other บังคับ (DEC-18) |
| รายการ | crr.item_name | — | ✓ | |
| รหัสทรัพย์สิน | crr.asset_code | — | — | ผู้ใช้กรอก (ไม่ผูกทะเบียนทรัพย์สิน · DEC-01) |
| อาการเสีย / ปัญหา | crr.problem → problem_lines[] | แตกบรรทัดตาม \n | ✓ | ขั้นต่ำ 2 แถวตามกระดาษ |
| ผู้แจ้งซ่อม / ผู้รับแจ้ง (ส่วนที่ 1) | owner + submitted_at · received_by + received_at | "ส่งในระบบ …" / "รับแจ้งในระบบ …" | ✓ | ผู้รับแจ้ง = เจ้าหน้าที่ IT (role-it-officer — ยังไม่อยู่ใน DOA contract) |
| วันที่ดำเนินการซ่อม | crr.repair_date | วันที่ไทย | ✓ (ส่วนที่ 2) | IT กรอก |
| ผลของการตรวจเช็ค/ซ่อม ☐×5 | crr.check_result (เลือก 1) | "☑"/"☐" | ✓ (ส่วนที่ 2) | |
| ระยะเวลา … ถึง … · ระบุร้านค้าที่ส่งเคลม · วันที่ส่งเคลม (×3 ชุด) | crr.claim_period_from/to · claim_vendor · claim_date | วันที่ไทย | ✓ เมื่อเลือก 3 ตัวเลือกล่าง | พิมพ์ค่าใต้ตัวเลือกที่เลือกเท่านั้น · ชุดอื่นเส้นประว่าง · แก้สะกด เครม→เคลม (DEC-13) · ถึง ≥ ระยะเวลา (เตือน · DEC-16) |
| ผู้ดำเนินการ + อนุมัติโดย (ช่องต่อขั้น DOA) | inspected_by + approval_submitted_at · approval_chain[] | ☑ อนุมัติ / ☑ ไม่อนุมัติ + "พิจารณาในระบบ …" | ✓ | จำนวนช่องตาม DOA กลาง (DEC-03/07) |
| ผลการซ่อม ☐×2 | crr.repair_result | "☑"/"☐" | ✓ (ปิดงาน) | |
| บรรทัดใต้ผลการซ่อม | crr.repair_note → repair_note_lines[] | | ✓ เมื่อ ไม่สามารถแก้ไขได้ | ขั้นต่ำ 2 แถว |
| ผู้ดำเนินการ / ผู้แจ้งซ่อม (ผลการซ่อม) | repaired_by + repaired_at · owner + acknowledged_at | "บันทึกในระบบ …" / "รับทราบในระบบ …" | ✓ | |

## 3. กติกาคำนวณ
- ไม่มีสูตร/ค่าคงที่บนกระดาษ · แตกข้อความหลายบรรทัดเป็น `*_lines[]` แล้วเติมแถวว่างให้ครบขั้นต่ำ · เกินขั้นต่ำหรือ DOA > 4 ขั้น → `layout.dense`
- ☑/☐ ทำใน data (`device_type.*` · `check_result.*` · `claim_sets[].box` · `repair_result.*`)

## 4. กติกาการพิมพ์
- ตารางกรอบ R9 · บล็อกลงชื่อทุกจุดห่อ `.signs-block` (ไม่ตัดข้ามหน้า) · ช่อง DOA แถวละ ≤4 · คู่ลงชื่อส่วนที่ 1 / ผลการซ่อม คงที่ 2 ช่องตามกระดาษ (ไม่ใช่ขั้น DOA)

## 5. วิธี build ใหม่
```bash
python3 make_data.py                                     # data 5 สถานะ (ข้อมูลสมมติ)
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "แบบฟอร์มใบแจ้งซ่อมอุปกรณ์คอมพิวเตอร์" --max-pages 2
python3 $TD/scripts/compare_original.py ../orig/SAMPLE.pdf out/approved.pdf -o out/compare --region 0:0.45
```

## 6. Checklist
- [x] parity JS ↔ Python IDENTICAL 5/5
- [x] ไม่มี {{…}} หลง (ทุกสถานะ · render_doc --strict)
- [ ] A4 2 หน้า ทุกสถานะ — **[NO-BROWSER] ยังไม่ยืนยันด้วย render_states บนเครื่องงาน** (ตรวจภาพเบื้องต้นนอกเครื่องงานด้วย Chromium: 5/5 = 2 หน้า · ไม่ใช่ผลด่านทางการ)
- [x] ลายเซ็นครบ: ผู้แจ้งซ่อม · ผู้รับแจ้ง · ผู้ดำเนินการ + ขั้น DOA · ผู้ดำเนินการ · ผู้แจ้งซ่อม

## 7. (Replica) ต้นฉบับ + ความต่างที่ตั้งใจ
- ต้นฉบับ: `6. FM-ITS-06 แบบฟอร์มใบแจ้งซ่อมอุปกรณ์คอมพิวเตอร์.xlsx` · Doc. No. FM-ITS-06 · Rev.00 : 01/07/2569 (footer ขวา)
- Profile: form_title_fs 14pt · form_logo_h 11mm · form_title_gap 4px · form_cb_fs 11pt · form_row_gap 3px · form_fill_m 34mm
- ความต่างที่ตั้งใจ: (1) 2 หน้า R10 (ตัดก่อนส่วนที่ 2 · หัวย่อหน้า 2) (2) ช่อง อนุมัติโดย = 1 ช่องต่อขั้น DOA + ☐ อนุมัติ/ไม่อนุมัติ (3) ใต้เส้นลงชื่อ = (ชื่อ) + บรรทัดวันที่ "ส่ง/รับแจ้ง/พิจารณา/บันทึก/รับทราบในระบบ …" แทน (…/…/…) (4) footer เลขที่/ร่าง + Doc. No. · Rev. · หน้า X/2 (5) แก้สะกด ตำแหน่ง · ส่งเคลม · สั่งซื้อ (6) ชุด ระยะเวลา/ร้านค้า/วันที่ส่งเคลม ใต้ตัวเลือก สั่งซื้อ คงคำ "ส่งเคลม" ตามกระดาษ (DEC-15 · OQ ลูกค้า)
- compare_original: **[NO-BROWSER] ข้าม** (ต้องมี approved.pdf) — รันรอบเต็มบนเครื่องที่มี browser · แนะนำ `--region 0:0.45` (หน้า 1 เทียบส่วนที่ 1)

## 8. (Replica) Data contract + สถานะ
| key | Source | ตัวอย่าง | หมายเหตุ |
|---|---|---|---|
| `company.name` · `company.logo` | Organization header_snapshot | data URI | ไม่ดึงสดหลังออกเลข |
| `doc.title` · `doc.no` · `doc.is_draft` | ค่าคงที่ · ENG-DOC-NUM · status | `CRR-2569-0012` | |
| `doc.form_code` · `doc.revision` | F-DOCCFG print_config | `FM-ITS-06` · `Rev.00 : 01/07/2569` | |
| `doc_date` · `report_date` · `due_date` · `repair_date` | crr.* | `10 ตุลาคม 2569` | string จัดรูปแล้ว |
| `employee.name` · `employee.position` | Employee snapshot | | PDPA |
| `delivery_location` · `item_name` · `asset_code` | crr.* | | |
| `device_type.{notebook,workstation,printer,other}` · `device_type_other` | crr.device_type · device_type_other | "☑"/"☐" | |
| `problem_lines[]` · `repair_note_lines[]` → `text` | crr.problem · repair_note | | เติมแถวว่าง 2/2 |
| `signs_part1[]` · `signs_part3[]` → role · name · position · date | owner/receiver · repairer/owner | | คงที่ 2 ช่อง |
| `check_result.{done,in_progress}` · `claim_sets[]` → box · label · period_from · period_to · vendor · claim_date | crr.check_result + claim_* | | 3 ชุดตามกระดาษ · ค่าเฉพาะชุดที่เลือก |
| `sign_rows[].signs[]` → role · name · position · date · decision | ผู้ดำเนินการ (ผู้ส่งอนุมัติ) + approval_chain | | sign_rows.py / tplSignRows |
| `repair_result.{fixed,unfixable}` | crr.repair_result | | |
| `layout.dense` | บรรทัดเกินขั้นต่ำ หรือ DOA > 4 ขั้น | | |

- parity: IDENTICAL 5/5
- สถานะ: draft (ร่าง ส่วนที่ 1) · approved (ปิดงาน · ส่งเคลมในประกัน · แก้ไขเรียบร้อย) · rejected (สั่งซื้อ · ไม่อนุมัติ) · long-text (อื่นๆ · 5/4 บรรทัด → dense · ไม่สามารถแก้ไขได้) · approved-doa6steps (DOA 6 ขั้น → 7 ช่อง 4+3) → HTML ครบ · PDF [NO-BROWSER]

## 9. (Replica) print_config
```json
{
  "doc_type": "CRR",
  "mode": "replica",
  "template_ref": "form.tpl.html",
  "template_version": "v1",
  "profile_ref": "profile.json",
  "form_code": "FM-ITS-06",
  "revision": "Rev.00 : 01/07/2569",
  "paper": "A4-portrait",
  "pages": 2,
  "page_break": "ก่อน ส่วนที่ 2 (R10 · ส่วนกรอกหลายหมวด + สายอนุมัติ dynamic สูงสุด 6+ ขั้น) · หัวตาราง เลขที่เอกสาร/วันที่ ซ้ำหน้า 2 · มีต่อหน้าถัดไป · หน้า X/2",
  "min_rows": 2,
  "text_min_rows": { "problem_lines": 2, "repair_note_lines": 2 },
  "dense_when_rows_over": 2,
  "header_source": "organization_snapshot_at_numbering",
  "sign_boxes": [
    { "box": "reporter", "label": "ผู้แจ้งซ่อม", "show_date": true, "section": "ส่วนที่ 1", "source": "owner · submitted_at" },
    { "box": "receiver", "label": "ผู้รับแจ้ง", "show_date": true, "section": "ส่วนที่ 1", "source": "received_by / received_at (เจ้าหน้าที่ IT กด รับแจ้ง) — ไม่ใช่ขั้น DOA" },
    { "box": "inspector", "label": "ผู้ดำเนินการ", "show_date": true, "section": "ส่วนที่ 2", "source": "inspected_by / approval_submitted_at (ผู้ส่งอนุมัติ = ผู้ขอของ DOA)" },
    { "box": "doa_step:*", "label": "from_doa_step", "show_decision": true, "show_date": true, "section": "ส่วนที่ 2" },
    { "box": "repairer", "label": "ผู้ดำเนินการ", "show_date": true, "section": "ผลการซ่อม", "source": "repaired_by / repaired_at" },
    { "box": "acknowledger", "label": "ผู้แจ้งซ่อม", "show_date": true, "section": "ผลการซ่อม", "source": "owner · acknowledged_at (ผู้แจ้งกด รับทราบผล)" }
  ],
  "decision_words": {
    "default": { "approve": "อนุมัติ", "reject": "ไม่อนุมัติ" },
    "by_role": {}
  },
  "config_reads": {},
  "footer_left": "เลขที่ {doc.no} · (ร่าง) · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE",
  "footer_right": "Doc. No. : {form_code} · {revision}",
  "sign_layout": {
    "source": "approval_chain snapshot (ผู้ดำเนินการผู้ส่งอนุมัติ + จำนวนขั้นตามที่ตั้งใน DOA) วางในส่วนที่ 2 ตามตำแหน่งบนกระดาษ · คู่ลงชื่อส่วนที่ 1 / ผลการซ่อม คงที่ 2 ช่องตามกระดาษ",
    "max_per_row": 4,
    "split": "even",
    "dense_when_steps_over": 4,
    "keep_together": true
  }
}
```
