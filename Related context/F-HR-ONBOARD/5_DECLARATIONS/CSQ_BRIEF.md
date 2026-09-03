# CSQ_BRIEF — F-HR-ONBOARD · On/Offboard (เข้าออกงาน)

> ออกโดย `csq-declaration` v1.0 · **Lane Mode (no-ask)** · S1.8 · 2026-08-29
> Input: `briefs/W3/F-HR-ONBOARD/PREBRIEF.md` v1.1 §12 (**authoritative**) + §5 state machine + §4 BR + §3.3 ทะเบียนสิทธิ์ · `LANE_BRIEF.md` (chip) · `_lane/DECL.json`
> **DIVERGENCE: —** (chip `csq ✓` = detect §12 = `CONTEXT_PACK/HR.md` แถว On/Offboard → **`✓ SecC (revoke สิทธิ์)`**)
> หมายเหตุ: `references/csq-contract.md` และ `references/brief-template.md` **ไม่มีในเวิร์กสเปซนี้** — ยึด contract จาก SKILL.md (§Trigger Rule · Iron Rule · Quality Gate G1–G9) + `cube-4.0-current-state.md §3` · **`profile_id` ติด `[DEFAULT — รอยืนยัน]`**
> **feature ประกาศเท่านั้น — ห้ามคำนวณผลรายท่อเอง · ห้ามเก็บคอลัมน์ผลรายท่อในตารางของ feature · ห้ามวาดการ์ดผล 7 ท่อในหน้าจอ**

## §1 Identity

| | |
|---|---|
| profile_id | **`CSQ-HRONB`** `[DEFAULT — รอยืนยัน · OQ-CSQ-02]` |
| feature_code | `F-HR-ONBOARD` · On/Offboard · เข้าออกงาน |
| module | HR |
| กลุ่ม (A/B/C) | **กลุ่ม B — SecC on sensitive change** (`CSQ_BACKFILL_REGISTER.md` ไม่มีในเวิร์กสเปซ · จัดกลุ่มตามลักษณะ event ตาม SKILL §Batch Mode) |
| **ท่อที่ประกาศ** | **`secc` ท่อเดียว** |
| version | 1.0 (2026-08-29) · `register_status: pending` |

## §2 Declared Events

> trigger point อ้าง **PREBRIEF §5 (state machine)** · **§4 (BR)** · **§3.3 (ทะเบียนสิทธิ์)** — ณ S1.8 ยังไม่มี FRD
> **ข้อผูกพันถึง S5 (`frd-generator-v6`):** ต้อง map ทุกแถวนี้เป็น `03_LOGIC §x.x` / `05_RULES BR-xx` จริง แล้ว **append ในไฟล์นี้** (ห้ามออกใบใหม่)

| # | event_id | trigger point (PREBRIEF) | ท่อที่ยิง | เงื่อนไข | payload fields |
|---|---|---|---|---|---|
| **E1** | `onboard.access_granted` | §5.1 **T-1/T-2** — ผลตอบกลับจาก Roles & Permissions = "เปิดแล้ว" ต่อรายการ (S-03 · BR-03 · BR-04 · FN-06) | **SecC** | **ทุกครั้งที่บุคคลได้รับบัญชีหรือสิทธิ์ใหม่** | `case_id` · `case_type` · `employee_id` · `access_kind` · `access_ref` · `granted_at` · `ack_by` · `ack_ref` · `company_id` |
| **E2** ⭐ | `offboard.access_revoked` | §5.2 **T-11** — ผลตอบกลับ "เพิกถอนแล้ว" ต่อรายการ จนครบทั้งทะเบียน (S-22 · S-23 · BR-04 · BR-05 · FN-31 · FN-33) | **SecC** | **ทุกครั้งที่สิทธิ์ถูกถอนออกจากบุคคล** — ยิง **ต่อรายการ** และมี event สรุปเมื่อครบ (`is_final = true`) | `case_id` · `employee_id` · `access_kind` · `access_ref` · `revoked_at` · `ack_by` · `ack_ref` · `revocation_due_at` · `is_final` · `revoked_count` · `total_count` |
| **E3** ⭐⭐ | `offboard.revocation_overdue` | **เลย `revocation_due_at` แล้วยังมีรายการที่ `revoke_state ≠ เพิกถอนแล้ว`** (S-24 · S-25 · S-29 · **BR-06** · FN-34 · FN-36 · FN-40) | **SecC** | **นี่คือ event ที่สำคัญที่สุดของใบนี้** — บุคคลพ้นสภาพแล้วแต่ยังเข้าระบบได้ · **ยิงซ้ำตามรอบจนกว่าจะครบ พร้อม `severity` ที่โตตามเวลาที่เลย** | `case_id` · `employee_id` · `last_working_day` · `revocation_due_at` · `overdue_hours` · `pending_count` · `pending_access_kinds[]` · `severity` · `retry_count` |
| **E4** | `offboard.immediate_revocation` | §5.2 **T-8 → T-11 ทันที** เมื่อ `is_immediate_exit = true` (S-26 · BR-05 · FN-37) | **SecC** | การเพิกถอนแบบเร่งด่วน (เลิกจ้าง/ออกก่อนกำหนด) — แยกจาก E2 เพราะ **โปรไฟล์ความเสี่ยงต่างกัน** และเกิดก่อนวันสุดท้ายตามสัญญา | `case_id` · `employee_id` · `termination_reason` · `ordered_by` · `ordered_at` · `last_working_day` · `access_count` |
| **E5** | `offboard.access_restored` | §5.2 **T-14** — ยกเลิกรอบหลังเพิกถอนไปแล้ว → **คำขอคืนสิทธิ์** สำเร็จ (S-38 · BR-14 · FN-50 · FN-51) | **SecC** | **การคืนสิทธิ์ให้บุคคลที่เคยถูกเพิกถอน** — เป็นเหตุการณ์ด้านความปลอดภัยเต็มตัว ต้องเห็นได้ในหน้า Consequence | `case_id` · `employee_id` · `access_kind` · `access_ref` · `restored_at` · `ack_by` · `cancel_reason` · **`reversal_of`** (ชี้ event `offboard.access_revoked` เดิม · BR-CSQ-04) |
| **E6** | `onboard.access_revoked_on_cancel` | §5.1 **T-4/T-5/T-6** — ยกเลิกรอบเข้างานทั้งที่เปิดบัญชีไปแล้ว (S-08 · BR-03 · BR-13 · FN-13) | **SecC** | บัญชีที่เปิดให้คนที่ไม่ได้เริ่มงาน **ต้องถูกปิดทันที** และต้องมองเห็นในระบบผลกระทบ | `case_id` · `employee_id` · `access_kind` · `access_ref` · `revoked_at` · `cancel_reason` · `ack_by` |
| **E7** | `offboard.temp_access_delegated` `[STD · จาก S1.5 G-01]` | งานส่งมอบความเป็นเจ้าของข้อมูล → **มอบสิทธิ์ชั่วคราวแก่ผู้รับมอบ** แทนการเลื่อนเวลาเพิกถอน (S-56 · **BR-31** · FN-75 · FN-76) | **SecC** | **การให้สิทธิ์เข้าถึงข้อมูลของคนอื่นแก่บุคคลที่สาม** — ต้องถูกบันทึกเป็นเหตุการณ์ด้านความปลอดภัย ไม่ใช่รายละเอียดของงานธุรการ | `case_id` · `employee_id` (เจ้าของข้อมูลเดิม) · `delegate_employee_id` · `access_kind` · `access_ref` · `granted_at` · `expires_at` · `ack_by` |

**ทำไมทุก event เป็น SecC:** feature นี้ **มีอยู่เพื่อเปิดและปิดสิทธิ์ของบุคคล** — ทุก event ข้างบนคือ *"เปลี่ยนสิทธิ์"* ตรงนิยามท่อ **SecC** ใน SKILL.md §Trigger Rule (ตระกูลเดียวกับ Roles & Permissions · Data Masking · Credit Limit) และตรงกับตาราง `CONTEXT_PACK/HR.md` แถว On/Offboard = **`✓ SecC (revoke สิทธิ์)`**
**ทำไมยิง `offboard.access_revoked` ต่อรายการ (ไม่ใช่ครั้งเดียวตอนจบ):** เพราะ **หลักฐานที่ตรวจสอบได้ต้องอยู่ระดับรายการ** (PREBRIEF §3.3 `ack_by`/`ack_at`/`ack_ref` · BR-04) — ถ้ายิงครั้งเดียวตอนครบ **เคสที่ครบไม่จริง (E3) จะไม่มีร่องรอยว่าอะไรทำไปแล้วบ้าง**

## §3 ท่อที่ไม่ประกาศ (และเหตุผล) — ห้ามเงียบ

| ท่อ | ประกาศ? | เหตุผล |
|---|---|---|
| **OC** (Operation) | ❌ **ห้าม — จุดที่พลาดง่ายที่สุดของ feature นี้** | feature นี้ **มี checklist จริงและงานทุกงานถูกประกาศเป็น SOW ของ Operation Process** (PREBRIEF S-45 · BR-02) → **`sow.*` ทำให้ OC เกิดขึ้นเองอยู่แล้วที่ฝั่ง OP** · การประกาศ `oc` ที่นี่ = **นับซ้ำ + register reject 422** · **ความรู้สึกว่า "มี checklist = ต้องมี OC" คือกับดัก** — เจ้าของท่อ OC คือ OP เจ้าเดียว (`current-state §3` · SKILL §Q2 ข้อ 1) · **FN-63 คือ FN ที่พิสูจน์ข้อนี้ด้วยตา** |
| **DC** (Decision) ระดับเอกสาร | ❌ **ห้าม** | **DOA engine เป็นเจ้าของ** — feature นี้มีการอนุมัติจริง (`offboard_approve_voluntary` / `offboard_approve_involuntary` / `offboard_approve_cancellation` · ดู `DOA_BRIEF.md`) **ยิ่งต้องไม่ประกาศซ้ำ** · **422** |
| **SC** | ❌ **ห้าม** | สงวนไว้ (OQ-C3 ยังไม่เคาะ) · `trigger=false` เสมอ |
| **DC** (terminal decision) | ⬜ ไม่ประกาศ | การอนุมัติ/ไม่อนุมัติการออกจากงาน **เป็นการเซ็นอนุมัติเอกสาร/คำขอ ไม่ใช่ terminal decision แบบ Continue/Adjust/Hold/Stop/Complete** ของกระบวนการ · ผลการทบทวนทดลองงาน (S-09) ก็ไม่ใช่ — มันเป็น **ข้อมูลนำเข้า** ของรอบออกงานหรือของ Employee Movement ไม่ใช่จุดจบของกระบวนการที่นี่ |
| **EC** (Economic) | ⬜ ไม่ประกาศ | ต้นทุนการเข้า/ออกงาน (ต้นทุนสรรหา · ต้นทุนตำแหน่งว่าง · เวลาที่ใช้ทำ checklist) **ยังไม่มีฐานคิดในระบบ และ scope note ตัดเรื่องเงินออกทั้งหมด** (BR-18) · ถ้าจะประกาศต้องมี Rate Card ก่อน มิฉะนั้นจะเป็นการ **ใส่ตัวเลขที่คำนวณเอง ซึ่ง G7 ห้าม** |
| **AC** (Accounting) | ⬜ ไม่ประกาศ | ไม่มีรายการทางบัญชีเกิดจาก feature นี้ — **ค่าชดเชย/เงินได้ครั้งสุดท้ายเกิดที่ Payroll (W4)** และ Accounting (S-44 · OQ-STD-OB5) |
| **FC** (Financial) | ⬜ ไม่ประกาศ | ไม่มีเงินสด/งบเปลี่ยนจากการเข้า-ออกงานที่นี่ · **งบอัตรากำลังอยู่ที่ Manpower Planning (W6)** · การจ่ายจริงอยู่ที่ Payroll |

## §4 Payload Contract

| field | ชนิด | มาจาก entity (PREBRIEF) | Classification / masking |
|---|---|---|---|
| `case_id` · `case_type` | text · enum | `onboard_case` / `offboard_case` §3.1 | Internal |
| `employee_id` | uuid | §3.1 (soft ref Employee Master) | **PII — ส่ง id เท่านั้น ห้ามส่งชื่อ** (BR-CSQ-03) |
| `company_id` | uuid | §3.1 | Internal |
| `access_kind` · `access_ref` | enum · text | **§3.3 `case_access_item`** | **Confidential** — `access_ref` เป็นชื่อระบบ/role ภายใน |
| `granted_at` · `revoked_at` · `restored_at` | timestamp | §3.3 `ack_at` | Internal |
| `ack_by` · `ack_ref` | employee ref · text | **§3.3 (ผลตอบกลับจาก Roles & Permissions)** | **PII (id เท่านั้น)** · Internal |
| `revocation_due_at` · `last_working_day` | timestamp · date | §3.1 | Internal |
| `overdue_hours` · `pending_count` · `revoked_count` · `total_count` · `retry_count` | int | §3.3 computed (`is_overdue`) | Internal |
| `pending_access_kinds[]` | enum[] | §3.3 | **Confidential — ส่งเป็น `access_kind` (ชนิด) เท่านั้น ห้ามส่ง `access_ref` รายตัวใน event ที่กระจายกว้าง** |
| `severity` | enum (`warning` · `high` · `critical`) | computed จาก `overdue_hours` | Internal · **การตัดสินระดับความรุนแรงสุดท้ายเป็นของ Engine — feature ส่งข้อเท็จจริงเท่านั้น** |
| `termination_reason` | enum | §3.1 | **Confidential — ส่งเฉพาะใน E4** (จำเป็นต่อการประเมินความเสี่ยง) · **ห้ามส่งใน E2/E3 ที่กระจายกว้างกว่า** |
| `ordered_by` · `ordered_at` · `cancel_reason` | employee ref · timestamp · text | §3.1 | PII (id) · Confidential |
| `delegate_employee_id` · `expires_at` | uuid · timestamp | §3.3 (E7 · S-56) | **PII (id)** · Internal |
| **`reversal_of`** | text (event ref) | E5 | **บังคับใน E5** — ชี้ event `offboard.access_revoked` เดิม (**BR-CSQ-04** — ห้ามลบ/แก้ผลเดิม) |
| `idempotency_key` | text | ระบบ | **บังคับทุก event** — unique ต่อ (`F-HR-ONBOARD`, `case_id`, `access_ref`, action) (**BR-CSQ-02**) |
| **ไม่มีจำนวนเงินทุกชนิด** | — | BR-18 | ✅ |

**Business Rules ที่ FRD ต้องมี (§05_RULES หัวข้อ "ผลกระทบ 7C (CSQ)"):**

| BR | เนื้อหาที่ใช้กับ On/Offboard |
|---|---|
| BR-CSQ-01 | ทุก event ในใบนี้ยิงเข้า Engine ผ่าน `POST /csq/events` ตาม Envelope — **ห้ามเขียนผลรายท่อลงตารางของ feature** |
| BR-CSQ-02 | `idempotency_key` unique ต่อ (feature, case, access_ref, action) — **สำคัญเป็นพิเศษเพราะ E3 ยิงซ้ำตามรอบ** (ต้องแยกด้วย `retry_count`/หน้าต่างเวลา ไม่ใช่ยิงซ้ำ key เดิม) |
| BR-CSQ-03 | payload **ห้ามพก field ชั้น Restricted/Confidential ดิบ** — ส่ง `employee_id` ไม่ส่งชื่อ · ส่ง `pending_access_kinds[]` ไม่ส่ง `access_ref` รายตัวในเหตุการณ์ที่กระจายกว้าง |
| BR-CSQ-04 | **การคืนสิทธิ์ (E5) ต้องมี `reversal_of` ชี้ event เดิม — ห้ามลบ/แก้ผลเดิม** (ตรงกับ BR-14 ของ PREBRIEF ที่บังคับว่าคืนสิทธิ์ = คำขอใหม่ ไม่ใช่การย้อนสถานะ) |
| BR-CSQ-05 | **feature ไม่ประกาศและไม่คำนวณท่อ OC และ DC ระดับเอกสาร** (มาจาก OP และ DOA engine) |
| **BR-CSQ-06** *(เพิ่มเฉพาะ feature นี้)* | **ห้ามยิง `offboard.access_revoked` จากการกระทำของคนในหน้าจอ** — ยิงได้เฉพาะเมื่อได้ **ผลตอบกลับจริงจาก Roles & Permissions** (BR-04) · **ไม่มี checkbox ใดในหน้าจอที่ทำให้ event นี้เกิดได้** (FN-39) |

## §5 Register Checklist (ก่อน deploy)

- [ ] ยืนยัน **`profile_id = CSQ-HRONB`** กับ Profile Registry (OQ-CSQ-02)
- [ ] ตรวจว่า **ไม่มี `oc` · ไม่มี `dc` · ไม่มี `sc`** ใน payload ที่ส่ง register — **ทั้งสามตัวถูก reject 422 จริง ไม่ใช่กฎบนกระดาษ** · ⭐ **ตรวจ `oc` เป็นพิเศษ เพราะ feature นี้มี checklist/SOW จริง**
- [ ] ตรวจว่า Engine ยอมรับ **event ที่ยิงต่อรายการ (E2) พร้อม event สรุป `is_final = true`** โดยไม่นับซ้ำ (OQ-CSQ-03)
- [ ] ตรวจว่า Engine ยอมรับ **event ที่ยิงซ้ำตามรอบ (E3)** โดยแยกด้วย `retry_count`/หน้าต่างเวลา ไม่ตีว่าเป็น duplicate (OQ-CSQ-04)
- [ ] ตรวจว่า Engine ยอมรับ **`config_version_ids.employment_term = null`** ถ้ามีการส่งก้อนเวอร์ชันเข้ามา — เพราะ HR Configuration ยังไม่เผยแพร่คีย์นี้ (**OQ-STD-OB3 ← OQ-STD-06**) · **คู่ขนานกับ OQ-CSQ-02 ของ F-HR-ROSTER ที่ต้องยอมรับ `shift_rule = null`**
- [ ] dev wire `emit` ที่ transition จริง (T-1/T-2 · T-4…T-6 · T-8 · T-11 · T-14) + จุดที่ได้ผลตอบกลับจาก Roles & Permissions + scheduler ของ E3
- [ ] deploy → ตรวจว่าแถวใน **Profile Registry** เปลี่ยนเป็น **เชื่อมแล้ว** · ตรวจ Event Log ว่า event แรกประทับผลถูกท่อ (SecC) ไม่ค้าง "ยังไม่ประเมิน"
- [ ] **ไม่มีการ์ดผล 7 ท่อในหน้าจอของ feature นี้** — มีได้แค่ลิงก์ "ดูผลกระทบ" ไปหน้า Consequence พร้อม `// TODO: ENG-CSQ`

## §6 Open Questions

| # | ประเด็น | ค่าที่ใช้ไปก่อน | เจ้าภาพ |
|---|---|---|---|
| OQ-CSQ-01 | **E7 `offboard.temp_access_delegated`** ควรเป็น SecC หรือไม่ประกาศ (เป็นการให้สิทธิ์ชั่วคราวแก่บุคคลที่สาม) | **ประกาศเป็น SecC** `[DEFAULT — รอยืนยัน]` — การให้คนหนึ่งเข้าถึงข้อมูลของอีกคนคือการเปลี่ยนสิทธิ์เต็มตัว | Architect / Policy Center |
| OQ-CSQ-02 | `profile_id` จริง | **`CSQ-HRONB`** `[DEFAULT — รอยืนยัน]` | Architect (7C Engine) |
| OQ-CSQ-03 | **E2 ยิงต่อรายการ + event สรุป** — Engine นับซ้ำหรือไม่ | ยิงต่อรายการ + `is_final` `[ASSUMED]` — **หลักฐานต้องอยู่ระดับรายการ** | Architect (ENG-CSQ) |
| OQ-CSQ-04 | **E3 ยิงซ้ำตามรอบ** — Engine ถือเป็น duplicate หรือไม่ | แยกด้วย `retry_count` + หน้าต่างเวลา `[ASSUMED]` | Architect (ENG-CSQ) |
| OQ-CSQ-05 | **ควรมีท่อ EC เมื่อมี Rate Card ในอนาคตหรือไม่** (ต้นทุนตำแหน่งว่าง/ต้นทุนการเข้า-ออกงาน) | **ไม่ประกาศรอบนี้** — ไม่มีฐานคิด และ scope ตัดเรื่องเงิน · **ห้ามใส่ตัวเลขที่คำนวณเอง (G7)** | Strike / Architect |

## Quality Gate (self-check)

| # | เช็ค | ผล |
|---|---|---|
| G1 | ไม่มี event ไหนประกาศท่อ `oc` | ✅ — §3 อธิบายเหตุผลชัดว่า checklist ผูก SOW จึงยิ่งต้องไม่ประกาศ · FN-63 พิสูจน์ |
| G2 | ไม่มี event ไหนประกาศ `dc` เพราะการอนุมัติ | ✅ — feature มี DOA จริง 3 action จึงยิ่งต้องไม่ประกาศ |
| G3 | ไม่มี event ไหนประกาศ `sc` | ✅ |
| G4 | ทุก event มี trigger point อ้างได้จริง | ✅ 7/7 อ้าง PREBRIEF §5/§4/§3.3 (จะแทนด้วย FRD § ที่ S5) |
| G5 | ทุก payload field มีจริงใน data dict ของ feature | ✅ อ้าง §3.1 · §3.3 ทุก field · **ไม่มี field ที่แต่งขึ้นใหม่** |
| G6 | event ที่ยิง EC ระบุ `kind` ครบ | ✅ **N/A — ไม่ประกาศ EC** (พร้อมเหตุผลใน §3) |
| G7 | EC จากเวลา/แรงงานที่ไม่มี Rate Card ระบุ `basis: declared` | ✅ **N/A — ไม่ประกาศ EC และไม่ใส่ตัวเลขเงินใด ๆ** (BR-18) |
| G8 | ค่าที่ยังไม่ยืนยันติด `[DEFAULT — รอยืนยัน]` ครบ | ✅ `profile_id` · E7 · OQ-CSQ-03/04 |
| G9 | `event_id` ไม่ชนกับ catalog เดิมโดยความหมายซ้อน | ✅ ใช้ prefix `onboard.` / `offboard.` + กริยาที่จบแล้ว · **ไม่ทับ `roles.*` ของ Policy Center** (นั่นคือมุมของผู้ถือทะเบียนสิทธิ์ · ที่นี่คือมุมของกระบวนการเข้า-ออกงาน) — **cross-check ตอน register** |
