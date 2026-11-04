# PRINT SPEC — แบบขออนุญาตออกปฏิบัติงานนอกสถานที่ (OSW · FORM REPLICA · dynamic)

> เอกสารประกอบสำหรับ Dev — แนบคู่ FRD ของ feature F-HR-OSW
> ต้นฉบับลูกค้า: **FM-HRM-02 Rev.00 (01/07/2569) · Credence** — ขึ้นเป็นเอกสารระบบด้วย thai-doc-pdf-generator คงหน้าตาแบบฟอร์มเดิม
> **สร้างแบบ dynamic: template (logic-less) + data JSON → HTML → PDF** — prototype กับ server ใช้ template และ data contract ชุดเดียวกัน

## 0. ไฟล์ในโฟลเดอร์ print/
| ไฟล์ | ใช้ทำอะไร |
|---|---|
| `osw_body.tpl.html` | **template ต้นฉบับ** (body · placeholder `{{…}}`) — แหล่งเดียว ทั้ง prototype (`OSW_TPL`) และ server |
| `OSW_template.html` | template ที่ build แล้ว (head + CSS + Sarabun ฝัง) เปิดดูโครงพร้อม placeholder |
| `render_osw.py` | ตัว render อ้างอิง (Python) — data JSON + template → body HTML |
| `sample_approved.data.json` · `sample_draft.data.json` | ตัวอย่าง data contract (OSW-2569-0007 ค้างคืน อนุญาตแล้ว · OSW-2569-0012 ร่าง ไป-กลับ) |
| `OSW_sample_approved.pdf` · `OSW_sample_draft.pdf` | ผลลัพธ์จาก pipeline เดียวกัน |
| `base_form_patch.css` | component FORM REPLICA ที่ต้องอัปเข้า skill (`assets/base.css`) |
| `compare_FM-HRM-02_vs_OSW.png` | ภาพเทียบต้นฉบับลูกค้า ↔ เอกสารระบบ |

### Pipeline (server)
```bash
# 1) backend สร้าง data JSON จาก record (§2) · 2) render · 3) build + PDF (thai-doc-pdf-generator)
python render_osw.py osw_body.tpl.html data.json -o body.html
python <skill>/scripts/build_html.py body.html --title "แบบขออนุญาตออกปฏิบัติงานนอกสถานที่" -o OSW-xxxx.html
python <skill>/scripts/render_pdf.py OSW-xxxx.html -o OSW-xxxx.pdf
```
- ใช้ engine mustache ตัวไหนก็ได้ (subset ที่ใช้: `{{a.b}}` escape · `{{{a.b}}}` raw เฉพาะโลโก้ · `{{#list}}…{{/list}}` · `{{#flag}}…{{/flag}}`)
- ตรวจแล้ว: ผลจาก `render_osw.py` = ผลจาก `tplRender()` ใน prototype **ตรงกันทุก byte** (ทั้ง 2 ตัวอย่าง)

## 1. สรุป
- **Pattern:** FORM REPLICA — โลโก้กลาง · ชื่อเอกสารกลาง · กรอกบนเส้นประ ตามแบบกระดาษ · **ช่องลายเซ็น = thai-doc B6 `.signs` เรียงแถวล่าง** (ช่องจาก DOA · ดู `DOA_BRIEF` / `DOCCFG_BRIEF`) · Doc No./Rev. ใน footer ขวา
- **ขนาด:** A4 แนวตั้ง ขอบ 14mm · 1 หน้าถึง 12 ช่วงวันที่ (เกิน 5 ใช้ `layout.dense`) · เกินนั้นตัดหน้าอัตโนมัติ บล็อกลงชื่อไม่ถูกตัดกลาง
- **ฟอนต์:** Sarabun · ตัวอักษรเนื้อหา 9.6pt · ชื่อเอกสาร 14pt
- **ต่างจากกระดาษ:** ลายเซ็นย้ายเป็นแถวล่าง (มาตรฐาน thai-doc) แทนเรียงกลางหน้า · footer "เลขที่ OSW-… · (ร่าง) · เอกสารนี้จัดทำโดยระบบ CUBE NATIVE" · บรรทัดวันที่ใต้ลายเซ็นแสดง "ส่งในระบบ / พิจารณาในระบบ วันที่ เวลา"

## 2. Data contract (JSON ที่ template ใช้) → Source
| key | Source | ตัวอย่าง | หมายเหตุ |
|---|---|---|---|
| `company.name` · `company.logo` | `header_snapshot` (จาก Organization ตอนออกเลข) | `Credence` · data URI / URL | ตัวอย่างใช้โลโก้จาก FM-HRM-02 · ไม่ดึงสดหลังออกเลข |
| `doc.title` · `doc.no` · `doc.is_draft` | ค่าคงที่ · ENG-DOC-NUM · status = draft | `OSW-2569-0007` · `false` | `is_draft` → footer "ร่าง" |
| `doc.form_code` · `doc.revision` | F-DOCCFG `print_config` | `FM-HRM-02` · `Rev. 00 : 01/07/2569` | แก้เมื่อลูกค้าออก Rev. ใหม่ |
| `req_date` | osw.req_date | `11 กันยายน 2569` | วัน เดือนเต็ม พ.ศ. |
| `to_name` | approval_chain[0].assignee → Employee.full_name | `คุณกริสดา จงศิริวัฒน์` | "คุณ" + ชื่อ |
| `employee.name` · `.position` · `.dept` | Employee.full_name · osw.pos · osw.dept | | ตำแหน่ง/ฝ่าย = snapshot ณ วันที่ขอ |
| `lines[]` → `no` · `date` · `time_from` · `time_to` · `purpose` | osw_lines | `1` · `9 – 10 ก.ย. 2569` · `08:30` · `17:30` · ข้อความ | **อย่างน้อย 5 แถว** (แถวว่างตามกระดาษ) · ไม่จำกัด |
| `mode.day_box` · `mode.overnight_box` | osw.mode | `☐` / `☑` | |
| `per_diem.nights` · `.paid_nights` · `.rate` · `.amount` | osw.nights · osw.paid_nights · osw.rate (snapshot ExpensePolicy.per_diem) · computed | `7` · `7` · `150` · `1,050.00` | ไป-กลับ = ว่าง (ยกเว้น rate) |
| `signs[]` → `role` · `name` · `position` · `date` · `decision` | ช่อง 1 = ผู้ขอ (พนักงาน · `submitted_at`) · ช่องถัดไป = 1 ช่องต่อขั้นใน `approval_chain` (DOA snapshot) | `ผู้บังคับบัญชา` · `กริสดา จงศิริวัฒน์` · `Managing Director` · `พิจารณาในระบบ 11 ก.ย. 2569 14:20 น.` · `{approve_box:'☑', reject_box:'☐'}` | **ไม่ hardcode จำนวนช่อง** — ตาม `print_config.sign_boxes` ที่ F-DOCCFG (DOCCFG_BRIEF v1.1) · DOA กี่ขั้นก็เรียงแถวล่างตาม thai-doc B6 `.signs` · ผู้ขอ `decision = null` · ยังไม่พิจารณา `date = วันที่ ........./........./.........` |
| `layout.dense` | lines.length > 5 | `true` | ระยะบรรทัดกระชับ — 12 ช่วงยังจบ 1 หน้า |

## 3. กติกาคำนวณ
- `per_diem = paid_nights × rate` (เฉพาะค้างคืน) · ปัด 2 ตำแหน่ง ROUND_HALF_UP

## 4. กติกาการพิมพ์
- A4 แนวตั้ง · แถวลายเซ็น + footer ชิดล่างหน้าเสมอ (`.doc-bottom`)
- พิมพ์ได้ทุกสถานะ (ร่าง: footer มีคำว่า "ร่าง" · ช่องผู้บังคับบัญชาว่าง)
- ≤ 12 ช่วงวันที่ = 1 หน้า (ทดสอบแล้ว) · เกินนั้นตัดหน้าอัตโนมัติ บล็อกลงชื่อไม่ถูกตัดกลาง
- ไม่พิมพ์เลขหน้าในเนื้อเอกสาร (กระดาษเดิมไม่มี)

## 5. Component ใหม่ใน thai-doc-pdf-generator (`base_form_patch.css`)
- เพิ่มต่อท้าย `assets/base.css` (ใช้ CI var เท่านั้น ไม่มี hex) → ใช้ซ้ำกับแบบฟอร์มลูกค้าตัวอื่นได้ทันที
- classes: `.form` `.form-brand` `.form-logo` `.form-title` `.form-date` `.form-row(--indent)` `.fill(--s/--m/--l/--left)` `.form-num` `.form-p` `.form-check(__lbl/__opts/__opt)` `.cb` · `.form--dense`
- ลายเซ็นไม่อยู่ใน patch — ใช้ `.signs` / `.sign` เดิมของ base.css
- ⚠ skill อยู่ในโฟลเดอร์อ่านอย่างเดียว — รอบนี้ build จากสำเนา skill + patch · ต้องอัป patch เข้า skill กลาง (และเพิ่มแถว pattern FORM REPLICA ใน `knowledge/document-types.md`)

## 6. Checklist
- [x] ลำดับ/ข้อความ/ช่องตรง FM-HRM-02 ทุกบรรทัด (เทียบภาพ compare)
- [x] 1 หน้า A4 (ตัวอย่าง 3 ช่วง + บรรทัดว่างถึง 5 · 12 ช่วงยัง 1 หน้า)
- [x] prototype ↔ server render ตรงกันทุก byte
- [x] 7 × 150 = 1,050.00 บาท
- [x] โลโก้ลูกค้า
- [ ] ยืนยันกับลูกค้า: ใช้ข้อความ "ส่งในระบบ / พิจารณาในระบบ" แทนลายมือชื่อได้ หรือต้องการลายเซ็นภาพ (e-signature)
