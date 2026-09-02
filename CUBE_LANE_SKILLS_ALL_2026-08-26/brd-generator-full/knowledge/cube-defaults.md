# CUBE Business Defaults

ค่า default สำหรับ Inference Logic เวลา RIF / user ไม่ระบุ
ใช้กับ brd-generator-full ใน Step 3 (Flexibility) + Step 6 (Philosophy Embed)

---

## D1: Security Preset Defaults (by Feature Type)

| Feature Type | Default Preset | เหตุผล |
|---|---|---|
| **Quotation (QT)** | P1 — Standard Transaction | Transaction document ทั่วไป |
| **Sales Order (SO)** | P1 — Standard Transaction | เหมือน QT |
| **Purchase Request (PR)** | P2 — Approval/Workflow | มี approval flow |
| **Purchase Order (PO)** | P2 — Approval/Workflow | มี approval + DoA |
| **Invoice** | P4 — Financial/Payment | เกี่ยวกับเงิน |
| **Receipt** | P4 — Financial/Payment | เกี่ยวกับเงิน |
| **Payment** | P4 — Financial/Payment | เกี่ยวกับเงิน |
| **Customer Master** | P3 — Master Data | Master data |
| **Vendor Master** | P3 — Master Data | Master data |
| **Product Master** | P3 — Master Data | Master data |
| **Employee Master** | P6 — HR/PII Sensitive | มี PII |
| **Payroll** | P6 — HR/PII Sensitive | salary + PII |
| **HR Report** | P6 — HR/PII Sensitive | sensitive data |
| **Dashboard / Report Viewer** | P5 — Report/Dashboard | อ่านอย่างเดียว |
| **Export Report** | P5 — Report/Dashboard | export data |
| **API Integration** | P7 — Integration/API | external |
| **Webhook Receiver** | P7 — Integration/API | external |
| **AI Bot / Agent** | P8 — AI/Automation | auto-decision |
| **Auto Approval** | P8 — AI/Automation | auto-decision |
| **Production Order** | P9 — OT/Manufacturing | OT integration |
| **IoT Data Collection** | P9 — OT/Manufacturing | machine data |
| **Audit Log Viewer** | P10 — Audit/Compliance | audit data |
| **Compliance Report** | P10 — Audit/Compliance | compliance |
| **Critical System Core** | P-MAX | maximum security |
| **Internal Tool (low-risk)** | P-MIN | minimum required |

---

## D2: Module Default Behavior

| Module | Style | Default Implementation |
|---|---|---|
| **Finance** | strict | Config File (เปลี่ยนยาก) + audit emphasis |
| **HR** | strict | Admin Panel + PII protection |
| **Sales** | flexible | Admin Panel for thresholds, Rule Management for discount |
| **Purchase** | strict | Admin Panel + DoA matrix |
| **Operations** | flexible | Rule Management for workflow rules |
| **Production** | dynamic | Engine Management for routing/scheduling |
| **AI/Automation** | dynamic | Rule Management + version control |
| **Manufacturing** | dynamic | Engine Management |
| **Logistics** | flexible | Rule Management for routing |

---

## D3: DoA (Delegation of Authority) Defaults

### Standard Approval Tiers (THB)

| Tier | Amount Range | Default Approver Role |
|---|---|---|
| Tier 1 | ≤ 50,000 | Line Manager / Section Head |
| Tier 2 | 50,001 - 200,000 | Department Manager |
| Tier 3 | 200,001 - 1,000,000 | Director / VP |
| Tier 4 | 1,000,001 - 5,000,000 | Senior Director / SVP |
| Tier 5 | > 5,000,000 | CEO + CFO (joint) |

### Module-Specific DoA

**Sales:**
- Discount ≤ 5% → Sales Officer
- Discount ≤ 15% → Sales Manager
- Discount ≤ 30% → Sales Director
- Discount > 30% → CEO

**Purchase:**
- PR ≤ 10,000 → Section Head
- PR ≤ 50,000 → Department Manager
- PR > 50,000 → standard tier

**Finance:**
- Payment ≤ 100,000 → Finance Manager
- Payment ≤ 1,000,000 → CFO
- Payment > 1,000,000 → CEO + CFO (joint)
- Write-off ≤ 10,000 → Finance Manager
- Write-off > 10,000 → CFO

**HR:**
- Salary adjustment ≤ 10% → HR Manager + Line Manager
- Salary adjustment > 10% → CEO

---

## D4: SLA Defaults (by Action Type)

### Document Approval SLAs

| Action | Default SLA | Owner | Action when breached |
|---|---|---|---|
| Approve PR (≤ Tier 2) | 1 business day | Approver | Notify + escalate at 2 days |
| Approve PO (≤ Tier 2) | 1 business day | Approver | Notify + escalate at 2 days |
| Approve PO (> Tier 2) | 2 business days | Approver | Notify + escalate at 3 days |
| Approve QT | 4 business hours | Sales Manager | Auto-notify + escalate |
| Approve Payment | 1 business day | Finance Manager | Notify CFO |
| Approve Leave (annual) | 1 business day | Line Manager | Auto-approve if not acted (configurable) |

### Document Processing SLAs

| Action | Default SLA | Owner |
|---|---|---|
| GR (Goods Receipt) | 1 business day after delivery | Warehouse |
| Invoice creation after delivery | 3 business days | AR Officer |
| Payment after invoice due | 0 days (on due date) | AP Officer |
| Period closing | 5 business days after month-end | Accountant |

### System SLAs

| Action | Default SLA | Action when breached |
|---|---|---|
| Email notification send | 5 minutes | Retry 3 times, then log |
| Webhook callback | 30 seconds | Retry with exponential backoff |
| Report generation | 30 seconds | Show progress; if > 1 min, send link via email |
| Search query response | 2 seconds | Add pagination/filters |

---

## D5: Threshold Defaults

### Sales Module

| Metric | Min | Max | Action |
|---|---|---|---|
| Customer Credit Limit Utilization | — | 80% | Warn at 80%, block at 100% |
| Quote Approval Time | — | 2 days | Alert manager |
| Quote Conversion Rate | 40% | — | Trigger sales review |
| Customer Discount | — | 30% (without approval) | Require Director approval |

### Finance Module

| Metric | Min | Max | Action |
|---|---|---|---|
| AR Aging | — | 60 days | Hold new sales / require deposit |
| AR Aging | — | 90 days | Block customer / write-off review |
| AP Aging | — | 30 days past due | Late payment alert to CFO |
| Cash Balance | 10% of monthly OPEX | — | Alert CFO |
| Reconciliation Mismatch | — | 0.1% | Investigate |

### HR Module

| Metric | Min | Max | Action |
|---|---|---|---|
| Time to Hire | — | 30 days | Escalate to HR Director |
| Probation Pass Rate | 80% | — | Review hiring criteria |
| Turnover Rate (monthly) | — | 5% | Alert CEO + HR Director |

### Operations Module

| Metric | Min | Max | Action |
|---|---|---|---|
| Inventory Stock-out | — | 5% of SKUs | Alert Purchasing + Sales |
| Order Fulfillment Time | — | 3 days | Escalate to Operations Manager |
| Return Rate | — | 3% | Quality review |

---

## D6: KPI Defaults (by Module)

### Sales
- Quote Conversion Rate (target: > 60%)
- Win Rate (target: > 30%)
- Average Deal Size (depends on industry)
- Sales Cycle Time (target: < 30 days)
- Customer Acquisition Cost (depends)

### Finance
- DSO — Days Sales Outstanding (target: < 45 days)
- DPO — Days Payable Outstanding (target: > 30 days)
- Closing Time (target: < 5 days)
- Reconciliation Rate (target: > 98%)
- Cash Conversion Cycle (target: < 60 days)

### HR
- Time to Hire (target: < 30 days)
- Turnover Rate (target: < 15% annual)
- Training Completion Rate (target: > 90%)
- Employee Satisfaction Score (target: > 4/5)
- Absenteeism Rate (target: < 3%)

### Production
- OEE — Overall Equipment Effectiveness (target: > 85%)
- Defect Rate (target: < 2%)
- Schedule Adherence (target: > 95%)
- Cycle Time (industry-specific)

### Operations
- Order Fulfillment Rate (target: > 95%)
- On-time Delivery (target: > 95%)
- Inventory Turnover (target: > 6x annual)
- Stock-out Rate (target: < 5%)

---

## D7: Document Numbering Defaults

### Format Pattern

| Document Type | Format | Example |
|---|---|---|
| Quotation | QT-YYYY-NNNNN | QT-2026-00001 |
| Sales Order | SO-YYYY-NNNNN | SO-2026-00001 |
| Purchase Request | PR-YYYY-NNNNN | PR-2026-00001 |
| Purchase Order | PO-YYYY-NNNNN | PO-2026-00001 |
| Goods Receipt | GR-YYYY-NNNNN | GR-2026-00001 |
| Invoice | INV-YYYY-NNNNN | INV-2026-00001 |
| Receipt | RC-YYYY-NNNNN | RC-2026-00001 |
| Voucher | VC-YYYY-NNNNN | VC-2026-00001 |
| Payment | PAY-YYYY-NNNNN | PAY-2026-00001 |
| Production Order | MO-YYYY-NNNNN | MO-2026-00001 |
| Goods Issue | GI-YYYY-NNNNN | GI-2026-00001 |

### Reset Logic

- **Default:** Reset เมื่อขึ้นปีใหม่ (Jan 1)
- **Alternative:** Reset เมื่อขึ้น fiscal year (e.g., Oct 1)
- **No reset:** ใช้ running number ต่อเนื่องไม่ reset (เลือกได้ใน config)

---

## D8: Audit Retention Defaults

| Audit Type | Retention Period | Notes |
|---|---|---|
| User login / logout | 1 year | Standard security |
| Document audit (CRUD) | 7 years | Thai tax law |
| Financial audit (transactions) | 10 years | Thai tax law |
| HR audit (personnel records) | Employment + 10 years | Labor law |
| System config changes | 7 years | Compliance |
| API access logs | 1 year | Security |
| Failed authentication | 2 years | Security forensics |

---

## D9: Notification Defaults

### Notification Channels (priority order)

1. **In-app notification** — primary, always on
2. **Email** — secondary, for important events
3. **LINE OA** — เน้น mobile + customer-facing
4. **SMS** — emergency / payment / OTP
5. **Push notification (mobile app)** — when user has app

### Notification Triggers (default events)

| Event | Channel | Recipient |
|---|---|---|
| Document submitted for approval | In-app + Email | Approver |
| Document approved/rejected | In-app + Email | Maker |
| SLA breach | In-app + Email | Owner + Manager |
| Threshold breach | In-app | Manager |
| Anomaly detected | In-app + Email | Manager + Auditor |
| Daily summary | Email | Department Head |
| Password expiry | Email | User |
| Account locked | Email + SMS | User + Admin |

---

## D10: Use these defaults if RIF doesn't specify

Pipeline Mode (Cowork Automation) ใช้ defaults เหล่านี้เมื่อ:
- RIF ไม่ระบุ
- REQ_PHILO ไม่ระบุ
- User ไม่ระบุใน intake

แต่ถ้าใช้ default แล้ว ต้อง:
1. ระบุใน Section 16-18 ว่า "[ใช้ default จาก cube-defaults D-XX]"
2. เพิ่มใน Section 15 Open Questions: "ขอ confirm ค่า default [X] ครับ"
3. AI Review Report: เตือนว่า "ใช้ default ค่า [X] — กรุณา confirm กับ stakeholder"

ใน Standalone Mode: ถาม user หรือ stakeholder ก่อนใช้ default
