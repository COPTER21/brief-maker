# Page Anatomy — Composition Recipes (#70–#73) — v6.5

> เกิดจากการเทียบไฟล์เลน (audit ศูนย์ — ถูกแต่จืด) กับไฟล์ vibe ที่ user ชอบกว่า:
> ต่างกันที่ **ความรวยของ composition** ไม่ใช่ความถูก — วัดได้: stat cards 1 vs 22 · chips 3 vs 24 · sortable 0 vs มี
> หมวดนี้สั่ง "ขั้นต่ำของความรวย" ต่อ pattern — ทุกข้อนับได้ ตรวจได้ เหมือนกฎอื่น
> ⚠️ ความรวย ≠ ขยายฟอนต์/ระยะ — density ยังยึด #63 เป๊ะ (รวยด้วย element ไม่ใช่ด้วยขนาด)

---

## Rule #70 — List Page Anatomy (Pattern A ทุกหน้า)
โครงบังคับจากบนลงล่าง — ขาดชั้นไหน = WARN, ขาด ≥2 ชั้น = BLOCK:
1. **Page header:** title + จำนวนรวม ("ทะเบียนสินค้า · 128 รายการ") + ปุ่ม primary + secondary (export ฯลฯ)
2. **Stat summary row (บังคับ ≥4 ใบ):** การ์ดสรุปมิติสำคัญจาก mock data จริง — นับตามสถานะ/ประเภท/
   ค่าที่ business สนใจ (เช่น ใช้งาน · ร่าง · รออนุมัติ · ต่ำกว่า min) · **คลิกการ์ด = filter ตาราง** ·
   ตัวเลขต้องตรงกับข้อมูลในตารางจริง (ห้ามเลขมั่ว — TC จะจับ)
3. **Toolbar:** search + filter chips/tabs **พร้อมตัวเลขนับต่อ chip** ("ทั้งหมด 128 · ใช้งาน 96 · ร่าง 12")
4. **ตาราง:** หัวคอลัมน์หลัก **sortable + ลูกศรบอกทิศ** · เซลล์ entity = 2 บรรทัด (ชื่อ 13px + code/รอง
   12px mute) · สถานะ = pill มีสีตาม semantic · ตัวเลขชิดขวา tabular-nums · action ท้ายแถว
5. **Footer:** pagination + "แสดง x–y จาก z"

## Rule #71 — Form/Wizard Anatomy
- ฟอร์มยาว: แบ่ง **section card** — แต่ละ section มี icon + หัวข้อ + คำอธิบายสั้น 1 บรรทัด (≤60 chars — เกินเข้า ⓘ)
- wizard: มี **summary panel/step review** ก่อน submit (ผู้ใช้เห็นของที่กรอกทั้งหมด) — ไม่ใช่กรอกจบแล้วยิงเลย
- field สำคัญ (รหัส, หน่วยฐาน) มี helper เชิง context: auto-gen badge, ⓘ, หรือ preview ค่า
- validation แสดง inline ใต้ field + summary บนหัวเมื่อกด submit ไม่ผ่าน

## Rule #72 — Drawer/Detail Anatomy
- header = **identity block**: avatar/thumb + ชื่อ + code + status pill (ไม่ใช่แค่ text บรรทัดเดียว)
- tabs **มีตัวเลขนับ** เมื่อเนื้อในเป็น list ("เอกสาร 4 · ประวัติ 12")
- ข้อมูลแสดงเป็น **definition grid** (label mute 11-12px / value 13px) เป็นกลุ่ม ๆ มีหัวข้อ — ไม่ใช่ p ต่อกัน
- มี timeline/audit section เมื่อ entity มี lifecycle

## Rule #73 — Interaction Richness (ขั้นต่ำ)
- หัวตาราง `is-sortable` + sort ทำงานจริงอย่างน้อยคอลัมน์หลัก (ชื่อ/code/วันที่/สถานะ)
- filter chip คลิกได้จริง + active state ชัด
- แถวตาราง hover + คลิกเปิด detail (ทั้งแถว ไม่ใช่เฉพาะปุ่มจิ๋ว)
- ทุกจำนวน/นับที่โชว์ sync กับข้อมูลจริงใน state (เปลี่ยน filter → เลขเปลี่ยนตาม)

---
### เพิ่มใน pre-flight (ต่อจากข้อ 14)
15. Pattern A: มี stat row ≥4 ใบ + chip counts + sortable headers (#70/#73)
16. wizard มี summary ก่อน submit · drawer header เป็น identity block (#71/#72)
17. ตัวเลขบน stat/chip ตรงกับ mock data จริง (สุ่มนับ 2 ค่า)
