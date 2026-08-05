# Philosophy Embed Guide

คู่มือการ embed Philosophy (COSO + Security + Health + Monitoring) เข้าไปใน BRD
ใช้ใน Step 6 ของ brd-generator-full

---

## หลักการ

Philosophy rules แบ่งเป็น 5 Pillars ตาม REQ-PHILO เดิม:

| Pillar | ไปอยู่ที่ Section ไหนของ BRD |
|---|---|
| Pillar 1: Flow + COSO | **Section 5 (User Journey)** — embed COSO column |
| Pillar 2: Brain + Scenarios | **Section 9 (Business Rules) + Section 10 (Edge Cases)** — embed Decision Points |
| Pillar 3: Guardrails | **Section 16 (Security & Compliance)** — preset + 78 controls |
| Pillar 4: Health Check | **Section 17 (Health Check)** — SLA + KPI + Threshold |
| Pillar 5: Monitoring | **Section 18 (Monitoring)** — Reports + Widgets |

---

## Embed Rule 1: COSO ใน Section 5 (User Journey)

### Mandatory Columns
ทุก step ใน User Journey table ต้องมี 4 columns:

| # | Step | **Maker** | **Checker** | **Approver** | **System** | Notes |
|---|---|---|---|---|---|---|

### Role Definitions
- **Maker**: คนสร้าง / กรอกข้อมูล (ผู้ลงมือ)
- **Checker**: คนตรวจ — *optional layer* — ไม่ทุก feature ต้องมี
- **Approver**: คนอนุมัติ — ต่างจาก Maker
- **System**: สิ่งที่ระบบทำอัตโนมัติ (validation, auto-fill, notification)

### SoD Rule (Mandatory)
ทุก approval step ต้องผ่าน:
```
Maker ≠ Approver ในข้อเดียวกัน
```

ถ้าผิด → ❌ Quality Gate PE02 ไม่ผ่าน

### Default Mapping (ถ้า RIF ไม่ระบุ)

| Module | Default Maker | Default Approver |
|---|---|---|
| Sales (Quote/SO) | Sales Officer | Sales Manager |
| Purchase (PR/PO) | Buyer | Purchasing Manager |
| Finance (Voucher/Payment) | Accountant | Finance Manager |
| HR (Hire/Leave) | HR Officer | HR Manager / Line Manager |
| Production (WO/MO) | Planner | Production Manager |
| Master Data | Admin | Senior Admin |

### DoA (Delegation of Authority) Default

ถ้าไม่ระบุ → ใส่ใน Open Questions:
- Manager DoA: ≤ 100,000 (default)
- Senior Manager DoA: ≤ 500,000
- Director DoA: ≤ 5,000,000
- CEO/Above: ไม่จำกัด

---

## Embed Rule 2: Decision Points ใน Section 9 + 10

### Decision Point Template (6 คำถาม)

ทุก critical decision ใน workflow ต้องตอบ:

```markdown
**Decision Point: [ชื่อ Decision]**

1. **เมื่อไหร่:** [trigger event]
2. **ใครตัดสิน:** [role + DoA]
3. **ตัดสินจากอะไร (criteria):**
   - Criteria 1: ...
   - Criteria 2: ...
4. **ทางเลือก (Options):**
   - A: [option A]
   - B: [option B]
   - C: [option C]
5. **ผลของแต่ละทาง:**
   - A → [outcome A]
   - B → [outcome B]
   - C → [outcome C]
6. **Audit Log:** [field/event ที่บันทึก]
```

### ใส่ที่ไหน?
- **Section 9 (Business Rules)**: ตัด Logic ที่เป็น auto-decision
- **Section 10 (Edge Cases)**: ตัด Logic ที่ต้องการคน decision

---

## Embed Rule 3: Security Preset ใน Section 16

### Preset Selection Logic

```
ถ้า REQ_PHILO มี preset → ใช้ตามนั้น
ถ้า user ระบุ → ใช้ตามนั้น
ถ้าไม่มี → infer จาก Module + Feature Type:
```

| Feature Type | Default Preset |
|---|---|
| Quote / PO / SO / Invoice | **P1** (Standard Transaction) — 12 controls |
| Approval Workflow / Multi-step | **P2** (Approval/Workflow) — 14 controls |
| Customer / Vendor / Item / Employee | **P3** (Master Data) — 10 controls |
| Payment / AR / AP | **P4** (Financial/Payment) — 16 controls |
| Report viewer / Dashboard | **P5** (Report/Dashboard) — 9 controls |
| Payroll / HR PII | **P6** (HR/PII Sensitive) — 15 controls |
| API integration | **P7** (Integration/API) — 11 controls |
| AI agent / Auto bot | **P8** (AI/Automation) — 10 controls |
| OT / Production / IoT | **P9** (OT/Manufacturing) — 13 controls |
| Audit trail / Compliance | **P10** (Audit/Compliance) — 12 controls |
| Critical (system core) | **P-MAX** — 78 controls |
| Internal tool only | **P-MIN** — 5 controls |

### Section 16 Structure

```markdown
## 16.1 Preset
**Preset เลือก:** [Pn] — [Name] ([N] controls)
**เหตุผล:** [why this preset]
**Overrides:** [ถ้ามีการเพิ่ม/ลด control]

## 16.2 Applicable Standards
| Standard | Applicable? | Reason |
|---|:---:|---|

## 16.3 Control Checklist
| Control ID | Standard | Control | Required | Implementation Notes |
|---|---|---|:---:|---|

## 16.4 Risk Statement (อย่างน้อย 3 risks)
| Risk ID | Risk | Likelihood | Impact | Mitigated by Control |
|---|---|---|---|---|
```

---

## Embed Rule 4: Health Check ใน Section 17

### Section Structure (5 sub-sections)

```markdown
## 17.1 SLA (Service Level Agreement)
ทุก step ที่มีเวลาควบคุม

| Step | SLA | Owner | Action when breached |
|---|---|---|---|

## 17.2 Control Points
Map controls จาก Section 16 ที่ทำงาน runtime

| Control ID | Where (เกิดที่ไหน) | When (เกิดเมื่อไหร่) | Result (ผลที่ต้องเกิด) |
|---|---|---|---|

## 17.3 KPI (อย่างน้อย 3 ตัว)

| KPI | Category | Target | Measure |
|---|---|---|---|

**Categories:**
- Volume (จำนวน)
- Quality (คุณภาพ — error rate, defect rate)
- Speed (ความเร็ว — cycle time, lead time)
- Compliance (การปฏิบัติตาม policy)
- Conversion (อัตราเปลี่ยน — Lead→Win, Quote→SO)

## 17.4 Threshold

| Metric | Min | Max | Action |
|---|---|---|---|

## 17.5 Throughput

- Capacity (เป้าหมาย)
- Baseline (ปัจจุบัน)
- Stress Point (จุดที่อาจมีปัญหา performance)
```

### KPI Default by Module

| Module | KPI Examples |
|---|---|
| Sales | Quote conversion rate, Win rate, Avg deal size |
| Finance | DSO (Days Sales Outstanding), Closing time, Reconciliation rate |
| HR | Time to hire, Turnover rate, Training completion |
| Production | OEE, Defect rate, Schedule adherence |

---

## Embed Rule 5: Monitoring ใน Section 18

### Section Structure (6 sub-sections)

```markdown
## 18.1 Reports Overview
4 types ที่ต้องมี:

| Report | Type | Frequency | Audience |
|---|---|---|---|
| ... | Performance | Daily | Manager |
| ... | Closing | Monthly | Director |
| ... | Anomaly | Real-time | Manager + Auditor |
| ... | Transaction | On-demand | Auditor |

## 18.2 Dashboard Widgets
อ้างอิง KPI/Threshold จาก 17.3 + 17.4

| Widget | Source KPI | Threshold (visual) |
|---|---|---|

## 18.3 Performance Report
- Daily breakdown
- Top/Bottom analysis
- Trend over time

## 18.4 Closing Report
- Period summary
- Year-over-year comparison
- Variance analysis

## 18.5 Anomaly Report
- Out-of-range transactions
- Suspicious patterns (e.g., approve < 1 min after submit)
- Override audit (e.g., approve over DoA)

## 18.6 Transaction Report
- Full audit trail per record
- State transition history
- All field changes
```

---

## Cross-Section Coverage Check (Mandatory)

หลัง embed ทุก section ต้องเช็ค:

### Coverage Matrix

| Source | Target | Check |
|---|---|---|
| Section 9 Business Rules (BC) | Section 10 Edge Cases / Scenarios | ทุก BC มี Edge Case cover |
| Section 16 Controls (runtime) | Section 17 Control Points (17.2) | ทุก runtime control มี Control Point |
| Section 17 SLA/KPI/Threshold | Section 18 Widget/Report | ทุก metric มี widget หรือ report |

### Verification Code

```python
# Pseudo-code สำหรับ verify cross-coverage
bcs = parse_section(BRD, 9, "business_conditions")
edges = parse_section(BRD, 10, "edge_cases")
for bc in bcs:
    if not any(edge.references == bc.id for edge in edges):
        flag_quality_gate("PE05: BC %s ไม่มี Edge Case cover" % bc.id)

controls = parse_section(BRD, 16, "control_checklist")
control_points = parse_section(BRD, 17, "control_points")
for c in controls:
    if c.runtime and not any(cp.control_id == c.id for cp in control_points):
        flag_quality_gate("PE05: Control %s runtime ไม่มี Control Point" % c.id)

metrics = parse_section(BRD, 17, ["sla", "kpi", "threshold"])
widgets = parse_section(BRD, 18, "widgets")
reports = parse_section(BRD, 18, "reports")
for m in metrics:
    if not (any(w.source == m.id for w in widgets) or any(r.includes == m.id for r in reports)):
        flag_quality_gate("PE05: Metric %s ไม่มี Widget/Report" % m.id)
```

---

## Bug Fix / Config Mini Mode

สำหรับ Bug Fix และ Config/Chore:
- **ตัด Section 17 + 18 ออก** (ไม่จำเป็น)
- **Section 16 ย่อ**: แค่ Risk Statement ถ้ามี (e.g., "Bug นี้กระทบ PDPA หรือไม่?")
- **COSO ใน Section 5**: ไม่ต้องเขียน (เพราะไม่มี Section 5)

---

## Summary: Philosophy Embed ทำให้ BRD แตกต่างจากเดิมยังไง

| Aspect | BRD เดิม | BRD + Philosophy Embed |
|---|---|---|
| Section 5 | User Journey | + COSO column ทุก step |
| Section 9 | Business Rules | + Decision Points (6 คำถาม) สำหรับ critical rules |
| Section 10 | Edge Cases | + Scenarios (Happy/Edge/Error) ผูกกับ BC |
| Section 16 | (ไม่มี) | + Security Preset + 78 Controls + Risks |
| Section 17 | (ไม่มี) | + SLA + KPI + Threshold + Throughput |
| Section 18 | (ไม่มี) | + Reports + Dashboard Widgets |

**ผลลัพธ์:** BRD เดียวจบ — Compliance ตรวจได้ + Dashboard ออกแบบได้ + Dev มี SLA ชัดเจน + Audit มี Trail
