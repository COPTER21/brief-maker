# 05_RULES — F-AGM-005 Contract Management

## §5.1 Business Rules (→ invariants §3)
| BR | Rule |
|---|---|
| BR-AGT-01 | build path: โควตา → แปลง(≥1) → รอบปลูก verified(≥1) → ประเภทสัญญา |
| BR-AGT-02 | total_tons = **manual input บังคับ > 0 ทุกประเภท** (crop-sum เป็น helper "ใช้ค่านี้" เท่านั้น) · plot_count/crop_count นับ |
| BR-AGT-03 | create → Waiting for verify เสมอ |
| BR-AGT-04 | approve/reject: Waiting เท่านั้น · approve ไม่ต้องมีเหตุผล · reject reason บังคับ · เดี่ยว+bulk |
| BR-AGT-05 | **write-back**: create → crop license='contracted' · reject → 'none' · approve → keep |
| BR-AGT-06 | 5 contract types + type-specific fields (เก็บเฉพาะ type ที่ตรง) |
| BR-AGT-07 | 1 crop : 1 active contract (กัน crop license=contracted เลือกซ้ำ) |
| BR-AGT-08 | delete + ลบ attachments + audit |
| BR-AGT-09 | audit ทุก mutation (+ bulk count + license write) |
| BR-AGT-10 | optimistic lock + idempotency |

## §5.4 Validation Rules
| VR | Field | Rule | Message |
|---|---|---|---|
| VR-01 | quota+plots+crops+type | required (plots≥1, crops≥1) | "กรุณาตรวจสอบข้อมูลให้ครบถ้วน" (Missing required fields) |
| VR-02 | crops | verified + ของโควตา | "เลือกรอบปลูกที่ตรวจสอบแล้ว" |
| VR-03 | crops | license ≠ contracted | "รอบปลูกนี้ทำสัญญาแล้ว" |
| VR-04 | reject_reason | บังคับเมื่อ reject | "กรุณากรอกเหตุผลในการปฏิเสธ" (Rejection reason is required) |
| VR-05 | type-specific | required ตาม type | "เลือกช่วงโปรโมชั่น" / "เลือกเครน" / "เลือกรายการส่งเสริม" |
| VR-06 | total_tons | manual, บังคับ > 0 (ทุก 5 ประเภท) | "กรุณากรอกจำนวนตันที่ทำสัญญา (> 0)" |
| VR-07 | support_items | type=support ต้องมี ≥1 รายการ · แต่ละรายการบังคับ support_type + price(≥0) + received_date | "กรุณาเพิ่มรายการส่งเสริมให้ครบ (ประเภท/ราคา/วันที่รับ)" |
| VR-08 | promotion7_period | ∈ 4 ค่า authoritative (หลังเปิดหีบ/ก่อนปิดปีใหม่/หลังเปิดปีใหม่/ก่อนปิดหีบ) | "เลือกช่วงโปรโมชั่น" |
| VR-09 | selected_crane | ∈ crane master (กุดโดน/ชื่นชม2/หนองกุงสวรรค์/โนนสำราญ) | "เลือกเครน" |
| VR-10 | early-purchase | ต้องการเฉพาะ total_tons · **ไม่มี attachments** | — |

## §5.2 State Machine (LOCK-02)
Waiting for verify --approve--> Verified (crop license คง contracted) · --reject(+reason)--> Reject (**crop license revert none**) · Verified/Reject → approve/reject ซ้ำไม่ได้ (409) · delete → ลบ

## §5.3 Permission (→ invariants §6)
เจ้าหน้าที่สัญญา: create/edit/delete · ผู้อนุมัติ: +approve/reject · SoD flag (OQ-CT6)

## §5.5 Edge Cases
| EC | Case | Expected |
|---|---|---|
| EC-01 | quota/plots/crops ไม่ครบ | "กรุณาตรวจสอบข้อมูลให้ครบถ้วน" block |
| EC-02 | crop ไม่ verified | excluded จาก available-items |
| EC-03 | crop license=contracted | กันเลือกซ้ำ "รอบปลูกนี้ทำสัญญาแล้ว" |
| EC-04 | type-specific field ไม่ครบ | VR-05 block |
| EC-05 | approve | ไม่ต้องมีเหตุผล → Verified |
| EC-06 | reject ไม่ใส่เหตุผล | VR-04 block |
| EC-07 | reject → crop license revert none | write-back (XT) |
| EC-08 | bulk เลือกรวม non-waiting | skip + summary |
| EC-09 | stale edit | 409 "ข้อมูลล้าสมัย กรุณารีเฟรช" |
| EC-10 | concurrent approve (status เปลี่ยน) | 409 "สถานะเปลี่ยนแปลงแล้ว กรุณารีเฟรช" |
| EC-11 | license write fail | rollback + retry queue |
| EC-12 | delete → crop license revert? | (OQ) default revert none เหมือน reject |
| EC-13 | double-submit create | idempotency → 1 รายการ |
| EC-14 | deep-link contract ไม่มี/deleted | "ไม่พบข้อมูลสัญญาที่เลือก" + กลับ list |
| EC-15 | total_tons ≤ 0 หรือว่าง | VR-06 block "กรุณากรอกจำนวนตันที่ทำสัญญา (> 0)" |
| EC-16 | support ไม่มีรายการ / รายการไม่ครบ (ประเภท/ราคา/วันที่รับ) | VR-07 block |
| EC-17 | export CSV | prototype ทำ client-side (UTF-8 BOM) · **backend API = Pending Spec (TC-522)** |

## §5.6 Error Catalog
ERR_MISSING_FIELDS "กรุณาตรวจสอบข้อมูลให้ครบถ้วน" · ERR_CROP_NOT_VERIFIED "เลือกรอบปลูกที่ตรวจสอบแล้ว" · ERR_CROP_ALREADY_CONTRACTED "รอบปลูกนี้ทำสัญญาแล้ว" · ERR_REJECT_NO_REASON "กรุณากรอกเหตุผลในการปฏิเสธ" · ERR_STALE(409) "ข้อมูลล้าสมัย กรุณารีเฟรช" · ERR_STATUS_CONFLICT "สถานะเปลี่ยนแปลงแล้ว กรุณารีเฟรช" · ERR_NOT_FOUND "ไม่พบข้อมูลสัญญาที่เลือก"
