# 06_TESTS — F-HR-RECRUIT (F127) สรรหา / Recruit

> **Audience:** QA engineer
> **Purpose:** Acceptance Criteria + DoD + Cross-Module + Microcopy-aware expected
> **Coverage source:** 02_API + 03_LOGIC + 05_RULES + FUNCTION_CHECKLIST (21 FN)
> **⭐ Microcopy:** expected text = **ข้อความจริงจาก สรรหา.html (verbatim)** (R14) — fallback microcopy กลาง html-generator-v9

---

## §6.1 Acceptance Criteria (AC) — ครอบ 21 FN

### AT-01 (FN-01): เปิดอัตรา — happy
**Given** recruiter, grade G4, hiring manager active
**When** POST /recruit/requisitions (position/count/grade/HM)
**Then** 201, status='draft', band_snapshot มี version_id='SS-2569-03'
**And** audit entry created

### AT-02 (FN-02/BR-08/EC-03): เปิดอัตราไม่มี Manpower
**Given** manpower_ref=null
**When** submit req form
**Then** บันทึกได้ · note is-warn "ยังไม่ได้ระบุแผนอัตรากำลัง … เปิดอัตราได้" · chip "ไม่มีแผน" (amber) · audit kind='warn' — **ไม่บล็อก**

### AT-03 (FN-08/BR-01): ส่งอนุมัติเปิด (DOA slot picker)
**Given** req draft
**When** "ส่งอนุมัติเปิด" → DOA modal
**Then** slot ว่างให้เลือกคน (ไม่ hardcode) · เลือกไม่ครบ → toast "กรุณาเลือกผู้อนุมัติให้ครบทุกขั้น" · ครบ → toast "ส่งอนุมัติแล้ว" · status=pending
**And** approve ครบทุก slot → toast "อนุมัติแล้ว" · status=approved

### AT-04 (FN-16/FN-91): ปิดอัตรา
**Given** req open
**When** "ปิดอัตรา" → confirm (title "ปิดอัตรานี้?")
**Then** toast "ปิดอัตราแล้ว" · status=closed (soft archive) · auto-close เมื่อ filled≥count

### AT-05 (FN-03): เพิ่มผู้สมัคร — happy
**When** POST /recruit/candidates (name/contact/resume/ตำแหน่ง + consent)
**Then** toast "สร้างผู้สมัครสำเร็จ" · stage='applied' · 201

### AT-06 (FN-04): ผูกผู้สมัครกับอัตรา
**When** เลือก "ตำแหน่งที่สมัคร" (cand_req combobox) → req
**Then** candidate.req_id set · reqViewDrawer แสดง "ผู้สมัครในอัตรานี้"

### AT-07 (FN-05/BR-02): consent PDPA — บันทึกได้แต่ gate
**Given** consent=false
**When** submit candidate
**Then** บันทึกเข้าคลังได้ · note "ยังไม่ได้รับความยินยอม — บันทึกเข้าคลังได้ แต่จะ ดำเนินการต่อ (คัดกรอง / สัมภาษณ์ / ข้อเสนอ) ไม่ได้ จนกว่าจะได้รับความยินยอม"

### AT-08 (FN-14/BR-10/EC-02): duplicate warn
**Given** email/phone ตรงผู้สมัครเดิม
**When** กรอกในฟอร์ม
**Then** live note is-warn + chip "เคยสมัคร" ทุกจอ — **ไม่บล็อก** (บันทึกได้)

### AT-09 (FN-05): บันทึกความยินยอมภายหลัง
**When** ปุ่ม "บันทึกความยินยอม" (candSetConsent)
**Then** toast "บันทึกความยินยอมแล้ว" · consent_ok=true, date=today · unmask contact

### AT-10 (FN-06/BR-03): เลื่อนสถานะบอร์ด
**Given** consent_ok=true
**When** "ถัดไป" บน kanban card
**Then** stage เลื่อน 1 ขั้น · audit append

### AT-11 (FN-05/EC-01): no-consent block เลื่อน
**Given** consent_ok=false
**When** "ถัดไป" (dir>0)
**Then** บล็อก · toast "ยังไม่ได้รับความยินยอม PDPA — เลื่อนสถานะไม่ได้" · 422 BR_CONSENT_REQUIRED

### AT-12 (FN-07): นัดสัมภาษณ์ + NTF
**When** "นัดสัมภาษณ์" → modal (วันที่/เวลา/ผู้สัมภาษณ์/สถานที่) → save
**Then** toast "นัดสัมภาษณ์แล้ว" · ntf ผู้สัมภาษณ์+ผู้สมัคร · interviewer snapshot เก็บ

### AT-13 (FN-09): scorecard
**Given** ไม่ให้คะแนน
**When** save → toast "กรุณาให้คะแนนก่อน"
**When** ให้คะแนน 1-5 + comment → toast "บันทึกผลประเมินแล้ว" · score ต่อผู้สัมภาษณ์

### AT-14 (FN-10/BR-04/BR-09/VR-03/EC-04/EC-11): สร้างข้อเสนอ + band freeze
**When** สร้าง offer (grade/start/salary)
**Then** band resolve + freeze version_id='SS-2569-03' · salary นอก band → toast "เงินนอกช่วง band — กรุณาระบุเหตุผล" + require reason
**And** band แก้ภายหลัง → offer ยึด snapshot (ไม่ re-resolve)

### AT-15 (FN-08/BR-04): offer DOA + ส่ง
**When** submitOffer → DOA approve ครบ → send
**Then** toast "ส่งข้อเสนอแล้ว" · status sent · ntf offer_sent

### AT-16 (FN-11/BR-05/EC-05): ตอบรับ → hired → handoff
**Given** offer.status ≠ accepted
**When** พยายาม hire → toast "ต้องให้ผู้สมัครตอบรับข้อเสนอก่อน" (บล็อก)
**Given** offer.status=accepted
**When** M-06 confirm (title "รับเข้าทำงาน + ส่งเข้า On/Offboard?")
**Then** toast "ส่งเข้า onboarding แล้ว" · stage=hired · onboard_sent=true · filled++ · **emit event · ไม่สร้าง employee** (ดู XT-01)

### AT-17 (FN-12/FN-91): ปฏิเสธ/ถอนตัว
**When** "ไม่ผ่าน/ถอนตัว" → reason modal (เหตุผลว่าง) → toast "กรุณาระบุเหตุผล"
**When** เลือกผล + เหตุผล → บันทึก · stage=rejected/withdrawn · soft archive

### AT-18 (FN-13): ไม่ผ่าน → talent pool
**When** reason modal เลือก "ไม่ผ่าน → เก็บ Talent Pool" (default)
**Then** stage=talent_pool + reason · TERMINAL pill

### AT-19 (FN-15): รายงาน funnel
**When** เปิด #/recruit/report
**Then** funnel bars (สมัคร→สัมภาษณ์→ข้อเสนอ→รับ) · stat "Time-to-hire เฉลี่ย" · filter "กรองตามอัตรา" ทำงานจริง · Export CSV → toast "ส่งออกรายงาน (CSV) — ต่อ dev" (stub)

### AT-20 (FN-90): ค้นหา/filter + empty state
**When** search/filter จน 0 แถว
**Then** empty state "ยังไม่มีอัตรา"/"ยังไม่มีผู้สมัคร" + "ล้างตัวกรอง"

### AT-21 (FN-92/VR-01/VR-02/EC-09): validate + double-submit
**When** submit ข้อมูลไม่ครบ → toast "กรุณากรอกข้อมูลที่ไฮไลต์ให้ครบ" + field `.is-invalid` + focus ตัวแรก
**When** กด submit ซ้ำเร็ว → ปุ่ม disabled + loader-2 spin (RC.busy) · Idempotency-Key กัน duplicate

### AT-22 (FN-93/BR-03): audit append-only
**When** create/แก้/เลื่อน/อนุมัติ/hire/close
**Then** history section "ประวัติ (append-only)" มี entry ทุก action · ไม่ลบ/แก้ย้อน

### AT-23 (FN-94/BR-06): masking RESTRICTED
**Given** persona=viewer หรือ manager
**Then** contact = masked (maskEmail/maskPhone) · chip "RESTRICTED · ปิดบังตามบทบาท"
**Given** persona=recruiter → unmask · **Given** !consent → "ต้องได้รับความยินยอมก่อน"

### AT-24 (VR-05/EC-06): viewer read-only
**Given** persona=viewer
**Then** ปุ่มสร้างซ่อน · เรียก mutation ทางอ้อม → toast "สิทธิ์อ่านอย่างเดียว" (guard 15 จุด)

### AT-25 (EC-08/OQ-17) `[AI-DEFAULT]`: cancel req ขณะ pipeline ค้าง
**When** cancel req ที่มี active candidate → require reason + warn "มีผู้สมัครค้างใน pipeline"
**Then** candidate ไม่ถูกยกเลิกอัตโนมัติ

### AT-26 (EC-07/OQ-D1) `[AI-DEFAULT]`: concurrent stage move
**Given** 2 recruiter move คนเดียวกันพร้อมกัน
**Then** first 200 · second 409 ERR_STALE_DATA · audit ทั้งคู่

---

## §6.2 Test Case Inventory (สรุป)

| TC | Name | Type | Maps | Priority |
|---|---|---|---|---|
| AT-01..04 | Requisition lifecycle | API+E2E | FN-01/02/08/16 | P0 |
| AT-05..09 | Candidate + consent + dup | API+E2E | FN-03/04/05/14 | P0 |
| AT-10..11 | Pipeline move + gate | E2E | FN-06 | P0 |
| AT-12..13 | Interview + scorecard | API | FN-07/09 | P1 |
| AT-14..16 | Offer + hire handoff | API+E2E | FN-08/10/11 | P0 |
| AT-17..18 | Terminate + talent pool | E2E | FN-12/13 | P1 |
| AT-19..20 | Report + search | E2E | FN-15/90 | P1 |
| AT-21..24 | Validate/audit/mask/viewer | E2E | FN-92/93/94 | P0 |
| AT-25..26 | Edge (AI-DEFAULT) | API stress | EC-07/08 | P2 |
| XT-01..03 | Cross-module | Integration | §6.9 | P1 |

---

## §6.3 Test Data Setup
- 2 tenants (isolated) · 3 req (open/approved/closed) · 6 ผู้สมัคร (ต่าง stage · 1 no-consent · 1 duplicate · 1 hired) · 2 offer · พ.ศ. dates
- Roles: qa_recruiter · qa_manager (slot approver) · qa_viewer
- Bands mock: G3(28-52k)/G4(45-85k)/G5(75-150k) version_id SS-2569-03
- Employees active (ผู้สัมภาษณ์/HM)

---

## §6.4 Definition of Done (DoD)
### Code
- [ ] ทุก AT-01..26 implemented + unit tests
- [ ] Integration (API+DB+Engine+external mock) pass
- [ ] E2E happy + critical edges (consent gate · hire route · masking · viewer) pass
- [ ] No critical/high security findings (PII/PDPA)
- [ ] coverage ≥ 80% logic layer
### Documentation
- [ ] API docs published · FRD §07 reflects final
- [ ] ENG-RCT-01/02 registered CUBIC (if register decision)
### QA
- [ ] P0+P1 pass · no P0/P1 bug open · **FN 21/21 มีเคส**
### Deployment
- [ ] Migration tested staging · **retention/handoff jobs = feature flag OFF** จนกว่า OQ-15/16 เคาะ

---

## §6.5 WebSocket / Realtime Events
- `interview_scheduled` → channel `tenant:<t>:interviewer` + candidate — approver/interviewer dashboard update
- `offer_sent` / `selection_result` / `candidate_accepted` → recruiter/candidate channel
- **doa_pending/doa_result** = DOA engine (ไม่ทดสอบซ้ำที่นี่)
- **handoff `recruit.candidate.hired`** = fire-and-forget → test emit เท่านั้น (ไม่ทดสอบฝั่งรับ · OQ-15)

---

## §6.6 Performance Benchmarks
| Endpoint | P95 | Throughput |
|---|---|---|
| GET requisitions/candidates (list) | < 500ms | 200 req/s |
| POST candidate (+dup check) | < 800ms | 50 req/s |
| GET report/funnel | < 1s | 50 req/s |
| POST hire (handoff) | < 1s | 50 req/s |

---

## §6.7 Test Environment
- staging tenant · mock Salary Structure API (deterministic band) · mock Policy Center DOA (slot resolve) · mock ENG-NOTIFY · Manpower = null hook

---

## §6.8 Trace: AC → Logic Coverage

| AC | API tested | Functions | Engines |
|---|---|---|---|
| AT-01 | API-02 | FN-01, FN-25 | — |
| AT-03 | API-05/06 | FN-03/04, FN-26 | — |
| AT-05/08 | API-10 | FN-08, FN-09 | ENG-RCT-02 |
| AT-11 | API-14 | FN-12, FN-24 | — |
| AT-12 | API-15 | FN-13 | — |
| AT-13 | API-16 | FN-14 | — |
| AT-14 | API-17 | FN-15, FN-25 | — |
| AT-16 | API-22 | FN-19, FN-07 | — |
| AT-19 | API-24 | FN-22 | ENG-RCT-01 |
| AT-23 | API-09/11 | FN-23 | — |
| AT-26 | API-14 | FN-12 (concurrent) | — |

> **Coverage:** ทุก Function (FN-01..26) + Engine (RCT-01/02) ถูก trace ≥1 AC. **FN 21/21 ครอบ** (FN-01..16 + FN-90..94).

---

## §6.9 Cross-Module Test Cases ⭐ (จาก BRD §12.1 Downstream)

| ID | Scenario | Downstream | Expected |
|---|---|---|---|
| **XT-01** | hire candidate (offer accepted) | On/Offboard | emit `recruit.candidate.hired` payload {candidate_id, position, grade_code, start_date, offer_snapshot, hired_at} · **ไม่มี employee_id · ไม่สร้าง employee** · fire-and-forget (ไม่รอ ack) · **ฝั่งรับไม่ทดสอบ (OQ-15)** |
| **XT-02** | สร้าง offer → band แก้ที่ Salary Structure ก่อน accept | Salary Structure | offer เดิมยึด freeze `band_version_id` (ไม่เปลี่ยน) |
| **XT-03** | นัดสัมภาษณ์/ส่ง offer/ผลคัดเลือก | ENG-NOTIFY | ntf event ยิงตรง trigger · ล้มเหลว → queue/retry (ไม่บล็อก · OQ-D4) |
| **XT-04** | submit-approval req/offer | Policy Center DOA | resolve slot chain runtime · **ไม่ hardcode** · Policy Center down → BR_DOA_UNRESOLVED (ไม่ประกาศ) |

---

## §6.10 Microcopy-Aware Expected Text (verbatim จาก สรรหา.html)

| Action | Expected (verbatim) |
|---|---|
| สร้างผู้สมัครสำเร็จ | "สร้างผู้สมัครสำเร็จ" |
| consent gate เลื่อน | "ยังไม่ได้รับความยินยอม PDPA — เลื่อนสถานะไม่ได้" |
| บันทึก consent | "บันทึกความยินยอมแล้ว" |
| offer นอก band | "เงินนอกช่วง band — กรุณาระบุเหตุผล" |
| board→offer ไม่มี offer | "ไปขั้น "ข้อเสนอ" ให้สร้างข้อเสนอในลิ้นชักผู้สมัคร" |
| hire ก่อน accepted | "ต้องให้ผู้สมัครตอบรับข้อเสนอก่อน" |
| hired สำเร็จ | "ส่งเข้า onboarding แล้ว" |
| confirm hire (title) | "รับเข้าทำงาน + ส่งเข้า On/Offboard?" |
| DOA เลือกไม่ครบ | "กรุณาเลือกผู้อนุมัติให้ครบทุกขั้น" |
| ส่งอนุมัติ | "ส่งอนุมัติแล้ว" |
| ประกาศรับ | "ประกาศรับแล้ว" |
| ปิดอัตรา | "ปิดอัตราแล้ว" |
| validate ไม่ครบ | "กรุณากรอกข้อมูลที่ไฮไลต์ให้ครบ" |
| scorecard ไม่ให้คะแนน | "กรุณาให้คะแนนก่อน" |
| offer ขาด field | "กรุณากรอกวันเริ่มงานและเงินเดือน" |
| terminate ไม่มีเหตุผล | "กรุณาระบุเหตุผล" |
| viewer mutation | "สิทธิ์อ่านอย่างเดียว" |
| นัดสัมภาษณ์ | "นัดสัมภาษณ์แล้ว" |
| ส่งข้อเสนอ | "ส่งข้อเสนอแล้ว" |
| Export CSV (stub) | "ส่งออกรายงาน (CSV) — ต่อ dev" |
| masked contact (no consent) | "ต้องได้รับความยินยอมก่อน" |

> ผลลัพธ์: ai-testcase-md-generator + qa-friendly-html-generator (step 9/11) จะ match จอจริง 1:1.
