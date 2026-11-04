# 03_LOGIC — F-TMP-003 คำขอมีและใช้ลายเซ็นดิจิทัล (DSR)

## 1. State machine
`draft → pending → approved` · `pending → draft` (ไม่สามารถดำเนินการได้ · DEC-08) · `draft|pending → cancelled`
`approved` = ล็อกแก้ไข · เอกสารที่ถูกยกเลิกแก้ต่อไม่ได้

## 2. ขอบเขตผลข้างเคียง (DEC-01 · DEC-02)
อนุมัติครบแล้ว **ไม่เปลี่ยนค่าในระบบ** และ **ไม่ส่งข้อมูลต่อระบบอื่น** — การออกใบรับรอง CA และการแก้ชื่อในทะเบียนพนักงาน (F-EMP-001) ทำนอกใบนี้
event ที่ประกาศไว้มีเฉพาะ `dsr_cancelled` · `dsr_name_change_requested` (ENG-NOTIFY)

### FN-01 เตรียมร่างใหม่
snapshot ผู้ขอจากทะเบียนพนักงาน: ชื่อ-นามสกุล ไทย/อังกฤษ · ตำแหน่ง · สังกัดหน่วยงาน · Email · โทร
`made_at` เสนอค่าเริ่มจากสถานที่ทำงานของผู้ขอ · `case_kind` เริ่มที่ `first` · `certified = false`

### FN-02 เลือกกรณี (case_kind)
เลือกได้ 1 ข้อเท่านั้น (DEC-16)
- `first` → ล้าง `renew_reason` · `change_type` · ช่องชื่อเดิม/ชื่อใหม่ทั้งหมด
- `renew` → บังคับเลือก `renew_reason` 1 ข้อ · ล้างช่องชื่อ
- `change` → บังคับเลือก `change_type` 1 ข้อ แล้วเปิดช่องชื่อตาม FN-03

### FN-03 ช่องชื่อตามประเภทการเปลี่ยน (DEC-13 · DEC-14)
| `change_type` | ช่องที่เปิดและบังคับ | ช่องที่ต้องว่าง |
|---|---|---|
| `first_name` | `old_first_name_th` · `new_first_name_th` · `new_first_name_en` | ช่องนามสกุลทั้งหมด |
| `last_name` | `old_last_name_th` · `new_last_name_th` · `new_last_name_en` | ช่องชื่อทั้งหมด |
| `both` | ครบทั้ง 6 ช่อง | — |
ชื่อเดิมภาษาอังกฤษ **ไม่มีช่องกรอก** — อ่านจากทะเบียนพนักงานมาแสดงคู่กับชื่อใหม่ (DEC-15)
`case_kind ≠ change` → ทั้ง 6 ช่องต้องเป็นค่าว่าง

### FN-04 บันทึกครั้งแรก → ออกเลขที่ (DEC-10)
เช็ค doc_type `DSR` เปิดใช้ที่ F-DOCCFG ก่อน → เรียก **ENG-DOC-NUM**`.next('DSR')` รูปแบบ `DSR-{YYYY}-{run:4}` reset รายปี scope global ไม่ no-gap
`doc_date` = วันที่บันทึกครั้งแรก · `header_snapshot` (ชื่อบริษัท/โลโก้) เก็บลงเอกสารตอนออกเลข

### FN-05 คำรับรองของผู้ยื่นคำขอ
`certified` ต้องเป็น true ก่อนออกจากขั้นที่ 1 · ข้อความรับรองตรงตามย่อหน้าบนกระดาษ (PDPA + พ.ร.บ. ธุรกรรมทางอิเล็กทรอนิกส์ พ.ศ. 2544)

### FN-06 ส่งอนุมัติ → resolve DOA (DEC-03)
**DOA-ENGINE-HOOK** — เรียก DOA กลาง (F-DLG-001) entry `DOA-DSR-01` ด้วย `doa_type = dsr` · `approval_scope = document_sign`
ค่าเริ่ม 1 ขั้น `role-mgr-hr` ป้าย "เจ้าหน้าที่" · จำนวนขั้น/role ตั้งที่ DOA กลาง — **ห้าม hardcode ในฟีเจอร์**
resolve ตอนส่งแล้ว freeze ลง `approval_chain` (BR-DOA-02) · ผู้ส่งเลือกคนต่อขั้นได้จาก slot picker

### FN-07 พิจารณา "ดำเนินการได้"
ขั้นปัจจุบัน `approved` → มีขั้นถัดไปไหม: มี → ขั้นถัดไป `pending` · ไม่มี → เอกสาร `approved`
**ไม่เปลี่ยนค่าใด ๆ ในระบบ และไม่ส่งต่อระบบอื่น (DEC-01 · DEC-02)**

### FN-08 พิจารณา "ไม่สามารถดำเนินการได้" (DEC-08)
บันทึกเหตุผลลงขั้นนั้น (ใช้เป็นข้อความช่อง "เนื่องจาก" บนแบบพิมพ์) → เอกสาร **กลับเป็น `draft` เลขเดิม** · ล้าง `submitted_at` · `approval_chain` resolve ใหม่ตอนส่งรอบถัดไป · ประวัติเก็บไว้ทั้งหมด

### FN-09 ยกเลิกเอกสาร (DEC-08)
เจ้าของหรือ admin role · สถานะ `draft`/`pending` · เหตุผลบังคับ → `cancelled` · ขั้นที่ค้างเป็น `skipped` · ยิง event `dsr_cancelled` ผ่าน ENG-NOTIFY

### FN-10 การมองเห็น (DEC-09)
`canSee(doc, user)` = เจ้าของ ∨ (สถานะ ≠ draft ∧ user อยู่ใน `approval_chain`) ∨ user มี admin role ของฝ่ายทรัพยากรบุคคล
ร่างของคนอื่นไม่เห็นเด็ดขาด — บังคับที่ชั้น service ไม่ใช่แค่ UI

### FN-11 แบบพิมพ์ (DEC-06 · DEC-07)
render จาก `print/form.tpl.html` (logic-less) + data contract · ช่องลงชื่อ = ผู้ยื่นคำขอ + 1 ช่องต่อขั้นใน `approval_chain` (ไม่ fix จำนวน) แถวละ ≤ 4
คำตัดสินผูก role จาก `print_config.decision_words.by_role` (`role-mgr-hr` → ดำเนินการได้ / ไม่สามารถดำเนินการได้)
ช่องตัวอย่างลายมือชื่อและลายมือเขียนชื่อเว้นเป็นกรอบว่างให้เซ็นหลังพิมพ์ ไม่ใช้ภาพลายมือชื่อแทนการพิจารณา
สำเนาเก็บผ่าน **ENG-DOC-STORE** เมื่อเอกสารถึงสถานะ `approved` (`approved_final`)

### FN-12 ของเสริม (DEC-11)
แนบไฟล์ (file policy เดียวกับ Document Center) · ส่งออก CSV ตามตัวกรอง · **ไม่มี** ทำซ้ำ · **ไม่มี** ประกาศเมื่ออนุมัติ

### FN-13 แจ้งผู้ดูแลทะเบียนพนักงาน (กรณีที่ 3)
ตอน `draft → pending` และ `case_kind = change` → ยิง event `dsr_name_change_requested` ผ่าน ENG-NOTIFY ถึง `role-mgr-hr`
เป็นการ **แจ้งให้คนไปแก้เอง** ไม่ใช่ระบบแก้ทะเบียนให้ (DEC-01 · DEC-02)
