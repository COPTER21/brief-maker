# COSO Roles Defaults

ใช้เมื่อ RIF หรือ user ไม่ระบุ COSO Roles ใน step ต่างๆ
อ้างอิงตามมาตรฐาน COSO Internal Control Framework

---

## 4 Roles in COSO

| Role | Description | Example |
|---|---|---|
| **Maker** | คนสร้าง / ลงมือ / กรอกข้อมูล | Sales Officer สร้าง QT |
| **Checker** | คนตรวจสอบก่อนถึง Approver (optional layer) | Senior Sales review ก่อนส่ง Manager |
| **Approver** | คนอนุมัติ — มีอำนาจตัดสินใจ | Sales Manager approve QT |
| **System** | สิ่งที่ระบบทำอัตโนมัติ | Auto-validate, Auto-fill, Audit Log |

---

## Default Mapping by Module

### Sales Module

| Action | Maker | Checker | Approver |
|---|---|---|---|
| Create Quote | Sales Officer | — | — |
| Submit Quote for approval | Sales Officer | Senior Sales (optional) | Sales Manager |
| Approve Quote (≤ 100K) | — | — | Sales Manager |
| Approve Quote (≤ 500K) | — | — | Sales Director |
| Approve Quote (> 500K) | — | — | CEO |
| Convert Quote to SO | Sales Officer | — | Sales Manager |
| Cancel SO | Sales Officer | Sales Manager | Sales Director |

### Purchase Module

| Action | Maker | Checker | Approver |
|---|---|---|---|
| Create PR | Requestor (any dept) | Department Head | — |
| Approve PR | — | — | Department Head |
| Convert PR to PO | Buyer (Purchasing) | — | Purchasing Manager |
| Approve PO (≤ 100K) | — | — | Purchasing Manager |
| Approve PO (≤ 500K) | — | — | Purchasing Director |
| Approve PO (> 500K) | — | — | CEO |
| Receive Goods (GR) | Warehouse Staff | Warehouse Manager | — |
| Approve GR Discrepancy | — | Warehouse Manager | Purchasing Manager |

### Finance Module

| Action | Maker | Checker | Approver |
|---|---|---|---|
| Create Voucher | Accountant | — | — |
| Approve Voucher | — | Senior Accountant | Finance Manager |
| Process Payment (≤ 100K) | Accountant | Senior Accountant | Finance Manager |
| Process Payment (≤ 1M) | Accountant | Finance Manager | CFO |
| Process Payment (> 1M) | Accountant | Finance Manager | CEO + CFO (joint) |
| Close Period | Accountant | Senior Accountant | Finance Manager |
| Approve Tax Filing | Accountant | Finance Manager | CFO |

### HR Module

| Action | Maker | Checker | Approver |
|---|---|---|---|
| Hire Request | Line Manager | HR Officer | Department Head |
| Approve Hire | — | HR Manager | Department Head |
| Promotion Request | Line Manager | HR Officer | Department Head + HR Director |
| Approve Promotion | — | HR Director | CEO (for senior roles) |
| Leave Request | Employee | — | Line Manager |
| Approve Leave (annual) | — | — | Line Manager |
| Approve Leave (special) | — | Line Manager | HR Manager |
| Salary Adjustment | HR Officer | HR Manager | CEO |

### Production Module

| Action | Maker | Checker | Approver |
|---|---|---|---|
| Create Production Order | Planner | — | Production Manager |
| Approve Production Order | — | Production Manager | Production Director |
| Material Issue | Warehouse Staff | Warehouse Manager | — |
| Quality Check | QC Inspector | QC Manager | — |
| Approve QC Result | — | — | QC Manager |
| Production Hold | QC Inspector | QC Manager | Production Director |

### Master Data Module

| Action | Maker | Checker | Approver |
|---|---|---|---|
| Create Customer | Sales Admin / Sales Officer | — | Sales Manager |
| Approve Customer Credit | — | Finance | Finance Manager |
| Create Vendor | Purchase Admin | Compliance Officer | Purchasing Manager |
| Approve Vendor Onboarding | — | Compliance Officer | Purchasing Director |
| Create Product | Product Manager | — | Product Director |
| Update Price List | Pricing Manager | — | Sales Director + Finance Manager |
| Inactivate Master Data | Admin | Senior Admin | Department Head |

---

## DoA (Delegation of Authority) Defaults

ถ้าไม่ระบุ ใช้ default ดังนี้:

### Approval Amount Tiers (THB)

| Tier | Amount | Default Approver |
|---|---|---|
| Tier 1 | ≤ 50,000 | Line Manager |
| Tier 2 | ≤ 200,000 | Department Manager |
| Tier 3 | ≤ 1,000,000 | Director |
| Tier 4 | ≤ 5,000,000 | Senior Director / VP |
| Tier 5 | > 5,000,000 | CEO + CFO (joint) |

### Special DoA

| Action | Approver |
|---|---|
| Write-off bad debt | CFO + Finance Director |
| Discount > 20% | Sales Director |
| Discount > 50% | CEO |
| Refund > 100K | Finance Director |
| Master Data deletion | Department Head + IT |

---

## SoD (Segregation of Duties) Rules

### Hard Rules (ห้ามฝ่าฝืน)

1. **Maker ≠ Approver** ในทุก approval step
2. **Vendor Onboarding ≠ Payment Processing** (คนเดียวกันไม่ได้)
3. **Customer Credit Setup ≠ Sales Order Creation** (คนเดียวกันไม่ได้)
4. **System Admin ≠ Audit Reviewer** (คนเดียวกันไม่ได้)
5. **Cash Receiving ≠ AR Reconciliation** (คนเดียวกันไม่ได้)

### Soft Rules (ควรหลีกเลี่ยง — แต่ override ได้พร้อม audit)

1. Junior Approver approve > DoA limit (require Senior co-approval + audit)
2. Approval ในช่วง off-hours (require comment + audit flag)
3. Approval ของตัวเองเป็น maker (require manager override + audit)

---

## Maker / Approver Inference จาก RIF

ถ้า RIF ระบุชื่อ role ใน §4 (Actors) แต่ไม่ระบุว่าเป็น Maker / Approver:

### Inference Logic

```
For each role in RIF §4:
  if role.responsibility contains keyword "สร้าง", "กรอก", "ลงมือ", "ส่ง":
    → Maker
  elif role.responsibility contains keyword "ตรวจ", "review":
    → Checker
  elif role.responsibility contains keyword "อนุมัติ", "approve", "ตัดสินใจ":
    → Approver
  elif role.responsibility contains keyword "เฝ้าระวัง", "ดู", "monitor":
    → Watcher (not in 4 core roles, but informational)
  else:
    → flag เป็น Open Question
```

---

## Watcher Role (Optional Informational Role)

ถึงไม่ใช่ใน 4 core roles แต่บางครั้งระบุได้:

| Watcher | คือใคร | บทบาท |
|---|---|---|
| Auditor | Internal Auditor | ตรวจหลังจาก fact |
| Compliance Officer | กฎหมาย/PDPA | ตรวจ compliance |
| Department Head | ผู้บริหารแผนก | รู้ว่าเกิดอะไรในแผนก (อาจไม่ approve เอง) |
| Owner | เจ้าของ feature | ต้องรู้ทุกการเปลี่ยนแปลง |

Watcher → ใส่ใน Section 18.5 Anomaly Report เป็น notification recipient
