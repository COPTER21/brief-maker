# 05_RULES — F-VENDOR-PRICELIST-001 Vendor Price List

> Audience: BE + QA. Business Rules + Validation + Edge Cases + Errors + Data Classification enforcement.

## §5.1 Business Rules (from BRD §9)
| Rule | Statement | Tag | Enforced in |
|---|---|---|---|
| R01 | 1 คู่ค้า–สินค้า = 1 รายการ (UNIQUE) | FIXED | DB uq + FN-03 |
| R02 | คู่ค้า status=active เท่านั้น | FIXED | FN-03 |
| R03 | สินค้า purchasable=true | FIXED | FN-03 |
| R04 | ราคา > 0 | FIXED | FN-04 |
| R05 | currency default = vendor.currency | CONFIGURABLE | API-05 default |
| R06 | buy_uom ∈ product buy uoms | FIXED | FN-03 |
| R07 | tax_code default = product.vat_group; GL resolve ที่ Finance Posting Setup | FIXED | API-05 default / ref |
| R08 | Tier: เรียง min↑, ห้าม overlap, เฉพาะ tier สุดท้าย max=∞ | FIXED | FN-04 |
| R09 | net/unit = (price÷per − disc + freight) ex-VAT | DYNAMIC | ENG-VPL-02 |
| R10 | valid_from required; valid_until เว้น=ไม่มีกำหนด | CONFIGURABLE | FN-04 |
| R11 | price change > THRESHOLD% → pending_approval; ≤ → auto | CONFIGURABLE | ENG-VPL-04 (config threshold, OQ1) |
| R12 | SoD: approver ≠ requester | FIXED | FN-08 |
| R13 | pricing = Confidential — mask ••• ถ้า role ∉ {proc,finance,admin} | FIXED | FN-12 (§5.7) |
| R14 | คู่ค้า blocked/blacklisted ตัดจาก compare | FIXED | API-12 / ENG-VPL-01 caller |
| R15 | compare normalize → THB @ FX; tier @ qty | DYNAMIC | ENG-VPL-03/-01 |
| R16 | get-price = net ต่ำสุดที่ qty ภายใน validity | DYNAMIC | ENG-VPL-01 |
| R17 | price change → history WORM (old/new/pct/by/at/reason) | FIXED | FN-07/-08 → T_history |
| R18 | SLA อนุมัติเปลี่ยนราคา | WARNING | ⚠️ OQ2 |

## §5.2 Validation Rules
| VR | Field/Action | Condition | Type | Message | Error code |
|---|---|---|---|---|---|
| VR01 | vendor+product | UNIQUE | Error | "คู่ค้า–สินค้านี้มีรายการแล้ว" | ERR_DUPLICATE_VENDOR_PRODUCT |
| VR02 | product | purchasable | Error | "สินค้าไม่ใช่ purchasable" | ERR_NOT_PURCHASABLE |
| VR03 | vendor | active | Error | "คู่ค้าไม่ active" | ERR_VENDOR_INACTIVE |
| VR04 | buy_uom | ∈ buy uoms | Error | "หน่วยไม่ใช่หน่วยซื้อของสินค้า" | ERR_UOM_INVALID |
| VR05 | price | > 0 | Error | "ราคาต้อง > 0" | ERR_PRICE_NONPOSITIVE |
| VR06 | tiers | ไม่ overlap + เรียง | Error | "ช่วงปริมาณ (tier) ซ้อนทับกัน" | ERR_TIER_OVERLAP |
| VR07 | valid_from | required | Error | "กรุณาระบุวันเริ่มราคา" | ERR_VALID_FROM_REQUIRED |
| VR08 | price-change reason | required | Error | "กรุณาระบุเหตุผล" | ERR_REASON_REQUIRED |
| VR09 | approve | approver ≠ requester | Error | "ผู้อนุมัติต้องไม่ใช่ผู้ขอ (SoD)" | ERR_SOD_SELF_APPROVAL |
| VR10 | price-change | no pending exists | Error | "มีคำขอเปลี่ยนราคาค้างอยู่" | ERR_PENDING_EXISTS |
| VR11 | edit/update | version match | Error | "ข้อมูลถูกแก้โดยผู้อื่น" | ERR_VERSION_CONFLICT |

## §5.3 Edge Cases (from BRD §10)
| EC | Scenario | Handling |
|---|---|---|
| E01 | เลือกคู่ค้า–สินค้าที่มีแล้ว | block UNIQUE (VR01) |
| E02 | คู่ค้าไม่ active | ไม่แสดงใน selector / block (VR03) |
| E03 | tier overlap | block (VR06) |
| E04 | ราคา ≤ 0 | block (VR05) |
| E05 | batch แถวว่าง/ไม่ครบ | ว่าง→ข้าม; ไม่ครบ→แดง+block save |
| E06 | CSV code ไม่พบใน master | นับ unmatched + ข้ามแถว (FN-06) |
| E07 | price change ไม่ใส่เหตุผล | block (VR08) |
| E08 | อนุมัติคำขอตัวเอง | block SoD (VR09) |
| E09 | disc>100% / net ติดลบ | clamp/ block (ENG-VPL-02 validate) |
| E10 | FX rate หาย | fallback rate ล่าสุด + flag (ENG-VPL-03) |
| E11 | concurrent edit | optimistic lock version/If-Match (VR11) |
| E12 | price change ขณะมี pending | block (VR10) |
| E13 | inactive item ใน get-price/compare | ตัดออก |
| E14 | ทุก tier หมดอายุ | get-price → ERR_NO_ACTIVE_PRICE |
| E15 | Confidential รั่วใน export/log | mask ทุก layer (§5.7) |
| E16 | role ไม่มีสิทธิ์เห็นราคา ใน compare/autofill | คืนค่าใช้งานได้แต่ UI mask |

## §5.4 Error Catalog
ดู 02_API §2.3 (รวม VR error codes ข้างบน) + ENG errors: ENG_ERR_NO_ACTIVE_PRICE, ENG_ERR_INVALID_INPUT, ENG_ERR_FX_RATE_MISSING.

## §5.5 State Machine (item)
active → inactive (toggle) · inactive → active · active → pending_approval (change>threshold) · pending_approval → active (approve/reject). Tier status (active/expired/pending) = derived จาก validity.

## §5.6 Threshold / Config
| Key | Default | Owner | Note |
|---|---|---|---|
| price_change_threshold_pct | TBD (OQ1) | Admin/Policy | ENG-VPL-04; Phase 2 → DOA |
| default_currency_source | vendor | Admin | R05 |
| approval_sla | TBD (OQ2) | Proc. Director | R18 |

## §5.7 Data Classification Enforcement (D-CLASS) ⭐
- **Confidential fields:** price, discount_pct, freight, net_unit (derived), old/new_price, pct, pending.
- **Allowed roles (เห็นไม่ mask):** Procurement (Officer/Manager/Director), Finance, Admin.
- **Enforcement:**
  - **UI:** ค่าเงินทั้งหมด render ผ่าน mask → `•••` ถ้า role ไม่อยู่ใน allowed (FN-12).
  - **API:** response มาส์กฝั่ง server (API-01/03/04/12) — ห้ามส่งตัวเลขจริงให้ client ที่ไม่มีสิทธิ์.
  - **get-price (API-13):** สำหรับ PR/PO service → คืนตัวเลขจริง (machine path) แต่ UI ปลายทางต้อง mask ตาม role ผู้ใช้ (E16).
  - **Export/Log:** export ราคา/print → mask ตาม role; audit log อ่านราคา = sensitive (log access).
- **Restricted reconciliation (OQ4):** ถ้า Policy Center ตัดสินให้ราคา = **Restricted** → ต้อง register Restricted Resources + access-request flow (เข้มกว่า mask). จนกว่าจะสรุป → Confidential เป็น baseline.
