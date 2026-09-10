# DOCCFG_BRIEF — F-HR-EXPENSE · เบิกค่าใช้จ่าย
> ประกาศ doc_type เท่านั้น · auto-register ตอน deploy · เลข/สำเนา จาก ENG-DOC-NUM/STORE — ห้าม format/+1 เอง

## doc_type ที่ประกาศ
| Code | ชื่อ | Module | Preset default | Reset | Scope | No-gap | Snap: ส่งออก | Snap: อนุมัติ+เซ็น |
|---|---|---|---|---|---|---|---|---|
| EXP | ใบเบิกค่าใช้จ่าย (EXP-YYYY-NNNN) | HR | {prefix}-{YYYY พ.ศ.}-{NNNN} | รายปี | branch (company) | yes | — (ใบภายใน) | ✓ (approved_final) |

## trigger ออกเลข
| transition | อ้าง | หมายเหตุ |
|---|---|---|
| pending→approved | PREBRIEF §5 (S-09) | ออกเลขตอน**อนุมัติ** (ไม่ออกตอน draft · no-gap) · `doc_no = ENG-DOC-NUM.next('EXP', company_ctx)` |

## trigger snapshot (ENG-DOC-STORE.store)
| event | อ้าง | flag |
|---|---|---|
| approved_final | ลายเซ็นครบ/อนุมัติสุดท้าย (S-15) | Snap: อนุมัติ+เซ็น ✓ — เก็บสำเนา PDF ใบเบิก |

## กติกา
- เลขทุกใบจาก ENG-DOC-NUM.next() · สำเนาทุกใบจาก ENG-DOC-STORE.store() · reset รายปี พ.ศ. · scope branch (แยกบริษัท)
