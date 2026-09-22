# NTF_BRIEF — F-ACC-DN Debit Note
> DOA events มาจาก DOA engine — ไม่ประกาศซ้ำ
| Event ID | Trigger | ผู้รับ | ข้อความ | Channel | ปิดได้ |
|---|---|---|---|---|---|
| ap_dn_approved_applied | pending→approved | เจ้าหน้าที่เจ้าหนี้ + ผู้จัดการจัดซื้อ | **{dn_no}** ลดหนี้ {api_no} ฿{grand} · คงค้างจ่ายใหม่ ฿{outstanding} | in-app | ✓ |
| ap_dn_sent | approved→sent | ผู้ติดต่อผู้ขาย (external) | ใบลดหนี้ **{dn_no}** อ้างใบกำกับ {vendor_invoice_no} ยอด ฿{grand} (แนบ PDF) | email | ✗ |
| ap_dn_cancelled | →cancelled | ผู้สร้าง | ใบลดหนี้ {ref} ถูกยกเลิก: {reason} | in-app | ✓ |
