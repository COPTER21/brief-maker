# DOA_BRIEF — F-HR-TRAIN (F133 · อบรม / Training)

> **ใบประกาศ DOA** — feature นี้ **ประกาศ**ว่ามีการอนุมัติหน้าตาแบบไหน แล้วคนเอาใบนี้ไป **ตั้งค่าจริงที่หน้า DOA กลาง (F-DLG-001 · Policy Center)**
> feature **ห้าม hardcode สายอนุมัติ** — สาย resolve runtime จาก DOA entry ณ เวลาส่งอนุมัติ แล้ว freeze ลง `approval_chain` (BR-DOA-02 · LD-05)
> **wire_status: `pending`** (ยังไม่ตั้งค่า DOA จริง)

---

## ⚠️ หมายเหตุสำคัญ (อ่านก่อน) — DOA master ไม่มีในการติดตั้งนี้

`.claude/skills/doa-declaration/references/doa-contract.md` **ไม่มีอยู่จริง** ในการติดตั้งชุดนี้ (มีแค่ `SKILL.md` — เหมือนกรณี F-HR-RECRUIT)
→ จึง **ยืนยัน `role-*` id กับทะเบียน DOA master ไม่ได้** ทุก role ในใบนี้ติดแท็ก `[DEFAULT — รอยืนยัน]`
→ Quality Gate **G1 ตรวจไม่ผ่านเชิงบวก** (verify กับ master ไม่ได้) — ดู §Quality Gate + **OQ-DOA** ท้ายใบ
→ นอกจากนี้มี **role-id drift** ที่ขั้นที่ 2 (`role-hr-dev-head` บนจอ vs `role-hr-ld-head` ในบรีฟต้นทาง) — **ไม่เลือกข้างในใบนี้** ยกเป็น OQ

---

## §1. Identity

| field | value |
|---|---|
| feature_id | **F-HR-TRAIN** (F133) |
| name | อบรม / Training |
| module | HR (Human Resources) |
| platform | Web (SPA · html-generator-v9) |
| approval_scope | **`policy_approve`** — อนุมัติเชิงนโยบาย/สิทธิ์ HR (ลงทะเบียนอบรมที่มีค่าใช้จ่าย) · **ไม่ใช่** `document_sign` (ไม่มีเอกสารพิมพ์ที่ต้องเซ็นลายเซ็นใน PDF · ใบรับรอง = soft ref ไม่มีเลขรัน · BR-07C) |
| จำนวนสายอนุมัติ (Q1) | **1 สาย** → ใช้ `matrix` เดียว (action เดียว: อนุมัติการลงทะเบียน) |
| มีวงเงินไหม (Q2) | **ไม่มีวงเงิน** `[ASSUMED · ตามงบ]` — อนุมัติตามระดับตำแหน่ง ไม่ผูก threshold ยอดเงิน · gate = **มี/ไม่มีค่าใช้จ่าย** (`has_cost`) ไม่ใช่จำนวนเงิน (LOCK-01 · BR-04) |
| แยกตามแผนก (Q3) | **merged** — ทุกแผนกใช้กฎชุดเดียว |
| DOA engine | F-DLG-001 (Policy Center) · resolve ผ่าน `FN-09` (external read) · mock บนจอ = `doaResolve()` |
| DOA entry ref (บนจอ) | `DOA-TRAIN-ENROLL-001` (จาก `doaResolve()` บรรทัด ~2191) |

---

## §2. Approval Actions (1 action)

action เดียว **ไม่ผูกวงเงิน** — เป็น role-based ตามระดับตำแหน่ง · SoD บังคับ maker ≠ approver (BR-DOA-04 · §5.3 Permission Matrix)

### อนุมัติการลงทะเบียนอบรม (Enrollment · เฉพาะ `has_cost`)
| หัวข้อ | รายละเอียด |
|---|---|
| kind | `train_enroll` |
| gate | **เฉพาะหลักสูตรมีค่าใช้จ่าย** (`has_cost=true`) → `status='pending_doa'` · **หลักสูตรฟรี → ข้าม DOA** ยืนยันทันที (`confirmed`) (LOCK-01 · BR-04 · FN-05) |
| trigger | ลงทะเบียนผู้เรียน (`submitEnroll`) → ถ้า has_cost เปิด slot picker (`openDoaModal`) → กด **ส่งอนุมัติ** (`submitDoa`) → resolve chain ผ่าน `FN-09` |
| approve (ครบทุก slot) | status `pending_doa → confirmed` → **ยืนยันการลงทะเบียน** + emit CSQ event `train.enrolled_paid` (EC · BR-09 · FN-10) |
| reject (slot ใด slot หนึ่ง) | `pending_doa → cancelled` · **บังคับใส่เหตุผล** (BR-18 · `ERR_REASON_REQUIRED`) · ประวัติ append-only (BR-DOA-03) |
| enforced by | `enrollApprove()` / `enrollReject()` — เฉพาะ persona `canApprove` (BR-13 · `ERR_NOT_APPROVER` 403) · `BR_DOA_SLOTS_INCOMPLETE` ถ้าเลือกผู้อนุมัติไม่ครบ · `BR_COURSE_NOT_PAID` ถ้าเรียก DOA กับหลักสูตรฟรี |

> **หมายเหตุ:** การอนุมัติ **ไม่เปลี่ยนตามยอดงบ** — `budget`/มูลค่า EC เป็น business field (Restricted · mask ตาม role) ไม่ใช่ input ของการ resolve สาย DOA · `cost` เก็บไว้เผื่อทำ threshold ภายหลัง แต่รอบนี้ไม่ใช้ (OQ ท้ายใบ)

---

## §3. Matrix ที่จะไปตั้งค่าที่ DOA กลาง

> 1 set ครอบทุกยอด: `amount_from: 0 · amount_to: null` (ไม่มีวงเงิน · ปิดปลายเปิด) · `chainMode: sequential`
> ทุก role ติดแท็ก **`[DEFAULT — รอยืนยัน]`** — master ไม่มีในการติดตั้งนี้ ยืนยันไม่ได้ (ดู OQ-DOA)

### set 1 — `train_enroll` (อนุมัติการลงทะเบียนอบรมที่มีค่าใช้จ่าย)
| field | value |
|---|---|
| amount_from | `0` (บาท) |
| amount_to | `null` (ไม่จำกัด — ไม่มีวงเงิน · gate = `has_cost`) |
| departments | `merged` (ทุกแผนก) |
| chainMode | `sequential` (2 ขั้น) |
| steps[roles] | ① `role-line-manager` **[DEFAULT — รอยืนยัน]** — หัวหน้าสายงานของผู้เรียน → ② **`role-hr-dev-head` ⟷ `role-hr-ld-head`** **[DEFAULT — รอยืนยัน · ⚠️ DRIFT — ยังไม่เลือกข้าง]** — ผจก.ฝ่ายพัฒนาบุคลากร |

> **⚠️ DRIFT ที่ขั้นที่ 2 (ยังไม่ตัดสินในใบนี้):**
> - บนจอ (`doaResolve()` · `อบรม.html` บรรทัด 2193) ใช้ **`role-hr-dev-head`**
> - บรีฟต้นทาง (`Pack Brief Feature/.../DOA_BRIEF.md` §3) + BR-14 ระบุ **`role-hr-ld-head`**
> - เป็นตำแหน่งเดียวกัน ("ผจก.ฝ่ายพัฒนาบุคลากร") แต่ **id ต่างกัน** → **ห้ามเดา/เลือกข้าง** เพราะ dev เอา id ไปตั้งค่าจริง → **OQ-DOA / OQ-04**
>
> **ไม่มีคอลัมน์วงเงิน/tier** ในตารางนี้โดยเจตนา — feature นี้ไม่มีวงเงิน (ต่างจาก PR/PO)
> **CL-0013 (สายอนุมัติผู้บริหาร) ยังแขวน** — ถ้ามติกำหนดให้เพิ่ม slot ระดับผู้บริหาร ตั้งเพิ่มที่ DOA กลางได้ (สาย resolve runtime · feature ไม่ต้องแก้โค้ด)

---

## §4. Field Contract สำหรับ FRD (entity: enrollment + T_training_approval_step)

field ที่ entity ต้องมี (สอดคล้อง 04_DB · FRD Injection §Entity) — **ไม่มี field ยอดเงินใน `doa_resolve_payload`**

| field | type | null | หมายเหตุ |
|---|---|---|---|
| `approval_required` | bool | NO | มาจาก DOA entry (ผูก `has_cost`) — ไม่ใช่ค่าคงที่ในตาราง |
| `approval_status` | enum | YES | แมปกับ enrollment state: `pending_doa \| confirmed \| cancelled` (draft/rejected → cancelled ตาม §5.2) |
| `doa_entry_ref` | string(40) | YES | FK ทะเบียน DOA (`DOA-TRAIN-ENROLL-001`) · nullable ตอน Phase 1 |
| `approver_role` | string | — | role ที่ต้องเซ็นในขั้นปัจจุบัน (resolve จาก DOA slot · ไม่ hardcode) |
| `approved_by` | string (user id) | YES | user/EMP ที่เซ็นจริงในแต่ละ slot (`approver_id`) |
| `approval_chain` | jsonb | YES | **snapshot สายที่ resolve ตอนส่ง · append-only** — `[{order, slotName, approver_role, approver_id, result, at}]` |
| `approved_at` | timestamp | YES | เวลาอนุมัติครบทุก slot |

> **⛔ ไม่มี field ยอดเงินใน `doa_resolve_payload`** — การ resolve สายไม่ผูก threshold · `budget` เป็น business field (Restricted · mask) ไม่ใช่ input ของ DOA
> map DB จริง (04_DB): approval summary ฝังใน enrollment + child table `T_training_approval_step` (order/slotName/approver_id/result/at) — AT-03

---

## §5. UI Contract สำหรับ HTML (อ้าง `outputs/F-HR-TRAIN/อบรม.html` ที่มีอยู่จริง)

พฤติกรรมที่หน้าจอ **มีแล้ว** และเป็นสัญญากับ dev (อ้าง function/selector จริงในไฟล์):

| ส่วน | ในไฟล์ปัจจุบัน |
|---|---|
| **Slot picker (DOA)** | modal "ส่งอนุมัติลงทะเบียน (DOA)" (บรรทัด ~2932) — `.slot`/`.slot-h` (เลข slot + ชื่อ slot + role id monospace `.sr`) + `searchSelectHTML('slot_N')` เลือกคนตามตำแหน่ง · chain มาจาก `doaResolve()` (mock resolved · 2 slot · ไม่มีวงเงิน · แสดง DOA entry `DOA-TRAIN-ENROLL-001`) |
| **ปุ่ม ส่งอนุมัติ** | ลงทะเบียนหลักสูตร has_cost → ปุ่ม "ลงทะเบียน + ส่งอนุมัติ" (`submitEnroll` → `openDoaModal`) → modal → `submitDoa()` set `status='pending_doa'` |
| **ปุ่ม อนุมัติ / ไม่อนุมัติ** | `enrollApprove()` / `enrollReject()` (บรรทัด ~2817/2830) แสดงเฉพาะ persona `canApprove` (บรรทัด 2705) · **ไม่อนุมัติ = บังคับเหตุผล** (BR-18) · guard `showToast('เฉพาะผู้อนุมัติ (DOA) เท่านั้น')` |
| **Badge สถานะ** | `ENROLL_STATUS` — `pending_doa` → `pill-warning` (รออนุมัติ DOA) · `confirmed` → `pill-info` · `passed` → `pill-success` · `cancelled` → `pill-muted` — CI Warm Light |
| **Approval Timeline** | `.timeline` (บรรทัด ~2618) — ไล่ทีละ slot: "ขั้น N: slotName" → `emp-chip` ผู้เซ็น → ผล (รอ/อนุมัติ+วันที่/ไม่อนุมัติ) · dot สี is-warning/is-success |
| **Hook My Approval** | `approvalHook` (บรรทัด ~2394) — "งานรออนุมัติของฉัน · N รายการ" นับ enrollment `status==='pending_doa'` |

**ข้อห้าม (คงไว้):** ห้าม `const APPROVAL_CHAIN = [...]` ในไฟล์ feature · ปัจจุบันใช้ `doaResolve()` mock พร้อม comment `[PENDING · DOA engine] ห้าม hardcode สายในโค้ด feature` (บรรทัด 2188–2189) · mock **1 tier** พอ (ไม่มีวงเงิน — ไม่ต้อง 2 tier)

---

## §6. Wire Checklist (dev · จน `wire_status: pending → wired`)

- [ ] สร้าง DOA entry จริงที่หน้า DOA กลาง — **1 entry** (`DOA-TRAIN-ENROLL-001` · merged · ไม่มีวงเงิน · sequential 2 slot)
- [ ] **ยืนยัน `role-*` id กับ DOA master** — ขั้น 1 `role-line-manager` · ขั้น 2 **`role-hr-dev-head` หรือ `role-hr-ld-head`** (⚠️ DRIFT · ปัจจุบัน `[DEFAULT]` · รอ **OQ-DOA/OQ-04**)
- [ ] wire `FN-09` resolve chain → Policy Center (F-DLG-001) แทน mock `doaResolve()`
- [ ] gate: resolve/ส่ง DOA **เฉพาะ `has_cost=true`** · ฟรี → ข้าม (LOCK-01 · BR-04)
- [ ] resolve สายตอนกดส่งอนุมัติ แล้ว **snapshot freeze** ลง `approval_chain` (BR-DOA-02 · LD-05)
- [ ] SoD: maker ≠ approver (BR-DOA-04 · BR-13 · `ERR_NOT_APPROVER`)
- [ ] reject → `cancelled` + เหตุผล append-only (BR-DOA-03 · BR-18)
- [ ] ใบ `pending_doa` โผล่ใน My Approval จริง
- [ ] ถ้า CL-0013 สรุปให้เพิ่ม slot ผู้บริหาร → เพิ่มที่ DOA กลาง (ไม่แก้โค้ด feature)
- [ ] toggle `wire_status: pending → wired` + อัปเดต `FEATURE_REGISTRY.md`

---

## §7. Open Questions

### 🔴 OQ-DOA (= OQ-04) — ยืนยัน role id + drift ขั้นที่ 2 กับ DOA master
- **owner:** พี่เบิร์ด / BA / SEC
- **ref:** DOA_BRIEF ต้นทาง (Pack Brief §3 · §7 OQ) · FRD BR-14 · 07_LOCKED LD-05 · 00_OVERVIEW OQ-04
- **คำถาม:**
  1. ยืนยัน `role-*` id **ขั้น 1** = `role-line-manager` (หัวหน้าสายงานของผู้เรียน) ตรงกับทะเบียน DOA master หรือไม่ — ปัจจุบัน `[DEFAULT — รอยืนยัน]` เพราะ **master `references/doa-contract.md` ไม่มีในการติดตั้งชุดนี้ → ยืนยันเองไม่ได้**
  2. **⚠️ DRIFT ขั้น 2:** ผจก.ฝ่ายพัฒนาบุคลากร — บนจอใช้ `role-hr-dev-head` · บรีฟต้นทาง/BR-14 ใช้ `role-hr-ld-head` — **id ไหนถูก?** (เดาผิดมีคนเอาไปตั้งค่าจริง · ใบนี้ **ไม่เลือกข้าง**)
  3. **CL-0013** (สายอนุมัติผู้บริหาร) แขวนอยู่ — ต้องเพิ่ม slot ที่ 3 (ระดับผู้บริหาร) สำหรับหลักสูตรค่าใช้จ่ายสูงหรือไม่?
  4. รอบนี้ยืนยัน **ไม่มีวงเงิน (ไม่มี threshold)** ใช่หรือไม่ (`[ASSUMED · ตามงบ]`) — ถ้าอนาคตจะแยกชั้นตามยอดงบ ต้องแปลง set เดียวเป็นหลายช่วง
- **บล็อกอะไร:** ไม่บล็อก HTML/FRD (สาย resolve runtime · declaration เท่านั้น) แต่ **บล็อกการตั้งค่า DOA จริง** (dev ต้องได้ id ยืนยัน + เคลียร์ drift ก่อน wire)

### OQ อื่นที่เกี่ยวข้อง (context · owner เดิม · ไม่กระทบ matrix DOA โดยตรง)
- **OQ-05** — RBAC หัวหน้า "สร้างได้/อนุมัติอย่างเดียว" (SEC/BA) · กระทบว่า persona ไหน `canApprove`
- **OQ-06** — นโยบาย reverse EC เมื่อ cancel หลังส่ง Expense (BA/Finance) · ไม่กระทบสาย DOA
- **OQ-03** — มูลค่า EC/อัตรากลางจาก Rate Card (F060 · pending) · ไม่กระทบสาย DOA

---

## ✅ Quality Gate (G1–G7)

| # | เช็ค | ผล |
|---|---|---|
| **G1** | ทุก role เป็น `role-*` ที่มีใน master | **⚠️ ยืนยันเชิงบวกไม่ได้** — `references/doa-contract.md` ไม่มีในการติดตั้งนี้ · ทุก role ติด `[DEFAULT — รอยืนยัน]` + **DRIFT ขั้น 2 ยังไม่เลือกข้าง** → ยก **OQ-DOA** (ไม่แต่ง id ใหม่นอกจากที่มีบนจอ/บรีฟ) |
| **G2** | ทุก set มี `amount_from` + `amount_to` | ✅ ครบ (`0` / `null`) |
| **G3** | ถ้ามีวงเงิน — ช่วงต่อเนื่องไม่ทับ | **N/A** — ไม่มีวงเงิน (1 set ครอบทุกยอด) |
| **G4** | set สุดท้าย `amount_to: null` | ✅ `amount_to: null` |
| **G5** | `approval_scope` เป็น 1 ใน 3 ค่าจริง | ✅ `policy_approve` |
| **G6** | ค่าที่ยังไม่ยืนยันติด `[DEFAULT — รอยืนยัน]` | ✅ ครบทุก role §3 · §6 · OQ-DOA + `[ASSUMED]` ที่ "ไม่มีวงเงิน" |
| **G7** | ไม่มีสายอนุมัติ hardcode ใน FRD/HTML | ✅ HTML ใช้ `doaResolve()` mock (comment `[PENDING · DOA engine] ห้าม hardcode`) · ไม่มี `const APPROVAL_CHAIN` · FRD `FN-09` resolve runtime (LD-05) |

**สรุป:** G2–G7 ผ่าน · **G1 ยืนยันเชิงบวกไม่ได้เพราะ master หาย + มี drift ขั้น 2 → ปิดด้วย OQ-DOA + แท็ก [DEFAULT — รอยืนยัน] ทุก role** (ไม่เคลมว่า G1 ผ่าน)

---

## 📌 งานที่คนต้องทำต่อ (หลังใบนี้)
- [ ] BA/พี่เบิร์ด/SEC ตอบ **OQ-DOA** (ยืนยัน role id ขั้น 1 + **เคลียร์ drift ขั้น 2** `role-hr-dev-head` vs `role-hr-ld-head` + CL-0013 slot ผู้บริหาร?)
- [ ] เอาใบนี้ไปตั้งค่า DOA entry จริง (1 entry) ที่หน้า DOA กลาง
- [ ] dev wire hook → `wire_status: pending → wired`
- [ ] เช็คใบ `pending_doa` โผล่ใน My Approval จริง
- [ ] แจ้งพี่เบิร์ดอัพ Google Sheet H·F·Q
