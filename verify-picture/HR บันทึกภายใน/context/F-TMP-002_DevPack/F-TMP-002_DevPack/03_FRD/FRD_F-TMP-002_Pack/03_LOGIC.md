# 03_LOGIC — F-TMP-002 บันทึกภายใน

## §3.1 Functions (Scope-Local)

### MEM-FN-01: createMemoDraft
- **Input:** `{to, subject, body, attachments[]}` + ผู้ใช้ปัจจุบัน
- **ขั้นตอน**
  1. ตรวจ `doc_type.MEM` เปิดใช้งานที่ F-DOCCFG — ปิดอยู่ → `DOCTYPE_INACTIVE`
  2. ตรวจ `to` `subject` `body` ไม่ว่าง — ไม่ครบ → `VALIDATION_FAILED`
  3. **ออกเลขที่: `ENG-DOC-NUM.next('MEM', company_ctx)`** ← จุดออกเลขเดียวของ feature นี้ (DEC-10 · ออกตอนบันทึกครั้งแรก) · ห้าม format เอง ห้าม +1 เอง
  4. snapshot หัวกระดาษจาก Organization ลง `header_snapshot` (ชื่อบริษัท + โลโก้)
  5. snapshot `from` จาก `Employee.full_name` + `Employee.department_name` ของผู้สร้าง
  6. `doc_date = today` · `status = 'draft'` · `approval_chain = []`
  7. append `audit`: "สร้างเอกสาร"
- **Output:** record พร้อม `doc_no`

### MEM-FN-02: updateMemoDraft
- แก้ได้เฉพาะ `status = 'draft'` และ `owner = ผู้ใช้ปัจจุบัน` — ไม่ใช่ → `NOT_OWNER`
- แก้ได้เฉพาะ `to` `subject` `body` `attachments` · **ห้ามแก้ `doc_no`** (immutable)
- append `audit`: "แก้ไขร่าง"

### MEM-FN-03: submitMemo
- ต้อง `status = 'draft'` และเป็นเจ้าของ
- **resolve สายอนุมัติจาก DOA entry ของ feature นี้ ณ เวลาที่กดส่ง แล้ว snapshot ลง `approval_chain`** (BR-DOA-02) — จำนวนขั้นและ role มาจาก DOA กลาง ห้าม hardcode ใน feature
- ผู้ใช้เลือกผู้พิจารณา 1 คนต่อขั้น · ต้องครบทุกขั้น · ผู้จัดทำอยู่ในรายชื่อไม่ได้ (BR-DOA-04 → `SELF_APPROVAL_DENIED`)
- ขั้นที่ 1 = `pending` · ขั้นอื่น = `waiting` · `status = 'pending'` · `submitted_at = now`
- DOA engine ยิง `doa_pending` เอง — feature ไม่ยิงซ้ำ

### MEM-FN-04: approveMemoStep
- ผู้เรียกต้องเป็น `assignee` ของขั้นที่ `pending` — ไม่ใช่ → `NOT_CURRENT_APPROVER`
- เก็บ `legal_opinion` ลง `approval_chain[i].note` และ `approval_chain[i].at = now` (= `legal_opinion_date`)
- มีขั้นถัดไป → ขั้นนั้นเป็น `pending`, `status` คง `pending` · ไม่มี → `status = 'approved'`
- **ไม่เปลี่ยนค่าใด ๆ ในระบบ และไม่ส่งข้อมูลต่อระบบอื่น** (DEC-01 · DEC-02)
- DOA engine ยิง `doa_result` เอง

### MEM-FN-05: rejectMemo
- ผู้เรียกต้องเป็นผู้พิจารณาขั้นปัจจุบัน · `legal_opinion` ว่างไม่ได้
- ขั้นปัจจุบัน = `rejected` · ขั้นที่เหลือ = `skipped` · `status = 'rejected'`

### MEM-FN-06: cancelMemo
- เรียกได้เมื่อ `status ∈ {draft, pending}` และผู้เรียกเป็นเจ้าของหรือ admin role (DEC-08) · `reason` บังคับ
- `status = 'cancelled'` · ขั้นที่ `pending` เป็น `skipped`
- **ยิง `mem_cancelled` ผ่าน ENG-NOTIFY** → ผู้พิจารณาขั้นปัจจุบัน (ยกเลิกระหว่างรออนุมัติ — DOA engine ไม่ยิงกรณีนี้)

### MEM-FN-07: listMemo / getMemo (การมองเห็น)
- กรองตาม DEC-09: `isAdmin || owner == me || (status != 'draft' && approval_chain.any(assignee == me))`
- ใบที่ไม่เข้าเงื่อนไข = `NOT_FOUND` (ไม่เปิดเผยว่ามีอยู่)
- ใช้ร่วมกับ API-11 (CSV) — ส่งออกเฉพาะแถวที่มองเห็นได้

### MEM-FN-08: reopenRejectedMemo
- `status = 'rejected'` และเป็นเจ้าของ → `status = 'draft'` · reset `approval_chain` เป็นค่า resolve ใหม่
- **`doc_no` คงเดิม ไม่ออกเลขใหม่** (DEC-08) · append `audit`: "กลับเป็นร่าง"

### MEM-FN-09: renderMemoPdf
- รวม data ตาม data contract (`MEM_data-contract.md`) แล้ว render `form.tpl.html` ฝั่ง server (renderer เดียวกับ prototype — ตรงกันทุกไบต์)
- ช่องลงชื่อ = `sign_rows` จาก `approval_chain` **1 ช่องต่อขั้น ไม่มีช่องผู้ขอ** (DEC-07 · DEC-14) · แบ่งแถวละ ≤4 ตาม `print_config.sign_layout`
- `legal_lines` เติมบรรทัดว่างจนครบ `print_config.min_rows` (2)
- **เก็บสำเนา: `ENG-DOC-STORE.store(pdf, 'MEM', memo_id, 'approved_final')`** เมื่อเอกสารเข้าสถานะ `approved` — engine ตรวจ flag เองว่าจะเก็บหรือไม่

### MEM-FN-10: attachMemoFile
- ส่งต่อ Document Center ตาม file policy เดิม · ชนิด/ขนาดไม่ผ่าน → ปฏิเสธเฉพาะไฟล์นั้น

## §3.2 Engines (Reusable)
| Engine | ใช้ทำอะไร | เจ้าของ |
|---|---|---|
| ENG-DOC-NUM | ออกเลขที่ `MEM` | F-DOCCFG |
| ENG-DOC-STORE | เก็บสำเนา PDF | F-DOCCFG |
| ENG-NOTIFY | ส่ง `mem_cancelled` | F-NOTIFY |
| DOA engine (DOA-ENGINE-HOOK) | resolve/freeze สายอนุมัติ · ยิง `doa_pending` / `doa_result` | F-DLG-001 |

> **ไม่มี engine ใหม่** — feature นี้ไม่มีสูตรคำนวณและไม่มีค่าคงที่บนกระดาษ

## §3.3 API ↔ Logic Trace
| API | Function | Engine ที่เรียก |
|---|---|---|
| API-03 | MEM-FN-01 | ENG-DOC-NUM |
| API-04 | MEM-FN-02 | — |
| API-05 | MEM-FN-03 | DOA engine |
| API-06 | MEM-FN-04 | DOA engine |
| API-07 | MEM-FN-05 | DOA engine |
| API-08 | MEM-FN-06 | ENG-NOTIFY (`mem_cancelled`) |
| API-09 | MEM-FN-08 | DOA engine |
| API-10 | MEM-FN-09 | ENG-DOC-STORE |
| API-01/02/11 | MEM-FN-07 | — |
| API-12 | MEM-FN-10 | Document Center |
