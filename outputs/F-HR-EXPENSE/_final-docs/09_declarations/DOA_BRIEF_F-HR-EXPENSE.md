# DOA_BRIEF — F-HR-EXPENSE (F101 · เบิกค่าใช้จ่าย / Expense Claim)

> **ใบประกาศ DOA** — feature นี้ **ประกาศ**ว่ามีการอนุมัติหน้าตาแบบไหน แล้วคนเอาใบนี้ไป **ตั้งค่าจริงที่หน้า DOA กลาง (F-DLG-001 · Policy Center)**
> feature **ห้าม hardcode สายอนุมัติ/ช่วงวงเงิน** — สาย resolve runtime จาก DOA entry ณ เวลาส่งอนุมัติ ตามยอดรวมใบเบิก แล้ว freeze ลง `approval_chain` (BR-DOA-02 · BR-05 · LD-03)
> **wire_status: `pending`** (ยังไม่ตั้งค่า DOA จริง)

---

## ⚠️ หมายเหตุสำคัญ (อ่านก่อน) — DOA master ไม่มีในการติดตั้งนี้

`.claude/skills/doa-declaration/references/doa-contract.md` **ไม่มีอยู่จริง** ในการติดตั้งชุดนี้ (มีแค่ `SKILL.md` — เหมือนกรณี F-HR-TRAIN / F-HR-RECRUIT)
→ จึง **ยืนยัน `role-*` id กับทะเบียน DOA master ไม่ได้** ทุก role ในใบนี้ติดแท็ก **`[DEFAULT — รอยืนยัน]`**
→ ซ้ำร้าย **HTML mock ใช้ชื่อตำแหน่งไทยล้วน** (`หัวหน้าสายงาน / ผู้จัดการแผนก / ผู้อำนวยการ` — บรรทัด 2199–2201) **ไม่มี `role-*` id เลย** · id ที่เสนอในใบนี้ (`role-line-manager` ฯลฯ) มาจาก DOA_BRIEF ต้นทางของ BA **ในฐานะข้อเสนอ default เท่านั้น ยังไม่ verify**
→ Quality Gate **G1 ตรวจไม่ผ่านเชิงบวก** (verify กับ master ไม่ได้) — ปิดด้วย **OQ-01** ท้ายใบ
→ **CL-0013 (สายอนุมัติผู้บริหาร) แขวนตั้งแต่ 31 ส.ค.** — ถ้ามติเปิด ต้องเพิ่ม slot ระดับผู้บริหารที่ DOA กลาง (ยกเป็น OQ-01 · **ห้ามเดา**)

---

## §1. Identity

| field | value |
|---|---|
| feature_id | **F-HR-EXPENSE** (F101) |
| name | เบิกค่าใช้จ่าย / Expense Claim |
| module | HR (Human Resources) |
| platform | Web (SPA · html-generator-v9 · archetype Q-document) |
| approval_scope | **`document_sign`** — ใบเบิกออกเลข `EXP-<พ.ศ.>-NNNN` + PDF A4 มีช่องลายเซ็น 3 ช่อง + sign tab (FN-23 · BR-06 · S-15) → เซ็นจริงบนเอกสาร |
| จำนวนสายอนุมัติ (Q1) | **1 สาย / 1 action** (อนุมัติใบเบิก) → ใช้ `matrix` เดียว **แต่มีหลายช่วงวงเงิน** (multi-range ในสายเดียว) |
| **มีวงเงินไหม (Q2)** | ✅ **มีวงเงิน** — สายเปลี่ยนตามยอดรวมใบเบิก (`doc_total`) · ยิ่งยอดสูงยิ่งเซ็นหลายชั้น (BR-04 · LOCK-01 · S-08) · **≠ HR ทั่วไปที่ไม่มีวงเงิน** |
| แยกตามแผนก (Q3) | **merged** — ทุกแผนกใช้กฎชุดเดียว (FRD ไม่ระบุ per_dept) |
| กลไก resolve | **FREE independent ranges** — feature ส่ง `doc_total` ให้ DOA กลาง resolve เอง · **ไม่ hardcode 3-tier ตายตัว** (จำนวนช่วง/จุดตัดแก้ได้อิสระที่ DOA กลาง · LOCK-01 · LD-03 · LK-1) |
| DOA engine | F-DLG-001 (Policy Center) · resolve ผ่าน **API-12 `GET /doa/resolve?amount=`** (FN-05 `resolveApprovalChain`) · mock บนจอ = `resolveDoa(total)` + `DOA_RANGES` (บรรทัด 2198–2213) |
| DOA entry ref (บนจอ) | **ไม่มีบนจอ** — HTML mock ไม่ได้ผูก entry-ref (ต่างจาก F-HR-TRAIN) · **ชื่อ key ที่จะตั้งจริงยังไม่กำหนด** → เสนอ `DOA-EXP-CLAIM-001` **`[DEFAULT — proposed key · รอยืนยัน]`** (ของจริงกำหนดตอนสร้าง entry ที่ DOA กลาง · **ห้าม hardcode ในโค้ด feature**) |

---

## §2. Approval Actions (1 action · ผูกวงเงิน)

action เดียว **ผูกวงเงิน (threshold)** — สาย resolve ตามยอดรวม · SoD บังคับ maker ≠ approver (BR-13 · BR-DOA-04 · §5.3 Permission Matrix)

### อนุมัติใบเบิก (Expense Claim · ตามวงเงิน)
| หัวข้อ | รายละเอียด |
|---|---|
| kind | `expense_claim` |
| trigger | ผู้เบิกกด **ส่งอนุมัติ** (`doSubmit` · FN-06 · API-05) จากสถานะ `draft` → resolve สายตามยอดรวม (FN-05) → เปิด slot picker เลือกผู้อนุมัติจริงต่อ slot (มติ 17 ส.ค.) → ครบทุก slot จึงส่งได้ (`submitReady` · `BR_DOA_SLOTS_INCOMPLETE`) → `status='pending_approval'` |
| gate | ส่งได้เมื่อ `grand>0` && line>0 (FN-05) + over-cap มี over_reason ครบ (FN-04) + ใบเสร็จหมวดบังคับครบ (FN-12) · **ไม่มี gate has_cost** — ทุกใบเข้า DOA ตามยอด (ยอดต่ำสุดก็ยังมีอย่างน้อย 1 ขั้น) |
| approve (ครบทุกขั้น) | `pending_approval → approved` · side-effect **ครั้งเดียวตอนจบ chain** (FN-07): ออกเลข `EXP` (FN-11) + snapshot PDF (FN-23) + emit 7C **FC+EC** (FN-22 · ไม่มี AC) + set pay_hook + emit NTF `exp.approved` |
| approve (ยังไม่ครบ) | คง `pending_approval` · toast "อนุมัติขั้น N แล้ว — รอขั้นถัดไป" · `approval_current++` (sequential) |
| reject (ขั้นใดขั้นหนึ่ง) | `pending_approval → rejected` · **บังคับใส่เหตุผล** (BR-18 · `ERR_REASON_REQUIRED` · ปุ่ม disabled จนกรอก) · reopen เฉพาะ `rejected → draft` (FN-10) · ประวัติ append-only (BR-DOA-03) |
| re-resolve (BR-05) | แก้ยอดหลังส่ง/ยื่นใหม่ **ข้ามช่วงวงเงิน** → resolve สายใหม่อัตโนมัติ (FN-05 เรียกซ้ำได้ · resolve ตอน submit · freeze หลังส่ง) |
| enforced by | `doApprove()` / `doReject()` (guard L2442/2476) — เฉพาะ role `canApprove` (`approver:true` · FN-20 · `ERR_NOT_APPROVER` 403) · เจ้าหน้าที่ HR/Finance เห็นทุกใบแต่ **approver:false** (กดอนุมัติไม่ได้) · ผู้เบิก approver:false (กัน self-approve) |

> **หมายเหตุ:** ยอด (`grand`/`doc_total`) เป็น **input ของการ resolve สาย** (ต่างจาก F-HR-TRAIN ที่ยอดเป็น business field เฉย ๆ) · ตัวเงินเป็น **Restricted** (mask ตาม role · FN-18) แต่ยังต้องส่งเข้า DOA เพื่อ resolve

---

## §3. Matrix ที่จะไปตั้งค่าที่ DOA กลาง — **FREE ranges (มีวงเงิน)**

> **1 สาย · หลายช่วงวงเงิน · `chainMode: sequential`** — feature ส่ง `doc_total` ให้ DOA resolve เอง
> **⛔ ตารางข้างล่าง = mock/ตัวอย่าง demo เท่านั้น** (จาก `DOA_RANGES` HTML บรรทัด 2199–2201) — **จำนวนช่วง / จุดตัด / ผู้เซ็น แก้ได้อิสระที่ DOA กลาง · ไม่ผูกกับโค้ด · ห้ามตีความว่าเป็น 3-tier ตายตัว** (LOCK-01 · LD-03)
> ทุก role ติดแท็ก **`[DEFAULT — รอยืนยัน]`** — master ไม่มี + HTML ใช้ชื่อตำแหน่งไทยล้วน (ไม่มี id) → ยืนยันไม่ได้ (ดู OQ-01)

### matrix `expense_claim` — resolve by `doc_total` (บาท)
| # ช่วง (ตัวอย่าง/mock) | amount_from | amount_to | departments | chainMode | steps[roles] |
|---|---|---|---|---|---|
| ex-1 | `0` | `5,000` | `merged` | `sequential` | ① `role-line-manager` **[DEFAULT — รอยืนยัน]** (จอ: "หัวหน้าสายงาน") |
| ex-2 | `5,000` | `50,000` | `merged` | `sequential` | ① `role-line-manager` → ② `role-dept-manager` **[DEFAULT — รอยืนยัน]** (จอ: "ผู้จัดการแผนก") |
| ex-3 | `50,000` | **`null`** (ไม่จำกัด) | `merged` | `sequential` | ① `role-line-manager` → ② `role-dept-manager` → ③ `role-director` **[DEFAULT — รอยืนยัน]** (จอ: "ผู้อำนวยการ") |

> **กลไกที่ประกาศจริง (ที่ dev ต้อง wire) — ไม่ใช่ตัวเลขข้างบน:**
> - feature เรียก `GET /doa/resolve?amount=<doc_total>` (API-12) → DOA กลางคืน `steps[]` ตามช่วงที่ตั้งไว้ → feature เปิด slot picker ให้เลือกคนจริงต่อ slot → freeze `approval_chain`
> - **ช่วงวงเงิน + ผู้เซ็นเป็นข้อมูลใน DOA กลาง ไม่ใช่ logic ใน feature** — เพิ่ม/ลด/แก้ช่วงได้โดยไม่แตะโค้ด F101
> - **CL-0013 (สายผู้บริหาร) แขวน 31 ส.ค.** — ถ้ามติเปิด อาจมีช่วงวงเงินสูง (+ slot ผู้บริหาร) เพิ่มที่ DOA กลาง → **OQ-01** (ห้ามเดาว่ามี/ไม่มี · ห้ามเดา role-id)
> - ตัวเลข 5,000 / 50,000 ในตาราง = **ค่า demo ในบรีฟต้นทาง A-EXP-03** ที่ยัง `[DEFAULT — รอยืนยัน]` — **ไม่ใช่จุดตัดที่เคาะแล้ว**

---

## §4. Field Contract สำหรับ FRD (entity: T_expense_claim + T_expense_approval_step)

field ที่ entity ต้องมี (สอดคล้อง 03_LOGIC FN-05/06/07 · 04_DB · 05_RULES) — **มี field ยอดเงินใน resolve payload** (ต่างจาก feature ไม่มีวงเงิน)

| field | type | null | หมายเหตุ |
|---|---|---|---|
| `doc_total` (grand) | money | NO | **ยอดที่ใช้ resolve สาย** (single source · `totals()`) · **re-resolve เมื่อแก้ข้ามช่วง** (BR-05 · FN-11) — Restricted (mask ตาม role) |
| `approval_required` | bool | NO | มาจาก DOA entry (ทุกใบเข้า DOA ตามยอด) — ไม่ใช่ค่าคงที่ในตาราง |
| `approval_status` | enum | NO | แมป lifecycle: `draft \| pending_approval \| approved \| rejected \| cancelled` (+ ปลายทาง `sent_to_pay/paid/closed` เป็น hook) |
| `doa_entry_ref` | string(40) | YES | FK ทะเบียน DOA (proposed `DOA-EXP-CLAIM-001` · `[DEFAULT — รอยืนยัน]`) · nullable ตอน Phase 1 |
| `doa_range_label` | string | YES | ป้ายช่วงที่ resolve ได้ (เช่น "5,000 – 50,000") · snapshot ตอน submit (จาก `rangeLabel()`) |
| `approver_role` | string | — | role ที่ต้องเซ็นในขั้นปัจจุบัน (resolve จาก DOA slot · **ไม่ hardcode**) |
| `approved_by` / `approver_id` | string (user/EMP id) | YES | ผู้เซ็นจริงต่อ slot (เลือกจาก slot picker · `APPROVERS`) |
| `approval_chain` | jsonb | YES | **snapshot สายที่ resolve ตอนส่ง · append-only** — `[{order, slot_role, approver_id, result, at}]` (child table `T_expense_approval_step`) |
| `doa_resolved_at` / `approved_at` | timestamp | YES | เวลา resolve / เวลาอนุมัติครบทุกขั้น |
| `reject_reason` | text | YES | บังคับตอน reject (BR-18) · append-only |

> **map DB จริง (04_DB):** สายเก็บใน child table `T_expense_approval_step` (order/slot_role/approver_id/result/acted_at) · `doc_total`/`doa_range_label` ฝังใน claim header
> **⛔ ห้าม hardcode สาย/ช่วงใน FRD/BR:** ไม่เขียน "ถ้าเกิน 50,000 ให้ ผอ.เซ็น" ลงใน feature — นั่นเป็นข้อมูลใน DOA · เขียนแทนว่า *"resolve จาก DOA entry ตอนส่งอนุมัติ ตาม `doc_total` แล้ว snapshot ลง `approval_chain`"*

---

## §5. UI Contract สำหรับ HTML (อ้าง `outputs/F-HR-EXPENSE/expense.html` ที่มีอยู่จริง)

พฤติกรรมที่หน้าจอ **มีแล้ว** และเป็นสัญญากับ dev (อ้าง function/บรรทัดจริง):

| ส่วน | ในไฟล์ปัจจุบัน |
|---|---|
| **resolve ตามวงเงิน** | `resolveDoa(total)` (L2213) หา range จาก `DOA_RANGES` (L2198) ตาม `total>=min && total<max` · เรียกซ้ำได้ → รองรับ re-resolve (BR-05) · comment ล็อกไว้ว่า **mock · ตั้งค่าจริงที่ DOA กลาง · ห้าม hardcode** (L2194–2197) |
| **Slot picker (DOA)** | modal "ส่งอนุมัติ — เลือกผู้อนุมัติแต่ละ slot" (L2411) — แสดงยอด + ช่วงที่ resolve ("**ตัวอย่าง/mock — ตั้งค่าจริงที่ DOA กลาง**") · `.slot-row`/`.slot-no` + `searchSelectHTML('slot-'+i)` เลือกคนจริงต่อ slot จาก `APPROVERS` (L2204) · **ไม่ prefill คนให้เอง** (L2493) |
| **ปุ่ม ส่งอนุมัติ** | `doSubmit` → resolve → modal → `submitReady()` (L2472) เช็คทุก slot มีผู้อนุมัติจริง · **ปุ่มส่ง disabled จนครบ** (UX-06 · `onSlotPickChange` L2473) → `BR_DOA_SLOTS_INCOMPLETE` |
| **ปุ่ม อนุมัติ / ไม่อนุมัติ** | `doApprove()` / `doReject()` (guard L2442/2476) แสดงเฉพาะ `canApprove` · **ไม่อนุมัติ = บังคับเหตุผล** (BR-18) · busy guard กัน double-submit (EC-03) |
| **Badge สถานะ** | pill lifecycle 8 state (L2182) — `draft / pending_approval(รออนุมัติ) / approved / rejected / cancelled / paid` · CI Warm Light |
| **Approval Timeline** | tab "ลายเซ็น/อนุมัติ" — ไล่ทีละขั้น: slot_role → ผู้เซ็น → ผล (รอ/อนุมัติ+วันที่/ตีกลับ) · sequential |
| **PDF + sign** | tab "PDF Preview (a4)" + ช่องลายเซ็น 3 ช่อง (FN-23 · document_sign) |
| **Hook My Approval** | ใบ `pending_approval` โผล่กล่องงานรออนุมัติ (นับ status==='pending_approval') |

**ข้อห้าม (คงไว้):** ห้าม `const APPROVAL_CHAIN = [...]` ในไฟล์ feature · ปัจจุบันใช้ `DOA_RANGES` + `resolveDoa()` **mock พร้อม comment ล็อก** (L2194–2197 `[มติ PM/BA · LK-1] FREE ranges · ไม่ hardcode`) · เพราะ **มีวงเงิน** mock จึงมี **3 ช่วงตัวอย่าง** (ให้เห็นว่าสายเปลี่ยนตามเงินจริง) — **ตัวอย่าง ไม่ใช่ contract**

---

## §6. Wire Checklist (dev · จน `wire_status: pending → wired`)

- [ ] สร้าง DOA entry จริงที่หน้า DOA กลาง — **matrix เดียว หลายช่วงวงเงิน (FREE ranges)** · กำหนดชื่อ key จริง (proposed `DOA-EXP-CLAIM-001`)
- [ ] **เคาะช่วงวงเงินจริง** (จำนวนช่วง + จุดตัด) — ค่า 5k/50k ปัจจุบันเป็น demo `[DEFAULT]` (OQ-01 · A-EXP-03)
- [ ] **ยืนยัน `role-*` id ทุกขั้นกับ DOA master** — `role-line-manager` / `role-dept-manager` / `role-director` ปัจจุบัน `[DEFAULT]` (จอใช้ชื่อไทยล้วน ยังไม่มี id) · รอ **OQ-01**
- [ ] **เคลียร์ CL-0013 (สายผู้บริหาร แขวน 31 ส.ค.)** — เพิ่มช่วง/slot ผู้บริหารหรือไม่ (OQ-01)
- [ ] wire `FN-05` → `GET /doa/resolve?amount=` (API-12) แทน mock `resolveDoa()` — ส่ง `doc_total`
- [ ] **re-resolve เมื่อแก้ยอดข้ามช่วง** (BR-05 · FN-11) · resolve ตอน submit แล้ว **snapshot freeze** ลง `approval_chain` (BR-DOA-02)
- [ ] SoD: maker ≠ approver (BR-DOA-04 · BR-13 · `ERR_NOT_APPROVER`) · เจ้าหน้าที่ HR/Finance `approver:false`
- [ ] reject → `rejected` + เหตุผล append-only (BR-DOA-03 · BR-18) · reopen เฉพาะ rejected
- [ ] ใบ `pending_approval` โผล่ใน My Approval จริง
- [ ] toggle `wire_status: pending → wired` + อัปเดต `FEATURE_REGISTRY.md`

---

## §7. Open Questions

### 🔴 OQ-01 (= A-EXP-03) — ช่วงวงเงินจริง + role-id + CL-0013 แขวน
- **owner:** **พี่เบิร์ด / BA / SEC** + DOA declaration
- **ref:** DOA_BRIEF ต้นทาง (Pack §3 · §7 A-EXP-03) · FRD 05_RULES BR-04 · 07_LOCKED LOCK-01/LD-03 · 00_OVERVIEW §0.8 OQ-01 · 03_LOGIC FN-05 OQ-01
- **คำถาม (ทั้งหมดห้ามเดา — เดาผิดมีคนเอาไปตั้งค่าจริง):**
  1. **ช่วงวงเงินจริง (FREE ranges):** จำนวนช่วง + จุดตัดเท่าไร? — ค่า `0–5,000 / 5,000–50,000 / 50,000+` ปัจจุบันเป็น **demo `[DEFAULT — รอยืนยัน]`** ไม่ใช่จุดตัดที่เคาะแล้ว
  2. **role-id แต่ละขั้น:** ยืนยัน `role-line-manager` / `role-dept-manager` / `role-director` (หรือ id จริงอื่น) กับ **DOA master** — ปัจจุบัน `[DEFAULT]` เพราะ **master `references/doa-contract.md` ไม่มีในการติดตั้งนี้** + **HTML mock ใช้ชื่อตำแหน่งไทยล้วน (ไม่มี id)**
  3. **🔴 CL-0013 (สายอนุมัติผู้บริหาร) แขวนตั้งแต่ 31 ส.ค.** — ต้องเพิ่มช่วงวงเงินสูง + slot ระดับผู้บริหารหรือไม่? ถ้าเปิด ตั้งเพิ่มที่ DOA กลาง (สาย resolve runtime · feature ไม่แก้โค้ด)
  4. **ชื่อ DOA entry key จริง** — เสนอ `DOA-EXP-CLAIM-001` (`[DEFAULT — proposed]`) · ยืนยันชื่อจริงตอนสร้าง entry
- **บล็อกอะไร:** **ไม่บล็อก HTML/FRD** (สาย resolve runtime · declaration เท่านั้น) แต่ **บล็อกการตั้งค่า DOA จริง + CL-0013 เป็น blocker** (dev ต้องได้ช่วง + role-id ยืนยัน + มติ CL-0013 ก่อน wire)

### OQ อื่นที่เกี่ยวข้อง (context · owner เดิม · ไม่กระทบ matrix DOA โดยตรง)
- **OQ-04** (RBAC · SEC/BA) — mapping role→login จริง + "ธุรการสร้างแทนผู้เบิก" · กระทบว่า persona ไหน `canApprove`
- **OQ-05** (BA/Finance) — reverse-EC / release-FC เมื่อยกเลิก/แก้ **หลังอนุมัติ** — ปัจจุบัน cancel เฉพาะ draft · reopen เฉพาะ rejected → **path ยกเลิกหลังอนุมัติ ยังไม่มี** · ไม่กระทบสาย DOA แต่กระทบ 7C
- **OQ-EXP-02** — 7C = FC/EC เท่านั้น (ไม่มี AC) · ล็อกแล้ว (LOCK-04) · ไม่กระทบสาย DOA

---

## ✅ Quality Gate (G1–G7)

| # | เช็ค | ผล |
|---|---|---|
| **G1** | ทุก role เป็น `role-*` ที่มีใน master | **⚠️ ยืนยันเชิงบวกไม่ได้** — `references/doa-contract.md` ไม่มีในการติดตั้งนี้ + HTML mock ใช้ชื่อไทยล้วน (ไม่มี id) · ทุก role ติด `[DEFAULT — รอยืนยัน]` → ยก **OQ-01** (ไม่แต่ง id ใหม่นอกจากที่ BA เสนอเป็น default) |
| **G2** | ทุก set มี `amount_from` + `amount_to` | ✅ ครบทุกช่วงตัวอย่าง (`0`/`5,000` · `5,000`/`50,000` · `50,000`/`null`) |
| **G3** | ถ้ามีวงเงิน — ช่วงต่อเนื่องไม่ทับ ไม่มีรู | ✅ ตัวอย่างต่อเนื่อง (`max` ช่วงก่อน = `min` ช่วงถัด · resolve ใช้ `total>=min && total<max` กันทับ) · **แต่ค่าเป็น demo — จุดตัดจริงรอ OQ-01** |
| **G4** | set สุดท้าย `amount_to: null` | ✅ ช่วงสูงสุด `amount_to: null` (Infinity บนจอ) — ใบเกินเพดานมีคนเซ็นเสมอ |
| **G5** | `approval_scope` เป็น 1 ใน 3 ค่าจริง | ✅ `document_sign` (ออก PDF + ช่องลายเซ็น + sign tab) |
| **G6** | ค่าที่ยังไม่ยืนยันติด `[DEFAULT — รอยืนยัน]` | ✅ ครบทุก role §3 · ทุกจุดตัดวงเงิน (demo) · DOA entry key · CL-0013 |
| **G7** | ไม่มีสายอนุมัติ hardcode ใน FRD/HTML | ✅ HTML ใช้ `DOA_RANGES`+`resolveDoa()` **mock** (comment `[LK-1] FREE ranges · ไม่ hardcode` L2194–2197) · ไม่มี `const APPROVAL_CHAIN` · FRD FN-05 resolve runtime ผ่าน API-12 (LD-03) |

**สรุป:** G2–G7 ผ่าน · **G1 ยืนยันเชิงบวกไม่ได้เพราะ master หาย + จอไม่มี role-id → ปิดด้วย OQ-01 + แท็ก `[DEFAULT — รอยืนยัน]` ทุก role/ช่วง** (ไม่เคลมว่า G1 ผ่าน)

---

## 📌 งานที่คนต้องทำต่อ (หลังใบนี้)
- [ ] BA/พี่เบิร์ด/SEC ตอบ **OQ-01** (ช่วงวงเงินจริง + ยืนยัน role-id ทุกขั้น + **เคลียร์ CL-0013 slot ผู้บริหาร** + ชื่อ entry key)
- [ ] เอาใบนี้ไปตั้งค่า DOA entry จริง (matrix เดียว หลายช่วงวงเงิน) ที่หน้า DOA กลาง
- [ ] dev wire `FN-05` → `GET /doa/resolve` · re-resolve ข้ามช่วง (BR-05) · toggle `wire_status: pending → wired`
- [ ] เช็คใบ `pending_approval` โผล่ใน My Approval จริง
- [ ] แจ้งพี่เบิร์ดอัพ Google Sheet H·F·Q
