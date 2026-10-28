# DOA_BRIEF — F-TMP-007 ใบเดินทางและสถานที่ปฎิบัติงาน  สำหรับ General Trade
> ใบประกาศ doa-declaration v1.2 · Verdict **PASS** · ประกาศเท่านั้น ห้าม hardcode สายในตัว feature · ที่มา: DEC-03, DEC-08, DEC-09 · ค่าเริ่มต้นยังไม่ยืนยัน [DEFAULT — รอยืนยัน]

## 1. Identity
| feature_id | ชื่อ | module | platform | doa_type | scope | โหมด | wire_status |
|---|---|---|---|---|---|---|---|
| F-TMP-007 | ใบเดินทางและสถานที่ปฎิบัติงาน  สำหรับ General Trade | sales | cube_core | `twp` | `document_sign` | **dynamic** — จำนวนขั้น/role ปรับที่ DOA กลางได้ ไม่ต้องแก้ feature | `pending` |

## 2. Approval Actions
| action | trigger | approve | reject |
|---|---|---|---|
| ส่งอนุมัติใบเดินทางและสถานที่ปฎิบัติงาน  สำหรับ General Trade | ผู้ขอกดส่งจาก `draft` | ผ่านขั้นถัดไป · ครบทุกขั้น = `approved` | กลับ `draft` (เลขเดิม) + เหตุผลบังคับ · ประวัติ append-only |
| ยกเลิกระหว่างรอ | owner, admin_role · สถานะ draft, pending | — | เหตุผลบังคับ → `cancelled` |

## 3. Matrix ที่จะไปตั้งค่า (DOA กลาง)
| set | amount_from | amount_to | departments | chainMode | steps |
|---|---|---|---|---|---|
| 1 | 0 บาท | ไม่จำกัด (null) | ทุกแผนก (merged) | sequential | ① `role-line-manager` (ผู้อนุมัติ) `[DEFAULT — รอยืนยัน]` |

ไม่มีวงเงิน — 1 ชุด `0 → null`

## 4. Field Contract (FRD 04_DB)
`approval_required bool` · `approval_status enum(draft|pending_approval|approved|rejected|cancelled)` · `doa_entry_ref string null` · `doa_ref string` · `approver_role string` · `approved_by string` · `approval_chain jsonb (snapshot ตอนส่ง · append-only)` · `approved_at timestamp`
BR-DOA-01 ส่งได้เฉพาะ draft · BR-DOA-02 resolve ตอนส่งแล้ว freeze · BR-DOA-03 reject → draft · BR-DOA-04 ผู้ขอพิจารณาใบตัวเองไม่ได้ · BR-DOA-05 ไม่ใช้ (ไม่มีวงเงิน)

## 5. UI Contract (HTML)
ปุ่มส่งอนุมัติ (draft) · **ตอนส่ง: ทุกช่องตำแหน่งให้ผู้ส่งค้น/เลือก "คน" (avatar + ตำแหน่ง + ชื่อ · มติ 2026-08-17)** · ป้ายสถานะ · Approval Timeline N ขั้น · ปุ่มตัดสินเฉพาะผู้มีสิทธิ์ขั้นปัจจุบัน ใช้คำตาม role · ไม่อนุมัติบังคับเหตุผล · hook My Approval
Mock: `python3 doa_tool.py mock TWP.doa.yaml` → `MOCK_DOA_RESOLVED` + `DECISION_WORDS` + marker `DOA-ENGINE-HOOK`
### 5.1 แบบพิมพ์
ช่องลงชื่อ PDF = ผู้ขอ + 1 ช่องต่อขั้นใน `approval_chain` (**จำนวนตาม DOA ไม่ fix**) แถวละ ≤4 · คำตัดสินผูก role (`print_config.decision_words.by_role`) · print_config `sign_boxes: doa_step:*` (thai-doc v2.1 `sign_rows`)

## 6. Wire Checklist
- [ ] ตั้ง entry ที่ DOA กลางตาม §3 · [ ] dev เรียก `GET /doa/resolve?feature_id=F-TMP-007` ตอนส่ง แล้ว snapshot · [ ] My Approval แสดงใบรอ · [ ] `wire_status: pending → wired`

## 7. Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| INFO | G1 | `role-line-manager` relative role (ผังองค์กร) — ยืนยันกับ DOA กลาง |
| INFO | G8 | ไม่ได้ให้ --print-config — ตรวจ sign_boxes ตอนขั้นแบบพิมพ์ |

## 8. Open Questions
| # | คำถาม | ใครตอบ |
|---|---|---|
| OQ-DOA-1 | role id role-line-manager ตรง master DOA กลางไหม | Strike + พี่เบิร์ด (ก่อน wire) |
| OQ-DOA-2 | ลูกค้ายืนยันสาย/จำนวนขั้นค่าเริ่มต้น (AI-DEFAULT) | ลูกค้า (ใบเซ็น) |
