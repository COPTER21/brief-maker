# Pending Registry — F-HR-RECRUIT (สำเนาเฉพาะ feature)

> คัดเฉพาะรายการของ F-HR-RECRUIT จากทะเบียนกลาง `outputs/_SHARED/DESIGN_SYSTEM_PENDING.md`
> (ต้นทางคือทะเบียนกลาง — ใบนี้ไว้ให้ dev/BA เห็นในชุด handoff)

| ID | วันที่ | ประเภท | รายละเอียด | หลักฐาน | สถานะ |
|---|---|---|---|---|---|
| DSP-01 | 2026-09-03 | BASE-KIT z-index | `.modal-backdrop` ใน BASE-KIT ใช้ `var(--z-backdrop)` (50) → modal ที่เปิด**ในลิ้นชัก (drawer z=55)** จมใต้ drawer มองไม่เห็น/กดไม่ได้ · ผู้ใช้เจอเอง ตัววัดเดิมจับไม่ได้ | แก้ที่ `สรรหา.html` (`.modal-backdrop{z-index:var(--z-portal)}`=60) · เพิ่มตัวตรวจ `JS_MODAL_UNDER_DRAWER` เข้า `outputs/_SHARED/_e2e/uikit.py` (พิสูจน์ย้อนโค้ดพังแล้วจับได้ · C3.8) · e2e case `c_modal_z` (UI-REG) | **รอเจ้าของ design system** แก้ที่ BASE-KIT ต้นทาง (ตอนนี้แก้เฉพาะสำเนา feature) |
