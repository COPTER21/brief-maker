# BRD: ใบเคลียร์เงินทดรองจ่าย (Advance Clearing)

| Field | Value |
|---|---|
| BRD ID | BRD-FIN-ACL-001 |
| Feature | F-FIN-ACL ใบเคลียร์เงินทดรองจ่าย |
| BRD Type | New Feature (แบบ 2 · ดึงข้อมูลเดิม) |
| Version | 1.0 |
| Status | **APPROVED (Prebrief Mode · Lane)** — DEC แทน Scope Lock จนมีใบเซ็นลูกค้า |
| Module | Finance (Core Cube · Operation) |
| Customer | Credence (แบบฟอร์ม FM-FIN-02 Rev.00 : 01/07/2569) |
| Request | REQ-2569-0000 (ชั่วคราว — รอเลขจริงจาก F186) |
| Input | PREBRIEF_REQ-2569-0000_v2 · FORM_SPEC.json · DECISIONS.lock (15 DEC · พร้อมเริ่มทำ) · feature.html (audit 0 · e2e 21/21 + 13/13) |
| Created / Updated | 2026-10-06 |

## Changelog
- v1.0 (2026-10-06): สร้างผ่าน brd-generator-full v2.3 Prebrief Mode (doc-master-pipeline ขั้น 7)
- v1.1 (2026-10-06): BR-12 ช่องลงชื่อ PDF dynamic ตาม DOA (user แจ้ง)

---

## 1. Business Context
### 1.1 ปัญหา / โอกาส
พนักงานที่เบิกเงินทดรองจ่าย ต้องเคลียร์ด้วยแบบฟอร์มกระดาษ FM-FIN-02 — คำนวณยอดด้วยมือ (ต้นฉบับ xlsx ไม่มีสูตร · ช่อง TOTAL พิมพ์ "ศูนย์บาทถ้วน" ทุกครั้ง) · ไม่รองรับกรณีใช้เกินเงินที่เบิก · ลงนาม 4 ช่องแบบส่งต่อมือ · การเงินตามสลิปโอนคืนแยก
### 1.2 เป้าหมาย
1. ขึ้นแบบฟอร์มเป็นเอกสารในระบบ ช่องตรงกระดาษ 1:1 ลูกค้าจำแบบเดิมได้ (PDF Replica)
2. ระบบคำนวณ รวม/หักยอดเบิก/เหลือส่งคืน/ตัวอักษร ให้เอง — ไม่มียอดผิด
3. สายอนุมัติ 3 ขั้นจาก DOA กลาง + ด่านสลิปโอนคืนก่อนการเงินรับเคลียร์
### 1.3 ตัวชี้วัด
ไม่มีใน input → **OQ-01** (ห้ามแต่งตัวเลข)
### 1.4 ที่มา
แบบฟอร์มลูกค้า FM-FIN-02 (xlsx) → FORM_SPEC 14 ช่อง · gate 10 หมวด: G1 ผู้ใช้ตอบ "ประเมินตาม standard" · G2–G10 = AI-DEFAULT

## 2. Scope
### 2.1 In Scope
- รายการใบเคลียร์ (ค้นหา/กรอง สถานะ·ผลเคลียร์·ฝ่าย · CSV) · สร้าง/แก้ร่าง wizard 3 ขั้น · ดูรายละเอียด 4 แท็บ (รายละเอียด › PDF › ลายเซ็น/อนุมัติ › ประวัติ)
- คำนวณ: รวมค่าใช้จ่าย · เหลือส่งคืน · TOTAL · ตัวอักษร (ติดลบได้)
- ส่งอนุมัติ DOA 3 ขั้น (เลือกคนต่อขั้น) · อนุมัติ / ไม่อนุมัติ→กลับร่าง · ยกเลิก (เหตุผลบังคับ)
- แนบไฟล์ (ใบเสร็จ + สลิปโอนคืน) · PDF FM-FIN-02 Replica ทุกสถานะ · เลขที่ ACL จาก ENG-DOC-NUM
### 2.2 Out of Scope
- ใบเบิกเงินทดรองจ่าย FM-FIN-01 (ไม่มีในระบบ → เลขใบเบิก + ยอดเบิกผู้ใช้กรอก) · ลงบัญชี/AP/GL · จ่ายเงินคืนพนักงานจริง · ทำซ้ำเอกสาร · เตือนเลยกำหนดเคลียร์ (ต้องมีวันที่เบิก)
### 2.3 Assumptions
- ข้อมูลผู้ขอ/ตำแหน่ง/ฝ่ายมีใน F-EMP-001 / F-ORG-001 · config ExpensePolicy + Company.bank_accounts มีหรือจะเพิ่ม (OQ-04)
### 2.4 Scope Lock (ชั่วคราว = DECISIONS.lock · ยังไม่มีใบเซ็น → OQ-02)
| DEC | หมวด | มติ | ที่มา |
|---|---|---|---|
| DEC-01 | G1 | อนุมัติแล้วไม่เปลี่ยนค่าในระบบ | ตอบแล้ว |
| DEC-02 | G1 | ไม่ส่งต่อระบบอื่นรอบนี้ | ตอบแล้ว |
| DEC-03 | G2 | DOA dynamic 3 ขั้น: role-line-manager → role-finance-officer → role-finance-manager · ไม่มีวงเงิน | AI-DEFAULT |
| DEC-04 | G3 | ค่าคงที่จาก config · TOTAL = เหลือส่งคืน · ติดลบ = เตือนไม่บล็อก · เหลือคืน>0 ต้องมีสลิปก่อนการเงินรับเคลียร์ · จำนวนเงิน > 0 ทศนิยม 2 | AI-DEFAULT |
| DEC-05 | G4 | ไม่จำกัดแถว · PDF ≥ 10 แถว | AI-DEFAULT |
| DEC-06 | G5 | ช่อง 1:1 · ไม่เพิ่มช่อง · แก้ป้าย ผ่าย→ฝ่าย | AI-DEFAULT |
| DEC-07 | G6 | ลายเซ็นแถวล่าง 1 ช่อง/ขั้น · ข้อความ "ส่ง/พิจารณาในระบบ" ไม่ใช้ภาพ | AI-DEFAULT |
| DEC-08 | G7 | ไม่อนุมัติ = กลับร่างเลขเดิม · ยกเลิก: เจ้าของ+การเงิน · ร่าง/รออนุมัติ · เหตุผลบังคับ | AI-DEFAULT |
| DEC-09 | G8 | เจ้าของ · ผู้อนุมัติหลังส่ง · role-finance-officer เห็นทั้งหมด | AI-DEFAULT |
| DEC-10 | G9 | ออกเลขตอนบันทึกครั้งแรก · รหัส ACL | AI-DEFAULT |
| DEC-11 | G10 | แนบไฟล์ ✓ · CSV ✓ · ทำซ้ำ ✗ · ประกาศ ✗ | AI-DEFAULT |
| DEC-12 | VALID | TOTAL + ตัวอักษรตรงยอดเสมอ | FORM_SPEC |
| DEC-13 | VALID | ยอดติดลบ (ใช้เกิน) มีทางรองรับ — เตือน ไม่บล็อก | FORM_SPEC |
| DEC-14 | VALID | ป้าย "ฝ่าย/แผนก" (แก้คำสะกด) | FORM_SPEC |
| DEC-15 | VALID | แนบหลักฐานระดับใบ · ไม่ผูกหมวดบัญชีรอบนี้ | FORM_SPEC |

## 3. Roles & Permissions (COSO)
| Role | COSO | ทำอะไร |
|---|---|---|
| พนักงาน (ผู้ขอเคลียร์) | Maker | สร้าง/แก้ร่าง · ส่ง · ยกเลิกของตัวเอง (ร่าง/รออนุมัติ) |
| role-line-manager (ผู้อนุมัติ/ตรวจสอบ) | Checker | ขั้น 1 อนุมัติ/ไม่อนุมัติ |
| role-finance-officer (ผู้รับเคลียร์เงิน) | Checker + Custodian | ขั้น 2 รับเคลียร์/ไม่รับเคลียร์ · ตรวจสลิป · เห็นทั้งหมด · ยกเลิกได้ |
| role-finance-manager (ผู้จัดการฝ่ายการเงิน) | Approver | ขั้น 3 อนุมัติ/ไม่อนุมัติ |

| Action | Maker | L-Mgr | Fin-Off | Fin-Mgr |
|---|:-:|:-:|:-:|:-:|
| ดูใบ | ของตน | หลังส่ง (อยู่ในสาย) | ทั้งหมด | หลังส่ง (อยู่ในสาย) |
| สร้าง/แก้ร่าง | ✓ ของตน | – | – | – |
| ตัดสินขั้น | – | ขั้น 1 | ขั้น 2 | ขั้น 3 |
| ยกเลิก | ✓ ของตน | – | ✓ | – |
SoD: ผู้ขอพิจารณาใบตัวเองไม่ได้ (BR-DOA-04)

## 4. User Journey
### 4.1 Happy Path
1. ผู้ขอ: สร้าง → ใส่เลขใบเบิก + ยอดเบิก → รายการค่าใช้จ่าย → ระบบคำนวณสด → แนบใบเสร็จ (+สลิปถ้าเหลือคืน) → บันทึก (ได้เลข ACL) → ส่ง เลือกคน 3 ขั้น
2. ขั้น 1 อนุมัติ → ขั้น 2 การเงินตรวจสลิป รับเคลียร์ → ขั้น 3 อนุมัติ → **เคลียร์แล้ว** · PDF เก็บสำเนา (approved_final)
### 4.2 Alternative
- ไม่อนุมัติ/ไม่รับเคลียร์ ขั้นใดก็ได้ → กลับร่าง เลขเดิม + เหตุผล → ผู้ขอแก้ ส่งใหม่ (resolve สายใหม่)
- เหลือคืน > 0 ไม่มีสลิป → ขั้น 2 กดรับเคลียร์ไม่ได้ ต้องไม่รับเคลียร์ให้ผู้ขอแนบ
- ใช้เกิน (ติดลบ) → ส่งได้ · เตือนทุกจอ · อนุมัติครบ → แจ้งการเงินจ่ายคืน (acl_overspent_approved)
- ยกเลิก (ร่าง/รออนุมัติ) โดยเจ้าของหรือการเงิน
```mermaid
flowchart LR
A[ร่าง] -->|ส่ง| B[รออนุมัติ ขั้น1]
B -->|อนุมัติ| C[ขั้น2 การเงิน]
C -->|รับเคลียร์ (มีสลิปถ้าเหลือคืน)| D[ขั้น3 ผจก.การเงิน]
D -->|อนุมัติ| E[เคลียร์แล้ว]
B & C & D -->|ไม่อนุมัติ/ไม่รับเคลียร์| A
A & B -->|ยกเลิก| X[ยกเลิก]
```

## 5. Data (จาก FORM_SPEC — ป้ายตามกระดาษ)
### 5.1 advance_clearing (header)
| ช่องบนกระดาษ | field | ชนิด | ที่มา | บังคับ |
|---|---|---|---|:-:|
| เลขที่ | doc_no | text | auto ENG-DOC-NUM | ✓ |
| วันที่ | doc_date | date | auto | ✓ |
| ชื่อผู้ขอเคลียร์ฯ | employee_id → snapshot name | ref | system F-EMP-001 (อ่านอย่างเดียว) | ✓ |
| ตำแหน่ง (Position) | position_snapshot | text | system F-EMP-001 | ✓ |
| ฝ่าย/แผนก | dept_snapshot | text | system F-ORG-001 | ✓ |
| อ้างอิงเลขที่ใบเบิกฯ | advance_ref | text | user | ✓ |
| หัก จำนวนเงินที่เบิกฯ | advance_amount | money(2) | user | ✓ >0 |
| รวมค่าใช้จ่าย | total_expense | money(2) | computed Σ | ✓ |
| จำนวนเงินที่เหลือส่งคืน · TOTAL | refund_amount | money(2) ±| computed | ✓ |
| ตัวอักษร | — | — | computed ตอน render | — |
| + DOA fields | approval_status · doa_entry_ref · approval_chain(jsonb snapshot) · approved_by · approved_at | | DOA | |
| + returned_reason · returned_by · returned_at | | | DEC-08 | |
### 5.2 advance_clearing_line
| ลำดับ (auto) | description (user ✓) | amount money(2) >0 (user ✓) |
### 5.3 attachments → Document Center (ไฟล์ระดับใบ)

## 6. User Stories
| ID | Story | AC หลัก |
|---|---|---|
| S-01 | ผู้ขอสร้างใบเคลียร์จากใบเบิก | เลขใบเบิก+ยอด บังคับ · ≥1 รายการ · คำนวณสด · บันทึกได้เลข ACL |
| S-02 | ผู้ขอแนบหลักฐาน | เหลือคืน>0 แสดงบัญชีบริษัทจาก config + เตือนแนบสลิป |
| S-03 | ผู้ขอส่งอนุมัติ | slot 3 ขั้นค่าเริ่มจาก DOA · ผู้ขอไม่อยู่ในรายชื่อ · บังคับเลือกครบ |
| S-04 | ผู้อนุมัติแต่ละขั้นตัดสิน | ปุ่มเฉพาะผู้พิจารณาขั้นปัจจุบัน · เรียงขั้น · ไม่อนุมัติบังคับเหตุผล → กลับร่าง |
| S-05 | การเงินรับเคลียร์ | เหลือคืน>0 ไม่มีสลิป = บล็อก · คำ รับเคลียร์/ไม่รับเคลียร์ |
| S-06 | ใช้เกินเงินเบิก | ยอดติดลบ + "ลบ…" ใน PDF · เตือนไม่บล็อก · แจ้งการเงินเมื่ออนุมัติครบ |
| S-07 | พิมพ์/ดาวน์โหลด PDF FM-FIN-02 | ทุกสถานะ · ลายเซ็น = ผู้ขอ + 1 ช่องต่อขั้นตามที่ตั้งใน DOA (dynamic · แถวละ ≤4) · ≥10 แถว |
| S-08 | ยกเลิก | เจ้าของ/การเงิน · ร่างหรือรออนุมัติ · เหตุผลบังคับ |
| S-09 | การเงินดูทุกใบ + CSV | กรอง สถานะ/ผลเคลียร์/ฝ่าย |

## 7. Status & Lifecycle
| จาก | Action | ไป | ใคร |
|---|---|---|---|
| — | บันทึกครั้งแรก | draft | Maker |
| draft | ส่ง | pending (ขั้น 1) | Maker |
| pending | อนุมัติขั้น n<N | pending (ขั้น n+1) | ผู้พิจารณาขั้น n |
| pending | อนุมัติขั้น N | approved (เคลียร์แล้ว) | ขั้น N |
| pending | ไม่อนุมัติ/ไม่รับเคลียร์ | draft (เลขเดิม · returned_*) | ผู้พิจารณาขั้นปัจจุบัน |
| draft / pending | ยกเลิก | cancelled | Maker / Fin-Off |
approved = ล็อกแก้ไข (ไม่มียกเลิก)

## 8. Business Rules + Validation
| ID | Rule | Tag | Type |
|---|---|:-:|---|
| BR-01 | total_expense = Σ line.amount | FIXED | Formula |
| BR-02 | refund_amount = advance_amount − total_expense (ติดลบได้) · TOTAL = refund | FIXED | Formula (DEC-04/12) |
| BR-03 | ติดลบ = เตือน "ใช้เกินเงินที่เบิก — บริษัทต้องจ่ายคืนพนักงาน" ไม่บล็อก | CONFIGURABLE | Policy (DEC-04 AI-DEFAULT) |
| BR-04 | refund > 0 ต้องมีสลิปก่อนขั้น role-finance-officer อนุมัติ | CONFIGURABLE | Control (DEC-04) |
| BR-05 | เส้นตายเคลียร์ (หมายเหตุ) = ExpensePolicy.advance_clear_due_day | CONFIGURABLE | Threshold |
| BR-06 | บัญชีรับเงินคืน = Company.bank_accounts[purpose=advance_refund] | CONFIGURABLE | Master |
| BR-07 | สายอนุมัติ resolve จาก DOA ตอนส่ง แล้ว freeze | FIXED | DOA (BR-DOA-02) |
| BR-08 | ไม่อนุมัติ → draft เลขเดิม · resolve ใหม่ตอนส่งรอบถัดไป | FIXED | DEC-08 |
| BR-09 | ออกเลขตอนบันทึกครั้งแรก · no-gap ✗ | CONFIGURABLE | DOCCFG |
| BR-10 | ร่างเห็นเฉพาะเจ้าของ (+ การเงิน) | FIXED | Visibility #109 |
| BR-11 | ตัวอักษรใช้ baht_text เดียวกันทั้ง FE/BE · ติดลบ = "ลบ…" | FIXED | Format |
| BR-12 | ช่องลงชื่อใน PDF = ผู้ขอ + 1 ช่องต่อขั้นที่ตั้งใน DOA (dynamic ไม่ fix) · แถวละ ≤4 · คำตัดสินตาม role | FIXED (จำนวน = DOA) | DEC-03 · DEC-07 |

| VR | ช่อง | เงื่อนไข | ข้อความ |
|---|---|---|---|
| VR-01 | advance_ref | required | กรุณาใส่เลขที่ใบเบิก |
| VR-02 | advance_amount | > 0 | ใส่ยอดที่เบิกมากกว่า 0 |
| VR-03 | line.description + amount | required · >0 · ≥1 แถว | ใส่รายละเอียดและจำนวนเงิน (มากกว่า 0) ให้ครบทุกรายการ |
| VR-04 | slot ผู้พิจารณา | ทุกขั้นต้องเลือก · ≠ ผู้ขอ | กรุณาเลือกผู้พิจารณา |
| VR-05 | เหตุผล ไม่อนุมัติ/ยกเลิก | required | กรุณาระบุเหตุผล |

### 8.5 ระดับความยืดหยุ่น
BR-03/04 → Admin Panel (ExpensePolicy) · BR-05 → Admin Panel · BR-06 → Company Master · BR-09 → F-DOCCFG

## 9. Edge Cases
| EC | กรณี | ผล |
|---|---|---|
| EC-01 | ใช้พอดี (refund = 0) | TOTAL 0.00 "ศูนย์บาทถ้วน" ไม่ต้องสลิป |
| EC-02 | ใช้เกิน | ติดลบ + เตือน + แจ้งการเงิน |
| EC-03 | รายการ > 10 แถว | PDF dense ยัง 1 หน้า (ทดสอบ 14 แถว) |
| EC-04 | ผู้ขอเป็นการเงินเอง (ขั้น 2 = ตัวเอง) | slot ว่าง ต้องเลือกคนอื่น |
| EC-05 | แก้ DOA ระหว่างใบรออนุมัติ | ใบเดิมใช้สาย snapshot |
| EC-06 | ส่ง/อนุมัติชนกัน (stale) | 409 → toast รีเฟรช สถานะไม่เปลี่ยน |
| EC-07 | แบบเอกสารปิดใช้ (F-DOCCFG) | ปุ่มสร้าง disabled |
| EC-08 | เลขใบเบิกเดียวเคลียร์ซ้ำหลายใบ | ไม่ตรวจรอบนี้ (ไม่มี FM-FIN-01) → OQ-05 |

## 10. Value Stream & Downstream Impact
Positioning: R2R / Expense — เบิกเงินทดรอง (FM-FIN-01 · ยังไม่มี) → **เคลียร์ (feature นี้)** → [ลงบัญชี / จ่ายคืน — ปิดรอบนี้]
| ปลายทาง | ข้อมูล | Trigger | หมายเหตุ |
|---|---|---|---|
| AP / GL | ค่าใช้จ่าย + ล้างลูกหนี้เงินทดรอง | approved | **ปิดรอบนี้ (DEC-02)** — ประกาศ event ใน FRD ไม่ยิง |
| การเงิน (จ่ายคืน/รับเงินคืน) | refund_amount | approved | แจ้งผ่าน ENG-NOTIFY เท่านั้น |
| F-DOCCFG / ENG-DOC-STORE | PDF snapshot | approved_final | |
| รายงาน | ใบเคลียร์ค้าง / ใช้เกิน | — | Report area อ่าน |

## 11. Delivery
Phase 1 = ทุกอย่างใน §2.1 · Phase 2 (เสนอ) = เชื่อม FM-FIN-01 (ดึงยอดเบิก · กันเคลียร์ซ้ำ · เตือนเลยกำหนด) + post AP/GL

## 12. Dev Summary "ใบสั่ง"
- Config: ExpensePolicy.advance_clear_due_day · Company.bank_accounts[purpose=advance_refund] · DOA entry F-FIN-ACL · doc_type ACL
- Declaration: DOA_BRIEF · NTF_BRIEF · DOCCFG_BRIEF · MDOC_BRIEF (ฉบับจริงหลัง FRD)
- Screen Inventory: P-01 รายการ · P-02 สร้าง/แก้ (drawer wide 3 ขั้น) · P-03 ดู (drawer 4 แท็บ) · M-01..05 modal ส่ง/อนุมัติ/ไม่อนุมัติ/ยกเลิก/ทิ้งข้อมูล
- UI Signals: เอกสารธุรกรรม + พิมพ์ + ลายเซ็น = ใช่ · Q-form

## 13. Open Questions
| OQ | คำถาม | เจ้าของ | Block? |
|---|---|---|---|
| OQ-01 | ตัวชี้วัดความสำเร็จ (เวลาเคลียร์เฉลี่ย / % ใบค้าง) | ลูกค้า Credence | ไม่ |
| OQ-02 | ลูกค้าเซ็นยืนยัน DEC-03..11 (AI-DEFAULT) — โดยเฉพาะ 3 ขั้น · กลับร่าง · ด่านสลิป · คำ รับเคลียร์/ไม่รับเคลียร์ | Strike → ลูกค้า | ก่อน UAT |
| OQ-03 | role id 3 ตัวตรง master DOA จริง | Strike + พี่เบิร์ด | ก่อน wire |
| OQ-04 | ExpensePolicy / Company.bank_accounts มีใน Core แล้วหรือยัง | พี่เบิร์ด | ก่อน dev |
| OQ-05 | ทำ FM-FIN-01 ใบเบิกเมื่อไร (ดึงยอด + กันเคลียร์ซ้ำ) | Strike | ไม่ |
| OQ-06 | รหัส ACL ชนกับ doc_type อื่นใน F-DOCCFG ไหม · function_code taxonomy | Strike | ก่อน register |

## 14. Security & Compliance
Preset: Standard Finance · PII: ชื่อผู้ขอ (pdpa) — ข้อมูลตัวอย่างใน prototype เป็นชื่อสมมติ · บัญชีธนาคารบริษัท = Internal · Audit append-only ทุก action · SoD ผู้ขอ≠ผู้อนุมัติ · ไฟล์แนบตาม file_policy Document Center (≤20MB · pdf/doc/xls/img)

## 15. Health Check / Monitoring
SLA ต่อขั้น: ไม่กำหนดรอบนี้ (WARNING → OQ-01) · KPI เสนอ: ใบรออนุมัติเกิน N วัน · ยอดใช้เกินรวม/เดือน · Widget: ใบเคลียร์ค้างตามฝ่าย

## Appendix — Screen List
P-01 `#/advance-clearing` · P-02 `#/advance-clearing/create` · `/edit/:id` · P-03 `#/advance-clearing/view/:id`
