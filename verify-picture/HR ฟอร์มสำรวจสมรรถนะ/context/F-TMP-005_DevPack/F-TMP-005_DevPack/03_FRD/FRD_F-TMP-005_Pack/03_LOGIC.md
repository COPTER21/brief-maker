# FRD 03 · LOGIC — F-TMP-005 แบบฟอร์มสำรวจสมรรถนะ

## 3.0 State machine
```
(new) --บันทึกร่าง--> draft --ส่งอนุมัติ--> pending --เห็นชอบครบทุกขั้น--> approved
                        ^                        |
                        |--ส่งกลับแก้ไข (เลขเดิม)--|
   draft | pending --ยกเลิก (มีเหตุผล)--> cancelled
```
- `rejected` เป็นสถานะชั่วคราวของ **ขั้นใน approval_chain** เท่านั้น — ตัวเอกสารกลับเป็น `draft` ทันที (DEC-09)
- ผ่านครบทุกขั้นแบบ sequential จึงเป็น `approved` (BR-DOA ของ DOA กลาง)

## FN-01 · บันทึกร่าง / ออกเลขที่เอกสาร
- ตรวจสถานะเปิดใช้ของ doc_type `CMP` ที่ **F-DOCCFG** ก่อน — ยังไม่เปิดใช้ → `DOC_TYPE_INACTIVE`
- บันทึกครั้งแรกเรียก `ENG-DOC-NUM.next('CMP', company_ctx)` (DEC-11 · `issue_on: first_save`) — ห้าม format เลขเอง ห้าม +1 เอง
- snapshot ข้อมูลผู้รับประเมิน (`employee_name` · `position_name` · `department_name`) และหัวกระดาษ (`header_snapshot`) ลงเอกสาร ณ เวลาออกเลข
- แก้ร่างครั้งถัดไปใช้เลขเดิม (ไม่ออกใหม่)

## FN-02 · ตรวจความครบถ้วนก่อนบันทึก/ส่ง
- `assessed_on` ต้องมีค่า
- `core_lines` และ `func_lines` ต้องมีอย่างน้อย 1 แถวที่มี `competency_name`
- แถวที่มี `competency_name` ต้องมี `level` (1–4) → ไม่มี = `LEVEL_REQUIRED`
- แถวที่ไม่มี `competency_name` แต่มี `description` หรือ `level` = แถวค้าง ต้องแก้หรือลบ
- แถวว่างทั้งแถวถูกตัดทิ้งตอนบันทึก ไม่เก็บลงฐานข้อมูล
- **เตือนไม่บล็อก:** มี `gaps` แต่ไม่ได้เลือก `development_plan` เลย

## FN-03 · ส่งอนุมัติ
- เรียก **DOA-ENGINE-HOOK** `GET /api/doa/resolve?doc_type=CMP&requester={emp}` → ได้ chain ตามจำนวนขั้นที่ตั้งที่ DOA กลาง (DEC-03)
- ผู้ส่งเลือกผู้พิจารณา 1 คนต่อขั้น (ค่าเริ่มจากผังองค์กร) — ผู้รับประเมินเลือกตัวเองไม่ได้ (BR-DOA-04)
- freeze chain ลง `approval_chain` (BR-DOA-02) · ขั้นแรก `pending` · สถานะเอกสาร = `pending`
- DOA engine ยิง `doa_pending` เอง — feature **ห้าม**ประกาศซ้ำ

## FN-04 · เห็นชอบ (approve ขั้นปัจจุบัน)
- เฉพาะผู้ที่เป็น assignee ของขั้น `pending` — ไม่ใช่ → `NOT_CURRENT_APPROVER`
- ปิดขั้นปัจจุบัน → เปิดขั้นถัดไป (`waiting` → `pending`) · ไม่มีขั้นถัดไป → เอกสาร `approved`
- คำที่แสดงมาจาก `print_config.decision_words.by_role[role_id]` (ผูก role ไม่ผูกลำดับขั้น) — `role-line-manager` = "เห็นชอบ"
- **อนุมัติครบแล้วไม่เปลี่ยนค่าใด ๆ ในระบบ และไม่ส่งต่อ module อื่น (DEC-01 · DEC-02)** — เก็บไว้ในเอกสารอย่างเดียว

## FN-05 · ส่งกลับแก้ไข (reject)
- ต้องมี `reason` — ไม่มี → `REASON_REQUIRED`
- ปิดขั้นปัจจุบันเป็น `rejected` + เก็บเหตุผล → **เอกสารกลับเป็น `draft` เลขเดิม** `submitted_at = null` และ resolve chain ใหม่ตอนส่งรอบถัดไป (DEC-09)
- บันทึกประวัติ append-only 2 รายการ: ผลการพิจารณา + "กลับเป็นร่าง"
- DOA engine ยิง `doa_result` เอง — feature ห้ามประกาศซ้ำ

## FN-06 · ยกเลิกเอกสาร
- เฉพาะสถานะ `draft` / `pending` โดยเจ้าของใบ หรือ admin role (`role-mgr-hr`) · ต้องมี `reason` (DEC-09)
- ขั้นที่ยัง `pending`/`waiting` เปลี่ยนเป็น `skipped` · เอกสาร `cancelled`
- ถ้ายกเลิกตอนสถานะ `pending` → `ENG-NOTIFY.emit('cmp_cancelled', { ref, actor, reason })` แจ้งผู้พิจารณาขั้นปัจจุบัน

## FN-07 · ออกแบบพิมพ์ PDF + เก็บสำเนา
- render ฝั่ง server จาก `print/form.tpl.html` (logic-less) + `docPrintData()` ตาม data contract
- ตารางระดับ 1–4 ในแบบพิมพ์มาจาก **config** `CompetencyLevelConfig.levels[]` ทุกครั้ง (DEC-04) — ห้าม hardcode คำอธิบายในเทมเพลตหรือในโค้ด
- เติมแถวว่างให้ครบขั้นต่ำตามกระดาษ (core 5 · func 6) ก่อนส่งเข้าเทมเพลต (DEC-05 · DEC-06)
- ช่องลงชื่อ = ผู้รับประเมิน + 1 ช่องต่อขั้นใน `approval_chain` แบ่งแถวละ ≤ 4 (DEC-08) — ไม่ fix จำนวน ไม่ใช้ภาพลายมือชื่อ
- เมื่อเอกสารเป็น `approved` เรียก `ENG-DOC-STORE.store('CMP', id, pdf)` (snapshot `approved_final`)

## FN-08 · การมองเห็น (ใช้กับทุก endpoint ที่คืนรายการ/ใบ)
`เห็นได้ = เป็นเจ้าของใบ` **หรือ** `เป็น assignee ในสายอนุมัติ และเอกสารไม่ใช่ draft` **หรือ** `เป็น admin role ของฝ่ายบุคคล` (DEC-10)
— ร่างของคนอื่นต้องไม่หลุดถึงผู้พิจารณาเด็ดขาด
