# 05_RULES — F-AGM-003 Plot Management

## §5.1 Business Rules (→ invariants §3)
| BR | Rule |
|---|---|
| BR-AGP-01 | quota binding บังคับก่อนกรอกข้อมูลแปลง · ผูก quota_id (read-only) |
| BR-AGP-02 | 1 quota/farmer : N plots (ไม่จำกัด) |
| BR-AGP-03 | create/import → status = Waiting for verify เสมอ |
| BR-AGP-04 | verify มี Confirm · Pass→Verified · Fail→Verification failed + reason |
| BR-AGP-05 | Bulk Fail = เหตุผลเดียวทุกรายการ |
| BR-AGP-06 | edit ไม่เปลี่ยน status อัตโนมัติ |
| BR-AGP-07 | audit ทุก create/edit/verify/delete (actor/time/count) |
| BR-AGP-08 | soft + hard delete + reason |
| BR-AGP-09 | deed_number unique → duplicate reject |
| BR-AGP-10 | CSV partial success + error report |
| BR-AGP-11 | optimistic lock + idempotency ทุก mutation |
| BR-AGP-12 | lat/long เก็บ 6 ทศนิยม |
| BR-AGP-13 | shapefile mandatory · document optional |

## §5.4 Validation Rules (verbatim จาก code)
| VR | Field | Rule | Message |
|---|---|---|---|
| VR-01 | required×14 | ครบ | "กรุณา…" per field |
| VR-02 | latitude | [-90,90] | "พิกัดละติจูดต้องอยู่ระหว่าง -90 ถึง 90" |
| VR-03 | longitude | [-180,180] | "พิกัดลองจิจูดต้องอยู่ระหว่าง -180 ถึง 180" |
| VR-04 | postal_code | 5 digits | "รหัสไปรษณีย์ต้องเป็นตัวเลข 5 หลัก" |
| VR-05 | area_rai | > 0 | "พื้นที่ต้องเป็นตัวเลขที่มากกว่า 0" |
| VR-06 | shapefile | มี | "กรุณาแนบไฟล์ลักษณะแปลง (Shapefile)" |
| VR-07 | deed_number | unique | "เลขที่เอกสารสิทธิ์ซ้ำ" |
| VR-08 | quota | เลือกก่อน | "ไม่พบโควตาที่ตรงกับหมายเลขที่กรอก" |
| VR-09 | fail_reason | บังคับเมื่อ Fail | "กรุณากรอกเหตุผล" |
| VR-10 | postal↔ตำบล | match | auto |
| VR-11 | address_line/deed_owner | ≤255 | "ความยาวเกิน" (TC-463) |
| VR-12 | cascade reset | เปลี่ยนจังหวัด→เคลียร์อำเภอ/ตำบล/postal | — |
| VR-13 | latitude/longitude | รับค่า/แสดงผล 6 ทศนิยม (decimal(9,6) · BR-AGP-12) | "พิกัดแสดง 6 ทศนิยม" |

## §5.2 State Machine (LOCK-02)
Waiting for verify --pass--> Verified · --fail(+reason)--> Verification failed · edit → status คงเดิม · Verified/failed → verify ซ้ำไม่ได้ (409) · any → soft/hard delete (audit)

## §5.3 Permission (→ invariants §6)
Field Officer: create/edit/delete/import/export · Admin/Steward: +verify/bulk · ปุ่มซ่อนตาม RBAC · SoD flag (OQ-P7)

## §5.5 Edge Cases
| EC | Case | Expected |
|---|---|---|
| EC-01 | quota ไม่พบ | inline error, block create |
| EC-02 | shapefile ไม่แนบ | VR-06 block |
| EC-03 | lat/long นอกช่วง | VR-02/03 |
| EC-04 | area = 0 / ติดลบ / ข้อความ | VR-05 |
| EC-05 | postal ≠ 5 หลัก | VR-04 |
| EC-06 | deed ซ้ำ (form/CSV/DB race) | reject "เลขที่เอกสารสิทธิ์ซ้ำ" |
| EC-07 | verify fail ไม่ใส่เหตุผล | VR-09 block |
| EC-08 | bulk เลือกทั้งหมด = เฉพาะ waiting | disabled แถวอื่น |
| EC-09 | bulk partial (บางรายการ verified แล้ว) | success/failed list + retry |
| EC-10 | edit ระเบียน verified | อนุญาต, status คงเดิม (OQ-P1) |
| EC-11 | delete ระเบียน verified | อนุญาต + audit (OQ-P2) |
| EC-12 | stale edit (version เก่า) | 409 "ข้อมูลล้าสมัย กรุณารีเฟรช" |
| EC-13 | concurrent verify (status เปลี่ยนแล้ว) | 409 "สถานะเปลี่ยนแปลงแล้ว กรุณารีเฟรช" |
| EC-14 | CSV header ไม่ตรง | reject ทั้งไฟล์ + column error |
| EC-15 | CSV lat/long/postal นอกเกณฑ์ | error รายแถว |
| EC-16 | double-submit create | idempotency → 1 รายการ |
| EC-17 | deep-link plot ไม่มี/ถูกลบ | 404 "ไม่พบข้อมูลแปลงที่เลือก" + กลับ list |
| EC-18 | quota ถูกลบหลังผูก | plot คง quota_no snapshot + flag |

## §5.6 Error Catalog
ERR_QUOTA_NOT_FOUND "ไม่พบโควตาที่ตรงกับหมายเลขที่กรอก" · BR_DEED_DUPLICATE "เลขที่เอกสารสิทธิ์ซ้ำ" · ERR_VALIDATION_FAILED (รายช่อง) · BR_VERIFY_FAIL_NO_REASON "กรุณากรอกเหตุผล" · ERR_STALE_DATA(409) "ข้อมูลล้าสมัย กรุณารีเฟรช" · BR_STATUS_CONFLICT "สถานะเปลี่ยนแปลงแล้ว กรุณารีเฟรช" · ERR_SHAPEFILE_REQUIRED "กรุณาแนบไฟล์ลักษณะแปลง (Shapefile)" · ERR_CSV_INVALID "ไฟล์ไม่ถูกต้อง กรุณาอัปโหลดไฟล์ CSV" · ERR_NOT_FOUND "ไม่พบข้อมูลแปลงที่เลือก"
