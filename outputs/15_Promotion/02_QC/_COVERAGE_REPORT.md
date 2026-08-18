# Coverage Report — F-SALES-PROMO (รอบ 1: HTML)

- วันที่ตรวจ: 18 สิงหาคม 2569
- Contract: `PREBRIEF_F-SALES-PROMO_Promotion.md` + `FUNCTION_CHECKLIST_F-SALES-PROMO_Promotion.md`
- Artifact: `outputs/15_Promotion/Promotion.html`
- Seed: `Pack Brief Feature/Promotion/f-promotion.html` เป็นฐาน; output มี surgical fixes จาก manual test

## Verdict: 🟢 FUNCTIONAL COVERAGE PASS

E2E ครอบ FN 38/38 และผ่าน 38/38 สองรอบ, console error 0 โดยทดสอบกับ DOM/function ของ seed จริง ไม่ใช่ selector จาก UI ฉบับอื่น

## Coverage Matrix

| FN | ผล | Evidence ใน HTML / E2E |
|---|---:|---|
| FN-01–03 | ✓ | `openCreate()`, `formDrawer()`, `.d-stepper`, `fSetType()`, `fSetScope()`, `comboSpec('scoperef')` |
| FN-04–07 | ✓ | `ruleEditor()` ครบ `LINE_DISC`, `FREE_GOODS`, `THRESHOLD`, `BUNDLE`; E2E เปิด editor จริงและเพิ่ม tier |
| FN-08 | ✓ | `formErrors()`, `ruleErrors()`; E2E วันย้อนหลัง+coupon ผิดและยืนยันว่าไปต่อไม่ได้ |
| FN-09 | ✓ | `renderModal()` submit มี summary 4 ช่อง + 2 ordered slots; ไม่เลือกคนถูก block |
| FN-10 | ✓ | pending drawer ไม่มีปุ่มแก้ไข; tab info แสดง assignee ที่ freeze แล้วครบสองขั้น |
| FN-11–12 | ✓ | `canActStep()`, `confirmApprove()` และ action เฉพาะผู้อนุมัติปัจจุบัน |
| FN-13 | ✓ | E2E ไม่อนุมัติโดยไม่มีเหตุผลถูก block แล้วกรอกเหตุผลกลับเป็น draft |
| FN-14 | ✓ | `comboSpec('slot-*')` ตัด `ME.name`; E2E ตรวจ option จริง |
| FN-15–16 | ✓ | `overlaps()`, overlap note/ack และ `overlapAck`; E2E บังคับช่วงเวลาทับเพื่อทดสอบ branch จริง |
| FN-17 | ✓ | `dupP()`; E2E ตรวจชื่อสำเนา, coupon ว่าง, วันเริ่มวันนี้ และ mode=create |
| FN-18 | ✓ | `calcPromo()` คืน line discount และ GL 4110-02 จากบรรทัดที่เข้าเงื่อนไข |
| FN-19 | ✓ | simulator แสดงของแถม 0.00; เพิ่ม/ลบบรรทัดได้; coupon/qty พิมพ์ต่อเนื่องไม่หลุด focus; ตาราง 7 คอลัมน์ไม่ทับ; dropdown เพิ่มสินค้า scroll ได้; engine รวม base qty |
| FN-20 | ✓ | E2E คำนวณ threshold และเลือก tier 50,000 ซึ่งเป็นขั้นสูงสุดที่ถึง |
| FN-21 | ✓ | E2E เปิด bundle candidate แล้วตรวจ limiting item ได้ 2 ชุด |
| FN-22 | ✓ | E2E ยืนยัน coupon ตัวเล็กติดและ coupon ว่างถูกข้ามพร้อมเหตุ |
| FN-23 | ✓ | candidates sort ตาม priority; `exclusive` ตั้ง `stopped` และบันทึก skip reason |
| FN-24 | ✓ | E2E ส่ง `promoAllowed:false` แล้วได้เหตุผล “ไม่ลดซ้ำ” |
| FN-31 | ✓ | E2E จำลอง `usage.byCust` ครบ quota แล้วได้ skip reason |
| FN-25–26 | ✓ | usage tab แสดง GL/ของแถม 0 บาท/ตัดสต๊อก, uses, discount, customers, budget และคงเหลือ |
| FN-27 | ✓ | `pStatus()` exhausted, progress warning ≥90%, budget guard ก่อน apply |
| FN-28 | ✓ | E2E กรอกเหตุผลระงับ → paused → เปิดต่อกลับ active |
| FN-29 | ✓ | E2E modal เหตุผล+วันมีผล แล้วปิดก่อนกำหนดเป็น ended |
| FN-30 | ✓ | action แสดงเฉพาะ draft/pending; E2E กรอกเหตุผลและยกเลิก draft |
| FN-90 | ✓ | 7 tabs, 7 rows, search coupon, type filter, scope filter ทุกขอบเขต/ทุกลูกค้า/group/channel, sort, empty state; ใช้ `any` แยกจาก scope `all`; expiring hook 14 วันอยู่ใน `isExpiring()` |
| FN-91 | ✓ | `viewDrawer()` มี 4 `.dtab` และ `.fact-grid .fact` 6 ช่อง |
| FN-92 | ✓ | `exportCsv()` ใช้ `filtered()` |
| FN-93 | ✓ | validation + `state.busy`/disabled guard |
| FN-94 | ✓ | append-only `.audit-timeline .tl-i`; ไม่มี control ลบประวัติ; เส้นตรงกึ่งกลางจุด |
| FN-95 | ✓ | Escape chain, backdrop, `#dd-portal`, `renderPortal()`; scroll ภายใน menu ไม่ถูก render ทับ |
| FN-96 | ✓ | approval tab แสดง `.emp-av`, ตำแหน่ง และชื่อครบสองขั้น; timeline geometry ผ่าน |

## Cross-feature / Scope Guard

- ราคา: Sales Price List → Trade Agreement → Promotion ตาม `CFG.applyOrder`
- scope อ้าง Customer Group และ Sales Channel; ไม่มีลูกค้าเฉพาะราย
- สินค้า/หน่วยมาจาก mock Item Master
- GL เลือกจาก mock GL Posting Group
- DOA ตามลำดับตำแหน่ง ไม่มีวงเงิน
- Quotation/Sales Order เป็น consumer ในอนาคต; Promotion ไม่ทำ stock check ของของแถม
- ไม่มี loyalty, Campaign Management, auto-cancel โปรเดิม, document running number หรือ notification declaration เพิ่มเอง

## Gate Note

Coverage เชิงพฤติกรรมผ่าน แต่ UX report ยังเก็บ V8 conformance findings ของ seed เป็น WARN และไม่ได้ซ่อนว่า self-audit ยังไม่ผ่านศูนย์
