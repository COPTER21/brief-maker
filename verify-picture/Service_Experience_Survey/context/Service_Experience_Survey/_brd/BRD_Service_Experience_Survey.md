# BRD: Service Experience Survey (แบบประเมินความพึงพอใจ Sales Admin — ลูกค้าต่างประเทศ)

| Field | Value |
|---|---|
| BRD ID | BRD-SAL-SEA-001 |
| Feature | F-TMP-006 Service Experience Survey (รหัสชั่วคราว — รอเลข feature จริง) |
| BRD Type | New Feature (แบบ 2 · ดึงข้อมูลเดิม — ชื่อลูกค้าจาก Customer master) |
| Version | 1.0 |
| Status | **APPROVED (Prebrief Mode · Lane · unattended)** — DEC แทน Scope Lock จนมีใบเซ็นลูกค้า · มติทุกหมวดเป็น AI-DEFAULT |
| Module | Sales (Core Cube · Sales Admin · ลูกค้าต่างประเทศ) |
| Customer | Credence (แบบฟอร์ม FM-SAL-22 Rev.00 : 01/07/2569) |
| Request | REQ-TMP-006 (ชั่วคราว — รอเลขจริงจาก F186) |
| Input | PREBRIEF_REQ-TMP-006_v2 · FORM_SPEC.json (14 ช่อง) · DECISIONS.lock (14 DEC · พร้อมเริ่มทำ) · feature.html (audit FAIL 0) |
| Created / Updated | 2026-10-11 |

## Changelog
- v1.0 (2026-10-11): สร้างผ่าน brd-generator-full v2.3 Prebrief Mode (doc-master-pipeline ขั้น 7 · โหมดไม่เฝ้า) · โครงอ้างอิงคู่ในประเทศ F-TMP-004 (FM-SAL-20) แต่ช่อง/ถ้อยคำยึด FM-SAL-22

---

## 1. Business Context
### 1.1 ปัญหา / โอกาส
ฝ่ายขายเก็บความพึงพอใจของลูกค้าต่างประเทศต่องาน Sales Admin ด้วยแบบฟอร์ม Word ภาษาอังกฤษ FM-SAL-22 "Service Experience Survey" — ให้คะแนน 1 (Very Dissatisfied) – 5 (Very Satisfied) รวม 10 หัวข้อใน 3 กลุ่ม (Communication & Responsiveness · Documentation & Execution · Professionalism) + Additional Feedback · ไฟล์กระจัดกระจาย ไม่มีเลขที่ ไม่ผูกกับลูกค้าใน Customer master · นำไปสรุปผลต้องรวบรวมเอง
### 1.2 เป้าหมาย
1. บันทึกแบบประเมินเป็นเอกสารในระบบ ช่องตรงกระดาษ 1:1 (DEC-06) — PDF Replica ภาษาอังกฤษหน้าตาเหมือน FM-SAL-22 ใน 1 หน้า
2. ผูกกับลูกค้าต่างประเทศใน Customer master + Month เพื่อสรุปผลรายเดือน/รายลูกค้า/รายกลุ่มได้ (ต่อยอดใบสรุปต่างประเทศ FM-SAL-23)
3. ผู้จัดการฝ่ายขายรู้ทันทีเมื่อมีหัวข้อที่ได้คะแนน ≤ 2 (event sea_low_score_recorded)
### 1.3 ตัวชี้วัด
ไม่มีใน input → **OQ-01** (ห้ามแต่งตัวเลข)
### 1.4 ที่มา
แบบฟอร์มลูกค้า FM-SAL-22 (docx 1 หน้า ภาษาอังกฤษ) → FORM_SPEC 14 ช่อง · gate 10 หมวด = AI-DEFAULT ทั้งหมด (โหมดไม่เฝ้า · `4_knowledge/governance/unattended-policy.md`)

## 2. Scope
### 2.1 In Scope
- รายการแบบประเมิน (segmented tabs ตามสถานะ · ค้นหา · กรองเดือน/ผู้บันทึก · CSV) · สร้าง/แก้ร่าง wizard 3 ขั้น · ดูรายละเอียด 4 แท็บ (รายละเอียด › PDF Preview › ลายเซ็น / อนุมัติ › ประวัติ)
- คะแนน 1–5 จำนวน 10 หัวข้อ 3 กลุ่ม (ข้อละ 1 คะแนน) · Additional Feedback · Company Name จาก Customer master (ต่างประเทศ) · Contact Person · Month
- บันทึกผล (ไม่มีขั้นพิจารณา — DEC-03) · ยกเลิก (เหตุผลบังคับ — G7) · แนบไฟล์ · PDF FM-SAL-22 Replica ทุกสถานะ · เลขที่ SEA จาก ENG-DOC-NUM
- แจ้งเตือน: คะแนนต่ำ → ผู้จัดการฝ่ายขาย · ยกเลิกโดยผู้อื่น → เจ้าของ (NTF_BRIEF)
### 2.2 Out of Scope
- ใบสรุปผลการประเมินต่างประเทศ (FM-SAL-23 — เอกสารอีกใบ) · แบบประเมิน/สรุปในประเทศ (FM-SAL-20/21) · ส่งแบบประเมินให้ลูกค้ากรอกเองผ่านลิงก์/พอร์ทัล · คะแนนรวม/ถ่วงน้ำหนักบนแบบพิมพ์ (กระดาษไม่มี — DEC-06) · ทำซ้ำเอกสาร (DEC-10) · ส่งต่อระบบอื่น (DEC-02) · แบบพิมพ์สองภาษา (OQ-08)
### 2.3 Assumptions
- ผู้บันทึก = เจ้าหน้าที่ Sales Admin ต่างประเทศที่รับแบบประเมินจากลูกค้า (ลูกค้าตอบทางอีเมล/ไฟล์ แล้วเจ้าหน้าที่บันทึกเข้าระบบ) → ยืนยันใน OQ-02
- Customer master แยกลูกค้าต่างประเทศได้ (OQ-04)
- ไม่มีช่องวันที่บนกระดาษ → วันที่บันทึกใช้เวลาระบบ (DEC-12)
### 2.4 Scope Lock (ชั่วคราว = DECISIONS.lock · ยังไม่มีใบเซ็น → OQ-02)
| DEC | หมวด | มติ | ที่มา |
|---|---|---|---|
| DEC-01 | G1 | ไม่เปลี่ยนค่าในระบบ | AI-DEFAULT |
| DEC-02 | G1 | ไม่ส่งต่อระบบอื่นรอบนี้ (ประกาศ event ไว้ใน FRD แต่ไม่ยิง) | AI-DEFAULT |
| DEC-03 | G2 | ไม่มีการอนุมัติ — กระดาษไม่มีช่องลงชื่อผู้อนุมัติ (สาย DOA = 0 ขั้น · ไม่มี DOA_BRIEF) | AI-DEFAULT |
| DEC-04 | G3 | ข้อละ 1 คะแนน (1 = Very Dissatisfied … 5 = Very Satisfied) · ครบ 10 ข้อจึงบันทึกผลได้ · ร่างไม่ครบได้ · Month ค่าเริ่ม = เดือนปัจจุบัน | AI-DEFAULT |
| DEC-05 | G4 | ไม่มีรายการซ้ำ (หัวข้อคงที่ 10 ข้อ) | AI-DEFAULT |
| DEC-06 | G5 | ช่องตรงกระดาษ 1:1 · ไม่เพิ่มช่อง · ป้ายภาษาอังกฤษตามกระดาษ | AI-DEFAULT |
| DEC-07 | G6 | ไม่มีช่องลงชื่อ (กระดาษไม่มี) · ไม่ใช้ภาพลายมือชื่อ | AI-DEFAULT |
| DEC-08 | G8 | เจ้าของ (ผู้บันทึก) · admin role ฝ่ายขาย (role-mgr-sales) เห็นทั้งหมด | AI-DEFAULT |
| DEC-09 | G9 | ออกเลขตอนบันทึกครั้งแรก · รหัส SEA | AI-DEFAULT |
| DEC-10 | G10 | แนบไฟล์ ✓ · ส่งออก CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗ | AI-DEFAULT |
| DEC-11 | VALID | 1 ข้อเลือกได้ 1 คะแนน · ครบ 10 ข้อจึงบันทึกผลได้ | FORM_SPEC |
| DEC-12 | VALID | ไม่มีช่องวันที่ → วันที่บันทึก = เวลาระบบ · ไม่เพิ่มช่อง | FORM_SPEC |
| DEC-13 | VALID | Month เลือกเดือน/ปี · ค่าเริ่ม = เดือนปัจจุบัน | FORM_SPEC |
| DEC-14 | VALID | ป้าย/หัวข้อ/แบบพิมพ์ภาษาอังกฤษตามกระดาษ · ปุ่ม/สถานะระบบภาษาไทย | FORM_SPEC |
G7 (ยกเลิก): เจ้าของ + admin role · สถานะร่าง/บันทึกผลแล้ว · เหตุผลบังคับ — บันทึกใน decisions.yaml (ไม่มีการอนุมัติจึงไม่ออก DEC แยก) → ใช้ใน BR-07

## 3. Roles & Permissions (COSO)
| Role | COSO | ทำอะไร |
|---|---|---|
| เจ้าหน้าที่ Sales Admin ต่างประเทศ (ผู้บันทึก) | Maker | สร้าง/แก้ร่างของตน · บันทึกผล · ยกเลิกของตน |
| role-mgr-sales (ผู้จัดการฝ่ายขาย · admin role) | Reviewer (รับทราบ) | เห็นทุกใบ · ยกเลิกได้ · รับแจ้งคะแนนต่ำ · ไม่มีขั้นพิจารณา |

| Action | Maker | role-mgr-sales | Sales Admin คนอื่น |
|---|:-:|:-:|:-:|
| ดูใบ | ของตน (ทุกสถานะ) | ทั้งหมด | ✗ |
| สร้าง/แก้ร่าง | ✓ ของตน | – | – |
| บันทึกผล | ✓ ของตน | – | – |
| ยกเลิก | ✓ ของตน | ✓ | ✗ |
| ส่งออก CSV | ใบที่เห็น | ใบที่เห็น | – |
SoD: ไม่มีขั้นพิจารณา (DEC-03) — การควบคุมคือ audit append-only + ยกเลิกต้องมีเหตุผล + ผู้จัดการรับแจ้งคะแนนต่ำ · DOA: field approver_role / approved_by / approval_chain ว่างไว้ (TODO: DOA engine — ถ้าลูกค้าเปลี่ยนมติให้มีอนุมัติ ตั้งที่ DOA กลาง)

## 4. User Journey
### 4.1 Happy Path
1. Sales Admin: สร้างแบบประเมิน → Month (เติมเดือนปัจจุบัน) → เลือก Company Name → กรอก Contact Person → ให้คะแนน 10 ข้อ (3 กลุ่ม) → Additional Feedback (ไม่บังคับ) → แนบไฟล์แบบประเมินที่ลูกค้าส่งมา (ไม่บังคับ) → ตรวจสอบ → **บันทึกผลแบบประเมิน** → ได้เลข SEA · สถานะ "บันทึกผลแล้ว"
2. มีข้อคะแนน ≤ 2 → ผู้จัดการฝ่ายขายได้รับแจ้ง (sea_low_score_recorded)
### 4.2 Alternative
- ลูกค้าตอบไม่ครบ → บันทึกแบบร่าง (ต้องมี Month + ลูกค้า + ผู้ติดต่อ) → กลับมาแก้ภายหลัง
- บันทึกผิด → ยกเลิกเอกสาร (เหตุผลบังคับ) แล้วสร้างใบใหม่ (ไม่มีทำซ้ำ — DEC-10)
```mermaid
flowchart LR
A[ร่าง] -->|บันทึกผล (ครบ 10 ข้อ)| B[บันทึกผลแล้ว]
A -->|ยกเลิก + เหตุผล| X[ยกเลิก]
B -->|ยกเลิก + เหตุผล| X
```

## 5. Data (จาก FORM_SPEC — ป้ายตามกระดาษ)
### 5.1 sales_admin_eval_ovs (header)
| ช่องบนกระดาษ | field | ชนิด | ที่มา | บังคับ |
|---|---|---|---|:-:|
| (เลขที่ — ระบบเพิ่มที่ footer) | doc_no | text | auto ENG-DOC-NUM | ✓ |
| Month | period_month | YYYY-MM | user (ค่าเริ่ม = เดือนปัจจุบัน) | ✓ |
| Company Name | customer_id → customer_name_snapshot | ref | system Customer master (อ่านอย่างเดียว) | ✓ |
| Contact Person | contact_person | text ≤ 120 (PDPA) | user | ✓ |
| Additional Feedback | comment | text ยาว | user | – |
| (ระบบ — ไม่มีบนกระดาษ) | created_at = วันที่บันทึก | timestamp | system | ✓ |
| (ระบบ · API response) | approver_role · approved_by · approval_chain | ว่าง (DEC-03 · ไม่สร้างคอลัมน์ใน DB รอบนี้) | TODO: DOA engine | – |
### 5.2 sales_admin_eval_ovs_score (10 แถวต่อใบ)
| กลุ่ม | หัวข้อ (ถ้อยคำตามกระดาษ) | q_key | score |
|---|---|---|---|
| COMMUNICATION & RESPONSIVENESS | Communication clarity | q1 | 1–5 |
| | Response time to inquiries | q2 | 1–5 |
| | Follow-up consistency | q3 | 1–5 |
| DOCUMENTATION & EXECUTION | Accuracy of documents | q4 | 1–5 |
| | Timeliness of document submission | q5 | 1–5 |
| | Shipment coordination support | q6 | 1–5 |
| | Effectiveness in resolving issues | q7 | 1–5 |
| | Proactive service updates | q8 | 1–5 |
| PROFESSIONALISM | Professionalism of our team | q9 | 1–5 |
| | Overall service satisfaction | q10 | 1–5 |
### 5.3 attachments → Document Center (ไฟล์ระดับใบ)

## 6. User Stories
| ID | Story | AC หลัก |
|---|---|---|
| S-01 | Sales Admin บันทึกแบบประเมินของลูกค้าต่างประเทศ | Month + ลูกค้า + ผู้ติดต่อ บังคับ · 10 ข้อ ข้อละ 1 คะแนน · ได้เลข SEA ตอนบันทึกครั้งแรก |
| S-02 | บันทึกเป็นร่างเมื่อลูกค้าตอบไม่ครบ | ร่างบันทึกได้แม้ไม่ครบ · บันทึกผลไม่ได้จนครบ 10 ข้อ |
| S-03 | ผู้จัดการรู้เมื่อคะแนนต่ำ | มีข้อ ≤ 2 ตอนบันทึกผล → แจ้ง role-mgr-sales · แบนเนอร์ในใบ |
| S-04 | พิมพ์/ดาวน์โหลด PDF FM-SAL-22 | ทุกสถานะ · 1 หน้า · ภาษาอังกฤษ · ✓ ในช่องคะแนนที่เลือก · Feedback ≥ 5 บรรทัด |
| S-05 | ยกเลิกใบที่บันทึกผิด | เจ้าของ/ผู้จัดการ · ร่างหรือบันทึกผลแล้ว · เหตุผลบังคับ |
| S-06 | ผู้จัดการดูทุกใบ + CSV | กรองเดือน/ผู้บันทึก/สถานะ |

## 7. Status & Lifecycle
| จาก | Action | ไป | ใคร |
|---|---|---|---|
| — | บันทึกครั้งแรก (แบบร่าง) | draft | Maker |
| — / draft | บันทึกผลแบบประเมิน (ครบ 10 ข้อ) | recorded | Maker |
| draft / recorded | ยกเลิก + เหตุผล | cancelled | Maker / role-mgr-sales |
recorded = ล็อกแก้ไข

## 8. Business Rules + Validation
| ID | Rule | Tag | Type |
|---|---|:-:|---|
| BR-01 | ข้อละ 1 คะแนนใน {1..5} | FIXED | Choice (DEC-04 · DEC-11) |
| BR-02 | บันทึกผลได้เมื่อตอบครบ 10 ข้อ · ร่างไม่ครบได้ | FIXED | Control (DEC-04) |
| BR-03 | Month บังคับ · ค่าเริ่ม = เดือนปัจจุบัน · ไม่มีช่องวันที่ (วันที่บันทึก = ระบบ) | FIXED | Validation (DEC-12/13) |
| BR-04 | คะแนน ≤ 2 = "คะแนนต่ำ" → event sea_low_score_recorded | CONFIGURABLE | Threshold (เกณฑ์ AI-DEFAULT → OQ-03) |
| BR-05 | ไม่มีขั้นพิจารณา: บันทึกผลแล้วมีผลทันที | FIXED | DEC-03 |
| BR-06 | ออกเลขตอนบันทึกครั้งแรก · no-gap ✗ | CONFIGURABLE | DOCCFG (DEC-09) |
| BR-07 | ยกเลิก: เจ้าของ + role-mgr-sales · ร่าง/บันทึกผลแล้ว · เหตุผลบังคับ | FIXED | G7 |
| BR-08 | ร่างเห็นเฉพาะเจ้าของ (+ role-mgr-sales) | FIXED | Visibility (DEC-08) |
| BR-09 | ชื่อลูกค้า snapshot ลงเอกสารตอนบันทึก | FIXED | Master ref |
| BR-10 | คะแนนเฉลี่ย = ค่าแสดงผล (list/สรุป) เท่านั้น ไม่เก็บ ไม่พิมพ์ | FIXED | DEC-06 |
| BR-11 | ป้าย/หัวข้อ/แบบพิมพ์ภาษาอังกฤษตามกระดาษ | FIXED | DEC-14 (สองภาษา → OQ-08) |
| BR-12 | Contact Person บังคับ · เป็นข้อมูลส่วนบุคคล | FIXED | DEC-06 · PDPA |

| VR | ช่อง | เงื่อนไข | ข้อความ |
|---|---|---|---|
| VR-01 | Month | required | กรุณาเลือกประจำเดือน |
| VR-02 | Company Name | required | กรุณาเลือกลูกค้า |
| VR-03 | Contact Person | required · ≤ 120 | กรุณากรอกชื่อผู้ติดต่อ |
| VR-04 | คะแนน 10 ข้อ | ครบตอนบันทึกผล | เลือกคะแนนให้ครบ 10 ข้อ |
| VR-05 | เหตุผลยกเลิก | required | กรุณาระบุเหตุผล |

### 8.5 ระดับความยืดหยุ่น
BR-04 → Sales Configuration · BR-06 → F-DOCCFG · ถ้อยคำหัวข้อ = ตามแบบฟอร์ม FM-SAL-22 Rev.00 (เปลี่ยน Rev. = เวอร์ชันใหม่ของแบบ ผ่าน mdoc)

## 9. Edge Cases
| EC | กรณี | ผล |
|---|---|---|
| EC-01 | ลูกค้าตอบไม่ครบ | เก็บเป็นร่าง · ปุ่มบันทึกผลแจ้งจำนวนข้อที่ขาด |
| EC-02 | Feedback ยาวเกิน 5 บรรทัด | PDF ตัดบรรทัดต่อ + layout dense ยัง 1 หน้า (ทดสอบ 8 บรรทัด) |
| EC-03 | ลูกค้ารายเดียวตอบซ้ำเดือนเดียวกัน | ไม่บล็อกรอบนี้ → OQ-06 |
| EC-04 | ลูกค้าเปลี่ยนชื่อใน master หลังบันทึก | ใบเดิมคง snapshot |
| EC-05 | บันทึกชนกัน (stale) | 409 → toast รีเฟรช สถานะไม่เปลี่ยน |
| EC-06 | แบบเอกสารปิดใช้ (F-DOCCFG) | ปุ่มสร้าง disabled |
| EC-07 | ชื่อ/ผู้ติดต่อเป็นอักษรต่างประเทศ | เก็บ UTF-8 · ฟอนต์แบบพิมพ์ต้องรองรับ (ตรวจรอบเต็ม) |

## 10. Value Stream & Downstream Impact
Positioning: Sales Admin ต่างประเทศ — เอกสารส่งออก/ประสานการขนส่ง/แก้ปัญหา → **เก็บแบบประเมิน (feature นี้)** → สรุปผลประเมินต่างประเทศ (FM-SAL-23) → แผนปรับปรุง
| ปลายทาง | ข้อมูล | Trigger | หมายเหตุ |
|---|---|---|---|
| สรุปผลการประเมินต่างประเทศ (FM-SAL-23) | คะแนนรายข้อ/กลุ่ม/เดือน/ลูกค้า | recorded | **ไม่ wire รอบนี้ (DEC-02)** — อ่านผ่าน API list ภายหลัง |
| ENG-NOTIFY | คะแนนต่ำ · ยกเลิก | recorded / cancelled | NTF_BRIEF |
| F-DOCCFG / ENG-DOC-NUM | เลขที่ SEA | บันทึกครั้งแรก | ไม่มี snapshot PDF (เอกสารภายใน) |

## 11. Delivery
Phase 1 = ทุกอย่างใน §2.1 · Phase 2 (เสนอ) = ลูกค้ากรอกเองผ่านลิงก์ (ภาษาอังกฤษ) · ป้อนข้อมูลเข้าใบสรุปต่างประเทศอัตโนมัติ · รวมโครงกับ FM-SAL-20 (ในประเทศ · SDA) ถ้าต้องการรายงานรวม

## 12. Dev Summary "ใบสั่ง"
- Config: doc_type SEA (F-DOCCFG) · เกณฑ์คะแนนต่ำ (ค่าเริ่ม ≤ 2) · Customer master flag ต่างประเทศ
- Declaration: NTF_BRIEF · DOCCFG_BRIEF · MDOC_BRIEF (ฉบับจริงหลัง FRD) · **ไม่มี DOA_BRIEF (DEC-03)**
- Screen Inventory: P-01 รายการ · P-02 สร้าง/แก้ (drawer wide 3 ขั้น) · P-03 ดู (drawer 4 แท็บ) · M-01 บันทึกผล · M-02 ยกเลิก · M-03 ทิ้งข้อมูล
- UI Signals: เอกสาร + พิมพ์ = ใช่ (ภาษาอังกฤษ) · ลายเซ็น = ไม่มี · archetype Q-form (DOA 0 ขั้น)

## 13. Open Questions
| OQ | คำถาม | เจ้าของ | Block? |
|---|---|---|---|
| OQ-01 | ตัวชี้วัดความสำเร็จ (เช่น % ลูกค้าต่างประเทศที่ตอบต่อเดือน) | ลูกค้า Credence | ไม่ |
| OQ-02 | ลูกค้าเซ็นยืนยัน DEC-01..10 (AI-DEFAULT) — โดยเฉพาะ "ไม่มีการอนุมัติ" (DEC-03) และผู้บันทึก = Sales Admin | ทีม → ลูกค้า | ก่อน UAT |
| OQ-03 | เกณฑ์ "คะแนนต่ำ" = ≤ 2 ถูกต้องไหม / ผู้รับแจ้ง | ลูกค้า | ไม่ |
| OQ-04 | Customer master แยกลูกค้าต่างประเทศได้หรือยัง | พี่เบิร์ด | ก่อน dev |
| OQ-05 | Contact Person เลือกจากรายชื่อผู้ติดต่อใน Customer master หรือพิมพ์เอง | ลูกค้า/ทีม | ไม่ |
| OQ-06 | ลูกค้ารายเดียวตอบได้กี่ครั้งต่อเดือน (กันซ้ำไหม) | ลูกค้า | ไม่ |
| OQ-07 | รหัส SEA (กัน SDS = FM-SAL-21 · SES = FM-SAL-23) · function_code taxonomy · รหัส feature จริงแทน F-TMP-006 | ทีม | ก่อน register |
| OQ-08 | แบบพิมพ์ภาษาอังกฤษล้วน (ตามกระดาษ) หรือสองภาษา · เลขปีในเลขที่/เดือน ใช้ ค.ศ. หรือ พ.ศ. | ลูกค้า | ไม่ |

## 14. Security & Compliance
Preset: Standard Sales · PII: **Contact Person** = ชื่อบุคคลของลูกค้า (PDPA · Confidential) — เห็นเฉพาะผู้มีสิทธิ์เห็นใบ · ไม่ใส่ใน log · ข้อมูลตัวอย่างใน prototype/แบบพิมพ์เป็นข้อมูลสมมติทั้งหมด · Audit append-only ทุก action · ไฟล์แนบตาม file_policy Document Center (≤20 MB · pdf/doc/xls/รูป)

## 15. Health Check / Monitoring
KPI เสนอ: จำนวนแบบประเมินต่อเดือน · สัดส่วนข้อคะแนนต่ำต่อกลุ่ม · ร่างค้างเกิน 7 วัน (เกณฑ์ → OQ-01)

## Appendix — Screen List
| ID | จอ | route |
|---|---|---|
| P-01 | รายการแบบประเมิน | #/sa-csat-ovs |
| P-02 | สร้าง / แก้ร่าง (wizard 3 ขั้น) | #/sa-csat-ovs/create · #/sa-csat-ovs/edit/:id |
| P-03 | ดูแบบประเมิน (4 แท็บ) | #/sa-csat-ovs/view/:id |

## Quality Gate (C1–C20)
C1–C19 ✅ · C16 ไม่มี Registry ของ feature ใหม่ = WARN (รหัสชั่วคราว F-TMP-006) · C20 Scope Lock = DECISIONS.lock ครบ DEC-01..14 + OQ-02 รอใบเซ็น ✅ → **APPROVED**
