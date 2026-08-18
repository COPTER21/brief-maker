# UAT Lite Selection Audit — F-SALES-PROMO

## Audit Gate

- Source: `testcases-F-SALES-PROMO.md`
- Source baseline: 55 cases / 173 steps
- Kept for human UAT: 31 cases
- Original steps in kept cases: 104 steps
- UAT steps after human-friendly merge: 67 steps
- Dropped to ledger: 24 cases
- Mode: Lite
- TC IDs of every kept case are unchanged.

## Merge Note

Merged 37 atomic navigation/verification steps into adjacent human-readable steps. No distinct input, visible validation, approval transition, promotion calculation, or acceptance checkpoint was removed. The main merged patterns were: opening a drawer plus selecting its tab; clicking confirm plus waiting for the resulting status; and repeated per-option checks represented as one explicit “select each value” instruction.

## Drop Ledger

- `TC-L03` · ตัด · ตัวกรองชนิดซ้ำกับวิธีทดสอบตัวกรองขอบเขตและแต่ละชนิดถูกพิสูจน์ในเส้นสร้างจริงแล้ว
- `TC-L06` · ตัด · sort/reset เป็น interaction รอง; AI test ครอบไว้แล้วและไม่เพิ่ม acceptance สำคัญกว่าชุด Lite
- `TC-L07` · ตัด · ดาวน์โหลด CSV ถูกตรวจโดย AI; การตรวจไฟล์ดาวน์โหลดซ้ำไม่เพิ่มกฎธุรกิจหลัก
- `TC-C03` · ตัด · LINE amount/base-UOM ซ้ำกับ `TC-C01` และการคิดราคาจริงใน `TC-S01`
- `TC-C04` · ตัด · boundary เปอร์เซ็นต์/priority เป็น permutation เชิงตัวเลข; validation ตัวแทนคงอยู่ใน `TC-C02`, `TC-C07`, `TC-C09`
- `TC-C10` · ตัด · ต้องพึ่งข้อมูลคูปองซ้ำจากระบบจริง; AI test ตรวจข้อห้ามนี้โดยตรงแล้ว
- `TC-A07` · ตัด · resume เป็นคู่กลับของ pause; เก็บ pause และ end early ซึ่งเป็น acceptance ที่เสี่ยงกว่า
- `TC-A09` · ตัด · forbidden transition หลายสถานะเป็น permutation; UI จำกัดปุ่มตามสถานะและ AI test ครบทุก transition
- `TC-S03` · ตัด · explicit channel ซ้ำกับ scope checks ใน `TC-L04` และผล eligibility หลักใน simulator cases ที่เก็บ
- `TC-S04` · ตัด · date/status permutations ตรวจโดย AI; คนทดสอบคงตรวจสถานะปลายทางหลังอนุมัติใน `TC-A04`
- `TC-S07` · ตัด · below-threshold message เป็นคู่ลบของ `TC-S06`; AI test ตรวจข้อความและ boundary แล้ว
- `TC-S10` · ตัด · การไม่คิดข้อตกลงการค้าซ้ำรวมอยู่ในผลรับงาน `TC-S01`
- `TC-S12` · ตัด · ต้องเตรียมประวัติใช้สิทธิ์รายลูกค้านอก prototype; AI test ครอบ quota แล้ว
- `TC-P02` · ตัด · wrong-current-approver เป็น permission permutation; `TC-P01`, `TC-A03`, `TC-A04` ครอบสิทธิ์ที่คนสังเกตได้
- `TC-P03` · ตัด · human/service boundary ต้องจำลอง identity ฝั่งระบบ; ไม่ใช่ขั้นที่ผู้ใช้ทั่วไปทำเองได้
- `TC-X01` · ตัด · ต้องจำลองสัญญาข้อมูลจากบัญชีราคาและข้อตกลงการค้า
- `TC-X02` · ตัด · ต้องทดสอบที่ใบเสนอราคา/ใบสั่งขายซึ่งยังไม่มี artifact ในแพ็กนี้
- `TC-X03` · ตัด · ต้องจำลอง Invoice, การบันทึกบัญชี และการนับสิทธิ์ซ้ำ
- `TC-X04` · ตัด · การตรวจสต๊อกเป็นงานของใบสั่งขาย ไม่ใช่หน้าจอโปรโมชัน
- `TC-X05` · ตัด · การ freeze สายอนุมัติหลังเปลี่ยน config ต้องใช้ DOA กลางจริง
- `TC-X06` · ตัด · inactive snapshot ต้องแก้ข้อมูล master ภายนอกและตรวจสัญญาระบบ
- `TC-N01` · ตัด · stale update ต้องเปิด session แข่งกันและจำลอง version conflict
- `TC-N02` · ตัด · double-submit/idempotency เป็นความน่าเชื่อถือหลังบ้าน; AI test ครอบแล้ว
- `TC-N03` · ตัด · designed-load response ต้องใช้เครื่องมือวัดโหลด ไม่ใช่ manual UAT

## Coverage Decision

Lite UAT ยังเก็บ happy path หลักทุกแบบ (ส่วนลดสินค้า, ของแถม, ส่วนลดตามยอด, ชุดราคาพิเศษ), visible validation, approval sequence, reject/pause/end, history, coupon behavior, priority/exclusive, budget, self-approval prohibition, and signed scope locks. System-only and cross-module checks remain fully traceable in the source AI test file.
