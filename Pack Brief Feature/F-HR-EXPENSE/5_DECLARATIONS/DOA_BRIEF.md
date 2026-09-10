# DOA_BRIEF — F-HR-EXPENSE · เบิกค่าใช้จ่าย
> ประกาศเท่านั้น · ห้าม hardcode สาย/วงเงินใน feature — ตั้งที่ DOA กลาง · resolve ตอนส่ง freeze · แก้ยอดข้ามช่วง = re-resolve

## 1. Identity
feature_id: F-HR-EXPENSE · name: เบิกค่าใช้จ่าย · module: HR · scope: อนุมัติใบเบิก **ตามวงเงิน (มีวงเงิน)**

## 2. Approval Actions
| action | trigger | approve | reject |
|---|---|---|---|
| อนุมัติใบเบิก | submitted→pending (S-01) | ออกเลข EXP + PDF · FC/EC · hook จ่าย | ตีกลับ (rejected)→แก้ยื่นใหม่ (S-06) |

## 3. Matrix ที่จะไปตั้งค่า (มีวงเงิน · หลายชั้น)  **[ASSUMED A-EXP-03 · DEFAULT — รอยืนยัน]**
| set | amount_from | amount_to | departments | chainMode | steps[roles] |
|---|---|---|---|---|---|
| tier1 | 0 | 5,000 (บาท) | ทุกแผนก | sequential | [`role-line-manager`] |
| tier2 | 5,000 | 50,000 | ทุกแผนก | sequential | [`role-line-manager`, `role-dept-manager`] |
| tier3 | 50,000 | null (ไม่จำกัด) | ทุกแผนก | sequential | [`role-line-manager`, `role-dept-manager`, `role-director`] |
> ยิ่งยอดสูงยิ่งเซ็นหลายชั้น · จุดตัดตามยอดรวมใบเบิก · **feature ส่งยอดรวมให้ DOA resolve — ไม่ตัดสินสายเอง**

## 4. Field Contract
- approver_role · approval_chain jsonb (snapshot · append-only) · doa_resolved_at · **doc_total** (ยอดที่ใช้ resolve · re-resolve เมื่อแก้ข้ามช่วง BR-05)

## 5. UI Contract
- ปุ่ม "ส่งอนุมัติ" → slot picker ตามตำแหน่งในสายที่ resolve (avatar+ตำแหน่ง+ชื่อ · มติ 17ส.ค.) · timeline สถานะ · My Approval hook · sign tab

## 6. Wire Checklist
- [ ] ตั้ง DOA entry 3 tiers · [ ] GET /doa/resolve ส่ง doc_total · [ ] re-resolve เมื่อแก้ยอดข้ามช่วง · [ ] snapshot chain → wired

## 7. Open Questions
- **A-EXP-03** (พี่เบิร์ด): ยืนยันช่วงวงเงิน/ผู้เซ็นแต่ละชั้น (ตัวเลข default ข้างบนรอเคาะ)
