# DOA_BRIEF — F084 · F-WH-STOCKTAKE · Stocktake

> ใบประกาศสำหรับตั้งค่าที่ DOA กลาง F019 เท่านั้น ฟีเจอร์ Stocktake ต้องเรียก resolve และ snapshot ผล ห้าม hardcode chain ใน production

## 1. Identity

| ช่อง | ค่า |
|---|---|
| feature_id | `F-WH-STOCKTAKE` (`F084`) |
| module | Warehouse |
| action | `approve_variance` |
| approval_scope | `policy_approve` |
| amount basis | `absolute_variance_value = Σ abs(diff_qty × unit_cost_snapshot)` |
| department mode | `merged` `[DEFAULT — รอยืนยัน]` |
| chain mode | `sequential` |
| wire_status | `pending` |

## 2. Approval Action

Trigger หลัง count/recount เสร็จและ status=`review` ผู้คุมรอบกด “ส่งอนุมัติ” ระบบ resolve ตามฐานมูลค่าส่วนต่าง ณ ขณะนั้นและ freeze `approval_chain`. อนุมัติครบ → `approved`; ไม่อนุมัติพร้อมเหตุผล → `rejected`, ปลด scope lock และเก็บทุก decision แบบ append-only

## 3. Matrix สำหรับตั้งค่ากลาง

Matrix ด้านล่างสะท้อน mock ที่ PM/BA ให้ทดสอบใน HTML เพื่อพิสูจน์ multi-tier; ก่อน wire จริงต้อง map ชื่อตำแหน่งเป็น `role-*` จาก master และให้ DOA admin ยืนยัน

| set | amount_from | amount_to | departments | chainMode | steps |
|---:|---:|---:|---|---|---|
| 1 | 0 | 19,999 | merged | sequential | ผู้จัดการคลัง |
| 2 | 20,000 | 199,999 | merged | sequential | ผู้จัดการคลัง → ผู้อำนวยการคลัง |
| 3 | 200,000 | null | merged | sequential | ผู้จัดการคลัง → ผู้อำนวยการคลัง → ผู้อำนวยการการเงิน |

`[DEFAULT — รอยืนยัน]` ทั้ง 3 ช่วงและ role mapping; ช่วงต่อเนื่อง ไม่ทับ และปลายสุดไม่จำกัด

ตัวอย่างใน prototype: ITM-001 จาก 12 เหลือ 11, cost snapshot 25,000 บาท → ฐานอนุมัติ 25,000 บาท → resolve 2 ขั้น

## 4. Field Contract

`approval_required`, `approval_status`, `doa_entry_ref`, `approval_base_amount`, `approver_role`, `approved_by`, `approved_at`, `approval_chain` และ `approval_steps[] {level, role_slot, person_id, decision, reason, decided_at}`. Chain เป็น snapshot append-only

## 5. UI Contract

- ปุ่ม “ส่งอนุมัติ” มีเฉพาะหัวหน้างานเมื่อ status=`review`
- slot picker ต่อขั้นเลือกคนจริงและแสดง avatar/ชื่อ/ตำแหน่ง
- ห้ามเลือกผู้นับ/ผู้นับซ้ำเป็น approver และห้ามเลือกคนซ้ำข้ามขั้น
- ปุ่ม “อนุมัติขั้นนี้/ไม่อนุมัติ” แสดงเฉพาะคนของ step ปัจจุบัน
- หน้าผลต่างแสดงฐานอนุมัติและ progress ขั้นปัจจุบัน
- My Approval hook ต้องรับรายการ pending จาก DOA กลางเมื่อ wire จริง

## 6. Wire Checklist

- [ ] สร้าง entry/action `approve_variance` ที่ DOA กลาง
- [ ] ยืนยัน 3 ช่วงและ map slot เป็น `role-*` จริง
- [ ] เรียก resolve ด้วย `absolute_variance_value` ตอนส่ง
- [ ] freeze chain/person snapshot และบังคับ sequential/SoD
- [ ] ให้ rejected/closed ส่ง audit และ lock-release ตาม FRD
- [ ] เปลี่ยน `wire_status` เป็น `wired` หลัง integration test ผ่าน

## 7. Open Questions

- OQ-DOA-01: รหัส `role-*` จริงของผู้จัดการคลัง/ผู้อำนวยการคลัง/ผู้อำนวยการการเงิน — DOA admin
- OQ-DOA-02: ยืนยันขอบเขต 0–19,999 / 20,000–199,999 / 200,000+ — Warehouse BA
- OQ-DOA-03: matrix แยกตามคลังหรือใช้ merged — Warehouse BA

## Quality Gate

G2–G7 ผ่าน; G1 รอ role master ตาม OQ-DOA-01 จึงยังเป็น `wire_status: pending` โดยไม่ hardcode role id ขึ้นเอง
