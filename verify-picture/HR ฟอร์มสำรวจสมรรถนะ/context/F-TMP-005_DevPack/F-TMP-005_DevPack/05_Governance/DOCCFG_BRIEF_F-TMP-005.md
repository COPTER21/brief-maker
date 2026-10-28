# DOCCFG_BRIEF — F-TMP-005
> **FINAL v1.0 — ยืนยันกับ FRD** · doccfg-declaration v2.1 · Verdict **PASS**
> Auto-register ลง Document Configuration (F003 / F-DOCCFG) ตอน deploy · admin ปรับค่าได้ทุกช่อง · เลขจาก ENG-DOC-NUM เท่านั้น · สำเนาจาก ENG-DOC-STORE เท่านั้น — ห้าม hardcode

## doc_type ที่ประกาศ
| Code | ชื่อ | Module | Preset default | Reset | Scope | No-gap | Snap: ส่งออก | Snap: อนุมัติครบ |
|---|---|---|---|---|---|---|---|---|
| CMP | แบบฟอร์มสำรวจสมรรถนะ | HR | {PREFIX}-{YYYY}-{run:4} | รายปี | global | ✗ | ✗ | ✓ |

## จุดออกเลข (ENG-DOC-NUM)
| เมื่อไหร่ | อ้าง FRD | หมายเหตุ |
|---|---|---|
| บันทึกครั้งแรก (สร้างร่าง) | 03_LOGIC FN-01 | CMP · เช็คสถานะเปิดใช้ที่ F-DOCCFG ก่อนออกเลข · ไม่อนุมัติแล้วกลับร่างใช้เลขเดิม |

## จุดเก็บสำเนา (ENG-DOC-STORE)
| Event | Code | อ้าง FRD |
|---|---|---|
| approved_final | CMP | 03_LOGIC FN-07 |

## แบบพิมพ์ (print_config → F-DOCCFG)
- **CMP** form_code FM-HRM-40 · REV.00 : 01/07/2569 · min_rows 6 · header `organization_snapshot_at_numbering` · ช่องลงชื่อ requester, doa_step:* (แถวละ ≤4) · คำตัดสินตาม role: `role-line-manager` = เห็นชอบ/ส่งกลับแก้ไข · ไฟล์ `print/print_config.json`

## Dev wiring note
- `doc.no = ENG-DOC-NUM.next('<CODE>', company_ctx)` ที่จุดออกเลข — ห้าม format เอง ห้าม +1 เอง
- render PDF จาก template + data contract แล้ว `ENG-DOC-STORE.store(pdf, '<CODE>', id, event)` — engine เช็ค flag เอง
- ช่องลงชื่อ PDF วนจาก `approval_chain` (thai-doc v2.1 `sign_rows`) — ห้าม fix จำนวน

## Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| PASS | D1–D8 | ผ่านทุกข้อ |
