# PRINT SPEC — แบบฟอร์มร้องขอดำเนินการด้าน IT (ITRS)

> เอกสารประกอบสำหรับ Dev — คู่กับ FRD/UI Brief ของ F-TMP-001 · โหมด **Replica** (แบบฟอร์มลูกค้า FM-ITS-01)
> ไฟล์คู่: `ITRS_template.html` (master, fonts ฝัง) · `form.tpl.html` (template logic-less) · `*.data.json` (5 สถานะ) · `out/*.html`
> ⚠️ **[NO-BROWSER]** เครื่องที่ทำงานไม่มี browser → ยังไม่ได้ render PDF/PNG ด้วย `render_pdf.py` / `render_states.py` และยังไม่รัน `compare_original.py` — ต้องรันรอบเต็มบนเครื่องที่มี browser
> ทุกมติที่อ้าง = AI-DEFAULT รอลูกค้ายืนยัน (DECISIONS.lock)

## 1. สรุป
- **ประเภทเอกสาร:** แบบฟอร์มร้องขอดำเนินการด้าน IT / IT Request Form · Doc. No. FM-ITS-01
- **ขนาด:** A4 แนวตั้ง 1 หน้า (กระดาษต้นฉบับ 1 หน้า · ไม่เข้าเงื่อนไข R10)
- **ฟอนต์:** Sarabun (ฝัง) · หมึกเดียวตาม profile
- **Renderer:** Playwright/Chromium (`prefer_css_page_size`, `print_background`)

## 2. Field Mapping
| ช่องในเอกสาร | Source | Format | บังคับ | หมายเหตุ |
|---|---|---|---|---|
| เลขที่ (ช่องขวาบน แทน "ITRS.") | ENG-DOC-NUM · doc_type ITRS | `ITRS-พ.ศ.-running` | ✓ | ออกตอนบันทึกครั้งแรก (DEC-10) |
| วันที่ | req_date (auto) | วัน เดือนไทย พ.ศ. | ✓ | |
| ตำแหน่ง | Employee.position | — | ✓ | แก้สะกด ตําแหน่ง→ตำแหน่ง (DEC-13) |
| ชื่อ-นามสกุล | Employee.full_name | — | ✓ | PDPA |
| วันที่ต้องการส่งมอบ | due_date | วันที่ไทย | ✓ | ≥ วันที่ขอ (เตือน · DEC-14) |
| สถานที่ส่งมอบ | delivery_location | — | ✓ | |
| เรื่องที่ต้องการ | subject | — | ✓ | |
| ประเภทงาน ☐×6 | job_type[] (multi) | "☑"/"☐" | ✓ ≥1 | อื่นๆ → job_type_other บังคับ (DEC-15) |
| รายละเอียดการร้องขอ | detail → detail_lines[] | แตกบรรทัดตาม \n | ✓ | ขั้นต่ำ 4 แถวตามกระดาษ |
| เหตุผล วัตถุประสงค์ หรือ ความจำเป็น | reason → reason_lines[] | | ✓ | ขั้นต่ำ 3 แถว |
| มาตรฐาน หรือ Spec ที่ต้องการ | spec → spec_lines[] | | — | ขั้นต่ำ 4 แถว |
| ผู้ร้องขอ | requester + submitted_at | "ส่งในระบบ …" | ✓ | |
| ตรวจสอบโดย (ช่องต่อขั้น DOA) | approval_chain[] | ☑ อนุมัติ / ☑ ไม่อนุมัติ + "พิจารณาในระบบ …" | ✓ | จำนวนช่องตาม DOA กลาง (DEC-03/07) |
| ดำเนินการโดย | performed_by · performed_at | "ดำเนินการในระบบ …" | หลังอนุมัติ | เจ้าหน้าที่ IT (role-it-officer — ยังไม่อยู่ใน DOA contract) |

## 3. กติกาคำนวณ
- ไม่มีสูตร/ค่าคงที่บนกระดาษ · แตกข้อความหลายบรรทัดเป็น `*_lines[]` แล้วเติมแถวว่างให้ครบขั้นต่ำ · เกินขั้นต่ำ → `layout.dense`

## 4. กติกาการพิมพ์
- ตารางกรอบ R9 · ลายเซ็น+footer ชิดล่าง (`.doc-bottom`) · `.signs-block` ไม่ตัดข้ามหน้า · แถวละ ≤4 ช่อง

## 5. วิธี build ใหม่
```bash
python3 make_data.py                                     # data 5 สถานะ (ข้อมูลสมมติ)
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "แบบฟอร์มร้องขอดำเนินการด้าน IT" --max-pages 1
python3 $TD/scripts/compare_original.py ../orig/SAMPLE.pdf out/approved.pdf -o out/compare --region 0:0.72
```

## 6. Checklist
- [x] parity JS ↔ Python IDENTICAL 5/5
- [x] ไม่มี {{…}} หลง (ทุกสถานะ)
- [ ] A4 1 หน้า ทุกสถานะ — **[NO-BROWSER] ยังไม่ยืนยันด้วย render_states บนเครื่องงาน** (ตรวจภาพเบื้องต้นนอกเครื่องงานด้วย Chromium: 5/5 = 1 หน้า · ไม่ใช่ผลด่านทางการ)
- [x] ลายเซ็นครบ: ผู้ร้องขอ + ขั้น DOA + ดำเนินการโดย

## 7. (Replica) ต้นฉบับ + ความต่างที่ตั้งใจ
- ต้นฉบับ: `1. FM-ITS-01 แบบฟอร์มขอรับบริการด้านเทคโนโลยีสารสนเทศ.xlsx` · Doc. No. FM-ITS-01 · Rev. — (ไม่มีบนกระดาษ → Rev.00 รอยืนยัน)
- Profile: form_title_fs 15pt · form_logo_h 11mm · form_title_gap 4px · form_grid_gap 6px · form_cb_fs 11pt
- ความต่างที่ตั้งใจ: (1) ช่อง "ITRS." ขวาบนแสดงเลขที่เอกสารเต็ม `ITRS-2569-xxxx` (prefix เดียวกัน ไม่พิมพ์ "ITRS." ซ้ำ) (2) ช่อง ตรวจสอบโดย = 1 ช่องต่อขั้น DOA + ☐ อนุมัติ/ไม่อนุมัติ (3) ใต้เส้นลงชื่อ = (ชื่อ) + บรรทัดวันที่ "ส่ง/พิจารณา/ดำเนินการในระบบ …" แทน (…/…/…) (4) footer เลขที่/ร่าง + Doc. No. · Rev. (5) แก้สะกด ตำแหน่ง (6) ลายเซ็นชิดล่างหน้า
- compare_original: **[NO-BROWSER] ข้าม** (ต้องมี approved.pdf) — รันรอบเต็มบนเครื่องที่มี browser

## 8. (Replica) Data contract + สถานะ
| key | Source | ตัวอย่าง | หมายเหตุ |
|---|---|---|---|
| `company.name` · `company.logo` | Organization header_snapshot | data URI | ไม่ดึงสดหลังออกเลข |
| `doc.title` · `doc.no` · `doc.is_draft` | ค่าคงที่ · ENG-DOC-NUM · status | `ITRS-2569-0007` | |
| `doc.form_code` · `doc.revision` | F-DOCCFG print_config | `FM-ITS-01` · `Rev.00` | |
| `req_date` · `due_date` | itrs.req_date · itrs.due_date | `10 ตุลาคม 2569` | string จัดรูปแล้ว |
| `employee.name` · `employee.position` | Employee snapshot | | PDPA |
| `delivery_location` · `subject` | itrs.* | | |
| `job_type.{buy_device,user_email,install_software,install_accessory,internet_wifi,other}` | itrs.job_types[] | "☑"/"☐" | |
| `job_type_other` | itrs.job_type_other | | ว่างเมื่อไม่ติ๊ก อื่นๆ |
| `detail_lines[]` · `reason_lines[]` · `spec_lines[]` → `text` | itrs.detail / reason / spec | | เติมแถวว่าง 4/3/4 |
| `sign_rows[].signs[]` → role · name · position · date · decision | ผู้ร้องขอ + approval_chain + performer | | sign_rows.py / tplSignRows |
| `layout.dense` | บรรทัดเกินขั้นต่ำ หรือ DOA > 4 ขั้น | | |

- parity: IDENTICAL 5/5
- สถานะ: draft · approved (ดำเนินการแล้ว) · rejected (อื่นๆ) · long-text (7/4/6 บรรทัด → dense) · approved-doa6steps (8 ช่อง 4+4) → HTML ครบ · PDF [NO-BROWSER]

## 9. (Replica) print_config
```json
{
  "doc_type": "ITRS",
  "mode": "replica",
  "template_ref": "form.tpl.html",
  "template_version": "v1",
  "profile_ref": "profile.json",
  "form_code": "FM-ITS-01",
  "revision": "Rev.00",
  "revision_note": "กระดาษไม่มี Rev. — ค่าเริ่ม Rev.00 รอลูกค้ายืนยัน (DEC-12)",
  "paper": "A4-portrait",
  "pages": 1,
  "min_rows": 4,
  "text_min_rows": { "detail_lines": 4, "reason_lines": 3, "spec_lines": 4 },
  "dense_when_rows_over": 4,
  "header_source": "organization_snapshot_at_numbering",
  "sign_boxes": [
    { "box": "requester", "label": "ผู้ร้องขอ", "show_date": true },
    { "box": "doa_step:*", "label": "from_doa_step", "show_decision": true, "show_date": true },
    { "box": "performer", "label": "ดำเนินการโดย", "show_date": true, "source": "performed_by / performed_at (เจ้าหน้าที่ IT กด ดำเนินการแล้ว) — ไม่ใช่ขั้น DOA" }
  ],
  "decision_words": {
    "default": { "approve": "อนุมัติ", "reject": "ไม่อนุมัติ" },
    "by_role": {}
  },
  "config_reads": {},
  "footer_left": "เลขที่ {doc.no} · (ร่าง) · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE",
  "footer_right": "Doc. No. : {form_code} · {revision}",
  "sign_layout": {
    "source": "approval_chain snapshot (ผู้ร้องขอ + จำนวนขั้นตามที่ตั้งใน DOA) + ช่องดำเนินการโดย ท้ายสุด",
    "max_per_row": 4,
    "split": "even",
    "dense_when_steps_over": 4,
    "keep_together": true
  }
}
```
