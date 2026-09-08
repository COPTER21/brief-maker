# PREBRIEF · Welfare — สวัสดิการ
archetype_confirmed: master  (master ทะเบียนสิทธิ์ + light transaction คำขอใช้สิทธิ์/คงเหลือ · ยืนยันตาม STANDARD_BASELINE §3 — ไม่ใช่ Pattern Q เพราะไม่มีเอกสารเลขรัน/PDF)
source: LANE_BRIEF.md + STANDARD_BASELINE.md (MUST 11 · lifecycle 6 state) · dep contracts CONFIG/ONBOARD/PAYROLL
lang: business ไทยล้วน · [แผน]/[มติ]/[AI-DRAFT]/[STD]/[ASSUMED]

## 0. Obligations — พันธะจากต้นทาง
| # | พันธะ | จาก | ถูกตอบที่ § |
|---|---|---|---|
| OB-1 | อ่านกลุ่มพนักงาน/คน = soft ref Employee Master (snapshot ชื่อ) | LD-4C-02 · CONTEXT_PACK | §3.4, S-05, BR-10 |
| OB-2 | เริ่ม/สิ้นสุดสิทธิ์ตาม On/Offboard signal (joiner/leaver · null≠ไม่มีวันจบ) | F-HR-ONBOARD §0.13 | S-13, S-15, BR-06 |
| OB-3 | จ่ายเงินจริง = hook display-only ไป Payroll PS-1/Expense (ไม่จ่ายเอง) | scope note · F-HR-PAYROLL | S-14, §9, "ไม่รองรับ" |
| OB-4 | อนุมัติคำขอ = DOA engine (GET /doa/resolve · slot picker มติ 17ส.ค.) | current-state §3 | S-07, BR-04, §12 |
| OB-5 | policy/effective_date/company_scope = อ่าน HR Configuration (#107) | HR-1 | §3.4, BR-03 |
| OB-6 | มูลค่าสวัสดิการกระทบเงินได้พนักงาน → CSQ EC | STANDARD_BASELINE cap.11 | BR-09, §12 |
| OB-7 | audit append-only · ไม่มี hard delete · RESTRICTED masking | current-state §3 | BR-07, BR-08 |

## 1. สรุป + ผู้ใช้ + สิทธิ์
- **ทำอะไร:** ทะเบียนสิทธิ์สวัสดิการต่อกลุ่มพนักงาน (โควตา/วงเงินต่อปีต่อคน) + ผู้ติดตาม + คำขอใช้สิทธิ์ → อนุมัติ → บันทึกการใช้ + คงเหลือ · **ไม่จ่ายเงินเอง**
- **ผู้ใช้:** HR Welfare Admin (จัดการทะเบียน/อนุมัติ) · หัวหน้า (อนุมัติชั้นต้น · DOA) · พนักงาน (ยื่นคำขอ — ผ่าน ESS ภายหลัง · รอบนี้ HR ยื่นแทนได้)
- **สิทธิ์:** ข้อมูลบุคคล/ผู้ติดตาม/มูลค่า = RESTRICTED · role จาก login (ไม่มี persona switch · demo = .demo-strip #105)

## 2. Scenarios (derive D1-D6 · Happy/Alt/Exception)
> D1 ปริมาณ=โควตา/วงเงิน · D2 state=คำขอ+benefit type · D3 อนุมัติ=DOA · D4 อ้างอิง=employment window/config · D5 ปลายทาง=hook จ่าย+CSQ · D6 STD=life event/open enrol
| S-XX | ประเภท | เรื่อง | ข้อมูลที่ต้องมี |
|---|---|---|---|
| S-01 | Happy | สร้างประเภทสวัสดิการ (benefit type) กำหนดกลุ่มมีสิทธิ์ + โควตา/วงเงินต่อปี + effective_date | ชื่อ · หมวด · หน่วยนับ(ครั้ง/บาท) · กลุ่มพนักงาน · โควตา/วงเงิน/ปี · ครอบผู้ติดตาม? · effective_date · company_scope |
| S-02 | Alt | แก้ประเภท = ออกเวอร์ชันใหม่ (effective_date ใหม่ · เก่ายังอ้างได้) | version_id · [effective_date, effective_to] ไม่ทับ [STD P-3] |
| S-03 | Alt | ปิดใช้ประเภท (soft archive) — คำขอเก่ายังอ่านได้ | reason · archived_at · ห้าม hard delete |
| S-04 | Exception | โควตา/วงเงิน ≤0 หรือช่วง effective ทับกัน → บล็อก+เหตุ | validation message |
| S-05 | Happy | เพิ่มผู้ติดตาม (คู่สมรส/บุตร) ให้พนักงาน + ความสัมพันธ์ + สถานะใช้สิทธิ์ | ชื่อ · ความสัมพันธ์ · วันเกิด · ใช้สิทธิ์ได้? |
| S-06 | Exception | ผู้ติดตามเกินจำนวน/อายุบุตรเกินเกณฑ์กลุ่ม → เตือน/บล็อกตามนโยบาย | เกณฑ์จาก benefit type · message |
| S-07 | Happy | ยื่นคำขอใช้สิทธิ์ (ตัวเอง/ผู้ติดตาม) เลือก type ที่มีสิทธิ์ + จำนวน/มูลค่า + แนบหลักฐาน → DOA → อนุมัติ → ตัดคงเหลือ | ผู้ขอ · type · ผู้ใช้สิทธิ์(คน/ผู้ติดตาม) · จำนวน/มูลค่า · แนบไฟล์ · วันที่ · เหตุผล |
| S-08 | Alt | ใช้สิทธิ์บางส่วน — โควตาเหลือ ใช้ต่อรอบหน้าได้ (balance ถูกต้อง) | ยอดใช้สะสม · คงเหลือ · ledger entry |
| S-09 | Exception | ใช้เกินคงเหลือ/วงเงิน → บล็อก + แสดงยอดคงเหลือ | คงเหลือ · จำนวนที่ขอ · BR-02 |
| S-10 | Exception | ยื่น type ที่ไม่มีสิทธิ์ (นอกกลุ่ม/นอกช่วง/พ้นสภาพ) → บล็อก | eligibility resolve result · เหตุ |
| S-11 | Alt | DOA ไม่อนุมัติ (rejected) → ไม่ตัดคงเหลือ + แจ้งเหตุ + เตือนผู้ยื่น | ผู้อนุมัติ · เหตุผล · แจ้งเตือน |
| S-12 | Alt | ยกเลิกคำขอก่อนอนุมัติ (cancelled) — ไม่กระทบคงเหลือ | สถานะ · ผู้ยกเลิก |
| S-13 | Exception | สิทธิ์สิ้นสุดเพราะพ้นสภาพ (leaver signal) → คำขอค้างระงับ + คงเหลือหยุด (revoked) | leaver effective_date · คำขอค้าง |
| S-14 | Alt | จ่ายผ่าน Payroll/Expense = hook display-only — Welfare แสดง "รอจ่าย/ส่งจ่ายแล้ว" อ่านจาก hook ไม่ CRUD | hook status [ASSUMED contract A-WEL-02] |
| S-15 | Happy | joiner signal → พนักงานใหม่เข้ากลุ่ม → สิทธิ์เปิดอัตโนมัติ [STD cap.13] | joiner effective_date · กลุ่ม |
| S-16 | Alt | รายงานการใช้สิทธิ์ตามแผน/กลุ่ม/ช่วงเวลา + filter (report tab) | มิติ: type/กลุ่ม/ช่วง · ยอดใช้/คงเหลือ/มูลค่า |

## 3. Data — full data dict
### 3.1 Header (คำขอใช้สิทธิ์)
| field | ชนิด | บังคับ | ที่มา |
|---|---|---|---|
| request_no | text (แสดง · ไม่ใช่เลขรันทางการ) | auto | ภายใน (ไม่ doccfg) |
| ผู้ยื่น | ref Employee (snapshot ชื่อ/ตำแหน่ง/แผนก) | ✓ | Employee Master [OB-1] |
| ผู้ใช้สิทธิ์ | เลือก: ตัวเอง / ผู้ติดตาม | ✓ | §3 dependents |
| benefit_type | ref (เฉพาะที่มีสิทธิ์ ณ วันยื่น) | ✓ | master §3 · resolve BR-01 |
| จำนวน/มูลค่า | number | ✓ | ≤ คงเหลือ BR-02 |
| วันที่ใช้สิทธิ์ | date (พ.ศ.) | ✓ | — |
| เหตุผล/รายละเอียด | text | ตามนโยบาย | — |
| แนบหลักฐาน | file[] | ตาม type | — |
| สถานะ | enum §5 | auto | state machine |
| config_version_id | snapshot | auto | HR Config resolve [OB-5] |

### 3.2 Lines — ไม่มี grid B2 (feature master · คำขอ 1 รายการต่อใบ) · ผู้ติดตามหลายคนเป็น sub-list ของพนักงาน ไม่ใช่ line เอกสาร
### 3.3 Computed / แสดงอย่างเดียว
คงเหลือ = โควตา/วงเงินต่อปี − ยอดใช้อนุมัติสะสม (ต่อคน·ต่อ type·ต่อปีสิทธิ์) · มูลค่าสวัสดิการสะสม (→CSQ) · สถานะจ่าย (hook อ่านจาก Payroll/Expense S-14)
### 3.4 Config ที่ feature นี้อ่าน (ไม่ CRUD · #107)
- HR Configuration `resolve(date, company_id)` — company_scope · ปฏิทิน/ปีสิทธิ์ · **[ASSUMED A-WEL-01: welfare_type ยังไม่ใช่ group ใน HR Config → benefit master เป็นของ Welfare เอง ใช้ pattern effective_date]**
- Employee Master — คน/ตำแหน่ง/แผนก/กลุ่ม (combobox #102 · avatar→ชื่อ→ตำแหน่ง·แผนก)
- On/Offboard `employment-window/resolve?include=signal` — joiner/leaver

## 4. Business Rules
| BR | กฎ | trace |
|---|---|---|
| BR-01 | สิทธิ์ = ต้องอยู่ในกลุ่มที่ benefit type กำหนด ณ วันยื่น (eligibility resolve) | S-07,S-10 |
| BR-02 | โควตา/วงเงินต่อปีสิทธิ์ต่อคน — ใช้เกินคงเหลือ = บล็อก | S-08,S-09 |
| BR-03 | benefit type ทุกเวอร์ชันมี effective_date · ช่วงไม่ทับ (HR-1 · P-3 pattern) | S-01,S-02,S-04 |
| BR-04 | คำขอผ่าน DOA ก่อนตัดคงเหลือ — GET /doa/resolve ไม่ hardcode chain (มติ 17ส.ค. slot picker) | S-07,S-11 |
| BR-05 | ตัดคงเหลือเฉพาะเมื่อ approved · reject/cancel/revoke ไม่ตัด | S-07,S-08,S-11,S-12 |
| BR-06 | ช่วงสิทธิ์ผูก employment window (joiner เปิด · leaver ปิด) · null≠"ไม่มีวันจบ" | S-13,S-15 |
| BR-07 | balance ledger + คำขอ = append-only · audit ทุก create/approve/แก้/ยกเลิก · soft archive | S-03,ทุก S |
| BR-08 | ข้อมูลบุคคล/ผู้ติดตาม/มูลค่า = RESTRICTED masking Policy Center | ทุก S |
| BR-09 | มูลค่าสวัสดิการที่อนุมัติ = ผลได้พนักงาน → ยิง CSQ EC (welfare.granted) | S-07 · §12 |
| BR-10 | snapshot ชื่อคน/บริษัท/config_version ณ เวลาบันทึก (soft ref LD-4C-02) | ทุก S |

## 5. State Machine
**คำขอใช้สิทธิ์:** `ร่าง(draft)` → `ยื่น(submitted)` → `รออนุมัติ(pending_approval·DOA)` → `อนุมัติ+บันทึกใช้(approved/recorded)` → `ปิด(closed)`
เส้นแยก: `ไม่อนุมัติ(rejected)` ← pending · `ยกเลิก(cancelled)` ← draft/submitted · `ระงับเพราะพ้นสภาพ(revoked)` ← ทุกสถานะก่อน closed (leaver)
**Benefit type (master):** `ร่าง` → `มีผล(active·effective_date)` → `แทนที่/ปิดใช้(superseded/archived)`
ทุก transition มีผู้กด: HR (สร้าง/แก้/ปิด) · ผู้ยื่น (ยื่น/ยกเลิก) · DOA approver (อนุมัติ/ไม่อนุมัติ) · ระบบ (revoke จาก leaver · ตัดคงเหลือ)

## 6. Actions ต่อหน้า (4 tabs · 1 เมนูซ้าย #104)
- Tab **ทะเบียนสวัสดิการ**: สร้าง/แก้(เวอร์ชัน)/ปิดใช้ benefit type · list + drawer
- Tab **คำขอใช้สิทธิ์**: สร้างคำขอ · ส่งอนุมัติ · ยกเลิก · ดูสถานะ+DOA chain · view drawer tabbed (รายละเอียด›หลักฐาน›คงเหลือ›ประวัติ)
- Tab **คงเหลือรายคน**: ค้นคน → เห็นสิทธิ์/โควตา/ใช้/คงเหลือต่อ type + ผู้ติดตาม
- Tab **รายงาน**: การใช้สิทธิ์ตามแผน/กลุ่ม/ช่วง (S-16)
- ปุ่มอนุมัติ = DOA confirm (Pattern D) · ยกเลิก/ปิด = confirm + soft archive

## 7. Data behaviour
คงเหลือคำนวณสด จาก ledger (ไม่เก็บซ้ำ) · แก้ benefit type ไม่ย้อนกระทบคำขอที่อนุมัติแล้ว (snapshot version) · จ่ายเงิน = อ่าน hook ไม่เขียน

## 8. Mock Data Spec (prove ทุก scenario)
- 4 benefit type: ประกันสุขภาพ(วงเงิน 30,000/ปี ครอบผู้ติดตาม) · ตรวจสุขภาพประจำปี(1 ครั้ง/ปี) · ค่าเล่าเรียนบุตร(20,000/ปี) · กองทุนสำรองเลี้ยงชีพ(สมัคร%) — effective 1 ม.ค. 2569
- 3 กลุ่มพนักงาน: พนักงานประจำ · ทดลองงาน(สิทธิ์จำกัด) · รายวัน(ไม่มีสิทธิ์บางตัว → S-10)
- พนักงาน 6 คน (1 มีผู้ติดตาม 2 · 1 ทดลองงาน · 1 กำลังพ้นสภาพ → S-13 · 1 joiner ใหม่ → S-15)
- คำขอ: อนุมัติแล้วบางส่วน(S-08) · เกินวงเงิน(S-09) · รออนุมัติ · ถูกปฏิเสธ(S-11) · ส่งจ่าย Payroll(S-14)
- วันที่ทั้งชุด = พ.ศ. (2569)

## 9. Edges + Hotspot + ผลปลายทาง
- leaver ระหว่างคำขอค้าง → revoke (S-13) · null last-day ≠ ยังทำงาน (BR-06)
- ปลายทาง: อนุมัติ → CSQ EC (มูลค่า) + hook จ่าย (Payroll/Expense display-only) + NTF ผู้ยื่น
- hotspot: eligibility resolve ผิดกลุ่ม/ผิดช่วง = บล็อกเงียบไม่ได้ ต้องบอกเหตุ (S-10)

## 10. OQ + [AI-DRAFT] register → pin
| id | เรื่อง | default | owner |
|---|---|---|---|
| A-WEL-01 | benefit master เป็นของ Welfare (ไม่ใช่ HR Config group) | ใช้ pattern effective_date เอง | Strike |
| A-WEL-02 | จ่ายเงินผ่าน Payroll/Expense = hook display-only | hook + [ASSUMED contract รอ FRD Phase B] | Strike |
| A-WEL-03 | DOA คำขอใช้สิทธิ์ ไม่มีวงเงิน สายเดียว | หัวหน้า→HR ตามตำแหน่ง | พี่เบิร์ด |
| A-WEL-04 | ผู้ติดตามเก็บใน Welfare | ชื่อ·ความสัมพันธ์·วันเกิด·สถานะใช้สิทธิ์ | Strike |
| A-WEL-05 | open enrolment window / life-event change | [AI-DRAFT] reason ของคำขอ · window อ้าง HR Config | Strike |

## 11. Coverage Matrix (ledger — gate)
| S-XX | BR | transition | หน้าจอ/field | FN |
|---|---|---|---|---|
| S-01 | BR-03 | type:ร่าง→มีผล | Tab ทะเบียน · drawer สร้าง | FN-01 |
| S-02 | BR-03 | type:มีผล→superseded | drawer แก้(เวอร์ชัน) | FN-02 |
| S-03 | BR-07 | type→archived | ปิดใช้ + confirm | FN-03 |
| S-04 | BR-03 | — | validation | FN-04 |
| S-05 | BR-10 | — | Tab คงเหลือ · sub-list ผู้ติดตาม | FN-05 |
| S-06 | BR-01 | — | validation ผู้ติดตาม | FN-06 |
| S-07 | BR-01,04,05,09 | คำขอ:ร่าง→approved | Tab คำขอ · สร้าง+ส่งอนุมัติ | FN-07,FN-08,FN-13 |
| S-08 | BR-02,05 | approved(บางส่วน) | คงเหลือ ledger | FN-09 |
| S-09 | BR-02 | บล็อก | validation | FN-10 |
| S-10 | BR-01,06 | บล็อก | eligibility resolve | FN-11 |
| S-11 | BR-04,05 | pending→rejected | DOA result + NTF | FN-14 |
| S-12 | BR-05 | →cancelled | ยกเลิกคำขอ | FN-15 |
| S-13 | BR-06 | →revoked | leaver signal | FN-16 |
| S-14 | BR-10 | — | hook สถานะจ่าย | FN-17 |
| S-15 | BR-06 | สิทธิ์เปิด | joiner signal | FN-18 |
| S-16 | BR-08 | — | Tab รายงาน + filter | FN-19 |
เงื่อนไข gate: ทุก BR ปรากฏ ≥1 scenario ✓ · ทุก transition ใน ≥1 scenario ✓ · ทุก scenario มี FN ✓

## §12 สัญญาณประกาศ (Declaration signals — S1.8 อ่าน)
| ท่อ | สัญญาณใน PREBRIEF (อ้าง S/FN) | chip | สรุป |
|---|---|---|---|
| DOA | S-07 ส่งอนุมัติคำขอใช้สิทธิ์ · **ไม่มีวงเงิน** (A-WEL-03) สายเดียวตามตำแหน่ง · GET /doa/resolve | ✓ | need |
| NTF | S-07 ยื่น · S-11 ผลอนุมัติ/ไม่อนุมัติ · ใกล้หมดโควตา · S-13 สิทธิ์สิ้นสุด (ไม่นับ doa_pending/result) | ✓ | need |
| CSQ | S-07/BR-09 มูลค่าสวัสดิการอนุมัติ = ผลได้พนักงาน → ท่อ **EC** เท่านั้น (ไม่ประกาศ OC/DC/SC) | ✓ | need |
| DOCCFG | ไม่มีเลขรัน/เอกสารทางการ | — | no |
| PDF DOC | ไม่มีแบบฟอร์มที่คนถือ/พิมพ์ | — | no |
DIVERGENCE: — (chip = detect ทุกท่อ)
