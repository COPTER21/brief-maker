# DOCCFG_BRIEF — F-ACC-CN Credit Note
| Code | ชื่อ | Module | Preset | Reset | Scope | No-gap | Snap ส่งออก | Snap อนุมัติ+เซ็น |
|---|---|---|---|---|---|---|---|---|
| CN | ใบลดหนี้ (ลูกค้า) | ACC (AR) | {PREFIX}-{YYYY}-{run:4} → CN-2026-0001 | รายปี | global [DEFAULT] | ✓ | ✓ | ✓ |
จุดออกเลข: pending_approval → approved (ขั้นสุดท้าย) — ไม่ออกตอน draft/ส่งอนุมัติ (Iron 4)
จุดเก็บสำเนา: approved_final (อนุมัติครบ + ลายเซ็น) · sent_external (ส่งลูกค้า)
Dev: `cn.code = ENG-DOC-NUM.next('CN', ctx)` ใน transaction อนุมัติขั้นสุดท้าย · ห้าม format เอง
