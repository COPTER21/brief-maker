# 03_LOGIC — F-TMP-007 ใบเดินทางและสถานที่ปฎิบัติงาน  สำหรับ General Trade

## 1. State machine
```
(ใหม่) --บันทึกร่าง--> draft --ส่งอนุมัติ--> pending --อนุมัติครบทุกขั้น--> approved
                         ^                      |
                         |----ไม่อนุมัติ (DEC-09)-|        (เลขที่เดิม · returned = true)
   draft / pending --ยกเลิก--> cancelled
```
- `approved` และ `cancelled` = สถานะปิด แก้ไขไม่ได้
- **ไม่มีสถานะ `rejected`** — ไม่อนุมัติแล้วกลับเป็น `draft` เลขที่เดิม (DEC-09)

### FN-01 — เติมข้อมูลผู้จัดทำจากระบบ (snapshot)
เมื่อเปิดหน้าสร้าง: อ่าน `Employee.full_name` / `Employee.position` / `Employee.department` / `Employee.phone` ของผู้ใช้ที่ login (F-EMP-001 · F-ORG-001)
บันทึกครั้งแรก → snapshot ลงเอกสาร (`from_name` · `from_position` · `from_department` · `from_phone`) ไม่ดึงสดอีกหลังออกเลข
ช่อง "โทรศัพท์" แก้ไขได้ในร่าง (ค่าเริ่มจากทะเบียนพนักงาน)

### FN-02 — คำนวณยอดรวมรายแถว (DEC-04 · DEC-14)
`line_total = cost_lodging + cost_hotel + cost_perdiem + cost_laundry + cost_fee + cost_post + cost_parking + cost_other`
- คำนวณที่ server ทุกครั้งที่บันทึก และคำนวณสดฝั่งหน้าจอเพื่อแสดงผล · ผู้ใช้แก้ไม่ได้ (ไม่รับจาก payload)
- หมายเหตุที่มา: ไฟล์ต้นฉบับของลูกค้าปล่อยคอลัมน์นี้ว่างไม่มีสูตร ทั้งที่แถวรวมยอดอ้างผลรวมของคอลัมน์นี้

### FN-03 — คำนวณยอดรวมรายคอลัมน์ (DEC-04 · DEC-13)
`total_<col> = Σ lines[].<col>` ของ **ทุกแถวในตาราง** สำหรับคอลัมน์ค่าใช้จ่าย 8 ช่อง + `line_total` + บิลน้ำมัน ลิตร/บาท
- คอลัมน์ "เลขไมล์" (เริ่มต้น/สิ้นสุด) ไม่รวมยอด ตามกระดาษ
- ผู้ใช้แก้ค่ารวมไม่ได้
- หมายเหตุที่มา: ต้นฉบับไม่มีสูตรรวมให้คอลัมน์ "ค่าใช้จ่ายที่พัก — ที่พัก" → ถือว่าผิดและเติมให้ครบ

### FN-04 — คำนวณสรุปท้ายใบ (DEC-04 · DEC-13)
`grand_total = total_claim + phone_cost` · `balance = grand_total − advance_received`
- `phone_cost` และ `advance_received` ผู้ใช้กรอก · `grand_total` และ `balance` computed ผู้ใช้แก้ไม่ได้
- หมายเหตุที่มา: ต้นฉบับใช้ `=P36` ทำให้ "รวมค่าใช้จ่ายทั้งสิ้นเป็นเงิน" ไม่รวมค่าโทรศัพท์
- `balance` ติดลบ ⇒ แสดงข้อความว่าผู้เดินทางต้องคืนเงินสำรองส่วนนั้น (เตือน ไม่บล็อก)

### FN-05 — ตรวจความสมเหตุสมผลของเลขไมล์ (เตือน ไม่บล็อก · DEC-04)
แถวใดมี `odometer_start > 0` และ `odometer_end > 0` และ `odometer_end < odometer_start`
⇒ แสดงคำเตือนพร้อมหมายเลขแถวในหน้าจอและในขั้นตรวจสอบ · **ส่งอนุมัติได้ตามปกติ**

### FN-06 — บันทึกร่างและออกเลขที่เอกสาร (DEC-11)
1. ตรวจ `DOC_TYPE('TWP').active` ที่ **F-DOCCFG** — ไม่เปิดใช้ ⇒ `DOCTYPE_INACTIVE`
2. validate ตาม 05_RULES §2
3. ครั้งแรกเท่านั้น: `ENG-DOC-NUM.next('TWP')` → `doc_no` (รูปแบบ `{PREFIX}-{YYYY}-{run:4}` · reset รายปี · scope global · ไม่ใช่ no-gap)
4. snapshot หัวกระดาษจาก Organization → `header_snapshot` (ใช้ตอนพิมพ์ ไม่ดึงสดอีก) · `doc_date` = วันที่บันทึกครั้งแรก
5. สถานะ `draft` · เขียน audit "สร้างเอกสาร"

### FN-07 — แก้ไขร่าง
อนุญาตเมื่อ `status = draft` และผู้ใช้เป็นเจ้าของ (`NOT_OWNER` ถ้าไม่ใช่) · เลขที่เดิม · audit "แก้ไขร่าง"
ใบที่ถูกส่งกลับแก้ไข (`returned = true`) แก้ไขได้ตามปกติ และ `returned` ถูกล้างเมื่อส่งอีกครั้ง

### FN-08 — ส่งอนุมัติ (resolve + freeze สายอนุมัติ)
1. เรียก DOA กลาง (F-DLG-001) `resolve(doc_type='twp', amount=null, department=<ฝ่ายของผู้ขอ>)` → รายการขั้น + role ต่อขั้น (**DOA-ENGINE-HOOK**)
2. ค่าเริ่มของผู้พิจารณาต่อขั้น: `role-line-manager` = ผู้บังคับบัญชาตรงจากผังองค์กร
3. ผู้ส่งเลือก/แก้ผู้พิจารณาได้ทุกขั้น — ผู้ขอเลือกตัวเองไม่ได้ (BR-DOA-04)
4. freeze ลง `approval_chain` (BR-DOA-02) · ขั้น 1 = `pending` ขั้นอื่น = `waiting` · สถานะใบ = `pending` · `returned = false`
5. audit "ส่งอนุมัติ" · DOA engine ยิง `doa_pending` เอง

### FN-09 — อนุมัติขั้นปัจจุบัน
เฉพาะผู้พิจารณาขั้นปัจจุบัน (`NOT_CURRENT_APPROVER`) · ขั้นนั้น = `approved` + เวลา + ความเห็น
มีขั้นถัดไป ⇒ ขั้นถัดไป = `pending` ใบยังคง `pending` · ครบทุกขั้น ⇒ ใบ = `approved`
**ไม่เปลี่ยนค่าในระบบ ไม่ส่งต่อระบบอื่น** (DEC-01 · DEC-02) — การตั้งหนี้/จ่ายคืนเงินสำรองทำนอกใบนี้

### FN-10 — ไม่อนุมัติ = ส่งกลับแก้ไข (DEC-09 · ตาม BR-DOA-03)
เหตุผลบังคับ (`REASON_REQUIRED`) · ใบกลับเป็น `draft` **เลขที่เดิม** · `returned = true` + เก็บเหตุผล/ผู้ส่งกลับ/เวลา
`approval_chain` ถูกล้างกลับเป็นค่าตั้งต้น (resolve ใหม่ตอนส่งรอบถัดไป ตาม BR-DOA-02) · audit "ไม่อนุมัติ — ส่งกลับแก้ไข"

### FN-11 — ยกเลิกเอกสาร
สถานะ `draft` หรือ `pending` เท่านั้น (DEC-09) · โดยเจ้าของหรือ admin role ของฝ่ายเจ้าของเอกสาร · เหตุผลบังคับ
ขั้นที่ยัง `pending`/`waiting` → `skipped` · ใบ = `cancelled` · ยิง event `twp_cancelled` ผ่าน ENG-NOTIFY

### FN-12 — การมองเห็น (query filter · DEC-10)
`เจ้าของ` OR (`status <> 'draft'` AND ผู้ใช้อยู่ใน `approval_chain`) OR `admin role ของฝ่ายเจ้าของเอกสาร`
ใบที่ไม่เข้าเงื่อนไข ⇒ ไม่อยู่ในผล A1 และ A2 ตอบ `NOT_FOUND`

### FN-13 — สร้างแบบพิมพ์ (PDF)
`docPrintData(record)` → data contract (`print/TWP_data-contract.md`) → render `form.tpl.html`
- เติมแถวว่างจนครบ **27 แถว** ตามกระดาษ (DEC-05) · เติมบรรทัด "เอกสารที่แนบ" จนครบ **3 บรรทัด** (DEC-06)
- ค่าแสดงทุกตัวเป็น string ที่จัดรูปแล้ว
- ช่องลงชื่อ = ผู้จัดทำ + 1 ช่องต่อขั้นใน `approval_chain` แบ่งแถวละ ≤ 4 (`sign_layout.max_per_row`)
- คำตัดสินผูก role จาก `print_config.decision_words` ไม่ผูกลำดับขั้น
- สำเนาเอกสาร: `ENG-DOC-STORE.store()` เมื่อใบเปลี่ยนเป็น `approved` (snapshot `approved_final`)

### FN-14 — ส่งออก CSV (DEC-12)
ส่งออกตามผลการกรองปัจจุบัน · หัวคอลัมน์ตามกระดาษ + รวมยอดคอลัมน์ค่าใช้จ่าย + สรุปท้ายใบ 4 ช่อง · UTF-8 BOM
