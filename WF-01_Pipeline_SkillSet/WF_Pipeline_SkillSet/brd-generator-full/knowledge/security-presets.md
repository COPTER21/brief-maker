# Security Control Presets

ชุด preset สำเร็จรูปสำหรับ feature ประเภทต่างๆ — user สามารถเลือก preset แล้วปรับ checklist เพิ่มลดได้

ทุก control ID อ้างอิงจาก `security_policy_75_controls.md`

---

## Preset List (เลือก 1 หรือ Custom)

| Preset | ใช้กับ feature ประเภท | Total Controls |
|---|---|---|
| **P1: Standard Transaction** | ใบเสนอราคา, PO, SO, Invoice ทั่วไป | 12 |
| **P2: Approval/Workflow** | Approval, DoA, Multi-step workflow | 14 |
| **P3: Master Data** | Customer, Vendor, Item, Employee Master | 10 |
| **P4: Financial/Payment** | Payment, AR/AP, Receipt, Expense | 16 |
| **P5: Report/Dashboard** | Report viewer, Dashboard, Export | 9 |
| **P6: HR/PII Sensitive** | HR, Payroll, Employee data | 15 |
| **P7: Integration/API** | API Gateway, External integration | 11 |
| **P8: AI/Automation** | AI features, Auto-decision, Agent | 10 |
| **P9: OT/Manufacturing** | IoT, Production, Machine integration | 13 |
| **P10: Audit/Compliance** | Audit trail, Compliance report | 12 |
| **P-MAX: Maximum Security** | Critical features ที่ต้องครบทุกมาตรฐาน | 78 (ทั้งหมด) |
| **P-MIN: Minimal** | Internal tool, Low-risk feature | 5 |
| **Custom** | User เลือกเองทีละข้อ | — |

---

## P1: Standard Transaction

**ใช้กับ:** ใบเสนอราคา, ใบสั่งซื้อ, ใบสั่งขาย, ใบกำกับภาษี, ใบรับสินค้าทั่วไป

| Control ID | Name | เหตุผล |
|---|---|---|
| S01-01 | DoA Limit | ทุก transaction ต้องเช็คเพดานอำนาจอนุมัติ |
| S01-02 | Maker-Checker Workflow | คนสร้าง ≠ คนอนุมัติ |
| S01-04 | SoD Conflict Matrix | ป้องกันสิทธิ์ทับซ้อน |
| S01-06 | Tolerance Limits | ยอมรับความคลาดเคลื่อน |
| S01-07 | Immutable Master Data Log | Before/After log |
| S02-01 | Password Policy | พื้นฐาน |
| S02-03 | Session Management | Idle timeout |
| S04-05 | Standard Master Data Mapping | Naming convention |
| S04-06 | SLA & Escalation Rules | ค้างนานต้อง alert |
| S06-03 | Standardized Audit Content | Who/What/When/Where/Result |
| S11-02 | Ticket Enforcement | ใส่เลขตั๋วทุก action |
| S14-02 | Payload Schema Validation | Validate input |

---

## P2: Approval/Workflow

**ใช้กับ:** Approval flow, DoA matrix, Multi-step workflow, Escalation

P1 (12) + เพิ่ม:
| Control ID | Name | เหตุผล |
|---|---|---|
| S01-03 | Temporary Delegation | มอบหมายชั่วคราว |
| S03-02 | Policy Versioning | DoA เปลี่ยนต้องเก็บประวัติ |

---

## P3: Master Data

**ใช้กับ:** Customer Master, Vendor Master, Item Master, Employee Master

| Control ID | Name | เหตุผล |
|---|---|---|
| S01-04 | SoD Conflict Matrix | ป้องกันสิทธิ์ทับซ้อน |
| S01-07 | Immutable Master Data Log | สำคัญที่สุด — ห้ามลบ Before/After |
| S02-01 | Password Policy | พื้นฐาน |
| S02-04 | Data Masking/Obfuscation | ปิดบัง PII บน UI |
| S02-05 | Data Classification Tags | tag ความลับ |
| S03-02 | Policy Versioning | track การแก้ไข |
| S04-05 | Standard Master Data Mapping | Naming convention |
| S06-03 | Standardized Audit Content | Audit log ทุก action |
| S07-06 | PII Tagging & Masking | flag PII fields |
| S11-02 | Ticket Enforcement | ทุก add/edit/delete ต้องมี ticket |

---

## P4: Financial/Payment

**ใช้กับ:** Payment Voucher, AR Receipt, AP Payment, Expense, Reconciliation

| Control ID | Name | เหตุผล |
|---|---|---|
| S01-01 | DoA Limit | บังคับเพดานอนุมัติ |
| S01-02 | Maker-Checker Workflow | บังคับ |
| S01-04 | SoD Conflict Matrix | ห้าม จัดซื้อ+จ่ายเงิน |
| S01-05 | 3-Way Matching | PO/GR/Invoice |
| S01-06 | Tolerance Limits | ยอมรับ tolerance |
| S01-07 | Immutable Master Data Log | สำคัญ |
| S02-02 | MFA Enforcer | ธุรกรรมเงินต้อง MFA |
| S02-04 | Data Masking | บัญชีธนาคารต้อง mask |
| S04-06 | SLA & Escalation Rules | ค้างต้อง escalate |
| S06-01 | ABAC | บทบาท+เวลา+สถานที่ |
| S06-03 | Standardized Audit Content | audit ทุกธุรกรรม |
| S06-05 | Payload Encryption | encrypt field สำคัญ |
| S11-01 | UAR Scheduler | ทบทวนสิทธิ์ทุก 90 วัน |
| S11-02 | Ticket Enforcement | ทุก action ต้องมีเหตุ |
| S11-04 | Batch Reconciliation | กระทบยอด |
| S11-05 | Continuous Evidence Export | ส่ง audit vault |

---

## P5: Report/Dashboard

**ใช้กับ:** Report viewer, Dashboard, Data Export, Analytics page

| Control ID | Name | เหตุผล |
|---|---|---|
| S02-04 | Data Masking | mask PII บนหน้าจอ |
| S02-05 | Data Classification Tags | tag ก่อน export |
| S02-06 | Export Limits | จำกัดจำนวนแถวต่อวัน |
| S04-03 | Resource & Capacity Limits | จำกัด query load |
| S04-05 | Standard Master Data Mapping | ชื่อ field ตรงกัน |
| S06-01 | ABAC | สิทธิ์ดู report ตามบทบาท |
| S06-03 | Standardized Audit Content | log ทุกการดู/export |
| S07-06 | PII Tagging & Masking | flag PII column |
| S08-05 | Processing Transparency Log | report นี้ใช้ data อะไร |

---

## P6: HR/PII Sensitive

**ใช้กับ:** HR module, Payroll, Employee profile, Recruitment

| Control ID | Name |
|---|---|
| S01-04 | SoD Conflict Matrix |
| S01-07 | Immutable Master Data Log |
| S02-02 | MFA Enforcer |
| S02-04 | Data Masking/Obfuscation |
| S02-05 | Data Classification Tags |
| S02-06 | Export Limits |
| S06-01 | ABAC |
| S06-03 | Standardized Audit Content |
| S06-05 | Payload Encryption |
| S07-01 | Granular Consent |
| S07-02 | Consent Withdrawal |
| S07-03 | Automated Data Portability |
| S07-04 | Anonymization (RTBF) |
| S07-05 | Dynamic Data Purging |
| S07-06 | PII Tagging & Masking |

---

## P7: Integration/API

**ใช้กับ:** API Gateway, Webhook, External system integration

| Control ID | Name |
|---|---|
| S03-01 | SCRM Access Control |
| S03-03 | Zero Trust Access |
| S03-04 | Anomaly Detection |
| S03-05 | Emergency Kill Switch |
| S04-03 | Resource & Capacity Limits |
| S06-03 | Standardized Audit Content |
| S06-05 | Payload Encryption |
| S06-06 | Input Sanitization |
| S14-01 | Rate Limiting & Throttling |
| S14-02 | Payload Schema Validation |
| S14-03 | JWT Lifecycle |

---

## P8: AI/Automation

**ใช้กับ:** AI features, Chatbot, Auto-decision engine, RPA

| Control ID | Name |
|---|---|
| S03-04 | Anomaly Detection |
| S04-03 | Resource & Capacity Limits |
| S07-04 | Anonymization (RTBF) |
| S08-01 | PII Data Flow Tracker |
| S08-03 | Dynamic Pseudonymization |
| S08-05 | Processing Transparency Log |
| S08-06 | Automated DPIA Trigger |
| S13-01 | Output Sanitization (Human-in-loop) |
| S13-02 | Prompt Injection Protection |
| S13-03 | Agent Execution Limits |

---

## P9: OT/Manufacturing

**ใช้กับ:** IoT integration, Production module, Machine data

| Control ID | Name |
|---|---|
| S02-07 | Geolocation Block |
| S03-03 | Zero Trust Access |
| S05-03 | Secure Protocol Blocker |
| S06-01 | ABAC |
| S09-01 | DMZ Enforcer |
| S09-02 | API Conduit Whitelisting |
| S09-03 | Strict Read-Only |
| S09-04 | SL-Based Authentication |
| S09-05 | IT/OT Severance Switch |
| S10-01 | Purdue Level Routing |
| S10-02 | Data Polling Rate Limiter |
| S10-04 | Workstation Binding |
| S10-06 | Maintenance Window Scheduler |

---

## P10: Audit/Compliance

**ใช้กับ:** Audit trail viewer, Compliance dashboard, SOC report

| Control ID | Name |
|---|---|
| S01-07 | Immutable Master Data Log |
| S03-02 | Policy Versioning |
| S06-03 | Standardized Audit Content |
| S06-04 | Audit Failure Alert |
| S06-05 | Payload Encryption |
| S08-05 | Processing Transparency Log |
| S11-01 | UAR Scheduler |
| S11-02 | Ticket Enforcement |
| S11-03 | Automated Restore Test |
| S11-04 | Batch Reconciliation |
| S11-05 | Continuous Evidence Export |
| S12-01 | Module Tiering (RTO/RPO) |

---

## P-MAX: Maximum Security

ใช้ **ทุก control ใน 78 ข้อ** สำหรับ feature critical สุดๆ เช่น Treasury, Wire Transfer, Core Master Data ที่กระทบทั้งบริษัท

→ ดู `security_policy_75_controls.md` ครบทุก S01 ถึง S14

---

## P-MIN: Minimal

ใช้กับ internal tool, dev tool, low-risk feature ที่ไม่มี data flow ออกนอกระบบ

| Control ID | Name |
|---|---|
| S02-01 | Password Policy |
| S02-03 | Session Management |
| S06-03 | Standardized Audit Content |
| S11-02 | Ticket Enforcement |
| S14-02 | Payload Schema Validation |

---

## วิธีใช้ใน Skill

**Step:** Pillar 3 (Guardrails) ของ BRD

1. Skill ถาม: "Feature นี้ตรงกับ preset ไหน?" (แสดงตาราง P1-P10 + Custom)
2. User เลือก preset (เช่น P1) หรือ "Custom"
3. ถ้าเลือก preset → Skill auto-fill checklist + ถาม "ต้องการเพิ่ม/ลด control ไหนไหม?"
4. ถ้าเลือก Custom → Skill แสดง 78 controls ให้ tick ทีละข้อ
5. ผลลัพธ์: ตาราง §3.2 ใน BRD พร้อม Required/Optional ระบุชัด
