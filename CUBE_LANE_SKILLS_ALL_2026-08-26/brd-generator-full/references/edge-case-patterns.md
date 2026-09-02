# Edge Case Patterns — 9 หมวด

ใช้ใน Step 2 (Enrich) ของ brd-generator-full
สแกน Section 5 + 9 ของ BRD แล้วเทียบกับ pattern ด้านล่าง

---

## FU — File Upload

**Trigger:** Feature มี upload file (รูป, เอกสาร, attachment)

### Patterns
- **FU-01**: File size เกิน limit → block + แสดงข้อความ
- **FU-02**: File type ไม่อนุญาต → block + แสดง list ของ type ที่อนุญาต
- **FU-03**: Upload หลายไฟล์พร้อมกัน → progress bar + handle failure ทีละไฟล์
- **FU-04**: Upload ถูกตัดกลางคัน (network drop) → retry / resume
- **FU-05**: File corrupted ตอน upload → checksum verify + reject
- **FU-06**: Duplicate file name → rename / overwrite / cancel (ถาม user)
- **FU-07**: ขณะ upload user navigate ออกจากหน้า → confirm dialog
- **FU-08**: ไฟล์มี virus → scan + block + แจ้ง admin
- **FU-09**: Storage เต็ม → block + แจ้ง admin

---

## CA — Concurrent Access

**Trigger:** Feature มีหลาย user ที่อาจแก้ข้อมูลเดียวกัน

### Patterns
- **CA-01**: 2 users แก้ record เดียวกัน → optimistic lock + version field
- **CA-02**: User A อ่าน → User B แก้ → User A save → conflict detection
- **CA-03**: Approve while editing → notify approver + lock
- **CA-04**: Bulk action กระทบ record ที่ user อื่นกำลังแก้ → skip + report
- **CA-05**: Delete record ที่อ้างอิงจาก feature อื่น → cascade/restrict/SET NULL
- **CA-06**: Session timeout ระหว่างกรอกฟอร์ม → save draft auto / warn
- **CA-07**: Race condition ใน Running Number → lock table หรือ sequence
- **CA-08**: Webhook callback ก่อน main transaction commit → idempotent

---

## EM — Email / Notification

**Trigger:** Feature มีส่ง email, SMS, LINE OA, push notification

### Patterns
- **EM-01**: Email server down → queue + retry 3 ครั้ง + log
- **EM-02**: Email bounce → mark contact as invalid + alert
- **EM-03**: Recipient เปลี่ยน email หลัง trigger → ส่งไปที่ใหม่ (snapshot vs current)
- **EM-04**: Notification ส่งซ้ำเพราะ retry → idempotent + message_id
- **EM-05**: User opt-out → respect preference
- **EM-06**: Template มี variable ที่ไม่มีข้อมูล → fallback / skip
- **EM-07**: Email ส่งช้าเกิน SLA → warn / escalate
- **EM-08**: User เปลี่ยนภาษา → ใช้ template ตาม locale
- **EM-09**: Spam filter block → check delivery status + alternative channel

---

## DI — Data Integrity / Lookup Master Data

**Trigger:** Feature มี FK / lookup ไปยัง Master Data

### Patterns
- **DI-01**: Master record ถูก deactivate ระหว่างที่ Transaction กำลังใช้ → ใช้ snapshot
- **DI-02**: Master record ถูกลบ → restrict / SET NULL / snapshot
- **DI-03**: Master record ถูกแก้ชื่อ → snapshot ค่าตอนสร้าง transaction
- **DI-04**: ค้นหา Master ไม่พบ → suggest similar / create new
- **DI-05**: Master มี duplicate (data quality) → deduplication
- **DI-06**: Master import มี FK ไปยัง record ที่ยังไม่มี → reject / create stub
- **DI-07**: Currency exchange rate เปลี่ยน → snapshot rate ตอน transaction
- **DI-08**: Price list หมดอายุ → ใช้ effective date ตอน transaction

---

## CL — Calculation

**Trigger:** Feature มีการคำนวณตัวเลข (sum, multiply, discount, tax)

### Patterns
- **CL-01**: Overflow number → handle / warn / block
- **CL-02**: Divide by zero → block + meaningful error
- **CL-03**: Rounding error (sum of lines ≠ total) → consistent rounding strategy
- **CL-04**: Negative amount → block / require approval
- **CL-05**: Discount > 100% → block
- **CL-06**: Tax calculation ของหลาย rate → tax per line vs document-level
- **CL-07**: Foreign currency → exchange rate snapshot
- **CL-08**: Recalculate when line item changes → cascade update header
- **CL-09**: Manual override of calculation → audit log + reason required
- **CL-10**: VAT vs non-VAT items in same document → separate calculation

---

## ST — Status / Workflow

**Trigger:** Feature มี state machine / approval flow

### Patterns
- **ST-01**: Skip step in workflow → block (ยกเว้น override role)
- **ST-02**: Revert to earlier state → audit log + reason
- **ST-03**: Approve own document → block (SoD)
- **ST-04**: Status เปลี่ยนจาก final state กลับมา (e.g., Approved → Draft) → require manager
- **ST-05**: Workflow definition เปลี่ยน ระหว่างที่มี in-flight transactions → version workflow
- **ST-06**: Reject reason ว่างเปล่า → require
- **ST-07**: Withdraw submission → กลับสู่ Draft + audit
- **ST-08**: Approval queue เกินจำนวน → escalate / delegate
- **ST-09**: Approver ลาออก → delegate / re-route
- **ST-10**: Cancellation of completed transaction → require manager + audit

---

## PD — PDF / Document Generation

**Trigger:** Feature มีการสร้าง PDF / Invoice / Report เอกสาร

### Patterns
- **PD-01**: ข้อความยาวเกิน → truncate / wrap / overflow page
- **PD-02**: Image ใหญ่เกิน → compress / fit-to-page
- **PD-03**: Font ไทยไม่ rendered → fallback font
- **PD-04**: PDF generation failed (server error) → retry + log
- **PD-05**: Logo missing → fallback placeholder + warn
- **PD-06**: เลขเอกสาร running number ขัดแย้ง → lock + atomic
- **PD-07**: Reprint of cancelled document → watermark "CANCELLED"
- **PD-08**: Multi-language PDF → font support per locale
- **PD-09**: Digital signature failed → reject + retry

---

## PM — Permission / Authorization

**Trigger:** Feature มี role-based access control

### Patterns
- **PM-01**: User role เปลี่ยน ระหว่าง session → logout / refresh permissions
- **PM-02**: API call without auth → 401 + redirect login
- **PM-03**: API call with valid auth but insufficient permission → 403 + log
- **PM-04**: User access data ที่ไม่ใช่ของตัวเอง (e.g., other branch) → block + alert
- **PM-05**: Bulk action กระทบ record ที่ user ไม่มีสิทธิ → skip per record
- **PM-06**: Delegated approval (acting on behalf) → audit log "as delegated by X"
- **PM-07**: Read vs Write permission → separate check
- **PM-08**: Permission inheritance (parent/child) → cascade correctly
- **PM-09**: Temporary access expiry → auto-revoke

---

## EN — Enhancement-specific

**Trigger:** BRD type = Enhancement

### Patterns
- **EN-01**: Existing data ไม่ตรงกับ schema ใหม่ → migration script
- **EN-02**: Existing data ละเมิด validation rule ใหม่ → grandfather / migrate / flag
- **EN-03**: Feature เดิมยังคงทำงานหลัง enhancement (regression) → ตรวจครบ
- **EN-04**: User ใช้ workflow เดิม + workflow ใหม่ พร้อมกัน → handle both
- **EN-05**: API contract เปลี่ยน → versioning (v1, v2)
- **EN-06**: UI เปลี่ยน user เคยใช้ shortcut เดิม → migration guide / tutorial
- **EN-07**: Permission model เปลี่ยน → backfill permission for existing roles
- **EN-08**: Audit log format เปลี่ยน → old logs ยัง readable
- **EN-09**: Config เดิม hardcode → migrate to Config Table

---

## Pattern Matching Logic

```
สแกน BRD แล้วทำ:

1. มี keyword "upload" / "ไฟล์แนบ" / "attach" → ตรวจ FU patterns
2. มี keyword "หลาย user" / "concurrent" / "approval" → ตรวจ CA patterns
3. มี keyword "email" / "notification" / "LINE" / "SMS" → ตรวจ EM patterns
4. มี FK / lookup ไปยัง Master Data → ตรวจ DI patterns
5. มี keyword "คำนวณ" / "sum" / "ส่วนลด" / "ภาษี" → ตรวจ CL patterns
6. มี state diagram / status flow → ตรวจ ST patterns
7. มี keyword "PDF" / "ใบเสนอราคา" / "พิมพ์" / "Invoice" → ตรวจ PD patterns
8. มี Section 4 (Roles & Permissions) → ตรวจ PM patterns
9. ถ้า BRD type = Enhancement → ตรวจ EN patterns เพิ่ม

แสดงเฉพาะ patterns ที่ตรงกับ feature → ใส่ Section 10.2 แบบ checkbox ☐
```
