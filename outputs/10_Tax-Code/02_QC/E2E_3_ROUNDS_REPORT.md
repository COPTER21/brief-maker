# รายงานยืนยัน E2E — Tax Code HTML (3 รอบ)

วันที่ทดสอบ: 5 สิงหาคม 2026  
ไฟล์ที่ทดสอบ: `../01_HTML/TaxCode.html`  
ผลรวม: **PASS — ผ่าน 3/3 รอบ, 48/48 checks, browser page error 0 รายการ**

## วิธีทดสอบ

- รันด้วย Chromium ผ่าน Playwright ที่ viewport 1440 × 900
- แต่ละรอบเริ่มด้วย browser page ใหม่ เพื่อไม่ให้ mock state ในหน่วยความจำรั่วข้ามรอบ
- ตรวจทั้ง UI ที่ผู้ใช้เห็น, state หลังทำรายการ, permission, effective date, snapshot และ overlay behavior
- เก็บผลแบบ machine-readable ใน `E2E_3_ROUNDS_RESULT.json`

## ผลแต่ละรอบ

| รอบ | ขอบเขตหลัก | Checks | Page errors | ผล |
|---|---|---:|---:|---|
| 1 | Smoke, route, VAT/WHT list, search/filter/sort, Tax Code picker, effective date, Esc/focus | 20/20 | 0 | PASS |
| 2 | Validation, สร้าง VAT/WHT, duplicate code, draft/archive, immutable used code, replacement, deactivate, no hard delete | 15/15 | 0 | PASS |
| 3 | Permission, GL lookup contract, effective date boundaries, snapshot immutability, modal/drawer Esc chain, dropdown flip | 13/13 | 0 | PASS |

## Bug ที่พบและแก้แล้ว

### BUG-E2E-01 — Confirmation modal อยู่ใต้ view drawer

- อาการ: เมื่อกด “ปิดใช้งาน” จาก drawer ตัว drawer บัง confirmation modal ทำให้กด modal ไม่ได้
- สาเหตุ: modal backdrop มี z-index ต่ำกว่า drawer
- การแก้: กำหนด page-specific modal layer เป็น `60` เหนือ drawer layer `51`
- ผลยืนยัน: รอบ 3 อ่าน computed z-index ได้ `modal=60`, `drawer=51` และ Esc ปิด modal ก่อน drawer ถูกต้อง

### BUG-E2E-02 — วันสิ้นสุดของรหัสเดิมคลาดหนึ่งวัน

- อาการ: รหัสทดแทนเริ่ม `2027-01-01` แต่รหัสเดิมสิ้นสุดเป็น `2026-12-30` แทน `2026-12-31`
- สาเหตุ: หักวันด้วย local time แล้วแปลงเป็น UTC ทำให้เกิด timezone offset
- การแก้: แยกค่าปี/เดือน/วันและคำนวณด้วย UTC (`Date.UTC` + `setUTCDate`)
- ผลยืนยัน: รอบ 2 ตรวจรหัสเดิมสิ้นสุด `2026-12-31` และเชื่อม `replacedByTaxCodeId` ถูกต้อง

## False failures ที่แยกออกจาก product bug

- ชุดทดสอบเดิมตรวจ overlay เร็วกว่าการเปิดผ่าน `requestAnimationFrame`; ปรับให้รอ class `is-open` ก่อนตรวจและตรวจ computed z-index เพิ่มเติม
- ปุ่มบางรายการ rerender DOM ภายใน click handler ทำให้ Playwright actionability รอ element เดิมที่ถูกถอดออก; ปรับ harness ให้ dispatch event สำหรับ action ดังกล่าว โดยยังตรวจ state/result หลังทำรายการครบ

## Quality audit หลังแก้

- `self_audit.py`: PASS ทุกข้อ
- Iron Rules audit: `FAIL=0`, `WARN=3`
- WARN ทั้ง 3 รายการมาจาก base-kit/shared source ที่ถูกล็อกไว้ ไม่ใช่ defect ของ Tax Code page-specific implementation

## Environment note และขอบเขตคำยืนยัน

- Sandbox ปิด network จึงโหลด external font/Lucide CDN ไม่ได้และมี `ERR_NETWORK_ACCESS_DENIED` รอบละ 5 รายการ; เป็นข้อจำกัด environment แยกจาก browser page error และไม่ทำให้ logic/UI flow ที่ทดสอบล้มเหลว
- ผลนี้ยืนยันว่า **ไม่พบ defect คงเหลือในขอบเขต 3-round E2E ที่ระบุด้านบน** ไม่ได้หมายถึงการรับประกันว่าไม่มี bug ในทุก browser, ทุกขนาดจอ, integration กับ backend จริง หรือข้อมูล production ทุกกรณี

## หลักฐาน

- ผลละเอียด: `E2E_3_ROUNDS_RESULT.json`
- Test runner: `e2e_tax_code.py`
- ภาพรอบ 1: `e2e_shots/round1_picker_payment_snapshot.png`
- ภาพรอบ 2: `e2e_shots/round2_lifecycle_complete.png`
- ภาพรอบ 3: `e2e_shots/round3_snapshot_immutable.png`

