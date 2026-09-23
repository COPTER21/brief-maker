# Declaration Index — F-ACC-DN ใบลดหนี้ผู้ขาย (F097)

> declarations ที่ **ผู้ใช้เลือกไว้ที่ kickoff** (C3.10) — รันหลัง step 7 · ผลลัพธ์ = ใบประกาศให้ dev ตั้งค่าระบบจริง
> Regenerated 2026-09-23 (superseded upstream stubs ใน `Pack Brief Feature/F-ACC-DN/5_DECLARATIONS/`)

| ท่อ | chip | detect | ไฟล์ (ฉบับเต็ม) | ผล |
|---|---|---|---|---|
| doa | ✓ | ✓ 1 สาย · มีวงเงิน 3 tier | `DOA_BRIEF_F-ACC-DN.md` | ตรง (approveGuard ใช้ dnRoom · FIX-01) |
| ntf | ✓ | ✓ 3 events (dn.issued/dn.sent/dn.cancelled) | `NTF_BRIEF_F-ACC-DN.md` | ตรง |
| csq | ✓ | ✓ AC (+EC actual) | `CSQ_BRIEF_F-ACC-DN.md` | ตรง (input-VAT gated by vendorCn · ม.82/10) |
| doccfg | ✓ | ✓ DN → DN-YYYY-NNNN | `DOCCFG_BRIEF_F-ACC-DN.md` | ตรง |
| pdfdoc | ✓ | ✓ (step 2) | `../_print/` (template + sample.pdf + print-spec) | ตรง |

**DIVERGENCE:** ไม่มี

## OQ รวมจาก declarations (ยกไป step-12 PROPOSALS)
- **OQ-DN-02** — จุดตัดวงเงิน DOA 50k/300k + role ต่อ tier [DEFAULT]
- **OQ-AP-06** — role-ids `role-mgr-pur`/`role-mgr-acc`/`role-cfo` [ASSUMED]
- **OQ-DN-05** — legal basis input-VAT ม.82/10 (เดือนที่ได้รับใบลดหนี้ผู้ขาย) [ASSUMED — mirror CN]
- **OQ-DN-03 / OQ-DN-06** — CSQ FC / เครดิตคงเหลือ→settlement/refund path [ASSUMED = ไม่ยิง FC]
- **OQ-DN-07** — CSQ profile-id + event id (late-fill vendorCn แยก event ไหม)
- **CSQ-OQ-DN-1** — EC สำหรับ DISC/PRICE/no-PO expense (kind=actual, base ติดลบ) [ASSUMED]
