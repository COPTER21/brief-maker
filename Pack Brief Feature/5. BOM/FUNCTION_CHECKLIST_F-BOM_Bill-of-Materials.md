# Function Checklist · BOM — สูตรการผลิต
> จาก PREBRIEF_F-BOM v1 (2026-08-09) · ทุก FN trace S-XX/BR-XX/VR-XX ได้
> WF = รีวิว HTML · DEV = พัฒนาจริง · QA = ทดสอบ — HTML as-built ผ่าน E2E 23 + vibe r3 regression 11 เคส

## หมวด 1 · สร้างสูตร (wizard 2 step)
| FN | ต้องทำอะไรได้ | trace | WF | DEV | QA |
|---|---|---|---|---|---|
| FN-01 | wizard 2 step: ① ข้อมูลสูตร ② ส่วนประกอบ · stepper บอกขั้นปัจจุบัน · ไม่มี hint/note | S-01 · OB-6 | ☐ | ☐ | ☐ |
| FN-02 | Step 1: เลือกสินค้า FG ผ่าน **combobox portal** (ค้นได้ · โชว์ **รูปสินค้า** + code + หน่วย) — เฉพาะ type FG | S-01 · BR-03 | ☐ | ☐ | ☐ |
| FN-03 | Step 1: version + ชื่อสูตร + ผลผลิต/สูตร + out_uom + toggle สูตรหลัก(★) | S-01 | ☐ | ☐ | ☐ |
| FN-04 | Step 2 line editor: **combobox portal ค้นวัตถุดิบ** (RM/PM/TR) — suggest ลอยทับตาราง ไม่ถูก clip | S-01 · OB-6 | ☐ | ☐ | ☐ |
| FN-05 | line: qty (>0) + UoM (**กรองหมวดเดียวกับวัตถุดิบ** VR-08) + scrap% + ปุ่มลบบรรทัด · spacing อ่านง่าย | S-01 · BR-06 | ☐ | ☐ | ☐ |
| FN-06 | cost rollup สด = Σ(std_cost×qty×(1+scrap%)) ต่อ 1 หน่วยผลผลิต · std_cost read-only | S-01 · BR-07/09 | ☐ | ☐ | ☐ |
| FN-07 | บันทึกร่าง / บันทึก+เปิดใช้ → record มี DOA null 4 fields + used=0 (BR-08) | S-01 · OB-3 | ☐ | ☐ | ☐ |

## หมวด 2 · สูตรหลัก + หลายสูตร
| FN | ต้องทำอะไรได้ | trace | WF | DEV | QA |
|---|---|---|---|---|---|
| FN-08 | ตั้งสูตรหลัก(★) 1 ตัว/FG — ตั้งใหม่ปลดเก่าอัตโนมัติ · badge "สูตรหลัก" ใน list + view | S-02 · BR-02 | ☐ | ☐ | ☐ |
| FN-09 | view "ภาพรวม" โชว์ทุก version ของ FG นั้น + ป้ายสูตรหลัก/สถานะ | S-03 | ☐ | ☐ | ☐ |

## หมวด 3 · แก้ไข + Validation
| FN | ต้องทำอะไรได้ | trace | WF | DEV | QA |
|---|---|---|---|---|---|
| FN-10 | แก้ได้ทุก field รวม lines แม้ used>0 (MO snapshot — BR-DEL [AI-DRAFT]) | S-04 | ☐ | ☐ | ☐ |
| FN-11 | VR-01/03: ไม่เลือก FG · ชื่อสูตรว่าง → block + toast | S-05 | ☐ | ☐ | ☐ |
| FN-12 | **VR-02: version ว่าง หรือซ้ำต่อ parent → block** (fix recheck — เดิม saveForm ไม่เช็ค) | S-05 · OB-8 | ☐ | ☐ | ☐ |
| FN-13 | VR-04/05: lines 0 · qty≤0 → block | S-05 | ☐ | ☐ | ☐ |
| FN-14 | VR-06/07: component ซ้ำ · component=parent (กัน BOM วน) → block | S-05 · BR-05 | ☐ | ☐ | ☐ |

## หมวด 4 · line behaviour
| FN | ต้องทำอะไรได้ | trace | WF | DEV | QA |
|---|---|---|---|---|---|
| FN-15 | เปลี่ยนวัตถุดิบในบรรทัด → UoM reset = base uom ตัวใหม่ + กรองหมวดใหม่ (EC-05) | S-06 · BR-06 | ☐ | ☐ | ☐ |

## หมวด 5 · สถานะ + ลบ
| FN | ต้องทำอะไรได้ | trace | WF | DEV | QA |
|---|---|---|---|---|---|
| FN-16 | stat 4 ใบกดกรอง + filter สินค้า/สถานะ + ค้นหา + sort ทำงานร่วม | §6 | ☐ | ☐ | ☐ |
| FN-17 | view header: statusMenu เปลี่ยนสถานะ 3 ค่า ทุกทิศ (BR-08 ไม่มีอนุมัติ) · หลุด active → ★ หลุดตาม | S-07 · BR-08 | ☐ | ☐ | ☐ |
| FN-18 | bulk bar: 3 สถานะ + ยกเลิก · เลือกทั้งหน้าจาก thead · แถวไฮไลต์ · หลุด active → ★ หลุด | S-07 | ☐ | ☐ | ☐ |
| FN-19 | bulk ลบ: confirm บอกยอดลบ/ข้าม — used>0 (มี MO อ้าง) ไม่ลบ · ไม่มีตัวลบได้ → disabled | S-08 · BR-DEL | ☐ | ☐ | ☐ |

## หมวด 6 · รูปสินค้า + v8
| FN | ต้องทำอะไรได้ | trace | WF | DEV | QA |
|---|---|---|---|---|---|
| FN-20 | **FG แสดงรูปสินค้า** ใน list + fgCombo + view header · onerror fallback ตัวอักษร (offline ได้) | S-01 · OB-6 | ☐ | ☐ | ☐ |
| FN-21 | **#95 Overlay Portal**: combobox suggest เป็น portal ท้าย body (fixed จาก rect) — ลอยทับตาราง ไม่ clip · เลือก option ปิด portal · scroll/resize reposition | OB-6 | ☐ | ☐ | ☐ |
| FN-22 | #96 sticky thead · #29 scroll ไม่เด้ง · #97 จอ 768–1180 sidebar off-canvas · Esc chain (modal>statusMenu>drawer) | OB-5 | ☐ | ☐ | ☐ |
| FN-23 | CI Warm Light + Satoshi (rebrand จาก Navy) · icons SVG ฝัง renderIcons เอง | OB-4 | ☐ | ☐ | ☐ |
| FN-90 | ลบทุกทางผ่าน confirm เสมอ | S-08 | ☐ | ☐ | ☐ |

## FN-30 · Edge ประกาศรอเคาะ (OQ-BOM-04)
| กรณี | พฤติกรรมปัจจุบัน | รอเคาะ | WF |
|---|---|---|---|
| std_cost วัตถุดิบ = 0/null (EC-CL-01) | ต้นทุนเพี้ยน — ปล่อยผ่าน | block/warn? | ☐ |
| scrap 100% (EC-CL-02) | ต้นทุน×2 — ปล่อยผ่าน | cap/warn? | ☐ |
| FG/วัตถุดิบ deactivate หลังมีสูตร active (EC-ST-01/02) | สูตรยัง valid — ปล่อยผ่าน | flag? | ☐ |

## FN-40 · สิ่งที่ไม่รองรับ (ตัดสินแล้ว — รีวิวว่า "ไม่มี" จริง)
| ห้ามมี | มติ/LOCK | WF |
|---|---|---|
| multi-level BOM (สูตรซ้อนสูตร) | BR-05 single-level | ☐ |
| อนุมัติสูตร / สายอนุมัติ / DOA | BR-08 | ☐ |
| import/export CSV | OB-7 (structured doc) | ☐ |
| routing/operation/แรงงาน · co-product/by-product | S-10 (นอก BOM) | ☐ |
| ปุ่มลบรายตัว / สูตรหลักหลายตัวต่อ FG / hint-note | มติเลน + BR-02 | ☐ |
