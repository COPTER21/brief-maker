# DOCCFG_BRIEF — F-ACC-DN Debit Note
| Code | ชื่อ | Module | Preset | Reset | Scope | No-gap | Snap ส่งออก | Snap อนุมัติ+เซ็น |
|---|---|---|---|---|---|---|---|---|
| DN | ใบลดหนี้ผู้ขาย (ฝั่งซื้อ) | ACC (AP) | {PREFIX}-{YYYY}-{run:4} → DN-2026-0001 | รายปี | global [DEFAULT] | ✓ | ✓ | ✓ |
จุดออกเลข: pending → approved (ขั้นสุดท้าย) · สำเนา: approved_final · sent_external
Dev: `dn.code = ENG-DOC-NUM.next('DN', ctx)` ในทรานแซกชันอนุมัติขั้นสุดท้าย
