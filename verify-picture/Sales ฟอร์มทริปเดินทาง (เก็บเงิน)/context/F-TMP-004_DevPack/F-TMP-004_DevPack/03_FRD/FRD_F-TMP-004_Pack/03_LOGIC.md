# 03_LOGIC — F-TMP-004 ใบเดินทาง : เขตการขาย General Trade

## 1. State machine
```
(ใหม่) --บันทึกร่าง--> draft --ส่งอนุมัติ--> pending --อนุมัติครบทุกขั้น--> approved
                         ^                      |
                         |----ไม่อนุมัติ (DEC-08)-|        (เลขที่เดิม · returned = true)
   draft / pending --ยกเลิก--> cancelled
```
- `approved` และ `cancelled` = สถานะปิด แก้ไขไม่ได้
- **ไม่มีสถานะ `rejected`** — ไม่อนุมัติแล้วกลับเป็น `draft` เลขที่เดิม (DEC-08)

### FN-01 — เติมข้อมูลผู้รับผิดชอบเขตจากระบบ (snapshot)
เมื่อเปิดหน้าสร้าง: อ่าน `Employee.full_name` / `Employee.position` / `Employee.department` ของผู้ใช้ที่ login (F-EMP-001 · F-ORG-001)
บันทึกครั้งแรก → snapshot ลงเอกสาร (`owner_name` · `owner_position` · `owner_department`) ไม่ดึงสดอีกหลังออกเลข

### FN-02 — คำนวณยอดรวมทุกคอลัมน์ (DEC-04 · DEC-12)
`total_<col> = Σ lines[].<col>` ของ **ทุกแถวในตาราง** สำหรับ 13 คอลัมน์ตัวเลข
- คำนวณที่ server ทุกครั้งที่บันทึก และคำนวณสดฝั่งหน้าจอเพื่อแสดงผล
- ผู้ใช้แก้ค่ารวมไม่ได้ (ไม่รับจาก payload)
- หมายเหตุที่มา: ไฟล์ต้นฉบับของลูกค้าใส่สูตร SUM ครอบช่วงไม่ครบ 8 จาก 13 ช่อง → ถือว่าผิดและแก้เป็นรวมทุกแถว

### FN-03 — ตรวจความสอดคล้องของแผนกับผลจริง (เตือน ไม่บล็อก · DEC-04)
เทียบ 6 คู่: วางบิล บิล/บาท · รับเช็ค บิล/บาท · เป้าหมายการขาย ร้าน/บาท กับช่อง Accual ของกลุ่มเดียวกัน
ผลรวม Accual > ผลรวมแผม ⇒ แสดงคำเตือนในหน้าจอและในขั้นตรวจสอบ · **ส่งอนุมัติได้ตามปกติ**

### FN-04 — บันทึกร่างและออกเลขที่เอกสาร (DEC-10)
1. ตรวจ `DOC_TYPE('TRV').active` ที่ **F-DOCCFG** — ไม่เปิดใช้ ⇒ `DOCTYPE_INACTIVE`
2. validate ตาม 05_RULES §2
3. ครั้งแรกเท่านั้น: `ENG-DOC-NUM.next('TRV')` → `doc_no` (รูปแบบ `{PREFIX}-{YYYY}-{run:4}` · reset รายปี · scope global · ไม่ใช่ no-gap)
4. snapshot หัวกระดาษจาก Organization → `header_snapshot` (ใช้ตอนพิมพ์ ไม่ดึงสดอีก)
5. สถานะ `draft` · เขียน audit "สร้างเอกสาร"

### FN-05 — แก้ไขร่าง
อนุญาตเมื่อ `status = draft` และผู้ใช้เป็นเจ้าของ (`NOT_OWNER` ถ้าไม่ใช่) · เลขที่เดิม · audit "แก้ไขร่าง"
ใบที่ถูกส่งกลับแก้ไข (`returned = true`) แก้ไขได้ตามปกติ และ `returned` ถูกล้างเมื่อส่งอีกครั้ง

### FN-06 — ส่งอนุมัติ (resolve + freeze สายอนุมัติ)
1. เรียก DOA กลาง (F-DLG-001) `resolve(doc_type='trv', amount=null, department=<ฝ่ายของผู้ขอ>)` → รายการขั้น + role ต่อขั้น (**DOA-ENGINE-HOOK**)
2. ค่าเริ่มของผู้พิจารณาต่อขั้น: `role-line-manager` = ผู้บังคับบัญชาตรงจากผังองค์กร · `role-mgr-sales` = ผู้จัดการฝ่ายขาย
3. ผู้ส่งเลือก/แก้ผู้พิจารณาได้ทุกขั้น — ผู้ขอเลือกตัวเองไม่ได้ (BR-DOA-04)
4. freeze ลง `approval_chain` (BR-DOA-02) · ขั้น 1 = `pending` ขั้นอื่น = `waiting` · สถานะใบ = `pending` · `returned = false`
5. audit "ส่งอนุมัติ" · DOA engine ยิง `doa_pending` เอง

### FN-07 — อนุมัติขั้นปัจจุบัน
เฉพาะผู้พิจารณาขั้นปัจจุบัน (`NOT_CURRENT_APPROVER`) · ขั้นนั้น = `approved` + เวลา + ความเห็น
มีขั้นถัดไป ⇒ ขั้นถัดไป = `pending` ใบยังคง `pending` · ครบทุกขั้น ⇒ ใบ = `approved`
**ไม่เปลี่ยนค่าในระบบ ไม่ส่งต่อระบบอื่น** (DEC-01 · DEC-02)

### FN-08 — ไม่อนุมัติ = ส่งกลับแก้ไข (DEC-08 · ข้อยกเว้นของ BR-DOA-03)
เหตุผลบังคับ (`REASON_REQUIRED`) · ใบกลับเป็น `draft` **เลขที่เดิม** · `returned = true` + เก็บเหตุผล/ผู้ส่งกลับ/เวลา
`approval_chain` ถูกล้างกลับเป็นค่าตั้งต้น (resolve ใหม่ตอนส่งรอบถัดไป ตาม BR-DOA-02) · audit "ไม่อนุมัติ — ส่งกลับแก้ไข"

### FN-09 — ยกเลิกเอกสาร
สถานะ `draft` หรือ `pending` เท่านั้น (DEC-08) · โดยเจ้าของหรือ admin role ของฝ่ายเจ้าของเอกสาร · เหตุผลบังคับ
ขั้นที่ยัง `pending`/`waiting` → `skipped` · ใบ = `cancelled` · ยิง event `trv_cancelled` ผ่าน ENG-NOTIFY

### FN-10 — การมองเห็น (query filter · DEC-09)
`เจ้าของ` OR (`status <> 'draft'` AND ผู้ใช้อยู่ใน `approval_chain`) OR `admin role ของฝ่ายเจ้าของเอกสาร`
ใบที่ไม่เข้าเงื่อนไข ⇒ ไม่อยู่ในผล A1 และ A2 ตอบ `NOT_FOUND`

### FN-11 — สร้างแบบพิมพ์ (PDF)
`docPrintData(record)` → data contract (`print/TRV_data-contract.md`) → render `form.tpl.html`
- เติมแถวว่างจนครบ **31 แถว** ตามกระดาษ (DEC-05) · ค่าแสดงทุกตัวเป็น string ที่จัดรูปแล้ว
- ช่องลงชื่อ = ผู้นำเสนอ + 1 ช่องต่อขั้นใน `approval_chain` แบ่งแถวละ ≤ 4 (`sign_layout.max_per_row`)
- คำตัดสินผูก role จาก `print_config.decision_words` ไม่ผูกลำดับขั้น
- สำเนาเอกสาร: `ENG-DOC-STORE.store()` เมื่อใบเปลี่ยนเป็น `approved` (snapshot `approved_final`)

### FN-12 — ส่งออก CSV (DEC-11)
ส่งออกตามผลการกรองปัจจุบัน · หัวคอลัมน์ตามกระดาษ + รวมยอด 13 ช่อง · UTF-8 BOM
