# DOA_BRIEF — F-ACC-CN ใบลดหนี้ลูกค้า (Credit Note)

> **Positioning:** feature **ประกาศ**ว่า "มีการอนุมัติแบบมีวงเงิน หน้าตาแบบนี้" — DOA กลาง (F-DLG-001) เป็นทะเบียนที่ dev เอา matrix นี้ไปตั้งค่าจริง
> **Iron:** feature **ไม่ hardcode** ลำดับผู้อนุมัติ/จุดตัดวงเงิน — resolve จาก DOA entry ตอนกดส่ง แล้ว freeze ลง `approval_chain`
> **Supersedes** upstream `Pack Brief Feature/F-ACC-CN/5_DECLARATIONS/DOA_BRIEF_F-ACC-CN.md` — จัดตาม FRD Pack + HTML source of truth (LD-05 OQ-b RESOLVED)
> **จาก engine — ห้ามประกาศซ้ำ:** NTF `doa_pending`/`doa_result` มาจาก DOA engine (ดู NTF brief) · CSQ DC ระดับเอกสาร มาจาก DOA engine — DOA brief นี้ประกาศแค่ **matrix + slot + field/UI contract**

---

## §1. Identity

| | |
|---|---|
| feature_id | **F-ACC-CN** (F096) |
| name | ใบลดหนี้ลูกค้า (Credit Note) |
| module | Accounting / AR |
| platform | CUBE 4.0 |
| scope | company (multi-tenant RLS) |
| approval_scope | `document_sign` — เซ็นแล้วขึ้นช่องลายเซ็นใน PDF (ม.86/10) |

---

## §2. Approval Actions

feature นี้มี **1 สายอนุมัติ** (Q1 = 1 สาย · Q3 = merged ทุกแผนก).

| Action | Trigger (state) | ผลเมื่ออนุมัติครบสาย | ผลเมื่อไม่อนุมัติ (reject) |
|---|---|---|---|
| ส่งอนุมัติใบลดหนี้ | `draft → pending_approval` (API-05 · FN-06 `submitForApproval`) | ขั้นสุดท้าย approve → `approved` · **ออกเลข CN** (ENG-DOC-NUM) · `cn_applied` ใบเดิม += grand · JE mock + ลดภาษีขายเดือน cnDate (FN-11 · BR-08/09) | `pending_approval → draft` · เหตุผลบังคับ · `approval_history` append-only · badge "ถูกตีกลับ N ครั้ง" (API-07 · FN-08) |

- **จุด resolve:** `resolveDoa(s)` อ่าน `totals(s).grand` (HTML ม.542) — tier ตามมูลค่า ณ กดส่ง แล้ว snapshot chain freeze (FN-06 · BR-07 · LD-01)
- **จุด re-check:** อนุมัติขั้นสุดท้าย → approveGuard re-check `grand ≤ outstanding` (FN-07/FN-17 · EC-01 · BR-02)

---

## §3. Matrix ที่จะไปตั้งค่า (กรอกหน้า DOA กลางได้ตรงช่อง)

**มีวงเงิน** (Q2 = มีวงเงิน) · entry `doa_entry_ref = DOA-ACC-CN` · `chainMode = sequential` · `departments = all` (merged)
**★ ฐานวงเงิน = `grand` = ยอดลดหนี้สุทธิ *หลังหักส่วนลดท้ายบิล* (NET-after-end-bill)** — LD-05 · BR-07 · **BA-confirmed 2026-09-22 (OQ-b RESOLVED)** · ตรง HTML `resolveDoa()` → `totals(s).grand`

| set | amount_from (บาท) | amount_to (บาท) | departments | chainMode | steps[roles] |
|:--:|---|---|---|---|---|
| 1 | 0 | 50,000 | all | sequential | `[role-mgr-sales]` |
| 2 | 50,000.01 | 300,000 | all | sequential | `[role-mgr-sales]` → `[role-mgr-acc]` |
| 3 | 300,000.01 | `null` | all | sequential | `[role-mgr-sales]` → `[role-mgr-acc]` → `[role-cfo]` |

- ช่วงต่อเนื่อง ไม่ทับ ไม่มีรู · set สุดท้าย `amount_to: null` (ไม่จำกัด) ✅ G3/G4
- ตรง `MOCK_DOA_ENTRY.matrix` ใน HTML (ม.541) 1:1 — mock มี 3 tier เพื่อพิสูจน์ว่าสายเปลี่ยนตามเงิน ✅
- **จุดตัด 50k/300k + บทบาท = [DEFAULT — รอยืนยัน]** ต้องเคาะที่ Policy Center (OQ-CN-04)

---

## §4. Field Contract (สำหรับ FRD / entity)

| field | ชนิด | หมายเหตุ |
|---|---|---|
| `approval_required` | bool | จาก DOA entry — ไม่ใช่ค่าคงที่ในตาราง |
| `approval_status` | enum | `draft \| pending_approval \| approved \| rejected \| cancelled` |
| `doa_entry_ref` | string | = `DOA-ACC-CN` (FK ทะเบียน DOA · nullable Phase 1) |
| `approver_role` | string | role ที่ต้องเซ็นขั้นปัจจุบัน (resolve จาก DOA) |
| `approved_by` | string | user id ที่เซ็นจริง |
| `approval_chain` | jsonb | snapshot สายที่ resolve ตอนส่ง — freeze, append-only (LD-01) |
| `approved_at` | timestamp | |
| `approval_history` | jsonb | ประวัติ reject append-only (BR-13) |

**Business Rules (DOA · มีใน 05_RULES BR-07 + §5.2/§5.3):**

| BR | เนื้อหา | สถานะใน FRD |
|---|---|---|
| BR-DOA-01 | ส่งอนุมัติได้เฉพาะ `draft` | ✅ BR-07 · submitGuard |
| BR-DOA-02 | สาย resolve ตอนส่ง แล้ว **freeze** — แก้ DOA ทีหลังไม่กระทบใบที่ส่งแล้ว | ✅ LD-01 |
| BR-DOA-03 | reject → กลับ `draft` · ประวัติ append-only | ✅ FN-08 · EC-06 |
| BR-DOA-04 | **SoD** — ผู้ขอเซ็นอนุมัติใบตัวเองไม่ได้ (`submitted_by !== actor`) | ✅ BR-07 · `canActStep` · §5.3 |
| BR-DOA-05 | แก้ยอดหลังตีกลับ → re-resolve สาย (มีวงเงิน) | ✅ resolve ใหม่ตอนส่งซ้ำ |

---

## §5. UI Contract (สำหรับ HTML — ตรงจอจริงแล้ว)

| ส่วน | รายละเอียด (HTML anchor) |
|---|---|
| ปุ่มส่งอนุมัติ | เฉพาะ `draft` · `openSubmitModal` (ม.920) — guard `submitGuard` (ม.645) |
| Slot picker | เลือก "คน" ต่อขั้น (avatar + ตำแหน่ง + ชื่อ) · `renderSubmitModal` (ม.921) · block ถ้าเลือกไม่ครบ ("เลือกผู้อนุมัติให้ครบทุกขั้น") |
| Badge สถานะ | draft / รออนุมัติ / อนุมัติแล้ว / ไม่อนุมัติ / ยกเลิก — `docPill` |
| Approval Timeline | ไล่ทีละขั้น role → ชื่อผู้เซ็น → เวลา → สถานะ · `renderSignTab` (ม.897) · progress `renderSignProgress` (ม.907) |
| ปุ่มอนุมัติ/ไม่อนุมัติ | เฉพาะผู้มีสิทธิ์ขั้นปัจจุบัน (`canActStep`) · ไม่อนุมัติบังคับใส่เหตุผล · `openApproveModal` (ม.928) |
| My Approval hook | ใบ `pending_approval` โผล่ใน My Approval ของ assignee ขั้นแรก (`confirmSubmit` ม.927) |
| tier preview | step5 wizard แสดง `resolveDoa()` tier + สาย (ม.639) — ไม่มี chain hardcode |

---

## §6. Wire Checklist (dev · จน `wire_status: pending → wired`)

- [ ] ตั้ง DOA entry `DOA-ACC-CN` ตาม matrix §3 ที่หน้า DOA กลาง
- [ ] resolve สายตอนกดส่ง (`grand` หลัง end-bill) + freeze ลง `approval_chain`
- [ ] wire BR-DOA-01..05 + SoD (`submitted_by !== actor`)
- [ ] re-resolve ถ้าแก้ยอดหลังตีกลับ (มีวงเงิน)
- [ ] re-check `grand ≤ outstanding` ที่ approve ขั้นสุดท้าย (EC-01 · approveGuard)
- [ ] ใบ `pending_approval` โผล่ใน My Approval จริง
- [ ] **ยืนยัน role master** `role-mgr-sales` / `role-mgr-acc` / `role-cfo` มีจริง (OQ-AR-06)
- `wire_status: pending`

---

## §7. Open Questions

| OQ | เรื่อง | ใครตอบ |
|---|---|---|
| OQ-CN-04 | จุดตัดวงเงิน 50k/300k + บทบาทต่อ tier (§3 = [DEFAULT — รอยืนยัน]) | Policy Center + Strike |
| OQ-AR-06 | **role-ids [ASSUMED]** — โดยเฉพาะ `role-mgr-acc` ยังไม่พบใน master DOA · `role-mgr-sales`/`role-cfo` ต้องยืนยันสะกด | Policy Center (master roles) |

> **[ASSUMED]:** role-ids ทั้ง 3 ตัวยึดตาม HTML `MOCK_DOA_ENTRY` + upstream brief — ยังไม่ยืนยันกับ DOA master (skill reference ไม่มีไฟล์ master ในเครื่องนี้). ถ้าตั้งค่าจริงแล้ว id ไม่ตรง → เป็น mapping ที่ Policy Center เคาะ ไม่ใช่ feature invent.
