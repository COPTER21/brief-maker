# DOA_BRIEF — F-HR-OT · OT / Shift (โอที)

> ออกโดย `doa-declaration` v1.0 · **Lane Mode (no-ask)** · S1.8 · 2026-08-29
> Input: `briefs/W2/F-HR-OT/PREBRIEF.md` v1.1 §12 (สัญญาณประกาศ · **authoritative**) + §5 state machine + §4 BR · `LANE_BRIEF.md` (chip) · `_lane/DECL.json`
> **DIVERGENCE: —** (chip `doa ✓` = detect §12 = ตาราง `CONTEXT_PACK/HR.md` แถว OT / Shift → ✓ **"เกินเพดาน = สายยาว"**)
> หมายเหตุ: `references/doa-contract.md` และ `references/brief-template.md` **ไม่มีในเวิร์กสเปซนี้** — ยึด contract จาก SKILL.md (Iron Rule · Quality Gate G1–G7) + `cube-4.0-current-state.md` §3 + `feature-catalog-master.md` §0 · **`role-*` id ทุกตัวจึงติด `[DEFAULT — รอยืนยัน]`** (ต้อง cross-check กับ master 14 roles ที่ Policy Center ก่อน set จริง)
> **feature ประกาศเท่านั้น — ห้าม hardcode สายอนุมัติ** (DOA iron rule · `GET /doa/resolve`) · **hardcode = governance Hard Stop**

## §1 Identity

| | |
|---|---|
| feature_id | `F-HR-OT` |
| feature name | OT / Shift · โอที (ใบขอทำงานล่วงเวลา) |
| module | HR |
| platform | Core ERP (core.2bsimple.com) |
| archetype | Q-document |
| **approval_scope** | **`document_sign`** — ใบ OT พิมพ์ออกมาได้และมีช่องลายเซ็น (3 ช่องปกติ · **4 ช่องเมื่อเกินเพดาน**) ตรงกับ `PDFDOC/template.html` |
| **มีวงเงิน (เงิน)?** | **❌ ไม่มีวงเงินเป็นเงินเลย** — feature นี้ **ห้ามมีตัวเลขเงินทุกชนิด** (PREBRIEF **BR-18** · scope note "ไม่คิดเงิน OT — Payroll คิด") → ทุก set ใช้ `amount_from: 0` · `amount_to: null` |
| **มีจุดตัด (threshold) ไหม?** | **✅ มี — และนี่คือสิ่งที่ต่างจาก Leave** · จุดตัดคือ **"ชั่วโมงสะสมในสัปดาห์เกินเพดาน OT หรือไม่"** (`over_cap`) — **ไม่ใช่จำนวนเงิน และไม่ใช่ตัวเลขที่เขียนตายไว้** |
| จำนวนสายอนุมัติ | **2 สาย** (`matrix` 2 ชุด ผูกกับ 2 action) — **ในเพดาน 2 ขั้น** · **เกินเพดาน 3 ขั้น** |
| chainMode | **`sequential`** ทั้งสองสาย — เซ็นไล่ทีละขั้น (PREBRIEF §5 T-3) |
| departments | **`merged`** — ทุกแผนกใช้กฎชุดเดียวกัน (ไม่มีสัญญาณแยกแผนกใน scope note) |
| version | 1.0 (2026-08-29) · `wire_status: pending` |

## §2 Approval Actions

| # | action_id | ชื่อ | trigger (PREBRIEF) | ผลเมื่อ **approve** | ผลเมื่อ **reject** |
|---|---|---|---|---|---|
| **A-1** | `ot_approve_within_cap` | **อนุมัติใบขอ OT (อยู่ในเพดาน)** | §5 T-2 `ร่าง → รออนุมัติ` เมื่อ **`over_cap = false`** (S-01 · FN-25 · FN-27) แล้วไล่ slot จนถึง T-4 `รออนุมัติ → อนุมัติแล้ว` | ใบเป็น **"อนุมัติแล้ว"** · ตั้ง `hours_approved_total` (อาจน้อยกว่าที่ขอ — A-4) · **render ใบ OT PDF + เก็บสำเนา `approved_final`** · เปิดทางให้ยืนยันเวลาจริง (T-8) | ใบเป็น **"ไม่อนุมัติ"** · **บังคับ `reject_reason`** (BR-12 · FN-30) · **เลขที่คงอยู่ ไม่ reuse** (BR-13) |
| **A-2** ⭐ | `ot_approve_over_cap` | **อนุมัติใบขอ OT (เกินเพดาน)** | §5 T-2 เมื่อ **`over_cap = true`** (S-06 · S-11 · FN-15 · FN-28) | เหมือน A-1 แต่ต้องผ่าน **3 ขั้น** ครบก่อน · tab ลายเซ็นต้องเห็นครบ 3 ชั้น (FN-32) · PDF มีช่องเซ็นช่องที่ 4 (FN-37) | เหมือน A-1 |
| **A-3** | `ot_confirm_actual_hours` | **ยืนยันเวลาจริง** | §5 T-8 `อนุมัติแล้ว → ยืนยันเวลาจริงแล้ว` (S-16 · FN-21) | ใบเป็น **"ยืนยันเวลาจริงแล้ว"** · ตั้ง `hours_confirmed_total` · **เริ่มเผยแพร่ให้ Payroll/ESS อ่าน** (BR-17) | ใบคงสถานะ "อนุมัติแล้ว" · บันทึกเหตุที่ยืนยันไม่ได้ในประวัติ |
| **A-4** | `ot_approve_partial` | **อนุมัติบางส่วน** | §5 T-4 เมื่อผู้อนุมัติรับรองชั่วโมงน้อยกว่าที่ขอ (S-17 · FN-31) | ใบเป็น "อนุมัติแล้ว" ด้วย `hours_approved_total < hours_requested_total` · **บังคับ `partial_reason`** (BR-21) | เหมือน A-1 reject |
| **A-5** | `ot_approve_withdrawal` | **อนุมัติการถอนใบที่อนุมัติ/ยืนยันแล้ว** `[ASSUMED · OQ-OT-11]` | §5 T-9 `อนุมัติแล้ว / ยืนยันเวลาจริงแล้ว → ถอน` (S-14 · FN-41) | ใบเป็น **"ถอน"** · เกิด **รายการกลับ (`reversal_of`)** ที่ชี้ของเดิม · **ใบเดิม ประวัติเดิม และสำเนา PDF เดิมไม่ถูกลบไม่ถูกแก้** (BR-27) | ใบคงสถานะเดิม · บันทึกการปฏิเสธคำขอถอนในประวัติ |
| **A-6** | `ot_approve_resubmit` | **อนุมัติใบที่แก้แล้วส่งใหม่** | §5 T-7 (S-15 · FN-33) | งานอนุมัติเดิมถูกยกเลิก → **`resolve` สายใหม่** · **ชั้นของสายเปลี่ยนได้ถ้าชั่วโมงข้าม/ต่ำกว่าเพดาน** · **เลขที่เดิมคงอยู่** | เหมือน A-1 reject |

> **A-3…A-6 ใช้ matrix ของ A-1 หรือ A-2 ตามค่า `over_cap` ณ เวลาที่ resolve** — ไม่มี matrix ของตัวเอง

## §3 Matrix ที่จะไปตั้งค่า (กรอกลงหน้า DOA กลางได้ตรงช่อง)

| set | ผูกกับ action | amount_from | amount_to | departments | chainMode | steps[roles] |
|---|---|---|---|---|---|---|
| **1** | `ot_approve_within_cap` | `0` บาท | `null` (ไม่จำกัด) | `merged` | `sequential` | **step 1:** `role-supervisor-direct` `[DEFAULT — รอยืนยัน]` — หัวหน้าโดยตรงของผู้ขอ · **step 2:** `role-mgr-hr` `[DEFAULT — รอยืนยัน]` — ผู้จัดการฝ่ายบุคคล |
| **2** ⭐ | `ot_approve_over_cap` | `0` บาท | `null` (ไม่จำกัด) | `merged` | `sequential` | **step 1:** `role-supervisor-direct` `[DEFAULT — รอยืนยัน]` · **step 2:** `role-mgr-hr` `[DEFAULT — รอยืนยัน]` · **step 3:** `role-exec-dept` `[DEFAULT — รอยืนยัน]` — ผู้บริหาร/ผู้จัดการฝ่ายต้นสังกัดของผู้ขอ |

- **`amount_to: null` ในชุดสุดท้ายของทั้งสอง set ✅ (G4)** — ไม่มีใบไหนตกขอบไม่มีคนเซ็น
- **ไม่มีรู/ไม่ทับ ✅ (G3)** — แต่ละ action มีชุดเดียวที่ครอบ `0 → ไม่จำกัด`
- **หน่วยเงิน:** บาท — แต่ feature นี้ **ไม่ส่งค่าเงินเข้า resolve เลย** (BR-18) · ช่อง amount มีไว้ให้ record ถูก schema ของ DOA เท่านั้น

### §3.1 ⭐ ทำไมจุดตัดถึงเป็น **action** ไม่ใช่ตัวเลขในช่วง `amount` (ข้อสำคัญที่สุดของใบนี้)

จุดตัดของ feature นี้คือ **"ชั่วโมงสะสมในสัปดาห์เกิน `ot_rate.cap_hours_week` หรือไม่"** ซึ่ง **ค่าเพดานเป็นพารามิเตอร์ที่มี `effective_date` และอยู่ที่ HR Configuration** (HR-1 · P-1 · P-8)

- ถ้าเอา **ตัวเลขชั่วโมง** ไปใส่เป็นขอบของ matrix ที่ DOA (เช่น `0–36` / `36–null`) จะเกิด **แหล่งความจริงสองที่ทันที** — วันที่ HR Configuration ประกาศเพดานใหม่ที่มีผลเดือนหน้า **matrix ที่ DOA จะเงียบ ๆ ผิดทันทีโดยไม่มีใครรู้** และนั่นคือการ hardcode ค่ากฎหมายในอีกรูปแบบหนึ่ง (ผิด **P-8**)
- วิธีที่ประกาศไว้ในใบนี้: feature **resolve เพดานจาก HR Configuration ณ `work_date`** → คำนวณธง **`over_cap`** → **เลือก action ที่จะส่งเข้า `GET /doa/resolve`** → เก็บ **`cap_snapshot_hours_week`** ไว้บนใบเป็นหลักฐานว่าตัดสินด้วยค่าเวอร์ชันไหน (PREBRIEF §3.1 · BR-09)
- ผลคือ: **สายอนุมัติยังมาจาก DOA 100% (ไม่ hardcode)** และ **ค่าเพดานยังอยู่ที่ HR Configuration 100% (ไม่ hardcode)** — ทั้งสอง invariant อยู่ครบพร้อมกัน
- **ทางเลือกที่ต้องให้ Architect เคาะ (OQ-DOA-03):** ถ้า DOA Engine รองรับ **มิติจุดตัดที่ไม่ใช่เงิน** (เช่น `threshold_key: ot_over_cap` แบบ boolean ที่ feature ส่งเข้ามา) ให้ยุบเหลือ **1 action 2 set** ได้ — แต่ **ห้ามใส่ตัวเลขชั่วโมงเป็นขอบของ set เด็ดขาด** ไม่ว่าจะเลือกทางไหน

### §3.2 กติกาอื่นของสาย

- **step 1 = "หัวหน้าโดยตรง"** ต้อง resolve จากสายบังคับบัญชาใน **Employee Master** ณ เวลาส่งอนุมัติ — **ไม่ใช่ role คงที่** (OQ-DOA-01)
- **step 3 = "ผู้บริหาร/ผู้จัดการฝ่ายต้นสังกัด"** — ต้องเป็นคนที่อยู่ **เหนือ step 1** ในสายบังคับบัญชา ไม่ใช่คนเดียวกัน (OQ-DOA-02)
- **มติ 2026-08-17 (บังคับ):** ทุก slot ต้องเลือก **"คน" ในตำแหน่ง** — แสดง **avatar + ตำแหน่ง + ชื่อ** ไม่ใช่ role id ลอย (FN-26)
- **SoD (BR-DOA-04 · BR-24):** ผู้ขอเซ็นอนุมัติใบของตัวเองไม่ได้ — กรณีหัวหน้าขอ OT เอง ให้ engine **ขึ้นไปหาผู้บังคับบัญชาเหนือขึ้นไป** `[DEFAULT — รอยืนยัน]` (OQ-DOA-02) · กรณีหัวหน้ายื่นแทนลูกทีม (S-35) ผู้ยื่นเป็นหัวหน้าและเป็นผู้อนุมัติ step 1 พร้อมกัน → **ต้องข้ามไปผู้บังคับบัญชาเหนือขึ้นไปเช่นกัน** (OQ-DOA-04)
- **จำนวน slot บนหน้าจอ = จำนวน step ที่ resolve ได้จริง (2 หรือ 3)** — html ห้ามวาด slot ตายตัว

## §4 Field Contract สำหรับ FRD (entity `ot_request`)

| field | ชนิด | nullable | หมายเหตุ |
|---|---|---|---|
| `approval_required` | bool | ✗ | **มาจาก DOA entry — ไม่ใช่ค่าคงที่ในตาราง** |
| `approval_action_id` | string | ✓ (Phase 1) | `ot_approve_within_cap` หรือ `ot_approve_over_cap` — **ตัดสินตอนกดส่ง จาก `over_cap`** |
| `approval_status` | enum | ✗ | `draft` · `pending_approval` · `approved` · **`time_confirmed`** · `rejected` · `cancelled` · `withdrawn` — map กับสถานะไทยใน PREBRIEF §5 |
| `over_cap` | bool | ✗ | **ธงที่เลือกสาย** — คำนวณจากชั่วโมงสะสมสัปดาห์เทียบ `cap_hours_week` ที่ resolve ณ `work_date` (BR-09) |
| `cap_snapshot_hours_week` | numeric(5,2) | ✓ | **snapshot ของเพดานที่ใช้ตัดสิน** + อยู่ในก้อน `config_version_ids` — หลักฐานว่าตัดสินด้วยค่าเวอร์ชันไหน |
| `doa_entry_ref` | string | ✓ (Phase 1) | FK ไปทะเบียน DOA |
| `approver_role` | string | ✓ | role ที่ต้องเซ็นในขั้นปัจจุบัน — **resolve จาก DOA ห้าม hardcode** |
| `approved_by` · `approved_at` | employee ref · timestamp | ✓ | ผู้เซ็นจริงในขั้นสุดท้าย |
| `approval_chain` | jsonb | ✓ | **snapshot ของสายที่ resolve ตอนกดส่ง · append-only** (BR-DOA-02) · **จำนวน step 2 หรือ 3** |
| `hours_requested_total` · `hours_approved_total` · `hours_confirmed_total` | numeric(6,2) | ✗/✓/✓ | 3 ตัวเลขอยู่คู่กันเสมอ ไม่เขียนทับกัน (PREBRIEF §7) |
| `partial_reason` | text | ✓ | **บังคับเมื่ออนุมัติบางส่วน** (BR-21) |
| `reject_reason` · `withdraw_reason` | text | ✓ | **บังคับเมื่อ reject / ถอน** (BR-12) |
| `confirmed_by` · `confirmed_at` | employee ref · timestamp | ✓ | ผู้ยืนยันเวลาจริง (A-3) — **คนละคนกับผู้อนุมัติได้** |

**Business Rules ที่ FRD ต้องมีเสมอ (จาก SKILL §FRD Injection):**

| BR | เนื้อหาที่ใช้กับ OT |
|---|---|
| BR-DOA-01 | ส่งอนุมัติได้เฉพาะสถานะ `ร่าง` (draft) — ตรงกับ PREBRIEF §5 T-2 |
| BR-DOA-02 | สายอนุมัติ resolve ตอนกดส่ง แล้ว **freeze ลง `approval_chain`** — แก้ DOA ทีหลังไม่กระทบใบที่ส่งไปแล้ว |
| BR-DOA-03 | reject → ใบเป็น "ไม่อนุมัติ" · ประวัติ **append-only** (BR-14) · แก้แล้วส่งใหม่ = **re-resolve สายใหม่** (T-7 · A-6) |
| **BR-DOA-05** *(ปรับให้เข้ากับ feature ที่จุดตัดไม่ใช่เงิน)* | **แก้ชั่วโมง/วันที่หลังส่งอนุมัติ → ต้อง re-resolve สาย และ `over_cap` ต้องถูกคำนวณใหม่** — ชั้นของสายเปลี่ยนได้ (S-15 · BR-11) แทนการ re-resolve ตามยอดเงิน |
| BR-DOA-04 | **ผู้ขอเซ็นอนุมัติใบตัวเองไม่ได้** (SoD · BR-24) |
| **BR-DOA-06** *(เพิ่มเฉพาะ feature นี้)* | **ห้ามอนุมัติเมื่อวันที่ทำ OT อยู่ในงวดที่ปิดแล้ว** — ตรวจซ้ำ ณ วินาทีอนุมัติ (BR-15 · P-7 · P-9) |
| **BR-DOA-07** *(เพิ่มเฉพาะ feature นี้)* | **ตรวจเพดานซ้ำ ณ วินาทีอนุมัติ** — ชั่วโมงสะสมของสัปดาห์อาจเปลี่ยนระหว่างรออนุมัติ (ใบอื่นของคนเดียวกันถูกอนุมัติไปก่อน) · ถ้าข้ามเพดานระหว่างทาง = **ตีกลับให้ส่งใหม่** เพื่อ re-resolve สายที่ยาวขึ้น **ห้ามอนุมัติต่อด้วยสายเดิม** |
| **BR-DOA-08** *(เพิ่มเฉพาะ feature นี้)* | **ห้ามอนุมัติเมื่อชั่วโมงที่ขอเกินเวลาจริงนอกกะ** จนกว่าจะมี `variance_ack_*` (BR-16 · FN-19) |
| **BR-DOA-09** *(เพิ่มเฉพาะ feature นี้)* | **ห้ามอนุมัติเมื่อทับใบ OT ใบอื่นของคนเดียวกัน หรือทับวันลาที่อนุมัติแล้ว** — ตรวจซ้ำ ณ วินาทีอนุมัติ (BR-19 · BR-29) |

## §5 UI Contract สำหรับ HTML (html-generator-v9 Sync Read)

| ส่วน | รายละเอียดสำหรับ OT |
|---|---|
| ปุ่ม **ส่งอนุมัติ** | อยู่ที่ **wizard step 5** · แสดงเฉพาะสถานะ "ร่าง" · disabled จนกว่า validate ผ่านครบ (ช่วงเวลา · ประเภทวัน · ไม่ทับใบอื่น/วันลา · งวดเปิด · ส่วนต่างเวลาจริง · รับทราบเมื่อยื่นแทน) |
| **แสดงผลตรวจเพดานที่ step 4** | ชั่วโมงสะสมสัปดาห์ / เพดาน (จาก HR Config) / ส่วนที่เหลือ · ถ้า `over_cap` → บอกว่า **"สายอนุมัติจะยาวขึ้น"** พร้อมแสดงสายที่จะได้ (FN-15) |
| **slot picker** (มติ 2026-08-17) | ที่ wizard step 5 — **จำนวน slot = 2 หรือ 3 ตามที่ DOA resolve คืนมา ห้ามวาดตายตัว** · แต่ละ slot เลือก **"คน" ในตำแหน่ง** แสดง **avatar → ชื่อ → ตำแหน่ง · แผนก** (#102) · **ห้ามแสดง role id ลอย** |
| Badge สถานะ | ร่าง / รออนุมัติ / อนุมัติแล้ว / **ยืนยันแล้ว** / ไม่อนุมัติ / ยกเลิก / ถอน — `.pill` 22px **คำเดียว** (#38.1) · CI Warm Light (ห้ามม่วง/น้ำเงิน) |
| **Approval Timeline** | อยู่ใน **view tab "ลายเซ็น"** — ไล่ทีละขั้น: ตำแหน่ง → ชื่อผู้เซ็น → เวลา → สถานะ · **กรณี `over_cap` ต้องเห็นครบ 3 ชั้น** (FN-32) |
| ปุ่ม **อนุมัติ / ไม่อนุมัติ / อนุมัติบางส่วน** | แสดงเฉพาะเจ้าของ slot ปัจจุบัน · **ไม่อนุมัติและอนุมัติบางส่วนบังคับใส่เหตุผล** (FN-30 · FN-31) |
| ปุ่ม **ยืนยันเวลาจริง** | แสดงเฉพาะสถานะ "อนุมัติแล้ว" และเมื่อวันที่ทำ OT ผ่านไปแล้ว + เวลาเข้างานของวันนั้นยืนยันแล้ว (FN-21) |
| ปุ่ม **ขอถอน** | แสดงเฉพาะสถานะ "อนุมัติแล้ว" / "ยืนยันแล้ว" · บังคับเหตุผล (FN-41) |
| Hook **My Approval** | ใบที่ `pending_approval` ต้องโผล่ในกล่อง My Approval ของผู้ถือ slot |
| mock ที่อนุญาต | `// TODO: DOA engine — resolve จาก DOA entry ของ feature นี้ (ดู DOA_BRIEF.md)` + `MOCK_DOA_RESOLVED = { within_cap: {action:'ot_approve_within_cap', chainMode:'sequential', steps:[{roles:['role-supervisor-direct']},{roles:['role-mgr-hr']}]}, over_cap: {action:'ot_approve_over_cap', chainMode:'sequential', steps:[{roles:['role-supervisor-direct']},{roles:['role-mgr-hr']},{roles:['role-exec-dept']}]} }` — **เลือกก้อนไหนขึ้นกับธง `over_cap` ที่คำนวณจากค่าเพดานที่ mock ว่ามาจาก HR Config** |
| **ข้อห้าม** | ❌ `const APPROVAL_CHAIN = ['หัวหน้า','HR']` ในไฟล์ feature · ❌ `if (hours > 36) …` หรือตัวเลขเพดานใด ๆ ในโค้ด — **ต้องมาจากค่าที่ mock ว่า resolve จาก HR Config** · ❌ วาด slot 2 หรือ 3 ช่องตายตัว · ❌ ตัวเลขเงินทุกชนิด |

## §6 Wire Checklist (pending → wired)

- [ ] เอา §3 ไปสร้าง **2 entry** ที่หน้า **DOA กลาง (Policy Center)** — `ot_approve_within_cap` (2 steps) และ `ot_approve_over_cap` (3 steps) · ทั้งคู่ `amount_from 0 / amount_to null` · `merged` · `sequential`
- [ ] **ยืนยัน `role-*` id จริง** กับ master 14 roles ก่อน set (ตอนนี้ทุกตัวเป็น `[DEFAULT — รอยืนยัน]`) — โดยเฉพาะวิธี resolve "หัวหน้าโดยตรง" และ "ผู้บริหารต้นสังกัด"
- [ ] **เคาะ OQ-DOA-03** — DOA รองรับมิติจุดตัดที่ไม่ใช่เงินหรือไม่ · ถ้ารองรับให้ยุบเหลือ 1 action 2 set · **ไม่ว่าทางไหนก็ห้ามใส่ตัวเลขชั่วโมงเป็นขอบของ set**
- [ ] dev wire `GET /doa/resolve` ที่ **wizard step 5** (ส่ง `action_id` ที่เลือกจาก `over_cap`) + จุดอนุมัติ/ปฏิเสธ/อนุมัติบางส่วน/ยืนยันเวลาจริง/ขอถอน/แก้แล้วส่งใหม่ (A-1…A-6)
- [ ] snapshot `approval_chain` + `cap_snapshot_hours_week` + `config_version_ids` ตอนส่ง (freeze) และ **re-resolve เมื่อแก้แล้วส่งใหม่** (BR-DOA-05)
- [ ] เพิ่ม guard **BR-DOA-06** (งวดปิด) · **BR-DOA-07** (ตรวจเพดานซ้ำ → ข้ามเพดานระหว่างรอ = ตีกลับให้ re-resolve) · **BR-DOA-08** (ส่วนต่างเวลาจริง) · **BR-DOA-09** (ทับใบอื่น/วันลา) ที่จุดอนุมัติ
- [ ] ตรวจว่าใบโผล่ใน **My Approval** จริง และ **`doa_pending`/`doa_result` แจ้งเตือนอัตโนมัติ** — **`NTF_BRIEF` ของ feature นี้ต้องไม่ประกาศซ้ำ**
- [ ] **ห้ามทำ delegation / expiry / reminder เอง** — DOA Engine มีให้แล้ว (`feature-catalog-master.md §0` · S1.5 G-10 · G-11)
- [ ] `wire_status: pending → wired` · อัพเดต `FEATURE_REGISTRY.md` · แจ้งพี่เบิร์ดอัพ Google Sheet H·F·Q
- [ ] **ตรวจว่า `CSQ_BRIEF` ไม่มี `dc`** — DC ระดับเอกสารเป็นของ DOA engine (register 422 ถ้าซ้ำ) · feature นี้มี approval จริง **สองชั้น** ยิ่งต้องไม่ประกาศซ้ำ

## §7 Open Questions

| # | ประเด็น | ค่าที่ใช้ไปก่อน | เจ้าภาพ |
|---|---|---|---|
| OQ-DOA-01 | **`role-*` id จริง** ของ "หัวหน้าโดยตรง" · "ผู้จัดการ HR" · "ผู้บริหารต้นสังกัด" — master 14 roles ไม่มีในเวิร์กสเปซ · "หัวหน้าโดยตรง" อาจต้อง dynamic resolve จาก Employee Master | `role-supervisor-direct` · `role-mgr-hr` · `role-exec-dept` `[DEFAULT — รอยืนยัน]` | Architect / Policy Center |
| OQ-DOA-02 | **SoD ชนกับ step 1** (ผู้ขอเป็นหัวหน้าเอง) | **ขึ้นไปหาผู้บังคับบัญชาเหนือขึ้นไป** `[DEFAULT — รอยืนยัน]` (ปลอดภัยกว่าการข้ามชั้น) | Strike / Policy Center |
| **OQ-DOA-03** ⭐ | **DOA Engine รองรับมิติจุดตัดที่ไม่ใช่เงินหรือไม่** (`threshold_key: ot_over_cap` boolean) | **ประกาศเป็น 2 action แยก** `[DEFAULT — รอยืนยัน]` — ปลอดภัยที่สุดเพราะไม่ต้องเอาตัวเลขชั่วโมงไปฝังใน matrix (ดู §3.1) | Architect (DOA Engine) |
| OQ-DOA-04 | หัวหน้า **ยื่นแทนลูกทีม** (S-35) — ผู้ยื่นคือหัวหน้าซึ่งเป็น step 1 ด้วย | **ข้ามไปผู้บังคับบัญชาเหนือขึ้นไปเช่นเดียวกับ OQ-DOA-02** `[ASSUMED]` | Strike |
| OQ-OT-11 | ถอนใบที่อนุมัติแล้วต้องผ่านสายอนุมัติซ้ำหรือไม่ (A-5) | **ต้องผ่านสายเดิมอีกครั้ง** `[ASSUMED]` (PREBRIEF §5 T-9) | Strike / BA |
| OQ-OT-19 | **อนุมัติอัตโนมัติ** เมื่อชั่วโมงต่ำกว่าเกณฑ์ (S1.5 G-06) | **ไม่รองรับ** — ถ้าจะมี ต้องตั้งเป็นกติกาที่ **DOA กลาง** ห้ามเขียนใน feature | Strike / Policy Center |

## Quality Gate (self-check)

| # | เช็ค | ผล |
|---|---|---|
| G1 | ทุก role เป็น `role-*` id (ไม่ใช่ชื่อตำแหน่งลอย) | ✅ `role-supervisor-direct` · `role-mgr-hr` · `role-exec-dept` — **ติด `[DEFAULT — รอยืนยัน]` ครบ** (OQ-DOA-01) |
| G2 | ทุก set มี `amount_from` และ `amount_to` ครบ | ✅ `0` / `null` ทั้ง 2 set |
| G3 | ช่วงต่อเนื่อง ไม่ทับ ไม่มีรู | ✅ แต่ละ action มีชุดเดียวครอบทั้งช่วง · **จุดตัดจริงอยู่ที่ action ไม่ใช่ช่วง amount** (§3.1) |
| G4 | set สุดท้าย `amount_to: null` | ✅ ทั้ง 2 set |
| G5 | `approval_scope` เป็นค่าที่มีจริง | ✅ `document_sign` (ใบ OT มีลายเซ็น + พิมพ์ได้) |
| G6 | ค่าที่ยังไม่ยืนยันติด `[DEFAULT — รอยืนยัน]` ครบ | ✅ role ids · A-5 · OQ-DOA-02 · OQ-DOA-03 |
| G7 | ไม่มีสายอนุมัติ hardcode หลุดเข้า FRD/HTML | ✅ §5 ระบุ mock pattern ที่อนุญาต + ข้อห้ามชัด · **hardcode = governance Hard Stop** |
| **G8** *(เพิ่มเฉพาะใบนี้)* | **ไม่มีตัวเลขเพดาน/ค่ากฎหมายฝังใน matrix หรือในโค้ด** | ✅ §3.1 — จุดตัดเป็น action ที่เลือกจากธง `over_cap` ซึ่งคำนวณจากค่าที่ resolve จาก HR Configuration ณ `work_date` พร้อม snapshot บนใบ |

**Verdict: PASS** — พร้อมให้คนไปตั้งค่า **2 entry** ที่หน้า DOA กลาง (`wire_status: pending`)
