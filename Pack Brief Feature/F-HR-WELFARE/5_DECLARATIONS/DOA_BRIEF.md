# DOA_BRIEF — F-HR-WELFARE · สวัสดิการ
> feature ประกาศเท่านั้น · ห้าม hardcode สายอนุมัติ — ตั้งค่าจริงที่หน้า DOA กลาง · resolve ตอนส่ง แล้ว freeze

## 1. Identity
feature_id: F-HR-WELFARE · name: สวัสดิการ · module: HR · platform: CUBE 4.0 · scope: อนุมัติ "คำขอใช้สิทธิ์สวัสดิการ"

## 2. Approval Actions
| action | trigger | ผล approve | ผล reject |
|---|---|---|---|
| อนุมัติคำขอใช้สิทธิ์ | คำขอ: submitted → pending_approval (S-07) | ตัดคงเหลือ + บันทึกการใช้ (recorded) + ยิง CSQ EC + NTF + hook จ่าย | ไม่ตัดคงเหลือ · rejected · NTF ผู้ยื่น (S-11) |

## 3. Matrix ที่จะไปตั้งค่า (กรอกลงหน้า DOA กลาง)  **[ASSUMED A-WEL-03 · DEFAULT — รอยืนยัน]**
| set | amount_from | amount_to | departments | chainMode | steps[roles] |
|---|---|---|---|---|---|
| default | 0 (บาท) | null (ไม่จำกัด) | ทุกแผนก | sequential 1 สาย | [`role-hr-line-manager`, `role-hr-welfare-admin`] |
> **ไม่มีวงเงิน** (สวัสดิการไม่ผูกจุดตัดยอดเงิน — ต่างจาก Expense Claim ที่มี threshold) · จุดตัดเดียว · หัวหน้าสายงาน → HR สวัสดิการ

## 4. Field Contract สำหรับ FRD
- approver_role string · approval_chain jsonb (snapshot สาย resolve ตอนส่ง · append-only) · doa_resolved_at timestamp · **ไม่มี field จำนวนเงินใน doa_resolve_payload** (ไม่มีวงเงิน)

## 5. UI Contract สำหรับ HTML
- ปุ่ม "ส่งอนุมัติ" → slot picker เลือกคนในตำแหน่ง (avatar + ตำแหน่ง + ชื่อ · มติ 2026-08-17 · ไม่ใช่ role id ลอย) · timeline สถานะอนุมัติ · hook "งานอนุมัติของฉัน" (My Approval)

## 6. Wire Checklist
- [ ] ตั้ง DOA entry ของ F-HR-WELFARE ที่หน้า DOA กลาง (matrix §3) · [ ] เชื่อม GET /doa/resolve ตอนส่ง · [ ] snapshot chain · [ ] My Approval hook → wire_status: pending → wired

## 7. Open Questions
- **A-WEL-03** (owner: พี่เบิร์ด): ยืนยันสาย หัวหน้า→HR สวัสดิการ · ไม่มีวงเงิน — ถ้าบางประเภท (เช่น กองทุน) ต้องผ่านคนอื่น ให้แยก set
