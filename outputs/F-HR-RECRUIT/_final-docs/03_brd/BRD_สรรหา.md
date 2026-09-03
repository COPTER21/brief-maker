# BRD — F127 สรรหา (Recruit / Candidate Pool)

> Business Requirements Document · WF-01 · SOW3.2 · Fresh Mode (HTML-first)
> Source of truth: `สรรหา.html` (ผ่าน ux+coverage gate + แก้ตาม REVIEW_FIX_ORDER รอบ 2) · PREBRIEF · FUNCTION_CHECKLIST (21 FN) · STANDARD_BASELINE

---

## Section 1 · Document Info

| หัวข้อ | รายละเอียด |
|---|---|
| BRD ID | BRD-F127-RECRUIT |
| Feature | สรรหา (Recruit / Candidate Pool) |
| Feature Code | F127 · HR Module · Wave W9 |
| Archetype | master + pipeline board (Pattern L kanban สำหรับ candidate stages · master สำหรับ requisition/candidate) |
| ประเภท BRD | New Feature |
| Version | 1.0 |
| Status | **APPROVED (มี Open Questions ค้าง OQ-15, OQ-16 — ไม่บล็อกการเขียน FRD ส่วนที่ไม่พึ่ง 2 ประเด็นนี้)** |
| Owner | BA (bird@2bsimple.com) |
| Stakeholders | HR สรรหา · Hiring Manager · ผู้สมัคร · Strike (integration/PDPA owner) · พี่เบิร์ด (PDPA policy) |
| Declarations | doa ✓ · ntf ✓ · csq ✓ (SecC PDPA + EC optional) · doccfg ✗ · pdfdoc ✗ |
| วันที่ | 2026-09-03 (พ.ศ. 2569) |

### Changelog
- v1.0 (2026-09-03): Initial via brd-generator-full (Fresh Mode · HTML-first). สกัด Screen Inventory จาก `สรรหา.html` · สะท้อนใบสั่งแก้ REVIEW_FIX_ORDER (FIX-01..07) · บันทึก OQ-15 (inbound handoff) + OQ-16 (PDPA retention) เป็น Open Questions

---

## Section 2 · Business Context

### 2.1 ปัญหา / โอกาส
องค์กรยังไม่มีระบบกลางจัดการงานสรรหา — การเปิดอัตรา, ทะเบียนผู้สมัคร, การเลื่อนสถานะใน pipeline, การนัดสัมภาษณ์/ประเมิน และการออกข้อเสนอจ้าง กระจายอยู่นอกระบบ ทำให้ (1) ไม่มี audit trail ของการอนุมัติเปิดอัตรา/ข้อเสนอ (2) ข้อมูลผู้สมัครที่เป็น PII ไม่ถูกควบคุมตาม PDPA (3) ไม่มีตัวเลข funnel/time-to-hire ให้ HR วัดผล

### 2.2 เป้าหมาย business
- รวมงานสรรหาไว้ที่เมนูเดียว 4 มุมมอง (ตำแหน่งที่เปิด · คลังผู้สมัคร · บอร์ดสรรหา · รายงาน)
- ทุกการเปิดอัตรา + ข้อเสนอจ้าง ผ่านสายอนุมัติ (DOA) ที่ประกาศไว้ — ไม่ hardcode
- คุมข้อมูลผู้สมัครแบบ RESTRICTED + บังคับ consent PDPA ก่อนเก็บ/ดำเนินการ
- ส่งผู้สมัครที่รับแล้วต่อไป On/Offboard เป็น handoff (ไม่ทำ onboarding เอง)

### 2.3 ตัวชี้วัดความสำเร็จ (บังคับวัดได้)

| ตัวชี้วัด | Baseline ปัจจุบัน | Target | วัดยังไง/จากไหน | วัดเมื่อไหร่ |
|---|---|---|---|---|
| Time-to-hire (วันจากเปิดอัตรา → hired) | ยังไม่มี baseline — **ต้องเก็บก่อน launch** | ลด ≥ 20% หลังใช้ครบ 1 ไตรมาส | รายงาน Funnel §Report tab (audit timestamp req.open → cand.hired) | รายเดือน |
| % อัตราที่ผ่าน DOA ครบก่อนประกาศ | 0% (ไม่มีระบบ) | 100% | audit log — req ที่ status=open ต้องมี approval.done=true | รายเดือน |
| % ผู้สมัครที่มี consent PDPA ก่อนเข้า pipeline | ไม่ทราบ (นอกระบบ) | 100% | candidate.consent.ok=true ก่อน stage เลื่อน | ต่อเนื่อง |
| Conversion funnel (สมัคร → สัมภาษณ์ → ข้อเสนอ → รับ) | ยังไม่มี baseline — **ต้องเก็บก่อน launch** | มองเห็น drop-off ทุกขั้น | รายงาน Funnel | รายเดือน |

> คู่ KPI ใน §17.3 — ทุกตัวข้างต้นมี widget/report ใน §18

### 2.4 ที่มา
STANDARD_BASELINE (Odoo Recruitment / D365 Talent / SAP SF Recruiting → MUST 12) + LANE_BRIEF F127 · current-state §3 (decision 2026-08-17 DOA slot picker)

---

## Section 3 · Scope

### 3.1 In Scope
1. เปิดอัตรา (requisition): ตำแหน่ง · จำนวน · ระดับ · ช่วงเงินเดือน (band soft-ref) · hiring manager · manpower_ref (hook nullable)
2. ส่งอนุมัติเปิดอัตรา + ข้อเสนอจ้าง ผ่าน DOA slot picker (ตามตำแหน่ง ไม่ผูกวงเงิน)
3. ประกาศรับ (ภายใน) · ปิดอัตรา (รับครบ/ยกเลิก)
4. คลังผู้สมัคร: เพิ่ม/แก้ผู้สมัคร · ผูก application กับอัตรา · consent PDPA · ตรวจซ้ำ (email/phone เตือน)
5. บอร์ดสรรหา (kanban): เลื่อนสถานะ คัดกรอง → สัมภาษณ์ → ข้อเสนอ → รับเข้าทำงาน + เส้นแยก (ไม่ผ่าน/ถอนตัว/Talent Pool)
6. นัดสัมภาษณ์ + แจ้งเตือนผู้สัมภาษณ์/ผู้สมัคร · ประเมิน (scorecard ต่อผู้สัมภาษณ์)
7. ออกข้อเสนอจ้าง (ตำแหน่ง · เงินเดือนตามระดับ+freeze band version · วันเริ่ม) → DOA → เสนอ → ตอบรับ/ปฏิเสธ
8. รับ (hired) → **ยิง event ส่งเข้า On/Offboard (handoff · soft-linkage)**
9. รายงาน funnel / time-to-hire + filter · Export CSV (ต่อ dev)
10. กติกากลาง: ค้นหา/filter + empty state · confirm+soft archive · validate+กัน double-submit · audit append-only · masking RESTRICTED/PDPA ตาม role

### 3.2 Out of Scope (ตัดโดยมติ — จาก FUNCTION_CHECKLIST §unsupported)

| ไม่ทำ | เหตุผล |
|---|---|
| จ้างจริง / สร้าง employee record / สัญญาจ้าง | [OB-1] On/Offboard เป็นเจ้าภาพ — Recruit ส่ง handoff เท่านั้น |
| ประกาศงานบน job board ภายนอก | hook/integration ภายนอก (SKIP→hook) |
| แบบทดสอบ/assessment · sourcing agency | NICE — ไม่รองรับ |
| offer letter PDF เลขรัน | soft-ref รอบนี้ (ไม่มี doccfg/pdfdoc) |
| สร้าง/แก้ระดับ-band เงินเดือน | อ่าน HR Configuration (#107) — ไม่ CRUD |

### 3.3 Assumptions
- Manpower (F124) **ยังไม่มีจริง** → manpower_ref เป็น hook display-only, null = ไม่บังคับ (เตือนแต่ทำได้)
- Salary Structure band อ่านจาก `GET /api/v1/salary-structure/bands/resolve` (mock) — คืน band + version_id, freeze snapshot คู่ข้อเสนอ
- Employee Master ใช้เป็น person picker ของผู้สัมภาษณ์ (snapshot)
- สายอนุมัติจริงมาจาก F-DLG-001 (Policy Center) — feature ประกาศ slot เท่านั้น

### 3.4 Scope Lock ⭐

| LOCK | ข้อความ | ที่มา |
|---|---|---|
| LOCK-OB1 | ผู้สมัครที่รับ → ส่ง On/Offboard (handoff) · **ไม่ทำ onboarding เอง / ไม่สร้าง employee** | F-HR-ONBOARD S-10, BR-05 |
| LOCK-OB2 | PDPA: consent + retention ผู้สมัคร (CSQ SecC) | S-05, BR-02, BR-06 |
| LOCK-OB3 | offer/req อนุมัติ = DOA (slot picker 2026-08-17) · **ไม่ hardcode สายอนุมัติ** | current-state §3 |
| LOCK-OB4 | เปิดอัตราอ้าง Manpower = hook · null = ไม่บังคับ | A-REC-01 |
| LOCK-OB5 | ข้อมูลผู้สมัคร RESTRICTED · audit append-only | current-state §3 · BR-06,07 |
| LOCK-DOA | DOA offer/req **ไม่ผูก threshold ยอดเงิน** — resolve ตามตำแหน่ง (slot) | PREBRIEF §12 |
| LOCK-DOCCFG | ไม่มีเลขรันเอกสาร (offer letter = soft-ref) | PREBRIEF §12 |

> LOCK ชนะทุก business rule — ถ้าขัด ให้ยึด LOCK + แจ้งใน AI Review. ไม่พบ SCOPE DRIFT (In Scope ทุกข้ออยู่ใต้ LOCK)

---

## Section 4 · User Roles & Permissions

| Role (persona) | เปิด/แก้อัตรา | เพิ่ม/แก้ผู้สมัคร | เลื่อนสถานะ | อนุมัติ (DOA) | บันทึก consent | ดูข้อมูล RESTRICTED |
|---|:--:|:--:|:--:|:--:|:--:|:--:|
| เจ้าหน้าที่สรรหา (recruiter) | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ (ตาม role) |
| ผู้จัดการสายงาน (manager / Hiring Manager) | ✓ | ✓ | ✓ | **✓ (canApprove เฉพาะ manager)** | ✓ | ✓ |
| ผู้ชมทั่วไป (viewer) | ✗ อ่านอย่างเดียว | ✗ | ✗ | ✗ | ✗ | ✗ (mask) |

> viewer = read-only จริง (FIX-02): ซ่อนปุ่มสร้าง/แก้ + guard `viewerRO()` ต้นทุก mutation function กันเส้นทางอ้อม
> persona segment เป็น prototype demo (Iron Rule #105) — ระบบจริงผูกสิทธิ์จาก role master

---

## Section 5 · User Journey (with COSO)

### 5.1 Happy Path — เปิดอัตรา → รับเข้าทำงาน

| # | Step | Route/หน้าจอ | Maker | Checker | Approver | System |
|---|---|---|---|---|---|---|
| 1 | เปิดอัตรา (กรอก req) | `recruit/req` → openReqCreate() | recruiter | — | — | validate fields, กัน double-submit |
| 2 | ส่งอนุมัติเปิดอัตรา | reqSubmitApproval → DOA modal | recruiter | — | **manager** (slot) | doaResolve('req') resolve slot |
| 3 | อนุมัติเปิดอัตรา | DOA slot picker | — | — | **manager** | ครบทุกขั้น → status=approved + NTF |
| 4 | ประกาศรับ | reqAnnounce() | recruiter | — | — | status=open |
| 5 | เพิ่มผู้สมัคร + consent PDPA | `recruit/pool` → openCandCreate() | recruiter | — | — | บังคับ consent ก่อนเก็บ · ตรวจซ้ำ email/phone |
| 6 | ผูก application กับอัตรา | drawer ผู้สมัคร | recruiter | — | — | link cand ↔ req |
| 7 | เลื่อนสถานะ คัดกรอง→สัมภาษณ์ | `recruit/board` candMoveStage() | recruiter | hiring manager | — | guard consent.ok ก่อนเลื่อน · audit |
| 8 | นัดสัมภาษณ์ | drawer tab สัมภาษณ์/ประเมิน | recruiter | — | — | NTF ผู้สัมภาษณ์+ผู้สมัคร |
| 9 | ประเมิน (scorecard) | drawer tab สัมภาษณ์/ประเมิน | ผู้สัมภาษณ์ (snapshot) | hiring manager | — | เก็บ score ต่อผู้สัมภาษณ์ |
| 10 | สร้างข้อเสนอ (freeze band) | drawer tab ข้อเสนอ | recruiter | — | — | bandResolve + snapshot version_id |
| 11 | ส่งอนุมัติข้อเสนอ | openDoaModal('offer') | recruiter | — | **manager** (slot) | doaResolve('offer') |
| 12 | เสนอ → ผู้สมัครตอบรับ | drawer tab ข้อเสนอ | recruiter | — | — | offer.status: pending→approved→sent→accepted |
| 13 | รับเข้าทำงาน + handoff | candHireHandoff() | recruiter | hiring manager | — | filled++ · req ปิดเมื่อครบ · **ยิง event onboarding** |

> **SoD check:** Maker (recruiter สร้าง req/offer) ≠ Approver (manager) ในทุก approval step ✓
> **COSO defaults** ตาม HR module (knowledge/coso-defaults.md): approval = manager, execution = recruiter

### 5.2 Alternative Paths
- **A1 เปิดอัตราไม่มี Manpower** (S-02): manpower_ref=null → เตือน "ยังไม่มีแผนอัตรากำลัง" แต่ทำต่อได้ (hook display-only)
- **A2 ไม่ผ่าน/ถอนตัว** (S-11/S-12): candTerminate → stage = rejected/withdrawn/talent_pool + เหตุผล (audit warn)
- **A3 board เลื่อนถึงขั้นรับ** (FIX-01): กด "ถัดไป" จากขั้นข้อเสนอ — ถ้า offer ยังไม่ accepted → บล็อก + พาไปแท็บข้อเสนอ · ถ้า accepted → route ผ่าน `candHireHandoff()` เส้นเดียวทั้งระบบ

### 5.3 Exception Paths
- **E1 ไม่ยินยอม PDPA** (S-05): consent.ok=false → เลื่อนสถานะไม่ได้ (guard `candMoveStage` dir>0) + toast
- **E2 ผู้สมัครซ้ำ** (S-13): email/phone match → เตือน "อาจเคยสมัคร" (ไม่บล็อก)

---

## Section 6 · Data Entity & Fields

### 6.1 Entity: Requisition (อัตราที่เปิด)

| # | Field | Label UI | Input Type | ค่า/ตัวเลือก | จำเป็น | หมายเหตุ |
|---|---|---|---|---|:--:|---|
| 1 | id / code | รหัสอัตรา | AUTO | REQ-xxxx | ✓ | ไม่ใช่เลขรันเอกสาร (ไม่ doccfg) |
| 2 | position | ตำแหน่ง | TEXT | | ✓ | |
| 3 | count | จำนวน | NUMBER | ≥1 | ✓ | คู่กับ filled |
| 4 | grade_code | ระดับ | DROPDOWN-SINGLE | G3/G4/G5 (จาก HR Config) | ✓ | soft-ref |
| 5 | band | ช่วงเงินเดือน | LOOKUP (read) | bandResolve(grade) → min/mid/max + version_id | ✓ | display จาก Salary Structure |
| 6 | hiring_manager | ผู้จัดการสายงาน | LOOKUP | Employee Master | ✓ | snapshot |
| 7 | manpower_ref | อ้างอัตรากำลัง | LOOKUP (hook) | Manpower F124 | ✗ | **nullable** · display-only |
| 8 | status | สถานะ | AUTO | draft/approved/open/closed/cancelled | ✓ | state machine |
| 9 | approval | สายอนุมัติ | OBJECT | doaResolve('req') steps[] | ✓ | ประกาศ slot · ไม่ hardcode |
| 10 | filled | รับแล้ว | AUTO | 0..count | ✓ | filled++ ตอน hired |
| A | audit fields | — | AUTO | created_by/date, modified_by/date | ✓ | append-only |

### 6.2 Entity: Candidate (ผู้สมัคร) — **RESTRICTED**

| # | Field | Label UI | Input Type | ค่า/ตัวเลือก | จำเป็น | หมายเหตุ |
|---|---|---|---|---|:--:|---|
| 1 | id | รหัสผู้สมัคร | AUTO | | ✓ | |
| 2 | name | ชื่อ-นามสกุล | TEXT | | ✓ | **RESTRICTED** mask ตาม role |
| 3 | contact | ติดต่อ (email/phone) | TEXT | | ✓ | **RESTRICTED** · ใช้ตรวจซ้ำ |
| 4 | resume | เรซูเม่ | FILE/TEXT | | ✗ | |
| 5 | interested_position | ตำแหน่งที่สนใจ | TEXT/LOOKUP | | ✗ | |
| 6 | consent | ความยินยอม PDPA | OBJECT | {ok:bool, date} | ✓ | **gate** ก่อนเก็บ/ดำเนินการ |
| 7 | retention_until | ระยะเก็บ/วันครบกำหนด | DISPLAY-ONLY | อ่านจาก Policy Center | ✗ | **OQ-16** · ห้าม hardcode (`retentionLabel()`) |
| 8 | stage | สถานะ pipeline | AUTO | applied/screening/interview/offer/hired · rejected/withdrawn/talent_pool | ✓ | |
| 9 | scores | ผลประเมิน | ARRAY | scorecard ต่อผู้สัมภาษณ์ | ✗ | |
| 10 | offer | ข้อเสนอ | OBJECT | ดู 6.3 | ✗ | |
| 11 | onboardSent | ส่ง onboarding แล้ว | AUTO | bool | ✓ | true หลัง handoff |
| 12 | reason | เหตุผล (ปฏิเสธ/ถอน) | TEXT | | เมื่อ terminal | |
| A | audit | — | AUTO | append-only | ✓ | |

### 6.3 Entity: Offer (ข้อเสนอจ้าง)

| # | Field | Label UI | Input Type | ค่า | จำเป็น | หมายเหตุ |
|---|---|---|---|---|:--:|---|
| 1 | position | ตำแหน่ง | TEXT | | ✓ | |
| 2 | salary | เงินเดือน | NUMBER | ต้องอยู่ในช่วง band | ✓ | เช็ค in-band |
| 3 | band_version_id | เวอร์ชัน band (freeze) | AUTO | SS-2569-03 | ✓ | **snapshot ณ สร้าง offer** |
| 4 | start_date | วันเริ่มงาน | DATE | | ✓ | ส่งเข้า bandResolve(date) |
| 5 | status | สถานะข้อเสนอ | AUTO | pending/approved/sent/accepted/declined | ✓ | |
| 6 | approval | สายอนุมัติ | OBJECT | doaResolve('offer') | ✓ | ประกาศ slot |

### 6.4 ER Diagram

```
Requisition ──(1:N)──▶ Candidate (application link · cand.req_ref)
Candidate ──(1:1)──▶ Offer (embedded)
Salary Structure ──(referenced by · read)──▶ Requisition.band / Offer.band_version_id  [freeze snapshot]
Employee Master ──(referenced by · read)──▶ Requisition.hiring_manager / Interview.interviewer  [snapshot]
Manpower (F124) ──(hook · nullable)──▶ Requisition.manpower_ref
Candidate(hired) ──(event handoff)──▶ On/Offboard  [OQ-15 · fire-and-forget]
```

---

## Section 7 · User Stories & Acceptance Criteria

- **US-01 (S-01):** ในฐานะ recruiter ฉันเปิดอัตราได้ · **AC:** (1) กรอกครบ → บันทึกเป็น draft (2) ส่งอนุมัติแล้วต้องผ่าน DOA ครบทุกขั้นก่อน status=open
- **US-02 (S-02):** ในฐานะ recruiter ฉันเปิดอัตราแม้ไม่มี Manpower plan · **AC:** (1) manpower_ref=null ได้ (2) แสดงเตือนแต่ไม่บล็อก
- **US-03 (S-03/S-05):** ในฐานะ recruiter ฉันเพิ่มผู้สมัครพร้อมบันทึกความยินยอม PDPA · **AC:** (1) ไม่มี consent → เก็บ/ดำเนินต่อไม่ได้ (2) มี consent → บันทึก date
- **US-04 (S-06):** ในฐานะ recruiter ฉันเลื่อนสถานะผู้สมัครบนบอร์ด · **AC:** (1) consent.ok=false → เลื่อนไม่ได้ (2) ทุกการเลื่อนถูก audit
- **US-05 (S-07):** ในฐานะ recruiter ฉันนัดสัมภาษณ์ · **AC:** (1) เลือกผู้สัมภาษณ์จาก Employee Master (2) ยิง NTF ทั้งผู้สัมภาษณ์และผู้สมัคร
- **US-06 (S-08):** ในฐานะผู้สัมภาษณ์ ฉันบันทึกผลประเมิน · **AC:** (1) score ต่อผู้สัมภาษณ์ (2) เห็นสรุปหลายผู้สัมภาษณ์
- **US-07 (S-09):** ในฐานะ recruiter ฉันสร้างข้อเสนอจ้าง · **AC:** (1) เงินเดือนตรวจ in-band (2) freeze band_version_id (3) ส่ง DOA ก่อนเสนอ
- **US-08 (S-10):** ในฐานะ recruiter ฉันรับผู้สมัครที่ตอบรับข้อเสนอ · **AC:** (1) เฉพาะ offer.status=accepted จึง hired ได้ (2) filled++ · req ปิดเมื่อครบ (3) ยิง event ส่งเข้า On/Offboard
- **US-09 (S-11/S-12):** ในฐานะ recruiter ฉันบันทึกผู้สมัครไม่ผ่าน/ถอนตัว · **AC:** (1) เลือกผล+เหตุผล (2) talent_pool = soft archive
- **US-10 (S-13):** ในฐานะ recruiter ฉันเห็นการเตือนผู้สมัครซ้ำ · **AC:** (1) match email/phone → เตือน (2) ไม่บล็อกการบันทึก
- **US-11 (S-14):** ในฐานะ HR ฉันดูรายงาน funnel/time-to-hire · **AC:** (1) เห็น conversion ทุกขั้น (2) filter ได้
- **US-12 (S-15):** ในฐานะ recruiter ฉันปิดอัตรา · **AC:** (1) รับครบ → closed อัตโนมัติ (2) ยกเลิกผ่าน confirm

---

## Section 8 · Status & Lifecycle

### 8.1 Requisition
```
draft ──ส่งอนุมัติ(DOA)──▶ (pending approval) ──อนุมัติครบ──▶ approved ──ประกาศ──▶ open
open ──filled>=count──▶ closed
draft/approved/open ──ยกเลิก──▶ cancelled
```

### 8.2 Candidate (pipeline)
```
applied ─▶ screening ─▶ interview ─▶ offer ─▶ hired(→onboarding handoff)
   └─(ทุกขั้น)─▶ rejected / withdrawn / talent_pool
```
Guard: เลื่อน dir>0 ต้อง consent.ok=true · เข้า offer ต้องมี offer object · เข้า hired ต้อง offer.status=accepted (route ผ่าน candHireHandoff)

### 8.3 Offer
```
pending ──DOA อนุมัติ──▶ approved ──เสนอ──▶ sent ──ผู้สมัครตอบ──▶ accepted / declined
```

| State | Trigger | Next |
|---|---|---|
| req.draft | reqSubmitApproval | pending |
| req.pending | อนุมัติครบทุก slot | approved |
| req.approved | reqAnnounce | open |
| req.open | filled≥count | closed |
| cand.offer | offer.accepted + hire confirm | hired + event |
| offer.sent | ผู้สมัครตอบรับ | accepted |

---

## Section 9 · Business Rules + Validation (with Tags)

| Rule | ข้อความ | ประเภท | Tag | ใครเปลี่ยน/บ่อย | ที่มา |
|---|---|---|---|---|---|
| BR-01 | req ต้องอนุมัติ (DOA) ครบก่อนประกาศ (open) | Prevent | FIXED | — | 🤖 |
| BR-02 | เก็บผู้สมัครได้เมื่อมี consent PDPA + ภายในระยะ retention | Prevent | **CONFIGURABLE** (retention period) | Policy Center admin / เป็นระยะ | ✅ (OQ-16 ค้างค่า) |
| BR-03 | ทุก pipeline transition ต้อง audit | Trigger | FIXED | — | 🤖 |
| BR-04 | offer ต้องอนุมัติ (DOA) ก่อนเสนอ · เงินเดือนตามระดับ (band soft-ref) | Prevent | FIXED (flow) | — | 🤖 |
| BR-05 | hired → ยิง handoff On/Offboard (event · ไม่สร้าง employee เอง) | Trigger | FIXED | — | ✅ (OQ-15 ค้างฝั่งรับ) |
| BR-06 | ข้อมูลผู้สมัคร RESTRICTED · masking + PDPA ตาม role | Error/Prevent | FIXED | — | 🤖 |
| BR-07 | audit append-only · soft archive (talent pool) | — | FIXED | — | 🤖 |
| BR-08 | อัตราอ้าง Manpower = hook · null ไม่บังคับ (เตือน) | Warning | CONFIGURABLE (เมื่อ F124 มีจริง) | — | 🤖 |
| BR-09 | snapshot ผู้สัมภาษณ์ + band version_id (freeze) | Trigger | FIXED | — | 🤖 |
| BR-10 | duplicate detect email/phone → เตือน ไม่บล็อก | Warning | CONFIGURABLE (match field) | Admin | 🤖 |
| VR-01 | field บังคับ (position/count/grade/hiring_manager) ต้องกรอก | Error | FIXED | — | field-level error (FIX-05) |
| VR-02 | กัน double-submit (RC.busy + loading state) | Prevent | FIXED | — | FIX-07 Iron Rule #44 |
| VR-03 | offer.salary ต้องอยู่ในช่วง band [min,max] | Warning/Error | CONFIGURABLE | HR Config | ✅ |
| VR-04 | DOA สายอนุมัติ resolve จาก slot — **ห้าม hardcode** | Prevent | DYNAMIC (Policy Center) | — | ✅ (declaration) |
| VR-05 | viewer = read-only · guard ทุก mutation | Prevent | FIXED | — | FIX-02 |

### 9.5 สรุประดับความยืดหยุ่น

| Rule | ระดับ | เหตุผล | ที่มา |
|---|---|---|---|
| BR-02 (retention period) | Admin Panel (Policy Center) | ระยะเก็บเป็น config เปลี่ยนตามนโยบาย PDPA | 🤖 AI-inferred → **OQ-16 (ต้องยืนยันค่าก่อน launch)** |
| BR-08 (manpower binding) | Admin Panel | เปลี่ยนเมื่อ F124 พร้อม | 🤖 |
| BR-10 (duplicate match field) | Admin Panel | เลือก field ที่ใช้ตรวจซ้ำ | 🤖 |
| VR-03 (salary in-band) | Admin Panel (HR Config) | อ่าน band จาก Salary Structure | 🤖 |
| VR-04 (DOA chain) | Rule Management (Policy Center F-DLG-001) | สายอนุมัติ = declaration ประกาศ ไม่ hardcode | ✅ Stakeholder (DOA declaration) |

> **Escalation:** VR-04 = DYNAMIC + Policy Center → อยู่ใน §15 OQ (declaration รอเคาะ) · BR-02 retention = 🤖 + config ที่ยังไม่มีค่า → OQ-16

---

## Section 10 · Edge Cases

### 10.1 Edge Cases ที่ PREBRIEF/RIF ระบุ (default ☑)
- ☑ no-consent → บล็อกการเลื่อน/เก็บ (E1)
- ☑ duplicate email/phone → เตือน ไม่บล็อก (E2)
- ☑ เปิดอัตราไม่มี Manpower → เตือน ทำได้ (A1)
- ☑ hired → onboard handoff (soft-linkage)
- ☑ board ข้ามขั้นไป hired โดยไม่ผ่าน offer accepted → บล็อก (FIX-01)
- ☑ viewer เรียก mutation ทางอ้อม → guard บล็อก (FIX-02)
- ☑ microcopy PDPA ต้องไม่ระบุ "เก็บไม่มีวันหมดอายุ" (FIX-03)

### 10.2 Edge Cases จาก AI Pattern Matching (☐ = แนะนำ · BA confirm ที่ SOW3.7)
- **PM (Permission):** ☐ role เปลี่ยนกลางทาง (recruiter→viewer) ขณะเปิด drawer → re-guard ตอน submit
- **DI (Lookup):** ☐ band version เปลี่ยนหลังสร้าง offer แต่ก่อน accept → ยึด freeze snapshot (ไม่ re-resolve) · ☐ hiring_manager/interviewer ถูกลบจาก Employee Master → ใช้ snapshot
- **ST (Status/Workflow):** ☐ req ถูกปิด (closed/cancelled) ขณะมีผู้สมัครค้าง pipeline → ต้องกำหนดพฤติกรรม (OQ) · ☐ offer declined หลัง req ปิด
- **EM (Notification):** ☐ ยิง NTF ล้มเหลว → retry/queue (ผูก ENG-NOTIFY)
- **CA (Concurrent):** ☐ 2 recruiter เลื่อนสถานะผู้สมัครคนเดียวกันพร้อมกัน → last-write + audit ทั้งคู่
- **⚠️ ยกเป็น OQ ทันที (กระทบข้อมูล/สิทธิ์):** consent ถูกถอนภายหลัง (withdraw consent) → ข้อมูลที่เก็บไปแล้วต้องทำอย่างไร → **ผูก OQ-16**

---

## Section 11 · Impact / Regression
New Feature — ไม่มี regression ของเดิม. ผลกระทบข้ามระบบดู §12.1 (Downstream). Regression scope เมื่อ integrate จริง: On/Offboard (OQ-15), Salary Structure API, ENG-NOTIFY, Policy Center (DOA + retention).

---

## Section 12.1 · Value Stream & Downstream Impact ⭐

**Value Stream:** HR — Hire-to-Retire · Recruit เป็นต้นน้ำของสาย "หา→รับ→เข้าทำงาน"

**Upstream (รับจาก):**
- Manpower Planning (F124) → trigger เปิดอัตรา (hook · ยังไม่มีจริง = null-able)
- HR Configuration (#107) / Salary Structure → grade + band (read)
- Employee Master → hiring manager + ผู้สัมภาษณ์ (read/snapshot)

**Downstream Impact Map:**

| ปลายทาง | ข้อมูลที่ไหลไป | Trigger | ถ้า Recruit เปลี่ยน/ยกเลิก |
|---|---|---|---|
| On/Offboard (F-HR-ONBOARD) | event: candidate hired (id, position, start_date, offer snapshot) | cand.stage=hired | **OQ-15** — ฝั่งรับยังไม่ออกแบบ · ตอนนี้ fire-and-forget ไม่รอ ack |
| Employee Master | (ทางอ้อม ผ่าน On/Offboard — Recruit ไม่สร้าง employee เอง) | onboarding เสร็จ | LOCK-OB1 |
| Salary Structure | อ่านอย่างเดียว — freeze band_version_id คู่ offer | สร้าง offer | ถ้า band แก้ภายหลัง → offer เดิมยึด snapshot |
| Notification (ENG-NOTIFY) | event: นัดสัมภาษณ์ · ข้อเสนอ · ผลคัดเลือก · ตอบรับ | state transition | ผูก NTF declaration |
| Policy Center (F-DLG-001) | resolve สายอนุมัติ req/offer | ส่งอนุมัติ | DOA declaration |
| Policy Center (PDPA config) | retention period ผู้สมัคร | เก็บผู้สมัคร | **OQ-16** — ครบกำหนด ลบ/anonymize |

**ผลกระทบแนวขวาง:** บัญชี/สต๊อก = ไม่มี (HR master flow) · รายงาน = funnel/time-to-hire feed HR dashboard · งบประมาณ = อัตรากำลัง (ผ่าน Manpower เมื่อมีจริง)

---

## Section 12.3 · Existing System Reference

| Rule/ความสามารถ | ระดับ | มีอยู่แล้ว? | Reference |
|---|---|:--:|---|
| DOA สายอนุมัติ (req/offer) | Rule Management | ✅ (F-DLG-001 Policy Center) | ประกาศผ่าน doa-declaration → DOA_BRIEF |
| Notification events | Config | ✅ (F-NOTIFY / ENG-NOTIFY) | ประกาศผ่าน ntf-declaration → NTF_BRIEF |
| Salary band resolve | Config (read) | ✅ (Salary Structure API-25) | `GET /salary-structure/bands/resolve` |
| PDPA retention period | Admin Panel | ❌ ยังไม่มีค่า | Policy Center — **OQ-16** |
| Manpower binding | hook | ❌ (F124 ยังไม่ dev) | display-only |
| RESTRICTED masking | Config | ⚠️ บางส่วน | ต้องผูก role master จริง |

---

## Section 13 · Delivery Phases

**Phase 1 — Feature Launch (ห้าม hardcode ตั้งแต่วันแรก):**
- Requisition/Candidate/Offer entity + state machine (seed) · pipeline board · consent gate · duplicate warn · audit append-only · funnel report
- DOA resolve ผ่าน slot (อ่าน Policy Center) · NTF ผ่าน ENG-NOTIFY · band resolve + freeze
- masking RESTRICTED ตาม role · viewer guard

**Phase 2 — Admin Panel (config ที่ยังไม่มีค่า):**
- PDPA retention period (OQ-16) · duplicate match field · salary in-band tolerance

**Phase 3 — Rule Management:**
- DOA chain management (F-DLG-001) — declaration-driven

**Phase 4 — Engine/Integration:**
- Inbound handoff On/Offboard (OQ-15) — ออกแบบฝั่งรับ + ack · Manpower binding เมื่อ F124 พร้อม

---

## Section 14 · Dev Requirements Summary "ใบสั่ง"

### 14.1 Config Foundation
- DOA entry `DOA-REQ-OPEN-001` / `DOA-OFFER-001` — slot-based (role-hiring-manager, role-hr-recruit-head) ไม่มีวงเงิน · **อ่านจาก Policy Center ไม่ hardcode**
- Retention config (Policy Center) — **ยังไม่มีค่า (OQ-16)** ห้ามใส่ default hardcode
- Salary band API (read) + freeze version_id คู่ offer
- NTF events: interview_scheduled, offer_sent, selection_result, candidate_accepted (ไม่นับ doa_* ที่มาจาก DOA engine อัตโนมัติ)

### 14.2 ข้อกำหนดจาก Tag
- VR-04 (DOA) = DYNAMIC → resolve runtime จาก Policy Center · **ห้าม hardcode สายอนุมัติในโค้ด feature**
- BR-02 (retention) = CONFIGURABLE → อ่าน period จาก Policy Center config · แสดง retention_until display-only
- VR-03 (salary in-band) = CONFIGURABLE → อ่าน band จาก Salary Structure (ใช้ของที่มีอยู่แล้ว ไม่สร้างใหม่)
- BR-08/BR-10 = CONFIGURABLE → Admin Panel

### 14.3 Edge Cases สำคัญที่ต้อง handle
- consent gate ต้นทุกการเลื่อน/เก็บ · freeze band snapshot (ไม่ re-resolve) · viewer guard ต้นทุก mutation · hired route ผ่าน candHireHandoff() เส้นเดียว (FIX-01)

### 14.4 WARNING ที่รอข้อสรุป (ห้ามเริ่มพัฒนาส่วนที่เกี่ยว)
- **OQ-15** inbound handoff On/Offboard — Strike · FRD §Integration
- **OQ-16** PDPA retention period + withdraw consent behavior — Strike/พี่เบิร์ด · FRD §PDPA + Policy Center

### 14.5 Regression Scope
N/A (New Feature) — ดู §11 สำหรับ integration regression เมื่อผูกระบบจริง

---

## Section 14.6 · Screen Inventory + UI Signals (หยาบ — ส่งต่อ FRD)

**1 feature = 1 เมนู (Iron Rule) · 4 แท็บในมุมมองเดียว + drawer + modals**

| # | ชื่อหน้า/มุมมอง | route (จาก HTML) | ประเภทหยาบ | ผู้ใช้หลัก | หน้าที่ (business) | หมายเหตุ |
|---|---|---|---|---|---|---|
| P-01 | ตำแหน่งที่เปิด (Requisition) | `recruit/req` | หน้ารายการ + action สร้าง | recruiter, manager | เปิดอัตรา · ส่งอนุมัติ DOA · ประกาศ · ปิด | ปุ่มสร้างซ่อนจาก viewer |
| P-02 | คลังผู้สมัคร (Candidate Pool) | `recruit/pool` | หน้ารายการ + action สร้าง | recruiter, manager | ทะเบียนผู้สมัคร · consent PDPA · RESTRICTED | ตรวจซ้ำ · masking ตาม role |
| P-03 | บอร์ดสรรหา (Pipeline) | `recruit/board` | kanban (Pattern L) | recruiter, hiring manager | เลื่อนสถานะ คัดกรอง→สัมภาษณ์→ข้อเสนอ→รับ + เส้นแยก | guard consent + offer accepted |
| P-04 | รายงานการสรรหา (Funnel) | `recruit/report` | รายงาน (ดู+export) | HR, manager | funnel · time-to-hire · Export CSV | |
| D-01 | ลิ้นชักผู้สมัคร | drawer (RC.dctx) | หน้ารายละเอียด (4 แท็บ) | recruiter, manager | ดู/จัดการผู้สมัครรายคน | tabs: `detail`/`assess`/`offer`/`history` |
| M-01 | ฟอร์มเปิดอัตราใหม่ | openReqCreate() | ฟอร์มสร้าง | recruiter | กรอก req + ส่งอนุมัติ | validate + double-submit guard |
| M-02 | ฟอร์มเพิ่มผู้สมัคร | openCandCreate() | ฟอร์มสร้าง | recruiter | กรอกผู้สมัคร + consent | banner PDPA (retention จาก Policy Center) |
| M-03 | DOA slot picker | openDoaModal('req'/'offer') | หน้ายืนยัน (approval) | manager | อนุมัติตาม slot (avatar+ตำแหน่ง+ชื่อ) | ไม่ผูกวงเงิน |
| M-04 | นัดสัมภาษณ์ | drawer tab assess | ฟอร์ม | recruiter | เลือกผู้สัมภาษณ์ + NTF | |
| M-05 | บันทึกผล (ไม่ผ่าน/ถอนตัว) | openReasonModal() | หน้ายืนยัน | recruiter | เลือกผล + เหตุผล | |
| M-06 | ยืนยันรับเข้าทำงาน | candHireHandoff confirm | หน้ายืนยัน | recruiter | ยิง event onboarding | soft-linkage |

**สรุปจำนวนหน้า:** ~4 มุมมองหลัก (1 เมนู) + 1 drawer (4 แท็บ) + ~6 modal/overlay

**UI Signals ส่งต่อ FRD (signal ไม่ใช่ spec):**
- เป็น Document/Transaction? **บางส่วน** — req + offer มี approver (DOA) แต่ **ไม่มีเลขรัน/ไม่พิมพ์เอกสาร** (offer letter = soft-ref) → FRD เลือก pattern เอง
- print/PDF? **ไม่มี** (รอบนี้)
- NON-STANDARD? ไม่มี — archetype master+kanban มาตรฐาน
- overlay registry: drawer + modal + confirm + toast · Esc chain · persona demo strip (Iron Rule #105 ไม่อยู่ page header)
- consent gate + RESTRICTED masking = state-driven UI (ผูก role/persona) → FRD ระบุ permission matrix

---

## Section 15 · Open Questions

| รหัส | คำถาม | สถานะ | ผู้เคาะ | กระทบ |
|---|---|---|---|---|
| **OQ-15** | Inbound handoff: hire → สร้าง Employee + เปิด On/Offboard จริงอย่างไร? ตอนนี้ soft-linkage ยิง event อย่างเดียว (จงใจค้าง · comment ในโค้ด) — ต้องออกแบบฝั่งรับ + ack | ⚠️ รอ | Strike | FRD §Integration |
| **OQ-16** | PDPA retention ผู้สมัคร: ระยะเก็บกี่เดือน/ปี? ครบกำหนดแล้ว ลบหรือ anonymize? Talent Pool ต่ออายุ consent อย่างไร? withdraw consent แล้วข้อมูลที่เก็บทำอย่างไร? — **เป็น config ที่ Policy Center ห้าม hardcode** · แทนที่สมมติเดิม "เก็บไม่มีวันหมดอายุ" ที่ถูกแก้ทิ้งแล้ว (FIX-03) | ⚠️ รอ | Strike / พี่เบิร์ด | FRD §PDPA + Policy Center |
| OQ-17 | req ถูกปิด (closed/cancelled) ขณะมีผู้สมัครค้าง pipeline → พฤติกรรม? (Edge 10.2 ST) | ⚠️ รอ | BA/HR | §8, §10 |
| Note | Manpower hook (F124) display-only ไม่บังคับ — ตรงกับสถานะ F124 ที่ยังไม่ dev (ไม่ใช่ OQ · ยืนยันแล้ว) | ✅ | — | — |
| Note | Declarations (doa/ntf/csq) — **ผู้ใช้/BA เลือก ไม่เดา** · รันหลัง step 7 เฉพาะที่เลือก | — | ผู้ใช้ | — |

---

## Section 16 · Security & Compliance

### 16.1 Preset
**P6 — HR / PII Sensitive (15 controls)** · เหตุผล: ข้อมูลผู้สมัคร = PII RESTRICTED ภายใต้ PDPA + CSQ SecC declaration

### 16.2 Applicable Standards
PDPA (พ.ร.บ.คุ้มครองข้อมูลส่วนบุคคล) ✅ · ISO 27001 (access control) ✅ · COSO (SoD approval) ✅ · GDPR-aligned (storage limitation) ✅

### 16.3 Control Checklist (สำคัญ)

| Control | Required | Implementation Notes |
|---|:--:|---|
| Field-level masking (RESTRICTED) | ✓ Must | mask name/contact ตาม role · viewer เห็นน้อยสุด |
| Consent management (PDPA) | ✓ Must | consent gate ก่อนเก็บ/ดำเนินการ · เก็บ date |
| Retention/storage limitation | ✓ Must | period จาก Policy Center · retention_until display · **OQ-16** |
| Access control (RBAC) | ✓ Must | recruiter/manager/viewer · canApprove=manager |
| SoD (Maker≠Approver) | ✓ Must | recruiter สร้าง / manager อนุมัติ |
| Audit trail (append-only) | ✓ Must | ทุก create/แก้/เลื่อน/อนุมัติ |
| DOA (delegation) | ✓ Must | slot-based · ไม่ hardcode |
| Data minimization | ○ Optional | เก็บเท่าที่จำเป็นต่อการสรรหา |

### 16.4 Risk Statement

| Risk | คำอธิบาย | Mitigated by |
|---|---|---|
| R-PII | ข้อมูลผู้สมัครรั่ว/เข้าถึงเกินสิทธิ์ | masking + RBAC + audit (BR-06, VR-05) |
| R-RETENTION | เก็บข้อมูลเกินระยะ = ผิด PDPA | retention config + OQ-16 (ห้าม hardcode "ไม่มีวันหมดอายุ") |
| R-APPROVAL | เปิดอัตรา/offer โดยไม่ผ่านอนุมัติ | DOA gate (BR-01, BR-04) · SoD |
| R-DATADRIFT | band เปลี่ยนหลัง offer | freeze band_version_id (BR-09) |

---

## Section 17 · Health Check

### 17.1 SLA
| Step | เวลาควบคุม | Owner |
|---|---|---|
| ส่งอนุมัติ req → อนุมัติ | ตาม DOA policy | Hiring Manager |
| ส่งข้อเสนอ → ผู้สมัครตอบรับ | (config) | recruiter ติดตาม |
| นัดสัมภาษณ์ → ประเมิน | (config) | ผู้สัมภาษณ์ |

### 17.2 Control Points
map จาก §16: consent gate · masking · DOA approval · audit — ทุกจุด runtime มี control point ตรวจได้

### 17.3 KPI
| KPI | ประเภท | คู่ตัวชี้วัด §2.3 |
|---|---|---|
| Time-to-hire | Speed | ✓ |
| DOA compliance rate | Compliance | ✓ |
| Consent coverage | Compliance | ✓ |
| Funnel conversion | Conversion | ✓ |
| จำนวนอัตราเปิด/ปิด | Volume | (report) |

### 17.4 Threshold
| ตัว | Min | Max | Action เมื่อเกิน |
|---|---|---|---|
| Time-to-hire | — | (config) | alert HR เมื่ออัตราค้างนานเกิน |
| Consent coverage | 100% | — | บล็อกการเลื่อน (hard gate) |

### 17.5 Throughput
Capacity: จำนวนผู้สมัคร/อัตราที่ระบบรองรับ — baseline เก็บหลัง launch

---

## Section 18 · Monitoring

### 18.1 Reports Overview
- **Performance:** funnel conversion + time-to-hire (report tab)
- **Closing:** อัตราที่ปิด (filled/cancelled) รายเดือน
- **Anomaly:** ผู้สมัครค้าง pipeline นานผิดปกติ · consent ขาด · retention ใกล้ครบ
- **Transaction:** audit log ทุก create/แก้/เลื่อน/อนุมัติ

### 18.2 Dashboard Widgets
- Funnel chart (สมัคร→สัมภาษณ์→ข้อเสนอ→รับ) · Time-to-hire trend · DOA compliance gauge · Consent coverage · อัตราเปิด/ปิด

### 18.3–18.6
Performance/Closing/Anomaly/Transaction report ผูก KPI/Threshold §17 — retention-due report (OQ-16) เพิ่มเมื่อกำหนดระยะ

---

## AI Review Report

```
═══════════════════════════════════════
AI REVIEW REPORT — BRD Generator Full
═══════════════════════════════════════
BRD: BRD-F127-RECRUIT — สรรหา (Recruit)
ประเภท: New Feature · HR · Wave W9
วันที่ตรวจ: 2026-09-03

CHECKLIST (New Feature C01-C23 + PE01-05):
✅ C01 Business Objective วัดผลได้ (§2.3 มี baseline/target/วิธีวัด)
✅ C02 User Roles ครบ (3 persona + permission matrix)
✅ C05 Story ไม่มีคำว่า "และ" (แยกครบ US-01..12)
✅ C10 ทุก rule ที่มีตัวเลข/เงื่อนไข ติด Tag
✅ C13 Edge Cases ครบหมวด (10.1 + 10.2 PM/DI/ST/EM/CA)
✅ C18 WARNING มีแผน (OQ-15/16 ระบุผู้เคาะ)
✅ C19 §14 ใบสั่งครบ
✅ C20 Scope Lock §3.4 ครบ (LOCK-OB1..5 + DOA/DOCCFG) · ไม่มี SCOPE DRIFT
✅ C21 Value Stream §12.1 upstream + downstream map ตอบ "แล้วไงต่อ" ทุกแถว
✅ C22 ตัวชี้วัด §2.3 มีคู่ §17.3
✅ C23 §9.5 marker 🤖/✅ ครบ · VR-04 DYNAMIC + BR-02 retention อยู่ใน OQ
✅ PE01 COSO ครบทุก step §5
✅ PE02 SoD ผ่าน (recruiter maker ≠ manager approver)
✅ PE03 Security Preset P6 + controls PDPA
✅ PE04 SLA/KPI/Threshold §17 ครบ
✅ PE05 Cross-section coverage (BC↔Edge, Control↔Health, Metric↔Monitor)

Screen Inventory: 4 มุมมองหลัก (route จริง recruit/req·pool·board·report)
  + drawer 4 แท็บ (detail/assess/offer/history) + ~6 modal = ตรงกับ HTML (ไม่มี HTML-RIF drift)

OPEN QUESTIONS ค้าง: OQ-15 (handoff · Strike) · OQ-16 (PDPA retention · Strike/พี่เบิร์ด) · OQ-17 (req ปิดขณะ pipeline ค้าง)

SUMMARY: ผ่าน 20/20 (checklist) · 3 OQ ค้าง (ไม่บล็อกการเขียน FRD ส่วนที่ไม่พึ่ง handoff/retention)

สถานะ: ✅ APPROVED (with Open Questions)
พร้อมส่งเข้า frd-generator-v6 — FRD ต้องกัน scope ที่พึ่ง OQ-15/16 ไว้จนกว่าเคาะ
═══════════════════════════════════════
```
