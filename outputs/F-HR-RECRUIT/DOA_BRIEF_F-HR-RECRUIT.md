# DOA_BRIEF — F-HR-RECRUIT (F127 · สรรหา / Recruit)

> **ใบประกาศ DOA** — feature นี้ **ประกาศ**ว่ามีการอนุมัติหน้าตาแบบไหน แล้วคนเอาใบนี้ไป **ตั้งค่าจริงที่หน้า DOA กลาง (F-DLG-001 · Policy Center)**
> feature **ห้าม hardcode สายอนุมัติ** — สาย resolve runtime จาก DOA entry ณ เวลาส่งอนุมัติ แล้ว freeze ลง `approval_chain` (VR-04 · BR-DOA-02)
> **wire_status: `pending`** (ยังไม่ตั้งค่า DOA จริง)

---

## ⚠️ หมายเหตุสำคัญ (อ่านก่อน) — DOA master ไม่มีในการติดตั้งนี้

`.claude/skills/doa-declaration/references/doa-contract.md` **ไม่มีอยู่จริง** ในการติดตั้งชุดนี้
→ จึง **ยืนยัน `role-*` id กับทะเบียน DOA master ไม่ได้** ทุก role ในใบนี้ติดแท็ก `[DEFAULT — รอยืนยัน]`
→ Quality Gate **G1 ตรวจไม่ผ่านเชิงบวก** (verify กับ master ไม่ได้) — ดู §Quality Gate + **OQ-DOA** ท้ายใบ

---

## §1. Identity

| field | value |
|---|---|
| feature_id | **F-HR-RECRUIT** (F127) |
| name | สรรหา / Recruit |
| module | HR (Human Resources) |
| platform | Web (SPA · html-generator-v9) |
| approval_scope | **`policy_approve`** — อนุมัติเชิงนโยบาย/สิทธิ์ HR (การจ้างงาน) · **ไม่ใช่** `document_sign` (ไม่มีเอกสารพิมพ์ที่ต้องเซ็นลายเซ็นในกล่อง PDF ในรอบนี้) |
| จำนวนสายอนุมัติ (Q1) | **หลายสาย** → ใช้ `actions[]` 2 ชุด (requisition · offer) |
| มีวงเงินไหม (Q2) | **ไม่มีวงเงิน** — อนุมัติตามระดับตำแหน่ง ไม่ผูก threshold ยอดเงิน (ทั้ง 2 action) |
| แยกตามแผนก (Q3) | **merged** — ทุกแผนกใช้กฎชุดเดียว |
| DOA engine | F-DLG-001 (Policy Center) · resolve ผ่าน `F127-FN-26 resolveDoaChain` (external read · EXT-DOA) |

---

## §2. Approval Actions (2 action)

ทั้ง 2 action **ไม่ผูกวงเงิน** — เป็น role-based ตามระดับตำแหน่ง · SoD บังคับ maker ≠ approver (BR-DOA-04 · §5.2)

### (a) อนุมัติเปิดอัตรา — Requisition
| หัวข้อ | รายละเอียด |
|---|---|
| kind | `req` |
| trigger | requisition `draft → pending` (กด **ส่งอนุมัติเปิด**) — resolve DOA slot chain ผ่าน `F127-FN-03 submitRequisitionApproval` → `FN-26` |
| approve (ครบทุก slot) | status `pending → approved` → พร้อม **ประกาศ** (`FN-06 announceRequisition` → `open`) · BR-01 |
| reject (slot ใด slot หนึ่ง) | ย้อน `pending → draft` · **บังคับใส่เหตุผล** · เก็บประวัติ append-only (BR-DOA-03) |
| enforced by | `F127-FN-04 approveApprovalStep(entity='req')` · error `BR_REQ_NOT_APPROVED` (422) · `ERR_NOT_IN_SLOT` (403 · SoD) |

### (b) อนุมัติข้อเสนอจ้าง — Offer
| หัวข้อ | รายละเอียด |
|---|---|
| kind | `offer` |
| trigger | offer `pending` (หลัง `FN-15 createOffer`) — กด **ส่งอนุมัติ** → `F127-FN-16 submitOfferApproval` → `FN-26` |
| approve (ครบทุก slot) | status `pending → approved` → **ส่งข้อเสนอ**ให้ผู้สมัครได้ (`FN-18a sendOffer` → `sent`) · BR-04 |
| reject | ย้อน `pending` · บังคับเหตุผล · append-only |
| enforced by | `F127-FN-17 approveApprovalStep(entity='offer')` · error `BR_OFFER_NOT_APPROVED` (422) |
| หมายเหตุเงินเดือน | `offer.salary` อ้าง **band แบบ soft-ref** (freeze `band_version_id` · BR-09) — **ไม่ใช่** amount tier ของ DOA · การอนุมัติ **ไม่เปลี่ยนตามยอดเงิน** |

---

## §3. Matrix ที่จะไปตั้งค่าที่ DOA กลาง

> ทั้ง 2 ชุด: `amount_from: 0 · amount_to: null` (ไม่มีวงเงิน · ปิดปลายเปิด = ทุกยอดใช้สายเดียวกัน) · `chainMode: sequential`
> ทุก role ติดแท็ก **`[DEFAULT — รอยืนยัน]`** — master ไม่มีในการติดตั้งนี้ ยืนยันไม่ได้ (ดู OQ-DOA)

**actions[] = 2 sets**

### set 1 — `requisition` (อนุมัติเปิดอัตรา)
| field | value |
|---|---|
| amount_from | `0` (บาท) |
| amount_to | `null` (ไม่จำกัด — ไม่มีวงเงิน) |
| departments | `merged` (ทุกแผนก) |
| chainMode | `sequential` |
| steps[roles] | ① `role-hiring-manager` **[DEFAULT — รอยืนยัน]** — ผู้จัดการสายงาน (Hiring Manager) → ② `role-hr-recruit-head` **[DEFAULT — รอยืนยัน]** — หัวหน้าฝ่ายสรรหา |

### set 2 — `offer` (อนุมัติข้อเสนอจ้าง)
| field | value |
|---|---|
| amount_from | `0` (บาท) |
| amount_to | `null` (ไม่จำกัด — เงินเดือนอ้าง band soft-ref เท่านั้น ไม่ผูก threshold) |
| departments | `merged` |
| chainMode | `sequential` |
| steps[roles] | ① `role-hiring-manager` **[DEFAULT — รอยืนยัน]** → ② `role-hr-recruit-head` **[DEFAULT — รอยืนยัน]** |

> **หมายเหตุ:** ระดับสูง (ผู้บริหาร/exec) **อาจ**เพิ่ม slot ที่ 3 — ตั้งเพิ่มที่ DOA กลางได้เมื่อ BA ยืนยัน (OQ-DOA) · feature ไม่ต้องแก้โค้ด (สาย resolve runtime)
> **ไม่มีคอลัมน์วงเงิน/tier** ในตารางนี้โดยเจตนา — feature นี้ไม่มีวงเงิน (ต่างจาก PR/PO)

---

## §4. Field Contract สำหรับ FRD (entity: requisition + offer)

field ที่ entity ต้องมี (สอดคล้อง 04_DB §4.2 · FRD Injection §Entity) — **ไม่มี field ยอดเงินใน `doa_resolve_payload`**

| field | type | null | หมายเหตุ |
|---|---|---|---|
| `approval_required` | bool | NO | มาจาก DOA entry ของ feature (ไม่ใช่ค่าคงที่ในตาราง) |
| `approval_status` | enum | YES | `draft \| pending_approval \| approved \| rejected \| cancelled` |
| `doa_entry_ref` | string(40) | YES | FK ไปทะเบียน DOA (nullable ตอน Phase 1 · resolve ตอนส่ง) |
| `approver_role` | string | — | role ที่ต้องเซ็นในขั้นปัจจุบัน (resolve จาก DOA slot · ไม่ hardcode) |
| `approved_by` | string (user id) | YES | user ที่เซ็นจริงในแต่ละ slot |
| `approval_chain` | jsonb | YES | **snapshot ของสายที่ resolve ตอนส่งอนุมัติ · append-only** — `[{order, slot, slotName, approver_role, approver_id?, decided_at?, result?}]` |
| `approved_at` | timestamp | YES | เวลาอนุมัติครบทุก slot |

> **⛔ ไม่มี field ยอดเงินใน `doa_resolve_payload`** — offer ไม่ผูก threshold · `offer.salary` เป็น business field (Confidential · band soft-ref) ไม่ใช่ input ของการ resolve สาย DOA
> map กับ DB จริง (04_DB): `requisition/offer.status` (state), `.approval_status`, `.doa_entry_ref`, `.approval_chain` มีครบแล้วในสองตาราง

---

## §5. UI Contract สำหรับ HTML (อ้าง `outputs/F-HR-RECRUIT/สรรหา.html` ที่มีอยู่จริง)

พฤติกรรมที่หน้าจอ **มีแล้ว** และเป็นสัญญากับ dev (อ้าง selector/ฟังก์ชันจริงในไฟล์):

| ส่วน | ในไฟล์ปัจจุบัน |
|---|---|
| **Slot picker (DOA)** | `.slot` / `.slot-h` (avatar + ชื่อ slot + role id monospace) — mock resolved chain `resolveDoaChain(kind)` (บรรทัด ~2161) คืน 2 slot: `role-hiring-manager` → `role-hr-recruit-head` · **ไม่มีวงเงิน · 1 ชั้น (single tier)** |
| **ปุ่ม ส่งอนุมัติ** | req: `reqSubmitApproval()` ปุ่ม "ส่งอนุมัติเปิด" แสดงเฉพาะ status `draft` · offer: ส่งอนุมัติหลัง createOffer |
| **ปุ่ม อนุมัติ / ไม่อนุมัติ** | `reqApprove()` / `reqReject()` แสดงเฉพาะ persona ที่ `canApprove` และอยู่ใน slot ปัจจุบัน · **ไม่อนุมัติ = บังคับเหตุผล** |
| **Badge สถานะ** | `pill-warning` (รออนุมัติ) · `pill-info` (อนุมัติแล้ว · รอประกาศ/พร้อมส่ง) · `pill-success` (อนุมัติแล้ว/เสร็จ) — CI Warm Light |
| **Approval Timeline** | `approvalSection(ap,label)` + `.timeline` — ไล่ทีละ slot: slotName → ผู้เซ็น → เวลา → ผล (รอ/ผ่าน/ตีกลับ) · แสดง DOA entry + "ขั้น N/M" |
| **Hook My Approval** | `approvalHook` (บรรทัด ~2341) — ใบสถานะ `รออนุมัติเปิด` โผล่กล่อง "งานรออนุมัติของฉัน · N รายการ" |

**ข้อห้าม (คงไว้):** ห้าม `const APPROVAL_CHAIN = [...]` ในไฟล์ feature · ใช้ `resolveDoaChain()` mock (`// TODO: DOA engine`) · mock **1 tier** พอ (ไม่มีวงเงิน — ไม่ต้อง 2 tier)

---

## §6. Wire Checklist (dev · จน `wire_status: pending → wired`)

- [ ] สร้าง DOA entry จริงที่หน้า DOA กลาง — **2 entry**: `requisition` + `offer` (ทั้งคู่ merged · ไม่มีวงเงิน · sequential 2 slot)
- [ ] ยืนยัน `role-*` id กับ DOA master (role-hiring-manager · role-hr-recruit-head) — **ปัจจุบัน [DEFAULT] · รอ OQ-DOA**
- [ ] wire `F127-FN-26 resolveDoaChain('req'|'offer')` → Policy Center (EXT-DOA) แทน mock
- [ ] resolve สายตอนกดส่งอนุมัติ แล้ว **snapshot freeze** ลง `approval_chain` (BR-DOA-02 · VR-04)
- [ ] SoD: maker ≠ approver บังคับที่ `FN-04` (`ERR_NOT_IN_SLOT`)
- [ ] reject → ย้อน draft/pending + เหตุผล append-only (BR-DOA-03)
- [ ] ใบ `pending_approval` โผล่ใน My Approval จริง
- [ ] toggle `wire_status: pending → wired` + อัปเดต `FEATURE_REGISTRY.md`

---

## §7. Open Questions

### 🔴 OQ-DOA — ยืนยัน role id + slot กับ DOA master
- **owner:** พี่เบิร์ด / BA
- **ref:** **A-REC-02** (PREBRIEF §10 · §12 · seed DOA_BRIEF)
- **คำถาม:**
  1. ยืนยัน `role-*` id ทั้ง 2 slot ของ **ทั้ง 2 action** — `role-hiring-manager` (ผู้จัดการสายงาน) · `role-hr-recruit-head` (หัวหน้าฝ่ายสรรหา) — **ตรงกับทะเบียน DOA master หรือไม่** (id ปัจจุบันเป็น `[DEFAULT — รอยืนยัน]` เพราะ **master `references/doa-contract.md` ไม่มีในการติดตั้งชุดนี้ → ยืนยันเองไม่ได้**)
  2. การอนุมัติระดับสูง (ผู้บริหาร/exec) **ต้องเพิ่ม slot ที่ 3 หรือไม่** สำหรับ requisition และ/หรือ offer (เช่นตำแหน่งระดับสูง/เงินเดือนเกินเกณฑ์นโยบาย) — ถ้าใช่ ตั้งเพิ่มที่ DOA กลาง
  3. offer/requisition ใช้สาย**เดียวกัน**หรือแยกกัน (ปัจจุบันเสนอ 2 entry สายเหมือนกัน)
- **บล็อกอะไร:** ไม่บล็อก HTML/FRD (สาย resolve runtime · declaration เท่านั้น) แต่ **บล็อกการตั้งค่า DOA จริง** (dev ต้องได้ id ยืนยันก่อน wire — เดาผิดมีคนเอาไปตั้งค่าจริง)

### OQ อื่นที่เกี่ยวข้อง (ยกมาเพื่อ context · owner เดิม)
- **A-REC-01** — เปิดอัตราไม่มี Manpower = hook (ไม่บล็อก · BR-08) · ไม่กระทบ DOA
- **A-REC-03** — handoff On/Offboard = event (OQ-15) · ไม่กระทบ DOA
- **A-REC-04 / OQ-16** — PDPA consent + retention · ไม่กระทบ DOA

---

## ✅ Quality Gate (G1–G7)

| # | เช็ค | ผล |
|---|---|---|
| **G1** | ทุก role เป็น `role-*` ที่มีใน master | **⚠️ ยืนยันเชิงบวกไม่ได้** — `references/doa-contract.md` ไม่มีในการติดตั้งนี้ · ทุก role จึงติด `[DEFAULT — รอยืนยัน]` + ยก **OQ-DOA** (ไม่แต่ง id อื่นเกิน 2 ตัวจาก seed/HTML) |
| **G2** | ทุก set มี `amount_from` + `amount_to` | ✅ ครบทั้ง 2 set (`0` / `null`) |
| **G3** | ถ้ามีวงเงิน — ช่วงต่อเนื่องไม่ทับ | **N/A** — ไม่มีวงเงิน (1 set/action ครอบทุกยอด) |
| **G4** | set สุดท้าย `amount_to: null` | ✅ ทั้ง 2 set `amount_to: null` |
| **G5** | `approval_scope` เป็น 1 ใน 3 ค่าจริง | ✅ `policy_approve` |
| **G6** | ค่าที่ยังไม่ยืนยันติด `[DEFAULT — รอยืนยัน]` | ✅ ครบทุก role ทั้ง §3 · §6 · OQ-DOA |
| **G7** | ไม่มีสายอนุมัติ hardcode ใน FRD/HTML | ✅ HTML ใช้ `resolveDoaChain()` mock (`// TODO: DOA engine`) · FRD `FN-26` resolve runtime (VR-04) — ไม่มี array role ในไฟล์ feature |

**สรุป:** G2–G7 ผ่าน · **G1 ยืนยันเชิงบวกไม่ได้เพราะ master หาย → ปิดด้วย OQ-DOA + แท็ก [DEFAULT — รอยืนยัน] ทุก role** (ไม่เคลมว่า G1 ผ่าน)

---

## 📌 งานที่คนต้องทำต่อ (หลังใบนี้)
- [ ] BA/พี่เบิร์ด ตอบ **OQ-DOA** (ยืนยัน role id + slot 3 exec?)
- [ ] เอาใบนี้ไปตั้งค่า DOA entry จริง (2 entry) ที่หน้า DOA กลาง
- [ ] dev wire hook → `wire_status: pending → wired`
- [ ] เช็คใบโผล่ใน My Approval จริง
