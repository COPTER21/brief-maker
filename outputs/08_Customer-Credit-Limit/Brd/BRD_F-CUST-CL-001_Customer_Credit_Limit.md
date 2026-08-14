# BRD — F-CUST-CL-001 Customer Credit Limit

| รายการ | ค่า |
|---|---|
| เวอร์ชัน / สถานะ | 1.0 / APPROVED |
| ประเภท | New Feature · Governance / Workflow |
| โมดูล | Sales (O2C) · Wave S2 |
| เจ้าของธุรกิจ | Credit Officer / Sales Admin |
| แหล่งอ้างอิง | PREBRIEF_F-CUST-CL-001, Function Checklist, HTML prototype ที่ผ่าน UX/E2E review |
| วันที่ | 2026-08-14 |

## 1. เอกสารและ Changelog

ฟีเจอร์นี้เป็นเจ้าของข้อมูลวงเงินเครดิตของลูกค้า การเปลี่ยนวงเงินต้องผ่าน DOA และมี audit แบบ append-only เสมอ

| เวอร์ชัน | วันที่ | รายการ |
|---|---|---|
| 1.0 | 2026-08-14 | สร้างจาก PREBRIEF และ HTML ที่ PM/BA ตรวจผ่าน |

## 2. Business Context

### 2.1 ปัญหาและเป้าหมาย

วงเงินเครดิตต้องมีเจ้าของข้อมูลเพียงจุดเดียว เพื่อป้องกันการแก้จาก Customer Master โดยตรง และให้ Sales Order ใช้ข้อมูลวงเงิน/hold ที่อนุมัติแล้วในการ credit check ภายหลัง ฟีเจอร์นี้ให้เจ้าหน้าที่เสนอการตั้งหรือปรับวงเงิน ติดตามยอดใช้และความเสี่ยง และให้ผู้มีสิทธิ์อนุมัติผ่าน DOA กลาง

### 2.2 Success metrics

| ตัวชี้วัด | Baseline | Target | วิธีวัด |
|---|---|---|---|
| การเปลี่ยนวงเงินที่มี audit ครบ | เก็บ baseline ก่อน launch | 100% | ตรวจ audit event ต่อ request |
| การเปลี่ยนวงเงินที่ bypass DOA | เก็บ baseline ก่อน launch | 0 รายการ | ตรวจ approval status / DOA snapshot |
| profile ลูกค้าใหม่ที่ถูกสร้างอัตโนมัติ | เก็บ baseline ก่อน launch | 100% ของ Customer Master create event | reconciliation รายวัน |

## 3. Scope

### 3.1 In scope

- ทะเบียน Credit Profile หนึ่งรายการต่อลูกค้าหนึ่งราย
- ขอวงเงินครั้งแรก ปรับเพิ่ม และปรับลดผ่าน DOA
- สถานะ `draft → pending_approval → approved/rejected` และวงเงินจริงเปลี่ยนเมื่อ approved ครบสายเท่านั้น
- hold/unhold, review, audit, list/search/filter/sort, AR/SO outstanding แบบอ่านอย่างเดียว
- ส่งวงเงินอนุมัติแล้วให้ Customer Master อ่าน และส่ง flag/limit ให้ Sales Order ใช้ credit check

### 3.2 Out of scope

- แก้วงเงินโดยตรงหรือแก้จาก Customer Master
- ลบ Credit Profile
- ตั้งสายอนุมัติหรือกำหนดผู้อนุมัติในฟีเจอร์นี้
- สร้าง/แก้ Sales Order, AR Invoice, Notification หรือ Customer Master
- My Approval รายบุคคล

### 3.3 Assumptions

- Customer Master เป็นแหล่งข้อมูลลูกค้าและส่ง create event ได้
- AR Invoice และ Sales Order จะเป็น read model ของยอดใช้เมื่อ feature ปลายทางพร้อม
- ผู้มีสิทธิ์อนุมัติและชื่อผู้เซ็นจริงมาจาก DOA/My Profile

### 3.4 Scope Lock

| LOCK | ข้อตกลงที่ห้ามเปลี่ยนใน feature |
|---|---|
| LOCK-CL-01 | Customer Credit Limit เป็นเจ้าของวงเงิน; Customer Master อ่านอย่างเดียว |
| LOCK-CL-02 | การตั้ง/ปรับวงเงินทุกครั้งผ่าน DOA; ห้าม hardcode chain |
| LOCK-CL-03 | Profile ผูกลูกค้า 1:1 และห้ามลบ; audit append-only |
| LOCK-CL-04 | ใช้สถานะกลาง ไม่สร้าง My Approval รายคน |
| LOCK-CL-05 | Sales Order/AR Invoice/Notification เป็น external contract ไม่ใช่งานสร้างในรอบนี้ |

## 4. Roles & Permissions

| Role | อ่าน | สร้าง/ส่งคำขอ | Hold / Unhold / Review | อนุมัติ / Reject |
|---|---:|---:|---:|---:|
| Credit Officer / Sales Admin | ✓ | ✓ | ✓ | — |
| DOA approver role | ✓ | — | — | ✓ เฉพาะขั้นปัจจุบันที่ DOA resolve |
| System | ✓ | สร้าง profile จาก event | บันทึก audit / คำนวณยอดใช้ | resolve DOA / apply limit |

## 5. User Journey with COSO

| Step | เหตุการณ์ | Maker | Checker | Approver | System |
|---|---|---|---|---|---|
| 1 | เปิด Credit Profile และตรวจยอดใช้/AR | Credit Officer | — | — | คำนวณ available/utilization |
| 2 | กรอกวงเงินใหม่และเหตุผล บันทึกเป็น `draft` | Credit Officer | — | — | ตรวจข้อมูลและ preview DOA |
| 3 | กด `ส่งอนุมัติ` | Credit Officer | — | DOA roles (ยังไม่ลงชื่อ) | resolve แล้ว freeze approval chain |
| 4 | อนุมัติทีละขั้น | — | — | DOA role ขั้นปัจจุบัน | บันทึก signer/time และ advance step |
| 5 | อนุมัติครบสาย | — | — | DOA role ขั้นสุดท้าย | apply limit, publish approved projection, audit |
| 6 | Reject พร้อมเหตุผล | — | — | DOA role ขั้นปัจจุบัน | เก็บเหตุผล, คงวงเงินเดิม, ปิดคำขอ |
| 7 | Hold/Unhold หรือ Review | Credit Officer | — | — | เปลี่ยน hold/review date และ audit |

SoD: ผู้ขอห้ามอนุมัติคำขอของตนเอง; ผู้อนุมัติจริงตรวจจาก DOA role และ My Profile

## 6. Data Entity

### 6.1 Credit Profile

| Field | Label | Type | Required | Source / note |
|---|---|---|---:|---|
| customer_id | รหัสลูกค้า | LOOKUP | ✓ | Customer Master |
| credit_limit | วงเงินเครดิต | NUMBER | — | เปลี่ยนหลัง approved เท่านั้น |
| risk_level | ระดับความเสี่ยง | DROPDOWN | — | low/mid/high; วิธีประเมินเป็น OQ |
| is_credit_hold | ระงับเครดิต | TOGGLE | ✓ | default false |
| payment_term / credit_period | เงื่อนไข / ระยะเครดิต | read-only | — | Customer Master/master |
| last_review_at | ทบทวนล่าสุด | DATE | — | update จาก review |
| audit_events | ประวัติ | system | ✓ | append-only |

### 6.2 Credit Limit Change Request

| Field | Label | Type | Required | Note |
|---|---|---|---:|---|
| request_no | เลขคำขอ | AUTO | ✓ | `CLR-YYYY-NNNN` |
| current_limit / requested_limit | วงเงินเดิม / วงเงินที่ขอ | NUMBER | ✓ | requested ต้องต่างจาก current |
| reason | เหตุผล | TEXTAREA | ✓ | required ก่อนส่ง |
| approval_status | สถานะ | system | ✓ | draft/pending_approval/approved/rejected |
| doa_entry_ref | DOA entry | system | — | binding เป็น OQ จนตั้งค่ากลางเสร็จ |
| approval_chain | สายอนุมัติ snapshot | system | — | resolve ณ เวลาส่ง; role-id only |
| current_step | ขั้นปัจจุบัน | system | — | advance ตาม approval |
| approved_by / approved_at | ผู้เซ็น/เวลา | system | — | จาก My Profile ตอนเซ็น |

Relationship: `Customer Master 1 ── 1 Credit Profile 1 ── N Change Request`; `Credit Profile 1 ── N Audit Event`.

## 7. User Stories & Acceptance Criteria

| ID | User story | Acceptance criteria |
|---|---|---|
| S-01 | เจ้าหน้าที่ตั้งวงเงินครั้งแรก | Given ลูกค้าเงินสด When ส่งคำขอและอนุมัติครบ Then วงเงินจริงเปลี่ยนจาก 0 และมี audit |
| S-02 | เจ้าหน้าที่ปรับวงเงิน | Given profile active When ขอเพิ่มหรือลด Then วงเงินเดิมคงอยู่จน approved ครบ |
| S-03 | ผู้อนุมัติตัดสินคำขอ | Given pending request When ลงชื่อในขั้นตน Then timeline และ step เปลี่ยน; ผู้ขอไม่เซ็นเอง |
| S-04 | เจ้าหน้าที่ hold เครดิต | Given profile active When กรอกเหตุผลและยืนยัน Then hold flag เปลี่ยนและ audit เพิ่ม |
| S-05 | ผู้ใช้ตรวจเครดิต | Given profile มีวงเงิน When เปิดรายละเอียด Then เห็น limit/used/available/utilization และ AR ที่เกี่ยวข้อง |
| S-06 | ระบบสร้าง profile | Given Customer Master สร้างลูกค้า When รับ event Then สร้าง profile limit 0/เงินสดหนึ่งรายการ |

## 8. Status & Lifecycle

```text
ไม่มีคำขอ → draft → pending_approval → approved (apply limit)
                         └──────────→ rejected (retain current limit)
Profile: active ⇄ hold
```

| From | Trigger | To | Guard |
|---|---|---|---|
| — | บันทึกคำขอ | draft | requested_limit ต่าง current_limit และมี reason |
| draft | ส่งอนุมัติ | pending_approval | DOA resolve สำเร็จ; ไม่เป็น no_amount_tier |
| pending_approval | approve ขั้นกลาง | pending_approval | approver เป็น current DOA role |
| pending_approval | approve ขั้นสุดท้าย | approved | ครบทุก step; apply limit |
| pending_approval | reject | rejected | reason required |
| active | hold | hold | reason required |
| hold | unhold | active | reason required |

## 9. Business Rules & Flexibility

| ID | Rule | Tag / implementation |
|---|---|---|
| BR-01 | ทุกการตั้งหรือปรับวงเงินผ่าน DOA | FIXED |
| BR-02 | apply วงเงินจริงเมื่อ approved ครบสายเท่านั้น | FIXED |
| BR-03 | ระบบ resolve และ snapshot chain จาก DOA ณ เวลาส่ง | CONFIGURABLE · DOA central |
| BR-04 | DOA เก็บ role-id; My Profile ให้ชื่อ/ผู้เซ็นจริง | FIXED |
| BR-05 | no_amount_tier ต้อง block ส่งแบบ fail-closed | FIXED |
| BR-06 | reason required สำหรับ change/reject/hold/unhold | FIXED |
| BR-07 | used = open AR Invoice + confirmed SO ที่ยังไม่วางบิล | CONFIGURABLE · read-model contract |
| BR-08 | near-full ≥85%, over >100%, limit 0 = เงินสด | CONFIGURABLE · threshold ต้องยืนยันโดย BA |
| BR-09 | hold ต้องส่งผลให้ SO block การขายเชื่อ | CONFIGURABLE · contract Sales Order |
| BR-10 | ทุก action เขียน audit append-only | FIXED |
| BR-11 | Customer Master create event สร้าง profile 0/เงินสด | FIXED |
| BR-12 | สถานะกลางเดียว; ไม่มี My Approval รายคน | FIXED |
| BR-13 | Customer Master อ่านวงเงินที่ approved แล้วเท่านั้น | FIXED |

### 9.5 Flexibility summary

- BR-03: DOA central matrix, เปลี่ยนได้ที่ DOA โดยผู้ดูแล policy
- BR-07/09: ต้อง wire กับ source/downstream feature เมื่อพร้อม
- BR-08: ค่า 85% เป็น `[AI-DEFAULT]` จาก brief รอ BA ยืนยัน

## 10. Edge Cases

| ID | Case | Expected |
|---|---|---|
| EC-01 | จำนวนเท่าเดิมหรือไม่มีเหตุผล | ปุ่มส่ง disabled |
| EC-02 | DOA ไม่พบ tier | ไม่ส่งคำขอ; แจ้งให้ตั้งช่วงวงเงินที่ DOA |
| EC-03 | ผู้ขอกดอนุมัติคำขอตนเอง | API ปฏิเสธ; audit security event |
| EC-04 | DOA ถูกแก้หลังส่ง | request เดิมใช้ snapshot เดิม |
| EC-05 | เปลี่ยนจำนวนหลังส่ง | ไม่ให้แก้; ต้องสร้าง draft ใหม่และ resolve ใหม่ |
| EC-06 | Reject ไม่มีเหตุผล | ปุ่มยืนยัน disabled |
| EC-07 | Customer ถูก hold | แสดงสถานะ hold; SO เป็นผู้ enforce การขายเชื่อ |
| EC-08 | AR/SO read model ไม่พร้อม | แสดงสถานะข้อมูลล่าสุดที่มี; ไม่ใช้เพื่อ apply limit |

## 11. Impact

ไม่มี regression กับ Customer Master เพราะเป็น read-only contract; ต้อง regression test การแสดงวงเงินที่ Customer Master และ credit check ที่ Sales Order หลัง endpoints พร้อม

## 12. Value Stream & Existing System

### 12.1 Position and downstream impact

`Customer Master → Customer Credit Limit → Sales Order credit check → AR Invoice outstanding`

| Direction | System | Data / trigger | Impact when changed |
|---|---|---|---|
| Upstream | Customer Master | customer_created | create profile 0/เงินสด |
| Upstream | AR Invoice / Sales Order | outstanding balances | recalculate used/available only |
| Upstream | Policy Center DOA | resolved chain | freeze snapshot at submit |
| Downstream | Customer Master | approved limit projection | display latest limit read-only |
| Downstream | Sales Order | approved limit + hold flag | block/warn credit sale per SO policy |

### 12.3 Existing system references

| Capability | Reference | Status |
|---|---|---|
| Customer reference | Related context/7. Customer | confirmed ref |
| Approval policy | Policy Center DOA / F-CL-001 | declaration pending wire |
| Approver identity | My Profile | external contract |
| Outstanding read model | Sales Order / AR Invoice | not available yet; mock only |

## 13. Delivery Phases

1. Launch: profile, request workflow, DOA resolve/snapshot, audit, hold/review, UI
2. Wire: Customer Master event/projection, My Profile signer, AR/SO read model
3. Downstream: Sales Order credit enforcement and agreed notification delivery

## 14. Development Requirements Summary

- ห้าม hardcode approval chain หรือแก้ DOA configuration ใน feature
- ทุก mutation ต้อง enforce permission server-side และ append audit
- ใช้ DOA snapshot ไม่ใช่ re-resolve ระหว่าง pending
- implement fail-closed หาก DOA resolve ไม่สำเร็จ
- เครดิตและยอดใช้เป็น money decimal; เวลา audit ใช้ server timestamp
- prototype เป็น UI source of truth: list, detail drawer, change drawer, approval tab, hold/review/reject overlays

### 14.6 Screen inventory

| ID | Route | Type | Primary user | Business purpose |
|---|---|---|---|---|
| P-01 | `#/credit-limit` | หน้ารายการ | Credit Officer | ค้นหา/filter/sort และดูสถานะกลาง |
| P-02 | overlay จาก P-01 | รายละเอียด drawer | ทุก role | ดู profile, AR, audit และ approval |
| P-03 | overlay จาก P-02 | change drawer | Credit Officer | บันทึก draft และส่งอนุมัติ |
| P-04 | overlay จาก P-02 | confirm/reject modal | Credit Officer / Approver | hold, unhold, reject พร้อมเหตุผล |

## 15. Open Questions

| ID | Question | Owner |
|---|---|---|
| OQ-CL-01 | DOA resolve ใช้ requested absolute limit หรือ delta | BA / Policy owner |
| OQ-CL-02 | มี direct-set band ที่ไม่ต้อง approve หรือไม่ | BA / Compliance |
| OQ-CL-03 | role ids และ amount tiers จริงใน DOA | DOA admin |
| OQ-CL-04 | hold/unhold ต้องผ่าน DOA หรือ credit officer permission | Compliance |
| OQ-CL-05 | risk source และ threshold ที่ยืนยันแล้ว | BA |
| OQ-CL-06 | API/event contract ของ Customer Master, SO, AR และ My Profile | respective feature owners |

## 16. Security & Compliance

Preset: Approval/financial governance (P2 + financial controls as applicable). Enforce RBAC, SoD, server-side authorization, immutable audit, least privilege, validation, and fail-closed DOA resolution. ไม่แสดงหรือเก็บลายเซ็นใน feature; identity อ้าง My Profile.

## 17. Health Check

| Area | Metric / threshold | Action |
|---|---|---|
| DOA resolve | success rate; error >0 | alert and block submission |
| Approval backlog | pending age by tier | dashboard for credit owner |
| Integration | unmatched Customer Master create event | reconciliation queue |
| Audit | mutation without audit | critical investigation |

## 18. Monitoring

รายงานที่ต้องมีภายหลัง: pending approvals aging, hold customers, utilization near/over limit, DOA resolution failures, profile reconciliation, and audit export for compliance.

---

## AI Review Report

**Verdict: APPROVED.** C01–C23 / PE01–PE05 reviewed: scope lock, roles/SoD, lifecycle, tagged rules, edge cases, value-stream contracts, KPI/monitoring, and OQs are present. No critical source conflict found. External features are recorded as contracts/OQs, not silently implemented in this scope.
