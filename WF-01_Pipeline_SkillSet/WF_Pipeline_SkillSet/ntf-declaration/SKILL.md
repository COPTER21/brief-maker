---
name: ntf-declaration
description: >
  Companion skill ฉีด context เรื่อง Notification (ENG-NOTIFY — F-NOTIFY Notification Center) เข้า pipeline
  ตอนทำ FRD และ HTML ของ feature ที่มี event แจ้งเตือน (สถานะเอกสารเปลี่ยน, มอบหมายงาน, แจ้งเฉพาะ เช่น low stock,
  ไฟล์แนบใหม่, ส่งเอกสารให้ลูกค้า) แล้วออก NTF_BRIEF_[F-xxx].md = ใบประกาศ event ที่ dev เอาไป wire เข้า
  ENG-NOTIFY ได้ทันที — feature ประกาศเท่านั้น ห้าม hardcode ช่องทาง/เงื่อนไขแจ้งเตือนใน feature
  ★ หัวใจ: แยก 2 แหล่ง event — (1) มี DOA → doa_pending/doa_result มาจาก DOA engine อัตโนมัติ ห้ามประกาศซ้ำ
  (2) event ธุรกิจของ feature เอง → ต้องประกาศที่นี่ พร้อม trigger point ที่ผูก state transition จริงจาก FRD 03_LOGIC
  ใช้เมื่อ user พูดถึง "ntf-declaration", "ทำ NTF brief", "ประกาศ notification", "แจ้งเตือนของ feature",
  "set notification", "notification hooks", "wire ENG-NOTIFY", "เตรียม notify entry" — และใช้อัตโนมัติทุกครั้งที่รัน
  frd-generator กับ feature ที่ติด chip 🔔 ใน WAVE_PLAN แม้ไม่เรียกชื่อ skill
  ★ ไม่ใช่ standalone — เป็น companion (Sync Read F-NOTIFY event catalog)
---

## เมื่อไหร่ต้องรัน
1. Feature ติด chip **🔔 Notify** ใน WAVE_PLAN_SALES.html (22 ตัว) — บังคับ
2. FRD/HTML มี action ที่คนอื่นต้องรู้: เปลี่ยนสถานะเอกสาร · มอบหมาย/assign · เกณฑ์แจ้งเฉพาะ (low stock, เกิน SLA, เกินวงเงิน) · ไฟล์แนบ · ส่งออกนอกระบบ

## Input
- FRD Pack ของ feature (บังคับ: 03_LOGIC state machine + 05_RULES) หรือ PREBRIEF §NTF Hooks (โหมด early-draft)
- Event catalog ปัจจุบันจาก F-NOTIFY (`f-notify.html` → EVENT_GROUPS) — Sync Read ห้าม copy ค้าง

## ขั้นตอน
1. อ่าน state machine + rules → list event candidates
2. **ตัด event ที่ DOA ยิงอยู่แล้ว** (doa_pending/doa_result/doa_escalate) — ประกาศซ้ำ = BLOCK
3. ต่อ event: กำหนด id (`{feature}_{event}` snake_case เช่น `so_confirmed`, `inv_low_stock`), trigger point (transition ไหน/เงื่อนไขไหน — อ้าง FRD § ได้), ผู้รับ (role หรือ "ผู้เกี่ยวข้องกับเอกสาร": ผู้สร้าง/ผู้ขาย/ผู้อนุมัติ), payload (ref_id + ตัวแปรในข้อความ), ข้อความ template (ไทย, มี **ตัวหนา** ที่เลขเอกสาร), default channel (in-app เสมอ / email เมื่อสำคัญ), บังคับ/ปิดได้
4. เช็คชนกับ event catalog เดิม — ชื่อซ้ำ/ความหมายซ้อน → ใช้ตัวเดิม
5. ออก `NTF_BRIEF_[F-xxx].md` + แนะบรรทัดที่ต้องเพิ่มใน EVENT_GROUPS ของ F-NOTIFY (ถ้าเป็น event กลุ่มใหม่)

## Output: NTF_BRIEF_[F-xxx].md (โครง)
```md
# NTF_BRIEF — F-SO-001 Sales Order
> ยิงผ่าน ENG-NOTIFY เท่านั้น — ห้าม hardcode · DOA events มาอัตโนมัติ ไม่อยู่ในใบนี้

| Event ID | Trigger (อ้าง FRD) | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| so_confirmed | S: draft→confirmed (03_LOGIC §2.1) | ผู้สร้าง SO + ทีมคลัง | **{so_id}** ลูกค้ายืนยันแล้ว — พร้อมเข้าคิวหยิบสินค้า | in-app | ✓ |
| so_credit_block | rule CR-01 เกินวงเงิน (05_RULES) | ผจก.ขาย | **{so_id}** เกินวงเงินเครดิต — ต้องการ override | in-app+email | ✗ บังคับ |

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
- กลุ่ม "เอกสารธุรกรรม" → ใช้ doc_status เดิม (ไม่เพิ่ม) / เพิ่มใหม่: ...
## Dev wiring note
- จุดเรียก: ENG-NOTIFY.emit(event_id, {ref, vars}) ที่ transition ตาม trigger — ห้ามเช็ค preference เอง
```

## กติกาตายตัว (Iron)
- ห้ามประกาศ doa_pending/result/escalate ซ้ำ (DOA engine เจ้าของ)
- ห้ามระบุ "ส่ง email/LINE" ใน logic feature — channel เป็นของ user preference + config กลาง
- ข้อความ template อยู่ในใบประกาศ ไม่ฝังใน code feature
- ทุก event ต้องมี ref (soft-reference ไปเอกสาร) ยกเว้น system broadcast
