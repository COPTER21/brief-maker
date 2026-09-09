# DOA_BRIEF — F131 Performance / ประเมินผลงาน (F-HR-PERF)

> **ยิงผ่าน ENG-DOA (F-DLG-001) เท่านั้น — feature "ประกาศ slot" เท่านั้น ห้าม hardcode สายอนุมัติ**
> Source of truth: FRD Pack (03_LOGIC §3.2 ENG-DOA · 02_API §API-11/12/14 · 05_RULES BR-05 · 07_LOCKED LK-1/LD-02)
> รันหลัง step 7 (FRD) · WF-01 declaration · 2026-09-09

---

## 1. Identity

| Field | Value |
|---|---|
| feature_id | F131 |
| feature_code | F-HR-PERF |
| name | Performance / ประเมินผลงาน |
| module | HR |
| platform | Web (SPA · tab-based) |
| approval_scope | `policy_approve` — อนุมัติ "สอบทานผลประเมิน" (ไม่ใช่ document_sign · ไม่ออก PDF/ลายเซ็น · LD-08) |
| **มีวงเงิน?** | **❌ ไม่มีวงเงิน** (ยืนยัน) — สอบทานผลประเมินไม่ผูกจำนวนเงิน (PREBRIEF §12 · 03_LOGIC ENG-DOA note · **ไม่ใช่ PR/PO**) |

---

## 2. Approval Actions

| # | Action | Trigger (FRD) | เมื่อผ่าน (approve) | เมื่อตีกลับ (reject) |
|:--:|---|---|---|---|
| A1 | **ส่งสอบทาน — freeze ผู้สอบทาน staged** (`sendCalibration` · FN-06 · API-11) | status = `calibration` + `weighted_score != null` (FIX-01) — HR เลือกผู้สอบทานจริงต่อขั้น (slot ว่าง · LK-1) | INSERT `T_perf_calibration_stage` (stage1=`current`, ที่เหลือ=`pending`) · คง status `calibration` (ยังไม่ publish · LD-02) | — (validate slot ครบ · ว่าง = 422 `BR_REVIEWER_SLOT_EMPTY`) |
| A2 | **บันทึกผลสอบทานรายขั้น** (`recordCalibrationStage` non-last · FN-07 · API-12) | ผู้สอบทานขั้น `current` บันทึกผล (stamp acted_at + actor_ref) | stage.status=`done` → เลื่อนขั้นถัดไป=`current` | ส่งกลับแก้ (กลับขั้น mgr — ดู A4 reopen) |
| A3 | **สอบทานขั้นสุดท้าย → เผยแพร่ + decision** (`recordCalibrationStage` last · FN-07 · API-12 isLast) | ทุก stage.status=`done` · ขั้นสุดท้ายบันทึก decision (ผ่าน / ทบทวน (PIP) / ไม่ผ่าน) | status → `published` + decision · ยิง **ENG-CSQ** `perf.result.published` (SecC/DC) + **ENG-NOTIFY** `perf.result.published` (ดู CSQ_BRIEF / NTF_BRIEF) | — (decision "ทบทวน"/"ไม่ผ่าน" = terminal decision ไม่ใช่การตีกลับ chain · เปิด PIP ได้) |
| A4 | **re-open ผลหลังเผยแพร่** (`reopenPublished` · FN-09 · API-14 · OQ-PERF-01 RESOLVED / LD-05) | authorized (manage) + open cycle + reason บังคับ | ส่งกลับขั้น `mgr` · เคลียร์ decision + `DELETE` calibration stages · คงคะแนน/gap · append-only audit ผู้แก้ · re-publish → **staged DOA ซ้ำ (re-resolve chain)** + CSQ ยิงซ้ำ per-person | 422 `BR_REASON_REQUIRED` ถ้า reason ว่าง |

> **SoD (07_OVERVIEW §0.4):** Maker (หัวหน้าประเมิน · `saveMgr`) ≠ Approver (ผู้สอบทานขั้นสุดท้าย). บังคับด้วย guard cascade (คะแนน mgr ครบ + ทุกขั้น `done` ก่อน `published`).

---

## 3. Matrix ที่จะไปตั้งค่า (หน้า DOA กลาง)

> **ไม่มีวงเงิน → 1 ชุดเดียว** `amount_from: 0 · amount_to: null` · chainMode = `sequential` (staged 2 ขั้น · LD-02)
> departments = `merged` (ทุกแผนกใช้กฎชุดเดียว · 03_LOGIC ไม่ระบุ per_dept)

| set | amount_from (บาท) | amount_to (บาท) | departments | chainMode | steps[stage · role_slot · role_id] |
|---|---:|---:|---|---|---|
| calibration | 0 | `null` (ไม่จำกัด) | merged | sequential | **stage 1** — slot "หัวหน้าสายงาน" · role_id = **«OQ-PERF-05 · CL-0013 — BA เคาะตอน config»** <br> **stage 2** — slot "ผู้สอบทาน (HRBP/ผู้บริหาร)" · role_id = **«OQ-PERF-05 · CL-0013 — BA เคาะตอน config»** |

- **ไม่มี field ยอดเงิน** ในทุก entity ของ feature (score/decision เป็น RESTRICTED performance data ไม่ใช่เงิน · 00_OVERVIEW §0.7).
- **slot ว่าง (value:null)** — HR เลือก "คน" จริงต่อขั้นตอนกดส่งสอบทาน (LK-1 · FIX-06/EC-08) · ENG-DOA `resolve` ผู้สอบทานตาม role_slot ณ ส่ง แล้ว freeze snapshot.
- 🔴 **role-id ของทั้ง 2 ขั้น = OQ-PERF-05 (CL-0013) — LEAVE AS OQ.** feature **ห้าม** invent role-id · BA กรอกที่ DOA กลางตอน config (07_LOCKED §7.5 · deadline: ก่อน Phase 3).

---

## 4. Field Contract สำหรับ FRD (มีอยู่แล้วใน pack — anchor)

| field | ชนิด | nullable | หมายเหตุ |
|---|---|:--:|---|
| `approval_chain` (snapshot per stage) | jsonb / `T_perf_calibration_stage` | — | freeze รายชื่อผู้สอบทาน ณ send (append-only · stamp acted_at + actor_ref) |
| `approver_role` (role_slot ต่อขั้น) | string | — | resolve จาก ENG-DOA · ไม่ hardcode |
| stage.status | enum `pending`/`current`/`done` | — | staged advance |
| decision | enum `ผ่าน`/`ทบทวน`/`ไม่ผ่าน` | ✓ (จนขั้นสุดท้าย) | terminal decision (บันทึกขั้นสุดท้าย) |
| **ยอดเงิน** | — | — | **ไม่มี field ยอดเงิน** (ยืนยัน · §1) |

---

## 5. UI Contract สำหรับ HTML (มีอยู่แล้วใน performance.html — anchor · ห้ามแก้จอ)

| ส่วน | รายละเอียด |
|---|---|
| **Slot picker (17 ส.ค.)** | เลือกผู้สอบทานจริง 2 ขั้น · slot ว่าง (ไม่ preset · LK-1) · ว่าง = block ส่ง |
| **Approval Timeline (staged)** | ไล่ทีละขั้น: role_slot → ผู้สอบทาน → เวลา → สถานะ (รอ/current/done) |
| ปุ่ม **ส่งสอบทาน** | เฉพาะ status `calibration` + คะแนน mgr ครบ (disabled ถ้ายังไม่ครบ · FIX-01) |
| ปุ่ม **บันทึกผลสอบทาน** | เฉพาะผู้สอบทานขั้น `current` · ขั้นสุดท้ายบังคับเลือก decision |
| **re-open** | เฉพาะ manage + published + open cycle · บังคับ reason |

---

## 6. Wire Checklist (`wire_status: pending → wired`)

- [ ] ตั้ง DOA entry `calibration` (2 stage sequential · no วงเงิน) ที่หน้า DOA กลาง — **กรอก role-id 2 ขั้นจาก OQ-PERF-05 (CL-0013)**
- [ ] dev wire: `sendCalibration` → ENG-DOA `resolve(role_slot)` + freeze snapshot (API-11)
- [ ] dev wire: `recordCalibrationStage` per-stage advance + publish บนขั้นสุดท้าย (API-12)
- [ ] dev wire: `reopenPublished` → re-resolve staged DOA ตอน re-publish (API-14)
- [ ] ยืนยัน SoD: หัวหน้าประเมิน (Maker) ≠ ผู้สอบทานขั้นสุดท้าย (Approver)

---

## 7. Open Questions

| OQ | คำถาม | Owner | สถานะ |
|---|---|---|---|
| **OQ-PERF-05** | **DOA chain executive role-ids (CL-0013)** — stage 1 (หัวหน้าสายงาน) + stage 2 (ผู้สอบทาน HRBP/ผู้บริหาร) ใช้ role-id ไหน | **BA (ที่ config)** | 🔴 **OPEN — feature ประกาศ slot เท่านั้น ไม่ hardcode role-id** |

> **ไม่ block FRD** — feature ประกาศ slot ครบแล้ว · role-id เป็นค่าที่ตั้งที่ DOA กลาง (07_LOCKED §7.5).
