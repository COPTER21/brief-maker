# HANDOFF — F-ACC-CN · Credit Note (ใบลดหนี้ลูกค้า) · Phase A → ba-done
> Lane W5P#2 · 2026-09-20 · dep AR Invoice = ba-done ✓ · **รอทีม vibe — Phase B ออกเอกสารหลัง HTML นิ่ง + ผ่าน re-gate html-review-fix-order**

## ทำอะไรไปแล้ว
S0 RIF 83% → S0.5 baseline (7 Must ✅ · 3 ⏭) → S1 PREBRIEF (S-01..16 · BR-01..10) + CHECKLIST FN 21 (.md/.html) → S1.5 → S1.8 (doa 3 tier/ntf/csq/doccfg/pdfdoc) → S2 HTML v9 (อ่าน SKILL.md ใหม่) → S3a WARN (BLOCK 0) → S3b PASS → S3c Playwright 30/30 → S4 BRD APPROVED

## ส่งมอบ
0_DIRECTION: RIF_v2 · BASELINE_ACC_CN · PREBRIEF · FUNCTION_CHECKLIST .md/.html · 1_HTML: F-ACC-CN_credit-note.html + _UX_CHECK_REPORT · _COVERAGE_R1 · _TECH_CHECK_S3c · 2_BRD: BRD_F-ACC-CN .md/.docx · 5_DECLARATIONS: DOA_BRIEF (3 tier) · NTF · CSQ · DOCCFG (CN) · CN_print-spec (ม.86/10) · DECLARATION_INDEX · build: output/2026-09-20/_qdoc_build/f-acc-cn.js (+kernel.js · pw_cn.py)

## ห้ามแตะ
โครง Pattern Q · B2 v2 engine · DOA slot picker (ห้าม chain hardcode) · hint/info-banner (#67.1) · ปุ่มสลับ view ขวาบน (#104) · DEMO badge (#105) · class toolbar (#106) · เปิดลดหนี้ไม่อ้างใบ (OQ-CN-01) · ทำหน้า Sales Return/RV/JE จริง
✅ vibe ได้: layout/microcopy/mock · ลำดับ field step 2 · ตาราง ref tab
**Phase B ต้องมี section "Demo-only elements":** `[data-demo="persona-switch"]` · `[data-demo="rv-simulate"]`

## ASSUMED / OQ + owner
OQ-CN-01 ≤คงเหลือ/ลดลอยปิด (ตามแผน · Strike) · OQ-CN-02 ยกเลิกหลังอนุมัติ = ไม่รองรับ (Strike) · OQ-CN-03 refund (Strike+Finance) · OQ-CN-04 tier DOA 50k/300k [DEFAULT] (Policy Center) · OQ-CN-05 กันยอดร่าง (Strike) · OQ-AR-06 role id (Policy Center) · [ASSUMED contract] Sales Return {sr_no, inv_no, line, qty_received} (W4-LITE) · CN reason master (config) · forward-wire JE F093

## DIVERGENCE / WARN
DIVERGENCE: ไม่มี · WARN S3a W-1..4 สืบทอด canonical · pdfdoc template/pdf = Phase B · kernel เพิ่ม hook `approveGuard` (ไม่กระทบ AR)

## คำสั่ง Phase B
html-review-fix-order → `run_state.py phase briefs/W5P/F-ACC-CN docs` → FRD (Sync Read DOA/NTF/CSQ/DOCCFG + Demo-only elements) → TC → UI Brief
