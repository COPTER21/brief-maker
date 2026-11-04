# DOCCFG_BRIEF — F-FIN-ACL ใบเคลียร์เงินทดรองจ่าย
> **FINAL v1.0 — ยืนยันกับ FRD_F-FIN-ACL_Pack (frd_lint Section N BLOCK 0)** · Auto-register ลง Document Configuration (F003 / F-DOCCFG) ตอน deploy · admin ปรับค่าได้ทุกช่อง
> เลขทุกใบจาก ENG-DOC-NUM เท่านั้น · สำเนาจาก ENG-DOC-STORE เท่านั้น · ทำแบบมือ (ไม่มี doccfg_tool.py) — ยังไม่ได้เช็คชน registry จริง

## doc_type ที่ประกาศ
| Code | ชื่อ | Module | Preset default | Reset | Scope | No-gap | Snap: ส่งออก | Snap: อนุมัติครบ |
|---|---|---|---|---|---|---|---|---|
| ACL | ใบเคลียร์เงินทดรองจ่าย | FIN | {PREFIX}-{YYYY}-{run:4} → ACL-2569-0001 | รายปี | global | ✗ | ✗ | ✓ |

## จุดออกเลข (ENG-DOC-NUM)
| เมื่อไหร่ | อ้าง | หมายเหตุ |
|---|---|---|
| บันทึกครั้งแรก (สร้าง draft) | 03_LOGIC FN-03 · DEC-10 | ไม่อนุมัติ → กลับร่างใช้เลขเดิม · ยกเลิกแล้วเลขไม่นำกลับมาใช้ (no-gap ✗) · เช็คสถานะเปิดใช้ที่ F-DOCCFG ก่อนออกเลข |

## จุดเก็บสำเนา (ENG-DOC-STORE)
| Event | เมื่อไหร่ |
|---|---|
| approved_final | ผ่าน DOA ขั้นสุดท้าย (03_LOGIC FN-05) — เก็บ PDF FM-FIN-02 |

## แบบพิมพ์
print_config: form_code FM-FIN-02 · Rev.00 : 01/07/2569 · Replica · min_rows 10 · sign_boxes ผู้ขอ + 1 ต่อขั้น DOA · ค่าอ่านจาก config: `ExpensePolicy.advance_clear_due_day`, `Company.bank_accounts[purpose=advance_refund]`

## Open
- OQ-CFG-1 รหัส `ACL` ชนกับ doc_type เดิมใน registry ไหม (เช็คที่ f-doccfg ก่อน register) — Strike
