# Health & Monitoring Patterns

Patterns สำหรับ Section 17 (Health Check) + Section 18 (Monitoring)
ใช้ใน Step 6 ของ brd-generator-full

---

## Section 17: Health Check Patterns

### 17.1 SLA Patterns

**Pattern A: Approval Flow SLA**
```
| Step | SLA | Owner | Action when breached |
|---|---|---|---|
| Submit → First approver | 4 hours (business hours) | First approver | Notify approver |
| First approver → Decision | 1 day | First approver | Escalate to manager |
| Second approver → Decision | 1 day | Second approver | Escalate to director |
```

**Pattern B: Document Processing SLA**
```
| Step | SLA | Owner | Action when breached |
|---|---|---|---|
| Create → Submit | No SLA (user pace) | — | — |
| Submit → Review | 4 hours | Reviewer | Auto-notify |
| Review → Finalize | 1 day | Reviewer | Escalate |
```

**Pattern C: External Integration SLA**
```
| Step | SLA | Owner | Action when breached |
|---|---|---|---|
| Send to External | 5 sec | System | Retry 3x |
| External Response | 30 sec | External API | Mark as failed, queue retry |
| Reconciliation | Daily 23:59 | System | Alert finance |
```

---

### 17.2 Control Points Patterns

**Pattern: Map Section 16 controls to runtime checks**

```
| Control ID | Where (เกิดที่ไหน) | When (เกิดเมื่อไหร่) | Result |
|---|---|---|---|
| C-01 (Access Control) | Every API call | Pre-action | Block if no permission |
| C-05 (Audit Log) | Every data change | Post-action | Insert audit row |
| C-08 (SoD) | Submit/Approve action | Pre-decision | Block if Maker = Approver |
| C-12 (Data Encryption) | Sensitive field write | Pre-storage | Encrypt at rest |
```

---

### 17.3 KPI Patterns by Module

#### Sales Module
| KPI | Category | Formula | Target |
|---|---|---|---|
| Quote Conversion Rate | Conversion | converted_quotes / total_quotes | > 60% |
| Win Rate | Conversion | won_deals / closed_deals | > 30% |
| Average Deal Size | Volume | SUM(deal_amount) / count | depends |
| Sales Cycle Time | Speed | AVG(closed_date - created_date) | < 30 days |
| Quote Approval Time | Speed | AVG(approved_at - submitted_at) | < 1 day |

#### Finance Module
| KPI | Category | Formula | Target |
|---|---|---|---|
| DSO (Days Sales Outstanding) | Speed | AR / Total Sales × 365 | < 45 days |
| Closing Time | Speed | days to close month | < 5 days |
| Reconciliation Rate | Quality | reconciled / total | > 98% |
| AP Aging | Compliance | overdue / total AP | < 5% |
| Tax Filing Accuracy | Quality | correct_filings / total | 100% |

#### HR Module
| KPI | Category | Formula | Target |
|---|---|---|---|
| Time to Hire | Speed | AVG(hire_date - request_date) | < 30 days |
| Turnover Rate | Quality | resigned / avg_headcount | < 15% (annual) |
| Training Completion | Compliance | completed / assigned | > 90% |
| Employee Satisfaction | Quality | survey score | > 4/5 |

#### Production Module
| KPI | Category | Formula | Target |
|---|---|---|---|
| OEE | Quality | Availability × Performance × Quality | > 85% |
| Defect Rate | Quality | defects / total_produced | < 2% |
| Schedule Adherence | Compliance | on_time / total_orders | > 95% |
| Cycle Time | Speed | AVG(end - start) | depends |

#### Operations Module
| KPI | Category | Formula | Target |
|---|---|---|---|
| Order Fulfillment Rate | Quality | shipped_on_time / total | > 95% |
| Inventory Turnover | Volume | COGS / avg_inventory | depends |
| Stock-out Rate | Quality | out_of_stock_days / total | < 5% |

---

### 17.4 Threshold Patterns

**Pattern: 4-level threshold with actions**

```
| Metric | Green (Normal) | Yellow (Watch) | Orange (Warn) | Red (Critical) | Action |
|---|---|---|---|---|---|
| QT Approval Time | < 1 day | 1-2 days | 2-3 days | > 3 days | Auto-escalate at red |
| AR Aging | < 30 days | 30-60 days | 60-90 days | > 90 days | Block new sales at red |
| Inventory Level | > safety_stock | reorder_point - safety | < reorder_point | < safety_stock | Auto-PR at orange |
```

**Pattern: Simple Min/Max**

```
| Metric | Min | Max | Action |
|---|---|---|---|
| QT Conversion Rate | 40% | — | Trigger sales review if below |
| Approval Time | — | 2 days | Alert manager if above |
```

---

### 17.5 Throughput Patterns

**Pattern: Scaling levels**

```
- Capacity (Designed): 1000 transactions/day
- Baseline (Current): 200 transactions/day (20% of capacity)
- Stress Point: 800 transactions/day → check DB performance
- Failure Point: 1500 transactions/day → system slowdown expected
```

**Pattern: Concurrent users**

```
- Designed: 100 concurrent users
- Current peak: 30 concurrent users
- Stress test: 80 concurrent users → response time degrades 2x
```

---

## Section 18: Monitoring Patterns

### 18.1 Reports Overview Patterns

**4 Standard Types (บังคับ):**

| Report Type | Purpose | Frequency | Audience |
|---|---|---|---|
| **Performance** | Daily ops monitoring | Real-time / Daily | Operations Manager |
| **Closing** | Period-end summary | Daily / Weekly / Monthly | Finance / Director |
| **Anomaly** | Out-of-range / suspicious activity | Real-time / Daily | Manager / Auditor |
| **Transaction** | Full audit trail | On-demand | Auditor / Compliance |

---

### 18.2 Dashboard Widget Patterns

**Pattern A: KPI Card**
```
Widget: [KPI Name]
Display: Big number + Trend arrow + % change vs previous period
Source: KPI #N from 17.3
Threshold: Color-coded from 17.4
```

**Pattern B: Trend Chart**
```
Widget: [Metric] Trend
Display: Line chart (last 30/90/365 days)
Source: KPI #N from 17.3
Drill-down: เข้า Detail Report
```

**Pattern C: Distribution**
```
Widget: [Metric] Distribution
Display: Pie / Donut / Bar chart
Source: Breakdown of KPI
Use: Top-N analysis, segmentation
```

**Pattern D: Funnel**
```
Widget: [Process] Funnel
Display: Funnel chart with conversion %
Source: Multiple state transitions
Use: Sales funnel, support ticket funnel
```

**Pattern E: Heat Map**
```
Widget: [Metric] Heat Map
Display: Grid (e.g., day × hour)
Source: Activity log
Use: Peak time analysis
```

---

### 18.3 Performance Report Patterns

```markdown
**Performance Report Template:**

1. **Summary** (top of report)
   - Period: [Date range]
   - Total: [number]
   - Avg: [number]
   - Trend: [up/down %]

2. **By Dimension**
   - By User / Employee
   - By Region / Branch
   - By Product / Service
   - By Customer Segment

3. **Top / Bottom**
   - Top 10 best performers
   - Bottom 10 (with action items)

4. **Trend**
   - Daily / Weekly / Monthly view
   - YoY comparison
```

---

### 18.4 Closing Report Patterns

```markdown
**Closing Report Template:**

1. **Period Summary**
   - Period: [Date range]
   - Total transactions: [N]
   - Total amount: [Amount]

2. **By Status**
   - Pending: [N]
   - Approved: [N]
   - Rejected: [N]
   - Cancelled: [N]

3. **YoY Comparison**
   - Current period vs Previous period
   - Variance analysis (absolute + %)

4. **Outstanding Items**
   - Pending approval > SLA
   - Pending payment > 30 days
```

---

### 18.5 Anomaly Report Patterns

**Common Anomaly Triggers:**

| Trigger | Description | Action |
|---|---|---|
| Over-DoA Approval | User approves > their DoA limit | Audit flag + investigate |
| Quick Approve | Approve < 1 minute after submit | Audit flag (suspicious) |
| Multiple Revisions | > 5 revisions in 1 day | Audit flag (instability) |
| Off-hours Activity | Action at 2-4 AM | Audit flag (potential fraud) |
| Round-amount | Suspicious round number (1,000,000) | Audit flag (possible manipulation) |
| Duplicate Pattern | Same data pattern repeated | Audit flag |
| Threshold Breach | Metric < Min or > Max | Auto-alert |
| Failed Login | > 5 failed attempts | Lock account |

---

### 18.6 Transaction Report Patterns

```markdown
**Transaction Report Template:**

For each transaction:

1. **Header**
   - Transaction ID
   - Type
   - Created by / date
   - Current status
   - Current owner

2. **Field Changes (Audit Log)**
   | Date/Time | User | Field | Old Value | New Value |

3. **State Transitions**
   | Date/Time | From State | To State | By User | Reason |

4. **Approvals**
   | Step | Approver | Decision | Date/Time | Reason |

5. **Attachments**
   | File | Size | Uploaded By | Date |

6. **Related Documents**
   | Type | Reference | Status |
```

---

## Coverage Verification

After embedding Section 17 + 18, verify:

```
Verification 1: SLA → Widget/Report
ทุก SLA ใน 17.1 → ต้องมี Widget ใน 18.2 หรือ Report ใน 18.3 ที่ track time

Verification 2: KPI → Widget
ทุก KPI ใน 17.3 → ต้องมี Widget ใน 18.2

Verification 3: Threshold → Anomaly Alert
ทุก Threshold ใน 17.4 → ต้องมี Anomaly trigger ใน 18.5

Verification 4: Control Point → Audit Trail
ทุก Control Point ใน 17.2 → ต้องบันทึกใน Transaction Report 18.6
```

ถ้าขาด coverage → ❌ Quality Gate PE05 ไม่ผ่าน
