# BASELINE_F-PUR-PO — PO ใบสั่งซื้อ vs ERP Standard

> S0.5 · feature-review-standard · 2026-09-10 · web search 3 queries (SAP / Odoo / D365+NetSuite) — เสริมด้วยความรู้ ERP ภายใน
> ขอบเขตเทียบ: SAP S/4HANA MM · Odoo 18 Purchase · Microsoft Dynamics 365 SCM · Oracle NetSuite · ERPNext v15

---

## 1. สรุปเร็ว
PO ของ ERP ระดับโลกไม่ใช่ "ฟอร์มสั่งของ" แต่เป็น **จุดเกิด commitment** — เอกสารที่พอ approve แล้วผูกพันตามกฎหมาย, กันงบ (encumbrance/commitment), และกลายเป็น "สัญญาต้นทาง" ที่ GRN และ AP Invoice ต้อง match กลับมา (3-way match). ทุกเจ้าจึงลงทุนกับ 3 เรื่องเหมือนกัน: **(ก) สายอนุมัติแบบ configurable ตามวงเงิน · (ข) การควบคุมการแก้ไขหลังอนุมัติ (change order / re-approval) · (ค) สถานะการรับของสะสมต่อบรรทัด (open qty / partially received)**

---

## 2. Must-have (ERP ทุกเจ้ามี — CUBE ต้องมีใน scope นี้)

| # | ความสามารถ | เทียบมาจาก | มีใน scope F-PUR-PO? |
|---|---|---|---|
| M-01 | Header/Line structure: vendor · วันที่ · เงื่อนไขชำระ · สกุลเงิน · warehouse ปลายทาง · line = item/qty/uom/ราคา/ส่วนลด/VAT/วันส่งของ | ทุกเจ้า | ✅ B2 v2 line editor |
| M-02 | สถานะ lifecycle ชัดเจน (draft → approved → sent → received → closed/cancelled) | Odoo (RFQ→RFQ Sent→PO→Done) · D365 (Draft→In review→Approved→Confirmed) | ✅ `draft → approved → sent → partially received → closed/cancelled` |
| M-03 | สายอนุมัติตามวงเงิน (release strategy / approval workflow) | SAP Release Strategy · D365 workflow · NetSuite BPO approval | ✅ DOA slot picker คนจริง |
| M-04 | สร้าง PO จาก PR/RFQ (พร้อม traceability กลับต้นทาง) | SAP PR→PO · Odoo RFQ · D365 | ✅ mock `[ASSUMED contract]` (PR = F072 · W2) |
| M-05 | สร้าง PO ตรงได้ (ไม่ต้องมี PR) | ทุกเจ้า (direct PO) | ✅ ในสโคป — บังคับต้องได้ |
| M-06 | ควบคุมการแก้หลังอนุมัติ = change order + re-approval | D365 Change management · NetSuite Resubmit · SAP re-release | ✅ Transition Guard → re-approve |
| M-07 | รับของสะสมต่อ line (open qty / partially received / delivery completed) | SAP GR + "Delivery Completed" indicator | ✅ สถานะ partially received (GRN ยิงกลับ · เลนถัดไป) |
| M-08 | Over/under-delivery tolerance % ต่อ line | SAP over/under delivery tolerance · Odoo bill control | ✅ **OQ-PO-01 `[ASSUMED]` default 0% · config ต่อ tenant** |
| M-09 | พิมพ์/ส่ง PO ให้ผู้ขาย (PDF + email) + สถานะ "sent" | Odoo Send by Email · SAP message output | ✅ สถานะ sent + pdfdoc print spec |
| M-10 | เลขเอกสารรันอัตโนมัติ ตั้งรูปแบบได้ | ทุกเจ้า (number sequence) | ✅ doccfg `PO-YYYY-NNNN` (ห้าม hardcode) |
| M-11 | ยกเลิก PO ได้ + กันยกเลิกหลังรับของบางส่วน | ทุกเจ้า | ✅ cancelled + guard |
| M-12 | Audit trail ว่าใครแก้อะไรเมื่อไร (append-only) | ทุกเจ้า | ✅ tab ประวัติ · append-only |
| M-13 | Budget/commitment check ตอนอนุมัติ (encumbrance) | D365 encumbrance · NetSuite commitment | ⚠️ **mock + `TODO: budget-control hook`** (Budget Control = F117 · W7) |
| M-14 | 3-way match readiness: PO เป็นต้นทางให้ GRN + AP Invoice | ทุกเจ้า | ✅ PO line เป็น source ให้ GRN (เลนถัดไป) |
| M-15 | เอกสารแนบ (ใบเสนอราคา/สัญญา) ติดกับ PO | ทุกเจ้า | ✅ เอกสารแนบใน landing (Pattern Q) |

---

## 3. Nice-to-have (ERP มี แต่ไม่อยู่รอบนี้ — ยกเป็น backlog)

| # | ความสามารถ | เทียบมาจาก | สถานะใน CUBE |
|---|---|---|---|
| N-01 | Blanket PO / Contract PO + call-off release | SAP Outline Agreement · NetSuite Blanket PO | backlog (ไม่อยู่ W3) |
| N-02 | Vendor portal / vendor confirmation กลับเข้าระบบ | Odoo portal · SAP Ariba | backlog |
| N-03 | Landed cost (ค่าขนส่ง/ภาษีนำเข้า เฉลี่ยเข้าต้นทุน) | Odoo landed cost · NetSuite | backlog (ผูก W5) |
| N-04 | Multi-currency + FX rate ณ วันอนุมัติ vs วันรับของ | ทุกเจ้า | scope นี้ = สกุลเงินเดี่ยว/แสดง field ได้ · logic FX ไม่ทำ |
| N-05 | Drop-ship PO ยิงตรงถึงลูกค้า | Odoo · NetSuite | backlog (ผูก O2C) |
| N-06 | Subcontracting PO (ส่งวัตถุดิบให้ผู้รับจ้าง) | SAP subcontracting | backlog |
| N-07 | Auto-PO จาก reorder point / MRP | ทุกเจ้า | backlog (ผูก Inventory Planning) |
| N-08 | Price history / last purchase price แนะนำตอนกรอกราคา | Odoo · ERPNext | ✅ แสดงเป็น hint ได้ (nice) — ไม่ block |
| N-09 | PO acknowledgement / expected date confirmation จากผู้ขาย | D365 confirmation | backlog |

---

## 4. Out-of-scope (จงใจไม่ทำ — ห้ามหลุดเข้ามา)
- **PR จริง** (F072 · W2-PUR-LITE) — PO แค่ mock contract ฝั่งรับ
- **Compare Vendors จริง** (F073 · W2) — รับผลผู้ชนะแบบ soft-ref เท่านั้น
- **Budget Control engine จริง** (F117 · W7) — hook เป็น mock + TODO
- **JE / GL posting** (W5) — PO ไม่ post บัญชี (commitment ≠ actual)
- **GRN / RTV** — feature ถัดไปในเลน W3P
- **AP Invoice / 3-way match execution** — คนละเลน
- Vendor Master / Item Master / UOM / Location / Cost Center — soft-ref LD-4C-02 (DONE แล้ว)

---

## 5. Gap vs CUBE (สิ่งที่ต้องระวังตอน PREBRIEF/HTML)

| Gap | รายละเอียด | ท่าที |
|---|---|---|
| G-01 | ERP ส่วนใหญ่ผูก **commitment เข้างบทันทีที่ approve** — CUBE ยังไม่มี Budget Control | mock hook + `TODO: budget-control hook` · แสดงผลตรวจงบเป็น mock badge ใน wizard step ตรวจสอบ ห้ามคำนวณจริง |
| G-02 | SAP/D365 มี **change order versioning** (PO v1/v2 เก็บทั้งคู่) | CUBE รอบนี้ = re-approve + audit trail (append-only) · versioning เต็มรูปแบบ = backlog · ต้องระบุใน PREBRIEF ว่าแก้แล้วสถานะกลับ draft/pending re-approve |
| G-03 | tolerance รับเกิน — ERP ตั้งได้ทั้ง over/under % ต่อ line | CUBE = `OQ-PO-01 [ASSUMED]` tolerance % ต่อ tenant · **default 0%** · owner Strike · เก็บเป็น config ไม่ hardcode ใน feature |
| G-04 | SAP มี "Delivery Completed" indicator ปิด line ทั้งที่รับไม่ครบ | CUBE ต้องมีทางปิด PO แบบ manual close (short-close) ไม่งั้น PO ค้างตลอดกาล → ใส่ใน PREBRIEF เป็น scenario |
| G-05 | Odoo/D365 ส่ง PO ทาง email แล้วบันทึกสถานะ sent อัตโนมัติ | CUBE = ntf declaration ยิง event `po.sent` · ห้าม hardcode ช่องทาง |
| G-06 | Approval matrix ของ ERP อ้าง role/position — **CUBE ล็อกว่าต้องเลือกคนจริง** (DOA-UI-LOCK 2026-08-17) | ต่างจาก standard โดยตั้งใจ — ห้ามเปลี่ยนกลับเป็น role ID |
| G-07 | ERP มี PO line type = service (ไม่มี stock movement) | CUBE รอบนี้รองรับ line type สินค้า/บริการ ที่ระดับ field · logic คลังต่างกันไปโผล่ที่ GRN | 

---

## 6. Verdict
Scope F-PUR-PO ครอบ **must-have 14/15 เต็ม** · M-13 (budget commitment) เป็น mock ตามกติกา forward-wire ที่ตั้งใจ — ไม่ถือว่าขาด
Gap ที่ต้องเติมเข้า PREBRIEF: **G-02 (re-approve + สถานะย้อน) · G-03 (tolerance config) · G-04 (manual short-close)**

Sources:
- [Applying Tolerances and the Delivery Completed Indicator — SAP Learning](https://learning.sap.com/courses/inventory-management-and-physical-inventory-in-sap-s-4hana/applying-tolerances-and-the-delivery-completed-indicator)
- [Setting up Purchase Order Release Strategy — SAP Community](https://community.sap.com/t5/sap-for-retail-blogs/setting-up-purchase-order-release-strategy/ba-p/13263453)
- [Purchase Features — Odoo](https://www.odoo.com/app/purchase-features)
- [Bill control policies / 3-way matching — Odoo documentation](https://www.odoo.com/documentation/16.0/purchase/purchases/rfq/3_way_matching.html)
- [Approve and confirm purchase orders — Dynamics 365 SCM](https://learn.microsoft.com/en-us/dynamics365/supply-chain/procurement/purchase-order-approval-confirmation)
- [Blanket Purchase Order Approval Workflow — Oracle NetSuite](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_4236988757.html)
- [Encumber purchase orders — Microsoft Learn](https://learn.microsoft.com/th-th/dynamicsax-2012/appuser-itpro/encumber-purchase-orders)
