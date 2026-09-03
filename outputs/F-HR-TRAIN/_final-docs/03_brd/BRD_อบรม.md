# BRD — Training / อบรม (F-HR-TRAIN · F133)

> เอกสาร Business Requirement ฉบับสมบูรณ์ · WF-01 · SOW3.2 (Actor: BA)
> Mode: **Fresh (HTML-first)** — สกัด Screen Inventory + behaviour จาก HTML ที่ผ่าน re-gate แล้ว (`outputs/F-HR-TRAIN/อบรม.html`)
> Conflict Priority ที่ใช้: **LOCK > PREBRIEF (business intent) > HTML (หน้าจอจริง)**

---

## Section 1 · Document Info

| หัวข้อ | ค่า |
|---|---|
| BRD ID | BRD-F-HR-TRAIN |
| Feature | Training / อบรม (การฝึกอบรมและพัฒนาบุคลากร) |
| Feature Code | F133 · F-HR-TRAIN |
| Archetype | **master** (แคตตาล็อกหลักสูตร + การลงทะเบียน — ไม่ใช่ Q-document) |
| ประเภท BRD | **New Feature** |
| Wave | W8 |
| Version | 1.0 |
| Status | **APPROVED** (ผ่าน Quality Gate ในตัว — ดู §14.7 · ทุก issue เปิดเป็น Open Question ไม่บล็อกเอกสาร) |
| Owner | BA — ทีม Human Capital (2BSimple) |
| Stakeholders | HR L&D (เจ้าหน้าที่ฝึกอบรม) · หัวหน้าสายงาน/ผู้จัดการฝ่ายพัฒนาบุคลากร (ผู้อนุมัติ) · พนักงาน (ผู้เรียน) · Finance (มุมต้นทุน EC) · SEC/PM |
| วันที่ | 2026-09-03 |
| Source of truth | HTML `อบรม.html` (3032 บรรทัด · audit FAIL=0 · qc-ux BLOCK=0 · coverage FN 18/18) + PREBRIEF + FUNCTION_CHECKLIST (18 FN) + STANDARD_BASELINE (MUST 9) + HANDOFF |

### 1.1 Changelog
- v1.0 (2026-09-03): Initial BRD via brd-generator-full (Fresh Mode, HTML-first) — สะท้อน scope หลัง BA review + 7 FIX (FIX-01..07)

---

## Section 2 · Business Context

### 2.1 ปัญหา / โอกาส
องค์กรจำเป็นต้องพัฒนาบุคลากรอย่างเป็นระบบ แต่ปัจจุบันการจัดอบรมกระจัดกระจาย — ไม่มีแคตตาล็อกหลักสูตรกลาง, ไม่มีทะเบียนรอบอบรม/การลงทะเบียนที่ตรวจสอบได้, ไม่มีการเชื่อม gap จากการประเมินผลงานเข้ากับหลักสูตร, และการอนุมัติค่าใช้จ่ายอบรมทำนอกระบบ ทำให้ควบคุมงบและตรวจสอบย้อนหลังยาก อีกทั้งประวัติอบรมรายคน/ชั่วโมงสะสมไม่ถูกบันทึกไว้ในที่เดียว

### 2.2 เป้าหมาย Business
1. มีแคตตาล็อกหลักสูตรกลาง (course catalog) พร้อมสถานะวงจรชีวิต ร่าง→เผยแพร่→ปิด
2. จัดรอบอบรม (session) และลงทะเบียน/มอบหมายผู้เรียน (จาก gap ประเมินผลงาน หรือเลือกเอง) โดยคุมจำนวนรับ
3. บังคับสายอนุมัติ (DOA) เฉพาะหลักสูตรที่**มีค่าใช้จ่าย** เพื่อคุมงบ — หลักสูตรฟรีลงทะเบียนได้ทันที
4. บันทึกผลอบรม (ผ่าน/ไม่ผ่าน) + ประเมินหลังอบรม พร้อมออกใบรับรอง (soft ref) และเก็บประวัติ/ชั่วโมงสะสมรายคน
5. เชื่อมค่าอบรมเข้า Expense Claim (hook · ไม่จ่าย/ไม่ post เอง) และวัด completion rate + ต้นทุนต่อหัว

### 2.3 ตัวชี้วัดความสำเร็จ (บังคับวัดได้)

| ตัวชี้วัด | Baseline ปัจจุบัน | Target | วัดยังไง / จากไหน | วัดเมื่อไหร่ |
|---|---|---|---|---|
| อัตราการอบรมสำเร็จ (completion rate = ผ่าน ÷ บันทึกผลจากรอบที่ปิดแล้ว) | ไม่มีระบบวัด — **ต้องเก็บ baseline ก่อน launch** | ≥ 80% | รายงานการอบรม §Report (FN-13) นับเฉพาะผลจากรอบ `closed` (FIX-01) | รายเดือน / รายไตรมาส |
| สัดส่วนการลงทะเบียนที่มาจาก gap ประเมินผลงาน | 0% (ไม่มี hook เดิม) | ≥ 40% ของการลงทะเบียนใหม่ | field `source=gap` + `gap_ref` บน Enrollment (FN-10) | รายไตรมาส |
| เวลาเฉลี่ยจากลงทะเบียน (มีค่าใช้จ่าย) → อนุมัติครบ (DOA) | ไม่มีข้อมูล — เก็บ baseline หลัง launch | ≤ 3 วันทำการ | timestamp audit trail ขั้นอนุมัติ DOA (FN-04/08) | รายเดือน |
| ต้นทุนต่อหัวของหลักสูตรมีค่าใช้จ่าย (งบ ÷ ผู้ผ่าน) | ไม่เคยคำนวณรวมศูนย์ | ติดตามแนวโน้ม (ไม่มี hard target รอบนี้ · display-only จน Rate Card พร้อม) | §Report การ์ดต้นทุนต่อหัว (FIX-05) | รายไตรมาส |

> คู่กับ §17.3 KPI ทุกตัว (ดู C22)

### 2.4 ที่มา
- LOCK มติ 17 ส.ค.: DOA เมื่อ has_cost · ค่าอบรม = hook Expense · gap = hook Performance · CSQ = EC (ไม่มี AC) · audit append-only · config หมวดอ่าน HR Config
- Baseline 3 ค่าย (Odoo eLearning/Surveys · D365 Learning · SAP SF Learning) — MUST 9 capability
- BA review รอบ 2 (2026-09-03) → 7 FIX (FIX-01..07)

---

## Section 3 · Scope

### 3.1 In Scope
1. แคตตาล็อกหลักสูตร: สร้าง/แก้ไข/เผยแพร่/ปิด · ระบุ has_cost + งบ · หมวดอ่านจาก HR Configuration (FN-01)
2. รอบอบรม (session): สร้าง/แก้ไข · วันเวลา/สถานที่/จำนวนรับ · เปิดรับสมัคร/ปิดรอบ (FN-02)
3. ลงทะเบียน/มอบหมายผู้เรียน: จาก gap (Performance hook) หรือเลือกเอง · บล็อกเมื่อเกินจำนวนรับ (FN-03)
4. DOA gate เมื่อหลักสูตรมีค่าใช้จ่าย → ขออนุมัติก่อนยืนยัน · ผ่าน DOA slot picker เลือกคนตามตำแหน่ง (ไม่ hardcode สาย) (FN-04, FN-08)
5. หลักสูตรฟรี → ลงทะเบียนยืนยันได้ทันที ข้าม DOA (FN-05)
6. เช็คชื่อเข้า/ขาดอบรม (attendance · FIX-03) → บันทึกผล (ผ่าน/ไม่ผ่าน) ได้เฉพาะรอบที่ปิดแล้ว (FIX-01) + ประเมินหลังอบรมคะแนน 1-5 + comment (FIX-03) (FN-06)
7. ออกใบรับรองผู้ผ่าน = soft ref (ไม่มีเลขรัน/ไม่ออก PDF ทางการ) (FN-07)
8. ค่าอบรม → ส่ง Expense Claim (hook display-only · ไม่จ่าย/ไม่ post) + ยิงมูลค่า **EC** (CSQ · ไม่มี AC) · ส่งได้หลัง confirmed + กันส่งซ้ำ (FIX-02) (FN-09)
9. gap จากประเมินผลงาน → แนะนำผู้เรียน (hook display-only · ไม่สร้าง gap เอง) (FN-10)
10. ยกเลิกการลงทะเบียน (soft archive คืนที่ว่าง) (FN-11)
11. ประวัติอบรมรายคน + ชั่วโมงสะสม (เฉพาะรายการที่ผ่าน) (FIX-04)
12. แจ้งเตือน 3 event: เปิดรับสมัคร / ยืนยันลงทะเบียน / ประกาศผล (FN-12)
13. รายงานการอบรม: completion rate + ต้นทุนต่อหัว + filter ตามหลักสูตร (FN-13, FIX-05)
14. กติกากลาง: ค้นหา/filter + empty state (FN-90) · ปิด/ยกเลิกผ่าน confirm + soft archive (FN-91) · validate + กัน double-submit (FN-92) · audit append-only ทุก create/แก้/อนุมัติ/บันทึกผล (FN-93) · masking ตาม role (FN-94)

### 3.2 Out of Scope (ดู §14.6 · unsupported 5 — ตัดโดยมติ)
1. **จ่ายเงินค่าอบรมจริง / ลงบัญชี** — ส่ง hook Expense Claim เท่านั้น (OB-1)
2. **ประเมินผลงาน / สร้าง gap เอง** — อ่านจาก Performance (hook) เท่านั้น (OB-2)
3. **eLearning content / SCORM · competency/skill mapping** — NICE ไม่รองรับรอบนี้ (OQ)
4. **ใบรับรองเลขรัน / PDF ทางการ** — รอบนี้เป็น soft ref (ไม่มี doccfg / pdfdoc)
5. **สร้าง/แก้ config หมวดหลักสูตรกลาง** — อ่านจาก HR Configuration (#107) เท่านั้น

### 3.3 Assumptions
- Employee (F011), Performance (F131), Expense Claim (F101), HR Config (F164) พร้อมใช้งาน (done)
- Rate Card (F060) **ยังไม่ dev** → มูลค่า EC/ต้นทุนต่อหัว = display-only อ้างอิง จนกว่าพร้อม (ไม่ hardcode)
- สายอนุมัติจริงมาจาก DOA กลาง (F-DLG-001 · Policy Center) — feature ประกาศเท่านั้น
- วันที่แสดงเป็น พ.ศ.

### 3.4 Scope Lock ⭐

**scope_lock_ref:** LANE_BRIEF + STANDARD_BASELINE (MUST 9) + HANDOFF §3 (LOCK 17 ส.ค.)

| LOCK-ID | มติที่ล็อก | ผลต่อ scope |
|---|---|---|
| LOCK-01 | อนุมัติ (DOA) เมื่อหลักสูตร **has_cost** เท่านั้น (ฟรี = ข้าม) | บังคับใน FN-04/05/08 · BR-04 |
| LOCK-02 | ค่าอบรม = **hook Expense Claim** (ไม่จ่าย/ไม่ post เอง) | FN-09 · BR-06 · Out-of-Scope #1 |
| LOCK-03 | gap = **hook Performance** (อ่านอย่างเดียว · ไม่สร้าง gap เอง) | FN-10 · BR-07 · Out-of-Scope #2 |
| LOCK-04 | CSQ = **EC เท่านั้น** (ไม่มี AC เพราะ Expense เป็นตัวลงบัญชี) | FN-09 · BR-09 · §12 |
| LOCK-05 | audit **append-only** + masking ตาม role | FN-93/94 · BR-08 |
| LOCK-06 | config หมวดหลักสูตร **อ่านจาก HR Config** (#107) | Out-of-Scope #5 |
| LOCK-07 | ใบรับรอง = **soft ref** (ไม่มีเลขรัน/PDF) | FN-07 · Out-of-Scope #4 |

**SCOPE DRIFT:** — (ไม่พบ In-Scope ที่เกินใบเซ็น) · HTML สอดคล้อง LOCK ทุกข้อ (LOCK-01 บังคับผ่าน `has_cost` gate ทั้ง create/enroll/approval; LOCK-04 EC ไม่มี AC ทุกจุด)

---

## Section 4 · User Roles & Permissions

> HTML มี persona demo 3 ตัว (hr / manager / viewer) เป็น scaffolding ทดสอบสิทธิ์ — RBAC จริงตั้งที่ระบบสิทธิ์กลาง

| Role | ดู | สร้าง/แก้ (หลักสูตร·รอบ) | ลงทะเบียน/ยกเลิก | อนุมัติ DOA | บันทึกผล/ใบรับรอง | ส่ง Expense (EC) | เห็นตัวเงิน (unmask) |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| HR L&D (เจ้าหน้าที่ฝึกอบรม) | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| หัวหน้า/ผู้จัดการ (ผู้อนุมัติ) | ✅ | ✅¹ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Viewer (อ่านอย่างเดียว) | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ (mask ••••••) |

¹ **OQ-05 (RBAC):** prototype ให้ non-viewer (รวมหัวหน้า) สร้าง/แก้ได้ ตาม recruit precedent — SEC/BA ต้องเคาะว่าหัวหน้าควร "สร้างได้" หรือ "อนุมัติอย่างเดียว"
- DOA gate: อนุมัติได้เฉพาะ role ที่ `canApprove` (FN guard FIX-02) — คนอื่นเห็นแต่ปุ่ม "ยกเลิก"
- Masking: ตัวเงิน (งบ/ต้นทุนต่อหัว) mask สำหรับ viewer (FN-94 · RESTRICTED บางส่วน)

---

## Section 5 · User Journey (with COSO)

### 5.1 Happy Path — หลักสูตรมีค่าใช้จ่าย (เข้าสาย DOA)

| # | Step | Route/Overlay จริง | Maker | Checker | Approver | System |
|:--:|---|---|---|---|---|---|
| 1 | สร้างหลักสูตร (has_cost + งบ) → เผยแพร่ | `#/train/course` → drawer form | HR L&D | — | — | validate + audit + สถานะ published |
| 2 | สร้างรอบอบรม (วันเวลา/สถานที่/จำนวนรับ) | `#/train/plan` → drawer form | HR L&D | — | — | guard: หลักสูตร published เท่านั้น (FIX-02) |
| 3 | เปิดรับสมัคร (รอบ → open) | session view drawer | HR L&D | — | — | สถานะ open + **NTF: เปิดรับ** |
| 4 | ลงทะเบียนผู้เรียน (จาก gap หรือเลือกเอง) | modal enroll (gap picker) | HR L&D | — | — | guard: ≤ จำนวนรับ · สร้าง Enrollment `pending_doa` |
| 5 | ส่งอนุมัติ (DOA) — เลือกคนตามตำแหน่งแต่ละขั้น | modal DOA slot picker | HR L&D | — | — | ผูก DOA entry · **NTF: ส่งอนุมัติ** |
| 6 | อนุมัติแต่ละขั้น (2 ขั้น) | session view › อนุมัติ/ผู้เรียน | — | หัวหน้าสายงาน | ผจก.พัฒนาบุคลากร | ครบ → `confirmed` · **NTF: ยืนยัน** · ยิงมูลค่า EC (CSQ) |
| 7 | ส่งค่าอบรม → Expense Claim (มูลค่า EC) | session view › ค่าใช้จ่าย | HR L&D | — | — | hook display-only · กันส่งซ้ำ (FIX-02) |
| 8 | ปิดรอบ (จบการอบรม) | session view drawer | HR L&D | — | — | สถานะ closed |
| 9 | เช็คชื่อเข้า/ขาด (attendance) | session view › ผู้เรียน | HR L&D | — | — | append audit (FIX-03) |
| 10 | บันทึกผล (ผ่าน/ไม่ผ่าน) + ประเมิน 1-5 | modal result | HR L&D | — | — | guard: closed + attended (FIX-01/03) · **NTF: ผล** |
| 11 | ออกใบรับรองผู้ผ่าน (soft ref) | ปุ่มในแถวผู้เรียน/ผล | HR L&D | — | — | cert soft ref · audit |

**SoD:** Maker (HR L&D · ลงทะเบียน/ส่งอนุมัติ) ≠ Approver (หัวหน้า/ผจก. · อนุมัติ DOA) — ผ่าน ✅

### 5.2 Alternative Paths
- **A1 หลักสูตรฟรี (LOCK-01):** step 5–7 ข้าม → ลงทะเบียนแล้ว `confirmed` ทันที + NTF ยืนยัน (ไม่มี Expense)
- **A2 ไม่อนุมัติ (reject):** ผู้อนุมัติระบุเหตุผล → Enrollment `cancelled` (append audit)
- **A3 ยกเลิกการลงทะเบียน (FN-11):** confirm → `cancelled` (soft archive) คืนที่ว่าง
- **A4 เกินจำนวนรับ:** ปุ่มลงทะเบียนถูก disable + note เตือน (BR-02)
- **A5 ดูประวัติอบรมรายคน (FIX-04):** คลิกชื่อผู้เรียน → modal ประวัติ + ชั่วโมงสะสม

> ทุก step map กับ route/overlay จริงบนจอ — ไม่มี step ลอยที่ไม่มีที่ยืน

---

## Section 6 · Data Entity & Fields
(รายละเอียด field ดู Step 4 — §6.1–§6.4)

### 6.1 Entities
- **Course** (หลักสูตร · header master)
- **Session** (รอบอบรม · 1 Course : N Session)
- **Enrollment** (การลงทะเบียน · 1 Session : N Enrollment · snapshot ผู้เรียน)
- **Approval** (สาย DOA · embedded ใน Enrollment เมื่อ has_cost)
- Reference (อ่านอย่างเดียว): Employee (F011) · Performance gap (F131) · HR Config category (F164) · Expense/EC (F101) · Rate Card (F060 · ยังไม่ dev)

### 6.2 Course — fields

| # | Field | Label UI | Type | ค่า/ตัวเลือก | จำเป็น | หมายเหตุ |
|:--:|---|---|---|---|:--:|---|
| 1 | code | รหัสหลักสูตร | AUTO | CRS-2569-NNN | auto | running ในโค้ด (ไม่ใช่ doccfg) |
| 2 | name | ชื่อหลักสูตร | TEXT | — | ✅ | |
| 3 | category | หมวดหลักสูตร | LOOKUP | จาก HR Config (safety/leadership/technical/comm/orientation) | ✅ | อ่านอย่างเดียว (#107) |
| 4 | instructor | ผู้สอน/วิทยากร | TEXT | ภายใน/ภายนอก | ✅ | |
| 5 | duration | ระยะเวลา | TEXT | เช่น "2 วัน (12 ชม.)" | ✅ | parse ชม. → ชั่วโมงสะสม (FIX-04) |
| 6 | has_cost | มีค่าใช้จ่าย? | TOGGLE | true/false | ✅ | **ตัวชี้ทั้ง DOA gate + Expense** (LOCK-01) |
| 7 | budget | งบประมาณหลักสูตร | NUMBER | บาท | ✅ ถ้า has_cost | งบภายใน (คนละส่วน EC) — BR-01 |
| 8 | desc | รายละเอียด | TEXTAREA | — | — | |
| 9 | status | สถานะ | ENUM | draft / published / closed | auto | |
| 10 | history | ประวัติ | AUDIT | append-only | auto | FN-93 |

### 6.3 Session — fields

| # | Field | Label UI | Type | จำเป็น | หมายเหตุ |
|:--:|---|---|---|:--:|---|
| 1 | code | รหัสรอบ | AUTO | auto | SES-2569-NNN |
| 2 | courseId | หลักสูตร | LOOKUP | ✅ | เฉพาะหลักสูตร published (FIX-02) |
| 3 | start / end | วันเริ่ม / วันสิ้นสุด | DATE | ✅ / — | end เว้นได้ (อบรมวันเดียว) |
| 4 | time | ช่วงเวลา | TEXT | — | เช่น 09:00–16:00 |
| 5 | capacity | จำนวนที่รับ | NUMBER | ✅ (≥1) | คุมจำนวนลงทะเบียน (BR-02) |
| 6 | location | สถานที่ | TEXT | ✅ | |
| 7 | status | สถานะ | ENUM | auto | draft / open / closed |
| 8 | history | ประวัติ | AUDIT | auto | FN-93 |

### 6.4 Enrollment — fields

| # | Field | Label UI | Type | หมายเหตุ |
|:--:|---|---|---|---|
| 1 | sessionId | รอบอบรม | LOOKUP | |
| 2 | emp (snapshot) | ผู้เรียน | SNAPSHOT | เก็บ id/name/position/dept ณ เวลาลงทะเบียน (BR-10) |
| 3 | source | ที่มา | ENUM | gap / manual (FN-10) |
| 4 | gap_ref | อ้างอิง gap | TEXT | PERF-NNNN (เมื่อ source=gap) |
| 5 | status | สถานะลงทะเบียน | ENUM | pending_doa / confirmed / passed / failed / cancelled |
| 6 | attended | เช็คชื่อ | ENUM | null / true(เข้า) / false(ขาด) — FIX-03 |
| 7 | result | ผล | ENUM | null / pass / fail (FN-06) |
| 8 | evalScore | คะแนนประเมินหลังอบรม | NUMBER | 1–5 (ไม่บังคับ) — FIX-03 |
| 9 | evalComment | ความเห็นประเมิน | TEXTAREA | FIX-03 |
| 10 | cert | ใบรับรอง | OBJECT | soft ref (id/issuedAt/note · ไม่มีเลขรัน) — FN-07 |
| 11 | expenseSent | ส่ง Expense แล้ว | TOGGLE | กันส่งซ้ำ (FIX-02) — FN-09 |
| 12 | approval | สาย DOA | OBJECT | embedded (entry + steps[order/slotName/approver_id/result/at]) |
| 13 | history | ประวัติ | AUDIT | append-only |

### 6.5 Entity Relationship
```
Course ──(1:N)──▶ Session ──(1:N)──▶ Enrollment ──(embeds)──▶ Approval(DOA)
Employee ──(referenced by · snapshot)──▶ Enrollment.emp
Performance(gap) ──(referenced by · hook)──▶ Enrollment.source/gap_ref
HR Config(category) ──(referenced by)──▶ Course.category
Expense/EC ◀──(hook display-only)── Enrollment (has_cost)
Rate Card ──(referenced by · ยังไม่ dev)──▶ มูลค่า EC / ต้นทุนต่อหัว
```

---

## Section 7 · User Stories & Acceptance Criteria

| ID | Story (As a … I want … so that …) | AC |
|---|---|---|
| US-01 | ในฐานะ HR L&D ฉันต้องการสร้างหลักสูตรพร้อมระบุมีค่าใช้จ่าย/งบ | AC1 กรอกชื่อ/หมวด/ผู้สอน/ระยะเวลาครบจึงเผยแพร่ได้ · AC2 has_cost=true ต้องกรอกงบ · AC3 บันทึกร่างได้ |
| US-02 | ในฐานะ HR L&D ฉันต้องการสร้างรอบอบรมของหลักสูตรที่เผยแพร่ | AC1 เลือกได้เฉพาะหลักสูตร published · AC2 ต้องมีวันเริ่ม/จำนวนรับ/สถานที่ · AC3 รอบใหม่เริ่มที่สถานะร่าง |
| US-03 | ในฐานะ HR L&D ฉันต้องการลงทะเบียนผู้เรียนจาก gap หรือเลือกเอง | AC1 แสดง gap จาก Performance ให้เลือก · AC2 บล็อกเมื่อเกินจำนวนรับ · AC3 กันลงทะเบียนซ้ำคนเดิม |
| US-04 | ในฐานะ HR L&D ฉันต้องการให้หลักสูตรมีค่าใช้จ่ายผ่านอนุมัติก่อนยืนยัน | AC1 has_cost → สถานะ pending_doa · AC2 เลือกผู้อนุมัติครบทุกขั้นจึงส่งได้ · AC3 หลักสูตรฟรีข้าม DOA ยืนยันทันที |
| US-05 | ในฐานะผู้อนุมัติ ฉันต้องการอนุมัติ/ไม่อนุมัติการลงทะเบียน | AC1 เฉพาะ role canApprove · AC2 อนุมัติครบทุกขั้น → confirmed + NTF · AC3 ไม่อนุมัติต้องระบุเหตุผล → cancelled |
| US-06 | ในฐานะ HR L&D ฉันต้องการบันทึกผลอบรมหลังจบรอบ | AC1 บันทึกผลได้เฉพาะรอบ closed (FIX-01) · AC2 ต้องเช็คชื่อเข้าก่อน (FIX-03) · AC3 ให้คะแนน 1-5 + comment ได้ · AC4 บันทึกแล้วประกาศผล + NTF |
| US-07 | ในฐานะ HR L&D ฉันต้องการออกใบรับรองผู้ผ่าน | AC1 เฉพาะผู้ผ่าน · AC2 เป็น soft ref ไม่มีเลขรัน/PDF |
| US-08 | ในฐานะ HR L&D ฉันต้องการส่งค่าอบรมเข้า Expense Claim | AC1 ส่งได้หลัง confirmed · AC2 กันส่งซ้ำ · AC3 เป็น hook display-only ไม่จ่าย/ไม่ post |
| US-09 | ในฐานะผู้ใช้ ฉันต้องการดูประวัติอบรมรายคน + ชั่วโมงสะสม | AC1 คลิกชื่อผู้เรียนเปิดประวัติ · AC2 ชั่วโมงสะสมนับเฉพาะรายการที่ผ่าน (FIX-04) |
| US-10 | ในฐานะผู้บริหาร ฉันต้องการดู completion rate + ต้นทุนต่อหัว | AC1 นับเฉพาะผลจากรอบ closed (FIX-01) · AC2 ต้นทุนต่อหัว = งบ ÷ ผู้ผ่าน (กันหารศูนย์) (FIX-05) · AC3 filter ตามหลักสูตร |

---

## Section 8 · Status & Lifecycle

### 8.1 Course
```
[ร่าง draft] ──เผยแพร่──▶ [เผยแพร่ published] ──ปิด──▶ [ปิดหลักสูตร closed]
```
| State | Trigger | Next |
|---|---|---|
| draft | เผยแพร่ | published |
| published | ปิดหลักสูตร | closed |
| published | (เงื่อนไข) รับสร้างรอบได้เฉพาะสถานะนี้ | — |

### 8.2 Session
```
[ร่าง draft] ──เปิดรับสมัคร──▶ [เปิดรับ open] ──ปิดรอบ──▶ [ปิดรอบ closed]
```
- เปิดรับ → NTF เปิดรับสมัคร (FN-12) · ปิดรอบ = จบการอบรม → ปลดล็อกการบันทึกผล (FIX-01)

### 8.3 Enrollment
```
ลงทะเบียน ─┬─(has_cost)─▶ [รออนุมัติ pending_doa] ──อนุมัติครบ──▶ [ยืนยัน confirmed]
           └─(ฟรี)──────────────────────────────────────────────▶ [ยืนยัน confirmed]
[confirmed] ──(รอบ closed + เช็คชื่อเข้า + บันทึกผล)──▶ [ผ่าน passed] / [ไม่ผ่าน failed]
[passed] ──ออกใบรับรอง──▶ (soft ref)
ทุก state ──ยกเลิก──▶ [ยกเลิก cancelled] (soft archive)
[pending_doa] ──ไม่อนุมัติ──▶ [cancelled]
```

---

## Section 9 · Business Rules + Validation (with Tags)

| ID | Rule | Type | Tag | ใครเปลี่ยน + บ่อยแค่ไหน |
|---|---|---|---|---|
| R01 (BR-01) | หลักสูตร has_cost → ต้องมีงบ (budget ≥ 0, ห้ามว่าง) | Prevent | **FIXED** | — (กติกาโครงสร้าง) |
| R02 (BR-02) | จำนวนลงทะเบียน (active) ≤ จำนวนรับ (capacity) — เกิน = บล็อก | Prevent | **FIXED** | — |
| R03 (BR-03) | ลงทะเบียนจาก gap (Performance hook) หรือเลือกเอง | Trigger | FIXED | — |
| R04 (BR-04 · LOCK-01) | has_cost → ต้องอนุมัติ (DOA) ก่อนยืนยัน · ฟรี → ข้าม DOA | Prevent | **FIXED** (มติล็อก) | ผู้บริหาร (มติ · ไม่บ่อย) |
| R05 (BR-05 · FIX-01) | บันทึกผลได้เฉพาะรอบที่ปิดแล้ว (closed) | Prevent | FIXED | — |
| R05b (FIX-03) | ต้องเช็คชื่อ attended=true ก่อนบันทึกผล | Prevent | FIXED | — |
| R06 (BR-06 · LOCK-02) | ค่าอบรม = hook Expense (ไม่จ่าย/ไม่ post เอง) | Trigger | FIXED | — |
| R07 (BR-07 · LOCK-03) | gap → หลักสูตร (hook Performance · อ่านอย่างเดียว) | Trigger | FIXED | — |
| R08 (BR-08 · LOCK-05) | audit append-only + masking ตาม role | Prevent | FIXED | — |
| R09 (BR-09 · LOCK-04) | มูลค่าอบรมอนุมัติ → CSQ **EC** เท่านั้น (ไม่มี AC) | Trigger | FIXED (มติล็อก) | ผู้บริหาร (มติ) |
| R10 (BR-10) | snapshot ชื่อ/ตำแหน่ง/แผนกผู้เรียน ณ เวลาลงทะเบียน | Trigger | FIXED | — |
| R11 (FIX-02) | สร้างรอบได้เฉพาะหลักสูตร published | Prevent | FIXED | — |
| R12 (FIX-02) | ส่ง Expense ได้หลัง confirmed + กันส่งซ้ำ (expenseSent) | Prevent | FIXED | — |
| R13 (FIX-02) | อนุมัติได้เฉพาะ role ที่มีสิทธิ์ (canApprove) | Prevent | FIXED | SEC (RBAC · OQ-05) |
| R14 | สายอนุมัติ DOA (จำนวนขั้น + ตำแหน่งแต่ละขั้น) | Config | **CONFIGURABLE** 🤖 | DOA กลาง F-DLG-001 — HR/Admin เปลี่ยนเป็นระยะ |
| R15 (FIX-04) | ชั่วโมงสะสม = ผลรวมชั่วโมงหลักสูตรเฉพาะรายการที่ผ่าน | Calc | FIXED | — |
| R16 (FIX-05) | ต้นทุนต่อหัว = งบ ÷ ผู้ผ่าน (ผู้ผ่าน=0 หรือฟรี → "—" กันหารศูนย์) | Calc | FIXED | — |
| R17 | มูลค่า EC/อัตรากลาง | Config | **DYNAMIC** 🤖 | Rate Card F060 (ยังไม่ dev · display-only) |

### 9.5 สรุประดับความยืดหยุ่น

| Rule | ระดับ Flexibility | เหตุผล | ที่มา |
|---|---|---|---|
| R14 (สาย DOA) | Admin Panel / Rule Management (DOA กลาง) | สายอนุมัติเปลี่ยนตามตำแหน่ง/องค์กร | 🤖 AI-inferred → **OQ-04** ให้ SEC/BA ยืนยัน |
| R17 (มูลค่า EC / อัตรากลาง) | Engine/Rule Management (Rate Card) | อัตราค่าอบรมเปลี่ยนได้ · ห้าม hardcode | 🤖 AI-inferred → **OQ-03** (Rate Card F060 ยังไม่ dev) |
| R01–R13, R15, R16 | FIXED (กติกาโครงสร้าง/มติล็อก) | โครงสร้าง flow + มติ 17 ส.ค. | ✅ LOCK / STANDARD_BASELINE |

> Escalation: R14 (CONFIGURABLE 🤖) และ R17 (DYNAMIC 🤖) → ยกเข้า §15 Open Questions ให้ยืนยันก่อนพัฒนา (C23)

---

## Section 10 · Edge Cases

### 10.1 Edge Cases ที่ PREBRIEF/BA ระบุ (☑ ยืนยันแล้ว)
- ☑ เกินจำนวนรับ → บล็อกลงทะเบียน + note เตือน (BR-02)
- ☑ หลักสูตรมีค่าใช้จ่าย → บังคับ DOA ก่อนยืนยัน (LOCK-01)
- ☑ ค่าอบรม → Expense hook (display-only)
- ☑ gap → แนะนำหลักสูตร (hook)
- ☑ บันทึกผลก่อนปิดรอบ → บล็อก (FIX-01)
- ☑ บันทึกผลก่อนเช็คชื่อ → บล็อก (FIX-03)
- ☑ ส่ง Expense ซ้ำ → กันซ้ำ (FIX-02)
- ☑ ต้นทุนต่อหัวเมื่อผู้ผ่าน=0 → แสดง "—" กันหารศูนย์ (FIX-05)

### 10.2 Edge Cases จาก AI Pattern Matching (☐ = แนะนำ · BA/dev ยืนยันที่ SOW3.7)
- ☐ [CA] ผู้อนุมัติ 2 คนอนุมัติขั้นเดียวกันพร้อมกัน → กันสถานะซ้อน (concurrent)
- ☐ [DI] ผู้เรียน/หมวด/ผู้อนุมัติถูกปิดใช้งานใน master ระหว่างค้างในสาย → นโยบายจัดการ
- ☐ [ST] ยกเลิกการลงทะเบียนหลังส่ง Expense แล้ว → นโยบาย reverse EC (⚠️ กระทบเงิน → **OQ-06**)
- ☐ [CL] duration ที่ parse ชั่วโมงไม่ได้ (รูปแบบแปลก) → ชั่วโมงสะสม = 0 (FIX-04 fallback มีแล้ว)
- ☐ [PM] viewer เห็นตัวเงิน mask — ตรวจว่า export/report ก็ mask ตาม role (FN-94)
- ☐ [EN] Rate Card พร้อมภายหลัง → migrate มูลค่า EC จาก display-only เป็นตัวเลขจริง

---

## Section 11 · Impact / Regression
New Feature — ไม่มี regression กับของเดิม แต่มี integration points (ดู §12.1):
- Performance (F131): เพิ่มการ "อ่าน" gap — ไม่แก้ข้อมูล Performance
- Expense Claim (F101): เพิ่ม hook รับมูลค่า EC — ต้องไม่ auto-post
- HR Config (F164): เพิ่มการ "อ่าน" หมวดหลักสูตร — ไม่ CRUD

---

## Section 12 · System Context

### 12.1 Value Stream & Downstream Impact ⭐

**Value Stream:** Human Capital → Learning & Development (พัฒนาบุคลากร)
**Upstream:** Performance Appraisal (F131 · gap ผลประเมิน → แนะนำผู้เรียน) · HR Configuration (F164 · หมวดหลักสูตร) · Employee (F011 · ผู้เรียน/ผู้อนุมัติ)

**Downstream Impact Map:**

| ปลายทาง | ข้อมูลที่ไหลไป | Trigger | ถ้าเปลี่ยน/ยกเลิกกลางทาง |
|---|---|---|---|
| Expense Claim (F101) | มูลค่าอบรม (EC · hook display-only) | ลงทะเบียน confirmed (has_cost) + กดส่ง | ยกเลิกหลังส่ง → ต้องมีนโยบาย reverse EC (**OQ-06**) |
| CSQ / โครงสร้างต้นทุน | ยิงมูลค่า EC (ไม่มี AC) | อนุมัติ DOA ครบ → confirmed | EC ไม่ post บัญชี — ผลกระทบ GL = ไม่มี (Expense เป็นตัวลงบัญชี) |
| DOA กลาง (F-DLG-001) | คำขออนุมัติ + ผู้อนุมัติตามตำแหน่ง | ส่งอนุมัติ (has_cost) | สายอนุมัติเปลี่ยนที่ DOA กลาง — feature ประกาศเท่านั้น |
| ENG-NOTIFY | 3 event (เปิดรับ/ยืนยัน/ผล) | state transition | ไม่มี event = ผู้เรียนไม่รู้สถานะ |
| ประวัติอบรม/ชั่วโมงสะสมรายคน | ผล passed + ชั่วโมง | บันทึกผล ผ่าน | ป้อนข้อมูล competency/พัฒนาบุคลากร (อนาคต) |
| Rate Card (F060 · ยังไม่ dev) | อัตรากลาง ← อ่านมาแสดง EC/ต้นทุนต่อหัว | เมื่อ Rate Card พร้อม | ตอนนี้ display-only (**OQ-03**) |

**ผลกระทบแนวขวาง:** งบประมาณ (งบภายในหลักสูตร · แยกจาก EC) · บัญชี/GL = **ไม่กระทบ** (EC ไม่ post) · รายงาน = completion rate + ต้นทุนต่อหัว

### 12.3 Existing System Reference

| Rule/องค์ประกอบ | ระดับ | มีอยู่แล้ว? | Reference |
|---|---|:--:|---|
| สายอนุมัติ (R14) | DOA กลาง | ✅ | F-DLG-001 Policy Center (feature ประกาศ · doa-declaration) |
| แจ้งเตือน (FN-12) | ENG-NOTIFY | ✅ | F-NOTIFY (ntf-declaration) |
| หมวดหลักสูตร | HR Config | ✅ | F164 (อ่านอย่างเดียว · #107) |
| มูลค่า EC / อัตรากลาง (R17) | Rate Card | ❌ | F060 ยังไม่ dev → display-only |
| Expense hook (R06) | Expense Claim | ✅ | F101 (hook display-only) |
| gap (R07) | Performance | ✅ | F131 (hook อ่านอย่างเดียว) |
| เลขรันเอกสาร | — | N/A | ใบรับรอง soft ref — ไม่ใช้ doccfg |

---

## Section 13 · Delivery Phases

**Phase 1 — Feature Launch (ทุกอย่างไม่ hardcode ตั้งแต่วันแรก):**
- Course/Session/Enrollment entity + state machine (3 lifecycle)
- has_cost gate (DOA/no-DOA) · attendance + result guard (FIX-01/03) · function guards (FIX-02)
- hook Expense (display-only) · hook Performance gap (read) · หมวดจาก HR Config (read)
- audit append-only + masking · NTF 3 event · report completion + ต้นทุนต่อหัว (FIX-05)
- **Declarations** (รันหลัง step 7 โดยผู้ใช้สั่ง): DOA · NTF · CSQ EC

**Phase 2 — เมื่อ Rate Card (F060) พร้อม:**
- ผูกมูลค่า EC/ต้นทุนต่อหัวจาก display-only → ตัวเลขจริง (R17)

**Phase 3 — Rule Management (ถ้า SEC/BA เคาะ):**
- ปรับ RBAC matrix (OQ-05) · ปรับ configurability สาย DOA (OQ-04)

---

## Section 14 · Dev Requirements Summary ("ใบสั่ง")

### 14.1 Config Foundation ที่ต้องเตรียม
- หมวดหลักสูตร: ผูก read-only จาก HR Config (F164) — ห้าม CRUD ในหน้านี้
- DOA entry `DOA-TRAIN-ENROLL-001` (ไม่มีวงเงิน) — สายจริงจาก F-DLG-001 (ห้าม hardcode สายในโค้ด)
- EC (CSQ) — โครงสร้างรับมูลค่าอบรม (ไม่มี AC · Expense ลงบัญชี)

### 14.2 ข้อกำหนดจาก Tag
- R14 (CONFIGURABLE): สาย DOA อ่านจาก DOA กลาง — ใช้ engine ที่มีอยู่ ไม่สร้างใหม่
- R17 (DYNAMIC): มูลค่า EC ต้องดึงจาก Rate Card เมื่อพร้อม — ตอนนี้ render display-only "อ้างอิง Rate Card · เชื่อมเมื่อพร้อม" ห้ามใส่ตัวเลขคงที่

### 14.3 ข้อกำหนดจาก Edge Cases / Validation (ต้อง handle เป็นพิเศษ)
- FIX-01: บันทึกผล + completion rate นับเฉพาะรอบ closed (defense-in-depth ทั้ง UI + submit)
- FIX-02: guard สร้างรอบ (published) · ส่ง Expense (confirmed+กันซ้ำ) · อนุมัติ (canApprove)
- FIX-03: attendance ต้อง true ก่อนบันทึกผล · eval 1-5 optional
- FIX-04: parse ชั่วโมงจาก duration (fallback 0) · นับสะสมเฉพาะ passed
- FIX-05: ต้นทุนต่อหัวกันหารศูนย์ + mask ตาม role

### 14.4 WARNING ที่รอข้อสรุป
- ดู §15 Open Questions (OQ-01..06)

### 14.6 Screen Inventory + UI Signals (หยาบ — ส่งต่อ FRD)

**Iron Rule #104:** 1 feature = 1 เมนู "Training & Development" · ส่วนย่อยเป็น **4 tabs** ในหน้าเดียว (route `#/train/<tab>`)

| # | ชื่อหน้า/overlay | route/trigger จริง | ประเภทหยาบ | ผู้ใช้หลัก | หน้าที่ (business) |
|---|---|---|---|---|---|
| P-01 | หลักสูตร (Course Catalog) | `#/train/course` | หน้ารายการ | HR L&D | ค้นหา/ดูหลักสูตร + สร้าง |
| P-02 | แผน / ลงทะเบียน (Session & Enrollment) | `#/train/plan` | หน้ารายการ | HR L&D · ผู้อนุมัติ | รอบอบรม + งานรออนุมัติของฉัน |
| P-03 | ผล / ใบรับรอง (Results & Certificates) | `#/train/result` | หน้ารายการ | HR L&D | บันทึกผล/ออกใบรับรอง |
| P-04 | รายงานการอบรม (Completion) | `#/train/report` | dashboard/รายงาน | ผู้บริหาร · HR | completion rate + ต้นทุนต่อหัว + scope-out |
| P-05 | ฟอร์มสร้าง/แก้ไขหลักสูตร | drawer (course form) | ฟอร์มสร้าง (ขั้นเดียว) | HR L&D | กรอกหลักสูตร + has_cost/งบ |
| P-06 | รายละเอียดหลักสูตร | drawer (course view) | หน้ารายละเอียด | ทุก role | ดู + เผยแพร่/ปิด + EC ref |
| P-07 | ฟอร์มสร้าง/แก้ไขรอบอบรม | drawer (session form) | ฟอร์มสร้าง (ขั้นเดียว) | HR L&D | กรอกรอบ + จำนวนรับ |
| P-08 | รายละเอียดรอบอบรม | drawer (session view · 4 sub-tabs: รายละเอียด›ผู้เรียน›อนุมัติ/ค่าใช้จ่าย›ประวัติ) | หน้ารายละเอียด | HR L&D · ผู้อนุมัติ | จัดการผู้เรียน/เช็คชื่อ/อนุมัติ/EC/ประวัติ |
| P-09 | ลงทะเบียนผู้เรียน | modal (enroll · gap picker) | หน้ายืนยัน/ฟอร์ม | HR L&D | เลือกจาก gap หรือค้นหาเอง |
| P-10 | ส่งอนุมัติ (DOA) | modal (slot picker) | หน้ายืนยัน | HR L&D | เลือกผู้อนุมัติตามตำแหน่งแต่ละขั้น |
| P-11 | บันทึกผล + ประเมิน | modal (result) | หน้ายืนยัน | HR L&D | ผ่าน/ไม่ผ่าน + คะแนน 1-5 + comment |
| P-12 | ประวัติอบรมรายคน | modal (emp history) | หน้ารายละเอียด | ทุก role | รายการอบรม + ชั่วโมงสะสม (FIX-04) |

**สรุป:** ~4 หน้าหลัก (tabs) + 8 overlay (2 drawer form · 2 drawer view · 4 modal) = 1 เมนูเดียว

**UI Signals ส่งต่อ FRD:**
- Archetype = **master** (ไม่ใช่ Q-document) — มี "ส่ง/เซ็น" ผ่าน DOA แต่ไม่มี PDF เอกสารทางการ
- print/PDF: ❌ (ใบรับรอง soft ref · รายงาน export CSV = "ต่อ dev")
- NON-STANDARD: — (ไม่มี · ตาม html-generator-v9 มาตรฐาน)

---

## Section 15 · Open Questions

| ID | คำถาม | สถานะ | หมายเหตุ |
|---|---|:--:|---|
| OQ-01 | **FN-10 framing:** จอทำ "แนะนำผู้เรียนที่มี gap" ในขณะ checklist เขียน "แนะนำหลักสูตร" — hook เนื้อในครบ · qc นับครอบ | ⚠️ รอ BA ยืนยัน framing | ไม่กระทบ logic · เป็นเรื่องถ้อยคำ/มุมมอง |
| OQ-02 (A-TRN-03) | ใบรับรอง = soft ref (ไม่มีเลขรัน/PDF) — ยืนยันว่าไม่ต้องออกเอกสารทางการรอบนี้ | ⚠️ รอยืนยัน | [ASSUMED] ตาม LOCK-07 |
| OQ-03 (A-TRN-01) | Rate Card (F060) ยังไม่ dev → มูลค่า EC/ต้นทุนต่อหัว display-only จนกว่าพร้อม | ⚠️ รอ dev Rate Card | R17 DYNAMIC 🤖 |
| OQ-04 | สาย DOA (R14) — จำนวนขั้น/ตำแหน่งจริง + DOA role-id master หายจาก install → ใช้ [DEFAULT] 2 ขั้น (หัวหน้าสายงาน + ผจก.พัฒนาบุคลากร) · CL-0013 (สายอนุมัติผู้บริหาร) แขวน | ⚠️ รอ SEC/BA เคาะ | ห้ามให้ skill เดารหัสสาย · เดาผิดมีคนตั้งค่าจริง |
| OQ-05 | RBAC matrix — หัวหน้า "สร้างได้/อนุมัติอย่างเดียว"? prototype ให้ non-viewer ทำได้ (recruit precedent) | ⚠️ รอ SEC/BA เคาะ | §4 note ¹ |
| OQ-06 | ยกเลิกการลงทะเบียนหลังส่ง Expense (EC) แล้ว → นโยบาย reverse EC | ⚠️ รอ BA/Finance | กระทบเงิน — ยกทันที (§10.2) |
| OQ-UX | ศัพท์ระบบบนจอ (hook / EC / CSQ) · แถวชื่อหลักสูตรยาว | ⚠️ รอ BA | UX judgment |

---

## Section 16 · Security & Compliance

### 16.1 Security Preset
**P6 (HR / PII Sensitive · 15 controls)** — feature จัดการข้อมูลบุคคล (ผู้เรียน/ผู้อนุมัติ) + ตัวเงิน (งบ/EC) + สายอนุมัติ

### 16.2 Applicable Standards (ย่อ)
- PDPA (ข้อมูลพนักงาน) ✅ · SoD/COSO (Maker≠Approver) ✅ · Audit trail (append-only) ✅ · Access control (RBAC) ✅

### 16.3 Control Checklist (สำคัญ)
| Control | Required | Implementation |
|---|:--:|---|
| RBAC ตาม role (hr/manager/viewer) | ✓Must | FN guard + persona (canApprove/unmask) |
| Data masking ตัวเงิน | ✓Must | maskMoney() สำหรับ viewer (FN-94) |
| Audit append-only ทุก mutation | ✓Must | audit() unshift ทุก create/แก้/อนุมัติ/ผล (FN-93) |
| SoD DOA (Maker≠Approver) | ✓Must | HR ลงทะเบียน · หัวหน้า/ผจก. อนุมัติ |
| Snapshot ผู้เรียน (กันข้อมูลเปลี่ยนย้อนหลัง) | ✓Must | empSnap ณ ลงทะเบียน (BR-10) |
| กัน double-submit / ส่ง Expense ซ้ำ | ○Should | TC.busy + expenseSent (FIX-02) |

### 16.4 Risk Statement
- Risk-1: ตัวเงิน (งบ/ต้นทุน) รั่วถึง viewer → mitigated by masking (FN-94)
- Risk-2: อนุมัติข้ามสิทธิ์ → mitigated by canApprove guard (R13/FIX-02)
- Risk-3: ค่าอบรม auto-post บัญชีโดยไม่ตั้งใจ → mitigated by hook display-only (LOCK-02/04)

---

## Section 17 · Health Check

### 17.1 SLA
- ลงทะเบียน (มีค่าใช้จ่าย) → อนุมัติครบ ≤ 3 วันทำการ (owner: ผู้อนุมัติ)
- บันทึกผล ≤ 5 วันทำการหลังปิดรอบ (owner: HR L&D)

### 17.2 Control Points
- ทุกการอนุมัติ/ปฏิเสธ/บันทึกผล/ส่ง EC ผ่าน audit append-only (map จาก §16.3)

### 17.3 KPI (คู่กับ §2.3)
- Completion rate ≥ 80% (จากรอบ closed)
- สัดส่วนลงทะเบียนจาก gap ≥ 40%
- เวลาอนุมัติ DOA เฉลี่ย ≤ 3 วัน
- ต้นทุนต่อหัว (ติดตามแนวโน้ม · display-only)

### 17.4 Threshold
- จำนวนลงทะเบียน = capacity → Max (บล็อกเพิ่ม · BR-02)
- ผู้ผ่าน = 0 → ต้นทุนต่อหัว "—" (กันหารศูนย์ · FIX-05)

### 17.5 Throughput
- Capacity ต่อรอบ = ตาม field capacity · ต่อยอดได้ด้วยการสร้างรอบเพิ่ม

---

## Section 18 · Monitoring

### 18.1 Reports Overview
- **Performance report:** completion rate ต่อหลักสูตร (funnel · FN-13)
- **Cost report:** ต้นทุนต่อหัว (มุม EC · FIX-05)
- **Transaction report:** รายการลงทะเบียน/ผล (filter ตามหลักสูตร) + Export CSV (ต่อ dev)
- **Anomaly:** ผู้ผ่าน=0 ในหลักสูตรมีค่าใช้จ่าย → ต้นทุนต่อหัวคำนวณไม่ได้ (flag "—")

### 18.2 Dashboard Widgets (หน้า Report)
- stat cards: หลักสูตร / รอบอบรม / ลงทะเบียนทั้งหมด / ผ่าน / อัตราผ่าน
- funnel completion rate ต่อหลักสูตร
- การ์ดต้นทุนต่อหัว (mask ตาม role)
- ขอบเขตที่ไม่รองรับ (unsupported 5 · แสดงเตือน)

---

## Cross-Section Coverage Check
- ✅ ทุก Business Condition (§9) มี Edge Case cover (§10)
- ✅ ทุก Control runtime (§16) มี Control Point (§17.2)
- ✅ ทุก KPI/Threshold (§17) มี Widget/Report (§18)
- ✅ FN 18/18 map เข้า §5/§7/§9 + capability ใหม่ FIX-01..07 อยู่ครบ (§3.1, §9, §14.3)

---

## Section 14.7 · AI Review Report (Quality Gate)

```
═══════════════════════════════════════
AI REVIEW REPORT — BRD Generator Full
BRD: BRD-F-HR-TRAIN — Training / อบรม
ประเภท: New Feature · วันที่: 2026-09-03
───────────────────────────────────────
✅ C01 Business Objective วัดผลได้ (§2.3 มีตัวเลข/แหล่งวัด)
✅ C02 User Roles ครบ (§4)
✅ C05 Story ไม่มีคำว่า "และ" ที่ทำให้ควรแยก
✅ C10 ทุก rule มีตัวเลข/เงื่อนไขติด Tag (§9)
✅ C13 Edge Cases ครบหมวด (§10.1/10.2)
✅ C18 WARNING ทุกข้อมีแผน (§15 OQ-01..06)
✅ C19 Section 14 ใบสั่งครบ
✅ C20 Scope Lock §3.4 ครบ (LOCK-01..07) · SCOPE DRIFT = none
✅ C21 Value Stream §12.1 ทุกแถวตอบ "แล้วไงต่อ"
✅ C22 ตัวชี้วัด §2.3 มี baseline/target/วิธีวัด + คู่ใน §17.3
✅ C23 §9.5 marker 🤖/✅ ครบ — R14/R17 (🤖) ลง OQ แล้ว
✅ PE01 COSO Roles ครบทุก step (§5.1)
✅ PE02 SoD ผ่าน (HR Maker ≠ หัวหน้า/ผจก. Approver)
✅ PE03 Security Preset P6 + controls (§16)
✅ PE04 SLA/KPI/Threshold ครบ (§17)
✅ PE05 Cross-section coverage ผ่าน
───────────────────────────────────────
ผ่าน: 16/16 · สถานะ: ✅ APPROVED
Note: 6 Open Questions (OQ-01..06 + OQ-UX) เป็น decision ของ BA/SEC/Finance
      ไม่บล็อกเอกสาร — dev ห้ามเริ่มส่วนที่ผูก OQ-03/04/05/06 จนกว่า resolve
═══════════════════════════════════════
```

**Declaration รอบนี้ (บันทึกไว้ · รันหลัง step 7 โดยผู้ใช้สั่งเท่านั้น):** DOA ✓ · NTF ✓ · CSQ EC ✓ (ไม่มี AC) · doccfg ✗ · pdfdoc ✗ — **BA/ผู้ใช้เป็นผู้สั่ง AI ไม่เรียกเอง**

---
*BRD นี้สร้างจาก HTML source of truth (`อบรม.html`) + PREBRIEF + FUNCTION_CHECKLIST (18 FN) + STANDARD_BASELINE + HANDOFF · Conflict Priority: LOCK > PREBRIEF > HTML · ถัดไป: frd-generator-v6*
