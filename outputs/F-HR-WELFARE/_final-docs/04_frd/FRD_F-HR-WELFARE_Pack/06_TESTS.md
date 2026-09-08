# 06_TESTS — F-HR-WELFARE · Welfare (สวัสดิการ)

> **Audience:** QA engineer
> **Coverage source:** 02_API + 03_LOGIC + 05_RULES + welfare.html (microcopy verbatim).
> **Expected text:** ยึด **ข้อความจริงบนจอ** (welfare.html) ก่อน — ห้ามแต่งคำเอง (§6.10).

---

## §6.1 Acceptance Criteria (AT — ครอบ 24 FN + authorized additions)

### AT-01 (FN-01): สร้างประเภทสวัสดิการ
**Given** role=admin ที่ P-01 · **When** กรอกชื่อ/หมวด/หน่วยนับ/quota>0/กลุ่ม≥1/effFrom + ยืนยัน · **Then** status=active + audit · toast **"สร้างประเภทสวัสดิการสำเร็จ"**.

### AT-02 (FN-02): แก้ = เวอร์ชันใหม่
**Given** เวอร์ชัน active · **When** ออกเวอร์ชันใหม่ effFrom หลังเดิม · **Then** เก่า→archived + effTo=วันก่อนหน้า · ใหม่=active version+1 · toast **"บันทึกการแก้ไข (ออกเวอร์ชันใหม่) แล้ว"**. **And** แก้ draft → toast **"เผยแพร่ประเภทสวัสดิการแล้ว (ร่าง → มีผล)"**.

### AT-03 (FN-03/91): ปิดใช้ (soft archive) + เตือนคำขอค้าง
**Given** ประเภทมีคำขอค้าง · **When** เปิด confirm ปิดใช้ · **Then** เตือนจำนวนใบ (FIX-06); ยืนยัน → status=archived (ไม่ลบ) · toast **"ปิดใช้ (เก็บถาวร) แล้ว"** · คำขอเก่ายังอ่านได้.

### AT-04 (FN-04): quota≤0 / ช่วง effective ทับ → บล็อก
**Given** quota=0 · **Then** "โควตา/วงเงินต้องมากกว่า 0" (422 BR_QUOTA_INVALID). **And** effFrom ≤ เดิม · **Then** "…ช่วงมีผลทับกันไม่ได้" (BR_EFFECTIVE_OVERLAP).

### AT-05 (FN-05): เพิ่มผู้ติดตาม
**Given** role=admin · **When** กรอก ชื่อ/rel/dob/eligible · **Then** เพิ่มสำเร็จ · toast **"เพิ่มผู้ติดตามแล้ว"**.

### AT-06 (FN-06): ผู้ติดตามเกิน/บุตรอายุเกิน
**Given** บุตร dob อายุ>20 · **Then** บล็อก "บุตรอายุเกิน 20 ปี — เกินเกณฑ์กลุ่ม". **And** ≥3 คน → warning (non-block).

### AT-07 (FN-07): สร้างคำขอ — type มีสิทธิ์ ณ วันยื่น + self/dep + แนบไฟล์
**Given** ผู้ยื่น · **When** เปิด combobox type · **Then** แสดง "มีสิทธิ์"/"ไม่มีสิทธิ์" ต่อ type; เลือก self/dependent + แนบไฟล์ + value>0 → สร้างได้.

### AT-08 (FN-08): ส่งอนุมัติ DOA slot picker
**Given** คำขอ draft/pending · **When** เปิด modal doa · **Then** slot 2 ขั้น (avatar+ตำแหน่ง+ชื่อ) + note "GET /doa/resolve"; เลือกไม่ครบ → "เลือกผู้อนุมัติให้ครบทุกขั้น"; ครบ → toast **"ส่งอนุมัติแล้ว · แจ้งเตือน HR อัตโนมัติ"** · chain freeze.

### AT-09 (FN-09): ใช้บางส่วน — คงเหลือถูกต้อง
**Given** อนุมัติบางส่วนแล้ว · **Then** balance tab แสดง used/remaining ถูกต้อง (นับเฉพาะ approved) · ใช้ต่อรอบได้.

### AT-10 (FN-10): ขอเกินคงเหลือ → บล็อก
**Given** value/amount > remaining · **Then** ปุ่มส่ง disabled + note danger; submit → toast **"ยื่นไม่ได้: เกินคงเหลือ"** (BR_OVER_BALANCE).

### AT-11 (FN-11): ยื่น type ไม่มีสิทธิ์ → บล็อก+เหตุ
**Given** พนักงานนอกกลุ่ม/นอกช่วง/พ้นสภาพ · **Then** บล็อก + เหตุ (เช่น "พนักงานพ้นสภาพแล้ว (leaver) — สิทธิ์สิ้นสุด ยื่นคำขอไม่ได้" / "กลุ่ม … ไม่มีสิทธิ์ในประเภทนี้") — ไม่บล็อกเงียบ.

### AT-12 (FN-12): ดูสถานะ + สาย DOA (อ่าน)
**Given** คำขอ pending · **Then** drawer tab รายละเอียด แสดง DOA timeline "สายอนุมัติ (จาก DOA กลาง)" + ชั้นปัจจุบัน.

### AT-13 (FN-13): อนุมัติขั้นสุดท้าย → ตัดคงเหลือ + 7C EC + hook
**Given** ขั้นสุดท้าย · **When** re-check ผ่าน (FIX-02) → อนุมัติ · **Then** status=approved · pay=pending · toast **"อนุมัติแล้ว · ตัดคงเหลือ + บันทึกมูลค่าเข้า 7C EC"** · history "ตัดคงเหลือ + บันทึกมูลค่าเข้า 7C EC + ส่งสถานะจ่าย" · CSQ EC + NTF ยิง.

### AT-14 (FN-14): ไม่อนุมัติ → ไม่ตัด + เหตุ + NTF
**Given** reason ว่าง · **Then** บล็อก. **And** ระบุเหตุ → status=rejected · ไม่ตัดคงเหลือ · toast **"บันทึกไม่อนุมัติ · แจ้งเตือนผู้ยื่น"**.

### AT-15 (FN-15): ยกเลิกก่อนอนุมัติ
**Given** status draft/pending · **Then** ยกเลิกได้ · toast **"ยกเลิกคำขอแล้ว"** · ไม่กระทบคงเหลือ. **And** approved → ปุ่มยกเลิกไม่ปรากฏ (BR_CANCEL_NOT_ALLOWED).

### AT-16 (FN-16): leaver → revoked · null≠ทำงาน
**Given** leaver signal (last_day set) · **Then** คำขอค้าง→revoked · คงเหลือหยุด · balance note "พนักงานพ้นสภาพ … คงเหลือหยุดคำนวณ". **And** last_day=null → ถือว่ายังทำงาน (ไม่ revoke).

### AT-17 (FN-17): สถานะจ่าย display-only
**Given** approved · **Then** payPill แสดงสถานะจ่าย (อ่าน Payroll/Expense) · **ไม่มีปุ่ม CRUD การจ่าย** · note "…display-only · Welfare ไม่จ่ายเอง".

### AT-18 (FN-18): joiner → สิทธิ์เปิดอัตโนมัติ
**Given** joiner signal · **Then** balance note "สิทธิ์เปิดอัตโนมัติ ตาม joiner signal" · คงเหลือคำนวณจากปีสิทธิ์.

### AT-19 (FN-19): รายงาน + filter จริง
**Given** P-04 · **When** เลือก filter type/group/from/to · **Then** ตาราง+agg อัปเดตจริง; ไม่มีข้อมูล → empty state.

### AT-20 (FN-90): ค้นหา/filter + empty
**Then** ทุก list filter ทำงานจริง + empty state ต่อหน้า.

### AT-21 (FN-92): validate + กัน double-submit
**Then** field บังคับ validate ก่อนบันทึก · ปุ่ม is-disabled ("กำลัง…") กันคลิกซ้ำ (lockBtn). (idempotency EC-08)

### AT-22 (FN-93): audit append-only
**Then** history timeline บันทึกทุก create/แก้/อนุมัติ/ยกเลิก/**กลับรายการ** (append-only) — ไม่มี hard delete.

### AT-23 (FN-94): RESTRICTED masking ตาม role
**Given** role=employee · **Then** มูลค่า/บุคคล = `•••`. **Given** role=manager · **Then** เห็นมูลค่า แต่ผู้ติดตาม mask. **Given** admin · เห็นครบ. (enforce backend — EC-09)

### AT-24 (FN-14 · OQ-WEL-01): กลับรายการ (reversal)
**Given** status=approved + role∈{admin,manager} · **Then** ปุ่ม "กลับรายการ" ปรากฏ (เฉพาะ approved && canApprove). **When** ระบุเหตุ + ยืนยัน · **Then** status=reversed · toast **"กลับรายการแล้ว · คืนสิทธิ์และมูลค่าให้พนักงาน · แจ้งเตือนผู้ยื่น"** · pill "กลับรายการแล้ว" · คงเหลือคืน · ข้อมูลเดิมคงอยู่ · history เพิ่ม "กลับรายการ · คืนมูลค่าเข้าเงินได้ (7C · EC)". **And** reason ว่าง → บล็อก. **And** approved ที่ไม่ใช่ canApprove → ปุ่มไม่ปรากฏ.

### AT-25 (OQ-WEL-03): exposure display-only
**Given** มีคำขอ pending อื่นบนสิทธิ์เดียวกัน · **Then** balance tab แสดง "คำขอรออนุมัติอื่นของสิทธิ์นี้: N ใบ · รวม {amount}" · **display-only ไม่ล็อก/reserve**.

### AT-26 (FIX-02/EC-07): re-check ณ อนุมัติ (atomic)
**Given** 2 คำขอ pending สิทธิ์เดียวกัน อนุมัติพร้อมกันจนรวมเกินเพดาน · **Then** ขั้นสุดท้าย re-check → รายที่สองบล็อก "คงเหลือไม่พอ ณ วันอนุมัติ" (BR_OVER_BALANCE_AT_APPROVAL) หรือ 409 ERR_STALE_DATA (optimistic lock · OQ-04).

### AT-27 (FIX-03): one-step advance
**Given** สาย DOA 2 ขั้น · **When** ขั้น 1 อนุมัติ · **Then** ขั้น 1=approved · ขั้น 2=current · **status ยัง pending** (ไม่ collapse) · toast "อนุมัติขั้น 1 แล้ว · ส่งต่อขั้นถัดไป". **When** ขั้น 2 อนุมัติ → finalize.

---

## §6.2 Test Case Inventory (สรุป)
| TC ID | Name | Type | Maps to | Priority |
|---|---|---|---|---|
| TC-01..19 | FN-01..19 happy/negative | API+UI | AT-01..19 | P0/P1 |
| TC-REV-01 | reversal append-only | API+UI | AT-24 | P0 |
| TC-EXP-01 | exposure display | UI | AT-25 | P1 |
| TC-CC-01 | concurrent approval | stress | AT-26 | P1 |
| TC-ADV-01 | one-step advance | API | AT-27 | P0 |
| TC-MASK-01 | masking per role | UI/API | AT-23 | P0 |
| TC-XT-01..05 | cross-module | integration | §6.9 | P0/P1 |

---

## §6.3 Test Data Setup
- 4 benefit type (ประกันสุขภาพ 30,000/ปี ครอบผู้ติดตาม · ตรวจสุขภาพ 1 ครั้ง/ปี · ค่าเล่าเรียนบุตร 20,000/ปี · PVD %) · effective 1 ม.ค. 2569.
- 3 กลุ่ม (ประจำ · ทดลองงาน สิทธิ์จำกัด · รายวัน ไม่มีสิทธิ์บางตัว).
- 6 พนักงาน (1 มีผู้ติดตาม 2 · 1 ทดลองงาน · 1 กำลังพ้นสภาพ→S-13 · 1 joiner→S-15).
- คำขอ mix: approved บางส่วน(S-08) · เกินวงเงิน(S-09) · pending · rejected(S-11) · ส่งจ่าย Payroll(S-14). ปี **พ.ศ. 2569**.
- Roles: qa_admin(admin) · qa_manager(manager) · qa_employee(employee, own scope).

---

## §6.4 Definition of Done (DoD)
### Code
- [ ] AT-01..27 implement + unit tests · integration (API+DB+Engine) · E2E happy + edge.
- [ ] Coverage ≥80% logic layer · security findings 0 critical/high.
### Documentation
- [ ] API docs (จาก 02_API) · FRD 07_LOCKED reflect final · CUBIC register ENG-WEL-01/02 (LD-04).
### QA
- [ ] P0+P1 pass · masking verified · reversal EC offset verified · one-step advance verified.
### Deployment
- [ ] Migration staging · DOA entry ตั้งที่ DOA กลาง (DOA_BRIEF §6) · CSQ/NTF events registered · rollback plan.

---

## §6.5 WebSocket / Realtime
- `welfare_request_submitted` → HR inbox update · `welfare_request_result` → maker toast · `welfare_request_reversed` → maker. (ยิงผ่าน ENG-NOTIFY — ไม่เช็ค channel เอง)

---

## §6.6 Performance
| Endpoint | P95 |
|---|---|
| GET /requests (list) | < 500ms |
| GET /balance (compute) | < 600ms |
| POST /requests/:id/approve | < 900ms (incl. re-check + CSQ/NTF) |

---

## §6.7 Test Environment
- staging tenant · pay-status hook = mock (A-WEL-02) · ENG-DOA resolve = deterministic mock (2-step) · ปี พ.ศ.

---

## §6.8 Trace: AC → Logic Coverage
| AC | API | Functions | Engines |
|---|---|---|---|
| AT-01/04 | API-02 | FN-01, FN-03 | — |
| AT-02 | API-04 | FN-02, FN-03 | — |
| AT-03 | API-05 | FN-04 | — |
| AT-05/06 | API-06 | FN-05 | — |
| AT-07/10/11 | API-09 | FN-07, FN-08, FN-09 | ENG-WEL-01, ENG-WEL-02 |
| AT-08 | API-11 | FN-10 | ENG-DOA |
| AT-13/26/27 | API-12 | FN-11, FN-19 | ENG-WEL-01/02, ENG-CSQ, ENG-NOTIFY |
| AT-14 | API-13 | FN-12 | ENG-NOTIFY |
| AT-15 | API-14 | FN-13 | — |
| AT-24 | API-15 | FN-14 | ENG-WEL-02, ENG-CSQ, ENG-NOTIFY |
| AT-09/25 | API-16 | FN-15, FN-16 | ENG-WEL-02 |
| AT-19 | API-17 | FN-17 | ENG-WEL-02 |
| AT-16/18 | (signal) | FN-18 | ENG-NOTIFY |
| AT-23 | all | FN-19 | — |

> ทุก Function (FN-01..19) + Engine (ENG-WEL-01/02) ถูก trace ≥1 AC ✅.

---

## §6.9 Cross-Module Test Cases ⭐ (จาก BRD §12.1)

| ID | Scenario | Downstream | Expected |
|---|---|---|---|
| **XT-01** | อนุมัติคำขอมีมูลค่า | CSQ (7C·EC) | ยิง event `welfare.granted` ท่อ **EC เท่านั้น** · payload {ref, employee_id, value_declared, basis=declared} · **ไม่มี OC/DC/SC** |
| **XT-02** | อนุมัติ | Payroll/Expense | pay=pending (display-only) · Expense revalidate วงเงิน · **ไม่มี pay action ใน Welfare** |
| **XT-03** | **กลับรายการ (reverse)** | CSQ | ยิง **EC reverse** (negative offsetting entry) คืนมูลค่าเข้าเงินได้ 7C·EC (คู่กับ EC forward) |
| **XT-04** | reverse คำขอที่ pay=sent | Payroll | `payroll_clawback=true` flag → แจ้งตั้งเบิกคืน · Welfare ไม่จ่าย/ไม่ clawback เอง |
| **XT-05** | ทุก state transition | Notification | ยิง 5 events (submitted/result/near_limit/eligibility_ended/**reversed**) · DOA events ไม่ซ้ำ |

---

## §6.10 Microcopy-Aware Expected Text
> ยึด verbatim จาก welfare.html: สร้างประเภทสำเร็จ = "สร้างประเภทสวัสดิการสำเร็จ" · ส่งอนุมัติ = "ส่งอนุมัติแล้ว · แจ้งเตือน HR อัตโนมัติ" · อนุมัติ final = "อนุมัติแล้ว · ตัดคงเหลือ + บันทึกมูลค่าเข้า 7C EC" · reject = "บันทึกไม่อนุมัติ · แจ้งเตือนผู้ยื่น" · **reverse = "กลับรายการแล้ว · คืนสิทธิ์และมูลค่าให้พนักงาน · แจ้งเตือนผู้ยื่น"** · cancel = "ยกเลิกคำขอแล้ว" · เกินคงเหลือ = "ยื่นไม่ได้: เกินคงเหลือ" · pill reversed = "กลับรายการแล้ว".
> ผล: ai-testcase-md-generator ต่อยอดได้ match จอ 1:1.
