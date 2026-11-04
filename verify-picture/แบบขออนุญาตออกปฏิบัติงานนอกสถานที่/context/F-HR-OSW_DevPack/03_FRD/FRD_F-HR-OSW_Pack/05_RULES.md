# 05_RULES — F-HR-OSW แบบขออนุญาตออกปฏิบัติงานนอกสถานที่

> Audience: BE · QA · declarative rules · ทุก rule อ้าง BRD §9 (R-xx)

## §5.1 Business Rules (BR)
| BR | Rule | Tag | BRD | บังคับที่ |
|---|---|:---:|---|---|
| BR-OSW-01 | สถานะเริ่มต้น = draft | FIXED | R01 | FN-05 |
| BR-OSW-02 | ผู้ขอ/ตำแหน่ง/ฝ่าย มาจากระบบ · snapshot ณ วันที่ขอ (ไม่มีช่องให้กรอก) | FIXED | R02 | FN-02/05 |
| BR-OSW-03 | ลักษณะเลือกได้อย่างเดียว: day หรือ overnight | FIXED | R03 | FN-03 · DB enum |
| BR-OSW-04 | per_diem = overnight ? paid_nights × rate : 0 | FIXED | R04 | FN-04 |
| BR-OSW-05 | rate = ExpensePolicy.per_diem ณ ตอนสร้างใบ (snapshot) · ห้าม hardcode 150 | CONFIGURABLE | R05 | FN-02 · `[AI-DEFAULT]` จุด snapshot = ตอนสร้าง (OQ-10) |
| BR-OSW-06 | nights เริ่มต้น = Σ(days−1) · paid_nights เริ่มต้น = nights · คำนวณใหม่เมื่อเปลี่ยนวันที่ จนกว่าผู้ใช้ปรับเอง | FIXED | R06 | FN-04 · UI |
| BR-OSW-07 | nights > maxNights = เตือน ไม่บล็อก | FIXED | R07 | FN-03 WARN |
| BR-OSW-08 | เวลาเริ่มต้น 08:30–17:30 จาก config `osw.default_time` | CONFIGURABLE | R08 | API-12 |
| BR-OSW-09 | สายอนุมัติ resolve จาก DOA entry `osw` ตอนส่ง แล้ว freeze ลง approval_chain | DYNAMIC | R09 | FN-07/08 |
| BR-OSW-10 | อนุมัติเรียงขั้น — ครบทุกขั้นจึง approved · ขั้นใด reject = จบ | FIXED | R10 | FN-09 |
| BR-OSW-11 | requester ≠ assignee ทุกขั้น (SoD) | FIXED | R11 | FN-07/08/09 |
| BR-OSW-12 | reject / cancel ต้องมีเหตุผล (1–500) | FIXED | R12 | API-08/09 |
| BR-OSW-13 | แก้ไขได้เฉพาะ draft ของตัวเอง · ส่งแล้วแก้ไม่ได้ | FIXED | R13 | FN-06 |
| BR-OSW-14 | เลขที่ ENG-DOC-NUM('OSW') ตอนบันทึกครั้งแรก · immutable | CONFIGURABLE (รูปแบบ) | R14 | FN-05 · DOCCFG_BRIEF |
| BR-OSW-15 | แบบเอกสาร OSW ไม่เปิดใช้ที่ F-DOCCFG (Document Configuration) → สร้างใหม่ไม่ได้ | FIXED | R15 | FN-02 |
| BR-OSW-16 | ไฟล์แนบ pdf/doc(x)/xls(x)/png/jpg ≤ 20 MB ต่อไฟล์ | CONFIGURABLE | R16 | file_policy |
| BR-OSW-17 | PDF = แบบพิมพ์ FM-HRM-02 ตาม `print_config` ที่ F-DOCCFG (form_code · revision · min_rows · sign_boxes) · หัวกระดาษจาก header_snapshot · ช่องลายเซ็น = ผู้ขอ + 1 ช่องต่อขั้น chain | CONFIGURABLE | R17 | FN-11 |
| BR-OSW-18 | approved → เก็บ PDF approved_final | CONFIGURABLE (flag) | R18 | FN-13 |
| BR-OSW-19 | มองเห็น: เจ้าของ · ผู้อยู่ใน chain · HR | FIXED | R19 | FN-01 |
| BR-OSW-20 | SLA การพิจารณาต่อขั้น | WARNING | R20 | ไม่ implement timer จนปิด OQ-04 |

## §5.2 State Machine
| From | Event | To | Guard | Actor |
|---|---|---|---|---|
| — | create | draft | BR-OSW-15 · VR ผ่าน | owner |
| draft | update | draft | owner · version | owner |
| draft | submit | pending_approval | VR ผ่าน · assignees ครบ · BR-OSW-11 | owner |
| pending_approval | approve (มีขั้นถัดไป) | pending_approval | actor = current assignee | approver |
| pending_approval | approve (ขั้นสุดท้าย) | approved | actor = current assignee | approver |
| pending_approval | reject | rejected | reason | approver |
| draft / pending_approval / approved | cancel | cancelled | reason · owner หรือ HR | owner / HR |
| rejected / cancelled | — | (terminal) | — | — |
ห้าม transition อื่น → 422 `BR_INVALID_TRANSITION`

## §5.3 Permission Matrix
| Action | Owner | Current approver | Other in chain | HR | Others |
|---|:---:|:---:|:---:|:---:|:---:|
| view | ✅ | ✅ | ✅ | ✅ | ❌ (404) |
| create | ✅ (ตัวเอง) | — | — | ✅ (ตัวเอง) | ✅ (ตัวเอง) |
| update draft | ✅ | ❌ | ❌ | ❌ | ❌ |
| submit | ✅ | ❌ | ❌ | ❌ | ❌ |
| approve / reject | ❌ | ✅ | ❌ | ❌ | ❌ |
| cancel | ✅ | ❌ | ❌ | ✅ | ❌ |
| pdf / export | ✅ | ✅ | ✅ | ✅ | ❌ |

## §5.4 Field Validation Rules
### Per-field declarative rules
| VR | Field | Rule | Type | Message (verbatim UI) |
|---|---|---|---|---|
| VR-01 | line dates | d_from, d_to required | Error | เลือกวันที่ไป |
| VR-02 | line dates + purpose | ทั้งคู่ว่าง | Error | เลือกวันที่และบอกว่าไปทำอะไร |
| VR-03 | purpose | required ≤300 | Error | บอกว่าไปทำอะไร ที่ไหน |
| VR-04 | d_to | ≥ d_from | Error | วันที่กลับต้องไม่ก่อนวันที่ไป |
| VR-05 | t_from, t_to | required | Error | ใส่เวลาให้ครบ |
| VR-06 | t_to (วันเดียว) | > t_from | Error | เวลาสิ้นสุดต้องหลังเวลาเริ่ม |
| VR-08 | nights (overnight) | ≥ 1 | Error | ใส่วันที่ก่อน หรือปรับจำนวนคืน (อย่างน้อย 1 คืน) |
| VR-09 | paid_nights | ≤ nights | Error | คืนที่ได้เบี้ยเลี้ยงต้องไม่เกินคืนที่ค้าง |
| VR-10 | nights | > maxNights | Warning | มากกว่าช่วงวันที่ (ค้างได้ N คืน) — ตรวจอีกครั้ง |
| VR-11 | d_from | < today | Warning | มี N ช่วงเป็นวันที่ผ่านมาแล้ว — ส่งเป็นคำขอย้อนหลัง |
| VR-12 | assignee ต่อขั้น | required | Error | กรุณาเลือกผู้พิจารณา |
| VR-13 | reason | required | Error | กรุณาระบุเหตุผล |
| VR-14 | attachment | type/size | Error | {ชื่อไฟล์} — ชนิดไฟล์ไม่รองรับ / {ชื่อไฟล์} — ไฟล์ใหญ่เกินกำหนด (สูงสุด 20 MB) |
| VR-15 | save/submit | API fail | Error | ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง |
### Cross-field rules
| VR-07 | lines | ช่วงไม่ทับกัน | Error | วันที่ซ้อนกับช่วงที่ N |
toast รวมเมื่อกดถัดไปไม่ผ่าน: "กรุณากรอกข้อมูลให้ครบถ้วน"

## §5.5 Edge Cases
| EC | กรณี | การจัดการ | ที่มา | สถานะ |
|---|---|---|---|---|
| EC-01 | ไป-กลับแต่มีคืน (ตัวอย่างกระดาษ) | เลือกได้อย่างเดียว · day → nights=0 | E01 | ☑ |
| EC-02 | คืนเกินช่วงวันที่ | WARN | E02 | ☑ |
| EC-03 | paid > nights | บล็อก | E03 | ☑ |
| EC-04 | ช่วงซ้อน | บล็อก (server ด้วย) | E04 | ☑ |
| EC-05 | เวลาสิ้นสุดก่อนเริ่ม (วันเดียว) | บล็อก | E05 | ☑ |
| EC-06 | คำขอย้อนหลัง | WARN ในขั้นตรวจสอบ | E06 | ☑ |
| EC-07 | > 5 ช่วง | ไม่จำกัด · PDF dense ≤12 ช่วง 1 หน้า | E07 | ☑ |
| EC-08 | ผู้ขอเลือกตัวเอง | ไม่อยู่ในรายชื่อ + server 422 | E08 | ☑ |
| EC-09 | API ล้ม (PR-4) | transaction rollback · UI คงข้อมูล · กดซ้ำได้ (idempotency) | E09 | ☑ `[AI-DEFAULT]` |
| EC-10 | ปิดฟอร์มค้าง | modal ทิ้งข้อมูล | E10 | ☑ |
| EC-11 | ไฟล์ไม่รองรับ/ใหญ่ | ปฏิเสธ | E11 | ☑ |
| EC-12 | DOA หลายขั้น | slot ต่อขั้น · sequential · ช่องลายเซ็นตามขั้น | E12 | ☑ |
| EC-13 | ผู้พิจารณาลาออก/ย้าย | reassign/delegation ที่ DOA กลาง (PR-6) | E13 | ☐ แนะนำ |
| EC-14 | ยกเลิกหลังวันเดินทาง | อนุญาต | E14 | ☐ `[AI-DEFAULT]` OQ-09 |
| EC-15 | กดซ้ำ | ปุ่ม disable + Idempotency-Key (PR-7) | E15 | ☐ `[AI-DEFAULT]` |
| EC-16 | ยกเลิกชนกับอนุญาต (PR-1) | optimistic lock → 409 ตัวหลัง | E16 | ☐ `[AI-DEFAULT]` |
| EC-17 | ไม่มีผู้บังคับบัญชา | slot ว่าง ต้องเลือก (VR-12) | E17 | ☐ |
| EC-18 | ไม่มีอัตราเบี้ยเลี้ยง | บล็อกค้างคืน `BR_PERDIEM_POLICY_MISSING` | E18 | ☐ `[AI-DEFAULT]` |
| EC-19 | อัตราเปลี่ยนระหว่างร่าง | ใช้อัตรา snapshot ตอนสร้าง | E19 | ☐ `[AI-DEFAULT]` OQ-10 |
| EC-20 | ข้อความยาว | ตัดบรรทัดในช่อง PDF | E20 | ☐ (ทดสอบแล้ว) |
| EC-21 | > 12 ช่วง | ขึ้นหน้า 2 · ลายเซ็นไม่ตัด | E21 | ☐ |
| EC-22 | เปิด URL ใบคนอื่น | 404 | E22 | ☐ |
| EC-23 | สิทธิ์ถูกถอนระหว่างพิจารณา (PR-3) | 403 "คุณไม่มีสิทธิ์ทำรายการนี้" + refresh | probe | ☐ `[AI-DEFAULT]` |
| EC-24 | callback DOA มาหลังยกเลิก | ignored | probe | ☐ `[AI-DEFAULT]` |

## §5.6 Error Catalog
| Code | HTTP | ความหมาย | UI |
|---|---|---|---|
| ERR_VALIDATION_FAILED | 400 | VR ไม่ผ่าน (`errors[]`) | ข้อความ VR ในการ์ด |
| ERR_ASSIGNEE_REQUIRED | 400 | ขาดผู้พิจารณา | กรุณาเลือกผู้พิจารณา |
| ERR_REASON_REQUIRED | 400 | ขาดเหตุผล | กรุณาระบุเหตุผล |
| ERR_NOT_OWNER / ERR_NOT_OWNER_OR_HR / ERR_NOT_CURRENT_APPROVER | 403 | ไม่มีสิทธิ์ | คุณไม่มีสิทธิ์ทำรายการนี้ |
| ERR_NOT_FOUND | 404 | ไม่พบ/ไม่มีสิทธิ์ดู | — |
| ERR_VERSION_CONFLICT | 409 | ถูกแก้ก่อน | ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่ |
| ERR_DUPLICATE_IDEMPOTENCY_KEY | 409 | ซ้ำ (คืนผลเดิม) | — |
| BR_DOCTYPE_INACTIVE | 422 | แบบเอกสารไม่เปิด | แบบเอกสารนี้ยังไม่เปิดใช้งาน |
| BR_PERDIEM_POLICY_MISSING | 422 | ไม่มีอัตรา | — (OQ-03) |
| BR_NOT_DRAFT | 422 | ไม่ใช่ร่าง | แก้ไขได้เฉพาะร่างของตัวเอง |
| BR_NOT_PENDING / BR_ALREADY_CLOSED / BR_INVALID_TRANSITION | 422 | สถานะไม่ถูก | ข้อมูลถูกแก้โดยผู้อื่น กรุณารีเฟรชแล้วลองใหม่ |
| BR_SOD_SELF_APPROVER | 422 | เลือกตัวเอง | คุณไม่มีสิทธิ์ทำรายการนี้ |
| BR_DOA_ENTRY_MISSING | 422 | ไม่มี DOA entry | ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง (alert admin) |
| ERR_INTERNAL | 500 | อื่น ๆ | ทำรายการไม่สำเร็จ กรุณาลองใหม่อีกครั้ง |

## §5.7 Security Bible Application
### D2: Authentication & Session
JWT ทุก API · session timeout platform
### D7: PII Protection
employee_name / purpose / actor_name = PII · ไม่ส่งในแจ้งเตือนเกินจำเป็น (osw_cancelled ส่งเลขที่ + ผู้ยกเลิกเท่านั้น)
### D-CLASS: Data Classification
| ระดับ | Fields | Enforcement |
|---|---|---|
| Confidential | employee_name, employee_id, purpose, per_diem_amount, actor_name | row scope BR-OSW-19 ที่ API-01/02/10/11 · audit view PDF/export |
| Internal | ที่เหลือ | RLS + JWT |
ไม่มี Restricted · ไม่มี Public
### D9: Audit Logging
ทุก transition + export + PDF download → T_osw_audit / audit view
### D15: Admin Actions
ไม่มี admin action ใน feature (config อยู่ feature กลาง)
### D17: Multi-Tenant Isolation
RLS ทุกตาราง · DOA/DOC engines เรียกด้วย tenant context

## §5.8 Compliance & Audit Requirements
COSO SoD (BR-OSW-11) · PDPA (D7) · ประวัติ append-only (S01-07) · DOA snapshot (S03-02)
**Declarations:** DOA_BRIEF v1.1 (wire pending · G1–G7 PASS) · DOCCFG_BRIEF v1.1 · MDOC_BRIEF_OSW (source=request · REQ-2569-0011) · **NTF_BRIEF: ยังไม่ทำ** — event ของ feature เองมี 1 ตัว `osw_cancelled` (02 §2.X) → รัน ntf-declaration ต่อ · `doa_pending`/`doa_result` เป็นของ DOA engine ห้ามประกาศซ้ำ
