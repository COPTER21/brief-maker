# DATA CONTRACT — ใบคำร้องขอดำเนินการด้านเอกสาร (DAR · FM-CCC-03)

> สัญญาข้อมูลระหว่าง backend ↔ template (`form.tpl.html`) · ใช้ทั้ง prototype (tpl_render.js) และ server (render_doc.py)
> กติกา: ค่าแสดงทุกตัวเป็น string ที่จัดรูปแล้ว · boolean ใช้เป็นเงื่อนไขเท่านั้น · checkbox = "☑"/"☐" · ว่าง = "" · ไม่มี {} ว่าง
> ตรวจ: `python scripts/parity_check.py form.tpl.html *.data.json` → IDENTICAL 5/5
> มติทั้งหมดเป็น **AI-DEFAULT** (DECISIONS.lock) รอลูกค้ายืนยัน

| key | Source (entity.field / engine) | ตัวอย่าง | หมายเหตุ |
|---|---|---|---|
| `company.name` · `company.logo` | Organization → header_snapshot (ตอนออกเลข) | `บริษัท ตัวอย่าง จำกัด` · data URI | ไม่ดึงสดหลังออกเลข |
| `doc.title` | ค่าคงที่ (หัวกระดาษ) | `ใบคำร้องขอดำเนินการด้านเอกสาร / Document Action Request (DAR Form )` | |
| `doc.no` (F05) | ENG-DOC-NUM · รหัส DAR · ออกเมื่อบันทึกครั้งแรก (DEC-10) | `DAR-2569-0001` | พิมพ์ที่ DAR.No. + footer ทุกหน้า |
| `doc.is_draft` · `doc.is_cancelled` | status | `true` | เงื่อนไขเท่านั้น |
| `doc.form_code` · `doc.revision` | F-DOCCFG print_config | `FM-CCC-03` · `Rev.00 : 01/07/2569` | |
| `dar_date` (F01) | dar.dar_date | `10 ตุลาคม 2569` | วันที่เต็ม พ.ศ. |
| `requester.name/division/department` (F02–F04) | dar.owner → Employee snapshot | | |
| `target.doc_no/revision/doc_name/effective_date/pl_wi_step` (F06–F09, F11) | dar.target_* | `WI-QA-01` · `Rev.02` | effective_date ก่อน dar_date = เตือน (DEC-15) |
| `purpose.new/revise/cancel/other` | dar.purpose (เลือก 1 · DEC-04) | `☑`/`☐` | |
| `issue.doa/policy/wi/form` | dar.issue_type (เลือก 1 · DEC-14) | `☑`/`☐` | |
| `origin.car/ic/ia/other` · `origin_detail` (F10) | dar.origin · dar.origin_detail | | อื่นๆ → บังคับรายละเอียด |
| `change_rows[]` → `before` · `after` (F12–F13) | แตกบรรทัดจาก change.before / change.after | | เติมแถวว่างครบ 8 (`change_min_rows`) |
| `related_p1[]` · `related_cont[]` · `has_related_cont` (F14–F15) | dar_related_docs (ไม่จำกัด · DEC-05) | | หน้า 1 = 22 − แถวแก้ไข (ขั้นต่ำ 14 แถวว่าง) · ส่วนเกินไปตารางต่อหน้า 2 |
| `dist_rows[].cells[]` → `box` · `label` | dar_distribution × รายการหน่วยงาน 27 ช่อง (ชุดซ้ำติด "(2)" · DEC-12) | `☑ การเงิน (FIN)` | แถวละ 4 · เติมช่องว่าง |
| `distribution.remark` (F16) · `distribution.emails` (F17) | dar.remark · dar.emails | | emails แสดงเฉพาะเมื่อเลือก E-mail |
| `receive.email/paper` | dar.receive_methods (≥1) | | |
| `receipt.name` · `receipt.date` | event ลงนามรับ (dar_received) | `ลงนามรับในระบบ 16 ต.ค. 2569 09:30 น.` | ไม่ใช่ขั้น DOA |
| `sign_rows[].signs[]` → `role` · `name` · `position` · `date` · `decision{approve_box,approve_word,reject_box,reject_word}` | ผู้จัดทำ + `approval_chain` (DOA snapshot) ผ่าน `sign_rows.py` / `tplSignRows()` | | จำนวนช่อง = 1 + จำนวนขั้น · แถวละ ≤4 · TODO: DOA engine |
| `layout.dense` | related > 18 หรือ ขั้น DOA > 4 | `true` | |
