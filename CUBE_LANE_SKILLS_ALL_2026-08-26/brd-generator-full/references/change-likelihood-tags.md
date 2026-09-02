# Change Likelihood Tags

ใช้ติด Tag กับทุก Business Rule ที่มีตัวเลข/เงื่อนไข ใน Section 9 ของ BRD

---

## 4 Tags

### 🔒 FIXED
**คำนิยาม:** ค่า/เงื่อนไขที่ไม่เปลี่ยนแปลง — เป็น Business Logic หลัก

**ตัวอย่าง:**
- "Status เริ่มต้น = Draft"
- "PDF ต้องใช้ A4 portrait"
- "Customer ID เป็น primary key"

**Implementation:** Hardcode ได้

---

### ⚙️ CONFIGURABLE
**คำนิยาม:** ค่า/เงื่อนไขที่อาจปรับตาม policy — แต่เปลี่ยนแค่ "ค่า" (ไม่ใช่ logic)

**ตัวอย่าง:**
- "DoA ผู้จัดการ ≤ 100,000 บาท"
- "QT อายุ 30 วัน"
- "Approval SLA = 1 วัน"

**Implementation:** Config Table หรือ Admin Panel

---

### 🔄 DYNAMIC
**คำนิยาม:** ค่า/เงื่อนไขที่ซับซ้อน — เปลี่ยนทั้ง "เงื่อนไข" + "logic"

**ตัวอย่าง:**
- "ส่วนลด: ถ้า qty>100 → 5%, ถ้า qty>500 → 10%, ถ้าเป็น VIP → +2%"
- "Commission rate ขึ้นกับ region + product category + tier"
- "Approval flow ขึ้นกับ amount + customer type + product"

**Implementation:** Rule Management หรือ Engine Management

---

### ⚠️ WARNING
**คำนิยาม:** ยังไม่ตัดสินใจ — รอ Stakeholder confirm

**ตัวอย่าง:**
- "SLA Approval ใช้เวลาเท่าไหร่ — รอ Sales Director"
- "DoA ระดับใหม่ — รอ CEO ตัดสินใจ"

**Implementation:** ห้ามเริ่มพัฒนาส่วนนี้จนกว่า Resolve

---

## Misclassification Patterns

### ❌ Pattern 1: ติด FIXED ที่จริงๆ ควรเป็น CONFIGURABLE

**สัญญาณ:**
- มีตัวเลขในข้อความ ("≤ 100,000", "30 วัน")
- เคยมีคนถามว่า "ปรับได้ไหม"
- เป็น policy ที่อาจเปลี่ยนทุก 1-2 ปี

**แก้:** เปลี่ยนเป็น CONFIGURABLE

### ❌ Pattern 2: ติด CONFIGURABLE ที่จริงๆ ควรเป็น DYNAMIC

**สัญญาณ:**
- มีคำว่า "ถ้า...แล้ว..."
- มีหลายเงื่อนไขซ้อน (if-else if-else)
- ต้องเก็บ rule แต่ละ rule แยกกัน

**แก้:** เปลี่ยนเป็น DYNAMIC

### ❌ Pattern 3: ติด CONFIGURABLE ทั้งที่ไม่มีตัวเลข

**สัญญาณ:**
- เป็น Business Logic core (เช่น "QT ต้องมี customer")
- ไม่มีอะไรให้ "config"

**แก้:** เปลี่ยนเป็น FIXED

### ❌ Pattern 4: ไม่ติด Tag เลย ทั้งที่ควรติด

**สัญญาณ:**
- มี Rule ที่มีตัวเลข/เงื่อนไข แต่ไม่ติด Tag

**แก้:** ติด Tag (เริ่มจาก WARNING ถ้าไม่แน่ใจ)

### ❌ Pattern 5: ติด WARNING ค้างนาน

**สัญญาณ:**
- WARNING ที่ไม่มีแผนหารือ
- WARNING ที่ผ่านมาหลายเดือนยังไม่ Resolve

**แก้:** ระบุแผนหารือ + กำหนดวันที่ + ใส่ Section 15 Open Questions
ถ้ายัง resolve ไม่ได้ → ไม่ผ่าน Quality Gate (C18)

---

## Decision Tree: ติด Tag ยังไง?

```
มี Business Rule ที่มีตัวเลข/เงื่อนไขไหม?
├── ไม่มี → ไม่ต้องติด Tag
└── มี
    ├── มีหลายเงื่อนไขซ้อน (if-else if-else) ไหม?
    │   ├── มี → DYNAMIC
    │   └── ไม่มี
    │       ├── เคยปรับ/อาจปรับใน 1-3 ปี ไหม?
    │       │   ├── ไม่ปรับเลย → FIXED
    │       │   ├── ปรับ → CONFIGURABLE
    │       │   └── ไม่แน่ใจ → WARNING (รอ stakeholder)
    │       └── ...
    └── ...
```

---

## ระดับความยืดหยุ่น (สำหรับ CONFIGURABLE/DYNAMIC)

### 🗄️ Config File
- ใครเปลี่ยน: IT/Dev
- บ่อยแค่ไหน: นานๆ ครั้ง (ปีละ 1 ครั้ง)
- เปลี่ยนอะไร: แค่ค่า
- ตัวอย่าง: Email server, log level, timezone

### 🎛️ Admin Panel
- ใครเปลี่ยน: Admin user
- บ่อยแค่ไหน: เป็นระยะ (เดือนละ-ปีละหลายครั้ง)
- เปลี่ยนอะไร: ค่า
- ตัวอย่าง: DoA limit, SLA threshold, document numbering

### 🧩 Rule Management
- ใครเปลี่ยน: ผู้บริหาร / Business Owner
- บ่อยแค่ไหน: เป็นระยะ-บ่อย
- เปลี่ยนอะไร: เงื่อนไข + ค่า
- ตัวอย่าง: Discount rules, commission rules, approval flow rules

### 🧠 Engine Management
- ใครเปลี่ยน: ผู้บริหาร / Business Architect
- บ่อยแค่ไหน: เป็นระยะ (Big change)
- เปลี่ยนอะไร: Flow + สูตร + กระบวนการ
- ตัวอย่าง: Approval Engine, Discount Engine, Routing Engine

---

## Inference Defaults (สำหรับ Pipeline Mode)

ถ้าไม่มี Stakeholder ตอบ ใช้ defaults ตาม module + rule type:

### By Module Type
| Module | Default Mode |
|---|---|
| Finance | strict — Config File default + เน้น audit |
| HR | strict — Admin Panel default + PII |
| Sales | flexible — Admin Panel default |
| Operations | flexible — Rule Management default |
| AI/Automation | dynamic — Rule Management default |

### By Rule Type
| Rule Type | Default Level |
|---|---|
| Threshold / Limit / Cap | Admin Panel |
| Formula / Calculation | Rule Management |
| Workflow logic | Engine Management |
| Constant / Lookup | Config File |
| Mapping table | Admin Panel |

---

## ตัวอย่าง Tag Table (ใช้ใน BRD Section 9)

| Rule ID | Rule | Tag | ใครเปลี่ยน | บ่อยแค่ไหน | ระดับ | เหตุผล |
|---|---|:---:|---|---|---|---|
| R01 | Status เริ่มต้น = Draft | FIXED | — | — | — | Business core |
| R02 | QT อายุ 30 วัน | CONFIGURABLE | Admin | ปีละ 1-2 ครั้ง | Admin Panel | เปลี่ยนค่า |
| R03 | DoA ผู้จัดการ ≤ 100K | CONFIGURABLE | Admin | ปีละ 1-2 ครั้ง | Admin Panel | เปลี่ยนค่า |
| R04 | สูตรส่วนลด tier | DYNAMIC | Sales Director | ตามแคมเปญ | Rule Management | เงื่อนไขซับซ้อน |
| R05 | SLA Approval | WARNING | — | — | — | รอ Sales Director |
