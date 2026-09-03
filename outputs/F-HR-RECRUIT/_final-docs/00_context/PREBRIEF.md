# PREBRIEF · Recruit — สรรหา
archetype_confirmed: master  (master requisition/candidate + pipeline board · ไม่ใช่ Q-document · ยืนยันตาม STANDARD_BASELINE §3)
source: LANE_BRIEF + STANDARD_BASELINE (MUST 12)

## 0. Obligations
| # | พันธะ | จาก | § |
|---|---|---|---|
| OB-1 | ผู้สมัครที่รับ → ส่ง On/Offboard (handoff) ไม่ทำ onboarding เอง | F-HR-ONBOARD | S-10, BR-05 |
| OB-2 | PDPA ความยินยอม + retention ผู้สมัคร | CSQ SecC | S-05, BR-02, BR-06 |
| OB-3 | offer/req อนุมัติ = DOA (17ส.ค. slot picker) | current-state §3 | S-01,S-09, BR-01,04 |
| OB-4 | เปิดอัตราอ้าง Manpower (hook · null=ไม่บังคับ) | A-REC-01 | S-02, BR-08 |
| OB-5 | ข้อมูลผู้สมัคร RESTRICTED · audit append-only | current-state §3 | BR-06,07 |

## 1. สรุป + ผู้ใช้
- ทำ: สรรหา — เปิดอัตรา → pool ผู้สมัคร → pipeline (คัดกรอง/สัมภาษณ์/ข้อเสนอ) → รับ → ส่ง onboarding
- ผู้ใช้: HR สรรหา · hiring manager (ประเมิน/อนุมัติ) · ผู้สมัคร (ตอบรับ) · ข้อมูลผู้สมัคร RESTRICTED (PDPA)

## 2. Scenarios (D1-D6)
| S-XX | ประเภท | เรื่อง | ข้อมูล |
|---|---|---|---|
| S-01 | Happy | เปิดอัตรา (ตำแหน่ง·จำนวน·ระดับ·ช่วงเงินเดือน·hiring manager) → อนุมัติ DOA → ประกาศ | req fields |
| S-02 | Alt | เปิดอัตราโดยไม่มี Manpower plan [A-REC-01] → เตือน ทำได้ | hook ref |
| S-03 | Happy | เพิ่มผู้สมัครเข้า pool (ชื่อ·ติดต่อ·resume·ความยินยอม PDPA) | candidate + consent |
| S-04 | Alt | ผูกผู้สมัครกับอัตรา (application) | app link |
| S-05 | Exception | ผู้สมัครไม่ยินยอม PDPA → เก็บ/ดำเนินต่อไม่ได้จนกว่าได้ consent | consent state |
| S-06 | Happy | เลื่อนสถานะใน pipeline board (คัดกรอง→สัมภาษณ์→ข้อเสนอ) | stage |
| S-07 | Happy | นัดสัมภาษณ์ + แจ้งเตือนผู้สัมภาษณ์/ผู้สมัคร | interview slot |
| S-08 | Happy | ประเมินผู้สมัคร (scorecard ต่อผู้สัมภาษณ์) | score/comment |
| S-09 | Happy | ข้อเสนอจ้าง (offer: ตำแหน่ง·เงินเดือน·วันเริ่ม) → DOA → เสนอ | offer + chain |
| S-10 | Alt | ผู้สมัครตอบรับ (accepted) → hired → **ส่ง On/Offboard (handoff)** | handoff event |
| S-11 | Alt | ปฏิเสธ/ถอนตัว (declined/withdrawn) | reason |
| S-12 | Alt | ไม่ผ่าน (rejected) + เหตุผล → เก็บ talent pool | reason |
| S-13 | Exception | ตรวจซ้ำ/เคยสมัคร (duplicate/rehire) → เตือน | email/phone match |
| S-14 | Alt | รายงาน funnel/time-to-hire + filter | metrics |
| S-15 | Alt | ปิดอัตรา (filled/cancelled) | close |

## 3. Data
### 3.1 Requisition: id·ตำแหน่ง·จำนวน·ระดับ·ช่วงเงินเดือน(band soft ref)·hiring_manager·สถานะ·manpower_ref(hook·nullable)·อนุมัติ chain
### 3.2 Candidate: id·ชื่อ·ติดต่อ(RESTRICTED)·resume·ตำแหน่งที่สนใจ·**consent_pdpa(bool·วันที่)**·stage·score·สถานะ
### 3.3 Offer: ตำแหน่ง·เงินเดือน·วันเริ่ม·สถานะ(pending/approved/sent/accepted/declined)·chain
### 3.4 Config อ่าน (ไม่ CRUD): HR Config (ระดับ/band เงินเดือน) · Employee Master (ผู้สัมภาษณ์) · Manpower (อัตรา · hook)

## 4. Business Rules
BR-01 req อนุมัติ(DOA) ก่อนประกาศ · BR-02 เก็บผู้สมัครได้เมื่อมี consent PDPA + retention · BR-03 pipeline transition audit · BR-04 offer อนุมัติ(DOA) ก่อนเสนอ · เงินเดือนตามระดับ(band soft ref) · BR-05 hired→handoff Onboard (event · ไม่สร้าง employee เอง) · BR-06 ผู้สมัคร RESTRICTED masking·PDPA · BR-07 audit append-only·soft archive(talent pool) · BR-08 อัตราอ้าง Manpower(hook·null ไม่บังคับ) · BR-09 snapshot ผู้สัมภาษณ์ · BR-10 duplicate detect email/phone (เตือนไม่บล็อก)

## 5. State Machine
**Req:** ร่าง→อนุมัติเปิด(DOA)→ประกาศ→สรรหา→ปิด(filled/cancelled)
**Candidate:** สมัคร→คัดกรอง→สัมภาษณ์→ข้อเสนอ(DOA)→รับ(hired→onboarding) · rejected · withdrawn · talent_pool
## 6. Actions (4 tabs · 1 เมนู): ตำแหน่งที่เปิด(req) · คลังผู้สมัคร(pool) · บอร์ดสรรหา(pipeline/kanban) · รายงาน · view drawer(รายละเอียด›สัมภาษณ์/ประเมิน›ข้อเสนอ›ประวัติ) · offer submit=DOA slot
## 7. Data behaviour: consent gate ก่อนเก็บ/ดำเนินต่อ · offer เงินเดือน snapshot band · hired handoff อ่านครั้งเดียว
## 8. Mock: 3 req (เปิด/อนุมัติ/ปิด) · 6 ผู้สมัคร (ต่าง stage · 1 no-consent · 1 duplicate · 1 hired) · offer 2 · พ.ศ.
## 9. Edges: no-consent บล็อก · duplicate เตือน · เปิดอัตราไม่มี Manpower เตือน · hired→onboard handoff
## 10. OQ: A-REC-01 เปิดอัตราไม่มี MP=hook · A-REC-02 offer DOA ตามระดับ · A-REC-03 handoff Onboard=event · A-REC-04 PDPA consent+retention

## 11. Coverage Matrix
| S | BR | หน้าจอ | FN |
|---|---|---|---|
| S-01 | BR-01 | req create+DOA | FN-01,FN-08 |
| S-02 | BR-08 | manpower hook warn | FN-02 |
| S-03 | BR-02,06 | candidate+consent | FN-03,FN-05 |
| S-04 | BR-03 | application link | FN-04 |
| S-05 | BR-02 | consent gate | FN-05 |
| S-06 | BR-03 | pipeline board | FN-06 |
| S-07 | BR-03 | interview + NTF | FN-07 |
| S-08 | BR-03 | scorecard | FN-09 |
| S-09 | BR-04 | offer+DOA | FN-10,FN-08 |
| S-10 | BR-05 | hired handoff | FN-11 |
| S-11 | BR-07 | declined/withdrawn | FN-12 |
| S-12 | BR-07 | rejected+pool | FN-13 |
| S-13 | BR-10 | duplicate warn | FN-14 |
| S-14 | BR-06 | report funnel | FN-15 |
| S-15 | BR-07 | close req | FN-16 |

## §12 สัญญาณประกาศ
| ท่อ | สัญญาณ | chip | สรุป |
|---|---|---|---|
| DOA | S-01 เปิดอัตรา · S-09 ข้อเสนอจ้าง (ตามระดับ · ไม่ผูก threshold ยอดเงิน) | ✓ | need |
| NTF | S-07 นัดสัมภาษณ์ · S-09 ข้อเสนอ · ผลคัดเลือก · ผู้สมัครตอบรับ (ไม่นับ doa_*) | ✓ | need |
| CSQ | S-05/BR-02 PDPA ข้อมูลผู้สมัคร → **SecC** · ต้นทุนสรรหา → EC (optional) | ✓ | need |
| DOCCFG | ไม่มีเลขรัน | — | no |
| PDF DOC | offer letter = soft ref รอบนี้ | — | no |
DIVERGENCE: —
