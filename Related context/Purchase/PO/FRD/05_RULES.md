# 05_RULES — F-PO-001 ใบสั่งซื้อ (Purchase Order)

> **Audience:** BE + QA
> **Purpose:** Business Rules + Validation + State + Edge Cases + Errors + Data Classification enforcement

---

## §5.1 Business Rules (from BRD §9)
| Rule ID | Rule | Tag | Enforced in |
|---|---|:---:|---|
| R01 | status เริ่มต้น = draft | FIXED | FN-01 |
| R02 | PO ต้องมีผู้ขาย 1 ราย | FIXED | FN-05 / VR01 |
| R03 | แหล่งที่มาบังคับ + โหมดที่อนุญาต | CONFIGURABLE | FN-05 (อ่าน `purchase_source_mode`) |
| R04 | source=CP → vendor = ผู้ชนะ (locked) | FIXED | FN-04 |
| R05 | source=PR/direct → เลือก vendor จาก master | FIXED | FN-04 |
| R06 | payment_term default = vendor, แก้ได้ | DYNAMIC | FN-01/UI |
| R07 | VAT = 7% | CONFIGURABLE | ENG po-amount (`vat_rate`) |
| R08 | line VAT mode none/add/included | FIXED | ENG po-amount |
| R09 | discount ฿/% ; ฿ ≤ line subtotal | FIXED | ENG po-amount / VR05 |
| R10 | ฐาน VAT = หลังหักส่วนลด | FIXED | ENG po-amount |
| R11 | WHT rate ตามหมวด ฐานก่อน VAT | CONFIGURABLE | ENG po-amount (`wht_rate`) |
| R12 | DoA: amount ≤ tier limit | CONFIGURABLE | ENG doa-resolver |
| R13 | Maker ≠ Approver | FIXED | FN-06 (SoD) |
| R14 | po_no running เมื่อ approved | CONFIGURABLE | FN-07 |
| R15 | GRN trigger ตาม payment type | DYNAMIC | downstream contract |
| R16 | DEP%: แก้ได้ | DYNAMIC | (Phase 3) |
| R17 | INST งวด: แก้ได้ | DYNAMIC | (Phase 3) |
| R18 | ยกเลิก approved → approve + reason | CONFIGURABLE | FN-06 |
| R19 | expected_date default = po_date+7 | CONFIGURABLE | FN-01 (`po_lead_days`) |
| R20 | SLA อนุมัติ | WARNING | ⚠️ Q1 |

## §5.2 Validation Rules
| VR | Field/Action | เงื่อนไข | Type | Error code | Message |
|---|---|---|---|---|---|
| VR01 | vendor_id | required (พ้น step2) | Error | VENDOR_REQUIRED | กรุณาเลือกผู้ขาย |
| VR02 | po_date | ≤ today | Error | PO_DATE_FUTURE | วันที่ห้ามเป็นอนาคต |
| VR03 | expected_date | ≥ po_date | Error | DATE_ORDER | วันรับต้องไม่ก่อนวันที่ PO |
| VR04 | lines | ≥1 + qty>0 + price≥0 | Error | LINE_REQUIRED | ต้องมีรายการอย่างน้อย 1 |
| VR05 | discount_amt | ≤ line subtotal | Trigger | — | cap อัตโนมัติ |
| VR06 | submit amount | ≤ DoA tier สูงสุด | Error | DOA_OVER_CEILING | เกินอำนาจอนุมัติทุก tier |
| VR07 | reject/return/cancel | reason required | Error | REASON_REQUIRED | กรุณาระบุเหตุผล |
| VR08 | source=CP | ต้องเลือกผู้ชนะ | Error | WINNER_REQUIRED | เลือกผู้ขายจากตารางผู้ชนะ |

## §5.3 Calculation Rules → ENG po-amount-engine
ดู 03_LOGIC §3.2. ตัวอย่างยืนยัน (ตรง PO PDF sample):
- VAT: 15,850 +VAT 1,109.50 = 16,959.50
- NoVAT: 12,000 (ยกเว้น) = 12,000
- Discount: 71,000 −5% = 67,450 +VAT 4,721.50 = 72,171.50
- WHT: 70,000 +VAT 4,900 −WHT 3% 2,100 = net 72,800

## §5.4 State Transition Rules (status_doc)
| Current | Action | Next | Guard | Role |
|---|---|---|---|---|
| draft | submit | pending | validate ผ่าน + DoA resolve (VR06) | Buyer |
| pending | approve | approved | SoD (R13) + tier (R12) | Approver |
| pending | reject | rejected | reason (VR07) | Approver |
| pending | return | return→draft | reason + rev+1 | Approver |
| approved | cancel | cancelled | approve + reason + no GRN/AP (E09) | Approver |
| draft | cancel | cancelled | reason | Buyer |
> approved → lock เอกสาร (R-immutable, C-10); แก้ไม่ได้ (API-04 block)

## §5.5 Edge Cases (from BRD §10)
| ID | Case | Handling |
|---|---|---|
| E01 | CP ผู้ชนะออก PO แล้ว | disable ปุ่มเลือก + แสดงเลข PO เดิม (API-11 ส่ง po_status) |
| E02 | เลือกแค่ PR | ไม่มีตารางผู้ชนะ → vendor combobox step2 |
| E03 | PO ตรง (ไม่เลือก source) | กดถัดไปได้ → step3 มีแถวเปล่า |
| E04 | discount ฿ > subtotal | cap (VR05) |
| E05 | clear source | reset vendor |
| E07 | ยอดรวม = 0 | block submit (LINE/AMOUNT) |
| E08 | WHT > total | block + warn (รอ Q2 rate) |
| E09 | cancel ที่มี GRN/AP | block — reverse downstream ก่อน |
| E12 | 2 users แก้ draft | optimistic lock (version) → 409 CONFLICT |
| E14 | vendor/item inactive หลังเลือก | ใช้ snapshot + warn ตอน submit |
| E16 | buyer อนุมัติเอง | block SoD (R13) |

## §5.6 Error Catalog
| Code | HTTP | Message |
|---|---|---|
| VENDOR_REQUIRED | 422 | กรุณาเลือกผู้ขาย |
| WINNER_REQUIRED | 422 | เลือกผู้ขายจากตารางผู้ชนะ |
| LINE_REQUIRED | 422 | ต้องมีรายการอย่างน้อย 1 |
| DATE_ORDER / PO_DATE_FUTURE | 422 | วันที่ไม่ถูกต้อง |
| NOT_EDITABLE | 409 | แก้ได้เฉพาะสถานะ draft |
| CONFLICT | 409 | เอกสารถูกแก้โดยผู้อื่น (refresh) |
| SOD_VIOLATION | 403 | ผู้จัดทำอนุมัติเองไม่ได้ |
| DOA_INSUFFICIENT | 403 | อำนาจอนุมัติไม่พอสำหรับยอดนี้ |
| DOA_OVER_CEILING | 422 | ยอดเกินอำนาจอนุมัติทุก tier |
| REASON_REQUIRED | 422 | กรุณาระบุเหตุผล |
| CANCEL_BLOCKED_DOWNSTREAM | 409 | มี GRN/AP แล้ว ยกเลิกไม่ได้ |

## §5.7 Data Classification Enforcement (D-CLASS)
- **Confidential** (unit_price, grand_total, vendor_tax_id, payment_term, discount): role-restricted API; **mask ใน list view** (เห็นเต็มใน detail ตาม role จัดซื้อ/บัญชี); full audit ทุกการเข้าถึง/แก้
- **Internal** (default): tenant row-level + role auth
- **Restricted:** ไม่มีในรอบนี้ → ไม่ต้อง wire Restricted Resources (ดู 00 §0.7.1)
- vendor_tax_id (PII) → masking pattern + PDPA audit (C-05/C-06)
