---
name: doa-declaration
description: >
  Companion skill ฉีด context ของ DOA (Delegation of Authority — F-DLG-001 ใน Policy Center)
  เข้า pipeline ตอนทำ FRD และ HTML ของ feature ที่มีการอนุมัติ (PR/PO/SO/Quotation/ใบลา/OT/
  เบิกค่าใช้จ่าย/ปรับสต๊อก/งบประมาณ) แล้วออก DOA_BRIEF_[F-xxx].md = ใบประกาศที่คนเอาไปตั้งค่าจริง
  ที่หน้า DOA กลางได้ทันที — feature ประกาศเท่านั้น ห้าม hardcode สายอนุมัติ
  ★ หัวใจ: ถามผู้ prompt ว่า feature นี้มีวงเงินหรือไม่ (PR/PO มี · ใบลา/OT ไม่มี) เพื่อเตรียม matrix
  ให้ไป set ที่ DOA กลางได้ถูกแบบ
  ใช้เมื่อ user พูดถึง "doa-declaration", "ทำ DOA brief", "ผูก DOA", "ประกาศ DOA",
  "DOA setting ของ feature", "สายอนุมัติของ PR/PO", "ตั้ง approval chain", "มีวงเงินอนุมัติ",
  "threshold อนุมัติ", "เตรียม DOA entry", "wire DOA" — และใช้อัตโนมัติทุกครั้งที่รัน
  frd-generator-v6 หรือ html-generator-v7 กับ feature ที่มี action อนุมัติ/เซ็น แม้ไม่เรียกชื่อ skill
  ★ ไม่ใช่ standalone — เป็น companion (Sync Read) ★ ไม่ทำ module config เช่น Purchase Config
---

# DOA Declaration v1.0 — Companion Skill

> **Positioning:** DOA feature (F-DLG-001) = **ทะเบียนกลาง** ของสายอนุมัติทั้งระบบ
> feature ใหม่ (PR/PO/SO/…) = **ผู้ประกาศ** ว่า "ฉันมีการอนุมัติ หน้าตาแบบนี้"
> skill นี้ = **ล่าม** ที่ทำให้ FRD/HTML พูดภาษาเดียวกับ DOA ตั้งแต่วันแรก

---

## 🎯 ปัญหาที่ skill นี้แก้

DOA เกิดก่อน feature อื่นทั้งหมด → ตอนทำ FRD/HTML ของ PR/PO/SO ตัว generator **ไม่รู้ว่ามี DOA อยู่**
ได้แค่ `// TODO: DOA engine` ลอย ๆ → กลายเป็นหนี้ที่ต้องไล่ผูกทีหลังทีละ feature

skill นี้ทำให้:
1. **ตอน FRD** — รู้ตั้งแต่ต้นว่ามี approval action อะไรบ้าง เขียนลง FRD ให้ถูกชั้น + ถูก field
2. **ตอน HTML** — gen ปุ่ม/สถานะ/timeline อนุมัติ + hook ไป My Approval โดยอ่าน chain จาก mock DOA entry
3. **ออก DOA_BRIEF** — ใบที่คนเอาไปกรอกที่ DOA กลางได้ตรงช่อง ไม่ต้องตีความใหม่

---

## 📍 Position in Pipeline

```
LANE_BRIEF / RIF
      ↓
frd-generator-v6  ←──── ★ doa-declaration (Sync Read: §DOA Contract + §FRD Injection)
      ↓                        │
FRD Pack                       ├─→ DOA_BRIEF_[F-xxx].md   ← output เดียวของ skill นี้
      ↓                        │
html-generator-v7 ←──── ★ doa-declaration (Sync Read: §HTML Injection)
      ↓
HTML prototype
      ↓
[คน] zip รวมเป็น dev package (DOA_BRIEF ไปด้วยในก้อนเดียว)
      ↓
[คน] เอา DOA_BRIEF ไปตั้งค่าจริงที่หน้า DOA กลาง → wire_status: pending → wired
```

**ขอบเขตชัด ๆ**
- ✅ ทำ: ประกาศว่า feature นี้มีอนุมัติแบบไหน + เตรียม matrix ให้ไปกรอก
- ❌ ไม่ทำ: ตั้งค่า DOA จริง (คนทำที่หน้า DOA กลาง) · ไม่ทำ module config (Purchase Config ฯลฯ) · ไม่แก้ตัว DOA feature เอง

---

## 🚦 Trigger Rule (เมื่อไหร่ต้องรัน)

รันอัตโนมัติเมื่อ feature ที่กำลังทำ **มีอย่างน้อย 1 ข้อ**:

| สัญญาณ | ตัวอย่าง |
|---|---|
| มี action คำว่า อนุมัติ / เซ็น / ส่งอนุมัติ / approve / sign / submit for approval | PR ส่งอนุมัติ |
| มี status `pending_approval` / `รออนุมัติ` / `approved` / `rejected` | PO |
| เป็นเอกสารธุรกรรมที่ออก PDF แล้วมีช่องลายเซ็น | QT / SO / INV |
| มี field `approver_*` / `approved_by` / `approval_chain` ใน schema | ทุกตัว |
| feature อยู่ใน `MOCK_FEATURES` ของ DOA v23 อยู่แล้ว | ดู `references/doa-contract.md` |

**ถ้าไม่เข้าเลย → ไม่ต้องรัน** และ**ห้าม**ยัด DOA placeholder เข้า feature ที่ไม่มีอนุมัติ (เป็น noise)

---

## 📥 Input

| # | Input | จำเป็น | ใช้ทำอะไร |
|---|---|---|---|
| 1 | Feature identity (id / ชื่อ / module) | **required** | key ของ DOA entry |
| 2 | FRD Pack หรือ LANE_BRIEF หรือ HTML | **required** | หา approval action ทุกตัว |
| 3 | คำตอบจาก Q1–Q4 (ดู §Interview) | **required** | สร้าง matrix |
| 4 | `references/doa-contract.md` | **required** | master ที่ห้ามแต่งเอง |

**Pre-check:** ถ้าหา approval action ไม่เจอเลยแม้แต่ตัวเดียว → ถามยืนยันก่อน ห้ามเดา

---

## 🎤 Interview — 4 คำถาม (ถามครั้งเดียวจบ)

**หลักการ:** เสนอ default ที่ infer มาแล้วเสมอ ให้ผู้ prompt แค่ยืนยันหรือแก้ — ห้ามถามลอย ๆ แบบไม่มีคำตอบตั้งต้น
ถ้าผู้ prompt ตอบมาแล้วในบรีฟ/แชท → **ข้ามคำถามนั้น** ไม่ต้องถามซ้ำ

### Q1 — กี่สายอนุมัติ?
> feature นี้มีการอนุมัติกี่สาย?
> - **1 สาย** → ใช้ `matrix` เดียว (ปกติ เช่น PR/PO/SO)
> - **หลายสาย** → ใช้ `actions[]` (เช่น Budget: เปิดปีงบ / ปิดปีงบ / ปิดงวด แยกสายกัน)

infer: นับ action ที่เข้าเกณฑ์ §Trigger Rule ใน FRD/HTML

### Q2 — ★ มีวงเงินไหม? (คำถามหลักของ skill นี้)
> การอนุมัติของ feature นี้ **เปลี่ยนตามจำนวนเงิน**หรือไม่?
> - **มีวงเงิน** → ยิ่งเงินเยอะยิ่งต้องเซ็นหลายชั้น (PR / PO / SO / PV / เบิกค่าใช้จ่าย / ปรับสต๊อก)
> - **ไม่มีวงเงิน** → ใครก็เซ็นชั้นเดียวจบไม่ว่าเท่าไหร่ (ใบลา / OT / โอนย้ายสินค้า / WHT / offboarding)

infer:
- feature อยู่ใน `MOCK_FEATURES` แล้ว → **ใช้ค่า `amount` ตามนั้น ห้ามเดาใหม่**
- ไม่อยู่ → มี field จำนวนเงิน/ยอดรวม/total ใน schema = เสนอ `มีวงเงิน` · ไม่มี = เสนอ `ไม่มีวงเงิน`
- ⚠️ ระวัง: HR ส่วนใหญ่ไม่มีวงเงิน **แต่ "เบิกค่าใช้จ่าย" มี** — อย่าตัดสินจาก module

**ถ้ามีวงเงิน → ถามต่อ: จุดตัดกี่ช่วง?**
เสนอ default ตาม `buildDefaultMatrix()` ของ DOA v23 (ผู้ prompt แก้ได้):

| ช่วง | amount_from | amount_to | ผู้เซ็น |
|---|---|---|---|
| 1 | 0 | 100,000 | ผู้จัดการของ module นั้น |
| 2 | 100,001 | 1,000,000 | + BU Head (`role-mgr-bu`) |
| 3 | 1,000,001 | *(ไม่จำกัด)* | + CFO (`role-cfo`) |

**ถ้าไม่มีวงเงิน** → 1 ชุดเดียว `amount_from: 0, amount_to: null` ผู้เซ็นชั้นเดียว = ผู้จัดการของ module

### Q3 — แยกตามแผนกผู้ขอไหม?
> - **merged** (default) — ทุกแผนกใช้กฎชุดเดียวกัน
> - **per_dept** — แต่ละแผนกมีสายของตัวเอง (เช่น Budget Request)

infer: default `merged` เสมอ เว้นแต่ FRD ระบุชัดว่าแยกแผนก

### Q4 — scope ไหน?
> - `document_sign` (default) — เซ็นแล้วขึ้นช่องลายเซ็นใน PDF (PR/PO/SO/QT/INV/…)
> - `budget_approve` — อนุมัติงบ
> - `policy_approve` — อนุมัติเชิงนโยบาย/สิทธิ์ (credit limit, discount override)

infer: เป็นเอกสารที่พิมพ์ออกมาได้ → `document_sign`

---

## 📤 Output — `DOA_BRIEF_[F-xxx].md`

ไฟล์เดียวต่อ feature · ใช้ template ที่ `references/brief-template.md`
ต้องมีครบ 7 ส่วน:

| § | ส่วน | เนื้อหา |
|---|---|---|
| 1 | Identity | feature_id, name, module, platform, scope |
| 2 | Approval Actions | ทุก action ที่ต้องอนุมัติ + trigger + ผลลัพธ์เมื่อ approve/reject |
| 3 | **Matrix ที่จะไปตั้งค่า** | ตาราง set: `amount_from / amount_to / departments / chainMode / steps[roles]` — **กรอกลงหน้า DOA กลางได้ตรงช่อง** |
| 4 | Field Contract สำหรับ FRD | field ที่ต้องมีใน entity + ชนิด + nullable |
| 5 | UI Contract สำหรับ HTML | ปุ่ม/สถานะ/timeline/My Approval hook |
| 6 | Wire Checklist | รายการที่ dev ต้องทำจน `wire_status: pending → wired` |
| 7 | Open Questions | ที่ผู้ prompt ยังไม่เคาะ (ระบุชัดว่าใครต้องตอบ) |

**กฎการเขียน**
- ทุก role ต้องอ้าง `role-*` id จาก master เท่านั้น — ห้ามเขียนชื่อตำแหน่งลอย ๆ
- ทุกตัวเลขวงเงินต้องมีหน่วยชัด (บาท) และ `amount_to: null` = ไม่จำกัด
- ถ้าเป็นค่า default ที่ skill เสนอเอง (ยังไม่ได้ยืนยัน) → ติด `[DEFAULT — รอยืนยัน]`

---

## 🔌 FRD Injection (Sync Read โดย frd-generator-v6)

เมื่อ frd-generator-v6 ทำ feature ที่เข้าเกณฑ์ ให้บังคับสิ่งนี้:

**1. Entity ต้องมี field ครบ (ห้ามขาด)**
```
approval_required     bool      -- จาก DOA entry, ไม่ใช่ค่าคงที่ในตาราง
approval_status       enum      -- draft | pending_approval | approved | rejected | cancelled
doa_entry_ref         string    -- FK ไปทะเบียน DOA (nullable ตอน Phase 1)
approver_role         string    -- role ที่ต้องเซ็นในขั้นปัจจุบัน (resolve จาก DOA)
approved_by           string    -- user id ที่เซ็นจริง
approval_chain        jsonb     -- snapshot ของสายที่ resolve ตอนส่งอนุมัติ (append-only)
approved_at           timestamp
```

**2. ข้อห้ามเด็ดขาด (Iron Rule)**
- ❌ ห้าม hardcode ลำดับผู้อนุมัติใน FRD/BR ของ feature
- ❌ ห้ามเขียน business rule แบบ "ถ้าเกิน 100,000 ให้ CFO เซ็น" ลงใน feature — **นั่นเป็นข้อมูลใน DOA ไม่ใช่ logic ใน feature**
- ✅ เขียนแทนว่า: *"ระบบ resolve สายอนุมัติจาก DOA entry ของ feature นี้ ณ เวลาที่กดส่งอนุมัติ แล้ว snapshot ลง `approval_chain`"*
- ✅ ทุกจุดที่ยังต่อ engine ไม่ได้ → คอมเมนต์ `// TODO: DOA engine` (audit.sh ยกเว้น Rule #24 ให้แล้ว)

**3. Business Rule ที่ต้องมีเสมอ**
| BR | เนื้อหา |
|---|---|
| BR-DOA-01 | ส่งอนุมัติได้เฉพาะสถานะ `draft` |
| BR-DOA-02 | สายอนุมัติ resolve ตอนส่ง แล้ว **freeze** — แก้ DOA ทีหลังไม่กระทบใบที่ส่งไปแล้ว |
| BR-DOA-03 | reject → กลับ `draft` แก้ได้ · ประวัติการ reject เก็บ append-only |
| BR-DOA-04 | ผู้ขอเซ็นอนุมัติใบตัวเองไม่ได้ (segregation of duty) |
| BR-DOA-05 | แก้ยอดเงินหลังส่งอนุมัติ → ต้อง re-resolve สาย (ถ้า feature มีวงเงิน) |

**4. §ที่ต้องเพิ่มใน FRD Pack** — `05_RULES.md` เพิ่มหัวข้อ "การอนุมัติ (DOA)" ชี้ไปที่ DOA_BRIEF ไฟล์นี้

---

## 🎨 HTML Injection (Sync Read โดย html-generator-v7)

**1. ต้องมีบนหน้าจอ**
| ส่วน | รายละเอียด |
|---|---|
| ปุ่ม **ส่งอนุมัติ** | แสดงเฉพาะ status `draft` · disabled ถ้ายังกรอกไม่ครบ |
| Badge สถานะ | draft / รออนุมัติ / อนุมัติแล้ว / ไม่อนุมัติ — ใช้สีตาม CI Warm Light |
| **Approval Timeline** | ไล่ทีละขั้น: role → ชื่อผู้เซ็น → เวลา → สถานะ (รอ/ผ่าน/ตีกลับ) |
| ปุ่ม **อนุมัติ / ไม่อนุมัติ** | แสดงเฉพาะผู้ที่มีสิทธิ์ในขั้นปัจจุบัน · ไม่อนุมัติต้องบังคับใส่เหตุผล |
| Hook **My Approval** | ใบที่ `pending_approval` ต้องโผล่ในกล่อง My Approval |

**2. ข้อห้าม**
- ❌ ห้ามเขียน `const APPROVAL_CHAIN = ['หัวหน้า','ผู้จัดการ']` ในไฟล์ feature
- ✅ ให้ประกาศ mock ที่ resolve จากรูป DOA entry แทน:
```js
// TODO: DOA engine — resolve จาก DOA entry ของ feature นี้ (ดู DOA_BRIEF_[F-xxx].md)
const MOCK_DOA_RESOLVED = { doa_entry_ref: 'DOA-0xx', chainMode: 'sequential',
  steps: [{ roles: ['role-mgr-pur'] }, { roles: ['role-mgr-bu'] }] };
```
- ถ้า feature **มีวงเงิน** → mock ต้องมีอย่างน้อย 2 tier เพื่อให้เห็นว่าสายเปลี่ยนตามเงินจริง

**3. Iron rules เดิมยังบังคับครบ** — z-index, min-height, numeric input `type="text" inputmode="numeric"`, ปุ่มลบส่ง index ไม่ส่ง string

---

## ✅ Quality Gate (ก่อนส่ง DOA_BRIEF)

| # | เช็ค | FAIL ถ้า |
|---|---|---|
| G1 | ทุก role เป็น `role-*` ที่มีใน master | เจอชื่อตำแหน่งลอย ๆ |
| G2 | ทุก set มี `amount_from` และ `amount_to` ครบ | ขาดช่อง |
| G3 | ถ้ามีวงเงิน — ช่วงต้องต่อเนื่องไม่ทับ ไม่มีรู | 100,000 → 100,000 (ทับ) หรือ 100,000 → 200,000 (มีรู) |
| G4 | set สุดท้ายต้อง `amount_to: null` | ปิดปลาย = ใบเกินเพดานไม่มีคนเซ็น |
| G5 | `approval_scope` เป็น 1 ใน 3 ค่าที่มีจริง | ค่าอื่น |
| G6 | ค่าที่ยังไม่ยืนยันติด `[DEFAULT — รอยืนยัน]` ครบ | เนียนใส่เป็นค่าจริง |
| G7 | ไม่มีสายอนุมัติ hardcode หลุดเข้า FRD/HTML | เจอ array ชื่อ role ในไฟล์ feature |

**FAIL ข้อไหนก็ตาม → แก้ก่อน ห้ามส่ง**

---

## 📚 References

| ไฟล์ | เนื้อหา |
|---|---|
| `references/doa-contract.md` | Master ที่ห้ามแต่งเอง — roles 14 ตัว, departments 8, scope 3, module 9, record schema, feature+amount catalog |
| `references/brief-template.md` | Template ของ DOA_BRIEF 7 ส่วน |

**อ่าน reference ก่อนเขียนเสมอ** — ห้ามตอบจากความจำเรื่อง role id / จุดตัดวงเงิน / ชื่อ scope

---

## 🚫 ห้ามทำ

1. ห้ามตั้งค่า DOA จริงแทนคน — skill นี้ออก**ใบประกาศ**เท่านั้น
2. ห้ามแก้ไฟล์ `doa-management-v*.html` — นั่นเป็นงานของ feature DOA เอง
3. ห้ามทำ module config (Purchase Config ฯลฯ) — คนละ skill
4. ห้ามยัด DOA เข้า feature ที่ไม่มีการอนุมัติ
5. ห้ามคิด strategy code (`flat`/`sequential`/`by_amount`) ขึ้นมาเป็นคำตอบ — **record จริงเก็บเป็น `matrix` ไม่ใช่ strategy** (strategy registry เป็นแค่ plugin catalog view)

---

## 📌 หลังส่ง DOA_BRIEF — งานที่คนต้องทำต่อ

- [ ] เอา DOA_BRIEF ไปตั้งค่า entry จริงที่หน้า DOA กลาง
- [ ] dev wire hook ที่ feature → toggle `wire_status: pending → wired`
- [ ] เช็คว่าใบโผล่ใน My Approval จริง
- [ ] อัพเดต `FEATURE_REGISTRY.md` (แก้จากหน้า project — read-only ในแชท)
- [ ] แจ้งพี่เบิร์ดอัพ Google Sheet H·F·Q
- [ ] แจ้ง Architect ถ้ามี ENG candidate ใหม่
