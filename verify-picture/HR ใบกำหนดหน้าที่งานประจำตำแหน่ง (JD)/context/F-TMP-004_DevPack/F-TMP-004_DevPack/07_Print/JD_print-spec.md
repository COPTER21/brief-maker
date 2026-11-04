# PRINT SPEC — ใบกำหนดหน้าที่งานประจำตำแหน่ง (Job Description) (JD)

> เอกสารประกอบสำหรับ Dev — แนบคู่กับ FRD/Brief ของ F-TMP-004
> ไฟล์คู่: `JD_template.html` (master, fonts ฝัง) · `out/*.html` (ทุกสถานะ) — [NO-BROWSER] ยังไม่มี PDF ตัวอย่าง
> **โหมด:** Replica (แบบฟอร์มลูกค้า FM-HRM-32)

## 1. สรุป
- **ประเภทเอกสาร:** ใบกำหนดหน้าที่งานประจำตำแหน่ง / Job Description
- **ขนาด:** A4 แนวตั้ง · ฟอนต์ Sarabun ฝัง base64 · หมึกตาม profile ลูกค้า
- **Renderer:** Playwright/Chromium (`render_pdf.py`) — รอบนี้ข้าม (NO-BROWSER)

## 2. Field Mapping
ดู `JD_data-contract.md` (key ↔ entity.field ↔ ตัวอย่าง)

## 3. กติกาคำนวณ
- `subordinate_summary` = "N ตำแหน่ง · M คน" จากแถวลูกน้องที่มีตำแหน่ง · ไม่มี = "ไม่มี" (DEC-13)
- ข้อความยาว: แยกบรรทัดตาม \n · ไม่ตัดคำในบรรทัดเอง (ให้ CSS ตัด)

## 4. กติกาการพิมพ์
- ตารางลงนามห่อ `.signs-block` ไม่ตัดข้ามหน้า · เนื้อหายาวขึ้นหน้า 2 ได้ (กระดาษต้นฉบับ 2 หน้า)

## 5. วิธี build ใหม่
```bash
python3 make_print.py                         # สร้าง form.tpl.html + *.data.json (ข้อมูลสมมติ)
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "ใบกำหนดหน้าที่งานประจำตำแหน่ง (Job Description)"
python3 $TD/scripts/build_html.py form.tpl.html --mode replica --profile profile.json -o JD_template.html
```

## 6. Checklist ก่อนส่งมอบ
- [x] parity IDENTICAL 5/5 · ไม่มี {{}} หลง
- [x] ลายเซ็นครบสาย (ผู้จัดทำ + DOA N ขั้น + ผู้ดำรงตำแหน่ง)
- [ ] จำนวนหน้า / compare_original — รอเครื่องที่มี browser

## 7. (Replica) ต้นฉบับลูกค้า + ความต่างที่ตั้งใจ
- ต้นฉบับ: `ใบกำหนดหน้าที่งานประจำตำแหน่ง (JD).docx` · Doc No. `FM-HRM-32` · Rev. `Rev. 00 : 01/07/2569` · 2 หน้า
- Profile: `profile.json` — form_fs 10pt · form_title_fs 14pt · logo 14mm กลาง · grid row 8mm
- ความต่างจากกระดาษ (ตั้งใจ): ตารางลงนามช่องผู้อนุมัติเพิ่มตามขั้น DOA (ค่าเริ่ม 1 = เท่ากระดาษ) · มีบรรทัดคำตัดสิน ☐ อนุมัติ ☐ ไม่อนุมัติ ในช่องผู้อนุมัติ · ข้อความ "ส่งในระบบ/พิจารณาในระบบ/รับทราบในระบบ" แทนลายมือ · footer เลขที่เอกสาร · ตาราง 4 คอลัมน์กว้างเท่ากัน (ต้นฉบับ ตำแหน่ง:จำนวน ≈ 3:1 — replica ห้าม style ใน body · ปรับผ่าน profile/CSS กลางไม่ได้)
- ผล compare_original: [NO-BROWSER] ข้าม (ต้องใช้ PDF จาก browser) — ให้รันบนเครื่องที่มี browser
- ภาพตรวจด้วยตา (ไม่ใช่ผลด่านทางการ): render นอกเครื่องด้วย Chromium — approved = 2 หน้า · doa6steps = 2 หน้า (ลงนาม 4+4) · long-12rows = 2 หน้า

## 8. (Replica) Data contract + สถานะที่ทดสอบ
- ตาราง contract: `JD_data-contract.md`
- parity JS ↔ Python: IDENTICAL 5/5
- สถานะ: draft · approved (รับทราบแล้ว) · rejected · long-12rows (ลูกน้อง 12 แถว + ข้อความยาว) · approved-doa6steps (8 ช่อง 2 แถว 4+4)

## 9. (Replica) print_config
```json
{
  "doc_type": "JD",
  "mode": "replica",
  "template_ref": "form.tpl.html",
  "template_version": "v1",
  "profile_ref": "profile.json",
  "form_code": "FM-HRM-32",
  "revision": "Rev. 00 : 01/07/2569",
  "paper": "A4-portrait",
  "pages_on_paper": 2,
  "min_rows": 3,
  "dense_when_rows_over": 6,
  "text_min_lines": { "job_purpose": 4, "key_responsibilities": 8, "job_specification": 4, "kpi": 4, "other_qualifications": 4 },
  "header_source": "organization_snapshot_at_numbering",
  "sign_boxes": [
    { "box": "requester", "label": "ผู้จัดทำ (Prepared By)", "show_date": true },
    { "box": "doa_step:*", "label": "from_doa_step", "show_decision": true, "show_date": true },
    { "box": "acknowledger", "label": "ผู้ดำรงตำแหน่ง (Acknowledged By)", "show_date": true, "position": "last", "note": "ไม่ใช่ขั้น DOA — ผู้ดำรงตำแหน่งกดรับทราบหลังอนุมัติ (DEC-04/DEC-16) · ว่างได้" }
  ],
  "decision_words": { "default": { "approve": "อนุมัติ", "reject": "ไม่อนุมัติ" }, "by_role": {} },
  "config_reads": {},
  "footer_left": "เลขที่ {doc.no} · (ร่าง) · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE",
  "footer_right": "Doc No. {form_code} · {revision}",
  "sign_layout": { "source": "approval_chain snapshot (ผู้จัดทำ + จำนวนขั้นตามที่ตั้งใน DOA) + ผู้ดำรงตำแหน่งท้ายสุด", "max_per_row": 4, "split": "even", "dense_when_steps_over": 4, "keep_together": true },
  "note": "ตารางลงนาม 3 ช่องบนกระดาษ = ผู้จัดทำ + DOA 1 ขั้น (ค่าเริ่ม) + ผู้ดำรงตำแหน่ง · ขั้น DOA เพิ่มที่ DOA กลาง ช่องเพิ่มตาม"
}

```
