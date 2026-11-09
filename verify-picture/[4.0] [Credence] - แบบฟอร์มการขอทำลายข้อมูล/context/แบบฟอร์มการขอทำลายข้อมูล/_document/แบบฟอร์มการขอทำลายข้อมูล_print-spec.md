# PRINT SPEC — แบบฟอร์มการขอทำลายข้อมูล (DRITS)

> เอกสารประกอบสำหรับ Dev — คู่กับ FRD/UI Brief ของ F-TMP-003 · โหมด **Replica** (แบบฟอร์มลูกค้า FM-ITS-02)
> ไฟล์คู่: `DRITS_template.html` (master, fonts ฝัง) · `form.tpl.html` (template logic-less) · `*.data.json` (5 สถานะ) · `out/*.html`
> ⚠️ **[NO-BROWSER]** เครื่องที่ทำงานไม่มี browser → ยังไม่ได้ render PDF/PNG ด้วย `render_pdf.py` / `render_states.py` และยังไม่รัน `compare_original.py` — ต้องรันรอบเต็มบนเครื่องที่มี browser
> ทุกมติที่อ้าง = AI-DEFAULT รอลูกค้ายืนยัน (DECISIONS.lock)

## 1. สรุป
- **ประเภทเอกสาร:** แบบฟอร์มการขอทำลายข้อมูล / Data Destruction Request Form · Doc. No. FM-ITS-02 · Rev.00 : 01/07/2569
- **ขนาด:** A4 แนวตั้ง 1 หน้า (กระดาษต้นฉบับ 1 หน้า · ไม่เข้าเงื่อนไข R10)
- **ฟอนต์:** Sarabun (ฝัง) · หมึกเดียวตาม profile · หัวช่องพื้นเทาตามกระดาษ
- **Renderer:** Playwright/Chromium (`prefer_css_page_size`, `print_background`)

## 2. Field Mapping
| ช่องในเอกสาร | Source | Format | บังคับ | หมายเหตุ |
|---|---|---|---|---|
| เลขที่เอกสาร (แทน "DRITS.") | ENG-DOC-NUM · doc_type DRITS | `DRITS-พ.ศ.-running` | ✓ | ออกตอนบันทึกครั้งแรก (DEC-10) |
| วันที่ | req_date (auto) | วัน เดือนไทย พ.ศ. | ✓ | |
| ชื่อ-นามสกุล | Employee.full_name | — | ✓ | PDPA |
| ตำแหน่ง | Employee.position | — | ✓ | แก้สะกด ตําแหน่ง→ตำแหน่ง (DEC-12) |
| รายละเอียดของข้อมูลที่ต้องการทำลาย | detail → detail_lines[] | แตกบรรทัดตาม \n | ✓ | ขั้นต่ำ 3 แถวตามกระดาษ |
| โปรแกรม | program → program_lines[] | | ✓ | ขั้นต่ำ 2 แถว |
| ประเภทข้อมูล ☐×10 | data_types[] (multi) | "☑"/"☐" | ✓ ≥1 | DEC-17 |
| ช่วงเวลาของข้อมูล จาก / ถึง | period_from · period_to | วันที่ไทย | ✓ | ถึง ≥ จาก (บังคับ) · ถึง ≤ วันที่ขอ (เตือน) DEC-15 |
| เหตุผลในการทำลายข้อมูล ☐×4 | destroy_reasons[] + destroy_reason_other | "☑"/"☐" | ✓ ≥1 | อื่นๆ ต้องระบุ (DEC-16) · แถวว่างท้าย = `destroy_reason_more` (ว่างไว้ตามกระดาษ) |
| วิธีการทำลายข้อมูล ☐×4 | destroy_methods[] + destroy_method_other | "☑"/"☐" | ✓ ≥1 | ☐ หน้า เข้ารหัสฯ แสดงครบ (DEC-14) · แถวว่างท้าย = `destroy_method_more` |
| ผู้ร้องขอ | requester + submitted_at | "ส่งในระบบ …" | ✓ | |
| ตรวจสอบ / อนุมัติ (ช่องต่อขั้น DOA) | approval_chain[] | ☑ อนุมัติ / ☑ ไม่อนุมัติ + "พิจารณาในระบบ …" | ✓ | ค่าเริ่ม 2 ขั้น · จำนวนช่องตาม DOA กลาง (DEC-03/07) · แก้สะกด อนุมัมติ→อนุมัติ (DEC-13) |
| เจ้าหน้าที่ IT | performed_by · performed_at | "ทำลายในระบบ …" | หลังอนุมัติ | ผู้ดำเนินการทำลาย (role-it-officer — ยังไม่อยู่ใน DOA contract) · ไม่ใช่ขั้น DOA |

## 3. กติกาคำนวณ
- ไม่มีสูตร/ค่าคงที่บนกระดาษ · แตกข้อความหลายบรรทัดเป็น `*_lines[]` แล้วเติมแถวว่างให้ครบขั้นต่ำ · เกินขั้นต่ำ → `layout.dense`

## 4. กติกาการพิมพ์
- ตารางกรอบ R9 · ลายเซ็น+footer ชิดล่าง (`.doc-bottom`) · `.signs-block` ไม่ตัดข้ามหน้า · แถวละ ≤4 ช่อง

## 5. วิธี build ใหม่
```bash
python3 make_data.py                                     # data 5 สถานะ (ข้อมูลสมมติ)
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "แบบฟอร์มการขอทำลายข้อมูล" --max-pages 1
python3 $TD/scripts/compare_original.py ../orig/SAMPLE.pdf out/approved.pdf -o out/compare --region 0:0.6
```

## 6. Checklist
- [x] parity JS ↔ Python IDENTICAL 5/5
- [x] ไม่มี {{…}} หลง · ไม่มี key ขาด (ทุกสถานะ)
- [ ] A4 1 หน้า ทุกสถานะ — **[NO-BROWSER] ยังไม่ยืนยันด้วย render_states บนเครื่องงาน** (ตรวจเบื้องต้นนอกเครื่องงานด้วย Chromium: long-text + doa6steps = 1 หน้า · ไม่ใช่ผลด่านทางการ)
- [x] ลายเซ็นครบ: ผู้ร้องขอ + ขั้น DOA + เจ้าหน้าที่ IT

## 7. (Replica) ต้นฉบับ + ความต่างที่ตั้งใจ
- ต้นฉบับ: `2. FM-ITS-02 แบบฟอร์มการขอทำลายข้อมูลเอกสารประจำปี.xlsx` · Doc. No. FM-ITS-02 · Rev.00 : 01/07/2569 (footer)
- Profile: form_title_fs 15pt · form_logo_h 11mm · form_grid_head_bg #BFBFBF · form_cb_fs 11pt
- ความต่างที่ตั้งใจ: (1) ช่อง "DRITS." แสดงเลขที่เต็ม `DRITS-2569-xxxx` (2) ช่องลงชื่อ = ผู้ร้องขอ + 1 ช่องต่อขั้น DOA (ค่าเริ่ม ตรวจสอบ · อนุมัติ) + เจ้าหน้าที่ IT **ท้ายสุด** — กระดาษวาง เจ้าหน้าที่ IT ก่อน อนุมัติ แต่ในระบบ IT ลงชื่อเมื่อทำลายเสร็จหลังอนุมัติ และขั้น DOA ต้องต่อเนื่องกัน (dynamic N ขั้น) (3) ใต้เส้นลงชื่อ = (ชื่อ) + "ส่ง/พิจารณา/ทำลายในระบบ …" แทน (…/…/…) (4) footer เลขที่/ร่าง + Doc. No. · Rev. (5) แก้สะกด ตำแหน่ง · อนุมัติ (6) ☐ ครบหน้า "เข้ารหัสและทำลายข้อมูลอย่างปลอดภัย" (7) ลายเซ็นชิดล่างหน้า
- compare_original: **[NO-BROWSER] ข้าม** (ต้องมี approved.pdf) — รันรอบเต็มบนเครื่องที่มี browser

## 8. (Replica) Data contract + สถานะ
| key | Source | ตัวอย่าง | หมายเหตุ |
|---|---|---|---|
| `company.name` · `company.logo` | Organization header_snapshot | data URI | ไม่ดึงสดหลังออกเลข |
| `doc.title` · `doc.no` · `doc.is_draft` | ค่าคงที่ · ENG-DOC-NUM · status | `DRITS-2569-0003` | |
| `doc.form_code` · `doc.revision` | F-DOCCFG print_config | `FM-ITS-02` · `Rev.00 : 01/07/2569` | |
| `req_date` · `period_from` · `period_to` | drits.* | `10 ตุลาคม 2569` | string จัดรูปแล้ว |
| `employee.name` · `employee.position` | Employee snapshot | | PDPA |
| `detail_lines[]` · `program_lines[]` → `text` | drits.detail / program | | เติมแถวว่าง 3/2 |
| `data_type.{customer,employee,finance,contract,inventory,system,marketing,internal_doc,sales,other}` | drits.data_types[] | "☑"/"☐" | |
| `destroy_reason.{retention_expired,duplicate_obsolete,authority_order,other}` · `destroy_reason_other` · `destroy_reason_more` | drits.destroy_reasons[] | | |
| `destroy_method.{permanent_delete,encrypt_destroy,licensed_software,other}` · `destroy_method_other` · `destroy_method_more` | drits.destroy_methods[] | | |
| `sign_rows[].signs[]` → role · name · position · date · decision | ผู้ร้องขอ + approval_chain + performer | | sign_rows.py / tplSignRows |
| `layout.dense` | บรรทัดเกินขั้นต่ำ หรือ DOA > 4 ขั้น | | |

- parity: IDENTICAL 5/5
- สถานะ: draft · approved (ทำลายแล้ว) · rejected (ขั้น 2 ไม่อนุมัติ) · long-text (6/3 บรรทัด → dense) · approved-doa6steps (8 ช่อง 4+4) → HTML ครบ · PDF [NO-BROWSER]

## 9. (Replica) print_config
```json
{
  "doc_type": "DRITS",
  "mode": "replica",
  "template_ref": "form.tpl.html",
  "template_version": "v1",
  "profile_ref": "profile.json",
  "form_code": "FM-ITS-02",
  "revision": "Rev.00 : 01/07/2569",
  "revision_note": "ตามท้ายกระดาษ Doc. No. : FM-ITS-02 Rev.00 : 01/07/2569",
  "paper": "A4-portrait",
  "pages": 1,
  "min_rows": 3,
  "text_min_rows": { "detail_lines": 3, "program_lines": 2 },
  "dense_when_rows_over": 3,
  "header_source": "organization_snapshot_at_numbering",
  "sign_boxes": [
    { "box": "requester", "label": "ผู้ร้องขอ", "show_date": true },
    { "box": "doa_step:*", "label": "from_doa_step", "show_decision": true, "show_date": true },
    { "box": "performer", "label": "เจ้าหน้าที่ IT", "show_date": true, "source": "performed_by / performed_at (เจ้าหน้าที่ IT กด บันทึกการทำลายแล้ว) — ไม่ใช่ขั้น DOA" }
  ],
  "decision_words": {
    "default": { "approve": "อนุมัติ", "reject": "ไม่อนุมัติ" },
    "by_role": {}
  },
  "config_reads": {},
  "footer_left": "เลขที่ {doc.no} · (ร่าง) · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE",
  "footer_right": "Doc. No. : {form_code} · {revision}",
  "sign_layout": {
    "source": "approval_chain snapshot (ผู้ร้องขอ + จำนวนขั้นตามที่ตั้งใน DOA) + ช่องเจ้าหน้าที่ IT ท้ายสุด",
    "max_per_row": 4,
    "split": "even",
    "dense_when_steps_over": 4,
    "keep_together": true
  }
}
```
