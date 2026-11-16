# DOA_BRIEF — F-TMP-004 แบบประเมินและคัดเลือกผู้ขาย/ผู้ให้บริการ ประจำปี
> ใบประกาศ doa-declaration v1.2 · Verdict **WARN** · ประกาศเท่านั้น ห้าม hardcode สายในตัว feature · ที่มา: DEC-03, DEC-07, DEC-08, DEC-14 · ค่าเริ่มต้นยังไม่ยืนยัน [DEFAULT — รอยืนยัน]

## 1. Identity
| feature_id | ชื่อ | module | platform | doa_type | scope | โหมด | wire_status |
|---|---|---|---|---|---|---|---|
| F-TMP-004 | แบบประเมินและคัดเลือกผู้ขาย/ผู้ให้บริการ ประจำปี | purchase | core | `vev` | `document_sign` | **dynamic** — จำนวนขั้น/role ปรับที่ DOA กลางได้ ไม่ต้องแก้ feature | `pending` |

## 2. Approval Actions
| action | trigger | approve | reject |
|---|---|---|---|
| ส่งอนุมัติแบบประเมินและคัดเลือกผู้ขาย/ผู้ให้บริการ ประจำปี | ผู้ขอกดส่งจาก `draft` | ผ่านขั้นถัดไป · ครบทุกขั้น = `approved` | กลับ `draft` (เลขเดิม) + เหตุผลบังคับ · ประวัติ append-only |
| ยกเลิกระหว่างรอ | owner, admin_role · สถานะ draft, pending | — | เหตุผลบังคับ → `cancelled` |

## 3. Matrix ที่จะไปตั้งค่า (DOA กลาง)
| set | amount_from | amount_to | departments | chainMode | steps |
|---|---|---|---|---|---|
| 1 | 0 บาท | ไม่จำกัด (null) | ทุกแผนก (merged) | sequential | ① `role-pur-officer` (ผู้จัดทำ (แผนกจัดซื้อ)) → ② `role-mgr-pur` (อนุมัติ (ผู้จัดการแผนกจัดซื้อ)) `[DEFAULT — รอยืนยัน]` |

ไม่มีวงเงิน — 1 ชุด `0 → null` · คำตัดสินเฉพาะ role: `role-pur-officer` = เห็นด้วย (Agree / Acknowledge) / ไม่เห็นด้วย (Not Agree) · `role-mgr-pur` = อนุมัติ (Approve) / ไม่อนุมัติ ( Not Approve)

## 4. Field Contract (FRD 04_DB)
`approval_required bool` · `approval_status enum(draft|pending_approval|approved|rejected|cancelled)` · `doa_entry_ref string null` · `doa_ref string` · `approver_role string` · `approved_by string` · `approval_chain jsonb (snapshot ตอนส่ง · append-only)` · `approved_at timestamp`
BR-DOA-01 ส่งได้เฉพาะ draft · BR-DOA-02 resolve ตอนส่งแล้ว freeze · BR-DOA-03 reject → draft · BR-DOA-04 ผู้ขอพิจารณาใบตัวเองไม่ได้ · BR-DOA-05 ไม่ใช้ (ไม่มีวงเงิน)

## 5. UI Contract (HTML)
ปุ่มส่งอนุมัติ (draft) · **ตอนส่ง: ทุกช่องตำแหน่งให้ผู้ส่งค้น/เลือก "คน" (avatar + ตำแหน่ง + ชื่อ · มติ 2026-08-17)** · ป้ายสถานะ · Approval Timeline N ขั้น · ปุ่มตัดสินเฉพาะผู้มีสิทธิ์ขั้นปัจจุบัน ใช้คำตาม role · ไม่อนุมัติบังคับเหตุผล · hook My Approval
Mock: `python3 doa_tool.py mock VEV.doa.yaml` → `MOCK_DOA_RESOLVED` + `DECISION_WORDS` + marker `DOA-ENGINE-HOOK`
### 5.1 แบบพิมพ์
ช่องลงชื่อ PDF = ผู้ขอ + 1 ช่องต่อขั้นใน `approval_chain` (**จำนวนตาม DOA ไม่ fix**) แถวละ ≤4 · คำตัดสินผูก role (`print_config.decision_words.by_role`) · print_config `sign_boxes: doa_step:*` (thai-doc v2.1 `sign_rows`)

## 6. Wire Checklist
- [ ] ตั้ง entry ที่ DOA กลางตาม §3 · [ ] dev เรียก `GET /doa/resolve?feature_id=F-TMP-004` ตอนส่ง แล้ว snapshot · [ ] My Approval แสดงใบรอ · [ ] `wire_status: pending → wired`

## 7. Quality Gate
| ระดับ | ข้อ | รายละเอียด |
|---|---|---|
| WARN | G1 | set 1: `role-pur-officer` ไม่อยู่ใน contract — เทียบ master DOA กลาง (--roles) ก่อน wire |

## 8. Open Questions
| # | คำถาม | ใครตอบ |
|---|---|---|
| OQ-DOA-1 | role id role-pur-officer ตรง master DOA กลางไหม | Strike + พี่เบิร์ด (ก่อน wire) |
| OQ-DOA-2 | ลูกค้ายืนยันสาย/จำนวนขั้นค่าเริ่มต้น (AI-DEFAULT) | ลูกค้า (ใบเซ็น) |

## 9. ขั้นตามเงื่อนไขผลประเมิน (DEC-14 · TODO: DOA engine)
| เงื่อนไข | เพิ่มขั้น | role | คำตัดสิน | สถานะ |
|---|---|---|---|---|
| `eval_result == fail` (คะแนนรวม < pass_threshold ของ VendorEvaluationConfig) | ต่อท้ายขั้นสุดท้าย | role-gm (ผู้บริหาร — ค่าเสนอ AI-DEFAULT · อาจเป็น role-proc-dir) | อนุมัติ (Approve) / ไม่อนุมัติ ( Not Approve) | proposed |
- ที่มา: หมายเหตุบนกระดาษ "กรณีประเมินได้ต่ำกว่า 6 คะแนน / ผู้จัดการฝ่ายจัดซื้อ และผู้บริหาร จะต้องเป็นผู้พิจารณาคัดเลือก…" — กระดาษไม่มีช่องลงชื่อผู้บริหาร
- DOA กลาง (matrix ตามวงเงิน) ยังไม่รองรับเงื่อนไขที่ไม่ใช่วงเงิน → feature ส่ง `eval_result` เป็น context ตอน resolve · ห้าม hardcode ขั้นใน feature · prototype จำลองด้วย `MOCK_DOA_CONDITIONAL`
- OQ-DOA-3: DOA กลางรองรับ condition ตาม field ของเอกสาร (eval_result) ไหม · ถ้าไม่ → ทางเลือก: ตั้ง 2 entry (ผ่าน/ไม่ผ่าน) แล้ว feature เลือก entry ตามผล (Strike + พี่เบิร์ด ก่อน wire)
