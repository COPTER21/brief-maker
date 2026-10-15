# PREBRIEF — F-PUR-PR · PR ใบขอซื้อ
source of truth เชิง business · lane CUBE-LANE-W2-PUR-LITE · P1 · 2026-09-10 · mode direction

## 1. สรุปฟีเจอร์
ใบขอซื้อ (Purchase Requisition) = เอกสารธุรกรรมต้นทางของสาย P2P — ผู้ขอระบุว่าต้องการซื้ออะไร เท่าไร ใช้เมื่อไร ลงศูนย์ต้นทุนไหน
ส่งเข้าสายอนุมัติตามวงเงิน (DOA) เมื่ออนุมัติครบใบ PR พร้อมให้ Compare Vendors (F073) และ PO (W3) ดึงไปใช้
**archetype = Q-document เต็มรูป** (Pattern Q + B2 v2 line editor)

## 2. State machine (append-only audit ทุก transition)
```
DRAFT ──submit──► PENDING_APPROVAL ──approve(ครบทุก slot)──► APPROVED ──(hook)──► [Compare/PO ปลายทาง]
  ▲                    │                                          │
  │                    ├──reject(+เหตุผล)──► REJECTED ──แก้ใหม่──► DRAFT (copy)
  │                    └──recall(ผู้ขอ)────► DRAFT
  └──cancel──► CANCELLED (จาก DRAFT เท่านั้น)
APPROVED ──cancel(+เหตุผล · ต้องยังไม่มี PO อ้าง)──► CANCELLED
```
กติกา: แก้ยอด/บรรทัดหลังส่งอนุมัติ = ต้อง recall กลับ DRAFT แล้ว submit ใหม่ (re-approve) — ห้ามแก้ระหว่าง PENDING

## 3. หน้าจอ (3 จอ ตาม LOCK-Q)
### 3.1 List (Pattern Q landing · lean list ห้ามซ้อนคอลัมน์ #103)
- คอลัมน์: เลขที่ PR · วันที่เอกสาร · ผู้ขอ (avatar+ชื่อ) · หน่วยงาน · วันที่ต้องการใช้ · มูลค่ารวม · สถานะ (chip)
- toolbar: ค้นหา · filter สถานะ/ช่วงวันที่/หน่วยงาน/ผู้ขอ · ปุ่ม "สร้างใบขอซื้อ"
- แถบ "เอกสารแนบ" ใน landing (Pattern Q #98) — รวมไฟล์แนบทุกใบที่เห็นได้
- row action: เปิดดู · คัดลอกใบ · (DRAFT) แก้ไข/ลบ
- empty / loading / error state ครบ

### 3.2 Wizard สร้าง/แก้ (5 steps — **ชื่อ/ลำดับล็อกโดย Pattern Q ห้ามเปลี่ยน**)
| Step | ชื่อ (ล็อก) | เนื้อหาของ PR |
|---|---|---|
| 1 | **เลือกแหล่งที่มา** | 2 tile: `สร้างใหม่` / `จากใบขอซื้อเดิม` (คัดลอกหัว+รายการ ไม่คัดลอกเลขที่/ลายเซ็น/ประวัติ → รองรับ SC-12) |
| 2 | **ข้อมูลหลักใบขอซื้อ** | `.form-grid` 2 คอลัมน์: ผู้ขอ (auto) · หน่วยงาน* · วันที่เอกสาร* · วันที่ต้องการใช้* (≥ วันที่เอกสาร) · ประเภทการขอซื้อ* · ศูนย์ต้นทุนหลัก (picker soft-ref) · เหตุผลการขอซื้อ* · **ผู้ขายที่แนะนำ** (soft-ref หลายราย · ไม่บังคับ) · อ้างอิงภายนอก · หมายเหตุ |
| 3 | **รายการสินค้า** | **B2 v2 ทั้งชุด** — grid 9 ช่อง (26/auto/64/92/92/78/72/104/54) · item combobox + free-text · ส่วนลด % · VAT segmented ในแถวขยาย · ศูนย์ต้นทุนรายบรรทัด → ส่วนลดท้ายบิล (toggle) → หัก ณ ที่จ่าย (toggle · ฝั่งจ่าย) → สรุปยอด |
| 4 | **เอกสารแนบ** | upload-zone · pdf/jpg/png/xlsx ≤10MB · ลบได้เฉพาะ DRAFT |
| 5 | **ตรวจสอบและยืนยัน** | read-only ทั้งหมด + แถบตรวจงบ (mock) + สายอนุมัติที่ระบบจะใช้ → ปุ่ม `บันทึกแบบร่าง` / `บันทึกและส่งอนุมัติ` (เปิด **DOA slot picker** เลือกคนจริงต่อ slot) |
> หมายเหตุ: ร่างแรกของ PREBRIEF วางลำดับเป็น ข้อมูล › รายการ › ผู้ขาย › แนบ › ตรวจสอบ —
> ปรับให้ตรง Pattern Q ตาม golden rule ข้อ 2 (Q-document ใช้ archetype Q เท่านั้น) · บันทึกเป็น DIVERGENCE-0 ใน `_COVERAGE_R1.md`

### 3.3 View drawer (4 tabs ตาม Pattern Q #98)
1. **รายละเอียด** — header + line grid read-only + totals + ผู้ขายที่แนะนำ + เอกสารแนบ + ปุ่มตามสถานะ
2. **PDF** — Pattern H A4 preview ตาม print spec (pdfdoc declaration) + ปุ่มพิมพ์/ดาวน์โหลด
3. **ลายเซ็น** — Pattern I signature card list: slot ตามสาย DOA · avatar + ชื่อ + ตำแหน่ง + สถานะ (รออนุมัติ/อนุมัติ/ไม่อนุมัติ) + วันเวลา + เหตุผล
4. **ประวัติ** — timeline append-only: สร้าง · แก้ไข · ส่งอนุมัติ · อนุมัติราย slot · ไม่อนุมัติ · เรียกคืน · ยกเลิก (ผู้ทำ · เวลา ค.ศ. · ค่าเดิม→ค่าใหม่)

## 4. Data
### 4.1 Header
`pr_no` (PR-YYYY-NNNN · จาก ENG-DOC-NUM ห้าม gen เอง) · `doc_date` · `required_date` · `requester_id/name/avatar` · `department` ·
`cost_center_id` (soft-ref nullable) · `pr_type` (goods|service|asset) · `reason` · `status` · `currency`=THB ·
`subtotal` · `discount_total` · `vat_base` · `vat_amount` · `grand_total` · `budget_check` (mock: ok/remaining/budget_code) ·
`created_by/at` · `submitted_at` · `approved_at` · `cancel_reason`
### 4.2 Line
`line_no` · `item_id` (soft-ref nullable) · `item_text` (free-text) · `description` · `qty` · `uom_id` · `unit_price_est` ·
`discount_value` · `discount_type` (amt|pct) · `vat_mode` (vat7|novat|vat0) · `cost_center_id` · `line_total` · `note`
### 4.3 ตาราง append-only
`pr_approval_slot` (slot_seq · approver_id · approver_name · approver_position · decision · decided_at · reason) ·
`pr_history` (event · actor · at · before · after) · `pr_attachment` (file_name · size · uploaded_by/at)

## 5. Scenario ครบ (happy / alternate / exception)
| # | Scenario | ผลที่ต้องได้ |
|---|---|---|
| SC-01 | Happy — สร้าง → กรอกครบ → ส่งอนุมัติ → อนุมัติครบทุก slot | สถานะ APPROVED · ประวัติครบทุก event · ลายเซ็นครบทุกการ์ด |
| SC-02 | บันทึกร่างกลางทาง แล้วกลับมาแก้ต่อ | DRAFT แก้ได้ทุกช่อง · เลขที่ยังไม่ออกจริงจนกว่าจะ submit ([ASSUMED] จองเลขตอน submit) |
| SC-03 | Line เป็น free-text ไม่มีใน Item Master | บันทึกได้ ไม่ block (soft-ref) |
| SC-04 | ผู้อนุมัติคนหนึ่งไม่อนุมัติ + ใส่เหตุผล | REJECTED · slot ที่เหลือไม่ต้องตัดสิน · แจ้งผู้ขอ · ผู้ขอคัดลอกใบไปแก้ใหม่ได้ |
| SC-05 | ผู้ขอเรียกคืนใบระหว่างรออนุมัติ | กลับ DRAFT · ลายเซ็นที่อนุมัติไปแล้วถูก void (ยังคงอยู่ในประวัติ) |
| SC-06 | ยอดสุทธิเกินวงเงิน slot ที่เลือก | เตือนที่ step 5 · ต้องเลือกผู้อนุมัติระดับที่ครอบวงเงิน (matrix มาจาก DOA กลาง) |
| SC-07 | ตรวจงบไม่ผ่าน (mock) | แถบเตือนสีส้ม "งบไม่พอ (mock)" + `TODO: budget-control hook` — **ยังส่งอนุมัติได้** (ไม่ block รอบนี้) |
| SC-08 | แก้ไขหลังส่งอนุมัติ | ปุ่มแก้ไขถูกปิด · ต้องเรียกคืนก่อน (microcopy อธิบาย) |
| SC-09 | ยกเลิกใบที่อนุมัติแล้ว | ต้องใส่เหตุผล + ยืนยัน (destructive confirm) · CANCELLED · append ประวัติ |
| SC-10 | ไม่มีสิทธิ์อนุมัติแต่เปิดใบ | เห็นได้ ปุ่มอนุมัติไม่ขึ้น |
| SC-11 | แนบไฟล์เกิน 10MB / นามสกุลไม่รองรับ | error inline ไม่ล้มทั้งฟอร์ม |
| SC-12 | คัดลอกใบเดิมเป็นใบใหม่ | ได้ DRAFT ใหม่ · ไม่ copy เลขที่/ลายเซ็น/ประวัติ |
| SC-13 | รายการว่าง (0 บรรทัด) แล้วกดส่งอนุมัติ | block + microcopy "ต้องมีอย่างน้อย 1 รายการ" |
| SC-14 | วันที่ต้องการใช้ < วันที่เอกสาร | block inline validation |
| SC-15 | List ไม่มีข้อมูล / โหลดพัง | empty state + error state พร้อมปุ่มลองใหม่ |

## 6. Cross-boundary
- **soft-ref (picker ไม่ FK · nullable)**: Vendor Master F007 · Item F009/F010 · Cost Center F012 · หน่วยนับ
- **DOA (F019 DONE)**: สายอนุมัติ + วงเงิน มาจาก DOA กลาง — feature แค่ประกาศ + แสดง slot picker
- **forward-wire**: `budgetControl.check(pr)` → **mock** + `// TODO: budget-control hook (F117 · W7)`
- **ปลายทาง (hook เท่านั้น ห้าม gen จอ)**: F073 Compare Vendors · F078 PO (W3)

## 7. Coverage matrix (FN ↔ scenario ↔ จอ)
ดู `FUNCTION_CHECKLIST_F-PUR-PR.md` — FN-01..FN-24 ทุกตัวผูก scenario + จอ + จุดตรวจ
