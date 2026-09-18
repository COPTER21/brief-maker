# FUNCTION_CHECKLIST — F-INV · Stock by Location

> ติ๊กตามได้ทั้ง wireframe → dev → QA · อ้าง PREBRIEF_F-INV_Stock-by-Location.md
> สถานะปัจจุบัน: ทุกข้อ implement + E2E ผ่านแล้วใน `f-inv.html` (2026-08-09/10)

## A. List — ตามสินค้า (aggregate)
- [x] FN-01 Stat 4 ใบ: สินค้า(SKU) / ต่ำกว่าขั้นต่ำ / สต็อกติดลบ / ตำแหน่ง HOLD — 3 ใบแรกกดกรอง (toggle)
- [x] FN-02 ตาราง 1 สินค้า 1 แถว: สินค้า | คงเหลือ | จองแล้ว | พร้อมใช้ | สถานะสต็อก (คอลัมน์เลข 130/110/110 + สถานะ 135)
- [x] FN-03 กรอง service (SV) ออกทุกจุด — guard `isStockable` ชั้นจอ + BACKEND exclude ตั้งแต่ query
- [x] FN-04 สถานะสั้น 3 ค่า: ปกติ / ต้องเติม / ขาดสต็อก (chip form เดียว dot+คำ สูง 23px เท่ากัน)
- [x] FN-05 รหัสอ้างอิง 2 ชุด (กลาง+เก่า) — ไม่มี code_item/code_sku ทุกจอ + search index
- [x] FN-22 ค้นหา (กลาง/เก่า/ชื่อ) + ซ่อนสต็อก 0 + รีเซ็ต + sort ด้วยค่าฐาน + pagination

## B. Product Drawer
- [x] FN-06 Tabs บนสุดนอก body · full-width · [ภาพรวม default | ตำแหน่งจัดเก็บ | การเคลื่อนไหว] · route `/sku/{pid}` refresh-safe
- [x] FN-07 ภาพรวม: สรุป 3 ใบฐาน + note ติดลบ/ต่ำกว่าขั้นต่ำ + การแปลงหน่วย + รายละเอียด (threshold·FIFO·ล่าสุด) + รหัส 2 ชุด — ไม่มี hint
- [x] FN-08 ตำแหน่งจัดเก็บ: จำนวนตามหน่วย loc · จอง/ว่าง/รวม เป็นฐานทั้งคอลัมน์ (Σ ตรงสรุป) — ไม่มี h3 ซ้ำ/คำอธิบาย
- [x] FN-09 Low stock: badge+stat+note — เทียบ "พร้อมใช้" กับ `min_stock` จาก Item Master (ไม่ตั้ง = ไม่เช็ค)
- [x] FN-10 การเคลื่อนไหว: merge ทุก balance ของสินค้า + `@ ตำแหน่ง` + ใหม่สุดก่อน (30 รายการแรก)
- [x] Header: pill "Master หยุดใช้งาน" ข้าง title · ปุ่มปรับสต็อก → divider → X (icon-btn · #31)

## C. View ตามตำแหน่ง + Loc/Balance Drawer
- [x] FN-11 การ์ดต่อตำแหน่ง + utilization bar (ไม่มี dev note)
- [x] FN-12 Loc drawer: "สิ่งที่อยู่ในตำแหน่งนี้" แสดงตามหน่วยของ loc + ฐานกำกับ f>1 · เจาะเป็น balance drawer (`/sku/S{id}`) ได้
- [x] Balance drawer เดิม: ov-stats หน่วย loc + uomloc/moves tab — hint ตัดครบ

## D. Manual Adjustment
- [x] FN-13 Modal กว้าง min(1440, 100vw−48) · line editor grid v8 B2: หัวคอลัมน์ สินค้า(360+)|ตำแหน่ง(320+)|ปรับ|จำนวน|คงเหลือ|ลบ
- [x] FN-14 เหตุผลบังคับ (6 ค่า) + หมายเหตุ + เพิ่ม/ลบบรรทัด (บรรทัดสุดท้ายลบไม่ได้)
- [x] FN-15 Validation ต่อบรรทัด live: จำนวนเต็ม>0 · ลดไม่เกิน on_hand−allocated ("ลดได้สูงสุด X") · loc ล็อก BP/blocked/frozen · master inactive · SV block — บรรทัด error = ใบไม่ผ่าน
- [x] FN-16 คงเหลือ live "ปัจจุบัน n → หลังปรับ m" (หน่วยตาม loc)
- [x] FN-17 **เพิ่มเข้าตำแหน่งว่าง**: dropdown ระบุ "· ว่าง — เพิ่มเข้าได้/· มีของ/· ล็อกอยู่" (ค้นคำ "ว่าง" ได้) + label "รายการใหม่ในตำแหน่งนี้" + submit สร้าง balance ใหม่
- [x] Summary bar: พร้อมบันทึก n/m · เพิ่มรวม +x ฐาน · ลดรวม −y ฐาน · รายการใหม่ z ตำแหน่ง
- [x] FN-18 บันทึก → RAW update + ADJ doc (append-only, before/after ฐาน) + movement ต่อ balance + toast เลขเอกสาร
- [x] FN-19 RBAC: ปุ่ม+action เฉพาะ warehouse_staff/finance (BACKEND: Policy Center)

## E. ระบบร่วม
- [x] FN-20 **#95 Overlay Portal** ทุก dropdown: portal ท้าย body + fixed + flip + คลิกนอกปิด (capture) + **Esc chain**: ①ปิด dd ②ปิด modal · `render()` เคลียร์ portal กัน orphan
- [x] FN-21 **#67.1**: ไม่มี hint/คำอธิบายสอนใช้ทุกจอ (คงเฉพาะ business alert: ติดลบ/ต่ำกว่าขั้นต่ำ)
- [x] FN-23 Break/Pack: picker กรอง SV · order active ล็อก loc (badge นับ) · movement แยก
- [x] FN-30 Edge: (pid,loc) unique · negative เฉพาะ EC-07 · bucketsFor Σ(n×f)=on_hand ทุกแถว · stat คำนวณจริงไม่ hardcode
- [x] FN-40 Gate: `node --check` ✓ · audit navy=0/console=0/hint=0 ✓ · Playwright E2E สะสม 60+ เคส PASS ✓ · md5 ship ✓

## หนี้ / รอเคาะ
- [ ] OQ-INV-01..05 (ดู PREBRIEF §6) — ก่อน dev handoff
- [ ] FRD/ENC pack (Navy) **stale** — regen จาก HTML ปัจจุบันเมื่อ OQ เคาะแล้ว
