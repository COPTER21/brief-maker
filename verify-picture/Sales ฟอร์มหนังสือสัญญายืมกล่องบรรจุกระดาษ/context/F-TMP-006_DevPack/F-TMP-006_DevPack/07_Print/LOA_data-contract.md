# DATA CONTRACT — หนังสือสัญญายืม (LOA · FM-SAL-14)

> สัญญาข้อมูลระหว่าง backend ↔ template (`form.tpl.html`) · ใช้ทั้ง prototype (`tpl_render.js`) และ server (`render_doc.py`)
> กติกา: ค่าแสดงทุกตัวเป็น string ที่จัดรูปแล้ว · boolean ใช้เป็นเงื่อนไขเท่านั้น · ว่าง = `""` · ไม่มี `{}` ว่าง
> ตรวจ: `python3 parity_check.py form.tpl.html *.data.json` → **IDENTICAL 5/5 · ไม่มีคำเตือน**

| key | Source (entity.field / engine) | ตัวอย่าง | หมายเหตุ |
|---|---|---|---|
| `company.name` | Organization.legal_name → header_snapshot (ตอนออกเลข) | `บริษัท ครีเดนซ์ จำกัด (มหาชน)` | ค่าคงที่ในเนื้อสัญญา **ห้าม hardcode** (DEC-04) · ไม่ดึงสดหลังออกเลข |
| `company.logo` | Organization.logo → header_snapshot | data URI | ตัวอย่างใช้โลโก้ placeholder |
| `doc.title` | ค่าคงที่ "หนังสือสัญญายืม" | `หนังสือสัญญายืม` | ถ้อยคำตามหัวฟอร์ม |
| `doc.no` | ENG-DOC-NUM.next() · preset `{PREFIX}-{YYYY}-{run:4}` | `LOA-2569-0001` | ออกเลขตอนบันทึกครั้งแรก (DEC-10) |
| `doc.running_no` | ENG-DOC-NUM (รูปแบบบนกระดาษ `{run:4}-{ค.ศ.}`) | `0001-2026` | เลขที่พิมพ์บนหัวกระดาษต้นฉบับ · ร่างยังไม่มี = `""` |
| `doc.is_draft` | status = draft | `true` | boolean ใช้เป็นเงื่อนไข section เท่านั้น |
| `doc.form_code` · `doc.revision` | F-DOCCFG `print_config` | `FM-SAL-14` · `Rev.00 : 01/07/2569` | |
| `copy.value` · `copy.label` | print_config.copies (ชุดที่สั่งพิมพ์) | `original` · `ต้นฉบับ` | 1 เลขที่ = 2 ชุด (ต้นฉบับ · สำเนา) — ชุดละ 1 หน้า |
| `req_date` | box_loan_agreement.doc_date | `7 ตุลาคม 2569` | วันที่เต็มไทย พ.ศ. · ร่าง = `""` |
| `customer.name` | Customer.name (F-SAL-CUS) | `บริษัท ตัวอย่างค้าปลีก จำกัด` | **pdpa** · ตัวอย่างใช้ชื่อสมมติ |
| `customer.code` | Customer.code (F-SAL-CUS) | `C-00012` | เติมอัตโนมัติเมื่อเลือกลูกค้า |
| `customer.address` | Customer.address (F-SAL-CUS) | `99/9 หมู่ 5 ถนนตัวอย่าง …` | **pdpa** · ผู้ใช้แก้ได้ (สถานที่ติดตั้งอาจต่างจากที่อยู่จดทะเบียน) |
| `lines[].detail` | box_loan_agreement.lines[].detail | `กล่องบรรจุกระดาษ ขนาด 40 x 30 x 30 ซม. จำนวน 50 ใบ` | เติมแถวว่างจนครบ `min_rows` = 1 (DEC-05 ไม่จำกัดแถว) |
| `damage_exception` | box_loan_agreement.damage_exception | `งานตามปกติ` | ช่องเติมแทรกกลางเงื่อนไขข้อ 1 · ไม่บังคับ → เว้นว่าง = เส้นประว่าง |
| `policy.free_replace_pct` · `policy.free_replace_pct_text` | SalesPolicy.box_free_replace_pct (+ คำอ่านไทย) | `10` · `สิบ` | **ห้าม hardcode** (DEC-04) · เปลี่ยนค่าแล้วเนื้อสัญญาที่พิมพ์เปลี่ยนตาม |
| `sign_rows[].signs[]` → `role` · `name` · `position` · `date` · `decision` | ผู้รับมอบ (คู่สัญญา) + `approval_chain` (DOA snapshot) | | จำนวนช่อง = 1 + จำนวนขั้นที่ตั้งใน DOA (**ห้าม fix**) · แถวละ ≤4 (`sign_rows.py` / `tplSignRows()`) |
| `signs[].decision.approve_word` · `reject_word` | print_config.decision_words.by_role[role_id] | `ลงนาม` · `ไม่ลงนาม` | ผูก role ไม่ผูกลำดับขั้น |
| `signs[].date` | ยังไม่พิจารณา = `วันที่ ........./........./.........` | `พิจารณาในระบบ 7 ต.ค. 2569 15:40 น.` | ไม่ใช้ภาพลายมือชื่อ (DEC-07) |
| `layout.dense` | `lines.length > 6` หรือ ขั้น DOA > 4 | `true` | |
