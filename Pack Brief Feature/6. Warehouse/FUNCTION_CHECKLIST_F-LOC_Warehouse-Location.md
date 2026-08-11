# FUNCTION_CHECKLIST — F-LOC · Warehouse Location Hierarchy

> อ้าง PREBRIEF_F-LOC_Warehouse-Location.md · สถานะ: implement + E2E ~25 เคสผ่านแล้วใน `f-loc.html` (2026-08-10)

## A. โครงสร้าง & Navigation
- [x] FN-01 Drill 5 ระดับ WH→Zone→Area(→Rack)→Location + breadcrumb chip + stat 5 ใบ
- [x] FN-02 **Flat "Location ทั้งหมด"** — stat card กดได้ → ตารางแบนข้ามชั้น + คอลัมน์ path ย่อ + ค้น/กรอง (OB-10)
- [x] FN-03 Area tab: Racks / Location ตรง (flexible parent)
- [x] FN-04 Hierarchy view: tree + node summary แชร์ state — **#96 full-height** (calc(100vh−330) floor 420, scroll ภายใน) — NON-STANDARD ติด OQ-LOC-02
- [x] FN-50 CI Warm Light + Satoshi + inline sprite 75 (no CDN) + no-hint + Rule #40 (รหัส|ชื่อ แยกคอลัมน์, ตัด avatar) + #51 form grid 2 คอลัมน์ + drawer 680

## B. CRUD
- [x] FN-05 Warehouse form: geo cascade จังหวัด→อำเภอ→ตำบล→ไปรษณีย์ auto (readonly, ไม่มี placeholder) · เปลี่ยนชั้นบนล้างชั้นล่าง
- [x] FN-10 Zone: temp_controlled + ช่วงอุณหภูมิ · Area: allows_direct toggle · Rack: R×C×L
- [x] FN-13 Location wizard 2 ขั้น: parent XOR + ประเภท 10 ค่า + พิกัด + behavior flags
- [x] FN-14 Validation: code unique ใน parent · parent=area ต้อง allows_direct
- [x] FN-15 **storage_uom** บังคับ (STORAGE_UOMS 7 ค่า) · **ล็อกเมื่อ hasStock** + ข้อความ "1 ตำแหน่ง 1 หน่วย" `[AI-DRAFT OQ-LOC-06]` · แสดง list column + view drawer (ภาพรวม + tab ความจุ) · mock sync F-INV
- [x] FN-16 View drawer: full path + ข้อมูลระดับ + รายการลูก + audit

## C. สถานะ & Bulk (จอปฏิบัติงาน)
- [x] FN-20 **statusMenu**: คลิก pill → portal menu (fixed+flip, คลิกนอกปิด capture) เลือก active/inactive/blocked/frozen — full ไม่ให้ตั้งมือ
- [x] FN-21 blocked/frozen → modal บังคับเหตุผล (inner-content pattern ของ modal กลาง) → apply + audit + toast
- [x] FN-22 **Bulk select**: checkbox (flat + rack + direct list) + bulk bar — สถานะ 4 ค่า (เหตุผลครั้งเดียวทั้งชุด) + **ตั้งหน่วยเก็บข้าม hasStock พร้อมนับแจ้ง** + ล้างที่เลือก
- [x] FN-23 ทุก mutation ลง audit ต่อ node (append-only)

## D. สร้างเร็ว
- [x] FN-30 **Bulk generation**: preset 3 (Rack มาตรฐาน / Aisle-Bay-Level / ชั้นเรียบ) + custom pattern + **live preview ชื่อ 5 ตัวแรก + จำนวนรวม** + storage_uom ใช้ทุกตัว + atomic
- [x] FN-31 **Quick add row** (rack + area direct): รหัส+ประเภท+หน่วยเก็บ → เพิ่มทันที (default cap) + กันซ้ำ + audit

## E. Guards
- [x] FN-40 RBAC: จัดการได้เฉพาะ role manage (canManage) — ไม่มี DOA (LD-07)
- [x] FN-41 ลบ = confirm modal · มีสต็อก/มีลูก active → block (default OQ-LOC-04)
- [x] FN-60 Gate: node --check ✓ · audit navy=0 console=0 cdn=0 hint=0 avatar=0 540px=0 ✓ · E2E ~25 PASS ✓ · md5 ship ✓

## หนี้ / รอเคาะ
- [ ] OQ-LOC-01..06 (PREBRIEF §6) — ก่อน dev handoff · OQ-LOC-02 tree (Chin) · OQ-LOC-06 โยง OQ-INV-03
- [ ] แจ้ง Architect: ENG-LOC-GEN + ENG-HIER-PATH
- [ ] FRD FULL 9 ไฟล์ (Navy) stale — regen + review delete/decommission state machine ลึกตอน regen
