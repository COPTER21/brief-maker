# 07_LOCKED_DECISIONS — F-VENDOR-PRICELIST-001 Vendor Price List

> Locked decisions (LD) + convention deviations. แก้ได้เฉพาะผ่าน revision ของ BRD/FRD.

## §7.1 Locked Decisions
| LD | Decision | Rationale | Source |
|---|---|---|---|
| LD-01 | **Buy-side เท่านั้น** — Sales Price List (sell-side, FK Sales Channel) แยก feature อนาคต | scope split; data model ต่างกัน | BRD §3.2 |
| LD-02 | **Batch = bulk-entry-grid (NON-STANDARD)** ไม่ใช่ wizard มาตรฐาน | ให้กรอก mass ได้เร็ว; conditions เป็น default ปรับรายตัวภายหลัง | BRD §14.6, OQ3 |
| LD-03 | **vendor-first navigation** เป็น lens ไม่ใช่ schema — data ยังเป็น vendor×product junction | ตรง SAP/D365 dual view; product-centric ยังต้องมีสำหรับ get-price/compare | BRD §3, HTML |
| LD-04 | **DOA = placeholder** (threshold% config + SoD in-feature) — ยังไม่ wire DOA engine กลาง | Phase 1 launch; Phase 2 Feature-DOA pairing ที่ Policy Center | BRD §13, OQ6 |
| LD-05 | **ราคา classification = Confidential** (baseline) | ตาม BRD R13; mask ตาม role | BRD §16, §5.7 |
| LD-06 | **ตัดทิ้ง: AVL, ราคาสัญญา/contract-lock, lead time, MOQ/MPQ, preferred vendor** | มติทีม — ลดความซับซ้อน | BRD Changelog |
| LD-07 | **create = active ทันที** (ไม่ผ่านอนุมัติตอนสร้าง); อนุมัติเฉพาะ "เปลี่ยนราคา > threshold" | ตาม HTML behavior | BRD §5, OQ5 |
| LD-08 | Wizard create = **2 ขั้น** (เชื่อมโยง / ราคา·Tier·Validity) — drawer ไม่ใช่ modal | CUBE NATIVE iron rule (drawer-not-modal) | BRD §14.6 |
| LD-09 | **search combo** สำหรับ product/vendor selector ทุกที่ (drawer/batch/filter) | UX — หาเร็ว | HTML |

## §7.2 Convention Deviations
| # | Deviation | Note |
|---|---|---|
| CD-01 | Sidebar = **232px** (ไม่ใช่ 256px ที่ FRD เก่าระบุ) | html-generator-v3 standard ปัจจุบัน = 232px; FRD F-SALES-CHANNEL-001 ที่ระบุ 256 = stale |
| CD-02 | Global Engine IDs (ENG-VPL-01..04) = **scope-local draft** | จะ assign UUID จริงตอน register CUBIC Registry |
| CD-03 | get-price (API-13) เป็น **service/machine path** — คืนราคาจริงแม้ caller ปลายทาง mask | enforcement ย้ายไป UI ปลายทาง (E16) |

## §7.3 ID Registry (this feature)
- API: F-VPL-API-01..13
- Functions: F-VPL-FN-01..12 (camelCase codes)
- Engines: ENG-VPL-01 price-select-engine · -02 landed-price-engine · -03 fx-normalize-engine · -04 doa-threshold-evaluator (kebab-case)
- Tables: T_vendor_price_item · T_vendor_price_tier · T_vendor_price_history
