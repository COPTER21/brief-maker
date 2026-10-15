# NTF_BRIEF — F-PUR-PR · PR ใบขอซื้อ
> ยิงผ่าน ENG-NOTIFY เท่านั้น — ห้าม hardcode ช่องทาง/เงื่อนไขใน feature
> **DOA events (doa_pending / doa_result / doa_escalate) มาจาก DOA engine อัตโนมัติ — ไม่อยู่ในใบนี้**

## Declared events (ธุรกิจของ feature เอง)
| Event ID | Trigger (อ้าง PREBRIEF §) | ผู้รับ | ข้อความ template | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| `pr_submitted` | S: DRAFT→PENDING_APPROVAL (§2) | ผู้ขอ (ยืนยันส่งแล้ว) | ส่งใบขอซื้อ **{pr_no}** เข้าสายอนุมัติแล้ว | in-app | ✓ |
| `pr_approved` | S: PENDING_APPROVAL→APPROVED ครบทุก slot (§2) | ผู้ขอ + ทีมจัดซื้อ | ใบขอซื้อ **{pr_no}** อนุมัติครบแล้ว — พร้อมเทียบราคาผู้ขาย | in-app+email | ✓ |
| `pr_rejected` | S: PENDING_APPROVAL→REJECTED (§2 · SC-04) | ผู้ขอ | ใบขอซื้อ **{pr_no}** ไม่ได้รับอนุมัติ — {reject_reason} | in-app+email | ✗ บังคับ |
| `pr_recalled` | S: PENDING_APPROVAL→DRAFT โดยผู้ขอ (SC-05) | ผู้อนุมัติทุก slot ที่ค้าง | ใบขอซื้อ **{pr_no}** ถูกเรียกคืนโดยผู้ขอ — ไม่ต้องพิจารณา | in-app | ✓ |
| `pr_cancelled` | S: →CANCELLED (SC-09) | ผู้ขอ + ผู้อนุมัติที่เคยเซ็น + ทีมจัดซื้อ | ใบขอซื้อ **{pr_no}** ถูกยกเลิก — {cancel_reason} | in-app | ✓ |
| `pr_budget_warning` | ผลตรวจงบ (mock) = ไม่พอ ที่ step 5 (SC-07) | ผู้ขอ + ผู้ดูแลงบหน่วยงาน | ใบขอซื้อ **{pr_no}** ยอด {grand_total} เกินงบคงเหลือ {remaining} (ตรวจจำลอง) | in-app | ✓ |
| `pr_attachment_added` | เพิ่มไฟล์แนบหลังส่งอนุมัติ (§FN-15) | ผู้อนุมัติขั้นปัจจุบัน | มีเอกสารแนบใหม่ในใบขอซื้อ **{pr_no}** | in-app | ✓ |

## Payload ต่อ event
`ref = {type:'PR', id: pr_id, no: pr_no}` + vars: `pr_no · grand_total · requester_name · reject_reason · cancel_reason · remaining`
ทุก event มี ref (soft-reference ไปเอกสาร) ✓

## เพิ่มเข้า Event Catalog (F-NOTIFY EVENT_GROUPS)
- กลุ่ม "เอกสารธุรกรรม" → ใช้ pattern `doc_status` เดิม สำหรับ `pr_submitted / pr_approved / pr_rejected / pr_recalled / pr_cancelled`
- กลุ่มใหม่ที่ต้องเพิ่ม: `pr_budget_warning` (เกณฑ์แจ้งเฉพาะ · ผูก forward-wire W7) · `pr_attachment_added` (ไฟล์แนบ)

## Dev wiring note
- `ENG-NOTIFY.emit(event_id, {ref, vars})` ที่ transition ตาม trigger — **ห้ามเช็ค preference เอง ห้ามระบุ email/LINE ใน feature**
- `pr_budget_warning` รอบนี้ยิงจาก mock — เมื่อ F117 Budget Control (W7) พร้อม เปลี่ยน trigger เป็นผล engine จริง (`TODO: budget-control hook`)
