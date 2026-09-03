# STANDARD_BASELINE — F-HR-RECRUIT · สรรหา
> S0.5 · Odoo Recruitment · Dynamics 365 (Attract/Talent) · SAP SuccessFactors Recruiting → matrix + lifecycle + archetype

## 1. Capability matrix (MUST = ทั้ง 3 ค่ายมี)
| # | Capability | Odoo | D365 | SAP SF | CUBE-fit | เหตุผล |
|---|---|---|---|---|---|---|
| 1 | เปิดอัตรา (job requisition) | ✓ | ✓ | ✓ | **MUST** | ต้นทางการสรรหา · อ้าง Manpower (hook) |
| 2 | ประกาศรับ (job posting internal) | ✓ | ✓ | ✓ | **MUST** | ภายใน · external board = hook |
| 3 | คลังผู้สมัคร (candidate pool/db) | ✓ | ✓ | ✓ | **MUST** | core master |
| 4 | รับใบสมัคร (application) | ✓ | ✓ | ✓ | **MUST** | ผูกกับอัตรา |
| 5 | pipeline stages/บอร์ด (คัดกรอง→สัมภาษณ์→ข้อเสนอ) | ✓ kanban | ✓ | ✓ | **MUST** | archetype pipeline board |
| 6 | นัดสัมภาษณ์ (interview scheduling) | ✓ | ✓ | ✓ | **MUST** | + NTF |
| 7 | ประเมินผู้สมัคร (scorecard/evaluation) | ✓ | ✓ | ✓ | **MUST** | ต่อผู้สัมภาษณ์ |
| 8 | ข้อเสนอจ้าง + อนุมัติ (offer + approval) | ✓ | ✓ | ✓ | **MUST** | = **DOA** |
| 9 | ส่งต่อ onboarding (hire handoff) | ✓ | ✓ | ✓ | **MUST** | → On/Offboard (ไม่ทำเอง) |
| 10 | PDPA/ความยินยอม + retention | △ | ✓ | ✓ GDPR | **MUST** | = **CSQ SecC** |
| 11 | แจ้งเตือน (นัด/ผล/ข้อเสนอ) | ✓ | ✓ | ✓ | **MUST** | ENG-NOTIFY |
| 12 | audit + masking ข้อมูลผู้สมัคร | — | ✓ | ✓ | **MUST** | RESTRICTED |
| 13 | ตรวจซ้ำ/เคยสมัคร (duplicate/rehire) | ✓ | ✓ | ✓ | SHOULD | ค้น pool |
| 14 | รายงาน funnel/time-to-hire | ✓ | ✓ | ✓ | SHOULD | report tab |
| 15 | ต้นทุนสรรหา (recruitment cost) | △ | ✓ | ✓ | SHOULD [AI-DRAFT] | CSQ EC (optional) |
| 16 | job board ภายนอก (external posting) | ✓ | ✓ | ✓ | SKIP→hook | integration ภายนอก |
| 17 | assessment/แบบทดสอบ · sourcing agency | ✓ | ✓ | ✓ | NICE→ไม่รองรับ | OQ |

**MUST = 12 (≥5 ✅)**

## 2. Lifecycle
**Requisition:** ร่าง → อนุมัติเปิด(open·DOA) → ประกาศ(posted) → สรรหา(sourcing) → ปิด(filled/closed/cancelled)
**Candidate:** สมัคร(applied) → คัดกรอง(screening) → สัมภาษณ์(interview) → ข้อเสนอ(offer·DOA) → รับ(hired→onboarding) · เส้นแยก: ไม่ผ่าน(rejected) · ถอนตัว(withdrawn) · เก็บ pool(talent pool)
actor: HR สรรหา · hiring manager (ประเมิน/อนุมัติ) · ผู้สมัคร (ตอบรับ) — **≥3 state ✅**

## 3. Archetype + surfaces
- **archetype = master + pipeline board** (Pattern L collection/kanban สำหรับ candidate stages · master สำหรับ requisition/candidate)
- surfaces: สร้าง ✓ (req+candidate) · ส่ง ✓ (offer) · เซ็น/อนุมัติ ✓ (DOA offer+req) · PDF ✗ (offer letter soft ref รอบนี้) · เตือน ✓ (NTF) · รายงาน ✓ (funnel)

## 4. Declarations: doa ✓ · ntf ✓ · csq ✓ (**SecC** PDPA + EC optional) · doccfg ✗ · pdfdoc ✗

## 5. scope ตัด แต่ MUST → OQ
- external job board / offer letter PDF = hook/soft-ref (ไม่ block · A-REC-03) · assessment/sourcing agency = NICE ไม่รองรับ
