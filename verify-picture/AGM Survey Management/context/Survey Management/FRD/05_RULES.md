# 05_RULES — F-AGM-006 Survey Management

## §5.1 Business Rules (→ invariants §3)
| BR | Rule |
|---|---|
| BR-AGS-01 | cascade: โควตา → แปลง(ของโควตา) → รอบปลูก(ของแปลง) → ฟอร์ม |
| BR-AGS-02 | snapshot farmer/plot/crop read-only |
| BR-AGS-03 | create/CSV → waiting_for_verify เสมอ |
| BR-AGS-04 | verify/reject: waiting เท่านั้น · verify note optional · reject reason บังคับ · เดี่ยว+bulk |
| BR-AGS-05 | **edit survey verified + save → กลับ waiting** |
| BR-AGS-06 | photos 4 หมวด (รูปกับแปลง/รูปพืชผล/รูปลำต้นในกอ/รูปสีดิน) |
| BR-AGS-07 | CSV per-row · ทุกแถว waiting · partial + report |
| BR-AGS-08 | soft cancel/delete + reason + audit |
| BR-AGS-09 | audit ทุก mutation (+ bulk count) |
| BR-AGS-10 | optimistic lock + idempotency |
| BR-AGS-11 | survey verified feeds Crop survey tab |

## §5.4 Validation Rules
| VR | Field | Rule | Message |
|---|---|---|---|
| VR-01 | cascade | quota→plot→crop ครบ | "กรุณากรอกข้อมูลให้ครบถ้วน" |
| VR-02 | crop | ของ plot ของ quota | cascade filter |
| VR-03 | พื้นฐาน+พืชผล | วันที่/ผู้สำรวจ/พันธุ์/ผลผลิต/ขนาด required | "กรุณากรอกข้อมูลให้ครบถ้วน" |
| VR-04 | yield/plot_size | yield≥0 · plot_size>0 | "กรุณาใส่ค่าที่ถูกต้อง" |
| VR-05 | lat/long | ช่วง (ถ้ากรอก) | "พิกัดไม่ถูกต้อง" |
| VR-06 | reject_reason | บังคับเมื่อ reject | "กรุณากรอกเหตุผลในการปฏิเสธ" |
| VR-07 | planted_month | 1–12 (ถ้ากรอก) | "กรุณาใส่ค่าที่ถูกต้อง" |
| VR-08 | cane_type | enum {อ้อยใหม่, อ้อยตอ} (ถ้ากรอก) | "กรุณาใส่ค่าที่ถูกต้อง" |
| VR-09 | cane_age_months | **derived** — ไม่รับ user input (คำนวณ FN-AT-CROP-192) | — |
| VR-10 | measurement ทั้งหมด (row_spacing/heights/internode/diameter/stalks/clumps) | ≥ 0 เมื่อกรอก · optional | "กรุณาใส่ค่าที่ถูกต้อง" |
| VR-11 | disease_pest_found | boolean (ไม่พบ/พบ) · disease_pest_detail optional | — |
| VR-12 | weed_density | enum {ไม่มี, น้อย, ปานกลาง, มาก} (ถ้ากรอก) · soil_type optional | "กรุณาใส่ค่าที่ถูกต้อง" |
| VR-13 | survey_postal_code | `^\d{5}$` (ถ้ากรอก) | "รหัสไปรษณีย์ไม่ถูกต้อง" |

## §5.2 State Machine (LOCK-02)
waiting --verify--> verified · --reject(+reason)--> rejected · **verified --edit+save--> waiting** · any --cancel/delete(+reason)--> cancelled/deleted · verified/rejected → verify ซ้ำไม่ได้ (409)

## §5.3 Permission (→ invariants §6)
เจ้าหน้าที่สำรวจ: create/edit/csv/cancel/delete · ผู้ตรวจสอบ: +verify/reject · SoD flag (OQ-SV5)

## §5.5 Edge Cases
| EC | Case | Expected |
|---|---|---|
| EC-01 | cascade ไม่ครบ | "กรุณากรอกข้อมูลให้ครบถ้วน" block |
| EC-02 | crop ไม่ใช่ของ plot | cascade filter |
| EC-03 | yield < 0 / plot_size ≤ 0 | VR-04 |
| EC-04 | reject ไม่ใส่เหตุผล | VR-06 block |
| EC-05 | edit survey verified → save | กลับ waiting (BR-05) |
| EC-06 | bulk เลือกรวม non-waiting | skip + summary |
| EC-07 | stale edit | 409 "ข้อมูลล้าสมัย กรุณารีเฟรช" |
| EC-08 | concurrent verify | 409 "สถานะเปลี่ยนแปลงแล้ว กรุณารีเฟรช" |
| EC-09 | CSV header ไม่ตรง | reject ทั้งไฟล์ + column error |
| EC-10 | CSV row cascade invalid | error รายแถว |
| EC-11 | double-submit | idempotency → 1 รายการ |
| EC-12 | deep-link survey ไม่มี/deleted | "ไม่พบข้อมูลแบบสำรวจที่เลือก" + กลับ list |

> **Note (Export):** List Export CSV = client-side ใน prototype · backend export endpoint + idempotency = **Pending Spec** (TC-606)

## §5.6 Error Catalog
ERR_CASCADE_INVALID "กรุณากรอกข้อมูลให้ครบถ้วน" · ERR_VALIDATION "กรุณาใส่ค่าที่ถูกต้อง" · ERR_REJECT_NO_REASON "กรุณากรอกเหตุผลในการปฏิเสธ" · ERR_STALE(409) "ข้อมูลล้าสมัย กรุณารีเฟรช" · ERR_STATUS_CONFLICT "สถานะเปลี่ยนแปลงแล้ว กรุณารีเฟรช" · ERR_CSV_INVALID "ไฟล์ไม่ถูกต้อง กรุณาอัปโหลดไฟล์ CSV" · ERR_NOT_FOUND "ไม่พบข้อมูลแบบสำรวจที่เลือก"
