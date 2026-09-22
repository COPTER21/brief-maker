# Pending Registry — F-ACC-CN ใบลดหนี้ลูกค้า (Credit Note)

1. **DSP-08** (2026-09-21) — v9.1 SKELETON z regression: shared `.backdrop` ได้ global `--z-backdrop`(50) แต่ modal `.card` ไม่มี z → backdrop ทับ card → คลิก card = ปิด modal (flow อนุมัติกดไม่ได้)
   - แก้สำเนา: `.modal-overlay > *:not(.backdrop){position:relative;z-index:var(--z-modal)}` + uikit `assert_modal_card_topmost` (prove-by-revert)
   - **ทุก feature ที่ gen ด้วย v9.1 จะโดนซ้ำจนกว่าจะแก้ skeleton ต้นทาง**
   - รายละเอียดเต็ม + หลักฐานอยู่ที่ `outputs/_SHARED/DESIGN_SYSTEM_PENDING.md`

2. คำถามเชิงธุรกิจและ integration ที่ยังต้องตัดสินใจอยู่ใน `PROPOSALS_outbound.md` (OQ-CN-01..04, OQ-AR-06 role-ids, F094/F090/F093/F105 [ASSUMED])
