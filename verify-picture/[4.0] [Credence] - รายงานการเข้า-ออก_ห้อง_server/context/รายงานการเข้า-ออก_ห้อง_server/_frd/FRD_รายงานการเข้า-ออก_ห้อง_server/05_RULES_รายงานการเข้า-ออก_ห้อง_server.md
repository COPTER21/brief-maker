# 05_RULES — F-TMP-006

## §5.1 Business Rules
| ID | Rule | Tag | ที่มา |
|---|---|---|---|
| BR-01 | เกณฑ์เวลาอยู่ในห้องอ่านจาก ServerRoomAccessConfig.max_stay_hours (ค่าเริ่ม 12) | CONFIGURABLE | DEC-04 |
| BR-02 | อยู่นานเกินเกณฑ์ / ผู้เข้าคนเดิมมีแถวค้างซ้อน → เตือน + ไฮไลต์ · ไม่บล็อก | CONFIGURABLE [AI-DEFAULT] | DEC-04 · DEC-12 (VALID) |
| BR-03 | แถวใหม่ → sral_certify_pending · เกินเวลา → sral_overstay ถึง admin role ฝ่าย IT | CONFIGURABLE | DEC-04 · NTF |
| BR-04 | ลายเซ็นผู้เข้า = ลงชื่อในระบบตอนบันทึก (ผู้บันทึก + เวลา · ไม่ใช้ภาพ) | FIXED [AI-DEFAULT] | DEC-07 |
| BR-05 | รับรองรายแถว: role-it-officer/admin role · ผู้รับรอง ≠ ผู้เข้า · แถวออกแล้ว · เอกสาร draft · ชื่อ+เวลาลงแถว (ไม่ใช้ภาพ) | FIXED [AI-DEFAULT] | DEC-07 · DEC-13 (VALID) |
| BR-06 | ช่อง 1:1 ตามกระดาษ 9 คอลัมน์ · ไม่เพิ่มช่อง · ตัดช่องว่างท้ายหัว "เหตุผลการเข้าใช้" | FIXED [AI-DEFAULT] | DEC-06 · DEC-14 (VALID) |
| BR-07 | แถวไม่จำกัด · PDF ≥ 21 แถว · 12 แถว/หน้า · หัวตารางซ้ำ · ไม่มีบล็อกลงชื่อท้ายใบ | FIXED | DEC-05 · DEC-07 |
| BR-08 | แนบไฟล์ระดับใบ (ไม่บังคับ) · CSV ✓ · ทำซ้ำ ✗ | FIXED [AI-DEFAULT] | DEC-10 |
| BR-09 | เลขออกตอนบันทึกครั้งแรก (SRAL) | FIXED | DEC-09 |
| BR-10 | submitted ล็อกแก้ไข · ยกเลิกได้ (draft/submitted) โดยเจ้าของหรือ admin role · เหตุผลบังคับ | FIXED [AI-DEFAULT] | G7 (raw) |
| BR-11 | ไม่เปลี่ยนค่าในระบบ · ไม่ส่งต่อระบบอื่น (ไม่เชื่อมระบบประตู/บัตร) | FIXED | DEC-01 · DEC-02 |
| BR-12 | การมองเห็น: เจ้าของ · admin role ฝ่าย IT เห็นทั้งหมด · ร่างไม่รั่วให้คนอื่น | FIXED | DEC-08 |
| BR-13 | ส่ง = ปิดรอบทันที · ไม่มีขั้นพิจารณาเอกสาร (กระดาษไม่มีช่องลงชื่อผู้พิจารณาท้ายใบ) · ต้องการขั้นพิจารณาก่อนเข้าห้อง = enhancement + DOA_BRIEF (OQ-02) | FIXED [AI-DEFAULT] | DEC-03 · DEC-11 (VALID) |
| BR-14 | ส่งปิดรอบต้องครบ: ทุกแถวมีวันเวลาออก + ผู้รับรอง · วันเวลาออกก่อนเข้า = บล็อก · แถวที่รับรองแล้วแก้/ลบไม่ได้ | FIXED [AI-DEFAULT] | DEC-04 · DEC-12 |

## §5.2 State Machine
| จาก | event | ไป | guard |
|---|---|---|---|
| — | save | draft | FN-03 ออกเลข |
| draft | save entries | draft | owner |
| draft | certify entry | draft | role-it-officer ≠ ผู้เข้า · แถวออกแล้ว (FN-10) |
| draft | submit | submitted | owner · ออกครบ + รับรองครบ · FN-08 sral_submitted |
| draft/submitted | cancel | cancelled | owner/admin role · เหตุผล · FN-08 sral_cancelled |

## §5.3 Permission Matrix
| Action | owner | role-it-officer อื่น | admin role IT | อื่น |
|---|:-:|:-:|:-:|:-:|
| ดู draft | ✓ | ✗ | ✓ | ✗ |
| ดู submitted/cancelled | ✓ | ✗ | ✓ | ✗ |
| สร้าง/แก้ draft | ✓ | ✗ | ✗ | ✗ |
| รับรองแถว (≠ ผู้เข้า) | ✓ | ✗ (มองไม่เห็นใบ) | ✓ | ✗ |
| ส่งปิดรอบ | ✓ | ✗ | ✗ | ✗ |
| ยกเลิก | ✓ | ✗ | ✓ | ✗ |

## §5.4 Validation Rules
| VR | ช่อง | เงื่อนไข | ข้อความ |
|---|---|---|---|
| VR-01 | ใบ | ≥ 1 แถวที่บันทึก | บันทึกการเข้าห้องอย่างน้อย 1 ครั้ง |
| VR-02 | visitor_name · visitor_department · in_date · in_time · purpose | required · เวลา HH:MM | กรอกชื่อ–นามสกุล · ฝ่าย/แผนก · วันที่และเวลาที่เข้า (HH:MM) · เหตุผลการเข้าใช้ ให้ครบทุกแถวที่บันทึก |
| VR-03 | out_date · out_time | กรอกคู่กัน · ≥ วันเวลาเข้า | วันเวลาที่ออกต้องไม่ก่อนวันเวลาที่เข้า |
| VR-04 | in_date · out_date | ≤ วันนี้ | (ปฏิทินปิดวันอนาคต · API 422 FUTURE_DATE) |
| VR-05 | เหตุผลยกเลิก | required | กรุณาระบุเหตุผล |
| VR-06 | ส่งปิดรอบ | status = draft · ผู้ส่ง = owner · ออกครบ + รับรองครบ | ยังส่งปิดรอบไม่ได้ — ยังไม่บันทึกเวลาออก N รายการ · ยังไม่รับรอง N รายการ |

## §5.5 Edge Cases
| EC | กรณี | ผล | อ้าง |
|---|---|---|---|
| EC-01 | ผู้เข้ายังอยู่ในห้อง | บันทึกร่างได้ · รับรองไม่ได้ · ปิดรอบไม่ได้ | BR-14 |
| EC-02 | อยู่ข้ามคืน | วันที่ออกคนละวันได้ · ชั่วโมงคิดข้ามวัน | FN-02 |
| EC-03 | อยู่เกิน 12 ชม. | ไฮไลต์ + sral_overstay · ไม่บล็อก | BR-02/03 |
| EC-04 | เจ้าหน้าที่ IT เข้าห้องเอง | owner รับรองไม่ได้ → admin role รับรอง | BR-05 |
| EC-05 | บุคคลภายนอก | พิมพ์ชื่อเอง · visitor_emp_id = null · ฝ่าย = บริษัท | FN-02 |
| EC-06 | > 24 แถว | PDF หน้า 3 อัตโนมัติ · dense | BR-07 |
| EC-07 | stale write | 409 → toast รีเฟรช | §2.3 |
| EC-08 | doc_type ปิดใช้ | ปุ่มสร้าง disabled | FN-03 |
| EC-09 | ลูกค้าต้องการขั้นพิจารณาก่อนเข้าห้องภายหลัง | enhancement: DOA_BRIEF + field สายพิจารณา · template แบบพิมพ์รองรับ sign_rows แล้ว | BR-13 · DEC-11 |
| EC-10 | แก้แถวที่รับรองแล้ว | 409 ENTRY_CERTIFIED · จอล็อกช่อง | BR-14 |
