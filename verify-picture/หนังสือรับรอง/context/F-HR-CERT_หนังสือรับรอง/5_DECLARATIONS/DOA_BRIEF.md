# DOA_BRIEF — F-HR-CERT · Employment / Salary Certificate (หนังสือรับรอง)

> ออกโดย `doa-declaration` v1.0 · **Lane Mode (no-ask)** · S1.8 · 2026-08-30
> Input: `briefs/W3/F-HR-CERT/PREBRIEF.md` v1.0 **§12 (สัญญาณประกาศ · authoritative)** + §5 state machine + §4 BR + §13 patch · `LANE_BRIEF.md` (chip) · `_lane/DECL.json`
> **DIVERGENCE: —** (chip `doa ✓` = detect §12 `need` = `CONTEXT_PACK/HR.md` แถวหนังสือรับรอง → **✓ "HR"**)
> หมายเหตุ: `references/doa-contract.md` และ `references/brief-template.md` **ไม่มีในเวิร์กสเปซนี้** (เหมือนเคส Leave / OT / On-Offboard / Employee Movement) — ยึด contract จาก SKILL.md (Iron Rule · Quality Gate G1–G7) + `cube-4.0-current-state.md §3` + `feature-catalog-master.md §0` · **`role-*` id ทุกตัวจึงติด `[DEFAULT — รอยืนยัน]`** (cross-check กับ master 14 roles ที่ Policy Center ก่อน set จริง) · role id ที่ใช้เป็นชุดเดียวกับที่ 4 ใบพี่น้องของ HR ประกาศไว้แล้ว
> **feature ประกาศเท่านั้น — ห้าม hardcode สายอนุมัติ** (DOA iron rule · `GET /doa/resolve`) · **hardcode = governance Hard Stop**

## §1 Identity

| | |
|---|---|
| feature_id | `F-HR-CERT` |
| feature name | Employment / Salary Certificate · หนังสือรับรอง (`CERT-YYYY-NNNN`) |
| module | HR |
| platform | Core ERP (core.2bsimple.com) |
| archetype | Q-document |
| **approval_scope** | **`document_sign`** — หนังสือพิมพ์ออกมาได้และมี **ช่องลงนาม 1 ช่อง + ที่ว่างสำหรับตราบริษัท** ตรงกับ `PDFDOC/template.html` · ชื่อ/ตำแหน่งผู้ลงนามบนหนังสือ = **ผู้อนุมัติขั้นสุดท้ายที่เซ็นจริง** (PREBRIEF FN-54) |
| **มีวงเงิน (เงิน)?** | ⭐ **❌ ไม่มีวงเงิน** — feature นี้ **มีตัวเลขค่าจ้างอยู่บนเอกสารจริง แต่ตัวเลขนั้นเป็น *ข้อมูลที่ถูกรับรอง* ไม่ใช่ *ยอดที่ถูกอนุมัติ*** · **ไม่มีเงินไหลออกจากองค์กรจากใบนี้เลย** (PREBRIEF **BR-06**) → ทุก set ใช้ `amount_from: 0` · `amount_to: null` |
| **มีจุดตัด (threshold) ไหม?** | ✅ **มี — และเป็นจุดตัดมิติเดียวที่ไม่ใช่เงิน** = **`has_salary_figure`** (ธงที่ระบบคำนวณจาก `cert_type`) |
| จำนวนสายอนุมัติ | **2 สาย** (`matrix` 2 ชุด ผูก 2 action) — **1 ขั้น** และ **2 ขั้น** |
| chainMode | **`sequential`** ทั้งสองสาย (PREBRIEF §5 T-02 → T-05) |
| departments | **`merged`** — ทุกแผนกใช้กฎชุดเดียวกัน (ไม่มีสัญญาณแยกแผนกใน scope note) |
| version | 1.0 (2026-08-30) · `wire_status: pending` |

## §2 Approval Actions

| # | action_id | ชื่อ | trigger (PREBRIEF) | ผลเมื่อ **approve** | ผลเมื่อ **reject** |
|---|---|---|---|---|---|
| **A-1** | `cert_approve_employment` | **อนุมัติคำขอหนังสือรับรองการทำงาน / ใบผ่านงาน** | §5 **T-02** เมื่อ **`has_salary_figure = false`** (S-01 · S-03 · S-43 · FN-28) | ใบเข้าสถานะ **"อนุมัติแล้ว"** (T-05) · **ยังไม่ใช่หนังสือ** — สิทธิ์ที่จะกดออกหนังสือเท่านั้น · NTF ผลอนุมัติถึงผู้ขอ (FN-60) | ใบเป็น **"ไม่อนุมัติ"** · **บังคับ `reject_reason`** (FN-31) · ⭐ **เลขที่คงอยู่ ไม่ reuse** (BR-01 · FN-25) |
| **A-2** ⭐ | `cert_approve_salary` | **อนุมัติคำขอหนังสือรับรองเงินเดือน (สายยาวกว่า)** | §5 **T-02** เมื่อ **`has_salary_figure = true`** (S-02 · S-18 · FN-28) | เหมือน A-1 · ⭐ **ผู้อนุมัติขั้นที่ 2 คือผู้ที่รับผิดชอบข้อมูลค่าจ้าง** — เป็นชั้นที่ยืนยันว่า *ข้อมูล RESTRICTED กำลังจะออกนอกองค์กรอย่างมีผู้รับผิดชอบ* | เหมือน A-1 |
| **A-3** | `cert_approve_resubmit` | **อนุมัติใบที่แก้แล้วส่งใหม่** | ใบถูกปฏิเสธ/ยกเลิก → ผู้ขอสร้าง **ใบใหม่ เลขใหม่** (S-10 · S-11 · BR-07) | ⭐ **`resolve` สายใหม่ทั้งสาย** — ชั้นเปลี่ยนได้ถ้าธง `has_salary_figure` เปลี่ยน | เหมือน A-1 |
| **A-4** | `cert_approve_reissue` | **อนุมัติการออกใหม่แทนฉบับเดิม** | §5 **T-09** ออกใหม่แทน (S-15 · FN-68 · `OQ-CT-09` default = ผ่านสายใหม่) | ใบใหม่ **เลขใหม่ + `supersedes: <เลขเดิม>`** · ใบเดิมเป็น **"ถูกแทนที่"** · ⭐ **ไม่แก้และไม่ลบของเดิม** (BR-22) | ใบใหม่เป็น "ไม่อนุมัติ" · ใบเดิมคงสถานะเดิมทุกประการ |

> **A-3 · A-4 ใช้ matrix ของ A-1/A-2 ตามค่า `has_salary_figure` ณ เวลาที่ resolve** — ไม่มี matrix ของตัวเอง (แพทเทิร์นเดียวกับ `F-HR-MOVE` A-5/A-6)
> ⭐ **"การออกหนังสือ" (T-06) ไม่ใช่ action ของ DOA** — เป็นการลงมือทำตามสิทธิ์ที่ได้จากการอนุมัติแล้ว · อำนาจอยู่ที่การอนุมัติคำขอ ไม่ใช่ที่การกดปุ่ม render (ถ้าทำเป็น action จะกลายเป็นการอนุมัติซ้ำสองชั้นในเรื่องเดียวกัน)
> ⭐ **"การเพิกถอน" (T-08) รอบนี้ไม่ประกาศเป็น action ของ DOA** — PREBRIEF §12 ไม่มีสัญญาณ DOA ที่ S-14 · รอบนี้ใช้ **สิทธิ์ระดับเดียวกับผู้อนุมัติหนังสือ + บังคับเหตุผล + audit append-only** (FN-67) → **`OQ-DOA-CT-C`** ให้ Strike เคาะว่าต้องมีสายอนุมัติของตัวเองไหม

## §3 Matrix ที่จะไปตั้งค่า (กรอกลงหน้า DOA กลางได้ตรงช่อง)

| set | ผูกกับ action | amount_from | amount_to | departments | chainMode | steps[roles] |
|---|---|---|---|---|---|---|
| **1** | `cert_approve_employment` | `0` บาท | `null` (ไม่จำกัด) | `merged` | `sequential` | **step 1:** `role-mgr-hr` `[DEFAULT — รอยืนยัน]` — ผู้จัดการฝ่ายบุคคล (**"HR อนุมัติ" ตาม scope note ตรงตัว**) |
| **2** ⭐ | `cert_approve_salary` | `0` บาท | `null` | `merged` | `sequential` | **step 1:** `role-mgr-hr` `[DEFAULT — รอยืนยัน]` · **step 2:** `role-comp-admin` `[DEFAULT — รอยืนยัน]` — **ผู้ดูแลข้อมูลค่าจ้าง (ผู้มีสิทธิ์เห็นตัวเลข RESTRICTED)** |

- **`amount_to: null` ในชุดสุดท้ายของทั้ง 2 set ✅ (G4)** — ไม่มีใบไหนตกขอบไม่มีคนเซ็น
- **ไม่มีรู/ไม่ทับ ✅ (G3)** — แต่ละ action มีชุดเดียวที่ครอบ `0 → ไม่จำกัด` · **การแบ่งสายเกิดที่ชั้น action ไม่ใช่ชั้นช่วงเงิน**
- **หน่วยเงิน:** บาท — แต่ feature นี้ **ไม่ส่งค่าเงินเข้า `resolve` เลย** (BR-06) · ช่อง `amount` มีไว้ให้ record ถูก schema ของ DOA เท่านั้น
- **ความยาวสาย 1 → 2 ขั้น** สอดคล้องกับ scope note "DOA (HR อนุมัติ)" + ข้อกำหนด RESTRICTED ✅ (G5 `approval_scope = document_sign`)

### §3.1 ⭐ ทำไมจุดตัดถึงเป็น `has_salary_figure` ไม่ใช่ตัวเลขเงินเดือนของคนที่ขอ

- ถ้าเอา **จำนวนเงินเดือนของพนักงาน** ไปเป็นขอบของ matrix (เช่น "เงินเดือนเกิน 100,000 ต้องให้ผู้บริหารเซ็น") จะเกิดผลเสีย **สองชั้นพร้อมกัน**: (ก) **ตัวเลขค่าจ้างที่มี `effective_date` ถูก hardcode ลงในทะเบียน DOA** — วันที่ Salary Structure ประกาศกระบอกใหม่ matrix จะเงียบ ๆ ผิดทันที (ผิด `P-8` · `P-8′`) (ข) ⭐ **ที่ร้ายกว่านั้น — มันทำให้ "เงินเดือนของคนคนหนึ่ง" รั่วออกมาเป็นความยาวของสายอนุมัติ** ใครก็ตามที่เห็นว่าใบนี้ต้องผ่านกี่ขั้น จะอนุมานช่วงเงินเดือนของเจ้าของใบได้ทันที — **นั่นคือช่องทางอ้อมที่ `SS-5` ห้ามไว้ตรง ๆ**
- วิธีที่ประกาศไว้ในใบนี้: feature **คำนวณธง `has_salary_figure` จาก `cert_type` เท่านั้น** (ฟังก์ชันตายตัว ไม่ใช่ดุลพินิจของผู้ยื่น · PREBRIEF §3.1) → **เลือก `action_id` จากธงนั้น** → ส่งเข้า `GET /doa/resolve` → **ไม่มีตัวเลขเงินเดินทางเข้าไปใน DOA เลยแม้แต่ค่าเดียว**
- ผลคือ: **สายอนุมัติมาจาก DOA 100%** และ **ตัวเลขค่าจ้างยังอยู่ที่ Salary Structure 100% พร้อมชั้น masking เดิม** — invariant ทั้งสองอยู่ครบพร้อมกัน · เป็นหลักการเดียวกับที่ 3 ใบพี่น้องเคาะไว้แล้ว (Leave = ประเภทการลา · OT = ธง `over_cap` · Movement = (`sub_type`, `has_pay_change`))
- **ทางเลือกที่ต้องให้ Architect เคาะ (`OQ-DOA-CT-B`):** ถ้า DOA Engine รองรับจุดตัดที่ไม่ใช่เงิน (`threshold_key: cert_has_salary_figure` แบบ boolean) ให้ยุบเหลือ **1 action 2 set** ได้ — แต่ **ห้ามใส่ตัวเลขเงินเป็นขอบของ set เด็ดขาด** ไม่ว่าจะเลือกทางไหน

### §3.2 กติกาอื่นของสาย

- **มติ 2026-08-17 (บังคับ):** ทุก slot ต้องเลือก **"คน" ในตำแหน่ง** — แสดง **avatar + ตำแหน่ง + ชื่อ** ไม่ใช่ role id ลอย (FN-27)
- **SoD (BR-DOA-04 · PREBRIEF BR-08 · FN-30):** ⭐ **จุดที่ feature นี้เสี่ยงกว่าใบอื่น** — ผู้ยื่นมักเป็น **HR เอง** (ยื่นแทนพนักงาน · S-35 · S-43) และผู้อนุมัติก็คือ HR → **ถ้า `resolve` คืนสายที่มีแต่ตัวผู้ยื่น ต้องบล็อกและให้ engine ขึ้นไปหาผู้บังคับบัญชาเหนือขึ้นไป** `[DEFAULT — รอยืนยัน]` (`OQ-DOA-CT-A`)
- **step 2 ของ set 2 (`role-comp-admin`)** เป็นขั้นที่ **ต้องมีสิทธิ์เห็นตัวเลขจริง** — ถ้าผู้ถูกเลือกใน slot นี้ไม่มีสิทธิ์ RESTRICTED **ต้องเลือกคนนั้นไม่ได้ตั้งแต่ตอน slot picker** (ไม่ใช่ปล่อยผ่านแล้วไปตายตอนกดออกหนังสือ · เชื่อมกับ FN-39)
- **จำนวน slot บนหน้าจอ = จำนวน step ที่ resolve ได้จริง (1 หรือ 2)** — html **ห้ามวาด slot ตายตัว**
- **การแช่แข็ง:** สาย resolve ตอนกดส่ง แล้ว **freeze** ลง `approval_chain` — แก้ทะเบียน DOA ทีหลังไม่กระทบใบที่ส่งไปแล้ว (BR-DOA-02 · PREBRIEF BR-07)
- **ไม่มี `amount` ที่จะทำให้ต้อง re-resolve** (BR-DOA-05 ไม่ applicable — feature นี้ไม่มียอดเงินบนใบที่แก้ได้)

## §4 Field Contract สำหรับ FRD (entity `employment_certificate`)

| field | ชนิด | nullable | หมายเหตุ |
|---|---|---|---|
| `approval_required` | bool | ✗ | มาจาก DOA entry — **ไม่ใช่ค่าคงที่ในตาราง** |
| `approval_status` | enum | ✗ | `draft` · `pending_approval` · `approved` · `rejected` · `cancelled` — map กับสถานะไทยใน PREBRIEF §5 |
| `doa_entry_ref` | string | ✓ (Phase 1) | FK ไปทะเบียน DOA |
| `doa_action_id` | string | ✗ เมื่อ ≥ `pending_approval` | ⭐ `cert_approve_employment` / `cert_approve_salary` — **ค่าที่เลือกจากธง `has_salary_figure` ด้วยฟังก์ชันตายตัว** |
| `has_salary_figure` | bool | ✗ | ⭐ **computed จาก `cert_type` เท่านั้น** — ห้ามให้ผู้ใช้ตั้งเอง |
| `approver_role` | string | ✓ | role ของขั้นปัจจุบัน (resolve จาก DOA) |
| `approved_by` · `approved_at` | string · timestamp | ✓ | ผู้เซ็นจริงขั้นสุดท้าย — ⭐ **ชื่อ+ตำแหน่งนี้คือสิ่งที่พิมพ์ใต้ช่องลงนามบนหนังสือ** |
| `approval_chain` | jsonb | ✓ | **snapshot ตอนกดส่ง · append-only** |
| `reject_reason` | text | ✓ | บังคับเมื่อ reject |
| `revoked_by` · `revoked_at` · `revoke_reason` | string · timestamp · text | ✓ | การเพิกถอน (ยังไม่ใช่ DOA action รอบนี้ · `OQ-DOA-CT-C`) |
| `supersedes` · `superseded_by` | string | ✓ | คู่ของการออกใหม่แทน |

**Business Rules ที่ต้องมีเสมอ (มาตรฐาน DOA · map กับ BR ของ PREBRIEF):**

| BR | เนื้อหา | map |
|---|---|---|
| BR-DOA-01 | ส่งอนุมัติได้เฉพาะสถานะ `draft` (ร่าง) | PREBRIEF §5 T-02 |
| BR-DOA-02 | สายอนุมัติ resolve ตอนส่ง แล้ว **freeze** — แก้ DOA ทีหลังไม่กระทบใบที่ส่งแล้ว | **BR-07** |
| BR-DOA-03 | reject → **ไม่กลับไปแก้ใบเดิม** — ใบนี้สิ้นสุด · แก้แล้วส่งใหม่ = ใบใหม่ เลขใหม่ (ต่างจาก PR/PO เพราะเลขเอกสารเป็นของทะเบียน append-only) · ประวัติ reject เก็บ append-only | **BR-01 · BR-07 · BR-22** |
| BR-DOA-04 | ผู้ขอ/ผู้ยื่นแทนเซ็นอนุมัติใบตัวเองไม่ได้ (SoD) | **BR-08** · FN-30 |
| BR-DOA-05 | *(ไม่ applicable)* — ไม่มียอดเงินบนใบที่แก้แล้วต้อง re-resolve | **BR-06** |

**§ที่ต้องเพิ่มใน FRD Pack:** `05_RULES.md` หัวข้อ "การอนุมัติ (DOA)" ชี้มาที่ไฟล์นี้ · `00_OVERVIEW §Dependencies` อ้าง `GET /doa/resolve`

## §5 UI Contract สำหรับ HTML (html-generator-v9 Sync Read)

| ส่วน | รายละเอียด |
|---|---|
| ปุ่ม **ส่งคำขอ** | แสดงเฉพาะสถานะ `ร่าง` · disabled จนกว่าจะเลือกคนครบทุก slot และ (ถ้าเข้าเงื่อนไข) ติ๊กร่องรอยความยินยอมแล้ว (FN-13 · FN-27) |
| **slot picker** | **จำนวน slot = จำนวน step ที่ resolve ได้จริง (1 หรือ 2)** · แต่ละ slot = combobox คน แสดง **avatar → ชื่อ → ตำแหน่ง · แผนก** (#102 · มติ 2026-08-17) · ⭐ slot ที่ผูกกับ `role-comp-admin` กรองเฉพาะผู้มีสิทธิ์เห็นข้อมูลค่าจ้าง |
| Badge สถานะ | ร่าง / รออนุมัติ / อนุมัติแล้ว / ไม่อนุมัติ / ยกเลิกแล้ว / **ออกแล้ว** / ส่งมอบแล้ว / เพิกถอนแล้ว / ถูกแทนที่ — **pill คำเดียว 22px** (#38.1) |
| **Approval Timeline** | tab "ประวัติ" — ไล่ทีละขั้น: ตำแหน่ง → ชื่อผู้เซ็น → เวลา → สถานะ (รอ/ผ่าน/ตีกลับ) · **append-only** (FN-70) |
| ปุ่ม **อนุมัติ / ไม่อนุมัติ** | เฉพาะผู้มีสิทธิ์ในขั้นปัจจุบัน · ไม่อนุมัติ **บังคับเหตุผล** (FN-31) |
| ปุ่ม **ออกหนังสือ** | ⭐ **แสดงเฉพาะสถานะ "อนุมัติแล้ว"** — เป็นปุ่มของ feature ไม่ใช่ของ DOA (FN-34) |
| Hook **My Approval** | ใบที่ `pending_approval` ต้องโผล่ในกล่อง My Approval |
| ⭐ **ห้ามมี** | `const APPROVAL_CHAIN = [...]` หรือ array ชื่อ role ในไฟล์ feature (**G7**) · ให้ประกาศ mock ที่ resolve จากรูป DOA entry แทน พร้อม `// TODO: DOA engine` |
| mock | ⭐ ต้องมี **อย่างน้อย 2 ชุด** (1 ขั้น กับ 2 ขั้น) เพื่อพิสูจน์ว่าสายเปลี่ยนตามธง `has_salary_figure` จริง (FN-28) — **ไม่ใช่เปลี่ยนตามเงิน** |

## §6 Wire Checklist (pending → wired)

- [ ] สร้าง DOA entry ของ `F-HR-CERT` ที่หน้า DOA กลาง ตาม matrix §3 (2 set)
- [ ] cross-check `role-mgr-hr` · `role-comp-admin` กับ master 14 roles ของ Policy Center → ลบป้าย `[DEFAULT — รอยืนยัน]`
- [ ] ยืนยันกติกา SoD เมื่อผู้ยื่นแทนคือ HR เอง (`OQ-DOA-CT-A`)
- [ ] ยืนยันว่า slot `role-comp-admin` กรองเฉพาะผู้มีสิทธิ์ RESTRICTED ได้จริงจาก Policy Center
- [ ] dev wire `GET /doa/resolve` ตอนกดส่ง + freeze `approval_chain` → toggle `wire_status: pending → wired`
- [ ] ตรวจว่าใบโผล่ใน My Approval จริง และชื่อผู้อนุมัติขั้นสุดท้ายไหลไปพิมพ์ใต้ช่องลงนามบน PDF
- [ ] ตรวจว่า **ไม่มีตัวเลขเงินใด ๆ ถูกส่งเข้า `resolve`** (grep `amount` ในโค้ดที่เรียก DOA = ต้องไม่มีค่าจริง)

## §7 Open Questions

| id | คำถาม | default ที่ใช้ | ใครตอบ |
|---|---|---|---|
| **OQ-DOA-CT-A** | เมื่อผู้ยื่นแทน (HR) เป็นคนเดียวกับผู้อนุมัติที่ resolve ได้ ให้ engine ขึ้นไปหาผู้บังคับบัญชาเหนือขึ้นไป หรือให้บล็อกแล้วให้เลือกคนอื่นในสิทธิ์เดียวกัน? | **บล็อก + ให้เลือกคนอื่นที่มีสิทธิ์เดียวกัน** `[DEFAULT — รอยืนยัน]` | Architect (DOA) |
| **OQ-DOA-CT-B** | DOA Engine รองรับ `threshold_key` ที่เป็น boolean (ไม่ใช่เงิน) ไหม — ถ้ารองรับให้ยุบเหลือ 1 action 2 set | **แยกเป็น 2 action** (ทำงานได้แน่นอนกับ schema ปัจจุบัน) | Architect (DOA) |
| **OQ-DOA-CT-C** | **การเพิกถอนหนังสือที่ออกไปแล้ว ต้องมีสายอนุมัติของตัวเองไหม?** | **ไม่มีสายแยกรอบนี้** — ใช้สิทธิ์ระดับผู้อนุมัติหนังสือ + บังคับเหตุผล + audit append-only (PREBRIEF §12 ไม่มีสัญญาณ DOA ที่ S-14) | **Strike / BA** |
| **OQ-DOA-CT-D** | ออกใหม่แทน (reissue) ต้องผ่านสายเต็มทุกครั้ง หรือย่อได้เมื่อเหตุผลคือ "ระบบพิมพ์ผิด"? | **ผ่านสายเต็มทุกครั้ง** (`OQ-CT-09`) — ใบใหม่ = เลขใหม่ = สายใหม่ | BA |

## Quality Gate (self-check)

| # | เช็ค | ผล |
|---|---|---|
| G1 | ทุก role เป็น `role-*` | ✅ `role-mgr-hr` · `role-comp-admin` — **ติด `[DEFAULT — รอยืนยัน]` ครบ** (master ไม่มีในเวิร์กสเปซ) |
| G2 | ทุก set มี `amount_from` + `amount_to` | ✅ ครบทั้ง 2 set |
| G3 | ช่วงไม่ทับ ไม่มีรู | ✅ แต่ละ action มีชุดเดียว `0 → null` |
| G4 | set สุดท้าย `amount_to: null` | ✅ ทั้ง 2 set |
| G5 | `approval_scope` เป็น 1 ใน 3 ค่าที่มีจริง | ✅ `document_sign` |
| G6 | ค่าที่ยังไม่ยืนยันติด `[DEFAULT — รอยืนยัน]` | ✅ ครบทุก role + กติกา SoD |
| G7 | ไม่มีสายอนุมัติ hardcode หลุดเข้า FRD/HTML | ✅ ประกาศไว้ใน §5 เป็นข้อห้ามชัดเจน + mock 2 ชุดพิสูจน์ |
