# 06_TESTS — F-VENDOR-PRICELIST-001 Vendor Price List

> Audience: QA. Acceptance per FR + DoD. ใช้คู่กับ frd-qa-generator (→ SCN/TC/DATA/CSV).

## §6.1 Acceptance Tests
| TC | Given | When | Then | Ref |
|---|---|---|---|---|
| TC-01 | อยู่หน้าคู่ค้า (active), canManage | กด "เพิ่มสินค้า" | wizard เปิด, คู่ค้า locked, step=1 | API-05/UI |
| TC-02 | เลือกสินค้าที่คู่ค้านี้มีแล้ว | next/save | block ERR_DUPLICATE_VENDOR_PRODUCT | R01/VR01 |
| TC-03 | สินค้าไม่ purchasable | เลือก | ไม่แสดง/บล็อก | R03/VR02 |
| TC-04 | tier 1–5 และ 4–7 | save | block ERR_TIER_OVERLAP | R08/VR06 |
| TC-05 | price=0 | save | block ERR_PRICE_NONPOSITIVE | R04/VR05 |
| TC-06 | ไม่กรอก valid_from | save | block ERR_VALID_FROM_REQUIRED | R10/VR07 |
| TC-07 | กรอกครบถูกต้อง | สร้าง | item status=active, version=1, tiers persisted | API-05 |
| TC-08 | batch: เลือกคู่ค้า + 3 แถว (1 ว่าง, 1 ราคาว่าง, 1 ครบ) | บันทึกทั้งหมด | created=1, skipped=1(ว่าง), error=1(ราคา) | API-07/E05 |
| TC-09 | CSV มี product_code ไม่พบใน master | upload | unmatched +1, แถวนั้นข้าม | API-08/E06 |
| TC-10 | price change +3% (threshold=5%) | submit | applied ทันที + history(applied) | R11/API-09 |
| TC-11 | price change +12% (threshold=5%) | submit | status=pending_approval + pending บันทึก | R11/API-09 |
| TC-12 | price change ไม่ใส่เหตุผล | submit | block ERR_REASON_REQUIRED | VR08/E07 |
| TC-13 | มี pending ค้าง | submit change ใหม่ | block ERR_PENDING_EXISTS | E12/VR10 |
| TC-14 | ผู้ขอ = ผู้อนุมัติ | approve | block ERR_SOD_SELF_APPROVAL | R12/VR09 |
| TC-15 | approver ≠ ผู้ขอ, มี pending | approve | price ใหม่ apply + history(approved) + clear pending + status=active | API-10 |
| TC-16 | reject pending | approve(reject) | คงราคาเดิม + history(rejected) + clear pending | API-10 |
| TC-17 | toggle ปิดรายการ | status=inactive | item inactive, ถูกตัดจาก get-price/compare | E13/API-11 |
| TC-18 | compare product มี 3 คู่ค้า (1 blocked) | qty=100 | คืน 2 คู่ค้า เรียง net/unit THB ↑, ตัวแรก cheapest | R14/R15/API-12 |
| TC-19 | get-price product+vendor+qty (tier ตรง validity) | call | คืน net ต่ำสุดที่ qty | R16/API-13 |
| TC-20 | get-price แต่ทุก tier หมดอายุ | call | ERR_NO_ACTIVE_PRICE | E14/API-13 |
| TC-21 | role = Other (ไม่มีสิทธิ์ราคา) | เปิด list/view | ราคาทั้งหมด = ••• | R13/§5.7 |
| TC-22 | role = Finance | เปิด list | เห็นราคาจริง | R13 |
| TC-23 | edit ขณะ record ถูกแก้โดยผู้อื่น | save (version เก่า) | block ERR_VERSION_CONFLICT | E11/VR11 |
| TC-24 | FX rate ของ USD หาย | compare | fallback + flag (ไม่ crash) | E10 |

## §6.2 Engine Unit Tests
| TC | Engine | Input | Expected |
|---|---|---|---|
| ENG-T1 | landed-price | price=100, per=1, disc=10, freight=5 | net=95 |
| ENG-T2 | landed-price | price=50, per=2, disc=0, freight=0 | net=25 |
| ENG-T3 | price-select | tiers[1–99=12, 100–499=10.5, 500–∞=9.5], qty=200 | tier 100–499, net=10.5 |
| ENG-T4 | price-select | qty นอกทุก tier / หมดอายุ | null |
| ENG-T5 | fx-normalize | 100 USD @36.5 | 3650 THB |
| ENG-T6 | doa-threshold | old=100,new=112,threshold=5 | requires_approval=true, pct=12 |

## §6.3 Definition of Done (DoD)
- [ ] ทุก API contract (01–13) implemented + role-gated + tenant RLS
- [ ] get-price (API-13) คืนผลถูกต้อง + PR/PO เรียกได้ (contract stable)
- [ ] Confidential mask ทำงานทุก layer (UI/API/export/log) ตาม §5.7
- [ ] SoD บังคับ (approver≠requester) + WORM history insert-only
- [ ] Tier overlap / price>0 / valid_from / UNIQUE บังคับครบ
- [ ] Optimistic lock (version/If-Match) บนทุก mutation
- [ ] DOA threshold = config (ไม่ hardcode) + TODO wiring Policy Center (Phase 2)
- [ ] Engines pure (no HTTP) + unit tests ENG-T1..T6 ผ่าน
- [ ] Acceptance TC-01..24 ผ่าน
