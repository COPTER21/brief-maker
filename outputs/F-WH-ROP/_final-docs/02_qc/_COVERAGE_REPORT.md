# Coverage Report — F-WH-ROP (รอบ 1: HTML)

- วันที่: 2026-09-18 · PM/BA re-gate
- Contract: Cube Feature List F085 + PREBRIEF/Scope Lock ที่ sync ตามคำยืนยัน PM/BA 2026-09-17
- References: F009, F088, F090, F072, F073 และ Notification
- Artifact: `outputs/F-WH-ROP/F-WH-ROP.html`
- Checklist: FN 8 · edge/rule/scope item 16

## Verdict: 🟢 PASS

สรุป: ครอบ 16/16 · gap block 0 · gap warn 0 · NOT-CHECKED 0

## Coverage Matrix

| Item | ประเภท | HTML | Evidence / หมายเหตุ |
|---|---|---|---|
| F009 → F085 ใช้ ATP | edge in | ✓ | `ropSnapshot()` ระบุ source F009; `ropEvaluatePair()` อ่าน `snapshot.atp` โดยตรง |
| F088/F090 ผ่าน F009 | scope guard | ✓ | หน้า “ประวัติ” ระบุห้ามหัก reserved/hold ซ้ำ; ไม่มี query Quality Hold ใน feature |
| นโยบายสินค้า×คลัง | rule | ✓ | `#/records` + drawer เก็บ Min/Max/Safety/Lead Time/ADU window/Pack Size ต่อคู่ |
| Safety-driven ROP | rule | ✓ | `ropEvaluatePair()`: `rop=max(min,safety+ADU×leadTime)` และ trigger เฉพาะ `ATP < ROP`; Drawer แสดงที่มาของ 19 ครบ |
| สูตรจำนวนแนะนำ | rule | ✓ | `raw=max(0,(Max+Safety)−ATP−On-Order)` แล้ว ceil ตาม Pack Size; ITEM-101 raw 27 ปัด 12 เป็น 36 |
| รายงานใกล้จุด | rule | ✓ | `near=!triggered && ATP<=ROP×1.2`; ตารางมี ต่ำกว่าจุด/ใกล้จุด/ปกติ สีแยก และ KPI “ใกล้จุด” |
| ADU จาก F009 | rule | ✓ | `#/settings` แสดง movement ที่นับ/ไม่นับและ window 30/60/90 |
| On-Order กัน PR ซ้ำ | rule | ✓ | Drawer แสดง “PO เปิด + PR Draft”; สูตรหัก On-Order ก่อนสร้าง |
| ตรวจทุกวัน + movement | trigger | ✓ | `TRIGGER` anchor ระบุ scheduler 06:00 + GRN/Issue/Transfer/Adjust/Reserve; UI แยกเวลาตรวจอัตโนมัติกับปุ่ม manual |
| F085 → Notification | edge out | ✓ | `ropNcCandidate()` emit `reorder_point.triggered` พร้อม idempotency key |
| F085 → F072 | edge out | ✓ | `ropPreparePR()` สร้าง status `draft` และรวม lines ต่อ warehouse/evaluation round |
| F072 → DOA | scope guard | ✓ | Draft response มี `submitted:false`; UI แสดง “ยังไม่ส่งอนุมัติ”; ไม่มี auto-submit handler |
| F073 vendor flow | scope guard | ✓ | Search dropdown “ผู้ขายหลัก (ไม่บังคับ)” เก็บ `preferredVendor`; PR ไม่ split vendorและส่ง `vendor_suggests` เป็นข้อมูลเสนอ |
| Contract/CSQ declarations | integration | ✓ | HTML anchor ระบุ `master.changed → SecC` หลัง policy commit; threshold เป็น NTF และ PR lifecycle เป็นของ F072 พร้อม origin refs; F085 ไม่ประกาศ OC/DC/SC/EC/AC/FC |
| Scope isolation | scope guard | ✓ | grep `F-WH-QHOLD/F-WH-CYCLE/F-WH-LOT/F-ACC-LC` = 0; ไม่มี action ของ feature อื่น |
| Race/demo guard | UI rule | ✓ | `state._busy` ครอบ 3 action; `.demo-only` ซ่อนแล้วไม่มีข้อความ demo/mock บนจอและไม่มี body overflow |

## FN Evidence

| FN | WF | Evidence |
|---|---|---|
| FN-01 | ✓ | routes/list/filter/sort + E2E FN-01 |
| FN-02 | ✓ | policy drawer/validation/version + E2E FN-02 |
| FN-03 | ✓ | `ropPolicyActive(item,warehouse,date)` + E2E FN-03 |
| FN-04 | ✓ | Safety-driven ROP/target, ATP/ADU/On-Order, 3 statuses และ rounding + E2E FN-04 |
| FN-05 | ✓ | suggestion list/search dropdown/no-policy state + E2E FN-05 |
| FN-06 | ✓ | Notification busy state/envelope/idempotency + E2E FN-06 |
| FN-07 | ✓ | grouped Draft/preferred vendor/replay/no submit + E2E FN-07 |
| FN-08 | ✓ | recompute replay, append-only history และ demo-only guard + E2E FN-08 |

## Scope check

- ไม่มีการสร้าง PO
- ไม่มีการ submit PR เข้า DOA
- ไม่มีการ query Quality Hold หรือหัก hold ซ้ำ
- ไม่มีการ split PR ตาม vendor
- ไม่มี printable document ของ F085 จึงข้าม workflow step 2

## Gaps

ไม่มี
