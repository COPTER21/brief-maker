# NTF_BRIEF — F-ACC-CN Credit Note
> DOA events (doa_pending/doa_result) มาจาก DOA engine — ไม่ประกาศซ้ำ
| Event ID | Trigger | ผู้รับ | ข้อความ | Channel default | ปิดได้ |
|---|---|---|---|---|---|
| ar_cn_approved_applied | pending→approved (ครบสาย) | เจ้าหน้าที่ลูกหนี้ + พนักงานขาย | **{cn_no}** อนุมัติแล้ว ลดหนี้ {inv_no} ฿{grand} · คงค้างใหม่ ฿{outstanding} | in-app | ✓ |
| ar_cn_sent | approved→sent | ผู้ติดต่อลูกค้า (external) | ใบลดหนี้ **{cn_no}** อ้างใบกำกับ {inv_no} ยอด ฿{grand} (แนบ PDF) | ตาม preference ลูกค้า | ✗ |
| ar_cn_cancelled | →cancelled | ผู้สร้าง | **{cn_no/ร่าง}** ถูกยกเลิก: {reason} | in-app | ✓ |
