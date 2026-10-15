# DOA_BRIEF — F-PUR-PO · PO ใบสั่งซื้อ

> ใบประกาศ — feature **ประกาศ** ว่ามีการอนุมัติแบบไหน · **ห้าม hardcode สายอนุมัติใน feature**
> คนเอาใบนี้ไปตั้งค่า entry จริงที่หน้า **DOA กลาง (F-DLG-001)** → `wire_status: pending → wired`
> ⚠️ **LOCK ที่เหนือกว่า template เดิมของ skill**: `DOA-UI-LOCK 2026-08-17` (GOLDEN_RULES §3) —
> ตอน submit **UI ต้องให้เลือกคนจริงต่อ slot** (avatar + ตำแหน่ง + ชื่อ) · **ห้ามแสดง role ID บนหน้าจอ**
> role ใน matrix ข้างล่างเป็น **นิยามฝั่งทะเบียน DOA** (ใช้กำหนดว่า slot นั้นดึงคนจากกลุ่มไหน) — ไม่ใช่สิ่งที่ผู้ใช้เห็น

---

## 1. Identity

| ช่อง | ค่า |
|---|---|
| feature_id | `F-PUR-PO` (fid F078) |
| ชื่อ | PO ใบสั่งซื้อ |
| module | Purchase (PUR) |
| platform | CUBE NATIVE — Web |
| approval_scope | `document_sign` |
| **มีวงเงิน** | ✅ **มี** — ชั้นอนุมัติเปลี่ยนตาม **ยอดสุทธิของใบ** (PREBRIEF BR-06) |
| chainMode | `sequential` (ไล่ทีละชั้น) |
| departments | `merged` — ทุกแผนกใช้กฎชุดเดียวกัน `[DEFAULT — รอยืนยัน]` |
| wire_status | `pending` |

---

## 2. Approval Actions

| Action | Trigger | สถานะก่อน | ผลเมื่ออนุมัติครบ | ผลเมื่อส่งกลับแก้ | ผลเมื่อปฏิเสธ |
|---|---|---|---|---|---|
| ส่งอนุมัติ PO | ผู้ใช้กด "ส่งอนุมัติ" ที่ wizard step 5 | `draft` | `approved` (เกิด commitment) | กลับ `draft` แก้ต่อได้ | `cancelled` |
| **re-approve หลังแก้** | ผู้ใช้กดแก้ใบที่ `approved`/`sent` แล้วยืนยัน Transition Guard | `approved` / `sent` | กลับ `approved` (สายใหม่ตามยอดใหม่) | กลับ `draft` | `cancelled` |

> ทุก action ต้องกรอกเหตุผลเมื่อ **ส่งกลับแก้ / ปฏิเสธ / แก้หลังอนุมัติ** (PREBRIEF S-05, S-08)

---

## 3. Matrix ที่จะไปตั้งค่าที่หน้า DOA กลาง

**หน่วย = บาท · `amount_to: null` = ไม่จำกัด · ช่วงต่อเนื่องไม่ทับ ไม่มีรู**

| set | amount_from | amount_to | departments | chainMode | steps (ลำดับ slot) |
|---|---|---|---|---|---|
| 1 | 0 | 100,000 | merged | sequential | slot 1: หัวหน้าแผนกจัดซื้อ |
| 2 | 100,001 | 1,000,000 | merged | sequential | slot 1: หัวหน้าแผนกจัดซื้อ → slot 2: ผู้อำนวยการสายงาน |
| 3 | 1,000,001 | *null (ไม่จำกัด)* | merged | sequential | slot 1: หัวหน้าแผนกจัดซื้อ → slot 2: ผู้อำนวยการสายงาน → slot 3: ประธานเจ้าหน้าที่ฝ่ายการเงิน |

`[DEFAULT — รอยืนยัน]` ทั้ง 3 set — จุดตัดวงเงินและจำนวนชั้นยังไม่ผ่านการเคาะจากเจ้าของกระบวนการ (owner: **Strike**)

**Gate check**
- G2 ทุก set มี `amount_from` + `amount_to` ครบ ✅
- G3 ช่วงต่อเนื่อง 0→100,000 · 100,001→1,000,000 · 1,000,001→null — ไม่ทับ ไม่มีรู ✅
- G4 set สุดท้าย `amount_to: null` ✅
- G5 `approval_scope = document_sign` ✅
- G6 ค่าที่ยังไม่ยืนยันติด `[DEFAULT — รอยืนยัน]` ครบ ✅
- G1 role master (`references/doa-contract.md`) **ไม่มีในเลนนี้** → เขียน slot เป็น "นิยามตำแหน่งที่ทะเบียน DOA ใช้ดึงคน" แทน role id · ผู้ตั้งค่าต้อง map เป็น `role-*` จริงตอนกรอกที่หน้า DOA กลาง — **บันทึกเป็นข้อจำกัดของรอบนี้ ไม่ใช่การแต่ง role เอง**

---

## 4. Field Contract (สำหรับ FRD Phase B)

| field | ชนิด | nullable | หมายเหตุ |
|---|---|---|---|
| `approval_required` | bool | ✗ | มาจาก DOA entry — ไม่ใช่ค่าคงที่ในตาราง PO |
| `approval_status` | enum | ✗ | `draft \| pending_approval \| approved \| rejected \| cancelled` |
| `doa_entry_ref` | string | ✓ (Phase A) | FK ทะเบียน DOA |
| `approval_chain` | jsonb | ✓ | **snapshot ตอนกดส่งอนุมัติ · append-only** — เก็บทั้ง slot และ **คนจริง**ที่ถูกเลือก |
| `approver_slot[]` | array | ✗ ตอนส่ง | ต่อ slot: `{slot_no, person_id, person_name, position, avatar_ref, decided_at, decision, comment}` |
| `approved_by` | string | ✓ | คนสุดท้ายที่อนุมัติครบสาย |
| `approved_at` | timestamp | ✓ | ค.ศ. |
| `reapprove_reason` | text | ✓ | บังคับเมื่อแก้หลัง approve (BR-10) |

---

## 5. UI Contract (บังคับใน HTML — Phase A ทำแล้ว)

| ส่วน | รายละเอียด |
|---|---|
| ปุ่ม **ส่งอนุมัติ** | แสดงเฉพาะ `draft` · disabled จนกว่า **ทุก slot มีคนจริง** (BR-07) |
| **Slot picker (LOCKED)** | ต่อ slot เลือก **คนจริง**: รูป/ตัวย่อ + **ชื่อ-นามสกุล** + **ตำแหน่ง** · ห้ามแสดงรหัส role · ห้ามปล่อยว่าง |
| Badge สถานะ | ร่าง / รออนุมัติ / อนุมัติแล้ว / ส่งแล้ว / รับบางส่วน / ปิดแล้ว / ยกเลิก — สี CI Warm Light |
| **Approval timeline** (tab ลายเซ็น) | ไล่ทีละ slot: ชื่อคน → ตำแหน่ง → เวลา (ค.ศ.) → สถานะ (รอ/ผ่าน/ส่งกลับ/ปฏิเสธ) + ความเห็น |
| ปุ่ม **อนุมัติ / ส่งกลับแก้ / ปฏิเสธ** | เฉพาะคนที่เป็น slot ปัจจุบัน · ส่งกลับ/ปฏิเสธ = บังคับใส่เหตุผล |
| Hook **My Approval** | ใบ `pending_approval` ต้องโผล่ในกล่อง My Approval |
| **ยอดเปลี่ยน → สายเปลี่ยน** | mock ต้องมีอย่างน้อย **2 tier** ให้เห็นจริงว่าข้ามจุดตัดแล้ว slot เพิ่ม |

**ข้อห้ามใน code**
- ❌ `const APPROVAL_CHAIN = [...]` ในไฟล์ feature
- ❌ business rule แบบ "ถ้าเกิน 100,000 ให้ CFO เซ็น" ใน FRD/feature — นั่นคือ**ข้อมูลใน DOA**
- ✅ เขียนแทนว่า: *ระบบ resolve สายจาก DOA entry ณ เวลากดส่งอนุมัติ แล้ว snapshot ลง `approval_chain`*
- ✅ จุดที่ยังต่อ engine ไม่ได้ → `// TODO: DOA engine`

---

## 6. Business Rules ที่ต้องมี (ส่งต่อ FRD Phase B)

| BR | เนื้อหา | ตรงกับ PREBRIEF |
|---|---|---|
| BR-DOA-01 | ส่งอนุมัติได้เฉพาะสถานะ `draft` | §5 |
| BR-DOA-02 | สาย resolve ตอนส่ง แล้ว **freeze** — แก้ DOA ทีหลังไม่กระทบใบที่ส่งไปแล้ว | §7 audit |
| BR-DOA-03 | ส่งกลับแก้ → `draft` · ประวัติเก็บ **append-only** | S-05 · BR-16 |
| BR-DOA-04 | ผู้ขอ/ผู้สร้างเซ็นอนุมัติใบตัวเองไม่ได้ (segregation of duty) | `[AI-DRAFT]` |
| BR-DOA-05 | **แก้ยอดหลังส่งอนุมัติ → re-resolve สายใหม่** (feature นี้มีวงเงิน) | S-08 · BR-06/BR-10 |

---

## 7. Wire Checklist (Phase B / dev)

- [ ] ตั้ง entry จริงที่หน้า DOA กลาง ตาม matrix §3 (map slot → `role-*` จริง)
- [ ] เคาะจุดตัดวงเงิน 3 ช่วง (ปลด `[DEFAULT — รอยืนยัน]`) — owner **Strike**
- [ ] wire `resolve()` ตอนกดส่งอนุมัติ + snapshot `approval_chain`
- [ ] wire re-resolve เมื่อแก้ยอดหลังอนุมัติ (BR-DOA-05)
- [ ] เช็คใบโผล่ใน My Approval จริง
- [ ] toggle `wire_status: pending → wired`

---

## 8. Open Questions

| # | ประเด็น | ใครตอบ |
|---|---|---|
| DOA-Q1 | จุดตัดวงเงิน 100,000 / 1,000,000 ใช้ตัวเลขนี้จริงไหม | **Strike** |
| DOA-Q2 | ต้องแยกสายตามแผนกผู้ขอ (`per_dept`) ไหม — รอบนี้ตั้ง `merged` | Strike |
| DOA-Q3 | **short-close (ปิดใบก่อนรับครบ)** ต้องผ่าน DOA ด้วยไหม — รอบนี้ไม่ผ่าน (PREBRIEF OQ-PO-04) | Strike |
| DOA-Q4 | ยกเลิก PO ที่ `sent` แล้ว ต้องให้ผู้อนุมัติเดิมรับทราบ/อนุมัติไหม | Strike |
| DOA-Q5 | master `role-*` ของ DOA ยังไม่มีในเลนนี้ — ใครยืนยัน mapping slot → role id | เจ้าของ F-DLG-001 |
