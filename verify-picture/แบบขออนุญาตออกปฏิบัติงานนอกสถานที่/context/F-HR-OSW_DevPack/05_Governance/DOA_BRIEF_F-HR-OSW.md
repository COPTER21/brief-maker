# DOA_BRIEF_F-HR-OSW — แบบขออนุญาตออกปฏิบัติงานนอกสถานที่ · v1.1 (5 ต.ค. 2569)

> **ใบประกาศ** ให้ผู้ดูแล DOA เอาไปตั้ง entry จริงที่หน้า DOA กลาง (Policy Center › DOA · F-DLG-001) — F-HR-OSW **ประกาศเท่านั้น** ไม่เก็บสายอนุมัติเอง
> ที่มา: FRD_F-HR-OSW_Pack v1.0.1 (02 API-05..09/13 · 03 FN-07/08/09/10/16 · 04 T_osw_request · 05 BR-OSW-09..12) · HTML รอบ 4 · DOCCFG_BRIEF v1.1 (sign_boxes) · DECISIONS DEC-03/10
> ✅ ยืนยันโดย DA 5 ต.ค. 2569: **DOA dynamic** (จำนวนขั้น/role ต่อขั้นตั้งที่ DOA กลาง feature รองรับ N ขั้น) · **ไม่มีวงเงิน** · wire_status = `pending`
> v1.1: sync กับ FRD Pack (field/API/function จริง) · ผูกช่องลายเซ็นกับ DOCCFG v1.1 · Quality Gate G1–G7

## §1 Identity
| Field | Value |
|---|---|
| feature_id | F-HR-OSW (รหัสจริงกำหนดตอนเริ่มพัฒนา — FRD 07 CD-01) |
| feature_name | แบบขออนุญาตออกปฏิบัติงานนอกสถานที่ (Off-site Work Request) |
| module | HR · Core Cube › HR |
| platform | Core (ต่อ tenant ลูกค้า) |
| DOA type (key) | `osw` |
| approval_scope | `document_sign` ✅ — ผลแต่ละขั้นขึ้นช่องลายเซ็นใน PDF (1 ช่องต่อขั้น · DOCCFG_BRIEF v1.1 sign_boxes) |
| approval_required | `true` ทุกใบ |
| chainMode | `sequential` |
| wire_status | `pending` |

## §2 Approval Actions
| # | Action | ปุ่ม / ที่มา | Trigger ไป DOA | Approve → | Reject → |
|---|---|---|---|---|---|
| A1 | ส่งขออนุญาต | wizard `บันทึกและส่งขออนุญาต` · view `ส่งขออนุญาต` (เฉพาะ draft ของตัวเอง) → M-01 | API-05 → FN-07 `DOA.resolve({type:'osw', requester, dept})` → slot picker 1 แถวต่อขั้น · API-06 → FN-08 snapshot `approval_chain` + `DOA.submit` → `pending_approval` | ขั้นถัดไป pending · ครบทุกขั้น → `approved` · ล็อกแก้ไข · FN-13 เก็บ PDF approved_final | `rejected` + เหตุผล · ขั้นที่เหลือ `skipped` · ผู้ขอทำซ้ำเป็นใบใหม่ (DEC-10) |
| A2 | ตัดสินขั้น (ในหน้า feature) | P-03 `อนุญาต` / `ไม่อนุญาต` · timeline inline (เฉพาะผู้พิจารณาขั้นปัจจุบัน) | API-07/08 → FN-09 → `DOA.decide` | ตาม A1 | ตาม A1 |
| A3 | ตัดสินขั้น (จาก My Approval) | กล่อง My Approval ของ DOA กลาง | DOA → callback API-13 → FN-16 → FN-09 | ตาม A1 | ตาม A1 |
| A4 | ยกเลิกระหว่างรอ | P-03 / ⋮ `ยกเลิกเอกสาร` (เจ้าของ/HR) | API-09 → FN-10 → `DOA.cancel(doa_ref)` | — | งานหายจาก My Approval · callback ที่มาทีหลัง = ignored |

**จำนวนสาย (Q1):** 1 สาย → `matrix` เดียว · **ไม่อยู่ในสาย DOA:** สร้าง/แก้ร่าง · ยกเลิก (ใช้สิทธิ์เจ้าของ/HR) · ทำซ้ำ · พิมพ์ · ส่งออก

## §3 Matrix ที่จะไปตั้งค่า (กรอกลงหน้า DOA กลาง)
**Q2 วงเงิน:** ❌ ไม่มีวงเงิน ✅ · **Q3 แยกแผนก:** `merged` ✅ · **Q4 scope:** `document_sign` ✅

| set | amount_from (บาท) | amount_to (บาท) | departments | chainMode | steps[roles] |
|---|---|---|---|---|---|
| 1 | 0 | `null` (ไม่จำกัด) | ทุกแผนก (merged) | `sequential` | step 1: `role-line-manager` — ผู้บังคับบัญชาตรงของผู้ขอ (resolve จากผังองค์กร F-ORG-001) ✅ ค่าเริ่มต้น |

- **Dynamic:** เพิ่มขั้น (เช่น `HR รับทราบ`) หรือเปลี่ยน role ได้ที่ DOA กลางโดยไม่แก้ feature — slot picker / timeline / ช่องลายเซ็น PDF ขยายตามจำนวนขั้นเอง (ทดสอบ 2 ขั้นแล้ว: FRD 06 AC-08 · prototype D11–D13)
- ตัวอย่างลูกค้า: ผู้อนุมัติ = MD ซึ่งเป็นผู้บังคับบัญชาตรงของผู้ขอ → ตรงกับ `role-line-manager`
- ผู้ส่งเปลี่ยนคนในแต่ละขั้นได้ตอนส่ง (slot picker) — ค่าเริ่มจาก resolve · ห้ามเลือกตัวเอง

**ค่าที่ F-HR-OSW ส่งตอน resolve/submit:** `type:'osw'` · `osw_id` · `osw_no` · `requester` · `dept` (org_unit_id) · `mode` · `range_from` · `range_to` · `tenant_id` — **ไม่ส่งยอดเงิน** (ไม่มีวงเงิน)

## §4 Field Contract สำหรับ FRD (`T_osw_request` — FRD 04 §4.2)
| Field มาตรฐาน (skill) | ใน F-HR-OSW | ชนิด | Null | หมายเหตุ |
|---|---|---|---|---|
| `approval_required` | `approval_required` | bool | NO | true |
| `approval_status` | `status` | varchar(20) | NO | draft / pending_approval / approved / rejected / cancelled (UI: ร่าง / รออนุญาต / อนุญาตแล้ว / ไม่อนุญาต / ยกเลิก) |
| `doa_entry_ref` | `doa_entry_ref` | varchar(40) | YES | |
| (อ้างงาน) | `doa_ref` | varchar(60) | YES | id งานใน DOA engine — ตรวจ callback (FN-16) |
| `approver_role` | `approver_role` | varchar(80) | YES | role ขั้นปัจจุบัน |
| `approved_by` | `approved_by` | uuid | YES | ผู้พิจารณาขั้นสุดท้าย |
| `approval_chain` | `approval_chain` | jsonb | YES | snapshot ตอนส่ง `[{step, role, role_id, assignee, assignee_name, assignee_position, status, at, note}]` · append-only · สถานะขั้น: waiting / pending / approved / rejected / skipped · **ใช้ render ช่องลายเซ็น PDF** |
| `approved_at` | `approved_at` | timestamptz | YES | |
| (เหตุผล) | `reject_reason` · `cancel_reason` | text | YES | บังคับเมื่อ reject/cancel |

| BR-DOA | F-HR-OSW | อ้าง |
|---|---|---|
| BR-DOA-01 ส่งได้เฉพาะ draft | ✅ | BR-OSW-13 · FN-08 · 422 BR_NOT_DRAFT |
| BR-DOA-02 resolve ตอนส่งแล้ว freeze | ✅ | BR-OSW-09 · FN-08 |
| BR-DOA-03 reject → กลับ draft แก้ได้ | ⚠️ **ต่างจากมาตรฐานโดยมติ DA (DEC-10):** reject = จบใบ · ผู้ขอทำซ้ำเป็นใบใหม่ · ประวัติ append-only | 05 §5.2 · 07 §7.0 |
| BR-DOA-04 ผู้ขออนุมัติเองไม่ได้ | ✅ | BR-OSW-11 · 422 BR_SOD_SELF_APPROVER |
| BR-DOA-05 แก้ยอดหลังส่ง → re-resolve | ไม่ใช้ (ไม่มีวงเงิน · แก้หลังส่งไม่ได้) | BR-OSW-13 |

## §5 UI Contract สำหรับ HTML (ตรวจกับ HTML รอบ 4 · UI Brief §6/§8)
| ส่วน | สถานะ | Anchor |
|---|---|---|
| ปุ่มส่งขออนุญาต | ✅ เฉพาะ draft + เจ้าของ | `#btnSaveSubmit` · `#btnSubmitView` → `openSubmit()` |
| Slot picker ต่อขั้น | ✅ 1 แถวต่อขั้น · ค่าเริ่มจาก resolve · ไม่มีผู้ขอในรายชื่อ · บังคับเลือก | M-01 `.slot-row` · `#fSlot{i}` · `resolveDoa()` |
| Badge สถานะ | ✅ | `docPill()` |
| Approval Timeline | ✅ แท็บ ลายเซ็น / อนุมัติ (ขั้น · role · คน · สถานะ · เวลา · ความเห็น) | `renderSignTab()` |
| ปุ่มอนุญาต / ไม่อนุญาต | ✅ เฉพาะผู้พิจารณาขั้นปัจจุบัน · ไม่อนุญาตบังคับเหตุผล | `canAct()` · `confirmApprove()` · `confirmReason()` |
| My Approval hook | ✅ การ์ด "รอฉันพิจารณา" + badge เมนู (prototype) · ระบบจริง = กล่อง My Approval + callback API-13 | `RECS.filter(canAct)` |
| ช่องลายเซ็น PDF | ✅ ผู้ขอ + 1 ช่องต่อขั้น (thai-doc B6 แถวล่าง) · ตาม `sign_boxes` | `oswPdfData().signs` |
| Mock | ✅ ตาม pattern ที่ skill กำหนด (ไม่มี array ชื่อตำแหน่งตายตัว) | `MOCK_DOA_RESOLVED` (DOA-ENGINE-HOOK) |

## §6 Wire Checklist
- [ ] DOA owner: ตรวจว่า `role-line-manager` (ผู้บังคับบัญชาตรงจากผังองค์กร) ใช้ได้ใน DOA กลาง
- [ ] ตั้ง entry `osw` ตาม §3
- [ ] BE: API-05 resolve · API-06 submit (snapshot) · API-07/08 decide · API-09 cancel · API-13 callback (sequential · ignore เมื่อไม่ pending)
- [ ] BE: ใบ `pending_approval` โผล่ใน My Approval ของผู้พิจารณาขั้นปัจจุบัน
- [ ] FE: แทน `MOCK_DOA_RESOLVED` / `resolveDoa()` ด้วย API-05
- [ ] toggle `wire_status: pending → wired`

## §7 Open Questions
ไม่มีค้าง ✅ (ปิดตามมติ DA 5 ต.ค. 2569: dynamic · ไม่มีวงเงิน · reject จบใบ · HR รับทราบ = เพิ่มขั้นที่ DOA กลาง)

## Quality Gate
| # | เช็ค | ผล |
|---|---|:---:|
| G1 | role เป็น `role-*` เท่านั้น | ✅ `role-line-manager` (ไฟล์ master `doa-contract.md` ไม่มีในสกิลที่ติดตั้ง — ตรวจที่ DOA กลางใน §6) |
| G2 | ทุก set มี amount_from / amount_to | ✅ |
| G3 | ช่วงต่อเนื่องไม่ทับไม่มีรู | ✅ (set เดียว) |
| G4 | set สุดท้าย `amount_to: null` | ✅ |
| G5 | approval_scope อยู่ใน 3 ค่า | ✅ `document_sign` |
| G6 | ไม่มีค่าที่ยังไม่ยืนยันซ่อนอยู่ | ✅ ไม่มี [DEFAULT] |
| G7 | ไม่มีสายอนุมัติ hardcode ใน FRD/HTML | ✅ FRD อ้าง resolve เท่านั้น · HTML ใช้ `MOCK_DOA_RESOLVED` ตาม pattern |
**Verdict: PASS**
