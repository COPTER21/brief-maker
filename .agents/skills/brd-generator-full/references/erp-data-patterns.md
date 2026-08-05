# ERP Common Data Patterns — 11 หมวด

ใช้ใน Step 4 ของ brd-generator-full สำหรับออกแบบ Section 6 (Data Entity & Fields)

---

## 1. Master-Detail Pattern (Header + Line Item)

**เมื่อใช้:** Transaction มีหลายรายการ (Order มีหลาย item, Invoice มีหลายบรรทัด)

**Pattern:**
```
Transaction_Header
├── transaction_no (PK, AUTO running)
├── customer_id (FK)
├── total_amount (calculated from lines)
├── status
└── audit fields

Transaction_Line
├── line_id (PK)
├── transaction_no (FK)
├── line_no (1, 2, 3, ...)
├── product_id (FK)
├── quantity
├── unit_price
├── line_total (qty × price)
└── audit fields
```

**Critical Rules:**
- header.total_amount = SUM(lines.line_total) — recalc on line change
- ลบ header → cascade delete lines
- Line ลำดับ (line_no) ห้ามซ้ำใน header เดียวกัน

---

## 2. Audit Fields (ทุก Entity)

**บังคับ:** ทุก entity ต้องมี

```
created_by      VARCHAR  -- user_id ที่สร้าง
created_date    DATETIME -- เวลาสร้าง
modified_by     VARCHAR  -- user_id ที่แก้ไขล่าสุด
modified_date   DATETIME -- เวลาแก้ไขล่าสุด
```

**Implementation:**
- Auto-fill จาก session.user
- Audit Log แยกต่างหาก (ทุก change ทุก field)

---

## 3. Soft Delete

**เมื่อใช้:** Entity ที่ลบแล้วยังต้อง audit / มี FK ไปหา

**Pattern:**
```
is_active         BOOLEAN  DEFAULT true
deactivated_by    VARCHAR  NULL
deactivated_date  DATETIME NULL
deactivate_reason TEXT     NULL
```

**Rules:**
- Filter is_active=true ใน default query
- Deactivate ≠ Delete (DB ยังเก็บ)
- Reactivate ได้ (clear deactivated_*)

---

## 4. Lookup with Snapshot

**เมื่อใช้:** Transaction อ้างอิง Master Data ที่อาจเปลี่ยนแปลง (Customer name, Product price)

**Pattern:**
```
Quote_Header
├── customer_id (FK to Customer)
├── customer_name (SNAPSHOT — เก็บค่า ณ เวลาสร้าง)
├── customer_tax_id (SNAPSHOT)
└── ...
```

**Why:** ถ้า Customer เปลี่ยนชื่อหลังออก Quote → Quote เก่ายังคงแสดงชื่อเดิม

**Rules:**
- Snapshot fields update เฉพาะตอนสร้าง / แก้ไขเฉพาะที่ allow
- Master change ไม่ propagate ย้อนหลัง

---

## 5. Running Number / Document Numbering

**เมื่อใช้:** Document ที่ต้องมีเลขเรียง (QT, PO, SO, Invoice, GR)

**Pattern:**
```
quote_no  VARCHAR(20)  -- "QT-2026-00001"
```

**Implementation:**
- Format: `[PREFIX]-[YEAR]-[5-digit]`
- Reset เมื่อ: ปีใหม่ / ไม่ reset (ขึ้นกับ policy)
- Locked via DB sequence หรือ atomic UPDATE
- ใช้ shared module: Document Numbering Engine

**Edge Cases:**
- Race condition → DB lock / sequence
- Gap allowed? (ปกติ: ใช่ จาก rollback)
- Reset logic → config

---

## 6. Status / Workflow Fields

**เมื่อใช้:** Entity มี state machine

**Pattern:**
```
status         VARCHAR  -- 'draft', 'submitted', 'approved', 'rejected'
submitted_by   VARCHAR  NULL
submitted_at   DATETIME NULL
approved_by    VARCHAR  NULL
approved_at    DATETIME NULL
rejected_by    VARCHAR  NULL
rejected_at    DATETIME NULL
reject_reason  TEXT     NULL
```

**Rules:**
- State transition table (Section 8) ต้องบังคับ
- ทุก state change ต้อง audit
- Reject Reason บังคับเมื่อ status = 'rejected'

---

## 7. Snapshot Fields (Detailed)

**ขยายจาก #4** — กรณีที่ต้อง snapshot หลายอย่าง

**Pattern:**
```
Quote_Line
├── product_id (FK)
├── product_code   (SNAPSHOT)
├── product_name   (SNAPSHOT)
├── unit_of_measure (SNAPSHOT)
├── unit_price     (SNAPSHOT — price ณ ตอนสร้าง)
├── currency       (SNAPSHOT)
├── exchange_rate  (SNAPSHOT)
```

**Critical:** ถ้า exchange rate / price เปลี่ยน → existing transactions ใช้ rate เดิม

---

## 8. Approval Workflow

**เมื่อใช้:** Document ที่ต้องผ่านการอนุมัติ

**Pattern:**
```
Approval_Step
├── step_id (PK)
├── transaction_no (FK)
├── step_no (1, 2, 3, ...)
├── approver_role (or approver_id)
├── approver_actual (FK — คนที่ approve จริง)
├── decision ('approve', 'reject', 'pending')
├── decision_date
├── reason TEXT
└── audit fields
```

**Rules:**
- ทุก step ต้องผ่านตามลำดับ (ห้าม skip)
- Reject ทำให้ workflow stop / กลับ Draft
- SoD: approver ≠ submitter

---

## 9. File Attachment

**Pattern:**
```
Attachment
├── attachment_id (PK)
├── entity_type ('quote', 'invoice', 'po', ...)
├── entity_id
├── file_name
├── file_size
├── file_type (mime)
├── file_path (or S3 key)
├── uploaded_by
├── uploaded_date
└── audit fields
```

**Rules:**
- Generic attachment table — ใช้ได้กับทุก entity
- File ลบจาก storage เมื่อ entity ลบ (cascade) หรือ soft delete
- Max size + allowed types ใน Config

---

## 10. Audit Log (Separate Entity)

**Pattern:**
```
Audit_Log
├── log_id (PK)
├── entity_type
├── entity_id
├── action ('create', 'update', 'delete', 'submit', 'approve', ...)
├── field_name (ถ้า update)
├── old_value
├── new_value
├── changed_by
├── changed_date
├── ip_address
├── user_agent
└── note
```

**Rules:**
- Append-only (ห้ามแก้)
- Bulk insert ใน background (performance)
- Retention policy (เก็บกี่ปี — Config)

---

## 11. Enhancement-Specific Patterns

**เมื่อใช้:** BRD type = Enhancement

### Action Table

```markdown
| Action | Field | ก่อน | หลัง | กระทบ |
|---|---|---|---|---|
| ADD | discount_tier_id | — | FK to Tier | สูตรคิดส่วนลด |
| MODIFY | unit_price | NUMBER | NUMBER (NULL allowed) | Quote สามารถมี unit_price ว่างได้ |
| REMOVE | legacy_field | TEXT | — | ลบ field |
| NO CHANGE | quote_no | VARCHAR | VARCHAR | — |
```

### Migration Notes

```markdown
### Migration Required:
- discount_tier_id default = 'TIER_DEFAULT' for existing rows
- unit_price NOT NULL constraint relaxed (existing data unaffected)
- legacy_field: backup before drop column
```

### Relationship Impact

```markdown
### กระทบ Relationships:
- Quote_Line → Tier (NEW FK)
- Quote_Header → User (existing — no change)
- Invoice → Quote (existing — no change)
```

---

## Input Types Reference

| Input Type | ใช้กับ | UI Render |
|---|---|---|
| AUTO | Auto-fill / Running Number | Read-only text |
| TEXT | Short text (< 255) | Input box |
| TEXTAREA | Long text | Multi-line |
| RICHTEXT | Formatted text | WYSIWYG editor |
| NUMBER | Integer / Decimal | Number input |
| DATE | Date only | Date picker |
| DATETIME | Date + Time | DateTime picker |
| DROPDOWN-SINGLE | Choose 1 from list | Select |
| DROPDOWN-MULTI | Choose many | Multi-select |
| LOOKUP | Reference Master | Lookup popup / autocomplete |
| TOGGLE | Boolean (yes/no) | Switch / Checkbox |

---

## Common Field Naming Convention

| Type | Convention | Example |
|---|---|---|
| Primary Key | `[entity]_id` | `quote_id` |
| Foreign Key | `[entity]_id` | `customer_id` |
| Snapshot | `[fk_entity]_[field]` | `customer_name`, `product_code` |
| Audit | `created_by`, `created_date`, `modified_by`, `modified_date` | — |
| Status | `status` | `'draft', 'submitted', ...` |
| Soft delete | `is_active` | boolean |
| Running | `[entity]_no` | `quote_no`, `invoice_no` |
| Date/time | `[event]_date` หรือ `[event]_at` | `submitted_date` / `submitted_at` |
| Amount | `[scope]_amount` | `total_amount`, `tax_amount`, `discount_amount` |

---

## Decision Tree: เลือก Pattern ไหน?

```
Entity นี้เป็น Transaction หรือ Master?
├── Master → Pattern #2 (Audit) + #3 (Soft Delete)
└── Transaction
    ├── มีหลายรายการไหม?
    │   ├── มี → Pattern #1 (Master-Detail) + #2 + #4 + #5
    │   └── ไม่มี → Pattern #2 + #4 + #5
    ├── มี Approval ไหม?
    │   ├── มี → + Pattern #6 (Status) + #8 (Approval Workflow)
    │   └── ไม่มี → + Pattern #6 (Status) basic
    ├── มี File Attachment ไหม?
    │   └── มี → + Pattern #9
    ├── ต้องการ Audit Trail ละเอียดไหม?
    │   └── ต้องการ → + Pattern #10
    └── BRD type = Enhancement?
        └── ใช่ → ใช้ Pattern #11 (Action Table)
```
