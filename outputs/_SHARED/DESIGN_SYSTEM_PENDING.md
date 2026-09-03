# Design System Pending Registry

บันทึกปัญหา BASE-KIT, CI token และข้อเสนอที่ต้องส่งกลับเจ้าของ design system
โดยเก็บหลักฐานจากตัวตรวจและตำแหน่ง artifact ที่พบจริง

| ID | วันที่ | Feature | ประเภท | รายละเอียด | หลักฐาน | สถานะ |
|---|---|---|---|---|---|---|
| DSP-01 | 2026-09-03 | F-HR-RECRUIT | BASE-KIT z-index | `.modal-backdrop` ใน BASE-KIT ใช้ `var(--z-backdrop)` (50) → modal ที่เปิด**ในลิ้นชัก (drawer z=55)** จมอยู่ใต้ drawer มองไม่เห็น/กดไม่ได้ · ผู้ใช้เจอเอง ตัววัดเดิมจับไม่ได้ | แก้ที่ `outputs/F-HR-RECRUIT/สรรหา.html` (`.modal-backdrop{z-index:var(--z-portal)}` =60) · เพิ่มตัวตรวจ `JS_MODAL_UNDER_DRAWER` เข้า `outputs/_SHARED/_e2e/uikit.py` (assert modal z > drawer z ขณะเปิดซ้อน · พิสูจน์ด้วยการย้อนโค้ดพังแล้วจับได้ · C3.8) · e2e case `c_modal_z` (UI-REG) | **รอเจ้าของ design system** แก้ที่ BASE-KIT ต้นทาง (ตอนนี้แก้เฉพาะสำเนา feature — จุดเดียวกันจะหลุดใน feature ถัดไปถ้าไม่แก้ต้นทาง) · เชื่อม [[html-v7-basekit-latent-bugs]] |

