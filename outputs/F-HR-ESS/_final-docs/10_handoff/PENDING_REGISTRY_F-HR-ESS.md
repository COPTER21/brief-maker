# PENDING (design-system) — เฉพาะที่เกี่ยวกับ F-HR-ESS

> คัดจากทะเบียนกลาง `outputs/_SHARED/DESIGN_SYSTEM_PENDING.md` (ต้นฉบับเต็มอยู่ที่นั่น)

- **DSP-01** (BASE-KIT z-index · modal-in-drawer) — `.modal-backdrop` ต้นทางใช้ `--z-backdrop`(50) < drawer(55) → modal จมใต้ drawer · ESS pre-wire แก้สำเนา `.modal-backdrop{z-index:var(--z-portal)}`=60 ตั้งแต่ step 1 (e2e Esc chain + qc-ux render ยืนยัน) · **รอแก้ BASE-KIT ต้นทาง** (เกิดซ้ำทุก HR feature)
- **DSP-04 (ใหม่ · ESS)** — listener click แบบ **capture-phase** ที่ document/body กลืน onclick ของ target ทั้งหน้า (การ์ด + ปุ่มยื่นคำขอ กดไม่ทำงาน · **qc-ux มองไม่เห็น**) · แก้สำเนา `}, true)`→`}, false)` + เพิ่ม uikit `assert_affordances_fire` (พิสูจน์กับเวอร์ชันพัง · C3.8) · **รอ generator/qc-ux ทบทวน pattern ต้นทาง**
