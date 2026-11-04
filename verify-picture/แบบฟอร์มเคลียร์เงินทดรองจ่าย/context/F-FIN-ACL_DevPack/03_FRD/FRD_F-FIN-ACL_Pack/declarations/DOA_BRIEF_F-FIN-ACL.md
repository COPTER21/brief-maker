# DOA_BRIEF — F-FIN-ACL ใบเคลียร์เงินทดรองจ่าย
> **FINAL v1.0 — ยืนยันกับ FRD_F-FIN-ACL_Pack (frd_lint Section N BLOCK 0)** · ประกาศเท่านั้น ห้าม hardcode สายในตัว feature · ที่มา: DECISIONS.lock DEC-03, DEC-07, DEC-08 (AI-DEFAULT)
> ทำแบบมือ — doa-declaration ที่ติดตั้งเป็น v1.0 (ไม่มี doa_tool.py / references/doa-contract.md) → role id ยังไม่ได้เทียบ master

## 1. Identity
| feature_id | ชื่อ | module | platform | scope |
|---|---|---|---|---|
| F-FIN-ACL | ใบเคลียร์เงินทดรองจ่าย | Finance | Core | `document_sign` |

## 2. Approval Actions
| action | trigger | approve | reject |
|---|---|---|---|
| ส่งเคลียร์เงินทดรองจ่าย | ผู้ขอกด "ส่งอนุมัติ" จาก `draft` (รายการ ≥1 · ยอดเหลือคืน > 0 ต้องแนบสลิป) | ผ่านขั้นถัดไป · ครบทุกขั้น = `approved` (เคลียร์แล้ว) | กลับ `draft` (เลขเดิม) + เหตุผลบังคับ · ประวัติ append-only |

## 3. Matrix ที่จะไปตั้งค่า (DOA กลาง)
| set | amount_from | amount_to | departments | chainMode | steps |
|---|---|---|---|---|---|
| 1 | 0 บาท | null (ไม่จำกัด) | ทุกแผนก (merged) | sequential | ① `role-line-manager` → ② `role-finance-officer` → ③ `role-finance-manager` `[DEFAULT — รอยืนยัน]` |

ไม่มีวงเงิน (DEC-03): ยอดเงินได้รับอนุมัติแล้วที่ใบเบิก (FM-FIN-01) — ใบเคลียร์เป็นการตรวจหลักฐาน · ถ้าลูกค้าต้องการแยกตามยอดใช้เกิน → เพิ่ม set ภายหลังที่ DOA กลาง

## 4. Field Contract (FRD 04_DB · ปฏิเสธ = กลับร่าง ตาม BR-DOA-03 · ขั้น 2 ด่านสลิป = 03 FN-05)
`approval_required bool` · `approval_status enum(draft|pending_approval|approved|rejected|cancelled)` · `doa_entry_ref string null` · `approver_role string` · `approved_by string` · `approval_chain jsonb (snapshot ตอนส่ง · append-only)` · `approved_at timestamp`
BR-DOA-01..04 บังคับ · BR-DOA-05 ไม่ใช้ (ไม่มีวงเงิน)

## 5. UI Contract (HTML)
ปุ่มส่งอนุมัติ (draft) · ป้ายสถานะ · Approval Timeline 3 ขั้น · ตอนส่ง: **ทุกช่องตำแหน่งให้ผู้ส่งค้น/เลือก "คน" ในตำแหน่งนั้น** (avatar + ตำแหน่ง + ชื่อ — มติ 2026-08-17) · ปุ่มพิจารณาเฉพาะผู้มีสิทธิ์ขั้นปัจจุบัน ใช้คำตามขั้น (ขั้น 2 = รับเคลียร์ / ไม่รับเคลียร์) · ไม่อนุมัติบังคับเหตุผล · hook My Approval
Mock ใน HTML: `MOCK_DOA_RESOLVED` + `// TODO: DOA engine`

## 5.1 แบบพิมพ์
ช่องลงชื่อใน PDF FM-FIN-02 วนจาก `approval_chain` — เพิ่ม/ลดขั้นที่ DOA กลางแล้วช่องเพิ่ม/ลดเอง (แถวละ ≤4) · คำตัดสินผูก role (`role-finance-officer` = รับเคลียร์/ไม่รับเคลียร์) ไม่ผูกลำดับขั้น

## 6. Wire Checklist
- [ ] ตั้ง entry ที่ DOA กลางตาม §3 · [ ] dev เรียก `GET /doa/resolve?feature_id=F-FIN-ACL` ตอนส่ง แล้ว snapshot · [ ] My Approval แสดงใบรอ · [ ] `wire_status: pending → wired`

## 7. Open Questions
| # | คำถาม | ใครตอบ |
|---|---|---|
| OQ-DOA-1 | role id `role-line-manager` / `role-finance-officer` / `role-finance-manager` ตรง master DOA จริงไหม | Strike + พี่เบิร์ด (blocking ก่อน wire) |
| OQ-DOA-2 | ลูกค้าต้องการ 3 ขั้นตามกระดาษจริงไหม (ยืนยันในใบเซ็น) | ลูกค้า Credence |
