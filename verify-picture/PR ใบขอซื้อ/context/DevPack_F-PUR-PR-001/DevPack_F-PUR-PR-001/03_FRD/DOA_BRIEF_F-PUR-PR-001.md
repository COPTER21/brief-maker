# DOA_BRIEF — F-PUR-PR · PR ใบขอซื้อ
> feature ประกาศเท่านั้น — สายอนุมัติจริงตั้งที่ DOA กลาง (F-DLG-001 / F019 DONE) · ห้าม hardcode ใน feature
> wire_status: **pending**

## §1 Identity
| key | value |
|---|---|
| feature_id | F-PUR-PR (fid F072) |
| name | PR ใบขอซื้อ (Purchase Requisition) |
| module | Purchase |
| platform | CUBE 4.0 web |
| scope | Phase A (direction) — ประกาศ + UI contract · ยังไม่ wire engine |
| **มีวงเงินหรือไม่** | **มี** (PR/PO เป็นกลุ่มมีวงเงิน) → matrix ต้องแบ่งช่วงเงิน |

## §2 Approval Actions
| Action | Trigger | ผล approve | ผล reject |
|---|---|---|---|
| ส่งอนุมัติใบขอซื้อ | ผู้ขอกด "ส่งอนุมัติ" ที่ wizard step 5 (สถานะ DRAFT เท่านั้น) | ทุก slot ครบ → `APPROVED` · ยิง `pr_approved` (NTF) + `doc.approved` (CSQ) | `REJECTED` + เหตุผลบังคับ · ผู้ขอคัดลอกไปแก้ใหม่ |
| เรียกคืน (recall) | ผู้ขอ ขณะ `PENDING_APPROVAL` | กลับ `DRAFT` · ลายเซ็นที่ลงแล้ว void (คงอยู่ในประวัติ) | — |
| ยกเลิกใบที่อนุมัติแล้ว | ผู้มีสิทธิ์ · ต้องยังไม่มี PO อ้าง | `CANCELLED` + เหตุผล | — |

## §3 Matrix ที่จะไปตั้งค่าที่ DOA กลาง  `[DEFAULT — รอยืนยัน]`
| set | amount_from (บาท) | amount_to (บาท) | departments | chainMode | steps[roles] |
|---|---|---|---|---|---|
| S1 | 0 | 50,000 | ALL | sequential | 1) `role-head-dept` |
| S2 | 50,000.01 | 500,000 | ALL | sequential | 1) `role-head-dept` → 2) `role-mgr-pur` |
| S3 | 500,000.01 | null (ไม่จำกัด) | ALL | sequential | 1) `role-head-dept` → 2) `role-mgr-pur` → 3) `role-cfo` |
> G3 check: ช่วงต่อเนื่อง ไม่ทับ ไม่มีรู ✓ · `amount_to: null` = ไม่จำกัด ✓ · ทุก role เป็น `role-*` ✓
> ตัวเลขทั้ง 3 ช่วงเป็น default ที่ lane เสนอ — **คนตั้งค่าจริงแก้ได้ที่หน้า DOA กลาง** feature ไม่รู้ตัวเลขนี้

## §4 Field Contract (สำหรับ FRD Phase B)
| field | type | nullable | หมายเหตุ |
|---|---|---|---|
| approval_required | bool | ✗ | จาก DOA entry ไม่ใช่ค่าคงที่ |
| approval_status | enum | ✗ | draft \| pending_approval \| approved \| rejected \| cancelled |
| doa_entry_ref | string | ✓ | FK ทะเบียน DOA (nullable Phase A) |
| approver_role | string | ✓ | role ขั้นปัจจุบัน (resolve จาก DOA) |
| approved_by | string | ✓ | user id ที่เซ็นจริง |
| approval_chain | jsonb | ✗ | **snapshot ตอนส่งอนุมัติ · append-only** |
| approved_at | timestamp | ✓ | |

## §5 UI Contract (บังคับใน HTML)
| ส่วน | รายละเอียด |
|---|---|
| ปุ่ม "ส่งอนุมัติ" | เฉพาะ `DRAFT` · disabled จนกรอกครบ + มี ≥1 บรรทัด |
| Badge สถานะ | ร่าง / รออนุมัติ / อนุมัติแล้ว / ไม่อนุมัติ / ยกเลิก — สี CI Warm Light |
| **DOA slot picker (locked 2026-08-17)** | step 5 · ต่อ slot เลือก **คนจริง**: avatar + ชื่อ + ตำแหน่ง — **ห้ามแสดง role ID ลอย** |
| Approval Timeline / tab ลายเซ็น | การ์ดต่อขั้น: ชื่อ+ตำแหน่ง+avatar → เวลา (ค.ศ.) → สถานะ (รอ/ผ่าน/ตีกลับ) + เหตุผล |
| ปุ่มอนุมัติ / ไม่อนุมัติ | เฉพาะผู้มีสิทธิ์ในขั้นปัจจุบัน · ไม่อนุมัติ = บังคับใส่เหตุผล |
| Hook My Approval | ใบ `pending_approval` ต้องโผล่กล่อง My Approval (mock) |
| mock ใน HTML | `MOCK_DOA_RESOLVED` **มี ≥2 tier** (มีวงเงิน) + `// TODO: DOA engine` |

## §6 Wire Checklist (pending → wired)
- [ ] สร้าง DOA entry ของ F-PUR-PR ที่หน้า DOA กลาง ตาม matrix §3
- [ ] replace `MOCK_DOA_RESOLVED` ด้วย resolve จริง ณ เวลา submit
- [ ] snapshot `approval_chain` ตอน submit แล้ว freeze (BR-DOA-02)
- [ ] BR-DOA-04 ผู้ขอเซ็นใบตัวเองไม่ได้
- [ ] BR-DOA-05 แก้ยอดหลังส่ง → re-resolve สาย (feature นี้มีวงเงิน)

## §7 Open Questions
| OQ | เรื่อง | ใครตอบ | default ที่ใช้ไปก่อน |
|---|---|---|---|
| OQ-DOA-1 | ตัวเลขวงเงิน 3 ช่วงจริง | ผู้บริหารจัดซื้อ / พี่เบิร์ด | 50,000 / 500,000 `[ASSUMED]` |
| OQ-DOA-2 | แยก matrix รายหน่วยงานไหม | เจ้าของกระบวนการ | ALL (ชุดเดียว) `[ASSUMED]` |
| OQ-DOA-3 | ยกเลิกใบที่อนุมัติแล้วต้องอนุมัติซ้ำไหม | เจ้าของกระบวนการ | ไม่ต้อง · แค่เหตุผล + confirm `[ASSUMED]` |
