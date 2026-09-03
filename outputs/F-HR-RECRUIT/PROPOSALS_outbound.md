# PROPOSALS (outbound) — F-HR-RECRUIT · F127 · สรรหา / Recruit

> รวบรวมจากงาน WF-01 รอบนี้ (2026-09-03) — สิ่งที่ **ต้องส่งกลับให้คนอื่นเคาะ/ตั้งค่า** ก่อน dev เอาไปทำจริง
> ทุกข้อ = ของค้างที่ **AI ตัดสินเองไม่ได้** (ยกเป็น OQ) หรือ **ต้องแก้ที่ feature/ระบบอื่น** (นอกขอบเขตรอบนี้)
> สถานะ verdict ทุก gate = **ไม่มี BLOCK** — ข้อล่างเป็น WARN/OQ ที่ไม่ขวางการส่งเอกสาร แต่ต้องเคลียร์ก่อน wire ระบบจริง

---

## A. Open Questions — รอ BA/PM/พี่เบิร์ดเคาะ

| OQ | เรื่อง | ทำไมต้องเคาะ | ใครตอบ | มติชั่วคราวที่ใช้ในเอกสาร |
|---|---|---|---|---|
| **OQ-15** | On/Offboard **inbound handoff ยังไม่ถูกออกแบบ** | FRD F-HR-ONBOARD ไม่มี endpoint/event ให้ Recruit ยิง "เริ่ม onboarding" · onboarding บังคับพนักงานต้องมีใน Employee Master ก่อน (`ERR_EMPLOYEE_NOT_FOUND`) — แต่ Recruit ไม่สร้าง employee (BR-05) → **ใครสร้าง employee ระหว่างกลาง = ยังไม่มีคำตอบ** | BA + เจ้าของ F064 On/Offboard | FN-11 = **outbound event stub** (`recruit.candidate.hired` soft-linkage · nullable `candidate_ref` กรอกมือ) · **ไม่ mock หน้าจอ feature ที่ยังไม่มี** (LOCK-LINKAGE) |
| **OQ-16** | PDPA **retention period** ของข้อมูลผู้สมัคร | FIX-03 กลับมติเดิม "ไม่มีวันหมดอายุ" → ต้องอ่านระยะเก็บ/ลบ/anonymize จาก **Policy Center** · ตอนนี้ HTML แสดง "ตามนโยบาย Policy Center (รอกำหนดระยะ)" | Strike / พี่เบิร์ด (PDPA owner) | retention = **display-only** อ่านจาก config กลาง (ยังไม่ผูกค่า) · CSQ event `recruit.candidate_stored.retention_until` รอค่านี้ |
| **OQ-17** | ปิดอัตรา (req) **guard ผู้สมัครค้าง** | FRD 05_RULES EC-08 ระบุ close mode filled/cancelled + warn "มีผู้สมัครค้าง" · HTML `reqClose()` ตั้ง `status='closed'` เดียว ไม่มี mode/branch/warn (Drift **DR-01**) | BA | dev เพิ่ม mode + guard ตอน bind API-08 · TC-I02 flag ให้ tester รายงาน |
| **OQ-DOA** | **DOA role id ยืนยันไม่ได้ — master หาย** | `references/doa-contract.md` หายจาก install → role `role-hiring-manager` / `role-hr-recruit-head` ตรวจกับ master ไม่ได้ · ยังไม่รู้ว่าระดับผู้บริหารต้องเพิ่มชั้นเซ็นไหม | พี่เบิร์ด (ref A-REC-02) | DOA_BRIEF ทุก role ติด **`[DEFAULT — รอยืนยัน]`** · G1 (role valid) บอกตรงว่าตรวจไม่ได้ · **บล็อกเฉพาะการ wire DOA จริง** ไม่บล็อกเอกสาร |
| **DR-04** | `candTerminate` ยิง `ntf()` แต่ **ไม่มี event ใน NTF_BRIEF** | HTML mock มี toast แจ้งตอน "ไม่ผ่าน/ถอนตัว" แต่ NTF_BRIEF ประกาศแค่ 4 event (interview/stage/offer_sent/offer_result) | BA | ถ้าการ terminate ต้องแจ้งผู้สมัคร → เพิ่ม event ใหม่ใน NTF · ถ้าไม่ → เอา `ntf` ออกตอน wire (ตอนนี้ toast mock ไม่บล็อก) |

---

## B. Dependency / Cross-feature — นอกขอบเขตรอบนี้

| # | รายการ | สถานะ | ข้อเสนอ |
|---|---|---|---|
| DEP-1 | **Manpower (F124)** — `dep` ของ F127 ในทะเบียน | **ยังไม่มีจริง** (PM/BA ยืนยัน) | hook nullable + **warn-only** (ไม่บล็อกเปิดอัตรา) · ผูกจริงเมื่อ F124 เกิด |
| DEP-2 | **Salary Structure (F062)** band | มีจริง — soft-ref อ่านผ่าน `bands/resolve` (API-25) · Recruit ไม่อยู่ในลิสต์ consumer ทางการ | ยืมมุมมอง band · snapshot `version_id` คู่ offer (freeze) · out-of-range = เตือนไม่บล็อก |
| DEP-3 | **Employee Master (F011)** ผู้สัมภาษณ์ | มีจริง — `employees?status=active` (F-EMP-API-01) | snapshot interviewer_id+name+position ณ นัด · Recruitment = Out of Scope ใน EMP |

---

## C. SEC_BRIEF — ยังไม่ทำรอบนี้

Cube_Feature_List มีมาตรฐาน SEC-1 (ทุก feature ทำ SEC_BRIEF ที่ S1.8 · `sec.can()`/`sec.mask` อ้าง F024/F057).
**รอบนี้ยังไม่ทำ SEC_BRIEF** (มติ [AI-DEFAULT] จาก kickoff — PM/BA มอบให้ตัดสินตาม standard แต่ยังไม่ยืนยันว่า Recruit ต้องทำ + ใครถือ).
→ **ข้อเสนอ:** BA เคาะว่า F127 ต้องมี SEC_BRIEF แยกไหม (PII ผู้สมัคร + PDPA เป็นความเสี่ยงสูง — น่าจะต้อง) · การ mask ใน HTML ทำแล้ว (`contactCell` + `PERSONAS.unmask`) แต่ยังไม่มีเอกสาร SEC ทางการ.

---

## D. ข้อเสนอปรับปรุง (ไม่บล็อก · จาก UI Brief §13)

1. Toast error ควรมีปุ่มปิด (ตอนนี้ auto-dismiss อย่างเดียว)
2. Deep-link drawer ผูก hash (`#/recruit/pool/C3`) → refresh-safe + แชร์ลิงก์ได้
3. Pool filter option `pipeline` = dead-branch (โค้ด filter รองรับแต่ไม่มี UI) → เพิ่ม option หรือถอด

---

## E. Backend-deferred (ไม่มีใน prototype · dev ทำตอน bind API)

- EC-10 (NTF retry) · EC-12 (Employee Master deletion) · 6 backend error codes · loading skeleton / 403·500 / optimistic-lock 409 (DR-02/DR-03)
- ทั้งหมด documented ใน FRD DoD §6.4 + TC Coverage Audit — **ไม่ใช่ gap เงียบ**

---

> **สรุปสำหรับผู้ตัดสิน:** เอกสารทั้ง pack ส่ง dev ได้ · ก่อน **wire ระบบจริง** ต้องเคลียร์ OQ-DOA (role id) + OQ-15 (handoff design) เป็นอย่างน้อย · OQ-16/17 + DR-04 + SEC_BRIEF เคาะได้ระหว่าง dev
