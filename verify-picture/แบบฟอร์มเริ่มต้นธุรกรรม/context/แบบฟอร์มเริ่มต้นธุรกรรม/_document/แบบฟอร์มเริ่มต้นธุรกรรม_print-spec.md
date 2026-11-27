# PRINT SPEC — แบบฟอร์มเริ่มต้นธุรกรรม (IVMA · FM-IVM-01)

> โหมด **Replica** (แบบฟอร์มลูกค้า) · thai-doc-pdf-generator v2.2 · มติทั้งหมด AI-DEFAULT (โหมดไม่เฝ้า) — รอลูกค้ายืนยันในใบลงนาม
> ไฟล์คู่: `form.tpl.html` (template logic-less) · `แบบฟอร์มเริ่มต้นธุรกรรม_template.html` (build แล้ว ฟอนต์ฝัง) · `*.data.json` 5 สถานะ · `print_config.json` · `profile.json`
> **[NO-BROWSER]** เครื่องที่ทำไม่มี browser → ยังไม่ได้ PDF / จำนวนหน้า / compare_original — ต้องรัน `render_states.py --max-pages 2` + `compare_original.py` บนเครื่องที่มี browser ก่อนส่ง dev

## 1. สรุป
- **ประเภทเอกสาร:** แบบฟอร์มเริ่มต้นธุรกรรม / Transaction Initiation Form · ฝ่ายบริหารการลงทุน
- **ขนาด:** A4 แนวตั้ง · **2 หน้า (R10)** — หน้า 1 = หัวกระดาษ + ข้อมูลธุรกรรม + ขอบเขตงาน + หมายเหตุ · หน้า 2 = หัวย่อ (ชื่อเอกสาร + เลขที่) + การตรวจทาน/อนุมัติ (บล็อกลงชื่อทั้งก้อน) + ประวัติการแก้ไข
- เหตุผล 2 หน้า: ส่วนกรอกข้อความยาว 6 ช่อง (ขอบเขตงาน) + 2 หมวด + สายอนุมัติ dynamic (ทดสอบ 6 ขั้น = 7 แถวลงนาม) + ประวัติแก้ไขไม่จำกัด → 1 หน้าต้องบีบฟอนต์ < 8pt ซึ่งห้าม · ทุกสถานะ = 2 หน้าเท่ากัน
- ฟอนต์ Sarabun · หมึกเดียว (profile) · ตารางกรอบเส้นทึบ R9

## 2. Field Mapping
| ช่องในเอกสาร | Source (entity.field) | Format | บังคับ | หมายเหตุ |
|---|---|---|---|---|
| เลขที่ (footer + หัวหน้า 2) | ENG-DOC-NUM `IVMA` | `IVMA-พ.ศ.-running` | ✓ | ออกตอนบันทึกครั้งแรก (DEC-10) |
| ชื่อเอกสาร | ค่าคงที่ `doc.title` | — | ✓ | "แบบฟอร์มเริ่มต้นธุรกรรม" |
| ชื่อบริษัท + โลโก้ | Organization snapshot | — | ✓ | ต้นฉบับพิมพ์ชื่อบริษัทลูกค้าตายตัว → ระบบใช้ของ Organization |
| ชื่อธุรกรรม / โครงการ | `txn.name` | ข้อความ | ✓ | |
| เจ้าของโครงการ | `txn.project_owner` | ข้อความ | ✓ | |
| แหล่งที่มาของธุรกรรม | `txn.source` | ข้อความ | ✓ | |
| ประเภทธุรกรรม | `txn.type` | ข้อความ | ✓ | |
| วันที่เริ่มโครงการ | `txn.start_date` | วัน เดือน(ไทย) พ.ศ. | ✓ | |
| ผู้รับผิดชอบ | Employee.full_name (F-EMP-001) | ข้อความ | ✓ | |
| หน่วยงานภายในที่เกี่ยวข้อง | `txn.internal_units` | ข้อความ (หลายหน่วยคั่น " · ") | | |
| บุคคลภายนอกที่เกี่ยวข้อง | `txn.external_parties` | ข้อความ | | PDPA |
| วัตถุประสงค์หลัก … ประเด็นคงค้าง | `scope.*` (5 ช่อง) | ข้อความยาว | 3 ช่องแรก ✓ | ขึ้นบรรทัดใหม่ในข้อมูล → backend รวมเป็น " · " (template escape) |
| การตรวจทาน / อนุมัติ | `sign_rows[].signs[]` | 1 แถว / ผู้ลงนาม | ✓ | ผู้จัดทำ + 1 แถวต่อขั้น DOA (ไม่ fix) |
| ประวัติการแก้ไข | `revisions[]` | ≥ 2 แถว | | ระบบเติมจากประวัติฉบับ |

## 3. กติกาคำนวณ
- ไม่มีสูตร/ค่าคงที่บนกระดาษ · data เติมแถวว่างประวัติการแก้ไขจนครบ `min_rows` = 2

## 4. กติกาการพิมพ์
- `.page-break` ก่อนหน้า 2 (ตั้งใจ) · หัวตารางซ้ำ (`thead`) · แถวไม่ตัดกลาง · `.signs-block` ไม่ตัดข้ามหน้า
- ท้ายหน้า 1 `.cont-note` "มีต่อหน้าถัดไป" · footer ทุกหน้ามีเลขที่ + "หน้า 1/2" / "หน้า 2/2" + Doc. No. / Rev.
- ฟอนต์ไม่ต่ำกว่า 8pt (profile form_fs 9pt)

## 5. วิธี build ใหม่
```bash
python3 make_data.py
python3 $TD/scripts/parity_check.py form.tpl.html *.data.json
python3 $TD/scripts/render_states.py form.tpl.html *.data.json -o out --mode replica --profile profile.json --title "แบบฟอร์มเริ่มต้นธุรกรรม" --max-pages 2
python3 $TD/scripts/compare_original.py ../orig/SAMPLE.pdf out/approved.pdf -o out/compare --region 0:0.55
python3 $TD/scripts/build_html.py form.tpl.html --title "แบบฟอร์มเริ่มต้นธุรกรรม" --mode replica --profile profile.json -o แบบฟอร์มเริ่มต้นธุรกรรม_template.html
```

## 6. Checklist
- [x] parity JS ↔ Python IDENTICAL 5/5
- [x] ไม่มี `{{}}` หลงใน HTML ทุกสถานะ (render_doc --strict + build_html)
- [ ] จำนวนหน้า = 2 ทุกสถานะ — **[NO-BROWSER] ยังไม่ได้ตรวจ**
- [ ] compare_original — **[NO-BROWSER] ยังไม่ได้ตรวจ**
- [x] ลายเซ็นครบสาย (ผู้จัดทำ + ขั้น DOA) · คำตัดสินผูก role

## 7. (Replica) ต้นฉบับ + ความต่างที่ตั้งใจ
- ต้นฉบับ: `1. FM-IVM-01 แบบฟอร์มเริ่มต้นธุรกรรม.xlsx` (1 หน้า) · Doc No. FM-IVM-01 · Rev.00 : 01/07/2569
- Profile: form_fs 9pt · form_title_fs 15pt · form_logo_h 12mm · form_title_gap 4px · form_grid_gap 6px
- ความต่าง (ตั้งใจ): (1) 1 หน้า → 2 หน้า ตาม R10 (2) หัวหมวดแถบน้ำเงินเข้ม → หัวตารางเทา (หมึกเดียวของ replica) (3) ตารางลงนามวนตาม DOA ไม่ fix 3 แถว · ช่องลายเซ็นใช้ ☐/☑ คำตัดสิน + "พิจารณาในระบบ วันที่ เวลา" แทนลายมือ (DEC-07) (4) footer ซ้ายเลขที่/ร่าง/CUBE NATIVE (5) ชื่อบริษัทจาก Organization
- compare_original: **[NO-BROWSER] ยังไม่ได้รัน** — เมื่อรัน ใช้ `--region 0:0.55` (ส่วนหน้า 1 ที่เทียบได้)

## 8. (Replica) Data contract + สถานะ
| key | Source | ตัวอย่าง | หมายเหตุ |
|---|---|---|---|
| `company.name` · `company.logo` | Organization header_snapshot | `บริษัท ตัวอย่าง จำกัด (มหาชน) และบริษัทในเครือ` · data URI | snapshot ตอนออกเลข |
| `doc.title` · `doc.no` · `doc.is_draft` | ค่าคงที่ · ENG-DOC-NUM · status=draft | `IVMA-2569-0001` | |
| `doc.form_code` · `doc.revision` | F-DOCCFG print_config | `FM-IVM-01` · `Rev.00 : 01/07/2569` | |
| `txn.*` (8) | เอกสารนี้ · `txn.responsible` ← Employee | ดู approved.data.json | ข้อมูลสมมติ |
| `scope.*` (5) | เอกสารนี้ | | |
| `revisions[]` → version · date · detail · prepared_by · approved_by | audit ฉบับเอกสาร | `00` · `10 ตุลาคม 2569` | เติมแถวว่างครบ 2 |
| `sign_rows[].signs[]` → role · name · position · date · decision{approve_box, approve_word, reject_box, reject_word} | ผู้จัดทำ + approval_chain | | sign_rows.py / tplSignRows |
| `layout.dense` | revisions > 12 หรือขั้น DOA > 4 | `true` | |
- สถานะ: draft · approved · rejected (ขั้น 2 ไม่อนุมัติ) · long-12revisions (ข้อความยาว + 12 ฉบับ) · approved-doa6steps (7 แถวลงนาม) → เป้าหมาย 2 หน้าทุกสถานะ (รอตรวจบนเครื่องมี browser)

## 9. print_config
ดู `print_config.json` (doc_type IVMA · pages 2 · sign_boxes requester + doa_step:* · decision_words.by_role)
