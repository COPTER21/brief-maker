# STANDARD_BASELINE — F-HR-WELFARE · สวัสดิการ (Welfare)
> S0.5 · baseline mode · เทียบ Odoo (HR/Insurance/Meal) · Dynamics 365 HR (Benefits management) · SAP SuccessFactors (Employee Central Benefits) → capability matrix + lifecycle + archetype ยืนยัน
> grounding: D365 Benefits management (Plan type→Plan→Option · eligibility rules · personal-contact/dependent eligibility · enroll workers/ESS · beneficiaries)

## 1. Capability matrix (แถว = ความสามารถ · MUST = ที่ทั้ง 3 ค่ายมีเหมือนกัน)
| # | Capability | Odoo | D365 | SAP SF | CUBE-fit | เหตุผล / มติ |
|---|---|---|---|---|---|---|
| 1 | ทะเบียนประเภทสวัสดิการ (benefit type/plan catalog) | △ (custom/Insurance/Meal) | ✓ Plan type→Plan→Option | ✓ Benefit types | **MUST** | core master ของ feature (archetype master) |
| 2 | เกณฑ์สิทธิ์ตามกลุ่มพนักงาน (eligibility rule) | △ | ✓ eligibility rules | ✓ eligibility criteria | **MUST** | scope note "ต่อกลุ่มพนักงาน" · อ้าง Employee Master group |
| 3 | วงเงิน/โควตาต่อปีต่อคน (coverage limit/quota) | △ | ✓ coverage amount | ✓ entitlement/limit | **MUST** | scope note "วงเงิน/โควตาต่อปีต่อคน" |
| 4 | คำขอใช้สิทธิ์/ลงทะเบียน (enrollment/claim request) | △ (Expenses) | ✓ enroll + ESS | ✓ enrollment + claim | **MUST** | transaction ของ feature |
| 5 | อนุมัติคำขอ (approval workflow) | ✓ | ✓ | ✓ | **MUST** | = **DOA engine** ประกาศ ไม่ทำเอง (doa) |
| 6 | ผู้ติดตาม/ผู้รับผลประโยชน์ (dependents/beneficiaries) | △ | ✓ personal-contact eligibility + beneficiary | ✓ dependents | **MUST** | scope note "คู่สมรส/บุตร" (A-WEL-04 เก็บใน Welfare) |
| 7 | บัญชีการใช้ + คงเหลือต่อปี (usage/balance ledger) | △ | ✓ | ✓ | **MUST** | scope note "บันทึกการใช้ + คงเหลือ" · append-only |
| 8 | ช่วงสิทธิ์มีผล (effective dating ของสิทธิ์) | △ | ✓ enrollment dates | ✓ | **MUST** | HR-1 effective_date · อ้าง HR Config pattern |
| 9 | แนบเอกสารหลักฐานคำขอ (attachment) | ✓ | ✓ | ✓ | **MUST** | ใบเสร็จ/หลักฐานการใช้สิทธิ์ |
| 10 | ปิดบังข้อมูลอ่อนไหว (masking RESTRICTED) | — | ✓ | ✓ | **MUST** | Policy Center · ข้อมูลบุคคล RESTRICTED |
| 11 | มูลค่าสวัสดิการ = ผลได้/ฐานภาษีพนักงาน (cost/value tracking) | △ | ✓ | ✓ | **MUST** | → **CSQ EC** (มูลค่าสวัสดิการกระทบเงินได้) |
| 12 | แจ้งเตือน (ยื่น/ผล/ใกล้หมดสิทธิ์-โควตา) | ✓ | ✓ | ✓ | **MUST** | = **ENG-NOTIFY** ประกาศ (ntf) |
| 13 | เริ่ม/สิ้นสุดสิทธิ์อัตโนมัติตามเข้า-ออกงาน (life event join/leave) | — | ✓ life events | ✓ event-driven | SHOULD | hook On/Offboard signal (joiner/leaver) |
| 14 | เปลี่ยนกลางปีตามเหตุการณ์ชีวิต (marriage/childbirth → เปิดสิทธิ์) | — | ✓ | ✓ | SHOULD [AI-DRAFT] | reason ของคำขอเปลี่ยนสิทธิ์ |
| 15 | รอบเปิดลงทะเบียน (open enrollment window) | — | ✓ | ✓ | SHOULD [AI-DRAFT] | period อ้าง HR Config |
| 16 | รายงานการใช้สิทธิ์ตามแผน/กลุ่ม/ต้นทุน | ✓ | ✓ | ✓ | SHOULD | report tab ในหน้า |
| 17 | จ่ายเงินคืน/เบิกจริง (reimbursement payout) | ✓ Expenses | ✓ payroll integ | ✓ reimbursement | **SKIP→OQ** | scope ตัด — hook Payroll/Expense (A-WEL-02) |
| 18 | หักเงินสมทบผ่านเงินเดือน (payroll deduction) | — | ✓ | ✓ | **SKIP→hook** | Payroll PS-1/HK-1 hook display-only |
| 19 | จัดการผู้ให้บริการ (provider/vendor: รพ./ประกัน) | — | ✓ | ✓ | NICE→ไม่รองรับ | OQ · ไม่อยู่ scope รอบนี้ |
| 20 | สวัสดิการยืดหยุ่น/แต้ม (flex credits) | — | ✓ | ✓ | NICE→ไม่รองรับ | OQ |

**MUST = 11 ข้อ (≥5 ✅)**

## 2. Lifecycle มาตรฐาน (state machine + actor + เอกสาร)
**2a. Benefit plan (master):** `ร่าง` → `เผยแพร่/มีผล (effective_date)` → `แทนที่ด้วยเวอร์ชันใหม่/ปิดใช้` — actor: HR Admin · ไม่มีเอกสารที่คนถือ (∴ ไม่ต้อง doccfg/pdfdoc)
**2b. Benefit request/enrolment (transaction):**
`ร่าง` → `ยื่น (submitted)` → `รออนุมัติ (DOA)` → **[approved]** `อนุมัติ → บันทึกการใช้ + ตัดคงเหลือ (recorded/active)` → `สิ้นสุด/หมดอายุ (closed)`
เส้นแยก: `ไม่อนุมัติ (rejected)` · `ยกเลิก (cancelled)` · `สิ้นสุดสิทธิ์เพราะพ้นสภาพ (revoked by leaver signal)`
actor: พนักงาน/HR (ยื่น) · หัวหน้า→HR (DOA อนุมัติ) · ระบบ (ตัดคงเหลือ · เตือน) — **≥3 state ✅ (6 state)**

## 3. Archetype ที่ควรใช้ + surfaces
- **archetype = master** (ทะเบียนสิทธิ์ CRUD) **+ light transaction** (คำขอ→อนุมัติ→บันทึก) ในหน้าเดียว 4 tabs · **ยืนยันตาม LANE_BRIEF (ไม่เปลี่ยน)**
- html-generator-v9 pattern: A (list) + B (create/edit drawer) + C (view drawer tabbed) + D (confirm อนุมัติ/ยกเลิก) · **ไม่ใช่ Pattern Q** (ไม่มีเอกสารเลขรัน/PDF)
- surface ที่ต้องมี: **สร้าง** ✓ (benefit type + request) · **ส่ง** ✓ (submit request) · **เซ็น/อนุมัติ** ✓ (DOA) · **PDF** ✗ (ไม่มีเอกสารทางการ) · **เตือน** ✓ (NTF) · **รายงาน** ✓ (usage report tab)

## 4. Declarations (ยืนยัน chip)
doa ✓ (approval) · ntf ✓ (submit/result/near-limit) · csq ✓ **EC เท่านั้น** (มูลค่าสวัสดิการ) · doccfg ✗ · pdfdoc ✗

## 5. scope note ตัด แต่ standard = MUST → OQ (ห้ามตัดเงียบ)
- **OQ A-WEL-02** จ่ายเงินคืน/หักผ่านเงินเดือน (standard MUST cap.17/18) — CUBE ตัดออก จ่ายจริงที่ Expense Claim/Payroll → รอบนี้ **hook display-only** · owner Strike
- provider management (cap.19) · flex credits (cap.20) = NICE → "ไม่รองรับ" + OQ (ไม่ critical)
