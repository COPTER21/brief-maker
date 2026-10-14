# 05_RULES — F-AGM-004 Crop Management

## §5.1 Business Rules (→ invariants §3)
| BR | Rule |
|---|---|
| BR-AGC-01 | double-binding บังคับ: Quota(verified,exact) → Plot(ของเจ้าของ quota + verified) → form |
| BR-AGC-02 | snapshot farmer/address/size read-only |
| BR-AGC-03 | create/CSV → waiting_for_verify เสมอ |
| BR-AGC-04 | **edit crop verified + save → กลับ waiting_for_verify** ⭐ |
| BR-AGC-05 | quota_id/plot_id แก้ไม่ได้ตอน edit |
| BR-AGC-06 | verify/reject: waiting เท่านั้น · reject reason บังคับ · เดี่ยว+bulk (skip non-eligible) |
| BR-AGC-07 | remaining = total_tons − ΣETCD · negative allowed + badge |
| BR-AGC-08 | ETCD/Survey read-only + fail-soft |
| BR-AGC-09 | soft cancel/delete + reason บังคับ + audit |
| BR-AGC-10 | CSV per-row idempotent · ทุกแถว waiting · partial + report |
| BR-AGC-11 | optimistic lock + idempotency ทุก mutation |
| BR-AGC-12 | audit ทุก mutation (+ bulk count) |
| BR-AGC-13 | agronomic fields (plot_code/variety/cane_type/found_disease_insect/disease_details) optional · cane_age_months derived read-only |
| BR-AGC-14 | Export CSV = client-side (เคารพ filter) · **backend export endpoint/idempotency = Pending Spec** (TC-581 — follow-up ทีม dev) |

## §5.4 Validation (verbatim จาก code)
| VR | Field | Rule | Message |
|---|---|---|---|
| VR-01 | quota_id | กรอก + verified | "กรุณากรอก quota_id" / "ไม่พบ Quota หรือสถานะไม่เป็น verified" |
| VR-02 | plot_id | ของ quota owner + verified | "ไม่พบแปลงของเจ้าของโควตา หรือแปลงยังไม่ผ่านการตรวจสอบ" |
| VR-03 | production_year_be | 2500-2600 | "กรุณากรอกปีผลผลิต พ.ศ." / "ปี พ.ศ. ต้องอยู่ระหว่าง 2500-2600" |
| VR-04 | planted_month | 1-12 | "กรุณาเลือกเดือนที่ปลูก" |
| VR-05 | total_tons | ≥ 0 | "กรุณากรอกปริมาณรวม" / "ปริมาณรวมต้องเป็นตัวเลขที่มากกว่าหรือเท่ากับ 0" |
| VR-06 | reject_reason | บังคับเมื่อ reject | "กรุณากรอกเหตุผลในการปฏิเสธ" |
| VR-07 | postal_code | 5 หลัก (ถ้ากรอก) | "รหัสไปรษณีย์ต้องเป็นตัวเลข 5 หลัก" |
| VR-08 | photos | ชนิด/ขนาด policy | "ไฟล์รูปไม่ถูกต้อง (ชนิด/ขนาด)" |
| VR-09 | cancel/delete reason | บังคับ | "กรุณากรอกเหตุผล" |
| VR-10 | variety | enum ∈ {khon-kaen-3, lk-92-11, ut-8} ถ้ากรอก (optional) | "สายพันธุ์ไม่ถูกต้อง" |
| VR-11 | cane_type | enum ∈ {new, ratoon} ถ้ากรอก (optional) | "ประเภทอ้อยไม่ถูกต้อง" |
| VR-12 | cane_age_months | **derived read-only** (FN-AT-CROP-192) · ไม่รับ user-input | — |
| VR-13 | found_disease_insect | boolean (ไม่พบ/พบ) · optional | — |
| VR-14 | plot_code / disease_details | text · optional | — |

## §5.2 State Machine (LOCK-02)
waiting --verify--> verified · --reject(+reason)--> rejected · **verified --edit+save--> waiting** · any --cancel(+reason)--> cancelled · any --delete(+reason)--> deleted · verified/rejected → verify ซ้ำไม่ได้ (409)

## §5.3 Permission (→ invariants §6)
เจ้าหน้าที่ crop: create/edit/csv/cancel/delete · ผู้ตรวจสอบ: +verify/reject · SoD flag (OQ-C4)

## §5.5 Edge Cases
| EC | Case | Expected |
|---|---|---|
| EC-01 | quota ไม่พบ/ไม่ verified | "ไม่พบ Quota หรือสถานะไม่เป็น verified" block |
| EC-02 | plot ไม่ใช่ของเจ้าของ quota / ไม่ verified | block owner mismatch |
| EC-03 | year นอก 2500-2600 | VR-03 |
| EC-04 | month นอก 1-12 | VR-04 |
| EC-05 | total_tons < 0 / ไม่ใช่ตัวเลข | VR-05 |
| EC-06 | reject ไม่ใส่เหตุผล | VR-06 block |
| EC-07 | edit crop verified → save | กลับ waiting (BR-04) |
| EC-08 | แก้ quota/plot ตอน edit | อ่านอย่างเดียว (block) |
| EC-09 | bulk เลือกรวม non-waiting | skip + summary |
| EC-10 | remaining ติดลบ | badge แดง (ไม่ block verify — OQ-C5) |
| EC-11 | ETCD/Survey down | fail-soft "ดึงข้อมูล...ไม่สำเร็จ" (ไม่ block landing) |
| EC-12 | stale edit | 409 "ข้อมูลล้าสมัย กรุณารีเฟรช" |
| EC-13 | concurrent verify (status เปลี่ยน) | 409 "สถานะเปลี่ยนแปลงแล้ว กรุณารีเฟรช" |
| EC-14 | CSV header ไม่ตรง | reject ทั้งไฟล์ + column error |
| EC-15 | CSV row quota/plot invalid | error รายแถว |
| EC-16 | double-submit create | idempotency → 1 รายการ |
| EC-17 | deep-link crop ไม่มี/deleted | "ไม่พบข้อมูลรอบปลูกที่เลือก" + กลับ list |
| EC-18 | cancel/delete ไม่ใส่เหตุผล | VR-09 block |

## §5.6 Error Catalog
ERR_QUOTA_NOT_VERIFIED "ไม่พบ Quota หรือสถานะไม่เป็น verified" · ERR_PLOT_OWNER_MISMATCH "ไม่พบแปลงของเจ้าของโควตา หรือแปลงยังไม่ผ่านการตรวจสอบ" · ERR_VALIDATION (รายช่อง) · ERR_REJECT_NO_REASON "กรุณากรอกเหตุผลในการปฏิเสธ" · ERR_STALE(409) "ข้อมูลล้าสมัย กรุณารีเฟรช" · ERR_STATUS_CONFLICT "สถานะเปลี่ยนแปลงแล้ว กรุณารีเฟรช" · ERR_CSV_INVALID "ไฟล์ไม่ถูกต้อง กรุณาอัปโหลดไฟล์ CSV" · ERR_ETCD_UNAVAILABLE (fail-soft) · ERR_NOT_FOUND "ไม่พบข้อมูลรอบปลูกที่เลือก"
