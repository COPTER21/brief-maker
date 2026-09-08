# DOA_BRIEF — F-HR-WELFARE · สวัสดิการ
> feature ประกาศเท่านั้น · **ห้าม hardcode สายอนุมัติ** — ตั้งค่าจริงที่หน้า DOA กลาง (F-DLG-001)
> สาย DOA **resolve ตอนส่ง แล้ว freeze snapshot** (BR-DOA-2 · LK-1) — แก้ DOA ทีหลังไม่กระทบใบที่ส่งไปแล้ว
> Source: FRD Pack (03_LOGIC FN-10/11 · 05_RULES BR-DOA-1..8) + `_DECISION_LOG_OQ.md` (A-WEL-03/CL-0013)

## 1. Identity
| field | value |
|---|---|
| feature_id | F-HR-WELFARE |
| name | สวัสดิการ (Welfare) |
| module | HR |
| platform | CUBE 4.0 |
| approval_scope | `policy_approve` — อนุมัติ "คำขอใช้สิทธิ์สวัสดิการ" (เชิงสิทธิ์/นโยบาย · **ไม่ใช่** document_sign · ไม่ออกเอกสารเลขรัน/ลายเซ็น PDF → DOCCFG NOT-NEEDED) |

## 2. Approval Actions
| action | trigger (อ้าง FRD) | ผล approve | ผล reject |
|---|---|---|---|
| อนุมัติคำขอใช้สิทธิ์สวัสดิการ | submit: `draft → submitted → pending_approval` (API-11 · FN-10) แล้วอนุมัติทีละขั้น (API-12 · FN-11) | **ขั้นสุดท้าย** → re-check (BR-DOA-4/FIX-02) → `approved` · ตัดคงเหลือ (live) · emit CSQ EC `welfare.granted` · pay='pending' hook · NTF `welfare_request_result` | `rejected` · **ไม่ตัดคงเหลือ** (BR-05) · reason บังคับ (VR-08) · NTF `welfare_request_result` |

> **หมายเหตุสาย 2 ขั้น (one-step advance · BR-DOA-3/FIX-03):** อนุมัติ 1 ครั้ง = เลื่อน **1 ขั้น** (current→approved, next→current) · status คง `pending_approval` จนขั้นสุดท้าย · **ห้าม collapse ทั้งสายในครั้งเดียว**.
> **Reversal (BR-11 · OQ-WEL-01):** `approved → reversed` (API-15 · FN-14) = การกลับรายการ append-only ของ HR admin/manager — **ไม่ใช่ approval step ของ DOA** (ไม่ต้องตั้ง chain แยก) · guard = `canApprove` เท่านั้น. CSQ/NTF ของ reversal ประกาศในใบ CSQ/NTF ไม่ใช่ที่นี่.

## 3. Matrix ที่จะไปตั้งค่า (กรอกลงหน้า DOA กลาง)  **[DEFAULT — รอยืนยัน role ids · A-WEL-03/CL-0013]**
| set | amount_from | amount_to | departments | chainMode | steps[roles] |
|---|---|---|---|---|---|
| default | 0 (บาท) | **null (ไม่จำกัด)** | ทุกแผนก (merged) | **sequential · 2 ขั้น** | ขั้น 1 `role-hr-line-manager` (หัวหน้าสายงาน) → ขั้น 2 `role-hr-welfare-admin` (HR สวัสดิการ) |

- **ไม่มีวงเงิน (no amount tier):** สวัสดิการ **ไม่ผูกจุดตัดยอดเงิน** — ต่างจาก Expense Claim/PR/PO ที่มี threshold · จุดตัดเดียว amount_from=0 / amount_to=null (G3/G4: ปลายเปิด ครบ ไม่มีรู ไม่ทับ).
- **ไม่มี exec-sign path:** A-WEL-03/CL-0013 default = **ไม่มีสาย CFO/ผู้บริหารเซ็นตามวงเงิน** (สวัสดิการไม่ value-tiered). ถ้าบางประเภท (เช่น กองทุน/วงเงินสูงพิเศษ) ต้องมีชั้นผู้บริหาร → **แยก set ที่หน้า DOA กลาง** (ยกเป็น OQ ด้านล่าง ไม่ตั้งเอง).
- **merged (Q3):** ทุกแผนกใช้กฎชุดเดียว — FRD ไม่ระบุแยกแผนก.
- ⚠️ **role ids ข้างต้นเป็น placeholder** สื่อความหมาย "หัวหน้าสายงาน → HR สวัสดิการ" — **ยังไม่ยืนยันกับ DOA master** (ไม่มี doa-contract.md ติดตั้งในเครื่อง) → ดู OQ §7 · BA เคาะรหัสจริงที่หน้า DOA กลาง.

## 4. Field Contract สำหรับ FRD (มีครบใน 03_LOGIC/04_DB แล้ว — ยืนยันไม่ขาด)
| field | ชนิด | nullable | หมายเหตุ |
|---|---|---|---|
| approval_status | enum | ✗ | draft \| submitted \| pending_approval \| approved \| rejected \| cancelled \| reversed \| revoked \| closed |
| doa_entry_ref | string | ✓ (Phase 1) | FK ทะเบียน DOA ของ feature นี้ |
| approval_chain / T_welfare_request_approval[] | jsonb/table | ✗ หลัง submit | **snapshot person {name, position} ตอน resolve** — append-only freeze (BR-DOA-2) |
| approver_role | string | ✗ ต่อ step | role ที่ต้องเซ็นในขั้นปัจจุบัน (resolve จาก DOA) |
| approved_by | string | ✓ | user id ผู้เซ็นจริง |
| approved_at / reversed_at / reverse_reason | timestamp/string | ✓ | reversed_at ≥ approved_at (cross-field) |
| **(ไม่มี field จำนวนเงินใน doa_resolve payload)** | — | — | **ไม่มีวงเงิน** — สายไม่เปลี่ยนตามยอด |

## 5. UI Contract สำหรับ HTML (ยืนยันตรงกับ welfare.html)
- ปุ่ม **"ส่งอนุมัติ"** → **slot picker เลือกคนในตำแหน่งจาก DOA กลาง** (avatar + ตำแหน่ง + ชื่อ · มติ 2026-08-17 · **ไม่ใช่ role id ลอย ๆ บนจอ**) · disabled ถ้าเลือกไม่ครบทุกขั้น (VR-09).
- **Approval Timeline** 2 ขั้น: role → ผู้เซ็น → เวลา → สถานะ (รอ/ผ่าน/ตีกลับ).
- ปุ่ม **"อนุมัติ / ไม่อนุมัติ"** โผล่เฉพาะผู้มีสิทธิ์ขั้นปัจจุบัน (`canApprove`) · ไม่อนุมัติบังคับใส่เหตุผล.
- ปุ่ม **"กลับรายการ"** (reversal) โผล่เฉพาะ `status==='approved' && canApprove()` — modal บังคับเหตุผล.
- Hook **"งานอนุมัติของฉัน" (My Approval):** ใบ `pending_approval` ต้องโผล่ในกล่อง My Approval.
- **ไม่มีปุ่มจ่ายจริง/execution ใน F102** (FIX-03 · no exec path) — สถานะจ่าย display-only (ปลายทาง Payroll F065).

## 6. Wire Checklist (dev)
- [ ] ตั้ง DOA entry ของ F-HR-WELFARE ที่หน้า DOA กลาง ตาม matrix §3 (2 ขั้น · no tier · no exec)
- [ ] ยืนยัน role ids จริง 2 ตัว (แทน placeholder) กับ BA
- [ ] เชื่อม `GET /doa/resolve` ตอนส่ง (API-11 · FN-10) → snapshot chain freeze
- [ ] one-step advance ต่อการกด (BR-DOA-3) · re-check ขั้นสุดท้าย (BR-DOA-4)
- [ ] My Approval hook → `wire_status: pending → wired`

## 7. Open Questions
- **OQ-DOA-01 (owner: BA / พี่เบิร์ด · BLOCKER ต่อ wire):** ยืนยัน **role id จริง 2 ตัว** ที่หน้า DOA กลาง สำหรับ "หัวหน้าสายงาน" (ขั้น 1) และ "HR สวัสดิการ" (ขั้น 2) — placeholder `role-hr-line-manager` / `role-hr-welfare-admin` **ยังไม่ verify กับ master** (ไม่มี doa-contract ในเครื่อง) → **ห้าม dev เดารหัส** (เดาผิด = ตั้งค่าสายผิดจริง).
- **OQ-DOA-02 (owner: BA):** ยืนยัน default **ไม่มีวงเงิน + ไม่มีสายผู้บริหาร** ครอบทุกประเภทสวัสดิการ — ถ้ามีประเภทพิเศษ (กองทุน/วงเงินสูง) ต้องผ่านชั้นเพิ่ม → **แยก set** (ไม่แก้ default นี้).
- **OQ-DOA-03 (owner: BA · อ้าง EC-10/OQ-02):** approver ในสายที่ freeze แล้ว ลาออก/ย้ายกลางคัน → default = ค้างขั้นนั้น + HR admin reverse/จัดการ · re-resolve กระทบสิทธิ์ = OQ.

---
_declaration รอบนี้: DOA · 2026-09-08 · Source: FRD 03_LOGIC/05_RULES/02_API + _DECISION_LOG_OQ.md (A-WEL-03/CL-0013)_
