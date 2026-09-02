---
file_id: KB-01-01
title: VS / VC / Path / CL / SOP / SOW Hierarchy
version: 1.0.0
last_updated: 2026-05-27
status: stable
---

# VS / VC / Path / CL / SOP / SOW — Business Process Hierarchy

## Quick Reference (TL;DR)

6 layers + 1 separate concern:

```
VS    Value Stream      "ระบบ business 1 ตัว"           เช่น P2P
 └─ VC    Value Chain   "happy path หลัก, decide ก่อน start"  เช่น Postpay / Prepay / Deposit
     └─ Path            "event ระหว่างทาง, เจอแล้วถึงรู้"   เช่น Happy / Short / Over / QC-Fail
         └─ CL          "Chain Link — ข้ามแผนก"
             └─ SOP     "Standard Operating Procedure — ในแผนก"
                 └─ SOW "Statement of Work — task 1 คน 1 deliverable (A→B→C)"

Edge Case (system-level: timeout, double-submit) → ไป FRD §Error Handling (NOT in Bible)
```

---

## 1. Definitions

### VS · Value Stream
**ระบบ business 1 ตัว** ที่มี trigger + outcome ชัดเจน  
- ตัวอย่าง: P2P (Procure-to-Pay), O2C (Order-to-Cash), H2R (Hire-to-Retire)
- 1 VS อาจประกอบด้วยหลาย VC

### VC · Value Chain
**Happy path หลักของกระบวนการ** ที่ตัดสินใจ **ก่อน start**
- เลือกจาก vendor terms / contract / business decision  
- ตัวอย่างใน P2P: **Full Postpay**, **Full Prepay**, **Deposit**, **Installment**, **Partial Delivery**, **Credit N วัน**, **Direct Payment**
- VC ถูก set ตอน trigger event แรก (เช่น PO Create)

### Path · Process Path
**เส้นทางย่อยภายใน VC เดียวกัน** ที่ขึ้นกับ **event ระหว่างทำ**
- เห็นของจริงแล้วถึงรู้
- ตัวอย่างใน P2P-Postpay: Happy / Short / Over / QC-Partial-Fail / QC-Full-Fail / Backorder / RTV-Replace / RTV-Refund

### CL · Chain Link
**งานข้ามแผนก** — phase ใหญ่ที่มี deliverable สำคัญ
- ตัวอย่าง P2P: CL1 Requisition, CL2 Procurement, CL3 Receiving+Payment

### SOP · Standard Operating Procedure
**งานภายในแผนก** — 1 actor group, 1 phase
- ตัวอย่าง: SOP "PR Approval" (HOD ภายในแผนก)

### SOW · Statement of Work
**Task ระดับคนเดียว 1 deliverable** — มี zigzag pattern
- Structure: A (Trigger "รอ...") → B (Task กริยา+object) → C (Result "รอ..."/"เสร็จสิ้น...")
- Chain rule: `C ของ SOW N = A ของ SOW N+1` (exact match)

---

## 2. Decision Rules (ใช้ตัดสินว่าควรเป็น layer ไหน)

| คำถาม | คำตอบ → layer |
|---|---|
| "เลือกตอนเซ็นสัญญา / setup vendor / config ก่อน start" | **VC** |
| "เห็นสถานการณ์จริงระหว่างทำแล้วถึงรู้" | **Path** |
| "งานข้ามฝ่าย หลายคนทำต่อกัน" | **CL** |
| "งานในแผนกเดียว 1 phase" | **SOP** |
| "task 1 คน 1 deliverable มี trigger→action→result" | **SOW** |
| "ระบบล่ม / network fail / validation / browser back" | **FRD Edge Case** (ไม่ใช่ business) |

---

## 3. Key Distinction — VC vs Path

| | VC | Path |
|---|---|---|
| **เมื่อตัดสิน** | ก่อน start | ระหว่างทำ |
| **อะไรกำหนด** | vendor terms / business decision | event / observed reality |
| **เปลี่ยนได้ไหมระหว่างทาง** | ไม่ (lock ตอน PO create) | ใช่ — เกิดเมื่อเจอ event |
| **ตัวอย่าง P2P** | Postpay vs Prepay vs Deposit | Happy vs Short vs QC-Fail |

→ **VC = "เราจะวิ่งเส้นไหน?"**  
→ **Path = "วิ่งไปแล้วเจออะไร?"**

---

## 4. Where each layer lives in artifacts

| layer | อยู่ใน document ไหน |
|---|---|
| VS | VS Charter, VS Bible (§1 Identity) |
| VC | VS Bible (§2 VC Catalog) |
| Path | VS Bible (§3 Path Catalog) |
| CL | VS Bible (§4) + per-feature BRD §Workflow |
| SOP | VS Bible (§4) + per-feature BRD §Workflow |
| SOW | VS Bible (§5 SOW Zigzag) + Brief Pack `04_Test_Scenarios.md` |
| Edge Case | FRD §Error Handling / §Non-Functional Requirements |

---

## 5. Common Confusion

### ❌ "Scenario" ≠ "Path"
- **Scenario** = test scenario (QA term) — combination of inputs to verify outcome
- **Path** = business process path — actual workflow branch

→ ใช้ **"Path"** ใน Bible/BRD, ใช้ **"Scenario"** เฉพาะใน Test docs

### ❌ "Channel" ≠ "VC"
- **Channel** = old term เคยใช้ใน v1 — ใช้แทน VC ได้ในบริบทเดิม
- **VC** = current canonical term

### ❌ Edge Case ไม่ใช่ Path
- **Path** = business event ที่เกิดได้ตามธรรมชาติของกระบวนการ (รับไม่ครบ, QC fail)
- **Edge Case** = technical/system anomaly (timeout, double-submit, race condition)

---

## 6. Outcome States (Path จบยังไงได้)

ทุก Path ต้องจบที่ 1 ใน outcome states:

| state | meaning |
|---|---|
| `Closed-Complete` | จบสมบูรณ์ ตรง PO ทุกอย่าง |
| `Closed-PartialFulfill` | จบแต่ไม่ครบ (รับขาด + close) |
| `Closed-Cancelled` | ยกเลิกก่อนจบ |
| `Closed-Replaced` | จบโดย vendor ส่งของใหม่ |
| `Closed-Returned` | จบโดย return (RTV) |
| `Disputed` | conflict ติด legal (ขึ้นกับ VS ว่าใส่หรือไม่) |

---

## 7. SOW Zigzag — A→B→C Pattern

```
SOW 1:  A1 (รอ...) → B1 (task) → C1 (รอ...)
                                      ║ exact match
SOW 2:  A2 (= C1)  → B2 (task) → C2 (รอ...)
                                      ║
SOW 3:  A3 (= C2)  → B3 (task) → C3 (เสร็จสิ้น...)  ← = vs.outcome
```

### Iron rules (5)
1. **A · Trigger** ขึ้นต้น `"รอ..."` เสมอ (ยกเว้น SOW แรกใช้ `vs.trigger`)
2. **B · Task** = กริยา + object ชัดเจน (ห้าม "ดำเนินการ...")
3. **C · Result** ขึ้นต้น `"รอ..."` หรือ `"เสร็จสิ้น..."`
4. **Chain**: `C ของ SOW N = A ของ SOW N+1` (copy-paste ตรงทุกอักษร)
5. **ปิด chain**: `C ของ SOW สุดท้าย = vs.outcome`

### 12 columns ต่อ SOW
`cl` · `cl_name` · `sop` · `sop_name` · `sow` · `sow_name` · `A` · `B` · `C` · `actor` · `target` · `sla` · `dod`

---

## Change Log

- **1.0.0** (2026-05-27): Initial — 6-layer hierarchy defined; VC vs Path clarified; outcome states + zigzag rules included
