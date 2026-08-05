# Flexibility Questionnaire Guide

ใช้ใน Step 3 ของ brd-generator-full
สำหรับสร้างคำถามให้ user/BA ไปถาม Stakeholder และวิเคราะห์คำตอบเป็นระดับความยืดหยุ่น

---

## เมื่อไหร่ใช้

หลังจาก Step 2 (Enrich) เสร็จ ตรวจ Section 9 → ถ้ามี Rule ที่ติด **CONFIGURABLE / DYNAMIC / WARNING** → สร้างคำถาม

---

## คำถามมาตรฐาน

### Q1: ใครเป็นคนเปลี่ยนค่า/เงื่อนไขนี้?

**ตัวเลือก:**
- A. IT / Developer (ต้อง deploy)
- B. Admin User (Admin Panel)
- C. ผู้บริหาร / Business Owner
- D. ไม่เปลี่ยน — ถูกแล้ว

**Mapping:**
- A → Config File
- B → Admin Panel
- C → Rule Management หรือ Engine Management
- D → ควรเปลี่ยน Tag เป็น FIXED

---

### Q2: บ่อยแค่ไหน?

**ตัวเลือก:**
- A. นานๆ ครั้ง (ปีละ 1 ครั้ง หรือเปลี่ยนครั้งเดียวจบ)
- B. เป็นระยะ (เดือนละครั้ง — ปีละหลายครั้ง)
- C. บ่อย (สัปดาห์ละครั้ง / แคมเปญละครั้ง)
- D. Real-time (ตามเหตุการณ์)

**Mapping:**
- A + IT → Config File
- A + Admin → Admin Panel
- B + Admin → Admin Panel
- B + Business → Rule Management
- C + Business → Rule Management
- D + Business → Engine Management

---

### Q3: (เฉพาะ DYNAMIC) เปลี่ยนอะไร? เปลี่ยนค่า หรือ เปลี่ยน Logic?

**ตัวเลือก:**
- A. เปลี่ยนค่า เช่น 100 → 200
- B. เปลี่ยนเงื่อนไข เช่น "ถ้า A>B → X" เปลี่ยนเป็น "ถ้า A>B และ C=D → X"
- C. เปลี่ยน Flow / สูตร / กระบวนการ

**Mapping:**
- A → Admin Panel (ลด Tag เป็น CONFIGURABLE)
- B → Rule Management
- C → Engine Management

---

### Q4: (เฉพาะ DYNAMIC) เงื่อนไขปัจจุบัน + อนาคต มีอะไรบ้าง?

**ใช้สำหรับ:**
- ตรวจ scope ของ Rule Engine
- หา hidden complexity ที่อาจทำให้ underestimate

**Action:**
- ใส่เป็น input ของ Rule Management implementation
- ถ้าเงื่อนไขซับซ้อนมาก → ยกระดับเป็น Engine Management

---

### Q5: (เฉพาะ WARNING) ตัดสินใจได้เมื่อไหร่?

**ตัวเลือก:**
- A. ภายในสัปดาห์นี้
- B. ภายในเดือนนี้
- C. หลัง release รอบนี้ (Phase 2)
- D. ยังไม่กำหนด

**Action:**
- A, B → Resolve ก่อน finalize BRD
- C → ใส่ Section 13 Phase 2 + Section 15 Open Questions
- D → ❌ ไม่ผ่าน Quality Gate (C18) — บังคับ stakeholder ระบุแผน

---

### Q6: (เฉพาะ Enhancement) Rule เดิมอยู่ในรูปแบบไหน?

**ตัวเลือก:**
- A. Hardcode ใน code
- B. Config File / DB Config Table
- C. Admin Panel
- D. ไม่รู้ — ต้องถาม Dev

**Action:**
- A → Phase 1 ต้อง migrate to Config Table + add seed
- B → Phase 1 อาจแค่ update value
- C → Phase 1 อาจแค่ update via Admin Panel (no code change)
- D → ใส่ Section 15 Open Questions + ขอ Dev Confirm

---

## วิเคราะห์คำตอบ → ระดับ

### Decision Matrix

| ใครเปลี่ยน | บ่อยแค่ไหน | เปลี่ยนอะไร | → ระดับ |
|---|---|---|---|
| IT/Dev | นานๆ ครั้ง | ค่า | **Config File** |
| Admin | นานๆ ครั้ง | ค่า | **Admin Panel** |
| Admin | เป็นระยะ | ค่า | **Admin Panel** |
| Business | เป็นระยะ | เงื่อนไข | **Rule Management** |
| Business | บ่อย / Real-time | เงื่อนไข | **Rule Management** |
| Business | บ่อย / Real-time | Flow / สูตร | **Engine Management** |

### Edge Cases ในการ Resolve

**Case 1: คำตอบขัดกัน**
- Stakeholder A บอก "IT เปลี่ยน" แต่ Stakeholder B บอก "Admin เปลี่ยน"
- → ใส่ Section 15 Open Questions + นัด Tech Lead + Business Owner หารือ

**Case 2: คำตอบไม่ชัด**
- "ไม่รู้สิ ตามแต่ละกรณี"
- → ใส่เป็น WARNING + ขอตัวอย่างเฉพาะ case

**Case 3: คำตอบ contradicts กับ Tag**
- ติด CONFIGURABLE แต่ Stakeholder บอก "เปลี่ยนเงื่อนไขด้วย"
- → ปรับ Tag เป็น DYNAMIC + Rule Management

---

## Pipeline Mode: Auto-Resolve

ในกรณีที่ Skill ทำงาน automated (ไม่มี Stakeholder สดให้ถาม) ใช้ inference logic:

### Inference Rules

**By Rule type:**
| Rule pattern | Default level |
|---|---|
| "≤ X", "≥ X", "= X" (เปรียบเทียบ) | Admin Panel |
| "ถ้า A แล้ว X, ถ้า B แล้ว Y" (multi-condition) | Rule Management |
| "สูตร", "calculation" | Rule Management |
| "Workflow", "approval flow", "step" | Engine Management |
| "Mapping table" (A → B) | Admin Panel |
| "Constant" (เช่น VAT 7%) | Config File / Admin Panel |
| "Lookup list" (e.g., country list) | Admin Panel |

**By Module type:**
| Module | Default style |
|---|---|
| Finance | strict — เน้น Config File + audit |
| HR | strict — เน้น Admin Panel + PII protection |
| Sales | flexible — Admin Panel |
| Operations | flexible — Rule Management |
| AI/Automation | dynamic — Rule Management |
| Manufacturing | dynamic — Engine Management |

**By Frequency hint จาก RIF:**
- ถ้า RIF มี "เปลี่ยนตามฤดูกาล / แคมเปญ" → Rule Management
- ถ้า RIF มี "ปีละครั้ง / นานๆ ครั้ง" → Admin Panel
- ถ้า RIF มี "fix ตามกฎหมาย" → Admin Panel + audit emphasis

---

## Output: Section 9.5 Format

```markdown
## 9.5 สรุประดับความยืดหยุ่น

### Resolved
| Rule ID | Tag | ใครเปลี่ยน | บ่อยแค่ไหน | ระดับ | เหตุผล |
|---|:---:|---|---|---|---|
| R02 | CONFIGURABLE | Admin | ปีละ 1-2 ครั้ง | Admin Panel | เปลี่ยนค่า simple |
| R04 | DYNAMIC | Sales Director | ตามแคมเปญ | Rule Management | เงื่อนไข tier |

### Pending (WARNING)
| Rule ID | ประเด็น | หารือกับ | กำหนดวันที่ | Phase |
|---|---|---|---|:---:|
| R05 | SLA Approval ใช้เวลาเท่าไหร่ | Sales Director | YYYY-MM-DD | 1 |

### Auto-Resolved (Pipeline Mode — ขอ user confirm)
| Rule ID | ระดับ (inferred) | เหตุผล (inference) | confirmed? |
|---|---|---|:---:|
| R02 | Admin Panel | Threshold + Module=Sales | ☐ |
| R04 | Rule Management | Multi-condition formula | ☐ |
```

---

## เมื่อ Skip ขั้นนี้ได้

- BRD Type = Bug Fix → ไม่มี Rule ใหม่
- BRD Type = Config/Chore → ตรวจว่าควรยกระดับเป็น Enhancement หรือไม่
- ไม่มี Rule ที่ติด CONFIGURABLE/DYNAMIC/WARNING เลย → ไม่มีงานให้ทำ
