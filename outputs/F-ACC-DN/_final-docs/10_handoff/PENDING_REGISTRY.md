# Pending Registry — F-ACC-DN ใบลดหนี้ผู้ขาย (Debit Note)

1. **DSP-08** (2026-09-21, occurrence #2 ที่ F-ACC-DN 2026-09-23) — v9.1 SKELETON z regression: shared `.backdrop` ได้ global `--z-backdrop`(50) แต่ modal `.card` ไม่มี z → backdrop ทับ card → คลิก card = ปิด modal (flow อนุมัติกดไม่ได้)
   - แก้สำเนา: `.modal-overlay > *:not(.backdrop){position:relative;z-index:var(--z-modal)}` + uikit `assert_modal_card_topmost` (prove-by-revert)
   - **ทุก feature ที่ gen ด้วย v9.1 จะโดนซ้ำจนกว่าจะแก้ skeleton ต้นทาง** — DN โดนคลาสเดียวกันกับ CN
   - รายละเอียดเต็ม + หลักฐานอยู่ที่ `outputs/_SHARED/DESIGN_SYSTEM_PENDING.md`

2. คำถามเชิงธุรกิจและ integration ที่ยังต้องตัดสินใจอยู่ใน `PROPOSALS_outbound.md` (OQ-AP-06 role-ids · OQ-DN-05 legal ม.82/10 · OQ-DN-02 DOA cut · OQ-DN-04 revise-doc · OQ-DN-03/06 vendor-credit settlement · OQ-DN-07 CSQ · F-ACC-APINV/RTV/F093/VAT report [ASSUMED])
